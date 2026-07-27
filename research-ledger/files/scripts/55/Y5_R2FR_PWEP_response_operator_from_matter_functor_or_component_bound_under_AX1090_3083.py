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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3083"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3083-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3083_00_3082_doc": ROOT / "3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton-under-AX1090.md",
    "SRC3083_01_3082_next": RESIDUALS / "P8_Y5_R2FR_3082_NEXT_TARGET.csv",
    "SRC3083_02_3082_projection_skeleton": RESIDUALS
    / "P8_Y5_R2FR_3082_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_NONCLAIM.csv",
    "SRC3083_03_3082_wep_requirements": RESIDUALS / "P8_Y5_R2FR_3082_WEP_RESPONSE_OPERATOR_REQUIREMENTS.csv",
    "SRC3083_04_3082_projective_guard": RESIDUALS / "P8_Y5_R2FR_3082_PROJECTIVE_GUARD_REQUIREMENTS.csv",
    "SRC3083_05_3082_claim_status": RESIDUALS / "P8_Y5_R2FR_3082_CLAIM_STATUS.csv",
    "SRC3083_06_1837_doc": ROOT / "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
    "SRC3083_07_1837_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_DERIVATION_ATTEMPT.csv",
    "SRC3083_08_1837_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_RESPONSE_CONTRACT.csv",
    "SRC3083_09_1837_bound_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_WEP_COMPONENT_BOUND_ROWS.csv",
    "SRC3083_10_1837_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_CURRENT_CORPUS_GATE.csv",
    "SRC3083_11_1045_doc": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
    "SRC3083_12_1045_functor_audit": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "SRC3083_13_1045_qbar_geom": RESIDUALS / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
    "SRC3083_14_1045_qbar_components": RESIDUALS / "P8_Y5_R10_1045_QBAR_COMPONENT_FILL_ROWS.csv",
    "SRC3083_15_1045_claim_gates": RESIDUALS / "P8_Y5_R10_1045_CLAIM_GATES.csv",
    "SRC3083_16_MICROSCOPE_provenance": RESIDUALS / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv",
    "SRC3083_17_tau_wep_schema": RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "SRC3083_18_branch_lock": MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
    "SRC3083_19_eta_convention": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
    "SRC3083_20_local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "SRC3083_21_single_coframe": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
    "SRC3083_22_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3083_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_3083_PWEP_DERIVATION_ATTEMPT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3083_PWEP_RESPONSE_CONTRACT.csv",
    "component_bounds": RESIDUALS / "P8_Y5_R2FR_3083_WEP_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "corpus_gate": RESIDUALS / "P8_Y5_R2FR_3083_CURRENT_CORPUS_GATE.csv",
    "dependency_ladder": RESIDUALS / "P8_Y5_R2FR_3083_PARENT_SIGNATURE_DEPENDENCY_LADDER.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3083_SCORE_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3083_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3083_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3083_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3083_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3083_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": LOCAL_BOUNDS / "PWEP_response_contract_3083_NONCLAIM.csv",
    "component_bounds_copy": LOCAL_BOUNDS / "WEP_component_bound_rows_3083_NONCLAIM.csv",
    "corpus_gate_copy": LOCAL_BOUNDS / "PWEP_current_corpus_gate_3083_NONCLAIM.csv",
    "dependency_ladder_copy": LOCAL_BOUNDS / "PWEP_parent_signature_dependency_ladder_3083_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3083_ordinary_matter_action_signature_source_label_forgetting_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


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
        "projection_ready",
        "matrix_ready",
        "coefficient_ready",
        "score_allowed",
        "operator_ready",
        "bound_ready",
        "parent_signed",
        "component_claim",
        "local_gr_claim",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
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
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "P_WEP_response_operator_evidence" if source_id != "SRC3083_22_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

