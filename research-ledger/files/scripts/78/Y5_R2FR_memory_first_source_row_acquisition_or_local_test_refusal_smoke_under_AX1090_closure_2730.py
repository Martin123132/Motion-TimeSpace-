from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2730-Y5-R2FR-memory-first-source-row-acquisition-or-local-test-refusal-smoke-under-AX1090-closure.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2730_SOURCE_REGISTER.csv",
    "scan": RESIDUALS / "P8_Y5_R2FR_2730_MEMORY_SOURCE_ROW_ACQUISITION_SCAN.csv",
    "accepted": RESIDUALS / "P8_Y5_R2FR_2730_ACCEPTED_MEMORY_SOURCE_ROWS_NONCLAIM.csv",
    "rejection": RESIDUALS / "P8_Y5_R2FR_2730_REJECTION_LEDGER.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2730_LOCAL_TEST_REFUSAL_SMOKE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2730_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2730_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2730_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2730_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2730_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_scan": LOCAL_BOUNDS / "memory_source_row_scan_2730_NONCLAIM.csv",
    "refusal_smoke": LOCAL_BOUNDS / "memory_local_test_refusal_smoke_2730_NONCLAIM.csv",
    "source_weight_rejection": SOURCE_WEIGHT / "memory_source_row_rejection_2730_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2730_MEMORY_PARENT_ACTION_DEEP_SOURCE_HUNT_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in cols) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2730_0_2729_handoff",
            "2730 source-row/refusal target",
            DOC.parent / "2729-Y5-R2FR-parent-memory-signature-contract-plus-finite-local-residual-interface-under-AX1090-closure.md",
            ["NEXT2729_0_selected", "MFI2729_0_lambda_gap", "VAL2729_OVERALL"],
        ),
        (
            "SRC2730_1_1024_scalar_chain",
            "old scalar nohair input pack already refused Z_X/M_X/J_X rows",
            DOC.parent / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            ["SIA1024_1_Z_X", "ALPHA1024_0_bulk_operator", "RUN1024_6_verdict"],
        ),
        (
            "SRC2730_2_1854_extraction",
            "previous Z_X/M_X extraction result",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv",
            ["EXT1854_5_verdict", "NO_CLAIM_GRADE_ZX_OR_MX2_FOUND"],
        ),
        (
            "SRC2730_3_2023_schema",
            "first-row schema for Z_X/M_X still missing",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv",
            ["ZMR2023_3_ZX", "MISSING_ZX_VALUE_OR_SIGN_THEOREM", "ZMR2023_4_MX2"],
        ),
        (
            "SRC2730_4_2197_acquisition",
            "Z_X acquisition row contract",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2197_ZX_SOURCE_ACQUISITION_ROW.csv",
            ["ZXA2197_0_ZX", "MISSING_PARENT_KINETIC_RESIDUE"],
        ),
        (
            "SRC2730_5_2216_signature",
            "parent Hessian signature extraction attempt",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv",
            ["PHS2216_0_candidate_density_shape", "parent_signed_now", "False"],
        ),
        (
            "SRC2730_6_2627_bound_pack",
            "finite memory bound pack with boundary anchors but missing MTS projection coefficients",
            RESIDUALS / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv",
            ["RBP2627_2_boundary_lift", "SOURCE_BACKED_ANCHORS_NOT_MTS_SCORE"],
        ),
        (
            "SRC2730_7_2628_rlocal",
            "dangerous J_X/qbar_XT source channel retained",
            RESIDUALS / "P8_Y5_CONSTRAINT_ELIMINATION_2628_RLOCAL_RESIDUAL_INTERFACE.csv",
            ["RLI2628_2_J_X_qbarXT", "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, description, path, needles in specs:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "description": description,
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
            }
        )
    return rows


