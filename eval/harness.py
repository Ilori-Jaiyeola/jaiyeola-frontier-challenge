#!/usr/bin/env python3
"""
Generic baseline-vs-advanced evaluation harness.

Purpose: run a set of test cases through both solutions, measure
correctness + cost/time, and produce a reproducible comparison table
and JSON result file. Adapt `run_case()` and `score_case()` once the
actual problem and its acceptance tests are known — the surrounding
scaffolding (timing, logging, retries, reporting) stays the same.

Usage:
    python eval/harness.py --baseline baseline/ --advanced advanced/ \
        --cases eval/cases/ --out eval/results/latest.json
"""

import argparse
import importlib.util
import json
import statistics
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class CaseResult:
    case_id: str
    solution: str  # "baseline" or "advanced"
    passed: bool
    score: float  # 0.0-1.0, or a domain-specific metric
    latency_s: float
    error: str = ""
    notes: str = ""


@dataclass
class RunSummary:
    solution: str
    n_cases: int
    n_passed: int
    pass_rate: float
    mean_score: float
    mean_latency_s: float
    p95_latency_s: float
    results: list = field(default_factory=list)


def load_solution_module(solution_dir: Path):
    """Expects solution_dir/solution.py exposing a `solve(case: dict) -> dict`."""
    entry = solution_dir / "solution.py"
    if not entry.exists():
        raise FileNotFoundError(f"No solution.py found in {solution_dir}")
    spec = importlib.util.spec_from_file_location(f"{solution_dir.name}_solution", entry)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "solve"):
        raise AttributeError(f"{entry} must define solve(case: dict) -> dict")
    return module


def load_cases(cases_dir: Path):
    """Expects one JSON file per case, or a single cases.json list."""
    cases = []
    single = cases_dir / "cases.json"
    if single.exists():
        cases = json.loads(single.read_text())
    else:
        for f in sorted(cases_dir.glob("*.json")):
            cases.append(json.loads(f.read_text()))
    if not cases:
        print(f"WARNING: no test cases found in {cases_dir}. "
              f"Add eval/cases/cases.json (a list of case dicts) or "
              f"one JSON file per case.", file=sys.stderr)
    return cases


def score_case(case: dict, output: dict) -> tuple[bool, float]:
    """
    Domain-specific scoring. Replace once the acceptance test format is known.
    Default: exact-match on an 'expected' key if present, else 'ran without
    error' counts as a pass with score 1.0.
    """
    if "expected" in case:
        passed = output.get("result") == case["expected"]
        return passed, 1.0 if passed else 0.0
    return True, 1.0


def run_case(module, case: dict, solution_name: str) -> CaseResult:
    start = time.perf_counter()
    try:
        output = module.solve(case)
        latency = time.perf_counter() - start
        passed, score = score_case(case, output)
        return CaseResult(
            case_id=case.get("id", "unknown"),
            solution=solution_name,
            passed=passed,
            score=score,
            latency_s=latency,
        )
    except Exception as e:
        latency = time.perf_counter() - start
        return CaseResult(
            case_id=case.get("id", "unknown"),
            solution=solution_name,
            passed=False,
            score=0.0,
            latency_s=latency,
            error=f"{type(e).__name__}: {e}",
        )


def summarize(solution_name: str, results: list[CaseResult]) -> RunSummary:
    n = len(results)
    n_passed = sum(1 for r in results if r.passed)
    latencies = sorted(r.latency_s for r in results) or [0.0]
    p95_idx = max(0, int(len(latencies) * 0.95) - 1)
    return RunSummary(
        solution=solution_name,
        n_cases=n,
        n_passed=n_passed,
        pass_rate=n_passed / n if n else 0.0,
        mean_score=statistics.mean(r.score for r in results) if n else 0.0,
        mean_latency_s=statistics.mean(latencies),
        p95_latency_s=latencies[p95_idx],
        results=[asdict(r) for r in results],
    )


def print_comparison(baseline: RunSummary, advanced: RunSummary):
    print("\n=== Baseline vs. Advanced ===")
    print(f"{'metric':<20}{'baseline':>15}{'advanced':>15}{'delta':>15}")
    rows = [
        ("pass_rate", baseline.pass_rate, advanced.pass_rate),
        ("mean_score", baseline.mean_score, advanced.mean_score),
        ("mean_latency_s", baseline.mean_latency_s, advanced.mean_latency_s),
        ("p95_latency_s", baseline.p95_latency_s, advanced.p95_latency_s),
    ]
    for name, b, a in rows:
        delta = a - b
        print(f"{name:<20}{b:>15.4f}{a:>15.4f}{delta:>+15.4f}")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--advanced", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("eval/results/latest.json"))
    args = parser.parse_args()

    cases = load_cases(args.cases)
    if not cases:
        sys.exit(1)

    baseline_module = load_solution_module(args.baseline)
    advanced_module = load_solution_module(args.advanced)

    baseline_results = [run_case(baseline_module, c, "baseline") for c in cases]
    advanced_results = [run_case(advanced_module, c, "advanced") for c in cases]

    baseline_summary = summarize("baseline", baseline_results)
    advanced_summary = summarize("advanced", advanced_results)

    print_comparison(baseline_summary, advanced_summary)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "baseline": asdict(baseline_summary),
        "advanced": asdict(advanced_summary),
    }, indent=2))
    print(f"Full results written to {args.out}")


if __name__ == "__main__":
    main()
