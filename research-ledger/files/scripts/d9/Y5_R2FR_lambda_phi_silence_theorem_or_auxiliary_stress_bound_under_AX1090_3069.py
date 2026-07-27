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

CHECKPOINT = "3069"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3069-Y5-R2FR-lambda-phi-silence-theorem-or-auxiliary-stress-bound-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3069_00_3068_doc": ROOT / "3068-Y5-R2FR-phi-owner-source-equation-or-tracefree-route-demotion-under-AX1090.md",
    "SRC3069_01_3068_next": RESIDUALS / "P8_Y5_R2FR_3068_NEXT_TARGET.csv",
    "SRC3069_02_3068_aux_variation": RESIDUALS / "P8_Y5_R2FR_3068_LOCAL_AUXILIARY_ACTION_VARIATION_AUDIT.csv",
    "SRC3069_03_3068_lambda_stress": RESIDUALS / "P8_Y5_R2FR_3068_LAMBDA_PHI_STRESS_AND_BOUND_ROWS_NONCLAIM.csv",
    "SRC3069_04_1527_multiplier_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_MULTIPLIER_STRESS_SILENCE_GATE.csv",
    "SRC3069_05_1528_energy_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
    "SRC3069_06_1529_doc": ROOT / "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
    "SRC3069_07_1529_boundary_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "SRC3069_08_1529_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_1529_CERTIFICATE_OR_BOUND_RUNNER.csv",
    "SRC3069_09_1529_bound_inputs": RESIDUALS / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv",
    "SRC3069_10_1530_doc": ROOT / "1530-Y5-lambda-phi-bound-input-source-pass.md",
    "SRC3069_11_1530_bound_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_ANALYTIC_BOUND_CONTRACT.csv",
    "SRC3069_12_1530_source_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_BOUND_INPUT_SOURCE_AUDIT.csv",
    "SRC3069_13_1530_dg_sgamma": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv",
    "SRC3069_14_1530_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1530_DECISION.csv",
    "SRC3069_15_1540_doc": ROOT / "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
    "SRC3069_16_1540_selector": RESIDUALS / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
    "SRC3069_17_1540_payoff": RESIDUALS / "P8_Y5_PARENT_QLOC_1540_SOURCE_SILENCE_PAYOFF.csv",
    "SRC3069_18_1540_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1540_DECISION.csv",
    "SRC3069_19_2713_boundary_gate": RESIDUALS / "P8_Y5_R2FR_2713_LAMBDA_PHI_BOUNDARY_GATE.csv",
    "SRC3069_20_2714_zero_attempt": RESIDUALS / "P8_Y5_R2FR_2714_LAMBDA_PHI_ZERO_ATTEMPT.csv",
    "SRC3069_21_1192_parent_phi": RESIDUALS / "P8_Y5_R10_1192_PARENT_PHI_SOURCE_AUDIT.csv",
    "SRC3069_22_1193_ricci_branch": RESIDUALS / "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
    "SRC3069_23_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3069_SOURCE_REGISTER.csv",
    "zero_theorem": RESIDUALS / "P8_Y5_R2FR_3069_LAMBDA_PHI_ZERO_THEOREM_AUDIT.csv",
    "stress_envelope": RESIDUALS / "P8_Y5_R2FR_3069_AUXILIARY_STRESS_BOUND_ENVELOPE_NONCLAIM.csv",
    "bound_inputs": RESIDUALS / "P8_Y5_R2FR_3069_BOUND_INPUT_REQUIREMENTS_NONCLAIM.csv",
    "consequence": RESIDUALS / "P8_Y5_R2FR_3069_KHAT_LOCAL_GR_CONSEQUENCE_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3069_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3069_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3069_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3069_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_theorem_copy": PARENT_ACTION / "lambda_phi_zero_theorem_audit_3069_NOT_SIGNED.csv",
    "stress_envelope_copy": LOCAL_BOUNDS / "auxiliary_lambda_phi_stress_bound_envelope_3069_NONCLAIM.csv",
    "bound_inputs_copy": LOCAL_BOUNDS / "lambda_phi_bound_input_requirements_3069_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3069_delta_g_SGamma_Kmetric_kernel_norms_NEXT_NONCLAIM.csv",
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
        "theorem_signed",
        "zero_claim",
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
            "role": "lambda_phi_silence_or_stress_bound_evidence" if source_id != "SRC3069_23_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