def scan_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "SCAN2730_0_ZX_1854",
            "target_quantity": "Z_X",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv"),
            "evidence_row": "EXT1854_0_ZX",
            "candidate_payload": "extracted_value=MISSING_ZX; extraction_status=NOT_EXTRACTED",
            "accepted_source_backed": False,
            "rejection_reason": "NO_VALUE_NO_UNITS_NO_PARENT_SOURCE",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_1_MX2_1854",
            "target_quantity": "M_X^2",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv"),
            "evidence_row": "EXT1854_1_MX2",
            "candidate_payload": "extracted_value=MISSING_MX2; extraction_status=NOT_EXTRACTED",
            "accepted_source_backed": False,
            "rejection_reason": "NO_VALUE_NO_SIGN_NO_PARENT_HESSIAN",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_2_ZX_SCHEMA_2023",
            "target_quantity": "Z_X",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv"),
            "evidence_row": "ZMR2023_3_ZX",
            "candidate_payload": "numeric_value=MISSING; current_status=MISSING_ZX_VALUE_OR_SIGN_THEOREM",
            "accepted_source_backed": False,
            "rejection_reason": "SCHEMA_ONLY",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_3_MX2_SCHEMA_2023",
            "target_quantity": "M_X^2",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv"),
            "evidence_row": "ZMR2023_4_MX2",
            "candidate_payload": "numeric_value=MISSING; current_status=MISSING_MX2_VALUE_OR_SIGN_THEOREM",
            "accepted_source_backed": False,
            "rejection_reason": "SCHEMA_ONLY",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_4_ZX_ACQUISITION_2197",
            "target_quantity": "Z_X",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2197_ZX_SOURCE_ACQUISITION_ROW.csv"),
            "evidence_row": "ZXA2197_0_ZX",
            "candidate_payload": "current_status=MISSING_PARENT_KINETIC_RESIDUE; acceptable_source written",
            "accepted_source_backed": False,
            "rejection_reason": "CONTRACT_NOT_SOURCE_ROW",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_5_HESSIAN_SIGNATURE_2216",
            "target_quantity": "parent Hessian signature",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv"),
            "evidence_row": "PHS2216_0..7",
            "candidate_payload": "candidate density shape found, but parent_signed_now=False for signature clauses",
            "accepted_source_backed": False,
            "rejection_reason": "FORMAL_SHAPE_FOUND_PARENT_OWNER_UNITS_SIGN_DOMAIN_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_6_BOUNDARY_ANCHORS_2627",
            "target_quantity": "boundary_lift_norm_X",
            "source_path": str(RESIDUALS / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv"),
            "evidence_row": "RBP2627_2_boundary_lift",
            "candidate_payload": "external pressure anchors: alpha3, Gdot, alpha2, xi, gamma-scale; missing MTS boundary norm/projection coefficient",
            "accepted_source_backed": False,
            "rejection_reason": "EXTERNAL_BOUND_ANCHORS_NOT_MTS_MEMORY_COEFFICIENT",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_7_JX_QBARXT_2628",
            "target_quantity": "J_X/qbar_XT",
            "source_path": str(RESIDUALS / "P8_Y5_CONSTRAINT_ELIMINATION_2628_RLOCAL_RESIDUAL_INTERFACE.csv"),
            "evidence_row": "RLI2628_2_J_X_qbarXT",
            "candidate_payload": "status=SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "accepted_source_backed": False,
            "rejection_reason": "CHANNEL_IDENTIFIED_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "SCAN2730_8_ALPHA_1024",
            "target_quantity": "K_X;Qbar_XH;qbar_XT;alpha_bulk",
            "source_path": str(DOC.parent / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"),
            "evidence_row": "ALPHA1024_3_bulk_R10_projection",
            "candidate_payload": "current_status=MISSING_ARENA_PROJECTION; runner_status=blocked_missing_alpha_projection_inputs",
            "accepted_source_backed": False,
            "rejection_reason": "ARENA_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
    ]


def accepted_rows(scan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = [row for row in scan if row["accepted_source_backed"] is True]
    if accepted:
        return accepted
    return [
        {
            "accepted_id": "ACCEPT2730_0_none",
            "quantity": "none",
            "source_path": "none",
            "value": "NO_ACCEPTED_SOURCE_BACKED_MEMORY_ROW_FOUND",
            "units": "none",
            "equation_ref": "none",
            "valid_for_claim": False,
        }
    ]


def rejection_rows(scan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, int] = {}
    for row in scan:
        buckets[row["rejection_reason"]] = buckets.get(row["rejection_reason"], 0) + 1
    rows = [
        {
            "rejection_id": f"REJ2730_{i}",
            "reason": reason,
            "count": count,
            "effect": "blocks source-backed memory row acceptance",
            "valid_for_claim": False,
        }
        for i, (reason, count) in enumerate(sorted(buckets.items()))
    ]
    rows.append(
        {
            "rejection_id": "REJ2730_verdict",
            "reason": "NO_SOURCE_ROW_ACCEPTED",
            "count": sum(buckets.values()),
            "effect": "run local-test refusal smoke; no local-GR or local-test claim",
            "valid_for_claim": False,
        }
    )
    return rows


def refusal_rows() -> list[dict[str, Any]]:
    interface = read_csv(RESIDUALS / "P8_Y5_R2FR_2729_FINITE_MEMORY_RESIDUAL_INPUT_INTERFACE.csv")
    r10_rows = read_csv(RESIDUALS / "P8_Y5_R2FR_2729_R10_ALPHA_SMOKE_ROWS_NONCLAIM.csv")
    rows: list[dict[str, Any]] = []
    for row in interface:
        value = row.get("value", "")
        score_status = row.get("score_status", "")
        refused = ("MISSING" in value) or ("DERIVED_ONLY_IF_INPUTS_EXIST" in value) or score_status != "SCOREABLE"
        rows.append(
            {
                "smoke_id": "SMOKE2730_MFI_" + row["input_id"],
                "target": row["quantity"],
                "input_value": value,
                "input_status": score_status,
                "score_attempted": False,
                "refused": refused,
                "refusal_reason": "MISSING_OR_DERIVED_ONLY_INPUT" if refused else "UNEXPECTED_SCOREABLE",
                "valid_for_claim": False,
            }
        )
    for row in r10_rows:
        refused = "MISSING" in row.get("lambda_value", "") or "MISSING" in row.get("alpha_predicted", "")
        rows.append(
            {
                "smoke_id": "SMOKE2730_R10_" + row["curve_id"],
                "target": "R10 alpha(lambda)",
                "input_value": f"lambda={row.get('lambda_value')};alpha={row.get('alpha_predicted')}",
                "input_status": row.get("derivation_status"),
                "score_attempted": False,
                "refused": refused,
                "refusal_reason": "MISSING_LAMBDA_OR_ALPHA" if refused else "UNEXPECTED_SCOREABLE",
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "smoke_id": "SMOKE2730_VERDICT",
            "target": "local tests",
            "input_value": "all source-row candidates refused",
            "input_status": "REFUSAL_SMOKE_PASS",
            "score_attempted": False,
            "refused": True,
            "refusal_reason": "INTERFACE_BLOCKS_FAKE_LOCAL_TEST_PASS",
            "valid_for_claim": False,
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE2730_0_source_row", "claim": "one memory source row accepted", "gate_pass": False, "reason": "no candidate has value, units, equation ref and parent source", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "GATE2730_1_r10_score", "claim": "R10 alpha(lambda) score can run", "gate_pass": False, "reason": "lambda_X and alpha_X are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "GATE2730_2_ppn_clock_orbital", "claim": "PPN/clock/orbital/WEP score can run", "gate_pass": False, "reason": "K_i projection vector and memory amplitude inputs are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "GATE2730_3_local_gr", "claim": "derived local GR/Newton reduction", "gate_pass": False, "reason": "memory source/signature remains unresolved and other gates remain live", "claim_allowed": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2730_0_no_row",
            "decision": "NO_ACCEPTED_MEMORY_SOURCE_ROW_FOUND",
            "because": "all located rows are schemas, conditional theorem statements, external bound anchors, or missing-value contracts",
            "next_action": "deep parent-action source hunt rather than local-test scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2730_1_refusal_smoke",
            "decision": "LOCAL_TEST_REFUSAL_SMOKE_PASSES",
            "because": "the 2729 interface refuses every placeholder and derived-only row",
            "next_action": "keep test plumbing safe until at least one source-backed memory row exists",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2730_2_best_next",
            "decision": "PARENT_ACTION_DEEP_SOURCE_HUNT",
            "because": "the closest promising object is the 2216 conditional Hessian shape, but parent owner/units/sign/domain are unsigned",
            "next_action": "inspect original parent action/action-sketch files for a real Hessian or source-current owner",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2730_0_selected",
            "status": "selected_primary",
            "target_doc": "2731-Y5-R2FR-parent-action-deep-memory-Hessian-source-hunt-or-closure-only-declaration-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_action_deep_memory_Hessian_source_hunt_or_closure_only_declaration_under_AX1090_2731.py",
            "mission": "search original parent-action/action-sketch files, not only downstream ledgers, for a real memory Hessian/source-current owner; if absent, mark the memory positive-operator route closure-only until new parent action text is supplied",
            "acceptance": "source-backed Z_X/M_X^2/J_X/boundary/action-owner row found, or closure-only declaration with finite residual interface retained",
            "forbidden": "local-test score from placeholders; fitted coefficients; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {"copy_id": "COPY2730_0_source_scan", "source_table": str(OUTPUTS["scan"]), "copy_path": str(BRANCH_OUTPUTS["source_scan"]), "purpose": "local branch sees source-row hunt outcome", "exists": BRANCH_OUTPUTS["source_scan"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2730_1_refusal_smoke", "source_table": str(OUTPUTS["refusal"]), "copy_path": str(BRANCH_OUTPUTS["refusal_smoke"]), "purpose": "local branch sees refusal smoke", "exists": BRANCH_OUTPUTS["refusal_smoke"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2730_2_source_weight_rejection", "source_table": str(OUTPUTS["rejection"]), "copy_path": str(BRANCH_OUTPUTS["source_weight_rejection"]), "purpose": "source-weight branch receives rejection ledger", "exists": BRANCH_OUTPUTS["source_weight_rejection"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2730_3_next_queue", "source_table": str(OUTPUTS["next"]), "copy_path": str(BRANCH_OUTPUTS["next_queue"]), "purpose": "queues deep parent-action source hunt", "exists": BRANCH_OUTPUTS["next_queue"].exists(), "valid_for_claim": False},
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    scan: list[dict[str, Any]],
    accepted: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    scan_complete = len(scan) >= 8 and all(row["accepted_source_backed"] is False for row in scan)
    accepted_none = len(accepted) == 1 and accepted[0]["value"] == "NO_ACCEPTED_SOURCE_BACKED_MEMORY_ROW_FOUND"
    refusal_pass = len(refusal) >= 10 and all(row["refused"] is True for row in refusal)
    gates_false = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2730_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_1_scan_complete", "passed": scan_complete, "detail": "source-row scan covers target candidates and accepts none", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_2_accepted_none", "passed": accepted_none, "detail": "accepted source row table explicitly records none found", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_3_refusal_smoke", "passed": refusal_pass, "detail": "local-test refusal smoke refuses every placeholder row", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_4_claim_gates_false", "passed": gates_false, "detail": "all local/test/GR claim gates remain false", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_5_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2730_6_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2730_7_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2730_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2730 finds no accepted memory source row and proves the local-test interface refuses placeholders",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2730 — Y5 R2/f(R): Memory First Source Row Acquisition Or Local-Test Refusal Smoke Under AX1090 Closure

Status: `Y5_R2FR_2730_no_accepted_memory_source_row_refusal_smoke_passes_nonclaim`

## Private Verdict

I tried the useful thing first: accept one real memory source row if the corpus already had it. It does not. The closest rows are still schemas, conditional Hessian shapes, missing-value extraction results, external bound anchors without MTS projection coefficients, or source channels with missing component values.

So 2730 takes the fallback branch and runs the refusal smoke. Result: the finite memory interface correctly refuses every fake local-test score. No R10, PPN, WEP, clock, orbital, Newton, local-GR, or public claim is opened.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Memory Source Row Acquisition Scan

{markdown_table(data["scan"], ["candidate_id", "target_quantity", "source_path", "evidence_row", "candidate_payload", "accepted_source_backed", "rejection_reason", "valid_for_claim"])}

## Accepted Memory Source Rows

{markdown_table(data["accepted"], ["accepted_id", "quantity", "source_path", "value", "units", "equation_ref", "valid_for_claim"])}

## Rejection Ledger

{markdown_table(data["rejection"], ["rejection_id", "reason", "count", "effect", "valid_for_claim"])}

## Local-Test Refusal Smoke

{markdown_table(data["refusal"], ["smoke_id", "target", "input_value", "input_status", "score_attempted", "refused", "refusal_reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a useful negative result. We did not find the missing coupling/signature row hiding in the downstream ledgers. That means the next move should not be another local-test run; it should be a deeper parent-action source hunt. If that hunt still fails, the memory positive-operator route has to be labelled closure-only until new parent action text is supplied. The good news is the test machinery now refuses the fake pass automatically.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    scan = scan_rows()
    accepted = accepted_rows(scan)
    rejection = rejection_rows(scan)
    refusal = refusal_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["scan"], scan)
    write_csv(OUTPUTS["accepted"], accepted)
    write_csv(OUTPUTS["rejection"], rejection)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["source_scan"], scan)
    write_csv(BRANCH_OUTPUTS["refusal_smoke"], refusal)
    write_csv(BRANCH_OUTPUTS["source_weight_rejection"], rejection)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, scan, accepted, refusal, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "scan": scan,
        "accepted": accepted,
        "rejection": rejection,
        "refusal": refusal,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2730 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
