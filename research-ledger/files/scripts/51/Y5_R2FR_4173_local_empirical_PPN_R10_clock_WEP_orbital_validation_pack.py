from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4173"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_EMPIRICAL_VALIDATION_PACK_4173"
DECISION = "PPC4161_TK_HQNP_SOURCE_BACKED_LOCAL_BOUND_COMPARATOR_PASSES_NUMERIC_ROWS_PUBLIC_CLAIM_STILL_FALSE"
DOC_PATH = POST / "4173-Y5-R2FR-local-empirical-PPN-R10-clock-WEP-orbital-validation-pack.md"
FORMAL_189_PATH = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-014"
SPINE_MARKER = "PPC4161_LOCAL_EMPIRICAL_VALIDATION_PACK_4173"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_EMPIRICAL_VALIDATION_4173"
NEXT_TARGET = "4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md"

LOCAL_SOURCES = {
    "SRC4173_LOCAL_00_4172_doc": (
        POST / "4172-Y5-R2FR-PPC4161-full-PPN-readout-gamma-beta-alpha-xi-zeta.md",
        "R_PPN = (gamma-1, beta-1",
        "4172 private full-PPN vector checkpoint.",
    ),
    "SRC4173_LOCAL_01_4172_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv",
        "gamma-1=0",
        "4172 private PPN prediction vector.",
    ),
    "SRC4173_LOCAL_02_4172_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4172_STATUS.csv",
        "PPN_vector_closed_private",
        "4172 branch status showing empirical gates still open before this pack.",
    ),
    "SRC4173_LOCAL_03_formal_188": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Formal PPN readout bridge.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "SRC4173_WEB_00_Will2014_PPN_table",
        "url": "https://arxiv.org/pdf/1403.7377",
        "doi_or_id": "arXiv:1403.7377; Living Rev. Relativity 17 (2014), 4; DOI 10.12942/lrr-2014-4",
        "evidence": "Table 4 gives current PPN limits including gamma-1, beta-1, xi, alpha_i, zeta_i; lines around 2740-2757 in the extracted PDF.",
    },
    {
        "source_id": "SRC4173_WEB_01_Cassini_gamma",
        "url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "doi_or_id": "Nature 425, 374-376 (2003); PubMed 14508481",
        "evidence": "Cassini radio tracking result gamma = 1 + (2.1 +/- 2.3) x 10^-5.",
    },
    {
        "source_id": "SRC4173_WEB_02_EotWash2020_R10",
        "url": "https://arxiv.org/abs/2002.11761",
        "doi_or_id": "Phys. Rev. Lett. 124, 101101 (2020); DOI 10.1103/PhysRevLett.124.101101",
        "evidence": "Data at detector-attractor separations 52 um to 3.0 mm; 95% confidence gravitational-strength Yukawa ranges < 38.6 um.",
    },
    {
        "source_id": "SRC4173_WEB_03_MICROSCOPE_final_WEP",
        "url": "https://arxiv.org/abs/2209.15487",
        "doi_or_id": "Phys. Rev. Lett. 129, 121102 (2022); DOI 10.1103/PhysRevLett.129.121102",
        "evidence": "Ti/Pt Eotvos parameter eta = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15.",
    },
    {
        "source_id": "SRC4173_WEB_04_Galileo_redshift",
        "url": "https://arxiv.org/abs/1812.03711",
        "doi_or_id": "Phys. Rev. Lett. 121, 231101 (2018); DOI 10.1103/PhysRevLett.121.231101",
        "evidence": "Fractional redshift deviation alpha = (+0.19 +/- 2.48) x 10^-5 at 1 sigma from eccentric Galileo satellites.",
    },
    {
        "source_id": "SRC4173_WEB_05_LLR_Gdot",
        "url": "https://arxiv.org/abs/2012.12032",
        "doi_or_id": "Universe 7, 34 (2021); DOI 10.3390/universe7020034",
        "evidence": "LLR relativistic parameters include Gdot/G0 = (-5.0 +/- 9.6) x 10^-15 yr^-1.",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_url_recorded": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "doi_or_id": "",
                "evidence": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    for source in WEB_SOURCES:
        rows.append(
            {
                **common(),
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_url_recorded": str(source["url"].startswith("https://")),
                "required_text": "recorded_web_source_string",
                "required_text_found": "True",
                "doi_or_id": source["doi_or_id"],
                "evidence": source["evidence"],
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def prediction_rows() -> List[Dict[str, str]]:
    raw_rows = [
        ("PPN_gamma_minus_1", "PPN", "gamma_minus_1", 0.0, "dimensionless", "4172 R_PPN=0"),
        ("PPN_beta_minus_1", "PPN_orbital", "beta_minus_1", 0.0, "dimensionless", "4172 EH <=2PN beta=1"),
        ("PPN_xi", "PPN", "xi", 0.0, "dimensionless", "4172 preferred-location channel silent"),
        ("PPN_alpha1", "PPN_preferred_frame", "alpha1", 0.0, "dimensionless", "4172 no independent vector/projector drift"),
        ("PPN_alpha2", "PPN_preferred_frame", "alpha2", 0.0, "dimensionless", "4172 no anisotropic q-basic residual"),
        ("PPN_alpha3", "PPN_conservation", "alpha3", 0.0, "dimensionless", "4172 Hilbert stress conserved"),
        ("PPN_zeta1", "PPN_conservation", "zeta1", 0.0, "dimensionless", "4172 single Hilbert source stress"),
        ("PPN_zeta2", "PPN_conservation", "zeta2", 0.0, "dimensionless", "4172 binding stress counted once"),
        ("PPN_zeta3", "PPN_conservation", "zeta3", 0.0, "dimensionless", "4172 EM/Poynting stress carried by T_total"),
        ("PPN_zeta4", "PPN_conservation", "zeta4", 0.0, "dimensionless", "4172 pressure/internal-energy bookkeeping descends to T_total"),
        ("PPN_Gdot_over_G", "clock_orbital", "Gdot_over_G", 0.0, "yr^-1", "4172 local coupling lock"),
        ("R10_yukawa_alpha", "short_range_gravity", "alpha_Yukawa_at_lambda_38p6um", 0.0, "dimensionless", "4172 no extra finite-range local force channel inside private packet"),
        ("WEP_eta_TiPt", "WEP", "eta_TiPt", 0.0, "dimensionless", "4169 one Hilbert source measure for matter/EM/binding"),
        ("CLOCK_redshift_alpha", "clock_redshift", "redshift_violation_alpha", 0.0, "dimensionless", "4172 same observed metric clock readout"),
        ("ORBIT_perihelion_combo", "orbital", "((2+2gamma-beta)/3)-1", 0.0, "dimensionless", "gamma=1 and beta=1 from 4172"),
    ]
    return [
        {
            **common(),
            "prediction_id": prediction_id,
            "arena": arena,
            "observable": observable,
            "mts_private_prediction": f"{value:.17g}",
            "units": units,
            "source_of_prediction": source_of_prediction,
            "parent_branch_condition": "PPC4161_TK_HQNP_private_packet_adopted",
            "public_claim_result": "not_claimed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for prediction_id, arena, observable, value, units, source_of_prediction in raw_rows
    ]


def allowed_abs_from_center_sigma(center: float, sigma: float, sigma_multiplier: float = 2.0) -> float:
    return abs(center) + sigma_multiplier * sigma


def bound_rows() -> List[Dict[str, str]]:
    microscope_sigma = math.sqrt(2.3e-15**2 + 1.5e-15**2)
    rows = [
        ("B4173_00_gamma", "PPN_gamma_minus_1", "PPN", "gamma_minus_1", "abs_limit", 2.3e-5, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 time-delay/Cassini limit; Cassini central value kept in source register."),
        ("B4173_01_beta", "PPN_beta_minus_1", "PPN_orbital", "beta_minus_1", "abs_limit", 8.0e-5, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 perihelion-shift bound; beta also appears in orbital combo."),
        ("B4173_02_xi", "PPN_xi", "PPN", "xi", "abs_limit", 4.0e-9, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 spin-precession bound from millisecond pulsars."),
        ("B4173_03_alpha1", "PPN_alpha1", "PPN_preferred_frame", "alpha1", "abs_limit", 7.0e-5, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 stronger alpha1 line from PSR J1738+0333."),
        ("B4173_04_alpha2", "PPN_alpha2", "PPN_preferred_frame", "alpha2", "abs_limit", 2.0e-9, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 spin-precession bound from millisecond pulsars."),
        ("B4173_05_alpha3", "PPN_alpha3", "PPN_conservation", "alpha3", "abs_limit", 4.0e-20, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 pulsar spin-down statistics bound."),
        ("B4173_06_zeta1", "PPN_zeta1", "PPN_conservation", "zeta1", "abs_limit", 2.0e-2, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 combined PPN bound."),
        ("B4173_07_zeta2", "PPN_zeta2", "PPN_conservation", "zeta2", "abs_limit", 4.0e-5, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 binary acceleration bound for PSR 1913+16."),
        ("B4173_08_zeta3", "PPN_zeta3", "PPN_conservation", "zeta3", "abs_limit", 1.0e-8, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 lunar acceleration / Newton's third law bound."),
        ("B4173_09_zeta4", "PPN_zeta4", "PPN_conservation", "zeta4", "not_independent", math.nan, "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Table 4 marks zeta4 as not independent; no standalone numeric bound claimed."),
        ("B4173_10_Gdot", "PPN_Gdot_over_G", "clock_orbital", "Gdot_over_G", "two_sigma_envelope", allowed_abs_from_center_sigma(-5.0e-15, 9.6e-15), "yr^-1", "SRC4173_WEB_05_LLR_Gdot", "LLR result -5.0 +/- 9.6 x 10^-15 yr^-1; envelope is |center|+2sigma."),
        ("B4173_11_R10", "R10_yukawa_alpha", "short_range_gravity", "alpha_Yukawa_at_lambda_38p6um", "anchor_only_non_curve_abs_limit", 1.0, "dimensionless", "SRC4173_WEB_02_EotWash2020_R10", "Eot-Wash 95% statement: gravitational-strength Yukawa interactions limited to ranges <38.6 um; not a full curve."),
        ("B4173_12_WEP", "WEP_eta_TiPt", "WEP", "eta_TiPt", "two_sigma_envelope", allowed_abs_from_center_sigma(-1.5e-15, microscope_sigma), "dimensionless", "SRC4173_WEB_03_MICROSCOPE_final_WEP", "MICROSCOPE Ti/Pt eta with stat and systematic uncertainties combined in quadrature."),
        ("B4173_13_clock", "CLOCK_redshift_alpha", "clock_redshift", "redshift_violation_alpha", "two_sigma_envelope", allowed_abs_from_center_sigma(0.19e-5, 2.48e-5), "dimensionless", "SRC4173_WEB_04_Galileo_redshift", "Galileo eccentric satellite redshift alpha = +0.19 +/- 2.48 x 10^-5."),
        ("B4173_14_orbit_combo", "ORBIT_perihelion_combo", "orbital", "((2+2gamma-beta)/3)-1", "derived_from_gamma_beta_bounds", 2.0e-5 + (8.0e-5 / 3.0), "dimensionless", "SRC4173_WEB_00_Will2014_PPN_table", "Conservative combo tolerance from gamma and beta table limits: |2 delta_gamma - delta_beta|/3."),
    ]
    output = []
    for bound_id, prediction_id, arena, observable, bound_type, bound_abs, units, source_id, note in rows:
        output.append(
            {
                **common(),
                "bound_id": bound_id,
                "prediction_id": prediction_id,
                "arena": arena,
                "observable": observable,
                "bound_type": bound_type,
                "allowed_abs_bound": "" if math.isnan(bound_abs) else f"{bound_abs:.17g}",
                "units": units,
                "source_id": source_id,
                "source_note": note,
                "source_backed": "True",
                "full_curve_available": "False" if "anchor_only" in bound_type else "not_required",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return output


def comparator_rows() -> List[Dict[str, str]]:
    predictions = {row["prediction_id"]: float(row["mts_private_prediction"]) for row in prediction_rows()}
    rows = []
    for bound in bound_rows():
        prediction_id = bound["prediction_id"]
        predicted_abs = abs(predictions[prediction_id])
        numeric_bound = bound["allowed_abs_bound"] != ""
        if numeric_bound:
            allowed = float(bound["allowed_abs_bound"])
            within_bound = predicted_abs <= allowed
            margin_text = "infinite_zero_prediction" if predicted_abs == 0.0 else f"{allowed / predicted_abs:.17g}"
            result = "pass_private_zero_residual_against_source_bound" if within_bound else "fail_private_prediction_exceeds_bound"
        else:
            allowed = math.nan
            within_bound = True
            margin_text = "not_numeric_not_independent"
            result = "conditional_pass_not_independent_no_standalone_numeric_bound"
        rows.append(
            {
                **common(),
                "comparison_id": f"C{bound['bound_id'][1:]}",
                "prediction_id": prediction_id,
                "arena": bound["arena"],
                "observable": bound["observable"],
                "mts_private_prediction_abs": f"{predicted_abs:.17g}",
                "allowed_abs_bound": "" if math.isnan(allowed) else f"{allowed:.17g}",
                "units": bound["units"],
                "numeric_bound": str(numeric_bound),
                "within_bound_private": str(within_bound),
                "margin": margin_text,
                "result": result,
                "source_id": bound["source_id"],
                "public_claim_result": "not_claimed",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def arena_summary_rows() -> List[Dict[str, str]]:
    comparisons = comparator_rows()
    arenas = sorted({row["arena"] for row in comparisons})
    rows = []
    for arena in arenas:
        arena_rows = [row for row in comparisons if row["arena"] == arena]
        numeric_rows = [row for row in arena_rows if row["numeric_bound"] == "True"]
        all_numeric_pass = all(row["within_bound_private"] == "True" for row in numeric_rows)
        nonnumeric_rows = [row for row in arena_rows if row["numeric_bound"] == "False"]
        rows.append(
            {
                **common(),
                "arena": arena,
                "row_count": str(len(arena_rows)),
                "numeric_bound_rows": str(len(numeric_rows)),
                "nonnumeric_guard_rows": str(len(nonnumeric_rows)),
                "all_numeric_rows_pass_private": str(all_numeric_pass),
                "nonnumeric_status": "none" if not nonnumeric_rows else "kept_as_identity_or_anchor_guard",
                "public_claim_result": "not_claimed",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4173_0_private_branch", "Comparator pass is conditional on PPC4161-TK-HQNP private branch adoption."),
        ("FW4173_1_no_raw_reanalysis", "This pack compares to source-backed published limits; it is not a raw-data reanalysis."),
        ("FW4173_2_R10_curve", "R10 uses an anchor-only Yukawa statement, not a digitized full alpha(lambda) curve."),
        ("FW4173_3_zeta4", "zeta4 is recorded as not independent rather than pretending a standalone numeric bound exists."),
        ("FW4173_4_global", "No global MTS parent-action adoption, cosmology/galaxy compatibility, or public local-GR theorem is claimed."),
        ("FW4173_5_G_value", "No numerical derivation of Newton's constant is claimed; only local constancy and zero residual are compared."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_claim": blocked_claim,
            "enforcement": "claim_allowed=false_and_valid_for_claim=false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, blocked_claim in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    comparisons = comparator_rows()
    numeric = [row for row in comparisons if row["numeric_bound"] == "True"]
    return [
        {
            **common(),
            "result": DECISION,
            "PPC4161_TK_HQNP_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "source_backed_bound_pack_built": "True",
            "numeric_comparator_rows": str(len(numeric)),
            "all_numeric_rows_pass_private": str(all(row["within_bound_private"] == "True" for row in numeric)),
            "nonnumeric_guard_rows": str(len([row for row in comparisons if row["numeric_bound"] == "False"])),
            "R10_full_curve_digitized": "False",
            "raw_data_reanalysis_run": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_189_written": "True",
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why_next": "4173 shows the private local branch has source-backed numeric bound compatibility; next is deciding whether the parent action truly adopts this local branch globally or keeps it quarantined.",
            "route_A": "derive parent-action adoption of PPC4161-TK-HQNP without closure smuggling",
            "route_B": "if global parent adoption cannot be derived, write an explicit quarantine/sector-map contract so local GR remains private but disciplined",
            "fallback": "future empirical upgrade can replace R10 anchor-only row with a digitized alpha(lambda) curve and raw-data tests",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4173_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4173_PRIVATE_PREDICTION_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4173_PRIVATE_PREDICTION_VECTOR.csv",
        "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE": SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv",
        "P8_Y5_R2FR_4173_COMPARATOR_RESULTS": SOURCE_DIR / "P8_Y5_R2FR_4173_COMPARATOR_RESULTS.csv",
        "P8_Y5_R2FR_4173_ARENA_SUMMARY": SOURCE_DIR / "P8_Y5_R2FR_4173_ARENA_SUMMARY.csv",
        "P8_Y5_R2FR_4173_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4173_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4173_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4173_STATUS.csv",
        "P8_Y5_R2FR_4173_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4173_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161-TK-HQNP private branch gives zero local residuals that pass the 4173 source-backed PPN, R10-anchor, WEP, clock-redshift, Gdot/G and orbital-combo comparator rows",
        "current_evidence": "formalization-workbench/189-PPC4161-local-empirical-validation-pack.md records source-backed bound rows from Will 2014 PPN Table 4, Eot-Wash 2020 R10, MICROSCOPE 2022 WEP, Galileo redshift, and LLR Gdot/G; all numeric private residual rows compare as zero <= bound; public_claim=false",
        "status": "private_packet_source_bound_comparator_pass_nonclaim_public_claim_false",
        "next_test": "Derive parent-action global adoption of PPC4161-TK-HQNP or write an explicit local-branch quarantine contract",
        "key_risk": "This is a source-bound comparator, not raw-data reanalysis or global MTS adoption; R10 is anchor-only and zeta4 has no standalone numeric bound",
    }
    normalized_new = {field: new_row.get(field, "") for field in fieldnames}
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    if existing:
        changed = False
        for row in rows:
            if row.get("claim_id") == CLAIM_ID:
                for field, value in normalized_new.items():
                    if row.get(field) != value:
                        row[field] = value
                        changed = True
        action = "updated" if changed else "already_present"
    else:
        rows.append(normalized_new)
        action = "added"

    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return action


def append_once(path: Path, marker: str, section: str) -> str:
    text = read_text(path)
    if marker in text:
        return "already_present"
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")
    return "added"


def ensure_packet_180_addendum() -> str:
    section = f"""
## PPC4161-TK-HQNP Addendum - Local Empirical Validation Pack

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4173-Y5-R2FR-local-empirical-PPN-R10-clock-WEP-orbital-validation-pack.md`

The private packet prediction vector is now compared against source-backed local bounds:

```text
gamma-1 = beta-1 = alpha1 = alpha2 = alpha3 = xi = zeta1 = zeta2 = zeta3 = zeta4 = 0,
Gdot/G = 0,
alpha_Yukawa = 0,
eta_TiPt = 0,
redshift_violation_alpha = 0.
```

Every numeric comparator row passes because the private residual is exactly zero. The result is not a public local-GR claim because the parent action has not yet been shown to globally force this branch, the R10 row is anchor-only rather than a full digitized curve, and no raw experimental data reanalysis is performed here.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Source-Backed Local Empirical Validation Pack - 4173

Marker: `{SPINE_MARKER}`  
Source bridge: `189-PPC4161-local-empirical-validation-pack.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4173` compares the private PPC4161-TK-HQNP zero-residual vector against source-backed local bounds:

```text
PPN gamma/beta/alpha_i/xi/zeta_i,
Gdot/G,
R10 Yukawa anchor,
MICROSCOPE WEP eta,
Galileo redshift alpha,
orbital perihelion combo.
```

All numeric rows pass inside the private branch because the predicted local residuals are zero. This improves the local-GR route from symbolic closure to source-bound compatibility, but it remains a private nonclaim until parent-action adoption and/or quarantine is handled:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_189() -> None:
    FORMAL_189_PATH.write_text(
        f"""# 189 - PPC4161 Local Empirical Validation Pack

Marker: `PPC4161_LOCAL_EMPIRICAL_VALIDATION_PACK_FROM_PRIVATE_ZERO_RESIDUALS`
Checkpoint: `4173`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private nonclaim. This file records a source-backed comparator pack, not a raw-data reanalysis and not a public local-GR theorem.

## Private Prediction Vector

```text
R_PPN = 0,
Gdot/G = 0,
alpha_Yukawa = 0,
eta_TiPt = 0,
redshift_violation_alpha = 0,
((2+2gamma-beta)/3)-1 = 0.
```

## Source-Backed Bound Classes
- PPN table limits from Clifford Will's Living Reviews/arXiv 2014 review.
- Short-range R10 anchor from Eot-Wash 2020.
- WEP eta from MICROSCOPE final 2022 result.
- Clock-redshift alpha from eccentric Galileo satellites.
- Local Gdot/G from Lunar Laser Ranging.

## Comparator Result
Every numeric row satisfies:

```text
abs(MTS_private_prediction) <= allowed_abs_bound.
```

The only nonnumeric guard row is `zeta4`, which Will's table records as not independent. It is therefore not fabricated as a standalone numeric pass.

## Remaining Firewall
The result is still not a public claim because:

```text
PPC4161-TK-HQNP is private branch adoption;
R10 is anchor-only here, not a full alpha(lambda) curve;
no raw experimental data reanalysis is run;
global MTS parent-action adoption is still open.
```

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4173 - Local Empirical PPN/R10/Clock/WEP/Orbital Validation Pack

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4172 closed the private GR-like local PPN vector. 4173 now does the empirical bound comparison against source-backed published limits.

## Comparator Logic
For each numeric bound row:

```text
abs(private_MTS_residual) <= source_backed_bound.
```

The private branch prediction is zero for all local residual rows, so the numeric rows pass. This is exactly what a local-GR limit should do: not beat GR by being dramatic, but avoid leaking any extra measurable local force, clock, WEP or PPN term.

## Source Classes
- Will 2014 PPN table for `gamma`, `beta`, `alpha_i`, `xi`, `zeta_i`.
- Eot-Wash 2020 R10 short-range inverse-square anchor.
- MICROSCOPE 2022 final WEP eta.
- Galileo eccentric-satellite redshift alpha.
- LLR `Gdot/G`.

## Nonclaim Guard
This is not a public local-GR claim. It is a source-bound compatibility pack for the private branch. R10 is anchor-only, `zeta4` is not independently numeric, and no raw data reanalysis is performed.

## Next Target
`{NEXT_TARGET}`

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def validate(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    checks: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, details: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(passed),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = parse_csv(outputs["P8_Y5_R2FR_4173_SOURCE_REGISTER"])
    add("VAL4173_0_sources", "all local source paths exist and all web source strings are recorded", all(row["exists_or_url_recorded"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))
    add("VAL4173_1_web_sources", "web source set includes Will, Cassini, Eot-Wash, MICROSCOPE, Galileo and LLR", all(any(token in row["source_id"] for row in sources) for token in ["Will2014", "Cassini", "EotWash", "MICROSCOPE", "Galileo", "LLR"]), "\n".join(row["source_id"] for row in sources))

    predictions = parse_csv(outputs["P8_Y5_R2FR_4173_PRIVATE_PREDICTION_VECTOR"])
    prediction_text = "\n".join(",".join(row.values()) for row in predictions)
    add("VAL4173_2_predictions", "prediction vector includes PPN, R10, WEP, clock and orbital rows with zero private residuals", all(token in prediction_text for token in ["gamma_minus_1", "beta_minus_1", "alpha_Yukawa", "eta_TiPt", "redshift_violation_alpha", "((2+2gamma-beta)/3)-1"]) and all(float(row["mts_private_prediction"]) == 0.0 for row in predictions), prediction_text)

    bounds = parse_csv(outputs["P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE"])
    bound_text = "\n".join(",".join(row.values()) for row in bounds)
    numeric_bounds = [row for row in bounds if row["allowed_abs_bound"] != ""]
    add("VAL4173_3_bounds", "bound table contains positive numeric source-backed bounds plus zeta4 non-independent guard", len(bounds) == 15 and len(numeric_bounds) == 14 and all(float(row["allowed_abs_bound"]) > 0 for row in numeric_bounds) and "not_independent" in bound_text, bound_text)

    comparisons = parse_csv(outputs["P8_Y5_R2FR_4173_COMPARATOR_RESULTS"])
    numeric_comparisons = [row for row in comparisons if row["numeric_bound"] == "True"]
    nonnumeric_comparisons = [row for row in comparisons if row["numeric_bound"] == "False"]
    add("VAL4173_4_comparator", "all numeric comparator rows pass and one nonnumeric zeta4 guard remains", len(numeric_comparisons) == 14 and all(row["within_bound_private"] == "True" for row in numeric_comparisons) and len(nonnumeric_comparisons) == 1 and nonnumeric_comparisons[0]["observable"] == "zeta4", str(comparisons))

    arena = parse_csv(outputs["P8_Y5_R2FR_4173_ARENA_SUMMARY"])
    arena_text = "\n".join(",".join(row.values()) for row in arena)
    add("VAL4173_5_arenas", "arena summary includes PPN, R10, WEP, clock and orbital classes and all numeric rows pass", all(token in arena_text for token in ["PPN", "short_range_gravity", "WEP", "clock_redshift", "orbital"]) and all(row["all_numeric_rows_pass_private"] == "True" for row in arena), arena_text)

    firewall = parse_csv(outputs["P8_Y5_R2FR_4173_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4173_6_firewall", "firewall blocks private-branch, raw-reanalysis, R10-curve, zeta4, global and numeric-G overclaims", all(token in firewall_text for token in ["private branch", "raw-data", "R10", "zeta4", "global MTS", "Newton's constant"]), firewall_text)

    formal_text = read_text(FORMAL_189_PATH)
    add("VAL4173_7_formal_189", "formal 189 records comparator result, nonnumeric guard, firewall and next target", FORMAL_189_PATH.exists() and all(token in formal_text for token in ["PPC4161_LOCAL_EMPIRICAL_VALIDATION_PACK_FROM_PRIVATE_ZERO_RESIDUALS", "abs(MTS_private_prediction) <= allowed_abs_bound", "zeta4", "R10 is anchor-only", NEXT_TARGET]), "formal 189 checked")

    packet_text = read_text(PACKET_180_PATH)
    add("VAL4173_8_packet_180", "packet 180 contains local empirical validation addendum", all(token in packet_text for token in [PACKET_MARKER, "alpha_Yukawa = 0", "eta_TiPt = 0", "redshift_violation_alpha = 0"]), "packet 180 checked")

    claims = parse_csv(CLAIMS_PATH)
    l014 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4173_9_claim_row", "claims register contains one L-014 source-bound comparator nonclaim row", len(l014) == 1 and l014[0].get("status") == "private_packet_source_bound_comparator_pass_nonclaim_public_claim_false" and "public_claim=false" in l014[0].get("current_evidence", ""), str(l014))

    spine_text = read_text(SPINE_PATH)
    add("VAL4173_10_spine", "spine contains 4173 marker, claim row and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "All numeric rows pass", NEXT_TARGET]), "spine checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4173_STATUS"])
    add("VAL4173_11_status", "status records source-bound pack built, numeric rows pass, public claim false and next target", len(status) == 1 and status[0]["source_backed_bound_pack_built"] == "True" and status[0]["all_numeric_rows_pass_private"] == "True" and status[0]["public_local_GR_claim_allowed"] == "False" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4173_NEXT_TARGET"])
    add("VAL4173_12_next", "next target moves to parent action adoption or explicit quarantine", len(next_loaded) == 1 and next_loaded[0]["next_target"] == NEXT_TARGET and "parent-action adoption" in "\n".join(next_loaded[0].values()), str(next_loaded))

    doc_text = read_text(DOC_PATH)
    add("VAL4173_13_doc", "checkpoint doc records comparator logic, sources, nonclaim guard and next target", all(token in doc_text for token in ["Comparator Logic", "Will 2014", "Eot-Wash 2020", "MICROSCOPE 2022", "not a public local-GR claim", NEXT_TARGET]), "doc checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4173_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_details = "compiled"
    except Exception as exc:
        compile_ok = False
        compile_details = repr(exc)
    finally:
        cache = SCRIPT_PATH.parent / "__pycache__"
        if cache.exists():
            shutil.rmtree(cache)
    add("VAL4173_15_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def write_outputs(outputs: Dict[str, Path]) -> None:
    write_csv(outputs["P8_Y5_R2FR_4173_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_PRIVATE_PREDICTION_VECTOR"], prediction_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_COMPARATOR_RESULTS"], comparator_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_ARENA_SUMMARY"], arena_summary_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4173_NEXT_TARGET"], next_rows())


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_189()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_outputs(outputs)
    write_csv(outputs["P8_Y5_R2FR_4173_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4173_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_189_PATH}")
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['details']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
