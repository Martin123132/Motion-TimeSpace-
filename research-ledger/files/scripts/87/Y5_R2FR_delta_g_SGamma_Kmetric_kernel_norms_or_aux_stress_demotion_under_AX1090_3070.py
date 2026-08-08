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

CHECKPOINT = "3070"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3070-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norms-or-aux-stress-demotion-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3070_00_3069_doc": ROOT / "3069-Y5-R2FR-lambda-phi-silence-theorem-or-auxiliary-stress-bound-under-AX1090.md",
    "SRC3070_01_3069_next": RESIDUALS / "P8_Y5_R2FR_3069_NEXT_TARGET.csv",
    "SRC3070_02_3069_stress": RESIDUALS / "P8_Y5_R2FR_3069_AUXILIARY_STRESS_BOUND_ENVELOPE_NONCLAIM.csv",
    "SRC3070_03_3069_inputs": RESIDUALS / "P8_Y5_R2FR_3069_BOUND_INPUT_REQUIREMENTS_NONCLAIM.csv",
    "SRC3070_04_1530_dg_sgamma": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv",
    "SRC3070_05_1530_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_DECISION.csv",
    "SRC3070_06_1530_bound_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_ANALYTIC_BOUND_CONTRACT.csv",
    "SRC3070_07_1289_variation": RESIDUALS / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
    "SRC3070_08_1289_derivative_row": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3070_09_1367_kernel_attempt": RESIDUALS / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "SRC3070_10_776_kgamma": RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "SRC3070_11_798_gamma_source": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "SRC3070_12_2816_zero_audit": RESIDUALS / "P8_Y5_R2FR_2816_MM_ML_ZERO_PROOF_AUDIT.csv",
    "SRC3070_13_2817_zero_attempt": RESIDUALS / "P8_Y5_R2FR_2817_MM_ML_KERNEL_ZERO_ATTEMPT.csv",
    "SRC3070_14_2816_norm_map": RESIDUALS / "P8_Y5_R2FR_2816_KERNEL_NORMALIZATION_MAP.csv",
    "SRC3070_15_2814_fallback": RESIDUALS / "P8_Y5_R2FR_2814_KMETRIC00_KERNEL_FALLBACK_LEDGER.csv",
    "SRC3070_16_2975_sign": RESIDUALS / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "SRC3070_17_2976_gamma_owner": RESIDUALS / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "SRC3070_18_3065_gamma_owner_gate": RESIDUALS / "P8_Y5_R2FR_3065_GAMMA_EFF_DENSITY_OWNER_GATE.csv",
    "SRC3070_19_3016_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "SRC3070_20_3018_gamma_bound": RESIDUALS / "P8_Y5_R2FR_3018_GAMMA_BOUND_INTERFACE.csv",
    "SRC3070_21_3059_slip_kernel": RESIDUALS / "P8_Y5_R2FR_3059_EPSILON_GAMMA_SLIP_KERNEL_FORMULA.csv",
    "SRC3070_22_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3070_SOURCE_REGISTER.csv",
    "kernel_audit": RESIDUALS / "P8_Y5_R2FR_3070_KMETRIC_KERNEL_NORM_AUDIT.csv",
    "zero_branch": RESIDUALS / "P8_Y5_R2FR_3070_KERNEL_ZERO_BRANCH_AUDIT.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_3070_DELTA_G_SGAMMA_BOUND_VECTOR_NONCLAIM.csv",
    "consequence": RESIDUALS / "P8_Y5_R2FR_3070_AUX_STRESS_DELTAK_QLOC_CONSEQUENCE_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3070_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3070_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3070_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3070_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_audit_copy": LOCAL_BOUNDS / "Kmetric_kernel_norm_audit_3070_NONCLAIM.csv",
    "zero_branch_copy": PARENT_ACTION / "Kmetric_kernel_zero_branch_audit_3070_NOT_SIGNED.csv",
    "bound_vector_copy": LOCAL_BOUNDS / "delta_g_SGamma_bound_vector_3070_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3070_m_Lcg_parent_kernel_certificate_NEXT_NONCLAIM.csv",
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
        "numeric_ready",
        "bound_ready",
        "kernel_zero_proved",
        "kernel_score_ready",
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
            "role": "delta_g_SGamma_Kmetric_kernel_norm_evidence" if source_id != "SRC3070_22_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

