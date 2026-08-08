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
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2902-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row-under-AX1090.md"

SRC_2901_DOC = ROOT / "2901-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090.md"
SRC_2901_NEXT = RESIDUALS / "P8_Y5_R2FR_2901_NEXT_TARGET.csv"
SRC_2901_LEAKS = RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CURRENT_ESCAPE_ROWS.csv"
SRC_2590_DOC = ROOT / "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"
SRC_2590_CONTRACT = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv"
SRC_2590_SECTORS = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_SECTOR_PIECE_LEDGER.csv"
SRC_2590_KERNEL = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_KERNEL_CHARGE_ROWS.csv"
SRC_2590_NEXT = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_NEXT_TARGET.csv"
SRC_2393_DOC = ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"
SRC_2393_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv"
SRC_2393_KERNEL = RESIDUALS / "P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv"
SRC_1008_THETA = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
SRC_1009_SECTORS = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_NOETHER_AUDIT = RESIDUALS / "P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv"
SRC_GAUGE_ATTEMPT = RESIDUALS / "P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2902_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv",
    "sectors": RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_SECTOR_PIECE_LEDGER.csv",
    "rows": RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2902_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2902_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2902_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2902_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2902_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2902_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": RAB_QUEUE / "JR2902_VERTICAL_QV_EXTRACTION_CONTRACT_NONCLAIM.csv",
    "sectors_copy": RAB_QUEUE / "JR2902_VERTICAL_QV_SECTOR_PIECE_LEDGER_NONCLAIM.csv",
    "rows_copy": LOCAL_BOUNDS / "Vertical_Qv_kernel_charge_rows_2902_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2902_VERTICAL_SECTOR_VARIATION_LEDGER_NEXT.csv",
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
        ("SRC2902_0_2901_doc", SRC_2901_DOC, "vertical Noether charge extraction;Theta_parent", "2901 selects Qv extraction as next gate"),
        ("SRC2902_1_2901_next", SRC_2901_NEXT, "NEXT2901_0_2902;epsilon_kernel_charge", "machine-readable 2902 handoff"),
        ("SRC2902_2_2901_leaks", SRC_2901_LEAKS, "epsilon_kernel_charge;Delta_q_kernel_current_escape_total", "q/kernel leakage rows feeding Qv"),
        ("SRC2902_3_2590_doc", SRC_2590_DOC, "delta L_parent = E_A delta Phi^A + dTheta_parent;QV_EXTRACTION_CONTRACT_READY_PARENT_UNSIGNED", "previous Qv extraction checkpoint"),
        ("SRC2902_4_2590_contract", SRC_2590_CONTRACT, "VQC2590_0_parent_variation;MISSING_TOTAL_PARENT_ACTION_AND_THETA", "previous extraction contract"),
        ("SRC2902_5_2590_sectors", SRC_2590_SECTORS, "QVP2590_6_total;TOTAL_NOT_PROMOTED", "previous sector piece ledger"),
        ("SRC2902_6_2590_kernel", SRC_2590_KERNEL, "VQL2590_0_kernel_charge;Delta_vertical_Noether_charge_total_over_MH", "previous Qv kernel rows"),
        ("SRC2902_7_2590_next", SRC_2590_NEXT, "NEXT2590_0_selected;2591-Y5-R2FR-vertical-sector-variation-ledger", "previous next target"),
        ("SRC2902_8_2393_doc", SRC_2393_DOC, "delta L_parent;Q_v", "earlier Qv contract"),
        ("SRC2902_9_2393_theorem", SRC_2393_THEOREM, "VNC2393_0_parent_variation;ROUTE_EXACT_NOT_CLAIMED", "earlier Qv theorem rows"),
        ("SRC2902_10_2393_kernel", SRC_2393_KERNEL, "VQL2393_0_kernel_charge;MISSING_THETA_PARENT", "earlier kernel charge rows"),
        ("SRC2902_11_1008_theta", SRC_1008_THETA, "theta_MTS;Q_tau", "parent theta/charge extraction guardrail"),
        ("SRC2902_12_1009_sectors", SRC_1009_SECTORS, "Parent sector contract;PCS1009_0_EH_core", "parent sector variation contract"),
        ("SRC2902_13_noether_chain", SRC_NOETHER_CHAIN, "D505_2_charge_form;Q_M", "Noether closure charge chain"),
        ("SRC2902_14_noether_audit", SRC_NOETHER_AUDIT, "N824_0_diffeomorphism_identity;conditional_identity_only", "Noether identity limitation source"),
        ("SRC2902_15_gauge_attempt", SRC_GAUGE_ATTEMPT, "NIA917_3_Noether_identity_limit;warning_active", "gauge/Noether identity guardrail"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("VQC2902_0_parent_variation", "parent variation identity", "delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi)", "MISSING_TOTAL_PARENT_ACTION_AND_THETA", "without sourced L_parent and Theta_parent, Q_v is notation", "epsilon_theta_piece_missing;epsilon_kernel_charge"),
        ("VQC2902_1_vertical_generator", "vertical generator action", "v_epsilon in ker(Dq) acts on every parent field, matter lift, boundary/reference datum and support variable", "MISSING_PARENT_VERTICAL_GENERATOR_ACTION", "kernel direction cannot be gauge unless its full field-space action is known", "epsilon_v_action_missing;epsilon_q_rank_or_integrability"),
        ("VQC2902_2_mu_v_current", "vertical Noether current", "delta_v L_parent = dmu_v + E_A v^A, J_v = Theta_parent(v_epsilon) - mu_v", "FORMAL_SHAPE_ONLY", "J_v decides whether vertical motion carries Hamiltonian charge", "epsilon_mu_v_missing;epsilon_kernel_charge"),
        ("VQC2902_3_Qv_constraints", "charge and constraint split", "J_v = dQ_v + C_v with C_v proportional to parent constraints in the same branch", "MISSING_VERTICAL_QV_AND_CONSTRAINTS", "conservation identity alone does not imply zero charge", "epsilon_Qv_piece_missing;epsilon_Cv_constraint_missing"),
        ("VQC2902_4_Hv_surface", "kernel Hamiltonian variation", "delta H_v[S]=int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)", "MISSING_HV_SURFACE_FORM", "this is the numerator of epsilon_kernel_charge", "epsilon_kernel_charge;epsilon_Hv_integrability"),
        ("VQC2902_5_zero_compact_flux", "zero compact flux theorem", "delta H_v[S]=0 for every allowed linked compact local surface S, or source-bound it", "MISSING_ZERO_FLUX_CERTIFICATE", "this is the real local-vacuum/kernel-nullness prize", "epsilon_kernel_charge;epsilon_Bv_ambiguity"),
        ("VQC2902_6_denominator", "positive same-frame denominator", "M_ref=H_tau-H_ref or Q_M/ell_J > 0 in the same q/e_obs/tau branch", "MISSING_POSITIVE_SAME_FRAME_MREF", "finite residual rows cannot be scored without non-fitted normalization", "all_normalized_Qv_rows"),
        ("VQC2902_7_verdict", "current verdict", "all VQC2902_0..6 pass with source paths, parent signatures and no retained sector ambiguity", "FAIL_CURRENT_MTS_QV_NOT_EXTRACTED", "route exact; parent objects and sector ledgers absent", "Delta_vertical_Noether_charge_total_over_Mref"),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "step": step,
                "required_equation": required_equation,
                "current_status": current_status,
                "why_it_matters": why_it_matters,
                "residual_if_missing": residual_if_missing,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for contract_id, step, required_equation, current_status, why_it_matters, residual_if_missing in specs
    ]


