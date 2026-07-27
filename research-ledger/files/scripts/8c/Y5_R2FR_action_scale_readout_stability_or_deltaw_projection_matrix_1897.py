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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1897"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1896_doc": ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md",
    "1896_validation": OUT / "P8_Y5_BRR545_1896_VALIDATION.csv",
    "1896_nohom_attempt": OUT / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
    "1896_nohom_gate": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv",
    "1896_basis": OUT / "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
    "1896_next": OUT / "P8_Y5_PARENT_QLOC_1896_NEXT_TARGET.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1067_action_owner": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1067_consequence": OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
    "1888_readout_stability": OUT / "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv",
    "1471_radiative_readout": OUT / "P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv",
    "1816_variation_before_readout": OUT / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
    "1675_source_readout_descent": OUT / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
    "1700_no_reentry_target": OUT / "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv",
    "1486_shadow_reentry": OUT / "P8_Y5_R10_1486_NO_SHADOW_READOUT_REENTRY_AUDIT.csv",
    "1454_vbr_attempt": OUT / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv",
    "1454_order_audit": OUT / "P8_Y5_R10_1454_SOURCE_READOUT_ORDER_AUDIT.csv",
    "1454_ca_split": OUT / "P8_Y5_R10_1454_C_A_READOUT_CALIBRATION_SPLIT.csv",
    "1490_species_readout": OUT / "P8_Y5_R10_1490_SPECIES_READOUT_DEPENDENCY_AUDIT.csv",
    "1888_finite_vector": OUT / "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv",
    "1890_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1890_COMPONENT_ROW_PROJECTION_REQUIREMENTS.csv",
    "1892_kernel_stubs": OUT / "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1896_doc": ["READOUT_MEASURE_STABILITY_UNSIGNED", "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md"],
    "1896_validation": ["VAL1896_OVERALL,PASS"],
    "1896_nohom_attempt": ["NH1896_4_readout_measure_gap", "READOUT_MEASURE_STABILITY_UNSIGNED"],
    "1896_nohom_gate": ["NHG1896_3_exhaustion_stability", "NOHOM_CLAIM_BLOCKED"],
    "1896_basis": ["DWB1896_0_vector_space", "DWB1896_6_no_cancellation_policy"],
    "1896_next": ["NEXT1896_0_primary", "action-scale/readout stability"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1067_action_owner": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_consequence": ["SWC1067_4_verdict", "finite Delta_w*tau_WEP branch remains"],
    "1888_readout_stability": ["ROS1888_6_verdict", "READOUT_STABILITY_NOT_PARENT_DERIVED"],
    "1471_radiative_readout": ["RRC1471_3_verdict", "REFUSE_PROMOTION_START_PREDICTION_FILL"],
    "1816_variation_before_readout": ["VBR1816_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"],
    "1675_source_readout_descent": ["SRD1675_5_verdict", "SOURCE_READOUT_DESCENT_NOT_CLOSED"],
    "1700_no_reentry_target": ["RNR1700_2_commutator", "READOUT_NO_REENTRY_SELECTED"],
    "1486_shadow_reentry": ["NSR1486_4_verdict", "OBSTRUCTION_SURVIVES"],
    "1454_vbr_attempt": ["VBR1454_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"],
    "1454_order_audit": ["SOA1454_5_verdict", "FAIL_CURRENT_PROOF"],
    "1454_ca_split": ["CAS1454_4_verdict", "PARTIAL_NOT_CLAIM"],
    "1490_species_readout": ["SRD1490_4_verdict", "OPEN_DEPENDENCIES_RETAINED"],
    "1888_finite_vector": ["FDV1888_0_core_vector", "FDV1888_5_orbital"],
    "1890_projection_requirements": ["PRJ1890_1_WEP", "PRJ1890_4_clock_orbital"],
    "1892_kernel_stubs": ["DK1892_1_WEP", "DK1892_5_orbital"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1897_SOURCE_REGISTER.csv",
    "stability_attempt": OUT / "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
    "stability_gate": OUT / "P8_Y5_PARENT_QLOC_1897_STABILITY_GATE.csv",
    "projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1897_STABILITY_PROJECTION_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1897_STABILITY_PROJECTION_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1897_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1897_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1897_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1897_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1897_VALIDATION.csv",
}


BRANCH_COPIES = {
    "stability_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["stability_attempt"].name,
    "projection_matrix": SOURCE_WEIGHT_DOCS / "DELTAW_ARENA_PROJECTION_MATRIX_1897_NONCLAIM.csv",
    "projection_requirements": QUEUE / "JR1897_DELTAW_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
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


def stability_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ASR1897_0_target",
            "claim_piece": "action-scale/readout stability after tree-level no-Hom",
            "formal_statement": "After parent variation, no measure, radiative, readout, material, source-worldtube, or clock/orbit map can create Coeff_active_source[species] terms if every such map is a domain-preserving postprocessing functor.",
            "status": "TARGET_EXACT",
            "proof_or_obstruction": "this is the exact theorem needed so source weights do not come back after the 1896 no-Hom grammar branch",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv:NH1896_4_readout_measure_gap; P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv:RNR1700_2_commutator",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_1_exact_conditional_theorem",
            "claim_piece": "one-owner stability theorem",
            "formal_statement": "If S_parent has one hbar/action-measure owner, one current normalization owner, variation occurs before all readouts, and every effective/readout map R is a typed endofunctor preserving the quotient coefficient domain, then D_label R(C_source)=0 and Delta_w tree-zero is stable.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "composition of coefficient-domain-preserving maps cannot enlarge the argument domain to SpeciesLabel; the derivative along a label-only vertical generator is zero",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_5_verdict; P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv:RRC1471_0_exact_conditional; P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv:VBR1816_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_2_action_scale_gap",
            "claim_piece": "single action scale / measure owner",
            "formal_statement": "hbar_parent, Dmu_parent, current normalization, and source normalization must be owned by one parent sector and must not admit species-only Jacobians.",
            "status": "ACTION_SCALE_OWNER_UNSIGNED",
            "proof_or_obstruction": "1067 leaves hbar/measure/current/readout ownership unsigned, and relative action-scale factors remain a live countermodel",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_4_verdict; P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv:SWC1067_1_relative_action_scale",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_3_readout_gap",
            "claim_piece": "readout no-reentry",
            "formal_statement": "[delta_parent, R_readout] must not produce source-only coefficient terms; if nonzero, the commutator becomes a finite residual transfer row.",
            "status": "READOUT_NO_REENTRY_UNSIGNED",
            "proof_or_obstruction": "readout domain separation is conditional; reduced EFT/readout branches, hidden marker return, and no-hidden-visible coefficient morphisms remain unsigned",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv:ROS1888_6_verdict; P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv:RNR1700_2_commutator",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_4_radiative_gap",
            "claim_piece": "radiative/effective closure",
            "formal_statement": "S_eff, thresholds, clock/WEP/R10 readouts, and laboratory kernels must preserve the no-species coefficient grammar after coarse-graining.",
            "status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "proof_or_obstruction": "1471 proves only the conditional domain-preservation theorem; threshold/readout and observed-lab bridge are not parent-signed",
            "source_anchor": "P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv:RRC1471_3_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_5_variation_order_gap",
            "claim_piece": "variation before readout/source-worldtube",
            "formal_statement": "post-current c_A and selector F(T_A,A) are killed only if they are downstream of the Hilbert/Noether source and cannot enter S_parent or S_eff before variation.",
            "status": "VARIATION_BEFORE_READOUT_UNSIGNED",
            "proof_or_obstruction": "1816 and 1454 kill post-current/readout factors conditionally, but pre-action weights and source-worldtube transfers remain live",
            "source_anchor": "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv:VBR1816_6_verdict; P8_Y5_R10_1454_C_A_READOUT_CALIBRATION_SPLIT.csv:CAS1454_4_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ASR1897_6_verdict",
            "claim_piece": "promote stable source-weight zero",
            "formal_statement": "Current MTS parent primitives prove one-owner action scale plus readout/effective no-reentry, so Delta_w=0 is stable across local arenas.",
            "status": "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the exact theorem is now sharp, but action-scale owner, readout no-reentry, radiative closure, variation-order/worldtube split, and parent Delta_w values are unsigned; must use finite projection matrix branch",
            "source_anchor": "ASR1897_0_target through ASR1897_5_variation_order_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def stability_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "STG1897_0_action_owner",
            "required_clause": "single parent hbar/action-measure/current owner",
            "current_status": "FAIL_OWNER_NOT_DERIVED",
            "if_pass": "relative pre-action source weights become removable/common-mode only",
            "if_fail": "Delta_w_species and c_A_current_rescale remain live components",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_4_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "STG1897_1_variation_order",
            "required_clause": "variation-before-readout and source-worldtube maps are downstream only",
            "current_status": "FAIL_CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            "if_pass": "post-current c_A and post-selector F(T_A,A) are readout/calibration, not parent source",
            "if_fail": "source-worldtube and selector transfer rows stay finite",
            "source_anchor": "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv:VBR1816_6_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "STG1897_2_readout_no_reentry",
            "required_clause": "[delta_parent, R_readout] has no source-coefficient codomain",
            "current_status": "FAIL_READOUT_STABILITY_NOT_PARENT_DERIVED",
            "if_pass": "downstream readouts cannot regenerate w_A",
            "if_fail": "readout-transfer projection coefficients remain explicit",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv:ROS1888_6_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "STG1897_3_radiative_closure",
            "required_clause": "loops, thresholds, EFT, and lab observables preserve quotient coefficient domains",
            "current_status": "FAIL_REFUSE_PROMOTION_START_PREDICTION_FILL",
            "if_pass": "effective/readout channels do not create hidden/species source coefficients",
            "if_fail": "R10/WEP/clock/PPN projection rows remain symbolic/nonclaim",
            "source_anchor": "P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv:RRC1471_3_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "STG1897_4_parent_values",
            "required_clause": "finite Delta_w components have parent values or theorem-zero signatures",
            "current_status": "FAIL_PARENT_DELTAW_VALUES_MISSING",
            "if_pass": "arena matrix can become a prediction runner input",
            "if_fail": "matrix is schema only and must refuse scoring",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_0_vector_space",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "STG1897_5_verdict",
            "required_clause": "stable source-weight zero or numeric finite Delta_w projection can be claimed",
            "current_status": "CLAIM_BLOCKED",
            "if_pass": "move to local-GR/R10/WEP scoring",
            "if_fail": "move to commutator proof or first WEP projection row v1",
            "source_anchor": "STG1897_0_action_owner through STG1897_4_parent_values",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "matrix_id": "DPM1897_0_core_vector",
            "arena": "core_component_vector",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained; Delta_mu_projector",
            "projection_formula": "Delta_w_eff = P_perp(Delta_w_species + c_A_current_rescale + Delta_w_marker_hidden) plus declared retained current/projector legs",
            "required_inputs": "parent component values; common-mode projector; material/source basis; norm; no-cancellation envelope",
            "current_status": "SYMBOLIC_MATRIX_ONLY_PARENT_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_0_vector_space",
            "units": "dimensionless or declared per current channel",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_1_WEP_MICROSCOPE",
            "arena": "WEP_MICROSCOPE_TiPt",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained",
            "projection_formula": "eta_TiPt = tau_WEP * K_WEP[Ti,Pt,Earth,readout] dot Delta_w_eff",
            "required_inputs": "official Ti/Pt material tensor; Earth/source worldtube; tau_WEP; force/readout convention; parent Delta_w_eff",
            "current_status": "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_1_WEP",
            "units": "dimensionless eta",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_2_R10",
            "arena": "R10_short_range",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained",
            "projection_formula": "alpha_Delta_w(lambda)=tau_R10(lambda)*K_R10(lambda)*Qbar_source_test(lambda) dot Delta_w_eff",
            "required_inputs": "range kernel; source/test composition; tau_R10(lambda); K_R10(lambda); digitized alpha_bound(lambda); parent Delta_w_eff",
            "current_status": "KERNEL_STUB_NONCLAIM_RANGE_KERNEL_AND_PARENT_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_2_R10",
            "units": "dimensionless alpha(lambda)",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_3_PPN",
            "arena": "PPN_beta_gamma_source",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained; Delta_mu_projector",
            "projection_formula": "[Delta gamma, Delta beta, alpha_i, xi]_source = M_PPN dot Delta_w_eff + retained source/test legs",
            "required_inputs": "weak-field solution; PPN operator matrix M_PPN; source/test split; parent Delta_w_eff; GR limit matching",
            "current_status": "KERNEL_STUB_NONCLAIM_OPERATOR_MATRIX_AND_GR_LIMIT_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_3_PPN",
            "units": "dimensionless PPN deviations",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_4_clock",
            "arena": "clock_and_constant_drift",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained",
            "projection_formula": "Delta ln nu_i = K_clock_i dot Delta_w_eff + retained alpha/mass/readout coefficients",
            "required_inputs": "clock sensitivity vector; alpha/mass split; source body composition; tau_clock; parent Delta_w_eff",
            "current_status": "KERNEL_STUB_NONCLAIM_CLOCK_SENSITIVITY_AND_PARENT_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_4_clock",
            "units": "dimensionless frequency shift or drift",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_5_orbital",
            "arena": "orbital_GM_inverse_square",
            "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; J_NH_retained; Delta_mu_projector",
            "projection_formula": "Delta ln(GM)_obs = K_orbital dot Delta_w_eff + retained finite-range/source-test/projector terms",
            "required_inputs": "source body composition; orbital GM convention; inverse-square kernel; tau_orbital; parent Delta_w_eff",
            "current_status": "KERNEL_STUB_NONCLAIM_ORBITAL_SOURCE_MAP_AND_PARENT_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_5_orbital",
            "units": "dimensionless GM/source deviation",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "DPM1897_6_no_cancellation_policy",
            "arena": "all_local_arenas",
            "components": "all finite Delta_w components",
            "projection_formula": "use sum_i |K_arena_i Delta_w_i| or a sourced covariance envelope; fitted cancellations cannot produce a pass",
            "required_inputs": "parent identity for cancellation or no-cancellation envelope plus sourced covariance",
            "current_status": "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_6_no_cancellation_policy",
            "units": "policy",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "DPR1897_0_parent_zero_or_values",
            "needed_for": "all projection rows",
            "requirement": "each Delta_w component has a parent numeric value, an uncertainty/bound, or a parent theorem-zero proof",
            "current_status": "MISSING_PARENT_DELTAW_VALUES",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_0_vector_space",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "DPR1897_1_arena_tau_K",
            "needed_for": "WEP/R10/PPN/clock/orbital rows",
            "requirement": "arena-specific tau, K, material/source/readout kernels with units and source paths",
            "current_status": "MISSING_ARENA_PROJECTION_KERNELS",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_1_WEP through DK1892_5_orbital",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "DPR1897_2_readout_order",
            "needed_for": "post-current c_A and source-worldtube transfer",
            "requirement": "prove source-worldtube/readout kernels are downstream and cannot enter parent variation",
            "current_status": "MISSING_VARIATION_BEFORE_READOUT_SIGNATURE",
            "source_anchor": "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv:VBR1816_6_verdict",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "DPR1897_3_no_reentry",
            "needed_for": "radiative/effective/readout leakage",
            "requirement": "prove [delta_parent, R_readout] has no source-only coefficient codomain, or introduce finite transfer coefficient",
            "current_status": "MISSING_READOUT_NO_REENTRY_PROOF",
            "source_anchor": "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv:RNR1700_2_commutator",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "requirement_id": "DPR1897_4_bound_inputs",
            "needed_for": "empirical comparison branch",
            "requirement": "real bound curves/arrays and matching model kernels before any claim-grade score",
            "current_status": "BOUND_ANCHOR_OR_SCHEMA_ONLY",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_2_WEP_MICROSCOPE;FDV1888_3_R10",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1897_0_action_owner_unsigned", "action_owner_signed": False, "readout_stability_signed": False, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_ACTION_SCALE_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1897_1_readout_unsigned", "action_owner_signed": True, "readout_stability_signed": False, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_READOUT_STABILITY_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1897_2_variation_unsigned", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_VARIATION_BEFORE_READOUT_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1897_3_radiative_unsigned", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_RADIATIVE_READOUT_CLOSURE_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1897_4_parent_values_missing", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1897_5_symbolic_projection", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": False, "expected_status": "REFUSED_PROJECTION_MATRIX_SYMBOLIC", "valid_for_claim": False},
        {"case_id": "DRY1897_6_cancellation", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": True, "uses_cancellation": True, "bound_only_anchor": False, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY1897_7_bound_anchor", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": True, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    action_owner_signed = bool_string(row["action_owner_signed"]) == "true"
    readout_stability_signed = bool_string(row["readout_stability_signed"]) == "true"
    variation_order_signed = bool_string(row["variation_order_signed"]) == "true"
    radiative_closure_signed = bool_string(row["radiative_closure_signed"]) == "true"
    parent_values_present = bool_string(row["parent_values_present"]) == "true"
    projection_numeric = bool_string(row["projection_numeric"]) == "true"
    uses_cancellation = bool_string(row["uses_cancellation"]) == "true"
    bound_only_anchor = bool_string(row["bound_only_anchor"]) == "true"

    if not action_owner_signed:
        status = "REFUSED_ACTION_SCALE_OWNER_UNSIGNED"
    elif not readout_stability_signed:
        status = "REFUSED_READOUT_STABILITY_UNSIGNED"
    elif not variation_order_signed:
        status = "REFUSED_VARIATION_BEFORE_READOUT_UNSIGNED"
    elif not radiative_closure_signed:
        status = "REFUSED_RADIATIVE_READOUT_CLOSURE_UNSIGNED"
    elif not parent_values_present:
        status = "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    elif not projection_numeric:
        status = "REFUSED_PROJECTION_MATRIX_SYMBOLIC"
    elif uses_cancellation:
        status = "REFUSED_CANCELLATION_ONLY"
    elif bound_only_anchor:
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
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
        {"gate_id": "CG1897_0_stability", "condition": "action-scale/readout stability is parent-signed", "current_status": "FAIL_ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv:ASR1897_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1897_1_projection_values", "condition": "Delta_w projection matrix has numeric/sourced parent components", "current_status": "FAIL_SYMBOLIC_MATRIX_ONLY_PARENT_VALUES_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_0_core_vector", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1897_2_arena_inputs", "condition": "WEP/R10/PPN/clock/orbital tau/K/material/readout kernels are sourced", "current_status": "FAIL_MISSING_ARENA_PROJECTION_KERNELS", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv:DPR1897_1_arena_tau_K", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1897_3_no_cancellation", "condition": "claim does not rely on fitted cancellation between residual components", "current_status": "PASS_POLICY_WRITTEN_BUT_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_6_no_cancellation_policy", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1897_4_verdict", "condition": "stable zero or finite projection can support local-GR/R10/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1897_0_stability through CG1897_3_no_cancellation", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1897_0_stability", "decision": "do not promote stable Delta_w=0", "reason": "one-owner theorem is exact conditionally, but the parent action-scale, measure/current owner, readout no-reentry, radiative closure, and variation-order clauses are unsigned", "status": "STABLE_ZERO_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "readout-variation commutator or action-scale parent owner", "valid_for_claim": False},
        {"decision_id": "DEC1897_1_projection_matrix", "decision": "stage Delta_w arena projection matrix as the honest fallback", "reason": "local arenas now have symbolic rows, dependencies, and refusal modes, but no parent values or full arena kernels", "status": "PROJECTION_MATRIX_STAGED_NONCLAIM", "next_dependency": "derive commutator zero or source first WEP/R10 matrix row", "valid_for_claim": False},
        {"decision_id": "DEC1897_2_next", "decision": "attack readout-variation commutator next", "reason": "this is narrower than full parent action-scale ownership and directly controls whether downstream kernels can become source couplings", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1898 readout-variation commutator zero or WEP projection row v1", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1897_0_primary",
            "selection_status": "selected",
            "target_doc": "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md",
            "target_script": "scripts/Y5_R2FR_readout_variation_commutator_zero_or_wep_projection_row_v1_1898.py",
            "objective": "try to prove [delta_parent, R_readout] has no source-only coefficient codomain; if it fails, build the first WEP projection row v1 with every missing input explicit",
            "success_condition": "parent-signed commutator/no-reentry theorem, or nonclaim WEP projection row with tau/K/material/source/readout dependencies and refusal states",
            "do_not": "do not claim local-GR/WEP/R10 from symbolic Delta_w rows, do not use fitted cancellations, and do not treat bound anchors as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1897_0_theory", "area": "source coupling derivation", "summary": "the exact one-owner/readout-stability theorem is written, but it is not parent-signed", "risk_level": "NARROW_STABILITY_GAP", "project_meaning": "the coupling problem is no longer vague; it is action-scale owner plus readout no-reentry plus radiative closure", "next_action": "prove the readout-variation commutator or action-scale owner", "valid_for_claim": False},
        {"status_id": "STAT1897_1_testing", "area": "local empirical branch", "summary": "WEP/R10/PPN/clock/orbital projection rows are staged as symbolic nonclaim matrix rows", "risk_level": "TEST_BRANCH_READY_FOR_INPUTS_NOT_SCORING", "project_meaning": "we can now plug real inputs when parent values or source-backed bounds exist, without pretending it is a pass", "next_action": "fill WEP row v1 or R10 row after commutator attempt", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "stability_attempt": stability_attempt_rows(),
        "stability_gate": stability_gate_rows(),
        "projection_matrix": projection_matrix_rows(),
        "projection_requirements": projection_requirement_rows(),
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
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SYMBOLIC", "NONCLAIM", "CLAIM_BLOCKED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


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
    checks.append({"validation_id": "VAL1897_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})
    stability_rows = csv_rows(OUTPUTS["stability_attempt"])
    checks.append({"validation_id": "VAL1897_01_stability_verdict", "status": "PASS" if any(row["attempt_id"] == "ASR1897_6_verdict" and row["status"] == "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED" for row in stability_rows) else "FAIL", "detail": "stable Delta_w zero remains unsigned", "valid_for_claim": False})
    projection_rows = csv_rows(OUTPUTS["projection_matrix"])
    checks.append({"validation_id": "VAL1897_02_projection_matrix", "status": "PASS" if len(projection_rows) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in projection_rows) else "FAIL", "detail": "Delta_w arena projection matrix rows are nonclaim/not score-ready", "valid_for_claim": False})
    requirement_rows = csv_rows(OUTPUTS["projection_requirements"])
    checks.append({"validation_id": "VAL1897_03_requirements_block", "status": "PASS" if all(row["blocks_claim"] == "True" and row["valid_for_claim"] == "False" for row in requirement_rows) else "FAIL", "detail": "all projection requirements block claims until sourced", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1897_04_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned owner/readout/variation/radiative gates, missing values, symbolic matrix, cancellation, and anchor-only bounds", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1897_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1897_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1897_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1897_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1898 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1897_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1897_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1897_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1897_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1897_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1897*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1897_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1897_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1897_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1897 action-scale/readout stability or Delta_w projection matrix", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1897 - Action-Scale Readout Stability Or Delta_w Projection Matrix

## Purpose

This checkpoint tries to prove that once the tree-level no-Hom/source-weight route is removed, source weights cannot return through action scale, measure, radiative closure, readout maps, source-worldtube projections, clocks, or local arena kernels.

If that proof remains unsigned, it stages the finite `Delta_w` arena projection matrix as a private nonclaim test scaffold.

## Result

- The stability theorem is exact conditionally: one parent action-scale/measure/current owner plus variation-before-readout plus typed readout/effective no-reentry would make `Delta_w=0` stable.
- The current corpus does not parent-sign those clauses.
- The fallback projection matrix now covers WEP, R10, PPN, clocks, orbital/GM, and no-cancellation policy.
- Every projection row remains symbolic, nonclaim, and blocked from scoring.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Action-Scale / Readout Stability Attempt

{markdown_table(rows_by_name["stability_attempt"])}

## Stability Gate

{markdown_table(rows_by_name["stability_gate"])}

## Delta_w Arena Projection Matrix

{markdown_table(rows_by_name["projection_matrix"])}

## Projection Requirements

{markdown_table(rows_by_name["projection_requirements"])}

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
