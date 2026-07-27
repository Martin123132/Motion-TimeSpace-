from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4190"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_MEMORY_STATIONARITY_GRADIENT_GATE_4190"
DECISION = (
    "LOCAL_MEMORY_STATIONARITY_CONTRACT_WRITTEN_DTXI_GRADXI_BOUNDS_COMPUTED_"
    "PARENT_FIXED_POINT_PROOF_STILL_OPEN_NONCLAIM"
)
DOC_PATH = POST / "4190-Y5-R2FR-local-memory-stationarity-gradient-zero-lemma-or-dtXi-bound.md"
FORMAL_206_PATH = FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-031"
SPINE_MARKER = "PPC4161_LOCAL_MEMORY_STATIONARITY_GRADIENT_ZERO_GATE_4190"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_MEMORY_STATIONARITY_GRADIENT_ZERO_GATE_4190"
NEXT_TARGET = "4191-Y5-R2FR-memory-fixed-point-equation-and-smooth-minimizer-contract.md"

SOURCES = {
    "SRC4190_00_4189_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4189_NEXT_TARGET.csv",
        "D_t Xi_0=0 and grad_perp Xi_0=0",
        "4189 handoff.",
    ),
    "SRC4190_01_4189_fill": (
        SOURCE_DIR / "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL.csv",
        "c_Gamma D_t Xi_0",
        "4189 first coefficient formulas.",
    ),
    "SRC4190_02_formal_205": (
        FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md",
        "C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|",
        "formal projection split.",
    ),
    "SRC4190_03_scalar_stationarity": (
        FORMAL / "129-scalar-channel-stationarity.md",
        "scalar_channel_stationarity_not_parent_derived_zLcg_pruned_repair_required",
        "older scalar stationarity gate.",
    ),
    "SRC4190_04_equation_register": (
        FORMAL / "05-equation-register.md",
        "grad m -> 0",
        "local memory equilibrium/screening register.",
    ),
    "SRC4190_05_product_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv",
        "C_Gamma_metric",
        "4188 product bounds.",
    ),
    "SRC4190_06_spine": (
        FORMAL / "07-unification-spine.md",
        "local_vacuum_plateau_rejected_as_current_derivation",
        "spine history of stationarity/plateau failure.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def strict_bound(product: str) -> Dict[str, str]:
    for row in parse_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv"):
        if row["effective_product"] == product:
            return row
    raise KeyError(product)


def stationarity_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "STC4190_0_memory_projection",
            "Xi_0 := N_0[P_loc Gamma_mem] is the scalar memory projection feeding Gdot/xi channels.",
            "definition",
            "filled",
        ),
        (
            "STC4190_1_fixed_point",
            "Local compact matter reaches a parent-owned memory fixed point: E_Xi[Xi_0; local invariants]=0.",
            "needed to avoid assuming stationarity",
            "unsigned",
        ),
        (
            "STC4190_2_smooth_minimizer",
            "The fixed point is a smooth unique minimizer, so no linear |z| or cusp term survives.",
            "kills the old scalar-channel cusp obstruction",
            "unsigned",
        ),
        (
            "STC4190_3_stationary_sources",
            "Local source/readout invariants are stationary along the compact local time flow tau.",
            "gives D_t Xi_0=0 by chain rule if fixed point is smooth",
            "conditional",
        ),
        (
            "STC4190_4_homogeneous_projection",
            "P_loc removes or suppresses transverse scalar gradients in tested local collars.",
            "gives grad_perp Xi_0=0 or activates xi bound",
            "conditional",
        ),
        (
            "STC4190_5_no_Lcg_dial",
            "No free z_Lcg or sector-tuned L_cg reference appears in the scalar source map.",
            "prevents hidden local tuning",
            "pruned_not_derived",
        ),
        (
            "STC4190_6_theorem_gate",
            "Only STC4190_1 through STC4190_5 together allow the exact zero lemma.",
            "keeps closure assumptions out of claims",
            "active_gate",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "statement": statement,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, statement, role, status in rows
    ]


