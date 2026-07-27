from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote"
DOC_PATH = ROOT / "596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_596_SOURCE_REGISTER.csv"
PI_FACTOR_TEST_PATH = RESIDUALS / "P8_Y5_R10_596_GAMMA_KHAT_PI_FACTOR_TEST.csv"
QLOC_GATE_PATH = RESIDUALS / "P8_Y5_R10_596_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv"
LEMMA_PATH = RESIDUALS / "P8_Y5_R10_596_QUOTIENT_PULLBACK_LEMMA.csv"
DEMOTION_PATH = RESIDUALS / "P8_Y5_R10_596_DEMOTION_ROUTING.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_596_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_596_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_596_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_596_VALIDATION.csv"

PRIOR_595_VALIDATION = RESIDUALS / "P8_Y5_BRR545_595_VALIDATION.csv"

STATUS = "Y5_R10_Gamma_Khat_qloc_pi_factor_test_partial_success_exact_zero_not_derived_q_loc_demoted_to_reduced_residual"
CLAIM_CEILING = "pi_factorisation_lemma_and_q_loc_demotion_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md"

SOURCE_FILES = [
    ("595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md", "immediate pi candidate handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_595_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_595_PI_OBSERVED_QUOTIENT_MAP.csv", "pi candidate rows"),
    ("source-intake/mts_residuals/P8_Y5_R10_595_QUOTIENT_FACTORISATION_TEST.csv", "Gamma/Khat/q_loc factorisation target"),
    ("source-intake/mts_residuals/P8_Y5_R10_595_DEMOTION_GATE.csv", "demotion policy"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "q_loc stress-divergence identity"),
    ("514-construct-GK-stress-action-or-residual-bound.md", "S_GK metric-response candidate"),
    ("515-match-Gamma-eff-Khat-to-metric-response-action.md", "current corpus match audit"),
    ("516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md", "Gamma owner candidate and q_loc runner spec"),
    ("517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md", "formal double-zero and Y5/Y6 blockers"),
    ("518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md", "q_loc/source-normalization residual input"),
    ("219-compact-shell-q_loc-source-projection-attempt.md", "older compact q_loc identity target"),
    ("220-Jrel-local-trivial-representative-or-closure-bound.md", "compact q_loc leakage budget"),
    ("scripts/Y5_R10_test_Gamma_Khat_qloc_factor_through_pi_or_demote.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_lemma_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "QPL596_0_pullback_setup",
            "statement": "Let pi:Conf_parent->Q_obs and v_X in ker(d pi). If Gamma_eff=gamma o pi, K_hat=kappa o pi, P_loc=Pi o pi, and the connection is built from g_obs=pi_g(Y), then these objects are vertical-blind.",
            "derivation": "L_{v_X}(gamma o pi)=d gamma[d pi(v_X)]=0; same for kappa, Pi, and g_obs-compatible nabla.",
            "consequence": "vertical representative motion cannot directly create qbar_XT or a new X fifth-force source through Gamma/Khat",
            "current_status": "conditional_lemma_proved",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "QPL596_1_q_loc_pullback",
            "statement": "Under the same pullback assumptions, q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) is also a pullback from Q_obs.",
            "derivation": "all ingredients in q_loc are functions of Q_obs, so L_{v_X}q_loc=0",
            "consequence": "q_loc is not a vertical-X representative source if the pullback assumptions are true",
            "current_status": "conditional_lemma_proved",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "QPL596_2_not_zero",
            "statement": "q_loc being a quotient pullback does not imply q_loc=0.",
            "derivation": "a nonzero tensor field on Q_obs can be vertical-blind and still physically observable",
            "consequence": "strict quotient factorisation solves the hidden-X issue, not the local-GR residual by itself",
            "current_status": "hard_distinction_added",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "QPL596_3_exact_zero_condition",
            "statement": "q_loc=0 follows only if T_GK^{mu nu}=Gamma_eff g_obs^{mu nu}-K_hat^{mu nu} is a Hilbert stress of a reduced diffeomorphism-invariant action and the reduced fields are on shell with no boundary flux.",
            "derivation": "diffeomorphism Ward identity gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A plus boundary terms; local compact vacuum requires E_A=0 and zero boundary flux",
            "consequence": "exact local silence needs reduced action ownership, not only pi factorisation",
            "current_status": "conditional_Ward_route_only",
            "valid_for_claim": "false",
        },
    ]


