from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1892"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1892-Y5-R2FR-ordinary-matter-action-signature-or-deltaw-species-projection-kernels.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1891_doc": ROOT / "1891-Y5-R2FR-matter-normalization-owner-or-deltaw-species-coefficient-source-row.md",
    "1891_validation": OUT / "P8_Y5_BRR545_1891_VALIDATION.csv",
    "1891_theorem": OUT / "P8_Y5_PARENT_QLOC_1891_MATTER_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1891_coeff": OUT / "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv",
    "1891_projection": OUT / "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv",
    "1891_next": OUT / "P8_Y5_PARENT_QLOC_1891_NEXT_TARGET.csv",
    "626_quotient_signature": OUT / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
    "711_quotient_descent": OUT / "P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
    "761_vertical_action_contract": OUT / "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
    "761_liev_audit": OUT / "P8_Y5_R10_761_LIEV_SMATTER_EVALUABILITY_AUDIT.csv",
    "767_matter_functor_reaudit": OUT / "P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
    "767_local_gr_bridge": OUT / "P8_Y5_R10_767_LOCAL_GR_BRIDGE.csv",
    "898_matter_descent": OUT / "P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
    "898_promotion_gate": OUT / "P8_Y5_R10_898_PROMOTION_GATE.csv",
    "1044_pullback": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
    "1044_premise_gate": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv",
    "1045_matter_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1088_minimal_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
}


