from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
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
            "source_id": "SRC1197_0_1196_next",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "NEXT1196_0_1197",
            "role": "direct 1197 handoff.",
        },
        {
            "source_id": "SRC1197_1_1196_anchor",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_1_dirichlet_anchor_kills_kernel",
            "role": "conditional anchored no-cokernel theorem.",
        },
        {
            "source_id": "SRC1197_2_1196_no_anchor",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_2_no_anchor_no_generic_zero",
            "role": "unanchored zero theorem rejected.",
        },
        {
            "source_id": "SRC1197_3_1196_projector",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_3_projector_perturbation_bound",
            "role": "projector leakage smallness condition.",
        },
        {
            "source_id": "SRC1197_4_1196_boundary",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_0_tracefree_adjoint_boundary",
            "role": "D_T adjoint boundary pairing.",
        },
        {
            "source_id": "SRC1197_5_1196_source_columns",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_4_first_source_columns",
            "role": "first coker/boundary source columns.",
        },
        {
            "source_id": "SRC1197_6_831_bound",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "original cokernel/boundary/regularizer bound.",
        },
        {
            "source_id": "SRC1197_7_832_boundary",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "CB832_3_boundary_residual",
            "role": "flat/curved tracefree solver boundary warning.",
        },
        {
            "source_id": "SRC1197_8_1019_boundary_fail",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "BE1019_6_verdict",
            "role": "boundary exactness does not close current claim.",
        },
        {
            "source_id": "SRC1197_9_1019_projector_pack",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_6_projector_zero_or_bound",
            "role": "projector zero-or-bound source-pack row.",
        },
        {
            "source_id": "SRC1197_10_1170_no_flux",
            "relative_path": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "needle": "PBC1170_1_no_flux_condition",
            "role": "sufficient local no-flux condition not derived.",
        },
        {
            "source_id": "SRC1197_11_1170_bound",
            "relative_path": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "needle": "PBC1170_2_finite_bound",
            "role": "finite boundary-bound fallback precedent.",
        },
        {
            "source_id": "SRC1197_12_1171_natural_fail",
            "relative_path": "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md",
            "needle": "NBC1171_5_verdict",
            "role": "generic natural boundary theorem is too weak.",
        },
        {
            "source_id": "SRC1197_13_1171_first_bound",
            "relative_path": "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md",
            "needle": "FBC1171_0_first_boundary_bound_row",
            "role": "first finite boundary-bound row template.",
        },
        {
            "source_id": "SRC1197_14_1134_strong_conditional",
            "relative_path": "1134-Y5-R10-no-swirl-harmonic-flux-lemma-or-epsilon-profile-runner.md",
            "needle": "THM1134_0_strong_conditional",
            "role": "strong conditional gradient-flow/no-exchange theorem shape.",
        },
        {
            "source_id": "SRC1197_15_1145_profile_template",
            "relative_path": "1145-Y5-R10-parent-branch-functional-for-chiD-or-epsilon-profile-source-row.md",
            "needle": "EPSRC1145_0_profile_source_row",
            "role": "source/profile row precedent after parent branch functional failed.",
        },
        {
            "source_id": "SRC1197_16_756_no_fake_guard",
            "relative_path": "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            "needle": "QCB756_5_no_fake_data_guard",
            "role": "no fake data guard for response/component rows.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def boundary_source_hunt_rows() -> list[dict[str, object]]:
    return [
        {
            "hunt_id": "BCH1197_0_residual_Dirichlet_anchor",
            "candidate_source": "pullback(P_loc V)=0 or V|partialD=0 for residual-sector test vectors",
            "would_close": "kills D_T adjoint boundary pairing and projected conformal-Killing zero modes",
            "corpus_evidence": "1196 states this as a sufficient theorem condition, not a sourced parent boundary rule",
            "status": "SUFFICIENT_CLOSURE_NOT_PARENT_SOURCED",
            "missing_for_claim": "parent action/boundary class deriving residual-sector Dirichlet without deleting physical charges",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_1_normal_no_flux_anchor",
            "candidate_source": "n_mu K_T^(mu nu)=0 on partialD",
            "would_close": "sets B_T[V,K_T]=0 for arbitrary admissible V",
            "corpus_evidence": "1170 records analogous no-flux as sufficient; 1171 warns generic natural BC does not set boundary primitive/value",
            "status": "SUFFICIENT_NOT_DERIVED",
            "missing_for_claim": "specific parent tensor boundary equation, not generic Neumann/natural wording",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_2_generic_natural_boundary",
            "candidate_source": "ordinary free-boundary/natural variation",
            "would_close": "might have killed boundary terms if the conjugate momentum equaled the needed primitive/pairing",
            "corpus_evidence": "1171 explicitly rejects generic natural BC as strong enough for boundary primitive zero",
            "status": "REJECTED_AS_GENERAL_THEOREM",
            "missing_for_claim": "a special D_T parent boundary action whose natural equation is exactly B_T=0",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_3_gradient_flow_no_exchange_analogy",
            "candidate_source": "positive mobility plus no-source stationarity plus no-exchange boundary",
            "would_close": "provides a model of how a parent action could kill local flux without plateau axiom",
            "corpus_evidence": "1134 has a strong conditional theorem, but for epsilon/domain flux and still not parent-signed",
            "status": "ANALOGY_ONLY_NOT_DT_SOURCE",
            "missing_for_claim": "D_T-specific mobility/elliptic energy and tracefree tensor boundary equation",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_4_boundary_exactness_projector",
            "candidate_source": "boundary exactness/projector orthogonality",
            "would_close": "could set boundary/projector components to zero if same boundary class is certified",
            "corpus_evidence": "1019 keeps exactness/projector route as fail_current_claim and source-pack fallback",
            "status": "NOT_CLOSED_USE_SOURCE_PACK",
            "missing_for_claim": "corner-free/harmonic-free boundary class and parent-signed projector zero or finite bound",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_5_rigid_mode_quotient",
            "candidate_source": "quotient out translations, rotations, dilations, and special conformal representatives",
            "would_close": "removes flat/frozen conformal-Killing cokernel modes without boundary anchoring",
            "corpus_evidence": "1196 identifies the need, but no parent quotient map for D_T modes is sourced",
            "status": "QUOTIENT_SOURCE_MISSING",
            "missing_for_claim": "parent q map proving these modes are gauge/representative directions and not physical residuals",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "BCH1197_6_verdict",
            "candidate_source": "parent-owned D_T boundary/no-cokernel certificate",
            "would_close": "would permit q_DT zero theorem instead of finite residual budget",
            "corpus_evidence": "no current source closes Dirichlet, no-flux, quotient, exactness, or projector clauses for D_T",
            "status": "BOUNDARY_SOURCE_NOT_FOUND_MOVE_TO_RUNNER",
            "missing_for_claim": "parent boundary/source theorem or numeric finite-bound rows",
            "valid_for_claim": False,
        },
    ]


def ck_anchor_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CKC1197_0_kernel_modes",
            "requirement": "identify all projected conformal-Killing-like cokernel modes in the local domain",
            "acceptance_rule": "basis/path exists for Ker(D_T^dagger) or a theorem proves it is empty after boundary/quotient restrictions",
            "current_status": "MISSING_COKERNEL_BASIS_OR_EMPTY_KERNEL_CERTIFICATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "CKC1197_1_anchor_or_quotient",
            "requirement": "remove rigid/projected CK modes by parent-owned boundary anchor or quotient map",
            "acceptance_rule": "same parent action supplies V|partialD=0, normal no-flux, or q-mode gauge quotient without physical charge loss",
            "current_status": "MISSING_PARENT_ANCHOR_OR_QUOTIENT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "CKC1197_2_ck_korn_constant",
            "requirement": "provide coercive CK/Korn inequality on the selected domain",
            "acceptance_rule": "finite C_CK or theorem-zero certificate in the same norm/domain as q_DT_bound",
            "current_status": "MISSING_C_CK_SOURCE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "CKC1197_3_projector_leakage",
            "requirement": "control nabla P_loc and boundary pullback leakage",
            "acceptance_rule": "eps_P source with C_CK*eps_P<1, or parent exact-zero proof for projector leakage",
            "current_status": "MISSING_EPS_P_OR_PROJECTOR_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "CKC1197_4_boundary_pairing",
            "requirement": "zero or source-bound B_T[V,K_T]",
            "acceptance_rule": "B_T=0 certificate or numeric trace/source norm in same units as G_res",
            "current_status": "MISSING_BOUNDARY_NORM_OR_ZERO_CERTIFICATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "CKC1197_5_observable_response",
            "requirement": "map q_DT_bound into local tests",
            "acceptance_rule": "W_PPN, W_R10(lambda), W_clock, and W_orbital source rows plus external bounds",
            "current_status": "MISSING_ARENA_RESPONSE_OPERATORS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_input_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    arenas = [
        ("CBI1197_0_PPN", "PPN_gamma_beta", "Delta_PPN_DT", "gamma_beta_bound_source_path"),
        ("CBI1197_1_R10", "R10_alpha_lambda", "alpha_DT(lambda)", "alpha_lambda_bound_curve_path"),
        ("CBI1197_2_clock", "clock_redshift_timing", "Delta_clock_DT", "clock_bound_source_path"),
        ("CBI1197_3_orbital", "orbital_ephemeris", "Delta_orbital_DT", "orbital_bound_source_path"),
    ]
    for row_id, arena, observable, bound_path_field in arenas:
        rows.append(
            {
                "row_id": row_id,
                "arena": arena,
                "observable": observable,
                "G_res_norm": "MISSING_G_RES_PROFILE",
                "coker_fraction": "MISSING_P_COKER_FRACTION",
                "boundary_norm": "MISSING_B_T_BOUNDARY_NORM",
                "regularizer_norm": "MISSING_E_REG_NORM",
                "coercivity_inverse": "MISSING_C_T_COERCIVITY",
                "kappa_T": "MISSING_KAPPA_T",
                "projector_leakage_norm": "MISSING_EPS_P_LEAKAGE",
                "response_norm": f"MISSING_W_{arena.upper()}",
                "observable_limit": f"MISSING_{bound_path_field.upper()}",
                "P_coker_basis_path": "MISSING_SOURCE_PATH",
                "G_res_profile_path": "MISSING_SOURCE_PATH",
                "boundary_condition_source_path": "MISSING_SOURCE_PATH",
                "parent_action_source_path": "MISSING_SOURCE_PATH",
                "projector_leakage_source_path": "MISSING_SOURCE_PATH",
                "response_source_path": "MISSING_SOURCE_PATH",
                "observable_bound_source_path": "MISSING_SOURCE_PATH",
                "numeric_ready": False,
                "valid_for_claim": False,
            }
        )
    return rows