zero_theorem_rows = [
    base(
        {
            "audit_id": "LPZ3069_0_multiplier_equation",
            "clause": "lambda_phi field equation",
            "statement": "delta_phi S_phiK=0 gives Box lambda_phi=-c_I R plus convention and boundary terms",
            "result": "EQUATION_IMPORTED",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_SIGN_CONVENTION;MISSING_BOUNDARY_TERMS",
            "source_ids": "SRC3069_02_3068_aux_variation;SRC3069_05_1528_energy_theorem",
        }
    ),
    base(
        {
            "audit_id": "LPZ3069_1_static_elliptic_reduction",
            "clause": "Box to spatial elliptic operator",
            "statement": "on a parent-owned stationary local collar, Box lambda_phi reduces to +/- Delta_h lambda_phi",
            "result": "CONDITIONAL_REDUCTION",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_STATIC_BRANCH_CERTIFICATE;MISSING_DOMAIN_METRIC_CERTIFICATE",
            "source_ids": "SRC3069_05_1528_energy_theorem;SRC3069_07_1529_boundary_audit",
        }
    ),
    base(
        {
            "audit_id": "LPZ3069_2_Ricci_flat_harmonic",
            "clause": "Ricci-flat harmonic branch",
            "statement": "if R=0 in the same parent local-vacuum branch, Delta_h lambda_phi=0",
            "result": "CONDITIONAL_HARMONIC_ROUTE",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_PARENT_RICCI_FLAT_DOMAIN;MISSING_SAME_BRANCH_LOCAL_VACUUM_CERTIFICATE",
            "source_ids": "SRC3069_04_1527_multiplier_gate;SRC3069_05_1528_energy_theorem;SRC3069_22_1193_ricci_branch",
        }
    ),
    base(
        {
            "audit_id": "LPZ3069_3_energy_identity",
            "clause": "harmonic no-hair identity",
            "statement": "int_D |grad lambda_phi|_h^2 dV = int_boundary lambda_phi n.grad(lambda_phi)dS - int_D lambda_phi Delta_h lambda_phi dV",
            "result": "ENERGY_IDENTITY_DERIVED_CONDITIONAL",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_POSITIVE_SPATIAL_METRIC;MISSING_DIFFERENTIABLE_BOUNDARY_DATA",
            "source_ids": "SRC3069_05_1528_energy_theorem",
        }
    ),
    base(
        {
            "audit_id": "LPZ3069_4_boundary_zero_mode",
            "clause": "boundary and zero-mode certificate",
            "statement": "Dirichlet lambda_phi=0, or Neumann/no-flux plus mean(lambda_phi)=0, would force lambda_phi=0 in the compact harmonic branch",
            "result": "ZERO_THEOREM_CONDITIONAL_ONLY",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_BOUNDARY_CONDITION_CERTIFICATE;MISSING_ZERO_MODE_CERTIFICATE;MISSING_SOURCE_BOUNDARY_MATCHING",
            "source_ids": "SRC3069_07_1529_boundary_audit;SRC3069_19_2713_boundary_gate;SRC3069_20_2714_zero_attempt",
        }
    ),
    base(
        {
            "audit_id": "LPZ3069_5_current_verdict",
            "clause": "current zero theorem status",
            "statement": "lambda_phi stress is theorem-zero only if all previous clauses are parent-signed in one branch",
            "result": "ZERO_THEOREM_NOT_CLOSED",
            "theorem_signed": "false",
            "zero_claim": "false",
            "missing_for_claim": "MISSING_PARENT_DOMAIN;MISSING_BOUNDARY;MISSING_ZERO_MODE;MISSING_RICCI_FLAT_OR_BOUND",
            "source_ids": "SRC3069_08_1529_runner;SRC3069_20_2714_zero_attempt",
        }
    ),
]

