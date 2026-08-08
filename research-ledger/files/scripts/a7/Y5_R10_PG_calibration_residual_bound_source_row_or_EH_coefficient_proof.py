from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_PG_calibration_residual_source_row_and_EH_coefficient_proof_audit_written_nonclaim"
CLAIM_CEILING = "PG_residual_source_row_and_EH_coefficient_audit_only_no_numeric_bound_no_MHref_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "700-Y5-R10-EH-Poisson-coefficient-parent-premise-or-PG-residual-numeric-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "699-Y5-R10-PG-calibration-residual-bound-source-row-or-EH-coefficient-proof.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "458_doc": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "531_doc": ROOT / "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "659_doc": ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "697_doc": ROOT / "697-Y5-R10-MHref-source-normalization-certificate-or-denominator-fill-row.md",
    "698_doc": ROOT / "698-Y5-R10-Hamiltonian-charge-to-Poisson-Gauss-MHref-calibration-or-residual-bound.md",
    "697_validation": RESIDUALS / "P8_Y5_BRR545_697_VALIDATION.csv",
    "698_validation": RESIDUALS / "P8_Y5_BRR545_698_VALIDATION.csv",
    "698_bridge": RESIDUALS / "P8_Y5_R10_698_PG_MHREF_BRIDGE_THEOREM_ATTEMPT.csv",
    "698_residual": RESIDUALS / "P8_Y5_R10_698_CALIBRATION_RESIDUAL_BOUND_ROW.csv",
    "698_obstructions": RESIDUALS / "P8_Y5_R10_698_ARROW_OBSTRUCTION_AUDIT.csv",
    "698_gates": RESIDUALS / "P8_Y5_R10_698_CLAIM_GATE_EVALUATION.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "hsm_scorecard": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "gauss_ppn_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "659_closure": RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
    "697_fill": RESIDUALS / "P8_Y5_R10_697_DENOMINATOR_FILL_ROW.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def first_row_with(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(field) == value:
            return row
    return {}


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {"source_id": source_id, "path": str(path), "exists": bool_text(path.exists()), "role": role, "generated_utc": now}
        for source_id, path, role in [
            ("402_doc", SOURCE_PATHS["402_doc"], "EH/source-normalization parent pair"),
            ("424_doc", SOURCE_PATHS["424_doc"], "same-frame EH-to-Poisson algebra"),
            ("458_doc", SOURCE_PATHS["458_doc"], "Hamiltonian charge to Poisson/Gauss calibration"),
            ("523_doc", SOURCE_PATHS["523_doc"], "source-normalization residual score predecessor"),
            ("529_doc", SOURCE_PATHS["529_doc"], "source-calibrated EH proof stack"),
            ("531_doc", SOURCE_PATHS["531_doc"], "Newton/beta residual envelope"),
            ("657_doc", SOURCE_PATHS["657_doc"], "source-normalization eight-channel vector"),
            ("659_doc", SOURCE_PATHS["659_doc"], "PiM flux obstruction identity"),
            ("696_doc", SOURCE_PATHS["696_doc"], "M_H_ref denominator blocker"),
            ("697_doc", SOURCE_PATHS["697_doc"], "M_H_ref source-normalization certificate"),
            ("698_doc", SOURCE_PATHS["698_doc"], "PG/M_H_ref bridge predecessor"),
            ("697_validation", SOURCE_PATHS["697_validation"], "697 validation gate"),
            ("698_validation", SOURCE_PATHS["698_validation"], "698 validation gate"),
            ("698_bridge", SOURCE_PATHS["698_bridge"], "698 bridge theorem attempt"),
            ("698_residual", SOURCE_PATHS["698_residual"], "698 unfilled calibration residual"),
            ("698_obstructions", SOURCE_PATHS["698_obstructions"], "698 arrow obstruction audit"),
            ("698_gates", SOURCE_PATHS["698_gates"], "698 claim gates"),
            ("pg_contract", SOURCE_PATHS["pg_contract"], "PG0-PG10 calibration contract"),
            ("hilbert_contract", SOURCE_PATHS["hilbert_contract"], "Hilbert monopole calibration contract"),
            ("hsm_scorecard", SOURCE_PATHS["hsm_scorecard"], "source-measure residual scorecard"),
            ("gauss_ppn_test", SOURCE_PATHS["gauss_ppn_test"], "Gauss/PPN test rows"),
            ("source_norm_scorecard", SOURCE_PATHS["source_norm_scorecard"], "source-normalization residual scorecard"),
            ("657_channels", SOURCE_PATHS["657_channels"], "eight retained source-normalization channels"),
            ("659_closure", SOURCE_PATHS["659_closure"], "closed PiM flux conditional identity"),
            ("696_denominator_audit", SOURCE_PATHS["696_denominator_audit"], "M_H_ref denominator audit"),
            ("697_fill", SOURCE_PATHS["697_fill"], "unfilled M_H_ref denominator row"),
        ]
    ]


