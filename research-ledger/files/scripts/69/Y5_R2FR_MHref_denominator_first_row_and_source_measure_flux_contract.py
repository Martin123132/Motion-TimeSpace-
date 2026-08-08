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
QUARANTINE = MICROSCOPE / "quarantine" / "1652"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md"

SOURCE_FILES = {
    "1651_doc": ROOT / "1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md",
    "1651_validation": OUT / "P8_Y5_BRR545_1651_VALIDATION.csv",
    "1651_next": OUT / "P8_Y5_PARENT_QLOC_1651_NEXT_TARGET.csv",
    "1651_contract": OUT / "P8_Y5_PARENT_QLOC_1651_FIRST_SOURCE_ROW_CONTRACT.csv",
    "1651_refusal": OUT / "P8_Y5_PARENT_QLOC_1651_BOBS_PRIORITY_REFUSAL_RUNNER.csv",
    "1651_targets": OUT / "P8_Y5_PARENT_QLOC_1651_ACQUISITION_TARGETS.csv",
    "1644_mstar": OUT / "P8_Y5_PARENT_QLOC_1644_MSTAR_THEOREM_ATTEMPT.csv",
    "1644_denominator": OUT / "P8_Y5_PARENT_QLOC_1644_SAME_FRAME_DENOMINATOR_CLAUSE_MAP.csv",
    "1645_theorem": OUT / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv",
    "1645_schema": OUT / "P8_Y5_PARENT_QLOC_1645_MHREF_SOURCE_ROW_SCHEMA.csv",
    "1645_curl": OUT / "P8_Y5_PARENT_QLOC_1645_FIELD_SPACE_CURL_OBSTRUCTION.csv",
    "1647_fallback": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "1648_component": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "source_measure_theorem": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "source_measure_clauses": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
    "ham_source_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "ham_pim_test": OUT / "P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv",
    "source_measure_attempt": OUT / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "r10_source_pack": OUT / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
    "r10_bound_schema": OUT / "P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv",
    "r10_bound_runner": OUT / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv",
    "queue_1645_mhref": QUEUE / "JR1645_MHREF_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
    "queue_1651_contract": QUEUE / "JR1651_FIRST_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
}

