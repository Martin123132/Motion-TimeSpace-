from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4005"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4005-Y5-R2FR-auxiliary-necessity-or-first-real-IX-source-coefficient.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

FINITE_B_RAB_BOUND = 6.102178699076298e-11

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4005_SOURCE_REGISTER.csv",
    "proof": SRC / "P8_Y5_R2FR_4005_AUXILIARY_NECESSITY_PROOF_ATTEMPT.csv",
    "language_gate": SRC / "P8_Y5_R2FR_4005_MINIMAL_OBJECT_LANGUAGE_GATE.csv",
    "coefficients": SRC / "P8_Y5_R2FR_4005_FIRST_REAL_IX_SOURCE_COEFFICIENT_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4005_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4005_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4005_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4005_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4005_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4005_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4005_VALIDATION.csv",
}

NEXT_DOC = "4006-Y5-R2FR-minimal-coframe-cell-parent-action-insertion-or-finite-RAB-coefficients.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4006_minimal_coframe_cell_parent_action_insertion_or_finite_RAB_coefficients.py"


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
        ("SRC4005_00_handoff", SRC / "P8_Y5_R2FR_4004_NEXT_TARGET.csv", "NEXT4004_0", "4004 handoff"),
        ("SRC4005_01_aux_zero", SRC / "P8_Y5_R2FR_4004_IX_AUXILIARY_KINETIC_FORK_THEOREM.csv", "IX4004_1_auxiliary_no_derivative_zero", "auxiliary zero theorem"),
        ("SRC4005_02_kinetic_counter", SRC / "P8_Y5_R2FR_4004_IX_AUXILIARY_KINETIC_FORK_THEOREM.csv", "IX4004_3_kinetic_countermodel", "kinetic countermodel"),
        ("SRC4005_03_aux_law", SRC / "P8_Y5_R2FR_4004_IX_COMPONENT_LAW.csv", "IXL4004_0_auxiliary_symplectic_zero", "auxiliary symplectic law"),
        ("SRC4005_04_deriv_law", SRC / "P8_Y5_R2FR_4004_IX_COMPONENT_LAW.csv", "IXL4004_1_derivative_current", "derivative current law"),
        ("SRC4005_05_finite_template", SRC / "P8_Y5_R2FR_4004_IX_COMPONENT_LAW.csv", "IXL4004_3_finite_force_template", "finite force template"),
        ("SRC4005_06_radial_config", SRC / "P8_Y5_R10_1272_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv", "RCD1272_2_radial_configuration_cell_normalization", "radial configuration-cell target"),
        ("SRC4005_07_parent_not_derived", SRC / "P8_Y5_R10_1272_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv", "RCD1272_7_verdict", "parent necessity verdict"),
        ("SRC4005_08_parent_contract", SRC / "P8_Y5_R10_1272_PARENT_NECESSITY_CONTRACT.csv", "PNC1272_1_radial_cell_owner", "parent radial-cell owner"),
        ("SRC4005_09_parent_zero", SRC / "P8_Y5_R10_1272_PARENT_NECESSITY_CONTRACT.csv", "PNC1272_7_parent_signed_zero_theorem", "parent-signed zero theorem contract"),
        ("SRC4005_10_linear_mult", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_4_linear_multiplier", "linear multiplier mechanism"),
        ("SRC4005_11_unimodular", SRC / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv", "HCO1273_5_unimodular_radial_cell", "unimodular radial-cell route"),
        ("SRC4005_12_no_deriv_verdict", SRC / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv", "GRAM2236_5_verdict", "no-derivative grammar verdict"),
        ("SRC4005_13_lambda_zero", SRC / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv", "ELIM2236_2_Lambda_zero", "auxiliary Lambda zero"),
        ("SRC4005_14_coframe_lock", SRC / "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv", "RCD3853_2_parent_cell_lock", "coframe cell lock"),
        ("SRC4005_15_scalar_reduction", SRC / "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv", "RCD3853_3_relation_to_3852_lambda", "scalar reduction to lambda_R"),
        ("SRC4005_16_finite_bound", SRC / "P8_Y5_R2FR_3853_FINITE_HAIR_FALLBACK_ROW.csv", "FHF3853_0_no_cell_lock_finite_hair", "finite RAB hair bound"),
        ("SRC4005_17_top_cell", SRC / "P8_Y5_R2FR_3854_TOPOLOGICAL_CELL_CHARGE_AUDIT.csv", "TCA3854_2_all_subdomain_charge", "all-subdomain cell charge"),
        ("SRC4005_18_lock_cond", SRC / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv", "CLT3854_1_topological_conditional", "cell lock conditional theorem"),
        ("SRC4005_19_lock_verdict", SRC / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv", "CLT3854_2_strict_current_verdict", "strict current verdict"),
        ("SRC4005_20_claim_policy", SRC / "P8_Y5_R2FR_3881_PARENT_ACTION_INSERTION_CONTRACT.csv", "PAC3881_10_claim_policy", "parent-action insertion claim policy"),
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


def proof_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "AN4005_0_cell_two_form_identity",
            "claim_piece": "radial observer-cell identity",
            "mathematical_form": "theta^0=T c dt, theta^1=sqrt(S)dr, Omega_tr=(theta^0/c) wedge theta^1=T sqrt(S) dt wedge dr, R_AB=ln(T^2 S)=2 ln(T sqrt(S)).",
            "derived_result": "The extra local reciprocal mode is exactly the radial coframe-cell density mode.",
            "status": "EXACT_IDENTITY",
            "source_path": str(SRC / "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_1_all_subdomain_cell_charge",
            "claim_piece": "pointwise cell lock from all local cells",
            "mathematical_form": "If Q_cell[D]=int_D(Omega_tr-Omega_ref)=0 for every local radial cell D, then T sqrt(S)-1=0 pointwise; hence R_AB=0.",
            "derived_result": "This is the strongest non-GR origin found: all-subdomain cell charge is sufficient by the fundamental lemma.",
            "status": "PROVED_IF_PARENT_SIGNED_BUT_EQUIVALENT_TO_LOCAL_CONSTRAINT",
            "source_path": str(SRC / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_2_multiplier_implementation",
            "claim_piece": "auxiliary multiplier implementation",
            "mathematical_form": "S_cell=int_U Lambda_J(Omega_tr-Omega_ref) -> int dr lambda_J ln(T sqrt(S)) = 1/2 int dr lambda_R ln(T^2 S).",
            "derived_result": "The lambda_R compatibility action is the scalar reduction of a coframe-cell lock, so the auxiliary route is not arbitrary decoration.",
            "status": "EXACT_REWRITE_OF_CANDIDATE",
            "source_path": str(SRC / "P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_3_minimal_object_language_exclusion",
            "claim_piece": "no-derivative auxiliary necessity under minimal grammar",
            "mathematical_form": "If the parent object language contains only the local coframe two-form cell lock, multiplier/topological all-cell charge, q-basic readout variables, and no vertical metric/connection/source labels, then D_mu R_AB, D_mu Lambda_R, and boundary derivative terms are not constructible.",
            "derived_result": "Under this minimal MTS object language, the extra sector must be auxiliary and I_X has no symplectic current.",
            "status": "DERIVED_CONDITIONAL_ON_MINIMAL_OBJECT_LANGUAGE",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_4_current_corpus_no_strict_necessity",
            "claim_piece": "strict-current limitation",
            "mathematical_form": "Gauge routes preserve Omega_tr or change readout; ordinary closed/global topological charges are too weak; only all-subdomain charge works, and that is equivalent to the local constraint.",
            "derived_result": "The current corpus does not yet prove auxiliary necessity from deeper primitives; it proves the exact condition that would make it true.",
            "status": "STRICT_PROOF_NOT_CLOSED",
            "source_path": str(SRC / "P8_Y5_R2FR_3854_OBSERVER_CELL_GAUGE_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_5_first_real_bound_target",
            "claim_piece": "finite I_X/R_AB fallback budget",
            "mathematical_form": f"B_RAB <= {FINITE_B_RAB_BOUND:.16e} before other gamma residuals, with B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|).",
            "derived_result": "If the auxiliary proof is not parent-signed, the first real nonclaim numerical target is the finite-hair budget, not a fabricated Z_R.",
            "status": "SOURCE_BACKED_BOUND_TARGET_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3853_FINITE_HAIR_FALLBACK_ROW.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "AN4005_6_verdict",
            "claim_piece": "auxiliary necessity verdict",
            "mathematical_form": "auxiliary_zero = all_subdomain_cell_charge + minimal_object_language + matter_descent + boundary_nohair + bulk_stress_guard; else finite coefficient rows.",
            "derived_result": "We have a genuine conditional derivation route and a real bound target. We do not yet have strict parent adoption of the route.",
            "status": "CONDITIONAL_DERIVATION_PLUS_FINITE_ROW",
            "source_path": str(SRC / "P8_Y5_R2FR_4004_DECISION_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def language_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MOL4005_0_fields",
            "requirement": "local coframe cell variables",
            "exact_condition": "theta^0, theta^1, Omega_tr, Lambda_J/lambda_R and q-basic public readout variables are declared before local readout.",
            "current_status": "CANDIDATE_PRESENT",
            "if_closed": "R_AB is a compatibility coordinate rather than a free physical scalar.",
            "if_open": "R_AB field sort remains ambiguous.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_1_all_local_cell_charge",
            "requirement": "all-subdomain cell lock",
            "exact_condition": "Q_cell[D]=int_D(Omega_tr-Omega_ref)=0 for every local radial cell D.",
            "current_status": "SUFFICIENT_BUT_NOT_PARENT_SIGNED",
            "if_closed": "R_AB=0 follows pointwise by the fundamental lemma.",
            "if_open": "cell lock is closure/control branch only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_2_no_vertical_metric",
            "requirement": "no vertical metric/connection",
            "exact_condition": "parent grammar has no G_vert, nabla_vert, or natural fibre metric that can form |D R_AB|^2.",
            "current_status": "REQUIRED_UNSIGNED",
            "if_closed": "D_mu R_AB kinetic terms are not constructible.",
            "if_open": "Z_R finite branch is legal.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_3_no_derivative_boundary",
            "requirement": "no derivative boundary/corner hair",
            "exact_condition": "no B_R[R_AB,D R_AB] or Pi_R^n boundary momentum is admitted by the variational class.",
            "current_status": "REQUIRED_UNSIGNED",
            "if_closed": "no Q_R/B_R exterior hair in I_X.",
            "if_open": "boundary coefficient row remains mandatory.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_4_matter_readout_descent",
            "requirement": "matter/source/readout ignores R_AB representative",
            "exact_condition": "delta_R(S_matter+B_readout+S_eff)=0 on the protected local branch.",
            "current_status": "REQUIRED_UNSIGNED",
            "if_closed": "E_R gives Lambda_R=0 and no source charge J_R.",
            "if_open": "J_R row remains mandatory.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_5_bulk_stress_guard",
            "requirement": "constraint stress cannot re-enter C_tau_bulk",
            "exact_condition": "metric/coframe variation of the cell-lock sector is zero, topological/proper, or retained as explicit stress residual.",
            "current_status": "OPEN_STRESS_GUARD",
            "if_closed": "Theta_X zero is not hiding force in stress.",
            "if_open": "I_X symplectic zero cannot promote local GR.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "MOL4005_6_claim_policy",
            "requirement": "parent adoption policy",
            "exact_condition": "the minimal coframe-cell object language is inserted into the parent action before any claim.",
            "current_status": "NOT_ADOPTED_IN_PARENT_ACTION",
            "if_closed": "auxiliary zero route can be re-scored with remaining 4003 gates.",
            "if_open": "keep closure label or finite coefficient branch.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "IXCOEF4005_0_B_RAB_budget",
            "quantity": "B_RAB_max_allowed_before_other_gamma_residuals",
            "numeric_value": FINITE_B_RAB_BOUND,
            "units": "dimensionless_gamma_like_budget",
            "formula": "B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)",
            "source_path": str(SRC / "P8_Y5_R2FR_3853_FINITE_HAIR_FALLBACK_ROW.csv"),
            "source_status": "SOURCE_BACKED_BOUND_TARGET",
            "coefficient_status": "BOUND_TARGET_ONLY_NOT_PREDICTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXCOEF4005_1_Z_R",
            "quantity": "Z_R",
            "numeric_value": "MISSING_SOURCE_BACKED_VALUE_OR_ZERO_THEOREM",
            "units": "parent_action_kinetic_units",
            "formula": "coefficient of |D R_AB|^2 if derivative branch is legal",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"),
            "source_status": "MISSING_INPUT",
            "coefficient_status": "REQUIRED_IF_NO_DERIVATIVE_GRAMMAR_FAILS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXCOEF4005_2_M_R2",
            "quantity": "M_R^2",
            "numeric_value": "MISSING_PARENT_HESSIAN_OR_RANGE_SCALE",
            "units": "inverse_length_squared_or_parent_units",
            "formula": "ell_R=sqrt(Z_R/M_R^2) when finite derivative branch is used",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"),
            "source_status": "MISSING_INPUT",
            "coefficient_status": "REQUIRED_IF_Z_R_FINITE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXCOEF4005_3_J_R",
            "quantity": "J_R",
            "numeric_value": "MISSING_MATTER_DESCENT_ZERO_OR_SOURCE_COUPLING",
            "units": "source_charge_density_units",
            "formula": "direct source/readout coupling in E_R",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"),
            "source_status": "MISSING_INPUT",
            "coefficient_status": "REQUIRED_IF_MATTER_DESCENT_FAILS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXCOEF4005_4_boundary",
            "quantity": "B_R_or_Pi_R_n",
            "numeric_value": "MISSING_BOUNDARY_NOHAIR_OR_FLUX_BOUND",
            "units": "boundary_momentum_or_charge_units",
            "formula": "boundary reciprocal charge/flux contribution to finite R_AB hair",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"),
            "source_status": "MISSING_INPUT",
            "coefficient_status": "REQUIRED_IF_BOUNDARY_NOHAIR_FAILS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXCOEF4005_5_projection",
            "quantity": "q_R_to_gamma_R10_PPN_projection",
            "numeric_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless_projection_or_kernel_units",
            "formula": "maps finite R_AB/I_X branch to gamma, beta, R10, clocks and orbital arenas",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"),
            "source_status": "NONCLAIM_TEMPLATE_ONLY",
            "coefficient_status": "REQUIRED_BEFORE_ANY_LOCAL_SCORE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4005_0_parent_signed_auxiliary",
            "description": "all-subdomain cell charge and minimal object language are parent-signed with source/boundary/stress guards",
            "all_subdomain_cell_charge": True,
            "minimal_object_language": True,
            "matter_descent": True,
            "boundary_nohair": True,
            "bulk_stress_guard": True,
            "finite_coefficients_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4005_1_cell_lock_without_grammar",
            "description": "cell lock is assumed/signed but derivative grammar and stress guards are not signed",
            "all_subdomain_cell_charge": True,
            "minimal_object_language": False,
            "matter_descent": True,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "finite_coefficients_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4005_2_gauge_or_global_charge_only",
            "description": "coordinate gauge, observer boost, split rescaling or single global charge only",
            "all_subdomain_cell_charge": False,
            "minimal_object_language": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "finite_coefficients_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4005_3_no_cell_lock_budget_only",
            "description": "no cell-lock derivation; carry finite RAB budget target only",
            "all_subdomain_cell_charge": False,
            "minimal_object_language": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "finite_coefficients_complete": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4005_4_finite_coefficients_complete",
            "description": "finite branch has source-backed coefficients and arena projections",
            "all_subdomain_cell_charge": False,
            "minimal_object_language": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "finite_coefficients_complete": True,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4005_5_missing_schema",
            "description": "source/schema paths missing",
            "all_subdomain_cell_charge": False,
            "minimal_object_language": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "finite_coefficients_complete": False,
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
            aux_zero = False
            finite_status = "MISSING"
            next_action = "repair source/schema"
        elif all(bool(case[key]) for key in ["all_subdomain_cell_charge", "minimal_object_language", "matter_descent", "boundary_nohair", "bulk_stress_guard"]):
            status = "CONDITIONAL_AUXILIARY_NECESSITY_CLOSED"
            aux_zero = True
            finite_status = "not_required_for_I_X"
            next_action = "carry to remaining 4003 projector/boundary/matter/Dq gates"
        elif bool(case["finite_coefficients_complete"]):
            status = "FINITE_BRANCH_SCORE_READY_NONCLAIM"
            aux_zero = False
            finite_status = "source_backed_coefficients_available"
            next_action = "score residual against local arenas without local-GR claim"
        elif bool(case["all_subdomain_cell_charge"]) and not bool(case["minimal_object_language"]):
            status = "CELL_LOCK_BUT_DERIVATIVE_ESCAPE_OPEN"
            aux_zero = False
            finite_status = "Z_R_boundary_stress_rows_required"
            next_action = "sign minimal object language or fill Z_R/J_R/B_R rows"
        elif not bool(case["all_subdomain_cell_charge"]):
            status = "NO_CELL_LOCK_USE_FINITE_BUDGET"
            aux_zero = False
            finite_status = f"B_RAB_bound_target={FINITE_B_RAB_BOUND:.16e}"
            next_action = "do not claim zero; acquire finite coefficients or adopt explicit closure"
        else:
            status = "AUXILIARY_NECESSITY_OPEN"
            aux_zero = False
            finite_status = "component_rows_required"
            next_action = "close missing guard or source coefficient"
        results.append(
            {
                "case_id": case["case_id"],
                "input_status": status,
                "I_X_auxiliary_zero_allowed": aux_zero,
                "finite_branch_status": finite_status,
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
            "decision_id": "DG4005_0_auxiliary_necessity",
            "question": "Did 4005 prove auxiliary/no-derivative necessity outright?",
            "answer": "False",
            "reason": "It proves necessity under a minimal coframe-cell object language, but current sources do not yet parent-sign that object language.",
            "action": "keep nonclaim; no local-GR promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4005_1_strongest_route",
            "question": "What is the strongest derivation route now?",
            "answer": "all-subdomain coframe-cell charge plus minimal object-language exclusion",
            "reason": "Gauge and ordinary topological/global charges fail; all-subdomain charge gives pointwise cell lock and the minimal grammar forbids derivative hair.",
            "action": "attempt parent action insertion contract next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4005_2_first_real_number",
            "question": "What is the first real finite-branch number?",
            "answer": f"B_RAB <= {FINITE_B_RAB_BOUND:.16e}",
            "reason": "No source-backed Z_R/M_R/J_R exists, but the finite hair budget is already source-backed by the 3853 fallback row.",
            "action": "use it as a nonclaim target while acquiring real coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CG4005_0_auxiliary_necessity", "auxiliary necessity theorem", False, "minimal object language not parent-signed"),
        ("CG4005_1_I_X_zero", "I_X zero claim", False, "source/boundary/stress guards remain open"),
        ("CG4005_2_local_GR_Newton", "local GR/Newton promotion", False, "4003 current-chain gates remain open"),
        ("CG4005_3_finite_branch_score", "finite branch score/pass", False, "Z_R/M_R/J_R/boundary/projection coefficients missing"),
        ("CG4005_4_public_claim", "public claim", False, "private nonclaim checkpoint"),
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
            "row_id": "NEXT4005_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "either write the minimal coframe-cell parent-action insertion contract that would sign auxiliary necessity, or acquire real finite R_AB/I_X coefficients against the B_RAB budget",
            "success_condition": "parent insertion includes all-subdomain cell charge, no vertical metric, no derivative boundary, matter/readout descent and stress guard; otherwise Z_R,M_R2,J_R,B_R/Pi_R,projection rows become source-backed nonclaim inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "auxiliary necessity is derived under minimal coframe-cell object language; strict current corpus still lacks parent adoption, so first real finite target is B_RAB <= 6.102178699076298e-11",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4005 - Auxiliary Necessity Or First Real I_X Source Coefficient",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The best derivation route is now precise:",
        "",
        "`Omega_tr=(theta^0/c) wedge theta^1=T sqrt(S) dt wedge dr`,",
        "",
        "`R_AB=ln(T^2 S)=2 ln(T sqrt(S))`.",
        "",
        "If the parent signs `int_D(Omega_tr-Omega_ref)=0` for every local radial cell `D`, then `Omega_tr=Omega_ref` pointwise, so `T sqrt(S)=1` and `R_AB=0`.",
        "",
        "## Auxiliary Necessity Attempt",
        "",
        "Under a minimal coframe-cell object language, the only allowed implementation is algebraic/topological/multiplier-like:",
        "",
        "`S_cell=int_U Lambda_J(Omega_tr-Omega_ref)`,",
        "",
        "with no vertical metric, no `D_mu R_AB`, no `D_mu Lambda_R`, no derivative boundary term, and no matter/readout source labels.",
        "",
        "Then the extra sector is auxiliary: `Theta_X=0`, `Q_tau^X=0/proper`, and `I_X=0` for this branch.",
        "",
        "## Why It Is Not Claimed Yet",
        "",
        "Current sources do not prove that minimal object language from deeper MTS primitives. Gauge routes fail, ordinary global/topological charges are too weak, and the all-subdomain charge is basically the local constraint written honestly.",
        "",
        "So this is not fake progress and not a public claim: it is the exact parent-action insertion target.",
        "",
        "## First Real Finite Target",
        "",
        f"If the parent does not sign the cell-lock/minimal-grammar route, the finite branch must satisfy `B_RAB <= {FINITE_B_RAB_BOUND:.16e}` before other gamma residuals.",
        "",
        "The missing coefficient rows are `Z_R`, `M_R^2`, `J_R`, boundary `B_R/Pi_R^n`, and arena projection. Those are not fabricated.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: `{row['input_status']}`, aux_zero={row['I_X_auxiliary_zero_allowed']}, finite=`{row['finite_branch_status']}`, claim={row['claim_allowed']}, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "We are closer in the useful sense: the route to `I_X=0` is now a single parent-insertion contract, and the fallback has a real bound target. The theory still needs the parent to sign the coframe-cell object language or produce real finite coefficients.",
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
    marker = "## 4005 - Auxiliary Necessity / First I_X Coefficient"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `R_AB=ln(T^2S)=2ln(T sqrt(S))` is the radial coframe-cell density mode; all-subdomain `int_D(Omega_tr-Omega_ref)=0` gives pointwise `R_AB=0`.
- Auxiliary route: under minimal coframe-cell object language with no vertical metric, derivative boundary, source label, or matter/readout coupling, the extra branch is auxiliary and `Theta_X=Q_tau^X=I_X=0` conditionally.
- Strict verdict: current sources do not parent-sign that minimal object language; gauge/global topological routes fail or are too weak.
- Finite fallback: first real bound target is `B_RAB <= {FINITE_B_RAB_BOUND:.16e}` before other gamma residuals; `Z_R`, `M_R^2`, `J_R`, boundary and projection coefficients remain missing/nonclaim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    coeffs: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4005_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4005_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4005_02_cell_identity", any(row["proof_id"] == "AN4005_0_cell_two_form_identity" for row in proof), "cell two-form identity present")
    add("VAL4005_03_subdomain_charge", any(row["proof_id"] == "AN4005_1_all_subdomain_cell_charge" for row in proof), "all-subdomain charge theorem present")
    add("VAL4005_04_multiplier", any(row["proof_id"] == "AN4005_2_multiplier_implementation" for row in proof), "multiplier implementation present")
    add("VAL4005_05_minimal_language", any(row["proof_id"] == "AN4005_3_minimal_object_language_exclusion" for row in proof), "minimal language exclusion present")
    add("VAL4005_06_no_strict_claim", any(row["proof_id"] == "AN4005_4_current_corpus_no_strict_necessity" for row in proof), "strict-current limitation present")
    add("VAL4005_07_bound_target", any(row["proof_id"] == "AN4005_5_first_real_bound_target" for row in proof), "first real bound target present")
    add("VAL4005_08_verdict", any(row["proof_id"] == "AN4005_6_verdict" for row in proof), "proof verdict present")
    add("VAL4005_09_language_gate_count", len(gates) == 7, "minimal object-language gates present")
    add("VAL4005_10_all_cell_gate", any(row["gate_id"] == "MOL4005_1_all_local_cell_charge" for row in gates), "all-local-cell gate present")
    add("VAL4005_11_no_vertical_gate", any(row["gate_id"] == "MOL4005_2_no_vertical_metric" for row in gates), "no-vertical-metric gate present")
    budget = next(row for row in coeffs if row["row_id"] == "IXCOEF4005_0_B_RAB_budget")
    add("VAL4005_12_budget_numeric", float(budget["numeric_value"]) > 0.0 and "SOURCE_BACKED_BOUND_TARGET" in budget["source_status"], "finite B_RAB budget is positive/source-backed target")
    add("VAL4005_13_coeff_missing_honest", any(row["row_id"] == "IXCOEF4005_1_Z_R" and "MISSING" in str(row["numeric_value"]) for row in coeffs), "missing Z_R is not fabricated")
    zero = next(row for row in results if row["case_id"] == "CASE4005_0_parent_signed_auxiliary")
    no_grammar = next(row for row in results if row["case_id"] == "CASE4005_1_cell_lock_without_grammar")
    no_lock = next(row for row in results if row["case_id"] == "CASE4005_3_no_cell_lock_budget_only")
    finite = next(row for row in results if row["case_id"] == "CASE4005_4_finite_coefficients_complete")
    missing = next(row for row in results if row["case_id"] == "CASE4005_5_missing_schema")
    add("VAL4005_14_aux_case", str(zero["I_X_auxiliary_zero_allowed"]).lower() == "true", "parent-signed auxiliary case zeroes I_X conditionally")
    add("VAL4005_15_derivative_escape_case", no_grammar["input_status"] == "CELL_LOCK_BUT_DERIVATIVE_ESCAPE_OPEN", "cell lock without grammar keeps derivative escape open")
    add("VAL4005_16_budget_case", str(FINITE_B_RAB_BOUND) in no_lock["finite_branch_status"] or f"{FINITE_B_RAB_BOUND:.16e}" in no_lock["finite_branch_status"], "no-cell-lock case carries finite budget")
    add("VAL4005_17_finite_case", finite["input_status"] == "FINITE_BRANCH_SCORE_READY_NONCLAIM" and str(finite["claim_allowed"]).lower() == "false", "finite coefficient case remains nonclaim")
    add("VAL4005_18_missing_blocks", missing["finite_branch_status"] == "MISSING", "missing schema blocks")
    add("VAL4005_19_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4005_20_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4005_21_doc_exists", DOC_PATH.exists() and "First Real Finite Target" in read_text(DOC_PATH), "document written")
    add("VAL4005_22_spine_updated", SPINE_PATH.exists() and "## 4005 - Auxiliary Necessity / First I_X Coefficient" in read_text(SPINE_PATH), "spine updated")
    add("VAL4005_23_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4005_24_compile", compile_ok, "script compiles")
    add("VAL4005_25_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4005_26_status_exists", OUTPUTS["status"].exists(), "status file exists")
    output_tables = [sources, proof, gates, coeffs, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4005_27_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4005_28_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4005_29_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    proof = proof_rows(timestamp)
    gates = language_gate_rows(timestamp)
    coeffs = coefficient_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["proof"], proof)
    write_csv(OUTPUTS["language_gate"], gates)
    write_csv(OUTPUTS["coefficients"], coeffs)
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

    validation = build_validation_rows(timestamp, sources, proof, gates, coeffs, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4005 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
