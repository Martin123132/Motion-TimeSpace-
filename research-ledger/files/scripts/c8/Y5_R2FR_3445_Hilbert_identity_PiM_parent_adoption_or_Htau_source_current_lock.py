from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3444": ROOT / "3444-Y5-R2FR-PiM-JH-commutator-zero-or-Icommutator-bound-input-under-AX1090.md",
    "next_3444": OUT / "P8_Y5_R2FR_3444_NEXT_TARGET.csv",
    "commutator_3444": OUT / "P8_Y5_R2FR_3444_COMMUTATOR_ZERO_THEOREM_ATTEMPT.csv",
    "branch_3444": OUT / "P8_Y5_R2FR_3444_PIM_BRANCH_SELECTION_GATE.csv",
    "signature_3444": OUT / "P8_Y5_R2FR_3444_CHAIN_MAP_SIGNATURE_AUDIT.csv",
    "csrc_update_3444": OUT / "P8_Y5_R2FR_3444_CSRC_FLUX_UPDATE.csv",
    "doc_3424": ROOT / "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
    "parent_density_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
    "variation_chain_3424": OUT / "P8_Y5_R2FR_3424_VARIATION_AND_NEWTON_CHAIN.csv",
    "pc3400_audit_3424": OUT / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
    "retained_rows_3424": OUT / "P8_Y5_R2FR_3424_RETAINED_SOURCE_BOUND_ROWS.csv",
    "doc_3426": ROOT / "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md",
    "chain_map_3426": OUT / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
    "branch_split_3426": OUT / "P8_Y5_R2FR_3426_PIM_BRANCH_SPLIT.csv",
    "topological_demoter_3426": OUT / "P8_Y5_R2FR_3426_TOPOLOGICAL_PIM_DEMOTER.csv",
    "parent_hilbert_clause_3340": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
    "hilbert_theorem_3340": OUT / "P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv",
    "hilbert_transfer_3372": OUT / "P8_Y5_R2FR_3372_HILBERT_SOURCE_TRANSFER_THEOREM_ATTEMPT.csv",
    "jh_derivation_3408": OUT / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv",
    "hilbert_current_contract_2586": OUT / "P8_Y5_SOURCE_COMPLEX_2586_HILBERT_CURRENT_CONTRACT.csv",
    "htau_certificate_2445": OUT / "P8_Y5_PARENT_QLOC_2445_HTAU_SOURCE_CHARGE_CERTIFICATE_AUDIT.csv",
    "htau_mhref_1732": OUT / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
    "htau_worldtube_2938": OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "htau_extraction_3006": OUT / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "htau_curl_3208": OUT / "P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv",
    "projector_stress_contract": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "projector_algebra_contract": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "pim_input_template": OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3445_SOURCE_REGISTER.csv",
    "parent_adoption_contract": OUT / "P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv",
    "typed_source_complex": OUT / "P8_Y5_R2FR_3445_TYPED_SOURCE_COMPLEX.csv",
    "commutator_reduction": OUT / "P8_Y5_R2FR_3445_COMMUTATOR_REDUCTION.csv",
    "htau_source_current_lock": OUT / "P8_Y5_R2FR_3445_HTAU_SOURCE_CURRENT_LOCK_AUDIT.csv",
    "pc3400_update": OUT / "P8_Y5_R2FR_3445_PC3400_3_UPDATE.csv",
    "residual_vector": OUT / "P8_Y5_R2FR_3445_RESIDUAL_VECTOR_AFTER_PIMH_ADOPTION.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3445_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3445_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3445_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3445_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3445_VALIDATION.csv",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    lines.extend("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows)
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3444": "immediate handoff from commutator route",
        "next_3444": "machine-readable 3445 target",
        "commutator_3444": "Hilbert identity commutator zero theorem",
        "branch_3444": "preferred branch selection",
        "signature_3444": "parent adoption clauses to sign",
        "csrc_update_3444": "C_src obstruction after commutator route",
        "doc_3424": "minimal source-coupling parent action checkpoint",
        "parent_density_3424": "candidate local parent action density",
        "variation_chain_3424": "metric variation and Newton chain",
        "pc3400_audit_3424": "PC3400 adoption status before PiMH split",
        "retained_rows_3424": "source-bound rows from the parent action checkpoint",
        "doc_3426": "PiM chain-map identity checkpoint",
        "chain_map_3426": "identity/inclusion theorem row",
        "branch_split_3426": "Hilbert identity branch selection",
        "topological_demoter_3426": "old topological PiM demotion",
        "parent_hilbert_clause_3340": "parent Hilbert source clause",
        "hilbert_theorem_3340": "conditional Hilbert source theorem",
        "hilbert_transfer_3372": "Hilbert transfer to source charge",
        "jh_derivation_3408": "Hilbert stress derivation from matter+EM variation",
        "hilbert_current_contract_2586": "Hilbert current source complex contract",
        "htau_certificate_2445": "H_tau certificate blockers",
        "htau_mhref_1732": "M_H_ref and PiM/H chain-map source rows",
        "htau_worldtube_2938": "Hamiltonian/worldtube source-measure theorem attempt",
        "htau_extraction_3006": "theta/Q_tau/H_tau extraction rows",
        "htau_curl_3208": "Hamiltonian one-form curl law",
        "projector_stress_contract": "stress retention for non-identity projectors",
        "projector_algebra_contract": "projector algebra guardrail",
        "pim_input_template": "fallback source-bound input template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCES.items()
    ]


