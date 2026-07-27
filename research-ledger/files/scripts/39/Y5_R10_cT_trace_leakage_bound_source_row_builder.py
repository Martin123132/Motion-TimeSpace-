from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST_CHECKPOINT / "source-intake" / "local_bounds"

OUTPUT_DOC = POST_CHECKPOINT / "871-Y5-R10-cT-trace-leakage-bound-source-row-builder.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_871_SOURCE_REGISTER.csv"
BOUND_SOURCE_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv"
CT_PROJECTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_871_CT_PROJECTION_CONTRACT.csv"
CT_BOUND_ROWS_PATH = RESIDUALS / "P8_Y5_R10_871_CT_BOUND_ROWS.csv"
CLAIM_READINESS_PATH = RESIDUALS / "P8_Y5_R10_871_CLAIM_READINESS.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_871_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_871_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_871_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_871_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_871_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_871_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_870_VALIDATION.csv"
LOCAL_BOUND_SOURCE_MAP = (
    POST_CHECKPOINT
    / "runs"
    / "20260530-232024-local-observables-data-map"
    / "results"
    / "published_bound_sources.csv"
)

STATUS = "Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim"
CLAIM_CEILING = "source_ready_cT_bound_ledger_only_no_R10_PPN_clock_WEP_or_orbital_pass"
NEXT_TARGET = "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    BOUND_SOURCE_CANDIDATES_PATH,
    CT_PROJECTION_CONTRACT_PATH,
    CT_BOUND_ROWS_PATH,
    CLAIM_READINESS_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "870_doc",
        "path": POST_CHECKPOINT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needles": [
            "CT870_0_alpha_lambda",
            "D870_2",
            "871-Y5-R10-cT-trace-leakage-bound-source-row-builder.md",
        ],
        "role": "immediate c_T trace leakage handoff",
    },
    {
        "source_id": "870_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V870_4_cT_bound_rows_ready,pass",
            "V870_8_all_rows_nonclaim,pass",
            "V870_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "563_R10_anchor",
        "path": POST_CHECKPOINT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "needles": [
            "EOTWASH_2020_PRL124101101",
            "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            "full_2020_Eot_Wash_alpha_lambda_curve",
        ],
        "role": "real R10 anchor source hierarchy and full-curve blocker",
    },
    {
        "source_id": "15_local_observables",
        "path": POST_CHECKPOINT / "15-local-observables-data-map.md",
        "needles": [
            "Cassini radio science",
            "MICROSCOPE final WEP result",
            "published bounds mapped",
        ],
        "role": "published PPN, clock, WEP local observable gates",
    },
    {
        "source_id": "15_published_bound_sources",
        "path": LOCAL_BOUND_SOURCE_MAP,
        "needles": [
            "cassini_bertotti_2003",
            "galileo_delva_2018",
            "microscope_touboul_2022",
        ],
        "role": "local source URL ledger for published observable gates",
    },
    {
        "source_id": "393_Newton_source",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "G_eff = kappa_eff c^4/(8 pi)",
            "constant universal",
            "Newtonian/local-GR promoted",
        ],
        "role": "source-normalized Newtonian limit and GM absorption blocker",
    },
    {
        "source_id": "179_PPN_silence",
        "path": POST_CHECKPOINT / "179-local-GR-PPN-silence-contract.md",
        "needles": [
            "q_loc^nu -> 0",
            "gamma = beta = 1",
            "screened effective, not derived",
        ],
        "role": "PPN silence target and q_loc blocker",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def bound_source_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": "SRC871_R10_EOTWASH_2020_ANCHOR",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)_Yukawa_strength",
            "source_title": "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
            "year": "2020",
            "source_url": "https://arxiv.org/abs/2002.11761; https://pubmed.ncbi.nlm.nih.gov/32216404/",
            "doi": "10.1103/PhysRevLett.124.101101",
            "extraction_method": "anchor_only_alpha_equals_1_threshold_from_563_source_hierarchy",
            "source_status": "anchor_only_noncurve",
            "units": "lambda:m; alpha:dimensionless",
            "usable_as": "provenance_and_smoke_anchor_only",
            "valid_for_claim": "false",
            "notes": "Full alpha(lambda) curve still absent; do not score a c_T claim from this anchor.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_R10_EOTWASH_2007_ANCHOR",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)_Yukawa_strength",
            "source_title": "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale",
            "year": "2007",
            "source_url": "https://arxiv.org/abs/hep-ph/0611184; https://link.aps.org/doi/10.1103/PhysRevLett.98.021101",
            "doi": "10.1103/PhysRevLett.98.021101",
            "extraction_method": "anchor_only_abs_alpha_le_1_threshold_from_563_source_hierarchy",
            "source_status": "continuity_anchor_only_noncurve",
            "units": "lambda:m; alpha:dimensionless",
            "usable_as": "historical_continuity_and_smoke_anchor_only",
            "valid_for_claim": "false",
            "notes": "Older threshold anchor; useful for plumbing but not a modern claim curve.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_PPN_CASSINI_GAMMA",
            "arena": "PPN_radio_science",
            "observable": "gamma_minus_one",
            "source_title": "Cassini radio-link Shapiro delay gamma constraint",
            "year": "2003",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/; https://doi.org/10.1038/nature01997",
            "doi": "10.1038/nature01997",
            "extraction_method": "published_bound_source_map_and_direct_citation",
            "source_status": "source_candidate_numeric_bound_available",
            "units": "dimensionless",
            "usable_as": "PPN gamma bound only after c_T_to_gamma projection exists",
            "valid_for_claim": "false",
            "notes": "Local map records gamma=1+(2.1+/-2.3)e-5; projection from c_T is missing.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_PPN_INPOP20A_BETA_GAMMA",
            "arena": "PPN_planetary_ephemerides",
            "observable": "beta_minus_one_and_gamma_minus_one",
            "source_title": "INPOP20a planetary ephemerides conservative PPN intervals",
            "year": "2021",
            "source_url": "https://arxiv.org/abs/2111.04499",
            "doi": "not_recorded_in_15_source_map",
            "extraction_method": "published_bound_source_map",
            "source_status": "source_candidate_numeric_bound_available",
            "units": "dimensionless",
            "usable_as": "planetary PPN cross-check after c_T projection exists",
            "valid_for_claim": "false",
            "notes": "Local map records beta and gamma conservative intervals; not a raw likelihood.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_CLOCK_GALILEO_REDSHIFT",
            "arena": "clock_redshift",
            "observable": "redshift_fractional_deviation",
            "source_title": "Galileo eccentric-satellite gravitational redshift test",
            "year": "2018",
            "source_url": "https://arxiv.org/abs/1812.03711",
            "doi": "not_recorded_in_15_source_map",
            "extraction_method": "published_bound_source_map",
            "source_status": "source_candidate_numeric_bound_available",
            "units": "dimensionless_fractional_deviation",
            "usable_as": "clock/load anomaly gate after c_T_to_clock projection exists",
            "valid_for_claim": "false",
            "notes": "Local map records (+0.19 +/- 2.48)e-5; projection from trace leakage to clock observable is absent.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_WEP_MICROSCOPE_FINAL",
            "arena": "weak_equivalence_principle",
            "observable": "eta_Ti_Pt",
            "source_title": "MICROSCOPE mission final WEP result",
            "year": "2022",
            "source_url": "https://arxiv.org/abs/2209.15487; https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "doi": "10.1103/PhysRevLett.129.121102",
            "extraction_method": "published_bound_source_map_and_PRL_source_candidate",
            "source_status": "source_candidate_numeric_bound_available",
            "units": "dimensionless_Eotvos_ratio",
            "usable_as": "WEP/composition coupling gate after species projection exists",
            "valid_for_claim": "false",
            "notes": "Local map records quadrature proxy 2.745906043549196e-15; c_T composition projection is missing.",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "SRC871_ORBITAL_LLR_REVIEW",
            "arena": "orbital_lunar_laser_ranging",
            "observable": "Gdot_over_G_or_anomalous_radial_acceleration",
            "source_title": "Tests of Gravity Using Lunar Laser Ranging",
            "year": "2010",
            "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/",
            "doi": "10.12942/lrr-2010-7",
            "extraction_method": "source_candidate_review_context_only",
            "source_status": "review_candidate_no_numeric_row_extracted",
            "units": "arena_dependent",
            "usable_as": "orbital source hierarchy only until numeric observable and c_T projection are selected",
            "valid_for_claim": "false",
            "notes": "Use to choose a source-normalization/orbital bound, not as a direct c_T claim row.",
            "generated_utc": generated_utc,
        },
    ]


