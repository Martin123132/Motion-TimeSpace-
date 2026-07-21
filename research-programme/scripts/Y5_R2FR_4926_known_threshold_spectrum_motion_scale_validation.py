from __future__ import annotations

import csv
import hashlib
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "particle_data" / "4926"
SCRIPTS = POST / "scripts"

MARKER = "MTS_KNOWN_THRESHOLD_MOTION_SCALE_4926"
FORMAL_MARKER = "PPC4161_KNOWN_THRESHOLD_MOTION_SCALE_4926"
VALIDATION_MARKER = "MTS_KNOWN_THRESHOLD_MOTION_SCALE_VALIDATION_4926"
RESEARCH = SCRIPTS / "Y5_R2FR_4926_known_threshold_spectrum_motion_scale.py"
CHECKPOINT = (
    POST
    / "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md"
)
FORMAL_NOTE = FORMAL / "942-PPC4161-known-threshold-spectrum-and-motion-scale-normalization.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

EXPECTED_OUTPUTS = [
    "P8_Y5_R2FR_4926_PDG_MASS_SNAPSHOT.csv",
    "P8_Y5_R2FR_4926_THRESHOLD_DOMAIN_SPLIT.csv",
    "P8_Y5_R2FR_4926_COLORLESS_VISIBLE_THRESHOLDS.csv",
    "P8_Y5_R2FR_4926_NEUTRINO_SCENARIOS.csv",
    "P8_Y5_R2FR_4926_LOCALITY_ENVELOPE.csv",
    "P8_Y5_R2FR_4926_QCD_MATCHING_FIREWALL.csv",
    "P8_Y5_R2FR_4926_MOTION_SCALE_DIMENSION_AUDIT.csv",
    "P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv",
    "P8_Y5_R2FR_4926_IR_WILSON_COLLAPSE.csv",
    "P8_Y5_R2FR_4926_SOURCE_REGISTER.csv",
    "P8_Y5_R2FR_4926_GATE_DECISION.csv",
]

