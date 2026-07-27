from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "parent_source_identity_decomposed_total_conservation_available_Hilbert_PiM_closure_not_derived_radial_template_written_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "parent_source_identity_decomposition_only_no_closed_PiM_flux_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md"

DOC_PATH = Path("499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_SOURCE_REGISTER.csv")
IDENTITY_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv")
RESIDUAL_DECOMPOSITION_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv")
ROUTE_TEST_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ROUTE_TESTS.csv")
RADIAL_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ROUTE_UPDATE.csv")

RADIAL_CALIBRATION_THEOREM_PATH = Path("source-intake/mts_residuals/P8_RADIAL_MEFF_THEOREM_ATTEMPT.csv")
RADIAL_CALIBRATION_GATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_COUPLING_GATES.csv")
PIM_ALGEBRA_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv")
PIM_FLUX_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv")
PIM_VARIATION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv")
HAMILTONIAN_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv")
PG_CALIBRATION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv")
GEFF_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "exact radial residual identity requiring parent source identity",
    },
    {
        "source_file": "497-source-normalization-derived-zero-route-or-numeric-input-template.md",
        "role": "radial and calibration rows selected as theorem-first source-normalization target",
    },
    {
        "source_file": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "Stokes theorem: closed Pi_M flux gives constant M_eff",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M algebra, commutation, and projector variation warning",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "mass-channel Ward/topological/Euler routes and overclaim guards",
    },
    {
        "source_file": "456-PiM-projector-variation-stress-ledger.md",
        "role": "product variation and metric-dependent projector stress ledger",
    },
    {
        "source_file": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "GR-like Hamiltonian boundary-charge route",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Gauss/orbital measured-GM calibration gate",
    },
    {
        "source_file": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "measured-GM absorption guardrails",
    },
    {
        "source_file": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH to Poisson source-normalization pair",
    },
    {
        "source_file": str(RADIAL_CALIBRATION_THEOREM_PATH),
        "role": "498 machine radial theorem attempt rows",
    },
    {
        "source_file": str(RADIAL_CALIBRATION_GATE_PATH),
        "role": "498 machine radial/calibration gate rows",
    },
    {
        "source_file": str(PIM_ALGEBRA_CONTRACT_PATH),
        "role": "454 Pi_M algebra contract",
    },
    {
        "source_file": str(PIM_FLUX_CONTRACT_PATH),
        "role": "455 Pi_M flux closure contract",
    },
    {
        "source_file": str(PIM_VARIATION_CONTRACT_PATH),
        "role": "456 Pi_M projector variation contract",
    },
    {
        "source_file": str(HAMILTONIAN_CONTRACT_PATH),
        "role": "457 Hamiltonian boundary-charge contract",
    },
    {
        "source_file": str(PG_CALIBRATION_CONTRACT_PATH),
        "role": "458 Poisson/Gauss calibration contract",
    },
    {
        "source_file": str(GEFF_CONTRACT_PATH),
        "role": "constant universal G_eff/kappa contract",
    },
    {
        "source_file": "scripts/parent_source_identity_for_closed_PiM_flux_or_radial_template.py",
        "role": "this checkpoint generator",
    },
]


IDENTITY_ATTEMPT_ROWS = [
    {
        "identity_id": "I499_0_total_parent_Ward",
        "identity": "total parent source conservation",
        "mathematical_form": "dJ_tot = 0 on shell, or dJ_tot equals owned Euler terms that vanish on the full parent equations",
        "status": "available_as_total_accounting_conditional",
        "what_it_proves": "the full parent source ledger can conserve total charge",
        "what_it_does_not_prove": "the observed Hilbert mass-channel current Pi_M J_H is separately closed",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "I499_1_split_total_current",
        "identity": "Hilbert plus extra-current split",
        "mathematical_form": "J_tot = J_H + J_extra, with J_extra = J_boundary + J_domain + J_projector + J_bulk + J_nonEH + J_kappa + J_frame",
        "status": "decomposition_written",
        "what_it_proves": "all ways of stealing source-normalization are named",
        "what_it_does_not_prove": "J_extra has zero Pi_M projection",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "I499_2_projected_product_rule",
        "identity": "projected current product rule",
        "mathematical_form": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M]J_H",
        "status": "exact_if_PiM_is_defined_on_the_current_space",
        "what_it_proves": "flux closure splits into a source-current term and a projector-commutator term",
        "what_it_does_not_prove": "the commutator vanishes for metric/domain/Hodge Pi_M",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "I499_3_parent_source_identity",
        "identity": "Hilbert mass closure residual identity",
        "mathematical_form": "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
        "status": "derived_as_decomposition_not_zero",
        "what_it_proves": "the exact obstruction to radial M_eff conservation is the projected extra-current plus Pi_M commutator/anomaly",
        "what_it_does_not_prove": "the obstruction is zero",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "I499_4_closed_flux_sufficient_conditions",
        "identity": "zero theorem conditions",
        "mathematical_form": "Pi_M dJ_extra=0, [d,Pi_M]J_H=0, A_parent=0 => d(Pi_M J_H)=0",
        "status": "conditional_sufficient_theorem",
        "what_it_proves": "the parent proof target is now exact and finite",
        "what_it_does_not_prove": "the current corpus satisfies the target",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "I499_5_radial_integral",
        "identity": "radial hair numerator",
        "mathematical_form": "epsilon_radial_Meff = c_M/M_eff * int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
        "status": "radial_template_formula_written",
        "what_it_proves": "if the zero theorem fails, the exact numerator to bound is known",
        "what_it_does_not_prove": "the numerator is below local bounds",
        "valid_for_claim": "false",
    },
]