def parent_adoption_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PAC3445_0_parent_action_branch",
            "object": "local parent branch data",
            "required_form": "S_loc=S_EH[g_obs;G_ref]+S_matter[e_obs,psi]+S_EM[g_obs,A;lambda_0]+S_Z+S_boundary, with branch data fixed before readout",
            "derives": "one public Hilbert stress and one ordinary source slot before measured-GM comparison",
            "current_status": "CAN_BE_ADOPTED_AS_BRANCH_CONTRACT_FROM_3424_3340",
            "remaining_risk": "parent action still candidate/private, not a public theorem of the full corpus",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC3445_1_define_CHM",
            "object": "Hilbert mass-current subcomplex",
            "required_form": "C_H^M(A_ext):={J_H^M[T_total,tau] on the compact exterior/source collar, with ordinary matter+EM stress from g_obs variation}",
            "derives": "the current acted on by Pi_M^H is the same Hilbert source object used by the public metric equation",
            "current_status": "DEFINITION_ADOPTED_FOR_PREFERRED_BRANCH",
            "remaining_risk": "tau, source collar and exterior on-shell domain still need H_tau/worldtube lock",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC3445_2_define_PiMH",
            "object": "Hilbert identity mass map",
            "required_form": "Pi_M^H := id_{C_H^M} or canonical inclusion/readout of the typed Hilbert mass-current slot; no Hodge, Green, DeWitt, metric-domain or post-fit orbital projector",
            "derives": "delta_g Pi_M^H=0 as an independent operator and [d,Pi_M^H]J_H^M=0",
            "current_status": "PARENT_BRANCH_ADOPTED_CONDITIONALLY_IN_3445",
            "remaining_risk": "this is a branch choice; old topological PiM and non-Hilbert channels must remain demoted/bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC3445_3_split_extra_channels",
            "object": "non-Hilbert residual split",
            "required_form": "J_total=J_H^M+J_extra, with J_extra covering hidden/domain/memory/boundary/projector/Y6/coupling/frame channels",
            "derives": "commutator zero cannot absorb extra source exchange into measured GM",
            "current_status": "RETAINED_AS_EXPLICIT_RESIDUAL_SPLIT",
            "remaining_risk": "Pi_M^H dJ_extra, anomaly, coupling and calibration tails remain the next live source-normalization problem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC3445_4_forbid_old_independent_topology",
            "object": "old topological PiM demotion",
            "required_form": "independent J_M_top is not used in the preferred local source branch unless Pi_M^top J_H=Pi_M^H J_H+dB_zero with R_eq=0 and zero boundary flux",
            "derives": "removes the conserved-wrong-object problem from the preferred branch",
            "current_status": "DEMOTED_FROM_PREFERRED_BRANCH",
            "remaining_risk": "if old topological labels are reintroduced, R_eq/B_zero/I_commutator rows immediately reactivate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def typed_source_complex() -> list[dict[str, Any]]:
    return [
        {
            "complex_id": "TSC3445_0_total_source",
            "object": "J_total",
            "definition": "full local source/current ledger entering MTS source-normalization analysis",
            "allowed_content": "J_H^M plus explicitly typed residual channels",
            "forbidden_shortcut": "calling J_total Hilbert after hidden or boundary exchange has been silently included",
            "status": "TYPED_SUM_NOT_SINGLE_UNOWNED_CURRENT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "complex_id": "TSC3445_1_mass_branch",
            "object": "J_H^M",
            "definition": "ordinary matter+EM Hilbert source current derived from variation of S_matter+S_EM with respect to g_obs/e_obs and contracted with tau when a mass current is needed",
            "allowed_content": "rest-mass, kinetic, pressure, stress, static EM, radiative EM/Poynting as Hilbert T_total contributions",
            "forbidden_shortcut": "species-only gravitational weights or separate EM/Poynting source owner",
            "status": "PREFERRED_SOURCE_COMPLEX_FOR_PiMH",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "complex_id": "TSC3445_2_extra_branch",
            "object": "J_extra",
            "definition": "all non-Hilbert, residual, hidden, boundary, domain, memory, projector, Y6 or coupling exchange channels",
            "allowed_content": "only as retained residuals with zero theorem or source-bound rows",
            "forbidden_shortcut": "folding J_extra into M_H_ref or measured GM calibration",
            "status": "RETAINED_RESIDUAL_BRANCH",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "complex_id": "TSC3445_3_PiMH_action",
            "object": "Pi_M^H",
            "definition": "identity/inclusion on TSC3445_1; not a projector chosen from observations",
            "allowed_content": "typed branch map fixed with the parent source action",
            "forbidden_shortcut": "Hodge/Green/orthogonal/domain projector unless its stress is retained",
            "status": "ADOPTED_FOR_CONDITIONAL_BRANCH",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def commutator_reduction() -> list[dict[str, Any]]:
    return [
        {
            "reduction_id": "CR3445_0_mass_branch_identity",
            "quantity": "[d,Pi_M^H]J_H^M",
            "derivation": "Pi_M^H J=J and Pi_M^H(dJ)=dJ on C_H^M(A_ext), so d(Pi_M^H J)-Pi_M^H(dJ)=dJ-dJ=0",
            "result": "THEOREM_ZERO_IN_ADOPTED_BRANCH",
            "remaining_condition": "J_H^M must stay in the same typed Hilbert mass-current complex and branch domain",
            "removed_from_obstruction": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reduction_id": "CR3445_1_no_independent_projector_stress",
            "quantity": "delta_g Pi_M^H",
            "derivation": "identity/inclusion has no separate metric-dependent kernel, Hodge representative, Green operator, normal selector or DeWitt inner product",
            "result": "NO_INDEPENDENT_PROJECTOR_STRESS_IN_IDENTITY_BRANCH",
            "remaining_condition": "all metric variation remains in T_total and the field equations, not in Pi_M^H",
            "removed_from_obstruction": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reduction_id": "CR3445_2_extra_projection_retained",
            "quantity": "-Pi_M^H dJ_extra",
            "derivation": "The typed identity proof is deliberately not applied to residual channels outside C_H^M(A_ext)",
            "result": "RETAINED_AS_EXPLICIT_SOURCE_EXCHANGE",
            "remaining_condition": "derive J_extra=0/projection-zero or source-bound it",
            "removed_from_obstruction": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reduction_id": "CR3445_3_old_topology_retained_if_reintroduced",
            "quantity": "R_eq+B_zero_flux+I_commutator^top",
            "derivation": "Old independent topological PiM is outside the preferred branch and cannot inherit the Hilbert identity proof",
            "result": "DROPPED_FROM_PREFERRED_BRANCH_RETAINED_IF_USED",
            "remaining_condition": "prove same-object equality before using old topological route",
            "removed_from_obstruction": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def htau_source_current_lock() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "HTL3445_0_Htau_one_form",
            "required_lock": "Hamiltonian one-form alpha_tau exists on the same branch",
            "mathematical_form": "alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref",
            "current_status": "FORMAL_IDENTITY_AVAILABLE_PARENT_THETA_QTAU_MISSING",
            "effect_if_closed": "H_tau can define M_H_ref without orbital-GM input",
            "if_open": "epsilon_Htau_curl and M_H_ref rows remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "HTL3445_1_integrability",
            "required_lock": "d_F alpha_tau=0 on allowed local branch",
            "mathematical_form": "d_F alpha_tau=-int_S i_tau omega_MTS + C_tau+C_S+C_ref=0",
            "current_status": "NOT_CLOSED_USE_3208_CURL_BOUND_ROUTE",
            "effect_if_closed": "H_tau is path-independent and can be a source denominator",
            "if_open": "Delta_H_curl_bound feeds source-normalization residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "HTL3445_2_reference_lock",
            "required_lock": "H_ref fixed before readout and source-blind",
            "mathematical_form": "D_source H_ref=0 with no GM_obs, source radius, composition or orbit label",
            "current_status": "OPEN_REFERENCE_CAN_ABSORB_SOURCE_NORMALIZATION",
            "effect_if_closed": "prevents calibration from hiding C_src",
            "if_open": "Delta_ref/source-normalization residual remains",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "HTL3445_3_same_tau_frame",
            "required_lock": "same tau_obs and e_obs are used by source, clock, orbit, PPN and R10 comparisons",
            "mathematical_form": "J_H^M[T_total,tau_obs], H_tau[tau_obs], orbital readout and local metric branch share one denominator convention",
            "current_status": "OPEN_TAU_FRAME_DENOMINATOR_CERTIFICATE_MISSING",
            "effect_if_closed": "source charge and observational GM live in the same frame",
            "if_open": "frame/calibration residual remains",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lock_id": "HTL3445_4_verdict",
            "required_lock": "H_tau-H_ref equals the Hilbert mass-current denominator generated by Pi_M^H",
            "mathematical_form": "M_H_ref = H_tau[S]-H_ref = int_W J_H^M + retained residuals, before orbital fitting",
            "current_status": "NOT_LOCKED_AFTER_3445",
            "effect_if_closed": "PC3400_3 could be fully signed",
            "if_open": "3446 must attack H_tau exactness/reference/M_H_ref instead of revisiting PiM commutator",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pc3400_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "PCU3445_0_PC3400_3_split",
            "pc_clause": "PC3400_3_Htau_PiM_chain",
            "before": "PARTIAL_NOT_SIGNED: H_tau and M_H named, integrability/H_ref/PiM chain-map equality unproved",
            "after": "PiM chain-map commutator component signed inside the preferred Hilbert-identity branch; H_tau/MHref/reference/source-current lock remains unsigned",
            "delta": "removes I_commutator^H from the preferred mass branch but does not close M_H_ref",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "PCU3445_1_RSB3424_0",
            "pc_clause": "RSB3424_0_epsilon_HPiM_Z",
            "before": "|partial_Z ln(M_H/(Pi_M J_H))| + |I_commutator|/M_H_ref",
            "after": "|partial_Z ln(M_H/(J_H^M))| + epsilon_Htau_curl + epsilon_ref + epsilon_tau_frame, with I_commutator^H=0 only in PiMH branch",
            "delta": "turns one symbolic PiM gap into concrete H_tau/reference/source-current locks",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "PCU3445_2_Newton_status",
            "pc_clause": "Newton first-order source transfer",
            "before": "blocked by H_tau/PiM/reference/no-extra-mass and v-fork",
            "after": "PiM commutator obstruction reduced; Newton still blocked by H_tau denominator, extra monopole/source exchange, coupling calibration and second-order PPN",
            "delta": "real progress, not local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_vector() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RV3445_0_Omega_GM_H",
            "symbol": "Omega_GM^H",
            "definition": "-Pi_M^H dJ_extra + A_parent + Delta_coupling + Delta_cal + Delta_PPN + epsilon_Htau_curl + epsilon_ref + epsilon_tau_frame",
            "status_after_3445": "PREFERRED_BRANCH_RESIDUAL_VECTOR",
            "zero_route": "derive every term zero from parent action, H_tau exactness, reference lock, source-current descent and local weak-field readout",
            "bound_route": "source-backed absolute no-cancellation bounds for each component",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RV3445_1_extra_current_projection",
            "symbol": "-Pi_M^H dJ_extra",
            "definition": "projection of non-Hilbert/source-exchange channels onto the Hilbert mass slot",
            "status_after_3445": "LIVE_NEXT_SOURCE_EXCHANGE_TERM",
            "zero_route": "prove no hidden/domain/memory/boundary/Y6/coupling source exchange in local branch",
            "bound_route": "finite source-current residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RV3445_2_Htau_denominator",
            "symbol": "epsilon_Htau_curl+epsilon_ref+epsilon_tau_frame",
            "definition": "failure of H_tau-H_ref to be a positive same-frame source denominator",
            "status_after_3445": "PRIMARY_NEXT_TARGET",
            "zero_route": "Theta/Q_tau extraction, integrability, fixed H_ref and same tau_obs certificate",
            "bound_route": "field-space curl/reference/frame denominator bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "RV3445_3_coupling_calibration",
            "symbol": "Delta_coupling+Delta_cal+Delta_PPN",
            "definition": "constant G/kappa calibration and weak-field/PPN readout residuals after source current is defined",
            "status_after_3445": "LIVE_DOWNSTREAM",
            "zero_route": "constant kappa, metric-potential v fork, Poisson/Gauss bridge and PPN second-order source-square law",
            "bound_route": "PPN/Gdot/R10/orbital residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3445_0_sources",
            "claim": "all 3445 cited source paths exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3445_1_parent_branch_adoption",
            "claim": "Pi_M^H is adopted as the preferred branch contract",
            "gate_pass": True,
            "reason": "3445 defines Pi_M^H as identity/inclusion on the typed Hilbert mass-current subcomplex and demotes old topological/Hodge branches",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3445_2_commutator_removed",
            "claim": "I_commutator^H is removed from the preferred mass branch",
            "gate_pass": True,
            "reason": "d(Pi_M^H J_H^M)-Pi_M^H dJ_H^M=0 by identity map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3445_3_Htau_lock",
            "claim": "H_tau-H_ref is locked to J_H^M as a positive same-frame source denominator",
            "gate_pass": False,
            "reason": "Theta/Q_tau extraction, integrability, H_ref and tau/frame certificate remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3445_4_extra_current_zero",
            "claim": "non-Hilbert source-exchange projection is zero",
            "gate_pass": False,
            "reason": "J_extra split is explicit but not theorem-zero or source-bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3445_5_local_GR_Newton",
            "claim": "local GR/Newton/source coupling can be publicly promoted",
            "gate_pass": False,
            "reason": "PiM commutator improved, but H_tau denominator, extra source exchange, coupling calibration and PPN residuals remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3445_0_adopt_PiMH",
            "decision": "Adopt Pi_M^H as the preferred branch contract, not as a measured-GM fit.",
            "because": "the identity/inclusion map is the only clean way to kill the commutator without a hidden Hodge/domain/readout projector",
            "next_action": "do not revisit generic PiM commutator unless the preferred branch is abandoned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3445_1_Htau_next",
            "decision": "Move the fight from PiM commutator to H_tau exactness and source denominator ownership.",
            "because": "PC3400_3 is now split: the PiM chain-map part is clean in the preferred branch, while M_H_ref/H_ref/tau remain the live obstruction",
            "next_action": "derive H_tau one-form exactness or stage a denominator curl/reference bound row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3445_2_EM_Poynting",
            "decision": "Keep EM/Poynting inside the Hilbert source if Maxwell uses public g_obs and constant lambda_0.",
            "because": "Poynting is an observer decomposition of T_EM, not a second source owner, but public Maxwell/Hodge still needs parent signature",
            "next_action": "when EM returns, audit public Maxwell/Hodge normalization rather than inventing a separate EM gravity coupling",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3446-Y5-R2FR-Htau-exact-one-form-reference-lock-or-MHref-denominator-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3446_Htau_exact_one_form_reference_lock_or_MHref_denominator_bound.py",
            "objective": "derive H_tau-H_ref as a positive same-frame Hilbert source denominator for the adopted Pi_M^H branch, using the one-form curl law, fixed reference selector and tau/frame lock; otherwise stage nonclaim M_H_ref, epsilon_Htau_curl, epsilon_ref and epsilon_tau_frame bound rows",
            "success_condition": "H_tau exactness/reference/tau lock is parent-signed for J_H^M before orbital fitting, or the denominator residual vector is schema-ready and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3445_0_PiMH_commutator",
            "branch": "Hilbert_identity_PiM",
            "I_commutator_H": "0_by_identity_branch_contract",
            "Htau_locked": False,
            "extra_current_zero": False,
            "score_ready": False,
            "result": "COMMUTATOR_ADVANCED_DENOMINATOR_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN3445_1_old_PiM",
            "branch": "old_topological_or_Hodge_PiM",
            "I_commutator_H": "not_applicable",
            "Htau_locked": False,
            "extra_current_zero": False,
            "score_ready": False,
            "result": "DEMOTED_TO_BOUND_OR_CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    generated_csv_rows_parse = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        if path.exists():
            try:
                read_csv(path)
            except csv.Error:
                generated_csv_rows_parse = False

    validations = [
        {
            "check_id": "VAL3445_0_sources_exist",
            "condition": "all cited 3445 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3445_1_PiMH_adopted",
            "condition": "Pi_M^H identity/inclusion is adopted as preferred branch contract",
            "passed": any(
                row["contract_id"] == "PAC3445_2_define_PiMH"
                and row["current_status"] == "PARENT_BRANCH_ADOPTED_CONDITIONALLY_IN_3445"
                for row in rows_by_name["parent_adoption_contract"]
            ),
            "detail": "preferred Hilbert identity branch written",
        },
        {
            "check_id": "VAL3445_2_commutator_removed_mass_branch",
            "condition": "I_commutator^H is theorem-zero in adopted branch",
            "passed": any(
                row["reduction_id"] == "CR3445_0_mass_branch_identity"
                and row["result"] == "THEOREM_ZERO_IN_ADOPTED_BRANCH"
                for row in rows_by_name["commutator_reduction"]
            ),
            "detail": "commutator no longer live in preferred mass branch",
        },
        {
            "check_id": "VAL3445_3_extra_current_retained",
            "condition": "extra source exchange is retained, not hidden in the identity proof",
            "passed": any(
                row["residual_id"] == "RV3445_1_extra_current_projection"
                and row["status_after_3445"] == "LIVE_NEXT_SOURCE_EXCHANGE_TERM"
                for row in rows_by_name["residual_vector"]
            ),
            "detail": "J_extra projection remains explicit",
        },
        {
            "check_id": "VAL3445_4_Htau_not_promoted",
            "condition": "H_tau denominator/source-current lock is not falsely promoted",
            "passed": any(
                row["lock_id"] == "HTL3445_4_verdict"
                and row["current_status"] == "NOT_LOCKED_AFTER_3445"
                for row in rows_by_name["htau_source_current_lock"]
            ),
            "detail": "H_tau exactness/reference/tau remain next target",
        },
        {
            "check_id": "VAL3445_5_PC3400_split",
            "condition": "PC3400_3 is split into solved PiM component and unsolved H_tau component",
            "passed": any(
                row["update_id"] == "PCU3445_0_PC3400_3_split"
                and "PiM chain-map commutator component signed" in row["after"]
                for row in rows_by_name["pc3400_update"]
            ),
            "detail": "PC3400_3 update written",
        },
        {
            "check_id": "VAL3445_6_old_topology_demoted",
            "condition": "old independent topological PiM remains demoted unless same-object proof exists",
            "passed": any(
                row["contract_id"] == "PAC3445_4_forbid_old_independent_topology"
                and row["current_status"] == "DEMOTED_FROM_PREFERRED_BRANCH"
                for row in rows_by_name["parent_adoption_contract"]
            ),
            "detail": "conserved-wrong-object guard remains active",
        },
        {
            "check_id": "VAL3445_7_next_target_Htau",
            "condition": "next target attacks H_tau exactness/reference lock",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3446-Y5-R2FR-Htau-exact-one-form-reference-lock"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3445_8_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": generated_csv_rows_parse,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3445_9_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3445_10_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3445_11_overall",
            "condition": "3445 Hilbert identity PiM adoption checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3445 - Hilbert Identity PiM Parent Adoption or Htau Source-Current Lock

## Summary
- This checkpoint takes the forward route opened in 3444: stop trying to rescue a generic `Pi_M`, and adopt the preferred local branch `Pi_M^H`.
- `Pi_M^H` is the identity/inclusion on the typed public Hilbert mass-current subcomplex `C_H^M(A_ext)`.
- Therefore `[d,Pi_M^H]J_H^M=0` exactly in the adopted branch, and there is no independent projector stress from `Pi_M^H`.
- This does **not** close local GR/Newton yet: `H_tau-H_ref` is not locked to a positive same-frame source denominator, and `J_extra`, coupling, reference and calibration tails stay live.
- Old independent topological `Pi_M` is not part of the preferred branch unless it proves same-object equality to the Hilbert source current.

## Source Register
{md_table(rows_by_name["source_register"])}

## Parent Adoption Contract
{md_table(rows_by_name["parent_adoption_contract"])}

## Typed Source Complex
{md_table(rows_by_name["typed_source_complex"])}

## Commutator Reduction
{md_table(rows_by_name["commutator_reduction"])}

## Htau Source-Current Lock Audit
{md_table(rows_by_name["htau_source_current_lock"])}

## PC3400.3 Update
{md_table(rows_by_name["pc3400_update"])}

## Residual Vector After PiMH Adoption
{md_table(rows_by_name["residual_vector"])}

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
This is the right kind of progress: the preferred branch now has a clean parent-style object, `Pi_M^H`, where the commutator dies by identity rather than wishful closure. The fight moves upstream to `H_tau`: we need a real source denominator, fixed reference, and same `tau`/frame lock before Newton or local GR can be claimed. In boxing terms, the footwork improved; we still have to land the source-denominator shot.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "parent_adoption_contract": parent_adoption_contract(),
        "typed_source_complex": typed_source_complex(),
        "commutator_reduction": commutator_reduction(),
        "htau_source_current_lock": htau_source_current_lock(),
        "pc3400_update": pc3400_update(),
        "residual_vector": residual_vector(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3445 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
