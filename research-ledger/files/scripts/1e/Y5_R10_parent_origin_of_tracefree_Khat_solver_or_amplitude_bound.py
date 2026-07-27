from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md"
NEXT_TARGET = "796-Y5-R10-KL-amplitude-PPN-budget-or-parent-relaxation-source.md"
STATUS = "Y5_R10_795_parent_origin_missing_tracefree_Khat_solver_kept_as_formal_repair_amplitude_bound_required_nonclaim"
CLAIM_CEILING = "parent_origin_and_amplitude_gate_only_no_adopted_solver_no_PPN_bound_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_795_SOURCE_REGISTER.csv"
ORIGIN_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_795_PARENT_ORIGIN_AUDIT.csv"
OLD_ANSATZ_COMPARISON_PATH = RESIDUALS / "P8_Y5_R10_795_OLD_A_LOC_ANSATZ_COMPARISON.csv"
AMPLITUDE_BOUND_PATH = RESIDUALS / "P8_Y5_R10_795_KL_AMPLITUDE_BOUND_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_795_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_795_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_795_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_795_PARENT_ORIGIN_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_795_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_795_PPN_BOUND_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_795_LOCAL_GR_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    ORIGIN_AUDIT_PATH,
    OLD_ANSATZ_COMPARISON_PATH,
    AMPLITUDE_BOUND_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "794_doc": {
        "path": POST_CHECKPOINT / "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
        "needles": ["Current result", "trace-free local solver"],
        "role": "immediate 795 handoff",
    },
    "794_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_794_VALIDATION.csv",
        "needles": ["V794_5_flat_cancel", "V794_13_no_claim"],
        "role": "prior validation guard",
    },
    "794_solver": {
        "path": RESIDUALS / "P8_Y5_R10_794_TRACEFREE_LONGITUDINAL_SOLVER.csv",
        "needles": ["TLS794_2_flat_cancellation", "TLS794_4_amplitude_warning"],
        "role": "formal solver input",
    },
    "793_routes": {
        "path": RESIDUALS / "P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
        "needles": ["GBS793_1_tracefree_longitudinal_solver", "GBS793_3_relaxation_fixed_point"],
        "role": "source route audit input",
    },
    "eq_register_old_A": {
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["Local longitudinal PPN tensor ansatz", "Box A_loc^nu = q_loc^nu"],
        "role": "older A_loc repair ansatz",
    },
    "red_team_A": {
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["Green-function solution for `A_loc^nu`", "full PPN residual vector"],
        "role": "older red-team warning for A_loc route",
    },
    "spine_q": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["q_loc^nu can be owned algebraically", "physical q_loc profile"],
        "role": "spine status for q_loc route",
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


