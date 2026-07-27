from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3018"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GAMMA_BOUND_ABS = 2.3e-5
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3018-Y5-R2FR-gamma-coefficient-fill-AST-or-beta-square-law-branch-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3018_00_3017_doc": ROOT / "3017-Y5-R2FR-source-current-Ward-owner-for-alpha3-or-gamma-coefficient-fill-under-AX1090.md",
    "SRC3018_01_3017_gamma_contract": RESIDUALS / "P8_Y5_R2FR_3017_GAMMA_COEFFICIENT_FILL_CONTRACT.csv",
    "SRC3018_02_3017_next": RESIDUALS / "P8_Y5_R2FR_3017_NEXT_TARGET.csv",
    "SRC3018_03_3016_doc": ROOT / "3016-Y5-R2FR-gamma-and-alpha3-PPN-kernel-first-derivation-under-AX1090.md",
    "SRC3018_04_3016_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "SRC3018_05_2489_doc": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
    "SRC3018_06_2489_kernel_csv": LOCAL_BOUNDS / "First_common_frame_PPN_response_kernel_2489_NONCLAIM.csv",
    "SRC3018_07_2919_doc": ROOT / "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md",
    "SRC3018_08_2919_beta_fallback": RESIDUALS / "P8_Y5_R2FR_2919_BETA_SOURCE_NORMALIZATION_FALLBACK_KERNEL.csv",
    "SRC3018_09_2893_beta_law": RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv",
    "SRC3018_10_2893_beta_vector": RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv",
    "SRC3018_11_2896_beta_components": RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_COMPONENTS.csv",
    "SRC3018_12_2896_newton_gate": RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv",
    "SRC3018_13_3015_ppn_comparators": RESIDUALS / "P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3018_SOURCE_REGISTER.csv",
    "gamma_attempt": RESIDUALS / "P8_Y5_R2FR_3018_GAMMA_COEFFICIENT_FILL_ATTEMPT.csv",
    "gamma_bound": RESIDUALS / "P8_Y5_R2FR_3018_GAMMA_BOUND_INTERFACE.csv",
    "beta_handoff": RESIDUALS / "P8_Y5_R2FR_3018_BETA_SQUARE_LAW_HANDOFF.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3018_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3018_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3018_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3018_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3018_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gamma_attempt_copy": LOCAL_BOUNDS / "gamma_coefficient_fill_attempt_3018_NONCLAIM.csv",
    "gamma_bound_copy": LOCAL_BOUNDS / "gamma_bound_interface_3018_NONCLAIM.csv",
    "beta_handoff_copy": LOCAL_BOUNDS / "beta_square_law_handoff_3018_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3018_BETA_SQUARE_LAW_SOURCE_NORMALIZATION_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3018_00_3017_doc": "3017 handoff: gamma coefficient fill or beta square-law branch",
    "SRC3018_01_3017_gamma_contract": "A_T/A_S/s_R/readout-gauge fill contract",
    "SRC3018_02_3017_next": "selected 3018 target and guardrails",
    "SRC3018_03_3016_doc": "gamma ratio kernel and alpha3 Ward warning",
    "SRC3018_04_3016_gamma_kernel": "gamma_eff=A_S/A_T source kernel",
    "SRC3018_05_2489_doc": "common-frame gamma and C_R delta_p combination law",
    "SRC3018_06_2489_kernel_csv": "first common-frame PPN response rows",
    "SRC3018_07_2919_doc": "stationary alpha3 attempt and beta fallback",
    "SRC3018_08_2919_beta_fallback": "beta_eff=B_source/A_source^2 handoff rows",
    "SRC3018_09_2893_beta_law": "source-normalized beta square-law derivation",
    "SRC3018_10_2893_beta_vector": "finite beta vector row retained nonclaim",
    "SRC3018_11_2896_beta_components": "beta residual envelope components",
    "SRC3018_12_2896_newton_gate": "source-normalized Newton precondition gate",
    "SRC3018_13_3015_ppn_comparators": "PPN comparator bounds including Cassini gamma and Will beta",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

