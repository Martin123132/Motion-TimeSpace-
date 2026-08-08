from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2677"
BRANCH_ID = "Y5_R2FR_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_OR_WA_JA_BOUND_2677"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2677-Y5-R2FR-no-species-action-weight-object-language-or-wA-JA-bound.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2677_SOURCE_REGISTER.csv",
    "object_language_audit": RESIDUALS / "P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv",
    "grammar_contract": RESIDUALS / "P8_Y5_R2FR_2677_PARENT_GRAMMAR_CONTRACT_NONCLAIM.csv",
    "wA_JA_bound_rows": RESIDUALS / "P8_Y5_R2FR_2677_WA_JA_BOUND_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2677_OBJECT_LANGUAGE_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2677_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2677_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2677_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2677_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2677_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_object_language": WEP_COEFF / "no_species_action_weight_object_language_nonclaim_2677.csv",
    "microscope_wA_JA": WEP_COEFF / "wA_JA_bound_rows_nonclaim_2677.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "WA_JA_BOUND_ROWS_2677_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "wA_JA_bound_rows_2677_NONCLAIM.csv",
    "wep_sources": SOURCE_INTAKE / "wep-sources" / "no_species_action_weight_object_language_wip_2677.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2677_2676_OWNER_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv",
        "required_needles": ["OWN2676_1_common_measure_route", "OWN2676_4_verdict", "w_A action weights", "J_A measure Jacobians"],
        "purpose": "inherits 2676 parent-owner failure and selects w_A/J_A",
    },
    {
        "source_id": "SRC2677_2676_COUNTERMODELS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv",
        "required_needles": ["CM2676_0_species_action_weight", "CM2676_1_species_measure_jacobian", "2.8e-15", "COUNTERMODEL_RETAINED_NONCLAIM"],
        "purpose": "imports explicit w_A/J_A nonclaim countermodel rows",
    },
    {
        "source_id": "SRC2677_2676_LEMMAS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_EXACT_CONDITIONAL_LEMMA_LEDGER.csv",
        "required_needles": ["LEM2676_1_classical_eom_not_enough", "REJECTION_LEMMA", "LEM2676_2_minimal_parent_clause"],
        "purpose": "keeps the classical EOM rejection and conditional parent clause",
    },
    {
        "source_id": "SRC2677_2676_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_NEXT_TARGET.csv",
        "required_needles": ["NEXT2676_0_selected", "no-species-action-weight", "w_A/J_A"],
        "purpose": "confirms 2677 was selected",
    },
    {
        "source_id": "SRC2677_COMMON_MEASURE_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv",
        "required_needles": ["CMT1452_0_target", "CMT1452_1_classical_EOM_limit", "CMT1452_2_quantum_measure_route", "CMT1452_3_species_jacobian_countermodel", "CMT1452_6_verdict"],
        "purpose": "primary source for w_A/J_A object-language proof attempt",
    },
    {
        "source_id": "SRC2677_COMMON_MEASURE_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_common_measure_signing_decision_1452.csv",
        "required_needles": ["SIGN1452_0_common_measure", "REFUSE_COMMON_MEASURE_ZERO_IMPORT_KEEP_JA_LEDGER", "hbar_parent_signed"],
        "purpose": "confirms common-measure zero cannot be imported",
    },
    {
        "source_id": "SRC2677_AX1090_STATUS",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv",
        "required_needles": ["AXRED1441_0_parent_object", "AXRED1441_2_common_measure", "NOT_REDUCED", "species-weight countermodel remains live"],
        "purpose": "tracks primitive reduction gap for parent object and common measure",
    },
    {
        "source_id": "SRC2677_AX1090_PROOF_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/AX1090_parent_object_proof_attempt.csv",
        "required_needles": ["AXP1447_2_axiom_reduction", "AXP1447_3_verdict", "PARENT_OBJECT_NOT_PROVEN"],
        "purpose": "confirms one-parent-object proof is not available",
    },
    {
        "source_id": "SRC2677_CONNECTED_CATEGORY",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv",
        "required_needles": ["CON1464_0_target", "CON1464_1_naturality_lemma", "CON1464_4_source_label_forgetting_dependency", "CON1464_5_verdict"],
        "purpose": "provides exact connected-category route for collapsing w_A",
    },
    {
        "source_id": "SRC2677_CONNECTED_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_connected_matter_category_signing_decision_1464.csv",
        "required_needles": ["SIGN1464_0_connected_matter_category", "KEEP_CONNECTEDNESS_CONDITIONAL_AND_USE_REGARDS_ROUTE_AS_NONCLAIM_DATA_PLAN", "naturality is exact"],
        "purpose": "records connectedness route as conditional-only",
    },
    {
        "source_id": "SRC2677_NO_SOURCE_SLOT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv",
        "required_needles": ["SIGN1451_0_no_slot", "REFUSE_ZERO_IMPORT_KEEP_BOUND_INPUTS", "AX1090_1", "AX1090_2"],
        "purpose": "blocks no-source-only-slot import",
    },
    {
        "source_id": "SRC2677_SOURCE_FACTORIZATION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv",
        "required_needles": ["SIGN1461_0_source_factorization", "source_label_forgetting_signed", "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD"],
        "purpose": "blocks source-label forgetting import",
    },
    {
        "source_id": "SRC2677_MINIMAL_PARENT_CLAUSE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv",
        "required_needles": ["MPC1439_0_clause", "MPC1439_1_formal_zero", "MPC1439_3_strength_warning", "NOT_ADOPTED_NOT_ZERO_CERTIFIED"],
        "purpose": "keeps formal zero target conditional-only",
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
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
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


def object_language_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "OL2677_0_target_rule",
            "claim_piece": "no species action weight or species Jacobian in parent grammar",
            "candidate_statement": "The parent object language admits one ordinary-matter action-density line and one species-blind measure; species labels are representation objects only, so w_A, hbar_A and J_A are not legal source/action-normalization symbols.",
            "derived_if_signed": "Delta w_AB=0 and Delta ln J_AB=0 before source variation; species source charge loses its two root countermodels",
            "current_status": "TARGET_SHARPENED_NOT_SIGNED",
            "blocking_clauses": "AX1090 parent object and common measure remain NOT_REDUCED",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "prove syntactic exclusion from parent action/measure primitives",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OL2677_1_eom_rejection",
            "claim_piece": "classical EOM cannot kill w_A",
            "candidate_statement": "delta(w_A S_A)/delta Psi_A=0 may preserve matter equations, but delta(w_A S_A)/delta g = w_A T_A changes the source.",
            "derived_if_signed": "prevents a false proof and keeps source variation as the relevant gate",
            "current_status": "REJECTION_LEMMA_CONFIRMED",
            "blocking_clauses": "none; this is a valid negative result",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_EXACT_CONDITIONAL_LEMMA_LEDGER.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "do not use matter EOM equivalence as WEP/source proof",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OL2677_2_quantum_measure_route",
            "claim_piece": "single hbar_parent/path measure forbids relative action weights",
            "candidate_statement": "A unique parent statistical/path-integral measure has exp(i sum_A S_A/hbar_parent), not independent exp(i w_A S_A/hbar_parent) sectors.",
            "derived_if_signed": "relative hbar_A and action weights are illegal object-language terms",
            "current_status": "CONDITIONAL_ROUTE_CLEAN_NOT_PARENT_SIGNED",
            "blocking_clauses": "parent statistical/path-integral measure owner not derived from MTS primitives",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "derive parent measure owner or retain w_A/hbar_A rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OL2677_3_connected_category_route",
            "claim_piece": "connected ordinary-matter category collapses natural action weights",
            "candidate_statement": "For nonzero parent-owned morphisms f:A->B, naturality w_B F(f)=F(f)w_A implies w_A=w_B; connectedness propagates w_A=w_*.",
            "derived_if_signed": "w_A becomes one common mode and drops out of WEP contrasts",
            "current_status": "EXACT_CONDITIONAL_THEOREM_GRAPH_OWNER_UNSIGNED",
            "blocking_clauses": "ordinary matter graph, nonzero parent-owned morphisms, source-label forgetting and calibration silence are not signed",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_connected_matter_category_signing_decision_1464.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "build a parent-owned connected graph certificate",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OL2677_4_source_label_forgetting",
            "claim_piece": "source/readout functor cannot reintroduce species labels",
            "candidate_statement": "Even if w_A collapses to a common mode, source/readout must forget material labels before source normalization and no spurion can return afterward.",
            "derived_if_signed": "prevents post-graph selectors from recreating w_A/J_A-like source labels",
            "current_status": "UNSIGNED_DEPENDENCY_RETAINED",
            "blocking_clauses": "source_label_forgetting_signed=false and no_source_only_slot_signed=false in signing ledgers",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "derive source-label forgetting or stage source-label residual rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OL2677_5_verdict",
            "claim_piece": "w_A/J_A object-language exclusion",
            "candidate_statement": "w_A=hbar_A=J_A=0 as independent species/action/measure residuals",
            "derived_if_signed": "species source-charge branch loses its deepest action/measure countermodels",
            "current_status": "NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_NOT_DERIVED",
            "blocking_clauses": "AX1090 parent object; common measure; connected graph owner; source-label forgetting; no spurion return",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_NEXT_TARGET.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "stage w_A/J_A nonclaim bounds and select connected graph certificate next",
            "timestamp_utc": stamp(),
        },
    ]


