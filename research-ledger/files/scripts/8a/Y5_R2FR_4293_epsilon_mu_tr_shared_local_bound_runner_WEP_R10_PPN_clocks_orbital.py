from __future__ import annotations

import csv
import io
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4293"
CLAIM_ID = "L-134"
BRANCH = "MTS_R2FR_Y5_EPSILON_MU_TR_SHARED_LOCAL_BOUND_RUNNER_WEP_R10_PPN_CLOCKS_ORBITAL_4293"
DECISION = "UNIT_PROJECTION_AJ_SEED_FAILS_LOCAL_PRECISION_TESTS_SHARED_BOUND_RUNNER_NONCLAIM"
MARKER = "PPC4161_EPSILON_MU_TR_SHARED_LOCAL_BOUND_RUNNER_4293"
PACKET_MARKER = "PPC4161_PACKET_EPSILON_MU_TR_SHARED_LOCAL_BOUND_RUNNER_4293"
NEXT_TARGET = "4294-Y5-R2FR-transition-membership-parent-action-or-projection-suppression-theorem.md"

FORMAL_PATH = FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md"
DOC_PATH = POST / "4293-Y5-R2FR-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4293_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PI_B_COEFFICIENT = 0.167893843691
TRANSITION_PIB = 0.5000000000287336
EPSILON_AJ_SEED = PI_B_COEFFICIENT * TRANSITION_PIB

BOUND_TABLE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"
BOUND_SOURCE_REGISTER_PATH = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_REGISTER.csv"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4293_LOCAL_00_4292_formal": (
        FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md",
        "score epsilon_mu_tr across WEP, R10, PPN, clocks",
        "4292 selects epsilon_mu_tr as the shared residual vector to score across local tests.",
    ),
    "SRC4293_LOCAL_01_4292_vector_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4292_EPSILON_MU_SHARED_VECTOR.csv",
        "epsilon_mu_tr",
        "4292 machine vector contains the shared transition residual components.",
    ),
    "SRC4293_LOCAL_02_4290_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4290_EPSILON_MU_BOUND_ROW.csv",
        "0.08394692185032419",
        "4290 supplies the private unit-window AJ capacity seed for epsilon_mu_tr.",
    ),
    "SRC4293_LOCAL_03_4173_bound_table": (
        BOUND_TABLE_PATH,
        "B4173_12_WEP",
        "4173 source-backed local empirical bound table.",
    ),
    "SRC4293_LOCAL_04_4173_source_register": (
        BOUND_SOURCE_REGISTER_PATH,
        "SRC4173_WEB_03_MICROSCOPE_final_WEP",
        "4173 source register for the imported local bound anchors.",
    ),
    "SRC4293_LOCAL_05_3702_R10_curve_candidate": (
        SOURCE_DIR / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv",
        "candidate_manual_review_required",
        "3702 has a nonclaim R10 curve candidate; this runner treats it as review-only.",
    ),
    "SRC4293_LOCAL_06_3707_R10_score_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv",
        "EXECUTABLE_NONCLAIM_PARENT_PN_LAMBDAH_ETA_AND_CURVE_REVIEW_REQUIRED",
        "3707 contains executable R10 score rows that remain nonclaim until review and parent products close.",
    ),
    "SRC4293_LOCAL_07_residual_template": (
        SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv",
        "R10_fifth_force",
        "Local residual template defines the WEP, PPN, clocks, Gdot, and fifth-force channels.",
    ),
}

