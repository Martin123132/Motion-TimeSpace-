from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_extra_sector_Hamiltonian_charge_silence_failed_current_claim_Cextra_channel_fill_written"
CLAIM_CEILING = "Cextra_Hamiltonian_charge_silence_attempt_only_no_radial_closure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md"

DOC_PATH = Path("556-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_556_SOURCE_REGISTER.csv")
SILENCE_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_SILENCE_ATTEMPT.csv")
CHANNEL_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv")
BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_556_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_556_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_556_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_556_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "555-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill.md",
        "role": "radial C-term closure failure selecting C_extra as next target",
    },
    {
        "source_file": "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
        "role": "Hamiltonian charge integrability/source equality failures",
    },
    {
        "source_file": "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
        "role": "Hamiltonian PiM repair residual decomposition",
    },
    {
        "source_file": "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "role": "Y5 extra-mass projection silence theorem and channelwise inputs",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator route for extra-sector silence",
    },
    {
        "source_file": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "role": "field-specific extra-sector silence acceptance gates",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "mu_extra owner ledger and source-normalization coefficient vector",
    },
    {
        "source_file": "468-mu-extra-coefficient-vector-to-local-bound-scorecard.md",
        "role": "mu_extra coefficient vector scorecard",
    },
    {
        "source_file": "469-fill-or-zero-highest-pressure-mu-extra-row.md",
        "role": "highest-pressure mu_extra fill/zero attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_DECOMPOSITION.csv",
        "role": "555 radial C-term decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_BOUND_FILL_ROW.csv",
        "role": "555 radial C-term fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_555_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv",
        "role": "522 extra-mass projection silence theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
        "role": "522 extra-mass channelwise required bound inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv",
        "role": "522 extra-mass observable map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_VALIDATION.csv",
        "role": "522 extra-mass validation",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
        "role": "506 positive operator/no-hair identity templates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
        "role": "local-zero extra premise requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
        "role": "field-specific silence acceptance gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SECTOR_SILENCE_STATUS.csv",
        "role": "sector-by-sector silence status",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "role": "mu_extra channel owner ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
        "role": "mu_extra channel bound summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "mu_extra source-normalization coefficient vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
        "role": "domain/projector coefficient inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv",
        "role": "boundary coefficient inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv",
        "role": "R11 source-normalization link",
    },
    {
        "source_file": "scripts/Y5_extra_sector_Hamiltonian_charge_silence_or_channel_fill.py",
        "role": "this checkpoint generator",
    },
]


