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

CHECKPOINT = "3060"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3060-Y5-R2FR-epsilon-Wchannel-metric-response-split-kS-kT-or-common-mode-theorem-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3060_00_3059_doc": ROOT / "3059-Y5-R2FR-no-GM-absorption-denominator-lock-or-epsilon-Wchannel-gamma-slip-kernel-under-AX1090.md",
    "SRC3060_01_3059_denominator": RESIDUALS / "P8_Y5_R2FR_3059_NO_GM_ABSORPTION_DENOMINATOR_LOCK_ATTEMPT.csv",
    "SRC3060_02_3059_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3059_EPSILON_GAMMA_SLIP_KERNEL_FORMULA.csv",
    "SRC3060_03_3059_response_split": RESIDUALS / "P8_Y5_R2FR_3059_METRIC_RESPONSE_SPLIT_REQUIREMENTS.csv",
    "SRC3060_04_3059_next": RESIDUALS / "P8_Y5_R2FR_3059_NEXT_TARGET.csv",
    "SRC3060_05_3057_first_K": RESIDUALS / "P8_Y5_R2FR_3057_FIRST_K_EPSILON_COEFFICIENTS.csv",
    "SRC3060_06_local_action_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3060_07_EH_impact": RESIDUALS / "P8_Y5_PARENT_EH_1512_NEWTON_PPN_IMPACT.csv",
    "SRC3060_08_GR_left_gate": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv",
    "SRC3060_09_PPN_metric_contract": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
    "SRC3060_10_PPN_source_gates": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
    "SRC3060_11_3015_PPN_kernel": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3060_12_3016_PPN_first_kernel": RESIDUALS / "P8_Y5_R2FR_3016_PPN_FIRST_KERNEL_ROWS.csv",
    "SRC3060_13_3055_epsilon": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "SRC3060_14_3056_grammar": RESIDUALS / "P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv",
    "SRC3060_15_3058_absorption_gate": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "SRC3060_16_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3060_SOURCE_REGISTER.csv",
    "common_mode": RESIDUALS / "P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv",
    "kst_split": RESIDUALS / "P8_Y5_R2FR_3060_KS_KT_RESPONSE_SPLIT_LEDGER.csv",
    "delta_contract": RESIDUALS / "P8_Y5_R2FR_3060_DELTA_KST_RESIDUAL_CONTRACT.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3060_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3060_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3060_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3060_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3060_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "common_mode_copy": PARENT_ACTION / "common_mode_metric_response_theorem_attempt_3060_CONDITIONAL_NOT_SIGNED.csv",
    "kst_split_copy": LOCAL_BOUNDS / "kS_kT_response_split_ledger_3060_NONCLAIM.csv",
    "delta_contract_copy": LOCAL_BOUNDS / "Delta_kST_residual_contract_3060_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3060_EH_COMMON_SOURCE_DOMINANCE_OR_DELTA_KST_BOUND_NEXT_NONCLAIM.csv",
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
        "theorem_active",
        "response_ready",
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

common_mode_rows = [
    base(
        {
            "theorem_id": "CMT3060_0_assumptions",
            "piece": "common-mode assumptions",
            "statement": "Assume EH metric operator dominance, universal Hilbert source, no extra scalar/vector/tensor local source, fixed observed gauge, and epsilon_Wchan only multiplies the common source normalization.",
            "derivation": "under these assumptions epsilon enters the same linearized metric equation source for temporal and spatial weak-field responses",
            "result": "ASSUMPTIONS_EXPLICIT",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_EH_DOMINANCE; MISSING_HILBERT_SOURCE_DESCENT; MISSING_EXTRA_FIELD_SILENCE; MISSING_GAUGE_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3060_06_local_action_blocks"]),
        }
    ),
    base(
        {
            "theorem_id": "CMT3060_1_EH_response",
            "piece": "EH common response",
            "statement": "For the EH weak-field branch, a common multiplicative source normalization rescales both Phi and Psi before calibrated U is fixed.",
            "derivation": "the same source amplitude appears in the linearized g00 and gij constraints; the ratio Psi/Phi remains one if no anisotropic/non-EH residual is present",
            "result": "k_T=1 and k_S=1 under EH/common-source assumptions",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_PARENT_P_EQUALS_1_OR_EH_DOMINANCE",
            "source_path": str(SOURCE_PATHS["SRC3060_08_GR_left_gate"]),
        }
    ),
    base(
        {
            "theorem_id": "CMT3060_2_gamma_zero",
            "piece": "gamma slip cancellation",
            "statement": "If k_S=k_T=1 then gamma-1=(k_S-k_T)epsilon_Wchan=0 at first order.",
            "derivation": "substitute common-mode response into 3059 symbolic gamma kernel",
            "result": "K_gamma_epsilon=0 conditionally",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_RESPONSE_SPLIT_THEOREM_ACTIVE_FOR_CURRENT_MTS",
            "source_path": str(SOURCE_PATHS["SRC3060_02_3059_gamma_kernel"]),
        }
    ),
    base(
        {
            "theorem_id": "CMT3060_3_failure_modes",
            "piece": "when common-mode fails",
            "statement": "If epsilon couples to extra fields, anisotropic stress, readout gauge, shadow frame, or non-EH operator terms, k_S-k_T may be nonzero.",
            "derivation": "any term that changes spatial curvature response without the same temporal response produces gamma slip",
            "result": "Delta_kST residual required",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_EXTRA_FIELD_SILENCE_AND_READOUT_GAUGE",
            "source_path": str(SOURCE_PATHS["SRC3060_11_3015_PPN_kernel"]),
        }
    ),
    base(
        {
            "theorem_id": "CMT3060_4_verdict",
            "piece": "3060 theorem verdict",
            "statement": "The common-mode theorem is coherent and probably the right local-GR route, but current MTS has not signed EH dominance/common Hilbert source/extra-field silence.",
            "derivation": "therefore k_S=k_T remains conditional, not an active PPN pass",
            "result": "CONDITIONAL_NOT_SIGNED",
            "theorem_active": "false",
            "missing_for_claim": "MISSING_PARENT_EH_COMMON_SOURCE_DOMINANCE",
            "source_path": str(SOURCE_PATHS["SRC3060_07_EH_impact"]),
        }
    ),
]

