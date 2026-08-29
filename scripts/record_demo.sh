#!/usr/bin/env bash
# Run this ON CAMERA during recording -- it walks through baseline,
# the standout advanced case, and the full comparison, printing clear
# section headers so you never have to remember which command is next.
# Run from the repo root: bash scripts/record_demo.sh
set -e

pause() { read -rp "   [press Enter to continue] " _; }

echo "=============================================="
echo " 1. BASELINE — naive keyword matching"
echo "=============================================="
python3 -c "
import sys, json
sys.path.insert(0, 'baseline')
import solution
cases = json.load(open('eval/cases/cases.json'))
for c in cases:
    print(c['id'], '->', solution.solve(c)['result'])
"
pause

echo "=============================================="
echo " 2. THE STANDOUT CASE — case-16 (adversarial)"
echo "=============================================="
python3 -c "
import json
c = [c for c in json.load(open('eval/cases/cases.json')) if c['id']=='case-16'][0]
print('Evidence text:')
print(' ', c['evidence'])
print()
print('Expected label:', c['expected'])
"
pause

echo "--- advanced/solution.py on case-16 ---"
python3 -c "
import sys, json
sys.path.insert(0, 'advanced')
import solution
c = [c for c in json.load(open('eval/cases/cases.json')) if c['id']=='case-16'][0]
r = solution.solve(c)
print('Result:', r['result'])
print('Reason:', r['reason'])
"
pause

echo "=============================================="
echo " 3. FULL COMPARISON — baseline vs advanced, all 16 cases"
echo "=============================================="
python3 eval/harness.py --baseline baseline/ --advanced advanced/ --cases eval/cases/ --out eval/results/latest.json
pause

echo "=============================================="
echo " 4. PROOF — now open eval/results/latest.json"
echo "    (eval -> results -> latest.json, opens in TextEdit)"
echo "=============================================="

