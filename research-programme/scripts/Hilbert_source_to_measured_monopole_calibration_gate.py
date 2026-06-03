from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Hilbert-source-to-measured-monopole-calibration-gate"
CHECKPOINT_DOC = "450-Hilbert-source-to-measured-monopole-calibration-gate.md"
STATUS = "Hilbert_source_to_measured_monopole_calibration_gate_written_conditional_Newton_bridge_calibration_not_parent_derived_P8_R1_R4_R9_R10_R11_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "Hilbert_monopole_calibration_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "451-mass-flux-projector-Euler-calibration-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv")


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
        "role": "EH/source weak-field chain and mu_obs decomposition",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson bridge and measured-GM requirements",
    },
    {
        "path": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "role": "Ward source ownership theorem and measured-GM caveats",
    },
    {
        "path": "446-source-owner-current-parent-action-contract.md",
        "role": "A4 mass-flux projector and parent action calibration terms",
    },
    {
        "path": "449-source-current-Ward-universality-theorem-attempt.md",
        "role": "Hilbert source-current sublemma and next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "SC6 closed calibrated mass projector requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "C3 closed calibrated mass current requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A4 mass-flux projector parent action block",
    },
    {
        "path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
        "role": "legal residual-current zero routes",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 source-normalization residual fallback",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "R1/R4/R9/R10 local source locks",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv",
        "role": "mu_obs source-normalization decomposition",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv",
        "role": "P8 measured-GM residual rows",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "A7 mass-flux projector Euler ledger",
    },
    {
        "path": "runs/20260602-154500-source-current-Ward-universality-theorem-attempt/results/source_current_Ward_contract.csv",
        "role": "machine source-current Ward contract rows",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_measured_monopole_theorem",
        "statement": "If the Hilbert/coframe current is the only active source, the mass-flux projector is closed and absolutely calibrated, the coupling is constant and universal, and all boundary/bulk/domain/range/species residual currents vanish or are retained below locks, then measured orbital GM equals the Hilbert monopole.",
        "mathematical_form": "mu_obs = G_eff M_eff[J_H] + mu_extra; d(Pi_M J_H)=0; mu_extra=0; partial_{t,r,A,lambda} mu_obs=0 => mu_obs=G_eff M_H",
        "status": "valid_conditional_Newton_source_bridge",
    },
    {
        "part": "calibration_limit",
        "statement": "A conserved Hilbert current is not automatically the measured Newtonian monopole; conservation does not fix the absolute normalization, the surface flux, or the absence of finite-range/radial/source-charge corrections.",
        "mathematical_form": "nabla_mu T_H^{mu nu}=0 does not imply M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H or mu_extra=0",
        "status": "blocks_overclaim",
    },
    {
        "part": "current_corpus_status",
        "statement": "The current corpus has the right calibration contracts and residual-vector rows, but it has not derived the mass-flux Euler equation, absolute calibration, zero compact-boundary flux, or constant universal coupling.",
        "mathematical_form": "A4/C3/SC6 remain conditional_flux_calibration_open",
        "status": "not_parent_derived",
    },
]


CALIBRATION_CHAIN = [
    {
        "step": 1,
        "chain_item": "Hilbert source current",
        "mathematical_form": "J_H from T_H^{mu nu}=2/sqrt(-g) delta S_m/delta g_munu or coframe equivalent",
        "needed_for": "formal matter source",
        "current_status": "conditional_from_449",
    },
    {
        "step": 2,
        "chain_item": "mass-flux projector",
        "mathematical_form": "Pi_M J_H selects the compact source monopole current",
        "needed_for": "separate mass monopole from stress/improvement/exchange terms",
        "current_status": "conditional_flux_calibration_open",
    },
    {
        "step": 3,
        "chain_item": "closed current",
        "mathematical_form": "d(Pi_M J_H)=0 or nabla_mu J_M^mu=0",
        "needed_for": "no source mass drift and no hidden exchange",
        "current_status": "not_parent_derived",
    },
    {
        "step": 4,
        "chain_item": "absolute calibration",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H",
        "needed_for": "turn source current into measured orbital GM",
        "current_status": "not_parent_derived",
    },
    {
        "step": 5,
        "chain_item": "constant universal coupling",
        "mathematical_form": "G_eff=kappa_eff c^4/(8 pi), partial_{t,r,A,lambda}G_eff=0",
        "needed_for": "Newtonian constant G rather than source-dependent calibration",
        "current_status": "not_parent_derived",
    },
    {
        "step": 6,
        "chain_item": "zero residual source monopole",
        "mathematical_form": "mu_extra=mu_boundary+mu_bulk+mu_domain+mu_memory+mu_range+mu_connection=0",
        "needed_for": "no hidden source hair or measured-GM absorption",
        "current_status": "not_parent_derived",
    },
    {
        "step": 7,
        "chain_item": "first-order Newton source",
        "mathematical_form": "nabla^2 Phi=4 pi G_eff rho_H with mu_obs=G_eff M_H",
        "needed_for": "Newtonian measured-GM force law",
        "current_status": "conditional_if_all_prior_steps_close",
    },
    {
        "step": 8,
        "chain_item": "second-order stability",
        "mathematical_form": "delta_beta_source=0 after the same normalization",
        "needed_for": "PPN beta/local-GR completion",
        "current_status": "not_derived",
    },
]


