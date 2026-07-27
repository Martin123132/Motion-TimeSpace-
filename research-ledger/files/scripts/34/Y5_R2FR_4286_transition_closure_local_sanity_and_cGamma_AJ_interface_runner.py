from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4286"
CLAIM_ID = "L-127"
BRANCH = "MTS_R2FR_Y5_TRANSITION_CLOSURE_LOCAL_SANITY_AND_CGAMMA_AJ_INTERFACE_RUNNER_4286"
DECISION = "NOLEAK_CLOSURE_LOCAL_SANITY_PASSES_AS_CLOSURE_CGAMMA_AJ_INTERFACE_REMAINS_BLOCKED_PENDING_REAL_PROFILES_NONCLAIM"
MARKER = "PPC4161_TRANSITION_CLOSURE_LOCAL_SANITY_AND_CGAMMA_AJ_INTERFACE_RUNNER_4286"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_CLOSURE_LOCAL_SANITY_AND_CGAMMA_AJ_INTERFACE_RUNNER_4286"
NEXT_TARGET = "4287-Y5-R2FR-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md"

FORMAL_PATH = FORMAL / "302-PPC4161-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md"
DOC_PATH = POST / "4286-Y5-R2FR-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4286_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
NUMERIC_TOL = 1e-12
AJ_REQUIREMENT = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"

SOURCES = {
    "SRC4286_00_4285_lock_doc": (
        FORMAL / "301-PPC4161-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md",
        "P_metric_loc_abs_max = 0",
        "4285 locks the local transition branch as explicit no-leak closure.",
    ),
    "SRC4286_01_102_thresholds": (
        FORMAL / "102-transition-closure-observable-threshold-spec.md",
        "local_current_leak_norm <= 1e-12",
        "102 supplies local implementation sanity thresholds.",
    ),
    "SRC4286_02_4285_lock_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4285_EXPLICIT_CLOSURE_LOCK.csv",
        "LOCAL_NO_LEAK_LOCKED",
        "4285 generated the machine-readable no-leak lock row.",
    ),
    "SRC4286_03_4285_AJ_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4285_CGAMMA_AJ_OPEN_ROWS.csv",
        "OPEN_PROFILE_ROW",
        "4285 keeps cGamma AJ profiles open.",
    ),
    "SRC4286_04_4284_shell_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "So the transition shell cannot be treated as a direct local metric source.",
        "4284 explains why closure/no-leak is needed.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if f"{CLAIM_ID}," in text:
        return
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4286 runs the explicit transition-closure local sanity interface. The no-leak closure passes as an implementation/contract sanity check with P_metric_loc_abs_max=0, local_current_leak_norm=0, and S_PPN_residual_norm=0, but this remains closure evidence rather than parent-derived local GR. The same checkpoint refuses to credit this closure to cGamma/AJ: R_transport_to_local, R_Bgrad_to_local, T_res/tau_L and c_Gamma remain missing real profile/coefficient rows.",'
        f'"4286 source register, local no-leak sanity inputs/results, control rows, cGamma AJ interface rows, decision and firewall.",'
        f'private_transition_closure_sanity_passes_cGamma_AJ_blocked_nonclaim,'
        f'"Derive or source the cGamma AJ profiles/coefficients, or derive a parent coefficient theorem that makes them vanish without closure smuggling.",'
        f'"Treating closure sanity as parent derivation, applying transition no-leak credit to cGamma AJ, or using control rows as physical evidence."\n'
    )
    path.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def local_sanity_input_rows() -> List[Dict[str, str]]:
    raw = [
        ("LSI4286_0", "P_metric_loc_abs_max", "0.0", "exact closure target", "0"),
        ("LSI4286_1", "local_current_leak_norm", "0.0", "exact closure target", "0"),
        ("LSI4286_2", "S_PPN_residual_norm", "0.0", "exact closure target", "0"),
        ("LSI4286_3", "implementation_tolerance", f"{NUMERIC_TOL:.1e}", "numeric sanity only", f"{NUMERIC_TOL:.1e}"),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "closure_value": value,
            "meaning": meaning,
            "threshold": threshold,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, value, meaning, threshold in raw
    ]


