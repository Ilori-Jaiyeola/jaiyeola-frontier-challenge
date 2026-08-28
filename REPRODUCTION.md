# Reproduction Guide

Written for someone starting from a totally clean machine.

## 0. Versions used

| Tool | Version | Notes |
|---|---|---|
| OS | | |
| Language runtime (Python/Node/etc.) | | |
| Package manager | | |
| Coding agent | | |
| Key libraries | | pin exact versions in requirements.txt / package.json |

## 1. Setup

```bash
git clone <repo-url>
cd <repo>
# language-specific env setup, e.g.:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Required data

<!-- What input data is needed, where it comes from (public/synthetic/
approved-anonymous per rule book), and where it must be placed. -->

## 3. Run the baseline

```bash
<exact command>
```
**Expected output:** <!-- what a correct run looks like -->
**Approx runtime / cost:** <!-- wall-clock, API cost if any -->

## 4. Run the advanced solution

```bash
<exact command>
```
**Expected output:**
**Approx runtime / cost:**

## 5. Run the evaluation (baseline vs. advanced)

```bash
python eval/harness.py --baseline baseline/ --advanced advanced/ --cases eval/cases/
```
**Expected output:** a comparison table (see `eval/harness.py`) written to
`eval/results/latest.json` and printed to stdout.

## 5b. Automatic CI (GitHub Actions)

This repo runs the same comparison automatically on every push, via
`.github/workflows/ci.yml`. Once you `git push`, check the **Actions** tab
on GitHub — no setup needed beyond having the workflow file in the repo.
Judges can also re-trigger it manually from the Actions tab
(`workflow_dispatch`) and download the `eval-results` artifact.

## 6. Troubleshooting

<!-- Known gotchas, e.g. rate limits, auth setup, platform-specific issues -->
