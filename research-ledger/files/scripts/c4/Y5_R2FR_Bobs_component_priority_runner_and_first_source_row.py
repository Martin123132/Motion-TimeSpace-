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
QUARANTINE = MICROSCOPE / "quarantine" / "1651"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md"

SOURCE_FILES = {
    "1650_doc": ROOT / "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
    "1650_validation": OUT / "P8_Y5_BRR545_1650_VALIDATION.csv",
    "1650_next": OUT / "P8_Y5_PARENT_QLOC_1650_NEXT_TARGET.csv",
    "1650_parent": OUT / "P8_Y5_PARENT_QLOC_1650_PARENT_SIGNATURE_VERDICT.csv",
    "1650_priority": OUT / "P8_Y5_PARENT_QLOC_1650_BOBS_SOURCE_ACQUISITION_PRIORITY.csv",
    "1650_local": OUT / "P8_Y5_PARENT_QLOC_1650_LOCAL_GR_STATUS_LEDGER.csv",
    "1649_schema": OUT / "P8_Y5_PARENT_QLOC_1649_BOBS_INPUT_RUNNER_SCHEMA.csv",
    "1648_component_fill": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "1648_dryrun": OUT / "P8_Y5_PARENT_QLOC_1648_BOBS_INPUT_RUNNER_DRYRUN.csv",
    "1647_fallback": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "1644_denominator": OUT / "P8_Y5_PARENT_QLOC_1644_SAME_FRAME_DENOMINATOR_CLAUSE_MAP.csv",
    "1643_inputs": OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_INPUT_STATUS.csv",
    "1640_boundary": OUT / "P8_Y5_PARENT_QLOC_1640_BOUNDARY_SILENCE_CLAUSE_LEDGER.csv",
    "1646_deltaH_schema": OUT / "P8_Y5_PARENT_QLOC_1646_DELTAH_COMPONENT_SOURCE_SCHEMA.csv",
    "queue_1649_bobs": QUEUE / "JR1649_BOBS_INPUT_RUNNER_SCHEMA_NONCLAIM.csv",
    "queue_1650_priority": QUEUE / "JR1650_BOBS_SOURCE_ACQUISITION_PRIORITY_NONCLAIM.csv",
}

