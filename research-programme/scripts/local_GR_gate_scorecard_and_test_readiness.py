#!/usr/bin/env python3
"""Checkpoint 250: local-GR gate scorecard and test readiness."""

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

CHECKPOINT_250_NAME = "local-GR-gate-scorecard-and-test-readiness"
RUN_226 = RUNS_ROOT / "20260601-000043-local-bound-preflight-and-baseline-comparison"
RUN_227 = RUNS_ROOT / "20260601-000044-local-PPN-coefficient-map-or-official-bound-manifest"
RUN_239 = RUNS_ROOT / "20260601-000056-nohair-theorem-targets-or-local-bound-runner"
RUN_247 = RUNS_ROOT / "20260601-000064-local-EH-exterior-sufficiency-stack-no-promotion"
RUN_249 = RUNS_ROOT / "20260601-000066-projector-boundary-only-condition-or-metric-only-reduction-fail"

STATUS = "local_GR_gate_scorecard_written_N5_blocks_metric_only_EH_empirical_tests_proxy_only_no_promotion"
CLAIM_CEILING = "local_GR_scorecard_and_proxy_readiness_no_PPN_or_beta_claim"
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 250 runner"),
        (WORK_DIR / "226-local-bound-preflight-and-baseline-comparison.md", "local proxy preflight baseline"),
        (WORK_DIR / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "official local-bound manifest"),
        (WORK_DIR / "247-local-EH-exterior-sufficiency-stack-no-promotion.md", "EH sufficiency stack"),
        (WORK_DIR / "249-projector-boundary-only-condition-or-metric-only-reduction-fail.md", "N5 metric-only blocker"),
        (RUN_226 / "results" / "coefficient_budget_ranking.csv", "closure coefficient budgets"),
        (RUN_227 / "results" / "official_local_bound_manifest.csv", "official local bound source manifest"),
        (RUN_239 / "results" / "nohair_priority_after_bound_preflight.csv", "no-hair pressure ranking"),
        (RUN_247 / "results" / "EH_premise_status_table.csv", "EH premise status"),
        (RUN_249 / "results" / "local_branch_update_after_249.csv", "local branch update after N5"),
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


def local_gr_gate_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "ordinary_exterior_region",
            "status": "definition_pass",
            "evidence": "T_matter|E=0 defines compact exterior outside source",
            "blocks_promotion": "no",
            "next_action": "carry as exterior-region definition",
        },
        {
            "gate": "N3_universal_strict_coframe",
            "status": "conditional",
            "evidence": "direct matter/clock coefficients vanish if strict coframe and R_loc hold",
            "blocks_promotion": "yes_parent_Rloc_missing",
            "next_action": "derive R_loc[D_bound] or keep direct-coupling pass conditional",
        },
        {
            "gate": "N2_no_TF",
            "status": "conditional",
            "evidence": "scalar boundary stress gives tau_TF=0 -> Phi-Psi=0",
            "blocks_promotion": "yes_parent_boundary_owner_missing",
            "next_action": "derive scalar-only boundary variable set",
        },
        {
            "gate": "N1_Meff",
            "status": "conditional",
            "evidence": "Pi_M absolute H2 flux closed -> conserved M_eff",
            "blocks_promotion": "yes_PiM_source_identity_missing",
            "next_action": "derive Pi_M flux closure and M_eff calibration",
        },
        {
            "gate": "N4_exact_relative_memory",
            "status": "conditional",
            "evidence": "P_mem J_rel=dA_rel if closed relative current and H2_relative=0",
            "blocks_promotion": "yes_Pmem_Arel_parent_owner_missing",
            "next_action": "derive P_mem/source identity/A_rel representative",
        },
        {
            "gate": "N5_projector_stress",
            "status": "open_blocker",
            "evidence": "bulk T_projector blocks metric-only EH unless zero/boundary-only",
            "blocks_promotion": "yes_hard_block",
            "next_action": "derive T_projector|bulk=0 or accept modified exterior branch",
        },
        {
            "gate": "N6_auxiliary_nohair",
            "status": "open",
            "evidence": "rank-zero X is necessary only; brackets/P[Y]/V_def owner missing",
            "blocks_promotion": "yes",
            "next_action": "derive parent symplectic structure before bracket closure",
        },
        {
            "gate": "metric_only_EH_exterior",
            "status": "blocked",
            "evidence": "N5 not boundary-only; N6 still open; exterior reduction not parent-derived",
            "blocks_promotion": "yes_hard_block",
            "next_action": "resolve N5/N6 before beta/local-GR claim",
        },
        {
            "gate": "beta_equals_one",
            "status": "conditional_theorem_only",
            "evidence": "if all N-gates plus metric-only EH hold, Schwarzschild beta=1 follows",
            "blocks_promotion": "yes_premises_open",
            "next_action": "do not promote beta until premises are parent-derived",
        },
    ]


