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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3045"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3045-Y5-R2FR-linear-source-normalization-coefficient-map-or-AW-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3045_00_3044_doc": ROOT / "3044-Y5-R2FR-AW-source-amplitude-theorem-or-DWPHI-bound-row-under-AX1090.md",
    "SRC3045_01_3044_theorem": RESIDUALS / "P8_Y5_R2FR_3044_AW_SOURCE_AMPLITUDE_THEOREM_ATTEMPT.csv",
    "SRC3045_02_3044_poisson": RESIDUALS / "P8_Y5_R2FR_3044_POISSON_UNIQUENESS_PROOF_ROUTE.csv",
    "SRC3045_03_3044_bound": RESIDUALS / "P8_Y5_R2FR_3044_DWPHI_AW_BOUND_ROW_SCHEMA.csv",
    "SRC3045_04_3044_next": RESIDUALS / "P8_Y5_R2FR_3044_NEXT_TARGET.csv",
    "SRC3045_05_newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
    "SRC3045_06_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3045_07_hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "SRC3045_08_mass_flux_contract": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
    "SRC3045_09_global_coupling": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3045_10_charge_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "SRC3045_11_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "SRC3045_12_gamma_fill": RESIDUALS / "P8_Y5_R2FR_3018_GAMMA_COEFFICIENT_FILL_ATTEMPT.csv",
    "SRC3045_13_beta_field_contract": RESIDUALS / "P8_Y5_R2FR_3019_SECOND_ORDER_FIELD_EQUATION_CONTRACT.csv",
    "SRC3045_14_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3045_15_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3045_SOURCE_REGISTER.csv",
    "coefficient_map": RESIDUALS / "P8_Y5_R2FR_3045_LINEAR_SOURCE_NORMALIZATION_COEFFICIENT_MAP.csv",
    "ratio_law": RESIDUALS / "P8_Y5_R2FR_3045_AW_COEFFICIENT_RATIO_LAW.csv",
    "premise_ladder": RESIDUALS / "P8_Y5_R2FR_3045_AW_PREMISE_LADDER.csv",
    "epsilon_components": RESIDUALS / "P8_Y5_R2FR_3045_EPSILON_A_COMPONENT_SCHEMA.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3045_DWPHI_FROM_LINEAR_COEFFICIENT_BOUND_SCHEMA.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3045_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3045_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3045_PROMOTION_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3045_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3045_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3045_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "coefficient_copy": PARENT_ACTION / "linear_source_normalization_coefficient_map_3045_NOT_SIGNED.csv",
    "ratio_copy": PARENT_ACTION / "AW_coefficient_ratio_law_3045_CONDITIONAL_NONCLAIM.csv",
    "premise_copy": PARENT_ACTION / "AW_premise_ladder_3045_NONCLAIM.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_A_component_schema_3045_BLOCKED_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "D_WPhi_from_linear_coefficient_3045_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3045_GREF_GEFFECTIVE_LOCK_OR_EPSILON_A_BOUND_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


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
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3045_00_3044_doc": "3044 handoff to linear source-normalization map",
    "SRC3045_01_3044_theorem": "A_W theorem attempt and not-claimed verdict",
    "SRC3045_02_3044_poisson": "Poisson uniqueness route premises",
    "SRC3045_03_3044_bound": "D_WPhi/A_W bound schema",
    "SRC3045_04_3044_next": "3045 target selector",
    "SRC3045_05_newton_stack": "source-normalized Newton rungs including SN5",
    "SRC3045_06_pg_contract": "Poisson/Gauss coefficient and calibration contract",
    "SRC3045_07_hilbert_contract": "Hilbert monopole/source calibration contract",
    "SRC3045_08_mass_flux_contract": "mass flux projector and absolute calibration contract",
    "SRC3045_09_global_coupling": "constant/global coupling superselection contract",
    "SRC3045_10_charge_attempt": "charge/current direct attempt",
    "SRC3045_11_gamma_kernel": "A_T gamma denominator algebra",
    "SRC3045_12_gamma_fill": "A_T source-normalization unfilled row",
    "SRC3045_13_beta_field_contract": "W denominator and A_source coefficient contract",
    "SRC3045_14_min_parent": "minimum parent local-GR action blocks",
    "SRC3045_15_symbol_map": "symbol to local-GR action map",
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

