from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4948"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4948_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4948_motion_Hessian_to_galaxy_phase_flow.py"
RESULT_JSON = SOURCE / "motion_Hessian_galaxy_phase_results.json"
LOGISTIC_CSV = SOURCE / "projective_logistic_derivation.csv"
EXPONENT_CSV = SOURCE / "parent_exponent_to_galaxy_gate.csv"
SOURCE_GATE_CSV = SOURCE / "source_amplitude_and_stress_gate.csv"
COMPOSITE_CSV = SOURCE / "composite_2PI_survivor_contract.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md"
FORMAL_NOTE = FORMAL / "964-PPC4161-parent-Hessian-galaxy-phase-and-2PI-interface.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

GALAXY_REPO = Path(r"D:\g4948")
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"
RESULT_MARKER = "MTS_4948_MOTION_HESSIAN_GALAXY_PHASE_INTERFACE"
CHECKPOINT_MARKER = "MTS_PARENT_HESSIAN_GALAXY_PHASE_2PI_INTERFACE_4948"
FORMAL_MARKER = "PPC4161_PARENT_HESSIAN_GALAXY_PHASE_2PI_4948"
PROVENANCE_MARKER = "MTS_PARENT_HESSIAN_GALAXY_PHASE_2PI_PROVENANCE_4948"
NEXT_TARGET = "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "125905252071eded2726b91cf0e5d99e4cc5baaccbb053c5ea0c823c50c0f576",
    RESULT_JSON: "4a63b8c77afcc8da0a323bfaff83b80886cf6a072b506d0190c2bbe535829b4c",
    LOGISTIC_CSV: "49ca0028a18208ff8a50c3615433d6d463e181f4d0086ddc8402658eff35828b",
    EXPONENT_CSV: "a48f5eacbac8dd46e7fef87e0b15e5adec9ed9a4b4e782a1709838b8e383e1b5",
    SOURCE_GATE_CSV: "3b34c3c0224a9be9de3fb2cb3d7e22a368caad1f2023da51ff559c360f08f273",
    COMPOSITE_CSV: "27041c4259538c16a798bcca19ed76795626aaf3f97741a635c262cae358a299",
    GALAXY_SNAPSHOT_CSV: "64cb0fd786f56fc324df0b47ad5fb17352daa8f5696c64b8a0b474bbe2a20cb7",
    PROVENANCE: "5b567ac037c83e45bcc1ceb9a844815a2f8d72dc7f435608935a066793512d31",
    CHECKPOINT: "b563ab1bf95974732dd5f2a3ab2cd5af2d5b414011648554e5247a930b47aec0",
    FORMAL_NOTE: "0a8bae8b54ada9d5b1493fac5b72cfdc5bf127f03a02bbd3ae4818503998184b",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def source_path(raw: str) -> Path:
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else ROOT / candidate


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
    add(checks, "VAL4948_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): [expected, digest(path)]
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4948_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4948_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4948_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4948_05_internal", "research checks pass", [], failed_internal, not failed_internal)
    source_errors = []
    for raw, expected in result["source_hashes"].items():
        path = source_path(raw)
        if not path.exists() or digest(path) != expected:
            source_errors.append(raw)
    add(checks, "VAL4948_06_sources", "result source paths and hashes", [], source_errors, not source_errors)
    clause_failures = [name for name, passed in result["source_clause_checks"].items() if not passed]
    add(checks, "VAL4948_07_clauses", "source clauses match", [], clause_failures, not clause_failures)

    tables = {
        "logistic": read_csv(LOGISTIC_CSV),
        "exponent": read_csv(EXPONENT_CSV),
        "source_gate": read_csv(SOURCE_GATE_CSV),
        "composite": read_csv(COMPOSITE_CSV),
        "galaxy": read_csv(GALAXY_SNAPSHOT_CSV),
    }
    malformed = {
        f"{name}:{index}": row
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4948_08_csv_shape", "generated CSV rows parse", {}, malformed, not malformed)
    nonclaims = [
        f"{name}:{index}"
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if row.get("valid_for_full_MTS_claim") != "False"
    ]
    add(checks, "VAL4948_09_nonclaim", "all evidence rows are full-MTS nonclaims", [], nonclaims, not nonclaims)

    logistic = tables["logistic"]
    expected_logistic_ids = {f"LOG4948_{index:02d}_{suffix}" for index, suffix in enumerate((
        "shell_map", "growing_ratio", "growing_occupation", "decaying_ratio",
        "decaying_occupation", "single_mode_complement", "canonical_support"
    ))}
    logistic_ids = {row["derivation_id"] for row in logistic}
    logistic_ok = len(logistic) == 7 and logistic_ids == expected_logistic_ids and all(row["passed"] == "True" for row in logistic)
    add(checks, "VAL4948_10_logistic_rows", "seven exact projective rows", sorted(expected_logistic_ids), sorted(logistic_ids), logistic_ok)
    logistic_map = {row["derivation_id"]: row for row in logistic}
    identities_ok = (
        "theta_mass n(1-n)" in logistic_map["LOG4948_02_growing_occupation"]["derived_equation"]
        and "-lambda_O4 b(1-b)" in logistic_map["LOG4948_04_decaying_occupation"]["derived_equation"]
        and "s=q and R_b=R_n" in logistic_map["LOG4948_05_single_mode_complement"]["derived_equation"]
        and logistic_map["LOG4948_06_canonical_support"]["status"] == "CANONICAL_EXPONENTIAL_IS_NOT_LOGISTIC"
    )
    add(checks, "VAL4948_11_identities", "logistic and nonidentity equations", True, identities_ok, identities_ok)
    residuals_ok = (
        float(result["projective_theorem"]["max_numeric_n_residual"]) < 1.0e-9
        and float(result["projective_theorem"]["max_numeric_b_residual"]) < 1.0e-9
    )
    add(checks, "VAL4948_12_numeric", "finite-difference projective residuals", "<1e-9", result["projective_theorem"], residuals_ok)

    exponents = tables["exponent"]
    expected_mappings = {"Wetterich_v_equals_minus_2lambda", "Wetterich_v_equals_plus_2lambda"}
    exponent_map = {row["mapping"]: row for row in exponents}
    add(checks, "VAL4948_13_exponent_rows", "two parent mappings", sorted(expected_mappings), sorted(exponent_map), len(exponents) == 2 and set(exponent_map) == expected_mappings)
    expected_theta = {
        "Wetterich_v_equals_minus_2lambda": 1.858483853942984,
        "Wetterich_v_equals_plus_2lambda": 1.8496934455116607,
    }
    theta_ok = all(math.isclose(float(exponent_map[name]["theta_mass_parent"]), value, rel_tol=1e-14) for name, value in expected_theta.items())
    add(checks, "VAL4948_14_theta", "mass critical exponents", expected_theta, {name: exponent_map[name]["theta_mass_parent"] for name in exponent_map}, theta_ok)
    o4_ok = all(math.isclose(float(row["lambda_O4_parent"]), 3.9960254522943828, rel_tol=1e-14) for row in exponents)
    add(checks, "VAL4948_15_O4", "O4 irrelevant exponent", 3.9960254522943828, [row["lambda_O4_parent"] for row in exponents], o4_ok)
    mismatch_ok = all(
        row["direct_locked_q_match_within_5_percent"] == "False"
        and row["zeta_required_differs_from_spectral_shell"] == "True"
        and 0.414 < float(row["zeta_required_to_force_locked_q"]) < 0.417
        for row in exponents
    )
    add(checks, "VAL4948_16_mismatch", "natural-shell q mismatch and unowned zeta", True, mismatch_ok, mismatch_ok)

    source_rows = tables["source_gate"]
    expected_source_ids = {f"SRCG4948_{index:02d}_{suffix}" for index, suffix in enumerate((
        "universal_length", "source_amplitude", "O4_boundary", "locked_q", "phase_candidate",
        "motion_kernel", "stress", "direct_map", "composite_route"
    ))}
    source_ids = {row["gate_id"] for row in source_rows}
    source_structure = len(source_rows) == 9 and source_ids == expected_source_ids and all(row["passed"] == "True" for row in source_rows)
    add(checks, "VAL4948_17_source_rows", "nine source and stress decisions", sorted(expected_source_ids), sorted(source_ids), source_structure)
    source_map = {row["gate_id"]: row for row in source_rows}
    decisions_ok = (
        source_map["SRCG4948_00_universal_length"]["decision"] == "PASS_SYMBOLIC_UNIVERSAL_SCALE"
        and source_map["SRCG4948_01_source_amplitude"]["decision"] == "DIRECT_CLASSICAL_SOURCE_REJECTED"
        and source_map["SRCG4948_06_stress"]["decision"] == "ACTIVATION_STRESS_NOT_DERIVED"
        and source_map["SRCG4948_07_direct_map"]["decision"] == "DIRECT_ONE_POINT_HESSIAN_MAP_REJECTED"
        and source_map["SRCG4948_08_composite_route"]["decision"] == "TWO_PI_COMPOSITE_ROUTE_SELECTED_FOR_DERIVATION"
    )
    add(checks, "VAL4948_18_source_decisions", "direct route rejected and 2PI selected", True, decisions_ok, decisions_ok)

    composite = tables["composite"]
    expected_composite_ids = {f"2PI4948_{index:02d}_{suffix}" for index, suffix in enumerate((
        "variables", "action", "Dyson", "state", "source", "occupation", "transitions", "stress", "Ward", "local_limit", "empirical"
    ))}
    composite_ids = {row["contract_id"] for row in composite}
    composite_ok = len(composite) == 11 and composite_ids == expected_composite_ids and all(row["passed"] == "True" for row in composite)
    add(checks, "VAL4948_19_composite_rows", "eleven 2PI contract rows", sorted(expected_composite_ids), sorted(composite_ids), composite_ok)
    composite_map = {row["contract_id"]: row for row in composite}
    contract_boundaries = (
        composite_map["2PI4948_02_Dyson"]["current_status"] == "EQUATION_DEFINED_NOT_SOLVED"
        and composite_map["2PI4948_07_stress"]["current_status"] == "VARIATIONAL_STRESS_DEFINITION_DERIVED_NUMERIC_PROFILE_OPEN"
        and composite_map["2PI4948_08_Ward"]["current_status"] == "WARD_CONTRACT_DEFINED"
        and composite_map["2PI4948_10_empirical"]["current_status"] == "EMPIRICAL_EXECUTION_DEFERRED_UNTIL_STRESS_EXISTS"
    )
    add(checks, "VAL4948_20_contract_boundary", "2PI equation and stress boundaries", True, contract_boundaries, contract_boundaries)

    galaxy = tables["galaxy"]
    galaxy_row = galaxy[0] if len(galaxy) == 1 else {}
    snapshot_ok = (
        len(galaxy) == 1
        and galaxy_row.get("head") == EXPECTED_GALAXY_HEAD
        and galaxy_row.get("expected_head") == EXPECTED_GALAXY_HEAD
        and galaxy_row.get("working_tree_clean") == "True"
        and galaxy_row.get("repository_modified_by_checkpoint") == "False"
        and math.isclose(float(galaxy_row.get("locked_q", "nan")), 0.77, rel_tol=0.0, abs_tol=1e-15)
    )
    add(checks, "VAL4948_21_snapshot", "read-only galaxy snapshot", True, galaxy_row, snapshot_ok)
    git_head = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    git_status = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "status", "--porcelain"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    add(checks, "VAL4948_22_galaxy_runtime", "galaxy clone head unchanged and clean", [EXPECTED_GALAXY_HEAD, ""], [git_head, git_status], git_head == EXPECTED_GALAXY_HEAD and not git_status)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["projective_logistic_shape_from_parent_eigenmode_derived"]
        and boundary["natural_radial_shell_log_derivative_derived"]
        and boundary["two_PI_composite_contract_defined"]
        and not boundary["locked_galaxy_q_predicted_by_parent_mass_mode"]
        and not boundary["galaxy_phase_q_proved_identical_to_locked_support_q"]
        and not boundary["source_dependent_Cn_Cb_derived"]
        and not boundary["activation_stress_tensor_calculated"]
        and not boundary["direct_one_point_Hessian_to_galaxy_map"]
        and not boundary["two_PI_composite_disk_solution_calculated"]
        and not boundary["galaxy_repository_modified"]
        and not boundary["full_MTS_galaxy_unification"]
    )
    add(checks, "VAL4948_23_boundary", "claim boundary is disciplined", True, boundary, boundary_ok)

    claim = next((row for row in read_csv(CLAIMS) if row["claim_id"] == "L-790"), None)
    claim_ok = bool(claim) and "private_nonclaim" in claim["status"] and NEXT_TARGET in claim["next_test"] and "FULL_MTS_FALSE" in claim["notes"]
    add(checks, "VAL4948_24_claim", "claim L-790 registered", True, claim, claim_ok)
    expected_variables = {
        "ProjectiveOccupation4948_MTS", "ParentMassExponent4948_MTS",
        "ParentO4BoundaryExponent4948_MTS", "CanonicalGalaxySupport4948_MTS",
        "UniversalGapTransition4948_MTS", "SourceAmplitudeObstruction4948_MTS",
        "Composite2PIOccupation4948_MTS", "PredictivityStatus4948_MTS",
    }
    variable_rows = [row for row in read_csv(VARIABLES) if row["symbol"] in expected_variables]
    add(checks, "VAL4948_25_variables", "eight variables registered", sorted(expected_variables), sorted(row["symbol"] for row in variable_rows), len(variable_rows) == 8 and {row["symbol"] for row in variable_rows} == expected_variables)

    document_markers = {
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT) and NEXT_TARGET in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE) and NEXT_TARGET in text(FORMAL_NOTE),
        "equation": "## 1.241 Projective Hessian occupations and the composite stress interface" in text(EQUATIONS),
        "red_team": "## 192. An eigenvalue is not a populated galaxy source" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4948_26_documents", "all formal document markers", {key: True for key in document_markers}, document_markers, all(document_markers.values()))
    equation_text = text(EQUATIONS)
    equation_ok = all(token in equation_text for token in (
        "dn/d ln R=theta n(1-n)", "db/d ln R=-lambda b(1-b)",
        "ell_gap=sqrt(G_N/J_gap)", "G^-1=D^-1+2 delta Gamma_2/delta G",
    ))
    add(checks, "VAL4948_27_equation", "equation 1.241 carries full interface", True, equation_ok, equation_ok)
    red_text = text(RED_TEAM)
    red_ok = all(token in red_text for token in (
        "do not identify the locked support q", "do not equate a Hessian eigenvalue",
        "do not fit SPARC before", "do not promote the 2PI contract",
    ))
    add(checks, "VAL4948_28_red_team", "red-team prohibitions retained", True, red_ok, red_ok)

    placeholder_tokens = ("MISSING_", "PLACEHOLDER", "TODO", "TBD")
    scan_paths = [RESULT_JSON, LOGISTIC_CSV, EXPONENT_CSV, SOURCE_GATE_CSV, COMPOSITE_CSV, GALAXY_SNAPSHOT_CSV, CHECKPOINT, FORMAL_NOTE]
    placeholders = {
        str(path): token
        for path in scan_paths
        for token in placeholder_tokens
        if token in text(path)
    }
    add(checks, "VAL4948_29_placeholders", "no placeholder markers", {}, placeholders, not placeholders)
    provenance_text = text(PROVENANCE)
    provenance_ok = all(token in provenance_text for token in (
        "https://github.com/Martin123132/MTS-Galaxy-Lab-",
        "https://arxiv.org/abs/hep-ph/0409233",
        EXPECTED_GALAXY_HEAD,
        "valid_for_full_MTS_claim=False",
    ))
    add(checks, "VAL4948_30_provenance", "web and local provenance recorded", True, provenance_ok, provenance_ok)
    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4948_31_pycache", "no scripts pycache", [], pycache, not pycache)

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
