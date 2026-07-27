from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1623"
INPUT_1623 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1623-Y5-R2FR-parent-object-language-field-list-or-finite-ZR-priors.md"

SOURCE_FILES = {
    "1622_doc": ROOT / "1622-Y5-R2FR-lambdaR-parent-origin-and-no-derivative-grammar-or-finite-ZR-row.md",
    "1622_validation": OUT / "P8_Y5_BRR545_1622_VALIDATION.csv",
    "1622_next": OUT / "P8_Y5_PARENT_QLOC_1622_NEXT_TARGET.csv",
    "1622_grammar": OUT / "P8_Y5_PARENT_QLOC_1622_NO_DERIVATIVE_GRAMMAR_AUDIT.csv",
    "1622_vertical": OUT / "P8_Y5_PARENT_QLOC_1622_VERTICAL_NULL_BAN_ATTEMPT.csv",
    "1622_finite": OUT / "P8_Y5_PARENT_QLOC_1622_FINITE_ZR_ROW.csv",
    "1055_parent_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1066_typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1078_proof": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1338_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1262_minimal": OUT / "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
    "1262_countermodel": OUT / "P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv",
    "1262_prior": OUT / "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
}

NEEDLES = {
    "1622_doc": ["VERTICAL_NULL_BAN_NOT_PARENT_SIGNED", "VAL1622_OVERALL"],
    "1622_validation": ["VAL1622_OVERALL", "PASS"],
    "1622_next": ["1623-Y5-R2FR-parent-object-language-field-list-or-finite-ZR-priors.md", "parent constructor list"],
    "1622_grammar": ["GRAM1622_6_verdict", "NO_DERIVATIVE_GRAMMAR_NOT_DERIVED"],
    "1622_vertical": ["VNB1622_5_verdict", "VERTICAL_NULL_BAN_NOT_PARENT_SIGNED"],
    "1622_finite": ["FZR1622_0_ZR", "MISSING_THEOREM_ZERO_OR_NUMERIC_PRIOR"],
    "1055_parent_contract": ["PAC1055_6_single_parent_action", "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS"],
    "1066_typing": ["OLT1066_6_verdict", "conditional_not_parent_derived"],
    "1078_proof": ["OL1078_4_verdict", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1107_exhaustion": ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
    "1236_certificate": ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1338_theorem": ["OLT1338_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1262_minimal": ["MIN1262_2_no_vertical_metric_connection", "NOT_PARENT_DERIVED"],
    "1262_countermodel": ["CM1262_1_vertical_metric_exists", "even representative variables can carry energy"],
    "1262_prior": ["PRIOR1262_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1623_SOURCE_REGISTER.csv"
FIELD_LIST_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1623_OBJECT_LANGUAGE_FIELD_LIST_AUDIT.csv"
NO_VERTICAL_METRIC = OUT / "P8_Y5_PARENT_QLOC_1623_NO_VERTICAL_METRIC_THEOREM_ATTEMPT.csv"
FINITE_PRIORS = OUT / "P8_Y5_PARENT_QLOC_1623_FINITE_ZR_PRIOR_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1623_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1623_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1623_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1623_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1623_VALIDATION.csv"

COPY_TARGETS = {
    FIELD_LIST_AUDIT: [
        QUARANTINE / "OBJECT_LANGUAGE_FIELD_LIST_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_object_language_field_list_audit_nonclaim_1623.csv",
    ],
    NO_VERTICAL_METRIC: [
        QUARANTINE / "NO_VERTICAL_METRIC_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_vertical_metric_theorem_attempt_nonclaim_1623.csv",
    ],
    FINITE_PRIORS: [
        QUARANTINE / "FINITE_ZR_PRIOR_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_ZR_prior_rows_nonclaim_1623.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1623.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1623.csv",
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
                "source_id": f"SRC1623_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1623_parent_object_language_field_list_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def field_list_rows() -> list[dict[str, Any]]:
    rows = [
        ("FL1623_0_positive_sorts", "allowed parent sorts", "Q_obs, observed coframe/metric/connection, matter fields, gauge/current data, representation constants, universal constants, topological levels, readout maps", "SCHEMA_AVAILABLE_NOT_PRIMITIVE_DERIVED", "a clean field-list contract exists"),
        ("FL1623_1_RAB_sort", "R_AB sort assignment", "must be compatibility/vertical representative data or constrained auxiliary, not independent physical scalar", "NOT_PARENT_DERIVED", "central missing proof for Z_R=0"),
        ("FL1623_2_no_vertical_metric_sort", "vertical metric/connection exclusion", "no G_vert or nabla_vert constructor on the R_AB fibre", "NOT_PARENT_DERIVED", "without this, vertical gradient energy is legal"),
        ("FL1623_3_no_hidden_coeff_slot", "visible coefficients exclude hidden/vertical arguments", "Coeff_vis[O] accepts Q_obs x Theta_rep x Top only; no C_hid or R_AB slot", "EXACT_IF_GRAMMAR_ACCEPTED_NOT_DERIVED", "protects against source/readout coefficient re-entry"),
        ("FL1623_4_source_label_forgetting", "source functor forgets species labels before gravity coupling", "T_total from one Hilbert variation, not per-species source weights", "CONDITIONAL_NOT_PARENT_DERIVED", "needed for WEP/R10/source-current branch"),
        ("FL1623_5_readout_stability", "EFT/readout preserves typed domains", "renormalized/readout maps do not regenerate C_hid -> Coeff_vis or R_AB gradient terms", "UNSIGNED_PARALLEL_GATE", "tree-level object language is insufficient alone"),
        ("FL1623_6_verdict", "parent field-list theorem", "FL1623_0 through FL1623_5 derived from MTS primitives", "PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED", "finite Z_R priors remain mandatory"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "field_list_id": field_list_id,
            "claim_piece": claim_piece,
            "typed_statement": typed_statement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv; P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv; P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for field_list_id, claim_piece, typed_statement, status, effect in rows
    ]


def no_vertical_metric_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NVM1623_0_exact_theorem_shape",
            "If R_AB is typed as compatibility/vertical representative data and no vertical metric/connection constructor exists, then no local kinetic term Z_R|nabla R_AB|^2 is well typed.",
            "EXACT_IF_OBJECT_LANGUAGE_SIGNED",
            "would close the no-derivative grammar without a plateau axiom",
        ),
        (
            "NVM1623_1_current_corpus",
            "Current object-language files provide the schema but not a primitive-to-parent derivation.",
            "SCHEMA_VALID_NOT_PARENT_DERIVED",
            "cannot import theorem-zero into MTS",
        ),
        (
            "NVM1623_2_countermodel",
            "If R_AB is a physical scalar or the parent contains G_vert/nabla_vert, the kinetic term is legal.",
            "COUNTERMODEL_ACTIVE",
            "finite Z_R branch cannot be deleted",
        ),
        (
            "NVM1623_3_boundary_readout",
            "Even a bulk no-vertical-metric theorem must protect boundary and readout maps from regenerating R_AB energy.",
            "BOUNDARY_READOUT_UNSIGNED",
            "B_R and arena projections remain live",
        ),
        (
            "NVM1623_4_verdict",
            "No-vertical-metric theorem",
            "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED",
            "Z_R=0 remains conditional; finite priors required",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "mathematical_statement": statement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv; P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv; P8_Y5_PARENT_QLOC_1622_VERTICAL_NULL_BAN_ATTEMPT.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, status, effect in rows
    ]


def finite_prior_rows() -> list[dict[str, Any]]:
    rows = [
        ("FZP1623_0_ZR", "Z_R", "kinetic residue / vertical-gradient coefficient", "MISSING_SOURCE_BACKED_INPUT", "kinetic normalization", "theorem-zero, sourced value, or explicit prior interval required"),
        ("FZP1623_1_MR2", "M_R^2", "mass gap / range owner", "MISSING_SOURCE_BACKED_INPUT", "mass^2 or length", "needed for ell_R=sqrt(Z_R/M_R^2) or finite Yukawa range"),
        ("FZP1623_2_JR", "J_R", "source current / source charge", "MISSING_SOURCE_BACKED_INPUT", "source-current units", "needed for local no-hair and R10/WEP amplitude"),
        ("FZP1623_3_BR", "B_R", "boundary/defect/readout tail", "MISSING_SOURCE_BACKED_INPUT", "boundary flux or alpha-tail units", "bulk no-operator theorem does not close edge leakage"),
        ("FZP1623_4_tau_R10", "tau_R10", "R10 arena projection", "MISSING_ARENA_PROJECTION", "dimensionless alpha mapping", "needed before alpha(lambda) comparison"),
        ("FZP1623_5_tau_PPN", "tau_PPN", "PPN/local-GR projection", "MISSING_ARENA_PROJECTION", "PPN dimensions", "needed before local GR/Newton claim"),
        ("FZP1623_6_tau_clock_orbital", "tau_clock/tau_orbital", "time/orbital projection", "MISSING_ARENA_PROJECTION", "yr^-1 or orbital residual units", "needed before clock/orbit comparison"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "prior_row_id": row_id,
            "coefficient": coefficient,
            "definition": definition,
            "status": status,
            "units": units,
            "required_next": required_next,
            "source_path": "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, coefficient, definition, status, units, required_next in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1623_0_sources", "1622 object-language target plus typed-object-language sources imported", "SOURCE_CONTEXT_READY", "field-list audit is source anchored"),
        ("RUN1623_1_field_list", "typed parent field-list schema inspected", "PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED", "schema exists but primitive derivation missing"),
        ("RUN1623_2_no_vertical_metric", "no vertical metric theorem attempt inspected", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED", "Z_R theorem-zero not available"),
        ("RUN1623_3_finite_priors", "finite Z_R/M_R/J_R/B_R/tau prior rows staged", "FINITE_ZR_PRIOR_ROWS_STAGED_NONCLAIM", "fallback branch is explicit"),
        ("RUN1623_4_local_GR", "object-language proof not closed", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1623_5_next", "last derivation route is primitive-to-parent constructor derivation", "SELECT_1624_PRIMITIVE_CONSTRUCTOR_DERIVATION_OR_ZR_PRIOR_ACQUISITION", "try primitive derivation once; otherwise acquire priors"),
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
        ("CG1623_0_field_list", "parent object-language field list", "BLOCKED", "schema valid but not primitive-derived"),
        ("CG1623_1_RAB_sort", "R_AB is compatibility/vertical data", "BLOCKED", "sort assignment not parent-derived"),
        ("CG1623_2_no_vertical_metric", "no vertical metric/connection", "BLOCKED", "countermodel active"),
        ("CG1623_3_no_derivative", "no R_AB/Lambda_R derivative grammar", "BLOCKED", "depends on object-language theorem"),
        ("CG1623_4_finite_priors", "finite Z_R priors claim-ready", "BLOCKED", "rows lack sourced values/projections"),
        ("CG1623_5_local_GR", "derived local GR/Newton recovery", "BLOCKED", "Z_R theorem-zero and finite tests not closed"),
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
        ("DEC1623_0_schema", "OBJECT_LANGUAGE_SCHEMA_EXISTS", "typed field-list certificate is coherent and useful as a private contract", "preserve it as a target"),
        ("DEC1623_1_no_theorem", "PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED", "current corpus lacks primitive-to-parent constructor derivation and no vertical metric exclusion", "do not claim Z_R=0/local GR"),
        ("DEC1623_2_finite", "FINITE_ZR_PRIOR_ROWS_STAGED_NONCLAIM", "finite prior rows now cover Z_R, M_R^2, J_R, B_R, and arena projections", "fill if derivation fails"),
        ("DEC1623_3_next", "NEXT_1624_PRIMITIVE_CONSTRUCTOR_DERIVATION_OR_ZR_PRIOR_ACQUISITION", "remaining derivation route is to build the parent constructor list directly from motion/time/space primitives", "attempt primitive derivation or move to data/prior acquisition"),
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
            "next_target": "1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md",
            "script": "scripts/Y5_R2FR_primitive_constructor_derivation_or_ZR_prior_acquisition.py",
            "objective": "attempt one direct derivation of the parent constructor/object-language list from motion-time-space primitives; if it cannot be derived, switch to acquiring finite Z_R/M_R/J_R/B_R priors and arena projections",
            "success_condition": "either a primitive-to-parent constructor theorem closes the no-vertical-metric gate, or finite prior acquisition begins with nonclaim rows",
            "do_not": "do not treat a schema as a theorem, do not hide vertical metric countermodels, do not keep deriving forever without finite-prior fallback, do not promote local GR",
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


def no_formalization_1623() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1623-Y5",
        "P8_Y5_PARENT_QLOC_1623",
        "P8_Y5_BRR545_1623",
        "Y5_R2FR_parent_object_language",
        "R2FR_object_language_field_list_audit_nonclaim_1623",
        "R2FR_finite_ZR_prior_rows_nonclaim_1623",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    field_list = read_csv(FIELD_LIST_AUDIT)
    no_vertical = read_csv(NO_VERTICAL_METRIC)
    priors = read_csv(FINITE_PRIORS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1623_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1623 local source paths exist"),
        ("VAL1623_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1623 source needles found"),
        ("VAL1623_2_input_dir_ready", INPUT_1623.exists(), "1623 quarantine input directory exists"),
        ("VAL1623_3_field_list_not_derived", any(row["status"] == "PARENT_OBJECT_LANGUAGE_FIELD_LIST_NOT_DERIVED" for row in field_list), "parent field-list theorem blocks promotion"),
        ("VAL1623_4_no_vertical_metric_not_derived", any(row["status"] == "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED" for row in no_vertical), "no-vertical-metric theorem not derived"),
        ("VAL1623_5_prior_rows_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in priors), "finite prior rows remain nonclaim"),
        ("VAL1623_6_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1623_7_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1623_8_decision_next", any(row["decision"] == "NEXT_1624_PRIMITIVE_CONSTRUCTOR_DERIVATION_OR_ZR_PRIOR_ACQUISITION" for row in decisions), "decision selects primitive-constructor or prior-acquisition next target"),
        ("VAL1623_9_next_target_selected", any("1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1623_10_csv_parse", csv_parses(generated_csvs), "all generated 1623 CSVs parse"),
        ("VAL1623_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1623 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1623_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1623_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1623_14_formalization_untouched", no_formalization_1623(), "no 1623 outputs found under formalization-workbench"),
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
            "check_id": "VAL1623_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1623 parent object-language field-list or finite ZR priors validation",
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
    field_rows = read_csv(FIELD_LIST_AUDIT)
    metric_rows = read_csv(NO_VERTICAL_METRIC)
    prior_rows = read_csv(FINITE_PRIORS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1623 - R2/fR Parent Object-Language Field List Or Finite ZR Priors

## Verdict
- 1623 confirms the parent object-language certificate is coherent, but not derived from MTS primitives.
- The no-vertical-metric theorem remains exact only if that certificate is parent-signed; current evidence does not prove `R_AB` is nonphysical compatibility data.
- The countermodel is still live: if `R_AB` is a physical scalar or a vertical fibre metric/connection exists, `Z_R (nabla R_AB)^2` is a legal operator.
- Finite nonclaim prior rows now cover `Z_R`, `M_R^2`, `J_R`, `B_R`, and arena projections for R10/PPN/clock/orbital tests.
- Next target is decisive: either attempt a primitive-to-parent constructor derivation from motion/time/space, or begin finite-prior acquisition rather than endlessly recycling closure language.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Object-Language Field-List Audit

{md_table(field_rows, ["field_list_id", "claim_piece", "typed_statement", "status", "effect"])}

## No-Vertical-Metric Theorem Attempt

{md_table(metric_rows, ["theorem_id", "mathematical_statement", "status", "effect"])}

## Finite ZR Prior Rows

{md_table(prior_rows, ["prior_row_id", "coefficient", "definition", "status", "units", "required_next"])}

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
    INPUT_1623.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        FIELD_LIST_AUDIT: field_list_rows(),
        NO_VERTICAL_METRIC: no_vertical_metric_rows(),
        FINITE_PRIORS: finite_prior_rows(),
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
