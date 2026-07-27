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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2889-Y5-R2FR-common-frame-bR-zero-or-first-PPN-kernel-row-under-AX1090.md"

SRC_2888_DOC = ROOT / "2888-Y5-R2FR-terminal-public-coframe-no-shadow-or-Cshadow-bound-row-under-AX1090.md"
SRC_2888_NEXT = RESIDUALS / "P8_Y5_R2FR_2888_NEXT_TARGET.csv"
SRC_2888_CSHADOW = RESIDUALS / "P8_Y5_R2FR_2888_CSHADOW_BOUND_ROW_NONCLAIM.csv"
SRC_2888_KERNELS = RESIDUALS / "P8_Y5_R2FR_2888_RESPONSE_KERNEL_LINKS_NONCLAIM.csv"
SRC_2888_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2888_VALIDATION.csv"

SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2489_RETRY = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PARENT_NO_SHADOW_RETRY.csv"
SRC_2489_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2489_INTERFACE = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESIDUAL_VECTOR_INTERFACE.csv"
SRC_2631_AUDIT = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_NO_SHADOW_GATE_AUDIT.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2889_SOURCE_REGISTER.csv",
    "bzero": RESIDUALS / "P8_Y5_R2FR_2889_BR_ZERO_THEOREM_ATTEMPT.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2889_COMMON_WEYL_PPN_KERNEL_ROW_NONCLAIM.csv",
    "inputs": RESIDUALS / "P8_Y5_R2FR_2889_KERNEL_INPUT_REQUIREMENTS.csv",
    "ppn": RESIDUALS / "P8_Y5_R2FR_2889_FULL_PPN_GUARD_LEDGER.csv",
    "update": RESIDUALS / "P8_Y5_R2FR_2889_CSHADOW_BR_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2889_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2889_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2889_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2889_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2889_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2889_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": LOCAL_BOUNDS / "RAB_COMMON_WEYL_PPN_KERNEL_ROW_2889_NONCLAIM.csv",
    "input_copy": SOURCE_WEIGHT / "RAB_BR_KERNEL_INPUT_REQUIREMENTS_2889_NONCLAIM.csv",
    "ppn_copy": BETA_DOCS / "RAB_FULL_PPN_GUARD_LEDGER_2889_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2889_xU_or_deltaP_profile_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2889_0_2888_doc", SRC_2888_DOC, "Status: `Y5_R2FR_2888_no_shadow_conditional_Cshadow_abs_nonclaim_2889_bR_next`;## Next Target", "2888 handoff"),
        ("SRC2889_1_2888_next", SRC_2888_NEXT, "NEXT2888_0_2889", "explicit 2889 target"),
        ("SRC2889_2_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_1_b_R_common_weyl;MISSING_b_R_VALUE", "b_R staged row"),
        ("SRC2889_3_2888_kernels", SRC_2888_KERNELS, "KER2888_0_PPN_metric;C_shadow_abs", "shadow kernel links"),
        ("SRC2889_4_2888_validation", SRC_2888_VALIDATION, "VAL2888_OVERALL", "2888 validation"),
        ("SRC2889_5_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "terminal coframe no-shadow theorem"),
        ("SRC2889_6_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_1_common_disformal", "common-frame countermodels"),
        ("SRC2889_7_2489_retry", SRC_2489_RETRY, "PNC2489_0_terminal_public_action_domain;PNC2489_3_verdict", "parent no-shadow retry"),
        ("SRC2889_8_2489_kernel", SRC_2489_KERNEL, "PPNK2489_0_conformal_gamma_kernel;PPNK2489_1_CR_delta_p_combo_kernel", "common Weyl PPN kernel"),
        ("SRC2889_9_2489_interface", SRC_2489_INTERFACE, "PPNV2489_1_bR;PPNV2489_7_total_abs", "PPN residual vector interface"),
        ("SRC2889_10_2631_audit", SRC_2631_AUDIT, "NSG2631_1_terminal_public_coframe;NSG2631_4_verdict", "no-shadow PPN gate audit"),
        ("SRC2889_11_2631_vector", SRC_2631_VECTOR, "PPNV2631_1_bR;PPNV2631_8_total_abs", "full PPN vector ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def bzero_rows() -> list[dict[str, Any]]:
    specs = [
        ("BRZ2889_0_exact_if_signed", "b_R=0 from no-Weyl-slot", "Allowed[S_matter,Obs] excludes e_obs=exp(b_R C_R)e_pub and any A_R(C_R) public-frame argument; then functional derivative with respect to C_R Weyl slot is zero.", "EXACT_CONDITIONAL_THEOREM", "2488/2489 no-shadow action-domain exclusion would set b_R=0 if parent-signed", "parent action-domain exclusion is unsigned"),
        ("BRZ2889_1_terminality", "terminal public coframe", "all ordinary matter/readout factors through terminal e_pub=E(Q_vis) before local PPN readout", "NOT_PARENT_SIGNED", "would remove hidden coframe representative dependence", "terminality/Q_vis ownership remains closure-only"),
        ("BRZ2889_2_countermodel", "common Weyl countermodel", "e_obs=exp(b_R C_R)e_pub remains covariant, universal and WEP-compatible while shifting gamma/clock readout", "COUNTERMODEL_SURVIVES", "blocks b_R=0 shortcut", "must derive no Weyl slot or source b_R"),
        ("BRZ2889_3_source_readout", "readout/gauge/source tail guard", "measured GM, PPN gauge and endpoint extraction cannot reintroduce b_R-like residuals", "NOT_DERIVED", "would isolate gamma response to b_R only", "readout/gauge/source-normalization tails remain open"),
        ("BRZ2889_4_verdict", "b_R zero theorem", "all above clauses close", "BR_ZERO_NOT_DERIVED_CURRENT_CORPUS", "do not set b_R=0", "stage common-Weyl PPN kernel row"),
    ]
    return [
        add_common(
            {
                "attempt_id": attempt_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "if_closed": if_closed,
                "current_blocker": blocker,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for attempt_id, target, statement, status, if_closed, blocker in specs
    ]


def kernel_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "kernel_id": "PPNK2889_0_common_weyl_gamma",
                "component": "b_R_common_Weyl",
                "observable": "gamma_minus_1",
                "ansatz": "g_obs=exp(2 sigma_R)g_GR, sigma_R=s_R U/c^2, s_R=b_R x_U",
                "derived_response": "gamma_eff=(1+s_R)/(1-s_R); gamma_minus_1=2s_R/(1-s_R)",
                "linearized_response": "gamma_minus_1 = 2*b_R*x_U + O((b_R*x_U)^2)",
                "bound_bridge": "|s_R| <= 1.14998677515209e-05 from Cassini |gamma-1|<=2.3e-05",
                "kernel_status": "SOURCE_BACKED_CONDITIONAL_KERNEL_NONCLAIM",
                "missing_inputs": "MISSING_b_R_VALUE;MISSING_x_U_PROFILE_OR_DELTA_P;MISSING_BETA_CHANNEL;MISSING_NO_OTHER_PPN_CHANNELS",
                "candidate_prediction": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "kernel_id": "PPNK2889_1_CR_delta_p_combo",
                "component": "C_R_profile_times_b_R",
                "observable": "gamma_obs_minus_1",
                "ansatz": "C_R=ln(T^2S)=2 delta_p U/c^2+O(U^2/c^4), sigma_R=b_R C_R",
                "derived_response": "gamma_obs=(1+delta_p+2*b_R*delta_p)/(1-2*b_R*delta_p)",
                "linearized_response": "gamma_obs-1 = delta_p + 4*b_R*delta_p + O(delta_p^2)",
                "bound_bridge": "Cassini bounds the combined residual, not b_R alone",
                "kernel_status": "DERIVED_SYMBOLIC_COMBO_NONCLAIM",
                "missing_inputs": "MISSING_delta_p_ZERO_OR_VALUE;MISSING_b_R_VALUE;MISSING_NO_CANCELLATION_THEOREM;MISSING_FULL_VECTOR_CLOSURE",
                "candidate_prediction": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def input_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2889_0_bR", "b_R", "common Weyl coefficient", "MISSING_b_R_VALUE_OR_ZERO", "parent no-Weyl theorem or source-backed coefficient", "cannot turn kernel into prediction"),
        ("REQ2889_1_xU", "x_U", "profile normalization linking C_R or sigma_R to U/c^2", "MISSING_x_U_PROFILE_OR_DELTA_P", "derive C_R profile or source delta_p/q_R_hat row", "Cassini bounds s_R=b_R*x_U, not b_R"),
        ("REQ2889_2_beta", "Delta_beta_total_abs", "second-order beta/source/operator/readout residual", "MISSING_BETA_RESPONSE_KERNEL", "beta component theorem-zero or finite row", "gamma-only pass is forbidden"),
        ("REQ2889_3_other_ppn", "Delta_PPN_abs", "full PPN no-cancellation vector", "SCHEMA_READY_VALUES_MISSING", "all PPN components theorem-zero or finite", "prevents hidden cancellation/victory on one observable"),
        ("REQ2889_4_readout", "alpha_readout_or_delta_GM", "PPN gauge/measured-GM calibration tail", "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION", "fixed-before-readout transfer theorem or finite tail", "observed U must match parent source mass convention"),
    ]
    return [
        add_common(
            {
                "requirement_id": req_id,
                "symbol": symbol,
                "definition": definition,
                "current_status": status,
                "next_input": next_input,
                "why_needed": why,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for req_id, symbol, definition, status, next_input, why in specs
    ]


def ppn_guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPNG2889_0_gamma", "gamma_minus_1", "b_R and delta_p combo", "CONDITIONAL_KERNEL_READY_VALUE_MISSING", "b_R, x_U/delta_p, no-other-channel proof"),
        ("PPNG2889_1_beta", "beta_minus_1", "second-order g00/source/operator/readout residual", "MISSING_BETA_RESPONSE_KERNEL", "second-order field equation and source-normalized vector"),
        ("PPNG2889_2_preferred", "alpha1/alpha2/alpha3/xi", "disformal/preferred-frame shadow d_R and endpoint/domain vectors", "MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION", "normalized disformal ansatz and vector response"),
        ("PPNG2889_3_source", "Newton_GM/WEP/source", "w_R and source-prefactor tails", "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL", "no-source-prefactor theorem or finite source vector"),
        ("PPNG2889_4_endpoint", "orbital/light-time/gauge tails", "epsilon_endpoint_R and readout/gauge shifts", "MISSING_ENDPOINT_SILENCE_OR_PROJECTION", "boundary endpoint silence or finite kernel"),
        ("PPNG2889_5_total_abs", "all PPN", "componentwise absolute sum", "SCHEMA_READY_VALUES_MISSING", "every head zeroed or bounded; no cancellation"),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "observable_targets": targets,
                "component": component,
                "current_status": status,
                "missing_for_claim": missing,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for guard_id, targets, component, status, missing in specs
    ]


def update_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "CSH2889_0_bR_update",
                "parent_row": "CSH2888_1_b_R_common_weyl",
                "symbol": "b_R",
                "previous_status": "CONDITIONAL_PPN_KERNEL_EXISTS_VALUE_MISSING",
                "new_information": "common-Weyl gamma kernel is explicit and source-backed as a conditional comparator, but b_R and x_U/delta_p remain missing",
                "updated_formula": "gamma_minus_1=2*b_R*x_U/(1-b_R*x_U) or gamma_obs-1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p) in the C_R profile route",
                "candidate_value": "MISSING_b_R_VALUE",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "current_status": "KERNEL_READY_BUT_COMPONENT_VALUE_MISSING",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2889_0_bR_zero", "b_R=0 is parent-derived", "FAIL", "no-Weyl action-domain exclusion is not parent-signed"),
        ("GATE2889_1_kernel", "common-Weyl gamma kernel is derived", "PASS_NONCLAIM", "conditional response formula exists and is source-backed as comparator"),
        ("GATE2889_2_prediction", "MTS gamma prediction is numeric/source-backed", "FAIL", "b_R and x_U/delta_p are missing"),
        ("GATE2889_3_full_ppn", "full PPN vector is closed", "FAIL", "beta, disformal, source, endpoint and readout tails remain open"),
        ("GATE2889_4_claim", "local GR/Newton/PPN claim follows", "FAIL", "gamma-only nonclaim kernel cannot prove local GR"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2889_0_ppn_kernel_runner",
                "status": "REFUSED_BR_XU_AND_FULL_PPN_VALUES_MISSING",
                "accepted_zero_theorems": 0,
                "accepted_kernel_rows": 0,
                "accepted_predictions": 0,
                "reason": "common-Weyl kernel is conditional/nonclaim; b_R, x_U/delta_p, beta and full PPN vector inputs are missing",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2889_0_zero", "BR_ZERO_NOT_DERIVED", "common Weyl countermodel survives until no-Weyl action-domain exclusion is parent-signed", "do not set b_R=0"),
        ("DEC2889_1_kernel", "INSTALL_COMMON_WEYL_GAMMA_KERNEL_NONCLAIM", "the conditional gamma response is exact enough to stage, but not enough to score", "keep Cassini as comparator only"),
        ("DEC2889_2_next", "SELECT_XU_OR_DELTAP_PROFILE_NEXT", "Cassini constrains s_R=b_R*x_U or a delta_p combo, so the next missing piece is the C_R/U profile or delta_p/q_R_hat route", "derive x_U/delta_p zero/value next"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2889_0_2890",
                "status": "selected_primary",
                "target_doc": "2890-Y5-R2FR-xU-delta-p-profile-zero-or-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_xU_delta_p_profile_zero_or_source_row_under_AX1090_2890.py",
                "mission": "derive x_U/delta_p/q_R_hat zero or source-backed profile row for the common-Weyl PPN kernel; if it fails, fill the first nonclaim profile input row with units, source convention and full-PPN blockers",
                "forbidden_shortcuts": "no Cassini-as-MTS-prediction; no b_R bound without x_U/delta_p; no gamma-only local-GR claim; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2889_0_kernel_copy", OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_copy"], "local-bounds copy of common-Weyl PPN kernel"),
        ("BR2889_1_input_copy", OUTPUTS["inputs"], BRANCH_OUTPUTS["input_copy"], "source-weight copy of b_R/x_U input requirements"),
        ("BR2889_2_ppn_copy", OUTPUTS["ppn"], BRANCH_OUTPUTS["ppn_copy"], "beta-source docs copy of full PPN guard ledger"),
        ("BR2889_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows = []
    for copy_id, source, destination, purpose in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    bzero = rows_by_name["bzero"]
    kernel = rows_by_name["kernel"]
    inputs = rows_by_name["inputs"]
    ppn = rows_by_name["ppn"]
    update = rows_by_name["update"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2889_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2889_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2889_2_bzero_not_adopted", any(row["current_status"] == "BR_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in bzero), "b_R zero theorem is not adopted"),
        ("VAL2889_3_kernel_rows", len(kernel) == 2 and kernel[0]["kernel_status"] == "SOURCE_BACKED_CONDITIONAL_KERNEL_NONCLAIM", "common-Weyl PPN kernel rows are staged"),
        ("VAL2889_4_kernel_nonclaim", all(row["comparison_ready"] is False for row in kernel), "kernel rows cannot score"),
        ("VAL2889_5_inputs_missing", len(inputs) == 5 and all("MISSING" in row["current_status"] or row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in inputs), "kernel input requirements remain explicit blockers"),
        ("VAL2889_6_full_ppn_guard", len(ppn) == 6 and any(row["guard_id"] == "PPNG2889_5_total_abs" for row in ppn), "full PPN no-cancellation guard is present"),
        ("VAL2889_7_update_missing", update[0]["current_status"] == "KERNEL_READY_BUT_COMPONENT_VALUE_MISSING", "b_R row update keeps value missing"),
        ("VAL2889_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2889_9_runner_refused", runner[0]["status"] == "REFUSED_BR_XU_AND_FULL_PPN_VALUES_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2889_10_next_target_2890", next_target[0]["next_id"] == "NEXT2889_0_2890" and next_target[0]["selected"] is True, "2890 target selected"),
        ("VAL2889_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2889_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2889_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2889_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2889_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2889_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2889_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2889_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2889 refused b_R=0, staged the common-Weyl gamma/CR-delta_p PPN kernels as nonclaim comparators, kept full-PPN no-cancellation guards, and selected x_U/delta_p profile for 2890.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2889 - Y5 R2FR Common-Frame bR Zero Or First PPN Kernel Row Under AX1090

Status: `Y5_R2FR_2889_bR_zero_not_derived_common_weyl_PPN_kernel_nonclaim_2890_next`

## Private Verdict

2889 attacks the first shadow head: `b_R`.

The zero route does not close. If the parent action/readout domain excluded any common Weyl slot `e_obs=exp(b_R C_R)e_pub`, then `b_R=0` would follow. But that exclusion is not parent-signed, and the common-Weyl countermodel remains legal.

The useful result is not a claim; it is a nonclaim kernel:

`g_obs=exp(2 sigma_R)g_GR`, `sigma_R=s_R U/c^2`, `s_R=b_R x_U`, hence `gamma_eff=(1+s_R)/(1-s_R)` and `gamma-1=2s_R/(1-s_R)`.

Cassini bounds `s_R`, not `b_R` by itself. Therefore no MTS prediction, bound, or local-GR pass is allowed until `b_R`, `x_U` or `delta_p/q_R_hat`, beta, readout, and the full PPN no-cancellation vector are closed.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## bR Zero Theorem Attempt

{md_table(rows_by_name["bzero"], ["attempt_id", "target", "current_status", "if_closed", "current_blocker", "valid_for_claim"])}

## Common-Weyl PPN Kernel Rows

{md_table(rows_by_name["kernel"], ["kernel_id", "component", "observable", "derived_response", "bound_bridge", "kernel_status", "comparison_ready", "valid_for_claim"])}

## Kernel Input Requirements

{md_table(rows_by_name["inputs"], ["requirement_id", "symbol", "current_status", "next_input", "why_needed", "valid_for_claim"])}

## Full PPN Guard Ledger

{md_table(rows_by_name["ppn"], ["guard_id", "observable_targets", "component", "current_status", "missing_for_claim", "valid_for_claim"])}

## Cshadow bR Update

{md_table(rows_by_name["update"], ["update_id", "symbol", "new_information", "updated_formula", "current_status", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_zero_theorems", "accepted_kernel_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "bzero": bzero_rows(),
        "kernel": kernel_rows(),
        "inputs": input_rows(),
        "ppn": ppn_guard_rows(),
        "update": update_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2889_OVERALL")
    print(f"VAL2889_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
