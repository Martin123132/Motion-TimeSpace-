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

CHECKPOINT = "3059"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3059-Y5-R2FR-no-GM-absorption-denominator-lock-or-epsilon-Wchannel-gamma-slip-kernel-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3059_00_3058_doc": ROOT / "3058-Y5-R2FR-epsilon-Wchannel-source-normalization-to-PPN-projection-or-parent-type-system-derivation-under-AX1090.md",
    "SRC3059_01_3058_local_projection": RESIDUALS / "P8_Y5_R2FR_3058_EPSILON_TO_LOCAL_NEWTON_PROJECTION.csv",
    "SRC3059_02_3058_absorption_gate": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "SRC3059_03_3058_ppn_projection": RESIDUALS / "P8_Y5_R2FR_3058_PPN_PROJECTION_ATTEMPT.csv",
    "SRC3059_04_3058_next": RESIDUALS / "P8_Y5_R2FR_3058_NEXT_TARGET.csv",
    "SRC3059_05_3057_first_K": RESIDUALS / "P8_Y5_R2FR_3057_FIRST_K_EPSILON_COEFFICIENTS.csv",
    "SRC3059_06_3055_epsilon": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "SRC3059_07_ppn_metric_contract": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
    "SRC3059_08_ppn_source_gates": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
    "SRC3059_09_3015_ppn_kernel": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3059_10_3016_first_kernel": RESIDUALS / "P8_Y5_R2FR_3016_PPN_FIRST_KERNEL_ROWS.csv",
    "SRC3059_11_2746_coeff": RESIDUALS / "P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv",
    "SRC3059_12_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3059_13_3052_readout_gates": RESIDUALS / "P8_Y5_R2FR_3052_READOUT_LOCK_GATE_EVALUATION.csv",
    "SRC3059_14_3054_w_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_PARENT_OWNER_CLAUSE.csv",
    "SRC3059_15_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3059_SOURCE_REGISTER.csv",
    "denominator_lock": RESIDUALS / "P8_Y5_R2FR_3059_NO_GM_ABSORPTION_DENOMINATOR_LOCK_ATTEMPT.csv",
    "gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3059_EPSILON_GAMMA_SLIP_KERNEL_FORMULA.csv",
    "response_split": RESIDUALS / "P8_Y5_R2FR_3059_METRIC_RESPONSE_SPLIT_REQUIREMENTS.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3059_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3059_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3059_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3059_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3059_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "denominator_lock_copy": LOCAL_BOUNDS / "no_GM_absorption_denominator_lock_attempt_3059_NOT_SIGNED.csv",
    "gamma_kernel_copy": LOCAL_BOUNDS / "epsilon_gamma_slip_kernel_formula_3059_SYMBOLIC_NONCLAIM.csv",
    "response_split_copy": LOCAL_BOUNDS / "metric_response_split_requirements_3059_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3059_METRIC_RESPONSE_SPLIT_OR_DENOMINATOR_LOCK_NEXT_NONCLAIM.csv",
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
        "kernel_ready",
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

