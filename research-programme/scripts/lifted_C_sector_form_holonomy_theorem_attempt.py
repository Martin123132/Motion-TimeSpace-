from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "lifted-C-sector-form-holonomy-theorem-attempt"
STATUS = "lifted_C_three_form_local_residual_nullness_conditionally_derived_parent_action_boundary_domain_missing"
CLAIM_CEILING = "conditional_lifted_C_theorem_shape_only_no_parent_selector_EH_WEP_clock_PPN_or_local_GR_promotion"
NEXT_TARGET = "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md"


SOURCE_DOCS = [
    {
        "path": "231-Jrel-cohomology-projector-or-local-EH-limit.md",
        "role": "successful Jrel form-degree cohomology gate and warning not to transfer degrees blindly",
    },
    {
        "path": "273-Cperp-relative-exactness-C-sector.md",
        "role": "scalar Cperp exactness rejection and future lifted C route statement",
    },
    {
        "path": "274-lifted-C-sector-form-holonomy-route.md",
        "role": "earlier lifted C route scan identifying the 3-form domain current as best target",
    },
    {
        "path": "275-JC-three-form-memory-current-from-Q.md",
        "role": "conditional kinematic Q/coherent-volume origin for J_C",
    },
    {
        "path": "276-coherent-domain-projector-from-parent-variables.md",
        "role": "fixed-D coherent projector derivation and unresolved physical domain selector",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal observed coframe contract and matter-coupling gate",
    },
    {
        "path": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
        "role": "binding scalar Cperp failure and projected-metric closure demotion",
    },
    {
        "path": "363-projected-metric-closure-ledger-and-lifted-C-route-contract.md",
        "role": "current lifted C theorem contract and no-smuggling rules",
    },
]


THEOREM_ASSUMPTIONS = [
    {
        "assumption": "lifted_variable",
        "statement": "C is not a fundamental scalar profile; the observable C_D is a domain class built from a 3-form memory current J_C",
        "mathematical_form": "C_D[D] = N_D^{-1} int_D J_C",
        "status": "definition_for_attempt",
    },
    {
        "assumption": "local_representative_shift",
        "statement": "local Cperp changes correspond to exact representative changes of the 3-form current",
        "mathematical_form": "delta J_C = d B_perp",
        "status": "conditional_not_parent_derived",
    },
    {
        "assumption": "stationary_boundary_primitive",
        "statement": "the primitive for local residual shifts vanishes or is pure gauge on stationary compact local boundaries",
        "mathematical_form": "B_perp|partialD = 0 or int_partialD B_perp = 0",
        "status": "required_missing_Euler_condition",
    },
    {
        "assumption": "global_memory_class",
        "statement": "FLRW/coherent domains can carry a nonzero class/current not removable by local exact shifts",
        "mathematical_form": "int_DFLRW J_C_top != 0",
        "status": "conditional_survival_requirement",
    },
    {
        "assumption": "matter_couples_to_class",
        "statement": "matter depends on C only through the class observable C_D or P_D C, not through B_perp or scalar Cperp",
        "mathematical_form": "S_m[psi, exp(C_D) g] with delta_Cperp C_D = 0",
        "status": "selector_theorem_target",
    },
    {
        "assumption": "parent_owns_domain_projector",
        "statement": "D, P_D, and P_coh arise from parent variables and are varied before Ward/Bianchi identities are read",
        "mathematical_form": "delta S / delta D = 0 and delta S / delta P_D retained",
        "status": "open",
    },
]


DEGREE_AUDIT = [
    {
        "object": "scalar_Cperp",
        "degree": "0-form",
        "local_exactness_result": "failed",
        "reason": "H0 relative triviality is too narrow and exact gradients can still be physical",
    },
    {
        "object": "Jrel_memory_flux",
        "degree": "2-form/current-like",
        "local_exactness_result": "conditional_success",
        "reason": "on shell, H2_relative vanishes after mass/shear projectors",
    },
    {
        "object": "JC_domain_memory_current",
        "degree": "3-form on spatial domain",
        "local_exactness_result": "conditional_for_residual_variations_only",
        "reason": "delta JC=dB can be boundary-null, but H3_relative may carry orientation/domain class",
    },
    {
        "object": "BC_boundary_potential",
        "degree": "2-form primitive",
        "local_exactness_result": "key_missing_piece",
        "reason": "vanishing primitive must follow from boundary Euler/stationarity rather than being imposed",
    },
    {
        "object": "CD_class_observable",
        "degree": "domain integral / class scalar",
        "local_exactness_result": "invariant_if_delta_JC_boundary_null",
        "reason": "delta C_D = N_D^{-1} int_partialD B_perp",
    },
]