SILENCE_ATTEMPT_ROWS = [
    {
        "step_id": "HEC556_0_target",
        "claim": "all non-EH extra sectors carry zero Hamiltonian mass charge through the compact source-free annulus",
        "mathematical_form": "C_extra=sum_i C_i^extra=0 in A",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a parent-action theorem-zero certificate",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_1_Noether_split",
        "claim": "the annulus leakage can be split into independently-owned extra-sector charge channels",
        "mathematical_form": "int_A C_extra = sum_i int_A Pi_M^H dJ_i^extra + possible owned anomaly terms",
        "current_result": "identity_route_available",
        "why_not_enough": "the split names channels but does not zero or numerically bound them",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_2_positive_operator_route",
        "claim": "field-specific positive source-free operators can silence extra sectors",
        "mathematical_form": "int_A <X,L_X X> = norm_positive[X] + boundary_flux; source=boundary_flux=0 => X=0/pure gauge/topological constant",
        "current_result": "conditional_reference",
        "why_not_enough": "current corpus has the gate, not the field-specific operators, signs, masses, source charges, and boundary values",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_3_rebasis_guardrail",
        "claim": "old mu_extra channels must be re-bucketed so C_boundary, C_projector, and C_ref are not double-counted as C_extra",
        "mathematical_form": "epsilon_extra_old -> {C_extra_core,C_boundary,C_projector,C_ref,source_equality}",
        "current_result": "guardrail_pass",
        "why_not_enough": "guardrail prevents double counting but does not close C_extra_core",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_4_bulk_memory_range",
        "claim": "bulk, memory, range, and motion/time-flow modes are silent in the local exterior",
        "mathematical_form": "C_bulk+C_memory+C_range+C_motion_time=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "no source-backed Yukawa/range profile or positive operator zero certificate is available",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_5_nonEH_kappa_frame_species",
        "claim": "non-EH operator, kappa drift, frame/species source, and source-normalization channels have zero Hamiltonian projection",
        "mathematical_form": "C_nonEH+C_kappa+C_frame_species=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "R11 operator vector, same-frame source charge, and derivative hair rows remain unfilled",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_6_parent_anomaly_no_cancellation",
        "claim": "any remaining parent anomaly/multiplier term is zero by identity, not by cancellation",
        "mathematical_form": "A_parent=0 and |C_extra| <= sum_i |C_i|",
        "current_result": "fail_current_claim",
        "why_not_enough": "no parent Ward identity or anomaly-zero certificate is supplied; cancellation credit is forbidden",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HEC556_7_verdict",
        "claim": "C_extra_over_MH can be set to zero in FB555_0",
        "mathematical_form": "C_extra_over_MH=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "all core extra channels remain theorem-zero missing or source-backed bound missing",
        "valid_for_claim": "false",
    },
]


