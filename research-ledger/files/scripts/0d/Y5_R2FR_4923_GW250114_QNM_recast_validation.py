from __future__ import annotations

import csv
import importlib.metadata
import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

import h5py
import numpy as np


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
TIMESTAMP = "2026-07-12T00:00:00Z"
MARKER = "MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923"
FORMAL_MARKER = "PPC4161_GW250114_QNM_WEYL_C3_RECAST_4923"
NEXT_TARGET = (
    "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-"
    "sign-and-scale-from-motion-scalar-determinant-or-explicit-"
    "counterterm-boundary.md"
)
VARIABLES = {
    "GW250114PSEOBPosterior4923_MTS",
    "AlphaEvQNM4923_MTS",
    "QNMShiftPlus4923_MTS",
    "QNMShiftMinus4923_MTS",
    "QNMDeviationMap4923_MTS",
    "GW250114AlphaPlus4923_MTS",
    "GW250114AlphaMinus4923_MTS",
    "GW250114SpinDomain4923_MTS",
    "CubicQNMBranchGate4923_MTS",
    "CubicCompactControl4923_MTS",
    "VacuumGRDomain4923_MTS",
}
EVIDENCE = (
    "P8_Y5_R2FR_4923_RELEASE_PROVENANCE.csv",
    "P8_Y5_R2FR_4923_PSEOB_POSTERIOR_AUDIT.csv",
    "P8_Y5_R2FR_4923_COMPATIBILITY.csv",
    "P8_Y5_R2FR_4923_QNM_COEFFICIENT_MAP.csv",
    "P8_Y5_R2FR_4923_BRANCH_RECAST.csv",
    "P8_Y5_R2FR_4923_ALPHA_PROFILE.csv",
    "P8_Y5_R2FR_4923_ROBUSTNESS.csv",
    "P8_Y5_R2FR_4923_DOMAIN_GATE.csv",
    "P8_Y5_R2FR_4923_GATE_DECISION.csv",
    "P8_Y5_R2FR_4923_SOURCE_REGISTER.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: str) -> bool:
    return value.strip().lower() == "true"


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def load_research() -> Any:
    path = SCRIPTS / "Y5_R2FR_4923_GW250114_QNM_recast.py"
    specification = importlib.util.spec_from_file_location("research_4923", path)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint 4923 research module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def validation_rows() -> list[dict[str, Any]]:
    research = load_research()
    rows: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )

    evidence_paths = [OUTPUT / filename for filename in EVIDENCE]
    tables = {filename: read_csv(OUTPUT / filename) for filename in EVIDENCE}
    release = tables[EVIDENCE[0]]
    posterior = tables[EVIDENCE[1]]
    compatibility = tables[EVIDENCE[2]]
    maps = tables[EVIDENCE[3]]
    recast = tables[EVIDENCE[4]]
    profiles = tables[EVIDENCE[5]]
    robustness = tables[EVIDENCE[6]]
    domain = tables[EVIDENCE[7]]
    decisions = tables[EVIDENCE[8]]
    sources = tables[EVIDENCE[9]]

    release_map = {row["source_id"]: row for row in release}
    posterior_map = {row["audit_id"]: row for row in posterior}
    compatibility_map = {
        row["compatibility_id"]: row for row in compatibility
    }
    map_rows = {row["map_id"]: row for row in maps}
    recast_map = {row["branch"]: row for row in recast}
    domain_map = {row["domain_id"]: row for row in domain}
    decision_map = {row["gate"]: row for row in decisions}

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4922_VALIDATION.csv")
    check(
        "VAL4923_00_prior",
        prior[-1]["check_id"] == "VAL4922_OVERALL"
        and prior[-1]["status"] == "PASS",
        "checkpoint 4922 validation passed",
    )
    check(
        "VAL4923_01_evidence",
        all(path.exists() and read_csv(path) for path in evidence_paths),
        "all ten evidence files exist and parse",
    )
    check(
        "VAL4923_02_release",
        len(release) == 7
        and all(bool_cell(row["passed"]) for row in release)
        and int(release_map["archive"]["size_bytes"]) == 1671496586
        and release_map["archive"]["hash"].lower()
        == research.EXPECTED_ARCHIVE_MD5.lower(),
        "official release size and MD5 reproduce",
    )

    with h5py.File(research.PSEOB_H5, "r") as handle:
        samples = handle["pSEOBNRv5PHM/posterior_samples"][:]
        prior_raw = handle[
            "pSEOBNRv5PHM/config_file/config/prior_dict"
        ][0]
    prior_text = prior_raw.decode() if isinstance(prior_raw, bytes) else str(prior_raw)
    reporting_mask = (
        (samples["domega440"] < 0.8)
        & (samples["dtau440"] < 0.8)
    )
    theory_mask = (
        reporting_mask
        & (samples["final_spin_non_evolved"] >= 0.0)
        & (samples["final_spin_non_evolved"] <= 0.7)
    )
    check(
        "VAL4923_03_sample_counts",
        len(samples) == 40776
        and int(reporting_mask.sum()) == 17742
        and int(theory_mask.sum()) == 17719,
        "raw, paper-reporting and theory-domain counts reproduce independently",
    )
    check(
        "VAL4923_04_audit_counts",
        int(posterior_map["POST4923_00_raw"]["value"]) == 40776
        and int(posterior_map["POST4923_01_reporting_cut"]["value"]) == 17742
        and int(posterior_map["POST4923_02_theory_support"]["value"]) == 17719
        and float(posterior_map["POST4923_03_support_fraction"]["value"]) > 0.998,
        "stored sample audit matches the independent count",
    )
    check(
        "VAL4923_05_priors",
        "domega220 = Uniform" in prior_text
        and "dtau220 = Uniform" in prior_text
        and "minimum=-0.8, maximum=2.0" in prior_text
        and len(posterior) == 11
        and all(bool_cell(row["passed"]) for row in posterior),
        "released independent uniform deviation priors and audit rows pass",
    )
    check(
        "VAL4923_06_compatibility",
        len(compatibility) == 5
        and all(bool_cell(row["passed"]) for row in compatibility)
        and compatibility_map["COMP4923_00_pSEOB"]["status"]
        == "COMPATIBLE_220"
        and compatibility_map["COMP4923_01_generic_PyRing"]["status"]
        == "COMPARATOR_NOT_PRIMARY",
        "the pSEOB 220 product is primary and PyRing remains separate",
    )
    check(
        "VAL4923_07_exclusions",
        compatibility_map["COMP4923_02_440"]["status"]
        == "INCOMPATIBLE_NO_440_CUBIC_COEFFICIENTS"
        and compatibility_map["COMP4923_03_polarizations"]["status"]
        == "BRANCH_CONDITIONAL_ONLY"
        and compatibility_map["COMP4923_04_scalar"]["status"]
        == "EXCLUDED_WRONG_SECTOR",
        "440, polarization-combination and scalar-sector rules are explicit",
    )

    coefficients = read_csv(research.COEFFICIENT_FILE)
    coefficient_arrays = research.load_coefficients()
    endpoint_maps = research.qnm_maps(np.asarray([0.7]), coefficient_arrays)
    plus_endpoint = endpoint_maps["polar_plus"]["shift"][0]
    minus_endpoint = endpoint_maps["axial_minus"]["shift"][0]
    check(
        "VAL4923_08_coefficients",
        len(coefficients) == 13
        and [int(row["order"]) for row in coefficients] == list(range(13)),
        "the complete order-12 source coefficient vectors are present",
    )
    check(
        "VAL4923_09_endpoint_reproduction",
        abs(float(plus_endpoint.real) - 0.220) < 5.0e-4
        and abs(float(plus_endpoint.imag) + 0.293) < 5.0e-4
        and abs(float(minus_endpoint.real) + 0.221) < 5.0e-4
        and abs(float(minus_endpoint.imag) - 0.251) < 5.0e-4,
        "both chi=0.7 convergence-table endpoints reproduce",
    )
    check(
        "VAL4923_10_maps",
        len(maps) == 8
        and all(bool_cell(row["passed"]) for row in maps)
        and all(
            row["alpha_identity"]
            == "alpha_ev=alpha_bar1=s_+(ell_+/M)^4"
            for row in maps
        ),
        "eight evaluated coefficient-map rows preserve the corpus identity",
    )
    check(
        "VAL4923_11_damping_sign",
        float(map_rows["MAP4923_polar_plus_spin_q50"]["k_damping_time"]) < 0.0
        and float(map_rows["MAP4923_axial_minus_spin_q50"]["k_damping_time"]) > 0.0,
        "the damping-time conversion retains its required minus sign",
    )

    plus = recast_map["polar_plus"]
    minus = recast_map["axial_minus"]
    check(
        "VAL4923_12_recast_rows",
        len(recast) == 2
        and all(bool_cell(row["passed"]) for row in recast),
        "both branch-conditional recasts pass",
    )
    check(
        "VAL4923_13_plus_interval",
        -0.019 < float(plus["alpha_lower_90"]) < -0.014
        and 0.029 < float(plus["alpha_upper_90"]) < 0.035,
        "the polar-plus interval is numerically stable",
    )
    check(
        "VAL4923_14_minus_interval",
        -0.047 < float(minus["alpha_lower_90"]) < -0.039
        and 0.018 < float(minus["alpha_upper_90"]) < 0.024,
        "the axial-minus interval is numerically stable",
    )
    check(
        "VAL4923_15_GR_and_no_signal",
        all(
            float(row["alpha_lower_90"]) < 0.0 < float(row["alpha_upper_90"])
            and bool_cell(row["GR_inside_90"])
            and float(row["delta_chi2_proxy_vs_GR"]) < 1.0
            and float(row["prior_edge_probability"]) < 1.0e-6
            for row in recast
        ),
        "both intervals contain GR without edge dependence or a one-unit improvement",
    )

    profile_norms: list[float] = []
    for branch in ("polar_plus", "axial_minus"):
        branch_rows = [row for row in profiles if row["branch"] == branch]
        alpha_values = np.asarray([float(row["alpha_ev"]) for row in branch_rows])
        density_values = np.asarray(
            [float(row["posterior_density"]) for row in branch_rows]
        )
        profile_norms.append(float(np.trapezoid(density_values, alpha_values)))
    check(
        "VAL4923_16_profiles",
        len(profiles) == 2 * research.ALPHA_POINTS
        and all(bool_cell(row["passed"]) for row in profiles)
        and all(abs(value - 1.0) < 1.0e-7 for value in profile_norms),
        "both stored posterior profiles are finite and normalized",
    )

    robust_max = max(float(row["max_abs_alpha_90"]) for row in robustness)
    check(
        "VAL4923_17_robustness",
        len(robustness) == 54
        and all(bool_cell(row["passed"]) for row in robustness)
        and 0.045 < robust_max < 0.060,
        "the 54-row bandwidth-spin-theory matrix gives the expected envelope",
    )
    robust_domain = domain_map["DOMAIN4923_robust_envelope"]
    check(
        "VAL4923_18_domain",
        len(domain) == 5
        and all(bool_cell(row["passed"]) for row in domain)
        and not bool_cell(robust_domain["domain_gate_passed"])
        and 3.0 < float(robust_domain["miss_factor"]) < 5.0,
        "the robust strong-field envelope fails the one-percent gate by order four",
    )
    check(
        "VAL4923_19_domain_probabilities",
        0.45 < float(plus["probability_one_percent_domain"]) < 0.65
        and 0.30 < float(minus["probability_one_percent_domain"]) < 0.50,
        "partial but non-certifying compact-domain posterior mass is recorded",
    )
    check(
        "VAL4923_20_weak_projection",
        float(domain_map["DOMAIN4923_weak_Earth_acceleration"]["value"]) < 1.0e-20
        and float(domain_map["DOMAIN4923_weak_Galileo_clock"]["value"]) < 1.0e-20,
        "the robust physical-length smoke leaves weak local residuals negligible",
    )

    expected_decisions = {
        "official_data_acquisition": "CLOSED",
        "gravitational_QNM_map": "CLOSED_FOR_220_TO_CHI_0P7",
        "440_extension": "NOT_AVAILABLE",
        "branch_conditional_recast": "COMPLETED_NONCLAIM",
        "nonzero_signal": "NOT_SUPPORTED",
        "polarization_excitation": "NOT_DERIVED",
        "weak_invariant_vacuum_GR": "RETAINED",
        "compact_vacuum_GR": "NOT_PROMOTED",
        "finite_MTS_zeta_plus": "NOT_DERIVED",
        "full_MTS_to_GR": "NOT_PROMOTED",
        "next_target": "RETURN_TO_PARENT_FINITE_MATCHING",
    }
    check(
        "VAL4923_21_decisions",
        len(decisions) == len(expected_decisions)
        and all(bool_cell(row["passed"]) for row in decisions)
        and all(
            decision_map[gate]["status"] == status
            for gate, status in expected_decisions.items()
        )
        and decision_map["next_target"]["decision"] == NEXT_TARGET,
        "all final gate states and the derivation-first next target agree",
    )

    checkpoint_path = POST / (
        "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-"
        "Weyl-cubic-recast-or-posterior-acquisition-gate.md"
    )
    formal_path = FORMAL / "939-PPC4161-GW250114-QNM-Weyl-C3-recast.md"
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4923" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    check(
        "VAL4923_22_documents",
        MARKER in checkpoint
        and "[-0.01687, 0.03195]" in checkpoint
        and "[-0.04306, 0.02104]" in checkpoint
        and "No GitHub action" in checkpoint
        and FORMAL_MARKER in formal_note
        and "MTS_GW250114_QNM_PROVENANCE_4923" in provenance
        and "Every generated CSV row is valid_for_claim=false" in provenance,
        "checkpoint, formal summary and provenance are synchronized",
    )

    claims = read_csv(FORMAL / "02-claims-register.csv")
    claim_rows = [row for row in claims if row.get("claim_id") == "L-765"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    variable_rows = [
        row for row in variables if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    check(
        "VAL4923_23_registers",
        len(claim_rows) == 1
        and "compact_and_full_GR_not_promoted" in claim_rows[0]["status"]
        and len(variable_rows) == len(VARIABLES)
        and {row["symbol"] for row in variable_rows} == VARIABLES
        and variable_sources_exist
        and "1.216 GW250114 gravitational-QNM Weyl-cubic recast" in equations
        and "167. A generic QNM interval is not a unique Weyl-cubic posterior"
        in redteam
        and "PPC4161 checkpoint 4923" in spine
        and "Last checkpoint:" in resume
        and "4923-Y5-R2FR-GW250114" in resume
        and FORMAL_MARKER in resume,
        "claim, variable, equation, red-team, spine and resume registers agree",
    )

    local_sources = [
        row for row in sources if bool_cell(row["local_path_required"])
    ]
    external_sources = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    check(
        "VAL4923_24_sources",
        len(sources) == 30
        and len(local_sources) == 24
        and len(external_sources) == 6
        and all(
            bool_cell(row["source_exists"])
            and bool_cell(row["marker_found"])
            and bool_cell(row["passed"])
            and len(row["sha256"]) == 64
            for row in local_sources
        )
        and all(
            row["source_path_or_url"].startswith("https://")
            and bool_cell(row["passed"])
            for row in external_sources
        ),
        "all local source paths and external source records pass",
    )

    all_rows = [row for table in tables.values() for row in table]
    all_text = "\n".join(
        value for row in all_rows for value in row.values() if value
    )
    numeric_values: list[float] = []
    for row in all_rows:
        for value in row.values():
            try:
                numeric_values.append(float(value))
            except (TypeError, ValueError):
                pass
    check(
        "VAL4923_25_hygiene",
        all(not bool_cell(row["valid_for_claim"]) for row in all_rows)
        and "MISSING_" not in all_text
        and numeric_values
        and all(math.isfinite(value) for value in numeric_values)
        and importlib.metadata.version("h5py") == "3.16.0"
        and importlib.metadata.version("qnm") == "0.4.4"
        and all(
            compile_source(path)
            for path in (
                SCRIPTS / "Y5_R2FR_4923_GW250114_QNM_recast.py",
                SCRIPTS / "Y5_R2FR_4923_GW250114_QNM_recast_validation.py",
            )
        )
        and not (SCRIPTS / "__pycache__").exists(),
        "nonclaim, finite-number, dependency, compilation and cache hygiene pass",
    )

    rows.append(
        {
            "check_id": "VAL4923_OVERALL",
            "status": (
                "PASS"
                if all(row["status"] == "PASS" for row in rows)
                else "FAIL"
            ),
            "detail": "all 4923 data, QNM-map, recast and domain checks pass",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def main() -> int:
    rows = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4923_VALIDATION.csv", rows)
    passed = all(row["status"] == "PASS" for row in rows)
    print(f"P8_Y5_BRR545_4923_VALIDATION_{'PASS' if passed else 'FAIL'}")
    print(f"checks={len(rows)} passed={sum(row['status'] == 'PASS' for row in rows)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