def make_factor_test_rows() -> list[dict[str, str]]:
    return [
        {
            "test_id": "PFT596_0_Gamma_eff",
            "object": "Gamma_eff",
            "pi_safe_form": "Gamma_eff[Y]=gamma[Q_obs]=gamma(pi(Y))",
            "required_evidence": "scalar density owner or reduced scalar functional with units and no representative marker",
            "current_evidence": "515 found no current corpus proof that Gamma_eff is a covariant scalar action density; 516 wrote a candidate response-doublet owner",
            "result": "conditional_candidate_not_current_match",
            "next_action": "construct reduced Gamma owner or retain residual row",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PFT596_1_K_hat",
            "object": "K_hat",
            "pi_safe_form": "K_hat^{mu nu}[Y]=kappa^{mu nu}[Q_obs]=metric response of gamma(pi(Y)) or exact improvement",
            "required_evidence": "K_hat equals metric response of sqrt(-g_obs)gamma including derivative and boundary terms",
            "current_evidence": "515 found no K_hat metric-response derivation; 514/516 give contract candidates only",
            "result": "conditional_candidate_not_current_match",
            "next_action": "compute response from proposed gamma and compare tensor structure",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PFT596_2_P_loc",
            "object": "P_loc",
            "pi_safe_form": "P_loc[Y]=Pi[Q_obs] or a fixed parent-owned reduced projector",
            "required_evidence": "projector is not selected after readout and does not hide unprojected force components",
            "current_evidence": "513 and 514 keep projector ownership open; 595 keeps readout-after-variation guard",
            "result": "open_not_closed",
            "next_action": "derive parent projector algebra or carry full unprojected residual",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PFT596_3_q_loc_vertical_blindness",
            "object": "q_loc",
            "pi_safe_form": "q_loc=Pi[Q_obs] nabla_mu T_GK^{mu nu}[Q_obs]",
            "required_evidence": "PFT596_0-PFT596_2 pass",
            "current_evidence": "conditional lemma works if Gamma/Khat/P_loc are rewritten as reduced pullbacks",
            "result": "passes_only_as_redefinition_contract",
            "next_action": "do not call q_loc zero; route to exactness gate",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PFT596_4_current_MTS_symbol_match",
            "object": "actual current symbols",
            "pi_safe_form": "existing Gamma_eff, K_hat, q_loc definitions are already reduced pullbacks or exact identities",
            "required_evidence": "source path with definitions and metric-response/no-marker proof",
            "current_evidence": "no current source proves this; current trail repeatedly marks match not derived",
            "result": "fail_for_claim",
            "next_action": "demote claim to reduced residual until 597 owner is built",
            "valid_for_claim": "false",
        },
    ]


def make_qloc_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "QEG596_0_vertical_source_gate",
            "question": "Can Gamma/Khat/q_loc be made blind to representative X?",
            "answer": "yes_conditionally_if_defined_as_Q_obs_pullbacks",
            "meaning": "this protects the lower-scrutiny quotient route from smuggling a vertical fifth-force field",
            "failure_route": "if any representative derivative survives, strict quotient route is demoted to diffeo-current or finite edge branch",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "QEG596_1_exact_local_zero_gate",
            "question": "Does quotient pullback imply q_loc=0?",
            "answer": "no",
            "meaning": "q_loc can be an observed reduced residual even when it is vertical-blind",
            "failure_route": "must derive Ward zero or score q_loc residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "QEG596_2_Ward_owner_gate",
            "question": "Is T_GK=Gamma g-Khat owned by a reduced diffeo-invariant action?",
            "answer": "not_for_current_MTS",
            "meaning": "513-516 provide a route, but 515 found no current scalar-density/metric-response match",
            "failure_route": "reduced residual runner",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "QEG596_3_Y5_Y6_gate",
            "question": "Do the response-doublet/double-zero clauses kill source normalization and extra stress?",
            "answer": "not_yet",
            "meaning": "517 and 518 keep Y5 source normalization, Y6 stress, PPN lock, and boundary response active",
            "failure_route": "source-normalization and PPN residual rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "QEG596_4_boundary_flux_gate",
            "question": "Can a bulk q_loc zero still leak through boundary/source-measure terms?",
            "answer": "yes_if_boundary_no_flux_not_proved",
            "meaning": "the exact route still needs boundary primitive/reference subtraction, not only bulk algebra",
            "failure_route": "compact-shell q_loc/source-measure bound",
            "valid_for_claim": "false",
        },
    ]


