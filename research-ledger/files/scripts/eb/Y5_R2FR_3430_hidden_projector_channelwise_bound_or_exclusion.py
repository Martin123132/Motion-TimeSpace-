from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3430-Y5-R2FR-hidden-projector-channelwise-bound-or-exclusion-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3429": ROOT / "3429-Y5-R2FR-gapped-Y6-nohair-positive-operator-or-DeltaExtra-row-under-AX1090.md",
    "gapped_channels_3429": OUT / "P8_Y5_R2FR_3429_GAPPED_CHANNEL_ROWS.csv",
    "validation_3429": OUT / "P8_Y5_BRR545_3429_VALIDATION.csv",
    "extra_mass_3428": OUT / "P8_Y5_R2FR_3428_EXTRA_MASS_DECOMPOSITION.csv",
    "mu_extra_owner": OUT / "P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
    "mu_extra_zero_gate": OUT / "P8_MU_EXTRA_ZERO_OWNER_GATE.csv",
    "domain_projector_coeffs": OUT / "P8_mu_extra_domain_projector_coefficients.csv",
    "local_zero_premises": OUT / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
    "qcoh_projector_algebra": OUT / "P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv",
    "projector_stress_2407": OUT / "P8_Y5_PARENT_QLOC_2407_PROJECTOR_VARIATION_STRESS_AUDIT.csv",
    "chainmap_2419": OUT / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv",
    "q_vertical_2420": OUT / "P8_Y5_PARENT_QLOC_2420_Q_VERTICAL_NOPOLE_ROUTE_LEDGER.csv",
    "readout_2418": OUT / "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv",
    "gamma_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "gamma_stress": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "gamma_residual": OUT / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
    "response_doublet": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "source_measure_residual": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "boundary_3427": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "pc3400_3429": OUT / "P8_Y5_R2FR_3429_PC3400_4_UPDATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3430_SOURCE_REGISTER.csv",
    "hidden_channel_decomposition": OUT / "P8_Y5_R2FR_3430_HIDDEN_CHANNEL_DECOMPOSITION.csv",
    "exclusion_theorem": OUT / "P8_Y5_R2FR_3430_CHANNEL_EXCLUSION_THEOREM.csv",
    "channel_audit": OUT / "P8_Y5_R2FR_3430_CHANNELWISE_EXCLUSION_AUDIT.csv",
    "residual_bound_rows": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
    "pc3400_4_update": OUT / "P8_Y5_R2FR_3430_PC3400_4_UPDATE.csv",
    "nohair_activation_update": OUT / "P8_Y5_R2FR_3430_NOHAIR_ACTIVATION_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3430_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3430_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3430_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3430_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3430_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3429": "handoff from gapped/Y6 no-hair theorem",
        "gapped_channels_3429": "open hidden/projector channels from 3429",
        "validation_3429": "prior checkpoint validation",
        "extra_mass_3428": "Delta_extra channel decomposition",
        "mu_extra_owner": "historic mu_extra channel owner ledger",
        "mu_extra_zero_gate": "zero-owner gate conditions",
        "domain_projector_coeffs": "domain/projector observable coefficient map",
        "local_zero_premises": "local-zero premise requirements",
        "qcoh_projector_algebra": "trace/coherent projector algebra",
        "projector_stress_2407": "projector stress variation audit",
        "chainmap_2419": "source-worldtube/projector chain-map gate",
        "q_vertical_2420": "q-vertical no-pole route ledger",
        "readout_2418": "readout no-reentry gate",
        "gamma_contract": "Gamma/Khat/q_loc first variation contract",
        "gamma_stress": "Gamma/Khat/q_loc stress rewrite",
        "gamma_residual": "Gamma/Khat/q_loc residual demotion paths",
        "response_doublet": "response/memory Euler source ledger",
        "source_measure_residual": "source-measure residual map",
        "boundary_3427": "reference/boundary flux rows",
        "pc3400_3429": "current no-extra-mass status",
    }
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        rows.append(
            {
                "source_id": key,
                "path": str(path),
                "exists": path.exists(),
                "role": roles[key],
                "valid_for_claim": False,
            }
        )
    return rows


