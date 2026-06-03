from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Ward-Bianchi-exchange-owner-for-Poisson-source"
CHECKPOINT_DOC = "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md"
STATUS = "Ward_Bianchi_exchange_owner_attempt_written_conditional_q_source_identity_but_mu_extra_and_nohair_not_derived_no_local_GR_pass"
CLAIM_CEILING = "Ward_Bianchi_exchange_owner_identity_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "430-Ward-source-residual-zero-route-gate.md"


SOURCE_DOCS = [
    {
        "path": "177-parent-action-perturbation-local-GR-contract.md",
        "role": "parent action and local q_loc silence contract",
    },
    {
        "path": "179-local-GR-PPN-silence-contract.md",
        "role": "q_loc blocker and plateau-axiom warning",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity and explicit projector/boundary/domain force ledger",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force fates and retained PPN residual map",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "Ward closure not sufficient for EH operator selection",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source and measured GM normalization",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "source_residuals and mu_extra in the EH-to-Poisson bridge",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH/source retained ledger and source-normalization channels",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "12-component local residual vector and local-GR pass requirements",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "machine-readable residual components R0-R11",
    },
    {
        "path": "runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv",
        "role": "sourced local-bound rows for residual implications",
    },
]


WARD_IDENTITY_CHAIN = [
    {
        "step": 1,
        "stage": "parent_action",
        "identity": "S_parent[g_obs, Psi_m, X_A, P_D, D, B, lambda_I] is local/covariant in the local branch",
        "status": "contract_not_parent_supplied",
        "meaning": "the Ward identity can only be theorem-level if the parent action exists with all exchange variables included",
    },
    {
        "step": 2,
        "stage": "diffeomorphism_variation",
        "identity": "delta_xi S_parent = integral sqrt(-g) [E_g^{mu nu} L_xi g_munu + sum_A E_A L_xi Z_A] + boundary = 0",
        "status": "structural_Ward_identity",
        "meaning": "diffeomorphism invariance forces every hidden/projector/boundary/domain term into the ledger",
    },
    {
        "step": 3,
        "stage": "integrated_Ward_identity",
        "identity": "2 nabla_mu E_g^{mu nu} = - sum_A E_A nabla^nu Z_A - F_projector^nu - F_boundary^nu - F_domain^nu - F_nonmetric^nu",
        "status": "conditional_identity",
        "meaning": "gravity is conserved only after auxiliary equations and force ledgers are owned",
    },
    {
        "step": 4,
        "stage": "same_frame_field_equation",
        "identity": "E_g^{mu nu} = E_EH^{mu nu} + E_nonEH^{mu nu} - kappa_eff T_obs^{mu nu}",
        "status": "decomposition_contract",
        "meaning": "matter/source conservation is read in the same observed frame; otherwise exchange is frame artefact",
    },
    {
        "step": 5,
        "stage": "Bianchi_projection",
        "identity": "kappa_eff nabla_mu T_obs^{mu nu} = nabla_mu E_nonEH^{mu nu} + T_obs^{mu nu} nabla_mu kappa_eff + sum_A E_A nabla^nu Z_A + F_P^nu + F_B^nu + F_D^nu + F_nm^nu",
        "status": "exchange_owner_identity",
        "meaning": "the local force is not arbitrary; it is exactly the unowned divergence of retained sectors",
    },
    {
        "step": 6,
        "stage": "local_projection",
        "identity": "q_loc^nu = P_loc[nabla_mu T_obs^{mu nu}] = kappa_eff^{-1} P_loc[div E_nonEH + T_obs nabla kappa_eff + E_Z nabla Z + F_P + F_B + F_D + F_nm]",
        "status": "exact_contract",
        "meaning": "q_loc^nu is zero only if the local projection of every exchange-owner term is zero",
    },
    {
        "step": 7,
        "stage": "Poisson_source",
        "identity": "source_residuals = P_Newton[div E_nonEH, delta kappa_eff, hidden stress, boundary/domain flux, fifth-force tail]",
        "status": "not_derived_zero",
        "meaning": "Bianchi ownership controls conservation, but Poisson source purity also needs no-hair/source-normalization",
    },
    {
        "step": 8,
        "stage": "measured_GM",
        "identity": "mu_obs = G_eff M_eff + mu_extra; Ward gives d(mu_total)/dt ownership, not mu_extra=0 by itself",
        "status": "not_derived_zero",
        "meaning": "a conserved hidden contribution can still shift measured GM or create range/species dependence",
    },
]


