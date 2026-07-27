from __future__ import annotations

import csv
import math
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_DELTA_REF_Q_SOURCE_STRICT_PROVENANCE_RUNNER_2452"
CHECKPOINT_ID = "2452"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2452-Y5-R2FR-Delta-ref-q-source-strict-provenance-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2452_SOURCE_REGISTER.csv",
    "strict_schema": OUT / "P8_Y5_PARENT_QLOC_2452_STRICT_INPUT_SCHEMA.csv",
    "candidate_inputs": OUT / "P8_Y5_PARENT_QLOC_2452_CANDIDATE_INPUT_TEMPLATE.csv",
    "strict_runner": OUT / "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
    "refusal_ledger": OUT / "P8_Y5_PARENT_QLOC_2452_REFUSAL_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2452_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2452_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2452_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2452_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2452_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_runner": QUEUE / "JR2452_DELTA_REF_Q_SOURCE_STRICT_PROVENANCE_RUNNER_NONCLAIM.csv",
    "queue_schema": QUEUE / "JR2452_DELTA_REF_Q_SOURCE_STRICT_SCHEMA_NONCLAIM.csv",
    "local_runner": LOCAL_BOUNDS / "Delta_ref_q_source_strict_runner_2452_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2452_00_2451_doc",
        "source_path": ROOT / "2451-Y5-R2FR-Bref-fixed-branch-selector-or-Delta-ref-q-source-provenance-pack.md",
        "needles": ["NEXT2451_0_selected", "DCP2451_0_partial_q_derivative", "DCR2451_0_schema_ready", "VAL2451_OVERALL"],
        "role": "2451 handoff selecting a strict q/source provenance runner",
    },
    {
        "source_id": "SRC2452_01_2451_provenance",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_DELTA_REF_Q_SOURCE_PROVENANCE_PACK.csv",
        "needles": ["DCP2451_0_partial_q_derivative", "DCP2451_1_partial_source_derivative", "DCP2451_5_component_bound"],
        "role": "live q/source Delta_ref provenance requirements",
    },
    {
        "source_id": "SRC2452_02_2451_readiness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_PROVENANCE_RUNNER_READINESS.csv",
        "needles": ["DCR2451_0_schema_ready", "DCR2451_1_values_ready", "DCR2451_2_no_silent_zero"],
        "role": "schema-ready but value-blocked runner state",
    },
    {
        "source_id": "SRC2452_03_2451_claim_gates",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_CLAIM_GATES.csv",
        "needles": ["CG2451_0_fixed_branch_selector", "CG2451_2_q_source_component_score", "BLOCKED"],
        "role": "current claim gates that must remain blocked",
    },
    {
        "source_id": "SRC2452_04_2451_selector",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_BREF_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
        "needles": ["FBS2451_8_verdict", "FAIL_CURRENT_CLAIM", "parent-owned Sigma_ref"],
        "role": "failed current fixed-branch selector theorem",
    },
    {
        "source_id": "SRC2452_05_2451_parent_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_PARENT_SELECTOR_CONTRACT.csv",
        "needles": ["FBC2451_0_selector_function", "FBC2451_6_N_E_sidecar", "MISSING_PARENT"],
        "role": "future parent selector contract slots",
    },
    {
        "source_id": "SRC2452_06_R10_runner_precedent",
        "source_path": ROOT / "1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md",
        "needles": ["THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_TRUE", "Strict Provenance Runner", "V1000_SUMMARY"],
        "role": "older source-only strict runner precedent",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "role": source["role"],
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing_needles),
                "source_pass": truth(path.exists() and not missing_needles),
            }
        )
    return rows


