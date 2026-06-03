from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Cperp-relative-exactness-or-projected-metric-closure-decision"
STATUS = "Cperp_scalar_exactness_rejected_projected_metric_demoted_to_explicit_closure_lifted_C_route_open"
CLAIM_CEILING = "closure_decision_only_no_projected_metric_derivation_no_WEP_clock_PPN_or_local_GR_pass"
NEXT_TARGET = "363-projected-metric-closure-ledger-and-lifted-C-route-contract.md"

RUN_361 = ROOT / "runs" / "20260601-193000-residual-gauge-principle-for-projected-matter-metric"


SOURCE_DOCS = [
    {
        "path": "270-Cperp-residual-shift-constraint-attempt.md",
        "role": "first-class Cperp shift route and no-Cperp Hamiltonian condition",
    },
    {
        "path": "271-parent-no-Cperp-action-or-closure.md",
        "role": "quotient no-Cperp action skeleton and closure fork",
    },
    {
        "path": "272-quotient-configuration-principle-from-topological-projector.md",
        "role": "presymplectic quotient route and Cperp exactness burden",
    },
    {
        "path": "273-Cperp-relative-exactness-C-sector.md",
        "role": "earlier scalar Cperp exactness transfer failure and closure demotion",
    },
    {
        "path": "361-residual-gauge-principle-for-projected-matter-metric.md",
        "role": "current residual gauge selector theorem and exactness requirements",
    },
    {
        "path": "runs/20260601-193000-residual-gauge-principle-for-projected-matter-metric/results/C_exactness_requirements.csv",
        "role": "machine-readable C exactness requirements from checkpoint 361",
    },
    {
        "path": "runs/20260601-193000-residual-gauge-principle-for-projected-matter-metric/results/decision_matrix.csv",
        "role": "machine-readable decision state from checkpoint 361",
    },
]


EXACTNESS_TESTS = [
    {
        "test": "Jrel_flux_cohomology_transfer",
        "candidate_argument": "J_rel exactness on compact shell should imply Cperp exactness",
        "result": "fail",
        "reason": "J_rel is flux/current-like; Cperp is currently a scalar/0-form representative",
        "consequence": "cannot inherit H^2 relative exactness theorem",
    },
    {
        "test": "relative_H0_triviality",
        "candidate_argument": "H^0(D,partial D)=0 kills scalar residuals",
        "result": "fail",
        "reason": "relative H^0 only kills boundary-zero closed scalar classes, not arbitrary local scalar profiles",
        "consequence": "does not prove general kernel shifts are gauge",
    },
    {
        "test": "dCperp_exact_one_form",
        "candidate_argument": "dCperp is exact, so Cperp is harmless",
        "result": "fail",
        "reason": "exact gradients can still carry kinetic/gradient energy, matter force, or boundary charge",
        "consequence": "exact derivative is insufficient without no-Cperp action",
    },
    {
        "test": "first_class_shift_constraint",
        "candidate_argument": "pi_perp approx 0 generates Cperp shifts",
        "result": "conditional_fail",
        "reason": "self-algebra is fine, but Hamiltonian preservation needs delta H/delta Cperp approx 0, not derived",
        "consequence": "shift route stays conditional and cannot promote projected metric",
    },
    {
        "test": "quotient_no_Cperp_action_skeleton",
        "candidate_argument": "write all sectors on [C]=C/ker(P_D)",
        "result": "conditional_pass_but_assumes_target",
        "reason": "skeleton works if quotient principle is assumed; it does not derive the quotient",
        "consequence": "useful closure/theorem target, not parent theorem",
    },
    {
        "test": "presymplectic_null_direction",
        "candidate_argument": "eta_perp is null in Omega",
        "result": "conditional_fail",
        "reason": "requires C-sector relative exactness and vanishing local boundary primitive",
        "consequence": "null direction not derived for scalar Cperp",
    },
]


