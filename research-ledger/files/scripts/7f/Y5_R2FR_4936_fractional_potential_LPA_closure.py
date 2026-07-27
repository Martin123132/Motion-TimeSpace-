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
OUTPUT = OUTPUT_DIR / "fractional_potential_LPA_closure_results.json"
SERIES_OUTPUT = OUTPUT_DIR / "fractional_potential_generated_operator_series.csv"

PARENT_ACTION = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
MOTION_ENTRY = OUTPUT_DIR.parent / "4935" / "motion_sector_entry_results.json"

MARKER = "MTS_4936_FRACTIONAL_POTENTIAL_LPA_CLOSURE"
EXPECTED_HASHES = {
    PARENT_ACTION: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    MOTION_ENTRY: "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("refusing to write an empty generated-operator series")
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
        raise RuntimeError(f"fractional-flow source hash mismatch: {hash_failures}")

    varphi = sp.symbols("varphi", positive=True)
    q = sp.symbols("q", positive=True)
    g_tilde = sp.symbols("g_tilde", positive=True)
    eta = sp.symbols("eta_psi", real=True)
    chi = sp.symbols("chi", positive=True)
    exponent = sp.Rational(4, 3)
    field_dimension = 1 + eta / 2
    potential = sp.Rational(3, 4) * g_tilde * varphi**exponent
    hessian = sp.simplify(sp.diff(potential, varphi, 2))

    litim_coefficient = (1 - eta / 6) / (32 * sp.pi**2)
    canonical_flow = sp.simplify(-4 * potential + field_dimension * varphi * sp.diff(potential, varphi))
    scalar_trace = sp.simplify(litim_coefficient / (1 + hessian))
    flow_in_q = sp.factor(
        (canonical_flow + scalar_trace).subs(varphi ** sp.Rational(2, 3), q)
    )
    expected_flow_in_q = (
        g_tilde * (eta - 4) * q**2 / 2
        + 3 * litim_coefficient * q / (g_tilde + 3 * q)
    )

    generated_rows: list[dict[str, Any]] = []
    generated_coefficients: dict[int, sp.Expr] = {}
    for order in range(1, 7):
        coefficient = sp.simplify(
            3 * litim_coefficient * (-3) ** (order - 1) / g_tilde**order
        )
        generated_coefficients[order] = coefficient
        generated_rows.append(
            {
                "q_power": order,
                "varphi_power": str(sp.Rational(2 * order, 3)),
                "operator": f"|varphi|^({2 * order}/3)",
                "scalar_trace_coefficient": str(coefficient),
                "inside_original_one_coupling_span": order == 2,
                "status": "RUNNING_COUPLING_CHANNEL" if order == 2 else "GENERATED_OUTSIDE_TRUNCATION",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    leading_generated = generated_coefficients[1]
    allowed_q2_scalar = generated_coefficients[2]
    projected_beta_g = sp.simplify(
        sp.Rational(4, 3)
        * (g_tilde * (eta - 4) / 2 + allowed_q2_scalar)
    )
    eta_for_canonical_marginality = sp.solve(
        sp.Eq(-4 + exponent * field_dimension, 0), eta
    )
    eta_for_scalar_trace_silence = sp.solve(sp.Eq(litim_coefficient, 0), eta)
    scalar_only_fixed_point_compatible = bool(
        set(eta_for_canonical_marginality) & set(eta_for_scalar_trace_silence)
    )

    eta_marginal = sp.Integer(4)
    cancellation_contract = {
        f"q^{order}": str(
            sp.simplify(-generated_coefficients[order].subs(eta, eta_marginal))
        )
        for order in range(1, 7)
        if order != 2
    }
    cancellation_contract["q^2_at_fixed_point"] = str(
        sp.simplify(
            -(
                g_tilde * (eta - 4) / 2 + generated_coefficients[2]
            ).subs(eta, eta_marginal)
        )
    )

    psi_of_chi = chi**3
    transformed_kinetic_factor = sp.simplify(sp.diff(psi_of_chi, chi) ** 2)
    transformed_potential = sp.simplify(
        sp.Rational(3, 4) * g_tilde * psi_of_chi**exponent
    )
    required_parent_metric = sp.simplify(
        1 / transformed_kinetic_factor
    ).subs(chi, varphi ** sp.Rational(1, 3))
    coupling_mass_dimension = sp.simplify(4 - exponent * field_dimension)

    checks = {
        "parent_Hessian_reproduced": hessian
        == g_tilde / (3 * varphi ** sp.Rational(2, 3)),
        "exact_q_flow_reproduced": sp.simplify(flow_in_q - expected_flow_in_q) == 0,
        "eta_zero_leading_generated_term": sp.simplify(
            leading_generated.subs(eta, 0) - 3 / (32 * sp.pi**2 * g_tilde)
        )
        == 0,
        "eta_zero_original_power_coefficient": sp.simplify(
            allowed_q2_scalar.subs(eta, 0)
            + 9 / (32 * sp.pi**2 * g_tilde**2)
        )
        == 0,
        "fractional_family_not_closed": generated_rows[0]["inside_original_one_coupling_span"]
        is False,
        "canonical_marginality_requires_eta_four": eta_for_canonical_marginality
        == [4],
        "scalar_trace_silence_requires_eta_six": eta_for_scalar_trace_silence
        == [6],
        "no_scalar_only_one_coupling_fixed_point": not scalar_only_fixed_point_compatible,
        "eta_four_trace_still_generates_q": sp.simplify(
            leading_generated.subs(eta, 4) - 1 / (32 * sp.pi**2 * g_tilde)
        )
        == 0,
        "composite_map_makes_potential_quartic": transformed_potential
        == sp.Rational(3, 4) * g_tilde * chi**4,
        "composite_map_makes_kinetic_degenerate": transformed_kinetic_factor
        == 9 * chi**4,
        "canonical_chi_requires_singular_parent_metric": required_parent_metric
        == 1 / (9 * varphi ** sp.Rational(4, 3)),
        "eta_zero_coupling_dimension_is_8_over_3": coupling_mass_dimension.subs(eta, 0)
        == sp.Rational(8, 3),
        "eta_four_coupling_is_dimensionless": coupling_mass_dimension.subs(eta, 4)
        == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"fractional-flow closure checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "derivation": {
            "dimensionless_potential": "u(varphi)=(3/4) g_tilde |varphi|^(4/3)",
            "dimensionless_field": "varphi=Z_psi^(1/2) k^(-(d-2)/2) psi in d=4",
            "LPA_prime_flow": "partial_t u=-4u+(1+eta_psi/2)varphi u'+[(1-eta_psi/6)/(32pi^2)]/(1+u'')",
            "Hessian": str(hessian),
            "q_definition": "q=|varphi|^(2/3)",
            "exact_flow_in_q": str(expected_flow_in_q),
            "eta_zero_exact_flow": str(sp.simplify(expected_flow_in_q.subs(eta, 0))),
            "eta_zero_small_q_series": "-2 g_tilde q^2 + 3q/(32pi^2 g_tilde) - 9q^2/(32pi^2 g_tilde^2) + 27q^3/(32pi^2 g_tilde^3) - ...",
        },
        "closure_theorem": {
            "result": "REJECTED_FOR_THE_ONE_COUPLING_FRACTIONAL_FAMILY",
            "reason": "the exact scalar trace has a nonzero |varphi|^(2/3) term, which is outside span{1,|varphi|^(4/3)} and dominates the retained interaction as varphi approaches zero",
            "general_small_field_rule": "for u~A|varphi|^p with 1<p<2, the optimized scalar trace begins as |varphi|^(2-p); equality with p occurs only at p=1, not p=4/3",
            "leading_generated_coefficient": str(leading_generated),
            "formal_one_coupling_projection_beta": str(projected_beta_g),
            "projection_warning": "the displayed beta_g is not a consistent truncation because the omitted q term is lower order than q^2",
        },
        "fixed_point_test": {
            "eta_for_classical_fractional_marginality": [
                int(value) for value in eta_for_canonical_marginality
            ],
            "eta_for_optimized_scalar_trace_silence": [
                int(value) for value in eta_for_scalar_trace_silence
            ],
            "common_eta": [],
            "nonzero_scalar_only_one_coupling_fixed_point": False,
            "eta_four_leading_q_coefficient": str(leading_generated.subs(eta, 4)),
            "eta_four_projected_beta_g": str(projected_beta_g.subs(eta, 4)),
        },
        "exact_mixed_trace_cancellation_contract_at_eta_four": {
            "required_rest_trace_coefficients": cancellation_contract,
            "interpretation": "an exact gravity/mixed trace must cancel every q^n channel outside q^2; at a fixed point it must also cancel the displayed q^2 coefficient",
            "status": "DERIVED_CONTRACT_NOT_YET_SATISFIED",
        },
        "composite_coordinate_test": {
            "map": "psi=chi^3",
            "potential": "V=(3/4)g_psi chi^4",
            "kinetic": "(1/2)(nabla psi)^2=(9/2)chi^4(nabla chi)^2",
            "required_parent_field_metric": "Z(psi)=1/[9|psi|^(4/3)] for a canonical chi kinetic term",
            "Jacobian": "dpsi/dchi=3chi^2 vanishes at chi=0",
            "result": "QUARTIC_POTENTIAL_RECOVERED_BUT_CURRENT_PARENT_KINETIC_NOT_EQUIVALENT",
        },
        "scale_consequence": {
            "coupling_mass_dimension": str(coupling_mass_dimension),
            "eta_zero": "[g_psi]=8/3 and dimensional analysis gives m_gap proportional to g_psi^(3/8)",
            "eta_four": "[g_psi]=0, so g_psi alone cannot generate a dimensionful mass gap at a scale-invariant fixed point",
            "conclusion": "the coefficient c_m remains a nonperturbative trajectory observable; it is not derivable from one-coupling dimensional analysis alone",
        },
        "next_routes": [
            "solve a full functional potential u_k(varphi) and count its relevant eigenperturbations",
            "derive the gravity-motion mixed trace and test the exact cancellation contract",
            "derive a parent field-space metric and measure that make chi fundamental rather than silently changing coordinates",
        ],
        "checks": checks,
        "claim_boundary": {
            "fractional_one_coupling_LPA_closed": False,
            "scalar_only_fractional_fixed_point_derived": False,
            "exact_escape_routes_derived": True,
            "mass_gap_coefficient_derived": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(SERIES_OUTPUT, generated_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_SERIES_SHA256={digest(SERIES_OUTPUT)}", flush=True)
    print(f"{MARKER}_LEADING_GENERATED={leading_generated}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