kernel_audit_rows = [
    base(
        {
            "kernel_id": "KNA3070_0_master_envelope",
            "kernel": "||delta_g S_Gamma||",
            "formula": "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "source_status": "SYMBOLIC_NORM_ENVELOPE",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_ALL_COMPONENT_NORMS;MISSING_UNITS;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3070_04_1530_dg_sgamma;SRC3070_08_1289_derivative_row",
        }
    ),
    base(
        {
            "kernel_id": "KNA3070_1_M_m",
            "kernel": "M_m",
            "formula": "Hilbert-normalized metric-response kernel for m, M_m^{00}:=-2 delta m/delta g_00",
            "source_status": "CONDITIONAL_ZERO_OR_COUNTERBRANCH",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_m_DEFINITION;MISSING_DELTA_m_DELTA_g_ZERO_OR_BOUND;MISSING_UNITS",
            "source_ids": "SRC3070_12_2816_zero_audit;SRC3070_13_2817_zero_attempt;SRC3070_14_2816_norm_map",
        }
    ),
    base(
        {
            "kernel_id": "KNA3070_2_M_L",
            "kernel": "M_L",
            "formula": "Hilbert-normalized metric-response kernel for L_cg, M_L^{00}:=-2 delta L_cg/delta g_00",
            "source_status": "CONDITIONAL_FIXED_PARAMETER_OR_COUNTERBRANCH",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_LCG_DEFINITION;MISSING_LCG_METRIC_SILENCE_OR_BOUND;MISSING_UNITS",
            "source_ids": "SRC3070_12_2816_zero_audit;SRC3070_13_2817_zero_attempt;SRC3070_14_2816_norm_map",
        }
    ),
    base(
        {
            "kernel_id": "KNA3070_3_K_conn",
            "kernel": "K_conn",
            "formula": "connection/derivative metric response from nabla, Hodge, field-space metric and derivative operators",
            "source_status": "OPEN_KERNEL",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_CONNECTION_VARIATION;MISSING_DERIVATIVE_OPERATOR_RESPONSE;MISSING_HELMHOLTZ_INTEGRABILITY_BOUND",
            "source_ids": "SRC3070_09_1367_kernel_attempt;SRC3070_10_776_kgamma",
        }
    ),
    base(
        {
            "kernel_id": "KNA3070_4_K_domain",
            "kernel": "K_domain",
            "formula": "domain/projector/collar metric-response kernel",
            "source_status": "OPEN_KERNEL",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PLOC_DOMAIN_COMMUTATOR;MISSING_COLLAR_GEOMETRY;MISSING_PROJECTOR_SILENCE",
            "source_ids": "SRC3070_09_1367_kernel_attempt;SRC3070_10_776_kgamma",
        }
    ),
    base(
        {
            "kernel_id": "KNA3070_5_K_boundary",
            "kernel": "K_boundary",
            "formula": "boundary/reference/corner metric-response kernel",
            "source_status": "OPEN_KERNEL",
            "kernel_score_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_FIXED_REFERENCE_THEOREM;MISSING_BOUNDARY_NO_FLUX;MISSING_CORNER_TERM_BOUND",
            "source_ids": "SRC3070_09_1367_kernel_attempt;SRC3070_10_776_kgamma",
        }
    ),
]

