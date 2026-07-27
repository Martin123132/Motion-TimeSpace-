from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3052"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3052-Y5-R2FR-source-frame-readout-lock-for-Gref-WPhi-or-dotG-numeric-coefficient-runner-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3052_00_3051_doc": ROOT / "3051-Y5-R2FR-source-frame-stress-test-of-topological-kappa-spine-or-first-dotG-coefficient-fill-under-AX1090.md",
    "SRC3052_01_3051_source_frame": RESIDUALS / "P8_Y5_R2FR_3051_SOURCE_FRAME_READOUT_STRESS.csv",
    "SRC3052_02_3051_topological": RESIDUALS / "P8_Y5_R2FR_3051_TOPOLOGICAL_STRESS_AND_COMPANION_AUDIT.csv",
    "SRC3052_03_3051_dotg_fill": RESIDUALS / "P8_Y5_R2FR_3051_DOTG_FIRST_COEFFICIENT_FILL_NONCLAIM.csv",
    "SRC3052_04_3051_next": RESIDUALS / "P8_Y5_R2FR_3051_NEXT_TARGET.csv",
    "SRC3052_05_dotg_target": DOTG_TARGET,
    "SRC3052_06_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3052_07_3050_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
    "SRC3052_08_3045_aw_law": RESIDUALS / "P8_Y5_R2FR_3045_AW_COEFFICIENT_RATIO_LAW.csv",
    "SRC3052_09_WPhi_not_signed": PARENT_ACTION / "W_equals_Phi_parent_readout_theorem_3042_NOT_SIGNED.csv",
    "SRC3052_10_source_readout_not_signed": PARENT_ACTION / "source_readout_lock_theorem_attempt_3036_NOT_SIGNED.csv",
    "SRC3052_11_same_coframe_clause": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
    "SRC3052_12_single_frame_gate": PARENT_ACTION / "single_observed_frame_parent_action_gate_2959_NOT_DERIVED.csv",
    "SRC3052_13_dotG_bound_source": RESIDUALS / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv",
    "SRC3052_14_dotG_projection_gate": PARENT_ACTION / "DotG_to_kappa_projection_gate_2933_NONCLAIM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3052_SOURCE_REGISTER.csv",
    "readout_candidate": RESIDUALS / "P8_Y5_R2FR_3052_GREF_WPHI_SOURCE_READOUT_LOCK_CANDIDATE.csv",
    "readout_gates": RESIDUALS / "P8_Y5_R2FR_3052_READOUT_LOCK_GATE_EVALUATION.csv",
    "aw_status": RESIDUALS / "P8_Y5_R2FR_3052_AW_NEWTON_LOCK_STATUS.csv",
    "dotg_runner": RESIDUALS / "P8_Y5_R2FR_3052_DOTG_NUMERIC_COEFFICIENT_RUNNER_RESULTS.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3052_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3052_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3052_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3052_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3052_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "readout_candidate_copy": PARENT_ACTION / "Gref_WPhi_source_readout_lock_candidate_3052_CONDITIONAL.csv",
    "readout_gates_copy": PARENT_ACTION / "readout_lock_gate_evaluation_3052_NOT_SIGNED.csv",
    "aw_status_copy": PARENT_ACTION / "AW_Newton_lock_status_3052_BLOCKED_NONCLAIM.csv",
    "dotg_runner_copy": LOCAL_BOUNDS / "dotG_numeric_coefficient_runner_3052_BLOCKED_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3052_WPHI_SOURCE_READOUT_THEOREM_OR_DOTG_VALUE_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str] | dict[str, Any]]) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "claim_active", "gate_passes_for_current_MTS"}
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def parse_numeric(value: str) -> float | None:
    stripped = value.strip()
    if "MISSING" in stripped.upper() or "ZERO_IF" in stripped.upper() or "DERIVED" in stripped.upper():
        return None
    if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", stripped):
        return float(stripped)
    return None


