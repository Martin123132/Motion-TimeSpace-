from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Qbar_source_pack_built_BX_closure_runner_blocked_nonclaim"
CLAIM_CEILING = "source_pack_and_closure_runner_scaffold_only_no_Qbar_claim_no_alpha_edge_no_R10_no_PPN_no_clock_no_orbital_no_local_GR_claim"
NEXT_TARGET = "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "682-Y5-R10-Qbar-numerator-denominator-source-pack-or-BX-closure-runner.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "680_doc": ROOT / "680-Y5-R10-parent-P-constitutive-owner-or-Qbar-numeric-denominator-source.md",
    "680_validation": RESIDUALS / "P8_Y5_BRR545_680_VALIDATION.csv",
    "680_p_owner": RESIDUALS / "P8_Y5_R10_680_P_CONSTITUTIVE_OWNER_ATTEMPT.csv",
    "680_bx": RESIDUALS / "P8_Y5_R10_680_BX_CLAIM_ROW_CANDIDATE.csv",
    "680_qbar_gate": RESIDUALS / "P8_Y5_R10_680_QBAR_DENOMINATOR_SOURCE_GATE.csv",
    "681_doc": ROOT / "681-Y5-R10-defect-potential-Z-map-or-explicit-BX-closure-demotion.md",
    "681_validation": RESIDUALS / "P8_Y5_BRR545_681_VALIDATION.csv",
    "681_z_map": RESIDUALS / "P8_Y5_R10_681_Z_MAP_ATTEMPT.csv",
    "681_bx_closure": RESIDUALS / "P8_Y5_R10_681_BX_CLOSURE_DEMOTION.csv",
    "681_decision": RESIDUALS / "P8_Y5_R10_681_DECISION.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "hamiltonian_measure_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector and Qbar placeholder source",
        "673_validation": "673 validation gate",
        "673_acquisition": "edge coefficient acquisition ledger",
        "674_validation": "674 validation gate",
        "674_requirements": "required coefficient contract for edge alpha",
        "675_validation": "675 validation gate",
        "675_blockers": "open edge blocker matrix",
        "680_doc": "P owner and Qbar denominator predecessor checkpoint",
        "680_validation": "680 validation gate",
        "680_p_owner": "P=dV_def/dZ partial owner attempt",
        "680_bx": "nonclaim B_X candidate row",
        "680_qbar_gate": "Qbar denominator gate source",
        "681_doc": "B_X closure demotion predecessor checkpoint",
        "681_validation": "681 validation gate",
        "681_z_map": "Z/Vdef partial-flow-only rows",
        "681_bx_closure": "explicit B_X closure demotion rows",
        "681_decision": "Qbar fallback decision row",
        "boundary_reference_status": "M_H_ref and boundary reference first-row status",
        "hamiltonian_measure_contract": "Hamiltonian source-measure and Pi_M contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def qbar_source_pack_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "pack_id": "QSP682_0_definition",
            "object": "Qbar_edge_XH(lambda)",
            "required_input": "dimensionless numerator-over-denominator edge projection",
            "candidate_definition": "Qbar_edge_XH(lambda) = Pi_M^H[Q_edge^H(lambda)] / M_H_ref",
            "current_evidence": "definition is stable across 671/673/674 but the row is still placeholder-level",
            "blocking_condition": "needs numeric or theorem-zero numerator, positive denominator, lambda support, units, and same-frame convention",
            "status": "definition_only_nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "674_requirements"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_1_Qedge_numerator",
            "object": "Q_edge^H(lambda)",
            "required_input": "boundary-current numerator for the H/source projection",
            "candidate_definition": "Q_edge^H(lambda) = integral_over_edge_shell epsilon_boundary B_X^H(lambda)",
            "current_evidence": "B_X exists only as explicit closure support after 681; no sourced shell, counterterm, or boundary class fixes the integral",
            "blocking_condition": "MISSING_QEDGE_NUMERATOR_FROM_PARENT_OR_SOURCE",
            "status": "blocked_by_BX_closure",
            "valid_for_claim": "false",
            "source_paths": source_list("680_bx", "681_bx_closure", "681_z_map"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_2_MH_denominator",
            "object": "M_H_ref",
            "required_input": "positive same-frame Hamiltonian/source mass denominator tied to measured GM",
            "candidate_definition": "M_H_ref = fixed-frame Hilbert/source charge after reference subtraction",
            "current_evidence": "boundary reference status reports 31 data rows and 20 theorem-zero rows with the term, but zero claim-valid rows",
            "blocking_condition": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "status": "blocked_by_denominator_source_gap",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_measure_contract", "680_qbar_gate"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_3_lambda_support",
            "object": "lambda_edge",
            "required_input": "positive edge range or support envelope in recognized units",
            "candidate_definition": "lambda_edge sets the R10 interpolation/support scale for Qbar_edge_XH(lambda)",
            "current_evidence": "671 and 675 keep lambda_edge at MISSING_EDGE_RANGE_OR_ENVELOPE",
            "blocking_condition": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "status": "blocked_by_support_gap",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "675_blockers"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_4_PiM_frame_reference",
            "object": "Pi_M^H",
            "required_input": "integrable projection operator and fixed reference convention",
            "candidate_definition": "Pi_M^H selects the H/source sector charge in the same frame as M_H_ref",
            "current_evidence": "Hamiltonian measure contract is a candidate only; integrable charge and constant-G reference are not parent-derived",
            "blocking_condition": "MISSING_INTEGRABLE_CHARGE_AND_REFERENCE_SUBTRACTION",
            "status": "blocked_by_projection_contract_gap",
            "valid_for_claim": "false",
            "source_paths": source_list("hamiltonian_measure_contract", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_5_units_force_law",
            "object": "alpha_edge(lambda)",
            "required_input": "dimensionally consistent map alpha_edge = K_edge Qbar_edge_XH qbar_XT",
            "candidate_definition": "alpha_edge(lambda) = K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT(lambda)",
            "current_evidence": "product form is runner-ready but K_edge, Qbar, qbar_XT, and lambda remain missing or nonclaim",
            "blocking_condition": "MISSING_NUMERIC_PRODUCT_INPUTS_AND_UNITS",
            "status": "blocked_by_alpha_product_inputs",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "674_requirements", "675_blockers"),
            "generated_utc": now,
        },
        {
            "pack_id": "QSP682_6_verdict",
            "object": "Qbar_edge_XH(lambda)",
            "required_input": "claim-ready source row or theorem-zero row",
            "candidate_definition": "none accepted in 682",
            "current_evidence": "the source pack is now explicit, but every route contains a missing parent/source input",
            "blocking_condition": "NO_CLAIM_READY_QBAR_ROW",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "674_requirements", "675_blockers", "680_qbar_gate", "681_bx_closure"),
            "generated_utc": now,
        },
    ]


