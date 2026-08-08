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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2930"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2930-Y5-R2FR-source-owner-Hcore-to-beta-denominator-binding-or-finite-local-residual-first-value-under-AX1090.md"

SRC_2929_DOC = ROOT / "2929-Y5-R2FR-beta-source-normalization-square-law-or-finite-source-residual-under-AX1090.md"
SRC_2929_NEXT = RESIDUALS / "P8_Y5_R2FR_2929_NEXT_TARGET.csv"
SRC_2929_BETA = RESIDUALS / "P8_Y5_R2FR_2929_BETA_FINITE_RESIDUAL_VECTOR.csv"
SRC_2929_NEWTON = RESIDUALS / "P8_Y5_R2FR_2929_NEWTON_GAUSS_ORBITAL_HANDOFF.csv"
SRC_2929_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2929_VALIDATION.csv"

SRC_2921_SCORECARD = RESIDUALS / "P8_Y5_R2FR_2921_SOURCE_NORMALIZED_NEWTON_SCORECARD_ROWS.csv"
SRC_2921_IDENTITY = RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv"
SRC_2922_OWNER = RESIDUALS / "P8_Y5_R2FR_2922_HAMILTONIAN_SECTOR_OWNER_AUDIT.csv"
SRC_2922_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_SCHEMA.csv"
SRC_2923_HCORE = RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv"
SRC_2923_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2923_SOURCE_MASS_ROW_TEMPLATE.csv"
SRC_2924_EH = RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv"
SRC_2924_GPB = RESIDUALS / "P8_Y5_R2FR_2924_GAUSS_POISSON_BRIDGE_CHECK.csv"
SRC_2924_ATTEMPT = RESIDUALS / "P8_Y5_R2FR_2924_SOURCE_MASS_FIRST_ROW_ATTEMPT.csv"
SRC_2924_REDUCTION = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2925_VECTOR = RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv"
SRC_2928_BETA = RESIDUALS / "P8_Y5_R2FR_2928_BETA_SOURCE_NORMALIZATION_HANDOFF.csv"
SRC_2928_COUPLING = RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv"
SRC_2578_GATE = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv"
SRC_2578_LEDGER = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2930_DENOMINATOR_BINDING_CONTRACT.csv",
    "ledger": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_2930_FIRST_VALUE_ACQUISITION_QUEUE.csv",
    "impact": RESIDUALS / "P8_Y5_R2FR_2930_LOCAL_GR_REDUCTION_IMPACT.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2930_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2930_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2930_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2930_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2930_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": PARENT_ACTION / "Source_owner_Hcore_beta_denominator_contract_2930_NONCLAIM.csv",
    "queue_copy": LOCAL_BOUNDS / "Finite_local_residual_first_value_queue_2930_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2930_PARENT_SOURCE_COEFFICIENT_OR_FIRST_VALUE_NEXT_NONCLAIM.csv",
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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


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
        ("SRC2930_00_2929_doc", SRC_2929_DOC, "NEXT2929_0_2930;source ownership;Validation overall: `True`", "2929 selected source-owner/Hcore denominator binding"),
        ("SRC2930_01_2929_next", SRC_2929_NEXT, "NEXT2929_0_2930;A_source;B_source;kappa_MTS;ell_J", "machine-readable 2930 target"),
        ("SRC2930_02_2929_beta", SRC_2929_BETA, "BFR2929_0_delta_beta_source;BFR2929_5_epsilon_SN;BFR2929_6_Delta_beta_total_abs", "active beta residual vector"),
        ("SRC2930_03_2929_newton", SRC_2929_NEWTON, "NGH2929_1_source_owner_gap;NGH2929_2_hcore_gap;NGH2929_4_next_forward_move", "source-owner/Hcore handoff"),
        ("SRC2930_04_2929_validation", SRC_2929_VALIDATION, "VAL2929_OVERALL;True", "2929 validation summary"),
        ("SRC2930_05_2921_identity", SRC_2921_IDENTITY, "PSM2921_0_target_identity;PSM2921_10_verdict", "source-mass identity audit"),
        ("SRC2930_06_2921_scorecard", SRC_2921_SCORECARD, "SN2921_0_dln_Geff_dt;SN2921_7_delta_beta_source;SN2921_9_total_guard", "source-normalized Newton residual scorecard"),
        ("SRC2930_07_2922_owner", SRC_2922_OWNER, "HOA2922_0_target;HOA2922_6_MHref_positive;HOA2922_10_verdict", "Hamiltonian sector-owner audit"),
        ("SRC2930_08_2922_schema", SRC_2922_SCHEMA, "SMR2922_0_identity;SMR2922_3_MHref;SMR2922_8_qRhat", "source-mass first-row schema"),
        ("SRC2930_09_2923_hcore", SRC_2923_HCORE, "HC2923_0_parent_action_block;HC2923_5_MHref_denominator;HC2923_10_total_guard", "Hcore/Q_tau coefficient checklist"),
        ("SRC2930_10_2923_template", SRC_2923_TEMPLATE, "SMT2923_0_parent_source_mass_theorem;SMT2923_1_parent_coefficient_map;SMT2923_7_total_guard", "source-mass row template"),
        ("SRC2930_11_2924_eh", SRC_2924_EH, "EHA2924_0_EH_action_block;EHA2924_4_EH_weak_field;EHA2924_5_total_verdict", "EH anchor coefficient map"),
        ("SRC2930_12_2924_gpb", SRC_2924_GPB, "GPB2924_0_EH_field_equation;GPB2924_4_MTS_verdict", "Gauss/Poisson bridge check"),
        ("SRC2930_13_2924_attempt", SRC_2924_ATTEMPT, "SMFA2924_0_EH_ADM_reference_row;SMFA2924_1_MTS_reduced_EH_source_row", "source-mass first row attempt"),
        ("SRC2930_14_2924_reduction", SRC_2924_REDUCTION, "RED2924_0_metric_identification;RED2924_8_worldtube_source_measure;RED2924_10_total_verdict", "MTS-to-EH reduction contract"),
        ("SRC2930_15_2925_vector", SRC_2925_VECTOR, "RV2925_0_metric_readout;RV2925_8_Poisson_Gauss_orbit;RV2925_TOTAL", "local GR reduction residual vector"),
        ("SRC2930_16_2928_beta", SRC_2928_BETA, "BH2928_BFB2919_0_beta_law;BH2928_BFB2919_1_source_residual;BH2928_BFB2919_6_epsilon_SN", "2928 beta/source-normalization handoff"),
        ("SRC2930_17_2928_coupling", SRC_2928_COUPLING, "CB2928_0_kappa_alpha3;CB2928_1_ellJ_alpha3;CB2928_3_coupling_total", "kappa/ellJ coupling rows"),
        ("SRC2930_18_2578_gate", SRC_2578_GATE, "COG2578_0_kappa_constant;COG2578_2_ellJ_source_scale;COG2578_4_verdict", "coupling baseline identity gate"),
        ("SRC2930_19_2578_ledger", SRC_2578_LEDGER, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ;RES2578_9_total", "coupling residual input ledger"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
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


def denominator_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("DBC2930_0_frame", "same observed source/orbit/readout frame", "tau_source=tau_charge=tau_clock=tau_readout and held fixed before local comparison", "NOT_PARENT_SIGNED", "2922/2923 require tau lock; current corpus has templates not one signed branch", False),
        ("DBC2930_1_denominator", "positive same-frame source denominator", "M_H_ref > 0 with G_ref, units, surface, reference, and no orbital-GM import", "MISSING_POSITIVE_SAME_FRAME_MHREF", "without this, A_source/B_source and epsilon_SN are not physically scoreable", False),
        ("DBC2930_2_A_source", "first-order source coefficient", "g_00=-1+2 A_source W/c^2+O(W^2), nabla^2 W=4*pi*G_ref*rho_H", "MISSING_PARENT_LINEAR_COEFFICIENT_MAP", "A_source must come from Hcore/source charge, not from fitted orbital GM", False),
        ("DBC2930_3_B_source", "second-order source coefficient", "g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(W^3)", "MISSING_PARENT_SECOND_ORDER_COEFFICIENT_MAP", "B_source must be from the same source family as A_source", False),
        ("DBC2930_4_square_law", "beta square-law theorem", "B_source=A_source^2 in the observed-U/source-normalized branch", "NOT_DERIVED", "this would give beta_eff=1 but is not in current corpus", False),
        ("DBC2930_5_Newton_source", "source-normalized Newton identity", "mu_obs=G0*M_H and epsilon_SN=0", "PARENT_SOURCE_MASS_IDENTITY_NOT_DERIVED", "2921 bridge is conditional; source ownership is not closed", False),
        ("DBC2930_6_kappa", "constant local coupling baseline", "Dln(kappa_MTS)=0 and G_ref/kappa source-frame match", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "kappa drift feeds Newton, beta, alpha3, clocks and local GR residuals", False),
        ("DBC2930_7_ellJ", "constant source-current scale", "Dln(ell_J)=0 in the same local source frame", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "ell_J drift feeds source-current, alpha3, beta and measured source mass", False),
        ("DBC2930_8_no_absorption", "no measured-GM/reference absorption", "delta_beta_source, epsilon_SN, Dln(kappa_MTS), Dln(ell_J) remain explicit until proved zero or finite-bounded", "PASS_GUARDRAIL", "this prevents the local limit from becoming a fitted calibration trick", True),
        ("DBC2930_9_verdict", "source-owner/Hcore beta denominator binding", "DBC2930_0 through DBC2930_8 close together", "DENOMINATOR_BINDING_NOT_DERIVED_FIRST_VALUE_QUEUE_REQUIRED", "2930 must move to source-backed first-value acquisition, not claim GR/Newton", False),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "clause": clause,
                "required_identity": required_identity,
                "current_status": current_status,
                "reason": reason,
                "condition_passed": condition_passed,
                "adopted_for_claim": False,
                "source_paths": ";".join(str(path) for path in [SRC_2922_OWNER, SRC_2923_HCORE, SRC_2924_REDUCTION, SRC_2928_COUPLING]),
            }
        )
        for contract_id, clause, required_identity, current_status, reason, condition_passed in specs
    ]