RESIDUAL_DECOMPOSITION_ROWS = [
    {
        "residual_id": "S499_0_projector_commutator",
        "obstruction": "[d,Pi_M]J_H or (delta Pi_M)J_H",
        "zero_condition": "Pi_M is parent-derived as metric-independent/topological absolute charge data, or projector stress is theorem-cancelled",
        "current_status": "not_parent_derived",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "fallback_observable": "projector-domain stress; radial source hair; nonEH operator vector",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_1_boundary_improvement",
        "obstruction": "Pi_M dJ_boundary or boundary owner flux",
        "zero_condition": "compact boundary mass flux is zero or a universal derivative-silent constant calibration",
        "current_status": "fail_open",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "fallback_observable": "boundary monopole shift; alpha3; xi; Gdot; beta source hair",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_2_domain_projector",
        "obstruction": "Pi_M dJ_domain plus domain/homology representative variation",
        "zero_condition": "domain selector is topological/covariant and carries no mass projection, vector, anisotropy, or time/range derivative",
        "current_status": "not_parent_derived",
        "affected_rows": "R5;R6;R7;R8;R9;R11",
        "fallback_observable": "preferred-frame/location rows and domain source-normalization coefficient",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_3_bulk_memory_or_X",
        "obstruction": "Pi_M dJ_bulk or finite-range memory/X exchange",
        "zero_condition": "mass-gap/no-source theorem or zero Pi_M projection of bulk exchange",
        "current_status": "not_derived_numeric_curve_preferred",
        "affected_rows": "R4;R10;R11",
        "fallback_observable": "alpha(lambda) curve and radial/range source-normalization",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_4_nonEH_operator",
        "obstruction": "Pi_M dJ_nonEH and non-EH source residual S_res",
        "zero_condition": "same-frame local exterior is metric-only EH plus Lambda or coefficients are bounded",
        "current_status": "conditional_not_parent_derived",
        "affected_rows": "R3;R4;R10;R11",
        "fallback_observable": "gamma/beta/fifth-force/operator residual vector",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_5_coupling_drift",
        "obstruction": "Pi_M(T_obs d kappa_eff) or running G_eff",
        "zero_condition": "constant universal parent kappa/G_eff with no time, range, species, radial, or frame derivative",
        "current_status": "conditional_not_parent_derived",
        "affected_rows": "R1;R4;R9;R10;R11",
        "fallback_observable": "Gdot; source-charge; radial/range dependent measured-GM",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_6_frame_species_source",
        "obstruction": "J_H is not the same measured source current for all observed matter",
        "zero_condition": "same observed coframe and selector-blind source-current theorem",
        "current_status": "not_parent_derived",
        "affected_rows": "R0;R1;R2;R11",
        "fallback_observable": "WEP/source eta, clock/frame residuals",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "S499_7_parent_anomaly_or_multiplier",
        "obstruction": "A_parent from unowned lambda_M, readout mask, or non-gauge source-normalization multiplier",
        "zero_condition": "multiplier is first-class/gauge/topological/Ward-owned, or no multiplier is used",
        "current_status": "not_satisfied",
        "affected_rows": "R1;R4;R7;R9;R11",
        "fallback_observable": "closure-only radial residual; no derivation credit",
        "valid_for_claim": "false",
    },
]


