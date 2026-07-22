import json
import math
from db.models import RepositoryMetric

LICENSE_WEIGHTS = {
    "MIT": 0.5,
    "BSD-3-Clause": 1.0,
    "Apache-2.0": 1.5,
    "MPL-2.0": 4.0,
    "LGPL-3.0": 6.0,
    "GPL-3.0": 8.0,
    "AGPL-3.0": 10.0,
    "SSPL": 10.0,
    "BSL-1.1": 9.0,
}

def calculate_fmdi(metric: RepositoryMetric) -> float:
    """
    Framework Migration & Displacement Index (FMDI).
    Calculates adoption/displacement velocity based on AST shift count, contributor retention, and 24h commits.
    """
    shifts = []
    if metric.framework_shifts:
        try:
            shifts = json.loads(metric.framework_shifts)
        except (json.JSONDecodeError, TypeError):
            shifts = []
            
    shift_factor = len(shifts) * 1.5 + 1.0
    churn_retention = max(0.01, 1.0 - metric.contributor_churn)
    velocity_log = math.log10(max(1, metric.commit_velocity_24h) + 1)
    
    fmdi = shift_factor * churn_retention * velocity_log
    return round(fmdi, 3)

def calculate_cffi(metric: RepositoryMetric) -> float:
    """
    Contributor Flight & Fragmentation Index (CFFI).
    Measures maintainer abandonment risk using contributor churn and issue delta.
    """
    churn = metric.contributor_churn
    issue_delta_factor = max(0, metric.open_issues_delta) * 0.1
    cffi = (churn * 7.0) + min(3.0, issue_delta_factor)
    return round(min(10.0, max(0.0, cffi)), 3)

def calculate_prei(metric: RepositoryMetric) -> float:
    """
    Production Readiness & Edge Optimization Index (PREI).
    Evaluates enterprise deployability based on quantization weight formats and fine-tuning frameworks.
    """
    formats = []
    if metric.model_weight_formats:
        try:
            formats = json.loads(metric.model_weight_formats)
        except (json.JSONDecodeError, TypeError):
            formats = []

    stacks = []
    if metric.fine_tuning_frameworks:
        try:
            stacks = json.loads(metric.fine_tuning_frameworks)
        except (json.JSONDecodeError, TypeError):
            stacks = []

    score = 2.0  # Baseline
    for fmt in formats:
        fmt_upper = str(fmt).upper()
        if "GGUF" in fmt_upper:
            score += 2.0
        elif "AWQ" in fmt_upper:
            score += 2.0
        elif "SAFETENSORS" in fmt_upper:
            score += 1.5
        elif "FP8" in fmt_upper:
            score += 1.5

    for stack in stacks:
        score += 1.0

    return round(min(10.0, score), 3)

def calculate_llrs(metric: RepositoryMetric) -> float:
    """
    License Toxicity & Legal Liability Score (LLRS).
    Computes legal risk exposure based on license restrictive weight and dynamic drift detection.
    """
    lic = metric.license_type or "Apache-2.0"
    base_weight = LICENSE_WEIGHTS.get(lic, 2.0)
    
    if metric.license_drift:
        base_weight *= 2.0
        
    return round(min(10.0, base_weight), 3)
