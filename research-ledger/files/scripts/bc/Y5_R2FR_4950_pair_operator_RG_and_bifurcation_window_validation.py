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
SOURCE = POST / "source-intake" / "functional_rg" / "4950"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4950_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4950_pair_operator_RG_and_bifurcation_window.py"
RESULT_JSON = SOURCE / "pair_operator_RG_and_bifurcation_results.json"
GENERATION_CSV = SOURCE / "pair_operator_generation_and_RG_closure.csv"
BIFURCATION_CSV = SOURCE / "stabilized_pair_bifurcation_law.csv"
LOCAL_CSV = SOURCE / "local_spherical_pair_thresholds.csv"
SPARC_WINDOW_CSV = SOURCE / "SPARC_spherical_pair_window.csv"
POTENTIAL_CSV = SOURCE / "SPARC_baryonic_potential_depth_proxy.csv"
DECISION_CSV = SOURCE / "pair_route_decision.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md"
FORMAL_NOTE = FORMAL / "966-PPC4161-pair-operator-RG-and-bifurcation-window.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
LOCAL_4947 = POST / "source-intake" / "functional_rg" / "4947" / "cross_arena_no_retuning_matrix.csv"
EXPECTED_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"
RESULT_MARKER = "MTS_4950_PAIR_OPERATOR_RG_AND_BIFURCATION_WINDOW"
CHECKPOINT_MARKER = "MTS_PAIR_OPERATOR_RG_BIFURCATION_WINDOW_4950"
FORMAL_MARKER = "PPC4161_PAIR_OPERATOR_RG_BIFURCATION_4950"
PROVENANCE_MARKER = "MTS_PAIR_OPERATOR_RG_BIFURCATION_PROVENANCE_4950"
NEXT_TARGET = "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md"

LIGHT_SPEED_KM_S = 299_792.458
LIGHT_SPEED_M_S = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR = 1.054571817e-34
PLANCK_LENGTH = math.sqrt(HBAR * NEWTON_G / LIGHT_SPEED_M_S**3)
KPC = 3.085677581491367e19

