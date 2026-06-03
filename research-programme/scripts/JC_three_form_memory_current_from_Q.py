from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "JC-three-form-memory-current-from-Q"
STATUS = "JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure"
CLAIM_CEILING = "shape_origin_strengthened_no_local_GR_or_unification_promotion"

U3_LEAD = 0.25
U3_C2_CLOSURE = 0.2429466120286312
B_MEM = 2.0 / 27.0


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
        (ROOT / "51-FLRW-memory-current-contract.md", "det(Q) memory exposure contract"),
        (ROOT / "52-load-tensor-origin-attempt.md", "Q as accumulated expansion/load tensor"),
        (ROOT / "60-relative-cohomology-boundary-contract.md", "local-zero / FLRW-nonzero relative class contract"),
        (ROOT / "142-domain-load-tensor-owner-promotion-gate.md", "coherent domain/load owner gate"),
        (ROOT / "274-lifted-C-sector-form-holonomy-route.md", "lifted 3-form route selection"),
        (ROOT / "scripts" / "JC_three_form_memory_current_from_Q.py", "this J_C ownership gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def construction_rows() -> list[dict[str, Any]]:
    return [
        {
            "construction": "unprojected_det_Q_three_form",
            "definition": "J_C = det(Q) Omega_D / V_D using full accumulated Q^i_j",
            "FLRW": "passes: Q=(N/u3)I gives det(Q)=(N/u3)^3",
            "local_silence": "fails_open: tracefree shear leaks at second order through det(XI+S)",
            "status": "rejected_as_lead",
        },
        {
            "construction": "coherent_trace_projected_det_Q_three_form",
            "definition": "Q_coh=(N_D/u3)I, J_C=det(Q_coh) Omega_D/V_D",
            "FLRW": "passes: N_D=N",
            "local_silence": "passes_if_domain_stationary_and_projection_parent_owned",
            "status": "best_conditional_route",
        },
        {
            "construction": "volume_holonomy_three_form",
            "definition": "N_D=(1/3)ln(V_D0/V_D), J_C=(N_D/u3)^3 Omega_D/V_D",
            "FLRW": "passes: V_D proportional a^3, so N_D=ln(a0/a)",
            "local_silence": "passes_if_bound_volume_stable",
            "status": "same_best_route_written_without_free_Q",
        },
        {
            "construction": "boundary_potential_route",
            "definition": "J_C=dB_C+J_C_top with integral_boundary B_C=0 locally",
            "FLRW": "passes_if_J_C_top_is_volume_expansion_class",
            "local_silence": "passes_if_boundary_primitive_theorem_derived",
            "status": "needed_for_exactness_theorem",
        },
    ]


def determinant_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "isotropic_FLRW",
            "Q": "X I",
            "determinant": "X^3",
            "implication": "p=3 follows from spatial dimension",
            "verdict": "pass",
        },
        {
            "case": "isotropic_plus_trace_perturbation",
            "Q": "(X+s) I",
            "determinant": "X^3 + 3X^2 s + 3X s^2 + s^3",
            "implication": "trace channel activates memory",
            "verdict": "controlled_if_trace_is_domain_coherent",
        },
        {
            "case": "tracefree_shear",
            "Q": "X I + S, Tr(S)=0",
            "determinant": "X^3 - (X/2)Tr(S^2) + det(S)",
            "implication": "unprojected det(Q) is not locally silent",
            "verdict": "fail_for_unprojected_Q",
        },
        {
            "case": "stationary_bound_domain",
            "Q": "Q_coh=0 by volume stability",
            "determinant": "0",
            "implication": "local memory off if D and projection are owned",
            "verdict": "conditional_pass",
        },
    ]


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "D1_spatial_volume",
            "statement": "Choose a physical domain D with volume form Omega_D and volume V_D=integral_D Omega_D",
            "status": "domain_not_parent_derived",
        },
        {
            "step": "D2_volume_log_load",
            "statement": "N_D=(1/3)ln(V_D0/V_D) follows from volume expansion theta_D=d ln V_D/dtau",
            "status": "kinematic",
        },
        {
            "step": "D3_coherent_Q",
            "statement": "Q_coh^i_j=(N_D/u3)delta^i_j is the isotropic coherent-volume part of accumulated load",
            "status": "conditional_on_projection_and_u3",
        },
        {
            "step": "D4_three_form",
            "statement": "J_C=det(Q_coh) Omega_D/V_D = (N_D/u3)^3 Omega_D/V_D",
            "status": "conditional_kinematic_definition",
        },
        {
            "step": "D5_class_scalar",
            "statement": "Integral_D J_C=(N_D/u3)^3 gives the scalar class observable",
            "status": "derived_within_conditional_branch",
        },
        {
            "step": "D6_activation",
            "statement": "F_D=1-exp[-Integral_D J_C] has F_D(0)=F_D'(0)=F_D''(0)=0",
            "status": "shape_derived_once_u3_given",
        },
        {
            "step": "D7_matter_metric",
            "statement": "bar_g=exp(B_mem F_D)g would depend only on domain class",
            "status": "matter_coupling_not_parent_derived",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "J_C_independent_new_field_avoided",
            "result": "yes_conditional",
            "evidence": "J_C can be written as normalized domain volume/load 3-form from Q_coh",
            "claim_effect": "shape origin strengthened",
        },
        {
            "gate": "p_equals_3_derived",
            "result": "yes_conditional",
            "evidence": "determinant/volume form on 3D spatial domain",
            "claim_effect": "cubic exponent no longer arbitrary inside branch",
        },
        {
            "gate": "u3_derived",
            "result": "no",
            "evidence": "u3 is still either lead closure 1/4 or C2 empirical closure",
            "claim_effect": "scale remains theorem target",
        },
        {
            "gate": "Bmem_derived",
            "result": "no",
            "evidence": "2/27 is carried as closure/theorem target",
            "claim_effect": "amplitude not promoted",
        },
        {
            "gate": "local_tracefree_shear_silent",
            "result": "not_for_unprojected_Q",
            "evidence": "det(XI+S)=X^3-(X/2)Tr(S^2)+det(S) for Tr(S)=0",
            "claim_effect": "must use parent-owned coherent projection or no promotion",
        },
        {
            "gate": "stationary_local_domain_silent",
            "result": "yes_if_domain_owned",
            "evidence": "stable volume gives N_D=0 and J_C=0",
            "claim_effect": "conditional local silence survives",
        },
        {
            "gate": "exactness_delta_J_equals_dB",
            "result": "not_derived",
            "evidence": "boundary primitive theorem still missing",
            "claim_effect": "274 exactness target remains open",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "domain selector, projection, u3, Bmem, and matter coupling remain underived",
            "claim_effect": "no local-GR/unification promotion",
        },
    ]


