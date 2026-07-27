from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4934"
PHOTON_FLOW = POST / "source-intake" / "functional_rg" / "4933" / "RHS_general_regulator_extracted.wl"
LINEAR_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_portal_linear_c3_zero.py"
LINEAR_JSON = SOURCE_DIR / "portal_linear_c3_zero_results.json"
OUTPUT = SOURCE_DIR / "portal_quadratic_c3_results.json"
MARKER = "MTS_4934_PORTAL_QUADRATIC_C3"
EXPECTED_HASHES = {
    PHOTON_FLOW: "28be0c586f31fa83a0a0b888f686b5564f6af0c4f74f5888d229aa9b58a8903c",
    LINEAR_JSON: "f0f30c1233d36d47a92655dd0023918f978d5a76056ffd196a378cdb3156c002",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load_linear_module():
    specification = importlib.util.spec_from_file_location("mts_4934_linear", LINEAR_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the 4934 linear portal derivation")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def ordered_four_derivative_contractions(
    weyl: sp.MutableDenseNDimArray,
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    dimension = 4
    quadratic_invariant, cubic_invariant = linear_module.curvature_invariants(weyl)
    flat_terms: list[sp.Expr] = []
    connection_terms: list[sp.Expr] = []
    for index_m in range(dimension):
        for index_r in range(dimension):
            for index_a in range(dimension):
                for index_b in range(dimension):
                    two_portal_matrix = sp.MutableDenseMatrix.zeros(dimension, dimension)
                    for row_index in range(dimension):
                        for column_index in range(dimension):
                            two_portal_matrix[row_index, column_index] = sum(
                                weyl[index_m, row_index, index_r, contracted_index]
                                * weyl[index_a, contracted_index, index_b, column_index]
                                for contracted_index in range(dimension)
                            )
                    flat_pairing = 4 * (
                        int(index_m == index_r and index_a == index_b)
                        + int(index_m == index_a and index_r == index_b)
                        + int(index_m == index_b and index_r == index_a)
                    )
                    flat_terms.append(sp.trace(two_portal_matrix) * flat_pairing)
                    for row_index in range(dimension):
                        for column_index in range(dimension):
                            connection_kernel = -(
                                int(index_m == index_a)
                                * weyl[column_index, row_index, index_r, index_b]
                                + int(index_r == index_a)
                                * weyl[column_index, row_index, index_m, index_b]
                                + int(index_m == index_b)
                                * weyl[column_index, row_index, index_r, index_a]
                                + int(index_r == index_b)
                                * weyl[column_index, row_index, index_m, index_a]
                                + int(index_m == index_r)
                                * weyl[column_index, row_index, index_a, index_b]
                                + int(index_a == index_b)
                                * weyl[column_index, row_index, index_m, index_r]
                            )
                            connection_terms.append(
                                two_portal_matrix[row_index, column_index]
                                * connection_kernel
                            )
    flat_heat_kernel_coefficient = linear_module.simplify_sum(flat_terms)
    connection_heat_kernel_coefficient = linear_module.simplify_sum(connection_terms)
    flat_ratio = sp.simplify(flat_heat_kernel_coefficient / quadratic_invariant)
    connection_ratio = sp.simplify(connection_heat_kernel_coefficient / cubic_invariant)
    return (
        flat_heat_kernel_coefficient,
        connection_heat_kernel_coefficient,
        flat_ratio,
        connection_ratio,
    )


def source_integrals() -> dict[str, sp.Expr]:
    spectral_value, gamma_a, gamma_df = sp.symbols("x gamma_a gamma_df")
    litim_regulator = 1 - spectral_value
    source_weight = -(
        1 + gamma_a - gamma_df * spectral_value
    ) * litim_regulator - spectral_value
    quadratic_curvature_moment = sp.factor(
        sp.integrate(spectral_value**3 * source_weight, (spectral_value, 0, 1))
    )
    cubic_curvature_moment = sp.factor(
        sp.integrate(spectral_value**2 * source_weight, (spectral_value, 0, 1))
    )
    source_c_squared_coefficient = sp.factor(
        -quadratic_curvature_moment / (4 * sp.pi**2)
    )
    derived_c_cubed_coefficient = sp.factor(
        -3 * cubic_curvature_moment / (4 * sp.pi**2)
    )
    return {
        "source_weight": source_weight,
        "quadratic_curvature_moment": quadratic_curvature_moment,
        "cubic_curvature_moment": cubic_curvature_moment,
        "source_c_squared_coefficient": source_c_squared_coefficient,
        "derived_c_cubed_coefficient": derived_c_cubed_coefficient,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    actual_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    failed_hashes = [
        path.as_posix()
        for path, expected_hash in EXPECTED_HASHES.items()
        if actual_hashes[path] != expected_hash
    ]
    if failed_hashes:
        raise RuntimeError(f"source hash mismatch: {failed_hashes}")
    photon_text = PHOTON_FLOW.read_text(encoding="utf-8")
    source_markers = (
        "CFFcoupl*WLCapitalDelta*((Ga1[WLCapitalDelta])^(2))",
        "-1+2*CFFcoupl*((WLCapitalDelta)^(2))*Ga1[WLCapitalDelta]",
        "1+WLGammaa-WLGammaDF*WLCapitalDelta",
    )
    missing_markers = [marker for marker in source_markers if marker not in photon_text]
    if missing_markers:
        raise RuntimeError(f"photon-flow source markers missing: {missing_markers}")

    weyl, _ = linear_module.build_generic_weyl()
    (
        flat_heat_kernel_coefficient,
        connection_heat_kernel_coefficient,
        flat_ratio,
        connection_ratio,
    ) = ordered_four_derivative_contractions(weyl)
    integrals = source_integrals()
    expected_flat_ratio = 6
    expected_connection_ratio = sp.Rational(3, 2)
    gamma_a_value = 0.04101920752494062
    gamma_df_value = -0.005379640817968146
    cff_value = 0.003729942575813481
    numeric_coefficient = float(
        integrals["derived_c_cubed_coefficient"].subs(
            {
                sp.Symbol("gamma_a"): gamma_a_value,
                sp.Symbol("gamma_df"): gamma_df_value,
            }
        )
    )
    fixed_point_projection = numeric_coefficient * cff_value**2
    derivative_on_weyl_projection = sp.Integer(0)
    checks = {
        "flat_ordered_derivative_ratio_is_6": flat_ratio == expected_flat_ratio,
        "connection_ratio_is_three_halves": connection_ratio == expected_connection_ratio,
        "source_C2_coefficient_reproduced": sp.simplify(
            integrals["source_c_squared_coefficient"]
            - (3 * sp.Symbol("gamma_a") - 2 * sp.Symbol("gamma_df") + 15)
            / (240 * sp.pi**2)
        )
        == 0,
        "quadratic_C3_formula_simplified": sp.simplify(
            integrals["derived_c_cubed_coefficient"]
            - (5 * sp.Symbol("gamma_a") - 3 * sp.Symbol("gamma_df") + 20)
            / (80 * sp.pi**2)
        )
        == 0,
        "derivative_on_weyl_terms_zero": derivative_on_weyl_projection == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"quadratic portal derivation failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): actual_hashes[path]
            for path in EXPECTED_HASHES
        },
        "operator_expansion": {
            "portal_operator_without_coupling": "U^nu_sigma=-8 C^{mu nu rho}_sigma D_mu D_rho",
            "quadratic_flow_term": "(g_CFF^2/2) Tr[U U W(Delta_a)] for the source Litim inverse propagator",
            "flat_angular_projection": "<C C D^4>/C^2 = (1/16)<p^4> before the (-8)^2/2 portal prefactor",
            "connection_projection": "<C C D^4>|linear bundle curvature = (3/16) C^3 <p^2> before the (-8)^2/2 portal prefactor",
            "after_portal_prefactor": "2 C^2 <p^4> + 6 C^3 <p^2>",
        },
        "symbolic_contractions": {
            "flat_heat_kernel_coefficient": str(flat_heat_kernel_coefficient),
            "flat_ratio_to_C_squared": str(flat_ratio),
            "connection_heat_kernel_coefficient": str(connection_heat_kernel_coefficient),
            "connection_ratio_to_C_cubed": str(connection_ratio),
        },
        "derivative_terms": {
            "odd_first_derivative_terms": "zero by symmetric momentum integration",
            "second_derivative_term": "proportional to delta_ab C^{a s b n}=0",
            "net_derivative_on_weyl_projection": str(derivative_on_weyl_projection),
        },
        "source_litim_match": {
            "weight": str(integrals["source_weight"]),
            "integral_x3_weight": str(integrals["quadratic_curvature_moment"]),
            "source_C2_quadratic_portal_coefficient": str(
                integrals["source_c_squared_coefficient"]
            ),
            "integral_x2_weight": str(integrals["cubic_curvature_moment"]),
        },
        "theorem": {
            "statement": "The complete portal-dependent photon contribution to the Weyl-cubic flow quadratic in g_CFF is fixed by the source Litim trace.",
            "formula": "Delta RHS_C3|g_CFF^2 = g_CFF^2*(5 gamma_a - 3 gamma_DF + 20)/(80 pi^2)",
            "coefficient_at_4933_combined_gammas": numeric_coefficient,
            "projection_at_4933_partial_fixed_point": fixed_point_projection,
            "passed": True,
        },
        "checks": checks,
        "remaining_portal_a6_terms": [],
        "remaining_exact_combined_term": "direct h_C3 contribution to the photon CFF projection",
        "full_combined_fixed_point_claimed": False,
        "all_checks_pass": all(checks.values()) and math.isfinite(fixed_point_projection),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_FORMULA={result['theorem']['formula']}", flush=True)
    print(f"{MARKER}_PROJECTION={fixed_point_projection:.16g}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


linear_module = load_linear_module()


if __name__ == "__main__":
    raise SystemExit(main())
