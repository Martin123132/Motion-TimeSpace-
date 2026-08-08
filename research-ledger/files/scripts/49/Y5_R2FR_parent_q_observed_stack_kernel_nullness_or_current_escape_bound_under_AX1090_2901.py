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

DOC = ROOT / "2901-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090.md"

SRC_2900_DOC = ROOT / "2900-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill-under-AX1090.md"
SRC_2900_NEXT = RESIDUALS / "P8_Y5_R2FR_2900_NEXT_TARGET.csv"
SRC_2900_ESCAPE = RESIDUALS / "P8_Y5_R2FR_2900_JDOMAIN_CURRENT_ESCAPE_ROWS.csv"
SRC_2589_DOC = ROOT / "2589-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"
SRC_2589_AUDIT = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_NULLNESS_AUDIT.csv"
SRC_2589_CERT = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_CERTIFICATE_GATE.csv"
SRC_2589_LEAKS = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_KERNEL_LEAK_ROWS.csv"
SRC_2589_NEXT = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_NEXT_TARGET.csv"
SRC_2392_DOC = ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"
SRC_2392_CERT = RESIDUALS / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv"
SRC_2392_LEAKS = RESIDUALS / "P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv"
SRC_1737_QDQ = ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md"
SRC_2529_QVERT = ROOT / "2529-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md"
SRC_1008_THETA = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
SRC_1760_MATTER = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"
SRC_1756_HIDDEN = ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md"
SRC_2588_OWNER = RESIDUALS / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv"
SRC_2588_LEAKS = RESIDUALS / "P8_Y5_OBS_STACK_2588_SOURCE_LEAK_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2901_SOURCE_REGISTER.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_NULLNESS_AUDIT.csv",
    "certificates": RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CERTIFICATE_GATE.csv",
    "leaks": RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CURRENT_ESCAPE_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2901_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2901_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2901_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2901_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2901_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2901_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "audit_copy": RAB_QUEUE / "JR2901_Q_KERNEL_NULLNESS_AUDIT_NONCLAIM.csv",
    "cert_copy": RAB_QUEUE / "JR2901_Q_KERNEL_CERTIFICATE_GATE_NONCLAIM.csv",
    "leaks_copy": LOCAL_BOUNDS / "Q_observed_stack_kernel_current_escape_rows_2901_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2901_VERTICAL_NOETHER_CHARGE_QV_NEXT.csv",
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
        ("SRC2901_0_2900_doc", SRC_2900_DOC, "parent `q` map with a presymplectic-null;J_domain_current_escape_envelope", "2900 reduces source-complex ownership to q/observed-stack kernel certificate"),
        ("SRC2901_1_2900_next", SRC_2900_NEXT, "NEXT2900_0_2901;ker(Dq) presymplectic-null", "machine-readable 2901 handoff"),
        ("SRC2901_2_2900_escape", SRC_2900_ESCAPE, "epsilon_q_owner;J_domain_current_escape_envelope", "current escape rows inherited from 2900"),
        ("SRC2901_3_2589_doc", SRC_2589_DOC, "V=ker(Dq);epsilon_kernel_charge", "previous vertical-kernel nullness checkpoint"),
        ("SRC2901_4_2589_audit", SRC_2589_AUDIT, "VKN2589_1_presymplectic_null;ROUTE_EXACT_NOT_CLAIMED", "previous nullness audit"),
        ("SRC2901_5_2589_cert", SRC_2589_CERT, "VKC2589_2_theta_Qv;MISSING_THETA_PARENT_AND_QV", "previous certificate gate"),
        ("SRC2901_6_2589_leaks", SRC_2589_LEAKS, "VKL2589_1_kernel_charge;Delta_vertical_kernel_total_over_MH", "previous kernel leak rows"),
        ("SRC2901_7_2589_next", SRC_2589_NEXT, "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction;no EH-only charge import", "previous next target"),
        ("SRC2901_8_2392_doc", SRC_2392_DOC, "V=ker(Dq);Theta_parent", "earlier exact kernel contract"),
        ("SRC2901_9_2392_cert", SRC_2392_CERT, "VKC2392_2_theta_Qv;MISSING_THETA_PARENT_AND_QV", "earlier certificate rows"),
        ("SRC2901_10_2392_leaks", SRC_2392_LEAKS, "epsilon_kernel_charge;MISSING_THETA_PARENT", "earlier kernel-charge leak values"),
        ("SRC2901_11_1737_qdq", SRC_1737_QDQ, "Dq;vertical", "q/Dq vertical basis source"),
        ("SRC2901_12_2529_qvert", SRC_2529_QVERT, "quotient", "psi determinant/quotient map route"),
        ("SRC2901_13_1008_theta", SRC_1008_THETA, "theta_MTS", "parent theta/charge extraction source"),
        ("SRC2901_14_1760_matter", SRC_1760_MATTER, "matter", "matter/worldtube descent source"),
        ("SRC2901_15_1756_hidden", SRC_1756_HIDDEN, "source", "hidden source-slot counterexample ledger"),
        ("SRC2901_16_2588_owner", SRC_2588_OWNER, "OSC2588_1_vertical_kernel;MISSING_PRESYMPLECTIC_NULL_KERNEL", "observed-stack owner certificate requiring kernel nullness"),
        ("SRC2901_17_2588_leaks", SRC_2588_LEAKS, "epsilon_q_owner;Delta_observed_stack_total_over_MH", "observed-stack source leak row requiring kernel proof"),
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


def audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("QK2901_0_q_map", "parent q map", "q:Phi_parent -> Q_vis must be a parent-defined submersion with explicit components, target, Dq and local branch domain", "MISSING_PARENT_Q_MAP", "q remains a target contract, not an owned object", "epsilon_q_owner"),
        ("QK2901_1_vertical_basis", "kernel basis", "V=ker(Dq) must be represented by parent field variations v_i with Dq[v_i]=0 before readout", "MISSING_PARENT_VERTICAL_BASIS", "kernel cannot be tested for charge or matter invisibility", "epsilon_q_rank_or_integrability"),
        ("QK2901_2_rank_integrability", "regular quotient geometry", "rank(Dq) is constant and [v_i,v_j] lies in span(V) with source-backed structure functions on the branch", "MISSING_RANK_AND_BRACKET_AUDIT", "q could be chart/pole dependent rather than a stable quotient", "epsilon_q_rank_or_integrability"),
        ("QK2901_3_presymplectic_null", "vertical CPS charge zero", "delta L_parent=E delta Phi+dTheta_parent and J_v=Theta_parent(v)-i_v L_parent=dQ_v+C_v+dB_v with int_S(delta Q_v-i_v Theta_parent+delta B_v)=0 or bounded", "MISSING_THETA_PARENT_QV_AND_ZERO_FLUX", "vertical directions may carry physical source/boundary charge", "epsilon_kernel_charge"),
        ("QK2901_4_matter_invisible", "matter/source invisibility", "delta_v S_matter=0 and delta_v J_H=0 follow from matter descent through q/e_obs plus fixed constants, lifts, support and no source-only slots", "MISSING_MATTER_DESCENT_AND_NO_SOURCE_SLOT", "ordinary matter could see the hidden directions", "epsilon_matter_kernel;epsilon_hidden_source_slot"),
        ("QK2901_5_basic_observed_stack", "basic e_obs/tau/ell_J stack", "Lie_v e_parent=0, Lie_v tau=0 and Lie_v ell_J=0 or source-bounded for every v_i", "MISSING_BASIC_STACK_CERTIFICATE", "same-frame/current-complex route stays conditional", "epsilon_DObs_e;epsilon_tau_selector;epsilon_ellJ_scale"),
        ("QK2901_6_boundary_history", "boundary/history/support silence", "Pi_local dB_v, history tails, reference terms and source-support variations vanish or enter an absolute envelope", "MISSING_BOUNDARY_HISTORY_SUPPORT_SILENCE", "kernel charge can hide on compact surfaces or in memory tails", "epsilon_boundary_history;E_support_jump"),
        ("QK2901_7_antitautology", "no projection by declaration", "q_candidate may not contain e_obs/tau/source readout as proof objects unless QK2901_1..6 pass independently", "ANTI_TAUTOLOGY_GUARD_ACTIVE", "prevents q=(observed stack) from smuggling in GR-looking frame success", "epsilon_projection_declaration"),
        ("QK2901_8_Mref", "positive same-frame denominator", "M_ref=H_tau-H_ref or Q_M/ell_J is positive and defined in the same q/e_obs/tau branch before normalization", "MISSING_POSITIVE_SAME_FRAME_MREF", "kernel leakage rows cannot be scored as dimensionless claim evidence", "all_normalized_rows"),
        ("QK2901_9_verdict", "parent q observed-stack kernel theorem", "q/e_obs/tau/ell_J are parent-owned and V=ker(Dq) is presymplectic-null, matter-invisible, boundary-silent and regular", "FAIL_CURRENT_MTS_Q_KERNEL_OWNER_NOT_DERIVED", "QK2901_0 through QK2901_8 remain unsigned", "Delta_q_kernel_current_escape_total"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "test_piece": test_piece,
                "formal_statement": formal_statement,
                "derivation_status": derivation_status,
                "current_gain": "exact_contract_or_guard_written",
                "remaining_gap": remaining_gap,
                "residual_if_missing": residual_if_missing,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for audit_id, test_piece, formal_statement, derivation_status, remaining_gap, residual_if_missing in specs
    ]