def bx_closure_runner_input_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "runner_id": "BCRI682_0_closure_scaffold",
            "branch_id": "MTS_R10_edge_branch_BX_closure_scaffold",
            "input_role": "nonclaim closure runner row",
            "symbol_or_row": "B_X_boundary_momentum",
            "value_or_formula": "B_X^nu = n_mu P^{mu nu} + B_ct^nu",
            "source_status": "explicit_closure_support_nonclaim",
            "failure_mode": "MISSING_PARENT_OWNED_FULL_Z_Vdef_MAB_AND_BCT",
            "runner_effect": "may be used for private sensitivity smoke only, never as R10 evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("680_bx", "681_bx_closure"),
            "generated_utc": now,
        },
        {
            "runner_id": "BCRI682_1_Qedge_placeholder",
            "branch_id": "MTS_R10_edge_branch_BX_closure_scaffold",
            "input_role": "Qbar numerator placeholder",
            "symbol_or_row": "Q_edge^H(lambda)",
            "value_or_formula": "MISSING_QEDGE_NUMERATOR",
            "source_status": "missing",
            "failure_mode": "B_X_closure_cannot_define_claim_numeric_integral",
            "runner_effect": "runner must stop before producing a claim row",
            "valid_for_claim": "false",
            "source_paths": source_list("681_bx_closure", "680_qbar_gate"),
            "generated_utc": now,
        },
        {
            "runner_id": "BCRI682_2_MH_placeholder",
            "branch_id": "MTS_R10_edge_branch_BX_closure_scaffold",
            "input_role": "Qbar denominator placeholder",
            "symbol_or_row": "M_H_ref",
            "value_or_formula": "MISSING_SOURCE_BACKED_M_H_REF",
            "source_status": "missing",
            "failure_mode": "same-frame positive source denominator not claim-valid",
            "runner_effect": "Qbar division is forbidden until denominator row is sourced",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "runner_id": "BCRI682_3_lambda_placeholder",
            "branch_id": "MTS_R10_edge_branch_BX_closure_scaffold",
            "input_role": "support placeholder",
            "symbol_or_row": "lambda_edge",
            "value_or_formula": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "source_status": "missing",
            "failure_mode": "no interpolation/support scale",
            "runner_effect": "R10 comparator remains blocked",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "675_blockers"),
            "generated_utc": now,
        },
        {
            "runner_id": "BCRI682_4_reference_zero_guard",
            "branch_id": "MTS_R10_edge_branch_reference_zero_guard",
            "input_role": "theorem-zero guardrail",
            "symbol_or_row": "reference_zero_not_evidence",
            "value_or_formula": "zero rows count only if parent-signed in the same arena and same frame",
            "source_status": "guardrail",
            "failure_mode": "conditional/template zero cannot replace missing source rows",
            "runner_effect": "prevents accidental promotion of reference-zero placeholders",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
    ]


