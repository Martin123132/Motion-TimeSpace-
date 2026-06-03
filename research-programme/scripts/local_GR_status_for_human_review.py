from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-status-for-human-review"
STATUS = "local_GR_status_for_human_review_written_MTS_to_GR_Newton_route_coherent_runner_ready_but_not_derived_no_public_claim"
CLAIM_CEILING = "human_review_status_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "400-runner-v3-numeric-smoke-extension.md"


SOURCE_DOCS = [
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity closure branch and remaining local-GR stack",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH operator selection under identity closure",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "Newtonian source-normalization contract",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "boundary/bulk joint no-hair and flux runner",
    },
    {
        "path": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "role": "preferred-frame/domain no-hair under identity closure",
    },
    {
        "path": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "role": "full local-GR sufficiency stack audit",
    },
    {
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "role": "runner-v3 implementation checkpoint",
    },
    {
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "role": "parent-action obligations for every runner-v3 row",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "machine-readable runner-v3 matrix",
    },
    {
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/runner_row_parent_obligations.csv",
        "role": "machine-readable parent obligations for runner-v3 rows",
    },
]


STATUS_SUMMARY = [
    {
        "question": "Is MTS locally derived to GR/Newton yet?",
        "answer": "no",
        "reason": "identity coframe is closure-labelled, while EH, source normalization, no-hair, force law, and PPN coefficient derivations remain open",
    },
    {
        "question": "Is the route coherent enough to test?",
        "answer": "yes",
        "reason": "runner-v3 has identity labels, retained residual rows, same-pipeline GR/null baseline, and no false pass flags",
    },
    {
        "question": "How grim is it?",
        "answer": "serious but not grim",
        "reason": "the work has moved from vague local-GR hope to a finite derivation/test stack; the hard part is paying the parent-action obligations",
    },
    {
        "question": "What is the strongest current claim?",
        "answer": "private internal claim only",
        "reason": "MTS has a disciplined GR-facing identity branch and runner-ready residual stack, not a public GR reduction",
    },
]


STRONG_POINTS = [
    {
        "strength": "WEP/coframe obstruction isolated",
        "why_it_matters": "identity closure removes the direct matter/coframe pullback in the test branch without pretending it is parent-derived",
        "key_artifact": "391;397",
    },
    {
        "strength": "EH is separated from WEP",
        "why_it_matters": "the framework no longer shortcuts from 'matter sees one metric' to 'Einstein-Hilbert follows'",
        "key_artifact": "392",
    },
    {
        "strength": "Newtonian source normalization is explicit",
        "why_it_matters": "the route now knows it must derive kappa_eff, G_eff, M_eff, measured GM, and no range/time/species leakage",
        "key_artifact": "393",
    },
    {
        "strength": "Boundary and bulk cannot hide",
        "why_it_matters": "q_BX joins boundary flux and bulk X into one local force/flux contract",
        "key_artifact": "394",
    },
    {
        "strength": "Preferred-frame rows are fairer",
        "why_it_matters": "coframe slip is closure-zero in the identity branch, but domain/projector/vector residues remain testable",
        "key_artifact": "395",
    },
    {
        "strength": "Runner-v3 exists",
        "why_it_matters": "GR/null baseline is sane and every non-derived row is blocked from false pass claims",
        "key_artifact": "397",
    },
    {
        "strength": "Parent action debt is exact",
        "why_it_matters": "every runner-v3 row now has a parent-action obligation instead of a vague 'derive it later'",
        "key_artifact": "398",
    },
]


OPEN_BLOCKERS = [
    {
        "blocker": "parent identity matter selector",
        "blocks": "public WEP/local-GR claim",
        "needed_derivation": "derive ehat=e and no species/nonmetric matter spurions from S_parent",
        "current_state": "closure_zero only",
    },
    {
        "blocker": "EH operator selection",
        "blocks": "Einstein-Hilbert/local GR",
        "needed_derivation": "metric-only local 4D second-order exterior or explicit retained non-EH coefficients",
        "current_state": "failed_open with non-EH ledger retained",
    },
    {
        "blocker": "source-normalized Newtonian limit",
        "blocks": "GR-to-Newton reduction",
        "needed_derivation": "constant universal kappa/G_eff/M_eff/measured GM absorption",
        "current_state": "conditional algebra, not parent-derived",
    },
    {
        "blocker": "boundary/bulk no-hair",
        "blocks": "clean local exterior and fifth-force safety",
        "needed_derivation": "class-only boundary, Ward-owned flux, source-free bulk-X no-hair or alpha_X(lambda_X)",
        "current_state": "conditional kill switches only",
    },
    {
        "blocker": "domain/projector preferred-frame no-hair",
        "blocks": "alpha1/alpha2/alpha3/xi pass",
        "needed_derivation": "domain/projector vectors gauge/topological or retained with owned stress",
        "current_state": "budget-ready but coefficients missing",
    },
    {
        "blocker": "fifth-force alpha(lambda)",
        "blocks": "fifth-force/delta_G scoring",
        "needed_derivation": "range, coupling, source/test charge, and screening/profile for each finite-range channel",
        "current_state": "unscored parameterized",
    },
    {
        "blocker": "PPN coefficient derivation",
        "blocks": "claiming GR limit",
        "needed_derivation": "gamma=beta=1, alpha_i=xi=0, no Gdot/G, no fifth force from parent action",
        "current_state": "budget-only runner rows",
    },
]


