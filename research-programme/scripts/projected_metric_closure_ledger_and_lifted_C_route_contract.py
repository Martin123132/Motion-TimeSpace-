from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "projected-metric-closure-ledger-and-lifted-C-route-contract"
STATUS = "projected_metric_closure_ledger_written_lifted_C_derivation_contract_set_GR_route_kept_open"
CLAIM_CEILING = "contract_only_no_lifted_C_theorem_no_local_GR_WEP_clock_or_PPN_promotion"
NEXT_TARGET = "364-lifted-C-sector-form-holonomy-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "346-GR-and-derivation-north-star-spine.md",
        "role": "north-star rule that GR reduction and derivation outrank empirical convenience",
    },
    {
        "path": "355-GR-reduction-and-derivation-priority-ledger.md",
        "role": "local GR reduction ledger and derivation-first priority stack",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "Einstein-Hilbert exterior operator requirements and no-promotion decision",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked residual runner and local bound guardrails",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "single observed coframe and universal matter coupling contract",
    },
    {
        "path": "361-residual-gauge-principle-for-projected-matter-metric.md",
        "role": "projected metric selector if Cperp is residual gauge/exact data",
    },
    {
        "path": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
        "role": "scalar Cperp exactness rejection and projected-metric closure demotion",
    },
    {
        "path": "runs/20260601-194500-Cperp-relative-exactness-or-projected-metric-closure-decision/results/decision.csv",
        "role": "machine-readable checkpoint 362 closure decision",
    },
]


GR_REDUCTION_SPINE = [
    {
        "layer": "operator",
        "target_statement": "local exterior equations reduce to metric-only four-dimensional second-order Einstein-Hilbert form",
        "current_status": "not_derived",
        "blocker": "Ward closure is necessary but not sufficient for unique EH operator",
        "source": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "next_action": "derive or explicitly assume the metric-only spin-2 exterior operator conditions",
    },
    {
        "layer": "matter",
        "target_statement": "all species couple to one observed coframe/metric with no direct non-geometric MTS vertex",
        "current_status": "conditional_contract",
        "blocker": "projected selector depends on Cperp exactness or closure",
        "source": "360-universal-matter-coupling-theorem-attempt.md",
        "next_action": "derive the observed metric selector from parent invariance rather than impose it",
    },
    {
        "layer": "projected_metric_selector",
        "target_statement": "matter invariance under representative shifts selects ghat_mn = exp(P_D C) g_mn",
        "current_status": "closure_in_scalar_C_sector",
        "blocker": "scalar Cperp exactness rejected in checkpoint 362",
        "source": "361-residual-gauge-principle-for-projected-matter-metric.md;362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
        "next_action": "lift C to a class/form/holonomy object and prove local Cperp is gauge/null",
    },
    {
        "layer": "local_tests",
        "target_statement": "PPN, WEP, clock, and fifth-force residuals vanish or stay below source-locked bounds",
        "current_status": "guardrail_runner_ready_no_pass",
        "blocker": "coefficients and selector theorem are not derived",
        "source": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "next_action": "keep residual vector explicit until lifted C and EH exterior gates pass",
    },
    {
        "layer": "newtonian_limit",
        "target_statement": "weak-field slow-motion limit gives Poisson plus geodesic acceleration for the observed metric",
        "current_status": "target_not_claim",
        "blocker": "requires EH/operator gate and universal observed metric gate",
        "source": "355-GR-reduction-and-derivation-priority-ledger.md",
        "next_action": "only derive after local operator and matter metric are parent-owned",
    },
]


CLOSURE_LEDGER = [
    {
        "object": "ghat_mn = exp(P_D C) g_mn",
        "current_label": "explicit_effective_closure",
        "allowed_role": "testable effective branch and theorem target",
        "forbidden_role": "parent-derived matter metric or local-GR proof",
        "upgrade_condition": "derive lifted C representative invariance and local Cperp null/exactness",
    },
    {
        "object": "scalar Cperp",
        "current_label": "physical_risk_or_unproved_gauge",
        "allowed_role": "residual variable inside runner or demoted closure branch",
        "forbidden_role": "silent gauge degree in scalar sector",
        "upgrade_condition": "show it is not fundamental scalar data but representative data of a class variable",
    },
    {
        "object": "P_D projector",
        "current_label": "conditional_parent_target",
        "allowed_role": "domain projector to be varied and stress-accounted",
        "forbidden_role": "external fixed selector inserted after variation",
        "upgrade_condition": "derive from parent domain/action variables with Bianchi/Ward accounting",
    },
    {
        "object": "universal matter coupling",
        "current_label": "conditional_contract",
        "allowed_role": "single observed coframe branch with direct species vertices absent by construction",
        "forbidden_role": "WEP pass without selector and coefficient theorem",
        "upgrade_condition": "prove all matter actions depend only on parent-owned observed coframe",
    },
    {
        "object": "local GR branch",
        "current_label": "open_not_promoted",
        "allowed_role": "derivation target with local bound runner",
        "forbidden_role": "claim recovered because closure branch looks metric",
        "upgrade_condition": "EH operator, universal coupling, and residual-vector gates all pass",
    },
]


