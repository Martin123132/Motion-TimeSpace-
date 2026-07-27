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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2829-Y5-R2FR-qbasic-public-coframe-no-source-prefactor-or-finite-vmq-acquisition-under-AX1090.md"

SRC_2828_NEXT = RESIDUALS / "P8_Y5_R2FR_2828_NEXT_TARGET.csv"
SRC_2828_FINITE = RESIDUALS / "P8_Y5_R2FR_2828_FIRST_FINITE_VMQ_Q_SOURCE_ROW_NONCLAIM.csv"
SRC_2828_ZERO = RESIDUALS / "P8_Y5_R2FR_2828_VMQ_ZERO_PROOF_AUDIT.csv"
SRC_2828_OWNER = RESIDUALS / "P8_Y5_R2FR_2828_MATTER_SOURCE_OWNER_LEDGER.csv"
SRC_2827_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2827_DQVM_DERIVATION_LEDGER.csv"
SRC_2486_MATTER = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv"
SRC_2486_THEOREM = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_THEOREM_ATTEMPT.csv"
SRC_2486_RESIDUAL = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_RESIDUAL_OWNER_SPLIT.csv"
SRC_1896_NOHOM = RESIDUALS / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv"
SRC_2466_HILBERT = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv"
SRC_2466_WEP = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_WEP_COMPOSITION_GUARDRAIL.csv"
SRC_2488_ACTION = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ACTION_DOMAIN_ATTEMPT.csv"
SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2489_RETRY = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PARENT_NO_SHADOW_RETRY.csv"
SRC_2489_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESIDUAL_VECTOR_INTERFACE.csv"
SRC_2489_GATES = RESIDUALS / "P8_Y5_NO_SHADOW_2489_CLAIM_GATES.csv"
SRC_2632_RESIDUAL = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_RESIDUAL_OWNER_LEDGER.csv"
SRC_2632_FRONTIER = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_LOCAL_GR_FRONTIER_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2829_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2829_QBASIC_NO_SOURCE_PREFACTOR_THEOREM_AUDIT.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2829_EPSILON_VMQ_SOURCE_READY_ACQUISITION_ROWS.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2829_EPSILON_VMQ_RESPONSE_KERNEL_REQUIREMENTS.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2829_CQM_AND_ARENA_READINESS_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2829_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2829_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2829_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2829_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2829_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": SOURCE_WEIGHT / "qbasic_no_source_prefactor_theorem_audit_2829_NONCLAIM.csv",
    "acquisition_copy": LOCAL_BOUNDS / "epsilon_vmq_source_ready_acquisition_rows_2829_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2829_EPSILON_VMQ_RESPONSE_KERNELS_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_QBASIC_PUBLIC_COFRAME_NO_SOURCE_PREFACTOR_2829"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2829_0_2828_next", SRC_2828_NEXT, "NEXT2828_0_2829", "2828 handoff selecting q-basic/no-source-prefactor or finite vmq acquisition"),
        ("SRC2829_1_2828_finite", SRC_2828_FINITE, "FVQ2828_0_first_row;FVQ2828_1_source_weight_shadow;FVQ2828_2_readout_shadow", "finite vmq rows staged by 2828"),
        ("SRC2829_2_2828_zero", SRC_2828_ZERO, "ZPA2828_1_qbasic_matter;ZPA2828_6_verdict", "2828 zero proof audit"),
        ("SRC2829_3_2828_owner", SRC_2828_OWNER, "OWN2828_3_q_source;OWN2828_5_readout", "2828 source-owner separation"),
        ("SRC2829_4_2827_derivation", SRC_2827_DERIVATION, "DER2827_6_matter_generator_condition", "exact Dq[v_m] kernel condition"),
        ("SRC2829_5_2486_matter", SRC_2486_MATTER, "MD2486_0_chain_rule;MD2486_1_no_source_prefactor", "matter descent and source-prefactor blockers"),
        ("SRC2829_6_2486_theorem", SRC_2486_THEOREM, "THM2486_1_matter_blindness;THM2486_2_current_signature_application", "conditional matter blindness and failed current signature"),
        ("SRC2829_7_2486_residual", SRC_2486_RESIDUAL, "RS2486_1_q_source;RS2486_3_matter_descent", "q-source and matter-descent residual owners"),
        ("SRC2829_8_1896_nohom", SRC_1896_NOHOM, "NH1896_1_conditional_typed_proof;NH1896_5_verdict", "no-Hom theorem conditional but unsigned"),
        ("SRC2829_9_2466_hilbert", SRC_2466_HILBERT, "HIL2466_0_define_T;HIL2466_4_matter_A_coupling", "Hilbert stress route and coupling unification blocker"),
        ("SRC2829_10_2466_wep", SRC_2466_WEP, "WEP2466_0_hilbert_universal;WEP2466_3_composition_bound", "WEP/source-composition guardrail"),
        ("SRC2829_11_2488_action", SRC_2488_ACTION, "AD2488_0_terminal_public_coframe;AD2488_4_verdict", "terminal public coframe action-domain attempt"),
        ("SRC2829_12_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "exact conditional no-shadow theorem and failure verdict"),
        ("SRC2829_13_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_2_source_prefactor", "common Weyl/source-prefactor countermodels"),
        ("SRC2829_14_2489_retry", SRC_2489_RETRY, "PNC2489_0_terminal_public_action_domain;PNC2489_3_verdict", "parent no-shadow retry remains unsigned"),
        ("SRC2829_15_2489_vector", SRC_2489_VECTOR, "PPNV2489_1_bR;PPNV2489_4_wR;PPNV2489_7_total_abs", "PPN residual vector components for finite rows"),
        ("SRC2829_16_2489_gates", SRC_2489_GATES, "GATE2489_1_parent_no_shadow;GATE2489_4_local_GR_Newton", "claim gates blocked"),
        ("SRC2829_17_2632_residual", SRC_2632_RESIDUAL, "RES2632_0_Delta_w_eff;RES2632_4_DObs_e_R", "rollforward residual owners for source-weight/readout leaks"),
        ("SRC2829_18_2632_frontier", SRC_2632_FRONTIER, "GRF2632_3_quotient_readout;GRF2632_4_full_PPN", "readout and PPN frontier blockers"),
    ]
    return [source_row(*spec) for spec in specs]


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        ("THA2829_0_exact_Dq_gate", "Dq[v_m]=0 iff v_m^q=0", "CLOSED_FROM_2827", "exact kernel condition exists", "does not prove v_m is q-basic", SRC_2827_DERIVATION, "DER2827_6_matter_generator_condition"),
        ("THA2829_1_terminal_public_coframe", "ordinary observables factor through terminal e_pub=E(Q_vis)", "CANDIDATE_NOT_PARENT_DERIVED", "2488 states the correct terminal public coframe condition", "terminality and Q_vis ownership are not parent-derived", SRC_2488_ACTION, "AD2488_0_terminal_public_coframe"),
        ("THA2829_2_no_frame_slot", "ordinary matter/readout excludes C_R/J_q Weyl/disformal slots", "CLOSURE_ONLY_NOT_DERIVED", "2488 supplies action-domain exclusion target", "common Weyl/disformal countermodels survive covariance and same-frame slogans", SRC_2488_ACTION, "AD2488_1_no_C_frame_slot"),
        ("THA2829_3_no_source_prefactor", "ordinary matter excludes source-only w_A(C_R) prefactors", "NOT_DERIVED", "2486/2488/1896 agree this is the required theorem", "object-language admissibility, no-Hom, readout/measure stability remain unsigned", SRC_2486_MATTER, "MD2486_1_no_source_prefactor"),
        ("THA2829_4_nohom", "no species/hidden-marker morphism into active source coefficients", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "typed/product proof exists conditionally", "parent sort derivation, hidden-invariant/no-marker exclusion and readout stability remain open", SRC_1896_NOHOM, "NH1896_5_verdict"),
        ("THA2829_5_hilbert_public_source", "single Hilbert source through public geometry", "PASS_CONDITIONAL_NONCLAIM", "Hilbert route is universal and WEP-friendlier", "tau/ell_J ownership, A-coupling unification, and source-shadow zero are not signed", SRC_2466_HILBERT, "HIL2466_4_matter_A_coupling"),
        ("THA2829_6_inheritance_stack", "connection, tau, source support, boundary endpoints inherit e_pub", "INHERITANCE_STACK_UNSIGNED", "2488 names the exact inheritance stack", "connection descent, tau pushforward, endpoint silence and local projection remain open", SRC_2488_ACTION, "AD2488_3_connection_tau_boundary_inherit"),
        ("THA2829_7_current_verdict", "q-basic/no-source-prefactor theorem closes v_m^q=0", "THEOREM_NOT_DERIVED_CURRENT_CORPUS", "exact conditional theorem exists but premises remain contracts", "finite epsilon_vmq acquisition rows are required", SRC_2488_ZERO, "ZTH2488_2_current_verdict"),
    ]
    return [
        nonclaim(
            {
                "theorem_audit_id": audit_id,
                "clause": clause,
                "status": status,
                "supporting_evidence": evidence,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "theorem_zero_proved": False,
                "finite_acquisition_required": audit_id == "THA2829_7_current_verdict",
                "control_only": True,
            }
        )
        for audit_id, clause, status, evidence, blocker, source_path, anchor in specs
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2829_0_epsilon_vmq_total", "epsilon_vmq", "total matter-generator q-component", "epsilon_vmq := ||v_m^q||_{Q_log,*} or ||Dq[v_m]||_{E_q} after E_q/v_m normalization", "MISSING_EQ_NORM;MISSING_VM_NORMALIZATION;MISSING_QBASIC_PUBLIC_COFRAME;MISSING_NO_SOURCE_PREFACTOR", "source theorem-zero from THA2829 or acquire finite bound from component envelope", "PPN;R10;clocks;orbital;local_GR", SRC_2828_FINITE, "FVQ2828_0_first_row"),
        ("ACQ2829_1_source_weight", "epsilon_vmq_source_weight", "source-only prefactor q leak", "finite q-component induced by w_A(C_R) or source-weight current that does not descend through Q_vis", "MISSING_PARENT_NOHOM;MISSING_READOUT_MEASURE_STABILITY;MISSING_WEP_KERNEL", "prove no-Hom/no-source-prefactor or acquire WEP/source-normalization bound", "WEP;source_normalization;local_GR;PPN", SRC_2828_FINITE, "FVQ2828_1_source_weight_shadow"),
        ("ACQ2829_2_readout", "epsilon_vmq_readout", "public coframe/readout q leak", "finite q-component from DObs_e_R, endpoint, boundary or post-readout gauge tail", "MISSING_DOBS_KERNEL;MISSING_TERMINAL_PUBLIC_COFRAME;MISSING_ENDPOINT_SILENCE", "prove terminal public coframe/inheritance stack or acquire readout response kernels", "PPN;clocks;orbital;local_GR", SRC_2828_FINITE, "FVQ2828_2_readout_shadow"),
        ("ACQ2829_3_common_weyl", "b_R_to_vmq", "common Weyl q leak", "e_obs = exp(b_R C_R)e_pub response component mapped into v_m^q envelope", "MISSING_PARENT_NO_SHADOW;MISSING_B_R_VALUE;MISSING_GAMMA_KERNEL", "prove no Weyl slot or source b_R response coefficient", "PPN_gamma;clocks;orbital", SRC_2488_COUNTER, "CM2488_0_common_weyl"),
        ("ACQ2829_4_disformal", "d_R_to_vmq", "disformal/preferred-frame q leak", "g_obs = A(C_R)^2 g_pub + D(C_R)u_mu u_nu mapped into preferred-frame residual", "MISSING_NO_DISFORMAL_SLOT;MISSING_D_R_VALUE;MISSING_PREFERRED_FRAME_KERNEL", "prove no disformal slot or source d_R preferred-frame response", "PPN_alpha1;PPN_alpha2;clocks", SRC_2488_COUNTER, "CM2488_1_common_disformal"),
        ("ACQ2829_5_endpoint", "epsilon_endpoint_to_vmq", "endpoint/boundary q leak", "boundary or endpoint dependence P_loc partial_Q_endpoint E contributes to q-source envelope", "MISSING_ENDPOINT_SILENCE;MISSING_BOUNDARY_KERNEL", "prove endpoint silence or acquire orbital/light-time endpoint bound", "orbital;R10;local_GR;light_time", SRC_2488_COUNTER, "CM2488_3_endpoint_boundary"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, component, definition, blockers, acquisition_path, arenas, source_path, anchor in specs:
        rows.append(
            nonclaim(
                {
                    "acquisition_id": row_id,
                    "symbol": symbol,
                    "component": component,
                    "definition": definition,
                    "units_required": "same q_log/E_q/v_m normalization before scoring",
                    "value_status": "MISSING_NUMERIC_VALUE",
                    "source_status": "MISSING_SOURCE_BACKED_VALUE_OR_THEOREM_ZERO",
                    "blockers": blockers,
                    "acquisition_path": acquisition_path,
                    "test_arenas": arenas,
                    "source_path": str(source_path),
                    "source_anchor": anchor,
                    "anchor_found": anchor in read_text(source_path),
                    "ready_for_acquisition": True,
                    "numeric_value_present": False,
                    "source_backed_value": False,
                    "theorem_zero": False,
                    "control_only": True,
                }
            )
        )
    return rows


def kernel_rows() -> list[dict[str, Any]]:
    specs = [
        ("KREQ2829_0_Cqm", "C_qm", "C_qm=||Dq[v_m]||_{E_q}", "requires E_q norm, v_m normalization, epsilon_vmq value or theorem-zero", "MISSING_EQ_NORM_AND_VALUE", SRC_2828_FINITE, "FVQ2828_0_first_row"),
        ("KREQ2829_1_PPN", "PPN response", "Delta_PPN_abs from q/source/readout components", "requires b_R,d_R,w_R,endpoint/readout kernels and no-cancellation envelope", "MISSING_PPN_VECTOR_VALUES", SRC_2489_VECTOR, "PPNV2489_7_total_abs"),
        ("KREQ2829_2_WEP", "WEP/source-weight response", "finite source-prefactor maps into composition/source normalization residual", "requires material/source tensor and WEP projection for epsilon_vmq_source_weight", "MISSING_WEP_SOURCE_KERNEL", SRC_2466_WEP, "WEP2466_3_composition_bound"),
        ("KREQ2829_3_clocks", "clock response", "tau/public coframe q leak maps into clock drift/preferred-frame residual", "requires tau inheritance or clock response kernel", "MISSING_CLOCK_KERNEL", SRC_2488_ACTION, "AD2488_3_connection_tau_boundary_inherit"),
        ("KREQ2829_4_orbital", "orbital/light-time response", "endpoint/boundary/readout q leak maps into orbital/light-time residual", "requires endpoint silence or finite orbital kernel", "MISSING_ORBITAL_ENDPOINT_KERNEL", SRC_2488_COUNTER, "CM2488_3_endpoint_boundary"),
        ("KREQ2829_5_R10", "R10/local short-range response", "finite epsilon_vmq maps into local q-source residual envelope", "requires R10 projection map in same q/E_q normalization", "MISSING_R10_PROJECTION_KERNEL", SRC_2486_RESIDUAL, "RS2486_1_q_source"),
    ]
    return [
        nonclaim(
            {
                "kernel_req_id": req_id,
                "kernel": kernel,
                "formula_or_map": formula,
                "required_inputs": required,
                "current_status": status,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "kernel_ready": False,
                "score_ready": False,
                "control_only": True,
            }
        )
        for req_id, kernel, formula, required, status, source_path, anchor in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("READY2829_0_theorem", "q-basic/no-source-prefactor theorem", "NOT_READY", "terminal public coframe, no frame slot, no source-prefactor, inheritance stack and no-Hom are unsigned", False),
        ("READY2829_1_acquisition", "epsilon_vmq acquisition rows", "READY_FOR_SOURCE_ACQUISITION_NONCLAIM", "rows have symbols, definitions, blockers, arenas and source anchors, but no values", False),
        ("READY2829_2_Cqm", "C_qm", "NOT_READY", "E_q norm, v_m normalization and epsilon_vmq value/theorem-zero missing", False),
        ("READY2829_3_local_lock", "local-lock reentry", "NOT_READY", "C_qm and source norm remain blocked", False),
        ("READY2829_4_empirical", "PPN/R10/clock/orbital scoring", "NOT_READY", "response kernels and source-backed values are missing", False),
    ]
    return [
        nonclaim(
            {
                "readiness_id": readiness_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "promotion_allowed": allowed,
                "control_only": True,
            }
        )
        for readiness_id, obj, status, reason, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    theorem_anchors = all(row["anchor_found"] for row in rows["theorem"])
    theorem_failed = any(row["theorem_audit_id"] == "THA2829_7_current_verdict" and row["status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in rows["theorem"])
    acquisition_ready = all(row["anchor_found"] and row["ready_for_acquisition"] and not row["numeric_value_present"] and not row["theorem_zero"] for row in rows["acquisition"])
    kernels_blocked = not any(row["kernel_ready"] for row in rows["kernel"])
    reentry_blocked = not any(row["promotion_allowed"] for row in rows["reentry"])
    specs = [
        ("CG2829_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2829_1_theorem_audit", "q-basic/no-source-prefactor theorem audited", theorem_anchors, "every theorem clause cites source evidence"),
        ("CG2829_2_theorem_zero", "v_m^q theorem-zero proved", False, "required parent action-domain/no-Hom/readout clauses remain unsigned"),
        ("CG2829_3_theorem_not_overclaimed", "theorem failure recorded honestly", theorem_failed, "conditional theorem is not promoted"),
        ("CG2829_4_acquisition_rows", "epsilon_vmq source-ready rows staged", acquisition_ready, "rows are acquisition-ready but nonclaim and value-missing"),
        ("CG2829_5_response_kernels", "response kernels ready for scoring", False, "kernel requirements are named but not filled"),
        ("CG2829_6_kernels_blocked", "response kernels blocked", kernels_blocked, "no kernel row is score-ready"),
        ("CG2829_7_Cqm", "C_qm promotable", False, "E_q/v_m/epsilon_vmq inputs missing"),
        ("CG2829_8_reentry_blocked", "local-lock and arena reentry blocked", reentry_blocked, "no promotion readiness row allows claims"),
        ("CG2829_9_GR_Newton", "local GR/Newton claim allowed", False, "q=0 selector, Newton-source normalization and epsilon_vmq zero/value remain missing"),
        ("CG2829_10_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "finite rows and response kernels lack source-backed values"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2829_0_theorem", "The q-basic/no-source-prefactor theorem still does not close.", "THEOREM_NOT_DERIVED", "2488/2489 give an exact conditional theorem but the parent action-domain/no-Hom/readout premises remain unsigned", "do not claim v_m^q=0"),
        ("DEC2829_1_gain", "Finite epsilon_vmq rows are now source-ready.", "ACQUISITION_READY_NONCLAIM", "the coupling debt has symbols, definitions, blockers, source anchors and arenas", "use these rows for theorem-zero or bound acquisition"),
        ("DEC2829_2_Cqm", "C_qm remains blocked.", "NO_CQM_PROMOTION", "epsilon_vmq has no value/theorem-zero and E_q/v_m normalization is missing", "do not reenter local-lock amplitude chain"),
        ("DEC2829_3_tests", "Do not run empirical scores yet.", "NO_SCORE_READY_KERNELS", "PPN/R10/clock/orbital response kernels are named but not sourced", "build response-kernel/source-acquisition interface next"),
        ("DEC2829_4_next", "Next target is epsilon_vmq response kernels and source acquisition.", "NEXT_2830_RESPONSE_KERNELS", "this is the bridge from derivation debt to testable finite residuals without cheating", "build kernel/source intake rows for epsilon_vmq components"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2829_0_2830",
                "status": "selected_primary",
                "target_doc": "2830-Y5-R2FR-epsilon-vmq-response-kernels-and-source-acquisition-interface-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_epsilon_vmq_response_kernels_and_source_acquisition_interface_under_AX1090_2830.py",
                "mission": "turn the source-ready epsilon_vmq finite rows into response-kernel/source-acquisition interfaces for PPN, R10, clocks, orbital and local-GR gates without claiming any score",
                "acceptance": "must cite 2829 acquisition rows and kernel requirements; must keep values missing unless sourced; no C_qm promotion; no local GR/Newton/PPN/R10 claim; formalization-workbench untouched",
                "forbidden": "do not insert numeric placeholders; do not treat acquisition-ready as evidence; do not run empirical scoring",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2829_0_theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"], "source-weight copy of q-basic/no-source-prefactor theorem audit"),
        ("BR2829_1_acquisition_copy", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"], "local-bounds copy of source-ready epsilon_vmq acquisition rows"),
        ("BR2829_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for epsilon_vmq response-kernel target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_numeric_keys = {"numeric_value", "coefficient", "alpha", "beta", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2829_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2829_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2829_2_theorem_anchors", all(row["anchor_found"] for row in rows_by_name["theorem"]), "all theorem-audit rows cite found anchors"),
        ("VAL2829_3_theorem_not_proved", any(row["theorem_audit_id"] == "THA2829_7_current_verdict" and row["status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["theorem"]), "q-basic/no-source-prefactor theorem fails honestly"),
        ("VAL2829_4_acquisition_rows_ready", all(row["ready_for_acquisition"] for row in rows_by_name["acquisition"]), "epsilon_vmq rows are source-ready for acquisition"),
        ("VAL2829_5_acquisition_nonclaim", all(not row["numeric_value_present"] and not row["source_backed_value"] and not row["theorem_zero"] for row in rows_by_name["acquisition"]), "epsilon_vmq rows remain nonclaim/value-missing"),
        ("VAL2829_6_kernels_blocked", not any(row["kernel_ready"] or row["score_ready"] for row in rows_by_name["kernel"]), "response kernels remain blocked/non-score-ready"),
        ("VAL2829_7_Cqm_blocked", not any(row["promotion_allowed"] for row in rows_by_name["reentry"]), "C_qm/local-lock/arena reentry remains blocked"),
        ("VAL2829_8_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local GR/Newton/PPN/R10"),
        ("VAL2829_9_no_numeric_insertions", no_numeric_insertions(rows_by_name), "no numeric coefficients or prediction values inserted"),
        ("VAL2829_10_next_target_2830", any(row["next_id"] == "NEXT2829_0_2830" and row["selected"] for row in rows_by_name["next"]), "epsilon_vmq response-kernel target selected next"),
        ("VAL2829_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2829_12_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2829_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2829_14_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2829_15_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2829_16_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2829_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2829_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2829_OVERALL",
            "passed": overall,
            "detail": "2829 audits the q-basic public coframe/no-source-prefactor theorem, finds it still conditional, converts epsilon_vmq into source-ready finite acquisition rows, blocks C_qm/local-lock/arena scoring, and selects response-kernel/source-acquisition interface next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2829 - Y5 R2FR qbasic Public Coframe No Source Prefactor Or Finite vmq Acquisition Under AX1090

Status: `Y5_R2FR_2829_qbasic_no_source_prefactor_not_derived_epsilon_vmq_source_ready_nonclaim`

## Private Verdict

2829 tries the theorem route one more time, with the right clauses:

`terminal public coframe + no Weyl/disformal frame slot + no source-only prefactor + no-Hom source typing + inheritance stack`.

The result is not a closure. The exact conditional theorem is sharp, but the parent action-domain grammar is still not signed. So `v_m^q=0` is still not proved.

The useful gain is that `epsilon_vmq` is now source-ready: the rows have symbols, definitions, blockers, source anchors, and test arenas. They still have no values, no theorem-zero status, and no claim permission.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## qbasic No Source Prefactor Theorem Audit

{markdown_table(rows["theorem"], ["theorem_audit_id", "clause", "status", "supporting_evidence", "blocker", "theorem_zero_proved", "finite_acquisition_required", "valid_for_claim"])}

## epsilon_vmq Source Ready Acquisition Rows

{markdown_table(rows["acquisition"], ["acquisition_id", "symbol", "component", "definition", "value_status", "source_status", "blockers", "test_arenas", "ready_for_acquisition", "valid_for_claim"])}

## epsilon_vmq Response Kernel Requirements

{markdown_table(rows["kernel"], ["kernel_req_id", "kernel", "formula_or_map", "required_inputs", "current_status", "kernel_ready", "score_ready", "valid_for_claim"])}

## Cqm And Arena Readiness Status

{markdown_table(rows["reentry"], ["readiness_id", "object", "status", "reason", "promotion_allowed", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["theorem"] = theorem_rows()
    rows["acquisition"] = acquisition_rows()
    rows["kernel"] = kernel_rows()
    rows["reentry"] = reentry_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "theorem", "acquisition", "kernel", "reentry", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2829_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2829_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
