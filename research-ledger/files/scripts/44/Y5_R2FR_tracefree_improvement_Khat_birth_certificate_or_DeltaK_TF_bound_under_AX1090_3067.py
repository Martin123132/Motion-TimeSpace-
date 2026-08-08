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

CHECKPOINT = "3067"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3067_00_3066_doc": ROOT / "3066-Y5-R2FR-Khat-component-source-list-and-DeltaK-tensor-slot-fill-or-identity-proof-under-AX1090.md",
    "SRC3067_01_3066_next": RESIDUALS / "P8_Y5_R2FR_3066_NEXT_TARGET.csv",
    "SRC3067_02_3066_route": RESIDUALS / "P8_Y5_R2FR_3066_TRACEFREE_ROUTE_AND_AMPLITUDE_LEDGER.csv",
    "SRC3067_03_3066_deltak_slots": RESIDUALS / "P8_Y5_R2FR_3066_DELTAK_TENSOR_SLOT_ROWS_NONCLAIM.csv",
    "SRC3067_04_1190_tracefree_solver": RESIDUALS / "P8_Y5_R10_1190_TRACEFREE_KHAT_SOLVER_GATE.csv",
    "SRC3067_05_794_tracefree_solver": RESIDUALS / "P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv",
    "SRC3067_06_1193_ricci_branch": RESIDUALS / "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
    "SRC3067_07_1287_KL00": RESIDUALS / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "SRC3067_08_833_amplitude": RESIDUALS / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
    "SRC3067_09_2219_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_KHAT_SOURCE_OWNER_AUDIT.csv",
    "SRC3067_10_2219_birth_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_2219_KHAT_BIRTH_CERTIFICATE_GATE.csv",
    "SRC3067_11_1525_origin": RESIDUALS / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv",
    "SRC3067_12_1527_adoption": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
    "SRC3067_13_1527_aux_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
    "SRC3067_14_1527_multiplier_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_MULTIPLIER_STRESS_SILENCE_GATE.csv",
    "SRC3067_15_1527_nonlocality": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_NONLOCALITY_GUARD.csv",
    "SRC3067_16_1527_phi_owner": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_PHI_OWNER_SOURCE_HUNT.csv",
    "SRC3067_17_1527_claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_CLAIM_GATE.csv",
    "SRC3067_18_1527_local_gr": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_LOCAL_GR_NEWTON_STATUS.csv",
    "SRC3067_19_794_curvature_amplitude": RESIDUALS / "P8_Y5_R10_794_CURVATURE_AND_AMPLITUDE_GATES.csv",
    "SRC3067_20_794_ppn_bounds": RESIDUALS / "P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv",
    "SRC3067_21_1193_claim_gates": RESIDUALS / "P8_Y5_R10_1193_CLAIM_GATES.csv",
    "SRC3067_22_1193_bound_inputs": RESIDUALS / "P8_Y5_R10_1193_BOUND_INPUT_ROWS.csv",
    "SRC3067_23_1193_compensator": RESIDUALS / "P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv",
    "SRC3067_24_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3067_SOURCE_REGISTER.csv",
    "birth_gate": RESIDUALS / "P8_Y5_R2FR_3067_TRACEFREE_BIRTH_CERTIFICATE_GATE.csv",
    "divergence_domain": RESIDUALS / "P8_Y5_R2FR_3067_KL_DIVERGENCE_AND_DOMAIN_AUDIT.csv",
    "deltak_tf_rows": RESIDUALS / "P8_Y5_R2FR_3067_DELTAK_TF_BOUND_ROWS_NONCLAIM.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3067_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3067_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3067_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3067_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3067_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "birth_gate_copy": PARENT_ACTION / "tracefree_Khat_birth_certificate_gate_3067_NOT_SIGNED.csv",
    "divergence_domain_copy": PARENT_ACTION / "tracefree_KL_divergence_domain_audit_3067_GUARDED.csv",
    "deltak_tf_copy": LOCAL_BOUNDS / "DeltaK_TF_bound_rows_3067_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3067_phi_owner_or_DeltaK_TF_bound_NEXT_NONCLAIM.csv",
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
        "certificate_pass",
        "gate_pass",
        "numeric_ready",
        "bound_ready",
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
            "role": "tracefree_Khat_birth_certificate_evidence" if source_id != "SRC3067_24_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