def hidden_channel_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "HCD3430_0_domain_projector",
            "channel": "domain/projector selector stress",
            "enters_as": "delta Pi_M, delta P_loc, moving support/domain stress",
            "zero_routes": "fixed topological projector; parent scalar selector with no vector; delta_g Pi=0 and D_domain Pi=0",
            "fallback_symbol": "epsilon_domain_projector_abs",
            "evidence": "P8_Y5_PARENT_QLOC_2407_PROJECTOR_VARIATION_STRESS_AUDIT.csv; P8_mu_extra_domain_projector_coefficients.csv",
            "current_status": "NOT_EXCLUDED_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_1_PiM_source_worldtube",
            "channel": "PiM/source-worldtube chain-map",
            "enters_as": "[d,Pi_W]J_H, delta Pi_W J_H, support/readout reentry",
            "zero_routes": "identity/inclusion Hilbert branch; fixed-domain chain-map; source current descent",
            "fallback_symbol": "I_commutator_abs_over_MHref",
            "evidence": "P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv; 3426 chain-map result",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_2_GammaKhat_q_loc",
            "channel": "Gamma/Khat/q_loc effective stress",
            "enters_as": "P_loc(nabla Gamma_eff - nabla K_hat) or div T_GK",
            "zero_routes": "diffeomorphism-invariant S_GK with on-shell Euler closure and double zero",
            "fallback_symbol": "epsilon_q_loc_TGK_mass",
            "evidence": "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv; P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
            "current_status": "VARIATIONAL_OWNER_MISSING",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_3_response_memory",
            "channel": "response/memory doublet",
            "enters_as": "history kernel, trace response, odd/even source response",
            "zero_routes": "positive local memory kernel plus no history injection plus source-free odd residual",
            "fallback_symbol": "epsilon_memory_kernel_abs",
            "evidence": "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv; P8_Y5_R2FR_3429_GAPPED_CHANNEL_ROWS.csv",
            "current_status": "CANDIDATE_ONLY_NOT_ZEROED",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_4_boundary_symplectic",
            "channel": "boundary/reference/symplectic/topological flux",
            "enters_as": "B_zero, Delta_symp, reference charge shift, collar flux",
            "zero_routes": "fixed reference plus boundary silence plus same Hilbert charge on same linking surface",
            "fallback_symbol": "epsilon_boundary_symplectic_abs",
            "evidence": "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv; P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
            "current_status": "PARTIAL_HILBERT_IDENTITY_ONLY",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_5_metric_readout_reentry",
            "channel": "metric/readout reentry",
            "enters_as": "the measured metric, source denominator, or readout map reintroduces hidden sector dependence",
            "zero_routes": "readout is public g_obs/e_obs only and source denominator is same Hilbert/Hamiltonian charge",
            "fallback_symbol": "epsilon_readout_reentry_abs",
            "evidence": "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv; P8_Y5_R2FR_3424 PC3400 candidate",
            "current_status": "NO_REENTRY_NOT_FULLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "channel_id": "HCD3430_6_total_hidden",
            "channel": "hidden/projector total",
            "enters_as": "Delta_extra_hidden/M_H_ref and PPN residual vector",
            "zero_routes": "all channel rows independently zero or parent Ward identity signs exact cancellation",
            "fallback_symbol": "epsilon_hidden_total_abs",
            "evidence": "P8_MU_EXTRA_ZERO_OWNER_GATE.csv; P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
            "current_status": "NO_CANCELLATION_ABSOLUTE_SUM",
            "valid_for_claim": False,
        },
    ]