derivation_rows = [
    base(
        {
            "theorem_id": "PWD3083_0_target",
            "claim_piece": "P_WEP response operator",
            "formal_statement": "For ordinary matter species A,B, eta_AB = n_mu[(a_A^mu-a_B^mu)]/g_N = P_WEP_eta_AB · DeltaGamma_WEP.",
            "proof_move": "derive the species acceleration from the parent-descended matter action and subtract A-B before inserting any empirical WEP bound",
            "current_status": "TARGET_DEFINED",
            "missing_for_parent_claim": "P_WEP_eta_AB must be derived from the parent matter functor, readout map, and branch lock",
            "parent_signed": "false",
            "source_ids": "SRC3083_02_3082_projection_skeleton;SRC3083_07_1837_derivation",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_1_conditional_zero_theorem",
            "claim_piece": "universal observed matter descent gives P_WEP=0",
            "formal_statement": "If every ordinary S_A factors as Sbar_A[Psi_A,e_obs(q_loc(Phi)),omega[e_obs],theta_A] with quotient-owned constants, one current/measure owner, and no independent Gamma/source-only species selector, then a_A^mu=a_B^mu for structureless test bodies and P_WEP_eta_AB=0.",
            "proof_move": "chain rule gives Lie_v e_obs=0 for vertical representatives; the minimal observed-geometry Euler equation is species-blind; subtracting A-B kills the common mode",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_parent_claim": "matter category, observed coframe functor, no-shadow-frame, constants/current owner, source-label forgetting, readout/product kernels",
            "parent_signed": "false",
            "source_ids": "SRC3083_07_1837_derivation;SRC3083_12_1045_functor_audit;SRC3083_13_1045_qbar_geom",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_2_response_decomposition",
            "claim_piece": "non-universal leakage decomposition",
            "formal_statement": "a_A^mu-a_B^mu = (P_A^spin-P_B^spin)Delta_spin + (P_A^mat-P_B^mat)Delta_material + (P_A^clock-P_B^clock)Delta_clock + (P_A^proj-P_B^proj)Delta_projective + Delta_frame/readout.",
            "proof_move": "retain every species-dependent variation channel as a linearized response coefficient until a parent theorem kills it",
            "current_status": "FORMAL_DECOMPOSITION_WRITTEN",
            "missing_for_parent_claim": "component response tensors, material sensitivities, common units, source/readout branch",
            "parent_signed": "false",
            "source_ids": "SRC3083_08_1837_contract;SRC3083_03_3082_wep_requirements",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_3_no_source_only_scalar",
            "claim_piece": "source-label/species-weight silence",
            "formal_statement": "No species-indexed w_A, A_A(X), B_A(X), m_A(X), clock marker, or material label may appear unless carried by an observable parent field/current/representation object.",
            "proof_move": "object-language/source-label forgetting would forbid WEP-only source scalars before variation",
            "current_status": "CONDITIONAL_ONLY",
            "missing_for_parent_claim": "parent object language, material representation category, and measure/current owner remain unsigned",
            "parent_signed": "false",
            "source_ids": "SRC3083_12_1045_functor_audit;SRC3083_14_1045_qbar_components",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_4_same_geometry_stack",
            "claim_piece": "same geometry stack for force, clock and readout",
            "formal_statement": "mu_m,e_m,g_m,omega_m,D_m, tau, rods, and test-body readout all descend through the same q_loc(Phi) branch.",
            "proof_move": "single observed coframe plus connection/readout descent would remove frame and connection re-entry into WEP",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_parent_claim": "q-map, matter functor, geometry stack, tau/normal lock and arena functors are not all signed",
            "parent_signed": "false",
            "source_ids": "SRC3083_12_1045_functor_audit;SRC3083_21_single_coframe",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_5_bound_comparison",
            "claim_piece": "WEP bound comparison",
            "formal_statement": "A WEP prediction row may compare to a source bound only after P_WEP, product convention, material/source/readout kernels and branch lock share the same parent branch.",
            "proof_move": "separate prediction-side derivation from comparison-side bound anchor",
            "current_status": "BOUND_ANCHOR_EXISTS_PREDICTION_SIDE_MISSING",
            "missing_for_parent_claim": "official readout/source kernels and P_WEP coefficients are not imported or derived",
            "parent_signed": "false",
            "source_ids": "SRC3083_16_MICROSCOPE_provenance;SRC3083_18_branch_lock;SRC3083_19_eta_convention",
        }
    ),
    base(
        {
            "theorem_id": "PWD3083_6_verdict",
            "claim_piece": "current MTS derives P_WEP",
            "formal_statement": "P_WEP=0 or P_WEP numeric is available for the current MTS corpus.",
            "proof_move": "all parent-signature clauses or all component-bound rows would have to pass",
            "current_status": "PWEP_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_parent_claim": "conditional theorem is clean but parent signature and component-bound inputs are missing",
            "parent_signed": "false",
            "source_ids": "SRC3083_10_1837_gate;SRC3083_15_1045_claim_gates",
        }
    ),
]