kst_split_rows = [
    base(
        {
            "split_id": "KST3060_0_common_mode",
            "case": "EH common-source response",
            "k_T": "1",
            "k_S": "1",
            "k_S_minus_k_T": "0",
            "status": "CONDITIONAL_THEOREM_CASE",
            "response_ready": "false",
            "blocker": "EH/common-source assumptions not signed",
        }
    ),
    base(
        {
            "split_id": "KST3060_1_lapse_only_countercase",
            "case": "temporal response only",
            "k_T": "1",
            "k_S": "0",
            "k_S_minus_k_T": "-1",
            "status": "DIAGNOSTIC_COUNTERCASE",
            "response_ready": "false",
            "blocker": "not claimed; shows why response split matters",
        }
    ),
    base(
        {
            "split_id": "KST3060_2_spatial_only_countercase",
            "case": "spatial response only",
            "k_T": "0",
            "k_S": "1",
            "k_S_minus_k_T": "1",
            "status": "DIAGNOSTIC_COUNTERCASE",
            "response_ready": "false",
            "blocker": "not claimed; shows why response split matters",
        }
    ),
    base(
        {
            "split_id": "KST3060_3_current_MTS",
            "case": "current MTS active branch",
            "k_T": "MISSING_PARENT_RESPONSE",
            "k_S": "MISSING_PARENT_RESPONSE",
            "k_S_minus_k_T": "Delta_kST",
            "status": "MISSING_RESPONSE_SPLIT",
            "response_ready": "false",
            "blocker": "parent weak-field metric response not derived",
        }
    ),
]