MONOPOLE_REQUIREMENTS = [
    {
        "requirement_id": "M0_same_frame_current",
        "requirement": "Hilbert current is varied in the same observed frame used by matter, clocks, rods, and the EH/Poisson operator",
        "mathematical_form": "e_source=e_matter=e_metric=e_obs",
        "failure_mode": "frame calibration split",
        "affected_rows": "R0;R2;R11",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "requirement_id": "M1_projector_defined_before_readout",
        "requirement": "Pi_M is a parent/source-normalization object, not a post-fit orbital readout mask",
        "mathematical_form": "Pi_M in S_source_norm before scoring",
        "failure_mode": "readout-defined GM absorbs new physics",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "conditional_no_cheat_contract",
    },
    {
        "requirement_id": "M2_flux_closure",
        "requirement": "projected mass current is closed in the compact local branch",
        "mathematical_form": "d(Pi_M J_H)=0",
        "failure_mode": "M_eff drift or exchange flux",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "conditional_flux_calibration_open",
    },
    {
        "requirement_id": "M3_absolute_orbital_calibration",
        "requirement": "the surface/integral normalization equals the measured orbital monopole",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H",
        "failure_mode": "conserved but misnormalized mass",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
    },
    {
        "requirement_id": "M4_no_boundary_improvement_flux",
        "requirement": "stress improvements and owned divergences carry no compact boundary monopole",
        "mathematical_form": "int_partialSigma n_i K_owner^{i0} dS=0",
        "failure_mode": "boundary or improvement source hair",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
    },
    {
        "requirement_id": "M5_no_nonHilbert_current",
        "requirement": "bulk, domain, memory, range, and connection sectors add no unowned source monopole",
        "mathematical_form": "q_retained^0=0 or retained with units/bounds",
        "failure_mode": "mu_extra survives",
        "affected_rows": "R3;R4;R7;R9;R10;R11",
        "current_status": "not_parent_derived",
    },
    {
        "requirement_id": "M6_no_derivative_hair",
        "requirement": "measured source strength has no time, radial, species, frame, or range derivatives",
        "mathematical_form": "partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=0",
        "failure_mode": "Gdot, WEP-source charge, radial hair, or fifth force",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
    },
    {
        "requirement_id": "M7_second_order_source_closure",
        "requirement": "the same measured-GM normalization survives weak-field second order",
        "mathematical_form": "delta_beta_source=0",
        "failure_mode": "PPN beta source residue",
        "affected_rows": "R4;R11",
        "current_status": "not_derived",
    },
]


