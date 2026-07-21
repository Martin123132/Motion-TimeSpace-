from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.parsing.mathematica import parse_mathematica


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4973"
SOURCE_4972 = POST / "source-intake" / "functional_rg" / "4972"
RESULT_4972 = SOURCE_4972 / "C3_EAA_to_amplitude_matching_results.json"
NONLOCAL_4972 = SOURCE_4972 / "C3_nonlocal_log_completion.csv"
SOURCE_2605_TAR = SOURCE / "arXiv-2605.29159-source.tar"
SOURCE_2605_TEX = SOURCE / "src-2605.29159" / "main_new.tex"
SOURCE_2210_TAR = SOURCE / "arXiv-2210.16072-source.tar"
SOURCE_2210_TEX = SOURCE / "src-2210.16072" / "formfactors.tex"
SOURCE_0911_TAR = SOURCE / "arXiv-0911.1168-source.tar"
SOURCE_0911_TEX = SOURCE / "src-0911.1168" / "cpt2009m.tex"
ABREU_MAIN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "src-2002.12374"
    / "source"
    / "main.tex"
)
ABREU_PPPP = ABREU_MAIN.parent / "anc" / "2loopRemainder" / "pppp_s-channel.m"
ABREU_MPPP = ABREU_MAIN.parent / "anc" / "2loopRemainder" / "mppp_s-channel.m"

CHARACTERISTICS_CSV = SOURCE / "C3_fixed_point_characteristics.csv"
NULL_DEFORMATION_CSV = SOURCE / "C3_kernel_null_deformation.csv"
ABREU_PROJECTION_CSV = SOURCE / "C3_Abreu_finite_remainder_projection.csv"
SOURCE_REQUIREMENTS_CSV = SOURCE / "C3_form_factor_source_requirements.csv"
RESULT_JSON = SOURCE / "C3_fixed_point_form_factor_kernel_results.json"

MARKER = "MTS_4973_C3_FIXED_POINT_FORM_FACTOR_KERNEL"
CHECKED_DATE = "2026-07-13"
SYMMETRIC_S = sp.Integer(1)
SYMMETRIC_T = -sp.Rational(1, 2)
SYMMETRIC_U = -sp.Rational(1, 2)
SYMMETRIC_STU = SYMMETRIC_S * SYMMETRIC_T * SYMMETRIC_U

