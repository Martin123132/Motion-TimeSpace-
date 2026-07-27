from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2690"
BRANCH_ID = "Y5_R2FR_SOURCE_DOMAIN_QUOTIENT_NO_PREFACTOR_NO_SHADOW_PACKAGE_OR_DELTA_W_FIRST_VALUE_ROW_2690"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2690-Y5-R2FR-source-domain-quotient-no-prefactor-no-shadow-package-or-delta-w-first-value-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2690_SOURCE_REGISTER.csv",
    "qsrc_package": RESIDUALS / "P8_Y5_R2FR_2690_QSRC_NO_PREFACTOR_NO_SHADOW_PACKAGE_AUDIT.csv",
    "closure_gate": RESIDUALS / "P8_Y5_R2FR_2690_QSRC_PACKAGE_CLOSURE_GATE.csv",
    "bypass_ledger": RESIDUALS / "P8_Y5_R2FR_2690_BYPASS_AND_COUNTERMODEL_LEDGER.csv",
    "first_value_row": RESIDUALS / "P8_Y5_R2FR_2690_DELTAW_SPECIES_FIRST_VALUE_ROW_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2690_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2690_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2690_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2690_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2690_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2690_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2690_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_qsrc_package": LOCAL_BOUNDS / "qsrc_no_prefactor_no_shadow_package_2690_NONCLAIM.csv",
    "local_first_value": LOCAL_BOUNDS / "deltaw_species_first_value_row_2690_NONCLAIM.csv",
    "wep_qsrc_package": WEP_RESIDUALS / "qsrc_no_prefactor_no_shadow_package_2690_NONCLAIM.csv",
    "wep_first_value": WEP_RESIDUALS / "deltaw_species_first_value_row_2690_NONCLAIM.csv",
    "source_weight_first_value": SOURCE_WEIGHT / "DELTAW_SPECIES_FIRST_VALUE_ROW_2690_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2690_2689_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2689_NEXT_TARGET.csv",
        "required_needles": ["NEXT2689_0_selected", "q_src maps labelled ordinary Hilbert source family", "no w_A/kappa_A/source-shadow bypass"],
        "purpose": "confirms selected 2690 q_src/no-prefactor/no-shadow target",
    },
    {
        "source_id": "SRC2690_2689_OWNER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2689_PARENT_ACTION_OWNER_GATE.csv",
        "required_needles": ["POG2689_1_q_src", "POG2689_2_no_prefactor", "POG2689_3_shadow_current"],
        "purpose": "imports owner gates from 2689",
    },
    {
        "source_id": "SRC2690_2689_DELTW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2689_DELTAW_COMPONENT_VALUE_ROWS_NONCLAIM.csv",
        "required_needles": ["DWV2689_0_delta_w_species", "MISSING_PARENT_VALUE_OR_ZERO_THEOREM", "DWV2689_9_acceptance"],
        "purpose": "imports first Delta_w value-row requirements",
    },
    {
        "source_id": "SRC2690_2649_QSRC",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CONSTRUCTOR_ATTEMPT.csv",
        "required_needles": ["QSRC2649_0_definition", "PREACTION_WEIGHT_BYPASS_SURVIVES", "SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED"],
        "purpose": "imports q_src constructor attempt and bypass",
    },
    {
        "source_id": "SRC2690_2649_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CLAUSE_GATE.csv",
        "required_needles": ["QG2649_0_parent_category", "QG2649_2_no_source_prefactors", "QSRC_CLAIM_BLOCKED"],
        "purpose": "imports q_src clause gate",
    },
    {
        "source_id": "SRC2690_2646_OWNER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
        "required_needles": ["MNO2646_1_conditional_owner_lemma", "MNO2646_5_countermodel", "MATTER_NORMALIZATION_OWNER_NOT_DERIVED"],
        "purpose": "imports no-source-prefactor/matter-normalization theorem attempt",
    },
    {
        "source_id": "SRC2690_2646_VALUE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv",
        "required_needles": ["DWS2646_0_delta_w_species", "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE", "SOURCE_PROJECTORS_NOT_DERIVED"],
        "purpose": "imports symbolic Delta_w_species first coefficient row",
    },
    {
        "source_id": "SRC2690_2617_IDENTITY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
        "required_needles": ["SMI2617_1_identity_source_map", "THEOREM_CONTRACT_READY_PARENT_UNSIGNED", "SMI2617_5_current_verdict"],
        "purpose": "imports single-source-map theorem and gap",
    },
    {
        "source_id": "SRC2690_2617_SHADOW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
        "required_needles": ["SSZ2617_1_shadow_as_action_term", "SSZ2617_3_shadow_as_projector", "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF"],
        "purpose": "imports source-shadow zero attempt",
    },
    {
        "source_id": "SRC2690_2617_INVENTORY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
        "required_needles": ["NHB2617_0_boundary_improvement", "NHB2617_4_post_variation_projector", "INVENTORY_READY_NONCLAIM"],
        "purpose": "imports non-Hilbert/boundary/projector bypass inventory",
    },
    {
        "source_id": "SRC2690_1889_WARD",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
        "required_needles": ["SWO1889_3_no_species_label_conditional", "SWO1889_5_pre_action_weight_leak", "SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED"],
        "purpose": "imports Ward/source-current owner limitations",
    },
    {
        "source_id": "SRC2690_1905_LINE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv",
        "required_needles": ["ADL1905_0_line_owner", "ADL1905_4_eom_shortcut", "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED"],
        "purpose": "imports action-density line owner gap",
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


def qsrc_package_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QPK2690_0_target",
            "q_src/no-prefactor/no-shadow package",
            "Construct q_src(J_lab)=T_total and prove every ordinary source coupling factors through it with no pre-action prefactor or post-Hilbert shadow bypass.",
            "TARGET_SHARP",
            "This is the minimum package that could make source-label forgetting theorem-grade.",
            "2689:NEXT2689_0_selected",
        ),
        (
            "QPK2690_1_qsrc_definition",
            "source-domain quotient",
            "J_lab={(T_A,A)} ~ J'_lab iff sum_A T_A=sum_B T'_B; q_src(J_lab)=T_total.",
            "MATHEMATICAL_CONSTRUCTOR_WRITTEN",
            "The quotient map is clean as mathematics, but parent physics must force all source couplings to factor through it.",
            "2649:QSRC2649_0_definition",
        ),
        (
            "QPK2690_2_factorization",
            "unique source map after quotient",
            "If F_src is local/covariant/additive/natural on Im(q_src), then F_src(T_total)=kappa_univ T_total up to one common scale.",
            "EXACT_CONDITIONAL_THEOREM",
            "Relative weights cannot be formed after labels are removed; this clause is good but conditional.",
            "2649:QSRC2649_1_factorization_theorem;1889:SWO1889_3_no_species_label_conditional",
        ),
        (
            "QPK2690_3_parent_adoption",
            "parent action/category adopts q_src before coupling",
            "C_parent -> C_source quotients labelled current families by total Hilbert current before any coupling coefficient is chosen.",
            "PARENT_ADOPTION_NOT_DERIVED",
            "Current evidence states the clause but does not derive it from MTS primitives or normal-form action grammar.",
            "2649:QSRC2649_2_parent_adoption_gap;2690:QPK2690_1_qsrc_definition",
        ),
        (
            "QPK2690_4_no_prefactor",
            "no pre-action source prefactor",
            "S_matter=sum_A S_A is the parent ordinary-matter action; w_A S_A and kappa_A T_A are not legal active-source-only objects before variation.",
            "NO_PREFACTOR_THEOREM_NOT_DERIVED",
            "q_src alone fails if it receives an already weighted Hilbert source sum_A w_A T_A.",
            "2649:QSRC2649_3_no_prefactor_bypass;2646:MNO2646_5_countermodel",
        ),
        (
            "QPK2690_5_no_shadow",
            "no post-Hilbert source-shadow/projector bypass",
            "T_active=T_H; any J_shadow is action content, boundary/improvement, nonvariational inconsistency, or a retained residual block.",
            "SHADOW_PACKAGE_CLASSIFIED_NOT_ZEROED",
            "The trichotomy is useful, but parent normal-form classification and boundary/projector silence are still unsigned.",
            "2617:SMI2617_2_shadow_trichotomy;2617:SSZ2617_4_current_verdict",
        ),
        (
            "QPK2690_6_nonhilbert_inventory",
            "non-Hilbert/boundary/projector residual inventory",
            "J_shadow may include spin/torsion, boundary, nonminimal, projector, or decoupled conserved blocks.",
            "INVENTORY_READY_NONCLAIM",
            "All channels are named and must be zeroed or bounded rather than hidden inside source universality.",
            "2617:NHB2617_5_verdict",
        ),
        (
            "QPK2690_7_action_line",
            "one action-density line support",
            "One parent action-density/measure/current line would prevent species-only Jacobians and collapse ordinary relative weights to common mode.",
            "ACTION_DENSITY_LINE_OWNER_UNSIGNED",
            "This is the cleanest no-prefactor route, but it is not parent-signed.",
            "1905:ADL1905_0_line_owner;2646:MNO2646_4_measure_action_density_line",
        ),
        (
            "QPK2690_8_projected_mass",
            "Newton/GM projection after source quotient",
            "Measured-GM requires d(Pi_M J_H)=0 with no exchange, boundary, anomaly, range or time-drift leakage.",
            "PROJECTED_MASS_SEPARATE_OPEN_GATE",
            "q_src helps source labels, not the whole Newtonian calibration problem.",
            "2649:QSRC2649_5_projected_mass_gap;1889:SWO1889_6_projected_mass_flux",
        ),
        (
            "QPK2690_9_verdict",
            "promote q_src/no-prefactor/no-shadow package",
            "Current MTS parent theory forces ordinary source coupling through q_src, forbids pre-action weights, and eliminates shadow/projector label reentry.",
            "PACKAGE_NOT_PARENT_DERIVED",
            "q_src is exact conditionally, but parent adoption, no-prefactor/action-line owner, shadow zero and projected mass remain unsigned.",
            "QPK2690_0_target through QPK2690_8_projected_mass",
        ),
    ]
    return [
        {
            "package_id": row[0],
            "claim_piece": row[1],
            "formal_statement": row[2],
            "current_status": row[3],
            "derivation_or_obstruction": row[4],
            "source_anchor": row[5],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def closure_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QG2690_0_qsrc_map", "q_src mathematical quotient is written", "PASS_CONDITIONAL_NONCLAIM", "relative labels absent from Im(q_src)", "not enough without parent adoption", "2649:QSRC2649_0_definition", "true"),
        ("QG2690_1_parent_adoption", "parent action/category requires all source maps factor through q_src", "FAIL_PARENT_ADOPTION_NOT_DERIVED", "source labels cannot enter F_src", "q_src remains closure contract", "2649:QG2649_0_parent_category", "false"),
        ("QG2690_2_no_prefactor", "pre-action w_A/kappa_A/source-only multipliers are illegal", "FAIL_NO_PREFACTOR_NOT_DERIVED", "weighted-source countermodel killed", "q_src may receive weighted T_source", "2649:QG2649_2_no_source_prefactors", "false"),
        ("QG2690_3_no_shadow", "post-Hilbert source-shadow/projector/non-Hilbert label reentry is zero or bounded", "FAIL_SHADOW_ZERO_NOT_DERIVED", "T_active=T_H reaches arenas", "delta_w_shadow/J_NH/projector rows remain live", "2617:SMI2617_5_current_verdict", "false"),
        ("QG2690_4_action_line", "one action-density line/measure/current owner is parent-signed", "FAIL_ACTION_LINE_UNSIGNED", "ordinary relative weights collapse to common mode", "Delta_w_species remains live", "1905:ADL1905_5_verdict", "false"),
        ("QG2690_5_projected_mass", "measured-GM/source projector calibration is closed", "FAIL_PROJECTED_MASS_OPEN", "Newton source normalization can use q_src result", "Newton/GM remains separate residual gate", "2649:QG2649_4_projected_mass", "false"),
        ("QG2690_6_ward_guard", "Ward conservation is not accepted as source-domain proof", "PASS_GUARD_ONLY", "prevents false promotion", "none; guard only", "1889:SWO1889_2_Ward_homogeneity", "true"),
        ("QG2690_7_no_cancellation", "finite values cannot pass by fitted cancellation", "PASS_GUARD_ONLY", "keeps empirical branch honest", "none; guard only", "2689:DWV2689_8_no_cancellation", "true"),
        ("QG2690_8_verdict", "source-label/source-shadow package can be claimed", "CLAIM_BLOCKED", "Delta_w_species/shadow theorem-zero promotable", "package remains derivation target", "QG2690_0 through QG2690_7", "false"),
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


def bypass_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("BYP2690_0_preaction_weight", "S_matter=sum_A w_A S_A", "survives q_src if inserted before variation", "Delta_w_species", "no-prefactor/action-density-line theorem or numeric epsilon_A row", "LIVE_COUNTERMODEL"),
        ("BYP2690_1_source_shadow_action", "J_shadow=delta DeltaS/delta e_obs", "is real action content, not a harmless RHS knob", "Delta_w_shadow or classified residual operator", "parent normal-form classifier", "RECLASSIFY_OR_BOUND"),
        ("BYP2690_2_nonvariational_shadow", "J_shadow inserted without action", "Bianchi rejects unless separately conserved real block", "J_decoupled residual", "arena exclusion or bound", "FILTERED_NOT_ZEROED"),
        ("BYP2690_3_boundary_improvement", "J_boundary=nabla U or delta S_boundary/delta e_obs", "silent only with falloff/local boundary theorem", "boundary source residual", "boundary silence theorem or bound", "LIVE_BOUNDARY_GATE"),
        ("BYP2690_4_postvariation_projector", "T_active=P_material(T_H)", "direct label reentry after clean Hilbert source", "projector/source-shadow residual", "P_material=identity theorem or bound", "LIVE_PROJECTOR_GATE"),
        ("BYP2690_5_projected_mass", "Pi_M J_H versus measured GM", "not solved by source-label quotient alone", "Delta_mu_projector/Newton source residual", "closed calibrated mass projector", "SEPARATE_NEWTON_GATE"),
    ]
    return [
        {
            "bypass_id": row[0],
            "bypass": row[1],
            "why_it_matters": row[2],
            "residual_owner": row[3],
            "needed_to_close": row[4],
            "status": row[5],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def first_value_row() -> list[dict[str, Any]]:
    return [
        {
            "value_row_id": "DWFV2690_0_delta_w_species",
            "component": "Delta_w_species",
            "coefficient_symbol": "epsilon_A",
            "definition": "relative active-source/action normalization after projecting out the universal common mode",
            "basis_formula": "w_A=w_common*(1+epsilon_A), sum_A p_A epsilon_A=0; Delta_w_species=P_perp epsilon",
            "current_value": "MISSING_PARENT_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "value_type": "symbolic_nonclaim_placeholder",
            "units": "dimensionless",
            "source_path": str(RESIDUALS / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv"),
            "source_anchor": "DWS2646_0_delta_w_species;DWS2646_1_common_mode_projector;DWS2646_2_Xi_injection_rule",
            "zero_route_status": "QSRC_NO_PREFACTOR_NO_SHADOW_PACKAGE_NOT_DERIVED",
            "missing_for_claim": "parent epsilon_A vector or theorem-zero; material/source composition vector p_A; P_perp convention; source path for value; no-cancellation norm; WEP/R10/PPN/clock/orbital K/tau/projection kernels",
            "arena_links": "WEP;R10;PPN;clock;orbital;Newton",
            "numeric_value_present": "false",
            "source_path_present": as_bool((RESIDUALS / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv").exists()),
            "projection_ready": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "value_row_id": "DWFV2690_1_delta_w_shadow",
            "component": "Delta_w_shadow",
            "coefficient_symbol": "delta_w_shadow",
            "definition": "coefficient multiplying source-shadow/non-Hilbert/projector residual after Hilbert variation",
            "basis_formula": "T_active=T_H + delta_w_shadow J_shadow",
            "current_value": "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND",
            "value_type": "shadow_bound_interface_nonclaim",
            "units": "dimensionless_or_arena_normalized",
            "source_path": str(RESIDUALS / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_DELTAW_SHADOW_BOUND_INTERFACE.csv"),
            "source_anchor": "DSH2617_0_delta_w_shadow;DSH2617_5_nonclaim_lock",
            "zero_route_status": "SOURCE_SHADOW_ZERO_NOT_DERIVED",
            "missing_for_claim": "shadow basis source paths; parent normal-form classification; arena projection; numeric bound table or theorem-zero",
            "arena_links": "WEP;R10;PPN;clock;orbital;Newton",
            "numeric_value_present": "false",
            "source_path_present": as_bool((RESIDUALS / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_DELTAW_SHADOW_BOUND_INTERFACE.csv").exists()),
            "projection_ready": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2690_0_all_signed", "true", "true", "true", "true", "true", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2690_1_qsrc_only", "true", "false", "false", "false", "false", "false", "false", "REJECT_QSRC_ONLY"),
        ("DRY2690_2_prefactor_open", "true", "true", "false", "true", "false", "false", "false", "REJECT_PREACTION_WEIGHT_BYPASS"),
        ("DRY2690_3_shadow_open", "true", "true", "true", "false", "false", "false", "false", "REJECT_SOURCE_SHADOW_BYPASS"),
        ("DRY2690_4_values_missing", "false", "false", "false", "false", "false", "false", "false", "REJECT_VALUE_ROWS_MISSING"),
        ("DRY2690_5_values_without_projection", "false", "false", "false", "false", "true", "false", "false", "REJECT_VALUES_WITHOUT_PROJECTIONS"),
        ("DRY2690_6_ward_only", "false", "false", "false", "false", "false", "false", "true", "REJECT_WARD_ONLY"),
        ("DRY2690_7_cancellation_only", "false", "false", "false", "false", "true", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
    ]
    return [
        {
            "case_id": row[0],
            "qsrc_written": row[1],
            "parent_adoption_signed": row[2],
            "no_prefactor_signed": row[3],
            "no_shadow_signed": row[4],
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
        case["qsrc_written"] == "true"
        and case["parent_adoption_signed"] == "true"
        and case["no_prefactor_signed"] == "true"
        and case["no_shadow_signed"] == "true"
    ):
        return "THEOREM_READY_IF_PARENT_SIGNED"
    if case["qsrc_written"] == "true" and case["parent_adoption_signed"] == "false":
        return "REJECT_QSRC_ONLY"
    if case["parent_adoption_signed"] == "true" and case["no_prefactor_signed"] == "false":
        return "REJECT_PREACTION_WEIGHT_BYPASS"
    if case["no_shadow_signed"] == "false" and case["parent_adoption_signed"] == "true":
        return "REJECT_SOURCE_SHADOW_BYPASS"
    if case["value_rows_present"] == "true":
        return "REJECT_VALUES_WITHOUT_PROJECTIONS"
    return "REJECT_VALUE_ROWS_MISSING"


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
        ("CG2690_0_qsrc", "q_src is written and parent-adopted before coupling", "FAIL_PARENT_ADOPTION_NOT_DERIVED", "QPK2690_3_parent_adoption", "false"),
        ("CG2690_1_no_prefactor", "pre-action source prefactors are impossible", "FAIL_NO_PREFACTOR_THEOREM_NOT_DERIVED", "QPK2690_4_no_prefactor", "false"),
        ("CG2690_2_no_shadow", "source-shadow/projector/non-Hilbert bypass is zero or bounded", "FAIL_SHADOW_PACKAGE_NOT_ZEROED", "QPK2690_5_no_shadow", "false"),
        ("CG2690_3_action_line", "action-density line/measure owner is signed", "FAIL_ACTION_DENSITY_LINE_OWNER_UNSIGNED", "QPK2690_7_action_line", "false"),
        ("CG2690_4_projected_mass", "Newton/GM projected source calibration is closed", "FAIL_PROJECTED_MASS_OPEN", "QPK2690_8_projected_mass", "false"),
        ("CG2690_5_value_rows", "finite Delta_w first rows are numeric/theorem-zero and projected", "FAIL_FIRST_VALUE_ROWS_NONCLAIM", "DWFV2690_0_delta_w_species;DWFV2690_1_delta_w_shadow", "false"),
        ("CG2690_6_guards", "Ward-only and cancellation-only shortcuts are refused", "PASS_GUARD_ONLY", "QG2690_6_ward_guard;QG2690_7_no_cancellation", "true"),
        ("CG2690_7_verdict", "source-coupling/local-GR branch can claim pass", "CLAIM_BLOCKED", "CG2690_0_qsrc through CG2690_6_guards", "false"),
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
            "decision_id": "DEC2690_0_qsrc",
            "decision": "DO_NOT_PROMOTE_QSRC_PACKAGE",
            "reason": "q_src is mathematically clean, but parent adoption, no-prefactor, source-shadow zero and projected-mass calibration are not derived together.",
            "status": "QSRC_PACKAGE_NOT_PARENT_DERIVED",
            "next_dependency": "parent action normal-form/source-map classifier",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2690_1_prefactor_shadow",
            "decision": "COMBINE_PREFACTOR_AND_SHADOW_AS_ONE OWNER DEBT",
            "reason": "A clean quotient still fails if labels enter before variation or return after Hilbert extraction.",
            "status": "BYPASSES_UNIFIED",
            "next_dependency": "classify allowed parent action source maps and residual channels",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2690_2_value_rows",
            "decision": "CREATE_FIRST_DELTAW_VALUE_ROWS_AS_NONCLAIM",
            "reason": "Delta_w_species and Delta_w_shadow now have explicit source paths, units and blockers, but no numeric value or theorem-zero.",
            "status": "FIRST_VALUE_ROWS_STAGED_NONCLAIM",
            "next_dependency": "parent epsilon/shadow values or theorem-zero plus arena kernels",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2690_3_next",
            "decision": "ATTACK_PARENT_ACTION_NORMAL_FORM_CLASSIFIER_NEXT",
            "reason": "The next leap is not more q_src algebra; it is a normal-form classifier saying where every source-like term lives.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2691 parent action normal-form source-map classifier or Delta_w value acquisition",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2690_0_selected",
            "kind": "selected",
            "target_doc": "2691-Y5-R2FR-parent-action-normal-form-source-map-classifier-or-delta-w-value-acquisition.md",
            "target_script": "scripts/Y5_R2FR_parent_action_normal_form_source_map_classifier_or_delta_w_value_acquisition_2691.py",
            "purpose": "classify every source-like parent term as Hilbert matter, left-hand geometry, boundary/improvement, nonvariational inconsistency, decoupled residual, or explicit finite Delta_w row",
            "acceptance_gate": "all pre-action prefactor and source-shadow/projector channels are either forbidden by parent normal form, reclassified as non-source geometry/boundary, or retained as finite sourced Delta_w/J_NH/projector rows",
            "forbidden_shortcuts": "q_src as theorem by definition; Ward-only proof; EOM division; action schema as derivation; source labels forgotten by preference; cancellation-only pass; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2690_0_qsrc", "source quotient", "MATHEMATICAL_QSRC_CLEAN_PARENT_ADOPTION_OPEN", "q_src exists as an exact quotient, but not as a parent-forced source domain"),
        ("STATUS2690_1_prefactor", "pre-action weights", "NO_PREFACTOR_THEOREM_NOT_DERIVED", "this is still the sharpest source-weight countermodel"),
        ("STATUS2690_2_shadow", "source-shadow bypass", "SHADOW_CLASSIFIED_NOT_ZEROED", "shadow is no longer vague, but needs normal-form classification or finite bounds"),
        ("STATUS2690_3_values", "Delta_w finite route", "FIRST_VALUE_ROWS_NONCLAIM", "Delta_w_species and Delta_w_shadow have explicit first value rows but no claim values"),
        ("STATUS2690_4_local_gr", "local GR/Newton", "SOURCE_SIDE_NOT_CLOSED", "source coupling is sharper, but Newton/GM projection and GR field-equation gates remain open"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2691 parent action normal-form source-map classifier",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2690_{name}",
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
    qsrc_package: list[dict[str, Any]],
    closure_gates: list[dict[str, Any]],
    bypasses: list[dict[str, Any]],
    value_rows: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    qsrc_written = any(row["package_id"] == "QPK2690_1_qsrc_definition" and row["current_status"] == "MATHEMATICAL_CONSTRUCTOR_WRITTEN" for row in qsrc_package)
    verdict_blocked = any(row["package_id"] == "QPK2690_9_verdict" and row["current_status"] == "PACKAGE_NOT_PARENT_DERIVED" for row in qsrc_package)
    gates_blocked = any(row["gate_id"] == "QG2690_8_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in closure_gates)
    bypasses_live = any(row["bypass_id"] == "BYP2690_0_preaction_weight" and row["status"] == "LIVE_COUNTERMODEL" for row in bypasses) and any(row["bypass_id"] == "BYP2690_4_postvariation_projector" and row["status"] == "LIVE_PROJECTOR_GATE" for row in bypasses)
    value_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in value_rows
    )
    value_sources_exist = all(row["source_path_present"] == "true" for row in value_rows)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2690_7_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2691" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2690_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2690_qsrc_constructor_written", qsrc_written, "q_src mathematical constructor is retained"),
        ("VAL2690_package_not_promoted", verdict_blocked, "q_src/no-prefactor/no-shadow package is not promoted"),
        ("VAL2690_closure_gates_block", gates_blocked, "closure gates block claims"),
        ("VAL2690_bypasses_retained", bypasses_live, "pre-action and post-variation bypasses are retained"),
        ("VAL2690_first_value_rows_nonclaim", value_nonclaim and value_sources_exist, "first Delta_w value rows are sourced as nonclaim and not score-ready"),
        ("VAL2690_dryrun_refusals", dryrun_ok, "dry-run refuses q_src-only, prefactor, shadow, Ward-only, missing values/projections and cancellation-only cases"),
        ("VAL2690_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2690_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2690_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2690_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2690_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2690_next_target_selected", next_target_ok, "2691 parent action normal-form source-map classifier target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2690_OVERALL",
            "passed": as_bool(overall),
            "detail": "2690 keeps q_src as a clean conditional, refuses package promotion, retains prefactor/shadow bypasses, and stages first Delta_w value rows",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    qsrc_package: list[dict[str, Any]],
    closure_gates: list[dict[str, Any]],
    bypasses: list[dict[str, Any]],
    value_rows: list[dict[str, Any]],
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
                "# 2690 - Y5/R2FR Source-Domain Quotient, No-Prefactor, No-Shadow Package or Delta-w First Value Row",
                "",
                "## Private Verdict",
                "",
                "`q_src` itself is clean: quotient labelled Hilbert-source families by their total stress and relative labels disappear. But `q_src` alone is not enough, because labels can enter before variation through `w_A S_A` or return after variation through source-shadow/projector/non-Hilbert channels.",
                "",
                "So 2690 does not close source universality. It does something useful instead: it makes the required package finite and explicit, and it creates first nonclaim value rows for `Delta_w_species` and `Delta_w_shadow` rather than pretending the rows are zero.",
                "",
                "No source-label, WEP, R10, PPN, clock, orbital, Newton, local-GR, GitHub, or public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## q_src / No-Prefactor / No-Shadow Package Audit",
                "",
                markdown_table(qsrc_package),
                "",
                "## Closure Gate",
                "",
                markdown_table(closure_gates),
                "",
                "## Bypass and Countermodel Ledger",
                "",
                markdown_table(bypasses),
                "",
                "## Delta-w First Value Rows",
                "",
                markdown_table(value_rows),
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
    qsrc_package = qsrc_package_rows()
    closure_gates = closure_gate_rows()
    bypasses = bypass_ledger_rows()
    value_rows = first_value_row()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["qsrc_package"], qsrc_package)
    write_csv(OUTPUTS["closure_gate"], closure_gates)
    write_csv(OUTPUTS["bypass_ledger"], bypasses)
    write_csv(OUTPUTS["first_value_row"], value_rows)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_qsrc_package"], qsrc_package)
    write_csv(BRANCH_OUTPUTS["local_first_value"], value_rows)
    write_csv(BRANCH_OUTPUTS["wep_qsrc_package"], qsrc_package)
    write_csv(BRANCH_OUTPUTS["wep_first_value"], value_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_first_value"], value_rows)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, qsrc_package, closure_gates, bypasses, value_rows, dry_results, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, qsrc_package, closure_gates, bypasses, value_rows, dry_cases, dry_results, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