def exclusion_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CEX3430_0_decompose",
            "statement": "Hidden/projector extra mass and PPN stress must be decomposed channelwise before any local-GR claim.",
            "formula": "T_hidden = sum_i T_i; epsilon_hidden_total <= sum_i |epsilon_i|",
            "derivation_status": "EXACT_ACCOUNTING_RULE",
            "missing_or_condition": "none for accounting; numeric coefficients still needed for bounds",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_1_public_hilbert_absorption",
            "statement": "A channel is not hidden-extra if it is exactly the Hilbert variation of the public matter/EM action defining M_H.",
            "formula": "T_i = T_Hilbert(public) => Delta_extra_i = 0 by bookkeeping, not by cancellation",
            "derivation_status": "SAFE_DEMOTION_RULE",
            "missing_or_condition": "requires same public metric/readout and same source denominator",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_2_fixed_topological_no_stress",
            "statement": "A fixed topological/projector representative contributes no local stress if it is metric/domain independent and has zero boundary flux.",
            "formula": "delta_g Pi_i = 0, D_D Pi_i = 0, Phi_boundary_i = 0 => T_i=0",
            "derivation_status": "CONDITIONAL_ZERO_THEOREM",
            "missing_or_condition": "parent must sign fixed representative and boundary silence",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_3_chainmap_zero",
            "statement": "A source-worldtube projector creates no hidden source if it is a fixed chain map on the Hilbert-current complex.",
            "formula": "dJ_H=0, [d,Pi]J_H=0, delta Pi=0, J_H=q*Jbar_H => d(Pi J_H)=0 and delta(Pi J_H)=Pi delta J_H",
            "derivation_status": "CONDITIONAL_ZERO_THEOREM",
            "missing_or_condition": "source descent, fixed support, fixed projector, and M_H_ref are not all parent-signed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_4_vertical_no_pole",
            "statement": "A vertical hidden direction is locally silent only if matter and readout descend through the quotient and no boundary pole remains.",
            "formula": "v in ker Dq, delta_v S_matter=0, delta_v g_obs=0, Phi_v=0 => Q_v^monopole=0",
            "derivation_status": "CONDITIONAL_ZERO_THEOREM",
            "missing_or_condition": "q chart/equivalence and psi quotient route are still open",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_5_positive_operator_nohair",
            "statement": "A hidden field channel is zero if it qualifies for the 3429 positive-operator no-hair theorem.",
            "formula": "lambda_i>0 and J_i=B_i=R_i=0 => X_i=0 => Delta_extra_i=0",
            "derivation_status": "IMPORTS_3429_CONDITIONAL_THEOREM",
            "missing_or_condition": "channel-specific lambda_i, source-zero, boundary-zero, and projector residual-zero inputs",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_6_symmetry_invisibility",
            "statement": "Exact local isotropy can remove vector/STF PPN leakage, but it does not by itself remove monopole mass charge.",
            "formula": "SO(3) exact => alpha1_i=alpha2_i=alpha3_i=xi_i=0 for vector/STF pieces; monopole_i still audited separately",
            "derivation_status": "SYMMETRY_FILTER_NOT_FULL_ZERO",
            "missing_or_condition": "isotropy theorem and monopole/source denominator still needed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CEX3430_7_bound_if_not_zero",
            "statement": "If a zero theorem fails, the channel becomes an absolute residual row rather than a hidden cancellation.",
            "formula": "|epsilon_i| <= C_Pi||delta Pi_i|| + C_D||D_D Pi_i|| + C_J||J_i||*/lambda_i + |Phi_i|/M_H_ref + epsilon_readout_i",
            "derivation_status": "BOUND_CONTRACT_READY_VALUES_MISSING",
            "missing_or_condition": "operator norms, source norms, boundary fluxes, response constants, and M_H_ref",
            "valid_for_claim": False,
        },
    ]


