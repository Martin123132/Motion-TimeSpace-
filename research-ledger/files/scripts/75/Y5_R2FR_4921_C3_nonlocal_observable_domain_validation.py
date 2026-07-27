from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4921_C3_nonlocal_observable_domain as research


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
FORMAL_MARKER = research.FORMAL_MARKER
NEXT_TARGET = research.NEXT_TARGET
VARIABLES = (
    "CubicMetricPacket4921_MTS",
    "CubicObservableLength4921_MTS",
    "CubicPotential4921_MTS",
    "CubicWeakTransfer4921_MTS",
    "CubicClockBound4921_MTS",
    "CubicStrongControl4921_MTS",
    "GoroffSagnottiRun4921_MTS",
    "NonlocalTailClass4921_MTS",
    "MaxwellMetricOnly4921_MTS",
    "VacuumGRDomain4921_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4921_COEFFICIENT_OWNERSHIP.csv",
    "P8_Y5_R2FR_4921_WEAK_FIELD_TRANSFER.csv",
    "P8_Y5_R2FR_4921_LOCAL_ARENA_BOUNDS.csv",
    "P8_Y5_R2FR_4921_STRONG_DOMAIN.csv",
    "P8_Y5_R2FR_4921_GOROFF_SAGNOTTI_RUNNING.csv",
    "P8_Y5_R2FR_4921_NONLOCAL_SEPARATION.csv",
    "P8_Y5_R2FR_4921_MAXWELL_PROJECTION.csv",
    "P8_Y5_R2FR_4921_GATE_DECISION.csv",
    "P8_Y5_R2FR_4921_SOURCE_REGISTER.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
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


def close(left: float, right: float, rel: float = 1.0e-11) -> bool:
    return math.isclose(left, right, rel_tol=rel, abs_tol=0.0)


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4920_VALIDATION.csv")
    ownership = read_csv(OUTPUT / EVIDENCE[0])
    transfer = read_csv(OUTPUT / EVIDENCE[1])
    arenas = read_csv(OUTPUT / EVIDENCE[2])
    strong = read_csv(OUTPUT / EVIDENCE[3])
    gs_rows = read_csv(OUTPUT / EVIDENCE[4])
    nonlocal_rows = read_csv(OUTPUT / EVIDENCE[5])
    maxwell = read_csv(OUTPUT / EVIDENCE[6])
    decisions = read_csv(OUTPUT / EVIDENCE[7])
    sources = read_csv(OUTPUT / EVIDENCE[8])

    owner_map = {row["owner_id"]: row for row in ownership}
    transfer_map = {row["transfer_id"]: row for row in transfer}
    arena_map = {row["arena_id"]: row for row in arenas}
    strong_map = {row["system"]: row for row in strong}
    gs_map = {row["running_id"]: row for row in gs_rows}
    nonlocal_map = {row["class_id"]: row for row in nonlocal_rows}
    maxwell_map = {row["projection_id"]: row for row in maxwell}
    decision_map = {row["gate"]: row for row in decisions}

    checkpoint_path = POST / (
        "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-"
        "observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md"
    )
    formal_path = FORMAL / "937-PPC4161-C3-nonlocal-observable-domain-gate.md"
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4921" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-763"
    ]
    variable_rows = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )

    evidence_paths = [OUTPUT / filename for filename in EVIDENCE]
    all_evidence_rows = [row for path in evidence_paths for row in read_csv(path)]
    all_text = "\n".join(
        value for row in all_evidence_rows for value in row.values() if value
    )
    numeric_cells: list[float] = []
    for row in all_evidence_rows:
        for value in row.values():
            try:
                numeric_cells.append(float(value))
            except (TypeError, ValueError):
                pass

    expected = research.local_bound_values()
    clock_row = arena_map["ARENA4921_00_Galileo_clock"]
    cassini_row = arena_map["ARENA4921_01_Cassini_light"]
    mercury_row = arena_map["ARENA4921_02_Mercury_orbit"]
    r10_row = arena_map["ARENA4921_03_R10"]
    ns_row = strong_map["1.4_solar_mass_12km_neutron_star"]
    bh_row = strong_map["10_solar_mass_Schwarzschild_horizon"]
    gs_one = gs_map["GS4921_log_1"]
    gs_hundred = gs_map["GS4921_log_100"]
    local_source_rows = [row for row in sources if bool_cell(row["local_path_required"])]
    external_source_rows = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4921_C3_nonlocal_observable_domain.py",
        SCRIPTS / "Y5_R2FR_4921_C3_nonlocal_observable_domain_validation.py",
    ]

    rows = [
        check(
            "VAL4921_00_prior",
            prior[-1]["check_id"] == "VAL4920_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4920 predecessor validation passes",
        ),
        check(
            "VAL4921_01_ownership_rows",
            len(ownership) == 6 and all(bool_cell(row["passed"]) for row in ownership),
            "six coefficient-ownership clauses pass",
        ),
        check(
            "VAL4921_02_finite_open",
            owner_map["OWNER4921_02_bare"]["status"] == "FINITE_PART_NOT_DERIVED",
            "finite cubic matching is not fabricated",
        ),
        check(
            "VAL4921_03_zero_not_theorem",
            owner_map["OWNER4921_03_MTS"]["status"] == "ZERO_BRANCH_NOT_ZERO_THEOREM",
            "active zero residual is branch scoped",
        ),
        check(
            "VAL4921_04_massless_nonlocal",
            owner_map["OWNER4921_04_massless"]["status"] == "NONLOCAL_NOT_LOCAL_C3",
            "massless form factors remain nonlocal",
        ),
        check(
            "VAL4921_05_flat_variations",
            owner_map["OWNER4921_05_flat"]["status"]
            == "NO_LINEAR_NEWTON_OR_PHOTON_POLE_SHIFT",
            "C3 does not change the flat propagator",
        ),
        check(
            "VAL4921_06_transfer_rows",
            len(transfer) == 7 and all(bool_cell(row["passed"]) for row in transfer),
            "seven exact transfer and proxy-scope rows pass",
        ),
        check(
            "VAL4921_07_potential_coefficient",
            close(float(transfer_map["TRANSFER4921_00_potential"]["coefficient"]), -0.5),
            "potential coefficient is minus one half",
        ),
        check(
            "VAL4921_08_acceleration_factor",
            close(float(transfer_map["TRANSFER4921_02_acceleration"]["coefficient"]), 6.0),
            "differentiation produces the required factor six",
        ),
        check(
            "VAL4921_09_light_integral",
            close(
                float(transfer_map["TRANSFER4921_03_light"]["coefficient"]),
                15.0 * math.pi / 16.0,
            ),
            "light-deflection line integral coefficient is exact",
        ),
        check(
            "VAL4921_10_orbit_map",
            "1+3e^2/2+e^4/8" in transfer_map["TRANSFER4921_05_orbit"]["formula"],
            "pericentre eccentricity polynomial is retained",
        ),
        check(
            "VAL4921_11_proxy_repaired",
            transfer_map["TRANSFER4921_06_proxy_repair"]["status"]
            == "4880_PROXY_SCOPE_CORRECTED",
            "curvature-only proxy is restricted to domain control",
        ),
        check(
            "VAL4921_12_arena_rows",
            len(arenas) == 4 and all(bool_cell(row["passed"]) for row in arenas),
            "three numeric local envelopes and one disciplined R10 blocker pass",
        ),
        check(
            "VAL4921_13_clock_coefficient",
            close(
                float(clock_row["coefficient_per_L3_4_m_minus_4"]),
                expected["clock_coefficient_m_minus_4"],
            ),
            "Galileo clock coefficient independently reproduces",
        ),
        check(
            "VAL4921_14_clock_cap",
            close(float(clock_row["L3_upper_m"]), expected["clock_cap_m"]),
            "Galileo L3 cap independently reproduces",
        ),
        check(
            "VAL4921_15_cassini_cap",
            close(float(cassini_row["L3_upper_m"]), expected["cassini_cap_m"]),
            "Cassini L3 cap independently reproduces",
        ),
        check(
            "VAL4921_16_mercury_conversion",
            close(float(mercury_row["bound_value"]), research.mercury_limit_rad_per_orbit()),
            "Mercury arcsecond-per-century tolerance converts to radians per orbit",
        ),
        check(
            "VAL4921_17_mercury_cap",
            close(float(mercury_row["L3_upper_m"]), expected["mercury_cap_m"]),
            "Mercury L3 cap independently reproduces",
        ),
        check(
            "VAL4921_18_selected_clock",
            float(clock_row["L3_upper_m"])
            == min(float(row["L3_upper_m"]) for row in arenas[:3]),
            "Galileo is the strongest current simple local envelope",
        ),
        check(
            "VAL4921_19_selected_saturates",
            close(float(clock_row["projected_at_selected_cap"]), research.TAU_CLOCK),
            "selected envelope saturates the clock tolerance",
        ),
        check(
            "VAL4921_20_cassini_safe",
            float(cassini_row["projected_at_selected_cap"])
            < float(cassini_row["bound_value"]),
            "selected local cap lies below Cassini tolerance",
        ),
        check(
            "VAL4921_21_mercury_safe",
            float(mercury_row["projected_at_selected_cap"])
            < float(mercury_row["bound_value"]),
            "selected local cap lies below Mercury tolerance",
        ),
        check(
            "VAL4921_22_R10_blocked",
            r10_row["L3_upper_m"] == ""
            and r10_row["status"]
            == "BLOCKED_REQUIRES_EXTENDED_SOURCE_GEOMETRY_NOT_YUKAWA_RECAST",
            "R10 is not assigned a fake Yukawa-derived C3 bound",
        ),
        check(
            "VAL4921_23_strong_rows",
            len(strong) == 5 and all(bool_cell(row["passed"]) for row in strong),
            "five inherited system benchmarks are recomputed",
        ),
        check(
            "VAL4921_24_K_identity",
            all(
                close(
                    float(row["K_m_minus_4"]),
                    12.0 * float(row["r_s_m"]) ** 2 / float(row["radius_m"]) ** 6,
                )
                for row in strong
            ),
            "every Kretschmann value follows 12 r_s^2/r^6",
        ),
        check(
            "VAL4921_25_NS_cap",
            6.0e3 < float(ns_row["L3_upper_m_for_domain"]) < 6.1e3,
            "neutron-star one-percent control cap is about 6.016 km",
        ),
        check(
            "VAL4921_26_BH_cap",
            8.6e3 < float(bh_row["L3_upper_m_for_domain"]) < 8.8e3,
            "ten-solar-mass horizon cap is about 8.691 km",
        ),
        check(
            "VAL4921_27_compact_not_certified",
            not bool_cell(ns_row["selected_local_cap_satisfies_domain"])
            and not bool_cell(bh_row["selected_local_cap_satisfies_domain"]),
            "the local clock envelope does not certify compact curvature",
        ),
        check(
            "VAL4921_28_weak_systems_controlled",
            all(
                bool_cell(strong_map[name]["selected_local_cap_satisfies_domain"])
                for name in ("Earth", "Sun", "one_solar_mass_white_dwarf")
            ),
            "the selected local cap controls the three weak-surface benchmarks",
        ),
        check(
            "VAL4921_29_GS_rows",
            len(gs_rows) == 2 and all(bool_cell(row["passed"]) for row in gs_rows),
            "two logarithmic running benchmarks pass",
        ),
        check(
            "VAL4921_30_GS_residue",
            close(float(gs_one["pole_residue"]), 209.0 / 2880.0),
            "Goroff-Sagnotti pole residue is exact",
        ),
        check(
            "VAL4921_31_GS_length",
            close(
                float(gs_one["L3_over_planck_length"]),
                (18.0 * (209.0 / 2880.0) / math.pi**2) ** 0.25,
            ),
            "running length is 0.603159 Planck lengths per unit log",
        ),
        check(
            "VAL4921_32_GS_log_scaling",
            close(
                float(gs_hundred["L3_running_m"]) / float(gs_one["L3_running_m"]),
                100.0**0.25,
            ),
            "L3 running scales as the fourth root of the logarithm",
        ),
        check(
            "VAL4921_33_GS_compact_safe",
            float(gs_hundred["ten_solar_BH_horizon_epsilon"]) < 1.0e-150,
            "even the log-100 running benchmark is negligible at the black-hole horizon",
        ),
        check(
            "VAL4921_34_nonlocal_rows",
            len(nonlocal_rows) == 6
            and all(bool_cell(row["passed"]) for row in nonlocal_rows),
            "six local/nonlocal separation clauses pass",
        ),
        check(
            "VAL4921_35_eternal_scope",
            "eternal source-free" in nonlocal_map["NONLOCAL4921_01_eternal"]["background_scope"],
            "quadratic no-correction theorem is state scoped",
        ),
        check(
            "VAL4921_36_radial_separation",
            nonlocal_map["NONLOCAL4921_02_material"]["radial_image"].startswith("r^-3")
            and nonlocal_map["NONLOCAL4921_03_C3"]["radial_image"].startswith("r^-6"),
            "material nonlocal and local cubic radial powers remain distinct",
        ),
        check(
            "VAL4921_37_no_cancellation",
            nonlocal_map["NONLOCAL4921_05_no_merge"]["cancellation_with_C3"]
            == "FORBIDDEN_WITHOUT_MATCHED_COEFFICIENTS",
            "no unsourced local/nonlocal cancellation is used",
        ),
        check(
            "VAL4921_38_maxwell_rows",
            len(maxwell) == 4 and all(bool_cell(row["passed"]) for row in maxwell),
            "four Maxwell projections pass",
        ),
        check(
            "VAL4921_39_no_direct_Maxwell",
            maxwell_map["MAXWELL4921_00_fixed_metric"]["status"]
            == "EXACT_OPERATOR_CONTENT",
            "pure C3 has no direct fixed-metric Maxwell coupling",
        ),
        check(
            "VAL4921_40_Poynting_retained",
            maxwell_map["MAXWELL4921_02_source"]["status"]
            == "POYNTING_VECTOR_RETAINED_AS_GRAVITATIONAL_SOURCE",
            "electromagnetic energy flux remains a metric source",
        ),
        check(
            "VAL4921_41_gate_rows",
            len(decisions) == 8 and all(bool_cell(row["passed"]) for row in decisions),
            "eight domain decisions pass",
        ),
        check(
            "VAL4921_42_weak_retained",
            decision_map["weak_invariant_vacuum_GR"]["status"]
            == "RETAINED_WITH_EXPLICIT_C3_BOUND_CLAUSE",
            "weak invariant-vacuum certificate carries the cubic clause",
        ),
        check(
            "VAL4921_43_compact_not_extended",
            decision_map["compact_vacuum_GR"]["status"] == "NOT_GLOBALLY_EXTENDED",
            "compact exact-GR domain is not overpromoted",
        ),
        check(
            "VAL4921_44_full_not_promoted",
            decision_map["full_MTS_to_GR"]["status"] == "NOT_PROMOTED",
            "full MTS-to-GR claim remains false",
        ),
        check(
            "VAL4921_45_next_target",
            decision_map["next_target"]["decision"] == NEXT_TARGET,
            "direct strong-field cubic test is the next target",
        ),
        check(
            "VAL4921_46_checkpoint_marker",
            MARKER in checkpoint and "L3 < 6.92765e7 m" in checkpoint,
            "checkpoint contains marker and selected local envelope",
        ),
        check(
            "VAL4921_47_checkpoint_caveat",
            "compact-vacuum and full-MTS claims remain false" in checkpoint,
            "checkpoint states the compact and full-theory boundary",
        ),
        check(
            "VAL4921_48_formal_marker",
            FORMAL_MARKER in formal_note and "0.603159 l_P" in formal_note,
            "formal summary contains marker and running result",
        ),
        check(
            "VAL4921_49_provenance",
            "MTS_C3_NONLOCAL_PROVENANCE_4921" in provenance
            and research.BURGER_URL in provenance
            and research.CALMET_URL in provenance,
            "provenance records both primary theory sources",
        ),
        check(
            "VAL4921_50_claim_register",
            len(claims) == 1
            and claims[0]["status"].startswith("weak_invariant_vacuum_GR_retained"),
            "claim L-763 is unique and branch scoped",
        ),
        check(
            "VAL4921_51_variable_register",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "ten canonical variables are registered once",
        ),
        check(
            "VAL4921_52_variable_sources",
            variable_sources_exist,
            "every registered variable source path exists",
        ),
        check(
            "VAL4921_53_equation_register",
            "1.214 Cubic-metric observable transfer and domain gate" in equations,
            "equation 1.214 is registered",
        ),
        check(
            "VAL4921_54_redteam_register",
            "165. A curvature invariant is not by itself the weak-field observable" in redteam,
            "red-team item 165 is registered",
        ),
        check(
            "VAL4921_55_spine_register",
            "PPC4161 checkpoint 4921" in spine and FORMAL_MARKER in spine,
            "unification spine checkpoint is registered",
        ),
        check(
            "VAL4921_56_resume",
            "Last checkpoint: `4921-" in resume and NEXT_TARGET in resume,
            "local resume points to checkpoint 4921 and 4922",
        ),
        check(
            "VAL4921_57_source_rows",
            len(sources) == 29,
            "twenty-nine local and external provenance rows are recorded",
        ),
        check(
            "VAL4921_58_local_sources",
            all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and len(row["sha256"]) == 64
                for row in local_source_rows
            ),
            "every local source exists, has its marker and is hashed",
        ),
        check(
            "VAL4921_59_external_sources",
            len(external_source_rows) == 7
            and all(
                row["source_path_or_url"].startswith("https://")
                and row["verification"] == "web_checked_2026-07-12"
                for row in external_source_rows
            ),
            "seven external sources are HTTPS and web-checked",
        ),
        check(
            "VAL4921_60_nonclaim_rows",
            all(not bool_cell(row["valid_for_claim"]) for row in all_evidence_rows),
            "all checkpoint evidence remains private nonclaim",
        ),
        check(
            "VAL4921_61_no_missing_markers",
            "MISSING_" not in all_text,
            "no placeholder marker appears in generated evidence",
        ),
        check(
            "VAL4921_62_numeric_finite",
            numeric_cells and all(math.isfinite(value) for value in numeric_cells),
            "all parseable numeric evidence cells are finite",
        ),
        check(
            "VAL4921_63_compile",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4921_64_no_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "scripts __pycache__ is absent",
        ),
    ]
    rows.append(
        check(
            "VAL4921_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "all 4921 cubic observable, nonlocal separation and domain checks pass",
        )
    )
    return rows


def main() -> int:
    rows = validation_rows()
    output_path = OUTPUT / "P8_Y5_BRR545_4921_VALIDATION.csv"
    write_csv(output_path, rows)
    passed = all(row["status"] == "PASS" for row in rows)
    print(f"P8_Y5_BRR545_4921_VALIDATION_{'PASS' if passed else 'FAIL'}")
    print(f"checks={len(rows)} passed={sum(row['status'] == 'PASS' for row in rows)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
