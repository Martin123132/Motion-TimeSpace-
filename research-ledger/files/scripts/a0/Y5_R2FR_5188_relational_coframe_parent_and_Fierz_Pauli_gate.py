from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5188"

PRIOR_CSV = OUT / "prior_relational_parent_supersession.csv"
SCALAR_CSV = OUT / "scalar_clock_pullback_no_go.csv"
FACTOR_CSV = OUT / "minimal_relational_coframe_factorization.csv"
RANK_CSV = OUT / "coframe_H_rank_and_invariance.csv"
FP_CSV = OUT / "Fierz_Pauli_gauge_nullspace.csv"
ADM_CSV = OUT / "MTS_ADM_dictionary_and_mode_count.csv"
WITNESS_CSV = OUT / "curved_and_weak_field_witnesses.csv"
ACTION_CSV = OUT / "same_coframe_GR_Newton_Maxwell_chain.csv"
BOUNDARY_CSV = OUT / "parent_upgrade_claim_boundary.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "relational_coframe_parent_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5188_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-"
    "and-Fierz-Pauli-selection-theorem.md"
)

MARKER = "MTS_5188_RELATIONAL_COFRAME_AND_FIERZ_PAULI_SELECTION_THEOREM"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

PARENT_ACTION = (
    "S_parent=(M_R^2/2) int d4x e (R[e]-2 Lambda_cal)"
    " -(Z_A/4) int d4x e F_mn F^mn"
    " +S_matter[e,omega_LC[e],A,Phi_visible]"
    " +S_motion[e,psi]+Gamma_controlled_EFT"
)

LEADING_THEOREM = (
    "FOUR_RELATIONAL_SCALAR_CLOCKS_AND_RODS_WITH_A_CONSTANT_INTERNAL_"
    "LORENTZ_METRIC_GIVE_EITHER_A_FLAT_PULLBACK_WHEN_THEIR_JACOBIAN_IS_"
    "INVERTIBLE_OR_A_DEGENERATE_METRIC_WHEN_IT_IS_NOT_SO_CURVED_LOCAL_GR_"
    "REQUIRES_NONSCALAR_GEOMETRIC_DATA_THE_MINIMAL_MULTIPLICATIVE_"
    "RELATIONAL_COFRAME_E_EQUALS_DISTORTION_TIMES_DX_IS_EXACTLY_"
    "SURJECTIVE_ON_NONDEGENERATE_COFRAMES_ITS_SPLIT_REDUNDANCY_AND_LOCAL_"
    "LORENTZ_KERNEL_REMOVE_NO_PHYSICAL_METRIC_DIRECTION_AND_ITS_COMPOSITE_"
    "H_EQUALS_SQRT_MINUS_G_TIMES_G_INVERSE_HAS_RANK_TEN_LINEARIZED_"
    "MASSLESS_SPIN_TWO_GAUGE_INVARIANCE_UNIQUELY_SELECTS_THE_FIERZ_PAULI_"
    "RATIOS_ONE_MINUS_TWO_TWO_MINUS_ONE_AND_THE_TWO_DERIVATIVE_NONLINEAR_"
    "CONSISTENCY_PARENT_THEN_RECOVERS_THE_EXISTING_EINSTEIN_NEWTON_AND_"
    "SAME_COFRAME_MAXWELL_POYNTING_CHAINS"
)

CLAIM_GUARD = (
    "THIS_DERIVES_THE_SCALAR_CLOCK_NO_GO_THE_COFRAME_FACTORIZATION_"
    "GAUGE_RANK_MODE_COUNT_AND_FIERZ_PAULI_SELECTION_IT_DOES_NOT_DERIVE_"
    "THE_NONSCALAR_DISTORTION_FIELD_FROM_THE_OLD_ONE_SCALAR_MTS_CORPUS_"
    "DOES_NOT_DERIVE_VISIBLE_U1_REPRESENTATIONS_OR_THE_ABSOLUTE_NEWTON_"
    "SCALE_AND_IS_NOT_A_FULL_MTS_UNIFICATION_CLAIM"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES: dict[str, tuple[Path, str]] = {
    "checkpoint_787_multifield_rank": (
        source_path(
            "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-"
            "metric-branch-decision.md"
        ),
        "3d43d255af2ed3768a871b9de288cc1b60aa4fda5f102b10e57f5bf2488c6e82",
    ),
    "checkpoint_788_nonholonomic": (
        source_path(
            "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md"
        ),
        "add3529cc977df2b1645cd347d98f32418aa04064bbc0a1ff0f5681d7a41d2de",
    ),
    "checkpoint_1940_lovelock": (
        source_path(
            "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-"
            "operator.md"
        ),
        "16fbae5f11f431f790629b5466db3f706374a046cf8834303f11e7b22fce6714",
    ),
    "checkpoint_1963_owned_coframe": (
        source_path(
            "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-"
            "hypermomentum-row.md"
        ),
        "b3f1208fab1d612818603032dd91ed9f4fd1e38e2ac576c8b403f3ac1731649a",
    ),
    "checkpoint_2008_additive_frame": (
        source_path(
            "2008-Y5-R2FR-parent-nonholonomic-frame-deformation-action-or-"
            "tetrad-residual-runner.md"
        ),
        "6c5050b697b788c9699cff4fcf5589c80dbc0f84ecaa13bae01cd10bf62ca03b",
    ),
    "checkpoint_2009_no_extra_split_mode": (
        source_path(
            "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-"
            "response-kernel.md"
        ),
        "9ec52182bd67364ef090785348d6d228376cb4c2eadccf70e9a527189b2777c3",
    ),
    "checkpoint_2017_split_gauge": (
        source_path(
            "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-"
            "zero-or-finite-A-source-row.md"
        ),
        "9a3f4ee8a1aed1daa2de0a788bab4ac94872fe2c221a285f45576f09d7b83668",
    ),
    "checkpoint_2048_motion_load_coframe": (
        source_path(
            "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-"
            "provenance.md"
        ),
        "010b77e9fe7cabdaab18d1d3667d7772225278d3715fb3d1ee15493771411a0d",
    ),
    "checkpoint_3846_metric_bridge": (
        source_path(
            "3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-"
            "reject.md"
        ),
        "0c8f8b2bd47c714a2caab6ba775db93db3f815226f909fe1e8b929d7500d134a",
    ),
    "checkpoint_4960_universal_source": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-"
            "and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-"
            "boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4961_scalar_origin_boundary": (
        source_path(
            "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-"
            "motion-Hessian-or-explicit-fundamental-field-boundary.md"
        ),
        "ec6c5ff4056ed13ad92cad5e70ce125d81183abd0d79c59345dd6393987e2de2",
    ),
    "checkpoint_5187_canonical_action": (
        source_path(
            "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-"
            "residue-and-scale-setting-theorem.md"
        ),
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674",
    ),
    "checkpoint_5187_result": (
        source_path(
            "source-intake/functional_rg/5187/"
            "canonical_local_parent_action_results.json"
        ),
        "05d9e06edf88c219a6d21f49303b7e98dd82f3d1ecee5c9d445da385d4fa4e6d",
    ),
}

EXTERNAL_SOURCES = {
    "Fierz_Pauli_1939": "https://doi.org/10.1098/rspa.1939.0140",
    "ADM_reprint": "https://arxiv.org/abs/gr-qc/0405109",
    "Weinberg_1964_soft_graviton": "https://doi.org/10.1103/PhysRev.135.B1049",
    "Weinberg_1965_Einstein_completion": "https://doi.org/10.1103/PhysRev.138.B988",
    "Deser_1970_self_coupling": "https://doi.org/10.1007/BF00759198",
    "Deser_author_reprint": "https://arxiv.org/abs/gr-qc/0411023",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def validation_row(
    check_id: str,
    check: str,
    passed: bool,
    observed: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "observed": str(observed),
        "expected": str(expected),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
    }


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def matrix_sha256(matrix: sp.Matrix) -> str:
    payload = sp.srepr(matrix).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def ricci_scalar(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
    dimension = len(coordinates)
    inverse = sp.simplify(metric.inv())
    gamma = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[rho, lam]
                        * (
                            sp.diff(metric[lam, nu], coordinates[mu])
                            + sp.diff(metric[lam, mu], coordinates[nu])
                            - sp.diff(metric[mu, nu], coordinates[lam])
                        )
                        for lam in range(dimension)
                    )
                    / 2
                )
                for nu in range(dimension)
            ]
            for mu in range(dimension)
        ]
        for rho in range(dimension)
    ]
    ricci = sp.zeros(dimension)
    for mu in range(dimension):
        for nu in range(dimension):
            ricci[mu, nu] = sp.simplify(
                sum(
                    sp.diff(gamma[rho][mu][nu], coordinates[rho])
                    - sp.diff(gamma[rho][mu][rho], coordinates[nu])
                    + sum(
                        gamma[rho][rho][lam] * gamma[lam][mu][nu]
                        - gamma[rho][nu][lam] * gamma[lam][mu][rho]
                        for lam in range(dimension)
                    )
                    for rho in range(dimension)
                )
            )
    return sp.factor(
        sum(
            inverse[mu, nu] * ricci[mu, nu]
            for mu in range(dimension)
            for nu in range(dimension)
        )
    )


def linearized_einstein_00() -> sp.Expr:
    coordinates = sp.symbols("t x y z")
    _, x, y, z = coordinates
    phi = sp.Function("Phi")(x, y, z)
    eta = sp.diag(-1, 1, 1, 1)
    h = sp.diag(-2 * phi, -2 * phi, -2 * phi, -2 * phi)
    h_mixed = eta * h
    h_upper = eta * h * eta
    h_trace = sp.simplify(
        sum(eta[a, b] * h[a, b] for a in range(4) for b in range(4))
    )

    def second(expression: sp.Expr, first: int, second_index: int) -> sp.Expr:
        return sp.diff(expression, coordinates[first], coordinates[second_index])

    mu = 0
    nu = 0
    term_one = sum(second(h_mixed[rho, nu], rho, mu) for rho in range(4))
    term_two = sum(second(h_mixed[rho, mu], rho, nu) for rho in range(4))
    box_h = sum(
        eta[a, b] * second(h[mu, nu], a, b)
        for a in range(4)
        for b in range(4)
    )
    trace_derivative = second(h_trace, mu, nu)
    double_divergence = sum(
        second(h_upper[rho, sigma], rho, sigma)
        for rho in range(4)
        for sigma in range(4)
    )
    box_trace = sum(
        eta[a, b] * second(h_trace, a, b)
        for a in range(4)
        for b in range(4)
    )
    return sp.simplify(
        (
            term_one
            + term_two
            - box_h
            - trace_derivative
            - eta[mu, nu] * (double_divergence - box_trace)
        )
        / 2
    )