delta_contract_rows = [
    base(
        {
            "residual_id": "DKST3060_0_definition",
            "symbol": "Delta_kST",
            "definition": "Delta_kST := k_S-k_T",
            "observable_link": "gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_RESPONSE_SPLIT",
            "valid_for_claim": "false",
            "next_action": "prove Delta_kST=0 by EH common-source dominance or derive numeric/source-backed k_S,k_T",
        }
    ),
    base(
        {
            "residual_id": "DKST3060_1_zero_condition",
            "symbol": "Delta_kST=0",
            "definition": "holds if epsilon_Wchan is pure common-mode Hilbert source normalization under EH operator dominance",
            "observable_link": "no first-order gamma slip from epsilon_Wchan",
            "units": "dimensionless",
            "current_value": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
            "next_action": "derive EH/common-source dominance from parent action",
        }
    ),
    base(
        {
            "residual_id": "DKST3060_2_bound_condition",
            "symbol": "Delta_kST * epsilon_Wchan",
            "definition": "if common-mode theorem fails, the product must be bounded against gamma_minus_1",
            "observable_link": "Cassini-style gamma comparator only after source/gauge/bound provenance is locked",
            "units": "dimensionless",
            "current_value": "NO_NUMERIC_PRODUCT",
            "valid_for_claim": "false",
            "next_action": "do not score until Delta_kST and epsilon_Wchan have source-backed values or bounds",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3060_0_common_mode",
            "claim": "epsilon_Wchan is pure common-mode metric response",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "requires EH dominance, Hilbert source descent, and extra-field silence",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3060_1_gamma_zero",
            "claim": "epsilon_Wchan gives zero first-order gamma slip",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "k_S=k_T is a conditional theorem case, not active current MTS",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3060_2_gamma_bound",
            "claim": "Delta_kST*epsilon_Wchan passes PPN gamma bounds",
            "status": "NO_NO_NUMERIC_PRODUCT",
            "claim_active": "false",
            "reason": "neither Delta_kST nor epsilon_Wchan is source-backed numeric",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3060_3_local_GR",
            "claim": "local GR/Newton PPN branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "EH/common-source dominance remains the next theorem gate",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3060_0_theorem",
            "question": "Can 3060 prove k_S=k_T?",
            "answer": "YES_CONDITIONALLY",
            "reason": "EH common-source response gives k_S=k_T=1 and cancels first-order gamma slip",
            "action": "record theorem shape but do not promote claim",
        }
    ),
    base(
        {
            "decision_id": "DEC3060_1_current_MTS",
            "question": "Does current MTS activate the common-mode theorem?",
            "answer": "NO",
            "reason": "EH dominance/common Hilbert source/extra-field silence are not parent-signed",
            "action": "carry Delta_kST residual",
        }
    ),
    base(
        {
            "decision_id": "DEC3060_2_next",
            "question": "Best next target?",
            "answer": "EH_COMMON_SOURCE_DOMINANCE",
            "reason": "proving this would set Delta_kST=0 and remove epsilon_Wchan from first-order gamma",
            "action": "build 3061 EH dominance/common-source theorem or Delta_kST bound schema",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3060_0_3061",
            "next_checkpoint": "3061-Y5-R2FR-EH-common-source-dominance-theorem-or-Delta-kST-bound-schema-under-AX1090.md",
            "script": "scripts/Y5_R2FR_EH_common_source_dominance_theorem_or_Delta_kST_bound_schema_under_AX1090_3061.py",
            "mission": "try to prove EH operator dominance plus common Hilbert source makes Delta_kST=0; if not, build nonclaim Delta_kST*epsilon_Wchan bound schema",
            "starting_equation": "gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)",
            "claim_policy": "no PPN/local-GR claim until Delta_kST is parent-zero or source-backed bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["common_mode"], common_mode_rows)
write_csv(OUTPUTS["kst_split"], kst_split_rows)
write_csv(OUTPUTS["delta_contract"], delta_contract_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["common_mode"], BRANCH_OUTPUTS["common_mode_copy"])
copy_csv(OUTPUTS["kst_split"], BRANCH_OUTPUTS["kst_split_copy"])
copy_csv(OUTPUTS["delta_contract"], BRANCH_OUTPUTS["delta_contract_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3060 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["common_mode"],
    OUTPUTS["kst_split"],
    OUTPUTS["delta_contract"],
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

has_common_mode_case = any(row["k_S_minus_k_T"] == "0" and row["status"] == "CONDITIONAL_THEOREM_CASE" for row in kst_split_rows)
has_delta_contract = any(row["symbol"] == "Delta_kST" for row in delta_contract_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
theorem_not_active = all(row["theorem_active"] == "false" for row in common_mode_rows)

validation_rows = [
    base({"validation_id": "VAL3060_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3060_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3060_02_common_mode_conditional", "passed": has_common_mode_case and theorem_not_active, "requirement": "common-mode kS=kT case is recorded but not active", "evidence": OUTPUTS["common_mode"].name}),
    base({"validation_id": "VAL3060_03_delta_contract", "passed": has_delta_contract, "requirement": "Delta_kST residual contract is explicit", "evidence": OUTPUTS["delta_contract"].name}),
    base({"validation_id": "VAL3060_04_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3060_05_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3060" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3060 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3060_06_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3060_07_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3060_08_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3060_09_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3061-"), "requirement": "next target selects EH common-source dominance or Delta_kST bound schema", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3060_10_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3060 - Epsilon W-Channel Metric Response Split kS-kT or Common-Mode Theorem

Status: `Y5_R2FR_3060_common_mode_kS_equals_kT_conditional_Delta_kST_named_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3060 gets a clean conditional result.

If `epsilon_Wchan` is only a common multiplicative Hilbert-source normalization inside an EH-dominated local metric operator, then it changes temporal and spatial weak-field response equally:

`k_T = 1`

`k_S = 1`

Therefore:

`k_S-k_T = 0`

and:

`gamma_minus_1 = (k_S-k_T) epsilon_Wchan = 0`

at first order.

That is the good route: epsilon can be real internally while still producing no first-order PPN gamma slip if the metric response is common-mode.

But this is **not claimed for current MTS**. EH dominance, Hilbert common-source descent, extra-field silence, gauge lock, and readout lock are still not parent-signed. So 3060 names the residual:

`Delta_kST := k_S-k_T`

Current physical gamma bridge:

`gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)`.

## Common-Mode Metric Response Theorem Attempt

{md_table(common_mode_rows, ["theorem_id", "piece", "statement", "derivation", "result", "theorem_active", "missing_for_claim"])}

## kS/kT Response Split Ledger

{md_table(kst_split_rows, ["split_id", "case", "k_T", "k_S", "k_S_minus_k_T", "status", "response_ready", "blocker"])}

## Delta kST Residual Contract

{md_table(delta_contract_rows, ["residual_id", "symbol", "definition", "observable_link", "current_value", "next_action"])}

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
    raise SystemExit(f"3060 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: common-mode theorem conditional; Delta_kST residual named nonclaim")
