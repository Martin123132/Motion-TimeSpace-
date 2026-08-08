from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1622"
INPUT_1622 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1622-Y5-R2FR-lambdaR-parent-origin-and-no-derivative-grammar-or-finite-ZR-row.md"

SOURCE_FILES = {
    "1621_doc": ROOT / "1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md",
    "1621_validation": OUT / "P8_Y5_BRR545_1621_VALIDATION.csv",
    "1621_next": OUT / "P8_Y5_PARENT_QLOC_1621_NEXT_TARGET.csv",
    "1621_constraint": OUT / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv",
    "1621_finite": OUT / "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv",
    "1562_origin": OUT / "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
    "1563_grammar": OUT / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv",
    "1238_first_class": OUT / "P8_Y5_R10_1238_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv",
    "1247_legitimacy": OUT / "P8_Y5_R10_1247_LAMBDAR_LEGITIMACY_TEST.csv",
    "1257_selector": OUT / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
    "1262_minimal": OUT / "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
    "1262_theorem": OUT / "P8_Y5_R10_1262_VERTICAL_NULL_THEOREM_CANDIDATE.csv",
    "1262_countermodel": OUT / "P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv",
    "1262_prior": OUT / "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
    "1528_energy": OUT / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
    "1529_bounds": OUT / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv",
}