def ct_projection_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "projection_id": "PC871_0_R10_alpha_lambda",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha_T(lambda)",
            "input_cT_piece": "c_T * P_loc J_trace finite-range scalar component",
            "required_formula": "alpha_T(lambda)=F_T[c_T,lambda_T,G_eff,M_eff,source_geometry]",
            "current_status": "blocked_projection_missing_and_full_curve_missing",
            "missing_inputs": "parent c_T coefficient; lambda_T/mass gap; source-normalized coupling; full alpha(lambda) curve",
            "claim_consequence": "R10/fifth-force claim forbidden; anchors are smoke-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "PC871_1_PPN_gamma_beta",
            "arena": "PPN_solar_system",
            "observable": "gamma-1,beta-1",
            "input_cT_piece": "local scalar trace leakage in metric potentials",
            "required_formula": "gamma-1=G_T_gamma*c_T and beta-1=G_T_beta*c_T plus source-normalization terms",
            "current_status": "blocked_parent_response_operator_missing",
            "missing_inputs": "metric response operator; gauge fixing; source-normalization residual split; degeneracy with c_S",
            "claim_consequence": "PPN/local-GR claim forbidden",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "PC871_2_clock_WEP",
            "arena": "clock_and_WEP",
            "observable": "clock drift and eta composition charge",
            "input_cT_piece": "trace leakage into matter clocks/species markers",
            "required_formula": "delta_nu/nu=C_T_clock*c_T and eta_AB=C_T_AB*c_T",
            "current_status": "blocked_species_marker_projection_missing",
            "missing_inputs": "matter action descent; species marker/no-marker theorem; clock functional; c_e separation",
            "claim_consequence": "clock/WEP claim forbidden",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "PC871_3_orbital_GM",
            "arena": "orbital_dynamics",
            "observable": "Gdot/G,delta_GM,anomalous_radial_acceleration",
            "input_cT_piece": "trace leakage into observed source normalization",
            "required_formula": "delta_mu/mu=C_T_mu*c_T with mu_obs=G_eff*M_eff+mu_extra",
            "current_status": "blocked_source_normalization_missing",
            "missing_inputs": "constant universal absorption proof; time constancy; source geometry; separation from c_S",
            "claim_consequence": "Newton/orbital/local-GR claim forbidden",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ct_bound_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)",
            "bound_value": "1.0",
            "bound_units": "dimensionless_alpha",
            "lambda_value": "3.86e-5",
            "lambda_units": "m",
            "confidence": "95_percent",
            "source_id": "SRC871_R10_EOTWASH_2020_ANCHOR",
            "source_path_or_url": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM; https://arxiv.org/abs/2002.11761",
            "extraction_status": "anchor_only_noncurve",
            "projection_status": "missing_cT_to_alpha_projection",
            "valid_for_claim": "false",
            "notes": "Positive numeric source-backed threshold anchor, deliberately invalid for claim scoring.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_R10_EOTWASH_2007_ALPHA1_56UM_ANCHOR",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)",
            "bound_value": "1.0",
            "bound_units": "dimensionless_alpha",
            "lambda_value": "5.6e-5",
            "lambda_units": "m",
            "confidence": "95_percent",
            "source_id": "SRC871_R10_EOTWASH_2007_ANCHOR",
            "source_path_or_url": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM; https://arxiv.org/abs/hep-ph/0611184",
            "extraction_status": "anchor_only_noncurve",
            "projection_status": "missing_cT_to_alpha_projection",
            "valid_for_claim": "false",
            "notes": "Continuity anchor only; not a full bound curve and not a claim row.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_PPN_CASSINI_GAMMA_SIGMA",
            "arena": "PPN_radio_science",
            "observable": "gamma_minus_one",
            "bound_value": "2.3e-5",
            "bound_units": "dimensionless_1sigma",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "confidence": "1sigma_published_uncertainty",
            "source_id": "SRC871_PPN_CASSINI_GAMMA",
            "source_path_or_url": "15-local-observables-data-map.md::Cassini radio science; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::cassini_bertotti_2003",
            "extraction_status": "numeric_published_bound_available",
            "projection_status": "missing_cT_to_gamma_projection",
            "valid_for_claim": "false",
            "notes": "Bound exists but is not a c_T bound until the response coefficient is derived.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_PPN_INPOP20A_BETA_INTERVAL",
            "arena": "PPN_planetary_ephemerides",
            "observable": "beta_minus_one",
            "bound_value": "7.16e-5",
            "bound_units": "dimensionless_conservative_interval",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "confidence": "conservative_acceptable_interval",
            "source_id": "SRC871_PPN_INPOP20A_BETA_GAMMA",
            "source_path_or_url": "15-local-observables-data-map.md::INPOP20a planetary ephemerides; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::inpop20a_fienga_2021",
            "extraction_status": "numeric_published_bound_available",
            "projection_status": "missing_cT_to_beta_projection",
            "valid_for_claim": "false",
            "notes": "Conservative PPN gate only; not a one-parameter c_T likelihood.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_CLOCK_GALILEO_REDSHIFT_SIGMA",
            "arena": "clock_redshift",
            "observable": "redshift_fractional_deviation",
            "bound_value": "2.48e-5",
            "bound_units": "dimensionless_1sigma_fractional_deviation",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "confidence": "1sigma_published_uncertainty",
            "source_id": "SRC871_CLOCK_GALILEO_REDSHIFT",
            "source_path_or_url": "15-local-observables-data-map.md::Galileo eccentric satellites; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::galileo_delva_2018",
            "extraction_status": "numeric_published_bound_available",
            "projection_status": "missing_cT_to_clock_projection",
            "valid_for_claim": "false",
            "notes": "Clock bound is source-ready but the MTS clock functional is not derived.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_WEP_MICROSCOPE_ETA_PROXY",
            "arena": "weak_equivalence_principle",
            "observable": "eta_Ti_Pt",
            "bound_value": "2.745906043549196e-15",
            "bound_units": "dimensionless_Eotvos_quadrature_proxy",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "confidence": "combined_1sigma_proxy_from_stat_syst",
            "source_id": "SRC871_WEP_MICROSCOPE_FINAL",
            "source_path_or_url": "15-local-observables-data-map.md::MICROSCOPE final WEP result; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::microscope_touboul_2022",
            "extraction_status": "numeric_published_bound_available",
            "projection_status": "missing_cT_species_marker_projection",
            "valid_for_claim": "false",
            "notes": "WEP bound is very sharp; precisely why the species/no-marker theorem cannot be hand-waved.",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT871_ORBITAL_LLR_REVIEW_PLACEHOLDER",
            "arena": "orbital_lunar_laser_ranging",
            "observable": "Gdot_over_G_or_anomalous_radial_acceleration",
            "bound_value": "MISSING_NUMERIC_ORBITAL_BOUND_SELECTION",
            "bound_units": "arena_dependent",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "confidence": "not_selected",
            "source_id": "SRC871_ORBITAL_LLR_REVIEW",
            "source_path_or_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/",
            "extraction_status": "review_candidate_no_numeric_row_extracted",
            "projection_status": "missing_cT_to_GM_or_acceleration_projection",
            "valid_for_claim": "false",
            "notes": "Kept as an acquisition row only; choose a specific orbital observable before any calculator.",
            "generated_utc": generated_utc,
        },
    ]


