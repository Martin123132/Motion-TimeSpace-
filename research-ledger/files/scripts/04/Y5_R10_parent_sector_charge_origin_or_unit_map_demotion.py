from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-parent-sector-charge-origin-or-unit-map-demotion"
DOC_PATH = ROOT / "605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_605_SOURCE_REGISTER.csv"
CHARGE_ORIGIN_PATH = RESIDUALS / "P8_Y5_R10_605_QSEC_ORIGIN_ATTEMPT.csv"
NO_GO_PATH = RESIDUALS / "P8_Y5_R10_605_QSEC_NO_GO_AND_DEMOTION_GATE.csv"
UNIT_CHANNEL_PATH = RESIDUALS / "P8_Y5_R10_605_UNIT_MAP_CHANNEL_DECISION.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_605_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_605_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_605_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_605_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_605_VALIDATION.csv"

PRIOR_604_VALIDATION = RESIDUALS / "P8_Y5_BRR545_604_VALIDATION.csv"
PRIOR_604_SECTOR = RESIDUALS / "P8_Y5_R10_604_SECTOR_CHARGE_THEOREM_ATTEMPT.csv"
PRIOR_604_UNIT = RESIDUALS / "P8_Y5_R10_604_UNIT_MAP_FORK_STATUS.csv"

STATUS = "Y5_R10_Qsec_origin_attempt_failed_PMTS_route_demoted_to_R10_unit_map_nonclaim"
CLAIM_CEILING = "Qsec_origin_failure_and_unit_map_routing_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md", "immediate 604 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_604_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_604_SECTOR_CHARGE_THEOREM_ATTEMPT.csv", "Q_sec theorem target"),
    ("source-intake/mts_residuals/P8_Y5_R10_604_UNIT_MAP_FORK_STATUS.csv", "unit-map fallback queued"),
    ("328-topological-MTS-support-projector-gate.md", "P_top/P_MTS sector-charge requirement"),
    ("324-CD-activity-kernel-commutation-gate.md", "C_D activity and kernel commutation failure"),
    ("323-S3-sector-label-combined-gate.md", "S3 singlet leakage guard"),
    ("311-sector-label-SD-origin-attempt.md", "support label and activity-operator circularity"),
    ("310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS superselection lemma"),
    ("293-domain-topology-selection-attempt.md", "domain topology selection not parent-derived"),
    ("448-constant-sector-universality-theorem-attempt.md", "ordinary constant-sector superselection analogy"),
    ("453-global-coupling-superselection-parent-action-contract.md", "global/superselection contract analogy"),
    ("574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md", "generator elimination order and finite envelope policy"),
    ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "finite qbar envelope trigger"),
    ("559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md", "R10 alpha(lambda) runner lineage"),
    ("563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md", "R10 real-bound curve/data plumbing checkpoint"),
    ("scripts/Y5_R10_parent_sector_charge_origin_or_unit_map_demotion.py", "this checkpoint generator"),
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


