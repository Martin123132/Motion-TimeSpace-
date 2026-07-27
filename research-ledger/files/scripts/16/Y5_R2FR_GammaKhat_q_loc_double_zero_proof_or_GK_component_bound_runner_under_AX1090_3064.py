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

CHECKPOINT = "3064"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3064_00_3063_doc": ROOT / "3063-Y5-R2FR-extra-field-double-zero-proof-or-Delta-kST-component-bound-runner-under-AX1090.md",
    "SRC3064_01_3063_next": RESIDUALS / "P8_Y5_R2FR_3063_NEXT_TARGET.csv",
    "SRC3064_02_3063_runner": RESIDUALS / "P8_Y5_R2FR_3063_DELTA_KST_COMPONENT_BOUND_RUNNER_NONCLAIM.csv",
    "SRC3064_03_3063_sector_status": RESIDUALS / "P8_Y5_R2FR_3063_EXTRA_SECTOR_COMPONENT_STATUS.csv",
    "SRC3064_04_operator_inventory": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
    "SRC3064_05_leakage_residuals": RESIDUALS / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_LEAKAGE_RESIDUAL_ROWS.csv",
    "SRC3064_06_extra_silence": RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv",
    "SRC3064_07_gk_contract": RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "SRC3064_08_gk_integrability": RESIDUALS / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
    "SRC3064_09_gk_demotion": RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
    "SRC3064_10_1010_theorem": RESIDUALS / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
    "SRC3064_11_1010_schema": RESIDUALS / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv",
    "SRC3064_12_1010_residuals": RESIDUALS / "P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv",
    "SRC3064_13_1280_audit": RESIDUALS / "P8_Y5_R10_1280_HELMHOLTZ_EULER_DOUBLE_ZERO_AUDIT.csv",
    "SRC3064_14_1502_conditional": RESIDUALS / "P8_Y5_R10_1502_CONDITIONAL_HELMHOLTZ_THEOREM.csv",
    "SRC3064_15_2364_euler_vector": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_Q_EULER_RESIDUAL_VECTOR.csv",
    "SRC3064_16_2409_khat_match": RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "SRC3064_17_2581_proof_gate": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
    "SRC3064_18_2581_residual_interface": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
    "SRC3064_19_2941_strong_gate": RESIDUALS / "P8_Y5_R2FR_2941_HELMHOLTZ_STRONG_ADOPTION_GATE.csv",
    "SRC3064_20_2976_gamma_owner": RESIDUALS / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "SRC3064_21_qloc_bound_spec": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
    "SRC3064_22_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3064_SOURCE_REGISTER.csv",
    "proof_gate": RESIDUALS / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
    "double_zero_attempt": RESIDUALS / "P8_Y5_R2FR_3064_GK_DOUBLE_ZERO_ATTEMPT.csv",
    "residual_interface": RESIDUALS / "P8_Y5_R2FR_3064_QLOC_RESIDUAL_INTERFACE.csv",
    "component_bounds": RESIDUALS / "P8_Y5_R2FR_3064_GK_COMPONENT_BOUND_RUNNER_NONCLAIM.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3064_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3064_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3064_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3064_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3064_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_gate_copy": PARENT_ACTION / "GammaKhat_q_loc_proof_gate_3064_NOT_SIGNED.csv",
    "residual_interface_copy": LOCAL_BOUNDS / "q_loc_residual_interface_3064_NONCLAIM.csv",
    "component_bounds_copy": LOCAL_BOUNDS / "GK_component_bound_runner_3064_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3064_Gamma_eff_density_Khat_identity_NEXT_NONCLAIM.csv",
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
        "theorem_zero",
        "numeric_ready",
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