NEEDLES = {
    "1650_doc": ["The next concrete move is an executable `B_obs` priority runner", "1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md"],
    "1650_validation": ["VAL1650_OVERALL", "PASS"],
    "1650_next": ["1651-Y5-R2FR-Bobs-component-priority-runner-and-first-source-row.md", "first-source-row runner"],
    "1650_parent": ["PSV1650_7_verdict", "PARENT_OWNER_NOT_CLOSED_CURRENT_CORPUS"],
    "1650_priority": ["BPA1650_0_denominator", "M_H_ref / Mstar_same_frame"],
    "1650_local": ["LGR1650_4_current_position", "PROMISING_BUT_NOT_CLAIMABLE"],
    "1649_schema": ["BIR1649_5_total_Bobs", "MISSING_COMPONENTS"],
    "1648_component_fill": ["BCF1648_5_total_B_observed", "MISSING_COMPONENTS"],
    "1648_dryrun": ["BIR1648_0_no_candidate", "BLOCKED_MISSING_COMPONENTS"],
    "1647_fallback": ["HSF1647_0_observed_reduced_boundary_flux", "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC"],
    "1644_denominator": ["MDC1644_6_poisson_gauss", "MISSING_BRIDGE"],
    "1643_inputs": ["IN1643_2_Mstar_same_frame", "MISSING_SAME_FRAME_PARENT_SOURCE_MASS"],
    "1640_boundary": ["BSC1640_5_all_clauses", "FAIL_CURRENT_PROOF"],
    "1646_deltaH_schema": ["DHS1646_0_deltaH_curl", "SCHEMA_ONLY_MISSING_PARENT_CURRENT_OR_NUMERIC_SOURCE"],
    "queue_1649_bobs": ["BIR1649_5_total_Bobs", "MISSING_COMPONENTS"],
    "queue_1650_priority": ["BPA1650_0_denominator", "M_H_ref / Mstar_same_frame"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1651_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1651_INTAKE_SCAN.csv"
RUNNER_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1651_BOBS_PRIORITY_RUNNER_INPUTS.csv"
FIRST_SOURCE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1651_FIRST_SOURCE_ROW_CONTRACT.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1651_BOBS_PRIORITY_REFUSAL_RUNNER.csv"
ACQUISITION_TARGETS = OUT / "P8_Y5_PARENT_QLOC_1651_ACQUISITION_TARGETS.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1651_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1651_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1651_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1651_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    RUNNER_INPUTS,
    FIRST_SOURCE_CONTRACT,
    REFUSAL_RUNNER,
    ACQUISITION_TARGETS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    INTAKE_SCAN,
    RUNNER_INPUTS,
    FIRST_SOURCE_CONTRACT,
    REFUSAL_RUNNER,
    ACQUISITION_TARGETS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    RUNNER_INPUTS: [
        QUARANTINE / "BOBS_PRIORITY_RUNNER_INPUTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Bobs_priority_runner_inputs_nonclaim_1651.csv",
        QUEUE / "JR1651_BOBS_PRIORITY_RUNNER_INPUTS_NONCLAIM.csv",
    ],
    FIRST_SOURCE_CONTRACT: [
        QUARANTINE / "FIRST_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_source_row_contract_nonclaim_1651.csv",
        QUEUE / "JR1651_FIRST_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
    ],
    REFUSAL_RUNNER: [
        QUARANTINE / "BOBS_PRIORITY_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Bobs_priority_refusal_runner_nonclaim_1651.csv",
        QUEUE / "JR1651_BOBS_PRIORITY_REFUSAL_RUNNER_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1651.csv",
        QUEUE / "JR1651_NEXT_TARGET_NONCLAIM.csv",
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
        "score_allowed",
        "score_ready",
        "source_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
        "valid_prediction_row",
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
                "role": "1651 Bobs priority runner and first source-row contract",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1651_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1651_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1651_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, folder_role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        if folder == RAW:
            status = "NO_RAW_LIVE_ROWS" if csv_count == 0 else "RAW_ROWS_PRESENT_REVIEW_REQUIRED"
        elif folder == ACCEPTED:
            status = "NO_ACCEPTED_LIVE_ROWS" if csv_count == 0 else "ACCEPTED_ROWS_PRESENT_REVIEW_REQUIRED"
        else:
            status = "QUEUE_PRESENT_NONCLAIM" if csv_count > 0 else "QUEUE_EMPTY"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": folder_role,
                "folder_path": str(folder),
                "csv_count": csv_count,
                "status": status,
                "source_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_input_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BRI1651_0_MHref",
            "M_H_ref / Mstar_same_frame",
            "denominator",
            "M_H_ref = H_tau[S_outer] - H_ref with integrability, fixed reference, positivity, and Poisson/Gauss bridge",
            "MISSING_STABLE_MH_REF",
            "blocks all normalized Bobs/PiR/qR rows",
            0,
        ),
        (
            "BRI1651_1_source_measure",
            "B_obs_source_measure_over_MH; Y5_projected_source_flux_over_MH",
            "source/coupling numerator",
            "source-measure silence or finite projected source flux with Pi_M/P_loc owner and M_H_ref",
            "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC",
            "coupling/source normalization leak",
            1,
        ),
        (
            "BRI1651_2_boundary",
            "B_obs_boundary_improvement_over_MH; Pi_R_boundary_abs; B_zero_flux",
            "boundary numerator",
            "proper/exact boundary theorem or source-backed boundary flux/reciprocal momentum with M_H_ref",
            "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC",
            "direct Q_R/Pi_R hair route",
            2,
        ),
        (
            "BRI1651_3_projector",
            "B_obs_projector_commutator_over_MH",
            "projector numerator",
            "parent-owned P_loc/Pi_M descent or finite commutator bound",
            "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC",
            "prevents projection smuggling",
            3,
        ),
        (
            "BRI1651_4_bulk",
            "B_obs_bulk_Euler_over_MH",
            "bulk Euler numerator",
            "parent-owned S_red/Gamma_eff/K_hat action and on-shell reduced fields or finite bound",
            "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC",
            "keeps derivation route alive",
            4,
        ),
        (
            "BRI1651_5_corner_tau",
            "B_obs_corner_edge_over_MH; tau_ref_surface_mismatch_over_MH",
            "corner/tau/reference numerator",
            "corner-edge theorem, same tau/surface/reference lock, or finite mismatch bound",
            "MISSING_OBSERVED_EDGE_ZERO_OR_NUMERIC",
            "stops boundary bookkeeping mass shifts",
            5,
        ),
        (
            "BRI1651_6_total",
            "B_observed_reduced_flux_over_MH; delta_H_tau_nonintegrable_over_MH",
            "total no-cancellation residual",
            "all component rows source-backed/theorem-zero with M_H_ref and no cancellation credit",
            "MISSING_COMPONENTS",
            "only total can feed a local/PPN runner",
            6,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_input_id": runner_input_id,
            "quantity": quantity,
            "input_class": input_class,
            "acceptance_requirement": acceptance_requirement,
            "current_status": current_status,
            "why_needed": why_needed,
            "priority_rank": priority_rank,
            "source_ready": False,
            "valid_for_runner": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_input_id, quantity, input_class, acceptance_requirement, current_status, why_needed, priority_rank in rows
    ]


def first_source_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "FSR1651_0_MHref_first",
            "M_H_ref / Mstar_same_frame",
            "system_id;surface_id;tau_id;H_tau_or_zero_theorem;H_ref;M_H_ref_value;units;positivity_status;integrability_status;Poisson_Gauss_bridge;source_path;valid_for_claim",
            "parent-signed Hamiltonian source charge or source-backed finite positive denominator",
            "MISSING_MHREF_SOURCE_ROW",
            "1652 primary",
        ),
        (
            "FSR1651_1_source_measure_first",
            "B_obs_source_measure_over_MH / Y5_projected_source_flux_over_MH",
            "system_id;annulus;Pi_M_owner;P_loc_owner;source_measure_rule;flux_value;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "source-measure theorem zero or finite source/projector flux bound",
            "MISSING_SOURCE_MEASURE_ROW",
            "1652 secondary / coupling lane",
        ),
        (
            "FSR1651_2_boundary_first",
            "B_obs_boundary_improvement_over_MH / Pi_R_boundary_abs",
            "system_id;surface_id;boundary_class;B_GK_component;Pi_R_boundary_abs;B_zero_flux;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "proper/exact boundary theorem or finite boundary/reciprocal momentum bound",
            "MISSING_BOUNDARY_ROW",
            "1652 tertiary",
        ),
        (
            "FSR1651_3_projector_support",
            "B_obs_projector_commutator_over_MH",
            "projector_id;domain;commutator_value;Pi_M_owner;P_loc_owner;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "parent projector descent theorem or finite commutator bound",
            "MISSING_PROJECTOR_ROW",
            "support row",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "quantity": quantity,
            "required_columns": required_columns,
            "acceptance_rule": acceptance_rule,
            "current_status": current_status,
            "lane": lane,
            "source_ready": False,
            "valid_for_runner": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, quantity, required_columns, acceptance_rule, current_status, lane in rows
    ]


def refusal_runner_rows() -> list[dict[str, object]]:
    refusal_base = "MISSING_SOURCE_PATH;MISSING_NUMERIC_OR_THEOREM_ZERO_VALUE;MISSING_UNITS;MISSING_PARENT_SIGNATURE;VALID_FOR_CLAIM_FALSE"
    rows = [
        ("RUN1651_0_MHref", "M_H_ref / Mstar_same_frame", "REFUSE_SCORING", refusal_base + ";MISSING_INTEGRABILITY_REFERENCE_POSITIVITY_POISSON_GAUSS"),
        ("RUN1651_1_source_measure", "B_obs_source_measure_over_MH; Y5_projected_source_flux_over_MH", "REFUSE_SCORING", refusal_base + ";MISSING_MHREF;MISSING_PIM_PLOC_OWNER"),
        ("RUN1651_2_boundary", "B_obs_boundary_improvement_over_MH; Pi_R_boundary_abs", "REFUSE_SCORING", refusal_base + ";MISSING_MHREF;MISSING_BOUNDARY_CLASS_ZERO"),
        ("RUN1651_3_projector", "B_obs_projector_commutator_over_MH", "REFUSE_SCORING", refusal_base + ";MISSING_MHREF;MISSING_PROJECTOR_DESCENT"),
        ("RUN1651_4_bulk", "B_obs_bulk_Euler_over_MH", "REFUSE_SCORING", refusal_base + ";MISSING_REDUCED_ACTION_OWNER"),
        ("RUN1651_5_total", "B_observed_reduced_flux_over_MH; delta_H_tau_nonintegrable_over_MH", "REFUSE_SCORING", "MISSING_COMPONENTS;MISSING_MHREF;NO_CANCELLATION_VECTOR_INCOMPLETE;VALID_FOR_CLAIM_FALSE"),
        ("RUN1651_6_local_GR", "local_GR_Newton_PPN", "REFUSE_SCORING", "B_OBS_NOT_SOURCE_READY;MHREF_NOT_SOURCE_READY;PIR_QR_BRANCH_NOT_ZERO_OR_BOUNDED;NO_CANCELLATION_VECTOR_INCOMPLETE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "quantity": quantity,
            "runner_decision": runner_decision,
            "refusal_reasons": refusal_reasons,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, quantity, runner_decision, refusal_reasons in rows
    ]


def acquisition_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "AT1651_0_primary",
            "M_H_ref / Mstar_same_frame",
            "derive/source same-frame Hamiltonian denominator first",
            "every Bobs and Pi_R/q_R normalized bound needs a noncircular positive source mass",
            "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
        ),
        (
            "AT1651_1_coupling_lane",
            "B_obs_source_measure_over_MH / Y5_projected_source_flux_over_MH",
            "derive/source coupling/source-measure flux row next",
            "this is the source-normalization/coupling leak that keeps the local branch from being GR-clean",
            "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
        ),
        (
            "AT1651_2_boundary_lane",
            "Pi_R_boundary_abs / B_obs_boundary_improvement_over_MH",
            "derive/source boundary reciprocal momentum and no-flux row",
            "this is the direct Q_R/r reciprocal-hair leak",
            "future after 1652 unless new boundary theorem appears",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "target_id": target_id,
            "target_quantity": target_quantity,
            "action": action,
            "why": why,
            "next_target": next_target,
            "source_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for target_id, target_quantity, action, why, next_target in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1651_0_live_source_row", "at least one Bobs/MHref row is source-ready", False, "BLOCKED", "raw and accepted intake are empty; contracts are nonclaim"),
        ("CG1651_1_runner_score", "Bobs priority runner can score", False, "REFUSED", "M_H_ref and all component values/theorem-zeros are missing"),
        ("CG1651_2_local_GR", "local GR/Newton/PPN follows from 1651", False, "NO_CLAIM", "runner hard-refuses missing inputs"),
        ("CG1651_3_no_cancellation", "total residual can use cancellation", False, "REFUSED", "component rows require absolute no-cancellation budget"),
        ("CG1651_4_guardrail", "1651 source-row guardrail is installed", "INTERNAL_ONLY", "PASS_AS_INTERNAL_GUARDRAIL_ONLY", "guardrail is not evidence"),
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
            "DEC1651_0_no_live_rows",
            "NO_RAW_OR_ACCEPTED_BOBS_SOURCE_ROWS",
            "source-intake/rab-sector/raw and accepted contain no live CSV candidates",
            "do not score; keep all Bobs source rows nonclaim",
        ),
        (
            "DEC1651_1_runner",
            "BOBS_PRIORITY_RUNNER_REFUSES_ALL_ROWS",
            "every row lacks source path, units, numeric/theorem-zero value, parent signature, M_H_ref, or no-cancellation budget",
            "use refusal output as the handrail for 1652",
        ),
        (
            "DEC1651_2_first_target",
            "MHREF_DENOMINATOR_FIRST_WITH_SOURCE_MEASURE_COUPLING_LANE",
            "M_H_ref is global denominator; source-measure/Y5 flux is the highest coupling-facing numerator",
            "1652 should attempt M_H_ref first row and source-measure flux contract together",
        ),
        (
            "DEC1651_3_no_claim",
            "NO_LOCAL_GR_OR_PPN_PROMOTION",
            "a refusal runner is not evidence",
            "keep local branch private/nonclaim",
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


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
            "script": "scripts/Y5_R2FR_MHref_denominator_first_row_and_source_measure_flux_contract.py",
            "objective": "attempt to derive or source the first M_H_ref/Mstar denominator row while pairing it with the source-measure/Y5 projected flux contract that carries the coupling leak",
            "success_condition": "either M_H_ref has a parent-signed/source-backed finite positive denominator row and the source-measure flux contract is theorem-zero/source-ready, or both are refused with exact missing inputs",
            "forbidden_shortcuts": "no orbital-GM import; no M_H_ref without integrability/reference/positivity; no source-measure zero without Pi_M/P_loc owner; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    intake_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        (
            "VAL1651_0_sources_exist",
            all(row["path_exists"] and row["needles_found"] for row in source_rows),
            "all cited 1651 source paths exist and needles are present",
        ),
        (
            "VAL1651_1_intake_scanned",
            any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows)
            and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows)
            and any(row["status"] == "QUEUE_PRESENT_NONCLAIM" for row in intake_rows),
            "raw/accepted/queue intake state recorded",
        ),
        (
            "VAL1651_2_priority_inputs_complete",
            len(input_rows) == 7
            and any(row["quantity"] == "M_H_ref / Mstar_same_frame" for row in input_rows)
            and any(row["quantity"] == "B_obs_source_measure_over_MH; Y5_projected_source_flux_over_MH" for row in input_rows),
            "priority runner inputs include denominator and coupling-facing source-measure row",
        ),
        (
            "VAL1651_3_first_source_contract_written",
            len(contract_rows) == 4
            and any(row["quantity"] == "M_H_ref / Mstar_same_frame" for row in contract_rows)
            and any(row["quantity"] == "B_obs_source_measure_over_MH / Y5_projected_source_flux_over_MH" for row in contract_rows),
            "first source-row contract covers MHref and source-measure flux",
        ),
        (
            "VAL1651_4_runner_refuses_all",
            len(refusal_rows) == 7 and all(row["runner_decision"] == "REFUSE_SCORING" for row in refusal_rows),
            "Bobs runner refuses every row until source/theorem data exist",
        ),
        (
            "VAL1651_5_acquisition_target_selected",
            any(row["target_id"] == "AT1651_0_primary" for row in target_rows)
            and any(row["target_id"] == "AT1651_1_coupling_lane" for row in target_rows),
            "primary denominator and coupling-lane targets selected",
        ),
        (
            "VAL1651_6_claim_gates_safe",
            all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim_rows),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1651_7_next_target_selected",
            next_targets[0]["next_target"] == "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
            "next target selects MHref first row and source-measure flux contract",
        ),
        (
            "VAL1651_8_csv_parse",
            generated_csv_parse,
            "all generated 1651 CSVs parse",
        ),
        (
            "VAL1651_9_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1651 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1651_10_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1651_11_queue_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1651_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1651_13_formalization_untouched",
            not formalization_dirty,
            "no 1651 outputs found under formalization-workbench",
        ),
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
            "check_id": "VAL1651_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1651 Bobs component priority runner and first source-row validation",
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


