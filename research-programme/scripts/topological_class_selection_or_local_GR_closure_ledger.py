from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "topological-class-selection-or-local-GR-closure-ledger"
STATUS = "topological_class_selection_not_parent_derived_local_GR_route_demoted_to_labelled_closure_and_residual_testing"
CLAIM_CEILING = "closure_ledger_and_test_pivot_only_no_class_selection_WEP_PPN_EH_or_local_GR_promotion"
NEXT_TARGET = "368-common-mode-class-metric-clock-PPN-residual-gate.md"


SOURCE_DOCS = [
    {
        "path": "279-representative-selection-boundary-polarization-no-go.md",
        "role": "smooth boundary polarization underselects representative selection",
    },
    {
        "path": "287-boundary-current-charge-owner-attempt.md",
        "role": "relative current supports conservation but not charge level, endpoints, or local class selection",
    },
    {
        "path": "292-relative-index-level-theorem-attempt.md",
        "role": "conditional k=9 relative index route for a B3-like coherent domain",
    },
    {
        "path": "293-domain-topology-selection-attempt.md",
        "role": "B3 topology selection attempt and superselection obstruction",
    },
    {
        "path": "300-boundary-state-local-silence-theorem-attempt.md",
        "role": "IR boundary-bath plus relative class selector contract, not parent-derived",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "boundary primitive derived inside fixed relative class, class selection open",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative-invariant matter selector conditional, class selection open",
    },
]


CLASS_SELECTION_TARGETS = [
    {
        "target": "stationary_local_trivial_class",
        "desired_statement": "local bound/vacuum domains carry Q_rel=0 or exact lifted-C class",
        "why_needed": "local representative/class metric must not create WEP/clock/PPN/fifth-force residuals",
        "current_status": "conditional_branch_assignment",
    },
    {
        "target": "FLRW_nonzero_class",
        "desired_statement": "coherent cosmological domains carry Q_rel != 0 and C_D/P_D C survives",
        "why_needed": "local silence must not erase the cosmology/memory pillar",
        "current_status": "conditional_branch_assignment",
    },
    {
        "target": "same_parent_rule",
        "desired_statement": "one parent class/domain principle gives local zero and FLRW nonzero",
        "why_needed": "otherwise the route is patchwork rather than unified field theory",
        "current_status": "not_derived",
    },
    {
        "target": "no_arbitrary_selector",
        "desired_statement": "no fitted smoothing scale, smooth Pi(C), or hand-picked quiet domain",
        "why_needed": "keeps the route competitive as field theory rather than local-test patch",
        "current_status": "smooth_selector_rejected",
    },
]


TOPOLOGICAL_ROUTE_TESTS = [
    {
        "route": "smooth_boundary_polarization",
        "candidate_rule": "Pi(C_coh) selects local zero and FLRW nonzero representatives",
        "result": "fail",
        "evidence": "endpoint/regularity/monotonicity constraints underselect Pi and add scales",
        "consequence": "cannot promote projected metric or local GR",
    },
    {
        "route": "relative_current_admissibility",
        "candidate_rule": "delta Q_rel[D]=0 restricts allowed boundary/domain variations",
        "result": "conditional_pass_but_not_selection",
        "evidence": "class-preserving variations are owned, but the physical class is not selected",
        "consequence": "boundary primitive silence is admissibility, not full local-GR derivation",
    },
    {
        "route": "relative_index_k9",
        "candidate_rule": "index(D,End(TSigma_D),rel)=+-9 fixes level for a B3 coherent cell",
        "result": "conditional_pass_but_topology_sensitive",
        "evidence": "requires single S2-boundary no-cycle B3-like domain",
        "consequence": "k=9 route is sharpened but depends on underived topology selection",
    },
    {
        "route": "domain_topology_selection",
        "candidate_rule": "parent action forces B3-like coherent cell topology",
        "result": "fail",
        "evidence": "local differential equations do not generally select topology; superselection remains",
        "consequence": "B3/k9 cannot be claimed as parent-derived",
    },
    {
        "route": "boundary_current_quantization",
        "candidate_rule": "integral periods select level, endpoints, and arrow",
        "result": "fail",
        "evidence": "period language does not choose k=9, n_today=1, n_early=3, or arrow 3->1",
        "consequence": "B_mem/u3/amplitude remain theorem targets or closures",
    },
    {
        "route": "IR_boundary_bath_selector",
        "candidate_rule": "sigma_D = Theta(b_D) Theta(c_D) separates local closed/gapped from FLRW open/nontrivial",
        "result": "conditional_pass_but_not_parent_derived",
        "evidence": "selector target precise, but local/FLRW boundary-state split not proven",
        "consequence": "use as residual-test parametrization, not local-GR theorem",
    },
]


CLOSURE_LEDGER = [
    {
        "piece": "fixed_D_Qcoh_projection",
        "status": "derived_for_fixed_D",
        "allowed_use": "define coherent-volume class candidate once D is physically supplied",
        "forbidden_use": "claim physical domain selection",
    },
    {
        "piece": "lifted_C_boundary_primitive",
        "status": "derived_inside_fixed_relative_class",
        "allowed_use": "treat local representative shifts as invisible within a selected class",
        "forbidden_use": "claim parent has selected local Q_rel=0",
    },
    {
        "piece": "representative_invariant_matter_action",
        "status": "conditional_theorem",
        "allowed_use": "forbid direct B_perp/b2/Cperp vertices in the closure branch",
        "forbidden_use": "claim WEP/clock pass or species universality",
    },
    {
        "piece": "class_metric_exp_lambda_CD_g",
        "status": "labelled_effective_closure_and_theorem_target",
        "allowed_use": "test common-mode projected/class metric branch",
        "forbidden_use": "claim fully parent-derived metric selector",
    },
    {
        "piece": "local_Qrel_zero_FLRW_nonzero",
        "status": "closure_branch_assignment",
        "allowed_use": "empirical/residual stress testing with labels",
        "forbidden_use": "claim derived local GR",
    },
    {
        "piece": "EH_exterior_operator",
        "status": "not_derived",
        "allowed_use": "separate theorem target or residual operator ledger",
        "forbidden_use": "use matter/class selector as substitute for EH proof",
    },
]


