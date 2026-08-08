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

CHECKPOINT = "3039"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3039-Y5-R2FR-relative-source-vertex-weight-theorem-or-first-XiH-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3039_00_3038_doc": ROOT / "3038-Y5-R2FR-common-source-functional-normal-form-or-XiH-bound-runner-under-AX1090.md",
    "SRC3039_01_3038_normal": RESIDUALS / "P8_Y5_R2FR_3038_COMMON_SOURCE_FUNCTIONAL_NORMAL_FORM_ATTEMPT.csv",
    "SRC3039_02_3038_derivative": RESIDUALS / "P8_Y5_R2FR_3038_FUNCTIONAL_DERIVATIVE_MATCH_AUDIT.csv",
    "SRC3039_03_3038_bounds": RESIDUALS / "P8_Y5_R2FR_3038_XIH_BOUND_RUNNER_SCHEMA.csv",
    "SRC3039_04_3033_shapes": RESIDUALS / "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv",
    "SRC3039_05_3034_tuple": RESIDUALS / "P8_Y5_R2FR_3034_CPSIH_COMPONENT_TUPLE_ROWS.csv",
    "SRC3039_06_3035_ratio": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_PROOF_ATTEMPT.csv",
    "SRC3039_07_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3039_08_2921_pg": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3039_09_no_prefactor": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "SRC3039_10_current_chain": RESIDUALS / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
    "SRC3039_11_parent_derivation": RESIDUALS / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
    "SRC3039_12_parent_terms": RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "SRC3039_13_3036_lock": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3039_SOURCE_REGISTER.csv",
    "quadratic_law": RESIDUALS / "P8_Y5_R2FR_3039_TWO_CHANNEL_QUADRATIC_EULER_LAW.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_3039_RELATIVE_SOURCE_VERTEX_WEIGHT_THEOREM_ATTEMPT.csv",
    "one_potential": RESIDUALS / "P8_Y5_R2FR_3039_SINGLE_POTENTIAL_READOUT_REDUCTION.csv",
    "bound_attempt": RESIDUALS / "P8_Y5_R2FR_3039_FIRST_XIH_BOUND_ROW_ATTEMPT.csv",
    "residual_contract": RESIDUALS / "P8_Y5_R2FR_3039_DELTA_A_PREFACTOR_RESIDUAL_CONTRACT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3039_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3039_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3039_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3039_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3039_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3039_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_attempt_copy": PARENT_ACTION / "relative_source_vertex_weight_theorem_3039_NOT_SIGNED.csv",
    "one_potential_copy": PARENT_ACTION / "single_potential_readout_reduction_3039_CANDIDATE_NONCLAIM.csv",
    "bound_attempt_copy": LOCAL_BOUNDS / "first_XiH_bound_row_attempt_3039_BLOCKED_NONCLAIM.csv",
    "residual_contract_copy": LOCAL_BOUNDS / "delta_A_prefactor_residual_contract_3039_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3039_SINGLE_POTENTIAL_READOUT_OR_XIH_BOUND_NEXT_NONCLAIM.csv",
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
    "SRC3039_00_3038_doc": "3038 handoff to relative weight theorem or XiH bound row",
    "SRC3039_01_3038_normal": "common source functional normal form and insufficiency statement",
    "SRC3039_02_3038_derivative": "functional derivative match audit",
    "SRC3039_03_3038_bounds": "XiH/C_WH/R_lock bound-runner schema",
    "SRC3039_04_3033_shapes": "C_psiH, C_WH and delta_A source coefficient shapes",
    "SRC3039_05_3034_tuple": "C_psiH component tuple with missing JHrho/C_N/K0 owners",
    "SRC3039_06_3035_ratio": "Xi_H definition and unity condition",
    "SRC3039_07_3024_ansatz": "minimal Hcore ansatz and psi_N=-log(N)",
    "SRC3039_08_2921_pg": "conditional Poisson/Gauss branch and W/c^2 coefficient",
    "SRC3039_09_no_prefactor": "no-source-prefactor theorem attempt and live countermodel",
    "SRC3039_10_current_chain": "ordinary matter current-chain attempt",
    "SRC3039_11_parent_derivation": "formal parent action derivation skeleton",
    "SRC3039_12_parent_terms": "parent action term contract and universal coupling rows",
    "SRC3039_13_3036_lock": "source-readout lock matrix",
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