def empirical_test_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel": "gamma_minus_1",
            "bound_source": "Cassini manifest ready",
            "theory_owner": "N2_no_TF",
            "readiness": "closure_proxy_only",
            "allowed_now": "stress-test c_gamma=0 assumption under scalar-boundary closure",
            "not_allowed": "claim Cassini pass",
        },
        {
            "channel": "Phi_minus_Psi",
            "bound_source": "internal slip/q-like proxy only",
            "theory_owner": "N2_no_TF",
            "readiness": "internal_proxy_only",
            "allowed_now": "test anisotropic-stress leakage budget",
            "not_allowed": "claim observational slip pass",
        },
        {
            "channel": "G_eff_over_G_minus_1",
            "bound_source": "internal q-like/source proxy only",
            "theory_owner": "N1_Meff",
            "readiness": "internal_proxy_only",
            "allowed_now": "test radial memory hair/source-normalization sensitivity",
            "not_allowed": "claim measured G_eff/local gravity pass",
        },
        {
            "channel": "beta_minus_1",
            "bound_source": "Will review manifest row; primary ephemeris source still needed",
            "theory_owner": "N1-N6 plus EH exterior",
            "readiness": "not_ready_for_official_bound",
            "allowed_now": "closure stress test only",
            "not_allowed": "claim beta or PPN pass",
        },
        {
            "channel": "alpha_clock",
            "bound_source": "Gravity Probe A/Galileo manifest ready",
            "theory_owner": "N3 plus R_loc/C branch",
            "readiness": "closure_proxy_only",
            "allowed_now": "test direct clock-vertex absence assumption",
            "not_allowed": "claim redshift/local-position-invariance pass",
        },
        {
            "channel": "epsilon_matter",
            "bound_source": "MICROSCOPE manifest ready",
            "theory_owner": "N3_universal_coupling",
            "readiness": "pressure_test_only",
            "allowed_now": "use as brutal prior on direct composition leakage",
            "not_allowed": "claim WEP pass until parent coupling theorem is owned",
        },
        {
            "channel": "q_loc",
            "bound_source": "internal compact q/J_rel proxy only",
            "theory_owner": "N4/N5/N6",
            "readiness": "internal_proxy_only",
            "allowed_now": "rank source leakage and projector-stress sensitivity",
            "not_allowed": "claim local source identity or no-hair pass",
        },
    ]


def theorem_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "N5_projector_bulk_zero_or_modified_branch",
            "why": "hard blocker for metric-only EH; bulk T_projector means modified exterior",
            "recommended_next": "derive T_projector|bulk=0 or explicitly demote local-GR branch to modified exterior",
        },
        {
            "rank": 2,
            "target": "N6_auxiliary_nohair_parent_symplectic",
            "why": "rank-zero X is not enough; no-hair brackets need parent symplectic form",
            "recommended_next": "derive parent/boundary symplectic structure for Y fields",
        },
        {
            "rank": 3,
            "target": "Rloc_strict_coframe_parent_selection",
            "why": "N3 direct coupling and local C-silence remain conditional",
            "recommended_next": "derive stationary bound-domain representative selection",
        },
        {
            "rank": 4,
            "target": "PiM_scalar_boundary_Pmem_parent_owners",
            "why": "N1/N2/N4 are useful but still conditional",
            "recommended_next": "derive boundary Hodge/DeWitt metric from parent action",
        },
        {
            "rank": 5,
            "target": "closure_flagged_local_bound_proxy_runner",
            "why": "empirical stress tests are useful only as internal diagnostics",
            "recommended_next": "run/update local-bound proxy matrix with explicit no-claim flags",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "MTS derives local GR",
            "status": "forbidden",
            "reason": "N5/N6/metric-only exterior and parent owners are open",
        },
        {
            "claim": "MTS local branch is dead",
            "status": "not_supported",
            "reason": "conditional sufficiency stack is coherent and has no contradiction yet",
        },
        {
            "claim": "If N1-N6 plus metric-only EH hold, beta=1 follows",
            "status": "allowed_conditional",
            "reason": "Lovelock/EH plus Schwarzschild exterior gives beta=1",
        },
        {
            "claim": "Local bounds can be used now",
            "status": "allowed_proxy_only",
            "reason": "official manifest and closure budgets exist, but coefficients are not parent-derived",
        },
        {
            "claim": "MTS passes Cassini/MICROSCOPE/clocks",
            "status": "forbidden",
            "reason": "official bounds cannot be pass/fail until coefficient map is parent-owned",
        },
    ]


