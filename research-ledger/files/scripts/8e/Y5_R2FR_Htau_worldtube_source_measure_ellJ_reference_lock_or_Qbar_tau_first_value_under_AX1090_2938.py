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

CHECKPOINT = "2938"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2938-Y5-R2FR-Htau-worldtube-source-measure-ellJ-reference-lock-or-Qbar-tau-first-value-under-AX1090.md"

SRC_2937_DOC = ROOT / "2937-Y5-R2FR-ellJ-source-current-owner-theorem-or-Qbar-tau-R10-projection-contract-under-AX1090.md"
SRC_2937_THEOREM = RESIDUALS / "P8_Y5_R2FR_2937_ELLJ_OWNER_THEOREM_ATTEMPT.csv"
SRC_2937_LEDGER = RESIDUALS / "P8_Y5_R2FR_2937_SOURCE_CURRENT_CLAUSE_LEDGER.csv"
SRC_2937_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2937_QBAR_TAU_R10_PROJECTION_CONTRACT.csv"
SRC_2937_TRANSFER = RESIDUALS / "P8_Y5_R2FR_2937_DOTG_R10_NEWTON_TRANSFER_MAP.csv"
SRC_2937_QUEUE = RESIDUALS / "P8_Y5_R2FR_2937_NUMERIC_ACQUISITION_QUEUE.csv"
SRC_2937_NEXT = RESIDUALS / "P8_Y5_R2FR_2937_NEXT_TARGET.csv"
SRC_2937_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2937_VALIDATION.csv"

SRC_1016_DOC = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
SRC_1017_DOC = ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
SRC_1007_DOC = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"