def claim_readiness_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CR871_0_parent_cT_projection",
            "required_for_claim": "derive c_T from parent action or prove c_T=0",
            "status": "blocked",
            "reason": "870 left P_loc J_trace no-hair unsigned; 871 only stages external gates",
            "next_action": "derive c_T response coefficient or theorem-zero return",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CR871_1_R10_full_curve",
            "required_for_claim": "full positive numeric alpha(lambda) curve or official table",
            "status": "blocked",
            "reason": "563 has only alpha=1 threshold anchors",
            "next_action": "digitize/source PRL 2020 curve before any R10 score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CR871_2_source_normalization",
            "required_for_claim": "map trace leakage through G_eff,M_eff,GM absorption without hiding a force",
            "status": "blocked",
            "reason": "393 source-normalized Newtonian branch is conditional only",
            "next_action": "derive constant universal absorption or keep c_S/c_T residual split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CR871_3_matter_marker_silence",
            "required_for_claim": "prove c_T does not induce species-dependent clocks/WEP charge",
            "status": "blocked",
            "reason": "clock/WEP gates are sharp and matter descent is not parent-signed",
            "next_action": "connect c_T to matter descent/no-marker theorem or bound it explicitly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC871_0_selected",
            "route": "cT_parent_projection_coefficient_or_theorem_zero_return",
            "status": "selected",
            "reason": "source rows now exist; the missing object is not more data but the parent map from P_loc J_trace to observables",
            "include": "derive c_T response coefficient, prove c_T=0, or write exact closure status if neither works",
            "exclude": "claim scoring, local GR pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG871_0_no_cT_bound_claim",
            "claim": "c_T is bounded by R10/PPN/clock/WEP/orbital tests",
            "status": "forbidden",
            "reason": "external bounds are source-ready but c_T observable projection is missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG871_1_no_R10_claim",
            "claim": "R10/fifth-force pass",
            "status": "forbidden",
            "reason": "only threshold anchors exist and parent alpha_T(lambda) is absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG871_2_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "c_T is only one retained q_loc channel and source normalization remains conditional",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG871_3_allowed_private_result",
            "claim": "c_T bound source rows are staged and all claim gates remain closed",
            "status": "allowed_private_nonclaim",
            "reason": "871 improves test plumbing without overstating theory status",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D871_0",
            "finding": "cT_bound_sources_staged",
            "reason": "R10 anchors plus PPN, clock, WEP, and orbital source candidates are recorded with units and provenance",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D871_1",
            "finding": "parent_projection_missing_is_now_primary_blocker",
            "reason": "without F_T from c_T/P_loc J_trace to observable amplitudes, data cannot decide the local branch",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D871_2",
            "finding": "the_coupling_is_the_fight",
            "reason": "local tests are not the weak part of the plumbing; the weak part is the coupling/projection coefficient",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive the c_T parent projection coefficient from P_loc J_trace to alpha(lambda), PPN, clock/WEP, and orbital observables, or prove c_T=0",
            "include": "parent variation, response operator, source normalization, matter descent/no-marker clauses, theorem-zero fallback",
            "exclude": "claim rows, fitted shortcuts, hidden calibration, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "built a c_T source/bound ledger across R10, PPN, clocks/WEP, and orbital channels",
            "best_partial_result": "the data gates are now explicit and nonclaim; R10 anchor rows are positive numeric smoke anchors",
            "hard_blockers": "parent c_T projection coefficient, full R10 curve, source normalization, matter marker silence",
            "what_is_not_claimed": "c_T bound, c_T zero, R10 pass, PPN pass, clock/WEP pass, orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def any_valid_for_claim_true(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            return True
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("valid_for_claim", "").strip().lower() == "true":
                    return True
    return False


