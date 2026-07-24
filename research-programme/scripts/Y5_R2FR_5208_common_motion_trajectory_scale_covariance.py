from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np
import sympy as sp
from scipy import constants, optimize


CHECKPOINT = 5208
MARKER = "MTS_5208_COMMON_MINIMAL_MOTION_TRAJECTORY_SCALE_COVARIANCE"
CHECKED_DATE = "2026-07-24"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5208-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-"
    "absolute-scale-covariance-and-local-GR-selection.md"
)
PUBLIC = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")
PUBLIC_HEAD = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD = "f850e4997657f457dddc05cbe50f21186588dcc7"
GALAXY_DIRTY = [
    " M scripts/mts-failure-lab.py",
    "?? scripts/mts_axisymmetric_phase.py",
    "?? scripts/mts_nonanalytic_phase.py",
    "?? scripts/mts_phase_flow_closure.py",
    "?? scripts/mts_phase_lensing_gate.py",
    "?? scripts/mts_self_similar_phase_disk.py",
]
FORMAL_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PRIMARY_N_WITH_LOCAL = 1646
LAMBDA4_QUADRATIC_CEILING = 3.582022879940714e-122

SOURCE_LOCKS = {
    POST
    / "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-"
    "GR-connected-trajectory-or-even-pair-sector-rejection.md": (
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131"
    ),
    POST
    / "scripts"
    / "Y5_R2FR_4951_coupled_VFZX2_fixed_and_running_gate.py": (
        "c6093a904d20c74c71443866b4ecf3ac4e125c394971065b5252f3b45bc52f9d"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4951"
    / "coupled_VFZX2_fixed_and_running_gate_results.json": (
        "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c"
    ),
    POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-"
    "2to4-amplitude-or-rate-route-rejection.md": (
        "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c"
    ),
    POST
    / "scripts"
    / "Y5_R2FR_4958_essential_PX_sixpoint_trajectory.py": (
        "521ffed6f208cf4c0db3fd596643fc0970f34e1050de71ab65e37c44906ff77f"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_PX_sixpoint_trajectory_results.json": (
        "383e13cd13c3e90be22dbf8ad589c756a26cad002f01da4ce151ad262e48ae67"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv": (
        "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081"
    ),
    POST
    / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-"
    "two-scale-theory-gate.md": (
        "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4"
    ),
    POST
    / "5204-Y5-R2FR-curvature-triggered-homogeneous-motion-state-local-PPN-Gdot-"
    "and-preparation-no-overlap-theorem.md": (
        "8923d9fac23289f1923659ac3352aa216ad89c1985140c01e1d9ed1907d7c535"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5204"
    / "curvature_triggered_motion_state_results.json": (
        "341abeb003983ab9593137983e792e4007742d1f46c17e95b194a5fb827c382a"
    ),
    POST
    / "5205-Y5-R2FR-normalized-CTP-regular-mode-ensemble-Hamiltonian-constraint-"
    "and-zero-Lambda-second-moment-selection-theorem.md": (
        "2563092d1eb5ede72275042bec70d70f79f7f98db371d5a710f681d59a38af50"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5205"
    / "normalized_CTP_regular_mode_state_results.json": (
        "08bc87ff2feefdf05d35a4df4836e55c9a4dd9eeeb3b7eff72c0960112400537"
    ),
    POST
    / "5207-Y5-R2FR-Cavendish-normalized-parent-scale-observed-density-map-and-"
    "self-consistent-source-calibrated-refit.md": (
        "8d0b856b7d53bc6b762ff8278eed98999e80079c948d47436db92bfd84bdfb32"
    ),
    POST
    / "scripts"
    / "Y5_R2FR_5207_Cavendish_source_calibrated_refit.py": (
        "9a130cb1f1fbb7c7188c5e73aeffe9e36eca6f4f6409db02abf9299b492f8e61"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5207"
    / "Cavendish_source_calibrated_results.json": (
        "a322ddacd011a47cfa288bf832ff953ab8a4c349d24bf2e03066b9ebfa1e24d8"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5207_VALIDATION.csv": (
        "24998ad798103351d38071920cd8ba4a47c22ae635f9264e0636b861fb117d6d"
    ),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


checkpoint_5207 = load_module(
    "mts_checkpoint_5207_for_5208",
    POST / "scripts" / "Y5_R2FR_5207_Cavendish_source_calibrated_refit.py",
)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def selected_digest(paths: list[Path], base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(file_digest(path).encode("ascii"))
    return digest.hexdigest()


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            allow_nan=False,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_cosmology_support_claim": False,
            "valid_for_full_MTS_claim": False,
            **row,
        }
        for row in rows
    ]


def git_state(repository: Path) -> tuple[str, list[str]]:
    safe = repository.as_posix()
    head = subprocess.run(
        ["git", "-c", f"safe.directory={safe}", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe}",
            "-C",
            str(repository),
            "status",
            "--porcelain=v1",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return head, status


def assert_source_locks() -> None:
    missing = [str(path) for path in SOURCE_LOCKS if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing locked sources: {missing}")
    mismatched = {
        str(path): {"expected": expected, "actual": file_digest(path)}
        for path, expected in SOURCE_LOCKS.items()
        if file_digest(path) != expected
    }
    if mismatched:
        raise RuntimeError(f"source lock mismatch: {mismatched}")


def canonical_field_quotient() -> tuple[list[dict[str, Any]], dict[str, str]]:
    chi = sp.symbols("chi", real=True)
    z0 = sp.symbols("Z0", positive=True)
    z2, mass2, lambda4, xi2, f4, c_x2 = sp.symbols(
        "z2 mass2 lambda4 xi2 f4 c_X2", real=True
    )
    psi = chi / sp.sqrt(z0) - z2 * chi**3 / (12 * z0 ** sp.Rational(5, 2))
    z_function = z0 + z2 * psi**2 / 2
    kinetic_residual = sp.expand(
        sp.series(z_function * sp.diff(psi, chi) ** 2 - 1, chi, 0, 4).removeO()
    )
    potential = mass2 * psi**2 / 2 + lambda4 * psi**4 / 24
    curvature = xi2 * psi**2 / 2 + f4 * psi**4 / 24
    potential_canonical = sp.expand(sp.series(potential, chi, 0, 6).removeO())
    curvature_canonical = sp.expand(sp.series(curvature, chi, 0, 6).removeO())
    mass2_canonical = sp.simplify(sp.diff(potential_canonical, chi, 2).subs(chi, 0))
    lambda4_canonical = sp.simplify(
        sp.diff(potential_canonical, chi, 4).subs(chi, 0)
    )
    xi2_canonical = sp.simplify(
        sp.diff(curvature_canonical, chi, 2).subs(chi, 0)
    )
    f4_canonical = sp.simplify(
        sp.diff(curvature_canonical, chi, 4).subs(chi, 0)
    )
    c_x2_canonical = sp.simplify(c_x2 / z0**2)
    expected_mass = mass2 / z0
    expected_lambda = lambda4 / z0**2 - 2 * mass2 * z2 / z0**3
    expected_xi = xi2 / z0
    expected_f4 = f4 / z0**2 - 2 * xi2 * z2 / z0**3
    checks = {
        "kinetic_residual": str(sp.simplify(kinetic_residual)),
        "mass_residual": str(sp.simplify(mass2_canonical - expected_mass)),
        "quartic_residual": str(
            sp.simplify(lambda4_canonical - expected_lambda)
        ),
        "curvature_quadratic_residual": str(
            sp.simplify(xi2_canonical - expected_xi)
        ),
        "curvature_quartic_residual": str(
            sp.simplify(f4_canonical - expected_f4)
        ),
        "canonical_c_X2": str(c_x2_canonical),
    }
    rows = tagged(
        [
            {
                "item": "canonical_field_coordinate",
                "input": "dchi/dpsi=sqrt(Z(psi)); Z(psi)>0",
                "derived_output": (
                    "psi=chi/sqrt(Z0)-z2 chi^3/(12 Z0^(5/2))+O(chi^5)"
                ),
                "status": "EXACT_LOCAL_FIELD_COORDINATE",
                "meaning": "positive Z is inessential for a single scalar",
            },
            {
                "item": "canonical_kinetic_germ",
                "input": "Z=Z0+z2 psi^2/2+O(psi^4)",
                "derived_output": "Z(psi)(dpsi/dchi)^2=1+O(chi^4)",
                "status": "EXACT_ZERO_THROUGH_DISPLAYED_ORDER",
                "meaning": "z2 is absorbed into canonical invariant couplings",
            },
            {
                "item": "canonical_pole_mass",
                "input": "mass2,Z0",
                "derived_output": str(mass2_canonical),
                "status": "DERIVED_INVARIANT",
                "meaning": "m_pole^2=V''(0)/Z0",
            },
            {
                "item": "canonical_quartic",
                "input": "lambda4,mass2,z2,Z0",
                "derived_output": str(lambda4_canonical),
                "status": "DERIVED_INVARIANT",
                "meaning": "field-dependent Z shifts the canonical quartic",
            },
            {
                "item": "canonical_curvature_quadratic",
                "input": "xi2,Z0",
                "derived_output": str(xi2_canonical),
                "status": "DERIVED_INVARIANT",
                "meaning": "zeta_c=xi2/(2 Z0)",
            },
            {
                "item": "canonical_curvature_quartic",
                "input": "f4,xi2,z2,Z0",
                "derived_output": str(f4_canonical),
                "status": "DERIVED_INVARIANT",
                "meaning": "F_R and Z cannot be counted as independent germs",
            },
            {
                "item": "canonical_X2_coefficient",
                "input": "c_X2,Z0",
                "derived_output": str(c_x2_canonical),
                "status": "DERIVED_INVARIANT",
                "meaning": "c_X2,can=c_X2/Z0^2 at the origin",
            },
        ]
    )
    return rows, checks


def trajectory_theorems() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    g, w, c_x2, a_x2 = sp.symbols("g w c_X2 A_X2", real=True)
    beta_g = 2 * g
    beta_w = -2 * w
    beta_j = sp.simplify(beta_g * w + g * beta_w)
    beta_c = 4 * c_x2 + 16 * g**2
    beta_a = sp.solve(
        sp.Eq(beta_c, sp.symbols("beta_A") * g**2 + 2 * a_x2 * g * beta_g),
        sp.symbols("beta_A"),
    )[0].subs(c_x2, a_x2 * g**2)
    lambda4, xi = sp.symbols("lambda4 xi", real=True)
    beta_lambda = 3 * lambda4**2 / (16 * sp.pi**2)
    beta_xi = lambda4 * (xi - sp.Rational(1, 6)) / (16 * sp.pi**2)
    minimal_surface = [
        sp.simplify(beta_lambda.subs(lambda4, 0)),
        sp.simplify(beta_xi.subs({lambda4: 0, xi: 0})),
    ]
    stability = sp.Matrix(
        [
            [-4, -1 / (32 * sp.pi**2), 0, 0, 0],
            [0, -2, -1 / (32 * sp.pi**2), 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1 / (96 * sp.pi**2), 0, -2, -1 / (32 * sp.pi**2)],
            [0, 0, 1 / (96 * sp.pi**2), 0, 0],
        ]
    )
    eigenvalues = sorted(
        [
            float(sp.N(value))
            for value, multiplicity in stability.eigenvals().items()
            for _ in range(multiplicity)
        ]
    )
    mass_to_xi = sp.simplify(stability[4, 1])
    quartic_to_xi = sp.simplify(stability[4, 2])
    source_4951 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "4951"
            / "coupled_VFZX2_fixed_and_running_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    source_4958 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "4958"
            / "essential_PX_sixpoint_trajectory_results.json"
        ).read_text(encoding="utf-8")
    )
    flow_rows = tagged(
        [
            {
                "item": "Gaussian_IR_Newton_mass_invariant",
                "equations": "beta_g=2g; beta_w=-2w; J_gap=g w",
                "derived_result": f"beta_J={beta_j}",
                "status": "EXACT",
                "consequence": "J_gap=G_N m_gap^2 is scale invariant",
            },
            {
                "item": "essential_X2_weak_trajectory",
                "equations": "beta_c=4c+16g^2; c=A_X2 g^2",
                "derived_result": f"beta_A_X2={sp.simplify(beta_a)}",
                "status": "EXACT_IN_LOCKED_ESSENTIAL_SCHEME",
                "consequence": "A_X2=A_ref+16 ln(k/k_ref)",
            },
            {
                "item": "minimal_VF_surface",
                "equations": (
                    "beta_lambda=3lambda^2/(16pi^2); "
                    "beta_xi=lambda(xi-1/6)/(16pi^2)"
                ),
                "derived_result": f"beta_lambda|0={minimal_surface[0]}; beta_xi|0={minimal_surface[1]}",
                "status": "EXACT_FIXED_BACKGROUND_COMPARATOR",
                "consequence": "lambda=xi=0 is invariant in the free massive scalar limit",
            },
            {
                "item": "mass_eigenvector_to_curvature_coordinate",
                "equations": "Percacci-Vacca exact FP1 polynomial stability matrix",
                "derived_result": f"B_xi,m2={mass_to_xi}",
                "status": "EXACT_ZERO_IN_SOURCE_COMPARATOR",
                "consequence": "the relevant mass deformation does not linearly generate xi",
            },
            {
                "item": "quartic_to_curvature_coordinate",
                "equations": "Percacci-Vacca exact FP1 polynomial stability matrix",
                "derived_result": f"B_xi,lambda={quartic_to_xi}",
                "status": "EXACT_NONZERO_IN_SOURCE_COMPARATOR",
                "consequence": "a nonzero quartic requires the correlated curvature coordinate",
            },
            {
                "item": "parent_functional_X2_index",
                "equations": "checkpoint-4958 minimal-essential functional trajectory",
                "derived_result": (
                    "one GR-connected relevant direction in both N=6,N=8 schemes"
                ),
                "status": (
                    "PASS"
                    if source_4958["gates"]["one_GR_connected_relevant_direction"]
                    else "FAIL"
                ),
                "consequence": "X2 is trajectory-owned rather than a new relevant datum",
            },
            {
                "item": "parent_mass_and_quartic_indices",
                "equations": "checkpoint-4951 MTS potential projection",
                "derived_result": (
                    f"theta_mass={source_4951['parent_indices']['theta_mass']}; "
                    f"theta_quartic={source_4951['parent_indices']['theta_quartic']}"
                ),
                "status": "SOURCE_LOCKED",
                "consequence": "mass is relevant while the regular quartic is irrelevant",
            },
        ]
    )
    delta = sp.symbols("delta", real=True)
    scale_rows = tagged(
        [
            {
                "item": "autonomous_flow_translation",
                "transformation": "u_delta(k)=u(exp(-delta) k)",
                "Newton_scale": "G_N -> exp(-2 delta) G_N",
                "motion_scale": "m_gap -> exp(delta) m_gap",
                "invariant": "G_N m_gap^2 -> G_N m_gap^2",
                "status": "EXACT_SCALE_COVARIANCE",
                "consequence": "an autonomous dimensionless RG flow cannot select an absolute unit",
            },
            {
                "item": "reduced_Newton_scale",
                "transformation": "M_N=(8pi G_N)^(-1/2) -> exp(delta) M_N",
                "Newton_scale": "one dimensional integration constant",
                "motion_scale": "m_gap/M_N invariant",
                "invariant": "J_gap",
                "status": "ABSOLUTE_SCALE_NO_GO",
                "consequence": "measured G_N is legitimate input, not an unfinished beta-function number",
            },
            {
                "item": "trajectory_parameter_count",
                "transformation": "gravity relevant direction plus mass relevant direction",
                "Newton_scale": "G_N",
                "motion_scale": "J_gap or m_gap/M_N",
                "invariant": "two essential scales before vacuum branch choice",
                "status": "DERIVED_TWO_SCALE_THEORY",
                "consequence": "no arena-specific mass or Newton retuning is allowed",
            },
        ]
    )
    symbolic = {
        "beta_J_gap": str(beta_j),
        "beta_A_X2": str(sp.simplify(beta_a)),
        "minimal_surface_residuals": [str(value) for value in minimal_surface],
        "stability_eigenvalues": eigenvalues,
        "mass_to_xi": str(mass_to_xi),
        "quartic_to_xi": str(quartic_to_xi),
        "scale_shift_symbol": str(delta),
    }
    return flow_rows, scale_rows, symbolic


def vector_parameters(vector: np.ndarray) -> dict[str, float]:
    return {
        "Omega_m": float(vector[0]),
        "log10_mu": float(vector[1]),
        "H0": float(vector[2]),
        "Omega_b_h2": float(vector[3]),
        "f_scalar": 1.0,
    }


def fit_minimal_source_branch() -> dict[str, Any]:
    result_5206 = json.loads(
        checkpoint_5207.RESULT_5206.read_text(encoding="utf-8")
    )
    starts = [
        np.asarray(
            [
                fit["params"]["Omega_m"],
                fit["params"]["log10_mu"],
                fit["params"]["H0"],
                fit["params"]["Omega_b_h2"],
            ],
            dtype=float,
        )
        for fit in result_5206["fits"]
    ]
    priors = (
        (0.15, 0.45),
        (-2.0, math.log10(5.0)),
        checkpoint_5207.checkpoint_5206.checkpoint_5195.H0_BOUNDS,
        checkpoint_5207.checkpoint_5206.checkpoint_5195.OMBH2_BOUNDS,
    )
    data = checkpoint_5207.checkpoint_5206.checkpoint_5195.load_joint_data()
    cache: dict[tuple[float, ...], float] = {}
    failures: dict[str, int] = {}
    evaluations = 0

    def objective(vector: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        key = tuple(round(float(value), 10) for value in vector)
        if key in cache:
            return cache[key]
        try:
            score = checkpoint_5207.score_calibrated(
                vector_parameters(vector),
                0.0,
                data,
                accuracy="fit",
                detail=False,
            )
            value = float(score["chi2_joint"])
        except (
            ValueError,
            RuntimeError,
            OverflowError,
            FloatingPointError,
            np.linalg.LinAlgError,
            checkpoint_5207.checkpoint_5206.checkpoint_5195.camb.baseconfig.CAMBError,
        ) as exc:
            name = type(exc).__name__
            failures[name] = failures.get(name, 0) + 1
            value = 1.0e30
        cache[key] = value
        return value

    steps = np.asarray([3.0e-5, 2.7e-4, 4.0e-3, 5.0e-7], dtype=float)
    started = time.perf_counter()
    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=priors,
            options={
                "maxiter": 120,
                "ftol": 2.0e-10,
                "maxls": 35,
                "eps": steps,
            },
        )
        for start in starts
    ]
    finite = [
        result
        for result in results
        if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e29
    ]
    if not finite:
        raise RuntimeError("all minimal-source-branch starts failed")
    best = min(finite, key=lambda result: float(result.fun))
    params = vector_parameters(np.asarray(best.x, dtype=float))
    exact = checkpoint_5207.score_calibrated(
        params,
        0.0,
        data,
        accuracy="exact",
        detail=True,
    )
    parameter_rows = []
    names = ["Omega_m", "log10_mu", "H0", "Omega_b_h2"]
    for name, value, bounds in zip(
        names,
        [params[name] for name in names],
        priors,
        strict=True,
    ):
        distance = min(value - bounds[0], bounds[1] - value) / (
            bounds[1] - bounds[0]
        )
        parameter_rows.append(
            {
                "parameter": name,
                "best_fit": value,
                "lower": bounds[0],
                "upper": bounds[1],
                "fractional_distance_to_edge": distance,
                "edge_flag": distance <= 0.01,
            }
        )
    k_count = 7
    fit = {
        "model": "ParentScalar_Lambda_zero_common_minimal_trajectory",
        "params": params,
        "zeta": 0.0,
        **exact,
        "k": k_count,
        "AIC_cosmology": exact["chi2_cosmology"] + 2.0 * k_count,
        "BIC_cosmology": exact["chi2_cosmology"]
        + k_count * math.log(checkpoint_5207.PRIMARY_N_COSMOLOGY),
        "AIC_joint": exact["chi2_joint"] + 2.0 * k_count,
        "BIC_joint": exact["chi2_joint"]
        + k_count * math.log(checkpoint_5207.PRIMARY_N_WITH_LOCAL),
        "convergence": (
            math.isfinite(exact["chi2_joint"])
            and abs(float(best.fun) - exact["chi2_joint"]) < 0.02
        ),
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "objective_evaluations": evaluations,
        "unique_objective_evaluations": len(cache),
        "successful_start_count": len(finite),
        "multistart_chi2_span": (
            max(float(result.fun) for result in finite)
            - min(float(result.fun) for result in finite)
        ),
        "prior_edge_flag": any(bool(row["edge_flag"]) for row in parameter_rows)
        or bool(exact["n_s_edge_flag"])
        or bool(exact["sigma8_edge_flag"]),
        "parameter_rows": parameter_rows,
        "failure_counts": failures,
        "runtime_seconds": time.perf_counter() - started,
    }
    return fit


def clean_fit(fit: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in fit.items()
        if key not in {"solution", "growth_residual_rows", "parameter_rows"}
    }


def model_comparison_rows(fit: dict[str, Any]) -> list[dict[str, Any]]:
    finite = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5207"
            / "Cavendish_source_calibrated_results.json"
        ).read_text(encoding="utf-8")
    )["fit"]
    result_5206 = json.loads(
        checkpoint_5207.RESULT_5206.read_text(encoding="utf-8")
    )
    baselines = [
        {
            "model": finite["model"],
            "chi2_joint": finite["chi2_joint"],
            "AIC_joint": finite["AIC_joint"],
            "BIC_joint": finite["BIC_joint"],
            "k": finite["k"],
            "edge": finite["prior_edge_flag"],
        }
    ]
    for baseline in result_5206["locked_comparators"]:
        baselines.append(
            {
                "model": baseline["model"],
                "chi2_joint": baseline["chi2_joint"],
                "AIC_joint": baseline["AIC_joint"],
                "BIC_joint": baseline["BIC_joint"],
                "k": baseline["k"],
                "edge": baseline["prior_edge_flag"],
            }
        )
    rows = []
    for baseline in baselines:
        delta_aic = fit["AIC_joint"] - baseline["AIC_joint"]
        delta_bic = fit["BIC_joint"] - baseline["BIC_joint"]
        rows.append(
            {
                "model": fit["model"],
                "baseline": baseline["model"],
                "delta_chi2_joint": fit["chi2_joint"]
                - baseline["chi2_joint"],
                "delta_AIC_joint": delta_aic,
                "delta_BIC_joint": delta_bic,
                "model_k": fit["k"],
                "baseline_k": baseline["k"],
                "model_edge_flag": fit["prior_edge_flag"],
                "baseline_edge_flag": baseline["edge"],
                "AIC_interpretation": (
                    "minimal_source_branch_favored"
                    if delta_aic < -2.0
                    else "draw_scale"
                    if abs(delta_aic) < 2.0
                    else "baseline_favored"
                ),
                "BIC_interpretation": (
                    "minimal_source_branch_favored"
                    if delta_bic < -2.0
                    else "draw_scale"
                    if abs(delta_bic) < 2.0
                    else "baseline_favored"
                ),
            }
        )
    return tagged(rows)


def physical_rows(
    fit: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, float],
]:
    megaparsec_m = constants.parsec * 1.0e6
    hbar_evs = constants.hbar / constants.electron_volt
    h0_si = fit["params"]["H0"] * 1000.0 / megaparsec_m
    h0_ev = h0_si * hbar_evs
    hbar_c_ev_m = constants.hbar * constants.c / constants.electron_volt
    planck_energy_ev = (
        math.sqrt(constants.hbar * constants.c**5 / constants.G)
        / constants.electron_volt
    )
    g_newton_ev = 1.0 / planck_energy_ev**2
    reduced_newton_ev = planck_energy_ev / math.sqrt(8.0 * math.pi)
    mu = 10.0 ** fit["params"]["log10_mu"]
    mass_ev = mu * h0_ev
    mass_inverse_m = mass_ev / hbar_c_ev_m
    mass_rate_si = mass_ev / hbar_evs
    g_h0 = g_newton_ev * h0_ev**2
    j_gap = g_newton_ev * mass_ev**2
    logarithmic_span = math.log(reduced_newton_ev / h0_ev)
    zeta_fit = abs(
        json.loads(
            (
                POST
                / "source-intake"
                / "functional_rg"
                / "5207"
                / "Cavendish_source_calibrated_results.json"
            ).read_text(encoding="utf-8")
        )["fit"]["zeta"]
    )
    unit_mass_induced_zeta = j_gap * logarithmic_span
    required_zeta_amplification = zeta_fit / unit_mass_induced_zeta
    unit_mass_induced_lambda = j_gap**2 * logarithmic_span
    scale_rows = tagged(
        [
            {
                "quantity": "H0",
                "value": h0_ev,
                "units": "eV",
                "derivation": "H0[km/s/Mpc] times hbar",
                "status": "DERIVED_FROM_FIT",
            },
            {
                "quantity": "m_gap",
                "value": mass_ev,
                "units": "eV",
                "derivation": "mu H0",
                "status": "DERIVED_FROM_FIT",
            },
            {
                "quantity": "G_N",
                "value": g_newton_ev,
                "units": "eV^-2",
                "derivation": "1/E_P^2 from SI hbar,c,G",
                "status": "MEASURED_SCALE_CONVERSION",
            },
            {
                "quantity": "J_gap",
                "value": j_gap,
                "units": "dimensionless",
                "derivation": "G_N m_gap^2",
                "status": "UNIVERSAL_SECOND_RELEVANT_DATUM",
            },
            {
                "quantity": "ln(M_N/H0)",
                "value": logarithmic_span,
                "units": "dimensionless",
                "derivation": "reduced Newton scale to Hubble scale",
                "status": "DERIVED_SCALE_INTERVAL",
            },
            {
                "quantity": "analytic_mass_induced_zeta_unit_coefficient",
                "value": unit_mass_induced_zeta,
                "units": "dimensionless",
                "derivation": "J_gap ln(M_N/H0)",
                "status": "PERTURBATIVE_POWER_COUNTING",
            },
            {
                "quantity": "amplification_needed_for_5207_zeta",
                "value": required_zeta_amplification,
                "units": "dimensionless",
                "derivation": "|zeta_5207|/[J_gap ln(M_N/H0)]",
                "status": "FINITE_ZETA_NOT_PARENT_SELECTED",
            },
            {
                "quantity": "analytic_mass_induced_lambda4_unit_coefficient",
                "value": unit_mass_induced_lambda,
                "units": "dimensionless",
                "derivation": "J_gap^2 ln(M_N/H0)",
                "status": "PERTURBATIVE_POWER_COUNTING",
            },
            {
                "quantity": "lambda4_quadratic_background_ceiling",
                "value": LAMBDA4_QUADRATIC_CEILING,
                "units": "dimensionless",
                "derivation": "locked checkpoint-5204 zero-Lambda ten-percent gate",
                "status": "SOURCE_LOCKED_BOUND",
            },
        ]
    )
    trajectory = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4958"
        / "essential_functional_GR_trajectory.csv"
    )
    solution = fit["solution"]
    x2_rows: list[dict[str, Any]] = []
    maxima: dict[str, float] = {}
    scale_ratio_parent = float(
        fit["background_diagnostics"]["scale_ratio_MR2_over_MN2"]
    )
    for scheme in ("dynamic_etaN", "reference_etaN0"):
        selected = [
            row
            for row in trajectory
            if row["scheme"] == scheme and row["polynomial_order"] == "8"
        ]
        selected.sort(key=lambda row: int(row["sample_index"]))
        previous, endpoint = selected[-2], selected[-1]
        g_reference = float(endpoint["g"])
        a_reference = float(endpoint["A2_a_over_g_power"])
        slope = (
            a_reference - float(previous["A2_a_over_g_power"])
        ) / (
            float(endpoint["t_log_k_over_seed"])
            - float(previous["t_log_k_over_seed"])
        )
        for k_over_h in (0.01, 1.0, 100.0):
            maximum_kinetic = -1.0
            maximum_total = -1.0
            maximum_n = 0.0
            maximum_a = 0.0
            maximum_g = 0.0
            for n_value, e_value, q_value in zip(
                solution.background.n_grid,
                solution.background.e_grid,
                solution.q_grid,
                strict=True,
            ):
                g_scale = (
                    g_newton_ev
                    * (h0_ev * float(e_value) * k_over_h) ** 2
                )
                a_value = a_reference + 8.0 * math.log(
                    g_scale / g_reference
                )
                g_hubble = g_newton_ev * (h0_ev * float(e_value)) ** 2
                kinetic_fraction = (
                    36.0
                    * scale_ratio_parent
                    / (8.0 * math.pi)
                    * abs(a_value)
                    * g_hubble
                    * float(q_value) ** 2
                )
                total_fraction = (
                    36.0
                    * scale_ratio_parent
                    / (8.0 * math.pi)
                    * abs(a_value)
                    * g_hubble
                    * float(q_value) ** 4
                )
                if kinetic_fraction > maximum_kinetic:
                    maximum_kinetic = kinetic_fraction
                    maximum_total = total_fraction
                    maximum_n = float(n_value)
                    maximum_a = a_value
                    maximum_g = g_hubble
            key = f"{scheme}_kH_{k_over_h:g}"
            maxima[f"{key}_kinetic"] = maximum_kinetic
            maxima[f"{key}_total"] = maximum_total
            x2_rows.append(
                {
                    "scheme": scheme,
                    "polynomial_order": 8,
                    "k_over_H": k_over_h,
                    "g_reference": g_reference,
                    "A_X2_reference": a_reference,
                    "measured_dA_dlnk": slope,
                    "derived_dA_dlnk": 16.0,
                    "maximum_background_N": maximum_n,
                    "A_X2_at_maximum": maximum_a,
                    "G_N_H_squared_at_maximum": maximum_g,
                    "maximum_abs_rho_X2_over_rho_kinetic": maximum_kinetic,
                    "maximum_abs_Omega_X2": maximum_total,
                    "status": "NEGLIGIBLE_ON_COMMON_MINIMAL_BACKGROUND",
                }
            )
    present_dynamic = next(
        row
        for row in x2_rows
        if row["scheme"] == "dynamic_etaN" and row["k_over_H"] == 1.0
    )
    c_x2_ev_minus4 = (
        present_dynamic["A_X2_at_maximum"] * g_newton_ev**2
    )
    x2_scale_ev = abs(c_x2_ev_minus4) ** (-0.25)
    x2_rows.extend(
        [
            {
                "scheme": "dynamic_etaN",
                "polynomial_order": 8,
                "k_over_H": 1.0,
                "g_reference": "",
                "A_X2_reference": "",
                "measured_dA_dlnk": "",
                "derived_dA_dlnk": 16.0,
                "maximum_background_N": 0.0,
                "A_X2_at_maximum": present_dynamic["A_X2_at_maximum"],
                "G_N_H_squared_at_maximum": g_h0,
                "maximum_abs_rho_X2_over_rho_kinetic": "",
                "maximum_abs_Omega_X2": "",
                "status": f"c_X2={c_x2_ev_minus4:.12e} eV^-4",
            },
            {
                "scheme": "dynamic_etaN",
                "polynomial_order": 8,
                "k_over_H": 1.0,
                "g_reference": "",
                "A_X2_reference": "",
                "measured_dA_dlnk": "",
                "derived_dA_dlnk": 16.0,
                "maximum_background_N": 0.0,
                "A_X2_at_maximum": present_dynamic["A_X2_at_maximum"],
                "G_N_H_squared_at_maximum": g_h0,
                "maximum_abs_rho_X2_over_rho_kinetic": "",
                "maximum_abs_Omega_X2": "",
                "status": f"|c_X2|^(-1/4)={x2_scale_ev:.12e} eV",
            },
        ]
    )
    local_systems = [
        ("Sun_surface", 695_700_000.0, 1.32712440018e20),
        ("Mercury_solar_orbit", 57_909_227_000.0, 1.32712440018e20),
        ("Earth_solar_orbit", constants.astronomical_unit, 1.32712440018e20),
        ("Saturn_solar_orbit", 1.43353e12, 1.32712440018e20),
        ("Moon_Earth_orbit", 384_400_000.0, 3.986004418e14),
    ]
    local_payload: list[dict[str, Any]] = [
        {
            "arena": "direct_matter_scalar_charge",
            "radius_m": "",
            "central_GM_m3_s2": "",
            "surface_potential_abs": "",
            "static_metric_induced_abs_delta_chi_over_chi_bound": 0.0,
            "causal_dynamic_abs_delta_chi_over_chi_bound": 0.0,
            "total_metric_induced_abs_delta_chi_over_chi_bound": 0.0,
            "homogeneous_tidal_to_Newton_ratio": 0.0,
            "derivation": "delta S_visible/delta chi=0 at constant F_R",
            "status": "EXACT_ZERO_DIRECT_CHARGE",
        }
    ]
    background_log_rate = h0_si * abs(
        float(fit["background_diagnostics"]["q0"])
        / float(fit["background_diagnostics"]["phi0"])
    )
    for arena, radius_m, central_gm in local_systems:
        potential = central_gm / (radius_m * constants.c**2)
        mass_radius = mass_inverse_m * radius_m
        static_induced_fraction = (
            2.0
            * potential
            * mass_radius**2
            / (1.0 + mass_radius**2)
        )
        k_rate = constants.c / radius_m
        dynamic_induced_fraction = (
            4.0
            * potential
            * background_log_rate
            * k_rate
            / (k_rate**2 + mass_rate_si**2)
        )
        total_induced_fraction = (
            static_induced_fraction + dynamic_induced_fraction
        )
        local_payload.append(
            {
                "arena": arena,
                "radius_m": radius_m,
                "central_GM_m3_s2": central_gm,
                "surface_potential_abs": potential,
                "static_metric_induced_abs_delta_chi_over_chi_bound": (
                    static_induced_fraction
                ),
                "causal_dynamic_abs_delta_chi_over_chi_bound": (
                    dynamic_induced_fraction
                ),
                "total_metric_induced_abs_delta_chi_over_chi_bound": (
                    total_induced_fraction
                ),
                "homogeneous_tidal_to_Newton_ratio": (
                    h0_si**2 * radius_m**3 / central_gm
                ),
                "derivation": (
                    "|delta chi/chi|<=2|Phi|m^2/(k^2+m^2)"
                    "+4|Phi||dot chi/chi|omega/(k^2+m^2), "
                    "k>=c/r, omega<=k; "
                    "tidal ratio=H0^2 r^3/(GM)"
                ),
                "status": "METRIC_INDUCED_RESPONSE_AND_COSMOLOGICAL_TIDE_NEGLIGIBLE",
            }
        )
    local_rows = tagged(local_payload)
    diagnostics = {
        "H0_eV": h0_ev,
        "m_gap_eV": mass_ev,
        "m_gap_inverse_m": mass_inverse_m,
        "G_N_eV_minus2": g_newton_ev,
        "M_N_eV": reduced_newton_ev,
        "G_N_H0_squared": g_h0,
        "J_gap": j_gap,
        "log_MN_over_H0": logarithmic_span,
        "unit_mass_induced_zeta": unit_mass_induced_zeta,
        "required_zeta_amplification": required_zeta_amplification,
        "unit_mass_induced_lambda4": unit_mass_induced_lambda,
        "maximum_X2_kinetic_fraction": max(
            value for key, value in maxima.items() if key.endswith("_kinetic")
        ),
        "maximum_X2_total_fraction": max(
            value for key, value in maxima.items() if key.endswith("_total")
        ),
        "c_X2_eV_minus4": c_x2_ev_minus4,
        "X2_scale_eV": x2_scale_ev,
        "maximum_local_cosmological_tide_ratio": max(
            float(row["homogeneous_tidal_to_Newton_ratio"])
            for row in local_rows
        ),
        "maximum_metric_induced_scalar_fraction": max(
            float(row["total_metric_induced_abs_delta_chi_over_chi_bound"])
            for row in local_rows
        ),
    }
    return scale_rows, tagged(x2_rows), local_rows, diagnostics