def qbar_claim_gate_evaluation_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "QCGE682_0_numerator_gate",
            "gate": "Q_edge numerator",
            "requirement": "numeric or parent-theorem-zero Q_edge^H(lambda) with boundary shell, counterterm, and projection",
            "observed_state": "MISSING_QEDGE_NUMERATOR_FROM_PARENT_OR_SOURCE",
            "result": "fail_blocked",
            "claim_effect": "Qbar cannot be claimed",
            "valid_for_claim": "false",
            "source_paths": source_list("681_bx_closure", "680_qbar_gate"),
            "generated_utc": now,
        },
        {
            "gate_id": "QCGE682_1_denominator_gate",
            "gate": "M_H_ref denominator",
            "requirement": "positive same-frame source mass tied to measured GM or a parent-owned source charge",
            "observed_state": "boundary reference file reports zero claim-valid M_H_ref rows",
            "result": "fail_blocked",
            "claim_effect": "Qbar division cannot be performed",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "QCGE682_2_lambda_gate",
            "gate": "lambda support",
            "requirement": "positive lambda_edge with recognized units and source path",
            "observed_state": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "result": "fail_blocked",
            "claim_effect": "R10 interpolation/comparison cannot run as evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "675_blockers"),
            "generated_utc": now,
        },
        {
            "gate_id": "QCGE682_3_projection_gate",
            "gate": "Pi_M same-frame projection",
            "requirement": "integrable Hamiltonian/source projection with fixed reference subtraction",
            "observed_state": "candidate only; not parent-derived",
            "result": "fail_blocked",
            "claim_effect": "numerator and denominator are not guaranteed in the same frame",
            "valid_for_claim": "false",
            "source_paths": source_list("hamiltonian_measure_contract", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "QCGE682_4_units_product_gate",
            "gate": "alpha product units",
            "requirement": "K_edge, Qbar_edge_XH, qbar_XT, and lambda all numeric, sourced, and dimensionally compatible",
            "observed_state": "all product inputs remain missing, placeholder, or nonclaim",
            "result": "fail_blocked",
            "claim_effect": "no alpha_edge, R10, PPN, clock, orbital, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "674_requirements", "675_blockers"),
            "generated_utc": now,
        },
        {
            "gate_id": "QCGE682_5_final_gate",
            "gate": "Qbar claim readiness",
            "requirement": "all gates pass with no MISSING markers and no closure-only inputs",
            "observed_state": "5 blocking gates remain open",
            "result": "fail_blocked",
            "claim_effect": "682 remains source-pack plumbing only",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "673_acquisition", "674_requirements", "675_blockers", "680_qbar_gate", "681_bx_closure"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    qbar_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    qbar_claim_rows = [row for row in qbar_rows if row["valid_for_claim"] == "true"]
    runner_claim_rows = [row for row in runner_rows if row["valid_for_claim"] == "true"]
    passing_gates = [row for row in gate_rows if row["result"] == "pass"]
    return [
        {
            "evaluator_id": "EV682_0_Qbar_pack",
            "target": "Qbar numerator/denominator source pack",
            "status": "built_nonclaim",
            "reason": f"qbar_rows={len(qbar_rows)};claim_rows={len(qbar_claim_rows)}",
            "claim_effect": "source pack explicit but no Qbar row promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV682_1_BX_closure_runner",
            "target": "B_X closure runner scaffold",
            "status": "blocked_nonclaim",
            "reason": f"runner_rows={len(runner_rows)};claim_rows={len(runner_claim_rows)}",
            "claim_effect": "closure runner can smoke-test schema only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV682_2_claim_gates",
            "target": "Qbar claim readiness",
            "status": "fail_blocked",
            "reason": f"passing_gates={len(passing_gates)};blocking_gates={len(gate_rows) - len(passing_gates)}",
            "claim_effect": "R10/local arenas stay blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV682_3_next_route",
            "target": "next sourceable input",
            "status": "selected_nonclaim",
            "reason": "M_H_ref is independently sourceable while Q_edge still depends on closure-owned B_X",
            "claim_effect": "next checkpoint should source the same-frame denominator or prove the numerator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D682_0_Qbar",
            "target": "Qbar_edge_XH(lambda)",
            "result": "source_pack_only",
            "reason": "definition is clear, but numerator, denominator, lambda support, projection, and units are not claim-ready",
            "next_action": "do not promote Qbar or alpha_edge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D682_1_BX",
            "target": "B_X closure runner",
            "result": "blocked_nonclaim_scaffold",
            "reason": "B_X is explicitly closure support after 681 and cannot define a sourced numerator by itself",
            "next_action": "permit schema/sensitivity smoke only with valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D682_2_next",
            "target": "M_H_ref or Q_edge",
            "result": "selected",
            "reason": "M_H_ref is the cleanest independent denominator gap; Q_edge remains tied to the harder boundary-current proof",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S682_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Qbar source pack built; every claim gate remains blocked",
            "blocked_claims": "Qbar;alpha_edge;R10;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def boundary_reference_mh_ref_claim_ready() -> bool:
    status_path = SOURCE_PATHS["boundary_reference_status"]
    if not status_path.exists():
        return False
    for source_row in read_csv(status_path):
        if source_row.get("quantity") == "M_H_ref":
            return (
                source_row.get("valid_for_claim") == "true"
                and source_row.get("claim_valid_data_rows") not in {"", "0"}
            )
    return False


def validation_rows(
    source_register: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [source_row["source_id"] for source_row in source_register if source_row["exists"] != "true"]
    rows.append({
        "check_id": "V682_0_source_paths_exist",
        "result": "pass" if not missing_sources else "fail",
        "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        "generated_utc": now,
    })

    validation_ids = ["671_validation", "673_validation", "674_validation", "675_validation", "680_validation", "681_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({
        "check_id": "V682_1_prior_validations_clean",
        "result": "pass" if all(failure_count == 0 for failure_count in prior_failures.values()) else "fail",
        "detail": ";".join(f"{source_id}={failure_count}" for source_id, failure_count in prior_failures.items()),
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V682_2_Qbar_pack_complete",
        "result": "pass" if len(qbar_rows) >= 7 else "fail",
        "detail": f"qbar_rows={len(qbar_rows)}",
        "generated_utc": now,
    })

    qbar_claim_rows = [source_row for source_row in qbar_rows if source_row["valid_for_claim"] == "true"]
    rows.append({
        "check_id": "V682_3_Qbar_pack_nonclaim",
        "result": "pass" if not qbar_claim_rows else "fail",
        "detail": "all Qbar source-pack rows remain valid_for_claim=false" if not qbar_claim_rows else f"claim_rows={len(qbar_claim_rows)}",
        "generated_utc": now,
    })

    required_blockers = ["MISSING_QEDGE_NUMERATOR", "MISSING_SOURCE_BACKED_M_H_REF", "MISSING_EDGE_RANGE_OR_ENVELOPE"]
    blocker_text = ";".join(";".join(source_row.values()) for source_row in qbar_rows + runner_rows + gate_rows)
    missing_blockers = [blocker for blocker in required_blockers if blocker not in blocker_text]
    rows.append({
        "check_id": "V682_4_required_blockers_recorded",
        "result": "pass" if not missing_blockers else "fail",
        "detail": "required blockers present" if not missing_blockers else "missing_blockers=" + ";".join(missing_blockers),
        "generated_utc": now,
    })

    runner_claim_rows = [source_row for source_row in runner_rows if source_row["valid_for_claim"] == "true"]
    rows.append({
        "check_id": "V682_5_BX_closure_runner_blocked",
        "result": "pass" if runner_rows and not runner_claim_rows and any("closure" in source_row["source_status"] for source_row in runner_rows) else "fail",
        "detail": f"runner_rows={len(runner_rows)};claim_rows={len(runner_claim_rows)}",
        "generated_utc": now,
    })

    failed_gates = [source_row for source_row in gate_rows if source_row["result"] != "pass"]
    rows.append({
        "check_id": "V682_6_claim_gates_block_claims",
        "result": "pass" if len(failed_gates) == len(gate_rows) and len(gate_rows) >= 5 else "fail",
        "detail": f"failed_gates={len(failed_gates)};gate_rows={len(gate_rows)}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V682_7_MH_ref_not_claim_ready",
        "result": "pass" if not boundary_reference_mh_ref_claim_ready() else "fail",
        "detail": "boundary reference status has no claim-ready M_H_ref row",
        "generated_utc": now,
    })

    selected_rows = [source_row for source_row in decision if source_row["next_action"] == NEXT_TARGET]
    rows.append({
        "check_id": "V682_8_next_target_selected",
        "result": "pass" if selected_rows else "fail",
        "detail": NEXT_TARGET,
        "generated_utc": now,
    })

    generated_rows = qbar_rows + runner_rows + gate_rows + evaluator + decision
    all_claim_rows = [source_row for source_row in generated_rows if source_row.get("valid_for_claim") == "true"]
    rows.append({
        "check_id": "V682_9_no_claim_rows_promoted",
        "result": "pass" if not all_claim_rows else "fail",
        "detail": "all generated 682 rows remain valid_for_claim=false" if not all_claim_rows else f"claim_rows={len(all_claim_rows)}",
        "generated_utc": now,
    })

    output_paths = [
        RESIDUALS / "P8_Y5_R10_682_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_682_QBAR_SOURCE_PACK.csv",
        RESIDUALS / "P8_Y5_R10_682_BX_CLOSURE_RUNNER_INPUT.csv",
        RESIDUALS / "P8_Y5_R10_682_QBAR_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_682_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_682_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_682_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_682_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({
        "check_id": "V682_10_generated_outputs_scoped",
        "result": "pass" if all(str(output_path).startswith(str(ROOT)) for output_path in output_paths) else "fail",
        "detail": "all 682 outputs target post-checkpoint-work",
        "generated_utc": now,
    })

    changed_count = formalization_changed_count()
    rows.append({
        "check_id": "V682_11_formalization_workbench_untouched",
        "result": "pass" if changed_count == 0 else "fail",
        "detail": f"formalization_changed_after_cutoff={changed_count}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V682_12_status_nonclaim",
        "result": "pass" if "no_Qbar_claim" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail",
        "detail": CLAIM_CEILING,
        "generated_utc": now,
    })

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for source_row in rows:
        rendered_values = [
            str(source_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        lines.append("| " + " | ".join(rendered_values) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 682 - Y5 R10 Qbar Numerator Denominator Source Pack Or BX Closure Runner

## Verdict

682 built the honest `Qbar_edge_XH(lambda)` source pack.

The useful definition is stable:

```text
Qbar_edge_XH(lambda) = Pi_M^H[Q_edge^H(lambda)] / M_H_ref
alpha_edge(lambda) = K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT(lambda)
```

But it is not claim-ready. The numerator still needs a parent-owned or source-backed `Q_edge^H(lambda)`, the denominator still needs a positive same-frame `M_H_ref`, and `lambda_edge`, `Pi_M`, units, and product inputs remain blocked. Since 681 demoted `B_X` to explicit closure support, the closure runner can only be a private smoke scaffold, not R10 evidence.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Qbar Source Pack

{markdown_table(qbar_rows, ["pack_id", "object", "required_input", "candidate_definition", "current_evidence", "blocking_condition", "status", "valid_for_claim"])}

## BX Closure Runner Input

{markdown_table(runner_rows, ["runner_id", "branch_id", "input_role", "symbol_or_row", "value_or_formula", "source_status", "failure_mode", "runner_effect", "valid_for_claim"])}

## Qbar Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "requirement", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: source or derive the same-frame `M_H_ref` denominator first, while keeping the harder `Q_edge` numerator proof visible. If `M_H_ref` still cannot be made claim-ready, the local R10 edge branch remains blocked rather than dressed up as evidence.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    qbar_rows = qbar_source_pack_rows()
    runner_rows = bx_closure_runner_input_rows()
    gate_rows = qbar_claim_gate_evaluation_rows()
    evaluator = evaluator_rows(qbar_rows, runner_rows, gate_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, qbar_rows, runner_rows, gate_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_682_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_QBAR_SOURCE_PACK.csv", qbar_rows, ["pack_id", "object", "required_input", "candidate_definition", "current_evidence", "blocking_condition", "status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_BX_CLOSURE_RUNNER_INPUT.csv", runner_rows, ["runner_id", "branch_id", "input_role", "symbol_or_row", "value_or_formula", "source_status", "failure_mode", "runner_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_QBAR_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "requirement", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_682_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_682_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, qbar_rows, runner_rows, gate_rows, evaluator, decision, validation)

    failures = [source_row for source_row in validation if source_row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"qbar_rows={len(qbar_rows)}")
    print(f"runner_rows={len(runner_rows)}")
    print(f"gate_rows={len(gate_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