LOCAL_NULL_DERIVATION = [
    {
        "step": 1,
        "statement": "Replace scalar Cperp by a representative variation of a lifted current.",
        "equation": "delta J_C = d B_perp",
        "status": "conditional_start",
    },
    {
        "step": 2,
        "statement": "Define the observed/domain memory scalar as a class integral.",
        "equation": "C_D[D] = N_D^{-1} int_D J_C",
        "status": "definition",
    },
    {
        "step": 3,
        "statement": "Compute the response of the class scalar to a local residual shift.",
        "equation": "delta C_D = N_D^{-1} int_D dB_perp = N_D^{-1} int_partialD B_perp",
        "status": "derived_by_Stokes",
    },
    {
        "step": 4,
        "statement": "Apply the stationary local boundary primitive condition.",
        "equation": "int_partialD B_perp = 0",
        "status": "conditional_missing_parent_boundary_Euler",
    },
    {
        "step": 5,
        "statement": "Conclude that matter depending only on C_D does not see local Cperp representative shifts.",
        "equation": "delta_Cperp C_D = 0 and delta_Cperp S_m[psi, exp(C_D)g] = 0",
        "status": "conditional_theorem",
    },
]


FLRW_SURVIVAL = [
    {
        "piece": "coherent_Q_origin",
        "statement": "For fixed D, Q_coh is the isotropic domain projection P_coh[Q] = (1/3)<Tr Q>_D I",
        "source": "276-coherent-domain-projector-from-parent-variables.md",
        "status": "fixed_D_derived",
    },
    {
        "piece": "three_form_current",
        "statement": "J_C = det(P_coh Q) Omega_D / V_D gives int_D J_C = det(Q_coh)",
        "source": "275-JC-three-form-memory-current-from-Q.md",
        "status": "conditional_kinematic_origin",
    },
    {
        "piece": "FLRW_reduction",
        "statement": "FLRW has P_coh[Q]=Q=(N/u3)I, so int_D J_C=(N/u3)^3",
        "source": "275-JC-three-form-memory-current-from-Q.md",
        "status": "conditional_pass",
    },
    {
        "piece": "local_stationary_domain",
        "statement": "stationary local systems require <Tr Q>_D=0 or boundary-null variations, giving delta C_D=0",
        "source": "276-coherent-domain-projector-from-parent-variables.md",
        "status": "conditional_domain_selector_missing",
    },
    {
        "piece": "same_parent_requirement",
        "statement": "The same P_D/P_coh/J_C structure must produce local silence and FLRW memory",
        "source": "363-projected-metric-closure-ledger-and-lifted-C-route-contract.md",
        "status": "live_bridge_not_proved",
    },
]


MATTER_METRIC_IMPLICATIONS = [
    {
        "claim": "projected_metric_from_representative_invariance",
        "result": "conditional",
        "condition": "matter action depends only on C_D/P_D C and the lifted C kernel is boundary-null",
        "implication": "exp(P_D C)g can become theorem target, not yet theorem",
    },
    {
        "claim": "WEP_direct_Cperp_vertex_absent",
        "result": "conditional",
        "condition": "all matter species share the same class observable and no species sees B_perp",
        "implication": "WEP runner remains active until the selector theorem is parent-derived",
    },
    {
        "claim": "clock_common_mode_safe",
        "result": "not_proved",
        "condition": "P_D C gradients/drift must be derived zero or bounded",
        "implication": "clock/redshift residual remains explicit",
    },
    {
        "claim": "local_GR_promotion",
        "result": "fail",
        "condition": "needs EH exterior operator plus universal coupling plus residual-vector control",
        "implication": "no local GR claim",
    },
]