contract_rows = [
    base(
        {
            "operator_id": "PWC3083_0_total",
            "operator": "P_WEP_eta_AB",
            "definition": "linearized map from retained DeltaGamma_WEP components to eta_AB",
            "formula": "eta_AB = g_N^-1 n_mu [(P_A-P_B)^mu_i DeltaGamma_WEP^i]",
            "required_inputs": "species pair; local source normal n_mu; g_N convention; common DeltaGamma units; source/readout branch; component response tensors",
            "zero_condition": "P_A=P_B for all ordinary species or DeltaGamma_WEP=0 by parent theorem",
            "fallback_bound": "absolute-summed component rows below WEP bound; no cancellation",
            "current_status": "CONTRACT_ONLY",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_1_spin",
            "operator": "P_WEP_spin",
            "definition": "spin/hypermomentum response difference between test materials",
            "formula": "eta_spin_AB = g_N^-1 n_mu (P_A^spin-P_B^spin)^mu_i Delta_spin^i",
            "required_inputs": "spin current norm; spin content of materials; torsion/spin response; same branch lock",
            "zero_condition": "spin torsion source is absent or species-universal under parent matter descent",
            "fallback_bound": "source-backed eta_spin_AB row",
            "current_status": "MISSING_SPIN_RESPONSE",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_2_material_source",
            "operator": "P_WEP_material",
            "definition": "composition/source-weight response difference",
            "formula": "eta_material_AB = Delta_w_AB*tau_WEP or direct parent product P_WEP_material·Delta_material",
            "required_inputs": "Delta_w_AB or material tensor; tau_WEP/direct product; source current owner; product convention",
            "zero_condition": "source-label forgetting and single current owner make Delta_w_AB=0",
            "fallback_bound": "finite Delta_w_AB row after tau_WEP or direct product is sourced",
            "current_status": "MISSING_MATERIAL_SOURCE_PRODUCT",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_3_clock_nonmetric",
            "operator": "P_WEP_clock",
            "definition": "clock/rod/nonmetric contribution to differential acceleration readout",
            "formula": "eta_clock_AB = g_N^-1 n_mu (P_A^Qtrace-P_B^Qtrace)^mu_i Delta_clock^i",
            "required_inputs": "clock/rod material response; Q_trace value and units; same coframe/readout proof",
            "zero_condition": "metric-compatible observed coframe and universal clock/rod descent",
            "fallback_bound": "clock/nonmetric WEP component row",
            "current_status": "MISSING_CLOCK_RESPONSE",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_4_projective",
            "operator": "P_WEP_projective",
            "definition": "projective trace leakage into source or test-body response",
            "formula": "eta_projective_AB = g_N^-1 n_mu (P_A^proj-P_B^proj)^mu_i Delta_projective^i",
            "required_inputs": "projective all-sector invariance certificate or trace coupling bound",
            "zero_condition": "all sectors projectively invariant or parent gauge fixes the trace before matter coupling",
            "fallback_bound": "projective leakage row",
            "current_status": "MISSING_PROJECTIVE_CERTIFICATE",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_5_frame_readout",
            "operator": "P_WEP_frame_readout",
            "definition": "single-frame, calibration and source-readout residual entering eta_AB",
            "formula": "eta_frame_AB = P_frame·Delta_frame + P_cal·Delta_cal + P_tau·Delta_tau_n",
            "required_inputs": "single coframe theorem; normal/tau lock; readout kernels; source-measure owner",
            "zero_condition": "one observed coframe and one readout/source branch are parent-signed",
            "fallback_bound": "frame/readout residual row",
            "current_status": "MISSING_SINGLE_FRAME_READOUT_KERNEL",
        }
    ),
    base(
        {
            "operator_id": "PWC3083_6_guard",
            "operator": "no_cancellation_guard",
            "definition": "WEP pass requires each retained component to be zero/bounded, not a tuned total",
            "formula": "abs(eta_total) <= sum_i abs(eta_i); every eta_i must pass or a parent identity must cancel it",
            "required_inputs": "component rows; sourced bound; parent cancellation identity if used",
            "zero_condition": "all component rows are theorem-zero",
            "fallback_bound": "absolute-summed finite vector",
            "current_status": "GUARD_ACTIVE",
        }
    ),
]