coefficient_map = [
    base(
        {
            "coefficient_id": "LCM3045_0_general_linear_pair",
            "quantity": "A_W",
            "definition": "linear coefficient in Phi_metric=A_W W",
            "derived_expression": "if ∇²Phi_metric=C_Phi rho_H+R_Phi and ∇²W=C_W rho_H+R_W, then A_W=C_Phi/C_W only when R_Phi-R_W is zero/common-mode and boundary data match",
            "current_status": "RATIO_LAW_DERIVED_PREMISES_UNSIGNED",
            "missing_for_claim": "MISSING_C_PHI_PARENT_VALUE; MISSING_C_W_PARENT_VALUE; MISSING_RESIDUAL_DIFFERENCE_ZERO; MISSING_BOUNDARY_LOCK",
            "source_anchor": "3044 PUN3044_1/PUN3044_2",
        }
    ),
    base(
        {
            "coefficient_id": "LCM3045_1_metric_phi_coefficient",
            "quantity": "C_Phi",
            "definition": "source coefficient in the same-frame metric Poisson equation",
            "derived_expression": "C_Phi = kappa_eff c^4/2 in the EH weak-field 00 branch",
            "current_status": "CONDITIONAL_FROM_EH_SOURCE_STACK_ONLY",
            "missing_for_claim": "MISSING_EH_ONLY_OPERATOR_SELECTION; MISSING_NONRELATIVISTIC_HILBERT_SOURCE_LIMIT; MISSING_NO_SOURCE_RESIDUALS",
            "source_anchor": "SN5/PG3",
        }
    ),
    base(
        {
            "coefficient_id": "LCM3045_2_W_denominator_coefficient",
            "quantity": "C_W",
            "definition": "source coefficient defining W before measured-GM fitting",
            "derived_expression": "C_W = 4*pi*G_ref if ∇²W=4*pi*G_ref rho_H is parent-owned",
            "current_status": "DENOMINATOR_CONTRACT_PRESENT_UNSIGNED",
            "missing_for_claim": "MISSING_PARENT_SOURCE_DEFINITION_FOR_W; MISSING_G_REF_OWNER; MISSING_SAME_SOURCE_DENSITY",
            "source_anchor": "FEC3019_0",
        }
    ),
    base(
        {
            "coefficient_id": "LCM3045_3_ratio_specialization",
            "quantity": "A_W_ratio",
            "definition": "ratio of the EH metric coefficient to the W denominator coefficient",
            "derived_expression": "A_W = C_Phi/C_W = kappa_eff c^4/(8*pi*G_ref)",
            "current_status": "DERIVED_CONDITIONAL_RATIO",
            "missing_for_claim": "MISSING_G_REF_EQUALS_KAPPA_EFF_C4_OVER_8PI; MISSING_PARENT_REFERENCE_NORMALIZATION",
            "source_anchor": "LCM3045_1/LCM3045_2",
        }
    ),
    base(
        {
            "coefficient_id": "LCM3045_4_AW_unity_condition",
            "quantity": "A_W=1 condition",
            "definition": "condition under which W and Phi_metric share the same normalization",
            "derived_expression": "A_W=1 iff G_ref = kappa_eff c^4/(8*pi), with same frame/source/boundary and no residual difference",
            "current_status": "EXACT_CONDITION_DERIVED_NOT_SIGNED",
            "missing_for_claim": "MISSING_GLOBAL_COUPLING_REFERENCE_LOCK; MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD; MISSING_RESIDUAL_SILENCE",
            "source_anchor": "PG7/HM4/MF7/GS0-GS7",
        }
    ),
    base(
        {
            "coefficient_id": "LCM3045_5_verdict",
            "quantity": "linear source-normalization coefficient map",
            "definition": "current status of deriving A_W=1 from parent/source normalization",
            "derived_expression": "map exists but current parent evidence does not sign the reference-coupling lock or residual silence",
            "current_status": "A_W_NOT_CLOSED_LINEAR_MAP_READY",
            "missing_for_claim": "MISSING_G_REF_LOCK_OR_NUMERIC_EPSILON_A_BOUND",
            "source_anchor": "3045 aggregate",
        }
    ),
]