def source_coefficient_ledger_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCL2930_0_A_source", "A_source", "linear source coefficient in g_00=-1+2 A_source W/c^2", "MISSING_PARENT_LINEAR_COEFFICIENT_MAP", "derive from Hcore/Q_tau/Pi_M^H or source-backed finite row", "dimensionless", "Newton;beta;gamma;orbital"),
        ("SCL2930_1_B_source", "B_source", "second-order source coefficient in g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4", "MISSING_PARENT_SECOND_ORDER_COEFFICIENT_MAP", "derive same-family second-order coefficient or source-backed finite row", "dimensionless", "beta;local_GR"),
        ("SCL2930_2_delta_beta_source", "delta_beta_source", "B_source/A_source^2 - 1", "ACTIVE_NONCLAIM_FROM_2929", "prove B_source=A_source^2 or acquire finite A/B coefficient values", "dimensionless", "PPN_beta"),
        ("SCL2930_3_epsilon_SN", "epsilon_SN", "(mu_obs-G_eff*M_H)/(G_eff*M_H)", "ACTIVE_NONCLAIM_FROM_2929", "close source-normalized Newton/Gauss/orbital identity or acquire finite value", "dimensionless", "Newton;orbital;beta"),
        ("SCL2930_4_Dln_kappa", "Dln(kappa_MTS)", "local derivative/drift/range/species/frame residual of coupling baseline", "ACTIVE_NONCLAIM_FROM_2928_AND_2578", "prove constant kappa or acquire finite source-backed value", "dimensionless_or_derivative_envelope", "Newton;alpha3;beta;clock;R10"),
        ("SCL2930_5_Dln_ellJ", "Dln(ell_J)", "local derivative/drift/range/species/frame residual of source-current scale", "ACTIVE_NONCLAIM_FROM_2928_AND_2578", "prove constant ell_J or acquire finite source-backed value", "dimensionless_or_derivative_envelope", "source_current;alpha3;beta;WEP"),
        ("SCL2930_6_Delta_denominator_binding_abs", "Delta_denominator_binding_abs", "sum_abs(delta_beta_source,epsilon_SN,Dln(kappa_MTS),Dln(ell_J),A_source_gap,B_source_gap)", "TOTAL_NOT_SCORE_READY", "all heads need theorem-zero or finite/source-backed values; no cancellation", "mixed_component_ledger", "local_GR;Newton;PPN;R10"),
    ]
    return [
        add_common(
            {
                "ledger_id": ledger_id,
                "symbol": symbol,
                "definition": definition,
                "current_status": current_status,
                "next_requirement": next_requirement,
                "units": units,
                "arena_links": arena_links,
                "numeric_value_present": False,
                "theorem_zero": False,
                "selected_for_first_value": symbol in {"delta_beta_source", "epsilon_SN", "Dln(kappa_MTS)", "Dln(ell_J)", "Delta_denominator_binding_abs"},
                "source_paths": ";".join(str(path) for path in [SRC_2929_BETA, SRC_2928_COUPLING, SRC_2578_LEDGER, SRC_2921_SCORECARD]),
            }
        )
        for ledger_id, symbol, definition, current_status, next_requirement, units, arena_links in specs
    ]