SRC_2667_CURL = RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv"
SRC_2667_GATE = RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"
SRC_2445_CERT = RESIDUALS / "P8_Y5_PARENT_QLOC_2445_HTAU_SOURCE_CHARGE_CERTIFICATE_AUDIT.csv"
SRC_2351_STATUS = RESIDUALS / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv"
SRC_2339_REF = RESIDUALS / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv"
SRC_2382_REF = RESIDUALS / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv"
SRC_1017_REFLOCK = RESIDUALS / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv"
SRC_910_CONTRACT = RESIDUALS / "P8_Y5_R10_910_INTEGRABILITY_REFERENCE_CONTRACT.csv"
SRC_2611_WORLDTUBE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv"
SRC_2611_DESCENT = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv"
SRC_2738_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2738_WORLDTUBE_FIRST_PAIR_CORE_TEMPLATE.csv"
SRC_2775_REQUIREMENTS = RESIDUALS / "P8_Y5_R2FR_2775_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
SRC_2642_ARENA = RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_ARENA_PROJECTION_SKELETON.csv"
SRC_2665_LOCK = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
SRC_2665_GATE = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2938_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2938_SOURCE_MEASURE_RESIDUAL_IDENTITY.csv",
    "obstructions": RESIDUALS / "P8_Y5_R2FR_2938_SOURCE_MEASURE_GLUE_OBSTRUCTION_LEDGER.csv",
    "reference": RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
    "first_value": RESIDUALS / "P8_Y5_R2FR_2938_QBAR_TAU_FIRST_VALUE_GATE.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2938_CLOSURE_ONLY_AXIOM_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2938_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2938_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2938_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2938_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2938_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "Htau_worldtube_source_measure_theorem_attempt_2938_NONCLAIM.csv",
    "identity_copy": PARENT_ACTION / "Source_measure_residual_identity_2938_NONCLAIM.csv",
    "first_value_copy": LOCAL_BOUNDS / "Qbar_tau_first_value_gate_2938_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR2938_HTAU_WORLDTUBE_OR_QBAR_TAU_NEXT_NONCLAIM.csv",
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
        ("SRC2938_00_2937_doc", SRC_2937_DOC, "NEXT2937_0_2938;M_source[W]=H_tau[S]-H_ref;Validation overall: `True`", "2937 handoff to Htau/worldtube source-measure glue"),
        ("SRC2938_01_2937_theorem", SRC_2937_THEOREM, "EJO2937_3_worldtube_measure_glue;EJO2937_6_verdict", "ellJ owner theorem attempt"),
        ("SRC2938_02_2937_ledger", SRC_2937_LEDGER, "SCL2937_5_worldtube;SCL2937_6_reference", "source-current clause ledger"),
        ("SRC2938_03_2937_contract", SRC_2937_CONTRACT, "R10C2937_0_Qbar_XH;R10C2937_1_tau_R10", "Qbar/tau projection contract"),
        ("SRC2938_04_2937_transfer", SRC_2937_TRANSFER, "TR2937_0_dotG_to_kappa;TR2937_2_Newton_orbital", "transfer map"),
        ("SRC2938_05_2937_queue", SRC_2937_QUEUE, "ACQ2937_8_worldtube_glue;MISSING_PARENT_INPUT", "acquisition queue"),
        ("SRC2938_06_2937_next", SRC_2937_NEXT, "NEXT2937_0_2938", "machine-readable 2938 target"),
        ("SRC2938_07_2937_validation", SRC_2937_VALIDATION, "VAL2937_OVERALL;True", "2937 validation"),
        ("SRC2938_08_1016_doc", SRC_1016_DOC, "W_source = closure(supp J_H[tau]);source-measure equality;V1016_SUMMARY", "worldtube selector contract"),
        ("SRC2938_09_1017_doc", SRC_1017_DOC, "M_H_ref;reference/integrability lock;CG1017_4_MHref_claim", "Hamiltonian PiM reference lock"),
        ("SRC2938_10_1007_doc", SRC_1007_DOC, "H_tau integrability/fixed-reference theorem attempted;SRS1007_0_integrability_formula", "Htau integrability residual row"),
        ("SRC2938_11_2667_curl", SRC_2667_CURL, "HTC2667_1_LX_owner;HTC2667_6_reference_curl_split", "integrability curl proof audit"),
        ("SRC2938_12_2667_gate", SRC_2667_GATE, "ICG2667_0_LX_owner;ICG2667_6_units", "integrability gate"),
        ("SRC2938_13_2445_cert", SRC_2445_CERT, "HTC2445_0_Htau_owner;HTC2445_4_source_equality", "Htau source-charge certificate"),
        ("SRC2938_14_2351_status", SRC_2351_STATUS, "HHS2351_1_Htau_integrability;HHS2351_4_anti_circularity_guard", "Htau/Href source row status"),
        ("SRC2938_15_2339_ref", SRC_2339_REF, "TQF2339_2_theta_Qtau;TQF2339_6_MHref_positive", "theta/Qtau/fixed reference audit"),
        ("SRC2938_16_2382_ref", SRC_2382_REF, "FRT2382_2_source_blind_chain_rule;FRT2382_6_verdict", "fixed reference selector theorem"),
        ("SRC2938_17_1017_reflock", SRC_1017_REFLOCK, "HRL1017_1_integrability_curl;HRL1017_5_MHref_denominator", "reference lock law"),
        ("SRC2938_18_910_contract", SRC_910_CONTRACT, "HIR910_3_integrability_zero;HIR910_6_source_calibration_link", "integrability/reference contract"),
        ("SRC2938_19_2611_worldtube", SRC_2611_WORLDTUBE, "WTA2611_0_support_selector;WTA2611_1_same_charge", "matter worldtube source owner audit"),
        ("SRC2938_20_2611_descent", SRC_2611_DESCENT, "MWD2611_1_conditional_theorem;MWD2611_3_worldtube_support", "matter/worldtube descent attempt"),
        ("SRC2938_21_2738_template", SRC_2738_TEMPLATE, "CORE2738_0_Wsrc;CORE2738_1_Jq", "worldtube first-pair template"),
        ("SRC2938_22_2775_requirements", SRC_2775_REQUIREMENTS, "SWT2775_0_source_stress_profile;SWT2775_5_verdict", "source worldtube requirements"),
        ("SRC2938_23_2642_arena", SRC_2642_ARENA, "ARENA2642_0_Newton_orbital;ARENA2642_2_R10", "arena projection skeleton"),
        ("SRC2938_24_2665_lock", SRC_2665_LOCK, "HLOCK2665_0_target;HLOCK2665_3_MHref", "Hamiltonian PiM Qbar lock"),
        ("SRC2938_25_2665_gate", SRC_2665_GATE, "PDG2665_1_worldtube;PDG2665_5_projector", "projector denominator gate"),
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "HWS2938_0_master_identity",
            "claim": "shared Hamiltonian/worldtube source measure exists",
            "exact_statement": "If delta H_tau[S]=int_S(delta Q_tau^MTS-i_tau theta_MTS)-delta H_ref is integrable, H_ref is fixed, and dQ_tau^MTS=rho_H dV_H+dB_zero on Sigma\\W_source, then M_source[W] := int_W rho_H dV_H = H_tau[S_outer]-H_ref - R_source_measure.",
            "derivation_status": "EXACT_CONDITIONAL_GAUSS_HAMILTONIAN_IDENTITY",
            "current_mts_status": "NOT_PARENT_SIGNED",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "theta_MTS/Q_tau^MTS, H_tau integrability, fixed H_ref, same-frame M_H_ref, and boundary/projector residuals are not closed",
            "source_paths": f"{SRC_1016_DOC};{SRC_1017_DOC};{SRC_2667_CURL};{SRC_2445_CERT}",
        },
        {
            "theorem_id": "HWS2938_1_theta_Qtau",
            "claim": "parent Noether charge is extracted",
            "exact_statement": "J_tau=theta_MTS(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau, with C_tau zero or explicitly retained.",
            "derivation_status": "REQUIRED_FIRST_PREMISE",
            "current_mts_status": "MISSING_PARENT_THETA_QTAU",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "single parent variation and sector current decomposition remain templates",
            "source_paths": f"{SRC_2339_REF};{SRC_2445_CERT};{SRC_2351_STATUS}",
        },
        {
            "theorem_id": "HWS2938_2_integrability",
            "claim": "H_tau is path-independent on the allowed branch",
            "exact_statement": "delta_1 delta_2 H_tau - delta_2 delta_1 H_tau = int_S i_tau omega_total(delta_1,delta_2)+curl(delta H_ref)=0.",
            "derivation_status": "CONDITIONAL_STANDARD_CPS_CRITERION",
            "current_mts_status": "INTEGRABILITY_BLOCKED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "L_X, Theta_X, omega_X, tau/surface lock, boundary exactness, projector stress and reference curl are missing",
            "source_paths": f"{SRC_2667_CURL};{SRC_2667_GATE};{SRC_1017_REFLOCK}",
        },
        {
            "theorem_id": "HWS2938_3_reference_lock",
            "claim": "H_ref is source-blind and fixed before readout",
            "exact_statement": "D_source Sigma_ref=0 implies D_source H_ref=0, and Sigma_ref carries no GM_obs, fitted mass, composition, source radius, or M_H_ref label.",
            "derivation_status": "CHAIN_RULE_CRITERION_DERIVED",
            "current_mts_status": "REFERENCE_SELECTOR_UNSIGNED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "source-blind selector grammar exists but no parent selector equation or positive same-frame denominator exists",
            "source_paths": f"{SRC_2382_REF};{SRC_2339_REF};{SRC_1017_REFLOCK}",
        },
        {
            "theorem_id": "HWS2938_4_worldtube_selector",
            "claim": "W_source is selected before arena fitting",
            "exact_statement": "W_source=closure(supp J_H[tau]) with compact regular support and linked exterior surfaces fixed in the same observed coframe.",
            "derivation_status": "CONDITIONAL_SELECTOR_LEMMA",
            "current_mts_status": "WORLDTUBE_OWNER_OPEN",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "same-frame J_H, tau lock, compactness, charge map, coupling descent and domain/projector silence remain unsigned",
            "source_paths": f"{SRC_1016_DOC};{SRC_2611_WORLDTUBE};{SRC_2738_TEMPLATE}",
        },
        {
            "theorem_id": "HWS2938_5_anti_circularity",
            "claim": "Newton/GM is not imported to define the source charge",
            "exact_statement": "M_H_ref and M_source[W] must be derived before orbital GM calibration; measured GM can only be a downstream readout.",
            "derivation_status": "GUARDRAIL_EXACT",
            "current_mts_status": "NONCLAIM_GUARD_ONLY",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "guard prevents cheating but does not provide the denominator",
            "source_paths": f"{SRC_2351_STATUS};{SRC_1016_DOC};{SRC_2642_ARENA}",
        },
        {
            "theorem_id": "HWS2938_6_verdict",
            "claim": "current MTS proves M_source[W]=H_tau-H_ref=int_W rho_H dV_H",
            "exact_statement": "A current claim requires HWS2938_1..4 plus bounded residual rows from the identity ledger.",
            "derivation_status": "THEOREM_ROUTE_SHARPENED_BUT_NOT_CLOSED",
            "current_mts_status": "SOURCE_MEASURE_GLUE_NOT_DERIVED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "demote current route to closure-only axiom or fill nonclaim first-value rows",
            "source_paths": f"{SRC_2937_DOC};{SRC_1016_DOC};{SRC_1017_DOC}",
        },
    ]
    return [add_common(row) for row in rows]