def eh_coefficient_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("EH699_0_same_frame", "same matter/source/readout metric", "g_obs=g_matter=g_source=g_readout through weak-field order", "conditional_not_parent_derived", "Delta_frame", "cannot promote PG3 coefficient to MTS claim"),
        ("EH699_1_EH_operator", "EH-only local exterior operator", "E_munu=G_munu+Lambda g_munu with nonEH operators zero or bounded", "not_derived_R11_template_only", "epsilon_operator", "Poisson coefficient remains conditional"),
        ("EH699_2_nonrel_source", "ordinary nonrelativistic Hilbert source", "T_00 ~= rho_H c^2 and pressure/stress/source residuals silent or bounded", "conditional_standard_limit", "source_coefficient_residual", "Poisson source may not be only mass density"),
        ("EH699_3_coefficient_algebra", "EH weak-field coefficient algebra", "nabla^2 Phi=(kappa_eff c^4/2)rho_H=4*pi*G_eff rho_H", "algebra_clean_if_prior_premises_hold", "none_if_premises_pass", "positive result: coefficient route is mathematically clean"),
        ("EH699_4_universal_kappa", "constant universal kappa/G", "G_eff=kappa_eff c^4/(8*pi); partial_t,r,A,lambda,frame G_eff=0", "not_parent_derived", "Delta_G", "coefficient can drift by time/range/species/frame"),
        ("EH699_5_no_source_residuals", "no extra source-normalization channels", "mu_obs=G_eff M_H_ref + mu_extra with mu_extra=0 or bounded", "EXACT_SUM_RULE_NON_NUMERIC_CHANNELS_UNFILLED", "mu_extra_over_GM", "hidden channels can contaminate M_H_ref"),
        ("EH699_6_verdict", "PG3 EH-to-Poisson coefficient proof", "EH699_0...EH699_5 pass", "conditional_not_claim_ready", "Delta_Poisson", "best next derivation arrow but not enough for measured-GM alone"),
    ]
    return [
        {
            "audit_id": audit_id,
            "premise": premise,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "residual_if_fail": residual_if_fail,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list("402_doc", "424_doc", "529_doc", "pg_contract", "657_channels"),
            "generated_utc": now,
        }
        for audit_id, premise, mathematical_form, current_status, residual_if_fail, claim_effect in rows
    ]