denominator_lock_rows = [
    base(
        {
            "lock_id": "DLOCK3059_0_Gref",
            "requirement": "G_ref is parent-owned as kappa_eff*c^4/(8*pi), not fitted from orbital GM",
            "current_status": "CONDITIONAL_NOT_ACTIVE",
            "gate_passes_for_current_MTS": "false",
            "if_passed": "epsilon_Wchan source rescaling can be compared to an independent denominator",
            "blocker": "G_ref/readout lock is candidate only",
            "source_path": str(SOURCE_PATHS["SRC3059_12_3050_gref"]),
        }
    ),
    base(
        {
            "lock_id": "DLOCK3059_1_source_mass",
            "requirement": "M_source comes from Hilbert source/Noether charge before orbital calibration",
            "current_status": "NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "if_passed": "prevents hiding epsilon_Wchan in source mass normalization",
            "blocker": "Hilbert/source readout descent remains unsigned",
            "source_path": str(SOURCE_PATHS["SRC3059_13_3052_readout_gates"]),
        }
    ),
    base(
        {
            "lock_id": "DLOCK3059_2_orbital_GM",
            "requirement": "orbital GM is a prediction/readout, not the definition of the source coefficient",
            "current_status": "NOT_PROVED",
            "gate_passes_for_current_MTS": "false",
            "if_passed": "epsilon_Wchan cannot be calibrated away by redefining GM",
            "blocker": "measured-GM/Gauss/orbital chain is not closed",
            "source_path": str(SOURCE_PATHS["SRC3059_08_ppn_source_gates"]),
        }
    ),
    base(
        {
            "lock_id": "DLOCK3059_3_ppn_U",
            "requirement": "PPN U uses locked G_ref and source mass rather than a refitted U_meas",
            "current_status": "BLOCKED",
            "gate_passes_for_current_MTS": "false",
            "if_passed": "epsilon_Wchan becomes an observable source-normalization residual",
            "blocker": "U first-order potential lock remains blocked",
            "source_path": str(SOURCE_PATHS["SRC3059_07_ppn_metric_contract"]),
        }
    ),
    base(
        {
            "lock_id": "DLOCK3059_4_verdict",
            "requirement": "no-GM-absorption denominator lock",
            "current_status": "FAILED_FOR_CURRENT_MTS",
            "gate_passes_for_current_MTS": "false",
            "if_passed": "could score Delta G_source/G_ref or feed physical PPN kernels",
            "blocker": "all denominator/readout locks are conditional or missing",
            "source_path": str(SOURCE_PATHS["SRC3059_02_3058_absorption_gate"]),
        }
    ),
]

gamma_kernel_rows = [
    base(
        {
            "kernel_id": "GK3059_0_response_ansatz",
            "quantity": "metric response amplitudes",
            "formula": "A_T = 1 + k_T*epsilon_Wchan + O(epsilon^2); A_S = 1 + k_S*epsilon_Wchan + O(epsilon^2)",
            "derivation": "A_T controls the calibrated g00/Newtonian source response; A_S controls gij spatial-curvature response",
            "result": "response split parametrized",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_k_T; MISSING_k_S",
        }
    ),
    base(
        {
            "kernel_id": "GK3059_1_gamma_law",
            "quantity": "gamma_minus_1",
            "formula": "gamma - 1 = A_S/A_T - 1 = (k_S-k_T)*epsilon_Wchan + O(epsilon^2)",
            "derivation": "expand ratio of spatial to temporal metric response after Newtonian normalization",
            "result": "SYMBOLIC_KERNEL_DERIVED",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_RESPONSE_SPLIT_VALUES",
        }
    ),
    base(
        {
            "kernel_id": "GK3059_2_common_mode",
            "quantity": "pure common-mode source normalization",
            "formula": "if k_S=k_T, then K_gamma_epsilon=0 at first order",
            "derivation": "equal spatial and temporal response rescales U but does not create gamma slip",
            "result": "CALIBRATION_SAFE_CASE_IDENTIFIED",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_PROOF_kS_EQUALS_kT",
        }
    ),
    base(
        {
            "kernel_id": "GK3059_3_lapse_only",
            "quantity": "lapse-only source response diagnostic",
            "formula": "if k_T=1 and k_S=0, then gamma-1=-epsilon_Wchan",
            "derivation": "temporal response changes while spatial response does not",
            "result": "DIAGNOSTIC_COUNTERCASE_NOT_CLAIMED",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_PROOF_OF_RESPONSE_CLASS",
        }
    ),
    base(
        {
            "kernel_id": "GK3059_4_spatial_only",
            "quantity": "spatial-only source response diagnostic",
            "formula": "if k_S=1 and k_T=0, then gamma-1=+epsilon_Wchan",
            "derivation": "spatial response changes while temporal normalization does not",
            "result": "DIAGNOSTIC_COUNTERCASE_NOT_CLAIMED",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_PROOF_OF_RESPONSE_CLASS",
        }
    ),
    base(
        {
            "kernel_id": "GK3059_5_verdict",
            "quantity": "K_gamma_epsilon",
            "formula": "K_gamma_epsilon = k_S-k_T",
            "derivation": "3059 supplies the symbolic gamma-slip kernel, but not the parent response values",
            "result": "SYMBOLIC_ONLY_NONCLAIM",
            "kernel_ready": "false",
            "missing_for_claim": "MISSING_PARENT_METRIC_RESPONSE_SPLIT",
        }
    ),
]