def residual_identity_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "identity_id": "SMRI2938_0_master",
            "quantity": "R_source_measure",
            "exact_formula": "M_source[W] - (H_tau[S_outer]-H_ref) = R_thetaQ + R_integrability + R_ref + R_boundary + R_projector + R_worldtube + R_frame + R_units",
            "units": "mass/source-charge units",
            "current_status": "IDENTITY_EXACT_COMPONENTS_UNFILLED",
            "required_for_zero": "all residual components theorem-zero or source-backed numeric bounds",
        },
        {
            "identity_id": "SMRI2938_1_R_thetaQ",
            "quantity": "R_thetaQ",
            "exact_formula": "failure of theta_MTS/Q_tau^MTS to be extracted from one parent Lagrangian current",
            "units": "charge units",
            "current_status": "MISSING_PARENT_THETA_QTAU",
            "required_for_zero": "parent L, theta_MTS, Q_tau^MTS, C_tau decomposition",
        },
        {
            "identity_id": "SMRI2938_2_R_integrability",
            "quantity": "R_integrability",
            "exact_formula": "field-space curl integral int_S i_tau omega_total + curl(delta H_ref)",
            "units": "charge units",
            "current_status": "MISSING_INTEGRABILITY_ZERO_OR_BOUND",
            "required_for_zero": "L_X/Theta_X/omega_X owner and boundary exactness",
        },
        {
            "identity_id": "SMRI2938_3_R_ref",
            "quantity": "R_ref",
            "exact_formula": "source/radius/frame/lambda derivative of H_ref or reference selector",
            "units": "charge units",
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "required_for_zero": "source-blind Sigma_ref with no GM/material/readout labels",
        },
        {
            "identity_id": "SMRI2938_4_R_boundary",
            "quantity": "R_boundary",
            "exact_formula": "B_zero_flux + Delta_symp + edge/corner terms across linked surfaces",
            "units": "charge units",
            "current_status": "BOUNDARY_COMPONENTS_MISSING",
            "required_for_zero": "proper/exact boundary theorem or source-backed finite terms",
        },
        {
            "identity_id": "SMRI2938_5_R_projector",
            "quantity": "R_projector",
            "exact_formula": "[d,Pi_M]J_H plus delta Pi_M stress/domain/Hodge variation",
            "units": "source-normalized charge units",
            "current_status": "RETAINED_PROJECTOR_OBSTRUCTION",
            "required_for_zero": "Pi_M commutator zero or bounded row",
        },
        {
            "identity_id": "SMRI2938_6_R_worldtube",
            "quantity": "R_worldtube",
            "exact_formula": "variation or mismatch of W_source, compact support, linking surfaces and source mask",
            "units": "source-normalized charge units",
            "current_status": "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "required_for_zero": "W_source=closure(supp J_H[tau]) parent-owned",
        },
        {
            "identity_id": "SMRI2938_7_R_frame",
            "quantity": "R_frame",
            "exact_formula": "different tau/coframe/clock/readout normalizations between source charge and observations",
            "units": "dimensionless or charge units after normalization",
            "current_status": "MISSING_SAME_FRAME_LOCK",
            "required_for_zero": "same observed tau/coframe across matter, H_tau, clocks, R10 and orbital readout",
        },
        {
            "identity_id": "SMRI2938_8_R_units",
            "quantity": "R_units",
            "exact_formula": "ell_J/C_source/unit conversion residual hidden in M_H_ref or Qbar_XH denominator",
            "units": "dimensionless normalization",
            "current_status": "ELLJ_OWNER_NOT_DERIVED",
            "required_for_zero": "ell_J fixed pre-readout and C_source source-current normalization fixed",
        },
    ]
    return [add_common(row) for row in rows]


