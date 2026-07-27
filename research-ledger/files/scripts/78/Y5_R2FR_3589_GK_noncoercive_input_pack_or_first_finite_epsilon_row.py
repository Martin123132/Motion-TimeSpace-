from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_GK_NONCOERCIVE_INPUT_PACK_3589"
CHECKPOINT_ID = "3589"
DOC = ROOT / "3589-Y5-R2FR-GK-noncoercive-input-pack-or-first-finite-epsilon-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3588": RESIDUALS / "P8_Y5_R2FR_3588_NEXT_TARGET.csv",
        "status_3588": RESIDUALS / "P8_Y5_R2FR_3588_STATUS.csv",
        "switch_3588": RESIDUALS / "P8_Y5_R2FR_3588_NONCOERCIVE_SWITCH_ROWS.csv",
        "validation_3588": RESIDUALS / "P8_Y5_BRR545_3588_VALIDATION.csv",
        "noncoercive_2079": RESIDUALS / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
        "owner_3587": RESIDUALS / "P8_Y5_R2FR_3587_GK_INPUT_OWNER_MATRIX.csv",
        "candidate_3587": RESIDUALS / "P8_Y5_R2FR_3587_GK_CANDIDATE_BOUND_INPUT_ROWS.csv",
        "hair_3586": RESIDUALS / "P8_Y5_R2FR_3586_GK_HAIR_BOUND_ROWS.csv",
        "epsilon_3585": RESIDUALS / "P8_Y5_R2FR_3585_EPSILON_HAIR_BOUND_ROWS.csv",
        "domain_3583": RESIDUALS / "P8_Y5_R2FR_3583_SAME_PANN_DOMAIN_THEOREM.csv",
        "geometry_3583": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "missing_coeff_2473": RESIDUALS / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
        "runner_inputs_2475": RESIDUALS / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv",
        "qloc_interface_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
        "qloc_gate_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
        "source_charge_1793": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "boundary_cohom_549": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
        "projector_obstruction_549": RESIDUALS / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_OBSTRUCTION_LEDGER.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3589_SOURCE_REGISTER.csv",
        "domain_constant_pack": RESIDUALS / "P8_Y5_R2FR_3589_DOMAIN_CONSTANT_PACK.csv",
        "input_pack": RESIDUALS / "P8_Y5_R2FR_3589_NONCOERCIVE_INPUT_PACK.csv",
        "finite_epsilon": RESIDUALS / "P8_Y5_R2FR_3589_FIRST_FINITE_EPSILON_ROW.csv",
        "circularity_gates": RESIDUALS / "P8_Y5_R2FR_3589_CIRCULARITY_GATES.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3589_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3589_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3589_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_GK_noncoercive_input_pack_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3589_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3589 finite noncoercive GK input-pack source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def domain_constant_pack_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "DCP3589_0_domain_id",
            "D_GK",
            "D_GK := D_ext with the stationary annulus, self-adjoint GK field domain, gauge quotient, and fixed boundary class",
            "DOMAIN_OBJECT_DEFINED_CONDITIONALLY",
            "3583 defines the exterior-domain certificate, but E_stat/self-adjoint GK domain is not parent-signed",
            "domain_3583",
            False,
        ),
        (
            "DCP3589_1_X_GK_norm",
            "X_GK",
            "X_GK := ||u_GK||_{E,nc,D_GK}, a finite-energy norm on u_GK=(A,gamma) after gauge/topology quotient",
            "NORM_CONTRACT_DEFINED_SYMBOLIC",
            "the norm is declared for the noncoercive branch and must match every source, boundary, and observable row",
            "switch_3588",
            False,
        ),
        (
            "DCP3589_2_C_Poincare_GK",
            "C_Poincare_GK",
            "best constant in ||u_GK||_{L2(D_GK)} <= C_Poincare_GK ||u_GK||_{E,nc,D_GK} on the selected quotient domain",
            "DERIVED_SYMBOLIC_GEOMETRIC_CONSTANT_DOMAIN_NUMERIC_MISSING",
            "mathematically standard once D_GK and quotient boundary class are fixed; not a fitted physics parameter",
            "positive_pack_1846",
            True,
        ),
        (
            "DCP3589_3_C_trace_GK",
            "C_trace_GK",
            "operator norm of the trace map u_GK in H^1(D_GK) -> u_GK|partialD in H^{1/2}(partialD)",
            "DERIVED_SYMBOLIC_GEOMETRIC_CONSTANT_DOMAIN_NUMERIC_MISSING",
            "mathematically standard once D_GK boundary regularity is fixed; needed for Phi_boundary_GK",
            "positive_pack_1846",
            True,
        ),
        (
            "DCP3589_4_C_top_GK",
            "C_top_GK",
            "finite-dimensional norm of harmonic/topological/projector kernel components in the chosen residual norm",
            "CONDITIONAL_ZERO_OR_FINITE_CONSTANT_NEEDS_TOPOLOGY_LOCK",
            "zero only if relative cohomology, projector ownership, and gauge kernel are parent-locked; otherwise finite input",
            "boundary_cohom_549",
            False,
        ),
        (
            "DCP3589_5_unit_contract",
            "GK_nc_units",
            "J_GK_norm*X_GK, Phi_boundary_GK, Q_top_GK, and F_outer_GK_abs must all be converted to the same X_GK^2 energy/residual units",
            "UNIT_CONTRACT_DEFINED_VALUES_MISSING",
            "prevents adding source, boundary, topology, and arena rows in incompatible normalizations",
            "candidate_3587",
            False,
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "mathematically_defined": mathematically_defined,
            "numeric_value_present": False,
            "domain_parent_signed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, definition, status, detail, source_key, mathematically_defined in rows
    ]


