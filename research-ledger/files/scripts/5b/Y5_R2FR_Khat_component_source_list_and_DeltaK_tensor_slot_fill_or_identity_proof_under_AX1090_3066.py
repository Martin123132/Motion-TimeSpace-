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

CHECKPOINT = "3066"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3066-Y5-R2FR-Khat-component-source-list-and-DeltaK-tensor-slot-fill-or-identity-proof-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3066_00_3065_doc": ROOT / "3065-Y5-R2FR-Gamma-eff-density-owner-and-Khat-metric-response-identity-or-DeltaK-input-fill-under-AX1090.md",
    "SRC3066_01_3065_next": RESIDUALS / "P8_Y5_R2FR_3065_NEXT_TARGET.csv",
    "SRC3066_02_3065_identity": RESIDUALS / "P8_Y5_R2FR_3065_KHAT_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    "SRC3066_03_3065_deltak": RESIDUALS / "P8_Y5_R2FR_3065_DELTAK_INPUT_ROWS_NONCLAIM.csv",
    "SRC3066_04_2809_component_attempt": RESIDUALS / "P8_Y5_R2FR_2809_KHAT_COMPONENT_MATCH_ATTEMPT.csv",
    "SRC3066_05_2700_metric_comparison": RESIDUALS / "P8_Y5_R2FR_2700_KHAT_METRIC_RESPONSE_COMPARISON_NONCLAIM.csv",
    "SRC3066_06_2807_match": RESIDUALS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv",
    "SRC3066_07_2409_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "SRC3066_08_2218_appearance": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_KHAT_SOURCE_APPEARANCE_TABLE.csv",
    "SRC3066_09_2218_tensor_comparison": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_TENSOR_COMPARISON.csv",
    "SRC3066_10_2219_birth_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_KHAT_BIRTH_CERTIFICATE_GATE.csv",
    "SRC3066_11_2219_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_KHAT_SOURCE_OWNER_AUDIT.csv",
    "SRC3066_12_2219_component_fill": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_DELTA_KHAT_COMPONENT_FILL.csv",
    "SRC3066_13_2219_nonclaim_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_KHAT_NONCLAIM_COMPONENT_ROWS.csv",
    "SRC3066_14_2813_khat00_hunt": RESIDUALS / "P8_Y5_R2FR_2813_KHAT00_CORPUS_HUNT.csv",
    "SRC3066_15_2810_deltak00": RESIDUALS / "P8_Y5_R2FR_2810_DELTAK00_SOURCE_ATTEMPT.csv",
    "SRC3066_16_2811_deltak00_review": RESIDUALS / "P8_Y5_R2FR_2811_DELTAK00_SOURCE_REVIEW.csv",
    "SRC3066_17_2809_bound_table": RESIDUALS / "P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv",
    "SRC3066_18_2975_bounds": RESIDUALS / "P8_Y5_R2FR_2975_DELTAK_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "SRC3066_19_1287_KL00": RESIDUALS / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "SRC3066_20_1190_tracefree": RESIDUALS / "P8_Y5_R10_1190_TRACEFREE_KHAT_SOLVER_GATE.csv",
    "SRC3066_21_793_trace_status": RESIDUALS / "P8_Y5_R10_793_KHAT_TRACE_STATUS_GATE.csv",
    "SRC3066_22_827_contract": RESIDUALS / "P8_Y5_R10_827_KHAT_RESPONSE_CONTRACT.csv",
    "SRC3066_23_830_owner": RESIDUALS / "P8_Y5_R10_830_KHAT_OWNER_AUDIT.csv",
    "SRC3066_24_833_amplitude": RESIDUALS / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
    "SRC3066_25_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3066_SOURCE_REGISTER.csv",
    "component_source_list": RESIDUALS / "P8_Y5_R2FR_3066_KHAT_COMPONENT_SOURCE_LIST.csv",
    "tensor_slot_audit": RESIDUALS / "P8_Y5_R2FR_3066_KHAT_TENSOR_SLOT_IDENTITY_AUDIT.csv",
    "deltak_slot_rows": RESIDUALS / "P8_Y5_R2FR_3066_DELTAK_TENSOR_SLOT_ROWS_NONCLAIM.csv",
    "route_ledger": RESIDUALS / "P8_Y5_R2FR_3066_TRACEFREE_ROUTE_AND_AMPLITUDE_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3066_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3066_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3066_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3066_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3066_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "component_source_copy": PARENT_ACTION / "Khat_component_source_list_3066_NOT_SIGNED.csv",
    "tensor_slot_copy": PARENT_ACTION / "Khat_tensor_slot_identity_audit_3066_NOT_SIGNED.csv",
    "deltak_slot_copy": LOCAL_BOUNDS / "DeltaK_tensor_slot_rows_3066_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3066_tracefree_improvement_birth_certificate_NEXT_NONCLAIM.csv",
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
        "source_signed_component",
        "identity_pass",
        "numeric_ready",
        "bound_ready",
        "live_khat_adopted",
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

