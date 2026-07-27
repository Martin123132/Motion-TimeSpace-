from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "radial_bound_inputs_audited_no_fillable_source_backed_numeric_rows_return_to_parent_glue"
CLAIM_CEILING = "no_radial_bound_score_no_epsilon_radial_Meff_zero_no_local_GR_or_Newton_promotion"
NEXT_TARGET = "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md"

DOC_PATH = Path("503-fill-radial-bound-inputs-or-return-to-parent-glue.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_SOURCE_REGISTER.csv")
SCAN_RESULTS_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_SCAN_RESULTS.csv")
GAP_LEDGER_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_GAP_LEDGER.csv")
FILL_DECISION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_FILL_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_ROUTE_UPDATE.csv")
NEXT_QUEUE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_NEXT_QUEUE.csv")

RUNNER_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv")
RUNNER_DRYRUN_RESULTS_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_DRYRUN_RESULTS.csv")
RUNNER_FORMULA_MAP_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_FORMULA_MAP.csv")
LOCAL_BOUNDS_PATH = Path("source-intake/local_bounds/local_bound_claims.csv")
P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
EQUALITY_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_INPUT_TEMPLATE.csv")

REQUIRED_TERMS = [
    "R_eq_integral",
    "I_extra_channel",
    "I_parent_radial",
    "I_value",
    "epsilon_radial_Meff",
    "dln_mu_dlnr",
    "partial_r_ln_mu_obs",
    "partial_r mu_obs",
    "radial_source_hair",
    "d(Pi_M J)",
]

RUNNER_VALUE_COLUMNS = {
    "I_value",
    "R_eq_integral",
    "I_extra_channel",
    "I_parent_radial",
    "epsilon_radial_Meff",
    "dln_mu_dlnr",
    "partial_r_ln_mu_obs",
    "computed_epsilon_radial_Meff",
    "computed_dln_mu_dlnr",
}

PLACEHOLDER_TOKENS = [
    "fill_",
    "missing",
    "not_filled",
    "not_run",
    "not_computed",
    "template",
    "placeholder",
    "symbolic",
    "required",
]

VALID_SOURCE_PLACEHOLDERS = {
    "",
    "fill_source_path",
    "fill_derivation_or_run_path",
    "not_applicable",
    "none",
    "missing",
}

NUMERIC_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


SOURCE_REGISTER = [
    {
        "source_file": "502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md",
        "role": "runner scaffold and no-data/no-claim state",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "equality theorem failed and radial-bound input template was created",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "exact source-normalization radial integral and bound formula",
    },
    {
        "source_file": str(RUNNER_INPUT_TEMPLATE_PATH),
        "role": "required numeric rows for the 502 runner",
    },
    {
        "source_file": str(RUNNER_DRYRUN_RESULTS_PATH),
        "role": "dry-run evidence that the runner correctly refuses a no-data score",
    },
    {
        "source_file": str(RUNNER_FORMULA_MAP_PATH),
        "role": "epsilon_radial_Meff and dln_mu_dlnr formula map",
    },
    {
        "source_file": str(EQUALITY_TEMPLATE_PATH),
        "role": "501 equality residual template rows",
    },
    {
        "source_file": str(LOCAL_BOUNDS_PATH),
        "role": "external local PPN/fifth-force locks, not source-integral inputs",
    },
    {
        "source_file": str(P8_TEMPLATE_PATH),
        "role": "P8 residual vector template containing radial source hair row",
    },
    {
        "source_file": "scripts/fill_radial_bound_inputs_or_return_to_parent_glue.py",
        "role": "this checkpoint generator and fillability audit",
    },
]

