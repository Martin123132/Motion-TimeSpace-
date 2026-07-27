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

CHECKPOINT = "3062"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3062-Y5-R2FR-EH-operator-dominance-and-extra-field-silence-or-Delta-kST-input-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3062_00_3061_doc": ROOT / "3061-Y5-R2FR-EH-common-source-dominance-theorem-or-Delta-kST-bound-schema-under-AX1090.md",
    "SRC3062_01_3061_dominance": RESIDUALS / "P8_Y5_R2FR_3061_EH_COMMON_SOURCE_DOMINANCE_GATE.csv",
    "SRC3062_02_3061_zero_attempt": RESIDUALS / "P8_Y5_R2FR_3061_DELTA_KST_ZERO_THEOREM_ATTEMPT.csv",
    "SRC3062_03_3061_bound_schema": RESIDUALS / "P8_Y5_R2FR_3061_DELTA_KST_EPSILON_BOUND_SCHEMA.csv",
    "SRC3062_04_3061_next": RESIDUALS / "P8_Y5_R2FR_3061_NEXT_TARGET.csv",
    "SRC3062_05_local_action_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3062_06_EH_impact": RESIDUALS / "P8_Y5_PARENT_EH_1512_NEWTON_PPN_IMPACT.csv",
    "SRC3062_07_EH_synthesis": RESIDUALS / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PPN_COMPONENT_FILL_LEDGER.csv",
    "SRC3062_08_GR_left_gate": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv",
    "SRC3062_09_hilbert": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "SRC3062_10_W_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_OWNER_GATE_EVALUATION.csv",
    "SRC3062_11_absorption": RESIDUALS / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
    "SRC3062_12_extra_silence": RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv",
    "SRC3062_13_extra_response": RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv",
    "SRC3062_14_double_zero_matrix": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_DOUBLE_ZERO_STATUS_MATRIX.csv",
    "SRC3062_15_leakage_residuals": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_LEAKAGE_RESIDUAL_ROWS.csv",
    "SRC3062_16_operator_inventory": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
    "SRC3062_17_ppn_kernel": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3062_18_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3062_SOURCE_REGISTER.csv",
    "eh_attempt": RESIDUALS / "P8_Y5_R2FR_3062_EH_OPERATOR_DOMINANCE_ATTEMPT.csv",
    "extra_audit": RESIDUALS / "P8_Y5_R2FR_3062_EXTRA_FIELD_SILENCE_AUDIT.csv",
    "delta_inputs": RESIDUALS / "P8_Y5_R2FR_3062_DELTA_KST_INPUT_ROWS_NONCLAIM.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3062_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3062_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3062_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3062_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3062_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "eh_attempt_copy": PARENT_ACTION / "EH_operator_dominance_attempt_3062_NOT_SIGNED.csv",
    "extra_audit_copy": LOCAL_BOUNDS / "extra_field_silence_audit_3062_NONCLAIM.csv",
    "delta_inputs_copy": LOCAL_BOUNDS / "Delta_kST_input_rows_3062_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3062_extra_field_double_zero_or_Delta_kST_component_runner_NEXT_NONCLAIM.csv",
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
        "proof_signed",
        "gate_passes_for_current_MTS",
        "theorem_zero",
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

