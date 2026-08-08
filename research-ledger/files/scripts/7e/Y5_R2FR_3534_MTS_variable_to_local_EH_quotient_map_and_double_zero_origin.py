from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3534-Y5-R2FR-MTS-variable-to-local-EH-quotient-map-and-double-zero-origin.md"
CANONICAL_STATUS = OUT / "P8_local_GR_MTS_variable_quotient_double_zero_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3534": {"path": Path(__file__).resolve(), "role": "3534 generator"},
    "doc_3533": {
        "path": ROOT / "3533-Y5-R2FR-local-EH-quotient-action-kernel-and-universal-matter-source.md",
        "role": "3533 local EH quotient kernel handoff",
    },
    "status_3533": {
        "path": OUT / "P8_local_GR_EH_quotient_action_kernel_status.csv",
        "role": "3533 canonical action-kernel status",
    },
    "next_3533": {
        "path": OUT / "P8_Y5_R2FR_3533_NEXT_TARGET.csv",
        "role": "3533-selected MTS variable map target",
    },
    "action_kernel_3533": {
        "path": OUT / "P8_Y5_R2FR_3533_ACTION_KERNEL.csv",
        "role": "3533 action kernel blocks",
    },
    "euler_tests_3533": {
        "path": OUT / "P8_Y5_R2FR_3533_EULER_ZERO_TESTS.csv",
        "role": "3533 kernel Euler tests",
    },
    "symbol_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "existing MTS symbol to local-GR map",
    },
    "qap_status": {
        "path": OUT / "P8_EM_quotient_action_derives_q_normal_form_status.csv",
        "role": "quotient action principle status",
    },
    "double_zero_memory": {
        "path": OUT / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "role": "double-zero memory origin attempt",
    },
    "double_zero_decision": {
        "path": OUT / "P8_DOUBLE_ZERO_MEMORY_DECISION.csv",
        "role": "double-zero decision ledger",
    },
    "double_zero_r11_clause": {
        "path": OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv",
        "role": "local silence multiplet and Sigma_loc clause",
    },
    "domain_selector_clause": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "role": "domain selector parent action clause",
    },
    "domain_variation": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "domain selector variation chain",
    },
    "qcoh_contract": {
        "path": OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv",
        "role": "Qcoh parent action contract",
    },
    "charge_current": {
        "path": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "charge-current equality attempt",
    },
    "em_hodge_vector": {
        "path": OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "role": "EM Hodge/Maxwell residual vector",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical residual bounds",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def variable_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "MQM3534_0_q_gobs",
            "MTS_symbol": "q(Phi); g_obs; observed coframe",
            "kernel_slot": "quotient base, not silent Y",
            "proposed_mapping": "q(Phi) defines the observed metric/coframe used by matter, clocks, Maxwell Hodge star, Hilbert stress and Hamiltonian charge.",
            "local_zero_or_invariance_condition": "vertical MTS variations D_Y leave q fixed: D_Y g_obs=0 and D_Y tau_obs=0 on the compact local branch",
            "double_zero_origin_candidate": "quotient invariance forbids q-private representative dependence in local scalar observables",
            "current_verdict": "BEST_ANCHOR_CONDITIONAL_QAP_UNSIGNED",
            "source_path": str(SOURCES["qap_status"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_1_Gamma_Khat",
            "MTS_symbol": "Gamma_eff; K_hat^{mu nu}",
            "kernel_slot": "silent connection/boundary residual Y_GammaK",
            "proposed_mapping": "Gamma_eff and K_hat are not new local forces; they must be the vertical Ward pair whose projected divergence defines q_loc^nu.",
            "local_zero_or_invariance_condition": "P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})=0 follows only if the pair is exact/on-shell in the local quotient",
            "double_zero_origin_candidate": "Ward-exact pair or boundary-exact pair; otherwise coefficient-bound branch",
            "current_verdict": "NOT_ZERO_OWNED_ROUTE_IDENTIFIED",
            "source_path": str(SOURCES["symbol_map"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_2_q_loc",
            "MTS_symbol": "q_loc^nu",
            "kernel_slot": "derived residual, not fundamental field",
            "proposed_mapping": "q_loc^nu is the local Ward/projection residual generated after quotienting, boundary subtraction and Pi_M readout.",
            "local_zero_or_invariance_condition": "q_loc^nu=0 if Gamma/Khat is exact, the local branch has no normal flux, and P_loc is charge-owned",
            "double_zero_origin_candidate": "no independent coupling; q_loc is downstream of exact Ward identity plus double-zero local Y channels",
            "current_verdict": "DERIVED_RESIDUAL_SHARPENED_NOT_CLOSED",
            "source_path": str(SOURCES["symbol_map"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_3_Ploc_PiM",
            "MTS_symbol": "P_loc; Pi_M",
            "kernel_slot": "charge-owned projector/readout",
            "proposed_mapping": "P_loc must reduce to the EH/Hilbert mass charge projector Pi_M^H before readout; no data-chosen smoothing projector.",
            "local_zero_or_invariance_condition": "[D_Y,Pi_M^H]J_H=0 when D_Y g_obs=D_Y tau_obs=D_Y J_H=0 and Pi_M is topological/charge-defined",
            "double_zero_origin_candidate": "charge identification plus quotient invariance; not a separate Sigma_loc factor",
            "current_verdict": "CONDITIONAL_ZERO_FROM_3532_3533",
            "source_path": str(SOURCES["charge_current"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_4_chiD",
            "MTS_symbol": "chi_D; Sigma_D",
            "kernel_slot": "auxiliary scalar component of Y_loc",
            "proposed_mapping": "chi_D is allowed only as an auxiliary scalar constrained by scalar/topological Sigma_D, not as a propagating domain wall.",
            "local_zero_or_invariance_condition": "chi_local=Sigma_local=0 and lambda_local=0 via delta_lambda and double-zero chi_D^2 coupling",
            "double_zero_origin_candidate": "S_mem,D proportional to chi_D^2, or chi_D=|A_D| from a norm-square amplitude",
            "current_verdict": "SUFFICIENT_VARIATION_CHAIN_NOT_PARENT_ORIGIN",
            "source_path": str(SOURCES["domain_selector_clause"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_5_Qcoh",
            "MTS_symbol": "Qcoh; Q_D; trace/STF load",
            "kernel_slot": "local silence multiplet component Y_Q",
            "proposed_mapping": "Qcoh contributes only through trace/source charge or through a local-silent STF/domain deviation in Y_loc.",
            "local_zero_or_invariance_condition": "local compact isotropy/constraint kills STF and domain parts: Qcoh_D=0 or Pi_STF Qcoh=0",
            "double_zero_origin_candidate": "det(Qcoh) current or norm-square tr(Q_STF^2) starts at quadratic/cubic order",
            "current_verdict": "BEST_DOUBLE_ZERO_CLUE_PARENT_OWNERSHIP_MISSING",
            "source_path": str(SOURCES["qcoh_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_6_memory",
            "MTS_symbol": "memory; B_mem; U_mem; I_M",
            "kernel_slot": "operator activation coefficient C_i(Y), not direct local source",
            "proposed_mapping": "memory may remain cosmologically active but local compact coupling must factor through Sigma_loc or chi_D^2.",
            "local_zero_or_invariance_condition": "C_mem(Y)=c_mem Sigma_loc+O(Y^3) with Sigma_loc=G_AB Y^A Y^B; no linear local memory vertex",
            "double_zero_origin_candidate": "norm-square local silence multiplet, determinant coherent-current route, or topological pairing",
            "current_verdict": "DOUBLE_ZERO_REQUIREMENT_DERIVED_ORIGIN_NOT_SIGNED",
            "source_path": str(SOURCES["double_zero_memory"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_7_flow",
            "MTS_symbol": "u^mu; h_mu_nu; X=nabla.u; shear/vector pieces",
            "kernel_slot": "preferred-frame/vector components of Y_loc",
            "proposed_mapping": "flow variables are admissible only as constrained local-zero kinematic auxiliaries, not as preferred local frame forces.",
            "local_zero_or_invariance_condition": "stationary compact Killing branch forces X=0, vector flux=0 and STF shear=0",
            "double_zero_origin_candidate": "SO(3) local isotropy: no scalar action term linear in vector/STF non-singlet without a spurion",
            "current_verdict": "REPRESENTATION_ZERO_ROUTE_NEEDS_PARENT_SELECTOR",
            "source_path": str(SOURCES["symbol_map"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_8_Lcg",
            "MTS_symbol": "L_cg; ell_tr",
            "kernel_slot": "derived scale from Y operator spectrum",
            "proposed_mapping": "transition scale should be mass-gap/domain-spectrum output of the Y_loc Hessian, not an independent local switch.",
            "local_zero_or_invariance_condition": "ell_tr/L_cg derives from eigenvalues of M^2_AB and source/domain boundary conditions",
            "double_zero_origin_candidate": "no local coupling if compact branch is below activation threshold and Y=0 is stable",
            "current_verdict": "DERIVATION_TARGET_NOT_FILLED",
            "source_path": str(SOURCES["symbol_map"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_9_EM_Maxwell",
            "MTS_symbol": "EM Hodge/Maxwell/Poynting residuals; C_XF2",
            "kernel_slot": "visible gauge stress owned by g_obs plus residual C_EM(Y)",
            "proposed_mapping": "Maxwell stress uses the same g_obs Hodge star; any hidden MTS coupling to F^2 or Poynting flux must factor through Sigma_loc or be bounded.",
            "local_zero_or_invariance_condition": "Delta_Hodge_EM=0 and C_XF2(Y)=O(Sigma_loc); stationary isolated source has no net Poynting boundary flux",
            "double_zero_origin_candidate": "quotient-visible Maxwell action plus nonbasic hidden fields excluded at linear order",
            "current_verdict": "COMPATIBLE_WITH_3520_3533_BUT_EM_ROWS_REMAIN_BOUND_REQUIRED",
            "source_path": str(SOURCES["em_hodge_vector"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "map_id": "MQM3534_10_kappa_G",
            "MTS_symbol": "kappa_eff; G_eff",
            "kernel_slot": "calibrated/topological constant, not local Y",
            "proposed_mapping": "G_ref/kappa0 belongs to the EH/source normalization product, not a local motion-memory field.",
            "local_zero_or_invariance_condition": "D_Y kappa_eff=0 and local D_t/r/source kappa drift zero by topological/superselection route",
            "double_zero_origin_candidate": "topological zero-form/three-form route, separate from Sigma_loc",
            "current_verdict": "CALIBRATED_OR_INTEGRATION_CONSTANT_NOT_DERIVED_FROM_MTS",
            "source_path": str(SOURCES["symbol_map"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def double_zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "DZT3534_0_representation_no_linear_singlet",
            "claim": "Local linear MTS hair is absent if every local residual variable is a non-singlet/sign-odd vertical variable and the parent action has no spurion selecting it.",
            "mathematical_form": "Y^A in nontrivial reps of H_loc; scalar Lagrangian invariant under H_loc => partial_A C_i(0)=0",
            "why_it_helps": "gives C_i(0)=dC_i(0)=0 without hand-tuning each coefficient",
            "status": "NEW_DERIVATION_ROUTE_CONDITIONAL",
            "remaining_gap": "prove actual MTS variables fall into nontrivial reps or constrained amplitudes",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DZT3534_1_norm_square_sigma",
            "claim": "If the local silence multiplet has positive parent metric G_AB and couplings depend on Sigma_loc=G_AB Y^A Y^B, all factored operators are double-zero.",
            "mathematical_form": "C_i(Y)=c_i Sigma_loc+O(Sigma_loc^2); C_i(0)=0; partial_A C_i(0)=0",
            "why_it_helps": "turns many R10/PPN/clock/WEP/R11 local residuals into one parent-owned double-zero theorem",
            "status": "SUFFICIENT_MECHANISM_ALREADY_COMPATIBLE_WITH_R11_CLAUSE",
            "remaining_gap": "G_AB positivity and universal factorization are not parent-derived",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DZT3534_2_aux_scalar_exception",
            "claim": "A scalar selector such as chi_D can carry a linear invariant, so it must be auxiliary and squared or it breaks the proof.",
            "mathematical_form": "linear f(chi_D)=chi_D rejected; f(chi_D)=chi_D^2 gives f(0)=f'(0)=0 and lambda_local=0",
            "why_it_helps": "identifies exactly where closure smoke enters: scalar linear domain switches",
            "status": "STRICT_GATE",
            "remaining_gap": "derive chi_D=Sigma_D=0 from local spectral/topological theorem",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DZT3534_3_det_Qcoh_route",
            "claim": "A coherent determinant/current route can produce at least a double zero, possibly cubic, if Qcoh is parent-owned.",
            "mathematical_form": "J_C ~ det(Qcoh) or tr(Q_STF^2); J_C(0)=0 and dJ_C(0)=0",
            "why_it_helps": "gives a more MTS-flavoured origin for p>=2 than simply declaring chi_D^2",
            "status": "BEST_PHYSICAL_CLUE_NOT_PARENT_OWNED",
            "remaining_gap": "Qcoh must be an action variable or Noether/load tensor, not a post-processor",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DZT3534_4_topological_projector",
            "claim": "Metric-independent topological/domain projectors can avoid bulk stress and preferred-frame leakage.",
            "mathematical_form": "delta_g P_MTS,D=0; delta_g S_top=boundary/exact; no Hodge/metric projector",
            "why_it_helps": "stops the projector from reintroducing PPN/R11 stress after the double-zero coupling",
            "status": "CONDITIONAL_PROJECTOR_ROUTE",
            "remaining_gap": "parent ownership of P_MTS,D and local trivial-class theorem remain open",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "DZT3534_5_QAP_visible_stack",
            "claim": "The quotient action principle can forbid q-private hidden source operators but does not by itself prove EH or all q-basic towers vanish.",
            "mathematical_form": "S_phys=Sbar[q(Phi),visible fields]+Sigma_loc O_hidden + allowed q-basic terms",
            "why_it_helps": "protects Maxwell/matter source descent while preserving the need for R11 coefficient gates",
            "status": "PARTIAL_DERIVATION_NOT_LOCAL_GR_PROOF",
            "remaining_gap": "EH operator selection and q-basic non-EH tower silence",
            "valid_for_claim": "False",
        },
    ]


def residual_channel_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "RCH3534_0_RPiM_RHtau",
            "local_channel": "source denominator double zero",
            "killed_if": "MQM3534_0 + MQM3534_3 + DZT3534_1 + boundary no-flux hold",
            "survives_as": "C_PiM and C_Htau bound rows from 3532",
            "observable_links": "Newton; Gdot; PPN; R10; orbital GM",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "channel_id": "RCH3534_1_domain_PPN",
            "local_channel": "domain vector/STF/source-normalization",
            "killed_if": "chi_D auxiliary squared, Sigma_local=0, P_MTS,D topological, R11 factorized by Sigma_loc",
            "survives_as": "alpha1/alpha2/alpha3/xi/R11 coefficient products",
            "observable_links": "PPN alpha_i; xi; R11; WEP",
            "current_status": "STRICTEST_ALPHA3_GATE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "channel_id": "RCH3534_2_memory_cosmo_local_split",
            "local_channel": "memory active cosmologically but silent locally",
            "killed_if": "compact local branch has Y_loc=0 while FLRW branch has nonzero scalar/domain invariant",
            "survives_as": "branch-switch residual or L_cg/ell_tr derivation debt",
            "observable_links": "cosmology; galaxies; Gdot; local fifth force",
            "current_status": "COMPATIBLE_ROUTE_NEEDS_BRANCH_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "channel_id": "RCH3534_3_EM_visible_stack",
            "local_channel": "Maxwell/EM stress and Poynting boundary flux",
            "killed_if": "EM Hodge star is g_obs and hidden F^2/Poynting couplings factor through Sigma_loc with stationary no-flux",
            "survives_as": "Delta_Hodge_EM; C_XF2; Phi_EM_rad; Delta_J_total",
            "observable_links": "Maxwell; alpha_EM; clock; WEP; PPN; Gdot",
            "current_status": "PARTIAL_VISIBLE_ROUTE_BOUND_ROWS_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "channel_id": "RCH3534_4_G_kappa",
            "local_channel": "G/kappa source normalization",
            "killed_if": "topological/superselection kappa plus fixed common matter action-density line",
            "survives_as": "D_X ln(G_ref w_common ell_J R_frame)",
            "observable_links": "Gdot; Newton; clocks; PPN",
            "current_status": "CALIBRATED_CONSTANT_NOT_MTS_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3534_0_variable_ownership",
            "requirement": "Every Y_loc component is an action variable, constrained auxiliary, or derived Noether/load tensor.",
            "failure_mode": "post-fit projector/smoother/selector masquerades as a field",
            "next_action_if_failed": "keep coefficient/bound branch",
            "passed_now": "False",
        },
        {
            "gate_id": "G3534_1_no_linear_singlet",
            "requirement": "No local scalar singlet linear in Y_loc appears in S_matter, S_EM, S_R11, source normalization, or boundary flux.",
            "failure_mode": "linear scalar selector or hidden source weight creates WEP/PPN/R10 residuals",
            "next_action_if_failed": "bound the corresponding coefficient directly",
            "passed_now": "False",
        },
        {
            "gate_id": "G3534_2_positive_norm_square",
            "requirement": "Sigma_loc=G_AB Y^A Y^B has parent-positive G_AB and compact local branch Y=0.",
            "failure_mode": "double-zero factor is a named closure switch rather than a derived invariant",
            "next_action_if_failed": "derive Hessian/mass-gap or demote Sigma_loc to closure",
            "passed_now": "False",
        },
        {
            "gate_id": "G3534_3_universal_factorization",
            "requirement": "All local non-EH/source-normalization operators factor by Sigma_loc or are topological/exact.",
            "failure_mode": "one unfactored q-basic operator reopens R11/PPN/fifth-force rows",
            "next_action_if_failed": "build R11 coefficient vector with no missing rows",
            "passed_now": "False",
        },
        {
            "gate_id": "G3534_4_same_visible_stack",
            "requirement": "Matter, clocks, EM, Hilbert stress and Hamiltonian charge use the same g_obs/coframe and tau.",
            "failure_mode": "same-looking GR limit hides frame/source/readout mismatch",
            "next_action_if_failed": "retain R_frame/R_units/Delta_Hodge_EM rows",
            "passed_now": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3534_0_best_theorem_route",
            "decision": "Pursue the representation/norm-square double-zero theorem.",
            "rationale": "It is less suspicious than tuning each local coefficient and directly explains why linear local MTS hair is absent.",
            "effect": "focus next proof on Y_loc ownership, local symmetry, and Sigma_loc positivity/factorization",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3534_1_scalar_selector_warning",
            "decision": "Treat scalar selectors as dangerous unless auxiliary and squared.",
            "rationale": "A scalar can appear linearly in the action; this is exactly how local GR gets broken by a hidden switch.",
            "effect": "chi_D must be derived as Sigma/norm/topological class or sent to coefficient bounds",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3534_2_no_promotion",
            "decision": "Do not promote local GR/Newton/PPN/EM pass yet.",
            "rationale": "The map is sharper and more physical, but parent ownership and universal factorization are still unproved.",
            "effect": "all claim flags remain false",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3534_0_variable_map",
            "quantity": "MTS_to_local_EH_quotient_map",
            "value": "constructed_with_actual_MTS_symbols",
            "meaning": "Gamma/Khat/q_loc/P_loc/Pi_M/chi_D/Qcoh/memory/flow/EM/kappa have explicit kernel placements",
            "claim_effect": "route is sharper but not claim-valid",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3534_1_double_zero",
            "quantity": "double_zero_origin",
            "value": "representation_norm_square_route_identified",
            "meaning": "linear local hair can be killed by local symmetry plus Sigma_loc=G_AB Y^A Y^B, if parent-owned",
            "claim_effect": "no PPN/R10/R11 pass until gates close",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3534_2_next",
            "quantity": "next_best_target",
            "value": "Yloc_Euler_equations_and_positive_Hessian_gate",
            "meaning": "derive Y_loc=0 and Sigma_loc positivity/factorization from an explicit parent variation",
            "claim_effect": "best next route to derived local GR",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3535-Y5-R2FR-Yloc-Euler-equations-positive-Hessian-and-R11-factorization-gate.md",
            "next_script": "scripts/Y5_R2FR_3535_Yloc_Euler_equations_positive_Hessian_and_R11_factorization_gate.py",
            "objective": "Attempt the parent variation that forces Y_loc=0, proves Sigma_loc=G_AB Y^A Y^B is positive, and checks whether every local non-EH/source operator factors through Sigma_loc.",
            "success_gate": "Either derive Y_loc=0 with positive Hessian and universal R11/source factorization, or emit explicit coefficient/bound rows for every unfactored local channel.",
            "why_next": "3534 maps actual MTS variables to the kernel and identifies the least-suspicious double-zero origin; now the Euler equations must own it.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    variable_map: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3534_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    mapped_symbols = ";".join(row["MTS_symbol"] for row in variable_map)
    required_fragments = ["Gamma_eff", "K_hat", "q_loc", "P_loc", "Pi_M", "chi_D", "Qcoh", "memory"]
    checks.append({"check_id": "VAL3534_1_actual_MTS_symbols_mapped", "passed": bool_text(all(fragment in mapped_symbols for fragment in required_fragments)), "detail": "Gamma/Khat/q_loc/P_loc/Pi_M/chi_D/Qcoh/memory included", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_2_double_zero_theorem_route", "passed": bool_text(any(row["theorem_id"] == "DZT3534_0_representation_no_linear_singlet" for row in theorem) and any(row["theorem_id"] == "DZT3534_1_norm_square_sigma" for row in theorem)), "detail": "representation and norm-square double-zero routes written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_3_scalar_selector_warning", "passed": bool_text(any(row["theorem_id"] == "DZT3534_2_aux_scalar_exception" for row in theorem) and any(row["decision_id"] == "DEC3534_1_scalar_selector_warning" for row in decisions)), "detail": "linear scalar selector risk is explicit", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_4_residual_channels_covered", "passed": bool_text({"RCH3534_0_RPiM_RHtau", "RCH3534_1_domain_PPN", "RCH3534_3_EM_visible_stack", "RCH3534_4_G_kappa"} <= {row["channel_id"] for row in channels}), "detail": "PiM/Htau, domain/PPN, EM, and G/kappa channels covered", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_5_gates_not_falsely_passed", "passed": bool_text(all(row["passed_now"] == "False" for row in gates)), "detail": "theorem gates are retained rather than promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + variable_map + theorem + channels + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/PPN/EM claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3535-Y5-R2FR-Yloc-Euler")), "detail": "3535 Yloc Euler/Hessian target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3534_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3534_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3534_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    variable_map: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3534 - MTS Variable To Local EH Quotient Map And Double-Zero Origin

## Summary
- **Actual MTS variables mapped:** `Gamma_eff`, `K_hat`, `q_loc`, `P_loc/Pi_M`, `chi_D`, `Qcoh`, memory, flow variables, EM residuals, and `kappa/G` now have explicit slots in the `g_obs/Y^A` kernel.
- **Main derivation route:** local MTS residuals must be non-singlet/sign-odd vertical variables or auxiliary squared scalars, so invariant local action terms cannot be linear in them.
- **Double-zero origin:** `Sigma_loc = G_AB Y^A Y^B` gives `C_i(0)=0` and `partial_A C_i(0)=0` if `G_AB` and factorization are parent-owned.
- **Hard warning:** scalar selectors like `chi_D` are dangerous; linear `chi_D` is rejected for local GR unless directly bounded.
- **Current verdict:** stronger and more physical than a gap ledger, but still not a local-GR claim. The next proof must derive `Y_loc=0`, positivity, and R11/source factorization.

## Core Theorem Candidate
Let `Y_loc^A` be the local residual multiplet containing the non-GR MTS channels. If the compact local branch has

`Y_loc^A = 0`,

and the parent action allows local operators only through

`Sigma_loc = G_AB Y_loc^A Y_loc^B >= 0`,

then any local operator coefficient

`C_i(Y)=c_i Sigma_loc + O(Sigma_loc^2)`

satisfies `C_i(0)=0` and `partial_A C_i(0)=0`. That is the clean double-zero route: no plateau axiom, no fitted GM trick, and no linear hidden local force.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## MTS Variable Map
{markdown_table(variable_map, ["map_id", "MTS_symbol", "kernel_slot", "proposed_mapping", "local_zero_or_invariance_condition", "double_zero_origin_candidate", "current_verdict", "source_path", "valid_for_claim"])}

## Double-Zero Theorem Routes
{markdown_table(theorem, ["theorem_id", "claim", "mathematical_form", "why_it_helps", "status", "remaining_gap", "valid_for_claim"])}

## Residual Channel Effects
{markdown_table(channels, ["channel_id", "local_channel", "killed_if", "survives_as", "observable_links", "current_status", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "requirement", "failure_mode", "next_action_if_failed", "passed_now"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    variable_map = variable_map_rows()
    theorem = double_zero_theorem_rows()
    channels = residual_channel_rows()
    gates = gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3534_SOURCE_REGISTER.csv",
        "variable_map": OUT / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv",
        "double_zero_routes": OUT / "P8_Y5_R2FR_3534_DOUBLE_ZERO_THEOREM_ROUTES.csv",
        "residual_channels": OUT / "P8_Y5_R2FR_3534_RESIDUAL_CHANNEL_EFFECTS.csv",
        "promotion_gates": OUT / "P8_Y5_R2FR_3534_PROMOTION_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3534_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3534_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3534_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3534_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["variable_map"], variable_map, ["map_id", "MTS_symbol", "kernel_slot", "proposed_mapping", "local_zero_or_invariance_condition", "double_zero_origin_candidate", "current_verdict", "source_path", "valid_for_claim"])
    write_csv(outputs["double_zero_routes"], theorem, ["theorem_id", "claim", "mathematical_form", "why_it_helps", "status", "remaining_gap", "valid_for_claim"])
    write_csv(outputs["residual_channels"], channels, ["channel_id", "local_channel", "killed_if", "survives_as", "observable_links", "current_status", "valid_for_claim"])
    write_csv(outputs["promotion_gates"], gates, ["gate_id", "requirement", "failure_mode", "next_action_if_failed", "passed_now"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, variable_map, theorem, channels, gates, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, variable_map, theorem, channels, gates, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