component_bound_rows = [
    base(
        {
            "bound_row_id": "WCB3083_0_spin",
            "component": "Delta_spin",
            "target": "eta_spin_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^spin-P_B^spin)^mu_i Delta_spin^i)",
            "accepted_evidence": "parent spin-torsion zero theorem OR numeric spin response with units/source path",
            "current_value": "MISSING_SPIN_RESPONSE_AND_DELTAGAMMA_SPIN",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(SOURCE_PATHS["SRC3083_16_MICROSCOPE_provenance"]),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_row_id": "WCB3083_1_material_source_weight",
            "component": "Delta_material_marker",
            "target": "eta_material_AB",
            "formula": "abs(Delta_w_AB*tau_WEP) or abs(P_WEP_material·Delta_material)",
            "accepted_evidence": "source-label forgetting zero theorem OR numeric Delta_w_AB and tau_WEP/direct product",
            "current_value": "MISSING_DELTA_W_AND_TAU_WEP",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(SOURCE_PATHS["SRC3083_17_tau_wep_schema"]),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_row_id": "WCB3083_2_clock_rods",
            "component": "Delta_clock_rod",
            "target": "eta_clock_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^Qtrace-P_B^Qtrace)^mu_i Delta_clock^i)",
            "accepted_evidence": "clock/rod metric descent theorem OR numeric Q_trace clock/rod response",
            "current_value": "MISSING_CLOCK_ROD_RESPONSE_AND_Q_TRACE",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(SOURCE_PATHS["SRC3083_16_MICROSCOPE_provenance"]),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_row_id": "WCB3083_3_projective_trace",
            "component": "Delta_projective_boundary",
            "target": "eta_projective_AB",
            "formula": "abs(g_N^-1 n_mu (P_A^proj-P_B^proj)^mu_i Delta_projective^i)",
            "accepted_evidence": "all-sector projective invariance theorem OR sourced trace leakage bound",
            "current_value": "MISSING_PROJECTIVE_INVARIANCE_OR_TRACE_BOUND",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(OUTPUTS["component_bounds"]),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_row_id": "WCB3083_4_frame_readout",
            "component": "Delta_frame_Delta_cal_Delta_tau_n",
            "target": "eta_frame_readout_AB",
            "formula": "abs(P_frame·Delta_frame + P_cal·Delta_cal + P_tau·Delta_tau_n)",
            "accepted_evidence": "single observed coframe/source/readout theorem OR numeric frame/readout residuals",
            "current_value": "MISSING_SINGLE_FRAME_THEOREM_OR_NUMERIC_FRAME_RESIDUAL",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(SOURCE_PATHS["SRC3083_21_single_coframe"]),
            "status": "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_row_id": "WCB3083_5_total_guard",
            "component": "WEP_component_vector",
            "target": "eta_total_guard",
            "formula": "sum_i abs(eta_i) <= eta_bound unless parent identity proves exact cancellation",
            "accepted_evidence": "all WCB3083 component rows pass or theorem-zero vector identity is parent-signed",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless",
            "comparison_bound": "MICROSCOPE_or_equivalent_WEP_bound_anchor_nonclaim",
            "source_path": str(SOURCE_PATHS["SRC3083_18_branch_lock"]),
            "status": "TOTAL_SCORE_REFUSED",
        }
    ),
]