ratio_law = [
    base(
        {
            "law_id": "RLAW3045_0_source_equations",
            "statement": "Let ∇²Phi=C_Phi rho_H+R_Phi and ∇²W=C_W rho_H+R_W on the same exterior domain.",
            "derivation": "subtract (C_Phi/C_W) times the W equation from the Phi equation",
            "result": "∇²[Phi-(C_Phi/C_W)W]=R_Phi-(C_Phi/C_W)R_W",
            "status": "DERIVED",
        }
    ),
    base(
        {
            "law_id": "RLAW3045_1_homogeneous_case",
            "statement": "If R_Phi-(C_Phi/C_W)R_W=0 and boundary data match after the same scaling, the difference is harmonic with zero boundary data.",
            "derivation": "elliptic uniqueness/maximum principle on the local exterior",
            "result": "Phi=(C_Phi/C_W)W",
            "status": "MATH_VALID_IF_PREMISES_PASS",
        }
    ),
    base(
        {
            "law_id": "RLAW3045_2_EH_W_ratio",
            "statement": "Using C_Phi=kappa_eff c^4/2 and C_W=4*pi*G_ref gives the source-amplitude ratio.",
            "derivation": "(kappa_eff c^4/2)/(4*pi*G_ref)",
            "result": "A_W=kappa_eff c^4/(8*pi*G_ref)",
            "status": "DERIVED_CONDITIONAL_RATIO",
        }
    ),
    base(
        {
            "law_id": "RLAW3045_3_unity_lock",
            "statement": "The unity coefficient is not a convention unless G_ref is parent-identified with the same kappa_eff/G_eff branch before measured-GM fitting.",
            "derivation": "A_W=1 iff G_ref=kappa_eff c^4/(8*pi)",
            "result": "G_ref/G_eff lock is the next missing theorem or residual row",
            "status": "LOCK_IDENTIFIED_NOT_SIGNED",
        }
    ),
]

premise_ladder = [
    base({"rung_id": "LAD3045_0_same_frame", "required_identity": "Phi, W, rho_H and test-body readout are in one observed/source frame", "source_anchor": "SN0/PG2", "current_status": "CONDITIONAL_NOT_PARENT_DERIVED", "if_missing": "A_W may be frame conversion"}),
    base({"rung_id": "LAD3045_1_EH_operator", "required_identity": "local 00 operator is EH Poisson or all non-EH operators are zero/scored", "source_anchor": "SN1/PG3", "current_status": "CONDITIONAL_EH_ONLY_NOT_PARENT_DERIVED_R11_VECTOR_UNFILLED", "if_missing": "C_Phi gains operator residual"}),
    base({"rung_id": "LAD3045_2_Hilbert_source", "required_identity": "same Hilbert/source density rho_H defines both equations", "source_anchor": "HM0/HM1/CC2/CC3", "current_status": "CONDITIONAL_OR_NOT_PARENT_DERIVED", "if_missing": "C_Phi/C_W compares different sources"}),
    base({"rung_id": "LAD3045_3_W_denominator", "required_identity": "W is parent-defined by ∇²W=4*pi*G_ref rho_H before orbital fitting", "source_anchor": "FEC3019_0", "current_status": "DENOMINATOR_CONTRACT_PRESENT_UNSIGNED", "if_missing": "W can be a fitted source coordinate"}),
    base({"rung_id": "LAD3045_4_Gref_lock", "required_identity": "G_ref equals kappa_eff c^4/(8*pi) as a parent normalization", "source_anchor": "PG7/HM4/MF7/GS0-GS7", "current_status": "MISSING_GLOBAL_COUPLING_REFERENCE_LOCK", "if_missing": "A_W remains G_eff/G_ref residual"}),
    base({"rung_id": "LAD3045_5_no_extra_monopole", "required_identity": "mu_extra, range, boundary, projector, memory and non-Hilbert monopoles vanish or are bounded", "source_anchor": "PG6/HM5/MF6", "current_status": "NOT_PARENT_DERIVED", "if_missing": "A_W absorbs hidden source residual"}),
    base({"rung_id": "LAD3045_6_boundary_lock", "required_identity": "same additive/asymptotic boundary condition for Phi and W", "source_anchor": "3044 PUN3044_4", "current_status": "MISSING_SAME_BOUNDARY_OR_ASYMPTOTIC_LOCK", "if_missing": "homogeneous hair survives"}),
    base({"rung_id": "LAD3045_7_AW_conclusion", "required_identity": "all LAD3045_0 through LAD3045_6 pass", "source_anchor": "3045 aggregate", "current_status": "CONCLUSION_BLOCKED_BY_PRIOR_RUNGS", "if_missing": "no A_W=1/Newton/local-GR claim"}),
]

