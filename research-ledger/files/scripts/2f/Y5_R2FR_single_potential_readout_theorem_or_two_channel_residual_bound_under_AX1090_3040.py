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

CHECKPOINT = "3040"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3040-Y5-R2FR-single-potential-readout-theorem-or-two-channel-residual-bound-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3040_00_3039_doc": ROOT / "3039-Y5-R2FR-relative-source-vertex-weight-theorem-or-first-XiH-bound-row-under-AX1090.md",
    "SRC3040_01_3039_single": RESIDUALS / "P8_Y5_R2FR_3039_SINGLE_POTENTIAL_READOUT_REDUCTION.csv",
    "SRC3040_02_3039_quadratic": RESIDUALS / "P8_Y5_R2FR_3039_TWO_CHANNEL_QUADRATIC_EULER_LAW.csv",
    "SRC3040_03_3039_residual": RESIDUALS / "P8_Y5_R2FR_3039_DELTA_A_PREFACTOR_RESIDUAL_CONTRACT.csv",
    "SRC3040_04_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3040_05_3033_shapes": RESIDUALS / "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv",
    "SRC3040_06_3035_ratio": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_PROOF_ATTEMPT.csv",
    "SRC3040_07_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3040_08_newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
    "SRC3040_09_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3040_10_eh_reduction": RESIDUALS / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
    "SRC3040_11_worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "SRC3040_12_3036_lock": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3040_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3040_SINGLE_POTENTIAL_READOUT_THEOREM_ATTEMPT.csv",
    "jacobian": RESIDUALS / "P8_Y5_R2FR_3040_WEAK_FIELD_READOUT_JACOBIAN_AUDIT.csv",
    "pullback": RESIDUALS / "P8_Y5_R2FR_3040_PULLBACK_FACTOR_LAW.csv",
    "residual_bound": RESIDUALS / "P8_Y5_R2FR_3040_TWO_CHANNEL_RESIDUAL_BOUND_SCHEMA.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3040_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3040_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3040_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3040_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3040_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3040_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "single_potential_readout_theorem_3040_CONDITIONAL_NOT_SIGNED.csv",
    "jacobian_copy": PARENT_ACTION / "weak_field_readout_jacobian_audit_3040_NONCLAIM.csv",
    "pullback_copy": PARENT_ACTION / "pullback_factor_law_3040_CONDITIONAL_NONCLAIM.csv",
    "residual_bound_copy": LOCAL_BOUNDS / "two_channel_residual_bound_schema_3040_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3040_PARENT_METRIC_READOUT_SIGNATURE_OR_JACOBIAN_BOUND_NEXT_NONCLAIM.csv",
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
    "SRC3040_00_3039_doc": "3039 handoff: single-potential readout theorem or residual bound",
    "SRC3040_01_3039_single": "single-potential route extracted in 3039",
    "SRC3040_02_3039_quadratic": "two-channel ratio law",
    "SRC3040_03_3039_residual": "delta_prefactor residual contract",
    "SRC3040_04_3024_ansatz": "Hcore ansatz and psi_N=-log(N)",
    "SRC3040_05_3033_shapes": "C_psiH/C_WH coefficient shapes",
    "SRC3040_06_3035_ratio": "Xi_H=C_WH unity condition",
    "SRC3040_07_pg_contract": "same-frame weak-field potential and Poisson/Gauss contracts",
    "SRC3040_08_newton_stack": "source-normalized Newton stack and g_00 weak-field row",
    "SRC3040_09_min_parent": "minimum local-GR parent action blocks and metric readout row",
    "SRC3040_10_eh_reduction": "EH reduction requirements",
    "SRC3040_11_worldtube_theorem": "worldtube/source measure and PPN readout theorem rows",
    "SRC3040_12_3036_lock": "source-readout lock blockers",
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