corpus_gate_rows = [
    base(
        {
            "gate_id": "CG3083_0_conditional_theorem",
            "claim": "conditional universal matter descent implies P_WEP=0",
            "gate_pass": "true",
            "reason": "the chain-rule/geodesic common-mode theorem is mathematically exact under its premises",
            "claim_allowed": "false",
        }
    ),
    base(
        {
            "gate_id": "CG3083_1_parent_matter_functor",
            "claim": "current corpus parent-signs the ordinary matter functor",
            "gate_pass": "false",
            "reason": "1045 keeps the parent matter category/descent open",
            "claim_allowed": "false",
        }
    ),
    base(
        {
            "gate_id": "CG3083_2_same_observed_geometry",
            "claim": "force, clocks, rods and readout use the same observed coframe/metric branch",
            "gate_pass": "false",
            "reason": "single coframe/source/readout theorem is not signed as one parent action object",
            "claim_allowed": "false",
        }
    ),
    base(
        {
            "gate_id": "CG3083_3_no_source_only_species_selector",
            "claim": "current corpus forbids source-only species weights and marker constants",
            "gate_pass": "false",
            "reason": "no-shadow-frame/no-marker and source-current owner clauses remain unsigned",
            "claim_allowed": "false",
        }
    ),
    base(
        {
            "gate_id": "CG3083_4_component_bound_rows",
            "claim": "current corpus has score-ready WEP component-bound rows",
            "gate_pass": "false",
            "reason": "component values, response tensors, tau_WEP/direct product and official kernels are missing",
            "claim_allowed": "false",
        }
    ),
    base(
        {
            "gate_id": "CG3083_5_current_PWEP",
            "claim": "current corpus derives or numerically sources P_WEP",
            "gate_pass": "false",
            "reason": "P_WEP remains a contract/ledger object; no WEP/local-GR claim follows",
            "claim_allowed": "false",
        }
    ),
]