NEEDLES = {
    "1651_doc": ["M_H_ref / Mstar_same_frame", "B_obs_source_measure_over_MH / Y5_projected_source_flux_over_MH"],
    "1651_validation": ["VAL1651_OVERALL", "PASS"],
    "1651_next": ["1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md", "source-measure flux contract"],
    "1651_contract": ["FSR1651_0_MHref_first", "FSR1651_1_source_measure_first"],
    "1651_refusal": ["RUN1651_0_MHref", "REFUSE_SCORING"],
    "1651_targets": ["AT1651_0_primary", "AT1651_1_coupling_lane"],
    "1644_mstar": ["MST1644_0_candidate_definition", "DEFINITION_GUARDRAIL_PASS_NONCLAIM"],
    "1644_denominator": ["MDC1644_6_poisson_gauss", "MISSING_BRIDGE"],
    "1645_theorem": ["HTM1645_5_verdict", "FAIL_CURRENT_CLAIM"],
    "1645_schema": ["MHS1645_0_M_H_ref", "MISSING_STABLE_MH_REF"],
    "1645_curl": ["ICO1645_5_curl_verdict", "NOT_PROVED_ZERO"],
    "1647_fallback": ["HSF1647_1_Y5_projected_source_flux", "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC"],
    "1648_component": ["BCF1648_2_source_measure_flux", "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC"],
    "source_measure_theorem": ["T509_1_flux_closure", "closure_not_derived_for_current_MTS"],
    "source_measure_clauses": ["SM509_3_flux_closure", "not_parent_derived"],
    "ham_source_contract": ["HSM541_1_integrable_charge", "not_derived_for_current_MTS"],
    "ham_pim_test": ["SMT540_1_charge_integrability", "not_derived_for_current_MTS"],
    "source_measure_attempt": ["SMT542_4_first_residual_trigger", "no source-backed B_zero_flux/Delta_symp row exists"],
    "r10_source_pack": ["BSM777_1_Cqmu_coefficient_input", "MISSING_NUMERIC_CQMU_OR_THEOREM_ZERO"],
    "r10_bound_schema": ["SMB778_1_numeric_bound_route", "schema_only"],
    "r10_bound_runner": ["SMR779_1_no_cancellation_bound", "blocked_missing_inputs"],
    "queue_1645_mhref": ["MHS1645_0_M_H_ref", "MISSING_STABLE_MH_REF"],
    "queue_1651_contract": ["FSR1651_0_MHref_first", "FSR1651_1_source_measure_first"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1652_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1652_INTAKE_SCAN.csv"
MHREF_FIRST_ROW_GATE = OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv"
SOURCE_MEASURE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1652_SOURCE_MEASURE_FLUX_CONTRACT.csv"
JOINT_ACCEPTANCE = OUT / "P8_Y5_PARENT_QLOC_1652_JOINED_ACCEPTANCE_MATRIX.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_SOURCE_MEASURE_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1652_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1652_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1652_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1652_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    MHREF_FIRST_ROW_GATE,
    SOURCE_MEASURE_CONTRACT,
    JOINT_ACCEPTANCE,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    INTAKE_SCAN,
    MHREF_FIRST_ROW_GATE,
    SOURCE_MEASURE_CONTRACT,
    JOINT_ACCEPTANCE,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    MHREF_FIRST_ROW_GATE: [
        QUARANTINE / "MHREF_FIRST_ROW_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_first_row_gate_nonclaim_1652.csv",
        QUEUE / "JR1652_MHREF_FIRST_ROW_GATE_NONCLAIM.csv",
    ],
    SOURCE_MEASURE_CONTRACT: [
        QUARANTINE / "SOURCE_MEASURE_FLUX_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_measure_flux_contract_nonclaim_1652.csv",
        QUEUE / "JR1652_SOURCE_MEASURE_FLUX_CONTRACT_NONCLAIM.csv",
    ],
    REFUSAL_RUNNER: [
        QUARANTINE / "MHREF_SOURCE_MEASURE_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_source_measure_refusal_runner_nonclaim_1652.csv",
        QUEUE / "JR1652_MHREF_SOURCE_MEASURE_REFUSAL_RUNNER_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1652.csv",
        QUEUE / "JR1652_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE, RAW, ACCEPTED]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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
        "score_allowed",
        "score_ready",
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
                "role": "1652 MHref denominator and source-measure flux joint gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1652_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1652_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1652_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        status = "QUEUE_PRESENT_NONCLAIM" if folder == QUEUE and csv_count else "NO_RAW_LIVE_ROWS" if folder == RAW and csv_count == 0 else "NO_ACCEPTED_LIVE_ROWS" if folder == ACCEPTED and csv_count == 0 else "LIVE_ROWS_REQUIRE_REVIEW"
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


def mhref_rows() -> list[dict[str, object]]:
    rows = [
        ("MHG1652_0_definition", "M_H_ref = H_tau[S_outer] - H_ref", "same-frame Hamiltonian/Noether source denominator", "DEFINITION_GUARDRAIL_ONLY", "definition exists but is not yet a source row"),
        ("MHG1652_1_parent_current", "Theta_total and Q_tau^MTS come from one parent action/current", "parent current owner", "MISSING_PARENT_THETA_QTAU", "H_tau is not computable without current owner"),
        ("MHG1652_2_integrability", "d_field alpha_tau = 0 on the allowed branch", "Hamiltonian charge integrability", "NOT_DERIVED", "field-space curl obstruction remains live"),
        ("MHG1652_3_reference", "H_ref fixed once and derivative-silent", "reference/counterterm lock", "NOT_DERIVED", "boundary/reference can move the denominator"),
        ("MHG1652_4_same_frame", "same tau/coframe/source surface for charge, clocks, PPN, orbit, boundary", "same observed frame lock", "UNSIGNED", "frame leakage can masquerade as source mass"),
        ("MHG1652_5_positive_finite", "0 < M_H_ref < infinity", "positive finite source mass", "NOT_DERIVED", "normalization can flip sign, vanish, or diverge"),
        ("MHG1652_6_poisson_gauss", "M_H_ref calibrates to Newtonian source monopole before orbital fitting", "Poisson/Gauss bridge", "MISSING_BRIDGE", "orbital GM import is refused"),
        ("MHG1652_7_first_row_verdict", "accept M_H_ref first source row", "all MHG1652_0..6 close or a source-backed finite row exists", "FIRST_ROW_NOT_ACCEPTED", "no parent-signed/source-backed denominator exists"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "clause": clause,
            "role": role,
            "status": status,
            "effect": effect,
            "required_columns": "system_id;tau_id;surface_outer;Q_tau_integral;H_tau;H_ref;M_H_ref;units;reference_rule;integrability_status;positivity_status;Poisson_Gauss_bridge;source_path;valid_for_claim",
            "denominator_ready": False,
            "source_ready": False,
            "valid_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, clause, role, status, effect in rows
    ]


def source_measure_rows() -> list[dict[str, object]]:
    rows = [
        ("SMF1652_0_coupling_descent", "ordinary matter/source/readout descends through one observed quotient geometry", "B_obs_source_measure theorem-zero route", "MISSING_COUPLING_DESCENT_INPUT", "without descent, source-measure flux can be a real coupling leak"),
        ("SMF1652_1_PiM_Ploc_owner", "Pi_M and P_loc are parent-owned projectors and commute with exterior/source split", "projected source current closure", "MISSING_PIM_PLOC_OWNER", "projector freedom can absorb failures"),
        ("SMF1652_2_radial_closure", "d(Pi_M J_H)=0 in compact source-free exterior", "Y5 projected source flux zero", "NOT_PARENT_DERIVED", "Y5_projected_source_flux_over_MH remains live"),
        ("SMF1652_3_Cqmu", "C_qmu q_loc/source-strength coefficient is zero or finite", "coupling coefficient row", "MISSING_NUMERIC_CQMU_OR_THEOREM_ZERO", "finite coupling coefficient needed for numeric bound"),
        ("SMF1652_4_flux_value", "source-measure flux value or zero theorem with units/source path", "B_obs_source_measure_over_MH numerator", "MISSING_SOURCE_FLUX_VALUE", "no source-backed flux row exists"),
        ("SMF1652_5_readout_response", "EM/clock/orbit/source-mass readouts use e_obs with no hidden representative map", "readout coupling response", "MISSING_READOUT_RESPONSE_INPUT", "readout leakage can mimic source-mass effects"),
        ("SMF1652_6_MHref_join", "source-measure numerator uses the same M_H_ref denominator", "normalization join", "BLOCKED_BY_MHREF", "cannot normalize source flux before denominator exists"),
        ("SMF1652_7_total", "B_obs_source_measure_over_MH total with no cancellation credit", "absolute coupling/source-measure budget", "MISSING_ALL_COMPONENTS_NO_CANCELLATION_TOTAL", "component rows cannot cancel unknowns"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "clause": clause,
            "role": role,
            "status": status,
            "effect": effect,
            "required_columns": "system_id;source_channel;matter_action_owner;Pi_M_owner;P_loc_owner;C_qmu;flux_value;M_H_ref;units;readout_response;source_path;zero_theorem_or_bound;valid_for_claim",
            "source_ready": False,
            "valid_for_runner": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, clause, role, status, effect in rows
    ]


def joint_rows() -> list[dict[str, object]]:
    rows = [
        ("JOIN1652_0_zero_zero", "M_H_ref parent-signed and source-measure flux theorem-zero", "ACCEPTABLE_FUTURE_ROUTE", "requires all denominator and source-measure clauses", "NOT_CURRENTLY_READY"),
        ("JOIN1652_1_numeric_denominator_zero_flux", "source-backed finite M_H_ref and source-measure zero theorem", "ACCEPTABLE_FUTURE_ROUTE", "needs M_H_ref row plus source-measure zero certificate", "NOT_CURRENTLY_READY"),
        ("JOIN1652_2_numeric_denominator_numeric_flux", "finite M_H_ref and finite absolute source flux", "ACCEPTABLE_FUTURE_BOUND_ROUTE", "requires units/source paths/no-cancellation and valid_for_claim true on every component", "NOT_CURRENTLY_READY"),
        ("JOIN1652_3_no_denominator", "source-measure flux row without M_H_ref", "REFUSE", "cannot normalize B_obs_source_measure_over_MH", "CURRENT_STATE"),
        ("JOIN1652_4_orbital_GM_denominator", "use observed orbital GM as denominator", "REFUSE", "would borrow Newtonian limit to prove Newtonian/local-GR limit", "FORBIDDEN_SHORTCUT"),
        ("JOIN1652_5_cancellation", "claim small total by cancelling unknown components", "REFUSE", "violates absolute no-cancellation policy", "FORBIDDEN_SHORTCUT"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "join_id": join_id,
            "case": case,
            "runner_decision": decision,
            "required_inputs": required_inputs,
            "current_status": status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for join_id, case, decision, required_inputs, status in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1652_0_MHref", "M_H_ref / Mstar_same_frame", "REFUSE_SCORING", "MISSING_PARENT_THETA_QTAU;MISSING_INTEGRABILITY;MISSING_REFERENCE_LOCK;MISSING_POSITIVITY;MISSING_POISSON_GAUSS;NO_ORBITAL_GM_IMPORT"),
        ("RUN1652_1_source_measure_zero", "B_obs_source_measure_over_MH zero theorem", "REFUSE_SCORING", "MISSING_COUPLING_DESCENT;MISSING_PIM_PLOC_OWNER;MISSING_SOURCE_MEASURE_SILENCE;MISSING_READOUT_RESPONSE"),
        ("RUN1652_2_source_measure_numeric", "B_obs_source_measure_over_MH finite bound", "REFUSE_SCORING", "MISSING_MHREF;MISSING_CQMU;MISSING_FLUX_VALUE;MISSING_UNITS;MISSING_SOURCE_PATH;NO_CANCELLATION_VECTOR_INCOMPLETE"),
        ("RUN1652_3_Y5_projected_flux", "Y5_projected_source_flux_over_MH", "REFUSE_SCORING", "MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC;MISSING_MHREF;MISSING_SOURCE_PATH"),
        ("RUN1652_4_joined_local", "local_GR_Newton_PPN", "REFUSE_SCORING", "MHREF_NOT_READY;SOURCE_MEASURE_NOT_READY;BOBS_TOTAL_MISSING;DELTAH_CURL_LIVE"),
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
        ("CG1652_0_MHref", "M_H_ref/Mstar first row accepted", False, "BLOCKED", "denominator clauses not parent-signed and no source row exists"),
        ("CG1652_1_source_measure", "source-measure/Y5 flux zero or finite bound accepted", False, "BLOCKED", "coupling descent/PiM/P_loc/flux rows missing"),
        ("CG1652_2_join", "source-measure flux can be normalized by M_H_ref", False, "REFUSED", "M_H_ref is not ready"),
        ("CG1652_3_local_GR", "local GR/Newton/PPN follows from 1652", False, "NO_CLAIM", "denominator and source-measure lane both refuse scoring"),
        ("CG1652_4_guardrail", "1652 joint gate installed", "INTERNAL_ONLY", "PASS_AS_INTERNAL_GUARDRAIL_ONLY", "guardrail is not evidence"),
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
        ("DEC1652_0_MHref", "MHREF_FIRST_ROW_NOT_ACCEPTED", "definition exists but current owner/integrability/reference/positivity/Poisson bridge are unsigned", "keep M_H_ref as the first acquisition target"),
        ("DEC1652_1_coupling", "SOURCE_MEASURE_FLUX_CONTRACT_NOT_READY", "source-measure theorem rows are conditional and Bobs pack lacks C_qmu/flux/readout inputs", "derive Pi_M/P_loc source-measure owner or source first coupling row"),
        ("DEC1652_2_join", "JOIN_REFUSES_WITHOUT_DENOMINATOR", "source-measure flux cannot be normalized without noncircular M_H_ref", "do not run local/PPN scoring"),
        ("DEC1652_3_next", "NEXT_1653_HTAU_QTAU_OR_SOURCE_MEASURE_OWNER_FIRST_ROW", "two shortest routes are parent current ownership for M_H_ref and Pi_M/P_loc source-measure owner for coupling", "select 1653 current/source-measure owner split gate"),
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
            "next_target": "1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md",
            "script": "scripts/Y5_R2FR_Htau_Qtau_current_owner_or_source_measure_owner_first_row.py",
            "objective": "try the two shortest parent-owner routes: derive Theta_total/Q_tau/M_H_ref current ownership, or derive Pi_M/P_loc source-measure owner; otherwise stage the first strict source rows for M_H_ref and B_obs_source_measure",
            "success_condition": "either parent current ownership or source-measure owner closes enough to create a valid first row, or both lanes hard-refuse with exact missing source fields",
            "forbidden_shortcuts": "no orbital-GM import; no M_H_ref without current/integrability/reference/positivity; no source-measure zero without Pi_M/P_loc owner; no cancellation; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, mhref, source_measure, joint, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1652_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1652 source paths exist and needles are present"),
        ("VAL1652_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1652_2_MHref_gate_complete", len(mhref) == 8 and any(row["status"] == "FIRST_ROW_NOT_ACCEPTED" for row in mhref), "M_H_ref first-row gate is complete and blocked"),
        ("VAL1652_3_source_measure_contract_complete", len(source_measure) == 8 and any(row["contract_id"] == "SMF1652_7_total" for row in source_measure), "source-measure/Y5 flux contract is complete"),
        ("VAL1652_4_join_refuses_shortcuts", any(row["join_id"] == "JOIN1652_4_orbital_GM_denominator" and row["runner_decision"] == "REFUSE" for row in joint) and any(row["join_id"] == "JOIN1652_5_cancellation" and row["runner_decision"] == "REFUSE" for row in joint), "joined runner refuses orbital-GM import and cancellation"),
        ("VAL1652_5_refusal_runner_blocks", len(refusal) == 5 and all(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks all current lanes"),
        ("VAL1652_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1652_7_next_target_selected", next_targets[0]["next_target"] == "1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md", "next target selects Htau/Qtau current owner or source-measure owner first row"),
        ("VAL1652_8_csv_parse", generated_csv_parse, "all generated 1652 CSVs parse"),
        ("VAL1652_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1652 generated rows keep MTS claim/no-score flags false"),
        ("VAL1652_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1652_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1652_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1652_13_formalization_untouched", not formalization_dirty, "no 1652 outputs found under formalization-workbench"),
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
            "check_id": "VAL1652_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1652 MHref denominator first row and source-measure flux contract validation",
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


def write_doc(source_rows, intake_rows, mhref, source_measure, joint, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1652 - MHref Denominator First Row And Source Measure Flux Contract

**Private status:** nonclaim joint gate. No `M_H_ref`, `M_*`, source-measure flux zero, `Y5_projected_source_flux`, `B_obs` bound, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1652` pairs the two things that cannot honestly be separated:

```text
M_H_ref = H_tau[S_outer] - H_ref
B_obs_source_measure_over_MH ~ source/projector/coupling flux divided by M_H_ref
```

The denominator route has a legal noncircular candidate, but no claim-ready row: parent current ownership, field-space integrability, fixed reference, positivity, same-frame lock, and Poisson/Gauss calibration are still unsigned.

The source-measure route is also only conditional: older source-measure files already state the right theorem, but `Pi_M/P_loc` ownership, radial closure, `C_qmu`, flux values, readout response, and no-cancellation accounting are missing.

So the joined runner refuses scoring. That is the correct result: a coupling/source-measure numerator without a same-frame Hamiltonian denominator is not a local-GR test; it is just a floating symbol.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## MHref First Row Gate

{markdown_table(mhref, ["gate_id", "clause", "role", "status", "effect"])}

## Source Measure Flux Contract

{markdown_table(source_measure, ["contract_id", "clause", "role", "status", "effect"])}

## Joined Acceptance Matrix

{markdown_table(joint, ["join_id", "case", "runner_decision", "required_inputs", "current_status"])}

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

This is the coupling bottleneck in its cleanest form. To make local GR derivable, MTS needs one parent-owned mass denominator and one parent-owned source-measure/projection law. If either remains a placeholder, every later PPN/Newton comparison is circular or unnormalised.
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
    mhref = mhref_rows()
    source_measure = source_measure_rows()
    joint = joint_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(INTAKE_SCAN, intake_rows)
    write_csv(MHREF_FIRST_ROW_GATE, mhref)
    write_csv(SOURCE_MEASURE_CONTRACT, source_measure)
    write_csv(JOINT_ACCEPTANCE, joint)
    write_csv(REFUSAL_RUNNER, refusal)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_targets)
    copy_outputs()

    validation = validation_rows(source_rows, intake_rows, mhref, source_measure, joint, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, mhref, source_measure, joint, refusal, claim, decisions, next_targets, validation)
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
