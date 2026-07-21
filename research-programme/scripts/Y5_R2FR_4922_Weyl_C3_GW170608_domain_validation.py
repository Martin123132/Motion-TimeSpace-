from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4922_Weyl_C3_GW170608_domain as research


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
    "WeylCubicPacket4922_MTS",
    "WeylCubicLength4922_MTS",
    "AlphaBar1GW4922_MTS",
    "BinaryCubicDirection4922_MTS",
    "PureI1Metric4922_MTS",
    "PureI1Clock4922_MTS",
    "GW170608Bound4922_MTS",
    "CubicCompactControl4922_MTS",
    "CubicMaxwellProjection4922_MTS",
    "VacuumGRDomain4922_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4922_BASIS_MAP.csv",
    "P8_Y5_R2FR_4922_4921_SUPERSESSION.csv",
    "P8_Y5_R2FR_4922_STATIC_METRIC_TRANSFER.csv",
    "P8_Y5_R2FR_4922_GW170608_INPUTS.csv",
    "P8_Y5_R2FR_4922_GW170608_COEFFICIENT_BOUND.csv",
    "P8_Y5_R2FR_4922_RINGDOWN_COMPARATOR.csv",
    "P8_Y5_R2FR_4922_LOCAL_WEAK_PROJECTION.csv",
    "P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv",
    "P8_Y5_R2FR_4922_GATE_DECISION.csv",
    "P8_Y5_R2FR_4922_SOURCE_REGISTER.csv",
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