def input_pack_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "NCI3589_0_C_Poincare_GK",
            "C_Poincare_GK",
            "DCP3589_2_C_Poincare_GK",
            "symbolic domain constant",
            "DERIVED_SYMBOLIC_VALUE_NUMERIC_DOMAIN_MISSING",
            "needs D_GK/domain_id/quotient boundary class before numeric use",
            "positive_pack_1846",
        ),
        (
            "NCI3589_1_C_trace_GK",
            "C_trace_GK",
            "DCP3589_3_C_trace_GK",
            "symbolic domain constant",
            "DERIVED_SYMBOLIC_VALUE_NUMERIC_DOMAIN_MISSING",
            "needs D_GK/boundary regularity before numeric use",
            "positive_pack_1846",
        ),
        (
            "NCI3589_2_C_top_GK",
            "C_top_GK",
            "DCP3589_4_C_top_GK",
            "topology/projector finite norm",
            "MISSING_TOPOLOGY_OR_PROJECTOR_ZERO_OR_FINITE_VALUE",
            "topological/projector sector cannot be hidden inside P_loc",
            "projector_obstruction_549",
        ),
        (
            "NCI3589_3_J_GK_norm",
            "J_GK_norm",
            "||(J_A,J_gamma)||_* in the dual of the selected noncoercive GK domain",
            "source-current norm",
            "MISSING_SOURCE_ZERO_OR_FINITE_SOURCE_NORM",
            "Euler/source gap survives until parent matter/current grammar fixes it",
            "qloc_interface_2581",
        ),
        (
            "NCI3589_4_Phi_boundary_GK",
            "Phi_boundary_GK",
            "absolute boundary/symplectic work in the GK integration-by-parts identity",
            "boundary flux",
            "MISSING_BOUNDARY_ZERO_OR_FINITE_FLUX",
            "self-adjoint domain/reference class and no symplectic leakage are still unsigned",
            "candidate_3587",
        ),
        (
            "NCI3589_5_Q_top_GK",
            "Q_top_GK",
            "harmonic/topological/projector-kernel charge not controlled by the local differential operator",
            "topology/projector charge",
            "MISSING_TOPOLOGY_PROJECTOR_GAUGE_KERNEL_VALUE",
            "must be zero or bounded separately before a local-GR/PPN score",
            "boundary_cohom_549",
        ),
        (
            "NCI3589_6_F_outer_GK_abs",
            "F_outer_GK_abs",
            "noncircular outer work/defect term independent of X_GK, or an absorbed quadratic defect with eta_GK<1",
            "outer forcing/defect",
            "MISSING_NONCIRCULAR_OUTER_WORK_OR_ABSORPTION",
            "3586 cross-excess term scales like ||u_GK||^2 and cannot be inserted as F_outer without absorption",
            "hair_3586",
        ),
        (
            "NCI3589_7_K_GK",
            "K_GK",
            "operator-to-observable conversion from X_GK to epsilon_GK_hair or arena residual",
            "observable map",
            "MISSING_OPERATOR_TO_OBSERVABLE_MAP",
            "R10/PPN/clock/orbital kernels remain arena-specific and missing",
            "runner_inputs_2475",
        ),
        (
            "NCI3589_8_domain_norm_units",
            "domain_id,norm_id,units",
            "shared metadata locking every row to the same D_GK, X_GK, source units, and boundary orientation",
            "metadata",
            "MISSING_DOMAIN_NORM_UNIT_LOCK",
            "without this lock the finite expression is algebraically visible but not score-ready",
            "domain_3583",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "formula_or_owner": formula,
            "role": role,
            "status": status,
            "blocker_or_detail": detail,
            "source_path": str(source_paths[source_key]),
            "numeric_value_present": False,
            "source_backed": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, formula, role, status, detail, source_key in rows
    ]


