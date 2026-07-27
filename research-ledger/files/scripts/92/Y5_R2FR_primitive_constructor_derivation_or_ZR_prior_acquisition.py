from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1624"
INPUT_1624 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md"

SOURCE_FILES = {
    "1623_doc": ROOT / "1623-Y5-R2FR-parent-object-language-field-list-or-finite-ZR-priors.md",
    "1623_validation": OUT / "P8_Y5_BRR545_1623_VALIDATION.csv",
    "1623_next": OUT / "P8_Y5_PARENT_QLOC_1623_NEXT_TARGET.csv",
    "1623_field_list": OUT / "P8_Y5_PARENT_QLOC_1623_OBJECT_LANGUAGE_FIELD_LIST_AUDIT.csv",
    "1623_no_vertical": OUT / "P8_Y5_PARENT_QLOC_1623_NO_VERTICAL_METRIC_THEOREM_ATTEMPT.csv",
    "1623_priors": OUT / "P8_Y5_PARENT_QLOC_1623_FINITE_ZR_PRIOR_ROWS.csv",
    "1237_primitive": OUT / "P8_Y5_R10_1237_MTS_PRIMITIVE_DERIVATION_AUDIT.csv",
    "1417_constructor": OUT / "P8_Y5_R10_1417_PRIMITIVE_CONSTRUCTOR_LIST_ATTEMPT.csv",
    "1417_exhaustion": OUT / "P8_Y5_R10_1417_CONSTRUCTOR_EXHAUSTION_PROOF_AUDIT.csv",
    "1568_recheck": OUT / "P8_Y5_PARENT_QLOC_1568_PRIMITIVE_DERIVATION_RECHECK.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1338_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1262_prior": OUT / "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
    "1262_countermodel": OUT / "P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv",
}