def numeric_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, u3 in [("lead_u3_one_quarter", U3_LEAD), ("C2_empirical_u3", U3_C2_CLOSURE)]:
        rows.extend(
            [
                {
                    "branch": label,
                    "quantity": "u3",
                    "value": u3,
                    "meaning": "transition/load scale used in J_C=(N_D/u3)^3",
                },
                {
                    "branch": label,
                    "quantity": "J_C_small_N_coefficient",
                    "value": 1.0 / (u3**3),
                    "meaning": "Integral_D J_C = coefficient * N_D^3",
                },
                {
                    "branch": label,
                    "quantity": "J_M_small_N_quadratic_coefficient",
                    "value": 3.0 / (u3**3),
                    "meaning": "d(Integral_D J_C)/dN_D = coefficient * N_D^2",
                },
                {
                    "branch": label,
                    "quantity": "F_third_derivative_at_zero",
                    "value": 6.0 / (u3**3),
                    "meaning": "activation F=1-exp[-(N_D/u3)^3] has a triple-zero",
                },
            ]
        )
    rows.append(
        {
            "branch": "fixed_amplitude",
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "amplitude remains closure/theorem target",
        }
    )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "J_C does not have to be an independent repair field: it can be conditionally written as a normalized coherent-domain volume/load 3-form built from Q_coh or directly from N_D. "
                "This derives the cubic shape and local stationary silence within the branch, but only if the domain selector and coherent projection are parent-owned. "
                "Unprojected det(Q) fails local tracefree-shear silence at second order, and u3, Bmem, matter coupling, and exact boundary primitive remain underived."
            ),
            "next_target": "derive_domain_selector_and_coherent_projection_or_demote_JC_to_effective_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "construction_candidates.csv": (
            construction_rows(),
            ["construction", "definition", "FLRW", "local_silence", "status"],
        ),
        "determinant_audit.csv": (
            determinant_audit_rows(),
            ["case", "Q", "determinant", "implication", "verdict"],
        ),
        "derivation_chain.csv": (derivation_chain_rows(), ["step", "statement", "status"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "numeric_locks.csv": (numeric_rows(), ["branch", "quantity", "value", "meaning"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "JC_independent_field_avoided": True,
        "JC_origin": "conditional_coherent_domain_volume_load_three_form",
        "p_equals_3_status": "conditional_shape_derived_from_3D_determinant",
        "unprojected_detQ_local_silence": False,
        "coherent_projection_parent_derived": False,
        "domain_selector_parent_derived": False,
        "u3_parent_derived": False,
        "Bmem_parent_derived": False,
        "matter_metric_parent_derived": False,
        "support_claim_allowed": False,
        "next_target": "derive_domain_selector_and_coherent_projection_or_demote_JC_to_effective_closure",
        "numeric": {
            "u3_lead": U3_LEAD,
            "u3_C2_closure": U3_C2_CLOSURE,
            "B_mem": B_MEM,
            "F_third_derivative_u3_lead": 6.0 / (U3_LEAD**3),
            "F_third_derivative_u3_C2": 6.0 / (U3_C2_CLOSURE**3),
        },
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="J_C three-form memory-current ownership gate from Q/coframe load.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
