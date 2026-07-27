from __future__ import annotations

import csv
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

CHECKPOINT = "3061"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3061-Y5-R2FR-EH-common-source-dominance-theorem-or-Delta-kST-bound-schema-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3061_00_3060_doc": ROOT / "3060-Y5-R2FR-epsilon-Wchannel-metric-response-split-kS-kT-or-common-mode-theorem-under-AX1090.md",
    "SRC3061_01_3060_common_mode": RESIDUALS / "P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv",
    "SRC3061_02_3060_delta": RESIDUALS / "P8_Y5_R2FR_3060_DELTA_KST_RESIDUAL_CONTRACT.csv",
    "SRC3061_03_3060_next": RESIDUALS / "P8_Y5_R2FR_3060_NEXT_TARGET.csv",
    "SRC3061_04_local_action_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3061_05_EH_impact": RESIDUALS / "P8_Y5_PARENT_EH_1512_NEWTON_PPN_IMPACT.csv",
    "SRC3061_06_EH_synthesis": RESIDUALS / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PPN_COMPONENT_FILL_LEDGER.csv",
    "SRC3061_07_GR_left_gate": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv",
    "SRC3061_08_hilbert": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "SRC3061_09_W_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_OWNER_GATE_EVALUATION.csv",
    "SRC3061_10_absorption": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "SRC3061_11_extra_silence": RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv",
    "SRC3061_12_extra_response": RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv",
    "SRC3061_13_ppn_kernel": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3061_14_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3061_SOURCE_REGISTER.csv",
    "dominance_gate": RESIDUALS / "P8_Y5_R2FR_3061_EH_COMMON_SOURCE_DOMINANCE_GATE.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_3061_DELTA_KST_ZERO_THEOREM_ATTEMPT.csv",
    "bound_schema": RESIDUALS / "P8_Y5_R2FR_3061_DELTA_KST_EPSILON_BOUND_SCHEMA.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3061_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3061_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3061_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3061_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3061_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "dominance_gate_copy": PARENT_ACTION / "EH_common_source_dominance_gate_3061_NOT_SIGNED.csv",
    "theorem_attempt_copy": PARENT_ACTION / "Delta_kST_zero_theorem_attempt_3061_CONDITIONAL_NOT_SIGNED.csv",
    "bound_schema_copy": LOCAL_BOUNDS / "Delta_kST_epsilon_bound_schema_3061_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3061_EH_EXTRA_SILENCE_OR_DELTA_KST_BOUND_INPUTS_NEXT_NONCLAIM.csv",
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
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "gate_passes_for_current_MTS",
        "theorem_active",
        "bound_ready",
    }
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


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


dotg_rows_before = rows(DOTG_TARGET)

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

dominance_gate_rows = [
    base(
        {
            "gate_id": "DOM3061_0_EH_operator",
            "requirement": "EH spin-2 metric operator dominates the local weak-field response",
            "current_status": "BLOCKED_STILL_MARKED_BY_CORPUS",
            "gate_passes_for_current_MTS": "false",
            "would_buy": "same GR metric response operator for temporal and spatial potentials",
            "blocker": "EH impact rows still say Newton/PPN are blocked until operator/source branch is owned",
            "source_path": str(SOURCE_PATHS["SRC3061_05_EH_impact"]),
        }
    ),
    base(
        {
            "gate_id": "DOM3061_1_common_Hilbert_source",
            "requirement": "same Hilbert source T_obs from S_matter[g_obs,psi] sources both weak-field equations",
            "current_status": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "would_buy": "epsilon_Wchan can only be common source normalization, not a spatial/lapse split",
            "blocker": "Hilbert source descent remains unsigned",
            "source_path": str(SOURCE_PATHS["SRC3061_08_hilbert"]),
        }
    ),
    base(
        {
            "gate_id": "DOM3061_2_extra_field_silence",
            "requirement": "extra motion/time/domain/memory/range fields have no linear local metric-response source",
            "current_status": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "would_buy": "prevents anisotropic/non-EH response generating Delta_kST",
            "blocker": "extra-sector silence remains audit/certificate level, not parent theorem",
            "source_path": str(SOURCE_PATHS["SRC3061_11_extra_silence"]),
        }
    ),
    base(
        {
            "gate_id": "DOM3061_3_W_metric_readout",
            "requirement": "W is retired as Phi_metric[g_obs] and not an independent channel",
            "current_status": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "would_buy": "prevents W-channel response from becoming a separate spatial/lapse kernel",
            "blocker": "W owner gates remain blocked",
            "source_path": str(SOURCE_PATHS["SRC3061_09_W_owner"]),
        }
    ),
    base(
        {
            "gate_id": "DOM3061_4_gauge_denominator",
            "requirement": "PPN gauge, G_ref, source mass, and orbital GM denominator are locked",
            "current_status": "BLOCKED",
            "gate_passes_for_current_MTS": "false",
            "would_buy": "allows Delta_kST*epsilon_Wchan to be interpreted physically if nonzero",
            "blocker": "no-GM-absorption/gauge gates remain blocked",
            "source_path": str(SOURCE_PATHS["SRC3061_10_absorption"]),
        }
    ),
]