HASH_LOCKS = {
    MAIN_SCRIPT: "24b800e16411041db722a0c28f680e1fe3221c5b5eb8a9188280c12489d81987",
    RESULT_JSON: "9243cf84c42036cddb29a267e6d425cc0f443d74410af11965542e0470860860",
    GENERATION_CSV: "83632ff3b05c51cade8befdb04689d93859697bccdd2faf3189fb68a58b441f2",
    BIFURCATION_CSV: "d0a275a96335373c11c1ee0d57985ad08b9df64ea9699355b95f6c7cde96695d",
    LOCAL_CSV: "4b39f5ec00100c8b38b467c836908bef7431d778c342374d540a9412c579c07d",
    SPARC_WINDOW_CSV: "6f88060429ee774b4e675a86b721fff9444a11c733562f1228ea66faa3c09acf",
    POTENTIAL_CSV: "02b1c2d790b67802bbc45cc52953af5e2a0dfb9a7773e6d3c169c5c5477e330e",
    DECISION_CSV: "4cff50abbf0a25491a1495621d84807ea46e1a179334acc28a33663532526b52",
    GALAXY_SNAPSHOT_CSV: "9c5c8ca72a3279e3b50f280f07ba0c056d2c148ae84d6ed78c83dc4a8d7eb613",
    PROVENANCE: "135660d20ecd0726f4baf83011533dca7645f925c627e9bde98fac7f5825605a",
    CHECKPOINT: "64188638f5d19e125e5c1305cce898332267295b26625c1492610a3c529774cf",
    FORMAL_NOTE: "04fe9b54423c4d91af96b5c5970ee84aecf0b31e70b7f7211a86cc02fcca9255",
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


def first_root(mu: float) -> float:
    if mu == 0.0:
        return math.pi / 2.0
    low = math.pi / 2.0
    high = math.pi - 1.0e-13
    for _ in range(180):
        middle = (low + high) / 2.0
        if middle / math.tan(middle) + mu > 0.0:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def threshold(radius_m: float, compactness: float, compton_length_m: float) -> tuple[float, float, float]:
    mu = 0.0 if math.isinf(compton_length_m) else radius_m / compton_length_m
    root = first_root(mu)
    return (mu**2 + root**2) / (6.0 * compactness), mu, root


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
    add(checks, "VAL4950_01_paths", "locked paths exist", [], missing, not missing)
    bad_hashes = {
        str(path): [expected, digest(path)]
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4950_02_hashes", "locked hashes match", {}, bad_hashes, not bad_hashes)
    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as exc:
            compile_errors.append(f"{path.name}:{exc}")
    add(checks, "VAL4950_03_compile", "scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4950_04_marker", "result marker", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)
    internal_failures = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4950_05_internal", "research checks pass", [], internal_failures, not internal_failures)
    source_errors = []
    for raw, expected in result["source_hashes"].items():
        path = source_path(raw)
        if not path.exists() or digest(path) != expected:
            source_errors.append(raw)
    add(checks, "VAL4950_06_sources", "source paths and hashes", [], source_errors, not source_errors)
    clause_failures = [name for name, passed in result["source_clause_checks"].items() if not passed]
    add(checks, "VAL4950_07_clauses", "authoritative source clauses", [], clause_failures, not clause_failures)

    tables = {
        "generation": read_csv(GENERATION_CSV),
        "bifurcation": read_csv(BIFURCATION_CSV),
        "local": read_csv(LOCAL_CSV),
        "sparc": read_csv(SPARC_WINDOW_CSV),
        "potential": read_csv(POTENTIAL_CSV),
        "decision": read_csv(DECISION_CSV),
        "galaxy": read_csv(GALAXY_SNAPSHOT_CSV),
    }
    malformed = {
        f"{name}:{index}": row
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4950_08_csv", "all generated CSV rows parse", {}, malformed, not malformed)
    invalid_claim_rows = [
        f"{name}:{index}"
        for name, rows in tables.items()
        for index, row in enumerate(rows)
        if row.get("valid_for_full_MTS_claim") != "False"
    ]
    add(checks, "VAL4950_09_nonclaim", "all rows retain full-MTS nonclaim", [], invalid_claim_rows, not invalid_claim_rows)

    generation = tables["generation"]
    expected_generation_ids = {f"GEN4950_{index:02d}_{suffix}" for index, suffix in enumerate((
        "even_basis", "VF_flow", "beta_xi", "minimal_xi", "direct_Tpsi2",
        "trace_basis", "X2", "quartic", "O4", "closure"
    ))}
    generation_ids = {row["generation_id"] for row in generation}
    generation_ok = len(generation) == 10 and generation_ids == expected_generation_ids and all(row["passed"] == "True" for row in generation)
    add(checks, "VAL4950_10_generation", "ten operator-generation rows", sorted(expected_generation_ids), sorted(generation_ids), generation_ok)
    generation_map = {row["generation_id"]: row for row in generation}
    rg_boundary = (
        generation_map["GEN4950_02_beta_xi"]["current_status"] == "ONE_LOOP_RG_IDENTITY_DERIVED"
        and generation_map["GEN4950_03_minimal_xi"]["current_status"] == "NOT_INVARIANT_IF_LAMBDA_NONZERO"
        and generation_map["GEN4950_04_direct_Tpsi2"]["current_status"] == "DIRECT_PARENT_TERM_EXCLUDED"
        and generation_map["GEN4950_06_X2"]["current_status"] == "GENERATED_CHANNEL_PARENT_SCHEME_COEFFICIENT_OPEN_NO_STATIC_MASS_SOURCE"
        and generation_map["GEN4950_09_closure"]["current_status"] == "CURRENT_PARENT_PAIR_SECTOR_NOT_RG_CLOSED"
    )
    add(checks, "VAL4950_11_RG_boundary", "RG closure and operator boundaries", True, rg_boundary, rg_boundary)
    beta_identity = (
        "beta_lambda=3lambda^2/(4pi)^2" in generation_map["GEN4950_02_beta_xi"]["equation_or_flow"]
        and "beta_xi=lambda(xi-1/6)/(4pi)^2" in generation_map["GEN4950_02_beta_xi"]["equation_or_flow"]
        and "-lambda/[6(4pi)^2]" in generation_map["GEN4950_03_minimal_xi"]["equation_or_flow"]
    )
    add(checks, "VAL4950_12_beta", "one-loop beta identities", True, beta_identity, beta_identity)

    bifurcation = tables["bifurcation"]
    expected_bifurcation_ids = {f"BIF4950_{index:02d}_{suffix}" for index, suffix in enumerate((
        "action", "trace_reduction", "Rayleigh", "top_hat", "massless", "stabilization", "energy", "local_GR"
    ))}
    bifurcation_ids = {row["derivation_id"] for row in bifurcation}
    bifurcation_ok = len(bifurcation) == 8 and bifurcation_ids == expected_bifurcation_ids and all(row["passed"] == "True" for row in bifurcation)
    add(checks, "VAL4950_13_bifurcation", "eight bifurcation derivation rows", sorted(expected_bifurcation_ids), sorted(bifurcation_ids), bifurcation_ok)
    roots = [first_root(mu) for mu in (0.0, 0.1, 1.0, 10.0, 100.0)]
    root_residuals = [abs(root / math.tan(root) + mu) for root, mu in zip(roots[1:], (0.1, 1.0, 10.0, 100.0))]
    root_ok = math.isclose(roots[0], math.pi / 2.0, abs_tol=1e-15) and max(root_residuals) < 2e-10 and all(left < right for left, right in zip(roots, roots[1:]))
    add(checks, "VAL4950_14_roots", "zero-mode roots independently solved", "ordered with residual <2e-10", {"roots": roots, "residuals": root_residuals}, root_ok)

    compton_cases = {
        "massless": math.inf,
        "lambda_100_kpc": 100.0 * KPC,
        "lambda_10_kpc": 10.0 * KPC,
        "lambda_1_kpc": 1.0 * KPC,
    }
    local_source = {
        row["system"]: row
        for row in read_csv(LOCAL_4947)
        if row["system"] in {"Earth", "Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star"}
    }
    local = tables["local"]
    local_map = {(row["compton_case"], row["system"]): row for row in local}
    local_errors: list[str] = []
    independent_local: dict[str, dict[str, float]] = {}
    for case, compton_length in compton_cases.items():
        independent_local[case] = {}
        for system, source in local_source.items():
            expected, mu, root = threshold(float(source["radius_m"]), float(source["compactness_GM_over_rc2"]), compton_length)
            independent_local[case][system] = expected
            row = local_map.get((case, system))
            if row is None or not (
                math.isclose(float(row["Bcrit_spherical"]), expected, rel_tol=3e-15)
                and math.isclose(float(row["mu_mL"]), mu, rel_tol=3e-15, abs_tol=1e-30)
                and math.isclose(float(row["threshold_root_x"]), root, rel_tol=3e-15)
            ):
                local_errors.append(case + ":" + system)
    add(checks, "VAL4950_15_local", "sixteen local thresholds recomputed", [], local_errors, len(local) == 16 and not local_errors)
    expected_massless = {
        "Earth": 590741454.2594202,
        "Sun": 193743.5022292329,
        "one_solar_mass_white_dwarf": 1949.40996924627,
        "1.4_solar_mass_12km_neutron_star": 2.387032615403596,
    }
    massless_ok = all(math.isclose(independent_local["massless"][key], value, rel_tol=2e-15) for key, value in expected_massless.items())
    add(checks, "VAL4950_16_massless_local", "massless local ceilings", expected_massless, independent_local["massless"], massless_ok)

    samples = load_samples()
    sparc = tables["sparc"]
    sparc_map = {(row["galaxy"], row["compton_case"]): row for row in sparc}
    sparc_errors: list[str] = []
    independent_thresholds: dict[str, list[float]] = {case: [] for case in compton_cases}
    independent_potential: dict[str, tuple[float, float]] = {}
    for sample in samples:
        name = sample["name"].removesuffix("_rotmod.dat")
        points = parse_points(sample["text"])
        baryonic = []
        for point in points:
            radius, _, _, vgas, vdisk, vbulge = point[:6]
            vbar2 = max(vgas * abs(vgas) + 0.5 * vdisk**2 + 0.7 * vbulge**2, 0.0)
            baryonic.append((radius, vbar2))
        compactness = baryonic[-1][1] / LIGHT_SPEED_KM_S**2
        for case, compton_length in compton_cases.items():
            expected, mu, root = threshold(baryonic[-1][0] * KPC, compactness, compton_length)
            independent_thresholds[case].append(expected)
            row = sparc_map.get((name, case))
            if row is None or not (
                math.isclose(float(row["Bcrit_spherical"]), expected, rel_tol=4e-15)
                and math.isclose(float(row["mu_mL"]), mu, rel_tol=4e-15, abs_tol=1e-30)
                and math.isclose(float(row["threshold_root_x"]), root, rel_tol=4e-15)
                and row["universal_window_vs_Sun"] == "False"
                and row["universal_window_vs_white_dwarf"] == "False"
                and row["universal_window_vs_neutron_star"] == "False"
            ):
                sparc_errors.append(name + ":" + case)
        radial_integral = sum(
            0.5 * (left[1] + right[1]) * math.log(right[0] / left[0])
            for left, right in zip(baryonic, baryonic[1:])
        )
        phi = 0.5 * baryonic[0][1] + radial_integral + baryonic[-1][1]
        floor = 1.0 / (2.0 * phi / LIGHT_SPEED_KM_S**2)
        independent_potential[name] = (phi, floor)
    add(checks, "VAL4950_17_sparc", "700 public thresholds independently recomputed", [], sparc_errors, len(samples) == 175 and len(sparc) == 700 and not sparc_errors)
    massless_values = independent_thresholds["massless"]
    massless_stats = {"min": min(massless_values), "median": statistics.median(massless_values), "max": max(massless_values)}
    expected_massless_stats = {"min": 910410.8776332821, "median": 17840079.957102247, "max": 468897347.42541593}
    stats_ok = all(math.isclose(massless_stats[key], value, rel_tol=2e-15) for key, value in expected_massless_stats.items())
    add(checks, "VAL4950_18_sparc_stats", "massless public threshold statistics", expected_massless_stats, massless_stats, stats_ok)
    window_counts = {
        column: sum(row[column] == "True" for row in sparc)
        for column in ("universal_window_vs_Sun", "universal_window_vs_white_dwarf", "universal_window_vs_neutron_star")
    }
    add(checks, "VAL4950_19_windows", "all 2100 local-window booleans false", {key: 0 for key in window_counts}, window_counts, all(value == 0 for value in window_counts.values()))

    potential = tables["potential"]
    potential_map = {row["galaxy"]: row for row in potential}
    potential_errors: list[str] = []
    for name, (phi, floor) in independent_potential.items():
        row = potential_map.get(name)
        if row is None or not (
            math.isclose(float(row["baryonic_potential_depth_proxy_km2_s2"]), phi, rel_tol=4e-15)
            and math.isclose(float(row["B_no_bound_floor_proxy"]), floor, rel_tol=4e-15)
        ):
            potential_errors.append(name)
    add(checks, "VAL4950_20_potential", "175 potential proxies independently recomputed", [], potential_errors, len(potential) == 175 and not potential_errors)
    potential_floors = [value[1] for value in independent_potential.values()]
    minimum_potential = min(potential_floors)
    potential_ratio = minimum_potential / independent_local["massless"]["one_solar_mass_white_dwarf"]
    potential_ok = math.isclose(minimum_potential, 143202.58570940062, rel_tol=2e-15) and potential_ratio > 73.0
    add(checks, "VAL4950_21_potential_floor", "potential proxy remains above white-dwarf ceiling", ">73", potential_ratio, potential_ok)

    decision = tables["decision"]
    expected_decision_ids = {f"DEC4950_{index:02d}_{suffix}" for index, suffix in enumerate((
        "RG_closure", "direct_trace", "xi_zero", "X2", "spherical_window",
        "potential_proxy", "stabilizer", "local_GR", "route", "next"
    ))}
    decision_ids = {row["decision_id"] for row in decision}
    decision_ok = len(decision) == 10 and decision_ids == expected_decision_ids and all(row["passed"] == "True" for row in decision)
    add(checks, "VAL4950_22_decisions", "ten route decisions", sorted(expected_decision_ids), sorted(decision_ids), decision_ok)
    decision_map = {row["decision_id"]: row for row in decision}
    route_ok = (
        decision_map["DEC4950_04_spherical_window"]["decision"] == "UNIVERSAL_SPHERICAL_PAIR_WINDOW_REJECTED"
        and decision_map["DEC4950_08_route"]["decision"] == "CURRENT_MINIMAL_LOCAL_PAIR_ROUTE_REJECTED"
        and decision_map["DEC4950_09_next"]["decision"] == "ADVANCE_TO_COUPLED_VFZX2_PARENT_FLOW"
    )
    add(checks, "VAL4950_23_route", "minimal pair route rejected and next selected", True, route_ok, route_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["curved_scalar_RG_requires_FpsiR"]
        and boundary["one_loop_beta_xi_derived"]
        and boundary["direct_Tpsi2_excluded_by_fixed_metric_parent"]
        and boundary["X2_scattering_channel_recognized"]
        and boundary["stabilized_bifurcation_law_derived"]
        and boundary["public_spherical_window_executed"]
        and not boundary["universal_spherical_pair_window_exists"]
        and not boundary["full_axisymmetric_3D_spectrum_solved"]
        and not boundary["xi_lambda_X2_parent_values_predicted"]
        and not boundary["current_minimal_local_pair_route_viable"]
        and not boundary["4947_local_GR_automatically_preserved_after_pair_extension"]
        and not boundary["full_MTS_galaxy_unification"]
        and not boundary["galaxy_repository_modified"]
    )
    add(checks, "VAL4950_24_boundary", "claim boundary", True, boundary, boundary_ok)

    galaxy = tables["galaxy"]
    snapshot = galaxy[0] if len(galaxy) == 1 else {}
    snapshot_ok = len(galaxy) == 1 and snapshot.get("head") == EXPECTED_HEAD and snapshot.get("working_tree_clean") == "True" and snapshot.get("sample_count") == "175" and snapshot.get("repository_modified_by_checkpoint") == "False"
    add(checks, "VAL4950_25_snapshot", "galaxy read-only snapshot", True, snapshot, snapshot_ok)
    runtime_head = subprocess.run(["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    runtime_status = subprocess.run(["git", "-C", str(GALAXY_REPO), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    add(checks, "VAL4950_26_runtime", "galaxy clone remains locked and clean", [EXPECTED_HEAD, ""], [runtime_head, runtime_status], runtime_head == EXPECTED_HEAD and not runtime_status)

    claim = next((row for row in read_csv(CLAIMS) if row["claim_id"] == "L-792"), None)
    claim_ok = bool(claim) and "private_nonclaim" in claim["status"] and NEXT_TARGET in claim["next_test"] and "FULL_MTS_FALSE" in claim["notes"]
    add(checks, "VAL4950_27_claim", "claim L-792 registered", True, claim, claim_ok)
    expected_variables = {
        "CurvedMotionFunctional4950_MTS", "NonminimalXiFlow4950_MTS",
        "EffectivePairCoefficient4950_MTS", "PairRayleighOperator4950_MTS",
        "TopHatPairThreshold4950_MTS", "StabilizedPairAmplitude4950_MTS",
        "GalaxyLocalPairWindow4950_MTS", "PredictivityStatus4950_MTS",
    }
    variable_rows = [row for row in read_csv(VARIABLES) if row["symbol"] in expected_variables]
    add(checks, "VAL4950_28_variables", "eight variables registered", sorted(expected_variables), sorted(row["symbol"] for row in variable_rows), len(variable_rows) == 8 and {row["symbol"] for row in variable_rows} == expected_variables)

    document_markers = {
        "checkpoint": CHECKPOINT_MARKER in text(CHECKPOINT) and NEXT_TARGET in text(CHECKPOINT),
        "formal": FORMAL_MARKER in text(FORMAL_NOTE) and NEXT_TARGET in text(FORMAL_NOTE),
        "equation": "## 1.243 Curved pair-operator flow and environmental zero mode" in text(EQUATIONS),
        "red_team": "## 194. A symmetry-allowed pair operator is not a viable source" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME) and NEXT_TARGET in text(RESUME),
        "provenance": PROVENANCE_MARKER in text(PROVENANCE),
    }
    add(checks, "VAL4950_29_documents", "all formal document markers", {key: True for key in document_markers}, document_markers, all(document_markers.values()))
    checkpoint_tokens = (
        "beta_xi=lambda(xi-1/6)/(4pi)^2",
        "B_crit=(mu^2+x^2)/(6C)",
        "minimum galaxy B_crit =9.10410878e5",
        "current minimal local pair route                  = rejected",
    )
    checkpoint_content = all(token in text(CHECKPOINT) for token in checkpoint_tokens)
    add(checks, "VAL4950_30_content", "checkpoint decisive equations and result", True, checkpoint_content, checkpoint_content)
    provenance_ok = all(token in text(PROVENANCE) for token in (
        "https://arxiv.org/abs/1810.06395",
        "https://arxiv.org/abs/1711.02224",
        "https://github.com/Martin123132/MTS-Galaxy-Lab-",
        EXPECTED_HEAD,
        "valid_for_full_MTS_claim=False",
    ))
    add(checks, "VAL4950_31_provenance", "primary and data provenance recorded", True, provenance_ok, provenance_ok)

    scan_paths = [RESULT_JSON, GENERATION_CSV, BIFURCATION_CSV, LOCAL_CSV, SPARC_WINDOW_CSV, POTENTIAL_CSV, DECISION_CSV, CHECKPOINT, FORMAL_NOTE]
    placeholder_tokens = ("MISSING_", "PLACEHOLDER", "TODO", "TBD")
    placeholders = {str(path): token for path in scan_paths for token in placeholder_tokens if token in text(path)}
    add(checks, "VAL4950_32_placeholders", "no placeholder markers", {}, placeholders, not placeholders)
    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4950_33_pycache", "no scripts pycache", [], pycache, not pycache)

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