def no_valid_claim_row_has_missing(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("valid_for_claim", "").strip().lower() != "true":
                    continue
                joined = " ".join(str(value) for value in row.values())
                if "MISSING_" in joined or "missing_" in joined.lower():
                    offenders.append(f"{path.name}:{row}")
    if offenders:
        return False, "; ".join(offenders[:5])
    return True, "no valid_for_claim=true row contains missing markers"


def r10_anchors_positive_numeric(rows: list[dict[str, object]]) -> tuple[bool, str]:
    r10_rows = [row for row in rows if str(row["bound_id"]).startswith("CT871_R10")]
    problems: list[str] = []
    for row in r10_rows:
        try:
            lambda_value = float(str(row["lambda_value"]))
            bound_value = float(str(row["bound_value"]))
        except ValueError:
            problems.append(f"{row['bound_id']} nonnumeric")
            continue
        if lambda_value <= 0 or bound_value <= 0:
            problems.append(f"{row['bound_id']} nonpositive")
        if row["valid_for_claim"] != "false":
            problems.append(f"{row['bound_id']} promoted")
    if problems:
        return False, ";".join(problems)
    return True, f"r10_anchor_rows={len(r10_rows)} positive numeric and nonclaim"


def build_validation_rows(
    source_rows: list[dict[str, object]],
    source_candidate_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
) -> list[dict[str, str]]:
    validation_rows: list[dict[str, str]] = []

    sources_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    validation_rows.append(
        {
            "check_id": "V871_0_sources_exist_and_needles",
            "result": "pass" if sources_ok else "fail",
            "detail": "all source paths exist and needles are present" if sources_ok else "one or more source checks failed",
        }
    )

    prior_ok, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    validation_rows.append(
        {
            "check_id": "V871_1_prior_870_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": prior_detail,
        }
    )

    source_urls_ok = all(row["source_url"] and row["valid_for_claim"] == "false" for row in source_candidate_rows)
    validation_rows.append(
        {
            "check_id": "V871_2_source_candidates_nonclaim_with_urls",
            "result": "pass" if source_urls_ok else "fail",
            "detail": f"source_candidates={len(source_candidate_rows)} nonclaim with URLs",
        }
    )

    anchors_ok, anchors_detail = r10_anchors_positive_numeric(bound_rows)
    validation_rows.append(
        {
            "check_id": "V871_3_R10_anchor_rows_positive_numeric_nonclaim",
            "result": "pass" if anchors_ok else "fail",
            "detail": anchors_detail,
        }
    )

    projection_blocked = all("blocked" in row["current_status"] for row in projection_rows)
    validation_rows.append(
        {
            "check_id": "V871_4_projection_contract_blocks_claim",
            "result": "pass" if projection_blocked else "fail",
            "detail": "all c_T observable projections remain blocked by missing parent inputs",
        }
    )

    readiness_blocked = all(row["status"] == "blocked" for row in readiness_rows)
    validation_rows.append(
        {
            "check_id": "V871_5_claim_readiness_blocked",
            "result": "pass" if readiness_blocked else "fail",
            "detail": "all claim readiness gates remain blocked",
        }
    )

    no_missing_valid_ok, no_missing_valid_detail = no_valid_claim_row_has_missing(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V871_6_no_valid_claim_row_has_missing_markers",
            "result": "pass" if no_missing_valid_ok else "fail",
            "detail": no_missing_valid_detail,
        }
    )

    claim_false = all(row["claim_allowed"] == "false" for row in decision_rows_value)
    validation_rows.append(
        {
            "check_id": "V871_7_claim_allowed_false",
            "result": "pass" if claim_false else "fail",
            "detail": "decision rows keep claim_allowed=false",
        }
    )

    all_nonclaim = not any_valid_for_claim_true(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V871_8_all_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )

    formalization_count = formalization_workbench_modified_count()
    validation_rows.append(
        {
            "check_id": "V871_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        }
    )

    validation_rows.append(
        {
            "check_id": "V871_10_route_selected",
            "result": "pass",
            "detail": NEXT_TARGET,
        }
    )

    validation_rows.append(
        {
            "check_id": "V871_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        }
    )

    return validation_rows


def markdown_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(field, "")) for field in fieldnames) + " |")
    return "\n".join(lines) + "\n"