gamma_attempt = [
    base(
        {
            "slot_id": "GAF3018_0_A_T",
            "quantity": "A_T",
            "derived_relation": "g00=-1+2 A_T U/c^2+O(c^-4) after fixed-GM comparison",
            "source_evidence": "3016 GAM3016_0; 3017 GCF3017_0",
            "current_status": "FORMULA_READY_VALUE_UNFILLED",
            "coefficient_value": "MISSING_A_T_PARENT_SOURCE_NORMALIZATION",
            "missing_for_claim": "MISSING_PARENT_FIELD_EQUATION_NORMAL_FORM; MISSING_FIXED_BEFORE_READOUT_SOURCE_CONVENTION",
            "claim_use": "cannot score gamma; common GM scaling alone is not a proof",
            "next_action": "derive A_T from parent weak-field source equation or prove it equals the shared Newtonian normalization",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_1_A_S",
            "quantity": "A_S",
            "derived_relation": "gij=(1+2 A_S U/c^2) delta_ij+O(c^-4) in the same observed PPN gauge",
            "source_evidence": "3016 GAM3016_0; 3017 GCF3017_1",
            "current_status": "FORMULA_READY_VALUE_UNFILLED",
            "coefficient_value": "MISSING_A_S_SPATIAL_METRIC_RESPONSE",
            "missing_for_claim": "MISSING_PARENT_SPATIAL_RESPONSE; MISSING_NO_SHADOW_OR_NO_DISFORMAL_METRIC_SLOT",
            "claim_use": "cannot score gamma without same-gauge A_S",
            "next_action": "derive spatial response from parent normal form or carry explicit epsilon_S residual",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_2_gamma_ratio",
            "quantity": "gamma_eff",
            "derived_relation": "gamma_eff=A_S/A_T; gamma_minus_1=(A_S-A_T)/A_T",
            "source_evidence": "3016 GAM3016_0; fixed-GM ratio guard",
            "current_status": "DERIVED_ALGEBRAIC_KERNEL_VALUES_MISSING",
            "coefficient_value": "MISSING_A_T_AND_A_S",
            "missing_for_claim": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_DIFFERENCE; MISSING_READOUT_GAUGE",
            "claim_use": "formula only; no prediction row",
            "next_action": "fill A_S-A_T in source-normalized gauge or prove relative difference zero",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_3_conformal_s_R",
            "quantity": "s_R",
            "derived_relation": "A_T=1-s_R; A_S=1+s_R; gamma_minus_1=2s_R/(1-s_R)",
            "source_evidence": "2489 PPNK2489_0; 3016 conformal specialization; 3017 GCF3017_2",
            "current_status": "CONDITIONAL_KERNEL_READY_VALUE_MISSING",
            "coefficient_value": "MISSING_b_R_x_U_OR_DELTA_P_PROFILE",
            "missing_for_claim": "MISSING_b_R_VALUE; MISSING_x_U_PROFILE_OR_DELTA_P; MISSING_BETA_CHANNEL; MISSING_NO_OTHER_PPN_CHANNELS",
            "claim_use": "conditional gamma interface only",
            "next_action": "derive s_R=0, source a finite s_R row, or demote to beta/source-normalization branch",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_4_CR_combo",
            "quantity": "delta_p and b_R",
            "derived_relation": "for C_R=ln(T^2S), gamma_obs_minus_1=(delta_p+4 b_R delta_p)/(1-2 b_R delta_p)",
            "source_evidence": "2489 PPNK2489_1",
            "current_status": "DERIVED_SYMBOLIC_COMBO_NONCLAIM",
            "coefficient_value": "MISSING_delta_p_ZERO_OR_VALUE; MISSING_b_R_VALUE",
            "missing_for_claim": "MISSING_NO_CANCELLATION_THEOREM; MISSING_FULL_VECTOR_CLOSURE",
            "claim_use": "Cassini constrains the combined residual, not b_R alone",
            "next_action": "try reciprocal-lock delta_p zero proof or retain combo as explicit gamma blocker",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_5_readout_gauge",
            "quantity": "PPN readout gauge",
            "derived_relation": "map from parent observed coframe and measured-GM convention to extracted PPN U/gamma",
            "source_evidence": "2489 PPNV2489_6; 3017 GCF3017_3",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "coefficient_value": "MISSING_alpha_readout_or_delta_GM",
            "missing_for_claim": "MISSING_FIXED_BEFORE_READOUT_THEOREM; MISSING_MEASURED_GM_TRANSFER_MAP",
            "claim_use": "prevents accidental gamma closure by readout choice",
            "next_action": "write source-normalized gauge map or keep gamma nonclaim",
        }
    ),
    base(
        {
            "slot_id": "GAF3018_6_verdict",
            "quantity": "gamma prediction row",
            "derived_relation": "a scoreable row requires A_T, A_S, readout gauge, and no hidden beta/preferred-frame tail",
            "source_evidence": "3017 next target; 2489 gamma-only-pass-forbidden decision",
            "current_status": "BLOCKED_NONCLAIM",
            "coefficient_value": "NO_SOURCE_BACKED_NUMERIC_GAMMA_ROW",
            "missing_for_claim": "MISSING_A_T; MISSING_A_S; MISSING_READOUT_GAUGE; MISSING_FULL_VECTOR_GUARD",
            "claim_use": "no Cassini/local-GR/PPN claim",
            "next_action": "route to beta square-law source-normalization gate rather than circling gamma again",
        }
    ),
]