NEEDLES = {
    "1621_doc": ["NO_POLE_NOT_DERIVED_CURRENT_MTS", "VAL1621_OVERALL"],
    "1621_validation": ["VAL1621_OVERALL", "PASS"],
    "1621_next": ["1622-Y5-R2FR-lambdaR-parent-origin-and-no-derivative-grammar-or-finite-ZR-row.md", "lambda_R/Z_R"],
    "1621_constraint": ["CFG1621_7_verdict", "CONSTRAINT_FIRST_ZMAP_NOT_DERIVED"],
    "1621_finite": ["FCR1621_1_Z_kinetic_residue", "MISSING_NO_POLE_OR_FINITE_RESIDUE"],
    "1562_origin": ["ORG1562_3_second_class_auxiliary", "BEST_CONDITIONAL_ROUTE"],
    "1563_grammar": ["GRAM1563_5_verdict", "FAIL_CURRENT_THEOREM"],
    "1238_first_class": ["FCR1238_5_verdict", "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED"],
    "1247_legitimacy": ["LRT1247_5_closure_guard", "lambda_R is closure with formal clothes on"],
    "1257_selector": ["SEL1257_0_field_exclusion", "SEL1257_2_generic_field_rule"],
    "1262_minimal": ["MIN1262_2_no_vertical_metric_connection", "NOT_PARENT_DERIVED"],
    "1262_theorem": ["THEO1262_0_vertical_null_ban", "EXACT_CONDITIONAL_NOT_PARENT_DERIVED"],
    "1262_countermodel": ["CM1262_1_vertical_metric_exists", "MIN1262_2 is essential"],
    "1262_prior": ["PRIOR1262_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1528_energy": ["LPE1528_6_theorem_shape", "THEOREM_SHAPE_WRITTEN_NOT_SIGNED"],
    "1529_bounds": ["BIN1529_8_no_cancellation_guard", "GUARD_WRITTEN"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1622_SOURCE_REGISTER.csv"
ORIGIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1622_LAMBDAR_PARENT_ORIGIN_AUDIT.csv"
GRAMMAR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1622_NO_DERIVATIVE_GRAMMAR_AUDIT.csv"
VERTICAL_NULL = OUT / "P8_Y5_PARENT_QLOC_1622_VERTICAL_NULL_BAN_ATTEMPT.csv"
FINITE_ZR = OUT / "P8_Y5_PARENT_QLOC_1622_FINITE_ZR_ROW.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1622_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1622_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1622_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1622_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1622_VALIDATION.csv"

COPY_TARGETS = {
    ORIGIN_AUDIT: [
        QUARANTINE / "LAMBDAR_PARENT_ORIGIN_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_lambdaR_parent_origin_audit_nonclaim_1622.csv",
    ],
    GRAMMAR_AUDIT: [
        QUARANTINE / "NO_DERIVATIVE_GRAMMAR_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_derivative_grammar_audit_nonclaim_1622.csv",
    ],
    VERTICAL_NULL: [
        QUARANTINE / "VERTICAL_NULL_BAN_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_vertical_null_ban_attempt_nonclaim_1622.csv",
    ],
    FINITE_ZR: [
        QUARANTINE / "FINITE_ZR_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_ZR_row_nonclaim_1622.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1622.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1622.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1622_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1622_lambdaR_parent_origin_no_derivative_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def origin_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("ORG1622_0_target", "derive lambda_R/Z_R as parent-owned algebraic constraint", "lambda_R C_R with C_R=R_AB must be selected by parent field grammar or phase-volume/current identity before readout", "TARGET_DEFINED", "keeps the constraint-first route precise"),
        ("ORG1622_1_variational_effect", "delta_lambda S=R_AB=0", "bare multiplier imposes the constraint", "FORMAL_PASS_NOT_DERIVATION", "variation works but explains nothing about parent origin"),
        ("ORG1622_2_phase_volume_current", "phase-volume/current grammar selects C_R=R_AB", "radial t-r cell balance or current-chain identity must force C_R rather than arbitrary volume constraint", "MOTIVATION_ONLY", "current files motivate but do not derive the constraint"),
        ("ORG1622_3_object_language", "typed parent constructor list excludes independent R_AB field", "R_AB appears only as compatibility/constraint data, not as a propagating scalar with allowed kinetic terms", "NOT_PARENT_DERIVED", "without the constructor list, generic scalar countermodel survives"),
        ("ORG1622_4_second_class_auxiliary", "algebraic auxiliary elimination before matter coupling", "E_Lambda:C_R=0 and E_R fixes Lambda_R with no derivative grammar and stable reduced readout", "BEST_CONDITIONAL_ROUTE_NOT_SIGNED", "strongest route but still conditional"),
        ("ORG1622_5_first_class_rejection", "first-class gauge origin", "needs generator, bracket closure, boundary charge, degree count, matter/readout invariance", "NOT_CONSTRUCTED", "first-class route remains heavier and currently unbuilt"),
        ("ORG1622_6_verdict", "lambda_R parent origin", "ORG1622_2 through ORG1622_5 close from parent action", "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED", "do not import no-pole/local-GR result"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "origin_id": origin_id,
            "claim_piece": claim_piece,
            "mathematical_requirement": requirement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv; P8_Y5_R10_1247_LAMBDAR_LEGITIMACY_TEST.csv; P8_Y5_R10_1238_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for origin_id, claim_piece, requirement, status, effect in rows
    ]


def grammar_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("GRAM1622_0_no_DRAB", "ban D_i R_AB and D_mu R_AB", "R_AB has no derivative operator because it is compatibility/vertical representative data, not a field", "REQUIRED_UNSIGNED", "Z_R remains finite if this is not parent-derived"),
        ("GRAM1622_1_no_DLambda", "ban D Lambda_R", "Lambda_R is an algebraic reaction variable, not a propagating multiplier field", "REQUIRED_UNSIGNED", "lambda_R hair survives if derivative terms are allowed"),
        ("GRAM1622_2_no_vertical_metric", "ban vertical fibre metric/connection", "no G_vert or nabla_vert exists that could make vertical gradients quotient-natural", "REQUIRED_UNSIGNED", "this is the central hidden-counterterm guard"),
        ("GRAM1622_3_no_boundary_derivative", "ban boundary/corner derivative terms for R_AB", "no proper edge kinetic/gradient term can regenerate Q_R/B_R after bulk elimination", "BOUNDARY_GRAMMAR_UNSIGNED", "edge hair remains a live residual"),
        ("GRAM1622_4_radiative_readout_closure", "readout/effective action preserves no-derivative grammar", "S_eff stays in parent-generated quotient image and cannot regenerate Z_R", "UNSIGNED", "tree-level grammar is not enough if readout reintroduces kinetic residue"),
        ("GRAM1622_5_countermodel", "if any derivative/vertical metric operator is legal", "locality allows int sqrt(h) Z_R h^{ij}D_iR_ABD_jR_AB", "FINITE_BRANCH_REQUIRED_IF_FAILS", "finite Z_R/M_R/J_R rows are mandatory"),
        ("GRAM1622_6_verdict", "no-derivative grammar", "GRAM1622_0 through GRAM1622_4 parent-signed", "NO_DERIVATIVE_GRAMMAR_NOT_DERIVED", "cannot claim Z_R=0 by grammar"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": grammar_id,
            "grammar_clause": clause,
            "mathematical_requirement": requirement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv; P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv; P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for grammar_id, clause, requirement, status, effect in rows
    ]


def vertical_null_rows() -> list[dict[str, Any]]:
    rows = [
        ("VNB1622_0_exact_conditional", "vertical-fibre null ban", "If R_AB is vertical representative data, S_loc descends through q, no vertical metric/connection exists, boundary/defects are silent, and readout preserves descent, then the Z_R gradient operator is illegal.", "EXACT_CONDITIONAL_THEOREM_RECORDED", "this is the best non-plateau derivation of Z_R=0"),
        ("VNB1622_1_no_plateau_smuggling", "operator ban instead of local extremum axiom", "D_i R_AB=0 is not assumed; the operator itself is forbidden by parent grammar if premises close.", "PLATEAU_AXIOM_AVOIDED_CONDITIONALLY", "keeps derivation discipline"),
        ("VNB1622_2_current_premises", "minimal assumptions MIN1262_0 through MIN1262_4", "all are currently not parent-derived or unsigned", "PREMISES_NOT_SIGNED", "the theorem cannot be imported into current MTS"),
        ("VNB1622_3_countermodel", "physical scalar or vertical metric countermodel", "if R_AB is physical or a vertical metric exists, the kinetic term is legal", "COUNTERMODEL_ACTIVE", "finite branch must remain live"),
        ("VNB1622_4_lambda_phi_energy", "multiplier/no-hair energy theorem analogy", "energy identities can silence multiplier gradients only with branch, boundary and zero-mode certificates", "USEFUL_ANALOGY_NOT_ORIGIN_PROOF", "does not derive lambda_R origin"),
        ("VNB1622_5_verdict", "vertical-null import", "exact theorem plus all minimal assumptions parent-derived", "VERTICAL_NULL_BAN_NOT_PARENT_SIGNED", "Z_R theorem-zero blocked"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ban_id": ban_id,
            "claim_piece": claim_piece,
            "mathematical_statement": statement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_R10_1262_VERTICAL_NULL_THEOREM_CANDIDATE.csv; P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv; P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ban_id, claim_piece, statement, status, effect in rows
    ]


def finite_zr_rows() -> list[dict[str, Any]]:
    rows = [
        ("FZR1622_0_ZR", "Z_R kinetic residue", "Z_R", "MISSING_THEOREM_ZERO_OR_NUMERIC_PRIOR", "kinetic normalization", "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv", "legal if R_AB is physical or vertical metric exists"),
        ("FZR1622_1_MR2", "R_AB mass/range scale", "M_R^2 or lambda_Range", "MISSING_MASS_GAP_OR_RANGE", "mass^2 or length", "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv", "needed for ell_R=sqrt(Z_R/M_R^2) or Yukawa range"),
        ("FZR1622_2_JR", "R_AB/Z source current", "J_R or beta_source^R", "MISSING_SOURCE_CURRENT_ZERO_OR_BOUND", "source-current units", "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv", "source-current zero remains conditional"),
        ("FZR1622_3_BR", "R_AB boundary/defect charge", "B_R or Pi_R^n", "MISSING_BOUNDARY_NO_FLUX_OR_BOUND", "boundary flux units", "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv", "bulk grammar cannot erase edge hair"),
        ("FZR1622_4_Corigin", "lambda_R origin coefficient", "C_lambda_origin", "MISSING_PARENT_ORIGIN", "dimensionless_or_action-density scale", "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv", "bare multiplier rejected"),
        ("FZR1622_5_tau", "arena projection", "tau_R10/tau_PPN/tau_clock/tau_orbital", "MISSING_ARENA_PROJECTION", "arena-specific", "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv", "finite coefficients cannot be tested without observable kernels"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "finite_row_id": row_id,
            "residual_channel": channel,
            "coefficient": coefficient,
            "status": status,
            "units": units,
            "source_path": source_path,
            "blocker": blocker,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, channel, coefficient, status, units, source_path, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1622_0_sources", "1621 target plus lambda/grammar/vertical-null sources imported", "SOURCE_CONTEXT_READY", "1622 gate is source anchored"),
        ("RUN1622_1_origin", "lambda_R parent origin routes inspected", "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED", "no magic multiplier import"),
        ("RUN1622_2_grammar", "no-derivative grammar inspected", "NO_DERIVATIVE_GRAMMAR_NOT_DERIVED", "Z_R theorem-zero not available"),
        ("RUN1622_3_vertical_null", "vertical-fibre null ban recorded", "VERTICAL_NULL_BAN_EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "best proof shape survives as conditional"),
        ("RUN1622_4_finite", "finite Z_R/M_R/J_R/B_R rows staged", "FINITE_ZR_ROWS_STAGED_NONCLAIM", "fallback branch is explicit"),
        ("RUN1622_5_local_GR", "lambda/grammar proof not closed", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1622_6_next", "next narrow proof is parent object-language and vertical metric exclusion", "SELECT_1623_PARENT_OBJECT_LANGUAGE_FIELD_LIST_OR_FINITE_ZR_PRIORS", "derive constructor list or source finite priors"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "input_state": input_state,
            "runner_result": result,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, input_state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1622_0_lambda_origin", "lambda_R parent origin", "BLOCKED", "origin is motivated but not parent-derived"),
        ("CG1622_1_no_derivative", "no derivative grammar for R_AB/Lambda_R", "BLOCKED", "no vertical metric/object-language exclusion not signed"),
        ("CG1622_2_vertical_null", "vertical-fibre null ban imports Z_R=0", "BLOCKED", "exact theorem premises not parent-derived"),
        ("CG1622_3_no_pole", "no physical R_AB pole", "BLOCKED", "countermodel remains legal"),
        ("CG1622_4_finite_rows", "finite Z_R rows claim-ready", "BLOCKED", "rows lack sourced values, units, and arena projections"),
        ("CG1622_5_source_current", "J_R=0/source-current silence", "BLOCKED", "depends on descent and verticality"),
        ("CG1622_6_local_GR", "derived local GR/Newton recovery", "BLOCKED", "constraint/no-pole proof did not close"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1622_0_best_theorem", "VERTICAL_NULL_BAN_IS_BEST_NON_PLATEAU_ROUTE", "it bans the kinetic operator rather than assuming a local plateau", "keep as formal proof target"),
        ("DEC1622_1_no_import", "LAMBDAR_AND_ZR_THEOREM_ZERO_NOT_DERIVED", "parent origin, no-derivative grammar, no vertical metric, boundary, and readout closure remain unsigned", "do not claim local GR/no-pole"),
        ("DEC1622_2_finite", "FINITE_ZR_ROWS_STAGED_NONCLAIM", "Z_R, M_R^2, J_R, B_R, lambda origin, and arena projections are explicit missing rows", "fill with sourced values if proof fails"),
        ("DEC1622_3_next", "NEXT_1623_PARENT_OBJECT_LANGUAGE_FIELD_LIST_OR_FINITE_ZR_PRIORS", "the narrowest proof is now the typed parent constructor list/no vertical metric exclusion", "derive object-language field list or move to finite priors"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1623-Y5-R2FR-parent-object-language-field-list-or-finite-ZR-priors.md",
            "script": "scripts/Y5_R2FR_parent_object_language_field_list_or_finite_ZR_priors.py",
            "objective": "try to derive a typed parent constructor list showing R_AB is compatibility/vertical data with no vertical metric or derivative grammar; if this fails, fill finite Z_R/M_R/J_R/B_R prior rows",
            "success_condition": "either the no-vertical-metric object-language theorem closes, or finite Z_R prior rows replace theorem-zero language",
            "do_not": "do not assume R_AB is nonphysical, do not ban operators by taste, do not hide boundary/readout regeneration, do not promote local GR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1622() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1622-Y5",
        "P8_Y5_PARENT_QLOC_1622",
        "P8_Y5_BRR545_1622",
        "Y5_R2FR_lambdaR_parent_origin",
        "R2FR_lambdaR_parent_origin_audit_nonclaim_1622",
        "R2FR_finite_ZR_row_nonclaim_1622",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    origin = read_csv(ORIGIN_AUDIT)
    grammar = read_csv(GRAMMAR_AUDIT)
    vertical = read_csv(VERTICAL_NULL)
    finite = read_csv(FINITE_ZR)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1622_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1622 local source paths exist"),
        ("VAL1622_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1622 source needles found"),
        ("VAL1622_2_input_dir_ready", INPUT_1622.exists(), "1622 quarantine input directory exists"),
        ("VAL1622_3_origin_not_derived", any(row["status"] == "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED" for row in origin), "lambdaR parent origin blocks promotion"),
        ("VAL1622_4_grammar_not_derived", any(row["status"] == "NO_DERIVATIVE_GRAMMAR_NOT_DERIVED" for row in grammar), "no-derivative grammar is not parent-signed"),
        ("VAL1622_5_vertical_null_conditional", any(row["status"] == "VERTICAL_NULL_BAN_NOT_PARENT_SIGNED" for row in vertical), "vertical-null ban remains conditional"),
        ("VAL1622_6_finite_rows_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in finite), "finite ZR rows remain nonclaim"),
        ("VAL1622_7_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1622_8_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1622_9_decision_next", any(row["decision"] == "NEXT_1623_PARENT_OBJECT_LANGUAGE_FIELD_LIST_OR_FINITE_ZR_PRIORS" for row in decisions), "decision selects object-language/no-vertical-metric next target"),
        ("VAL1622_10_next_target_selected", any("1623-Y5-R2FR-parent-object-language-field-list-or-finite-ZR-priors.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1622_11_csv_parse", csv_parses(generated_csvs), "all generated 1622 CSVs parse"),
        ("VAL1622_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1622 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1622_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1622_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1622_15_formalization_untouched", no_formalization_1622(), "no 1622 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1622_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1622 lambdaR parent origin and no-derivative grammar or finite ZR row validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "/").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    origin_rows = read_csv(ORIGIN_AUDIT)
    grammar_rows = read_csv(GRAMMAR_AUDIT)
    vertical_rows = read_csv(VERTICAL_NULL)
    finite_rows = read_csv(FINITE_ZR)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1622 - R2/fR lambdaR Parent Origin And No-Derivative Grammar Or Finite ZR Row

## Verdict
- 1622 preserves the best derivation route: a vertical-fibre null ban can forbid the `Z_R (nabla R_AB)^2` operator without smuggling in a local plateau axiom.
- Current MTS still cannot import that result because `lambda_R` parent origin, typed object-language exclusion, no vertical metric/connection, boundary silence, and readout closure are not parent-signed.
- Bare `lambda_R R_AB` variation is explicitly refused as a derivation: it imposes `R_AB=0` only after the multiplier is inserted.
- Finite nonclaim rows are staged for `Z_R`, `M_R^2/range`, `J_R`, `B_R`, `lambda_R` origin, and arena projections.
- The next narrow target is the typed parent constructor list: prove `R_AB` is compatibility/vertical data with no vertical fibre metric, or stop using theorem-zero language and fill finite priors.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## lambdaR Parent Origin Audit

{md_table(origin_rows, ["origin_id", "claim_piece", "mathematical_requirement", "status", "effect"])}

## No-Derivative Grammar Audit

{md_table(grammar_rows, ["grammar_id", "grammar_clause", "mathematical_requirement", "status", "effect"])}

## Vertical Null Ban Attempt

{md_table(vertical_rows, ["ban_id", "claim_piece", "mathematical_statement", "status", "effect"])}

## Finite ZR Row

{md_table(finite_rows, ["finite_row_id", "residual_channel", "coefficient", "status", "units", "source_path", "blocker"])}

## Runner

{md_table(runner, ["runner_id", "input_state", "runner_result", "effect"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "status", "reason"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"])}

## Validation

{md_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1622.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        ORIGIN_AUDIT: origin_audit_rows(),
        GRAMMAR_AUDIT: grammar_audit_rows(),
        VERTICAL_NULL: vertical_null_rows(),
        FINITE_ZR: finite_zr_rows(),
        RUNNER: runner_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    generated_csvs = list(outputs.keys())
    remove_pycache()
    write_csv(VALIDATION, validation_rows(generated_csvs))
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