def parse_numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        value_float = float(value)
        return value_float if math.isfinite(value_float) else None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper().startswith("NONEXECUTABLE"):
        return None
    try:
        value_float = float(text)
    except ValueError:
        return None
    return value_float if math.isfinite(value_float) else None


def source_path_ok(value: Any) -> bool:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return False
    path = Path(text)
    if not path.is_absolute():
        path = ROOT / text
    return path.exists()


def run_bound_rows(inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    numeric_fields = [
        "G_res_norm",
        "coker_fraction",
        "boundary_norm",
        "regularizer_norm",
        "coercivity_inverse",
        "kappa_T",
        "projector_leakage_norm",
        "response_norm",
        "observable_limit",
    ]
    path_fields = [
        "P_coker_basis_path",
        "G_res_profile_path",
        "boundary_condition_source_path",
        "parent_action_source_path",
        "projector_leakage_source_path",
        "response_source_path",
        "observable_bound_source_path",
    ]
    outputs: list[dict[str, object]] = []
    for row in inputs:
        missing_numeric = [field for field in numeric_fields if parse_numeric(row.get(field)) is None]
        missing_paths = [field for field in path_fields if not source_path_ok(row.get(field))]
        if missing_numeric or missing_paths:
            outputs.append(
                {
                    "row_id": row["row_id"],
                    "arena": row["arena"],
                    "runner_status": "blocked_missing_inputs",
                    "q_cokernel_bound": "MISSING_INPUT",
                    "q_boundary_bound": "MISSING_INPUT",
                    "q_regularizer_bound": "MISSING_INPUT",
                    "q_projector_bound": "MISSING_INPUT",
                    "q_total_bound": "MISSING_INPUT",
                    "observable_bound": "MISSING_INPUT",
                    "observable_limit": row["observable_limit"],
                    "passes_all": False,
                    "block_reason": "missing_fields:" + ";".join(missing_numeric + missing_paths),
                    "no_cancellation_guard": "ACTIVE_ABSOLUTE_SUM_REQUIRED",
                    "valid_for_claim": False,
                }
            )
            continue
        values = {field: abs(parse_numeric(row[field]) or 0.0) for field in numeric_fields}
        q_cokernel = values["coker_fraction"] * values["G_res_norm"]
        q_boundary = values["boundary_norm"]
        q_regularizer = values["kappa_T"] * values["coercivity_inverse"] * values["regularizer_norm"]
        q_projector = values["projector_leakage_norm"]
        q_total = q_cokernel + q_boundary + q_regularizer + q_projector
        observable_bound = values["response_norm"] * q_total
        passes_all = observable_bound <= values["observable_limit"]
        outputs.append(
            {
                "row_id": row["row_id"],
                "arena": row["arena"],
                "runner_status": "computed_nonclaim" if passes_all else "computed_fail",
                "q_cokernel_bound": q_cokernel,
                "q_boundary_bound": q_boundary,
                "q_regularizer_bound": q_regularizer,
                "q_projector_bound": q_projector,
                "q_total_bound": q_total,
                "observable_bound": observable_bound,
                "observable_limit": values["observable_limit"],
                "passes_all": passes_all,
                "block_reason": "computed rows still require review before promotion",
                "no_cancellation_guard": "ACTIVE_ABSOLUTE_SUM_USED",
                "valid_for_claim": False,
            }
        )
    return outputs


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1197_0_boundary_source",
            "claim": "parent-owned D_T boundary/no-cokernel condition is sourced",
            "status": "BLOCKED_SOURCE_NOT_FOUND",
            "why": "Dirichlet/no-flux/quotient/exactness clauses remain sufficient or rejected, not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1197_1_cokernel_zero",
            "claim": "P_coker(D_T)G_res=0",
            "status": "BLOCKED_COKERNEL_BASIS_OR_ZERO_CERTIFICATE_MISSING",
            "why": "conformal-Killing-like modes are not removed by a sourced anchor or quotient map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1197_2_bound_runner_claim",
            "claim": "finite q_DT_bound passes local tests",
            "status": "BLOCKED_RUNNER_INPUTS_MISSING",
            "why": "all arena rows require source-backed G_res, P_coker, B_T, E_reg, eps_P, response, and external bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1197_3_local_GR",
            "claim": "MTS reduces to local GR/Newton through D_T",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "boundary source and finite-bound runner remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1197_0_source_hunt",
            "decision": "parent_boundary_source_not_found",
            "reason": "sufficient boundary/anchor conditions exist, but current corpus does not sign them for D_T",
            "next_action": "either derive the D_T-specific parent boundary action or fill finite-bound input rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1197_1_natural_boundary",
            "decision": "generic_natural_BC_rejected",
            "reason": "generic natural boundary conditions control conjugate momentum, not necessarily the D_T pairing needed for q suppression",
            "next_action": "do not use generic naturalness as a local-GR shortcut",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1197_2_runner",
            "decision": "first_DT_cokernel_boundary_runner_installed",
            "reason": "the residual budget is now executable once real arena/source inputs are supplied",
            "next_action": "choose one arena, preferably R10 or PPN, and fill the first real source row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1197_3_best_next",
            "decision": "parent_anchor_or_first_real_input",
            "reason": "derivation remains preferred, but the runner prevents an unfalsifiable closure if the derivation keeps failing",
            "next_action": "1198 should try D_T parent anchor once more, then fill R10/PPN inputs if no source appears",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1197_0_1198",
            "next_target": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "objective": "make one more targeted attempt to derive/source the D_T parent boundary anchor; if not found, fill the first real nonclaim R10/PPN input row for the q_DT bound runner",
            "include": "D_T-specific boundary action; residual-sector anchor; quotient map for CK modes; C_CK/eps_P; first R10 or PPN source row; strict no-claim validation",
            "exclude": "generic natural-boundary shortcut; unanchored zero; local-GR pass; fake numeric inputs; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    source_hunt: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    output_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    source_statuses = {row["status"] for row in source_hunt}
    all_inputs_nonclaim = all(row.get("valid_for_claim") is False for row in input_rows)
    all_outputs_blocked = all(row["runner_status"] == "blocked_missing_inputs" and row.get("valid_for_claim") is False for row in output_rows)
    all_gates_blocked = all(row.get("claim_allowed") is False for row in gates + nexts)
    contract_blocked = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in contract_rows)
    decisions_nonclaim = all(row.get("valid_for_claim") is False for row in decisions)
    return [
        {
            "check_id": "V1197_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_1_boundary_source_hunt_done",
            "result": "pass" if "BOUNDARY_SOURCE_NOT_FOUND_MOVE_TO_RUNNER" in source_statuses else "fail",
            "detail": "boundary/no-cokernel source hunt records that no parent D_T source currently closes",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_2_contract_rows_blocked",
            "result": "pass" if contract_blocked and len(contract_rows) >= 6 else "fail",
            "detail": "CK/Korn anchor, projector leakage, boundary, and response requirements are explicit and blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_3_runner_inputs_nonclaim",
            "result": "pass" if all_inputs_nonclaim and len(input_rows) == 4 else "fail",
            "detail": "PPN, R10, clock, and orbital input templates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_4_runner_outputs_refuse_missing",
            "result": "pass" if all_outputs_blocked and len(output_rows) == 4 else "fail",
            "detail": "runner refuses every arena row because required numeric/source inputs are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_5_claim_gates_blocked",
            "result": "pass" if all_gates_blocked and all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all 1197 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_6_decisions_nonclaim",
            "result": "pass" if decisions_nonclaim else "fail",
            "detail": "decision ledger remains private/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1197_0_1198" else "fail",
            "detail": "1198 handoff targets parent anchor source or first real bound input fill",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1197_SUMMARY",
            "result": "pass",
            "detail": "1197 fails to source a parent-owned D_T boundary/no-cokernel theorem, rejects generic natural-boundary shortcut, installs a strict nonclaim PPN/R10/clock/orbital q_DT bound runner, and hands off to parent-anchor or first-real-input work",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    source_hunt: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    output_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1197 - Y5/R10 D_T boundary condition source or cokernel-bound runner",
            "**Current verdict:** no parent-owned D_T boundary/no-cokernel source is found in the current corpus. The route stays alive, but only as a conditional theorem or as a finite residual-bound runner.",
            "**Main progress:** generic natural-boundary wording is explicitly rejected as too weak, and the first strict PPN/R10/clock/orbital `q_DT` runner is installed. It refuses every row until real source-backed inputs exist.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Boundary source hunt\n\n" + table(source_hunt),
            "## CK/Korn anchor contract\n\n" + table(contract_rows),
            "## Cokernel-bound input template\n\n" + table(input_rows),
            "## Cokernel-bound runner output\n\n" + table(output_rows),
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
    source_hunt = boundary_source_hunt_rows()
    contract_rows = ck_anchor_contract_rows()
    input_rows = bound_input_rows()
    output_rows = run_bound_rows(input_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(
        sources,
        source_hunt,
        contract_rows,
        input_rows,
        output_rows,
        gates,
        decisions,
        nexts,
    )

    outputs = {
        "P8_Y5_R10_1197_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1197_BOUNDARY_SOURCE_HUNT.csv": source_hunt,
        "P8_Y5_R10_1197_CK_ANCHOR_CONTRACT.csv": contract_rows,
        "P8_Y5_R10_1197_COKERNEL_BOUND_INPUT_TEMPLATE.csv": input_rows,
        "P8_Y5_R10_1197_COKERNEL_BOUND_RUNNER_OUTPUT.csv": output_rows,
        "P8_Y5_R10_1197_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1197_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1197_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1197_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, source_hunt, contract_rows, input_rows, output_rows, gates, decisions, validations, nexts)

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
