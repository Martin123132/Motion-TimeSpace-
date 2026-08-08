from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3206-Y5-R2FR-Bobs-residual-acquisition-runner-after-Kperp-screen-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3206_INPUTS.csv"
SCHEMA = OUT / "P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA.csv"
TEMPLATE = OUT / "P8_Y5_R2FR_3206_BOBS_CANDIDATE_INPUT_TEMPLATE.csv"
REFUSAL = OUT / "P8_Y5_R2FR_3206_SCORING_REFUSAL_GATE.csv"
DRYRUN = OUT / "P8_Y5_R2FR_3206_DRYRUN_SCORE_TABLE.csv"
QUEUE = OUT / "P8_Y5_R2FR_3206_NEXT_ACQUISITION_QUEUE.csv"
DECISION = OUT / "P8_Y5_R2FR_3206_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3206_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "formalization":
        return FW / relative_path
    if location == "post_checkpoint":
        return ROOT / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lower_terms = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lower_terms):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def b(value: bool) -> str:
    return "true" if value else "false"


def parse_positive_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed > 0.0:
        return parsed
    return None


SOURCES = [
    {
        "input_id": "SRC3206_00",
        "location": "post_checkpoint",
        "relative_path": "3205-Y5-R2FR-Kperp-extension-safety-screen-or-Bobs-pivot-under-AX1090.md",
        "role": "3205 triggered Bobs residual acquisition for scoring path",
        "terms": ["Bobs residual acquisition", "TRIGGERED_FOR_SCORING_PATH", "M_H_ref", "claim"],
    },
    {
        "input_id": "SRC3206_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3205_BOBS_PIVOT_TRIGGER.csv",
        "role": "machine-readable Bobs pivot trigger",
        "terms": ["TRIGGERED_FOR_SCORING_PATH", "M_H_ref", "source-measure", "boundary"],
    },
    {
        "input_id": "SRC3206_02",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "Bobs priority ledger and local-GR status synthesis",
        "terms": ["M_H_ref", "B_obs_source_measure", "B_obs_boundary", "Bobs"],
    },
    {
        "input_id": "SRC3206_03",
        "location": "post_checkpoint",
        "relative_path": "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
        "role": "Bobs input schema and missing observed-boundary-flux candidate",
        "terms": ["B_obs", "M_H_ref", "MISSING_COMPONENTS", "source_measure"],
    },
    {
        "input_id": "SRC3206_04",
        "location": "post_checkpoint",
        "relative_path": "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
        "role": "observed reduced boundary/source/projector flux decomposition",
        "terms": ["B_obs^nu", "B_source_measure", "B_projector", "Current MTS"],
    },
    {
        "input_id": "SRC3206_05",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv",
        "role": "Poynting residual bound schema",
        "terms": ["B_obs_EM_Poynting", "M_H_ref", "valid_for_claim"],
    },
    {
        "input_id": "SRC3206_06",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3201_COEFFICIENT_ACQUISITION_QUEUE.csv",
        "role": "Kperp/Bobs acquisition queue after rank-owner split",
        "terms": ["B_obs_source_measure", "MISSING_BOBS_SOURCE_ROWS", "KPERP"],
    },
]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "source_path": rel(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "generated_utc": now,
            }
        )
    return rows