dependency_rows = [
    base(
        {
            "dependency_id": "DEP3083_0_q_kernel",
            "parent_clause": "q_loc: Phi_parent -> Q_loc and v_X in ker(Dq_loc)",
            "effect_on_PWEP": "lets observed geometry be insensitive to vertical representative motion",
            "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "if_closed": "feeds P_WEP common-mode theorem",
            "if_open": "Delta_material/frame components remain live",
        }
    ),
    base(
        {
            "dependency_id": "DEP3083_1_observed_coframe",
            "parent_clause": "e_obs=Obs_e(q_loc(Phi)); g_obs and connection are owned by the same branch",
            "effect_on_PWEP": "kills visible-geometry differential acceleration from DeltaGamma if matter sees only e_obs",
            "current_status": "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "if_closed": "P_WEP geometry part can be zero",
            "if_open": "frame/readout WEP row stays mandatory",
        }
    ),
    base(
        {
            "dependency_id": "DEP3083_2_matter_category",
            "parent_clause": "ordinary matter bundles and lifts are fixed/gauge-owned over observed geometry",
            "effect_on_PWEP": "prevents physical material changes from being hidden as vertical gauge motion",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "if_closed": "species acceleration is a common geodesic response",
            "if_open": "spin/material WEP rows stay mandatory",
        }
    ),
    base(
        {
            "dependency_id": "DEP3083_3_no_shadow_marker",
            "parent_clause": "no hidden conformal/disformal frame, mass, EM, clock, or material-marker X dependence",
            "effect_on_PWEP": "forbids universal/non-universal fifth-force and WEP marker countermodels",
            "current_status": "GUARD_WRITTEN_NOT_PARENT_DERIVED",
            "if_closed": "qbar_marker and source-label WEP channels narrow sharply",
            "if_open": "marker/constants coefficients must be sourced",
        }
    ),
    base(
        {
            "dependency_id": "DEP3083_4_readout_product",
            "parent_clause": "branch lock, eta convention, tau_WEP/direct product and source/readout kernels",
            "effect_on_PWEP": "turns a theorem or component vector into a comparable eta_AB row",
            "current_status": "BOUND_ANCHOR_EXISTS_PREDICTION_SIDE_MISSING",
            "if_closed": "WEP bound comparator can run",
            "if_open": "MICROSCOPE anchor cannot certify an MTS prediction",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3083_0_parent_signature",
            "blocks": "P_WEP=0 claim",
            "missing": "one parent action signature for ordinary matter, observed coframe, constants, no-shadow frame and readout",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3083_1_response_tensors",
            "blocks": "numeric P_WEP vector",
            "missing": "P_A-P_B response tensors for spin, material, clock, projective and frame/readout channels",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3083_2_component_values",
            "blocks": "WEP score",
            "missing": "DeltaGamma component values or parent zero theorems",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3083_3_no_cancellation_guard",
            "blocks": "combined eta_AB pass",
            "missing": "individual component pass or parent cancellation identity",
            "status": "GUARD_ACTIVE",
            "score_allowed": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3083_0_conditional_success",
            "decision": "PWEP_ZERO_THEOREM_SHAPE_IS_EXACT_CONDITIONAL",
            "reason": "universal observed-matter descent would make WEP common-mode and force P_WEP=0",
            "next_action": "try to parent-sign the ordinary matter action signature and source-label forgetting",
        }
    ),
    base(
        {
            "decision_id": "DEC3083_1_current_refusal",
            "decision": "PWEP_NOT_CLAIMED_FOR_CURRENT_MTS",
            "reason": "matter functor, single observed frame, no source-only selector/no-shadow marker, and readout/product kernels remain unsigned or missing",
            "next_action": "keep WEP rows nonclaim and do not promote local GR",
        }
    ),
    base(
        {
            "decision_id": "DEC3083_2_best_next",
            "decision": "ORDINARY_MATTER_ACTION_SIGNATURE_SOURCE_LABEL_FORGETTING_NEXT",
            "reason": "the least-cheatable route is to prove the ordinary matter category has one observed coframe, one measure/current owner and no source-label scalar",
            "next_action": "3084-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3083_0_conditional_theorem",
            "claim": "universal observed matter descent would imply P_WEP=0",
            "claim_active": "false",
            "status": "CONDITIONAL_THEOREM_ONLY_NOT_CURRENT_MTS_CLAIM",
            "reason": "the theorem is exact but its parent premises are unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3083_1_current_PWEP",
            "claim": "current MTS has P_WEP=0 or numeric P_WEP",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "parent signature and component-bound inputs are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3083_2_WEP_pass",
            "claim": "WEP test passes",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "component vector is nonclaim and bound comparison cannot run",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3083_3_local_GR",
            "claim": "local GR/Newton recovery follows from WEP branch",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "WEP is one harsh coupling channel, not the full DeltaGamma/DeltaK/P4 closure",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3083_0_3084",
            "next_checkpoint": "3084-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_ordinary_matter_action_signature_source_label_forgetting_or_WEP_bound_first_fill_under_AX1090_3084.py",
            "mission": "try to parent-sign ordinary matter action descent: one observed coframe, one measure/current owner, no source-only species labels, and no shadow-frame marker dependence; otherwise fill the first WEP component-bound input row",
            "starting_equation": "S_A = Sbar_A[Psi_A,e_obs(q_loc(Phi)),omega[e_obs],theta_A] with Lie_v theta_A=0 and no A_A(X),B_A(X),w_A source-only labels",
            "claim_policy": "no WEP or local-GR claim until the signature is parent-signed or all WEP component-bound rows are source-backed and pass with no-cancellation guard",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["derivation"], derivation_rows)
write_csv(OUTPUTS["contract"], contract_rows)
write_csv(OUTPUTS["component_bounds"], component_bound_rows)
write_csv(OUTPUTS["corpus_gate"], corpus_gate_rows)
write_csv(OUTPUTS["dependency_ladder"], dependency_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"])
copy_csv(OUTPUTS["component_bounds"], BRANCH_OUTPUTS["component_bounds_copy"])
copy_csv(OUTPUTS["corpus_gate"], BRANCH_OUTPUTS["corpus_gate_copy"])
copy_csv(OUTPUTS["dependency_ladder"], BRANCH_OUTPUTS["dependency_ladder_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3083_0_contract", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"]),
        ("BR3083_1_component_bounds", OUTPUTS["component_bounds"], BRANCH_OUTPUTS["component_bounds_copy"]),
        ("BR3083_2_corpus_gate", OUTPUTS["corpus_gate"], BRANCH_OUTPUTS["corpus_gate_copy"]),
        ("BR3083_3_dependency_ladder", OUTPUTS["dependency_ladder"], BRANCH_OUTPUTS["dependency_ladder_copy"]),
        ("BR3083_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3083 - P_WEP Response Operator\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + derivation_rows
    + contract_rows
    + component_bound_rows
    + corpus_gate_rows
    + dependency_rows
    + score_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_derivation_ids = {
    "PWD3083_0_target",
    "PWD3083_1_conditional_zero_theorem",
    "PWD3083_2_response_decomposition",
    "PWD3083_3_no_source_only_scalar",
    "PWD3083_4_same_geometry_stack",
    "PWD3083_5_bound_comparison",
    "PWD3083_6_verdict",
}
required_contract_ids = {
    "PWC3083_0_total",
    "PWC3083_1_spin",
    "PWC3083_2_material_source",
    "PWC3083_3_clock_nonmetric",
    "PWC3083_4_projective",
    "PWC3083_5_frame_readout",
    "PWC3083_6_guard",
}
required_bound_ids = {
    "WCB3083_0_spin",
    "WCB3083_1_material_source_weight",
    "WCB3083_2_clock_rods",
    "WCB3083_3_projective_trace",
    "WCB3083_4_frame_readout",
    "WCB3083_5_total_guard",
}
required_gate_ids = {
    "CG3083_0_conditional_theorem",
    "CG3083_1_parent_matter_functor",
    "CG3083_2_same_observed_geometry",
    "CG3083_3_no_source_only_species_selector",
    "CG3083_4_component_bound_rows",
    "CG3083_5_current_PWEP",
}

current_pwep_gate = next(row for row in corpus_gate_rows if row["gate_id"] == "CG3083_5_current_PWEP")
conditional_row = next(row for row in derivation_rows if row["theorem_id"] == "PWD3083_1_conditional_zero_theorem")
validation_rows = [
    base(
        {
            "validation_id": "VAL3083_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3083_03_derivation_rows_present",
            "passed": str(required_derivation_ids.issubset({row["theorem_id"] for row in derivation_rows})),
            "requirement": "P_WEP target, conditional theorem, decomposition, source-label silence, geometry stack, bound comparison and verdict are present",
            "evidence": OUTPUTS["derivation"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_04_conditional_theorem_not_claim",
            "passed": str(
                conditional_row["current_status"] == "EXACT_CONDITIONAL_THEOREM"
                and conditional_row["parent_signed"] == "false"
                and conditional_row["valid_for_claim"] == "false"
            ),
            "requirement": "conditional P_WEP=0 theorem is written but not promoted as a current MTS claim",
            "evidence": OUTPUTS["derivation"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_05_contract_complete_nonclaim",
            "passed": str(required_contract_ids.issubset({row["operator_id"] for row in contract_rows}) and not has_claim_true(contract_rows)),
            "requirement": "P_WEP response contract covers total, spin, material, clock, projective, frame/readout and no-cancellation guard as nonclaim rows",
            "evidence": OUTPUTS["contract"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_06_component_bounds_nonclaim",
            "passed": str(required_bound_ids.issubset({row["bound_row_id"] for row in component_bound_rows}) and not has_claim_true(component_bound_rows)),
            "requirement": "WEP component-bound fallback rows are staged and invalid for claim",
            "evidence": OUTPUTS["component_bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_07_gates_refuse_current_PWEP",
            "passed": str(required_gate_ids.issubset({row["gate_id"] for row in corpus_gate_rows}) and current_pwep_gate["gate_pass"] == "false" and not has_claim_true(corpus_gate_rows)),
            "requirement": "current corpus gate refuses P_WEP while allowing only the conditional theorem shape",
            "evidence": OUTPUTS["corpus_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_08_dependency_ladder_present",
            "passed": str(len(dependency_rows) == 5 and not has_claim_true(dependency_rows)),
            "requirement": "parent signature dependency ladder records q-kernel, coframe, matter category, no-shadow marker and readout/product clauses",
            "evidence": OUTPUTS["dependency_ladder"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_09_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] in {"BLOCKS_SCORE", "GUARD_ACTIVE"} for row in score_blocker_rows)),
            "requirement": "parent signature, response tensor, component value and no-cancellation blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_10_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no WEP, P_WEP=0, local-GR or Newton claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3083_11_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3084-Y5-R2FR-ordinary-matter-action-signature")),
            "requirement": "next target moves to ordinary matter action signature and source-label forgetting",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_12_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3083_13_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3083_14_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3083_15_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3083 outputs remains zero",
            "evidence": f"formalization_3083_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3083_16_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3083_17_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3083 - P_WEP Response Operator from Matter Functor or Component Bound

Status: `Y5_R2FR_3083_PWEP_conditional_theorem_current_claim_refused`

Generated: `{RUN_UTC}`

## Verdict

3083 gets the WEP coupling problem into its sharpest current form.

The good news: the theorem shape is clean. If ordinary matter really descends through one observed coframe/metric branch, with quotient-owned constants, one current/measure owner, no source-only species labels, and no hidden conformal/disformal/marker frame, then the WEP response is common-mode and `P_WEP = 0`.

The hard news: the current corpus still does **not** parent-sign those premises as one action object. Therefore this checkpoint does not claim `P_WEP=0`, does not claim a WEP pass, and does not promote local GR/Newton recovery.

The next best target is not another broad local-GR sweep. It is the ordinary-matter action signature itself: one observed coframe, one measure/current owner, source-label forgetting, and no shadow-frame marker dependence.

## P_WEP Derivation Attempt

{md_table(derivation_rows, ["theorem_id", "claim_piece", "current_status", "missing_for_parent_claim", "parent_signed"])}

## P_WEP Response Contract

{md_table(contract_rows, ["operator_id", "operator", "definition", "formula", "current_status"])}

## WEP Component-Bound Fallback

{md_table(component_bound_rows, ["bound_row_id", "component", "target", "current_value", "status"])}

## Current Corpus Gate

{md_table(corpus_gate_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"])}

## Parent Signature Dependency Ladder

{md_table(dependency_rows, ["dependency_id", "parent_clause", "effect_on_PWEP", "current_status"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Derivation attempt: `{OUTPUTS["derivation"]}`
- Response contract: `{OUTPUTS["contract"]}`
- Component-bound fallback: `{OUTPUTS["component_bounds"]}`
- Current corpus gate: `{OUTPUTS["corpus_gate"]}`
- Dependency ladder: `{OUTPUTS["dependency_ladder"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["contract_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["component_bounds_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["corpus_gate_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["dependency_ladder_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