zero_branch_rows = [
    base(
        {
            "zero_id": "KZB3070_0_Mm_fixed_field",
            "target": "M_m=0",
            "conditional_statement": "If m is a parent-owned independent scalar held fixed in the Hilbert variation, then M_m can vanish.",
            "current_status": "CONDITIONAL_RELATIVE_ZERO_NOT_LIVE",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_m_FIXED_FIELD_CLAUSE;MISSING_NO_METRIC_COMPOSITE_READOUT",
            "source_ids": "SRC3070_13_2817_zero_attempt",
        }
    ),
    base(
        {
            "zero_id": "KZB3070_1_Mm_counterbranch",
            "target": "M_m retained",
            "conditional_statement": "If m is metric-composite, norm-selected, curvature-derived or domain-selected, M_m generally survives.",
            "current_status": "COUNTERBRANCH_RETAINED",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_EXPLICIT_PARENT_m_DEFINITION_OR_FINITE_BOUND",
            "source_ids": "SRC3070_13_2817_zero_attempt",
        }
    ),
    base(
        {
            "zero_id": "KZB3070_2_ML_fixed_L0",
            "target": "M_L=0",
            "conditional_statement": "If L_cg=L0 is a fixed parent scalar parameter under Hilbert variation, then M_L can vanish.",
            "current_status": "EXACT_UNDER_CLOSURE_NOT_LIVE",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_FIXED_LCG_CLAUSE;MISSING_READOUT_DOMAIN_SEPARATION",
            "source_ids": "SRC3070_13_2817_zero_attempt",
        }
    ),
    base(
        {
            "zero_id": "KZB3070_3_ML_counterbranch",
            "target": "M_L retained",
            "conditional_statement": "If L_cg is a proper length, curvature scale, density scale, support radius or projector collar, M_L generally survives.",
            "current_status": "COUNTERBRANCH_RETAINED",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_LCG_PARENT_DEFINITION_OR_RESPONSE_COEFFICIENT",
            "source_ids": "SRC3070_13_2817_zero_attempt",
        }
    ),
    base(
        {
            "zero_id": "KZB3070_4_Fprime_fixed_point",
            "target": "F'(m_*)=0",
            "conditional_statement": "The m-channel linear leakage is removed if the parent locks the local state to a stationary point m_*.",
            "current_status": "CONDITIONAL_ONLY",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_PARENT_SELECTION_OF_m_STAR;MISSING_FPRIME_ZERO_THEOREM",
            "source_ids": "SRC3070_11_798_gamma_source;SRC3070_12_2816_zero_audit",
        }
    ),
    base(
        {
            "zero_id": "KZB3070_5_conn_domain_boundary",
            "target": "K_conn=K_domain=K_boundary=0",
            "conditional_statement": "Hidden derivative/domain/boundary kernels vanish only with same-branch connection, projector and fixed-reference silence.",
            "current_status": "NOT_PROVED",
            "kernel_zero_proved": "false",
            "missing_for_claim": "MISSING_K_CONN_ZERO;MISSING_K_DOMAIN_ZERO;MISSING_K_BOUNDARY_ZERO",
            "source_ids": "SRC3070_10_776_kgamma;SRC3070_12_2816_zero_audit",
        }
    ),
]

bound_vector_rows = [
    base(
        {
            "row_id": "DGSB3070_0_master",
            "quantity": "E_SGamma",
            "definition": "upper envelope for ||delta_g S_Gamma||",
            "bound_formula": "(2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "symbolic_value": "MISSING_KERNEL_VECTOR",
            "status": "BOUND_VECTOR_WRITTEN_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_COMPONENT_KERNELS;MISSING_UNITS;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3070_04_1530_dg_sgamma",
        }
    ),
    base(
        {
            "row_id": "DGSB3070_1_local_fixed_point_special_case",
            "quantity": "E_SGamma_fixed_point",
            "definition": "conditional small-kernel route at m=m_* with F'(m_*)=0 and L_cg metric silence",
            "bound_formula": "(2/3)(2L_cg^-3|F_*|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "symbolic_value": "MISSING_LCG_SILENCE_AND_HIDDEN_KERNELS",
            "status": "SPECIAL_CASE_CONDITIONAL_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_LOCK_TO_m_STAR;MISSING_LCG_METRIC_SILENCE;MISSING_HIDDEN_KERNEL_BOUNDS",
            "source_ids": "SRC3070_08_1289_derivative_row;SRC3070_11_798_gamma_source",
        }
    ),
    base(
        {
            "row_id": "DGSB3070_2_full_zero_gate",
            "quantity": "E_SGamma_zero",
            "definition": "exact zero route for the source-metric response",
            "bound_formula": "E_SGamma=0 if F'=0, M_L=0 or F=0, and K_conn=K_domain=K_boundary=0",
            "symbolic_value": "ZERO_GATE_CONDITIONAL_NOT_DERIVED",
            "status": "ZERO_GATE_NOT_SIGNED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_LOCK;MISSING_LCG_SILENCE;MISSING_BOUNDARY_DOMAIN_CONNECTION_SILENCE",
            "source_ids": "SRC3070_08_1289_derivative_row;SRC3070_12_2816_zero_audit",
        }
    ),
    base(
        {
            "row_id": "DGSB3070_3_aux_stress_substitution",
            "quantity": "epsilon_lambda_phi",
            "definition": "substitute E_SGamma into the lambda_phi stress envelope",
            "bound_formula": "epsilon_lambda_phi <= |C_T|(C_E A_lambda)^2 + |C_T|C_P C_E A_lambda E_SGamma + boundary_flux",
            "symbolic_value": "MISSING_A_LAMBDA_AND_E_SGAMMA",
            "status": "AUX_STRESS_DEMOTED_TO_BOUND_SCHEMA",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_P;MISSING_C_E;MISSING_C_T;MISSING_A_LAMBDA;MISSING_E_SGAMMA;MISSING_PROJECTION",
            "source_ids": "SRC3070_02_3069_stress;SRC3070_06_1530_bound_contract",
        }
    ),
]