ROUTE_TEST_ROWS = [
    {
        "route_id": "RT499_0_total_Ward_only",
        "route": "use total Ward conservation alone",
        "test_result": "rejected_for_Hilbert_mass_closure",
        "reason": "dJ_tot=0 allows exchange between observed Hilbert mass and hidden/source sectors",
        "next_action": "must prove zero Pi_M projection of J_extra",
        "valid_for_claim": "false",
    },
    {
        "route_id": "RT499_1_topological_PiM",
        "route": "derive Pi_M as metric-independent absolute cohomology charge and close total mass current",
        "test_result": "promising_but_not_in_corpus",
        "reason": "would kill commutator/projector stress, but still needs on-shell equality to Hilbert measured current",
        "next_action": NEXT_TARGET,
        "valid_for_claim": "false",
    },
    {
        "route_id": "RT499_2_Hamiltonian_charge",
        "route": "use observed-time Hamiltonian boundary charge",
        "test_result": "conditional_downstream_of_EH_boundary_calibration",
        "reason": "clean GR route, but EH constraint algebra, charge equality, extra-charge silence, and Gauss calibration are not parent-derived",
        "next_action": "retain as route after EH/local-boundary action improves",
        "valid_for_claim": "false",
    },
    {
        "route_id": "RT499_3_Euler_multiplier",
        "route": "vary lambda_M to impose d(Pi_M J_H)=0",
        "test_result": "closure_only_unless_independently_owned",
        "reason": "mathematically sufficient but explanatory only if lambda_M has gauge/topological/Ward origin and no unowned stress",
        "next_action": "do not use as derivation without parent origin",
        "valid_for_claim": "false",
    },
    {
        "route_id": "RT499_4_numeric_radial_template",
        "route": "fill the exact radial source-current numerator",
        "test_result": "fallback_required_if_theorem_rows_stay_open",
        "reason": "keeps theory testable without pretending local Newton is derived",
        "next_action": "build radial bound runner if 500 topological route fails",
        "valid_for_claim": "false",
    },
]


