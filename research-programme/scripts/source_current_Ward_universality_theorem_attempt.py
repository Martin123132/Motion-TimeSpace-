from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-current-Ward-universality-theorem-attempt"
CHECKPOINT_DOC = "449-source-current-Ward-universality-theorem-attempt.md"
STATUS = "source_current_Ward_universality_theorem_attempt_written_Hilbert_current_conditional_measured_GM_not_parent_derived_P8_R1_R4_R9_R11_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "source_current_Ward_universality_conditional_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "450-Hilbert-source-to-measured-monopole-calibration-gate.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv")


CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "closes_component",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source normalization and measured-GM obstruction",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "EH-to-Poisson bridge and source-normalization requirements",
    },
    {
        "path": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "role": "conditional Ward source-ownership theorem and Bianchi warning",
    },
    {
        "path": "446-source-owner-current-parent-action-contract.md",
        "role": "parent action blocks needed for K_owner and q_retained",
    },
    {
        "path": "448-constant-sector-universality-theorem-attempt.md",
        "role": "constant-sector route and source-current Ward next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "C0-C7 source-owner identity contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A0-A10 source-owner parent-action term contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
        "role": "legal q_retained zero routes",
    },
    {
        "path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
        "role": "constant-sector C3 universal source variation requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 residual vector fallback",
    },
    {
        "path": "runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/owner_identity_contract.csv",
        "role": "machine owner-current identity rows",
    },
    {
        "path": "runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/residual_current_ledger.csv",
        "role": "residual source/exchange channel ledger",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/variation_identity_requirements.csv",
        "role": "V0-V8 variation identities",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/q_retained_zero_conditions.csv",
        "role": "q_retained legal zero condition rows",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/residual_activation_map.csv",
        "role": "source-owner failures to residual rows",
    },
    {
        "path": "runs/20260602-153000-constant-sector-universality-theorem-attempt/results/constant_sector_contract.csv",
        "role": "C3 source-current universality input from 448",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_Hilbert_source_current_theorem",
        "statement": "If all matter species couple to one observed coframe, matter constants are MTS-independent representation data, and the gravitational source is defined by the Hilbert/coframe variation of the same matter action with one universal coupling, then the active matter source current is species-blind.",
        "mathematical_form": "tau_a^mu = det(e)^-1 delta S_m/delta e_mu^a; T_munu = e_(mu)^a tau_{nu)a}; E_munu = kappa_univ T_munu; no kappa_A J_A",
        "status": "valid_conditional_source_rule",
    },
    {
        "part": "Ward_conservation_limit",
        "statement": "Diffeomorphism and local Lorentz Ward identities give on-shell conservation and stress symmetrization, but they do not by themselves prove measured orbital GM, zero boundary flux, zero hidden exchange, or absolute mass calibration.",
        "mathematical_form": "nabla_mu T_tot^{mu nu}=0 does not imply mu_obs=G_eff M_eff or q_retained^nu=0",
        "status": "blocks_overclaim",
    },
    {
        "part": "current_corpus_status",
        "statement": "The current corpus has contracts for the required source current, but it has not derived the source-current Ward identity plus mass-monopole calibration and zero retained current from a completed parent action.",
        "mathematical_form": "C3_universal_source_variation and P8 C0-C7 remain contract rows",
        "status": "not_parent_derived",
    },
]


