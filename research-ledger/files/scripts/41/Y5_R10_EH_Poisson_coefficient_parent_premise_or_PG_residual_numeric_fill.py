from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_EH_Poisson_coefficient_algebra_certificate_written_parent_premises_unsigned_Delta_Poisson_fill_unfilled_nonclaim"
CLAIM_CEILING = "EH_Poisson_coefficient_algebra_only_no_Delta_Poisson_value_no_MHref_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "701-Y5-R10-Delta-Poisson-source-coefficient-fill-or-Gauss-orbit-bridge.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "700-Y5-R10-EH-Poisson-coefficient-parent-premise-or-PG-residual-numeric-fill.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "425_doc": ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "531_doc": ROOT / "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "699_doc": ROOT / "699-Y5-R10-PG-calibration-residual-bound-source-row-or-EH-coefficient-proof.md",
    "699_validation": RESIDUALS / "P8_Y5_BRR545_699_VALIDATION.csv",
    "699_eh_audit": RESIDUALS / "P8_Y5_R10_699_EH_COEFFICIENT_PROOF_AUDIT.csv",
    "699_pg_source_rows": RESIDUALS / "P8_Y5_R10_699_PG_RESIDUAL_SOURCE_ROW_PACK.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "gauss_ppn_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "402_doc": "EH/source-normalization parent pair",
        "424_doc": "same-frame EH-to-Poisson algebra",
        "425_doc": "EH retained ledger and source-normalization test plan",
        "429_doc": "Ward/Bianchi exchange owner for Poisson source",
        "529_doc": "source-calibrated EH proof stack",
        "531_doc": "Newton/beta residual envelope",
        "655_doc": "EH operator selection gate",
        "699_doc": "immediate predecessor",
        "699_validation": "699 validation gate",
        "699_eh_audit": "699 EH coefficient proof audit",
        "699_pg_source_rows": "699 PG residual source-row pack",
        "pg_contract": "PG0-PG10 calibration contract",
        "gauss_ppn_test": "Gauss/PPN readout tests",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
        "696_denominator_audit": "M_H_ref denominator blocker",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def algebra_certificate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("ALG700_0_field_equation", "same-frame EH field equation", "G_munu[g_obs]+Lambda g_obs_munu=kappa_eff T_munu[g_obs]", "algebra_premise_written", "requires same-frame parent premise"),
        ("ALG700_1_weak_metric", "weak static metric convention", "g_00=-1+2 Phi/c^2 + O(c^-4)", "standard_limit", "requires observed metric/readout lock"),
        ("ALG700_2_source_limit", "nonrelativistic Hilbert source", "T_00 ~= rho_H c^2", "conditional_standard_limit", "requires pressure/stress/source residuals silent or bounded"),
        ("ALG700_3_linearized_00", "linearized 00 Einstein tensor", "G_00 ~= 2 nabla^2 Phi/c^2", "algebra_written", "sign/convention fixed to 424/402"),
        ("ALG700_4_poisson_coefficient", "Poisson coefficient", "nabla^2 Phi=(kappa_eff c^4/2)rho_H=4*pi*G_eff rho_H", "algebra_clean_if_Geff_defined", "G_eff=kappa_eff c^4/(8*pi)"),
        ("ALG700_5_delta_poisson_definition", "coefficient residual", "Delta_Poisson := abs((kappa_eff c^4)/(8*pi*G_ref)-1)+abs(source_residuals)/(4*pi*G_ref*rho_H)", "definition_written_not_filled", "nonclaim executable residual"),
    ]
    return [
        {
            "algebra_id": algebra_id,
            "step": step,
            "mathematical_form": form,
            "status": status,
            "condition": condition,
            "valid_for_claim": "false",
            "source_paths": source_list("402_doc", "424_doc", "pg_contract"),
            "generated_utc": generated,
        }
        for algebra_id, step, form, status, condition in rows
    ]


def parent_premise_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EHP700_0_same_frame", "one observed metric/coframe for source and readout", "conditional_not_parent_derived", "Delta_frame", "blocks coefficient claim"),
        ("EHP700_1_EH_only", "metric-only local second-order EH exterior", "not_derived_R11_template_only", "epsilon_operator", "non-EH pieces can alter coefficient/slip/range"),
        ("EHP700_2_Levi_Civita", "observed connection is Levi-Civita", "not_parent_derived", "connection_residual", "source equation can differ from EH Poisson"),
        ("EHP700_3_source_conservation", "Bianchi/Ward exchange is closed in matter source", "not_fully_closed", "source_exchange_residual", "extra force/source exchange can enter Poisson"),
        ("EHP700_4_nonrel_source", "ordinary compact nonrelativistic source limit", "conditional_standard_limit", "source_coefficient_residual", "rho_H may not be the only source"),
        ("EHP700_5_universal_kappa", "kappa/G constant universal source-blind", "not_parent_derived", "Delta_G", "coefficient can drift or carry species/range dependence"),
        ("EHP700_6_no_source_residuals", "mu_extra/source residuals zero or bounded", "channels_unfilled", "mu_extra_over_GM", "hidden source-normalization channels remain"),
        ("EHP700_7_verdict", "parent-ready EH Poisson coefficient", "fail_current_corpus", "Delta_Poisson", "algebra certificate only; parent premise unsigned"),
    ]
    return [
        {
            "premise_id": premise_id,
            "premise": premise,
            "current_status": status,
            "residual_if_fail": residual,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("424_doc", "425_doc", "429_doc", "529_doc", "655_doc", "657_channels"),
            "generated_utc": generated,
        }
        for premise_id, premise, status, residual, effect in rows
    ]