def build_prior_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "row_id": "PRIOR5188_00_787",
                "source_checkpoint": 787,
                "prior_result": "four first-jet directions can span ten symmetric metric variations",
                "retained": True,
                "superseded_or_advanced": "advanced by exact rank and curvature separation",
            },
            {
                "row_id": "PRIOR5188_01_788",
                "source_checkpoint": 788,
                "prior_result": "exact-gradient coframe is a flat pullback; nonholonomic coframe remains viable",
                "retained": True,
                "superseded_or_advanced": "proved as an exact flat-or-degenerate dichotomy",
            },
            {
                "row_id": "PRIOR5188_02_1963",
                "source_checkpoint": 1963,
                "prior_result": "owned-coframe local action exists as a conditional branch",
                "retained": True,
                "superseded_or_advanced": "given a relational factorization, gauge ranks and mode count",
            },
            {
                "row_id": "PRIOR5188_03_2008_2017",
                "source_checkpoint": "2008-2017",
                "prior_result": "additive split e=dX+A has a split gauge only when the action is e-only",
                "retained": True,
                "superseded_or_advanced": "replaced by multiplicative e=E dX with exact surjectivity",
            },
            {
                "row_id": "PRIOR5188_04_2048",
                "source_checkpoint": 2048,
                "prior_result": "static spherical T,S coframe and Levi-Civita connection were constructed",
                "retained": True,
                "superseded_or_advanced": "embedded as a symmetry-reduced relational coframe",
            },
            {
                "row_id": "PRIOR5188_05_3846",
                "source_checkpoint": 3846,
                "prior_result": "g=h-c_star^2 tau tau is Lorentzian under exact rank/sign assumptions",
                "retained": True,
                "superseded_or_advanced": "completed by the coframe and ADM time-space-motion dictionary",
            },
            {
                "row_id": "PRIOR5188_06_4961",
                "source_checkpoint": 4961,
                "prior_result": "one scalar cannot own integrated H or exact Diff",
                "retained": True,
                "superseded_or_advanced": "strengthened: four scalar clocks pass point rank but still cannot curve without extra tensor data",
            },
            {
                "row_id": "PRIOR5188_07_5187",
                "source_checkpoint": 5187,
                "prior_result": "integrated H, Diff and visible fields remained explicit parent data",
                "retained": True,
                "superseded_or_advanced": "H is now composite of a minimal coframe candidate; non-scalar E and visible representations remain parent data",
            },
            {
                "row_id": "PRIOR5188_08_search_verdict",
                "source_checkpoint": "corpus-wide 2026/2035/2048/2107/2108/2109/2117 search",
                "prior_result": "no parent-owned full-rank MTS map into a generic coframe was found",
                "retained": True,
                "superseded_or_advanced": "minimal parent extension is stated rather than hidden",
            },
        ]
    )


def build_rank_metrics() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    eta = sp.diag(-1, 1, 1, 1)
    pairs = [(mu, nu) for mu in range(4) for nu in range(mu, 4)]
    coframe_basis: list[sp.Matrix] = []
    for a in range(4):
        for mu in range(4):
            basis = sp.zeros(4)
            basis[a, mu] = 1
            coframe_basis.append(basis)

    metric_columns: list[list[sp.Expr]] = []
    h_columns: list[list[sp.Expr]] = []
    for delta_e in coframe_basis:
        delta_g = delta_e.T * eta + eta * delta_e
        delta_g_inverse = -eta * delta_g * eta
        delta_sqrt_g = sp.trace(delta_e)
        delta_h = delta_sqrt_g * eta + delta_g_inverse
        metric_columns.append([delta_g[mu, nu] for mu, nu in pairs])
        h_columns.append([delta_h[mu, nu] for mu, nu in pairs])

    e_to_metric = sp.Matrix(10, 16, lambda row, col: metric_columns[col][row])
    e_to_h = sp.Matrix(10, 16, lambda row, col: h_columns[col][row])
    split_to_e = sp.eye(16).row_join(sp.eye(16))
    split_to_metric = e_to_metric * split_to_e
    split_to_h = e_to_h * split_to_e

    jacobian = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 2],
        ]
    )
    distortion = sp.Matrix(
        [
            [2, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 2, 0],
            [0, 1, 0, 2],
        ]
    )
    relabel = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
        ]
    )
    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    coframe = distortion * jacobian
    relabelled_coframe = (distortion * relabel.inv()) * (relabel * jacobian)
    metric = coframe.T * eta * coframe
    boosted_metric = (boost * coframe).T * eta * (boost * coframe)
    density_h = coframe.det() * metric.inv()
    boosted_coframe = boost * coframe
    boosted_h = boosted_coframe.det() * boosted_metric.inv()

    metrics = {
        "e_to_metric_rank": int(e_to_metric.rank()),
        "e_to_metric_nullity": 16 - int(e_to_metric.rank()),
        "e_to_H_rank": int(e_to_h.rank()),
        "e_to_H_nullity": 16 - int(e_to_h.rank()),
        "split_to_e_rank": int(split_to_e.rank()),
        "split_to_e_nullity": 32 - int(split_to_e.rank()),
        "split_to_metric_rank": int(split_to_metric.rank()),
        "split_to_metric_nullity": 32 - int(split_to_metric.rank()),
        "split_to_H_rank": int(split_to_h.rank()),
        "split_to_H_nullity": 32 - int(split_to_h.rank()),
        "det_J": int(jacobian.det()),
        "det_E": int(distortion.det()),
        "det_e": int(coframe.det()),
        "det_g": int(metric.det()),
        "determinant_identity_residual": sp.simplify(
            metric.det() + coframe.det() ** 2
        )
        == 0,
        "relabel_invariance_exact": matrix_zero(relabelled_coframe - coframe),
        "lorentz_condition_exact": matrix_zero(boost.T * eta * boost - eta),
        "metric_lorentz_invariance_exact": matrix_zero(boosted_metric - metric),
        "H_lorentz_invariance_exact": matrix_zero(boosted_h - density_h),
        "e_to_metric_jacobian_sha256": matrix_sha256(e_to_metric),
        "e_to_H_jacobian_sha256": matrix_sha256(e_to_h),
    }

    rows = tagged(
        [
            {
                "row_id": "RANK5188_00_split_to_e",
                "map": "(delta E,delta J)->delta e=delta E+delta J at E=J=I",
                "rank": metrics["split_to_e_rank"],
                "nullity": metrics["split_to_e_nullity"],
                "meaning": "multiplicative split is surjective on all 16 coframe directions",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_01_e_to_g",
                "map": "delta e -> delta g=delta e^T eta+eta delta e",
                "rank": metrics["e_to_metric_rank"],
                "nullity": metrics["e_to_metric_nullity"],
                "meaning": "all ten metric directions are covered; six Lorentz-frame directions are null",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_02_split_to_g",
                "map": "(delta E,delta J)->delta g",
                "rank": metrics["split_to_metric_rank"],
                "nullity": metrics["split_to_metric_nullity"],
                "meaning": "six Lorentz plus sixteen first-jet split directions leave the metric unchanged",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_03_e_to_H",
                "map": "delta e -> delta H, H=sqrt(-g) g^{-1}",
                "rank": metrics["e_to_H_rank"],
                "nullity": metrics["e_to_H_nullity"],
                "meaning": "integrated H is a complete rank-ten coframe composite",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_04_split_to_H",
                "map": "(delta E,delta J)->delta H",
                "rank": metrics["split_to_H_rank"],
                "nullity": metrics["split_to_H_nullity"],
                "meaning": "no Hilbert-source direction is lost",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_05_determinant",
                "map": "det g=det(eta)(det e)^2=-(det E det J)^2",
                "rank": "",
                "nullity": "",
                "meaning": f"detE={metrics['det_E']};detJ={metrics['det_J']};detg={metrics['det_g']}",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_06_relabel",
                "map": "J->S J; E->E S^-1",
                "rank": "",
                "nullity": "",
                "meaning": "e, g and H are invariant under relational-chart relabelling",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "RANK5188_07_local_Lorentz",
                "map": "E->Lambda E; Lambda^T eta Lambda=eta",
                "rank": "",
                "nullity": 6,
                "meaning": "g and H are invariant under the six local Lorentz frame directions",
                "status": "DERIVED_EXACT",
            },
        ]
    )
    return rows, metrics


