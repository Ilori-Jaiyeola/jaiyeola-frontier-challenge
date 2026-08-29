# Reproduction Guide

Written for someone starting from a totally clean machine.

## 0. Versions used

| Tool | Version | Notes |
|---|---|---|
| OS | any (Linux/macOS/Windows) | no OS-specific code |
| Python | 3.12.3 (developed against) | 3.9+ should work — only stdlib used (`json`, `re`, `pathlib`) |
| Package manager | pip | `requirements.txt` is currently empty — no third-party dependencies |
| Coding agent | Claude (claude.ai chat, free plan) | see README Section 8 for full disclosure |

## 1. Setup

```bash
git clone <repo-url>
cd micro1-frontier-challenge-2026
# No virtual env or pip install strictly required — stdlib only.
# If you prefer isolation anyway:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # currently empty, no-op
```

## 2. Required data

All data is bundled in the repo and synthetic — no external download, no
API key, no network access needed:
- `eval/knowledge_base/vuln_db.json` — a small synthetic vulnerability
  knowledge base (invented "SYN-####-####" IDs, not real CVEs) modeling
  the shape of real advisories.
- `eval/cases/cases.json` — 10 synthetic scan findings with known-correct
  labels, used as ground truth for scoring.

## 3. Run the baseline alone

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'baseline')
import solution
cases = json.load(open('eval/cases/cases.json'))
for c in cases:
    print(c['id'], '->', solution.solve(c)['result'])
"
```
**Expected output:** one line per case (`case-01 -> Confirmed`, etc).
**Approx runtime:** under 1 second. **Cost:** $0 — no API calls.

## 4. Run the advanced solution alone

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'advanced')
import solution
cases = json.load(open('eval/cases/cases.json'))
for c in cases:
    r = solution.solve(c)
    print(c['id'], '->', r['result'], '|', r['reason'])
"
```
**Expected output:** one line per case with label + plain-English reason.
**Approx runtime:** under 1 second. **Cost:** $0 — no API calls.

## 5. Run the evaluation (baseline vs. advanced)

```bash
python3 eval/harness.py --baseline baseline/ --advanced advanced/ --cases eval/cases/ --out eval/results/latest.json
```
**Expected output:**
```
=== Baseline vs. Advanced ===
metric                     baseline       advanced          delta
pass_rate                    0.5625         1.0000        +0.4375
mean_score                   0.5625         1.0000        +0.4375
...
Full results written to eval/results/latest.json
```
Baseline should score 9/16 (56.25%), advanced should score 16/16 (100%).
**Approx runtime:** under 1 second. **Cost:** $0.

## 5b. Automatic CI (GitHub Actions)

This repo runs the same comparison automatically on every push, via
`.github/workflows/ci.yml`. Once you `git push`, check the **Actions** tab
on GitHub — no setup needed beyond having the workflow file in the repo.
Judges can also re-trigger it manually from the Actions tab
(`workflow_dispatch`) and download the `eval-results` artifact.

## 6. Troubleshooting

- **`FileNotFoundError` for `vuln_db.json`:** run commands from the repo
  root, not from inside `baseline/`/`advanced/`/`eval/` — the paths in
  `advanced/solution.py` are relative to the repo root via `Path(__file__)`.
- **`ModuleNotFoundError: solution`:** the `sys.path.insert(0, 'baseline')`
  (or `'advanced'`) line in the one-liners above is required since these
  aren't installed packages — just local files.
- **Advanced solution's memory (dedupe) behavior:** `_session_state` is
  module-level, so it persists across calls within one Python process/run
  but resets on a fresh run — this is intentional (session-scoped memory,
  not persistent storage).
