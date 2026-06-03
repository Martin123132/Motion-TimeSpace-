from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-EH-exterior-operator-from-Ward-closed-action"
STATUS = "EH_exterior_operator_sufficiency_sharpened_Ward_closure_not_enough_operator_axioms_open_no_local_GR_promotion"
CLAIM_CEILING = "conditional_EH_operator_sufficiency_only_no_parent_EH_derivation_no_local_GR_or_PPN_pass"
NEXT_TARGET = "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md"


SOURCE_DOCS = [
    {
        "path": "236-local-EH-operator-or-constraint-algebra-decision.md",
        "role": "earlier choice to attack the local EH operator route",
    },
    {
        "path": "238-metric-only-exterior-reduction-or-nohair-theorem.md",
        "role": "metric-only exterior sector audit and N1-N6 target stack",
    },
    {
        "path": "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
        "role": "earlier EH sufficiency theorem with N1-N6 premises",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "explicit Ward force ledger",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force fate map and retained residual vector",
    },
    {
        "path": "runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/theorem_or_retain_decisions.csv",
        "role": "machine-readable theorem-or-retain decisions from checkpoint 357",
    },
]


SUFFICIENCY_ASSUMPTIONS = [
    {
        "assumption": "A0_compact_local_exterior",
        "statement": "work outside ordinary matter support; enclosed source appears only as conserved monopole/boundary data",
        "status_after_357": "definition_plus_monopole_condition",
        "why_needed": "separates local vacuum/exterior equations from matter interior",
    },
    {
        "assumption": "A1_single_physical_metric_or_coframe",
        "statement": "all local matter, clocks, rulers, photons, and lab standards see one g/e",
        "status_after_357": "not_derived_hard_open",
        "why_needed": "without this there is no single GR metric to reduce to",
    },
    {
        "assumption": "A2_Ward_force_closure",
        "statement": "F_X + F_P + F_boundary + F_domain + F_matter_nonmetric = 0 or retained residuals are absent through PPN order",
        "status_after_357": "mapped_but_not_proved",
        "why_needed": "conservation cannot be faked by dropping hidden force channels",
    },
    {
        "assumption": "A3_no_local_MTS_bulk_or_boundary_hair",
        "statement": "E_MTS_munu is zero, pure gauge, or conserved monopole boundary renormalization in compact exterior",
        "status_after_357": "candidate_mechanisms_only",
        "why_needed": "nonzero exterior hair produces PPN/fifth-force residuals",
    },
    {
        "assumption": "A4_metric_only_exterior_variables",
        "statement": "after constraints/no-hair, the only local propagating exterior field is the metric/coframe",
        "status_after_357": "not_derived",
        "why_needed": "EH uniqueness applies only after extra scalar/vector/tensor fields are removed",
    },
    {
        "assumption": "A5_local_diffeomorphism_invariant_action",
        "statement": "the remaining exterior action is local and invariant under spacetime diffeomorphisms",
        "status_after_357": "structural_target",
        "why_needed": "Bianchi identity and covariant metric equations require it",
    },
    {
        "assumption": "A6_second_order_metric_equations",
        "statement": "the surviving metric field equations contain no higher than second derivatives",
        "status_after_357": "operator_axiom_not_parent_derived",
        "why_needed": "forbids higher-curvature/f(R)/nonlocal operators that would alter PPN unless suppressed",
    },
    {
        "assumption": "A7_four_dimensional_low_energy_exterior",
        "statement": "the local exterior is effectively four-dimensional at tested scales",
        "status_after_357": "assumed_for_local_tests",
        "why_needed": "EH uniqueness is dimension/low-energy dependent",
    },
]