EXPECTED_HASHES = {
    RESULT_4972: "e150ec2b9424804ea50ad8a0258086e41436c8653e6214262160e1e2c593d4a1",
    NONLOCAL_4972: "a044b3e12494b10ab24903f19ab5e40f412f06253fa4aefec020bc4faa2d9385",
    SOURCE_2605_TAR: "de812502809d1f4af4bf13e16617a3f05a030fb973cb696b5a97f16169625948",
    SOURCE_2605_TEX: "e3f783efb9df57d19c49e96215e1fbf27470b6053c45d133887ba7233a6c974a",
    SOURCE_2210_TAR: "38eec7cf76ea16101964d2abe27fdc4bd0e3ef15abe7db003985484d06403d5e",
    SOURCE_2210_TEX: "258210906af3de03e64bbeeb50d844b68533ee555ff05dfb7b953e0971d0ae10",
    SOURCE_0911_TAR: "0b6f1f693d56390b00bd19a583cc1edb695330ee128c1dbdbbc727ad554357a4",
    SOURCE_0911_TEX: "8cc7344187523211abd274cdbf8fbdc75b794662f5a062ddf1662f96195b7d8e",
    ABREU_MAIN: "11acdee89baad0298aafc5cc975be9d981d985bb37d2da86914281ca2c997fc8",
    ABREU_PPPP: "42128b16a7451b6213abd06c0eae9bfa649f5890df365c04f6209fd6b5630483",
    ABREU_MPPP: "6d426fbba39e4a02413fd17f5d4869a33c3cabb4263d88dd8e9e8e8a7a52c2a5",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def exact_text(expression: sp.Expr) -> str:
    return str(sp.expand_log(sp.simplify(expression), force=True))


def complex_parts(expression: sp.Expr) -> tuple[float, float]:
    numeric = complex(sp.N(expression, 18))
    return float(numeric.real), float(numeric.imag)


def parse_abreu_remainder(path: Path) -> sp.Expr:
    source_text = path.read_text(encoding="utf-8")
    normalized = source_text.replace("cGB[mu]", "cgb").replace(
        "cR3[mu]", "cr3"
    )
    normalized = re.sub(r"\bS\b", "ss", normalized)
    normalized = re.sub(r"\bT\b", "tt", normalized)
    return parse_mathematica(normalized)


def source_scope_checks() -> dict[str, bool]:
    source_2605 = SOURCE_2605_TEX.read_text(encoding="utf-8")
    source_2210 = SOURCE_2210_TEX.read_text(encoding="utf-8")
    source_0911 = SOURCE_0911_TEX.read_text(encoding="utf-8")
    return {
        "2605_flow_equation_and_boundary_function_present": (
            "kF_k^{\\left(0,0,1\\right)}" in source_2605
            and "Imposing the boundary condition" in source_2605
        ),
        "2605_fluctuation_form_factor_limitation_explicit": (
            "Extending the analysis to fluctuation form factors"
            in source_2605
            and "At present, no general non-perturbative method exists"
            in source_2605
        ),
        "2605_three_four_vertex_kernel_structure_present": (
            "\\Gamma_k^{(3)}" in source_2605
            and "\\Gamma_k^{(4)}" in source_2605
        ),
        "2210_four_field_six_argument_requirement_present": (
            "four fields generically have six independent arguments"
            in source_2210
        ),
        "2210_graviton_scattering_quartic_requirement_present": (
            "two-to-two graviton scattering requires extending this result to quartic order"
            in source_2210
        ),
        "0911_generic_third_order_heat_kernel_present": (
            "The third-order form factors $F_{i}$, $i=1$ to $29$"
            in source_0911
        ),
    }


def characteristic_rows() -> tuple[list[dict[str, Any]], dict[str, bool]]:
    radial_ratio, angle_ratio, integration_variable = sp.symbols(
        "rho z v", positive=True
    )
    boundary_function = sp.Function("C")(angle_ratio)
    source_kernel = sp.Function("H")
    kernel_integral = sp.Integral(
        source_kernel(integration_variable, angle_ratio * integration_variable),
        (integration_variable, 0, radial_ratio),
    )
    fixed_point_solution = boundary_function / radial_ratio - kernel_integral / (
        2 * radial_ratio
    )
    characteristic_residual = sp.simplify(
        radial_ratio * sp.diff(fixed_point_solution, radial_ratio)
        + fixed_point_solution
        + source_kernel(radial_ratio, angle_ratio * radial_ratio) / 2
    )
    homogeneous_solution = boundary_function / radial_ratio
    homogeneous_residual = sp.simplify(
        radial_ratio * sp.diff(homogeneous_solution, radial_ratio)
        + homogeneous_solution
    )
    momentum_squared, rg_scale_squared = sp.symbols(
        "Q2 k2", positive=True
    )
    dimensionful_homogeneous = sp.simplify(
        (boundary_function / radial_ratio / rg_scale_squared).subs(
            radial_ratio, momentum_squared / rg_scale_squared
        )
    )
    constant_kernel = sp.symbols("H_0", finite=True)
    regular_particular = sp.simplify(
        -sp.integrate(
            constant_kernel,
            (integration_variable, 0, radial_ratio),
        )
        / (2 * radial_ratio)
    )
    rows = tagged(
        [
            {
                "derivation_id": "C3CHAR4973_00_DIMENSION",
                "object": "dimensionful Weyl-cubic form factor",
                "definition": "F_k(x,y)=k^2 f_C3,k(k^2 x,k^2 y); x=s/k^2; y=t/k^2; u=-s-t",
                "equation": "partial_lnk F=2F+2x F_x+2y F_y+H_C3,k",
                "result": "the extra +2F follows from mass dimension [f_C3]=-2",
                "status": "CANONICAL_SCALING_DERIVED",
            },
            {
                "derivation_id": "C3CHAR4973_01_FIXED_POINT",
                "object": "projected C3 fixed-point equation",
                "definition": "D=x partial_x+y partial_y",
                "equation": "(1+D)F_*(x,y)=-H_*(x,y)/2",
                "result": "first-order two-variable characteristic equation",
                "status": "SYMBOLICALLY_DERIVED",
            },
            {
                "derivation_id": "C3CHAR4973_02_CHARACTERISTIC",
                "object": "fixed-angle characteristic",
                "definition": "x=rho; y=z rho",
                "equation": "d[rho F_*(rho,z rho)]/d rho=-H_*(rho,z rho)/2",
                "result": "F_*=C(z)/rho-[1/(2rho)] integral_0^rho H_*(v,zv)dv",
                "status": "EXACT_CHARACTERISTIC_SOLUTION",
            },
            {
                "derivation_id": "C3CHAR4973_03_HOMOGENEOUS",
                "object": "C3 homogeneous fixed-point mode",
                "definition": "H_*=0",
                "equation": "F_hom=C(z)/rho",
                "result": "f_hom=C(t/s)/s; an inverse-momentum nonlocal mode",
                "status": "EXACT_HOMOGENEOUS_MODE",
            },
            {
                "derivation_id": "C3CHAR4973_04_QUASILOCAL",
                "object": "quasi-local UV boundary",
                "definition": "F_* finite and analytic as rho approaches zero at fixed z; H_* finite",
                "equation": "C(z)=0",
                "result": "the C3 fixed-point form factor is unique once the full H_*(x,y) is known",
                "status": "CONDITIONAL_UNIQUENESS_QUASILOCAL_BRANCH",
            },
            {
                "derivation_id": "C3CHAR4973_05_SOURCE_LIMIT",
                "object": "currently retained parent information",
                "definition": "zero-momentum local beta plus endpoint physical logarithm",
                "equation": "H_C3,k(0,0) and one asymptotic slope do not specify H_C3,k(x,y)",
                "result": "the characteristic equation is closed but its momentum-resolved source is not",
                "status": "FULL_KERNEL_ABSENT_NOT_SET_TO_ZERO",
            },
        ]
    )
    checks = {
        "C3_characteristic_solution_exact": characteristic_residual == 0,
        "C3_homogeneous_solution_exact": homogeneous_residual == 0,
        "C3_homogeneous_mode_is_inverse_momentum": sp.simplify(
            dimensionful_homogeneous - boundary_function / momentum_squared
        )
        == 0,
        "finite_kernel_gives_regular_particular_solution": sp.simplify(
            regular_particular + constant_kernel / 2
        )
        == 0,
    }
    return rows, checks


def null_deformation_rows() -> tuple[list[dict[str, Any]], dict[str, bool]]:
    momentum_ratio = sp.symbols("x", positive=True)
    deformation_amplitude = sp.symbols("a", real=True)
    null_kernel = deformation_amplitude * momentum_ratio / (
        1 + momentum_ratio
    ) ** 2
    ultraviolet_endpoint = sp.limit(null_kernel, momentum_ratio, 0, dir="+")
    infrared_endpoint = sp.limit(null_kernel, momentum_ratio, sp.oo)
    finite_shift = sp.simplify(
        sp.integrate(
            -null_kernel / (2 * momentum_ratio),
            (momentum_ratio, 0, sp.oo),
        )
    )
    rows: list[dict[str, Any]] = []
    for amplitude_value in (-2, -1, 0, 1, 2):
        shift_value = sp.simplify(
            finite_shift.subs(deformation_amplitude, amplitude_value)
        )
        rows.append(
            {
                "deformation_id": f"C3NULL4973_a{amplitude_value:+d}",
                "projected_kernel": "Delta K_a(x)=a*x/(1+x)^2",
                "a": amplitude_value,
                "x_definition": "x=Q^2/k^2; dlnk=-dx/(2x)",
                "Delta_K_at_x0": ultraviolet_endpoint,
                "Delta_K_at_xinf": infrared_endpoint,
                "local_beta_shift": 0,
                "asymptotic_log_slope_shift": 0,
                "finite_conversion_shift": shift_value,
                "helicity_embedding": "Delta K_h=P_h*Delta K_a preserves P_pppp/P_mppp=10",
                "status": "ENDPOINT_SILENT_FINITE_ANCHOR_SHIFT",
            }
        )
    checks = {
        "null_kernel_vanishes_at_local_endpoint": ultraviolet_endpoint == 0,
        "null_kernel_vanishes_at_log_endpoint": infrared_endpoint == 0,
        "null_kernel_finite_shift_is_minus_a_over_two": sp.simplify(
            finite_shift + deformation_amplitude / 2
        )
        == 0,
        "null_kernel_can_shift_anchor_both_signs": (
            finite_shift.subs(deformation_amplitude, -1) > 0
            and finite_shift.subs(deformation_amplitude, 1) < 0
        ),
    }
    return tagged(rows), checks


def abreu_projection_rows() -> tuple[list[dict[str, Any]], dict[str, bool], dict[str, Any]]:
    mandelstam_s, mandelstam_t, c_gb, c_r3 = sp.symbols(
        "ss tt cgb cr3"
    )
    substitutions = {
        mandelstam_s: SYMMETRIC_S,
        mandelstam_t: SYMMETRIC_T,
        c_gb: 0,
        c_r3: 0,
    }
    all_plus = parse_abreu_remainder(ABREU_PPPP)
    single_minus = parse_abreu_remainder(ABREU_MPPP)
    projected: dict[str, dict[str, sp.Expr]] = {}
    rows: list[dict[str, Any]] = []
    for helicity, expression in (("++++", all_plus), ("-+++", single_minus)):
        loop_only = sp.simplify(expression.subs(substitutions))
        c3_projector = sp.simplify(
            sp.diff(expression, c_r3).subs(
                {
                    mandelstam_s: SYMMETRIC_S,
                    mandelstam_t: SYMMETRIC_T,
                }
            )
        )
        apparent_shift = sp.simplify(loop_only / c3_projector)
        loop_real, loop_imaginary = complex_parts(loop_only)
        shift_real, shift_imaginary = complex_parts(apparent_shift)
        projected[helicity] = {
            "loop_only": loop_only,
            "projector": c3_projector,
            "apparent_shift": apparent_shift,
        }
        rows.append(
            {
                "projection_id": f"ABREU4973_{helicity}",
                "helicity": helicity,
                "s": SYMMETRIC_S,
                "t": SYMMETRIC_T,
                "u": SYMMETRIC_U,
                "stu": SYMMETRIC_STU,
                "C3_projector": exact_text(c3_projector),
                "Einstein_loop_remainder_exact": exact_text(loop_only),
                "Einstein_loop_remainder_real": loop_real,
                "Einstein_loop_remainder_imag": loop_imaginary,
                "apparent_delta_c_exact": exact_text(apparent_shift),
                "apparent_delta_c_real": shift_real,
                "apparent_delta_c_imag": shift_imaginary,
                "status": "DIRECT_FINITE_REMAINDER_PROJECTED_NOT_A_UNIVERSAL_C3_SHIFT",
            }
        )
    apparent_difference = sp.simplify(
        projected["++++"]["apparent_shift"]
        - projected["-+++"]["apparent_shift"]
    )
    coupling_free_invariant = sp.expand(
        projected["++++"]["loop_only"]
        - 10 * projected["-+++"]["loop_only"]
    )
    difference_real, difference_imaginary = complex_parts(apparent_difference)
    invariant_real, invariant_imaginary = complex_parts(coupling_free_invariant)
    rows.append(
        {
            "projection_id": "ABREU4973_CROSS_HELICITY",
            "helicity": "++++ minus 10*(-+++)",
            "s": SYMMETRIC_S,
            "t": SYMMETRIC_T,
            "u": SYMMETRIC_U,
            "stu": SYMMETRIC_STU,
            "C3_projector": 0,
            "Einstein_loop_remainder_exact": exact_text(coupling_free_invariant),
            "Einstein_loop_remainder_real": invariant_real,
            "Einstein_loop_remainder_imag": invariant_imaginary,
            "apparent_delta_c_exact": exact_text(apparent_difference),
            "apparent_delta_c_real": difference_real,
            "apparent_delta_c_imag": difference_imaginary,
            "status": "C3_COUPLING_CANCELS_NONLOCAL_LOOP_INVARIANT_NONZERO",
        }
    )
    finite_shift_symbol, local_c, loop_pppp, loop_mppp = sp.symbols(
        "zeta c L_pppp L_mppp"
    )
    projector_pppp = projected["++++"]["projector"]
    projector_mppp = projected["-+++"]["projector"]
    amplitude_pppp = projector_pppp * local_c + loop_pppp
    amplitude_mppp = projector_mppp * local_c + loop_mppp
    transformed_pppp = sp.simplify(
        projector_pppp * (local_c + finite_shift_symbol)
        + loop_pppp
        - projector_pppp * finite_shift_symbol
        - amplitude_pppp
    )
    transformed_mppp = sp.simplify(
        projector_mppp * (local_c + finite_shift_symbol)
        + loop_mppp
        - projector_mppp * finite_shift_symbol
        - amplitude_mppp
    )
    rows.append(
        {
            "projection_id": "ABREU4973_SCHEME_ORBIT",
            "helicity": "both",
            "C3_projector": "P_h",
            "Einstein_loop_remainder_exact": "L_h -> L_h-P_h*zeta",
            "apparent_delta_c_exact": "c -> c+zeta",
            "status": "EXACT_FINITE_RENORMALIZATION_INVARIANCE_ONE_MATCH_REQUIRED",
        }
    )
    checks = {
        "Abreu_local_C3_projector_factor_ten": sp.simplify(
            projector_pppp - 10 * projector_mppp
        )
        == 0,
        "Abreu_raw_loop_remainder_not_local_C3_factor_ten": coupling_free_invariant
        != 0,
        "Abreu_apparent_finite_shifts_disagree": apparent_difference != 0,
        "finite_scheme_orbit_invariant_all_plus": transformed_pppp == 0,
        "finite_scheme_orbit_invariant_single_minus": transformed_mppp == 0,
    }
    summary = {
        "all_plus_apparent_shift": exact_text(
            projected["++++"]["apparent_shift"]
        ),
        "single_minus_apparent_shift": exact_text(
            projected["-+++"]["apparent_shift"]
        ),
        "apparent_shift_difference": exact_text(apparent_difference),
        "coupling_free_cross_helicity_invariant": exact_text(
            coupling_free_invariant
        ),
    }
    return tagged(rows), checks, summary


def source_requirement_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "requirement_id": "C3SRC4973_00_KERNEL",
                "required_object": "momentum-resolved fluctuation C3 source H_C3,k(s/k^2,t/k^2)",
                "parent_status": "ABSENT",
                "source_path": relative(SOURCE_2605_TEX),
                "source_scope": "quadratic background form factors only; fluctuation extension explicitly beyond scope",
                "needed_for": "fixed-point characteristic integral and finite conversion",
                "next_action": "derive the C3 fluctuation kernel from the parent vertex flow",
            },
            {
                "requirement_id": "C3SRC4973_01_PROPAGATOR",
                "required_object": "full parent Gamma_k^(2) including graviton ghost motion and retained matter thresholds",
                "parent_status": "PARTIAL_LOCAL_HESSIANS_ONLY",
                "source_path": relative(SOURCE_2605_TEX),
                "source_scope": "the fluctuation kernel depends on the dressed inverse propagator",
                "needed_for": "loop denominator and threshold content",
                "next_action": "assemble the source-locked parent Hessian in one gauge and field parametrization",
            },
            {
                "requirement_id": "C3SRC4973_02_VERTICES",
                "required_object": "parent Gamma_k^(3) and Gamma_k^(4) fluctuation vertices",
                "parent_status": "NOT_ASSEMBLED_FOR_C3_FORM_FACTOR",
                "source_path": relative(SOURCE_2605_TEX),
                "source_scope": "primary source gives the tadpole plus two-vertex kernel topology",
                "needed_for": "momentum and angular dependence of H_C3,k",
                "next_action": "differentiate the retained parent action and project the two topologies",
            },
            {
                "requirement_id": "C3SRC4973_03_OPERATOR_BASIS",
                "required_object": "nonlocal cubic and quartic graviton operator basis with channel arguments",
                "parent_status": "GENERIC_BASIS_SOURCES_ACQUIRED_NOT_PARENT_PROJECTED",
                "source_path": f"{relative(SOURCE_2210_TEX)};{relative(SOURCE_0911_TEX)}",
                "source_scope": "six arguments at four-field order; generic 29-invariant third-order heat-kernel basis",
                "needed_for": "avoid mixing C3 with redundant or quartic structures",
                "next_action": "reduce on shell before numerical integration and retain both helicity projectors",
            },
            {
                "requirement_id": "C3SRC4973_04_REGULATOR",
                "required_object": "same regulator gauge ghost and field split as the selected local EAA trajectory",
                "parent_status": "LOCAL_SCHEME_LOCKED_FULL_FORM_FACTOR_CONVERSION_ABSENT",
                "source_path": relative(RESULT_4972),
                "source_scope": "tree normalization is exact but finite Wilsonian-to-HV conversion remains",
                "needed_for": "meaningful finite scheme match",
                "next_action": "calculate both local and momentum projections in one declared scheme",
            },
            {
                "requirement_id": "C3SRC4973_05_PROJECTORS",
                "required_object": "++++ and -+++ physical C3 helicity projectors",
                "parent_status": "AVAILABLE_EXACT",
                "source_path": f"{relative(RESULT_4972)};{relative(ABREU_PPPP)};{relative(ABREU_MPPP)}",
                "source_scope": "P_pppp/P_mppp=10 and exact action normalization",
                "needed_for": "operator and convention check",
                "next_action": "apply to every momentum-resolved kernel row",
            },
            {
                "requirement_id": "C3SRC4973_06_ENDPOINTS",
                "required_object": "local beta and physical infrared logarithmic slope",
                "parent_status": "AVAILABLE_EXACT",
                "source_path": relative(NONLOCAL_4972),
                "source_scope": "four state-count endpoint rows close the logarithmic running",
                "needed_for": "UV and IR endpoint tests",
                "next_action": "use as boundary checks, not as a substitute for the interior kernel",
            },
            {
                "requirement_id": "C3SRC4973_07_FINITE_MATCH",
                "required_object": "one finite regulator-to-HV amplitude match or one measured lambda",
                "parent_status": "ABSENT",
                "source_path": relative(ABREU_MAIN),
                "source_scope": "two-loop amplitude has an exact finite-renormalization orbit and one physical scale lambda",
                "needed_for": "absolute on-shell anchor if the kernel is not calculated",
                "next_action": "calculate one common-scheme amplitude datum or retain lambda explicitly",
            },
        ]
    )


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes: dict[str, str] = {}
    for path, expected_hash in EXPECTED_HASHES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        actual_hash = digest(path)
        if actual_hash != expected_hash:
            raise ValueError(
                f"source hash mismatch for {path}: {actual_hash} != {expected_hash}"
            )
        source_hashes[relative(path)] = actual_hash

    source_checks = source_scope_checks()
    characteristic_output, characteristic_checks = characteristic_rows()
    null_output, null_checks = null_deformation_rows()
    abreu_output, abreu_checks, abreu_summary = abreu_projection_rows()
    requirement_output = source_requirement_rows()

    result_4972 = json.loads(RESULT_4972.read_text(encoding="utf-8"))
    nonlocal_4972 = read_csv(NONLOCAL_4972)
    absent_required = [
        row["requirement_id"]
        for row in requirement_output
        if row["parent_status"] == "ABSENT"
    ]
    checks = {
        **source_checks,
        **characteristic_checks,
        **null_checks,
        **abreu_checks,
        "4972_parent_result_passed": bool(result_4972["all_checks_pass"]),
        "4972_four_nonlocal_endpoint_rows_retained": len(nonlocal_4972) == 4,
        "source_requirements_include_kernel_and_finite_match": set(
            absent_required
        )
        == {"C3SRC4973_00_KERNEL", "C3SRC4973_07_FINITE_MATCH"},
        "all_scientific_rows_remain_nonclaim": all(
            row["valid_for_full_MTS_claim"] is False
            for row in (
                characteristic_output
                + null_output
                + abreu_output
                + requirement_output
            )
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}

    write_csv(CHARACTERISTICS_CSV, characteristic_output)
    write_csv(NULL_DEFORMATION_CSV, null_output)
    write_csv(ABREU_PROJECTION_CSV, abreu_output)
    write_csv(SOURCE_REQUIREMENTS_CSV, requirement_output)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "C3_fixed_point_flow": {
            "definition": "F_k(x,y)=k^2 f_C3,k(k^2x,k^2y)",
            "flow": "partial_lnk F=2F+2xF_x+2yF_y+H_C3,k",
            "fixed_point": "(1+x partial_x+y partial_y)F_*=-H_*/2",
            "characteristic": "F_*(rho,zrho)=C(z)/rho-[1/(2rho)] integral_0^rho H_*(v,zv)dv",
            "quasi_local_boundary": "C(z)=0 conditionally excludes the inverse-momentum homogeneous mode",
        },
        "finite_anchor_test": {
            "null_kernel": "Delta K_a(x)=a*x/(1+x)^2",
            "endpoint_shifts": {"local_beta": 0, "physical_log": 0},
            "finite_shift": "Delta(delta_c_fin)=-a/2",
            "conclusion": "local beta plus physical logarithm do not identify the finite conversion",
        },
        "direct_two_loop_remainder_test": abreu_summary,
        "scheme_orbit": "c -> c+zeta and L_h -> L_h-P_h*zeta leaves every amplitude invariant",
        "decision": "FULL_MOMENTUM_KERNEL_REQUIRED_OR_ONE_EXPLICIT_MATCHED_LAMBDA",
        "route_status": "CHARACTERISTIC_DERIVED_CONDITIONAL_UNIQUENESS_PROVED_CURRENT_LOCAL_ONLY_FINITE_ANCHOR_CONSTRUCTIVELY_REJECTED",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "valid_for_full_MTS_claim": False,
        "claim_ceiling": "C3 form-factor equation and exact finite-anchor non-identifiability from current local and endpoint data; no complete amplitude claim",
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_PASSED={sum(bool(value) for value in checks.values())}", flush=True)
    print(
        f"{MARKER}_FAILED={sum(not bool(value) for value in checks.values())}",
        flush=True,
    )
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if not result["all_checks_pass"]:
        failed = [key for key, value in checks.items() if not value]
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