negative_s_limit = -GAMMA_BOUND_ABS / (2.0 - GAMMA_BOUND_ABS)
positive_s_limit = GAMMA_BOUND_ABS / (2.0 + GAMMA_BOUND_ABS)

gamma_bound = [
    base(
        {
            "bound_id": "GBI3018_0_general_ratio",
            "component": "gamma_minus_1",
            "formula": "abs((A_S-A_T)/A_T) <= 2.3e-05",
            "comparator_bound_abs": GAMMA_BOUND_ABS,
            "derived_requirement": "A_T and A_S must be in the same fixed-before-readout PPN gauge with A_T nonzero",
            "validity_scope": "general weak-field metric coefficient interface",
            "status": "FORMULA_READY_VALUES_MISSING",
            "missing_for_claim": "MISSING_A_T; MISSING_A_S; MISSING_READOUT_GAUGE",
        }
    ),
    base(
        {
            "bound_id": "GBI3018_1_epsilon_difference",
            "component": "epsilon_S_minus_epsilon_T",
            "formula": "A_T=1+epsilon_T, A_S=1+epsilon_S => abs((epsilon_S-epsilon_T)/(1+epsilon_T)) <= 2.3e-05",
            "comparator_bound_abs": GAMMA_BOUND_ABS,
            "derived_requirement": "relative time/spatial coefficient mismatch must be tiny; measured GM cannot absorb it",
            "validity_scope": "small residual envelope with no cancellation shortcut",
            "status": "BOUND_INTERFACE_READY_VALUES_MISSING",
            "missing_for_claim": "MISSING_EPSILON_T; MISSING_EPSILON_S",
        }
    ),
    base(
        {
            "bound_id": "GBI3018_2_conformal_s_R",
            "component": "s_R",
            "formula": "abs(2s_R/(1-s_R)) <= 2.3e-05",
            "comparator_bound_abs": GAMMA_BOUND_ABS,
            "derived_requirement": f"for the regular branch, {negative_s_limit:.14e} <= s_R <= {positive_s_limit:.14e}; 2489 conservative shorthand is abs(s_R)<=1.14998677515209e-05",
            "validity_scope": "conformal special case only; not full PPN",
            "status": "CONDITIONAL_BOUND_INTERFACE_VALUES_MISSING",
            "missing_for_claim": "MISSING_s_R_VALUE_OR_ZERO_THEOREM; MISSING_BETA_AND_PREFERRED_FRAME_GUARDS",
        }
    ),
    base(
        {
            "bound_id": "GBI3018_3_CR_combo",
            "component": "delta_p_times_b_R",
            "formula": "abs(delta_p*(1+4b_R)/(1-2b_R*delta_p)) <= 2.3e-05",
            "comparator_bound_abs": GAMMA_BOUND_ABS,
            "derived_requirement": "Cassini bounds the delta_p/b_R combination, not b_R alone",
            "validity_scope": "C_R=ln(T^2S) route from 2489",
            "status": "SYMBOLIC_BOUND_INTERFACE_VALUES_MISSING",
            "missing_for_claim": "MISSING_delta_p_VALUE; MISSING_b_R_VALUE; MISSING_NO_CANCELLATION_THEOREM",
        }
    ),
    base(
        {
            "bound_id": "GBI3018_4_no_gamma_only_pass",
            "component": "full_PPN_vector_guard",
            "formula": "gamma bound satisfaction is necessary but not sufficient for local GR",
            "comparator_bound_abs": "not_applicable",
            "derived_requirement": "beta, alpha1, alpha2, alpha3, xi, source, endpoint and readout tails remain componentwise",
            "validity_scope": "project discipline guard",
            "status": "GUARD_ACTIVE",
            "missing_for_claim": "MISSING_FULL_PPN_VECTOR; MISSING_ALPHA3_ZERO_OR_BOUND; MISSING_BETA_SQUARE_LAW",
        }
    ),
]

