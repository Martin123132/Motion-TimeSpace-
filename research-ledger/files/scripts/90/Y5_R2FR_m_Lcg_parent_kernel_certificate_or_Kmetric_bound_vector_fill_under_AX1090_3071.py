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

CHECKPOINT = "3071"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3071-Y5-R2FR-m-Lcg-parent-kernel-certificate-or-Kmetric-bound-vector-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3071_00_3070_doc": ROOT / "3070-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norms-or-aux-stress-demotion-under-AX1090.md",
    "SRC3071_01_3070_next": RESIDUALS / "P8_Y5_R2FR_3070_NEXT_TARGET.csv",
    "SRC3071_02_3070_kernel_audit": RESIDUALS / "P8_Y5_R2FR_3070_KMETRIC_KERNEL_NORM_AUDIT.csv",
    "SRC3071_03_3070_zero_branch": RESIDUALS / "P8_Y5_R2FR_3070_KERNEL_ZERO_BRANCH_AUDIT.csv",
    "SRC3071_04_3070_bound_vector": RESIDUALS / "P8_Y5_R2FR_3070_DELTA_G_SGAMMA_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3071_05_1368_kernel_hunt": RESIDUALS / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "SRC3071_06_1368_decision": RESIDUALS / "P8_Y5_R10_1368_DECISION_LEDGER.csv",
    "SRC3071_07_1292_parent_match": RESIDUALS / "P8_Y5_R10_1292_M_LCG_PARENT_SOURCE_MATCH_AUDIT.csv",
    "SRC3071_08_1520_metric_silence": RESIDUALS / "P8_Y5_PARENT_LCG_1520_METRIC_SILENCE_THEOREM.csv",
    "SRC3071_09_1520_contract": RESIDUALS / "P8_Y5_PARENT_LCG_1520_PARENT_CONTRACT_AUDIT.csv",
    "SRC3071_10_1520_decision": RESIDUALS / "P8_Y5_PARENT_LCG_1520_DECISION.csv",
    "SRC3071_11_1532_lcg_ownership": RESIDUALS / "P8_Y5_PARENT_QLOC_1532_LCG_OWNERSHIP_AUDIT.csv",
    "SRC3071_12_1532_lcg_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1532_LCG_ZERO_CONTRACT.csv",
    "SRC3071_13_1369_lcg_hunt": RESIDUALS / "P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
    "SRC3071_14_1369_lcg_response": RESIDUALS / "P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
    "SRC3071_15_1370_lcg_contract_audit": RESIDUALS / "P8_Y5_R10_1370_PARENT_LCG_CONTRACT_AUDIT.csv",
    "SRC3071_16_1370_lcg_contract_candidate": RESIDUALS / "P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
    "SRC3071_17_2734_lcg_silence": RESIDUALS / "P8_Y5_R2FR_2734_LCG_METRIC_SILENCE_AUDIT.csv",
    "SRC3071_18_2734_ml_bound": RESIDUALS / "P8_Y5_R2FR_2734_FIRST_ML_KERNEL_NORM_ROW.csv",
    "SRC3071_19_2734_ml_inputs": RESIDUALS / "P8_Y5_R2FR_2734_ML_BOUND_INPUT_SCHEMA.csv",
    "SRC3071_20_2734_decision": RESIDUALS / "P8_Y5_R2FR_2734_DECISION_LEDGER.csv",
    "SRC3071_21_798_gamma_source": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "SRC3071_22_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3071_23_2816_zero_audit": RESIDUALS / "P8_Y5_R2FR_2816_MM_ML_ZERO_PROOF_AUDIT.csv",
    "SRC3071_24_2817_zero_attempt": RESIDUALS / "P8_Y5_R2FR_2817_MM_ML_KERNEL_ZERO_ATTEMPT.csv",
    "SRC3071_25_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3071_SOURCE_REGISTER.csv",
    "m_certificate": RESIDUALS / "P8_Y5_R2FR_3071_M_PARENT_KERNEL_CERTIFICATE_AUDIT.csv",
    "lcg_certificate": RESIDUALS / "P8_Y5_R2FR_3071_LCG_PARENT_KERNEL_CERTIFICATE_AUDIT.csv",
    "source_root": RESIDUALS / "P8_Y5_R2FR_3071_SOURCE_ROOT_DOUBLE_ZERO_ROUTE_AUDIT.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_3071_MM_ML_BOUND_VECTOR_NONCLAIM.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3071_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3071_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3071_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3071_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3071_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "m_certificate_copy": PARENT_ACTION / "m_parent_kernel_certificate_3071_NOT_SIGNED.csv",
    "lcg_certificate_copy": PARENT_ACTION / "Lcg_parent_kernel_certificate_3071_NOT_SIGNED.csv",
    "source_root_copy": PARENT_ACTION / "source_root_double_zero_route_3071_UNSIGNED.csv",
    "bound_vector_copy": LOCAL_BOUNDS / "Mm_ML_bound_vector_3071_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3071_source_root_local_lock_or_Mm_ML_bound_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


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
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "certificate_signed",
        "kernel_zero_proved",
        "numeric_ready",
        "bound_ready",
        "local_gr_claim",
        "khat_claim",
    }
    for row in input_rows:
        for field in claim_fields:
            if field in row and boolish(row[field]):
                return True
    return False


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


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


