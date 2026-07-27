from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4930"
SCRIPTS = POST / "scripts"

MARKER = "MTS_SIX_DERIVATIVE_MATTER_BLOCK_STABILITY_4930"
VALIDATION_MARKER = "MTS_SIX_DERIVATIVE_MATTER_BLOCK_VALIDATION_4930"
FORMAL_MARKER = "PPC4161_SIX_DERIVATIVE_MATTER_BLOCK_4930"
NEXT_TARGET = "4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md"

RESEARCH = SCRIPTS / "Y5_R2FR_4930_six_derivative_matter_block_stability.py"
CHECKPOINT = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
FORMAL_NOTE = FORMAL / "946-PPC4161-six-derivative-matter-basis-and-C3-block-stability.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
VALIDATION_OUTPUT = OUTPUT / "P8_Y5_BRR545_4930_VALIDATION.csv"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv",
    "P8_Y5_R2FR_4930_QUOTIENT_IDENTITIES.csv",
    "P8_Y5_R2FR_4930_GRSMEFT_DIM6_BASIS.csv",
    "P8_Y5_R2FR_4930_SCALAR_FIXED_POINT_COMPARATOR.csv",
    "P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_LEAK.csv",
    "P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_SCAN.csv",
    "P8_Y5_R2FR_4930_GAUGE_DETERMINANT_MIXING_WITNESS.csv",
    "P8_Y5_R2FR_4930_BLOCK_TRIANGULARITY_GATE.csv",
    "P8_Y5_R2FR_4930_MODAL_STABILITY_BOUND.csv",
    "P8_Y5_R2FR_4930_MODAL_MIXING_MONTE_CARLO.csv",
    "P8_Y5_R2FR_4930_MAXWELL_CONSTITUTIVE_MAP.csv",
    "P8_Y5_R2FR_4930_MAXWELL_CURVATURE_SMOKE.csv",
    "P8_Y5_R2FR_4930_WILSON_PARAMETER_COUNT.csv",
    "P8_Y5_R2FR_4930_PARENT_INHERITANCE_GATE.csv",
    "P8_Y5_R2FR_4930_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4930_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "1908.08050v2.pdf": "0a7488198a3d164e33461bd149a83117be0f005b34363f77d2f8667d04f321b3",
    SOURCE / "1908.08050v2-source.tar": "957fc506fb05d1692beab79f0979dda0bcb1867f378002f31640143c406e41ed",
    SOURCE / "2110.09566v1.pdf": "ce782d269d38357b2c68eb805072395f60c0a22776b6cdce819a698427d72b59",
    SOURCE / "2110.09566v1-source.tar": "2ef680490ccf2e3f86cc8ff7f926fdd7e612345284948dd7775417326e617156",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not reader.fieldnames or any(None in row for row in rows):
        raise ValueError(f"malformed CSV: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def add_check(
    rows: list[dict[str, Any]],
    validation_id: str,
    description: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": validation_id,
            "description": description,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "checkpoint_marker": VALIDATION_MARKER,
            "valid_for_claim": False,
            "source_checked_date": "2026-07-12",
        }
    )


def beta_g(newton: float, weight_1: float) -> float:
    pure = 2.0 * newton * (-32.0 * newton + 6.0 * math.pi) / (
        -9.0 * newton + 6.0 * math.pi
    )
    return pure + weight_1 * newton**2 / (6.0 * math.pi)


def beta_c3_pure(newton: float, c3_coupling: float) -> float:
    pi = math.pi
    numerator = (
        69.0 * newton
        + (
            -3_709_440.0 * newton**2 * pi
            + 14_515_200.0 * newton * pi**2
            + 1_451_520.0 * pi**3
        )
        * c3_coupling
        + (
            47_585_664.0 * newton**3 * pi**2
            - 21_337_344.0 * newton**2 * pi**3
        )
        * c3_coupling**2
        + (
            -84_188_160.0 * newton**4 * pi**3
            + 78_382_080.0 * newton**3 * pi**4
        )
        * c3_coupling**3
    )
    return -numerator / (120_960.0 * (9.0 * newton - 6.0 * pi) * pi**2)