epsilon_components = [
    base({"component_id": "EPSA3045_0_coupling_reference", "quantity": "epsilon_Gref", "definition": "kappa_eff c^4/(8*pi*G_ref)-1", "status": "FORMULA_READY_VALUE_MISSING", "missing_input": "G_ref/kappa_eff parent lock or numeric bound", "affected_tests": "Newton;PPN;R10;orbital"}),
    base({"component_id": "EPSA3045_1_frame", "quantity": "epsilon_frame", "definition": "same-frame conversion between source equation and matter readout", "status": "MISSING_FRAME_SOURCE_THEOREM_OR_BOUND", "missing_input": "delta_frame_source", "affected_tests": "Newton;PPN;clock;WEP"}),
    base({"component_id": "EPSA3045_2_operator", "quantity": "epsilon_operator", "definition": "non-EH/R11 linear 00 operator contribution to C_Phi", "status": "MISSING_R11_VECTOR_ZERO_OR_VALUE", "missing_input": "c_nonEH_operator_vector", "affected_tests": "PPN;R10;local_GR"}),
    base({"component_id": "EPSA3045_3_source_current", "quantity": "epsilon_source_current", "definition": "Hilbert/projected source mismatch between rho_H and W source", "status": "MISSING_CHARGE_CURRENT_EQUALITY", "missing_input": "eta_source_AB; Pi_M current closure", "affected_tests": "WEP;Newton;orbital"}),
    base({"component_id": "EPSA3045_4_extra_monopole", "quantity": "epsilon_mu_extra", "definition": "mu_extra/(G_eff M_eff) from boundary/bulk/domain/range/memory/connection channels", "status": "MISSING_ZERO_OR_NUMERIC_MU_EXTRA", "missing_input": "mu_extra coefficient map", "affected_tests": "Newton;R10;orbital"}),
    base({"component_id": "EPSA3045_5_boundary", "quantity": "epsilon_boundary", "definition": "homogeneous boundary/asymptotic mismatch in Phi-(C_Phi/C_W)W", "status": "MISSING_BOUNDARY_LOCK_OR_BOUND", "missing_input": "boundary/asymptotic reference equality", "affected_tests": "Newton;PPN;orbital"}),
    base({"component_id": "EPSA3045_6_range_radial", "quantity": "epsilon_range_radial", "definition": "finite-range or radial dependence in G_eff, M_eff, or W/Phi source strength", "status": "MISSING_RANGE_RADIAL_ZERO_OR_BOUND", "missing_input": "alpha(lambda); partial_r ln mu_obs", "affected_tests": "R10;orbital;galaxy_bridge"}),
    base({"component_id": "EPSA3045_7_readout", "quantity": "epsilon_readout", "definition": "readout/gauge conversion that changes the extracted first-order metric coefficient", "status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION", "missing_input": "PPN readout gauge", "affected_tests": "PPN gamma/beta"}),
]