def sector_rows() -> list[dict[str, Any]]:
    specs = [
        ("QVP2902_0_EH_reference", "EH/local geometry reference", "Theta_EH[e_obs]", "Q_v^EH[v;e_obs]", "REFERENCE_ONLY_NOT_TOTAL_MTS", "MTS parent reduction and silent-sector certificates before EH can be the only piece", "epsilon_Qv_piece_missing"),
        ("QVP2902_1_boundary_reference", "boundary/reference/improvement", "Theta_boundary + delta B_ref", "Q_v^boundary + B_v", "MISSING_FIXED_BEFORE_READOUT_CONVENTION", "fixed improvement ambiguity, no post-readout counterterm and compact no-flux proof", "epsilon_Bv_ambiguity"),
        ("QVP2902_2_extra_motion_time", "motion/time/domain/memory residual", "Theta_extra[v]", "Q_v^extra + C_v^extra", "MISSING_EXTRA_SECTOR_VARIATION", "local silence/double-zero or finite source-backed extra-sector charge", "epsilon_Qv_piece_missing"),
        ("QVP2902_3_projector_source_measure", "projector/source-measure Pi_M", "Theta_projector[v]", "Q_v^projector + C_v^projector", "MISSING_PROJECTOR_SYMPLECTIC_ALGEBRA", "Pi_M parent variation, chain map, closure and measured-GM calibration", "epsilon_Qv_piece_missing;epsilon_Cv_constraint_missing"),
        ("QVP2902_4_matter_source", "matter/source/worldtube glue", "Theta_matter/source[v]", "Q_v^matter/source + C_v^matter", "MISSING_MATTER_SOURCE_GLUE", "Hilbert current equality, matter descent, worldtube support, no source-prefactor and boundary silence", "epsilon_matter_kernel;epsilon_hidden_source_slot"),
        ("QVP2902_5_constraint_total", "constraint and C_v total", "constraint-proportional pieces", "C_v=C_EH+C_extra+C_projector+C_matter+C_boundary", "MISSING_CONSTRAINT_TOTAL_ZERO_OR_BOUND", "each C_v piece is parent EOM/proper constraint or source-bounded", "epsilon_Cv_constraint_missing;epsilon_kernel_charge"),
        ("QVP2902_6_total", "total vertical Noether charge", "Theta_parent(v)=sum_i Theta_i(v)", "Q_v=sum_i Q_v^i", "TOTAL_NOT_PROMOTED", "all sector pieces must be theorem-zero, fixed or finite-sourced in one branch", "Delta_vertical_Noether_charge_total_over_Mref"),
    ]
    return [
        add_common(
            {
                "piece_id": piece_id,
                "sector": sector,
                "theta_piece": theta_piece,
                "Qv_piece": qv_piece,
                "current_status": current_status,
                "missing_to_close": missing_to_close,
                "residual_if_missing": residual_if_missing,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for piece_id, sector, theta_piece, qv_piece, current_status, missing_to_close, residual_if_missing in specs
    ]


def charge_rows() -> list[dict[str, Any]]:
    specs = [
        ("VQL2902_0_kernel_charge", "epsilon_kernel_charge", "abs(int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece))/M_ref", "dimensionless Hamiltonian charge leakage", "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_B_V;MISSING_C_V;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_REF", SRC_2590_KERNEL, "local_GR;Newton;PPN;R10;clock;orbital"),
        ("VQL2902_1_theta_piece", "epsilon_theta_piece_missing", "abs(int_S i_v(Theta_EH+Theta_matter+Theta_extra+Theta_projector+Theta_boundary)_missing)/M_ref", "dimensionless symplectic-potential leakage", "MISSING_SECTOR_THETA_SPLIT;MISSING_M_REF", SRC_2590_SECTORS, "H_tau;M_ref;local_GR"),
        ("VQL2902_2_Qv_piece", "epsilon_Qv_piece_missing", "abs(int_S(Q_v_EH+Q_v_matter+Q_v_extra+Q_v_projector+Q_v_boundary)_missing)/M_ref", "dimensionless vertical charge piece leakage", "MISSING_QV_SECTOR_LEDGER;MISSING_M_REF", SRC_2590_SECTORS, "local_GR;Newton;source_mass"),
        ("VQL2902_3_Bv_ambiguity", "epsilon_Bv_ambiguity", "abs(int_S delta B_v_unfixed)/M_ref", "dimensionless boundary-improvement ambiguity", "MISSING_BV_CONVENTION;MISSING_FIXED_BEFORE_READOUT_CERTIFICATE;MISSING_M_REF", SRC_2393_KERNEL, "clock;orbital;PPN;boundary"),
        ("VQL2902_4_Cv_constraint", "epsilon_Cv_constraint_missing", "abs(int_S C_v_nonconstraint_or_unbounded)/M_ref", "dimensionless constraint leakage", "MISSING_PARENT_CONSTRAINT_SPLIT;MISSING_EOM_SOURCE;MISSING_M_REF", SRC_2590_SECTORS, "Bianchi;conservation;source_current"),
        ("VQL2902_5_integrability", "epsilon_Hv_integrability", "curl_fieldspace int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)/M_ref", "dimensionless field-space curl", "MISSING_FIELDSPACE_CURL_TEST;MISSING_SURFACE_CLASS;MISSING_M_REF", SRC_2590_KERNEL, "Hamiltonian_integrability;clock;orbital"),
        ("VQL2902_TOTAL", "Delta_vertical_Noether_charge_total_over_Mref", "sum_abs(VQL2902_0..VQL2902_5)", "dimensionless_after_M_ref", "COMPONENTS_MISSING", SRC_2590_DOC, "q_owner;Newton;local_GR;PPN;R10;clock;orbital"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "observable_link": observable_link,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, current_value, source_path, observable_link in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    specs = [
        ("EVAL2902_0_Qv_claim", "strict_claim", "Qv_extracted = all(VQC2902_0..6 parent-signed and all QVP2902 sector pieces closed)", "NOT_EVALUATED", "REFUSED_MISSING_PARENT_OBJECTS", "total action, Theta_parent, v action, mu_v, Q_v, C_v, B_v, surface class, integrability and M_ref are missing"),
        ("EVAL2902_1_EH_control", "reference_control", "EH Q_v may be used as a template only after all MTS extra/projector/matter/boundary sectors are zero/fixed/bounded", "REFERENCE_ONLY", "EH_ONLY_IMPORT_REJECTED", "EH charge is not total MTS charge"),
        ("EVAL2902_2_residual_envelope", "nonclaim_residual_envelope", "Delta_vertical_Noether_charge_total_over_Mref=sum_abs(kernel,theta,Qv,Bv,Cv,integrability)", "NOT_EVALUATED", "STAGED_MISSING_COMPONENT_VALUES", "rows have units/source paths but no theorem-zero or numeric values"),
    ]
    return [
        add_common(
            {
                "eval_id": eval_id,
                "mode": mode,
                "formula": formula,
                "computed_value": computed_value,
                "result": result,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for eval_id, mode, formula, computed_value, result, reason in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2902_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2902_1_formal_contract", "vertical Qv extraction route is written", "PASS_NONCLAIM", "delta L, J_v, Q_v, C_v, B_v and delta H_v tests are explicit", True),
        ("GATE2902_2_parent_action_theta", "total L_parent and Theta_parent are extracted", "FAIL", "1008/1009 still leave total current-chain action and theta pieces unsigned", False),
        ("GATE2902_3_vertical_Qv", "Q_v is extracted for current MTS", "FAIL", "vertical generator action, mu_v, Q_v, constraints and sector pieces are missing", False),
        ("GATE2902_4_zero_kernel_flux", "kernel compact flux is zero", "FAIL", "B_v convention, surface class, integrability and zero-flux certificate are missing", False),
        ("GATE2902_5_EH_import", "EH charge alone supplies MTS vertical Q_v", "REJECTED_SHORTCUT", "EH can only be reference/template until retained MTS sectors are closed", False),
        ("GATE2902_6_local_GR", "q/Obs_e, Newton or local-GR can be promoted", "FAIL_CLOSED", "Q_v extraction is upstream and still unclosed", False),
        ("GATE2902_7_next", "sector variation ledger is selected next", "PASS_NONCLAIM", "the next non-cheatable object is the sector split of Theta/mu/Qv/Cv", True),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": gate_passed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason, gate_passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2902_0_Qv_proof", "REFUSED_MISSING_PARENT_OBJECTS", "L_parent;Theta_parent;v action;mu_v;Q_v;C_v;B_v;surface class;integrability;M_ref", 0, "formal route exists but current MTS has no parent-signed extraction"),
        ("RUN2902_1_sector_rows", "STAGED_NONCLAIM_ROWS", "epsilon_theta_piece_missing;epsilon_Qv_piece_missing;epsilon_Bv_ambiguity;epsilon_Cv_constraint_missing;epsilon_Hv_integrability", 0, "sector pieces are explicit but unfilled"),
        ("RUN2902_2_next_sector_ledger", "NEXT_TARGET_SELECTED", "vertical sector variation ledger", 0, "sector split is now the best next derivation target"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2902_0_accept_Qv_contract", "VERTICAL_QV_EXTRACTION_CONTRACT_ACCEPTED", "the right object is a sector-derived Q_v with compact-flux control, not a slogan that the kernel is gauge", "kernel nullness now requires parent variation and sector charge bookkeeping"),
        ("DEC2902_1_no_Qv_claim", "QV_NOT_EXTRACTED_FOR_CURRENT_MTS", "total parent action, Theta_parent, v action, mu_v, Q_v, C_v, B_v, surface class, integrability and M_ref are missing", "epsilon_kernel_charge and Delta_vertical_Noether_charge_total_over_Mref remain nonclaim"),
        ("DEC2902_2_EH_shortcut_refused", "EH_ONLY_CHARGE_IMPORT_REJECTED", "EH charge is a reference anchor only; extra/projector/matter/boundary pieces can carry vertical charge", "no q/Obs_e, Newton, local-GR, PPN, clock or orbital claim is reopened"),
        ("DEC2902_3_next", "VERTICAL_SECTOR_VARIATION_LEDGER_SELECTED_NEXT", "the least-cheatable next step is to split Theta_parent(v), mu_v, Q_v and C_v by sector", "2903 should derive the sector ledger or keep theta/Qv/Cv piece rows nonclaim"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2902_0_2903",
                "status": "selected_primary",
                "target_doc": "2903-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_vertical_sector_variation_ledger_or_Qv_piece_leak_rows_under_AX1090_2903.py",
                "mission": "derive sector pieces of Theta_parent(v), mu_v, Q_v and C_v for EH/local geometry, boundary/reference, extra/residual, projector/source-measure and matter/source sectors",
                "success_condition": "all retained sector pieces are theorem-zero, fixed before readout, constraint-proportional, or source-bounded in one parent branch",
                "fallback_condition": "fill epsilon_theta_piece_missing, epsilon_Qv_piece_missing, epsilon_Cv_constraint_missing and epsilon_Bv_ambiguity with sector source paths and valid_for_claim=false",
                "forbidden": "EH-only total charge; post-readout counterterm; q/Obs_e tautology; fitted M_ref; local-GR/Newton claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2902_0_contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"], "RAB queue copy of Qv extraction contract"),
        ("BR2902_1_sectors_copy", OUTPUTS["sectors"], BRANCH_OUTPUTS["sectors_copy"], "RAB queue copy of Qv sector piece ledger"),
        ("BR2902_2_rows_copy", OUTPUTS["rows"], BRANCH_OUTPUTS["rows_copy"], "local-bounds copy of Qv kernel-charge rows"),
        ("BR2902_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue copy of vertical sector variation next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
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


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def local_source_path_exists(source_path: str) -> bool:
    return Path(source_path).exists()


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    contract_rows_data = all_rows["contract"]
    sector_rows_data = all_rows["sectors"]
    charge_rows_data = all_rows["rows"]
    evaluator_rows_data = all_rows["evaluator"]
    gate_rows_data = all_rows["gates"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "epsilon_kernel_charge",
        "epsilon_theta_piece_missing",
        "epsilon_Qv_piece_missing",
        "epsilon_Bv_ambiguity",
        "epsilon_Cv_constraint_missing",
        "epsilon_Hv_integrability",
        "Delta_vertical_Noether_charge_total_over_Mref",
    }
    found_symbols = {row["symbol"] for row in charge_rows_data}
    value_rows = [row for row in charge_rows_data if row["row_id"] != "VQL2902_TOTAL"]

    checks = [
        ("VAL2902_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2902_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2902_2_contract_refused", any(row["contract_id"] == "VQC2902_7_verdict" and "FAIL" in row["current_status"] for row in contract_rows_data), "Qv extraction remains refused for current MTS"),
        ("VAL2902_3_sector_ledger_present", any(row["piece_id"] == "QVP2902_6_total" for row in sector_rows_data), "sector piece ledger covers retained Qv sectors"),
        ("VAL2902_4_required_rows_present", required_symbols <= found_symbols, "all required Qv residual symbols are present"),
        ("VAL2902_5_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in charge_rows_data), "all Qv rows remain nonclaim"),
        ("VAL2902_6_rows_units_sources", all(row["units"] and local_source_path_exists(row["source_path"]) for row in value_rows), "non-total Qv rows have units and existing source paths"),
        ("VAL2902_7_evaluator_refuses", any(row["eval_id"] == "EVAL2902_0_Qv_claim" and row["result"] == "REFUSED_MISSING_PARENT_OBJECTS" for row in evaluator_rows_data), "strict Qv evaluator refuses missing parent objects"),
        ("VAL2902_8_EH_shortcut_rejected", any(row["gate_id"] == "GATE2902_5_EH_import" and row["result"] == "REJECTED_SHORTCUT" for row in gate_rows_data), "EH-only shortcut rejected"),
        ("VAL2902_9_local_gr_fail_closed", any(row["gate_id"] == "GATE2902_6_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_data), "local GR/Newton remains fail-closed"),
        ("VAL2902_10_next_target_2903", any(row["next_id"] == "NEXT2902_0_2903" and row["selected"] for row in next_rows_data), "2903 sector variation ledger target selected"),
        ("VAL2902_11_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2902_12_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2902_13_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2902_OVERALL", overall, "2902 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2902 - Y5 R2FR Vertical Noether Charge Qv Extraction or Kernel-Charge Source Row Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row-under-AX1090`",
        "Status: `Y5_R2FR_2902_Qv_not_extracted_sector_piece_ledger_source_ready_2903_next`",
        "Claim ceiling: `vertical_Qv_kernel_charge_nonclaim_only_no_q_kernel_owner_source_complex_PiM_lock_epsilon_charge_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2902 tries to turn the q-kernel question into the actual charge calculation. The route is exact, but it does not close for current MTS.",
        "",
        "The required machinery is `delta L_parent = E_A delta Phi^A + dTheta_parent`, a full vertical action `v in ker(Dq)` on every parent sector, `J_v = Theta_parent(v)-mu_v`, `J_v=dQ_v+C_v`, and `delta H_v[S]=int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)`.",
        "",
        "Current MTS has not extracted the total parent action, total `Theta_parent`, `mu_v`, sector `Q_v`, constraint split `C_v`, boundary improvement `B_v`, surface/integrability class, or positive same-frame `M_ref`. EH charge remains a reference template only; importing it as total MTS charge is explicitly rejected.",
        "",
        "The next non-cheatable target is now sector bookkeeping: split `Theta_parent(v)`, `mu_v`, `Q_v`, and `C_v` across EH/local geometry, boundary/reference, extra/residual, projector/source-measure, and matter/source sectors.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Qv Extraction Contract",
        "",
        md_table(all_rows["contract"], ["contract_id", "step", "required_equation", "current_status", "why_it_matters", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Sector Piece Ledger",
        "",
        md_table(all_rows["sectors"], ["piece_id", "sector", "theta_piece", "Qv_piece", "current_status", "missing_to_close", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Kernel Charge Rows",
        "",
        md_table(all_rows["rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Evaluator",
        "",
        md_table(all_rows["evaluator"], ["eval_id", "mode", "computed_value", "result", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(all_rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is a hard but useful result: the gap is not vague. The missing object is the sector-derived vertical charge. If those pieces vanish or are bounded in one parent branch, the q/kernel route gets teeth. If a sector survives, MTS has to own it as a physical residual instead of hiding it in the word gauge.",
        "",
        "## Forbidden Claims From 2902",
        "",
        "- MTS has extracted total `Theta_parent`, `Q_v`, `C_v`, `B_v` or `delta H_v`.",
        "- EH charge alone is the total MTS vertical charge.",
        "- The q-kernel is presymplectic-null or matter-invisible.",
        "- MTS has proved parent q ownership, source-complex ownership, `Pi_M` lock, `epsilon_charge=0`, measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["contract"] = contract_rows()
    all_rows["sectors"] = sector_rows()
    all_rows["rows"] = charge_rows()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "contract", "sectors", "rows", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2902_OVERALL")
    print(f"2902 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