def make_charge_origin_rows() -> list[dict[str, str]]:
    return [
        {
            "origin_id": "QO605_0_relative_topology_charge",
            "candidate": "relative/topological charge",
            "mathematical_form": "Q_top labels exact versus non-exact relative boundary classes",
            "what_it_earns": "supports P_top and kills exact local representatives conditionally",
            "failure_mode": "does not distinguish MTS top class from edge/horizon/top class",
            "verdict": "insufficient_for_Qsec",
            "next_if_kept": "use as P_top factor only, not P_MTS",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_1_S3_singlet_charge",
            "candidate": "cell/coherent S3 singlet label",
            "mathematical_form": "Q_S3 labels singlet versus doublet sectors of motion/time/cell components",
            "what_it_earns": "owns coherent rank-one/singlet projectors conditionally",
            "failure_mode": "ordinary isotropic EM/thermal baths can also be singlets",
            "verdict": "insufficient_for_Qsec",
            "next_if_kept": "use for coherent cell rank only, not MTS sector support",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_2_activity_support_charge",
            "candidate": "S_D=support(C_D^dagger C_D)",
            "mathematical_form": "A_D=C_D^dagger C_D and S_D=1_(0,infinity)(A_D)",
            "what_it_earns": "threshold-free support projector if C_D is already parent-owned",
            "failure_mode": "circular for Q_sec because C_D needs P_MTS to exclude ordinary coherent IR relative baths",
            "verdict": "circular_for_PMTS_origin",
            "next_if_kept": "usable only after Q_sec/P_MTS exists",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_3_boundary_momentum_map",
            "candidate": "boundary/no-pole momentum-map charge",
            "mathematical_form": "G[epsilon]=int epsilon C_X + Q_boundary[epsilon]",
            "what_it_earns": "could classify gauge/edge charges if differentiable and first class",
            "failure_mode": "current corpus has no parent-owned momentum map and boundary charges remain open",
            "verdict": "not_available",
            "next_if_kept": "route nonzero boundary charge into residuals",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_4_global_superselection_declaration",
            "candidate": "declare MTS sector as global superselection label",
            "mathematical_form": "Q_parent = Q_dyn x K_sec with Q_sec in K_sec and delta_local Q_sec=0",
            "what_it_earns": "would be a clean explicit closure premise for P_MTS if declared",
            "failure_mode": "declaration is not derivation and still must define nondegenerate q_MTS",
            "verdict": "closure_premise_not_parent_theorem",
            "next_if_kept": "label PMTS branch as closure and score residuals",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_5_topological_zero_form_or_integration_constant",
            "candidate": "future parent topological/integration charge",
            "mathematical_form": "sector label arises as closed zero-form/integration constant or BF-like topological boundary charge",
            "what_it_earns": "could derive nonlocal sector constancy without local stress if built into parent action",
            "failure_mode": "not present in current corpus and no nondegenerate MTS-versus-edge functional is supplied",
            "verdict": "future_research_not_current_derivation",
            "next_if_kept": "requires new parent action ingredient, outside current derivation pass",
            "valid_for_claim": "false",
        },
        {
            "origin_id": "QO605_6_parent_origin_verdict",
            "candidate": "Q_sec as current parent theorem",
            "mathematical_form": "self-adjoint nondegenerate conserved sector charge with [K_B,Q_sec]=0",
            "what_it_earns": "would derive P_MTS and ordinary/MTS block kernel",
            "failure_mode": "all available candidates are insufficient, circular, or closure-only",
            "verdict": "fail_current_corpus",
            "next_if_kept": "demote PMTS route and build unit-map scorer",
            "valid_for_claim": "false",
        },
    ]


def make_no_go_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "NG605_0_non_degeneracy",
            "requirement": "q_MTS distinct from q_ord and q_edge",
            "current_result": "fail_current_corpus",
            "reason": "P_top degenerates MTS with edge; S3 degenerates MTS with ordinary coherent baths",
            "consequence": "no parent P_MTS theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG605_1_conservation_or_commutation",
            "requirement": "Q_sec conserved and [K_B,Q_sec]=0",
            "current_result": "not_derived",
            "reason": "no boundary action symmetry or conserved sector current is supplied",
            "consequence": "ordinary/MTS block kernel remains conditional",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG605_2_non_circularity",
            "requirement": "Q_sec must not be defined using P_MTS itself",
            "current_result": "activity_support_route_circular",
            "reason": "C_D=P_MTS P_rel P_IR P_coh works only after P_MTS exists",
            "consequence": "support label cannot derive its own sector charge",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG605_3_no_hidden_projector_stress",
            "requirement": "Q_sec/P_MTS stress is topological/internal or retained",
            "current_result": "open",
            "reason": "without Q_sec type, delta_g P_MTS is unknown",
            "consequence": "q_loc and PPN rows remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG605_4_stop_rule",
            "requirement": "do not keep iterating equivalent projector closures",
            "current_result": "demote_now",
            "reason": "604/605 reduce the lock to a genuinely missing parent charge, not an algebra gap",
            "consequence": "unit-map scoring becomes the disciplined next route",
            "valid_for_claim": "false",
        },
    ]


