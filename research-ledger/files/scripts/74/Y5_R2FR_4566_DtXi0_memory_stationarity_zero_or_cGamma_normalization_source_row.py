from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4566"
CLAIM_ID = "L-408"
BRANCH_ID = "MTS_R2FR_Y5_DTXI0_STATIONARITY_OR_CGAMMA_NORM_4566"
MARKER = "PPC4161_DTXI0_MEMORY_STATIONARITY_ZERO_OR_CGAMMA_NORMALIZATION_SOURCE_ROW_4566"
PACKET_MARKER = "PPC4161_PACKET_DTXI0_STATIONARITY_OR_CGAMMA_NORM_4566"
DECISION = "DTXI0_CONDITIONAL_STATIONARY_BRANCH_ZERO_DERIVED_CGAMMA_NORMALIZATION_MISSING_STATIC_AMPLITUDES_RETAINED"
NEXT_TARGET = "4567-Y5-R2FR-cGamma-static-source-homogeneity-and-boundary-amplitude-zero-or-AJ-profile-row.md"

FORMAL_PATH = FORMAL / "582-PPC4161-DtXi0-memory-stationarity-zero-or-cGamma-normalization-source-row.md"
DOC_PATH = POST / "4566-Y5-R2FR-DtXi0-memory-stationarity-zero-or-cGamma-normalization-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4565 = FORMAL / "581-PPC4161-cGamma-memory-projector-parent-zero-or-first-profile-bound-row.md"
CSV_4565_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4565_NEXT_TARGET.csv"
POST_4545 = POST / "4545-Y5-R2FR-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"
CSV_4543_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4543_PRODUCT_TO_COEFFICIENT_THEOREM.csv"
CSV_4543_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4543_GDOT_CONVERSION_INPUT_LEDGER.csv"
CSV_4544_DTXI = SOURCE_DIR / "P8_Y5_R2FR_4544_DTXI_ZERO_THEOREM.csv"
CSV_4544_TENSOR = SOURCE_DIR / "P8_Y5_R2FR_4544_TENSOR_PERP_GDOT_SPLIT.csv"
CSV_4544_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4544_DTXI_TPERP_FINITE_BOUND.csv"
CSV_4545_MAP = SOURCE_DIR / "P8_Y5_R2FR_4545_ATTRACTOR_STATIONARITY_MAP.csv"
CSV_4545_BUDGET = SOURCE_DIR / "P8_Y5_R2FR_4545_GDOT_REDUCED_BUDGET.csv"
CSV_4545_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4566_SOURCE_REGISTER.csv"
STATIONARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_DTXI0_STATIONARITY_THEOREM.csv"
GDOT_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_GDOT_PRODUCT_BRANCH_VERDICT.csv"
NORMALIZATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_CGAMMA_NORMALIZATION_SOURCE_ROW.csv"
RETAINED_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_RETAINED_STATIC_AMPLITUDES.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4566_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4566_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4566_00_4565_formal", "4565 Gdot product row", DOC_4565, "C_Gamma_Gdot = c_Gamma D_t Xi_0"),
        ("SRC4566_01_4565_next", "4565 next target CSV", CSV_4565_NEXT, "4566-Y5-R2FR-DtXi0-memory-stationarity-zero-or-cGamma-normalization-source-row.md"),
        ("SRC4566_02_4543_theorem", "4543 Gdot theorem", CSV_4543_THEOREM, "THM4543_2_exact_silence_route"),
        ("SRC4566_03_4543_inputs", "4543 conversion inputs", CSV_4543_INPUT, "IN4543_5_zero_route"),
        ("SRC4566_04_4544_DtXi", "4544 D_t Xi zero theorem", CSV_4544_DTXI, "ZTH4544_3_time_derivative_zero"),
        ("SRC4566_05_4544_tensor", "4544 tensor split", CSV_4544_TENSOR, "TPS4544_2_trace_scalar"),
        ("SRC4566_06_4544_bound", "4544 finite Gdot budget", CSV_4544_BOUND, "FB4544_2_product_budget"),
        ("SRC4566_07_4545_doc", "4545 stationarity/boundary split", POST_4545, "HAMILTONIAN_STATIONARY_BRANCH_GIVES_DERIVATIVE_SILENCE_FULL_BOUNDARY_NOHAIR_REMAINS_OPEN"),
        ("SRC4566_08_4545_map", "4545 attractor stationarity map", CSV_4545_MAP, "PZ4545_3_attractor_stationarity"),
        ("SRC4566_09_4545_budget", "4545 Gdot reduced budget", CSV_4545_BUDGET, "GB4545_1_stationary_derivative_reduction"),
        ("SRC4566_10_4545_retained", "4545 retained residuals", CSV_4545_RETAINED, "RR4545_0_source_silence"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4566 D_t Xi_0 stationarity / cGamma normalization source row",
                "valid_for_claim": "False",
            }
        )
    return rows