component_source_rows = [
    base(
        {
            "slot_id": "KCS3066_0_all",
            "tensor_slot": "all",
            "needed_live_formula": "source-owned K_hat^{mu nu} before readout with units, domain, derivative, projector and boundary terms",
            "best_found": "all useful Khat appearances are targets, identities, residual slots or conditional templates",
            "current_status": "NO_COMPONENT_MATCH_AVAILABLE",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_08_2218_appearance"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_1_00",
            "tensor_slot": "00 / energy",
            "needed_live_formula": "K_hat^{00}",
            "best_found": "formal tracefree-longitudinal candidate K_L^{00}=2 nabla^0 nabla^0 phi - (1/2)g^{00}Box phi",
            "current_status": "FORMAL_CANDIDATE_FOUND_NONCLAIM_NOT_LIVE_KHAT",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_14_2813_khat00_hunt"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_2_0i",
            "tensor_slot": "0i / momentum-preferred-frame",
            "needed_live_formula": "K_hat^{0i}",
            "best_found": "no current component formula for K_hat^{0i}",
            "current_status": "MISSING_COMPONENT_FORMULA",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_04_2809_component_attempt"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_3_trace",
            "tensor_slot": "spatial trace",
            "needed_live_formula": "h_ij K_hat^{ij}",
            "best_found": "K_hat is treated as trace-free after Gamma_eff metric-proportional split; no current trace formula or fixed volume convention",
            "current_status": "TRACE_SHORTCUT_BLOCKED_MISSING_TRACE_FORMULA",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_21_793_trace_status"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_4_tracefree",
            "tensor_slot": "spatial tracefree/shear",
            "needed_live_formula": "K_hat^{<ij>}",
            "best_found": "tracefree longitudinal route K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi is exact as a candidate",
            "current_status": "SERIOUS_FORMAL_ROUTE_NOT_PARENT_ADOPTED",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_20_1190_tracefree"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_5_derivative",
            "tensor_slot": "derivative/connection/domain",
            "needed_live_formula": "K_conn, derivative-order, CDB/domain and integration-by-parts terms",
            "best_found": "connection/domain/CDB derivative order open ledgers only",
            "current_status": "LIVE_UNEXTRACTED_NOT_MATCH",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_09_2218_tensor_comparison"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_6_boundary",
            "tensor_slot": "boundary/improvement/projector",
            "needed_live_formula": "K_boundary plus symplectic/corner/projector terms with no-flux convention",
            "best_found": "boundary/projector open ledgers only",
            "current_status": "MISSING_BOUNDARY_CONVENTION",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_10_2219_birth_gate"]),
        }
    ),
    base(
        {
            "slot_id": "KCS3066_7_units",
            "tensor_slot": "units/readout",
            "needed_live_formula": "stress-density units and response map into q_loc/PPN/R10/clock/orbital arenas",
            "best_found": "stress-density and q_loc/readout units are missing",
            "current_status": "MISSING_UNITS_READOUT",
            "source_signed_component": "false",
            "usable_for_identity": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_10_2219_birth_gate"]),
        }
    ),
]