def first_value_queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("FVQ2930_0_delta_beta_source", "delta_beta_source", "beta", "A_source and B_source from the same source-normalized Hcore branch", "7.8e-05", "highest_value_if_parent_coefficients_exist", "MISSING_A_SOURCE_B_SOURCE_VALUES"),
        ("FVQ2930_1_epsilon_SN", "epsilon_SN", "source_normalized_Newton", "mu_obs, G_eff, M_H, source frame and uncertainty with no orbital-GM circular denominator", "7.8e-05_or_contextual_Newton_bound", "highest_value_if_source_mass_row_exists", "MISSING_MUOBS_GEFF_MH_ROW"),
        ("FVQ2930_2_Dln_kappa", "Dln(kappa_MTS)", "coupling_baseline", "time/range/species/frame derivative or theorem-zero source path for kappa_MTS", "arena_specific", "selected_if_coupling_data_available", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE"),
        ("FVQ2930_3_Dln_ellJ", "Dln(ell_J)", "source_current_scale", "time/range/species/frame derivative or theorem-zero source path for ell_J", "arena_specific", "selected_if_source_current_data_available", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE"),
        ("FVQ2930_4_A_source", "A_source", "linear_source_coefficient", "parent weak-field linear coefficient extraction with units and source path", "nonzero_and_frame_locked", "selected_if_parent_action_coefficients_available", "MISSING_PARENT_LINEAR_COEFFICIENT_MAP"),
        ("FVQ2930_5_B_source", "B_source", "second_order_source_coefficient", "parent weak-field O(W^2) coefficient extraction with same denominator as A_source", "finite_and_frame_locked", "selected_if_parent_action_coefficients_available", "MISSING_PARENT_SECOND_ORDER_COEFFICIENT_MAP"),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "symbol": symbol,
                "sector": sector,
                "required_input": required_input,
                "target_bound_or_gate": target_bound_or_gate,
                "priority_logic": priority_logic,
                "current_status": current_status,
                "units_locked": False,
                "source_path_required": True,
                "numeric_value_present": False,
                "theorem_zero": False,
                "valid_for_claim": False,
            }
        )
        for queue_id, symbol, sector, required_input, target_bound_or_gate, priority_logic, current_status in specs
    ]