def obstruction_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS2938_0_theta_Qtau", "theta_MTS/Q_tau^MTS", "MISSING_PARENT_THETA_QTAU", SRC_2339_REF, "derive single parent current-chain variation"),
        ("OBS2938_1_integrability", "delta H_tau curl", "INTEGRABILITY_BLOCKED", SRC_2667_GATE, "prove curl zero or fill component bound"),
        ("OBS2938_2_reference", "H_ref/Sigma_ref", "REFERENCE_SELECTOR_UNSIGNED", SRC_2382_REF, "parent-sign source-blind fixed reference selector"),
        ("OBS2938_3_MHref", "M_H_ref", "MISSING_POSITIVE_SAME_FRAME_MHREF", SRC_2351_STATUS, "derive finite positive denominator without orbital GM import"),
        ("OBS2938_4_worldtube", "W_source", "MISSING_PARENT_WORLDTUBE_SELECTOR", SRC_2611_WORLDTUBE, "prove support selector and compactness"),
        ("OBS2938_5_same_charge", "Pi_M J_H equals Hamiltonian/topological source", "NOT_DERIVED_KEY_BLOCKER", SRC_2611_WORLDTUBE, "derive charge-current equality or carry R_eq/I_commutator"),
        ("OBS2938_6_projector", "Pi_M/domain stress", "RETAINED_PROJECTOR_OBSTRUCTION", SRC_2665_LOCK, "derive commutator zero or source-bound it"),
        ("OBS2938_7_tau_frame", "same tau/coframe", "MISSING_SAME_FRAME_LOCK", SRC_2339_REF, "lock tau across source, charge, clocks and readout"),
        ("OBS2938_8_anti_circularity", "not orbital GM imported", "GUARD_READY_NONCLAIM", SRC_2351_STATUS, "keep guard; no source claim until denominator derived"),
    ]
    return [
        add_common(
            {
                "obstruction_id": obstruction_id,
                "object": obj,
                "current_status": status,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "blocks_source_measure_claim": True,
                "next_action": next_action,
            }
        )
        for obstruction_id, obj, status, source_path, next_action in specs
    ]