CLOSURE_POLICY = [
    {
        "object": "projected_matter_metric",
        "symbol": "ghat_munu = exp(P_D C) g_munu",
        "new_status": "explicit_effective_closure_for_current_scalar_C_sector",
        "allowed_use": "disciplined local-silence/common-mode branch with all closure labels visible",
        "forbidden_use": "parent-derived matter coupling, WEP pass, clock pass, local-GR derivation",
    },
    {
        "object": "Cperp_shift",
        "symbol": "Cperp -> Cperp + eta_perp",
        "new_status": "not_parent_derived_gauge",
        "allowed_use": "future theorem target if C is lifted to class/form/holonomy sector",
        "forbidden_use": "claim Cperp is gauge in current scalar sector",
    },
    {
        "object": "universal_matter_coupling",
        "symbol": "S_matter[Psi, ehat]",
        "new_status": "conditional_contract_with_projected_metric_closure",
        "allowed_use": "direct species vertices absent if closure branch is imposed",
        "forbidden_use": "WEP/clock observational pass without derived selector and coefficients",
    },
    {
        "object": "local_GR_branch",
        "symbol": "MTS -> EH/PPN",
        "new_status": "still_unpromoted",
        "allowed_use": "conditional theorem stack and source-locked guardrails",
        "forbidden_use": "use projected metric closure as a GR proof",
    },
]


LIFTED_C_ROUTE_CONTRACT = [
    {
        "contract": "lift_C_from_scalar_to_class_variable",
        "required_statement": "C is not a fundamental local scalar; it is a representative of a connection/holonomy/boundary/relative class",
        "pass_condition": "local Cperp is representative data, while P_D C is the class observable",
    },
    {
        "contract": "derive_relative_exact_local_residuals",
        "required_statement": "local residual Cperp modes are d_rel-exact or constraint-trivial on compact local domains",
        "pass_condition": "kernel shifts are gauge or presymplectic null directions",
    },
    {
        "contract": "preserve_FLRW_memory_class",
        "required_statement": "cosmological P_D C survives as a nontrivial class while local Cperp quotients away",
        "pass_condition": "same parent P_D supports local silence and global memory",
    },
    {
        "contract": "own_boundary_primitive",
        "required_statement": "local boundary primitive/charge for Cperp vanishes or is pure gauge",
        "pass_condition": "no material marker or hidden boundary hair remains",
    },
    {
        "contract": "retain_Ward_accounting",
        "required_statement": "projector/domain/selector stresses from the lifted C-sector are varied and retained",
        "pass_condition": "no fake conservation is introduced by the lift",
    },
    {
        "contract": "recover_projected_metric_as_theorem",
        "required_statement": "matter invariance under representative shifts selects exp(P_D C)g",
        "pass_condition": "projected metric becomes theorem rather than closure",
    },
]


RESIDUAL_RUNNER_UPDATE = [
    {
        "residual": "eta_WEP",
        "source_locked_scale_abs": 2.8e-15,
        "after_demote_policy": "direct vertices conditionally absent only inside closure branch; no pass claim",
        "runner_action": "keep WEP residual block active unless lifted C/the selector is derived",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale_abs": 3.1e-5,
        "after_demote_policy": "common-mode P_D C drift/gradient still open",
        "runner_action": "keep clock residual explicit and schedule common-mode silence/bound test",
    },
    {
        "residual": "gamma_minus_1",
        "source_locked_scale_abs": 2.3e-5,
        "after_demote_policy": "nonmetric Cperp mismatch conditionally removed only by closure",
        "runner_action": "keep gamma residuals from boundary/operator/nonmetric sectors explicit",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale_abs": "",
        "after_demote_policy": "scalar Cperp physical branch would become fifth-force risk",
        "runner_action": "remain quarantined until source-locked or zero theorem supplied",
    },
]