def build_scalar_rows(
    rank_metrics: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coordinates = sp.symbols("t x y z")
    _, x, _, _ = coordinates
    nonlinear_pullback_metric = sp.diag(-1, sp.exp(2 * x), 1, 1)
    nonlinear_pullback_ricci = sp.simplify(
        ricci_scalar(nonlinear_pullback_metric, coordinates)
    )
    metrics = {
        "four_scalar_first_jet_metric_rank": rank_metrics[
            "e_to_metric_rank"
        ],
        "invertible_constant_internal_metric_is_flat": (
            nonlinear_pullback_ricci == 0
        ),
        "nonlinear_pullback_sample_R": str(nonlinear_pullback_ricci),
        "rank_deficient_branch_is_degenerate": True,
        "nonconstant_target_metric_adds_tensor_data": True,
    }
    rows = tagged(
        [
            {
                "row_id": "SCALAR5188_00_definition",
                "branch": "four relational scalars only",
                "equation": "g_mn=eta_AB partial_m X^A partial_n X^B=J^T eta J",
                "result": "candidate has pointwise rank but no independent curvature carrier",
                "status": "DEFINED",
            },
            {
                "row_id": "SCALAR5188_01_point_rank",
                "branch": "rank(J)=4",
                "equation": "rank(delta g/delta J)=10 at J=I",
                "result": rank_metrics["e_to_metric_rank"],
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "SCALAR5188_02_invertible",
                "branch": "det(J)!=0",
                "equation": "X^A are local coordinates and g=X^* eta",
                "result": "Riemann[g]=X^*Riemann[eta]=0",
                "status": "DERIVED_EXACT_FLAT_PULLBACK",
            },
            {
                "row_id": "SCALAR5188_03_nonlinear_witness",
                "branch": "X=(t,exp(x),y,z)",
                "equation": "g=diag(-1,exp(2x),1,1)",
                "result": f"R={nonlinear_pullback_ricci}",
                "status": "EXECUTED_EXACT_ZERO",
            },
            {
                "row_id": "SCALAR5188_04_rank_deficient",
                "branch": "det(J)=0",
                "equation": "det(g)=det(eta) det(J)^2",
                "result": "det(g)=0",
                "status": "DERIVED_EXACT_DEGENERATE",
            },
            {
                "row_id": "SCALAR5188_05_dichotomy",
                "branch": "constant internal eta and no extra tensor",
                "equation": "det(J)!=0 => flat; det(J)=0 => degenerate",
                "result": "generic curved local GR is impossible",
                "status": "PROVED_NO_GO",
            },
            {
                "row_id": "SCALAR5188_06_target_metric_escape",
                "branch": "g=G_AB(X)dX^A dX^B",
                "equation": "G_AB has ten local components in relational coordinates",
                "result": "curvature is possible only because new tensor data G_AB were supplied",
                "status": "NOT_A_SCALAR_ONLY_ESCAPE",
            },
            {
                "row_id": "SCALAR5188_07_one_scalar",
                "branch": "one motion scalar",
                "equation": "rank(first-jet map)<=5",
                "result": "checkpoint 4961 obstruction remains",
                "status": "RETAINED_NO_GO",
            },
        ]
    )
    return rows, metrics


def build_factor_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "row_id": "FACTOR5188_00_fields",
                "object": "relational clocks/rods plus distortion",
                "definition": "J^A_m=partial_m X^A; E^a_A(x) is an independent spacetime-scalar GL(4) coframe distortion",
                "derived_property": "E carries the geometric information absent from scalar clocks",
                "status": "MINIMAL_PARENT_EXTENSION",
            },
            {
                "row_id": "FACTOR5188_01_coframe",
                "object": "public coframe",
                "definition": "e^a_m=E^a_A J^A_m",
                "derived_property": "a spacetime one-form under Diff and Lorentz vector under frame rotations",
                "status": "DERIVED_FROM_PARENT_FIELDS",
            },
            {
                "row_id": "FACTOR5188_02_metric",
                "object": "public metric",
                "definition": "g_mn=eta_ab e^a_m e^b_n",
                "derived_property": "Lorentzian whenever det(E)det(J)!=0",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "FACTOR5188_03_H",
                "object": "integrated tensor density",
                "definition": "H^mn=|det(e)| e_a^m eta^ab e_b^n=sqrt(-g)g^mn",
                "derived_property": "rank-ten metric-density composite; not an additional independent field",
                "status": "DERIVED_EXACT_INSIDE_CANDIDATE",
            },
            {
                "row_id": "FACTOR5188_04_surjectivity",
                "object": "coframe map",
                "definition": "for any e and invertible J choose E=e J^-1",
                "derived_property": "every local nondegenerate coframe is represented exactly",
                "status": "PROVED_EXACT_SURJECTIVITY",
            },
            {
                "row_id": "FACTOR5188_05_anholonomy",
                "object": "curvature carrier",
                "definition": "de^a=dE^a_A wedge dX^A because d^2 X^A=0",
                "derived_property": "variable E permits anholonomy and curved Levi-Civita geometry",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "FACTOR5188_06_relabel",
                "object": "relational-chart redundancy",
                "definition": "X->f(X), J->S J, E->E S^-1",
                "derived_property": "e, g, H and every e-only observable are invariant",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "FACTOR5188_07_lorentz",
                "object": "frame redundancy",
                "definition": "E->Lambda(x)E with Lambda^T eta Lambda=eta",
                "derived_property": "six coframe directions are metric-null",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "FACTOR5188_08_diff",
                "object": "spacetime Diff",
                "definition": "X and E are spacetime scalars except for relational/frame indices; e^a=e^a_m dx^m",
                "derived_property": "a parent action written as a scalar four-form is manifestly Diff invariant",
                "status": "PARENT_SYMMETRY_REALIZED_NOT_SCALAR_GENERATED",
            },
            {
                "row_id": "FACTOR5188_09_unitary_gauge",
                "object": "relational gauge X^A=x^A",
                "definition": "J=I and e=E",
                "derived_property": "candidate reduces to the owned-coframe branch without changing observables",
                "status": "DERIVED_EXACT",
            },
            {
                "row_id": "FACTOR5188_10_old_scalar_status",
                "object": "old motion scalar psi",
                "definition": "psi may remain a scalar matter/exchange field but is not the sole metric owner",
                "derived_property": "checkpoint 5187 reflection-even local silence remains intact",
                "status": "RETAINED_AS_COMPONENT_NOT_GEOMETRY_BOOTSTRAP",
            },
        ]
    )


def build_fp_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    constraint_rows: list[list[sp.Expr]] = []
    eta = sp.diag(-1, 1, 1, 1)
    momenta = [
        sp.Matrix([1, 2, 3, 4]),
        sp.Matrix([2, -1, 1, 3]),
        sp.Matrix([3, 1, -2, 1]),
    ]
    for momentum in momenta:
        momentum_squared = (momentum.T * eta * momentum)[0]
        for mu in range(4):
            for nu in range(mu, 4):
                h = sp.zeros(4)
                h[mu, nu] = 1
                h[nu, mu] = 1
                h_upper = eta * h * eta
                h_trace = sp.trace(eta * h)
                h_divergence = h_upper.T * momentum
                h_kk = (momentum.T * h_upper * momentum)[0]
                for xi_index in range(4):
                    xi = sp.eye(4)[:, xi_index]
                    gauge_h = momentum * xi.T + xi * momentum.T
                    gauge_h_upper = eta * gauge_h * eta
                    gauge_trace = sp.trace(eta * gauge_h)
                    gauge_divergence = gauge_h_upper.T * momentum
                    gauge_kk = (
                        momentum.T * gauge_h_upper * momentum
                    )[0]
                    basis_one = 2 * momentum_squared * sum(
                        h[i, j] * gauge_h_upper[i, j]
                        for i in range(4)
                        for j in range(4)
                    )
                    basis_two = 2 * (
                        h_divergence.T * eta * gauge_divergence
                    )[0]
                    basis_three = (
                        h_kk * gauge_trace + gauge_kk * h_trace
                    )
                    basis_four = (
                        2 * momentum_squared * h_trace * gauge_trace
                    )
                    constraint_rows.append(
                        [basis_one, basis_two, basis_three, basis_four]
                    )
    constraint_matrix = sp.Matrix(constraint_rows)
    nullspace = constraint_matrix.nullspace()
    normalized = sp.simplify(nullspace[0] / nullspace[0][0])
    expected = sp.Matrix([1, -2, 2, -1])
    residual = constraint_matrix * expected
    metrics = {
        "constraint_row_count": int(constraint_matrix.rows),
        "constraint_rank": int(constraint_matrix.rank()),
        "constraint_nullity": int(constraint_matrix.cols - constraint_matrix.rank()),
        "normalized_null_vector": [int(value) for value in normalized],
        "expected_vector": [1, -2, 2, -1],
        "gauge_residual_exact_zero": matrix_zero(residual),
        "constraint_matrix_sha256": matrix_sha256(constraint_matrix),
        "positive_energy_standard_vector": [
            "-1/2",
            "1",
            "-1",
            "1/2",
        ],
    }
    rows = tagged(
        [
            {
                "row_id": "FP5188_00_basis",
                "object": "general Lorentz-invariant local two-derivative symmetric-tensor quadratic action",
                "equation": "L=a(dh_mn)^2+b(d_m h^mn)(d^r h_rn)+c(d_m h^mn)d_n h+d(dh)^2",
                "result": "four coefficient directions before gauge invariance",
                "status": "DEFINED",
            },
            {
                "row_id": "FP5188_01_gauge",
                "object": "massless spin-two gauge variation",
                "equation": "delta h_mn=partial_m xi_n+partial_n xi_m",
                "result": "quadratic bilinear must annihilate every gauge direction",
                "status": "IMPOSED_PARENT_SYMMETRY",
            },
            {
                "row_id": "FP5188_02_matrix",
                "object": "exact rational Lorentzian gauge-constraint matrix",
                "equation": "120 timelike/spacelike h/xi/momentum probes by four coefficient columns",
                "result": f"rank={metrics['constraint_rank']};nullity={metrics['constraint_nullity']}",
                "status": "EXECUTED_EXACT",
            },
            {
                "row_id": "FP5188_03_unique_ratio",
                "object": "(a,b,c,d)",
                "equation": "kernel(M_FP)",
                "result": "(1,-2,2,-1)",
                "status": "DERIVED_UNIQUE_UP_TO_OVERALL_SCALE",
            },
            {
                "row_id": "FP5188_04_standard_sign",
                "object": "positive helicity-two convention",
                "equation": "L_FP=-1/2 L1+L2-L3+1/2 L4",
                "result": "overall sign/normalization fixed by positive residue M_R^2>0",
                "status": "DERIVED_AFTER_POSITIVITY",
            },
            {
                "row_id": "FP5188_05_nonlinear",
                "object": "two-derivative nonlinear completion",
                "equation": "single massless spin-two pole + local gauge consistency + universal Hilbert source",
                "result": "Einstein-Hilbert plus Lambda up to field redefinitions, boundary and topological terms",
                "status": "INHERITED_DERIVED_UNDER_4960_CONSISTENCY_PREMISES",
            },
            {
                "row_id": "FP5188_06_scope",
                "object": "higher derivative/nonlocal operators",
                "equation": "not removed by Fierz-Pauli gauge uniqueness",
                "result": "retain the 5187 controlled EFT corridor",
                "status": "EXPLICIT_SCOPE_BOUNDARY",
            },
        ]
    )
    return rows, metrics


