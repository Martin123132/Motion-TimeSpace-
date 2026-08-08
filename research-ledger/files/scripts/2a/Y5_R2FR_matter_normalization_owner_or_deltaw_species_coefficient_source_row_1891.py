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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1891"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1891-Y5-R2FR-matter-normalization-owner-or-deltaw-species-coefficient-source-row.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1890_doc": ROOT / "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md",
    "1890_validation": OUT / "P8_Y5_BRR545_1890_VALIDATION.csv",
    "1890_normalization_owner": OUT / "P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv",
    "1890_component_row": OUT / "P8_Y5_PARENT_QLOC_1890_DELTAW_SPECIES_FIRST_COMPONENT_ROW_NONCLAIM.csv",
    "1890_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv",
    "1890_next": OUT / "P8_Y5_PARENT_QLOC_1890_NEXT_TARGET.csv",
    "954_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "955_schema": OUT / "P8_Y5_R10_955_RESIDUAL_INPUT_SCHEMA.csv",
    "1045_matter_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1088_minimal_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1097_constant_universality": OUT / "P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
    "1098_owner_signature": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1098_action_theorem": OUT / "P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv",
    "1098_forbidden_vertex": OUT / "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
    "constant_contract": OUT / "P8_constant_sector_universality_CONTRACT.csv",
    "1488_fixed_constants": OUT / "P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv",
}


SOURCE_NEEDLES = {
    "1890_doc": [
        "MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
        "Delta_w_species remains a live finite component",
    ],
    "1890_validation": ["VAL1890_OVERALL,PASS"],
    "1890_normalization_owner": [
        "MNO1890_5_verdict",
        "MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
    ],
    "1890_component_row": [
        "DWS1890_0_species_prefactor_component",
        "SOURCE_BACKED_COMPONENT_DEFINED_NONNUMERIC",
    ],
    "1890_projection_requirements": [
        "PRJ1890_1_WEP",
        "PRJ1890_2_R10",
        "MISSING_PARENT_NUMERIC_COEFFICIENT",
    ],
    "1890_next": ["NEXT1890_0_primary", "matter-normalization-owner"],
    "954_clause": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    "955_schema": ["epsilon", "source"],
    "1045_matter_functor": [
        "MFS1045_5_constants_split",
        "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
    ],
    "1088_minimal_signature": [
        "MOMS1088_3_constant_superselection",
        "MOMS1088_4_no_species_weights",
        "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
    ],
    "1097_constant_universality": [
        "CSU1097_5_verdict",
        "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
    ],
    "1098_owner_signature": [
        "OCS1098_4_source_weight_exclusion",
        "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
    ],
    "1098_action_theorem": [
        "OCT1098_1_chain_rule",
        "OWNER_THEOREM_NOT_PROMOTED",
    ],
    "1098_forbidden_vertex": [
        "FV1098_6_source_weight_X",
        "forbidden_required_but_currently_legal",
    ],
    "constant_contract": [
        "C3_universal_source_variation",
        "not_parent_derived",
    ],
    "1488_fixed_constants": [
        "FCR1488_2_common_calibration",
        "CONSTANT_DEBT_RETAINED",
    ],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1891_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_1891_MATTER_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "nongrav_owner_audit": OUT / "P8_Y5_PARENT_QLOC_1891_NONGRAV_STANDARD_OWNER_AUDIT.csv",
    "coefficient_row": OUT / "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv",
    "projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1891_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1891_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1891_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1891_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1891_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1891_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1891_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1891_VALIDATION.csv",
}


