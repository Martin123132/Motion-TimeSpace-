from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2970"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2970-Y5-R2FR-parent-quotient-map-and-basic-matter-action-signature-or-DqZ-JA-coefficient-row-under-AX1090.md"

SRC_2969_DOC = ROOT / "2969-Y5-R2FR-DqZ-and-JA-source-current-descent-proof-or-residual-bound-row-under-AX1090.md"
SRC_2969_NEXT = RESIDUALS / "P8_Y5_R2FR_2969_NEXT_TARGET.csv"
SRC_2969_THEOREM = RESIDUALS / "P8_Y5_R2FR_2969_COMBINED_DESCENT_THEOREM_LEDGER.csv"
SRC_2969_DQZ = RESIDUALS / "P8_Y5_R2FR_2969_DQZ_CLAUSE_AUDIT.csv"
SRC_2969_JA = RESIDUALS / "P8_Y5_R2FR_2969_JA_SOURCE_CURRENT_AUDIT.csv"
SRC_2969_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2969_DQZ_JA_RESIDUAL_BOUND_ROWS_NONCLAIM.csv"
SRC_2969_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2969_VALIDATION.csv"

SRC_2911_QMAP = PARENT_ACTION / "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv"
SRC_2913_AUX = PARENT_ACTION / "Parent_auxiliary_constraint_origin_2913_NONCLAIM.csv"
SRC_2912_CONSTRAINT = PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv"
SRC_2956_DESCENT = PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv"
SRC_2957_NOHOM = PARENT_ACTION / "no_hidden_visible_hom_gate_2957_NOT_DERIVED.csv"
SRC_2952_NOPOLE = PARENT_ACTION / "no_pole_quotient_audit_2952_NOT_DERIVED.csv"
SRC_2926_AX = PARENT_ACTION / "AX1090_parent_object_no_hidden_visible_audit_2926_NONCLAIM.csv"
SRC_2710_OWNER = SOURCE_WEIGHT / "AX1090_0_PARENT_OBJECT_OWNER_GATE_2710_NONCLAIM.csv"
SRC_2711_CLOSURE = SOURCE_WEIGHT / "AX1090_PARENT_OBJECT_EXPLICIT_CLOSURE_2711_NONCLAIM.csv"
SRC_2829_QBASIC = SOURCE_WEIGHT / "qbasic_no_source_prefactor_theorem_audit_2829_NONCLAIM.csv"
SRC_2885_DQZ = SOURCE_WEIGHT / "RAB_DQZ_ZERO_OR_FACTOR_BLOCKER_LEDGER_2885_NONCLAIM.csv"
SRC_2886_REQ = SOURCE_WEIGHT / "RAB_DQZ_COMPONENT_INPUT_REQUIREMENTS_2886_NONCLAIM.csv"
SRC_2887_COBS = SOURCE_WEIGHT / "RAB_COBS_OPERATOR_NORM_ROW_2887_NONCLAIM.csv"
SRC_2888_CSHADOW = SOURCE_WEIGHT / "RAB_CSHADOW_BOUND_ROW_2888_NONCLAIM.csv"
SRC_2892_NEUTRAL = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_2893_NO_SOURCE = SOURCE_WEIGHT / "RAB_BETA_SOURCE_NO_SOURCE_SLOT_UPDATE_2893_NONCLAIM.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2970_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
    "qmap": RESIDUALS / "P8_Y5_R2FR_2970_QMAP_KERNEL_AUDIT.csv",
    "matter": RESIDUALS / "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_2970_FIRST_LEAKAGE_COEFFICIENT_ROWS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2970_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2970_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2970_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2970_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2970_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_copy": PARENT_ACTION / "parent_quotient_basic_matter_signature_attempt_2970_NOT_DERIVED.csv",
    "coefficient_copy": LOCAL_BOUNDS / "DqZ_JA_first_leakage_coefficients_2970_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2970_first_leakage_coefficient_acquisition_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2970_00_2969_doc", SRC_2969_DOC, "NEXT2969_0_2970;theorem shape", "2969 handoff"),
        ("SRC2970_01_2969_next", SRC_2969_NEXT, "NEXT2969_0_2970", "machine-readable 2970 target"),
        ("SRC2970_02_2969_theorem", SRC_2969_THEOREM, "THM2969_0_combined_descent;THM2969_3_current_application", "combined descent theorem status"),
        ("SRC2970_03_2969_dqz", SRC_2969_DQZ, "DQZ2969_0_parent_q;DQZ2969_6_verdict", "Dq_Z clause audit"),
        ("SRC2970_04_2969_ja", SRC_2969_JA, "JA2969_0_quotient_action;JA2969_7_verdict", "J_A clause audit"),
        ("SRC2970_05_2969_bounds", SRC_2969_BOUNDS, "BND2969_0_DqZ_norm;BND2969_3_current_owner_countermodels", "Dq_Z/J_A bound interface"),
        ("SRC2970_06_2969_validation", SRC_2969_VALIDATION, "VAL2969_OVERALL", "2969 validation"),
        ("SRC2970_07_2911_qmap", SRC_2911_QMAP, "QMAP2911_0_projection_form;QMAP2911_7_verdict", "q-map and kernel attempt"),
        ("SRC2970_08_2913_aux", SRC_2913_AUX, "PAO2913_0_parent_sort;PAO2913_6_verdict", "auxiliary constraint origin"),
        ("SRC2970_09_2912_constraint", SRC_2912_CONSTRAINT, "CFP2912_0_exact_conditional;CFP2912_5_current_verdict", "constraint-first theorem"),
        ("SRC2970_10_2956_descent", SRC_2956_DESCENT, "DESC2956_0_chain_rule;DESC2956_7_verdict", "matter pullback descent"),
        ("SRC2970_11_2957_nohom", SRC_2957_NOHOM, "HOM2957_0_theorem_target;HOM2957_7_verdict", "no-hidden-visible-hom"),
        ("SRC2970_12_2952_nopole", SRC_2952_NOPOLE, "QNP2952_1_parent_q_object;QNP2952_6_matter_descent", "no-pole quotient audit"),
        ("SRC2970_13_2926_ax", SRC_2926_AX, "AX2926_0_parent_object;AX2926_5_total_verdict", "AX1090 parent object audit"),
        ("SRC2970_14_2710_owner", SRC_2710_OWNER, "AUD2710_0_parent_object;AUD2710_6_verdict", "parent object owner gate"),
        ("SRC2970_15_2711_closure", SRC_2711_CLOSURE, "AX1090_0_LC;AX1090_0_LC_6", "explicit closure guardrail"),
        ("SRC2970_16_2829_qbasic", SRC_2829_QBASIC, "THA2829_0_exact_Dq_gate;THA2829_7_current_verdict", "q-basic/no-source-prefactor audit"),
        ("SRC2970_17_2885_dqz", SRC_2885_DQZ, "DQZF2885_0_Dq_Z_norm;DQZF2885_3_direct_tail_sum", "DqZ finite factor blockers"),
        ("SRC2970_18_2886_req", SRC_2886_REQ, "REQ2886_2_DqZ;REQ2886_5_direct_tails", "DqZ component requirements"),
        ("SRC2970_19_2887_cobs", SRC_2887_COBS, "COBS2887_0_operator_norm;COBS2887_2_shadow_frame_guard", "C_Obs operator rows"),
        ("SRC2970_20_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_0_C_shadow_abs;CSH2888_1_b_R_common_weyl", "shadow coefficient rows"),
        ("SRC2970_21_2892_neutral", SRC_2892_NEUTRAL, "PAS2892_1_quotient_action;PAS2892_5_result", "quotient-invariant matter action"),
        ("SRC2970_22_2893_no_source", SRC_2893_NO_SOURCE, "BZ2893_3_no_source_only_slot;BZ2893_6_verdict", "no source-only slot update"),
        ("SRC2970_23_2676_owner", SRC_2676_OWNER, "OWN2676_2_hilbert_current_sublemma;OWN2676_4_verdict", "action/current owner"),
        ("SRC2970_24_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_3_species_blind_measure;GRM2677_6_verdict", "species-blind grammar"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def signature_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIG2970_0_parent_object", "AX1090 parent action object", "one parent action object owns q, matter, source, boundary and variation order", "SCHEMA_AVAILABLE_NOT_DERIVED", "AX1090_0 remains missing, not adopted as an axiom", SRC_2926_AX),
        ("SIG2970_1_q_object", "q: Conf_parent -> Q_obs/Q_vis", "canonical domain-scoped quotient map before matter/readout", "BLOCKED_Q_OBJECT_NOT_PARENT_SIGNED", "current q projection is formal unless the parent chart and domain are independent", SRC_2952_NOPOLE),
        ("SIG2970_2_vertical_kernel", "v_Z in ker(Dq)", "selected Z generator lies in Dq kernel on an open branch", "BLOCKED_OPEN_BRANCH_KERNEL_NOT_SIGNED", "pointwise or post-hoc verticality is refused", SRC_2952_NOPOLE),
        ("SIG2970_3_auxiliary_constraint", "S_Z auxiliary block", "Z/Lambda compatibility pair is in S_parent before q/readout", "PARENT_AUXILIARY_ORIGIN_NOT_DERIVED", "parent action image, units/rank and forcing silence are missing", SRC_2913_AUX),
        ("SIG2970_4_Qvis_constructor", "Q_vis constructor", "q|C_Z=qbar(Q_vis) contains no hidden representative labels", "MISSING_FACTORISATION_CERTIFICATE", "Q_vis constructor and no-hidden-visible-hom remain unsigned", SRC_2911_QMAP),
        ("SIG2970_5_theta_dmu_basic", "theta/dmu basicness", "coframe, measure and connection factor through q or fixed parent constants", "UNSIGNED_GEOMETRY_FUNCTOR_EXTENSION", "coframe/measure owner and no-shadow stack remain missing", SRC_2952_NOPOLE),
        ("SIG2970_6_basic_matter_action", "q-basic ordinary matter action", "S_matter=Sbar[q(Phi),Psi,theta(q)] with no direct Z argument", "EXACT_CONDITIONAL_SCHEMA_NOT_PARENT_SIGNED", "action-domain/no-shadow exclusion remains unsigned", SRC_2892_NEUTRAL),
        ("SIG2970_7_no_source_slot", "no direct Z/source prefactor", "ordinary matter grammar forbids w_A(Z)S_A, J_Z Z and source-only kappa_A(Z)T_A slots", "UNSIGNED", "no-source-only slot is still a contract, not a parent theorem", SRC_2893_NO_SOURCE),
        ("SIG2970_8_verdict", "2970 parent signature", "all parent quotient/basic-matter signature clauses close in one branch", "NOT_DERIVED_COEFFICIENT_ROWS_REQUIRED", "the route remains conditional; first leakage coefficients are staged", SRC_2969_NEXT),
    ]
    return [
        add_common(
            {
                "signature_id": signature_id,
                "object": obj,
                "required_statement": required,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "fallback_coefficient_required": True,
            }
        )
        for signature_id, obj, required, status, blocker, path in rows
    ]


