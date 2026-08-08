from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4949"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4949_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4949_CTP_2PI_static_source_and_occupation_gate.py"
RESULT_JSON = SOURCE / "CTP_2PI_static_source_results.json"
CTP_CSV = SOURCE / "CTP_2PI_parent_reconstruction.csv"
AXISYMMETRIC_CSV = SOURCE / "axisymmetric_Dyson_and_static_production_gate.csv"
SPARC_CSV = SOURCE / "SPARC_outer_occupation_scale_diagnostic.csv"
STRESS_CSV = SOURCE / "occupation_stress_conservation_and_local_limit.csv"
PAIR_CSV = SOURCE / "reflection_even_pair_source_next_operator_gate.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
FORMAL_NOTE = FORMAL / "965-PPC4161-CTP-2PI-static-source-no-go-and-pair-operator-pivot.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
EXPECTED_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"
RESULT_MARKER = "MTS_4949_CTP_2PI_STATIC_SOURCE_AND_OCCUPATION_GATE"
CHECKPOINT_MARKER = "MTS_CTP_2PI_STATIC_SOURCE_OCCUPATION_NO_GO_4949"
FORMAL_MARKER = "PPC4161_CTP_2PI_STATIC_SOURCE_NO_GO_4949"
PROVENANCE_MARKER = "MTS_CTP_2PI_STATIC_SOURCE_PROVENANCE_4949"
NEXT_TARGET = "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md"

LIGHT_SPEED = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR = 1.054571817e-34
PLANCK_LENGTH = math.sqrt(HBAR * NEWTON_G / LIGHT_SPEED**3)
KPC = 3.085677581491367e19

