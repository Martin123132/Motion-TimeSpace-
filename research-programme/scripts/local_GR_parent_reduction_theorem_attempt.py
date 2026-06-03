from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-parent-reduction-theorem-attempt"
STATUS = "local_GR_parent_reduction_conditional_theorem_written_N5_parent_action_blockers_remain_no_PPN_promotion"
CLAIM_CEILING = "conditional_GR_reduction_only_no_local_GR_or_PPN_claim"


SOURCE_DOCS = [
    ("177-parent-action-perturbation-local-GR-contract.md", "parent action / perturbation / local-GR contract"),
    ("234-boundary-metric-variation-and-Bianchi-ledger.md", "projector stress and Bianchi ledger"),
    ("236-local-EH-operator-or-constraint-algebra-decision.md", "local EH exterior route decision"),
    ("245-exact-relative-memory-or-projector-stress-bianchi.md", "N4 exact memory and N5 projector-stress obligation"),
    ("247-local-EH-exterior-sufficiency-stack-no-promotion.md", "conditional local EH sufficiency theorem"),
    ("250-local-GR-gate-scorecard-and-test-readiness.md", "current local-GR scorecard"),
    ("261-Hstar-H0-scale-lock-and-local-silence-attempt.md", "scale lock and local-silence status"),
    ("346-GR-and-derivation-north-star-spine.md", "north-star project spine"),
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": path.exists(),
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this theorem-ledger builder",
            "exists": script_path.exists(),
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def theorem_statement_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "parent_action_form",
            "statement": (
                "S_parent = (1/2kappa) int sqrt(-g)(R-2Lambda) + S_m[g,psi] + "
                "S_MTS[g, X, P_mem, projectors, boundary/domain variables]"
            ),
            "status": "contract_form_only",
            "source": "177; 236; 346",
            "note": "metric/coframe and MTS sector must be varied, not fitted in after the fact",
        },
        {
            "item": "metric_variation_identity",
            "statement": "G_munu + Lambda g_munu = kappa T_munu + E_MTS_munu",
            "status": "conditional_identity",
            "source": "177; 234",
            "note": "E_MTS_munu is only legitimate if obtained by varying S_MTS",
        },
        {
            "item": "bianchi_identity",
            "statement": "nabla_mu (T_matter^munu + kappa^-1 E_MTS^munu) = 0",
            "status": "conditional_on_diffeomorphism_invariant_parent_action",
            "source": "177; 234; 245",
            "note": "dropping projector stress breaks the conservation ledger",
        },
        {
            "item": "local_GR_reduction_theorem",
            "statement": (
                "If E_MTS_munu has no bulk exterior support, hidden projector stress is zero or retained "
                "conservedly, matter is minimally coupled to one metric/coframe, and the local exterior action "
                "is Einstein-Hilbert, then the local weak-field/PPN limit is GR with residual vector zero."
            ),
            "status": "conditional_theorem",
            "source": "247; 250; 346",
            "note": "this is a real finite theorem target, but its premises are not all parent-derived",
        },
    ]


def n_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "N0_unique_metric_coframe",
            "needed_for": "single geometry for matter, clocks, rulers, lensing, and PPN",
            "current_status": "specified_contract_not_fully_derived",
            "blocks_promotion": True,
            "next_action": "derive matter coupling from parent action rather than imposing physical metric by convention",
        },
        {
            "gate": "N1_exterior_ordinary_matter_absent",
            "needed_for": "vacuum exterior around compact source",
            "current_status": "definition_pass_for_exterior_region",
            "blocks_promotion": False,
            "next_action": "keep as definition of the local exterior, not as a test result",
        },
        {
            "gate": "N2_no_trace_free_shear_stress",
            "needed_for": "gamma=1 and no anisotropic projector force",
            "current_status": "conditional",
            "blocks_promotion": True,
            "next_action": "show trace-free projector/boundary sector vanishes or is carried in conserved stress",
        },
        {
            "gate": "N3_no_local_scalar_vector_hair",
            "needed_for": "no fifth-force, preferred-frame, or clock residuals",
            "current_status": "conditional",
            "blocks_promotion": True,
            "next_action": "prove no-hair/screening for local boundary/domain variables",
        },
        {
            "gate": "N4_exact_relative_memory",
            "needed_for": "relative memory is pure gauge/topological in local exterior",
            "current_status": "conditional_pass",
            "blocks_promotion": True,
            "next_action": "tie exactness to N5 so pure-gauge memory does not hide stress",
        },
        {
            "gate": "N5_projector_stress_Bianchi_safe",
            "needed_for": "metric-only Einstein-Hilbert exterior and conserved local equations",
            "current_status": "open_hard_blocker",
            "blocks_promotion": True,
            "next_action": "derive T_projector=0, boundary-only cancellation, or retained conserved T_projector",
        },
        {
            "gate": "N6_metric_only_EH_exterior",
            "needed_for": "Einstein equation and Schwarzschild/Newton/PPN limit",
            "current_status": "blocked_by_N5_and_parent_action_ownership",
            "blocks_promotion": True,
            "next_action": "derive exterior EH operator from parent action after N5 is owned",
        },
    ]