SOURCE_NEEDLES = {
    "1891_doc": ["MATTER_NORMALIZATION_OWNER_NOT_DERIVED", "NEXT1891_0_primary"],
    "1891_validation": ["VAL1891_OVERALL,PASS"],
    "1891_theorem": ["MNO1891_5_verdict", "MATTER_NORMALIZATION_OWNER_NOT_DERIVED"],
    "1891_coeff": ["DWS1891_0_delta_w_species_coefficient_slot", "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE"],
    "1891_projection": ["PRJ1891_1_WEP", "PRJ1891_2_R10", "MISSING_PPN_OPERATOR_NORM"],
    "1891_next": ["NEXT1891_0_primary", "ordinary-matter action signature"],
    "626_quotient_signature": ["QIM626_5_signature_verdict", "not_closed"],
    "711_quotient_descent": ["QDA711_9_verdict", "fail_current_corpus"],
    "761_vertical_action_contract": ["MVA761_5_evaluability_verdict", "parent_matter_vertical_action_not_signed"],
    "761_liev_audit": ["LEV761_3_current_corpus", "not_evaluable_as_parent_theorem"],
    "767_matter_functor_reaudit": ["PMR767_0_explicit_parent_matter_functor", "still_unsigned"],
    "767_local_gr_bridge": ["LGB767_2_Newton_source", "open_residual"],
    "898_matter_descent": ["MDS898_5_verdict", "not_signed"],
    "898_promotion_gate": ["PG898_1_matter_descent", "fail_for_claim"],
    "1044_pullback": ["MPD1044_7_exact_theorem_if_signed", "EXACT_CONDITIONAL_THEOREM"],
    "1044_premise_gate": ["MPG1044_6_verdict", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED"],
    "1045_matter_functor": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1088_minimal_signature": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
    "1236_certificate": ["CERT1236_5_source_label_forgetting", "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1892_SOURCE_REGISTER.csv",
    "signature_attempt": OUT / "P8_Y5_PARENT_QLOC_1892_ORDINARY_MATTER_ACTION_SIGNATURE_ATTEMPT.csv",
    "clause_matrix": OUT / "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv",
    "projection_kernels": OUT / "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1892_SIGNATURE_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1892_SIGNATURE_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1892_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1892_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1892_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1892_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1892_VALIDATION.csv",
}


BRANCH_COPIES = {
    "signature_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["signature_attempt"].name,
    "clause_matrix": QUEUE / "JR1892_SIGNATURE_CLAUSE_MATRIX_NONCLAIM.csv",
    "projection_kernels": SOURCE_WEIGHT_DOCS / "DELTAW_PROJECTION_KERNEL_STUBS1892_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def signature_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "OMAS1892_0_target_signature",
            "claim_piece": "ordinary-matter action signature",
            "mathematical_statement": "S_matter = sum_A S_A[Psi_A; e_obs(q(Phi)), omega[e_obs], A_obs(q(Phi)), theta_A] with total Hilbert source J=delta S_matter/delta e_obs before readout",
            "status": "TARGET_SIGNATURE_SHARP",
            "derivation_or_obstruction": "this is the exact signature needed to make representative vertical motion invisible to ordinary matter and source weights",
            "source_anchor": "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv:MOMS1088_0_action_form",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "OMAS1892_1_chain_rule_if_signed",
            "claim_piece": "local source zero theorem",
            "mathematical_statement": "for v in ker(Dq), Lie_v e_obs=Lie_v A_obs=Lie_v theta_A=0 and an owned matter lift imply Lie_v S_matter is boundary/gauge only, hence qbar_XT and Delta_w_species vanish",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "derivation_or_obstruction": "standard chain-rule identity already exists; it needs all signature clauses simultaneously parent-signed",
            "source_anchor": "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv:MPD1044_1_chain_rule_identity;MPD1044_7_exact_theorem_if_signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "OMAS1892_2_signature_not_signed",
            "claim_piece": "parent adoption attempt",
            "mathematical_statement": "promote the target signature as the current MTS parent action",
            "status": "ORDINARY_MATTER_ACTION_SIGNATURE_NOT_PARENT_SIGNED",
            "derivation_or_obstruction": "quotient object, matter bundle, vertical lift, constants, no source weights, hbar/measure, boundary, and readout closure remain written as clauses rather than derived parent structure",
            "source_anchor": "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv:MFS1045_6_verdict; P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv:MOMS1088_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "OMAS1892_3_projection_fallback",
            "claim_piece": "finite Delta_w projection fallback",
            "mathematical_statement": "if the signature cannot be parent-signed, Delta_w_species must be carried as a finite dimensionless coefficient into arena-specific projection kernels",
            "status": "FALLBACK_KERNEL_STUBS_REQUIRED_NONCLAIM",
            "derivation_or_obstruction": "projection kernels can make the branch testable but cannot promote local GR until parent epsilon_A and tau/K/Qbar inputs are sourced",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_0_core..PRJ1891_5_orbital",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def clause_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "OMC1892_0_quotient_object",
            "signature_clause": "parent quotient object and observed geometry",
            "required_identity": "q_loc exists, v in ker(Dq_loc), e_obs=E(q_loc(Phi)), omega_obs=omega[e_obs]",
            "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "if_signed": "geometry/source sees no representative frame motion",
            "if_unsigned": "c_g, disformal, and connection residuals remain live",
            "source_anchor": "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv:QIM626_0_descent_equivalence;QIM626_2_measure_and_connection_descent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_1_matter_bundle",
            "signature_clause": "ordinary matter bundle over observed geometry",
            "required_identity": "Psi_A in Gamma(E_A[e_obs,A_obs]) and S_A uses only e_obs, owned connection/gauge data, and theta_A",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "if_signed": "Lie_v S_matter becomes evaluable without smuggled matter frames",
            "if_unsigned": "a fitted matter frame/source split can be mistaken for GR recovery",
            "source_anchor": "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv:MVA761_0_domain_category; P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv:MFS1045_2_matter_bundle_functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_2_vertical_lift",
            "signature_clause": "fixed/gauge ordinary-matter vertical lift",
            "required_identity": "delta_v Psi_A=0 or an owned gauge/local-Lorentz/diffeomorphism lift with boundary-only variation",
            "current_status": "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "if_signed": "ordinary matter does not acquire a physical source charge from representative motion",
            "if_unsigned": "vertical motion may be a real fifth-force/source label",
            "source_anchor": "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv:MVA761_1_fixed_Psi_vertical_action;MVA761_2_gauge_lift_action; P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv:MPG1044_1_vertical_kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_3_constant_superselection",
            "signature_clause": "constants and representation standards",
            "required_identity": "Lie_v theta_A=0 for masses, charges, alpha_EM, clocks, binding, representation labels, or else the channel is retained as a finite residual",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "if_signed": "constant/clock/material source charges theorem-zero",
            "if_unsigned": "WEP, clock, alpha, mass, and binding residual rows remain active",
            "source_anchor": "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv:MOMS1088_3_constant_superselection; P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv:MPG1044_2_constant_superselection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_4_source_functor_label_forgetting",
            "signature_clause": "total Hilbert source before readout",
            "required_identity": "J_grav = delta S_matter/delta e_obs with no pre-variation w_A, kappa_A, material selector, or per-species source label",
            "current_status": "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED",
            "if_signed": "Delta_w_species=0 follows from source functor grammar",
            "if_unsigned": "relative source weights remain the main coupling debt",
            "source_anchor": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_5_source_label_forgetting; P8_Y5_PARENT_QLOC_1891_MATTER_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv:MNO1891_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_5_hbar_measure_action_scale",
            "signature_clause": "single action-scale/measure owner",
            "required_identity": "one hbar_parent and measure normalization for all ordinary sectors; no species-only path-integral/statistical Jacobian",
            "current_status": "OWNER_NOT_DERIVED",
            "if_signed": "action-scale prefactor cannot reappear as w_A S_A",
            "if_unsigned": "effective hbar_A or measure factors mimic Delta_w_species",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_6_no_shadow_boundary_readout",
            "signature_clause": "no shadow frame, marker, boundary, or readout re-entry",
            "required_identity": "no hidden conformal/disformal frame, marker/domain selector, boundary local projection, or EFT/readout term can act as an active source coefficient",
            "current_status": "BOUNDARY_AND_EFT_SILENCE_NOT_SIGNED",
            "if_signed": "bare parent signature survives local tests",
            "if_unsigned": "post-readout or boundary source terms can restore fifth-force pressure",
            "source_anchor": "P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv:MDS898_4_boundary_EFT_no_extension; P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv:MPG1044_4_boundary_support_silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OMC1892_7_verdict",
            "signature_clause": "ordinary matter action signature as current MTS theorem",
            "required_identity": "OMC1892_0 through OMC1892_6 are all derived from one parent action",
            "current_status": "ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "if_signed": "local source coupling branch can promote Delta_w_species and qbar_XT to theorem-zero",
            "if_unsigned": "keep the local branch blocked and carry finite Delta_w projection kernels",
            "source_anchor": "OMC1892_0_quotient_object through OMC1892_6_no_shadow_boundary_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "DK1892_0_core_vector",
            "arena": "core_component_vector",
            "kernel_formula": "epsilon_perp = P_perp epsilon, with P_perp removing the common calibration mode using sourced composition weights p_A",
            "required_inputs": "parent epsilon_A vector; species/material basis; composition weights p_A; norm/no-cancellation convention",
            "current_status": "SYMBOLIC_STUB_ONLY_PARENT_COEFFICIENT_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_0_delta_w_species_coefficient_slot",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DK1892_1_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "kernel_formula": "eta_TiPt = tau_WEP * DeltaQ_TiPt dot epsilon_perp",
            "required_inputs": "Ti/Pt material tensor; Earth/source composition; tau_WEP; force convention; parent epsilon_A vector",
            "current_status": "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_1_WEP",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DK1892_2_R10",
            "arena": "R10_short_range",
            "kernel_formula": "alpha_Delta_w(lambda)=tau_R10(lambda)*K_R10(lambda)*Qbar_source_test(lambda) dot epsilon_perp",
            "required_inputs": "range kernel; source/test composition; tau_R10(lambda); K_R10(lambda); digitized alpha_bound(lambda); parent epsilon_A vector",
            "current_status": "KERNEL_STUB_NONCLAIM_RANGE_KERNEL_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_2_R10",
            "units": "dimensionless alpha(lambda)",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DK1892_3_PPN",
            "arena": "PPN_beta_gamma_source",
            "kernel_formula": "[Delta gamma, Delta beta, alpha_i, xi]_source = M_PPN * epsilon_perp plus retained beta_w/source-test legs",
            "required_inputs": "weak-field solution; PPN operator matrix M_PPN; source/test split; parent epsilon_A vector",
            "current_status": "KERNEL_STUB_NONCLAIM_OPERATOR_MATRIX_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_3_PPN",
            "units": "dimensionless PPN deviations",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DK1892_4_clock",
            "arena": "clock_and_constant_drift",
            "kernel_formula": "Delta ln nu_i = K_clock_i dot epsilon_perp + retained alpha/mass/readout coefficients",
            "required_inputs": "clock sensitivity vector; alpha/mass split; source body composition; tau_clock; parent epsilon_A vector",
            "current_status": "KERNEL_STUB_NONCLAIM_CLOCK_SENSITIVITY_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_4_clock",
            "units": "dimensionless frequency shift or drift",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DK1892_5_orbital",
            "arena": "orbital_GM_inverse_square",
            "kernel_formula": "Delta ln(GM)_obs = K_orbital dot epsilon_perp + retained finite-range/source-test terms",
            "required_inputs": "source body composition; orbital GM convention; inverse-square kernel; tau_orbital; parent epsilon_A vector",
            "current_status": "KERNEL_STUB_NONCLAIM_ORBITAL_SOURCE_MAP_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_5_orbital",
            "units": "dimensionless GM/source deviation",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1892_0_signature_unsigned",
            "signature_parent_signed": False,
            "uses_closure_as_theorem": False,
            "coefficient_kind": "symbolic_free",
            "projection_kernel_ready": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1892_1_closure_as_theorem",
            "signature_parent_signed": False,
            "uses_closure_as_theorem": True,
            "coefficient_kind": "symbolic_free",
            "projection_kernel_ready": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_CLOSURE_NOT_PARENT_THEOREM",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1892_2_signature_signed_but_no_coeff",
            "signature_parent_signed": True,
            "uses_closure_as_theorem": False,
            "coefficient_kind": "missing_parent_epsilon",
            "projection_kernel_ready": True,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_MISSING_PARENT_EPSILON_VECTOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1892_3_projection_missing",
            "signature_parent_signed": True,
            "uses_closure_as_theorem": False,
            "coefficient_kind": "parent_numeric",
            "projection_kernel_ready": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_PROJECTION_KERNEL_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1892_4_bound_shortcut",
            "signature_parent_signed": True,
            "uses_closure_as_theorem": False,
            "coefficient_kind": "parent_numeric",
            "projection_kernel_ready": True,
            "uses_bound_as_prediction": True,
            "expected_status": "REFUSED_BOUND_NOT_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1892_5_schema_only_kernel",
            "signature_parent_signed": False,
            "uses_closure_as_theorem": False,
            "coefficient_kind": "symbolic_free",
            "projection_kernel_ready": "schema_only",
            "uses_bound_as_prediction": False,
            "expected_status": "SCHEMA_KERNEL_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    signature_signed = bool_string(row["signature_parent_signed"]) == "true"
    closure_as_theorem = bool_string(row["uses_closure_as_theorem"]) == "true"
    coefficient_kind = str(row["coefficient_kind"])
    projection_ready_raw = bool_string(row["projection_kernel_ready"])
    projection_ready = projection_ready_raw == "true"
    bound_shortcut = bool_string(row["uses_bound_as_prediction"]) == "true"

    if closure_as_theorem:
        status = "REFUSED_CLOSURE_NOT_PARENT_THEOREM"
    elif projection_ready_raw == "schema_only":
        status = "SCHEMA_KERNEL_ONLY_NOT_EVIDENCE"
    elif not signature_signed:
        status = "REFUSED_SIGNATURE_UNSIGNED"
    elif coefficient_kind == "missing_parent_epsilon":
        status = "REFUSED_MISSING_PARENT_EPSILON_VECTOR"
    elif not projection_ready:
        status = "REFUSED_PROJECTION_KERNEL_MISSING"
    elif bound_shortcut:
        status = "REFUSED_BOUND_NOT_PREDICTION"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"

    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1892_0_signature",
            "condition": "ordinary matter action signature parent-signed",
            "current_status": "FAIL_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv:OMC1892_7_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1892_1_source_label_forgetting",
            "condition": "source functor returns total Hilbert stress and forgets species labels before coupling",
            "current_status": "FAIL_CONDITIONAL_LEMMA_NOT_PARENT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv:OMC1892_4_source_functor_label_forgetting",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1892_2_projection_kernels",
            "condition": "Delta_w projection kernels have sourced tau/K/Qbar/material maps",
            "current_status": "FAIL_KERNEL_STUBS_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_0_core_vector..DK1892_5_orbital",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1892_3_verdict",
            "condition": "local GR/Newton source coupling is derived or executable as bounded residual",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1892_0_signature through CG1892_2_projection_kernels",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1892_0_signature",
            "decision": "ordinary-matter action signature is not yet a parent theorem",
            "reason": "all needed clauses exist, but they are still contracts/conditional lemmas, not one derived parent action",
            "status": "SIGNATURE_ROUTE_SHARP_BUT_UNSIGNED",
            "next_dependency": "source-functor label forgetting is the smallest high-leverage clause",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1892_1_projection_fallback",
            "decision": "projection-kernel stubs are staged as nonclaim fallback",
            "reason": "if the source functor cannot be signed, finite Delta_w can still be made testable without fake passes",
            "status": "KERNEL_STUBS_STAGED_NONCLAIM",
            "next_dependency": "WEP material tensor and/or R10 range kernel plus parent epsilon_A vector",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1892_2_next",
            "decision": "attack source-functor label forgetting next",
            "reason": "it is narrower than the full matter action signature and directly targets the coupling bottleneck",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1893 source-functor label forgetting or WEP kernel v0",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1892_0_primary",
            "selection_status": "selected",
            "target_doc": "1893-Y5-R2FR-source-functor-label-forgetting-or-deltaw-wep-kernel-v0.md",
            "target_script": "scripts/Y5_R2FR_source_functor_label_forgetting_or_deltaw_wep_kernel_v0_1893.py",
            "objective": "try to derive the source functor that forgets species labels and returns total Hilbert stress-energy; if it fails, build a WEP Delta_w projection-kernel v0 with all missing material/source inputs explicit",
            "success_condition": "parent-signed source-label forgetting, or a nonclaim WEP kernel row with material tensor, tau requirement, epsilon vector requirement, and no bound-as-prediction shortcut",
            "do_not": "do not claim WEP/local GR, do not treat Ward conservation as label forgetting, and do not score symbolic kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1892_0_project_position",
            "area": "GR/Newton reduction",
            "summary": "the exact ordinary-matter action signature needed for local GR has been identified but not derived",
            "risk_level": "CENTRAL_DERIVATION_GAP",
            "project_meaning": "MTS is no longer vague here; the failure is localized to a finite set of parent action clauses",
            "next_action": "derive source-label forgetting first because it is the narrowest coupling clause",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1892_1_empirical_branch",
            "area": "testability",
            "summary": "Delta_w projection kernels now have explicit WEP/R10/PPN/clock/orbital stub formulas",
            "risk_level": "TEST_BRANCH_PREPARED_NONCLAIM",
            "project_meaning": "if the derivation route fails, the coupling debt can be bounded rather than hand-waved",
            "next_action": "source WEP material tensor or R10 range kernel only after parent epsilon_A is defined",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "signature_attempt": signature_attempt_rows(),
        "clause_matrix": clause_matrix_rows(),
        "projection_kernels": projection_kernel_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    flag_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in flag_fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    blocked_markers = [
        "MISSING",
        "UNSIGNED",
        "NOT_DERIVED",
        "NOT_PARENT",
        "BLOCKED",
        "FAIL",
        "STUB",
        "NONCLAIM",
        "SYMBOLIC",
        "CLAIM_BLOCKED",
    ]
    readiness_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values())
            if any(marker in row_text for marker in blocked_markers):
                for field in readiness_fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/stub rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1892_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all source paths exist and needles found",
            "valid_for_claim": False,
        }
    )

    signature_rows_loaded = csv_rows(OUTPUTS["signature_attempt"])
    checks.append(
        {
            "validation_id": "VAL1892_01_signature_attempt",
            "status": "PASS"
            if any(row["attempt_id"] == "OMAS1892_2_signature_not_signed" and row["status"] == "ORDINARY_MATTER_ACTION_SIGNATURE_NOT_PARENT_SIGNED" for row in signature_rows_loaded)
            else "FAIL",
            "detail": "signature attempt remains unsigned",
            "valid_for_claim": False,
        }
    )

    clause_rows_loaded = csv_rows(OUTPUTS["clause_matrix"])
    checks.append(
        {
            "validation_id": "VAL1892_02_clause_matrix",
            "status": "PASS"
            if any(row["clause_id"] == "OMC1892_7_verdict" and row["current_status"] == "ORDINARY_MATTER_SIGNATURE_NOT_DERIVED" for row in clause_rows_loaded)
            else "FAIL",
            "detail": "all signature clauses recorded with nonclaim verdict",
            "valid_for_claim": False,
        }
    )

    kernel_rows_loaded = csv_rows(OUTPUTS["projection_kernels"])
    checks.append(
        {
            "validation_id": "VAL1892_03_projection_kernels",
            "status": "PASS"
            if len(kernel_rows_loaded) >= 6 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in kernel_rows_loaded)
            else "FAIL",
            "detail": "WEP/R10/PPN/clock/orbital kernel stubs are nonclaim and not score-ready",
            "valid_for_claim": False,
        }
    )

    dry_rows_loaded = csv_rows(OUTPUTS["dryrun_results"])
    checks.append(
        {
            "validation_id": "VAL1892_04_dryrun",
            "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows_loaded) else "FAIL",
            "detail": "dry-run rejects unsigned signature, closure-theorem substitution, missing epsilon, missing kernels, and bound shortcuts",
            "valid_for_claim": False,
        }
    )

    gate_rows_loaded = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1892_05_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1892_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows_loaded) else "FAIL",
            "detail": "claim gate remains blocked",
            "valid_for_claim": False,
        }
    )

    next_rows_loaded = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1892_06_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1892_0_primary" and row["selection_status"] == "selected" for row in next_rows_loaded) else "FAIL",
            "detail": "1893 source-functor label-forgetting target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1892_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1892_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1892_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    checks.append(
        {
            "validation_id": "VAL1892_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1892_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1892*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1892_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1892_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1892_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1892 ordinary-matter action signature or Delta_w projection kernels",
            "valid_for_claim": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1892 - Ordinary-Matter Action Signature Or Delta_w Species Projection Kernels

## Purpose

This checkpoint attacks the full ordinary-matter action signature needed for derived local GR/Newton source coupling.

## Result

- The exact signature is now written as a finite clause matrix: quotient geometry, matter bundle, vertical lift, constants, source-label forgetting, action-scale owner, and no shadow/boundary/readout re-entry.
- The signature is still not parent-signed. It remains a strong derivation contract, not a claim.
- Nonclaim `Delta_w_species` projection-kernel stubs are staged for WEP, R10, PPN, clocks, and orbital systems.
- Next best target is narrower: derive the source functor that forgets species labels before coupling, or build WEP kernel v0 as fallback.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Signature Attempt

{markdown_table(rows_by_name["signature_attempt"])}

## Signature Clause Matrix

{markdown_table(rows_by_name["clause_matrix"])}

## Delta_w Projection Kernel Stubs

{markdown_table(rows_by_name["projection_kernels"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