RADIAL_TEMPLATE_ROWS = [
    {
        "template_id": "T499_0_identity_integral",
        "required_quantity": "I_parent_radial",
        "definition": "int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
        "required_columns": "system_id;r1;r2;c_M;M_eff_ref;I_parent_radial;norm_convention;units;source_file;assumptions",
        "maps_to": "epsilon_radial_Meff = c_M * I_parent_radial / M_eff_ref",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "T499_1_commutator_profile",
        "required_quantity": "I_commutator",
        "definition": "int_A_ext [d,Pi_M]J_H",
        "required_columns": "system_id;projector_type;metric_dependence_flag;I_commutator;units;source_file;assumptions",
        "maps_to": "projector stress and radial/source-normalization rows",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "T499_2_extra_channel_integrals",
        "required_quantity": "I_extra_by_channel",
        "definition": "int_A_ext Pi_M dJ_extra separated by boundary/domain/bulk/nonEH/kappa/frame/species",
        "required_columns": "system_id;channel;I_extra;units;affected_rows;source_file;assumptions",
        "maps_to": "mu_extra channel vector and R4/R9/R10/R11 residuals",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "T499_3_observable_bound",
        "required_quantity": "radial_measured_GM_bound",
        "definition": "dln_mu_dlnr or finite shell Delta mu/mu inferred from local/orbital data",
        "required_columns": "system_id;r;mu_obs_or_proxy;dln_mu_dlnr;bound_source;units;source_file;assumptions",
        "maps_to": "R4 beta/source hair and R10 fifth-force/radial profile",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D499_0_identity",
        "status": "decomposition_derived_not_zero",
        "meaning": "the parent source identity reduces closed Hilbert Pi_M flux to zero projected extra-current plus zero projector commutator/anomaly",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D499_1_total_conservation",
        "status": "insufficient",
        "meaning": "total Ward conservation can conserve the whole ledger but does not prove the observed Hilbert mass channel is closed",
        "next_action": "derive zero Pi_M projection of extra channels or retain radial residuals",
    },
    {
        "decision_id": "D499_2_topological_route",
        "status": "best_derivation_route",
        "meaning": "a metric-independent topological Pi_M current could kill the commutator and avoid Hodge projector stress, but it is not yet in the corpus",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D499_3_radial_template",
        "status": "written_unfilled",
        "meaning": "if the topological/source theorem fails, the exact radial numerator is ready to become a numeric/source-backed bound",
        "next_action": "build bound runner only after the theorem-first 500 attempt",
    },
    {
        "decision_id": "D499_4_promotion",
        "status": "forbidden",
        "meaning": "no closed Pi_M flux, mu_extra zero, Newtonian recovery, PPN pass, or local-GR pass is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PARENT_SOURCE_IDENTITY",
        "previous_status": "closed_PiM_flux_parent_derived_false",
        "new_status": "identity_decomposed_total_conservation_not_Hilbert_closure",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RADIAL_MEFF_HAIR",
        "previous_status": "exact_residual_identity_written_parent_closed_flux_missing",
        "new_status": "radial_numerator_split_into_extra_current_commutator_anomaly",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "TOPOLOGICAL_PIM",
        "previous_status": "conditional_promising_route",
        "new_status": "best_next_derivation_target_for_commutator_zero_and_stress_silence",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_by_parent_source_identity_and_calibration_lock",
        "new_status": "still_blocked_by_extra_current_commutator_calibration_and_PPN_source_stability",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        source_file = row["source_file"]
        rows.append(
            {
                **row,
                "exists": str((ROOT / source_file).exists()),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    radial_rows = read_csv(RADIAL_CALIBRATION_THEOREM_PATH)
    radial_gates = read_csv(RADIAL_CALIBRATION_GATE_PATH)
    pim_flux_rows = read_csv(PIM_FLUX_CONTRACT_PATH)
    pim_variation_rows = read_csv(PIM_VARIATION_CONTRACT_PATH)
    hamiltonian_rows = read_csv(HAMILTONIAN_CONTRACT_PATH)
    pg_rows = read_csv(PG_CALIBRATION_CONTRACT_PATH)

    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_identity_rows = [row for row in IDENTITY_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_residual_rows = [row for row in RESIDUAL_DECOMPOSITION_ROWS if row["valid_for_claim"] == "true"]
    claim_route_rows = [row for row in ROUTE_TEST_ROWS if row["valid_for_claim"] == "true"]
    claim_template_rows = [row for row in RADIAL_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    required_residuals = {
        "S499_0_projector_commutator",
        "S499_1_boundary_improvement",
        "S499_2_domain_projector",
        "S499_3_bulk_memory_or_X",
        "S499_4_nonEH_operator",
        "S499_5_coupling_drift",
        "S499_6_frame_species_source",
        "S499_7_parent_anomaly_or_multiplier",
    }
    residual_ids = {row["residual_id"] for row in RESIDUAL_DECOMPOSITION_ROWS}

    return [
        {
            "rule_id": "V499_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V499_1_prior_contracts_loaded",
            "rule": "498 radial rows and PiM/Hamiltonian/PG contracts are loaded",
            "result": "pass"
            if radial_rows and radial_gates and pim_flux_rows and pim_variation_rows and hamiltonian_rows and pg_rows
            else "fail",
            "evidence": f"radial_rows={len(radial_rows)};radial_gates={len(radial_gates)};FC={len(pim_flux_rows)};PV={len(pim_variation_rows)};HC={len(hamiltonian_rows)};PG={len(pg_rows)}",
            "claim_effect": "499 tied to prior gates",
        },
        {
            "rule_id": "V499_2_identity_decomposition",
            "rule": "identity attempt includes total Ward, split, product rule, obstruction identity, zero conditions, and radial integral",
            "result": "pass" if len(IDENTITY_ATTEMPT_ROWS) == 6 else "fail",
            "evidence": f"identity_rows={len(IDENTITY_ATTEMPT_ROWS)}",
            "claim_effect": "decomposition concrete",
        },
        {
            "rule_id": "V499_3_residual_coverage",
            "rule": "residual decomposition covers commutator, boundary, domain, bulk, nonEH, coupling, frame/species, and anomaly channels",
            "result": "pass" if required_residuals.issubset(residual_ids) else "fail",
            "evidence": ";".join(sorted(residual_ids)),
            "claim_effect": "no hidden source channel",
        },
        {
            "rule_id": "V499_4_radial_template",
            "rule": "fallback radial template contains identity integral, commutator profile, extra-channel integrals, and observable bound rows",
            "result": "pass" if len(RADIAL_TEMPLATE_ROWS) == 4 else "fail",
            "evidence": f"template_rows={len(RADIAL_TEMPLATE_ROWS)}",
            "claim_effect": "test branch ready but unfilled",
        },
        {
            "rule_id": "V499_5_no_false_claims",
            "rule": "no identity, residual, route, or template row is claim-valid",
            "result": "pass" if not claim_identity_rows and not claim_residual_rows and not claim_route_rows and not claim_template_rows else "fail",
            "evidence": f"identity_claims={len(claim_identity_rows)};residual_claims={len(claim_residual_rows)};route_claims={len(claim_route_rows)};template_claims={len(claim_template_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 499 - Parent Source Identity For Closed PiM Flux Or Radial Template

Private source-normalization checkpoint. This is not a public closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `498` made the radial source-normalization obstruction exact:

```text
epsilon_radial_Meff is proportional to int_A_ext d(Pi_M J).
```

This checkpoint asks whether the parent action can force:

```text
d(Pi_M J_H)=0
```

or whether the row must become a radial source-current template.

Short answer:

```text
Total parent conservation can be written as bookkeeping.
That is not enough.

The useful identity is:

d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.

So closed Hilbert Pi_M flux follows only if the projected extra-current,
projector commutator, and parent anomaly/multiplier terms vanish.

The current corpus has not proved those vanish.
The exact radial fallback template is now written.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_source_identity_for_closed_PiM_flux_or_radial_template.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Parent Source Identity Attempt

The key distinction is:

```text
dJ_tot = 0
```

does not imply:

```text
d(Pi_M J_H)=0.
```

The local Newton branch needs the second equation, because orbits read the observed Hilbert/measured mass channel, not an arbitrary conserved total charge containing hidden boundary/domain/projector pieces.

{markdown_table(IDENTITY_ATTEMPT_ROWS)}

## 5. Residual Decomposition

The obstruction has now been split into the source-normalization rows that would have to vanish or be numerically bounded:

{markdown_table(RESIDUAL_DECOMPOSITION_ROWS)}

## 6. Route Tests

{markdown_table(ROUTE_TEST_ROWS)}

## 7. Radial Template

If the theorem route fails, the fallback is no longer vague:

```text
epsilon_radial_Meff
  = c_M I_parent_radial / M_eff_ref
```

with:

```text
I_parent_radial = int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent].
```

{markdown_table(RADIAL_TEMPLATE_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The parent source identity has been reduced to an exact decomposition.
Closed Hilbert Pi_M flux requires zero projected extra-current, zero projector commutator, and zero parent anomaly/multiplier source.
The radial fallback template is now explicit.
```

Forbidden:

```text
MTS has derived d(Pi_M J_H)=0.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | topological Pi_M is the best remaining derivation route because it can kill the commutator/projector-stress obstruction without using a Hodge metric projector |
| 2 | radial bound runner | if the topological route fails, fill `I_parent_radial` and map it to local radial/source-normalization bounds |
| 3 | parent-fixed calibration lock | even closed flux still needs charge-to-Hilbert-mass and constant universal coupling |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-parent-source-identity-for-closed-PiM-flux-or-radial-template"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (IDENTITY_ATTEMPT_PATH, IDENTITY_ATTEMPT_ROWS),
        (RESIDUAL_DECOMPOSITION_PATH, RESIDUAL_DECOMPOSITION_ROWS),
        (ROUTE_TEST_PATH, ROUTE_TEST_ROWS),
        (RADIAL_TEMPLATE_PATH, RADIAL_TEMPLATE_ROWS),
        (VALIDATION_PATH, validations),
        (DECISION_PATH, DECISION_ROWS),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "identity_attempt": str(ROOT / IDENTITY_ATTEMPT_PATH),
        "residual_decomposition": str(ROOT / RESIDUAL_DECOMPOSITION_PATH),
        "route_tests": str(ROOT / ROUTE_TEST_PATH),
        "radial_template": str(ROOT / RADIAL_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "identity_rows": len(IDENTITY_ATTEMPT_ROWS),
        "residual_rows": len(RESIDUAL_DECOMPOSITION_ROWS),
        "route_test_rows": len(ROUTE_TEST_ROWS),
        "radial_template_rows": len(RADIAL_TEMPLATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "parent_identity_decomposed": True,
        "total_conservation_available": True,
        "Hilbert_PiM_flux_closed_parent_derived": False,
        "projected_extra_current_zero_derived": False,
        "projector_commutator_zero_derived": False,
        "parent_anomaly_zero_derived": False,
        "epsilon_radial_Meff_zero_derived": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