def origin_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "POA795_0_auxiliary_phi_constraint",
            "candidate_origin": "add auxiliary phi with constraint Box phi=(2/3)Gamma_eff",
            "what_it_would_do": "generates the flat/local trace-free K_L cancellation algebra",
            "failure_or_cost": "closure unless the constraint is derived from symmetry; higher-derivative/stiff dynamics risk",
            "status": "closure_candidate_not_adopted",
            "needed_to_promote": "parent symmetry or Euler equation producing phi naturally",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "POA795_1_relaxation_source",
            "candidate_origin": "open-system relaxation drives K_hat toward div K_hat=grad Gamma_eff",
            "what_it_would_do": "makes q_loc=0 an attractor rather than a hand-set constraint",
            "failure_or_cost": "needs covariant dissipative parent dynamics and transient PPN safety",
            "status": "best_parent_origin_candidate_but_unsigned",
            "needed_to_promote": "relaxation operator, positivity, stability, locality, and amplitude theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "POA795_2_old_A_loc_green_function",
            "candidate_origin": "use existing A_loc Green-function repair ansatz",
            "what_it_would_do": "solves a longitudinal tensor response to q_loc for bounds",
            "failure_or_cost": "existing source treats it as PPN-bound repair route, not a parent derivation",
            "status": "bound_route_not_parent_origin",
            "needed_to_promote": "source equation for A_loc from S_MTS or local tensor operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "POA795_3_moment_closure",
            "candidate_origin": "derive K_L from covariant coarse-grained moment closure",
            "what_it_would_do": "ties solver to motion/pregeometry variables instead of adding phi by hand",
            "failure_or_cost": "moment closure and signature/covariance gates are still missing",
            "status": "possible_but_not_available",
            "needed_to_promote": "closed moment equation whose longitudinal trace-free part equals K_L",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "POA795_4_verdict",
            "candidate_origin": "adopt parent origin for trace-free K_hat solver?",
            "what_it_would_do": "would let q_loc zero theorem become physically meaningful",
            "failure_or_cost": "no source currently signs phi/A/K_L as parent-owned",
            "status": "not_adopted",
            "needed_to_promote": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def old_ansatz_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "compare_id": "OAC795_0_old_vector_A",
            "object": "A_loc^nu Green-function ansatz",
            "relation_to_794": "older vector route solves Box A_loc^nu=q_loc^nu and builds K_L,loc response",
            "advantage": "already connected to PPN-bound language and nonzero q_loc branch",
            "limitation": "does not prove q_loc=0 and is not parent-derived",
            "status": "retain_for_bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "compare_id": "OAC795_1_new_scalar_phi",
            "object": "trace-free scalar phi solver",
            "relation_to_794": "new route cancels grad Gamma_eff in flat/local patch while respecting K_hat trace-free status",
            "advantage": "gives a clean algebraic q_loc cancellation candidate",
            "limitation": "not the same as old A_loc ansatz and lacks parent origin/amplitude safety",
            "status": "retain_for_derivation_test",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "compare_id": "OAC795_2_unification_rule",
            "object": "A_loc/phi solver family",
            "relation_to_794": "treat as longitudinal tensor carrier family, not local-GR proof",
            "advantage": "keeps repair and bound routes in one framework",
            "limitation": "any nonzero carrier must be PPN/orbital/clock/R10 safe",
            "status": "unified_as_nonclaim_carrier_family",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def amplitude_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "KAB795_0_scale_law",
            "quantity": "K_L amplitude",
            "bound_or_law": "if Box phi=(2/3)Gamma_eff on scale L, then phi~Gamma_eff L^2 and K_L~Gamma_eff up to geometry constants",
            "meaning": "divergence cancellation does not make the stress small",
            "status": "formal_scaling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KAB795_1_Newton_fraction",
            "quantity": "epsilon_K = |c^2 Kbar_L,00| / |4 pi G rho|",
            "bound_or_law": "epsilon_K must be below local Newton/PPN tolerance",
            "meaning": "q_loc=0 still fails if K_L contributes too much to the local metric source",
            "status": "missing_numeric_source_model",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KAB795_2_PPN_vector",
            "quantity": "{delta_gamma, delta_beta, alpha1, alpha2, eta_AB, Gdot/G, clock_delta_z}",
            "bound_or_law": "response vector from K_L/A_loc/K_perp must be below observational limits",
            "meaning": "formal cancellation needs a full local-test pass, not only q_loc algebra",
            "status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KAB795_3_Kperp_guard",
            "quantity": "K_perp,loc",
            "bound_or_law": "K_perp must be zero, higher-order suppressed, or explicitly PPN-bounded",
            "meaning": "longitudinal control does not control transverse tensor modes",
            "status": "open_from_prior_work",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KAB795_4_acceptance",
            "quantity": "solver acceptance",
            "bound_or_law": "parent origin plus epsilon_K/PPN/Kperp bounds are all required",
            "meaning": "no local GR claim until both origin and amplitude close",
            "status": "not_satisfied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D795_0_parent_origin_not_found",
            "decision": "do not adopt trace-free solver as parent-derived",
            "reason": "existing corpus supplies repair/bound ansatz, not a signed parent source equation for phi/A/K_L",
            "result": "parent_origin_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D795_1_amplitude_gate_primary",
            "decision": "make K_L amplitude/PPN budget the next gate",
            "reason": "even exact q_loc cancellation can leave a local metric source",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D795_2_no_local_GR_claim",
            "decision": "do not claim local GR/Newton recovery",
            "reason": "parent origin, amplitude, PPN response, and K_perp guard remain open",
            "result": "claim_blocked",
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
            "main_result": "no parent origin for the trace-free Khat solver was found; existing A_loc route is a repair/bound ansatz, so the solver must be treated as a formal carrier until amplitude and PPN budgets close",
            "hard_blocker": "derive parent relaxation/moment source for phi/A/K_L or prove the carrier amplitude is locally PPN/Newton safe",
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
    origins: list[dict[str, Any]],
    old_compare: list[dict[str, Any]],
    amplitude: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_794_clean = all(validation_clean(number) for number in range(665, 795))
    origins_complete = len(origins) == 5
    no_parent_origin = any(row["audit_id"] == "POA795_4_verdict" and row["status"] == "not_adopted" for row in origins)
    old_compare_complete = len(old_compare) == 3
    old_ansatz_bound_route = any(row["compare_id"] == "OAC795_0_old_vector_A" and row["status"] == "retain_for_bounds" for row in old_compare)
    amplitude_complete = len(amplitude) == 5
    scale_law_present = any(row["gate_id"] == "KAB795_0_scale_law" and row["status"] == "formal_scaling" for row in amplitude)
    ppn_missing = any(row["gate_id"] == "KAB795_2_PPN_vector" and row["status"] == "missing_response_matrix" for row in amplitude)
    kperp_open = any(row["gate_id"] == "KAB795_3_Kperp_guard" and row["status"] == "open_from_prior_work" for row in amplitude)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D795_1_amplitude_gate_primary" for row in decisions)
    no_claim = any(row["decision_id"] == "D795_2_no_local_GR_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, origins, old_compare, amplitude, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V795_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V795_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V795_2_prior_665_794_clean", prior_665_794_clean, "665-794 validation rows have no failures"),
        ("V795_3_origins_complete", origins_complete, "parent-origin audit rows complete"),
        ("V795_4_no_parent_origin", no_parent_origin, "solver parent origin not adopted"),
        ("V795_5_old_compare_complete", old_compare_complete, "old A_loc comparison rows complete"),
        ("V795_6_old_ansatz_bound_route", old_ansatz_bound_route, "older A_loc route retained for bounds only"),
        ("V795_7_amplitude_complete", amplitude_complete, "amplitude/PPN gate rows complete"),
        ("V795_8_scale_law_present", scale_law_present, "K_L~Gamma_eff scaling recorded"),
        ("V795_9_ppn_missing", ppn_missing, "PPN response matrix missing"),
        ("V795_10_kperp_open", kperp_open, "K_perp guard remains open"),
        ("V795_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V795_12_no_claim", no_claim, "local GR/Newton claim remains blocked"),
        ("V795_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V795_14_claim_artifacts_absent", claim_artifacts_absent, "no parent-origin/qloc/PPN/local-GR claim artifact fabricated"),
        ("V795_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V795_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V795_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    old_compare: list[dict[str, Any]],
    amplitude: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 795 - Y5 R10 Parent Origin Of Tracefree Khat Solver Or Amplitude Bound

Current result: **the trace-free solver remains useful, but it is not parent-derived yet**. The corpus already had an `A_loc` longitudinal Green-function route, but it was a repair/bound ansatz, not a physical origin for the solver. The strongest next move is therefore amplitude discipline: even if `q_loc` is algebraically cancelled, the carrier `K_L` is generally of order `Gamma_eff`, so it can still fail Newton/PPN unless bounded.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Parent Origin Audit

{markdown_table(origins, ["audit_id", "candidate_origin", "what_it_would_do", "failure_or_cost", "status", "needed_to_promote", "valid_for_claim"])}

## Old A Loc Ansatz Comparison

{markdown_table(old_compare, ["compare_id", "object", "relation_to_794", "advantage", "limitation", "status", "valid_for_claim"])}

## K_L Amplitude Bound Gate

{markdown_table(amplitude, ["gate_id", "quantity", "bound_or_law", "meaning", "status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The solver is not dead, but it has changed job title: it is no longer a proof by itself, it is a candidate carrier that needs an origin and a budget. If MTS can derive a relaxation or moment source for it, excellent. If not, the local branch must show `K_L`, `A_loc`, and `K_perp` are PPN/Newton safe.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    origins = origin_audit_rows(generated_utc)
    old_compare = old_ansatz_rows(generated_utc)
    amplitude = amplitude_bound_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, origins, old_compare, amplitude, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ORIGIN_AUDIT_PATH, origins, ["audit_id", "candidate_origin", "what_it_would_do", "failure_or_cost", "status", "needed_to_promote", "valid_for_claim", "generated_utc"])
    write_csv(OLD_ANSATZ_COMPARISON_PATH, old_compare, ["compare_id", "object", "relation_to_794", "advantage", "limitation", "status", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_BOUND_PATH, amplitude, ["gate_id", "quantity", "bound_or_law", "meaning", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, origins, old_compare, amplitude, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"795 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