def reference_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "REF2938_0_MHref_definition",
            "quantity": "M_H_ref",
            "contract": "M_H_ref := H_tau[S_outer] - H_ref, finite, positive, same tau/coframe, and not imported from orbital GM",
            "current_status": "MISSING_STABLE_MH_REF",
            "required_inputs": "H_tau; H_ref; units; tau_id; frame_id; source path; positivity; no-orbital-import certificate",
        },
        {
            "contract_id": "REF2938_1_Href_selector",
            "quantity": "H_ref/Sigma_ref",
            "contract": "Sigma_ref depends only on boundary/topology/stationarity/asymptotic coframe data, not source/material/GM/readout labels",
            "current_status": "DEFINITION_CONTRACT_ONLY",
            "required_inputs": "parent selector equation; source-blind derivative certificate",
        },
        {
            "contract_id": "REF2938_2_ellJ_lock",
            "quantity": "ell_J",
            "contract": "ell_J is fixed before source/readout and cannot be absorbed into M_H_ref, Qbar_XH, C_source or measured GM",
            "current_status": "NAMED_NOT_OWNED",
            "required_inputs": "source-current owner theorem or independent drift bound",
        },
        {
            "contract_id": "REF2938_3_Csource_lock",
            "quantity": "C_source",
            "contract": "C_source is the same source-current normalization in dotG, Newton/orbital, R10 and PPN",
            "current_status": "SOURCE_CURRENT_NORMALIZATION_NOT_FIXED",
            "required_inputs": "J_H/rho_H worldtube measure glue and frame/reference silence",
        },
        {
            "contract_id": "REF2938_4_no_laundering",
            "quantity": "anti-circularity guard",
            "contract": "Measured orbital GM may test the derived source charge but cannot define H_tau, H_ref, M_H_ref, ell_J, Qbar_XH or tau_R10",
            "current_status": "GUARDRAIL_INSTALLED_NONCLAIM",
            "required_inputs": "audit path for every source/denominator row",
        },
    ]
    return [add_common(row) for row in rows]


def first_value_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("FVG2938_0_MHref", "M_H_ref", "first positive same-frame source denominator", "MISSING_STABLE_MH_REF", SRC_2351_STATUS),
        ("FVG2938_1_Qbar_XH", "Qbar_XH(lambda;source)", "first source charge denominator for R10 alpha", "BLOCKED_BY_MHREF_AND_QX_PIECES", SRC_2937_CONTRACT),
        ("FVG2938_2_tau_R10", "tau_R10(lambda;test)", "first R10 material/readout projection", "MISSING_ARENA_PROJECTION", SRC_2937_CONTRACT),
        ("FVG2938_3_dotG_transfer", "D_t ln kappa_MTS bound transfer", "first transfer from dotG/G to kappa_MTS", "BLOCKED_BY_ELLJ_CSOURCE_RFRAME", SRC_2937_TRANSFER),
        ("FVG2938_4_Newton_GM", "Newton/orbital source check", "first non-circular comparison to orbital GM", "BLOCKED_UNTIL_SOURCE_CHARGE_DERIVED", SRC_2642_ARENA),
        ("FVG2938_5_claim_gate", "any first value claim", "no MISSING_PARENT_INPUT, source paths exist, valid_for_claim=true", "CLAIM_BLOCKED", SRC_2937_QUEUE),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "quantity": quantity,
                "purpose": purpose,
                "current_status": status,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "numeric_value": "MISSING_PARENT_INPUT",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for gate_id, quantity, purpose, status, source_path in specs
    ]