def build_adm_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    symmetric_basis: list[sp.Matrix] = []
    for i in range(3):
        for j in range(i, 3):
            basis = sp.zeros(3)
            basis[i, j] = 1
            basis[j, i] = 1
            symmetric_basis.append(basis)
    dewitt = sp.Matrix(
        [
            [
                sp.trace(first * second)
                - sp.trace(first) * sp.trace(second)
                for second in symmetric_basis
            ]
            for first in symmetric_basis
        ]
    )
    eigenvalues = dewitt.eigenvals()
    positive = sum(
        multiplicity
        for value, multiplicity in eigenvalues.items()
        if value > 0
    )
    negative = sum(
        multiplicity
        for value, multiplicity in eigenvalues.items()
        if value < 0
    )
    zero = sum(
        multiplicity
        for value, multiplicity in eigenvalues.items()
        if value == 0
    )
    physical_configuration_dof = (12 - 2 * 4) // 2
    metrics = {
        "dewitt_rank": int(dewitt.rank()),
        "dewitt_positive": int(positive),
        "dewitt_negative": int(negative),
        "dewitt_zero": int(zero),
        "dewitt_matrix": [
            [int(value) for value in dewitt.row(row)]
            for row in range(dewitt.rows)
        ],
        "ADM_first_class_constraints": 4,
        "physical_spin2_configuration_dof": physical_configuration_dof,
    }
    rows = tagged(
        [
            {
                "row_id": "ADM5188_00_time",
                "MTS_word": "time",
                "geometric_object": "tau=e^0/c_star=N dt on the hypersurface-orthogonal branch",
                "equation": "tau(u)=1",
                "derived_role": "clock one-form and foliation normal",
                "status": "EXACT_DICTIONARY",
            },
            {
                "row_id": "ADM5188_01_space",
                "MTS_word": "space",
                "geometric_object": "h_mn=sum_i e^i_m e^i_n",
                "equation": "h_mn u^n=0; rank(h)=3",
                "derived_role": "positive spatial geometry",
                "status": "EXACT_DICTIONARY",
            },
            {
                "row_id": "ADM5188_02_motion",
                "MTS_word": "motion",
                "geometric_object": "u plus K_ij=(1/2)L_u h_ij",
                "equation": "K is the rate of spatial geometry along physical time flow",
                "derived_role": "motion is the gravitational kinetic variable, not an extra slogan",
                "status": "EXACT_DICTIONARY",
            },
            {
                "row_id": "ADM5188_03_metric",
                "MTS_word": "time-space synthesis",
                "geometric_object": "g_mn=h_mn-c_star^2 tau_m tau_n",
                "equation": "checkpoint 3846 bridge",
                "derived_role": "public Lorentzian metric",
                "status": "EXACT_INSIDE_NONDEGENERATE_BRANCH",
            },
            {
                "row_id": "ADM5188_04_action",
                "MTS_word": "GR dynamics",
                "geometric_object": "ADM Einstein-Hilbert action",
                "equation": "S_EH=(M_R^2/2) int N sqrt(h)[R3+K_ij K^ij-K^2-2 Lambda]+boundary",
                "derived_role": "one action evolves space through time while enforcing Diff constraints",
                "status": "EXACT_GAUSS_CODAZZI_REWRITE",
            },
            {
                "row_id": "ADM5188_05_momentum",
                "MTS_word": "motion momentum",
                "geometric_object": "pi^ij=M_R^2 sqrt(h)(K^ij-K h^ij)",
                "equation": "delta S/delta dot(h_ij)",
                "derived_role": "canonical motion of spatial geometry",
                "status": "DERIVED_FROM_ADM_ACTION",
            },
            {
                "row_id": "ADM5188_06_constraints",
                "MTS_word": "gauge/constraint structure",
                "geometric_object": "Hamiltonian H_perp and three momentum H_i constraints",
                "equation": "N and N^i are Lagrange multipliers",
                "derived_role": "four first-class generators realize spacetime Diff",
                "status": "STANDARD_PARENT_CONSTRAINT_THEOREM",
            },
            {
                "row_id": "ADM5188_07_mode_count",
                "MTS_word": "physical gravity modes",
                "geometric_object": "six h_ij coordinates and four first-class constraints",
                "equation": "(12-2*4)/2=2",
                "derived_role": "two massless helicity-two configuration degrees of freedom",
                "status": "DERIVED_EXACT_COUNT",
            },
            {
                "row_id": "ADM5188_08_dewitt",
                "MTS_word": "motion Hessian",
                "geometric_object": "K_ij K^ij-K^2",
                "equation": f"rank={metrics['dewitt_rank']};inertia=({metrics['dewitt_positive']}+,{metrics['dewitt_negative']}-,{metrics['dewitt_zero']}0)",
                "derived_role": "full spatial kinetic rank; constrained conformal direction is explicit",
                "status": "EXECUTED_EXACT",
            },
        ]
    )
    return rows, metrics


def build_witness_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coordinates = sp.symbols("t x y z")
    t, _, _, _ = coordinates
    scale_factor = sp.Function("a")(t)
    flrw_metric = sp.diag(
        -1,
        scale_factor**2,
        scale_factor**2,
        scale_factor**2,
    )
    flrw_ricci = sp.factor(ricci_scalar(flrw_metric, coordinates))
    hubble = sp.symbols("H", positive=True)
    de_sitter_ricci = sp.simplify(
        6
        * (
            sp.exp(hubble * t)
            * sp.diff(sp.exp(hubble * t), t, 2)
            + sp.diff(sp.exp(hubble * t), t) ** 2
        )
        / sp.exp(hubble * t) ** 2
    )
    weak_g00 = -2
    weak_gii = -2
    einstein_00 = linearized_einstein_00()
    laplacian_phi = (
        sp.Derivative(sp.Function("Phi")(*coordinates[1:]), coordinates[1], 2)
        + sp.Derivative(sp.Function("Phi")(*coordinates[1:]), coordinates[2], 2)
        + sp.Derivative(sp.Function("Phi")(*coordinates[1:]), coordinates[3], 2)
    )
    metrics = {
        "FLRW_Ricci_scalar": str(flrw_ricci),
        "de_Sitter_Ricci_scalar": str(de_sitter_ricci),
        "weak_metric_g00_coefficient": weak_g00,
        "weak_metric_gii_coefficient": weak_gii,
        "linearized_Einstein_G00": str(einstein_00),
        "linearized_Einstein_G00_equals_2_laplacian": (
            sp.simplify(einstein_00 - 2 * laplacian_phi) == 0
        ),
        "PPN_gamma": 1,
    }
    rows = tagged(
        [
            {
                "row_id": "WITNESS5188_00_FLRW",
                "coframe": "e=diag(1,a(t),a(t),a(t)); X=x",
                "metric_or_curvature": "g=diag(-1,a^2,a^2,a^2)",
                "executed_result": f"R={flrw_ricci}",
                "meaning": "variable E carries genuine cosmological curvature",
                "status": "EXECUTED_EXACT",
            },
            {
                "row_id": "WITNESS5188_01_deSitter",
                "coframe": "a(t)=exp(Ht)",
                "metric_or_curvature": "flat-slicing de Sitter witness",
                "executed_result": f"R={de_sitter_ricci}",
                "meaning": "nonzero curvature is generated without changing relational coordinates",
                "status": "EXECUTED_EXACT",
            },
            {
                "row_id": "WITNESS5188_02_static_motion_load",
                "coframe": "e=diag(T,sqrt(S),r,r sin(theta)) in (t,r,theta,phi)",
                "metric_or_curvature": "ds2=-T^2 dt2+S dr2+r2 dOmega2",
                "executed_result": "exact embedding of checkpoint 2048",
                "meaning": "earlier T,S work is a symmetry reduction, not discarded",
                "status": "DERIVED_ALGEBRAIC_EMBEDDING",
            },
            {
                "row_id": "WITNESS5188_03_weak_Newton",
                "coframe": "e^0_0=1+Phi; e^i_j=(1-Phi)delta^i_j",
                "metric_or_curvature": "g00=-(1+2Phi)+O(Phi2); gij=(1-2Phi)deltaij+O(Phi2)",
                "executed_result": "Phi=Psi and gamma=1",
                "meaning": "one coframe potential controls slow bodies and light",
                "status": "DERIVED_EXACT_TO_LINEAR_ORDER",
            },
            {
                "row_id": "WITNESS5188_04_Einstein00",
                "coframe": "same weak coframe",
                "metric_or_curvature": "linearized Einstein tensor",
                "executed_result": f"G00={einstein_00}",
                "meaning": "M_R^2 G00=rho gives nabla2 Phi=rho/(2M_R^2)=4 pi G_N rho",
                "status": "EXECUTED_EXACT_LINEARIZATION",
            },
            {
                "row_id": "WITNESS5188_05_geodesic",
                "coframe": "same public metric",
                "metric_or_curvature": "slow geodesic and null eikonal",
                "executed_result": "d2x/dt2=-grad(Phi); PPN gamma=1",
                "meaning": "Newton, clocks and lensing are not separately retuned",
                "status": "INHERITED_FROM_SINGLE_METRIC",
            },
        ]
    )
    return rows, metrics


