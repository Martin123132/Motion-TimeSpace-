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

CHECKPOINT = "3058"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3058-Y5-R2FR-epsilon-Wchannel-source-normalization-to-PPN-projection-or-parent-type-system-derivation-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3058_00_3057_doc": ROOT / "3057-Y5-R2FR-parent-type-system-no-spurion-proof-or-first-epsilon-Wchannel-arena-coefficients-under-AX1090.md",
    "SRC3058_01_3057_first_K": RESIDUALS / "P8_Y5_R2FR_3057_FIRST_K_EPSILON_COEFFICIENTS.csv",
    "SRC3058_02_3057_arena_status": RESIDUALS / "P8_Y5_R2FR_3057_ARENA_COEFFICIENT_STATUS.csv",
    "SRC3058_03_3057_no_spurion": RESIDUALS / "P8_Y5_R2FR_3057_NO_SPURION_PROOF_ATTEMPT.csv",
    "SRC3058_04_3057_next": RESIDUALS / "P8_Y5_R2FR_3057_NEXT_TARGET.csv",
    "SRC3058_05_3056_bound_schema": RESIDUALS / "P8_Y5_R2FR_3056_EPSILON_WCHANNEL_BOUND_SCHEMA.csv",
    "SRC3058_06_3056_gates": RESIDUALS / "P8_Y5_R2FR_3056_GRAMMAR_GATE_EVALUATION.csv",
    "SRC3058_07_3055_epsilon": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "SRC3058_08_ppn_metric_contract": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
    "SRC3058_09_ppn_source_gates": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
    "SRC3058_10_ppn_residual_vector": RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv",
    "SRC3058_11_3015_ppn_kernel_contract": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3058_12_3016_ppn_first_kernel": RESIDUALS / "P8_Y5_R2FR_3016_PPN_FIRST_KERNEL_ROWS.csv",
    "SRC3058_13_2746_ppn_coeff": RESIDUALS / "P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv",
    "SRC3058_14_1883_full_ppn_vector": RESIDUALS / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
    "SRC3058_15_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3058_16_3052_readout": RESIDUALS / "P8_Y5_R2FR_3052_READOUT_LOCK_GATE_EVALUATION.csv",
    "SRC3058_17_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3058_SOURCE_REGISTER.csv",
    "local_projection": RESIDUALS / "P8_Y5_R2FR_3058_EPSILON_TO_LOCAL_NEWTON_PROJECTION.csv",
    "ppn_absorption_gate": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "ppn_projection": RESIDUALS / "P8_Y5_R2FR_3058_PPN_PROJECTION_ATTEMPT.csv",
    "parent_type_fallback": RESIDUALS / "P8_Y5_R2FR_3058_PARENT_TYPE_SYSTEM_FALLBACK.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3058_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3058_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3058_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3058_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3058_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_projection_copy": LOCAL_BOUNDS / "epsilon_to_local_Newton_projection_3058_INTERNAL_NONCLAIM.csv",
    "ppn_absorption_gate_copy": LOCAL_BOUNDS / "PPN_GM_absorption_and_gauge_gate_3058_NOT_READY.csv",
    "ppn_projection_copy": LOCAL_BOUNDS / "PPN_projection_attempt_3058_BLOCKED_NONCLAIM.csv",
    "parent_type_fallback_copy": PARENT_ACTION / "parent_type_system_fallback_3058_NOT_SIGNED.csv",
    "next_copy": RAB_QUEUE / "JR3058_NO_GM_ABSORPTION_OR_PPN_KERNEL_FILL_NEXT_NONCLAIM.csv",
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
        "ppn_ready",
        "physical_bound_ready",
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

local_projection_rows = [
    base(
        {
            "projection_id": "LNP3058_0_internal_delta_A",
            "quantity": "delta_A_source",
            "formula": "delta_A_source = epsilon_Wchan + R_lock + Delta_operator_pullback + higher_order",
            "K_epsilon": "1",
            "status": "DERIVED_INTERNAL_NONCLAIM",
            "physical_interpretation": "epsilon_Wchan enters the internal local source-normalization residual linearly with unit coefficient",
            "claim_limit": "not a physical PPN coefficient",
            "source_path": str(SOURCE_PATHS["SRC3058_01_3057_first_K"]),
        }
    ),
    base(
        {
            "projection_id": "LNP3058_1_G_source",
            "quantity": "Delta G_source/G_ref",
            "formula": "Delta G_source/G_ref = epsilon_Wchan if W/Phi, G_ref, Hilbert source, denominator and no-GM-absorption gates pass",
            "K_epsilon": "1_if_gates_pass",
            "status": "CONDITIONAL_NOT_ACTIVE",
            "physical_interpretation": "epsilon_Wchan could rescale the source-side Newton coefficient relative to G_ref",
            "claim_limit": "blocked by readout gates and measured-GM absorption",
            "source_path": str(SOURCE_PATHS["SRC3058_15_3050_gref"]),
        }
    ),
    base(
        {
            "projection_id": "LNP3058_2_measured_GM_degeneracy",
            "quantity": "Newtonian orbital U",
            "formula": "U_meas = G_meas * integral rho_obs/r; a common source rescaling is absorbed unless G_ref/M_H/GM denominator is independently locked",
            "K_epsilon": "calibration_degenerate",
            "status": "PPN_ABSORPTION_WARNING",
            "physical_interpretation": "PPN uses a calibrated Newtonian potential, so source-normalization alone is not automatically gamma_minus_1",
            "claim_limit": "must prove no-GM-absorption before using Cassini/PPN bounds on epsilon_Wchan",
            "source_path": str(SOURCE_PATHS["SRC3058_08_ppn_metric_contract"]),
        }
    ),
]