EXCHANGE_OWNER_CONDITIONS = [
    {
        "condition_id": "C0_same_frame",
        "condition": "all matter clocks/rulers/photons and the gravitational operator use the same observed metric/coframe",
        "needed_for": "R0;R2;R3;R4;R11",
        "current_status": "not_parent_derived",
        "zero_result_if_met": "removes fake frame-exchange terms from q_loc",
        "failure_if_missing": "clock/WEP/gamma/beta residuals can be frame artefacts",
    },
    {
        "condition_id": "C1_auxiliary_on_shell",
        "condition": "every hidden variable Z_A has an Euler equation E_A=0 or an explicit retained residual",
        "needed_for": "R7;R9;R10;R11",
        "current_status": "open",
        "zero_result_if_met": "kills sum_A E_A nabla^nu Z_A in q_loc",
        "failure_if_missing": "unowned local force/source exchange",
    },
    {
        "condition_id": "C2_projector_covariant",
        "condition": "P_D is covariant/dynamical/topological, not a fixed external projector",
        "needed_for": "R5;R6;R7;R8;R11",
        "current_status": "conditional_open",
        "zero_result_if_met": "removes explicit diffeo-breaking projector force",
        "failure_if_missing": "preferred-frame/location and alpha3 flux channels",
    },
    {
        "condition_id": "C3_boundary_nohair",
        "condition": "boundary terms are pure topological/class constants or conserved monopoles with no shear/vector/radial hair",
        "needed_for": "R3;R4;R7;R8;R9",
        "current_status": "not_derived",
        "zero_result_if_met": "local projection of boundary flux vanishes except allowed monopole normalization",
        "failure_if_missing": "gamma/beta/alpha3/xi/Gdot residuals",
    },
    {
        "condition_id": "C4_nonEH_divergence_silent",
        "condition": "non-EH operators are absent, pure boundary, or mapped into a coefficient vector below local locks",
        "needed_for": "R3;R4;R5;R6;R8;R10;R11",
        "current_status": "retained",
        "zero_result_if_met": "div E_nonEH has no local Poisson/PPN effect",
        "failure_if_missing": "Ward-conserved but non-GR exterior",
    },
    {
        "condition_id": "C5_constant_kappa_Geff",
        "condition": "kappa_eff/G_eff is constant, universal, species-independent, and range-independent locally",
        "needed_for": "R1;R4;R9;R10",
        "current_status": "not_derived",
        "zero_result_if_met": "removes T_obs nabla kappa_eff and Gdot/source-normalization drift",
        "failure_if_missing": "Gdot/G, WEP source charge, beta, fifth-force/source range residuals",
    },
    {
        "condition_id": "C6_mu_extra_zero",
        "condition": "hidden/boundary/domain contributions do not enter measured GM except as a fixed universal calibration",
        "needed_for": "R1;R4;R9;R10",
        "current_status": "not_derived",
        "zero_result_if_met": "mu_obs=G_eff M_eff with no species/time/range correction",
        "failure_if_missing": "Poisson algebra can pass while measured Newton source is contaminated",
    },
    {
        "condition_id": "C7_R10_R11_resolved",
        "condition": "alpha(lambda) curve and non-EH coefficient vector are supplied or theorem-zero",
        "needed_for": "R10;R11",
        "current_status": "symbolic_deferred",
        "zero_result_if_met": "symbolic rows become testable or vanish by theorem",
        "failure_if_missing": "no fifth-force/operator pass can be claimed",
    },
]


