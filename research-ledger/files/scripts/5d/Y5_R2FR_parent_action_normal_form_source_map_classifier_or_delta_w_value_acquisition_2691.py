from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2691"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_NORMAL_FORM_SOURCE_MAP_CLASSIFIER_OR_DELTA_W_VALUE_ACQUISITION_2691"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2691-Y5-R2FR-parent-action-normal-form-source-map-classifier-or-delta-w-value-acquisition.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2691_SOURCE_REGISTER.csv",
    "normal_form_classifier": RESIDUALS / "P8_Y5_R2FR_2691_PARENT_ACTION_NORMAL_FORM_SOURCE_MAP_CLASSIFIER.csv",
    "source_map_gate": RESIDUALS / "P8_Y5_R2FR_2691_SOURCE_MAP_IDENTITY_AND_CLASSIFIER_GATE.csv",
    "residual_pack": RESIDUALS / "P8_Y5_R2FR_2691_RESIDUAL_COEFFICIENT_PACK_NONCLAIM.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_R2FR_2691_GR_NEWTON_BRIDGE_IMPLICATIONS.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2691_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2691_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2691_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2691_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2691_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2691_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2691_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_classifier": LOCAL_BOUNDS / "parent_action_normal_form_source_map_classifier_2691_NONCLAIM.csv",
    "local_residual_pack": LOCAL_BOUNDS / "source_map_residual_coefficient_pack_2691_NONCLAIM.csv",
    "wep_classifier": WEP_RESIDUALS / "parent_action_normal_form_source_map_classifier_2691_NONCLAIM.csv",
    "wep_residual_pack": WEP_RESIDUALS / "source_map_residual_coefficient_pack_2691_NONCLAIM.csv",
    "source_weight_residual_pack": SOURCE_WEIGHT / "SOURCE_MAP_RESIDUAL_COEFFICIENT_PACK_2691_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2691_2690_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2690_NEXT_TARGET.csv",
        "required_needles": ["NEXT2690_0_selected", "classify every source-like parent term", "formalization-workbench edits"],
        "purpose": "confirms selected 2691 normal-form classifier target",
    },
    {
        "source_id": "SRC2691_2690_BYPASS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2690_BYPASS_AND_COUNTERMODEL_LEDGER.csv",
        "required_needles": ["BYP2690_0_preaction_weight", "BYP2690_4_postvariation_projector", "SEPARATE_NEWTON_GATE"],
        "purpose": "imports source-map bypasses to classify",
    },
    {
        "source_id": "SRC2691_2690_VALUES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2690_DELTAW_SPECIES_FIRST_VALUE_ROW_NONCLAIM.csv",
        "required_needles": ["DWFV2690_0_delta_w_species", "DWFV2690_1_delta_w_shadow", "MISSING_PARENT_NUMERIC_VALUE_OR_THEOREM_ZERO"],
        "purpose": "imports first nonclaim value rows",
    },
    {
        "source_id": "SRC2691_2618_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "required_needles": ["ANF2618_0_parent_action_partition", "ANF2618_5_forbidden_source_map", "SIGNATURE_READY_PARENT_UNSIGNED"],
        "purpose": "imports prior normal-form signature",
    },
    {
        "source_id": "SRC2691_2618_SOURCE_MAP",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SOURCE_MAP_IDENTITY_GATE.csv",
        "required_needles": ["SMG2618_0_euler_equation_gate", "SMG2618_2_no_source_prefactor_gate", "NOT_CLAIMABLE"],
        "purpose": "imports source-map identity gate",
    },
    {
        "source_id": "SRC2691_2618_CLASSIFICATION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_TERM_CLASSIFICATION_LEDGER.csv",
        "required_needles": ["SCL2618_0_hilbert_matter", "SCL2618_5_post_variation_projector", "CLASSIFICATION_LEDGER_READY_NONCLAIM"],
        "purpose": "imports classification ledger",
    },
    {
        "source_id": "SRC2691_2618_COEFFS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_COEFFICIENT_PACK.csv",
        "required_needles": ["SCP2618_0_delta_w_shadow", "SCP2618_3_c_lhs_GR", "NONCLAIM_LOCK"],
        "purpose": "imports normal-form coefficient pack",
    },
    {
        "source_id": "SRC2691_2580_INVENTORY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
        "required_needles": ["EI2580_0_GK", "EI2580_4_PiM", "EI2580_9_worldtube_source"],
        "purpose": "imports broader extra-sector inventory",
    },
    {
        "source_id": "SRC2691_2580_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EXTRA_INVENTORY_COUPLING_2580_LEAKAGE_RESIDUAL_ROWS.csv",
        "required_needles": ["LR2580_0_GK", "LR2580_9_worldtube_source", "LR2580_TOTAL"],
        "purpose": "imports leakage residual row pattern",
    },
    {
        "source_id": "SRC2691_2485_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv",
        "required_needles": ["NF2485_0_parent_action_skeleton", "NF2485_2_public_field_equation", "NF2485_3_Newton_Poisson_gate"],
        "purpose": "imports parent normal-form skeleton and Newton gate",
    },
    {
        "source_id": "SRC2691_2485_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv",
        "required_needles": ["DG2485_3_higher_curvature", "DG2485_5_nonminimal_matter", "DG2485_6_projector_postvariation"],
        "purpose": "imports derivative grammar for classifier",
    },
    {
        "source_id": "SRC2691_2579_DESCENT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DESCENT_PACKAGE_AUDIT.csv",
        "required_needles": ["EDP2579_0_EH_core", "EDP2579_4_PiM_lock", "EH_DESCENT_COUPLING_PIM_PACKAGE_NOT_DERIVED_CURRENT_CORPUS"],
        "purpose": "imports GR/Newton descent blockers",
    },
    {
        "source_id": "SRC2691_SOURCE_OWNER_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "required_needles": ["A0_total_covariant_parent", "A6_selector_blind_source_action", "A10_second_order_source_closure"],
        "purpose": "imports source-owner parent action terms",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def classifier_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLS2691_0_target", "classifier target", "Every source-like term must be Hilbert matter, LHS geometry/operator, boundary/improvement, nonvariational inconsistency, decoupled residual, or explicit finite coefficient row.", "TARGET_SHARP", "prevents source-map debt hiding under vague coupling language", "2690:NEXT2690_0_selected", "NOT_CLAIM"),
        ("CLS2691_1_hilbert_matter", "minimal ordinary matter", "S_matter_min[e_obs,Psi,theta] varied before readout gives T_H.", "ALLOWED_SOURCE_OWNER_CONDITIONAL", "allowed RHS owner but no pre-action w_A prefactors may be inserted", "2618:SCL2618_0_hilbert_matter;2485:NF2485_2_public_field_equation", "HILBERT_RHS"),
        ("CLS2691_2_lhs_geometry", "geometry/MTS operator", "S_geom+S_MTS+nonminimal geometry variations live on E_LHS.", "ALLOWED_LHS_OWNER_CONDITIONAL", "must derive EH/Newton limit or carry operator residuals", "2618:ANF2618_1_geometry_left_hand_owner;2579:EDP2579_0_EH_core", "LHS_OPERATOR"),
        ("CLS2691_3_nonminimal_matter", "nonminimal matter-geometry/source coupling", "f(X,Phi,labels)L_m or A(X)J_m must be forbidden, moved to modified matter dynamics, or retained as coefficient.", "MUST_CLASSIFY_RETAINED", "cannot masquerade as an unowned source-shadow knob", "2618:SCL2618_2_nonminimal_coupling;2485:DG2485_5_nonminimal_matter", "FINITE_RESIDUAL_OR_FORBID"),
        ("CLS2691_4_boundary_improvement", "boundary/improvement current", "S_boundary or nabla_alpha U^{alpha mu nu} is silent only with boundary/falloff theorem, otherwise coefficient row.", "BOUNDARY_SILENCE_OR_BOUND_REQUIRED", "boundary source leakage remains live", "2618:SCL2618_3_boundary_improvement;2485:DG2485_2_topological_boundary", "BOUNDARY_OR_RESIDUAL"),
        ("CLS2691_5_nonhilbert_current", "spin/torsion/non-Hilbert label current", "J_spin/J_torsion/J_label must be absent, LHS geometry, pure improvement, or bounded residual.", "ABSENCE_RECLASSIFICATION_OR_BOUND_REQUIRED", "label-carrying non-Hilbert currents are not zero by naming", "2617:NHB2617_1_spin_torsion_current;2618:SCL2618_4_nonHilbert_label_current", "FINITE_RESIDUAL_OR_RECLASSIFY"),
        ("CLS2691_6_postvariation_projector", "post-variation material/source projector", "P_material(T_H)-T_H is forbidden unless action-owned; otherwise Delta_w_shadow/projector coefficient.", "FORBIDDEN_BY_CONTRACT_NOT_PARENT_SIGNED", "direct label reentry after q_src/Hilbert extraction remains live", "2618:SCL2618_5_post_variation_projector;2690:BYP2690_4_postvariation_projector", "FORBID_OR_DELTAW_SHADOW"),
        ("CLS2691_7_decoupled_block", "separately conserved decoupled block", "J_dec with nabla_mu J_dec^{mu nu}=0 must be excluded from tested ordinary source or bounded.", "ARENA_EXCLUSION_OR_BOUND_REQUIRED", "Bianchi permits it if real and conserved", "2618:SCL2618_6_decoupled_block;2617:NHB2617_2_decoupled_conserved_block", "DECOUPLED_RESIDUAL"),
        ("CLS2691_8_pim_source_measure", "PiM/worldtube/source glue", "Pi_M J_H, topological current and worldtube charge equality must be parent-owned before Newton source claim.", "PROJECTED_MASS_PARALLEL_GATE_OPEN", "source labels may be narrowed while measured GM still fails", "2580:EI2580_4_PiM;2580:EI2580_9_worldtube_source;2579:EDP2579_4_PiM_lock", "NEWTON_SOURCE_GATE"),
        ("CLS2691_9_kappa_coupling", "kappa/G/common coupling owner", "G_eff/kappa_eff must carry no time/radius/species/frame/domain labels.", "COMMON_COUPLING_OWNER_UNSIGNED", "common source map still needs universal coupling branch", "2580:EI2580_7_kappa;P8_source_owner_parent_action_terms_CONTRACT:A5_constant_universal_coupling", "COUPLING_RESIDUAL"),
        ("CLS2691_10_verdict", "complete classifier theorem", "The current corpus supplies a complete parent normal-form source-map classifier with every source-like term assigned and zeroed/bounded.", "CLASSIFIER_LEDGER_READY_NOT_COMPLETE", "classifier is useful, but complete action inventory, boundary silence, projector identity, nonminimal classification and EH/Newton operator limit remain unsigned", "CLS2691_0_target through CLS2691_9_kappa_coupling", "NOT_CLAIM"),
    ]
    return [
        {
            "classifier_id": row[0],
            "class": row[1],
            "normal_form_rule": row[2],
            "current_status": row[3],
            "meaning": row[4],
            "source_anchor": row[5],
            "owner_bucket": row[6],
            "parent_signed": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def source_map_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("SMC2691_0_euler_parent", "field equation is Euler-Lagrange from one complete S_parent", "FAIL_COMPLETE_PARENT_ACTION_INVENTORY_UNSIGNED", "source-map identity follows by variation", "source terms remain classifier rows", "2618:SMG2618_0_euler_equation_gate", "false"),
        ("SMC2691_1_hilbert_identity", "ordinary RHS source is T_H only", "CONDITIONAL_SOURCE_IDENTITY_NOT_PARENT_COMPLETE", "T_active=T_H for ordinary matter", "identity-only source map remains contract", "2618:ANF2618_2_hilbert_matter_owner", "false"),
        ("SMC2691_2_no_prefactor", "no source-only matter prefactor before variation", "FAIL_NO_PREFACTOR_NOT_DERIVED", "Delta_w_species zero route opens", "Delta_w_species remains nonclaim row", "2618:SMG2618_2_no_source_prefactor_gate;2690:BYP2690_0_preaction_weight", "false"),
        ("SMC2691_3_no_shadow_projector", "no independent F_shadow(T_H,labels)", "FAIL_PROJECTOR_SHADOW_IDENTITY_UNSIGNED", "Delta_w_shadow zero route opens", "projector/shadow rows remain live", "2618:SMG2618_1_no_shadow_map_gate", "false"),
        ("SMC2691_4_boundary_silence", "boundary/improvement terms have zero compact source flux or explicit row", "FAIL_BOUNDARY_SILENCE_UNSIGNED", "boundary rows leave local source map", "boundary coefficient row retained", "2618:ANF2618_4_boundary_owner", "false"),
        ("SMC2691_5_gr_lhs", "left-hand operator has Einstein/Newton weak-field limit", "NEXT_BRIDGE_NOT_DERIVED_HERE", "source-side work becomes GR/Newton reduction", "local GR still not claimed", "2618:SMG2618_3_gr_lhs_gate;2579:EDP2579_7_verdict", "false"),
        ("SMC2691_6_no_cancellation", "no finite residual pass through cancellations", "PASS_GUARD_ONLY", "keeps future testing honest", "guard only", "2690:QG2690_7_no_cancellation", "true"),
        ("SMC2691_7_verdict", "source-map identity/classifier can claim local source universality", "CLAIM_BLOCKED", "source-side source universality promotable", "classifier remains nonclaim", "SMC2691_0 through SMC2691_6", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "required_clause": row[1],
            "current_status": row[2],
            "if_signed": row[3],
            "if_unsigned": row[4],
            "source_anchor": row[5],
            "gate_pass": row[6],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def residual_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("RCP2691_0_delta_w_species", "Delta_w_species", "pre-action relative source/action normalization", "DWFV2690_0_delta_w_species", "MISSING_PARENT_VALUE_OR_ZERO_THEOREM", "dimensionless", "WEP;R10;PPN;clock;orbital;Newton"),
        ("RCP2691_1_delta_w_shadow", "Delta_w_shadow", "post-Hilbert source-shadow/projector residual", "DWFV2690_1_delta_w_shadow", "MISSING_NORMAL_FORM_ZERO_OR_BOUND", "dimensionless_or_arena_normalized", "WEP;R10;PPN;clock;orbital;Newton"),
        ("RCP2691_2_c_nonminimal", "c_nonminimal", "direct matter-MTS/geometric nonminimal source term", "SCP2618_1_c_nonminimal", "MISSING_OPERATOR_BASIS_AND_BOUND", "operator_dependent", "WEP;PPN;R10"),
        ("RCP2691_3_c_boundary", "c_boundary", "boundary/domain/improvement source residual", "SCP2618_2_c_boundary", "MISSING_BOUNDARY_SILENCE_OR_BOUND", "boundary_operator_dependent", "Newton;PPN;orbital;R11"),
        ("RCP2691_4_c_projector", "c_projector_operator", "post-variation/source-measure projector commutator", "2580:LR2580_4_PiM", "MISSING_PROJECTOR_IDENTITY_OR_BOUND", "dimensionless_or_declared", "Newton;WEP;PPN;orbital"),
        ("RCP2691_5_c_lhs_GR", "E_LHS_GR_residual", "left-hand deviation from Einstein/Newton operator", "SCP2618_3_c_lhs_GR", "MISSING_GR_LIMIT_DERIVATION", "curvature_or_operator_units", "Newton;PPN;local_GR"),
        ("RCP2691_6_total_envelope", "Delta_source_map_classifier_abs", "absolute no-cancellation envelope over retained classifier residuals", "SCP2618_4_R_total_residual;LR2580_TOTAL", "MISSING_COMPONENT_NORMS_AND_ARENA_KERNELS", "mixed_declared", "all"),
    ]
    return [
        {
            "row_id": row[0],
            "symbol": row[1],
            "definition": row[2],
            "source_anchor": row[3],
            "current_status": row[4],
            "units": row[5],
            "observable_link": row[6],
            "numeric_value_present": "false",
            "source_path_present": "true",
            "projection_ready": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        ("GRB2691_0_source_side", "source-side classification", "NARROWED_NOT_CLOSED", "Hilbert source is the target RHS, but prefactor/shadow/projector rows remain", "normal-form classifier or residual coefficients"),
        ("GRB2691_1_lhs_operator", "left-hand Einstein/Newton limit", "NEXT_REQUIRED_BRIDGE", "even perfect source map does not prove GR unless E_LHS -> Einstein tensor/Newton Poisson", "derive EH operator limit or residual pack"),
        ("GRB2691_2_projected_mass", "measured GM/Newton calibration", "PARALLEL_GATE_OPEN", "q_src/Hilbert source does not close Pi_M/worldtube/source-glue", "PiM/Hamiltonian/source-measure lock"),
        ("GRB2691_3_claim_status", "local GR/Newton claim", "CLAIM_BLOCKED", "source classifier and LHS GR bridge are both required", "run 2692 LHS bridge"),
    ]
    return [
        {
            "bridge_id": row[0],
            "topic": row[1],
            "status": row[2],
            "meaning": row[3],
            "next_dependency": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2691_0_all_classified_and_lhs", "true", "true", "true", "true", "true", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2691_1_classifier_only", "true", "false", "false", "false", "false", "false", "false", "REJECT_CLASSIFIER_ONLY"),
        ("DRY2691_2_unclassified_shadow", "false", "false", "false", "false", "false", "false", "false", "REJECT_UNCLASSIFIED_SOURCE_TERM"),
        ("DRY2691_3_source_without_lhs", "true", "true", "true", "false", "false", "false", "false", "REJECT_SOURCE_WITHOUT_LHS_GR"),
        ("DRY2691_4_boundary_open", "true", "true", "false", "true", "false", "false", "false", "REJECT_BOUNDARY_OPEN"),
        ("DRY2691_5_values_without_kernels", "false", "false", "false", "false", "true", "false", "false", "REJECT_VALUES_WITHOUT_PROJECTIONS"),
        ("DRY2691_6_ward_only", "false", "false", "false", "false", "false", "false", "true", "REJECT_WARD_ONLY"),
        ("DRY2691_7_cancellation_only", "false", "false", "false", "false", "true", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
    ]
    return [
        {
            "case_id": row[0],
            "complete_classifier": row[1],
            "source_identity_signed": row[2],
            "boundary_silent": row[3],
            "lhs_gr_signed": row[4],
            "value_rows_present": row[5],
            "cancellation_only": row[6],
            "ward_only": row[7],
            "expected_status": row[8],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in cases
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["ward_only"] == "true":
        return "REJECT_WARD_ONLY"
    if (
        case["complete_classifier"] == "true"
        and case["source_identity_signed"] == "true"
        and case["boundary_silent"] == "true"
        and case["lhs_gr_signed"] == "true"
    ):
        return "THEOREM_READY_IF_PARENT_SIGNED"
    if case["complete_classifier"] == "false" and case["value_rows_present"] == "false":
        return "REJECT_UNCLASSIFIED_SOURCE_TERM"
    if case["complete_classifier"] == "true" and case["source_identity_signed"] == "false":
        return "REJECT_CLASSIFIER_ONLY"
    if case["boundary_silent"] == "false" and case["source_identity_signed"] == "true":
        return "REJECT_BOUNDARY_OPEN"
    if case["lhs_gr_signed"] == "false" and case["source_identity_signed"] == "true":
        return "REJECT_SOURCE_WITHOUT_LHS_GR"
    if case["value_rows_present"] == "true":
        return "REJECT_VALUES_WITHOUT_PROJECTIONS"
    return "REJECT_UNCLASSIFIED_SOURCE_TERM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "computed_status": computed,
                "expected_status": case["expected_status"],
                "status_match": as_bool(computed == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2691_0_classifier", "normal-form classifier is complete and parent-signed", "FAIL_CLASSIFIER_LEDGER_READY_NOT_COMPLETE", "CLS2691_10_verdict", "false"),
        ("CG2691_1_source_identity", "T_active=T_H and no prefactor/shadow/projector bypass", "FAIL_SOURCE_MAP_IDENTITY_UNSIGNED", "SMC2691_7_verdict", "false"),
        ("CG2691_2_boundary", "boundary/improvement terms are silent or bounded", "FAIL_BOUNDARY_SILENCE_UNSIGNED", "SMC2691_4_boundary_silence", "false"),
        ("CG2691_3_lhs_gr", "left-hand operator has Einstein/Newton limit", "FAIL_LHS_GR_BRIDGE_NOT_DERIVED", "SMC2691_5_gr_lhs", "false"),
        ("CG2691_4_residual_values", "retained residual coefficient pack has values/kernels", "FAIL_RESIDUAL_PACK_NONCLAIM", "RCP2691_6_total_envelope", "false"),
        ("CG2691_5_guardrails", "Ward-only/cancellation-only/action-schema shortcuts refused", "PASS_GUARD_ONLY", "DRY2691_*", "true"),
        ("CG2691_6_verdict", "local source/GR/Newton branch can claim pass", "CLAIM_BLOCKED", "CG2691_0_classifier through CG2691_5_guardrails", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "gate_pass": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2691_0_classifier",
            "decision": "CLASSIFIER_LEDGER_WRITTEN_NOT_PROMOTED",
            "reason": "Every major source-like class now has a bucket, but the complete parent action inventory and silence/identity proofs are unsigned.",
            "status": "NONCLAIM_PROGRESS",
            "next_dependency": "LHS Einstein/Newton operator bridge and residual values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2691_1_source_map",
            "decision": "SOURCE_MAP_SMUGGLING_REDUCED_TO FINITE ROWS",
            "reason": "Prefactor, shadow, boundary, nonminimal, projector and PiM routes cannot hide; they are either theorem debts or rows.",
            "status": "BYPASSES_EXPOSED",
            "next_dependency": "normal-form zero proofs or coefficient acquisition",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2691_2_gr",
            "decision": "MOVE_TO_LEFT_HAND_GR_LIMIT_NEXT",
            "reason": "A clean RHS source map still does not prove GR/Newton; the next derivation-first route is E_LHS -> Einstein/Newton or operator residual rows.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2692 GR left-hand Einstein/Newton limit or operator residual pack",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2691_0_selected",
            "kind": "selected",
            "target_doc": "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
            "target_script": "scripts/Y5_R2FR_GR_left_hand_Einstein_Newton_limit_or_operator_residual_pack_2692.py",
            "purpose": "derive E_LHS -> Einstein tensor plus Newton/Poisson weak-field limit from parent normal form, or stage explicit nonclaim operator residual coefficients",
            "acceptance_gate": "left-hand operator reduces to EH/Newton with source-map classifier retained, or c_lhs_GR/higher-derivative/projector/source residual rows are explicit and nonclaim",
            "forbidden_shortcuts": "importing GR as assumption; source-side proof as full GR proof; EOM division; action schema as derivation; cancellation-only pass; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2691_0_classifier", "source-map classifier", "LEDGER_READY_NOT_THEOREM", "source-like terms now have buckets but not full parent signatures"),
        ("STATUS2691_1_source_side", "source universality", "NARROWED_NOT_CLOSED", "prefactor/shadow/projector routes are exposed as finite gates"),
        ("STATUS2691_2_residuals", "finite residual route", "COEFFICIENT_PACK_NONCLAIM", "retained rows exist but have no values/projections"),
        ("STATUS2691_3_gr", "GR/Newton bridge", "LHS_OPERATOR_NEXT", "source side is not enough; derive Einstein/Newton left-hand operator next"),
        ("STATUS2691_4_claims", "claim status", "ALL_LOCAL_CLAIMS_BLOCKED", "no local-GR/WEP/R10/PPN/clock/orbital/Newton claim"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2692 left-hand Einstein/Newton limit target",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2691_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    classifier: list[dict[str, Any]],
    source_gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    classifier_written = any(row["classifier_id"] == "CLS2691_10_verdict" and row["current_status"] == "CLASSIFIER_LEDGER_READY_NOT_COMPLETE" for row in classifier)
    source_blocked = any(row["gate_id"] == "SMC2691_7_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in source_gates)
    residual_pack_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and row["score_ready"] == "false" and row["numeric_value_present"] == "false" for row in residuals)
    gr_next = any(row["bridge_id"] == "GRB2691_1_lhs_operator" and row["status"] == "NEXT_REQUIRED_BRIDGE" for row in bridge)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2691_6_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2692" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2691_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2691_classifier_written_not_promoted", classifier_written, "classifier ledger is written but not complete/theorem-grade"),
        ("VAL2691_source_map_gate_blocks", source_blocked, "source-map identity gate blocks claims"),
        ("VAL2691_residual_pack_nonclaim", residual_pack_nonclaim, "residual coefficient pack remains nonclaim/not score-ready"),
        ("VAL2691_gr_bridge_selected", gr_next, "left-hand GR/Newton bridge is selected as next derivation route"),
        ("VAL2691_dryrun_refusals", dryrun_ok, "dry-run refuses classifier-only, unclassified terms, source-without-LHS, boundary-open, Ward-only and cancellation shortcuts"),
        ("VAL2691_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2691_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2691_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2691_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2691_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2691_next_target_selected", next_target_ok, "2692 left-hand Einstein/Newton target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2691_OVERALL",
            "passed": as_bool(overall),
            "detail": "2691 writes the normal-form source-map classifier, refuses promotion, exposes finite residual rows, and selects the left-hand GR/Newton bridge",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    classifier: list[dict[str, Any]],
    source_gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2691 - Y5/R2FR Parent Action Normal-Form Source-Map Classifier or Delta-w Value Acquisition",
                "",
                "## Private Verdict",
                "",
                "This checkpoint does the useful boring thing: it stops source-like terms from hiding. Every source-looking object is forced into a bucket: Hilbert matter, left-hand geometry/operator, boundary/improvement, non-Hilbert or projector residual, decoupled block, PiM/source-measure gate, coupling residual, or explicit finite coefficient row.",
                "",
                "The classifier is not yet a theorem. It is a disciplined ledger. The important move is that the next derivation target is now the left-hand GR/Newton operator limit; a clean RHS source map alone still does not give GR.",
                "",
                "No local-GR, Newton, WEP, R10, PPN, clock, orbital, GitHub, or public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Normal-Form Source-Map Classifier",
                "",
                markdown_table(classifier),
                "",
                "## Source-Map Identity and Classifier Gate",
                "",
                markdown_table(source_gates),
                "",
                "## Residual Coefficient Pack",
                "",
                markdown_table(residuals),
                "",
                "## GR/Newton Bridge Implications",
                "",
                markdown_table(bridge),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    classifier = classifier_rows()
    source_gates = source_map_gate_rows()
    residuals = residual_pack_rows()
    bridge = gr_bridge_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["normal_form_classifier"], classifier)
    write_csv(OUTPUTS["source_map_gate"], source_gates)
    write_csv(OUTPUTS["residual_pack"], residuals)
    write_csv(OUTPUTS["gr_bridge"], bridge)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_classifier"], classifier)
    write_csv(BRANCH_OUTPUTS["local_residual_pack"], residuals)
    write_csv(BRANCH_OUTPUTS["wep_classifier"], classifier)
    write_csv(BRANCH_OUTPUTS["wep_residual_pack"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight_residual_pack"], residuals)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, classifier, source_gates, residuals, bridge, dry_results, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, classifier, source_gates, residuals, bridge, dry_cases, dry_results, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
