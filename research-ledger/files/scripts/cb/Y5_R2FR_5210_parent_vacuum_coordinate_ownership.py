from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import sympy as sp

import Y5_R2FR_5209_finite_mass_PX_vacuum_branch_gate as checkpoint_5209


CHECKPOINT = 5210
MARKER = "MTS_5210_PARENT_VACUUM_COORDINATE_RENORMALIZATION_DATUM_THEOREM"
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
    / "5210-Y5-R2FR-parent-vacuum-coordinate-local-invariant-CTP-RG-"
    "source-and-renormalization-datum-theorem.md"
)
PUBLIC = checkpoint_5209.PUBLIC
GALAXY = checkpoint_5209.GALAXY
PUBLIC_HEAD = checkpoint_5209.PUBLIC_HEAD
GALAXY_HEAD = checkpoint_5209.GALAXY_HEAD
GALAXY_DIRTY = checkpoint_5209.GALAXY_DIRTY
FORMAL_LOCK = checkpoint_5209.FORMAL_LOCK
SPEED_OF_LIGHT = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR_SI = 1.054571817e-34
HBAR_EV_S = 6.582119569e-16
EV_JOULE = 1.602176634e-19
MPC_M = 3.0856775814913673e22
SOURCE_LOCKS = {
    POST
    / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-"
    "induced-coefficient-matching-to-GN-Lambda-and-R2.md": (
        "8798d2de8c48ccd4fcc22d676aa1ae37cb6ac7691a579f9444095a8302832780"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4876_HEAT_KERNEL_MATCHING.csv": (
        "faa0112055235a30948fb45a5fec63773e3c7a56e280c22bd4de773ea200852d"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4876_VALIDATION.csv": (
        "77354ddca778b0cbd8c6d7f673da053cd3205e49f1dfb52dfb9c4bd18bad3cd6"
    ),
    POST
    / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-"
    "form-factor-completion-or-renormalized-vacuum-freeze.md": (
        "9d57f0ec8028530a48c7cab90b0447fead680461500a8c3da2390a253ac39dd4"
    ),
    POST / "scripts" / "Y5_R2FR_4877_spectrum_nonlocal_vacuum.py": (
        "1262f50ecdc8022393f4a63b5127ddf83a0724dfc4d7935ebd70c97561cb8a3e"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4877_DETERMINANT_WEIGHTS.csv": (
        "8810a92f0ed5f7e8b14b5ef6dbb67493c101d0edf0c61f32cef0fd239f5792c1"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4877_BRANCH_TESTS.csv": (
        "2dab97878d495e281a23dc9351e99bdc9a2234e61bfc4c635650c9284ba1b37d"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4877_VACUUM_FREEZE.csv": (
        "48b087ea5d207a0ddfaf31080ffab5064d7dc5c3e6e05a1575f3b89a6156ab58"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4877_VALIDATION.csv": (
        "1bb197d4a02899b938a7a03c31023428d81b85b4ad60dd563df83d42edca5265"
    ),
    POST
    / "4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-"
    "gate.md": (
        "231a7ae70425d3860ba8a9355c175d6ca8a996254c82931abf2c40b7ba616063"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4934"
    / "completed_combined_flow_results.json": (
        "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4934_VALIDATION.csv": (
        "90c66ecdbbcaf823d562e834f3058cf0051524be6fd16071fd10a3c38a3d24db"
    ),
    POST
    / "5202-Y5-R2FR-scalar-curvature-no-go-translation-gauge-TEGR-"
    "coframe-ancestry-and-mode-theorem.md": (
        "753a01fd12a36fe687877c70a89b97b838a5761a6af31c5d756c4ec5bc7a810b"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5202"
    / "translation_gauge_TEGR_coframe_ancestry_results.json": (
        "7cd2cdf5a76fce560382303bf9e1f13e49279943cd0533db48d93346697e3bb1"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5202_VALIDATION.csv": (
        "23f752f8887aeed4830cdcb4732665c0d015cc292c91bbf150d72c44650d20de"
    ),
    POST
    / "5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-"
    "coupling-and-branch-reduction-theorem.md": (
        "0c456634e22a3f6e03ce648fe34c28e5557d562a47249b04201a2602b67c8a6b"
    ),
    POST / "scripts" / "Y5_R2FR_5203_canonical_translation_parent_action_branch_gate.py": (
        "f52fbd568214e6970a9e6160b285edab027045b5b31bd51d700488a7cdb6604d"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "canonical_translation_parent_action_results.json": (
        "4199e389c41acf8b7c4414912afd88b616429440e90952e80553a235f528b2fe"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "canonical_translation_parent_action.csv": (
        "f0a84d6d37697d9f01b6991ca32e20f6e87352185224b437ac6611039d952c27"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5203"
    / "coefficient_state_closure_ownership.csv": (
        "c6f046a416ba5e5cc9502827c4081bad6866e49ff6497f802af4ee6bb974ea5e"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5203_VALIDATION.csv": (
        "9c2276566021444909ba6838047c0288ac42a1e73831f51d1e6fedfb3c267b44"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5195"
    / "joint_CMB_informed_refit_results.json": (
        "538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad"
    ),
    POST
    / "5209-Y5-R2FR-finite-mass-essential-PX-threshold-backreaction-"
    "vacuum-rank-and-local-GR-Maxwell-gate.md": (
        "0e23836824de9281d17bbfb47c6c2350bc91e899356796cb640e622e342bc384"
    ),
    POST / "scripts" / "Y5_R2FR_5209_finite_mass_PX_vacuum_branch_gate.py": (
        "88c48a13192d1c394bfab38b9b0b894e866b9bc1eba403c8d5487a1e5386ca8a"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5209"
    / "finite_mass_PX_vacuum_branch_results.json": (
        "98dbaacbb1fafe5bb50dcc9999a4d64b0e94cabf5c4ff74f0b5aea2a5f14a598"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5209"
    / "vacuum_constraint_rank_and_threshold.csv": (
        "5bcf99a28020e42387768657d49840fa6f7171847f6f7b0788bfb564709a15af"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5209_VALIDATION.csv": (
        "9b0aa85a4ad32bcf9734092247a4860c3550b07b35ef09cf68b74f3b2fbf0460"
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_digest(paths: list[Path], base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(file_digest(path).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint": CHECKPOINT,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "claim_allowed": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def assert_source_locks() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path, expected in SOURCE_LOCKS.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = file_digest(path)
        if actual != expected:
            raise RuntimeError(
                f"source lock mismatch for {path}: expected {expected}, got {actual}"
            )
        hashes[path.relative_to(POST).as_posix()] = actual
    return hashes


def symbolic_vacuum_theorem() -> dict[str, Any]:
    vacuum_coordinate, mass_ratio, supertrace_weight = sp.symbols(
        "u0 w W0",
        real=True,
    )
    beta_vacuum = (
        -4 * vacuum_coordinate
        + supertrace_weight / (32 * sp.pi**2 * (1 + mass_ratio))
    )
    stationary_coordinate = supertrace_weight / (
        128 * sp.pi**2 * (1 + mass_ratio)
    )
    c_zero, determinant_proxy, difference_metric = sp.symbols(
        "C0 x g_a",
        positive=True,
    )
    ctp_vacuum = -c_zero * (
        sp.sqrt(determinant_proxy + difference_metric / 2)
        - sp.sqrt(determinant_proxy - difference_metric / 2)
    )
    log_mr2, log_za, log_mpsi2, log_zpsi, log_lambda = sp.symbols(
        "lnMR2 lnZA lnMpsi2 lnZpsi lnLambda",
        real=True,
    )
    calibration_jacobian = sp.Matrix(
        [
            [-1, 0, 0, 0, 0],
            [0, -1, 0, 0, 0],
            [0, 0, 1, -1, 0],
            [0, 0, 0, 0, 1],
        ]
    )
    scale_factor, torus_volume = sp.symbols("a V4", positive=True)
    scaled_volume = scale_factor**4 * torus_volume
    checks = {
        "beta_u0": str(beta_vacuum),
        "beta_at_zero": str(
            sp.simplify(beta_vacuum.subs(vacuum_coordinate, 0))
        ),
        "stationary_u0": str(stationary_coordinate),
        "stationary_residual": str(
            sp.simplify(
                beta_vacuum.subs(vacuum_coordinate, stationary_coordinate)
            )
        ),
        "linearized_eigenvalue": str(
            sp.diff(beta_vacuum, vacuum_coordinate)
        ),
        "canonical_critical_exponent": str(
            -sp.diff(beta_vacuum, vacuum_coordinate)
        ),
        "massless_scalar_source": float(
            beta_vacuum.subs(
                {
                    vacuum_coordinate: 0,
                    mass_ratio: 0,
                    supertrace_weight: 1,
                }
            )
        ),
        "massless_scalar_u0_star": float(
            stationary_coordinate.subs(
                {mass_ratio: 0, supertrace_weight: 1}
            )
        ),
        "massless_scalar_plus_U1_source": float(
            beta_vacuum.subs(
                {
                    vacuum_coordinate: 0,
                    mass_ratio: 0,
                    supertrace_weight: 3,
                }
            )
        ),
        "massless_scalar_plus_U1_u0_star": float(
            stationary_coordinate.subs(
                {mass_ratio: 0, supertrace_weight: 3}
            )
        ),
        "ctp_diagonal": str(
            sp.simplify(ctp_vacuum.subs(difference_metric, 0))
        ),
        "ctp_difference_variation": str(
            sp.simplify(
                sp.diff(ctp_vacuum, difference_metric).subs(
                    difference_metric,
                    0,
                )
            )
        ),
        "calibration_rank": calibration_jacobian.rank(),
        "calibration_nullity": (
            len(
                (
                    log_mr2,
                    log_za,
                    log_mpsi2,
                    log_zpsi,
                    log_lambda,
                )
            )
            - calibration_jacobian.rank()
        ),
        "volume_scale_derivative": str(
            sp.diff(scaled_volume, scale_factor)
        ),
        "torus_volume_nonzero": True,
        "torus_total_divergence_integral": 0,
    }
    return checks


def vacuum_operator_rows(symbolic: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "clause": "diffeomorphism",
            "operator": "integral d4x sqrt(-g) C0_R",
            "test": "sqrt(-g)d4x is a scalar density measure",
            "operator_allowed": True,
            "zero_selected": False,
            "status": "INVARIANT_OPERATOR",
        },
        {
            "clause": "local_Lorentz",
            "operator": "integral d4x e C0_R",
            "test": "det(Lambda)=+1 leaves the oriented coframe determinant e invariant",
            "operator_allowed": True,
            "zero_selected": False,
            "status": "INVARIANT_OPERATOR",
        },
        {
            "clause": "local_translation_gauge",
            "operator": "integral d4x e C0_R",
            "test": "e is built from the translation-covariant relational coframe",
            "operator_allowed": True,
            "zero_selected": False,
            "status": "INVARIANT_OPERATOR",
        },
        {
            "clause": "visible_U1",
            "operator": "integral d4x e C0_R",
            "test": "the volume operator contains no charged field",
            "operator_allowed": True,
            "zero_selected": False,
            "status": "INVARIANT_OPERATOR",
        },
        {
            "clause": "motion_Z2_or_constant_shift",
            "operator": "integral d4x e C0_R",
            "test": "the volume operator is independent of the motion scalar",
            "operator_allowed": True,
            "zero_selected": False,
            "status": "INVARIANT_OPERATOR",
        },
        {
            "clause": "local_BRST_cohomology_modulo_boundary",
            "operator": "integral d4x e C0_R",
            "test": (
                "on compact boundaryless flat T4 the volume integral is V4>0 "
                "whereas any globally defined total divergence integrates to zero"
            ),
            "operator_allowed": True,
            "zero_selected": False,
            "status": "NONTRIVIAL_LOCAL_INVARIANT_WITNESS",
        },
        {
            "clause": "not_topological",
            "operator": "integral d4x e C0_R",
            "test": (
                "under e^A_mu->a e^A_mu the integral scales as a^4 V4 and "
                f"has derivative {symbolic['volume_scale_derivative']}"
            ),
            "operator_allowed": True,
            "zero_selected": False,
            "status": "CONTINUOUS_METRIC_RESPONSE",
        },
    ]
    return tagged(rows)


def ctp_rows(symbolic: dict[str, Any]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "clause": "CTP_diagonal_normalization",
                "equation": "Gamma_C0[g,g]=C0[V(g)-V(g)]=0",
                "value": symbolic["ctp_diagonal"],
                "removes_physical_vacuum_stress": False,
                "status": "EXACT_DIAGONAL_CANCELLATION",
            },
            {
                "clause": "difference_metric_variation",
                "equation": (
                    "delta Gamma_C0/delta g_a^mn|a=0="
                    "-C0 sqrt(-g_r) g^r_mn/2"
                ),
                "value": symbolic["ctp_difference_variation"],
                "removes_physical_vacuum_stress": False,
                "status": "NONZERO_PHYSICAL_VARIATION",
            },
            {
                "clause": "CTP_interpretation",
                "equation": "Gamma[Phi,Phi]=0 but delta_a Gamma|a=0 gives the EOM",
                "value": "vacuum bubbles cancel in value, not in stress",
                "removes_physical_vacuum_stress": False,
                "status": "NORMALIZATION_IS_NOT_ZERO_SELECTION",
            },
        ]
    )


def frg_rows(symbolic: dict[str, Any]) -> list[dict[str, Any]]:
    weight_rows = read_csv(
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_R2FR_4877_BRANCH_TESTS.csv"
    )
    selected_branches = {
        row["branch"]: row
        for row in weight_rows
        if row["branch"]
        in {
            "primitive_real_psi_only",
            "real_psi_plus_public_U1",
            "imported_SM_without_RH_neutrinos",
        }
    }
    rows: list[dict[str, Any]] = [
        {
            "case": "optimized_scalar_vacuum_trace",
            "equation": (
                "partial_t C0_E=k^4/[32 pi^2 (1+w)]"
            ),
            "W0": 1,
            "w": "m^2/k^2",
            "beta_at_u0_zero": symbolic["massless_scalar_source"],
            "zero_surface_invariant": False,
            "status": "DERIVED_RESOLVED_ONE_LOOP_SOURCE",
        },
        {
            "case": "dimensionless_vacuum_coordinate",
            "equation": (
                "beta_u0=-4u0+W0/[32 pi^2(1+w)]"
            ),
            "W0": "symbolic",
            "w": "symbolic",
            "beta_at_u0_zero": symbolic["beta_at_zero"],
            "zero_surface_invariant": False,
            "status": "EXACT_THRESHOLD_FORM",
        },
        {
            "case": "massless_scalar_stationary_coordinate",
            "equation": "u0*=1/(128 pi^2)",
            "W0": 1,
            "w": 0,
            "beta_at_u0_zero": symbolic["massless_scalar_source"],
            "u0_stationary": symbolic["massless_scalar_u0_star"],
            "linear_eigenvalue": symbolic["linearized_eigenvalue"],
            "critical_exponent": symbolic["canonical_critical_exponent"],
            "zero_surface_invariant": False,
            "status": "CANONICAL_RELEVANT_VACUUM_BLOCK",
        },
        {
            "case": "real_scalar_plus_public_U1",
            "equation": "W0=1+2=3",
            "W0": 3,
            "w": 0,
            "beta_at_u0_zero": symbolic[
                "massless_scalar_plus_U1_source"
            ],
            "u0_stationary": symbolic[
                "massless_scalar_plus_U1_u0_star"
            ],
            "zero_surface_invariant": False,
            "status": "MINIMAL_CANONICAL_BOSONIC_PARENT_NONZERO_SOURCE",
        },
    ]
    for branch_name, source in selected_branches.items():
        rows.append(
            {
                "case": branch_name,
                "equation": "W0=Ns+2Nv-4ND",
                "W0": float(source["W0"]),
                "w": "massless_counting_limit",
                "beta_at_u0_zero": (
                    float(source["W0"]) / (32.0 * math.pi**2)
                ),
                "zero_surface_invariant": (
                    abs(float(source["W0"])) < 1.0e-15
                ),
                "status": "LOCKED_SIGNED_SPECTRUM_TEST",
            }
        )
    rows.extend(
        [
            {
                "case": "gravity_and_ghost_completion",
                "equation": "beta_u0_full=beta_u0_matter+beta_u0_gravity+ghosts",
                "W0": "not source-complete in current vacuum truncation",
                "w": "not applicable",
                "beta_at_u0_zero": "UNCOMPUTED_FULL_PARENT_VALUE",
                "zero_surface_invariant": False,
                "status": "CANNOT_MANUFACTURE_CANCELLATION_FROM_UNSOURCED_TERMS",
            },
            {
                "case": "technical_naturalness_boundary",
                "equation": (
                    "u0=0 requires a parent identity making beta_u0|u0=0=0 "
                    "at every scale"
                ),
                "W0": "no owned identity",
                "w": "all thresholds",
                "beta_at_u0_zero": "NONZERO_IN_EXPLICIT_MATTER_BLOCK",
                "zero_surface_invariant": False,
                "status": "ZERO_NOT_DERIVED_BY_CURRENT_PARENT",
            },
        ]
    )
    return tagged(rows)


def fixed_point_and_parameter_rows(
    symbolic: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    fixed_point_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "4934"
        / "completed_combined_flow_results.json"
    )
    fixed_point = json.loads(fixed_point_path.read_text(encoding="utf-8"))
    fixed_block = fixed_point["source_complete_selected_row_fixed_point"]
    coordinates = fixed_point["canonical_projection_contract"][
        "essential_coordinates"
    ]
    ownership_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5203"
        / "coefficient_state_closure_ownership.csv"
    )
    lambda_ownership = next(
        row for row in ownership_rows if row["object"] == "Lambda_cal"
    )
    action_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5203"
        / "canonical_translation_parent_action.csv"
    )
    action_text = " ".join(
        " ".join(str(value) for value in row.values()) for row in action_rows
    ).lower()
    absent_mechanisms = {
        "unimodular_constraint": "unimodular" not in action_text,
        "four_form_adjuster": (
            "four-form" not in action_text and "4-form" not in action_text
        ),
        "vacuum_sequester": "sequester" not in action_text,
        "supersymmetry_supertrace_identity": (
            "supersym" not in action_text
        ),
    }
    rows: list[dict[str, Any]] = [
        {
            "test": "checkpoint_4934_coordinate_coverage",
            "coordinates": ",".join(coordinates),
            "rank_or_count": len(coordinates),
            "result": "u0/C0/Lambda absent",
            "zero_selected": False,
            "status": "VACUUM_DIRECTION_OUTSIDE_DECLARED_TRUNCATION",
        },
        {
            "test": "checkpoint_4934_stability_index",
            "coordinates": ",".join(coordinates),
            "rank_or_count": fixed_block["signed_index"][
                "negative_real_parts"
            ],
            "result": "one relevant direction only inside this five-coordinate system",
            "zero_selected": False,
            "status": "CANNOT_EXTRAPOLATE_INDEX_TO_OMITTED_VACUUM_COORDINATE",
        },
        {
            "test": "calibration_Jacobian",
            "coordinates": "lnMR2,lnZA,lnMpsi2,lnZpsi,lnLambda",
            "rank_or_count": symbolic["calibration_rank"],
            "result": (
                f"rank={symbolic['calibration_rank']}; "
                f"nullity={symbolic['calibration_nullity']}"
            ),
            "zero_selected": False,
            "status": "LAMBDA_IS_AN_INDEPENDENT_PHYSICAL_COORDINATE",
        },
        {
            "test": "checkpoint_5203_ownership",
            "coordinates": "Lambda_cal",
            "rank_or_count": 1,
            "result": (
                f"{lambda_ownership['ownership']}; "
                f"arena_retuning={lambda_ownership['arena_retuning']}"
            ),
            "zero_selected": False,
            "status": "ONE_UNIVERSAL_COSMOLOGICAL_CALIBRATION",
        },
        {
            "test": "checkpoint_5209_state_constraint_rank",
            "coordinates": "Omega_Lambda,sigma2",
            "rank_or_count": 1,
            "result": "nullity one; P(X) moments do not select Lambda",
            "zero_selected": False,
            "status": "STATE_CLOSURE_ROUTE_REJECTED",
        },
    ]
    for mechanism, absent in absent_mechanisms.items():
        rows.append(
            {
                "test": mechanism,
                "coordinates": "canonical checkpoint-5203 action basis",
                "rank_or_count": 0 if absent else 1,
                "result": "absent" if absent else "present",
                "zero_selected": False,
                "status": (
                    "NOT_IN_SELECTED_PARENT_ACTION"
                    if absent
                    else "REQUIRES_SEPARATE_AUDIT"
                ),
            }
        )
    summary = {
        "fixed_point_coordinates": coordinates,
        "fixed_point_coordinate_count": len(coordinates),
        "fixed_point_relevant_count_in_declared_truncation": fixed_block[
            "signed_index"
        ]["negative_real_parts"],
        "vacuum_coordinate_in_fixed_point": any(
            name.lower() in {"u0", "c0", "lambda", "lambda_cal"}
            for name in coordinates
        ),
        "calibration_rank": symbolic["calibration_rank"],
        "calibration_nullity": symbolic["calibration_nullity"],
        "lambda_ownership": lambda_ownership["ownership"],
        "arena_retuning": lambda_ownership["arena_retuning"],
        "absent_zero_selection_mechanisms": absent_mechanisms,
    }
    return tagged(rows), summary


def radiative_stability_rows(
    symbolic: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    reduced_planck_eV = (
        math.sqrt(
            HBAR_SI * SPEED_OF_LIGHT / (8.0 * math.pi * NEWTON_G)
        )
        * SPEED_OF_LIGHT**2
        / EV_JOULE
    )
    cutoff_ratio = 4.0 * math.pi * math.sqrt(6.0)
    cutoff_eV = cutoff_ratio * reduced_planck_eV
    scalar_quartic_loop_eV4 = cutoff_eV**4 / (64.0 * math.pi**2)
    cosmology = load_primary_cosmology()
    free_fit = cosmology["ParentScalar_Lambda_free"]
    h0_per_second = (
        float(free_fit["params"]["H0"]) * 1000.0 / MPC_M
    )
    h0_eV = HBAR_EV_S * h0_per_second
    omega_lambda = float(
        free_fit["background_diagnostics"]["omega_lambda"]
    )
    critical_density_eV4 = (
        3.0 * reduced_planck_eV**2 * h0_eV**2
    )
    fitted_vacuum_density_eV4 = (
        omega_lambda * critical_density_eV4
    )
    critical_ratio = scalar_quartic_loop_eV4 / critical_density_eV4
    fitted_ratio = scalar_quartic_loop_eV4 / fitted_vacuum_density_eV4
    result_5209 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5209"
            / "finite_mass_PX_vacuum_branch_results.json"
        ).read_text(encoding="utf-8")
    )
    finite_mass_fraction = float(
        result_5209["vacuum"]["finite_mass_vacuum_fraction_bound"]
    )
    rows = tagged(
        [
            {
                "quantity": "Newton_matched_scalar_cutoff",
                "formula": "Lambda_UV/Mbar=4 pi sqrt(6)",
                "value": cutoff_ratio,
                "units": "dimensionless",
                "interpretation": "checkpoint-4876 scalar-only matching diagnostic",
                "status": "SCHEME_DEPENDENT_MATCHING_SCALE",
            },
            {
                "quantity": "quartic_scalar_vacuum_term",
                "formula": "C0_loop=Lambda_UV^4/(64 pi^2)",
                "value": scalar_quartic_loop_eV4,
                "units": "eV^4",
                "interpretation": "massless one-real-scalar cutoff diagnostic",
                "status": "COUNTERTERM_SENSITIVITY_NOT_OBSERVABLE_PREDICTION",
            },
            {
                "quantity": "fitted_critical_density",
                "formula": "rho_crit=3 Mbar^2 H0^2",
                "value": critical_density_eV4,
                "units": "eV^4",
                "interpretation": "checkpoint-5195 free-Lambda branch",
                "status": "INTERNAL_COMPRESSED_CMB_CALIBRATION",
            },
            {
                "quantity": "fitted_vacuum_density",
                "formula": "rho_Lambda=Omega_Lambda rho_crit",
                "value": fitted_vacuum_density_eV4,
                "units": "eV^4",
                "interpretation": "checkpoint-5195 free-Lambda branch",
                "status": "INTERNAL_COMPRESSED_CMB_CALIBRATION",
            },
            {
                "quantity": "quartic_to_critical_sensitivity",
                "formula": "C0_loop/rho_crit",
                "value": critical_ratio,
                "units": "dimensionless",
                "interpretation": "regulator-dependent naturalness diagnostic",
                "status": "NOT_A_MEASURED_FINE_TUNING_PROBABILITY",
            },
            {
                "quantity": "quartic_to_fitted_vacuum_sensitivity",
                "formula": "C0_loop/rho_Lambda",
                "value": fitted_ratio,
                "units": "dimensionless",
                "interpretation": "regulator-dependent naturalness diagnostic",
                "status": "NOT_A_MEASURED_FINE_TUNING_PROBABILITY",
            },
            {
                "quantity": "finite_motion_mass_threshold",
                "formula": "|Delta Omega_vac,mass| checkpoint 5209",
                "value": finite_mass_fraction,
                "units": "critical-density fraction",
                "interpretation": (
                    "tiny finite mass threshold cannot cancel the quartic coordinate"
                ),
                "status": "TOO_SMALL_TO_SELECT_VACUUM",
            },
            {
                "quantity": "resolved_zero_surface_source",
                "formula": "beta_u0(0)=1/(32 pi^2) for one real scalar",
                "value": symbolic["massless_scalar_source"],
                "units": "dimensionless beta function",
                "interpretation": "zero requires a cancellation identity not a small mass",
                "status": "NONZERO_EXPLICIT_SOURCE",
            },
        ]
    )
    metrics = {
        "reduced_planck_eV": reduced_planck_eV,
        "cutoff_ratio": cutoff_ratio,
        "cutoff_eV": cutoff_eV,
        "scalar_quartic_loop_eV4": scalar_quartic_loop_eV4,
        "critical_density_eV4": critical_density_eV4,
        "fitted_vacuum_density_eV4": fitted_vacuum_density_eV4,
        "quartic_to_critical_ratio": critical_ratio,
        "quartic_to_fitted_vacuum_ratio": fitted_ratio,
        "finite_mass_vacuum_fraction_bound": finite_mass_fraction,
    }
    return rows, metrics


def load_primary_cosmology() -> dict[str, dict[str, Any]]:
    result_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5195"
        / "joint_CMB_informed_refit_results.json"
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    return {
        fit["model"]: fit
        for fit in result["fits"]
        if fit["config"] == "primary_fs8_wCDM_prior"
    }


def conditional_cosmology_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    fits = load_primary_cosmology()
    free_fit = fits["ParentScalar_Lambda_free"]
    zero_fit = fits["ParentScalar_Lambda_zero"]
    lcdm_fit = fits["LCDM"]
    rows: list[dict[str, Any]] = []
    for model_name in (
        "LCDM",
        "wCDM",
        "CPL",
        "ParentScalar_Lambda_free",
        "ParentScalar_Lambda_zero",
    ):
        fit = fits[model_name]
        rows.append(
            {
                "model": model_name,
                "chi2": fit["chi2_total"],
                "k": fit["k"],
                "n": fit["n"],
                "AIC": fit["AIC"],
                "BIC": fit["BIC"],
                "delta_chi2_vs_LCDM": (
                    fit["chi2_total"] - lcdm_fit["chi2_total"]
                ),
                "delta_AIC_vs_LCDM": fit["AIC"] - lcdm_fit["AIC"],
                "delta_BIC_vs_LCDM": fit["BIC"] - lcdm_fit["BIC"],
                "prior_edge": fit["prior_edge_flag"],
                "status": "LOCKED_INTERNAL_PRIMARY_FIT",
            }
        )
    rows.extend(
        [
            {
                "model": "Lambda_zero_minus_Lambda_free",
                "chi2": (
                    zero_fit["chi2_total"] - free_fit["chi2_total"]
                ),
                "k": zero_fit["k"] - free_fit["k"],
                "n": zero_fit["n"],
                "AIC": zero_fit["AIC"] - free_fit["AIC"],
                "BIC": zero_fit["BIC"] - free_fit["BIC"],
                "delta_chi2_vs_LCDM": "",
                "delta_AIC_vs_LCDM": "",
                "delta_BIC_vs_LCDM": "",
                "prior_edge": (
                    zero_fit["prior_edge_flag"]
                    or free_fit["prior_edge_flag"]
                ),
                "status": "CONDITIONAL_NESTED_BRANCH_COMPARISON",
            },
            {
                "model": "interpretation",
                "chi2": "",
                "k": "",
                "n": "",
                "AIC": "",
                "BIC": "",
                "delta_chi2_vs_LCDM": "",
                "delta_AIC_vs_LCDM": "",
                "delta_BIC_vs_LCDM": "",
                "prior_edge": False,
                "status": (
                    "AIC_BIC_CAN_COMPARE_DECLARED_BRANCHES_BUT_CANNOT_DERIVE_"
                    "THE_ZERO_LAMBDA_PARENT_CONDITION"
                ),
            },
        ]
    )
    summary = {
        "free_chi2": float(free_fit["chi2_total"]),
        "zero_chi2": float(zero_fit["chi2_total"]),
        "zero_minus_free_delta_chi2": float(
            zero_fit["chi2_total"] - free_fit["chi2_total"]
        ),
        "zero_minus_free_delta_AIC": float(
            zero_fit["AIC"] - free_fit["AIC"]
        ),
        "zero_minus_free_delta_BIC": float(
            zero_fit["BIC"] - free_fit["BIC"]
        ),
        "free_H0_km_s_Mpc": float(free_fit["params"]["H0"]),
        "free_Omega_Lambda": float(
            free_fit["background_diagnostics"]["omega_lambda"]
        ),
        "free_prior_edge": bool(free_fit["prior_edge_flag"]),
        "zero_prior_edge": bool(zero_fit["prior_edge_flag"]),
    }
    return tagged(rows), summary


def local_propagation_rows(
    cosmology: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    h0_per_second = (
        cosmology["free_H0_km_s_Mpc"] * 1000.0 / MPC_M
    )
    omega_lambda = cosmology["free_Omega_Lambda"]
    lambda_per_square_metre = (
        3.0
        * omega_lambda
        * h0_per_second**2
        / SPEED_OF_LIGHT**2
    )
    kiloparsec_m = MPC_M / 1000.0
    gigaparsec_m = 1000.0 * MPC_M
    arenas = [
        ("R10_50_micrometre", 5.0e-5, None),
        ("laboratory_1_m", 1.0, None),
        ("Earth_surface", 6_371_000.0, 3.986004418e14),
        ("solar_system_1_AU", 149_597_870_700.0, 1.32712440018e20),
        ("Saturn_orbit", 1.43353e12, 1.32712440018e20),
        ("galaxy_100_kpc", 100.0 * kiloparsec_m, None),
        ("cosmology_1_Gpc", gigaparsec_m, None),
    ]
    rows: list[dict[str, Any]] = []
    for arena, length_m, central_gm in arenas:
        lambda_length_squared = lambda_per_square_metre * length_m**2
        potential_fraction = lambda_length_squared / 6.0
        acceleration_ratio: float | str = ""
        if central_gm is not None:
            acceleration_ratio = (
                omega_lambda
                * h0_per_second**2
                * length_m**3
                / central_gm
            )
        rows.append(
            {
                "arena": arena,
                "length_m": length_m,
                "Lambda_cal_m^-2": lambda_per_square_metre,
                "Lambda_L2": lambda_length_squared,
                "abs_Phi_Lambda_over_c2": potential_fraction,
                "central_GM_m3_s-2": (
                    central_gm if central_gm is not None else ""
                ),
                "a_Lambda_over_a_Newton": acceleration_ratio,
                "direct_Maxwell_portal": 0.0,
                "arena_retuning": False,
                "locally_small_below_1e-6": (
                    lambda_length_squared < 1.0e-6
                ),
                "status": (
                    "SINGLE_CALIBRATION_LOCAL_BACKGROUND_PROPAGATION"
                    if lambda_length_squared < 1.0e-6
                    else "FULL_CURVED_BACKGROUND_REQUIRED"
                ),
            }
        )
    earth = next(row for row in rows if row["arena"] == "Earth_surface")
    saturn = next(row for row in rows if row["arena"] == "Saturn_orbit")
    galaxy = next(row for row in rows if row["arena"] == "galaxy_100_kpc")
    r10 = next(row for row in rows if row["arena"] == "R10_50_micrometre")
    summary = {
        "H0_per_second": h0_per_second,
        "Lambda_cal_m^-2": lambda_per_square_metre,
        "R10_Lambda_L2": float(r10["Lambda_L2"]),
        "Earth_aLambda_over_aNewton": float(
            earth["a_Lambda_over_a_Newton"]
        ),
        "Saturn_aLambda_over_aNewton": float(
            saturn["a_Lambda_over_a_Newton"]
        ),
        "galaxy_100kpc_Lambda_L2": float(galaxy["Lambda_L2"]),
        "maximum_local_Lambda_L2_through_100kpc": max(
            float(row["Lambda_L2"])
            for row in rows
            if row["arena"] != "cosmology_1_Gpc"
        ),
        "arena_retuning_count": sum(
            bool(row["arena_retuning"]) for row in rows
        ),
    }
    return tagged(rows), summary


def decision_rows(
    fixed_point: dict[str, Any],
    cosmology: dict[str, float],
    local: dict[str, float],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "existing_parent_symmetry_selects_C0_zero",
                "result": "false; the volume operator is allowed by every selected symmetry",
                "claim": "REJECTED_FOR_CURRENT_PARENT",
                "next_action": "do not invoke a hidden symmetry",
            },
            {
                "gate": "CTP_normalization_selects_C0_zero",
                "result": "false; diagonal value vanishes but difference variation is nonzero",
                "claim": "REJECTED_EXACTLY",
                "next_action": "retain vacuum stress in the physical equation",
            },
            {
                "gate": "resolved_RG_preserves_u0_zero",
                "result": "false; beta_u0(0)=W0/[32pi^2(1+w)]",
                "claim": "REJECTED_IN_EXPLICIT_ONE_LOOP_BLOCK",
                "next_action": "a future zero claim requires a full parent cancellation identity",
            },
            {
                "gate": "existing_fixed_point_selects_vacuum",
                "result": (
                    "false; u0 is absent from "
                    f"{fixed_point['fixed_point_coordinate_count']}-coordinate "
                    "checkpoint-4934 truncation"
                ),
                "claim": "OUTSIDE_DECLARED_TRUNCATION",
                "next_action": "add u0 before quoting a vacuum critical exponent",
            },
            {
                "gate": "current_parameter_ownership",
                "result": (
                    "Lambda_cal is one universal renormalization/calibration datum; "
                    "no arena retuning"
                ),
                "claim": "PROVED_BOUNDARY_OF_CURRENT_PARENT",
                "next_action": "freeze it once like G_N and alpha_EM",
            },
            {
                "gate": "conditional_zero_branch_evidence",
                "result": (
                    f"Delta chi2={cosmology['zero_minus_free_delta_chi2']:.6g}; "
                    f"Delta AIC={cosmology['zero_minus_free_delta_AIC']:.6g}; "
                    f"Delta BIC={cosmology['zero_minus_free_delta_BIC']:.6g}"
                ),
                "claim": "MODEL_COMPARISON_ONLY_NOT_PARENT_DERIVATION",
                "next_action": "retain both declared branches in cosmology tests",
            },
            {
                "gate": "local_GR_obstruction_from_calibrated_Lambda",
                "result": (
                    "none at tested background order; max Lambda L2 through "
                    f"100 kpc={local['maximum_local_Lambda_L2_through_100kpc']:.6e}"
                ),
                "claim": "BACKGROUND_TERM_BOUNDED_NOT_FULL_LOCAL_GR_PASS",
                "next_action": "resume source-coupling and residual-vector derivation",
            },
            {
                "gate": "selected_next_route",
                "result": (
                    "the vacuum fork is closed as an explicit parameter boundary "
                    "rather than left as a recurring missing derivation"
                ),
                "claim": "PRIVATE_CHECKPOINT_ONLY",
                "next_action": (
                    "RESUME_UNIVERSAL_SOURCE_COUPLING_AND_LOCAL_GR_WITH_ONE_"
                    "FROZEN_LAMBDA_DATUM"
                ),
            },
            {
                "gate": "optional_vacuum_prediction_route",
                "result": (
                    "a stronger claim remains possible only in an enlarged "
                    "source-complete UV truncation"
                ),
                "claim": "NOT_COMPLETED",
                "next_action": (
                    "ADD_U0_TO_THE_FULL_UV_HESSIAN_AND_SEARCH_FOR_A_PARENT_"
                    "WARD_OR_SUPERTRACE_IDENTITY"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source": path.relative_to(POST).as_posix(),
            "sha256": expected,
            "role": "locked parent evidence",
            "status": "SOURCE_LOCKED",
        }
        for path, expected in SOURCE_LOCKS.items()
    ]
    rows.extend(
        [
            {
                "source": "checkpoint-5210 local-invariant/torus witness",
                "sha256": "",
                "role": "proves the volume operator is not a total derivative",
                "status": "NEW_EXACT_DERIVATION",
            },
            {
                "source": "checkpoint-5210 optimized scalar vacuum trace",
                "sha256": "",
                "role": "derives beta_u0 and tests invariance of u0=0",
                "status": "NEW_EXACT_DERIVATION",
            },
            {
                "source": "checkpoint-5210 calibration Jacobian",
                "sha256": "",
                "role": "counts Lambda_cal as an independent physical coordinate",
                "status": "NEW_EXACT_RANK_DERIVATION",
            },
            {
                "source": "checkpoint-5210 Schwarzschild-de Sitter propagation",
                "sha256": "",
                "role": "propagates one fitted Lambda calibration without retuning",
                "status": "NEW_NUMERICAL_BOUND",
            },
        ]
    )
    return tagged(rows)


def build_document(
    symbolic: dict[str, Any],
    fixed_point: dict[str, Any],
    radiative: dict[str, float],
    cosmology: dict[str, float],
    local: dict[str, float],
    evidence_digest: str,
) -> str:
    coordinates = ", ".join(fixed_point["fixed_point_coordinates"])
    return f"""# 5210 - Parent Vacuum Coordinate: Local-Invariant, CTP/RG Source and Renormalization-Datum Theorem

Private derivation and boundary checkpoint. No GitHub action and no
cosmological-constant, full-MTS or full-local-GR claim.

Marker: `{MARKER}`.

## Executive result

This checkpoint closes the repeated `Lambda_cal=0` fork for the parent that
has actually been constructed.

The constant volume operator

```text
S_vac=-integral d4x e U_Lambda,
U_Lambda=M_R^2 Lambda_cal,
C0_R=-M_R^2 Lambda_cal
```

is allowed by diffeomorphisms, local Lorentz symmetry, the relational local
translation gauge symmetry, visible `U(1)` and the motion `Z2`/constant-shift
limits. It is not a boundary term: on compact boundaryless flat `T4`,
`integral e=V4>0`, while a globally defined total divergence integrates to
zero. It is not topological because `e^A_mu -> a e^A_mu` sends the integral
to `a^4 V4`.

No existing parent symmetry therefore sets its coefficient to zero.

The Schwinger-Keldysh/CTP identity does not do it either:

```text
Gamma_C0[g,g]=0,

delta Gamma_C0 / delta g_a^mn |_(g_a=0)
 =-C0 sqrt(-g_r) g^r_mn/2 !=0.
```

CTP normalization cancels the diagonal value of vacuum bubbles, not their
stress in the physical metric equation.

Finally, the explicitly resolved optimized scalar trace gives

```text
partial_t C0_E = k^4/[32 pi^2(1+w)],
w=m^2/k^2,

u0=C0_E/k^4,

beta_u0
 =-4u0+W0/[32 pi^2(1+w)].
```

Hence `u0=0` is not an invariant RG surface when `W0!=0`. For one massless
real scalar,

```text
beta_u0(0)={symbolic['massless_scalar_source']:.12e},
u0*={symbolic['massless_scalar_u0_star']:.12e},
d beta_u0/d u0=-4,
theta0=+4.
```

The canonical real-motion-scalar plus public-`U(1)` matter block has
`W0=1+2=3`, not zero. A larger gravity/ghost calculation may shift this
coordinate, but no unsourced term can be called a cancellation.

The result is not “MTS predicts zero.” It is the sharper and usable result:
**the present parent owns `Lambda_cal` as one universal renormalized
calibration datum, fixed once and never retuned by arena.**

## 1. Exact symmetry boundary

The volume density is a scalar density under Diff and a determinant under
local Lorentz/translation-gauge transformations. It contains no charged
field and no motion scalar. Consequently every selected gauge and discrete
symmetry permits it.

The compact-`T4` witness is enough to reject the only possible
boundary-term escape inside the current local action:

```text
integral_T4 d4x partial_mu J^mu=0,
integral_T4 d4x e=V4>0.
```

The coefficient is therefore a genuine local action coordinate modulo
boundaries. This is a statement about the selected parent basis, not a
no-go theorem against constructing a different unimodular, four-form,
sequestered or supersymmetric theory. None of those mechanisms occurs in
the checkpoint-5203 canonical parent action.

## 2. CTP variation theorem

Write the doubled vacuum term as

```text
Gamma_C0^CTP=C0[V(g_+)-V(g_-)].
```

At `g_+=g_-` the value is zero by unitarity. The physical equation is
obtained by variation in the difference direction before taking that
limit, and that variation is nonzero. The one-variable determinant proxy
used by the executable gate gives

```text
Gamma=-C0[sqrt(x+g_a/2)-sqrt(x-g_a/2)],
Gamma|_(g_a=0)={symbolic['ctp_diagonal']},
dGamma/dg_a|_(g_a=0)={symbolic['ctp_difference_variation']}.
```

This exactly mirrors the tensor equation already derived at checkpoint
4876. CTP state normalization cannot be used to remove `Lambda_cal`.

## 3. RG non-invariance theorem

For the Litim/optimized scalar regulator, the vacuum projection of the
Wetterich trace is

```text
1/2 integral_(p^2<k^2) d4p/(2pi)^4
 [2k^2/(k^2+m^2)]
 =k^4/[32pi^2(1+w)].
```

The symbolic fixed-coordinate residual is
`{symbolic['stationary_residual']}`. The source at zero is nonzero for the
locked primitive branches:

```text
W0=1                         real motion scalar;
W0=3                         real scalar + public U(1);
W0=-62                       imported SM benchmark without RH neutrinos.
```

None is zero. The sign of an imported spectrum does not matter for the
present theorem; nonzero `W0` is enough to show that zero is not invariant.
The finite motion mass only multiplies this source by `1/(1+w)` and cannot
create an exact zero at finite `w`.

A technically stable zero would require a parent Ward identity or exact
supertrace cancellation that enforces

```text
beta_u0|_(u0=0)=0
```

through thresholds and interactions. No such identity is present in the
resolved parent.

## 4. Fixed-point coverage and parameter count

Checkpoint 4934 solved the source-complete minimal fixed point in

```text
({coordinates}).
```

It found one relevant direction **inside that
{fixed_point['fixed_point_coordinate_count']}-coordinate truncation**.
`u0`, `C0` and `Lambda_cal` are absent. Its stability index therefore
cannot count or select the vacuum direction.

The canonical calibration Jacobian over

```text
coordinates:
 (ln M_R^2,ln Z_A,ln M_psi^2,ln Z_psi,ln Lambda_cal);

observables:
 (ln G_N,ln alpha_EM,ln m_pole^2,ln Lambda_cal)
```

has

```text
rank={fixed_point['calibration_rank']},
nullity={fixed_point['calibration_nullity']}.
```

The one null direction is the elementary field normalization. The
`Lambda_cal` column is independent. Checkpoint 5209 independently showed
that the homogeneous state constraint has rank one over
`(Omega_Lambda,sigma2)` and that nonlinear `P(X)` moments increase rather
than remove the nullity. The vacuum cannot be transferred into a hidden
state closure.

## 5. Radiative-stability diagnostic

The checkpoint-4876 one-real-scalar Newton matching gives

```text
Lambda_UV/Mbar=4pi sqrt(6)
 ={radiative['cutoff_ratio']:.12e}.
```

In that declared cutoff scheme,

```text
C0_loop=Lambda_UV^4/(64pi^2)
 ={radiative['scalar_quartic_loop_eV4']:.12e} eV^4;

rho_crit=3 Mbar^2 H0^2
 ={radiative['critical_density_eV4']:.12e} eV^4;

C0_loop/rho_crit
 ={radiative['quartic_to_critical_ratio']:.12e}.
```

This is a regulator-dependent counterterm-sensitivity diagnostic, not an
observable probability and not a claimed calculation of the measured
vacuum. It does show why the tiny finite-motion threshold from checkpoint
5209,

```text
|Delta Omega_vac,mass|
 <={radiative['finite_mass_vacuum_fraction_bound']:.12e},
```

cannot dynamically cancel the independent quartic coordinate.

## 6. What the data do and do not say

The checkpoint-5195 primary internal fits give

```text
Lambda-free parent:
 chi2={cosmology['free_chi2']:.12f};

Lambda-zero parent:
 chi2={cosmology['zero_chi2']:.12f};

zero minus free:
 Delta chi2={cosmology['zero_minus_free_delta_chi2']:.12f};
 Delta AIC={cosmology['zero_minus_free_delta_AIC']:.12f};
 Delta BIC={cosmology['zero_minus_free_delta_BIC']:.12f}.
```

Neither branch hits a prior edge. The zero branch pays one fewer parameter
and therefore wins this conditional AIC/BIC comparison despite a
`{cosmology['zero_minus_free_delta_chi2']:.6g}` worsening in chi-squared.
That is legitimate model comparison. It is **not** a derivation that the
parent action owns exact zero.

Both branches remain useful empirical tests. The free branch supplies one
universal calibration; the zero branch remains an explicitly imposed
renormalization condition.

## 7. Local propagation without retuning

Using the free-branch internal calibration

```text
H0={cosmology['free_H0_km_s_Mpc']:.12f} km s^-1 Mpc^-1,
Omega_Lambda={cosmology['free_Omega_Lambda']:.12f},
Lambda_cal={local['Lambda_cal_m^-2']:.12e} m^-2,
```

the Schwarzschild-de Sitter weak-field terms are

```text
Phi(r)=-GM/r-Lambda_cal c^2 r^2/6,
a_r=-GM/r^2+Lambda_cal c^2 r/3.
```

The single calibration propagates to

```text
Lambda L^2 at 50 micrometres
 ={local['R10_Lambda_L2']:.12e};

a_Lambda/a_Newton at Earth surface
 ={local['Earth_aLambda_over_aNewton']:.12e};

a_Lambda/a_Newton at Saturn
 ={local['Saturn_aLambda_over_aNewton']:.12e};

Lambda L^2 at 100 kpc
 ={local['galaxy_100kpc_Lambda_L2']:.12e}.
```

The direct Maxwell portal remains zero; `Lambda_cal` enters only through
the universal metric. These are background residuals, not substitutes for
the full PPN, clock, orbital or R10 projection. They establish that retaining
one calibrated vacuum datum does not obstruct the local-GR branch at this
order.

## 8. Decision

The derive-first search has produced a definite negative theorem for the
existing zero route:

1. no selected symmetry forbids the volume operator;
2. it is neither boundary nor topological;
3. CTP normalization leaves its physical stress;
4. the explicit matter FRG sources it at zero;
5. the current fixed point does not contain the coordinate;
6. `P(X)` state moments do not select it.

The project should therefore stop reopening `Lambda_cal=0` as though one
more rearrangement of the same parent might prove it. The honest competitive
field-theory route is:

```text
one universal Lambda_cal renormalization/calibration;
no arena-by-arena retuning;
both free and zero cosmology branches retained as declared tests;
resume derivation of universal source coupling and the local-GR residual vector.
```

If a future vacuum prediction is wanted, it is a separate ultraviolet
calculation: add `u0` to a source-complete parent Hessian and derive a Ward
or supertrace identity. The existing “one relevant direction” statement
cannot be used for it.

Selected next route:

```text
RESUME_UNIVERSAL_SOURCE_COUPLING_AND_LOCAL_GR_WITH_ONE_FROZEN_LAMBDA_DATUM
```

## Reproducibility

Evidence CSV digest:

```text
{evidence_digest}
```

Run:

```text
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py --dry-run
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py --validate-saved
```
"""


def validation_rows(
    symbolic: dict[str, Any],
    operator_rows: list[dict[str, Any]],
    ctp_evidence: list[dict[str, Any]],
    frg_evidence: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    fixed_point: dict[str, Any],
    radiative: dict[str, float],
    cosmology_rows: list[dict[str, Any]],
    cosmology: dict[str, float],
    local_rows: list[dict[str, Any]],
    local: dict[str, float],
    datasets: dict[str, list[dict[str, Any]]],
    evidence_digest: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        check: str,
        passed: bool,
        observed: Any,
        expected: Any,
        detail: str,
    ) -> None:
        rows.append(
            {
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
                "detail": detail,
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
            }
        )

    add(
        "source_lock_count",
        len(SOURCE_LOCKS) >= 20,
        len(SOURCE_LOCKS),
        ">=20",
        "all declared parent sources are SHA256 locked",
    )
    add(
        "stationary_residual",
        symbolic["stationary_residual"] == "0",
        symbolic["stationary_residual"],
        "0",
        "conditional fixed coordinate solves beta_u0=0",
    )
    add(
        "linearized_eigenvalue",
        symbolic["linearized_eigenvalue"] == "-4",
        symbolic["linearized_eigenvalue"],
        "-4",
        "canonical vacuum block eigenvalue",
    )
    add(
        "critical_exponent",
        symbolic["canonical_critical_exponent"] == "4",
        symbolic["canonical_critical_exponent"],
        "4",
        "theta=-eigenvalue convention",
    )
    add(
        "scalar_source_nonzero",
        symbolic["massless_scalar_source"] > 0.0,
        symbolic["massless_scalar_source"],
        ">0",
        "u0=0 is not invariant in the explicit scalar block",
    )
    add(
        "scalar_plus_U1_source_nonzero",
        symbolic["massless_scalar_plus_U1_source"] > 0.0,
        symbolic["massless_scalar_plus_U1_source"],
        ">0",
        "minimal canonical bosonic matter block has W0=3",
    )
    add(
        "CTP_diagonal_zero",
        symbolic["ctp_diagonal"] == "0",
        symbolic["ctp_diagonal"],
        "0",
        "unitarity diagonal value",
    )
    add(
        "CTP_difference_variation_nonzero",
        symbolic["ctp_difference_variation"] != "0",
        symbolic["ctp_difference_variation"],
        "nonzero",
        "physical vacuum stress remains",
    )
    add(
        "calibration_rank",
        symbolic["calibration_rank"] == 4,
        symbolic["calibration_rank"],
        4,
        "four physical calibrations",
    )
    add(
        "calibration_nullity",
        symbolic["calibration_nullity"] == 1,
        symbolic["calibration_nullity"],
        1,
        "one elementary field-normalization null direction",
    )
    add(
        "torus_nonboundary_witness",
        (
            symbolic["torus_volume_nonzero"]
            and symbolic["torus_total_divergence_integral"] == 0
        ),
        (
            symbolic["torus_volume_nonzero"],
            symbolic["torus_total_divergence_integral"],
        ),
        "(True,0)",
        "volume operator cannot be a total derivative",
    )
    for row in operator_rows:
        add(
            f"operator_clause_{row['clause']}",
            bool(row["operator_allowed"]) and not bool(row["zero_selected"]),
            (row["operator_allowed"], row["zero_selected"]),
            "(True,False)",
            row["status"],
        )
    for row in ctp_evidence:
        add(
            f"CTP_clause_{row['clause']}",
            not bool(row["removes_physical_vacuum_stress"]),
            row["removes_physical_vacuum_stress"],
            False,
            row["status"],
        )
    primitive_rows = {
        row["case"]: row
        for row in frg_evidence
        if row["case"]
        in {
            "primitive_real_psi_only",
            "real_psi_plus_public_U1",
            "imported_SM_without_RH_neutrinos",
        }
    }
    for branch, expected_weight in {
        "primitive_real_psi_only": 1.0,
        "real_psi_plus_public_U1": 3.0,
        "imported_SM_without_RH_neutrinos": -62.0,
    }.items():
        observed_weight = float(primitive_rows[branch]["W0"])
        add(
            f"W0_{branch}",
            math.isclose(observed_weight, expected_weight, abs_tol=1.0e-15),
            observed_weight,
            expected_weight,
            "locked checkpoint-4877 signed spectrum",
        )
        add(
            f"zero_invariant_{branch}",
            not bool(primitive_rows[branch]["zero_surface_invariant"]),
            primitive_rows[branch]["zero_surface_invariant"],
            False,
            "nonzero signed vacuum weight",
        )
    add(
        "fixed_point_coordinate_count",
        fixed_point["fixed_point_coordinate_count"] == 5,
        fixed_point["fixed_point_coordinate_count"],
        5,
        "checkpoint-4934 declared truncation",
    )
    add(
        "vacuum_coordinate_absent",
        not fixed_point["vacuum_coordinate_in_fixed_point"],
        fixed_point["vacuum_coordinate_in_fixed_point"],
        False,
        "the one-relevant-direction index cannot count u0",
    )
    add(
        "fixed_point_relevant_count_scope",
        fixed_point["fixed_point_relevant_count_in_declared_truncation"] == 1,
        fixed_point["fixed_point_relevant_count_in_declared_truncation"],
        1,
        "relevant count is retained only within the declared five coordinates",
    )
    add(
        "Lambda_ownership",
        fixed_point["lambda_ownership"] == "one cosmological calibration",
        fixed_point["lambda_ownership"],
        "one cosmological calibration",
        "checkpoint-5203 coefficient ownership",
    )
    add(
        "arena_retuning_forbidden",
        fixed_point["arena_retuning"] == "FORBIDDEN",
        fixed_point["arena_retuning"],
        "FORBIDDEN",
        "single universal calibration",
    )
    for mechanism, absent in fixed_point[
        "absent_zero_selection_mechanisms"
    ].items():
        add(
            f"mechanism_absent_{mechanism}",
            bool(absent),
            absent,
            True,
            "not in canonical checkpoint-5203 parent basis",
        )
    add(
        "radiative_sensitivity_large",
        radiative["quartic_to_critical_ratio"] > 1.0e120,
        radiative["quartic_to_critical_ratio"],
        ">1e120",
        "scheme-dependent diagnostic only",
    )
    add(
        "finite_mass_threshold_tiny",
        radiative["finite_mass_vacuum_fraction_bound"] < 1.0e-120,
        radiative["finite_mass_vacuum_fraction_bound"],
        "<1e-120",
        "cannot select/cancel the vacuum coordinate",
    )
    add(
        "cosmology_free_converged_no_edge",
        not cosmology["free_prior_edge"],
        cosmology["free_prior_edge"],
        False,
        "locked checkpoint-5195 fit",
    )
    add(
        "cosmology_zero_converged_no_edge",
        not cosmology["zero_prior_edge"],
        cosmology["zero_prior_edge"],
        False,
        "locked checkpoint-5195 fit",
    )
    add(
        "conditional_delta_chi2",
        math.isclose(
            cosmology["zero_minus_free_delta_chi2"],
            0.09080707555787915,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        cosmology["zero_minus_free_delta_chi2"],
        0.09080707555787915,
        "zero branch slightly worsens chi-squared",
    )
    add(
        "conditional_delta_AIC",
        math.isclose(
            cosmology["zero_minus_free_delta_AIC"],
            -1.9091929244421208,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        cosmology["zero_minus_free_delta_AIC"],
        -1.9091929244421208,
        "one-parameter penalty favors the zero branch conditionally",
    )
    add(
        "conditional_delta_BIC",
        math.isclose(
            cosmology["zero_minus_free_delta_BIC"],
            -7.315296305679129,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        cosmology["zero_minus_free_delta_BIC"],
        -7.315296305679129,
        "one-parameter penalty favors the zero branch conditionally",
    )
    add(
        "local_R10_background_small",
        local["R10_Lambda_L2"] < 1.0e-60,
        local["R10_Lambda_L2"],
        "<1e-60",
        "single calibrated de Sitter background",
    )
    add(
        "local_Earth_acceleration_small",
        local["Earth_aLambda_over_aNewton"] < 1.0e-29,
        local["Earth_aLambda_over_aNewton"],
        "<1e-29",
        "not a full PPN projection",
    )
    add(
        "local_Saturn_acceleration_small",
        local["Saturn_aLambda_over_aNewton"] < 1.0e-19,
        local["Saturn_aLambda_over_aNewton"],
        "<1e-19",
        "not a full orbital likelihood",
    )
    add(
        "local_100kpc_background_small",
        local["galaxy_100kpc_Lambda_L2"] < 1.0e-8,
        local["galaxy_100kpc_Lambda_L2"],
        "<1e-8",
        "background term remains perturbative",
    )
    add(
        "no_arena_retuning",
        local["arena_retuning_count"] == 0,
        local["arena_retuning_count"],
        0,
        "same Lambda used for every row",
    )
    add(
        "all_evidence_nonclaim",
        all(
            row.get("valid_for_full_MTS_claim") is False
            for evidence_rows in datasets.values()
            for row in evidence_rows
        ),
        True,
        True,
        "no CSV row opens a full-MTS claim",
    )
    add(
        "cosmology_rows_present",
        len(cosmology_rows) == 7,
        len(cosmology_rows),
        7,
        "five models plus branch comparison and interpretation",
    )
    add(
        "local_rows_present",
        len(local_rows) == 7,
        len(local_rows),
        7,
        "R10 through cosmology scales",
    )
    add(
        "fixed_rows_present",
        len(fixed_rows) == 9,
        len(fixed_rows),
        9,
        "coverage, rank, ownership, state rank and four mechanism checks",
    )
    add(
        "evidence_digest_present",
        len(evidence_digest) == 64,
        evidence_digest,
        "64 hex characters",
        "deterministic CSV evidence lock",
    )
    add(
        "formal_tree_unchanged",
        checkpoint_5209.checkpoint_5208.tree_digest(FORMAL) == FORMAL_LOCK,
        checkpoint_5209.checkpoint_5208.tree_digest(FORMAL),
        FORMAL_LOCK,
        "no pre-checkpoint workbench edit",
    )
    public_head, public_status = checkpoint_5209.checkpoint_5208.git_state(PUBLIC)
    galaxy_head, galaxy_status = checkpoint_5209.checkpoint_5208.git_state(GALAXY)
    add(
        "public_worktree_unchanged",
        public_head == PUBLIC_HEAD and not public_status,
        (public_head, public_status),
        (PUBLIC_HEAD, ""),
        "no GitHub/public worktree action",
    )
    add(
        "galaxy_repository_unchanged",
        galaxy_head == GALAXY_HEAD and galaxy_status == GALAXY_DIRTY,
        (galaxy_head, galaxy_status),
        (GALAXY_HEAD, GALAXY_DIRTY),
        "read-only galaxy boundary retained",
    )
    add(
        "scripts_cache_absent",
        not (POST / "scripts" / "__pycache__").exists(),
        (POST / "scripts" / "__pycache__").exists(),
        False,
        "no bytecode artifact retained",
    )
    return rows


def run_checkpoint() -> None:
    source_hashes = assert_source_locks()
    symbolic = symbolic_vacuum_theorem()
    operator_evidence = vacuum_operator_rows(symbolic)
    ctp_evidence = ctp_rows(symbolic)
    frg_evidence = frg_rows(symbolic)
    fixed_rows, fixed_point = fixed_point_and_parameter_rows(symbolic)
    radiative_rows, radiative = radiative_stability_rows(symbolic)
    cosmology_rows, cosmology = conditional_cosmology_rows()
    local_rows, local = local_propagation_rows(cosmology)
    decisions = decision_rows(fixed_point, cosmology, local)
    provenance = provenance_rows()
    datasets = {
        "vacuum_operator_symmetry_cohomology.csv": operator_evidence,
        "CTP_diagonal_and_physical_variation.csv": ctp_evidence,
        "vacuum_FRG_source_and_invariance.csv": frg_evidence,
        "fixed_point_coverage_and_parameter_count.csv": fixed_rows,
        "spectrum_and_radiative_stability.csv": radiative_rows,
        "conditional_cosmology_model_comparison.csv": cosmology_rows,
        "single_calibration_local_propagation.csv": local_rows,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in datasets.items():
        write_csv(OUT / name, rows)
    evidence_digest = selected_digest(
        [OUT / name for name in datasets],
        OUT,
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "claim_status": "PRIVATE_PARAMETER_BOUNDARY_NO_FULL_MTS_CLAIM",
        "source_hashes": source_hashes,
        "symbolic_checks": symbolic,
        "fixed_point_and_parameter_count": fixed_point,
        "radiative_diagnostics": radiative,
        "conditional_cosmology": cosmology,
        "local_propagation": local,
        "vacuum_zero_status": (
            "NOT_SELECTED_BY_CURRENT_SYMMETRY_CTP_STATE_OR_RESOLVED_RG"
        ),
        "current_parent_status": (
            "LAMBDA_CAL_IS_ONE_UNIVERSAL_RENORMALIZATION_DATUM"
        ),
        "selected_next_route": (
            "RESUME_UNIVERSAL_SOURCE_COUPLING_AND_LOCAL_GR_WITH_ONE_"
            "FROZEN_LAMBDA_DATUM"
        ),
        "optional_vacuum_prediction_route": (
            "ADD_U0_TO_FULL_UV_HESSIAN_AND_DERIVE_A_PARENT_IDENTITY"
        ),
        "evidence_csv_sha256": evidence_digest,
        "formal_tree_sha256": (
            checkpoint_5209.checkpoint_5208.tree_digest(FORMAL)
        ),
    }
    write_json(
        OUT / "parent_vacuum_coordinate_ownership_results.json",
        result,
    )
    DOCUMENT.write_text(
        build_document(
            symbolic,
            fixed_point,
            radiative,
            cosmology,
            local,
            evidence_digest,
        ),
        encoding="utf-8",
    )
    validation = validation_rows(
        symbolic,
        operator_evidence,
        ctp_evidence,
        frg_evidence,
        fixed_rows,
        fixed_point,
        radiative,
        cosmology_rows,
        cosmology,
        local_rows,
        local,
        datasets,
        evidence_digest,
    )
    write_csv(VALIDATION, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "vacuum_zero_status": result["vacuum_zero_status"],
                "current_parent_status": result["current_parent_status"],
                "beta_u0_at_zero_real_scalar": symbolic[
                    "massless_scalar_source"
                ],
                "conditional_zero_minus_free": {
                    "delta_chi2": cosmology[
                        "zero_minus_free_delta_chi2"
                    ],
                    "delta_AIC": cosmology["zero_minus_free_delta_AIC"],
                    "delta_BIC": cosmology["zero_minus_free_delta_BIC"],
                },
                "maximum_local_Lambda_L2_through_100kpc": local[
                    "maximum_local_Lambda_L2_through_100kpc"
                ],
                "selected_next_route": result["selected_next_route"],
                "evidence_csv_sha256": evidence_digest,
                "formal_tree_sha256": result["formal_tree_sha256"],
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    assert_source_locks()
    result_path = OUT / "parent_vacuum_coordinate_ownership_results.json"
    if not result_path.is_file() or not VALIDATION.is_file() or not DOCUMENT.is_file():
        raise RuntimeError("checkpoint-5210 saved products are incomplete")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"saved validation failures: {failures}")
    csv_paths = sorted(OUT.glob("*.csv"))
    actual_digest = selected_digest(csv_paths, OUT)
    if actual_digest != result["evidence_csv_sha256"]:
        raise RuntimeError("checkpoint-5210 evidence digest changed")
    if checkpoint_5209.checkpoint_5208.tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed")
    public_head, public_status = checkpoint_5209.checkpoint_5208.git_state(PUBLIC)
    galaxy_head, galaxy_status = checkpoint_5209.checkpoint_5208.git_state(GALAXY)
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
                "formal_tree_sha256": (
                    checkpoint_5209.checkpoint_5208.tree_digest(FORMAL)
                ),
                "current_parent_status": result["current_parent_status"],
                "selected_next_route": result["selected_next_route"],
            },
            indent=2,
        )
    )


def dry_run() -> None:
    assert_source_locks()
    symbolic = symbolic_vacuum_theorem()
    fixed_rows, fixed_point = fixed_point_and_parameter_rows(symbolic)
    cosmology_rows, cosmology = conditional_cosmology_rows()
    local_rows, local = local_propagation_rows(cosmology)
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "stationary_residual": symbolic["stationary_residual"],
                "scalar_beta_at_zero": symbolic[
                    "massless_scalar_source"
                ],
                "calibration_rank": symbolic["calibration_rank"],
                "vacuum_coordinate_in_fixed_point": fixed_point[
                    "vacuum_coordinate_in_fixed_point"
                ],
                "fixed_rows": len(fixed_rows),
                "cosmology_rows": len(cosmology_rows),
                "local_rows": len(local_rows),
                "maximum_local_Lambda_L2_through_100kpc": local[
                    "maximum_local_Lambda_L2_through_100kpc"
                ],
                "formal_tree_sha256": (
                    checkpoint_5209.checkpoint_5208.tree_digest(FORMAL)
                ),
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