bound_rows = [
    base(
        {
            "bound_id": "BND3045_0_AW_ratio",
            "quantity": "A_W",
            "expression": "A_W=kappa_eff c^4/(8*pi*G_ref)+epsilon_frame+epsilon_operator+epsilon_source_current+epsilon_mu_extra+epsilon_boundary+epsilon_range_radial+epsilon_readout",
            "units": "dimensionless",
            "status": "SYMBOLIC_COMPONENT_BOUND_READY_VALUES_MISSING",
            "blocking_issue": "MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS",
            "claim_use": "cannot score A_W yet",
        }
    ),
    base(
        {
            "bound_id": "BND3045_1_Delta_A",
            "quantity": "Delta_A",
            "expression": "|epsilon_Gref|+|epsilon_frame|+|epsilon_operator|+|epsilon_source_current|+|epsilon_mu_extra|+|epsilon_boundary|+|epsilon_range_radial|+|epsilon_readout|",
            "units": "dimensionless",
            "status": "BOUND_ENVELOPE_READY_VALUES_MISSING",
            "blocking_issue": "MISSING_NUMERIC_OR_THEOREM_ZERO_COMPONENT_ROWS",
            "claim_use": "needed before D_WPhi bound row is executable",
        }
    ),
    base(
        {
            "bound_id": "BND3045_2_DWPhi",
            "quantity": "D_WPhi_total_abs",
            "expression": "|D_WPhi| <= Delta_A/(1-Delta_A) for Delta_A<1",
            "units": "dimensionless",
            "status": "NO_VALID_BOUND_ROW_CREATED",
            "blocking_issue": "MISSING_DELTA_A",
            "claim_use": "no D_WPhi/Newton/PPN/local-GR claim",
        }
    ),
]