stress_envelope_rows = [
    base(
        {
            "envelope_id": "ASE3069_0_A_source_norm",
            "quantity": "A_lambda",
            "definition": "source amplitude for the lambda_phi equation",
            "formula": "A_lambda = |c_I| ||R|| + boundary_source_norm + initial_data_norm",
            "status": "COMPOSITE_SOURCE_NORM_DEFINED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_c_I;MISSING_R_NORM;MISSING_BOUNDARY_SOURCE_NORM;MISSING_INITIAL_DATA_NORM",
            "source_ids": "SRC3069_09_1529_bound_inputs;SRC3069_11_1530_bound_contract",
        }
    ),
    base(
        {
            "envelope_id": "ASE3069_1_gradient_bound",
            "quantity": "||grad lambda_phi||",
            "definition": "elliptic gradient estimate in the local collar",
            "formula": "||grad lambda_phi|| <= C_E A_lambda",
            "status": "CONDITIONAL_ANALYTIC_BOUND",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_E;MISSING_ELLIPTIC_BRANCH;MISSING_REGULARITY_CLASS",
            "source_ids": "SRC3069_11_1530_bound_contract;SRC3069_12_1530_source_audit",
        }
    ),
    base(
        {
            "envelope_id": "ASE3069_2_poincare_bound",
            "quantity": "||lambda_phi||",
            "definition": "Poincare/zero-mode estimate",
            "formula": "||lambda_phi|| <= C_P C_E A_lambda",
            "status": "CONDITIONAL_ANALYTIC_BOUND",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_P;MISSING_ZERO_MODE_OWNER;MISSING_BOUNDARY_CLASS",
            "source_ids": "SRC3069_11_1530_bound_contract;SRC3069_12_1530_source_audit",
        }
    ),
    base(
        {
            "envelope_id": "ASE3069_3_stress_bound",
            "quantity": "epsilon_lambda_phi",
            "definition": "auxiliary multiplier stress envelope feeding DeltaK_TF and q_loc",
            "formula": "epsilon_lambda_phi <= |C_T|(C_E A_lambda)^2 + |C_T| C_P C_E A_lambda ||delta_g S_Gamma|| + boundary_flux",
            "status": "SYMBOLIC_BOUND_WRITTEN_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_DELTA_G_SGAMMA_NORM;MISSING_BOUNDARY_FLUX_BOUND;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3069_03_3068_lambda_stress;SRC3069_11_1530_bound_contract;SRC3069_13_1530_dg_sgamma",
        }
    ),
    base(
        {
            "envelope_id": "ASE3069_4_delta_g_SGamma_reduction",
            "quantity": "||delta_g S_Gamma||",
            "definition": "metric response norm of S_Gamma=(2/3)(Gamma_eff+C)",
            "formula": "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'| ||M_m|| + 2L_cg^-3|F| ||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "status": "REDUCED_TO_KMETRIC_KERNEL_NORMS",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_M_m;MISSING_M_L;MISSING_K_CONN;MISSING_K_DOMAIN;MISSING_K_BOUNDARY;MISSING_UNITS",
            "source_ids": "SRC3069_13_1530_dg_sgamma;SRC3069_14_1530_decision",
        }
    ),
]

