from __future__ import annotations

import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4934"
VAN_DE_VEN_ARCHIVE = SOURCE_DIR / "hep-th-9708152-source.gz"
VAN_DE_VEN_TEX = SOURCE_DIR / "vandeven9708152" / "ncnotes12.tex"
C3_TEX = POST / "source-intake" / "functional_rg" / "4929" / "src2312" / "ess_cubic.tex"
PHOTON_TEX = POST / "source-intake" / "functional_rg" / "4932" / "src-2405.08860" / "WGCqg.tex"
OUTPUT = SOURCE_DIR / "portal_linear_c3_zero_results.json"
MARKER = "MTS_4934_PORTAL_LINEAR_C3_ZERO"
EXPECTED_HASHES = {
    VAN_DE_VEN_ARCHIVE: "a6e7967d52207ebe3f7a8795b7fa052ecddf82ef942eb098995f8b62b2f38c94",
    VAN_DE_VEN_TEX: "b75bbee3d477afcd8bb3f916de6daa8ba78bf1853d79042ba7685c30d123f7d8",
    C3_TEX: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
    PHOTON_TEX: "a849214a16c2bc68651912db1e0622ebb04f6041662d401a57e8578825beafd2",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def build_two_form_basis(dimension: int) -> list[sp.MutableDenseNDimArray]:
    basis: list[sp.MutableDenseNDimArray] = []
    for first_index, second_index in combinations(range(dimension), 2):
        element = sp.MutableDenseNDimArray.zeros(dimension, dimension)
        element[first_index, second_index] = 1
        element[second_index, first_index] = -1
        basis.append(element)
    return basis


def build_generic_weyl() -> tuple[sp.MutableDenseNDimArray, dict[str, sp.Symbol]]:
    dimension = 4
    basis = build_two_form_basis(dimension)
    hodge = sp.zeros(6)
    for column_index in range(6):
        for row_index in range(6):
            hodge[row_index, column_index] = sp.Rational(1, 4) * sum(
                basis[row_index][index_a, index_b]
                * sp.LeviCivita(index_a, index_b, index_c, index_d)
                * basis[column_index][index_c, index_d]
                for index_a in range(dimension)
                for index_b in range(dimension)
                for index_c in range(dimension)
                for index_d in range(dimension)
            )
    self_dual = (hodge - sp.eye(6)).nullspace()
    anti_self_dual = (hodge + sp.eye(6)).nullspace()
    chiral_basis = sp.Matrix.hstack(
        *[
            vector / sp.sqrt((vector.T * vector)[0])
            for vector in self_dual + anti_self_dual
        ]
    )
    plus_first, plus_second, minus_first, minus_second = sp.symbols(
        "plus_first plus_second minus_first minus_second"
    )
    eigenvalues = (
        plus_first,
        plus_second,
        -plus_first - plus_second,
        minus_first,
        minus_second,
        -minus_first - minus_second,
    )
    curvature_operator = sp.simplify(chiral_basis * sp.diag(*eigenvalues) * chiral_basis.T)
    weyl = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    weyl[index_a, index_b, index_c, index_d] = sp.expand(
                        sum(
                            basis[row_index][index_a, index_b]
                            * curvature_operator[row_index, column_index]
                            * basis[column_index][index_c, index_d]
                            for row_index in range(6)
                            for column_index in range(6)
                        )
                    )
    symbols = {
        "plus_first": plus_first,
        "plus_second": plus_second,
        "minus_first": minus_first,
        "minus_second": minus_second,
    }
    return weyl, symbols


def simplify_sum(terms: list[sp.Expr]) -> sp.Expr:
    return sp.factor(sp.expand(sum(terms, sp.Integer(0))))


def curvature_invariants(weyl: sp.MutableDenseNDimArray) -> tuple[sp.Expr, sp.Expr]:
    dimension = 4
    quadratic = simplify_sum(
        [
            weyl[index_a, index_b, index_c, index_d] ** 2
            for index_a in range(dimension)
            for index_b in range(dimension)
            for index_c in range(dimension)
            for index_d in range(dimension)
        ]
    )
    cubic = simplify_sum(
        [
            weyl[index_r, index_s, index_m, index_n]
            * weyl[index_m, index_n, index_a, index_b]
            * weyl[index_a, index_b, index_r, index_s]
            for index_r in range(dimension)
            for index_s in range(dimension)
            for index_m in range(dimension)
            for index_n in range(dimension)
            for index_a in range(dimension)
            for index_b in range(dimension)
        ]
    )
    return quadratic, cubic


def check_weyl_tensor(weyl: sp.MutableDenseNDimArray) -> dict[str, bool]:
    dimension = 4
    antisymmetric_first_pair = all(
        sp.expand(weyl[index_a, index_b, index_c, index_d] + weyl[index_b, index_a, index_c, index_d])
        == 0
        for index_a in range(dimension)
        for index_b in range(dimension)
        for index_c in range(dimension)
        for index_d in range(dimension)
    )
    antisymmetric_second_pair = all(
        sp.expand(weyl[index_a, index_b, index_c, index_d] + weyl[index_a, index_b, index_d, index_c])
        == 0
        for index_a in range(dimension)
        for index_b in range(dimension)
        for index_c in range(dimension)
        for index_d in range(dimension)
    )
    pair_exchange = all(
        sp.expand(weyl[index_a, index_b, index_c, index_d] - weyl[index_c, index_d, index_a, index_b])
        == 0
        for index_a in range(dimension)
        for index_b in range(dimension)
        for index_c in range(dimension)
        for index_d in range(dimension)
    )
    first_bianchi = all(
        sp.expand(
            weyl[index_a, index_b, index_c, index_d]
            + weyl[index_a, index_c, index_d, index_b]
            + weyl[index_a, index_d, index_b, index_c]
        )
        == 0
        for index_a in range(dimension)
        for index_b in range(dimension)
        for index_c in range(dimension)
        for index_d in range(dimension)
    )
    ricci_zero = all(
        simplify_sum(
            [weyl[index_a, index_b, index_a, index_d] for index_a in range(dimension)]
        )
        == 0
        for index_b in range(dimension)
        for index_d in range(dimension)
    )
    return {
        "antisymmetric_first_pair": antisymmetric_first_pair,
        "antisymmetric_second_pair": antisymmetric_second_pair,
        "pair_exchange": pair_exchange,
        "first_bianchi": first_bianchi,
        "ricci_zero": ricci_zero,
    }


def build_rnc_terms(
    weyl: sp.MutableDenseNDimArray,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, tuple[sp.Symbol, ...]]:
    dimension = 4
    coordinates = sp.symbols("x0:4")
    bundle_connection: list[sp.Matrix] = []
    for derivative_index in range(dimension):
        bundle_connection.append(
            sp.Matrix(
                dimension,
                dimension,
                lambda row_index, column_index: sum(
                    sp.Rational(1, 2)
                    * weyl[row_index, column_index, coordinate_index, derivative_index]
                    * coordinates[coordinate_index]
                    for coordinate_index in range(dimension)
                ),
            )
        )
    normal_metric = sp.Matrix(
        dimension,
        dimension,
        lambda first_index, second_index: sum(
            sp.Rational(1, 3)
            * weyl[first_index, index_a, second_index, index_b]
            * coordinates[index_a]
            * coordinates[index_b]
            for index_a in range(dimension)
            for index_b in range(dimension)
        ),
    )
    connection_squared = sp.zeros(dimension)
    for derivative_index in range(dimension):
        connection_squared += bundle_connection[derivative_index] * bundle_connection[derivative_index]
    metric_connection = sp.zeros(dimension)
    for first_index in range(dimension):
        for second_index in range(dimension):
            metric_connection += sp.Rational(3, 4) * sp.diff(
                normal_metric[first_index, second_index]
                * bundle_connection[second_index],
                coordinates[first_index],
            )
    van_vleck_quartic = sp.trace(normal_metric * normal_metric) / 20
    scalar_normalization = (
        sp.Rational(1, 2)
        * sum(
            sp.diff(van_vleck_quartic, coordinates[index], 2)
            for index in range(dimension)
        )
        * sp.eye(dimension)
    )
    return connection_squared, metric_connection, scalar_normalization, coordinates


def portal_contraction(
    weyl: sp.MutableDenseNDimArray,
    matrix_polynomial: sp.Matrix,
    coordinates: tuple[sp.Symbol, ...],
) -> sp.Expr:
    dimension = 4
    return simplify_sum(
        [
            weyl[index_m, index_n, index_r, index_s]
            * sp.diff(
                matrix_polynomial[index_s, index_n],
                coordinates[index_m],
                coordinates[index_r],
            )
            / 3
            for index_m in range(dimension)
            for index_n in range(dimension)
            for index_r in range(dimension)
            for index_s in range(dimension)
        ]
    )


def bundle_commutator(
    weyl: sp.MutableDenseNDimArray,
    first_derivative: int,
    second_derivative: int,
    form_index: int,
    raised_form_index: int,
    row_index: int,
    column_index: int,
) -> sp.Expr:
    dimension = 4
    return simplify_sum(
        [
            -weyl[contracted_index, form_index, first_derivative, second_derivative]
            * weyl[row_index, column_index, contracted_index, raised_form_index]
            + weyl[raised_form_index, contracted_index, first_derivative, second_derivative]
            * weyl[row_index, column_index, form_index, contracted_index]
            + weyl[row_index, contracted_index, first_derivative, second_derivative]
            * weyl[contracted_index, column_index, form_index, raised_form_index]
            - weyl[contracted_index, column_index, first_derivative, second_derivative]
            * weyl[row_index, contracted_index, form_index, raised_form_index]
            for contracted_index in range(dimension)
        ]
    )


def derivative_portal_contraction(weyl: sp.MutableDenseNDimArray) -> sp.Expr:
    dimension = 4
    terms: list[sp.Expr] = []
    for index_m in range(dimension):
        for index_n in range(dimension):
            for index_r in range(dimension):
                for index_s in range(dimension):
                    second_derivative = sp.Rational(1, 8) * sum(
                        bundle_commutator(
                            weyl,
                            contracted_index,
                            index_r,
                            index_m,
                            contracted_index,
                            index_s,
                            index_n,
                        )
                        + bundle_commutator(
                            weyl,
                            contracted_index,
                            index_m,
                            index_r,
                            contracted_index,
                            index_s,
                            index_n,
                        )
                        for contracted_index in range(dimension)
                    )
                    terms.append(
                        weyl[index_m, index_n, index_r, index_s]
                        * second_derivative
                        / 3
                    )
    return simplify_sum(terms)


def lower_order_normalization(
    weyl: sp.MutableDenseNDimArray, quadratic_invariant: sp.Expr
) -> tuple[sp.Expr, sp.Expr]:
    dimension = 4
    contraction = simplify_sum(
        [
            sp.Rational(1, 2)
            * weyl[index_m, index_n, index_r, index_s]
            * weyl[index_s, index_n, index_m, index_r]
            for index_m in range(dimension)
            for index_n in range(dimension)
            for index_r in range(dimension)
            for index_s in range(dimension)
        ]
    )
    return contraction, sp.simplify(contraction / quadratic_invariant)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    failed_hashes = [
        path.as_posix()
        for path, expected_hash in EXPECTED_HASHES.items()
        if source_hashes[path] != expected_hash
    ]
    if failed_hashes:
        raise RuntimeError(f"source hash mismatch: {failed_hashes}")
    van_de_ven_text = VAN_DE_VEN_TEX.read_text(encoding="latin-1")
    required_markers = (
        "Fock-Schwinger gauge and Riemann normal coordinates",
        "\\sa_1 &=& \\Z",
        "\\ZM[X,Y,K]",
        "\\sfrac34 K +\\sfrac38 K^2",
        "Y (I +\\sfrac12 K",
    )
    missing_markers = [marker for marker in required_markers if marker not in van_de_ven_text]
    if missing_markers:
        raise RuntimeError(f"heat-kernel source markers missing: {missing_markers}")

    weyl, symbols = build_generic_weyl()
    symmetry_checks = check_weyl_tensor(weyl)
    quadratic_invariant, cubic_invariant = curvature_invariants(weyl)
    connection_squared, metric_connection, scalar_normalization, coordinates = build_rnc_terms(weyl)
    connection_squared_projection = portal_contraction(weyl, connection_squared, coordinates)
    metric_connection_projection = portal_contraction(weyl, metric_connection, coordinates)
    scalar_projection = portal_contraction(weyl, scalar_normalization, coordinates)
    derivative_projection = derivative_portal_contraction(weyl)
    total_projection = simplify_sum(
        [
            connection_squared_projection,
            metric_connection_projection,
            scalar_projection,
            derivative_projection,
        ]
    )
    lower_contraction, lower_ratio = lower_order_normalization(weyl, quadratic_invariant)
    all_checks_pass = all(symmetry_checks.values()) and all(
        expression == 0
        for expression in (
            connection_squared_projection,
            metric_connection_projection,
            scalar_projection,
            derivative_projection,
            total_projection,
        )
    )
    all_checks_pass = all_checks_pass and lower_ratio == -sp.Rational(1, 4)
    if not all_checks_pass:
        raise RuntimeError("portal linear C3 symbolic identity failed")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): source_hashes[path]
            for path in EXPECTED_HASHES
        },
        "primary_records": [
            "https://arxiv.org/abs/hep-th/9708152",
            "https://arxiv.org/abs/hep-th/9704166",
            "https://arxiv.org/abs/2312.03831",
            "https://arxiv.org/abs/2405.08860",
        ],
        "operator_contract": {
            "photon_action": "1/4 F^2 + G_CFF C^{mu nu rho sigma} F_mu_nu F_rho_sigma",
            "portal_hessian_on_ricci_flat_background": "P_portal^nu_sigma=-8 G_CFF C^{mu nu rho}_sigma D_mu D_rho",
            "minimal_operator": "Delta_a=-D^2 delta + Ricci",
            "source_regulator": "natural regulator is a scalar function of Delta_a and is independent of G_CFF",
        },
        "heat_kernel_contract": {
            "recursion": "a_(j,n)=j/(j+n) times the n-jet of the transformed Laplace operator acting on a_(j-1)",
            "linear_CFF_C3_jet": "[D_mu D_rho a_1]=(1/3) Z_(mu rho) on Ricci-flat backgrounds",
            "rnc_terms_retained": [
                "Y_mu Y^mu",
                "partial_mu[(3/4)K^{mu nu}Y_nu]",
                "(1/2)partial^2 tr(K^2)/20",
                "symmetrized second-curvature derivative reduced by divergence-free Weyl to bundle commutators",
            ],
        },
        "generic_weyl_parameterization": {
            "self_dual_eigenvalues": [
                str(symbols["plus_first"]),
                str(symbols["plus_second"]),
                f"-{symbols['plus_first']}-{symbols['plus_second']}",
            ],
            "anti_self_dual_eigenvalues": [
                str(symbols["minus_first"]),
                str(symbols["minus_second"]),
                f"-{symbols['minus_first']}-{symbols['minus_second']}",
            ],
            "quadratic_invariant": str(sp.factor(quadratic_invariant)),
            "cubic_invariant": str(sp.factor(cubic_invariant)),
            "symmetry_checks": symmetry_checks,
        },
        "normalization_check": {
            "C_DD_a0_contraction": str(lower_contraction),
            "ratio_to_C_squared": str(lower_ratio),
            "expected_ratio": "-1/4",
            "passed": lower_ratio == -sp.Rational(1, 4),
        },
        "weyl_cubic_projections": {
            "connection_squared": str(connection_squared_projection),
            "metric_connection": str(metric_connection_projection),
            "scalar_van_vleck": str(scalar_projection),
            "derivative_commutator": str(derivative_projection),
            "total": str(total_projection),
        },
        "theorem": {
            "statement": "The portal-dependent photon contribution to the Weyl-cubic flow that is linear in g_CFF vanishes exactly in the declared source scheme.",
            "formula": "Delta RHS_C3|linear in g_CFF = 0",
            "regulator_dependence": "none within scalar functions of the source natural Delta_a, because the tensor projection multiplying every threshold functional is identically zero",
            "proof_scope": [
                "four dimensions",
                "parity-even Weyl-cubic projection",
                "Ricci-flat minimal-essential projection",
                "source harmonic photon gauge",
                "source natural regulator independent of g_CFF",
                "boundary terms discarded as in the source local flow",
            ],
            "passed": total_projection == 0,
        },
        "remaining_exact_terms": [
            "quadratic g_CFF^2 Weyl-cubic photon contribution to beta_h_C3",
            "direct h_C3 contribution to the photon CFF projection",
        ],
        "closed_terms": [
            "minimal Maxwell a6 Weyl-cubic term",
            "linear g_CFF Weyl-cubic portal term",
            "principal cubic g_CFF^3 Weyl-cubic portal term",
            "six forbidden direct C3 photon projections: F2, FDeltaF, RFF, SFF, F2sq, F4",
        ],
        "full_combined_fixed_point_claimed": False,
        "all_checks_pass": all_checks_pass,
    }
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_LOWER_RATIO={lower_ratio}", flush=True)
    print(f"{MARKER}_LINEAR_C3_PROJECTION={total_projection}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