eh_attempt_rows = [
    base(
        {
            "gate_id": "EHD3062_0_EH_core_action",
            "requirement": "local parent action contains an EH core in g_obs",
            "candidate_formula": "S_EH=(2*kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "current_status": "SOURCE_ROW_PRESENT_BUT_NOT_OPERATOR_SELECTED",
            "proof_signed": "false",
            "would_close": "identifies the candidate spin-2 operator",
            "blocker": "source row exists, but the corpus still marks Newton/PPN blocked until operator/source branch is owned",
            "source_path": str(SOURCE_PATHS["SRC3062_05_local_action_blocks"]),
        }
    ),
    base(
        {
            "gate_id": "EHD3062_1_constant_coupling",
            "requirement": "kappa_eff is a constant integration/global sector in local experiments",
            "candidate_formula": "delta kappa_eff=0 on the local weak-field collar",
            "current_status": "REQUIRED_NOT_SIGNED",
            "proof_signed": "false",
            "would_close": "prevents source-normalization drift from masquerading as metric response",
            "blocker": "constant-kappa proof/value remains one of the extra-sector silence blockers",
            "source_path": str(SOURCE_PATHS["SRC3062_12_extra_silence"]),
        }
    ),
    base(
        {
            "gate_id": "EHD3062_2_common_Hilbert_source",
            "requirement": "same Hilbert source T_obs sources both scalar/lapse and spatial weak-field equations",
            "candidate_formula": "T_obs^munu=(-2/sqrt(-g_obs)) delta S_matter[psi,g_obs]/delta g_obs_munu",
            "current_status": "NOT_SIGNED",
            "proof_signed": "false",
            "would_close": "keeps epsilon_Wchan as common source normalization rather than a k_S/k_T split",
            "blocker": "Hilbert source descent remains unsigned",
            "source_path": str(SOURCE_PATHS["SRC3062_09_hilbert"]),
        }
    ),
    base(
        {
            "gate_id": "EHD3062_3_extra_operator_silence",
            "requirement": "extra fields do not contribute a linear local metric-response operator",
            "candidate_formula": "D_C_X(Phi0)=0 and D_V(Phi0)=0 with positive Hessian/gap and silent boundary projector",
            "current_status": "AUDIT_LEVEL_ONLY",
            "proof_signed": "false",
            "would_close": "sets Delta_extra_linear=0 in Delta_kST",
            "blocker": "double-zero matrix has not_signed/open/candidate rows rather than a parent theorem",
            "source_path": str(SOURCE_PATHS["SRC3062_14_double_zero_matrix"]),
        }
    ),
    base(
        {
            "gate_id": "EHD3062_4_common_mode_metric_response",
            "requirement": "EH response gives k_T=k_S=1 after gauge/readout lock",
            "candidate_formula": "linearized EH operator E_EH[h]=kappa0 T_obs in the same PPN gauge and denominator",
            "current_status": "CONDITIONAL_ONLY",
            "proof_signed": "false",
            "would_close": "sets Delta_EH_operator=0",
            "blocker": "gauge/readout/no-GM-absorption locks remain blocked",
            "source_path": str(SOURCE_PATHS["SRC3062_11_absorption"]),
        }
    ),
    base(
        {
            "gate_id": "EHD3062_5_boundary_projector_silence",
            "requirement": "local boundary/projector terms do not split spatial and temporal potentials",
            "candidate_formula": "P_loc boundary load and selector commutator vanish or are second order on the local collar",
            "current_status": "NOT_SIGNED",
            "proof_signed": "false",
            "would_close": "sets Delta_boundary_projector=0",
            "blocker": "domain/projector and boundary silence are open in the extra inventory",
            "source_path": str(SOURCE_PATHS["SRC3062_15_leakage_residuals"]),
        }
    ),
]