def local_sanity_result_rows() -> List[Dict[str, str]]:
    raw = [
        ("LSR4286_0_exact_Pmetric", "P_metric_loc_abs_max", 0.0, 0.0, "CLOSURE_EXACT_PASS_NONCLAIM"),
        ("LSR4286_1_exact_leak", "local_current_leak_norm", 0.0, 0.0, "CLOSURE_EXACT_PASS_NONCLAIM"),
        ("LSR4286_2_exact_ppn", "S_PPN_residual_norm", 0.0, 0.0, "CLOSURE_EXACT_PASS_NONCLAIM"),
        ("LSR4286_3_numeric_pass", "implementation_control", 1e-15, NUMERIC_TOL, "CONTROL_PASS_NONCLAIM"),
        ("LSR4286_4_numeric_fail", "implementation_control", 1e-6, NUMERIC_TOL, "CONTROL_FAIL_NONCLAIM"),
    ]
    rows: List[Dict[str, str]] = []
    for result_id, quantity, value, threshold, verdict in raw:
        passed = value <= threshold
        if threshold == 0.0:
            passed = value == 0.0
        rows.append(
            {
                **common(),
                "result_id": result_id,
                "quantity": quantity,
                "value": f"{value:.12e}",
                "threshold": f"{threshold:.12e}",
                "passed": str(passed),
                "verdict": verdict,
                "claim_scope": "closure_sanity_only",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def cgamma_aj_interface_rows() -> List[Dict[str, str]]:
    raw = [
        ("AJI4286_0", "R_transport_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "BLOCKED"),
        ("AJI4286_1", "R_Bgrad_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "BLOCKED"),
        ("AJI4286_2", "T_res/tau_L", "MISSING_PARENT_NORMALIZATION", "needed for AJ conversion", "BLOCKED"),
        ("AJI4286_3", "c_Gamma", "MISSING_PARENT_COEFFICIENT", "needed for AJ conversion", "BLOCKED"),
        ("AJI4286_4", "closure_credit_to_AJ", "FORBIDDEN", "no-leak transition closure does not fill AJ profiles", "BLOCKED_BY_FIREWALL"),
    ]
    return [
        {
            **common(),
            "interface_id": interface_id,
            "quantity": quantity,
            "value": value,
            "requirement": requirement,
            "status": status,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interface_id, quantity, value, requirement, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4286_0",
            "selected_route": "CGAMMA_AJ_PROFILE_OR_PARENT_COEFFICIENT_NEXT",
            "meaning": "Transition closure local sanity passes as closure-only; cGamma AJ interface remains blocked and must be attacked directly.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4286_0", "Do not treat closure no-leak sanity as a parent derivation."),
        ("FW4286_1", "Do not transfer transition no-leak closure credit to cGamma AJ profiles."),
        ("FW4286_2", "Do not treat implementation control rows as physical evidence."),
        ("FW4286_3", "Do not hide missing T_res/tau_L or c_Gamma behind the closure lock."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4286_0",
            "status": "CLOSURE_SANITY_PASSES_CGAMMA_AJ_BLOCKED",
            "summary": "Transition closure is executable as a no-leak sanity condition, but the next real local-GR pressure is cGamma/AJ profiles and coefficients.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4286_0",
            "target_file": NEXT_TARGET,
            "task": "Try to derive or source cGamma AJ profiles/coefficient rows: R_transport_to_local, R_Bgrad_to_local, T_res/tau_L and c_Gamma.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 302 Transition Closure Local Sanity And cGamma AJ Interface Runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4286 runs the transition closure local sanity check.

Under the explicit closure lock:

```text
P_metric_loc_abs_max = 0,
local_current_leak_norm = 0,
S_PPN_residual_norm = 0.
```

This passes the local no-leak sanity interface, with implementation tolerance:

```text
<= {NUMERIC_TOL:.1e}.
```

But this is closure-only. It is not a parent derivation.

## cGamma AJ Interface

The same closure does **not** fill:

```text
R_transport_to_local,
R_Bgrad_to_local,
T_res/tau_L,
c_Gamma.
```

The AJ branch remains blocked until those rows are derived or sourced. The closure lock cannot be used as credit for them.

## Next Physics Target

The next real pressure point is:

```text
cGamma AJ real profile or parent coefficient derivation.
```

No public local-GR claim is made.
"""


def checkpoint_doc() -> str:
    return f"""
# 4286 - transition closure local sanity and cGamma AJ interface runner

Marker: `{MARKER}`

Decision: `{DECISION}`

The local no-leak sanity rows pass as closure-only:

```text
P_metric_loc_abs_max = 0,
local_current_leak_norm = 0,
S_PPN_residual_norm = 0.
```

The `cGamma` AJ interface remains blocked pending real profiles or parent coefficients.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    inputs = csv_rows(paths["inputs"])
    results = csv_rows(paths["results"])
    aj = csv_rows(paths["aj"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + inputs
        + results
        + aj
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4286_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4286_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4286_2_inputs",
            {"P_metric_loc_abs_max", "local_current_leak_norm", "S_PPN_residual_norm"}.issubset({row["quantity"] for row in inputs}),
            "local sanity inputs emitted",
        ),
        (
            "VAL4286_3_exact_passes",
            all(row["passed"] == "True" for row in results if row["verdict"] == "CLOSURE_EXACT_PASS_NONCLAIM"),
            "exact closure rows pass",
        ),
        (
            "VAL4286_4_controls",
            any(row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in results)
            and any(row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in results),
            "control pass/fail rows emitted",
        ),
        (
            "VAL4286_5_AJ_blocked",
            {"R_transport_to_local", "R_Bgrad_to_local", "T_res/tau_L", "c_Gamma", "closure_credit_to_AJ"}.issubset({row["quantity"] for row in aj})
            and all(row["score_ready"] == "False" for row in aj),
            "AJ interface remains blocked",
        ),
        ("VAL4286_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4286_7_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4286_8_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4286_9_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4286_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4286_SOURCE_REGISTER.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4286_LOCAL_SANITY_INPUTS.csv",
        "results": SOURCE_DIR / "P8_Y5_R2FR_4286_LOCAL_SANITY_RESULTS.csv",
        "aj": SOURCE_DIR / "P8_Y5_R2FR_4286_CGAMMA_AJ_INTERFACE_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4286_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4286_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4286_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4286_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["inputs"], local_sanity_input_rows())
    write_csv(paths["results"], local_sanity_result_rows())
    write_csv(paths["aj"], cgamma_aj_interface_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4286 closure sanity and cGamma AJ interface",
        "4286 runs the transition closure local no-leak sanity interface and keeps it explicitly closure-only. It also blocks any attempt to use that closure to fill cGamma AJ profiles; R_transport, R_Bgrad, T_res/tau_L and c_Gamma remain the next direct target.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4286 packet local sanity runner",
        "Packet update: transition no-leak sanity passes as closure-only. The cGamma AJ interface is still blocked pending real profile/coefficient derivation.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