ppn_absorption_gate_rows = [
    base(
        {
            "gate_id": "PPNG3058_0_U_definition",
            "requirement": "PPN U uses the same measured-GM/source normalization as the local Newton branch",
            "current_status": "BLOCKED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "first-order measured-GM/Gauss/orbital chain remains unfilled",
            "source_path": str(SOURCE_PATHS["SRC3058_08_ppn_metric_contract"]),
        }
    ),
    base(
        {
            "gate_id": "PPNG3058_1_no_GM_absorption",
            "requirement": "epsilon_Wchan cannot be absorbed into G_meas*M_obs before PPN comparison",
            "current_status": "NOT_PROVED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "G_ref, source mass and orbital GM denominator lock are still conditional",
            "source_path": str(SOURCE_PATHS["SRC3058_16_3052_readout"]),
        }
    ),
    base(
        {
            "gate_id": "PPNG3058_2_same_metric_response",
            "requirement": "the epsilon source residual maps separately into g00 and gij response coefficients",
            "current_status": "MISSING_COMPONENT_KERNEL",
            "gate_passes_for_current_MTS": "false",
            "blocker": "A_S/A_T or equivalent spatial/lapse metric response values missing",
            "source_path": str(SOURCE_PATHS["SRC3058_12_3016_ppn_first_kernel"]),
        }
    ),
    base(
        {
            "gate_id": "PPNG3058_3_beta_second_order",
            "requirement": "source normalization remains fixed through O(U^2) beta expansion",
            "current_status": "MISSING_SECOND_ORDER_KERNEL",
            "gate_passes_for_current_MTS": "false",
            "blocker": "second-order weak-field source equation not computed",
            "source_path": str(SOURCE_PATHS["SRC3058_09_ppn_source_gates"]),
        }
    ),
    base(
        {
            "gate_id": "PPNG3058_4_readout_gauge",
            "requirement": "PPN coordinate/readout gauge is fixed before coefficient comparison",
            "current_status": "MISSING_READOUT_GAUGE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "PPN kernel contract still lists missing readout gauge/source frame",
            "source_path": str(SOURCE_PATHS["SRC3058_11_3015_ppn_kernel_contract"]),
        }
    ),
]

ppn_projection_rows = [
    base(
        {
            "ppn_id": "PPNP3058_0_common_mode",
            "observable": "calibrated first-order Newtonian U",
            "projection_formula": "epsilon_Wchan common-mode source rescaling -> absorbed into U_meas unless no-GM-absorption gate passes",
            "K_epsilon_PPN": "0_after_Newtonian_calibration_if_pure_common_mode",
            "status": "CALIBRATION_IDENTITY_NONCLAIM",
            "ppn_ready": "false",
            "reason": "a pure common-mode source rescaling is not a PPN gamma/beta residual by itself",
        }
    ),
    base(
        {
            "ppn_id": "PPNP3058_1_gamma_slip",
            "observable": "gamma_minus_1",
            "projection_formula": "gamma_minus_1 = K_gamma_slip * epsilon_Wchan + other residuals, only if epsilon creates different spatial/lapse metric response",
            "K_epsilon_PPN": "MISSING_K_GAMMA_SLIP",
            "status": "MISSING_COMPONENT_KERNEL",
            "ppn_ready": "false",
            "reason": "need A_S/A_T or equivalent metric response; source normalization alone is not enough",
        }
    ),
    base(
        {
            "ppn_id": "PPNP3058_2_beta",
            "observable": "beta_minus_1",
            "projection_formula": "beta_minus_1 = K_beta_source * epsilon_Wchan + second_order_tail",
            "K_epsilon_PPN": "MISSING_K_BETA_SECOND_ORDER",
            "status": "MISSING_SECOND_ORDER_KERNEL",
            "ppn_ready": "false",
            "reason": "beta is a second-order metric response; internal K=1 does not supply it",
        }
    ),
    base(
        {
            "ppn_id": "PPNP3058_3_alpha_preferred_frame",
            "observable": "alpha1/alpha2/alpha3/xi",
            "projection_formula": "preferred-frame PPN terms require frame/vector/domain kernels independent of epsilon_Wchan",
            "K_epsilon_PPN": "NO_DIRECT_COEFFICIENT_FROM_SOURCE_NORMALIZATION",
            "status": "OUT_OF_SCOPE_FOR_EPSILON_ONLY",
            "ppn_ready": "false",
            "reason": "epsilon_Wchan is scalar source normalization; frame kernels remain separate",
        }
    ),
    base(
        {
            "ppn_id": "PPNP3058_4_verdict",
            "observable": "physical PPN vector",
            "projection_formula": "PPN_vector = calibrated_common_mode + metric_slip + beta_second_order + frame_terms",
            "K_epsilon_PPN": "NOT_FILLED",
            "status": "PPN_PROJECTION_BLOCKED_NONCLAIM",
            "ppn_ready": "false",
            "reason": "no physical PPN claim until no-GM-absorption and metric response kernels are signed",
        }
    ),
]