WARD_IDENTITIES = [
    {
        "identity_id": "W0_Hilbert_coframe_current",
        "identity": "matter source current is the observed-coframe variation",
        "mathematical_form": "tau_a^mu = det(e)^-1 delta S_m/delta e_mu^a",
        "what_it_gives": "one source definition for all matter fields",
        "what_remains_open": "whether S_parent really forbids extra source weights or hidden source terms",
        "status": "conditional_input",
    },
    {
        "identity_id": "W1_local_Lorentz_symmetry",
        "identity": "spin/hypermomentum improvements are either Belinfante-owned or retained",
        "mathematical_form": "T_[munu] + D_lambda S^lambda_{munu}=0",
        "what_it_gives": "symmetric metric stress if connection/spin sectors are properly owned",
        "what_remains_open": "independent connection, torsion, or projective source charge",
        "status": "not_closed_for_all_sectors",
    },
    {
        "identity_id": "W2_diffeomorphism_Ward",
        "identity": "on matter equations, the Hilbert stress is covariantly conserved in the observed geometry",
        "mathematical_form": "nabla_mu T_m^{mu nu}=0 if E_Psi=0 and no explicit nonmetric/source arguments",
        "what_it_gives": "geodesic/source conservation route",
        "what_remains_open": "separate observed-source conservation if hidden sectors exchange momentum",
        "status": "conditional_standard_identity",
    },
    {
        "identity_id": "W3_universal_coupling",
        "identity": "field equation uses one kappa for the Hilbert current",
        "mathematical_form": "E_munu[g_obs] = kappa_univ T_munu + retained_residuals_munu",
        "what_it_gives": "no kappa_A species source weight",
        "what_remains_open": "constant kappa/G_eff and residual source tensor elimination",
        "status": "not_parent_derived",
    },
    {
        "identity_id": "W4_mass_monopole_projection",
        "identity": "Newtonian source monopole is the calibrated mass projection of the same Hilbert current",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_Hilbert and d(Pi_M J_Hilbert)=0",
        "what_it_gives": "route from field source to measured GM",
        "what_remains_open": "absolute calibration and no radial/time/species leakage",
        "status": "conditional_flux_calibration_open",
    },
    {
        "identity_id": "W5_residual_source_split",
        "identity": "all non-Hilbert source terms are exact-owned zero flux or retained",
        "mathematical_form": "q_res^nu = nabla_mu K_owner^{mu nu} + q_retained^nu",
        "what_it_gives": "honest separation between theorem-zero and residual data",
        "what_remains_open": "K_owner formula and q_retained zero proof",
        "status": "not_parent_derived",
    },
]