def reduction_impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("LRI2930_0_Newton", "Newton limit", "requires epsilon_SN=0 plus constant source/coupling denominator", "BLOCKED_NONCLAIM", "source owner/Hcore denominator unsigned"),
        ("LRI2930_1_beta", "PPN beta", "requires beta_eff=B_source/A_source^2 and B_source=A_source^2", "BLOCKED_NONCLAIM", "exact extraction law yes, square law no"),
        ("LRI2930_2_alpha3", "PPN alpha3", "requires coupling/source-current drift and preferred-frame heads zero or bounded", "BLOCKED_NONCLAIM", "Dln(kappa_MTS), Dln(ell_J), boundary/domain heads active"),
        ("LRI2930_3_RV2925", "MTS-to-EH local reduction vector", "requires metric readout, constant coupling, EH core, matter descent, source/worldtube, and Poisson/Gauss/orbit clauses", "BLOCKED_NONCLAIM", "2925 residual vector remains nonzero/unsourced"),
        ("LRI2930_4_best_next", "best route of attack", "obtain one parent coefficient theorem or one finite source-backed local residual value", "FORWARD_ROUTE_SELECTED", "moves from pure derivation attempt to derivation-or-first-value falsifiable row"),
    ]
    return [
        add_common(
            {
                "impact_id": impact_id,
                "target": target,
                "requires": requires,
                "current_status": current_status,
                "reason": reason,
                "source_paths": ";".join(str(path) for path in [SRC_2929_DOC, SRC_2925_VECTOR, SRC_2928_COUPLING, SRC_2924_REDUCTION]),
            }
        )
        for impact_id, target, requires, current_status, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2930_0_denominator_binding", "same-frame source denominator/coefficient map is parent-signed", "BLOCKED_NONCLAIM", "M_H_ref, Pi_M^H, A_source, B_source not owned together", False),
        ("CG2930_1_first_value", "one first-value residual row is source-backed and units-locked", "BLOCKED_NONCLAIM", "queue rows are schemas only; no numeric/theorem-zero value imported", False),
        ("CG2930_2_Newton", "source-normalized Newton/Gauss/orbital pass", "BLOCKED_NONCLAIM", "epsilon_SN remains active", False),
        ("CG2930_3_beta", "PPN beta pass", "BLOCKED_NONCLAIM", "delta_beta_source remains active", False),
        ("CG2930_4_coupling", "constant kappa_MTS and ell_J pass", "BLOCKED_NONCLAIM", "Dln(kappa_MTS) and Dln(ell_J) remain active", False),
        ("CG2930_5_local_GR", "local GR/Newton reduction follows", "BLOCKED_NONCLAIM", "RV2925 and beta/Newton/coupling heads remain open", False),
        ("CG2930_6_progress", "2930 selects a falsifiable next row instead of another loop", "PASS_GUARDRAIL", "next checkpoint must derive a coefficient or acquire a first value", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "current_status": current_status,
                "reason": reason,
                "claim_passed": claim_passed,
            }
        )
        for gate_id, claim, current_status, reason, claim_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2930_0_binding_result", "do not claim source-owner/Hcore denominator binding", "A_source, B_source, M_H_ref, kappa_MTS and ell_J are not parent-owned together", "keep local GR/Newton nonclaim", False),
        ("DEC2930_1_no_loop", "do not rerun the owner theorem without new primitive input", "2921-2924 already localize the missing owner package", "move to a coefficient theorem or first-value row", False),
        ("DEC2930_2_first_value_policy", "first acceptable forward row must be theorem-zero or finite/source-backed", "no cancellation and no measured-GM absorption are the discipline gates", "target delta_beta_source, epsilon_SN, Dln(kappa_MTS), or Dln(ell_J)", False),
        ("DEC2930_3_project_state", "project is closer but still pre-claim", "the GR reduction spine now has explicit denominator/coupling rows and a next empirical acquisition queue", "derive or acquire one row in 2931", False),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "valid_for_claim": valid_for_claim,
            }
        )
        for decision_id, decision, because, next_action, valid_for_claim in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2930_0_2931",
                "selection": "selected_primary",
                "target_doc": "2931-Y5-R2FR-parent-source-coefficient-theorem-or-first-finite-local-residual-value-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_source_coefficient_theorem_or_first_finite_local_residual_value_under_AX1090_2931.py",
                "objective": "try one concrete coefficient theorem first: derive A_source and B_source from the same Hcore/source denominator and test whether B_source=A_source^2; if that fails, acquire or stage the first finite source-backed value for delta_beta_source, epsilon_SN, Dln(kappa_MTS), or Dln(ell_J) with units and no measured-GM absorption",
                "acceptance_gate": "one row becomes theorem-zero or finite/source-backed with source path, units, bound/comparator, and valid_for_claim policy; otherwise all local-GR/Newton claims stay closed and the missing source input is named exactly",
                "fallback": "if parent coefficients are inaccessible, prioritize Dln(kappa_MTS) or Dln(ell_J) because they also hit alpha3/Newton/clock arenas",
                "valid_for_claim": False,
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"]),
        ("queue_copy", OUTPUTS["queue"], BRANCH_OUTPUTS["queue_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copies:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    contract = read_csv_rows(OUTPUTS["contract"])
    ledger = read_csv_rows(OUTPUTS["ledger"])
    queue = read_csv_rows(OUTPUTS["queue"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    required_contracts = {
        "DBC2930_1_denominator",
        "DBC2930_2_A_source",
        "DBC2930_3_B_source",
        "DBC2930_6_kappa",
        "DBC2930_7_ellJ",
        "DBC2930_9_verdict",
    }
    required_symbols = {
        "A_source",
        "B_source",
        "delta_beta_source",
        "epsilon_SN",
        "Dln(kappa_MTS)",
        "Dln(ell_J)",
        "Delta_denominator_binding_abs",
    }
    required_queue_symbols = {"delta_beta_source", "epsilon_SN", "Dln(kappa_MTS)", "Dln(ell_J)", "A_source", "B_source"}
    promoted_rows = [
        row
        for row in [*ledger, *queue]
        if as_bool(row.get("numeric_value_present")) or as_bool(row.get("theorem_zero")) or as_bool(row.get("valid_for_claim"))
    ]
    all_paths = [Path(row["source_path"]) for row in source_rows if row.get("source_path")]
    no_formalization_2930 = not list(FORMALIZATION.rglob("*2930*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2930_0_sources_exist", all(as_bool(row.get("path_exists")) for row in source_rows), "every cited source path exists"),
        ("VAL2930_1_source_anchors_found", all(as_bool(row.get("anchors_found")) for row in source_rows), "every cited source anchor is present"),
        ("VAL2930_2_outputs_parse", all(csv_parses(path) for path in OUTPUTS.values()), "all 2930 CSV outputs parse"),
        ("VAL2930_3_doc_exists", DOC.exists(), "2930 markdown checkpoint exists"),
        ("VAL2930_4_contract_complete", required_contracts <= {row.get("contract_id", "") for row in contract}, "denominator binding contract has required clauses"),
        ("VAL2930_5_contract_nonclaim", any(row.get("contract_id") == "DBC2930_9_verdict" and row.get("current_status") == "DENOMINATOR_BINDING_NOT_DERIVED_FIRST_VALUE_QUEUE_REQUIRED" for row in contract), "denominator binding verdict remains nonclaim"),
        ("VAL2930_6_ledger_complete", required_symbols <= {row.get("symbol", "") for row in ledger}, "source coefficient ledger has all required symbols"),
        ("VAL2930_7_queue_complete", required_queue_symbols <= {row.get("symbol", "") for row in queue}, "first-value acquisition queue has all required targets"),
        ("VAL2930_8_no_rows_promoted", not promoted_rows, "no ledger/queue row is numeric, theorem-zero, or valid-for-claim"),
        ("VAL2930_9_claims_closed", all(not as_bool(row.get("claim_passed")) for row in claims), "all claim gates remain closed"),
        ("VAL2930_10_next_target_selected", any(row.get("next_id") == "NEXT2930_0_2931" for row in next_rows), "2931 next target selected"),
        ("VAL2930_11_branch_copies_parse", all(as_bool(row.get("destination_parses")) for row in branches), "branch copies parse cleanly"),
        ("VAL2930_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()), "all outputs remain under post-checkpoint-work"),
        ("VAL2930_13_sources_not_formalization", all(not is_under(path, FORMALIZATION) for path in all_paths) if FORMALIZATION.exists() else True, "no formalization-workbench source/output dependency"),
        ("VAL2930_14_no_formalization_2930_outputs", no_formalization_2930, "no formalization-workbench 2930 outputs"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "blocking_if_false": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2930_OVERALL",
                "passed": overall,
                "check": "2930 validation overall",
                "blocking_if_false": True,
            }
        )
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    contract = read_csv_rows(OUTPUTS["contract"])
    ledger = read_csv_rows(OUTPUTS["ledger"])
    queue = read_csv_rows(OUTPUTS["queue"])
    impact = read_csv_rows(OUTPUTS["impact"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2930_OVERALL"), {})

    sections = [
        "# 2930 - Y5/R2FR Source-Owner Hcore To Beta Denominator Binding Or Finite Local Residual First Value Under AX1090",
        "",
        "Status: `Y5_R2FR_2930_denominator_binding_not_derived_first_value_queue_2931_next`",
        "",
        "Claim ceiling: `source_denominator_contract_yes_parent_binding_no_first_value_queue_yes_no_Newton_no_beta_no_alpha3_no_local_GR_no_PPN_no_R10_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2930 binds the source-owner/Hcore chain back into the live local-GR reduction gates. The useful expansion grammar is now explicit:",
        "",
        "`g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(W^3)`, with `nabla^2 W=4*pi*G_ref*rho_H`,",
        "",
        "so the measured-`U` beta comparison is still",
        "",
        "`beta_eff = B_source/A_source^2`.",
        "",
        "The current corpus does not yet parent-sign the same-frame source denominator, `A_source`, `B_source`, `kappa_MTS`, and `ell_J` together. Therefore this checkpoint does not claim Newton, beta, PPN, or local GR. It turns the obstruction into a first-value acquisition queue: either derive the parent coefficient theorem next, or source one finite residual row without measured-`GM` absorption.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Denominator Binding Contract",
        "",
        md_table(contract, ["contract_id", "clause", "required_identity", "current_status", "reason", "condition_passed", "adopted_for_claim"]),
        "",
        "## Source Coefficient Ledger",
        "",
        md_table(ledger, ["ledger_id", "symbol", "definition", "current_status", "next_requirement", "units", "arena_links", "numeric_value_present", "theorem_zero", "selected_for_first_value"]),
        "",
        "## First-Value Acquisition Queue",
        "",
        md_table(queue, ["queue_id", "symbol", "sector", "required_input", "target_bound_or_gate", "priority_logic", "current_status", "numeric_value_present", "theorem_zero", "valid_for_claim"]),
        "",
        "## Local GR Reduction Impact",
        "",
        md_table(impact, ["impact_id", "target", "requires", "current_status", "reason"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "current_status", "reason", "claim_passed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branches, ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "blocking_if_false"]),
        "",
        f"Validation overall: `{overall.get('passed', False)}`.",
        "",
        "## Bottom Line",
        "",
        "This is not a victory lap, but it is a useful narrowing. The GR/Newton route now has a precise coefficient contract: own the same source denominator, then read `A_source` and `B_source` from the same parent weak-field family. If `B_source=A_source^2` follows, beta becomes clean. If not, the theory must carry `delta_beta_source` as a real finite residual.",
        "",
        "The best next move is one hard coefficient theorem or one honest first value. The cleanest leap is `A_source/B_source` from Hcore. The more empirical fallback is a source-backed value or bound for `Dln(kappa_MTS)` or `Dln(ell_J)`, because those touch alpha3, Newton, clocks, and source-current tests at once.",
        "",
        "## Non-Claims",
        "",
        "- no same-frame source denominator is parent-signed;",
        "- no `A_source` or `B_source` value is claimed;",
        "- no `B_source=A_source^2` theorem is claimed;",
        "- no `Dln(kappa_MTS)=0` or `Dln(ell_J)=0` theorem is claimed;",
        "- no Newton, beta, PPN, R10, or local-GR pass is claimed;",
        "- no public/GitHub claim is made.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["contract"], denominator_contract_rows())
    write_csv(OUTPUTS["ledger"], source_coefficient_ledger_rows())
    write_csv(OUTPUTS["queue"], first_value_queue_rows())
    write_csv(OUTPUTS["impact"], reduction_impact_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    DOC.write_text("# 2930 preflight\n", encoding="utf-8")
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2930_OVERALL"), {})
    print(f"wrote {DOC}")
    print(f"validation overall: {overall.get('passed')}")


if __name__ == "__main__":
    main()