quadratic_law_rows = [
    base(
        {
            "law_id": "TQ3039_0_two_channel_action",
            "object": "independent two-channel local quadratic branch",
            "equation": "S_2 = integral mu_obs[-(C_N K0/2)|grad psi_N|^2 -(O_W/2)|grad chi_W|^2 + rho_H(a_H psi_N + a_W chi_W)]",
            "consequence": "Euler equations have source coefficients Xi_H=-a_H/(C_N K0) and C_W=a_W/O_W up to sign/operator conventions",
            "status": "EXACT_LOCAL_NORMAL_FORM_NONCLAIM",
            "source_path": str(SOURCE_PATHS["SRC3039_01_3038_normal"]),
        }
    ),
    base(
        {
            "law_id": "TQ3039_1_ratio_law",
            "object": "relative source/operator ratio",
            "equation": "delta_prefactor := Xi_H/C_WH - 1 = [-a_H/(C_N K0)]/[a_W/O_W] - 1",
            "consequence": "local GR first-order source normalization is equivalent to a relative vertex/operator equality before R_lock terms",
            "status": "RATIO_LAW_DERIVED_FROM_NORMAL_FORM",
            "source_path": str(SOURCE_PATHS["SRC3039_06_3035_ratio"]),
        }
    ),
    base(
        {
            "law_id": "TQ3039_2_degeneracy",
            "object": "two-channel degeneracy",
            "equation": "rho_H common does not imply a_H/(C_N K0)=a_W/O_W",
            "consequence": "a shared source density still leaves one dimensionless relative coupling unless a parent theorem removes it",
            "status": "FREE_RELATIVE_COUPLING_IDENTIFIED",
            "source_path": str(SOURCE_PATHS["SRC3039_02_3038_derivative"]),
        }
    ),
    base(
        {
            "law_id": "TQ3039_3_claim_gate",
            "object": "source normalization gate",
            "equation": "delta_A_source = delta_prefactor + R_lock",
            "consequence": "claim requires delta_prefactor=0 and R_lock=0 by theorem, or a finite no-cancellation bound below arena thresholds",
            "status": "GATE_EXACT_NONCLAIM",
            "source_path": str(SOURCE_PATHS["SRC3039_03_3038_bounds"]),
        }
    ),
]