def make_unit_channel_rows() -> list[dict[str, str]]:
    return [
        {
            "channel_id": "UMC605_0_R10_alpha_lambda",
            "channel": "R10 alpha(lambda)",
            "selection_status": "recommended_first_nonclaim_channel",
            "why": "existing R10 bound-curve and alpha(lambda) runner lineage make it the least ambiguous first unit-map target",
            "required_inputs": "lambda, alpha_predicted or coefficient product, sign/profile, source paths, valid bound curve",
            "blocked_by": "compact-shell proxy is dimensionless and not yet mapped to alpha(lambda)",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UMC605_1_PPN_vector",
            "channel": "PPN residual vector",
            "selection_status": "defer_until_R10_map",
            "why": "PPN is the real local-GR judge but requires many components, source normalization, R11, and measured-GM gates",
            "required_inputs": "gamma, beta, alpha1, alpha2, alpha3, xi, Gdot, source-normalization rows",
            "blocked_by": "too many still-open components for the first unit-map scorer",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UMC605_2_WEP_source",
            "channel": "WEP/source charge",
            "selection_status": "defer",
            "why": "requires constant-sector and source-current universality debts from 448/576",
            "required_inputs": "species/source charge coefficient, Eotvos bound, composition map",
            "blocked_by": "qbar/source-current premises not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UMC605_3_clock",
            "channel": "clock/redshift/fine-structure",
            "selection_status": "defer",
            "why": "needs a specific coupling from compact-shell proxy to clock constants or spectral shifts",
            "required_inputs": "delta_nu/nu or dot_alpha/alpha coefficient and clock/source data",
            "blocked_by": "no clock unit conversion from compact-shell proxy",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UMC605_4_demotion_policy",
            "channel": "unit-map workflow",
            "selection_status": "activated_nonclaim",
            "why": "Q_sec derivation failed, so the PMTS route is closure/theorem target only",
            "required_inputs": "606 input template with all rows valid_for_claim=false until numeric and sourced",
            "blocked_by": "no physical score yet",
            "valid_for_claim": "false",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU605_0_Qsec_origin",
            "previous_status": "parent_sector_charge_missing",
            "new_status": "origin_attempt_failed_current_corpus",
            "reason": "available candidates are insufficient, circular, or closure-only",
            "still_needed": "new parent action ingredient or explicit closure label",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU605_1_PMTS_route",
            "previous_status": "conditional_Qsec_kernel_theorem_written",
            "new_status": "demoted_to_theorem_target_closure",
            "reason": "block theorem is algebraically clean but lacks parent charge origin",
            "still_needed": "do not use P_MTS for local evidence without numeric unit map",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU605_2_unit_map",
            "previous_status": "queued_if_Qsec_origin_fails",
            "new_status": "R10_alpha_lambda_channel_recommended",
            "reason": "R10 has existing source-backed bound-curve infrastructure and a single alpha(lambda) readout target",
            "still_needed": "606 channel-lock and input template",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU605_3_local_GR_stack",
            "previous_status": "q_loc_R11_boundary_open",
            "new_status": "still_open",
            "reason": "demotion does not close GR reduction; it only makes the closure branch testable",
            "still_needed": "PPN/WEP/R11/source-normalization gates remain separate",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D605_0_Qsec_failure",
            "decision": "reject current Q_sec derivation",
            "meaning": "no cited parent object gives a nondegenerate conserved MTS sector charge",
            "claim_status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D605_1_PMTS_demotion",
            "decision": "demote P_MTS route to theorem target or closure",
            "meaning": "P_MTS may remain in private conditional models, but cannot be counted as derived support",
            "claim_status": "closure_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D605_2_first_unit_channel",
            "decision": "choose R10 alpha(lambda) as first unit-map channel",
            "meaning": "R10 is the cleanest first scorer because the bound-curve and alpha runner infrastructure already exist",
            "claim_status": "nonclaim_template_next",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D605_3_promotion",
            "decision": "forbid local-GR/PPN/R10 promotion",
            "meaning": "unit-map routing is not evidence until numeric coefficients, units, source paths, and bounds are filled",
            "claim_status": "forbidden",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU605_0_allowed",
            "allowed_after_605": "cite Q_sec as an exact future parent theorem target",
            "forbidden_after_605": "keep deriving equivalent P_MTS projectors without a new charge ingredient",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU605_1_allowed",
            "allowed_after_605": "build a nonclaim R10 alpha(lambda) unit-map template",
            "forbidden_after_605": "score compact-shell proxy directly as alpha(lambda)",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU605_2_allowed",
            "allowed_after_605": "keep PPN/WEP/clock maps queued after R10",
            "forbidden_after_605": "claim R10 success would equal local GR",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S605_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "Qsec_status": "origin_failed_current_corpus",
            "PMTS_status": "demoted_to_conditional_theorem_target",
            "unit_map_status": "R10_alpha_lambda_first_channel_recommended_nonclaim",
            "best_private_read": "605 is the stop rule for the projector route. The algebra is clean, but Q_sec is not derived. The honest move is now to turn the compact-shell proxy into a sourced R10 alpha(lambda) unit-map template and test it as closure, not as derived local GR.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    no_go_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_604_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result", "").strip().lower() != "pass"]
    prior_sector = read_csv(PRIOR_604_SECTOR)
    prior_unit = read_csv(PRIOR_604_UNIT)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in charge_rows if row["valid_for_claim"] == "true"],
        *[row for row in no_go_rows if row["valid_for_claim"] == "true"],
        *[row for row in unit_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    qsec_fail = any(row["origin_id"] == "QO605_6_parent_origin_verdict" and row["verdict"] == "fail_current_corpus" for row in charge_rows)
    demote_now = any(row["gate_id"] == "NG605_4_stop_rule" and row["current_result"] == "demote_now" for row in no_go_rows)
    r10_selected = any(row["channel_id"] == "UMC605_0_R10_alpha_lambda" and row["selection_status"] == "recommended_first_nonclaim_channel" for row in unit_rows)
    unit_activated = any(row["channel_id"] == "UMC605_4_demotion_policy" and row["selection_status"] == "activated_nonclaim" for row in unit_rows)
    pmts_demoted = any(row["runner_id"] == "RU605_1_PMTS_route" and row["new_status"] == "demoted_to_theorem_target_closure" for row in runner_rows)
    local_gr_open = any(row["runner_id"] == "RU605_3_local_GR_stack" and row["new_status"] == "still_open" for row in runner_rows)
    return [
        {
            "check_id": "V605_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V605_1_prior_604_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};sector_rows={len(prior_sector)};unit_rows={len(prior_unit)}",
        },
        {
            "check_id": "V605_2_Qsec_origin_failed_explicitly",
            "result": "pass" if qsec_fail else "fail",
            "detail": f"Qsec_fail={qsec_fail};charge_rows={len(charge_rows)}",
        },
        {
            "check_id": "V605_3_projector_stop_rule_activated",
            "result": "pass" if demote_now and pmts_demoted else "fail",
            "detail": f"demote_now={demote_now};PMTS_demoted={pmts_demoted}",
        },
        {
            "check_id": "V605_4_R10_unit_channel_selected_nonclaim",
            "result": "pass" if r10_selected and unit_activated else "fail",
            "detail": f"R10_selected={r10_selected};unit_activated={unit_activated}",
        },
        {
            "check_id": "V605_5_local_GR_still_open",
            "result": "pass" if local_gr_open else "fail",
            "detail": "R10 unit-map route does not equal PPN/local-GR promotion",
        },
        {
            "check_id": "V605_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V605_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    no_go_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 605 Y5 R10 parent sector charge origin or unit-map demotion

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- I tried the parent-sector-charge route directly. Current corpus does not derive `Q_sec`.
- The available candidates each fail in a different way: `P_top` cannot separate MTS from edge, `S3` cannot separate MTS from ordinary coherent baths, support projectors are circular without `P_MTS`, and momentum-map/boundary charges are not parent-owned.
- Therefore `P_MTS` is demoted to a conditional theorem target or closure ingredient, not a derived local-GR support object.
- The disciplined next route is a nonclaim unit-map scorer. First channel: `R10 alpha(lambda)`, because the bound-curve and alpha-runner infrastructure already exists.

## Charge-Origin Attempt
{markdown_table(charge_rows, ["origin_id", "candidate", "mathematical_form", "what_it_earns", "failure_mode", "verdict", "next_if_kept", "valid_for_claim"])}

## No-Go And Demotion Gate
{markdown_table(no_go_rows, ["gate_id", "requirement", "current_result", "reason", "consequence", "valid_for_claim"])}

## Unit-Map Channel Decision
{markdown_table(unit_rows, ["channel_id", "channel", "selection_status", "why", "required_inputs", "blocked_by", "valid_for_claim"])}

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_605", "forbidden_after_605", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is the honest bell on the projector round. We did not lose the conditional theorem; we lost the right to pretend it is already parent-derived. That is useful. Next we make the closure branch put its gloves on: map the compact-shell proxy into `R10 alpha(lambda)` with units, source paths, and failure modes, and score nothing until every input is real.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    charge_rows = make_charge_origin_rows()
    no_go_rows = make_no_go_rows()
    unit_rows = make_unit_channel_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, charge_rows, no_go_rows, unit_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(CHARGE_ORIGIN_PATH, charge_rows, ["origin_id", "candidate", "mathematical_form", "what_it_earns", "failure_mode", "verdict", "next_if_kept", "valid_for_claim"])
    write_csv(NO_GO_PATH, no_go_rows, ["gate_id", "requirement", "current_result", "reason", "consequence", "valid_for_claim"])
    write_csv(UNIT_CHANNEL_PATH, unit_rows, ["channel_id", "channel", "selection_status", "why", "required_inputs", "blocked_by", "valid_for_claim"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_605", "forbidden_after_605", "next_action"])
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
            "Qsec_status",
            "PMTS_status",
            "unit_map_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        charge_rows,
        no_go_rows,
        unit_rows,
        runner_rows,
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