GAP_LEDGER_ROWS = [
    {
        "gap_id": "G503_0_R_eq_integral",
        "required_input": "system_id;r1;r2;R_eq_integral or I_value for channel=R_eq;units;source_file;assumptions",
        "current_evidence": "only template rows and symbolic equality-residual formulas found",
        "why_it_matters": "R_eq is the direct equality failure term in Pi_M J_H = J_M_top + dB_zero + R_eq",
        "minimum_fill_route": "derive R_eq=0 from parent Hilbert/topological glue, or provide a sourced worldtube integral bound",
        "claim_if_unfilled": "epsilon_radial_Meff remains unscored",
    },
    {
        "gap_id": "G503_1_B_zero_or_boundary_flux",
        "required_input": "system_id;r1;r2;I_B_zero or boundary flux integral;units;source_file;assumptions",
        "current_evidence": "boundary terms are repeatedly named as danger channels, but not numerically bounded here",
        "why_it_matters": "a divergence can hide exactly the radial/source hair that local PPN tests punish",
        "minimum_fill_route": "prove compact-boundary no-flux/topological silence, or provide a sourced surface-flux bound",
        "claim_if_unfilled": "no Newton/local-GR promotion from boundary bookkeeping",
    },
    {
        "gap_id": "G503_2_extra_source_channels",
        "required_input": "channelwise I_extra_channel for domain, bulk, non-EH, kappa, frame, species, memory, and connection rows",
        "current_evidence": "channel names and local locks exist, but no executable radial integral vector was found",
        "why_it_matters": "small total residual by cancellation is not accepted; each channel must be zero-derived or separately bounded",
        "minimum_fill_route": "derive theorem-zero certificates for each channel or fill source-backed numeric bounds",
        "claim_if_unfilled": "mu_extra remains retained",
    },
    {
        "gap_id": "G503_3_observed_radial_profile",
        "required_input": "system_id;r1;r2;dln_mu_dlnr or epsilon_radial_Meff profile bound;bound_source;pass_fail",
        "current_evidence": "local empirical locks exist for gamma, beta, Gdot, alpha(lambda), and operator rows, but no radial profile was found",
        "why_it_matters": "source-normalized Newton needs a constant measured monopole, not just a fitted GM at one radius",
        "minimum_fill_route": "connect to a specific orbital/ephemeris/fifth-force data product or derive d(Pi_M J)=0",
        "claim_if_unfilled": "radial source hair stays open",
    },
]

FILL_DECISION_ROWS = [
    {
        "decision_id": "D503_0_no_auto_fill",
        "decision": "do_not_fill_runner_inputs",
        "basis": "no source-backed numeric R_eq, I_extra_channel, I_parent_radial, epsilon_radial_Meff, or dln_mu_dlnr rows were found",
        "allowed_next_action": "return_to_parent_glue_or_build_explicit_external_input_plan",
        "forbidden_next_action": "compute epsilon_radial_Meff from placeholders or call local GR/Newton recovered",
        "valid_for_claim": "true",
    },
    {
        "decision_id": "D503_1_local_bounds_are_locks_not_inputs",
        "decision": "keep_local_bound_rows_as_acceptance_locks",
        "basis": "Cassini, beta, Gdot, fifth-force, WEP, and R11 rows constrain any future residual but do not supply the missing parent source integrals",
        "allowed_next_action": "map future numeric residuals to R3/R4/R9/R10/R11 thresholds",
        "forbidden_next_action": "treat empirical null bounds as derivations of d(Pi_M J)=0",
        "valid_for_claim": "true",
    },
    {
        "decision_id": "D503_2_derivation_priority",
        "decision": "prefer_parent_Hilbert_worldtube_glue_before_more_scoring",
        "basis": "the runner is built; the missing object is the equality/source-measure bridge, not a plotting or coding problem",
        "allowed_next_action": NEXT_TARGET,
        "forbidden_next_action": "smuggle plateau/no-hair axioms into the parent action",
        "valid_for_claim": "true",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "R503_0_current_branch",
        "status": "blocked_for_numeric_scoring_not_blocked_for_derivation",
        "what_closed": "confirmed the radial runner has no legitimate source-backed inputs to consume yet",
        "what_remains": "derive the parent Hilbert worldtube/source-measure glue or define an explicit external radial input protocol",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R503_1_claim_ceiling",
        "status": "claim_ceiling_enforced",
        "what_closed": "no placeholder arithmetic and no public-facing local-GR claim",
        "what_remains": "turn Pi_M J_H equality into a parent theorem or retain closure-only status",
        "next_target": NEXT_TARGET,
    },
]

NEXT_QUEUE_ROWS = [
    {
        "priority": "1",
        "target": NEXT_TARGET,
        "why": "this is the only non-cheat route to epsilon_radial_Meff=0 from the theory itself",
        "deliverable": "worldtube/source-measure theorem attempt with explicit failure clauses",
    },
    {
        "priority": "2",
        "target": "external radial input protocol",
        "why": "if derivation stalls, the runner needs real residual integrals or orbital/fifth-force profile bounds",
        "deliverable": "data contract for r1/r2/source/channel/unit/no-cancellation rows",
    },
    {
        "priority": "3",
        "target": "constant measured-GM calibration lock",
        "why": "even a radial bound does not alone prove GR; measured-GM, Poisson/Gauss, and constant G still have to line up",
        "deliverable": "separate theorem stack for monopole calibration",
    },
]


def is_numeric(value: str) -> bool:
    return bool(NUMERIC_RE.match(value.strip()))


def normalize_boolish(value: str) -> str:
    return value.strip().lower()


def has_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in PLACEHOLDER_TOKENS)


