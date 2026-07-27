from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NO_SHADOW_ACTION_DOMAIN_2572"
CHECKPOINT_ID = "2572"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2572-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2572_SOURCE_REGISTER.csv",
    "action_domain": OUT / "P8_Y5_NO_SHADOW_2572_ACTION_DOMAIN_CONTRACT.csv",
    "zero_theorem": OUT / "P8_Y5_NO_SHADOW_2572_ZERO_THEOREM.csv",
    "coupling_shadow": OUT / "P8_Y5_NO_SHADOW_2572_COUPLING_SHADOW_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_NO_SHADOW_2572_COUNTERMODEL_LEDGER.csv",
    "response_kernel": OUT / "P8_Y5_NO_SHADOW_2572_RESPONSE_KERNEL_ACQUISITION.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2572_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2572_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2572_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2572_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2572_VALIDATION.csv",
}

COPY_TARGETS = {
    "action_domain": LOCAL_BOUNDS / "No_shadow_action_domain_contract_2572_NONCLAIM.csv",
    "zero_theorem": LOCAL_BOUNDS / "No_shadow_zero_theorem_2572_NONCLAIM.csv",
    "coupling_shadow": LOCAL_BOUNDS / "Coupling_shadow_audit_2572_NONCLAIM.csv",
    "response_kernel": LOCAL_BOUNDS / "Common_frame_coupling_response_kernel_acquisition_2572_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2572_FIRST_COMMON_FRAME_COUPLING_RESPONSE_KERNEL_OR_ACTION_GRAMMAR.csv",
}