consequence_rows = [
    base(
        {
            "consequence_id": "CON3070_0_progress",
            "question": "Did 3070 source numeric Kmetric kernel norms?",
            "answer": "NO",
            "result": "kernel vector is organized but not score-ready",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "all component kernels remain missing, conditional, or hidden-response terms",
        }
    ),
    base(
        {
            "consequence_id": "CON3070_1_real_gain",
            "question": "Did 3070 reduce the problem?",
            "answer": "YES",
            "result": "delta_g S_Gamma now has an official component vector and exact zero-gate clauses",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "the next target can focus on parent definitions of m and L_cg rather than repeating broad Kmetric hunts",
        }
    ),
    base(
        {
            "consequence_id": "CON3070_2_tracefree_route",
            "question": "What happens to the tracefree auxiliary route?",
            "answer": "RETAINED_AS_BOUND_BRANCH",
            "result": "lambda_phi stress remains a symbolic finite-residual branch feeding DeltaK_TF and q_loc",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "E_SGamma and A_lambda are not numeric or theorem-zero",
        }
    ),
]

claim_rows = [
    base({"claim_id": "CLAIM3070_0_delta_g_SGamma_bound", "claim": "||delta_g S_Gamma|| is source-backed or theorem-zero", "status": "NO_SYMBOLIC_ONLY", "claim_active": "false", "reason": "M_m, M_L, K_conn, K_domain and K_boundary are not numeric/theorem-zero"}),
    base({"claim_id": "CLAIM3070_1_aux_stress_bounded", "claim": "lambda_phi auxiliary stress is score-bounded", "status": "NO_BOUND_SCHEMA_ONLY", "claim_active": "false", "reason": "E_SGamma and A_lambda remain missing-input envelopes"}),
    base({"claim_id": "CLAIM3070_2_Khat_adoption", "claim": "tracefree K_L can be promoted to live Khat", "status": "NO_KERNEL_GATE_OPEN", "claim_active": "false", "reason": "Kmetric response remains missing component kernel norms"}),
    base({"claim_id": "CLAIM3070_3_local_GR_PPN", "claim": "local GR/PPN branch is derived", "status": "NO", "claim_active": "false", "reason": "DeltaK_TF/q_loc residual channel remains active"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3070_0_3071",
            "next_checkpoint": "3071-Y5-R2FR-m-Lcg-parent-kernel-certificate-or-Kmetric-bound-vector-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_m_Lcg_parent_kernel_certificate_or_Kmetric_bound_vector_fill_under_AX1090_3071.py",
            "mission": "try to parent-sign m as fixed/metric-silent and L_cg as fixed/metric-silent in the Hilbert variation; if not, retain M_m and M_L as explicit bound inputs",
            "starting_equation": "E_SGamma=(2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "claim_policy": "no Khat/q_loc/local-GR claim unless M_m/M_L and hidden kernels are zero or source-bounded in the same parent branch",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["kernel_audit"], kernel_audit_rows)
write_csv(OUTPUTS["zero_branch"], zero_branch_rows)
write_csv(OUTPUTS["bound_vector"], bound_vector_rows)
write_csv(OUTPUTS["consequence"], consequence_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["kernel_audit"], BRANCH_OUTPUTS["kernel_audit_copy"])
copy_csv(OUTPUTS["zero_branch"], BRANCH_OUTPUTS["zero_branch_copy"])
copy_csv(OUTPUTS["bound_vector"], BRANCH_OUTPUTS["bound_vector_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": str(path.exists()),
            "row_count": row_count(path),
            "description": "3070 branch copy for parent-action/local-bound/acquisition-queue continuity",
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
master_envelope_present = any(row["kernel_id"] == "KNA3070_0_master_envelope" and "delta_g S_Gamma" in row["kernel"] for row in kernel_audit_rows)
all_kernel_rows_nonclaim = all(row["kernel_score_ready"] == "false" and row["numeric_ready"] == "false" and row["bound_ready"] == "false" for row in kernel_audit_rows)
zero_branches_guarded = all(row["kernel_zero_proved"] == "false" and row["valid_for_claim"] == "false" for row in zero_branch_rows)
counterbranches_present = any(row["zero_id"] == "KZB3070_1_Mm_counterbranch" for row in zero_branch_rows) and any(row["zero_id"] == "KZB3070_3_ML_counterbranch" for row in zero_branch_rows)
bound_vector_written = any(row["row_id"] == "DGSB3070_0_master" and row["status"] == "BOUND_VECTOR_WRITTEN_NONCLAIM" for row in bound_vector_rows)
aux_substitution_present = any(row["row_id"] == "DGSB3070_3_aux_stress_substitution" and "epsilon_lambda_phi" in row["quantity"] for row in bound_vector_rows)
all_bound_vector_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in bound_vector_rows)
consequence_progress = any(row["consequence_id"] == "CON3070_1_real_gain" and row["answer"] == "YES" for row in consequence_rows)
all_claims_inactive = all(row["claim_active"] == "false" for row in claim_rows)
next_is_3071 = next_rows[0]["next_checkpoint"].startswith("3071-")

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

validation_rows = [
    base({"validation_id": "VAL3070_00_sources_exist", "passed": all_sources_exist, "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3070_01_sources_parse", "passed": all_sources_parse, "requirement": "all cited CSV sources parse and markdown sources exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3070_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3070_03_master_envelope_present", "passed": master_envelope_present and all_kernel_rows_nonclaim, "requirement": "delta_g S_Gamma master kernel envelope is recorded as nonclaim", "evidence": OUTPUTS["kernel_audit"].name}),
    base({"validation_id": "VAL3070_04_zero_branches_guarded", "passed": zero_branches_guarded and counterbranches_present, "requirement": "M_m/M_L zero routes are guarded and counterbranches retained", "evidence": OUTPUTS["zero_branch"].name}),
    base({"validation_id": "VAL3070_05_bound_vector_nonclaim", "passed": bound_vector_written and aux_substitution_present and all_bound_vector_nonclaim, "requirement": "bound vector and auxiliary-stress substitution are nonclaim", "evidence": OUTPUTS["bound_vector"].name}),
    base({"validation_id": "VAL3070_06_consequence_progress", "passed": consequence_progress, "requirement": "checkpoint records real progress without claim promotion", "evidence": OUTPUTS["consequence"].name}),
    base({"validation_id": "VAL3070_07_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row activates Khat, q_loc, local-GR, R10, PPN, clock or orbital claims", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3070_08_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3070" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3070 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3070_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3070_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3070_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench generated-output count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3070_12_next_target", "passed": next_is_3071, "requirement": "next target selects m/Lcg parent kernel certificate", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3070_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3070 - Delta g S_Gamma Kmetric Kernel Norms or Aux-Stress Demotion

Status: `Y5_R2FR_3070_delta_g_SGamma_kernel_vector_frozen_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3070 attacked the shared source-response bottleneck:

`||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)`.

No numeric kernel norm was sourced. But the kernel vector is now frozen into five explicit obligations: `M_m`, `M_L`, `K_conn`, `K_domain`, and `K_boundary`.

The conditional zero routes are also clear:

- `M_m=0` only if `m` is a parent-owned fixed field under Hilbert variation.
- `M_L=0` only if `L_cg` is a fixed parent scalar/parameter, not a metric-composite length, support scale or projector collar.
- `K_conn=K_domain=K_boundary=0` only if the same branch signs derivative, projector/collar and fixed-reference boundary silence.

Current MTS does not sign those clauses. So 3070 does **not** claim `delta_g S_Gamma=0`, a numeric auxiliary-stress bound, `Khat` adoption, `q_loc=0`, or local GR/PPN.

The win is that `lambda_phi` stress, `DeltaK_TF`, and `q_loc` now share the same official nonclaim kernel vector instead of three separate fog banks.

## Kmetric Kernel Norm Audit

{md_table(kernel_audit_rows, ["kernel_id", "kernel", "formula", "source_status", "kernel_score_ready", "missing_for_claim"])}

## Kernel Zero Branch Audit

{md_table(zero_branch_rows, ["zero_id", "target", "conditional_statement", "current_status", "kernel_zero_proved", "missing_for_claim"])}

## Delta g S_Gamma Bound Vector

{md_table(bound_vector_rows, ["row_id", "quantity", "bound_formula", "symbolic_value", "status", "numeric_ready", "bound_ready"])}

## Aux-Stress / DeltaK / q_loc Consequence Ledger

{md_table(consequence_rows, ["consequence_id", "question", "answer", "result", "local_gr_claim", "khat_claim", "reason"])}

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
    raise SystemExit(f"3070 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: delta_g S_Gamma kernel vector frozen; no numeric/source-backed Kmetric kernel norm claim")
