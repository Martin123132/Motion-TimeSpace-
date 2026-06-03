from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-no-Cperp-action-or-closure"
STATUS = "parent_no_Cperp_quotient_action_skeleton_constructed_quotient_principle_not_derived"
CLAIM_CEILING = "quotient_action_skeleton_internal_only_no_local_GR_or_unification_promotion"

B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05


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
    sources = [
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector and Bianchi accounting"),
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "topological projector parent skeleton"),
        (ROOT / "269-metric-selector-principle-attempt.md", "metric selector conditional theorem"),
        (ROOT / "270-Cperp-residual-shift-constraint-attempt.md", "Cperp first-class route"),
        (ROOT / "scripts" / "parent_no_Cperp_action_or_closure.py", "this quotient-action gate"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def quotient_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "configuration_space",
            "allowed_variable": "[C] = C / ker(P_D), represented by C_D = P_D C",
            "forbidden_dependence": "raw Cperp representative",
            "invariance_result": "Cperp -> Cperp + eta_perp leaves physical variables unchanged",
            "status": "quotient_axiom_not_derived",
        },
        {
            "sector": "gravity_local",
            "allowed_variable": "g_munu plus EH/local metric variables",
            "forbidden_dependence": "Cperp kinetic or gradient energy",
            "invariance_result": "local EH limit not directly polluted by Cperp",
            "status": "background_contract",
        },
        {
            "sector": "memory_class",
            "allowed_variable": "C_D, relative/topological classes, J_rel projected class",
            "forbidden_dependence": "representative-level Cperp potential V(Cperp)",
            "invariance_result": "delta_H/delta_Cperp = 0 for class potential",
            "status": "conditional_skeleton",
        },
        {
            "sector": "matter_metric",
            "allowed_variable": "bar_g_munu = exp(C_D) g_munu",
            "forbidden_dependence": "exp(C_D + epsilon Cperp) with epsilon != 0",
            "invariance_result": "delta S_matter / delta Cperp = 0",
            "status": "conditional_previous",
        },
        {
            "sector": "projector_topology",
            "allowed_variable": "metric-independent relative-chain P_D and wedge/topological constraints",
            "forbidden_dependence": "Hodge/metric least-energy projector for local no-hair",
            "invariance_result": "no bulk metric stress from projector in local exterior",
            "status": "conditional_previous",
        },
        {
            "sector": "gauge_fixing",
            "allowed_variable": "optional representative gauge P_D Cperp=0 or boundary primitive choice",
            "forbidden_dependence": "gauge-fixing treated as physical energy",
            "invariance_result": "does not affect quotient observables if Faddeev/gauge stress accounted",
            "status": "optional_not_parent_derived",
        },
        {
            "sector": "boundary_domain",
            "allowed_variable": "domain labels, W_D, boundary terms, relative class data",
            "forbidden_dependence": "frozen external domain average",
            "invariance_result": "Noether/Bianchi possible only if varied",
            "status": "required_open",
        },
    ]


def Hamiltonian_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "matter Hamiltonian",
            "ordinary_risk": "depends on exp(C_D+Cperp)g",
            "quotient_form": "depends on exp(C_D)g",
            "deltaH_deltaCperp": "0",
            "status": "conditional_pass",
        },
        {
            "term": "C kinetic term",
            "ordinary_risk": "pi_perp^2 or dot(Cperp)^2",
            "quotient_form": "no Cperp kinetic term; pi_perp approx 0",
            "deltaH_deltaCperp": "0 if primary constraint preserved",
            "status": "skeleton_pass_not_parent_derived",
        },
        {
            "term": "C gradient term",
            "ordinary_risk": "(nabla Cperp)^2 local stiffness",
            "quotient_form": "only class/topological boundary terms; no representative gradient energy",
            "deltaH_deltaCperp": "0 up to boundary/gauge-fixing",
            "status": "skeleton_pass_not_parent_derived",
        },
        {
            "term": "memory potential",
            "ordinary_risk": "V(C_D+Cperp)",
            "quotient_form": "V(C_D, class data)",
            "deltaH_deltaCperp": "0",
            "status": "conditional_pass",
        },
        {
            "term": "topological projector",
            "ordinary_risk": "metric/Hodge projection creates physical representative dependence",
            "quotient_form": "relative-chain wedge constraints only",
            "deltaH_deltaCperp": "0 for exact representative shifts",
            "status": "conditional_previous",
        },
        {
            "term": "domain boundary",
            "ordinary_risk": "external domain selection hides stress",
            "quotient_form": "domain labels/boundaries varied with stress retained",
            "deltaH_deltaCperp": "not enough alone; needed for covariance",
            "status": "open",
        },
    ]