birth_gate_rows = [
    base(
        {
            "gate_id": "TFBC3067_0_parent_action_term",
            "clause": "parent action birth certificate",
            "required_contract": "A local parent term such as S_I=int sqrt(-g) c_I phi R or equivalent is written with fields, coefficient, sign, measure and domain before readout.",
            "best_current_evidence": "1525/1527 stage a phi R improvement response, but 2219 records it as staged rather than parent-signed.",
            "status": "STAGED_NOT_PARENT_SIGNED",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_PARENT_ACTION_TERM;MISSING_COEFFICIENT;MISSING_SIGN_CONVENTION;MISSING_DOMAIN",
            "consequence": "K_L cannot yet be promoted to live MTS K_hat.",
            "source_ids": "SRC3067_10_2219_birth_gate;SRC3067_11_1525_origin;SRC3067_12_1527_adoption",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_1_phi_owner_source_equation",
            "clause": "phi owner and source equation",
            "required_contract": "phi is a parent-owned local field or auxiliary variable with an Euler equation that yields Box phi=(2/3)(Gamma_eff+C) in the relevant branch.",
            "best_current_evidence": "1527 labels phi owner unresolved; 1190/794 derive only the formal solver condition.",
            "status": "OWNER_UNRESOLVED",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_PHI_OWNER;MISSING_LOCAL_EULER_EQUATION;MISSING_SOURCE_NORMALIZATION",
            "consequence": "The cancellation div K_L = grad Gamma_eff remains a formal inverse-problem solution, not a parent theorem.",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_05_794_tracefree_solver;SRC3067_16_1527_phi_owner",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_2_live_Khat_adoption",
            "clause": "live tensor adoption",
            "required_contract": "The current MTS K_hat is explicitly defined as the tracefree metric response/improvement tensor in the same branch and convention.",
            "best_current_evidence": "3066 finds a formal route but no live source-signed component list; 1527 adoption row is staged nonclaim.",
            "status": "ADOPTION_ROW_STAGED_NONCLAIM",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_LIVE_KHAT_DEFINITION;MISSING_COMPONENT_LIST;MISSING_PROJECTOR_CONVENTION",
            "consequence": "DeltaK_TF must remain a live residual.",
            "source_ids": "SRC3067_00_3066_doc;SRC3067_02_3066_route;SRC3067_12_1527_adoption",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_3_curved_domain_exactness",
            "clause": "curvature and exactness domain",
            "required_contract": "The branch is Ricci-flat, Einstein, or has a sourced vector/tensor compensator proving the Ricci curl obstruction vanishes.",
            "best_current_evidence": "1193 derives the Ricci-curl obstruction and says generic matter Ricci domains are not automatically exact.",
            "status": "GENERIC_MATTER_DOMAIN_BLOCKED",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_RICCI_DOMAIN_CLASSIFIER;MISSING_COMPENSATOR_SOURCE;MISSING_EXACTNESS_THEOREM",
            "consequence": "Flat-patch cancellation is not enough for a local-GR theorem in matter environments.",
            "source_ids": "SRC3067_06_1193_ricci_branch;SRC3067_19_794_curvature_amplitude;SRC3067_23_1193_compensator",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_4_boundary_green_projector",
            "clause": "Green inverse and boundary silence",
            "required_contract": "The inverse Box/Green construction, boundary condition, local collar and projector are fixed so no boundary force leaks into q_loc.",
            "best_current_evidence": "794/1190 keep boundary conditions as missing; 1527 nonlocality guard remains nonclaim.",
            "status": "BOUNDARY_PROJECTOR_OPEN",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_GREEN_INVERSE;MISSING_BOUNDARY_CONDITION;MISSING_LOCAL_PROJECTOR_SILENCE",
            "consequence": "K_L can be a useful formal solution but not a physical local plateau theorem.",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_05_794_tracefree_solver;SRC3067_15_1527_nonlocality",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_5_multiplier_and_matter_silence",
            "clause": "auxiliary multiplier and matter descent silence",
            "required_contract": "Any lambda_phi or auxiliary enforcement stress is silent or absorbed, and matter action descends without representative-dependent Weyl/disformal terms.",
            "best_current_evidence": "1527 multiplier-stress and local-GR/Newton gates remain unsigned.",
            "status": "AUXILIARY_STRESS_NOT_SILENT",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_MULTIPLIER_STRESS_SILENCE;MISSING_MATTER_DESCENT;MISSING_WEYL_DISFORMAL_ZERO",
            "consequence": "The improvement tensor could still back-react as a non-GR local stress channel.",
            "source_ids": "SRC3067_14_1527_multiplier_silence;SRC3067_18_1527_local_gr",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_6_amplitude_metric_response",
            "clause": "metric-response amplitude safety",
            "required_contract": "K_L cancellation comes with a sourced bound showing the induced tracefree metric response stays below PPN/local-force limits.",
            "best_current_evidence": "833 gives ||K||_L2=sqrt(n/(n-1))*||Gamma||_L2, so no automatic parametric suppression exists.",
            "status": "NO_PARAMETRIC_SUPPRESSION",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_METRIC_RESPONSE_COEFFICIENT;MISSING_PPN_VECTOR;MISSING_LOCAL_FORCE_BOUND",
            "consequence": "q_loc cancellation alone would not prove metric safety.",
            "source_ids": "SRC3067_08_833_amplitude;SRC3067_20_794_ppn_bounds;SRC3067_22_1193_bound_inputs",
        }
    ),
    base(
        {
            "gate_id": "TFBC3067_7_units_readout_normalization",
            "clause": "units and readout",
            "required_contract": "Gamma_eff, phi, K_hat and the PPN/local observables share locked units, normalization and weak-field projection.",
            "best_current_evidence": "3065/3066 retain units/readout as missing in DeltaK and q_loc consequence rows.",
            "status": "UNITS_READOUT_OPEN",
            "gate_pass": "false",
            "missing_for_claim": "MISSING_UNITS;MISSING_OBSERVABLE_READOUT;MISSING_WEAK_FIELD_NORMALIZATION",
            "consequence": "No local-GR, PPN, R10, clock or orbital claim can be made from this route yet.",
            "source_ids": "SRC3067_03_3066_deltak_slots;SRC3067_17_1527_claim_gate",
        }
    ),
]