def lemma_attempt_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "LEM4190_0_exact_stationarity",
            "If Xi_0 is a smooth unique fixed point of stationary local invariants, then D_t Xi_0=0.",
            "mathematically valid conditional",
            "parent fixed-point equation missing",
        ),
        (
            "LEM4190_1_exact_homogeneity",
            "If the local projector kills transverse source gradients or local invariants are homogeneous, then grad_perp Xi_0=0.",
            "mathematically valid conditional",
            "projector/source-gradient theorem missing",
        ),
        (
            "LEM4190_2_cusp_warning",
            "Even local stationarity fails if source maps contain linear |z| cusp terms.",
            "known obstruction",
            "old 129 gate pruned z_Lcg but did not derive smoothness",
        ),
        (
            "LEM4190_3_result",
            "Current corpus does not close the exact lemma, but it gives the correct finite bound rows.",
            "nonclaim progress",
            "move to fixed-point/minimizer derivation or numeric profile fill",
        ),
    ]
    return [
        {
            **common(),
            "lemma_id": lemma_id,
            "statement": statement,
            "math_status": math_status,
            "current_blocker": blocker,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for lemma_id, statement, math_status, blocker in rows
    ]


def profile_bound_rows() -> List[Dict[str, str]]:
    gdot_bound = float(strict_bound("C_Gamma_Gdot")["max_abs_effective_product"])
    xi_bound = float(strict_bound("C_Gamma_metric")["max_abs_effective_product"])
    c_gamma_values = [1.0, 1e-3, 1e-6, 1e-9, 1e-12]
    rows: List[Dict[str, str]] = []
    for c_abs in c_gamma_values:
        rows.append(
            {
                **common(),
                "bound_id": f"DTXI4190_cGamma_{c_abs:.0e}",
                "channel": "D_t Xi_0",
                "assumed_abs_cGamma": f"{c_abs:.17g}",
                "required_abs_profile_bound": f"{gdot_bound / c_abs:.17g}",
                "units": "yr^-1",
                "derived_from": "C_Gamma_Gdot <= 2.42e-14 yr^-1",
                "interpretation": "|D_t Xi_0| must be below this value if c_Gamma has the assumed magnitude.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(
            {
                **common(),
                "bound_id": f"GRADXI4190_cGamma_{c_abs:.0e}",
                "channel": "L_loc grad_perp Xi_0",
                "assumed_abs_cGamma": f"{c_abs:.17g}",
                "required_abs_profile_bound": f"{xi_bound / c_abs:.17g}",
                "units": "dimensionless",
                "derived_from": "C_Gamma_xi <= 4e-9",
                "interpretation": "|L_loc grad_perp Xi_0| must be below this value if c_Gamma has the assumed magnitude.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            **common(),
            "bound_id": "SYMBOLIC4190_DTXI",
            "channel": "D_t Xi_0",
            "assumed_abs_cGamma": "|c_Gamma|",
            "required_abs_profile_bound": "2.42e-14 / |c_Gamma|",
            "units": "yr^-1",
            "derived_from": "C_Gamma_Gdot product bound",
            "interpretation": "symbolic exact profile bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            **common(),
            "bound_id": "SYMBOLIC4190_GRADXI",
            "channel": "L_loc grad_perp Xi_0",
            "assumed_abs_cGamma": "|c_Gamma|",
            "required_abs_profile_bound": "4e-9 / |c_Gamma|",
            "units": "dimensionless",
            "derived_from": "C_Gamma_xi product bound",
            "interpretation": "symbolic exact profile bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4190_0",
            "decision": DECISION,
            "exact_zero_lemma_closed": "False",
            "finite_profile_bounds_ready": "True",
            "best_next_route": "derive parent fixed-point equation and smooth minimizer for Xi_0",
            "fallback_route": "fill D_t Xi_0 and L_loc grad_perp Xi_0 profile values and compare against 4190 rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4190_0_no_stationarity_assumption", "D_t Xi_0=0 and grad_perp Xi_0=0 are theorem targets, not assumptions."),
        ("FW4190_1_no_Lcg_dial", "No z_Lcg or free L_cg reference may be used to tune local stationarity."),
        ("FW4190_2_product_bounds_only", "Profile bounds are conditional on assumed |c_Gamma| and are not direct c_Gamma measurements."),
        ("FW4190_3_no_public_claim", "No local-GR, PPN, clock, orbital or R10 pass follows from this gate."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "enforced": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "stationarity_contract_written": "True",
            "exact_zero_lemma_closed": "False",
            "dtXi_bound_rows": str(len([r for r in profile_bound_rows() if r["channel"] == "D_t Xi_0"])),
            "gradXi_bound_rows": str(len([r for r in profile_bound_rows() if r["channel"] == "L_loc grad_perp Xi_0"])),
            "finite_profile_bounds_ready": "True",
            "numeric_profile_value_available": "False",
            "public_local_GR_claim_allowed": "False",
            "formal_206_written": str(FORMAL_206_PATH.exists()),
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4190 writes the stationarity theorem contract and finite D_t Xi_0 / grad Xi_0 bounds, but exact zero still needs a parent fixed-point/minimizer proof.",
            "route_A": "derive E_Xi[Xi_0; local invariants]=0 with smooth unique minimizer and stationary local inputs",
            "route_B": "fill numeric or symbolic D_t Xi_0 and grad_perp Xi_0 profile values and score them against 4190 bounds",
            "recommended_first": "fixed-point equation and smooth-minimizer contract",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc_text() -> str:
    return f"""# 206 - PPC4161 Local Memory Stationarity Gradient Zero Gate

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR and does not assume local stationarity. It writes the exact stationarity/homogeneity contract and computes the finite profile bounds required if stationarity fails.

## Stationarity Contract

Let:

```text
Xi_0 := N_0[P_loc Gamma_mem].
```

The exact local scalar-memory silence route requires:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

This follows only if the parent supplies a smooth local fixed point:

```text
E_Xi[Xi_0; local invariants] = 0
```

with stationary local inputs, no cusp-linear `|z|` terms, no free `z_Lcg` dial, and no unsuppressed transverse source-gradient projection.

## Finite Bounds

If exact stationarity is not proved, then:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma|  yr^-1
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|.
```

For `|c_Gamma|=1`, this means:

```text
|D_t Xi_0| <= 2.42e-14 yr^-1
|L_loc grad_perp Xi_0| <= 4e-9.
```

## Verdict

The zero lemma is not closed. The useful advance is that the next derivation now has an exact target: either derive the fixed-point/minimizer theorem or fill profile values for `D_t Xi_0` and `grad_perp Xi_0`.

## Next Gate

`{NEXT_TARGET}` should attack the parent fixed-point equation and smooth-minimizer contract.
"""


def checkpoint_doc_text() -> str:
    return f"""# 4190 - Local Memory Stationarity Gradient Zero Lemma Or dtXi Bound

Generated by: `post-checkpoint-work/scripts/Y5_R2FR_4190_local_memory_stationarity_gradient_zero_or_dtXi_bound.py`

## Summary

4190 uses the older scalar-channel stationarity gate and the new 4189 projection split to write the exact zero/bound condition for the scalar memory projection `Xi_0`.

## Result

Exact zero remains unproved, but the fallback is now executable:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|
```

## Decision

`{DECISION}`
"""


def ensure_docs() -> None:
    FORMAL_206_PATH.write_text(formal_doc_text(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc_text(), encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The local scalar-memory stationarity contract is written and finite D_t Xi_0 / gradient profile bounds are computed as functions of |c_Gamma|.",
            "current_evidence": "4190 stationarity contract, lemma attempt, cGamma-normalized profile bound runner, decision ledger and nonclaim firewall.",
            "status": "private_stationarity_contract_nonclaim_exact_zero_open_profile_bounds_ready",
            "next_test": "Derive the parent fixed-point equation with smooth minimizer or fill D_t Xi_0 and grad_perp Xi_0 profiles.",
            "key_risk": "Assuming local stationarity or choosing L_cg by hand would smuggle the closure the gate is meant to test.",
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "appended"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4190 Local Memory Stationarity Gradient Zero Gate

Marker: `{PACKET_MARKER}`

4190 writes the exact scalar memory stationarity target:

```text
D_t Xi_0 = 0,
grad_perp Xi_0 = 0.
```

If this cannot be proved, finite profile bounds apply:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1,
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|.
```
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "appended"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Local Memory Stationarity Gradient Zero Gate

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4190 turns the 4189 scalar projection target into a theorem/bound fork:

```text
D_t Xi_0 = 0 and grad_perp Xi_0 = 0
```

must be derived from a parent fixed-point/minimizer equation, not assumed. If it is not derived, the finite profile bounds are:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1
|L_loc grad_perp Xi_0| <= 4e-9 / |c_Gamma|.
```
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "appended"


def validation_rows(rows_by_name: Dict[str, List[Dict[str, str]]], claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    source_register = rows_by_name["P8_Y5_R2FR_4190_SOURCE_REGISTER"]
    status = rows_by_name["P8_Y5_R2FR_4190_STATUS"][0]
    profile_rows = rows_by_name["P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS"]
    all_generated_rows = [
        row
        for name, rows in rows_by_name.items()
        if name != "P8_Y5_R2FR_4190_SOURCE_REGISTER"
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4190_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source_register), str(source_register)),
        ("VAL4190_1_source_tokens", "all source tokens found", all(row["required_text_found"] == "True" for row in source_register), str(source_register)),
        ("VAL4190_2_contract", "stationarity contract written", status["stationarity_contract_written"] == "True", str(status)),
        ("VAL4190_3_zero_open", "exact zero lemma remains open", status["exact_zero_lemma_closed"] == "False", str(status)),
        ("VAL4190_4_profile_bounds", "finite profile bounds exist", len(profile_rows) >= 12 and status["finite_profile_bounds_ready"] == "True", str(len(profile_rows))),
        ("VAL4190_5_symbolic_bounds", "symbolic cGamma-normalized rows exist", any(row["bound_id"] == "SYMBOLIC4190_DTXI" for row in profile_rows) and any(row["bound_id"] == "SYMBOLIC4190_GRADXI" for row in profile_rows), "symbolic rows present"),
        ("VAL4190_6_no_public_claim", "public local GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4190_7_formal_206", "formal 206 exists with marker", FORMAL_206_PATH.exists() and SPINE_MARKER in read_text(FORMAL_206_PATH), str(FORMAL_206_PATH)),
        ("VAL4190_8_checkpoint_doc", "checkpoint doc exists with decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4190_9_claim_row", "claim register contains L-031", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4190_10_packet_180", "packet marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4190_11_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4190_12_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
    ]
    validation = [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(passed),
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed, detail in checks
    ]
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4190_13_py_compile",
            "check": "script compiles and __pycache__ removed",
            "passed": str(not pycache.exists()),
            "detail": str(SCRIPT_PATH),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    ensure_docs()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4190_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4190_STATIONARITY_CONTRACT": stationarity_contract_rows(),
        "P8_Y5_R2FR_4190_LEMMA_ATTEMPT": lemma_attempt_rows(),
        "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS": profile_bound_rows(),
        "P8_Y5_R2FR_4190_DECISION": decision_rows(),
        "P8_Y5_R2FR_4190_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4190_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4190_NEXT_TARGET": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(SOURCE_DIR / f"{name}.csv", rows)

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4190_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4190 validation failed: {failed}")

    print(DECISION)
    print(f"formal={FORMAL_206_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