extra_audit_rows = [
    base(
        {
            "sector_id": "X3062_0_GK_q_loc",
            "parent_sector": "Gamma/Khat/q_loc",
            "silence_condition": "C_GK(Phi0)=0; D C_GK(Phi0)=0; D V_GK(Phi0)=0; positive gap; boundary silence",
            "source_status": "not_signed",
            "theorem_zero": "false",
            "residual_component": "Delta_extra_GK_linear",
            "feeds_Delta_kST": "true",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO; MISSING_GAP; MISSING_BOUNDARY_SILENCE",
            "source_path": str(SOURCE_PATHS["SRC3062_14_double_zero_matrix"]),
        }
    ),
    base(
        {
            "sector_id": "X3062_1_memory_response",
            "parent_sector": "response/memory doublet",
            "silence_condition": "memory response is even about the local fixed point and has no linear metric stress",
            "source_status": "candidate_only",
            "theorem_zero": "false",
            "residual_component": "Delta_extra_memory_linear",
            "feeds_Delta_kST": "true",
            "missing_for_claim": "MISSING_PARENT_EVENNESS_THEOREM; MISSING_NUMERIC_BOUND",
            "source_path": str(SOURCE_PATHS["SRC3062_13_extra_response"]),
        }
    ),
    base(
        {
            "sector_id": "X3062_2_domain_projector",
            "parent_sector": "domain/projector selector",
            "silence_condition": "selector/projector stress and P_loc commutator vanish in local stationary vacuum",
            "source_status": "open",
            "theorem_zero": "false",
            "residual_component": "Delta_domain_projector",
            "feeds_Delta_kST": "true",
            "missing_for_claim": "MISSING_PROJECTOR_COMMUTATOR_ZERO; MISSING_LOCAL_BOUNDARY_CONDITION",
            "source_path": str(SOURCE_PATHS["SRC3062_15_leakage_residuals"]),
        }
    ),
    base(
        {
            "sector_id": "X3062_3_metric_readout",
            "parent_sector": "metric/readout protection",
            "silence_condition": "D_A g_readout|Phi0 produces no representative Weyl/disformal spatial-lapse split",
            "source_status": "open",
            "theorem_zero": "false",
            "residual_component": "Delta_gauge_readout",
            "feeds_Delta_kST": "true",
            "missing_for_claim": "MISSING_READOUT_OWNER; MISSING_NO_DISFORMAL_PROOF",
            "source_path": str(SOURCE_PATHS["SRC3062_16_operator_inventory"]),
        }
    ),
    base(
        {
            "sector_id": "X3062_4_PiM_source_measure",
            "parent_sector": "PiM/source-measure projector",
            "silence_condition": "source-measure projector equals EH/Hilbert source to first order",
            "source_status": "not_signed",
            "theorem_zero": "false",
            "residual_component": "Delta_source_anisotropy",
            "feeds_Delta_kST": "true",
            "missing_for_claim": "MISSING_PIM_VALUE; MISSING_DPIM_ZERO; MISSING_NO_GM_ABSORPTION",
            "source_path": str(SOURCE_PATHS["SRC3062_15_leakage_residuals"]),
        }
    ),
    base(
        {
            "sector_id": "X3062_5_kappa",
            "parent_sector": "constant gravitational coupling",
            "silence_condition": "D ln(kappa_MTS)=0 or source-backed local bound is supplied",
            "source_status": "missing_parent_constant_kappa_proof_or_value",
            "theorem_zero": "false",
            "residual_component": "Delta_kappa_source_norm",
            "feeds_Delta_kST": "false_common_mode_if_only_normalization",
            "missing_for_claim": "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE",
            "source_path": str(SOURCE_PATHS["SRC3062_12_extra_silence"]),
        }
    ),
]

