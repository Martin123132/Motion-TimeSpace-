from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_888_parent_spine_readout_clause_integration_attempt_not_closed_finite_trace_carrier_runner_skeleton_built_nonclaim"
CLAIM_CEILING = "parent_spine_integration_attempt_and_finite_trace_runner_skeleton_only_no_readout_promotion_no_cT_zero_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "889-Y5-R10-finite-trace-carrier-runner-dryrun-or-parent-spine-clause-repair.md"


SOURCE_SPECS = [
    {
        "source_id": "887_doc",
        "path": ROOT / "887-Y5-R10-readout-only-boundary-support-action-clause-or-finite-trace-carrier-source-pack.md",
        "needle": "clean local-GR route has been narrowed to one parent-spine clause",
        "role": "immediate readout-clause handoff",
    },
    {
        "source_id": "887_validation",
        "path": OUT / "P8_Y5_BRR545_887_VALIDATION.csv",
        "needle": "V887_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "887_readout_clause",
        "path": OUT / "P8_Y5_R10_887_READOUT_BOUNDARY_CLAUSE.csv",
        "needle": "RO887_6_clause_verdict",
        "role": "clause being tested for parent-spine integration",
    },
    {
        "source_id": "887_source_pack",
        "path": OUT / "P8_Y5_R10_887_FINITE_TRACE_SOURCE_PACK.csv",
        "needle": "FT887_7_source_provenance",
        "role": "finite trace carrier fallback inputs",
    },
    {
        "source_id": "177_parent_action",
        "path": ROOT / "177-parent-action-perturbation-local-GR-contract.md",
        "needle": "S_parent =",
        "role": "parent action contract and boundary slot",
    },
    {
        "source_id": "346_north_star",
        "path": ROOT / "346-GR-and-derivation-north-star-spine.md",
        "needle": "MTS does not yet derive local GR/PPN.",
        "role": "GR derivation north-star policy",
    },
    {
        "source_id": "512_symbol_map",
        "path": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "needle": "q_loc^nu = P_loc",
        "role": "q_loc/Gamma/Khat residual map",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needle": "local_GR_claim | hardest_next_blocker",
        "role": "local GR reduction stack and remaining blockers",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero != physical spurion",
        "role": "source-at-zero/no-spurion discipline",
    },
    {
        "source_id": "446_no_cheat",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "readout variables enter only after variation and cannot backreact",
        "role": "readout-after-variation no-cheat rule",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "q_loc[U] is a compact-domain restriction/jet quotient",
        "role": "compact q_loc quotient contract",
    },
    {
        "source_id": "437_R10_contract",
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needle": "Anything else remains symbolic and blocks R10 promotion.",
        "role": "R10 finite-carrier claim contract",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(stringify(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "tested whether the 887 readout-only boundary-support clause can be inserted into the existing parent/local-GR spine and converted the fallback source pack into a finite trace carrier runner skeleton",
            "best_partial_result": "the clause is policy-compatible with source-at-zero/readout-after-variation discipline and fits the boundary slot as a subgate, but no existing parent-spine file jointly signs boundary support, compact q_loc exclusion, no-tail, matter no-marker, and local-GR reduction",
            "hard_blockers": "no parent-integrated R_tr clause, no signed P_tr local rank zero, no no-tail/boundary theorem, no q_loc Ward/Noether zero proof, no finite Z_tr/lambda_tr/Q_tr response coefficients, no sourced R10/PPN/clock/orbital comparison rows",
            "what_is_not_claimed": "P_tr readout-only theorem, c_T=0, finite trace carrier pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def parent_spine_integration_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "integration_id": "PSI888_0_parent_action_slot",
            "source_anchor": "177_parent_action",
            "test": "does the parent action already contain a legitimate boundary/readout slot for R_tr",
            "finding": "177 has an S_boundary/local-GR contract slot, so the clause has a place to live, but it does not explicitly integrate RO887_0 through RO887_5",
            "status": "slot_exists_clause_not_integrated",
            "claim_effect": "no promotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "integration_id": "PSI888_1_north_star_policy",
            "source_anchor": "346_north_star",
            "test": "does the clause satisfy the GR derivation north-star by itself",
            "finding": "346 still says MTS does not yet derive local GR/PPN; trace readout silence is only one subgate under the local EH/Newton/PPN spine",
            "status": "compatible_not_sufficient",
            "claim_effect": "keeps local GR blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "integration_id": "PSI888_2_q_loc_residual_map",
            "source_anchor": "512_symbol_map",
            "test": "can R_tr be used as a post-readout cancellation of q_loc",
            "finding": "512 requires q_loc to vanish by parent Ward/Noether variation or remain an explicit residual; the readout clause cannot be smuggled in after variation to cancel Gamma_eff/K_hat terms",
            "status": "must_be_prevariation_or_residual",
            "claim_effect": "no q_loc zero claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "integration_id": "PSI888_3_local_GR_spine",
            "source_anchor": "654_local_gr_spine",
            "test": "does closing the trace readout branch close the local-GR stack",
            "finding": "654 keeps EH operator selection, source charge/GM normalization, PPN vector, boundary no-flux, R10 and transition control open; trace readout addresses only one extra-sector channel",
            "status": "partial_subgate_only",
            "claim_effect": "local GR remains fail_for_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "integration_id": "PSI888_4_source_at_zero_policy",
            "source_anchor": "338_readout_gate;446_no_cheat",
            "test": "is source-at-zero/readout-after-variation allowed as a discipline",
            "finding": "yes as a private policy shape: readout variables may enter after variation and at zero source, provided they cannot backreact or cancel a residual",
            "status": "policy_compatible",
            "claim_effect": "permits a repair target but not a theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "integration_id": "PSI888_5_integration_verdict",
            "source_anchor": "887_readout_clause;177_parent_action;346_north_star;512_symbol_map;654_local_gr_spine",
            "test": "are RO887_0 through RO887_5 signed by one parent spine/action together with local-GR requirements",
            "finding": "no; the corpus supports the shape of the clause, but not its parent integration or its use as a local-GR theorem",
            "status": "not_parent_integrated",
            "claim_effect": "finite trace carrier runner skeleton remains mandatory as fallback",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def compatibility_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G888_0_source_at_zero",
            "clause_tested": "source-at-zero physical-spurion exclusion",
            "evidence": "338 and 446 support readout-after-variation/source-at-zero as a no-cheat rule",
            "gate_result": "pass_private_policy",
            "reason_claim_still_blocked": "policy compatibility is not a parent-integrated trace theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G888_1_boundary_support_no_tail",
            "clause_tested": "trace readout has boundary/FLRW support and no compact local tail",
            "evidence": "887 states the required clause; 870/887 do not yet sign it from the parent action",
            "gate_result": "fail_open",
            "reason_claim_still_blocked": "a local tail would create retained c_T/H_tr response",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G888_2_q_loc_exclusion",
            "clause_tested": "compact q_loc ignores R_tr/global trace endpoint data",
            "evidence": "874 gives a compact-domain quotient contract; 512 still demands parent Ward/Noether zero or residual",
            "gate_result": "fail_open",
            "reason_claim_still_blocked": "q_loc/Gamma_eff/K_hat cannot be zeroed by readout rhetoric",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G888_3_matter_no_marker",
            "clause_tested": "matter constants and charges carry no trace marker",
            "evidence": "887 requires no-marker descent; 873-style source-zero logic is not parent-integrated here",
            "gate_result": "fail_open",
            "reason_claim_still_blocked": "WEP/clock/EM/source-charge channels remain possible",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G888_4_EH_PPN_source_normalization",
            "clause_tested": "local EH/Newton/PPN/source normalization stack",
            "evidence": "346 and 654 keep this broader local-GR stack open",
            "gate_result": "outside_trace_clause_blocked",
            "reason_claim_still_blocked": "even a closed trace readout branch would not alone derive local GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G888_5_total_gate",
            "clause_tested": "readout clause integration as a route to c_T/local-GR silence",
            "evidence": "one policy-compatible pass and multiple parent-signature failures",
            "gate_result": "fail_for_claim",
            "reason_claim_still_blocked": "the clean route is narrowed, not completed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def finite_trace_runner_skeleton_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "runner_id": "RUN888_0_input_schema",
            "mode": "schema",
            "required_inputs": "P_tr,H_tr,Z_tr,mu_tr^2,lambda_tr,J_tr,Q_tr/m,R10 alpha(lambda),PPN coefficients,clock/WEP response,orbital/GM response,source provenance",
            "formula_or_check": "all inputs must be numeric/sourced with units before any comparison can be valid_for_claim=true",
            "current_status": "MISSING_PARENT_AND_ARENA_INPUTS",
            "runner_action": "reject claim rows and emit blocker ledger",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RUN888_1_zero_branch",
            "mode": "conditional_zero",
            "required_inputs": "parent-integrated RO887_0 through RO887_5 plus 886 rank-zero/no-pole/source-cokernel theorem",
            "formula_or_check": "if parent_integrated_readout=true then alpha_tr=0, PPN_trace=0, clock_trace=0 only for the trace channel",
            "current_status": "BLOCKED_NOT_PARENT_INTEGRATED",
            "runner_action": "do not execute zero-return claim branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RUN888_2_finite_branch_R10",
            "mode": "finite_carrier_R10",
            "required_inputs": "Z_tr,lambda_tr,Q_tr^A/m_A,Q_tr^B/m_B,full sourced alpha_bound(lambda)",
            "formula_or_check": "alpha_tr_AB=(Q_tr^A/m_A)(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs); pass only if abs(alpha_tr)<=alpha_bound(lambda_tr)",
            "current_status": "MISSING_COEFFICIENTS_AND_BOUND_CURVE",
            "runner_action": "prepare nonclaim dry-run only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RUN888_3_PPN_clock_orbital",
            "mode": "finite_carrier_local_arenas",
            "required_inputs": "C_T_gamma,C_T_beta,C_T_clock_i,Delta(Q_tr/m)_AB,orbital Yukawa or GM-absorption response",
            "formula_or_check": "compare residual vector against PPN, WEP/clock, and orbital bounds with baseline/source normalization recorded",
            "current_status": "MISSING_RESPONSE_OPERATORS",
            "runner_action": "keep all arenas blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RUN888_4_claim_policy",
            "mode": "claim_guard",
            "required_inputs": "no MISSING markers and every source path exists",
            "formula_or_check": "valid_for_claim can only turn true after source-backed numeric rows and acceptance gates pass",
            "current_status": "BLOCKED_BY_MISSING_MARKERS",
            "runner_action": "force nonclaim outputs",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RUN888_5_runner_verdict",
            "mode": "verdict",
            "required_inputs": "either parent-integrated zero theorem or finite carrier coefficients/bounds",
            "formula_or_check": "current corpus has neither, so runner is a skeleton and blocker ledger only",
            "current_status": "SKELETON_ONLY_NO_PHYSICAL_RUN",
            "runner_action": "select 889 dry-run/repair target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG888_0_readout_integration",
            "promotion_target": "P_tr is parent-integrated readout-only boundary observable",
            "required_to_pass": "RO887_0 through RO887_5 signed inside one parent action/spine",
            "current_evidence": "policy-compatible shape, not integrated",
            "gate_result": "fail_for_claim",
            "next_action": "repair parent spine clause or keep finite runner fallback",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG888_1_cT_zero",
            "promotion_target": "trace branch gives c_T=0/zero local carrier",
            "required_to_pass": "readout integration plus 886 rank-zero/no-pole/source-cokernel premises",
            "current_evidence": "conditional theorem only",
            "gate_result": "fail_for_claim",
            "next_action": "do not claim c_T silence",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG888_2_finite_runner_pass",
            "promotion_target": "finite trace carrier passes R10/PPN/clock/orbital tests",
            "required_to_pass": "numeric sourced coefficients and bound curves with accepted residual comparisons",
            "current_evidence": "runner skeleton only; missing parent inputs",
            "gate_result": "fail_for_claim",
            "next_action": "dry-run schema and blocker ledger in 889",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG888_3_local_GR",
            "promotion_target": "local GR/Newton is derived",
            "required_to_pass": "trace branch plus EH/source-normalization/PPN/q_loc/boundary branches all closed",
            "current_evidence": "trace branch not closed and broader stack remains open",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked and derivation-first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC888_0_selected",
            "route": "finite_trace_carrier_runner_dryrun_or_parent_spine_clause_repair",
            "status": "selected",
            "reason": "the parent-spine integration attempt found policy compatibility but no parent signature, so the next honest step is either repair the missing clause or dry-run the finite-carrier runner without claims",
            "include": "schema dry-run, missing-input blocker ledger, optional parent-clause repair target, no promotion",
            "exclude": "public claim, GitHub action, formalization-workbench edits, fitted coupling, R10/PPN/local-GR pass",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG888_0_no_readout_promotion",
            "forbidden_claim": "P_tr is proven readout-only",
            "status": "forbidden",
            "reason": "888 finds compatibility but no parent-spine integration",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG888_1_no_cT_zero",
            "forbidden_claim": "c_T=0 or trace branch has no local carrier",
            "status": "forbidden",
            "reason": "rank-zero/no-pole/source-cokernel premises remain conditional",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG888_2_no_finite_carrier_pass",
            "forbidden_claim": "finite trace carrier passes local tests",
            "status": "forbidden",
            "reason": "runner is a skeleton with missing parent coefficients and arena bounds",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG888_3_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace branch and wider local-GR stack are still open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG888_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "888 cleanly pins the route: repair parent clause or run finite-carrier blocker dry-run",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D888_0",
            "finding": "parent_spine_slot_exists",
            "reason": "177 provides a boundary/action slot compatible with a readout clause",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D888_1",
            "finding": "readout_clause_not_integrated",
            "reason": "no current parent spine/action signs source-at-zero boundary support, q_loc exclusion, no-tail, and matter no-marker jointly",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D888_2",
            "finding": "finite_runner_skeleton_built",
            "reason": "the 887 finite source pack is converted into a runner skeleton that refuses claims while parent coefficients and arena bounds are missing",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "either dry-run the finite trace carrier runner to prove the blocker logic end-to-end, or repair the parent-spine readout clause by writing the missing boundary/no-tail/q_loc/no-marker parent signatures",
            "include": "nonclaim runner dry-run, missing-input ledger, parent-clause repair option, validation that all local claims remain blocked",
            "exclude": "R10/PPN/local-GR pass, numeric claim without sourced coefficients, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_887_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_887_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(row_groups: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)) != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    integration_rows: list[dict[str, object]],
    compatibility_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    integration_ids = {row["integration_id"] for row in integration_rows}
    runner_statuses = [str(row["current_status"]) for row in runner_rows]
    row_groups = [
        source_rows,
        summary_rows,
        integration_rows,
        compatibility_rows,
        runner_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    ]
    checks = [
        {
            "check_id": "V888_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all 887 and parent-spine source paths exist and needles are present",
        },
        {
            "check_id": "V888_1_prior_887_clean",
            "result": "pass" if prior_887_clean() else "fail",
            "detail": "P8_Y5_BRR545_887_VALIDATION.csv clean",
        },
        {
            "check_id": "V888_2_parent_spine_rows_cover_core_sources",
            "result": "pass" if {"PSI888_0_parent_action_slot", "PSI888_1_north_star_policy", "PSI888_2_q_loc_residual_map", "PSI888_3_local_GR_spine", "PSI888_5_integration_verdict"}.issubset(integration_ids) else "fail",
            "detail": "177/346/512/654 and final integration verdict represented",
        },
        {
            "check_id": "V888_3_integration_not_promoted",
            "result": "pass" if any(row["integration_id"] == "PSI888_5_integration_verdict" and row["status"] == "not_parent_integrated" for row in integration_rows) else "fail",
            "detail": "readout clause remains not parent-integrated",
        },
        {
            "check_id": "V888_4_source_at_zero_compatible_but_insufficient",
            "result": "pass" if any(row["gate_id"] == "G888_0_source_at_zero" and row["gate_result"] == "pass_private_policy" for row in compatibility_rows) and any(row["gate_id"] == "G888_5_total_gate" and row["gate_result"] == "fail_for_claim" for row in compatibility_rows) else "fail",
            "detail": "source-at-zero policy compatibility does not promote the claim",
        },
        {
            "check_id": "V888_5_finite_runner_skeleton_present",
            "result": "pass" if len(runner_rows) >= 6 and any("SKELETON_ONLY" in status for status in runner_statuses) and all(("MISSING" in status or "BLOCKED" in status or "SKELETON" in status) for status in runner_statuses) else "fail",
            "detail": "finite trace runner skeleton is present and blocked by missing inputs",
        },
        {
            "check_id": "V888_6_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V888_7_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V888_8_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V888_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V888_10_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V888_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    integration_rows: list[dict[str, object]],
    compatibility_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 888 - Y5/R10 Parent-Spine Readout Clause Integration or Finite Trace Carrier Runner",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the 887 readout-only clause is compatible with the parent-spine discipline but not integrated as a theorem**. The existing corpus has a boundary/action slot and source-at-zero policy support, but it does not jointly sign boundary support, compact `q_loc` exclusion, no-tail/no-flux, matter no-marker descent, and the wider local-GR/EH/PPN stack. Therefore the honest fallback is a finite trace carrier runner skeleton, with every local arena still blocked by missing parent coefficients or sourced bounds.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Parent Spine Integration",
        md_table(integration_rows),
        "",
        "## Compatibility Gates",
        md_table(compatibility_rows),
        "",
        "## Finite Trace Runner Skeleton",
        md_table(runner_rows),
        "",
        "## Promotion Gates",
        md_table(promotion_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(guard_rows),
        "",
        "## Decisions",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    integration_rows = parent_spine_integration_rows(generated_utc)
    compatibility_rows = compatibility_gate_rows(generated_utc)
    runner_rows = finite_trace_runner_skeleton_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        summary_rows,
        integration_rows,
        compatibility_rows,
        runner_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    )

    outputs = {
        "P8_Y5_R10_888_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_888_PARENT_SPINE_INTEGRATION.csv": integration_rows,
        "P8_Y5_R10_888_COMPATIBILITY_GATES.csv": compatibility_rows,
        "P8_Y5_R10_888_FINITE_TRACE_RUNNER_SKELETON.csv": runner_rows,
        "P8_Y5_R10_888_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_888_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_888_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_888_DECISION.csv": decision_rows_,
        "P8_Y5_R10_888_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_888_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_888_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "888-Y5-R10-parent-spine-readout-clause-integration-or-finite-trace-carrier-runner.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        integration_rows,
        compatibility_rows,
        runner_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_888_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
