from __future__ import annotations

import csv
import hashlib
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

CHECKPOINT = "3072"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3072-Y5-R2FR-source-root-double-zero-local-lock-or-Mm-ML-bound-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3072_00_3071_doc": ROOT / "3071-Y5-R2FR-m-Lcg-parent-kernel-certificate-or-Kmetric-bound-vector-fill-under-AX1090.md",
    "SRC3072_01_3071_next": RESIDUALS / "P8_Y5_R2FR_3071_NEXT_TARGET.csv",
    "SRC3072_02_3071_source_root": RESIDUALS / "P8_Y5_R2FR_3071_SOURCE_ROOT_DOUBLE_ZERO_ROUTE_AUDIT.csv",
    "SRC3072_03_3071_bound_vector": RESIDUALS / "P8_Y5_R2FR_3071_MM_ML_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3072_04_1532_lcg_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1532_LCG_ZERO_CONTRACT.csv",
    "SRC3072_05_1532_double_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1532_DOUBLE_ZERO_SOURCE_CONTRACT.csv",
    "SRC3072_06_1531_zero_route": RESIDUALS / "P8_Y5_PARENT_QLOC_1531_ZERO_ROUTE_AUDIT.csv",
    "SRC3072_07_1531_bound_envelope": RESIDUALS / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
    "SRC3072_08_2734_ml_bound": RESIDUALS / "P8_Y5_R2FR_2734_FIRST_ML_KERNEL_NORM_ROW.csv",
    "SRC3072_09_2734_ml_inputs": RESIDUALS / "P8_Y5_R2FR_2734_ML_BOUND_INPUT_SCHEMA.csv",
    "SRC3072_10_2734_root_lock": RESIDUALS / "P8_Y5_R2FR_2734_SOURCE_ROOT_LOCK_COMPARISON.csv",
    "SRC3072_11_2734_decision": RESIDUALS / "P8_Y5_R2FR_2734_DECISION_LEDGER.csv",
    "SRC3072_12_798_gamma_source": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "SRC3072_13_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3072_14_2816_zero_audit": RESIDUALS / "P8_Y5_R2FR_2816_MM_ML_ZERO_PROOF_AUDIT.csv",
    "SRC3072_15_2817_zero_attempt": RESIDUALS / "P8_Y5_R2FR_2817_MM_ML_KERNEL_ZERO_ATTEMPT.csv",
    "SRC3072_16_3070_kernel_audit": RESIDUALS / "P8_Y5_R2FR_3070_KMETRIC_KERNEL_NORM_AUDIT.csv",
    "SRC3072_17_3070_bound_vector": RESIDUALS / "P8_Y5_R2FR_3070_DELTA_G_SGAMMA_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3072_18_gk_contract": RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "SRC3072_19_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3072_SOURCE_REGISTER.csv",
    "double_zero": RESIDUALS / "P8_Y5_R2FR_3072_SOURCE_ROOT_DOUBLE_ZERO_AUDIT.csv",
    "local_lock": RESIDUALS / "P8_Y5_R2FR_3072_LOCAL_LOCK_DELTA_M_AMPLITUDE_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3072_MM_ML_COEFFICIENT_BOUND_ROWS_NONCLAIM.csv",
    "hidden": RESIDUALS / "P8_Y5_R2FR_3072_HIDDEN_KERNEL_CONSEQUENCE_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3072_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3072_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3072_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3072_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3072_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "double_zero_copy": PARENT_ACTION / "source_root_double_zero_audit_3072_UNSIGNED.csv",
    "local_lock_copy": PARENT_ACTION / "local_lock_Delta_m_amplitude_audit_3072_NOT_SIGNED.csv",
    "bound_copy": LOCAL_BOUNDS / "Mm_ML_coefficient_bound_rows_3072_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3072_hidden_kernel_silence_or_bound_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        "amplitude_law_signed",
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


dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": str(path.exists()),
            "parse_ok": str(source_parse_ok(path)),
            "row_count": row_count(path),
            "role": "source_root_double_zero_local_lock_evidence" if source_id != "SRC3072_19_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