def stationarity_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "DS4566_0_profile_definition",
            "statement": "Xi_0 := N_0[P_loc Gamma_mem]",
            "derivation": "imported scalar projection definition from 4544/4189",
            "requires": "smooth scalar projection and fixed local collar/readout map",
            "status": "DEFINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DS4566_1_green_problem",
            "statement": "L_Xi delta Xi = P_loc J_res with B_Xi delta Xi = b_Xi",
            "derivation": "memory scalar residual packaged as a local Green/uniqueness problem",
            "requires": "parent-owned L_Xi, boundary operator B_Xi and projection P_loc",
            "status": "CONTRACT_WRITTEN_PARENT_OPERATOR_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DS4566_2_stationary_branch_zero",
            "statement": "D_t Xi_0 = 0 in a stationary compact branch",
            "derivation": "if local invariants I_A and scalar boundary charges Q_B are stationary along tau, smooth chain rule gives D_t Xi_0=0",
            "requires": "L_tau I_A=0, L_tau Q_B=0, no incoming homogeneous/kernel mode, stationary boundary data",
            "status": "PASS_CONDITIONAL_STATIONARY_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DS4566_3_gdot_product_silence",
            "statement": "If D_t Xi_0=0 and T_perp,Gdot=0, then C_Gamma_Gdot=0",
            "derivation": "substitute into C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot",
            "requires": "stationarity plus tensor/perp scalar-boundary silence",
            "status": "CONDITIONAL_GDOT_SILENCE",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DS4566_4_global_limit",
            "statement": "D_t Xi_0=0 is not a global c_Gamma parent-zero theorem",
            "derivation": "Hamiltonian conservation controls derivative drift, not static source amplitude, spatial homogeneity or full boundary no-hair",
            "requires": "separate source/static/boundary amplitude closures",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def gdot_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "GV4566_0_product_identity",
            "object": "C_Gamma_Gdot",
            "result": "C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot",
            "status": "EXACT_CHANNEL_IDENTITY_RETAINED",
            "claim_effect": "Gdot row is a product/sum bound, not a c_Gamma bound",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "GV4566_1_derivative_silence",
            "object": "D_t Xi_0",
            "result": "D_t Xi_0=0 in the stationary compact local branch",
            "status": "CONDITIONAL_BRANCH_PASS",
            "claim_effect": "removes scalar time-profile drift only if branch premises are accepted",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "GV4566_2_tensor_perp",
            "object": "T_perp,Gdot",
            "result": "pure TT monopole is scalar-Gdot silent, but trace/scalar and boundary pieces remain",
            "status": "PARTIAL_TENSOR_SPLIT_RETAINED",
            "claim_effect": "Gdot silence still needs T_trace/T_boundary zero or bound",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "GV4566_3_coefficient",
            "object": "c_Gamma",
            "result": "not bounded or normalized by D_t Xi_0=0",
            "status": "NO_STANDALONE_COEFFICIENT_CLAIM",
            "claim_effect": "a zero profile can make any c_Gamma compatible with the Gdot product unless other arenas/profiles normalize it",
            "valid_for_claim": "False",
        },
    ]


def normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CN4566_0_cGamma",
            "quantity": "c_Gamma",
            "source_value": "MISSING_PARENT_NORMALIZATION",
            "units": "MISSING_PARENT_UNITS",
            "needed_for": "standalone coefficient bound or natural-size prior",
            "status": "NOT_SOURCED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "CN4566_1_JGdot",
            "quantity": "J_Gdot^Gamma",
            "source_value": "absorbed_into_D_t_Xi_0_in_unit_normalized_smoke",
            "units": "yr^-1 per Gamma-profile unit",
            "needed_for": "convert product bound into a physical profile/Jacobian bound",
            "status": "SYMBOLIC_ONLY",
            "valid_for_claim": "False",
        },
        {
            "row_id": "CN4566_2_Xmin",
            "quantity": "X_min <= |D_t Xi_0|",
            "source_value": "MISSING_NONZERO_PROFILE_FLOOR",
            "units": "yr^-1",
            "needed_for": "upper bound on |c_Gamma| from product inequality",
            "status": "NOT_SOURCED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "CN4566_3_Tmax",
            "quantity": "|T_perp,Gdot| <= T_max",
            "source_value": "MISSING_TRACE_BOUNDARY_TENSOR_BOUND",
            "units": "yr^-1",
            "needed_for": "coefficient-bound route |c_Gamma| <= (B_Gdot+T_max)/X_min",
            "status": "NOT_SOURCED",
            "valid_for_claim": "False",
        },
    ]


