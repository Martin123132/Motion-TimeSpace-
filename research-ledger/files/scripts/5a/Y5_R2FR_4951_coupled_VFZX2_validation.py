from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4951"
OUTPUT = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4951_VALIDATION.csv"
)

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4951_coupled_VFZX2_fixed_and_running_gate.py"
RESULT_JSON = SOURCE / "coupled_VFZX2_fixed_and_running_gate_results.json"
SOURCE_AUDIT_CSV = SOURCE / "coupled_VFZX2_linear_source_audit.csv"
HESSIAN_CSV = SOURCE / "pair_onset_Hessian_projection.csv"
FIXED_POINT_CSV = SOURCE / "parent_and_source_fixed_point_indices.csv"
RUNNING_CSV = SOURCE / "running_pair_window_gate.csv"
DECISION_CSV = SOURCE / "pair_sector_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = (
    POST
    / "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md"
)
FORMAL_NOTE = FORMAL / "967-PPC4161-VFZX2-shift-source-and-static-pair-route-decision.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

LOCAL_THRESHOLDS_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4950"
    / "local_spherical_pair_thresholds.csv"
)
SPARC_THRESHOLDS_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4950"
    / "SPARC_spherical_pair_window.csv"
)
GALAXY_REPO = Path(r"D:\g4948")
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"

RESULT_MARKER = "MTS_4951_COUPLED_VFZX2_FIXED_AND_RUNNING_GATE"
FORMAL_MARKER = "PPC4161_VFZX2_SHIFT_SOURCE_STATIC_PAIR_DECISION_4951"
NEXT_TARGET = "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md"
KPC_METRES = 3.085677581491367e19