double_zero_rows = [
    base(
        {
            "audit_id": "DZ3072_0_parent_source_root",
            "target": "F(m_*)=0",
            "derivation_attempt": "Treat Gamma_eff=L_cg^-2 F(m) as a vacuum-subtracted local source; the L_cg chain coefficient vanishes if the parent action selects a root m_* with F(m_*)=0.",
            "derived_result": "SUFFICIENT_CONDITION_RECONFIRMED_NOT_PARENT_SIGNED",
            "certificate_signed": "false",
            "algebraic_zero": "conditional",
            "missing_for_claim": "MISSING_PARENT_SOURCE_ROOT;MISSING_BACKGROUND_SUBTRACTION_RULE;MISSING_NO_FITTED_PER_SYSTEM_ROOT",
            "source_ids": "SRC3072_04_1532_lcg_zero;SRC3072_05_1532_double_zero;SRC3072_10_2734_root_lock",
        }
    ),
    base(
        {
            "audit_id": "DZ3072_1_stationary_root",
            "target": "F'(m_*)=0",
            "derivation_attempt": "A local extremum of the parent source functional would force the first derivative coefficient to vanish, deleting the linear M_m chain at exact lock.",
            "derived_result": "EXTREMUM_LAW_IDENTIFIED_BUT_UNSIGNED",
            "certificate_signed": "false",
            "algebraic_zero": "conditional",
            "missing_for_claim": "MISSING_PARENT_EULER_EQUATION_FOR_m;MISSING_PARENT_SELECTION_OF_m_STAR;MISSING_FPRIME_ZERO_THEOREM",
            "source_ids": "SRC3072_05_1532_double_zero;SRC3072_12_798_gamma_source;SRC3072_14_2816_zero_audit",
        }
    ),
    base(
        {
            "audit_id": "DZ3072_2_double_zero",
            "target": "F(m_*)=F'(m_*)=0",
            "derivation_attempt": "Taylor expand F(m_*+delta m)=F0+F1 delta m+1/2 F2 delta m^2+...; algebraic M_L and M_m coefficients both vanish at exact lock only when F0=F1=0.",
            "derived_result": "EXACT_CHAIN_ZERO_IF_DOUBLE_ZERO_AND_EXACT_LOCK",
            "certificate_signed": "false",
            "algebraic_zero": "conditional",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_LOCAL_LOCK_THEOREM;MISSING_HIDDEN_KERNEL_SILENCE",
            "source_ids": "SRC3072_02_3071_source_root;SRC3072_04_1532_lcg_zero;SRC3072_05_1532_double_zero;SRC3072_13_1289_derivative",
        }
    ),
    base(
        {
            "audit_id": "DZ3072_3_same_branch_guard",
            "target": "anti-smuggling guard",
            "derivation_attempt": "The root, stationary condition, Hilbert variation, local vacuum branch, and Kmetric response must belong to the same parent action branch.",
            "derived_result": "GUARD_RETAINED",
            "certificate_signed": "false",
            "algebraic_zero": "guard_only",
            "missing_for_claim": "MISSING_SINGLE_PARENT_ACTION_SIGNING_ALL_CLAUSES;MISSING_VARIATION_CONVENTION_LOCK",
            "source_ids": "SRC3072_04_1532_lcg_zero;SRC3072_05_1532_double_zero",
        }
    ),
    base(
        {
            "audit_id": "DZ3072_4_current_verdict",
            "target": "source-root double-zero route",
            "derivation_attempt": "The route is the cleanest algebraic path because it kills coefficients rather than declaring M_m or M_L absent.",
            "derived_result": "BEST_ROUTE_NOT_CLOSED_RETAIN_BOUND_FALLBACK",
            "certificate_signed": "false",
            "algebraic_zero": "not_claimed",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO_AND_LOCAL_LOCK;MISSING_DELTA_m_AMPLITUDE_LAW;MISSING_HIDDEN_KERNEL_BOUNDS",
            "source_ids": "SRC3072_03_3071_bound_vector;SRC3072_08_2734_ml_bound;SRC3072_17_3070_bound_vector",
        }
    ),
]

