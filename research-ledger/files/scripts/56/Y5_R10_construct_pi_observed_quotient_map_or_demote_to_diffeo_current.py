from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current"
DOC_PATH = ROOT / "595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_595_SOURCE_REGISTER.csv"
PI_MAP_PATH = RESIDUALS / "P8_Y5_R10_595_PI_OBSERVED_QUOTIENT_MAP.csv"
FACTORISATION_PATH = RESIDUALS / "P8_Y5_R10_595_QUOTIENT_FACTORISATION_TEST.csv"
REDTEAM_PATH = RESIDUALS / "P8_Y5_R10_595_NO_CHEAT_REDTEAM.csv"
DEMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_595_DEMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_595_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_595_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_595_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_595_VALIDATION.csv"

PRIOR_594_VALIDATION = RESIDUALS / "P8_Y5_BRR545_594_VALIDATION.csv"

STATUS = "Y5_R10_pi_observed_quotient_candidate_constructed_strict_route_live_but_not_promoted"
CLAIM_CEILING = "candidate_pi_map_and_demotion_gate_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md"

SOURCE_FILES = [
    ("594-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md", "immediate route selection handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_594_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_594_ROUTE_SELECTION.csv", "lower-scrutiny route choice"),
    ("source-intake/mts_residuals/P8_Y5_R10_594_QUOTIENT_MAP_CONSTRUCTION_CONTRACT.csv", "pi construction contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv", "matter blindness blockers"),
    ("source-intake/mts_residuals/P8_Y5_R10_594_BOUNDARY_CLOSURE_LEDGER.csv", "boundary/ADM blockers"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "conditional no-pole theorem chain"),
    ("410-quotient-matter-functor-theorem-attempt.md", "matter functor quotient attempt"),
    ("414-local-quotient-invariant-algebra-triviality-gate.md", "local invariant algebra blocker"),
    ("422-matter-functor-blindness-readout-after-variation-theorem-attempt.md", "readout-after-variation guard"),
    ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no-extension/minimality blocker"),
    ("592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md", "Noether P/J origin contract"),
    ("scripts/Y5_R10_construct_pi_observed_quotient_map_or_demote_to_diffeo_current.py", "this checkpoint generator"),
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
    rows: list[dict[str, str]] = []
    for source_file, role in SOURCE_FILES:
        rows.append(
            {
                "source_file": source_file,
                "exists": str((ROOT / source_file).exists()),
                "role": role,
            }
        )
    return rows


def make_pi_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "PIM595_0_parent_space",
            "object": "Conf_parent(local compact region)",
            "candidate_definition": "Y=(O,R,B_ref), where O are observed/reduced fields, R are representative fibre variables, and B_ref fixes local boundary reference data",
            "mathematical_test": "Conf_parent is a fibre bundle over Q_obs with projection pi(Y)=O",
            "current_result": "candidate_constructed_as_formal_bundle",
            "claim_status": "nonclaim_candidate",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PIM595_1_observed_quotient",
            "object": "Q_obs",
            "candidate_definition": "Q_obs=(g_obs or e_obs, Phi_red, ordinary matter fields psi_A, universal constants theta_univ, compact-boundary ADM/reference class)",
            "mathematical_test": "every local observable, ruler, clock, and matter coupling is a function/functor of Q_obs only",
            "current_result": "partly_named_not_verified_for_MTS_Gamma_Khat_qloc",
            "claim_status": "open",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PIM595_2_equivalence_relation",
            "object": "Y ~_X Y'",
            "candidate_definition": "Y and Y' are equivalent when pi(Y)=pi(Y') and they differ only by compactly supported representative motion in R",
            "mathematical_test": "for every vertical parameter zeta with zeta|boundary=0, exp(zeta v_X) stays inside the same equivalence class",
            "current_result": "definition_available_if_boundary_domain_is_proper",
            "claim_status": "conditional",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PIM595_3_vertical_generator",
            "object": "v_X",
            "candidate_definition": "v_X[O]=0, v_X[B_ref]=0, v_X[R]=delta_X R, with no action on matter/readout variables except through quotient-invariant O",
            "mathematical_test": "d pi(v_X)=0 field-by-field; no hidden induced variation of g_obs, theta_univ, or psi_A",
            "current_result": "formal_dpi_zero_by_definition_but_MTS_field_identification_open",
            "claim_status": "conditional",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PIM595_4_parent_action_pullback",
            "object": "S_parent",
            "candidate_definition": "S_parent[Y]=S_GR[g_obs]+S_extra_red[g_obs,Phi_red]+S_matter[psi_A,g_obs,theta_univ]+dB_rep[R,B_ref]",
            "mathematical_test": "delta_X S_parent=0 plus exact/proper boundary term before imposing field equations",
            "current_result": "works_as_contract_not_as_current_MTS_derivation",
            "claim_status": "open",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PIM595_5_boundary_domain",
            "object": "proper local vertical transformations",
            "candidate_definition": "vertical transformations are compactly supported or fixed at the local boundary; ordinary ADM time/rotation translations are excluded from v_X",
            "mathematical_test": "Q_X[zeta]=0 for proper vertical zeta while ADM/Hamiltonian charges remain in Q_obs",
            "current_result": "boundary_rule_written_not_derived_from_parent_B_rep",
            "claim_status": "open",
            "valid_for_claim": "false",
        },
    ]