FAILURE_MODES = [
    {
        "failure_mode": "conserved_but_not_calibrated",
        "construction": "J_H is conserved but Pi_M and G_ref normalization are not fixed",
        "why_it_blocks_Newton": "Newtonian dynamics measures GM, not an arbitrary conserved current",
        "fallback": "P8_Meff_conservation/source-normalization residual row",
        "affected_rows": "R4;R9;R11",
    },
    {
        "failure_mode": "surface_improvement_mass_shift",
        "construction": "T_H -> T_H + nabla B with nonzero int_boundary B",
        "why_it_blocks_Newton": "local conservation survives while the compact monopole shifts",
        "fallback": "boundary/exchange coefficient vector",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
    },
    {
        "failure_mode": "source_charge_calibration_split",
        "construction": "mu_obs(A)=G_eff M_H[A]+mu_extra[A]",
        "why_it_blocks_Newton": "species dependence is physical, not a unit convention",
        "fallback": "P8_species_source_charge and R1 source channel",
        "affected_rows": "R1;R11",
    },
    {
        "failure_mode": "range_or_radial_hair_absorbed_into_GM",
        "construction": "mu_obs(r,lambda)=G_eff M_H + delta_mu(r,lambda)",
        "why_it_blocks_Newton": "finite-range/radial dependence changes force law outside a pure monopole",
        "fallback": "R10 alpha(lambda) curve or radial source residual",
        "affected_rows": "R3;R4;R10;R11",
    },
    {
        "failure_mode": "time_drift_hidden_in_Geff",
        "construction": "G_eff(t)M_eff or memory flux drift is called measured GM",
        "why_it_blocks_Newton": "local Gdot lock is severe and cannot be waived by calibration language",
        "fallback": "Gdot/G residual row",
        "affected_rows": "R9;R11",
    },
    {
        "failure_mode": "Poisson_first_order_only",
        "construction": "first-order Poisson coefficient matches but beta/source nonlinear residue remains",
        "why_it_blocks_Newton": "Newtonian force is not full local GR/PPN completion",
        "fallback": "P8_nonlinear_beta_source_residue",
        "affected_rows": "R4;R11",
    },
]


