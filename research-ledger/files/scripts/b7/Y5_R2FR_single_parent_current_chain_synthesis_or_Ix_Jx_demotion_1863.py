from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1863"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1863-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_SOURCE_REGISTER.csv",
    "parent_current_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_PARENT_CURRENT_CONTRACT.csv",
    "single_chain_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_SINGLE_PARENT_CHAIN_AUDIT.csv",
    "ix_jx_demotion": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_IX_JX_DEMOTION_LEDGER.csv",
    "finite_residual_requirements": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_FINITE_RESIDUAL_REQUIREMENTS.csv",
    "local_gr_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_LOCAL_GR_IMPACT.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1863_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1863_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def path_has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1863_0_1862_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            "required_needle": "NEXT1862_0_primary",
            "use_in_1863": "selects the single parent current chain synthesis or I_X/J_X demotion target.",
        },
        {
            "source_id": "SRC1863_1_1862_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1862_VALIDATION.csv",
            "required_needle": "VAL1862_OVERALL",
            "use_in_1863": "confirms the previous checkpoint passed before this synthesis begins.",
        },
        {
            "source_id": "SRC1863_2_1801_jx_doc",
            "source_kind": "JX_source_gate",
            "source_path": ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
            "required_needle": "JX_SOURCE_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED",
            "use_in_1863": "imports the source-zero failure and no-cancellation component policy for J_X.",
        },
        {
            "source_id": "SRC1863_3_1801_source_silence_csv",
            "source_kind": "JX_source_gate_csv",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_SOURCE_SILENCE_GATE.csv",
            "required_needle": "JZS1801_8_verdict",
            "use_in_1863": "provides the channelwise J_X silence verdict.",
        },
        {
            "source_id": "SRC1863_4_1801_bound_pack",
            "source_kind": "component_bound_schema",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_COMPONENT_BOUND_PACK.csv",
            "required_needle": "JCB1801_5_total_abs_guard",
            "use_in_1863": "provides the absolute no-cancellation J_X component envelope.",
        },
        {
            "source_id": "SRC1863_5_1802_matter_readout_doc",
            "source_kind": "matter_readout_gate",
            "source_path": ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
            "required_needle": "JMatter_AND_READOUT_ZERO_NOT_SIGNED",
            "use_in_1863": "imports the matter/readout conditional theorem and unsigned parent signature.",
        },
        {
            "source_id": "SRC1863_6_1802_theorem_csv",
            "source_kind": "matter_readout_csv",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
            "required_needle": "MRT1802_7_verdict",
            "use_in_1863": "records the exact parent-unsigned theorem gate for matter/readout silence.",
        },
        {
            "source_id": "SRC1863_7_1802_qbar_rows",
            "source_kind": "qbar_readout_rows",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_QBAR_READOUT_COMPONENT_ROWS.csv",
            "required_needle": "QRC1802_5_total_abs_guard",
            "use_in_1863": "imports the qbar/readout absolute envelope rows.",
        },
        {
            "source_id": "SRC1863_8_1803_hidden_couplings",
            "source_kind": "hidden_coupling_gate",
            "source_path": ROOT / "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md",
            "required_needle": "HIDDEN_COUPLINGS_RETAINED",
            "use_in_1863": "imports hidden Weyl/disformal, marker, source-prefactor and nonminimal countermodels.",
        },
        {
            "source_id": "SRC1863_9_1804_constants",
            "source_kind": "constant_sector_gate",
            "source_path": ROOT / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md",
            "required_needle": "ALPHA_MASS_CLOCK_CHANNELS_RETAINED",
            "use_in_1863": "imports the dimensionless alpha/mass/clock constant-sector debt.",
        },
        {
            "source_id": "SRC1863_10_1849_qbarXT_doc",
            "source_kind": "active_qbarXT_branch",
            "source_path": ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            "required_needle": "QZ1849_6_verdict",
            "use_in_1863": "ports qbar_XT source-zero into the active parent-q_loc branch and keeps it nonclaim.",
        },
        {
            "source_id": "SRC1863_11_1849_qbarXT_csv",
            "source_kind": "qbarXT_component_envelope",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv",
            "required_needle": "QBC1849_5_total_abs_guard",
            "use_in_1863": "provides the current qbar_XT absolute component envelope.",
        },
        {
            "source_id": "SRC1863_12_1855_minimal_clause",
            "source_kind": "minimal_X_closure_candidate",
            "source_path": ROOT / "1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md",
            "required_needle": "CLOSURE_CANDIDATE_NOT_MTS_DERIVATION",
            "use_in_1863": "shows the scalar/EFT closure clause is coherent but not derived from MTS primitives.",
        },
        {
            "source_id": "SRC1863_13_1856_physical_scalar_rejection",
            "source_kind": "physical_X_branch_decision",
            "source_path": ROOT / "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md",
            "required_needle": "REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH",
            "use_in_1863": "keeps the derived-local-GR route constraint/auxiliary first rather than physical scalar first.",
        },
        {
            "source_id": "SRC1863_14_1857_constraint_route",
            "source_kind": "constraint_local_GR_route",
            "source_path": ROOT / "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
            "required_needle": "FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED",
            "use_in_1863": "imports the clean conditional auxiliary/constraint local-GR theorem with unsigned premises.",
        },
        {
            "source_id": "SRC1863_15_1859_parent_euler_bridge",
            "source_kind": "best_surviving_route",
            "source_path": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            "required_needle": "SELECT_AS_PARENT_EULER_BRIDGE",
            "use_in_1863": "selects the noncircular parent Euler/time-radial difference bridge rather than direct phase-volume closure.",
        },
        {
            "source_id": "SRC1863_16_1860_q_loc_bridge",
            "source_kind": "q_loc_EH_bridge",
            "source_path": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            "required_needle": "epsilon_GK_q_loc",
            "use_in_1863": "keeps Gamma/Khat/q_loc as an explicit nonclaim residual blocking local EH inheritance.",
        },
        {
            "source_id": "SRC1863_17_1861_evenness",
            "source_kind": "coupling_lock_gate",
            "source_path": ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "required_needle": "EVENNESS_THEOREM_NOT_ACTIVATED",
            "use_in_1863": "imports the exact but physically unactivated evenness/source-functional theorem.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in sources:
        path = source["source_path"]
        needle = source["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_kind": source["source_kind"],
                "source_path": str(path),
                "path_exists": as_bool_text(path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(path, needle)),
                "use_in_1863": source["use_in_1863"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def parent_current_contract() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_0_parent_action",
            "object": "single parent action",
            "exact_contract": "S_parent[Phi,Psi,Lambda] fixes L_parent, matter/readout slots, constraints, boundary terms, constants and projection maps before any local limit is taken.",
            "current_evidence": "1855 writes a coherent minimal closure clause; 1856 rejects physical Xhat as fundamental in the current branch.",
            "missing_signature": "MISSING_MTS_PRIMITIVE_PARENT_ACTION_WITH_FIELD_CONTENT_AND_ALLOWED_VERTICES",
            "status": "CONTRACT_SHAPE_READY_NOT_PARENT_SIGNED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_1_variation_current",
            "object": "Theta_total and Q_tau^MTS",
            "exact_contract": "delta L_parent = E_A delta Phi^A + d Theta_total and delta H_tau = integral_S(delta Q_tau^MTS - i_tau Theta_total) with fixed boundary/reference prescription.",
            "current_evidence": "1798/1862 identify Theta_total/Q_tau ownership as the current-owner bottleneck.",
            "missing_signature": "MISSING_PARENT_THETA_TOTAL_QTAU_CURRENT_OWNER",
            "status": "CURRENT_OWNER_UNSIGNED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_2_source_measure",
            "object": "observed source charge",
            "exact_contract": "Delta_Hsrc := G_ref^-1 integral_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress] must vanish or be component-bounded in one normalization.",
            "current_evidence": "1862 keeps Delta_Hsrc and its Pi_M/tau_obs/integrability chain as the live Y5 source-normalization debt.",
            "missing_signature": "MISSING_PIM_TAU_OBS_SOURCE_CHARGE_OWNER_AND_COMPONENT_VALUES",
            "status": "SOURCE_MEASURE_NOT_ZERO_NOT_BOUNDED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_3_vertical_generator",
            "object": "q and v_X",
            "exact_contract": "q: Phi_parent -> Q_vis exists before matter/readout, and the dangerous local direction satisfies Dq[v_X]=0 or is removed by constraint before physical phase space.",
            "current_evidence": "1802 and 1849 give exact chain-rule theorems if q/Dq/v_X are parent signed; 1857 gives the auxiliary/constraint conditional theorem.",
            "missing_signature": "MISSING_PARENT_Q_MAP_DQ_KERNEL_OR_CONSTRAINT_DEGREE_COUNT",
            "status": "VERTICALITY_CONDITIONAL_NOT_PARENT_SIGNED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_4_matter_descent",
            "object": "ordinary matter action",
            "exact_contract": "S_matter = Sbar[Psi, e_obs(q(Phi)), omega_obs(q(Phi)), theta(q(Phi) or superselected)] with no direct X/source/marker vertices.",
            "current_evidence": "1802/1849 prove the chain-rule zero conditionally; 1803/1804 retain hidden frames, source-prefactors, alpha, mass, clock and marker channels.",
            "missing_signature": "MISSING_MATTER_FUNCTOR_NO_SHADOW_NO_MARKER_CONSTANT_SUPERSELECTION",
            "status": "MATTER_DESCENT_UNSIGNED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_5_boundary_history",
            "object": "boundary and history silence",
            "exact_contract": "Boundary, source-worldtube, domain, support, reference and memory/history terms are exact, zero-flux, compact-local, or source-bounded in the same projected units.",
            "current_evidence": "1801 keeps J_boundary and J_history open; 1849 keeps non-Hilbert/domain/support qbar tails open.",
            "missing_signature": "MISSING_BOUNDARY_EDGE_HISTORY_NONHILBERT_SOURCE_ZERO_OR_BOUNDS",
            "status": "BOUNDARY_HISTORY_TAILS_RETAINED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_6_Gamma_Khat",
            "object": "q_loc variational pair",
            "exact_contract": "Gamma_eff and K_hat are one metric-response pair, q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) is a Ward/Euler residual, and its double-zero is physically locked.",
            "current_evidence": "1860 proves a formal normal form exists but live MTS has not activated Gamma/Khat source-signature, metric-response, boundary, projector or observable lock.",
            "missing_signature": "MISSING_LIVE_GAMMA_KHAT_ACTION_METRIC_RESPONSE_AND_OBSERVABLE_LOCK",
            "status": "QLOC_ZERO_NOT_DERIVED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_7_parent_Euler_bridge",
            "object": "local GR/Newton reduced branch",
            "exact_contract": "An MTS-owned time/radial parent Euler difference D_R[MTS]=E_time-E_radial=partial_r C_R-S_R=0 must give S_R=0 and Q_R=0 without importing GR equations.",
            "current_evidence": "1859 rejects direct phase-volume derivation and selects the parent Euler bridge as the best noncircular route.",
            "missing_signature": "MISSING_MTS_OWNED_E_TIME_E_RADIAL_SOURCE_AND_NO_CHARGE_CERTIFICATES",
            "status": "BEST_ROUTE_SELECTED_NOT_DERIVED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCC1863_8_synthesis_verdict",
            "object": "single parent current chain",
            "exact_contract": "PCC1863_0 through PCC1863_7 close together from one parent action with one normalization and one no-cancellation residual policy.",
            "current_evidence": "The contract is precise enough to audit, but multiple required parent signatures are unsigned and several residual components lack values.",
            "missing_signature": "MISSING_SINGLE_PARENT_CURRENT_CERTIFICATE",
            "status": "SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED",
            "closes_chain": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def single_parent_chain_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_0_one_action",
            "clause": "one parent action owns all sectors before readout",
            "required_for_closure": "L_parent declares field content, quotient, constants, matter, EM, boundary, history, source and readout slots.",
            "current_status": "ACTION_GRAMMAR_INCOMPLETE",
            "failure_mode": "sublemmas can be true in different closures without one common parent certificate.",
            "closure_cost": "derive or explicitly assume the full parent action grammar.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_1_variational_current",
            "clause": "Theta_total/Q_tau current owner",
            "required_for_closure": "Noether/symplectic current and charge are extracted from the same L_parent and boundary domain.",
            "current_status": "PARENT_CURRENT_OWNER_UNSIGNED",
            "failure_mode": "source charge can be normalization-dependent or readout-defined.",
            "closure_cost": "derive Q_tau^MTS and H_ref/Pi_M/tau_obs from the parent variation.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_2_verticality",
            "clause": "v_X is quotient-vertical or eliminated",
            "required_for_closure": "Dq[v_X]=0, or a first/second-class constraint removes X before physical matter/readout.",
            "current_status": "CONDITIONAL_ONLY",
            "failure_mode": "ordinary matter can still see an X-dependent frame/source/constant channel.",
            "closure_cost": "derive q/Dq kernel or constraint degree count from MTS primitives.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_3_matter_and_constants",
            "clause": "matter constants and markers descend",
            "required_for_closure": "Observed coframe, matter functor, alpha_EM, mass ratios, nuclear/clock constants and material markers are quotient-owned or superselected.",
            "current_status": "HIDDEN_COUPLINGS_RETAINED",
            "failure_mode": "field theory can be WEP-quiet but still carry a common local source-normalization or clock/R10 residual.",
            "closure_cost": "parent no-extra-F2/no-mass-vertex/no-marker theorem, or finite coefficient rows.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_4_readout_order",
            "clause": "readout cannot re-enter source",
            "required_for_closure": "All arena maps are strict post-solution maps absent from S_parent, S_eff, pre-action weights and source normalizers.",
            "current_status": "PURE_READOUT_SAFE_NOT_GENERAL",
            "failure_mode": "calibration, projector, source-worldtube or effective-action feedback can feed J_X.",
            "closure_cost": "arena-by-arena typed readout theorem or finite reentry coefficients.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_5_boundary_history",
            "clause": "boundary, non-Hilbert and history tails are silent",
            "required_for_closure": "edge charges, reference subtraction, support shifts, domain terms and memory kernels are zero or bounded absolutely.",
            "current_status": "TAILS_RETAINED",
            "failure_mode": "local exterior branch inherits hidden source terms even if visible matter pullback is silent.",
            "closure_cost": "zero-flux/exact primitive theorem or source-backed component bounds.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_6_q_loc_EH_bridge",
            "clause": "Gamma/Khat/q_loc activates EH fixed point",
            "required_for_closure": "Gamma_eff and K_hat are a single variational response pair and q_loc is physically locked to the dangerous local residual.",
            "current_status": "FORMAL_NORMAL_FORM_NOT_LIVE_PARENT_SIGNED",
            "failure_mode": "formal double-zero could apply to a shadow variable instead of local PPN/source-normalization residuals.",
            "closure_cost": "live Gamma/Khat action-existence plus observable lock and boundary/projector silence.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPC1863_7_verdict",
            "clause": "all clauses close in one branch",
            "required_for_closure": "A single signed parent chain owns current, matter, constants, readout, boundary, q_loc and local Euler reduction.",
            "current_status": "FAIL_CURRENT_CLAIM",
            "failure_mode": "local GR/Newton would be closure-smuggled if promoted now.",
            "closure_cost": "demote I_X/J_X to finite residuals and prioritize one parent-action proof queue.",
            "claim_gate": "BLOCKED",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def ix_jx_demotion_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_0_I_X",
            "symbol": "I_X",
            "meaning": "first non-EH curl/source component in delta_H_tau/current integrability.",
            "formula_or_bound": "I_X retained inside delta_H_tau/M_H_ref = (|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref.",
            "current_status": "NOT_THEOREM_ZERO",
            "missing_for_zero": "MISSING_PARENT_CURRENT_OWNER;MISSING_X_SOURCE_SILENCE;MISSING_PROJECTOR_BOUNDARY_DQ_LOCK",
            "nonclaim_residual_action": "retain I_X as a finite source-normalization residual until bounded.",
            "observable_links": "orbital;PPN;local_GR;source_normalization",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_1_J_X",
            "symbol": "J_X",
            "meaning": "ordinary and hidden source current for the dangerous X/local residual direction.",
            "formula_or_bound": "|J_X| <= |J_matter|+|J_chiD_wall|+|J_boundary|+|J_readout|+|J_history|+|Pi_M_projection_tail|.",
            "current_status": "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "missing_for_zero": "MISSING_CHANNEL_ZERO_OR_COMPONENT_BOUNDS",
            "nonclaim_residual_action": "keep no-cancellation absolute envelope; no opposite-sign cancellation credit.",
            "observable_links": "R10;WEP;clock;PPN;orbital",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_2_J_matter",
            "symbol": "J_matter or qbar_XT",
            "meaning": "test/source matter pullback into the X direction.",
            "formula_or_bound": "|J_matter| <= M_T |qbar_XT|; |qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|.",
            "current_status": "CONDITIONAL_CHAIN_RULE_NOT_PARENT_SIGNED",
            "missing_for_zero": "MISSING_Q_KERNEL;MISSING_OBS_E_DESCENT;MISSING_MATTER_FUNCTOR;MISSING_NO_MARKER_CONSTANTS;MISSING_HIDDEN_SOURCE_ZERO",
            "nonclaim_residual_action": "retain qbar_XT component envelope with all values missing.",
            "observable_links": "R10;WEP;clock;fine_structure;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_3_J_readout",
            "symbol": "J_readout or C_R[A]",
            "meaning": "readout/effective source reentry after variation.",
            "formula_or_bound": "|J_readout| <= ||delta R_readout/delta X|| + |shadow_frame_tail| + |calibration_source_mask|.",
            "current_status": "PURE_POSTPROCESSING_SAFE_NOT_GENERAL",
            "missing_for_zero": "MISSING_ARENA_DOMAIN_TYPING;MISSING_PREACTION_WEIGHT_EXCLUSION;MISSING_PROJECTOR_CHAIN_MAP;MISSING_CALIBRATION_FEEDBACK_ZERO",
            "nonclaim_residual_action": "retain arena-specific readout coefficients until typed as pure postprocessing.",
            "observable_links": "Pantheon;BAO;SPARC;R10;WEP;clock;PPN",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_4_constants",
            "symbol": "b_alpha, b_mu, b_mA, b_nuc, b_clock_i",
            "meaning": "dimensionless constant, mass-ratio, nuclear and clock leakage into matter/source/readout.",
            "formula_or_bound": "b_alpha=Lie_v ln(alpha_EM); b_mA=Lie_v ln(m_A/m_ref); b_clock_i=K_alpha_i b_alpha+K_mu_i b_mu+K_nuc_i b_nuc+...",
            "current_status": "ALPHA_MASS_CLOCK_CHANNELS_RETAINED",
            "missing_for_zero": "MISSING_TQ_OWNER;MISSING_UNIQUE_F2;MISSING_NO_ALPHA_VERTEX;MISSING_MATTER_SPECTRUM_OWNER;MISSING_CLOCK_READOUT_DESCENT",
            "nonclaim_residual_action": "retain constant-sector coefficient provenance rows.",
            "observable_links": "fine_structure;WEP;clock;R10",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_5_boundary_history",
            "symbol": "J_boundary, J_history, qbar_nonH",
            "meaning": "edge charge, support, domain, reference, non-Hilbert and memory/history source tails.",
            "formula_or_bound": "|J_boundary|+|J_history|+|qbar_nonH| retained under absolute no-cancellation bounds.",
            "current_status": "TAILS_NOT_ZERO_NOT_BOUNDED",
            "missing_for_zero": "MISSING_BOUNDARY_FLUX_ZERO;MISSING_EDGE_CHARGE_ZERO;MISSING_REFERENCE_OWNER;MISSING_HISTORY_KERNEL_THEOREM;MISSING_NONHILBERT_BOUND",
            "nonclaim_residual_action": "keep as separate finite residual requirements, not hidden inside matter zero.",
            "observable_links": "orbital;source_normalization;R10;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_6_epsilon_GK_q_loc",
            "symbol": "epsilon_GK_q_loc",
            "meaning": "Gamma/Khat/q_loc residual blocking local EH/GR inheritance.",
            "formula_or_bound": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}); epsilon_GK_q_loc retained until live action/metric-response/observable lock closes.",
            "current_status": "QLOC_ZERO_NOT_DERIVED",
            "missing_for_zero": "MISSING_GAMMA_EFF_SOURCE_SIGNATURE;MISSING_KHAT_METRIC_RESPONSE;MISSING_HELMHOLTZ_LIVE_INPUTS;MISSING_OBSERVABLE_LOCK",
            "nonclaim_residual_action": "retain explicit nonclaim local-EH bridge residual.",
            "observable_links": "PPN;local_GR;Newton;clock;orbital",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "IJX1863_7_total_vector",
            "symbol": "R_local^MTS",
            "meaning": "minimal local residual vector after demotion.",
            "formula_or_bound": "R_local^MTS := (Delta_Hsrc, I_X, J_X, qbar_XT, b_alpha/b_mA/b_clock, boundary/history tails, epsilon_GK_q_loc, q_R/S_R).",
            "current_status": "FINITE_NONCLAIM_VECTOR_REQUIRED",
            "missing_for_zero": "MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS;MISSING_NUMERIC_COMPONENT_BOUNDS;MISSING_PARENT_ZERO_THEOREMS",
            "nonclaim_residual_action": "use this as the private proof/test queue; do not treat as local-GR pass.",
            "observable_links": "R10;WEP;PPN;clock;orbital;local_GR",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def finite_residual_requirements() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FRR1863_0_common_units",
            "requirement": "shared projected units",
            "needed_rows": "Delta_Hsrc;I_X;J_X;qbar_XT;epsilon_GK_q_loc;q_R/S_R",
            "current_status": "MISSING_COMMON_UNITS",
            "why_it_matters": "without common units, no residual vector can be compared to PPN/R10/clock/orbital limits.",
            "next_action": "declare dimensionless normalization or source-charge units for each component.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FRR1863_1_arena_projections",
            "requirement": "projection operators into test arenas",
            "needed_rows": "tau_R10;tau_PPN;tau_clock;tau_orbital;tau_WEP",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "why_it_matters": "a residual can be harmless in one arena and lethal in another.",
            "next_action": "map each residual into R10, WEP, PPN, clocks and orbital observables.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FRR1863_2_zero_or_bound_source",
            "requirement": "zero theorem or source-backed numeric bound for every component",
            "needed_rows": "all IJX1863 residual components",
            "current_status": "MISSING_ZERO_OR_NUMERIC_BOUNDS",
            "why_it_matters": "claiming local GR requires every live component to vanish or sit below a sourced bound.",
            "next_action": "attempt parent-action proof first; otherwise acquire finite coefficient rows.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FRR1863_3_no_cancellation",
            "requirement": "absolute no-cancellation policy",
            "needed_rows": "J_X;qbar_XT;constant-sector;boundary/history;epsilon_GK_q_loc",
            "current_status": "POLICY_ACTIVE",
            "why_it_matters": "opposite-sign hidden couplings do not count as a derivation.",
            "next_action": "sum absolute envelopes unless a theorem identifies one common vanishing current.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FRR1863_4_parent_Euler_bridge",
            "requirement": "derive local reciprocal/GR branch from parent Euler difference",
            "needed_rows": "E_time;E_radial;D_R[MTS];S_R;Q_R;boundary/no-charge certificates",
            "current_status": "BEST_ROUTE_SELECTED_NOT_DERIVED",
            "why_it_matters": "this is the least circular route to GR-like local reduction without importing GR equations.",
            "next_action": "build the 1864 proof queue around this bridge and the residual vector.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def local_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1863_0_positive",
            "finding": "The target theorem is now sharply stated.",
            "impact": "Local GR/Newton can be pursued as a reduced parent branch rather than as a guessed plateau.",
            "status": "PROGRESS_NOT_CLAIM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1863_1_blocker",
            "finding": "The single parent-current certificate is absent.",
            "impact": "No local EH/GR/Newton inheritance can be claimed from the present corpus.",
            "status": "BLOCKS_LOCAL_GR_CLAIM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1863_2_best_route",
            "finding": "The physical-scalar route is worse than the auxiliary/constraint/Euler bridge route.",
            "impact": "The next derivation should try to eliminate the dangerous residual before matter readout, then show the parent Euler difference gives the GR reciprocal condition.",
            "status": "ROUTE_SELECTED",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1863_3_backstop",
            "finding": "If the parent theorem fails, the finite residual vector is testable.",
            "impact": "The branch does not collapse into handwaving; it becomes a sourced local-residual comparison problem.",
            "status": "BACKSTOP_NONCLAIM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1863_0_single_parent_chain",
            "claim": "one parent current chain closes the local source-normalized branch",
            "status": "BLOCKED",
            "reason": "PCC1863_8 is SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1863_1_I_X_J_X_zero",
            "claim": "I_X and J_X vanish on the local branch",
            "status": "BLOCKED",
            "reason": "I_X/J_X are demoted to finite nonclaim residuals with missing source-zero proofs and missing numeric bounds.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1863_2_local_GR_Newton",
            "claim": "MTS locally reduces to GR/Newton in the current branch",
            "status": "BLOCKED",
            "reason": "Delta_Hsrc, matter/constants/readout leakage, boundary/history tails, Gamma/Khat/q_loc and parent Euler bridge remain unsigned.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1863_3_R10_WEP_PPN_clock_orbital",
            "claim": "local bound arenas pass from this derivation",
            "status": "BLOCKED",
            "reason": "finite residual vector lacks common units, arena projections and source-backed numeric values.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1863_4_public_theory_claim",
            "claim": "1863 is public evidence for a local-GR reduction",
            "status": "BLOCKED_PRIVATE_ONLY",
            "reason": "1863 is a private derivation discipline checkpoint, not a result claim.",
            "gate_pass": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1863_0_contract_written",
            "decision": "SINGLE_PARENT_CURRENT_CHAIN_CONTRACT_IS_PRECISE",
            "reason": "the required objects and equations can be named without ambiguity: L_parent, Theta_total, Q_tau, q/Dq, matter descent, boundary/history, q_loc and parent Euler bridge.",
            "next_action": "use the contract as the proof checklist.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1863_1_not_promoted",
            "decision": "SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED",
            "reason": "the live corpus has exact conditional subtheorems but no one parent action signs all clauses together.",
            "next_action": "do not claim local GR/Newton or I_X/J_X zero.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1863_2_demotion",
            "decision": "IX_JX_DEMOTED_TO_FINITE_NONCLAIM_RESIDUAL_VECTOR",
            "reason": "demotion preserves testability and prevents closure-smuggling while derivations are still attempted.",
            "next_action": "track R_local^MTS as a source-backed residual vector.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1863_3_best_route",
            "decision": "PARENT_EULER_BRIDGE_PLUS_RESIDUAL_VECTOR_PRIORITIZED",
            "reason": "1859 already rejected direct phase-volume derivation and selected the noncircular E_time-E_radial bridge; 1863 adds the coupling/source residual vector needed to make that bridge honest.",
            "next_action": "build 1864 local-GR reduction contract/prioritizer.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1863_0_primary",
            "next_target": "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
            "script": "scripts/Y5_R2FR_local_GR_reduction_contract_and_residual_vector_prioritizer_1864.py",
            "objective": "convert the 1863 single-parent contract and R_local^MTS residual vector into a minimal local-GR reduction theorem checklist, then prioritize the first derivation target: parent Euler bridge, matter/constants/source-current exclusion, Gamma/Khat action pair, or boundary/source-measure closure.",
            "selection_status": "selected",
            "success_condition": "either a signed parent clause closes a residual channel, or the residual channel is converted into a source-ready finite nonclaim row with units and arena projections.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1863_1_parallel",
            "next_target": "1864b-Y5-R2FR-no-extra-F2-no-mass-source-vertex-signature.md",
            "script": "scripts/Y5_R2FR_no_extra_F2_no_mass_source_vertex_signature_1864b.py",
            "objective": "attack the highest-risk hidden coupling subproblem directly by trying to forbid independent EM kinetic, mass, binding and source-only vertices from the parent action.",
            "selection_status": "held_parallel",
            "success_condition": "no-extra-F2/no-mass/no-source-weight theorem-zero or finite b_alpha/b_mA/b_nuc/delta_kappa rows.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    truthy = {"true", "pass", "passed", "yes", "1"}
    guarded_fields = {"valid_for_claim", "claim_allowed", "gate_pass", "closes_chain"}
    for rows in rows_by_name.values():
        for row in rows:
            for field, value in row.items():
                if field in guarded_fields and str(value).strip().lower() in truthy:
                    return False
    return True


def missing_rows_not_claim_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            valid = str(row.get("valid_for_claim", "")).strip().lower() == "true"
            claim = str(row.get("claim_allowed", "")).strip().lower() == "true"
            if "MISSING_" in text and (valid or claim):
                return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        folder.mkdir(parents=True, exist_ok=True)
    for path in paths:
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1863_{path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1863_{path.name}",
        ]
        if not all(target.exists() for target in expected):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1863*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    contracts = rows_by_name["parent_current_contract"]
    demotion = rows_by_name["ix_jx_demotion"]
    claims = rows_by_name["claim_gate"]
    decisions = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1863_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in sources) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1863_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in sources) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1863_2_contract_not_promoted",
            "status": "PASS" if any(row["status"] == "SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED" for row in contracts) else "FAIL",
            "detail": "single parent current chain remains unsigned",
        },
        {
            "validation_id": "VAL1863_3_all_contract_closure_flags_false",
            "status": "PASS" if all(row["closes_chain"] == "False" for row in contracts) else "FAIL",
            "detail": "no parent-current clause is promoted as closing the chain",
        },
        {
            "validation_id": "VAL1863_4_ix_jx_demoted",
            "status": "PASS" if any(row["current_status"] == "FINITE_NONCLAIM_VECTOR_REQUIRED" for row in demotion) else "FAIL",
            "detail": "I_X/J_X route is demoted to finite nonclaim residual vector",
        },
        {
            "validation_id": "VAL1863_5_residual_requirements_present",
            "status": "PASS" if len(rows_by_name["finite_residual_requirements"]) >= 4 else "FAIL",
            "detail": "finite residual requirements include units, arena projections, zero/bound rows and no-cancellation policy",
        },
        {
            "validation_id": "VAL1863_6_claim_gates_blocked",
            "status": "PASS" if all(row["status"].startswith("BLOCKED") for row in claims) else "FAIL",
            "detail": "all local/R10/WEP/PPN/clock/orbital claim gates remain blocked",
        },
        {
            "validation_id": "VAL1863_7_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated theorem, score, closure or claim flag is true",
        },
        {
            "validation_id": "VAL1863_8_missing_not_ready",
            "status": "PASS" if missing_rows_not_claim_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1863_9_decision_next",
            "status": "PASS" if any(row["decision"] == "PARENT_EULER_BRIDGE_PLUS_RESIDUAL_VECTOR_PRIORITIZED" for row in decisions) else "FAIL",
            "detail": "decision selects parent Euler bridge plus residual vector prioritization",
        },
        {
            "validation_id": "VAL1863_10_next_selected",
            "status": "PASS" if any(row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1863_11_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1863_12_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist for generated non-validation CSVs",
        },
        {
            "validation_id": "VAL1863_13_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1863_14_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1863 outputs found under formalization-workbench",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1863_OVERALL",
            "status": overall,
            "detail": "1863 single parent current chain synthesis or I_X/J_X demotion checkpoint",
        }
    )
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "valid_for_claim": as_bool_text(False),
        }
        for row in checks
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1863 - Y5/R2FR Single Parent Current Chain Synthesis Or I_X/J_X Demotion",
        "",
        "## Verdict",
        "",
        "1863 writes the exact contract a future parent action must satisfy for the local branch to inherit GR/Newton without smuggling in a plateau axiom. The good news is that the route is now mathematically sharp: one parent action must own `L_parent`, `Theta_total`, `Q_tau^MTS`, `q/Dq`, matter descent, constants, readout order, boundary/history silence, `Gamma_eff/K_hat/q_loc`, and the parent Euler bridge.",
        "",
        "The bad news-but-useful bad news is that the live corpus does not yet sign those clauses in one branch. The conditional sublemmas are real, but not enough to claim `I_X=0`, `J_X=0`, or local GR/Newton. So 1863 demotes `I_X/J_X` into an explicit finite nonclaim residual vector rather than pretending the coupling problem is solved.",
        "",
        "**Claim ceiling:** no single-parent-current closure claim, no `I_X/J_X` source-zero claim, no R10/WEP/PPN/clock/orbital pass, no local-GR/Newton reduction claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1863.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1863", "valid_for_claim"],
        ),
        "",
        "## Parent Current Contract",
        "",
        markdown_table(
            rows_by_name["parent_current_contract"],
            ["contract_id", "object", "exact_contract", "current_evidence", "missing_signature", "status", "closes_chain", "valid_for_claim"],
        ),
        "",
        "## Single Parent Chain Audit",
        "",
        markdown_table(
            rows_by_name["single_chain_audit"],
            ["audit_id", "clause", "required_for_closure", "current_status", "failure_mode", "closure_cost", "claim_gate", "valid_for_claim"],
        ),
        "",
        "## I_X/J_X Demotion Ledger",
        "",
        markdown_table(
            rows_by_name["ix_jx_demotion"],
            ["residual_id", "symbol", "meaning", "formula_or_bound", "current_status", "missing_for_zero", "nonclaim_residual_action", "observable_links", "valid_for_claim"],
        ),
        "",
        "## Finite Residual Requirements",
        "",
        markdown_table(
            rows_by_name["finite_residual_requirements"],
            ["requirement_id", "requirement", "needed_rows", "current_status", "why_it_matters", "next_action", "valid_for_claim"],
        ),
        "",
        "## Local GR Impact",
        "",
        markdown_table(
            rows_by_name["local_gr_impact"],
            ["impact_id", "finding", "impact", "status", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Claim Gates",
        "",
        markdown_table(
            rows_by_name["claim_gate"],
            ["claim_id", "claim", "status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Decision Ledger",
        "",
        markdown_table(
            rows_by_name["decision_ledger"],
            ["decision_id", "decision", "reason", "next_action", "valid_for_claim"],
        ),
        "",
        "## Next Target",
        "",
        markdown_table(
            rows_by_name["next_target"],
            ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "status", "detail", "valid_for_claim"],
        ),
        "",
        "## Interpretation",
        "",
        "This is a proper tightening, not a collapse. The work has reached the stage where the coupling problem cannot hide behind a word like 'matter' or 'source'. Either the parent action kills each channel by construction, or the channel becomes a finite residual with units and arena projections. The best next punch is the 1864 prioritizer: make the local-GR theorem contract minimal, then attack the highest-leverage clause first instead of wandering through the whole jungle at once.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "parent_current_contract": parent_current_contract(),
        "single_chain_audit": single_parent_chain_audit(),
        "ix_jx_demotion": ix_jx_demotion_ledger(),
        "finite_residual_requirements": finite_residual_requirements(),
        "local_gr_impact": local_gr_impact(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }

    non_validation_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, rows_by_name[key])

    copy_branch_outputs(non_validation_paths)
    remove_pycache()

    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()

    if any(row["status"] == "FAIL" for row in rows_by_name["validation"]):
        raise SystemExit("1863 validation failed")

    print(f"Wrote {DOC_PATH}")
    for path in OUTPUTS.values():
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