def build_action_rows(
    result_5187: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    prior_claim = result_5187["claim_status"]
    electric_symbols = sp.symbols("E_x E_y E_z")
    magnetic_symbols = sp.symbols("B_x B_y B_z")
    electric = sp.Matrix(electric_symbols)
    magnetic = sp.Matrix(magnetic_symbols)
    eta = sp.diag(-1, 1, 1, 1)
    field_strength = sp.zeros(4)
    for spatial_index, component in enumerate(electric_symbols, start=1):
        field_strength[0, spatial_index] = component
        field_strength[spatial_index, 0] = -component
    field_strength[1, 2] = -magnetic_symbols[2]
    field_strength[2, 1] = magnetic_symbols[2]
    field_strength[2, 3] = -magnetic_symbols[0]
    field_strength[3, 2] = magnetic_symbols[0]
    field_strength[3, 1] = -magnetic_symbols[1]
    field_strength[1, 3] = magnetic_symbols[1]
    field_strength_upper = eta * field_strength * eta
    field_strength_mixed = field_strength_upper * eta
    field_square = sp.simplify(
        sum(
            field_strength[mu, nu] * field_strength_upper[mu, nu]
            for mu in range(4)
            for nu in range(4)
        )
    )
    stress_upper = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            stress_upper[mu, nu] = sp.simplify(
                sum(
                    field_strength_upper[mu, alpha]
                    * field_strength_mixed[nu, alpha]
                    for alpha in range(4)
                )
                - eta[mu, nu] * field_square / 4
            )
    poynting = sp.Matrix([stress_upper[0, index] for index in range(1, 4)])
    expected_poynting = electric.cross(magnetic)
    expected_energy = sp.simplify(
        (electric.dot(electric) + magnetic.dot(magnetic)) / 2
    )
    stress_trace = sp.simplify(
        sum(
            eta[mu, nu] * stress_upper[mu, nu]
            for mu in range(4)
            for nu in range(4)
        )
    )
    metrics = {
        "prior_GR_Newton_chain": bool(
            prior_claim["leading_local_GR_Newton_chain_inside_parent"]
        ),
        "prior_Maxwell_Poynting_chain": bool(
            prior_claim[
                "flat_Maxwell_Lorentz_stress_Poynting_chain_inside_parent"
            ]
        ),
        "prior_Hessian_block_diagonal": bool(
            prior_claim["vacuum_Hessian_block_diagonal"]
        ),
        "prior_universal_residue": bool(
            prior_claim["one_universal_leading_spin2_residue"]
        ),
        "canonical_Maxwell_F2": str(field_square),
        "canonical_Maxwell_energy_density": str(stress_upper[0, 0]),
        "canonical_Maxwell_energy_expected": str(expected_energy),
        "canonical_Maxwell_energy_exact": (
            sp.simplify(stress_upper[0, 0] - expected_energy) == 0
        ),
        "canonical_Poynting_vector": [str(value) for value in poynting],
        "canonical_Poynting_expected": [
            str(value) for value in expected_poynting
        ],
        "canonical_Poynting_exact": matrix_zero(
            poynting - expected_poynting
        ),
        "canonical_Maxwell_stress_trace": str(stress_trace),
    }
    rows = tagged(
        [
            {
                "row_id": "ACTION5188_00_parent",
                "sector": "one local parent action",
                "equation": PARENT_ACTION,
                "derivation": "replace independent H by H[e(E,dX)] while retaining the 5187 action",
                "status": "CONSTRUCTED_MINIMAL_PARENT_CANDIDATE",
            },
            {
                "row_id": "ACTION5188_01_no_independent_connection",
                "sector": "geometry",
                "equation": "omega=omega_LC[e]; no independent Gamma argument",
                "derivation": "connection hypermomentum is absent by variable signature",
                "status": "DERIVED_INSIDE_PARENT",
            },
            {
                "row_id": "ACTION5188_02_Einstein",
                "sector": "gravity",
                "equation": "M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn",
                "derivation": "Fierz-Pauli plus two-derivative nonlinear consistency and Hilbert variation",
                "status": "DERIVED_UNDER_EXPLICIT_PARENT_PREMISES",
            },
            {
                "row_id": "ACTION5188_03_Newton",
                "sector": "weak static gravity",
                "equation": "nabla2 Phi=4 pi G_N rho; G_N=1/(8 pi M_R^2)",
                "derivation": "executed G00=2 nabla2 Phi and the same Einstein residue",
                "status": "DERIVED_UNDER_EXPLICIT_PARENT_PREMISES",
            },
            {
                "row_id": "ACTION5188_04_geodesic_lensing",
                "sector": "matter and light",
                "equation": "a=-grad(Phi); gamma=1; null rays use g[e]",
                "derivation": "one owned coframe for source, matter, clocks and photons",
                "status": "DERIVED_UNDER_SAME_FRAME_FUNCTOR",
            },
            {
                "row_id": "ACTION5188_05_Maxwell",
                "sector": "electromagnetism",
                "equation": "S_EM=-(Z_A/4)int e F_mn F^mn; F=dA; dF=0",
                "derivation": "the Hodge star and all contractions are built from the same e",
                "status": "DERIVED_INSIDE_U1_PARENT_CONTENT",
            },
            {
                "row_id": "ACTION5188_06_Coulomb_Lorentz",
                "sector": "electromagnetic force",
                "equation": "nabla_m(Z_A F^mn)=J^n; m u.nabla u^m=q F^m_n u^n",
                "derivation": "A variation and worldline/matter variation",
                "status": "DERIVED_INSIDE_U1_PARENT_CONTENT",
            },
            {
                "row_id": "ACTION5188_07_stress_Poynting",
                "sector": "electromagnetic gravity source",
                "equation": "T_EM,mn=Z_A(F_ma F_n^a-g_mn F2/4); T_EM^0i=Z_A(E cross B)^i=(E_c cross B_c)^i",
                "derivation": "coframe variation of the same Maxwell action",
                "status": "EXECUTED_EXACT_IN_LOCAL_ORTHONORMAL_FRAME",
            },
            {
                "row_id": "ACTION5188_07b_Maxwell_checks",
                "sector": "electromagnetic local orthonormal frame",
                "equation": f"F2={field_square};T00={stress_upper[0, 0]};trace(T)={stress_trace}",
                "derivation": f"T0i={tuple(poynting)}=E cross B",
                "status": "EXECUTED_EXACT",
            },
            {
                "row_id": "ACTION5188_08_split_no_extra_mode",
                "sector": "relational split",
                "equation": "deltaS/deltaE^a_A=E_e,a^m J^A_m; deltaS/deltaX^A=-partial_m(E_e,a^m E^a_A)",
                "derivation": "if S depends on E,X only through e, E equations imply X equations",
                "status": "DERIVED_NO_EXTRA_SPLIT_MODE",
            },
            {
                "row_id": "ACTION5188_09_extra_mode_guard",
                "sector": "parent extensions",
                "equation": "separate X or E terms not expressible through e",
                "derivation": "break split identity and require a new pole/constraint analysis",
                "status": "FORBIDDEN_IN_MINIMAL_PARENT_OR_EXPLICITLY_SCORED",
            },
            {
                "row_id": "ACTION5188_10_EFT",
                "sector": "controlled corrections",
                "equation": "C3, CFF, nonlocal and p8plus terms remain as in checkpoint 5187",
                "derivation": "coframe construction does not erase already bounded EFT operators",
                "status": "RETAINED_WITH_EXISTING_CORRIDOR",
            },
        ]
    )
    return rows, metrics


def build_boundary_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "row_id": "BOUND5188_00_scalar_no_go",
                "object": "scalar-clock-only curved GR",
                "current_status": "REJECTED_EXACTLY",
                "what_is_derived": "flat-or-degenerate dichotomy for constant internal metric",
                "what_remains": "none for this branch",
            },
            {
                "row_id": "BOUND5188_01_coframe",
                "object": "minimal relational coframe",
                "current_status": "CONSTRUCTED_EXACTLY",
                "what_is_derived": "surjectivity, determinant, split redundancy, Lorentz kernel and H map",
                "what_remains": "physical parent principle selecting E",
            },
            {
                "row_id": "BOUND5188_02_diff",
                "object": "Diff",
                "current_status": "MANIFEST_PARENT_SYMMETRY",
                "what_is_derived": "natural field action and ADM first-class realization inside EH",
                "what_remains": "Diff is not generated by the old scalar alone",
            },
            {
                "row_id": "BOUND5188_03_spin2",
                "object": "massless spin-two kinetic operator",
                "current_status": "DERIVED_UNIQUE_UP_TO_SCALE",
                "what_is_derived": "Fierz-Pauli ratio (1,-2,2,-1)",
                "what_remains": "overall M_R scale calibration",
            },
            {
                "row_id": "BOUND5188_04_EH",
                "object": "Einstein-Hilbert local two-derivative action",
                "current_status": "DERIVED_UNDER_EXPLICIT_CONSISTENCY_PREMISES",
                "what_is_derived": "nonlinear completion inside one positive massless spin-two Diff parent",
                "what_remains": "higher-derivative/nonlocal EFT corridor",
            },
            {
                "row_id": "BOUND5188_05_GR_Newton",
                "object": "leading local GR and Newton",
                "current_status": "ESTABLISHED_INSIDE_PARENT",
                "what_is_derived": "Einstein, Poisson, Newton, geodesic and gamma=1 chains",
                "what_remains": "absolute G_N calibration and complete all-operator equality",
            },
            {
                "row_id": "BOUND5188_06_EM",
                "object": "Maxwell, Lorentz, stress and Poynting",
                "current_status": "ESTABLISHED_INSIDE_PARENT",
                "what_is_derived": "same-coframe U1 action and source/stress chain",
                "what_remains": "why visible U1 representations and charge spectrum are selected",
            },
            {
                "row_id": "BOUND5188_07_old_MTS",
                "object": "old scalar motion field",
                "current_status": "SURVIVES_AS_MATTER_EXCHANGE_COMPONENT",
                "what_is_derived": "reflection-even local source silence from 5187 is preserved",
                "what_remains": "map its dynamics to coframe/ADM invariants without making it sole geometry",
            },
            {
                "row_id": "BOUND5188_08_original_spirit",
                "object": "motion-time-space interpretation",
                "current_status": "FORMALIZED_AS_TAU_H_U_K",
                "what_is_derived": "time one-form, spatial geometry and its motion reconstruct g and the ADM action",
                "what_remains": "derive tau,h,u/K from a deeper MTS microscopic parent or retain them fundamental",
            },
            {
                "row_id": "BOUND5188_09_full_unification",
                "object": "full MTS fundamental theory",
                "current_status": "NOT_CLAIMED",
                "what_is_derived": "a viable non-scalar parent architecture and exact leading local limits",
                "what_remains": "coframe origin, visible representations, scale origin, cosmology/galaxy/particle completion",
            },
            {
                "row_id": "BOUND5188_10_decision",
                "object": "parent ontology",
                "current_status": "MINIMAL_EXTENSION_REQUIRED",
                "what_is_derived": "old scalar-only ontology cannot carry generic curved geometry",
                "what_remains": "choose E/tau/h/u as fundamental or derive them from a genuinely non-scalar MTS sector",
            },
            {
                "row_id": "BOUND5188_11_invertible_patch",
                "object": "relational chart domain",
                "current_status": "LOCAL_NONDEGENERATE_BRANCH_ONLY",
                "what_is_derived": "all factorization and split theorems hold wherever det(J)det(E) is nonzero",
                "what_remains": "global atlas, caustic and topology treatment",
            },
            {
                "row_id": "BOUND5188_12_e_only",
                "object": "no-extra-split-mode premise",
                "current_status": "EXACT_IF_E_ONLY",
                "what_is_derived": "X equation is dependent on the E/coframe equation",
                "what_remains": "forbid or separately analyze every direct X/E operator not expressible through e",
            },
            {
                "row_id": "BOUND5188_13_boundary",
                "object": "relational and Diff boundary generators",
                "current_status": "LOCAL_PROPER_TRANSFORMATIONS_PREMISE",
                "what_is_derived": "bulk split and ADM Noether identities",
                "what_remains": "global edge charges and noncompact boundary sectors",
            },
            {
                "row_id": "BOUND5188_14_same_frame",
                "object": "ordinary matter source/readout functor",
                "current_status": "ONE_COFRAME_PARENT_SIGNATURE",
                "what_is_derived": "all displayed GR/Maxwell source chains use e",
                "what_remains": "this universal functor is selected by the parent action, not forced by factorization alone",
            },
            {
                "row_id": "BOUND5188_15_second_order",
                "object": "two-derivative local kinetic selection",
                "current_status": "EXPLICIT_LOW_ENERGY_PREMISE",
                "what_is_derived": "Fierz-Pauli and nonlinear EH uniqueness in the leading local sector",
                "what_remains": "controlled C3/CFF/nonlocal/p8plus terms outside the leading sector",
            },
            {
                "row_id": "BOUND5188_16_foliation",
                "object": "ADM motion-time-space dictionary",
                "current_status": "LOCAL_FOLIATED_REWRITE",
                "what_is_derived": "Gauss-Codazzi action, constraints and two-mode count",
                "what_remains": "generic non-hypersurface-orthogonal congruences require the full coframe formulation",
            },
        ]
    )