SOURCE_RESIDUAL_DECOMPOSITION = [
    {
        "term": "delta_kappa_source",
        "symbolic_form": "P_Newton[T_00 delta kappa_eff]",
        "owner_condition": "C5_constant_kappa_Geff",
        "residual_rows": "R1;R4;R9",
        "zero_status": "not_derived",
        "notes": "constant kappa is source normalization, not pure Bianchi",
    },
    {
        "term": "nonEH_divergence",
        "symbolic_form": "P_Newton[nabla_mu E_nonEH^{mu0}]",
        "owner_condition": "C4_nonEH_divergence_silent;C7_R10_R11_resolved",
        "residual_rows": "R3;R4;R10;R11",
        "zero_status": "retained",
        "notes": "a conserved non-EH tensor can still change gamma/beta/fifth-force",
    },
    {
        "term": "auxiliary_offshell_force",
        "symbolic_form": "P_Newton[sum_A E_A nabla^0 Z_A]",
        "owner_condition": "C1_auxiliary_on_shell",
        "residual_rows": "R7;R9;R10",
        "zero_status": "open",
        "notes": "requires actual auxiliary equations, not an inserted plateau",
    },
    {
        "term": "projector_domain_force",
        "symbolic_form": "P_Newton[F_P^0 + F_D^0]",
        "owner_condition": "C2_projector_covariant",
        "residual_rows": "R5;R6;R7;R8",
        "zero_status": "conditional_open",
        "notes": "covariance owns conservation but not automatically no preferred-frame residual",
    },
    {
        "term": "boundary_flux",
        "symbolic_form": "P_Newton[F_B^0]",
        "owner_condition": "C3_boundary_nohair",
        "residual_rows": "R3;R4;R7;R8;R9",
        "zero_status": "not_derived",
        "notes": "monopole-only boundary can be harmless; shear/vector/drift cannot be dropped",
    },
    {
        "term": "nonmetric_matter_exchange",
        "symbolic_form": "P_Newton[F_nm^0]",
        "owner_condition": "C0_same_frame",
        "residual_rows": "R0;R1;R2",
        "zero_status": "not_parent_derived",
        "notes": "universal matter metric/coframe theorem is required",
    },
]


MU_EXTRA_DECOMPOSITION = [
    {
        "mu_channel": "species_source_charge",
        "symbolic_form": "partial_A mu_obs",
        "test_rows": "R1",
        "Ward_result": "total exchange can be conserved",
        "remaining_zero_condition": "species-blind matter/source functor and no material-marker coupling",
        "status": "not_derived",
    },
    {
        "mu_channel": "time_drift",
        "symbolic_form": "d ln(G_eff M_eff)/dt",
        "test_rows": "R9",
        "Ward_result": "total drift must have an owner",
        "remaining_zero_condition": "local kappa and measured mass are stationary",
        "status": "not_derived",
    },
    {
        "mu_channel": "range_dependence",
        "symbolic_form": "partial_lambda mu_obs or alpha(lambda)",
        "test_rows": "R10",
        "Ward_result": "finite-range exchange can be conserved",
        "remaining_zero_condition": "alpha(lambda)=0 by theorem or curve below data",
        "status": "symbolic_deferred",
    },
    {
        "mu_channel": "boundary_monopole_shift",
        "symbolic_form": "delta mu_B",
        "test_rows": "R4;R9",
        "Ward_result": "boundary monopole can be conserved",
        "remaining_zero_condition": "universal fixed calibration, no beta/Gdot leakage",
        "status": "retained",
    },
    {
        "mu_channel": "domain_projector_mass",
        "symbolic_form": "delta mu_D[P_D,D]",
        "test_rows": "R5;R6;R7;R8;R11",
        "Ward_result": "covariant domain stress can be in total ledger",
        "remaining_zero_condition": "no preferred-frame/location or alpha3-equivalent flux",
        "status": "retained",
    },
]


RESIDUAL_VECTOR_IMPLICATIONS = [
    {
        "row_id": "R0_identity_coframe_direct",
        "observable": "eta_WEP_direct_geometry",
        "Ward_effect": "same-frame Ward identity helps only if matter functor is universal",
        "post_429_state": "not_upgraded",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "observable": "eta_WEP_source_charge",
        "Ward_effect": "conserved exchange does not prove species-blind source charge",
        "post_429_state": "retained",
    },
    {
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "Ward_effect": "requires same matter clock frame; Ward total conservation is insufficient",
        "post_429_state": "retained",
    },
    {
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "Ward_effect": "non-EH or boundary shear can be conserved but still alter slip",
        "post_429_state": "retained",
    },
    {
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "Ward_effect": "source_residual and mu_extra zero conditions now explicit",
        "post_429_state": "retained",
    },
    {
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "Ward_effect": "projector/domain covariance must still kill preferred-frame vector terms",
        "post_429_state": "retained",
    },
    {
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "Ward_effect": "same as R5 but tighter lock",
        "post_429_state": "retained",
    },
    {
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "Ward_effect": "main beneficiary: unowned momentum flux now has exact owner identity target",
        "post_429_state": "conditional_route_not_pass",
    },
    {
        "row_id": "R8_xi",
        "observable": "xi",
        "Ward_effect": "domain/boundary anisotropy must be no-hair, not merely conserved",
        "post_429_state": "retained",
    },
    {
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "Ward_effect": "total exchange ownership does not prove local stationary measured GM",
        "post_429_state": "retained",
    },
    {
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "Ward_effect": "finite-range force may be conserved; still needs alpha(lambda) curve or zero theorem",
        "post_429_state": "symbolic_deferred",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "observable": "non_EH_operator_coefficients",
        "Ward_effect": "Ward conservation does not select EH; coefficient vector still required",
        "post_429_state": "symbolic_deferred",
    },
]