EXPECTED_HASHES = {
    SOURCE / "pdg-2026.0.sqlite": "40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe",
    SOURCE / "NuFIT-6.0-v2.pdf": "66ff020fea48d04fe703e99559d625ed3d0bacfc36cbf619b8df16652d54194f",
    SOURCE / "Heavy-Fields-and-Gravity-v2.pdf": "57e93146014b3b02b518fd456c739bbc87cbe0974660c84b86301edc45799dd3",
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
    compile_targets = [RESEARCH, Path(__file__).resolve()]
    compile_failures: list[str] = []
    for path in compile_targets:
        try:
            compile(source_text(path), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4926_00_compile",
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
        timeout=120,
        check=False,
    )
    add_check(
        checks,
        "VAL4926_01_research_run",
        "research generator reruns successfully",
        "return 0 and PASS marker",
        f"return={run.returncode}; stdout={run.stdout.strip()}",
        run.returncode == 0
        and "P8_Y5_R2FR_4926_KNOWN_THRESHOLD_MOTION_SCALE_PASS" in run.stdout,
    )

    missing_outputs = [name for name in EXPECTED_OUTPUTS if not (OUTPUT / name).exists()]
    add_check(
        checks,
        "VAL4926_02_outputs",
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
        "VAL4926_03_csv_shape",
        "all evidence CSVs parse with no overflow columns",
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
        "VAL4926_04_markers",
        "all generated evidence rows carry the checkpoint marker",
        0,
        len(marker_failures),
        not marker_failures,
    )
    claimable_rows = [row for row in all_evidence_rows if as_bool(row.get("valid_for_claim"))]
    add_check(
        checks,
        "VAL4926_05_nonclaim",
        "all checkpoint evidence remains nonclaim",
        0,
        len(claimable_rows),
        not claimable_rows,
    )
    missing_markers = [
        row
        for row in all_evidence_rows
        if "MISSING_" in " ".join(str(value) for value in row.values())
    ]
    add_check(
        checks,
        "VAL4926_06_no_placeholder_tokens",
        "no generated row contains a MISSING placeholder token",
        0,
        len(missing_markers),
        not missing_markers,
    )

    hash_failures = [
        path.name
        for path, expected_hash in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected_hash
    ]
    add_check(
        checks,
        "VAL4926_07_source_hashes",
        "PDG NuFIT and heavy-field files match locked SHA-256 values",
        0,
        len(hash_failures),
        not hash_failures,
    )

    source_rows = parsed["P8_Y5_R2FR_4926_SOURCE_REGISTER.csv"]
    source_failures = [row["source_id"] for row in source_rows if not as_bool(row["passed"])]
    add_check(
        checks,
        "VAL4926_08_source_register",
        "all local markers hashes and external primary URLs are recorded",
        0,
        len(source_failures),
        not source_failures,
    )

    mass_rows = parsed["P8_Y5_R2FR_4926_PDG_MASS_SNAPSHOT.csv"]
    mass_species = {row["species_id"]: row for row in mass_rows}
    electron_mass = float(mass_species["electron"]["mass_eV"])
    add_check(
        checks,
        "VAL4926_09_PDG_snapshot",
        "eight PDG records are API-extracted and the electron mass is locked",
        "8 rows; 510998.95069 eV; package 2026.0",
        f"{len(mass_rows)} rows; {electron_mass} eV; package {mass_species['electron']['pdg_api_package']}",
        len(mass_rows) == 8
        and math.isclose(electron_mass, 510998.95069, rel_tol=1.0e-13)
        and mass_species["electron"]["pdg_api_package"] == "2026.0",
    )

    visible_rows = parsed["P8_Y5_R2FR_4926_COLORLESS_VISIBLE_THRESHOLDS.csv"]
    visible_total = next(
        row for row in visible_rows if row["row_id"] == "VIS4926_total_without_neutrinos"
    )
    add_check(
        checks,
        "VAL4926_10_visible_sum",
        "signed non-neutrino colorless sum matches the independent target",
        -1.640178869062048e-99,
        visible_total["a_threshold_m4"],
        math.isclose(
            float(visible_total["a_threshold_m4"]),
            -1.640178869062048e-99,
            rel_tol=2.0e-14,
        ),
    )
    add_check(
        checks,
        "VAL4926_11_visible_locality",
        "all six source-locked colorless free fields pass m greater than 10Q",
        0,
        sum(1 for row in visible_rows[:-1] if not as_bool(row["passed"])),
        all(as_bool(row["passed"]) for row in visible_rows[:-1]),
    )

    neutrino_rows = parsed["P8_Y5_R2FR_4926_NEUTRINO_SCENARIOS.csv"]
    max_neutrino_length = max(
        float(row["colorless_total_absolute_length_m"]) for row in neutrino_rows
    )
    add_check(
        checks,
        "VAL4926_12_neutrino_scenarios",
        "four lightest-zero scenarios retain one nonlocal eigenstate",
        "4 rows; one nonlocal state each",
        f"{len(neutrino_rows)} rows; counts={[row['massless_nonlocal_eigenstates'] for row in neutrino_rows]}",
        len(neutrino_rows) == 4
        and all(row["massless_nonlocal_eigenstates"] == "1" for row in neutrino_rows),
    )
    add_check(
        checks,
        "VAL4926_13_max_colorless",
        "largest colorless threshold length matches the normal-Dirac benchmark",
        1.5576594346003402e-21,
        max_neutrino_length,
        math.isclose(max_neutrino_length, 1.5576594346003402e-21, rel_tol=2.0e-14),
    )
    max_compact_ratio = max(
        float(row["colorless_a_ratio_to_NS_one_percent"]) for row in neutrino_rows
    )
    add_check(
        checks,
        "VAL4926_14_colorless_compact",
        "all displayed colorless scenarios are over ninety coefficient orders below compact target",
        "less than 1e-90",
        max_compact_ratio,
        max_compact_ratio < 1.0e-90,
    )

    locality_rows = parsed["P8_Y5_R2FR_4926_LOCALITY_ENVELOPE.csv"]
    strict_gw = next(
        row
        for row in locality_rows
        if row["arena"] == "GW250114" and row["gate"] == "strict_locality_gate"
    )
    add_check(
        checks,
        "VAL4926_15_locality_envelope",
        "strict per-Dirac locality envelope is compact negligible",
        "ell=3.273337966535713e-17 m and ratio below 1e-80",
        f"ell={strict_gw['max_threshold_length_m']}; ratio={strict_gw['a_ratio_to_NS_one_percent']}",
        math.isclose(
            float(strict_gw["max_threshold_length_m"]),
            3.273337966535713e-17,
            rel_tol=2.0e-14,
        )
        and float(strict_gw["a_ratio_to_NS_one_percent"]) < 1.0e-80,
    )

    dimension_rows = parsed["P8_Y5_R2FR_4926_MOTION_SCALE_DIMENSION_AUDIT.csv"]
    dimension_statuses = {row["status"] for row in dimension_rows}
    add_check(
        checks,
        "VAL4926_16_dimension_repair",
        "dimension audit derives Delta=3/2 and canonical 8/3 coupling",
        "all six checks pass",
        f"{sum(as_bool(row['passed']) for row in dimension_rows)}/{len(dimension_rows)}",
        len(dimension_rows) == 6
        and all(as_bool(row["passed"]) for row in dimension_rows)
        and "NONCANONICAL_FIELD_DIMENSION_DERIVED" in dimension_statuses
        and "CANONICAL_COUPLING_REPAIR_DERIVED" in dimension_statuses,
    )

    motion_rows = parsed["P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv"]
    motion_by_branch = {row["branch"]: row for row in motion_rows}
    minimal_motion_length = float(
        motion_by_branch["C_N_1_central_c_m"][
            "motion_threshold_length_m_per_real_pole"
        ]
    )
    add_check(
        checks,
        "VAL4926_17_motion_benchmark",
        "minimal branch numerical transform matches the Planck-scale calculation",
        6.349828232642897e-37,
        minimal_motion_length,
        math.isclose(minimal_motion_length, 6.349828232642897e-37, rel_tol=2.0e-14),
    )
    add_check(
        checks,
        "VAL4926_18_CN_nonclaim",
        "every normalization row refuses parent ownership",
        0,
        sum(1 for row in motion_rows if as_bool(row.get("parent_derived"))),
        all(not as_bool(row.get("parent_derived")) for row in motion_rows),
    )
    cn_log = float(motion_by_branch["compact_bound_on_C_N"]["log10_C_N_max"])
    cpsi_min = float(
        motion_by_branch["generic_canonical_coupling_floor"][
            "C_psi_min_for_NS_one_percent"
        ]
    )
    add_check(
        checks,
        "VAL4926_19_normalization_bounds",
        "one-pole CN and canonical-coupling compact transforms are reproduced",
        "log10 CNmax=634.6308; Cpsi_min=1.96038e-211",
        f"log10 CNmax={cn_log}; Cpsi_min={cpsi_min}",
        math.isclose(cn_log, 634.6308338490828, rel_tol=1.0e-14)
        and math.isclose(cpsi_min, 1.960375552989088e-211, rel_tol=2.0e-14),
    )

    qcd_rows = parsed["P8_Y5_R2FR_4926_QCD_MATCHING_FIREWALL.csv"]
    qcd_by_id = {row["row_id"]: row for row in qcd_rows}
    add_check(
        checks,
        "VAL4926_20_QCD_firewall",
        "QCD compact coefficient firewall is numeric while exact matching stays open",
        "C_required>1e118 and status absorbed in one remainder",
        f"C={qcd_by_id['QCD4926_02_NS_firewall']['value']}; status={qcd_by_id['QCD4926_04_matching_status']['status']}",
        float(qcd_by_id["QCD4926_02_NS_firewall"]["value"]) > 1.0e118
        and qcd_by_id["QCD4926_04_matching_status"]["status"]
        == "ABSORBED_IN_ONE_IR_WILSON_REMAINDER",
    )

    ir_rows = parsed["P8_Y5_R2FR_4926_IR_WILSON_COLLAPSE.csv"]
    add_check(
        checks,
        "VAL4926_21_one_Wilson",
        "every spectrum scenario retains one low-energy I1 parameter",
        "one in every row",
        [row["independent_low_energy_I1_test_parameters"] for row in ir_rows],
        all(row["independent_low_energy_I1_test_parameters"] == "1" for row in ir_rows),
    )
    max_offset_ratio = max(float(row["known_offset_ratio_to_GW_envelope"]) for row in ir_rows)
    add_check(
        checks,
        "VAL4926_22_offset_size",
        "known offsets are negligible relative to the current GW envelope",
        "less than 1e-100",
        max_offset_ratio,
        max_offset_ratio < 1.0e-100,
    )

    gate_rows = parsed["P8_Y5_R2FR_4926_GATE_DECISION.csv"]
    gate_map = {row["gate"]: row for row in gate_rows}
    add_check(
        checks,
        "VAL4926_23_gate_state",
        "weak GR is retained while compact and full claims remain unpromoted",
        "weak retained; compact false; full false",
        f"weak={gate_map['weak_GR']['status']}; compact={gate_map['compact_GR']['status']}; full={gate_map['full_MTS_to_GR']['status']}",
        gate_map["weak_GR"]["status"] == "RETAINED"
        and gate_map["compact_GR"]["status"] == "NOT_PROMOTED"
        and gate_map["full_MTS_to_GR"]["status"] == "NOT_PROMOTED"
        and all(not as_bool(row["claim_promoted"]) for row in gate_rows),
    )

    required_markers = {
        CHECKPOINT: MARKER,
        FORMAL_NOTE: FORMAL_MARKER,
        SOURCE / "PROVENANCE.md": "MTS_KNOWN_THRESHOLD_MOTION_SCALE_PROVENANCE_4926",
        RESUME: "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue",
        FORMAL / "02-claims-register.csv": "L-768",
        FORMAL / "04-variable-audit.csv": "MotionNormalizationCoefficient4926_MTS",
        FORMAL / "05-equation-register.md": "1.219 Known thresholds and repaired motion normalization",
        FORMAL / "06-consistency-red-team.md": "170. A dimensionful old coupling is not a canonical physical scale",
        FORMAL / "07-unification-spine.md": "PPC4161 checkpoint 4926",
    }
    marker_problems = [
        path.name
        for path, marker in required_markers.items()
        if not path.exists() or marker not in source_text(path)
    ]
    add_check(
        checks,
        "VAL4926_24_registers",
        "checkpoint formal note provenance resume and five registers carry their markers",
        0,
        len(marker_problems),
        not marker_problems,
    )

    required_variables = {
        "KnownColorlessC3Threshold4926_MTS",
        "NeutrinoThresholdScenarios4926_MTS",
        "LocalThresholdEnvelope4926_MTS",
        "QCDMatchingBlock4926_MTS",
        "MotionOldFieldDimension4926_MTS",
        "MotionNormalizationMass4926_MTS",
        "MotionCanonicalCoupling4926_MTS",
        "MotionPhysicalScale4926_MTS",
        "MotionNormalizationCoefficient4926_MTS",
        "IRWilsonCollapse4926_MTS",
        "VacuumGRThresholdStatus4926_MTS",
    }
    variable_symbols = {
        row["symbol"] for row in read_csv(FORMAL / "04-variable-audit.csv")
    }
    add_check(
        checks,
        "VAL4926_25_variables",
        "all eleven canonical variables are registered",
        11,
        len(required_variables & variable_symbols),
        required_variables <= variable_symbols,
    )

    pycache_paths = list((POST / "scripts").rglob("__pycache__"))
    add_check(
        checks,
        "VAL4926_26_pycache",
        "scripts tree contains no Python bytecode cache directories",
        0,
        len(pycache_paths),
        not pycache_paths,
    )

    all_passed = all(as_bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4926_OVERALL",
        "checkpoint 4926 evidence and claim-discipline validation",
        "all checks pass",
        f"{sum(as_bool(row['passed']) for row in checks)}/{len(checks)} pre-overall checks pass",
        all_passed,
    )
    write_csv(OUTPUT / "P8_Y5_BRR545_4926_VALIDATION.csv", checks)
    print(
        "P8_Y5_BRR545_4926_VALIDATION_PASS"
        if all_passed
        else "P8_Y5_BRR545_4926_VALIDATION_FAIL"
    )
    print(f"checks_passed={sum(as_bool(row['passed']) for row in checks)}/{len(checks)}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
