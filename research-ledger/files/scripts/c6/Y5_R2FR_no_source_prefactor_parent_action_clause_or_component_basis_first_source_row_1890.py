from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1890"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md"

INPUTS = {
    "1889_doc": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
    "1889_validation": OUT / "P8_Y5_BRR545_1889_VALIDATION.csv",
    "1889_functor_contract": OUT / "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv",
    "1889_component_basis": OUT / "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv",
    "1889_next": OUT / "P8_Y5_PARENT_QLOC_1889_NEXT_TARGET.csv",
    "954_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "954_label_forgetting": OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
    "955_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "955_classification": OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "955_schema": OUT / "P8_Y5_R10_955_RESIDUAL_INPUT_SCHEMA.csv",
    "955_runner": OUT / "P8_Y5_R10_955_SPECIES_WEIGHT_RESIDUAL_RUNNER.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1067_action_scale": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1078_object_language": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1338_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1694_variation": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    "1762_deltaw": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1889_doc": ["NO_SOURCE_PREFACTOR_PARENT_ACTION_CLAUSE_IS_NEXT", "parent no-source-prefactor/no-double-counting"],
    "1889_validation": ["VAL1889_OVERALL,PASS"],
    "1889_functor_contract": ["NSF1889_2_no_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"],
    "1889_component_basis": ["CB1889_1_pre_action_species_prefactor", "LIVE_COUNTERMODEL_COMPONENT"],
    "1889_next": ["NEXT1889_0_primary", "do not claim local GR"],
    "954_clause": ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"],
    "954_label_forgetting": ["PLF954_2_prefactor_obstruction", "exact_contract_written_not_parent_signed"],
    "955_lemma": ["MMA955_3_relative_prefactor", "exact_lemma_contract_not_parent_derivation"],
    "955_classification": ["SPC955_2_relative_species_weight", "live_countermodel"],
    "955_schema": ["RIS955_0_epsilon_vector", "MISSING_PARENT_INPUT"],
    "955_runner": ["SWR955_2_WEP_surface_beta_source", "REJECTED_MISSING_PARENT_INPUT"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1067_action_scale": ["ASO1067_2_path_integral_measure", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1078_object_language": ["OL1078_2_forbidden_slot", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1236_certificate": ["CERT1236_5_source_label_forgetting", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1338_theorem": ["OLT1338_4_action_scale_owner", "NOT_DERIVED_CURRENT_CORPUS"],
    "1694_variation": ["VAR1694_1_Hilbert_source", "VAR1694_5_identity_verdict"],
    "1762_deltaw": ["DW1762_1_delta_w_A", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"],
    "1491_delta_w_pack": ["DWI1491_1_MICROSCOPE_TiPt", "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED"],
    "local_bounds": ["R1_WEP_source_charge", "2.8e-15"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1890_SOURCE_REGISTER.csv",
    "no_prefactor_attempt": OUT / "P8_Y5_PARENT_QLOC_1890_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv",
    "normalization_owner": OUT / "P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv",
    "first_component_row": OUT / "P8_Y5_PARENT_QLOC_1890_DELTAW_SPECIES_FIRST_COMPONENT_ROW_NONCLAIM.csv",
    "projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1890_NO_PREFACTOR_COMPONENT_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1890_NO_PREFACTOR_COMPONENT_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1890_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1890_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1890_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1890_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1890_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1890_VALIDATION.csv",
}

SOURCE_WEIGHT_TEMPLATE_COPY = SOURCE_WEIGHT_DOCS / "DELTAW_SPECIES1890_FIRST_COMPONENT_ROW_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_status": "PASS" if ok else "FAIL",
                "needle_detail": detail,
                "required_needles": "; ".join(SOURCE_NEEDLES[source_id]),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_prefactor_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_0_target",
            "claim": "parent action forbids independent source-only species prefactors before variation",
            "formal_statement": "Allowed[S_matter] excludes w_A S_A when w_A has no nongravitational field, gauge, representation, or current owner",
            "attempt_result": "TARGET_EXACT",
            "effect_if_signed": "T_source=T_total and Delta_w_species=0 after common-mode calibration",
            "gap": "must be parent action grammar/normalization theorem, not a preference after WEP pressure",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NEXT_TARGET.csv:NEXT1889_0_primary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_1_exact_conditional_lemma",
            "claim": "same total matter action plus no w_A gives label-forgotten source",
            "formal_statement": "S_matter=sum_A S_A[Psi_A,e_obs,theta_A] and T_total=delta S_matter/delta e_obs imply source object is T_total, not {(T_A,A)}",
            "attempt_result": "EXACT_IF_PARENT_SIGNED",
            "effect_if_signed": "source functor can use the conditional uniqueness theorem to produce one kappa_univ",
            "gap": "the no-source-prefactor clause is not itself derived",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_0_single_matter_functional;PAC954_1_no_source_prefactors;PAC954_2_total_Hilbert_derivative",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_2_double_counting_route",
            "claim": "source-only w_A double-counts matter normalization",
            "formal_statement": "masses, charges, Yukawa/representation constants and current normalizations are allowed only through nongravitational matter data theta_A; an extra active-source multiplier is not a measured matter parameter",
            "attempt_result": "PLAUSIBLE_PARENT_CLAUSE_NOT_DERIVED",
            "effect_if_signed": "w_A is classified as a forbidden source coefficient, not a legitimate matter constant",
            "gap": "needs a parent matter-normalization owner, not just interpretive bookkeeping",
            "source_anchor": "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv:PLF954_3_minimal_matter_normalization;P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_5_minimal_schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_3_classical_eom_failure",
            "claim": "classical field equations remove relative w_A",
            "formal_statement": "delta(w_A S_A)/delta Psi_A can be divided by constant w_A, but delta(w_A S_A)/delta e_obs = w_A T_A and exp(i w_A S_A/hbar) changes quantum/statistical weight",
            "attempt_result": "CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY",
            "effect_if_signed": "none; this route cannot sign the theorem",
            "gap": "Hilbert source and measure still know about w_A",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_0_matter_EOM;VAR1694_1_Hilbert_source;P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_2_path_integral_measure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_4_field_rescaling_failure",
            "claim": "field redefinitions universally remove w_A",
            "formal_statement": "Psi_A -> sqrt(w_A) Psi_A can move w_A into interactions, charges, composite material parameters, currents, or the measure",
            "attempt_result": "FIELD_RESCALING_NOT_GENERAL",
            "effect_if_signed": "model-specific simplifications may exist but no parent theorem follows",
            "gap": "needs simultaneous preservation of interactions, nongrav constants, Hilbert source, and measure",
            "source_anchor": "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_4_field_rescaling_limit;P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_3_field_redefinition_limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_5_object_language_route",
            "claim": "typed parent object language makes w_A untypeable",
            "formal_statement": "Arg(S_parent) contains geometry, matter fields, gauge/current data, representation constants and universal constants, but no inert source-only scalar slot",
            "attempt_result": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
            "effect_if_signed": "w_A cannot appear before variation",
            "gap": "parent object-language typing remains unsigned",
            "source_anchor": "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv:SSE1066_5_verdict;P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv:OL1078_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_6_countermodel",
            "claim": "covariance/additivity/Ward/naturality exclude relative prefactors",
            "formal_statement": "S_matter=sum_A w_A S_A with constant relative w_A is covariant, additive and Ward-compatible if the parent grammar allows the labels",
            "attempt_result": "COUNTERMODEL_SURVIVES",
            "effect_if_signed": "none; the countermodel is the reason the parent clause is needed",
            "gap": "direct-sum species labels can carry constants unless the parent functor forbids them",
            "source_anchor": "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv:SPC955_2_relative_species_weight;P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv:OLT1338_3_naturality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NSP1890_7_verdict",
            "claim": "no-source-prefactor parent action clause is derived",
            "formal_statement": "parent matter normalization owner + typed object language + single action/measure owner + no hidden/readout spurion => partial S_matter/partial w_A undefined",
            "attempt_result": "NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "effect_if_signed": "Delta_w_species theorem-zero and source-side GR/Newton route can advance to projected-mass and left-hand gates",
            "gap": "matter-normalization owner, action-scale owner, object-language typing, and readout/no-spurion stability remain unsigned",
            "source_anchor": "NSP1890_0 through NSP1890_6",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def normalization_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "MNO1890_0_allowed_matter_data",
            "object": "masses, charges, representations, gauge currents, Yukawa/spectral constants",
            "owner_rule": "allowed only as nongravitational matter/representation data theta_A or owned current normalizations",
            "status": "ALLOWED_IF_OBSERVABLE_OWNER_SIGNED",
            "risk_if_missing": "a source-only multiplier can be disguised as matter normalization",
            "source_anchor": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_5_source_label_forgetting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "MNO1890_1_forbidden_source_multiplier",
            "object": "w_A multiplying only active gravitational source/action weight",
            "owner_rule": "forbidden unless it is an owned matter parameter with nongravitational readout or a finite residual coefficient row",
            "status": "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED",
            "risk_if_missing": "T_source=sum_A w_A T_A survives and maps to WEP/R10/PPN/Newton residuals",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_1_no_source_prefactors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "MNO1890_2_common_mode",
            "object": "w_common multiplying the whole matter action",
            "owner_rule": "calibration-only after uniqueness; not a relative WEP/R10 residual by itself",
            "status": "COMMON_MODE_ONLY_AFTER_PARENT_UNIQUENESS",
            "risk_if_missing": "absorbing relative weights into G_N/GM hides a physical residual",
            "source_anchor": "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv:SPC955_1_common_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "MNO1890_3_hbar_measure_owner",
            "object": "hbar_parent and path-integral/statistical measure",
            "owner_rule": "one parent phase/measure normalization for all ordinary matter sectors; no species-only measure Jacobian",
            "status": "OWNER_NOT_DERIVED",
            "risk_if_missing": "species-dependent effective hbar_A or J_A measure factors mimic w_A S_A",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_0_hbar_parent;HMO1067_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "MNO1890_4_readout_spurion",
            "object": "hidden marker, boundary/domain class, readout mask",
            "owner_rule": "must not re-enter as a source prefactor after label-forgetting",
            "status": "NO_SPURION_STILL_UNSIGNED",
            "risk_if_missing": "w_A returns as w(m,D,boundary,A) or post-readout source mask",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_3_no_hidden_spurion_return",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "MNO1890_5_verdict",
            "object": "matter normalization owner",
            "owner_rule": "fix ordinary matter normalization before gravitational source extraction and forbid active-source-only relative weights",
            "status": "MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            "risk_if_missing": "Delta_w_species remains a live finite component",
            "source_anchor": "MNO1890_0 through MNO1890_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def first_component_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_row_id": "DWS1890_0_species_prefactor_component",
            "branch_id": BRANCH_ID,
            "component_basis": "Delta_w_component_basis_v1",
            "component": "Delta_w_species",
            "component_definition": "relative pre-variation species/action/source prefactor after common-mode projection",
            "basis_formula": "w_A=w_common(1+epsilon_A), sum_common epsilon_A=0, Delta_w_species={epsilon_A}",
            "coefficient_origin": "pre-action source-only species prefactor w_A S_A if parent no-prefactor theorem fails",
            "current_value": "MISSING_PARENT_NUMERIC_COEFFICIENT",
            "units": "dimensionless",
            "source_path": str(INPUTS["954_clause"]),
            "source_anchor": "PAC954_1_no_source_prefactors; PAC954_2_total_Hilbert_derivative",
            "derivation_status": "SOURCE_BACKED_COMPONENT_DEFINED_NONNUMERIC",
            "zero_route_status": "NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "required_for_claim": "parent theorem-zero or numeric epsilon_A vector with component basis, norm, source path, tau, K/Qbar/material projections",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PRJ1890_0_core",
            "arena": "core_component_vector",
            "formula": "Delta_w_species={epsilon_A}; common mode projected out before any arena score",
            "required_inputs": "species/material basis, norm, no-cancellation policy, parent numeric coefficients",
            "current_status": "MISSING_PARENT_NUMERIC_COEFFICIENT",
            "source_anchor": "P8_Y5_R10_955_RESIDUAL_INPUT_SCHEMA.csv:RIS955_0_epsilon_vector",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1890_1_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "formula": "eta_TiPt = (DeltaQ_TiPt dot Delta_w_species) * tau_WEP",
            "required_inputs": "official Ti/Pt material tensor, Earth/source worldtube, tau_WEP, force/readout convention",
            "current_status": "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "source_anchor": "local_bound_claims.csv:R1_WEP_source_charge; P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv:DWI1491_1_MICROSCOPE_TiPt",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1890_2_R10",
            "arena": "R10_short_range",
            "formula": "alpha_delta_w(lambda)=K_R10(lambda) Qbar_source_test(lambda).Delta_w_species",
            "required_inputs": "K_R10(lambda), Qbar_source_test(lambda), tau_R10(lambda), range/kernel convention, digitized bound curve",
            "current_status": "SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING",
            "source_anchor": "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv:DWI1491_3_R10",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1890_3_PPN",
            "arena": "PPN_beta_gamma_source",
            "formula": "Delta_beta_source <= K_PPN (||Delta_w_species|| + |beta_w_source| + |beta_w_test|)",
            "required_inputs": "weak-field source solution, source/test split, PPN operator norm, beta_w normalization",
            "current_status": "MISSING_PPN_OPERATOR_NORM_AND_SOURCE_TEST_LEGS",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_1_beta_w_source_test",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1890_4_clock_orbital",
            "arena": "clock_and_orbital",
            "formula": "|clock/orbital product| <= |K_arena dot Delta_w_species| |tau_arena|",
            "required_inputs": "clock mass/alpha split, orbital GM convention, source body composition, tau_clock/tau_orbital",
            "current_status": "PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED",
            "source_anchor": "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv:DWI1491_4_clock;DWI1491_5_orbital",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1890_0_theorem_unsigned", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": False, "numeric_coefficient": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_1_classical_eom", "parent_theorem": False, "classical_eom_shortcut": True, "field_rescale_shortcut": False, "component_row": False, "numeric_coefficient": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_2_field_rescale", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": True, "component_row": False, "numeric_coefficient": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_FIELD_RESCALING_NOT_GENERAL", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_3_component_no_numeric", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": False, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_4_bound_anchor", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": False, "tau": False, "K_projection": False, "bound_anchor": True, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_5_missing_tau", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": True, "tau": False, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_TAU_PROJECTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_6_missing_K", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": True, "tau": True, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_K_QBAR_PROJECTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_7_G_absorption", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": True, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_G_ABSORPTION_WITHOUT_UNIQUENESS", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_8_cancellation", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": True, "schema_only": False, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1890_9_schema_only", "parent_theorem": False, "classical_eom_shortcut": False, "field_rescale_shortcut": False, "component_row": True, "numeric_coefficient": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": True, "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE", "valid_for_claim": False, "claim_allowed": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["classical_eom_shortcut"]) == "true":
        status = "REFUSED_CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY"
        detail = "classical EOM shape does not fix Hilbert source or measure"
    elif bool_string(row["field_rescale_shortcut"]) == "true":
        status = "REFUSED_FIELD_RESCALING_NOT_GENERAL"
        detail = "field rescaling can move the weight into interactions/currents/measure"
    elif bool_string(row["parent_theorem"]) != "true" and bool_string(row["component_row"]) != "true":
        status = "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"
        detail = "no-source-prefactor theorem is not parent-signed"
    elif bool_string(row["bound_anchor"]) == "true":
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
        detail = "experimental bounds do not define a parent coefficient"
    elif bool_string(row["numeric_coefficient"]) != "true":
        status = "REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT"
        detail = "component row has no parent numeric coefficient"
    elif bool_string(row["tau"]) != "true":
        status = "REFUSED_MISSING_TAU_PROJECTION"
        detail = "arena projection tau is missing"
    elif bool_string(row["K_projection"]) != "true":
        status = "REFUSED_MISSING_K_QBAR_PROJECTION"
        detail = "K/Qbar/material projection is missing"
    elif bool_string(row["G_absorption"]) == "true":
        status = "REFUSED_G_ABSORPTION_WITHOUT_UNIQUENESS"
        detail = "relative source weights cannot be hidden in G before uniqueness"
    elif bool_string(row["cancellation"]) == "true":
        status = "REFUSED_CANCELLATION_ONLY"
        detail = "component cancellation needs parent identity"
    elif bool_string(row["schema_only"]) == "true":
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        detail = "schema exercise is not physics evidence"
    else:
        status = "REFUSED_UNCLASSIFIED_NONCLAIM"
        detail = "case remains nonclaim"
    return {
        **row,
        "observed_status": status,
        "status_detail": detail,
        "status_matches_expected": status == row["expected_status"],
        "valid_prediction_row": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1890_0_parent_zero",
            "input_kind": "no_source_prefactor_zero_theorem",
            "runner_status": "REFUSED_NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "reason": "matter-normalization owner, object language, action-scale owner and no-spurion/readout stability remain unsigned",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1890_1_first_component",
            "input_kind": "Delta_w_species_first_component_row",
            "runner_status": "REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT_AND_PROJECTIONS",
            "reason": "row is source-backed as a component definition but has no numeric coefficient, tau, or K/Qbar projections",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1890_2_bound_anchors",
            "input_kind": "WEP_R10_PPN_bound_anchors",
            "runner_status": "REFUSED_BOUND_ANCHORS_NOT_PREDICTIONS",
            "reason": "bounds cannot be used as Delta_w_species predictions",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE1890_0_zero_theorem",
            "claim": "Delta_w_species=0 from no-source-prefactor parent action theorem",
            "required": "matter-normalization owner, object-language typing, single action/measure owner, no spurion/readout return",
            "current_status": "BLOCKED_NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1890_1_first_component_row",
            "claim": "Delta_w_species component row is score-ready",
            "required": "numeric parent coefficient vector, units, source path, basis, tau, K/Qbar/material projections",
            "current_status": "BLOCKED_COMPONENT_ROW_NONNUMERIC",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1890_2_GR_Newton_source",
            "claim": "source side reduces to GR/Newton",
            "required": "zero theorem or all finite components bounded plus projected mass/Newton calibration and left-hand field equation gate",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1890_0_theorem",
            "question": "can no-source-prefactor be derived now?",
            "answer": "not from current corpus",
            "basis": "the exact conditional theorem exists, but matter-normalization owner and typed parent action remain unsigned",
            "decision": "NO_SOURCE_PREFACTOR_REMAINS_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1890_1_component",
            "question": "can the first component row be sourced without pretending to score?",
            "answer": "yes, as a nonnumeric component definition only",
            "basis": "Delta_w_species is source-backed to PAC954/SPC955/VAR1694 but still lacks parent numeric coefficient and projections",
            "decision": "FIRST_COMPONENT_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1890_2_next",
            "question": "what is the next best derivation target?",
            "answer": "matter-normalization owner",
            "basis": "if ordinary matter normalization is owned by nongravitational representation/current data, source-only w_A becomes double-counting rather than a legal parameter",
            "decision": "SELECT_1891_MATTER_NORMALIZATION_OWNER_OR_DELTAW_SPECIES_COEFFICIENT_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1890_0_primary",
            "selection_status": "selected",
            "target_doc": "1891-Y5-R2FR-matter-normalization-owner-or-deltaw-species-coefficient-source-row.md",
            "target_script": "scripts/Y5_R2FR_matter_normalization_owner_or_deltaw_species_coefficient_source_row_1891.py",
            "objective": "try to derive the parent matter-normalization owner from nongravitational representation/current standards so source-only w_A is double-counting; if it fails, source the first explicit Delta_w_species coefficient row as nonclaim with units and projection requirements",
            "success_condition": "parent-signed matter-normalization owner, or a sourced nonclaim coefficient row with numeric/symbolic coefficient origin, declared units, tau/K/Qbar requirements, and no bound-anchor shortcut",
            "do_not": "do not claim local GR, do not use classical EOM rescaling as proof, do not absorb relative weights into G, and do not score WEP/R10/PPN bounds as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS1890_0_progress",
            "area": "coupling theorem",
            "status": "no-source-prefactor theorem sharpened",
            "detail": "the theorem is now a precise parent action/matter-normalization owner problem, not a Ward or EOM problem",
            "risk_level": "USEFUL_PROGRESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1890_1_main_bottleneck",
            "area": "matter-normalization owner",
            "status": "unsigned",
            "detail": "source-only w_A is forbidden by contract but not yet derived as double-counting from parent MTS primitives",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1890_2_fallback",
            "area": "finite component row",
            "status": "first component row staged nonclaim",
            "detail": "Delta_w_species has a source-backed definition and projection requirements, but no parent numeric coefficient",
            "risk_level": "BLOCKED_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_prefactor_attempt": no_prefactor_attempt_rows(),
        "normalization_owner": normalization_owner_rows(),
        "first_component_row": first_component_row_rows(),
        "projection_requirements": projection_requirement_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:  # noqa: BLE001
            return False, f"{path.name}:{exc}"
        details.append(f"{path.name}:{len(rows)}")
    return True, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for row in csv_rows(path):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) == "true":
                    return False, f"{path.name}:{field}=true"
    return True, "all claim flags false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values()).upper()
            if any(marker in joined for marker in ("MISSING", "UNSIGNED", "BLOCKED", "NOT_DERIVED", "COUNTERMODEL")):
                if bool_string(row.get("score_ready", "false")) == "true" or bool_string(row.get("valid_for_claim", "false")) == "true":
                    return False, f"{path.name}:row{index}:blocked marker marked ready"
    return True, "blocked-marker rows are not claim-ready"


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["no_prefactor_attempt"], MICROSCOPE_RESIDUALS / OUTPUTS["no_prefactor_attempt"].name)
    shutil.copy2(OUTPUTS["normalization_owner"], QUEUE / "JR1890_MATTER_NORMALIZATION_OWNER_AUDIT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["first_component_row"], SOURCE_WEIGHT_TEMPLATE_COPY)
    shutil.copy2(OUTPUTS["projection_requirements"], QUEUE / "JR1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    source_rows = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1890_0_sources_exist",
            "status": "PASS" if all(bool_string(row["exists"]) == "true" for row in source_rows) else "FAIL",
            "detail": f"{sum(bool_string(row['exists']) == 'true' for row in source_rows)}/{len(source_rows)} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1890_1_needles_found",
            "status": "PASS" if all(row["needle_status"] == "PASS" for row in source_rows) else "FAIL",
            "detail": f"{sum(row['needle_status'] == 'PASS' for row in source_rows)}/{len(source_rows)} source needles found",
            "valid_for_claim": False,
        }
    )

    attempt_rows = csv_rows(OUTPUTS["no_prefactor_attempt"])
    checks.append(
        {
            "validation_id": "VAL1890_2_theorem_not_promoted",
            "status": "PASS"
            if any(row["attempt_id"] == "NSP1890_7_verdict" and row["attempt_result"] == "NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED" for row in attempt_rows)
            else "FAIL",
            "detail": "no-source-prefactor theorem remains conditional",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1890_3_exact_conditional_retained",
            "status": "PASS" if any(row["attempt_result"] == "EXACT_IF_PARENT_SIGNED" for row in attempt_rows) else "FAIL",
            "detail": "exact conditional total-variation lemma retained",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1890_4_countermodel_retained",
            "status": "PASS" if any(row["attempt_result"] == "COUNTERMODEL_SURVIVES" for row in attempt_rows) else "FAIL",
            "detail": "relative pre-action source prefactor countermodel retained",
            "valid_for_claim": False,
        }
    )

    owner_rows = csv_rows(OUTPUTS["normalization_owner"])
    checks.append(
        {
            "validation_id": "VAL1890_5_normalization_owner_unsigned",
            "status": "PASS"
            if any(row["audit_id"] == "MNO1890_5_verdict" and row["status"] == "MATTER_NORMALIZATION_OWNER_NOT_DERIVED" for row in owner_rows)
            else "FAIL",
            "detail": "matter-normalization owner remains unsigned",
            "valid_for_claim": False,
        }
    )

    component_rows = csv_rows(OUTPUTS["first_component_row"])
    checks.append(
        {
            "validation_id": "VAL1890_6_first_component_nonclaim",
            "status": "PASS"
            if len(component_rows) == 1
            and component_rows[0]["component"] == "Delta_w_species"
            and bool_string(component_rows[0]["score_ready"]) == "false"
            and bool_string(component_rows[0]["valid_for_claim"]) == "false"
            else "FAIL",
            "detail": "Delta_w_species first component row staged as nonclaim",
            "valid_for_claim": False,
        }
    )

    projection_rows = csv_rows(OUTPUTS["projection_requirements"])
    required_projection_ids = {"PRJ1890_1_WEP", "PRJ1890_2_R10", "PRJ1890_3_PPN"}
    checks.append(
        {
            "validation_id": "VAL1890_7_projection_requirements",
            "status": "PASS" if required_projection_ids.issubset({row["projection_id"] for row in projection_rows}) else "FAIL",
            "detail": f"projection_rows={len(projection_rows)}",
            "valid_for_claim": False,
        }
    )

    dryrun_rows = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED",
        "REFUSED_CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY",
        "REFUSED_FIELD_RESCALING_NOT_GENERAL",
        "REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_MISSING_TAU_PROJECTION",
        "REFUSED_MISSING_K_QBAR_PROJECTION",
        "REFUSED_G_ABSORPTION_WITHOUT_UNIQUENESS",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    observed_statuses = {row["observed_status"] for row in dryrun_rows}
    checks.append(
        {
            "validation_id": "VAL1890_8_dryrun_failure_modes",
            "status": "PASS"
            if expected_statuses.issubset(observed_statuses) and all(bool_string(row["status_matches_expected"]) == "true" for row in dryrun_rows)
            else "FAIL",
            "detail": "dryrun_statuses=" + ",".join(row["observed_status"] for row in dryrun_rows),
            "valid_for_claim": False,
        }
    )

    runner_rows = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1890_9_runner_refusal",
            "status": "PASS" if all(bool_string(row["score_ready"]) == "false" for row in runner_rows) else "FAIL",
            "detail": "all runners refuse claim scoring",
            "valid_for_claim": False,
        }
    )

    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1890_10_claim_gates",
            "status": "PASS" if all(bool_string(row["pass_gate"]) == "false" for row in gate_rows) else "FAIL",
            "detail": "all claim gates remain blocked",
            "valid_for_claim": False,
        }
    )

    decision_rows_loaded = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1890_11_decision",
            "status": "PASS"
            if any(row["decision"] == "SELECT_1891_MATTER_NORMALIZATION_OWNER_OR_DELTAW_SPECIES_COEFFICIENT_SOURCE_ROW" for row in decision_rows_loaded)
            else "FAIL",
            "detail": "decision selects matter-normalization owner or Delta_w_species coefficient row next",
            "valid_for_claim": False,
        }
    )

    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1890_12_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1890_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1891 matter-normalization owner selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1890_13_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps matter-normalization owner as main bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1890_14_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1890_15_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1890_16_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["no_prefactor_attempt"].name,
        QUEUE / "JR1890_MATTER_NORMALIZATION_OWNER_AUDIT_NONCLAIM.csv",
        SOURCE_WEIGHT_TEMPLATE_COPY,
        QUEUE / "JR1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1890_17_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1890_18_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1890*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1890_19_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1890_count={len(formalization_hits)}", "valid_for_claim": False})

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1890_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1890 no-source-prefactor parent action clause or component basis first source row", "valid_for_claim": False})
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1890 - No-Source-Prefactor Parent Action Clause Or Component-Basis First Source Row

