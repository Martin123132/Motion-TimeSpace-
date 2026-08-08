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
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3065"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3065-Y5-R2FR-Gamma-eff-density-owner-and-Khat-metric-response-identity-or-DeltaK-input-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3065_00_3064_doc": ROOT / "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md",
    "SRC3065_01_3064_next": RESIDUALS / "P8_Y5_R2FR_3064_NEXT_TARGET.csv",
    "SRC3065_02_3064_proof_gate": RESIDUALS / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
    "SRC3065_03_3064_q_loc": RESIDUALS / "P8_Y5_R2FR_3064_QLOC_RESIDUAL_INTERFACE.csv",
    "SRC3065_04_3064_GK_runner": RESIDUALS / "P8_Y5_R2FR_3064_GK_COMPONENT_BOUND_RUNNER_NONCLAIM.csv",
    "SRC3065_05_Khat_2409": RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "SRC3065_06_Gamma_owner_2976": RESIDUALS / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "SRC3065_07_Helmholtz_2941": RESIDUALS / "P8_Y5_R2FR_2941_HELMHOLTZ_STRONG_ADOPTION_GATE.csv",
    "SRC3065_08_GK_contract": RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "SRC3065_09_GK_integrability": RESIDUALS / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
    "SRC3065_10_1010_schema": RESIDUALS / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv",
    "SRC3065_11_1010_residuals": RESIDUALS / "P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv",
    "SRC3065_12_metric_comparison_2700": RESIDUALS / "P8_Y5_R2FR_2700_KHAT_METRIC_RESPONSE_COMPARISON_NONCLAIM.csv",
    "SRC3065_13_match_2807": RESIDUALS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv",
    "SRC3065_14_components_2809": RESIDUALS / "P8_Y5_R2FR_2809_KHAT_COMPONENT_MATCH_ATTEMPT.csv",
    "SRC3065_15_owner_rollforward_2977": RESIDUALS / "P8_Y5_R2FR_2977_GAMMA_EFF_OWNER_ROLLFORWARD_NONCLAIM.csv",
    "SRC3065_16_gamma_coefficients_3017": RESIDUALS / "P8_Y5_R2FR_3017_GAMMA_COEFFICIENT_FILL_CONTRACT.csv",
    "SRC3065_17_density_2217": BETA_DOCS / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv",
    "SRC3065_18_action_2799": BETA_DOCS / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv",
    "SRC3065_19_reduced_match_1649": RAB_QUEUE / "JR1649_REDUCED_GK_SYMBOL_MATCH_AUDIT_NONCLAIM.csv",
    "SRC3065_20_conjugacy_1712": RAB_QUEUE / "JR1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv",
    "SRC3065_21_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3065_SOURCE_REGISTER.csv",
    "density_owner": RESIDUALS / "P8_Y5_R2FR_3065_GAMMA_EFF_DENSITY_OWNER_GATE.csv",
    "khat_identity": RESIDUALS / "P8_Y5_R2FR_3065_KHAT_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    "deltak_inputs": RESIDUALS / "P8_Y5_R2FR_3065_DELTAK_INPUT_ROWS_NONCLAIM.csv",
    "qloc_consequence": RESIDUALS / "P8_Y5_R2FR_3065_QLOC_CONSEQUENCE_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3065_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3065_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3065_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3065_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3065_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "density_owner_copy": PARENT_ACTION / "Gamma_eff_density_owner_gate_3065_NOT_SIGNED.csv",
    "khat_identity_copy": PARENT_ACTION / "Khat_metric_response_identity_audit_3065_NOT_SIGNED.csv",
    "deltak_inputs_copy": LOCAL_BOUNDS / "DeltaK_input_rows_3065_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3065_Khat_component_source_list_or_DeltaK_tensor_slots_NEXT_NONCLAIM.csv",
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
        "parent_signed",
        "identity_signed",
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

