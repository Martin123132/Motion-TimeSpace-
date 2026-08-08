from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB_SECTOR / "docs"
QUARANTINE = MICROSCOPE / "quarantine" / "1625"
INPUT_1625 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1625-Y5-R2FR-finite-ZR-prior-row-builder-and-arena-projection-schema.md"

SOURCE_FILES = {
    "1624_doc": ROOT / "1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md",
    "1624_validation": OUT / "P8_Y5_BRR545_1624_VALIDATION.csv",
    "1624_next": OUT / "P8_Y5_PARENT_QLOC_1624_NEXT_TARGET.csv",
    "1624_acquisition": OUT / "P8_Y5_PARENT_QLOC_1624_FINITE_ZR_PRIOR_ACQUISITION_PLAN.csv",
    "1624_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1624_CLAIM_GATE.csv",
    "1624_decision": OUT / "P8_Y5_PARENT_QLOC_1624_DECISION.csv",
    "1262_prior_requirements": OUT / "P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv",
    "1264_source_requirements": OUT / "P8_Y5_R10_1264_FINITE_ZR_SOURCE_ROW_REQUIREMENTS.csv",
    "1265_runner_schema": OUT / "P8_Y5_R10_1265_FINITE_ZR_BOUND_RUNNER_SCHEMA.csv",
    "1563_fallback_ledger": OUT / "P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv",
    "1564_intake_status": OUT / "P8_Y5_PARENT_QLOC_1564_FINITE_ZR_INTAKE_STATUS.csv",
    "1565_source_intake": OUT / "P8_Y5_PARENT_QLOC_1565_FINITE_ZR_SOURCE_ROW_INTAKE.csv",
    "1566_validator_rules": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RULES.csv",
    "1566_validator_summary": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_SUMMARY.csv",
    "1623_prior_rows": OUT / "P8_Y5_PARENT_QLOC_1623_FINITE_ZR_PRIOR_ROWS.csv",
    "1262_countermodel": OUT / "P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv",
}