NO_GO_REASONING = [
    {
        "claim": "topology alone selects the physical class",
        "verdict": "rejected",
        "reason": "topology labels sectors but does not choose which sector is realized without boundary/initial/admissibility data",
    },
    {
        "claim": "relative closure selects the representative",
        "verdict": "rejected",
        "reason": "d_rel J=0 preserves class and supports invariance but does not pick Q_rel=0 locally or Q_rel!=0 cosmologically",
    },
    {
        "claim": "k=9 index is automatic",
        "verdict": "rejected",
        "reason": "k=9 depends on B3-like topology; other admissible topologies give different levels",
    },
    {
        "claim": "matter selector implies local GR",
        "verdict": "rejected",
        "reason": "matter representative invariance does not derive EH exterior operator, common-mode silence, or PPN coefficients",
    },
    {
        "claim": "local route is dead",
        "verdict": "rejected",
        "reason": "it remains a disciplined closure branch and a theorem target, now with exact residual tests to run",
    },
]


RESIDUAL_TEST_PIVOT = [
    {
        "test_area": "common_mode_clock_redshift",
        "closure_input": "ghat_mn=exp(lambda C_D)g_mn with local Q_rel branch assignment",
        "observable": "alpha_clock_redshift and local drift/gradient of C_D/P_D C",
        "acceptance_rule": "derive zero or bound against source-locked clock limits; do not claim pass by assumption",
    },
    {
        "test_area": "PPN_gamma_beta_slip",
        "closure_input": "class metric plus retained residual exterior operator",
        "observable": "gamma-1, beta-1, Phi-Psi, fifth-force terms",
        "acceptance_rule": "compare to GR baseline and source-locked local bounds with coefficients explicit",
    },
    {
        "test_area": "WEP_species_universality",
        "closure_input": "representative-invariant matter action with universal F(C_D)",
        "observable": "eta_WEP and hidden species-specific F_A(C_D) channels",
        "acceptance_rule": "forbid by theorem or keep eta_WEP residual active",
    },
    {
        "test_area": "local_vs_FLRW_class_split",
        "closure_input": "Q_rel_local=0, Q_rel_FLRW!=0",
        "observable": "boundary-state sigma_D, IR MTS bath b_D, class norm c_D",
        "acceptance_rule": "stress-test whether edge cases destroy local silence or cosmology survival",
    },
    {
        "test_area": "empirical_cosmology_closure",
        "closure_input": "class metric amplitude/normalization still labelled closure",
        "observable": "SN/BAO/CMB/growth residuals and AIC/BIC against baselines",
        "acceptance_rule": "compare to LCDM/wCDM/CPL/DM-style baselines, flag prior-edge dependence",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Topological and relative-current machinery sharpen class selection but do not parent-derive local Q_rel=0 and FLRW Q_rel nonzero; local-GR route is demoted to labelled closure plus residual testing.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "turn the class-metric closure into a local residual gate for common-mode clock, PPN, and fifth-force channels",
        "pass_condition": "each residual is theorem-zero, source-locked bounded, or explicitly failed",
    },
    {
        "priority": 2,
        "target": "369-source-locked-closure-branch-local-bound-runner.md",
        "task": "prepare a runnable residual-bound matrix for the labelled closure branch",
        "pass_condition": "WEP/clock/PPN/fifth-force rows have coefficients, source bounds, and branch labels",
    },
    {
        "priority": 3,
        "target": "370-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "task": "separate EH derivation target from residual modified-gravity operator testing",
        "pass_condition": "no matter-selector success is used as a fake EH proof",
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
            "gate": "smooth_polarization_rejected",
            "status": "pass",
            "evidence": "checkpoint 279 underselects Pi(C_coh)",
        },
        {
            "gate": "relative_index_k9_parent_derived",
            "status": "fail",
            "evidence": "k=9 requires underived B3-like topology selection",
        },
        {
            "gate": "relative_current_class_selection_parent_derived",
            "status": "fail",
            "evidence": "relative current preserves/labels class but does not choose local zero or FLRW nonzero",
        },
        {
            "gate": "boundary_state_split_parent_derived",
            "status": "fail",
            "evidence": "IR bath/class selector is a contract, not a proven local/FLRW split",
        },
        {
            "gate": "local_GR_route_demoted_to_labelled_closure",
            "status": "pass",
            "evidence": "closure ledger records derived, conditional, closure, and failed pieces",
        },
        {
            "gate": "residual_test_pivot_written",
            "status": "pass",
            "evidence": "clock/WEP/PPN/fifth-force/local-FLRW split tests queued",
        },
        {
            "gate": "WEP_PPN_EH_or_local_GR_promoted",
            "status": "fail",
            "evidence": "class selection, common-mode silence, and EH operator remain open",
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
    write_csv(results_dir / "class_selection_targets.csv", CLASS_SELECTION_TARGETS)
    write_csv(results_dir / "topological_route_tests.csv", TOPOLOGICAL_ROUTE_TESTS)
    write_csv(results_dir / "closure_ledger.csv", CLOSURE_LEDGER)
    write_csv(results_dir / "no_go_reasoning.csv", NO_GO_REASONING)
    write_csv(results_dir / "residual_test_pivot.csv", RESIDUAL_TEST_PIVOT)
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
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 367 topological class-selection or local-GR closure-ledger artifacts."
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