proof_gate_rows = [
    base(
        {
            "gate_id": "GK3064_0_action_existence",
            "required_clause": "a parent-owned local diffeomorphism-invariant scalar action S_GK exists",
            "mathematical_form": "S_GK[g,Phi] with T_GK^{mu nu}=-2/sqrt(-g) delta S_GK/delta g_{mu nu}",
            "current_status": "NOT_SUPPLIED_CURRENT_CORPUS",
            "proof_signed": "false",
            "failure_if_missing": "Gamma_eff/Khat/q_loc remain bookkeeping or closure variables, not derived dynamics",
            "source_path": str(SOURCE_PATHS["SRC3064_17_2581_proof_gate"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_1_Gamma_eff_density_owner",
            "required_clause": "Gamma_eff is a parent-owned scalar density with field content, units, branch domain and metric dependence",
            "mathematical_form": "sqrt(-g) Gamma_eff[g,Phi,nabla Phi,D,...] is the density varied in S_GK",
            "current_status": "FORMAL_RESPONSE_DOUBLET_CANDIDATE_ONLY",
            "proof_signed": "false",
            "failure_if_missing": "C0/dC zero can be formal while not applying to current MTS variables",
            "source_path": str(SOURCE_PATHS["SRC3064_20_2976_gamma_owner"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_2_Khat_metric_response_identity",
            "required_clause": "K_hat equals the metric response of Gamma_eff in the same convention",
            "mathematical_form": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} plus derivative and boundary terms",
            "current_status": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "proof_signed": "false",
            "failure_if_missing": "q_loc is not a Ward/Euler residual and Delta_K remains live",
            "source_path": str(SOURCE_PATHS["SRC3064_16_2409_khat_match"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_3_Helmholtz_integrability",
            "required_clause": "the proposed T_GK satisfies Helmholtz/second-variation symmetry",
            "mathematical_form": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} symmetric under metric-variation exchange up to boundary and gauge constraints",
            "current_status": "NOT_CHECKED_CURRENT_SYMBOLS",
            "proof_signed": "false",
            "failure_if_missing": "no action exists for the proposed stress",
            "source_path": str(SOURCE_PATHS["SRC3064_13_1280_audit"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_4_Euler_Ward_closure",
            "required_clause": "fields inside Gamma_eff/Khat obey compact local vacuum Euler equations",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_GK, so E_A=0 and B_GK=0 imply q_loc^nu=0",
            "current_status": "NOT_DERIVED",
            "proof_signed": "false",
            "failure_if_missing": "q_loc remains a physical local force/source-exchange residual",
            "source_path": str(SOURCE_PATHS["SRC3064_10_1010_theorem"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_5_fixed_point_double_zero",
            "required_clause": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 at the local fixed point",
            "mathematical_form": "Gamma_eff(Phi0)g^{mu nu}-K_hat^{mu nu}(Phi0)=0 and partial_A[Gamma_eff g^{mu nu}-K_hat^{mu nu}]|Phi0=0",
            "current_status": "NOT_MATCHED",
            "proof_signed": "false",
            "failure_if_missing": "F1 survives as PPN/source-normalization hair",
            "source_path": str(SOURCE_PATHS["SRC3064_07_gk_contract"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_6_projector_boundary",
            "required_clause": "P_loc is parent-owned and boundary/symplectic no-flux holds",
            "mathematical_form": "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, integral_boundary Delta(theta_GK,Q_GK,tau)=0",
            "current_status": "OPEN",
            "proof_signed": "false",
            "failure_if_missing": "projected or bulk zero can hide force components or leak through boundaries",
            "source_path": str(SOURCE_PATHS["SRC3064_17_2581_proof_gate"]),
        }
    ),
    base(
        {
            "gate_id": "GK3064_7_units_projection",
            "required_clause": "q_loc units and weak-field projection into PPN/local force/source-mass arenas are fixed",
            "mathematical_form": "q_loc^nu -> Delta_gamma, alpha_i, xi, source-normalization, R10/R11 rows in one observed frame",
            "current_status": "MISSING_UNITS_RESPONSE_COEFFICIENTS",
            "proof_signed": "false",
            "failure_if_missing": "a finite q_loc profile cannot be compared to experiments",
            "source_path": str(SOURCE_PATHS["SRC3064_21_qloc_bound_spec"]),
        }
    ),
]

double_zero_rows = [
    base(
        {
            "attempt_id": "DZGK3064_0_value_zero",
            "target": "epsilon_C0_GammaKhat",
            "desired_result": "T_GK(Phi0)=0 after accepted background subtraction",
            "derivation_attempt": "Gamma0 subtraction plus response-doublet evenness would remove the constant GK stress offset",
            "current_status": "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "theorem_zero": "false",
            "missing_for_claim": "MISSING_Gamma_eff_density_owner; MISSING_background_subtraction_rule; MISSING_Khat_identity",
            "source_path": str(SOURCE_PATHS["SRC3064_20_2976_gamma_owner"]),
        }
    ),
    base(
        {
            "attempt_id": "DZGK3064_1_derivative_zero",
            "target": "epsilon_dC_GammaKhat",
            "desired_result": "partial_A T_GK(Phi0)=0",
            "derivation_attempt": "exchange-even density Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) kills the linear Z term if Z is the physical q_loc generator",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "theorem_zero": "false",
            "missing_for_claim": "MISSING_Z_BASIS_PHYSICAL_LOCK; MISSING_source_readout_evenness; MISSING_current_MTS_match",
            "source_path": str(SOURCE_PATHS["SRC3064_20_2976_gamma_owner"]),
        }
    ),
    base(
        {
            "attempt_id": "DZGK3064_2_gap",
            "target": "M_GK^2",
            "desired_result": "positive/gapped GK operator on compact local collar",
            "derivation_attempt": "positive Hessian M_AB would make any retained GK tail short-range and bounded",
            "current_status": "MISSING_MAB_OWNER_UNITS_POSITIVITY",
            "theorem_zero": "false",
            "missing_for_claim": "MISSING_MAB_source; MISSING_units; MISSING_positivity; MISSING_constraint_quotient",
            "source_path": str(SOURCE_PATHS["SRC3064_20_2976_gamma_owner"]),
        }
    ),
    base(
        {
            "attempt_id": "DZGK3064_3_q_projection_zero",
            "target": "q_loc_projection",
            "desired_result": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})=0 on local compact vacuum",
            "derivation_attempt": "Ward identity plus Euler equations plus boundary silence would make q_loc vanish on shell",
            "current_status": "NOT_DERIVED",
            "theorem_zero": "false",
            "missing_for_claim": "MISSING_Euler_closure; MISSING_boundary_no_flux; MISSING_projector_owner",
            "source_path": str(SOURCE_PATHS["SRC3064_10_1010_theorem"]),
        }
    ),
    base(
        {
            "attempt_id": "DZGK3064_4_verdict",
            "target": "Delta_extra_GK_linear",
            "desired_result": "Delta_extra_GK_linear=0",
            "derivation_attempt": "requires value zero, derivative zero, positive/closed operator, q projection zero, and physical PPN lock",
            "current_status": "NOT_PROVED_CURRENT_CORPUS",
            "theorem_zero": "false",
            "missing_for_claim": "GK3064_0_THROUGH_GK3064_7_UNSIGNED",
            "source_path": str(OUTPUTS["proof_gate"]),
        }
    ),
]

residual_interface_rows = [
    base(
        {
            "residual_id": "QLOC3064_0_q_loc_vector",
            "symbol": "q_loc^nu",
            "definition": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "status": "RETAINED_UNTIL_GK_PROOF_GATES_PASS",
            "observable_link": "PPN_alpha_i_xi;source_normalization_R11;local_force;clock_orbital",
            "units": "dimensionless_or_force_per_mass_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "S_GK;Khat_metric_response;Helmholtz;Euler;double_zero;P_loc;boundary",
            "source_path": str(SOURCE_PATHS["SRC3064_18_2581_residual_interface"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_1_Delta_K",
            "symbol": "Delta_K",
            "definition": "K_hat - K_metric[Gamma_eff]",
            "status": "RETAINED_SYMBOLIC_GAP",
            "observable_link": "metric_response;PPN;source_mass",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "Khat metric-response identity in one convention",
            "source_path": str(SOURCE_PATHS["SRC3064_16_2409_khat_match"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_2_H_GK",
            "symbol": "H_GK",
            "definition": "antisymmetric Helmholtz/second-variation obstruction for proposed T_GK",
            "status": "RETAINED_SYMBOLIC_GAP",
            "observable_link": "action_existence;local_GR",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "explicit second-variation symmetry calculation",
            "source_path": str(SOURCE_PATHS["SRC3064_13_1280_audit"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_3_J_GK",
            "symbol": "J_GK",
            "definition": "source-current work in Gamma/Khat Euler identity",
            "status": "RETAINED_SYMBOLIC_GAP",
            "observable_link": "PPN_preferred_frame;source_exchange",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "source-free compact local Euler equations from same parent action",
            "source_path": str(SOURCE_PATHS["SRC3064_18_2581_residual_interface"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_4_B_GK",
            "symbol": "B_GK",
            "definition": "boundary/symplectic work from S_GK integrations by parts",
            "status": "RETAINED_SYMBOLIC_GAP",
            "observable_link": "boundary_flux;R10;R11",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "no-flux or fixed topological subtraction theorem",
            "source_path": str(SOURCE_PATHS["SRC3064_18_2581_residual_interface"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_5_P_loc_commutator",
            "symbol": "P_loc_commutator",
            "definition": "failure of P_loc to be parent-owned and commute with fixed-point/readout limit",
            "status": "RETAINED_SYMBOLIC_GAP",
            "observable_link": "domain_projector;preferred_frame",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "parent projector algebra and fixed-point commutation",
            "source_path": str(SOURCE_PATHS["SRC3064_18_2581_residual_interface"]),
        }
    ),
    base(
        {
            "residual_id": "QLOC3064_TOTAL",
            "symbol": "q_loc_residual_abs",
            "definition": "absolute no-cancellation envelope over q_loc, Delta_K, H_GK, J_GK, B_GK and P_loc gaps",
            "status": "MISSING_COMPONENT_INPUTS",
            "observable_link": "local_GR;PPN;R10;R11;WEP",
            "units": "dimensionless_or_declared_per_projection",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "needed_for_zero": "all residual components theorem-zero or source-backed numeric and bounded",
            "source_path": str(OUTPUTS["residual_interface"]),
        }
    ),
]

component_bound_rows = [
    base(
        {
            "component_id": "GKCB3064_0_Delta_extra_GK_linear",
            "quantity": "Delta_extra_GK_linear",
            "bound_formula": "abs(eta_GK)*(abs(epsilon_C0_GammaKhat)+abs(epsilon_dC_GammaKhat)+abs(q_loc_projection))/max(M_GK^2,M_floor^2)",
            "required_inputs": "eta_GK;epsilon_C0_GammaKhat;epsilon_dC_GammaKhat;q_loc_projection;M_GK^2;projection_units",
            "candidate_value": "MISSING_COMPONENT_INPUTS",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "PPN_gamma;local_force;source_mass",
            "source_path": str(SOURCE_PATHS["SRC3064_02_3063_runner"]),
        }
    ),
    base(
        {
            "component_id": "GKCB3064_1_epsilon_C0",
            "quantity": "epsilon_C0_GammaKhat",
            "bound_formula": "abs(T_GK(Phi0)) after background subtraction and Khat convention lock",
            "required_inputs": "T_GK(Phi0);Gamma0_subtraction_rule;Khat_metric_response_convention",
            "candidate_value": "MISSING_PARENT_VALUE_ZERO",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "source_mass;PPN_gamma",
            "source_path": str(OUTPUTS["double_zero_attempt"]),
        }
    ),
    base(
        {
            "component_id": "GKCB3064_2_epsilon_dC",
            "quantity": "epsilon_dC_GammaKhat",
            "bound_formula": "norm(partial_A T_GK(Phi0)) on physical Z/q_loc basis",
            "required_inputs": "Z_basis_physical_lock;partial_A_T_GK;source_readout_evenness;units",
            "candidate_value": "MISSING_PARENT_DERIVATIVE_ZERO",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "PPN_gamma;local_force",
            "source_path": str(OUTPUTS["double_zero_attempt"]),
        }
    ),
    base(
        {
            "component_id": "GKCB3064_3_q_projection",
            "quantity": "q_loc_projection",
            "bound_formula": "norm(P_loc(nabla Gamma_eff - div K_hat)) in the chosen local arena",
            "required_inputs": "P_loc_owner;q_loc_profile;arena_projection;source_units;boundary_condition",
            "candidate_value": "MISSING_QLOC_PROFILE_OR_ZERO_THEOREM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "PPN_alpha_i_xi;local_force;clock_orbital",
            "source_path": str(OUTPUTS["residual_interface"]),
        }
    ),
    base(
        {
            "component_id": "GKCB3064_4_mass_gap",
            "quantity": "M_GK^2",
            "bound_formula": "positive lower gap of the GK Hessian/operator after quotient/gauge removal",
            "required_inputs": "M_AB owner;units;positivity;constraint quotient;domain",
            "candidate_value": "MISSING_M_GK_SQUARED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "R10;PPN_gamma;local_force_range",
            "source_path": str(SOURCE_PATHS["SRC3064_20_2976_gamma_owner"]),
        }
    ),
    base(
        {
            "component_id": "GKCB3064_5_projection_to_gamma",
            "quantity": "K_GK_to_gamma",
            "bound_formula": "abs(gamma_minus_1)_GK <= abs(K_GK_to_gamma)*abs(Delta_extra_GK_linear)/(1-abs(epsilon_T))",
            "required_inputs": "K_GK_to_gamma;epsilon_T_bound;fixed_GM_denominator;readout_gauge",
            "candidate_value": "MISSING_GAMMA_PROJECTION_COEFFICIENT",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_targets": "Cassini_PPN_gamma;light_time",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv"),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3064_0_q_loc_zero",
            "claim": "q_loc^nu=0 is derived for current MTS",
            "status": "NO_NOT_DERIVED",
            "claim_active": "false",
            "reason": "S_GK, Khat metric-response identity, Helmholtz, Euler, double-zero, projector and boundary gates remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3064_1_Delta_extra_GK_zero",
            "claim": "Delta_extra_GK_linear=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "epsilon_C0, epsilon_dC, q_loc projection and M_GK gap are not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3064_2_GK_bound_ready",
            "claim": "GK component runner is numeric/source-backed",
            "status": "NO_SCHEMA_ONLY",
            "claim_active": "false",
            "reason": "component rows remain missing-value nonclaim scaffolds",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3064_3_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "3064 keeps q_loc as the official residual interface rather than smuggling a plateau axiom",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3064_0_zero_proof",
            "question": "Did 3064 prove q_loc^nu=0?",
            "answer": "NO",
            "reason": "the current corpus supplies a route and conditional templates, not a parent-signed S_GK/Khat/Helmholtz/Euler/double-zero/no-flux chain",
            "action": "retain q_loc and GK residual components",
        }
    ),
    base(
        {
            "decision_id": "DEC3064_1_bound_runner",
            "question": "Can GK be numerically bounded now?",
            "answer": "NO",
            "reason": "eta_GK, epsilon_C0, epsilon_dC, q_loc_projection, M_GK^2 and gamma projection coefficient are missing",
            "action": "keep component runner nonclaim",
        }
    ),
    base(
        {
            "decision_id": "DEC3064_2_best_next",
            "question": "Best next derivation target?",
            "answer": "OWN_GAMMA_EFF_DENSITY_AND_KHAT_IDENTITY",
            "reason": "without K_hat=K_metric[Gamma_eff], q_loc cannot be promoted from residual bookkeeping to a Ward/Euler object",
            "action": "attack Gamma_eff scalar-density ownership and Khat metric-response identity before attempting another q_loc zero claim",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3064_0_3065",
            "next_checkpoint": "3065-Y5-R2FR-Gamma-eff-density-owner-and-Khat-metric-response-identity-or-DeltaK-input-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Gamma_eff_density_owner_and_Khat_metric_response_identity_or_DeltaK_input_fill_under_AX1090_3065.py",
            "mission": "try to parent-own Gamma_eff as a scalar density and prove K_hat=K_metric[Gamma_eff]; if not, fill Delta_K nonclaim input rows",
            "starting_equation": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}); if K_hat=K_metric[Gamma_eff] and Euler/boundary gates close, q_loc can be Ward/Euler zero",
            "claim_policy": "no q_loc/local-GR claim unless Gamma_eff density ownership and Khat metric-response identity are parent-signed in the same branch",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["proof_gate"], proof_gate_rows)
write_csv(OUTPUTS["double_zero_attempt"], double_zero_rows)
write_csv(OUTPUTS["residual_interface"], residual_interface_rows)
write_csv(OUTPUTS["component_bounds"], component_bound_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["proof_gate"], BRANCH_OUTPUTS["proof_gate_copy"])
copy_csv(OUTPUTS["residual_interface"], BRANCH_OUTPUTS["residual_interface_copy"])
copy_csv(OUTPUTS["component_bounds"], BRANCH_OUTPUTS["component_bounds_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3064 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["proof_gate"],
    OUTPUTS["double_zero_attempt"],
    OUTPUTS["residual_interface"],
    OUTPUTS["component_bounds"],
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

all_proof_unsigned = all(row["proof_signed"] == "false" for row in proof_gate_rows)
all_double_zero_false = all(row["theorem_zero"] == "false" for row in double_zero_rows)
all_residuals_nonclaim = all(row["valid_for_claim"] == "false" and "MISSING" in row["numeric_value"] for row in residual_interface_rows)
all_bounds_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in component_bound_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
has_delta_k = any("DeltaK" in row["next_checkpoint"] or "DeltaK" in row["script"] for row in next_rows)

validation_rows = [
    base({"validation_id": "VAL3064_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3064_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3064_02_proof_gates_unsigned", "passed": all_proof_unsigned, "requirement": "GK proof gates remain unsigned unless parent-signed", "evidence": OUTPUTS["proof_gate"].name}),
    base({"validation_id": "VAL3064_03_double_zero_not_promoted", "passed": all_double_zero_false, "requirement": "GK double-zero attempt does not promote theorem-zero", "evidence": OUTPUTS["double_zero_attempt"].name}),
    base({"validation_id": "VAL3064_04_residuals_retained", "passed": all_residuals_nonclaim, "requirement": "q_loc residual interface remains explicit and nonclaim", "evidence": OUTPUTS["residual_interface"].name}),
    base({"validation_id": "VAL3064_05_component_bounds_nonclaim", "passed": all_bounds_nonclaim, "requirement": "GK component-bound runner remains schema-only", "evidence": OUTPUTS["component_bounds"].name}),
    base({"validation_id": "VAL3064_06_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3064_07_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3064" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3064 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3064_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3064_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3064_10_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3064_11_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3065-") and has_delta_k, "requirement": "next target selects Gamma_eff density/Khat identity or DeltaK input fill", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3064_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3064 - GammaKhat q_loc Double-Zero Proof or GK Component Bound Runner

Status: `Y5_R2FR_3064_GK_q_loc_zero_not_derived_residual_interface_retained`

Generated: `{RUN_UTC}`

## Verdict

3064 attacks the highest-priority extra-sector leak:

`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})`.

The desired proof is elegant:

1. own `Gamma_eff` as a scalar density in a parent action;
2. prove `K_hat = K_metric[Gamma_eff]`;
3. pass Helmholtz integrability;
4. use Euler/Ward closure plus boundary silence;
5. prove `T_GK(Phi0)=0` and `partial_A T_GK(Phi0)=0`;
6. lock the projection/readout to physical PPN/local residual variables.

The current corpus does not sign that chain. Therefore 3064 does **not** claim `q_loc^nu=0`, `Delta_extra_GK_linear=0`, or local GR.

The strongest new reduction is this: the next real bottleneck is not a vague plateau problem. It is the concrete identity

`K_hat^{{mu nu}} = 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{{mu nu}}`

in the same parent branch and convention. Without that, `q_loc` remains the official retained residual.

## GK Proof Gate

{md_table(proof_gate_rows, ["gate_id", "required_clause", "mathematical_form", "current_status", "proof_signed", "failure_if_missing"])}

## GK Double-Zero Attempt

{md_table(double_zero_rows, ["attempt_id", "target", "desired_result", "derivation_attempt", "current_status", "theorem_zero", "missing_for_claim"])}

## q_loc Residual Interface

{md_table(residual_interface_rows, ["residual_id", "symbol", "definition", "status", "observable_link", "numeric_value", "needed_for_zero"])}

## GK Component Bound Runner

{md_table(component_bound_rows, ["component_id", "quantity", "bound_formula", "required_inputs", "candidate_value", "numeric_ready", "bound_ready"])}

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
    raise SystemExit(f"3064 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: q_loc zero not derived; GK residual interface retained")
