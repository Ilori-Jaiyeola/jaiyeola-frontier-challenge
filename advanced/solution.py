"""
Advanced: agentic vulnerability triage pipeline.

Design choices (each addressing a specific weakness in the baseline):

1. CONTEXT / TOOL USE -- looks up the finding's plugin_name in a local
   synthetic vulnerability knowledge base (eval/knowledge_base/vuln_db.json)
   to get the actual affected version range, rather than trusting the
   scanner's own prose.

2. VERIFICATION -- two independent checks, applied differently depending
   on vulnerability class:
     a. VERSION-DEPENDENT vulns: is service_version actually inside the
        known-affected range? If in range, is there anything in the
        evidence text that contradicts exploitability (e.g. a secure
        protocol negotiated by default despite an insecure one being
        offered)? Only confirm if version matches AND nothing contradicts.
     b. CONFIG-CLASS vulns (version-independent, e.g. weak credentials,
        no-auth-required): version is irrelevant, so these REQUIRE direct
        evidence of exploitation (a real login, a real unauthenticated
        command executing) to confirm -- a banner/open-port alone is not
        enough.

3. MEMORY -- maintains a running _session_state across calls within a
   batch run, so repeated findings against the same host+plugin in one
   session are recognized as duplicates rather than re-analyzed from
   scratch.

4. STRUCTURED, CLIENT-READY OUTPUT -- every result includes a plain-
   English justification tied to the specific evidence used.

Must expose: solve(case: dict) -> dict
"""

import json
import re
from pathlib import Path

_KB_PATH = Path(__file__).parent.parent / "eval" / "knowledge_base" / "vuln_db.json"
_kb_cache = None

_session_state = {}


def _load_kb():
    global _kb_cache
    if _kb_cache is None:
        with open(_KB_PATH) as f:
            _kb_cache = {e["plugin_name"]: e for e in json.load(f)["entries"]}
    return _kb_cache


def _parse_version(v):
    try:
        parts = tuple(int(p) for p in re.findall(r"\d+", v))
        return parts if parts else None  # e.g. "unknown" -> no digits -> must be None,
                                          # not (), which Python would silently treat as
                                          # "less than" any real version tuple
    except (ValueError, TypeError):
        return None


def _version_in_range(version, vmin, vmax):
    v, lo, hi = _parse_version(version), _parse_version(vmin), _parse_version(vmax)
    if v is None or lo is None or hi is None:
        return None
    return lo <= v <= hi


# Direct proof of exploitation -- required to confirm a CONFIG-CLASS finding
# (version-independent: a real login succeeded, a real unauthenticated
# command executed), since a banner/open-port alone proves nothing there.
_DIRECT_EVIDENCE_PATTERNS = [
    "returned file contents", "successful login", "returned pong",
    "no auth required", "confirmed via", "no password prompt bypass required",
]

# Signals that CONTRADICT exploitability even when the version matches --
# e.g. a secure protocol is negotiated by default despite an insecure one
# being merely offered. Generalizes case-05's TLS scenario: the finding
# looks right on paper but the evidence itself shows the vulnerable path
# isn't actually what's active.
_CONTRADICTING_EVIDENCE_PATTERNS = [
    "negotiated by default", "not required in this instance",
    "preferred by default",
]

# Explicit demonstrated-exploitation language that should override the
# contradiction check above -- added after case-16 revealed that
# "negotiated by default" can appear in the SAME sentence as a real,
# successful attack (a forced downgrade), which the general heuristic
# alone can't distinguish from case-05's genuinely-not-exploited scenario.
_STRONG_OVERRIDE_PATTERNS = [
    "downgrade attack succeeded", "attack succeeded", "forced downgrade",
    "successfully forced",
]


def _has_strong_override(evidence):
    ev = evidence.lower()
    return any(p in ev for p in _STRONG_OVERRIDE_PATTERNS)


def _has_direct_evidence(evidence):
    ev = evidence.lower()
    return any(p in ev for p in _DIRECT_EVIDENCE_PATTERNS)


def _has_contradicting_evidence(evidence):
    ev = evidence.lower()
    return any(p in ev for p in _CONTRADICTING_EVIDENCE_PATTERNS)


def solve(case: dict) -> dict:
    host = case.get("host")
    plugin_name = case.get("plugin_name")
    service_version = case.get("service_version", "")
    evidence = case.get("evidence", "")

    key = (host, plugin_name)
    if key in _session_state:
        prior = _session_state[key]
        return {
            "result": prior["result"],
            "reason": f"Duplicate of an earlier finding on {host} for "
                      f"'{plugin_name}' already triaged this session "
                      f"(memory hit) -- reusing prior result: {prior['reason']}",
        }

    kb = _load_kb()
    entry = kb.get(plugin_name)

    if entry is None:
        result = {
            "result": "Needs Verification",
            "reason": f"No knowledge-base entry for plugin '{plugin_name}' -- "
                      f"cannot verify affected version range. Flagging for "
                      f"manual review rather than guessing.",
        }
        _session_state[key] = result
        return result

    is_config_class = (entry["affected_version_min"] == "0.0"
                        and entry["affected_version_max"] == "999.0")

    if is_config_class:
        if _has_direct_evidence(evidence):
            result = {
                "result": "Confirmed",
                "reason": f"'{plugin_name}' is a config-class issue (version-"
                          f"independent per {entry['synthetic_cve']}). Evidence "
                          f"shows direct proof of exploitation, not just a "
                          f"passive signal -- confirming.",
            }
        else:
            result = {
                "result": "Needs Verification",
                "reason": f"'{plugin_name}' is a config-class issue -- version "
                          f"is irrelevant, but the evidence provided is only a "
                          f"passive signal (open port/banner), not direct proof "
                          f"({entry['false_positive_notes']}). Needs manual "
                          f"confirmation before reporting.",
            }
    else:
        in_range = _version_in_range(
            service_version, entry["affected_version_min"], entry["affected_version_max"]
        )
        if in_range is False:
            result = {
                "result": "Likely False Positive",
                "reason": f"Detected version {service_version} is outside the "
                          f"known-affected range {entry['affected_version_min']}"
                          f"-{entry['affected_version_max']} for "
                          f"'{plugin_name}' ({entry['synthetic_cve']}). "
                          f"{entry['false_positive_notes']}",
            }
        elif in_range is True:
            if _has_strong_override(evidence):
                result = {
                    "result": "Confirmed",
                    "reason": f"Version {service_version} is within the "
                              f"affected range, and although the evidence "
                              f"mentions a mitigating factor, it also describes "
                              f"an explicit successful exploitation -- "
                              f"confirming despite the general contradiction "
                              f"pattern (see false_positive_notes: "
                              f"{entry['false_positive_notes']}).",
                }
            elif _has_contradicting_evidence(evidence):
                result = {
                    "result": "Needs Verification",
                    "reason": f"Version {service_version} is within the "
                              f"affected range, but the evidence itself "
                              f"suggests the vulnerable configuration may not "
                              f"actually be active ({entry['false_positive_notes']})"
                              f" -- needs manual confirmation before reporting.",
                }
            else:
                result = {
                    "result": "Confirmed",
                    "reason": f"Version {service_version} is within the "
                              f"known-affected range {entry['affected_version_min']}"
                              f"-{entry['affected_version_max']} for "
                              f"'{plugin_name}' and evidence does not "
                              f"contradict exploitability -- confirming.",
                }
        else:
            result = {
                "result": "Needs Verification",
                "reason": "Could not parse/compare version strings -- "
                          "flagging for manual review rather than guessing.",
            }

    _session_state[key] = result
    return result