def extract_bound(value: str) -> float | None:
    match = re.search(r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)", value)
    if not match:
        return None
    return float(match.group(1))


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

readout_candidate_rows = [
    base(
        {
            "candidate_id": "LOCK3052_0_single_readout",
            "required_identity": "g_obs := g_matter := g_source := g_clock := g_orbit",
            "effect": "places matter, source, clocks, orbit and weak-field potential in one frame",
            "would_close": "delta_frame_source and frame ambiguity in dln_Geff_dt",
            "current_status": "CONDITIONAL_CLAUSE_EXISTS_NOT_ACTIVE",
        }
    ),
    base(
        {
            "candidate_id": "LOCK3052_1_WPhi",
            "required_identity": "W := Phi_metric in the same observed weak-field readout",
            "effect": "prevents a second potential denominator from surviving after G_ref lock",
            "would_close": "D_WPhi and A_W mismatch if G_ref also locks",
            "current_status": "NOT_SIGNED",
        }
    ),
    base(
        {
            "candidate_id": "LOCK3052_2_Gref",
            "required_identity": "G_ref := kappa_eff c^4/(8*pi) in the same source-normalized observed frame",
            "effect": "substitutes into A_W = kappa_eff c^4/(8*pi*G_ref)",
            "would_close": "A_W=1 conditionally",
            "current_status": "CONDITIONAL_NOT_ACTIVE",
        }
    ),
    base(
        {
            "candidate_id": "LOCK3052_3_Tobs",
            "required_identity": "T_obs is the Hilbert source obtained by varying S_matter[g_obs, psi]",
            "effect": "ties source normalization to the same equation that defines G_ref",
            "would_close": "source/readout mismatch and WEP-source charge if species/source labels are absent",
            "current_status": "NOT_SIGNED",
        }
    ),
]

readout_gate_rows = [
    base(
        {
            "gate_id": "RG3052_0_same_frame",
            "requirement": "one observed frame/coframe for all readouts",
            "candidate_result": "conditional same-coframe clause exists",
            "current_MTS_result": "NOT_ACTIVE_PARENT_DERIVED",
            "gate_passes_for_current_MTS": "false",
            "blocking_source": str(SOURCE_PATHS["SRC3052_11_same_coframe_clause"]),
        }
    ),
    base(
        {
            "gate_id": "RG3052_1_WPhi",
            "requirement": "W is retired or identified with Phi_metric",
            "candidate_result": "would make AW denominator unique",
            "current_MTS_result": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocking_source": str(SOURCE_PATHS["SRC3052_09_WPhi_not_signed"]),
        }
    ),
    base(
        {
            "gate_id": "RG3052_2_source",
            "requirement": "T_obs comes from the same Hilbert source variation",
            "candidate_result": "standard if S_matter[g_obs,psi] is the only source action",
            "current_MTS_result": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocking_source": str(SOURCE_PATHS["SRC3052_10_source_readout_not_signed"]),
        }
    ),
    base(
        {
            "gate_id": "RG3052_3_Gref",
            "requirement": "G_ref is a parent readout, not an independent fitted denominator",
            "candidate_result": "G_ref := kappa_eff c^4/(8*pi)",
            "current_MTS_result": "CONDITIONAL_NOT_ACTIVE",
            "gate_passes_for_current_MTS": "false",
            "blocking_source": str(SOURCE_PATHS["SRC3052_06_3050_gref"]),
        }
    ),
]

all_gates_pass = all(boolish(row["gate_passes_for_current_MTS"]) for row in readout_gate_rows)