SOURCES = [
    {
        "source_id": "SRC2572_00_2571_handoff",
        "source_path": ROOT / "2571-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": ["NEXT2571_0_selected", "DLEAK2571_5_coupling_readout", "VAL2571_OVERALL"],
        "role": "active handoff: no-shadow action-domain with coupling shadow included",
    },
    {
        "source_id": "SRC2572_01_2488_precedent",
        "source_path": ROOT / "2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": ["AD2488_4_verdict", "ZTH2488_0_exact_conditional", "VAL2488_OVERALL"],
        "role": "earlier no-shadow action-domain attempt without the upgraded coupling slot",
    },
    {
        "source_id": "SRC2572_02_1880_terminal",
        "source_path": ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
        "needles": ["TPC1880_0_terminal_object", "ZTH1880_0_exact_conditional", "VAL1880_OVERALL"],
        "role": "terminal public coframe/no-shadow conditional theorem",
    },
    {
        "source_id": "SRC2572_03_1879_coframe_owner",
        "source_path": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
        "needles": ["PCO1879_1_coframe_owner", "CFL1879_0_bR", "VAL1879_OVERALL"],
        "role": "parent coframe ownership and common-frame finite rows",
    },
    {
        "source_id": "SRC2572_04_1738_kernel",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["DOBS_E_KERNEL_ZERO_NOT_SIGNED", "SAME_COFRAME_IS_NOT_ENOUGH", "VAL1738_OVERALL"],
        "role": "same-frame countermodel and DObs_e blocker",
    },
    {
        "source_id": "SRC2572_05_1933_coeff_descent",
        "source_path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["QDT1933_1_vertical_zero", "TYPE1933_4_verdict", "VAL1933_OVERALL"],
        "role": "conditional coefficient descent theorem and unsigned coefficient owner",
    },
    {
        "source_id": "SRC2572_06_2568_source_norm",
        "source_path": ROOT / "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["ENORM2568_1_e_kappaG", "ENORM2568_2_e_ellJ_owner", "VAL2568_OVERALL"],
        "role": "kappa_MTS and ell_J source-normalization residuals",
    },
    {
        "source_id": "SRC2572_07_2569_EH_coupling",
        "source_path": ROOT / "2569-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
        "needles": ["KRES2569_4_e_ellJ_owner", "e_EH_import", "VAL2569_OVERALL"],
        "role": "EH origin/coupling owner split and no-EH-import guardrail",
    },
    {
        "source_id": "SRC2572_08_2571_validation",
        "source_path": OUT / "P8_Y5_BRR545_2571_VALIDATION.csv",
        "needles": ["VAL2571_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def action_domain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "AD2572_0_terminal_public_coframe",
            "clause": "ordinary local readouts factor through a terminal public coframe",
            "formal_statement": "Obs_A(Phi,Psi)=Obsbar_A(E(Q_vis(Phi)),Psi,theta_pub,c_pub) for rods, clocks, photons, Hilbert source, orbit readout and local tests",
            "status": "CANDIDATE_NOT_PARENT_DERIVED",
            "proof_attempt": "If the parent category contains a terminal ordinary-readout object E(Q_vis), representative fields cannot enter local metric observations.",
            "blocker": "the current parent normal form does not prove terminality or the visible quotient object Q_vis",
            "implication_if_signed": "DObs_e[v_hidden]=0 for all hidden directions in ker(Dq_parent)",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2572_1_no_metric_shadow_slot",
            "clause": "no Weyl/disformal shadow-frame argument",
            "formal_statement": "Allowed[S_matter,Obs] excludes A_R(C_R,J_q)^2 g_pub, B_R(C_R,J_q)u_mu u_nu and E(Q_vis,C_R,J_q)",
            "status": "CLOSURE_ONLY_NOT_DERIVED",
            "proof_attempt": "Covariance plus one public frame is insufficient because a universal hidden Weyl/disformal factor is still covariant.",
            "blocker": "no parent action-domain grammar bans C_R/J_q dependence inside the ordinary metric/coframe slot",
            "implication_if_signed": "b_R=d_R=0 structurally",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2572_2_no_source_prefactor_slot",
            "clause": "no source-only matter prefactor",
            "formal_statement": "Allowed[S_matter] excludes sum_A w_A(C_R,J_q)L_A(Psi_A,e_pub) and source-current weights not descending through Q_vis",
            "status": "NOT_DERIVED",
            "proof_attempt": "WEP and Ward conservation do not independently forbid universal or sector-balanced source weights.",
            "blocker": "ordinary matter descent and source-current owner are not parent-signed at the action-domain level",
            "implication_if_signed": "w_R=0 and part of E_norm/source shadow is silenced",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2572_3_no_coupling_shadow_slot",
            "clause": "visible couplings and source-current scales are parent-owned coefficients",
            "formal_statement": "kappa_MTS=kappa_bar(Q_vis or parent constant), ell_J=ell_bar(parent), c_vis=q_parent^*c_bar; no dependence on C_R,J_q,endpoint or fitted GM/H0",
            "status": "COUPLING_ACTION_DOMAIN_UNSIGNED",
            "proof_attempt": "Coefficient descent gives dc_vis[v]=0 exactly if c_vis descends from q_parent, but the premise is not parent-signed.",
            "blocker": "e_kappaG, e_ellJ_owner, a1_vs_ellJ and coefficient descent remain residual owners",
            "implication_if_signed": "epsilon_coupling_readout_abs=0 and no fitted-GM/H0 coupling absorption is needed",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2572_4_inheritance_stack",
            "clause": "connection, tau, constants, source support and boundary endpoints inherit the same public domain",
            "formal_statement": "omega=omega[e_pub], tau=tau(Q_vis), c_vis=cbar(Q_vis), support=sigma(Q_vis), P_loc dE/dQ_endpoint=0",
            "status": "INHERITANCE_STACK_UNSIGNED",
            "proof_attempt": "Metric/coframe descent alone can be reopened later by connection, clocks, constants, source support, projector or endpoint maps.",
            "blocker": "connection descent, tau pushforward, constants owner, boundary endpoint silence and projector order remain open branches",
            "implication_if_signed": "endpoint/projector/clock/coupling leaks cannot re-enter after coframe descent",
            "valid_for_claim": False,
        },
        {
            "clause_id": "AD2572_5_verdict",
            "clause": "parent action-domain exclusion closes no-shadow including coupling slots",
            "formal_statement": "AD2572_0 through AD2572_4 are all parent-signed in one ordinary-sector action grammar",
            "status": "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS",
            "proof_attempt": "Attempted derivation reaches an exact contract, but the present parent normal form is still a skeleton rather than an admissible-object theorem.",
            "blocker": "terminality, no-extra-frame grammar, no-source-prefactor, coupling ownership and inheritance stack are unsigned",
            "implication_if_signed": "b_R=d_R=w_R=epsilon_endpoint_R=epsilon_coupling_readout_abs=0",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "ZTH2572_0_exact_conditional_no_shadow",
            "theorem_statement": "If ordinary readout has terminal e_pub=E(Q_vis), no C_R/J_q metric/source/endpoint slot, q-basic visible coefficients and inherited connection/tau/source/boundary maps, then hidden representative directions have zero local readout.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_failure": "Functional derivatives with respect to excluded hidden arguments vanish; inherited maps have no independent hidden argument to reintroduce them.",
            "required_clauses": "AD2572_0;AD2572_1;AD2572_2;AD2572_3;AD2572_4",
            "consequence": "DObs_e[v]=0, Domega[v]=0, dc_vis[v]=0, and source/readout endpoint shadows vanish",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2572_1_coefficient_descent",
            "theorem_statement": "If c_vis=q_parent^*cbar and v in ker(Dq_parent), then dc_vis(v)=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_failure": "dc_vis(v)=d(cbar o q_parent)(v)=dcbar(Dq_parent[v])=0.",
            "required_clauses": "parent-signed coefficient map for kappa_MTS, ell_J and every ordinary visible constant",
            "consequence": "epsilon_coupling_readout_abs is theorem-zero only after coefficient/source-scale ownership is signed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2572_2_shortcuts_rejected",
            "theorem_statement": "Same-frame language, WEP, Ward conservation, q_shape forgetting and fitted GM/H0 cannot prove no-shadow or coupling silence.",
            "status": "SHORTCUTS_REJECTED",
            "proof_or_failure": "Countermodels remain covariant and universal while moving metric, clock, source normalization or coupling readout.",
            "required_clauses": "parent action-domain exclusion or source-backed response kernels",
            "consequence": "no local-GR/Newton claim can be made from slogans or fitted baselines",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2572_3_current_verdict",
            "theorem_statement": "Current MTS derives terminal public coframe no-shadow including coupling slots.",
            "status": "NO_SHADOW_COUPLING_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "proof_or_failure": "The exact theorem exists only after unsigned action-domain and coefficient-owner premises are promoted.",
            "required_clauses": "all AD2572 clauses plus parent EH/coupling origin",
            "consequence": "finite leak rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZTH2572_4_fallback",
            "theorem_statement": "Unsigned no-shadow and coupling rows must become response-kernel inputs, not claims.",
            "status": "RESPONSE_KERNEL_REQUIRED_NONCLAIM",
            "proof_or_failure": "Finite b_R,d_R,w_R,endpoint,kappa,ell_J coefficients need arena-specific kernels, accepted bounds, units, source paths and no-cancellation envelopes.",
            "required_clauses": "PPN/clock/WEP/orbital kernels or parent action grammar",
            "consequence": "first fallback is a common-frame plus coupling PPN response kernel",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coupling_shadow_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coupling_id": "CS2572_0_kappa_MTS",
            "object": "kappa_MTS / G_parent / a1",
            "shadow_risk": "local gravitational strength can be shifted by hidden representative or fitted measurement normalization",
            "current_owner": "e_kappaG",
            "zero_condition": "parent EH-leading coefficient derives kappa_MTS before G_ref, GM, H0 or local tests are read",
            "current_status": "OWNER_UNSIGNED",
            "finite_fallback": "K_PPN_kappa * |D ln kappa_MTS| plus source-normalization response",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "CS2572_1_ell_J",
            "object": "ell_J source-current scale",
            "shadow_risk": "Hilbert source current amplitude can be rescaled while stationary mass readout appears clean",
            "current_owner": "e_ellJ_owner",
            "zero_condition": "ell_J fixed by parent scale, parent gap or tau-normalization theorem before fitted GM/H0",
            "current_status": "OWNER_UNSIGNED",
            "finite_fallback": "K_source_ellJ * |D ln ell_J| into PPN/orbital/source normalization",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "CS2572_2_visible_constants",
            "object": "c_vis including alpha_EM, clock constants, masses and binding coefficients",
            "shadow_risk": "local rods/clocks/constants can move even if the metric coframe is common",
            "current_owner": "e_coeff_descent;R_alpha;R_clock;R_mass;R_binding",
            "zero_condition": "all visible constants descend as q_parent^*cbar with no material marker or hidden slot",
            "current_status": "COEFFICIENT_DESCENT_UNSIGNED",
            "finite_fallback": "clock/WEP/material response kernels with no-cancellation envelope",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "CS2572_3_Hilbert_source_mass",
            "object": "M_H / source support / projector map",
            "shadow_risk": "source normalization can be hidden in worldtube support, projector order or boundary endpoint terms",
            "current_owner": "E_norm;c_projector_operator;e_jump_support;e_hilbert_shadow",
            "zero_condition": "Hilbert source, support and projector descend from the same terminal public domain",
            "current_status": "SOURCE_STACK_UNSIGNED",
            "finite_fallback": "source-normalization and orbital response kernel",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "CS2572_4_no_absorption_guard",
            "object": "G_ref / orbital GM / H0 calibration",
            "shadow_risk": "fitted baselines can absorb coupling leaks and fake a local-GR pass",
            "current_owner": "readout-order guardrail",
            "zero_condition": "couplings are fixed before empirical baselines and not inferred from the same data used for local tests",
            "current_status": "GUARDRAIL_ACTIVE_NONCLAIM",
            "finite_fallback": "report residuals against explicitly fixed baseline conventions",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2572_0_common_weyl",
            "ansatz": "e_obs = exp(b_R C_R) e_pub",
            "why_it_survives": "one universal coframe can still depend on a hidden representative and shift local metric/clock/PPN readout",
            "kills_shortcut": "same-frame;WEP;covariance",
            "required_fix": "derive b_R=0 by action-domain exclusion or source PPN/clock/orbital response bounds",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2572_1_common_disformal",
            "ansatz": "g_obs = A(C_R)^2 g_pub + D(C_R) u_mu u_nu",
            "why_it_survives": "a universal preferred-frame/disformal dependence can be covariant once the current field is in the domain",
            "kills_shortcut": "covariance;single-public-metric",
            "required_fix": "derive no current/disformal slot or source preferred-frame PPN kernel",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2572_2_source_prefactor",
            "ansatz": "S_matter includes sum_A w_A(C_R,J_q)L_A(Psi_A,e_pub)",
            "why_it_survives": "source normalization can move while the metric coframe looks universal",
            "kills_shortcut": "WEP;Ward;metric-only readout",
            "required_fix": "derive no source-only slot or source WEP/clock/R10 source-leg bounds",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2572_3_coupling_rescale",
            "ansatz": "kappa_obs=exp(s_k C_R)kappa_pub and ell_J_obs=exp(s_J C_R)ell_J_pub",
            "why_it_survives": "visible coupling and source-current scale can shift while the public coframe remains shared",
            "kills_shortcut": "same-frame;stationary-source-cancellation;fitted-GM",
            "required_fix": "derive parent coefficient/source-scale ownership or source coupling response kernels",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2572_4_endpoint_boundary",
            "ansatz": "e_obs=E(Q_vis,Q_endpoint) with P_loc partial_Q_endpoint E nonzero",
            "why_it_survives": "boundary or endpoint data can leak locally after the bulk coframe is declared public",
            "kills_shortcut": "bulk coframe descent",
            "required_fix": "derive boundary endpoint silence or source orbital/light-time endpoint kernel",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2572_5_qshape_forgetting",
            "ansatz": "Dq_shape[v_R]=0 while DObs_e[v_R] or dc_vis[v_R] is nonzero",
            "why_it_survives": "forgetting a label in q_shape does not prove clocks, rods, photons, sources or couplings forget it",
            "kills_shortcut": "q_shape;cheap verticality",
            "required_fix": "derive observed readout functor basicity or retain finite DObs/coupling rows",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def response_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "KER2572_0_PPN_metric_coupling",
            "arena": "PPN_metric_gamma_beta_preferred_frame",
            "selected_priority": "SELECTED_FIRST_KERNEL_NONCLAIM",
            "candidate_relation": "|delta gamma|+|delta beta|+|alpha_i| <= K_b|b_R|+K_d|d_R|+K_end|epsilon_endpoint_R|+K_k|Dln kappa_MTS|+K_J|Dln ell_J|",
            "required_inputs": "b_R;d_R;epsilon_endpoint_R;Dln kappa_MTS;Dln ell_J;PPN response operator;GR baseline;accepted PPN bounds;source convention",
            "missing_inputs": "MISSING_RESPONSE_KERNEL;MISSING_NUMERIC_COEFFICIENTS;MISSING_ACCEPTED_BOUND_SET;MISSING_BASELINE",
            "reason_for_priority": "PPN is the sharpest local-GR-facing arena for common-frame plus coupling leaks",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2572_1_source_normalization",
            "arena": "local_source_normalization_Newton",
            "selected_priority": "SECONDARY_KERNEL_NONCLAIM",
            "candidate_relation": "|delta GM_eff/GM| <= K_source_k|Dln kappa_MTS|+K_source_J|Dln ell_J|+K_norm|E_norm|+K_proj|epsilon_projector_endpoint|",
            "required_inputs": "source convention;kappa owner;ell_J owner;Hilbert worldtube map;projector response;no fitted-GM absorption rule",
            "missing_inputs": "MISSING_SOURCE_RESPONSE_KERNEL;MISSING_OWNER_THEOREM;MISSING_BASELINE_CONVENTION",
            "reason_for_priority": "Newtonian reduction lives or dies on source normalization, not just coframe cleanliness",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2572_2_clock_WEP_constants",
            "arena": "clock_WEP_material",
            "selected_priority": "TERTIARY_KERNEL_NONCLAIM",
            "candidate_relation": "|delta clock|+|eta_WEP| <= K_clock_b|b_R|+K_WEP_w|w_R|+K_c|dc_vis|+material_terms",
            "required_inputs": "material sensitivities;tau_clock;tau_WEP;visible constants map;accepted clock/WEP bounds",
            "missing_inputs": "MISSING_MATERIAL_MAP;MISSING_TAU_PROJECTION;MISSING_CONSTANTS_RESPONSE_KERNEL",
            "reason_for_priority": "common-mode source shifts may evade differential WEP but still show in clocks/constants",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2572_3_orbital_light_time",
            "arena": "orbital_light_time",
            "selected_priority": "FOURTH_KERNEL_NONCLAIM",
            "candidate_relation": "|delta orbit|+|delta light_time| <= K_orb_b|b_R|+K_orb_d|d_R|+K_orb_end|epsilon_endpoint_R|+K_orb_G|Dln(kappa_MTS ell_J)|",
            "required_inputs": "orbital response kernel;ephemeris baseline;endpoint projection;fixed-GM convention",
            "missing_inputs": "MISSING_ORBIT_KERNEL;MISSING_ENDPOINT_PROJECTION;MISSING_FIXED_GM_BASELINE",
            "reason_for_priority": "orbital/light-time tests catch endpoint and coupling leaks that can hide in simple metric rows",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2572_4_R10_guarded",
            "arena": "R10_short_range_guarded",
            "selected_priority": "HELD_LATER_WRONG_ROUTE_GUARD",
            "candidate_relation": "alpha_R10(lambda) receives a source-leg term only after finite-range Z_R/M_R^2/lambda_R and source/test charges exist",
            "required_inputs": "Z_R;M_R^2;lambda_R;source/test charges;R10 bound curve;tau_R10;coupling source leg",
            "missing_inputs": "MISSING_FINITE_RANGE_OPERATOR;MISSING_SOURCE_TEST_CHARGES;MISSING_BOUND_CURVE",
            "reason_for_priority": "common-frame/coupling source leakage cannot replace the finite-range R10 branch",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "KER2572_5_absolute_envelope",
            "arena": "all_local_arenas",
            "selected_priority": "NO_CANCELLATION_ENVELOPE_REQUIRED",
            "candidate_relation": "epsilon_local_abs=|b_R|+|d_R|+|w_R|+|epsilon_endpoint_R|+|Dln kappa_MTS|+|Dln ell_J|+|dc_vis|+source/projector leaks",
            "required_inputs": "all leak coefficients with units, source paths, response kernels, normalization frame and no-cancellation rule",
            "missing_inputs": "MISSING_NUMERIC_OR_THEOREM_ZERO_FOR_ALL_COMPONENTS",
            "reason_for_priority": "prevents accidental cancellation from being sold as local GR",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2572_0_internal",
            "claim": "2572 may be used as a private no-shadow/coupling audit and response-kernel routing file.",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "all public/local claims are blocked and finite rows are nonclaim",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2572_1_no_shadow_zero",
            "claim": "b_R=d_R=w_R=epsilon_endpoint_R=0.",
            "gate_status": "BLOCKED",
            "reason": "terminal public coframe, no-extra-frame grammar, no source-prefactor and inheritance stack are not parent-derived",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2572_2_coupling_zero",
            "claim": "epsilon_coupling_readout_abs=0 and kappa_MTS/ell_J/c_vis are parent-owned.",
            "gate_status": "BLOCKED",
            "reason": "coefficient descent is exact only conditionally; e_kappaG, e_ellJ_owner and a1_vs_ellJ remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2572_3_response_kernel_score",
            "claim": "finite common-frame/coupling rows pass PPN, clock/WEP, orbital or R10 bounds.",
            "gate_status": "BLOCKED",
            "reason": "response kernels, numeric coefficients, accepted bounds, units and baselines are missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2572_4_local_GR_Newton",
            "claim": "MTS reduces to local GR/Newton through no-shadow coframe and coupling ownership.",
            "gate_status": "BLOCKED",
            "reason": "no-shadow/coupling ownership is not derived and still needs EH origin, source normalization, beta and conservation closure",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2572_5_no_shortcuts",
            "claim": "A same-frame, WEP, Ward, q_shape, fitted-GM/H0 or EH-import shortcut is used as proof.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all shortcut routes are explicitly rejected or held as countermodels",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2572_0_result",
            "decision": "ACTION_DOMAIN_NO_SHADOW_WITH_COUPLING_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "The zero theorem is exact if terminality, no-extra-frame, source, coupling and inheritance clauses are signed, but the parent action grammar is still not signed.",
            "effect": "retain b_R,d_R,w_R,endpoint,kappa,ell_J,c_vis and total-envelope rows as nonclaim residuals",
        },
        {
            "decision_id": "DEC2572_1_upgrade",
            "decision": "COUPLING_SHADOW_IS_NOW_PART_OF_THE_NO_SHADOW_GATE",
            "reason": "A shared coframe can still fail local GR if kappa_MTS, ell_J or visible constants move through hidden readout slots.",
            "effect": "local GR/Newton cannot be claimed until coframe silence and coupling/source-scale ownership close together",
        },
        {
            "decision_id": "DEC2572_2_best_next",
            "decision": "FIRST_COMMON_FRAME_COUPLING_PPN_KERNEL_OR_PARENT_ACTION_GRAMMAR_SELECTED",
            "reason": "PPN gives the cleanest local-GR-facing pressure test, while a typed parent action grammar remains the least empirical derivation route.",
            "effect": "next checkpoint should either sign the ordinary-sector action grammar or build the first PPN response-kernel row",
        },
        {
            "decision_id": "DEC2572_3_route_guard",
            "decision": "R10_HELD_LATER_AS_GUARDED_SOURCE_LEG",
            "reason": "R10 still needs a finite-range operator and real alpha(lambda) bound chain; coupling source legs cannot replace that.",
            "effect": "do not route no-shadow failure into R10 claims",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2572_0_selected",
            "selection_status": "selected",
            "target_file": "2573-Y5-R2FR-first-common-frame-coupling-PPN-response-kernel-or-parent-action-grammar.md",
            "target_script": "scripts/Y5_R2FR_first_common_frame_coupling_PPN_response_kernel_or_parent_action_grammar_2573.py",
            "task": "try to sign a typed parent ordinary-sector action grammar that forbids hidden coframe/source/coupling slots; if it remains unsigned, stage the first source-ready PPN response kernel mapping b_R,d_R,endpoint,kappa_MTS,ell_J leaks to gamma,beta and preferred-frame residuals",
            "acceptance_target": "one parent action-domain theorem clause or one source-ready PPN response-kernel row; all local-GR/Newton claims blocked unless theorem-zero or source-backed numeric bounds exist",
            "guardrails": "no same-frame shortcut; no WEP/Ward shortcut; no q_shape shortcut; no fitted GM/H0; no R10 shortcut; no EH import; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "action_domain": OUTPUTS["action_domain"],
        "zero_theorem": OUTPUTS["zero_theorem"],
        "coupling_shadow": OUTPUTS["coupling_shadow"],
        "response_kernel": OUTPUTS["response_kernel"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2572_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2572_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2572_01_action_domain_verdict_blocked",
        any(row["clause_id"] == "AD2572_5_verdict" and row["status"] == "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS" for row in data["action_domain"]),
        "action-domain no-shadow proof attempt is explicit and blocked",
    )
    add(
        "VAL2572_02_zero_theorem_conditional",
        any(row["theorem_id"] == "ZTH2572_0_exact_conditional_no_shadow" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in data["zero_theorem"]),
        "exact conditional no-shadow theorem is retained",
    )
    add(
        "VAL2572_03_coupling_zero_conditional",
        any(row["theorem_id"] == "ZTH2572_1_coefficient_descent" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in data["zero_theorem"]),
        "coefficient/coupling zero theorem is exact but conditional",
    )
    add(
        "VAL2572_04_coupling_shadow_rows",
        len(data["coupling_shadow"]) >= 5 and all(row["valid_for_claim"] is False for row in data["coupling_shadow"]),
        "coupling/source-scale shadow rows are present and nonclaim",
    )
    add(
        "VAL2572_05_countermodels_retained",
        len(data["countermodels"]) >= 6 and all(row["valid_for_claim"] is False for row in data["countermodels"]),
        "Weyl, disformal, source-prefactor, coupling, endpoint and q_shape countermodels remain live",
    )
    add(
        "VAL2572_06_first_kernel_selected",
        any(row["kernel_id"] == "KER2572_0_PPN_metric_coupling" and row["selected_priority"] == "SELECTED_FIRST_KERNEL_NONCLAIM" for row in data["response_kernel"]),
        "PPN metric/coupling response kernel is selected as first fallback",
    )
    add(
        "VAL2572_07_kernel_rows_nonclaim",
        all(row["valid_for_claim"] is False for row in data["response_kernel"]),
        "all response-kernel rows are nonclaim and missing-input guarded",
    )
    add("VAL2572_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]), "no gate allows no-shadow, coupling, local-GR, PPN, R10 or Newton claim")
    add(
        "VAL2572_09_shortcuts_rejected",
        any(row["gate_id"] == "GATE2572_5_no_shortcuts" and row["gate_pass"] is True for row in data["claim_gates"]),
        "same-frame, WEP, Ward, q_shape, fitted-GM/H0, EH import and R10 shortcuts are rejected",
    )
    add(
        "VAL2572_10_next_target_written",
        any(row["route_id"] == "NEXT2572_0_selected" for row in data["next_target"]),
        "2573 parent action grammar or common-frame/coupling PPN response target selected",
    )
    add("VAL2572_11_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["branch_copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2572*", "*P8_Y5_NO_SHADOW_2572*", "*JR2572*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2572_12_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2572 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2572_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2572_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2572_OVERALL",
        overall,
        "2572 blocks no-shadow/coupling promotion, preserves exact conditional theorem, stages coupling shadow rows, and selects 2573",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2572 Y5 R2FR Terminal Public Coframe No-Shadow Action Domain Or First Response Kernel",
        "",
        "**Status:** no public/local claim. The no-shadow theorem is exact only as a conditional theorem, and the current corpus still does not derive the parent action-domain grammar that excludes hidden Weyl, disformal, source-prefactor, endpoint and coupling/source-scale slots.",
        "",
        "**Main result:** the derivation route sharpened but did not close. The required parent contract is now exact: ordinary readout must factor through terminal `e_pub=E(Q_vis)`, and visible couplings/source scales must descend as parent-owned q-basic coefficients before any empirical `G_ref`, `GM`, `H0` or local-test normalization is used. Without that, local GR can still be spoiled by `b_R`, `d_R`, `w_R`, endpoint leakage, `kappa_MTS`, `ell_J`, or visible constants even when the coframe is shared. Therefore the disciplined fallback is a first PPN common-frame-plus-coupling response kernel, not a claim.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Action-Domain Contract",
        markdown_table(data["action_domain"], ["clause_id", "clause", "formal_statement", "status", "proof_attempt", "blocker", "implication_if_signed", "valid_for_claim"]),
        "",
        "## Zero Theorem",
        markdown_table(data["zero_theorem"], ["theorem_id", "theorem_statement", "status", "proof_or_failure", "required_clauses", "consequence", "valid_for_claim"]),
        "",
        "## Coupling Shadow Audit",
        markdown_table(data["coupling_shadow"], ["coupling_id", "object", "shadow_risk", "current_owner", "zero_condition", "current_status", "finite_fallback", "valid_for_claim"]),
        "",
        "## Countermodel Ledger",
        markdown_table(data["countermodels"], ["countermodel_id", "ansatz", "why_it_survives", "kills_shortcut", "required_fix", "valid_for_claim"]),
        "",
        "## Response-Kernel Acquisition",
        markdown_table(data["response_kernel"], ["kernel_id", "arena", "selected_priority", "candidate_relation", "required_inputs", "missing_inputs", "reason_for_priority", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "action_domain": action_domain_rows(),
        "zero_theorem": zero_theorem_rows(),
        "coupling_shadow": coupling_shadow_rows(),
        "countermodels": countermodel_rows(),
        "response_kernel": response_kernel_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["action_domain"], data["action_domain"])
    write_csv(OUTPUTS["zero_theorem"], data["zero_theorem"])
    write_csv(OUTPUTS["coupling_shadow"], data["coupling_shadow"])
    write_csv(OUTPUTS["countermodels"], data["countermodels"])
    write_csv(OUTPUTS["response_kernel"], data["response_kernel"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2572_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