tensor_slot_rows = [
    base(
        {
            "identity_id": "KTI3066_0_00",
            "tensor_slot": "00",
            "required_identity": "K_hat^{00}=K_metric^{00}",
            "identity_result": "NOT_PROVED",
            "identity_pass": "false",
            "reason": "formal KL00 candidate exists but is not live current-MTS K_hat^{00}; Kmetric side remains conditional",
            "DeltaK_slot": "DeltaK_00",
            "source_path": str(SOURCE_PATHS["SRC3066_14_2813_khat00_hunt"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_1_0i",
            "tensor_slot": "0i",
            "required_identity": "K_hat^{0i}=K_metric^{0i}",
            "identity_result": "NOT_EVALUABLE",
            "identity_pass": "false",
            "reason": "no K_hat^{0i} formula and no vector norm/projection",
            "DeltaK_slot": "DeltaK_0i",
            "source_path": str(SOURCE_PATHS["SRC3066_04_2809_component_attempt"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_2_trace",
            "tensor_slot": "spatial trace",
            "required_identity": "h_ij K_hat^{ij}=h_ij K_metric^{ij}",
            "identity_result": "NOT_EVALUABLE",
            "identity_pass": "false",
            "reason": "trace shortcut is blocked; volume/sign convention and live trace formula are missing",
            "DeltaK_slot": "DeltaK_trace",
            "source_path": str(SOURCE_PATHS["SRC3066_21_793_trace_status"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_3_tracefree",
            "tensor_slot": "tracefree/shear",
            "required_identity": "K_hat^{<ij>}=K_metric^{<ij>}",
            "identity_result": "FORMAL_ROUTE_ONLY",
            "identity_pass": "false",
            "reason": "K_L tracefree identity is exact, but parent origin for phi, curvature/boundary errors and live adoption are missing",
            "DeltaK_slot": "DeltaK_TF",
            "source_path": str(SOURCE_PATHS["SRC3066_20_1190_tracefree"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_4_derivative",
            "tensor_slot": "derivative/connection/domain",
            "required_identity": "K_hat derivative terms match K_metric derivative response of Gamma_eff",
            "identity_result": "NOT_EVALUABLE",
            "identity_pass": "false",
            "reason": "derivative-order, K_conn, CDB/domain and integration-by-parts terms remain retained residuals",
            "DeltaK_slot": "DeltaK_deriv",
            "source_path": str(SOURCE_PATHS["SRC3066_12_2219_component_fill"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_5_boundary",
            "tensor_slot": "boundary/improvement/projector",
            "required_identity": "boundary/improvement terms match or vanish under no-flux/source-measure theorem",
            "identity_result": "OPEN",
            "identity_pass": "false",
            "reason": "boundary no-flux, projector commutator and source-measure descent are not signed",
            "DeltaK_slot": "DeltaK_boundary",
            "source_path": str(SOURCE_PATHS["SRC3066_12_2219_component_fill"]),
        }
    ),
    base(
        {
            "identity_id": "KTI3066_6_verdict",
            "tensor_slot": "full tensor",
            "required_identity": "all slots pass in one branch with units and boundary convention fixed",
            "identity_result": "FAIL_CURRENT_CLAIM",
            "identity_pass": "false",
            "reason": "no source-owned live Khat tensor definition can be promoted; best route is tracefree improvement birth certificate",
            "DeltaK_slot": "DeltaK_total",
            "source_path": str(SOURCE_PATHS["SRC3066_11_2219_owner_audit"]),
        }
    ),
]

deltak_slot_rows = [
    base(
        {
            "slot_id": "DKS3066_0_total",
            "quantity": "Delta_K^{mu nu}",
            "definition": "K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "slot_bound_formula": "||Delta_K|| <= sum_slots ||DeltaK_slot|| with no-cancellation policy",
            "candidate_value": "MISSING_SOURCE_BACKED_COMPONENTS",
            "units": "stress_or_declared_per_projection",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "q_loc;PPN;Newton;source_mass;R10;clock;orbital",
            "missing_for_claim": "MISSING_LIVE_KHAT_COMPONENTS;MISSING_KMETRIC_COMPONENTS;MISSING_UNITS;MISSING_BOUNDARY_CONVENTION",
            "source_path": str(OUTPUTS["tensor_slot_audit"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_1_00",
            "quantity": "DeltaK_00",
            "definition": "time-time metric-response mismatch",
            "slot_bound_formula": "|K_hat^{00}-K_metric^{00}| plus derivative contribution to q_DeltaK",
            "candidate_value": "MISSING_KHAT00_LIVE_ADOPTION",
            "units": "stress",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "Newton;PPN_gamma;source_normalization",
            "missing_for_claim": "formal_KL00_not_live;missing_Kmetric00;missing_boundary",
            "source_path": str(SOURCE_PATHS["SRC3066_14_2813_khat00_hunt"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_2_0i",
            "quantity": "DeltaK_0i",
            "definition": "momentum/preferred-frame metric-response mismatch",
            "slot_bound_formula": "||K_hat^{0i}-K_metric^{0i}||",
            "candidate_value": "MISSING_KHAT0I_FORMULA",
            "units": "stress",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "alpha1;alpha2;alpha3;local_force",
            "missing_for_claim": "missing_vector_component;missing_projection_norm",
            "source_path": str(SOURCE_PATHS["SRC3066_04_2809_component_attempt"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_3_trace",
            "quantity": "DeltaK_trace",
            "definition": "spatial trace mismatch",
            "slot_bound_formula": "|h_ij(K_hat^{ij}-K_metric^{ij})|",
            "candidate_value": "MISSING_TRACE_FORMULA_AND_VOLUME_CONVENTION",
            "units": "stress",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "PPN_gamma;orbital;pressure_trace",
            "missing_for_claim": "trace_shortcut_blocked;missing_Gamma0_subtraction;missing_volume_convention",
            "source_path": str(SOURCE_PATHS["SRC3066_21_793_trace_status"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_4_tracefree",
            "quantity": "DeltaK_TF",
            "definition": "tracefree/shear mismatch",
            "slot_bound_formula": "||K_hat^{<ij>}-K_metric^{<ij>}|| including curved Ricci/boundary error",
            "candidate_value": "MISSING_TRACEFREE_BIRTH_CERTIFICATE",
            "units": "stress",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "PPN_shear;anisotropic_stress;light_time",
            "missing_for_claim": "missing_parent_phi;missing_curved_source_equation;missing_boundary;amplitude_live",
            "source_path": str(SOURCE_PATHS["SRC3066_20_1190_tracefree"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_5_derivative",
            "quantity": "DeltaK_deriv",
            "definition": "derivative/connection/domain mismatch",
            "slot_bound_formula": "C_t||partial_t DeltaK||+C_r||partial_r DeltaK||+C_ang||partial_ang DeltaK||+C_conn||Gamma_conn||||DeltaK||",
            "candidate_value": "MISSING_DERIVATIVE_RESPONSE_CONSTANTS",
            "units": "force_density_after_divergence",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "q_loc;preferred_frame;orbital",
            "missing_for_claim": "missing_derivative_order;missing_K_conn;missing_CDB_domain",
            "source_path": str(SOURCE_PATHS["SRC3066_18_2975_bounds"]),
        }
    ),
    base(
        {
            "slot_id": "DKS3066_6_boundary",
            "quantity": "DeltaK_boundary",
            "definition": "boundary/projector/corner/source-worldtube mismatch",
            "slot_bound_formula": "||K_boundary|| + ||P_loc_commutator|| + ||source_worldtube_boundary||",
            "candidate_value": "MISSING_BOUNDARY_NO_FLUX_OR_VALUE",
            "units": "stress_or_surface_traction",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "R10;R11;source_mass;local_force",
            "missing_for_claim": "missing_no_flux;missing_projector_commutator;missing_source_measure_descent",
            "source_path": str(SOURCE_PATHS["SRC3066_12_2219_component_fill"]),
        }
    ),
]

route_ledger_rows = [
    base(
        {
            "route_id": "ROUTE3066_0_tracefree_identity",
            "route": "tracefree longitudinal improvement",
            "formula": "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi",
            "positive_result": "tracefree identity is exact in four dimensions; flat-patch divergence can cancel grad Gamma_eff with Box phi=(2/3)Gamma_eff+C",
            "blocker": "parent origin for phi/A_nu, curved Ricci term, Green inverse, boundary conditions and amplitude response remain open",
            "live_khat_adopted": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_20_1190_tracefree"]),
        }
    ),
    base(
        {
            "route_id": "ROUTE3066_1_amplitude_warning",
            "route": "Khat carrier amplitude",
            "formula": "||K||_L2=sqrt(n/(n-1))*||Gamma||_L2 in flat Hessian carrier",
            "positive_result": "amplitude law is derived and useful",
            "blocker": "q cancellation does not make Khat metrically safe unless Gamma is tiny, metric-null, or response-bounded",
            "live_khat_adopted": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_24_833_amplitude"]),
        }
    ),
    base(
        {
            "route_id": "ROUTE3066_2_best_next",
            "route": "tracefree improvement birth certificate",
            "formula": "parent-sign phi source equation, boundary/no-flux and metric response coefficient before adopting K_L",
            "positive_result": "this is the best concrete route found, not just a symbolic residual",
            "blocker": "birth certificate absent",
            "live_khat_adopted": "false",
            "source_path": str(SOURCE_PATHS["SRC3066_11_2219_owner_audit"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3066_0_live_Khat_components",
            "claim": "live K_hat tensor components are source-owned",
            "status": "NO",
            "claim_active": "false",
            "reason": "formal candidates exist, but no source-signed live Khat tensor component list was found",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3066_1_Khat_identity",
            "claim": "K_hat=K_metric[Gamma_eff] slot-by-slot",
            "status": "NO",
            "claim_active": "false",
            "reason": "every tensor slot is missing a live component, a Kmetric side, or a boundary/units convention",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3066_2_DeltaK_bound_ready",
            "claim": "Delta_K tensor-slot bounds are numeric/source-backed",
            "status": "NO_SCHEMA_ONLY",
            "claim_active": "false",
            "reason": "DeltaK slot rows are missing-input nonclaim rows",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3066_3_q_loc_zero",
            "claim": "q_loc^nu=0 follows from the Khat identity",
            "status": "NO",
            "claim_active": "false",
            "reason": "Delta_K remains live, and Euler/boundary/projector gates are still upstream blockers",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3066_4_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "3066 improves the source list and next route, not the GR claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3066_0_identity",
            "question": "Did 3066 prove Khat identity?",
            "answer": "NO",
            "reason": "no live Khat component source list exists; formal KL00/KL route is nonclaim",
            "action": "retain Delta_K slot rows",
        }
    ),
    base(
        {
            "decision_id": "DEC3066_1_progress",
            "question": "Did 3066 find anything useful?",
            "answer": "YES_FORMAL_TRACEFREE_ROUTE",
            "reason": "the tracefree longitudinal carrier has exact identities and a candidate KL00 row",
            "action": "move next to a birth-certificate gate rather than another broad hunt",
        }
    ),
    base(
        {
            "decision_id": "DEC3066_2_best_next",
            "question": "Best next target?",
            "answer": "TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE",
            "reason": "KSO2219_2 is the best concrete candidate route, but it needs parent phi, curved source equation, boundary and amplitude gates",
            "action": "try to parent-sign K_L or demote it to DeltaK_TF bound only",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3066_0_3067",
            "next_checkpoint": "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_tracefree_improvement_Khat_birth_certificate_or_DeltaK_TF_bound_under_AX1090_3067.py",
            "mission": "try to parent-sign the tracefree longitudinal K_L route as live Khat; if not, demote it to a DeltaK_TF bound-only component",
            "starting_equation": "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi; div K_L matches grad Gamma_eff only after parent phi equation, curvature, boundary and amplitude gates close",
            "claim_policy": "no Khat/q_loc/local-GR claim unless K_L is parent-born, live-adopted as Khat, boundary-safe and metrically bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["component_source_list"], component_source_rows)
write_csv(OUTPUTS["tensor_slot_audit"], tensor_slot_rows)
write_csv(OUTPUTS["deltak_slot_rows"], deltak_slot_rows)
write_csv(OUTPUTS["route_ledger"], route_ledger_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["component_source_list"], BRANCH_OUTPUTS["component_source_copy"])
copy_csv(OUTPUTS["tensor_slot_audit"], BRANCH_OUTPUTS["tensor_slot_copy"])
copy_csv(OUTPUTS["deltak_slot_rows"], BRANCH_OUTPUTS["deltak_slot_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3066 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["component_source_list"],
    OUTPUTS["tensor_slot_audit"],
    OUTPUTS["deltak_slot_rows"],
    OUTPUTS["route_ledger"],
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

all_components_unsigned = all(row["source_signed_component"] == "false" for row in component_source_rows)
has_formal_kl00_guarded = any(row["slot_id"] == "KCS3066_1_00" and "FORMAL_CANDIDATE" in row["current_status"] and row["usable_for_identity"] == "false" for row in component_source_rows)
all_identity_false = all(row["identity_pass"] == "false" for row in tensor_slot_rows)
all_deltak_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in deltak_slot_rows)
all_deltak_missing = all("MISSING" in row["candidate_value"] for row in deltak_slot_rows)
route_next_present = any(row["route_id"] == "ROUTE3066_2_best_next" and row["live_khat_adopted"] == "false" for row in route_ledger_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
next_is_3067 = next_rows[0]["next_checkpoint"].startswith("3067-")

validation_rows = [
    base({"validation_id": "VAL3066_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3066_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3066_02_components_unsigned", "passed": all_components_unsigned, "requirement": "no live Khat tensor component is source-signed", "evidence": OUTPUTS["component_source_list"].name}),
    base({"validation_id": "VAL3066_03_formal_KL00_guarded", "passed": has_formal_kl00_guarded, "requirement": "formal KL00 candidate is retained as nonclaim only", "evidence": OUTPUTS["component_source_list"].name}),
    base({"validation_id": "VAL3066_04_identity_false", "passed": all_identity_false, "requirement": "Khat identity is not promoted in any tensor slot", "evidence": OUTPUTS["tensor_slot_audit"].name}),
    base({"validation_id": "VAL3066_05_deltak_nonclaim", "passed": all_deltak_nonclaim and all_deltak_missing, "requirement": "DeltaK tensor-slot rows are missing-input nonclaim rows", "evidence": OUTPUTS["deltak_slot_rows"].name}),
    base({"validation_id": "VAL3066_06_route_next_present", "passed": route_next_present, "requirement": "tracefree birth-certificate route is selected without adopting live Khat", "evidence": OUTPUTS["route_ledger"].name}),
    base({"validation_id": "VAL3066_07_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3066_08_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3066" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3066 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3066_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3066_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3066_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3066_12_next_target", "passed": next_is_3067, "requirement": "next target selects tracefree improvement birth certificate or DeltaK_TF bound", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3066_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3066 - Khat Component Source List and DeltaK Tensor-Slot Fill or Identity Proof

Status: `Y5_R2FR_3066_no_live_Khat_component_identity_formal_tracefree_route_retained_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3066 hunted for live `K_hat` tensor components.

Result: no source-signed live component list was found. The corpus is not empty, though: it contains a serious formal tracefree-longitudinal route,

`K_L^{{mu nu}} = 2 nabla^mu nabla^nu phi - (1/2) g^{{mu nu}} Box phi`,

and a formal `K_L^{{00}}` candidate. But that route is not parent-born as the current MTS `K_hat`, and it still has open parent-phi, curvature, boundary, Green-inverse and amplitude gates.

So `K_hat = K_metric[Gamma_eff]` is not proved. `Delta_K` remains retained slot-by-slot:

`Delta_K^{{mu nu}} = K_hat^{{mu nu}} - K_metric^{{mu nu}}[Gamma_eff]`.

The productive next move is no longer a broad Khat hunt. It is a tracefree-improvement birth-certificate test.

## Khat Component Source List

{md_table(component_source_rows, ["slot_id", "tensor_slot", "needed_live_formula", "best_found", "current_status", "source_signed_component", "usable_for_identity"])}

## Tensor-Slot Identity Audit

{md_table(tensor_slot_rows, ["identity_id", "tensor_slot", "required_identity", "identity_result", "identity_pass", "reason", "DeltaK_slot"])}

## DeltaK Tensor-Slot Rows

{md_table(deltak_slot_rows, ["slot_id", "quantity", "definition", "slot_bound_formula", "candidate_value", "numeric_ready", "bound_ready", "missing_for_claim"])}

## Tracefree Route and Amplitude Ledger

{md_table(route_ledger_rows, ["route_id", "route", "formula", "positive_result", "blocker", "live_khat_adopted"])}

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
    raise SystemExit(f"3066 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: no live Khat component identity; tracefree route retained nonclaim")