WEB_SOURCES = [
    (
        "SRC4293_WEB_00_Will2014_PPN",
        "https://arxiv.org/abs/1403.7377",
        "arXiv:1403.7377; Living Reviews in Relativity 17, 4 (2014); DOI 10.12942/lrr-2014-4",
        "Primary PPN review source used by the 4173 bound table for gamma, beta, and orbital combination rows.",
    ),
    (
        "SRC4293_WEB_01_EotWash2020_R10",
        "https://arxiv.org/abs/2002.11761",
        "Phys. Rev. Lett. 124, 101101 (2020); DOI 10.1103/PhysRevLett.124.101101",
        "Short-range inverse-square/Yukawa source; gravitational-strength alpha=1 excluded for lambda > 38.6 um.",
    ),
    (
        "SRC4293_WEB_02_MICROSCOPE2022_WEP",
        "https://arxiv.org/abs/2209.15487",
        "Phys. Rev. Lett. 129, 121102 (2022); DOI 10.1103/PhysRevLett.129.121102",
        "Final MICROSCOPE Ti/Pt Eotvos result used for the WEP source-charge contrast row.",
    ),
    (
        "SRC4293_WEB_03_Galileo2018_clock",
        "https://arxiv.org/abs/1812.03711",
        "Phys. Rev. Lett. 121, 231101 (2018); DOI 10.1103/PhysRevLett.121.231101",
        "Galileo redshift test source used for the clock alpha row.",
    ),
    (
        "SRC4293_WEB_04_LLR2021_Gdot",
        "https://arxiv.org/abs/2012.12032",
        "Universe 7, 34 (2021); DOI 10.3390/universe7020034",
        "Lunar-laser-ranging Gdot source used for the local time-drift row.",
    ),
]