ARTIFACT_POINTERS = [
    {
        "artifact": "local-GR stack audit",
        "path": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "use": "best technical snapshot of the GR/Newton sufficiency stack",
    },
    {
        "artifact": "runner-v3",
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "use": "machine-readable/test-facing local residual runner",
    },
    {
        "artifact": "runner-v3 matrix CSV",
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "use": "exact row states for WEP/clock/PPN/fifth-force/operator residuals",
    },
    {
        "artifact": "parent-action contract v2",
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "use": "exact derivation obligations for every non-derived runner row",
    },
    {
        "artifact": "parent obligations CSV",
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/runner_row_parent_obligations.csv",
        "use": "machine-readable row-to-parent-action debt map",
    },
]


NEXT_STEPS = [
    {
        "priority": 1,
        "step": "extend runner-v3 numeric smoke controls",
        "why": "moves from clean bookkeeping to same-pipeline residual sweeps and fair GR/null comparisons",
        "target": NEXT_TARGET,
    },
    {
        "priority": 2,
        "step": "attempt parent identity matter selector theorem",
        "why": "first real chance to turn identity closure into derived WEP/coframe theorem",
        "target": "401-parent-matter-selector-theorem-attempt.md",
    },
    {
        "priority": 3,
        "step": "attempt EH/source-normalization theorem pair",
        "why": "GR-to-Newton needs both EH-shaped dynamics and measured-GM source normalization",
        "target": "402-EH-source-normalization-parent-pair.md",
    },
    {
        "priority": 4,
        "step": "keep empirical work fair",
        "why": "every MTS local stress test should run GR/null through the same pipeline before judging MTS",
        "target": "runner-v3 numeric extensions and future local/cosmology tests",
    },
]


RISK_REGISTER = [
    {
        "risk": "overclaiming identity closure",
        "consequence": "turns branch assumption into fake WEP/local-GR theorem",
        "mitigation": "keep closure_zero visible until parent theorem exists",
    },
    {
        "risk": "turning budgets into wins",
        "consequence": "source locks become decorative rather than discipline",
        "mitigation": "runner-v3 keeps claim_allowed=false for all smoke rows",
    },
    {
        "risk": "ignoring baseline failures",
        "consequence": "pipeline bugs could look like MTS failures",
        "mitigation": "same-pipeline GR/null baseline first",
    },
    {
        "risk": "hiding force-law profiles",
        "consequence": "fifth-force/delta_G row becomes fake scalar score",
        "mitigation": "retain alpha(lambda) requirement",
    },
    {
        "risk": "trying to solve everything in prose",
        "consequence": "pretty theory text without derivations or tests",
        "mitigation": "parent-action obligations and runner-v3 artifacts stay machine-readable",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The current MTS-to-GR/Newton route is coherent and substantially cleaner than before the identity-stack work. It is not a derived local-GR reduction. The strongest honest position is: MTS has a disciplined identity-branch local runner, an explicit GR/Newton sufficiency stack, and a parent-action obligation map for every non-derived row. The next best move is to extend runner-v3 numerically and then attack the parent identity matter selector theorem.",
        "human_readable_status_written": True,
        "local_GR_claim_allowed": False,
        "runner_ready": True,
        "contract_ready": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "extend runner-v3 smoke controls toward real symbolic/numeric coefficient sweeps",
        "pass_condition": "same-pipeline GR/null baseline plus retained MTS residual sweeps",
    },
    {
        "priority": 2,
        "target": "401-parent-matter-selector-theorem-attempt.md",
        "task": "attempt to derive or reject the parent identity matter selector",
        "pass_condition": "R0 moves toward derived_zero or remains explicit closure only",
    },
    {
        "priority": 3,
        "target": "402-EH-source-normalization-parent-pair.md",
        "task": "try to pair EH operator selection with source-normalized Newtonian limit",
        "pass_condition": "clear derivation route or retained operator/source residuals",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "human_status_summary_written",
            "status": "pass",
            "evidence": f"{len(STATUS_SUMMARY)} status questions answered",
        },
        {
            "gate": "strengths_and_blockers_written",
            "status": "pass",
            "evidence": f"{len(STRONG_POINTS)} strengths and {len(OPEN_BLOCKERS)} blockers recorded",
        },
        {
            "gate": "artifact_pointers_written",
            "status": "pass",
            "evidence": f"{len(ARTIFACT_POINTERS)} key artifacts listed",
        },
        {
            "gate": "next_steps_written",
            "status": "pass",
            "evidence": f"{len(NEXT_STEPS)} near-term steps recorded",
        },
        {
            "gate": "risk_register_written",
            "status": "pass",
            "evidence": f"{len(RISK_REGISTER)} project risks recorded",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "status memo says route is coherent but not derived local GR",
        },
        {
            "gate": "public_overclaim_blocked",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "status_summary.csv", STATUS_SUMMARY)
    write_csv(results_dir / "strong_points.csv", STRONG_POINTS)
    write_csv(results_dir / "open_blockers.csv", OPEN_BLOCKERS)
    write_csv(results_dir / "artifact_pointers.csv", ARTIFACT_POINTERS)
    write_csv(results_dir / "next_steps.csv", NEXT_STEPS)
    write_csv(results_dir / "risk_register.csv", RISK_REGISTER)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "human_readable_status_written": True,
        "strong_points": len(STRONG_POINTS),
        "open_blockers": len(OPEN_BLOCKERS),
        "runner_ready": True,
        "contract_ready": True,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 399 local-GR status for human review artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