OPERATOR_BASIS_AUDIT = [
    {
        "operator_family": "Einstein_Hilbert_plus_Lambda",
        "example": "sqrt(-g) (R - 2 Lambda)",
        "allowed_if": "all sufficiency assumptions hold",
        "local_effect": "GR exterior; Newton/PPN standard with gamma=beta=1 after source normalization",
        "status": "target_operator",
    },
    {
        "operator_family": "boundary_topological_terms",
        "example": "Gibbons-Hawking-York / topological Euler-like boundary pieces",
        "allowed_if": "do not change local bulk field equations and boundary charges are monopole/safe",
        "local_effect": "no bulk PPN effect",
        "status": "allowed_if_owned",
    },
    {
        "operator_family": "higher_curvature",
        "example": "R^2, R_munu R^munu, Weyl^2",
        "allowed_if": "coefficients vanish by parent theorem or are suppressed below local bounds",
        "local_effect": "extra massive scalar/spin-2 modes or higher-derivative corrections",
        "status": "must_forbid_or_bound",
    },
    {
        "operator_family": "scalar_tensor_or_auxiliary_metric_couplings",
        "example": "phi R, (nabla phi)^2, V(phi)",
        "allowed_if": "phi is frozen/pure gauge/mass-gapped with no local source",
        "local_effect": "gamma/beta/WEP/fifth-force residuals if active",
        "status": "must_nohair_or_retain",
    },
    {
        "operator_family": "vector_or_preferred_frame_terms",
        "example": "u^mu u^nu R_munu, aether/domain-normal operators",
        "allowed_if": "domain vector is pure gauge/covariant with no local vev",
        "local_effect": "alpha1/alpha2/preferred-frame residuals",
        "status": "quarantined_unless_derived_silent",
    },
    {
        "operator_family": "torsion_or_nonmetricity",
        "example": "T^2, Q^2, independent connection couplings",
        "allowed_if": "connection is Levi-Civita in local exterior or extra pieces are algebraic/boundary-only",
        "local_effect": "spin/WEP/clock/light-cone residuals",
        "status": "must_forbid_or_bound",
    },
    {
        "operator_family": "nonlocal_or_memory_kernel",
        "example": "R Box^-1 R, history/domain memory kernels",
        "allowed_if": "kernel is inactive in compact local exterior or reduced to safe boundary data",
        "local_effect": "scale-dependent fifth force or secular drift",
        "status": "must_nohair_or_bound",
    },
]


EH_OPERATOR_THEOREM = [
    {
        "step": 1,
        "claim": "Ward closure plus no-hair removes hidden nonmetric force channels",
        "result": "conserved local metric stress ledger",
        "status": "conditional_not_proved",
    },
    {
        "step": 2,
        "claim": "single metric/coframe and no extra local propagating fields leave a metric-only exterior",
        "result": "S_ext = S_ext[g] + boundary",
        "status": "conditional_not_proved",
    },
    {
        "step": 3,
        "claim": "local, diffeo-invariant, four-dimensional, second-order metric-only action has EH plus Lambda bulk form",
        "result": "S_ext = (16 pi G_eff)^-1 int sqrt(-g)(R - 2 Lambda_eff) + boundary",
        "status": "conditional_sufficiency",
    },
    {
        "step": 4,
        "claim": "compact local vacuum exterior has negligible Lambda at PPN scale",
        "result": "G_munu = 0 to local PPN order",
        "status": "conditional_sufficiency",
    },
    {
        "step": 5,
        "claim": "static spherical exterior with conserved monopole source is Schwarzschild to weak-field order",
        "result": "Newtonian potential plus gamma=1, beta=1 baseline before residual corrections",
        "status": "conditional_sufficiency",
    },
]


OBSTRUCTION_LEDGER = [
    {
        "obstruction": "Ward_closure_not_enough",
        "meaning": "a conserved metric equation can still be non-EH if higher-curvature or extra field operators remain",
        "required_fix": "derive metric-only second-order operator restriction or bound extra operators",
        "severity": "hard_operator_gate",
    },
    {
        "obstruction": "second_order_axiom_not_parent_derived",
        "meaning": "EH uniqueness relies on excluding R^2/f(R)/nonlocal terms",
        "required_fix": "parent low-energy/regularity theorem that higher operators vanish or are suppressed",
        "severity": "hard_operator_gate",
    },
    {
        "obstruction": "universal_matter_coupling_open",
        "meaning": "even EH metric equations do not give GR observables if matter does not couple universally",
        "required_fix": "derive single matter metric/coframe action",
        "severity": "hard_observable_gate",
    },
    {
        "obstruction": "source_normalization_open",
        "meaning": "Newtonian limit needs measured G and conserved monopole source normalization",
        "required_fix": "derive kappa/G_eff and M_eff mapping from parent action",
        "severity": "normalization_gate",
    },
    {
        "obstruction": "quarantined_preferred_frame_and_fifth_force_sectors",
        "meaning": "alpha1/alpha2/xi/fifth-force bounds are not fully source-locked in the local runner",
        "required_fix": "source-lock numeric sectors or prove zero by theorem",
        "severity": "empirical_gate",
    },
]


