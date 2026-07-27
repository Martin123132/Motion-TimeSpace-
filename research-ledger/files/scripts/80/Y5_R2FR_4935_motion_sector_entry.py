from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4935"
OUTPUT = OUTPUT_DIR / "motion_sector_entry_results.json"
TABLE_OUTPUT = OUTPUT_DIR / "motion_sector_entry_operator_table.csv"

PARENT_ACTION = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
NORMALIZATION = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
MASS_GAP = POST / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md"
SIX_DERIVATIVE = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
BASIS = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
TRAJECTORY = OUTPUT_DIR / "completed_fixed_point_trajectory_results.json"

MARKER = "MTS_4935_MOTION_SECTOR_ENTRY"
EXPECTED_HASHES = {
    PARENT_ACTION: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    NORMALIZATION: "512c200c0d5dfb32884404c0536678a6116ba4fa0d5103187012393746770926",
    MASS_GAP: "9d5d420a8c2cac6fc3d65352e2dec7c44f635b083a6840c18267a105a02a7ca3",
    SIX_DERIVATIVE: "1b987f0040d4288d9057b52f2f792c6484b6a0a8edd0bf817d71f7abf6a03755",
    BASIS: "93d8485ad79cc72ce2e9f6be3d81dc3605c785cb45436431d64041415e951361",
    TRAJECTORY: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("refusing to write an empty motion-entry table")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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
        raise RuntimeError(f"motion-entry source hash mismatch: {hash_failures}")

    psi = sp.symbols("psi", positive=True)
    g_psi = sp.symbols("g_psi", positive=True)
    c_mass = sp.symbols("c_m", positive=True)
    k_scale = sp.symbols("k", positive=True)
    eta_psi = sp.symbols("eta_psi", real=True)
    potential = sp.Rational(3, 4) * g_psi * psi ** sp.Rational(4, 3)
    first_derivative = sp.simplify(sp.diff(potential, psi))
    second_derivative = sp.simplify(sp.diff(potential, psi, 2))
    vacuum_hessian_limit = sp.limit(second_derivative, psi, 0, dir="+")

    dimension_g_psi = sp.Rational(8, 3)
    dimension_mu = sp.simplify(sp.Rational(3, 8) * dimension_g_psi)
    dimension_mass_squared = 2 * dimension_mu
    g_tilde = sp.symbols("g_tilde", positive=True)
    w_mass = c_mass**2 * g_tilde ** sp.Rational(3, 4)
    beta_g_tilde_canonical = -dimension_g_psi * g_tilde
    beta_w_canonical = sp.simplify(
        sp.diff(w_mass, g_tilde) * beta_g_tilde_canonical
    )

    threshold_w = sp.symbols("w", nonnegative=True)
    decoupling_factor = 1 / (1 + threshold_w)
    c6_scalar = 1 / (sp.Integer(30240) * (4 * sp.pi) ** 2)
    delta_beta_g = sp.symbols("g_N", real=True) ** 2 * decoupling_factor / (6 * sp.pi)
    delta_beta_h = eta_psi * c6_scalar * decoupling_factor

    basis_rows = read_csv(BASIS)
    o4_rows = [row for row in basis_rows if row["operator_id"] == "S6_O4"]
    active_motion_rows = [
        row
        for row in basis_rows
        if row["scalar_field_degree"] != "0"
        and row["quadratic_Hessian_nonzero_at_nabla_phi_zero"].lower() == "true"
    ]
    if len(o4_rows) != 1 or [row["operator_id"] for row in active_motion_rows] != ["S6_O4"]:
        raise RuntimeError("the source-locked motion Hessian selection did not isolate O4")

    operator_rows = [
        {
            "entry_id": "ME4935_00_parent_kinetic",
            "operator": "-1/2 integral H^{mu nu} partial_mu psi partial_nu psi",
            "quadratic_Hessian": "Z_psi(-Box_g)+V_eff''(psi_0)",
            "canonical_dimensionless_coordinate": "Z_psi and w_psi=m_gap^2/k^2",
            "Gaussian_beta_eigenvalue": "-2 for w_psi",
            "critical_exponent": "+2",
            "entry_status": "RENORMALIZED_1PI_HESSIAN_REQUIRED",
            "reason": "the literal bare vacuum Hessian diverges at psi=0",
        },
        {
            "entry_id": "ME4935_01_fractional_potential",
            "operator": "(3/4) g_psi |psi|^(4/3)",
            "quadratic_Hessian": "g_psi/(3 |psi|^(2/3)) for psi!=0; +infinity at psi=0",
            "canonical_dimensionless_coordinate": "g_tilde_psi=k^(-8/3)g_psi",
            "Gaussian_beta_eigenvalue": "-8/3",
            "critical_exponent": "+8/3",
            "entry_status": "SECOND_RELEVANT_SCALE_UNLESS_PARENT_FLOW_FIXES_IT",
            "reason": "g_psi is invariant after canonical field normalization and sets mu=g_psi^(3/8)",
        },
        {
            "entry_id": "ME4935_02_minimal_scalar_trace",
            "operator": "Tr[(partial_t R_k)/(Delta_psi+R_k+m_gap^2)]",
            "quadratic_Hessian": "Z_psi(-Box_g+m_gap^2)",
            "canonical_dimensionless_coordinate": "w_psi=m_gap^2/k^2",
            "Gaussian_beta_eigenvalue": "threshold dependent",
            "critical_exponent": "not an additional coordinate beyond w_psi",
            "entry_status": "EXACT_OPTIMIZED_THRESHOLD_DERIVED",
            "reason": "D_psi=1/(1+w_psi), Delta beta_g=g_N^2 D_psi/(6pi), Delta beta_h=eta_psi c6 D_psi",
        },
        {
            "entry_id": "ME4935_03_O4_portal",
            "operator": "u_O4 integral sqrt(g) C^2 (nabla psi)^2",
            "quadratic_Hessian": "-2u_O4 nabla_mu[C^2 nabla^mu] in the displayed action normalization",
            "canonical_dimensionless_coordinate": "u4_tilde=k^4 u_O4",
            "Gaussian_beta_eigenvalue": "+4 before additive gravity terms",
            "critical_exponent": "-4 before mixing",
            "entry_status": "UNIQUE_SIX_DERIVATIVE_MOTION_HESSIAN_PORTAL",
            "reason": "the source quotient proves O1 O2 O5 have zero quadratic Hessian at constant motion background while O4 does not",
        },
    ]
    for row in operator_rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False

    trajectory = json.loads(TRAJECTORY.read_text(encoding="utf-8"))
    trajectory_claim = trajectory["claim_boundary"]
    checks = {
        "all_source_hashes_match": not hash_failures,
        "potential_first_derivative": first_derivative == g_psi * psi ** sp.Rational(1, 3),
        "potential_second_derivative": second_derivative
        == g_psi / (3 * psi ** sp.Rational(2, 3)),
        "only_classical_stationary_point_is_zero": sp.limit(
            first_derivative, psi, 0, dir="+"
        )
        == 0,
        "bare_vacuum_Hessian_diverges": vacuum_hessian_limit == sp.oo,
        "gpsi_mass_dimension_is_8_over_3": dimension_g_psi == sp.Rational(8, 3),
        "mu_mass_dimension_is_one": dimension_mu == 1,
        "mass_squared_dimension_is_two": dimension_mass_squared == 2,
        "canonical_gpsi_beta_is_minus_8_over_3": beta_g_tilde_canonical
        == -sp.Rational(8, 3) * g_tilde,
        "canonical_mass_beta_is_minus_two": beta_w_canonical == -2 * w_mass,
        "optimized_threshold_has_correct_limits": decoupling_factor.subs(threshold_w, 0)
        == 1
        and sp.limit(decoupling_factor, threshold_w, sp.oo) == 0,
        "unique_quadratic_motion_portal_is_O4": len(active_motion_rows) == 1,
        "minimal_trajectory_precedes_motion_entry": trajectory_claim[
            "GR_connected_minimal_trajectory_derived"
        ]
        and not trajectory_claim["motion_sector_included"],
    }
    if not all(checks.values()):
        raise RuntimeError(f"motion-sector entry checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "parent_motion_action": {
            "kinetic": "-1/2 integral H^{mu nu} partial_mu psi partial_nu psi",
            "potential": "V(psi)=(3/4)g_psi|psi|^(4/3)",
            "field_coordinate_status": "psi is canonically normalized; old M_N is redundant; g_psi is invariant",
            "potential_first_derivative": str(first_derivative),
            "potential_second_derivative_away_from_zero": str(second_derivative),
            "vacuum": "psi_0=0 is the only classical stationary point",
            "bare_vacuum_Hessian_limit": str(vacuum_hessian_limit),
            "conclusion": "the bare fractional potential has no finite ordinary Hessian at its vacuum and cannot be inserted as a standard finite-mass scalar propagator",
        },
        "renormalized_entry": {
            "required_1PI_two_point": "Gamma_psi,k^(2)=Z_psi,k[-Box_g+m_psi,k^2]+higher derivative and curvature terms",
            "mass_gap": "m_gap=c_m g_psi^(3/8)",
            "dimensionless_potential": "g_tilde_psi=k^(-8/3)g_psi",
            "dimensionless_mass": "w_psi=m_gap^2/k^2=c_m^2 g_tilde_psi^(3/4)",
            "canonical_beta_g_tilde": str(beta_g_tilde_canonical),
            "canonical_beta_w": str(beta_w_canonical),
            "canonical_critical_exponents": {
                "g_tilde_psi": 8.0 / 3.0,
                "w_psi": 2.0,
            },
            "predictivity_consequence": "unless gravity-motion interactions produce and select a non-Gaussian motion fixed point or a parent identity ties g_psi to G_N, motion adds a second physical relevant scale after the overall Newton scale",
        },
        "minimal_optimized_trace": {
            "decoupling_factor": str(decoupling_factor),
            "Delta_beta_g": str(delta_beta_g),
            "scalar_c6": str(c6_scalar),
            "Delta_beta_h": str(delta_beta_h),
            "eta_zero_result": "Delta beta_h=0 for the minimal scalar natural optimized trace at eta_psi=0",
            "UV_limit": "w_psi -> 0 gives one real massless scalar spectator",
            "IR_limit": "w_psi -> infinity decouples the motion loop as k^2/m_gap^2",
        },
        "six_derivative_entry": {
            "source_basis_size": len(basis_rows),
            "motion_rows_with_nonzero_quadratic_Hessian": [
                row["operator_id"] for row in active_motion_rows
            ],
            "unique_portal": "O4=C^2(nabla psi)^2",
            "O4_action_convention": "S_O4=u_O4 integral sqrt(g) C^2(nabla psi)^2",
            "O4_Hessian": "-2u_O4 nabla_mu[C^2 nabla^mu]",
            "required_next_beta_block": "{beta_gtilde_psi,beta_w_or_mass,beta_uO4,eta_psi} plus their affine contributions to the existing 20 selected rows",
        },
        "operator_rows": operator_rows,
        "checks": checks,
        "claim_boundary": {
            "motion_parent_Hessian_form_derived": True,
            "bare_zero_background_Hessian_usable": False,
            "renormalized_1PI_entry_required": True,
            "minimal_mass_threshold_derived": True,
            "motion_relevant_scale_identified": True,
            "motion_fixed_point_calculated": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(TABLE_OUTPUT, operator_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_TABLE_SHA256={digest(TABLE_OUTPUT)}", flush=True)
    print(f"{MARKER}_BARE_HESSIAN={vacuum_hessian_limit}", flush=True)
    print(f"{MARKER}_MOTION_CRITICAL_EXPONENT={8.0 / 3.0}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