def closure_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "closure_id": "CAX2938_0_source_measure_axiom",
            "axiom_if_adopted": "Axiom SM: M_source[W] := H_tau[S_outer]-H_ref := int_W rho_H dV_H on the local weak-field branch.",
            "cost": "Turns source-measure glue into closure rather than derivation; must be labeled as an assumption in GR/Newton bridge.",
            "allowed_use": "private algebraic continuation only; no local-GR/Newton/R10 claim.",
            "current_recommendation": "do_not_adopt_yet_try_parent_derivation_first",
        },
        {
            "closure_id": "CAX2938_1_reference_axiom",
            "axiom_if_adopted": "Axiom REF: H_ref and ell_J are fixed pre-readout and source-blind.",
            "cost": "Blocks reference laundering but remains an axiom until Sigma_ref is parent-derived.",
            "allowed_use": "use as a temporary branch label, not evidence.",
            "current_recommendation": "keep_as_fallback_only",
        },
        {
            "closure_id": "CAX2938_2_Qbar_tau_axiom",
            "axiom_if_adopted": "Axiom R10: Qbar_XH and tau_R10 are same-source support integrals normalized by M_H_ref.",
            "cost": "Allows smoke calculations but does not prove the local branch.",
            "allowed_use": "nonclaim runner input only.",
            "current_recommendation": "only_after_failed_2939_derivation",
        },
    ]
    return [add_common(row) for row in rows]


def claim_gate_rows(theorem_rows: list[dict[str, Any]], identity_rows: list[dict[str, Any]], first_value_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conditional_identity = any(row["theorem_id"] == "HWS2938_0_master_identity" and row["derivation_status"] == "EXACT_CONDITIONAL_GAUSS_HAMILTONIAN_IDENTITY" for row in theorem_rows)
    current_source_measure = any(row["theorem_id"] == "HWS2938_6_verdict" and row["current_mts_status"] != "SOURCE_MEASURE_GLUE_NOT_DERIVED" for row in theorem_rows)
    identity_components_filled = all("MISSING" not in row["current_status"] and "UNFILLED" not in row["current_status"] and "UNSIGNED" not in row["current_status"] for row in identity_rows)
    first_values_ready = all(str(row["valid_for_claim"]).lower() == "true" and "MISSING" not in str(row["numeric_value"]) for row in first_value_rows)
    rows = [
        ("CG2938_0_conditional_identity", "conditional source-measure identity written", conditional_identity, "PASS_CONDITIONAL_NONCLAIM" if conditional_identity else "FAIL"),
        ("CG2938_1_current_source_measure", "current MTS proves M_source[W]=H_tau-H_ref", current_source_measure, "BLOCKED_NONCLAIM"),
        ("CG2938_2_residual_components", "all source-measure residual components are zero/bounded", identity_components_filled, "BLOCKED_COMPONENTS_UNFILLED"),
        ("CG2938_3_first_values", "Qbar/tau/MHref first values are score-ready", first_values_ready, "BLOCKED_MISSING_PARENT_INPUT"),
        ("CG2938_4_dotG_transfer", "dotG/G can constrain kappa_MTS", False, "BLOCKED_BY_ELLJ_CSOURCE_RFRAME"),
        ("CG2938_5_Newton_GR", "Newton/local-GR reduction can be claimed", False, "BLOCKED_BY_SOURCE_MEASURE_AND_PPN_RESIDUALS"),
        ("CG2938_6_R10", "R10 alpha branch can be claimed", False, "BLOCKED_BY_QBAR_TAU_MHREF"),
        ("CG2938_7_public_claim", "any public local/empirical claim allowed from 2938", False, "NO_PUBLIC_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "blocks_claim": not passed or gate_id != "CG2938_0_conditional_identity",
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2938_0_result",
            "decision": "keep source-measure theorem as conditional, not claimed",
            "reason": "the Gauss/Hamiltonian identity is exact once parent Noether charge, integrability, fixed reference and worldtube selector are signed",
            "next_action": "do not use M_source[W]=H_tau-H_ref as current MTS evidence yet",
        },
        {
            "decision_id": "DEC2938_1_biggest_blocker",
            "decision": "theta_MTS/Q_tau^MTS extraction is now the root blocker",
            "reason": "without the parent Noether charge, H_tau, M_H_ref, Qbar_XH and Newton source measure are all denominator shadows",
            "next_action": "derive a minimal parent Noether current extraction or stage exact closure-only axiom",
        },
        {
            "decision_id": "DEC2938_2_second_blocker",
            "decision": "integrability/reference lock remains coupled",
            "reason": "H_tau is not a number until its field-space curl and H_ref selector are fixed",
            "next_action": "split 2939 into theta/Qtau first, then curl/reference if theta/Qtau succeeds",
        },
        {
            "decision_id": "DEC2938_3_empirical_order",
            "decision": "delay Qbar/tau numeric first values",
            "reason": "running R10 now would just test placeholders because M_H_ref and source measure are not derived",
            "next_action": "keep first-value gates nonclaim until source-measure denominator exists",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2938_0_2939",
                "priority": "selected_primary",
                "next_doc": "2939-Y5-R2FR-parent-Noether-theta-Qtau-extraction-or-source-measure-closure-axiom-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_Noether_theta_Qtau_extraction_or_source_measure_closure_axiom_under_AX1090_2939.py",
                "objective": "Try to extract theta_MTS, Q_tau^MTS and C_tau from the minimal parent current-chain action so H_tau becomes a real source charge; if extraction fails, write the exact closure-only axiom and keep all local claims blocked.",
                "include": "single parent variation; theta_MTS; Q_tau^MTS; C_tau residual; tau generator; allowed boundary class; source-current leg; no EH-only import",
                "exclude": "R10/local-GR/Newton claim; measured-GM denominator; fitted H_ref; invented Q_tau; GitHub action; formalization-workbench edits",
            }
        )
    ]


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    first_value_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2938 - Y5 R2FR: Htau worldtube source-measure ellJ reference lock or Qbar/tau first value under AX1090