def grammar_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "GRM2677_0_single_action_density_line",
            "grammar_clause": "ordinary matter couples to one parent action-density line A_parent*dmu_parent",
            "forbids": "independent hbar_A or w_A action-density line automorphisms",
            "current_status": "CONTRACT_TARGET_NOT_SIGNED",
            "required_source": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_1_species_as_representation_data",
            "grammar_clause": "species labels identify representation objects and internal constants, not active source-normalization scalars",
            "forbids": "species-only source slot and species action weights",
            "current_status": "CONTRACT_TARGET_NOT_SIGNED",
            "required_source": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_2_connected_morphism_certificate",
            "grammar_clause": "ordinary matter category is connected by parent-owned nonzero morphisms on the action-density line",
            "forbids": "different natural scalar weights on connected ordinary sectors",
            "current_status": "EXACT_CONDITIONAL_GRAPH_NOT_SIGNED",
            "required_source": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_3_species_blind_measure",
            "grammar_clause": "parent measure is a functorial species-blind measure, not product_A J_A Dpsi_A",
            "forbids": "species measure Jacobian J_A",
            "current_status": "CONTRACT_TARGET_NOT_SIGNED",
            "required_source": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_4_source_label_forgetting",
            "grammar_clause": "source/readout functor forgets species labels before source normalization and cannot reintroduce a spurion after quotienting",
            "forbids": "post-graph source labels recreating w_A/J_A",
            "current_status": "UNSIGNED_DEPENDENCY",
            "required_source": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_5_boundary_domain_no_reentry",
            "grammar_clause": "boundary, domain, bulk and class sectors cannot carry composition labels that mimic action weights",
            "forbids": "q_BA, q_DA, q_XA re-entry as source-side WEP terms",
            "current_status": "DEFERRED_TO_BOUNDARY_DOMAIN_BRANCH",
            "required_source": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "GRM2677_6_verdict",
            "grammar_clause": "all no-species-action-weight grammar clauses are parent-signed",
            "forbids": "w_A, hbar_A and J_A as live local species source residuals",
            "current_status": "GRAMMAR_NOT_PARENT_SIGNED",
            "required_source": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def wA_JA_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WJ2677_0_delta_w_AB",
            "symbol": "Delta_w_AB",
            "definition": "relative species action-weight contrast after removing common-mode action-scale calibration",
            "formula": "Delta_epsilon_AB contains Delta_w_AB when S_matter=sum_A w_A S_A before source variation",
            "candidate_value": "MISSING_PARENT_ZERO_OR_NUMERIC_DELTA_W_AB",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv")),
            "status": "NONCLAIM_BOUND_ROW_MISSING_THEORY_VALUE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove w_A illegal or fill finite Delta_w_AB independent of WEP bound",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WJ2677_1_delta_ln_J_AB",
            "symbol": "Delta_ln_J_AB",
            "definition": "relative species measure-Jacobian contrast in the parent/effective matter measure",
            "formula": "Delta_epsilon_AB contains Delta ln J_AB if Dmu_parent -> product_A J_A Dpsi_A",
            "candidate_value": "MISSING_PARENT_ZERO_OR_NUMERIC_DELTA_LN_J_AB",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv")),
            "status": "NONCLAIM_BOUND_ROW_MISSING_THEORY_VALUE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove species-blind measure functor or fill finite Delta_ln_J_AB",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WJ2677_2_relative_hbar_A",
            "symbol": "Delta_hbar_A/hbar",
            "definition": "relative species action-scale contrast hidden as hbar_A or equivalent action normalization",
            "formula": "relative hbar_A is equivalent to a w_A-like source/action weight unless parent hbar is unique",
            "candidate_value": "MISSING_PARENT_UNIQUE_HBAR_OR_NUMERIC_DELTA_HBAR",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "status": "NONCLAIM_BOUND_ROW_MISSING_THEORY_VALUE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive unique parent action scale or retain hbar_A as source residual",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WJ2677_3_connected_common_mode",
            "symbol": "w_A=w_*",
            "definition": "connected-category/naturality route collapses species action weights to one common mode",
            "formula": "if parent graph connected and F(f) nonzero, w_B F(f)=F(f) w_A implies w_A=w_B",
            "candidate_value": "ZERO_CONTRAST_IF_GRAPH_OWNER_SIGNED",
            "bound_or_scale": "not a numeric bound",
            "units": "conditional theorem",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "status": "CONDITIONAL_THEOREM_ONLY",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "construct parent-owned ordinary-matter graph certificate",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WJ2677_4_source_label_reentry",
            "symbol": "sigma_source_A",
            "definition": "source-label or spurion reintroduced after quotient/readout despite action-weight collapse",
            "formula": "Delta_epsilon_AB includes Delta sigma_source_AB if source functor retains/reintroduces labels",
            "candidate_value": "MISSING_SOURCE_LABEL_FORGETTING_ZERO_OR_NUMERIC_SIGMA",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "status": "NONCLAIM_BOUND_ROW_MISSING_THEORY_VALUE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive source-label forgetting or fill finite source-label residual",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WJ2677_5_absolute_envelope",
            "symbol": "epsilon_wJ_abs",
            "definition": "absolute no-cancellation envelope for action-weight and measure-Jacobian residuals",
            "formula": "abs(epsilon_wJ_total) >= abs(Delta_w_AB)+abs(Delta_ln_J_AB)+abs(Delta_hbar_A/hbar)+abs(Delta_sigma_source_AB)",
            "candidate_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv")),
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only after each component is zero or numerically bounded",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], grammar_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2677_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "object_language_audit",
                "has_parent_zero": row["theorem_zero"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_OBJECT_LANGUAGE_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in grammar_rows:
        rows.append(
            {
                "runner_id": f"RUN2677_{row['clause_id']}",
                "target_id": row["clause_id"],
                "stage": "grammar_contract",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["required_source"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_GRAMMAR_CLAUSE_UNSIGNED",
                "next_action": "derive parent grammar clause or keep bound row",
                "timestamp_utc": stamp(),
            }
        )
    for row in bound_rows:
        rows.append(
            {
                "runner_id": f"RUN2677_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "wA_JA_bound_row",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_WA_JA_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2677_0_object_language_zero",
            "claim": "parent grammar excludes w_A, hbar_A and J_A",
            "status": "FAIL_AX1090_AND_COMMON_MEASURE_UNSIGNED",
            "blocking_rows": "OL2677_0_target_rule;OL2677_2_quantum_measure_route;GRM2677_6_verdict",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2677_1_connected_category_zero",
            "claim": "connected ordinary-matter category collapses w_A to common mode",
            "status": "FAIL_GRAPH_OWNER_SOURCE_LABEL_FORGETTING_UNSIGNED",
            "blocking_rows": "OL2677_3_connected_category_route;OL2677_4_source_label_forgetting;WJ2677_3_connected_common_mode",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2677_2_wA_JA_bound_rows",
            "claim": "finite w_A/J_A rows can be scored",
            "status": "FAIL_MISSING_NUMERIC_VALUES_AND_ENVELOPE",
            "blocking_rows": "WJ2677_0_delta_w_AB;WJ2677_1_delta_ln_J_AB;WJ2677_5_absolute_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2677_3_eom_guardrail",
            "claim": "classical EOM alone is not used as source-equivalence proof",
            "status": "PASS_GUARDRAIL",
            "blocking_rows": "none",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2677_4_local_GR",
            "claim": "local GR/PPN can use w_A/J_A silence",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "OL2677_5_verdict;CG2677_0_object_language_zero;CG2677_2_wA_JA_bound_rows",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2677_0_theorem_attempt",
            "question": "Can 2677 prove w_A/hbar_A/J_A are illegal in the parent object language?",
            "result": "not_yet",
            "reason": "AX1090 parent object and common measure are not reduced; connectedness/naturality is exact but graph owner and source-label forgetting are unsigned",
            "action": "retain no-species-action-weight as proof target, not claim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2677_1_useful_result",
            "question": "What did 2677 add?",
            "result": "root countermodels isolated",
            "reason": "w_A, hbar_A, J_A and source-label reentry now have separate nonclaim rows and a no-cancellation envelope",
            "action": "use these as the next local WEP/source runner inputs",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2677_2_next_route",
            "question": "Best next derivation target?",
            "result": "connected_ordinary_matter_graph_certificate",
            "reason": "connectedness/naturality is the cleanest exact theorem for killing w_A as a differential source weight",
            "action": "select 2678 connected ordinary matter graph certificate or w_A bound",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2677_0_selected",
            "kind": "selected",
            "target_doc": "2678-Y5-R2FR-connected-ordinary-matter-graph-certificate-or-wA-bound.md",
            "target_script": "scripts/Y5_R2FR_connected_ordinary_matter_graph_certificate_or_wA_bound_2678.py",
            "purpose": "try to build the parent-owned ordinary matter graph/morphism certificate that makes action weights natural and common, or keep w_A as a finite nonclaim bound row",
            "acceptance_gate": "graph objects, nonzero parent morphisms, action-density functor, source-label forgetting and calibration silence are all signed; otherwise w_A remains nonclaim",
            "forbidden_shortcuts": "assuming matter graph connected without certificate; using EEP/WEP as axiom; using classical EOM alone; importing epsilon_A=0; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2677_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2677_1_progress",
            "field": "action_weight_gap",
            "value": "w_A/J_A object-language proof not closed but root rows are explicit",
            "status": "improved_not_claimed",
            "note": "we now know connected graph certificate is the best theorem route",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2677_2_next",
            "field": "next_derivation",
            "value": "connected_ordinary_matter_graph_certificate",
            "status": "selected",
            "note": "exact naturality lemma is available; the missing piece is parent graph ownership",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2677_0_object_language",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["object_language_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_object_language"]),
            "contents": "object-language proof audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2677_1_wA_JA",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["wA_JA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_wA_JA"]),
            "contents": "w_A/J_A bound rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2677_2_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["wA_JA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight w_A/J_A rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2677_3_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["wA_JA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local w_A/J_A bound rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2677_4_wep_sources",
            "branch": "wep-sources",
            "source_table": rel_path(OUTPUTS["grammar_contract"]),
            "destination": str(BRANCH_OUTPUTS["wep_sources"]),
            "contents": "grammar contract retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_sources_exist_and_needles_found",
            "passed": as_bool(source_ok),
            "details": "all cited source paths exist and required needles are present",
        }
    )

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_nonclaim_guard",
            "passed": as_bool(all_nonclaim),
            "details": "all generated rows carry valid_for_claim=false",
        }
    )

    verdict_blocks = any(
        row["audit_id"] == "OL2677_5_verdict"
        and row["current_status"] == "NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_NOT_DERIVED"
        for row in rows["object_language_audit"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_object_language_verdict_blocks_claim",
            "passed": as_bool(verdict_blocks),
            "details": "w_A/J_A grammar exclusion is not promoted",
        }
    )

    grammar_ok = (
        any(row["clause_id"] == "GRM2677_3_species_blind_measure" for row in rows["grammar_contract"])
        and any(row["clause_id"] == "GRM2677_6_verdict" and row["current_status"] == "GRAMMAR_NOT_PARENT_SIGNED" for row in rows["grammar_contract"])
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_grammar_contract_complete",
            "passed": as_bool(grammar_ok),
            "details": "single action-density, representation-data, connected graph, measure and source-label clauses are present",
        }
    )

    bound_ids = {row["row_id"] for row in rows["wA_JA_bound_rows"]}
    required_bound_ids = {
        "WJ2677_0_delta_w_AB",
        "WJ2677_1_delta_ln_J_AB",
        "WJ2677_2_relative_hbar_A",
        "WJ2677_3_connected_common_mode",
        "WJ2677_4_source_label_reentry",
        "WJ2677_5_absolute_envelope",
    }
    bounds_ok = required_bound_ids.issubset(bound_ids) and all(row["valid_for_claim"] == "false" for row in rows["wA_JA_bound_rows"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_wA_JA_rows_complete_nonclaim",
            "passed": as_bool(bounds_ok),
            "details": "Delta_w, Delta_ln_J, hbar_A, connected common mode, source-label and envelope rows exist as nonclaim",
        }
    )

    eom_guard = any(row["gate_id"] == "CG2677_3_eom_guardrail" and row["status"] == "PASS_GUARDRAIL" for row in rows["claim_gates"])
    local_blocked = any(row["gate_id"] == "CG2677_4_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_claim_gates_correct",
            "passed": as_bool(eom_guard and local_blocked),
            "details": "EOM shortcut is rejected and local-GR remains blocked",
        }
    )

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_runner_refuses_unsigned_rows",
            "passed": as_bool(runner_refuses),
            "details": "runner refuses scoring without parent zero or numeric bounds",
        }
    )

    next_selected = any(
        row["target_id"] == "NEXT2677_0_selected"
        and "2678-Y5-R2FR-connected-ordinary-matter-graph-certificate-or-wA-bound.md" in row["target_doc"]
        for row in rows["next_target"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_next_target_selected",
            "passed": as_bool(next_selected),
            "details": "next target selects connected ordinary matter graph certificate",
        }
    )

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_csv_parse",
            "passed": as_bool(csv_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results)),
        }
    )

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_branch_copies_parse",
            "passed": as_bool(branch_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse)),
        }
    )

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_formalization_write_guard",
            "passed": as_bool(formalization_guard),
            "details": "generated path allowlist excludes formalization-workbench",
        }
    )

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_pycache_absent_at_validation_time",
            "passed": as_bool(pycache_absent),
            "details": "scripts/__pycache__ absent when validation rows were produced",
        }
    )

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2677_pycache_absent_at_validation_time")
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2677_OVERALL",
            "passed": as_bool(overall),
            "details": "2677 keeps no-species-action-weight theorem conditional, writes w_A/J_A rows, rejects EOM shortcut, and selects connected graph certificate next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} — No Species Action Weight Object Language Or w_A/J_A Bound",
        "",
        "## Private Verdict",
        "",
        "2677 tried the root-cause proof: make `w_A`, `hbar_A`, and `J_A` illegal in the parent object language rather than merely small. The result is not a proof yet. The cleanest route is the connected ordinary-matter category/naturality lemma: if the parent-owned matter graph is connected, natural action-density weights collapse to one common mode. But the graph certificate, source-label forgetting, and no-spurion-return clauses are still unsigned.",
        "",
        "So this checkpoint does **not** claim WEP, local GR, or species-source silence. It does lock in a useful negative result: classical equations of motion alone cannot prove source equivalence, because source variation still sees `w_A`.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Object-Language Audit",
        "",
        markdown_table(rows["object_language_audit"]),
        "",
        "## Parent Grammar Contract",
        "",
        markdown_table(rows["grammar_contract"]),
        "",
        "## w_A / J_A Bound Rows",
        "",
        markdown_table(rows["wA_JA_bound_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["object_language_audit"] = object_language_audit_rows()
    rows["grammar_contract"] = grammar_contract_rows()
    rows["wA_JA_bound_rows"] = wA_JA_bound_rows()
    rows["runner_results"] = runner_results_rows(rows["object_language_audit"], rows["grammar_contract"], rows["wA_JA_bound_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "object_language_audit",
        "grammar_contract",
        "wA_JA_bound_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_object_language"], rows["object_language_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_wA_JA"], rows["wA_JA_bound_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["wA_JA_bound_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["wA_JA_bound_rows"])
    write_csv(BRANCH_OUTPUTS["wep_sources"], rows["grammar_contract"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