def channel_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CHA3430_0_domain_projector",
            "channel": "domain/projector selector stress",
            "best_zero_attempt": "CEX3430_2 fixed-topological no-stress plus scalar selector",
            "why_it_could_work": "projector stress vanishes if Pi is a fixed topological representative and not a metric/domain functional",
            "why_not_closed": "PVS2407_2/PVS2407_4 retain Hodge/domain projector stress; P0/P3 local-zero premises are unsigned",
            "current_output": "bound epsilon_domain_projector_abs and keep PPN vector/shear rows live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_1_PiM_worldtube",
            "channel": "PiM/source-worldtube projector",
            "best_zero_attempt": "CEX3430_3 fixed chain-map on Hilbert current",
            "why_it_could_work": "identity/inclusion Pi_M branch creates no commutator stress and preserves EH/Hilbert charge",
            "why_not_closed": "CMG2419 requires source descent, fixed support/domain, fixed Pi, and M_H_ref; current old topological branch is demoted",
            "current_output": "bound I_commutator_abs_over_MHref and delta_PiW_JH",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_2_GammaKhat_q_loc",
            "channel": "Gamma/Khat/q_loc",
            "best_zero_attempt": "derive S_GK and use Euler/diffeomorphism identity",
            "why_it_could_work": "if T_GK is Hilbert stress of a diffeomorphism-invariant parent sector, divergence is on-shell controlled",
            "why_not_closed": "GK513 action existence/integrability/Euler closure/double-zero are not parent signed",
            "current_output": "bound epsilon_q_loc_TGK_mass and PPN residual vector instead of plateau axiom",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_3_response_memory",
            "channel": "response/memory doublet",
            "best_zero_attempt": "CEX3430_5 positive local kernel no-hair",
            "why_it_could_work": "a stable local memory kernel with no source/history injection relaxes to silent calibration",
            "why_not_closed": "Y0/Y1/Y4/Y5/Y6 response rows are not zeroed; history/source-normalization may be exchange-even",
            "current_output": "bound epsilon_memory_kernel_abs and source-normalization offsets",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_4_boundary_symplectic",
            "channel": "boundary/reference/symplectic flux",
            "best_zero_attempt": "fixed reference plus same Hilbert linking surface",
            "why_it_could_work": "3427 kills the old topological-Hilbert B_zero only on the identity/Hilbert branch",
            "why_not_closed": "residual MTS/Z/Y6/projector sectors can still create boundary/symplectic flux",
            "current_output": "bound epsilon_boundary_symplectic_abs and Delta_symp",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_5_metric_readout",
            "channel": "metric/readout reentry",
            "best_zero_attempt": "public g_obs/e_obs readout only",
            "why_it_could_work": "a single public metric and same Hilbert denominator prevent hidden pieces from re-entering measured GM",
            "why_not_closed": "readout no-reentry and M_H_ref/tau/source-normalization remain partial",
            "current_output": "bound epsilon_readout_reentry_abs",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CHA3430_6_total_guard",
            "channel": "hidden total",
            "best_zero_attempt": "all previous channels independently zero",
            "why_it_could_work": "then Delta_extra_hidden is empty without cancellation tricks",
            "why_not_closed": "no parent Ward identity currently signs cancellation among nonzero channels",
            "current_output": "absolute no-cancellation sum epsilon_hidden_total_abs",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "HBR3430_0_domain_projector",
            "channel": "domain/projector selector stress",
            "residual_symbol": "epsilon_domain_projector_abs",
            "symbolic_bound": "C_Pi_g||delta_g Pi|| + C_Pi_D||D_D Pi|| + C_vec||epsilon_domain_vector|| + C_flux||epsilon_domain_flux||",
            "needed_numeric_inputs": "operator norms for delta_g Pi and D_D Pi; W_domain_alpha1/alpha2/alpha3/xi; M_H_ref",
            "test_arenas": "PPN alpha1/alpha2/alpha3/xi; source-normalization; orbital GM",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_1_PiM_worldtube",
            "channel": "PiM/source-worldtube chain-map",
            "residual_symbol": "I_commutator_abs_over_MHref",
            "symbolic_bound": "||[d,Pi_W]J_H||*/M_H_ref + ||(delta Pi_W)J_H||*/M_H_ref + |Delta_support|/M_H_ref",
            "needed_numeric_inputs": "chain-map defect norm; source current norm; support/readout motion norm; M_H_ref",
            "test_arenas": "Newtonian source calibration; PPN gamma/beta; orbital GM consistency",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_2_GammaKhat_q_loc",
            "channel": "Gamma/Khat/q_loc",
            "residual_symbol": "epsilon_q_loc_TGK_mass",
            "symbolic_bound": "C_GK ||P_loc div T_GK||* / M_H_ref + C_beta ||beta_qloc|| + C_boundary |Phi_GK|/M_H_ref",
            "needed_numeric_inputs": "T_GK action owner or residual norm; beta_qloc map; local projection norm; boundary flux",
            "test_arenas": "PPN beta/gamma/alpha; fifth-force/R10; local source conservation",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_3_response_memory",
            "channel": "response/memory doublet",
            "residual_symbol": "epsilon_memory_kernel_abs",
            "symbolic_bound": "C_mem lambda_mem^-1 (||J_mem||* + ||history_injection||* + |Phi_mem|)",
            "needed_numeric_inputs": "positive kernel gap; source/history norms; response-to-Hilbert-mass map",
            "test_arenas": "Gdot/clocks; cosmological memory split; PPN preferred-frame leakage",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_4_boundary_symplectic",
            "channel": "boundary/reference/symplectic flux",
            "residual_symbol": "epsilon_boundary_symplectic_abs",
            "symbolic_bound": "(|B_zero| + |Delta_symp| + |Delta_H_ref| + |Phi_boundary|)/M_H_ref",
            "needed_numeric_inputs": "boundary flux; symplectic reference shift; same-frame M_H_ref; linking surface normalization",
            "test_arenas": "orbital GM; clocks/Gdot; local conservation",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_5_readout_reentry",
            "channel": "metric/readout reentry",
            "residual_symbol": "epsilon_readout_reentry_abs",
            "symbolic_bound": "||delta_hidden g_obs||/||g_public|| + |delta_hidden M_ref|/M_H_ref + |delta_cal|",
            "needed_numeric_inputs": "readout derivative; hidden metric coupling; source denominator derivative; calibration residual",
            "test_arenas": "PPN gamma/beta; Newtonian limit; source calibration",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3430_6_total_hidden",
            "channel": "hidden/projector total",
            "residual_symbol": "epsilon_hidden_total_abs",
            "symbolic_bound": "sum(abs(HBR3430_0..HBR3430_5)) with no cancellations unless a parent Ward identity is signed",
            "needed_numeric_inputs": "all channel bounds or zero certificates",
            "test_arenas": "local GR/Newton/PPN/R10/clocks/orbital",
            "status": "ABSOLUTE_SUM_GUARD",
            "valid_for_claim": False,
        },
    ]