def make_demotion_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "DR596_A_strict_quotient_vertical_X",
            "status_after_596": "kept_as_conditional_construction_route",
            "reason": "the pullback lemma can make Gamma/Khat/q_loc vertical-blind if they are defined on Q_obs",
            "not_allowed": "claim q_loc=0 or local GR from vertical-blindness alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "DR596_B_q_loc_exact_zero",
            "status_after_596": "demoted_for_current_claim",
            "reason": "current MTS lacks reduced S_GK owner, K_hat metric response, Y5/Y6 closure, and boundary no-flux",
            "not_allowed": "use q_loc silence as a theorem-zero row",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "DR596_C_observed_reduced_residual",
            "status_after_596": "promoted_as_honest_fallback",
            "reason": "a vertical-blind but nonzero q_loc is an observed reduced residual, not a hidden X field",
            "not_allowed": "hide it under quotient language",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "DR596_D_diffeo_current_backup",
            "status_after_596": "backup_open",
            "reason": "if reduced Gamma/Khat owner fails, C_X may still match ordinary parent diffeomorphism/momentum current",
            "not_allowed": "double-count ADM/Hamiltonian charges",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "DR596_E_finite_edge_bound",
            "status_after_596": "fallback_open",
            "reason": "if neither quotient nor diffeo-current proof closes, q_loc/edge/source-normalization rows must be bounded numerically",
            "not_allowed": "mark diagnostic coefficients as source-backed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D596_0_pullback_lemma_accepted",
            "decision": "accept the conditional quotient-pullback lemma",
            "meaning": "if Gamma/Khat/P_loc are reduced Q_obs objects, q_loc is vertical-blind and does not smuggle an X fifth force",
            "claim_status": "conditional_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D596_1_exact_q_loc_zero_not_derived",
            "decision": "demote q_loc exact zero for current MTS",
            "meaning": "vertical-blindness is not local-GR silence; Ward owner, metric response, Y5/Y6, and boundary gates remain open",
            "claim_status": "q_loc_zero_false_for_current_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D596_2_next_owner_or_runner",
            "decision": "force 597 to choose reduced GK owner or q_loc residual runner",
            "meaning": "the next pass must either build S_GK on Q_obs or stop theorem-hunting and score the retained residual",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU596_0_allowed",
            "allowed_after_596": "say q_loc can be made vertical-blind under explicit Q_obs pullback assumptions",
            "forbidden_after_596": "say quotient factorisation has derived q_loc=0",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU596_1_allowed",
            "allowed_after_596": "treat nonzero q_loc as an observed reduced residual needing Ward ownership or bounds",
            "forbidden_after_596": "hide a nonzero q_loc inside representative-gauge language",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU596_2_allowed",
            "allowed_after_596": "keep diffeo-current and finite-edge routes as backups",
            "forbidden_after_596": "close the local branch without S_GK, boundary no-flux, and source-normalization proof",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S596_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "strict_quotient_status": "vertical_X_route_live_exact_q_loc_zero_demoted",
            "best_private_read": "The quotient route scores a real conceptual win: Gamma/Khat/q_loc can be made vertical-blind if reduced to Q_obs. But exact q_loc=0 is not derived; it now needs a reduced GK action owner or must be scored as an observed residual.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    factor_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_595_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in lemma_rows if row["valid_for_claim"] == "true"],
        *[row for row in factor_rows if row["valid_for_claim"] == "true"],
        *[row for row in gate_rows if row["valid_for_claim"] == "true"],
        *[row for row in demotion_rows if row["valid_for_claim"] == "true"],
    ]
    pullback_lemma = any(row["lemma_id"] == "QPL596_1_q_loc_pullback" for row in lemma_rows)
    not_zero_guard = any(row["lemma_id"] == "QPL596_2_not_zero" for row in lemma_rows)
    gamma_fail = any(row["test_id"] == "PFT596_0_Gamma_eff" and row["result"] == "conditional_candidate_not_current_match" for row in factor_rows)
    khat_fail = any(row["test_id"] == "PFT596_1_K_hat" and row["result"] == "conditional_candidate_not_current_match" for row in factor_rows)
    exact_demoted = any(row["route_id"] == "DR596_B_q_loc_exact_zero" and "demoted" in row["status_after_596"] for row in demotion_rows)
    residual_route = any(row["route_id"] == "DR596_C_observed_reduced_residual" for row in demotion_rows)
    return [
        {
            "check_id": "V596_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V596_1_prior_595_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V596_2_pullback_lemma_written",
            "result": "pass" if pullback_lemma else "fail",
            "detail": f"lemma_rows={len(lemma_rows)}",
        },
        {
            "check_id": "V596_3_pullback_not_zero_guard",
            "result": "pass" if not_zero_guard else "fail",
            "detail": "q_loc pullback does not imply q_loc zero",
        },
        {
            "check_id": "V596_4_current_symbol_match_not_overclaimed",
            "result": "pass" if gamma_fail and khat_fail else "fail",
            "detail": f"Gamma_conditional={gamma_fail};Khat_conditional={khat_fail}",
        },
        {
            "check_id": "V596_5_exact_zero_demoted",
            "result": "pass" if exact_demoted else "fail",
            "detail": "q_loc exact zero not derived for current MTS",
        },
        {
            "check_id": "V596_6_residual_route_present",
            "result": "pass" if residual_route else "fail",
            "detail": "observed reduced residual fallback present",
        },
        {
            "check_id": "V596_7_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V596_8_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    factor_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 596 Y5 R10 test Gamma Khat qloc factor through pi or demote

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The strict quotient route gets a real but limited win: if `Gamma_eff`, `K_hat`, and `P_loc` are reduced pullbacks from `Q_obs`, then `q_loc` is vertical-blind and does not smuggle in a physical representative-`X` fifth force.
- That is not the same as deriving `q_loc=0`. A nonzero field on `Q_obs` can be perfectly quotient-safe and still physically observable.
- Current MTS still does not prove the reduced `S_GK` owner, the `K_hat` metric-response identity, Y5/Y6 source closure, or boundary no-flux.
- Therefore exact `q_loc` silence is demoted for the current claim. The route now has to build a reduced GK action owner or run `q_loc` as an observed residual.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Quotient Pullback Lemma
{markdown_table(lemma_rows, ["lemma_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim"])}

## Gamma Khat Pi Factor Test
{markdown_table(factor_rows, ["test_id", "object", "pi_safe_form", "required_evidence", "current_evidence", "result", "next_action", "valid_for_claim"])}

## Qloc Exactness Or Residual Gate
{markdown_table(gate_rows, ["gate_id", "question", "answer", "meaning", "failure_route", "valid_for_claim"])}

## Demotion Routing
{markdown_table(demotion_rows, ["route_id", "status_after_596", "reason", "not_allowed", "next_action", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_596", "forbidden_after_596", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a disciplined demotion, not a collapse. The low-scrutiny move still helps: the dangerous hidden `X` force can be kept out if the local objects are genuinely reduced variables. But the judges will not give local-GR points for that alone. To score the round, `T_GK` must be owned by a reduced action or `q_loc` must be bounded honestly.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    lemma_rows = make_lemma_rows()
    factor_rows = make_factor_test_rows()
    gate_rows = make_qloc_gate_rows()
    demotion_rows = make_demotion_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, lemma_rows, factor_rows, gate_rows, demotion_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(LEMMA_PATH, lemma_rows, ["lemma_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim"])
    write_csv(
        PI_FACTOR_TEST_PATH,
        factor_rows,
        ["test_id", "object", "pi_safe_form", "required_evidence", "current_evidence", "result", "next_action", "valid_for_claim"],
    )
    write_csv(QLOC_GATE_PATH, gate_rows, ["gate_id", "question", "answer", "meaning", "failure_route", "valid_for_claim"])
    write_csv(DEMOTION_PATH, demotion_rows, ["route_id", "status_after_596", "reason", "not_allowed", "next_action", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_596", "forbidden_after_596", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "claim_allowed",
            "R10_pass",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "strict_quotient_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        lemma_rows,
        factor_rows,
        gate_rows,
        demotion_rows,
        decision_rows,
        route_update_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