def write_doc(
    source_rows: list[dict[str, object]],
    intake_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1651 - Bobs Component Priority Runner And First Source Row

**Private status:** nonclaim runner checkpoint. No `B_obs` source row, `M_H_ref`, `M_*`, `delta_H_tau` zero, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1651` turns the 1650 priority ledger into an executable refusal runner. Raw and accepted intake are empty, so no row can be promoted. The queue contains useful nonclaim templates, but templates are not evidence.

The acquisition order is now explicit:

```text
1. M_H_ref / Mstar_same_frame
2. B_obs_source_measure_over_MH / Y5_projected_source_flux_over_MH
3. B_obs_boundary_improvement_over_MH / Pi_R_boundary_abs / B_zero_flux
4. B_obs_projector_commutator_over_MH
5. B_obs_bulk_Euler_over_MH
6. corner/tau/reference rows
7. total absolute no-cancellation residual
```

The runner refuses scoring because the denominator, numerator components, source paths, units, parent signatures, and no-cancellation vector are missing. This is a good private checkpoint: it tells us exactly what the first real row must contain instead of letting the branch dissolve into handwaving.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Bobs Priority Runner Inputs

{markdown_table(input_rows, ["runner_input_id", "quantity", "input_class", "acceptance_requirement", "current_status", "priority_rank"])}

## First Source Row Contract

{markdown_table(contract_rows, ["contract_id", "quantity", "required_columns", "acceptance_rule", "current_status", "lane"])}

## Refusal Runner

{markdown_table(refusal_rows, ["run_id", "quantity", "runner_decision", "refusal_reasons"])}

## Acquisition Targets

{markdown_table(target_rows, ["target_id", "target_quantity", "action", "why", "next_target"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The next genuinely useful row is not a cosmology or galaxy fit. It is a local-source row: a noncircular `M_H_ref/Mstar` denominator and the source-measure/Y5 projected flux contract that carries the coupling leak. Once those exist, the local branch can start becoming testable instead of just internally disciplined.
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
    input_rows = runner_input_rows()
    contract_rows = first_source_contract_rows()
    refusal_rows = refusal_runner_rows()
    target_rows = acquisition_target_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(INTAKE_SCAN, intake_rows)
    write_csv(RUNNER_INPUTS, input_rows)
    write_csv(FIRST_SOURCE_CONTRACT, contract_rows)
    write_csv(REFUSAL_RUNNER, refusal_rows)
    write_csv(ACQUISITION_TARGETS, target_rows)
    write_csv(CLAIM_GATE, claim_rows)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_targets)
    copy_outputs()

    validation = validation_rows(source_rows, intake_rows, input_rows, contract_rows, refusal_rows, target_rows, claim_rows, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, input_rows, contract_rows, refusal_rows, target_rows, claim_rows, decisions, next_targets, validation)
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