theorem_attempt_rows = [
    base(
        {
            "theorem_id": "DKZERO3061_0_if_all_gates",
            "statement": "If DOM3061_0..4 pass, epsilon_Wchan is a pure common-mode source normalization inside EH response.",
            "derivation": "EH common-source dominance makes k_T=k_S=1; W/Hilbert/gauge locks prevent independent channel split",
            "result": "Delta_kST=0",
            "theorem_active": "false",
            "missing_for_claim": "ALL_DOMINANCE_GATES_CURRENTLY_BLOCK",
        }
    ),
    base(
        {
            "theorem_id": "DKZERO3061_1_current_status",
            "statement": "Current MTS does not pass EH/common-source dominance gates.",
            "derivation": "source files explicitly keep EH, Hilbert source, W owner, extra silence and PPN gauge locks unsigned",
            "result": "Delta_kST_zero_not_claimed",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_PARENT_EH_COMMON_SOURCE_DOMINANCE",
        }
    ),
    base(
        {
            "theorem_id": "DKZERO3061_2_bound_fallback",
            "statement": "If the zero theorem cannot be signed, the physical first-order gamma residual is Delta_kST*epsilon_Wchan.",
            "derivation": "combine 3060 gamma bridge with current live residuals",
            "result": "bound_schema_required",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_NUMERIC_DELTA_KST; MISSING_NUMERIC_EPSILON_WCHAN; MISSING_PPN_DENOMINATOR_LOCK",
        }
    ),
]

