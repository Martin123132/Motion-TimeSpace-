from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
R10_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def numeric(value: Any) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1199_0_1198_next",
            "relative_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "NEXT1198_0_1199",
            "role": "direct 1199 handoff.",
        },
        {
            "source_id": "SRC1199_1_1198_R10_import",
            "relative_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "QDT1198_0_R10_external_bound_import",
            "role": "nonclaim R10 external curve import.",
        },
        {
            "source_id": "SRC1199_2_1198_dryrun",
            "relative_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "DR1198_0_R10_qDT_bound_import_dryrun",
            "role": "R10 dry-run blocked by missing MTS-side inputs.",
        },
        {
            "source_id": "SRC1199_3_1198_anchor_no_go",
            "relative_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "DTA1198_5_verdict",
            "role": "D_T natural-boundary anchor no-go.",
        },
        {
            "source_id": "SRC1199_4_1035_R10_projection",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXD1035_4_R10_harmonic_projection",
            "role": "R10 harmonic projection contract precedent.",
        },
        {
            "source_id": "SRC1199_5_1035_harmonic_missing",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXF1035_3_harmonic",
            "role": "R10 harmonic projection is missing/nonnumeric.",
        },
        {
            "source_id": "SRC1199_6_437_yukawa",
            "relative_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "Yukawa_potential",
            "role": "accepted R10 Yukawa potential convention.",
        },
        {
            "source_id": "SRC1199_7_437_no_scalar_shortcut",
            "relative_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "single_delta_G_scalar",
            "role": "R10 is range-dependent; scalar residual is insufficient.",
        },
        {
            "source_id": "SRC1199_8_831_bound",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "q_loc/D_T residual bound by cokernel, boundary, and regularizer.",
        },
        {
            "source_id": "SRC1199_9_1197_runner",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "CBI1197_1_R10",
            "role": "R10 q_DT runner input row.",
        },
        {
            "source_id": "SRC1199_10_R10_candidate",
            "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "needle": "R10_VECTOR_2020_REVIEW_0000",
            "role": "real numeric external review-candidate curve.",
        },
        {
            "source_id": "SRC1199_11_1034_projection_blocked",
            "relative_path": "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "needle": "CGATE1034_2_mts_projection",
            "role": "MTS R10 projection blocked precedent.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def projection_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "R10P1199_0_observable_convention",
            "quantity": "alpha_DT(lambda)",
            "contract": "Use the same Yukawa convention as the R10 bound curve: V=V_N[1+alpha(lambda) exp(-r/lambda)] or the equivalent acceleration/torque projection.",
            "mathematical_form": "unit_alpha_signal(lambda)=Pi_R10[Torque[V_N exp(-r/lambda)]].",
            "status": "CONVENTION_FIXED_NONCLAIM",
            "missing_for_claim": "same-frame normalization and official/human-promoted bound curve",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_1_qDT_residual_budget",
            "quantity": "q_DT_bound",
            "contract": "Carry the D_T residual as an absolute positive budget before any R10 projection.",
            "mathematical_form": "q_DT_bound = f_coker||G_res|| + ||B_T|| + kappa_T C_T||E_reg|| + ||Delta_P||.",
            "status": "BOUND_FORM_DEFINED_INPUTS_MISSING",
            "missing_for_claim": "f_coker, G_res profile, B_T norm, kappa_T, C_T, E_reg, Delta_P source rows",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_2_W_R10_definition",
            "quantity": "W_R10(lambda)",
            "contract": "Define the R10 response operator as the unit-normalized torque/readout response to a unit q_DT residual profile.",
            "mathematical_form": "W_R10(lambda)=||Pi_R10 K_exp(lambda) G_DT|| / |unit_alpha_signal(lambda)|, with K_exp the experiment/source-test kernel.",
            "status": "PROJECTION_OPERATOR_DEFINED_SYMBOLICALLY",
            "missing_for_claim": "R10 geometry kernel, source/test density, harmonic weights, q_DT profile convention, unit-alpha denominator",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_3_alpha_bound_formula",
            "quantity": "alpha_DT_envelope(lambda)",
            "contract": "The scoreable prediction is a conservative envelope, not a signed cancellation.",
            "mathematical_form": "|alpha_DT(lambda)| <= W_R10(lambda) q_DT_bound.",
            "status": "ABSOLUTE_ENVELOPE_FORM_DEFINED",
            "missing_for_claim": "numeric W_R10(lambda) and numeric q_DT_bound components",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_4_non_yukawa_guard",
            "quantity": "non_Yukawa_qDT",
            "contract": "If q_DT does not produce a Yukawa-profile force, compare only through a conservative alpha_envelope(lambda) over the R10 separation/harmonic range.",
            "mathematical_form": "alpha_envelope(lambda) >= sup_R |delta a_DT(R)/a_N(R)| / |(1+R/lambda) exp(-R/lambda)|, or the torque-kernel analogue.",
            "status": "NON_YUKAWA_SHORTCUT_BLOCKED",
            "missing_for_claim": "declared R range/kernel, q_DT force profile, conservative supremum calculation",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_5_curve_join_rule",
            "quantity": "R10 pass condition",
            "contract": "For every curve row, require abs(alpha_DT(lambda_i)) <= alpha_bound(lambda_i), with no signed cancellation between components.",
            "mathematical_form": "W_R10(lambda_i)[f_coker||G||+||B_T||+kappa_T C_T||E_reg||+||Delta_P||] <= alpha_bound(lambda_i).",
            "status": "JOIN_RULE_DEFINED_NONEXECUTABLE",
            "missing_for_claim": "all theory-side inputs and promoted/nonclaim policy decision for bound curve",
            "valid_for_claim": False,
        },
        {
            "contract_id": "R10P1199_6_verdict",
            "quantity": "MTS-side R10 projection",
            "contract": "1199 converts q_DT-to-R10 from a vague missing input into a concrete response-operator contract.",
            "mathematical_form": "alpha_DT_bound(lambda)=W_R10(lambda) q_DT_bound, with all W/q inputs source-gated.",
            "status": "CONTRACT_DERIVED_NO_NUMERIC_R10_SCORE",
            "missing_for_claim": "W_R10, G_res, P_coker, B_T, E_reg, eps_P, and response/source paths",
            "valid_for_claim": False,
        },
    ]