WEAK_FIELD_LIMIT_MAP = [
    {
        "quantity": "Newtonian_Poisson_limit",
        "EH_value_if_conditions_hold": "nabla^2 Phi = 4 pi G_eff rho inside weak source; vacuum exterior nabla^2 Phi=0",
        "open_parent_issue": "G_eff/kappa and M_eff source normalization not derived",
        "residual_if_failed": "delta_G_or_fifth_force",
    },
    {
        "quantity": "gamma",
        "EH_value_if_conditions_hold": "gamma = 1",
        "open_parent_issue": "trace-free/shear/operator corrections must vanish",
        "residual_if_failed": "gamma_minus_1",
    },
    {
        "quantity": "beta",
        "EH_value_if_conditions_hold": "beta = 1",
        "open_parent_issue": "nonlinear scalar/boundary/higher-curvature terms must vanish",
        "residual_if_failed": "beta_minus_1",
    },
    {
        "quantity": "preferred_frame",
        "EH_value_if_conditions_hold": "alpha1 = alpha2 = 0",
        "open_parent_issue": "domain/vector/coframe preferred-frame sectors must vanish",
        "residual_if_failed": "preferred_frame_alpha1_alpha2",
    },
    {
        "quantity": "clock_WEP",
        "EH_value_if_conditions_hold": "metric redshift and WEP follow from universal coupling",
        "open_parent_issue": "single matter metric/coframe not derived",
        "residual_if_failed": "alpha_clock_redshift; eta_WEP",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "build the source-locked residual runner using the force-ledger residual vector and operator obstruction flags",
        "pass_condition": "numeric-ready sectors compare against locked gamma/beta/WEP/clock scales while open sectors remain quarantined",
    },
    {
        "priority": 2,
        "target": "360-universal-matter-coupling-theorem-attempt.md",
        "task": "attack the hardest observable gate: one metric/coframe for all matter/clocks/rulers/photons",
        "pass_condition": "derive universal coupling or retain WEP/clock residuals explicitly",
    },
    {
        "priority": 3,
        "target": "361-second-order-EH-operator-parent-selection-or-higher-curvature-bounds.md",
        "task": "derive why higher-curvature/nonlocal operators are absent or bounded",
        "pass_condition": "second-order EH operator becomes parent-derived or higher operators enter the residual runner",
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


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    must_forbid_or_bound = sum(1 for row in OPERATOR_BASIS_AUDIT if "must" in row["status"] or "quarantined" in row["status"])
    open_assumptions = sum(1 for row in SUFFICIENCY_ASSUMPTIONS if "not_derived" in row["status_after_357"] or "not_proved" in row["status_after_357"] or "not_parent_derived" in row["status_after_357"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "EH_sufficiency_stack_written",
            "status": "pass",
            "evidence": f"{len(SUFFICIENCY_ASSUMPTIONS)} assumptions and {len(EH_OPERATOR_THEOREM)} theorem steps mapped",
        },
        {
            "gate": "operator_basis_audited",
            "status": "pass",
            "evidence": f"{len(OPERATOR_BASIS_AUDIT)} operator families audited; {must_forbid_or_bound} require forbidding/bounding/quarantine",
        },
        {
            "gate": "Ward_closure_sufficient_by_itself",
            "status": "fail",
            "evidence": "Ward closure does not exclude higher-curvature, scalar/vector, torsion, nonmetricity, or nonlocal operators",
        },
        {
            "gate": "EH_operator_parent_derived",
            "status": "fail",
            "evidence": f"{open_assumptions} sufficiency assumptions remain not derived/not proved after 357",
        },
        {
            "gate": "weak_field_GR_baseline_conditional",
            "status": "pass",
            "evidence": "if EH sufficiency stack holds, Newton/gamma/beta/preferred-frame/clock-WEP baseline is defined",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "operator axioms, universal coupling, source normalization, and no-hair remain open",
        },
        {
            "gate": "PPN_pass_claimed",
            "status": "fail",
            "evidence": "no numeric residual comparison performed in this operator checkpoint",
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
            "EH_operator_parent_derived": False,
            "local_GR_promoted": False,
            "PPN_pass_claimed": False,
            "main_result": "Ward/nohair closure is necessary but not sufficient; EH exterior follows only with metric-only, local, diffeomorphic, second-order, four-dimensional operator assumptions",
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
    gates = gate_result_rows(source_rows)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": source_rows,
        "EH_sufficiency_assumptions.csv": SUFFICIENCY_ASSUMPTIONS,
        "operator_basis_audit.csv": OPERATOR_BASIS_AUDIT,
        "EH_operator_theorem_steps.csv": EH_OPERATOR_THEOREM,
        "operator_obstruction_ledger.csv": OBSTRUCTION_LEDGER,
        "weak_field_limit_map.csv": WEAK_FIELD_LIMIT_MAP,
        "next_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gates,
        "decision.csv": decisions,
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "sufficiency_assumptions": len(SUFFICIENCY_ASSUMPTIONS),
        "operator_families_audited": len(OPERATOR_BASIS_AUDIT),
        "obstructions": len(OBSTRUCTION_LEDGER),
        "EH_operator_parent_derived": False,
        "local_GR_promoted": False,
        "PPN_pass_claimed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