bound_schema_rows = [
    base(
        {
            "bound_id": "DKB3061_0_schema",
            "quantity": "gamma_minus_1_from_epsilon_channel",
            "formula": "gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)",
            "needed_inputs": "Delta_kST_zero_or_numeric; epsilon_Wchan_zero_or_numeric; PPN denominator/gauge lock; gamma comparator",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "bound_ready": "false",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "bound_id": "DKB3061_1_zero_route",
            "quantity": "Delta_kST",
            "formula": "Delta_kST=0 if EH/common-source dominance gates pass",
            "needed_inputs": "DOM3061_0..4 active",
            "current_status": "BLOCKED_ZERO_ROUTE",
            "bound_ready": "false",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "bound_id": "DKB3061_2_numeric_route",
            "quantity": "Delta_kST*epsilon_Wchan",
            "formula": "abs(Delta_kST*epsilon_Wchan) <= gamma_bound after gauge/denominator lock",
            "needed_inputs": "numeric/source-backed Delta_kST; numeric/source-backed epsilon_Wchan; no-cancellation policy",
            "current_status": "MISSING_NUMERIC_PRODUCT",
            "bound_ready": "false",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "bound_id": "DKB3061_3_guard",
            "quantity": "PPN gamma comparator",
            "formula": "external gamma bound constrains only after physical projection exists",
            "needed_inputs": "do not use bound to define Delta_kST or epsilon_Wchan",
            "current_status": "GUARD_ACTIVE",
            "bound_ready": "false",
            "valid_for_claim": "false",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3061_0_EH_dominance",
            "claim": "EH common-source dominance is active",
            "status": "NO_GATES_BLOCK",
            "claim_active": "false",
            "reason": "all dominance gates are blocked or unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3061_1_Delta_kST_zero",
            "claim": "Delta_kST=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "zero theorem depends on unsigned dominance gates",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3061_2_bound_ready",
            "claim": "Delta_kST*epsilon_Wchan is bound-ready",
            "status": "NO_SCHEMA_ONLY",
            "claim_active": "false",
            "reason": "numeric/product and denominator/gauge lock missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3061_3_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "3061 identifies the exact dominance gate but does not close it",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3061_0_zero",
            "question": "Can 3061 sign Delta_kST=0?",
            "answer": "NO",
            "reason": "EH operator dominance/common Hilbert source/extra silence/W owner/gauge locks all remain unsigned",
            "action": "do not claim gamma closure",
        }
    ),
    base(
        {
            "decision_id": "DEC3061_1_best_route",
            "question": "Best next route?",
            "answer": "ATTACK_DOMINANCE_GATES_IN_ORDER",
            "reason": "a proof of EH common-source dominance is stronger than a weak bound schema",
            "action": "start with EH operator dominance and extra-field silence, because those are the largest unclosed gates",
        }
    ),
    base(
        {
            "decision_id": "DEC3061_2_fallback",
            "question": "What if derivation fails?",
            "answer": "BOUND_PRODUCT",
            "reason": "Delta_kST*epsilon_Wchan is now a precise physical gamma residual product",
            "action": "only build numeric bound rows after product inputs exist",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3061_0_3062",
            "next_checkpoint": "3062-Y5-R2FR-EH-operator-dominance-and-extra-field-silence-or-Delta-kST-input-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_EH_operator_dominance_and_extra_field_silence_or_Delta_kST_input_fill_under_AX1090_3062.py",
            "mission": "try to prove EH operator dominance and extra-field silence for the local weak-field branch; if not, fill nonclaim Delta_kST input rows",
            "starting_equation": "Delta_kST=0 requires EH common-source dominance; otherwise gamma_minus_1=Delta_kST*epsilon_Wchan",
            "claim_policy": "no local-GR/PPN claim until EH dominance or numeric Delta_kST inputs are sourced",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["dominance_gate"], dominance_gate_rows)
write_csv(OUTPUTS["theorem_attempt"], theorem_attempt_rows)
write_csv(OUTPUTS["bound_schema"], bound_schema_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["dominance_gate"], BRANCH_OUTPUTS["dominance_gate_copy"])
copy_csv(OUTPUTS["theorem_attempt"], BRANCH_OUTPUTS["theorem_attempt_copy"])
copy_csv(OUTPUTS["bound_schema"], BRANCH_OUTPUTS["bound_schema_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3061 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["dominance_gate"],
    OUTPUTS["theorem_attempt"],
    OUTPUTS["bound_schema"],
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
dotg_rows_after = rows(DOTG_TARGET)

all_gates_block = all(row["gate_passes_for_current_MTS"] == "false" for row in dominance_gate_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
all_bounds_nonready = all(row["bound_ready"] == "false" for row in bound_schema_rows)
all_theorems_inactive = all(row["theorem_active"] == "false" for row in theorem_attempt_rows)

validation_rows = [
    base({"validation_id": "VAL3061_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3061_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3061_02_dominance_gates_block", "passed": all_gates_block, "requirement": "EH/common-source dominance gates block current MTS", "evidence": OUTPUTS["dominance_gate"].name}),
    base({"validation_id": "VAL3061_03_theorem_inactive", "passed": all_theorems_inactive, "requirement": "Delta_kST zero theorem remains inactive", "evidence": OUTPUTS["theorem_attempt"].name}),
    base({"validation_id": "VAL3061_04_bound_schema_nonready", "passed": all_bounds_nonready, "requirement": "Delta_kST epsilon bound schema remains nonready", "evidence": OUTPUTS["bound_schema"].name}),
    base({"validation_id": "VAL3061_05_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3061_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3061" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3061 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3061_07_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3061_08_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3061_09_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3061_10_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3062-"), "requirement": "next target selects EH dominance/extra silence or Delta_kST input fill", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3061_11_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3061 - EH Common-Source Dominance Theorem or Delta kST Bound Schema

Status: `Y5_R2FR_3061_EH_common_source_dominance_gates_block_Delta_kST_bound_schema_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3061 tries to sign the theorem that would make the local PPN gamma problem go away:

`Delta_kST = k_S-k_T = 0`

This would follow if the local branch has EH metric-operator dominance, a common Hilbert source, extra-field silence, W retired as `Phi_metric`, and a fixed PPN gauge/denominator.

Current MTS does **not** pass those gates yet. The corpus still marks EH/PPN as blocked, Hilbert source descent unsigned, W ownership unsigned, extra-sector silence unproven, and PPN denominator/gauge lock blocked.

So 3061 keeps the exact residual product live:

`gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)`.

No local-GR/PPN claim is active.

## EH Common-Source Dominance Gate

{md_table(dominance_gate_rows, ["gate_id", "requirement", "current_status", "gate_passes_for_current_MTS", "would_buy", "blocker"])}

## Delta kST Zero Theorem Attempt

{md_table(theorem_attempt_rows, ["theorem_id", "statement", "derivation", "result", "theorem_active", "missing_for_claim"])}

## Delta kST Epsilon Bound Schema

{md_table(bound_schema_rows, ["bound_id", "quantity", "formula", "needed_inputs", "current_status", "bound_ready"])}

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
    raise SystemExit(f"3061 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: EH dominance gates block; Delta_kST bound schema nonclaim")