def finite_epsilon_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "FFE3589_0_a_GK",
            "a_GK",
            "C_Poincare_GK*J_GK_norm + C_trace_GK*abs(Phi_boundary_GK) + C_top_GK*abs(Q_top_GK)",
            "linear source/boundary/topology coefficient controlling the noncoercive finite branch",
            "DERIVED_BY_DUALITY_TRACE_TOPOLOGY_SYMBOLIC",
            "noncoercive_2079",
        ),
        (
            "FFE3589_1_X_GK_bound",
            "X_GK_bound_nc",
            "0.5*(a_GK + sqrt(a_GK^2 + 4*F_outer_GK_abs))",
            "first finite noncoercive GK energy envelope, valid only if F_outer_GK_abs is nonnegative and independent of X_GK or all quadratic defects are absorbed",
            "FIRST_FINITE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "switch_3588",
        ),
        (
            "FFE3589_2_epsilon_GK_hair_nc",
            "epsilon_GK_hair_nc",
            "K_GK*X_GK_bound_nc",
            "first finite GK hair row that does not use a positive lambda_GK denominator",
            "FIRST_FINITE_EPSILON_ROW_SYMBOLIC_NONCLAIM",
            "epsilon_3585",
        ),
        (
            "FFE3589_3_score_policy",
            "score_ready",
            "False until all inputs in P8_Y5_R2FR_3589_NONCOERCIVE_INPUT_PACK.csv have numeric/sourced values and shared units",
            "prevents R10/PPN/local-GR scoring from symbolic placeholders",
            "BLOCKED_CURRENT_SCORE",
            "runner_inputs_2475",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "uses_positive_lambda_denominator": False,
            "numeric_value_present": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, meaning, status, source_key in rows
    ]


def circularity_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "CIRC3589_0_no_lambda_denominator",
            "finite branch must not use 1/lambda_GK or lambda_GK>0",
            "PASS_GUARD",
            "FFE3589 uses X_GK_bound_nc and never divides by lambda_GK",
            "switch_3588",
        ),
        (
            "CIRC3589_1_Fouter_independence",
            "F_outer_GK_abs must be an external/noncircular finite work term independent of X_GK",
            "FAIL_CURRENT_SCORE",
            "no current source row supplies such a value",
            "missing_coeff_2473",
        ),
        (
            "CIRC3589_2_cross_excess_not_outer_work",
            "epsilon_cross_hair_GK proportional to ||u_GK||^2 cannot be inserted into F_outer_GK_abs as if it were fixed forcing",
            "PASS_GUARD_BLOCKS_CHEAT",
            "quadratic cross excess must be absorbed by eta_GK<1 or kept as branch failure",
            "hair_3586",
        ),
        (
            "CIRC3589_3_absorption_alternative",
            "if quadratic defect <= eta_GK X_GK^2 with eta_GK<1, move it to the left and replace F_outer by fixed work terms",
            "AVAILABLE_BUT_MISSING_ETA_INPUT",
            "this is the lawful bridge between noncoercive finite branch and weak coercivity",
            "noncoercive_2079",
        ),
        (
            "CIRC3589_4_topology_projector_not_silent",
            "Q_top_GK cannot be set to zero by local projection alone",
            "FAIL_CURRENT_CLAIM",
            "projector/topology ownership remains open and must be a row in a_GK",
            "projector_obstruction_549",
        ),
        (
            "CIRC3589_5_first_finite_epsilon_constructed",
            "first symbolic epsilon_GK_hair_nc row exists",
            "PASS_SYMBOLIC_NONCLAIM",
            "the formula is usable for future input acquisition but not for public or empirical claims",
            "switch_3588",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "criterion": criterion,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "blocks_score": status.startswith("FAIL"),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, criterion, status, detail, source_key in rows
    ]