PROOF_STEPS = [
    {
        "step": 1,
        "claim": "Start with one observed coframe and selector-blind matter.",
        "mathematical_step": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "status": "conditional_from_prior_contracts",
        "gap": "one observed coframe and selector blindness remain contract-labelled",
    },
    {
        "step": 2,
        "claim": "Define the matter source current by variation with respect to that coframe.",
        "mathematical_step": "tau_a^mu = det(e)^-1 delta S_m/delta e_mu^a",
        "status": "valid_definition_if_parent_uses_e_obs",
        "gap": "source current must be defined before readout/fitting, not after residuals are known",
    },
    {
        "step": 3,
        "claim": "Local Lorentz and diffeomorphism Ward identities make this the conserved Hilbert/Belinfante source on matter shell.",
        "mathematical_step": "D_mu tau_a^mu = 0 or nabla_mu T_m^{mu nu}=0 after matter EOM and owned spin terms",
        "status": "conditional_standard_identity",
        "gap": "independent connection or hypermomentum source terms can survive unless P4/P8 closes them",
    },
    {
        "step": 4,
        "claim": "If the gravitational equation couples with one universal kappa, species source weights are forbidden.",
        "mathematical_step": "E_munu = kappa_univ sum_A T_A_munu, not sum_A kappa_A T_A_munu",
        "status": "valid_conditional_math",
        "gap": "kappa_univ is not parent-derived constant/universal in the current corpus",
    },
    {
        "step": 5,
        "claim": "Then active source charge is zero relative to inertial Hilbert mass for ordinary matter.",
        "mathematical_step": "partial_A ln(mu_Hilbert/M_inertial)=0",
        "status": "conditional_for_Hilbert_source",
        "gap": "measured orbital mu_obs may still include mu_extra, boundary flux, range charge, or calibration drift",
    },
    {
        "step": 6,
        "claim": "To become measured Newtonian GM, the Hilbert current must equal the closed calibrated mass-flux projector.",
        "mathematical_step": "mu_obs=G_eff M_eff[J_Hilbert] and d(Pi_M J_Hilbert)=0",
        "status": "not_parent_derived",
        "gap": "checkpoint 446 lists A4/C3 as conditional_flux_calibration_open",
    },
    {
        "step": 7,
        "claim": "All non-Hilbert source currents must be absent, exact-owned zero flux, no-haired, or retained.",
        "mathematical_step": "q_retained^nu=0 by legal zero route, or q_retained enters P8 residual vector",
        "status": "not_parent_derived",
        "gap": "boundary, bulk, domain, memory, range, and connection channels remain open",
    },
    {
        "step": 8,
        "claim": "Therefore Ward source universality is a strong sublemma, not a Newton/local-GR promotion.",
        "mathematical_step": "Hilbert source universality != measured_GM pass unless P8 C0-C7 close",
        "status": "no_promotion",
        "gap": "next target is Hilbert-source-to-measured-monopole calibration",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "species_weighted_source_equation",
        "construction": "E_munu=sum_A kappa_A T_A_munu with all T_A from the same e_obs",
        "why_Ward_does_not_block": "each T_A can be conserved while the gravitational equation weights species differently",
        "required_blocker": "universal kappa/source-current parent identity",
        "affected_rows": "R1;R4;R11",
    },
    {
        "counterexample": "nonminimal_curvature_matter_coupling",
        "construction": "S_m contains f_A(Z) R O_A or alpha_EM(Z) F^2",
        "why_Ward_does_not_block": "Ward identities move terms between stress and geometry but do not set coefficients zero",
        "required_blocker": "no direct memory/projector matter-argument theorem",
        "affected_rows": "R1;R2;R3;R4;R10;R11",
    },
    {
        "counterexample": "independent_connection_hypermomentum",
        "construction": "matter has hypermomentum/projective source charge in an independent connection sector",
        "why_Ward_does_not_block": "coframe Hilbert stress is not the full source if connection variation carries source charge",
        "required_blocker": "P4 compatibility plus no-Gamma source-charge theorem",
        "affected_rows": "R0;R1;R2;R11",
    },
    {
        "counterexample": "boundary_improvement_monopole",
        "construction": "T_munu -> T_munu + nabla_lambda B^{lambda}_{munu} with nonzero compact-boundary flux",
        "why_Ward_does_not_block": "improvement is conserved locally but shifts the surface monopole",
        "required_blocker": "zero compact boundary flux theorem",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
    },
    {
        "counterexample": "hidden_bulk_or_domain_exchange",
        "construction": "nabla_mu T_matter^{mu nu}=-F_X^nu-F_D^nu while total T is conserved",
        "why_Ward_does_not_block": "total conservation allows exchange with hidden sectors",
        "required_blocker": "exact owner decomposition plus q_retained=0 or residual scoring",
        "affected_rows": "R4;R7;R9;R10;R11",
    },
    {
        "counterexample": "mass_flux_projector_calibration_split",
        "construction": "J_Hilbert is conserved but Pi_M J used for orbital GM is not absolutely calibrated",
        "why_Ward_does_not_block": "conservation is not normalization to measured GM",
        "required_blocker": "closed calibrated mass-monopole theorem",
        "affected_rows": "R1;R4;R9;R10;R11",
    },
    {
        "counterexample": "universal_time_or_range_drift",
        "construction": "kappa_univ(t,r,lambda) or G_eff(t,r,lambda) multiplies a universal source",
        "why_Ward_does_not_block": "species universality can hold while Newtonian GM drifts or becomes range dependent",
        "required_blocker": "constant universal coupling and no range/radial source hair",
        "affected_rows": "R4;R9;R10;R11",
    },
]


PROMOTION_LADDER = [
    {
        "level": "L0_total_Ward_conservation",
        "identity": "nabla_mu T_tot^{mu nu}=0",
        "earns": "bookkeeping consistency only",
        "does_not_earn": "measured GM, WEP source charge, Newton, or local GR",
        "current_status": "structural_available_not_sufficient",
    },
    {
        "level": "L1_Hilbert_matter_source",
        "identity": "T_munu = 2/sqrt(-g) delta S_m/delta g_munu or coframe equivalent",
        "earns": "common matter source current if one-frame/selector-blind premises hold",
        "does_not_earn": "absolute source calibration or no hidden residual current",
        "current_status": "conditional_sublemma",
    },
    {
        "level": "L2_universal_gravity_coupling",
        "identity": "E_munu = kappa_univ T_munu",
        "earns": "no species-weighted active source for ordinary matter",
        "does_not_earn": "time/range/radial constancy of G_eff or zero mu_extra",
        "current_status": "not_parent_derived",
    },
    {
        "level": "L3_measured_monopole_calibration",
        "identity": "mu_obs=G_eff M_eff[J_Hilbert], d(Pi_M J_Hilbert)=0, mu_extra=0",
        "earns": "Newtonian measured-GM source normalization",
        "does_not_earn": "full PPN beta/gamma/preferred-frame completion by itself",
        "current_status": "not_parent_derived",
    },
    {
        "level": "L4_PPN_local_GR_completion",
        "identity": "EH operator plus all R0-R11 residuals theorem-zero or bounded",
        "earns": "local-GR branch",
        "does_not_earn": "cosmology or full unified theory by itself",
        "current_status": "not_promoted",
    },
]


