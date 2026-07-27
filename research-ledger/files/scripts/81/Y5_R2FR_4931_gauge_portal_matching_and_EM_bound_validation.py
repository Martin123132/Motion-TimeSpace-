from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, alpha, c, hbar, m_e, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4931"
SCRIPTS = POST / "scripts"

MARKER = "MTS_GAUGE_CURVATURE_PORTAL_MATCHING_EM_BOUND_4931"
VALIDATION_MARKER = "MTS_GAUGE_CURVATURE_PORTAL_MATCHING_EM_BOUND_VALIDATION_4931"
FORMAL_MARKER = "PPC4161_GAUGE_PORTAL_MATCHING_EM_BOUND_4931"
NEXT_TARGET = "4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md"

RESEARCH = SCRIPTS / "Y5_R2FR_4931_gauge_portal_matching_and_EM_bound.py"
CHECKPOINT = POST / "4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md"
FORMAL_NOTE = FORMAL / "947-PPC4161-gauge-portal-matching-and-EM-Wilson-bound.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
VALIDATION_OUTPUT = OUTPUT / "P8_Y5_BRR545_4931_VALIDATION.csv"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4931_PORTAL_BETA_BOUNDARY.csv",
    "P8_Y5_R2FR_4931_DIRAC_THRESHOLD_MATCHING.csv",
    "P8_Y5_R2FR_4931_ELECTROWEAK_PORTAL_PROJECTION.csv",
    "P8_Y5_R2FR_4931_CHARGED_LEPTON_THRESHOLDS.csv",
    "P8_Y5_R2FR_4931_PHOTON_CHARACTERISTIC.csv",
    "P8_Y5_R2FR_4931_SCHWARZSCHILD_POLARIZATION.csv",
    "P8_Y5_R2FR_4931_QED_ARENA_CONTROL.csv",
    "P8_Y5_R2FR_4931_OBSERVATIONAL_BOUNDS.csv",
    "P8_Y5_R2FR_4931_WILSON_BOUND_PROJECTION.csv",
    "P8_Y5_R2FR_4931_PARENT_MATCHING_LEDGER.csv",
    "P8_Y5_R2FR_4931_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4931_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "0306021.pdf": "051bb00b53a2405c5fe9e60ce8caa3fb53569fc521c3c160056a9ddc63308dd9",
    SOURCE / "0306021-source.tar": "4bb0cf7e021fd642f562c779b409e1d26cc42fc8aeae605fc1514bca565ba8b1",
    SOURCE / "0812.4849.pdf": "c0ba0b57f459cd03fa9ec36234e58e64acd214ab570d577806307b01cbf66071",
    SOURCE / "0812.4849-source.tar": "d094ed32127888dd0052e8341d43c83407dbe24c8f2813e3c5f4c49149781438",
    SOURCE / "1505.01844.pdf": "13ea6e7d9250257f72b8f3ea82c8b4c4f83c295998367164a5f2fcda1f071e1f",
    SOURCE / "1505.01844-source.tar": "74bb7123a648f87b36783253d54b51a17924e82e333d1ed421d4381a9aaac657",
    SOURCE / "1609.00723.pdf": "8f2c3437aaf3ab741f4ddf5139042859f802dff5e753a54d8401406faa80669e",
    SOURCE / "1609.00723-source.tar": "828b1655d88e414cd23f05684287a0ffa6d8c44ab03af4002a2b2cb0cc3dca26",
    SOURCE / "2110.06056.pdf": "08e6cad354b13c86683fde298338fb4738c28e5059d2dc3a3ebea631c20d1ba0",
    SOURCE / "2110.06056-source.tar": "22d1f0ead77c2a2bfb305968be0cfded94846c680ed55fab25c1994bba6ad421",
    SOURCE / "2303.10203.pdf": "db39ae9337d4fcb74108626a0fc04f2116eb5e9e6573d6d58b55d06366bf09cb",
    SOURCE / "2303.10203-source.tar": "0772442c8d3357750fd47310c193eb0a50ae92a670a7ddcbc6b99a1453917765",
    SOURCE / "2505.21431.pdf": "cf0cdec154d7ad74ada903e88f76d1fa90f2f73a14711eee11900a714ad3e192",
    SOURCE / "2505.21431-source.tar": "64e80415d379269b83eaf2bb94e71cdcfcd19210369a9bfbd8b6cda7c9ae276f",
}

