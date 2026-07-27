from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "792-Y5-R10-geometric-q-loc-cancellation-or-TMTS-residual-bound.md"
NEXT_TARGET = "793-Y5-R10-Gamma-Khat-balance-source-equation-or-local-bound-inputs.md"
STATUS = "Y5_R10_792_q_loc_cancellation_routes_written_no_parent_balance_TMTS_bound_interface_built_nonclaim"
CLAIM_CEILING = "q_loc_cancellation_and_bound_interface_only_no_Gamma_Khat_balance_proof_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_792_SOURCE_REGISTER.csv"
QLOC_CANCELLATION_PATH = RESIDUALS / "P8_Y5_R10_792_QLOC_CANCELLATION_GATE.csv"
TMTS_BOUND_PATH = RESIDUALS / "P8_Y5_R10_792_TMTS_CARRIER_BOUND_INTERFACE.csv"
GAMMA_KHAT_INPUTS_PATH = RESIDUALS / "P8_Y5_R10_792_GAMMA_KHAT_INPUT_REQUIREMENTS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_792_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_792_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_792_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_792_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_792_TMTS_BOUND_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_792_LOCAL_GR_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_792_PPN_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    QLOC_CANCELLATION_PATH,
    TMTS_BOUND_PATH,
    GAMMA_KHAT_INPUTS_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "791_doc": {
        "path": POST_CHECKPOINT / "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md",
        "needles": ["Current result", "geometric q_loc"],
        "role": "immediate 792 handoff",
    },
    "791_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_791_VALIDATION.csv",
        "needles": ["V791_8_q_loc_not_derived", "V791_11_next_target_selected"],
        "role": "prior validation guard",
    },
    "791_ward": {
        "path": RESIDUALS / "P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv",
        "needles": ["WZG791_3_geometric_q_loc_zero", "WZG791_4_bound_fallback"],
        "role": "q_loc zero-or-bound gate input",
    },
    "791_taxonomy": {
        "path": RESIDUALS / "P8_Y5_R10_791_EXCHANGE_CURRENT_TAXONOMY.csv",
        "needles": ["ECT791_1_q_loc_geometric", "ECT791_2_TQ_stress"],
        "role": "exchange taxonomy input",
    },
    "790_suppression": {
        "path": RESIDUALS / "P8_Y5_R10_790_LOCAL_SUPPRESSION_GATES.csv",
        "needles": ["LSG790_1_exchange_current_zero_or_bound", "LSG790_7_Newton_limit_gate"],
        "role": "local suppression gate input",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["q_loc", "physical q_loc profile"],
        "role": "q_loc spine status",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["Q^", "T_matter"],
        "role": "exchange convention",
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


def qloc_cancellation_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "QCG792_0_definition",
            "route": "Define r^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}; q_loc^nu = P_loc r^nu.",
            "zero_condition": "P_loc r^nu = 0",
            "what_it_proves": "geometric q_loc is locally silent",
            "status": "definition_only",
            "missing_before_claim": "owned Gamma_eff, K_hat, P_loc, and boundary conditions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QCG792_1_exact_balance",
            "route": "K_hat balance equation",
            "zero_condition": "nabla_mu K_hat^{mu nu} = nabla^nu Gamma_eff + j_perp^nu with P_loc j_perp^nu=0",
            "what_it_proves": "q_loc=0 by construction if the balance is parent-derived",
            "status": "conditional_tautology_until_parent_signed",
            "missing_before_claim": "Euler/constraint equation for K_hat proving this balance",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QCG792_2_local_silence",
            "route": "constant trace plus transverse stress",
            "zero_condition": "P_loc nabla^nu Gamma_eff=0 and P_loc nabla_mu K_hat^{mu nu}=0 separately",
            "what_it_proves": "q_loc=0 without cancellation fine-tuning",
            "status": "strong_but_not_derived",
            "missing_before_claim": "local fixed-point/screening theorem for Gamma_eff and K_hat",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QCG792_3_projector_kernel",
            "route": "projection kernel silence",
            "zero_condition": "r^nu lies in ker(P_loc), e.g. pure gauge/outside local support under specified boundary conditions",
            "what_it_proves": "q_loc=0 for local observables while residual may exist globally",
            "status": "possible_not_defined",
            "missing_before_claim": "mathematical definition of P_loc and its kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QCG792_4_verdict",
            "route": "adopt q_loc zero theorem?",
            "zero_condition": "one of QCG792_1..3 is parent-signed",
            "what_it_proves": "local exchange-current gate closes",
            "status": "not_adopted",
            "missing_before_claim": "Gamma/K_hat source equation or projector-kernel theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def tmts_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "TCB792_0_divergence_carrier",
            "object": "T_Q^{mu nu}",
            "bound_or_relation": "nabla_mu T_Q^{mu nu} = -q_loc^nu",
            "interpretation": "if q_loc is not zero, it must be carried by an MTS stress to preserve total Bianchi consistency",
            "needed_input": "local Green/divergence inverse with boundary conditions",
            "status": "carrier_relation_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "TCB792_1_stress_scale",
            "object": "||T_Q||",
            "bound_or_relation": "||T_Q|| <= C_div L_loc ||q_loc|| + boundary/source terms",
            "interpretation": "stress scale from inverting a divergence on a local patch of size L_loc",
            "needed_input": "C_div, L_loc, norm definition, boundary/source-measure control",
            "status": "symbolic_bound_interface",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "TCB792_2_metric_response",
            "object": "||h_Q||",
            "bound_or_relation": "||h_Q|| <= C_GR kappa_GR L_loc^2 ||T_Q||",
            "interpretation": "rough weak-field metric response from the stress carrier",
            "needed_input": "C_GR, gauge choice, source geometry, background domain",
            "status": "symbolic_bound_interface",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "TCB792_3_acceleration_response",
            "object": "||a_Q||",
            "bound_or_relation": "||a_Q|| ~ c^2 ||h_Q|| / L_loc or direct non-geodesic response coefficient times ||q_loc||",
            "interpretation": "connects q_loc/T_Q to orbital/lab acceleration residuals",
            "needed_input": "response coefficient and arena-specific bound",
            "status": "missing_numeric_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "TCB792_4_observable_bound",
            "object": "PPN/orbital/clock/R10 response vector",
            "bound_or_relation": "R_obs(q_loc) < R_bound for every local arena",
            "interpretation": "fallback if q_loc zero theorem fails",
            "needed_input": "PPN, orbital, clock, and R10 response matrices plus real source bounds",
            "status": "missing_bound_rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gamma_khat_input_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "GKI792_0_Gamma_eff_equation",
            "needed_object": "source equation for Gamma_eff",
            "why_needed": "determines whether nabla Gamma_eff vanishes, is screened, or is cancelled locally",
            "acceptance_gate": "Euler/Ward equation or local fixed-point theorem",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "GKI792_1_Khat_equation",
            "needed_object": "source/constitutive equation for K_hat^{mu nu}",
            "why_needed": "determines whether div K_hat balances nabla Gamma_eff",
            "acceptance_gate": "parent variation or constraint equation for K_hat",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "GKI792_2_Ploc_definition",
            "needed_object": "local projector P_loc and kernel",
            "why_needed": "needed to know what local experiments actually see",
            "acceptance_gate": "mathematical operator with boundary/support conditions",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "GKI792_3_boundary_conditions",
            "needed_object": "local boundary/source-measure conditions",
            "why_needed": "divergence inversion and projector-kernel routes depend on boundary data",
            "acceptance_gate": "local patch boundary theorem or sourced bound",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "GKI792_4_response_coefficients",
            "needed_object": "q_loc -> observable response coefficients",
            "why_needed": "needed if zero theorem fails and the residual must be bounded",
            "acceptance_gate": "PPN/orbital/clock/R10 response map",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D792_0_zero_not_claimed",
            "decision": "do not claim q_loc=0",
            "reason": "all cancellation routes need parent-signed Gamma/K_hat/P_loc equations",
            "result": "zero_theorem_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D792_1_bound_interface_ready",
            "decision": "retain T_Q/T_MTS carrier bound as fallback",
            "reason": "if q_loc does not cancel, total Bianchi consistency requires a stress carrier whose local metric/force footprint must be bounded",
            "result": "symbolic_bound_ready_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D792_2_next_target",
            "decision": "derive Gamma/K_hat balance source equation or collect local bound inputs next",
            "reason": "this is the smallest missing object for closing or bounding q_loc",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D792_3_no_local_GR_claim",
            "decision": "do not claim local GR/Newton recovery",
            "reason": "q_loc zero/bound remains open",
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
            "main_result": "q_loc cancellation routes are now explicit, but none are parent-signed; fallback T_Q/T_MTS carrier bound is written symbolically",
            "hard_blocker": "derive Gamma_eff/K_hat/P_loc source equations or supply q_loc response coefficients and local bounds",
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
    cancellation: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_791_clean = all(validation_clean(number) for number in range(665, 792))
    cancellation_complete = len(cancellation) == 5
    exact_balance_present = any(row["gate_id"] == "QCG792_1_exact_balance" for row in cancellation)
    zero_not_adopted = any(row["gate_id"] == "QCG792_4_verdict" and row["status"] == "not_adopted" for row in cancellation)
    bound_complete = len(bounds) == 5
    carrier_relation_present = any(row["bound_id"] == "TCB792_0_divergence_carrier" for row in bounds)
    observable_bound_missing = any(row["bound_id"] == "TCB792_4_observable_bound" and row["status"] == "missing_bound_rows" for row in bounds)
    inputs_complete = len(inputs) == 5
    inputs_missing = all(row["status"] == "missing" for row in inputs)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D792_2_next_target" for row in decisions)
    no_claim = any(row["decision_id"] == "D792_3_no_local_GR_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, cancellation, bounds, inputs, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V792_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V792_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V792_2_prior_665_791_clean", prior_665_791_clean, "665-791 validation rows have no failures"),
        ("V792_3_cancellation_complete", cancellation_complete, "q_loc cancellation rows complete"),
        ("V792_4_exact_balance_present", exact_balance_present, "Gamma/K_hat exact balance route recorded"),
        ("V792_5_zero_not_adopted", zero_not_adopted, "q_loc zero theorem not adopted"),
        ("V792_6_bound_complete", bound_complete, "T_Q/T_MTS carrier bound rows complete"),
        ("V792_7_carrier_relation_present", carrier_relation_present, "divergence carrier relation recorded"),
        ("V792_8_observable_bound_missing", observable_bound_missing, "observable bound rows still missing"),
        ("V792_9_inputs_complete", inputs_complete, "Gamma/Khat input rows complete"),
        ("V792_10_inputs_missing", inputs_missing, "all Gamma/Khat/P_loc inputs still missing"),
        ("V792_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V792_12_no_claim", no_claim, "local GR/Newton claim remains blocked"),
        ("V792_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V792_14_claim_artifacts_absent", claim_artifacts_absent, "no qloc/TMTS/local-GR/PPN claim artifact fabricated"),
        ("V792_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V792_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V792_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    cancellation: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 792 - Y5 R10 Geometric Q Loc Cancellation Or TMTS Residual Bound

Current result: **geometric `q_loc` is not yet zero, but the exact ways it could become zero are now explicit**. The cleanest route is a parent-signed balance equation `div K_hat = grad Gamma_eff` up to the kernel of `P_loc`. Without that, `q_loc` must be carried by a stress `T_Q/T_MTS` whose metric, acceleration, PPN, clock, orbital, and R10 footprints must be bounded. This is not a local-GR claim; it is the first honest zero-or-bound fork.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Qloc Cancellation Gate

{markdown_table(cancellation, ["gate_id", "route", "zero_condition", "what_it_proves", "status", "missing_before_claim", "valid_for_claim"])}

## TMTS Carrier Bound Interface

{markdown_table(bounds, ["bound_id", "object", "bound_or_relation", "interpretation", "needed_input", "status", "valid_for_claim"])}

## Gamma Khat Input Requirements

{markdown_table(inputs, ["input_id", "needed_object", "why_needed", "acceptance_gate", "status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The local-GR branch now has a precise hinge. Either the parent theory gives a real `Gamma_eff/K_hat/P_loc` balance that kills `q_loc`, or MTS carries the mismatch in `T_Q/T_MTS` and we must bound that carrier in local arenas. The next target is therefore the source equation for `Gamma_eff` and `K_hat`, not another broad rewrite.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    cancellation = qloc_cancellation_rows(generated_utc)
    bounds = tmts_bound_rows(generated_utc)
    inputs = gamma_khat_input_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, cancellation, bounds, inputs, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_CANCELLATION_PATH, cancellation, ["gate_id", "route", "zero_condition", "what_it_proves", "status", "missing_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(TMTS_BOUND_PATH, bounds, ["bound_id", "object", "bound_or_relation", "interpretation", "needed_input", "status", "valid_for_claim", "generated_utc"])
    write_csv(GAMMA_KHAT_INPUTS_PATH, inputs, ["input_id", "needed_object", "why_needed", "acceptance_gate", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, cancellation, bounds, inputs, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"792 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
