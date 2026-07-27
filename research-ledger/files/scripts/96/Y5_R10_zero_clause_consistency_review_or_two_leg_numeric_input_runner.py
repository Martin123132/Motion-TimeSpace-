from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "635-Y5-R10-zero-clause-consistency-review-or-two-leg-numeric-input-runner.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_zero_clause_consistency_review_or_two_leg_numeric_input_runner.py"

STATUS = "Y5_R10_zero_clause_consistency_review_blocks_adoption_two_leg_numeric_runner_staged_nonclaim"
CLAIM_CEILING = "consistency_review_and_two_leg_runner_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "636-Y5-R10-zero-clause-covariance-and-constants-repair-or-finite-input-sourcing.md"

PRIOR_634_DOC = ROOT / "634-Y5-R10-zero-branch-parent-clause-draft-or-two-leg-input-fill.md"
PRIOR_634_VALIDATION = MTS_DIR / "P8_Y5_BRR545_634_VALIDATION.csv"
PRIOR_634_CLAUSE = MTS_DIR / "P8_Y5_R10_634_ZERO_BRANCH_PARENT_CLAUSE_DRAFT.csv"
PRIOR_634_CHAIN = MTS_DIR / "P8_Y5_R10_634_ZERO_CLAUSE_CONSEQUENCE_CHAIN.csv"
PRIOR_634_OBLIGATIONS = MTS_DIR / "P8_Y5_R10_634_ZERO_CLAUSE_CONSISTENCY_OBLIGATIONS.csv"
PRIOR_634_FALLBACK = MTS_DIR / "P8_Y5_R10_634_TWO_LEG_FALLBACK_INPUT_FILL.csv"
PRIOR_632_ENVELOPE = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_635_SOURCE_REGISTER.csv"
CONSISTENCY_REVIEW = MTS_DIR / "P8_Y5_R10_635_ZERO_CLAUSE_CONSISTENCY_REVIEW.csv"
SECTOR_IMPACT = MTS_DIR / "P8_Y5_R10_635_SECTOR_IMPACT_MATRIX.csv"
ADOPTION_GATE = MTS_DIR / "P8_Y5_R10_635_ZERO_CLAUSE_ADOPTION_GATE.csv"
TWO_LEG_INPUT_STATUS = MTS_DIR / "P8_Y5_R10_635_TWO_LEG_INPUT_STATUS.csv"
TWO_LEG_NUMERIC_RUNNER = MTS_DIR / "P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_635_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_635_ROUTE_UPDATE.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_635_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_635_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_635_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_634_DOC, "immediate zero-clause draft checkpoint"),
        (PRIOR_634_VALIDATION, "634 validation gate"),
        (PRIOR_634_CLAUSE, "zero-branch parent clause draft"),
        (PRIOR_634_CHAIN, "zero-clause consequence chain"),
        (PRIOR_634_OBLIGATIONS, "consistency obligations"),
        (PRIOR_634_FALLBACK, "two-leg fallback input fill"),
        (PRIOR_632_ENVELOPE, "two-leg pressure envelope"),
        (ROOT / "241-C-silence-screening-or-parent-selection-theorem.md", "conformal trace-source no-go"),
        (ROOT / "360-universal-matter-coupling-theorem-attempt.md", "universal matter coupling attempt"),
        (ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "vertical observation theorem"),
        (ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "primitive quotient/no-marker clause"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC635_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def consistency_review_rows() -> list[dict[str, Any]]:
    return [
        {
            "review_id": "CR635_0_scope",
            "obligation": "zero clause governs ordinary local matter coupling, not all MTS effective variables",
            "review_result": "guarded_pass",
            "evidence": "ZP634 and CC634_5 explicitly branch-scope the clause and preserve quotient observables for cosmology/galaxies",
            "remaining_gap": "must propagate this wording into the future unification spine",
            "adoption_blocker": "false",
            "valid_for_claim": "false",
        },
        {
            "review_id": "CR635_1_covariance",
            "obligation": "q, Obs(q), and S_matter are covariant/functorial",
            "review_result": "open_blocker",
            "evidence": "conditional functor language exists, but q/Obs are not parent-derived as covariant maps",
            "remaining_gap": "derive q and Obs as parent objects rather than gauge-fixed readout conventions",
            "adoption_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "review_id": "CR635_2_no_shadow_frame",
            "obligation": "forbid hidden conformal/disformal/source-frame maps",
            "review_result": "open_blocker",
            "evidence": "ZP634 forbids A_g/B_g in ordinary matter and 241 warns unscreened conformal trace branches are not silent",
            "remaining_gap": "need a parent-level no-shadow-frame theorem, not only a policy clause",
            "adoption_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "review_id": "CR635_3_constants",
            "obligation": "EM, particle masses, clock constants, and species labels are Xhat-independent or quotient-owned",
            "review_result": "open_blocker",
            "evidence": "ZP634_3 states the rule; 566 identifies no-marker/no-spurion need",
            "remaining_gap": "EM/particle/time sectors need explicit constant-ownership audit",
            "adoption_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "review_id": "CR635_4_boundary",
            "obligation": "vertical boundary/projector/domain currents have zero ordinary-matter projection",
            "review_result": "open_blocker",
            "evidence": "ZP634_5 states exact/gauge/Ward-owned or retained outside ordinary matter",
            "remaining_gap": "boundary/projector silence remains historically retained/closure-only",
            "adoption_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "review_id": "CR635_5_gr_limit",
            "obligation": "after zero matter coupling, EH/PPN/operator branch still reduces to GR",
            "review_result": "open_blocker",
            "evidence": "CC634_4 correctly says local tests become operator-sector questions",
            "remaining_gap": "EH-only/PPN/nohair operator reduction remains separate and not solved by c_g=0",
            "adoption_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def sector_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector_id": "SI635_0_local_R10",
            "sector": "R10/fifth-force",
            "if_zero_clause_adopted": "ordinary matter source/test charges vanish",
            "review_status": "would_help_strongly_but_not_adopted",
            "risk_if_unreviewed": "hidden boundary or shadow-frame current fakes a source leg",
            "next_check": "no-shadow-frame and boundary repair",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SI635_1_WEP_clock",
            "sector": "WEP/clocks/constants",
            "if_zero_clause_adopted": "direct Xhat matter charge is absent only if constants are Xhat-independent",
            "review_status": "open_blocker",
            "risk_if_unreviewed": "masses, charges, alpha, or clock constants become material spurions",
            "next_check": "constant-sector ownership audit",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SI635_2_EM_particle",
            "sector": "EM/particle",
            "if_zero_clause_adopted": "EM and particle parameters must be quotient-owned representation data",
            "review_status": "open_blocker",
            "risk_if_unreviewed": "the zero clause silently conflicts with charge/mass emergence work",
            "next_check": "EM/particle compatibility review",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SI635_3_cosmology_galaxy",
            "sector": "cosmology/galaxy effective sectors",
            "if_zero_clause_adopted": "large-scale MTS variables may survive only as quotient observables or gravitational-sector terms",
            "review_status": "guarded_pass_needs_spine_wording",
            "risk_if_unreviewed": "zero clause overkills useful phenomenology",
            "next_check": "scope wording in unification spine",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SI635_4_operator_GR",
            "sector": "EH/PPN/operator reduction",
            "if_zero_clause_adopted": "fifth-force leg is killed but non-EH operator residues remain possible",
            "review_status": "open_blocker",
            "risk_if_unreviewed": "mistaking c_g=0 for full local GR",
            "next_check": "EH/nohair/PPN residual branch",
            "valid_for_claim": "false",
        },
    ]


def adoption_gate_rows(review_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocker_rows = [row for row in review_rows if row["adoption_blocker"] == "true"]
    return [
        {
            "gate_id": "AG635_0_review_count",
            "requirement": "all six consistency obligations reviewed",
            "result": "pass" if len(review_rows) == 6 else "fail",
            "detail": f"review_rows={len(review_rows)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG635_1_no_blockers",
            "requirement": "zero adoption blockers",
            "result": "blocked" if blocker_rows else "pass",
            "detail": f"adoption_blockers={len(blocker_rows)}",
            "adoption_allowed": "false" if blocker_rows else "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG635_2_claim_status",
            "requirement": "do not claim c_g=0 unless adoption is allowed and source-backed",
            "result": "pass",
            "detail": "c_g_zero_claimed=false;ZP634 remains proposed selector",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def two_leg_input_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "TLS635_0_beta_source",
            "symbol": "beta_source",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "status": "not_scoreable",
            "needed_source": "delta S_source/dXhat or zero theorem",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TLS635_1_beta_test",
            "symbol": "beta_test",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "status": "not_scoreable",
            "needed_source": "delta S_test/dXhat or zero theorem",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TLS635_2_Z_eff",
            "symbol": "Z_eff",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "action_normalization",
            "status": "not_scoreable",
            "needed_source": "local quadratic action/Hessian",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TLS635_3_lambda_X",
            "symbol": "lambda_X",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "m",
            "status": "not_scoreable",
            "needed_source": "sqrt(Z_eff/M_X^2)",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TLS635_4_profile_factor",
            "symbol": "profile_factor(lambda)",
            "current_value": "pressure_scan_only",
            "units": "dimensionless",
            "status": "not_claim_source",
            "needed_source": "tau_R10,Qbar_XH,source geometry,curve promotion",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TLS635_5_cross_arena",
            "symbol": "tau_WEP,tau_PPN,tau_clock,tau_orbital",
            "current_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "status": "not_scoreable",
            "needed_source": "same charge law mapped to all local arenas",
            "valid_for_claim": "false",
        },
    ]


def two_leg_numeric_runner_rows() -> list[dict[str, Any]]:
    envelope_rows = read_csv(PRIOR_632_ENVELOPE)
    by_profile: dict[str, list[dict[str, str]]] = {}
    for row in envelope_rows:
        by_profile.setdefault(row.get("profile_factor", ""), []).append(row)
    out: list[dict[str, Any]] = []
    for profile_factor, rows in sorted(by_profile.items(), key=lambda item: float(item[0])):
        numeric_rows = [
            row
            for row in rows
            if parse_float(row.get("universal_two_leg_bound_abs_c_eff")) is not None
            and parse_float(row.get("lambda_value")) is not None
        ]
        if numeric_rows:
            tightest = min(numeric_rows, key=lambda row: parse_float(row["universal_two_leg_bound_abs_c_eff"]))
            tightest_bound = tightest["universal_two_leg_bound_abs_c_eff"]
            tightest_lambda = tightest["lambda_value"]
        else:
            tightest_bound = ""
            tightest_lambda = ""
        out.append(
            {
                "runner_id": f"TNR635_{len(out)}",
                "profile_factor": profile_factor,
                "law": "alpha_X=profile_factor*c_eff^2",
                "tightest_lambda_m": tightest_lambda,
                "tightest_abs_c_eff_pressure_bound": tightest_bound,
                "physical_inputs_ready": "false",
                "missing_inputs": "beta_source;beta_test;Z_eff;lambda_X;profile_factor_source;cross_arena_projection",
                "runner_status": "pressure_only_not_scoreable",
                "source": rel(PRIOR_632_ENVELOPE),
                "valid_for_claim": "false",
            }
        )
    return out


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D635_0_main_verdict",
            "decision": STATUS,
            "meaning": "zero clause is promising but blocked from adoption by open consistency obligations",
            "status": "review_progress_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D635_1_zero_clause",
            "decision": "do_not_adopt_yet",
            "meaning": "scope is guarded, but covariance, constants, shadow-frame, boundary, and GR-limit checks remain open",
            "status": "blocked_for_adoption",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D635_2_two_leg_runner",
            "decision": "numeric_pressure_runner_staged_nonclaim",
            "meaning": "profile-factor pressure summaries exist, but physical beta/Z/lambda/profile inputs are missing",
            "status": "fallback_pressure_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D635_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "neither zero clause nor finite branch is claim-ready",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU635_0_allowed",
            "allowed_after_635": "Repair zero-clause blockers one by one, starting with covariance and constants.",
            "forbidden_after_635": "Adopt ZP634 as a theorem or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU635_1_allowed",
            "allowed_after_635": "Use two-leg runner as private pressure only.",
            "forbidden_after_635": "Score finite coupling while beta/Z/lambda/profile inputs are missing.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU635_2_allowed",
            "allowed_after_635": "Keep c_g=0 as proposed selector, not proof.",
            "forbidden_after_635": "Let zero matter coupling erase separate EH/PPN/operator debts.",
            "next_action": NEXT_TARGET,
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC635_0_covariance_repair",
            "required_output": "define q, Q_obs, Obs(q), and S_matter as covariant/functorial parent objects",
            "success_condition": "ZP634 is not a gauge-fixed readout trick",
            "if_success": "one adoption blocker closes",
            "if_fail": "zero clause remains closure-only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC635_1_constants_repair",
            "required_output": "audit EM, masses, charges, clocks, and species labels for Xhat-independence",
            "success_condition": "no material/constant spurion reopens WEP/clock channels",
            "if_success": "constants blocker closes",
            "if_fail": "finite or mixed branch must be retained",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC635_2_finite_input_sourcing",
            "required_output": "source beta_source,beta_test,Z_eff,lambda_X,profile_factor if zero blockers cannot close",
            "success_condition": "two-leg runner becomes physically scoreable in private",
            "if_success": "R10/WEP/PPN/clock pressure can be evaluated",
            "if_fail": "finite branch remains pressure-only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(review_rows: list[dict[str, Any]], numeric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = [row for row in review_rows if row["adoption_blocker"] == "true"]
    unit_row = next((row for row in numeric_rows if row.get("profile_factor") == "1"), {})
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "zero_clause_adopted": "false",
            "adoption_blockers": len(blockers),
            "guarded_passes": len([row for row in review_rows if row["review_result"] == "guarded_pass"]),
            "two_leg_runner_rows": len(numeric_rows),
            "unit_profile_tightest_abs_c_eff_pressure_bound": unit_row.get("tightest_abs_c_eff_pressure_bound", ""),
            "unit_profile_tightest_lambda_m": unit_row.get("tightest_lambda_m", ""),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    numeric_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_634_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    blockers = [row for row in review_rows if row.get("adoption_blocker") == "true"]
    adoption_allowed = any(row.get("adoption_allowed") == "true" for row in gate_rows)
    input_claim_rows = [row for row in input_rows if row.get("valid_for_claim") == "true"]
    numeric_claim_rows = [row for row in numeric_rows if row.get("valid_for_claim") == "true"]
    unit_row = next((row for row in numeric_rows if row.get("profile_factor") == "1"), {})
    unit_bound = parse_float(unit_row.get("tightest_abs_c_eff_pressure_bound"))
    return [
        {
            "check_id": "V635_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V635_1_prior_634_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V635_2_consistency_review_complete",
            "result": "pass" if len(review_rows) == 6 and len(blockers) >= 1 else "fail",
            "detail": f"review_rows={len(review_rows)};blockers={len(blockers)}",
        },
        {
            "check_id": "V635_3_sector_impact_complete",
            "result": "pass" if len(sector_rows) == 5 else "fail",
            "detail": f"sector_rows={len(sector_rows)}",
        },
        {
            "check_id": "V635_4_adoption_blocked",
            "result": "pass" if len(gate_rows) == 3 and not adoption_allowed else "fail",
            "detail": f"gate_rows={len(gate_rows)};adoption_allowed={bool_text(adoption_allowed)}",
        },
        {
            "check_id": "V635_5_two_leg_inputs_nonclaim_missing",
            "result": "pass" if len(input_rows) == 6 and not input_claim_rows else "fail",
            "detail": f"input_rows={len(input_rows)};claim_rows={len(input_claim_rows)}",
        },
        {
            "check_id": "V635_6_numeric_pressure_runner_nonclaim",
            "result": "pass" if len(numeric_rows) == 4 and not numeric_claim_rows and unit_bound is not None and unit_bound < 0.05 else "fail",
            "detail": f"numeric_rows={len(numeric_rows)};claim_rows={len(numeric_claim_rows)};unit_bound={unit_bound}",
        },
        {
            "check_id": "V635_7_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V635_8_no_local_claim",
            "result": "pass",
            "detail": "zero_clause_adopted=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def build_doc(
    source_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    numeric_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 635 Y5 R10 zero clause consistency review or two leg numeric input runner",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- The zero clause is promising but not adoptable yet.\n"
            "- Scope passes as a guarded clause, but covariance, shadow-frame exclusion, constants, boundary silence, and GR/operator reduction remain blockers.\n"
            "- Therefore `c_g=0` is still not claimed.\n"
            "- The two-leg finite runner is staged as pressure-only; physical beta/Z/lambda/profile inputs are still missing.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Zero Clause Consistency Review\n" + markdown_table(review_rows),
            "## Sector Impact Matrix\n" + markdown_table(sector_rows),
            "## Zero Clause Adoption Gate\n" + markdown_table(gate_rows),
            "## Two-Leg Input Status\n" + markdown_table(input_rows),
            "## Two-Leg Numeric Input Runner\n" + markdown_table(numeric_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Next Contract\n" + markdown_table(contracts),
            "## Nonclaim Summary\n" + markdown_table(summary),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    review_rows = consistency_review_rows()
    sector_rows = sector_impact_rows()
    gate_rows = adoption_gate_rows(review_rows)
    input_rows = two_leg_input_status_rows()
    numeric_rows = two_leg_numeric_runner_rows()
    decisions = decision_rows()
    routes = route_update_rows()
    contracts = next_contract_rows()
    summary = nonclaim_summary_rows(review_rows, numeric_rows)
    validations = validation_rows(source_rows, review_rows, sector_rows, gate_rows, input_rows, numeric_rows, contracts)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(CONSISTENCY_REVIEW, review_rows)
    write_csv(SECTOR_IMPACT, sector_rows)
    write_csv(ADOPTION_GATE, gate_rows)
    write_csv(TWO_LEG_INPUT_STATUS, input_rows)
    write_csv(TWO_LEG_NUMERIC_RUNNER, numeric_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(NEXT_CONTRACT, contracts)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            review_rows,
            sector_rows,
            gate_rows,
            input_rows,
            numeric_rows,
            decisions,
            routes,
            contracts,
            summary,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )
    failed = [row for row in validations if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))


if __name__ == "__main__":
    main()
