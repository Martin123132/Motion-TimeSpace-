from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1653"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md"

SOURCE_FILES = {
    "1652_doc": ROOT / "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
    "1652_validation": OUT / "P8_Y5_BRR545_1652_VALIDATION.csv",
    "1652_next": OUT / "P8_Y5_PARENT_QLOC_1652_NEXT_TARGET.csv",
    "1652_mhref_gate": OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv",
    "1652_source_measure_contract": OUT / "P8_Y5_PARENT_QLOC_1652_SOURCE_MEASURE_FLUX_CONTRACT.csv",
    "1652_refusal": OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_SOURCE_MEASURE_REFUSAL_RUNNER.csv",
    "1652_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1652_CLAIM_GATE.csv",
    "1645_theorem": OUT / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv",
    "1645_curl": OUT / "P8_Y5_PARENT_QLOC_1645_FIELD_SPACE_CURL_OBSTRUCTION.csv",
    "1645_schema": OUT / "P8_Y5_PARENT_QLOC_1645_MHREF_SOURCE_ROW_SCHEMA.csv",
    "1646_doc": ROOT / "1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
    "1646_current_owner": OUT / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "1646_qtau": OUT / "P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv",
    "1646_noether": OUT / "P8_Y5_PARENT_QLOC_1646_NOETHER_EXTRACTION_TEST.csv",
    "1646_deltaH_schema": OUT / "P8_Y5_PARENT_QLOC_1646_DELTAH_COMPONENT_SOURCE_SCHEMA.csv",
    "1646_validation": OUT / "P8_Y5_BRR545_1646_VALIDATION.csv",
    "1647_hybrid": OUT / "P8_Y5_PARENT_QLOC_1647_HYBRID_CURRENT_OWNER_AUDIT.csv",
    "1647_fallback": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "1648_flux_clause": OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
    "1648_component": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "source_measure_theorem": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "ham_pim_test": OUT / "P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv",
    "r10_source_pack": OUT / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
    "r10_bound_runner": OUT / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv",
    "queue_1652_mhref": QUEUE / "JR1652_MHREF_FIRST_ROW_GATE_NONCLAIM.csv",
    "queue_1652_source_measure": QUEUE / "JR1652_SOURCE_MEASURE_FLUX_CONTRACT_NONCLAIM.csv",
    "queue_1652_refusal": QUEUE / "JR1652_MHREF_SOURCE_MEASURE_REFUSAL_RUNNER_NONCLAIM.csv",
}