response_split_rows = [
    base(
        {
            "requirement_id": "RSPLIT3059_0_kT",
            "needed_object": "k_T",
            "definition": "partial derivative of temporal/lapse Newtonian response A_T with respect to epsilon_Wchan at epsilon=0",
            "needed_source": "linearized g00 equation in fixed PPN gauge after W/Hilbert/source denominator lock",
            "current_status": "MISSING",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "requirement_id": "RSPLIT3059_1_kS",
            "needed_object": "k_S",
            "definition": "partial derivative of spatial curvature response A_S with respect to epsilon_Wchan at epsilon=0",
            "needed_source": "linearized gij equation in fixed PPN gauge after W/Hilbert/source denominator lock",
            "current_status": "MISSING",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "requirement_id": "RSPLIT3059_2_difference",
            "needed_object": "k_S-k_T",
            "definition": "first-order epsilon_Wchan coefficient in gamma_minus_1",
            "needed_source": "parent metric response split or proof of common-mode equality",
            "current_status": "SYMBOLIC_ONLY",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "requirement_id": "RSPLIT3059_3_beta",
            "needed_object": "K_beta_epsilon",
            "definition": "second-order g00 response to epsilon_Wchan",
            "needed_source": "O(U^2) weak-field expansion and source-normalization freeze",
            "current_status": "MISSING_SECOND_ORDER",
            "valid_for_claim": "false",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3059_0_denominator_lock",
            "claim": "epsilon_Wchan cannot be absorbed into measured GM",
            "status": "NO_NOT_PROVED",
            "claim_active": "false",
            "reason": "G_ref/source mass/orbital GM/PPN U locks are conditional or blocked",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3059_1_gamma_kernel",
            "claim": "K_gamma_epsilon is physically sourced",
            "status": "NO_SYMBOLIC_ONLY",
            "claim_active": "false",
            "reason": "3059 derives K_gamma_epsilon=k_S-k_T but k_S,k_T are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3059_2_common_mode_zero",
            "claim": "epsilon_Wchan gives zero gamma slip",
            "status": "NO_NEEDS_kS_EQUALS_kT_PROOF",
            "claim_active": "false",
            "reason": "common-mode zero is a case, not yet a theorem",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3059_3_local_GR",
            "claim": "PPN/local-GR branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "metric response split remains missing",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3059_0_denominator",
            "question": "Can 3059 prove no-GM absorption?",
            "answer": "NO",
            "reason": "the necessary independent denominator locks are all conditional or missing",
            "action": "do not score epsilon_Wchan as physical source-G residual",
        }
    ),
    base(
        {
            "decision_id": "DEC3059_1_gamma",
            "question": "Can 3059 derive a gamma kernel?",
            "answer": "YES_SYMBOLICALLY",
            "reason": "gamma-1=(k_S-k_T)*epsilon_Wchan follows from metric response ratio",
            "action": "next derive k_S and k_T or prove k_S=k_T",
        }
    ),
    base(
        {
            "decision_id": "DEC3059_2_next",
            "question": "Best next target?",
            "answer": "METRIC_RESPONSE_SPLIT",
            "reason": "k_S-k_T is now the missing physical PPN bridge",
            "action": "build 3060 kS/kT parent metric response split or common-mode theorem",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3059_0_3060",
            "next_checkpoint": "3060-Y5-R2FR-epsilon-Wchannel-metric-response-split-kS-kT-or-common-mode-theorem-under-AX1090.md",
            "script": "scripts/Y5_R2FR_epsilon_Wchannel_metric_response_split_kS_kT_or_common_mode_theorem_under_AX1090_3060.py",
            "mission": "derive k_S and k_T from the parent weak-field metric equations, or prove epsilon_Wchan is pure common-mode with k_S=k_T",
            "starting_equation": "gamma - 1 = (k_S-k_T)*epsilon_Wchan + O(epsilon^2)",
            "claim_policy": "no PPN/local-GR claim until k_S-k_T is parent-derived or theorem-zero",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["denominator_lock"], denominator_lock_rows)
write_csv(OUTPUTS["gamma_kernel"], gamma_kernel_rows)
write_csv(OUTPUTS["response_split"], response_split_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["denominator_lock"], BRANCH_OUTPUTS["denominator_lock_copy"])
copy_csv(OUTPUTS["gamma_kernel"], BRANCH_OUTPUTS["gamma_kernel_copy"])
copy_csv(OUTPUTS["response_split"], BRANCH_OUTPUTS["response_split_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3059 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["denominator_lock"],
    OUTPUTS["gamma_kernel"],
    OUTPUTS["response_split"],
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

all_denominator_gates_block = all(row["gate_passes_for_current_MTS"] == "false" for row in denominator_lock_rows)
has_gamma_formula = any(row["formula"] == "K_gamma_epsilon = k_S-k_T" for row in gamma_kernel_rows)
has_missing_split = any(row["current_status"] == "MISSING" for row in response_split_rows)
kernel_all_nonready = all(row["kernel_ready"] == "false" for row in gamma_kernel_rows)

validation_rows = [
    base({"validation_id": "VAL3059_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3059_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3059_02_denominator_lock_blocks", "passed": all_denominator_gates_block, "requirement": "no-GM-absorption denominator lock blocks current MTS", "evidence": OUTPUTS["denominator_lock"].name}),
    base({"validation_id": "VAL3059_03_gamma_kernel_symbolic", "passed": has_gamma_formula and kernel_all_nonready, "requirement": "symbolic gamma kernel is derived but not claim-ready", "evidence": OUTPUTS["gamma_kernel"].name}),
    base({"validation_id": "VAL3059_04_response_split_missing", "passed": has_missing_split, "requirement": "k_S/k_T response split remains missing", "evidence": OUTPUTS["response_split"].name}),
    base({"validation_id": "VAL3059_05_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3059" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3059 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3059_06_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active flags"}),
    base({"validation_id": "VAL3059_07_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3059 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3059_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3059_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3059_10_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3059_11_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3060-"), "requirement": "next target selects kS/kT metric response split or common-mode theorem", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3059_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3059 - No-GM-Absorption Denominator Lock or Epsilon W-Channel Gamma-Slip Kernel

Status: `Y5_R2FR_3059_no_GM_absorption_not_proved_gamma_slip_kernel_symbolic_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3059 cannot prove the no-GM-absorption denominator lock. `G_ref`, Hilbert source mass, orbital GM, and PPN `U` are still not locked strongly enough to stop a common source-normalization shift being calibrated away.

But 3059 does derive the symbolic gamma-slip kernel.

Let:

`A_T = 1 + k_T epsilon_Wchan + O(epsilon^2)`

`A_S = 1 + k_S epsilon_Wchan + O(epsilon^2)`

where `A_T` is the temporal/Newtonian source response and `A_S` is the spatial-curvature response. Then:

`gamma - 1 = A_S/A_T - 1`

so:

`gamma - 1 = (k_S-k_T) epsilon_Wchan + O(epsilon^2)`.

This is useful but not claimable. The missing object is now very specific:

`k_S-k_T`.

If `k_S=k_T`, epsilon is pure common mode and gives no first-order gamma slip. If `k_S!=k_T`, epsilon becomes a real PPN gamma residual. Current MTS has not derived either case.

## No-GM-Absorption Denominator Lock Attempt

{md_table(denominator_lock_rows, ["lock_id", "requirement", "current_status", "gate_passes_for_current_MTS", "if_passed", "blocker"])}

## Epsilon Gamma-Slip Kernel Formula

{md_table(gamma_kernel_rows, ["kernel_id", "quantity", "formula", "derivation", "result", "kernel_ready", "missing_for_claim"])}

## Metric Response Split Requirements

{md_table(response_split_rows, ["requirement_id", "needed_object", "definition", "needed_source", "current_status", "valid_for_claim"])}

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
    raise SystemExit(f"3059 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: no-GM absorption not proved; gamma kernel symbolic; kS-kT missing")