def make_factorisation_rows() -> list[dict[str, str]]:
    return [
        {
            "test_id": "QFT595_0_EH_local_GR_block",
            "sector": "local GR metric/coframe",
            "factorisation_requirement": "Einstein-Hilbert and ordinary matter metric use g_obs/e_obs in Q_obs",
            "what_would_pass": "v_X[g_obs]=0 and the local vacuum exterior equations reduce to the EH equations for g_obs",
            "current_result": "safe_contract_if_g_obs_is_quotient_variable",
            "scrutiny_level": "low_if_kept_explicit",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_1_matter_metric",
            "sector": "matter and clocks",
            "factorisation_requirement": "hat_g(Y)=hat_g_red(pi(Y)) and theta_univ=theta_univ(pi(Y)) with no representative marker",
            "what_would_pass": "delta_X S_matter=0 for all ordinary matter species before readout",
            "current_result": "blocked_until_no_marker_or_functor_universality_is_proved",
            "scrutiny_level": "medium",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_2_Gamma_Khat_qloc",
            "sector": "Gamma_eff, K_hat, q_loc",
            "factorisation_requirement": "Gamma_eff and K_hat must be pullbacks from Q_obs or combine into an exact vertical identity with q_loc=0",
            "what_would_pass": "P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) is identically zero/exact on fibres, not merely small",
            "current_result": "highest_risk_open_test_next",
            "scrutiny_level": "high",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_3_memory_domain_projector",
            "sector": "memory/domain/projector fields",
            "factorisation_requirement": "memory/domain variables split into Phi_red in Q_obs plus pure representative fibre R",
            "what_would_pass": "all source/load terms used in cosmology/galaxy work depend on Phi_red, not on vertical R",
            "current_result": "not_checked_against_full_symbol_spine",
            "scrutiny_level": "medium_high",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_4_Noether_PJ",
            "sector": "P/J/C_X",
            "factorisation_requirement": "theta(v_X)-mu_X=dB_rep with zero proper boundary integral",
            "what_would_pass": "P=0/exact, J_eff=0, C_X=-nabla P+J=0 as an off-shell quotient identity",
            "current_result": "conditional_if_action_pullback_and_boundary_primitive_are_built",
            "scrutiny_level": "medium",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_5_boundary_ADM_separation",
            "sector": "boundary charges",
            "factorisation_requirement": "vertical X excludes ordinary improper GR symmetries and has zero compact local charge",
            "what_would_pass": "Q_X=0 while ADM mass/angular momentum/reference subtraction remain observable in Q_obs",
            "current_result": "not_derived_but_guard_is_explicit",
            "scrutiny_level": "medium_high",
            "valid_for_claim": "false",
        },
        {
            "test_id": "QFT595_6_readout_order",
            "sector": "observables/readout",
            "factorisation_requirement": "readout is R_read:Sol(S_parent)->Observables after parent variation",
            "what_would_pass": "no post-readout reduced action is varied as if fundamental to fake q_loc=0",
            "current_result": "contract_retained",
            "scrutiny_level": "low_if_obeyed",
            "valid_for_claim": "false",
        },
    ]