divergence_rows = [
    base(
        {
            "audit_id": "KLD3067_0_tracefree_identity",
            "theorem_or_step": "four-dimensional tracefree identity",
            "formula": "g_{mu nu} K_L^{mu nu}=2 Box phi-(1/2)*4 Box phi=0",
            "result": "EXACT_FORMAL_IDENTITY",
            "pass_status": "formal_only_guarded",
            "domain": "4D geometry",
            "blocker": "identity is algebraic but does not parent-sign K_L as live Khat",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_05_794_tracefree_solver",
        }
    ),
    base(
        {
            "audit_id": "KLD3067_1_curved_divergence",
            "theorem_or_step": "curved divergence identity",
            "formula": "nabla_mu K_L^{mu nu}=(3/2)nabla^nu Box phi+2 R^nu_sigma nabla^sigma phi",
            "result": "CURVED_RESIDUAL_DERIVED_UP_TO_RIEMANN_SIGN",
            "pass_status": "derived_but_not_claim",
            "domain": "curved local domain",
            "blocker": "Ricci term must be cancelled, classified, or bounded in matter regions",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_06_1193_ricci_branch",
        }
    ),
    base(
        {
            "audit_id": "KLD3067_2_flat_patch_solver",
            "theorem_or_step": "flat/local commuting derivative solver",
            "formula": "Box phi=(2/3)(Gamma_eff+C) gives partial_mu K_L^{mu nu}=partial^nu Gamma_eff",
            "result": "FORMAL_FLAT_PATCH_CANCELLATION",
            "pass_status": "conditional_only",
            "domain": "flat patch or negligible curvature collar",
            "blocker": "needs parent phi equation, Green inverse and patch-error budget",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_05_794_tracefree_solver",
        }
    ),
    base(
        {
            "audit_id": "KLD3067_3_einstein_branch_solver",
            "theorem_or_step": "Einstein/Ricci-aligned branch",
            "formula": "(3/2)Box phi+2 Lambda_E phi=Gamma_eff+C can cancel the divergence in an Einstein branch",
            "result": "SPECIAL_BRANCH_CONDITIONAL",
            "pass_status": "conditional_only",
            "domain": "Ricci-flat or Einstein-aligned local domain",
            "blocker": "does not cover generic matter domain without an exactness theorem",
            "source_ids": "SRC3067_06_1193_ricci_branch",
        }
    ),
    base(
        {
            "audit_id": "KLD3067_4_generic_matter_obstruction",
            "theorem_or_step": "Ricci-curl obstruction",
            "formula": "curl[(3/2)nabla Box phi+2 Ricci.grad phi]=2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi)",
            "result": "GENERIC_MATTER_NOT_AUTOMATICALLY_EXACT",
            "pass_status": "obstruction_retained",
            "domain": "generic matter Ricci region",
            "blocker": "need compensator/current, alignment theorem, or bounded residual",
            "source_ids": "SRC3067_06_1193_ricci_branch;SRC3067_23_1193_compensator",
        }
    ),
    base(
        {
            "audit_id": "KLD3067_5_amplitude_law",
            "theorem_or_step": "tracefree Hessian amplitude law",
            "formula": "||K_L||_L2=sqrt(n/(n-1))*||Gamma_eff||_L2 in the flat carrier normalization",
            "result": "NO_AUTOMATIC_AMPLITUDE_SUPPRESSION",
            "pass_status": "bound_needed",
            "domain": "flat carrier amplitude estimate",
            "blocker": "metric response coefficient and observational residual vector are not sourced",
            "source_ids": "SRC3067_08_833_amplitude",
        }
    ),
]