CONTRACT = [
    {
        "contract_id": "SC0_single_observed_coframe_input",
        "required_identity": "all matter/source standards vary the same observed coframe",
        "mathematical_form": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "closes_component": "frame split input to Hilbert current",
        "affected_rows": "R0;R1;R2;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "parent-selected observed-frame theorem",
        "fallback_if_missing": "frame/source calibration residuals remain active",
    },
    {
        "contract_id": "SC1_Hilbert_source_definition",
        "required_identity": "active ordinary matter source is defined by variation of the matter action",
        "mathematical_form": "tau_a^mu=det(e)^-1 delta S_m/delta e_mu^a",
        "closes_component": "ordinary matter source-current definition",
        "affected_rows": "R1;R4;R11",
        "current_status": "conditional_definition",
        "evidence_needed": "explicit parent source-current definition before readout/scoring",
        "fallback_if_missing": "source current remains fitted/readout-defined",
    },
    {
        "contract_id": "SC2_Ward_conservation_on_matter_shell",
        "required_identity": "diffeomorphism/local Lorentz Ward identities conserve and symmetrize the Hilbert current",
        "mathematical_form": "nabla_mu T_m^{mu nu}=0 after E_Psi=0 and owned spin/connection terms",
        "closes_component": "separate matter-current conservation",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "conditional_standard_identity",
        "evidence_needed": "show no explicit MTS/source arguments or unowned connection terms in S_m",
        "fallback_if_missing": "exchange force residuals remain active",
    },
    {
        "contract_id": "SC3_universal_kappa_coupling",
        "required_identity": "field equation uses one universal source coupling for the Hilbert current",
        "mathematical_form": "E_munu=kappa_univ T_munu, partial_A kappa_univ=0",
        "closes_component": "species source-weight split",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant universal coupling parent identity",
        "fallback_if_missing": "kappa_A/source-charge residual row remains",
    },
    {
        "contract_id": "SC4_no_nonHilbert_source_current",
        "required_identity": "bulk, boundary, domain, memory, range, and connection sectors do not add unowned active source current",
        "mathematical_form": "q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu with q_retained^nu=0 or retained",
        "closes_component": "mu_extra/source exchange bypass",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "formula-level K_owner and legal q_retained zero proof",
        "fallback_if_missing": "P8 residual vector and boundary/exchange coefficient rows remain",
    },
    {
        "contract_id": "SC5_zero_compact_boundary_flux",
        "required_identity": "owned divergence has no compact exterior source flux except a universal constant calibration",
        "mathematical_form": "int_partialSigma n_i K_owner^{i0} dS=0 or constant universal calibration",
        "closes_component": "boundary/improvement monopole",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
        "evidence_needed": "class-only/topological no-flux boundary theorem",
        "fallback_if_missing": "alpha3/Gdot/source-normalization rows remain retained",
    },
    {
        "contract_id": "SC6_closed_calibrated_mass_projector",
        "required_identity": "measured-GM mass monopole is the closed calibrated projection of the Hilbert current",
        "mathematical_form": "d(Pi_M J_Hilbert)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_Hilbert",
        "closes_component": "measured GM source normalization",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_flux_calibration_open",
        "evidence_needed": "mass-flux projector Euler equation and absolute calibration proof",
        "fallback_if_missing": "measured-GM/Newton claim blocked",
    },
    {
        "contract_id": "SC7_no_time_range_radial_species_drift",
        "required_identity": "source strength carries no time, radial, range, species, or frame dependence beyond the calibrated monopole",
        "mathematical_form": "partial_t mu_obs=partial_r mu_obs=partial_lambda mu_obs=partial_A mu_obs=0",
        "closes_component": "Gdot/fifth-force/source-charge/radial hair",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant coupling plus no range/radial/source-charge theorems",
        "fallback_if_missing": "Gdot/source/fifth-force residuals remain",
    },
    {
        "contract_id": "SC8_second_order_source_stability",
        "required_identity": "first-order Hilbert-source normalization survives PPN beta order",
        "mathematical_form": "delta_beta_source=0 after measured-GM normalization",
        "closes_component": "nonlinear source-normalization beta residue",
        "affected_rows": "R4;R11",
        "current_status": "not_derived",
        "evidence_needed": "second-order weak-field source solution",
        "fallback_if_missing": "beta/source residual row remains active",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_Hilbert_source_current_written",
        "pass_condition": "one-frame selector-blind matter plus Hilbert variation gives a common source current",
        "current_result": "pass_conditional",
        "evidence": "Ward identity and proof chain recorded",
    },
    {
        "gate": "Ward_not_overclaimed",
        "pass_condition": "total conservation is not treated as measured-GM calibration",
        "current_result": "pass",
        "evidence": "promotion ladder separates L0-L4",
    },
    {
        "gate": "species_weight_counterexample_retained",
        "pass_condition": "kappa_A T_A counterexample remains visible",
        "current_result": "pass",
        "evidence": "counterexample table recorded",
    },
    {
        "gate": "source_current_parent_derived",
        "pass_condition": "SC0-SC8 are parent-derived",
        "current_result": "fail",
        "evidence": "universal kappa, no non-Hilbert current, zero boundary flux, and mass projector calibration remain open",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "mu_obs=G_eff M_eff[J_Hilbert] with mu_extra=0",
        "current_result": "fail",
        "evidence": "Hilbert source sublemma only; measured monopole calibration not derived",
    },
    {
        "gate": "local_GR_promoted",
        "pass_condition": "full R0-R11 vector and parent premises are cleared",
        "current_result": "fail",
        "evidence": "source-current checkpoint only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "Hilbert source-current conditional theorem written",
        "status": "pass_conditional",
        "evidence": "coframe variation plus Ward identities recorded",
    },
    {
        "claim": "Ward/Bianchi overclaim blocked",
        "status": "pass",
        "evidence": "promotion ladder separates total conservation from measured-GM calibration",
    },
    {
        "claim": "source-current universality contract written",
        "status": "pass",
        "evidence": str(CONTRACT_PATH),
    },
    {
        "claim": "universal kappa/source equation parent-derived",
        "status": "fail",
        "evidence": "SC3 remains not_parent_derived",
    },
    {
        "claim": "measured Hilbert monopole parent-derived",
        "status": "fail",
        "evidence": "SC6 remains conditional_flux_calibration_open",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "P8/R1/R4/R9/R11 remain retained",
    },
]