beta_handoff = [
    base(
        {
            "beta_id": "BSH3018_0_beta_eff",
            "quantity": "beta_eff",
            "relation": "beta_eff = B_source/A_source^2",
            "source_evidence": "2893 BSL2893_2; 2919 BFB2919_0",
            "current_status": "DERIVED_KINEMATIC_LAW_COEFFICIENTS_UNFILLED",
            "missing_for_claim": "MISSING_A_SOURCE; MISSING_B_SOURCE",
            "comparator_bound_abs": BETA_BOUND_ABS,
            "next_action": "derive A_source and B_source from the parent source-normalized field equation",
        }
    ),
    base(
        {
            "beta_id": "BSH3018_1_square_law",
            "quantity": "B_source=A_source^2",
            "relation": "delta_beta_source = B_source/A_source^2 - 1, so beta_source zero iff B_source=A_source^2",
            "source_evidence": "2893 BSL2893_3; 2919 BFB2919_1",
            "current_status": "SQUARE_LAW_TARGET_IDENTIFIED_UNSIGNED",
            "missing_for_claim": "MISSING_PARENT_SQUARE_THEOREM_OR_FINITE_RESIDUAL",
            "comparator_bound_abs": BETA_BOUND_ABS,
            "next_action": "try theorem proof before empirical bound fitting",
        }
    ),
    base(
        {
            "beta_id": "BSH3018_2_measured_GM_guard",
            "quantity": "linear_absorption_guard",
            "relation": "A_source=1+a1 eps, B_source=1+b1 eps => beta_eff-1=(b1-2a1)eps+O(eps^2)",
            "source_evidence": "2893 BSL2893_4",
            "current_status": "DERIVED_GUARD",
            "missing_for_claim": "MISSING_b1_MINUS_2a1_ZERO_OR_BOUND",
            "comparator_bound_abs": BETA_BOUND_ABS,
            "next_action": "do not let first-order GM calibration hide second-order source mismatch",
        }
    ),
    base(
        {
            "beta_id": "BSH3018_3_active_heads",
            "quantity": "Delta_beta_total_abs",
            "relation": "sum_abs(source-normalization, operator, boundary/domain, readout and epsilon_SN heads)",
            "source_evidence": "2919 BFB2919_3 through BFB2919_7; 2896 beta envelope components",
            "current_status": "COMPONENT_ENVELOPE_SELECTED_NONCLAIM",
            "missing_for_claim": "MISSING_R11_COMPONENT_VALUES; MISSING_BOUNDARY_DOMAIN_ZERO; MISSING_READOUT_THEOREM; MISSING_GAUSS_ORBITAL_SOURCE_SCORECARD",
            "comparator_bound_abs": BETA_BOUND_ABS,
            "next_action": "3019 should derive the square law or keep a finite beta component ledger",
        }
    ),
    base(
        {
            "beta_id": "BSH3018_4_selected_next",
            "quantity": "3019 target",
            "relation": "beta square-law source-normalization gate is more productive than another gamma loop",
            "source_evidence": "3017 DEC3017_3; 2919 beta fallback; 2893 square-law derivation",
            "current_status": "NEXT_TARGET_SELECTED",
            "missing_for_claim": "MISSING_BETA_SQUARE_LAW_PROOF",
            "comparator_bound_abs": BETA_BOUND_ABS,
            "next_action": "build 3019 beta square-law source-normalization gate",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3018_0_sources",
            "gate": "every cited local source path exists",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "source-backed audit, not memory-only",
        }
    ),
    base(
        {
            "gate_id": "GATE3018_1_gamma_formula",
            "gate": "gamma algebraic interface exists",
            "result": True,
            "notes": "gamma_eff=A_S/A_T and conformal/CR combo laws retained",
        }
    ),
    base(
        {
            "gate_id": "GATE3018_2_gamma_values",
            "gate": "A_T, A_S and readout gauge are source-backed",
            "result": False,
            "notes": "all remain value/source-normalization missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3018_3_gamma_score",
            "gate": "MTS gamma can be scored against Cassini",
            "result": False,
            "notes": "formula exists, but no valid prediction row exists",
        }
    ),
    base(
        {
            "gate_id": "GATE3018_4_beta_handoff",
            "gate": "beta square-law handoff is executable",
            "result": True,
            "notes": "B_source/A_source^2 law exists and coefficient blockers are explicit",
        }
    ),
    base(
        {
            "gate_id": "GATE3018_5_local_GR_claim",
            "gate": "local GR / Newtonian limit is claimable",
            "result": False,
            "notes": "gamma values, beta square-law, alpha3 zero/current theorem and remaining PPN vector are still missing",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3018_0_gamma_progress",
            "decision": "gamma is now an exact coefficient-fill problem rather than a vague GR-limit wish",
            "rationale": "A_T, A_S, s_R, C_R combo and readout gauge are separated with explicit source requirements",
            "consequence": "future work can target one missing coefficient or theorem at a time",
        }
    ),
    base(
        {
            "decision_id": "DEC3018_1_no_gamma_claim",
            "decision": "do not score or claim gamma",
            "rationale": "A_T/A_S/readout values are still missing and 2489 forbids gamma-only PPN/local-GR passes",
            "consequence": "all gamma rows remain nonclaim and fail closed",
        }
    ),
    base(
        {
            "decision_id": "DEC3018_2_route_to_beta",
            "decision": "select beta square-law source-normalization gate as the next leap",
            "rationale": "beta has a clean kinematic law beta_eff=B_source/A_source^2 and directly tests GR-like second-order closure",
            "consequence": "3019 should try to prove B_source=A_source^2 or bound the residual vector",
        }
    ),
    base(
        {
            "decision_id": "DEC3018_3_project_status",
            "decision": "GR reduction path remains live but unclosed",
            "rationale": "gamma algebra is in hand; alpha3 and beta expose the needed parent source-current and source-normalization theorems",
            "consequence": "good progress, not a local-GR pass",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3018_0_3019",
            "target_doc": "3019-Y5-R2FR-beta-square-law-source-normalization-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_beta_square_law_source_normalization_gate_under_AX1090_3019.py",
            "mission": "derive B_source=A_source^2 from the parent source-normalized weak-field equation, or produce a finite beta residual component ledger that remains nonclaim",
            "success_condition": "beta_eff either reduces to 1 by a parent-signed square law in the same observed U convention, or the exact missing A_source/B_source/operator/readout/boundary components are recorded for the next derivation",
            "forbidden": "no EH/Schwarzschild import as MTS proof; no measured-GM shortcut; no gamma-only local-GR claim; no cross-component cancellation; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["gamma_attempt"], gamma_attempt)
write_csv(OUTPUTS["gamma_bound"], gamma_bound)
write_csv(OUTPUTS["beta_handoff"], beta_handoff)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("gamma_attempt_copy", "gamma_attempt"),
    ("gamma_bound_copy", "gamma_bound"),
    ("beta_handoff_copy", "beta_handoff"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3018_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = source_register + gamma_attempt + gamma_bound + beta_handoff + promotion_gates + decision + next_target

gamma_quantities = {row["quantity"] for row in gamma_attempt}
bound_ids = {row["bound_id"] for row in gamma_bound}

validation_rows = [
    {
        "validation_id": "VAL3018_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3018_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3018_02_gamma_slots_present",
        "passed": {"A_T", "A_S", "s_R", "PPN readout gauge", "gamma prediction row"}.issubset(gamma_quantities),
        "requirement": "gamma coefficient fill includes A_T, A_S, s_R, readout gauge and verdict row",
        "evidence": OUTPUTS["gamma_attempt"].name,
    },
    {
        "validation_id": "VAL3018_03_gamma_formulas_present",
        "passed": any("gamma_eff=A_S/A_T" in row["derived_relation"] for row in gamma_attempt)
        and any("gamma_obs_minus_1" in row["derived_relation"] for row in gamma_attempt),
        "requirement": "general gamma ratio and C_R combo law are recorded",
        "evidence": OUTPUTS["gamma_attempt"].name,
    },
    {
        "validation_id": "VAL3018_04_bound_interfaces_present",
        "passed": {"GBI3018_0_general_ratio", "GBI3018_2_conformal_s_R", "GBI3018_3_CR_combo"}.issubset(bound_ids),
        "requirement": "general, conformal and C_R combo bound interfaces are present",
        "evidence": OUTPUTS["gamma_bound"].name,
    },
    {
        "validation_id": "VAL3018_05_gamma_claim_blocked",
        "passed": any(row["slot_id"] == "GAF3018_6_verdict" and row["current_status"] == "BLOCKED_NONCLAIM" for row in gamma_attempt)
        and any(row["gate_id"] == "GATE3018_3_gamma_score" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "no gamma score or local-GR claim is allowed from 3018",
        "evidence": f"{OUTPUTS['gamma_attempt'].name}; {OUTPUTS['gates'].name}",
    },
    {
        "validation_id": "VAL3018_06_beta_handoff_present",
        "passed": any(row["relation"] == "beta_eff = B_source/A_source^2" for row in beta_handoff)
        and any(row["quantity"] == "B_source=A_source^2" for row in beta_handoff),
        "requirement": "beta square-law handoff includes beta_eff and square-law target",
        "evidence": OUTPUTS["beta_handoff"].name,
    },
    {
        "validation_id": "VAL3018_07_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and all(not boolish(row.get("valid_for_claim")) for row in claim_rows),
        "requirement": "all rows remain nonclaim/private-control rows",
        "evidence": "all 3018 generated ledgers",
    },
    {
        "validation_id": "VAL3018_08_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3018 generated ledgers",
    },
    {
        "validation_id": "VAL3018_09_branch_copies_exist",
        "passed": all(boolish(row["exists"]) for row in branch_rows),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": OUTPUTS["branches"].name,
    },
    {
        "validation_id": "VAL3018_10_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3018_11_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3018_12_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3019-Y5-R2FR-beta-square-law-source-normalization"),
        "requirement": "next target selects beta square-law source-normalization gate",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3018_99_overall",
        "passed": overall_pass,
        "requirement": "all 3018 validation checks pass",
        "evidence": "aggregate of VAL3018_00 through VAL3018_12",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3018 - Gamma Coefficient Fill AST or Beta Square-Law Branch under AX1090

Status: `Y5_R2FR_3018_gamma_contract_executable_values_missing_beta_square_law_next`

## Verdict

3018 makes the gamma gate sharper, but does not pretend it is closed.

The usable gamma law is still exact:

`gamma_eff=A_S/A_T`, hence `gamma-1=(A_S-A_T)/A_T`.

That is real progress because the local-GR question is no longer vague. The current missing objects are now precise: `A_T`, `A_S`, `s_R`, the `C_R`/`delta_p` combination, and the fixed-before-readout PPN gauge map.

But none of those coefficient values are parent-signed here. Therefore there is no source-backed Cassini gamma score, no PPN pass, and no local-GR claim.

The constructive move is to stop circling gamma and attack the second-order GR reduction gate:

`beta_eff = B_source/A_source^2`.

If the parent action proves `B_source=A_source^2` in the same observed `U` convention, the local branch gains a serious GR-reduction theorem. If not, the beta residual becomes an explicit component ledger rather than a hidden assumption.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Gamma Coefficient Fill Attempt

{md_table(gamma_attempt, ["slot_id", "quantity", "derived_relation", "current_status", "coefficient_value", "missing_for_claim", "next_action"])}

## Gamma Bound Interface

{md_table(gamma_bound, ["bound_id", "component", "formula", "derived_requirement", "status", "missing_for_claim"])}

## Beta Square-Law Handoff

{md_table(beta_handoff, ["beta_id", "quantity", "relation", "current_status", "missing_for_claim", "next_action"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["gamma_attempt"]}`
- `{OUTPUTS["gamma_bound"]}`
- `{OUTPUTS["beta_handoff"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["gamma_attempt_copy"]}`
- `{BRANCH_OUTPUTS["gamma_bound_copy"]}`
- `{BRANCH_OUTPUTS["beta_handoff_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No gamma score without source-backed `A_T`, `A_S`, and readout gauge.
- No gamma-only local-GR or PPN pass.
- No measured-`GM` shortcut for spatial/time coefficient mismatch.
- No beta pass without `B_source=A_source^2` or a finite source-backed residual below the comparator.
- No `alpha3` pass without source-current/no-flux theorem-zero or an ultratight bound.
- No EH/Schwarzschild import as MTS proof.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
