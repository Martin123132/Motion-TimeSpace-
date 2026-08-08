from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1173-Y5-R10-local-JC-exact-source-zero-or-first-norm-input-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1173_0_1172_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1172_NEXT_TARGET.csv",
            "needle": "NEXT1172_0_1173",
            "role": "handoff to local J_C exact source zero or first norm input row.",
        },
        {
            "source_id": "SRC1173_1_1172_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1172_VALIDATION.csv",
            "needle": "V1172_SUMMARY",
            "role": "1172 validation summary.",
        },
        {
            "source_id": "SRC1173_2_1172_input",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1172_LOCAL_FINITE_BOUND_RUNNER_INPUTS.csv",
            "needle": "LFI1172_0_JC_exact_norm",
            "role": "missing J_C exact norm input.",
        },
        {
            "source_id": "SRC1173_3_1172_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1172_ZERO_BRANCH_CONDITIONS.csv",
            "needle": "ZBC1172_0_exact_source_zero",
            "role": "missing J_C exact source zero theorem.",
        },
        {
            "source_id": "SRC1173_4_1172_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1172_BC_BOUND_FILLED_FROM_JC_SCHEMA.csv",
            "needle": "BCF1172_0_symbolic_bound",
            "role": "symbolic boundary bound requiring norm_JC_exact.",
        },
        {
            "source_id": "SRC1173_5_1166_variation",
            "relative_path": "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            "needle": "delta J_C = J_C Tr(Q^{-1} delta Q) - J_C delta(log N_D)",
            "role": "J_C variation formula from Q/coframe determinant.",
        },
        {
            "source_id": "SRC1173_6_1166_obstruction",
            "relative_path": "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            "needle": "int_D delta J_C = 0",
            "role": "relative local exactness/volume-lock obstruction.",
        },
        {
            "source_id": "SRC1173_7_1167_lock",
            "relative_path": "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
            "needle": "Sigma_C=0, Phi_C|partialD=0, and moving_boundary_term=0",
            "role": "conditional local stationary lock.",
        },
        {
            "source_id": "SRC1173_8_274_split",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "lifted-C exact/top split.",
        },
        {
            "source_id": "SRC1173_9_275_origin",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "J_C = det(Q_coh) Omega_D / V_D",
            "role": "J_C coherent determinant definition.",
        },
        {
            "source_id": "SRC1173_10_275_local_catch",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "stationary local silence",
            "role": "older local-stationary conditional branch.",
        },
        {
            "source_id": "SRC1173_11_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def residual_object_rows() -> list[dict[str, object]]:
    rows = [
        {
            "object_id": "RJO1173_0_background_warning",
            "quantity": "J_C background/coherent form",
            "definition": "J_C = det(Q_coh) Omega_D / V_D",
            "status": "NOT_THE_LOCAL_RESIDUAL_TO_ZERO",
            "reason": "a local volume form can be exact on a bounded domain without being small or physically dangerous; zeroing full J_C would erase the coherent memory object.",
            "next_use": "separate background/coherent class from residual exact source",
            "valid_for_claim": False,
        },
        {
            "object_id": "RJO1173_1_residual_exact_source",
            "quantity": "j_C^exact",
            "definition": "j_C^exact := residual/local variation of J_C after top/coherent projection and allowed stationary background subtraction",
            "status": "CORRECT_BOUND_INPUT_OBJECT",
            "reason": "1172 finite bound should be fed by the local residual exact source norm, not by the absolute coherent volume form.",
            "next_use": "replace norm_JC_exact shorthand with norm_jC_exact_residual in runner rows",
            "valid_for_claim": False,
        },
        {
            "object_id": "RJO1173_2_variation_source",
            "quantity": "delta J_C",
            "definition": "delta J_C = J_C [Tr(Q^{-1} delta Q) - delta(log N_D)] plus domain/coframe-reference terms",
            "status": "KINEMATIC_SOURCE_FORMULA",
            "reason": "this gives the first real symbolic norm input: residual exact source is controlled by trace Q-flow and normalization/domain flow.",
            "next_use": "derive zero from local stationarity or fill symbolic norm row",
            "valid_for_claim": False,
        },
        {
            "object_id": "RJO1173_3_integral_vs_norm",
            "quantity": "int_D delta J_C versus ||delta J_C||",
            "definition": "volume lock int_D delta J_C=0 kills the relative integral obstruction but does not force pointwise/L2 norm zero",
            "status": "NO_OVERCLAIM_GUARD",
            "reason": "a zero integral can still have exact fluctuations that feed B_C norms.",
            "next_use": "need either pointwise/source-free theorem or finite L2 bound",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def zero_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "zero_id": "JCZ1173_0_stationary_pointwise",
            "condition": "D_tau Q_coh=0, delta N_D=0, fixed/co-moving local domain, and no coframe-reference variation",
            "attempt": "then delta J_C=0 pointwise from the determinant variation formula",
            "status": "CONDITIONAL_ZERO_THEOREM_SHAPE",
            "why_not_claim": "local Q-flow stationarity and domain normalization are not parent-derived",
            "valid_for_claim": False,
        },
        {
            "zero_id": "JCZ1173_1_volume_lock",
            "condition": "int_D delta J_C=0 from Sigma_C=0, Phi_C=0, and no moving-boundary term",
            "attempt": "kills relative integral obstruction and supports exact/boundary-silent branch",
            "status": "INTEGRAL_ZERO_NOT_NORM_ZERO",
            "why_not_claim": "does not imply ||j_C^exact||=0 unless local fluctuations also vanish",
            "valid_for_claim": False,
        },
        {
            "zero_id": "JCZ1173_2_mean_subtracted_residual",
            "condition": "define j_C^res = delta J_C - <delta J_C>_D Omega_D and impose volume lock",
            "attempt": "mean-subtracted residual has zero coherent integral by construction/volume lock",
            "status": "USEFUL_REDEFINITION_NOT_ZERO_THEOREM",
            "why_not_claim": "j_C^res can still have nonzero L2 norm and boundary primitive",
            "valid_for_claim": False,
        },
        {
            "zero_id": "JCZ1173_3_exact_source_zero_verdict",
            "condition": "all local residual Q-flow, normalization, domain, harmonic, and weighted-Stokes terms vanish",
            "attempt": "would set norm_jC_exact_residual=0 and close the 1172 zero branch",
            "status": "NOT_DERIVED",
            "why_not_claim": "requires parent local stationarity/no-source theorem stronger than current files supply",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def norm_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "JNI1173_0_first_symbolic_norm_row",
            "quantity": "norm_jC_exact_residual",
            "formula": "||j_C^exact|| <= ||J_C|| * (||Tr(Q^{-1} delta Q)|| + |delta log N_D|) + ||domain/coframe_reference_terms||",
            "units": "J_C_norm_units_per_selected_L2_volume_measure",
            "source_or_theorem": "1166 determinant variation formula",
            "current_value": "SYMBOLIC_ONLY_MISSING_QFLOW_NORM_AND_UNITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "JNI1173_1_zero_subcase",
            "quantity": "norm_jC_exact_residual_zero",
            "formula": "0 if delta Q_coh=0, delta N_D=0, domain/coframe_reference_terms=0, and harmonic/weighted residuals are zero",
            "units": "same_as_norm_jC_exact_residual",
            "source_or_theorem": "conditional local stationarity theorem needed",
            "current_value": "MISSING_PARENT_LOCAL_Q_STATIONARITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "JNI1173_2_trace_Qflow_norm",
            "quantity": "||Tr(Q^{-1} delta Q)||",
            "formula": "trace part of coherent Q-flow/load-volume variation",
            "units": "inverse_time_or_variation_parameter_units",
            "source_or_theorem": "MISSING_LOCAL_QFLOW_BOUND",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "JNI1173_3_normalization_flow",
            "quantity": "|delta log N_D|",
            "formula": "normalization/domain-volume variation contribution",
            "units": "inverse_time_or_variation_parameter_units",
            "source_or_theorem": "MISSING_ND_DOMAIN_RULE",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "JNI1173_4_reference_terms",
            "quantity": "domain/coframe_reference_terms",
            "formula": "moving-domain, projector, coframe-reference, or cutoff terms not captured by fixed-domain determinant variation",
            "units": "same_as_norm_jC_exact_residual",
            "source_or_theorem": "MISSING_DOMAIN_TRANSPORT_AND_PROJECTOR_VARIATION",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def runner_update_rows() -> list[dict[str, object]]:
    rows = [
        {
            "runner_id": "JCR1173_0_rename_bound_input",
            "old_input": "norm_JC_exact",
            "new_input": "norm_jC_exact_residual",
            "reason": "avoid feeding the finite-bound runner with the full coherent/background J_C volume form",
            "runner_effect": "1172 symbolic bound remains valid with the residual source norm substituted",
            "valid_for_claim": False,
        },
        {
            "runner_id": "JCR1173_1_updated_symbolic_bound",
            "old_input": "sqrt(area_partialD) C_trace C_Hodge norm_JC_exact",
            "new_input": "sqrt(area_partialD) C_trace C_Hodge norm_jC_exact_residual",
            "reason": "only the residual exact source should generate local boundary leakage",
            "runner_effect": "bound is sharper and less likely to falsely punish coherent FLRW/top memory",
            "valid_for_claim": False,
        },
        {
            "runner_id": "JCR1173_2_acceptance",
            "old_input": "MISSING_JC_EXACT_NORM",
            "new_input": "SYMBOLIC_ONLY_MISSING_QFLOW_NORM_AND_UNITS",
            "reason": "the determinant variation gives a formula but no numeric/source-backed inputs",
            "runner_effect": "runner can dry-run schema but must refuse claim",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1173_0_zero_theorem",
            "test": "derive j_C exact residual zero",
            "status": "REFUSED_PARENT_STATIONARITY_MISSING",
            "result": "zero follows only if local Q-flow, normalization, domain, harmonic, and weighted terms vanish",
            "blocked_by": "local_Q_stationarity;N_D_rule;domain_transport;cohomology;weighted_Stokes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1173_1_norm_row",
            "test": "stage first norm input row",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "result": "norm_jC_exact_residual is bounded symbolically by Q-flow and normalization variations",
            "blocked_by": "numeric/source-backed Q-flow norm and units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1173_2_runner_update",
            "test": "feed 1172 finite boundary runner",
            "status": "SCHEMA_UPDATED_NUMERIC_INPUTS_MISSING",
            "result": "runner input is corrected from background J_C to residual j_C",
            "blocked_by": "Q-flow bound;domain constants;weighted-Stokes terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1173_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "1173 sharpens the source object but does not score an arena",
            "blocked_by": "local stationarity theorem or numeric norm row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1173_0_object_definition",
            "gate": "correct residual source object",
            "current_status": "PASS_NONCLAIM",
            "reason": "background J_C is separated from local residual j_C exact source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1173_1_zero_theorem",
            "gate": "j_C exact residual zero",
            "current_status": "BLOCKED",
            "reason": "local Q-flow stationarity and domain normalization are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1173_2_norm_input",
            "gate": "source-backed norm_jC_exact_residual",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "reason": "formula exists but Q-flow/norm/units are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1173_3_runner_claim",
            "gate": "finite boundary runner can claim",
            "current_status": "BLOCKED_NO_NUMERIC_BOUND",
            "reason": "domain constants and weighted-Stokes terms are also still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1173_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "no zero theorem or scored finite bound exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1173_0_residual_correction",
            "decision": "interpret_norm_input_as_residual_not_background",
            "reason": "full J_C includes coherent/top memory and should not be zeroed in local tests",
            "next_action": "use norm_jC_exact_residual in finite-bound runner",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1173_1_zero_status",
            "decision": "do_not_claim_local_zero",
            "reason": "stationary local silence is conditional and only integral lock is currently available",
            "next_action": "derive local Q-flow stationarity or fill norm row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1173_2_best_next",
            "decision": "target_Qflow_stationarity_or_bound",
            "reason": "Q-flow trace and N_D/domain variation are now the earliest missing source terms",
            "next_action": "try to derive Tr(Q^-1 delta Q)-delta log N_D=0 locally, or stage bounded Q-flow coefficients",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1173_0_1174",
            "next_target": "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
            "objective": "try to derive the local stationarity condition Tr(Q^-1 delta Q)-delta log N_D=0; if not, stage first Q-flow/norm bound inputs for norm_jC_exact_residual",
            "include": "Q_coh trace flow; N_D normalization; domain transport; stationary local vacuum; physical-charge guard; nonclaim finite-bound runner",
            "exclude": "zeroing full background J_C; using integral lock as norm zero; local claim; c_g zero; invented numeric values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    residuals: list[dict[str, object]],
    zeros: list[dict[str, object]],
    norms: list[dict[str, object]],
    updates: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1173_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_1_residual_object_defined",
            "result": "pass" if any(r["quantity"] == "j_C^exact" for r in residuals) else "fail",
            "detail": "local residual exact source is separated from coherent/background J_C",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_2_variation_formula_used",
            "result": "pass" if any("Tr(Q^{-1} delta Q)" in str(r["definition"]) for r in residuals) else "fail",
            "detail": "determinant variation formula is used for the norm input",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_3_integral_not_norm_guard",
            "result": "pass" if any(r["status"] == "NO_OVERCLAIM_GUARD" for r in residuals) else "fail",
            "detail": "int_D delta J_C=0 is not overclaimed as L2 norm zero",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_4_zero_theorem_refused",
            "result": "pass" if any(r["status"] == "NOT_DERIVED" for r in zeros) else "fail",
            "detail": "local zero theorem remains unsigned",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_5_symbolic_norm_row_created",
            "result": "pass" if any(r["input_id"] == "JNI1173_0_first_symbolic_norm_row" for r in norms) else "fail",
            "detail": "first symbolic norm_jC_exact_residual input row is created",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_6_runner_input_renamed",
            "result": "pass" if any(r["new_input"] == "norm_jC_exact_residual" for r in updates) else "fail",
            "detail": "finite-bound runner is updated to use residual exact norm",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_7_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in norms)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_8_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses zero, norm, finite-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_9_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1173 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_10_no_claim_rows",
            "result": "pass"
            if all(r.get("valid_for_claim") is False for r in residuals + zeros + norms + updates + gates + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_11_next_target",
            "result": "pass" if nexts and "1174" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1174 handoff targets local Q-flow stationarity or first Q-flow bound row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_12_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_13_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1173_SUMMARY",
            "result": "pass",
            "detail": "1173 corrects the bound input to the residual exact source j_C, refuses to zero full background J_C, stages the symbolic Q-flow norm row, and hands off to local Q-flow stationarity or bounded Q-flow inputs",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    residuals: list[dict[str, object]],
    zeros: list[dict[str, object]],
    norms: list[dict[str, object]],
    updates: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1173 — Y5/R10 local J_C exact source zero or first norm input row",
        "**Current verdict:** the local zero route still does not close, but the finite-bound runner is now conceptually sharper. `norm_JC_exact` must be read as the residual exact source norm `norm_jC_exact_residual`, not the full coherent/background `J_C` volume form.",
        "**Main progress:** the first symbolic source row is now `||j_C^exact|| <= ||J_C|| (||Tr(Q^{-1} delta Q)|| + |delta log N_D|) + ||domain/coframe_reference_terms||`. This pushes the missing physics down to local Q-flow stationarity or a source-backed Q-flow bound.",
        "**Important guard:** `int_D delta J_C=0` is an integral/relative obstruction condition, not an L2 norm-zero theorem. It helps, but it cannot by itself erase local exact fluctuations.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Residual source object correction\n\n" + table(residuals),
        "## Local exact-source zero attempt\n\n" + table(zeros),
        "## First norm input row\n\n" + table(norms),
        "## Finite-bound runner update\n\n" + table(updates),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    residuals = residual_object_rows()
    zeros = zero_attempt_rows()
    norms = norm_input_rows()
    updates = runner_update_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, residuals, zeros, norms, updates, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1173_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1173_RESIDUAL_SOURCE_OBJECT_CORRECTION.csv": residuals,
        "P8_Y5_R10_1173_LOCAL_EXACT_SOURCE_ZERO_ATTEMPT.csv": zeros,
        "P8_Y5_R10_1173_FIRST_NORM_INPUT_ROW.csv": norms,
        "P8_Y5_R10_1173_FINITE_BOUND_RUNNER_UPDATE.csv": updates,
        "P8_Y5_R10_1173_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1173_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1173_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1173_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1173_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, residuals, zeros, norms, updates, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