BOUND_IMPORT_SPECS = [
    ("ARENA4293_GAMMA", "B4173_00_gamma", "PPN_gamma", "gamma_minus_1", "Y_gamma * epsilon_mu_tr"),
    ("ARENA4293_BETA", "B4173_01_beta", "PPN_beta", "beta_minus_1", "Y_beta * epsilon_mu_tr"),
    ("ARENA4293_GDOT", "B4173_10_Gdot", "Gdot", "Gdot_over_G", "d epsilon_mu_tr / dt"),
    ("ARENA4293_R10", "B4173_11_R10", "R10_short_range", "alpha_Yukawa_at_lambda_38p6um", "Y_R10(lambda) * epsilon_mu_tr"),
    ("ARENA4293_WEP", "B4173_12_WEP", "WEP_source_charge", "eta_TiPt", "Y_WEP * epsilon_mu_tr"),
    ("ARENA4293_CLOCK", "B4173_13_clock", "clock_redshift", "redshift_violation_alpha", "Y_clock * epsilon_mu_tr"),
    ("ARENA4293_ORBIT", "B4173_14_orbit_combo", "orbital_PPN_combo", "((2+2gamma-beta)/3)-1", "Y_orbit * epsilon_mu_tr"),
]


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = list(rows[0].keys()) if rows else []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return "MISSING_NUMERIC"
    return f"{value:.16g}"


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4293 turns epsilon_mu_tr into a shared local-bound runner. The private AJ transition seed "
                "epsilon_AJ=0.08394692185032419 is compared against source-backed WEP, PPN gamma/beta, clock, "
                "orbital, Gdot and R10 anchor rows. Unit projection fails WEP, gamma, beta, clocks, orbital and "
                "one-year Gdot by large margins; R10 alpha=1 at lambda=38.6 um is only a diagnostic anchor and "
                "does not prove a fifth-force pass because epsilon_mu_tr must first be mapped to finite-range hair. "
                "The result is a nonclaim: either prove transition Hilbert membership/epsilon zero, or derive small "
                "projection coefficients / static-degenerate channels."
            ),
            (
                "4293 source register, bound imports, projection contract, unit-projection smoke rows, required "
                "suppression rows, degeneracy ledger, decision, firewall, status and validation CSV."
            ),
            "private_epsilon_mu_tr_shared_local_bound_runner_unit_projection_fails_nonclaim",
            (
                "Attempt parent-action membership zero for the transition monopole, or derive projection suppression "
                "coefficients Y_WEP,Y_gamma,Y_beta,Y_clock,Y_orbit plus static/no-range theorems for Gdot and R10."
            ),
            (
                "Claiming local-GR/R10/WEP pass from the AJ seed, treating the R10 threshold anchor as a full curve, "
                "absorbing observable residuals into G_cal, or assuming order-one transition leakage is safe."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle_role in []:
        del source_id, path, needle_role
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_url_recorded": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "evidence": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    for source_id, url, doi_or_id, evidence in WEB_SOURCES:
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "source_type": "web_source",
                "path_or_url": url,
                "exists_or_url_recorded": "True",
                "required_text": "recorded_primary_source_url",
                "required_text_found": "True",
                "doi_or_id": doi_or_id,
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def source_register_lookup() -> Dict[str, Dict[str, str]]:
    return {row.get("source_id", ""): row for row in csv_rows(BOUND_SOURCE_REGISTER_PATH)}


def bound_lookup() -> Dict[str, Dict[str, str]]:
    return {row.get("bound_id", ""): row for row in csv_rows(BOUND_TABLE_PATH)}


def arena_bound_import_rows() -> List[Dict[str, str]]:
    bounds = bound_lookup()
    sources = source_register_lookup()
    rows: List[Dict[str, str]] = []
    for arena_id, bound_id, arena, observable, projection_formula in BOUND_IMPORT_SPECS:
        bound = bounds.get(bound_id, {})
        source = sources.get(bound.get("source_id", ""), {})
        allowed = to_float(bound.get("allowed_abs_bound", ""))
        rows.append(
            {
                **common(),
                "arena_id": arena_id,
                "bound_id": bound_id,
                "arena": arena,
                "observable": observable,
                "projection_formula": projection_formula,
                "allowed_abs_bound": bound.get("allowed_abs_bound", "MISSING_BOUND"),
                "allowed_abs_bound_numeric_positive": str(math.isfinite(allowed) and allowed > 0.0),
                "units": bound.get("units", "MISSING_UNITS"),
                "source_id": bound.get("source_id", "MISSING_SOURCE_ID"),
                "source_url": source.get("path_or_url", "MISSING_SOURCE_URL"),
                "source_backed": bound.get("source_backed", "False"),
                "full_curve_available": bound.get("full_curve_available", "MISSING_CURVE_STATUS"),
                "import_note": "source-backed external bound; MTS row remains nonclaim until projection coefficient is parent-derived",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def projection_contract_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PC4293_WEP",
            "WEP_source_charge",
            "composition/source-charge contrast",
            "eta_source_AB = Y_WEP * epsilon_mu_tr + O(epsilon^2)",
            "differential_only",
            "Universal static monopole can hide in GM; WEP sees species/composition derivative only.",
            "NEEDS_PARENT_SOURCE_BLINDNESS_OR_Y_WEP_BOUND",
        ),
        (
            "PC4293_GAMMA",
            "PPN_gamma",
            "observed spatial-curvature readout",
            "gamma_minus_1 = Y_gamma * epsilon_mu_tr + O(epsilon^2)",
            "metric_projection_only",
            "Raw monopole amplitude is not automatically gamma; calibrated GM and spatial metric coefficient must be separated.",
            "NEEDS_PARENT_METRIC_READOUT_COEFFICIENT",
        ),
        (
            "PC4293_BETA",
            "PPN_beta",
            "second-order observed metric readout",
            "beta_minus_1 = Y_beta * epsilon_mu_tr + O(epsilon^2)",
            "metric_projection_only",
            "Beta is not cleared by Poisson/source normalization alone.",
            "NEEDS_PARENT_BETA_READOUT_COEFFICIENT",
        ),
        (
            "PC4293_CLOCK",
            "clock_redshift",
            "clock-frame potential coupling",
            "alpha_clock = Y_clock * epsilon_mu_tr + O(epsilon^2)",
            "clock_projection_only",
            "Clock success requires the MTS clock variable to be in the observed metric frame.",
            "NEEDS_CLOCK_FRAME_MAP",
        ),
        (
            "PC4293_ORBIT",
            "orbital_PPN_combo",
            "source-normalized orbital/PPN combination",
            "delta_orbit = Y_orbit * epsilon_mu_tr + O(epsilon^2)",
            "source_denominator_degenerate",
            "A universal static GM shift is denominator-degenerate unless independent source mass/readout is supplied.",
            "NEEDS_INDEPENDENT_SOURCE_DENOMINATOR",
        ),
        (
            "PC4293_GDOT",
            "Gdot",
            "local time drift of source normalization",
            "Gdot/G ~ d epsilon_mu_tr / dt",
            "derivative_only",
            "Static epsilon is invisible to Gdot; drifting epsilon is ultra-constrained.",
            "NEEDS_STATIC_THEOREM_OR_DRIFT_PROFILE",
        ),
        (
            "PC4293_R10",
            "R10_short_range",
            "finite-range Yukawa/range hair",
            "alpha_tr(lambda) = Y_R10(lambda) * epsilon_mu_tr",
            "finite_range_only",
            "A static zero-range/source normalization shift is not a Yukawa curve.",
            "NEEDS_RANGE_HAIR_MAP_AND_REVIEWED_CURVE",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "arena": arena,
            "constrained_component": component,
            "first_order_projection": formula,
            "what_bound_actually_sees": sees,
            "degeneracy_or_caveat": caveat,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, arena, component, formula, sees, caveat, status in raw
    ]


def bound_value(bound_id: str) -> float:
    return to_float(bound_lookup().get(bound_id, {}).get("allowed_abs_bound", ""))


def smoke_row(
    smoke_id: str,
    arena: str,
    observable: str,
    bound_id: str,
    predicted_abs: float,
    projection_assumption: str,
    expected_result: str,
    note: str,
) -> Dict[str, str]:
    bound = bound_value(bound_id)
    ratio = predicted_abs / bound if math.isfinite(bound) and bound > 0 else math.nan
    direct_pass = math.isfinite(bound) and predicted_abs <= bound
    return {
        **common(),
        "smoke_id": smoke_id,
        "arena": arena,
        "observable": observable,
        "bound_id": bound_id,
        "epsilon_AJ_seed": fmt(EPSILON_AJ_SEED),
        "projection_assumption": projection_assumption,
        "predicted_abs_under_assumption": fmt(predicted_abs),
        "allowed_abs_bound": fmt(bound),
        "ratio_predicted_to_bound": fmt(ratio),
        "direct_numeric_pass": str(direct_pass),
        "expected_result": expected_result,
        "expected_matches_numeric": str(
            (expected_result.startswith("FAIL") and not direct_pass)
            or (expected_result.startswith("DIAGNOSTIC_PASS") and direct_pass)
        ),
        "interpretation": note,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def unit_projection_smoke_rows() -> List[Dict[str, str]]:
    return [
        smoke_row(
            "SMOKE4293_WEP_Y1",
            "WEP_source_charge",
            "eta_source_AB",
            "B4173_12_WEP",
            EPSILON_AJ_SEED,
            "Y_WEP=1",
            "FAIL_UNIT_PROJECTION",
            "Order-one composition/source-charge leakage is excluded; WEP demands an extremely small differential projection or zero theorem.",
        ),
        smoke_row(
            "SMOKE4293_GAMMA_Y1",
            "PPN_gamma",
            "gamma_minus_1",
            "B4173_00_gamma",
            EPSILON_AJ_SEED,
            "Y_gamma=1",
            "FAIL_UNIT_PROJECTION",
            "Order-one leakage into gamma is excluded; gamma needs a small readout coefficient or membership zero.",
        ),
        smoke_row(
            "SMOKE4293_BETA_Y1",
            "PPN_beta",
            "beta_minus_1",
            "B4173_01_beta",
            EPSILON_AJ_SEED,
            "Y_beta=1",
            "FAIL_UNIT_PROJECTION",
            "Order-one leakage into beta is excluded; beta needs a derived readout coefficient.",
        ),
        smoke_row(
            "SMOKE4293_CLOCK_Y1",
            "clock_redshift",
            "alpha_clock",
            "B4173_13_clock",
            EPSILON_AJ_SEED,
            "Y_clock=1",
            "FAIL_UNIT_PROJECTION",
            "Order-one clock-frame leakage is excluded by redshift tests.",
        ),
        smoke_row(
            "SMOKE4293_ORBIT_Y1",
            "orbital_PPN_combo",
            "delta_orbit_combo",
            "B4173_14_orbit_combo",
            EPSILON_AJ_SEED,
            "Y_orbit=1",
            "FAIL_UNIT_PROJECTION",
            "Order-one leakage into the orbital PPN combination is excluded unless it is pure calibrated GM denominator.",
        ),
        smoke_row(
            "SMOKE4293_GDOT_1YR_DRIFT",
            "Gdot",
            "Gdot_over_G",
            "B4173_10_Gdot",
            EPSILON_AJ_SEED,
            "epsilon_mu_tr relaxes on 1 yr timescale",
            "FAIL_UNIT_DRIFT",
            "Any year-scale drift of this amplitude is excluded; static/no-drift theorem or ultra-long timescale is required.",
        ),
        smoke_row(
            "SMOKE4293_R10_DIRECT_ANCHOR",
            "R10_short_range",
            "alpha_Yukawa_at_lambda_38p6um",
            "B4173_11_R10",
            EPSILON_AJ_SEED,
            "alpha_tr(38.6um)=epsilon_mu_tr",
            "DIAGNOSTIC_PASS_NONCLAIM",
            "The alpha=1 threshold anchor would not kill this amplitude directly, but this is not a claim because R10 needs range hair and a reviewed full curve.",
        ),
    ]


def required_suppression_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row_id, arena, observable, bound_id, coefficient in [
        ("REQ4293_WEP", "WEP_source_charge", "eta_source_AB", "B4173_12_WEP", "Y_WEP"),
        ("REQ4293_GAMMA", "PPN_gamma", "gamma_minus_1", "B4173_00_gamma", "Y_gamma"),
        ("REQ4293_BETA", "PPN_beta", "beta_minus_1", "B4173_01_beta", "Y_beta"),
        ("REQ4293_CLOCK", "clock_redshift", "alpha_clock", "B4173_13_clock", "Y_clock"),
        ("REQ4293_ORBIT", "orbital_PPN_combo", "delta_orbit_combo", "B4173_14_orbit_combo", "Y_orbit"),
        ("REQ4293_R10_ANCHOR", "R10_short_range", "alpha_Yukawa_at_lambda_38p6um", "B4173_11_R10", "Y_R10_anchor"),
    ]:
        bound = bound_value(bound_id)
        required = bound / EPSILON_AJ_SEED if math.isfinite(bound) and EPSILON_AJ_SEED > 0.0 else math.nan
        rows.append(
            {
                **common(),
                "requirement_id": row_id,
                "arena": arena,
                "observable": observable,
                "coefficient_or_timescale": coefficient,
                "law": f"{coefficient} <= bound/epsilon_AJ_seed",
                "epsilon_AJ_seed": fmt(EPSILON_AJ_SEED),
                "allowed_abs_bound": fmt(bound),
                "required_value": fmt(required),
                "units": "dimensionless",
                "status": "FULL_BOUND_REQUIRED" if row_id == "REQ4293_R10_ANCHOR" else "SUPPRESSION_OR_ZERO_THEOREM_REQUIRED",
                "interpretation": "R10 anchor-only diagnostic; must not be treated as full curve" if row_id == "REQ4293_R10_ANCHOR" else "Projection coefficient must be below this value if epsilon_AJ_seed survives.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    gdot_bound = bound_value("B4173_10_Gdot")
    timescale = EPSILON_AJ_SEED / gdot_bound if math.isfinite(gdot_bound) and gdot_bound > 0 else math.nan
    rows.append(
        {
            **common(),
            "requirement_id": "REQ4293_GDOT_TIMESCALE",
            "arena": "Gdot",
            "observable": "Gdot_over_G",
            "coefficient_or_timescale": "T_drift_min",
            "law": "T_drift_yr >= epsilon_AJ_seed / |Gdot/G|_bound",
            "epsilon_AJ_seed": fmt(EPSILON_AJ_SEED),
            "allowed_abs_bound": fmt(gdot_bound),
            "required_value": fmt(timescale),
            "units": "yr",
            "status": "STATIC_THEOREM_OR_ULTRALONG_DRIFT_REQUIRED",
            "interpretation": "If epsilon_mu_tr is time-varying at this amplitude, the drift timescale must be cosmologically enormous.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def degeneracy_ledger_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEG4293_0_universal_static_monopole",
            "epsilon_mu_tr universal l=0 static source amplitude",
            "Degenerate with G_cal M_H^dress unless independent source denominator or membership proof exists.",
            "Do not score raw universal epsilon as WEP/R10/Gdot by itself.",
        ),
        (
            "DEG4293_1_WEP",
            "eta_source_AB",
            "WEP sees species/composition contrast, not common-mode GM.",
            "Need Y_WEP from source-charge derivative or prove source blindness.",
        ),
        (
            "DEG4293_2_R10",
            "alpha_tr(lambda)",
            "R10 sees finite-range Yukawa/range hair, not ordinary long-range source normalization.",
            "Need range map and reviewed curve before any R10 claim.",
        ),
        (
            "DEG4293_3_Gdot",
            "dln_mu_tr_dt",
            "Gdot sees time drift only; a static residual is invisible to this row.",
            "Need static theorem or drift profile.",
        ),
        (
            "DEG4293_4_PPN",
            "gamma_minus_1, beta_minus_1",
            "PPN rows see observed metric readout coefficients, not raw source mass alone.",
            "Need Y_gamma and Y_beta from weak-field readout.",
        ),
        (
            "DEG4293_5_clock",
            "alpha_clock",
            "Clock tests see clock-frame coupling after MTS clock variable maps to the observed frame.",
            "Need clock-frame map.",
        ),
        (
            "DEG4293_6_orbital",
            "orbital PPN/source-normalization combo",
            "Orbital fits can absorb common GM but not beta/gamma/time/range/species residuals.",
            "Need independent denominator split.",
        ),
    ]
    return [
        {
            **common(),
            "degeneracy_id": row_id,
            "object": obj,
            "degeneracy": degeneracy,
            "required_resolution": required,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, obj, degeneracy, required in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4293_0",
            "decision": DECISION,
            "what_moved": "epsilon_mu_tr is no longer an abstract missing coupling; it now has arena-specific local precision pressure and required suppression laws.",
            "headline": "Order-one leakage of the AJ seed is locally dead; the theory needs transition membership zero or small projection coefficients.",
            "not_claimed": "local-GR pass, WEP pass, R10 pass, PPN pass, clock pass, orbital pass",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4293_0_no_AJ_to_observable_claim", "Private AJ capacity is not empirical evidence unless the projection coefficient is derived."),
        ("FW4293_1_no_R10_anchor_overclaim", "The alpha=1 at 38.6 um threshold is an anchor, not a reviewed full bound curve."),
        ("FW4293_2_no_GM_hiding", "Universal GM degeneracy cannot hide WEP, range, time-drift, gamma/beta, or clock residuals."),
        ("FW4293_3_no_order_one_leakage", "Order-one leakage of epsilon_AJ_seed into local observables fails the smoke gate."),
        ("FW4293_4_no_public_pass", "All 4293 rows remain private nonclaim rows."),
    ]
    return [
        {
            **common(),
            "firewall_id": row_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    failed = [row for row in unit_projection_smoke_rows() if row["expected_result"].startswith("FAIL")]
    return [
        {
            **common(),
            "status_id": "STATUS4293_0",
            "result": "SHARED_LOCAL_BOUND_RUNNER_READY_UNIT_PROJECTION_FAILS",
            "epsilon_AJ_seed": fmt(EPSILON_AJ_SEED),
            "unit_projection_fail_count": str(len(failed)),
            "diagnostic_r10_anchor_pass_nonclaim": "True",
            "primary_live_gap": "derive transition membership zero or projection suppression coefficients",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4293_0",
            "next_target": NEXT_TARGET,
            "objective": "Try to derive either epsilon_mu_tr=0 from parent transition membership or derive the small arena projection coefficients required by 4293.",
            "priority_order": "membership_zero_first; then Y_WEP/Y_gamma/Y_beta/Y_clock/Y_orbit suppression; then static Gdot theorem; then R10 range-hair map",
            "why": "4293 shows order-one transition leakage is not viable in local precision tests.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    y_wep = bound_value("B4173_12_WEP") / EPSILON_AJ_SEED
    y_gamma = bound_value("B4173_00_gamma") / EPSILON_AJ_SEED
    y_beta = bound_value("B4173_01_beta") / EPSILON_AJ_SEED
    y_clock = bound_value("B4173_13_clock") / EPSILON_AJ_SEED
    y_orbit = bound_value("B4173_14_orbit_combo") / EPSILON_AJ_SEED
    y_r10 = bound_value("B4173_11_R10") / EPSILON_AJ_SEED
    t_gdot = EPSILON_AJ_SEED / bound_value("B4173_10_Gdot")
    return f"""
# 309 epsilon_mu_tr shared local bound runner: WEP/R10/PPN/clocks/orbital

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4293 takes the live transition residue from 4292,

```text
epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress),
```

and scores the private AJ seed

```text
epsilon_AJ_seed = {EPSILON_AJ_SEED:.16g}
```

against source-backed local precision rows.

The blunt answer is:

```text
order-one projection of epsilon_AJ_seed into local observables fails.
```

This is not a failure of the whole MTS programme. It is a sharp constraint on the transition/coupling branch: the parent theory must derive either `epsilon_mu_tr=0` in local Hilbert membership, or small projection coefficients.

## Required projection suppression

If an observable has first-order form

```text
O_i = Y_i epsilon_mu_tr + O(epsilon^2),
```

then the imported local bounds require:

```text
Y_WEP   <= {y_wep:.16g}
Y_gamma <= {y_gamma:.16g}
Y_beta  <= {y_beta:.16g}
Y_clock <= {y_clock:.16g}
Y_orbit <= {y_orbit:.16g}
```

For local drift:

```text
T_drift >= {t_gdot:.16g} yr
```

if the full seed amplitude changes on a timescale `T_drift`.

The R10 anchor gives:

```text
Y_R10_anchor <= {y_r10:.16g}
```

but this is only a diagnostic anchor. R10 constrains finite-range hair `alpha_tr(lambda)`, not raw static source normalization, so no R10 pass is claimed.

## Interpretation

The useful distinction is:

```text
common static monopole  -> can be GM/source-denominator degenerate
composition contrast    -> WEP
finite range hair       -> R10
time drift              -> Gdot/clocks/orbits
metric readout          -> gamma, beta, clock, orbital PPN
```

So the path forward is not another generic statement that "the coupling is missing". The precise missing object is now:

```text
parent-derived local projection map:
epsilon_mu_tr -> (Y_WEP, Y_gamma, Y_beta, Y_clock, Y_orbit, d/dt, alpha_tr(lambda)).
```

## Nonclaim

No local-GR, WEP, R10, PPN, clock, or orbital pass is claimed from 4293.

The next target is `{NEXT_TARGET}`: try the parent-action membership zero first; if it does not close, derive the suppression coefficients directly.
"""


def checkpoint_doc() -> str:
    return f"""
# 4293 Y5 R2FR epsilon_mu_tr shared local bound runner

## Purpose

This checkpoint converts the 4292 shared transition residual into a real local empirical pressure test across WEP, R10, PPN, clocks and orbital rows.

## Outcome

The private AJ seed is:

```text
epsilon_AJ_seed = {EPSILON_AJ_SEED:.16g}.
```

Unit projection into WEP, PPN gamma/beta, clock, orbital and one-year Gdot rows fails. R10 has a diagnostic anchor-only pass if one incorrectly treats `alpha_tr(38.6um)=epsilon_mu_tr`, but this is not claim-valid because R10 needs finite-range hair and a reviewed full curve.

## Next

Try to derive `epsilon_mu_tr=0` from parent transition membership. If that fails, derive the projection suppression map:

```text
epsilon_mu_tr -> Y_WEP, Y_gamma, Y_beta, Y_clock, Y_orbit, d/dt, alpha_tr(lambda).
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    imports = csv_rows(paths["arena_bound_imports"])
    contracts = csv_rows(paths["projection_contract"])
    smokes = csv_rows(paths["unit_projection_smoke"])
    requirements = csv_rows(paths["required_suppression"])
    degeneracy = csv_rows(paths["degeneracy_ledger"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        (
            "VAL4293_0_sources_exist_or_recorded",
            bool(sources) and all(row["exists_or_url_recorded"] == "True" for row in sources),
            "all local sources exist and web source URLs are recorded",
        ),
        (
            "VAL4293_1_local_needles_found",
            bool(sources)
            and all(
                row["required_text_found"] == "True"
                for row in sources
                if row["source_type"] == "local_file"
            ),
            "all local source needles found",
        ),
        (
            "VAL4293_2_bound_imports_positive_source_backed",
            bool(imports)
            and all(row["allowed_abs_bound_numeric_positive"] == "True" for row in imports)
            and all(row["source_backed"] == "True" for row in imports),
            "all imported bound rows are positive and source-backed",
        ),
        (
            "VAL4293_3_projection_contract_complete",
            {row["arena"] for row in contracts}
            == {"WEP_source_charge", "PPN_gamma", "PPN_beta", "clock_redshift", "orbital_PPN_combo", "Gdot", "R10_short_range"},
            "projection contract covers all target arenas",
        ),
        (
            "VAL4293_4_unit_smoke_expected",
            bool(smokes)
            and all(row["expected_matches_numeric"] == "True" for row in smokes)
            and sum(row["expected_result"].startswith("FAIL") for row in smokes) == 6
            and any(row["expected_result"] == "DIAGNOSTIC_PASS_NONCLAIM" for row in smokes),
            "unit projection smoke results match expected fail/diagnostic pattern",
        ),
        (
            "VAL4293_5_required_suppression_rows",
            any(row["requirement_id"] == "REQ4293_WEP" and to_float(row["required_value"]) < 1.0e-12 for row in requirements)
            and any(row["requirement_id"] == "REQ4293_GDOT_TIMESCALE" and to_float(row["required_value"]) > 1.0e12 for row in requirements),
            "WEP and Gdot required-suppression scales are present",
        ),
        (
            "VAL4293_6_degeneracy_ledger",
            any(row["degeneracy_id"] == "DEG4293_0_universal_static_monopole" for row in degeneracy)
            and any(row["degeneracy_id"] == "DEG4293_2_R10" for row in degeneracy),
            "degeneracy ledger separates common monopole and R10 finite-range hair",
        ),
        ("VAL4293_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4293_8_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4293_9_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-134 private nonclaim row",
        ),
        ("VAL4293_10_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
        (
            "VAL4293_11_spine_packet_markers",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4293_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4293_SOURCE_REGISTER.csv",
        "arena_bound_imports": SOURCE_DIR / "P8_Y5_R2FR_4293_ARENA_BOUND_IMPORTS.csv",
        "projection_contract": SOURCE_DIR / "P8_Y5_R2FR_4293_EPSILON_PROJECTION_CONTRACT.csv",
        "unit_projection_smoke": SOURCE_DIR / "P8_Y5_R2FR_4293_UNIT_PROJECTION_SMOKE_RESULTS.csv",
        "required_suppression": SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "degeneracy_ledger": SOURCE_DIR / "P8_Y5_R2FR_4293_DEGENERACY_LEDGER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4293_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4293_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4293_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4293_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["arena_bound_imports"], arena_bound_import_rows())
    write_csv(paths["projection_contract"], projection_contract_rows())
    write_csv(paths["unit_projection_smoke"], unit_projection_smoke_rows())
    write_csv(paths["required_suppression"], required_suppression_rows())
    write_csv(paths["degeneracy_ledger"], degeneracy_ledger_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4293 epsilon_mu_tr shared local bound runner",
        (
            "4293 turns the transition residual `epsilon_mu_tr` into an arena-specific local-bound runner. "
            "The private AJ seed `0.08394692185032419` fails if projected with order-one coefficients into WEP, "
            "PPN gamma/beta, clock, orbital and one-year Gdot rows. R10 has only an anchor-level diagnostic nonclaim. "
            "The live theory task is now parent transition membership zero or a derived projection suppression map."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4293 packet epsilon_mu_tr shared local bound runner",
        (
            "Packet update: `epsilon_mu_tr` is no longer a generic missing coupling. It is split by observable channel: "
            "composition contrast, finite-range hair, time drift, metric readout, clock frame, and source-denominator "
            "degeneracy. Order-one leakage fails; zero/suppression derivation is required."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: epsilon_AJ_seed={EPSILON_AJ_SEED:.12e}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