HASH_LOCKS = {
    MAIN_SCRIPT: "b2ed318c746177cd3e7a7954a81dac198633e07fe75ed6b6d0d2c8a7e30f2586",
    RESULT_JSON: "d0c35037c02ac0765cb4c726f52a6e4d99132ad64f14fb9f7d0056e2b8e10121",
    CTP_CSV: "18205d8433dd7a3a19ae8298c73300b50f76852a9afb4cec20385ac8a7ec07db",
    AXISYMMETRIC_CSV: "99e68fe685c7f23c3eec7b542d63f7766f674ab08f980f0df7402f314463d794",
    SPARC_CSV: "959c76b6e88efcf9ddcc9d010a20fbb1cefebfb310797e0b1814e76e3a13e92a",
    STRESS_CSV: "1476efcfd0d2d3ba18fe5ef75e8789a3b6aeddb0884630ac67a46e6a331680ad",
    PAIR_CSV: "b1d59a08ce6b48ee6a21da5e0e4ae0b3fdb4766efb448124998f9a014c759297",
    GALAXY_SNAPSHOT_CSV: "7a290dc34f176d07f5b428a8a4b2a170fc887abeb03075419eaadf12f2509443",
    PROVENANCE: "1b6c10da339c676f0aa03458aa89b84edd74965f258350f66f8eeaac70e071d8",
    CHECKPOINT: "772bee9863471ab7e4a4e4887773b91786110539d471243c26aaa1b88866f7b8",
    FORMAL_NOTE: "175a408e8aadd8aa512c65a9614988bce615ee57dbe0bc925adb6bb44288da23",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_path(raw: str) -> Path:
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_samples() -> list[dict[str, str]]:
    raw = text(GALAXY_SAMPLES)
    return json.loads(raw[raw.index("[") : raw.rindex("]") + 1])


def parse_points(raw: str) -> list[list[float]]:
    return [
        [float(value) for value in line.split()]
        for line in raw.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": check_id,
            "test": test,
            "expected": json.dumps(expected, sort_keys=True, default=str),
            "actual": json.dumps(actual, sort_keys=True, default=str),
            "passed": bool(passed),
            "checkpoint_marker": RESULT_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "VAL4949_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): [expected, digest(path)]
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4949_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4949_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4949_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4949_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = []
    for raw, expected in result["source_hashes"].items():
        path = source_path(raw)
        if not path.exists() or digest(path) != expected:
            source_errors.append(raw)
    add(checks, "VAL4949_06_sources", "source paths and hashes", [], source_errors, not source_errors)
    clause_failures = [name for name, passed in result["source_clause_checks"].items() if not passed]
    add(checks, "VAL4949_07_clauses", "authoritative source clauses", [], clause_failures, not clause_failures)

    tables = {
        "ctp": read_csv(CTP_CSV),
        "axis": read_csv(AXISYMMETRIC_CSV),
        "sparc": read_csv(SPARC_CSV),
        "stress": read_csv(STRESS_CSV),
        "pair": read_csv(PAIR_CSV),
        "galaxy": read_csv(GALAXY_SNAPSHOT_CSV),
    }
    malformed = {
        f"{name}:{index}": row
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4949_08_csv", "all generated CSV rows parse", {}, malformed, not malformed)
    invalid_claim_rows = [
        f"{name}:{index}"
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if row.get("valid_for_full_MTS_claim") != "False"
    ]
    add(checks, "VAL4949_09_nonclaim", "all rows retain full-MTS nonclaim", [], invalid_claim_rows, not invalid_claim_rows)

    ctp = tables["ctp"]
    expected_ctp_ids = {f"CTP4949_{index:02d}_{suffix}" for index, suffix in enumerate((
        "parent_action", "CTP_variables", "Dyson", "KB_spectral", "KB_statistical",
        "scalar_Gamma2", "metric_quantum_hierarchy", "initial_state", "Euclidean_boundary"
    ))}
    ctp_ids = {row["derivation_id"] for row in ctp}
    ctp_ok = len(ctp) == 9 and ctp_ids == expected_ctp_ids and all(row["passed"] == "True" for row in ctp)
    add(checks, "VAL4949_10_ctp_rows", "nine CTP derivation rows", sorted(expected_ctp_ids), sorted(ctp_ids), ctp_ok)
    ctp_map = {row["derivation_id"]: row for row in ctp}
    ctp_boundary = (
        ctp_map["CTP4949_05_scalar_Gamma2"]["status"] == "SCALAR_COLLISION_AND_SOURCE_KERNELS_ZERO"
        and ctp_map["CTP4949_06_metric_quantum_hierarchy"]["status"] == "SCALAR_ONLY_2PI_NOT_FULL_PARENT_QUANTUM_CLOSURE"
        and ctp_map["CTP4949_07_initial_state"]["status"] == "OCCUPATION_IS_INITIAL_DATA_WITHOUT_SOURCE_KERNEL"
        and ctp_map["CTP4949_08_Euclidean_boundary"]["status"] == "EUCLIDEAN_CONTRACT_REPLACED_FOR_OCCUPATION_DYNAMICS"
    )
    add(checks, "VAL4949_11_ctp_boundary", "scalar and full-parent CTP boundary", True, ctp_boundary, ctp_boundary)

    axis = tables["axis"]
    expected_axis_ids = {f"AXI4949_{index:02d}_{suffix}" for index, suffix in enumerate((
        "metric", "operator", "mode_operator", "positivity", "static_modes",
        "Bogoliubov", "occupation", "O4", "full_quantum"
    ))}
    axis_ids = {row["gate_id"] for row in axis}
    axis_ok = len(axis) == 9 and axis_ids == expected_axis_ids and all(row["passed"] == "True" for row in axis)
    add(checks, "VAL4949_12_axis_rows", "nine axisymmetric source gates", sorted(expected_axis_ids), sorted(axis_ids), axis_ok)
    axis_map = {row["gate_id"]: row for row in axis}
    source_no_go = (
        axis_map["AXI4949_03_positivity"]["decision"] == "PASS_POSITIVE_OPERATOR_NO_BIFURCATION"
        and axis_map["AXI4949_05_Bogoliubov"]["decision"] == "STATIC_PAIR_PRODUCTION_EXACT_ZERO"
        and axis_map["AXI4949_06_occupation"]["decision"] == "SOURCE_DEPENDENT_AMPLITUDE_NOT_DERIVED"
        and axis_map["AXI4949_07_O4"]["decision"] == "O4_DOES_NOT_POPULATE_STATIC_COMPOSITE"
    )
    add(checks, "VAL4949_13_static_no_go", "positive static no-production chain", True, source_no_go, source_no_go)

    samples = load_samples()
    sparc = tables["sparc"]
    add(checks, "VAL4949_14_sample_count", "175 public samples and outputs", [175, 175], [len(samples), len(sparc)], len(samples) == 175 and len(sparc) == 175)
    sparc_map = {row["galaxy"]: row for row in sparc}
    independent_errors: list[str] = []
    independent_logs: list[float] = []
    independent_gap_logs: list[float] = []
    for sample in samples:
        name = sample["name"].removesuffix("_rotmod.dat")
        point = parse_points(sample["text"])[-1]
        radius_kpc, vobs, _, vgas, vdisk, vbulge = point[:6]
        radius_m = radius_kpc * KPC
        vbar2 = vgas * abs(vgas) + 0.5 * vdisk**2 + 0.7 * vbulge**2
        residual_v2 = max(vobs**2 - vbar2, 0.0)
        energy = residual_v2 * 1.0e6 * LIGHT_SPEED**2 / (4.0 * math.pi * NEWTON_G * radius_m**2)
        one_quantum = HBAR * LIGHT_SPEED / radius_m**4
        occupation = energy / one_quantum if residual_v2 > 0.0 else 0.0
        gap = (PLANCK_LENGTH / radius_m) ** 2
        row = sparc_map.get(name)
        if row is None:
            independent_errors.append(name + ":missing")
            continue
        comparisons = (
            math.isclose(float(row["outer_radius_kpc"]), radius_kpc, rel_tol=0.0, abs_tol=1e-14),
            math.isclose(float(row["outer_Vbar2_km2_s2"]), vbar2, rel_tol=2e-15, abs_tol=1e-12),
            math.isclose(float(row["outer_residual_V2_km2_s2"]), residual_v2, rel_tol=2e-15, abs_tol=1e-12),
            math.isclose(float(row["Jgap_if_correlation_length_equals_outer_radius"]), gap, rel_tol=2e-15),
            math.isclose(float(row["occupation_per_R_cell_required"]), occupation, rel_tol=3e-15, abs_tol=0.0),
        )
        if not all(comparisons):
            independent_errors.append(name + ":value")
        if occupation > 0.0:
            independent_logs.append(math.log10(occupation))
            independent_gap_logs.append(math.log10(gap))
    add(checks, "VAL4949_15_recompute", "all sample diagnostics independently recomputed", [], independent_errors, not independent_errors)
    positive_count = sum(row["positive_outer_residual"] == "True" for row in sparc)
    add(checks, "VAL4949_16_positive", "173 positive outer residuals", 173, positive_count, positive_count == 173)
    expected_stats = {
        "min": 99.07773582607567,
        "median": 102.51076468255594,
        "max": 105.29331688171573,
        "gap_median": -110.67167303782026,
    }
    actual_stats = {
        "min": min(independent_logs),
        "median": statistics.median(independent_logs),
        "max": max(independent_logs),
        "gap_median": statistics.median(independent_gap_logs),
    }
    stats_ok = all(math.isclose(actual_stats[key], value, rel_tol=0.0, abs_tol=1e-12) for key, value in expected_stats.items())
    add(checks, "VAL4949_17_stats", "occupation and gap summary statistics", expected_stats, actual_stats, stats_ok)
    formula_ok = all(
        math.isclose(
            float(row["occupation_per_R_cell_required"]),
            (math.sqrt(float(row["outer_residual_V2_km2_s2"])) * 1000.0 / LIGHT_SPEED) ** 2
            * (float(row["outer_radius_kpc"]) * KPC / PLANCK_LENGTH) ** 2
            / (4.0 * math.pi),
            rel_tol=4e-15,
        )
        for row in sparc
        if row["positive_outer_residual"] == "True"
    )
    add(checks, "VAL4949_18_formula", "dimensionless occupation identity", True, formula_ok, formula_ok)

    stress = tables["stress"]
    expected_stress_ids = {f"STR4949_{index:02d}_{suffix}" for index, suffix in enumerate((
        "state_subtraction", "stress", "Ward", "vacuum", "vacuum_polarization", "local_limit", "macroscopic_scale", "predictivity"
    ))}
    stress_ids = {row["gate_id"] for row in stress}
    stress_ok = len(stress) == 8 and stress_ids == expected_stress_ids and all(row["passed"] == "True" for row in stress)
    add(checks, "VAL4949_19_stress_rows", "eight stress and local-limit gates", sorted(expected_stress_ids), sorted(stress_ids), stress_ok)
    stress_map = {row["gate_id"]: row for row in stress}
    stress_boundary = (
        stress_map["STR4949_02_Ward"]["decision"] == "PASS_CONDITIONAL_CONSERVATION"
        and stress_map["STR4949_03_vacuum"]["decision"] == "VACUUM_OCCUPATION_STRESS_ZERO"
        and stress_map["STR4949_05_local_limit"]["decision"] == "PASS_LOCAL_GR_RECOVERY"
        and stress_map["STR4949_07_predictivity"]["decision"] == "CURRENT_MINIMAL_2PI_GALAXY_ROUTE_REJECTED"
    )
    add(checks, "VAL4949_20_stress_boundary", "stress conservation recovery and rejection", True, stress_boundary, stress_boundary)

    pair = tables["pair"]
    expected_pair_ids = {f"PAIR4949_{index:02d}_{suffix}" for index, suffix in enumerate((
        "existing_metric_pair", "Rpsi2", "Tpsi2", "quartic", "state_history", "acceptance"
    ))}
    pair_ids = {row["operator_id"] for row in pair}
    pair_ok = len(pair) == 6 and pair_ids == expected_pair_ids and all(row["passed"] == "True" for row in pair)
    add(checks, "VAL4949_21_pair_rows", "six next-operator gates", sorted(expected_pair_ids), sorted(pair_ids), pair_ok)
    adopted = [row["operator_id"] for row in pair if "NOT_ADOPTED" not in row["decision"] and row["operator_id"] in {"PAIR4949_01_Rpsi2", "PAIR4949_02_Tpsi2"}]
    add(checks, "VAL4949_22_no_adoption", "no pair coefficient adopted", [], adopted, not adopted)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["CTP_2PI_equations_derived"]
        and boundary["axisymmetric_parent_Dyson_operator_derived"]
        and boundary["static_vacuum_pair_production_zero"]
        and boundary["state_stress_conservation_contract_derived"]
        and boundary["local_GR_recovery_derived"]
        and boundary["SPARC_occupation_scale_diagnostic_calculated"]
        and not boundary["source_dependent_composite_amplitude_derived"]
        and not boundary["macroscopic_galaxy_stress_calculated"]
        and not boundary["current_minimal_2PI_galaxy_route_viable"]
        and not boundary["pair_source_operator_parent_derived"]
        and not boundary["full_MTS_galaxy_unification"]
        and not boundary["galaxy_repository_modified"]
    )
    add(checks, "VAL4949_23_boundary", "claim boundary", True, boundary, boundary_ok)

    galaxy = tables["galaxy"]
    snapshot = galaxy[0] if len(galaxy) == 1 else {}
    snapshot_ok = (
        len(galaxy) == 1
        and snapshot.get("head") == EXPECTED_HEAD
        and snapshot.get("working_tree_clean") == "True"
        and snapshot.get("repository_modified_by_checkpoint") == "False"
        and snapshot.get("sample_count") == "175"
    )
    add(checks, "VAL4949_24_snapshot", "galaxy read-only snapshot", True, snapshot, snapshot_ok)
    runtime_head = subprocess.run(["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    runtime_status = subprocess.run(["git", "-C", str(GALAXY_REPO), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    add(checks, "VAL4949_25_runtime", "galaxy clone remains locked and clean", [EXPECTED_HEAD, ""], [runtime_head, runtime_status], runtime_head == EXPECTED_HEAD and not runtime_status)

    claim = next((row for row in read_csv(CLAIMS) if row["claim_id"] == "L-791"), None)
    claim_ok = bool(claim) and "private_nonclaim" in claim["status"] and NEXT_TARGET in claim["next_test"] and "FULL_MTS_FALSE" in claim["notes"]
    add(checks, "VAL4949_26_claim", "claim L-791 registered", True, claim, claim_ok)
    expected_variables = {
        "CTPStatisticalFunction4949_MTS", "AxisymmetricMotionOperator4949_MTS",
        "StaticProductionNoGo4949_MTS", "OccupationStress4949_MTS",
        "VacuumStateSubtraction4949_MTS", "SPARCOccupationScale4949_MTS",
        "PairOperatorGate4949_MTS", "PredictivityStatus4949_MTS",
    }
    variable_rows = [row for row in read_csv(VARIABLES) if row["symbol"] in expected_variables]
    add(checks, "VAL4949_27_variables", "eight variables registered", sorted(expected_variables), sorted(row["symbol"] for row in variable_rows), len(variable_rows) == 8 and {row["symbol"] for row in variable_rows} == expected_variables)

    document_markers = {
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT) and NEXT_TARGET in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE) and NEXT_TARGET in text(FORMAL_NOTE),
        "equation": "## 1.242 CTP motion occupation, static source theorem and state stress" in text(EQUATIONS),
        "red_team": "## 193. A two-point function is not a sourced occupation" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4949_28_documents", "all document markers", {key: True for key in document_markers}, document_markers, all(document_markers.values()))
    checkpoint_tokens = (
        "Gamma_2^scalar=0", "static vacuum pair production",
        "99.0777", "current minimal scalar 2PI galaxy route",
    )
    checkpoint_lower = text(CHECKPOINT).lower()
    token_ok = all(token.lower() in checkpoint_lower for token in checkpoint_tokens)
    add(checks, "VAL4949_29_checkpoint_content", "checkpoint contains decisive equations and results", True, token_ok, token_ok)
    provenance_ok = all(token in text(PROVENANCE) for token in (
        "https://arxiv.org/abs/hep-ph/0409233",
        "https://github.com/Martin123132/MTS-Galaxy-Lab-",
        EXPECTED_HEAD,
        "valid_for_full_MTS_claim=False",
    ))
    add(checks, "VAL4949_30_provenance", "primary and data provenance recorded", True, provenance_ok, provenance_ok)

    scan_paths = [RESULT_JSON, CTP_CSV, AXISYMMETRIC_CSV, SPARC_CSV, STRESS_CSV, PAIR_CSV, CHECKPOINT, FORMAL_NOTE]
    placeholder_tokens = ("MISSING_", "PLACEHOLDER", "TODO", "TBD")
    placeholders = {str(path): token for path in scan_paths for token in placeholder_tokens if token in text(path)}
    add(checks, "VAL4949_31_placeholders", "no placeholder markers", {}, placeholders, not placeholders)
    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4949_32_pycache", "no scripts pycache", [], pycache, not pycache)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"VALIDATION_ROWS={len(checks)}")
    print(f"FAILED={len(failed)}")
    if failed:
        print("FAILED_IDS=" + ",".join(failed))
    print(f"OUTPUT_SHA256={digest(OUTPUT)}")
    print("PASS" if not failed else "FAIL")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