local_lock_rows = [
    base(
        {
            "lock_id": "LL3072_0_exact_lock",
            "quantity": "delta m",
            "candidate_law": "delta m=0 in the local test collar",
            "derivation_status": "NOT_SIGNED",
            "amplitude_law_signed": "false",
            "amplitude_bound": "Delta_m=0 only with parent no-hair/local-lock theorem",
            "missing_for_claim": "MISSING_LOCAL_LOCK_NO_HAIR_THEOREM;MISSING_BOUNDARY_COLLAR_EXCLUSION;MISSING_SOURCE_SUPPORT_ZERO",
            "source_ids": "SRC3072_05_1532_double_zero;SRC3072_12_798_gamma_source;SRC3072_14_2816_zero_audit",
        }
    ),
    base(
        {
            "lock_id": "LL3072_1_static_relaxation_bound",
            "quantity": "Delta_m",
            "candidate_law": "(-D_m Delta + M_scr^2)delta m = U_B S_cg + drift(m_L,L_cg,Pi_B,mu_B) + boundary",
            "derivation_status": "SCHEMATIC_SOURCE_BACKED_NOT_NUMERIC",
            "amplitude_law_signed": "false",
            "amplitude_bound": "Delta_m <= C_lock (U_B^pS S_cg_bar + D_drift_bar + B_boundary_bar)/M_scr^2",
            "missing_for_claim": "MISSING_D_m;MISSING_M_scr;MISSING_C_LOCK;MISSING_SOURCE_NORMS;MISSING_DRIFT_BOUND;MISSING_BOUNDARY_FLUX_BOUND",
            "source_ids": "SRC3072_12_798_gamma_source",
        }
    ),
    base(
        {
            "lock_id": "LL3072_2_screened_scaling",
            "quantity": "source-gradient scaling",
            "candidate_law": "If delta m=O(U_B^pS), grad delta m=O(U_B^pS/L_tr), baseline drifts are O(U_B^pL,U_B^pT), then s=O(U_B^(2pS),U_B^pL,U_B^pT)/L_tr.",
            "derivation_status": "CONDITIONAL_SCALING_ONLY",
            "amplitude_law_signed": "false",
            "amplitude_bound": "requires sourced pS,pL,pT,U_B,L_tr and observable projection",
            "missing_for_claim": "MISSING_SCREENING_EXPONENTS;MISSING_U_B_BOUND;MISSING_L_TR;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3072_12_798_gamma_source",
        }
    ),
    base(
        {
            "lock_id": "LL3072_3_transition_support",
            "quantity": "local transition collar",
            "candidate_law": "The finite off-root branch is safe only if transition support is outside or suppressed within the experimental local domain.",
            "derivation_status": "OPEN_SUPPORT_THEOREM",
            "amplitude_law_signed": "false",
            "amplitude_bound": "Delta_m support and gradients must be tied to collar geometry before PPN/R10 use",
            "missing_for_claim": "MISSING_TRANSITION_SUPPORT_THEOREM;MISSING_COLLAR_GEOMETRY;MISSING_DOMAIN_PROJECTOR_COMMUTATOR",
            "source_ids": "SRC3072_10_2734_root_lock;SRC3072_16_3070_kernel_audit",
        }
    ),
]

bound_rows = [
    base(
        {
            "row_id": "BND3072_0_master_retained",
            "quantity": "E_SGamma",
            "formula": "(2/3)(L_cg^-2|F'| M_m_bar + 2 L_cg^-3|F| M_L_bar + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "status": "MASTER_BOUND_RETAINED_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "MISSING_KERNEL_VECTOR",
            "missing_for_claim": "MISSING_M_m_BAR;MISSING_M_L_BAR;MISSING_K_CONN;MISSING_K_DOMAIN;MISSING_K_BOUNDARY;MISSING_UNITS",
            "source_ids": "SRC3072_03_3071_bound_vector;SRC3072_17_3070_bound_vector",
        }
    ),
    base(
        {
            "row_id": "BND3072_1_root_only",
            "quantity": "E_SGamma_root_only",
            "formula": "(2/3)(L_min^-2(F1_bar+F2_bar Delta_m)M_m_bar + 2L_min^-3(F1_bar Delta_m + 1/2 F2_bar Delta_m^2)M_L_bar + hidden kernels)",
            "status": "ROOT_ONLY_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "F(m_*)=0 without F'(m_*)=0 keeps m-chain leakage",
            "missing_for_claim": "MISSING_PARENT_SOURCE_ROOT;MISSING_F1_BAR;MISSING_F2_BAR;MISSING_DELTA_m;MISSING_KERNEL_NORMS",
            "source_ids": "SRC3072_08_2734_ml_bound;SRC3072_09_2734_ml_inputs",
        }
    ),
    base(
        {
            "row_id": "BND3072_2_stationary_only",
            "quantity": "E_SGamma_stationary_only",
            "formula": "(2/3)(L_min^-2 F2_bar Delta_m M_m_bar + 2L_min^-3 |F0| M_L_bar + hidden kernels + higher terms)",
            "status": "STATIONARY_ONLY_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "F'(m_*)=0 without F(m_*)=0 leaves L_cg leakage",
            "missing_for_claim": "MISSING_F0_OR_SOURCE_ROOT;MISSING_DELTA_m;MISSING_M_m_BAR;MISSING_M_L_BAR;MISSING_HIDDEN_KERNELS",
            "source_ids": "SRC3072_05_1532_double_zero;SRC3072_12_798_gamma_source",
        }
    ),
    base(
        {
            "row_id": "BND3072_3_double_zero_finite_lock",
            "quantity": "E_SGamma_double_zero_Delta_m",
            "formula": "(2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + ||K_conn|| + ||K_domain|| + ||K_boundary|| + higher terms)",
            "status": "BEST_ALGEBRAIC_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "double-zero makes M_m leakage linear in Delta_m and M_L leakage quadratic in Delta_m",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_DELTA_m_AMPLITUDE_LAW;MISSING_F2_BAR;MISSING_L_MIN;MISSING_M_m_BAR;MISSING_M_L_BAR;MISSING_HIDDEN_KERNEL_BOUNDS",
            "source_ids": "SRC3072_08_2734_ml_bound;SRC3072_12_798_gamma_source;SRC3072_13_1289_derivative",
        }
    ),
    base(
        {
            "row_id": "BND3072_4_exact_lock_double_zero",
            "quantity": "E_SGamma_algebraic_chain",
            "formula": "0 for algebraic M_m/M_L coefficients if F(m_*)=F'(m_*)=0 and delta m=0; hidden kernels are separate",
            "status": "EXACT_CHAIN_ZERO_CONDITIONAL_NOT_CLAIMED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "symbolic_value": "algebraic chain can vanish without proving local GR",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_EXACT_LOCAL_LOCK;MISSING_K_CONN_DOMAIN_BOUNDARY_ZERO",
            "source_ids": "SRC3072_04_1532_lcg_zero;SRC3072_05_1532_double_zero;SRC3072_16_3070_kernel_audit",
        }
    ),
]