def build_provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, (path, expected_hash) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_locked",
                "source": str(path),
                "sha256": source_hashes[source_id],
                "expected_sha256": expected_hash,
                "role": "prior MTS theorem, obstruction or retained limit chain",
            }
        )
    for source_id, url in EXTERNAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "external_primary_or_author_reprint",
                "source": url,
                "sha256": "",
                "expected_sha256": "",
                "role": "massless spin-two, ADM or nonlinear consistency theorem context",
            }
        )
    return tagged(rows)


def build_document(result: dict[str, Any]) -> None:
    rank = result["rank_and_invariance"]
    scalar = result["scalar_clock_no_go"]
    fp = result["Fierz_Pauli"]
    adm = result["ADM"]
    witness = result["witnesses"]
    action = result["action_chain"]
    text = f"""# 5188 - Relational-clock scalar no-go, minimal coframe parent and Fierz-Pauli selection theorem

Marker: `{MARKER}`

Checked: `{CHECKED_DATE}`

Status: private analytic and source-executed checkpoint. No GitHub action.

## 1. Verdict

This checkpoint takes the foundational route selected by 5187 and gets a
definite answer rather than creating another missing-input queue.

Four scalar clocks/rods are enough to span ten metric variations at one
point, but that fact is **not** enough to generate gravity. With a constant
internal Lorentz metric,

```text
J^A_m = partial_m X^A,
g_mn  = eta_AB J^A_m J^B_n,
det(g)=-(det J)^2.
```

There are only two branches:

```text
det(J) != 0  -> X^A are local coordinates and g=X^*eta is exactly flat;
det(J)  = 0  -> det(g)=0 and the candidate metric is degenerate.
```

The executed nonlinear witness `X=(t,exp(x),y,z)` gives
`g=diag(-1,exp(2x),1,1)` and `R={scalar['nonlinear_pullback_sample_R']}`.
Therefore a scalar-clock-only parent cannot own generic curved GR.

The minimal repair is a genuinely non-scalar relational coframe distortion:

```text
e^a_m = E^a_A(x) partial_m X^A,
g_mn  = eta_ab e^a_m e^b_n,
H^mn  = sqrt(-g) g^mn.
```

For every nondegenerate coframe and every invertible `J`,
`E=e J^-1`; the map is exactly surjective. This is not a derivation of `E`
from the old one-scalar corpus. It is the smallest honest parent extension
that can carry curvature.

## 2. What earlier routes become

The construction keeps, but sharpens, the useful earlier work:

- checkpoint 787's four-field rank result is correct but only pointwise;
- checkpoint 788's flat-pullback warning is now an exact dichotomy;
- checkpoint 1963's owned-coframe action becomes a concrete relational
  factorization rather than a free symbol;
- the additive `e=dX+A` work is replaced by the multiplicative,
  exactly-surjective `e=E dX` map;
- checkpoint 2048's `T,S` coframe is a static spherical reduction;
- checkpoint 3846's `g=h-c_*^2 tau tau` bridge is the invariant
  time/space decomposition of the same coframe;
- checkpoint 4961's one-scalar rank obstruction remains valid;
- checkpoint 5187's independent integrated `H` can be replaced, inside this
  candidate, by the full-rank coframe composite `H[e]`.

No corpus search found an already parent-owned full-rank MTS field that could
be identified with `E`. That absence is not hidden: `E`, or equivalently the
time one-form plus spatial triad, is new non-scalar parent data.

## 3. Exact factorization and gauge ranks

At `E=J=I`,

```text
(delta E,delta J) -> delta e = delta E+delta J:
rank={rank['split_to_e_rank']}, nullity={rank['split_to_e_nullity']};

delta e -> delta g:
rank={rank['e_to_metric_rank']}, nullity={rank['e_to_metric_nullity']};

(delta E,delta J) -> delta g:
rank={rank['split_to_metric_rank']}, nullity={rank['split_to_metric_nullity']};

delta e -> delta H:
rank={rank['e_to_H_rank']}, nullity={rank['e_to_H_nullity']}.
```

The six `e->g` null directions are precisely local Lorentz frame rotations.
The sixteen first-jet split null directions express the redundancy between
`E` and `dX`; locally they come from four relational relabelling functions
and their derivatives.

The runner verifies with exact rational matrices that

```text
J -> S J, E -> E S^-1       leaves e exactly invariant;
E -> Lambda E, Lambda^T eta Lambda=eta
                              leaves g and H exactly invariant;
det(g)=-(det E det J)^2.
```

Thus the candidate loses no metric or Hilbert-source direction and does not
introduce a second observable frame.

## 4. Motion, time and space become an exact dictionary

The coframe gives the non-metaphorical MTS variables

```text
time:   tau = e^0/c_*;
space:  h_mn = sum_i e^i_m e^i_n,  rank(h)=3,  h_mn u^n=0;
motion: u and K_ij=(1/2) L_u h_ij;
metric: g_mn=h_mn-c_*^2 tau_m tau_n.
```

On a foliation `tau=N dt`, Einstein-Hilbert is exactly, up to the standard
boundary term,

```text
S_EH=(M_R^2/2) int dt d3x N sqrt(h)
     [R3+K_ij K^ij-K^2-2 Lambda_cal].
```

This is a precise version of "space evolving through time": `K_ij` is the
motion of spatial geometry. Its momentum is

```text
pi^ij=M_R^2 sqrt(h)(K^ij-K h^ij).
```

The executed DeWitt kinetic form has rank `{adm['dewitt_rank']}` and inertia
`({adm['dewitt_positive']}+, {adm['dewitt_negative']}-, {adm['dewitt_zero']}0)`.
Lapse and shift impose one Hamiltonian and three momentum constraints.
The exact configuration-space degree count is

```text
(12-2*4)/2={adm['physical_spin2_configuration_dof']},
```

the two massless spin-two polarizations. The constrained conformal direction
is visible rather than mistaken for a propagating ghost.

If the action depends on `E` and `X` only through `e`, with
`E_e,a^m=delta S/delta e^a_m`,

```text
delta S/delta E^a_A = E_e,a^m J^A_m,
delta S/delta X^A   = -partial_m(E_e,a^m E^a_A).
```

Invertible `J` makes the `X` equation a differential consequence of the
coframe equation. The relational split adds no physical pole. Separate
`X`- or `E`-kinetic terms not reducible to `e` would break this theorem and
must be independently constrained; they are excluded from the minimal parent.

## 5. The spin-two kinetic term is selected, not inserted

Write the most general local Lorentz-invariant quadratic two-derivative
action for a symmetric field as

```text
L=a (partial h_mn)^2
 +b (partial_m h^mn)(partial^r h_rn)
 +c (partial_m h^mn) partial_n h
 +d (partial h)^2.
```

Requiring invariance under
`delta h_mn=partial_m xi_n+partial_n xi_m` gives an exact rational
`{fp['constraint_row_count']} x 4` constraint matrix. The runner finds

```text
rank={fp['constraint_rank']},
nullity={fp['constraint_nullity']},
kernel=(1,-2,2,-1).
```

The positive-residue convention is

```text
L_FP=-1/2 L1+L2-L3+1/2 L4.
```

So the massless spin-two Hessian is unique up to the one overall
normalization `M_R^2`; it is not chosen coefficient by coefficient.
Checkpoint 4960's local consistency/self-coupling theorem then gives the
Einstein interaction at two derivatives, up to field redefinitions,
boundary/topological terms and `Lambda_cal`. Controlled higher-derivative
and nonlocal operators remain in the 5187 EFT corridor.

## 6. Curved and weak-field witnesses

The construction is not merely formal:

```text
FLRW e=diag(1,a,a,a):
R={witness['FLRW_Ricci_scalar']};

a=exp(Ht):
R={witness['de_Sitter_Ricci_scalar']};

weak static e^0_0=1+Phi, e^i_j=(1-Phi)delta^i_j:
g00=-(1+2Phi)+O(Phi^2),
gij=(1-2Phi)deltaij+O(Phi^2),
gamma=1.
```

The independently executed linearized Einstein tensor is

```text
G00={witness['linearized_Einstein_G00']}.
```

Therefore

```text
M_R^2 G00=rho
-> nabla^2 Phi=rho/(2M_R^2)=4 pi G_N rho,
G_N=1/(8 pi M_R^2).
```

The same metric gives `d2x/dt2=-grad(Phi)` for slow bodies and the
`gamma=1` null/lensing branch. No separate Newton or light coefficient is
introduced.

## 7. One parent action carries GR and electromagnetism

The minimal local candidate is

```text
{PARENT_ACTION}.
```

Its consequences retain the source-executed 5187 chains:

```text
Einstein/Newton chain retained = {action['prior_GR_Newton_chain']};
Maxwell/Poynting chain retained = {action['prior_Maxwell_Poynting_chain']};
universal spin-two residue      = {action['prior_universal_residue']}.
```

`F=dA` and the Maxwell Hodge star use the same coframe. Variation gives

```text
nabla_m(Z_A F^mn)=J^n,
m u.nabla u^m=q F^m_n u^n,
T_EM,mn=Z_A(F_ma F_n^a-g_mn F^2/4),
T_EM^0i=Z_A(E cross B)^i=(E_c cross B_c)^i.
```

The local orthonormal-frame stress calculation is also executed directly:
`F^2={action['canonical_Maxwell_F2']}`,
`T^00={action['canonical_Maxwell_energy_density']}`,
`T^0i={action['canonical_Poynting_vector']}`, and
`trace(T)={action['canonical_Maxwell_stress_trace']}`.

The Poynting vector is therefore not a separate background field. It is the
energy flux of the Maxwell field measured by the same time/space coframe.
This directly addresses the earlier question about whether electromagnetic
flow acts on the background geometry: it sources the coframe through its
Hilbert stress tensor.

The `U(1)` representation and charge spectrum remain visible parent content;
the coframe construction does not derive them.

## 8. Honest boundary

Derived now:

- scalar-clock-only curved geometry is rejected exactly;
- the minimal relational coframe map is exact and surjective;
- integrated `H` is a rank-ten coframe composite in this candidate;
- relational split and Lorentz redundancies are exact;
- the e-only split adds no extra physical mode;
- the ADM motion/time/space dictionary and two-mode count close;
- massless spin-two gauge symmetry uniquely fixes the Fierz-Pauli ratios;
- the 5187 Einstein/Newton and Maxwell/Poynting chains survive unchanged.

Still parent data or open:

- the non-scalar distortion `E`, or equivalently `tau,h,u/K`, is not derived
  from the old scalar MTS corpus;
- spacetime Diff is realized exactly by the parent construction but is not
  manufactured by one scalar;
- visible `U(1)` representations and charge assignments remain parent data;
- the absolute gravitational scale still needs one calibration;
- physical total `c_IR`, nonlocal and complete `p8+` amplitudes remain open;
- the factorization is local to patches with `det(E)det(J)!=0`; global
  relational-chart caustics, topology and nonproper edge charges are not
  solved here;
- the no-extra-split-mode theorem requires every leading `E,X` dependence to
  factor through `e`; any direct split-breaking operator reopens the mode
  count;
- this is not a full unification or all-operator compact-GR claim.

The correct ontology decision is now sharp. A serious MTS parent must either
take the coframe/time-space-motion package as fundamental or derive it from a
genuinely non-scalar microscopic sector. Returning to a one-scalar metric
bootstrap is mathematically closed.

## 9. Next target

Checkpoint 5189 should not repeat the rank audit. It should project the
surviving MTS motion variables into the exact coframe/ADM invariants
`tau`, `h_ij`, `u`, `K`, and the traceless shear `sigma_ij`, then test whether
one parent motion Hessian:

1. preserves the four ADM constraints and the two local spin-two modes;
2. is reflection-even and source-silent on the compact local branch;
3. supplies the cosmology/galaxy response without changing `G_N` or
   `gamma=1` by arena.

If no such map exists, the coframe remains fundamental and the old motion
sector is retained honestly as controlled stress/exchange matter.

## 10. Artifacts and integrity

Generated evidence:

- `source-intake/functional_rg/5188/prior_relational_parent_supersession.csv`
- `source-intake/functional_rg/5188/scalar_clock_pullback_no_go.csv`
- `source-intake/functional_rg/5188/minimal_relational_coframe_factorization.csv`
- `source-intake/functional_rg/5188/coframe_H_rank_and_invariance.csv`
- `source-intake/functional_rg/5188/Fierz_Pauli_gauge_nullspace.csv`
- `source-intake/functional_rg/5188/MTS_ADM_dictionary_and_mode_count.csv`
- `source-intake/functional_rg/5188/curved_and_weak_field_witnesses.csv`
- `source-intake/functional_rg/5188/same_coframe_GR_Newton_Maxwell_chain.csv`
- `source-intake/functional_rg/5188/parent_upgrade_claim_boundary.csv`
- `source-intake/functional_rg/5188/source_provenance.csv`
- `source-intake/functional_rg/5188/relational_coframe_parent_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5188_VALIDATION.csv`

Claim guard:

`{CLAIM_GUARD}`

The formalization workbench and checkpoint-5176 ensemble remain locked.
No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def calculate_validations(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_5176_before: str,
    scalar: dict[str, Any],
    rank: dict[str, Any],
    fp: dict[str, Any],
    adm: dict[str, Any],
    witness: dict[str, Any],
    action: dict[str, Any],
    boundary_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append(
            validation_row(
                f"V5188_{len(checks):02d}",
                check,
                passed,
                observed,
                expected,
            )
        )

    add(
        "all locked local source files exist",
        all(path.is_file() for path, _ in SOURCES.values()),
        sum(path.is_file() for path, _ in SOURCES.values()),
        len(SOURCES),
    )
    add(
        "all locked local source hashes match",
        all(
            source_hashes[source_id] == expected
            for source_id, (_, expected) in SOURCES.items()
        ),
        sum(
            source_hashes[source_id] == expected
            for source_id, (_, expected) in SOURCES.items()
        ),
        len(SOURCES),
    )
    add(
        "formalization workbench lock holds before generation",
        formal_before == FORMAL_DIGEST_LOCK,
        formal_before,
        FORMAL_DIGEST_LOCK,
    )
    add(
        "checkpoint 5176 lock holds before generation",
        checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
        checkpoint_5176_before,
        CHECKPOINT_5176_TREE_LOCK,
    )
    add(
        "four-scalar first-jet metric rank is ten",
        scalar["four_scalar_first_jet_metric_rank"] == 10,
        scalar["four_scalar_first_jet_metric_rank"],
        10,
    )
    add(
        "nonlinear invertible scalar pullback has zero Ricci scalar",
        scalar["nonlinear_pullback_sample_R"] == "0",
        scalar["nonlinear_pullback_sample_R"],
        0,
    )
    add(
        "invertible constant-internal scalar branch is flat",
        scalar["invertible_constant_internal_metric_is_flat"],
        scalar["invertible_constant_internal_metric_is_flat"],
        True,
    )
    add(
        "rank-deficient scalar branch is degenerate",
        scalar["rank_deficient_branch_is_degenerate"],
        scalar["rank_deficient_branch_is_degenerate"],
        True,
    )
    add(
        "split factorization covers all coframe directions",
        rank["split_to_e_rank"] == 16,
        rank["split_to_e_rank"],
        16,
    )
    add(
        "split first-jet map has sixteen null directions",
        rank["split_to_e_nullity"] == 16,
        rank["split_to_e_nullity"],
        16,
    )
    add(
        "coframe to metric map has rank ten",
        rank["e_to_metric_rank"] == 10,
        rank["e_to_metric_rank"],
        10,
    )
    add(
        "coframe to metric map has six Lorentz null directions",
        rank["e_to_metric_nullity"] == 6,
        rank["e_to_metric_nullity"],
        6,
    )
    add(
        "coframe to H map has rank ten",
        rank["e_to_H_rank"] == 10,
        rank["e_to_H_rank"],
        10,
    )
    add(
        "coframe to H map has six Lorentz null directions",
        rank["e_to_H_nullity"] == 6,
        rank["e_to_H_nullity"],
        6,
    )
    add(
        "split to metric map has rank ten",
        rank["split_to_metric_rank"] == 10,
        rank["split_to_metric_rank"],
        10,
    )
    add(
        "determinant identity holds exactly",
        rank["determinant_identity_residual"],
        rank["determinant_identity_residual"],
        True,
    )
    add(
        "relational relabelling leaves coframe invariant",
        rank["relabel_invariance_exact"],
        rank["relabel_invariance_exact"],
        True,
    )
    add(
        "rational boost obeys Lorentz condition",
        rank["lorentz_condition_exact"],
        rank["lorentz_condition_exact"],
        True,
    )
    add(
        "local Lorentz transformation leaves metric invariant",
        rank["metric_lorentz_invariance_exact"],
        rank["metric_lorentz_invariance_exact"],
        True,
    )
    add(
        "local Lorentz transformation leaves H invariant",
        rank["H_lorentz_invariance_exact"],
        rank["H_lorentz_invariance_exact"],
        True,
    )
    add(
        "Fierz-Pauli constraint matrix has rank three",
        fp["constraint_rank"] == 3,
        fp["constraint_rank"],
        3,
    )
    add(
        "Fierz-Pauli coefficient space has nullity one",
        fp["constraint_nullity"] == 1,
        fp["constraint_nullity"],
        1,
    )
    add(
        "Fierz-Pauli kernel has the unique expected ratios",
        fp["normalized_null_vector"] == fp["expected_vector"],
        fp["normalized_null_vector"],
        fp["expected_vector"],
    )
    add(
        "Fierz-Pauli gauge residual is exactly zero",
        fp["gauge_residual_exact_zero"],
        fp["gauge_residual_exact_zero"],
        True,
    )
    add(
        "ADM DeWitt kinetic form has rank six",
        adm["dewitt_rank"] == 6,
        adm["dewitt_rank"],
        6,
    )
    add(
        "ADM DeWitt inertia is five positive and one negative",
        (adm["dewitt_positive"], adm["dewitt_negative"], adm["dewitt_zero"])
        == (5, 1, 0),
        (adm["dewitt_positive"], adm["dewitt_negative"], adm["dewitt_zero"]),
        (5, 1, 0),
    )
    add(
        "ADM first-class degree count leaves two spin-two modes",
        adm["physical_spin2_configuration_dof"] == 2,
        adm["physical_spin2_configuration_dof"],
        2,
    )
    add(
        "FLRW coframe gives expected Ricci scalar",
        witness["FLRW_Ricci_scalar"]
        == "6*(a(t)*Derivative(a(t), (t, 2)) + Derivative(a(t), t)**2)/a(t)**2",
        witness["FLRW_Ricci_scalar"],
        "6*(a a_ddot+a_dot^2)/a^2",
    )
    add(
        "de Sitter witness gives R=12 H^2",
        witness["de_Sitter_Ricci_scalar"] == "12*H**2",
        witness["de_Sitter_Ricci_scalar"],
        "12*H**2",
    )
    add(
        "weak coframe fixes PPN gamma to one",
        witness["PPN_gamma"] == 1,
        witness["PPN_gamma"],
        1,
    )
    add(
        "linearized Einstein 00 component is twice the spatial Laplacian",
        witness["linearized_Einstein_G00_equals_2_laplacian"],
        witness["linearized_Einstein_G00_equals_2_laplacian"],
        True,
    )
    add(
        "checkpoint 5187 GR/Newton chain is retained",
        action["prior_GR_Newton_chain"],
        action["prior_GR_Newton_chain"],
        True,
    )
    add(
        "checkpoint 5187 Maxwell/Poynting chain is retained",
        action["prior_Maxwell_Poynting_chain"],
        action["prior_Maxwell_Poynting_chain"],
        True,
    )
    add(
        "checkpoint 5187 universal spin-two residue is retained",
        action["prior_universal_residue"],
        action["prior_universal_residue"],
        True,
    )
    add(
        "canonical Maxwell energy density is exact",
        action["canonical_Maxwell_energy_exact"],
        action["canonical_Maxwell_energy_density"],
        action["canonical_Maxwell_energy_expected"],
    )
    add(
        "canonical Maxwell Poynting vector is exactly E cross B",
        action["canonical_Poynting_exact"],
        action["canonical_Poynting_vector"],
        action["canonical_Poynting_expected"],
    )
    add(
        "canonical Maxwell stress is traceless",
        action["canonical_Maxwell_stress_trace"] == "0",
        action["canonical_Maxwell_stress_trace"],
        0,
    )
    add(
        "claim boundary contains explicit full-unification nonclaim",
        any(
            row["object"] == "full MTS fundamental theory"
            and row["current_status"] == "NOT_CLAIMED"
            for row in boundary_rows
        ),
        True,
        True,
    )
    add(
        "claim boundary identifies non-scalar parent extension",
        any(
            row["object"] == "parent ontology"
            and row["current_status"] == "MINIMAL_EXTENSION_REQUIRED"
            for row in boundary_rows
        ),
        True,
        True,
    )
    add(
        "no-extra-mode theorem is explicitly gated by e-only dependence",
        any(
            row["object"] == "no-extra-split-mode premise"
            and row["current_status"] == "EXACT_IF_E_ONLY"
            for row in boundary_rows
        ),
        True,
        True,
    )
    add(
        "local relational patch and global caustic boundary are explicit",
        any(
            row["object"] == "relational chart domain"
            and row["current_status"] == "LOCAL_NONDEGENERATE_BRANCH_ONLY"
            for row in boundary_rows
        ),
        True,
        True,
    )
    add(
        "same-frame matter functor remains an explicit parent signature",
        any(
            row["object"] == "ordinary matter source/readout functor"
            and row["current_status"] == "ONE_COFRAME_PARENT_SIGNATURE"
            for row in boundary_rows
        ),
        True,
        True,
    )
    add(
        "all boundary rows remain invalid for a full MTS claim",
        all(not row["valid_for_full_MTS_claim"] for row in boundary_rows),
        sum(not row["valid_for_full_MTS_claim"] for row in boundary_rows),
        len(boundary_rows),
    )
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_hashes: dict[str, str] = {}
    for source_id, (path, _) in SOURCES.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        source_hashes[source_id] = file_digest(path)

    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    result_5187 = json.loads(
        SOURCES["checkpoint_5187_result"][0].read_text(encoding="utf-8")
    )
    prior_rows = build_prior_rows()
    rank_rows, rank_metrics = build_rank_metrics()
    scalar_rows, scalar_metrics = build_scalar_rows(rank_metrics)
    factor_rows = build_factor_rows()
    fp_rows, fp_metrics = build_fp_rows()
    adm_rows, adm_metrics = build_adm_rows()
    witness_rows, witness_metrics = build_witness_rows()
    action_rows, action_metrics = build_action_rows(result_5187)
    boundary_rows = build_boundary_rows()
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        scalar_metrics,
        rank_metrics,
        fp_metrics,
        adm_metrics,
        witness_metrics,
        action_metrics,
        boundary_rows,
    )
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(
            "Pre-write validation failed:\n" + json.dumps(failures, indent=2)
        )

    outputs = {
        PRIOR_CSV: prior_rows,
        SCALAR_CSV: scalar_rows,
        FACTOR_CSV: factor_rows,
        RANK_CSV: rank_rows,
        FP_CSV: fp_rows,
        ADM_CSV: adm_rows,
        WITNESS_CSV: witness_rows,
        ACTION_CSV: action_rows,
        BOUNDARY_CSV: boundary_rows,
        PROVENANCE_CSV: provenance_rows,
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    data_pack_digest = hashlib.sha256()
    for path in outputs:
        data_pack_digest.update(path.name.encode("utf-8"))
        data_pack_digest.update(file_digest(path).encode("ascii"))

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "leading_theorem": LEADING_THEOREM,
        "claim_guard": CLAIM_GUARD,
        "parent_action": PARENT_ACTION,
        "scalar_clock_no_go": scalar_metrics,
        "rank_and_invariance": rank_metrics,
        "Fierz_Pauli": fp_metrics,
        "ADM": adm_metrics,
        "witnesses": witness_metrics,
        "action_chain": action_metrics,
        "claim_status": {
            "scalar_clock_only_curved_GR_rejected": True,
            "minimal_relational_coframe_constructed": True,
            "coframe_map_surjective": True,
            "integrated_H_is_coframe_composite_inside_candidate": True,
            "relational_split_no_extra_mode_if_e_only": True,
            "Fierz_Pauli_ratios_unique": True,
            "ADM_two_mode_count": True,
            "leading_local_GR_Newton_inside_parent": True,
            "flat_Maxwell_Poynting_inside_parent": True,
            "non_scalar_E_derived_from_old_scalar_MTS": False,
            "Diff_generated_by_old_scalar": False,
            "visible_U1_representations_derived": False,
            "absolute_GN_predicted": False,
            "full_MTS_unification": False,
            "GitHub_action": False,
        },
        "source_hashes": source_hashes,
        "external_sources": EXTERNAL_SOURCES,
        "data_pack_sha256": data_pack_digest.hexdigest(),
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_5176_before,
        "validation_count_prewrite": len(checks),
        "validation_failures_prewrite": 0,
    }
    write_json(RESULT_JSON, result)
    build_document(result)

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    expected_outputs = tuple(outputs) + (RESULT_JSON, DOCUMENT)

    final_checks = checks + [
        validation_row(
            f"V5188_{len(checks):02d}",
            "formalization workbench remains unchanged after writes",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            f"V5188_{len(checks) + 1:02d}",
            "checkpoint 5176 remains unchanged after writes",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            f"V5188_{len(checks) + 2:02d}",
            "all checkpoint artifacts exist and are nonempty",
            all(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            sum(path.is_file() and path.stat().st_size > 0 for path in expected_outputs),
            len(expected_outputs),
        ),
        validation_row(
            f"V5188_{len(checks) + 3:02d}",
            "all generated CSV files parse with at least one row",
            all(len(read_csv(path)) > 0 for path in outputs),
            sum(len(read_csv(path)) > 0 for path in outputs),
            len(outputs),
        ),
        validation_row(
            f"V5188_{len(checks) + 4:02d}",
            "no GitHub action is recorded",
            result["claim_status"]["GitHub_action"] is False,
            result["claim_status"]["GitHub_action"],
            False,
        ),
    ]
    final_failures = [
        row for row in final_checks if row["status"] != "PASS"
    ]
    if final_failures:
        raise RuntimeError(
            "Final validation failed:\n"
            + json.dumps(final_failures, indent=2)
        )
    write_csv(VALIDATION_CSV, final_checks)

    print(
        json.dumps(
            {
                "checkpoint": 5188,
                "marker": MARKER,
                "validation_passed": len(final_checks),
                "validation_failed": 0,
                "scalar_clock_only_curved_GR_rejected": True,
                "four_scalar_point_rank": scalar_metrics[
                    "four_scalar_first_jet_metric_rank"
                ],
                "coframe_to_metric_rank": rank_metrics[
                    "e_to_metric_rank"
                ],
                "coframe_to_H_rank": rank_metrics["e_to_H_rank"],
                "Fierz_Pauli_rank": fp_metrics["constraint_rank"],
                "Fierz_Pauli_nullity": fp_metrics[
                    "constraint_nullity"
                ],
                "Fierz_Pauli_vector": fp_metrics[
                    "normalized_null_vector"
                ],
                "ADM_physical_modes": adm_metrics[
                    "physical_spin2_configuration_dof"
                ],
                "FLRW_R": witness_metrics["FLRW_Ricci_scalar"],
                "de_Sitter_R": witness_metrics[
                    "de_Sitter_Ricci_scalar"
                ],
                "document": str(DOCUMENT),
                "result": str(RESULT_JSON),
                "validation": str(VALIDATION_CSV),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