parent_type_fallback_rows = [
    base(
        {
            "fallback_id": "PTF3058_0_type_system",
            "route": "parent type system/no-spurion",
            "why_it_matters": "proving epsilon_Wchan=0 avoids calibration-degenerate PPN bounding",
            "current_status": "STILL_OPEN",
            "next_requirement": "derive q-stack owner, no source/readout spurion, and variation-before-readout theorem",
            "source_path": str(SOURCE_PATHS["SRC3058_03_3057_no_spurion"]),
        }
    ),
    base(
        {
            "fallback_id": "PTF3058_1_physical_kernel",
            "route": "physical PPN kernel",
            "why_it_matters": "if epsilon_Wchan is nonzero, only a nonabsorbed metric response can be compared to PPN bounds",
            "current_status": "MISSING",
            "next_requirement": "derive A_S/A_T or K_gamma_slip and beta second-order response in fixed gauge",
            "source_path": str(SOURCE_PATHS["SRC3058_11_3015_ppn_kernel_contract"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3058_0_internal_K",
            "claim": "epsilon_Wchan has internal local Newton source coefficient K=1",
            "status": "YES_INTERNAL_NONCLAIM",
            "claim_active": "false",
            "reason": "internal bookkeeping only; not a physical pass",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3058_1_ppn_gamma",
            "claim": "epsilon_Wchan maps to gamma_minus_1 with a sourced coefficient",
            "status": "NO_MISSING_METRIC_SLIP_KERNEL",
            "claim_active": "false",
            "reason": "common-mode source normalization is calibration-degenerate unless metric slip/no-GM-absorption is proven",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3058_2_ppn_beta",
            "claim": "epsilon_Wchan maps to beta_minus_1 with a sourced coefficient",
            "status": "NO_MISSING_SECOND_ORDER_KERNEL",
            "claim_active": "false",
            "reason": "beta requires O(U^2) source/metric response",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3058_3_local_GR",
            "claim": "local GR/Newton PPN branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "3058 blocks an unsafe PPN shortcut and selects next denominator/kernel gate",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3058_0_projection",
            "question": "Can internal K=1 be used directly as a PPN bound coefficient?",
            "answer": "NO",
            "reason": "PPN first-order U is calibrated by measured Newtonian normalization; common-mode source rescaling may be absorbed",
            "action": "do not score epsilon_Wchan against Cassini/gamma yet",
        }
    ),
    base(
        {
            "decision_id": "DEC3058_1_real_progress",
            "question": "What did 3058 add?",
            "answer": "CALIBRATION_GATE",
            "reason": "it separates internal source normalization from physical PPN metric-slip coefficients",
            "action": "require no-GM-absorption or derive A_S/A_T metric response",
        }
    ),
    base(
        {
            "decision_id": "DEC3058_2_next",
            "question": "Best next target?",
            "answer": "NO_GM_ABSORPTION_OR_GAMMA_SLIP_KERNEL",
            "reason": "this is the missing bridge between epsilon_Wchan and observable local tests",
            "action": "build 3059 denominator-lock / metric-slip kernel attempt",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3058_0_3059",
            "next_checkpoint": "3059-Y5-R2FR-no-GM-absorption-denominator-lock-or-epsilon-Wchannel-gamma-slip-kernel-under-AX1090.md",
            "script": "scripts/Y5_R2FR_no_GM_absorption_denominator_lock_or_epsilon_Wchannel_gamma_slip_kernel_under_AX1090_3059.py",
            "mission": "try to prove epsilon_Wchan cannot be absorbed into measured GM; if not, derive the gamma-slip kernel requiring separate spatial/lapse metric response",
            "starting_equation": "delta_A_source = epsilon_Wchan + ... but PPN gamma needs nonabsorbed metric slip, not just source normalization",
            "claim_policy": "no PPN/local-GR claim until no-GM-absorption or a sourced gamma/beta kernel exists",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["local_projection"], local_projection_rows)
write_csv(OUTPUTS["ppn_absorption_gate"], ppn_absorption_gate_rows)
write_csv(OUTPUTS["ppn_projection"], ppn_projection_rows)
write_csv(OUTPUTS["parent_type_fallback"], parent_type_fallback_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["local_projection"], BRANCH_OUTPUTS["local_projection_copy"])
copy_csv(OUTPUTS["ppn_absorption_gate"], BRANCH_OUTPUTS["ppn_absorption_gate_copy"])
copy_csv(OUTPUTS["ppn_projection"], BRANCH_OUTPUTS["ppn_projection_copy"])
copy_csv(OUTPUTS["parent_type_fallback"], BRANCH_OUTPUTS["parent_type_fallback_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3058 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["local_projection"],
    OUTPUTS["ppn_absorption_gate"],
    OUTPUTS["ppn_projection"],
    OUTPUTS["parent_type_fallback"],
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

has_internal_k = any(row["K_epsilon"] == "1" for row in local_projection_rows)
has_absorption_warning = any(row["status"] == "PPN_ABSORPTION_WARNING" for row in local_projection_rows)
all_ppn_gates_block = all(row["gate_passes_for_current_MTS"] == "false" for row in ppn_absorption_gate_rows)
ppn_all_nonready = all(row["ppn_ready"] == "false" for row in ppn_projection_rows)

validation_rows = [
    base({"validation_id": "VAL3058_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3058_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3058_02_internal_K_preserved", "passed": has_internal_k, "requirement": "internal K_epsilon_source_norm=1 is preserved", "evidence": OUTPUTS["local_projection"].name}),
    base({"validation_id": "VAL3058_03_absorption_warning", "passed": has_absorption_warning, "requirement": "measured-GM/PPN absorption warning is explicit", "evidence": OUTPUTS["local_projection"].name}),
    base({"validation_id": "VAL3058_04_ppn_gates_block", "passed": all_ppn_gates_block, "requirement": "PPN no-absorption/gauge gates block current claims", "evidence": OUTPUTS["ppn_absorption_gate"].name}),
    base({"validation_id": "VAL3058_05_ppn_projection_nonready", "passed": ppn_all_nonready, "requirement": "physical PPN projection remains nonready", "evidence": OUTPUTS["ppn_projection"].name}),
    base({"validation_id": "VAL3058_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3058" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3058 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3058_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active flags"}),
    base({"validation_id": "VAL3058_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3058 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3058_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3058_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3058_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3058_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3059-"), "requirement": "next target selects no-GM-absorption or gamma-slip kernel", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3058_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3058 - Epsilon W-Channel Source Normalization to PPN Projection or Parent Type-System Derivation

Status: `Y5_R2FR_3058_internal_Kepsilon_preserved_PPN_absorption_gate_blocks_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3058 protects the project from a tempting but unsafe shortcut.

We have the internal local source-normalization bridge:

`delta_A_source = epsilon_Wchan + R_lock + Delta_operator_pullback + higher_order`

so internally:

`K_epsilon_source_norm = 1`.

But this is **not automatically** a PPN `gamma` or `beta` coefficient. In a PPN comparison the first-order Newtonian potential is calibrated by the measured Newtonian normalization:

`U_meas = G_meas integral rho_obs/r`.

Therefore a pure common-mode source rescaling can be absorbed into `G_meas*M_obs` unless the framework independently locks `G_ref`, source mass, orbital GM, and the PPN gauge/readout. To get an observable PPN residual, `epsilon_Wchan` must either:

1. survive the no-GM-absorption denominator lock, or
2. create a metric-slip/second-order response with a sourced kernel such as `K_gamma_slip` or `K_beta_source`.

3058 does not find those kernels. It keeps `K=1` as an internal bridge and blocks the physical PPN claim.

## Epsilon to Local Newton Projection

{md_table(local_projection_rows, ["projection_id", "quantity", "formula", "K_epsilon", "status", "physical_interpretation", "claim_limit"])}

## PPN GM Absorption and Gauge Gate

{md_table(ppn_absorption_gate_rows, ["gate_id", "requirement", "current_status", "gate_passes_for_current_MTS", "blocker"])}

## PPN Projection Attempt

{md_table(ppn_projection_rows, ["ppn_id", "observable", "projection_formula", "K_epsilon_PPN", "status", "ppn_ready", "reason"])}

## Parent Type-System Fallback

{md_table(parent_type_fallback_rows, ["fallback_id", "route", "why_it_matters", "current_status", "next_requirement"])}

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
    raise SystemExit(f"3058 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: internal K=1 preserved; PPN projection blocked by GM absorption/gauge gates")