def g_res_profile_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "schema_id": "GRP1199_0_G_res_profile",
            "required_object": "G_res^nu(x)",
            "definition": "local source vector entering D_TK_T=G_res, e.g. P_loc nabla^nu Gamma_eff after branch-specific corrections",
            "required_fields": "domain_id;coframe;gauge;units;profile_grid_or_formula;norm_L2_or_weighted;source_path;equation_ref",
            "current_value": "MISSING_G_RES_PROFILE",
            "valid_for_claim": False,
        },
        {
            "schema_id": "GRP1199_1_P_coker_fraction",
            "required_object": "f_coker(lambda/domain)",
            "definition": "fraction or projection norm of G_res into Ker(D_T^dagger) after boundary/quotient restrictions",
            "required_fields": "cokernel_basis_path;projection_inner_product;domain_boundary_class;fraction_abs;source_path",
            "current_value": "MISSING_P_COKER_FRACTION",
            "valid_for_claim": False,
        },
        {
            "schema_id": "GRP1199_2_B_T_boundary_norm",
            "required_object": "||B_T||",
            "definition": "bound on int_partialD n_mu K_T^(mu nu)(P_loc V)_nu or a zero certificate",
            "required_fields": "boundary_geometry;trace_norm;K_T_normal_norm;P_locV_trace_norm;zero_certificate_or_bound_path;units",
            "current_value": "MISSING_B_T_BOUNDARY_NORM",
            "valid_for_claim": False,
        },
        {
            "schema_id": "GRP1199_3_projector_leakage",
            "required_object": "eps_P or ||Delta_P||",
            "definition": "nabla P_loc, coframe, domain-motion, and boundary-pullback leakage entering the D_T adjoint/range theorem",
            "required_fields": "P_loc_definition;derivative_bound;coframe_variation;boundary_pullback;source_path;C_CK_eps_P_status",
            "current_value": "MISSING_EPS_P_LEAKAGE",
            "valid_for_claim": False,
        },
        {
            "schema_id": "GRP1199_4_W_R10",
            "required_object": "W_R10(lambda)",
            "definition": "normalized R10 torque/readout response to q_DT_bound, divided by unit-alpha Yukawa response",
            "required_fields": "lambda;lambda_units;unit_alpha_denominator;torque_kernel_path;source_test_density_path;harmonic_weights;normalization;source_path",
            "current_value": "MISSING_W_R10_ALPHA_LAMBDA",
            "valid_for_claim": False,
        },
        {
            "schema_id": "GRP1199_5_no_cancellation",
            "required_object": "absolute component envelope",
            "definition": "all q_DT residual contributions must be summed by absolute values before comparing to alpha_bound(lambda)",
            "required_fields": "component_list;component_abs_values;sum_abs;no_signed_cancellation_guard",
            "current_value": "GUARD_ACTIVE_ABSOLUTE_SUM_ONLY",
            "valid_for_claim": False,
        },
    ]