CHANNEL_MAP_ROWS = [
    {
        "map_id": "HECM556_0_boundary_improvement",
        "prior_channel": "EX522_0_boundary_improvement",
        "symbol": "epsilon_boundary",
        "radial_bucket": "C_boundary/C_ref_not_Cextra_core",
        "Hamiltonian_charge_risk": "finite boundary/reference mass shift can mimic measured monopole",
        "required_zero_or_bound": "boundary nohair/no-flux or fixed reference subtraction with derivatives zero",
        "current_status": "open_elsewhere_not_counted_in_Cextra_core",
        "next_required_artifact": "boundary/reference residual rows already retained",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_1_domain_projector",
        "prior_channel": "EX522_1_domain_projector",
        "symbol": "epsilon_domain_projector",
        "radial_bucket": "mixed_Cextra_core_and_C_projector",
        "Hamiltonian_charge_risk": "domain selector stress or projector variation creates preferred-frame/source-normalization hair",
        "required_zero_or_bound": "domain stress zero plus Pi_M commutator/projector zero or executable coefficient vector",
        "current_status": "not_derived_not_filled",
        "next_required_artifact": "P8_mu_extra_domain_projector_coefficients.csv plus R11 executable vector",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_2_bulk_memory_range",
        "prior_channel": "EX522_2_bulk_memory_range",
        "symbol": "epsilon_bulk_X",
        "radial_bucket": "Cextra_core",
        "Hamiltonian_charge_risk": "massive/light tail or memory exchange carries finite-range fifth-force/radial charge",
        "required_zero_or_bound": "positive source-free mass-gap/no-hair theorem or source-backed alpha(lambda) curve",
        "current_status": "not_derived_not_filled",
        "next_required_artifact": NEXT_TARGET,
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_3_nonEH_operator",
        "prior_channel": "EX522_3_nonEH_operator",
        "symbol": "epsilon_nonEH_source",
        "radial_bucket": "Cextra_core/C_EH_interface",
        "Hamiltonian_charge_risk": "non-EH weak-field operators alter the source potential or PPN coefficients",
        "required_zero_or_bound": "EH-only reduction or complete R11 coefficient vector below local locks",
        "current_status": "not_derived_not_filled",
        "next_required_artifact": "R11 non-EH operator vector with units and weak-field map",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_4_coupling_drift",
        "prior_channel": "EX522_4_coupling_drift",
        "symbol": "epsilon_time_drift",
        "radial_bucket": "Cextra_core/C_EH_interface",
        "Hamiltonian_charge_risk": "kappa/G_eff/time drift leaks into Hamiltonian mass normalization",
        "required_zero_or_bound": "constant-kappa superselection plus dln_Meff_dt zero or source-backed Gdot bound",
        "current_status": "conditional_not_derived_here",
        "next_required_artifact": "time-drift residual or theorem-zero row",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_5_frame_species_source",
        "prior_channel": "EX522_5_frame_species_source",
        "symbol": "epsilon_species_A",
        "radial_bucket": "Cextra_core/source_equality_interface",
        "Hamiltonian_charge_risk": "species/frame-dependent source charge breaks one observed-frame source equality",
        "required_zero_or_bound": "same coframe/source theorem plus WEP/source-charge residual below lock",
        "current_status": "same_coframe_partial_not_Hamiltonian_source_derived",
        "next_required_artifact": "same-frame source equality certificate or WEP source-charge vector",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_6_projector_stress",
        "prior_channel": "EX522_6_projector_stress",
        "symbol": "Delta_PiM",
        "radial_bucket": "C_projector_not_Cextra_core",
        "Hamiltonian_charge_risk": "projector variation shifts mass charge through the annulus",
        "required_zero_or_bound": "Hamiltonian PiM equality plus projector commutator/symplectic silence",
        "current_status": "open_elsewhere_not_counted_in_Cextra_core",
        "next_required_artifact": "projector commutator and old/new PiM equivalence rows",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_7_parent_anomaly_multiplier",
        "prior_channel": "EX522_7_parent_anomaly_multiplier",
        "symbol": "A_parent",
        "radial_bucket": "Cextra_core",
        "Hamiltonian_charge_risk": "unowned parent multiplier/anomaly term can source radial closure failure",
        "required_zero_or_bound": "parent Ward/Noether anomaly-zero identity or retained anomaly coefficient",
        "current_status": "not_satisfied",
        "next_required_artifact": "parent anomaly zero certificate or A_parent coefficient row",
        "valid_for_claim": "false",
    },
    {
        "map_id": "HECM556_8_absolute_calibration",
        "prior_channel": "EX522_8_absolute_calibration",
        "symbol": "epsilon_calibration",
        "radial_bucket": "C_ref/source_equality_not_Cextra_core",
        "Hamiltonian_charge_risk": "absolute offset may be harmless only if universal and derivative-free",
        "required_zero_or_bound": "fixed reference/source calibration with no time/radial/species/range dependence",
        "current_status": "conditional_harmless_not_parent_fixed",
        "next_required_artifact": "reference/source-equality calibration row",
        "valid_for_claim": "false",
    },
]