**Private status:** derivation-first coupling checkpoint; no WEP/R10/PPN/Newton/local-GR claim.

## Result

1890 tries to prove the exact clause exposed by 1889:

```text
Allowed[S_matter] excludes w_A S_A
when w_A has no nongravitational field, gauge, representation, or current owner.
```

The conditional theorem is clean:

```text
S_matter=sum_A S_A[Psi_A,e_obs,theta_A]
T_total = delta S_matter / delta e_obs
no source-only w_A before variation
=> source sees T_total, not {{(T_A,A)}}.
```

But the present corpus still does not derive the parent matter-normalization owner that would make source-only `w_A` illegal rather than merely absent from a preferred action. Classical EOM scaling and field redefinitions do not solve it generally; they can leave the Hilbert source, interactions, currents, and quantum/statistical measure changed.

So 1890 does two useful things: it preserves the exact theorem as a contract, and it stages the first source-backed nonclaim component row `Delta_w_species` with explicit WEP/R10/PPN projection requirements. It is not score-ready.

## No-Source-Prefactor Theorem Attempt

{markdown_table(rows_by_name["no_prefactor_attempt"])}

## Matter-Normalization Owner Audit

{markdown_table(rows_by_name["normalization_owner"])}

## First Delta_w Species Component Row

{markdown_table(rows_by_name["first_component_row"])}

## Projection Requirements

{markdown_table(rows_by_name["projection_requirements"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
