from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_boundary_reference_first_row_data_and_theorem_zero_audit_no_claim_value_found"
CLAIM_CEILING = "boundary_reference_first_row_still_unfilled_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md"

DOC_PATH = Path("544-Y5-boundary-reference-first-row-data-or-theorem-zero.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_544_SOURCE_REGISTER.csv")
DATA_SOURCE_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv")
THEOREM_ZERO_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv")
FIRST_ROW_STATUS_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_544_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_544_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_544_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
        "role": "previous boundary/reference theorem attempt and first-row fill pack",
    },
    {
        "source_file": "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
        "role": "source-measure theorem attempt and first residual evaluator",
    },
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "source-measure contract and residual scorecard",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue and boundary/reference residual runner",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "boundary/R11 stress theorem stack and closure fill pack",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "boundary no-flux shortcut rejection",
    },
    {
        "source_file": "scripts/Y5_boundary_reference_first_row_data_or_theorem_zero.py",
        "role": "this checkpoint generator",
    },
]


CANDIDATE_FILES = [
    Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv"),
    Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_EVALUATOR.csv"),
    Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv"),
    Path("source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_EVALUATOR.csv"),
    Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv"),
    Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"),
    Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"),
    Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"),
    Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv"),
    Path("source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv"),
    Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"),
    Path("source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv"),
    Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv"),
    Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_REQUIRED_IDENTITIES.csv"),
    Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"),
]


REQUIRED_QUANTITIES = {
    "B_zero_flux": [
        "B_zero_flux",
        "B_zero",
        "boundary_flux",
        "boundary flux",
        "epsilon_boundary_flux",
        "linked-surface flux",
        "finite surface charges",
        "C_boundary",
        "boundary_improvement",
        "boundary monopole",
    ],
    "Delta_symp": [
        "Delta_symp",
        "symplectic_boundary",
        "symplectic boundary",
        "Hamiltonian reference",
        "reference subtraction",
        "reference shift",
        "Delta_symp_ref",
        "boundary/reference",
        "reference terms",
    ],
    "M_H_ref": [
        "M_H_ref",
        "M_H",
        "M_eff",
        "Meff",
        "Hilbert",
        "monopole calibration",
        "measured GM",
        "orbital GM",
        "mass charge",
        "source mass",
    ],
}

PLACEHOLDER_TERMS = [
    "MISSING",
    "missing",
    "not_filled",
    "template",
    "unfilled",
    "not_derived",
    "fail",
    "open",
    "conditional",
    "not_yet",
    "closure",
    "retained",
    "reference_only",
    "not_claimable",
    "blocks",
    "not_parent_derived",
    "no",
]

ZERO_LANGUAGE_TERMS = [
    "zero",
    "=0",
    "vanish",
    "vanishes",
    "silent",
    "topological",
    "no-flux",
    "no flux",
    "flux closure",
    "theorem_zero",
]

STATUS_KEYS = [
    "result",
    "current_status",
    "status",
    "owned_by_current_corpus",
    "valid_for_claim",
    "claim_status",
    "derivation_status",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: Any) -> float | None:
    try:
        text = str(value).strip()
        if text == "":
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def source_exists(source_file: str) -> bool:
    if not source_file:
        return False
    if "MISSING" in source_file or source_file.startswith("reference"):
        return False
    return (ROOT / source_file).exists()


def normalized_text(value: Any) -> str:
    return str(value or "").replace("_", " ").replace("-", " ").lower()


def row_text(row: dict[str, Any]) -> str:
    pieces: list[str] = []
    for key, value in row.items():
        pieces.append(str(key))
        pieces.append(str(value))
    return " | ".join(pieces)


def matched_quantities(row: dict[str, Any]) -> list[str]:
    raw = row_text(row)
    raw_lower = raw.lower()
    normalized = normalized_text(raw)
    matched: list[str] = []
    for quantity, terms in REQUIRED_QUANTITIES.items():
        if any(term.lower() in raw_lower or normalized_text(term) in normalized for term in terms):
            matched.append(quantity)
    return matched


def has_zero_language(row: dict[str, Any]) -> bool:
    raw_lower = row_text(row).lower()
    normalized = normalized_text(raw_lower)
    return any(term in raw_lower or normalized_text(term) in normalized for term in ZERO_LANGUAGE_TERMS)