hidden_rows = [
    base(
        {
            "hidden_id": "HK3072_0_K_conn",
            "kernel": "K_conn",
            "status": "RETAINED_OPEN_KERNEL",
            "reason": "double-zero only addresses algebraic F/F' chain coefficients, not metric variation of connections, derivative operators, Hodge maps, or field-space metric",
            "next_requirement": "derive connection/operator metric-response silence or source a finite norm bound",
            "missing_for_claim": "MISSING_CONNECTION_VARIATION;MISSING_DERIVATIVE_OPERATOR_RESPONSE;MISSING_HELMHOLTZ_INTEGRABILITY_BOUND",
            "source_ids": "SRC3072_16_3070_kernel_audit;SRC3072_13_1289_derivative",
        }
    ),
    base(
        {
            "hidden_id": "HK3072_1_K_domain",
            "kernel": "K_domain",
            "status": "RETAINED_OPEN_KERNEL",
            "reason": "local projector/domain/collar metric response can reintroduce residuals even when source coefficients vanish",
            "next_requirement": "prove P_loc/domain/collar silence or bind it as a projected residual",
            "missing_for_claim": "MISSING_PLOC_DOMAIN_COMMUTATOR;MISSING_COLLAR_GEOMETRY;MISSING_PROJECTOR_SILENCE",
            "source_ids": "SRC3072_16_3070_kernel_audit",
        }
    ),
    base(
        {
            "hidden_id": "HK3072_2_K_boundary",
            "kernel": "K_boundary",
            "status": "RETAINED_OPEN_KERNEL",
            "reason": "transition support and boundary flux determine whether off-root leakage reaches the local arena",
            "next_requirement": "derive no-flux/boundary-collar theorem or source a boundary flux bound",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX;MISSING_TRANSITION_SUPPORT_THEOREM;MISSING_BOUNDARY_FLUX_BOUND",
            "source_ids": "SRC3072_12_798_gamma_source;SRC3072_16_3070_kernel_audit",
        }
    ),
    base(
        {
            "hidden_id": "HK3072_3_observable_projection",
            "kernel": "PPN/R10/clock/orbital readout",
            "status": "NOT_PROMOTED",
            "reason": "a formal residual bound is not an arena pass until projected into observables with units and baselines",
            "next_requirement": "after hidden kernels are bounded, map residual vector into PPN, R10, clocks, orbital and WEP rows",
            "missing_for_claim": "MISSING_OBSERVABLE_PROJECTION;MISSING_UNITS;MISSING_ARENA_BASELINES",
            "source_ids": "SRC3072_16_3070_kernel_audit;SRC3072_17_3070_bound_vector",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3072_0_proof_result",
            "question": "Can 3072 prove F(m_*)=F'(m_*)=0 and exact local lock from existing parent sources?",
            "answer": "No; existing sources make it the clean route but still mark parent source root, stationary root, and local-lock/no-hair clauses unsigned.",
            "route_status": "DERIVATION_ROUTE_OPEN_NOT_CLAIMED",
            "next_action": "attack hidden kernels while preserving double-zero as conditional best algebraic branch",
        }
    ),
    base(
        {
            "decision_id": "DEC3072_1_useful_gain",
            "question": "What did this checkpoint add?",
            "answer": "It converts the local extremum idea into explicit amplitude laws: exact double-zero kills algebraic chain; finite lock leaves M_m leakage linear in Delta_m and M_L leakage quadratic in Delta_m.",
            "route_status": "BOUND_SHARPENED",
            "next_action": "source or derive Delta_m, F2_bar, M_m_bar, M_L_bar and hidden kernel norms",
        }
    ),
    base(
        {
            "decision_id": "DEC3072_2_next_target",
            "question": "Best next target?",
            "answer": "Do not circle bare M_m/M_L zero again; go after K_conn/K_domain/K_boundary silence or finite bounds, because those survive even under a perfect double-zero.",
            "route_status": "NEXT_TARGET_SELECTED",
            "next_action": "3073 hidden-kernel silence-or-bound vector fill",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3072_0_double_zero",
            "claim": "F(m_*)=F'(m_*)=0 is parent-derived",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "same-branch parent root, stationarity and local-lock theorem remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3072_1_local_gr",
            "claim": "local GR/Newton/PPN/R10 pass",
            "claim_active": "false",
            "status": "BLOCKED",
            "reason": "algebraic coefficient control is not enough; hidden kernels and observable projection are open",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3072_2_bound_only",
            "claim": "3072 supplies private nonclaim bound rows",
            "claim_active": "false",
            "status": "PRIVATE_NONCLAIM_LEDGER",
            "reason": "bounds are symbolic and missing sourced constants",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3072_0_3073",
            "next_checkpoint": "3073-Y5-R2FR-hidden-kernel-silence-or-bound-vector-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_hidden_kernel_silence_or_bound_vector_fill_under_AX1090_3073.py",
            "mission": "derive or bound K_conn, K_domain, and K_boundary after the double-zero/local-lock algebraic route remains unsigned",
            "starting_equation": "E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "claim_policy": "no Khat/q_loc/local-GR claim unless hidden kernels, units, and observable projections are source-backed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["double_zero"], double_zero_rows)
write_csv(OUTPUTS["local_lock"], local_lock_rows)
write_csv(OUTPUTS["bounds"], bound_rows)
write_csv(OUTPUTS["hidden"], hidden_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["double_zero"], BRANCH_OUTPUTS["double_zero_copy"])
copy_csv(OUTPUTS["local_lock"], BRANCH_OUTPUTS["local_lock_copy"])
copy_csv(OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(src),
            "copy_path": str(dst),
            "copy_exists": str(dst.exists()),
            "copy_parse_ok": str(csv_ok(dst)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, src, dst in [
        ("BC3072_0_double_zero", OUTPUTS["double_zero"], BRANCH_OUTPUTS["double_zero_copy"]),
        ("BC3072_1_local_lock", OUTPUTS["local_lock"], BRANCH_OUTPUTS["local_lock_copy"]),
        ("BC3072_2_bound_rows", OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_copy"]),
        ("BC3072_3_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3072_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3072 draft\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)

generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
formalization_3072 = list(FORMALIZATION.rglob("*3072*")) if FORMALIZATION.exists() else []

validation_rows = [
    base(
        {
            "validation_id": "VAL3072_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_02_csv_parse",
            "passed": str(all(csv_ok(path) for path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3072_03_double_zero_unsigned",
            "passed": str(not any(boolish(row["certificate_signed"]) for row in double_zero_rows)),
            "requirement": "double-zero theorem remains unsigned",
            "evidence": OUTPUTS["double_zero"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_04_local_lock_not_signed",
            "passed": str(not any(boolish(row["amplitude_law_signed"]) for row in local_lock_rows)),
            "requirement": "local-lock Delta_m amplitude law remains not signed",
            "evidence": OUTPUTS["local_lock"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_05_bound_rows_nonclaim",
            "passed": str(not has_claim_true(bound_rows)),
            "requirement": "coefficient bound rows remain nonclaim and nonnumeric",
            "evidence": OUTPUTS["bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_06_hidden_kernels_retained",
            "passed": str(all("RETAINED" in row["status"] or row["status"] == "NOT_PROMOTED" for row in hidden_rows)),
            "requirement": "K_conn, K_domain, K_boundary and observable projection remain open",
            "evidence": OUTPUTS["hidden"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_07_no_local_gr_claim",
            "passed": str(not has_claim_true(claim_rows)),
            "requirement": "no Khat, q_loc, local-GR, PPN, R10, clock or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_08_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3073-Y5-R2FR-hidden-kernel")),
            "requirement": "next target moves to hidden-kernel silence or bound fill",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_09_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_10_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3072_11_outputs_under_post_checkpoint",
            "passed": str(all(under(path, ROOT) for path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3072_12_no_formalization_workbench_outputs",
            "passed": str(not formalization_3072 and all(not under(path, FORMALIZATION) for path in generated_csvs + [DOC])),
            "requirement": "formalization-workbench modified-file count for 3072 outputs remains zero",
            "evidence": f"formalization_3072_matches={len(formalization_3072)}",
        }
    ),
    base(
        {
            "validation_id": "VAL3072_13_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3072_14_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3072_15_amplitude_formula_contains_Delta_m",
            "passed": str(any("Delta_m <=" in row["amplitude_bound"] for row in local_lock_rows)),
            "requirement": "finite local-lock amplitude bound is explicit",
            "evidence": OUTPUTS["local_lock"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3072_16_double_zero_bound_contains_linear_and_quadratic_leakage",
            "passed": str(any("Delta_m M_m_bar" in row["formula"] and "Delta_m^2 M_L_bar" in row["formula"] for row in bound_rows)),
            "requirement": "double-zero finite-lock bound records linear M_m and quadratic M_L leakage",
            "evidence": OUTPUTS["bounds"].name,
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3072 — Source-Root Double-Zero Local Lock or Mm/ML Bound Fill

Status: `Y5_R2FR_3072_double_zero_local_lock_not_signed_hidden_kernels_next`

Generated: `{RUN_UTC}`

## Verdict

3072 tried the cleanest derivation route: make the local source branch choose a root and stationary point,

`F(m_*)=0`, `F'(m_*)=0`,

then lock the local domain to `m=m_*+delta m` with a controlled amplitude `|delta m| <= Delta_m`.

The result is useful but not yet claimable. Existing sources already support the chain identity and the conditional double-zero contract, but they do **not** parent-sign the source root, the stationary-root theorem, or the local-lock/no-hair amplitude law. Therefore 3072 does **not** claim `Khat`, `q_loc=0`, local GR, PPN, R10, clock, WEP, or orbital success.

The gain is sharper than the previous checkpoint: if a future parent action supplies the double zero and a finite local-lock amplitude, the algebraic residual scales as

`E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + ||K_conn|| + ||K_domain|| + ||K_boundary|| + higher terms)`.

So the `M_m` leakage is linear in `Delta_m`, the `M_L` leakage is quadratic in `Delta_m`, and the hidden kernels remain the next wall.

## Double-Zero Audit

{md_table(double_zero_rows, ["audit_id", "target", "derived_result", "certificate_signed", "missing_for_claim"])}

## Local-Lock / Delta_m Audit

{md_table(local_lock_rows, ["lock_id", "quantity", "derivation_status", "amplitude_bound", "missing_for_claim"])}

## Coefficient Bounds

{md_table(bound_rows, ["row_id", "quantity", "status", "formula", "missing_for_claim"])}

## Hidden Kernel Consequence

{md_table(hidden_rows, ["hidden_id", "kernel", "status", "next_requirement", "missing_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "answer", "route_status", "next_action"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Double-zero audit: `{OUTPUTS["double_zero"]}`
- Local-lock audit: `{OUTPUTS["local_lock"]}`
- Bound rows: `{OUTPUTS["bounds"]}`
- Hidden kernel ledger: `{OUTPUTS["hidden"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
write_csv(OUTPUTS["validation"], validation_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

failed = [row for row in validation_rows if row["passed"] != "True"]
print(f"wrote {DOC}")
print(f"validation passed {len(validation_rows) - len(failed)}/{len(validation_rows)}")
if failed:
    for row in failed:
        print(f"FAILED {row['validation_id']}: {row['requirement']} :: {row['evidence']}")
    raise SystemExit(1)