def activation_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3589_0_sources", "PASS", "all source paths and selected anchors exist", "next_3588"),
        ("GATE3589_1_domain_constants", "PASS_SYMBOLIC_NONCLAIM", "C_Poincare_GK and C_trace_GK are mathematically defined once D_GK is fixed", "positive_pack_1846"),
        ("GATE3589_2_input_pack", "PASS_SOURCE_READY_NONCLAIM", "all finite noncoercive input slots have source/unit owners", "candidate_3587"),
        ("GATE3589_3_first_finite_epsilon", "PASS_SYMBOLIC_NONCLAIM", "epsilon_GK_hair_nc expression exists without lambda_GK denominator", "switch_3588"),
        ("GATE3589_4_Fouter", "FAIL_CURRENT_SCORE", "noncircular F_outer_GK_abs or eta_GK<1 absorption is missing", "hair_3586"),
        ("GATE3589_5_no_hidden_score", "PASS_GUARD", "R10/PPN/local-GR score remains blocked until numeric/sourced finite inputs exist", "runner_inputs_2475"),
        ("GATE3589_6_local_GR", "FAIL_CURRENT_CLAIM", "finite GK hair row does not close source coupling, EM gauge/corner, GM calibration, or PPN residuals", "source_charge_1793"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "FIRST_NONCOERCIVE_EPSILON_ROW_DERIVED_INPUT_PACK_SOURCE_BLOCKED",
            "strongest_result": "3589 derives the first finite GK noncoercive branch without using lambda_GK: a_GK=C_Poincare_GK*J_GK_norm+C_trace_GK*|Phi_boundary_GK|+C_top_GK*|Q_top_GK|, X_GK<=0.5*(a_GK+sqrt(a_GK^2+4F_outer_GK_abs)), and epsilon_GK_hair_nc<=K_GK*X_GK. C_Poincare_GK and C_trace_GK are promoted from vague missing parameters to symbolic geometric constants once D_GK is fixed.",
            "decision": "keep GK finite branch alive as a source-ready nonclaim formula; block scoring because F_outer_GK_abs/K_GK/source-boundary-topology inputs are not numeric/sourced and F_outer circularity is unresolved",
            "still_missing": "D_GK numeric/domain lock; C_top_GK or topology zero; J_GK_norm; Phi_boundary_GK; Q_top_GK; noncircular F_outer_GK_abs or eta_GK<1 absorption; K_GK observable map; shared units; source coupling/Newton/PPN closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3588"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3589_0",
            "target_doc": "3590-Y5-R2FR-GK-outer-work-absorption-or-finite-branch-failure.md",
            "target_script": "scripts/Y5_R2FR_3590_GK_outer_work_absorption_or_finite_branch_failure.py",
            "objective": "try to derive a noncircular F_outer_GK_abs independent of X_GK, or an absorption bound eta_GK<1 for quadratic cross/projector defects; if neither closes, demote finite GK hair to an explicit residual parameter",
            "success_gate": "F_outer_GK_abs is source-backed and independent of X_GK, or eta_GK<1 is parent-signed; otherwise the GK finite branch is marked structurally non-score-ready rather than repeatedly refilled",
            "reason": "3589 shows the only remaining mathematical danger in the finite branch is circular outer work/quadratic defect absorption",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    domain_constants: list[dict[str, object]],
    inputs: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    circularity: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3588": "NEXT3588_0",
        "status_3588": "LAMBDA_GK_UNSIGNED_NONCOERCIVE_SWITCH_ACTIVE",
        "switch_3588": "NCS3588_1_finite_branch_law",
        "validation_3588": "VAL3588_12_formalization_workbench_untouched",
        "noncoercive_2079": "FIN2079_0_branch_law",
        "owner_3587": "GIO3587_1_J_GK_norm",
        "candidate_3587": "GIB3587_4_K_GK_candidate",
        "hair_3586": "GHB3586_6_epsilon_cross_hair_GK",
        "epsilon_3585": "EHB3585_1_epsilon_coercive_extra",
        "domain_3583": "SPD3583_0_Estat_object",
        "geometry_3583": "GRS3583_7_R_ann_abs_after_3583",
        "missing_coeff_2473": "MISS2473_5_Cmetric",
        "runner_inputs_2475": "RUN2475_R10_ANCHOR_INPUT",
        "qloc_interface_2581": "QLOC2581_3_Euler_source_gap",
        "qloc_gate_2581": "GK2581_4_double_zero",
        "source_charge_1793": "Y5SC1793_5_Gauss_orbital_calibration",
        "positive_pack_1846": "OP1846_3_self_adjoint_domain",
        "boundary_cohom_549": "BCT549_5_derivative_silence",
        "projector_obstruction_549": "PSO550_0_topological_route_not_owned",
    }
    validations.append(("VAL3589_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3589 source paths exist"))
    validations.append(("VAL3589_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3589 anchors found"))
    validations.append(("VAL3589_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3589 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3589_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3589_4_domain_constants_defined", {"C_Poincare_GK", "C_trace_GK", "C_top_GK", "X_GK"}.issubset({str(row["symbol"]) for row in domain_constants}), "domain/norm constants are explicitly defined"))
    required_inputs = {"C_Poincare_GK", "C_trace_GK", "C_top_GK", "J_GK_norm", "Phi_boundary_GK", "Q_top_GK", "F_outer_GK_abs", "K_GK", "domain_id,norm_id,units"}
    validations.append(("VAL3589_5_input_pack_complete", required_inputs.issubset({str(row["symbol"]) for row in inputs}), "all finite noncoercive input rows are present"))
    validations.append(("VAL3589_6_first_finite_epsilon_present", any(row["symbol"] == "epsilon_GK_hair_nc" and row["status"] == "FIRST_FINITE_EPSILON_ROW_SYMBOLIC_NONCLAIM" for row in finite_rows), "first noncoercive epsilon_GK_hair row exists"))
    finite_formula_text = " ".join(str(row["formula"]) for row in finite_rows)
    validations.append(("VAL3589_7_no_lambda_denominator", "lambda_GK" not in finite_formula_text and all(str(row.get("uses_positive_lambda_denominator", False)).lower() == "false" for row in finite_rows), "finite formula does not use lambda_GK"))
    validations.append(("VAL3589_8_circularity_guard_active", any(row["gate_id"] == "CIRC3589_2_cross_excess_not_outer_work" and row["status"] == "PASS_GUARD_BLOCKS_CHEAT" for row in circularity), "quadratic cross excess cannot be smuggled into F_outer"))
    validations.append(("VAL3589_9_Fouter_blocks_score", any(row["gate_id"] == "GATE3589_4_Fouter" and row["status"] == "FAIL_CURRENT_SCORE" for row in gates), "noncircular F_outer/eta absorption remains the score blocker"))
    generated_rows = domain_constants + inputs + finite_rows + circularity + gates + status + next_target
    validations.append(("VAL3589_10_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" and str(row.get("claim_allowed", False)).lower() == "false" for row in generated_rows), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3589_11_next_target_selected", any(row["next_id"] == "NEXT3589_0" for row in next_target), "3590 outer-work absorption target selected"))
    validations.append(("VAL3589_12_generated_source_paths_exist", all(Path(str(row["source_path"])).exists() for row in domain_constants + inputs + finite_rows + circularity + gates + status), "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3589*")) or any(FORMALIZATION.rglob("3589-Y5-R2FR*"))
    validations.append(("VAL3589_13_formalization_workbench_untouched", not formalization_touched, "no 3589 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    domain_constants: list[dict[str, object]],
    inputs: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    circularity: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3589 - GK noncoercive input pack or first finite epsilon row",
        "",
        "## Verdict",
        "3589 constructs the finite noncoercive GK route instead of only saying inputs are missing.  The first finite row is now explicit:",
        "",
        "`a_GK=C_Poincare_GK J_GK_norm + C_trace_GK |Phi_boundary_GK| + C_top_GK |Q_top_GK|`,",
        "",
        "`X_GK <= 0.5*(a_GK + sqrt(a_GK^2 + 4 F_outer_GK_abs))`,",
        "",
        "`epsilon_GK_hair_nc <= K_GK X_GK`.",
        "",
        "The expression is deliberately nonclaim: it does not use `lambda_GK`, but it needs a noncircular `F_outer_GK_abs` or an absorption proof for quadratic defects before it can be scored.",
        "",
        "## Domain constant pack",
    ]
    for row in domain_constants:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['status']} - {row['definition']}")
    lines.extend(["", "## Noncoercive input pack"])
    for row in inputs:
        lines.append(f"- `{row['input_id']}` `{row['symbol']}`: {row['status']} - {row['blocker_or_detail']}")
    lines.extend(["", "## First finite epsilon row"])
    for row in finite_rows:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Circularity gates"])
    for row in circularity:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['criterion']}")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    domain_constants = domain_constant_pack_rows(source_paths)
    inputs = input_pack_rows(source_paths)
    finite_rows = finite_epsilon_rows(source_paths)
    circularity = circularity_gate_rows(source_paths)
    gates = activation_gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "domain_constant_pack": domain_constants,
        "input_pack": inputs,
        "finite_epsilon": finite_rows,
        "circularity_gates": circularity,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, domain_constants, inputs, finite_rows, circularity, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(domain_constants, inputs, finite_rows, circularity, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3589 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
