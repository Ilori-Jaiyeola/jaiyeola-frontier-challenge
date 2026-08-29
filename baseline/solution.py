"""
Baseline: naive keyword-based triage.

This represents the "simple script or template" baseline option from the
challenge brief -- specifically, it models what happens when an analyst
just reads the scanner's own description text at face value with no
independent verification. It looks ONLY at wording in raw_description,
never checks service_version against real affected ranges, never looks
at evidence quality, and has no memory across findings.

Must expose: solve(case: dict) -> dict
"""


def solve(case: dict) -> dict:
    text = case.get("raw_description", "").lower()

    # Naive rule: if the scanner's own text sounds confident/severe, trust it.
    strong_words = ["is vulnerable", "is using default", "detected version",
                    "matches a known", "confirmed"]
    weak_words = ["may be", "may allow", "possibly"]

    if any(w in text for w in strong_words):
        label = "Confirmed"
    elif any(w in text for w in weak_words):
        label = "Needs Verification"
    else:
        label = "Confirmed"  # default: naive baseline trusts the scanner

    return {
        "result": label,
        "reason": "Keyword match on scanner description text only -- no "
                  "version check, no evidence check, no cross-finding memory.",
    }