DECISION = [
    {
        "decision": "The source-current Ward universality route has been sharpened. A real conditional theorem is available: with one observed coframe, selector-blind matter, MTS-independent constants, Hilbert/coframe source definition, and one universal kappa, ordinary matter has a common active source current and no species-weighted source charge. But Ward conservation is not measured-GM calibration. The current corpus still lacks universal kappa, zero non-Hilbert source current, zero compact boundary flux, closed calibrated mass-monopole projection, no time/range/radial/species drift, and second-order source stability. Therefore this checkpoint is a strong GR-style sublemma, not a Newton, PPN, measured-GM, or local-GR promotion.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": NEXT_TARGET,
        "why_next": "the next missing bridge is equality between the Hilbert source current and the measured Newtonian monopole",
    },
    {
        "rank": 2,
        "target": "derive constant universal kappa/G_eff identity",
        "why_next": "source current universality still fails if the field equation carries kappa_A or G_eff drift",
    },
    {
        "rank": 3,
        "target": "map SC0-SC8 into the P8 residual evaluator",
        "why_next": "failed source-current contracts should automatically activate R1/R4/R9/R11 rows",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as output_handle:
        writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for data_row in rows:
        values = []
        for fieldname in fieldnames:
            value = str(data_row.get(fieldname, ""))
            value = value.replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    source_register = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        source_register.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return source_register


def build_gate_results(source_register: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]
    gate_results = [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == CONTRACT_COLUMNS else "fail",
            "evidence": "source-current Ward contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 3 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem statement rows",
        },
        {
            "gate": "Ward_identities_written",
            "status": "pass" if len(WARD_IDENTITIES) == 6 else "fail",
            "evidence": f"{len(WARD_IDENTITIES)} Ward identity rows",
        },
        {
            "gate": "proof_steps_written",
            "status": "pass" if len(PROOF_STEPS) == 8 else "fail",
            "evidence": f"{len(PROOF_STEPS)} proof steps recorded",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLES) == 7 else "fail",
            "evidence": f"{len(COUNTEREXAMPLES)} counterexamples recorded",
        },
        {
            "gate": "promotion_ladder_written",
            "status": "pass" if len(PROMOTION_LADDER) == 5 else "fail",
            "evidence": f"{len(PROMOTION_LADDER)} promotion levels recorded",
        },
        {
            "gate": "source_current_contract_written",
            "status": "pass",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "Ward_not_overclaimed",
            "status": "pass",
            "evidence": "total Ward conservation is separated from Hilbert source and measured-GM calibration",
        },
        {
            "gate": "Hilbert_source_current_conditional",
            "status": "pass",
            "evidence": "conditional coframe/Hilbert source theorem recorded",
        },
        {
            "gate": "universal_kappa_parent_derived",
            "status": "fail",
            "evidence": "SC3 remains not_parent_derived",
        },
        {
            "gate": "nonHilbert_source_zero_derived",
            "status": "fail",
            "evidence": "SC4 and SC5 remain open/fail_open",
        },
        {
            "gate": "measured_monopole_calibrated",
            "status": "fail",
            "evidence": "SC6 remains conditional_flux_calibration_open",
        },
        {
            "gate": "P8_species_source_charge_theorem_zero",
            "status": "fail",
            "evidence": "Hilbert source current does not by itself clear all P8 species/source channels",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "measured GM and extra source channels remain open",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "source-current theorem attempt only",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 449 - Source-Current Ward Universality Theorem Attempt

Private P8/R1/R4/R9/R11 source-current checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 448 isolated the missing constant-sector bridge: the active gravitational source must be the same Ward/Hilbert current that matter uses in the observed coframe, not a species-weighted or readout-defined source current.

This checkpoint asks whether Ward identities can derive that source current. The answer is useful but limited: they can define and conserve the Hilbert source under strong premises, but measured Newtonian `GM` still requires calibration, zero flux, and no retained source current.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_current_Ward_universality_theorem_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Ward Identities

{markdown_table(WARD_IDENTITIES)}

## 6. Conditional Proof Steps

{markdown_table(PROOF_STEPS)}

## 7. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 8. Promotion Ladder

{markdown_table(PROMOTION_LADDER)}

## 9. Source-Current Ward Contract

The source-current Ward universality contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 10. Gate Tests

{markdown_table(GATE_TESTS)}

## 11. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 12. Gate Results

{markdown_table(gate_results)}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: this is one of the better GR-connection moves so far. The route to GR-like source universality is not mystical: one observed coframe, Hilbert stress, Ward conservation, and one universal coupling. But the hard Newton step is still not free. The Hilbert current must be shown to be the measured mass monopole with no hidden boundary, bulk, domain, range, memory, or connection source. That is the next gate.

## 14. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    gate_results = build_gate_results(source_register)
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "theorem_statement.csv", THEOREM_STATEMENT)
    write_csv(results_dir / "Ward_identities.csv", WARD_IDENTITIES)
    write_csv(results_dir / "proof_steps.csv", PROOF_STEPS)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
    write_csv(results_dir / "promotion_ladder.csv", PROMOTION_LADDER)
    write_csv(results_dir / "source_current_Ward_contract.csv", CONTRACT, CONTRACT_COLUMNS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / CONTRACT_PATH, CONTRACT, CONTRACT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_Hilbert_source_current_written": True,
        "Ward_not_overclaimed": True,
        "Hilbert_source_current_conditional": True,
        "universal_kappa_parent_derived": False,
        "nonHilbert_source_zero_derived": False,
        "measured_monopole_calibrated": False,
        "P8_species_source_charge_derived_zero": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "counterexamples": len(COUNTEREXAMPLES),
        "contract_rows": len(CONTRACT),
        "failed_gates": [gate_row["gate"] for gate_row in gate_results if gate_row["status"] == "fail"],
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the MTS source-current Ward universality theorem attempt checkpoint.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-154500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()

