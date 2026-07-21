from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, c, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "nonlocal_form_factors" / "4927"
SCRIPTS = POST / "scripts"

MARKER = "MTS_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927"
FORMAL_MARKER = "PPC4161_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927"
VALIDATION_MARKER = "MTS_MOTION_NORMALIZATION_COVARIANCE_VALIDATION_4927"
RESEARCH = SCRIPTS / "Y5_R2FR_4927_motion_normalization_covariance_residue.py"
CHECKPOINT = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
FORMAL_NOTE = FORMAL / "943-PPC4161-motion-normalization-covariance-residue-and-all-mass-loop-gate.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
NEXT_TARGET = "4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4927_COVARIANCE_DIMENSION_AUDIT.csv",
    "P8_Y5_R2FR_4927_FIELD_REDEFINITION_ORBIT.csv",
    "P8_Y5_R2FR_4927_INVARIANT_JACOBIAN.csv",
    "P8_Y5_R2FR_4927_STRESS_RESIDUE_CANCELLATION.csv",
    "P8_Y5_R2FR_4927_EH_MATCHING_IDENTIFIABILITY.csv",
    "P8_Y5_R2FR_4927_WEYL_FORM_FACTOR_BETA.csv",
    "P8_Y5_R2FR_4927_SCALAR_FORM_FACTOR_SCAN.csv",
    "P8_Y5_R2FR_4927_CROSS_ARENA_TRANSFER.csv",
    "P8_Y5_R2FR_4927_MOTION_MASS_REGIME_GATE.csv",
    "P8_Y5_R2FR_4927_NORMALIZATION_DECISION.csv",
    "P8_Y5_R2FR_4927_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4927_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "massive-scalar-nonlocal-form-factors-v3.pdf": "7fa6c9d5e22429b80e091e63fefb8ec578023f65dffa5200d062089749d52ec6",
    SOURCE / "2003.04503v3-source.tar": "268830a2b76dfaa2f075a45d4751f55d81f7be262bea0e884fd8ae166a3985e1",
    SOURCE / "matter-form-factors-decoupling-4D-v2.pdf": "e26accddfbc861c4379c291650f722912c32dd99f3d0c8738d5344b9edb89c4b",
    SOURCE / "1812.00460v2-source.tar": "355c7b031d397cc9c4546fb42bab2e338dbecab93b794eb92a50b4182048128e",
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
        "VAL4927_00_compile",
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
        "VAL4927_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4927_MOTION_NORMALIZATION_COVARIANCE_PASS" in run.stdout,
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4927_02_outputs",
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
        "VAL4927_03_csv_shape",
        "all evidence CSVs parse without malformed rows",
        "no malformed rows",
        ";".join(parse_failures) or "no malformed rows",
        not parse_failures,
    )

    all_evidence_rows = [row for rows in parsed.values() for row in rows]
    marker_failures = [
        row for row in all_evidence_rows if row.get("checkpoint_marker") != MARKER
    ]
    add_check(
        checks,
        "VAL4927_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable_rows = [row for row in all_evidence_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4927_05_nonclaim",
        "all checkpoint evidence remains private nonclaim",
        0,
        len(claimable_rows),
        not claimable_rows,
    )
    placeholder_rows = [
        row
        for row in all_evidence_rows
        if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4927_06_no_placeholders",
        "no generated row contains a MISSING placeholder token",
        0,
        len(placeholder_rows),
        not placeholder_rows,
    )

    hash_failures = [
        path.name
        for path, expected_hash in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected_hash
    ]
    add_check(
        checks,
        "VAL4927_07_source_hashes",
        "all four form-factor source files match locked SHA-256 values",
        0,
        len(hash_failures),
        not hash_failures,
    )

    source_rows = parsed["P8_Y5_R2FR_4927_SOURCE_REGISTER.csv"]
    source_failures = [row["source_id"] for row in source_rows if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4927_08_source_register",
        "binary hashes local derivation markers registers and primary URLs are verified",
        "29 rows; zero failures",
        f"{len(source_rows)} rows; failures={source_failures}",
        len(source_rows) == 29 and not source_failures,
    )

    covariance_rows = parsed["P8_Y5_R2FR_4927_COVARIANCE_DIMENSION_AUDIT.csv"]
    covariance = {row["audit_id"]: row for row in covariance_rows}
    add_check(
        checks,
        "VAL4927_09_covariance_dimensions",
        "old and canonical covariance coefficients have dimensions minus five and minus four",
        "B_old=-5; B_psi=-4; both metric terms dimension 0",
        f"old={covariance['CDIM4927_03_correct_old']['coefficient_mass_dimension']}; canonical={covariance['CDIM4927_04_correct_canonical']['coefficient_mass_dimension']}",
        len(covariance_rows) == 7
        and covariance["CDIM4927_00_core_raw"]["resulting_metric_term_dimension"] == "5"
        and covariance["CDIM4927_01_4872_old"]["resulting_metric_term_dimension"] == "3"
        and covariance["CDIM4927_02_4872_canonical"]["resulting_metric_term_dimension"] == "2"
        and covariance["CDIM4927_03_correct_old"]["coefficient_mass_dimension"] == "-5"
        and covariance["CDIM4927_03_correct_old"]["resulting_metric_term_dimension"] == "0"
        and covariance["CDIM4927_04_correct_canonical"]["coefficient_mass_dimension"] == "-4"
        and covariance["CDIM4927_04_correct_canonical"]["resulting_metric_term_dimension"] == "0",
    )

    orbit_rows = parsed["P8_Y5_R2FR_4927_FIELD_REDEFINITION_ORBIT.csv"]
    max_g_error = max(float(row["g_psi_error"]) for row in orbit_rows)
    max_b_error = max(float(row["B_psi_error"]) for row in orbit_rows)
    m_values = [float(row["M_N_prime"]) for row in orbit_rows]
    add_check(
        checks,
        "VAL4927_10_field_orbit",
        "five old-field coordinate choices preserve both physical invariants",
        "errors below 1e-14 across eight M_N orders",
        f"rows={len(orbit_rows)}; g_error={max_g_error}; B_error={max_b_error}; span={max(m_values)/min(m_values)}",
        len(orbit_rows) == 5
        and max_g_error < 1.0e-14
        and max_b_error < 1.0e-14
        and math.isclose(max(m_values) / min(m_values), 1.0e8, rel_tol=1.0e-14),
    )

    jacobian_rows = parsed["P8_Y5_R2FR_4927_INVARIANT_JACOBIAN.csv"]
    jacobian = {row["row_id"]: row for row in jacobian_rows}
    null_vectors = {row["null_vector"] for row in jacobian_rows[1:]}
    add_check(
        checks,
        "VAL4927_11_identifiability_rank",
        "joint invariant map has rank three nullity three and the stated null basis",
        "rank=3 nullity=3 with three exact null vectors",
        f"rank={jacobian['IJ4927_rank']['rank']}; nullity={jacobian['IJ4927_rank']['nullity']}; vectors={sorted(null_vectors)}",
        len(jacobian_rows) == 4
        and jacobian["IJ4927_rank"]["rank"] == "3"
        and jacobian["IJ4927_rank"]["nullity"] == "3"
        and null_vectors
        == {"3;1;-3;0;0;0", "0;0;0;1;-1;0", "0;0;0;1;0;-1"}
        and all(float(row["null_error"]) < 1.0e-14 for row in jacobian_rows),
    )

    stress_rows = parsed["P8_Y5_R2FR_4927_STRESS_RESIDUE_CANCELLATION.csv"]
    max_residue_error = max(abs(float(row["normalization_residue"]) - 1.0) for row in stress_rows)
    add_check(
        checks,
        "VAL4927_12_stress_residue",
        "M_N cancels for n=2 3 4 stress loops over three normalization scales",
        "nine rows with unit residue",
        f"rows={len(stress_rows)}; max_error={max_residue_error}",
        len(stress_rows) == 9
        and {row["stress_insertions"] for row in stress_rows} == {"2", "3", "4"}
        and max_residue_error < 3.0e-15,
    )

    eh_rows = parsed["P8_Y5_R2FR_4927_EH_MATCHING_IDENTIFIABILITY.csv"]
    add_check(
        checks,
        "VAL4927_13_EH_no_coordinate_fix",
        "no stress EH composite or cutoff route fixes the old coordinate normalization",
        "all C_N_fixed false; invariant parameterization selected",
        f"rows={len(eh_rows)}; fixed={sum(as_bool(row['C_N_fixed']) for row in eh_rows)}",
        len(eh_rows) == 6
        and all(not as_bool(row["C_N_fixed"]) for row in eh_rows)
        and eh_rows[-1]["status"] == "SELECTED_INVARIANT_PARAMETERIZATION",
    )

    beta_rows = parsed["P8_Y5_R2FR_4927_WEYL_FORM_FACTOR_BETA.csv"]
    beta_values = [float(row["beta_exact_dkW_dlnu"]) for row in beta_rows]
    max_series_error = max(float(row["series_error"]) for row in beta_rows)
    endpoint_sum = (1.0 / 12.0) * (1.0 / 5.0)
    add_check(
        checks,
        "VAL4927_14_beta_theorem",
        "exact Weyl beta samples obey the negative-series endpoint theorem",
        "-1/60 <= beta <= 0 and endpoint sum=1/60",
        f"range=[{min(beta_values)},{max(beta_values)}]; endpoint={endpoint_sum}; series_error={max_series_error}",
        len(beta_rows) == 6
        and all(-1.0 / 60.0 <= value <= 0.0 for value in beta_values)
        and all(beta_values[index] > beta_values[index + 1] for index in range(len(beta_values) - 1))
        and math.isclose(endpoint_sum, 1.0 / 60.0, rel_tol=0.0, abs_tol=1.0e-18)
        and max_series_error < 1.0e-15,
    )

    scan_rows = parsed["P8_Y5_R2FR_4927_SCALAR_FORM_FACTOR_SCAN.csv"]
    pair_counts: dict[str, int] = {}
    for row in scan_rows:
        pair_counts[row["pair_id"]] = pair_counts.get(row["pair_id"], 0) + 1
    max_ratio = max(float(row["bound_ratio"]) for row in scan_rows)
    mass_ratios = [float(row["mass_over_q_high"]) for row in scan_rows]
    add_check(
        checks,
        "VAL4927_15_exact_scan_shape",
        "five arena pairs each scan 81 masses from 1e-20 through 1e20",
        "405 rows; 81 per pair; exact endpoints",
        f"rows={len(scan_rows)}; counts={pair_counts}; endpoints=({min(mass_ratios)},{max(mass_ratios)})",
        len(scan_rows) == 405
        and len(pair_counts) == 5
        and set(pair_counts.values()) == {81}
        and math.isclose(min(mass_ratios), 1.0e-20, rel_tol=1.0e-14)
        and math.isclose(max(mass_ratios), 1.0e20, rel_tol=1.0e-14),
    )
    add_check(
        checks,
        "VAL4927_16_exact_scan_bound",
        "every exact massive form-factor difference lies below the integrated beta bound",
        "max bound ratio <= 1+3e-13 and all rows pass",
        max_ratio,
        max_ratio <= 1.0 + 3.0e-13
        and all(as_bool(row["passed"]) for row in scan_rows)
        and {row["mass_regime"] for row in scan_rows} == {"light", "crossover", "heavy"},
    )

    transfer_rows = parsed["P8_Y5_R2FR_4927_CROSS_ARENA_TRANSFER.csv"]
    electron_volt_joule = physical_constants["electron volt"][0]
    reduced_planck_energy_eV = math.sqrt(hbar * c**5 / (8.0 * math.pi * G)) / electron_volt_joule
    transfer_formula_errors: list[float] = []
    for row in transfer_rows:
        q_high = float(row["q_high_eV"])
        logarithm = float(row["ln_q_high_over_q_low"])
        expected = q_high**2 * logarithm / (480.0 * math.pi**2 * reduced_planck_energy_eV**2)
        actual = float(row["spin2_transfer_per_real_scalar"])
        transfer_formula_errors.append(abs(actual - expected) / expected)
    max_transfer = max(
        max(
            float(row["spin2_transfer_per_real_scalar"]),
            float(row["spin0_minimal_massless_envelope_per_real_scalar"]),
            float(row["unit_weight_Newton_running_envelope_per_real_scalar"]),
        )
        for row in transfer_rows
    )
    add_check(
        checks,
        "VAL4927_17_transfer_formula",
        "spin-two transfers independently reproduce the reduced-Planck formula",
        "five rows; relative errors below 2e-14",
        f"rows={len(transfer_rows)}; max_error={max(transfer_formula_errors)}",
        len(transfer_rows) == 5 and max(transfer_formula_errors) < 2.0e-14,
    )
    add_check(
        checks,
        "VAL4927_18_local_envelope",
        "all one-scalar spin-two spin-zero and Newton envelopes are below 1e-30",
        2.5057690980704453e-39,
        max_transfer,
        math.isclose(max_transfer, 2.5057690980704453e-39, rel_tol=2.0e-14)
        and max_transfer < 1.0e-30,
    )

    regime_rows = parsed["P8_Y5_R2FR_4927_MOTION_MASS_REGIME_GATE.csv"]
    add_check(
        checks,
        "VAL4927_19_mass_regimes",
        "heavy crossover light and all-mass domains are explicitly separated",
        "four passing regimes and no 1/m^2 continuation to zero",
        [row["regime"] for row in regime_rows],
        {row["regime"] for row in regime_rows}
        == {"heavy", "crossover", "light_or_massless", "all"}
        and all(as_bool(row["passed"]) for row in regime_rows)
        and "never continue 1/m^2 to zero mass"
        in next(row["forbidden_extrapolation"] for row in regime_rows if row["regime"] == "light_or_massless"),
    )

    normalization_rows = parsed["P8_Y5_R2FR_4927_NORMALIZATION_DECISION.csv"]
    normalization = {row["object"]: row for row in normalization_rows}
    add_check(
        checks,
        "VAL4927_20_normalization_decision",
        "C_N is removed while invariant scalar and covariance quantities remain physical",
        "C_N redundant and motion-loop local safety all-mass",
        f"CN={normalization['C_N=M_N/M_Pl']['new_status']}; loop={normalization['motion-loop local GR safety']['new_status']}",
        normalization["C_N=M_N/M_Pl"]["new_status"] == "redundant old-field coordinate"
        and normalization["motion-loop local GR safety"]["new_status"]
        == "all-mass domain covered for finite pole multiplicity",
    )

    gate_rows = parsed["P8_Y5_R2FR_4927_GATE_DECISION.csv"]
    gate = {row["gate"]: row for row in gate_rows}
    add_check(
        checks,
        "VAL4927_21_gate_state",
        "weak GR Newton Maxwell survives while compact and full claims stay unpromoted",
        "weak retained; compact/full false; next target 4928 C3 flow",
        f"weak={gate['weak_GR_Newton_Maxwell']['status']}; compact={gate['compact_GR']['status']}; full={gate['full_MTS_to_GR']['status']}; next={gate['next_target']['decision']}",
        gate["weak_GR_Newton_Maxwell"]["status"] == "RETAINED"
        and gate["compact_GR"]["status"] == "NOT_PROMOTED_TOTAL_WILSON_REMAINDER_OPEN"
        and gate["full_MTS_to_GR"]["status"] == "NOT_PROMOTED"
        and gate["next_target"]["decision"] == NEXT_TARGET
        and all(not as_bool(row["claim_promoted"]) for row in gate_rows),
    )

    required_markers = {
        CHECKPOINT: MARKER,
        FORMAL_NOTE: FORMAL_MARKER,
        SOURCE / "PROVENANCE.md": "MTS_MOTION_NORMALIZATION_FORM_FACTOR_PROVENANCE_4927",
        RESUME: NEXT_TARGET,
        FORMAL / "02-claims-register.csv": "L-769",
        FORMAL / "04-variable-audit.csv": "MotionNormalizationStatus4927_MTS",
        FORMAL / "05-equation-register.md": "1.220 Motion-coordinate redundancy and all-mass scalar loop bound",
        FORMAL / "06-consistency-red-team.md": "171. A field-coordinate normalization is not a physical coupling",
        FORMAL / "07-unification-spine.md": "PPC4161 checkpoint 4927",
    }
    marker_problems = [
        path.name
        for path, marker in required_markers.items()
        if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4927_22_registers",
        "checkpoint formal note provenance resume and five registers carry their markers",
        0,
        len(marker_problems),
        not marker_problems,
    )

    required_variables = {
        "OldCovarianceCoefficient4927_MTS",
        "CanonicalCovarianceCoefficient4927_MTS",
        "MotionFieldCoordinateOrbit4927_MTS",
        "MotionInvariantCoupling4927_MTS",
        "MotionStressResidue4927_MTS",
        "MotionEHIdentifiability4927_MTS",
        "MassiveScalarWeylFormFactor4927_MTS",
        "WeylFormFactorBetaBound4927_MTS",
        "MotionAllMassLoopGate4927_MTS",
        "MotionNormalizationStatus4927_MTS",
        "VacuumGRMotionLoopStatus4927_MTS",
    }
    variable_symbols = {row["symbol"] for row in read_csv(FORMAL / "04-variable-audit.csv")}
    add_check(
        checks,
        "VAL4927_23_variables",
        "all eleven canonical checkpoint variables are registered",
        11,
        len(required_variables & variable_symbols),
        required_variables <= variable_symbols,
    )

    pycache_paths = list(SCRIPTS.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4927_24_pycache",
        "scripts tree contains no Python bytecode cache directories",
        0,
        len(pycache_paths),
        not pycache_paths,
    )

    all_passed = all(as_bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4927_OVERALL",
        "checkpoint 4927 derivation evidence and claim-discipline validation",
        "all checks pass",
        f"{sum(as_bool(row['passed']) for row in checks)}/{len(checks)} pre-overall checks pass",
        all_passed,
    )
    write_csv(OUTPUT / "P8_Y5_BRR545_4927_VALIDATION.csv", checks)
    print(
        "P8_Y5_BRR545_4927_VALIDATION_PASS"
        if all_passed
        else "P8_Y5_BRR545_4927_VALIDATION_FAIL"
    )
    print(f"checks_passed={sum(as_bool(row['passed']) for row in checks)}/{len(checks)}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