def strict_schema_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "schema_id": "SIS2452_0_partial_q_Delta_ref",
            "field": "partial_q_Delta_ref",
            "required_input": "finite numeric derivative or theorem_zero_q=True with theorem_zero_authority=PARENT_SIGNED_TRUE",
            "units_requirement": "partial_q_units and Delta_ref_units explicit",
            "source_requirement": "source_path exists and equation_ref identifies parent equation/component certificate",
            "rejects": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO; closure-zero; notation-zero",
        },
        {
            "schema_id": "SIS2452_1_Delta_q_scale",
            "field": "Delta_q_scale",
            "required_input": "finite positive q-variation scale",
            "units_requirement": "Delta_q_scale_units explicit and same-frame",
            "source_requirement": "q parameter definition and extraction path required",
            "rejects": "unity placeholder; chosen-to-shrink residual; MISSING_Q_SOURCE_SCALE",
        },
        {
            "schema_id": "SIS2452_2_partial_source_Delta_ref",
            "field": "partial_source_Delta_ref",
            "required_input": "finite numeric derivative or theorem_zero_source=True with theorem_zero_authority=PARENT_SIGNED_TRUE",
            "units_requirement": "partial_source_units and Delta_ref_units explicit",
            "source_requirement": "source_path exists and equation_ref identifies parent equation/component certificate",
            "rejects": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO; closure-zero; notation-zero",
        },
        {
            "schema_id": "SIS2452_3_Delta_source_scale",
            "field": "Delta_source_scale",
            "required_input": "finite positive source-variation scale",
            "units_requirement": "Delta_source_scale_units explicit and same-frame",
            "source_requirement": "source parameter definition and extraction path required",
            "rejects": "unity placeholder; chosen-to-shrink residual; MISSING_Q_SOURCE_SCALE",
        },
        {
            "schema_id": "SIS2452_4_Bref_rule",
            "field": "B_ref_rule",
            "required_input": "fixed parent-owned formula for B_ref before q/source/readout",
            "units_requirement": "frame and counterterm convention declared",
            "source_requirement": "parent selector equation or finite provenance source path",
            "rejects": "hidden observed-GM labels; source labels; post-fit branch selection",
        },
        {
            "schema_id": "SIS2452_5_N_E",
            "field": "N_E",
            "required_input": "finite positive same-frame Hamiltonian/source normalization",
            "units_requirement": "N_E_units and denominator_origin explicit",
            "source_requirement": "definition path and equation_ref required",
            "rejects": "orbital-GM import; fitted denominator; MISSING_SAME_FRAME_N_E",
        },
        {
            "schema_id": "SIS2452_6_theorem_zero_authority",
            "field": "theorem_zero_authority",
            "required_input": "PARENT_SIGNED_TRUE if either q/source theorem_zero switch is True",
            "units_requirement": "units still recorded for zeroed derivative slot",
            "source_requirement": "parent theorem path, selector equation, and component certificate",
            "rejects": "zero-by-closure; boundary-projector silence; desire for local-GR pass",
        },
        {
            "schema_id": "SIS2452_7_no_cancellation_guard",
            "field": "no_cancellation_guard",
            "required_input": "ABS_COMPONENT_SUM_NO_SIGN_CANCELLATION",
            "units_requirement": "(abs(partial_q*Delta_q)+abs(partial_source*Delta_source))/N_E",
            "source_requirement": "no sign cancellation credit is allowed in local residual gate",
            "rejects": "opposite-sign cancellation; tuned cancellation; branch cancellation",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def live_candidate_rows() -> list[dict[str, Any]]:
    provenance_path = OUTPUTS["source_register"].parent / "P8_Y5_PARENT_QLOC_2451_DELTA_REF_Q_SOURCE_PROVENANCE_PACK.csv"
    live_rows = read_csv(provenance_path)
    rows: list[dict[str, Any]] = []
    for live in live_rows:
        provenance_id = live.get("provenance_id", "UNKNOWN")
        if provenance_id not in {
            "DCP2451_0_partial_q_derivative",
            "DCP2451_1_partial_source_derivative",
            "DCP2451_5_component_bound",
        }:
            continue
        component_kind = "combined"
        if "partial_q" in provenance_id:
            component_kind = "q"
        elif "partial_source" in provenance_id:
            component_kind = "source"
        rows.append(
            {
                **metadata(),
                "candidate_id": f"CIR2452_live_{provenance_id}",
                "purpose": f"live 2451 row import: {live.get('coefficient', '')}",
                "origin_row": provenance_id,
                "component_kind": component_kind,
                "target": live.get("target_row", "Delta_ref_q_source_component_over_N_E"),
                "formula": "(abs(partial_q_Delta_ref*Delta_q_scale)+abs(partial_source_Delta_ref*Delta_source_scale))/N_E",
                "q_parameter": "MISSING_Q_PARAMETER",
                "partial_q_Delta_ref": live.get("current_value", "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO") if component_kind == "q" else "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO",
                "partial_q_units": "MISSING_PARTIAL_Q_UNITS",
                "Delta_q_scale": "MISSING_Q_SOURCE_SCALE",
                "Delta_q_scale_units": "MISSING_DELTA_Q_SCALE_UNITS",
                "source_parameter": "MISSING_SOURCE_PARAMETER",
                "partial_source_Delta_ref": live.get("current_value", "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO") if component_kind == "source" else "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO",
                "partial_source_units": "MISSING_PARTIAL_SOURCE_UNITS",
                "Delta_source_scale": "MISSING_Q_SOURCE_SCALE",
                "Delta_source_scale_units": "MISSING_DELTA_SOURCE_SCALE_UNITS",
                "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
                "N_E": "MISSING_SAME_FRAME_N_E",
                "N_E_units": "MISSING_N_E_UNITS",
                "denominator_origin": "MISSING_DENOMINATOR_ORIGIN",
                "B_ref_rule": "MISSING_PARENT_BREF_RULE",
                "fixed_branch_id": "MISSING_FIXED_BRANCH_ID",
                "source_path": "MISSING_SOURCE_FILE",
                "equation_ref": "MISSING_EQUATION_REF",
                "theorem_zero_q": "False",
                "theorem_zero_source": "False",
                "theorem_zero_authority": "MISSING_PARENT_SIGNATURE",
                "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
                "row_class": "live_placeholder",
            }
        )
    return rows


def adversarial_candidate_rows() -> list[dict[str, Any]]:
    doc_path = str(ROOT / "2451-Y5-R2FR-Bref-fixed-branch-selector-or-Delta-ref-q-source-provenance-pack.md")
    base = {
        **metadata(),
        "origin_row": "2452_adversarial_policy_test",
        "component_kind": "combined",
        "target": "Delta_ref_q_source_component_over_N_E",
        "formula": "(abs(partial_q_Delta_ref*Delta_q_scale)+abs(partial_source_Delta_ref*Delta_source_scale))/N_E",
        "q_parameter": "q_ref",
        "partial_q_Delta_ref": "2.5",
        "partial_q_units": "Delta_ref/q_unit",
        "Delta_q_scale": "0.20",
        "Delta_q_scale_units": "q_unit",
        "source_parameter": "source_ref",
        "partial_source_Delta_ref": "1.5",
        "partial_source_units": "Delta_ref/source_unit",
        "Delta_source_scale": "0.10",
        "Delta_source_scale_units": "source_unit",
        "Delta_ref_units": "internal_energy_like",
        "N_E": "10.0",
        "N_E_units": "internal_energy_like",
        "denominator_origin": "PARENT_SAME_FRAME_N_E_SMOKE_ONLY",
        "B_ref_rule": "parent_selector_fixed_before_readout_smoke_only",
        "fixed_branch_id": "Sigma_ref_smoke_only",
        "source_path": doc_path,
        "equation_ref": "SMOKE_ROW_NOT_PHYSICS",
        "theorem_zero_q": "False",
        "theorem_zero_source": "False",
        "theorem_zero_authority": "NOT_USED",
        "no_cancellation_guard": "ABS_COMPONENT_SUM_NO_SIGN_CANCELLATION",
        "row_class": "adversarial_or_smoke",
    }
    return [
        {
            **base,
            "candidate_id": "CIR2452_3_theorem_zero_without_parent_signature",
            "purpose": "prove zero switches are rejected without parent signature",
            "partial_q_Delta_ref": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO",
            "theorem_zero_q": "True",
            "theorem_zero_authority": "MISSING_PARENT_SIGNATURE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **base,
            "candidate_id": "CIR2452_4_hidden_orbital_GM_import",
            "purpose": "prove hidden orbital-GM denominator import is rejected",
            "N_E": "1.0",
            "denominator_origin": "ORBITAL_GM_IMPORTED_FROM_OBSERVED_FIT",
            "B_ref_rule": "B_ref fixed by observed GM calibration",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **base,
            "candidate_id": "CIR2452_5_cancellation_guard_missing",
            "purpose": "prove sign-cancellation rows are rejected",
            "no_cancellation_guard": "SIGNED_SUM_CANCELLATION_ALLOWED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **base,
            "candidate_id": "CIR2452_6_numeric_smoke_nonclaim",
            "purpose": "prove the numeric absolute-value path computes while staying nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def candidate_input_rows() -> list[dict[str, Any]]:
    return [*live_candidate_rows(), *adversarial_candidate_rows()]


def is_missing(value: Any) -> bool:
    stripped = str(value).strip()
    return not stripped or stripped.upper().startswith("MISSING") or stripped.upper().startswith("SCHEMA_ONLY")


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def finite_float(value: Any) -> tuple[bool, float | None]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


def source_exists(value: str) -> bool:
    if is_missing(value):
        return False
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / value
    return path.exists()


def derivative_value(row: dict[str, Any], derivative_field: str, zero_field: str) -> tuple[bool, float | None, list[str]]:
    reasons: list[str] = []
    numeric_ok, numeric_value = finite_float(row.get(derivative_field, ""))
    theorem_zero = is_true(row.get(zero_field, "False"))
    parent_signed = theorem_zero and row.get("theorem_zero_authority") == "PARENT_SIGNED_TRUE"
    if theorem_zero and not parent_signed:
        reasons.append(f"{zero_field.upper()}_REJECTED_WITHOUT_PARENT_SIGNED_TRUE")
    if numeric_ok:
        return True, numeric_value, reasons
    if parent_signed:
        return True, 0.0, reasons
    reasons.append(f"MISSING_NUMERIC_{derivative_field.upper()}_OR_PARENT_SIGNED_ZERO")
    return False, None, reasons


def positive_value(row: dict[str, Any], field: str) -> tuple[bool, float | None, list[str]]:
    numeric_ok, numeric_value = finite_float(row.get(field, ""))
    if not numeric_ok or numeric_value is None or numeric_value <= 0:
        return False, None, [f"MISSING_POSITIVE_{field.upper()}"]
    return True, numeric_value, []


def evaluate_candidate(row: dict[str, Any]) -> dict[str, Any]:
    data_reasons: list[str] = []
    q_ok, q_derivative, q_reasons = derivative_value(row, "partial_q_Delta_ref", "theorem_zero_q")
    source_ok, source_derivative, source_reasons = derivative_value(row, "partial_source_Delta_ref", "theorem_zero_source")
    data_reasons.extend(q_reasons)
    data_reasons.extend(source_reasons)

    q_scale_ok, q_scale, q_scale_reasons = positive_value(row, "Delta_q_scale")
    source_scale_ok, source_scale, source_scale_reasons = positive_value(row, "Delta_source_scale")
    n_e_ok, n_e, n_e_reasons = positive_value(row, "N_E")
    data_reasons.extend(q_scale_reasons)
    data_reasons.extend(source_scale_reasons)
    data_reasons.extend(n_e_reasons)

    for field in [
        "q_parameter",
        "partial_q_units",
        "Delta_q_scale_units",
        "source_parameter",
        "partial_source_units",
        "Delta_source_scale_units",
        "Delta_ref_units",
        "N_E_units",
        "denominator_origin",
        "fixed_branch_id",
        "equation_ref",
    ]:
        if is_missing(row.get(field, "")):
            data_reasons.append(f"MISSING_{field.upper()}")

    bref_rule = str(row.get("B_ref_rule", ""))
    if is_missing(bref_rule):
        data_reasons.append("MISSING_PARENT_BREF_RULE")
    forbidden_bref_tokens = ["observed", "calibration", "post_fit", "post-fit", "source label"]
    if not is_missing(bref_rule) and any(token in bref_rule.lower() for token in forbidden_bref_tokens):
        data_reasons.append("BREF_RULE_CONTAINS_FORBIDDEN_OBSERVED_OR_CALIBRATION_LABEL")

    denominator_origin = str(row.get("denominator_origin", ""))
    forbidden_denominator_tokens = ["orbital_gm", "observed_fit", "calibration", "fitted"]
    if any(token in denominator_origin.lower() for token in forbidden_denominator_tokens):
        data_reasons.append("DENOMINATOR_ORIGIN_FORBIDDEN_ORBITAL_GM_OR_FIT")

    if not source_exists(str(row.get("source_path", ""))):
        data_reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_COMPONENT_SUM_NO_SIGN_CANCELLATION":
        data_reasons.append("MISSING_NO_CANCELLATION_GUARD")

    unity_placeholder_fields = []
    for field, value in {
        "Delta_q_scale": q_scale,
        "Delta_source_scale": source_scale,
        "N_E": n_e,
    }.items():
        if value == 1.0 and is_missing(row.get("source_path", "")):
            unity_placeholder_fields.append(field)
    if unity_placeholder_fields:
        data_reasons.append("UNITY_PLACEHOLDER_WITHOUT_SOURCE:" + ",".join(unity_placeholder_fields))

    score_ready = not data_reasons and q_ok and source_ok and q_scale_ok and source_scale_ok and n_e_ok
    computed_ratio = "NOT_SCORED"
    if score_ready and q_derivative is not None and source_derivative is not None and q_scale is not None and source_scale is not None and n_e is not None:
        computed_ratio = f"{(abs(q_derivative * q_scale) + abs(source_derivative * source_scale)) / n_e:.16e}"

    claim_reasons: list[str] = []
    if not is_true(row.get("valid_for_claim", "False")):
        claim_reasons.append("VALID_FOR_CLAIM_FALSE_NONCLAIM_OR_SMOKE")

    component_row_allowed = score_ready and not claim_reasons
    if score_ready and claim_reasons:
        verdict = "SMOKE_COMPUTED_NONCLAIM"
    elif score_ready:
        verdict = "ACCEPTABLE_COMPONENT_INPUT_SCHEMA_PASSED"
    else:
        verdict = "REFUSED_CURRENT_ROW_MISSING_PROVENANCE_OR_PARENT_SELECTOR"

    return {
        **metadata(),
        "runner_id": row["candidate_id"].replace("CIR2452", "RUN2452"),
        "candidate_id": row["candidate_id"],
        "origin_row": row.get("origin_row", ""),
        "component_kind": row.get("component_kind", ""),
        "verdict": verdict,
        "score_ready": truth(score_ready),
        "component_row_allowed": truth(component_row_allowed),
        "downstream_claim_allowed": "False",
        "computed_abs_component_over_N_E": computed_ratio,
        "data_failure_reasons": ";".join(data_reasons) if data_reasons else "none",
        "claim_failure_reasons": ";".join(claim_reasons) if claim_reasons else "none",
        "acceptance_rule": "parent-signed theorem-zero or fully sourced finite numeric q/source component; no closure zero; no hidden GM; no cancellation credit",
    }


def strict_runner_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate_candidate(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run in runner:
        if run["verdict"] == "ACCEPTABLE_COMPONENT_INPUT_SCHEMA_PASSED":
            refusal = "not_refused_by_component_schema"
            required_exit = "downstream claim still needs residual envelope/local bound comparison"
        elif run["verdict"] == "SMOKE_COMPUTED_NONCLAIM":
            refusal = "computed_but_nonclaim_smoke"
            required_exit = "replace smoke row with real sourced coefficients and valid_for_claim=True"
        else:
            refusal = "refused"
            required_exit = "finite sourced coefficients or parent-signed theorem-zero selector"
        rows.append(
            {
                **metadata(),
                "refusal_id": run["runner_id"].replace("RUN2452", "REF2452"),
                "candidate_id": run["candidate_id"],
                "refusal": refusal,
                "why": run["data_failure_reasons"] if run["data_failure_reasons"] != "none" else run["claim_failure_reasons"],
                "required_exit": required_exit,
                "claim_allowed": "False",
            }
        )
    return rows


def claim_gate_rows(runner: list[dict[str, Any]]) -> list[dict[str, Any]]:
    live_rows_refused = all(
        row["verdict"] == "REFUSED_CURRENT_ROW_MISSING_PROVENANCE_OR_PARENT_SELECTOR"
        for row in runner
        if str(row["candidate_id"]).startswith("CIR2452_live_")
    )
    smoke_computed = any(row["candidate_id"] == "CIR2452_6_numeric_smoke_nonclaim" and row["verdict"] == "SMOKE_COMPUTED_NONCLAIM" for row in runner)
    rows = [
        {
            "gate_id": "GATE2452_0_live_Delta_ref_q_source_rows",
            "claim": "current 2451 Delta_ref q/source rows are usable",
            "gate_status": "BLOCKED",
            "reason": "live rows are placeholders and strict runner refuses them" if live_rows_refused else "unexpected live-row acceptance",
            "gate_pass": truth(False),
        },
        {
            "gate_id": "GATE2452_1_theorem_zero_switch",
            "claim": "q/source theorem-zero can be used without parent selector",
            "gate_status": "BLOCKED",
            "reason": "theorem-zero requires theorem_zero_authority=PARENT_SIGNED_TRUE",
            "gate_pass": truth(False),
        },
        {
            "gate_id": "GATE2452_2_numeric_path_smoke",
            "claim": "runner arithmetic path works",
            "gate_status": "SMOKE_ONLY",
            "reason": "numeric smoke computes but remains nonclaim" if smoke_computed else "numeric smoke did not compute",
            "gate_pass": truth(smoke_computed),
        },
        {
            "gate_id": "GATE2452_3_downstream_local_GR",
            "claim": "Delta_ref/RCS2446_0/S_Eq/local-GR branch passes",
            "gate_status": "BLOCKED",
            "reason": "component provenance is guarded but not supplied; downstream residual envelope remains open",
            "gate_pass": truth(False),
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2452_0_runner_installed",
            "decision": "install strict q/source provenance runner",
            "reason": "2451 made the required rows explicit but did not supply coefficients or a parent selector theorem",
            "effect": "future q/source rows can be tested without accidental promotion",
        },
        {
            "decision_id": "DEC2452_1_current_rows_refused",
            "decision": "keep current 2451 Delta_ref q/source component rows nonclaim",
            "reason": "missing derivative/scale/B_ref/N_E/source/equation evidence remains",
            "effect": "no Delta_ref, RCS2446_0, S_Eq, R10, PPN, or local-GR pass is claimed",
        },
        {
            "decision_id": "DEC2452_2_no_fake_zero",
            "decision": "zero-by-closure is rejected",
            "reason": "theorem-zero switches require a parent-signed selector or component certificate",
            "effect": "the route must be derived, not smuggled in as a plateau axiom",
        },
        {
            "decision_id": "DEC2452_3_next_parent_selector",
            "decision": "move to parent B_ref selector variational equation",
            "reason": "the strict runner is now in place; the next real physics gap is the owner equation for Sigma_ref/B_ref",
            "effect": "2453 should try the derivation first and only then stage finite coefficient rows",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2452_0_selected",
            "selection_status": "selected",
            "target_file": "2453-Y5-R2FR-parent-Bref-selector-variational-equation-or-finite-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_parent_Bref_selector_variational_equation_or_finite_coefficient_row_2453.py",
            "task": "derive a parent-owned Sigma_ref/B_ref selector equation that fixes B_ref before q/source/readout, or stage finite q/source coefficient rows through the 2452 strict runner",
            "acceptance_target": "parent selector theorem must satisfy no-marker, no-observed-GM, no-post-fit-source, same-frame N_E, and counterterm convention clauses; otherwise remain nonclaim",
            "guardrails": "do not claim Delta_ref/RCS2446_0/S_Eq/local-GR; do not edit formalization-workbench; do not push GitHub",
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_specs = [
        ("queue_runner", OUTPUTS["strict_runner"], COPY_TARGETS["queue_runner"]),
        ("queue_schema", OUTPUTS["strict_schema"], COPY_TARGETS["queue_schema"]),
        ("local_runner", OUTPUTS["strict_runner"], COPY_TARGETS["local_runner"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
                "notes": "nonclaim branch copy for future source intake",
            }
        )
    return rows


def formalization_marker_hits() -> list[str]:
    if not FORMALIZATION.exists():
        return []
    markers = ["2452-", "_2452", "2452_", "P8_Y5_PARENT_QLOC_2452", "P8_Y5_BRR545_2452"]
    hits: list[str] = []
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            if any(marker in filename for marker in markers):
                hits.append(str(Path(dirpath) / filename))
    return hits


def csv_parse_ok(path: Path) -> tuple[bool, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, repr(exc)
    return True, f"CSV parses with {len(rows)} rows"


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    runner = data["strict_runner"]
    live_rows = [row for row in runner if str(row["candidate_id"]).startswith("CIR2452_live_")]
    theorem_row = next((row for row in runner if row["candidate_id"] == "CIR2452_3_theorem_zero_without_parent_signature"), None)
    hidden_gm_row = next((row for row in runner if row["candidate_id"] == "CIR2452_4_hidden_orbital_GM_import"), None)
    cancellation_row = next((row for row in runner if row["candidate_id"] == "CIR2452_5_cancellation_guard_missing"), None)
    smoke_row = next((row for row in runner if row["candidate_id"] == "CIR2452_6_numeric_smoke_nonclaim"), None)
    source_ok = all(row["source_pass"] == "True" for row in data["source_register"])
    schema_fields = {row["field"] for row in data["strict_schema"]}
    required_fields = {
        "partial_q_Delta_ref",
        "Delta_q_scale",
        "partial_source_Delta_ref",
        "Delta_source_scale",
        "B_ref_rule",
        "N_E",
        "theorem_zero_authority",
        "no_cancellation_guard",
    }
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL2452_00_sources_exist",
            "status": "PASS" if source_ok else "FAIL",
            "notes": "all cited source paths exist and needles are present",
            "detail": "",
        },
        {
            "check_id": "VAL2452_01_schema_core_fields",
            "status": "PASS" if required_fields.issubset(schema_fields) else "FAIL",
            "notes": "strict schema covers q derivative, source derivative, scales, B_ref, N_E, theorem-zero, and no-cancellation",
            "detail": "",
        },
        {
            "check_id": "VAL2452_02_live_rows_refused",
            "status": "PASS" if live_rows and all(row["verdict"] == "REFUSED_CURRENT_ROW_MISSING_PROVENANCE_OR_PARENT_SELECTOR" for row in live_rows) else "FAIL",
            "notes": "current 2451 q/source rows are refused",
            "detail": "",
        },
        {
            "check_id": "VAL2452_03_theorem_zero_guard",
            "status": "PASS" if theorem_row and "THEOREM_ZERO_Q_REJECTED_WITHOUT_PARENT_SIGNED_TRUE" in theorem_row["data_failure_reasons"] else "FAIL",
            "notes": "theorem-zero switch is rejected without parent signature",
            "detail": "",
        },
        {
            "check_id": "VAL2452_04_hidden_GM_rejected",
            "status": "PASS" if hidden_gm_row and "DENOMINATOR_ORIGIN_FORBIDDEN_ORBITAL_GM_OR_FIT" in hidden_gm_row["data_failure_reasons"] else "FAIL",
            "notes": "hidden orbital-GM/fitted denominator route is rejected",
            "detail": "",
        },
        {
            "check_id": "VAL2452_05_cancellation_rejected",
            "status": "PASS" if cancellation_row and "MISSING_NO_CANCELLATION_GUARD" in cancellation_row["data_failure_reasons"] else "FAIL",
            "notes": "sign-cancellation route is rejected",
            "detail": "",
        },
        {
            "check_id": "VAL2452_06_numeric_smoke_computes_nonclaim",
            "status": "PASS" if smoke_row and smoke_row["verdict"] == "SMOKE_COMPUTED_NONCLAIM" and smoke_row["computed_abs_component_over_N_E"] != "NOT_SCORED" else "FAIL",
            "notes": "numeric arithmetic path computes but remains nonclaim",
            "detail": smoke_row["computed_abs_component_over_N_E"] if smoke_row else "",
        },
        {
            "check_id": "VAL2452_07_claim_gates_blocked",
            "status": "PASS" if all(row["claim_allowed"] == "False" for row in data["claim_gates"]) else "FAIL",
            "notes": "downstream Delta_ref/RCS2446_0/S_Eq/local-GR claims remain blocked",
            "detail": "",
        },
        {
            "check_id": "VAL2452_08_next_target_written",
            "status": "PASS" if data["next_target"] and data["next_target"][0]["route_id"] == "NEXT2452_0_selected" else "FAIL",
            "notes": "2453 parent selector target selected",
            "detail": "",
        },
        {
            "check_id": "VAL2452_09_branch_copies",
            "status": "PASS" if all(row["target_exists"] == "True" for row in data["branch_copies"]) else "FAIL",
            "notes": "strict runner/schema nonclaim copies exist",
            "detail": "",
        },
        {
            "check_id": "VAL2452_10_no_formalization_artifacts",
            "status": "PASS" if not formalization_marker_hits() else "FAIL",
            "notes": "no 2452 artifacts were written to formalization-workbench",
            "detail": ";".join(formalization_marker_hits()[:10]),
        },
    ]
    csv_outputs = [
        OUTPUTS["source_register"],
        OUTPUTS["strict_schema"],
        OUTPUTS["candidate_inputs"],
        OUTPUTS["strict_runner"],
        OUTPUTS["refusal_ledger"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decisions"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    for path in csv_outputs:
        ok, detail = csv_parse_ok(path)
        checks.append(
            {
                "check_id": f"VAL2452_CSV_{path.stem}",
                "status": "PASS" if ok else "FAIL",
                "notes": detail,
                "detail": str(path),
            }
        )
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL2452_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "notes": "2452 strict q/source provenance runner installed and claims remain blocked",
            "detail": "",
        }
    )
    return [{**metadata(), **row} for row in checks]


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2452 Y5 R2FR Delta-ref q/source Strict Provenance Runner

**Status:** strict q/source provenance runner installed; no Delta_ref, RCS2446_0, S_E^q, R10, PPN, or local-GR pass is claimed.

**Private reading:** 2452 does not solve the coupling. It makes the coupling hole harder to paper over. The only clean exits are now a parent-signed q/source zero theorem or fully sourced finite q/source coefficients.

## Source Register
{table(["source_id", "source_path", "role", "exists", "missing_needles", "source_pass"], data["source_register"])}

## Strict Input Schema
{table(["schema_id", "field", "required_input", "rejects"], data["strict_schema"])}

## Candidate Inputs
{table(["candidate_id", "purpose", "origin_row", "component_kind", "partial_q_Delta_ref", "Delta_q_scale", "partial_source_Delta_ref", "Delta_source_scale", "N_E", "B_ref_rule", "theorem_zero_q", "theorem_zero_source", "theorem_zero_authority", "no_cancellation_guard", "valid_for_claim"], data["candidate_inputs"])}

## Strict Provenance Runner
{table(["runner_id", "candidate_id", "verdict", "score_ready", "component_row_allowed", "downstream_claim_allowed", "computed_abs_component_over_N_E", "data_failure_reasons", "claim_failure_reasons"], data["strict_runner"])}

## Refusal Ledger
{table(["refusal_id", "candidate_id", "refusal", "why", "required_exit", "claim_allowed"], data["refusal_ledger"])}

## Claim Gates
{table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "reason", "effect"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "strict_schema": strict_schema_rows(),
    }
    data["candidate_inputs"] = candidate_input_rows()
    data["strict_runner"] = strict_runner_rows(data["candidate_inputs"])
    data["refusal_ledger"] = refusal_ledger_rows(data["strict_runner"])
    data["claim_gates"] = claim_gate_rows(data["strict_runner"])
    data["decisions"] = decision_rows()
    data["next_target"] = next_target_rows()

    for key in ["source_register", "strict_schema", "candidate_inputs", "strict_runner", "refusal_ledger", "claim_gates", "decisions", "next_target"]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()