def pg_residual_source_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("PGR699_0_total", "epsilon_PG_MHref_abs", "abs(GM_orbit/G_ref - M_H_ref)/M_H_ref", "MISSING_ALL_COMPONENTS", "dimensionless", "PGB698_0_epsilon_PG_MHref_abs"),
        ("PGR699_1_charge_current", "Delta_charge_current", "abs(B_xi/G_ref - M_H[Pi_M J_H])/M_H_ref", "MISSING_CHARGE_CURRENT_EQUALITY_OR_BOUND", "dimensionless", "SRC523_0_charge_current_normalization"),
        ("PGR699_2_frame", "Delta_frame", "source/readout/potential frame mismatch contribution", "MISSING_SAME_FRAME_CALIBRATION_OR_BOUND", "dimensionless", "OBS698_2_frame_split"),
        ("PGR699_3_poisson", "Delta_Poisson", "EH/source coefficient deviation from 4*pi*G_ref*rho_H", "MISSING_EH_POISSON_COEFFICIENT_OR_BOUND", "dimensionless", "SRC523_1_Poisson_operator_source"),
        ("PGR699_4_gauss", "Delta_Gauss", "Gauss surface residual from volume/boundary/projector/domain terms", "MISSING_GAUSS_SURFACE_CALIBRATION_OR_BOUND", "dimensionless", "SRC523_2_Gauss_volume_boundary"),
        ("PGR699_5_orbit", "Delta_orbit", "pure inverse-square orbital readout residual including alpha(lambda)/radial hair", "MISSING_ORBITAL_READOUT_OR_ALPHA_LAMBDA_BOUND", "dimensionless", "SRC523_3_orbital_readout"),
        ("PGR699_6_Gref", "Delta_G", "time/range/species/frame drift of G_ref", "MISSING_GREF_DRIFT_SOURCE_RANGE_BOUND", "dimensionless_or_derivative_units", "SRC523_5_Geff_time_or_range_drift"),
        ("PGR699_7_mu_extra", "mu_extra_over_GM", "absolute no-cancellation sum of extra source-normalization channels", "MISSING_MU_EXTRA_ZERO_OR_CHANNEL_BOUNDS", "dimensionless", "SRC523_4_extra_mass_channels_total"),
        ("PGR699_8_beta_guard", "delta_beta_source_guard", "second-order source-stability guard before local-GR promotion", "MISSING_SECOND_ORDER_SOURCE_STABILITY_BOUND", "dimensionless", "SRC523_10_second_order_PPN_source"),
    ]
    return [
        {
            "source_row_id": source_row_id,
            "quantity": quantity,
            "definition": definition,
            "current_status": current_status,
            "required_units": required_units,
            "linked_prior_row": linked_prior_row,
            "required_columns": "quantity;value_or_theorem_zero;units;normalization;source_path;equation_ref;arena_lock;valid_for_claim",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "false",
            "source_paths": source_list("698_residual", "698_obstructions", "source_norm_scorecard"),
            "generated_utc": now,
        }
        for source_row_id, quantity, definition, current_status, required_units, linked_prior_row in rows
    ]


