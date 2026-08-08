from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4006"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4006-Y5-R2FR-minimal-coframe-cell-parent-action-insertion-or-finite-RAB-coefficients.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

FINITE_B_RAB_BOUND = 6.102178699076298e-11

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4006_SOURCE_REGISTER.csv",
    "packet": SRC / "P8_Y5_R2FR_4006_PARENT_INSERTION_PACKET.csv",
    "variation": SRC / "P8_Y5_R2FR_4006_VARIATION_CHAIN.csv",
    "stress_gate": SRC / "P8_Y5_R2FR_4006_STRESS_CURRENT_GATE.csv",
    "finite_rows": SRC / "P8_Y5_R2FR_4006_FINITE_COEFFICIENT_ACQUISITION_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4006_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4006_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4006_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4006_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4006_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4006_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4006_VALIDATION.csv",
}

NEXT_DOC = "4007-Y5-R2FR-cell-lock-matter-readout-descent-or-JR-bound-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4007_cell_lock_matter_readout_descent_or_JR_bound_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4006_00_handoff", SRC / "P8_Y5_R2FR_4005_NEXT_TARGET.csv", "NEXT4005_0", "4005 handoff"),
        ("SRC4006_01_cell_identity", SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv", "AN4005_0_cell_two_form_identity", "cell identity"),
        ("SRC4006_02_subdomain_charge", SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv", "AN4005_1_all_subdomain_cell_charge", "all-subdomain route"),
        ("SRC4006_03_minimal_language", SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv", "AN4005_3_minimal_object_language_exclusion", "minimal object language"),
        ("SRC4006_04_finite_budget", SRC / "P8_Y5_R2FR_4005_FIRST_REAL_IX_SOURCE_COEFFICIENT_ROWS.csv", "IXCOEF4005_0_B_RAB_budget", "finite budget"),
        ("SRC4006_05_action_candidate", SRC / "P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv", "CCA3853_0_two_form_cell_lock", "coframe action candidate"),
        ("SRC4006_06_scalar_reduction", SRC / "P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv", "CCA3853_1_scalar_reduction", "scalar lambda_R reduction"),
        ("SRC4006_07_cell_lock_status", SRC / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv", "CLT3854_1_topological_conditional", "cell lock theorem"),
        ("SRC4006_08_no_gauge", SRC / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv", "CLT3854_0_gauge_verdict", "gauge route rejection"),
        ("SRC4006_09_linear_multiplier", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_4_linear_multiplier", "linear multiplier mechanism"),
        ("SRC4006_10_unimodular", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_5_unimodular_radial_cell", "unimodular route"),
        ("SRC4006_11_elambda", SRC / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv", "ELIM2236_0_E_Lambda", "E_Lambda variation"),
        ("SRC4006_12_er", SRC / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv", "ELIM2236_1_E_R", "E_R variation"),
        ("SRC4006_13_lambda_zero", SRC / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv", "ELIM2236_2_Lambda_zero", "Lambda zero"),
        ("SRC4006_14_no_symp", SRC / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv", "ELIM2236_3_no_symplectic_hair", "no symplectic hair"),
        ("SRC4006_15_no_deriv", SRC / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv", "GRAM2236_0_no_DRAB", "no derivative grammar"),
        ("SRC4006_16_no_boundary_deriv", SRC / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv", "GRAM2236_3_no_boundary_derivative", "no boundary derivative"),
        ("SRC4006_17_fallback", SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv", "FALL2236_2_JR", "finite J_R fallback"),
        ("SRC4006_18_parent_policy", SRC / "P8_Y5_R2FR_3881_PARENT_ACTION_INSERTION_CONTRACT.csv", "PAC3881_10_claim_policy", "parent insertion policy"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def insertion_packet_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": "PIP4006_0_fields",
            "requirement": "coframe-cell field content",
            "exact_condition": "parent branch declares theta^0, theta^1, Omega_tr=(theta^0/c) wedge theta^1, Omega_ref=dt wedge dr, and Lambda_J/lambda_R before local readout",
            "variation_role": "defines the reciprocal cell mode R_AB=ln(T^2S)",
            "status": "INSERTION_PACKET_READY_NOT_ADOPTED",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_1_action",
            "requirement": "minimal cell-lock action",
            "exact_condition": "S_cell=int_U Lambda_J (Omega_tr-Omega_ref), with scalar reduction int dr lambda_J ln(T sqrt(S))=(1/2)int dr lambda_R R_AB",
            "variation_role": "delta_Lambda enforces the cell lock",
            "status": "EXACT_CANDIDATE_ACTION",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_2_no_derivative_language",
            "requirement": "auxiliary no-derivative object language",
            "exact_condition": "no D_mu R_AB, no D_mu Lambda_R, no vertical metric/connection, and no derivative boundary/corner term",
            "variation_role": "makes Theta_cell=0 and removes Pi_R^n/Q_R hair unless boundary/source terms are added separately",
            "status": "REQUIRED_FOR_AUXILIARY_CLAIM",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_3_matter_readout",
            "requirement": "matter and readout descent",
            "exact_condition": "delta_R(S_matter+B_readout+S_eff)=0 on the protected local branch",
            "variation_role": "lets E_R set Lambda_R=0 rather than finite source charge",
            "status": "NEXT_HARD_GATE",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_4_boundary",
            "requirement": "boundary no-hair",
            "exact_condition": "no B_R[R_AB,D R_AB], no Pi_R^n, or a parent-fixed proper/topological boundary representative",
            "variation_role": "prevents reciprocal boundary charge from surviving after bulk elimination",
            "status": "REQUIRED_UNSIGNED",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_5_stress",
            "requirement": "cell-block stress silence",
            "exact_condition": "cell-block metric/coframe stress is proportional to Lambda_R plus explicit source/boundary defects; with Lambda_R=0 and defects zero it is silent",
            "variation_role": "prevents I_X=0 from hiding a C_tau_bulk or PPN stress residual",
            "status": "DERIVED_CONDITIONAL_STRESS_GUARD",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "packet_id": "PIP4006_6_claim_policy",
            "requirement": "no adoption by script",
            "exact_condition": "this checkpoint writes an insertion packet; it does not silently rewrite the public parent action",
            "variation_role": "keeps theorem route private/nonclaim until intentionally adopted",
            "status": "BLOCKING_FOR_CLAIM",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def variation_chain_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "variation_id": "VAR4006_0_delta_Lambda",
            "varied_object": "Lambda_J or lambda_R",
            "calculation": "delta_Lambda S_cell=0 gives Omega_tr=Omega_ref; scalar reduction gives R_AB=ln(T^2S)=0",
            "closes": "cell_lock;R_AB_zero",
            "status": "EXACT_IF_INSERTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "variation_id": "VAR4006_1_delta_R_or_cell_density",
            "varied_object": "R_AB/u_cell or equivalent cell-density variable",
            "calculation": "delta_R S_total gives lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0",
            "closes": "lambda_R_zero only if J_R=boundary=readout_regen=0",
            "status": "EXACT_CONDITIONAL_SOURCE_SILENCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "variation_id": "VAR4006_2_delta_coframe_metric",
            "varied_object": "theta^0,theta^1 or g_obs",
            "calculation": "delta_e S_cell is proportional to Lambda_J times delta Omega_tr plus explicit defects; after E_R sets Lambda_J=0 and defects vanish, T_cell^{mu nu}=0/proper",
            "closes": "stress_guard;C_tau_bulk_cell",
            "status": "DERIVED_CONDITIONAL_STRESS_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "variation_id": "VAR4006_3_delta_boundary",
            "varied_object": "boundary/corner representative",
            "calculation": "if no derivative boundary term is allowed, Pi_R^n=0; otherwise B_R/Pi_R^n enters the finite hair row",
            "closes": "boundary_nohair_or_finite_BR",
            "status": "EXACT_FORK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "variation_id": "VAR4006_4_symplectic_potential",
            "varied_object": "cell block derivatives",
            "calculation": "because S_cell contains no D_mu R_AB or D_mu Lambda_R, Theta_cell^mu=0 and Q_tau^cell is zero/proper unless a boundary improvement is inserted",
            "closes": "I_X_symplectic_zero",
            "status": "EXACT_IF_NO_DERIVATIVE_LANGUAGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "variation_id": "VAR4006_5_derivative_counterbranch",
            "varied_object": "allowed kinetic/elastic R_AB term",
            "calculation": "if Z_R |D R_AB|^2 is legal then Theta_R^mu=-Z_R nabla^mu R_AB delta R_AB and the finite coefficient branch is mandatory",
            "closes": "no_zero_claim",
            "status": "FINITE_BRANCH_IF_LANGUAGE_GATE_FAILS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def stress_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SCG4006_0_master",
            "quantity": "Delta_cell_stress_current",
            "formula": "|Lambda_R| + |J_R| + |B_R/Pi_R^n| + |readout_regen| + |Z_R derivative escape|",
            "zero_condition": "all terms vanish by E_R source silence, boundary nohair, readout descent, and no-derivative grammar",
            "current_status": "CONDITIONAL_ZERO_NOT_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SCG4006_1_lambda",
            "quantity": "Lambda_R",
            "formula": "Lambda_R=-(J_R+delta B_R/delta R_AB+readout_regen)",
            "zero_condition": "J_R=0, boundary derivative=0, readout_regen=0",
            "current_status": "NEXT_GATE_DEPENDS_ON_MATTER_READOUT_DESCENT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SCG4006_2_symplectic",
            "quantity": "Theta_cell/Q_tau_cell",
            "formula": "Theta_cell=0 and Q_tau_cell=0/proper if no derivatives and no boundary improvement",
            "zero_condition": "minimal object language plus boundary nohair",
            "current_status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "SCG4006_3_finite_bound",
            "quantity": "B_RAB",
            "formula": f"B_RAB <= {FINITE_B_RAB_BOUND:.16e}",
            "zero_condition": "not a zero condition; finite fallback bound target",
            "current_status": "BOUND_TARGET_SOURCE_BACKED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FR4006_0_B_RAB",
            "coefficient": "B_RAB",
            "value": FINITE_B_RAB_BOUND,
            "units": "dimensionless_gamma_like_budget",
            "needed_if": "cell lock/stress guards are not parent-signed",
            "source_status": "BOUND_TARGET_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FR4006_1_J_R",
            "coefficient": "J_R",
            "value": "MISSING_MATTER_READOUT_DESCENT_ZERO_OR_NUMERIC_SOURCE",
            "units": "source_charge_density_units",
            "needed_if": "E_R source silence is not proved",
            "source_status": "NEXT_DERIVATION_OR_BOUND_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FR4006_2_B_R",
            "coefficient": "B_R/Pi_R^n",
            "value": "MISSING_BOUNDARY_NOHAIR_OR_NUMERIC_FLUX",
            "units": "boundary_charge_or_momentum_units",
            "needed_if": "boundary nohair is not proved",
            "source_status": "MISSING_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FR4006_3_Z_R",
            "coefficient": "Z_R",
            "value": "MISSING_ZERO_THEOREM_OR_SOURCE_BACKED_VALUE",
            "units": "parent kinetic units",
            "needed_if": "no-derivative object language fails",
            "source_status": "MISSING_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FR4006_4_projection",
            "coefficient": "arena projection",
            "value": "MISSING_GAMMA_BETA_R10_CLOCK_ORBIT_KERNEL",
            "units": "arena_dependent",
            "needed_if": "any finite coefficient survives",
            "source_status": "MISSING_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4006_0_full_insertion_signed",
            "description": "cell action inserted with matter/readout descent, boundary nohair, no derivatives and stress guard",
            "inserted": True,
            "matter_descent": True,
            "boundary_nohair": True,
            "no_derivative": True,
            "stress_guard": True,
            "finite_rows_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4006_1_inserted_source_open",
            "description": "cell action inserted but matter/readout source term is open",
            "inserted": True,
            "matter_descent": False,
            "boundary_nohair": True,
            "no_derivative": True,
            "stress_guard": False,
            "finite_rows_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4006_2_inserted_boundary_open",
            "description": "cell action inserted but boundary/corner reciprocal hair remains possible",
            "inserted": True,
            "matter_descent": True,
            "boundary_nohair": False,
            "no_derivative": True,
            "stress_guard": False,
            "finite_rows_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4006_3_derivative_language_allowed",
            "description": "vertical metric/derivative language is legal",
            "inserted": True,
            "matter_descent": True,
            "boundary_nohair": True,
            "no_derivative": False,
            "stress_guard": False,
            "finite_rows_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4006_4_finite_coefficients_complete",
            "description": "finite branch has real coefficient rows and projections",
            "inserted": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "no_derivative": False,
            "stress_guard": False,
            "finite_rows_complete": True,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4006_5_missing_schema",
            "description": "schema/source paths are missing",
            "inserted": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "no_derivative": False,
            "stress_guard": False,
            "finite_rows_complete": False,
            "schema_complete": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in cases:
        if not bool(case["schema_complete"]):
            status = "BLOCKED_MISSING_SCHEMA"
            theorem_status = "MISSING"
            next_action = "repair source/schema rows"
        elif all(bool(case[key]) for key in ["inserted", "matter_descent", "boundary_nohair", "no_derivative", "stress_guard"]):
            status = "CONDITIONAL_CELL_BLOCK_SILENT"
            theorem_status = "R_AB=0;Lambda_R=0;Theta_cell=0;T_cell=0_conditionally"
            next_action = "carry to projector/Dq/EM/source normalization gates"
        elif bool(case["finite_rows_complete"]):
            status = "FINITE_BRANCH_READY_NONCLAIM"
            theorem_status = "finite_coefficients_available"
            next_action = "score against local arenas without local-GR claim"
        elif bool(case["inserted"]) and not bool(case["matter_descent"]):
            status = "J_R_SOURCE_OPEN"
            theorem_status = "Lambda_R_not_zero_until_JR_closed"
            next_action = "prove matter/readout descent or fill J_R"
        elif bool(case["inserted"]) and not bool(case["boundary_nohair"]):
            status = "BOUNDARY_HAIR_OPEN"
            theorem_status = "B_R/Pi_R_required"
            next_action = "prove boundary nohair or fill boundary flux"
        elif bool(case["inserted"]) and not bool(case["no_derivative"]):
            status = "DERIVATIVE_ESCAPE_OPEN"
            theorem_status = "Z_R_required"
            next_action = "prove no vertical metric or fill Z_R/M_R2"
        else:
            status = "INSERTION_NOT_ADOPTED"
            theorem_status = f"finite_budget_target={FINITE_B_RAB_BOUND:.16e}"
            next_action = "adopt packet intentionally or acquire finite coefficients"
        results.append(
            {
                "case_id": case["case_id"],
                "input_status": status,
                "cell_block_status": theorem_status,
                "claim_allowed": False,
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return results


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DG4006_0_insertion_result",
            "question": "Does the inserted coframe-cell block mathematically close I_X?",
            "answer": "Conditionally",
            "reason": "The variation chain closes R_AB, Lambda_R, Theta_cell and stress only if matter/readout descent, boundary nohair and no-derivative grammar are all signed.",
            "action": "do not claim; use packet as parent insertion target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4006_1_next_gate",
            "question": "Which guard should be attacked next?",
            "answer": "matter/readout descent J_R=0",
            "reason": "E_R gives Lambda_R=-(J_R+B_R+readout_regen); without J_R=0 the cell block can carry stress even when R_AB=0.",
            "action": f"write {NEXT_DOC}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4006_2_finite_fallback",
            "question": "What if the guard fails?",
            "answer": "fill J_R first",
            "reason": "J_R is the first coefficient that directly blocks Lambda_R=0 and stress silence.",
            "action": "make J_R the next finite/nonclaim source row if no descent theorem closes",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CG4006_0_parent_adoption", "parent action adopted", False, "packet written but not adopted"),
        ("CG4006_1_I_X_zero", "I_X zero", False, "matter/readout, boundary and no-derivative guards not all signed"),
        ("CG4006_2_cell_stress_zero", "cell stress zero", False, "Lambda_R zero depends on J_R/B_R/readout silence"),
        ("CG4006_3_local_GR", "local GR/Newton promotion", False, "other 4003 current-chain gates remain open"),
        ("CG4006_4_finite_pass", "finite branch pass", False, "finite coefficients/projections missing"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4006_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove matter/readout descent J_R=0 for the cell-lock sector, or create the first source-backed finite J_R bound row",
            "success_condition": "delta_R(S_matter+B_readout+S_eff)=0 is parent-signed for the protected local branch, giving Lambda_R=0 once boundary/readout defects vanish; otherwise J_R gets units, source path, arena map and valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "coframe-cell parent insertion packet and variation chain written; R_AB/Lambda/stress/I_X close conditionally, with J_R matter-readout descent selected as next hard gate",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4006 - Minimal Coframe-Cell Parent Action Insertion Or Finite RAB Coefficients",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The proposed parent block passes the internal variation sanity check conditionally.",
        "",
        "`S_cell = int_U Lambda_J (Omega_tr - Omega_ref)`",
        "",
        "with scalar reduction",
        "",
        "`S_cell -> int dr lambda_J ln(T sqrt(S)) = (1/2) int dr lambda_R R_AB`.",
        "",
        "## Variation Chain",
        "",
        "- `delta_Lambda`: gives `Omega_tr=Omega_ref`, hence `T sqrt(S)=1`, hence `R_AB=0`.",
        "- `delta_R`: gives `lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0`.",
        "- `delta_e`: cell stress is proportional to `lambda_R` plus explicit source/boundary/readout defects.",
        "- no derivatives: `Theta_cell=0`, `Q_tau_cell=0/proper`, so the symplectic part of `I_X` is zero.",
        "",
        "So the block is not obviously poison. The catch is exact and useful: `lambda_R=0` needs `J_R=0`, boundary nohair, and readout descent.",
        "",
        "## No Claim",
        "",
        "This checkpoint writes an insertion packet. It does not silently adopt the packet into the final parent action, and it does not claim local GR.",
        "",
        "## Finite Fallback",
        "",
        f"If any guard fails, the finite branch remains constrained by `B_RAB <= {FINITE_B_RAB_BOUND:.16e}`, with first hard coefficient `J_R` because it directly prevents `lambda_R=0`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: `{row['input_status']}`, cell=`{row['cell_block_status']}`, claim={row['claim_allowed']}, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a forward step: the coframe-cell block has a coherent conditional variation chain. The next real bottleneck is not the multiplier; it is proving `J_R=0` for ordinary matter/readout or paying it as a finite coefficient.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4006 - Coframe-Cell Parent Insertion"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: insertion packet `S_cell=int_U Lambda_J(Omega_tr-Omega_ref)` has a coherent conditional variation chain.
- Variations: `delta_Lambda` gives `R_AB=0`; `delta_R` gives `lambda_R+J_R+delta B_R/delta R_AB+readout_regen=0`; coframe stress is silent only after `lambda_R=0` and defects vanish.
- Symplectic result: no-derivative grammar gives `Theta_cell=Q_tau_cell=0/proper`, so the symplectic piece of `I_X` closes conditionally.
- No claim: packet is not adopted in final parent action; local-GR/Newton remains blocked.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    packet: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4006_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4006_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4006_02_packet_action", any(row["packet_id"] == "PIP4006_1_action" for row in packet), "cell action packet present")
    add("VAL4006_03_packet_no_deriv", any(row["packet_id"] == "PIP4006_2_no_derivative_language" for row in packet), "no-derivative packet present")
    add("VAL4006_04_packet_matter", any(row["packet_id"] == "PIP4006_3_matter_readout" for row in packet), "matter/readout gate present")
    add("VAL4006_05_packet_stress", any(row["packet_id"] == "PIP4006_5_stress" for row in packet), "stress guard present")
    add("VAL4006_06_not_adopted", all(str(row["adopted_in_parent_action"]).lower() == "false" for row in packet), "packet not silently adopted")
    add("VAL4006_07_delta_lambda", any(row["variation_id"] == "VAR4006_0_delta_Lambda" for row in variation), "delta Lambda variation present")
    add("VAL4006_08_delta_R", any(row["variation_id"] == "VAR4006_1_delta_R_or_cell_density" for row in variation), "delta R variation present")
    add("VAL4006_09_delta_stress", any(row["variation_id"] == "VAR4006_2_delta_coframe_metric" for row in variation), "coframe stress variation present")
    add("VAL4006_10_symplectic", any(row["variation_id"] == "VAR4006_4_symplectic_potential" for row in variation), "symplectic zero variation present")
    add("VAL4006_11_stress_master", any(row["gate_id"] == "SCG4006_0_master" for row in stress), "stress master gate present")
    add("VAL4006_12_lambda_gate", any(row["gate_id"] == "SCG4006_1_lambda" for row in stress), "lambda stress gate present")
    b_row = next(row for row in finite if row["row_id"] == "FR4006_0_B_RAB")
    add("VAL4006_13_budget", float(b_row["value"]) > 0.0 and b_row["source_status"] == "BOUND_TARGET_ONLY", "B_RAB budget target present")
    add("VAL4006_14_JR_next", any(row["row_id"] == "FR4006_1_J_R" and "NEXT" in row["source_status"] for row in finite), "J_R selected as next coefficient")
    zero = next(row for row in results if row["case_id"] == "CASE4006_0_full_insertion_signed")
    jr = next(row for row in results if row["case_id"] == "CASE4006_1_inserted_source_open")
    boundary = next(row for row in results if row["case_id"] == "CASE4006_2_inserted_boundary_open")
    derivative = next(row for row in results if row["case_id"] == "CASE4006_3_derivative_language_allowed")
    finite_case = next(row for row in results if row["case_id"] == "CASE4006_4_finite_coefficients_complete")
    missing = next(row for row in results if row["case_id"] == "CASE4006_5_missing_schema")
    add("VAL4006_15_zero_case", zero["input_status"] == "CONDITIONAL_CELL_BLOCK_SILENT", "full insertion case closes conditionally")
    add("VAL4006_16_JR_case", jr["input_status"] == "J_R_SOURCE_OPEN", "J_R-open case routed correctly")
    add("VAL4006_17_boundary_case", boundary["input_status"] == "BOUNDARY_HAIR_OPEN", "boundary-open case routed correctly")
    add("VAL4006_18_derivative_case", derivative["input_status"] == "DERIVATIVE_ESCAPE_OPEN", "derivative escape case routed correctly")
    add("VAL4006_19_finite_case", finite_case["input_status"] == "FINITE_BRANCH_READY_NONCLAIM" and str(finite_case["claim_allowed"]).lower() == "false", "finite case remains nonclaim")
    add("VAL4006_20_missing_blocks", missing["cell_block_status"] == "MISSING", "missing schema blocks")
    add("VAL4006_21_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4006_22_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4006_23_doc_exists", DOC_PATH.exists() and "Variation Chain" in read_text(DOC_PATH), "document written")
    add("VAL4006_24_spine_updated", SPINE_PATH.exists() and "## 4006 - Coframe-Cell Parent Insertion" in read_text(SPINE_PATH), "spine updated")
    add("VAL4006_25_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4006_26_compile", compile_ok, "script compiles")
    add("VAL4006_27_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [sources, packet, variation, stress, finite, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4006_28_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4006_29_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4006_30_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    packet = insertion_packet_rows(timestamp)
    variation = variation_chain_rows(timestamp)
    stress = stress_gate_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["packet"], packet)
    write_csv(OUTPUTS["variation"], variation)
    write_csv(OUTPUTS["stress_gate"], stress)
    write_csv(OUTPUTS["finite_rows"], finite)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, packet, variation, stress, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4006 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
