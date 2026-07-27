from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md"
NEXT_TARGET = "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md"
STATUS = "Y5_R10_794_tracefree_longitudinal_Khat_solver_formal_flat_patch_pass_curved_parent_amplitude_open_nonclaim"
CLAIM_CEILING = "formal_tracefree_solver_only_no_parent_origin_no_curved_global_solver_no_PPN_bound_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_794_SOURCE_REGISTER.csv"
SOLVER_PATH = RESIDUALS / "P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv"
CURVATURE_BOUND_PATH = RESIDUALS / "P8_Y5_R10_794_CURVATURE_AND_AMPLITUDE_GATES.csv"
PPN_BOUND_PATH = RESIDUALS / "P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_794_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_794_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_794_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_794_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_794_PARENT_KHAT_SOLVER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_794_PPN_BOUND_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_794_LOCAL_GR_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SOLVER_PATH,
    CURVATURE_BOUND_PATH,
    PPN_BOUND_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "793_doc": {
        "path": POST_CHECKPOINT / "793-Y5-R10-Gamma-Khat-balance-source-equation-or-local-bound-inputs.md",
        "needles": ["Current result", "trace-free longitudinal"],
        "role": "immediate 794 handoff",
    },
    "793_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_793_VALIDATION.csv",
        "needles": ["V793_8_longitudinal_selected", "V793_12_no_claim"],
        "role": "prior validation guard",
    },
    "793_routes": {
        "path": RESIDUALS / "P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
        "needles": ["GBS793_1_tracefree_longitudinal_solver", "best_derivation_route"],
        "role": "selected solver route",
    },
    "793_trace": {
        "path": RESIDUALS / "P8_Y5_R10_793_KHAT_TRACE_STATUS_GATE.csv",
        "needles": ["KTS793_1_tracefree_status", "KTS793_3_degrees_of_freedom"],
        "role": "trace-free status input",
    },
    "eq_register_05": {
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["trace-free residual", "q_loc^nu"],
        "role": "q_loc and K_hat source register",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["[K_hat,mu_nu] = L^-2", "[nabla_mu K_hat^{mu nu}] = L^-3"],
        "role": "dimensional ledger",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def solver_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "TLS794_0_solver_definition",
            "statement": "In four dimensions define K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2) g^{mu nu} Box phi.",
            "result": "tracefree_by_construction",
            "derivation_note": "g_mu_nu K_L^{mu nu}=2 Box phi - 2 Box phi=0",
            "missing_before_claim": "parent origin and boundary conditions for phi",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "TLS794_1_flat_divergence",
            "statement": "In a flat/local commuting-derivative patch, partial_mu K_L^{mu nu}=(3/2) partial^nu Box phi.",
            "result": "pass_formal_flat_patch",
            "derivation_note": "partial_mu(2 partial^mu partial^nu phi - 1/2 eta^{mu nu} Box phi)=2 partial^nu Box phi - 1/2 partial^nu Box phi",
            "missing_before_claim": "curved correction and local patch error budget",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "TLS794_2_flat_cancellation",
            "statement": "If Box phi=(2/3) Gamma_eff, then partial_mu K_L^{mu nu}=partial^nu Gamma_eff and q_loc=0 in the flat/local patch.",
            "result": "formal_local_cancellation_candidate",
            "derivation_note": "this is the first non-trace K_hat route that can cancel grad Gamma_eff",
            "missing_before_claim": "show phi/K_L is generated by parent equations rather than chosen to cancel q_loc",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "TLS794_3_curved_correction",
            "statement": "In curved geometry, nabla_mu K_L^{mu nu}=(3/2)nabla^nu Box phi + 2 R^nu_sigma nabla^sigma phi plus convention-dependent curvature/sign terms.",
            "result": "curvature_correction_open",
            "derivation_note": "the flat solver only survives if curvature terms are negligible, cancelled, or included in the source equation",
            "missing_before_claim": "curved operator, sign convention, and Ricci-term control",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "TLS794_4_amplitude_warning",
            "statement": "The solver can cancel divergence while leaving K_L amplitude of order Gamma_eff, so local metric/PPN footprint may remain.",
            "result": "amplitude_not_safe",
            "derivation_note": "q_loc=0 is not identical to K_MTS=0 or local GR",
            "missing_before_claim": "bound K_L, Kbar_tr,loc,00, PPN gamma/beta/alpha_i response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "TLS794_5_solver_verdict",
            "statement": "Adopt trace-free longitudinal K_hat solver as q_loc proof?",
            "result": "not_adopted_formal_candidate_only",
            "derivation_note": "flat/local algebra works, but parent origin, curvature, boundary, and amplitude gates remain open",
            "missing_before_claim": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def curvature_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CAG794_0_curved_operator",
            "gate": "replace flat Box phi=(2/3)Gamma_eff by a covariant operator including Ricci terms",
            "risk_if_missing": "formal cancellation fails outside flat/local patch",
            "status": "missing_curved_solver",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CAG794_1_boundary_conditions",
            "gate": "specify boundary/Green choice for phi",
            "risk_if_missing": "solver is nonunique and can hide nonlocal/source-measure effects",
            "status": "missing_boundary_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CAG794_2_parent_origin",
            "gate": "derive phi or A^nu from parent MTS variables/action",
            "risk_if_missing": "K_L becomes a hand-tuned counterterm",
            "status": "missing_parent_origin",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CAG794_3_amplitude_control",
            "gate": "bound |K_L| and Kbar_tr,loc,00 even when div K_L cancels q_loc",
            "risk_if_missing": "q_loc=0 but metric still fails PPN/Newton",
            "status": "missing_amplitude_bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ppn_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PBR794_0_PPN_metric",
            "object": "K_L/K_hat contribution to metric equation",
            "needed_bound": "delta_gamma, delta_beta, alpha_i below PPN limits",
            "status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "PBR794_1_Newton_source",
            "object": "Kbar_tr,loc,00",
            "needed_bound": "|c^2 Kbar_tr,loc,00| / |4 pi G rho| below local Newton residual tolerance",
            "status": "missing_source_model",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "PBR794_2_orbital",
            "object": "extra acceleration from K_L/T_Q",
            "needed_bound": "planetary/lunar/binary residual map",
            "status": "missing_orbital_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "PBR794_3_clock_R10",
            "object": "clock/R10 projection of carrier stress",
            "needed_bound": "clock redshift and short-range alpha(lambda) projections",
            "status": "missing_clock_R10_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D794_0_formal_solver_retained",
            "decision": "retain trace-free longitudinal solver as formal q_loc cancellation candidate",
            "reason": "flat/local algebra cancels grad Gamma_eff without violating trace-free K_hat",
            "result": "formal_candidate_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D794_1_no_q_zero_claim",
            "decision": "do not claim q_loc=0",
            "reason": "parent origin, curved correction, boundary data, and amplitude/PPN bounds are missing",
            "result": "claim_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D794_2_next_target",
            "decision": "test parent origin or amplitude bound next",
            "reason": "the algebraic cancellation is useless for local GR unless the carrier is physical and locally safe",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "a trace-free longitudinal K_hat solver formally cancels grad Gamma_eff in a flat/local patch via Box phi=(2/3)Gamma_eff, but curved corrections, parent origin, boundary data, and amplitude/PPN safety remain open",
            "hard_blocker": "prove solver comes from parent MTS dynamics and bound its local metric footprint",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    solver: list[dict[str, Any]],
    curvature: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_793_clean = all(validation_clean(number) for number in range(665, 794))
    solver_complete = len(solver) == 6
    tracefree = any(row["step_id"] == "TLS794_0_solver_definition" and row["result"] == "tracefree_by_construction" for row in solver)
    flat_cancel = any(row["step_id"] == "TLS794_2_flat_cancellation" and row["result"] == "formal_local_cancellation_candidate" for row in solver)
    curved_open = any(row["step_id"] == "TLS794_3_curved_correction" and row["result"] == "curvature_correction_open" for row in solver)
    amplitude_warning = any(row["step_id"] == "TLS794_4_amplitude_warning" and row["result"] == "amplitude_not_safe" for row in solver)
    solver_not_adopted = any(row["step_id"] == "TLS794_5_solver_verdict" and row["result"] == "not_adopted_formal_candidate_only" for row in solver)
    curvature_complete = len(curvature) == 4
    ppn_complete = len(ppn) == 4
    ppn_missing = all(row["status"].startswith("missing") for row in ppn)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D794_2_next_target" for row in decisions)
    no_claim = any(row["decision_id"] == "D794_1_no_q_zero_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, solver, curvature, ppn, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V794_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V794_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V794_2_prior_665_793_clean", prior_665_793_clean, "665-793 validation rows have no failures"),
        ("V794_3_solver_complete", solver_complete, "trace-free longitudinal solver rows complete"),
        ("V794_4_tracefree", tracefree, "K_L trace-free construction recorded"),
        ("V794_5_flat_cancel", flat_cancel, "flat/local q_loc cancellation candidate recorded"),
        ("V794_6_curved_open", curved_open, "curved correction still open"),
        ("V794_7_amplitude_warning", amplitude_warning, "amplitude safety warning recorded"),
        ("V794_8_solver_not_adopted", solver_not_adopted, "solver not adopted as proof"),
        ("V794_9_curvature_complete", curvature_complete, "curvature/amplitude gates complete"),
        ("V794_10_ppn_complete", ppn_complete, "PPN bound requirement rows complete"),
        ("V794_11_ppn_missing", ppn_missing, "all PPN/local bound projections missing"),
        ("V794_12_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V794_13_no_claim", no_claim, "q_loc/local GR claim remains blocked"),
        ("V794_14_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V794_15_claim_artifacts_absent", claim_artifacts_absent, "no qloc/parent/PPN/local-GR claim artifact fabricated"),
        ("V794_16_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V794_17_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V794_18_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    solver: list[dict[str, Any]],
    curvature: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 794 - Y5 R10 Tracefree Longitudinal Khat Solver Or PPN Bound

Current result: **there is a formal trace-free local solver for the `q_loc` cancellation problem**. In a flat/local patch, `K_L^{{mu nu}}=2 nabla^mu nabla^nu phi - (1/2)g^{{mu nu}}Box phi` is trace-free, and `Box phi=(2/3)Gamma_eff` gives `div K_L = grad Gamma_eff`. That is promising, but not a proof: curvature corrections, boundary data, parent-action origin, and the metric/PPN amplitude of `K_L` remain open.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Tracefree Longitudinal Solver

{markdown_table(solver, ["step_id", "statement", "result", "derivation_note", "missing_before_claim", "valid_for_claim"])}

## Curvature And Amplitude Gates

{markdown_table(curvature, ["gate_id", "gate", "risk_if_missing", "status", "valid_for_claim"])}

## PPN Bound Requirements

{markdown_table(ppn, ["bound_id", "object", "needed_bound", "status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is the best local mathematical result in this sub-branch so far: the trace-free condition does not kill the cancellation route. But it also does not give local GR by itself, because the object that cancels the divergence may still gravitate. Next we have to ask whether this solver is produced by the parent MTS dynamics, and whether its amplitude is small enough for PPN/Newton.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    solver = solver_rows(generated_utc)
    curvature = curvature_bound_rows(generated_utc)
    ppn = ppn_bound_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, solver, curvature, ppn, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SOLVER_PATH, solver, ["step_id", "statement", "result", "derivation_note", "missing_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(CURVATURE_BOUND_PATH, curvature, ["gate_id", "gate", "risk_if_missing", "status", "valid_for_claim", "generated_utc"])
    write_csv(PPN_BOUND_PATH, ppn, ["bound_id", "object", "needed_bound", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, solver, curvature, ppn, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"794 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