def is_real_source_path(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered not in VALID_SOURCE_PLACEHOLDERS and not lowered.startswith("fill_")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv_rows(path: Path, max_rows: int | None = None) -> tuple[list[str], list[dict[str, str]], str]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            rows: list[dict[str, str]] = []
            for index, row in enumerate(reader):
                if max_rows is not None and index >= max_rows:
                    break
                rows.append({key or "": value or "" for key, value in row.items()})
            return list(reader.fieldnames or []), rows, "parsed"
    except Exception as exc:  # noqa: BLE001 - audit wants status not exception bubbling
        return [], [], f"parse_error:{type(exc).__name__}:{exc}"


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": path.exists(),
            }
        )
    return rows


def row_is_fillable_candidate(row: dict[str, str], fieldnames: list[str]) -> tuple[bool, str]:
    value_columns = [field for field in fieldnames if field in RUNNER_VALUE_COLUMNS]
    if not value_columns:
        return False, "no_runner_value_columns"

    numeric_columns = [field for field in value_columns if is_numeric(row.get(field, ""))]
    if not numeric_columns:
        return False, "no_numeric_runner_values"

    numeric_status = normalize_boolish(row.get("numeric_status", ""))
    if numeric_status in {"missing", "not_computed", "not_run", "placeholder"}:
        return False, "numeric_status_not_ready"

    valid_for_claim = normalize_boolish(row.get("valid_for_claim", ""))
    if valid_for_claim == "false":
        return False, "valid_for_claim_false"

    source_file = row.get("source_file", "")
    if "source_file" in fieldnames and not is_real_source_path(source_file):
        return False, "source_file_placeholder"

    joined = " ".join(str(value) for value in row.values())
    if has_placeholder(joined):
        return False, "placeholder_tokens_present"

    return True, "fillable_candidate"


def scan_candidate_csvs() -> list[dict[str, Any]]:
    search_roots = [ROOT / "source-intake", ROOT / "runs"]
    scan_rows: list[dict[str, Any]] = []

    for search_root in search_roots:
        if not search_root.exists():
            continue
        for path in sorted(search_root.rglob("*.csv")):
            fieldnames, rows, parse_status = read_csv_rows(path, max_rows=500)
            header_text = " ".join(fieldnames)
            body_text = " ".join(" ".join(row.values()) for row in rows[:50])
            searchable = f"{header_text} {body_text}"
            matched_terms = [term for term in REQUIRED_TERMS if term in searchable]
            if not matched_terms:
                continue

            candidate_count = 0
            rejection_reasons: dict[str, int] = {}
            placeholder_row_count = 0
            false_claim_count = 0
            numeric_value_count = 0
            source_path_count = 0

            for row in rows:
                joined = " ".join(row.values())
                if has_placeholder(joined):
                    placeholder_row_count += 1
                if normalize_boolish(row.get("valid_for_claim", "")) == "false":
                    false_claim_count += 1
                if any(is_numeric(row.get(field, "")) for field in RUNNER_VALUE_COLUMNS if field in row):
                    numeric_value_count += 1
                if is_real_source_path(row.get("source_file", "")):
                    source_path_count += 1

                is_candidate, reason = row_is_fillable_candidate(row, fieldnames)
                if is_candidate:
                    candidate_count += 1
                else:
                    rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1

            if candidate_count:
                classification = "fillable_numeric_candidate_requires_manual_review"
            elif path.name.endswith("_TEMPLATE.csv") or placeholder_row_count:
                classification = "template_or_placeholder_only"
            elif numeric_value_count and not source_path_count:
                classification = "numeric_without_runner_source_path"
            elif "local_bound_claims" in path.name:
                classification = "local_empirical_lock_not_runner_input"
            else:
                classification = "symbolic_or_decision_reference"

            scan_rows.append(
                {
                    "csv_file": rel(path),
                    "parse_status": parse_status,
                    "matched_terms": ";".join(matched_terms),
                    "field_count": len(fieldnames),
                    "sampled_rows": len(rows),
                    "numeric_runner_value_rows": numeric_value_count,
                    "real_source_path_rows": source_path_count,
                    "placeholder_rows": placeholder_row_count,
                    "valid_for_claim_false_rows": false_claim_count,
                    "fillable_candidate_rows": candidate_count,
                    "dominant_rejection_reasons": ";".join(f"{key}:{value}" for key, value in sorted(rejection_reasons.items())),
                    "classification": classification,
                }
            )

    scan_rows.sort(
        key=lambda row: (
            row["classification"] != "fillable_numeric_candidate_requires_manual_review",
            row["classification"] != "template_or_placeholder_only",
            row["csv_file"],
        )
    )
    return scan_rows