CONTRACT = [
    {
        "contract_id": "HM0_Hilbert_current_input",
        "required_identity": "ordinary matter source is the Hilbert/coframe current from the same observed matter action",
        "mathematical_form": "J_H derived from T_H^{mu nu}=2/sqrt(-g) delta S_m/delta g_munu",
        "closes_component": "formal source-current input",
        "affected_rows": "R1;R4;R11",
        "current_status": "conditional_from_449",
        "evidence_needed": "one observed coframe and selector-blind matter/source action",
        "fallback_if_missing": "source current remains readout/fitted and no Newton claim",
    },
    {
        "contract_id": "HM1_parent_defined_mass_projector",
        "required_identity": "mass-flux projector is part of the parent source-normalization structure",
        "mathematical_form": "Pi_M J_H appears in S_source_norm before readout/scoring",
        "closes_component": "no post-fit GM mask",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "conditional_no_cheat_contract",
        "evidence_needed": "explicit parent source-normalization term and variation",
        "fallback_if_missing": "measured GM is calibration-only and not derived",
    },
    {
        "contract_id": "HM2_mass_flux_closure",
        "required_identity": "projected Hilbert mass current is closed in the compact local branch",
        "mathematical_form": "d(Pi_M J_H)=0",
        "closes_component": "P8_Meff_conservation",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "conditional_flux_calibration_open",
        "evidence_needed": "Euler equation for Pi_M J_H or source-current Ward closure",
        "fallback_if_missing": "M_eff drift/source-flux residual row",
    },
    {
        "contract_id": "HM3_absolute_monopole_calibration",
        "required_identity": "closed Hilbert mass current has the measured orbital GM normalization",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H",
        "closes_component": "measured-GM normalization",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "surface/integral calibration theorem tied to orbital GM",
        "fallback_if_missing": "conserved current is not measured Newtonian mass",
    },
    {
        "contract_id": "HM4_constant_universal_Geff",
        "required_identity": "G_eff/kappa_eff is constant, universal, and not source/species/range/time dependent",
        "mathematical_form": "G_eff=kappa_eff c^4/(8 pi); partial_{t,r,A,lambda}G_eff=0",
        "closes_component": "Gdot/source/range coupling drift",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant universal coupling identity",
        "fallback_if_missing": "Gdot/source/fifth-force rows remain retained",
    },
    {
        "contract_id": "HM5_zero_mu_extra",
        "required_identity": "all non-Hilbert source contributions vanish, are universal constants, or are retained as residual data",
        "mathematical_form": "mu_extra=mu_boundary+mu_bulk+mu_domain+mu_memory+mu_range+mu_connection=0 or mapped",
        "closes_component": "P8_boundary_bulk_domain_mu_extra; P8_range_dependence; P8_radial_source_hair",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "K_owner formula, zero boundary flux, no-hair, or executable residual coefficients",
        "fallback_if_missing": "P8 residual vector blocks measured-GM/Newton claim",
    },
    {
        "contract_id": "HM6_no_derivative_source_hair",
        "required_identity": "measured source strength is time/radial/species/range/frame independent",
        "mathematical_form": "partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=0",
        "closes_component": "P8_Geff_time_drift; P8_species_source_charge; P8_range_dependence; P8_frame_calibration_split",
        "affected_rows": "R0;R1;R2;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant coupling, source-charge, no-range, and same-frame calibration theorems",
        "fallback_if_missing": "activate row-specific residuals and forbid Newton/local-GR pass",
    },
    {
        "contract_id": "HM7_second_order_source_stability",
        "required_identity": "first-order measured-GM normalization survives PPN beta order",
        "mathematical_form": "delta_beta_source=0",
        "closes_component": "P8_nonlinear_beta_source_residue",
        "affected_rows": "R4;R11",
        "current_status": "not_derived",
        "evidence_needed": "second-order weak-field source calculation",
        "fallback_if_missing": "Poisson-only bridge cannot be local-GR promotion",
    },
    {
        "contract_id": "HM8_empirical_retained_fallback",
        "required_identity": "any nonzero calibration residual is made executable with units, source path, normalization, and row lock",
        "mathematical_form": "dln_Geff_dt, dln_Meff_dt, eta_source_AB, alpha(lambda), partial_r ln mu_obs, mu_extra/(GM)",
        "closes_component": "none; retained-data branch only",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "numeric residual or derived bound",
        "fallback_if_missing": "no measured-GM/Newton/PPN/local-GR claim",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_monopole_theorem_written",
        "pass_condition": "Hilbert source plus closure/calibration/zero-residual premises imply measured GM",
        "current_result": "pass_conditional",
        "evidence": "calibration chain recorded",
    },
    {
        "gate": "conservation_not_overclaimed",
        "pass_condition": "conserved Hilbert current is not treated as measured orbital monopole",
        "current_result": "pass",
        "evidence": "calibration limit and failure modes recorded",
    },
    {
        "gate": "mass_projector_parent_derived",
        "pass_condition": "Pi_M J_H closure and absolute calibration are parent-derived",
        "current_result": "fail",
        "evidence": "A7/HM2/HM3 remain conditional/open",
    },
    {
        "gate": "mu_extra_zero_derived",
        "pass_condition": "boundary/bulk/domain/memory/range/connection residual monopole is theorem-zero or retained below locks",
        "current_result": "fail",
        "evidence": "HM5 remains not_parent_derived",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "mu_obs=G_eff M_H with all derivatives zero",
        "current_result": "fail",
        "evidence": "constant G_eff, flux closure, absolute calibration, and zero hair remain open",
    },
    {
        "gate": "local_GR_promoted",
        "pass_condition": "full R0-R11 vector and EH/PPN source premises are cleared",
        "current_result": "fail",
        "evidence": "monopole calibration gate only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "Hilbert-to-measured-monopole conditional theorem written",
        "status": "pass_conditional",
        "evidence": "calibration chain shows sufficient conditions for mu_obs=G_eff M_H",
    },
    {
        "claim": "GM calibration overclaim blocked",
        "status": "pass",
        "evidence": "conserved current is distinguished from measured orbital monopole",
    },
    {
        "claim": "Hilbert monopole calibration contract written",
        "status": "pass",
        "evidence": str(CONTRACT_PATH),
    },
    {
        "claim": "mass-flux projector parent-derived",
        "status": "fail",
        "evidence": "Pi_M closure and absolute calibration are not derived",
    },
    {
        "claim": "measured GM parent-derived",
        "status": "fail",
        "evidence": "P8 residual components remain open",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "source-normalization and second-order source closure remain retained",
    },
]