def retained_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RS4566_0_source_static",
            "object": "P_loc[U_B S_cg]",
            "why_retained": "stationarity can make derivative drift zero without proving the static source amplitude vanishes",
            "next_action": "derive compact support/source silence or finite A_J profile row",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RS4566_1_spatial_homogeneity",
            "object": "P_loc[D_m Delta_h m_L]",
            "why_retained": "D_t m_L=0 does not imply D_m m_L=0",
            "next_action": "derive attractor homogeneity or finite gradient/source profile row",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RS4566_2_boundary_amplitude",
            "object": "P_loc[boundary_in], T_boundary",
            "why_retained": "constant scalar monopole is derivative-silent but trace/shear/vector boundary amplitude is not zero",
            "next_action": "boundary no-hair or finite T_boundary bound",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RS4566_3_kernel_mode",
            "object": "D_t h_ker and incoming homogeneous modes",
            "why_retained": "Hamiltonian no-flux must also exclude incoming memory/kernel modes",
            "next_action": "topological no-influx theorem or numeric mode amplitude",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG4566_0_stationarity",
            "requirement": "derive D_t Xi_0=0",
            "status": "PASS_CONDITIONAL_STATIONARY_BRANCH",
            "claim_effect": "Gdot scalar time-profile can vanish in the stationary compact branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4566_1_tperp",
            "requirement": "prove T_perp,Gdot=0 or bound it",
            "status": "PARTIAL_TT_ZERO_TRACE_BOUNDARY_OPEN",
            "claim_effect": "full Gdot silence not globally promoted",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4566_2_cGamma_norm",
            "requirement": "source c_Gamma/J_Gdot normalization or nonzero profile floor",
            "status": "FAIL_NOT_SOURCED",
            "claim_effect": "no standalone c_Gamma bound",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4566_3_static_amplitudes",
            "requirement": "source/static/boundary amplitudes closed",
            "status": "FAIL_RETAINED_STATIC_AMPLITUDES",
            "claim_effect": "local-GR/Newton public claim remains blocked",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4566_4_next",
            "requirement": "next target attacks static source/boundary amplitudes",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": f"next target = {NEXT_TARGET}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4566_0_main",
            "decision": DECISION,
            "what_was_derived": "D_t Xi_0=0 is conditionally derived on the stationary compact branch; with T_perp,Gdot=0 this silences the Gdot product channel.",
            "what_failed": "The result is not global parent stationarity, does not normalize c_Gamma, and does not close static source/spatial/boundary amplitudes.",
            "action_taken": "Keep the Gdot product row as a conditional-zero/nonclaim row and send the next attack to static source homogeneity and boundary amplitude.",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "After derivative stationarity, the live cGamma pressure is no longer D_t Xi_0 in the stationary branch; it is static source support, spatial homogeneity, trace/boundary amplitude and any nonzero AJ/profile coefficient.",
            "success_condition": "Derive P_loc[U_B S_cg]=0, P_loc[D_m Delta_h m_L]=0 and T_boundary=0, or produce a finite A_J/profile row with units and no-cancellation guards.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "DtXi0_stationary_branch_zero": "True",
            "DtXi0_parent_global_zero": "False",
            "Tperp_Gdot_zero_global": "False",
            "cGamma_normalization_sourced": "False",
            "static_amplitudes_retained": "True",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "timestamp_utc": utc_now(),
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    stationarity: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    normalization: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append({"validation_id": "VAL4566_0_sources", "check": "all source paths and needles validate", "status": "PASS" if source_ok else "FAIL", "details": f"{len(sources)} sources"})

    st_text = "\n".join(str(value) for row in stationarity for value in row.values())
    st_ok = all(token in st_text for token in ["D_t Xi_0 = 0", "PASS_CONDITIONAL_STATIONARY_BRANCH", "C_Gamma_Gdot=0", "PUBLIC_CLAIM_BLOCKED"])
    st_ok = st_ok and all(row["valid_for_claim"] == "False" for row in stationarity)
    rows.append({"validation_id": "VAL4566_1_stationarity", "check": "stationarity theorem is conditional and nonclaim", "status": "PASS" if st_ok else "FAIL", "details": f"{len(stationarity)} theorem rows"})

    verdict_text = "\n".join(str(value) for row in verdict for value in row.values())
    verdict_ok = all(token in verdict_text for token in ["EXACT_CHANNEL_IDENTITY_RETAINED", "CONDITIONAL_BRANCH_PASS", "NO_STANDALONE_COEFFICIENT_CLAIM"])
    rows.append({"validation_id": "VAL4566_2_gdot_verdict", "check": "Gdot verdict separates product identity, derivative silence and no cGamma bound", "status": "PASS" if verdict_ok else "FAIL", "details": f"{len(verdict)} verdict rows"})

    norm_text = "\n".join(str(value) for row in normalization for value in row.values())
    norm_ok = all(token in norm_text for token in ["MISSING_PARENT_NORMALIZATION", "J_Gdot^Gamma", "MISSING_NONZERO_PROFILE_FLOOR", "MISSING_TRACE_BOUNDARY_TENSOR_BOUND"])
    rows.append({"validation_id": "VAL4566_3_normalization", "check": "normalization/source rows remain explicit missing inputs", "status": "PASS" if norm_ok else "FAIL", "details": f"{len(normalization)} normalization rows"})

    retained_text = "\n".join(str(value) for row in retained for value in row.values())
    retained_ok = all(token in retained_text for token in ["P_loc[U_B S_cg]", "P_loc[D_m Delta_h m_L]", "T_boundary", "D_t h_ker"])
    rows.append({"validation_id": "VAL4566_4_retained", "check": "static/source/boundary amplitudes remain retained", "status": "PASS" if retained_ok else "FAIL", "details": f"{len(retained)} retained rows"})

    gates_text = "\n".join(str(value) for row in gates for value in row.values())
    gates_ok = all(token in gates_text for token in ["PASS_CONDITIONAL_STATIONARY_BRANCH", "FAIL_NOT_SOURCED", "FAIL_RETAINED_STATIC_AMPLITUDES", "PASS_NEXT_SELECTED"])
    gates_ok = gates_ok and all(row["valid_for_claim"] == "False" for row in gates)
    rows.append({"validation_id": "VAL4566_5_gates", "check": "promotion gates keep conditional win but block public claim", "status": "PASS" if gates_ok else "FAIL", "details": f"{len(gates)} gates"})

    decision_ok = decision and decision[0]["decision"] == DECISION and decision[0]["valid_for_claim"] == "False"
    status_ok = status and status[0]["DtXi0_stationary_branch_zero"] == "True" and status[0]["DtXi0_parent_global_zero"] == "False" and status[0]["static_amplitudes_retained"] == "True"
    next_ok = next_target and next_target[0]["next_target"] == NEXT_TARGET
    rows.append({"validation_id": "VAL4566_6_decision_status", "check": "decision/status select static amplitude target", "status": "PASS" if decision_ok and status_ok and next_ok else "FAIL", "details": NEXT_TARGET})

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL4566_7_overall", "check": "overall 4566 checkpoint validation", "status": "PASS" if overall else "FAIL", "details": "DtXi0 conditional zero integrated; static amplitudes retained" if overall else "one or more validations failed"})
    return rows