COUNTEREXAMPLE_BRANCHES = [
    {
        "counterexample": "conserved_scalar_tensor",
        "how_it_satisfies_Ward": "total scalar plus metric stress is covariantly conserved",
        "why_it_fails_local_GR": "gamma/beta/fifth-force can differ from GR",
        "blocked_by_condition": "C4_nonEH_divergence_silent;C7_R10_R11_resolved",
    },
    {
        "counterexample": "conserved_boundary_monopole_with_drift",
        "how_it_satisfies_Ward": "boundary charge is in the total stress ledger",
        "why_it_fails_local_GR": "measured GM drifts or beta source normalization shifts",
        "blocked_by_condition": "C3_boundary_nohair;C6_mu_extra_zero",
    },
    {
        "counterexample": "covariant_domain_vector",
        "how_it_satisfies_Ward": "domain vector action is diffeomorphism-invariant",
        "why_it_fails_local_GR": "preferred-frame alpha1/alpha2/xi residuals survive",
        "blocked_by_condition": "C2_projector_covariant plus no vector hair",
    },
    {
        "counterexample": "fixed_external_projector",
        "how_it_satisfies_Ward": "it does not; explicit diffeo breaking is hidden if projector is not varied",
        "why_it_fails_local_GR": "fake conservation and fake GR by dropped stress",
        "blocked_by_condition": "forbidden rather than retained",
    },
    {
        "counterexample": "species_dependent_source_charge",
        "how_it_satisfies_Ward": "each species can be conserved in its own coupled sector",
        "why_it_fails_local_GR": "WEP/source-charge row fails",
        "blocked_by_condition": "C0_same_frame;C6_mu_extra_zero",
    },
    {
        "counterexample": "pure_Poisson_with_slip",
        "how_it_satisfies_Ward": "00 equation can reduce to Poisson",
        "why_it_fails_local_GR": "gamma/light bending/PPN spatial curvature still fail",
        "blocked_by_condition": "PPN completion and C4",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "target": "derive Ward exchange-owner identity",
        "result": "conditional_pass",
        "evidence": "Noether/Bianchi chain written with all force channels explicit",
        "claim_allowed": False,
    },
    {
        "target": "derive q_loc^nu=0",
        "result": "conditional_only",
        "evidence": "q_loc^nu=0 follows only if C0-C7 local projections vanish or are retained below locks",
        "claim_allowed": False,
    },
    {
        "target": "derive source_residuals=0",
        "result": "not_derived",
        "evidence": "non-EH divergence, boundary/domain flux, kappa drift, and fifth-force tails remain open",
        "claim_allowed": False,
    },
    {
        "target": "derive mu_extra=0",
        "result": "not_derived",
        "evidence": "conserved hidden stress can still shift measured GM by species/time/range/domain channels",
        "claim_allowed": False,
    },
    {
        "target": "promote local GR/Newton/PPN",
        "result": "fail",
        "evidence": "Ward ownership is necessary but not sufficient for EH operator, source normalization, and PPN completion",
        "claim_allowed": False,
    },
]