DECISION = [
    {
        "decision": "The Hilbert-source-to-measured-monopole gate is now explicit. The conditional bridge is clean: if the Hilbert current is parent-owned, projected by a closed mass-flux operator, absolutely calibrated to the orbital monopole, multiplied by constant universal G_eff, and stripped of boundary/bulk/domain/memory/range/connection residual monopoles, then measured GM follows and the Poisson source is Newtonian at first order. The current corpus does not derive the mass-flux Euler equation, absolute calibration, zero mu_extra, derivative silence, or second-order beta stability. Therefore the source-current progress is real but measured GM, Newton, PPN, and local GR remain unpromoted.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": NEXT_TARGET,
        "why_next": "Pi_M J_H closure plus absolute calibration is the central missing equation for measured GM",
    },
    {
        "rank": 2,
        "target": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "why_next": "even a closed mass current is not Newtonian if G_eff/kappa drifts or carries source dependence",
    },
    {
        "rank": 3,
        "target": "map HM0-HM8 into the P8 residual evaluator",
        "why_next": "failed calibration rows should automatically activate R1/R4/R9/R10/R11 source-normalization tests",
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
            "evidence": "Hilbert monopole calibration contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 3 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "calibration_chain_written",
            "status": "pass" if len(CALIBRATION_CHAIN) == 8 else "fail",
            "evidence": f"{len(CALIBRATION_CHAIN)} calibration chain rows",
        },
        {
            "gate": "monopole_requirements_written",
            "status": "pass" if len(MONOPOLE_REQUIREMENTS) == 8 else "fail",
            "evidence": f"{len(MONOPOLE_REQUIREMENTS)} requirement rows",
        },
        {
            "gate": "failure_modes_written",
            "status": "pass" if len(FAILURE_MODES) == 6 else "fail",
            "evidence": f"{len(FAILURE_MODES)} failure modes",
        },
        {
            "gate": "contract_written",
            "status": "pass",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "conservation_not_overclaimed",
            "status": "pass",
            "evidence": "conserved Hilbert current separated from measured orbital monopole",
        },
        {
            "gate": "mass_projector_parent_derived",
            "status": "fail",
            "evidence": "Pi_M closure and absolute calibration remain open",
        },
        {
            "gate": "absolute_calibration_parent_derived",
            "status": "fail",
            "evidence": "surface/integral calibration to orbital GM is not parent-derived",
        },
        {
            "gate": "mu_extra_zero_derived",
            "status": "fail",
            "evidence": "boundary/bulk/domain/memory/range/connection residual monopoles remain open",
        },
        {
            "gate": "derivative_hair_zero_derived",
            "status": "fail",
            "evidence": "time/radial/species/range/frame derivatives remain contract targets",
        },
        {
            "gate": "second_order_source_stability",
            "status": "fail",
            "evidence": "delta_beta_source not derived",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "HM2-HM7 not all closed",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "measured-GM calibration gate only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "P8 source-normalization and PPN rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 450 - Hilbert Source to Measured Monopole Calibration Gate

Private P8/R1/R4/R9/R10/R11 measured-GM checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 449 gave the useful conditional Hilbert/Ward source-current sublemma. This checkpoint asks the harder Newton question: when is that formal Hilbert current equal to the measured orbital monopole `GM`?

The answer is strict. A conserved Hilbert current helps, but Newton needs a closed, absolutely calibrated mass-flux projector and no hidden boundary, bulk, domain, memory, range, connection, species, radial, or time-dependent source contribution.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Hilbert_source_to_measured_monopole_calibration_gate.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Calibration Chain

{markdown_table(CALIBRATION_CHAIN)}

## 6. Monopole Requirements

{markdown_table(MONOPOLE_REQUIREMENTS)}

## 7. Failure Modes

{markdown_table(FAILURE_MODES)}

## 8. Hilbert-Monopole Calibration Contract

The Hilbert-source-to-measured-monopole calibration contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Gate Tests

{markdown_table(GATE_TESTS)}

## 10. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 11. Gate Results

{markdown_table(gate_results)}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is another good narrowing. The GR/Newton bridge is structurally clean if the parent action can make `Pi_M J_Hilbert` the measured monopole. But right now that equality is still the missing machine, not a theorem. The next best move is to attack the mass-flux projector Euler/calibration equation directly.

## 13. Next Queue

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
    write_csv(results_dir / "calibration_chain.csv", CALIBRATION_CHAIN)
    write_csv(results_dir / "monopole_requirements.csv", MONOPOLE_REQUIREMENTS)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
    write_csv(results_dir / "Hilbert_monopole_calibration_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "conditional_measured_monopole_theorem_written": True,
        "conservation_not_overclaimed": True,
        "Hilbert_current_input_conditional": True,
        "mass_projector_parent_derived": False,
        "absolute_calibration_parent_derived": False,
        "mu_extra_zero_derived": False,
        "derivative_hair_zero_derived": False,
        "second_order_source_stability": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "failure_modes": len(FAILURE_MODES),
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
    parser = argparse.ArgumentParser(description="Write the MTS Hilbert-source-to-measured-monopole calibration gate.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-160000.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