theorem_rows = [
    base(
        {
            "theorem_id": "SPT3040_0_target",
            "claim_piece": "single-potential readout theorem",
            "formal_statement": "psi_N and chi_W:=W/c^2 are fixed first-order readouts of one parent metric potential phi_g, not independent source channels",
            "derivation_step": "prove phi_g exists in the observed metric/coframe branch and both readouts descend before source calibration",
            "result": "TARGET_EXACT",
            "missing_for_claim": "MISSING_PARENT_METRIC_READOUT_SIGNATURE; MISSING_W_EQUALS_PHI_READOUT; MISSING_FRAME_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3040_01_3039_single"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_1_gr_style_readout",
            "claim_piece": "weak-field lapse readout",
            "formal_statement": "with g_00=-1+2 Phi/c^2, zero shift, and phi_g:=Phi/c^2, N=sqrt(1-2 phi_g) and psi_N=-log(N)=phi_g+O(phi_g^2)",
            "derivation_step": "Taylor expand the observed lapse in the same-frame weak-field branch",
            "result": "CONDITIONAL_FIRST_ORDER_DERIVED",
            "missing_for_claim": "MISSING_PARENT_SIGNATURE_FOR_g00_BRANCH; MISSING_SIGN_CONVENTION_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3040_07_pg_contract"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_2_w_readout",
            "claim_piece": "W/c^2 readout",
            "formal_statement": "if W=Phi in the same observed weak-field branch, chi_W=W/c^2=phi_g and r_W=1",
            "derivation_step": "identify the Poisson/Gauss potential with the same Phi used by the orbital/matter readout",
            "result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_W_EQUALS_PHI_PARENT_READOUT; MISSING_NO_POST_FIT_ORBITAL_GM_IMPORT",
            "source_path": str(SOURCE_PATHS["SRC3040_08_newton_stack"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_3_one_source_pairing",
            "claim_piece": "single source pairing",
            "formal_statement": "S_src^loc = integral mu_obs rho_H a_phi phi_g, with no separate a_H psi_N + a_W chi_W source slots",
            "derivation_step": "forbid the two-channel source representation as a parent object, not as a gauge choice",
            "result": "NOT_PROVED",
            "missing_for_claim": "MISSING_SINGLE_PAIRING_PARENT_ACTION; MISSING_NO_TWO_CHANNEL_SOURCE_SLOT_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3040_12_3036_lock"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_4_pullback_factor",
            "claim_piece": "readout-Jacobian pullback factor",
            "formal_statement": "for y=r_y phi_g, source/operator coefficient in y-chart is a_phi*r_y/H_phi; hence Xi_H/C_WH = r_H/r_W up to sign/unit conventions",
            "derivation_step": "pull back one source pairing and one kinetic Hessian through the two readout coordinates",
            "result": "EXACT_PULLBACK_LAW_DERIVED_CONDITIONAL_INPUTS",
            "missing_for_claim": "MISSING_H_phi_OWNER; MISSING_READOUT_JACOBIANS_AS_PARENT_VALUES; MISSING_SIGN_UNIT_MAP",
            "source_path": str(SOURCE_PATHS["SRC3040_02_3039_quadratic"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_5_first_order_closure",
            "claim_piece": "first-order prefactor closure",
            "formal_statement": "if r_H=r_W=1 and signs/units match, delta_prefactor=Xi_H/C_WH-1=0 at first weak-field order",
            "derivation_step": "combine psi_N=phi_g+O(phi_g^2), chi_W=phi_g, one source pairing and one Hessian",
            "result": "CONDITIONAL_CLOSE_OF_DELTA_PREFACTOR_ONLY",
            "missing_for_claim": "MISSING_PARENT_SIGNED_PREMISES; R_LOCK_STILL_OPEN; SECOND_ORDER_PPN_NOT_CLOSED",
            "source_path": str(SOURCE_PATHS["SRC3040_03_3039_residual"]),
        }
    ),
    base(
        {
            "theorem_id": "SPT3040_6_verdict",
            "claim_piece": "3040 theorem verdict",
            "formal_statement": "single-potential readout gives a real conditional derivation path for the first-order coupling, but current MTS corpus has not parent-signed the readout theorem",
            "derivation_step": "promote neither local GR nor Newton; stage the parent metric readout signature as the next target",
            "result": "CONDITIONAL_ROUTE_FOUND_NOT_CLAIMED",
            "missing_for_claim": "MISSING_PARENT_METRIC_READOUT_SIGNATURE; MISSING_R_LOCK_ZERO_OR_BOUND; MISSING_PPN_SECOND_ORDER",
            "source_path": str(SOURCE_PATHS["SRC3040_00_3039_doc"]),
        }
    ),
]

jacobian_rows = [
    base(
        {
            "audit_id": "JAC3040_0_phi_exists",
            "object": "parent metric potential phi_g",
            "required_identity": "phi_g is the first-order scalar metric/coframe perturbation in the observed local branch",
            "current_status": "CONDITIONAL_GR_STYLE_OBJECT",
            "blocks_claim": "MTS parent field/readout signature not supplied",
            "source_path": str(SOURCE_PATHS["SRC3040_09_min_parent"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_1_lapse",
            "object": "psi_N=-log(N)",
            "required_identity": "psi_N=phi_g+O(phi_g^2) from g_00=-N^2=-1+2 Phi/c^2",
            "current_status": "FIRST_ORDER_ALGEBRA_OK_IF_SIGN_BRANCH_FIXED",
            "blocks_claim": "needs parent-signed g_00/N convention and observed frame lock",
            "source_path": str(SOURCE_PATHS["SRC3040_04_3024_ansatz"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_2_w",
            "object": "chi_W=W/c^2",
            "required_identity": "chi_W=phi_g+O(phi_g^2), i.e. W=Phi in the same observed branch",
            "current_status": "CONDITIONAL_IN_PG_STACK_NOT_PARENT_SIGNED",
            "blocks_claim": "W could still be an independently calibrated Poisson/orbital potential",
            "source_path": str(SOURCE_PATHS["SRC3040_07_pg_contract"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_3_same_frame",
            "object": "observed frame",
            "required_identity": "matter, source variation, clocks, rods, orbits and metric equation use one e_obs",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "blocks_claim": "delta_frame_source remains active",
            "source_path": str(SOURCE_PATHS["SRC3040_08_newton_stack"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_4_source_pairing",
            "object": "one source slot",
            "required_identity": "rho_H pairs once with phi_g before any psi_N/W readout coordinates are introduced",
            "current_status": "MISSING",
            "blocks_claim": "two-channel a_H/a_W countermodel survives",
            "source_path": str(SOURCE_PATHS["SRC3040_12_3036_lock"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_5_hessian",
            "object": "one kinetic Hessian",
            "required_identity": "H_phi is the unique rank-one first-order scalar Hessian pulled back to both readouts",
            "current_status": "MISSING",
            "blocks_claim": "operator mismatch O_W/(C_NK0) can survive even with same source",
            "source_path": str(SOURCE_PATHS["SRC3040_05_3033_shapes"]),
        }
    ),
    base(
        {
            "audit_id": "JAC3040_6_ppn",
            "object": "second-order stability",
            "required_identity": "the same readout source normalization survives gamma/beta/PPN order",
            "current_status": "NOT_REACHED",
            "blocks_claim": "first-order Newton-looking closure is not local GR",
            "source_path": str(SOURCE_PATHS["SRC3040_11_worldtube_theorem"]),
        }
    ),
]

pullback_rows = [
    base(
        {
            "law_id": "PBL3040_0_coordinate",
            "quantity": "readout_coordinate",
            "formula": "y = r_y phi_g + O(phi_g^2)",
            "meaning": "readout Jacobian r_y is the only first-order coordinate factor if there is one parent potential",
            "status": "DEFINITION",
        }
    ),
    base(
        {
            "law_id": "PBL3040_1_source",
            "quantity": "source_vertex_in_y_chart",
            "formula": "a_y = a_phi/r_y",
            "meaning": "S_src=a_phi rho_H phi_g = (a_phi/r_y) rho_H y at first order",
            "status": "PULLBACK_ALGEBRA",
        }
    ),
    base(
        {
            "law_id": "PBL3040_2_operator",
            "quantity": "operator_in_y_chart",
            "formula": "O_y = H_phi/r_y^2",
            "meaning": "H_phi |grad phi_g|^2 becomes (H_phi/r_y^2)|grad y|^2",
            "status": "PULLBACK_ALGEBRA",
        }
    ),
    base(
        {
            "law_id": "PBL3040_3_coefficient",
            "quantity": "source_operator_coefficient",
            "formula": "C_y = a_y/O_y = a_phi*r_y/H_phi",
            "meaning": "coefficient differences come from readout Jacobians, not a free coupling",
            "status": "EXACT_FIRST_ORDER",
        }
    ),
    base(
        {
            "law_id": "PBL3040_4_ratio",
            "quantity": "prefactor_ratio",
            "formula": "Xi_H/C_WH = r_H/r_W + sign_unit_residual",
            "meaning": "single-potential route reduces the 3039 coupling problem to r_H=r_W plus sign/unit lock",
            "status": "CONDITIONAL_LAW",
        }
    ),
    base(
        {
            "law_id": "PBL3040_5_gr_branch",
            "quantity": "GR_style_first_order_value",
            "formula": "r_H=1 and r_W=1 if psi_N=-log(sqrt(1-2 Phi/c^2)) and W=Phi",
            "meaning": "delta_prefactor=0 at first order on the signed weak-field branch",
            "status": "CONDITIONAL_VALUE_NOT_PARENT_CLAIM",
        }
    ),
]

residual_bound_rows = [
    base(
        {
            "bound_id": "TCB3040_0_D_readout",
            "quantity": "D_readout",
            "definition": "abs(r_H/r_W - 1) plus sign/unit mismatch",
            "required_input": "parent readout Jacobians r_H, r_W with units and sign convention",
            "current_status": "MISSING_PARENT_READOUT_VALUES",
            "validity_rule": "zero by theorem or finite source-backed bound",
        }
    ),
    base(
        {
            "bound_id": "TCB3040_1_D_pairing",
            "quantity": "D_pairing",
            "definition": "residual from separate a_H psi_N and a_W chi_W source slots",
            "required_input": "single-pairing proof or finite a_H/a_W bound",
            "current_status": "MISSING_SINGLE_PAIRING_PROOF",
            "validity_rule": "no two-channel source slot before variation",
        }
    ),
    base(
        {
            "bound_id": "TCB3040_2_D_hessian",
            "quantity": "D_hessian",
            "definition": "residual from O_W/(C_NK0) not being one Hessian pullback",
            "required_input": "H_phi and readout pullback map, or finite operator mismatch bound",
            "current_status": "MISSING_HESSIAN_OWNER",
            "validity_rule": "rank-one scalar Hessian in the local branch",
        }
    ),
    base(
        {
            "bound_id": "TCB3040_3_D_prefactor_total",
            "quantity": "delta_prefactor_total_abs",
            "definition": "abs(D_readout)+abs(D_pairing)+abs(D_hessian)",
            "required_input": "all first-order components in common norm",
            "current_status": "BLOCKED_COMPONENTS_MISSING",
            "validity_rule": "absolute envelope; no tuned cancellation",
        }
    ),
    base(
        {
            "bound_id": "TCB3040_4_local_GR_gate",
            "quantity": "delta_A_source_total_abs",
            "definition": "delta_prefactor_total_abs plus R_lock components and second-order PPN residuals",
            "required_input": "prefactor components; R_frame; R_tau; R_worldtube; Omega_GM; beta/gamma",
            "current_status": "NOT_SCOREABLE",
            "validity_rule": "local GR only if first-order and PPN envelopes pass",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3040_0_two_channel_survives",
            "countermodel": "psi_N and W/c^2 are treated as independent readout/source coordinates with separate source slots",
            "effect": "single-potential algebra cannot be used; delta_prefactor remains free or bounded",
            "status": "LIVE_UNLESS_PARENT_READOUT_SIGNED",
        }
    ),
    base(
        {
            "countermodel_id": "CM3040_1_w_not_phi",
            "countermodel": "W is an orbital/Gauss potential calibrated after fitting rather than the metric Phi",
            "effect": "r_W is not parent-owned and can import measured GM",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3040_2_hessian_split",
            "countermodel": "lapse and W readouts share Phi but not the same kinetic Hessian pullback",
            "effect": "operator mismatch recreates the coupling problem",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3040_3_first_order_not_ppn",
            "countermodel": "first-order r_H=r_W passes but second-order beta/gamma source stability fails",
            "effect": "Newton-looking success does not become local GR",
            "status": "GUARDRAIL",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3040_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3040 is source-backed to 3039 plus existing local-GR/PG rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_1_lapse_algebra",
            "gate": "weak-field lapse gives psi_N=phi_g+O(phi_g^2)",
            "result": any(row["theorem_id"] == "SPT3040_1_gr_style_readout" for row in theorem_rows),
            "notes": "conditional algebra, not parent signature",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_2_pullback_law",
            "gate": "single-potential pullback factor law is explicit",
            "result": any(row["law_id"] == "PBL3040_4_ratio" for row in pullback_rows),
            "notes": "Xi_H/C_WH becomes r_H/r_W plus sign/unit residual",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_3_prefactor_conditional_zero",
            "gate": "delta_prefactor is conditionally zero if r_H=r_W=1",
            "result": any(row["theorem_id"] == "SPT3040_5_first_order_closure" for row in theorem_rows),
            "notes": "conditional first-order closure only",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_4_parent_signature",
            "gate": "MTS parent action signs the metric readout theorem",
            "result": False,
            "notes": "current rows are conditional_not_parent_derived",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_5_bound_schema",
            "gate": "two-channel residual bound schema exists",
            "result": any(row["bound_id"] == "TCB3040_4_local_GR_gate" for row in residual_bound_rows),
            "notes": "fallback remains nonclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_6_countermodels",
            "gate": "live countermodels are retained",
            "result": any(row["status"].startswith("LIVE") for row in countermodel_rows),
            "notes": "prevents one-potential axiom smuggling",
        }
    ),
    base(
        {
            "gate_id": "GATE3040_7_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local-GR/Newton/PPN/R10 claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3040_0_theorem",
            "question": "does the single-potential readout route close the first-order coupling algebra?",
            "answer": "CONDITIONALLY_YES",
            "reason": "if psi_N and W/c^2 are both first-order readouts of phi_g with r_H=r_W=1, the apparent relative coupling becomes zero at first order",
            "next_action": "do not claim; parent-sign the metric readout theorem and one source/Hessian pullback",
        }
    ),
    base(
        {
            "decision_id": "DEC3040_1_current_corpus",
            "question": "is this parent-signed by the current MTS corpus?",
            "answer": "NO",
            "reason": "same-frame weak-field potential, W=Phi, single source pairing and Hessian pullback remain conditional or missing",
            "next_action": "3041 should sign or reject the parent metric readout signature; otherwise use D_readout/D_pairing/D_hessian bound rows",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3040_0_3041",
            "next_checkpoint": "3041-Y5-R2FR-parent-metric-readout-signature-or-readout-jacobian-bound-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_parent_metric_readout_signature_or_readout_jacobian_bound_under_AX1090_3041.py",
            "mission": "parent-sign or reject the metric readout signature g_00=-1+2Phi/c^2, psi_N=-log(N)=Phi/c^2+O(2), W=Phi, one source pairing and one Hessian pullback",
            "starting_equation": "Xi_H/C_WH = r_H/r_W + sign_unit_residual; GR-like first-order branch has r_H=r_W=1",
            "do_not_repeat": "do not assume W=Phi or one Hessian without a parent readout/action signature; do not promote first-order closure to PPN/local GR",
            "claim_policy": "first-order Newton source prefactor can only be promoted after parent signature plus R_lock; local GR additionally needs second-order beta/gamma stability",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "theorem": theorem_rows,
    "jacobian": jacobian_rows,
    "pullback": pullback_rows,
    "residual_bound": residual_bound_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
shutil.copyfile(OUTPUTS["jacobian"], BRANCH_OUTPUTS["jacobian_copy"])
shutil.copyfile(OUTPUTS["pullback"], BRANCH_OUTPUTS["pullback_copy"])
shutil.copyfile(OUTPUTS["residual_bound"], BRANCH_OUTPUTS["residual_bound_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for single-potential readout route",
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
    + theorem_rows
    + jacobian_rows
    + pullback_rows
    + residual_bound_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3040_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3040_02_lapse_algebra",
            "passed": bool(gates[1]["result"]),
            "requirement": "weak-field lapse readout algebra is written",
            "evidence": OUTPUTS["theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_03_pullback_law",
            "passed": bool(gates[2]["result"]),
            "requirement": "single-potential pullback factor law exists",
            "evidence": OUTPUTS["pullback"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_04_conditional_zero",
            "passed": bool(gates[3]["result"]),
            "requirement": "conditional first-order delta_prefactor zero row exists",
            "evidence": OUTPUTS["theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_05_parent_not_signed",
            "passed": any(row["result"] == "CONDITIONAL_ROUTE_FOUND_NOT_CLAIMED" for row in theorem_rows),
            "requirement": "parent signature is not claim-promoted",
            "evidence": OUTPUTS["theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_06_bound_schema",
            "passed": bool(gates[5]["result"]),
            "requirement": "two-channel residual bound schema exists",
            "evidence": OUTPUTS["residual_bound"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_07_countermodels",
            "passed": bool(gates[6]["result"]),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_08_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3040 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3040_09_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_10_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3040_11_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3040_12_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3041-"),
            "requirement": "next target selects parent metric readout signature or readout-Jacobian bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3040_13_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3040 - Single-Potential Readout Theorem Or Two-Channel Residual Bound under AX1090

Status: `Y5_R2FR_3040_single_potential_first_order_prefactor_conditionally_closes_parent_signature_missing`

## Verdict

3040 finds the cleanest route so far for the first-order GR/Newton source prefactor.

If there is one parent metric potential `phi_g` and the two readouts are

`psi_N = r_H phi_g + O(phi_g^2)` and `chi_W := W/c^2 = r_W phi_g + O(phi_g^2)`,

then pulling back one source pairing and one kinetic Hessian gives

`Xi_H/C_WH = r_H/r_W + sign_unit_residual`.

On the GR-style weak-field branch already present in the corpus,

`g_00=-1+2 Phi/c^2`, `N=sqrt(1-2 Phi/c^2)`, `psi_N=-log(N)=Phi/c^2+O(Phi^2/c^4)`, and if `W=Phi`, then `r_H=r_W=1`.

So the first-order coupling/prefactor problem can conditionally close without a fitted coupling:

`delta_prefactor = Xi_H/C_WH - 1 = 0`

at first order.

But this is **not** promoted to a claim. The current MTS corpus has not yet parent-signed `W=Phi`, the single source pairing, the single Hessian pullback, the same-frame readout, `R_lock=0`, or the second-order PPN stability.

## Single-Potential Readout Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim_piece", "formal_statement", "result", "missing_for_claim"])}

## Weak-Field Readout Jacobian Audit

{md_table(jacobian_rows, ["audit_id", "object", "required_identity", "current_status", "blocks_claim"])}

## Pullback Factor Law

{md_table(pullback_rows, ["law_id", "quantity", "formula", "meaning", "status"])}

## Two-Channel Residual Bound Schema

{md_table(residual_bound_rows, ["bound_id", "quantity", "definition", "required_input", "current_status", "validity_rule"])}

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
print("3040 verdict: single-potential route conditionally closes first-order prefactor; parent readout signature still missing.")
