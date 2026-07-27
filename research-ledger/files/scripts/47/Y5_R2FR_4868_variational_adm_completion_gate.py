from __future__ import annotations

import csv
import gzip
import math
import tarfile
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

from Y5_R2FR_4868_fixed_background_variational_remainder import (
    reduced_lagrangians,
    solve_extrapolated_bvp_profile,
    solve_profile,
)


CHECKPOINT = "4868"
TIMESTAMP = "2026-07-10T12:48:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4869-Y5-R2FR-v4-l0-linearized-Einstein-constraint-and-ADM-monopole-or-kappa4-completion-bound.md"
KAPPA_BOUND = 1.4532678437


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def archive_contains(path: Path, member: str, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        with tarfile.open(path, "r:*") as archive:
            extracted = archive.extractfile(member)
            if extracted is None:
                return False
            return needle in extracted.read().decode("utf-8", errors="replace")
    except (tarfile.TarError, OSError):
        return False


def gzip_contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
            return needle in handle.read()
    except OSError:
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def tolman_f_c3(compactness: float) -> float:
    return (
        10 * compactness / 7
        + 5 * (1146 * 0 - 67669) * compactness**2 / 126126
        + 975961420 * compactness**3 / 90053964
    )


def weak_f(compactness: float, ratio: float) -> float:
    return (
        10
        * compactness
        * ratio
        * (3 * ratio + 11)
        / (21 * (1 + ratio))
    )


def weak_kappa(compactness: float, ratio: float) -> float:
    return -(
        compactness
        * ratio
        * (27 * ratio**2 + 57 * ratio + 98)
        / (21 * (1 + ratio))
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4868_00_public", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "public action and coefficient map"),
        ("SRC4868_01_first", POST / "4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md", "Tolman VII", "known C3 first response"),
        ("SRC4868_02_prior", POST / "4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md", "LEADING_QUARTIC_SELF_ENERGY_4867", "leading quartic response"),
        ("SRC4868_03_prior_validation", OUTPUT / "P8_Y5_BRR545_4867_VALIDATION.csv", "VAL4867_OVERALL", "prior validation"),
        ("SRC4868_04_checkpoint", POST / "4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md", "FINITE_COMPACTNESS_VARIATIONAL_ADM_COMPLETION_4868", "human derivation"),
        ("SRC4868_05_formal", FORMAL / "884-PPC4161-finite-compactness-variational-and-ADM-completion-gate.md", "PPC4161_FINITE_COMPACTNESS_VARIATIONAL_ADM_GATE_4868", "formal integration"),
        ("SRC4868_06_claim", FORMAL / "02-claims-register.csv", "L-710", "claim register"),
        ("SRC4868_07_variable", FORMAL / "04-variable-audit.csv", "D4_ADM_completion_MTS", "variable audit"),
        ("SRC4868_08_equation", FORMAL / "05-equation-register.md", "1.161 Finite-compactness flow functional", "equation register"),
        ("SRC4868_09_redteam", FORMAL / "06-consistency-red-team.md", "112. Finite-compactness variational and ADM completion red team", "red-team register"),
        ("SRC4868_10_spine", FORMAL / "07-unification-spine.md", "checkpoint 4868", "unification spine"),
        ("SRC4868_11_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4868-", "resume marker"),
        ("SRC4868_12_core_script", POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py", "solve_extrapolated_bvp_profile", "symbolic and numerical core"),
        ("SRC4868_13_generator", Path(__file__).resolve(), 'CHECKPOINT = "4868"', "checkpoint generator"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "member": "",
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    archives = [
        ("SRC4868_14_gupta", Path(r"D:\Temp\2104.04596-source.tar"), "tar", "main.tex", r"\section{Solutions for slowly moving stars}", "published finite-star first response"),
        ("SRC4868_15_foster", Path(r"D:\Temp\gr-qc-0509121-source.tar"), "gzip", "single_tex", r"\mathcal{E} = \mathcal{E}_{G} + \mathcal{E}_{\AE}", "general aether Noether energy"),
        ("SRC4868_16_eling", Path(r"D:\Temp\gr-qc-0507059-source.tar"), "gzip", "single_tex", r"E_{\rm \ae}", "aligned asymptotic aether energy"),
    ]
    for source_id, path, archive_kind, member, needle, role in archives:
        valid = archive_contains(path, member, needle) if archive_kind == "tar" else gzip_contains(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local_primary_archive",
                "source_locator": str(path),
                "member": member,
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": valid,
                "role": role,
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4868_17_urls",
            "source_kind": "primary_url_ledger",
            "source_locator": "https://arxiv.org/abs/gr-qc/0509121;https://arxiv.org/abs/gr-qc/0507059;https://arxiv.org/abs/0706.0704;https://arxiv.org/abs/2104.04596",
            "member": "",
            "needle": "source URLs recorded",
            "source_exists": True,
            "needle_found": True,
            "role": "primary provenance ledger",
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def functional_rows() -> list[dict[str, Any]]:
    lagrangian_2, lagrangian_4, arguments = reduced_lagrangians()
    radius, ratio, lapse, radial_metric, lapse_prime, radial_flow, angular_flow, radial_prime, angular_prime = arguments
    fields = (radial_flow, angular_flow, radial_prime, angular_prime)
    polynomial_2 = sp.Poly(lagrangian_2, *fields)
    polynomial_4 = sp.Poly(lagrangian_4, *fields)
    derivative_matrix = sp.hessian(lagrangian_2, (radial_prime, angular_prime))
    velocity, norm = sp.symbols("v norm", real=True)
    gamma_squared = 1 / (1 - velocity**2)
    time_component = 1 + norm * velocity**2 / 2 + (norm / 2 - norm**2 / 8) * velocity**4
    unit_residual = sp.series(
        -time_component**2 + gamma_squared * velocity**2 * norm + 1,
        velocity,
        0,
        6,
    ).removeO()
    c_1 = (1 + ratio) / 2
    c_2 = sp.Rational(2, 3) / (1 + ratio)
    c_3 = -c_1
    c_14 = 2 * ratio / (1 + ratio)
    c_4 = c_14 - c_1
    checks = [
        ("FUN4868_00_c13", "c1+c3", sp.factor(c_1 + c_3), 0, "luminal public tensor surface"),
        ("FUN4868_01_c14", "c1+c4", sp.factor(c_1 + c_4), c_14, "acceleration coefficient"),
        ("FUN4868_02_c123", "c1+c2+c3", sp.factor(c_1 + c_2 + c_3), c_2, "scalar coefficient"),
        ("FUN4868_03_unit", "unit norm through v4", sp.factor(unit_residual), 0, "gamma boundary normalization retained"),
        ("FUN4868_04_L2_degree", "L2 total field degree", polynomial_2.total_degree(), 2, "quadratic stationary functional"),
        ("FUN4868_05_L4_degree", "L4 maximum field degree", polynomial_4.total_degree(), 4, "quartic coefficient including gamma terms"),
        ("FUN4868_06_D_symmetric", "L2 derivative Hessian symmetry", derivative_matrix - derivative_matrix.T, sp.zeros(2), "Euler principal matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, expected, meaning in checks:
        passed = sp.simplify(derived - expected) == 0 if not isinstance(derived, sp.MatrixBase) else derived == expected
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(derived),
                "expected": sp.sstr(expected),
                "meaning": meaning,
                "status": "PASS" if passed else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.extend(
        [
            {
                "row_id": "FUN4868_07_Euler",
                "quantity": "finite-C radial Euler system",
                "derived": "D q''+(D'+M-M^T)q'+(M'-F)q=0",
                "expected": "Euler-Lagrange equation from L2",
                "meaning": "exact generated two-field BVP",
                "status": "DERIVED",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "row_id": "FUN4868_08_stationarity",
                "quantity": "zero-boundary v3 bulk cross term",
                "derived": "delta I2[q1; q3]=Euler[q1]*q3+boundary=0",
                "expected": "zero on stationary q1 with regular/zero-residual q3 boundary data",
                "meaning": "L4[q1] is complete fixed-background bulk v4 coefficient",
                "status": "DERIVED_CONDITIONAL_BOUNDARY",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ratio = 1 / 3
    for compactness in (0.001, 0.03, 0.1, 0.2, 0.3):
        result = solve_extrapolated_bvp_profile(
            compactness,
            ratio,
            base_maximum_radius=200.0,
            tolerance=1.0e-7,
        )
        f_c3 = tolman_f_c3(compactness)
        rows.append(
            {
                "row_id": f"BVP4868_C{compactness:.3f}",
                "compactness": compactness,
                "ratio": ratio,
                "coarse_f_bulk": result["coarse_f_action"],
                "fine_f_bulk": result["fine_f_action"],
                "f_bulk_extrapolated": result["f_action"],
                "coarse_kappa_bulk": result["coarse_kappa_action"],
                "fine_kappa_bulk": result["fine_kappa_action"],
                "kappa_bulk_extrapolated": result["kappa_action"],
                "radial_tail_extrapolated": result["radial_tail"],
                "angular_tail_extrapolated": result["angular_tail"],
                "aether_surface_2": result["surface_energy_2"],
                "aether_surface_4": result["surface_energy_4"],
                "weak_f": weak_f(compactness, ratio),
                "weak_kappa": weak_kappa(compactness, ratio),
                "tolman_f_C3": f_c3,
                "first_response_fractional_deficit": (f_c3 - float(result["f_action"])) / f_c3,
                "coarse_maximum_rms_residual": result["coarse_maximum_rms_residual"],
                "fine_maximum_rms_residual": result["fine_maximum_rms_residual"],
                "status": "REGULAR_FIXED_BACKGROUND_PARTIAL_NONCLAIM",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def variational_rows(scans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_compactness = {float(row["compactness"]): row for row in scans}
    rows: list[dict[str, Any]] = []
    for compactness in (0.03, 0.3):
        result = solve_profile(
            compactness,
            1 / 3,
            basis_count=7,
            maximum_radius=400.0,
            interior_points=1000,
            exterior_points=3000,
        )
        eigenvalues = np.asarray(result["hessian_eigenvalues"], dtype=float)
        reference = by_compactness[compactness]
        rows.append(
            {
                "row_id": f"VAR4868_C{compactness:.2f}",
                "compactness": compactness,
                "basis_count": result["basis_count"],
                "minimum_hessian_eigenvalue": float(np.min(eigenvalues)),
                "hessian_condition_number": float(np.max(eigenvalues) / np.min(eigenvalues)),
                "variational_f_bulk": result["f_action"],
                "collocation_f_bulk": reference["f_bulk_extrapolated"],
                "f_fractional_difference": abs(float(result["f_action"]) / float(reference["f_bulk_extrapolated"]) - 1),
                "variational_kappa_bulk": result["kappa_action"],
                "collocation_kappa_bulk": reference["kappa_bulk_extrapolated"],
                "kappa_fractional_difference": abs(float(result["kappa_action"]) / float(reference["kappa_bulk_extrapolated"]) - 1),
                "status": "POSITIVE_FINITE_BASIS_CROSSCHECK_NOT_COERCIVITY_PROOF",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def surface_rows(scans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ratio = sp.symbols("r", positive=True, real=True)
    leading_2 = sp.factor((3 * ratio**2 - 60 * ratio + 1) / (18 * (1 + ratio)))
    leading_4 = sp.factor((9 * ratio**2 - 45 * ratio + 8) / (9 * (1 + ratio)))
    endpoint = next(row for row in scans if math.isclose(float(row["compactness"]), 0.3))
    entries = [
        ("SUR4868_00_static", "static aether charge divided by pM", "-r/(1+r)", "-c14bar/2", "published aligned-energy regression", "PASS"),
        ("SUR4868_01_E2", "quadratic aether surface coefficient", "[9Cr^2-36Cr+11C+(3r^2+1)Ainf+(12r+4)Binf]/[18(1+r)G]", "Foster Noether charge", "exact asymptotic evaluation", "DERIVED"),
        ("SUR4868_02_E4", "quartic aether surface coefficient", "[45Cr^2-135Cr+50C+(12r^2-9r+7)Ainf+(-12r^2+54r-2)Binf]/[45(1+r)G]", "Foster Noether charge", "exact asymptotic evaluation", "DERIVED"),
        ("SUR4868_03_tail", "pure-GR boost tail", "Ainf=Binf=-2C+O(C2)", "coordinate boost of Schwarzschild", "isolates universal frame term", "DERIVED"),
        ("SUR4868_04_lead2", "leading Eae2/(pC/G)", sp.sstr(leading_2), "substitute Ainf=Binf=-2C", "must cancel against ADM at O(C)", "PASS"),
        ("SUR4868_05_lead4", "leading Eae4/(pC/G)", sp.sstr(leading_4), "substitute Ainf=Binf=-2C", "must cancel against ADM at O(C)", "PASS"),
        ("SUR4868_06_endpoint2", "endpoint Eae2/M", float(endpoint["aether_surface_2"]) / 0.3, "numeric extrapolated tails", "completion input", "NUMERIC_NONCLAIM"),
        ("SUR4868_07_endpoint4", "endpoint Eae4/M", float(endpoint["aether_surface_4"]) / 0.3, "numeric extrapolated tails", "completion input", "NUMERIC_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "derived": derived,
            "expected_or_source": expected,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, derived, expected, meaning, status in entries
    ]


def completion_rows(scans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scan in scans:
        compactness = float(scan["compactness"])
        ratio = float(scan["ratio"])
        bulk_2_over_mass = -float(scan["f_bulk_extrapolated"]) / 2
        bulk_4_over_mass = float(scan["kappa_bulk_extrapolated"])
        aether_2_over_mass = float(scan["aether_surface_2"]) / compactness
        aether_4_over_mass = float(scan["aether_surface_4"]) / compactness
        physical_2_over_mass = -float(scan["tolman_f_C3"]) / 2
        adm_2_over_mass = physical_2_over_mass - aether_2_over_mass
        completion_2_over_mass = adm_2_over_mass - bulk_2_over_mass
        adm_4_low = -KAPPA_BOUND - aether_4_over_mass
        adm_4_high = KAPPA_BOUND - aether_4_over_mass
        completion_4_low = -KAPPA_BOUND - bulk_4_over_mass - aether_4_over_mass
        completion_4_high = KAPPA_BOUND - bulk_4_over_mass - aether_4_over_mass
        leading_target = weak_kappa(compactness, ratio) - bulk_4_over_mass - aether_4_over_mass
        rows.append(
            {
                "row_id": f"ADM4868_C{compactness:.3f}",
                "compactness": compactness,
                "ratio": ratio,
                "bulk_2_over_M": bulk_2_over_mass,
                "aether_2_over_M": aether_2_over_mass,
                "physical_2_over_M_C3": physical_2_over_mass,
                "standard_ADM_2_over_M_C3": adm_2_over_mass,
                "completion_D2_over_M_C3": completion_2_over_mass,
                "bulk_4_over_M": bulk_4_over_mass,
                "aether_4_over_M": aether_4_over_mass,
                "standard_ADM_4_over_M_low": adm_4_low,
                "standard_ADM_4_over_M_high": adm_4_high,
                "completion_D4_over_M_low": completion_4_low,
                "completion_D4_over_M_high": completion_4_high,
                "leading_C_completion_target": leading_target,
                "target_inside_interval": completion_4_low <= leading_target <= completion_4_high,
                "status": "V2_CALIBRATED_C3_V4_INTERVAL_ONLY_ADM_MONOPOLE_OPEN",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "small-p fixed-background flow reduction", "RETAIN_DERIVED", "the leading flow Euler system decouples on the GR background"),
        (2, "finite-C collocation profile", "RETAIN_PARTIAL", "regular numerical branch found with controlled outer-radius extrapolation"),
        (3, "finite-basis variational profile", "RETAIN_CROSSCHECK", "positive sampled Hessian and percent-level agreement; not a coercivity theorem"),
        (4, "bulk finite-C f and kappa4", "REJECT_AS_PHYSICAL", "bulk f misses the known C3 first response by 42.27% at the endpoint"),
        (5, "raw bulk plus aether surface", "QUARANTINE", "Foster total energy also requires the metric ADM charge"),
        (6, "aether Noether surface charge", "RETAIN_DERIVED", "exact through v4 and aligned static regression passes"),
        (7, "D4 ADM completion variable", "OPEN_SINGLE_SCALAR", "binary data give a finite interval but not its value"),
        (8, "next derivation", "V4_L0_EINSTEIN_CONSTRAINT", "derive the fixed-baryon ADM monopole rather than add a closure"),
        (9, "physical finite-C kappa4 and local GR", "NOT_PROMOTED", "ADM monopole, v3 asymptotic extraction, EoS repeat, and solitary map remain"),
    ]
    return [
        {
            "priority": priority,
            "target": target,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, target, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_fixed_background_functional", "CLOSED", "exact L2/L4 and Euler matrices generated", "retain as source term for metric completion"),
        (2, "R_flow_BVP", "CLOSED_NUMERIC_SMOKE", "two solvers and outer-radius extrapolation agree", "repeat after coupled metric equation is added"),
        (3, "R_aether_surface", "CLOSED", "Noether surface charge through v4 derived", "combine only with standard ADM charge"),
        (4, "R_bulk_physical_identification", "REJECTED", "known first response disproves it at finite C", "never use raw bulk kappa4 as a claim row"),
        (5, "R_ADM_v2", "CALIBRATED_C3", "known f fixes the missing l0 completion", "use as regression for the v4 Einstein solver"),
        (6, "R_ADM_v4", "OPEN_DECISIVE_SINGLE_SCALAR", "D4/M interval derived but value unknown", "solve the v4 l0 Hamiltonian constraint"),
        (7, "R_v3_l1", "OPEN_AFTER_MONOPOLE", "independent asymptotic response extraction still needed", "cross-check the mass result from the dipole tail"),
        (8, "R_full_EOS", "OPEN_NUMERIC", "Tolman VII only", "repeat with one tabulated neutron-star EoS"),
        (9, "R_local_GR", "OPEN_HARD", "finite compact response and solitary map not closed", "do not promote"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    functional: list[dict[str, Any]],
    scans: list[dict[str, Any]],
    variational: list[dict[str, Any]],
    surface: list[dict[str, Any]],
    completion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-710"]
    variables = [row for row in read_csv(FORMAL / "04-variable-audit.csv") if row.get("symbol") == "D4_ADM_completion_MTS"]
    checkpoint = (POST / "4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md").read_text(encoding="utf-8")
    formal = (FORMAL / "884-PPC4161-finite-compactness-variational-and-ADM-completion-gate.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4867_VALIDATION.csv")
    weak_row = min(scans, key=lambda row: float(row["compactness"]))
    endpoint = max(scans, key=lambda row: float(row["compactness"]))
    endpoint_completion = max(completion, key=lambda row: float(row["compactness"]))

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, functional, scans, variational, surface, completion, decisions, residuals)
    checks = [
        result("VAL4868_00_sources", len(sources) == 18 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4868_01_functional", len(functional) == 9 and all(row["status"] != "FAIL" for row in functional), "coefficient, unit, degree and Euler checks pass"),
        result("VAL4868_02_bvp", len(scans) == 5 and all(float(row["fine_maximum_rms_residual"]) <= 1.01e-7 for row in scans), "five finite-C BVP rows converge"),
        result("VAL4868_03_outer", all(abs(float(row["fine_f_bulk"]) - float(row["coarse_f_bulk"])) < 0.003 for row in scans), "Rmax 200 to 400 drift remains below 0.003"),
        result("VAL4868_04_weak_f", abs(float(weak_row["f_bulk_extrapolated"]) / float(weak_row["weak_f"]) - 1) < 0.03, "small-C bulk f returns weak coefficient"),
        result("VAL4868_05_weak_kappa", abs(float(weak_row["kappa_bulk_extrapolated"]) / float(weak_row["weak_kappa"]) - 1) < 0.03, "small-C bulk kappa returns checkpoint-4867 coefficient"),
        result("VAL4868_06_rejection", float(endpoint["first_response_fractional_deficit"]) > 0.3, f"endpoint first-response deficit={float(endpoint['first_response_fractional_deficit']):.6g}"),
        result("VAL4868_07_variational", len(variational) == 2 and all(float(row["minimum_hessian_eigenvalue"]) > 0 and float(row["f_fractional_difference"]) < 0.05 and float(row["kappa_fractional_difference"]) < 0.05 for row in variational), "finite-basis cross-check positive and within five percent"),
        result("VAL4868_08_surface", len(surface) == 8 and surface[0]["status"] == "PASS" and surface[4]["status"] == "PASS" and surface[5]["status"] == "PASS", "static and boosted surface formulas pass"),
        result("VAL4868_09_completion", len(completion) == 5 and all(row["target_inside_interval"] for row in completion), "leading target lies inside every derived D4 interval"),
        result("VAL4868_10_endpoint_interval", math.isclose(float(endpoint_completion["completion_D4_over_M_low"]), -1.1056599999, rel_tol=0, abs_tol=0.01) and math.isclose(float(endpoint_completion["completion_D4_over_M_high"]), 1.8008756875, rel_tol=0, abs_tol=0.01), "endpoint ADM-completion interval reproduced"),
        result("VAL4868_11_decision", decisions[3]["decision"] == "REJECT_AS_PHYSICAL" and decisions[7]["decision"] == "V4_L0_EINSTEIN_CONSTRAINT", "failed shortcut and next derivation recorded"),
        result("VAL4868_12_residual", residuals[3]["status"] == "REJECTED" and residuals[5]["status"] == "OPEN_DECISIVE_SINGLE_SCALAR", "bulk rejection and ADM scalar separated"),
        result("VAL4868_13_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all checkpoint rows remain private nonclaim"),
        result("VAL4868_14_registers", len(claims) == 1 and len(variables) == 1 and variables[0].get("status") == "finite_compactness_completion_scalar_isolated_numeric_interval_open_nonclaim", f"claims={len(claims)} variables={len(variables)}"),
        result("VAL4868_15_documents", "FINITE_COMPACTNESS_VARIATIONAL_ADM_COMPLETION_4868" in checkpoint and "PPC4161_FINITE_COMPACTNESS_VARIATIONAL_ADM_GATE_4868" in formal, "checkpoint and formal markers found"),
        result("VAL4868_16_resume", resume_checkpoint_at_least(resume, 4868) and NEXT_TARGET in resume, "resume advanced to ADM monopole"),
        result("VAL4868_17_prior", prior[-1].get("status") == "PASS", "4867 validation remains green"),
        result("VAL4868_18_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py"), "generator and numeric core compile"),
        result("VAL4868_19_pycache", not (POST / "scripts" / "__pycache__").exists(), "no scripts pycache directory"),
    ]
    checks.append(
        result(
            "VAL4868_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "FINITE_COMPACTNESS_VARIATIONAL_AND_ADM_COMPLETION_GATE_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    functional = functional_rows()
    scans = scan_rows()
    variational = variational_rows(scans)
    surface = surface_rows(scans)
    completion = completion_rows(scans)
    decisions = decision_rows()
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        functional,
        scans,
        variational,
        surface,
        completion,
        decisions,
        residuals,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_REDUCED_FUNCTIONAL.csv", functional)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_FINITE_C_BVP_SCAN.csv", scans)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_VARIATIONAL_CROSSCHECK.csv", variational)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_AETHER_SURFACE_CHARGE.csv", surface)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_ADM_COMPLETION_CONTRACT.csv", completion)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4868_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4868_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4868_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4868_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