Status: `Y5_R2FR_2938_conditional_Htau_worldtube_source_measure_identity_written_current_MTS_blocked_theta_Qtau_2939_next`

Claim ceiling: `conditional_source_measure_identity_yes_current_M_source_no_MHref_no_Qbar_tau_no_dotG_transfer_no_Newton_no_local_GR_no_R10_no_GitHub_claim`

2938 is the serious bridge attempt: make the Newton/GR source object derivable instead of importing measured `GM`. The clean result is an exact conditional identity. If a parent Noether charge `Q_tau^MTS`, integrable `H_tau`, fixed source-blind `H_ref`, and parent-owned compact worldtube all exist in the same observed frame, then the source measure is the Hamiltonian charge:

`M_source[W] = int_W rho_H dV_H = H_tau[S_outer] - H_ref - R_source_measure`.

The current corpus still does not close the required parent objects, so this checkpoint refuses a claim and turns the missing source-measure equality into a component residual vector.

## Source Register

{md_table(source_rows, ["source_id", "source_type", "source_path", "path_exists", "anchors_found", "role"])}

## Htau/Worldtube Source-Measure Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim", "derivation_status", "current_mts_status", "condition_passed", "application_to_current_mts", "blocking_gap"])}

## Source-Measure Residual Identity

{md_table(identity_rows, ["identity_id", "quantity", "exact_formula", "current_status", "required_for_zero"])}

## Obstruction Ledger

{md_table(obstruction_rows, ["obstruction_id", "object", "current_status", "blocks_source_measure_claim", "next_action"])}

## MHref/ellJ Reference Lock Contract

{md_table(reference_rows, ["contract_id", "quantity", "contract", "current_status", "required_inputs"])}

## Qbar/tau First-Value Gate

{md_table(first_value_rows, ["gate_id", "quantity", "purpose", "current_status", "numeric_value", "valid_for_claim"])}

## Closure-Only Axiom Ledger

{md_table(closure_rows, ["closure_id", "axiom_if_adopted", "cost", "allowed_use", "current_recommendation"])}

## Claim Gates