def priority_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("PRI699_0", "EH-to-Poisson coefficient parent premise", "highest", "cleanest algebraic arrow; proving it would reduce Delta_Poisson but not the whole M_H_ref bridge", NEXT_TARGET),
        ("PRI699_1", "PG residual numeric/source fill", "highest", "turns the bridge failure into executable data if derivation stalls", NEXT_TARGET),
        ("PRI699_2", "Gauss surface and orbital readout", "high", "hardest anti-circularity point: cannot borrow observed GM", "701-Y5-R10-Gauss-surface-or-orbital-readout-residual-fill.md"),
        ("PRI699_3", "charge-current equality and PiM flux", "high", "upstream of measured source mass; ties to 659 obstruction identity", "702-Y5-R10-charge-current-equality-or-PiM-flux-bound.md"),
        ("PRI699_4", "universal G and mu_extra channels", "high", "coupling/source-channel silence blocks using any empirical GM denominator", "703-Y5-R10-universal-G-or-mu-extra-channel-bound.md"),
    ]
    return [
        {
            "priority_id": priority_id,
            "target": target,
            "priority": priority,
            "why": why,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for priority_id, target, priority, why, next_action in rows
    ]


def handoff_snapshot_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("SNAP699_0_core_status", "overall", "promising_private_framework_not_claim_ready", "GR-shaped local bridge exists but is conditional; denominator is the main lock"),
        ("SNAP699_1_biggest_gap", "M_H_ref", "blocked", "need parent-owned Hamiltonian charge -> Poisson/Gauss -> orbit equality without borrowing GM"),
        ("SNAP699_2_best_positive", "derivation", "useful", "EH-to-Poisson coefficient algebra is clean if same-frame EH/source premises are derived"),
        ("SNAP699_3_empirical_next", "testing", "not_yet", "do not score PPN/R10 until M_H_ref or epsilon_PG_MHref_abs has sourced rows"),
        ("SNAP699_4_local_GR", "PPN", "blocked_not_dead", "Newton-looking bridge still needs beta/gamma/source-stability followthrough"),
        ("SNAP699_5_next_month_start", "next", NEXT_TARGET, "start by trying EH coefficient premise; if not closed, fill PG residual source rows"),
    ]
    return [
        {
            "snapshot_id": snapshot_id,
            "topic": topic,
            "status": status,
            "short_read": short_read,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for snapshot_id, topic, status, short_read in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("CG699_0_EH_coefficient", "same-frame EH-to-Poisson proof", "conditional_not_claim_ready", "fail_conditional", "Delta_Poisson not cleared"),
        ("CG699_1_residual_source_rows", "all PG residual components sourced or theorem-zero", "MISSING_SOURCE_PATH rows retained", "fail_blocked", "epsilon_PG_MHref_abs not numeric"),
        ("CG699_2_MHref", "M_H_ref denominator claim-ready", "MISSING_CERTIFIED_POSITIVE_M_H_REF", "fail_blocked", "B_TF/e_TF cannot score"),
        ("CG699_3_no_circularity", "no GM_orbit substitution shortcut", "guard_active", "pass_policy", "prevents false Newton proof"),
        ("CG699_4_local_GR", "Newton plus PPN followthrough", "not_reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed_state,
            "result": result,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list("698_gates", "pg_contract", "696_denominator_audit"),
            "generated_utc": now,
        }
        for gate_id, gate, observed_state, result, claim_effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D699_0_EH_coefficient",
            "target": "EH-to-Poisson coefficient proof",
            "result": "best_derivation_target_selected",
            "reason": "PG3 is the cleanest algebraic arrow, but still needs parent premises before claim use",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D699_1_residual_source_pack",
            "target": "epsilon_PG_MHref_abs source row pack",
            "result": "written_unfilled",
            "reason": "if derivation stalls, the exact PG failure can become a source-backed bound instead of a vague blocker",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D699_2_handoff",
            "target": "low-usage handoff",
            "result": "snapshot_written",
            "reason": "monthly usage is nearly gone; snapshot records where the work actually stands",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S699_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "EH-to-Poisson coefficient is the best next proof arrow, and PG residual source rows are now staged but unfilled",
            "hardest_blocker": "parent-owned same-frame EH/source premise plus no source residuals; then Gauss/orbit without GM circularity",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    return all(row.get("valid_for_claim") != "true" for rows in rows_by_name.values() for row in rows)


def validation_rows(
    source_rows: list[dict[str, str]],
    eh_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    priorities: list[dict[str, str]],
    snapshot: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    summary: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failure_counts = {sid: len(validation_failures_for(sid)) for sid in ["697_validation", "698_validation"]}
    pgb698 = read_csv(SOURCE_PATHS["698_residual"])[0]
    rows_by_name = {
        "eh": eh_rows,
        "residual": residual_rows,
        "priorities": priorities,
        "snapshot": snapshot,
        "gates": gates,
        "decisions": decisions,
        "summary": summary,
    }
    residual_missing = len(residual_rows) == 9 and all(row["source_path"] == "MISSING_SOURCE_PATH" for row in residual_rows)
    eh_conditional = len(eh_rows) == 7 and all(row["valid_for_claim"] == "false" for row in eh_rows)
    pgb698_still_unfilled = pgb698.get("M_H_ref") == "MISSING_CERTIFIED_POSITIVE_M_H_REF" and pgb698.get("valid_for_claim") == "false"
    gates_block = len(gates) == 5 and all(row["valid_for_claim"] == "false" for row in gates)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decisions) and summary[0]["next_target"] == NEXT_TARGET
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_699_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_699_EH_COEFFICIENT_PROOF_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_699_PG_RESIDUAL_SOURCE_ROW_PACK.csv",
        RESIDUALS / "P8_Y5_R10_699_ARROW_PRIORITY_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_699_HANDOFF_SNAPSHOT.csv",
        RESIDUALS / "P8_Y5_R10_699_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_699_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_699_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_699_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V699_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V699_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{k}={v}" for k, v in prior_failure_counts.items())),
        ("V699_2_698_residual_still_unfilled", pgb698_still_unfilled, f"PGB698_MHref={pgb698.get('M_H_ref','missing')}"),
        ("V699_3_EH_audit_complete_nonclaim", eh_conditional, f"eh_rows={len(eh_rows)}"),
        ("V699_4_PG_source_rows_unfilled", residual_missing, f"residual_rows={len(residual_rows)}"),
        ("V699_5_priority_and_handoff_written", len(priorities) == 5 and len(snapshot) == 6, f"priority_rows={len(priorities)};snapshot_rows={len(snapshot)}"),
        ("V699_6_claim_gates_block", gates_block, f"gate_rows={len(gates)}"),
        ("V699_7_no_claim_rows_promoted", no_claim_rows, "all 699 generated rows valid_for_claim=false"),
        ("V699_8_next_target_selected", next_selected, NEXT_TARGET),
        ("V699_9_generated_outputs_scoped", scoped_outputs, "all 699 outputs target post-checkpoint-work"),
        ("V699_10_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V699_11_status_nonclaim", "no_MHref" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": now} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, eh_rows, residual_rows, priorities, snapshot, gates, decisions, summary, validation):
    doc = f"""# 699 - Y5 R10 PG Calibration Residual Bound Source Row Or EH Coefficient Proof

## Verdict

699 makes the best low-usage move: it splits the next target into two honest branches.

1. Try to prove the cleanest arrow: the same-frame EH source equation gives the standard Poisson coefficient.
2. If that cannot be parent-signed, fill the PG calibration residual source-row pack instead of pretending `M_H_ref` is known.

The positive result is useful but conditional:

```text
G_munu = kappa_eff T_munu
T_00 ~= rho_H c^2
=> nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4*pi*G_eff rho_H
```

The claim blocker is unchanged: this algebra is not enough until same-frame EH/source premises, constant `G_ref`, no `mu_extra`, Gauss surface calibration, and pure orbital readout are parent-owned or source-bounded.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## EH Coefficient Proof Audit

{markdown_table(eh_rows, ["audit_id", "premise", "current_status", "residual_if_fail", "claim_effect", "valid_for_claim"])}

## PG Residual Source Row Pack

{markdown_table(residual_rows, ["source_row_id", "quantity", "current_status", "required_units", "linked_prior_row", "source_path", "valid_for_claim"])}

## Arrow Priority Decision

{markdown_table(priorities, ["priority_id", "target", "priority", "why", "next_action", "valid_for_claim"])}

## Handoff Snapshot

{markdown_table(snapshot, ["snapshot_id", "topic", "status", "short_read", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    eh_rows = eh_coefficient_audit_rows()
    residual_rows = pg_residual_source_rows()
    priorities = priority_rows()
    snapshot = handoff_snapshot_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, eh_rows, residual_rows, priorities, snapshot, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_699_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_EH_COEFFICIENT_PROOF_AUDIT.csv", eh_rows, ["audit_id", "premise", "mathematical_form", "current_status", "residual_if_fail", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_PG_RESIDUAL_SOURCE_ROW_PACK.csv", residual_rows, ["source_row_id", "quantity", "definition", "current_status", "required_units", "linked_prior_row", "required_columns", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_ARROW_PRIORITY_DECISION.csv", priorities, ["priority_id", "target", "priority", "why", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_HANDOFF_SNAPSHOT.csv", snapshot, ["snapshot_id", "topic", "status", "short_read", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_699_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_699_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, eh_rows, residual_rows, priorities, snapshot, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"eh_rows={len(eh_rows)}")
    print(f"residual_rows={len(residual_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