def validation_rows(sources: list[dict[str, Any]], scans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    parse_failures = [row["csv_file"] for row in scans if not str(row["parse_status"]).startswith("parsed")]
    fillable_count = sum(int(row["fillable_candidate_rows"]) for row in scans)
    return [
        {
            "check_id": "V503_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V503_1_csv_scan_parsed",
            "result": "pass" if not parse_failures else "fail",
            "detail": f"parse_failures={len(parse_failures)}",
        },
        {
            "check_id": "V503_2_no_fillable_inputs_found",
            "result": "pass" if fillable_count == 0 else "review",
            "detail": f"fillable_candidate_rows={fillable_count}",
        },
        {
            "check_id": "V503_3_runner_not_scored_from_placeholders",
            "result": "pass",
            "detail": "radial_bound_scored=false",
        },
        {
            "check_id": "V503_4_local_GR_claim_blocked",
            "result": "pass",
            "detail": "local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        full_path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        (results_dir / filename).write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    scans: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    fillable_count = sum(int(row["fillable_candidate_rows"]) for row in scans)
    scanned_count = len(scans)
    scan_preview = scans[:40]
    return f"""# 503 — Fill Radial-Bound Inputs or Return to Parent Glue

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Short Answer

The 502 runner is executable as a dry-run scaffold, but the corpus does **not** yet contain source-backed numeric rows for `R_eq_integral`, `I_extra_channel`, `I_parent_radial`, `epsilon_radial_Meff`, or `dln_mu_dlnr`.

So the honest move is:

```text
do not score the radial bound from placeholders;
return to parent Hilbert/worldtube/source-measure glue, or build an explicit external input plan.
```

That is not a failure of the framework; it is the theory-discipline gate doing its job. The missing thing is not another notebook cell. The missing thing is the parent identity that says which source current is the measured monopole, or a sourced external residual integral that bounds the failure.

## 2. Source Register

{markdown_table(sources)}

## 3. Scan Summary

- Matching CSV/source rows scanned: `{scanned_count}`
- Fillable numeric candidate rows found: `{fillable_count}`
- Decision: `no_auto_fill`

The scan found many symbolic references, templates, decision rows, and local empirical locks. It did not find the actual runner input rows needed to compute a radial bound.

## 4. Scan Results Preview

{markdown_table(scan_preview)}

## 5. Gap Ledger

{markdown_table(GAP_LEDGER_ROWS)}

## 6. Fill Decision

{markdown_table(FILL_DECISION_ROWS)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
MTS has an executable radial-bound runner scaffold.
MTS has audited the corpus and found no fillable source-backed radial input rows yet.
MTS has a clear next fork: derive parent glue or build an explicit external input protocol.
```

Forbidden:

```text
MTS has scored epsilon_radial_Meff.
MTS has derived epsilon_radial_Meff = 0.
MTS has derived d(Pi_M J)=0.
MTS has derived mu_extra = 0.
MTS has recovered Newton/PPN/local GR from the parent action.
```

## 10. Next Queue

{markdown_table(NEXT_QUEUE_ROWS)}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-fill-radial-bound-inputs-or-return-to-parent-glue"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    scans = scan_candidate_csvs()
    validations = validation_rows(sources, scans)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SCAN_RESULTS_PATH, scans),
        (GAP_LEDGER_PATH, GAP_LEDGER_ROWS),
        (FILL_DECISION_PATH, FILL_DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
        (NEXT_QUEUE_PATH, NEXT_QUEUE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, scans, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    parse_failures = [row["csv_file"] for row in scans if not str(row["parse_status"]).startswith("parsed")]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    review_validations = [row for row in validations if row["result"] == "review"]
    fillable_count = sum(int(row["fillable_candidate_rows"]) for row in scans)
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "scan_results": str(ROOT / SCAN_RESULTS_PATH),
        "gap_ledger": str(ROOT / GAP_LEDGER_PATH),
        "fill_decision": str(ROOT / FILL_DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "next_queue": str(ROOT / NEXT_QUEUE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "scan_rows": len(scans),
        "parse_failures": len(parse_failures),
        "failed_validation_rows": len(failed_validations),
        "review_validation_rows": len(review_validations),
        "fillable_numeric_input_rows": fillable_count,
        "radial_bound_scored": False,
        "epsilon_radial_Meff_computed": False,
        "dln_mu_dlnr_computed": False,
        "epsilon_radial_Meff_zero_derived": False,
        "Hilbert_topological_current_equality_derived": False,
        "parent_worldtube_glue_derived": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "returned_to_parent_glue": True,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
