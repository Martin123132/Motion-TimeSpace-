from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def coupling_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "SCT4462_0_same_coframe_functor",
            "object": "ordinary matter, clocks, rods, photons, EM and orbital readout",
            "exact_statement": "If every ordinary local sector is a functor of the same observed coframe/metric, S_A=S_A[Psi_A,e_obs,omega[e_obs],theta_A] and S_EM=-1/4 int sqrt(-g_obs) F^2, then every local source is measured by one Hilbert stress tensor T_H[g_obs].",
            "derives": "one source frame; no second metric/disformal matter readout; no standalone Poynting-background source",
            "must_be_parent_signed": "observed coframe functor, matter bundle functor, no-shadow-frame guard, Maxwell-Hodge owner and constant-sector split",
            "if_unsigned": "retain c_D, qbar_geom, qbar_marker, EM side-channel and material/source-charge residuals",
            "current_status": "CONDITIONAL_SELECTOR_THEOREM_NOT_GLOBAL_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_1_noether_hilbert_source",
            "object": "T_H^{mu nu}",
            "exact_statement": "For a diffeomorphism-invariant local action, T_H^{mu nu}=(-2/sqrt(-g_obs)) delta S_matter+EM/delta g_obs_munu and the field equations imply nabla_mu T_total^{mu nu}=0, with Lorentz/Poynting exchange internal to T_total.",
            "derives": "Bianchi-compatible source conservation and a single stress-energy object for matter plus EM",
            "must_be_parent_signed": "same action owns theta_total, Q_tau, boundary routing and Maxwell-Hodge stress",
            "if_unsigned": "source conservation and EM stress ownership become residual-bound inputs",
            "current_status": "EXACT_CONDITIONAL_NOETHER_CHAIN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_2_kappa_lock",
            "object": "kappa_eff and G_cal",
            "exact_statement": "If kappa_eff=kappa_* Z_H, the topological kappa sector gives D_A ln kappa_*=0, and Hilbert source-measure descent gives delta_ZH=0, then D_A ln kappa_eff=0 and G_cal=c^4 kappa_eff/(8*pi) is a local constant.",
            "derives": "no local Gdot, no range/species/source-frame drift in the calibrated coupling",
            "must_be_parent_signed": "topological kappa adoption plus Hilbert source-measure descent",
            "if_unsigned": "retain delta_kappa, delta_ZH, Gdot/G, species-source and radial-source residuals",
            "current_status": "PRIVATE_SELECTOR_ZERO_LAW_NOT_NUMERIC_G_PREDICTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_3_worldtube_charge",
            "object": "M_H^dress[W_H;tau]",
            "exact_statement": "If the Hamiltonian charge on a linking surface is radially stable, M_H^dress[W_H;tau]=H_tau[S_link]-H_ref=int_W rho_H dV defines the source mass before any orbital readout.",
            "derives": "anti-circular mass source for Poisson/Gauss/Newton readout",
            "must_be_parent_signed": "Pi_M/H_tau/worldtube glue, boundary silence and compact-exterior flux closure",
            "if_unsigned": "retain Pi_M commutator, extra current, boundary flux and calibration residuals",
            "current_status": "PRIVATE_PACKET_GLUE_PRESENT_PARENT_ADOPTION_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_4_poisson_newton",
            "object": "Newtonian limit",
            "exact_statement": "With G_munu[g_obs]=kappa_eff T_H_munu, G_00^lin=2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2 give nabla^2 Phi_N=4*pi G_cal rho_H and a_r=-G_cal M_H^dress/r^2.",
            "derives": "Newtonian mechanics as the slow-motion weak-field readout of the same Hilbert source",
            "must_be_parent_signed": "EH/Palatini principal block, kappa lock, Hilbert source and worldtube mass glue",
            "if_unsigned": "Newton branch remains a private selector closure or orbital residual test",
            "current_status": "STRUCTURAL_DERIVATION_CONDITIONAL_ON_SELECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_5_scalar_source_coupling",
            "object": "C_matter and alpha_eff",
            "exact_statement": "For a pure metric f(R)-like scalar branch with universal Hilbert trace coupling, C_matter=1 in the 4461 normalization and alpha_eff=1/3; scalar decoupling requires a parent zero theorem C_matter=0, while species-dependent C_A reopens WEP.",
            "derives": "the missing 4461 scalar coupling is no longer arbitrary: it is 1, 0, or species-dependent according to the parent source functor",
            "must_be_parent_signed": "pure R2 basis, same Hilbert trace source, no screening/readout loophole and no D2 contamination",
            "if_unsigned": "alpha_eff stays a residual coefficient tied to WEP/R10/PPN",
            "current_status": "CONDITIONAL_VALUE_MAP_WRITTEN_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_6_WEP_response",
            "object": "P_WEP eta_AB",
            "exact_statement": "For a finite-range source coupling a_i(r)=G_cal M/r^2[1+C_A C_S alpha_0(1+r/lambda)exp(-r/lambda)], eta_AB ~= (C_A-C_B) C_S alpha_0(1+r/lambda)exp(-r/lambda); universal same-Hilbert coupling gives C_A=C_B and eta_AB=0.",
            "derives": "first explicit WEP response operator for scalar/source drift rows",
            "must_be_parent_signed": "same matter source charge per inertial mass for all test bodies, source charge C_S fixed by the same worldtube Hilbert mass",
            "if_unsigned": "stage C_A-C_B and C_S as WEP/R10/orbital bound rows",
            "current_status": "RESPONSE_OPERATOR_FILLED_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCT4462_7_no_absorption_guard",
            "object": "fitted-G / fitted-GM guard",
            "exact_statement": "A coupling residual is not allowed to disappear into measured G or orbital GM unless the parent proves it is a constant universal calibration; radial, time, range, source, species or frame dependence must remain as named residuals.",
            "derives": "anti-cheat guard for local source-normalization tests",
            "must_be_parent_signed": "D_A ln kappa_eff=0 and delta source/readout residuals zero, or explicit bound rows",
            "if_unsigned": "retain epsilon_radial, epsilon_time, epsilon_species, epsilon_frame, alpha(lambda), Gdot/G and PPN beta/gamma residuals",
            "current_status": "GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_law_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "NSL4462_0_EH_source",
            "equation": "G_munu[g_obs] = kappa_eff T_H_munu",
            "requires": "same-coframe Hilbert source and EH/Palatini principal block",
            "result": "source side is one T_H, not galaxy/cosmology/orbit-specific fitted source",
            "status": "PRIVATE_SELECTOR_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "law_id": "NSL4462_1_G_cal",
            "equation": "G_cal = c^4 kappa_eff/(8*pi)",
            "requires": "topological kappa lock and source-measure normalization",
            "result": "calibrated Newton coupling; numerical G not predicted unless parent fixes kappa_eff",
            "status": "STRUCTURAL_NOT_NUMERIC_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "law_id": "NSL4462_2_Poisson",
            "equation": "nabla^2 Phi_N = 4*pi G_cal rho_H",
            "requires": "G_00^lin=2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2",
            "result": "Newtonian Poisson equation from the same Hilbert source",
            "status": "CONDITIONAL_DERIVED",
            "valid_for_claim": False,
        },
        {
            "law_id": "NSL4462_3_Gauss_orbit",
            "equation": "Phi_N=-G_cal M_H^dress/r; a_r=-G_cal M_H^dress/r^2",
            "requires": "worldtube Hamiltonian mass and exterior monopole/far-field readout",
            "result": "orbital acceleration tests the charge instead of defining it",
            "status": "CONDITIONAL_DERIVED",
            "valid_for_claim": False,
        },
        {
            "law_id": "NSL4462_4_EM_stress",
            "equation": "T_EM^{mu nu}=F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F^2; S_i=-T_EM(n,e_i)",
            "requires": "Maxwell-Hodge owner on g_obs",
            "result": "Poynting flux is a Hilbert-stress component, not a separate background force",
            "status": "PRIVATE_SELECTOR_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "law_id": "NSL4462_5_WEP_yukawa",
            "equation": "eta_AB ~= (C_A-C_B) C_S alpha_0(1+r/lambda) exp(-r/lambda)",
            "requires": "linear finite-range source coupling and common source-frame normalization",
            "result": "universal coupling gives eta_AB=0; species coupling becomes testable",
            "status": "SYMBOLIC_RESPONSE_OPERATOR",
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "SRC4462_0_delta_kappa",
            "symbol": "delta_kappa",
            "meaning": "source-coupling drift after kappa/source-measure normalization",
            "zero_condition": "D_A ln kappa_* = 0 and delta_ZH = D_A delta_ZH = 0",
            "observable": "Gdot/G; orbital GM; PPN beta/gamma; clocks",
            "fallback_bound_row": "MISSING_DELTA_KAPPA_PROFILE_OR_ZERO_THEOREM",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_1_species_charge",
            "symbol": "Delta_C_AB = C_A-C_B",
            "meaning": "composition-dependent scalar/source charge per inertial mass",
            "zero_condition": "same Hilbert source charge for all ordinary matter species",
            "observable": "WEP eta_AB; clock/source charge; R10 if finite range",
            "fallback_bound_row": "MISSING_SPECIES_CHARGE_VECTOR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_2_source_charge",
            "symbol": "C_S",
            "meaning": "source worldtube scalar/source charge relative to Hilbert mass",
            "zero_condition": "source charge equals universal Hilbert mass or scalar source decouples",
            "observable": "R10 alpha(lambda); orbital inverse-square; WEP source response",
            "fallback_bound_row": "MISSING_SOURCE_CHARGE_NORMALIZATION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_3_frame_leak",
            "symbol": "c_D/qbar_geom",
            "meaning": "second metric, disformal frame, or visible-geometry frame leakage",
            "zero_condition": "single observed coframe functor and no-shadow-frame theorem",
            "observable": "WEP; clocks; lightcone; EM propagation; PPN gamma",
            "fallback_bound_row": "MISSING_FRAME_LEAK_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_4_DeltaGamma_WEP",
            "symbol": "DeltaGamma_WEP",
            "meaning": "connection/hypermomentum contribution to differential acceleration",
            "zero_condition": "metric/coframe-only connection or source-silent algebraic connection equation",
            "observable": "WEP; clocks; lightcone; PPN",
            "fallback_bound_row": "MISSING_DELTAGAMMA_COMPONENT_VALUES_AND_UNITS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_5_alpha_R2",
            "symbol": "alpha_eff(lambda_R2)",
            "meaning": "finite c2/R2 scalar branch source coupling",
            "zero_condition": "c2=0, c_R2_eff=0, or C_matter=0 by parent theorem",
            "observable": "R10; PPN gamma; orbital inverse-square; WEP if species-dependent",
            "fallback_bound_row": "MISSING_C2_CMATTER_ALPHA_BOUND_CURVE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "SRC4462_6_EM_side_channel",
            "symbol": "epsilon_EM_extra_inner",
            "meaning": "hidden EM-current multiplier or standalone Poynting-background source",
            "zero_condition": "Maxwell-Hodge Hilbert stress owner and radiative boundary routing",
            "observable": "EM propagation; source energy accounting; Poynting flux; clocks",
            "fallback_bound_row": "MISSING_EM_SIDE_CHANNEL_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4462_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "source validation is performed by the generator",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4462_1_coupling_theorem",
            "claim": "source-coupling/Newton theorem is written",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "structural theorem is conditional on private selector adoption",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4462_2_PWEP_operator",
            "claim": "first WEP response operator is filled",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "symbolic eta_AB operator filled; component/source charges remain unsourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4462_3_numeric_G",
            "claim": "MTS predicts numerical Newton G",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "G_cal is structurally calibrated; no parent scale law fixes kappa_eff numerically",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4462_4_public_local_GR",
            "claim": "public MTS-to-local-GR/Newton claim allowed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "parent adoption, residual coefficients and empirical gates remain open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4462_5_next_target",
            "claim": "next kappa scale/residual target selected",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "4463-Y5-R2FR-parent-kappa-scale-law-or-calibrated-G-residual-runner.md",
            "valid_for_claim": False,
        },
    ]