def status_summary(row: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in STATUS_KEYS:
        if key in row and str(row.get(key, "")).strip():
            parts.append(f"{key}={row[key]}")
    return "; ".join(parts)


def declared_valid_for_claim(row: dict[str, Any]) -> bool:
    return str(row.get("valid_for_claim", "")).strip().lower() == "true"


def placeholder_detected(row: dict[str, Any]) -> bool:
    raw = row_text(row)
    return any(term in raw for term in PLACEHOLDER_TERMS)


def numeric_field_count(row: dict[str, Any]) -> int:
    return sum(1 for value in row.values() if parse_float(value) is not None)


def theorem_pass_language(row: dict[str, Any]) -> bool:
    raw = row_text(row).lower()
    result = str(row.get("result", "")).lower()
    status = str(row.get("current_status", "")).lower()
    owned = str(row.get("owned_by_current_corpus", "")).lower()
    if "conditional" in raw or "fail" in raw or "missing" in raw or "not_derived" in raw:
        return False
    if declared_valid_for_claim(row):
        return True
    if "pass" in result and owned in {"yes", "true", "owned"}:
        return True
    return "claim_ready" in status


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    for candidate in CANDIDATE_FILES:
        rows.append(
            {
                "source_file": rel(candidate),
                "role": "candidate CSV scanned for B_zero_flux, Delta_symp, M_H_ref, or theorem-zero evidence",
                "exists": (ROOT / candidate).exists(),
            }
        )
    return rows


def data_source_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    audit_index = 0
    for candidate in CANDIDATE_FILES:
        candidate_rows = read_csv(candidate)
        for row_number, row in enumerate(candidate_rows, start=1):
            quantities = matched_quantities(row)
            if not quantities:
                continue
            row_source = row.get("source_file", "")
            source_file_exists = source_exists(row_source)
            row_placeholder = placeholder_detected(row)
            numeric_count = numeric_field_count(row)
            covers_all = all(quantity in quantities for quantity in REQUIRED_QUANTITIES)
            reference_only = "reference" in row_text(row).lower() and declared_valid_for_claim(row) is False
            claim_candidate = (
                covers_all
                and declared_valid_for_claim(row)
                and source_file_exists
                and not row_placeholder
                and numeric_count >= 3
            )
            if claim_candidate:
                audit_status = "claim_data_candidate"
                reason = "row covers all required quantities with numeric source-backed claim-valid values"
            elif reference_only:
                audit_status = "rejected_reference_only"
                reason = "reference-only zero is explicitly not current MTS evidence"
            elif row_placeholder:
                audit_status = "rejected_template_open_or_conditional"
                reason = "row contains missing/template/conditional/open/fail language"
            elif not covers_all:
                audit_status = "not_first_row_complete"
                reason = "row does not cover B_zero_flux, Delta_symp, and M_H_ref together"
            elif not source_file_exists:
                audit_status = "rejected_no_source_file"
                reason = "row has no existing source_file for the value"
            else:
                audit_status = "rejected_not_claim_valid"
                reason = "row is not declared valid_for_claim"
            rows.append(
                {
                    "audit_id": f"DSA544_{audit_index}",
                    "candidate_file": rel(candidate),
                    "candidate_row": row_number,
                    "quantity_terms": ";".join(quantities),
                    "covers_all_required_quantities": str(covers_all).lower(),
                    "declared_valid_for_claim": str(declared_valid_for_claim(row)).lower(),
                    "row_source_file": row_source,
                    "source_file_exists": str(source_file_exists).lower(),
                    "placeholder_detected": str(row_placeholder).lower(),
                    "numeric_field_count": numeric_count,
                    "status_summary": status_summary(row),
                    "audit_status": audit_status,
                    "reason": reason,
                    "claim_data_candidate": str(claim_candidate).lower(),
                }
            )
            audit_index += 1
    return rows


def theorem_zero_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    audit_index = 0
    for candidate in CANDIDATE_FILES:
        candidate_rows = read_csv(candidate)
        for row_number, row in enumerate(candidate_rows, start=1):
            quantities = matched_quantities(row)
            if not quantities and not has_zero_language(row):
                continue
            zero_language = has_zero_language(row)
            if not zero_language:
                continue
            claim_zero = theorem_pass_language(row) and all(quantity in quantities for quantity in ["B_zero_flux", "Delta_symp"])
            if claim_zero:
                audit_status = "claim_zero_candidate"
                reason = "row appears to be an owned theorem zero for the numerator"
            elif "reference" in row_text(row).lower() and declared_valid_for_claim(row) is False:
                audit_status = "rejected_reference_only"
                reason = "reference zero is not current MTS evidence"
            elif "conditional" in row_text(row).lower():
                audit_status = "rejected_conditional_only"
                reason = "zero is conditional on unowned premises"
            elif "fail" in row_text(row).lower() or "not_derived" in row_text(row).lower():
                audit_status = "rejected_failed_or_not_derived"
                reason = "row explicitly says failed/not-derived"
            elif not all(quantity in quantities for quantity in ["B_zero_flux", "Delta_symp"]):
                audit_status = "not_boundary_reference_numerator_zero"
                reason = "zero language does not jointly prove B_zero_flux=Delta_symp=0"
            else:
                audit_status = "rejected_not_claim_valid"
                reason = "zero language is not owned/claim-valid"
            rows.append(
                {
                    "audit_id": f"TZA544_{audit_index}",
                    "candidate_file": rel(candidate),
                    "candidate_row": row_number,
                    "zero_target_terms": ";".join(quantities) if quantities else "general_zero_language",
                    "zero_language_detected": str(zero_language).lower(),
                    "declared_valid_for_claim": str(declared_valid_for_claim(row)).lower(),
                    "status_summary": status_summary(row),
                    "audit_status": audit_status,
                    "reason": reason,
                    "claim_zero_candidate": str(claim_zero).lower(),
                }
            )
            audit_index += 1
    return rows


def first_row_status_rows(
    data_audit: list[dict[str, Any]],
    theorem_audit: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for quantity in ["B_zero_flux", "Delta_symp", "M_H_ref"]:
        data_hits = [row for row in data_audit if quantity in row["quantity_terms"].split(";")]
        claim_data_hits = [row for row in data_hits if row["claim_data_candidate"] == "true"]
        theorem_hits = [row for row in theorem_audit if quantity in row["zero_target_terms"].split(";")]
        claim_theorem_hits = [row for row in theorem_hits if row["claim_zero_candidate"] == "true"]
        rows.append(
            {
                "quantity": quantity,
                "required_role": {
                    "B_zero_flux": "boundary/improvement linked-surface flux numerator",
                    "Delta_symp": "Hamiltonian reference/symplectic subtraction numerator",
                    "M_H_ref": "positive Hilbert/source mass denominator tied to measured GM",
                }[quantity],
                "data_rows_with_term": len(data_hits),
                "claim_valid_data_rows": len(claim_data_hits),
                "theorem_zero_rows_with_term": len(theorem_hits),
                "claim_valid_theorem_zero_rows": len(claim_theorem_hits),
                "current_best_evidence": "templates, contracts, or conditional/failed theorem rows only",
                "status": "missing_claim_valid_source_or_zero_theorem",
                "next_action": "derive from minimal parent action clause or fill retained residual row with source-backed data",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "quantity": "epsilon_boundary_reference_abs",
            "required_role": "(|B_zero_flux|+|Delta_symp|)/M_H_ref first residual envelope",
            "data_rows_with_term": len([row for row in data_audit if "B_zero_flux" in row["quantity_terms"] and "Delta_symp" in row["quantity_terms"] and "M_H_ref" in row["quantity_terms"]]),
            "claim_valid_data_rows": len([row for row in data_audit if row["claim_data_candidate"] == "true"]),
            "theorem_zero_rows_with_term": len([row for row in theorem_audit if "B_zero_flux" in row["zero_target_terms"] and "Delta_symp" in row["zero_target_terms"]]),
            "claim_valid_theorem_zero_rows": len([row for row in theorem_audit if row["claim_zero_candidate"] == "true"]),
            "current_best_evidence": "not computed for current MTS; reference zero remains non-evidence",
            "status": "first_row_unfilled",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    )
    return rows


def decision_rows(data_audit: list[dict[str, Any]], theorem_audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claim_data_rows = [row for row in data_audit if row["claim_data_candidate"] == "true"]
    claim_zero_rows = [row for row in theorem_audit if row["claim_zero_candidate"] == "true"]
    return [
        {
            "decision_id": "D544_0_no_claim_valid_data_row",
            "status": "no_source_backed_first_row_values_found",
            "meaning": "scan found no claim-valid numeric values for B_zero_flux, Delta_symp, and M_H_ref together",
            "evidence_count": len(claim_data_rows),
            "claim_status": "first_row_unfilled",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D544_1_no_claim_valid_theorem_zero",
            "status": "no_owned_boundary_reference_zero_theorem_found",
            "meaning": "zero language exists, but it is reference-only, conditional, failed, or not the required numerator theorem",
            "evidence_count": len(claim_zero_rows),
            "claim_status": "boundary_reference_zero_not_derived",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D544_2_derivability_rule",
            "status": "must_not_smuggle_plateau_or_zero_axiom",
            "meaning": "next work must derive the boundary/reference zero from a parent action clause or retain the residual explicitly",
            "evidence_count": 0,
            "claim_status": "derivation_required",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D544_3_private_no_push",
            "status": "private_no_github",
            "meaning": "no public/GitHub action is performed",
            "evidence_count": 0,
            "claim_status": "safe_private_work",
            "next_action": "continue_private_derivation",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "BOUNDARY_REFERENCE_FIRST_ROW",
            "previous_status": "fill_pack_written_zero_theorem_failed",
            "new_status": "data_and_theorem_audit_done_no_claim_value_found",
            "accepted_for_claim": "false",
            "next_target": NEXT_TARGET,
        },
        {
            "route_id": "SOURCE_MEASURE_THEOREM",
            "previous_status": "blocked_by_boundary_reference_first_row",
            "new_status": "still_blocked_first_row_unfilled",
            "accepted_for_claim": "false",
            "next_target": NEXT_TARGET,
        },
        {
            "route_id": "SOURCE_NORMALIZED_NEWTON",
            "previous_status": "blocked_by_source_measure_and_measured_GM",
            "new_status": "still_blocked_boundary_reference_and_GM_denominator_missing",
            "accepted_for_claim": "false",
            "next_target": NEXT_TARGET,
        },
        {
            "route_id": "LOCAL_GR",
            "previous_status": "blocked_source_measure_Newton_PPN",
            "new_status": "still_blocked_no_boundary_reference_parent_zero",
            "accepted_for_claim": "false",
            "next_target": NEXT_TARGET,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    data_audit: list[dict[str, Any]],
    theorem_audit: list[dict[str, Any]],
    first_row_status: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    missing_candidates = [rel(path) for path in CANDIDATE_FILES if not (ROOT / path).exists()]
    prior_fill_pack = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv"))
    prior_evaluator = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_EVALUATOR.csv"))
    claim_data_rows = [row for row in data_audit if row["claim_data_candidate"] == "true"]
    claim_zero_rows = [row for row in theorem_audit if row["claim_zero_candidate"] == "true"]
    first_row_claims = [row for row in first_row_status if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V544_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V544_1_candidate_files_exist",
            "result": "pass" if not missing_candidates else "fail",
            "detail": f"missing_candidates={len(missing_candidates)}",
        },
        {
            "check_id": "V544_2_prior_543_loaded",
            "result": "pass" if len(prior_fill_pack) == 2 and len(prior_evaluator) == 2 else "fail",
            "detail": f"prior_fill_pack_rows={len(prior_fill_pack)};prior_evaluator_rows={len(prior_evaluator)}",
        },
        {
            "check_id": "V544_3_data_audit_written",
            "result": "pass" if len(data_audit) >= 10 else "fail",
            "detail": f"data_audit_rows={len(data_audit)}",
        },
        {
            "check_id": "V544_4_theorem_zero_audit_written",
            "result": "pass" if len(theorem_audit) >= 10 else "fail",
            "detail": f"theorem_zero_audit_rows={len(theorem_audit)}",
        },
        {
            "check_id": "V544_5_no_claim_evidence_found",
            "result": "pass" if not claim_data_rows and not claim_zero_rows else "fail",
            "detail": f"claim_data_rows={len(claim_data_rows)};claim_zero_rows={len(claim_zero_rows)}",
        },
        {
            "check_id": "V544_6_first_row_status_no_overclaim",
            "result": "pass" if len(first_row_status) == 4 and not first_row_claims else "fail",
            "detail": "boundary_reference_zero_derived=false; first_residual_claim_filled=false; source_measure=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    data_audit: list[dict[str, Any]],
    theorem_audit: list[dict[str, Any]],
    first_row_status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, str]],
    route_updates: list[dict[str, Any]],
) -> str:
    claim_data_rows = [row for row in data_audit if row["claim_data_candidate"] == "true"]
    claim_zero_rows = [row for row in theorem_audit if row["claim_zero_candidate"] == "true"]
    return f"""# 544 - Y5 Boundary Reference First Row Data or Theorem Zero

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

I scanned the current post-checkpoint evidence for either:

```text
source-backed numbers for B_zero_flux, Delta_symp, and M_H_ref
```

or:

```text
an owned theorem proving B_zero_flux = Delta_symp = 0
```

The result is still negative for claim use.

There are many useful contract/template/conditional rows, but no row gives a claim-valid current-MTS value for the first boundary/reference residual. The reference-zero row is useful as a calculator sanity check only; it is not evidence for the current theory branch.

## 2. Data Source Audit

{markdown_table(data_audit)}

## 3. Theorem-Zero Audit

{markdown_table(theorem_audit)}

## 4. First Row Status

{markdown_table(first_row_status)}

## 5. Decision

{markdown_table(decisions)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(route_updates)}

## 9. Claim Ceiling

Allowed:

```text
MTS has audited the corpus for first-row boundary/reference data and theorem-zero evidence.
MTS has found the exact missing first-row quantities.
MTS has kept the local-GR reduction gate honest.
```

Forbidden:

```text
MTS has filled epsilon_boundary_reference_abs for the current branch.
MTS has proved B_zero_flux=Delta_symp=0.
MTS has derived source-measure glue, measured GM, Newton, PPN, or local GR.
```

## 10. Practical Read

This is the right kind of grim: not a contradiction, but a hard derivation gate. The corpus is not telling us "the local branch is dead"; it is telling us "do not pretend boundary/reference charge bookkeeping is done."

The next useful move is no longer another broad scan. We need the minimal parent action clause or boundary condition contract that would make the numerator vanish. If that cannot be written without an axiom, this row becomes an explicit residual input rather than a hidden assumption.

## 11. Audit Counts

```text
data_audit_rows={len(data_audit)}
theorem_zero_audit_rows={len(theorem_audit)}
claim_data_rows={len(claim_data_rows)}
claim_zero_rows={len(claim_zero_rows)}
```

## 12. Next Target

`{NEXT_TARGET}`

Next: write the exact minimal action/boundary contract that would derive `B_zero_flux=Delta_symp=0`; if it cannot be made parent-owned, keep `epsilon_boundary_reference_abs` as a retained residual row.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-boundary-reference-first-row-data-or-theorem-zero"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    data_audit = data_source_audit_rows()
    theorem_audit = theorem_zero_audit_rows()
    first_row_status = first_row_status_rows(data_audit, theorem_audit)
    decisions = decision_rows(data_audit, theorem_audit)
    route_updates = route_update_rows()
    validations = validation_rows(sources, data_audit, theorem_audit, first_row_status)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (DATA_SOURCE_AUDIT_PATH, data_audit),
        (THEOREM_ZERO_AUDIT_PATH, theorem_audit),
        (FIRST_ROW_STATUS_PATH, first_row_status),
        (DECISION_PATH, decisions),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, route_updates),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(
        generated_at_utc,
        run_dir,
        sources,
        data_audit,
        theorem_audit,
        first_row_status,
        decisions,
        validations,
        route_updates,
    )
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    missing_candidates = [rel(path) for path in CANDIDATE_FILES if not (ROOT / path).exists()]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_data_rows = [row for row in data_audit if row["claim_data_candidate"] == "true"]
    claim_zero_rows = [row for row in theorem_audit if row["claim_zero_candidate"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "data_source_audit": str(ROOT / DATA_SOURCE_AUDIT_PATH),
        "theorem_zero_audit": str(ROOT / THEOREM_ZERO_AUDIT_PATH),
        "first_row_status": str(ROOT / FIRST_ROW_STATUS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "candidate_files": len(CANDIDATE_FILES),
        "missing_candidate_files": missing_candidates,
        "failed_validation_rows": len(failed_validations),
        "data_audit_rows": len(data_audit),
        "theorem_zero_audit_rows": len(theorem_audit),
        "first_row_status_rows": len(first_row_status),
        "claim_data_rows": len(claim_data_rows),
        "claim_zero_rows": len(claim_zero_rows),
        "boundary_reference_zero_derived": False,
        "first_boundary_reference_residual_claim_filled": False,
        "source_measure_theorem_derived": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nboundary_reference_first_row_unfilled_no_source_measure_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