def qmap_rows() -> list[dict[str, Any]]:
    rows = [
        ("QMAP2970_0_projection", "q(Phi)=Q_vis", "FORMAL_PROJECTION_AVAILABLE_NOT_PROOF", "epsilon_q_parent", "projection declaration does not by itself prove parent ownership", SRC_2911_QMAP),
        ("QMAP2970_1_geometry", "Dq[Z] on e_obs/g_obs/omega/dmu", "CONDITIONAL_ZERO_NOT_ADOPTED", "epsilon_geometry_basic", "observed coframe, no-shadow and q/Z norms are unsigned", SRC_2911_QMAP),
        ("QMAP2970_2_source", "Dq[Z] on source current/normalization", "NOT_ZERO_ON_CURRENT_EVIDENCE", "epsilon_source_basic", "J_H owner, worldtube, no-source-slot and Pi_M equality are unsigned", SRC_2911_QMAP),
        ("QMAP2970_3_readout", "Dq[Z] on clocks/EM/PPN/orbits", "CONDITIONAL_ZERO_NOT_ADOPTED", "epsilon_readout_basic", "marker and radiative/readout re-entry remain open", SRC_2911_QMAP),
        ("QMAP2970_4_boundary_projector", "Dq[Z] on boundary/projector/support", "NOT_ZERO_OR_UNPROVED", "epsilon_boundary_projector", "boundary/corner/projector and source support are independent channels", SRC_2911_QMAP),
        ("QMAP2970_5_norm", "Dq_Z_norm", "MISSING_NUMERIC_OR_THEOREM_ZERO", "eps_q_parent", "q/Z norms and Dq matrix are missing", SRC_2885_DQZ),
        ("QMAP2970_6_verdict", "Dq[v_Z]=0 current branch", "NOT_PARENT_SIGNED_FINITE_DQZ_REQUIRED", "Dq_Z_norm_total", "field chart, q map, Z basis, source/readout descent and boundary do not close together", SRC_2911_QMAP),
    ]
    return [
        add_common(
            {
                "qmap_id": qmap_id,
                "component": component,
                "current_status": status,
                "fallback_coefficient": coeff,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "finite_value_present": False,
            }
        )
        for qmap_id, component, status, coeff, blocker, path in rows
    ]