delta_input_rows = [
    base(
        {
            "input_id": "DKIN3062_0_total",
            "quantity": "Delta_kST",
            "units": "dimensionless",
            "definition": "k_S-k_T",
            "component_formula": "Delta_EH_operator+Delta_extra_linear+Delta_source_anisotropy+Delta_gauge_readout+Delta_boundary_projector",
            "candidate_value": "MISSING_PARENT_ZERO_OR_NUMERIC_COMPONENTS",
            "source_status": "NONCLAIM_SYMBOLIC_CONTRACT",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_EH_DOMINANCE; MISSING_EXTRA_SILENCE; MISSING_NUMERIC_COMPONENT_ROWS",
            "source_path": str(OUTPUTS["eh_attempt"]),
        }
    ),
    base(
        {
            "input_id": "DKIN3062_1_EH_operator",
            "quantity": "Delta_EH_operator",
            "units": "dimensionless",
            "definition": "spatial-temporal split from non-common EH/operator normalization",
            "component_formula": "k_S^EH-k_T^EH",
            "candidate_value": "0_IF_EH_COMMON_MODE_THEOREM_SIGNED_ELSE_MISSING",
            "source_status": "BLOCKED_BY_OPERATOR_SELECTION_AND_GAUGE_LOCK",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_EH_OPERATOR_DOMINANCE; MISSING_PPN_GAUGE_DENOMINATOR_LOCK",
            "source_path": str(OUTPUTS["eh_attempt"]),
        }
    ),
    base(
        {
            "input_id": "DKIN3062_2_extra_linear",
            "quantity": "Delta_extra_linear",
            "units": "dimensionless",
            "definition": "first-order anisotropic metric response from extra fields",
            "component_formula": "sum_X eta_X D C_X(Phi0)/M_X^2 plus allowed derivative/boundary pieces",
            "candidate_value": "MISSING_DOUBLE_ZERO_OR_NUMERIC_ETA_DC_OVER_M2",
            "source_status": "BLOCKED_BY_EXTRA_DOUBLE_ZERO_AUDIT",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C0; MISSING_dC; MISSING_GAP; MISSING_BOUNDARY_SILENCE",
            "source_path": str(OUTPUTS["extra_audit"]),
        }
    ),
    base(
        {
            "input_id": "DKIN3062_3_source_anisotropy",
            "quantity": "Delta_source_anisotropy",
            "units": "dimensionless",
            "definition": "difference between source current seen by spatial and lapse weak-field equations",
            "component_formula": "(T_S-T_T)/T_obs after Hilbert-source descent",
            "candidate_value": "MISSING_HILBERT_DESCENT_OR_NUMERIC_SOURCE_SPLIT",
            "source_status": "BLOCKED_BY_MATTER_DESCENT",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_COMMON_HILBERT_SOURCE; MISSING_ORDINARY_MATTER_SIGNATURE",
            "source_path": str(SOURCE_PATHS["SRC3062_09_hilbert"]),
        }
    ),
    base(
        {
            "input_id": "DKIN3062_4_gauge_readout",
            "quantity": "Delta_gauge_readout",
            "units": "dimensionless",
            "definition": "representative/gauge/readout leakage that shifts gamma without a physical EH split",
            "component_formula": "delta(gamma)_readout after W retirement and no-disformal proof",
            "candidate_value": "MISSING_GAUGE_READOUT_LOCK",
            "source_status": "BLOCKED_BY_W_OWNER_AND_NO_GM_ABSORPTION_GATES",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_W_RETIREMENT_PARENT_OWNER; MISSING_NO_DISFORMAL_PROOF; MISSING_GM_DENOMINATOR_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3062_10_W_owner"]),
        }
    ),
    base(
        {
            "input_id": "DKIN3062_5_boundary_projector",
            "quantity": "Delta_boundary_projector",
            "units": "dimensionless",
            "definition": "local boundary/projector load that splits spatial and temporal responses",
            "component_formula": "P_loc commutator plus boundary stress contribution to k_S-k_T",
            "candidate_value": "MISSING_BOUNDARY_PROJECTOR_SILENCE",
            "source_status": "BLOCKED_BY_DOMAIN_PROJECTOR_OPEN_ROWS",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PROJECTOR_ZERO; MISSING_LOCAL_COLLAR_BOUNDARY_DATA",
            "source_path": str(SOURCE_PATHS["SRC3062_15_leakage_residuals"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3062_0_EH_operator_dominance",
            "claim": "EH operator dominance is derived for current MTS",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "EH core exists as a candidate block, but operator selection/source/gauge locks are not signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3062_1_extra_field_silence",
            "claim": "extra fields are silent at first order in the local weak-field branch",
            "status": "NO_AUDIT_ONLY",
            "claim_active": "false",
            "reason": "double-zero and boundary/projector conditions remain open/not_signed/candidate_only",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3062_2_Delta_kST_zero",
            "claim": "Delta_kST=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "zero follows only if EH dominance plus extra silence are parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3062_3_Delta_kST_bound_ready",
            "claim": "Delta_kST inputs are numeric/source-backed enough for a local PPN bound",
            "status": "NO_SYMBOLIC_NONCLAIM_ROWS_ONLY",
            "claim_active": "false",
            "reason": "3062 fills residual components, not measured coefficients",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3062_4_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "3062 sharpens the closure contract but does not close it",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3062_0_zero_proof",
            "question": "Did 3062 prove EH dominance plus extra-field silence?",
            "answer": "NO",
            "reason": "the source hierarchy provides candidate action blocks and audit evidence, not a parent-signed theorem",
            "action": "do not claim Delta_kST=0 or local GR",
        }
    ),
    base(
        {
            "decision_id": "DEC3062_1_best_route",
            "question": "Best next route?",
            "answer": "PROVE_EXTRA_DOUBLE_ZERO_FIRST",
            "reason": "extra-field silence is the largest uncontrolled linear leakage into Delta_kST and is already decomposed by sector",
            "action": "attempt C(Phi0)=0, D C(Phi0)=0, D V(Phi0)=0, positive-gap, and boundary-silence proof before numeric bounds",
        }
    ),
    base(
        {
            "decision_id": "DEC3062_2_fallback",
            "question": "What if the double-zero proof fails?",
            "answer": "BUILD_COMPONENT_BOUND_RUNNER",
            "reason": "Delta_kST now has explicit nonclaim component rows that can be bounded one-by-one",
            "action": "make a runner for symbolic/numeric Delta_kST components without allowing a claim until source-backed values exist",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3062_0_3063",
            "next_checkpoint": "3063-Y5-R2FR-extra-field-double-zero-proof-or-Delta-kST-component-bound-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_extra_field_double_zero_proof_or_Delta_kST_component_bound_runner_under_AX1090_3063.py",
            "mission": "try to parent-sign extra-field double zeros and boundary silence; if not, build a nonclaim Delta_kST component-bound runner",
            "starting_equation": "Delta_kST=Delta_EH_operator+Delta_extra_linear+Delta_source_anisotropy+Delta_gauge_readout+Delta_boundary_projector",
            "claim_policy": "no local-GR/PPN claim unless every Delta_kST component is zero by theorem or numeric/source-backed and bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["eh_attempt"], eh_attempt_rows)
write_csv(OUTPUTS["extra_audit"], extra_audit_rows)
write_csv(OUTPUTS["delta_inputs"], delta_input_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["eh_attempt"], BRANCH_OUTPUTS["eh_attempt_copy"])
copy_csv(OUTPUTS["extra_audit"], BRANCH_OUTPUTS["extra_audit_copy"])
copy_csv(OUTPUTS["delta_inputs"], BRANCH_OUTPUTS["delta_inputs_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3062 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["eh_attempt"],
    OUTPUTS["extra_audit"],
    OUTPUTS["delta_inputs"],
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

all_eh_unsigned = all(row["proof_signed"] == "false" for row in eh_attempt_rows)
all_extra_unsigned = all(row["theorem_zero"] == "false" for row in extra_audit_rows)
all_delta_nonclaim = all(row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in delta_input_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
delta_formula_present = any("Delta_EH_operator+Delta_extra_linear" in row["component_formula"] for row in delta_input_rows)

validation_rows = [
    base({"validation_id": "VAL3062_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3062_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3062_02_EH_attempt_unsigned", "passed": all_eh_unsigned, "requirement": "EH dominance proof remains unsigned unless every clause is parent-signed", "evidence": OUTPUTS["eh_attempt"].name}),
    base({"validation_id": "VAL3062_03_extra_silence_unsigned", "passed": all_extra_unsigned, "requirement": "extra-field silence remains nonclaim while double-zero clauses are unsigned", "evidence": OUTPUTS["extra_audit"].name}),
    base({"validation_id": "VAL3062_04_delta_inputs_nonclaim", "passed": all_delta_nonclaim and delta_formula_present, "requirement": "Delta_kST component rows are present but nonclaim", "evidence": OUTPUTS["delta_inputs"].name}),
    base({"validation_id": "VAL3062_05_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3062_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3062" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3062 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3062_07_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3062_08_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3062_09_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3062_10_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3063-"), "requirement": "next target selects extra double-zero proof or Delta_kST component runner", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3062_11_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3062 - EH Operator Dominance and Extra-Field Silence or Delta kST Input Fill

Status: `Y5_R2FR_3062_EH_operator_dominance_not_signed_extra_silence_nonclaim_Delta_kST_components_filled`

Generated: `{RUN_UTC}`

## Verdict

3062 takes the 3061 residual seriously:

`gamma_minus_1 = Delta_kST * epsilon_Wchan + O(epsilon^2)`.

The clean GR route would be:

`Delta_kST = 0`.

That requires EH operator dominance, a common Hilbert source, extra-field silence, W/readout retirement, gauge/denominator lock, and local boundary/projector silence. The current corpus does **not** sign those clauses yet.

So 3062 does not claim local GR. It writes the exact nonclaim component contract:

`Delta_kST = Delta_EH_operator + Delta_extra_linear + Delta_source_anisotropy + Delta_gauge_readout + Delta_boundary_projector`.

The good news is that the problem is no longer foggy. The local-GR branch now has named failure modes and named residual inputs.

## EH Operator Dominance Attempt

{md_table(eh_attempt_rows, ["gate_id", "requirement", "candidate_formula", "current_status", "proof_signed", "would_close", "blocker"])}

## Extra-Field Silence Audit

{md_table(extra_audit_rows, ["sector_id", "parent_sector", "silence_condition", "source_status", "theorem_zero", "residual_component", "feeds_Delta_kST", "missing_for_claim"])}

## Delta kST Input Rows

{md_table(delta_input_rows, ["input_id", "quantity", "definition", "component_formula", "candidate_value", "source_status", "bound_ready", "missing_for_claim"])}

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
    raise SystemExit(f"3062 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: EH dominance not signed; extra silence nonclaim; Delta_kST components filled")