def delta_poisson_fill_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "fill_id": "DP700_0_first_Delta_Poisson_fill",
            "target_prior_row": "PGR699_3_poisson",
            "quantity": "Delta_Poisson",
            "definition": "abs((kappa_eff*c^4)/(8*pi*G_ref)-1)+abs(source_residuals)/(4*pi*G_ref*rho_H)",
            "value_or_theorem_zero": "MISSING_VALUE_OR_THEOREM_ZERO",
            "kappa_eff": "MISSING_PARENT_KAPPA_EFF",
            "G_ref": "MISSING_CONSTANT_UNIVERSAL_GREF",
            "source_residuals": "MISSING_SOURCE_RESIDUAL_BOUND",
            "rho_H_normalization": "MISSING_RHO_H_NORMALIZATION",
            "units": "dimensionless",
            "equation_ref": "MISSING_EQUATION_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "unfilled_after_parent_premise_failure",
            "valid_for_claim": "false",
            "source_paths": source_list("699_pg_source_rows", "source_norm_scorecard", "pg_contract"),
            "generated_utc": generated,
        }
    ]


def route_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("ROUTE700_0", "derive_parent_premise", "try to parent-sign same-frame EH/source/kappa/no-residual premises", "highest", NEXT_TARGET),
        ("ROUTE700_1", "fill_Delta_Poisson", "supply numeric/theorem-zero source row for coefficient residual", "highest", NEXT_TARGET),
        ("ROUTE700_2", "then_Gauss_orbit", "after Delta_Poisson is cleared, attack Gauss surface/orbit arrows", "high", "702-Y5-R10-Gauss-surface-or-orbital-readout-residual-fill.md"),
    ]
    return [
        {
            "route_id": route_id,
            "route": route,
            "why": why,
            "priority": priority,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for route_id, route, why, priority, next_action in rows
    ]


def handoff_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("SNAP700_0", "best_positive", "EH-to-Poisson coefficient algebra is clean and now isolated"),
        ("SNAP700_1", "not_claim_ready", "parent premises are unsigned, especially same-frame EH/source, EH-only operator, universal kappa, and no source residuals"),
        ("SNAP700_2", "next_executable", "Delta_Poisson fill row is now the smallest concrete source-row target"),
        ("SNAP700_3", "local_GR_status", "still blocked; this only attacks first-order coefficient, not measured GM or PPN followthrough"),
    ]
    return [
        {
            "snapshot_id": snapshot_id,
            "topic": topic,
            "short_read": short_read,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for snapshot_id, topic, short_read in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG700_0_algebra", "EH coefficient algebra written", "algebra_clean", "pass_structure", "not claim credit"),
        ("CG700_1_parent_premise", "all parent premises signed", "fail_current_corpus", "fail_blocked", "Delta_Poisson retained"),
        ("CG700_2_numeric_fill", "Delta_Poisson numeric/theorem-zero row filled", "MISSING_VALUE_OR_THEOREM_ZERO", "fail_blocked", "no PG score"),
        ("CG700_3_MHref", "M_H_ref denominator safe", "MISSING_CERTIFIED_POSITIVE_M_H_REF", "fail_blocked", "no B_TF/e_TF"),
        ("CG700_4_local_GR", "PPN/local-GR promotion", "not_reached", "fail_blocked", "no local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("699_eh_audit", "696_denominator_audit", "gauss_ppn_test"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "decision_id": "D700_0_algebra_certificate",
            "target": "EH-to-Poisson coefficient",
            "result": "algebra_certificate_written",
            "reason": "the coefficient relation is clean under same-frame EH/source assumptions",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        },
        {
            "decision_id": "D700_1_parent_premise",
            "target": "parent premise promotion",
            "result": "failed_current_corpus",
            "reason": "same-frame, EH-only, Levi-Civita, universal kappa, and no-source-residual clauses are still unsigned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        },
        {
            "decision_id": "D700_2_fill",
            "target": "Delta_Poisson numeric/source row",
            "result": "row_written_unfilled",
            "reason": "the residual is now executable-shaped if the derivation route stalls",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        },
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S700_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "EH-to-Poisson algebra is clean but parent premises remain unsigned; Delta_Poisson fill row is staged",
            "hardest_blocker": "same-frame EH/source parent premise plus universal kappa and no source residuals",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def validation_rows(source_rows, algebra, premises, fill, routes, handoff, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("699_validation"))
    pgr699_poisson = [row for row in read_csv(SOURCE_PATHS["699_pg_source_rows"]) if row.get("source_row_id") == "PGR699_3_poisson"][0]
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [algebra, premises, fill, routes, handoff, gates, decisions, summary]
        for row in group
    )
    fill_missing = fill[0]["value_or_theorem_zero"] == "MISSING_VALUE_OR_THEOREM_ZERO" and fill[0]["source_path"] == "MISSING_SOURCE_PATH"
    scoped = all(
        str(path).startswith(str(ROOT))
        for path in [
            DOC_PATH,
            RESIDUALS / "P8_Y5_R10_700_SOURCE_REGISTER.csv",
            RESIDUALS / "P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
            RESIDUALS / "P8_Y5_R10_700_PARENT_PREMISE_AUDIT.csv",
            RESIDUALS / "P8_Y5_R10_700_DELTA_POISSON_FILL_ROW.csv",
            RESIDUALS / "P8_Y5_R10_700_ROUTE_DECISION.csv",
            RESIDUALS / "P8_Y5_R10_700_HANDOFF_SNAPSHOT.csv",
            RESIDUALS / "P8_Y5_R10_700_CLAIM_GATE_EVALUATION.csv",
            RESIDUALS / "P8_Y5_R10_700_DECISION.csv",
            RESIDUALS / "P8_Y5_R10_700_NONCLAIM_SUMMARY.csv",
            RESIDUALS / "P8_Y5_BRR545_700_VALIDATION.csv",
        ]
    )
    formalization_count = formalization_changed_count()
    checks = [
        ("V700_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V700_1_prior_699_clean", prior_failures == 0, f"699_validation_failures={prior_failures}"),
        ("V700_2_699_poisson_row_loaded", pgr699_poisson.get("current_status") == "MISSING_EH_POISSON_COEFFICIENT_OR_BOUND", pgr699_poisson.get("current_status", "missing")),
        ("V700_3_algebra_certificate_written", len(algebra) == 6, f"algebra_rows={len(algebra)}"),
        ("V700_4_parent_premise_audit_blocks", len(premises) == 8 and premises[-1]["current_status"] == "fail_current_corpus", f"premise_rows={len(premises)}"),
        ("V700_5_Delta_Poisson_fill_unfilled", fill_missing, "Delta_Poisson row keeps missing markers"),
        ("V700_6_gates_block_claim", len(gates) == 5 and all(row["valid_for_claim"] == "false" for row in gates), f"gate_rows={len(gates)}"),
        ("V700_7_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V700_8_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V700_9_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V700_10_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V700_11_status_nonclaim", "no_Delta_Poisson_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, algebra, premises, fill, routes, handoff, gates, decisions, summary, validation) -> None:
    doc = f"""# 700 - Y5 R10 EH Poisson Coefficient Parent Premise Or PG Residual Numeric Fill

## Verdict

700 isolates the cleanest local-GR bridge arrow:

```text
G_munu[g_obs]=kappa_eff T_munu[g_obs]
T_00 ~= rho_H c^2
G_00 ~= 2 nabla^2 Phi/c^2
=> nabla^2 Phi=(kappa_eff c^4/2)rho_H=4*pi*G_eff rho_H
```

The algebra is clean. The parent-premise promotion is not. Same-frame EH/source ownership, EH-only operator selection, Levi-Civita compatibility, source conservation, constant universal `kappa/G`, and zero source residuals are still unsigned.

So `Delta_Poisson` is staged as the next executable source row, but it is not filled and no claim is promoted.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Algebra Certificate

{markdown_table(algebra, ["algebra_id", "step", "status", "condition", "valid_for_claim"])}

## Parent Premise Audit

{markdown_table(premises, ["premise_id", "premise", "current_status", "residual_if_fail", "claim_effect", "valid_for_claim"])}

## Delta Poisson Fill Row

{markdown_table(fill, ["fill_id", "quantity", "value_or_theorem_zero", "kappa_eff", "G_ref", "source_residuals", "source_path", "valid_for_claim"])}

## Route Decision

{markdown_table(routes, ["route_id", "route", "why", "priority", "next_action", "valid_for_claim"])}

## Handoff Snapshot

{markdown_table(handoff, ["snapshot_id", "topic", "short_read", "valid_for_claim"])}

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
    algebra = algebra_certificate_rows()
    premises = parent_premise_rows()
    fill = delta_poisson_fill_rows()
    routes = route_rows()
    handoff = handoff_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, algebra, premises, fill, routes, handoff, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_700_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv", algebra, ["algebra_id", "step", "mathematical_form", "status", "condition", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_PARENT_PREMISE_AUDIT.csv", premises, ["premise_id", "premise", "current_status", "residual_if_fail", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_DELTA_POISSON_FILL_ROW.csv", fill, ["fill_id", "target_prior_row", "quantity", "definition", "value_or_theorem_zero", "kappa_eff", "G_ref", "source_residuals", "rho_H_normalization", "units", "equation_ref", "source_path", "derivation_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_ROUTE_DECISION.csv", routes, ["route_id", "route", "why", "priority", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_HANDOFF_SNAPSHOT.csv", handoff, ["snapshot_id", "topic", "short_read", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_700_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_700_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, algebra, premises, fill, routes, handoff, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"algebra_rows={len(algebra)}")
    print(f"premise_rows={len(premises)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