def test_workflow_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "workflow_item": "refresh official manifest sources",
            "run_now": "optional",
            "output": "updated source manifest only",
            "claim_flag": "no pass/fail",
        },
        {
            "step": 2,
            "workflow_item": "rerun local closure pressure matrix",
            "run_now": "yes_short",
            "output": "closure coefficient pressure by channel/case",
            "claim_flag": "proxy only",
        },
        {
            "step": 3,
            "workflow_item": "add N5 branch variants",
            "run_now": "yes_short",
            "output": "zero/boundary/bulk projector stress sensitivity rows",
            "claim_flag": "internal diagnostic",
        },
        {
            "step": 4,
            "workflow_item": "official PPN likelihood/bound application",
            "run_now": "no",
            "output": "defer until coefficients parent-derived",
            "claim_flag": "blocked",
        },
        {
            "step": 5,
            "workflow_item": "long local-data pipeline",
            "run_now": "no",
            "output": "only after parent gates improve",
            "claim_flag": "not ready",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    open_or_blocked = sum(
        1
        for row in local_gr_gate_scorecard_rows()
        if row["status"] in {"open", "open_blocker", "blocked", "conditional", "conditional_theorem_only"}
    )
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "local GR gate scorecard written",
            "status": "pass",
            "evidence": f"gate_rows={len(local_gr_gate_scorecard_rows())}",
            "claim_allowed": "scorecard only",
        },
        {
            "gate": "empirical test readiness separated from theory status",
            "status": "pass",
            "evidence": f"test_rows={len(empirical_test_readiness_rows())}",
            "claim_allowed": "proxy readiness only",
        },
        {
            "gate": "local GR promoted",
            "status": "fail",
            "evidence": f"open_or_blocked_gates={open_or_blocked}",
            "claim_allowed": "no",
        },
        {
            "gate": "local branch declared dead",
            "status": "fail",
            "evidence": "conditional stack remains coherent but blocked",
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The local-GR branch is neither solved nor dead. It is a finite conditional stack with N5 as the sharpest metric-only blocker, N6 still open, and N1/N2/N3/N4 useful but parent-conditional. Empirical local-bound work is ready only as closure/proxy stress testing, not as official pass/fail.",
            "main_gain": "the theorem/test queue is explicit, ranked, and claim-safe",
            "main_failure": "local GR, beta, and official local-bound passes remain unproved",
            "next_target": "251-local-bound-proxy-runner-refresh-with-N5-branches.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_250_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    gate_rows = local_gr_gate_scorecard_rows()
    readiness_rows = empirical_test_readiness_rows()
    priority_rows = theorem_priority_rows()
    policy_rows = claim_policy_rows()
    workflow_rows = test_workflow_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "local_GR_gate_scorecard.csv": (
            gate_rows,
            ["gate", "status", "evidence", "blocks_promotion", "next_action"],
        ),
        "empirical_test_readiness.csv": (
            readiness_rows,
            ["channel", "bound_source", "theory_owner", "readiness", "allowed_now", "not_allowed"],
        ),
        "theorem_priority_queue.csv": (
            priority_rows,
            ["rank", "target", "why", "recommended_next"],
        ),
        "claim_policy.csv": (
            policy_rows,
            ["claim", "status", "reason"],
        ),
        "test_workflow_queue.csv": (
            workflow_rows,
            ["step", "workflow_item", "run_now", "output", "claim_flag"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "local_GR_promoted": False,
        "local_branch_dead_claimed": False,
        "empirical_tests_ready_as_proxy_only": True,
        "hardest_metric_only_blocker": "N5_projector_stress",
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
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