def fit_rows(fit: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics = fit["background_diagnostics"]
    local = fit["local"]
    return tagged(
        [
            {
                "model": fit["model"],
                "zeta_c": fit["zeta"],
                "Omega_m": fit["params"]["Omega_m"],
                "log10_mu": fit["params"]["log10_mu"],
                "mu": 10.0 ** fit["params"]["log10_mu"],
                "H0": fit["params"]["H0"],
                "Omega_b_h2": fit["params"]["Omega_b_h2"],
                "phi0": diagnostics["phi0"],
                "q0": diagnostics["q0"],
                "M_R2_over_M_N2": diagnostics["scale_ratio_MR2_over_MN2"],
                "present_source_ratio": diagnostics[
                    "present_Poisson_source_ratio"
                ],
                "gamma_minus_one": local["gamma_minus_one"],
                "Gdot_over_G_yr_inv": local["Gdot_over_G_yr_inv"],
                "chi2_cosmology": fit["chi2_cosmology"],
                "chi2_local": fit["chi2_local"],
                "chi2_joint": fit["chi2_joint"],
                "k": fit["k"],
                "AIC_joint": fit["AIC_joint"],
                "BIC_joint": fit["BIC_joint"],
                "convergence": fit["convergence"],
                "prior_edge_flag": fit["prior_edge_flag"],
            }
        ]
    )


def decision_rows(
    fit: dict[str, Any],
    comparisons: list[dict[str, Any]],
    physical: dict[str, float],
) -> list[dict[str, Any]]:
    finite_row = next(
        row
        for row in comparisons
        if row["baseline"] == "ParentST_Lambda_zero_Cavendish_calibrated"
    )
    return tagged(
        [
            {
                "gate": "positive_Z_independent_trajectory_coordinate",
                "result": "REJECTED_BY_CANONICAL_FIELD_QUOTIENT",
                "evidence": "dchi/dpsi=sqrt(Z) removes Z exactly where Z>0",
                "next_action": "use canonical F,V,c_X2 invariants",
            },
            {
                "gate": "finite_zeta_parent_selection",
                "result": "NOT_SELECTED",
                "evidence": (
                    f"minimal minus finite delta AIC={finite_row['delta_AIC_joint']}; "
                    f"delta BIC={finite_row['delta_BIC_joint']}"
                ),
                "next_action": "retain zeta=0 as the leading source-derived branch",
            },
            {
                "gate": "common_minimal_bulk_trajectory",
                "result": "SELECTED_AT_KNOWN_ESSENTIAL_AND_LINEAR_MASS_ORDER",
                "evidence": (
                    "F_R=M_R^2; V=m_gap^2 chi^2/2; Z=1; "
                    "X2 inherited from the GR-connected functional trajectory"
                ),
                "next_action": "calculate finite-mass nonlinear functional backreaction",
            },
            {
                "gate": "local_transition_requirement",
                "result": "REMOVED_ON_MINIMAL_BRANCH",
                "evidence": (
                    "constant F_R gives zero direct charge and "
                    f"metric-induced |delta chi/chi|<="
                    f"{physical['maximum_metric_induced_scalar_fraction']:.6e}"
                ),
                "next_action": "retain only homogeneous cosmological tide and EFT bounds",
            },
            {
                "gate": "X2_cosmological_backreaction",
                "result": "BOUNDED_NEGLIGIBLE",
                "evidence": (
                    f"maximum kinetic fraction={physical['maximum_X2_kinetic_fraction']:.6e}"
                ),
                "next_action": "do not fit c_X2 to cosmology",
            },
            {
                "gate": "absolute_G_N_from_autonomous_parent_flow",
                "result": "IMPOSSIBLE_WITHOUT_DIMENSIONFUL_BOUNDARY_DATUM",
                "evidence": "RG-time translation rescales G_N and m_gap but preserves J_gap",
                "next_action": "treat measured G_N as one legitimate integration constant",
            },
            {
                "gate": "universal_motion_scale",
                "result": "SECOND_RELEVANT_DATUM_RETAINED",
                "evidence": f"J_gap={physical['J_gap']:.12e}",
                "next_action": "no arena-specific m_gap retuning",
            },
            {
                "gate": "Lambda_cal_zero",
                "result": "BRANCH_HYPOTHESIS_NOT_DERIVED",
                "evidence": "checkpoint-5205 Hamiltonian rank theorem",
                "next_action": "derive vacuum branch selection or keep explicit conditional label",
            },
            {
                "gate": "full_MTS_unification",
                "result": "NOT_CLAIMED",
                "evidence": "finite-mass nonlinear functional flow and Lambda selection remain open",
                "next_action": (
                    "derive mass-deformed essential P(X) trajectory and vacuum branch"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source": str(path),
                "sha256": expected,
                "role": (
                    "locked local parent derivation or machine evidence"
                ),
                "exists": path.is_file(),
            }
            for path, expected in SOURCE_LOCKS.items()
        ]
    )


def build_document(
    fit: dict[str, Any],
    comparisons: list[dict[str, Any]],
    physical: dict[str, float],
) -> str:
    comparison = next(
        row
        for row in comparisons
        if row["baseline"] == "ParentST_Lambda_zero_Cavendish_calibrated"
    )
    lcdm = next(row for row in comparisons if row["baseline"] == "LCDM")
    wcdm = next(row for row in comparisons if row["baseline"] == "wCDM")
    cpl = next(row for row in comparisons if row["baseline"] == "CPL")
    diagnostics = fit["background_diagnostics"]
    return f"""# 5208 - Common Minimal Motion Trajectory, Canonical-`Z` Quotient, Absolute-Scale Covariance and Local-GR Selection

Private derivation and empirical robustness checkpoint. No GitHub action and
no full-MTS or public cosmology claim.

Marker: `{MARKER}`.

## Executive result

The checkpoint-5207 finite-curvature branch is not the unique route connecting
the cosmological scalar to local GR. A cleaner source-selected branch exists.

For one scalar with `Z(psi)>0`, define

```text
chi(psi)=integral_0^psi sqrt(Z(u)) du.
```

Then the two-derivative kinetic term is canonical exactly. Near the
reflection-symmetric origin,

```text
m_can^2       =m2/Z0;
lambda4_can   =lambda4/Z0^2-2 m2 z2/Z0^3;
xi_can        =xi2/Z0;
zeta_c        =xi2/(2 Z0);
c_X2,can      =c_X2/Z0^2.
```

Thus `Z`, `F_R`, `V` and `c_X2` are not four independent germs. The physical
trajectory must be stated in canonical invariant coordinates.

## 1. Minimal common trajectory

The locked parent results imply:

```text
massless shift-symmetric surface:
  m2=lambda4=xi=z2=0 is invariant;

relevant mass eigenvector:
  no linear xi component in the exact source comparator;

regular quartic:
  irrelevant in the MTS potential projection;

essential X2 function:
  one GR-connected relevant direction and therefore trajectory-owned.
```

The leading common trajectory is consequently

```text
F_R(chi)=M_R^2;
V(chi)=m_gap^2 chi^2/2;
Z_can=1;
P_ge2(X)=the locked GR-connected essential P(X) trajectory;
Lambda_cal=0 as an explicit branch hypothesis.
```

This is a two-scale theory, not a parameter-free theory: measured `G_N` and
one universal `J_gap=G_N m_gap^2` remain the two relevant data. No value may
be retuned by arena.

## 2. Absolute-scale theorem

For an autonomous dimensionless RG system, translating RG time gives

```text
u_delta(k)=u(exp(-delta)k);
G_N -> exp(-2delta) G_N;
m_gap -> exp(delta) m_gap;
G_N m_gap^2 -> G_N m_gap^2.
```

Therefore an autonomous parent flow can predict dimensionless ratios and
critical exponents but cannot select an absolute number in SI units. The
measured value of `G_N` is one legitimate dimensional integration constant,
just as in GR. This is an exact scale-covariance result rather than an
unfilled coefficient ledger.

For the fitted minimal branch,

```text
H0                    ={physical['H0_eV']:.12e} eV;
m_gap                 ={physical['m_gap_eV']:.12e} eV;
J_gap                 ={physical['J_gap']:.12e};
ln(M_N/H0)            ={physical['log_MN_over_H0']:.12g}.
```

## 3. Direct source-selected refit

Fixing `zeta_c=0` rather than fitting it gives

```text
Omega_m               ={fit['params']['Omega_m']:.12g};
mu=m_gap/H0           ={10.0 ** fit['params']['log10_mu']:.12g};
H0                    ={fit['params']['H0']:.12g} km/s/Mpc;
Omega_b h^2           ={fit['params']['Omega_b_h2']:.12g};
phi0                  ={diagnostics['phi0']:.12g};
q0                    ={diagnostics['q0']:.12g};
M_R^2/M_N^2           ={diagnostics['scale_ratio_MR2_over_MN2']:.12g};
present source ratio  ={diagnostics['present_Poisson_source_ratio']:.12g};
gamma-1               ={fit['local']['gamma_minus_one']:.12g};
Gdot/G                ={fit['local']['Gdot_over_G_yr_inv']:.12g} yr^-1;
chi2_joint            ={fit['chi2_joint']:.12g};
AIC_joint             ={fit['AIC_joint']:.12g};
BIC_joint             ={fit['BIC_joint']:.12g}.
```

Against the fitted finite-`zeta_c` checkpoint-5207 branch:

```text
Delta chi2={comparison['delta_chi2_joint']:.12g};
Delta AIC ={comparison['delta_AIC_joint']:.12g};
Delta BIC ={comparison['delta_BIC_joint']:.12g}.
```

The finite coupling buys only a small chi-square change. AIC is draw-scale
but numerically favors the minimal branch, while BIC clearly favors it after
the extra coordinate is counted. The source-selected zero-coupling branch is
therefore the better parent default.

Against standard comparators:

```text
minimal minus LCDM: Delta AIC={lcdm['delta_AIC_joint']:.6g},
                    Delta BIC={lcdm['delta_BIC_joint']:.6g};
minimal minus wCDM: Delta AIC={wcdm['delta_AIC_joint']:.6g},
                    Delta BIC={wcdm['delta_BIC_joint']:.6g};
minimal minus CPL:  Delta AIC={cpl['delta_AIC_joint']:.6g},
                    Delta BIC={cpl['delta_BIC_joint']:.6g}.
```

This remains internal model-discipline evidence, not a cosmological claim.

## 4. Why local GR no longer needs a scalar transition

On the selected branch `F_R` is constant and visible matter has no direct
motion portal. Therefore the direct scalar charge of a material body is
exactly zero. A local metric perturbation can nevertheless force a tiny
response of the time-dependent homogeneous scalar:

```text
(k^2/a^2+m_gap^2) delta chi
 approximately -2 m_gap^2 chi_bar Phi
              +4 dot(chi_bar) dot(Phi).
```

Taking `k>=c/r` and the causal envelope `omega<=k` gives

```text
|delta chi/chi_bar|
 <=[2|Phi|m_gap^2
    +4|Phi||dot(chi_bar)/chi_bar|omega]
   /(k^2+m_gap^2)
 <={physical['maximum_metric_induced_scalar_fraction']:.6e}
```

over the selected local systems. The homogeneous cosmological scalar also
contributes background stress, but its largest tested solar-system tidal
ratio is only

```text
{physical['maximum_local_cosmological_tide_ratio']:.6e}.
```

Thus the finite-`zeta` problem of dynamically forcing
`phi_cosmology -> phi_local=0` disappears on this common minimal branch.

## 5. Generated `X^2` term

The weak essential flow is

```text
beta_g=2g;
beta_c=4c+16g^2;
c=A_X2 g^2;
beta_A_X2=16.
```

Extrapolating the two locked checkpoint-4958 trajectory schemes to `k~H`
and scanning `0.01<=k/H<=100` gives

```text
max |rho_X2/rho_kinetic|
 ={physical['maximum_X2_kinetic_fraction']:.6e};

max |Omega_X2|
 ={physical['maximum_X2_total_fraction']:.6e}.
```

The generated derivative interaction is therefore retained in the parent
action but cannot be used as a cosmological fit parameter.

## 6. Remaining boundary

```text
canonical Z quotient                              = derived;
minimal mass-only F_R,V trajectory                = selected at known order;
essential X2 trajectory                           = inherited and bounded;
absolute G_N prediction from autonomous RG        = rejected exactly;
local scalar transition                           = unnecessary on zeta=0;
local GR/Newton/Maxwell leading branch             = retained;
finite-mass nonlinear functional backreaction      = not fully calculated;
absolute Lambda_cal=0 selection                    = not derived;
full MTS unification                               = not claimed.
```

Selected next route:

```text
DERIVE_FINITE_MASS_ESSENTIAL_PX_BACKREACTION_AND_VACUUM_BRANCH_SELECTION.
```
"""


def validation_rows(
    payload: dict[str, Any],
    output_names: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check: str, passed: bool, detail: Any) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    add(
        "source_lock_count",
        len(SOURCE_LOCKS) == 16,
        len(SOURCE_LOCKS),
    )
    for path, expected in SOURCE_LOCKS.items():
        add(
            f"source_{path.name}",
            path.is_file() and file_digest(path) == expected,
            expected,
        )
    for name, residual in payload["canonical_field_checks"].items():
        if name == "canonical_c_X2":
            add(name, residual == "c_X2/Z0**2", residual)
        else:
            add(name, residual == "0", residual)
    symbolic = payload["trajectory_symbolic"]
    add("beta_J_exact_zero", symbolic["beta_J_gap"] == "0", symbolic["beta_J_gap"])
    add("beta_A_X2_exact_16", symbolic["beta_A_X2"] == "16", symbolic["beta_A_X2"])
    add(
        "minimal_surface_exact",
        symbolic["minimal_surface_residuals"] == ["0", "0"],
        symbolic["minimal_surface_residuals"],
    )
    add(
        "source_stability_spectrum",
        symbolic["stability_eigenvalues"] == [-4.0, -2.0, -2.0, 0.0, 0.0],
        symbolic["stability_eigenvalues"],
    )
    add("mass_to_xi_zero", symbolic["mass_to_xi"] == "0", symbolic["mass_to_xi"])
    fit = payload["fit"]
    add("minimal_fit_converged", bool(fit["convergence"]), fit["optimizer_message"])
    add("minimal_fit_optimizer", bool(fit["optimizer_success"]), fit["optimizer_message"])
    add("minimal_fit_not_edge", not bool(fit["prior_edge_flag"]), fit["prior_edge_flag"])
    add("minimal_zeta_exact_zero", float(fit["zeta"]) == 0.0, fit["zeta"])
    diagnostics = fit["background_diagnostics"]
    add(
        "minimal_Cavendish_scale_exact",
        abs(float(diagnostics["scale_ratio_MR2_over_MN2"]) - 1.0) < 1.0e-12,
        diagnostics["scale_ratio_MR2_over_MN2"],
    )
    add(
        "minimal_source_ratio_exact",
        abs(float(diagnostics["present_Poisson_source_ratio"]) - 1.0) < 1.0e-12,
        diagnostics["present_Poisson_source_ratio"],
    )
    add(
        "minimal_gamma_exact",
        abs(float(fit["local"]["gamma_minus_one"])) < 1.0e-20,
        fit["local"]["gamma_minus_one"],
    )
    add(
        "minimal_Gdot_exact",
        abs(float(fit["local"]["Gdot_over_G_yr_inv"])) < 1.0e-25,
        fit["local"]["Gdot_over_G_yr_inv"],
    )
    physical = payload["physical"]
    add("J_gap_positive", physical["J_gap"] > 0.0, physical["J_gap"])
    add(
        "finite_zeta_requires_nonperturbative_amplification",
        physical["required_zeta_amplification"] > 1.0e100,
        physical["required_zeta_amplification"],
    )
    add(
        "mass_induced_quartic_below_ceiling",
        physical["unit_mass_induced_lambda4"] < LAMBDA4_QUADRATIC_CEILING,
        physical["unit_mass_induced_lambda4"],
    )
    add(
        "X2_kinetic_suppression",
        physical["maximum_X2_kinetic_fraction"] < 1.0e-100,
        physical["maximum_X2_kinetic_fraction"],
    )
    add(
        "X2_total_suppression",
        physical["maximum_X2_total_fraction"] < 1.0e-100,
        physical["maximum_X2_total_fraction"],
    )
    add(
        "local_cosmological_tide_suppression",
        physical["maximum_local_cosmological_tide_ratio"] < 1.0e-18,
        physical["maximum_local_cosmological_tide_ratio"],
    )
    add(
        "metric_induced_scalar_suppression",
        physical["maximum_metric_induced_scalar_fraction"] < 1.0e-20,
        physical["maximum_metric_induced_scalar_fraction"],
    )
    comparisons = payload["model_comparisons"]
    add("comparison_count", len(comparisons) == 5, len(comparisons))
    finite = next(
        row
        for row in comparisons
        if row["baseline"] == "ParentST_Lambda_zero_Cavendish_calibrated"
    )
    add(
        "minimal_AIC_preferred_to_finite_zeta",
        float(finite["delta_AIC_joint"]) < 0.0,
        finite["delta_AIC_joint"],
    )
    add(
        "minimal_BIC_preferred_to_finite_zeta",
        float(finite["delta_BIC_joint"]) < 0.0,
        finite["delta_BIC_joint"],
    )
    add(
        "all_evidence_rows_nonclaim",
        all(
            not bool(row["valid_for_full_MTS_claim"])
            for dataset in payload["row_datasets"]
            for row in dataset
        ),
        "all false",
    )
    for name in output_names:
        add(f"output_{name}", (OUT / name).is_file(), str(OUT / name))
    add("document_exists", DOCUMENT.is_file(), str(DOCUMENT))
    add(
        "formal_tree_unchanged",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    public_head, public_status = git_state(PUBLIC)
    galaxy_head, galaxy_status = git_state(GALAXY)
    add("public_head_unchanged", public_head == PUBLIC_HEAD, public_head)
    add("public_clean", public_status == [], public_status)
    add("galaxy_head_unchanged", galaxy_head == GALAXY_HEAD, galaxy_head)
    add("galaxy_dirty_paths_unchanged", galaxy_status == GALAXY_DIRTY, galaxy_status)
    add(
        "no_script_pycache",
        not (POST / "scripts" / "__pycache__").exists(),
        str(POST / "scripts" / "__pycache__"),
    )
    return rows


def run_checkpoint() -> None:
    assert_source_locks()
    if tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed before checkpoint 5208")
    public_head, public_status = git_state(PUBLIC)
    galaxy_head, galaxy_status = git_state(GALAXY)
    if public_head != PUBLIC_HEAD or public_status:
        raise RuntimeError("public worktree changed before checkpoint 5208")
    if galaxy_head != GALAXY_HEAD or galaxy_status != GALAXY_DIRTY:
        raise RuntimeError("galaxy repository changed before checkpoint 5208")
    canonical_rows, canonical_checks = canonical_field_quotient()
    flow_rows, scale_covariance_rows, trajectory_symbolic = trajectory_theorems()
    fit = fit_minimal_source_branch()
    comparisons = model_comparison_rows(fit)
    power_rows, x2_rows, local_rows, physical = physical_rows(fit)
    fit_summary = fit_rows(fit)
    decisions = decision_rows(fit, comparisons, physical)
    provenance = provenance_rows()
    output_payloads = {
        "canonical_field_quotient.csv": canonical_rows,
        "common_trajectory_flow_theorems.csv": flow_rows,
        "absolute_scale_covariance.csv": scale_covariance_rows,
        "minimal_source_branch_fit.csv": fit_summary,
        "minimal_source_branch_parameters.csv": tagged(fit["parameter_rows"]),
        "model_comparisons.csv": comparisons,
        "physical_scale_and_power_counting.csv": power_rows,
        "X2_FLRW_suppression.csv": x2_rows,
        "local_GR_residual_bounds.csv": local_rows,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in output_payloads.items():
        write_csv(OUT / name, rows)
    DOCUMENT.write_text(
        build_document(fit, comparisons, physical),
        encoding="utf-8",
    )
    evidence_paths = [OUT / name for name in output_payloads]
    result_name = "common_minimal_motion_trajectory_results.json"
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "canonical_field_checks": canonical_checks,
        "trajectory_symbolic": trajectory_symbolic,
        "fit": clean_fit(fit),
        "model_comparisons": [
            {
                key: value
                for key, value in row.items()
                if key
                not in {
                    "checkpoint",
                    "marker",
                    "checked_date",
                    "valid_for_cosmology_support_claim",
                    "valid_for_full_MTS_claim",
                }
            }
            for row in comparisons
        ],
        "physical": physical,
        "claim_status": {
            "canonical_Z_quotient_derived": True,
            "absolute_GN_from_autonomous_RG_rejected": True,
            "minimal_mass_only_common_trajectory_selected_at_known_order": True,
            "finite_zeta_parent_selected": False,
            "local_scalar_transition_required_on_selected_branch": False,
            "X2_cosmological_backreaction_relevant": False,
            "finite_mass_nonlinear_functional_flow_complete": False,
            "Lambda_zero_parent_derived": False,
            "cosmology_support": False,
            "full_MTS": False,
            "GitHub_action": False,
        },
        "selected_next_route": (
            "DERIVE_FINITE_MASS_ESSENTIAL_PX_BACKREACTION_AND_VACUUM_BRANCH_SELECTION"
        ),
        "source_hashes": {
            str(path): expected for path, expected in SOURCE_LOCKS.items()
        },
        "evidence_csv_sha256": selected_digest(evidence_paths, OUT),
        "formal_tree_sha256": tree_digest(FORMAL),
        "public_head": public_head,
        "galaxy_head": galaxy_head,
        "row_datasets": [
            canonical_rows,
            flow_rows,
            scale_covariance_rows,
            fit_summary,
            tagged(fit["parameter_rows"]),
            comparisons,
            power_rows,
            x2_rows,
            local_rows,
            decisions,
            provenance,
        ],
    }
    output_names = [*output_payloads, result_name]
    write_json(OUT / result_name, payload)
    validation = validation_rows(payload, output_names)
    write_csv(VALIDATION, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(json.dumps(failures, indent=2, default=json_default))
    result_payload = {
        key: value for key, value in payload.items() if key != "row_datasets"
    }
    result_payload["validation"] = {
        "passed": len(validation),
        "failed": 0,
        "validation_path": str(VALIDATION),
    }
    write_json(OUT / result_name, result_payload)
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "chi2_joint": fit["chi2_joint"],
                "delta_AIC_vs_finite_zeta": next(
                    row["delta_AIC_joint"]
                    for row in comparisons
                    if row["baseline"]
                    == "ParentST_Lambda_zero_Cavendish_calibrated"
                ),
                "J_gap": physical["J_gap"],
                "maximum_X2_kinetic_fraction": physical[
                    "maximum_X2_kinetic_fraction"
                ],
                "selected_next_route": result_payload["selected_next_route"],
                "evidence_csv_sha256": result_payload["evidence_csv_sha256"],
                "formal_tree_sha256": result_payload["formal_tree_sha256"],
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    assert_source_locks()
    result = OUT / "common_minimal_motion_trajectory_results.json"
    if not result.is_file() or not VALIDATION.is_file() or not DOCUMENT.is_file():
        raise RuntimeError("checkpoint-5208 saved products are incomplete")
    payload = json.loads(result.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION)
    failures = [row for row in validation if row["status"] != "PASS"]
    csv_paths = [
        path
        for path in OUT.glob("*.csv")
        if path.name != VALIDATION.name
    ]
    actual_digest = selected_digest(csv_paths, OUT)
    if actual_digest != payload["evidence_csv_sha256"]:
        raise RuntimeError(
            f"evidence digest changed: {actual_digest} != {payload['evidence_csv_sha256']}"
        )
    if failures:
        raise RuntimeError(f"saved validation contains failures: {failures}")
    if tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed")
    public_head, public_status = git_state(PUBLIC)
    galaxy_head, galaxy_status = git_state(GALAXY)
    if public_head != PUBLIC_HEAD or public_status:
        raise RuntimeError("public worktree changed")
    if galaxy_head != GALAXY_HEAD or galaxy_status != GALAXY_DIRTY:
        raise RuntimeError("galaxy repository changed")
    if (POST / "scripts" / "__pycache__").exists():
        raise RuntimeError("script __pycache__ exists")
    print(
        json.dumps(
            {
                "saved_validation": f"{len(validation)}/{len(validation)} PASS",
                "evidence_csv_sha256": actual_digest,
                "formal_tree_sha256": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def dry_run() -> None:
    assert_source_locks()
    canonical_rows, canonical_checks = canonical_field_quotient()
    flow_rows, scale_rows, symbolic = trajectory_theorems()
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "canonical_rows": len(canonical_rows),
                "flow_rows": len(flow_rows),
                "scale_rows": len(scale_rows),
                "canonical_checks": canonical_checks,
                "trajectory_symbolic": symbolic,
                "formal_tree_sha256": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        dry_run()
    elif arguments.validate_saved:
        validate_saved()
    else:
        run_checkpoint()


if __name__ == "__main__":
    main()