aw_status_rows = [
    base(
        {
            "aw_id": "AW3052_0_ratio",
            "formula": "A_W = kappa_eff c^4/(8*pi*G_ref)",
            "candidate_lock": "if G_ref := kappa_eff c^4/(8*pi), then A_W=1",
            "current_status": "BLOCKED_READOUT_GATES_NOT_SIGNED",
            "passes_for_claim": "false",
            "reason": "same-frame W/Phi/T_obs/G_ref lock is conditional only",
        }
    ),
    base(
        {
            "aw_id": "AW3052_1_Newton",
            "formula": "nabla^2 Phi_metric = 4*pi*G_ref*rho",
            "candidate_lock": "weak-field limit of G_munu=kappa_eff T_munu",
            "current_status": "CONDITIONAL_ONLY",
            "passes_for_claim": "false",
            "reason": "source normalization and W/Phi readout remain not signed",
        }
    ),
]

dotg_rows = rows(DOTG_TARGET)
dotg_runner_rows: list[dict[str, Any]] = []
for index, row in enumerate(dotg_rows):
    candidate = row.get("candidate_value", row.get("predicted_value", ""))
    numeric_candidate = parse_numeric(candidate)
    bound_value = extract_bound(row.get("bound_or_target", ""))
    if numeric_candidate is not None and bound_value is not None:
        result = "PASS_NUMERIC_NONCLAIM" if abs(numeric_candidate) <= bound_value else "FAIL_NUMERIC_NONCLAIM"
        reason = f"abs({numeric_candidate}) <= {bound_value}" if abs(numeric_candidate) <= bound_value else f"abs({numeric_candidate}) > {bound_value}"
    else:
        result = "BLOCKED_MISSING_NUMERIC_DOTG_COEFFICIENT"
        reason = "candidate_value is not a numeric parent prediction or derived zero"
    dotg_runner_rows.append(
        base(
            {
                "run_id": f"DOTGRUN3052_{index}",
                "row_id": row.get("row_id", f"row_{index}"),
                "component_id": row.get("component_id", "P8_Geff_time_drift"),
                "candidate_value": candidate,
                "numeric_candidate": "" if numeric_candidate is None else numeric_candidate,
                "bound_or_target": row.get("bound_or_target", ""),
                "numeric_bound": "" if bound_value is None else bound_value,
                "runner_result": result,
                "reason": reason,
                "claim_effect": "no dotG pass claim",
            }
        )
    )

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3052_0_readout_lock",
            "claim": "same-frame G_ref/W/Phi/T_obs lock is active",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "all readout gates fail for current MTS",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3052_1_AW",
            "claim": "A_W=1 is claimable",
            "status": "NO_BLOCKED",
            "claim_active": "false",
            "reason": "candidate algebra works, current readout gates not signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3052_2_dotG",
            "claim": "dln_Geff_dt passes numeric bound",
            "status": "NO_NUMERIC_COEFFICIENT_MISSING",
            "claim_active": "false",
            "reason": "dotG runner found no numeric parent prediction or derived zero",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3052_0_lock",
            "question": "Can 3052 sign the readout lock?",
            "answer": "NO",
            "reason": "the candidate lock is written, but W/Phi/source/G_ref gates remain conditional/not signed",
            "action": "do not promote A_W/Newton",
        }
    ),
    base(
        {
            "decision_id": "DEC3052_1_dotG_runner",
            "question": "Does the dotG fallback runner score?",
            "answer": "NO",
            "reason": "target rows contain missing markers rather than numeric predictions",
            "action": "next target must derive W/Phi/source readout or fill real dotG coefficient",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3052_0_3053",
            "next_checkpoint": "3053-Y5-R2FR-WPhi-source-readout-theorem-or-real-dotG-coefficient-value-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WPhi_source_readout_theorem_or_real_dotG_coefficient_value_under_AX1090_3053.py",
            "mission": "try to prove W=Phi_metric and T_obs source readout from the candidate parent spine; if this fails, acquire or derive a real numeric dln_Geff_dt coefficient value rather than another placeholder",
            "starting_equation": "A_W=1 requires W=Phi_metric, T_obs from S_matter[g_obs,psi], and G_ref=kappa_eff c^4/(8*pi) in one frame",
            "claim_policy": "no Newton/local-GR claim until the readout theorem or a scored dotG coefficient exists",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["readout_candidate"], readout_candidate_rows)
write_csv(OUTPUTS["readout_gates"], readout_gate_rows)
write_csv(OUTPUTS["aw_status"], aw_status_rows)
write_csv(OUTPUTS["dotg_runner"], dotg_runner_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["readout_candidate"], BRANCH_OUTPUTS["readout_candidate_copy"])
copy_csv(OUTPUTS["readout_gates"], BRANCH_OUTPUTS["readout_gates_copy"])
copy_csv(OUTPUTS["aw_status"], BRANCH_OUTPUTS["aw_status_copy"])
copy_csv(OUTPUTS["dotg_runner"], BRANCH_OUTPUTS["dotg_runner_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3052 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["readout_candidate"],
    OUTPUTS["readout_gates"],
    OUTPUTS["aw_status"],
    OUTPUTS["dotg_runner"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]

validation_rows = [
    base({"validation_id": "VAL3052_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3052_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3052_02_readout_candidate_written", "passed": len(readout_candidate_rows) >= 4, "requirement": "same-frame readout lock candidate is written", "evidence": OUTPUTS["readout_candidate"].name}),
    base({"validation_id": "VAL3052_03_readout_gates_block", "passed": not all_gates_pass and all(not boolish(row["gate_passes_for_current_MTS"]) for row in readout_gate_rows), "requirement": "readout gates remain blocked for current MTS", "evidence": OUTPUTS["readout_gates"].name}),
    base({"validation_id": "VAL3052_04_aw_nonclaim", "passed": all(row["passes_for_claim"] == "false" for row in aw_status_rows), "requirement": "A_W/Newton lock is not promoted", "evidence": OUTPUTS["aw_status"].name}),
    base({"validation_id": "VAL3052_05_dotG_runner_blocks", "passed": len(dotg_runner_rows) >= 1 and all(row["runner_result"].startswith("BLOCKED") for row in dotg_runner_rows), "requirement": "dotG numeric runner blocks on missing predictions", "evidence": OUTPUTS["dotg_runner"].name}),
    base({"validation_id": "VAL3052_06_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active flags"}),
    base({"validation_id": "VAL3052_07_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "readout/dotG claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3052_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3052_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3052_10_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3052_11_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3053-"), "requirement": "next target selects WPhi source readout theorem or real dotG coefficient", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3052_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3052 - Source-Frame Readout Lock for Gref/WPhi or dotG Numeric Coefficient Runner

Status: `Y5_R2FR_3052_readout_lock_candidate_written_dotG_runner_blocked_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3052 writes the exact readout lock needed for the Newton coefficient:

`g_obs := g_matter := g_source := g_clock := g_orbit`

`W := Phi_metric`

`G_ref := kappa_eff c^4/(8*pi)`

`T_obs := -2/sqrt(-g_obs) delta S_matter[g_obs,psi]/delta g_obs`

If all four are active in one source-normalized observed frame, then:

`A_W = kappa_eff c^4/(8*pi*G_ref) = 1`

But 3052 cannot sign the lock for current MTS. The algebra is good; the parent readout adoption is not yet proven. The fallback `dotG` runner also blocks because the target rows still contain missing parent coefficients rather than numeric predictions.

## Readout Lock Candidate

{md_table(readout_candidate_rows, ["candidate_id", "required_identity", "effect", "would_close", "current_status"])}

## Readout Gate Evaluation

{md_table(readout_gate_rows, ["gate_id", "requirement", "candidate_result", "current_MTS_result", "gate_passes_for_current_MTS", "blocking_source"])}

## AW/Newton Lock Status

{md_table(aw_status_rows, ["aw_id", "formula", "candidate_lock", "current_status", "passes_for_claim", "reason"])}

## dotG Numeric Runner

{md_table(dotg_runner_rows, ["run_id", "row_id", "candidate_value", "numeric_candidate", "bound_or_target", "numeric_bound", "runner_result", "reason"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3052 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: readout lock candidate written; dotG numeric runner blocked nonclaim")