deltak_tf_rows = [
    base(
        {
            "row_id": "DKTF3067_0_total_tracefree_residual",
            "quantity": "DeltaK_TF",
            "definition": "K_hat^{<ij>} - K_metric^{<ij>}[Gamma_eff]",
            "bound_expression": "||DeltaK_TF|| <= ||K_hat^{<ij>}-K_L^{<ij>}|| + ||K_L^{<ij>}-K_metric^{<ij>}||",
            "symbolic_value": "MISSING_LIVE_KHAT_ADOPTION + MISSING_PARENT_METRIC_RESPONSE_MATCH",
            "status": "BOUND_ONLY_SCHEMA_NONCLAIM",
            "missing_for_claim": "MISSING_LIVE_KHAT_ADOPTION;MISSING_PARENT_METRIC_RESPONSE_MATCH;MISSING_NUMERIC_BOUND",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_02_3066_route;SRC3067_12_1527_adoption",
        }
    ),
    base(
        {
            "row_id": "DKTF3067_1_phi_owner_component",
            "quantity": "epsilon_phi_owner",
            "definition": "failure of phi to be a parent-owned local field with the required source equation",
            "bound_expression": "||epsilon_phi_owner|| enters DeltaK_TF and q_loc through div K_L",
            "symbolic_value": "MISSING_PHI_OWNER_SOURCE",
            "status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "MISSING_PHI_OWNER;MISSING_EULER_EQUATION",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_16_1527_phi_owner",
        }
    ),
    base(
        {
            "row_id": "DKTF3067_2_curvature_exactness_component",
            "quantity": "epsilon_Ricci_curl",
            "definition": "generic matter obstruction to writing div K_L as grad Gamma_eff",
            "bound_expression": "||2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi)||",
            "symbolic_value": "MISSING_RICCI_DOMAIN_OR_COMPENSATOR",
            "status": "MISSING_ARENA_PROJECTION",
            "missing_for_claim": "MISSING_RICCI_CLASSIFIER;MISSING_COMPENSATOR;MISSING_DOMAIN_BOUND",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_06_1193_ricci_branch;SRC3067_23_1193_compensator",
        }
    ),
    base(
        {
            "row_id": "DKTF3067_3_boundary_green_component",
            "quantity": "epsilon_boundary_Green",
            "definition": "boundary or Green-inverse leakage in the tracefree scalar solver",
            "bound_expression": "||P_loc div K_L - P_loc grad Gamma_eff||_boundary",
            "symbolic_value": "MISSING_GREEN_BOUNDARY_PROJECTOR",
            "status": "MISSING_BOUNDARY_INPUT",
            "missing_for_claim": "MISSING_GREEN_FUNCTION;MISSING_BOUNDARY_CONDITION;MISSING_PROJECTOR",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_04_1190_tracefree_solver;SRC3067_15_1527_nonlocality",
        }
    ),
    base(
        {
            "row_id": "DKTF3067_4_amplitude_metric_component",
            "quantity": "epsilon_KL_metric_response",
            "definition": "metric response sourced by the tracefree Hessian improvement",
            "bound_expression": "sqrt(n/(n-1))*||Gamma_eff|| times response coefficient and local readout",
            "symbolic_value": "MISSING_RESPONSE_COEFFICIENT_AND_PPN_VECTOR",
            "status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "MISSING_RESPONSE_COEFFICIENT;MISSING_PPN_LIMIT;MISSING_R10_CLOCK_ORBITAL_READOUT",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_08_833_amplitude;SRC3067_20_794_ppn_bounds;SRC3067_22_1193_bound_inputs",
        }
    ),
    base(
        {
            "row_id": "DKTF3067_5_auxiliary_stress_component",
            "quantity": "epsilon_aux_stress",
            "definition": "stress from enforcing phi or quotient constraints",
            "bound_expression": "||T_lambda_phi^{TF}+T_aux^{TF}||",
            "symbolic_value": "MISSING_MULTIPLIER_STRESS_SILENCE",
            "status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "MISSING_MULTIPLIER_STRESS_SILENCE;MISSING_MATTER_DESCENT",
            "numeric_ready": "false",
            "bound_ready": "false",
            "source_ids": "SRC3067_14_1527_multiplier_silence;SRC3067_18_1527_local_gr",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3067_0_tracefree_birth_certificate",
            "claim": "K_L is parent-born and live-adopted as current MTS K_hat",
            "status": "NO_BIRTH_CERTIFICATE_NOT_CLOSED",
            "claim_active": "false",
            "reason": "all birth-certificate gates remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3067_1_DeltaK_TF_zero",
            "claim": "DeltaK_TF=0",
            "status": "NO_RETAINED_BOUND_COMPONENT",
            "claim_active": "false",
            "reason": "live adoption, curvature, boundary and amplitude inputs are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3067_2_q_loc_zero",
            "claim": "q_loc^nu=0 follows from the tracefree improvement route",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "div K_L cancellation is formal/conditional and not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3067_3_local_GR_PPN",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "DeltaK_TF and amplitude/readout residuals remain live",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3067_0_birth_certificate",
            "question": "Did 3067 parent-sign the tracefree Khat route?",
            "answer": "NO",
            "reason": "K_L is algebraically strong but has no live parent action, phi owner, boundary silence or amplitude safety certificate.",
            "action": "do not promote Khat/q_loc/local-GR; keep DeltaK_TF bound-only rows",
        }
    ),
    base(
        {
            "decision_id": "DEC3067_1_progress",
            "question": "Did 3067 improve the route?",
            "answer": "YES_BOTTLENECK_SHARPENED",
            "reason": "the route is now reduced to phi-owner/source equation plus adoption/boundary/amplitude gates, rather than a broad Khat mystery.",
            "action": "attack phi owner/source equation first because other gates depend on it",
        }
    ),
    base(
        {
            "decision_id": "DEC3067_2_best_next",
            "question": "Best next derivation target?",
            "answer": "PHI_OWNER_SOURCE_EQUATION_OR_TRACEFREE_ROUTE_DEMOTION",
            "reason": "without parent phi equation, the tracefree route is only an inverse solver and cannot reduce MTS to GR locally.",
            "action": "build 3068 around deriving phi's parent equation or explicitly demoting the route to closure/bound-only",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3067_0_3068",
            "next_checkpoint": "3068-Y5-R2FR-phi-owner-source-equation-or-tracefree-route-demotion-under-AX1090.md",
            "script": "scripts/Y5_R2FR_phi_owner_source_equation_or_tracefree_route_demotion_under_AX1090_3068.py",
            "mission": "try to derive a parent-owned phi source equation that makes the tracefree K_L route a real Khat mechanism; if not, demote tracefree K_L to closure/bound-only",
            "starting_equation": "K_L^{mu nu}=2 nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi with div K_L=(3/2)grad Box phi+2 Ricci.grad phi",
            "claim_policy": "no Khat/q_loc/local-GR claim unless phi has a parent Euler equation, live adoption, boundary silence and amplitude/readout bounds",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["birth_gate"], birth_gate_rows)
write_csv(OUTPUTS["divergence_domain"], divergence_rows)
write_csv(OUTPUTS["deltak_tf_rows"], deltak_tf_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["birth_gate"], BRANCH_OUTPUTS["birth_gate_copy"])
copy_csv(OUTPUTS["divergence_domain"], BRANCH_OUTPUTS["divergence_domain_copy"])
copy_csv(OUTPUTS["deltak_tf_rows"], BRANCH_OUTPUTS["deltak_tf_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": str(path.exists()),
            "row_count": row_count(path),
            "description": "3067 branch copy for parent-action/local-bound/acquisition-queue continuity",
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
all_birth_gates_false = all(row["gate_pass"] == "false" and row["valid_for_claim"] == "false" for row in birth_gate_rows)
critical_phi_gate_false = any(row["gate_id"] == "TFBC3067_1_phi_owner_source_equation" and row["gate_pass"] == "false" for row in birth_gate_rows)
formal_identity_guarded = any(row["audit_id"] == "KLD3067_0_tracefree_identity" and row["pass_status"] == "formal_only_guarded" for row in divergence_rows)
curved_divergence_present = any(row["audit_id"] == "KLD3067_1_curved_divergence" and "Ricci" in row["blocker"] for row in divergence_rows)
generic_obstruction_retained = any(row["audit_id"] == "KLD3067_4_generic_matter_obstruction" and row["pass_status"] == "obstruction_retained" for row in divergence_rows)
all_divergence_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in divergence_rows)
all_deltak_tf_nonclaim = all(
    row["numeric_ready"] == "false"
    and row["bound_ready"] == "false"
    and row["valid_for_claim"] == "false"
    and "MISSING" in row["symbolic_value"]
    for row in deltak_tf_rows
)
all_claims_inactive = all(row["claim_active"] == "false" for row in claim_rows)
next_is_3068 = next_rows[0]["next_checkpoint"].startswith("3068-")

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

validation_rows = [
    base({"validation_id": "VAL3067_00_sources_exist", "passed": all_sources_exist, "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3067_01_sources_parse", "passed": all_sources_parse, "requirement": "all cited CSV sources parse and markdown sources exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3067_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3067_03_birth_gates_unsigned", "passed": all_birth_gates_false and critical_phi_gate_false, "requirement": "tracefree Khat birth certificate is not signed", "evidence": OUTPUTS["birth_gate"].name}),
    base({"validation_id": "VAL3067_04_formal_identity_guarded", "passed": formal_identity_guarded and all_divergence_nonclaim, "requirement": "exact tracefree identity is recorded but guarded from claim", "evidence": OUTPUTS["divergence_domain"].name}),
    base({"validation_id": "VAL3067_05_curved_obstruction_retained", "passed": curved_divergence_present and generic_obstruction_retained, "requirement": "curvature/Ricci exactness obstruction remains explicit", "evidence": OUTPUTS["divergence_domain"].name}),
    base({"validation_id": "VAL3067_06_DeltaK_TF_nonclaim", "passed": all_deltak_tf_nonclaim, "requirement": "DeltaK_TF rows are missing-input bound-only rows", "evidence": OUTPUTS["deltak_tf_rows"].name}),
    base({"validation_id": "VAL3067_07_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row activates Khat, q_loc, local-GR, R10, PPN, clock or orbital claims", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3067_08_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3067" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3067 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3067_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3067_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3067_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench generated-output count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3067_12_next_target", "passed": next_is_3068, "requirement": "next target selects phi-owner source equation or tracefree demotion", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3067_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3067 - Tracefree Improvement Khat Birth Certificate or DeltaK_TF Bound

Status: `Y5_R2FR_3067_tracefree_Khat_birth_certificate_not_signed_DeltaK_TF_bound_only`

Generated: `{RUN_UTC}`

## Verdict

3067 tested whether the tracefree longitudinal candidate can become the live MTS `K_hat`.

The algebraic route is real:

`K_L^{{mu nu}} = 2 nabla^mu nabla^nu phi - (1/2) g^{{mu nu}} Box phi`

is exactly tracefree in four dimensions, and its curved divergence is

`nabla_mu K_L^{{mu nu}}=(3/2)nabla^nu Box phi+2 R^nu_sigma nabla^sigma phi`

up to the Riemann-sign convention.

That is a serious mechanism-shaped object, not fluff. But it is **not yet a parent-signed mechanism**. The current corpus does not close the parent action, phi-owner/source-equation, live-adoption, boundary, curvature-domain, auxiliary-stress or amplitude/readout gates.

Therefore 3067 does **not** claim `K_hat=K_L`, `DeltaK_TF=0`, `q_loc^nu=0`, local GR, PPN, R10, clock or orbital success. The route remains useful, but only as a guarded derivation target or as a `DeltaK_TF` bound component.

## Tracefree Birth Certificate Gate

{md_table(birth_gate_rows, ["gate_id", "clause", "status", "gate_pass", "missing_for_claim", "consequence"])}

## KL Divergence and Domain Audit

{md_table(divergence_rows, ["audit_id", "theorem_or_step", "formula", "result", "pass_status", "blocker"])}

## DeltaK_TF Bound Rows

{md_table(deltak_tf_rows, ["row_id", "quantity", "definition", "bound_expression", "symbolic_value", "status", "numeric_ready", "bound_ready"])}

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

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3067 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: tracefree Khat birth certificate not signed; DeltaK_TF retained as nonclaim bound-only route")