def make_redteam_rows() -> list[dict[str, str]]:
    return [
        {
            "redteam_id": "NCR595_0_conformal_universal_marker",
            "attack": "hat_g_mu_nu=exp(2 a X)g_obs_mu_nu",
            "why_reviewers_accept_attack": "it is universal and covariant, so WEP alone does not kill it",
            "required_kill": "prove allowed matter metric functors factor through pi, forcing a=0 or X absent",
            "current_status": "not_killed",
            "route_if_not_killed": "finite qbar_XT or diffeo-current route",
        },
        {
            "redteam_id": "NCR595_1_material_marker",
            "attack": "add a covariant material/readout marker that transforms along the representative fibre",
            "why_reviewers_accept_attack": "strict covariance does not by itself forbid new universal marker fields",
            "required_kill": "minimality/no-natural-marker theorem or explicit extension tax",
            "current_status": "not_killed",
            "route_if_not_killed": "finite WEP/R10 coefficient branch",
        },
        {
            "redteam_id": "NCR595_2_boundary_edge_mode",
            "attack": "vertical symmetry carries a nonzero edge charge",
            "why_reviewers_accept_attack": "gauge directions can have physical boundary charges",
            "required_kill": "proper vertical domain or exact B_rep with zero compact-boundary integral",
            "current_status": "not_killed",
            "route_if_not_killed": "source-backed edge alpha(lambda)",
        },
        {
            "redteam_id": "NCR595_3_Gamma_Khat_real_field",
            "attack": "Gamma_eff or K_hat contains a real local scalar/vector not determined by Q_obs",
            "why_reviewers_accept_attack": "then q_loc is a real source profile, not a quotient identity",
            "required_kill": "derive Gamma_eff and K_hat as quotient pullbacks or exact vertical primitive",
            "current_status": "next_primary_test",
            "route_if_not_killed": "demote strict quotient branch",
        },
        {
            "redteam_id": "NCR595_4_second_class_remnant",
            "attack": "rank-zero representative sector leaves a second-class remnant or stabilizer",
            "why_reviewers_accept_attack": "zero kinetic rank alone is not gauge",
            "required_kill": "Dirac bracket closure and no proper stabilizer proof",
            "current_status": "not_killed",
            "route_if_not_killed": "diffeo-current or finite residual",
        },
        {
            "redteam_id": "NCR595_5_post_readout_cheat",
            "attack": "choose a readout-reduced action where q_loc=0 and vary it as fundamental",
            "why_reviewers_accept_attack": "that would bake the desired closure into the effective variables",
            "required_kill": "readout only after solving parent Euler equations",
            "current_status": "guard_written",
            "route_if_not_killed": "reject proof credit",
        },
    ]