def matter_rows() -> list[dict[str, Any]]:
    rows = [
        ("MAT2970_0_chain_rule", "matter pullback chain rule", "delta_v S_matter=0 if Dq[v]=0 and matter descends", "CONDITIONAL_THEOREM_VALID", "chain rule is not the same as parent signature", SRC_2956_DESCENT),
        ("MAT2970_1_functor_domain", "ordinary matter functor domain", "ordinary matter depends only on observed geometry, fields and fixed representation data", "EXACT_CONTRACT_NOT_PARENT_SIGNED", "direct source/worldtube vertices remain legal", SRC_2956_DESCENT),
        ("MAT2970_2_no_hidden_visible_hom", "no hidden visible coefficient map", "visible coefficients are q-pulled back or fixed data", "NO_HIDDEN_VISIBLE_HOM_NOT_DERIVED", "domain signatures are not parent-owned", SRC_2957_NOHOM),
        ("MAT2970_3_no_source_prefactor", "no source-only prefactor", "ordinary matter excludes source-only w_A(Z) or kappa_A(Z) slots", "NOT_DERIVED", "object-language admissibility and readout stability remain unsigned", SRC_2829_QBASIC),
        ("MAT2970_4_Hilbert_current", "Hilbert current owner", "fixed common action varied before readout gives unique Hilbert source", "EXACT_SUBTHEOREM_CONDITIONAL", "common S_matter and variation-before-readout are not parent-signed", SRC_2676_OWNER),
        ("MAT2970_5_species_measure", "species-blind measure", "parent measure is not product_A J_A Dpsi_A", "CONTRACT_TARGET_NOT_SIGNED", "species measure Jacobians and action weights survive as countermodels", SRC_2677_GRAMMAR),
        ("MAT2970_6_no_spurion_return", "source label forgetting", "source/readout functor cannot reintroduce a spurion after quotienting", "UNSIGNED_DEPENDENCY", "post-graph source labels remain open", SRC_2677_GRAMMAR),
        ("MAT2970_7_verdict", "q-basic matter action current claim", "ordinary matter action is parent-signed q-basic and source-slot free", "NOT_DERIVED_J_DIRECT_J_SPURION_ROWS_REQUIRED", "matter action descent, no-source slot and current-owner clauses do not close", SRC_2969_JA),
    ]
    return [
        add_common(
            {
                "matter_id": matter_id,
                "object": obj,
                "required_statement": required,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "fallback_coefficient_required": True,
            }
        )
        for matter_id, obj, required, status, blocker, path in rows
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        ("COEF2970_0_eps_q_parent", "eps_q_parent", "failure of parent-owned q declaration before matter/readout", "dimensionless", "Dq_Z_norm <= eps_q_parent + eps_constraint + eps_factorization", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2911_QMAP),
        ("COEF2970_1_eps_constraint", "eps_constraint", "failure of constraint-first Z elimination/tangent proof", "dimensionless", "Dq_Z_norm <= eps_q_parent + eps_constraint + eps_factorization", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2913_AUX),
        ("COEF2970_2_eps_factorization", "eps_factorization", "failure of q|C_Z=qbar(Q_vis) and Q_vis constructor", "dimensionless", "Dq_Z_norm <= eps_q_parent + eps_constraint + eps_factorization", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2911_QMAP),
        ("COEF2970_3_eps_theta_basic", "eps_theta_basic", "failure of theta/coframe/measure basicness under v_Z", "dimensionless_or_geometry_norm", "J_A_bulk <= C_theta eps_theta_basic + ...", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2886_REQ),
        ("COEF2970_4_J_direct", "J_direct", "direct Z/source vertex in ordinary matter action", "action_derivative_or_source_normalized", "J_A_bulk <= C_matter Dq_Z_norm + |J_direct| + |J_spurion| + |J_nonH|", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2892_NEUTRAL),
        ("COEF2970_5_J_spurion", "J_spurion", "source-only species/marker prefactor or post-quotient spurion", "source_normalized", "J_A_countermodel_tail <= K_spurion |J_spurion| + ...", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2677_GRAMMAR),
        ("COEF2970_6_J_nonH", "J_nonH", "non-Hilbert current bypass not owned by common matter action", "source_normalized", "J_A_countermodel_tail <= K_nonH |J_nonH| + ...", "MISSING_SOURCE_BACKED_UPPER_BOUND", SRC_2676_OWNER),
        ("COEF2970_7_C_Obs_e", "C_Obs_e", "observed coframe/readout operator norm", "dimensionless", "DqZ_readout <= C_Obs_e Dq_Z_norm + C_shadow_abs", "MISSING_NUMERIC_OR_THEOREM_ZERO", SRC_2887_COBS),
        ("COEF2970_8_C_shadow_abs", "C_shadow_abs", "representative Weyl/disformal/source/readout shadow envelope", "dimensionless", "DqZ_readout <= C_Obs_e Dq_Z_norm + C_shadow_abs", "MISSING_NUMERIC_OR_THEOREM_ZERO", SRC_2888_CSHADOW),
        ("COEF2970_9_total", "DqZ_JA_first_leakage_total", "absolute no-cancellation envelope for first Dq_Z/J_A leakage heads", "mixed_declared_by_projection", "total <= sum absolute heads; no cancellations, no fitted baseline absorption", "COEFFICIENT_ACQUISITION_REQUIRED", SRC_2969_BOUNDS),
    ]
    return [
        add_common(
            {
                "coefficient_id": coeff_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "bound_interface": formula,
                "candidate_value": candidate,
                "lower_bound": 0 if symbol != "DqZ_JA_first_leakage_total" else "nonnegative_envelope",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for coeff_id, symbol, definition, units, formula, candidate, path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2970_0_parent_object", "AX1090 parent object signed", False, "PARENT_OBJECT_NOT_DERIVED"),
        ("CG2970_1_qmap", "q and v_Z in ker(Dq) parent-signed", False, "QMAP_KERNEL_NOT_SIGNED"),
        ("CG2970_2_constraint", "constraint-first elimination parent-owned", False, "AUXILIARY_ORIGIN_NOT_DERIVED"),
        ("CG2970_3_matter", "q-basic matter action parent-signed", False, "MATTER_ACTION_NOT_PARENT_SIGNED"),
        ("CG2970_4_no_source_slot", "direct source/spurion slots excluded", False, "SOURCE_SLOT_COUNTERMODELS_SURVIVE"),
        ("CG2970_5_coefficients", "first leakage coefficients source-backed finite", False, "COEFFICIENT_VALUES_MISSING"),
        ("CG2970_6_local_GR", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2970_0_signature", "parent quotient/basic-matter signature not acquired", "every source gives conditional shape but refuses parent signature", "do not adopt Dq_Z=0 or J_A=0"),
        ("DEC2970_1_coefficients", "first leakage coefficient rows staged", "the honest fallback is finite eps/J rows, not another closure pass", "acquire eps_q_parent, eps_constraint, J_direct and J_spurion next"),
        ("DEC2970_2_route", "derivation route remains alive", "the failure is not algebraic contradiction; it is missing parent object-language signature", "keep using no-cancellation residual ledgers"),
        ("DEC2970_3_claims", "no local-GR, R10, PPN, clock, WEP or orbital claim", "all new coefficient rows have missing upper bounds and valid_for_claim=false", "private checkpoint only"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2970_0_2971",
                "priority": "selected_primary",
                "next_doc": "2971-Y5-R2FR-first-DqZ-JA-leakage-coefficient-acquisition-or-theorem-zero-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_first_DqZ_JA_leakage_coefficient_acquisition_or_theorem_zero_under_AX1090_2971.py",
                "objective": "Try to source or theorem-zero the first leakage coefficients eps_q_parent, eps_constraint, eps_factorization, J_direct and J_spurion; if not, split each into smaller source-ready subcoefficients.",
                "include": "eps_q_parent;eps_constraint;eps_factorization;eps_theta_basic;J_direct;J_spurion;J_nonH;C_Obs_e;C_shadow_abs;source-backed upper bounds;no-cancellation envelope",
                "exclude": "boundary no-flux proof;CDB closure;M_AB signature proof;arena scoring;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("signature_copy", OUTPUTS["signature"], BRANCH_OUTPUTS["signature_copy"]),
        ("coefficient_copy", OUTPUTS["coefficients"], BRANCH_OUTPUTS["coefficient_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2970_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2970_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2970_2_signature_not_signed", any(row["signature_id"] == "SIG2970_8_verdict" and row["current_status"] == "NOT_DERIVED_COEFFICIENT_ROWS_REQUIRED" for row in all_rows["signature"]), "parent signature not acquired and coefficients required", True),
        ("VAL2970_3_qmap_not_signed", any(row["qmap_id"] == "QMAP2970_6_verdict" and row["current_status"] == "NOT_PARENT_SIGNED_FINITE_DQZ_REQUIRED" for row in all_rows["qmap"]), "qmap kernel not signed and DqZ finite row required", True),
        ("VAL2970_4_matter_not_signed", any(row["matter_id"] == "MAT2970_7_verdict" and row["current_status"] == "NOT_DERIVED_J_DIRECT_J_SPURION_ROWS_REQUIRED" for row in all_rows["matter"]), "basic matter action not signed and J rows required", True),
        ("VAL2970_5_required_coefficients_present", {"eps_q_parent", "eps_constraint", "J_direct", "J_spurion"}.issubset({row["symbol"] for row in all_rows["coefficients"]}), "requested first coefficients are present", True),
        ("VAL2970_6_coefficients_nonclaim", all(row["finite_value_present"] is False and row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["coefficients"]), "coefficient rows remain nonclaim and not score-ready", True),
        ("VAL2970_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2970_8_next_target_written", any(row["next_id"] == "NEXT2970_0_2971" for row in all_rows["next"]), "2971 coefficient acquisition next target selected", True),
        ("VAL2970_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2970_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2970_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2970_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2970 outputs were written to formalization-workbench", True),
        ("VAL2970_13_doc_written", DOC.exists(), "2970 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2970_OVERALL", "passed": overall, "check": "2970 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2970 - Y5 R2FR: parent quotient map and basic matter action signature or DqZ/JA coefficient row under AX1090

Status: `Y5_R2FR_2970_parent_signature_not_acquired_first_DqZ_JA_leakage_coefficients_staged_nonclaim`

Claim ceiling: `no_DqZ_zero_no_JA_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

2970 tested whether the parent quotient map and q-basic matter action can be signed instead of merely assumed.

- Result: the signature route remains mathematically sharp but not parent-derived in the current corpus.
- The failed clauses are concrete: parent object, q object, open-branch `v_Z in ker(Dq)`, auxiliary constraint origin, `Q_vis` factorization, q-basic geometry, q-basic ordinary matter and no source-only slot.
- Fallback now exists as first leakage coefficient rows: `eps_q_parent`, `eps_constraint`, `eps_factorization`, `J_direct`, `J_spurion`, plus required shadow/current tails.
- This is progress toward derivable local GR because the missing parent signature is now converted into bounded source-ready heads instead of another closure axiom.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Parent Signature Gate

{md_table(all_rows["signature"], ["signature_id", "object", "current_status", "blocking_gap", "parent_signed", "fallback_coefficient_required"])}

## Q-Map Kernel Audit

{md_table(all_rows["qmap"], ["qmap_id", "component", "current_status", "fallback_coefficient", "blocking_gap"])}

## Basic Matter Action Audit

{md_table(all_rows["matter"], ["matter_id", "object", "current_status", "blocking_gap", "fallback_coefficient_required"])}

## First Leakage Coefficient Rows

{md_table(all_rows["coefficients"], ["coefficient_id", "symbol", "definition", "bound_interface", "candidate_value", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "signature": signature_rows(),
        "qmap": qmap_rows(),
        "matter": matter_rows(),
        "coefficients": coefficient_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2970 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