def close(left: float, right: float, rel: float = 1.0e-10) -> bool:
    return math.isclose(left, right, rel_tol=rel, abs_tol=1.0e-15)


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4921_VALIDATION.csv")
    basis = read_csv(OUTPUT / EVIDENCE[0])
    supersession = read_csv(OUTPUT / EVIDENCE[1])
    metric = read_csv(OUTPUT / EVIDENCE[2])
    gw_inputs = read_csv(OUTPUT / EVIDENCE[3])
    gw_bounds = read_csv(OUTPUT / EVIDENCE[4])
    ringdown = read_csv(OUTPUT / EVIDENCE[5])
    local = read_csv(OUTPUT / EVIDENCE[6])
    compact = read_csv(OUTPUT / EVIDENCE[7])
    decisions = read_csv(OUTPUT / EVIDENCE[8])
    sources = read_csv(OUTPUT / EVIDENCE[9])

    basis_map = {row["map_id"]: row for row in basis}
    super_map = {row["item"]: row for row in supersession}
    metric_map = {row["metric_id"]: row for row in metric}
    input_map = {row["input_id"]: row for row in gw_inputs}
    bound_map = {row["branch"]: row for row in gw_bounds}
    ring_map = {row["comparator_id"]: row for row in ringdown}
    local_map = {row["projection_id"]: row for row in local}
    compact_map = {row["system"]: row for row in compact}
    decision_map = {row["gate"]: row for row in decisions}

    checkpoint_path = POST / (
        "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-"
        "bound-or-compact-vacuum-GR-domain-gate.md"
    )
    predecessor_path = POST / (
        "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-"
        "observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md"
    )
    formal_path = FORMAL / "938-PPC4161-Weyl-C3-GW170608-domain-gate.md"
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4922" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    predecessor = predecessor_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    claims_all = read_csv(FORMAL / "02-claims-register.csv")
    claim_764 = [row for row in claims_all if row.get("claim_id") == "L-764"]
    claim_763 = [row for row in claims_all if row.get("claim_id") == "L-763"]
    variable_all = read_csv(FORMAL / "04-variable-audit.csv")
    variable_rows = [row for row in variable_all if row.get("symbol") in VARIABLES]
    old_variable_rows = [
        row for row in variable_all if row.get("symbol", "").endswith("4921_MTS")
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

    local_source_rows = [row for row in sources if bool_cell(row["local_path_required"])]
    external_source_rows = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4922_Weyl_C3_GW170608_domain.py",
        SCRIPTS / "Y5_R2FR_4922_Weyl_C3_GW170608_domain_validation.py",
    ]

    negative = bound_map["negative"]
    positive = bound_map["positive"]
    ns = compact_map["1.4_solar_mass_12km_neutron_star"]
    bh = compact_map["10_solar_mass_Schwarzschild_horizon"]

    rows = [
        check(
            "VAL4922_00_prior",
            prior[-1]["check_id"] == "VAL4921_OVERALL"
            and prior[-1]["status"] == "PASS",
            "the archived 4921 validation completed before supersession",
        ),
        check(
            "VAL4922_01_prior_superseded",
            "SUPERSEDED BY CHECKPOINT 4922" in predecessor,
            "the predecessor is prominently demoted rather than silently reused",
        ),
        check(
            "VAL4922_02_evidence_files",
            all(path.exists() and read_csv(path) for path in evidence_paths),
            "all ten evidence tables exist and parse with data rows",
        ),
        check(
            "VAL4922_03_basis_rows",
            len(basis) == 8 and all(bool_cell(row["passed"]) for row in basis),
            "eight basis-map clauses pass",
        ),
        check(
            "VAL4922_04_corpus_operator",
            basis_map["BASIS4922_00_corpus"]["status"]
            == "EXACT_CONTRACTION_MATCH"
            and "O_+=I1=C7" in basis_map["BASIS4922_00_corpus"]["relation"],
            "the corpus operator is identified with I1 and C7",
        ),
        check(
            "VAL4922_05_ricci_flat_identity",
            "I2=I1/2" in basis_map["BASIS4922_01_identity"]["relation"],
            "the declared smooth Ricci-flat quotient identity is retained",
        ),
        check(
            "VAL4922_06_action_normalization",
            "a_+=16 pi G_N zeta_+=s_+ ell_+^4"
            in basis_map["BASIS4922_02_action"]["definition"],
            "the invariant action coefficient and length share one normalization",
        ),
        check(
            "VAL4922_07_waveform_map",
            basis_map["BASIS4922_03_waveform"]["relation"]
            == "alpha_bar1=s_+(ell_+/M_geo)^4",
            "the exact sample-level alpha_bar1 map is registered",
        ),
        check(
            "VAL4922_08_binary_direction",
            basis_map["BASIS4922_04_binary"]["status"]
            == "NUISANCE_DIRECTION_NOT_IDENTIFIED_WITH_ZETA_PLUS",
            "the second binary coefficient is not folded into zeta_plus",
        ),
        check(
            "VAL4922_09_Burger_map",
            "zeta_+=lambda(beta2+beta1/2)"
            in basis_map["BASIS4922_05_Burger"]["relation"],
            "the Burger coordinate is mapped to the invariant quotient",
        ),
        check(
            "VAL4922_10_noninvertibility",
            basis_map["BASIS4922_06_noninvertible"]["status"]
            == "NONINVERTIBILITY_PROVED",
            "beta1 zero and beta2 nonzero supplies the strict counterexample",
        ),
        check(
            "VAL4922_11_supersession_rows",
            len(supersession) == 7
            and all(bool_cell(row["passed"]) for row in supersession),
            "seven predecessor corrections are explicit",
        ),
        check(
            "VAL4922_12_old_length_inactive",
            not bool_cell(super_map["4921_L3_definition"]["active_use"])
            and super_map["4921_L3_definition"]["new_status"]
            == "BURGER_BETA1_BENCHMARK_ONLY",
            "the old L3 coordinate is inactive",
        ),
        check(
            "VAL4922_13_old_local_bounds_demoted",
            all(
                not bool_cell(super_map[item]["active_use"])
                for item in (
                    "4921_Galileo_bound",
                    "4921_Cassini_bound",
                    "4921_Mercury_bound",
                )
            ),
            "all three old local envelopes are demoted",
        ),
        check(
            "VAL4922_14_control_replaced",
            super_map["4921_compact_control"]["replacement"]
            == "ell_+<(tau/K)^(1/4)",
            "the canonical curvature control no longer contains the old factor nine",
        ),
        check(
            "VAL4922_15_weak_replacement",
            bool_cell(super_map["weak_invariant_vacuum_GR"]["active_use"])
            and "GW170608" in super_map["weak_invariant_vacuum_GR"]["replacement"],
            "weak GR is retained only through the corrected replacement",
        ),
        check(
            "VAL4922_16_metric_rows",
            len(metric) == 7 and all(bool_cell(row["passed"]) for row in metric),
            "seven pure-I1 static-transfer clauses pass",
        ),
        check(
            "VAL4922_17_f_coefficients",
            "24 s ell_+^4 M^2[9/r^6-49M/(3r^7)]"
            in metric_map["METRIC4922_00_f"]["formula"],
            "the sourced radial-function coefficients are preserved",
        ),
        check(
            "VAL4922_18_N_coefficient",
            "-108 s ell_+^4 M^2/r^6"
            in metric_map["METRIC4922_01_N"]["formula"],
            "the sourced lapse coefficient is preserved",
        ),
        check(
            "VAL4922_19_r6_cancellation",
            close(24.0 * 9.0 - 2.0 * 108.0, 0.0),
            "the first-order r^-6 terms cancel as 216 minus 216",
        ),
        check(
            "VAL4922_20_r7_product",
            close(2.0 * 108.0 * 2.0 - 24.0 * 49.0 / 3.0, 40.0)
            and "40 s ell_+^4 M^3/r^7"
            in metric_map["METRIC4922_02_cancel"]["formula"],
            "the surviving N-squared-f coefficient is forty",
        ),
        check(
            "VAL4922_21_potential",
            "delta Phi=-20 s ell_+^4 M^3/r^7"
            == metric_map["METRIC4922_03_potential"]["formula"],
            "the corrected clock potential coefficient is minus twenty",
        ),
        check(
            "VAL4922_22_acceleration",
            "140 ell_+^4 M^2/r^6"
            in metric_map["METRIC4922_04_acceleration"]["formula"],
            "differentiation gives the acceleration coefficient 140",
        ),
        check(
            "VAL4922_23_clock",
            "20 ell_+^4 M^2"
            in metric_map["METRIC4922_05_clock"]["formula"],
            "the two-radius clock transfer uses the corrected r^-7 profile",
        ),
        check(
            "VAL4922_24_control",
            "epsilon_K=ell_+^4 K"
            in metric_map["METRIC4922_06_control"]["formula"],
            "the canonical strict-EFT parameter is registered",
        ),
        check(
            "VAL4922_25_GW_input_rows",
            len(gw_inputs) == 5
            and all(bool_cell(row["passed"]) for row in gw_inputs),
            "five published GW/model inputs pass",
        ),
        check(
            "VAL4922_26_alpha1_interval",
            close(float(input_map["GW4922_00_alpha1"]["lower_90"]), -0.16)
            and close(float(input_map["GW4922_00_alpha1"]["upper_90"]), 2.82),
            "the alpha_bar1 90-percent interval reproduces",
        ),
        check(
            "VAL4922_27_alpha2_interval",
            close(float(input_map["GW4922_01_alpha2"]["lower_90"]), -3.27)
            and close(float(input_map["GW4922_01_alpha2"]["upper_90"]), 3.77),
            "the marginalized alpha_bar2 interval reproduces",
        ),
        check(
            "VAL4922_28_Bayes_factor",
            close(float(input_map["GW4922_02_Bayes"]["central"]), -2.81)
            and input_map["GW4922_02_Bayes"]["status"]
            == "DATA_DISFAVORS_EFT_RELATIVE_TO_GR",
            "the negative model-selection result is not presented as a signal",
        ),
        check(
            "VAL4922_29_mass_scope",
            close(float(input_map["GW4922_03_mass"]["central"]), 19.0)
            and "APPROXIMATE" in input_map["GW4922_03_mass"]["status"],
            "the 12 plus 7 solar-mass conversion is labelled approximate",
        ),
        check(
            "VAL4922_30_model_scope",
            "no_direct_EFT_merger_simulation"
            == input_map["GW4922_04_model"]["lower_90"],
            "the approximate merger-model boundary is explicit",
        ),
        check(
            "VAL4922_31_bound_rows",
            len(gw_bounds) == 3
            and all(bool_cell(row["passed"]) for row in gw_bounds),
            "two sign branches and one primary-statement row pass",
        ),
        check(
            "VAL4922_32_negative_ratio",
            close(float(negative["ell_plus_over_M_upper"]), 0.16**0.25),
            "the negative-branch dimensionless length bound reproduces",
        ),
        check(
            "VAL4922_33_positive_ratio",
            close(float(positive["ell_plus_over_M_upper"]), 2.82**0.25),
            "the positive-branch dimensionless length bound reproduces",
        ),
        check(
            "VAL4922_34_mass_length",
            close(float(positive["approx_M_geo_m"]), 28056.724129635342),
            "the approximate nineteen-solar-mass geometric length reproduces",
        ),
        check(
            "VAL4922_35_negative_length",
            close(float(negative["approx_ell_plus_upper_m"]), 17744.630386530593),
            "the illustrative negative-branch physical length reproduces",
        ),
        check(
            "VAL4922_36_positive_length",
            close(float(positive["approx_ell_plus_upper_m"]), 36357.937522423665),
            "the illustrative positive-branch physical length reproduces",
        ),
        check(
            "VAL4922_37_horizon_epsilon",
            close(float(negative["horizon_epsilon_at_same_mass"]), 0.12)
            and close(float(positive["horizon_epsilon_at_same_mass"]), 2.115),
            "the sign-dependent same-mass horizon controls reproduce",
        ),
        check(
            "VAL4922_38_domain_factors",
            close(float(negative["one_percent_domain_ratio"]), 12.0)
            and close(float(positive["one_percent_domain_ratio"]), 211.5),
            "the one-percent-domain miss factors reproduce",
        ),
        check(
            "VAL4922_39_ringdown_rows",
            len(ringdown) == 5
            and all(bool_cell(row["passed"]) for row in ringdown),
            "five ringdown, scaling and compatibility rows pass",
        ),
        check(
            "VAL4922_40_mixed_not_direct",
            "NOT_DIRECT" in ring_map["RING4922_00_mixed"]["mapping_to_ell_plus"],
            "the mixed parity ringdown number is not misused as a pure-I1 bound",
        ),
        check(
            "VAL4922_41_future_sources",
            ring_map["RING4922_03_future"]["status"] == "NEXT_DIRECT_TARGET"
            and research.GW250114_URL in ring_map["RING4922_03_future"]["source"]
            and research.GRAVITATIONAL_QNM_URL
            in ring_map["RING4922_03_future"]["source"]
            and ring_map["RING4922_04_scalar_exclusion"]["status"]
            == "EXCLUDED_AS_DIRECT_GRAVITATIONAL_QNM_TEMPLATE"
            and research.SCALAR_HIGH_SPIN_C3_URL
            in ring_map["RING4922_04_scalar_exclusion"]["source"],
            "the gravitational template is paired and the scalar sector excluded",
        ),
        check(
            "VAL4922_42_local_rows",
            len(local) == 6 and all(bool_cell(row["passed"]) for row in local),
            "six corrected weak projections pass",
        ),
        check(
            "VAL4922_43_clock_cap",
            close(float(local_map["LOCAL4922_00_clock_cap"]["value"]), 7584108240.78759),
            "the corrected pure-I1 Galileo envelope reproduces",
        ),
        check(
            "VAL4922_44_clock_at_GW",
            close(
                float(local_map["LOCAL4922_01_clock_at_GW"]["value"]),
                1.3098770899518595e-26,
            ),
            "the Galileo anomaly at the positive GW endpoint reproduces",
        ),
        check(
            "VAL4922_45_acceleration_at_GW",
            close(
                float(local_map["LOCAL4922_02_Earth_acceleration"]["value"]),
                7.195760220047237e-26,
            ),
            "the Earth acceleration residual reproduces",
        ),
        check(
            "VAL4922_46_Earth_control",
            close(
                float(local_map["LOCAL4922_03_Earth_curvature"]["value"]),
                2.4671177897304817e-26,
            ),
            "the Earth curvature control reproduces",
        ),
        check(
            "VAL4922_47_Sun_control",
            close(
                float(local_map["LOCAL4922_04_Sun_curvature"]["value"]),
                1.6131431015357298e-27,
            ),
            "the Sun curvature control reproduces",
        ),
        check(
            "VAL4922_48_Maxwell_projection",
            close(float(local_map["LOCAL4922_05_Maxwell"]["value"]), 0.0)
            and "NO_DIRECT_COUPLING"
            in local_map["LOCAL4922_05_Maxwell"]["status"],
            "pure I1 has no direct fixed-metric Maxwell variation",
        ),
        check(
            "VAL4922_49_compact_rows",
            len(compact) == 5
            and all(bool_cell(row["passed"]) for row in compact),
            "all five inherited system curvatures are reprojected",
        ),
        check(
            "VAL4922_50_NS_cap",
            close(float(ns["ell_plus_upper_m_for_domain"]), 3473.408489247101),
            "the neutron-star one-percent curvature cap reproduces",
        ),
        check(
            "VAL4922_51_BH_cap",
            close(float(bh["ell_plus_upper_m_for_domain"]), 5017.854280181087),
            "the ten-solar-mass horizon one-percent cap reproduces",
        ),
        check(
            "VAL4922_52_compact_failure",
            not bool_cell(ns["negative_GW_endpoint_controls_domain"])
            and not bool_cell(ns["positive_GW_endpoint_controls_domain"])
            and not bool_cell(bh["negative_GW_endpoint_controls_domain"])
            and not bool_cell(bh["positive_GW_endpoint_controls_domain"]),
            "neither sign endpoint certifies the selected compact benchmarks",
        ),
        check(
            "VAL4922_53_gate_rows",
            len(decisions) == 8
            and all(bool_cell(row["passed"]) for row in decisions),
            "eight final gate decisions pass",
        ),
        check(
            "VAL4922_54_weak_gate",
            decision_map["weak_invariant_vacuum_GR"]["status"]
            == "RETAINED_AFTER_CORRECTED_TRANSFER",
            "the weak invariant-vacuum route survives the corrected map",
        ),
        check(
            "VAL4922_55_compact_gate",
            decision_map["compact_vacuum_GR"]["status"] == "NOT_PROMOTED",
            "compact-vacuum GR remains unpromoted",
        ),
        check(
            "VAL4922_56_parent_gate",
            decision_map["finite_MTS_zeta_plus"]["status"] == "NOT_DERIVED",
            "the observational bound is not substituted for parent matching",
        ),
        check(
            "VAL4922_57_full_gate",
            decision_map["full_MTS_to_GR"]["status"] == "NOT_PROMOTED",
            "the full MTS-to-GR claim remains false",
        ),
        check(
            "VAL4922_58_next_target",
            decision_map["next_target"]["decision"] == NEXT_TARGET,
            "the next target is the compatible gravitational-QNM GW250114 recast",
        ),
        check(
            "VAL4922_59_checkpoint",
            MARKER in checkpoint
            and "beta1=0, beta2!=0" in checkpoint
            and "epsilon_h = (3/4) abs(alpha_bar1)" in checkpoint,
            "the checkpoint contains the marker, counterexample and compact gate",
        ),
        check(
            "VAL4922_60_formal",
            FORMAL_MARKER in formal_note
            and "-0.16<alpha_bar1<2.82" in formal_note,
            "the formal note records the marker and direct interval",
        ),
        check(
            "VAL4922_61_provenance",
            "MTS_WEYL_C3_GW170608_PROVENANCE_4922" in provenance
            and research.LIU_YUNES_URL in provenance
            and research.CANO_QNM_URL in provenance
            and research.GRAVITATIONAL_QNM_URL in provenance
            and "scalar perturbation" in provenance
            and "Every generated CSV row is `valid_for_claim=false`" in provenance,
            "primary sources, sector exclusion and nonclaim discipline are recorded",
        ),
        check(
            "VAL4922_62_claims",
            len(claim_764) == 1
            and "compact_vacuum_compact_matter_and_full_MTS_not_promoted"
            in claim_764[0]["status"]
            and len(claim_763) == 1
            and claim_763[0]["status"].startswith("superseded_by_4922"),
            "L-764 is active and L-763 is explicitly superseded",
        ),
        check(
            "VAL4922_63_registers",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES)
            and variable_sources_exist
            and sum("superseded" in row["status"] for row in old_variable_rows) >= 7
            and "1.215 Weyl-cubic basis map and GW170608 bound" in equations
            and "166. A probe-potential coefficient is not the invariant Weyl-cubic packet"
            in redteam
            and "PPC4161 checkpoint 4922" in spine
            and "Last checkpoint: `4922-" in resume
            and NEXT_TARGET in resume,
            "variables, equation, red-team, spine and resume registers are synchronized",
        ),
        check(
            "VAL4922_64_hygiene",
            len(sources) == 26
            and len(local_source_rows) == 18
            and len(external_source_rows) == 8
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and len(row["sha256"]) == 64
                for row in local_source_rows
            )
            and all(
                row["source_path_or_url"].startswith("https://")
                and row["verification"] == "web_checked_2026-07-12"
                for row in external_source_rows
            )
            and all(not bool_cell(row["valid_for_claim"]) for row in all_evidence_rows)
            and "MISSING_" not in all_text
            and numeric_cells
            and all(math.isfinite(value) for value in numeric_cells)
            and all(compile_source(path) for path in scripts)
            and not (SCRIPTS / "__pycache__").exists(),
            "sources, nonclaim rows, numeric cells, scripts and cache hygiene pass",
        ),
    ]
    rows.append(
        check(
            "VAL4922_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "all 4922 invariant Weyl-cubic, GW170608 and domain checks pass",
        )
    )
    return rows


def main() -> int:
    rows = validation_rows()
    output_path = OUTPUT / "P8_Y5_BRR545_4922_VALIDATION.csv"
    write_csv(output_path, rows)
    passed = all(row["status"] == "PASS" for row in rows)
    print(f"P8_Y5_BRR545_4922_VALIDATION_{'PASS' if passed else 'FAIL'}")
    print(f"checks={len(rows)} passed={sum(row['status'] == 'PASS' for row in rows)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
