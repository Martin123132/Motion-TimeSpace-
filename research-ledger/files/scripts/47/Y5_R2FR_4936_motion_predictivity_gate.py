from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4936"
OUTPUT = OUTPUT_DIR / "motion_predictivity_gate_results.json"
ROUTE_OUTPUT = OUTPUT_DIR / "motion_predictivity_route_gate.csv"

CHECKPOINT_4935 = POST / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
MOTION_ENTRY = POST / "source-intake" / "functional_rg" / "4935" / "motion_sector_entry_results.json"
FRACTIONAL_FLOW = OUTPUT_DIR / "fractional_potential_LPA_closure_results.json"
SOURCE_FLOW = OUTPUT_DIR / "scalar_source_flow_evaluation_results.json"
O4_PROJECTION = OUTPUT_DIR / "O4_functional_trace_projection_results.json"

MARKER = "MTS_4936_MOTION_PREDICTIVITY_GATE"
EXPECTED_HASHES = {
    CHECKPOINT_4935: "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    MOTION_ENTRY: "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    FRACTIONAL_FLOW: "8af1d8bf764372917991126c86de63847714f1a48ca4f5eb0925d1b91a4fdf96",
    SOURCE_FLOW: "ab7394cf0ea455b40ec8678f5bb5cf34025657a51af499b5e92825b993dd6359",
    O4_PROJECTION: "06f6663105791669020729e21227db5007d696ea22d184081c9069d2d3d9bc99",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"motion predictivity source hash mismatch: {hash_failures}")

    fractional = json.loads(FRACTIONAL_FLOW.read_text(encoding="utf-8"))
    source_flow = json.loads(SOURCE_FLOW.read_text(encoding="utf-8"))
    o4 = json.loads(O4_PROJECTION.read_text(encoding="utf-8"))

    ratio_n, ratio_b, q_value, s_value = sp.symbols(
        "r_n r_b q s", positive=True
    )
    occupation_n = ratio_n / (1 + ratio_n)
    occupation_b = ratio_b / (1 + ratio_b)
    n_flow = sp.simplify(sp.diff(occupation_n, ratio_n) * q_value * ratio_n)
    b_flow = sp.simplify(sp.diff(occupation_b, ratio_b) * (-s_value * ratio_b))
    n_logistic = sp.simplify(q_value * occupation_n * (1 - occupation_n))
    b_logistic = sp.simplify(-s_value * occupation_b * (1 - occupation_b))

    radius, radius_n, radius_b = sp.symbols("R R_n R_b", positive=True)
    n_solution = sp.simplify(
        (radius / radius_n) ** q_value
        / (1 + (radius / radius_n) ** q_value)
    )
    b_solution = sp.simplify(
        (radius_b / radius) ** s_value
        / (1 + (radius_b / radius) ** s_value)
    )

    point_b = source_flow["fixed_points"]["B"]
    exponents_b = sorted(point_b["critical_exponents"])
    conditional_q = max(exponents_b)
    conditional_s = abs(min(exponents_b))

    route_rows = [
        {
            "route_id": "MP4936_R1_one_coupling_fractional",
            "route": "retain only g_tilde |varphi|^(4/3)",
            "mathematical_gate": "exact scalar trace must preserve span{1,|varphi|^(4/3)}",
            "result": "REJECTED",
            "reason": "the trace generates |varphi|^(2/3) with a nonzero coefficient and has no nonzero scalar-only one-coupling fixed point",
            "selected_next": False,
        },
        {
            "route_id": "MP4936_R2_exact_mixed_trace_cancellation",
            "route": "retain the fractional family by exact gravity-motion cancellation",
            "mathematical_gate": "the mixed trace satisfies every coefficient identity in the eta=4 cancellation contract",
            "result": "OPEN_BUT_UNSATISFIED",
            "reason": "the contract is exact, but the required six-derivative mixed trace has not produced those coefficients",
            "selected_next": False,
        },
        {
            "route_id": "MP4936_R3_composite_chi",
            "route": "set psi=chi^3 and treat the potential as quartic",
            "mathematical_gate": "the parent derives Z(psi)=1/[9|psi|^(4/3)] and a nonsingular measure map",
            "result": "INCOMPATIBLE_WITH_CURRENT_PARENT",
            "reason": "the current canonical psi kinetic term becomes 9chi^4(nabla chi)^2 and the map Jacobian vanishes at the vacuum",
            "selected_next": False,
        },
        {
            "route_id": "MP4936_R4_functional_motion_potential",
            "route": "solve u_k(varphi) with the full gravity-motion Hessian and O4 projection",
            "mathematical_gate": "a regular fixed functional, a finite relevant spectrum, and a GR-connected trajectory exist",
            "result": "SELECTED",
            "reason": "this is the only route that preserves the current parent action without discarding operators generated by its exact trace",
            "selected_next": True,
        },
        {
            "route_id": "MP4936_R5_phenomenological_closure",
            "route": "insert m_gap, O4, or occupation profiles as fitted closures",
            "mathematical_gate": "not applicable",
            "result": "DEMOTED",
            "reason": "it cannot establish the requested derivable GR-connected field theory",
            "selected_next": False,
        },
    ]
    for row in route_rows:
        row["valid_for_claim"] = False
        row["checkpoint_marker"] = MARKER

    checks = {
        "n_logistic_identity_exact": sp.simplify(n_flow - n_logistic) == 0,
        "b_logistic_identity_exact": sp.simplify(b_flow - b_logistic) == 0,
        "n_solution_has_correct_limits": sp.limit(n_solution, radius, 0) == 0
        and sp.limit(n_solution, radius, sp.oo) == 1,
        "b_solution_has_correct_limits": sp.limit(b_solution, radius, 0) == 1
        and sp.limit(b_solution, radius, sp.oo) == 0,
        "fractional_one_coupling_route_rejected": fractional["claim_boundary"][
            "fractional_one_coupling_LPA_closed"
        ]
        is False,
        "source_B_has_one_relevant_direction": point_b["relevant_directions"] == 1,
        "O4_numeric_coefficient_not_smuggled": o4["claim_boundary"][
            "numeric_O4_beta_coefficient_derived"
        ]
        is False,
        "exactly_one_route_selected": sum(
            row["selected_next"] for row in route_rows
        )
        == 1,
        "functional_route_selected": next(
            row for row in route_rows if row["selected_next"]
        )["route_id"]
        == "MP4936_R4_functional_motion_potential",
    }
    if not all(checks.values()):
        raise RuntimeError(f"motion predictivity checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "decision": {
            "selected_route": "full functional motion potential coupled to the gravity-motion block Hessian",
            "one_coupling_parent_realization": "rejected",
            "motion_sector_overall": "NOT_REJECTED; REQUIRES_FUNCTIONAL_COMPLETION",
            "predictivity_target": "one total relevant direction after scale setting, or an explicit derivation of every additional relevant datum",
            "next_checkpoint": "derive the constant-background gravity-motion Hessian and functional potential trace, then solve its fixed-functional/eigenoperator boundary-value problem",
        },
        "why_the_route_is_plausible_but_not_proved": {
            "executed_primary_source_precedent": "the reproduced scalar-gravity fixed point B has one relevant and one irrelevant direction and connects to a Gaussian infrared regime in its source theory",
            "source_B_critical_exponents": exponents_b,
            "boundary": "that source is shift-symmetric and four-derivative; its numbers are not MTS coefficients",
        },
        "galaxy_phase_flow_interface": {
            "status": "EXACT_KINEMATIC_MAP_DERIVED_PHYSICAL_OWNERSHIP_PENDING",
            "occupation_definition": "n=r_n/(1+r_n), b=r_b/(1+r_b), with positive amplitude ratios",
            "multiplicative_parent_flow": "d ln r_n/d ln R=q and d ln r_b/d ln R=-s",
            "derived_bounded_flow": "dn/d ln R=q n(1-n); db/d ln R=-s b(1-b)",
            "solutions": {
                "n": "1/[1+(R_n/R)^q]",
                "b": "1/[1+(R/R_b)^s]",
            },
            "RG_eigenvalue_map": "if k is proportional to 1/R and delta a scales as k^lambda, then q=-lambda=theta for a growing occupation; a decaying boundary occupation has s=lambda=-theta",
            "conditional_source_B_example_not_MTS_prediction": {
                "q": conditional_q,
                "s": conditional_s,
            },
            "ownership_requirements": [
                "identify r_n and r_b as positive ratios of parent Hessian eigenamplitudes or spectral weights",
                "derive rather than assume k proportional to 1/R in the galactic background",
                "derive q and s from the coupled MTS functional stability spectrum",
                "vary the resulting effective action to obtain the activation stress tensor and lensing source",
            ],
        },
        "route_rows": route_rows,
        "checks": checks,
        "claim_boundary": {
            "motion_sector_rejected": False,
            "one_coupling_fractional_realization_rejected": True,
            "functional_completion_selected": True,
            "MTS_motion_fixed_function_derived": False,
            "galaxy_logistic_shape_kinematically_derived": True,
            "galaxy_logistic_parent_amplitudes_identified": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(ROUTE_OUTPUT, route_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_ROUTES_SHA256={digest(ROUTE_OUTPUT)}", flush=True)
    print(f"{MARKER}_CONDITIONAL_Q={conditional_q}", flush=True)
    print(f"{MARKER}_CONDITIONAL_S={conditional_s}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