{md_table(claim_rows, ["claim_gate_id", "claim", "condition_passed", "status", "blocks_claim", "claim_allowed"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{next(row["passed"] for row in validation if row["validation_id"] == "VAL2938_OVERALL")}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    identity_rows = residual_identity_rows()
    obstruction_rows_data = obstruction_rows()
    reference_rows = reference_contract_rows()
    first_value_rows = first_value_gate_rows()
    closure_rows_data = closure_rows()
    claim_rows = claim_gate_rows(theorem_rows, identity_rows, first_value_rows)
    decision = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem_rows)
    write_csv(OUTPUTS["identity"], identity_rows)
    write_csv(OUTPUTS["obstructions"], obstruction_rows_data)
    write_csv(OUTPUTS["reference"], reference_rows)
    write_csv(OUTPUTS["first_value"], first_value_rows)
    write_csv(OUTPUTS["closure"], closure_rows_data)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    shutil.copy2(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
    shutil.copy2(OUTPUTS["identity"], BRANCH_OUTPUTS["identity_copy"])
    shutil.copy2(OUTPUTS["first_value"], BRANCH_OUTPUTS["first_value_copy"])
    shutil.copy2(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])
    branch_rows = [
        add_common(
            {
                "copy_id": copy_id,
                "source_path": str(source_path),
                "copy_path": str(copy_path),
                "source_exists": source_path.exists(),
                "copy_exists": copy_path.exists(),
                "valid_for_claim": False,
            }
        )
        for copy_id, source_path, copy_path in [
            ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"]),
            ("identity_copy", OUTPUTS["identity"], BRANCH_OUTPUTS["identity_copy"]),
            ("first_value_copy", OUTPUTS["first_value"], BRANCH_OUTPUTS["first_value_copy"]),
            ("queue_copy", OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"]),
        ]
    ]
    write_csv(OUTPUTS["branches"], branch_rows)

    generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_exist = all(str(row["path_exists"]).lower() == "true" for row in source_rows)
    anchors_ok = all(str(row["anchors_found"]).lower() == "true" for row in source_rows)
    conditional_identity = any(row["theorem_id"] == "HWS2938_0_master_identity" and row["derivation_status"] == "EXACT_CONDITIONAL_GAUSS_HAMILTONIAN_IDENTITY" for row in theorem_rows)
    current_blocked = any(row["theorem_id"] == "HWS2938_6_verdict" and row["current_mts_status"] == "SOURCE_MEASURE_GLUE_NOT_DERIVED" for row in theorem_rows)
    identity_components_unfilled = any("MISSING" in row["current_status"] or "UNFILLED" in row["current_status"] or "UNSIGNED" in row["current_status"] or "NOT_DERIVED" in row["current_status"] for row in identity_rows)
    first_value_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" and "MISSING" in str(row["numeric_value"]) for row in first_value_rows)
    closure_labelled_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" and "no" in str(row["allowed_use"]).lower() or str(row["valid_for_claim"]).lower() == "false" for row in closure_rows_data)
    claims_blocked = all(str(row["claim_allowed"]).lower() == "false" for row in claim_rows)
    branches_exist = all(row["copy_exists"] for row in branch_rows)
    outputs_under_root = all(is_under(path, ROOT) for path in generated_csvs + [DOC])
    formalization_clean = not any(FORMALIZATION.rglob("*2938*")) if FORMALIZATION.exists() else True
    csvs_parse = all(csv_parses(path) for path in generated_csvs)

    validation = [
        {"validation_id": "VAL2938_0_sources_exist", "passed": sources_exist, "check": "all cited local source paths exist", "required": True},
        {"validation_id": "VAL2938_1_anchors_found", "passed": anchors_ok, "check": "all source anchors found", "required": True},
        {"validation_id": "VAL2938_2_conditional_identity", "passed": conditional_identity, "check": "conditional source-measure identity written", "required": True},
        {"validation_id": "VAL2938_3_current_blocked", "passed": current_blocked, "check": "current MTS source-measure claim remains blocked", "required": True},
        {"validation_id": "VAL2938_4_identity_components_unfilled", "passed": identity_components_unfilled, "check": "residual identity exposes unfilled components", "required": True},
        {"validation_id": "VAL2938_5_first_value_nonclaim", "passed": first_value_nonclaim, "check": "Qbar/tau/MHref first-value gates remain nonclaim", "required": True},
        {"validation_id": "VAL2938_6_closure_labelled_nonclaim", "passed": closure_labelled_nonclaim, "check": "closure axioms are labelled nonclaim", "required": True},
        {"validation_id": "VAL2938_7_claims_blocked", "passed": claims_blocked, "check": "no empirical/local-GR/Newton claim allowed", "required": True},
        {"validation_id": "VAL2938_8_branches_exist", "passed": branches_exist, "check": "branch copy files exist", "required": True},
        {"validation_id": "VAL2938_9_csvs_parse", "passed": csvs_parse, "check": "all generated CSV files parse", "required": True},
        {"validation_id": "VAL2938_10_outputs_under_post_checkpoint", "passed": outputs_under_root, "check": "all generated outputs are under post-checkpoint-work", "required": True},
        {"validation_id": "VAL2938_11_formalization_clean", "passed": formalization_clean, "check": "no 2938 outputs were written to formalization-workbench", "required": True},
    ]
    overall = all(row["passed"] is True for row in validation)
    validation.append({"validation_id": "VAL2938_OVERALL", "passed": overall, "check": "2938 validation overall", "required": True})
    validation = [add_common(row) for row in validation]
    write_csv(OUTPUTS["validation"], validation)
    write_doc(source_rows, theorem_rows, identity_rows, obstruction_rows_data, reference_rows, first_value_rows, closure_rows_data, claim_rows, decision, next_rows, branch_rows, validation)

    print(f"wrote {DOC}")
    print(f"validation overall: {overall}")


if __name__ == "__main__":
    main()
