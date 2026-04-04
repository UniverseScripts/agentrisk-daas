import os
import asyncio
import httpx
from datetime import datetime, timedelta, timezone
import json

from db.connection import AsyncSessionLocal
from sqlalchemy.dialects.postgresql import insert
import db.models

# Hardcoded, deterministic Target Repository Matrix (Top 50 AI/ML)
TARGET_REPOSITORIES = [
    "pytorch/pytorch", "huggingface/transformers", "meta-llama/llama3",
    "langchain-ai/langchain", "openai/openai-python", "milvus-io/milvus",
    "qdrant/qdrant", "vllm-project/vllm", "microsoft/DeepSpeed",
    "ggerganov/llama.cpp", "ollama/ollama", "dmlc/xgboost",
    "microsoft/LightGBM", "scikit-learn/scikit-learn", "keras-team/keras",
    "tensorflow/tensorflow", "google-research/google-research", "huggingface/diffusers",
    "CompVis/stable-diffusion", "stability-ai/stablediffusion", "runwayml/stable-diffusion",
    "AUTOMATIC1111/stable-diffusion-webui", "awslabs/gluon-ts", "lk-geimfari/awesomedata",
    "facebookresearch/faiss", "ray-project/ray", "huggingface/peft",
    "huggingface/accelerate", "rwightman/pytorch-image-models", "OpenPipe/OpenPipe",
    "unslothai/unsloth", "sgl-project/sglang", "lmsysorg/fschat",
    "baichuan-inc/Baichuan2", "QwenLM/Qwen", "THUDM/ChatGLM-6B",
    "THUDM/ChatGLM2-6B", "01-ai/Yi", "mistralai/mistral-src",
    "bclavie/RAGatouille", "deepset-ai/haystack", "run-llama/llama_index",
    "weaviate/weaviate", "chroma-core/chroma", "lancedb/lancedb",
    "openai/whisper", "m-bain/whisperx", "comfyanonymous/ComfyUI",
    "lllyasviel/ControlNet", "lllyasviel/Fooocus"
]

GRAPHQL_URL = "https://api.github.com/graphql"

async def fetch_repository_metrics(client: httpx.AsyncClient, repo_name: str, since_dt: datetime) -> dict | None:
    owner, name = repo_name.split("/")
    since_iso = since_dt.isoformat()
    issue_closed_query = f"repo:{repo_name} is:issue closed:>={since_iso}"
    issue_opened_query = f"repo:{repo_name} is:issue created:>={since_iso}"

    query = """
    query ($owner: String!, $name: String!, $since: GitTimestamp!, $issueClosedQuery: String!, $issueOpenedQuery: String!) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history(since: $since) {
                totalCount
                nodes {
                  author {
                    email
                    user {
                      id
                    }
                  }
                }
              }
            }
          }
        }
        forks(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            createdAt
          }
        }
      }
      closedIssues: search(query: $issueClosedQuery, type: ISSUE, first: 1) {
        issueCount
      }
      openedIssues: search(query: $issueOpenedQuery, type: ISSUE, first: 1) {
        issueCount
      }
      rateLimit {
        remaining
      }
    }
    """
    variables = {
        "owner": owner,
        "name": name,
        "since": since_iso,
        "issueClosedQuery": issue_closed_query,
        "issueOpenedQuery": issue_opened_query
    }

    try:
        response = await client.post(GRAPHQL_URL, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        
        # Rate limit perimeter mapping
        rate_limit = data.get("data", {}).get("rateLimit", {}).get("remaining", 5000)
        if rate_limit < 500:
            print(f"WARNING: Rate limit extremely low ({rate_limit}). Approaching shadowban margin.")
            if rate_limit < 100:
                 return {"rate_limited": True}

        repo_data = data.get("data", {}).get("repository", {})
        if not repo_data or not repo_data.get("defaultBranchRef"):
             return None

        # Commits & Authors
        history = repo_data["defaultBranchRef"]["target"]["history"]
        total_commits_past_24h = history["totalCount"]
        
        unique_authors = set()
        for node in history["nodes"]:
            author = node.get("author", {})
            identifier = author.get("email") or str(author.get("user", {}).get("id"))
            if identifier:
                unique_authors.add(identifier)
        
        unique_commit_authors_past_24h = len(unique_authors)

        # Churn Formula
        if total_commits_past_24h == 0:
            contributor_churn = 0.0
        else:
            contributor_churn = 1.0 - (unique_commit_authors_past_24h / total_commits_past_24h)

        # Forks Delta 24h
        forks_data = repo_data.get("forks", {}).get("nodes", [])
        fork_velocity_24h = sum(1 for f in forks_data if datetime.fromisoformat(f["createdAt"].replace('Z', '+00:00')) >= since_dt)

        # Issues Delta (Opened - Closed)
        closed_issues = data.get("data", {}).get("closedIssues", {}).get("issueCount", 0)
        opened_issues = data.get("data", {}).get("openedIssues", {}).get("issueCount", 0)
        open_issues_delta = opened_issues - closed_issues

        return {
            "rate_limited": False,
            "repo_name": repo_name,
            "commit_velocity_24h": total_commits_past_24h,
            "open_issues_delta": open_issues_delta,
            "fork_velocity_24h": fork_velocity_24h,
            "contributor_churn": float(contributor_churn)
        }

    except Exception as e:
        print(f"Failed to fetch {repo_name}: {e}")
        return None

async def ingest_metrics():
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("CRITICAL: GITHUB_TOKEN environment variable missing.")
        return

    since_dt = datetime.now(timezone.utc) - timedelta(days=1)
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json",
    }

    metrics_payload = []
    
    async with httpx.AsyncClient(headers=headers, timeout=20.0) as client:
        for repo_name in TARGET_REPOSITORIES:
            result = await fetch_repository_metrics(client, repo_name, since_dt)
            if not result:
                continue
            if result.get("rate_limited"):
                print("ABORTING: GitHub Rate limit depleted. Saving current payload...")
                break
            
            result.pop("rate_limited")
            result["timestamp"] = datetime.now(timezone.utc)
            metrics_payload.append(result)
            
            # Artificial sleep to reduce burst and lower ban probability 
            await asyncio.sleep(0.1)

    if not metrics_payload:
        print("No metrics extracted. Exiting.")
        return

    # Asynchronous Database Ingestion (Idempotent Upsert)
    async with AsyncSessionLocal() as session:
        # Utilize PostgreSQL ON CONFLICT DO UPDATE clause
        stmt = insert(db.models.RepositoryMetric).values(metrics_payload)
        stmt = stmt.on_conflict_do_update(
            index_elements=['repo_name', 'timestamp'],
            set_={
                'commit_velocity_24h': stmt.excluded.commit_velocity_24h,
                'open_issues_delta': stmt.excluded.open_issues_delta,
                'fork_velocity_24h': stmt.excluded.fork_velocity_24h,
                'contributor_churn': stmt.excluded.contributor_churn
            }
        )
        await session.execute(stmt)
        await session.commit()
    print(f"Successfully ingested {len(metrics_payload)} records into repository_metrics ledger.")

if __name__ == "__main__":
    asyncio.run(ingest_metrics())
