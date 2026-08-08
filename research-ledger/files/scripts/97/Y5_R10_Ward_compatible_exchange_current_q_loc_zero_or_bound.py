from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md"
NEXT_TARGET = "792-Y5-R10-geometric-q-loc-cancellation-or-TMTS-residual-bound.md"
STATUS = "Y5_R10_791_matter_exchange_Q_zero_theorem_conditional_geometric_q_loc_still_open_nonclaim"
CLAIM_CEILING = "conditional_Ward_exchange_gate_only_no_parent_signed_matter_universality_no_geometric_q_loc_zero_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_791_SOURCE_REGISTER.csv"
EXCHANGE_TAXONOMY_PATH = RESIDUALS / "P8_Y5_R10_791_EXCHANGE_CURRENT_TAXONOMY.csv"
WARD_ZERO_PATH = RESIDUALS / "P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv"
QLOC_BOUND_PATH = RESIDUALS / "P8_Y5_R10_791_QLOC_BOUND_INTERFACE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_791_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_791_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_791_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_791_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_791_LOCAL_GR_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_791_MATTER_UNIVERSALITY_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_791_PPN_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    EXCHANGE_TAXONOMY_PATH,
    WARD_ZERO_PATH,
    QLOC_BOUND_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "790_doc": {
        "path": POST_CHECKPOINT / "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
        "needles": ["Current result", "Q_nu/q_loc"],
        "role": "immediate 791 handoff",
    },
    "790_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_790_VALIDATION.csv",
        "needles": ["V790_7_Q_gate_primary", "V790_12_no_local_claim"],
        "role": "prior validation guard",
    },
    "790_suppression": {
        "path": RESIDUALS / "P8_Y5_R10_790_LOCAL_SUPPRESSION_GATES.csv",
        "needles": ["LSG790_1_exchange_current_zero_or_bound", "LSG790_0_Ward_compatible_split"],
        "role": "exchange-current gate input",
    },
    "789_ward": {
        "path": RESIDUALS / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
        "needles": ["VWI789_2_exchange_current", "VWI789_3_Bianchi"],
        "role": "Ward/Bianchi input",
    },
    "785_contract": {
        "path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_5_matter_metric_only_coupling", "PMC785_6_parent_action_metric_ownership"],
        "role": "matter universality blocker",
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