theorem_attempt_rows = [
    base(
        {
            "theorem_id": "RSV3039_0_target",
            "claim_piece": "relative source-vertex weight theorem",
            "formal_statement": "parent grammar/symmetry makes the relative coefficient a_H/a_W non-independent and fixes -a_H/(C_N K0)=a_W/O_W",
            "proof_attempt": "combine no-source-prefactor, single action scale, common source functional, readout lock and operator normalization lock",
            "result": "TARGET_EXACT",
            "missing_for_claim": "MISSING_PARENT_OBJECT_LANGUAGE; MISSING_SINGLE_POTENTIAL_READOUT; MISSING_OPERATOR_PULLBACK; MISSING_ACTION_SCALE_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3039_09_no_prefactor"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_1_no_prefactor",
            "claim_piece": "no source-only weights",
            "formal_statement": "pre-action weights w_A(Z), kappa_A(Z) and source labels are untypeable rather than merely absent from an ansatz",
            "proof_attempt": "2645 gives the exact clause and live countermodel",
            "result": "NOT_PROVED",
            "missing_for_claim": "MISSING_TYPED_OBJECT_LANGUAGE; MISSING_NO_SPURION_RETURN; MISSING_MEASURE_COFAME_DESCENT",
            "source_path": str(SOURCE_PATHS["SRC3039_09_no_prefactor"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_2_single_action_scale",
            "claim_piece": "single action and measure normalization",
            "formal_statement": "all source vertices inherit one parent action scale and one observed measure before variation",
            "proof_attempt": "parent action derivation skeleton supports the required shape if full Lagrangian is supplied",
            "result": "FORMAL_IF_ACTION_SUPPLIED",
            "missing_for_claim": "MISSING_FULL_PARENT_LAGRANGIAN; MISSING_HBAR_OR_ACTION_SCALE_OWNER; MISSING_MEASURE_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3039_11_parent_derivation"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_3_operator_pullback",
            "claim_piece": "operator normalization lock",
            "formal_statement": "C_N K0 and O_W are pullbacks of the same parent kinetic Hessian along fixed readout directions",
            "proof_attempt": "3038 identifies the need but current rows only provide separate Hcore and W operator shapes",
            "result": "NOT_PROVED",
            "missing_for_claim": "MISSING_PARENT_KINETIC_HESSIAN; MISSING_READOUT_JACOBIANS; MISSING_POSITIVITY_AND_RANK",
            "source_path": str(SOURCE_PATHS["SRC3039_04_3033_shapes"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_4_single_potential_escape",
            "claim_piece": "metric one-potential route",
            "formal_statement": "if psi_N and chi_W are not independent fields but fixed first-order readouts of one parent scalar phi_g, the independent a_H/a_W freedom disappears",
            "proof_attempt": "rewrite psi_N=r_H phi_g, chi_W=r_W phi_g and require one source pairing integral rho_H a_phi phi_g",
            "result": "PROMISING_CONDITIONAL_ROUTE",
            "missing_for_claim": "MISSING_phi_g_PARENT_READOUT; MISSING_r_H_r_W_VALUES; MISSING_SINGLE_PAIRING_PROOF; MISSING_SIGN_CONVENTION",
            "source_path": str(SOURCE_PATHS["SRC3039_07_3024_ansatz"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_5_two_channel_counterexample",
            "claim_piece": "proof obstruction",
            "formal_statement": "S_src=rho_H(a_H psi_N+a_W chi_W) with arbitrary a_H/a_W is covariant and common-source but fails Xi_H=C_WH generically",
            "proof_attempt": "constructs a legal-looking branch unless parent grammar proves single-potential or no relative source weight",
            "result": "COUNTERMODEL_SURVIVES",
            "missing_for_claim": "MISSING_RULE_MAKING_TWO_CHANNEL_RELATIVE_WEIGHT_UNTYPEABLE",
            "source_path": str(SOURCE_PATHS["SRC3039_01_3038_normal"]),
        }
    ),
    base(
        {
            "theorem_id": "RSV3039_6_verdict",
            "claim_piece": "3039 theorem verdict",
            "formal_statement": "the current corpus does not derive the relative source-vertex weight theorem on the independent two-channel branch",
            "proof_attempt": "the cleanest surviving route is to collapse the two channels to one parent metric potential/readout before fitting",
            "result": "THEOREM_NOT_CLOSED_ROUTE_SHARPENED",
            "missing_for_claim": "MISSING_SINGLE_POTENTIAL_PARENT_READOUT_THEOREM_OR_NUMERIC_BOUND_ROW",
            "source_path": str(SOURCE_PATHS["SRC3039_00_3038_doc"]),
        }
    ),
]

one_potential_rows = [
    base(
        {
            "readout_id": "SPR3039_0_reframe",
            "object": "single parent metric potential",
            "formula": "psi_N = r_H phi_g + O(phi_g^2), chi_W = r_W phi_g + O(phi_g^2)",
            "what_it_buys": "turns two apparent source vertices into projections of one source pairing",
            "status": "CANDIDATE_ROUTE_NOT_SIGNED",
            "missing_for_claim": "MISSING_phi_g_FIELD; MISSING_READOUT_JACOBIANS; MISSING_DOMAIN_OF_VALIDITY",
        }
    ),
    base(
        {
            "readout_id": "SPR3039_1_one_source_pairing",
            "object": "source coupling",
            "formula": "S_src^loc = integral mu_obs rho_H a_phi phi_g",
            "what_it_buys": "a_H and a_W become coordinate artifacts rather than independent constants",
            "status": "CONDITIONAL_IF_PARENT_SIGNED",
            "missing_for_claim": "MISSING_SINGLE_PAIRING_IN_PARENT_ACTION; MISSING_NO_TWO_CHANNEL_SOURCE_SLOT",
        }
    ),
    base(
        {
            "readout_id": "SPR3039_2_operator_pullback",
            "object": "kinetic normalization",
            "formula": "O_H = H_phi r_H^2 and O_W = H_phi r_W^2 on the same Hessian branch",
            "what_it_buys": "operator mismatch can be reduced to readout Jacobians instead of a free coupling",
            "status": "CONDITIONAL_IF_HESSIAN_SIGNED",
            "missing_for_claim": "MISSING_H_phi; MISSING_RANK_ONE_KINETIC_BLOCK; MISSING_BOUNDARY_TERMS",
        }
    ),
    base(
        {
            "readout_id": "SPR3039_3_ratio_condition",
            "object": "single-potential equality law",
            "formula": "Xi_H/C_WH = F(r_H,r_W,H_phi,a_phi,signs); local GR requires this pullback factor to equal 1",
            "what_it_buys": "changes the problem from arbitrary coupling to a concrete readout-Jacobian identity",
            "status": "EXACT_NEXT_DERIVATION_TARGET",
            "missing_for_claim": "MISSING_EXPLICIT_PULLBACK_FACTOR; MISSING_SIGN_AND_UNIT_MAP",
        }
    ),
    base(
        {
            "readout_id": "SPR3039_4_metric_hint",
            "object": "GR weak-field clue",
            "formula": "in a GR-like weak field, lapse and Newtonian potential are one metric perturbation read two ways",
            "what_it_buys": "suggests the next route should be metric-readout degeneracy, not another free source coupling",
            "status": "HEURISTIC_NOT_PROOF",
            "missing_for_claim": "MISSING_MTS_PARENT_METRIC_READOUT_DERIVATION",
        }
    ),
    base(
        {
            "readout_id": "SPR3039_5_gate",
            "object": "single-potential promotion gate",
            "formula": "prove phi_g exists, both readouts descend from it, source pairs once, Hessian pulls back once, and residual boundary terms vanish/bound",
            "what_it_buys": "would close the relative source-vertex problem without a fitted Xi_H",
            "status": "PROMOTION_GATE_OPEN",
            "missing_for_claim": "ALL_FIVE_CLAUSES_UNSIGNED",
        }
    ),
]

bound_attempt_rows = [
    base(
        {
            "bound_row_id": "XB3039_0_attempt",
            "quantity": "Xi_H",
            "definition": "-a_H/(C_N K0)",
            "candidate_value": "MISSING_NUMERIC_VALUE",
            "units": "MISSING_UNITS",
            "source_anchor": "3034 tuple plus 3038 bound schema",
            "status": "BLOCKED_NOT_SOURCE_BACKED",
            "validity_failure": "a_H/JHrho, C_N, K0, sign and unit convention are not numeric parent-owned rows",
        }
    ),
    base(
        {
            "bound_row_id": "XB3039_1_delta",
            "quantity": "delta_XiH",
            "definition": "Xi_H/C_WH - 1",
            "candidate_value": "NOT_COMPUTED",
            "units": "dimensionless",
            "source_anchor": "3035 unity condition",
            "status": "BLOCKED_BY_XiH_AND_CWH",
            "validity_failure": "C_WH remains comparator/conditional without parent G_ref/M_H_ref owner",
        }
    ),
    base(
        {
            "bound_row_id": "XB3039_2_prefactor",
            "quantity": "R_prefactor",
            "definition": "[-a_H/(C_N K0)]/[a_W/O_W] - 1",
            "candidate_value": "NOT_COMPUTED",
            "units": "dimensionless",
            "source_anchor": "3039 two-channel quadratic law",
            "status": "BLOCKED_BY_RELATIVE_WEIGHT",
            "validity_failure": "a_H/a_W and O_W/(C_NK0) are theorem targets, not sourced values",
        }
    ),
    base(
        {
            "bound_row_id": "XB3039_3_first_row_verdict",
            "quantity": "first finite XiH/delta_XiH bound row",
            "definition": "source-backed numeric row suitable for the 3038 bound runner",
            "candidate_value": "NONE",
            "units": "N/A",
            "source_anchor": "3039 synthesis",
            "status": "NO_VALID_BOUND_ROW_CREATED",
            "validity_failure": "fabricating a number would be worse than leaving the gate blocked",
        }
    ),
]

residual_contract_rows = [
    base(
        {
            "contract_id": "DPR3039_0_prefactor",
            "quantity": "delta_prefactor",
            "formula": "delta_prefactor = [-a_H/(C_N K0)]/[a_W/O_W] - 1",
            "promotion_rule": "zero by relative source-vertex/operator theorem, or finite numeric bound",
            "status": "FORMULA_EXACT_NONCLAIM",
        }
    ),
    base(
        {
            "contract_id": "DPR3039_1_single_potential",
            "quantity": "delta_prefactor_single_potential",
            "formula": "delta_prefactor becomes a readout-Jacobian/Hessian pullback residual if psi_N and chi_W descend from one phi_g",
            "promotion_rule": "derive explicit pullback factor and show it equals 1 in the local GR branch",
            "status": "NEXT_DERIVATION_TARGET",
        }
    ),
    base(
        {
            "contract_id": "DPR3039_2_total",
            "quantity": "delta_A_source_total_abs",
            "formula": "abs(delta_prefactor)+abs(R_frame)+abs(R_tau)+abs(R_worldtube)+abs(Omega_GM/M_H_ref)",
            "promotion_rule": "absolute envelope only; no tuned cancellation",
            "status": "BLOCKED_COMPONENTS_MISSING",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3039_0_two_channel",
            "countermodel": "same rho_H couples to psi_N and chi_W with independent a_H and a_W",
            "effect": "common source functional passes while local GR source normalization fails generically",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3039_1_equal_vertices_operator_mismatch",
            "countermodel": "a_H=a_W but C_NK0 and O_W are independent",
            "effect": "relative operator normalization still shifts Xi_H/C_WH",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3039_2_prefactor_grammar_gap",
            "countermodel": "no-source-prefactor is a preferred clause but not made untypeable by parent object language",
            "effect": "source weights can return as legal pre-action constants",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3039_3_single_potential_unsigned",
            "countermodel": "psi_N and chi_W are treated as one metric potential without deriving the readout map",
            "effect": "closes the problem only by axiom if not parent-signed",
            "status": "GUARDRAIL",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3039_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3039 is source-backed to current corpus rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_1_quadratic_law",
            "gate": "two-channel quadratic Euler ratio law is written",
            "result": any(row["law_id"] == "TQ3039_1_ratio_law" for row in quadratic_law_rows),
            "notes": "exact local algebra, nonclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_2_theorem_attempt",
            "gate": "relative source-vertex theorem attempt exists",
            "result": any(row["theorem_id"] == "RSV3039_0_target" for row in theorem_attempt_rows),
            "notes": "attempt fails to close",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_3_theorem_closed",
            "gate": "relative source-vertex theorem is derived",
            "result": False,
            "notes": "two-channel countermodel and operator-pullback gap survive",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_4_single_potential_route",
            "gate": "single-potential readout route is extracted",
            "result": any(row["readout_id"] == "SPR3039_3_ratio_condition" for row in one_potential_rows),
            "notes": "best next derivation route",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_5_bound_row_blocked",
            "gate": "first XiH bound row remains blocked instead of fabricated",
            "result": any(row["status"] == "NO_VALID_BOUND_ROW_CREATED" for row in bound_attempt_rows),
            "notes": "fail-closed empirical fallback",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_6_countermodels",
            "gate": "live countermodels are retained",
            "result": any(row["status"] == "LIVE_BLOCKER" for row in countermodel_rows),
            "notes": "prevents axiom smuggling",
        }
    ),
    base(
        {
            "gate_id": "GATE3039_7_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local-GR/Newton/PPN/R10 claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3039_0_relative_theorem",
            "question": "does the independent two-channel branch derive the relative source-vertex/operator lock?",
            "answer": "NO",
            "reason": "common rho_H plus no-source-prefactor clauses do not by themselves fix a_H/a_W or O_W/(C_NK0)",
            "next_action": "do not claim; move to single-potential readout theorem or source numeric XiH bounds",
        }
    ),
    base(
        {
            "decision_id": "DEC3039_1_best_route",
            "question": "what route has the least scrutiny risk?",
            "answer": "single parent metric potential/readout first",
            "reason": "it converts the free coupling ratio into an explicit readout-Jacobian/Hessian identity, which is a derivable mathematical target rather than a fitted constant",
            "next_action": "3040 should prove or reject psi_N and W/c^2 as fixed first-order readouts of one phi_g",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3039_0_3040",
            "next_checkpoint": "3040-Y5-R2FR-single-potential-readout-theorem-or-two-channel-residual-bound-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_single_potential_readout_theorem_or_two_channel_residual_bound_under_AX1090_3040.py",
            "mission": "prove psi_N and W/c^2 are fixed first-order readouts of one parent metric potential phi_g with one source pairing and one kinetic Hessian, or keep the two-channel residual as a finite bound target",
            "starting_equation": "delta_prefactor = [-a_H/(C_N K0)]/[a_W/O_W] - 1; single-potential route rewrites this as a readout-Jacobian/Hessian pullback residual",
            "do_not_repeat": "do not treat common rho_H or equal a_H=a_W as sufficient; do not assume psi_N=W/c^2 without a parent readout theorem",
            "claim_policy": "no local GR/Newton claim until the single-potential pullback factor equals 1 by theorem or the two-channel residual vector is source-bounded",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "quadratic_law": quadratic_law_rows,
    "theorem_attempt": theorem_attempt_rows,
    "one_potential": one_potential_rows,
    "bound_attempt": bound_attempt_rows,
    "residual_contract": residual_contract_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["theorem_attempt"], BRANCH_OUTPUTS["theorem_attempt_copy"])
shutil.copyfile(OUTPUTS["one_potential"], BRANCH_OUTPUTS["one_potential_copy"])
shutil.copyfile(OUTPUTS["bound_attempt"], BRANCH_OUTPUTS["bound_attempt_copy"])
shutil.copyfile(OUTPUTS["residual_contract"], BRANCH_OUTPUTS["residual_contract_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for relative-weight/single-potential route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + quadratic_law_rows
    + theorem_attempt_rows
    + one_potential_rows
    + bound_attempt_rows
    + residual_contract_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3039_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3039_02_quadratic_law",
            "passed": bool(gates[1]["result"]),
            "requirement": "two-channel quadratic Euler ratio law is written",
            "evidence": OUTPUTS["quadratic_law"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_03_theorem_attempt",
            "passed": bool(gates[2]["result"]),
            "requirement": "relative source-vertex theorem attempt exists",
            "evidence": OUTPUTS["theorem_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_04_theorem_not_claimed",
            "passed": any(row["result"] == "THEOREM_NOT_CLOSED_ROUTE_SHARPENED" for row in theorem_attempt_rows),
            "requirement": "failed theorem is not claim-promoted",
            "evidence": OUTPUTS["theorem_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_05_single_potential_route",
            "passed": bool(gates[4]["result"]),
            "requirement": "single-potential readout route is extracted",
            "evidence": OUTPUTS["one_potential"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_06_bound_fail_closed",
            "passed": bool(gates[5]["result"]),
            "requirement": "first XiH bound row remains blocked instead of fabricated",
            "evidence": OUTPUTS["bound_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_07_residual_contract",
            "passed": any(row["quantity"] == "delta_prefactor" for row in residual_contract_rows),
            "requirement": "delta_prefactor residual contract exists",
            "evidence": OUTPUTS["residual_contract"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_08_countermodels",
            "passed": bool(gates[6]["result"]),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_09_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3039 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3039_10_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_11_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3039_12_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3039_13_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3040-"),
            "requirement": "next target selects single-potential readout theorem or residual bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3039_14_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3039 - Relative Source-Vertex Weight Theorem Or First XiH Bound Row under AX1090

Status: `Y5_R2FR_3039_relative_weight_theorem_not_closed_single_potential_route_extracted_bound_row_blocked`

## Verdict

3039 tries the clean theorem route behind the 3038 condition

`Xi_H=C_WH iff -a_H/(C_N K0)=a_W/O_W`.

The exact two-channel quadratic law is now explicit:

`delta_prefactor = [-a_H/(C_N K0)]/[a_W/O_W] - 1`

and

`delta_A_source = delta_prefactor + R_lock`.

On the independent two-channel branch, the theorem still does **not** close. A common `rho_H` source plus no-source-prefactor clauses do not by themselves fix both the relative vertex `a_H/a_W` and the operator ratio `O_W/(C_N K0)`.

The useful forward move is the single-potential route: if `psi_N` and `W/c^2` are not independent source channels but fixed first-order readouts of one parent metric potential `phi_g`, the apparent coupling freedom can collapse into a concrete readout-Jacobian/Hessian identity. That is the next derivation target.

No finite `Xi_H` bound row was created because the required numeric parent inputs are still missing.

## Two-Channel Quadratic Euler Law

{md_table(quadratic_law_rows, ["law_id", "object", "equation", "consequence", "status"])}

## Relative Source-Vertex Weight Theorem Attempt

{md_table(theorem_attempt_rows, ["theorem_id", "claim_piece", "formal_statement", "result", "missing_for_claim"])}

## Single-Potential Readout Reduction

{md_table(one_potential_rows, ["readout_id", "object", "formula", "what_it_buys", "status", "missing_for_claim"])}

## First XiH Bound Row Attempt

{md_table(bound_attempt_rows, ["bound_row_id", "quantity", "definition", "candidate_value", "status", "validity_failure"])}

## Delta A Prefactor Residual Contract

{md_table(residual_contract_rows, ["contract_id", "quantity", "formula", "promotion_rule", "status"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "effect", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3039 verdict: relative source-vertex theorem not closed; single-potential readout route extracted; XiH bound row blocked.")