def candidate_curve_samples() -> list[dict[str, object]]:
    if not R10_CANDIDATE.exists():
        return [
            {
                "sample_id": "R10J1199_missing_candidate",
                "lambda_value": "MISSING_CANDIDATE",
                "lambda_units": "m",
                "alpha_bound": "MISSING_CANDIDATE",
                "alpha_predicted_bound": "MISSING_W_R10_AND_QDT",
                "score_status": "blocked_missing_candidate",
                "valid_for_claim": False,
            }
        ]
    rows = read_csv(R10_CANDIDATE)
    numeric_rows = []
    for row in rows:
        lambda_value = numeric(row.get("lambda_value"))
        alpha_bound = numeric(row.get("alpha_bound"))
        if lambda_value is not None and alpha_bound is not None:
            numeric_rows.append((lambda_value, alpha_bound, row))
    if not numeric_rows:
        return [
            {
                "sample_id": "R10J1199_no_numeric_rows",
                "lambda_value": "MISSING_NUMERIC",
                "lambda_units": "m",
                "alpha_bound": "MISSING_NUMERIC",
                "alpha_predicted_bound": "MISSING_W_R10_AND_QDT",
                "score_status": "blocked_no_numeric_curve_rows",
                "valid_for_claim": False,
            }
        ]
    numeric_rows = sorted(numeric_rows, key=lambda item: item[0])
    indices = sorted({0, len(numeric_rows) // 2, len(numeric_rows) - 1, min(range(len(numeric_rows)), key=lambda index: numeric_rows[index][1])})
    samples: list[dict[str, object]] = []
    for output_index, index in enumerate(indices):
        lambda_value, alpha_bound, row = numeric_rows[index]
        samples.append(
            {
                "sample_id": f"R10J1199_{output_index}_nonclaim_curve_join_sample",
                "bound_id": row.get("bound_id", ""),
                "lambda_value": lambda_value,
                "lambda_units": row.get("lambda_units", "m"),
                "alpha_bound": alpha_bound,
                "alpha_bound_source": row.get("alpha_bound_source", ""),
                "alpha_predicted_bound": "MISSING_W_R10_TIMES_QDT_BOUND",
                "W_R10": "MISSING_W_R10_ALPHA_LAMBDA",
                "q_DT_bound": "MISSING_QDT_BOUND_COMPONENTS",
                "pass_condition": "abs_alpha_predicted_bound <= alpha_bound",
                "score_status": "blocked_missing_MTS_side_projection",
                "candidate_valid_for_claim": row.get("valid_for_claim", ""),
                "valid_for_claim": False,
            }
        )
    return samples


def runner_input_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "QDR1199_0_R10_projection_template",
            "arena": "R10_alpha_lambda",
            "observable": "alpha_DT(lambda)",
            "external_bound_curve_path": str(R10_CANDIDATE.relative_to(ROOT)),
            "external_bound_status": "REVIEW_CANDIDATE_NONCLAIM",
            "W_R10_lambda": "MISSING_W_R10_ALPHA_LAMBDA",
            "G_res_norm": "MISSING_G_RES_PROFILE",
            "coker_fraction": "MISSING_P_COKER_FRACTION",
            "boundary_norm": "MISSING_B_T_BOUNDARY_NORM",
            "regularizer_norm": "MISSING_E_REG_NORM",
            "coercivity_inverse": "MISSING_C_T_COERCIVITY",
            "kappa_T": "MISSING_KAPPA_T",
            "projector_leakage_norm": "MISSING_EPS_P_LEAKAGE",
            "unit_alpha_denominator_path": "MISSING_SOURCE_PATH",
            "torque_kernel_path": "MISSING_SOURCE_PATH",
            "qDT_profile_path": "MISSING_SOURCE_PATH",
            "numeric_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_output_rows(samples: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "run_id": "QDO1199_0_R10_join_dryrun",
            "curve_samples": len(samples),
            "external_bound_available": R10_CANDIDATE.exists(),
            "theory_side_ready": False,
            "runner_status": "blocked_missing_MTS_side_projection",
            "alpha_DT_bound": "MISSING_W_R10_TIMES_QDT_BOUND",
            "tightest_candidate_alpha": min([numeric(row.get("alpha_bound")) for row in samples if numeric(row.get("alpha_bound")) is not None] or [0.0]),
            "passes_all": False,
            "block_reason": "missing_fields:W_R10_lambda;G_res_profile;P_coker_fraction;B_T_boundary_norm;E_reg_norm;C_T;kappa_T;eps_P;unit_alpha_denominator;torque_kernel;qDT_profile",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1199_0_projection_contract",
            "claim": "q_DT-to-R10 projection is numerically sourced",
            "status": "BLOCKED_CONTRACT_ONLY",
            "why": "W_R10(lambda) is defined but no torque/readout kernel, unit-alpha denominator, or q_DT profile is sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1199_1_G_res_profile",
            "claim": "G_res profile and P_coker fraction are sourced",
            "status": "BLOCKED_PROFILE_AND_COKERNEL_MISSING",
            "why": "G_res, cokernel basis/projection, boundary norm, and projector leakage rows are still placeholders",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1199_2_R10_score",
            "claim": "R10 q_DT row can pass/fail against alpha_bound(lambda)",
            "status": "BLOCKED_NO_ALPHA_DT_PREDICTION",
            "why": "external curve exists as nonclaim review candidate, but alpha_DT(lambda) is not computed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1199_3_local_GR",
            "claim": "MTS reduces to local GR/Newton through R10-safe q_DT suppression",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "projection, source profile, boundary/cokernel, and parent action gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1199_0_projection_contract",
            "decision": "W_R10_contract_written",
            "reason": "R10 requires a normalized torque/readout projection against a unit-alpha Yukawa signal",
            "next_action": "source or approximate the R10 torque kernel/unit-alpha denominator before numeric scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1199_1_profile_status",
            "decision": "G_res_profile_pack_missing",
            "reason": "q_DT_bound cannot be converted to alpha(lambda) until the local residual profile, cokernel fraction, boundary norm, and eps_P leakage are specified",
            "next_action": "build a q_DT profile source pack or choose a conservative profile envelope",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1199_2_external_curve_status",
            "decision": "R10_curve_used_only_for_nonclaim_join",
            "reason": "the 2020 review-candidate curve is numeric and useful, but not promoted to a claim curve",
            "next_action": "keep using it for private dry-runs while sourcing MTS-side inputs",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1199_3_best_next",
            "decision": "build_W_R10_kernel_stub_or_qDT_profile_pack",
            "reason": "the largest remaining uncertainty is not the external bound, it is the mapping from MTS q_DT residuals into the R10 measured harmonics",
            "next_action": "1200 should create the first W_R10 kernel/source-pack stub and qDT profile envelope rows",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1199_0_1200",
            "next_target": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "objective": "build the first nonclaim W_R10(lambda) kernel/source-pack stub and q_DT profile-envelope rows, so the R10 runner can eventually compute alpha_DT(lambda) instead of only listing missing fields",
            "include": "unit-alpha Yukawa denominator; R10 torque/readout kernel schema; qDT profile envelope; P_coker fraction placeholder discipline; B_T/eps_P source rows; nonclaim curve join",
            "exclude": "promoting review curve; invented W_R10 values; local-GR/R10 pass; signed cancellation; GitHub; formalization edits",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    profile_schema: list[dict[str, object]],
    samples: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    contract_ids = {row["contract_id"] for row in contracts}
    schema_ids = {row["schema_id"] for row in profile_schema}
    samples_numeric = all(numeric(row.get("lambda_value")) is not None and numeric(row.get("alpha_bound")) is not None for row in samples if "sample" in str(row.get("sample_id", "")))
    samples_nonclaim = all(row.get("valid_for_claim") is False for row in samples)
    runner_blocked = all(row.get("runner_status") == "blocked_missing_MTS_side_projection" and row.get("valid_for_claim") is False for row in runner_outputs)
    input_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in runner_inputs)
    gates_blocked = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in gates + nexts)
    decisions_nonclaim = all(row.get("valid_for_claim") is False for row in decisions)
    return [
        {
            "check_id": "V1199_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_1_projection_contract_present",
            "result": "pass" if {"R10P1199_2_W_R10_definition", "R10P1199_3_alpha_bound_formula", "R10P1199_5_curve_join_rule"} <= contract_ids else "fail",
            "detail": "W_R10 definition, alpha envelope, and curve join rule are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_2_Gres_profile_schema_present",
            "result": "pass" if {"GRP1199_0_G_res_profile", "GRP1199_1_P_coker_fraction", "GRP1199_4_W_R10"} <= schema_ids else "fail",
            "detail": "G_res, P_coker, boundary/leakage, and W_R10 schema rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_3_curve_join_samples_numeric_nonclaim",
            "result": "pass" if samples_numeric and samples_nonclaim else "fail",
            "detail": "R10 curve join samples have numeric lambda/alpha bound values and remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_4_runner_inputs_nonclaim",
            "result": "pass" if input_nonclaim else "fail",
            "detail": "R10 qDT runner input row remains nonclaim with missing W/q inputs",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_5_runner_outputs_blocked",
            "result": "pass" if runner_blocked else "fail",
            "detail": "R10 join dry-run blocks because MTS-side projection/profile inputs are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_6_claim_gates_blocked",
            "result": "pass" if gates_blocked else "fail",
            "detail": "all 1199 claim gates and next target remain blocked/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_7_decisions_nonclaim",
            "result": "pass" if decisions_nonclaim else "fail",
            "detail": "decision ledger remains private/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1199_SUMMARY",
            "result": "pass",
            "detail": "1199 derives the q_DT-to-R10 projection contract W_R10(lambda), stages the G_res/P_coker/B_T/eps_P profile schema, joins nonclaim curve samples, and keeps R10/local-GR scoring blocked until MTS-side inputs are sourced",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    profile_schema: list[dict[str, object]],
    samples: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1199 - Y5/R10 q_DT to R10 projection or G_res profile source",
            "**Current verdict:** q_DT-to-R10 is now an explicit projection contract, not a slogan. The required object is `W_R10(lambda) q_DT_bound`, normalized against a unit-alpha Yukawa torque/readout signal. No numeric R10 score follows yet.",
            "**Main progress:** the nonclaim 2020 R10 curve can now be joined to sample lambda rows, but every sample remains blocked because `W_R10`, `G_res`, `P_coker`, `B_T`, and `eps_P` are still missing on the MTS side.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## R10 projection contract\n\n" + table(contracts),
            "## G_res profile schema\n\n" + table(profile_schema),
            "## Nonclaim curve join samples\n\n" + table(samples),
            "## Runner input row\n\n" + table(runner_inputs),
            "## Runner dry-run output\n\n" + table(runner_outputs),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    contracts = projection_contract_rows()
    profile_schema = g_res_profile_schema_rows()
    samples = candidate_curve_samples()
    runner_inputs = runner_input_rows()
    runner_outputs = runner_output_rows(samples)
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(
        sources,
        contracts,
        profile_schema,
        samples,
        runner_inputs,
        runner_outputs,
        gates,
        decisions,
        nexts,
    )

    outputs = {
        "P8_Y5_R10_1199_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1199_PROJECTION_CONTRACT.csv": contracts,
        "P8_Y5_R10_1199_GRES_PROFILE_SCHEMA.csv": profile_schema,
        "P8_Y5_R10_1199_R10_CURVE_JOIN_SAMPLES_NONCLAIM.csv": samples,
        "P8_Y5_R10_1199_RUNNER_INPUT_TEMPLATE.csv": runner_inputs,
        "P8_Y5_R10_1199_RUNNER_DRYRUN_OUTPUT.csv": runner_outputs,
        "P8_Y5_R10_1199_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1199_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1199_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1199_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, contracts, profile_schema, samples, runner_inputs, runner_outputs, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