bound_input_rows = [
    base({"input_id": "BIN3069_0_C_P", "quantity": "C_P", "role": "Poincare/zero-mode constant", "required_for": "||lambda_phi|| <= C_P ||grad lambda_phi||", "status": "MISSING_BOUND_CONSTANT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_09_1529_bound_inputs;SRC3069_12_1530_source_audit"}),
    base({"input_id": "BIN3069_1_C_E", "quantity": "C_E", "role": "elliptic gradient estimate constant", "required_for": "||grad lambda_phi|| <= C_E A_lambda", "status": "MISSING_BOUND_CONSTANT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_09_1529_bound_inputs;SRC3069_12_1530_source_audit"}),
    base({"input_id": "BIN3069_2_C_T", "quantity": "C_T", "role": "stress conversion/projection constant", "required_for": "epsilon_lambda_phi stress envelope", "status": "MISSING_BOUND_CONSTANT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_09_1529_bound_inputs;SRC3069_12_1530_source_audit"}),
    base({"input_id": "BIN3069_3_c_I", "quantity": "c_I", "role": "improvement coupling coefficient", "required_for": "A_lambda and K_L coefficient match", "status": "MISSING_PARENT_COEFFICIENT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_02_3068_aux_variation"}),
    base({"input_id": "BIN3069_4_R_norm", "quantity": "||R||", "role": "Ricci scalar source norm", "required_for": "non-Ricci-flat lambda_phi source", "status": "MISSING_SOURCE_NORM", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_09_1529_bound_inputs;SRC3069_12_1530_source_audit"}),
    base({"input_id": "BIN3069_5_boundary_source_norm", "quantity": "boundary_source_norm", "role": "boundary data amplitude", "required_for": "A_lambda and boundary flux", "status": "MISSING_BOUNDARY_INPUT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_07_1529_boundary_audit;SRC3069_09_1529_bound_inputs"}),
    base({"input_id": "BIN3069_6_initial_data_norm", "quantity": "initial_data_norm", "role": "Lorentzian/elliptic branch initial or reference data", "required_for": "A_lambda if static elliptic reduction is not fully signed", "status": "MISSING_BRANCH_INPUT", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_09_1529_bound_inputs"}),
    base({"input_id": "BIN3069_7_delta_g_SGamma_norm", "quantity": "||delta_g S_Gamma||", "role": "metric response of source term", "required_for": "lambda_phi S_Gamma stress term", "status": "REDUCED_BUT_NOT_NUMERIC", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_13_1530_dg_sgamma"}),
    base({"input_id": "BIN3069_8_observable_projection", "quantity": "Pi_obs", "role": "projection into PPN/R10/clock/orbital observables", "required_for": "score-ready local-GR residual comparison", "status": "MISSING_OBSERVABLE_PROJECTION", "numeric_ready": "false", "bound_ready": "false", "source_ids": "SRC3069_12_1530_source_audit"}),
]

consequence_rows = [
    base(
        {
            "consequence_id": "KLC3069_0_zero_theorem_payoff",
            "condition": "if lambda_phi=0 is parent-signed",
            "result": "auxiliary stress channel vanishes and the tracefree K_L route can return to Khat adoption/curvature/amplitude gates",
            "current_status": "CONDITIONAL_PAYOFF_ONLY",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "zero theorem clauses are not parent-signed",
        }
    ),
    base(
        {
            "consequence_id": "KLC3069_1_bound_payoff",
            "condition": "if epsilon_lambda_phi is numerically bounded below local limits",
            "result": "tracefree route can survive as a finite residual rather than exact local-GR theorem",
            "current_status": "SYMBOLIC_BOUND_ONLY",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "constants, curvature norm, delta_g S_Gamma norm and observable projection are missing",
        }
    ),
    base(
        {
            "consequence_id": "KLC3069_2_current_state",
            "condition": "current MTS source state",
            "result": "DeltaK_TF/q_loc/local-GR remain nonclaim; next shared bottleneck is delta_g S_Gamma Kmetric kernel norms",
            "current_status": "CLAIM_BLOCKED_BUT_BOUND_SCHEMA_SHARP",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "reason": "1530 already reduces the sharpest multiplier-stress term to Kmetric kernels",
        }
    ),
]

claim_rows = [
    base({"claim_id": "CLAIM3069_0_lambda_phi_zero", "claim": "lambda_phi=0 is proved in current MTS", "status": "NO_CONDITIONAL_ONLY", "claim_active": "false", "reason": "domain, boundary/no-flux, zero-mode and Ricci-flat branch are unsigned"}),
    base({"claim_id": "CLAIM3069_1_aux_stress_bounded", "claim": "auxiliary lambda_phi stress is numerically bounded below local limits", "status": "NO_SYMBOLIC_ONLY", "claim_active": "false", "reason": "bound constants and observable projection are missing"}),
    base({"claim_id": "CLAIM3069_2_Khat_adoption", "claim": "tracefree K_L can be promoted to live Khat", "status": "NO_LAMBDA_GATE_OPEN", "claim_active": "false", "reason": "lambda_phi stress is neither theorem-zero nor score-bounded"}),
    base({"claim_id": "CLAIM3069_3_local_GR_PPN", "claim": "local GR/PPN branch is derived", "status": "NO", "claim_active": "false", "reason": "DeltaK_TF/q_loc residual channel remains open"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3069_0_3070",
            "next_checkpoint": "3070-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norms-or-aux-stress-demotion-under-AX1090.md",
            "script": "scripts/Y5_R2FR_delta_g_SGamma_Kmetric_kernel_norms_or_aux_stress_demotion_under_AX1090_3070.py",
            "mission": "source or bound the Kmetric kernel norms inside ||delta_g S_Gamma||, because they are the shared bottleneck for lambda_phi stress, DeltaK_TF and q_loc",
            "starting_equation": "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'||M_m|| + 2L_cg^-3|F|||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "claim_policy": "no local-GR/Khat claim unless the kernel norms and observable projection are source-backed or theorem-zero",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["zero_theorem"], zero_theorem_rows)
write_csv(OUTPUTS["stress_envelope"], stress_envelope_rows)
write_csv(OUTPUTS["bound_inputs"], bound_input_rows)
write_csv(OUTPUTS["consequence"], consequence_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["zero_theorem"], BRANCH_OUTPUTS["zero_theorem_copy"])
copy_csv(OUTPUTS["stress_envelope"], BRANCH_OUTPUTS["stress_envelope_copy"])
copy_csv(OUTPUTS["bound_inputs"], BRANCH_OUTPUTS["bound_inputs_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": str(path.exists()),
            "row_count": row_count(path),
            "description": "3069 branch copy for parent-action/local-bound/acquisition-queue continuity",
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
zero_theorem_not_signed = any(row["audit_id"] == "LPZ3069_5_current_verdict" and row["result"] == "ZERO_THEOREM_NOT_CLOSED" for row in zero_theorem_rows)
all_zero_rows_nonclaim = all(row["theorem_signed"] == "false" and row["zero_claim"] == "false" and row["valid_for_claim"] == "false" for row in zero_theorem_rows)
energy_identity_present = any(row["audit_id"] == "LPZ3069_3_energy_identity" and "ENERGY_IDENTITY" in row["result"] for row in zero_theorem_rows)
stress_envelope_written = any(row["envelope_id"] == "ASE3069_3_stress_bound" and "delta_g S_Gamma" in row["formula"] for row in stress_envelope_rows)
dg_sgamma_reduced = any(row["envelope_id"] == "ASE3069_4_delta_g_SGamma_reduction" and row["status"] == "REDUCED_TO_KMETRIC_KERNEL_NORMS" for row in stress_envelope_rows)
all_stress_rows_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in stress_envelope_rows)
all_bound_inputs_missing = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and ("MISSING" in row["status"] or row["status"] == "REDUCED_BUT_NOT_NUMERIC") for row in bound_input_rows)
current_consequence_blocked = any(row["consequence_id"] == "KLC3069_2_current_state" and row["current_status"] == "CLAIM_BLOCKED_BUT_BOUND_SCHEMA_SHARP" for row in consequence_rows)
all_claims_inactive = all(row["claim_active"] == "false" for row in claim_rows)
next_is_3070 = next_rows[0]["next_checkpoint"].startswith("3070-")

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

validation_rows = [
    base({"validation_id": "VAL3069_00_sources_exist", "passed": all_sources_exist, "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3069_01_sources_parse", "passed": all_sources_parse, "requirement": "all cited CSV sources parse and markdown sources exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3069_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3069_03_zero_theorem_not_signed", "passed": zero_theorem_not_signed and all_zero_rows_nonclaim, "requirement": "lambda_phi zero theorem remains conditional and nonclaim", "evidence": OUTPUTS["zero_theorem"].name}),
    base({"validation_id": "VAL3069_04_energy_identity_retained", "passed": energy_identity_present, "requirement": "harmonic energy identity is retained as the conditional proof route", "evidence": OUTPUTS["zero_theorem"].name}),
    base({"validation_id": "VAL3069_05_stress_envelope_written", "passed": stress_envelope_written and all_stress_rows_nonclaim, "requirement": "auxiliary stress bound envelope is written but nonclaim", "evidence": OUTPUTS["stress_envelope"].name}),
    base({"validation_id": "VAL3069_06_delta_g_SGamma_shared_bottleneck", "passed": dg_sgamma_reduced, "requirement": "delta_g S_Gamma is reduced to Kmetric kernel norms", "evidence": OUTPUTS["stress_envelope"].name}),
    base({"validation_id": "VAL3069_07_bound_inputs_missing", "passed": all_bound_inputs_missing, "requirement": "bound inputs remain missing or reduced-but-not-numeric", "evidence": OUTPUTS["bound_inputs"].name}),
    base({"validation_id": "VAL3069_08_consequence_guarded", "passed": current_consequence_blocked, "requirement": "Khat/local-GR consequence remains explicitly blocked", "evidence": OUTPUTS["consequence"].name}),
    base({"validation_id": "VAL3069_09_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row activates Khat, q_loc, local-GR, R10, PPN, clock or orbital claims", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3069_10_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3069" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3069 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3069_11_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3069_12_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3069_13_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench generated-output count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3069_14_next_target", "passed": next_is_3070, "requirement": "next target selects delta_g S_Gamma Kmetric kernel norms", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3069_15_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3069 - Lambda Phi Silence Theorem or Auxiliary Stress Bound

Status: `Y5_R2FR_3069_lambda_phi_zero_not_signed_aux_stress_bound_reduced_to_Kmetric_kernels`

Generated: `{RUN_UTC}`

## Verdict

3069 tested the `lambda_phi` no-hair route.

The mathematical skeleton is sound in the right branch:

`Box lambda_phi = -c_I R`.

If the same parent branch gives a stationary compact local collar, `R=0`, Dirichlet `lambda_phi=0` or no-flux plus zero-mode fixing, then the harmonic energy identity forces `lambda_phi=0`. In that special branch the auxiliary stress would vanish.

But current MTS does **not** parent-sign the needed domain, boundary/no-flux, zero-mode, static elliptic, or same-branch Ricci-flat certificates. So 3069 does **not** claim `lambda_phi=0`.

The fallback is now sharper:

`epsilon_lambda_phi <= |C_T|(C_E A_lambda)^2 + |C_T| C_P C_E A_lambda ||delta_g S_Gamma|| + boundary_flux`,

with

`A_lambda = |c_I| ||R|| + boundary_source_norm + initial_data_norm`.

That is not numeric yet, but it is no longer vague. The sharpest shared bottleneck is now `||delta_g S_Gamma||`, already reduced to Kmetric kernel norms.

## Lambda Phi Zero Theorem Audit

{md_table(zero_theorem_rows, ["audit_id", "clause", "statement", "result", "theorem_signed", "zero_claim", "missing_for_claim"])}

## Auxiliary Stress Bound Envelope

{md_table(stress_envelope_rows, ["envelope_id", "quantity", "formula", "status", "numeric_ready", "bound_ready", "missing_for_claim"])}

## Bound Input Requirements

{md_table(bound_input_rows, ["input_id", "quantity", "role", "required_for", "status", "numeric_ready", "bound_ready"])}

## Khat and Local-GR Consequence Ledger

{md_table(consequence_rows, ["consequence_id", "condition", "result", "current_status", "local_gr_claim", "khat_claim", "reason"])}

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
    raise SystemExit(f"3069 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: lambda_phi zero theorem not signed; auxiliary stress bound reduced to delta_g S_Gamma/Kmetric kernels")