FAILURE_MODES = [
    {
        "failure": "boundary_primitive_imposed",
        "meaning": "if int_partialD B_perp=0 is assumed rather than varied, the route is closure",
        "repair": "derive a boundary Euler/natural boundary condition from the parent action",
    },
    {
        "failure": "domain_selector_imposed",
        "meaning": "if D/P_D/P_coh is chosen for convenience, conservation and local silence are not owned",
        "repair": "derive D and projector stress from parent variables",
    },
    {
        "failure": "matter_sees_representative",
        "meaning": "if matter couples to B_perp or scalar Cperp, fifth-force/WEP/clock risks return",
        "repair": "prove representative-shift invariance of the matter action",
    },
    {
        "failure": "three_form_added_by_hand",
        "meaning": "J_C becomes a repair field rather than MTS geometry",
        "repair": "derive J_C from Q/coframe/load with fixed-D projection and domain variation",
    },
    {
        "failure": "FLRW_class_killed",
        "meaning": "local quotient also erases cosmological memory",
        "repair": "separate local exact residuals from global/coherent domain class",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Stokes/local-boundary-null route conditionally derives Cperp representative invisibility, but parent boundary/domain/matter selector theorem is still missing",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive or reject the boundary primitive condition int_partialD B_perp=0 from a parent domain/boundary Euler equation",
        "pass_condition": "local residual exactness is a variational boundary result, not an imposed no-leak condition",
    },
    {
        "priority": 2,
        "target": "366-representative-invariant-matter-action-for-lifted-C.md",
        "task": "prove matter sees only C_D/P_D C and not B_perp or scalar representative data",
        "pass_condition": "universal observed metric selector follows from representative invariance",
    },
    {
        "priority": 3,
        "target": "367-EH-exterior-reduction-after-lifted-C-gate.md",
        "task": "reconnect the lifted C result to the metric-only Einstein-Hilbert exterior operator gate",
        "pass_condition": "local exterior operator is EH plus explicitly bounded residuals",
    },
    {
        "priority": 4,
        "target": "368-source-locked-local-residual-vector-after-lifted-C.md",
        "task": "rerun WEP/clock/PPN/fifth-force residual ledger after the selector attempt",
        "pass_condition": "each residual is theorem-zero or quantitatively bounded",
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
            "gate": "scalar_Cperp_exactness_rejected",
            "status": "pass",
            "evidence": "checkpoint 362 imported as binding; scalar route is not reused",
        },
        {
            "gate": "lifted_C_local_null_derivation",
            "status": "conditional_pass",
            "evidence": "delta C_D = int_D dB = int_boundary B, so boundary-null local shifts are invisible",
        },
        {
            "gate": "boundary_primitive_parent_derived",
            "status": "fail",
            "evidence": "int_boundary B_perp=0 is required but not yet derived from an Euler/natural boundary condition",
        },
        {
            "gate": "FLRW_memory_survives",
            "status": "conditional_pass",
            "evidence": "coherent Q route gives int_D J_C=(N/u3)^3 on FLRW if D/Pcoh is parent-owned",
        },
        {
            "gate": "domain_projector_parent_owned",
            "status": "fail",
            "evidence": "fixed-D Qcoh is derived, but the physical domain D/P_D is not",
        },
        {
            "gate": "matter_metric_parent_derived",
            "status": "fail",
            "evidence": "representative-invariant matter coupling is a theorem target, not proved",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "EH operator and residual-vector gates remain open",
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
    write_csv(results_dir / "theorem_assumptions.csv", THEOREM_ASSUMPTIONS)
    write_csv(results_dir / "degree_audit.csv", DEGREE_AUDIT)
    write_csv(results_dir / "local_null_derivation.csv", LOCAL_NULL_DERIVATION)
    write_csv(results_dir / "FLRW_survival.csv", FLRW_SURVIVAL)
    write_csv(results_dir / "matter_metric_implications.csv", MATTER_METRIC_IMPLICATIONS)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
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
        description="Write checkpoint 364 lifted C theorem-attempt artifacts."
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