dotg_rows_before = rows(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": str(path.exists()),
            "parse_ok": str(source_parse_ok(path)),
            "row_count": row_count(path),
            "role": "m_Lcg_parent_kernel_certificate_evidence" if source_id != "SRC3071_25_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

m_certificate_rows = [
    base(
        {
            "cert_id": "MCERT3071_0_named_symbol",
            "target": "m parent definition",
            "candidate_or_test": "m appears in Gamma_eff=L_cg^-2 F(m), with conditional locked expansion m=m_*+delta m",
            "result": "NAMED_SYMBOL_CONDITIONAL_LOCK_NO_PARENT_DEFINITION",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_DEFINITION_OF_m;MISSING_m_PROFILE;MISSING_LOCAL_LOCK_THEOREM",
            "source_ids": "SRC3071_07_1292_parent_match;SRC3071_21_798_gamma_source",
        }
    ),
    base(
        {
            "cert_id": "MCERT3071_1_fixed_field_route",
            "target": "M_m=0",
            "candidate_or_test": "if m is an independent parent scalar held fixed in Hilbert variation, delta_g m=0",
            "result": "CONDITIONAL_RELATIVE_ZERO_NOT_LIVE",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_m_FIXED_FIELD_CLAUSE;MISSING_NO_METRIC_COMPOSITE_READOUT;MISSING_VARIATION_ORDER",
            "source_ids": "SRC3071_05_1368_kernel_hunt;SRC3071_24_2817_zero_attempt",
        }
    ),
    base(
        {
            "cert_id": "MCERT3071_2_metric_composite_counterbranch",
            "target": "M_m retained",
            "candidate_or_test": "if m is a metric-composite, marker, norm, curvature scalar, projector contraction, or domain-selected scalar, delta_g m survives",
            "result": "COUNTERBRANCH_RETAINED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_NO_MARKER_THEOREM;MISSING_EXPLICIT_PARENT_m_DEFINITION_OR_RESPONSE_BOUND",
            "source_ids": "SRC3071_05_1368_kernel_hunt;SRC3071_07_1292_parent_match",
        }
    ),
    base(
        {
            "cert_id": "MCERT3071_3_active_memory_stress_split",
            "target": "m-sector active stress",
            "candidate_or_test": "even if algebraic delta_g m=0, any kinetic/source/boundary memory action contributes separate Hilbert stress",
            "result": "SEPARATE_RESIDUAL_REQUIRED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_MEMORY_STRESS_NOHAIR;MISSING_SOURCE_ZERO;MISSING_BOUNDARY_ZERO_OR_BOUND",
            "source_ids": "SRC3071_05_1368_kernel_hunt",
        }
    ),
]

lcg_certificate_rows = [
    base(
        {
            "cert_id": "LCGCERT3071_0_fixed_L0",
            "target": "M_L=0",
            "candidate_or_test": "L_cg=L0 as a positive fixed scalar parameter held fixed under Hilbert variation",
            "result": "COVARIANCE_ADMISSIBLE_CLOSURE_CANDIDATE",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_ACTION_ADOPTION;MISSING_UNITS;MISSING_SCALE_ORIGIN;MISSING_VARIATION_BEFORE_READOUT_CERTIFICATE",
            "source_ids": "SRC3071_08_1520_metric_silence;SRC3071_09_1520_contract;SRC3071_16_1370_lcg_contract_candidate",
        }
    ),
    base(
        {
            "cert_id": "LCGCERT3071_1_no_smuggling",
            "target": "fixed L0 anti-smuggling guard",
            "candidate_or_test": "cell-volume, curvature, density, source, projector or domain readout must not masquerade as L0 inside Hilbert variation",
            "result": "REQUIRED_GUARD_NOT_LIVE_PARENT_RULE",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_ELL_D_VS_LCG_SPLIT;MISSING_DOMAIN_NO_FLUX_CERTIFICATE;MISSING_READOUT_SEPARATION",
            "source_ids": "SRC3071_09_1520_contract;SRC3071_15_1370_lcg_contract_audit;SRC3071_16_1370_lcg_contract_candidate",
        }
    ),
    base(
        {
            "cert_id": "LCGCERT3071_2_quotient_owned",
            "target": "M_L=0 through quotient descent",
            "candidate_or_test": "if L_cg=Lbar(q(Phi),theta) and q,theta descend metric-silently, delta_g L_cg=0",
            "result": "COVARIANT_ROUTE_UNSIGNED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_QUOTIENT_MAP;MISSING_THETA_OWNER;MISSING_METRIC_SILENT_DESCENT_THEOREM",
            "source_ids": "SRC3071_11_1532_lcg_ownership;SRC3071_17_2734_lcg_silence",
        }
    ),
    base(
        {
            "cert_id": "LCGCERT3071_3_metric_composite",
            "target": "M_L retained",
            "candidate_or_test": "if L_cg is a proper length, curvature scale, density scale, domain support, or projector collar, M_L generically survives",
            "result": "COUNTERBRANCH_RETAINED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_LCG_PARENT_DEFINITION_OR_RESPONSE_COEFFICIENT;MISSING_ML_BOUND",
            "source_ids": "SRC3071_11_1532_lcg_ownership;SRC3071_13_1369_lcg_hunt;SRC3071_17_2734_lcg_silence",
        }
    ),
]

source_root_rows = [
    base(
        {
            "route_id": "SR3071_0_F_root",
            "target": "remove L_cg chain coefficient",
            "statement": "F(m_*)=0 removes the algebraic L_cg response term -2 L_cg^-3 F(m) M_L at the locked local vacuum even if M_L is finite",
            "result": "BEST_ALGEBRAIC_ROUTE_UNSIGNED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_SOURCE_ROOT;MISSING_SAME_BRANCH_LOCAL_LOCK;MISSING_NO_FITTED_PER_SYSTEM_ROOT",
            "source_ids": "SRC3071_11_1532_lcg_ownership;SRC3071_12_1532_lcg_zero;SRC3071_17_2734_lcg_silence",
        }
    ),
    base(
        {
            "route_id": "SR3071_1_Fprime_stationary",
            "target": "remove m-chain coefficient",
            "statement": "F'(m_*)=0 removes the linear M_m coefficient at the local stationary point",
            "result": "CONDITIONAL_ONLY",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_SELECTION_OF_m_STAR;MISSING_FPRIME_ZERO_THEOREM",
            "source_ids": "SRC3071_21_798_gamma_source;SRC3071_23_2816_zero_audit",
        }
    ),
    base(
        {
            "route_id": "SR3071_2_double_zero",
            "target": "remove both algebraic M_L and M_m coefficients",
            "statement": "F(m_*)=0 and F'(m_*)=0 remove the algebraic L_cg and m kernel coefficients at the fixed point",
            "result": "STRONG_CONDITION_UNSIGNED",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_LOCAL_LOCK_AMPLITUDE_LAW;MISSING_TRANSITION_SUPPORT_THEOREM",
            "source_ids": "SRC3071_12_1532_lcg_zero;SRC3071_18_2734_ml_bound;SRC3071_20_2734_decision",
        }
    ),
    base(
        {
            "route_id": "SR3071_3_finite_displacement",
            "target": "bounded off-root branch",
            "statement": "near a double zero, residual L_cg response is quadratic in Delta_m: ||R_L|| <= |C_sign| L_min^-3 F2_bar Delta_m^2 M_L_bar + O(Delta_m^3)",
            "result": "BEST_BOUND_IF_LOCK_NOT_EXACT",
            "certificate_signed": "false",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_DELTA_m_AMPLITUDE_LAW;MISSING_F2_BAR;MISSING_ML_BAR;MISSING_L_MIN",
            "source_ids": "SRC3071_18_2734_ml_bound;SRC3071_19_2734_ml_inputs;SRC3071_20_2734_decision",
        }
    ),
]

bound_vector_rows = [
    base(
        {
            "row_id": "MML3071_0_master_bound",
            "quantity": "E_SGamma",
            "formula": "(2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "status": "BOUND_VECTOR_RETAINED_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_M_m_AND_M_L_PARENT_CERTIFICATES",
            "missing_for_claim": "MISSING_M_m;MISSING_M_L;MISSING_K_CONN;MISSING_K_DOMAIN;MISSING_K_BOUNDARY",
            "source_ids": "SRC3071_04_3070_bound_vector;SRC3071_22_1289_derivative",
        }
    ),
    base(
        {
            "row_id": "MML3071_1_fixed_L0_branch",
            "quantity": "M_L",
            "formula": "M_L=0 if L_cg=L0 is parent-fixed and anti-smuggling/readout-separation clauses are live",
            "status": "CONDITIONAL_ZERO_NOT_LIVE",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_PARENT_FIXED_L0_ADOPTION",
            "missing_for_claim": "MISSING_PARENT_ACTION_ADOPTION;MISSING_SCALE_ORIGIN;MISSING_READOUT_SEPARATION",
            "source_ids": "SRC3071_08_1520_metric_silence;SRC3071_09_1520_contract",
        }
    ),
    base(
        {
            "row_id": "MML3071_2_fixed_m_branch",
            "quantity": "M_m",
            "formula": "M_m=0 if m is a parent-owned independent scalar held fixed under Hilbert variation",
            "status": "CONDITIONAL_ZERO_NOT_LIVE",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_PARENT_m_FIXED_FIELD_ADOPTION",
            "missing_for_claim": "MISSING_PARENT_m_DEFINITION;MISSING_NO_METRIC_COMPOSITE_READOUT",
            "source_ids": "SRC3071_05_1368_kernel_hunt;SRC3071_24_2817_zero_attempt",
        }
    ),
    base(
        {
            "row_id": "MML3071_3_double_zero_branch",
            "quantity": "algebraic M_m/M_L coefficients",
            "formula": "F(m_*)=F'(m_*)=0 makes the algebraic M_m/M_L coefficients vanish at exact lock",
            "status": "BEST_DERIVATION_ROUTE_UNSIGNED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_PARENT_DOUBLE_ZERO_AND_LOCK",
            "missing_for_claim": "MISSING_SOURCE_ROOT;MISSING_STATIONARY_ROOT;MISSING_LOCAL_LOCK",
            "source_ids": "SRC3071_12_1532_lcg_zero;SRC3071_20_2734_decision",
        }
    ),
    base(
        {
            "row_id": "MML3071_4_finite_bound_inputs",
            "quantity": "M_m_bar;M_L_bar;Delta_m;F2_bar;L_min",
            "formula": "off-root residuals require explicit bounds for M_m, M_L, Delta_m, F derivatives and L_cg lower bound",
            "status": "BOUND_INPUTS_MISSING",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_BOUND_INPUTS",
            "missing_for_claim": "MISSING_M_m_BAR;MISSING_M_L_BAR;MISSING_DELTA_m;MISSING_F2_BAR;MISSING_L_MIN",
            "source_ids": "SRC3071_18_2734_ml_bound;SRC3071_19_2734_ml_inputs",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3071_0_m_certificate",
            "decision": "Do not claim M_m=0.",
            "result": "M_CERTIFICATE_NOT_SIGNED",
            "rationale": "m has a conditional fixed-field route, but current sources do not parent-define m or exclude metric-composite/readout meanings.",
            "next_action": "prefer double-zero/root-lock route or retain M_m as bound input",
        }
    ),
    base(
        {
            "decision_id": "DEC3071_1_Lcg_certificate",
            "decision": "Do not claim M_L=0 from fixed L0.",
            "result": "LCG_CERTIFICATE_NOT_SIGNED",
            "rationale": "fixed L0 is mathematically clean but closure-looking until parent adoption, scale origin, and readout separation are explicit.",
            "next_action": "prefer F(m_*)=0 coefficient kill over bare fixed-scale silence",
        }
    ),
    base(
        {
            "decision_id": "DEC3071_2_best_route",
            "decision": "Use source-root/double-zero as the next derivation-first target.",
            "result": "NEXT_SOURCE_ROOT_LOCAL_LOCK",
            "rationale": "F(m_*)=0 and F'(m_*)=0 remove algebraic M_L and M_m coefficients without needing to declare L_cg metric-silent.",
            "next_action": "derive parent source root, stationary root, and Delta_m/local-lock amplitude law",
        }
    ),
]

claim_rows = [
    base({"claim_id": "CLAIM3071_0_Mm_zero", "claim": "M_m=0 is parent-signed", "status": "NO", "claim_active": "false", "reason": "m parent definition/fixed-field clause is missing"}),
    base({"claim_id": "CLAIM3071_1_ML_zero", "claim": "M_L=0 is parent-signed", "status": "NO", "claim_active": "false", "reason": "fixed L0/quotient-silent routes are unsigned and counterbranches remain"}),
    base({"claim_id": "CLAIM3071_2_double_zero", "claim": "F(m_*)=F'(m_*)=0 is parent-signed", "status": "NO", "claim_active": "false", "reason": "source-root and local-lock amplitude law are missing"}),
    base({"claim_id": "CLAIM3071_3_local_GR_PPN", "claim": "local GR/PPN branch is derived", "status": "NO", "claim_active": "false", "reason": "E_SGamma, DeltaK_TF and q_loc residual channels remain open"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3071_0_3072",
            "next_checkpoint": "3072-Y5-R2FR-source-root-double-zero-local-lock-or-Mm-ML-bound-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_root_double_zero_local_lock_or_Mm_ML_bound_fill_under_AX1090_3072.py",
            "mission": "try to derive F(m_*)=0 and F'(m_*)=0 plus a local-lock/Delta_m amplitude law; if not, retain M_m/M_L coefficient bounds as explicit nonclaim inputs",
            "starting_equation": "E_SGamma=(2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + hidden kernels)",
            "claim_policy": "no Khat/q_loc/local-GR claim unless source root, stationary root, local lock, hidden-kernel silence and observable projection are source-backed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["m_certificate"], m_certificate_rows)
write_csv(OUTPUTS["lcg_certificate"], lcg_certificate_rows)
write_csv(OUTPUTS["source_root"], source_root_rows)
write_csv(OUTPUTS["bound_vector"], bound_vector_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["m_certificate"], BRANCH_OUTPUTS["m_certificate_copy"])
copy_csv(OUTPUTS["lcg_certificate"], BRANCH_OUTPUTS["lcg_certificate_copy"])
copy_csv(OUTPUTS["source_root"], BRANCH_OUTPUTS["source_root_copy"])
copy_csv(OUTPUTS["bound_vector"], BRANCH_OUTPUTS["bound_vector_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": str(path.exists()),
            "row_count": row_count(path),
            "description": "3071 branch copy for parent-action/local-bound/acquisition-queue continuity",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
non_validation_csv_paths = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path != OUTPUTS["validation"]]
all_output_rows: list[dict[str, Any]] = []
for output_path in non_validation_csv_paths:
    all_output_rows.extend(rows(output_path))

dotg_rows_after = rows(DOTG_TARGET)
formalization_generated_hits = [path for path in generated_paths if under(path, FORMALIZATION)]

all_sources_exist = all(boolish(row["exists"]) for row in source_register)
all_sources_parse = all(boolish(row["parse_ok"]) for row in source_register)
m_cert_not_signed = all(row["certificate_signed"] == "false" and row["kernel_zero_proved"] == "false" for row in m_certificate_rows)
lcg_cert_not_signed = all(row["certificate_signed"] == "false" and row["kernel_zero_proved"] == "false" for row in lcg_certificate_rows)
counterbranches_retained = any(row["cert_id"] == "MCERT3071_2_metric_composite_counterbranch" for row in m_certificate_rows) and any(row["cert_id"] == "LCGCERT3071_3_metric_composite" for row in lcg_certificate_rows)
source_root_preferred = any(row["route_id"] == "SR3071_2_double_zero" and row["result"] == "STRONG_CONDITION_UNSIGNED" for row in source_root_rows)
finite_bound_present = any(row["route_id"] == "SR3071_3_finite_displacement" and "Delta_m" in row["statement"] for row in source_root_rows)
all_bound_rows_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in bound_vector_rows)
decision_next_source_root = any(row["decision_id"] == "DEC3071_2_best_route" and row["result"] == "NEXT_SOURCE_ROOT_LOCAL_LOCK" for row in decision_rows)
all_claims_inactive = all(row["claim_active"] == "false" for row in claim_rows)
next_is_3072 = next_rows[0]["next_checkpoint"].startswith("3072-")

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

validation_rows = [
    base({"validation_id": "VAL3071_00_sources_exist", "passed": all_sources_exist, "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3071_01_sources_parse", "passed": all_sources_parse, "requirement": "all cited CSV sources parse and markdown sources exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3071_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3071_03_m_certificate_not_signed", "passed": m_cert_not_signed, "requirement": "M_m zero certificate remains unsigned", "evidence": OUTPUTS["m_certificate"].name}),
    base({"validation_id": "VAL3071_04_lcg_certificate_not_signed", "passed": lcg_cert_not_signed, "requirement": "M_L zero certificate remains unsigned", "evidence": OUTPUTS["lcg_certificate"].name}),
    base({"validation_id": "VAL3071_05_counterbranches_retained", "passed": counterbranches_retained, "requirement": "metric-composite m/Lcg counterbranches are retained", "evidence": f"{OUTPUTS['m_certificate'].name};{OUTPUTS['lcg_certificate'].name}"}),
    base({"validation_id": "VAL3071_06_source_root_route_staged", "passed": source_root_preferred and finite_bound_present, "requirement": "source-root/double-zero route is staged but nonclaim", "evidence": OUTPUTS["source_root"].name}),
    base({"validation_id": "VAL3071_07_bound_vector_nonclaim", "passed": all_bound_rows_nonclaim, "requirement": "M_m/M_L bound vector rows remain nonclaim", "evidence": OUTPUTS["bound_vector"].name}),
    base({"validation_id": "VAL3071_08_decision_next", "passed": decision_next_source_root, "requirement": "decision selects source-root/local-lock next target", "evidence": OUTPUTS["decision"].name}),
    base({"validation_id": "VAL3071_09_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row activates Khat, q_loc, local-GR, R10, PPN, clock or orbital claims", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3071_10_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3071" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3071 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3071_11_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3071_12_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3071_13_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench generated-output count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3071_14_next_target", "passed": next_is_3072, "requirement": "next target selects source-root double-zero/local lock", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3071_15_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3071 - m/Lcg Parent Kernel Certificate or Kmetric Bound Vector Fill

Status: `Y5_R2FR_3071_Mm_ML_certificates_not_signed_source_root_route_selected`

Generated: `{RUN_UTC}`

## Verdict

3071 tested whether the two algebraic kernels inside `delta_g S_Gamma` can be killed directly:

`M_m := -2 delta m / delta g_00`, and `M_L := -2 delta L_cg / delta g_00`.

Neither zero certificate is live.

For `m`, the fixed-field route is mathematically clean only if `m` is parent-defined as an independent scalar held fixed under Hilbert variation. Current sources do not prove that, and they retain metric-composite/readout/marker counterbranches.

For `L_cg`, fixed `L_cg=L0` is also mathematically clean and covariant as a scalar parameter, but it remains closure-looking until the parent action adopts it, supplies its scale origin, and separates it from domain/readout lengths. Metric-composite `L_cg` counterbranches remain live.

The best next derivation route is therefore not bare `L_cg` silence. It is the source-root/double-zero route:

`F(m_*)=0`, `F'(m_*)=0`.

That would remove the algebraic coefficients multiplying `M_L` and `M_m` at the locked local vacuum, with finite off-root residuals controlled by a `Delta_m` amplitude law. This is less suspicious than simply declaring the coarse-graining scale fixed, but it is still unsigned.

No `Khat`, `q_loc`, local-GR/PPN, R10, clock, or orbital claim is promoted.

## m Parent Kernel Certificate Audit

{md_table(m_certificate_rows, ["cert_id", "target", "candidate_or_test", "result", "certificate_signed", "missing_for_claim"])}

## Lcg Parent Kernel Certificate Audit

{md_table(lcg_certificate_rows, ["cert_id", "target", "candidate_or_test", "result", "certificate_signed", "missing_for_claim"])}

## Source Root / Double-Zero Route Audit

{md_table(source_root_rows, ["route_id", "target", "statement", "result", "certificate_signed", "missing_for_claim"])}

## Mm/ML Bound Vector

{md_table(bound_vector_rows, ["row_id", "quantity", "formula", "status", "symbolic_value", "numeric_ready", "bound_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "result", "rationale", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

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

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3071 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: M_m/M_L zero certificates not signed; source-root double-zero selected as next derivation route")