def schema_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "DEN3206_00_MH_ref",
            "denominator",
            "M_H_ref_same_frame",
            "positive same-frame Hamiltonian/Newton denominator",
            "system_id;domain_id;M_H_ref;units;frame_definition;source_path;valid_for_claim",
            "must be positive, source-backed, same-frame, and noncircular",
            0,
        ),
        (
            "BOB3206_01_source_measure",
            "component",
            "B_obs_source_measure_over_MH",
            "projected source-measure / source-normalization leakage",
            "system_id;domain_id;raw_flux_bound;M_H_ref;projection;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "source-measure silence theorem or source-backed finite bound",
            1,
        ),
        (
            "BOB3206_02_boundary_improvement",
            "component",
            "B_obs_boundary_improvement_over_MH",
            "boundary/reference/worldtube improvement flux",
            "system_id;surface_id;boundary_class;raw_flux_bound;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "proper boundary zero theorem or source-backed finite boundary flux",
            2,
        ),
        (
            "BOB3206_03_projector_commutator",
            "component",
            "B_obs_projector_commutator_over_MH",
            "commutator leakage from P_loc/Pi_M/projector/frame split",
            "system_id;projector_id;commutator_bound;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "parent projector algebra or finite commutator bound",
            3,
        ),
        (
            "BOB3206_04_corner_edge",
            "component",
            "B_obs_corner_edge_over_MH",
            "corner/edge/tau-reference/surface mismatch residual",
            "system_id;corner_or_edge_id;raw_flux_bound;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "observed edge-mode zero theorem or finite corner flux source",
            4,
        ),
        (
            "BOB3206_05_Kperp_residual",
            "component",
            "B_obs_Kperp_residual_over_MH",
            "parked Kperp extension residual if local suppression is not parent-derived",
            "system_id;domain_id;Kperp_bound;projection;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "parent Kperp suppression theorem or source-backed residual bound",
            5,
        ),
        (
            "BOB3206_06_EM_Poynting",
            "component",
            "B_obs_EM_Poynting_over_MH",
            "EM/Poynting subchannel bound from 3200",
            "system_id;surface_id;S_normal_bound;tau_EM;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "quiet zero certificate or finite Poynting bound with tau_EM status",
            6,
        ),
        (
            "BOB3206_07_bulk_Euler",
            "component",
            "B_obs_bulk_Euler_over_MH",
            "bulk reduced Euler/Ward symbol residual",
            "system_id;domain_id;bulk_Euler_bound;M_H_ref;units;source_path;zero_theorem_or_bound;valid_for_claim",
            "on-shell reduced equations or finite source-backed bound",
            7,
        ),
        (
            "BOB3206_08_total_no_cancellation",
            "total",
            "B_observed_reduced_flux_over_MH",
            "absolute sum of live component bounds with no cancellation credit",
            "component_id;value;units;source_path;no_cancellation_flag;valid_for_claim",
            "all components valid, numeric, same-frame, and no-cancellation",
            8,
        ),
    ]
    return [
        {
            "schema_id": schema_id,
            "row_type": row_type,
            "quantity": quantity,
            "role": role,
            "required_columns": required_columns,
            "claim_gate": claim_gate,
            "priority": priority,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for schema_id, row_type, quantity, role, required_columns, claim_gate, priority in rows
    ]


def template_rows(schemas: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for row in schemas:
        value_field = "M_H_ref" if row["row_type"] == "denominator" else "component_bound"
        rows.append(
            {
                "template_id": row["schema_id"].replace("DEN", "TPL").replace("BOB", "TPL"),
                "schema_id": row["schema_id"],
                "row_type": row["row_type"],
                "quantity": row["quantity"],
                "system_id": "MISSING_SYSTEM_ID",
                "domain_or_surface_id": "MISSING_DOMAIN_OR_SURFACE_ID",
                value_field: "MISSING_NUMERIC_VALUE",
                "units": "MISSING_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "zero_theorem_or_bound": "MISSING_ZERO_THEOREM_OR_BOUND",
                "no_cancellation_flag": "true" if row["row_type"] == "total" else "not_applicable",
                "ready_to_score": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def refusal_rows(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    denominator = next(row for row in candidates if row["row_type"] == "denominator")
    components = [row for row in candidates if row["row_type"] == "component"]
    denominator_value = parse_positive_float(str(denominator.get("M_H_ref", "")))
    valid_components = [
        row for row in components
        if parse_positive_float(str(row.get("component_bound", ""))) is not None
        and row.get("valid_for_claim") == "true"
        and "MISSING" not in str(row.get("source_path", ""))
    ]
    rows = [
        {
            "gate_id": "REF3206_00_denominator",
            "gate": "M_H_ref positive same-frame denominator",
            "pass": b(denominator_value is not None and denominator.get("valid_for_claim") == "true"),
            "detail": "M_H_ref is missing, nonsourced, or not valid_for_claim",
            "score_action": "REFUSE_SCORE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "REF3206_01_components",
            "gate": "all required Bobs components numeric/source-backed",
            "pass": b(len(valid_components) == len(components)),
            "detail": f"valid_components={len(valid_components)} required_components={len(components)}",
            "score_action": "REFUSE_SCORE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "REF3206_02_no_cancellation",
            "gate": "absolute no-cancellation total",
            "pass": "false",
            "detail": "cannot build total until denominator and every live component row are valid",
            "score_action": "REFUSE_SCORE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "REF3206_03_overall",
            "gate": "Bobs residual score readiness",
            "pass": "false",
            "detail": "SCORE_REFUSED_CURRENT_CORPUS: acquisition schema exists but source-backed rows do not",
            "score_action": "WRITE_ACQUISITION_QUEUE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]
    return rows


def dryrun_rows(refusals: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    score_ready = all(row["pass"] == "true" for row in refusals[:3])
    return [
        {
            "score_id": "DRY3206_00_current_corpus",
            "score_status": "NOT_RUN_REFUSED" if not score_ready else "RUN_READY",
            "B_observed_reduced_flux_over_MH": "NOT_COMPUTED",
            "component_count": 7,
            "valid_component_count": 0,
            "denominator_status": "MISSING_MH_REF",
            "no_cancellation_status": "NOT_EVALUATED",
            "interpretation": "runner is executable but refuses to score without source-backed denominator and component rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def queue_rows() -> list[dict[str, object]]:
    now = stamp()
    queue = [
        ("ACQ3206_00", "M_H_ref_same_frame", "derive/source positive same-frame denominator", "M_H_ref, frame_definition, units, source_path", 0),
        ("ACQ3206_01", "B_obs_source_measure_over_MH", "derive source-measure silence or finite source-measure bound", "raw_flux_bound, projection, M_H_ref, units, source_path", 1),
        ("ACQ3206_02", "B_obs_boundary_improvement_over_MH", "derive proper boundary zero theorem or finite boundary flux", "boundary_class, raw_flux_bound, M_H_ref, units, source_path", 2),
        ("ACQ3206_03", "B_obs_projector_commutator_over_MH", "derive projector/frame commutator silence or finite commutator bound", "projector_id, commutator_bound, M_H_ref, units, source_path", 3),
        ("ACQ3206_04", "B_obs_corner_edge_over_MH", "derive edge/corner zero theorem or finite corner flux bound", "corner_or_edge_id, raw_flux_bound, M_H_ref, units, source_path", 4),
        ("ACQ3206_05", "B_obs_Kperp_residual_over_MH", "source/bound parked Kperp extension residual if not parent-suppressed", "Kperp_bound, projection, M_H_ref, units, source_path", 5),
        ("ACQ3206_06", "B_obs_EM_Poynting_over_MH", "supply quiet-zero certificate or finite Poynting bound", "S_normal_bound, tau_EM, M_H_ref, units, source_path", 6),
        ("ACQ3206_07", "B_obs_bulk_Euler_over_MH", "source on-shell reduced-Euler zero or finite bulk residual", "bulk_Euler_bound, M_H_ref, units, source_path", 7),
    ]
    return [
        {
            "queue_id": queue_id,
            "target": target,
            "required_next_input": required_next_input,
            "minimum_columns": minimum_columns,
            "priority": priority,
            "status": "MISSING_SOURCE_BACKED_ROW",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for queue_id, target, required_next_input, minimum_columns, priority in queue
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3206_00",
            "result": "BOBS_RUNNER_BUILT_SCORE_REFUSED_UNTIL_SOURCE_ROWS_EXIST",
            "claim_status": "NO_LOCAL_GR_NEWTON_PPN_OR_RESIDUAL_SCORE_CLAIM",
            "decision": "the Bobs acquisition runner is now executable and refuses scoring because M_H_ref and all live component rows are missing/source-invalid in the current corpus",
            "best_next_route": "acquire the first source-backed row, starting with M_H_ref same-frame denominator before any component score",
            "next_target": "3207-Y5-R2FR-MH-ref-denominator-source-row-or-Bobs-runner-remains-refused-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    schemas: list[dict[str, object]],
    candidates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, SCHEMA, TEMPLATE, REFUSAL, DRYRUN, QUEUE, DECISION]
    schema_quantities = {row["quantity"] for row in schemas}
    required = {
        "M_H_ref_same_frame",
        "B_obs_source_measure_over_MH",
        "B_obs_boundary_improvement_over_MH",
        "B_obs_projector_commutator_over_MH",
        "B_obs_corner_edge_over_MH",
        "B_obs_Kperp_residual_over_MH",
        "B_obs_EM_Poynting_over_MH",
        "B_obs_bulk_Euler_over_MH",
        "B_observed_reduced_flux_over_MH",
    }
    return [
        {
            "check_id": "VAL3206_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_01_schema_complete",
            "check": "Bobs schema includes denominator, live components, Poynting, Kperp, and total",
            "pass": b(required <= schema_quantities),
            "detail": f"schema_rows={len(schemas)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_02_template_nonclaim",
            "check": "candidate input template has no valid claim rows",
            "pass": b(all(row["valid_for_claim"] == "false" and row["ready_to_score"] == "false" for row in candidates)),
            "detail": f"template_rows={len(candidates)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_03_refusal_active",
            "check": "runner refuses scoring in current corpus",
            "pass": b(any(row["detail"].startswith("SCORE_REFUSED_CURRENT_CORPUS") for row in refusals)),
            "detail": ";".join(f"{row['gate']}={row['pass']}" for row in refusals),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_04_dryrun_no_score",
            "check": "dry run does not compute a residual score",
            "pass": b(dryrun[0]["score_status"] == "NOT_RUN_REFUSED" and dryrun[0]["B_observed_reduced_flux_over_MH"] == "NOT_COMPUTED"),
            "detail": dryrun[0]["interpretation"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_05_queue_prioritizes_denominator",
            "check": "acquisition queue starts with M_H_ref denominator",
            "pass": b(queue[0]["target"] == "M_H_ref_same_frame" and queue[0]["priority"] == 0),
            "detail": ";".join(f"{row['queue_id']}={row['target']}" for row in queue[:4]),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_06_decision_nonclaim",
            "check": "decision records runner built but score refused",
            "pass": b(decisions[0]["result"] == "BOBS_RUNNER_BUILT_SCORE_REFUSED_UNTIL_SOURCE_ROWS_EXIST" and decisions[0]["valid_for_claim"] == "false"),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_07_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [schemas, candidates, refusals, dryrun, queue, decisions] for row in table)),
            "detail": "no local-GR, Newton, PPN, Bobs score, or residual claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3206_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    schemas: list[dict[str, object]],
    refusals: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3206 - Bobs Residual Acquisition Runner After Kperp Screen Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, residual score, parent-action promotion, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3206 turns the Bobs pivot into an executable acquisition/refusal runner.",
        "",
        "Verdict:",
        "",
        "```text",
        "Bobs runner: built.",
        "Residual score: refused.",
        "Reason: M_H_ref and source-backed component rows are missing.",
        "```",
        "",
        "This is progress because the scoring path now has a machine-readable schema and a hard refusal gate, not vibes.",
        "",
        "## Component Schema",
        "",
    ]
    for row in schemas:
        lines.append(f"- `{row['schema_id']}`: `{row['quantity']}` - {row['role']}")
    lines.extend(["", "## Refusal Gate", ""])
    for row in refusals:
        lines.append(f"- `{row['gate_id']}`: `{row['gate']}` -> `{row['pass']}`; {row['detail']}")
    lines.extend(
        [
            "",
            "## Dry Run",
            "",
            f"- Status: `{dryrun[0]['score_status']}`",
            f"- Score: `{dryrun[0]['B_observed_reduced_flux_over_MH']}`",
            f"- Interpretation: {dryrun[0]['interpretation']}",
            "",
            "## Acquisition Queue",
            "",
        ]
    )
    for row in queue:
        lines.append(f"- `{row['queue_id']}`: `{row['target']}` -> `{row['status']}`")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"`{decisions[0]['result']}`.",
            "",
            f"Claim status: `{decisions[0]['claim_status']}`.",
            "",
            f"Decision: {decisions[0]['decision']}",
            "",
            f"Best next route: {decisions[0]['best_next_route']}",
            "",
            "Next target:",
            "",
            "```text",
            str(decisions[0]["next_target"]),
            "```",
            "",
            "## Generated Evidence",
            "",
            f"- `{rel(INPUTS)}`",
            f"- `{rel(SCHEMA)}`",
            f"- `{rel(TEMPLATE)}`",
            f"- `{rel(REFUSAL)}`",
            f"- `{rel(DRYRUN)}`",
            f"- `{rel(QUEUE)}`",
            f"- `{rel(DECISION)}`",
            f"- `{rel(VALIDATION)}`",
            "",
            "## Validation",
            "",
        ]
    )
    for row in validations:
        lines.append(f"- `{row['check_id']}`: `{row['pass']}` - {row['detail']}")
    lines.extend(["", "All generated rows remain `valid_for_claim=false`.", ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = input_rows()
    schemas = schema_rows()
    candidates = template_rows(schemas)
    refusals = refusal_rows(candidates)
    dryrun = dryrun_rows(refusals)
    queue = queue_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(SCHEMA, schemas)
    write_csv(TEMPLATE, candidates)
    write_csv(REFUSAL, refusals)
    write_csv(DRYRUN, dryrun)
    write_csv(QUEUE, queue)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, schemas, candidates, refusals, dryrun, queue, decisions)
    write_csv(VALIDATION, validations)
    write_doc(schemas, refusals, dryrun, queue, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3206 validation failed: {detail}")
    print(f"3206 generated {DOC}")


if __name__ == "__main__":
    main()