def derivation_vs_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "question": "Can a no-Cperp parent action be written?",
            "answer": "yes_conditionally",
            "evidence": "all physical sectors can be written on quotient variable C_D and class data",
            "consequence": "Hamiltonian Cperp independence follows inside this skeleton",
        },
        {
            "question": "Is the quotient configuration principle derived?",
            "answer": "no",
            "evidence": "the action starts from [C]=C/ker(P_D); it does not yet derive why this is the physical configuration space",
            "consequence": "not a parent theorem",
        },
        {
            "question": "Does this improve over closure?",
            "answer": "yes",
            "evidence": "it states the exact action-level condition needed for first-class Cperp",
            "consequence": "the branch is mathematically disciplined",
        },
        {
            "question": "Is projected metric selector promoted?",
            "answer": "no",
            "evidence": "quotient principle, domain scale, and FLRW amplitude remain open",
            "consequence": "no local-GR or unification claim",
        },
        {
            "question": "What if quotient principle fails?",
            "answer": "demote_to_closure",
            "evidence": "then exp(P_D C)g is an imposed effective coupling",
            "consequence": "local branch remains closure-supported only",
        },
    ]


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "Q1_quotient_configuration_space",
            "required_form": "physical C-sector is [C]=C/ker(P_D), not raw C",
            "status": "not_derived",
            "failure_mode": "Cperp may be physical",
        },
        {
            "contract": "Q2_no_representative_dynamics",
            "required_form": "no kinetic/gradient/potential terms for Cperp except gauge-fixing/exact boundary terms",
            "status": "skeleton_constructed",
            "failure_mode": "Cperp becomes local scalar",
        },
        {
            "contract": "Q3_universal_quotient_matter_metric",
            "required_form": "all matter sees exp(C_D)g",
            "status": "conditional_previous",
            "failure_mode": "WEP/composition/local trace source danger",
        },
        {
            "contract": "Q4_topological_projector",
            "required_form": "P_D metric-independent relative-chain projector",
            "status": "conditional_previous",
            "failure_mode": "projector stress or Hodge tuning",
        },
        {
            "contract": "Q5_domain_variation",
            "required_form": "domain labels/weights/boundaries varied; stresses retained",
            "status": "open",
            "failure_mode": "Bianchi violation hidden by external average",
        },
        {
            "contract": "Q6_FLRW_reduction",
            "required_form": "same quotient/projector yields coherent FLRW memory class",
            "status": "open",
            "failure_mode": "local repair not unified with cosmology",
        },
        {
            "contract": "Q7_amplitude_and_scale",
            "required_form": "derive B_mem=2/27 and Hstar=H0 or keep closure",
            "status": "not_derived",
            "failure_mode": "no parent amplitude promotion",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "no_Cperp_action_writeable",
            "result": "conditional_pass",
            "evidence": "quotient action depends on C_D and classes, not raw Cperp",
            "claim_effect": "first-class Hamiltonian condition can be satisfied by construction",
        },
        {
            "gate": "quotient_principle_parent_derived",
            "result": "fail_open",
            "evidence": "configuration space quotient is assumed, not derived",
            "claim_effect": "no theorem promotion",
        },
        {
            "gate": "Hamiltonian_Cperp_independence",
            "result": "conditional_pass_inside_skeleton",
            "evidence": "matter/kinetic/gradient/potential terms omit Cperp",
            "claim_effect": "solves checkpoint-270 condition if quotient axiom is granted",
        },
        {
            "gate": "Bianchi_domain_stress",
            "result": "open",
            "evidence": "domain variation/stress must still be retained",
            "claim_effect": "conservation remains conditional",
        },
        {
            "gate": "unified_FLRW_reduction",
            "result": "open",
            "evidence": "same quotient action has not derived B_mem or FLRW memory projection",
            "claim_effect": "no unification claim",
        },
        {
            "gate": "closure_policy",
            "result": "explicit",
            "evidence": "if Q1 fails, projected matter metric is imposed effective closure",
            "claim_effect": "prevents silent overclaim",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "Q1, Q5, Q6, Q7 remain open",
            "claim_effect": "no local-GR or unification promotion",
        },
    ]


def numeric_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "fixed closure/theorem target carried forward",
        },
        {
            "quantity": "epsilon_local_DeltaC_max",
            "value": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "residual Cperp matter coupling bound if quotient coupling leaks",
        },
        {
            "quantity": "epsilon_local_qR_max",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter local qR-like residual coupling bound",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A parent no-Cperp action can be constructed as a quotient-action skeleton: all physical sectors depend on C_D=P_D C and class data, "
                "so delta H/delta Cperp=0 follows inside the skeleton. But this starts by assuming the quotient configuration principle [C]=C/ker(P_D); "
                "that principle is not yet derived. Therefore the projected metric selector is a disciplined theorem target, not a promoted result."
            ),
            "next_target": "derive_quotient_configuration_principle_from_topological_projector_or_label_projected_metric_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "quotient_action_skeleton.csv": (
            quotient_action_rows(),
            ["sector", "allowed_variable", "forbidden_dependence", "invariance_result", "status"],
        ),
        "Hamiltonian_independence_audit.csv": (
            Hamiltonian_audit_rows(),
            ["term", "ordinary_risk", "quotient_form", "deltaH_deltaCperp", "status"],
        ),
        "derivation_vs_closure.csv": (derivation_vs_closure_rows(), ["question", "answer", "evidence", "consequence"]),
        "theorem_contract.csv": (theorem_contract_rows(), ["contract", "required_form", "status", "failure_mode"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "numeric_bounds.csv": (numeric_rows(), ["quantity", "value", "meaning"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision_rows()[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "no_Cperp_action_writeable": True,
        "Hamiltonian_Cperp_independence_inside_skeleton": True,
        "quotient_configuration_principle_derived": False,
        "projected_metric_selector_promoted": False,
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "derive_quotient_configuration_principle_from_topological_projector_or_label_projected_metric_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parent no-Cperp quotient action or closure gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
