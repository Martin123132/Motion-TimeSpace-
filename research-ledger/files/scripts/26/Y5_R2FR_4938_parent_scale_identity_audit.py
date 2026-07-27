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
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4938"
OUTPUT = SOURCE_DIR / "parent_scale_identity_audit_results.json"
CANDIDATE_OUTPUT = SOURCE_DIR / "scale_identity_candidate_audit.csv"
BOUND_OUTPUT = SOURCE_DIR / "motion_scale_bound_translation.csv"

GEOMETRIC_FRAMEWORK = ROOT / "core-mts-framework" / "field-theory" / "geometric-field-framework.md"
FUNDAMENTAL_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
MASS_GAP_4909 = POST / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md"
SCALE_REPAIR_4926 = POST / "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md"
NORMALIZATION_4927 = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
CHECKPOINT_4937 = POST / "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md"
SCALE_ROWS_4926 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv"
FIXED_GATE_4937 = POST / "source-intake" / "functional_rg" / "4937" / "functional_potential_fixed_gate_results.json"

MARKER = "MTS_4938_PARENT_SCALE_IDENTITY_AUDIT"
EXPECTED_HASHES = {
    GEOMETRIC_FRAMEWORK: "b5a6d5ab7c3cca6484897f26e7dedba35ca67a00962c460d46bb6834ee41d3b9",
    FUNDAMENTAL_ACTION: "afbb6a6e86ee30ca790f829374b791b307ace0e20f175b1600632205f9aeff54",
    MASS_GAP_4909: "9d5d420a8c2cac6fc3d65352e2dec7c44f635b083a6840c18267a105a02a7ca3",
    SCALE_REPAIR_4926: "bbdd4a5b4928e1339730f05a10b9b6ea98ace83d30d78356b3c7294df14ea562",
    NORMALIZATION_4927: "512c200c0d5dfb32884404c0536678a6116ba4fa0d5103187012393746770926",
    CHECKPOINT_4937: "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5",
    SCALE_ROWS_4926: "d27b69621f81e5590ebba74103b6cd5b7e19c0ca28476f0df0aae5aa7d50e533",
    FIXED_GATE_4937: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
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
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path) if path.exists() else "MISSING"}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"parent scale identity source hash mismatch: {hash_failures}")

    scale_factor = sp.symbols("s", positive=True)
    normalization_mass, old_coupling, old_covariance = sp.symbols(
        "M_N lambda_old B_old", positive=True
    )
    newton_constant = sp.symbols("G_N", positive=True)
    harmonic = (1 + sp.sqrt(5)) / 2
    planck_mass = newton_constant ** sp.Rational(-1, 2)

    transformed_normalization = scale_factor**2 * normalization_mass
    transformed_coupling = scale_factor ** sp.Rational(2, 3) * old_coupling
    transformed_covariance = old_covariance / scale_factor**2
    canonical_coupling = old_coupling * normalization_mass ** sp.Rational(-1, 3)
    transformed_canonical_coupling = sp.simplify(
        transformed_coupling * transformed_normalization ** sp.Rational(-1, 3)
    )
    canonical_covariance = old_covariance * normalization_mass
    transformed_canonical_covariance = sp.simplify(
        transformed_covariance * transformed_normalization
    )
    scale_invariant = sp.simplify(
        canonical_coupling * newton_constant ** sp.Rational(4, 3)
    )
    transformed_scale_invariant = sp.simplify(
        transformed_canonical_coupling
        * newton_constant ** sp.Rational(4, 3)
    )

    fixed_harmonic_old_coupling = harmonic**4 * planck_mass**3
    transformed_relation_ratio = sp.simplify(
        transformed_coupling.subs(old_coupling, fixed_harmonic_old_coupling)
        / fixed_harmonic_old_coupling
    )
    normalization_power = sp.symbols("p", real=True)
    normalization_family = harmonic**normalization_power * planck_mass
    invariant_family = sp.simplify(
        fixed_harmonic_old_coupling
        * normalization_family ** sp.Rational(-1, 3)
        * newton_constant ** sp.Rational(4, 3)
    )

    field, field_dot, gamma = sp.symbols("phi phi_dot gamma", real=True)
    damping_density = gamma * field * field_dot
    damping_boundary = gamma * field**2 / 2
    damping_is_boundary = sp.diff(damping_boundary, field) * field_dot == damping_density

    scale_rows = read_csv(SCALE_ROWS_4926)

    def unique_row(branch: str) -> dict[str, str]:
        matches = [row for row in scale_rows if row["branch"] == branch]
        if len(matches) != 1:
            raise RuntimeError(f"expected one 4926 scale row {branch}, found {len(matches)}")
        return matches[0]

    compact_floor = unique_row("generic_canonical_coupling_floor")
    central_mass = unique_row("C_N_1_central_c_m")
    low_mass = unique_row("C_N_1_conservative_low_c_m")
    high_mass = unique_row("C_N_1_conservative_high_c_m")
    invariant_floor = float(compact_floor["C_psi_min_for_NS_one_percent"])
    mass_profiles = {
        "conservative_low": float(low_mass["c_m"]),
        "pilot_central": float(central_mass["c_m"]),
        "conservative_high": float(high_mass["c_m"]),
    }
    bound_rows: list[dict[str, Any]] = []
    for profile, c_mass in mass_profiles.items():
        j_floor = c_mass**2 * invariant_floor ** (3.0 / 4.0)
        bound_rows.append(
            {
                "profile": profile,
                "c_m": c_mass,
                "I_M_floor": invariant_floor,
                "J_gap_floor": j_floor,
                "log10_J_gap_floor": math.log10(j_floor),
                "m_gap_over_M_Pl_floor": math.sqrt(j_floor),
                "bound_origin": "4926 one-real-pole neutron-star one-percent Weyl-cubic threshold envelope",
                "upper_bound": "NOT_DERIVED",
                "status": "CONDITIONAL_COMPACT_SAFETY_FLOOR_NONCLAIM",
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    candidate_rows = [
        {
            "candidate": "fixed_golden_ratio_and_old_lambda_formula",
            "proposed_owner": "Phi_G^2=Phi_G+1 and lambda_old=Phi_G^4 M_Pl^3",
            "test": "preserve the exact old-field coordinate orbit",
            "result": "REJECT_AS_PHYSICAL_SCALE_IDENTITY",
            "reason": "with fixed Phi_G the formula is changed by s^(2/3) under an allowed old-field rescaling, so it selects a coordinate rather than an observable",
        },
        {
            "candidate": "M_N_equals_M_Pl",
            "proposed_owner": "minimal single-scale normalization",
            "test": "derive the old-field normalization from a variational or residue condition",
            "result": "CONDITIONAL_COORDINATE_CHOICE",
            "reason": "4927 proves M_N lies on a redundant field-coordinate orbit and the Einstein residue cannot select it",
        },
        {
            "candidate": "M_N_equals_gamma_equals_Phi_G_M_Pl",
            "proposed_owner": "use the old damping coefficient as the missing action normalization",
            "test": "the gamma term must be a non-boundary physical residue",
            "result": "REJECT",
            "reason": "for constant gamma, gamma phi partial_t phi is exactly one-half gamma partial_t(phi^2), so it cannot normalize an observable pole",
        },
        {
            "candidate": "old_covariance_metric_coefficient",
            "proposed_owner": "g_mn=eta_mn+B_old<partial phi_old partial phi_old>",
            "test": "the public metric and coefficient must fix the old field residue",
            "result": "REJECT_IN_CURRENT_PARENT",
            "reason": "the dimensionally repaired invariant is B_psi=B_old M_N; B_old transforms inversely and the scalar-only public metric branch was rejected",
        },
        {
            "candidate": "Einstein_Hilbert_stress_residue",
            "proposed_owner": "match closed scalar stress correlators to measured Newton residue",
            "test": "closed stress amplitudes must depend on M_N",
            "result": "EXACT_ZERO_SENSITIVITY",
            "reason": "each old stress vertex contributes M_N^-1 and each propagator M_N, so every closed loop is invariant",
        },
        {
            "candidate": "minimal_functional_UV_critical_surface",
            "proposed_owner": "gravity-motion fixed point removes the independent mass datum",
            "test": "the MES-connected enlarged stability matrix has only one relevant direction",
            "result": "REJECT_IN_DECLARED_MINIMAL_BLOCK",
            "reason": "4937 derives a separate relevant regular motion mass direction with theta about 1.85",
        },
        {
            "candidate": "explicit_two_scale_parent",
            "proposed_owner": "take G_N and J_gap=m_gap^2 G_N as independent essential data",
            "test": "coordinates are invariant and every local limit carries the same fixed value without retuning",
            "result": "SELECTED_CURRENT_PARENT_STATUS",
            "reason": "this is the only route consistent with the field-coordinate theorem and the calculated critical index without adding an unsigned identity",
        },
    ]
    for row in candidate_rows:
        row["valid_for_full_MTS_claim"] = False
        row["checkpoint_marker"] = MARKER

    fixed_gate = json.loads(FIXED_GATE_4937.read_text(encoding="utf-8"))
    normalization_text = NORMALIZATION_4927.read_text(encoding="utf-8-sig")
    checks = {
        "harmonic_is_positive_golden_root": sp.simplify(harmonic**2 - harmonic - 1) == 0
        and harmonic > 0,
        "canonical_coupling_invariant_under_old_field_orbit": sp.simplify(
            transformed_canonical_coupling - canonical_coupling
        )
        == 0,
        "canonical_covariance_invariant_under_old_field_orbit": sp.simplify(
            transformed_canonical_covariance - canonical_covariance
        )
        == 0,
        "Newton_motion_I_invariant_under_old_field_orbit": sp.simplify(
            transformed_scale_invariant - scale_invariant
        )
        == 0,
        "fixed_harmonic_lambda_relation_breaks_orbit": transformed_relation_ratio
        == scale_factor ** sp.Rational(2, 3),
        "normalization_family_leaves_free_power": sp.simplify(
            invariant_family - harmonic ** (4 - normalization_power / 3)
        )
        == 0,
        "gamma_term_is_exact_boundary": damping_is_boundary,
        "4927_declares_CN_redundant": "C_N=M_N/M_Pl` is not a physical parameter" in normalization_text,
        "4927_leaves_invariant_gap_unpredicted": "physical invariant motion gap        = still unpredicted" in normalization_text,
        "4937_one_scale_branch_false": fixed_gate["predictivity_decision"][
            "unchanged_parent_one_scale_fixed_function"
        ]
        is False,
        "compact_floor_is_positive": invariant_floor > 0.0,
        "all_translated_J_floors_positive": all(
            row["J_gap_floor"] > 0.0 for row in bound_rows
        ),
        "exactly_one_current_route_selected": sum(
            row["result"] == "SELECTED_CURRENT_PARENT_STATUS"
            for row in candidate_rows
        )
        == 1,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise RuntimeError(f"parent scale identity checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "old_field_coordinate_theorem": {
            "orbit": "phi_old'=s phi_old; M_N'=s^2 M_N; lambda_old'=s^(2/3)lambda_old; B_old'=s^(-2)B_old",
            "invariants": [
                "g_psi=lambda_old M_N^(-1/3)",
                "B_psi=B_old M_N",
                "I_M=g_psi G_N^(4/3)",
            ],
            "fixed_harmonic_relation_ratio_under_orbit": str(
                transformed_relation_ratio
            ),
            "theorem": "a proposed scale identity must be constant on this orbit; the printed fixed-Phi_G old-coordinate lambda formula is not",
        },
        "harmonic_formula_audit": {
            "Phi_G": str(harmonic),
            "numeric_Phi_G": float(harmonic),
            "old_formula": "gamma=Phi_G M_Pl; lambda_old=Phi_G^4 M_Pl^3",
            "normalization_family": "M_N=Phi_G^p M_Pl",
            "implied_physical_invariant": "I_M(p)=Phi_G^(4-p/3)",
            "examples": {
                "p=0_M_N_equals_M_Pl": float(invariant_family.subs(normalization_power, 0)),
                "p=1_M_N_equals_gamma": float(invariant_family.subs(normalization_power, 1)),
            },
            "decision": "Phi_G fixes a dimensionless number but does not fix the missing field normalization power p",
        },
        "physical_two_scale_coordinates": {
            "gravity_scale": "G_N or M_Pl=G_N^(-1/2)",
            "motion_scale": "m_gap",
            "dimensionless_ratio": "J_gap=m_gap^2 G_N",
            "fractional_coordinate_relation": "J_gap=c_m^2 I_M^(3/4)",
            "I_M": "g_psi G_N^(4/3)",
            "status": "EXPLICIT_SECOND_ESSENTIAL_SCALE_IN_UNCHANGED_PARENT",
        },
        "compact_bound_translation": {
            "I_M_lower_bound_one_real_pole": invariant_floor,
            "I_M_upper_bound": None,
            "profiles": bound_rows,
            "boundary": "the lower bound is a conditional local compact-safety envelope inherited from 4926 and the unpromoted c_m profile; it is not a scale measurement",
        },
        "candidate_decision": {
            "selected": "explicit_two_scale_parent",
            "parent_identity_derived": False,
            "current_parent_identity_rejected_after_owner_audit": True,
            "reason": "every current owner is coordinate-dependent, a boundary term, residue-silent, or contradicted by the two-relevant-direction functional spectrum",
        },
        "checks": checks,
        "claim_boundary": {
            "field_coordinate_invariant_scale_ratio_derived": True,
            "golden_ratio_fixes_physical_motion_scale": False,
            "gamma_fixes_physical_motion_scale": False,
            "Einstein_residue_fixes_motion_scale": False,
            "minimal_UV_surface_fixes_motion_scale": False,
            "explicit_second_essential_scale_required": True,
            "numeric_motion_scale_measured": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(CANDIDATE_OUTPUT, candidate_rows)
    write_csv(BOUND_OUTPUT, bound_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_CANDIDATES_SHA256={digest(CANDIDATE_OUTPUT)}", flush=True)
    print(f"{MARKER}_BOUNDS_SHA256={digest(BOUND_OUTPUT)}", flush=True)
    print(f"{MARKER}_I_FLOOR={invariant_floor:.12e}", flush=True)
    print(f"{MARKER}_DECISION=EXPLICIT_TWO_SCALE", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