BOUND_FILL_ROWS = [
    {
        "fill_id": "FB556_0_HPiM_Cextra_core_channel_bound",
        "residual_component": "C_extra_over_MH",
        "formula": "abs(epsilon_domain_stress_over_MH)+abs(epsilon_bulk_memory_range_over_MH)+abs(epsilon_nonEH_operator_over_MH)+abs(epsilon_kappa_drift_over_MH)+abs(epsilon_frame_species_over_MH)+abs(A_parent_over_MH)+abs(epsilon_motion_time_flow_over_MH)",
        "epsilon_domain_stress_over_MH": "MISSING_DOMAIN_STRESS_ZERO_OR_BOUND",
        "epsilon_bulk_memory_range_over_MH": "MISSING_BULK_MEMORY_RANGE_ZERO_OR_YUKAWA_BOUND",
        "epsilon_nonEH_operator_over_MH": "MISSING_NONEH_OPERATOR_ZERO_OR_R11_VECTOR",
        "epsilon_kappa_drift_over_MH": "MISSING_KAPPA_DRIFT_ZERO_OR_GDOT_BOUND",
        "epsilon_frame_species_over_MH": "MISSING_FRAME_SPECIES_SOURCE_ZERO_OR_WEP_BOUND",
        "A_parent_over_MH": "MISSING_PARENT_ANOMALY_ZERO_OR_BOUND",
        "epsilon_motion_time_flow_over_MH": "MISSING_MOTION_TIME_FLOW_ZERO_OR_BOUND",
        "excluded_no_double_count": "epsilon_boundary->C_boundary/C_ref;Delta_PiM->C_projector;epsilon_calibration->C_ref/source_equality",
        "mapped_lock_rows": "R1_WEP_source_charge;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "bound_rule": "each Cextra core channel must pass individually or theorem-zero; no cancellation credit and no double counting with C_boundary/C_projector/C_ref",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_Cextra_charge_silence_failure",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "HEO556_0_field_specific_operator_missing",
        "obstruction": "positive source-free silence route exists only as a template; individual extra fields lack signed operators, masses, source charges, and boundary conditions",
        "activated_residual": "C_extra_over_MH",
        "repair": "write field-specific Euler/Noether operator and energy identity for each core extra channel",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HEO556_1_bulk_memory_range_unfilled",
        "obstruction": "bulk/memory/range tails are not theorem-zero and have no source-backed Yukawa/fifth-force coefficient curve",
        "activated_residual": "epsilon_bulk_memory_range_over_MH;R10_fifth_force",
        "repair": "attempt positive operator mass-gap/no-hair theorem or fill alpha(lambda) curve",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HEO556_2_nonEH_R11_open",
        "obstruction": "non-EH operator/source-normalization channel lacks an executable R11 coefficient vector",
        "activated_residual": "epsilon_nonEH_operator_over_MH;R11_EH_operator_ledger",
        "repair": "derive EH-only local operator or fill R11 vector with units, normalization, and weak-field map",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HEO556_3_frame_species_open",
        "obstruction": "same observed-frame source equality is not strong enough to remove species/frame-dependent Hamiltonian source charge",
        "activated_residual": "epsilon_frame_species_over_MH;R1_WEP_source_charge",
        "repair": "derive same-coframe source theorem or fill WEP/source-charge residual vector",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HEO556_4_anomaly_no_Ward_identity",
        "obstruction": "parent anomaly/multiplier term has no Ward or Noether zero certificate",
        "activated_residual": "A_parent_over_MH",
        "repair": "prove A_parent=0 from the parent action or keep a source-backed anomaly coefficient",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HEO556_5_no_promotion_from_rebasis",
        "obstruction": "rebucketing channels avoids double counting but does not make any Cextra core term vanish",
        "activated_residual": "epsilon_HPiM_radial_closure_abs;epsilon_HPiM_total_abs",
        "repair": "close Cextra core plus C_EH/C_projector/C_boundary/C_ref before promoting radial closure",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D556_0_Cextra_zero_failed",
        "status": "extra_sector_Hamiltonian_charge_silence_not_signed",
        "meaning": "current MTS cannot yet set C_extra_over_MH to zero",
        "claim_status": "C_extra_over_MH_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D556_1_rebasis_done",
        "status": "old_extra_mass_channels_rebucketed",
        "meaning": "boundary/projector/reference channels are separated from Cextra core to avoid double counting",
        "claim_status": "guardrail_pass_not_theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D556_2_fill_row_written",
        "status": "Cextra_core_channel_fill_row_written_unfilled",
        "meaning": "C_extra now has explicit core channel placeholders rather than one broad missing symbol",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D556_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no radial closure, source-measure, measured-GM, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D556_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_EXTRA_CHARGE_SILENCE",
        "previous_status": "next_highest_pressure_radial_Cterm_channel",
        "new_status": "attempted_failed_current_claim_Cextra_channel_fill_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_RADIAL_CLOSURE",
        "previous_status": "attempted_failed_current_claim_Cterm_fill_row_written",
        "new_status": "still_failed_Cextra_core_not_zero_or_bounded",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_EXTRA_MASS_PROJECTION",
        "previous_status": "silence_theorem_written_channelwise_bound_inputs_written_no_zero_derived",
        "new_status": "rebucketed_into_Hamiltonian_Cterm_basis_no_channel_pass",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_radial_closure_also_not_signed",
        "new_status": "still_blocked_extra_charge_silence_not_signed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_radial_Cterm_zero_not_signed",
        "new_status": "closure_only_Cextra_not_zero_or_bounded",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def evaluator_rows() -> list[dict[str, Any]]:
    return [
        {
            "fill_id": row["fill_id"],
            "residual_component": row["residual_component"],
            "numeric_status": "not_computed_missing_theorem_zero_or_source_backed_values",
            "mapped_lock_rows": row["mapped_lock_rows"],
            "pass_status": "not_claimable",
            "valid_for_claim": "false",
            "notes": "fill only with theorem-zero certificates or source-backed Cextra core channel coefficients; excluded channels stay in C_boundary/C_projector/C_ref",
        }
        for row in BOUND_FILL_ROWS
    ]


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_555_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    radial_decomp = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_DECOMPOSITION.csv"))
    radial_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_BOUND_FILL_ROW.csv"))
    extra_theorem = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv"))
    extra_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"))
    extra_map = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv"))
    extra_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_VALIDATION.csv"))
    energy_identity = read_csv(Path("source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"))
    premise_requirements = read_csv(Path("source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv"))
    acceptance_gates = read_csv(Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv"))
    sector_status = read_csv(Path("source-intake/mts_residuals/P8_MTS_SECTOR_SILENCE_STATUS.csv"))
    owner_ledger = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv"))
    bound_summary = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv"))
    coefficient_vector = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv"))
    domain_coefficients = read_csv(Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv"))
    boundary_coefficients = read_csv(Path("source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv"))
    r11_link = read_csv(Path("source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv"))
    claim_attempt_rows = [row for row in SILENCE_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_map_rows = [row for row in CHANNEL_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V556_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V556_1_prior_555_clean",
            "result": "pass" if len(prior_validation) == 10 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V556_2_radial_Cterm_context_loaded",
            "result": "pass" if len(radial_decomp) == 6 and len(radial_fill) == 1 else "fail",
            "detail": f"radial_decomp={len(radial_decomp)};radial_fill={len(radial_fill)}",
        },
        {
            "check_id": "V556_3_Y5_extra_mass_evidence_loaded",
            "result": "pass" if len(extra_theorem) == 5 and len(extra_inputs) == 9 and len(extra_map) == 4 and len(extra_validation) == 7 else "fail",
            "detail": f"extra_theorem={len(extra_theorem)};extra_inputs={len(extra_inputs)};extra_map={len(extra_map)};extra_validation={len(extra_validation)}",
        },
        {
            "check_id": "V556_4_silence_gate_evidence_loaded",
            "result": "pass" if len(energy_identity) == 4 and len(premise_requirements) == 5 and len(acceptance_gates) == 3 and len(sector_status) == 6 else "fail",
            "detail": f"energy_identity={len(energy_identity)};premises={len(premise_requirements)};acceptance_gates={len(acceptance_gates)};sector_status={len(sector_status)}",
        },
        {
            "check_id": "V556_5_mu_extra_vector_evidence_loaded",
            "result": "pass" if len(owner_ledger) == 8 and len(bound_summary) == 8 and len(coefficient_vector) == 8 and len(domain_coefficients) == 5 and len(boundary_coefficients) == 4 and len(r11_link) == 8 else "fail",
            "detail": f"owner_ledger={len(owner_ledger)};bound_summary={len(bound_summary)};coefficient_vector={len(coefficient_vector)};domain={len(domain_coefficients)};boundary={len(boundary_coefficients)};r11_link={len(r11_link)}",
        },
        {
            "check_id": "V556_6_attempt_and_channel_map_complete",
            "result": "pass" if len(SILENCE_ATTEMPT_ROWS) == 8 and len(CHANNEL_MAP_ROWS) == 9 else "fail",
            "detail": f"attempt_rows={len(SILENCE_ATTEMPT_ROWS)};channel_map_rows={len(CHANNEL_MAP_ROWS)}",
        },
        {
            "check_id": "V556_7_fill_row_written",
            "result": "pass" if len(BOUND_FILL_ROWS) == 1 and len(eval_rows) == 1 else "fail",
            "detail": f"fill_rows={len(BOUND_FILL_ROWS)};evaluator_rows={len(eval_rows)}",
        },
        {
            "check_id": "V556_8_no_claim_rows",
            "result": "pass" if not claim_attempt_rows and not claim_map_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": f"claim_attempt={len(claim_attempt_rows)};claim_map={len(claim_map_rows)};claim_fill={len(claim_fill_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V556_9_no_overclaim",
            "result": "pass" if not claim_attempt_rows and not claim_map_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": "Cextra_zero_signed=false; radial_closure=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 556 - Y5 Extra-Sector Hamiltonian Charge Silence or Channel Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

`C_extra` does not vanish for current MTS.

This is not a new catastrophe; it is the same old extra-mass problem pushed into the sharper Hamiltonian annulus language. The useful improvement is that `C_extra` is no longer one mystery bucket. It is now split into core channels, while boundary/projector/reference pieces are explicitly excluded to avoid double counting:

```text
C_extra_core =
  C_domain_stress + C_bulk_memory_range + C_nonEH_operator
  + C_kappa_drift + C_frame_species + A_parent
  + C_motion_time_flow.
```

Every one of those needs a theorem-zero certificate or a source-backed coefficient row before radial closure can pass.

## 2. Hamiltonian Extra-Charge Silence Attempt

{markdown_table(SILENCE_ATTEMPT_ROWS)}

## 3. Channel Re-Basis Map

{markdown_table(CHANNEL_MAP_ROWS)}

## 4. First Cextra Fill Row

{markdown_table(BOUND_FILL_ROWS)}

## 5. Evaluator

{markdown_table(eval_rows)}

## 6. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has attempted extra-sector Hamiltonian charge silence.
MTS has re-bucketed old extra-mass channels into the Hamiltonian C-term basis.
MTS has an explicit C_extra core channel fill row.
```

Forbidden:

```text
MTS has proved C_extra = 0.
MTS has proved radial Hamiltonian closure.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is good bridge-building work, even though it is another failed theorem attempt. The old "extra stuff might leak" problem is now a finite checklist. The best next move is the cleanest Cextra core channel: bulk/memory/range. If it has a positive source-free operator, we try to zero it. If not, it becomes a Yukawa/fifth-force coefficient row.

## 13. Next Target

`{NEXT_TARGET}`

Next: attack `epsilon_bulk_memory_range_over_MH` by attempting a positive-operator/no-hair proof or filling a source-backed Yukawa bound.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()
    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SILENCE_ATTEMPT_PATH, SILENCE_ATTEMPT_ROWS),
        (CHANNEL_MAP_PATH, CHANNEL_MAP_ROWS),
        (BOUND_FILL_PATH, BOUND_FILL_ROWS),
        (EVALUATOR_PATH, eval_rows),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, eval_rows, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
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
        "silence_attempt": str(ROOT / SILENCE_ATTEMPT_PATH),
        "channel_map": str(ROOT / CHANNEL_MAP_PATH),
        "bound_fill": str(ROOT / BOUND_FILL_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "missing_sources": missing_sources,
        "failed_validations": failed_validations,
        "Cextra_zero_signed": False,
        "Cextra_channel_fill_written": True,
        "radial_closure_claim_allowed": False,
        "source_measure_claim_allowed": False,
        "measured_GM_claim_allowed": False,
        "Newton_claim_allowed": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "formalization_workbench_modified": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