NEEDLES = {
    "1624_doc": [
        "PRIMITIVE_CONSTRUCTOR_DERIVATION_FAILS_CURRENT_CORPUS",
        "FINITE_ZR_PRIOR_ACQUISITION_STARTED_NONCLAIM",
        "VAL1624_OVERALL",
    ],
    "1624_validation": ["VAL1624_OVERALL", "PASS"],
    "1624_next": [
        "1625-Y5-R2FR-finite-ZR-prior-row-builder-and-arena-projection-schema.md",
        "runner that refuses claims",
    ],
    "1624_acquisition": ["ACQ1624_0_ZR", "ACQ1624_7_runner_policy"],
    "1624_claim_gate": ["CG1624_3_finite_priors", "BLOCKED"],
    "1624_decision": ["NEXT_1625_FINITE_ZR_PRIOR_ROW_BUILDER", "FINITE_ZR_PRIOR_ACQUISITION_STARTED_NONCLAIM"],
    "1262_prior_requirements": ["PRIOR1262_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1264_source_requirements": ["FZR1264_0_ZR", "MISSING_SOURCE_BACKED_ROW"],
    "1265_runner_schema": ["BR1265_1_finite_qRhat", "WAITING_FOR_LIVE_ROWS"],
    "1563_fallback_ledger": ["FALL1563_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1564_intake_status": ["NO_LIVE_RAW_ROWS", "NO_ACCEPTED_ROWS"],
    "1565_source_intake": ["STRICT_REQUIREMENTS_STAGED_NONCLAIM", "NO_ACCEPTED_ROWS"],
    "1566_validator_rules": ["RULE1566_1_no_missing_markers", "hard_reject"],
    "1566_validator_summary": ["NO_ACCEPTED_SOURCE_READY_ROWS", "DOCS_TEMPLATES_REJECTED_AS_EXPECTED"],
    "1623_prior_rows": ["FZP1623_0_ZR", "MISSING_ARENA_PROJECTION"],
    "1262_countermodel": ["CM1262_1_vertical_metric_exists", "even representative variables can carry energy"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1625_SOURCE_REGISTER.csv"
PRIOR_ROW_BUILDER = OUT / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"
ARENA_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1625_ARENA_PROJECTION_SCHEMA.csv"
INTAKE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1625_LIVE_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"
RUNNER_GATES = OUT / "P8_Y5_PARENT_QLOC_1625_RUNNER_REFUSAL_GATES.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1625_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1625_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1625_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1625_VALIDATION.csv"

RAB_DOC_PRIOR_BUILDER = RAB_DOCS / "ZR1625_FINITE_ZR_PRIOR_ROW_BUILDER_NONCLAIM.csv"
RAB_DOC_ARENA_SCHEMA = RAB_DOCS / "ZR1625_ARENA_PROJECTION_SCHEMA_NONCLAIM.csv"
RAB_DOC_INTAKE_TEMPLATE = RAB_DOCS / "ZR1625_LIVE_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"
RAB_DOC_RUNNER_GATES = RAB_DOCS / "ZR1625_RUNNER_REFUSAL_GATES_NONCLAIM.csv"

COPY_TARGETS = {
    PRIOR_ROW_BUILDER: [
        QUARANTINE / "FINITE_ZR_PRIOR_ROW_BUILDER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_ZR_prior_row_builder_nonclaim_1625.csv",
        RAB_DOC_PRIOR_BUILDER,
    ],
    ARENA_SCHEMA: [
        QUARANTINE / "ARENA_PROJECTION_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_arena_projection_schema_nonclaim_1625.csv",
        RAB_DOC_ARENA_SCHEMA,
    ],
    INTAKE_TEMPLATE: [
        QUARANTINE / "LIVE_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_live_source_row_template_nonclaim_1625.csv",
        RAB_DOC_INTAKE_TEMPLATE,
    ],
    RUNNER_GATES: [
        QUARANTINE / "RUNNER_REFUSAL_GATES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_gates_nonclaim_1625.csv",
        RAB_DOC_RUNNER_GATES,
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1625.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1625.csv",
    ],
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def file_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def all_needles_found(source_id: str) -> bool:
    text = file_text(SOURCE_FILES[source_id])
    return all(needle in text for needle in NEEDLES[source_id])


def ensure_dirs() -> None:
    for directory in [OUT, INPUT_1625, BRANCH_RESIDUALS, RAB_DOCS]:
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_str(value: Any) -> str:
    return str(value).strip().lower()


def is_false(value: Any) -> bool:
    return bool_str(value) == "false"


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": rel(path),
                "exists": path.exists(),
                "required_needles": "; ".join(NEEDLES[source_id]),
                "needles_found": all_needles_found(source_id),
                "role": "1625 finite Z_R row-builder provenance",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def prior_row_builder_rows() -> list[dict[str, Any]]:
    base = [
        (
            "PB1625_0_ZR",
            "Z_R",
            "kinetic residue / vertical-gradient coefficient",
            "theorem_zero_parent_signed; numeric_source_value; bounded_prior_interval",
            "declared kinetic normalization units",
            "kinetic normalization must state whether Z_R multiplies grad R_AB grad R_AB, q_Rhat, or an equivalent normalized mode",
            "feeds q_Rhat amplitude and ell_R=sqrt(Z_R/M_R^2) if M_R^2 exists",
        ),
        (
            "PB1625_1_MR2",
            "M_R^2",
            "mass gap / screening range owner",
            "parent Hessian eigenvalue; sourced screening-scale value; bounded range prior",
            "mass^2 or length^-2 after declared normalization",
            "normalization must state whether M_R^2 is a Hessian eigenvalue, inverse range, or fitted suppression scale",
            "defines ell_R=sqrt(Z_R/M_R^2) or equivalent massive response scale",
        ),
        (
            "PB1625_2_JR",
            "J_R",
            "matter/source coupling to the R_AB residual channel",
            "matter-descent zero theorem; numeric source-current coefficient; bounded source-current prior",
            "source-current units compatible with the normalized R_AB equation",
            "normalization must specify source convention and matter variable used",
            "sets finite q_Rhat amplitude and local-source leakage if not zero",
        ),
        (
            "PB1625_3_BR",
            "B_R",
            "boundary/defect/readout tail coefficient",
            "boundary no-flux theorem; numeric boundary-flux coefficient; bounded exterior-tail prior",
            "boundary flux or alpha-tail units after stated projection",
            "normalization must specify boundary surface, falloff convention, and exterior residual owner",
            "controls Pi_R^n or boundary hair leaking into local tests",
        ),
    ]
    rows = []
    required_columns = (
        "coefficient_symbol; coefficient_value; coefficient_units; normalization_convention; "
        "parent_action_block; source_path; source_anchor; arena_projection; evidence_type"
    )
    for row_id, symbol, role, evidence, units, normalization, relation in base:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "prior_builder_id": row_id,
                "coefficient_symbol": symbol,
                "coefficient_role": role,
                "allowed_evidence_modes": evidence,
                "live_row_required_columns": required_columns,
                "required_units": units,
                "normalization_rule": normalization,
                "source_requirement": "local source_path must exist and source_anchor must appear in that source",
                "arena_projection_required": "tau_R10, tau_PPN, tau_clock, tau_orbital, or all must be supplied before scoring",
                "observable_relation": relation,
                "current_status": "MISSING_SOURCE_BACKED_INPUT",
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def arena_projection_rows() -> list[dict[str, Any]]:
    definitions = [
        (
            "AP1625_0_tau_R10",
            "tau_R10",
            "R10 / short-range fifth-force bound",
            "Z_R, M_R^2, J_R, B_R",
            "alpha_R(lambda) or an explicitly equivalent residual-force amplitude",
            "must produce lambda, alpha_predicted, alpha_bound, and source-backed bound row before any pass/fail comparison",
        ),
        (
            "AP1625_1_tau_PPN",
            "tau_PPN",
            "PPN / weak-field local-GR recovery",
            "Z_R, M_R^2, J_R, B_R plus metric-response normalization",
            "gamma-1, beta-1, preferred-frame/source residual vector, or theorem-zero equivalent",
            "must map finite residuals into PPN observables and compare to explicit limits, not just say auxiliary",
        ),
        (
            "AP1625_2_tau_clock",
            "tau_clock",
            "clock / local time-drift channel",
            "Z_R, M_R^2, J_R, B_R plus clock-readout coupling",
            "Gdot/G, frequency drift, redshift residual, or clock-comparison amplitude",
            "must state units, cadence, observable, and reference bound before scoring",
        ),
        (
            "AP1625_3_tau_orbital",
            "tau_orbital",
            "orbital / ephemeris / binary-dynamics channel",
            "Z_R, M_R^2, J_R, B_R plus orbital response kernel",
            "perihelion drift, range residual, GM drift, inverse-square residual, or binary timing residual",
            "must state target system, observable, units, and acceptance ceiling before scoring",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "projection_symbol": symbol,
            "arena": arena,
            "required_input_coefficients": inputs,
            "observable_output": output,
            "acceptance_gate": gate,
            "current_status": "MISSING_ARENA_PROJECTION",
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, symbol, arena, inputs, output, gate in definitions
    ]


def intake_template_rows() -> list[dict[str, Any]]:
    rows = []
    for builder in prior_row_builder_rows():
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "template_row_id": builder["prior_builder_id"].replace("PB", "TEMPLATE"),
                "row_type": "coefficient_source_row_template_not_live",
                "coefficient_symbol": builder["coefficient_symbol"],
                "evidence_type": "MISSING_THEOREM_ZERO_OR_NUMERIC_SOURCE_OR_PRIOR_INTERVAL",
                "coefficient_value": "MISSING_NUMERIC_VALUE",
                "prior_lower": "MISSING_PRIOR_LOWER",
                "prior_upper": "MISSING_PRIOR_UPPER",
                "coefficient_units": "MISSING_UNITS",
                "normalization_convention": "MISSING_NORMALIZATION_CONVENTION",
                "parent_action_block": "MISSING_PARENT_ACTION_BLOCK",
                "source_path": "MISSING_LOCAL_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "arena_projection": "MISSING_ARENA_PROJECTION",
                "rejection_reason": "template row only; contains MISSING markers and cannot be scored",
                "current_status": "TEMPLATE_REJECTED_NONCLAIM",
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    for projection in arena_projection_rows():
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "template_row_id": projection["projection_id"].replace("AP", "TEMPLATE"),
                "row_type": "arena_projection_row_template_not_live",
                "coefficient_symbol": projection["projection_symbol"],
                "evidence_type": "MISSING_NUMERIC_ARENA_KERNEL",
                "coefficient_value": "MISSING_PROJECTION_KERNEL",
                "prior_lower": "MISSING_ACCEPTANCE_LOWER_OR_NOT_APPLICABLE",
                "prior_upper": "MISSING_ACCEPTANCE_UPPER_OR_BOUND",
                "coefficient_units": "MISSING_OBSERVABLE_UNITS",
                "normalization_convention": "MISSING_PROJECTION_NORMALIZATION",
                "parent_action_block": "MISSING_PARENT_TO_ARENA_MAP",
                "source_path": "MISSING_LOCAL_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "arena_projection": projection["arena"],
                "rejection_reason": "template row only; arena relation has no numeric/source-backed kernel",
                "current_status": "TEMPLATE_REJECTED_NONCLAIM",
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_gate_rows() -> list[dict[str, Any]]:
    gates = [
        (
            "RG1625_0_docs_not_live",
            "rows under source-intake/rab-sector/docs are templates, not live evidence",
            "DOCS_TEMPLATE_NOT_LIVE_INTAKE",
            "hard_reject",
        ),
        (
            "RG1625_1_required_columns",
            "live rows must include coefficient_symbol, coefficient_value, coefficient_units, normalization_convention, parent_action_block, source_path, source_anchor, arena_projection, and evidence_type",
            "MISSING_REQUIRED_COLUMNS_OR_EMPTY_FIELD",
            "hard_reject",
        ),
        (
            "RG1625_2_no_missing_markers",
            "any field containing MISSING, TBD, PLACEHOLDER, or TEMPLATE rejects the row",
            "PLACEHOLDER_MARKER_PRESENT",
            "hard_reject",
        ),
        (
            "RG1625_3_numeric_or_theorem_zero",
            "row must contain a numeric value/prior interval or a parent-signed theorem-zero certificate",
            "NO_NUMERIC_OR_THEOREM_ZERO_EVIDENCE",
            "hard_reject",
        ),
        (
            "RG1625_4_units_and_normalization",
            "units and normalization must state the parent variable and observable convention",
            "UNITS_OR_NORMALIZATION_MISSING",
            "hard_reject",
        ),
        (
            "RG1625_5_source_path_anchor",
            "source_path must resolve locally and source_anchor must appear in its text",
            "SOURCE_PATH_OR_ANCHOR_INVALID",
            "hard_reject",
        ),
        (
            "RG1625_6_arena_projection",
            "coefficient rows do not score until mapped into R10, PPN, clock, orbital, or all",
            "ARENA_PROJECTION_MISSING",
            "hard_reject",
        ),
        (
            "RG1625_7_no_claim_flags",
            "valid_for_claim=true, claim_allowed=true, score_ready=true, or valid_prediction_row=true rejects private rows",
            "CLAIM_FLAG_TRUE_REJECTED",
            "hard_reject",
        ),
        (
            "RG1625_8_local_GR_lock",
            "local GR/Newton recovery remains blocked until either theorem-zero or finite-prior arena comparisons pass",
            "LOCAL_GR_CLAIM_BLOCKED",
            "hard_reject",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "rule": rule,
            "failure_status": failure_status,
            "severity": severity,
            "runner_action": "refuse scoring and emit blocker ledger",
            "current_status": "ACTIVE_HARD_REJECT",
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, rule, failure_status, severity in gates
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        (
            "CG1625_0_finite_priors",
            "finite Z_R/M_R^2/J_R/B_R priors claim-ready",
            "BLOCKED",
            "row builder exists, but no live source-backed coefficient rows are accepted",
        ),
        (
            "CG1625_1_R10",
            "R10 alpha(lambda) comparison",
            "BLOCKED",
            "tau_R10 kernel and alpha bound/source rows are not connected to live coefficients",
        ),
        (
            "CG1625_2_PPN",
            "PPN/local-GR residual vector",
            "BLOCKED",
            "tau_PPN map is schema-only and finite residuals are not numerically bounded",
        ),
        (
            "CG1625_3_clock",
            "clock/time-drift comparison",
            "BLOCKED",
            "tau_clock kernel lacks source-backed coefficient and observable bound",
        ),
        (
            "CG1625_4_orbital",
            "orbital/ephemeris comparison",
            "BLOCKED",
            "tau_orbital kernel lacks source-backed coefficient and observable bound",
        ),
        (
            "CG1625_5_local_GR",
            "derived local GR/Newton recovery",
            "BLOCKED",
            "neither theorem-zero nor finite-prior comparison branch is closed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1625_0_schema",
            "decision": "FINITE_ZR_PRIOR_ROW_BUILDER_STAGED_NONCLAIM",
            "reason": "the local branch now has explicit source-row requirements for Z_R, M_R^2, J_R, and B_R",
            "next_action": "use the row builder only as a validator target, not as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1625_1_arena",
            "decision": "ARENA_PROJECTION_SCHEMA_STAGED_NONCLAIM",
            "reason": "R10, PPN, clock, and orbital tests now have named tau projections with required observables",
            "next_action": "hunt for numeric/source-backed kernels or write blocker rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1625_2_runner",
            "decision": "RUNNER_REFUSES_PLACEHOLDERS_AND_DOC_TEMPLATES",
            "reason": "any MISSING/template/docs-only row is hard rejected before scoring",
            "next_action": "scan raw/accepted intake and corpus for a first live candidate row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1625_3_next",
            "decision": "NEXT_1626_LIVE_SOURCE_ROW_VALIDATOR_AND_FIRST_PRIOR_HUNT",
            "reason": "the schema is now clear enough to start looking for real inputs without smuggling claims",
            "next_action": "build validator/hunt runner for live source rows and blocker ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md",
            "script": "scripts/Y5_R2FR_finite_ZR_live_source_row_validator_and_first_prior_hunt.py",
            "objective": "scan raw/accepted R_AB intake plus current corpus for source-backed finite Z_R, M_R^2, J_R, B_R, tau_R10, tau_PPN, tau_clock, and tau_orbital rows; accept none unless 1625 gates pass",
            "success_condition": "either at least one live row passes strict source/unit/normalization/arena checks as nonclaim, or a precise blocker ledger identifies the missing coefficient source",
            "do_not": "do not score templates, do not treat docs rows as live data, do not reopen theorem-zero, do not claim local GR/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def row_has_true_claim_flag(row: dict[str, Any]) -> bool:
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
        if field in row and bool_str(row[field]) == "true":
            return True
    return False


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
    except Exception:
        return False
    return True


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        PRIOR_ROW_BUILDER,
        ARENA_SCHEMA,
        INTAKE_TEMPLATE,
        RUNNER_GATES,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source_id, source in SOURCE_FILES.items():
        if source.exists():
            target = INPUT_1625 / f"{source_id}{source.suffix}"
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    prior_rows = read_csv(PRIOR_ROW_BUILDER)
    arena_rows = read_csv(ARENA_SCHEMA)
    template_rows = read_csv(INTAKE_TEMPLATE)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_generated_rows: list[dict[str, Any]] = []
    for path in paths:
        all_generated_rows.extend(read_csv(path))

    expected_coefficients = {"Z_R", "M_R^2", "J_R", "B_R"}
    expected_projections = {"tau_R10", "tau_PPN", "tau_clock", "tau_orbital"}
    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    builder_coefficients = {row["coefficient_symbol"] for row in prior_rows}
    arena_symbols = {row["projection_symbol"] for row in arena_rows}
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_generated_rows)
    template_rejected = all(
        "MISSING" in " ".join(str(value) for value in row.values()) and row["current_status"] == "TEMPLATE_REJECTED_NONCLAIM"
        for row in template_rows
    )
    hard_rejects = all(row["current_status"] == "ACTIVE_HARD_REJECT" and row["severity"] == "hard_reject" for row in runner_rows)
    runner_contains_locks = all(
        needle in file_text(RUNNER_GATES)
        for needle in ["DOCS_TEMPLATE_NOT_LIVE_INTAKE", "PLACEHOLDER_MARKER_PRESENT", "LOCAL_GR_CLAIM_BLOCKED"]
    )
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    docs_copied = all(path.exists() for path in [RAB_DOC_PRIOR_BUILDER, RAB_DOC_ARENA_SCHEMA, RAB_DOC_INTAKE_TEMPLATE, RAB_DOC_RUNNER_GATES])
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1625*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1625_0_sources_exist", source_ok, "all cited 1625 local source paths exist"),
        ("VAL1625_1_needles_found", needles_ok, "all required 1625 source needles found"),
        ("VAL1625_2_builder_coefficients", builder_coefficients == expected_coefficients, "Z_R, M_R^2, J_R, B_R builder rows present"),
        ("VAL1625_3_arena_symbols", arena_symbols == expected_projections, "tau_R10, tau_PPN, tau_clock, tau_orbital projection rows present"),
        ("VAL1625_4_nonclaim_flags", nonclaim_ok, "all generated 1625 rows remain nonclaim/non-score-ready"),
        ("VAL1625_5_template_rejected", template_rejected, "template rows contain MISSING markers and are explicitly rejected"),
        ("VAL1625_6_runner_hard_rejects", hard_rejects, "all runner gates are active hard rejects"),
        ("VAL1625_7_runner_locks", runner_contains_locks, "runner refuses docs templates, placeholders, and local-GR claims"),
        ("VAL1625_8_claim_gates_closed", claim_closed, "all claim gates are blocked"),
        (
            "VAL1625_9_decision_next",
            "NEXT_1626_LIVE_SOURCE_ROW_VALIDATOR_AND_FIRST_PRIOR_HUNT" in decision_text,
            "decision selects live source row validator and first prior hunt next",
        ),
        (
            "VAL1625_10_next_target_selected",
            "1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md" in next_text,
            "next target selected",
        ),
        ("VAL1625_11_docs_copied", docs_copied, "RAB docs templates copied as nonclaim files"),
        ("VAL1625_12_branch_copies", branch_copies, "branch/quarantine nonclaim copies exist"),
        ("VAL1625_13_csv_parse", csv_ok, "all generated 1625 CSVs parse"),
        ("VAL1625_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1625_15_formalization_untouched", formalization_clean, "no 1625 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1625_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1625 finite Z_R prior row builder and arena projection schema validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    prior_rows = read_csv(PRIOR_ROW_BUILDER)
    arena_rows = read_csv(ARENA_SCHEMA)
    template_rows = read_csv(INTAKE_TEMPLATE)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1625 — Finite `Z_R` Prior Row Builder And Arena Projection Schema

## Status

Private checkpoint. This does **not** claim local GR/Newton recovery, R10, PPN, clock, or orbital success. It turns the finite-residual route into a strict source-row contract.

## Why This Exists

`1624` ended the current primitive-constructor loop: the motion/time/space primitive route does not yet derive the parent object language or the no-vertical-metric theorem. The honest next move is therefore finite-prior plumbing: if `Z_R`, `M_R^2`, `J_R`, or `B_R` are nonzero, the branch must say how large they are, where that number came from, and how it projects into real tests.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Finite Prior Row Builder

{markdown_table(prior_rows, ["prior_builder_id", "coefficient_symbol", "coefficient_role", "required_units", "current_status"])}

## Arena Projection Schema

{markdown_table(arena_rows, ["projection_id", "projection_symbol", "arena", "observable_output", "current_status"])}

## Nonclaim Intake Template

These rows are deliberately invalid as evidence: they contain `MISSING` markers so the runner refuses them.

{markdown_table(template_rows, ["template_row_id", "row_type", "coefficient_symbol", "current_status", "rejection_reason"])}

## Runner Refusal Gates

{markdown_table(runner_rows, ["gate_id", "failure_status", "severity", "current_status"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decision, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        PRIOR_ROW_BUILDER: prior_row_builder_rows(),
        ARENA_SCHEMA: arena_projection_rows(),
        INTAKE_TEMPLATE: intake_template_rows(),
        RUNNER_GATES: runner_gate_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