NEEDLES = {
    "1652_doc": ["M_H_ref = H_tau[S_outer] - H_ref", "older source-measure files"],
    "1652_validation": ["VAL1652_OVERALL", "PASS"],
    "1652_next": ["1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md", "source-measure owner"],
    "1652_mhref_gate": ["MHG1652_1_parent_current", "MISSING_PARENT_THETA_QTAU"],
    "1652_source_measure_contract": ["SMF1652_1_PiM_Ploc_owner", "MISSING_PIM_PLOC_OWNER"],
    "1652_refusal": ["RUN1652_0_MHref", "RUN1652_1_source_measure_zero"],
    "1652_claim_gate": ["CG1652_3_local_GR", "NO_CLAIM"],
    "1645_theorem": ["HTM1645_5_verdict", "FAIL_CURRENT_CLAIM"],
    "1645_curl": ["ICO1645_5_curl_verdict", "NOT_PROVED_ZERO"],
    "1645_schema": ["MHS1645_0_M_H_ref", "MISSING_STABLE_MH_REF"],
    "1646_doc": ["Theta_total/Q_tau^MTS", "Q_tau^MTS = Q_EH + Q_boundary/ref + Q_extra + Q_projector + C_matter/source"],
    "1646_current_owner": ["TQ1646_5_owner_verdict", "FAIL_CURRENT_CLAIM"],
    "1646_qtau": ["QTS1646_5_total", "NOT_PROMOTED"],
    "1646_noether": ["NET1646_4_verdict", "FAIL_CURRENT_CLAIM"],
    "1646_deltaH_schema": ["DHS1646_0_deltaH_curl", "SCHEMA_ONLY_MISSING_PARENT_CURRENT_OR_NUMERIC_SOURCE"],
    "1646_validation": ["VAL1646_OVERALL", "PASS"],
    "1647_hybrid": ["HCO1647_7_owner_verdict", "FAIL_CURRENT_CLAIM"],
    "1647_fallback": ["HSF1647_1_Y5_projected_source_flux", "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC"],
    "1648_flux_clause": ["OFC1648_4_source_measure_silence", "BLOCKED"],
    "1648_component": ["BCF1648_2_source_measure_flux", "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC"],
    "source_measure_theorem": ["T509_1_flux_closure", "closure_not_derived_for_current_MTS"],
    "ham_pim_test": ["SMT540_1_charge_integrability", "not_derived_for_current_MTS"],
    "r10_source_pack": ["BSM777_1_Cqmu_coefficient_input", "MISSING_NUMERIC_CQMU_OR_THEOREM_ZERO"],
    "r10_bound_runner": ["SMR779_1_no_cancellation_bound", "blocked_missing_inputs"],
    "queue_1652_mhref": ["MHG1652_1_parent_current", "MISSING_PARENT_THETA_QTAU"],
    "queue_1652_source_measure": ["SMF1652_1_PiM_Ploc_owner", "MISSING_PIM_PLOC_OWNER"],
    "queue_1652_refusal": ["RUN1652_0_MHref", "RUN1652_1_source_measure_zero"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1653_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1653_INTAKE_SCAN.csv"
CURRENT_OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1653_HTAU_QTAU_CURRENT_OWNER_GATE.csv"
SOURCE_MEASURE_OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1653_SOURCE_MEASURE_OWNER_GATE.csv"
FIRST_ROW_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1653_FIRST_SOURCE_ROW_LEDGER.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1653_OWNER_FIRST_ROW_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1653_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1653_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1653_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1653_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    CURRENT_OWNER_GATE,
    SOURCE_MEASURE_OWNER_GATE,
    FIRST_ROW_LEDGER,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CURRENT_OWNER_GATE,
    SOURCE_MEASURE_OWNER_GATE,
    FIRST_ROW_LEDGER,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CURRENT_OWNER_GATE: [
        QUARANTINE / "HTAU_QTAU_CURRENT_OWNER_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Htau_Qtau_current_owner_gate_nonclaim_1653.csv",
        QUEUE / "JR1653_HTAU_QTAU_CURRENT_OWNER_GATE_NONCLAIM.csv",
    ],
    SOURCE_MEASURE_OWNER_GATE: [
        QUARANTINE / "SOURCE_MEASURE_OWNER_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_measure_owner_gate_nonclaim_1653.csv",
        QUEUE / "JR1653_SOURCE_MEASURE_OWNER_GATE_NONCLAIM.csv",
    ],
    FIRST_ROW_LEDGER: [
        QUARANTINE / "FIRST_SOURCE_ROW_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_source_row_ledger_nonclaim_1653.csv",
        QUEUE / "JR1653_FIRST_SOURCE_ROW_LEDGER_NONCLAIM.csv",
    ],
    REFUSAL_RUNNER: [
        QUARANTINE / "OWNER_FIRST_ROW_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_owner_first_row_refusal_runner_nonclaim_1653.csv",
        QUEUE / "JR1653_OWNER_FIRST_ROW_REFUSAL_RUNNER_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1653.csv",
        QUEUE / "JR1653_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "denominator_ready",
        "first_row_ready",
        "owner_ready",
        "score_allowed",
        "score_ready",
        "source_measure_owner_ready",
        "source_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1653 Htau/Qtau current-owner or source-measure owner first-row gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1653_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1653_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1653_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        if folder == RAW and csv_count == 0:
            status = "NO_RAW_LIVE_ROWS"
        elif folder == ACCEPTED and csv_count == 0:
            status = "NO_ACCEPTED_LIVE_ROWS"
        elif folder == QUEUE and csv_count:
            status = "QUEUE_PRESENT_NONCLAIM"
        else:
            status = "LIVE_ROWS_REQUIRE_REVIEW"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": role,
                "folder_path": str(folder),
                "csv_count": csv_count,
                "status": status,
                "source_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def current_owner_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "HTO1653_0_parent_action_current",
            "one explicit L_parent owns EH, matter, extra fields, boundary/reference, tau, and coupling sectors",
            "delta L_parent = E_A delta Phi^A + dTheta_total",
            "TEMPLATE_AVAILABLE_NOT_CURRENT_OWNER",
            "no single parent current-chain has been varied with every retained sector",
        ),
        (
            "HTO1653_1_Qtau_extraction",
            "Q_tau^MTS is extracted from the same Theta_total",
            "J_tau = Theta_total(Phi,L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau",
            "FORMAL_SHAPE_AVAILABLE_NOT_CERTIFICATE",
            "Q_extra, Q_projector, boundary/reference, and matter-source terms remain unowned or unglued",
        ),
        (
            "HTO1653_2_integrability_reference",
            "Hamiltonian one-form is closed with fixed reference subtraction",
            "d_field integral_S(delta Q_tau - i_tau Theta_total)=0 and delta H_ref=0",
            "NOT_DERIVED",
            "field-space curl and reference-lock obstruction remain live",
        ),
        (
            "HTO1653_3_MHref_denominator",
            "M_H_ref is a positive finite same-frame source denominator",
            "M_H_ref = H_tau[S_outer] - H_ref with 0 < M_H_ref < infinity",
            "NO_FIRST_ROW",
            "no parent-signed or source-backed denominator row exists",
        ),
        (
            "HTO1653_4_Poisson_Gauss_bridge",
            "Hamiltonian source charge calibrates to Newtonian source monopole before orbital fitting",
            "lim_local exterior integral_S Q_tau = G_ref M_source without importing observed orbital GM",
            "MISSING_BRIDGE",
            "using orbital GM as denominator is circular and remains refused",
        ),
        (
            "HTO1653_5_owner_verdict",
            "accept Theta_total/Q_tau/M_H_ref owner chain",
            "HTO1653_0 through HTO1653_4 all pass together",
            "OWNER_NOT_ACCEPTED",
            "current-owner route is alive as a formal contract but not closed for present MTS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "needed_object": needed_object,
            "owner_test": owner_test,
            "current_status": status,
            "blocker": blocker,
            "required_first_row_fields": "system_id;tau_id;surface_outer;L_parent_id;Theta_total_id;Q_tau_integral;H_tau;H_ref;M_H_ref;units;reference_rule;integrability_status;positivity_status;Poisson_Gauss_bridge;source_path;valid_for_claim",
            "owner_ready": False,
            "denominator_ready": False,
            "first_row_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, needed_object, owner_test, status, blocker in rows
    ]


def source_measure_owner_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SMO1653_0_coupling_descent",
            "ordinary matter/source/readout uses one observed quotient geometry",
            "S_matter = Sbar[q(Phi), Psi, theta] with no representative marker in readouts",
            "MISSING_COUPLING_DESCENT_INPUT",
            "matter/readout leakage can masquerade as source-measure flux",
        ),
        (
            "SMO1653_1_PiM_owner",
            "Pi_M is selected by the parent current or source measure, not by later fitting",
            "Pi_M J_H is the parent-owned mass-source current",
            "MISSING_PIM_OWNER",
            "source mass projector remains adjustable",
        ),
        (
            "SMO1653_2_Ploc_owner",
            "P_loc is the parent-owned local projection/readout map",
            "P_loc commutes with source/exterior split and observed readout",
            "MISSING_PLOC_OWNER",
            "local projection can absorb residual coupling",
        ),
        (
            "SMO1653_3_commutator_closure",
            "projected source current is closed in compact source-free exterior",
            "d(Pi_M J_H)=0 or abs(integral_A d(Pi_M J_H))/M_H_ref is source bounded",
            "NOT_PARENT_DERIVED",
            "Y5 projected source flux remains live",
        ),
        (
            "SMO1653_4_Cqmu_flux_readout",
            "C_qmu, source-measure flux, and readout response are zero or numeric with units",
            "abs(B_source_measure)/M_H_ref <= sourced no-cancellation component sum",
            "MISSING_NUMERIC_OR_ZERO_ROWS",
            "B_obs source-measure channel cannot be scored",
        ),
        (
            "SMO1653_5_MHref_join",
            "source-measure numerator uses the same M_H_ref denominator",
            "B_obs_source_measure_over_MH is normalized by the 1653 M_H_ref row",
            "BLOCKED_BY_MHREF",
            "source-measure owner cannot stand alone without the Hamiltonian denominator",
        ),
        (
            "SMO1653_6_owner_verdict",
            "accept Pi_M/P_loc/source-measure owner chain",
            "SMO1653_0 through SMO1653_5 all pass together",
            "OWNER_NOT_ACCEPTED",
            "source-measure route is a precise contract but not currently closed",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "needed_object": needed_object,
            "owner_test": owner_test,
            "current_status": status,
            "blocker": blocker,
            "required_first_row_fields": "system_id;source_channel;matter_action_owner;Pi_M_owner;P_loc_owner;commutator_status;C_qmu;flux_value;M_H_ref;units;readout_response;source_path;zero_theorem_or_bound;valid_for_claim",
            "source_measure_owner_ready": False,
            "source_ready": False,
            "first_row_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, needed_object, owner_test, status, blocker in rows
    ]


def first_row_ledger_rows() -> list[dict[str, object]]:
    rows = [
        (
            "FSR1653_0_MHref_parent_certificate",
            "Theta_total_Qtau_MHref_owner_certificate",
            "explicit parent action/current certificate for M_H_ref",
            "L_parent_id;Theta_total_id;Q_tau_id;tau_id;surface_outer;H_tau;H_ref;M_H_ref;units;reference_rule;integrability_status;positivity_status;Poisson_Gauss_bridge;source_path;valid_for_claim",
            "MISSING_PARENT_THETA_QTAU;MISSING_INTEGRABILITY;MISSING_REFERENCE_LOCK;MISSING_POSITIVITY;MISSING_POISSON_GAUSS",
        ),
        (
            "FSR1653_1_MHref_source_row",
            "M_H_ref_numeric_or_symbolic_source_row",
            "finite same-frame source denominator if parent certificate is not yet closed",
            "system_id;tau_id;surface_outer;H_tau;H_ref;M_H_ref;uncertainty;units;reference_rule;same_frame_lock;source_path;valid_for_claim",
            "MISSING_H_TAU;MISSING_H_REF;MISSING_MHREF_VALUE;MISSING_UNITS;MISSING_SOURCE_PATH;NO_ORBITAL_GM_IMPORT",
        ),
        (
            "FSR1653_2_Bobs_zero_certificate",
            "B_obs_source_measure_zero_certificate",
            "parent-owned zero theorem for source-measure leakage",
            "system_id;matter_action_owner;Pi_M_owner;P_loc_owner;commutator_status;readout_response;zero_theorem;source_path;valid_for_claim",
            "MISSING_COUPLING_DESCENT;MISSING_PIM_OWNER;MISSING_PLOC_OWNER;MISSING_SOURCE_MEASURE_SILENCE;MISSING_READOUT_RESPONSE",
        ),
        (
            "FSR1653_3_Bobs_numeric_bound",
            "B_obs_source_measure_numeric_no_cancellation_bound",
            "finite absolute component bound if zero theorem fails",
            "component_id;C_qmu;flux_value;readout_coefficient;M_H_ref;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "MISSING_MHREF;MISSING_CQMU;MISSING_FLUX_VALUE;MISSING_READOUT_COEFFICIENT;MISSING_UNITS;MISSING_SOURCE_PATH;NO_CANCELLATION_VECTOR_INCOMPLETE",
        ),
        (
            "FSR1653_4_Y5_projected_source_flux",
            "Y5_projected_source_flux_over_MH",
            "projected source current zero or bounded across the exterior annulus",
            "system_id;annulus;Pi_M_owner;P_loc_owner;flux_value;M_H_ref;units;source_path;valid_for_claim",
            "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC;MISSING_PLOC_OWNER;MISSING_MHREF;MISSING_SOURCE_PATH",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target_quantity": target_quantity,
            "purpose": purpose,
            "required_columns": required_columns,
            "missing_fields": missing_fields,
            "row_status": "STRICT_TEMPLATE_ONLY_NOT_ACCEPTED",
            "accepted_for_scoring": False,
            "first_row_ready": False,
            "valid_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, target_quantity, purpose, required_columns, missing_fields in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RUN1653_0_current_owner",
            "Theta_total/Q_tau/M_H_ref owner chain",
            "REFUSE_SCORING",
            "MISSING_PARENT_THETA_QTAU;MISSING_QTAU_EXTRA_PROJECTOR_MATTER_OWNER;MISSING_INTEGRABILITY;MISSING_REFERENCE_LOCK;MISSING_POSITIVITY;MISSING_POISSON_GAUSS",
        ),
        (
            "RUN1653_1_source_measure_owner",
            "Pi_M/P_loc/source-measure owner chain",
            "REFUSE_SCORING",
            "MISSING_COUPLING_DESCENT;MISSING_PIM_OWNER;MISSING_PLOC_OWNER;MISSING_PROJECTOR_COMMUTATOR_CLOSURE;MISSING_CQMU_FLUX_READOUT;BLOCKED_BY_MHREF",
        ),
        (
            "RUN1653_2_MHref_first_row",
            "M_H_ref / Mstar_same_frame first row",
            "REFUSE_SCORING",
            "MISSING_PARENT_CERTIFICATE_OR_SOURCE_ROW;NO_ORBITAL_GM_IMPORT",
        ),
        (
            "RUN1653_3_Bobs_first_row",
            "B_obs_source_measure_over_MH first row",
            "REFUSE_SCORING",
            "MISSING_ZERO_CERTIFICATE_OR_NUMERIC_NO_CANCELLATION_BOUND;MISSING_MHREF",
        ),
        (
            "RUN1653_4_joined_local",
            "local_GR_Newton_PPN_R10_WEP",
            "REFUSE_SCORING",
            "CURRENT_OWNER_NOT_ACCEPTED;SOURCE_MEASURE_OWNER_NOT_ACCEPTED;FIRST_ROWS_NOT_ACCEPTED;NO_LOCAL_CLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "quantity": quantity,
            "runner_decision": decision,
            "refusal_reasons": refusal_reasons,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, quantity, decision, refusal_reasons in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1653_0_current_owner", "Theta_total/Q_tau/M_H_ref chain is parent-owned", False, "BLOCKED", "current owner remains unsigned"),
        ("CG1653_1_source_measure_owner", "Pi_M/P_loc/source-measure chain is parent-owned", False, "BLOCKED", "projector/source-measure owner remains unsigned"),
        ("CG1653_2_first_rows", "M_H_ref and B_obs first rows are accepted", False, "BLOCKED", "strict rows are templates only"),
        ("CG1653_3_local_GR", "local GR/Newton/PPN/R10/WEP follows from 1653", False, "NO_CLAIM", "both owner lanes and first rows refuse scoring"),
        ("CG1653_4_guardrail", "1653 owner/first-row split gate installed", "INTERNAL_ONLY", "PASS_AS_INTERNAL_GUARDRAIL_ONLY", "guardrail is not evidence"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DEC1653_0_current_owner",
            "CURRENT_OWNER_ROUTE_NOT_CLOSED",
            "the parent-current formulae are right, but present files do not supply one varied current-chain for all retained sectors",
            "keep H_tau/Q_tau/M_H_ref as a first-row target, not a claim",
        ),
        (
            "DEC1653_1_source_measure_owner",
            "SOURCE_MEASURE_OWNER_ROUTE_NOT_CLOSED",
            "Pi_M/P_loc, commutator closure, coupling descent, C_qmu, flux, and readout response are not parent-signed",
            "treat B_obs as the coupling bottleneck and require zero certificate or numeric no-cancellation bound",
        ),
        (
            "DEC1653_2_first_rows",
            "STRICT_FIRST_ROW_TEMPLATES_STAGED",
            "both derivation lanes now have exact missing-field ledgers",
            "next work should try to fill one strict row rather than reopen broad local-GR scoring",
        ),
        (
            "DEC1653_3_next",
            "NEXT_1654_PROJECTOR_COMMUTATOR_OR_FIRST_ROW_FILL",
            "the smallest noncircular progress is either Pi_M/P_loc commutator ownership or a sourced M_H_ref/B_obs row",
            "select 1654 projector-commutator owner or first strict source-row fill runner",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1654-Y5-R2FR-PiM-Ploc-commutator-owner-or-first-strict-source-row-fill.md",
            "script": "scripts/Y5_R2FR_PiM_Ploc_commutator_owner_or_first_strict_source_row_fill.py",
            "objective": "try the smallest noncircular closure: prove Pi_M/P_loc projector commutator ownership for source-measure flux, or fill one strict M_H_ref/B_obs source row with real fields; otherwise hard-refuse with missing inputs",
            "success_condition": "one owner certificate or one first row becomes source-backed and valid_for_claim=true, or every row remains valid_for_claim=false with exact missing-field blockers",
            "forbidden_shortcuts": "no orbital-GM import; no source-measure zero without Pi_M/P_loc owner; no B_obs scoring without M_H_ref; no cancellation; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, current_owner, source_owner, first_rows, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1653_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1653 source paths exist and needles are present"),
        ("VAL1653_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1653_2_current_owner_blocked", len(current_owner) == 6 and any(row["current_status"] == "OWNER_NOT_ACCEPTED" for row in current_owner), "Htau/Qtau/MHref current-owner route is explicit and blocked"),
        ("VAL1653_3_source_measure_owner_blocked", len(source_owner) == 7 and any(row["current_status"] == "OWNER_NOT_ACCEPTED" for row in source_owner), "Pi_M/P_loc/source-measure owner route is explicit and blocked"),
        ("VAL1653_4_first_rows_staged", len(first_rows) == 5 and all(row["row_status"] == "STRICT_TEMPLATE_ONLY_NOT_ACCEPTED" for row in first_rows), "strict M_H_ref and B_obs first-row ledgers are staged as nonclaim"),
        ("VAL1653_5_refusal_runner_blocks", len(refusal) == 5 and all(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks all current lanes"),
        ("VAL1653_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1653_7_next_target_selected", next_targets[0]["next_target"] == "1654-Y5-R2FR-PiM-Ploc-commutator-owner-or-first-strict-source-row-fill.md", "next target selects projector commutator owner or first strict source-row fill"),
        ("VAL1653_8_csv_parse", generated_csv_parse, "all generated 1653 CSVs parse"),
        ("VAL1653_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1653 generated rows keep MTS claim/no-score flags false"),
        ("VAL1653_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1653_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1653_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1653_13_formalization_untouched", not formalization_dirty, "no 1653 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1653_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1653 Htau/Qtau current-owner or source-measure owner first-row validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, intake_rows, current_owner, source_owner, first_rows, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1653 - Htau Qtau Current Owner Or Source Measure Owner First Row

**Private status:** nonclaim owner/first-row split gate. No `Theta_total`, `Q_tau^MTS`, `M_H_ref`, source-measure flux zero, `B_obs_source_measure_over_MH`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

`1653` tests the two shortest noncircular routes left after `1652`:

```text
Route A: L_parent -> Theta_total -> Q_tau^MTS -> H_tau -> M_H_ref
Route B: S_matter/Pi_M/P_loc descent -> d(Pi_M J_H)=0 or B_obs_source_measure/M_H bound
```

Both routes are formally sharp, but neither is closed in the current corpus. The current-owner lane still lacks one parent current that owns all retained sectors, integrability, fixed reference, positivity, and the Poisson/Gauss bridge. The source-measure lane still lacks coupling descent, parent-owned `Pi_M/P_loc`, projector commutator closure, `C_qmu`, source flux/readout rows, and the same `M_H_ref` denominator.

So `1653` does not demote the route; it demotes the claim. The useful gain is that the missing object is now precise: either a parent-owned projector/current certificate, or one strict source-backed `M_H_ref`/`B_obs` first row.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Htau/Qtau Current Owner Gate

{markdown_table(current_owner, ["gate_id", "needed_object", "owner_test", "current_status", "blocker"])}

## Source Measure Owner Gate

{markdown_table(source_owner, ["gate_id", "needed_object", "owner_test", "current_status", "blocker"])}

## First Source Row Ledger

{markdown_table(first_rows, ["row_id", "target_quantity", "purpose", "missing_fields", "row_status"])}

## Refusal Runner

{markdown_table(refusal, ["run_id", "quantity", "runner_decision", "refusal_reasons"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The coupling hunch survives this pass, but in a stricter form: the missing coupling is not merely a coefficient. It is the parent-owned map that makes the source numerator and Hamiltonian mass denominator live in the same geometry. Until that map is signed, local-GR scoring is premature. The best next shot is narrow and mechanical: prove the `Pi_M/P_loc` commutator/source-owner clause, or fill one strict source row without borrowing orbital `GM`.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    intake_rows = intake_scan_rows()
    current_owner = current_owner_gate_rows()
    source_owner = source_measure_owner_gate_rows()
    first_rows = first_row_ledger_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (INTAKE_SCAN, intake_rows),
        (CURRENT_OWNER_GATE, current_owner),
        (SOURCE_MEASURE_OWNER_GATE, source_owner),
        (FIRST_ROW_LEDGER, first_rows),
        (REFUSAL_RUNNER, refusal),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, intake_rows, current_owner, source_owner, first_rows, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, current_owner, source_owner, first_rows, refusal, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1653 validation failed; see P8_Y5_BRR545_1653_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1653 validation PASS")


if __name__ == "__main__":
    main()