BRANCH_COPIES = {
    "theorem_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["theorem_attempt"].name,
    "nongrav_owner_audit": QUEUE / "JR1891_NONGRAV_STANDARD_OWNER_AUDIT_NONCLAIM.csv",
    "coefficient_row": SOURCE_WEIGHT_DOCS / "DELTAW_SPECIES1891_COEFFICIENT_ROW_NONCLAIM.csv",
    "projection_requirements": QUEUE / "JR1891_DELTAW_SPECIES_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
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
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "MNO1891_0_target",
            "claim_piece": "matter-normalization owner",
            "mathematical_statement": "ordinary matter normalizations are owned by nongravitational representation/current data before the gravitational source current is extracted",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "would make any source-only w_A a duplicate label rather than a new physical coupling",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "MNO1891_1_conditional_double_counting",
            "claim_piece": "double-counting lemma",
            "mathematical_statement": "if S_matter=sum_A S_A[Psi_A,e_obs,A_obs,theta_A] with theta_A fixed/owned and J_grav=delta S_matter/delta e_obs before readout, then replacing J_grav by sum_A w_A J_A adds a second species label not present in the parent matter object",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "linearity of Hilbert variation gives the common current; source-only relative weights are extra pre-variation structure unless the parent action declares them",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_1_no_source_prefactors; P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv:MOMS1088_4_no_species_weights",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "MNO1891_2_nongrav_owner_route",
            "claim_piece": "nongravitational standard owner route",
            "mathematical_statement": "masses, charges, alpha, spectra, clock constants, and current normalizations must be fixed representation/superselection data or separately retained residual fields with Lie_v theta_A=0",
            "status": "CONDITIONAL_SUPPORT_ONLY",
            "proof_or_obstruction": "1097/1098/1488 give the exact owner clauses but mark the parent signature and forbidden-vertex closure unsigned",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_6_verdict; P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv:FCR1488_3_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "MNO1891_3_countermodel",
            "claim_piece": "owner route can fail",
            "mathematical_statement": "q(Phi) fixed and theta_A fixed still allow DeltaS=sum_A epsilon_A S_A or a species-dependent measure Jacobian unless the parent action grammar forbids that slot",
            "status": "COUNTERMODEL_RETAINED",
            "proof_or_obstruction": "this creates a relative source charge while preserving many nongravitational readouts, so it cannot be dismissed by field rescaling or classical EOM alone",
            "source_anchor": "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv:FV1098_6_source_weight_X; P8_constant_sector_universality_CONTRACT.csv:C3_universal_source_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "MNO1891_4_common_mode_guard",
            "claim_piece": "G/GM absorption guard",
            "mathematical_statement": "a common multiplier can be calibration-only only after uniqueness and silence of species, time, range, frame, and readout dependence are parent-signed",
            "status": "COMMON_MODE_ONLY_NOT_RELATIVE_PROOF",
            "proof_or_obstruction": "absorbing the relative vector into G_N/GM would hide exactly the WEP/R10/PPN residual being audited",
            "source_anchor": "P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv:FCR1488_2_common_calibration; P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_2_common_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "MNO1891_5_verdict",
            "claim_piece": "promote matter-normalization owner for current MTS",
            "mathematical_statement": "ordinary representation/current standards fully own matter normalization and exclude every active-source-only w_A before variation",
            "status": "MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            "proof_or_obstruction": "ordinary matter action signature, source-weight exclusion, hbar/measure owner, and radiative/readout closure remain unsigned in the cited corpus",
            "source_anchor": "MNO1891_1_conditional_double_counting through MNO1891_4_common_mode_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def nongrav_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NSO1891_0_alpha_maxwell_norm",
            "standard": "alpha_EM and Maxwell/gauge kinetic normalization",
            "owner_requirement": "fixed gauge representation/kinetic owner; no independent f_X(Xhat) F^2 or lambda_A F^2 source channel",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "gap": "unique EM/gauge normalization is written as a route but not parent-signed",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_1_unique_EM_owner; P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv:FV1098_1_scalar_F2",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_1_mass_yukawa_qcd_binding",
            "standard": "masses, Yukawas, QCD/binding response, material constants",
            "owner_requirement": "fixed representation/superselection data or explicitly retained residual fields; no Xhat-dependent masses/binding slots",
            "current_status": "NOT_PARENT_SIGNED",
            "gap": "mass/binding/clock/WEP material channels stay live until a parent action forbids active constant vertices",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_2_matter_spectrum_owner; P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv:FV1098_2_mass_X;FV1098_4_binding_X",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_2_clock_spectral_readout",
            "standard": "clock and spectral readouts",
            "owner_requirement": "clock frequencies descend from quotient-owned coframe plus fixed constants; no hidden readout or shadow clock slot",
            "current_status": "UNSIGNED",
            "gap": "clock residual rows remain separate because readout closure is not parent-derived",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_3_clock_readout_owner; P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv:FV1098_5_clock_readout_X",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_3_source_weight_exclusion",
            "standard": "active gravitational source current",
            "owner_requirement": "source current is the common observed-coframe Hilbert variation of the same parent matter action; no kappa_A, w_A, or material-only multiplier",
            "current_status": "UNSIGNED",
            "gap": "source-current Ward conservation is not enough to enforce species-blind source weights",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_4_source_weight_exclusion; P8_constant_sector_universality_CONTRACT.csv:C3_universal_source_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_4_parent_matter_functor",
            "standard": "ordinary matter bundle/action signature",
            "owner_requirement": "one parent matter functor assigns Psi_A, e_obs, A_obs, theta_A, vertical lifts, and no shadow frame/domain for all ordinary species",
            "current_status": "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "gap": "the signature is exact as a contract but not constructed as one parent action",
            "source_anchor": "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv:MFS1045_6_verdict; P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv:MOMS1088_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_5_hbar_measure_owner",
            "standard": "hbar/statistical measure/common action scale",
            "owner_requirement": "one parent phase/measure normalization for all ordinary matter; no species-only measure Jacobian",
            "current_status": "OWNER_NOT_DERIVED",
            "gap": "species-dependent effective hbar_A or measure factors can mimic a source prefactor unless signed away",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_3_hbar_measure_owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_6_radiative_readout_closure",
            "standard": "effective/readout closure",
            "owner_requirement": "forbidden source and constant vertices do not re-enter through renormalization, boundary/domain classes, or post-variation readout",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "gap": "bare action silence would not survive into observed tests without this closure",
            "source_anchor": "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv:OCS1098_5_radiative_readout_closure; P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_4_readout_spurion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSO1891_7_verdict",
            "standard": "matter-normalization owner from nongrav standards",
            "owner_requirement": "all ordinary constants/current normalizations are parent-owned and every active-source-only relative coefficient is either theorem-zero or retained as a finite residual row",
            "current_status": "NONGRAV_STANDARD_OWNER_NOT_DERIVED",
            "gap": "enough structure exists to write the contract sharply, but not enough to claim Delta_w_species=0",
            "source_anchor": "NSO1891_0_alpha_maxwell_norm through NSO1891_6_radiative_readout_closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coefficient_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_row_id": "DWS1891_0_delta_w_species_coefficient_slot",
            "branch_id": BRANCH_ID,
            "component_basis": "Delta_w_component_basis_v2_matter_normalization_owner",
            "component": "Delta_w_species",
            "coefficient_symbol": "epsilon_A",
            "component_definition": "relative active-source/action normalization after projecting out the universal common mode",
            "basis_formula": "w_A = w_common * (1 + epsilon_A), with sum_A p_A epsilon_A = 0 for the chosen material/source composition weights p_A",
            "coefficient_origin": "symbolic free coefficient retained because the matter-normalization owner/no-source-prefactor theorem is not parent-derived",
            "current_value": "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE",
            "units": "dimensionless",
            "source_path": str(INPUTS["1890_component_row"]),
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_DELTAW_SPECIES_FIRST_COMPONENT_ROW_NONCLAIM.csv:DWS1890_0_species_prefactor_component",
            "derivation_status": "SOURCE_BACKED_COEFFICIENT_SLOT_SYMBOLIC_NONNUMERIC",
            "zero_route_status": "MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            "missing_for_claim": "parent numeric or parent-derived symbolic epsilon_A vector; material basis p_A; no-cancellation norm; tau/K/Qbar projections",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "component_row_id": "DWS1891_1_common_mode_projector",
            "branch_id": BRANCH_ID,
            "component_basis": "Delta_w_component_basis_v2_matter_normalization_owner",
            "component": "P_perp_common_mode",
            "coefficient_symbol": "P_perp",
            "component_definition": "projector that removes any universal action-scale/common-G calibration mode before WEP/R10/PPN scoring",
            "basis_formula": "Delta_w_species = P_perp w, P_perp = I - u p^T/(p^T u) once the arena composition weights p are sourced",
            "coefficient_origin": "symbolic projector required by the common-mode guard; not an empirical pass",
            "current_value": "SYMBOLIC_PROJECTOR_NO_ARENA_COMPOSITION_VECTOR",
            "units": "dimensionless",
            "source_path": str(INPUTS["1890_normalization_owner"]),
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_2_common_mode; P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv:FCR1488_2_common_calibration",
            "derivation_status": "SCHEMA_ONLY_NOT_SCOREABLE",
            "zero_route_status": "COMMON_MODE_NOT_RELATIVE_PROOF",
            "missing_for_claim": "arena composition weights and proof that only the common mode is calibratable",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PRJ1891_0_core",
            "arena": "core_component_vector",
            "formula": "Delta_w_species = P_perp {epsilon_A}; no arena score before p_A, norm, and parent coefficient origin are fixed",
            "required_inputs": "species/material basis; common-mode projector; parent coefficient vector; no-cancellation norm",
            "current_status": "SYMBOLIC_COMPONENT_ONLY_PARENT_COEFFICIENT_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_0_delta_w_species_coefficient_slot",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1891_1_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "formula": "eta_TiPt = tau_WEP * DeltaQ_TiPt dot Delta_w_species",
            "required_inputs": "official Ti/Pt composition tensor; Earth/source worldtube; tau_WEP; force/readout convention; parent epsilon_A vector",
            "current_status": "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv:PRJ1890_1_WEP",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1891_2_R10",
            "arena": "R10_short_range",
            "formula": "alpha_Delta_w(lambda) = K_R10(lambda) * Qbar_source_test(lambda) dot Delta_w_species",
            "required_inputs": "K_R10(lambda); Qbar_source_test(lambda); tau_R10(lambda); range/kernel convention; digitized bound curve; parent epsilon_A vector",
            "current_status": "SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv:PRJ1890_2_R10",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1891_3_PPN",
            "arena": "PPN_beta_gamma_source",
            "formula": "Delta beta_source <= K_PPN * (||Delta_w_species|| + |beta_w_source| + |beta_w_test|)",
            "required_inputs": "weak-field source solution; source/test split; PPN operator norm; beta_w normalization; parent epsilon_A vector",
            "current_status": "MISSING_PPN_OPERATOR_NORM_AND_SOURCE_TEST_LEGS",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv:PRJ1890_3_PPN",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1891_4_clock",
            "arena": "clock_and_constant_drift",
            "formula": "|Delta nu_i/nu_i| <= |K_clock_i dot Delta_w_species| |tau_clock| after alpha/mass split is sourced",
            "required_inputs": "clock mass/alpha decomposition; source body composition; tau_clock; local no-running theorem or finite clock coefficient rows",
            "current_status": "PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv:PRJ1890_4_clock_orbital",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ1891_5_orbital",
            "arena": "orbital_GM_and_inverse_square",
            "formula": "Delta(GM)_obs/GM <= K_orbital dot Delta_w_species plus any retained beta_w/source-test legs",
            "required_inputs": "source body composition; orbital GM convention; tau_orbital; inverse-square kernel; parent epsilon_A vector",
            "current_status": "PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv:PRJ1890_4_clock_orbital",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1891_0_owner_unsigned",
            "matter_normalization_owner_parent_signed": False,
            "coefficient_kind": "symbolic_free_no_parent_value",
            "arena_projection_ready": False,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_MATTER_NORMALIZATION_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_1_constant_owner_not_source_owner",
            "matter_normalization_owner_parent_signed": False,
            "coefficient_kind": "constant_owner_contract_only",
            "arena_projection_ready": False,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_CONSTANT_OWNER_NOT_SOURCE_PREFACTOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_2_representation_data_not_active_weight",
            "matter_normalization_owner_parent_signed": False,
            "coefficient_kind": "representation_label_only",
            "arena_projection_ready": False,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_REPRESENTATION_DATA_NOT_ACTIVE_SOURCE_WEIGHT",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_3_missing_parent_coefficient",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "missing_parent_numeric_or_symbolic",
            "arena_projection_ready": True,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_4_bound_anchor_shortcut",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "parent_numeric",
            "arena_projection_ready": True,
            "uses_bound_anchor_as_prediction": True,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_5_missing_projection",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "parent_numeric",
            "arena_projection_ready": False,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_MISSING_TAU_K_QBAR_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_6_absorb_relative_weight",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "parent_numeric",
            "arena_projection_ready": True,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": True,
            "uses_cancellation_only": False,
            "expected_status": "REFUSED_G_ABSORPTION_WITHOUT_UNIQUENESS",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_7_cancellation_only",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "parent_numeric",
            "arena_projection_ready": True,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": True,
            "expected_status": "REFUSED_CANCELLATION_ONLY",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1891_8_schema_math_only",
            "matter_normalization_owner_parent_signed": True,
            "coefficient_kind": "symbolic_projector_only",
            "arena_projection_ready": False,
            "uses_bound_anchor_as_prediction": False,
            "absorbs_relative_weight_into_G": False,
            "uses_cancellation_only": False,
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    owner_signed = bool_string(row["matter_normalization_owner_parent_signed"]) == "true"
    coefficient_kind = str(row["coefficient_kind"])
    projection_ready = bool_string(row["arena_projection_ready"]) == "true"
    bound_shortcut = bool_string(row["uses_bound_anchor_as_prediction"]) == "true"
    absorbs_g = bool_string(row["absorbs_relative_weight_into_G"]) == "true"
    cancellation = bool_string(row["uses_cancellation_only"]) == "true"

    if not owner_signed:
        if coefficient_kind == "constant_owner_contract_only":
            status = "REFUSED_CONSTANT_OWNER_NOT_SOURCE_PREFACTOR"
        elif coefficient_kind == "representation_label_only":
            status = "REFUSED_REPRESENTATION_DATA_NOT_ACTIVE_SOURCE_WEIGHT"
        else:
            status = "REFUSED_MATTER_NORMALIZATION_OWNER_UNSIGNED"
    elif coefficient_kind == "missing_parent_numeric_or_symbolic":
        status = "REFUSED_MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT"
    elif bound_shortcut:
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    elif not projection_ready and coefficient_kind == "symbolic_projector_only":
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
    elif not projection_ready:
        status = "REFUSED_MISSING_TAU_K_QBAR_PROJECTION"
    elif absorbs_g:
        status = "REFUSED_G_ABSORPTION_WITHOUT_UNIQUENESS"
    elif cancellation:
        status = "REFUSED_CANCELLATION_ONLY"
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


def runner_refusal_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refusal_order = []
    seen = set()
    for row in results:
        status = row["computed_status"]
        if status not in seen:
            refusal_order.append(status)
            seen.add(status)
    return [
        {
            "runner_id": "RUN1891_0_deltaw_species_source_row_smoke_runner",
            "branch_id": BRANCH_ID,
            "input_component": "Delta_w_species",
            "accepted_for_scoring": False,
            "refusal_statuses": "; ".join(refusal_order),
            "minimum_to_unlock": "parent-signed matter-normalization owner or parent numeric/symbolic epsilon_A vector, plus tau/K/Qbar/material projections and real bound curves",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1891_0_matter_normalization_owner",
            "condition": "ordinary matter normalization/source-current owner is parent-signed",
            "current_status": "FAIL_MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_MATTER_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv:MNO1891_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1891_1_coefficient_value",
            "condition": "Delta_w_species coefficient vector has parent numeric or parent-derived symbolic values",
            "current_status": "FAIL_SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_0_delta_w_species_coefficient_slot",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1891_2_projection_kernels",
            "condition": "WEP/R10/PPN/clock/orbital tau, K, and Qbar/material projections are sourced",
            "current_status": "FAIL_PROJECTION_REQUIREMENTS_BLOCKED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_PROJECTION_REQUIREMENTS.csv:PRJ1891_1_WEP..PRJ1891_5_orbital",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1891_3_bound_shortcut_guard",
            "condition": "external bounds are used only after a prediction exists, never as the prediction",
            "current_status": "PASS_GUARD_WRITTEN_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_DRYRUN_RESULTS.csv:DRY1891_4_bound_anchor_shortcut",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1891_4_verdict",
            "condition": "all local-GR/R10/WEP/PPN gates pass",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1891_0_matter_normalization_owner through CG1891_3_bound_shortcut_guard",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1891_0_theorem_route",
            "decision": "do not claim Delta_w_species=0",
            "reason": "the double-counting theorem is exact only after the matter-normalization owner and source-weight exclusion are parent-signed",
            "status": "DERIVATION_ROUTE_STILL_OPEN_BUT_UNSIGNED",
            "next_dependency": "ordinary matter action signature and source-current owner must be signed in the parent action",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1891_1_component_route",
            "decision": "retain Delta_w_species as a symbolic nonclaim coefficient row",
            "reason": "this preserves the coupling debt honestly instead of hiding it in G, classical EOM rescaling, or a bound anchor",
            "status": "NONCLAIM_ROW_STAGED",
            "next_dependency": "source parent coefficient vector or build arena projection kernels for an empirical bound intake",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1891_2_project_strategy",
            "decision": "best next shot is the ordinary-matter action signature with projection-kernel fallback",
            "reason": "if the signature closes, the local branch strengthens sharply; if not, the finite-coupling branch becomes testable without overclaiming",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1892 ordinary matter action signature or Delta_w_species projection kernels",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1891_0_primary",
            "selection_status": "selected",
            "target_doc": "1892-Y5-R2FR-ordinary-matter-action-signature-or-deltaw-species-projection-kernels.md",
            "target_script": "scripts/Y5_R2FR_ordinary_matter_action_signature_or_deltaw_species_projection_kernels_1892.py",
            "objective": "try to parent-sign the ordinary-matter action signature that owns e_obs, A_obs, theta_A, source variation, and no w_A slots; if it fails, build nonclaim WEP/R10/PPN/clock/orbital projection kernels for Delta_w_species",
            "success_condition": "either a parent-signed no-source-weight ordinary matter signature, or sourced projection-kernel rows that keep every arena blocked until a parent epsilon_A vector exists",
            "do_not": "do not claim local GR, do not treat a constant-owner contract as a source-current proof, do not absorb relative weights into G, and do not use bounds as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1891_0_main_bottleneck",
            "area": "local GR / Newton source coupling",
            "summary": "the coupling bottleneck is now sharply localized to the matter-normalization/source-current owner",
            "risk_level": "MAIN_BOTTLENECK",
            "project_meaning": "this is not a random loose end; it is the exact place where GR recovery either becomes a theorem or becomes a finite residual branch",
            "next_action": "sign the ordinary-matter action signature or build Delta_w_species projection kernels",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1891_1_strength",
            "area": "derivation discipline",
            "summary": "the conditional double-counting theorem is clean and useful",
            "risk_level": "PROMISING_CONDITIONAL",
            "project_meaning": "if the parent action can forbid source-only weights, Delta_w_species collapses without fitting",
            "next_action": "promote the owner route from contract to parent action",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1891_2_empirical_readiness",
            "area": "test branch",
            "summary": "nonclaim coefficient and projection requirements are staged, but no arena score is allowed yet",
            "risk_level": "EVIDENCE_GATE_HELD",
            "project_meaning": "the framework is being protected from fake wins while still preparing for WEP/R10/PPN/clock/orbital tests",
            "next_action": "source parent epsilon_A or projection kernels",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    results = dryrun_result_rows(cases)
    return {
        "source_register": source_register_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "nongrav_owner_audit": nongrav_owner_audit_rows(),
        "coefficient_row": coefficient_row_rows(),
        "projection_requirements": projection_requirement_rows(),
        "dryrun_cases": cases,
        "dryrun_results": results,
        "runner_refusal": runner_refusal_rows(results),
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
    flag_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "gate_pass",
        "accepted_for_scoring",
    }
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
        "COUNTERMODEL",
        "COUNTEREXAMPLE",
        "NONNUMERIC",
        "NO_PARENT_VALUE",
        "LEGAL",
        "CLAIM_BLOCKED",
    ]
    readiness_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "gate_pass",
        "accepted_for_scoring",
    }
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values())
            if any(marker in row_text for marker in blocked_markers):
                for field in readiness_fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:  # pragma: no cover - validation diagnostic
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    source_rows = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1891_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows) else "FAIL",
            "detail": "all source paths exist and needles found",
            "valid_for_claim": False,
        }
    )

    theorem_rows_loaded = csv_rows(OUTPUTS["theorem_attempt"])
    checks.append(
        {
            "validation_id": "VAL1891_01_theorem_verdict",
            "status": "PASS"
            if any(row["theorem_id"] == "MNO1891_5_verdict" and row["status"] == "MATTER_NORMALIZATION_OWNER_NOT_DERIVED" for row in theorem_rows_loaded)
            else "FAIL",
            "detail": "theorem route remains conditional, not claimed",
            "valid_for_claim": False,
        }
    )

    owner_rows_loaded = csv_rows(OUTPUTS["nongrav_owner_audit"])
    checks.append(
        {
            "validation_id": "VAL1891_02_nongrav_owner_audit",
            "status": "PASS"
            if any(row["audit_id"] == "NSO1891_7_verdict" and row["current_status"] == "NONGRAV_STANDARD_OWNER_NOT_DERIVED" for row in owner_rows_loaded)
            else "FAIL",
            "detail": "nongravitational owner route audited and retained unsigned",
            "valid_for_claim": False,
        }
    )

    coeff_rows_loaded = csv_rows(OUTPUTS["coefficient_row"])
    coeff_ok = all(
        row["units"] == "dimensionless"
        and row["valid_for_claim"] == "False"
        and row["score_ready"] == "False"
        and Path(row["source_path"]).exists()
        for row in coeff_rows_loaded
    )
    checks.append(
        {
            "validation_id": "VAL1891_03_coefficient_row_nonclaim",
            "status": "PASS" if coeff_ok else "FAIL",
            "detail": "Delta_w_species coefficient rows are dimensionless, sourced, symbolic/nonclaim, and not score-ready",
            "valid_for_claim": False,
        }
    )

    projection_rows_loaded = csv_rows(OUTPUTS["projection_requirements"])
    checks.append(
        {
            "validation_id": "VAL1891_04_projection_requirements",
            "status": "PASS"
            if len(projection_rows_loaded) >= 6 and all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in projection_rows_loaded)
            else "FAIL",
            "detail": "core, WEP, R10, PPN, clock, and orbital projection requirements remain blocked",
            "valid_for_claim": False,
        }
    )

    result_rows_loaded = csv_rows(OUTPUTS["dryrun_results"])
    checks.append(
        {
            "validation_id": "VAL1891_05_dryrun_statuses",
            "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in result_rows_loaded) else "FAIL",
            "detail": "dry-run runner refuses unsigned owner, missing coefficients, bound shortcuts, missing projections, G absorption, cancellation-only, and schema-only rows",
            "valid_for_claim": False,
        }
    )

    runner_rows_loaded = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1891_06_runner_refusal",
            "status": "PASS" if all(row["accepted_for_scoring"] == "False" and row["valid_prediction_row"] == "False" for row in runner_rows_loaded) else "FAIL",
            "detail": "runner refuses scoring until parent coefficients and projections exist",
            "valid_for_claim": False,
        }
    )

    gate_rows_loaded = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1891_07_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1891_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows_loaded) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
        }
    )

    decision_rows_loaded = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1891_08_decision",
            "status": "PASS" if any(row["decision_id"] == "DEC1891_2_project_strategy" and row["status"] == "NEXT_TARGET_SELECTED" for row in decision_rows_loaded) else "FAIL",
            "detail": "next strategy selected",
            "valid_for_claim": False,
        }
    )

    next_rows_loaded = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1891_09_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1891_0_primary" and row["selection_status"] == "selected" for row in next_rows_loaded) else "FAIL",
            "detail": "1892 target written",
            "valid_for_claim": False,
        }
    )

    status_rows_loaded = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1891_10_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows_loaded) else "FAIL",
            "detail": "project bottleneck snapshot identifies coupling/source owner",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1891_11_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1891_12_blocked_markers_not_ready",
            "status": "PASS" if blocked_ok else "FAIL",
            "detail": blocked_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1891_13_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    checks.append(
        {
            "validation_id": "VAL1891_14_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1891_15_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1891*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1891_16_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1891_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1891_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1891 matter-normalization owner or Delta_w_species coefficient source row",
            "valid_for_claim": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1891 - Matter-Normalization Owner Or Delta_w Species Coefficient Source Row

## Purpose

This checkpoint tries the derivation-first route for the local source coupling problem:

1. Prove that ordinary nongravitational standards own matter normalization, so a source-only `w_A` is double-counting.
2. If the proof is not parent-signed, retain `Delta_w_species` as a symbolic nonclaim coefficient row instead of hiding it in `G`, classical EOM rescaling, or a bound anchor.

## Result

- The conditional theorem is clean: if the parent ordinary-matter action owns `theta_A`, `e_obs`, `A_obs`, the Hilbert source current, the common action/measure scale, and variation-before-readout, then source-only `w_A S_A` is forbidden as duplicate structure.
- Current MTS does not yet have that parent-signed owner. The exact verdict remains `MATTER_NORMALIZATION_OWNER_NOT_DERIVED`.
- `Delta_w_species` is therefore retained as a symbolic, dimensionless, source-backed, nonclaim coefficient row. It is not score-ready for WEP, R10, PPN, clocks, or orbital systems.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Matter-Normalization Owner Theorem Attempt

{markdown_table(rows_by_name["theorem_attempt"])}

## Nongravitational Standard Owner Audit

{markdown_table(rows_by_name["nongrav_owner_audit"])}

## Delta_w Species Coefficient Rows

{markdown_table(rows_by_name["coefficient_row"])}

## Projection Requirements

{markdown_table(rows_by_name["projection_requirements"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

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