def ppn_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "delta_gamma",
            "symbolic_owner": "trace-free spatial residual E_MTS^TF_ij / anisotropic projector stress",
            "zero_condition": "N2 and N5 eliminate or conservedly retain trace-free projector stress with no bulk exterior support",
            "current_status": "symbolic_bound_only",
            "promotion_allowed": False,
        },
        {
            "residual": "delta_beta",
            "symbolic_owner": "second-order scalar residual E_MTS^(2)_00 plus nonlinear stress conservation/no-hair terms",
            "zero_condition": "N3, N5, and N6 give metric-only EH exterior through post-Newtonian order",
            "current_status": "conditional_on_EH_stack",
            "promotion_allowed": False,
        },
        {
            "residual": "preferred_frame_alpha1_alpha2",
            "symbolic_owner": "vector residual E_MTS_0i and any domain-frame vector hair",
            "zero_condition": "single physical coframe plus no local vector/domain hair",
            "current_status": "uncomputed_symbolic",
            "promotion_allowed": False,
        },
        {
            "residual": "clock_redshift_drift",
            "symbolic_owner": "direct matter-clock coupling to MTS variables or local scalar gradients",
            "zero_condition": "matter couples only to g/e and MTS local gradients vanish or are screened",
            "current_status": "uncomputed_symbolic",
            "promotion_allowed": False,
        },
        {
            "residual": "WEP_fifth_force",
            "symbolic_owner": "composition-dependent coupling in S_matter or unscreened local MTS force",
            "zero_condition": "universal metric/coframe coupling and no local MTS force on matter species",
            "current_status": "uncomputed_symbolic",
            "promotion_allowed": False,
        },
    ]


def closure_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_or_axiom": "physical metric/coframe selection",
            "why_needed": "GR reduction requires one geometry for all local observables",
            "current_state": "contracted but not parent-derived",
            "if_not_derived": "explicit local-GR closure axiom",
        },
        {
            "closure_or_axiom": "N5 projector stress zero/retained theorem",
            "why_needed": "prevents fake Bianchi conservation and metric-only EH overclaim",
            "current_state": "open hard blocker",
            "if_not_derived": "local branch remains closure/proxy only",
        },
        {
            "closure_or_axiom": "local no-hair/screening",
            "why_needed": "kills scalar/vector/fifth-force/clock residuals",
            "current_state": "conditional",
            "if_not_derived": "PPN residual vector cannot be set to zero",
        },
        {
            "closure_or_axiom": "metric-only Einstein-Hilbert exterior",
            "why_needed": "gives Newton/Schwarzschild/PPN GR limit",
            "current_state": "conditional sufficiency theorem, not parent-derived",
            "if_not_derived": "MTS is not yet a GR-reducing field theory",
        },
        {
            "closure_or_axiom": "PPN residual vector calculation",
            "why_needed": "turns local silence into measurable gamma/beta/preferred-frame/clock bounds",
            "current_state": "symbolic map only",
            "if_not_derived": "local empirical tests remain proxy pressure tests",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], n_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    n5 = next(row for row in n_gates if row["gate"] == "N5_projector_stress_Bianchi_safe")
    n6 = next(row for row in n_gates if row["gate"] == "N6_metric_only_EH_exterior")
    hard_blockers = [row["gate"] for row in n_gates if row["blocks_promotion"] and "open" in row["current_status"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited source files exist" if sources_ok else "missing source file",
        },
        {
            "gate": "conditional_EH_reduction_theorem_written",
            "status": "pass",
            "evidence": "if E_MTS has no conserved bulk exterior support, local EH/PPN GR follows conditionally",
        },
        {
            "gate": "metric_variation_owned_by_parent",
            "status": "fail",
            "evidence": "S_MTS variation is still a contract, not a completed parent derivation",
        },
        {
            "gate": "N5_projector_stress_cleared",
            "status": "fail" if n5["current_status"] == "open_hard_blocker" else "pass",
            "evidence": n5["next_action"],
        },
        {
            "gate": "metric_only_EH_exterior_derived",
            "status": "fail" if "blocked" in n6["current_status"] else "pass",
            "evidence": n6["current_status"],
        },
        {
            "gate": "PPN_residual_vector_calculated",
            "status": "fail",
            "evidence": "symbolic owner map written, numerical/closed-form residuals not derived",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "promotion blocked by parent variation, N5, N6, and uncomputed PPN vector",
        },
        {
            "gate": "branch_declared_dead",
            "status": "fail",
            "evidence": "conditional theorem is coherent; blockers are named rather than fatal",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
        {
            "gate": "hard_blocker_count",
            "status": "info",
            "evidence": ";".join(hard_blockers),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A real conditional GR-reduction theorem has been isolated: if the parent action yields one physical "
                "metric/coframe, diffeomorphism-safe stress accounting, no bulk MTS exterior support, and a metric-only "
                "EH exterior, then local Newton/PPN GR follows. The derivation does not promote because N5 projector "
                "stress, parent variation ownership, and the explicit PPN residual vector remain unresolved."
            ),
            "next_target": "derive_N5_projector_stress_zero_or_retained_conservation_theorem",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem = theorem_statement_rows()
    n_gates = n_gate_rows()
    ppn = ppn_residual_rows()
    closures = closure_ledger_rows()
    gates = gate_rows(sources, n_gates)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source_path", "role", "exists", "issue"]),
        "theorem_statement.csv": (theorem, ["item", "statement", "status", "source", "note"]),
        "local_N_gate_status.csv": (
            n_gates,
            ["gate", "needed_for", "current_status", "blocks_promotion", "next_action"],
        ),
        "ppn_residual_vector_map.csv": (
            ppn,
            ["residual", "symbolic_owner", "zero_condition", "current_status", "promotion_allowed"],
        ),
        "closure_or_axiom_ledger.csv": (
            closures,
            ["closure_or_axiom", "why_needed", "current_state", "if_not_derived"],
        ),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": decisions[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "source_paths_missing": sum(1 for row in sources if not row["exists"]),
        "local_GR_promoted": False,
        "PPN_promoted": False,
        "conditional_theorem_written": True,
        "primary_blocker": "N5_projector_stress_Bianchi_safe",
        "next_target": decisions[0]["next_target"],
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(payload["status"] + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt local GR parent-reduction theorem ledger.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