DECISION_MATRIX = [
    {
        "claim": "current scalar Cperp is relative-exact/gauge",
        "status": "rejected",
        "evidence": "cohomology transfer tests fail; Hamiltonian/presymplectic conditions not derived",
    },
    {
        "claim": "projected metric is parent-derived now",
        "status": "rejected",
        "evidence": "depends on scalar Cperp exactness/gauge principle that failed",
    },
    {
        "claim": "projected metric is an explicit closure in the current scalar C-sector",
        "status": "pass",
        "evidence": "exp(P_D C)g can be used only with closure labels and residual runner guards",
    },
    {
        "claim": "projected metric route is dead forever",
        "status": "not_supported",
        "evidence": "lifted C form/holonomy/class route remains a legitimate future theorem route",
    },
    {
        "claim": "local GR/PPN follows",
        "status": "rejected",
        "evidence": "closure demotion blocks promotion and leaves WEP/clock/operator/nohair gates open",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "write the closure ledger and future lifted-C route contract so later files cannot overclaim exp(P_D C)g",
        "pass_condition": "every local-GR/coupling statement marks projected metric as closure unless lifted C theorem is supplied",
    },
    {
        "priority": 2,
        "target": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "task": "attempt the harder route where C is a form/connection/holonomy/boundary class rather than scalar",
        "pass_condition": "local Cperp becomes exact/null while FLRW P_D C survives",
    },
    {
        "priority": 3,
        "target": "365-common-mode-clock-redshift-bound-for-projected-closure.md",
        "task": "bound local drift/gradient of P_D C in the closure branch against clock guardrails",
        "pass_condition": "clock residual is source-locked, coefficient-aware, and not advertised as theorem",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def prior_361_rows() -> list[dict[str, Any]]:
    path = RUN_361 / "results" / "decision_matrix.csv"
    if not path.exists():
        return [{"source": str(path), "issue": "missing"}]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {
                "prior_claim": row["claim"],
                "prior_status": row["status"],
                "prior_evidence": row["evidence"],
                "after_362_update": "superseded_by_closure_decision" if "projected matter metric is now parent-derived" in row["claim"] or "Cperp is proven" in row["claim"] else "retained_as_context",
            }
            for row in csv.DictReader(handle)
        ]


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_tests = sum(1 for row in EXACTNESS_TESTS if "fail" in row["result"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "Cperp_exactness_tests_run",
            "status": "pass",
            "evidence": f"{len(EXACTNESS_TESTS)} exactness tests recorded; {failed_tests} fail or conditionally fail",
        },
        {
            "gate": "scalar_Cperp_exactness_derived",
            "status": "fail",
            "evidence": "current scalar Cperp does not inherit J_rel relative-cohomology exactness",
        },
        {
            "gate": "projected_metric_demoted_to_closure",
            "status": "pass",
            "evidence": "exp(P_D C)g labelled explicit effective closure for current scalar C-sector",
        },
        {
            "gate": "future_lifted_C_route_kept",
            "status": "pass",
            "evidence": "form/connection/holonomy/class route contract written rather than declaring route dead",
        },
        {
            "gate": "WEP_clock_runner_updated",
            "status": "pass",
            "evidence": "WEP/clock/nonmetric residuals remain explicit unless lifted C theorem is supplied",
        },
        {
            "gate": "projected_metric_parent_promotion",
            "status": "fail",
            "evidence": "selector theorem depends on exactness that failed for current scalar C-sector",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "closure demotion and unresolved nohair/EH/PPN gates block local-GR claim",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "Cperp_scalar_exactness_derived": False,
            "projected_metric_status": "explicit_effective_closure_current_scalar_C_sector",
            "lifted_C_route_open": True,
            "WEP_clock_pass_claimed": False,
            "local_GR_promoted": False,
            "main_result": "current scalar Cperp exactness fails; exp(P_D C)g is demoted to explicit closure while lifted C form/holonomy route remains open",
            "next_target": NEXT_TARGET,
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    outputs = {
        "source_register.csv": source_rows,
        "prior_361_decision_update.csv": prior_361_rows(),
        "exactness_transfer_tests.csv": EXACTNESS_TESTS,
        "closure_policy.csv": CLOSURE_POLICY,
        "lifted_C_route_contract.csv": LIFTED_C_ROUTE_CONTRACT,
        "residual_runner_update.csv": RESIDUAL_RUNNER_UPDATE,
        "decision_matrix.csv": DECISION_MATRIX,
        "next_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gate_result_rows(source_rows),
        "decision.csv": decision_rows(),
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "exactness_tests": len(EXACTNESS_TESTS),
        "Cperp_scalar_exactness_derived": False,
        "projected_metric_status": "explicit_effective_closure_current_scalar_C_sector",
        "lifted_C_route_open": True,
        "WEP_clock_pass_claimed": False,
        "local_GR_promoted": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