def pc3400_4_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_id": "PC3400_4",
            "requirement": "no extra compact-source mass outside public Hilbert matter/EM/Poynting source",
            "new_result": "hidden/projector channels now have a theorem-or-bound decomposition",
            "signed_part": "public Hilbert stress remains safe; gapped/Y6 no-hair theorem exists conditionally; hidden channels are separately named",
            "open_part": "no hidden channel has a parent-signed zero certificate or numeric bound inputs",
            "status": "PARTIAL_NOT_PROMOTED",
            "valid_for_claim": False,
        }
    ]


def nohair_activation_update() -> list[dict[str, Any]]:
    return [
        {
            "activation_id": "NHA3430_0_domain_projector",
            "needed_for_3429": "R_X=0 or bounded projector residual",
            "3430_result": "projector residual decomposed into delta_g Pi, D_D Pi, support motion, and vector/shear leakage",
            "activation_status": "NOT_ZERO_BOUND_ROW_READY",
            "valid_for_claim": False,
        },
        {
            "activation_id": "NHA3430_1_source_current",
            "needed_for_3429": "J_X=0 or bounded source current",
            "3430_result": "source-worldtube chain-map and q-vertical descent are exact conditional routes but not parent signed",
            "activation_status": "NOT_ZERO_BOUND_ROW_READY",
            "valid_for_claim": False,
        },
        {
            "activation_id": "NHA3430_2_boundary",
            "needed_for_3429": "B_X=0 or bounded boundary flux",
            "3430_result": "identity/Hilbert branch is cleaner, but residual hidden/projector boundary flux remains possible",
            "activation_status": "NOT_ZERO_BOUND_ROW_READY",
            "valid_for_claim": False,
        },
        {
            "activation_id": "NHA3430_3_total",
            "needed_for_3429": "lambda_X plus J/B/R zero or numeric values",
            "3430_result": "3429 cannot activate globally until channel bounds or zero certificates fill HBR3430_0..5",
            "activation_status": "NOHAIR_STILL_CONDITIONAL",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3430_0_channel_decomposition",
            "gate": "all hidden/projector channels are decomposed",
            "result": "PASS_ACCOUNTING",
            "evidence": "HCD3430_0 through HCD3430_6",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3430_1_zero_certificates",
            "gate": "every hidden/projector channel has a parent-signed zero theorem",
            "result": "FAIL_CURRENT",
            "evidence": "CHA3430 rows retain unsigned parent/projector/readout/source inputs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3430_2_bound_contracts",
            "gate": "every nonzero channel has a symbolic bound row",
            "result": "PASS_SYMBOLIC_VALUES_MISSING",
            "evidence": "HBR3430_0 through HBR3430_6",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3430_3_no_cancellation",
            "gate": "hidden total uses absolute sum, not tuned cancellation",
            "result": "PASS_GUARD",
            "evidence": "CEX3430_0 and HBR3430_6",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3430_4_PC3400_4",
            "gate": "no-extra-mass PC3400_4 is signed",
            "result": "BLOCKED_PARTIAL",
            "evidence": "hidden/projector channels are not zero/bounded numerically",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3430_5_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "result": "BLOCKED",
            "evidence": "PC3400_4, M_H_ref/tau, and second-order PPN remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3430_0_not_magic",
            "decision": "Do not declare hidden/projector silence from covariance alone.",
            "reason": "Bianchi conservation allows conserved extra stress; it does not prove zero stress or zero monopole.",
            "action": "require channel zero certificate or absolute bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3430_1_best_route",
            "decision": "The least-scrutiny route is fixed/topological projector or identity-Hilbert projector, not a fitted plateau.",
            "reason": "it removes delta Pi and commutator stress before PPN scoring",
            "action": "next derive domain/projector no-stress theorem or operator bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3430_2_bound_route",
            "decision": "If no projector zero proof closes, the branch still moves forward as a residual vector.",
            "reason": "every channel now has a symbolic residual slot and test arena",
            "action": "fill coefficients or demote local-GR claim to bounded nonclaim",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3431_domain_projector_no_stress_theorem_or_operator_bound.py",
            "objective": "attack the hardest highest-leverage hidden channel: prove fixed/topological/scalar domain projector has zero stress, or produce an operator norm bound for delta_g Pi and D_D Pi",
            "success_condition": "either HCD3430_0 becomes zero-certified or HBR3430_0 gets source-backed inputs ready for PPN/R10 scoring",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3430_0",
            "purpose": "prevent accidental promotion",
            "rule": "local GR remains false unless all hidden channels have zero certificates or numeric absolute bounds below tests",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3430_1",
            "purpose": "no cancellation discipline",
            "rule": "epsilon_hidden_total_abs is an absolute sum unless a parent Ward identity signs exact cancellation",
            "current_value": "absolute_sum_guard=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    # This stays conservative: only count filesystem timestamps later than this script file.
    # It should remain zero because this generator only writes post-checkpoint-work outputs.
    script_time = Path(__file__).stat().st_mtime
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= script_time)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    channel_rows = rows_by_name["hidden_channel_decomposition"]
    theorem_rows = rows_by_name["exclusion_theorem"]
    audit_rows = rows_by_name["channel_audit"]
    bound_rows = rows_by_name["residual_bound_rows"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3430_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3430_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3430_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3430_3_channel_coverage",
            "condition": "major hidden/projector channels are covered",
            "passed": len(channel_rows) >= 7 and any(row["channel_id"] == "HCD3430_6_total_hidden" for row in channel_rows),
            "detail": f"{len(channel_rows)} channel rows",
        },
        {
            "check_id": "VAL3430_4_zero_theorem_routes",
            "condition": "proof routes are explicit, not merely missing-input ledger",
            "passed": len(theorem_rows) >= 8 and any(row["theorem_id"] == "CEX3430_7_bound_if_not_zero" for row in theorem_rows),
            "detail": "public/topological/chainmap/vertical/nohair/symmetry/bound routes present",
        },
        {
            "check_id": "VAL3430_5_no_silent_promotion",
            "condition": "each audited channel is either unsigned or bound-staged, not promoted",
            "passed": all(str(row["valid_for_claim"]).lower() == "false" for row in audit_rows),
            "detail": "channel audit stays nonclaim",
        },
        {
            "check_id": "VAL3430_6_bound_rows",
            "condition": "each nonzero hidden channel has a residual bound row",
            "passed": len(bound_rows) >= 7 and any(row["bound_id"] == "HBR3430_6_total_hidden" for row in bound_rows),
            "detail": f"{len(bound_rows)} bound rows",
        },
        {
            "check_id": "VAL3430_7_local_GR_blocked",
            "condition": "local GR remains blocked until hidden channels close",
            "passed": any(row["gate_id"] == "PG3430_5_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3430_8_next_target",
            "condition": "next target attacks a concrete channel, not another broad sweep",
            "passed": next_rows[0]["target_doc"].startswith("3431-Y5-R2FR-domain-projector"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3430_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3430_10_overall",
            "condition": "3430 hidden/projector checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3430 - Hidden/Projector Channelwise Bound or Exclusion

## Summary
- This checkpoint attacks the hidden/projector sector directly instead of merely saying it is missing.
- The result is a channel theorem: every hidden channel must be absorbed into public Hilbert stress, fixed/topological with no stress, a fixed chain-map, vertical quotient-silent, positive-operator silent, symmetry-invisible for vector/STF leakage, or explicitly bounded.
- No hidden cancellation is allowed. The total hidden residual is an absolute sum unless a parent Ward identity signs exact cancellation.
- Current MTS still does not get a local-GR claim, but the obstruction is now a finite channel list with proof routes and bound formulas.
- The next best target is the domain/projector no-stress theorem, because it is the highest-leverage hidden channel.

## Source Register
{md_table(rows_by_name["source_register"])}

## Hidden Channel Decomposition
{md_table(rows_by_name["hidden_channel_decomposition"])}

## Channel Exclusion Theorem
{md_table(rows_by_name["exclusion_theorem"])}

## Channelwise Exclusion Audit
{md_table(rows_by_name["channel_audit"])}

## Hidden Projector Bound Rows
{md_table(rows_by_name["residual_bound_rows"])}

## PC3400_4 Update
{md_table(rows_by_name["pc3400_4_update"])}

## Nohair Activation Update
{md_table(rows_by_name["nohair_activation_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This moves the work forward in the way we wanted: hidden/projector is no longer a fog-bank. It is now a finite opponent list. The local-GR route wins only by proving or bounding each opponent, with the domain/projector stress channel first in the queue.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "hidden_channel_decomposition": hidden_channel_decomposition(),
        "exclusion_theorem": exclusion_theorem(),
        "channel_audit": channel_audit(),
        "residual_bound_rows": residual_bound_rows(),
        "pc3400_4_update": pc3400_4_update(),
        "nohair_activation_update": nohair_activation_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3430 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