LIFTED_C_CONTRACT = [
    {
        "requirement": "replace_scalar_with_class_representative",
        "exact_contract": "C is a representative of a connection, form, holonomy, boundary, or relative class rather than a standalone local scalar",
        "why_it_matters_for_GR": "local representative noise can be quotient data while the observed metric remains universal",
        "failure_mode": "ordinary scalar Cperp creates fifth-force, clock, WEP, and nonmetric residuals",
    },
    {
        "requirement": "derive_local_kernel_nullness",
        "exact_contract": "for compact local domains, Cperp lies in a gauge/presymplectic-null/exact kernel with vanishing local boundary primitive",
        "why_it_matters_for_GR": "matter cannot see local nonmetric representative mismatch",
        "failure_mode": "projected metric remains imposed closure",
    },
    {
        "requirement": "preserve_global_memory",
        "exact_contract": "the same parent structure leaves P_D C or class observables nonzero on FLRW/cosmological domains",
        "why_it_matters_for_GR": "local GR silence does not erase the cosmology pillar",
        "failure_mode": "the lift kills the signal it was meant to explain",
    },
    {
        "requirement": "vary_projector_and_domain_data",
        "exact_contract": "projector, domain, and boundary variables are varied before conservation laws are read",
        "why_it_matters_for_GR": "Bianchi/Ward identities are real rather than bookkeeping tricks",
        "failure_mode": "hidden external selector stress violates conservation",
    },
    {
        "requirement": "recover_observed_metric_theorem",
        "exact_contract": "representative-shift invariance forces matter to depend on exp(P_D C)g and not on Cperp",
        "why_it_matters_for_GR": "closure metric becomes derived metric, opening the WEP/local-GR route",
        "failure_mode": "common metric is only an empirical ansatz",
    },
    {
        "requirement": "connect_to_EH_exterior",
        "exact_contract": "after quotienting local representative data, the exterior metric operator is EH plus controlled residuals",
        "why_it_matters_for_GR": "this is the actual GR reduction target",
        "failure_mode": "the theory is a modified-gravity/dark-sector model rather than a GR-reducing field theory",
    },
]


NO_SMUGGLING_RULES = [
    {
        "rule": "closure_labels_visible",
        "required_practice": "every use of exp(P_D C)g says closure unless lifted C theorem is supplied",
        "violation": "calling the projected metric parent-derived from scalar Cperp",
    },
    {
        "rule": "GR_reduction_before_GR_claim",
        "required_practice": "local GR means EH operator plus universal matter metric plus residual vector controlled",
        "violation": "using one successful sub-gate as if it proves GR",
    },
    {
        "rule": "derive_or_bound_every_residual",
        "required_practice": "WEP, clock, gamma, beta, and fifth-force terms are either zero by theorem or bounded by runner",
        "violation": "dropping a residual because it is inconvenient",
    },
    {
        "rule": "compare_against_baselines",
        "required_practice": "empirical tests compare MTS closures against appropriate GR/LCDM/DM/MOND baselines where meaningful",
        "violation": "holding only MTS to stress tests and treating pipeline failures as theory failures",
    },
    {
        "rule": "local_and_cosmic_same_parent",
        "required_practice": "the same parent object must explain local silence and cosmic memory activation",
        "violation": "using separate unrelated mechanisms for GR and cosmology without a bridge",
    },
]


THEOREM_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt the lifted C form/holonomy/class theorem rather than assume the projected metric",
        "pass_condition": "local Cperp is exact/null while P_D C survives as global memory",
    },
    {
        "priority": 2,
        "target": "365-EH-exterior-reduction-after-lifted-C-gate.md",
        "task": "if lifted C passes, reconnect to the EH exterior operator gate",
        "pass_condition": "metric-only second-order exterior equations follow or a residual operator is bounded",
    },
    {
        "priority": 3,
        "target": "366-source-locked-local-residual-vector-after-lifted-C.md",
        "task": "rerun the local residual ledger after the selector theorem attempt",
        "pass_condition": "WEP, clock, gamma, beta, and fifth-force entries are derived zero or quantitatively bounded",
    },
    {
        "priority": 4,
        "target": "367-Newtonian-limit-from-observed-metric.md",
        "task": "derive the Newtonian weak-field slow-motion limit only after observed metric ownership is settled",
        "pass_condition": "Poisson equation and geodesic acceleration emerge with identified residual terms",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "the next derivation route is lifted C; scalar projected metric remains closure until that theorem exists",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
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
            "gate": "checkpoint_362_imported",
            "status": "pass",
            "evidence": "scalar Cperp exactness rejection is treated as binding for the current branch",
        },
        {
            "gate": "closure_ledger_written",
            "status": "pass",
            "evidence": "projected metric, scalar Cperp, P_D, matter coupling, and local GR labels recorded",
        },
        {
            "gate": "lifted_C_contract_written",
            "status": "pass",
            "evidence": "six theorem requirements define the route that could upgrade closure to derivation",
        },
        {
            "gate": "no_smuggling_rules_written",
            "status": "pass",
            "evidence": "rules block projected-metric, GR, and residual overclaims",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "EH operator, lifted C selector, and residual-vector gates are still open",
        },
        {
            "gate": "derivation_priority_preserved",
            "status": "pass",
            "evidence": "next target is a theorem attempt, not a numerical fit or closure patch",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "gr_reduction_spine.csv", GR_REDUCTION_SPINE)
    write_csv(results_dir / "closure_ledger.csv", CLOSURE_LEDGER)
    write_csv(results_dir / "lifted_C_contract.csv", LIFTED_C_CONTRACT)
    write_csv(results_dir / "no_smuggling_rules.csv", NO_SMUGGLING_RULES)
    write_csv(results_dir / "theorem_queue.csv", THEOREM_QUEUE)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 363 closure ledger and lifted C route contract artifacts."
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