DECISION = [
    {
        "decision": "Ward/Bianchi exchange ownership gives a clean conditional identity for q_loc^nu: the local force is exactly the projected divergence of unowned non-EH, auxiliary, projector, boundary, domain, nonmetric, and kappa/source-normalization terms. This is progress because it forbids hand-waving and identifies the zero conditions. It does not yet derive q_loc^nu=0, source_residuals=0, or mu_extra=0 from the current parent corpus, so local GR remains unpromoted.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "q_loc_zero_derived": "conditional_only",
        "source_residuals_zero_derived": "no",
        "mu_extra_zero_derived": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "430-Ward-source-residual-zero-route-gate.md",
        "task": "rank C0-C7 by which zero route is mathematically derivable versus only empirically boundable",
        "priority": "P0",
    },
    {
        "next_file": "430-MTS-local-residual-vector-evaluator.md",
        "task": "build the evaluator for filled MTS residual predictions against local sourced bounds",
        "priority": "P0",
    },
    {
        "next_file": "430-R10-R11-curve-and-operator-vector-contract.md",
        "task": "make alpha(lambda) and non-EH operator-vector rows executable rather than symbolic",
        "priority": "P1",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": path.exists(),
                "role": item["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    claim_rows = [row for row in THEOREM_ATTEMPT_STATUS if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "Ward_identity_chain_written",
            "status": "pass" if len(WARD_IDENTITY_CHAIN) == 8 else "fail",
            "evidence": f"{len(WARD_IDENTITY_CHAIN)} identity steps",
        },
        {
            "gate": "exchange_owner_conditions_written",
            "status": "pass" if len(EXCHANGE_OWNER_CONDITIONS) == 8 else "fail",
            "evidence": f"{len(EXCHANGE_OWNER_CONDITIONS)} zero conditions C0-C7",
        },
        {
            "gate": "source_residual_decomposition_written",
            "status": "pass" if len(SOURCE_RESIDUAL_DECOMPOSITION) == 6 else "fail",
            "evidence": f"{len(SOURCE_RESIDUAL_DECOMPOSITION)} source-residual terms",
        },
        {
            "gate": "mu_extra_decomposition_written",
            "status": "pass" if len(MU_EXTRA_DECOMPOSITION) == 5 else "fail",
            "evidence": f"{len(MU_EXTRA_DECOMPOSITION)} measured-GM channels",
        },
        {
            "gate": "residual_vector_implications_written",
            "status": "pass" if len(RESIDUAL_VECTOR_IMPLICATIONS) == 12 else "fail",
            "evidence": f"{len(RESIDUAL_VECTOR_IMPLICATIONS)} R0-R11 implications",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLE_BRANCHES) == 6 else "fail",
            "evidence": f"{len(COUNTEREXAMPLE_BRANCHES)} Ward-satisfying failure branches",
        },
        {
            "gate": "q_loc_zero_derived",
            "status": "conditional_only",
            "evidence": "requires C0-C7 local zero/retained conditions",
        },
        {
            "gate": "source_residuals_zero_derived",
            "status": "fail",
            "evidence": "non-EH/source-normalization/boundary/domain/fifth-force terms remain open",
        },
        {
            "gate": "mu_extra_zero_derived",
            "status": "fail",
            "evidence": "measured GM source normalization remains unproved",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "Ward identity only; no EH/Newton/PPN/fifth-force pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    source_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    source_table_rows = [
        {"source_file": row["source_file"], "exists": row["exists"], "role": row["role"]}
        for row in source_rows
    ]
    chain_rows = [
        {"step": row["step"], "stage": row["stage"], "status": row["status"], "meaning": row["meaning"]}
        for row in WARD_IDENTITY_CHAIN
    ]
    condition_rows = [
        {
            "condition_id": row["condition_id"],
            "needed_for": row["needed_for"],
            "current_status": row["current_status"],
            "failure_if_missing": row["failure_if_missing"],
        }
        for row in EXCHANGE_OWNER_CONDITIONS
    ]
    source_residual_rows = [
        {
            "term": row["term"],
            "owner_condition": row["owner_condition"],
            "residual_rows": row["residual_rows"],
            "zero_status": row["zero_status"],
        }
        for row in SOURCE_RESIDUAL_DECOMPOSITION
    ]
    mu_rows = [
        {
            "mu_channel": row["mu_channel"],
            "test_rows": row["test_rows"],
            "Ward_result": row["Ward_result"],
            "status": row["status"],
        }
        for row in MU_EXTRA_DECOMPOSITION
    ]
    residual_rows = [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "Ward_effect": row["Ward_effect"],
            "post_429_state": row["post_429_state"],
        }
        for row in RESIDUAL_VECTOR_IMPLICATIONS
    ]
    counter_rows = [
        {
            "counterexample": row["counterexample"],
            "how_it_satisfies_Ward": row["how_it_satisfies_Ward"],
            "why_it_fails_local_GR": row["why_it_fails_local_GR"],
        }
        for row in COUNTEREXAMPLE_BRANCHES
    ]
    status_rows = [
        {
            "target": row["target"],
            "result": row["result"],
            "evidence": row["evidence"],
        }
        for row in THEOREM_ATTEMPT_STATUS
    ]
    gate_table_rows = [
        {"gate": row["gate"], "status": row["status"], "evidence": row["evidence"]}
        for row in gate_result_rows
    ]
    text = f"""# 429 - Ward/Bianchi Exchange Owner For Poisson Source

Private derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 428 defined the local residual vector. This checkpoint attacks the main physics bottleneck: can Ward/Bianchi exchange ownership derive `q_loc^nu=0`, `source_residuals=0`, and `mu_extra=0` rather than smuggling in a local-vacuum plateau?

Short answer: it gives a clean conditional identity, but not yet the full zero theorem. Ward/Bianchi ownership tells us exactly where every local force must live. It does not by itself prove that each owned force vanishes.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Ward_Bianchi_exchange_owner_for_Poisson_source.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_table_rows, ["source_file", "exists", "role"])}

## 4. Ward/Bianchi Identity Chain

{markdown_table(chain_rows, ["step", "stage", "status", "meaning"])}

The central identity is:

```text
q_loc^nu = P_loc[nabla_mu T_obs^(mu nu)]
         = kappa_eff^-1 P_loc[
             div E_nonEH
           + T_obs nabla kappa_eff
           + E_Z nabla Z
           + F_projector + F_boundary + F_domain + F_nonmetric
           ].
```

That is progress: `q_loc^nu` is no longer a mystery knob. But the right-hand side must still be zeroed or retained term by term.

## 5. Exchange Owner Conditions

{markdown_table(condition_rows, ["condition_id", "needed_for", "current_status", "failure_if_missing"])}

## 6. Source-Residual Decomposition

{markdown_table(source_residual_rows, ["term", "owner_condition", "residual_rows", "zero_status"])}

## 7. Measured-GM / `mu_extra` Decomposition

{markdown_table(mu_rows, ["mu_channel", "test_rows", "Ward_result", "status"])}

Ward conservation can say "the hidden contribution is owned." It cannot alone say "the hidden contribution is absent from measured `GM`." That is why `mu_extra=0` remains a separate source-normalization theorem target.

## 8. Residual Vector Implications

{markdown_table(residual_rows, ["row_id", "observable", "Ward_effect", "post_429_state"])}

## 9. Ward-Satisfying Counterexamples

{markdown_table(counter_rows, ["counterexample", "how_it_satisfies_Ward", "why_it_fails_local_GR"])}

These are the no-cheat examples. A theory can satisfy a Ward identity and still not reduce to GR. So the Ward identity is necessary footwork, not the knockout.

## 10. Theorem Attempt Status

{markdown_table(status_rows, ["target", "result", "evidence"])}

## 11. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is a useful step. We did not get the belt, but we now know the exact punch list. The local-GR derivation has become C0-C7. If we can prove those zero/retained conditions from the parent action, then `q_loc`, `source_residuals`, and `mu_extra` stop being hand-inserted closures and become derivable.

## 13. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "Ward_identity_chain.csv", WARD_IDENTITY_CHAIN)
    write_csv(results_dir / "exchange_owner_conditions.csv", EXCHANGE_OWNER_CONDITIONS)
    write_csv(results_dir / "source_residual_decomposition.csv", SOURCE_RESIDUAL_DECOMPOSITION)
    write_csv(results_dir / "mu_extra_decomposition.csv", MU_EXTRA_DECOMPOSITION)
    write_csv(results_dir / "residual_vector_implications.csv", RESIDUAL_VECTOR_IMPLICATIONS)
    write_csv(results_dir / "counterexample_branches.csv", COUNTEREXAMPLE_BRANCHES)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_gates = [row["gate"] for row in gate_result_rows if row["status"] == "fail" and row["gate"] not in {"source_residuals_zero_derived", "mu_extra_zero_derived", "local_GR_promoted"}]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "Ward_identity_steps": len(WARD_IDENTITY_CHAIN),
        "exchange_owner_conditions": len(EXCHANGE_OWNER_CONDITIONS),
        "source_residual_terms": len(SOURCE_RESIDUAL_DECOMPOSITION),
        "mu_extra_channels": len(MU_EXTRA_DECOMPOSITION),
        "residual_vector_rows": len(RESIDUAL_VECTOR_IMPLICATIONS),
        "q_loc_zero_derived": "conditional_only",
        "source_residuals_zero_derived": False,
        "mu_extra_zero_derived": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, source_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 429 Ward/Bianchi exchange-owner theorem attempt for Poisson source residuals."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