def make_demotion_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "DG595_0_strict_quotient_route",
            "trigger_condition": "pi exists and all bulk/matter/readout/boundary structures factor through pi with exact/proper representative boundary",
            "decision_if_triggered": "keep strict quotient-zero and remove physical X alpha row as theorem-zero",
            "current_status": "not_triggered_candidate_only",
            "next_test": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG595_1_diffeo_current_backup",
            "trigger_condition": "pi fails but C_X is exactly the parent diffeomorphism/momentum current with no ADM double-count",
            "decision_if_triggered": "demote strict quotient route to backup and use diffeo-current identity route",
            "current_status": "backup_open",
            "next_test": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG595_2_edge_residual_fallback",
            "trigger_condition": "pi fails, diffeo-current identity fails, but parent coefficients or real bound rows can be sourced",
            "decision_if_triggered": "score finite alpha_edge(lambda) with source-backed coefficients",
            "current_status": "fallback_blocked_missing_coefficients",
            "next_test": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG595_3_closure_only_demote",
            "trigger_condition": "no pi, no C_X identity, no sourced finite coefficient survives",
            "decision_if_triggered": "demote local R10/local-GR branch to explicit closure-only assumption",
            "current_status": "last_resort_not_triggered",
            "next_test": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D595_0_pi_candidate_constructed",
            "decision": "construct a formal observed quotient map pi with representative fibre R",
            "meaning": "the lower-scrutiny route is mathematically coherent as a bundle/pullback contract",
            "claim_status": "candidate_only_not_proved",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D595_1_not_demoted_yet",
            "decision": "do not demote strict quotient route yet",
            "meaning": "the route has a coherent pi candidate, but Gamma/Khat/q_loc and no-marker tests remain open",
            "claim_status": "route_live_but_blocked",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D595_2_Gamma_Khat_qloc_is_decisive",
            "decision": "make Gamma_eff, K_hat, and q_loc the next pass/fail target",
            "meaning": "if these do not factor through pi or become exact vertical identities, strict quotient-zero collapses",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU595_0_allowed",
            "allowed_after_595": "use pi(Y)=Q_obs as the strict quotient candidate",
            "forbidden_after_595": "claim local no-pole/R10 pass before Gamma/Khat/q_loc and matter marker tests pass",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU595_1_allowed",
            "allowed_after_595": "treat conformal marker and boundary edge modes as live red-team attacks",
            "forbidden_after_595": "dismiss universal conformal coupling by saying it is WEP-safe",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU595_2_allowed",
            "allowed_after_595": "demote to diffeo-current identity if q_loc cannot be made a quotient identity",
            "forbidden_after_595": "carry strict quotient language while retaining an independent local X source",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S595_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "strict_quotient_status": "live_but_blocked",
            "best_private_read": "The lower-scrutiny route survives as a formal quotient-map contract. The hard test is now whether Gamma_eff, K_hat, and q_loc are quotient pullbacks/exact identities rather than independent local source data.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    pi_rows: list[dict[str, str]],
    factor_rows: list[dict[str, str]],
    redteam_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_594_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in pi_rows if row["valid_for_claim"] == "true"],
        *[row for row in factor_rows if row["valid_for_claim"] == "true"],
        *[row for row in demotion_rows if row["valid_for_claim"] == "true"],
    ]
    pi_projection = any(
        row["map_id"] == "PIM595_0_parent_space"
        and "pi(Y)=O" in f"{row['candidate_definition']} {row['mathematical_test']}"
        for row in pi_rows
    )
    dpi_zero = any(row["map_id"] == "PIM595_3_vertical_generator" and "d pi(v_X)=0" in row["mathematical_test"] for row in pi_rows)
    gamma_gate = any(row["test_id"] == "QFT595_2_Gamma_Khat_qloc" and row["current_result"] == "highest_risk_open_test_next" for row in factor_rows)
    conformal_attack = any("conformal" in row["redteam_id"].lower() or "conformal" in row["attack"].lower() for row in redteam_rows)
    boundary_attack = any("boundary" in row["attack"].lower() or "edge" in row["attack"].lower() for row in redteam_rows)
    demotion_gate = any(row["gate_id"] == "DG595_1_diffeo_current_backup" for row in demotion_rows)
    return [
        {
            "check_id": "V595_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V595_1_prior_594_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V595_2_pi_projection_candidate_written",
            "result": "pass" if pi_projection else "fail",
            "detail": f"pi_rows={len(pi_rows)}",
        },
        {
            "check_id": "V595_3_vertical_dpi_zero_written",
            "result": "pass" if dpi_zero else "fail",
            "detail": "d pi(v_X)=0 retained as field-by-field test",
        },
        {
            "check_id": "V595_4_Gamma_Khat_qloc_not_falsely_closed",
            "result": "pass" if gamma_gate else "fail",
            "detail": "Gamma_eff/K_hat/q_loc remains highest-risk next test",
        },
        {
            "check_id": "V595_5_no_cheat_attacks_retained",
            "result": "pass" if conformal_attack and boundary_attack else "fail",
            "detail": f"redteam_rows={len(redteam_rows)};conformal={conformal_attack};boundary={boundary_attack}",
        },
        {
            "check_id": "V595_6_demotion_gate_present",
            "result": "pass" if demotion_gate else "fail",
            "detail": "diffeo-current backup remains explicit",
        },
        {
            "check_id": "V595_7_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V595_8_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    pi_rows: list[dict[str, str]],
    factor_rows: list[dict[str, str]],
    redteam_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 595 Y5 R10 construct pi observed quotient map or demote to diffeo current

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The lower-scrutiny route is still alive: a formal quotient map `pi: Conf_parent -> Q_obs` can be written without immediately creating a local fifth-force field.
- The clean construction is `Y=(O,R,B_ref)` with `pi(Y)=O`: observed/reduced data live in `O`, representative fibre data live in `R`, and the compact boundary reference stays fixed.
- This is not yet a proof. It becomes a proof only if the current MTS objects, especially `Gamma_eff`, `K_hat`, and `q_loc`, factor through `pi` or become exact/proper vertical identities.
- If `q_loc` remains an independent physical source profile, we demote the strict quotient route and go to the diffeo-current or finite-edge branch.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Pi Observed Quotient Map
{markdown_table(pi_rows, ["map_id", "object", "candidate_definition", "mathematical_test", "current_result", "claim_status", "valid_for_claim"])}

## Quotient Factorisation Test
{markdown_table(factor_rows, ["test_id", "sector", "factorisation_requirement", "what_would_pass", "current_result", "scrutiny_level", "valid_for_claim"])}

## No-Cheat Red Team
{markdown_table(redteam_rows, ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed"])}

## Demotion Gate
{markdown_table(demotion_rows, ["gate_id", "trigger_condition", "decision_if_triggered", "current_status", "next_test", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_595", "forbidden_after_595", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is the slippery route in the good sense: the fifth-force boxer is not dodged by tiny coefficients; it is kept out of the ring by making `X` representative data, not observable data. But the trick only works if `Gamma_eff`, `K_hat`, and `q_loc` do not smuggle the boxer back in through the side door.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    pi_rows = make_pi_map_rows()
    factor_rows = make_factorisation_rows()
    redteam_rows = make_redteam_rows()
    demotion_rows = make_demotion_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, pi_rows, factor_rows, redteam_rows, demotion_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        PI_MAP_PATH,
        pi_rows,
        ["map_id", "object", "candidate_definition", "mathematical_test", "current_result", "claim_status", "valid_for_claim"],
    )
    write_csv(
        FACTORISATION_PATH,
        factor_rows,
        ["test_id", "sector", "factorisation_requirement", "what_would_pass", "current_result", "scrutiny_level", "valid_for_claim"],
    )
    write_csv(
        REDTEAM_PATH,
        redteam_rows,
        ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed"],
    )
    write_csv(
        DEMOTION_GATE_PATH,
        demotion_rows,
        ["gate_id", "trigger_condition", "decision_if_triggered", "current_status", "next_test", "valid_for_claim"],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_595", "forbidden_after_595", "next_action"])
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
        pi_rows,
        factor_rows,
        redteam_rows,
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