def certificate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CERT2901_0_q_map", "parent q map", "write q(Phi), Q_vis, Dq and the local branch with constant-rank domain", "MISSING_PARENT_Q_MAP", "epsilon_q_owner"),
        ("CERT2901_1_vertical_basis", "parent vertical basis", "list every v_i as a variation of parent fields and prove Dq[v_i]=0", "MISSING_PARENT_VERTICAL_BASIS", "epsilon_q_rank_or_integrability"),
        ("CERT2901_2_rank_bracket", "rank/involutive distribution", "rank(Dq) constant and [v_i,v_j]=c_ij^k v_k with source-backed coefficient/norm control", "MISSING_RANK_AND_BRACKET_AUDIT", "epsilon_q_rank_or_integrability"),
        ("CERT2901_3_theta_Qv", "Theta_parent and vertical Q_v", "derive delta L_parent=E delta Phi+dTheta_parent and J_v=Theta_parent(v)-i_v L=dQ_v+constraints+improvements", "MISSING_THETA_PARENT_AND_QV", "epsilon_kernel_charge"),
        ("CERT2901_4_zero_compact_flux", "zero compact local flux", "prove int_S(delta Q_v-i_v Theta_parent+boundary/reference improvements)=0 on linked local surfaces", "MISSING_ZERO_COMPACT_FLUX_CERTIFICATE", "epsilon_kernel_charge"),
        ("CERT2901_5_matter_descent", "matter-invisible kernel", "S_matter, constants, matter lifts, worldtube support and Hilbert current descend through q/e_obs for every v_i", "MISSING_MATTER_DESCENT_SIGNATURE", "epsilon_matter_kernel"),
        ("CERT2901_6_no_hidden_source_slot", "no hidden source slot", "exclude direct V_m[v,rho_A,W_source,C_top], source prefactors, material markers, species weights and support selectors outside q", "MISSING_NO_DIRECT_SOURCE_SLOT_PROOF", "epsilon_hidden_source_slot"),
        ("CERT2901_7_basic_stack", "basic observed stack", "Lie_v e_obs=Lie_v tau=Lie_v ell_J=0 or a source-backed finite bound exists", "MISSING_BASIC_STACK_CERTIFICATE", "epsilon_DObs_e;epsilon_tau_selector;epsilon_ellJ_scale"),
        ("CERT2901_8_boundary_history", "boundary/history/reference silence", "Pi_local dB_v=0 and J_history[v]=0 or bounded on compact local domains", "MISSING_BOUNDARY_HISTORY_SILENCE", "epsilon_boundary_history"),
        ("CERT2901_9_Mref", "positive same-frame M_ref", "derive H_tau-H_ref or Q_M/ell_J in the same q/e_obs/tau branch before normalizing leakage", "MISSING_POSITIVE_SAME_FRAME_MREF", "all_normalized_rows"),
        ("CERT2901_10_no_tautology", "non-tautological q promotion", "q/observed-stack promotion is forbidden until independent kernel certificates pass", "PROJECTION_BY_DECLARATION_BLOCK_ACTIVE", "epsilon_projection_declaration"),
    ]
    return [
        add_common(
            {
                "certificate_id": certificate_id,
                "certificate": certificate,
                "required_test": required_test,
                "status": status,
                "residual_if_missing": residual_if_missing,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for certificate_id, certificate, required_test, status, residual_if_missing in specs
    ]


def leak_rows() -> list[dict[str, Any]]:
    specs = [
        ("LEAK2901_0_q_owner", "epsilon_q_owner", "abs(int_S(J_H[q_candidate]-J_H[q_parent]))/M_ref", "dimensionless", "MISSING_PARENT_Q_MAP;MISSING_J_H_DENSITY;MISSING_M_REF", SRC_2588_LEAKS, "source_normalization;PPN;R11;local_GR"),
        ("LEAK2901_1_rank_integrability", "epsilon_q_rank_or_integrability", "norm([v_i,v_j] mod V)+norm(rank(Dq)-rank_expected)", "field-space quotient defect", "MISSING_VERTICAL_BASIS;MISSING_BRACKET_TABLE;MISSING_RANK_AUDIT", SRC_2589_LEAKS, "q_owner;Obs_e;local_GR;PPN"),
        ("LEAK2901_2_kernel_charge", "epsilon_kernel_charge", "abs(int_S(delta Q_v-i_v Theta_parent+boundary_improvements))/M_ref", "dimensionless Hamiltonian charge leakage", "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_BOUNDARY_IMPROVEMENTS;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_REF", SRC_2392_LEAKS, "local_GR;Newton;PPN;R10;clock;orbital"),
        ("LEAK2901_3_matter_kernel", "epsilon_matter_kernel", "abs(delta_v S_matter_on_shell)/M_ref", "dimensionless matter-source leakage", "MISSING_MATTER_DESCENT;MISSING_MATTER_LIFT;MISSING_WORLDTUBE_SUPPORT;MISSING_M_REF", SRC_2392_LEAKS, "WEP;source_normalization;PPN;orbital"),
        ("LEAK2901_4_hidden_source_slot", "epsilon_hidden_source_slot", "abs(partial_v V_m[v,rho_A,W_source,C_top])/M_ref", "dimensionless hidden-source leakage", "MISSING_NO_DIRECT_SLOT_PROOF;MISSING_VM_DENSITY;MISSING_M_REF", SRC_2392_LEAKS, "WEP;source_normalization;R11"),
        ("LEAK2901_5_boundary_history", "epsilon_boundary_history", "abs(int_S Pi_local dB_v + int_history J_history[v])/M_ref", "dimensionless boundary/history leakage", "MISSING_BOUNDARY_FLUX;MISSING_HISTORY_TAIL;MISSING_M_REF", SRC_2392_LEAKS, "R10;clock;orbital;local_GR"),
        ("LEAK2901_6_basic_stack", "epsilon_basic_stack", "||Lie_v e_obs||+||Lie_v tau||+||Lie_v ell_J|| source-weighted", "dimensionless stack response", "MISSING_BASIC_EOBS_TAU_ELLJ_CERTIFICATE", SRC_2588_LEAKS, "same_frame;clock;source_mass;PPN"),
        ("LEAK2901_7_projection_declaration", "epsilon_projection_declaration", "1 if q/Obs_e relies on observed variables inside q before null-kernel proof else 0", "boolean guard", "MISSING_NULL_KERNEL_PROOF", SRC_2588_LEAKS, "q_owner;Obs_e;same_frame"),
        ("LEAK2901_TOTAL", "Delta_q_kernel_current_escape_total", "sum_abs(LEAK2901_0..LEAK2901_7)", "dimensionless_after_common_source_normalization", "COMPONENTS_MISSING", SRC_2900_DOC, "source_complex;epsilon_charge;Newton;PPN;R10;R11;local_GR"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
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
        for row_id, symbol, formula, units, current_value, source_path, observable_link in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    specs = [
        ("EVAL2901_0_q_kernel_claim", "strict_claim", "q_kernel_owner = all(CERT2901_0..CERT2901_10 parent-signed)", "NOT_EVALUATED", "REFUSED_UNSIGNED_CERTIFICATES", "q map, vertical basis, rank/bracket, Theta/Q_v, matter descent, basic stack, boundary/history and M_ref are unsigned"),
        ("EVAL2901_1_cps_control", "conditional_theorem_control", "if V=ker(Dq) is regular, presymplectic-null, matter-invisible and boundary-silent, q/observed-stack promotion is non-tautological", "CONDITIONAL_ONLY", "USEFUL_NOT_CLAIM", "this is the exact test but current MTS lacks the parent objects"),
        ("EVAL2901_2_escape_envelope", "nonclaim_residual_envelope", "Delta_q_kernel_current_escape_total=sum_abs(q_owner,rank,kernel_charge,matter,hidden,boundary,basic_stack,projection_guard)", "NOT_EVALUATED", "STAGED_MISSING_COMPONENT_VALUES", "rows have units/source paths but no theorem-zero or numeric values"),
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
        ("GATE2901_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2901_1_contract_written", "q/kernel contract is explicit", "PASS_NONCLAIM", "V=ker(Dq) is tested as geometry plus charge, not gauge by naming", True),
        ("GATE2901_2_q_map", "parent q map exists", "FAIL", "q components, Dq, target Q_vis and branch domain are not parent-owned", False),
        ("GATE2901_3_rank_basis", "vertical basis/rank/bracket audit exists", "FAIL", "v_i basis, constant rank and involutive bracket table are missing", False),
        ("GATE2901_4_presymplectic_null", "vertical directions have zero compact Noether charge", "FAIL", "Theta_parent, Q_v and zero-flux certificate are missing", False),
        ("GATE2901_5_matter_invisible", "vertical kernel is invisible to matter/source/readout", "FAIL", "matter descent, no hidden source slots, constants, lifts and support are not signed", False),
        ("GATE2901_6_basic_stack", "e_obs/tau/ell_J are basic over q", "FAIL", "basic-stack certificate remains missing", False),
        ("GATE2901_7_projection_guard", "projection-by-declaration is blocked", "PASS_GUARD", "q=(observed stack) cannot count until independent kernel tests pass", True),
        ("GATE2901_8_leak_rows", "kernel current-escape rows are source-ready", "PASS_NONCLAIM", "rows include units and source paths but remain unscored", True),
        ("GATE2901_9_local_GR", "Newton/local-GR source bridge is derived", "FAIL_CLOSED", "q/kernel owner is necessary but not sufficient and currently unproved", False),
        ("GATE2901_10_next", "next target extracts vertical Noether charge Q_v", "PASS_NONCLAIM", "least-cheatable next derivation is the charge calculation", True),
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
        ("RUN2901_0_q_kernel_proof", "REFUSED_UNSIGNED_CERTIFICATES", "q map; vertical basis; rank/bracket; Theta/Q_v; zero flux; matter invisibility; basic stack; boundary/history; M_ref", 0, "current MTS supplies a sharp contract, not the required parent objects"),
        ("RUN2901_1_escape_rows", "STAGED_NONCLAIM_ROWS", "epsilon_q_owner;epsilon_q_rank_or_integrability;epsilon_kernel_charge;epsilon_matter_kernel;epsilon_hidden_source_slot;epsilon_boundary_history;epsilon_basic_stack;epsilon_projection_declaration", 0, "rows are source-ready but missing theorem-zero/numeric values"),
        ("RUN2901_2_next_Qv", "NEXT_TARGET_SELECTED", "Theta_parent and Q_v extraction for vertical variations", 0, "the q/observed-stack proof now depends on vertical Noether charge"),
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
        ("DEC2901_0_accept_kernel_gate", "COVARIANT_PHASE_SPACE_KERNEL_GATE_ACCEPTED", "vertical directions are harmless only when their Noether charge, matter response and boundary/history response vanish or are bounded", "q/observed-stack promotion depends on Theta_parent/Q_v plus matter/boundary certificates"),
        ("DEC2901_1_no_q_promotion", "DO_NOT_PROMOTE_Q_OBSERVED_STACK_OWNER", "q map, vertical basis, rank, CPS charge, matter invisibility and basic stack remain unsigned", "epsilon_q_owner and Delta_q_kernel_current_escape_total stay nonclaim"),
        ("DEC2901_2_no_tautology", "REJECT_Q_BY_DECLARATION", "including e_obs/tau/source readout inside q is not a proof before independent kernel nullness", "projection-declaration remains an explicit guard row"),
        ("DEC2901_3_next", "SELECT_VERTICAL_NOETHER_CHARGE_QV_EXTRACTION", "the least-cheatable next derivation is to calculate Theta_parent and Q_v for v_i", "build 2902 vertical Noether charge Qv extraction or kernel-charge source row"),
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
                "next_id": "NEXT2901_0_2902",
                "status": "selected_primary",
                "target_doc": "2902-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_vertical_Noether_charge_Qv_extraction_or_kernel_charge_source_row_under_AX1090_2902.py",
                "mission": "derive Theta_parent and Q_v for vertical variations and prove int_S(delta Q_v - i_v Theta_parent + boundary improvements)=0 on compact linked local surfaces, or fill epsilon_kernel_charge with source paths, units, denominator status and valid_for_claim=false",
                "forbidden": "EH-only charge import as MTS total; q=(e_obs,...) tautology; fitted M_ref; post-readout counterterm; source-only slot; Newton/local-GR/beta/R10 claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2901_1_rank_parallel",
                "status": "held_parallel",
                "target_doc": "2902b-Y5-R2FR-vertical-basis-rank-bracket-audit-or-epsilon-q-integrability-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_vertical_basis_rank_bracket_audit_or_epsilon_q_integrability_row_under_AX1090_2902b.py",
                "mission": "list v_i, prove v_i in ker(Dq), constant rank and [v_i,v_j] in V, or fill epsilon_q_rank_or_integrability",
                "forbidden": "observed-frame variables as defining kernel without independent nullness",
                "selected": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2901_2_matter_parallel",
                "status": "held_parallel",
                "target_doc": "2902c-Y5-R2FR-matter-boundary-invisibility-or-hidden-source-kernel-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_matter_boundary_invisibility_or_hidden_source_kernel_bound_under_AX1090_2902c.py",
                "mission": "prove delta_v S_matter=0 plus boundary/history/source-support silence for each v_i, or fill matter/hidden/boundary kernel rows",
                "forbidden": "source-prefactor, material-marker, worldtube-support or boundary-tail silence by naming",
                "selected": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2901_0_audit_copy", OUTPUTS["audit"], BRANCH_OUTPUTS["audit_copy"], "RAB queue copy of q/kernel nullness audit"),
        ("BR2901_1_cert_copy", OUTPUTS["certificates"], BRANCH_OUTPUTS["cert_copy"], "RAB queue copy of q/kernel certificate gate"),
        ("BR2901_2_leaks_copy", OUTPUTS["leaks"], BRANCH_OUTPUTS["leaks_copy"], "local-bounds copy of q/kernel current-escape rows"),
        ("BR2901_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue copy of vertical Noether Qv next target"),
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
    audit_rows_data = all_rows["audit"]
    certificate_rows_data = all_rows["certificates"]
    leak_rows_data = all_rows["leaks"]
    evaluator_rows_data = all_rows["evaluator"]
    gate_rows_data = all_rows["gates"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]

    required_symbols = {
        "epsilon_q_owner",
        "epsilon_q_rank_or_integrability",
        "epsilon_kernel_charge",
        "epsilon_matter_kernel",
        "epsilon_hidden_source_slot",
        "epsilon_boundary_history",
        "epsilon_basic_stack",
        "epsilon_projection_declaration",
        "Delta_q_kernel_current_escape_total",
    }
    found_symbols = {row["symbol"] for row in leak_rows_data}
    value_rows = [row for row in leak_rows_data if row["row_id"] != "LEAK2901_TOTAL"]

    checks = [
        ("VAL2901_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2901_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2901_2_audit_verdict_refused", any(row["audit_id"] == "QK2901_9_verdict" and "FAIL" in row["derivation_status"] for row in audit_rows_data), "q/kernel owner theorem remains refused"),
        ("VAL2901_3_certificate_gates_blocked", all(not row["valid_for_claim"] and not row["parent_signed"] for row in certificate_rows_data), "all q/kernel certificates remain nonclaim"),
        ("VAL2901_4_required_leak_rows", required_symbols <= found_symbols, "all required q/kernel leak symbols are present"),
        ("VAL2901_5_leak_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in leak_rows_data), "all leak rows remain nonclaim"),
        ("VAL2901_6_leak_units_sources", all(row["units"] and local_source_path_exists(row["source_path"]) for row in value_rows), "non-total leak rows have units and existing source paths"),
        ("VAL2901_7_evaluator_refuses", any(row["eval_id"] == "EVAL2901_0_q_kernel_claim" and row["result"] == "REFUSED_UNSIGNED_CERTIFICATES" for row in evaluator_rows_data), "strict q/kernel evaluator refuses unsigned certificates"),
        ("VAL2901_8_projection_guard", any(row["gate_id"] == "GATE2901_7_projection_guard" and row["result"] == "PASS_GUARD" for row in gate_rows_data), "projection-by-declaration guard is active"),
        ("VAL2901_9_local_gr_fail_closed", any(row["gate_id"] == "GATE2901_9_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_data), "local GR/Newton remains fail-closed"),
        ("VAL2901_10_next_target_2902", any(row["next_id"] == "NEXT2901_0_2902" and row["selected"] for row in next_rows_data), "2902 vertical Noether charge Qv target selected"),
        ("VAL2901_11_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2901_12_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2901_13_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2901_OVERALL", overall, "2901 validation overall"))
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
        "# 2901 - Y5 R2FR Parent q Observed-Stack Kernel Nullness or Current-Escape Bound Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-parent-q-observed-stack-kernel-nullness-or-current-escape-bound-under-AX1090`",
        "Status: `Y5_R2FR_2901_q_kernel_owner_not_derived_CPS_charge_gate_source_ready_Qv_2902_next`",
        "Claim ceiling: `q_kernel_current_escape_nonclaim_only_no_source_complex_owner_PiM_lock_epsilon_charge_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2901 attacks the upstream question left by 2900: can the observed stack be treated as a real parent quotient rather than a projection label?",
        "",
        "The answer for current MTS is still no, but the shape is now exact. A parent `q` route is claim-grade only if `q:Phi_parent -> Q_vis` is written with an explicit `Dq`, a regular vertical distribution `V=ker(Dq)`, and every vertical generator is presymplectic-null, matter-invisible, boundary/history silent, and invisible to the basic `e_obs/tau/ell_J` stack.",
        "",
        "That is not philosophy; it is a covariant phase-space charge calculation. The core test is `delta L_parent = E delta Phi + dTheta_parent`, `J_v = Theta_parent(v)-i_v L_parent = dQ_v + C_v + dB_v`, and zero or source-bounded compact flux `int_S(delta Q_v - i_v Theta_parent + delta B_v)`.",
        "",
        "Current MTS has not supplied the parent `q` map, vertical basis, rank/bracket audit, `Theta_parent/Q_v`, matter-invisibility proof, boundary/history silence, or positive same-frame `M_ref`. So the route stays alive but nonclaim, and the next best move is the vertical Noether charge extraction.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## q/Kernel Nullness Audit",
        "",
        md_table(all_rows["audit"], ["audit_id", "test_piece", "formal_statement", "derivation_status", "remaining_gap", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Certificate Gate",
        "",
        md_table(all_rows["certificates"], ["certificate_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"]),
        "",
        "## q/Kernel Current-Escape Rows",
        "",
        md_table(all_rows["leaks"], ["row_id", "symbol", "formula", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
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
        "This is a useful contraction of the problem. If we can get `Q_v` and show its compact flux vanishes for the true vertical directions, the observed-stack route becomes much more serious. If it fails, the failure is not vague: it is a kernel charge/source residual with units, source paths and no permission to hide inside measured `GM`.",
        "",
        "## Forbidden Claims From 2901",
        "",
        "- MTS has proved parent `q/e_obs/tau/ell_J` ownership.",
        "- MTS has proved `V=ker(Dq)` is presymplectic-null, matter-invisible, boundary-silent or regular.",
        "- MTS may promote `q=(e_obs,...)` by definition.",
        "- MTS has proved the source-worldtube/current-complex owner theorem, `Pi_M` lock, `epsilon_charge=0`, measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["audit"] = audit_rows()
    all_rows["certificates"] = certificate_rows()
    all_rows["leaks"] = leak_rows()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "audit", "certificates", "leaks", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2901_OVERALL")
    print(f"2901 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