def exchange_taxonomy_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "object_id": "ECT791_0_Q_matter",
            "object": "Q_matter_nu = nabla_mu T_matter^mu_nu",
            "meaning": "ordinary-matter nonconservation/exchange current",
            "zero_route": "if S_matter[e,omega,Psi] has no direct Phi_MTS dependence and matter EOM hold, diffeo invariance gives Q_matter_nu=0",
            "if_nonzero": "equivalence-principle or non-geodesic force channel",
            "status": "conditional_zero_theorem_available_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "object_id": "ECT791_1_q_loc_geometric",
            "object": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "meaning": "local geometric/MTS residual current, not automatically matter nonconservation",
            "zero_route": "P_loc(nabla Gamma_eff - div K_hat)=0, or both nabla Gamma_eff and div K_hat vanish locally",
            "if_nonzero": "must be carried by T_MTS divergence or becomes a local metric/source residual",
            "status": "open_primary_geometric_gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "object_id": "ECT791_2_TQ_stress",
            "object": "T_Q_mu_nu with nabla_mu T_Q^mu_nu = -q_loc_nu or -Q_nu",
            "meaning": "stress carrier that can make the total Bianchi identity work",
            "zero_route": "not needed if q_loc=0; otherwise construct with boundary conditions and bound its metric effect",
            "if_nonzero": "PPN/orbital residual stress channel",
            "status": "missing_construction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "object_id": "ECT791_3_boundary_exchange",
            "object": "Q_boundary_nu from source-measure/boundary variation",
            "meaning": "hidden exchange caused by nonlocal/source-measure terms",
            "zero_route": "boundary/source-measure silence theorem or explicit cancellation in total Ward identity",
            "if_nonzero": "fifth-force/source-renormalization channel",
            "status": "missing_boundary_variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ward_zero_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "WZG791_0_total_Ward_identity",
            "claim": "diffeomorphism-invariant total action implies total on-shell conservation",
            "condition": "all fields varied and boundary/source-measure terms included",
            "result": "pass_conditional",
            "missing_before_claim": "explicit covariant S_MTS and boundary terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG791_1_matter_Q_zero",
            "claim": "minimal ordinary matter action gives Q_matter_nu=0 on matter equations of motion",
            "condition": "S_matter depends on MTS only through e,omega[e], owned gauge fields, and constants; no direct psi/Gamma/q_loc dependence",
            "result": "strong_conditional_theorem",
            "missing_before_claim": "parent-signed matter universality/no-spurion certificate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG791_2_q_loc_not_same_as_Q_matter",
            "claim": "geometric q_loc can be nonzero even when Q_matter=0, if it is carried by T_MTS or boundary stress",
            "condition": "nabla T_MTS = -q_loc and total conservation holds",
            "result": "taxonomy_split_required",
            "missing_before_claim": "construct T_Q/T_MTS carrier and bound its metric effect",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG791_3_geometric_q_loc_zero",
            "claim": "q_loc^nu=0 if the local projected Gamma/K_hat balance closes",
            "condition": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})=0 with local boundary conditions",
            "result": "not_derived",
            "missing_before_claim": "Gamma_eff/K_hat source equations or cancellation theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG791_4_bound_fallback",
            "claim": "if q_loc is not zero, local GR can still survive only if its force/metric residual is below bounds",
            "condition": "map q_loc to acceleration, PPN, orbital, clock, or R10 response",
            "result": "bound_interface_needed",
            "missing_before_claim": "response coefficients and real local bound rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qloc_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QBI791_0_acceleration",
            "residual": "spatial Q_i or q_loc_i",
            "observable_map": "a_extra_i ~ Q_i / rho_matter or metric stress response from T_Q",
            "needed_bound": "|a_extra| below orbital/lab fifth-force residuals",
            "status": "missing_response_coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBI791_1_energy_exchange",
            "residual": "Q_0",
            "observable_map": "matter energy drift / clock or local conservation anomaly",
            "needed_bound": "energy-exchange rate below clock/conservation constraints",
            "status": "missing_clock_energy_response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBI791_2_PPN",
            "residual": "T_Q_mu_nu or q_loc carrier stress",
            "observable_map": "gamma,beta,alpha_i shifts",
            "needed_bound": "PPN residual vector below current limits",
            "status": "missing_PPN_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBI791_3_R10",
            "residual": "short-range projected q_loc/source-measure channel",
            "observable_map": "alpha(lambda) fifth-force projection",
            "needed_bound": "real R10 bound curve plus sourced projection coefficient",
            "status": "missing_R10_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D791_0_matter_Q_conditional_zero",
            "decision": "record conditional zero theorem for ordinary matter exchange current",
            "reason": "minimal matter coupling through e/omega is enough to give Q_matter=0 by Ward identity",
            "result": "conditional_theorem_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D791_1_q_loc_still_open",
            "decision": "do not identify geometric q_loc with matter nonconservation",
            "reason": "q_loc may be carried by T_MTS while matter remains conserved, but then it is still a local metric residual",
            "result": "geometric_gate_open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D791_2_next_target",
            "decision": "derive q_loc cancellation or build T_MTS residual bound next",
            "reason": "this is the first remaining obstruction after the matter Ward theorem is separated out",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D791_3_no_claim",
            "decision": "do not claim local GR/Newton recovery",
            "reason": "parent-signed matter universality and geometric q_loc zero/bound are both missing",
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
            "main_result": "ordinary matter exchange Q_matter can be conditionally zero by Ward identity if matter couples only to e/omega, but geometric q_loc remains an open MTS residual that must cancel or be carried by bounded T_MTS stress",
            "hard_blocker": "prove parent-signed matter universality and derive P_loc(nabla Gamma_eff - div K_hat)=0, or bound the resulting T_Q/T_MTS residual",
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
    taxonomy: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_790_clean = all(validation_clean(number) for number in range(665, 791))
    taxonomy_complete = len(taxonomy) == 4
    matter_q_split = any(row["object_id"] == "ECT791_0_Q_matter" for row in taxonomy)
    geometric_q_split = any(row["object_id"] == "ECT791_1_q_loc_geometric" for row in taxonomy)
    ward_complete = len(ward) == 5
    matter_q_conditional = any(row["gate_id"] == "WZG791_1_matter_Q_zero" and row["result"] == "strong_conditional_theorem" for row in ward)
    qloc_not_derived = any(row["gate_id"] == "WZG791_3_geometric_q_loc_zero" and row["result"] == "not_derived" for row in ward)
    bound_interface_complete = len(bounds) == 4
    bounds_missing = all(row["status"].startswith("missing") for row in bounds)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D791_2_next_target" for row in decisions)
    no_claim = any(row["decision_id"] == "D791_3_no_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, taxonomy, ward, bounds, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V791_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V791_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V791_2_prior_665_790_clean", prior_665_790_clean, "665-790 validation rows have no failures"),
        ("V791_3_taxonomy_complete", taxonomy_complete, "exchange-current taxonomy rows complete"),
        ("V791_4_matter_Q_split", matter_q_split, "matter exchange current separated"),
        ("V791_5_geometric_q_split", geometric_q_split, "geometric q_loc separated"),
        ("V791_6_ward_complete", ward_complete, "Ward zero theorem gate rows complete"),
        ("V791_7_matter_Q_conditional", matter_q_conditional, "conditional matter Q zero theorem recorded"),
        ("V791_8_q_loc_not_derived", qloc_not_derived, "geometric q_loc zero not derived"),
        ("V791_9_bound_interface_complete", bound_interface_complete, "q_loc bound interface rows complete"),
        ("V791_10_bounds_missing", bounds_missing, "all q_loc bounds still missing projections"),
        ("V791_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V791_12_no_claim", no_claim, "local GR/Newton claim remains blocked"),
        ("V791_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V791_14_claim_artifacts_absent", claim_artifacts_absent, "no qloc/local-GR/matter-universality/PPN claim artifact fabricated"),
        ("V791_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V791_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V791_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    taxonomy: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 791 - Y5 R10 Ward-Compatible Exchange Current Q Loc Zero Or Bound

Current result: **the exchange-current problem splits into two different beasts**. Ordinary matter exchange `Q_matter` has a strong conditional zero theorem: if matter couples only through `e` and `omega[e]`, Ward identities give `nabla T_matter = 0`. But the geometric MTS residual `q_loc = P_loc(nabla Gamma_eff - div K_hat)` is not automatically killed by that theorem. It must either cancel geometrically or be carried by an explicitly bounded `T_MTS/T_Q` residual.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Exchange Current Taxonomy

{markdown_table(taxonomy, ["object_id", "object", "meaning", "zero_route", "if_nonzero", "status", "valid_for_claim"])}

## Ward Zero Theorem Gate

{markdown_table(ward, ["gate_id", "claim", "condition", "result", "missing_before_claim", "valid_for_claim"])}

## Qloc Bound Interface

{markdown_table(bounds, ["bound_id", "residual", "observable_map", "needed_bound", "status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a nice narrowing. The matter-conservation part is not the monster if the parent action signs minimal matter coupling. The real monster is geometric `q_loc`: prove `P_loc(nabla Gamma_eff - div K_hat)=0`, or build the stress carrier and show its PPN/orbital/clock/R10 footprint is below bounds.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    taxonomy = exchange_taxonomy_rows(generated_utc)
    ward = ward_zero_rows(generated_utc)
    bounds = qloc_bound_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, taxonomy, ward, bounds, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(EXCHANGE_TAXONOMY_PATH, taxonomy, ["object_id", "object", "meaning", "zero_route", "if_nonzero", "status", "valid_for_claim", "generated_utc"])
    write_csv(WARD_ZERO_PATH, ward, ["gate_id", "claim", "condition", "result", "missing_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_BOUND_PATH, bounds, ["bound_id", "residual", "observable_map", "needed_bound", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, taxonomy, ward, bounds, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"791 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
