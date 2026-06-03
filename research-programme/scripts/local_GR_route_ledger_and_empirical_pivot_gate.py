#!/usr/bin/env python3
"""Checkpoint 225: consolidate local-GR route and choose next pivot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_225_NAME = "local-GR-route-ledger-and-empirical-pivot-gate"
RUN_218 = RUNS_ROOT / "20260601-000035-sidecar-readonly-join-contract-or-local-qloc"
RUN_220 = RUNS_ROOT / "20260601-000037-Jrel-local-trivial-representative-or-closure-bound"
RUN_222 = RUNS_ROOT / "20260601-000039-parent-X-sector-degree-count-and-boundary-action"
RUN_224 = RUNS_ROOT / "20260601-000041-defect-potential-Vdef-or-X-route-demotion"

STATUS = "local_GR_route_consolidated_no_promotion_pivot_to_empirical_bound_preflight"
CLAIM_CEILING = "local_GR_private_proxy_and_closure_ledger_no_PPN_or_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 225 local-GR route ledger script"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent action/local-GR contract"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "effective scalar local PPN contract"),
        (WORK_DIR / "218-sidecar-readonly-join-contract-or-local-qloc.md", "compact q_loc proxy"),
        (WORK_DIR / "219-compact-shell-q_loc-source-projection-attempt.md", "source projection theorem target"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness/bound"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity route"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "X degree-count audit"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X/P constitutive owner audit"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def demotion gate"),
        (RUN_218 / "results" / "local_q_proxy_readout.csv", "local compact q proxy data"),
        (RUN_220 / "results" / "Jrel_closure_bound_table.csv", "J_rel leakage bound data"),
        (RUN_222 / "results" / "local_PPN_hair_risk_map.csv", "X-sector PPN hair risk map"),
        (RUN_224 / "results" / "promotion_blockers.csv", "latest local route blockers"),
        (RUN_224 / "results" / "X_route_demotion_policy.csv", "latest demotion policy"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def route_checkpoint_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": "218",
            "artifact": "sidecar-readonly-join-contract-or-local-qloc",
            "gain": "compact-shell q_R-like magnitude proxy passes for toy solar/Mercury/GPS cases",
            "failure": "no gamma/beta/slip/q_loc derivation",
            "current_class": "magnitude_proxy_only",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "219",
            "artifact": "compact-shell-q_loc-source-projection-attempt",
            "gain": "clean q_loc theorem target and leakage budget",
            "failure": "Noether/source identity and local trivial J_rel representative missing",
            "current_class": "conditional_theorem_target_plus_bound",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "220",
            "artifact": "Jrel-local-trivial-representative-or-closure-bound",
            "gain": "zero-by-declaration rejected; exact local J_rel route stated",
            "failure": "exact representative and pointwise projector annihilation not parent-derived",
            "current_class": "closure_bound_retained",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "221",
            "artifact": "Noether-source-identity-or-compact-PPN-closure-map",
            "gain": "source identity gets a parent-variation template via response field X",
            "failure": "X sector, boundary primitive, degree count, and PPN coefficients not owned",
            "current_class": "action_class_template",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "222",
            "artifact": "parent-X-sector-degree-count-and-boundary-action",
            "gain": "regular kinetic X rejected; first-order constraint route isolated",
            "failure": "zero propagating X degrees not proven; boundary primitive not selected",
            "current_class": "conditional_constraint_route",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "223",
            "artifact": "X-constraint-algebra-and-Khat-Gamma-constitutive-owner",
            "gain": "free P and invertible H(P) rejected; composite P[Y] route identified",
            "failure": "constraint algebra and defect-potential owner not derived",
            "current_class": "conditional_composite_multiplier_route",
            "promotion_effect": "none",
        },
        {
            "checkpoint": "224",
            "artifact": "defect-potential-Vdef-or-X-route-demotion",
            "gain": "V_def decomposed into partial/closure blocks; X route explicitly demoted",
            "failure": "Z_mu_nu, M_AB, boundary primitive, amplitude, algebra, and stress variation missing",
            "current_class": "closure_support_theorem_target",
            "promotion_effect": "none",
        },
    ]


def local_bound_stack_rows() -> list[dict[str, Any]]:
    q_rows = read_csv_rows(RUN_218 / "results" / "local_q_proxy_readout.csv")
    j_rows = {row["case"]: row for row in read_csv_rows(RUN_220 / "results" / "Jrel_closure_bound_table.csv")}
    risk_rows = {row["case"]: row for row in read_csv_rows(RUN_222 / "results" / "local_PPN_hair_risk_map.csv")}

    rows: list[dict[str, Any]] = []
    for q_row in q_rows:
        case = q_row["case"]
        j_row = j_rows.get(case, {})
        risk_row = risk_rows.get(case, {})
        q_total = float(q_row["q_total_proxy"])
        q_gate = float(q_row["q_R_like_gate"])
        leakage_budget = float(j_row["max_allowed_abs_Ploc_drel_Jrel_leakage"]) if j_row else q_gate - q_total
        rows.append(
            {
                "case": case,
                "use_in_gate": q_row["use_in_gate"],
                "q_total_proxy": q_total,
                "q_R_like_gate": q_gate,
                "q_proxy_ratio_to_gate": float(q_row["ratio_to_gate"]),
                "max_allowed_abs_Ploc_drel_Jrel_leakage": leakage_budget,
                "leakage_budget_fraction_of_gate": leakage_budget / q_gate,
                "max_order_unity_response_coefficient_proxy": risk_row.get("max_order_unity_response_coefficient_proxy", ""),
                "risk_readout": risk_row.get("risk_readout", "stress_only_or_unmapped"),
                "status": "bounded_proxy_no_PPN_promotion",
            }
        )
    return rows


def residual_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "q_R_like_magnitude_proxy",
            "current_status": "passes_current_compact_proxy",
            "evidence": "checkpoint 218 compact q proxy rows below 2.3e-5",
            "missing_for_promotion": "real PPN observable mapping and source identity",
        },
        {
            "residual": "q_loc^nu",
            "current_status": "closure_bounded_theorem_target",
            "evidence": "checkpoints 219-220 set leakage budget and exact-J_rel route",
            "missing_for_promotion": "Noether source identity plus local trivial J_rel representative",
        },
        {
            "residual": "gamma_minus_1",
            "current_status": "closure_only",
            "evidence": "checkpoint 221 PPN closure vector uses c_gamma epsilon_J",
            "missing_for_promotion": "derived coefficient c_gamma from weak-field metric solution",
        },
        {
            "residual": "beta_minus_1",
            "current_status": "closure_only",
            "evidence": "checkpoint 221 PPN closure vector uses c_beta epsilon_J",
            "missing_for_promotion": "derived nonlinear weak-field metric coefficient",
        },
        {
            "residual": "Phi_minus_Psi",
            "current_status": "closure_only",
            "evidence": "checkpoint 221 PPN closure vector uses c_slip epsilon_J",
            "missing_for_promotion": "boundary anisotropic stress/slip derivation",
        },
        {
            "residual": "G_eff_over_G_minus_1",
            "current_status": "closure_only",
            "evidence": "checkpoint 221 PPN closure vector uses c_G epsilon_J",
            "missing_for_promotion": "local source renormalization map",
        },
        {
            "residual": "alpha_clock",
            "current_status": "forbidden_by_contract_not_derived",
            "evidence": "minimal/universal matter coupling guardrail",
            "missing_for_promotion": "parent proof of no clock/composition coupling",
        },
        {
            "residual": "epsilon_matter",
            "current_status": "forbidden_by_contract_not_derived",
            "evidence": "WEP/composition guardrail",
            "missing_for_promotion": "universal matter coupling from action",
        },
    ]


def promotion_blocker_rows() -> list[dict[str, Any]]:
    blockers = read_csv_rows(RUN_224 / "results" / "promotion_blockers.csv")
    rows: list[dict[str, Any]] = []
    for blocker in blockers:
        rows.append(
            {
                "blocker": blocker["blocker"],
                "required": blocker["required"],
                "current_status": blocker["current_status"],
                "effect": blocker["effect"],
                "next_handling": "theory_route" if blocker["blocker"] in {"B1_parent_Z_definition", "B2_full_MAB", "B5_constraint_algebra", "B6_stress_variation"} else "closure_or_bound_route",
            }
        )
    rows.append(
        {
            "blocker": "B7_real_local_bound_baseline",
            "required": "map current proxy ledger onto real local tests with fair GR/MTS baseline discipline",
            "current_status": "not_run",
            "effect": "we do not yet know which local bound is the tightest practical discriminator",
            "next_handling": "empirical_preflight_route",
        }
    )
    return rows


def pivot_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "continue_Vdef_derivation",
            "value": "high_theory_value",
            "readiness": "low",
            "risk": "keeps generating elegant placeholders without new evidence",
            "decision": "defer",
            "reason": "checkpoint 224 shows six open/missing blockers before promotion",
        },
        {
            "option": "derive_PPN_coefficients",
            "value": "high_local_GR_value",
            "readiness": "medium_low",
            "risk": "coefficients depend on still-unowned P/Z/M_AB/boundary stress",
            "decision": "defer_until_preflight",
            "reason": "first identify which residual/local system is tightest",
        },
        {
            "option": "local_bound_empirical_preflight",
            "value": "high_discipline_value",
            "readiness": "high",
            "risk": "proxy-only if not clearly labelled",
            "decision": "recommended_next",
            "reason": "uses existing q proxy/leakage budgets to rank local tests before further theory placeholders",
        },
        {
            "option": "galaxy_sidecar_readonly_join",
            "value": "medium_empirical_value",
            "readiness": "medium",
            "risk": "distracts from local-GR gate",
            "decision": "pending_after_local_preflight",
            "reason": "galaxy pillar matters, but local GR is the immediate promotion bottleneck",
        },
        {
            "option": "public_claim_or_promotion",
            "value": "negative",
            "readiness": "none",
            "risk": "overclaim",
            "decision": "forbidden",
            "reason": CLAIM_CEILING,
        },
    ]


def allowed_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "local_bound_preflight",
            "allowed_output": "rank compact cases and residuals by proxy tightness",
            "forbidden_output": "claim PPN pass or derived GR",
            "dry_run_first": "yes",
        },
        {
            "test": "Cassini_like_gamma_gate",
            "allowed_output": "compare epsilon_J coefficient budget to a declared gamma-bound proxy",
            "forbidden_output": "use gamma bound without deriving c_gamma",
            "dry_run_first": "yes",
        },
        {
            "test": "clock_WEP_guardrail",
            "allowed_output": "confirm no direct matter/clock coupling is present in the closure contract",
            "forbidden_output": "claim WEP theorem",
            "dry_run_first": "yes",
        },
        {
            "test": "GR_baseline_comparison",
            "allowed_output": "state GR residuals are zero/by construction for these proxy channels and compare MTS closure residual budget",
            "forbidden_output": "test only MTS while treating baseline as immune",
            "dry_run_first": "yes",
        },
    ]


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_failures = sum(
        row["use_in_gate"] == "yes" and float(row["q_proxy_ratio_to_gate"]) > 1.0
        for row in bound_rows
    )
    open_blockers = sum(row["current_status"] in {"missing", "not_derived", "empirical_closure", "contract_only", "not_run"} for row in blockers)
    recommended = "local_bound_empirical_preflight"
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "local route consolidated",
            "status": "pass",
            "evidence": "checkpoints 218-224 listed with current class",
            "claim_allowed": "private route ledger",
        },
        {
            "gate": "compact q proxies below internal gate",
            "status": "pass" if compact_failures == 0 else "fail",
            "evidence": f"compact_failures={compact_failures}",
            "claim_allowed": "magnitude proxy only",
        },
        {
            "gate": "closure support separated from derivation",
            "status": "pass",
            "evidence": "X/Vdef demotion policy carried forward",
            "claim_allowed": "no hidden promotion drift",
        },
        {
            "gate": "local GR promotion blockers remain",
            "status": "fail",
            "evidence": f"open_blockers={open_blockers}",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "next action selected",
            "status": "pass",
            "evidence": f"recommended={recommended}",
            "claim_allowed": "workflow decision",
        },
        {
            "gate": "public/local PPN claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(worst_budget: float, tightest_case: str) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The local-GR branch has a bounded compact-shell proxy and increasingly sharp theorem targets, but the derivation chain after 218-224 ends in closure support: J_rel exactness, source identity, X multiplier, composite P, and V_def are all useful organizing machinery, not derived local GR. The next best move is a local-bound empirical preflight that ranks which proxy residual and compact system is most constraining before inventing more parent-action placeholders.",
            "main_gain": "local route is consolidated with no hidden promotion drift",
            "main_failure": "six parent-theory blockers plus one not-run empirical local-bound baseline remain",
            "worst_compact_Jrel_leakage_budget": worst_budget,
            "tightest_ppn_proxy_case": tightest_case,
            "next_target": "226-local-bound-preflight-and-baseline-comparison.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_225_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    route_rows = route_checkpoint_rows()
    bound_rows = local_bound_stack_rows()
    residual_rows = residual_status_rows()
    blocker_rows = promotion_blocker_rows()
    pivot_rows = pivot_decision_rows()
    test_rows = allowed_test_rows()
    gates = claim_gate_rows(source_rows, bound_rows, blocker_rows)

    compact_bounds = [
        float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"])
        for row in bound_rows
        if row["use_in_gate"] == "yes"
    ]
    worst_budget = min(compact_bounds)
    compact_risks = [row for row in bound_rows if row["use_in_gate"] == "yes" and row["max_order_unity_response_coefficient_proxy"] != ""]
    tightest_case = min(
        compact_risks,
        key=lambda row: float(row["max_order_unity_response_coefficient_proxy"]),
    )["case"]
    decision = decision_rows(worst_budget, tightest_case)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "local_GR_route_checkpoint_ledger.csv": (
            route_rows,
            ["checkpoint", "artifact", "gain", "failure", "current_class", "promotion_effect"],
        ),
        "compact_local_bound_stack.csv": (
            bound_rows,
            [
                "case",
                "use_in_gate",
                "q_total_proxy",
                "q_R_like_gate",
                "q_proxy_ratio_to_gate",
                "max_allowed_abs_Ploc_drel_Jrel_leakage",
                "leakage_budget_fraction_of_gate",
                "max_order_unity_response_coefficient_proxy",
                "risk_readout",
                "status",
            ],
        ),
        "PPN_residual_status_ledger.csv": (
            residual_rows,
            ["residual", "current_status", "evidence", "missing_for_promotion"],
        ),
        "promotion_blocker_ledger.csv": (
            blocker_rows,
            ["blocker", "required", "current_status", "effect", "next_handling"],
        ),
        "pivot_decision_matrix.csv": (
            pivot_rows,
            ["option", "value", "readiness", "risk", "decision", "reason"],
        ),
        "allowed_local_test_matrix.csv": (
            test_rows,
            ["test", "allowed_output", "forbidden_output", "dry_run_first"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "worst_compact_Jrel_leakage_budget",
                "tightest_ppn_proxy_case",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_failures = sum(
        row["use_in_gate"] == "yes" and float(row["q_proxy_ratio_to_gate"]) > 1.0
        for row in bound_rows
    )
    open_blockers = sum(
        row["current_status"] in {"missing", "not_derived", "empirical_closure", "contract_only", "not_run"}
        for row in blocker_rows
    )
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "compact_q_proxy_failures": compact_failures,
        "worst_compact_Jrel_leakage_budget": worst_budget,
        "tightest_ppn_proxy_case": tightest_case,
        "local_GR_route_consolidated": True,
        "X_route_status": "closure_support_theorem_target",
        "Vdef_status": "composite_candidate_contract",
        "open_or_not_run_blockers": open_blockers,
        "recommended_next": "local_bound_empirical_preflight",
        "local_GR_promoted": False,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