def write_output_doc(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    source_candidate_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    source_fields = ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"]
    candidate_fields = [
        "source_id",
        "arena",
        "observable",
        "source_title",
        "year",
        "source_url",
        "doi",
        "extraction_method",
        "source_status",
        "units",
        "usable_as",
        "valid_for_claim",
        "notes",
        "generated_utc",
    ]
    projection_fields = [
        "projection_id",
        "arena",
        "observable",
        "input_cT_piece",
        "required_formula",
        "current_status",
        "missing_inputs",
        "claim_consequence",
        "valid_for_claim",
        "generated_utc",
    ]
    bound_fields = [
        "bound_id",
        "arena",
        "observable",
        "bound_value",
        "bound_units",
        "lambda_value",
        "lambda_units",
        "confidence",
        "source_id",
        "source_path_or_url",
        "extraction_status",
        "projection_status",
        "valid_for_claim",
        "notes",
        "generated_utc",
    ]
    readiness_fields = ["gate_id", "required_for_claim", "status", "reason", "next_action", "valid_for_claim", "generated_utc"]
    route_fields = ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"]
    guard_fields = ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"]
    decision_fields = ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"]
    next_fields = ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"]
    summary_fields = [
        "status",
        "claim_ceiling",
        "what_changed",
        "best_partial_result",
        "hard_blockers",
        "what_is_not_claimed",
        "next_target",
        "valid_for_claim",
        "generated_utc",
    ]
    validation_fields = ["check_id", "result", "detail"]

    doc = "\n".join(
        [
            "# 871 - Y5/R10 c_T Trace Leakage Bound Source Row Builder",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Generated UTC: `{generated_utc}`",
            "",
            "Current result: **the c_T coupling is now source-ready but not theory-ready**. R10 anchors, Cassini/INPOP PPN gates, Galileo clock redshift, MICROSCOPE WEP, and LLR/orbital source candidates are staged with units and provenance. None of them becomes a c_T bound because the parent projection from `P_loc J_trace` to observable amplitudes is still missing.",
            "",
            "## Nonclaim Summary",
            markdown_table(summary_rows, summary_fields),
            "## Source Register",
            markdown_table(source_rows, source_fields),
            "## Bound Source Candidates",
            markdown_table(source_candidate_rows, candidate_fields),
            "## c_T Projection Contract",
            markdown_table(projection_rows, projection_fields),
            "## c_T Bound Rows",
            markdown_table(bound_rows, bound_fields),
            "## Claim Readiness",
            markdown_table(readiness_rows, readiness_fields),
            "## Route Choice",
            markdown_table(route_rows, route_fields),
            "## Claim Guard",
            markdown_table(guard_rows, guard_fields),
            "## Decision",
            markdown_table(decision_rows_value, decision_fields),
            "## Next Target",
            markdown_table(next_rows, next_fields),
            "## Validation",
            markdown_table(validation_rows, validation_fields),
        ]
    )
    OUTPUT_DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    source_candidate_rows = bound_source_candidate_rows(generated_utc)
    projection_rows = ct_projection_contract_rows(generated_utc)
    bound_rows = ct_bound_rows(generated_utc)
    readiness_rows = claim_readiness_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_value = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(
        SOURCE_REGISTER_PATH,
        source_rows,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        BOUND_SOURCE_CANDIDATES_PATH,
        source_candidate_rows,
        [
            "source_id",
            "arena",
            "observable",
            "source_title",
            "year",
            "source_url",
            "doi",
            "extraction_method",
            "source_status",
            "units",
            "usable_as",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        CT_PROJECTION_CONTRACT_PATH,
        projection_rows,
        [
            "projection_id",
            "arena",
            "observable",
            "input_cT_piece",
            "required_formula",
            "current_status",
            "missing_inputs",
            "claim_consequence",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        CT_BOUND_ROWS_PATH,
        bound_rows,
        [
            "bound_id",
            "arena",
            "observable",
            "bound_value",
            "bound_units",
            "lambda_value",
            "lambda_units",
            "confidence",
            "source_id",
            "source_path_or_url",
            "extraction_status",
            "projection_status",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        CLAIM_READINESS_PATH,
        readiness_rows,
        ["gate_id", "required_for_claim", "status", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_CHOICE_PATH,
        route_rows,
        ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        CLAIM_GUARD_PATH,
        guard_rows,
        ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows_value,
        ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_TARGET_PATH,
        next_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "what_changed",
            "best_partial_result",
            "hard_blockers",
            "what_is_not_claimed",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )

    validation_rows = build_validation_rows(
        source_rows,
        source_candidate_rows,
        projection_rows,
        bound_rows,
        readiness_rows,
        decision_rows_value,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_output_doc(
        generated_utc,
        source_rows,
        source_candidate_rows,
        projection_rows,
        bound_rows,
        readiness_rows,
        route_rows,
        guard_rows,
        decision_rows_value,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"871 validation failed: {failed}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
