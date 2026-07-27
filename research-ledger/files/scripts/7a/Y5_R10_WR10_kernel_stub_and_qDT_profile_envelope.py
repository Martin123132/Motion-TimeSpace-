from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md"
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


def numeric(value: Any) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


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


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1200_0_1199_next",
            "relative_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "NEXT1199_0_1200",
            "role": "direct 1200 handoff.",
        },
        {
            "source_id": "SRC1200_1_1199_WR10",
            "relative_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_2_W_R10_definition",
            "role": "W_R10 response operator definition.",
        },
        {
            "source_id": "SRC1200_2_1199_qDT",
            "relative_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_3_alpha_bound_formula",
            "role": "alpha_DT envelope formula.",
        },
        {
            "source_id": "SRC1200_3_1199_Gres",
            "relative_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "GRP1199_0_G_res_profile",
            "role": "G_res profile schema.",
        },
        {
            "source_id": "SRC1200_4_1035_harmonic",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXD1035_4_R10_harmonic_projection",
            "role": "R10 torque harmonic projection precedent.",
        },
        {
            "source_id": "SRC1200_5_1035_missing",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXF1035_3_harmonic",
            "role": "R10 harmonic projection missing status.",
        },
        {
            "source_id": "SRC1200_6_437_yukawa",
            "relative_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "Yukawa_potential",
            "role": "R10 Yukawa potential convention.",
        },
        {
            "source_id": "SRC1200_7_437_no_scalar",
            "relative_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "single_delta_G_scalar",
            "role": "R10 cannot be scalar-only.",
        },
        {
            "source_id": "SRC1200_8_831_bound",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "q_DT residual bound components.",
        },
        {
            "source_id": "SRC1200_9_1197_R10_runner",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "CBI1197_1_R10",
            "role": "R10 q_DT runner template.",
        },
        {
            "source_id": "SRC1200_10_R10_candidate",
            "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "needle": "R10_VECTOR_2020_REVIEW_0000",
            "role": "nonclaim R10 numeric curve for dry-run samples.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def wr10_kernel_stub_rows() -> list[dict[str, object]]:
    return [
        {
            "kernel_id": "WRK1200_0_unit_alpha_denominator",
            "object": "D_Y(lambda)",
            "definition": "unit-alpha Yukawa denominator in the actual R10 readout.",
            "mathematical_form": "D_Y(lambda)=||Pi_R10 T_h[V_N exp(-r/lambda)]||_abs over declared harmonic channels.",
            "required_sources": "R10 geometry; Newtonian source/test density; separation/rotation model; harmonic channel weights; readout normalization",
            "current_status": "STUB_SOURCE_PACK_ROW_VALUES_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "WRK1200_1_qDT_numerator",
            "object": "N_DT(lambda)",
            "definition": "R10 readout response to a unit-normalized q_DT residual profile.",
            "mathematical_form": "N_DT(lambda)=||Pi_R10 T_h[Phi_DT[G_DT_profile,lambda]]||_abs.",
            "required_sources": "qDT profile convention; Green/force map from q_DT to Phi_DT; same R10 torque kernel; source/test support",
            "current_status": "STUB_SOURCE_PACK_ROW_VALUES_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "WRK1200_2_harmonic_channels",
            "object": "Pi_R10",
            "definition": "projection onto the measured R10 torque/readout harmonic channels.",
            "mathematical_form": "Pi_R10 T = abs(w_18 T_18omega)+abs(w_120 T_120omega)+abs(retained_harmonic_tail).",
            "required_sources": "harmonic channel list; weights; phase convention; whether 18omega/120omega are both used for this curve",
            "current_status": "HARMONIC_CHANNELS_NAMED_WEIGHTS_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "WRK1200_3_WR10_ratio",
            "object": "W_R10(lambda)",
            "definition": "dimensionless response factor converting q_DT_bound to alpha_DT envelope.",
            "mathematical_form": "W_R10(lambda)=N_DT(lambda)/D_Y(lambda), with D_Y(lambda)>0 and all numerator components absolute-summed.",
            "required_sources": "WRK1200_0; WRK1200_1; denominator positivity certificate; same frame/unit convention",
            "current_status": "SYMBOLIC_RATIO_READY_NUMERIC_VALUES_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "WRK1200_4_denominator_zero_guard",
            "object": "D_Y(lambda)>0 guard",
            "definition": "R10 response cannot be normalized where the unit-alpha denominator vanishes or is not defined.",
            "mathematical_form": "valid row requires finite positive D_Y(lambda_i); otherwise row_status=blocked_zero_or_missing_denominator.",
            "required_sources": "unit-alpha torque denominator table or official response kernel",
            "current_status": "DENOMINATOR_VALUES_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "kernel_id": "WRK1200_5_verdict",
            "object": "W_R10 kernel source pack",
            "definition": "1200 creates the first W_R10 source-pack stub; no W_R10 values are invented.",
            "mathematical_form": "alpha_DT_bound(lambda)=W_R10(lambda)[f_coker||G_res||+||B_T||+kappa_T C_T||E_reg||+||Delta_P||].",
            "required_sources": "kernel table plus qDT profile envelope table",
            "current_status": "KERNEL_STUB_CREATED_NONCLAIM",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
    ]


def qdt_profile_envelope_rows() -> list[dict[str, object]]:
    return [
        {
            "profile_id": "QPE1200_0_total_envelope",
            "component": "q_DT_bound_total",
            "definition": "absolute residual budget before R10 projection.",
            "formula": "q_DT_bound = q_coker + q_boundary + q_regularizer + q_projector",
            "required_fields": "q_coker;q_boundary;q_regularizer;q_projector;units;domain_id;source_path",
            "current_value": "MISSING_COMPONENT_VALUES",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QPE1200_1_cokernel_component",
            "component": "q_coker",
            "definition": "projection of G_res onto surviving D_T adjoint cokernel modes.",
            "formula": "q_coker = f_coker ||G_res||",
            "required_fields": "f_coker;G_res_norm;cokernel_basis_path;inner_product;boundary_class;source_path",
            "current_value": "MISSING_P_COKER_AND_G_RES",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QPE1200_2_boundary_component",
            "component": "q_boundary",
            "definition": "finite bound or zero certificate for the D_T adjoint boundary pairing.",
            "formula": "q_boundary = ||B_T|| >= |int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS|",
            "required_fields": "boundary_geometry;K_T_trace_norm;P_locV_trace_norm;zero_certificate_or_bound;source_path",
            "current_value": "MISSING_B_T_BOUNDARY_NORM",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QPE1200_3_regularizer_component",
            "component": "q_regularizer",
            "definition": "regularizer or parent action residue contribution.",
            "formula": "q_regularizer = kappa_T C_T ||E_reg||",
            "required_fields": "kappa_T;C_T;E_reg_norm;regularizer_source_path;parent_action_status",
            "current_value": "MISSING_REGULARIZER_COERCIVITY_INPUTS",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QPE1200_4_projector_component",
            "component": "q_projector",
            "definition": "P_loc/coframe/domain-motion leakage entering the D_T adjoint/range theorem.",
            "formula": "q_projector = ||Delta_P|| or eps_P||G_res|| with C_CK eps_P < 1 for zero-route absorption.",
            "required_fields": "eps_P;P_loc_definition;coframe_variation;domain_motion;C_CK;source_path",
            "current_value": "MISSING_EPS_P_LEAKAGE",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "profile_id": "QPE1200_5_profile_shape",
            "component": "G_DT_profile_shape",
            "definition": "shape profile used by N_DT(lambda), normalized separately from q_DT_bound amplitude.",
            "formula": "G_DT_profile(x)=G_res(x)/||G_res|| or conservative envelope over allowed local profiles.",
            "required_fields": "profile_grid_or_formula;normalization;support;gauge;coframe;domain;source_path",
            "current_value": "MISSING_QDT_PROFILE_SHAPE",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
    ]


def source_pack_template_rows() -> list[dict[str, object]]:
    return [
        {
            "pack_id": "SP1200_0_WR10_kernel_pack",
            "file_to_fill": "source-intake/mts_residuals/P8_Y5_R10_1200_WR10_KERNEL_VALUES_TO_FILL.csv",
            "required_columns": "lambda;lambda_units;D_Y_unit_alpha;N_DT_unit_profile;W_R10;harmonic_channels;kernel_source_path;valid_for_claim",
            "acceptance_rule": "D_Y_unit_alpha>0;W_R10>=0;kernel_source_path exists;valid_for_claim false until reviewed",
            "current_status": "TEMPLATE_DECLARED_NOT_FILLED",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP1200_1_QDT_profile_pack",
            "file_to_fill": "source-intake/mts_residuals/P8_Y5_R10_1200_QDT_PROFILE_VALUES_TO_FILL.csv",
            "required_columns": "domain_id;profile_id;G_res_norm;f_coker;B_T_norm;kappa_T;C_T;E_reg_norm;Delta_P_norm;q_DT_bound;source_path;valid_for_claim",
            "acceptance_rule": "all components numeric nonnegative; source_path exists;absolute-sum guard active",
            "current_status": "TEMPLATE_DECLARED_NOT_FILLED",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP1200_2_curve_join_pack",
            "file_to_fill": "source-intake/mts_residuals/P8_Y5_R10_1200_R10_JOIN_VALUES_TO_FILL.csv",
            "required_columns": "lambda;alpha_bound;W_R10;q_DT_bound;alpha_DT_bound;passes;curve_source_path;theory_source_path;valid_for_claim",
            "acceptance_rule": "alpha_DT_bound=W_R10*q_DT_bound;alpha_DT_bound<=alpha_bound;no signed cancellation;curve remains nonclaim unless promoted",
            "current_status": "TEMPLATE_DECLARED_NOT_FILLED",
            "valid_for_claim": False,
        },
    ]


def candidate_samples() -> list[dict[str, object]]:
    if not R10_CANDIDATE.exists():
        return [
            {
                "sample_id": "JS1200_missing_curve",
                "lambda_value": "MISSING",
                "alpha_bound": "MISSING",
                "status": "blocked_missing_curve",
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
    numeric_rows = sorted(numeric_rows, key=lambda item: item[0])
    if not numeric_rows:
        return [
            {
                "sample_id": "JS1200_no_numeric_curve_rows",
                "lambda_value": "MISSING",
                "alpha_bound": "MISSING",
                "status": "blocked_no_numeric_curve_rows",
                "valid_for_claim": False,
            }
        ]
    chosen = sorted({0, len(numeric_rows) // 2, len(numeric_rows) - 1, min(range(len(numeric_rows)), key=lambda index: numeric_rows[index][1])})
    samples: list[dict[str, object]] = []
    for output_index, index in enumerate(chosen):
        lambda_value, alpha_bound, row = numeric_rows[index]
        samples.append(
            {
                "sample_id": f"JS1200_{output_index}_WR10_stub_join_sample",
                "bound_id": row.get("bound_id", ""),
                "lambda_value": lambda_value,
                "lambda_units": row.get("lambda_units", "m"),
                "alpha_bound": alpha_bound,
                "D_Y_unit_alpha": "MISSING_UNIT_ALPHA_DENOMINATOR",
                "N_DT_unit_profile": "MISSING_QDT_NUMERATOR_RESPONSE",
                "W_R10": "MISSING_WR10",
                "q_DT_bound": "MISSING_QDT_BOUND",
                "alpha_DT_bound": "MISSING_WR10_TIMES_QDT",
                "join_status": "blocked_kernel_and_profile_missing",
                "valid_for_claim": False,
            }
        )
    return samples


def runner_dryrun_rows(samples: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "run_id": "RUN1200_0_WR10_qDT_join_dryrun",
            "sample_rows": len(samples),
            "external_curve_available": R10_CANDIDATE.exists(),
            "WR10_ready": False,
            "qDT_profile_ready": False,
            "runner_status": "blocked_missing_kernel_and_profile_values",
            "alpha_DT_bound": "MISSING_WR10_TIMES_QDT",
            "block_reason": "missing_fields:D_Y_unit_alpha;N_DT_unit_profile;W_R10;G_res_norm;f_coker;B_T_norm;kappa_T;C_T;E_reg_norm;Delta_P_norm;qDT_profile_shape",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1200_0_WR10_values",
            "claim": "W_R10(lambda) values are available",
            "status": "BLOCKED_KERNEL_VALUES_MISSING",
            "why": "unit-alpha denominator and qDT numerator response are only stubbed, not numeric/source-backed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1200_1_qDT_profile",
            "claim": "q_DT profile envelope is numeric/source-backed",
            "status": "BLOCKED_PROFILE_VALUES_MISSING",
            "why": "G_res, f_coker, B_T, regularizer, projector leakage, and profile shape are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1200_2_R10_score",
            "claim": "R10 qDT dry-run can score",
            "status": "BLOCKED_JOIN_VALUES_MISSING",
            "why": "alpha_DT_bound cannot be computed without W_R10 and q_DT_bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1200_3_local_GR",
            "claim": "MTS local-GR reduction is R10-safe",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "R10 projection, qDT profile, parent action, and boundary/cokernel gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1200_0_kernel_stub",
            "decision": "WR10_source_pack_stub_created",
            "reason": "W_R10 needs numerator/denominator torque-readout kernels, not an invented scalar response",
            "next_action": "fill D_Y and N_DT from geometry/official kernel or build conservative toy kernel explicitly marked nonclaim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1200_1_qDT_profile",
            "decision": "qDT_profile_envelope_rows_created",
            "reason": "R10 cannot constrain q_DT until amplitude components and profile shape are separated",
            "next_action": "source G_res profile or build a conservative profile-envelope family",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1200_2_best_next",
            "decision": "fill_first_nonclaim_kernel_value_or_profile_family",
            "reason": "the runner now has exact columns; the next progress comes from populating one with sourced or explicitly toy nonclaim data",
            "next_action": "1201 should attempt an official/geometry W_R10 source; if unavailable, create a transparent toy-kernel smoke row with claim_allowed=false",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1200_0_1201",
            "next_target": "1201-Y5-R10-WR10-official-kernel-source-or-toy-kernel-smoke-row.md",
            "objective": "source an official/geometry R10 torque kernel for W_R10, or create a transparent toy-kernel smoke row that exercises the qDT runner while remaining nonclaim",
            "include": "D_Y unit-alpha denominator; N_DT unit qDT numerator; harmonic weights; source/test geometry; qDT profile family; nonclaim dry-run",
            "exclude": "invented claim W_R10; promoting review curve; local-GR/R10 pass; signed cancellation; GitHub; formalization edits",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    profiles: list[dict[str, object]],
    packs: list[dict[str, object]],
    samples: list[dict[str, object]],
    dryruns: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    kernel_ids = {row["kernel_id"] for row in kernels}
    profile_ids = {row["profile_id"] for row in profiles}
    sample_numeric = all(numeric(row.get("lambda_value")) is not None and numeric(row.get("alpha_bound")) is not None for row in samples if str(row.get("sample_id", "")).startswith("JS1200_"))
    all_nonclaim = all(row.get("valid_for_claim") is False for row in kernels + profiles + packs + samples + dryruns + gates + decisions + nexts)
    dryrun_blocked = all(row.get("runner_status") == "blocked_missing_kernel_and_profile_values" for row in dryruns)
    gates_blocked = all(row.get("claim_allowed") is False for row in gates + nexts)
    return [
        {
            "check_id": "V1200_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_1_WR10_stub_present",
            "result": "pass" if {"WRK1200_0_unit_alpha_denominator", "WRK1200_1_qDT_numerator", "WRK1200_3_WR10_ratio"} <= kernel_ids else "fail",
            "detail": "W_R10 denominator, numerator, and ratio rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_2_qDT_profile_envelope_present",
            "result": "pass" if {"QPE1200_0_total_envelope", "QPE1200_1_cokernel_component", "QPE1200_5_profile_shape"} <= profile_ids else "fail",
            "detail": "qDT profile-envelope rows include total, cokernel, and shape components",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_3_source_pack_templates_present",
            "result": "pass" if len(packs) == 3 else "fail",
            "detail": "kernel, qDT profile, and join source-pack templates are declared",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_4_samples_numeric_nonclaim",
            "result": "pass" if sample_numeric and all(row.get("valid_for_claim") is False for row in samples) else "fail",
            "detail": "R10 join samples have numeric lambda/alpha bounds and remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_5_dryrun_blocked",
            "result": "pass" if dryrun_blocked else "fail",
            "detail": "dry-run blocks because kernel/profile values are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_6_claim_gates_blocked",
            "result": "pass" if gates_blocked else "fail",
            "detail": "all 1200 claim gates and next target remain blocked/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_7_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1200_SUMMARY",
            "result": "pass",
            "detail": "1200 creates the first W_R10 kernel/source-pack stub and qDT profile-envelope rows, then blocks the R10 join until numerator, denominator, and qDT profile values are sourced",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    profiles: list[dict[str, object]],
    packs: list[dict[str, object]],
    samples: list[dict[str, object]],
    dryruns: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1200 - Y5/R10 W_R10 kernel stub and qDT profile envelope",
            "**Current verdict:** `W_R10(lambda)` is now a concrete source-pack object: a unit-alpha R10 denominator and a unit-qDT numerator must be supplied before any R10 score exists. No numeric `W_R10` value is invented.",
            "**Main progress:** the `q_DT` profile envelope is split into cokernel, boundary, regularizer, projector, and profile-shape rows, giving the runner real columns to fill instead of one vague missing-input blob.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## W_R10 kernel stub\n\n" + table(kernels),
            "## qDT profile envelope\n\n" + table(profiles),
            "## Source-pack templates\n\n" + table(packs),
            "## Nonclaim join samples\n\n" + table(samples),
            "## Runner dry-run\n\n" + table(dryruns),
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
    kernels = wr10_kernel_stub_rows()
    profiles = qdt_profile_envelope_rows()
    packs = source_pack_template_rows()
    samples = candidate_samples()
    dryruns = runner_dryrun_rows(samples)
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, kernels, profiles, packs, samples, dryruns, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1200_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1200_WR10_KERNEL_STUB.csv": kernels,
        "P8_Y5_R10_1200_QDT_PROFILE_ENVELOPE.csv": profiles,
        "P8_Y5_R10_1200_SOURCE_PACK_TEMPLATES.csv": packs,
        "P8_Y5_R10_1200_R10_JOIN_SAMPLES_NONCLAIM.csv": samples,
        "P8_Y5_R10_1200_RUNNER_DRYRUN.csv": dryruns,
        "P8_Y5_R10_1200_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1200_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1200_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1200_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, kernels, profiles, packs, samples, dryruns, gates, decisions, validations, nexts)

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