HASH_LOCKS = {
    MAIN_SCRIPT: "c6093a904d20c74c71443866b4ecf3ac4e125c394971065b5252f3b45bc52f9d",
    RESULT_JSON: "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c",
    SOURCE_AUDIT_CSV: "b2b63e37a8603a9d16cd42103ec2f08c6a28a4960debd045950ba28343293f2f",
    HESSIAN_CSV: "895c589b41f4c428e21dfda09a1a739dba5016ef1a647cf955ae444ff25d38f0",
    FIXED_POINT_CSV: "39f065d2de1ae4ffa298ad0e40b782f955c530ae9b7d5bf83c8e29763f8b53ae",
    RUNNING_CSV: "b8be4170d757b1d5de2de41a08faff2f14c161b529a38f4ccbd518f17636eb8d",
    DECISION_CSV: "a5621de0008cc800c36cdcc353e937fdb2db7744ff4c4a8f1a5128f83ca6b478",
    PROVENANCE: "88d0737feb6b0de6d2a178772852ea0b251e88e9389fc9c1077733ddcc4baff9",
    CHECKPOINT: "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131",
    FORMAL_NOTE: "43fddc9f460e47165b92ddd795073bb162bad188c5e3c5af54ff3367cd8353c0",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_path(raw: str) -> Path:
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else ROOT / candidate


def add(
    rows: list[dict[str, Any]],
    validation_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": validation_id,
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
    add(checks, "VAL4951_01_paths", "locked paths exist", [], missing, not missing)
    hash_errors = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4951_02_hashes", "locked hashes match", {}, hash_errors, not hash_errors)

    compile_errors: list[str] = []
    for script_path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(script_path), str(script_path), "exec")
        except Exception as error:
            compile_errors.append(f"{script_path.name}:{error}")
    add(checks, "VAL4951_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(
        checks,
        "VAL4951_04_marker",
        "result marker",
        RESULT_MARKER,
        result.get("marker"),
        result.get("marker") == RESULT_MARKER,
    )
    internal_failures = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4951_05_internal", "research checks pass", [], internal_failures, not internal_failures)

    source_errors: list[str] = []
    for raw_path, expected_hash in result["source_hashes"].items():
        path = source_path(raw_path)
        if not path.exists() or digest(path) != expected_hash:
            source_errors.append(raw_path)
    add(checks, "VAL4951_06_sources", "source paths and hashes", [], source_errors, not source_errors)
    source_clause_failures = [
        name for name, passed in result["source_contract"].items() if not passed
    ]
    add(
        checks,
        "VAL4951_07_source_clauses",
        "primary source clauses",
        [],
        source_clause_failures,
        not source_clause_failures,
    )

    tables = {
        "source": read_csv(SOURCE_AUDIT_CSV),
        "hessian": read_csv(HESSIAN_CSV),
        "fixed": read_csv(FIXED_POINT_CSV),
        "running": read_csv(RUNNING_CSV),
        "decision": read_csv(DECISION_CSV),
    }
    malformed = {
        f"{table_name}:{index}": row
        for table_name, rows in tables.items()
        for index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4951_08_csv", "all generated CSV rows parse", {}, malformed, not malformed)
    promoted = [
        f"{table_name}:{index}"
        for table_name, rows in tables.items()
        for index, row in enumerate(rows)
        if row.get("valid_for_full_MTS_claim") != "False"
    ]
    add(checks, "VAL4951_09_nonclaim", "all output rows remain nonclaim", [], promoted, not promoted)

    source_map = {row["coordinate"]: row for row in tables["source"]}
    expected_source_coordinates = {
        "m2=V''(0)/Z0",
        "lambda4=V''''(0)/Z0^2",
        "xi=F''(0)/Z0",
        "z2=Z''(0)/Z0",
        "c_ess X2",
    }
    source_ok = (
        set(source_map) == expected_source_coordinates
        and all(
            source_map[coordinate]["additive_parent_source_at_GMFP"] == "0"
            for coordinate in expected_source_coordinates - {"c_ess X2"}
        )
        and source_map["c_ess X2"]["linear_onset_entry"] == "False"
    )
    add(
        checks,
        "VAL4951_10_zero_source",
        "five-coordinate source theorem",
        sorted(expected_source_coordinates),
        sorted(source_map),
        source_ok,
    )

    hessian_map = {row["term"]: row for row in tables["hessian"]}
    silent_terms = ("lambda4 psi4/24", "z2 psi2 X/2", "c_ess X2")
    hessian_ok = (
        hessian_map["complete psi=0 Hessian"]["quadratic_contribution"]
        == "Gamma2=-Z0 box+V''(0)-F''(0)R"
        and all(
            hessian_map[term]["quadratic_contribution"] == "0"
            and hessian_map[term]["enters_static_onset"] == "False"
            for term in silent_terms
        )
    )
    add(checks, "VAL4951_11_hessian_rows", "complete onset Hessian rows", True, hessian_ok, hessian_ok)

    fluctuation, gradient, test_field = sp.symbols("epsilon grad f", real=True)
    mass_squared, pair_coupling, curvature = sp.symbols("m2 xi R", real=True)
    wave_normalization, quartic, wave_curvature, x2_coupling = sp.symbols(
        "Z0 lambda4 z2 cX2", real=True
    )
    kinetic = fluctuation**2 * gradient / 2
    density = (
        wave_normalization * kinetic
        + wave_curvature * fluctuation**2 * test_field**2 * kinetic / 2
        + x2_coupling * kinetic**2
        + mass_squared * fluctuation**2 * test_field**2 / 2
        + quartic * fluctuation**4 * test_field**4 / 24
        - pair_coupling * curvature * fluctuation**2 * test_field**2 / 2
    )
    independent_quadratic = sp.expand(density).coeff(fluctuation, 2)
    expected_quadratic = (
        wave_normalization * gradient
        + (mass_squared - pair_coupling * curvature) * test_field**2
    ) / 2
    symbolic_hessian_ok = sp.simplify(independent_quadratic - expected_quadratic) == 0
    add(
        checks,
        "VAL4951_12_hessian_symbolic",
        "quadratic density independently expanded",
        str(expected_quadratic),
        str(independent_quadratic),
        symbolic_hessian_ok,
    )

    fixed_rows = tables["fixed"]
    parent_mass = next(row for row in fixed_rows if row["coordinate"] == "mass m2")
    parent_quartic = next(row for row in fixed_rows if row["coordinate"] == "quartic lambda4")
    parent_index_ok = (
        math.isclose(float(parent_mass["critical_exponent"]), 1.8466610449470542, rel_tol=2e-15)
        and parent_mass["classification"] == "RELEVANT"
        and math.isclose(float(parent_quartic["critical_exponent"]), -0.1533389550529459, rel_tol=2e-15)
        and parent_quartic["classification"] == "IRRELEVANT"
    )
    add(checks, "VAL4951_13_parent_indices", "parent mass and quartic indices", True, parent_index_ok, parent_index_ok)
    fp1_row = next(row for row in fixed_rows if row["fixed_point"] == "FP1")
    fp2_row = next(row for row in fixed_rows if row["fixed_point"] == "FP2")
    comparator_ok = (
        fp1_row["critical_exponent"] == "4;2;2;-0;-0"
        and "F''=1/3" in fp2_row["fixed_value"]
        and all(value == "0" for value in result["source_comparator"]["physical_gauge_FP1_residual"])
        and all(value == "0" for value in result["source_comparator"]["physical_gauge_FP2_residual"])
    )
    add(checks, "VAL4951_14_comparators", "physical-gauge fixed points exact", True, comparator_ok, comparator_ok)

    fixed_beta_lambda = 3 * quartic**2 / (16 * sp.pi**2)
    fixed_beta_xi = quartic * (pair_coupling - sp.Rational(1, 6)) / (16 * sp.pi**2)
    source_beta_lambda = sp.sympify(
        result["source_comparator"]["fixed_background_beta_lambda"],
        locals={"lambda4": quartic, "pi": sp.pi},
    )
    source_beta_xi = sp.sympify(
        result["source_comparator"]["fixed_background_beta_xi"],
        locals={"lambda4": quartic, "xi_pair": pair_coupling, "pi": sp.pi},
    )
    beta_ok = (
        sp.simplify(source_beta_lambda - fixed_beta_lambda) == 0
        and sp.simplify(source_beta_xi - fixed_beta_xi) == 0
    )
    add(checks, "VAL4951_15_betas", "universal beta identities independently built", True, beta_ok, beta_ok)

    local_rows = read_csv(LOCAL_THRESHOLDS_CSV)
    sparc_rows = read_csv(SPARC_THRESHOLDS_CSV)
    local_massless = {
        row["system"]: row for row in local_rows if row["compton_case"] == "massless"
    }
    sparc_massless = [row for row in sparc_rows if row["compton_case"] == "massless"]
    easiest = min(sparc_massless, key=lambda row: float(row["Bcrit_spherical"]))
    threshold_ok = (
        len(sparc_rows) == 700
        and len(sparc_massless) == 175
        and easiest["galaxy"] == "NGC5005"
        and math.isclose(float(easiest["Bcrit_spherical"]), 910410.8776332821, rel_tol=2e-15)
    )
    add(checks, "VAL4951_16_threshold", "easiest galaxy independently selected", True, easiest, threshold_ok)
    window_counts = {
        key: sum(row[key] == "True" for row in sparc_rows)
        for key in (
            "universal_window_vs_Sun",
            "universal_window_vs_white_dwarf",
            "universal_window_vs_neutron_star",
        )
    }
    add(
        checks,
        "VAL4951_17_windows",
        "all 2100 local-window booleans false",
        {key: 0 for key in window_counts},
        window_counts,
        all(value == 0 for value in window_counts.values()),
    )

    running_rows = tables["running"]
    white_dwarf_row = next(
        row for row in running_rows if row["comparison"].endswith("one_solar_mass_white_dwarf")
    )
    neutron_star_row = next(
        row for row in running_rows if row["comparison"].endswith("1.4_solar_mass_12km_neutron_star")
    )
    galaxy_radius = float(easiest["outer_radius_kpc"]) * KPC_METRES
    white_dwarf_threshold = float(
        local_massless["one_solar_mass_white_dwarf"]["Bcrit_spherical"]
    )
    neutron_star_threshold = float(
        local_massless["1.4_solar_mass_12km_neutron_star"]["Bcrit_spherical"]
    )
    expected_white_dwarf_growth = float(easiest["Bcrit_spherical"]) / white_dwarf_threshold
    expected_neutron_star_growth = float(easiest["Bcrit_spherical"]) / neutron_star_threshold
    expected_white_dwarf_exponent = math.log(expected_white_dwarf_growth) / math.log(
        float(local_massless["one_solar_mass_white_dwarf"]["radius_m"]) / galaxy_radius
    )
    expected_neutron_star_exponent = math.log(expected_neutron_star_growth) / math.log(
        float(local_massless["1.4_solar_mass_12km_neutron_star"]["radius_m"]) / galaxy_radius
    )
    running_requirement_ok = (
        math.isclose(float(white_dwarf_row["required_B_IR_growth"]), expected_white_dwarf_growth, rel_tol=2e-15)
        and math.isclose(float(neutron_star_row["required_B_IR_growth"]), expected_neutron_star_growth, rel_tol=2e-15)
        and math.isclose(float(white_dwarf_row["required_average_dlnB_dlnk"]), expected_white_dwarf_exponent, rel_tol=2e-15)
        and math.isclose(float(neutron_star_row["required_average_dlnB_dlnk"]), expected_neutron_star_exponent, rel_tol=2e-15)
    )
    add(
        checks,
        "VAL4951_18_running_requirements",
        "required growth and exponents recomputed",
        {
            "WD_growth": expected_white_dwarf_growth,
            "NS_growth": expected_neutron_star_growth,
            "WD_exponent": expected_white_dwarf_exponent,
            "NS_exponent": expected_neutron_star_exponent,
        },
        {
            "WD_growth": white_dwarf_row["required_B_IR_growth"],
            "NS_growth": neutron_star_row["required_B_IR_growth"],
            "WD_exponent": white_dwarf_row["required_average_dlnB_dlnk"],
            "NS_exponent": neutron_star_row["required_average_dlnB_dlnk"],
        },
        running_requirement_ok,
    )

    trajectory_errors: list[str] = []
    logarithmic_interval = math.log(
        float(local_massless["one_solar_mass_white_dwarf"]["radius_m"]) / galaxy_radius
    )
    beta_coefficient = 3.0 / (16.0 * math.pi**2)
    trajectory_rows = [
        row for row in running_rows if row["comparison"].startswith("analytic_VF_trajectory")
    ]
    for row in trajectory_rows:
        initial_lambda = float(row["lambda_at_local_scale"])
        final_lambda = initial_lambda / (
            1.0 - beta_coefficient * initial_lambda * logarithmic_interval
        )
        expected_ratio = (final_lambda / initial_lambda) ** (1.0 / 3.0)
        if not (
            math.isclose(float(row["lambda_at_galaxy_scale"]), final_lambda, rel_tol=2e-15)
            and math.isclose(float(row["xi_minus_one_sixth_IR_over_local"]), expected_ratio, rel_tol=2e-15)
            and expected_ratio < 1.0
            and row["passes_required_growth"] == "False"
        ):
            trajectory_errors.append(row["comparison"])
    add(
        checks,
        "VAL4951_19_trajectories",
        "four analytic trajectories independently integrated",
        [],
        trajectory_errors,
        len(trajectory_rows) == 4 and not trajectory_errors,
    )

    decision_map = {row["gate"]: row for row in tables["decision"]}
    route_ok = (
        decision_map["common_parent_shift_source"]["result"] == "PASS_ZERO_THEOREM"
        and decision_map["complete_VFZX2_linear_onset"]["result"] == "PASS_EXACT_HESSIAN"
        and decision_map["local_galaxy_spectral_ordering"]["result"] == "FAIL_EMPTY_WINDOW"
        and decision_map["stable_IR_VF_running"]["result"] == "FAIL_WRONG_RUNNING_SIGN"
        and decision_map["4951_route_decision"]["result"]
        == "REJECT_CURRENT_STATIC_VFZX2_GALAXY_BRIDGE"
    )
    add(checks, "VAL4951_20_decision", "route decision follows gates", True, route_ok, route_ok)
    boundary = result["decision"]
    boundary_ok = (
        boundary["coupled_VFZX2_RG_closure_required"]
        and not boundary["current_static_even_pair_galaxy_bridge"]
        and boundary["local_GR_Newton_Maxwell_4947_retained"]
        and boundary["next_target"] == NEXT_TARGET
    )
    add(checks, "VAL4951_21_boundary", "claim boundary", True, boundary, boundary_ok)

    claim = next((row for row in read_csv(CLAIMS) if row["claim_id"] == "L-793"), None)
    claim_ok = (
        bool(claim)
        and "private_nonclaim" in claim["status"]
        and claim["next_test"] == NEXT_TARGET
        and "FULL_MTS_FALSE" in claim["notes"]
    )
    add(checks, "VAL4951_22_claim", "claim L-793 registered", True, claim, claim_ok)
    expected_variables = {
        "ShiftSymmetricPairSurface4951_MTS",
        "PairOnsetHessian4951_MTS",
        "ParentMotionIndices4951_MTS",
        "PhysicalGaugeVFComparator4951_MTS",
        "StableVFIRTrajectory4951_MTS",
        "PairRunningRequirement4951_MTS",
        "StaticVFZX2Decision4951_MTS",
        "PredictivityStatus4951_MTS",
    }
    variable_rows = [
        row for row in read_csv(VARIABLES) if row["symbol"] in expected_variables
    ]
    variable_symbols = {row["symbol"] for row in variable_rows}
    add(
        checks,
        "VAL4951_23_variables",
        "eight variables registered",
        sorted(expected_variables),
        sorted(variable_symbols),
        len(variable_rows) == 8 and variable_symbols == expected_variables,
    )

    document_markers = {
        "checkpoint": FORMAL_MARKER in text(CHECKPOINT) and NEXT_TARGET in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE),
        "equation": "## 1.244 `V-F-Z-X2` shift source, onset Hessian and infrared inversion gate" in text(EQUATIONS),
        "red_team": "## 195. Functional closure does not imply a static source" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
    }
    add(
        checks,
        "VAL4951_24_documents",
        "formal document markers",
        {key: True for key in document_markers},
        document_markers,
        all(document_markers.values()),
    )
    checkpoint_tokens = (
        "beta_m2|0 = beta_lambda4|0 = beta_xi|0 = beta_z2|0 = 0",
        "Gamma_psi_psi=-Z0 box+m2-xi R",
        "Bgal/BWD > 4.67019e2",
        "current static VFZX2 galaxy bridge               = rejected as derived route",
    )
    content_ok = all(token in text(CHECKPOINT) for token in checkpoint_tokens)
    add(checks, "VAL4951_25_content", "decisive equations and result recorded", True, content_ok, content_ok)
    provenance_tokens = (
        "https://arxiv.org/abs/0911.0386",
        "https://arxiv.org/abs/1501.00888",
        "https://arxiv.org/abs/1711.02224",
        "https://arxiv.org/abs/2110.09566",
        "No external fixed-point coordinate is inserted into the MTS parent flow.",
    )
    provenance_ok = all(token in text(PROVENANCE) for token in provenance_tokens)
    add(checks, "VAL4951_26_provenance", "primary provenance and firewall", True, provenance_ok, provenance_ok)

    placeholder_tokens = ("MISSING_", "PLACEHOLDER", "TODO", "TBD")
    scan_paths = [
        RESULT_JSON,
        SOURCE_AUDIT_CSV,
        HESSIAN_CSV,
        FIXED_POINT_CSV,
        RUNNING_CSV,
        DECISION_CSV,
        CHECKPOINT,
        FORMAL_NOTE,
    ]
    placeholders = {
        str(path): token
        for path in scan_paths
        for token in placeholder_tokens
        if token in text(path)
    }
    add(checks, "VAL4951_27_placeholders", "no placeholder markers", {}, placeholders, not placeholders)

    runtime_head = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    runtime_status = subprocess.run(
        ["git", "-C", str(GALAXY_REPO), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    add(
        checks,
        "VAL4951_28_galaxy_repo",
        "galaxy repository remains locked and clean",
        [EXPECTED_GALAXY_HEAD, ""],
        [runtime_head, runtime_status],
        runtime_head == EXPECTED_GALAXY_HEAD and not runtime_status,
    )

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4951_29_pycache", "no scripts pycache", [], pycache, not pycache)

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