density_owner_rows = [
    base(
        {
            "gate_id": "GDO3065_0_density_ansatz",
            "object": "Gamma_eff",
            "candidate_or_requirement": "Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
            "current_status": "FORMAL_RESPONSE_DOUBLET_CANDIDATE",
            "parent_signed": "false",
            "what_is_real_progress": "a reusable scalar-density ansatz exists",
            "blocking_gap": "candidate is not adopted as the current MTS parent density",
            "source_path": str(SOURCE_PATHS["SRC3065_06_Gamma_owner_2976"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_1_scalar_density_slot",
            "object": "sqrt(-g) Gamma_eff",
            "candidate_or_requirement": "local diffeomorphism scalar-density slot for S_GK=-int sqrt(-g) Gamma_eff",
            "current_status": "DENSITY_SLOT_FORMAL_ONLY",
            "parent_signed": "false",
            "what_is_real_progress": "the correct variational object is named",
            "blocking_gap": "field content, branch domain, units and metric dependence are incomplete",
            "source_path": str(SOURCE_PATHS["SRC3065_18_action_2799"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_2_exchange_evenness",
            "object": "E:Z->-Z",
            "candidate_or_requirement": "exchange-even density forbids a linear Z source if source/readout sectors are also even",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "parent_signed": "false",
            "what_is_real_progress": "formal F1=0 route survives",
            "blocking_gap": "Y5/Y6 source/readout even-channel debt remains open",
            "source_path": str(SOURCE_PATHS["SRC3065_17_density_2217"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_3_background",
            "object": "Gamma0",
            "candidate_or_requirement": "Gamma0 must be constant or background-subtracted so nabla Gamma0 does not source q_loc",
            "current_status": "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "parent_signed": "false",
            "what_is_real_progress": "the needed subtraction rule is explicit",
            "blocking_gap": "EH/Lambda/background compatibility and boundary/readout convention are not parent-signed",
            "source_path": str(SOURCE_PATHS["SRC3065_17_density_2217"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_4_MAB_owner",
            "object": "M_AB",
            "candidate_or_requirement": "H_AB=partial_A partial_B Gamma_eff at Z=0 equals M_AB with units, positivity and domain",
            "current_status": "MISSING_MAB_OWNER_UNITS_POSITIVITY",
            "parent_signed": "false",
            "what_is_real_progress": "formal Hessian extraction is immediate from the ansatz",
            "blocking_gap": "M_AB source, units, positivity and gauge/constraint removal not closed",
            "source_path": str(SOURCE_PATHS["SRC3065_17_density_2217"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_5_Zbasis_physical_lock",
            "object": "Z^A",
            "candidate_or_requirement": "response-displacement direction equals the actual quotient-vertical/local residual generator",
            "current_status": "MISSING_Z_BASIS_PHYSICAL_LOCK",
            "parent_signed": "false",
            "what_is_real_progress": "identifies the exact reason formal F1=0 cannot yet become physical",
            "blocking_gap": "physical Y0-Y6 component coverage is not parent-locked",
            "source_path": str(SOURCE_PATHS["SRC3065_20_conjugacy_1712"]),
        }
    ),
    base(
        {
            "gate_id": "GDO3065_6_verdict",
            "object": "Gamma_eff scalar density owner",
            "candidate_or_requirement": "source-backed Gamma_eff with fields, units, metric dependence and parent branch signature",
            "current_status": "NOT_PARENT_SIGNED",
            "parent_signed": "false",
            "what_is_real_progress": "density route is coherent but remains a candidate",
            "blocking_gap": "use Delta_K/q_loc residual rows until density ownership closes",
            "source_path": str(SOURCE_PATHS["SRC3065_06_Gamma_owner_2976"]),
        }
    ),
]

khat_identity_rows = [
    base(
        {
            "identity_id": "KMI3065_0_formal_Kmetric",
            "target": "K_metric[Gamma_eff]",
            "required_identity": "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} with volume, derivative and boundary conventions",
            "current_evidence": "formal response-doublet variation exists",
            "current_status": "PASS_FORMAL_STEP_ONLY",
            "identity_signed": "false",
            "residual_if_missing": "none_for_formal_step",
            "source_path": str(SOURCE_PATHS["SRC3065_05_Khat_2409"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_1_live_Khat_source",
            "target": "live_MTS_Khat",
            "required_identity": "a source-signed live K_hat tensor component list in the same branch",
            "current_evidence": "no source-signed live K_hat component list",
            "current_status": "MISSING_COMPONENT_SOURCE",
            "identity_signed": "false",
            "residual_if_missing": "Delta_K remains uninterpretable component-by-component",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_2_tensor_identity",
            "target": "K_hat == K_metric",
            "required_identity": "source path proving K_hat is defined as the same metric response under one convention",
            "current_evidence": "no derivation as delta[sqrt(-g)Gamma_eff]/delta g found",
            "current_status": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "identity_signed": "false",
            "residual_if_missing": "q_metric_response_defect",
            "source_path": str(SOURCE_PATHS["SRC3065_05_Khat_2409"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_3_00_component",
            "target": "K_hat^{00}",
            "required_identity": "K_hat^{00}=K_metric^{00}",
            "current_evidence": "no current component formula for K_hat^{00}",
            "current_status": "MISSING_COMPONENT_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_00",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_4_0i_component",
            "target": "K_hat^{0i}",
            "required_identity": "K_hat^{0i}=K_metric^{0i}",
            "current_evidence": "no current component formula for K_hat^{0i}",
            "current_status": "MISSING_COMPONENT_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_0i",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_5_spatial_trace",
            "target": "h_ij K_hat^{ij}",
            "required_identity": "spatial trace of K_hat equals spatial trace of K_metric in a fixed volume convention",
            "current_evidence": "no current trace formula or fixed volume convention",
            "current_status": "MISSING_TRACE_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_trace",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_6_spatial_tracefree",
            "target": "K_hat^{<ij>}",
            "required_identity": "tracefree/shear part of K_hat equals tracefree/shear part of K_metric",
            "current_evidence": "no current tracefree tensor formula",
            "current_status": "MISSING_TF_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_TF",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_7_derivative_boundary",
            "target": "derivative and boundary terms",
            "required_identity": "all derivative, improvement, symplectic and boundary terms are included in both tensors",
            "current_evidence": "boundary units/flux/open collar not fixed",
            "current_status": "MISSING_BOUNDARY_FLUX_CONTROL",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_boundary",
            "source_path": str(SOURCE_PATHS["SRC3065_13_match_2807"]),
        }
    ),
    base(
        {
            "identity_id": "KMI3065_8_verdict",
            "target": "K_hat metric-response parent signature",
            "required_identity": "all KMI3065 component, density, convention and boundary clauses pass in one branch",
            "current_evidence": "only the formal variation step passes; live ownership and Khat identity fail",
            "current_status": "NOT_PROVED_CURRENT_CORPUS",
            "identity_signed": "false",
            "residual_if_missing": "Delta_K retained as official metric-response gap",
            "source_path": str(SOURCE_PATHS["SRC3065_05_Khat_2409"]),
        }
    ),
]

deltak_rows = [
    base(
        {
            "input_id": "DK3065_0_total",
            "quantity": "Delta_K^{mu nu}",
            "definition": "K_hat^{mu nu} - K_metric^{mu nu}[Gamma_eff]",
            "component_formula": "DeltaK_00 + DeltaK_0i + DeltaK_trace + DeltaK_TF + DeltaK_derivative_boundary + DeltaK_convention",
            "candidate_value": "MISSING_COMPONENT_INPUTS",
            "units": "same_as_metric_response_stress_or_declared_per_projection",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "q_loc;PPN_gamma;source_mass;local_force",
            "source_path": str(OUTPUTS["khat_identity"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_1_00",
            "quantity": "DeltaK_00",
            "definition": "time-time metric-response mismatch",
            "component_formula": "K_hat^{00}-K_metric^{00}",
            "candidate_value": "MISSING_KHAT00_FORMULA",
            "units": "declared_with_Khat00",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "Newton;PPN_gamma;source_normalization",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_2_0i",
            "quantity": "DeltaK_0i",
            "definition": "momentum/preferred-frame metric-response mismatch",
            "component_formula": "K_hat^{0i}-K_metric^{0i}",
            "candidate_value": "MISSING_KHAT0I_FORMULA",
            "units": "declared_with_Khat0i",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "alpha1;alpha2;alpha3;local_force",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_3_trace",
            "quantity": "DeltaK_trace",
            "definition": "spatial trace metric-response mismatch",
            "component_formula": "h_ij(K_hat^{ij}-K_metric^{ij})",
            "candidate_value": "MISSING_SPATIAL_TRACE_FORMULA",
            "units": "declared_with_spatial_trace",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "PPN_gamma;orbital;pressure_trace",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_4_tracefree",
            "quantity": "DeltaK_TF",
            "definition": "spatial tracefree/shear metric-response mismatch",
            "component_formula": "K_hat^{<ij>}-K_metric^{<ij>}",
            "candidate_value": "MISSING_TRACEFREE_FORMULA",
            "units": "declared_with_tracefree_slot",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "PPN_shear;lensing_style_tail;local_anisotropic_stress",
            "source_path": str(SOURCE_PATHS["SRC3065_14_components_2809"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_5_derivative_boundary",
            "quantity": "DeltaK_derivative_boundary",
            "definition": "derivative/improvement/boundary convention mismatch",
            "component_formula": "DeltaK_derivative_terms + DeltaK_boundary_terms + DeltaK_symplectic_improvement",
            "candidate_value": "MISSING_BOUNDARY_AND_DERIVATIVE_CONVENTION",
            "units": "declared_with_boundary_flux",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "boundary_flux;R10;R11;source_mass",
            "source_path": str(SOURCE_PATHS["SRC3065_13_match_2807"]),
        }
    ),
    base(
        {
            "input_id": "DK3065_6_density_owner",
            "quantity": "DeltaK_density_owner_defect",
            "definition": "failure of Gamma_eff to be the parent-owned density whose metric response is being compared",
            "component_formula": "K_metric[candidate Gamma_eff] - K_metric[parent Gamma_eff]",
            "candidate_value": "MISSING_PARENT_GAMMA_EFF_DENSITY_OWNER",
            "units": "declared_with_Gamma_eff_owner",
            "numeric_ready": "false",
            "bound_ready": "false",
            "observable_link": "all_GK_q_loc_channels",
            "source_path": str(OUTPUTS["density_owner"]),
        }
    ),
]

qloc_consequence_rows = [
    base(
        {
            "consequence_id": "QKC3065_0_decomposition",
            "statement": "If K_hat=K_metric[Gamma_eff]+Delta_K, then q_loc splits into Ward/Euler part plus a Delta_K defect.",
            "formula": "q_loc^nu=P_loc(Ward_Euler^nu - nabla_mu Delta_K^{mu nu})",
            "current_status": "DELTA_K_RETAINED",
            "meaning": "even if the Ward/Euler part later closes, Delta_K must be zero or bounded",
            "source_path": str(OUTPUTS["deltak_inputs"]),
        }
    ),
    base(
        {
            "consequence_id": "QKC3065_1_formal_step_guard",
            "statement": "Formal variation of a candidate density is not enough to identify live K_hat.",
            "formula": "K_metric[candidate] exists does not imply K_hat_live=K_metric[candidate]",
            "current_status": "GUARD_ACTIVE",
            "meaning": "prevents a definitional win from being smuggled into local GR",
            "source_path": str(OUTPUTS["khat_identity"]),
        }
    ),
    base(
        {
            "consequence_id": "QKC3065_2_local_GR",
            "statement": "Local GR cannot be claimed while Delta_K is missing.",
            "formula": "gamma_minus_1 still receives GK/q_loc projection tails unless Delta_K and remaining gates vanish",
            "current_status": "LOCAL_GR_BLOCKED",
            "meaning": "the project is closer because the hinge is named, not because it is closed",
            "source_path": str(SOURCE_PATHS["SRC3065_03_3064_q_loc"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3065_0_density_owner",
            "claim": "Gamma_eff is parent-owned as the current MTS scalar density",
            "status": "NO_CANDIDATE_ONLY",
            "claim_active": "false",
            "reason": "density ansatz and evenness are formal candidates, not parent signatures",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3065_1_Khat_identity",
            "claim": "K_hat=K_metric[Gamma_eff]",
            "status": "NO_FORMAL_VARIATION_ONLY",
            "claim_active": "false",
            "reason": "formal K_metric exists but live K_hat component/source identity is missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3065_2_DeltaK_zero",
            "claim": "Delta_K=0",
            "status": "NO_RETAINED_SYMBOLIC_GAP",
            "claim_active": "false",
            "reason": "component slots and boundary conventions are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3065_3_q_loc_zero",
            "claim": "q_loc^nu=0 follows as a Ward/Euler identity",
            "status": "NO_DELTAK_AND_EULER_GATES_OPEN",
            "claim_active": "false",
            "reason": "Khat identity is not signed, and Euler/boundary/projector gates are still open",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3065_4_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "3065 protects the hinge rather than pretending it is closed",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3065_0_density",
            "question": "Did 3065 parent-own Gamma_eff?",
            "answer": "NO",
            "reason": "the corpus has a reusable candidate density, but field content, units, branch domain, Z-basis and boundary conventions are not signed",
            "action": "keep density owner gate nonclaim",
        }
    ),
    base(
        {
            "decision_id": "DEC3065_1_Khat",
            "question": "Did 3065 prove K_hat=K_metric[Gamma_eff]?",
            "answer": "NO",
            "reason": "formal K_metric exists, but live K_hat component formulas and tensor-slot comparison are missing",
            "action": "retain Delta_K as the official metric-response defect",
        }
    ),
    base(
        {
            "decision_id": "DEC3065_2_next",
            "question": "Best next derivation target?",
            "answer": "LIVE_KHAT_COMPONENT_SOURCE_LIST",
            "reason": "without live K_hat components, the identity cannot even be compared component-by-component",
            "action": "build Khat tensor-slot source list and DeltaK component fill attempt before claiming identity",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3065_0_3066",
            "next_checkpoint": "3066-Y5-R2FR-Khat-component-source-list-and-DeltaK-tensor-slot-fill-or-identity-proof-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Khat_component_source_list_and_DeltaK_tensor_slot_fill_or_identity_proof_under_AX1090_3066.py",
            "mission": "find or construct live K_hat component formulas for 00, 0i, spatial trace, tracefree and boundary slots; if absent, fill Delta_K tensor-slot nonclaim rows",
            "starting_equation": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "claim_policy": "no Khat/q_loc/local-GR claim unless live K_hat and K_metric are compared in every tensor slot with units and boundary convention fixed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["density_owner"], density_owner_rows)
write_csv(OUTPUTS["khat_identity"], khat_identity_rows)
write_csv(OUTPUTS["deltak_inputs"], deltak_rows)
write_csv(OUTPUTS["qloc_consequence"], qloc_consequence_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["density_owner"], BRANCH_OUTPUTS["density_owner_copy"])
copy_csv(OUTPUTS["khat_identity"], BRANCH_OUTPUTS["khat_identity_copy"])
copy_csv(OUTPUTS["deltak_inputs"], BRANCH_OUTPUTS["deltak_inputs_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3065 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["density_owner"],
    OUTPUTS["khat_identity"],
    OUTPUTS["deltak_inputs"],
    OUTPUTS["qloc_consequence"],
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

all_density_unsigned = all(row["parent_signed"] == "false" for row in density_owner_rows)
all_identity_unsigned = all(row["identity_signed"] == "false" for row in khat_identity_rows)
formal_step_guarded = any(row["current_status"] == "PASS_FORMAL_STEP_ONLY" and row["identity_signed"] == "false" for row in khat_identity_rows)
all_deltak_nonclaim = all(row["numeric_ready"] == "false" and row["bound_ready"] == "false" and row["valid_for_claim"] == "false" for row in deltak_rows)
all_deltak_missing = all("MISSING" in row["candidate_value"] for row in deltak_rows)
all_claims_inactive = all(str(row["claim_active"]).lower() == "false" for row in claim_rows)
next_is_3066 = next_rows[0]["next_checkpoint"].startswith("3066-")

validation_rows = [
    base({"validation_id": "VAL3065_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3065_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3065_02_density_unsigned", "passed": all_density_unsigned, "requirement": "Gamma_eff density owner remains unsigned", "evidence": OUTPUTS["density_owner"].name}),
    base({"validation_id": "VAL3065_03_identity_unsigned", "passed": all_identity_unsigned and formal_step_guarded, "requirement": "Khat identity remains unsigned despite formal variation step", "evidence": OUTPUTS["khat_identity"].name}),
    base({"validation_id": "VAL3065_04_deltak_nonclaim", "passed": all_deltak_nonclaim and all_deltak_missing, "requirement": "Delta_K rows are missing-input nonclaim rows", "evidence": OUTPUTS["deltak_inputs"].name}),
    base({"validation_id": "VAL3065_05_qloc_consequence_guard", "passed": any("DELTA_K_RETAINED" in row["current_status"] for row in qloc_consequence_rows), "requirement": "q_loc remains guarded by retained Delta_K defect", "evidence": OUTPUTS["qloc_consequence"].name}),
    base({"validation_id": "VAL3065_06_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3065_07_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3065" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3065 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3065_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3065_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3065_10_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3065_11_next_target", "passed": next_is_3066, "requirement": "next target selects Khat component source list or DeltaK tensor-slot fill", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3065_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3065 - Gamma_eff Density Owner and Khat Metric-Response Identity or DeltaK Input Fill

Status: `Y5_R2FR_3065_Gamma_eff_candidate_only_Khat_identity_not_signed_DeltaK_retained`

Generated: `{RUN_UTC}`

## Verdict

3065 tests the hinge identified in 3064:

`K_hat = K_metric[Gamma_eff]`.

The current corpus gives a real formal step: once a candidate density exists, the formal metric response can be written. That is useful, but it is not enough. The live MTS `K_hat` has not been shown equal to that metric response in the same branch, convention, tensor slots, units and boundary treatment.

So the result is:

`Delta_K = K_hat - K_metric[Gamma_eff]`

remains an official retained metric-response defect. Consequently:

`q_loc = Ward/Euler part - P_loc div(Delta_K)`.

No `q_loc=0`, `Delta_extra_GK_linear=0`, or local-GR/PPN claim is active.

## Gamma_eff Density Owner Gate

{md_table(density_owner_rows, ["gate_id", "object", "candidate_or_requirement", "current_status", "parent_signed", "what_is_real_progress", "blocking_gap"])}

## Khat Metric-Response Identity Audit

{md_table(khat_identity_rows, ["identity_id", "target", "required_identity", "current_evidence", "current_status", "identity_signed", "residual_if_missing"])}

## DeltaK Input Rows

{md_table(deltak_rows, ["input_id", "quantity", "definition", "component_formula", "candidate_value", "numeric_ready", "bound_ready", "observable_link"])}

## q_loc Consequence Ledger

{md_table(qloc_consequence_rows, ["consequence_id", "statement", "formula", "current_status", "meaning"])}

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
    raise SystemExit(f"3065 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: Gamma_eff candidate only; Khat identity not signed; Delta_K retained")