SOLAR_MASS_KG = 1.988409870698051e30
SOLAR_RADIUS_M = 6.957e8


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


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


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


def dirac_threshold(charge: float, mass_kg: float) -> float:
    return -(charge**2) * alpha * (hbar / (mass_kg * c)) ** 2 / (360.0 * math.pi)


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
        "VAL4931_00_compile",
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
        "VAL4931_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}; stderr={run.stderr.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4931_GAUGE_PORTAL_MATCHING_EM_BOUND_PASS" in run.stdout
        and not run.stderr.strip(),
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4931_02_outputs",
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
        "VAL4931_03_csv_shape",
        "all evidence CSVs parse without malformed rows",
        "no malformed rows",
        ";".join(parse_failures) or "no malformed rows",
        not parse_failures,
    )

    all_rows = [row for rows in parsed.values() for row in rows]
    marker_failures = [row for row in all_rows if row.get("checkpoint_marker") != MARKER]
    add_check(
        checks,
        "VAL4931_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable = [row for row in all_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4931_05_nonclaim",
        "all checkpoint evidence remains private nonclaim",
        0,
        len(claimable),
        not claimable,
    )
    placeholders = [
        row for row in all_rows if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4931_06_no_placeholder_tokens",
        "open physics is named rather than represented by placeholder tokens",
        0,
        len(placeholders),
        not placeholders,
    )
    failed_rows = [row for row in all_rows if not as_bool(row.get("passed", True))]
    add_check(
        checks,
        "VAL4931_07_row_pass",
        "all generated derivation and source rows pass their internal contracts",
        0,
        len(failed_rows),
        not failed_rows,
    )

    hash_failures = [
        path.name
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    ]
    add_check(
        checks,
        "VAL4931_08_hashes",
        "all seven PDF and source-archive pairs retain locked SHA256 hashes",
        0,
        len(hash_failures),
        not hash_failures,
    )

    sources = parsed["P8_Y5_R2FR_4931_SOURCE_REGISTER.csv"]
    add_check(
        checks,
        "VAL4931_09_source_register",
        "source register verifies binaries text markers and primary URLs",
        "36 passed source rows",
        f"rows={len(sources)}; failed={sum(not as_bool(row['passed']) for row in sources)}",
        len(sources) == 36 and all(as_bool(row["passed"]) for row in sources),
    )

    beta = {row["beta_id"]: row for row in parsed["P8_Y5_R2FR_4931_PORTAL_BETA_BOUNDARY.csv"]}
    add_check(
        checks,
        "VAL4931_10_beta_boundary",
        "massless U1 and Yang-Mills additive sources vanish while full MTS remains open",
        "two additive zeros and one open MTS row",
        ";".join(f"{key}:{row['status']}" for key, row in beta.items()),
        len(beta) == 6
        and math.isclose(float(beta["BETA4931_01_Einstein_Maxwell_additive"]["additive_source_at_u_zero"]), 0.0)
        and math.isclose(float(beta["BETA4931_02_Einstein_Yang_Mills_additive"]["additive_source_at_u_zero"]), 0.0)
        and not as_bool(beta["BETA4931_01_Einstein_Maxwell_additive"]["multiplicative_gamma_derived"])
        and beta["BETA4931_05_full_MTS"]["status"] == "NONPERTURBATIVE_FIXED_POINT_OPEN",
    )
    canonical = beta["BETA4931_03_canonical_Gaussian_estimate"]
    add_check(
        checks,
        "VAL4931_11_canonical_fixed_point",
        "strict canonical comparator has u*=0 and theta=-2 with explicit scope guard",
        "0 and -2",
        f"u={canonical['fixed_point']}; theta={canonical['critical_exponent']}; scope={canonical['scope']}",
        math.isclose(float(canonical["fixed_point"]), 0.0)
        and math.isclose(float(canonical["critical_exponent"]), -2.0)
        and "comparator" in canonical["scope"],
    )

    matching = {
        row["matching_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_DIRAC_THRESHOLD_MATCHING.csv"]
    }
    add_check(
        checks,
        "VAL4931_12_matching_normalization",
        "GRSMEFT and independent QED sources give the same canonical magnitude",
        "1/[90(4pi)^2m^2] magnitude",
        f"primary={matching['MATCH4931_01_QED']['canonical_result']}; cross={matching['MATCH4931_02_independent_magnitude']['canonical_result']}",
        len(matching) == 5
        and "alpha_EM/[360pi]" in matching["MATCH4931_01_QED"]["canonical_result"]
        and "alpha_EM/[360pi]" in matching["MATCH4931_02_independent_magnitude"]["canonical_result"]
        and "magnitude only" in matching["MATCH4931_02_independent_magnitude"]["sign_policy"],
    )

    leptons = {
        row["particle"]: row
        for row in parsed["P8_Y5_R2FR_4931_CHARGED_LEPTON_THRESHOLDS.csv"]
    }
    expected_e = dirac_threshold(1.0, m_e)
    expected_mu = dirac_threshold(1.0, physical_constants["muon mass"][0])
    expected_tau = dirac_threshold(1.0, physical_constants["tau mass"][0])
    expected_sum = expected_e + expected_mu + expected_tau
    add_check(
        checks,
        "VAL4931_13_lepton_thresholds",
        "independent constants calculation reproduces electron muon tau and subtotal",
        f"electron={expected_e}; sum={expected_sum}",
        f"electron={leptons['electron']['Delta_c_gamma_m2']}; sum={leptons['e+mu+tau free-lepton sum']['Delta_c_gamma_m2']}",
        len(leptons) == 4
        and math.isclose(float(leptons["electron"]["Delta_c_gamma_m2"]), expected_e, rel_tol=1.0e-14)
        and math.isclose(float(leptons["muon"]["Delta_c_gamma_m2"]), expected_mu, rel_tol=1.0e-14)
        and math.isclose(float(leptons["tau"]["Delta_c_gamma_m2"]), expected_tau, rel_tol=1.0e-14)
        and math.isclose(float(leptons["e+mu+tau free-lepton sum"]["Delta_c_gamma_m2"]), expected_sum, rel_tol=1.0e-14)
        and all(not as_bool(row["full_SM_threshold"]) for row in leptons.values()),
    )

    ew = {
        row["projection_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_ELECTROWEAK_PORTAL_PROJECTION.csv"]
    }
    add_check(
        checks,
        "VAL4931_14_electroweak_projection",
        "photon Z AZ and gluon rows preserve one-combination identifiability",
        "five rows; no separate cB/cW determination",
        f"rows={len(ew)}; photon={ew['EW4931_00_photon']['coefficient']}",
        len(ew) == 5
        and "cos^2" in ew["EW4931_00_photon"]["coefficient"]
        and "c_W-c_B" in ew["EW4931_02_mixed"]["coefficient"]
        and all(not as_bool(row["individual_UV_coefficients_separated"]) for row in ew.values())
        and ew["EW4931_04_gluon"]["status"] == "NOT_CONSTRAINED_BY_THIS_CHECKPOINT",
    )

    characteristic = {
        row["characteristic_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_PHOTON_CHARACTERISTIC.csv"]
    }
    add_check(
        checks,
        "VAL4931_15_characteristic",
        "action excitation principal symbol and projected dispersion carry consistent factors",
        "-4 excitation; -8 symbol; +8 projection",
        ";".join(f"{key}:{row['equation']}" for key, row in characteristic.items()),
        len(characteristic) == 10
        and "-4 c_gamma" in characteristic["EM4931_01_excitation"]["equation"]
        and "-8 c_gamma" in characteristic["EM4931_03_principal_symbol"]["equation"]
        and "=8 c_gamma" in characteristic["EM4931_04_projected_dispersion"]["equation"]
        and "not |k|" in characteristic["EM4931_06_no_frequency_dispersion"]["equation"],
    )
    add_check(
        checks,
        "VAL4931_16_conservation",
        "current and total Hilbert-stress Ward identities are retained with the stress scope guard",
        "nabla J=0 and nabla T=-FJ",
        f"J={characteristic['EM4931_07_current_conservation']['equation']}; T={characteristic['EM4931_08_Hilbert_stress']['equation']}",
        "=0" in characteristic["EM4931_07_current_conservation"]["equation"]
        and "=-F" in characteristic["EM4931_08_Hilbert_stress"]["equation"]
        and "full Hilbert stress" in characteristic["EM4931_09_Poynting_constitutive_bound"]["exactness"],
    )

    schwarzschild = {
        row["observable_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_SCHWARZSCHILD_POLARIZATION.csv"]
    }
    add_check(
        checks,
        "VAL4931_17_schwarzschild",
        "Schwarzschild dispersion optical factors and validity interval are source mapped",
        "seven rows with +/-12 reciprocal rho and control-only interval",
        ";".join(f"{key}:{row['formula']}" for key, row in schwarzschild.items()),
        len(schwarzschild) == 7
        and "+/-12" in schwarzschild["SCH4931_00_dispersion"]["formula"]
        and "12|c_gamma|" in schwarzschild["SCH4931_01_velocity_split"]["formula"]
        and "=1/rho_l" in schwarzschild["SCH4931_04_PPM_metric"]["formula"]
        and schwarzschild["SCH4931_05_horizon_validity"]["status"] == "VALIDITY_CONDITION_NOT_DATA"
        and schwarzschild["SCH4931_06_Sultana_Dyer_control"]["status"] == "CONTROL_ONLY_NOT_BOUND",
    )

    arenas = {
        row["arena"]: row for row in parsed["P8_Y5_R2FR_4931_QED_ARENA_CONTROL.csv"]
    }
    mass_geom_sun = G * SOLAR_MASS_KG / c**2
    expected_solar_split = 12.0 * abs(expected_sum) * mass_geom_sun / SOLAR_RADIUS_M**3
    add_check(
        checks,
        "VAL4931_18_arena_control",
        "independent solar calculation reproduces the QED polarization control and all four are tiny",
        expected_solar_split,
        arenas["solar_limb"]["leading_abs_polarization_velocity_split"],
        len(arenas) == 4
        and math.isclose(
            float(arenas["solar_limb"]["leading_abs_polarization_velocity_split"]),
            expected_solar_split,
            rel_tol=1.0e-14,
        )
        and all(float(row["leading_abs_polarization_velocity_split"]) < 1.0e-35 for row in arenas.values())
        and all(not as_bool(row["empirical_test"]) for row in arenas.values()),
    )

    bounds = {
        row["bound_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_OBSERVATIONAL_BOUNDS.csv"]
    }
    add_check(
        checks,
        "VAL4931_19_bound_units",
        "PSR and M87 source quantities convert to square metres correctly",
        "PSR 6e6; M87 2.85156e25",
        f"PSR={bounds['BOUND4931_03_PSR_original']['abs_or_upper_bound_m2']}; M87={bounds['BOUND4931_05_M87_case']['abs_or_upper_bound_m2']}",
        len(bounds) == 6
        and math.isclose(float(bounds["BOUND4931_03_PSR_original"]["abs_or_upper_bound_m2"]), 6.0e6)
        and math.isclose(float(bounds["BOUND4931_04_PSR_secondary_abs"]["sqrt_bound_m"]), 2450.0)
        and math.isclose(float(bounds["BOUND4931_05_M87_case"]["abs_or_upper_bound_m2"]), 2.85156e25),
    )
    add_check(
        checks,
        "VAL4931_20_bound_scope",
        "one-sided original PSR and conditional two-sided secondary/M87 rows remain distinct",
        "PSR false; secondary and M87 true",
        f"PSR={bounds['BOUND4931_03_PSR_original']['two_sided_absolute']}; secondary={bounds['BOUND4931_04_PSR_secondary_abs']['two_sided_absolute']}; M87={bounds['BOUND4931_05_M87_case']['two_sided_absolute']}",
        not as_bool(bounds["BOUND4931_03_PSR_original"]["two_sided_absolute"])
        and as_bool(bounds["BOUND4931_04_PSR_secondary_abs"]["two_sided_absolute"])
        and as_bool(bounds["BOUND4931_05_M87_case"]["two_sided_absolute"])
        and bounds["BOUND4931_03_PSR_original"]["status"]
        == "STRONGEST_LEGACY_POSITIVE_SIDE_CONDITIONAL_BOUND"
        and bounds["BOUND4931_04_PSR_secondary_abs"]["status"]
        == "STRONG_SECONDARY_ABSOLUTE_RECAST_NOT_PRIMARY_LIKELIHOOD"
        and bounds["BOUND4931_05_M87_case"]["status"]
        == "MODERN_TWO_SIDED_CONDITIONAL_CASE_BOUND"
        and all(row["assumptions"].strip() for row in bounds.values()),
    )
    add_check(
        checks,
        "VAL4931_21_radar_discrepancy",
        "both conflicting radar values are retained and quarantined",
        "3.9e15 and 1.1e16 m^2; consistency false",
        f"intro={bounds['BOUND4931_01_radar_intro']['abs_or_upper_bound_m2']}; detailed={bounds['BOUND4931_02_radar_detailed']['abs_or_upper_bound_m2']}",
        math.isclose(float(bounds["BOUND4931_01_radar_intro"]["abs_or_upper_bound_m2"]), 3.9e15)
        and math.isclose(float(bounds["BOUND4931_02_radar_detailed"]["abs_or_upper_bound_m2"]), 1.1e16)
        and not as_bool(bounds["BOUND4931_01_radar_intro"]["source_internal_consistent"])
        and not as_bool(bounds["BOUND4931_02_radar_detailed"]["source_internal_consistent"]),
    )

    projections = {
        row["projection_id"]: row
        for row in parsed["P8_Y5_R2FR_4931_WILSON_BOUND_PROJECTION.csv"]
    }
    psr_ratio = abs(expected_sum) / 6.0e6
    add_check(
        checks,
        "VAL4931_22_wilson_projection",
        "known QED ratios and one-sided/two-sided residual formulas are independently consistent",
        psr_ratio,
        projections["PROJ_BOUND4931_03_PSR_original"]["known_to_bound_ratio"],
        len(projections) == 4
        and math.isclose(
            float(projections["PROJ_BOUND4931_03_PSR_original"]["known_to_bound_ratio"]),
            psr_ratio,
            rel_tol=1.0e-14,
        )
        and "<B-c_free_leptons" in projections["PROJ_BOUND4931_03_PSR_original"]["residual_formula"]
        and "<=B+|c_free_leptons|" in projections["PROJ_BOUND4931_05_M87_case"]["residual_formula"]
        and all(not as_bool(row["robust_general_bound"]) for row in projections.values()),
    )

    parent = {
        row["component"]: row
        for row in parsed["P8_Y5_R2FR_4931_PARENT_MATCHING_LEDGER.csv"]
    }
    add_check(
        checks,
        "VAL4931_23_parent_ledger",
        "parent QCD EW and conditional-minimal branches remain separated from the numeric lepton subtotal",
        "six components and only lepton subtotal included",
        f"rows={len(parent)}; included={[key for key,row in parent.items() if as_bool(row['included_in_4931_numeric_total'])]}",
        len(parent) == 6
        and as_bool(parent["c_gamma_free_leptons"]["included_in_4931_numeric_total"])
        and not as_bool(parent["c_gamma_parent(mu_match)"]["included_in_4931_numeric_total"])
        and not as_bool(parent["c_gamma_QCD_hadronic"]["included_in_4931_numeric_total"])
        and not as_bool(parent["c_gamma_EW_spin1"]["included_in_4931_numeric_total"])
        and not as_bool(parent["conditional_minimal_threshold_branch"]["included_in_4931_numeric_total"]),
    )

    gates = {
        row["gate"]: row for row in parsed["P8_Y5_R2FR_4931_GATE_DECISION.csv"]
    }
    add_check(
        checks,
        "VAL4931_24_decision",
        "final gate records perturbative progress retains weak GR and selects 4932 without promotion",
        "additive closed; full fixed point open; compact not promoted; next 4932",
        f"add={gates['one_loop_massless_additive_beta']['status']}; full={gates['full_MTS_portal_fixed_point']['status']}; compact={gates['compact_and_full_MTS_to_GR']['status']}; next={gates['next_target']['decision']}",
        gates["one_loop_massless_additive_beta"]["status"] == "CLOSED_IN_ON_SHELL_PERTURBATIVE_BASIS"
        and gates["full_MTS_portal_fixed_point"]["status"] == "OPEN_BUT_NARROWED"
        and gates["weak_GR_Newton"]["status"] == "RETAINED"
        and gates["compact_and_full_MTS_to_GR"]["status"] == "NOT_PROMOTED"
        and gates["next_target"]["decision"] == NEXT_TARGET
        and all(not as_bool(row["claim_promoted"]) for row in gates.values()),
    )

    marker_paths = [
        (CHECKPOINT, MARKER),
        (FORMAL_NOTE, FORMAL_MARKER),
        (PROVENANCE, "MTS_GAUGE_CURVATURE_PORTAL_PROVENANCE_4931"),
        (CLAIMS, "L-773"),
        (VARIABLES, "GaugePortalStatus4931_MTS"),
        (EQUATIONS, "1.224 Gauge-curvature portal matching and electromagnetic Wilson boundary"),
        (RED_TEAM, "175. A one-loop additive zero is not an all-orders portal prediction"),
        (SPINE, "PPC4161 checkpoint 4931"),
        (RESUME, NEXT_TARGET),
    ]
    marker_path_failures = [
        path.name for path, marker in marker_paths if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4931_25_registers",
        "checkpoint provenance formal note registers spine and resume markers exist",
        0,
        len(marker_path_failures),
        not marker_path_failures,
    )

    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    add_check(
        checks,
        "VAL4931_26_register_csv",
        "claims and variable registers parse with unique new identifiers",
        "one L-773 and sixteen 4931 variables",
        f"L-773={sum(row['claim_id']=='L-773' for row in claims_rows)}; vars={sum('4931_MTS' in row['symbol'] for row in variable_rows)}",
        sum(row["claim_id"] == "L-773" for row in claims_rows) == 1
        and sum("4931_MTS" in row["symbol"] for row in variable_rows) == 16,
    )

    pycache = list(SCRIPTS.rglob("__pycache__"))
    checkpoint_cache = [
        path for directory in pycache for path in directory.glob("*") if "4931" in path.name
    ]
    add_check(
        checks,
        "VAL4931_27_pycache",
        "checkpoint execution creates no 4931 bytecode cache",
        0,
        len(checkpoint_cache),
        not checkpoint_cache,
    )

    write_csv(VALIDATION_OUTPUT, checks)
    passed_count = sum(as_bool(row["passed"]) for row in checks)
    all_passed = passed_count == len(checks)
    print("P8_Y5_BRR545_4931_VALIDATION_PASS" if all_passed else "P8_Y5_BRR545_4931_VALIDATION_FAIL")
    print(f"checks_passed={passed_count}/{len(checks)}")
    if not all_passed:
        print("failed=" + ",".join(row["validation_id"] for row in checks if not as_bool(row["passed"])))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