def independent_eta_fixed_point(weight_1: float, eta_scalar: float) -> tuple[float, float]:
    newton_star = brentq(
        lambda value: beta_g(value, weight_1),
        1.0e-12,
        (2.0 * math.pi / 3.0) * (1.0 - 1.0e-10),
    )
    source = eta_scalar / (30_240.0 * (4.0 * math.pi) ** 2)
    pi = math.pi
    denominator = 120_960.0 * (9.0 * newton_star - 6.0 * pi) * pi**2
    coefficients = [
        -84_188_160.0 * newton_star**4 * pi**3
        + 78_382_080.0 * newton_star**3 * pi**4,
        47_585_664.0 * newton_star**3 * pi**2
        - 21_337_344.0 * newton_star**2 * pi**3,
        -3_709_440.0 * newton_star**2 * pi
        + 14_515_200.0 * newton_star * pi**2
        + 1_451_520.0 * pi**3,
        69.0 * newton_star - source * denominator,
    ]
    roots = np.roots(coefficients)
    real_roots = [float(root.real) for root in roots if abs(root.imag) < 1.0e-9]
    return newton_star, min(real_roots, key=abs)


def main() -> int:
    checks: list[dict[str, Any]] = []
    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__).resolve()):
        try:
            compile(source_text(path), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4930_00_compile",
        "research and validation scripts compile in memory",
        "no syntax errors",
        ";".join(compile_failures) or "no syntax errors",
        not compile_failures,
    )

    run = subprocess.run(
        [sys.executable, "-B", str(RESEARCH)],
        cwd=POST,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    add_check(
        checks,
        "VAL4930_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}; stderr={run.stderr.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4930_SIX_DERIVATIVE_MATTER_BLOCK_PASS" in run.stdout
        and not run.stderr.strip(),
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4930_02_outputs",
        "all expected evidence tables exist",
        len(EXPECTED_OUTPUTS),
        len(EXPECTED_OUTPUTS) - len(missing_outputs),
        not missing_outputs,
    )

    parsed: dict[str, list[dict[str, str]]] = {}
    parse_failures: list[str] = []
    for name in EXPECTED_OUTPUTS:
        try:
            parsed[name] = read_csv(OUTPUT / name)
        except (OSError, ValueError) as error:
            parse_failures.append(f"{name}:{error}")
    add_check(
        checks,
        "VAL4930_03_csv_shape",
        "all evidence CSVs parse without malformed rows",
        "no malformed rows",
        ";".join(parse_failures) or "no malformed rows",
        not parse_failures,
    )

    all_rows = [row for rows in parsed.values() for row in rows]
    marker_failures = [row for row in all_rows if row.get("checkpoint_marker") != MARKER]
    add_check(
        checks,
        "VAL4930_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable = [row for row in all_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4930_05_nonclaim",
        "all checkpoint evidence remains private nonclaim",
        0,
        len(claimable),
        not claimable,
    )
    placeholders = [
        row
        for row in all_rows
        if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4930_06_no_placeholders",
        "no generated row contains a placeholder token",
        0,
        len(placeholders),
        not placeholders,
    )

    hash_failures = [
        path.name
        for path, expected_hash in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected_hash
    ]
    add_check(
        checks,
        "VAL4930_07_hashes",
        "all four primary PDF and author-source files match locked hashes",
        0,
        len(hash_failures),
        not hash_failures,
    )

    source_rows = parsed["P8_Y5_R2FR_4930_SOURCE_REGISTER.csv"]
    source_failures = [row["source_id"] for row in source_rows if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4930_08_sources",
        "primary archives source markers generated ledgers and URLs verify",
        "28 rows; zero failures",
        f"{len(source_rows)} rows; failures={source_failures}",
        len(source_rows) == 28 and not source_failures,
    )

    scalar = parsed["P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"]
    scalar_by_id = {row["operator_id"]: row for row in scalar}
    add_check(
        checks,
        "VAL4930_09_scalar_basis",
        "the CP-even scalar quotient contains exactly O1 through O5",
        "five independent rows; O4 direct Hessian",
        f"ids={sorted(scalar_by_id)}; O4={scalar_by_id['S6_O4']['quadratic_Hessian_nonzero_at_nabla_phi_zero']}",
        set(scalar_by_id) == {"S6_O1", "S6_O2", "S6_O3", "S6_O4", "S6_O5"}
        and all(as_bool(row["IBP_EOM_quotient_independent"]) for row in scalar)
        and as_bool(scalar_by_id["S6_O4"]["quadratic_Hessian_nonzero_at_nabla_phi_zero"])
        and not as_bool(scalar_by_id["S6_O1"]["quadratic_Hessian_nonzero_at_nabla_phi_zero"])
        and not as_bool(scalar_by_id["S6_O2"]["quadratic_Hessian_nonzero_at_nabla_phi_zero"])
        and not as_bool(scalar_by_id["S6_O5"]["quadratic_Hessian_nonzero_at_nabla_phi_zero"]),
    )

    identities = {row["identity_id"]: row for row in parsed["P8_Y5_R2FR_4930_QUOTIENT_IDENTITIES.csv"]}
    add_check(
        checks,
        "VAL4930_10_quotient_identities",
        "the two exact reductions and five-operator completeness row agree with source",
        "3 O3; -O4/8; count 5",
        f"{identities['QI4930_00_Weyl_wave']['coefficient']};{identities['QI4930_01_scalar_Hessian']['coefficient']};{identities['QI4930_03_completeness']['coefficient']}",
        math.isclose(float(identities["QI4930_00_Weyl_wave"]["coefficient"]), 3.0)
        and math.isclose(float(identities["QI4930_01_scalar_Hessian"]["coefficient"]), -0.125)
        and int(identities["QI4930_03_completeness"]["coefficient"]) == 5,
    )

    grsmeft = parsed["P8_Y5_R2FR_4930_GRSMEFT_DIM6_BASIS.csv"]
    even = [row for row in grsmeft if row["CP"] == "even"]
    odd = [row for row in grsmeft if row["CP"] == "odd"]
    multiplicities = {row["coefficient"]: int(row["internal_multiplicity"]) for row in grsmeft}
    add_check(
        checks,
        "VAL4930_11_grsmeft_basis",
        "dimension-six GRSMEFT has ten operators in five parity pairs",
        "10 total; 5 even; 5 odd; B/W/G multiplicities 1/3/8",
        f"total={len(grsmeft)}; even={len(even)}; odd={len(odd)}; mult={multiplicities}",
        len(grsmeft) == 10
        and len(even) == 5
        and len(odd) == 5
        and multiplicities["c_B"] == 1
        and multiplicities["c_W"] == 3
        and multiplicities["c_G"] == 8,
    )

    comparator = {row["branch"]: row for row in parsed["P8_Y5_R2FR_4930_SCALAR_FIXED_POINT_COMPARATOR.csv"]}
    primary = comparator["2110_full_eta_primary"]
    secondary = comparator["2110_full_eta_secondary"]
    add_check(
        checks,
        "VAL4930_12_scalar_comparator",
        "source fixed-point branches reproduce eta and matter stability signs",
        "primary eta 1.27 all irrelevant; secondary not all irrelevant",
        f"primary={primary}; secondary_all={secondary['all_tracked_matter_directions_irrelevant']}",
        math.isclose(float(primary["eta_scalar"]), 1.27)
        and math.isclose(float(primary["c_X2_star"]), -16.6)
        and as_bool(primary["all_tracked_matter_directions_irrelevant"])
        and not as_bool(secondary["all_tracked_matter_directions_irrelevant"])
        and all(not as_bool(row["projection_compatible_with_4928_numeric_splice"]) for row in comparator.values()),
    )

    leak = parsed["P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_LEAK.csv"]
    eta_primary = next(row for row in leak if math.isclose(float(row["eta_scalar"]), 1.27))
    independent_g, independent_h = independent_eta_fixed_point(1.0, 1.27)
    expected_source = 1.27 / (30_240.0 * (4.0 * math.pi) ** 2)
    add_check(
        checks,
        "VAL4930_13_eta_leak",
        "independent calculation reproduces the direct eta source and fixed point",
        "eta*c6 and matching g*,h*",
        f"source={eta_primary['delta_beta_h_equals_eta_c6']}; g={independent_g}; h={independent_h}",
        math.isclose(float(eta_primary["delta_beta_h_equals_eta_c6"]), expected_source, rel_tol=1.0e-14)
        and math.isclose(float(eta_primary["g_star"]), independent_g, rel_tol=1.0e-12)
        and math.isclose(float(eta_primary["h_star"]), independent_h, rel_tol=1.0e-10)
        and as_bool(eta_primary["two_coordinate_topology_survives"]),
    )

    scan = parsed["P8_Y5_R2FR_4930_ANOMALOUS_DIMENSION_SCAN.csv"]
    scan_failures = [row["scan_id"] for row in scan if not as_bool(row["survives"]) or not as_bool(row["passed"])]
    theta_g = [float(row["theta_g"]) for row in scan]
    theta_h = [float(row["theta_h"]) for row in scan]
    add_check(
        checks,
        "VAL4930_14_eta_scan",
        "the full W1-eta direct-leak grid preserves inherited topology",
        "9801 rows; zero failures; exponents bounded from zero",
        f"rows={len(scan)}; failures={len(scan_failures)}; theta_g=[{min(theta_g)},{max(theta_g)}]; theta_h=[{min(theta_h)},{max(theta_h)}]",
        len(scan) == 9801
        and not scan_failures
        and min(theta_g) > 2.4
        and max(theta_h) < -6.3,
    )

    gauge = parsed["P8_Y5_R2FR_4930_GAUGE_DETERMINANT_MIXING_WITNESS.csv"]
    gauge_by_sector = {row["sector"]: row for row in gauge}
    add_check(
        checks,
        "VAL4930_15_gauge_witness",
        "gauge determinant cubic witnesses include U1 SU2 and SU3 multiplicities",
        "-32/3; -32; -256/3",
        ";".join(f"{key}={row['cubic_C3_witness_coefficient_times_multiplicity']}" for key, row in gauge_by_sector.items()),
        len(gauge) == 3
        and math.isclose(float(gauge_by_sector["U1Y"]["cubic_C3_witness_coefficient_times_multiplicity"]), -32.0 / 3.0)
        and math.isclose(float(gauge_by_sector["SU2"]["cubic_C3_witness_coefficient_times_multiplicity"]), -32.0)
        and math.isclose(float(gauge_by_sector["SU3"]["cubic_C3_witness_coefficient_times_multiplicity"]), -256.0 / 3.0)
        and all(not as_bool(row["full_FRG_coefficient_derived"]) for row in gauge),
    )

    block = {row["clause"]: row for row in parsed["P8_Y5_R2FR_4930_BLOCK_TRIANGULARITY_GATE.csv"]}
    add_check(
        checks,
        "VAL4930_16_block_gate",
        "generic full C3 block triangularity is rejected while quotient clauses close",
        "quotients true; O4 Higgs gauge eta and full triangle false",
        ";".join(f"{key}={row['satisfied']}" for key, row in block.items()),
        as_bool(block["scalar_six_derivative_quotient"]["satisfied"])
        and as_bool(block["GRSMEFT_dimension_six_quotient"]["satisfied"])
        and not as_bool(block["scalar_O4_portal"]["satisfied"])
        and not as_bool(block["Higgs_C2_portal"]["satisfied"])
        and not as_bool(block["gauge_CFF_portals"]["satisfied"])
        and not as_bool(block["scalar_anomalous_dimension"]["satisfied"])
        and not as_bool(block["full_block_triangularity"]["satisfied"]),
    )

    modal = parsed["P8_Y5_R2FR_4930_MODAL_STABILITY_BOUND.csv"]
    signed = [row for row in modal if row["scenario"].startswith("full_signed_")]
    no_eta = next(row for row in signed if row["scenario"] == "full_signed_C3_plus_scalar_no_eta")
    pair = next(row for row in modal if row["scenario"] == "pairwise_scalar_no_eta_real")
    add_check(
        checks,
        "VAL4930_17_modal_contract",
        "signed comparator and pairwise stability contracts are numerically consistent",
        "3 signed rows; one relevant; gap 1.88; product 75.0975519",
        f"signed={len(signed)}; relevant={no_eta['relevant_beta_modes']}; gap={no_eta['imaginary_axis_gap']}; pair={pair['sufficient_modal_mixing_bound']}",
        len(signed) == 3
        and all(int(row["relevant_beta_modes"]) == 1 for row in signed)
        and math.isclose(float(no_eta["imaginary_axis_gap"]), 1.88)
        and "75.09755189359788" in pair["sufficient_modal_mixing_bound"]
        and all(not as_bool(row["full_MTS_bound_measured"]) for row in modal),
    )

    monte = parsed["P8_Y5_R2FR_4930_MODAL_MIXING_MONTE_CARLO.csv"]
    theorem_rows = [row for row in monte if float(row["norm_over_gap"]) < 1.0]
    outside_rows = [row for row in monte if float(row["norm_over_gap"]) >= 1.0]
    add_check(
        checks,
        "VAL4930_18_modal_smoke",
        "seeded signed-index smoke respects the theorem and exposes above-bound failures",
        "5 theorem rows with zero failures; at least one above-bound failure",
        f"theorem={[(row['norm_over_gap'],row['failed_signed_stability_index']) for row in theorem_rows]}; outside={[(row['norm_over_gap'],row['failed_signed_stability_index']) for row in outside_rows]}",
        len(monte) == 9
        and len(theorem_rows) == 5
        and all(int(row["failed_signed_stability_index"]) == 0 for row in theorem_rows)
        and all(as_bool(row["theorem_guarantees_no_crossing"]) for row in theorem_rows)
        and any(int(row["failed_signed_stability_index"]) > 0 for row in outside_rows),
    )

    maxwell = {row["map_id"]: row for row in parsed["P8_Y5_R2FR_4930_MAXWELL_CONSTITUTIVE_MAP.csv"]}
    add_check(
        checks,
        "VAL4930_19_maxwell_map",
        "electroweak constitutive Maxwell Poynting vacuum and conservation rows close",
        "7 rows with c_gamma H epsilon Poynting and F=0",
        f"rows={len(maxwell)}; ids={sorted(maxwell)}",
        len(maxwell) == 7
        and "cos^2" in maxwell["EM4930_00_EW"]["equation"]
        and "-4 c_gamma" in maxwell["EM4930_01_constitutive"]["equation"]
        and "epsilon_CF" in maxwell["EM4930_04_Poynting"]["equation"]
        and "F=0" in maxwell["EM4930_05_vacuum"]["equation"]
        and all(as_bool(row["passed"]) for row in maxwell.values()),
    )

    curvature = parsed["P8_Y5_R2FR_4930_MAXWELL_CURVATURE_SMOKE.csv"]
    add_check(
        checks,
        "VAL4930_20_curvature_smoke",
        "four curvature-control rows remain positive internal nonempirical targets",
        "4 positive rows; empirical false",
        f"rows={len(curvature)}; arenas={[row['arena'] for row in curvature]}",
        len(curvature) == 4
        and all(float(row["sqrt_C2_m_minus2"]) > 0.0 for row in curvature)
        and all(float(row["abs_c_gamma_internal_bound_m2"]) > 0.0 for row in curvature)
        and all(not as_bool(row["empirical_constraint"]) for row in curvature),
    )

    wilson = {
        row["arena_or_action"]: int(row["independent_gravity_coupled_Wilson_coefficients"])
        for row in parsed["P8_Y5_R2FR_4930_WILSON_PARAMETER_COUNT.csv"]
    }
    add_check(
        checks,
        "VAL4930_21_wilson_count",
        "arena-specific and full-action Wilson counts are distinct",
        "1,2,5,5,9,14",
        wilson,
        wilson
        == {
            "uncharged_constant_motion_vacuum": 1,
            "photon_curved_background": 2,
            "unbroken_SM_parity_even_dimension6_gravity": 5,
            "shift_symmetric_motion_plus_gravity_six_derivative": 5,
            "unified_parity_even_union": 9,
            "unified_with_GRSMEFT_parity_partners": 14,
        },
    )

    inheritance = {row["clause"]: row for row in parsed["P8_Y5_R2FR_4930_PARENT_INHERITANCE_GATE.csv"]}
    add_check(
        checks,
        "VAL4930_22_inheritance",
        "full C3 flow inheritance remains false because portal beta blocks are open",
        "all_parent_inheritance false and three portal clauses open",
        f"all={inheritance['all_parent_inheritance']['satisfied']}",
        not as_bool(inheritance["scalar_O4_beta"]["satisfied"])
        and not as_bool(inheritance["Higgs_portal_beta"]["satisfied"])
        and not as_bool(inheritance["gauge_portal_beta"]["satisfied"])
        and not as_bool(inheritance["modal_mixing_norm"]["satisfied"])
        and not as_bool(inheritance["all_parent_inheritance"]["satisfied"]),
    )

    gates = {row["gate"]: row for row in parsed["P8_Y5_R2FR_4930_GATE_DECISION.csv"]}
    add_check(
        checks,
        "VAL4930_23_decision",
        "final gate rejects generic triangle retains weak GR and selects 4931",
        "triangle rejected; vacuum one; full nine; next 4931",
        f"triangle={gates['generic_block_triangularity']['status']}; vacuum={gates['vacuum_Wilson_count']['status']}; full={gates['full_unified_Wilson_count']['status']}; next={gates['next_target']['decision']}",
        gates["generic_block_triangularity"]["status"] == "REJECTED_WITH_SPECIAL_ZERO_SUBMANIFOLD"
        and gates["vacuum_Wilson_count"]["status"] == "ONE_RETAINED"
        and gates["full_unified_Wilson_count"]["status"] == "NINE_PARITY_EVEN_BEFORE_UV_PREDICTION"
        and gates["weak_GR_Newton"]["status"] == "RETAINED"
        and gates["Maxwell_full_MTS_to_GR"]["status"] == "BOUNDED_NOT_PROMOTED"
        and gates["next_target"]["decision"] == NEXT_TARGET,
    )

    marker_paths = [
        (CHECKPOINT, MARKER),
        (FORMAL_NOTE, FORMAL_MARKER),
        (PROVENANCE, "MTS_SIX_DERIVATIVE_MATTER_BLOCK_PROVENANCE_4930"),
        (CLAIMS, "L-772"),
        (VARIABLES, "C3BlockStatus4930_MTS"),
        (EQUATIONS, "1.223 Six-derivative matter quotient and C3 block-stability boundary"),
        (RED_TEAM, "174. Arena silence is not full-action derivation"),
        (SPINE, "PPC4161 checkpoint 4930"),
        (RESUME, NEXT_TARGET),
    ]
    marker_path_failures = [
        path.name
        for path, marker in marker_paths
        if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4930_24_registers",
        "checkpoint provenance formal note registers and resume markers exist",
        0,
        len(marker_path_failures),
        not marker_path_failures,
    )

    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    add_check(
        checks,
        "VAL4930_25_register_csv",
        "claims and variable registers remain parseable with unique new identifiers",
        "one L-772 and sixteen 4930 variables",
        f"L-772={sum(row['claim_id'] == 'L-772' for row in claims_rows)}; vars={sum('4930_MTS' in row['symbol'] for row in variable_rows)}",
        sum(row["claim_id"] == "L-772" for row in claims_rows) == 1
        and sum("4930_MTS" in row["symbol"] for row in variable_rows) == 16,
    )

    pycache = list(SCRIPTS.rglob("__pycache__"))
    checkpoint_cache = [
        path
        for directory in pycache
        for path in directory.glob("*")
        if "4930" in path.name
    ]
    add_check(
        checks,
        "VAL4930_26_pycache",
        "checkpoint execution creates no 4930 bytecode cache",
        0,
        len(checkpoint_cache),
        not checkpoint_cache,
    )

    write_csv(VALIDATION_OUTPUT, checks)
    passed_count = sum(as_bool(row["passed"]) for row in checks)
    all_passed = passed_count == len(checks)
    print("P8_Y5_BRR545_4930_VALIDATION_PASS" if all_passed else "P8_Y5_BRR545_4930_VALIDATION_FAIL")
    print(f"checks_passed={passed_count}/{len(checks)}")
    if not all_passed:
        print("failed=" + ",".join(row["validation_id"] for row in checks if not as_bool(row["passed"])))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