countermodels = [
    base({"countermodel_id": "CM3045_0_Gref_mismatch", "case": "G_ref differs from kappa_eff c^4/(8*pi) by a constant factor", "why_it_blocks": "all orbital data can absorb the factor while parent A_W is not unity", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3045_1_nonEH_linear_operator", "case": "a retained R11/source-normalization operator contributes at linear order", "why_it_blocks": "C_Phi is not just kappa_eff c^4/2", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3045_2_source_current_split", "case": "rho_H in metric equation and W source density differ by projector/source-current leakage", "why_it_blocks": "C_Phi/C_W compares different right-hand sides", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3045_3_boundary_hair", "case": "Phi-(C_Phi/C_W)W has nonzero homogeneous exterior data", "why_it_blocks": "the ratio law alone does not kill boundary/asymptotic hair", "status": "LIVE_BLOCKER"}),
]

decision_rows = [
    base({"decision_id": "DEC3045_0_ratio", "question": "can the linear coefficient map be written exactly?", "answer": "YES_CONDITIONAL", "reason": "A_W=C_Phi/C_W and EH/W rows give A_W=kappa_eff c^4/(8*pi*G_ref)", "action": "promote ratio law, not unity claim"}),
    base({"decision_id": "DEC3045_1_unity", "question": "is A_W=1 derived now?", "answer": "NO", "reason": "G_ref lock, same-source ownership, residual silence, and boundary lock are unsigned", "action": "keep epsilon_A/D_WPhi residual"}),
    base({"decision_id": "DEC3045_2_shortcut", "question": "can measured orbital GM set G_ref=G_eff?", "answer": "NO", "reason": "that would make A_W a post-fit convention rather than a parent prediction", "action": "require parent normalization or explicit residual bound"}),
    base({"decision_id": "DEC3045_3_next", "question": "what is the next least-smuggly target?", "answer": "G_ref/G_eff reference lock or epsilon_A bound", "reason": "the remaining first-order obstruction is no longer W but the parent coupling/reference identity", "action": "3046 should prove the global/reference coupling lock or stage numeric component rows"}),
]

gates = [
    base({"gate_id": "GATE3045_0_sources_exist", "gate": "all cited source paths exist", "passed": all(boolish(row["exists"]) for row in source_register), "claim_effect": "source-backed checkpoint"}),
    base({"gate_id": "GATE3045_1_ratio_law", "gate": "A_W=C_Phi/C_W ratio law is derived", "passed": True, "claim_effect": "real mathematical progress"}),
    base({"gate_id": "GATE3045_2_EH_ratio", "gate": "A_W=kappa_eff c^4/(8*pi*G_ref) conditional ratio is recorded", "passed": True, "claim_effect": "identifies coupling/reference lock"}),
    base({"gate_id": "GATE3045_3_Gref_lock", "gate": "G_ref equals kappa_eff c^4/(8*pi) is parent-signed", "passed": False, "claim_effect": "blocks A_W=1"}),
    base({"gate_id": "GATE3045_4_same_source", "gate": "same Hilbert/source density is parent-signed for both equations", "passed": False, "claim_effect": "blocks source-normalized Newton"}),
    base({"gate_id": "GATE3045_5_residual_silence", "gate": "operator/source/boundary/range/readout residual difference is zero or bounded", "passed": False, "claim_effect": "blocks D_WPhi=0"}),
    base({"gate_id": "GATE3045_6_component_bound", "gate": "epsilon_A component rows have numeric or theorem-zero values", "passed": False, "claim_effect": "blocks executable A_W bound"}),
    base({"gate_id": "GATE3045_7_no_claim_rows", "gate": "no generated 3045 row is valid for claim", "passed": True, "claim_effect": "private nonclaim checkpoint"}),
    base({"gate_id": "GATE3045_8_next_target", "gate": "next target selects G_ref/G_eff lock or epsilon_A bound", "passed": True, "claim_effect": "does not circle W again"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3045_0_3046",
            "next_checkpoint": "3046-Y5-R2FR-Gref-Geff-reference-lock-or-epsilon-A-bound-row-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_Gref_Geff_reference_lock_or_epsilon_A_bound_row_under_AX1090_3046.py",
            "mission": "prove G_ref=kappa_eff c^4/(8*pi) as a parent/source-normalization identity with same-source residual silence, or create first source-backed epsilon_A component rows",
            "starting_equation": "A_W=kappa_eff c^4/(8*pi*G_ref)+epsilon_A_residual; D_WPhi=-epsilon_A/(1+epsilon_A)",
            "do_not_repeat": "do not infer the reference lock from fitted orbital GM or a naming convention",
            "claim_policy": "no Newton/PPN/local-GR claim until the reference lock or Delta_A bound is parent-signed/source-backed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["coefficient_map"], coefficient_map)
write_csv(OUTPUTS["ratio_law"], ratio_law)
write_csv(OUTPUTS["premise_ladder"], premise_ladder)
write_csv(OUTPUTS["epsilon_components"], epsilon_components)
write_csv(OUTPUTS["bound"], bound_rows)
write_csv(OUTPUTS["countermodels"], countermodels)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["gates"], gates)
write_csv(OUTPUTS["next"], next_rows)

branch_map = [
    ("coefficient_copy", OUTPUTS["coefficient_map"], BRANCH_OUTPUTS["coefficient_copy"], "linear source-normalization coefficient map copy"),
    ("ratio_copy", OUTPUTS["ratio_law"], BRANCH_OUTPUTS["ratio_copy"], "A_W coefficient ratio law copy"),
    ("premise_copy", OUTPUTS["premise_ladder"], BRANCH_OUTPUTS["premise_copy"], "A_W premise ladder copy"),
    ("epsilon_copy", OUTPUTS["epsilon_components"], BRANCH_OUTPUTS["epsilon_copy"], "epsilon_A component schema copy"),
    ("bound_copy", OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"], "blocked D_WPhi bound schema copy"),
    ("queue_copy", OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"], "3046 acquisition queue copy"),
]
branch_rows: list[dict[str, Any]] = []
for copy_id, source, destination, description in branch_map:
    shutil.copyfile(source, destination)
    branch_rows.append(
        base(
            {
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "description": description,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
non_validation_csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
formalization_hits = list(FORMALIZATION.rglob("*3045*")) if FORMALIZATION.exists() else []

all_non_validation_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_non_validation_rows.extend(rows(path))

validation_rows = [
    base({"validation_id": "VAL3045_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3045_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated non-validation CSV and branch-copy rows parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3045_02_ratio_law", "passed": any(row["coefficient_id"] == "LCM3045_3_ratio_specialization" and "kappa_eff c^4/(8*pi*G_ref)" in row["derived_expression"] for row in coefficient_map), "requirement": "A_W ratio law is recorded", "evidence": OUTPUTS["coefficient_map"].name}),
    base({"validation_id": "VAL3045_03_unity_not_promoted", "passed": any(row["decision_id"] == "DEC3045_1_unity" and row["answer"] == "NO" for row in decision_rows), "requirement": "A_W=1 is not claimed", "evidence": OUTPUTS["decision"].name}),
    base({"validation_id": "VAL3045_04_Gref_gate_fails", "passed": any(row["gate_id"] == "GATE3045_3_Gref_lock" and not boolish(row["passed"]) for row in gates), "requirement": "G_ref lock remains failed for claim", "evidence": OUTPUTS["gates"].name}),
    base({"validation_id": "VAL3045_05_bound_fail_closed", "passed": any(row["bound_id"] == "BND3045_2_DWPhi" and row["status"] == "NO_VALID_BOUND_ROW_CREATED" for row in bound_rows), "requirement": "D_WPhi bound row remains blocked without Delta_A", "evidence": OUTPUTS["bound"].name}),
    base({"validation_id": "VAL3045_06_no_claim_rows", "passed": not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("valid_prediction_row")) for row in all_non_validation_rows), "requirement": "no 3045 row is valid for claim", "evidence": "generated rows"}),
    base({"validation_id": "VAL3045_07_countermodels_live", "passed": len(countermodels) >= 4 and all(row["status"] == "LIVE_BLOCKER" for row in countermodels), "requirement": "shortcut countermodels remain live", "evidence": OUTPUTS["countermodels"].name}),
    base({"validation_id": "VAL3045_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3045_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3045_10_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3045 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3045_11_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3046-"), "requirement": "next target selects G_ref/G_eff lock or epsilon_A bound", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3045_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3045 - Linear Source-Normalization Coefficient Map or A_W Bound Row

Status: `Y5_R2FR_3045_AW_ratio_law_derived_Gref_lock_open`

Generated: `{RUN_UTC}`

## Verdict

3045 extracts the first-order source-normalization map instead of circling the `W` symbol again.

If

`nabla^2 Phi_metric = C_Phi rho_H + R_Phi`

and

`nabla^2 W = C_W rho_H + R_W`,

then the local amplitude is controlled by the ratio `A_W=C_Phi/C_W`, provided the residual difference and boundary data are silent.

Using the existing EH/source row gives the sharper conditional law:

`A_W = kappa_eff c^4/(8*pi*G_ref)`.

So `A_W=1` is not a free notation choice. It requires the parent/reference identity

`G_ref = kappa_eff c^4/(8*pi)`,

plus same frame, same Hilbert source, no extra monopole/source residual, and same boundary/asymptotic condition. Those premises are not signed yet, so 3045 does not claim Newton, PPN, local GR, `A_W=1`, or `D_WPhi=0`.

## Coefficient Map

{md_table(coefficient_map, ["coefficient_id", "quantity", "derived_expression", "current_status", "missing_for_claim"])}

## Ratio Law

{md_table(ratio_law, ["law_id", "statement", "derivation", "result", "status"])}

## Premise Ladder

{md_table(premise_ladder, ["rung_id", "required_identity", "current_status", "if_missing"])}

## Epsilon_A Components

{md_table(epsilon_components, ["component_id", "quantity", "definition", "status", "missing_input"])}

## Bound Schema

{md_table(bound_rows, ["bound_id", "quantity", "expression", "status", "blocking_issue"])}

## Countermodels

{md_table(countermodels, ["countermodel_id", "case", "why_it_blocks", "status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "passed", "claim_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3045 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: A_W ratio law derived; G_ref lock open; no claim rows")