NEEDLES = {
    "1623_doc": ["PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED", "VAL1623_OVERALL"],
    "1623_validation": ["VAL1623_OVERALL", "PASS"],
    "1623_next": ["1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md", "finite prior acquisition"],
    "1623_field_list": ["FL1623_6_verdict", "PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED"],
    "1623_no_vertical": ["NVM1623_4_verdict", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED"],
    "1623_priors": ["FZP1623_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1237_primitive": ["PRIM1237_8_verdict", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED"],
    "1417_constructor": ["PCL1417_7_verdict", "CONSTRUCTOR_EXHAUSTION_NOT_PROVED"],
    "1417_exhaustion": ["PEX1417_7_verdict", "NOT_PROVED_CURRENT_CORPUS"],
    "1568_recheck": ["PRIM1568_4_verdict", "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL"],
    "1236_certificate": ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1338_theorem": ["OLT1338_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1262_prior": ["PRIOR1262_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1262_countermodel": ["CM1262_1_vertical_metric_exists", "even representative variables can carry energy"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1624_SOURCE_REGISTER.csv"
PRIMITIVE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1624_PRIMITIVE_CONSTRUCTOR_DERIVATION_AUDIT.csv"
NO_VERTICAL_METRIC_DECISION = OUT / "P8_Y5_PARENT_QLOC_1624_NO_VERTICAL_METRIC_DECISION.csv"
FINITE_PRIOR_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1624_FINITE_ZR_PRIOR_ACQUISITION_PLAN.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1624_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1624_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1624_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1624_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1624_VALIDATION.csv"

COPY_TARGETS = {
    PRIMITIVE_AUDIT: [
        QUARANTINE / "PRIMITIVE_CONSTRUCTOR_DERIVATION_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_primitive_constructor_derivation_audit_nonclaim_1624.csv",
    ],
    NO_VERTICAL_METRIC_DECISION: [
        QUARANTINE / "NO_VERTICAL_METRIC_DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_vertical_metric_decision_nonclaim_1624.csv",
    ],
    FINITE_PRIOR_ACQUISITION: [
        QUARANTINE / "FINITE_ZR_PRIOR_ACQUISITION_PLAN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_ZR_prior_acquisition_plan_nonclaim_1624.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1624.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1624.csv",
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
                "source_id": f"SRC1624_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1624_primitive_constructor_or_finite_prior_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def primitive_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PCD1624_0_motion_load", "motion-load primitive", "supplies local clock/load scaffold and Newtonian leading target", "PARTIAL_QOBS_SCAFFOLD_ONLY", "does not derive typed parent constructor exhaustion"),
        ("PCD1624_1_reciprocity", "T^2 S=1 / R_AB=0", "supplies GR-like radial routing if derived", "LOCAL_GR_ROUTE_CONDITIONAL_NOT_GRAMMAR", "does not type coefficients or exclude R_AB kinetic residue"),
        ("PCD1624_2_observer_map", "observed coframe/readout map", "supplies candidate Q_obs variables", "READOUT_SORT_PARTIAL_CONTRACT", "does not derive parent action domain or readout closure"),
        ("PCD1624_3_primitive_sort_exhaustion", "complete primitive constructor list", "Motion/Time/Space plus quotient/frame/matter/coefficients/measure/readout must exhaust parent syntax", "CONSTRUCTOR_EXHAUSTION_NOT_PROVED", "no source proves this list is forced rather than adopted"),
        ("PCD1624_4_no_species_source_slot", "Hom(SpeciesLabel,Coeff_active_source)=empty", "would forbid species/source weights and source-current rescalings", "EXACT_IF_TYPED_GRAMMAR_SIGNED_NOT_DERIVED", "typed grammar is a schema, not a primitive theorem"),
        ("PCD1624_5_action_measure_owner", "single parent action scale/current owner", "one measure/current owner makes species action multipliers impossible or gauge", "MISSING_PARENT_OWNER", "w_A S_A countermodel survives"),
        ("PCD1624_6_readout_transfer", "EFT/readout closure", "effective/readout maps preserve typed parent domains", "UNSIGNED_TRANSFER_GATE", "tree-level constructor list would not be test-grade alone"),
        ("PCD1624_7_verdict", "primitive-to-parent constructor derivation", "PCD1624_0 through PCD1624_6 close from MTS primitives", "PRIMITIVE_CONSTRUCTOR_DERIVATION_FAILS_CURRENT_CORPUS", "pivot to finite Z_R prior acquisition"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "route": route,
            "what_it_supplies": supplies,
            "result": result,
            "effect": effect,
            "source_anchors": "P8_Y5_R10_1237_MTS_PRIMITIVE_DERIVATION_AUDIT.csv; P8_Y5_R10_1417_PRIMITIVE_CONSTRUCTOR_LIST_ATTEMPT.csv; P8_Y5_R10_1417_CONSTRUCTOR_EXHAUSTION_PROOF_AUDIT.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, route, supplies, result, effect in rows
    ]


def no_vertical_metric_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("NVD1624_0_theorem_shape", "If parent constructor exhaustion proves no vertical metric/connection on R_AB fibre, Z_R kinetic residue is ill typed.", "EXACT_CONDITIONAL_RETAINED", "good theorem shape survives"),
        ("NVD1624_1_current_evidence", "Primitive constructor route does not prove the object language or no-vertical-metric exclusion.", "NOT_DERIVED_CURRENT_CORPUS", "cannot import Z_R=0"),
        ("NVD1624_2_countermodel", "If R_AB is physical or vertically metrized, Z_R (nabla R_AB)^2 is legal.", "COUNTERMODEL_ACTIVE", "finite Z_R branch remains live"),
        ("NVD1624_3_no_more_loop", "Further repetition of schema-only object-language checks is no longer useful without new primitives/source files.", "STOP_RECYCLING_THEOREM_ZERO", "move to priors unless new derivation evidence appears"),
        ("NVD1624_4_verdict", "No-vertical-metric theorem for current MTS.", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT", "finite-prior acquisition is selected"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "statement": statement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1623_NO_VERTICAL_METRIC_THEOREM_ATTEMPT.csv; P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv; P8_Y5_PARENT_QLOC_1568_PRIMITIVE_DERIVATION_RECHECK.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, statement, status, effect in rows
    ]


def finite_prior_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ1624_0_ZR", "Z_R", "kinetic residue / vertical-gradient coefficient", "theory_source_or_prior_interval", "kinetic normalization", "search local parent-action rows for theorem-zero; otherwise create bounded prior", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_1_MR2", "M_R^2", "mass gap / range owner", "theory_source_or_range_prior", "mass^2 or length", "source Hessian/mass-gap if available; otherwise define broad nonclaim range", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_2_JR", "J_R", "source current / source charge", "matter_descent_or_finite_source_bound", "source-current units", "derive zero only if descent closes; otherwise fill source-current coefficient prior", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_3_BR", "B_R", "boundary/defect/readout tail", "boundary_no_flux_or_flux_bound", "boundary flux or alpha-tail units", "source no-flux theorem or finite boundary envelope", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_4_tau_R10", "tau_R10", "R10 alpha(lambda) projection", "arena_projection_kernel", "dimensionless alpha mapping", "map Z_R/M_R/J_R into alpha(lambda) before R10 scoring", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_5_tau_PPN", "tau_PPN", "PPN/local-GR projection", "weak_field_projection_kernel", "PPN units", "map finite branch into gamma,beta,alpha_i,xi/source normalization", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_6_tau_clock_orbital", "tau_clock/tau_orbital", "clock/orbital projection", "time_or_orbital_kernel", "yr^-1 or orbital residual units", "map finite branch into Gdot/GMdot/orbital drift channels", "NOT_STARTED_NONCLAIM"),
        ("ACQ1624_7_runner_policy", "finite-prior runner policy", "no score-ready prediction until all required priors and arena maps are numeric/source-backed", "claim_safety_policy", "rule", "all rows valid_for_claim=false until no MISSING markers remain", "ACTIVE_GUARD"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "coefficient": coefficient,
            "definition": definition,
            "required_evidence": evidence,
            "units": units,
            "next_action": next_action,
            "status": status,
            "source_path": "P8_Y5_PARENT_QLOC_1623_FINITE_ZR_PRIOR_ROWS.csv; P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, coefficient, definition, evidence, units, next_action, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1624_0_sources", "1623 target plus primitive-constructor audits imported", "SOURCE_CONTEXT_READY", "1624 is anchored to current evidence"),
        ("RUN1624_1_primitive", "motion/time/space primitive constructor derivation rechecked", "PRIMITIVE_CONSTRUCTOR_DERIVATION_FAILS_CURRENT_CORPUS", "schema remains nonclaim"),
        ("RUN1624_2_no_vertical", "no-vertical-metric theorem current status checked", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT", "Z_R theorem-zero remains blocked"),
        ("RUN1624_3_pivot", "finite Z_R/M_R/J_R/B_R/tau acquisition plan staged", "FINITE_ZR_PRIOR_ACQUISITION_STARTED_NONCLAIM", "fallback branch begins"),
        ("RUN1624_4_local_GR", "neither theorem-zero nor finite priors are claim-ready", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1624_5_next", "next step is finite prior row builder", "SELECT_1625_FINITE_ZR_PRIOR_ROW_BUILDER", "build schema/runner for numeric/source-backed priors"),
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
        ("CG1624_0_primitive_constructor", "primitive-to-parent constructor theorem", "BLOCKED", "current evidence says derivation fails"),
        ("CG1624_1_no_vertical_metric", "no vertical metric/connection", "BLOCKED", "countermodel remains live"),
        ("CG1624_2_ZR_zero", "Z_R theorem-zero", "BLOCKED", "object-language/no-vertical-metric proof not derived"),
        ("CG1624_3_finite_priors", "finite Z_R priors claim-ready", "BLOCKED", "acquisition plan exists but rows are not numeric/source-backed"),
        ("CG1624_4_arena_projection", "R10/PPN/clock/orbital arena projections", "BLOCKED", "projection kernels missing"),
        ("CG1624_5_local_GR", "derived local GR/Newton recovery", "BLOCKED", "neither exact theorem nor finite test branch is closed"),
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
        ("DEC1624_0_derivation", "PRIMITIVE_CONSTRUCTOR_DERIVATION_FAILS_CURRENT_CORPUS", "1237/1417/1568 already show motion/time/space primitives do not derive the sorted object language", "stop spending theorem-zero credit here"),
        ("DEC1624_1_no_vertical", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT", "the theorem shape is exact conditional, but current evidence does not sign its premises", "keep it as future theorem target only if new primitives appear"),
        ("DEC1624_2_pivot", "FINITE_ZR_PRIOR_ACQUISITION_STARTED_NONCLAIM", "finite rows for Z_R, M_R^2, J_R, B_R, and arena kernels are now the honest route", "build finite-prior row builder next"),
        ("DEC1624_3_next", "NEXT_1625_FINITE_ZR_PRIOR_ROW_BUILDER", "the next aligned move is empirical/prior plumbing, not another closure-loop theorem audit", "construct nonclaim schema and runner for finite Z_R branch"),
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
            "next_target": "1625-Y5-R2FR-finite-ZR-prior-row-builder-and-arena-projection-schema.md",
            "script": "scripts/Y5_R2FR_finite_ZR_prior_row_builder_and_arena_projection_schema.py",
            "objective": "build nonclaim finite-prior rows for Z_R, M_R^2, J_R, B_R, tau_R10, tau_PPN, tau_clock, and tau_orbital, with units, required source evidence, and runner refusal gates",
            "success_condition": "finite Z_R branch has parseable nonclaim prior/acquisition rows and a runner that refuses claims until numeric source-backed inputs and arena maps exist",
            "do_not": "do not reopen theorem-zero, do not score placeholders, do not promote local GR, do not claim R10/PPN/clock/orbital pass",
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


def no_formalization_1624() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1624-Y5",
        "P8_Y5_PARENT_QLOC_1624",
        "P8_Y5_BRR545_1624",
        "Y5_R2FR_primitive_constructor",
        "R2FR_primitive_constructor_derivation_audit_nonclaim_1624",
        "R2FR_finite_ZR_prior_acquisition_plan_nonclaim_1624",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    primitive = read_csv(PRIMITIVE_AUDIT)
    no_vertical = read_csv(NO_VERTICAL_METRIC_DECISION)
    acquisition = read_csv(FINITE_PRIOR_ACQUISITION)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1624_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1624 local source paths exist"),
        ("VAL1624_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1624 source needles found"),
        ("VAL1624_2_input_dir_ready", INPUT_1624.exists(), "1624 quarantine input directory exists"),
        ("VAL1624_3_primitive_fails", any(row["result"] == "PRIMITIVE_CONSTRUCTOR_DERIVATION_FAILS_CURRENT_CORPUS" for row in primitive), "primitive constructor derivation fails current evidence"),
        ("VAL1624_4_no_vertical_final_block", any(row["status"] == "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT" for row in no_vertical), "no-vertical-metric theorem remains blocked"),
        ("VAL1624_5_finite_acquisition_started", any(row["status"] == "ACTIVE_GUARD" for row in acquisition), "finite prior acquisition policy staged"),
        ("VAL1624_6_acquisition_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in acquisition), "finite acquisition rows remain nonclaim"),
        ("VAL1624_7_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1624_8_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1624_9_decision_next", any(row["decision"] == "NEXT_1625_FINITE_ZR_PRIOR_ROW_BUILDER" for row in decisions), "decision selects finite ZR prior row builder next"),
        ("VAL1624_10_next_target_selected", any("1625-Y5-R2FR-finite-ZR-prior-row-builder-and-arena-projection-schema.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1624_11_csv_parse", csv_parses(generated_csvs), "all generated 1624 CSVs parse"),
        ("VAL1624_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1624 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1624_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1624_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1624_15_formalization_untouched", no_formalization_1624(), "no 1624 outputs found under formalization-workbench"),
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
            "check_id": "VAL1624_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1624 primitive constructor derivation or ZR prior acquisition validation",
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
    primitive_rows = read_csv(PRIMITIVE_AUDIT)
    no_vertical_rows = read_csv(NO_VERTICAL_METRIC_DECISION)
    acquisition_rows = read_csv(FINITE_PRIOR_ACQUISITION)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1624 - R2/fR Primitive Constructor Derivation Or ZR Prior Acquisition

## Verdict
- 1624 performs the direct primitive-to-parent constructor check and refuses promotion: current MTS primitives do not derive the sorted object language/no-vertical-metric theorem.
- Motion-load, reciprocity, and observer-map work remain valuable local-GR scaffolding, but they do not exhaust parent constructors or ban `Z_R (nabla R_AB)^2`.
- This ends the current theorem-zero loop for `Z_R`: without new primitive evidence, the honest route is finite prior acquisition.
- Finite nonclaim acquisition rows are started for `Z_R`, `M_R^2`, `J_R`, `B_R`, `tau_R10`, `tau_PPN`, `tau_clock`, and `tau_orbital`.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Primitive Constructor Derivation Audit

{md_table(primitive_rows, ["audit_id", "route", "what_it_supplies", "result", "effect"])}

## No-Vertical-Metric Decision

{md_table(no_vertical_rows, ["decision_id", "statement", "status", "effect"])}

## Finite ZR Prior Acquisition Plan

{md_table(acquisition_rows, ["acquisition_id", "coefficient", "definition", "required_evidence", "units", "next_action", "status"])}

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
    INPUT_1624.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        PRIMITIVE_AUDIT: primitive_audit_rows(),
        NO_VERTICAL_METRIC_DECISION: no_vertical_metric_decision_rows(),
        FINITE_PRIOR_ACQUISITION: finite_prior_acquisition_rows(),
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