def write_doc(
    path: Path,
    title: str,
    sources: list[dict[str, Any]],
    stationarity: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    normalization: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# {title}

Branch: `{BRANCH_ID}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4566 answers the immediate question from the first Gdot product row:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot.
```

On the stationary compact local branch:

```text
D_t Xi_0 = 0
```

is conditionally derived from stationary local invariants, Hamiltonian no-flux, scalar conserved boundary data and no incoming homogeneous/kernel mode.

Therefore:

```text
D_t Xi_0 = 0 and T_perp,Gdot = 0 => C_Gamma_Gdot = 0.
```

But this is not a public cGamma/local-GR win. It does not source `c_Gamma`, does not give a nonzero profile floor, and does not remove static source/spatial/boundary amplitudes.

## Source Register

{markdown_table(sources)}

## DtXi0 Stationarity Theorem

{markdown_table(stationarity)}

## Gdot Product Branch Verdict

{markdown_table(verdict)}

## cGamma Normalization Source Row

{markdown_table(normalization)}

## Retained Static Amplitudes

{markdown_table(retained)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decision)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4566 integrates the conditional D_t Xi_0=0 stationary-branch result for the c_Gamma Gdot product, while retaining c_Gamma normalization, tensor-perp, static source and boundary amplitude gaps.",
        "current_evidence": "Generated source register, DtXi stationarity theorem, Gdot branch verdict, normalization source row, retained amplitudes, promotion gates, status and validation CSVs.",
        "status": "DtXi0_conditional_stationary_zero_static_amplitudes_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using derivative stationarity as if it proved full c_Gamma zero, full boundary no-hair, or a standalone coefficient bound.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Conditional branch win only; static amplitudes and normalization remain open.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    stationarity = stationarity_rows()
    verdict = gdot_verdict_rows()
    normalization = normalization_rows()
    retained = retained_rows()
    gates = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()
    status = status_rows()
    validation = validate(sources, stationarity, verdict, normalization, retained, gates, decision, next_target, status)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(STATIONARITY_CSV, stationarity)
    write_csv(GDOT_VERDICT_CSV, verdict)
    write_csv(NORMALIZATION_CSV, normalization)
    write_csv(RETAINED_CSV, retained)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)
    write_csv(VALIDATION_PATH, validation)

    write_doc(FORMAL_PATH, "4566 - DtXi0 memory stationarity zero or cGamma normalization source row", sources, stationarity, verdict, normalization, retained, gates, decision, next_target, validation)
    write_doc(DOC_PATH, "4566 - Y5 R2FR DtXi0 Memory Stationarity Zero Or cGamma Normalization Source Row", sources, stationarity, verdict, normalization, retained, gates, decision, next_target, validation)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4566 DtXi0 Stationarity Or cGamma Normalization

Marker: `{MARKER}`  
The Gdot product channel now has a conditional derivative-silence result:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot,
D_t Xi_0 = 0 in the stationary compact branch.
```

If `T_perp,Gdot=0` too, then `C_Gamma_Gdot=0`. This is a real local derivative win, but not a public cGamma/local-GR theorem: `c_Gamma` is not normalized, trace/boundary tensor pieces remain, and static source/spatial/boundary amplitudes are still open. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4566 Packet Integration - DtXi0 Stationarity

Marker: `{PACKET_MARKER}`  
The packet may use `D_t Xi_0=0` only inside the stationary compact branch. The Gdot product channel is conditionally silent if `T_perp,Gdot=0`, but `c_Gamma` normalization, static source support, spatial homogeneity and boundary amplitude remain live. Next target: `{NEXT_TARGET}`.
""",
    )

    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Decision: {DECISION}")


if __name__ == "__main__":
    main()
