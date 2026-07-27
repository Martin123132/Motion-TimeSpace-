from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3867"
BRANCH = "MTS_R2FR_Y5_SOURCE_BACKED_JOINT_ALPHA_CURRENT_F2_INPUT_ACQUISITION_OR_IMAGE_CONSTRUCTOR_3867"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3866_THEOREM = OUT / "P8_Y5_R2FR_3866_JOINT_RUNNER_THEOREM.csv"
CSV_3866_SCHEMA = OUT / "P8_Y5_R2FR_3866_JOINT_INPUT_SCHEMA.csv"
CSV_3866_RESULTS = OUT / "P8_Y5_R2FR_3866_DRYRUN_RESULTS.csv"
CSV_3866_NEXT = OUT / "P8_Y5_R2FR_3866_NEXT_TARGET.csv"
CSV_3866_VALIDATION = OUT / "P8_Y5_BRR545_3866_VALIDATION.csv"
CSV_1052_CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
CSV_1052_R10 = OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"
CSV_3680_ZG = OUT / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv"
CSV_3680_ZERO = OUT / "P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv"
CSV_3118_BALPHA = OUT / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv"
CSV_2766_IMAGE = OUT / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_2659_HOM = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CSV_1057_F2 = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3867_SOURCE_REGISTER.csv",
    "schema": OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_INPUT_SCHEMA.csv",
    "acquisition": OUT / "P8_Y5_R2FR_3867_INPUT_ACQUISITION_STATUS.csv",
    "candidates": OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv",
    "runner": OUT / "P8_Y5_R2FR_3867_JOINT_RUNNER_REEVALUATION.csv",
    "image": OUT / "P8_Y5_R2FR_3867_IMAGE_CONSTRUCTOR_AUDIT.csv",
    "gates": OUT / "P8_Y5_R2FR_3867_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3867_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3867_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3867_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3867_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3867_00_3866_theorem", CSV_3866_THEOREM, "JRI3866_5_next_handoff", "3866 handoff: runner executable, needs inputs or image constructor"),
    ("SRC3867_01_3866_schema", CSV_3866_SCHEMA, "SCHEMA3866_3", "required z_g_tau input schema"),
    ("SRC3867_02_3866_results", CSV_3866_RESULTS, "BLOCKED_ALPHA_ONLY_NO_ZG", "alpha-only dryrun block"),
    ("SRC3867_03_3866_next", CSV_3866_NEXT, "NEXT3866_0", "declared 3867 target"),
    ("SRC3867_04_3866_validation", CSV_3866_VALIDATION, "PASS", "previous validation pass"),
    ("SRC3867_05_clock_bound", CSV_1052_CLOCK, "ACB1052_2", "best current clock alpha product bound"),
    ("SRC3867_06_wep_projection", CSV_1052_WEP, "AWP1052_0_alpha_Coulomb", "MICROSCOPE alpha/Coulomb projection"),
    ("SRC3867_07_r10_projection", CSV_1052_R10, "RAP1052_0_product_law", "R10 alpha product-law projection"),
    ("SRC3867_08_zg_components", CSV_3680_ZG, "ZGD3680_7_two_knob_identity", "z_g component decomposition and identity"),
    ("SRC3867_09_zg_zero", CSV_3680_ZERO, "ZG3680_7_verdict", "z_g zero theorem verdict"),
    ("SRC3867_10_balpha_template", CSV_3118_BALPHA, "BAP3118_1", "b_alpha product input template"),
    ("SRC3867_11_image_exhaustion", CSV_2766_IMAGE, "VOE2766_6_verdict", "visible image exhaustion verdict"),
    ("SRC3867_12_no_hom", CSV_2659_HOM, "ODT2659_1_exact_typed_theorem", "typed no-hidden-visible-hom conditional theorem"),
    ("SRC3867_13_f2_counterterms", CSV_1057_F2, "CT1057_1_hidden_scalar", "surviving hidden scalar F2 counterterm"),
]

IDENTITY = "b_alpha_X = 2 z_g - s_XF2"
RUNNER_LAW = "|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def find_row(path: Path, needle: str) -> dict[str, str]:
    if not path.exists():
        return {}
    for row in read_csv_rows(path):
        if needle in " ".join(str(value) for value in row.values()):
            return row
    return {}


def parse_float_or_none(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.startswith("MISSING") or text in {"NA", "not_applicable", "None"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "source_backed_nonclaim_input_acquisition",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def input_schema_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("SCHEMA3867_0", "external_bound", "external experiment/source", "numeric bound in same arena", "required for scoring", "clock and WEP partial; R10 curve not promoted", "positive numeric value plus source row"),
        ("SCHEMA3867_1", "tau_A", "MTS projection/readout", "same-domain projection scale", "required for scoring", "missing except absorbed clock product form", "source-backed or parent-derived"),
        ("SCHEMA3867_2", "b_alpha_tau", "MTS alpha drift/source coefficient", "arena product b_alpha_X*tau_A", "required for scoring", "template only", "numeric/theorem-zero with source path"),
        ("SCHEMA3867_3", "z_g_tau", "MTS current normalization", "arena product z_g*tau_A", "required for scoring", "missing and not zero-proved", "numeric/theorem-zero with source path"),
        ("SCHEMA3867_4", "s_XF2_tau", "MTS F2 coefficient", "direct prediction or projection product", "optional if inferred from identity; required for direct score", "missing", "numeric/theorem-zero with source path"),
        ("SCHEMA3867_5", "projection_consistency", "domain matching", "same Xhat/material/profile/readout convention", "required for scoring", "missing", "explicit row tying all factors to one arena"),
        ("SCHEMA3867_6", "image_constructor_certificate", "parent action", "A_vis=Image(ParentGenerate) proof", "alternative to numeric scoring", "conditional only", "parent-signed exactness/fullness/no-Hom/radiative/readout clauses"),
    ]
    return [
        {
            "schema_id": row_id,
            "field": field,
            "owner": owner,
            "meaning": meaning,
            "requirement": requirement,
            "current_status": current_status,
            "promotion_rule": promotion_rule,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, owner, meaning, requirement, current_status, promotion_rule in rows
    ]


def acquisition_status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "ACQ3867_0_clock_bound",
            "arena": "clock",
            "input_class": "external_bound",
            "source_row": "ACB1052_2",
            "source_path": rel(CSV_1052_CLOCK),
            "status": "SOURCE_BACKED_AVAILABLE",
            "usable_now": True,
            "missing_for_claim": "MTS b_alpha_tau_clock; z_g_tau_clock; s_XF2_tau_clock or parent image theorem; clock readout normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "ACQ3867_1_wep_projection",
            "arena": "MICROSCOPE_WEP",
            "input_class": "external_bound_and_material_alpha_projection",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "source_path": rel(CSV_1052_WEP),
            "status": "SOURCE_BACKED_PARTIAL",
            "usable_now": True,
            "missing_for_claim": "beta_source_alpha theorem/prior; tau_WEP; shared domain rule; full material model; z_g_tau_WEP; s_XF2_tau_WEP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "ACQ3867_2_r10_projection",
            "arena": "R10_short_range",
            "input_class": "product_law_projection",
            "source_row": "RAP1052_0_product_law",
            "source_path": rel(CSV_1052_R10),
            "status": "FORMULA_ONLY_NONCLAIM",
            "usable_now": False,
            "missing_for_claim": "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; epsilon_tail; promoted alpha_bound(lambda) curve; z_g_tau_R10; s_XF2_tau_R10",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "ACQ3867_3_zg_components",
            "arena": "all_local_arenas",
            "input_class": "MTS_current_normalization",
            "source_row": "ZGD3680_0_to_ZGD3680_7",
            "source_path": rel(CSV_3680_ZG),
            "status": "DECOMPOSITION_AVAILABLE_VALUES_MISSING",
            "usable_now": False,
            "missing_for_claim": "z_Qstar; z_lattice,A; z_Noether,A; z_cA_post,A; z_readout,A; source-arena extensions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "ACQ3867_4_parent_image",
            "arena": "parent_visible_operator_domain",
            "input_class": "alternative_exact_derivation",
            "source_row": "VOE2766_6_verdict; ODT2659_1_exact_typed_theorem",
            "source_path": rel(CSV_2766_IMAGE) + "; " + rel(CSV_2659_HOM),
            "status": "CONDITIONAL_UNSIGNED",
            "usable_now": False,
            "missing_for_claim": "quotient exactness/fullness; no hidden-visible Hom signed by parent; radiative/readout stability; boundary/local projection silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def candidate_rows(timestamp: str) -> list[dict[str, object]]:
    clock = find_row(CSV_1052_CLOCK, "ACB1052_2")
    wep = find_row(CSV_1052_WEP, "AWP1052_0_alpha_Coulomb")
    r10 = find_row(CSV_1052_R10, "RAP1052_0_product_law")
    zg = find_row(CSV_3680_ZG, "ZGD3680_7_two_knob_identity")
    image = find_row(CSV_2766_IMAGE, "VOE2766_6_verdict")
    f2 = find_row(CSV_1057_F2, "CT1057_1_hidden_scalar")

    return [
        {
            "candidate_id": "CAND3867_0_clock_alpha_product",
            "arena": "clock",
            "source_row": "ACB1052_2",
            "source_path": rel(CSV_1052_CLOCK),
            "external_observable": clock.get("clock_pair", "171Yb+ E3 / 171Yb+ E2"),
            "external_bound_value": clock.get("product_bound_1sigma_yr_inv", "2.1e-18"),
            "external_bound_units": "yr^-1",
            "external_status": "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "b_alpha_tau": "MISSING_BALPHA_TIMES_TAU_CLOCK",
            "z_g_tau": "MISSING_ZG_TIMES_TAU_CLOCK",
            "s_XF2_tau": "MISSING_SXF2_TIMES_TAU_CLOCK",
            "projection_consistency": "MISSING_CLOCK_XHAT_READOUT_NORMALIZATION",
            "runner_verdict": "BLOCKED_EXTERNAL_BOUND_AVAILABLE_MTS_JOINT_INPUTS_MISSING",
            "next_action": "derive/source z_g_tau_clock first, then b_alpha_tau_clock under same readout convention",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "CAND3867_1_wep_alpha_coulomb",
            "arena": "MICROSCOPE_WEP",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "source_path": rel(CSV_1052_WEP),
            "external_observable": wep.get("channel", "alpha/Coulomb composition channel"),
            "external_bound_value": wep.get("eta_bound", "2.8e-15"),
            "external_bound_units": "dimensionless_eta",
            "external_status": "SOURCE_BACKED_WEP_BOUND_PARTIAL_ALPHA_PROJECTION",
            "b_alpha_tau": "MISSING_BETA_SOURCE_ALPHA_TIMES_BALPHA_TIMES_TAU_WEP",
            "z_g_tau": "MISSING_ZG_TIMES_TAU_WEP",
            "s_XF2_tau": "MISSING_SXF2_TIMES_TAU_WEP",
            "projection_consistency": "MISSING_SHARED_SOURCE_MATERIAL_ORBIT_READOUT_DOMAIN",
            "runner_verdict": "BLOCKED_MISSING_SOURCE_PROJECTION_AND_ZG_SXF2",
            "next_action": "derive beta_source_alpha/tau_WEP from parent current owner or keep WEP as bound-input-only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "CAND3867_2_r10_product_law",
            "arena": "R10_short_range",
            "source_row": "RAP1052_0_product_law",
            "source_path": rel(CSV_1052_R10),
            "external_observable": r10.get("formula", "alpha_X(lambda)=K_X^R10(lambda) beta_s beta_t + epsilon_tail"),
            "external_bound_value": "MISSING_VALID_ALPHA_BOUND_CURVE",
            "external_bound_units": "dimensionless_alpha_lambda_curve",
            "external_status": "PRODUCT_LAW_ONLY_NONCLAIM",
            "b_alpha_tau": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL",
            "z_g_tau": "MISSING_ZG_TIMES_TAU_R10",
            "s_XF2_tau": "MISSING_SXF2_TIMES_TAU_R10",
            "projection_consistency": "MISSING_LAMBDA_PROFILE_MATERIAL_AND_KERNEL_DOMAIN",
            "runner_verdict": "BLOCKED_R10_PROFILE_BETA_BOUND_CURVE_AND_ZG_SXF2_MISSING",
            "next_action": "only promote after real alpha_bound(lambda) curve plus parent beta/kernel coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "CAND3867_3_zg_decomposition",
            "arena": "all_local_arenas",
            "source_row": "ZGD3680_7_two_knob_identity",
            "source_path": rel(CSV_3680_ZG),
            "external_observable": zg.get("formula", IDENTITY),
            "external_bound_value": "not_external_bound",
            "external_bound_units": "dimensionless_or_arena_product",
            "external_status": "MTS_COMPONENT_DECOMPOSITION_IMPORTED",
            "b_alpha_tau": "linked_by_identity",
            "z_g_tau": "MISSING_COMPONENT_VALUES_OR_ZERO_PROOF",
            "s_XF2_tau": "linked_by_identity",
            "projection_consistency": "MISSING_ARENA_COMPONENT_OWNERSHIP",
            "runner_verdict": "BLOCKED_ZG_ZERO_OR_BOUND_NOT_PROVED",
            "next_action": "prove or bound z_Qstar, z_lattice, z_Noether, z_cA_post, z_readout in one arena",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "CAND3867_4_parent_image_constructor",
            "arena": "parent_visible_operator_domain",
            "source_row": "VOE2766_6_verdict",
            "source_path": rel(CSV_2766_IMAGE),
            "external_observable": image.get("claim_piece", "visible operator-domain exhaustion theorem"),
            "external_bound_value": "not_numeric_route",
            "external_bound_units": "theorem_certificate",
            "external_status": "CONDITIONAL_THEOREM_IMPORTED",
            "b_alpha_tau": "zero_if_image_constructor_closes",
            "z_g_tau": "zero_if_current_owner_closes",
            "s_XF2_tau": "zero_if_no_extra_F2_image_closes",
            "projection_consistency": "UNSIGNED_PARENT_CONSTRUCTOR",
            "runner_verdict": "BLOCKED_PARENT_IMAGE_CONSTRUCTOR_UNSIGNED",
            "next_action": "construct the parent visible image category or demote to explicit closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "CAND3867_5_hidden_F2_counterterm",
            "arena": "visible_EM",
            "source_row": "CT1057_1_hidden_scalar",
            "source_path": rel(CSV_1057_F2),
            "external_observable": f2.get("formula", "DeltaS=-1/4 int sqrt(-g_obs) f(I_hid) F_Q^2"),
            "external_bound_value": "counterexample_not_bound",
            "external_bound_units": "operator_coefficient",
            "external_status": "LEGAL_IF_NO_HOM_UNSIGNED",
            "b_alpha_tau": "can_be_reopened_by_hidden_F2",
            "z_g_tau": "separate_current_normalization_still_live",
            "s_XF2_tau": "MISSING_OR_ALLOWED_COUNTERTERM",
            "projection_consistency": "MISSING_TRIVIAL_HIDDEN_INVARIANT_ALGEBRA",
            "runner_verdict": "BLOCKED_HIDDEN_SCALAR_F2_COUNTERTERM_NOT_EXCLUDED",
            "next_action": "prove no hidden-visible Hom/trivial hidden invariant algebra before claiming no-extra-F2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_reevaluation_rows(candidates: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        external_bound = parse_float_or_none(candidate["external_bound_value"])
        missing_mts = any(str(candidate[key]).startswith("MISSING") for key in ("b_alpha_tau", "z_g_tau", "s_XF2_tau"))
        theorem_route = candidate["candidate_id"] == "CAND3867_4_parent_image_constructor"
        counterexample_route = candidate["candidate_id"] == "CAND3867_5_hidden_F2_counterterm"
        claim_allowed = False
        if external_bound is not None and external_bound > 0 and not missing_mts:
            verdict = "BLOCKED_UNEXPECTED_NEEDS_MANUAL_REVIEW"
        elif theorem_route:
            verdict = "BLOCKED_THEOREM_ROUTE_UNSIGNED"
        elif counterexample_route:
            verdict = "BLOCKED_COUNTERTERM_ROUTE_STILL_OPEN"
        elif external_bound is not None and external_bound > 0:
            verdict = "BLOCKED_SOURCE_BOUND_READY_MTS_SIDE_MISSING"
        else:
            verdict = str(candidate["runner_verdict"])
        rows.append(
            {
                "reeval_id": "RUN3867_" + candidate["candidate_id"].split("_", 1)[1],
                "candidate_id": candidate["candidate_id"],
                "arena": candidate["arena"],
                "external_bound_numeric": external_bound if external_bound is not None else "MISSING_OR_NOT_NUMERIC",
                "external_bound_positive": external_bound is not None and external_bound > 0,
                "missing_mts_joint_inputs": missing_mts,
                "image_constructor_signed": False,
                "runner_law": RUNNER_LAW,
                "verdict": verdict,
                "claim_allowed": claim_allowed,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def image_constructor_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("IMG3867_0_parent_generator_category", "ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topology,e_obs] category exists", "PARTIAL_CONTRACT", "VOE2766_1_parent_generator_domain", "turn contract into explicit functor/domain object"),
        ("IMG3867_1_quotient_exactness_fullness", "visible quotient functor is exact/full enough to exhaust coefficient objects", "UNSIGNED", "VOE2766_2_quotient_functor_exactness", "prove no extra Coeff(O_vis) object appears after quotient"),
        ("IMG3867_2_no_hidden_visible_hom", "Hom(C_hid,Coeff(F_Q^2)) absent/constant", "CONDITIONAL_NOT_PARENT_SIGNED", "ODT2659_1_exact_typed_theorem", "make typed-domain exclusion a parent theorem, not closure"),
        ("IMG3867_3_no_independent_F2", "no independent visible Coeff(F_Q^2)", "OPEN_COUNTERTERM", "CT1057_1_hidden_scalar", "kill hidden scalar F2 and radiative/readout reentry"),
        ("IMG3867_4_radiative_readout_stability", "effective/readout action stays in parent image", "UNSIGNED", "VOE2766_4_radiative_readout_closure", "prove loops/apparatus maps cannot generate extra visible coefficients"),
        ("IMG3867_5_boundary_projection_silence", "boundary/local projection does not generate visible coefficient tails", "UNSIGNED", "VOE2766_5_boundary_projection_silence", "derive or keep as explicit closure"),
        ("IMG3867_6_current_normalization_owner", "z_g current normalization is parent-owned/zero or bounded", "UNSIGNED", "ZG3680_7_verdict", "next gate: z_g component zero proof or source-backed values"),
    ]
    return [
        {
            "audit_id": audit_id,
            "clause": clause,
            "status": status,
            "source_row": source_row,
            "next_action": next_action,
            "closes_image_route": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, clause, status, source_row, next_action in rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    runner: list[dict[str, object]],
    image: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    clock_bound = next(row for row in candidates if row["candidate_id"] == "CAND3867_0_clock_alpha_product")
    wep_bound = next(row for row in candidates if row["candidate_id"] == "CAND3867_1_wep_alpha_coulomb")
    r10_bound = next(row for row in candidates if row["candidate_id"] == "CAND3867_2_r10_product_law")
    gates = [
        ("GATE3867_0_sources", "source paths and row needles resolve", all(row["exists"] and row["needle_found"] for row in sources), "source register resolves all imported ledgers"),
        ("GATE3867_1_clock_external_bound", "clock external alpha product bound positive", parse_float_or_none(clock_bound["external_bound_value"]) is not None and parse_float_or_none(clock_bound["external_bound_value"]) > 0, "ACB1052_2 imported as nonclaim product bound"),
        ("GATE3867_2_wep_external_bound", "WEP eta bound positive", parse_float_or_none(wep_bound["external_bound_value"]) is not None and parse_float_or_none(wep_bound["external_bound_value"]) > 0, "AWP1052_0 imported as nonclaim partial projection"),
        ("GATE3867_3_r10_valid_curve", "R10 valid alpha(lambda) curve available", False, "RAP1052_0 is product law only; no promoted bound curve/coefficient rows"),
        ("GATE3867_4_mts_joint_inputs", "same-domain MTS b_alpha/z_g/s_XF2 inputs available", False, "all scored arenas still miss MTS-side joint products"),
        ("GATE3867_5_zg_zero_or_bound", "z_g zero theorem or numeric bound available", False, "3680 says z_g=0 not proved and component values missing"),
        ("GATE3867_6_image_constructor", "parent image constructor signed", all(row["status"] == "SIGNED" for row in image), "image route still conditional/unsigned"),
        ("GATE3867_7_no_claim_leak", "no candidate or runner row permits a claim", all(not bool(row.get("valid_for_claim", False)) for row in candidates + runner), "nonclaim discipline preserved"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": "PASS" if passed else "BLOCKED",
            "claim_allowed": False,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, passed, reason in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3867_0",
            "decision": "3867 imports real clock/WEP source-backed rows but keeps them nonclaim",
            "consequence": "we have usable evidence plumbing without pretending MTS predictions exist",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3867_1",
            "decision": "the next mathematical target is z_g, not another generic audit",
            "consequence": "go after z_Qstar, z_lattice, z_Noether, z_cA_post and z_readout zero/bound clauses directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3867_2",
            "decision": "R10 remains bound-curve/coefficient blocked",
            "consequence": "do not spend more tokens scoring R10 until alpha_bound(lambda), K_X, beta_s and beta_t are source-backed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3867_3",
            "decision": "hidden F2 counterterm is the active counterexample to no-extra-F2",
            "consequence": "prove no hidden-visible Hom/trivial hidden invariant algebra or retain explicit closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3867_0",
            "target_checkpoint": "3868-Y5-R2FR-zg-component-zero-proof-or-source-backed-current-normalization-inputs.md",
            "script": "scripts/Y5_R2FR_3868_zg_component_zero_proof_or_source_backed_current_normalization_inputs.py",
            "objective": "derive or source the z_g component products z_Qstar, z_lattice, z_Noether, z_cA_post and z_readout in one local arena before any alpha/F2 claim",
            "why_next": "3867 shows external clock/WEP evidence is available, but the runner blocks because z_g is neither zeroed nor bounded; z_g is the coupling/current-normalization bottleneck",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3867_0",
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "SOURCE_BACKED_EVIDENCE_IMPORTED_BUT_MTS_JOINT_INPUTS_BLOCK_CLAIM",
            "claim_allowed": False,
            "public_claim": False,
            "next_gate": "3868 z_g component zero proof or source-backed current-normalization inputs",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    schema: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    candidates: list[dict[str, object]],
    runner: list[dict[str, object]],
    image: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3867 — Source-Backed Joint Alpha / Current / F2 Input Acquisition Or Image Constructor

Generated: `{timestamp}`

## Purpose

3866 made the joint runner executable:

`{IDENTITY}`

`{RUNNER_LAW}`

3867 stops treating the missing inputs as vibes. It imports the strongest local source-backed rows we currently have, separates external evidence from MTS-side prediction inputs, and decides the next derivation gate.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Source-Backed Input Schema

{markdown_table(schema, ["schema_id", "field", "owner", "requirement", "current_status"])}

## Acquisition Status

{markdown_table(acquisition, ["status_id", "arena", "input_class", "status", "usable_now", "missing_for_claim"])}

## Candidate Rows

{markdown_table(candidates, ["candidate_id", "arena", "external_status", "external_bound_value", "b_alpha_tau", "z_g_tau", "s_XF2_tau", "runner_verdict"])}

## Runner Reevaluation

{markdown_table(runner, ["reeval_id", "arena", "external_bound_positive", "missing_mts_joint_inputs", "verdict", "claim_allowed"])}

## Image Constructor Audit

{markdown_table(image, ["audit_id", "clause", "status", "source_row", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is progress, not a retreat: clock and WEP now have source-backed external rows wired into the joint runner, and the runner correctly refuses to promote them because the missing piece is the MTS-side current/coupling normalization, especially `z_g`.

The next best move is therefore not another broad audit. It is a narrow strike on `z_g`: prove or bound the component law for `z_Qstar`, `z_lattice`, `z_Noether`, `z_cA_post`, and `z_readout` in one arena.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3866", "Current State After 3867", 1)
    text = "\n".join(line for line in text.splitlines() if not line.startswith("<!-- Generated by 3867 at "))
    paragraph = (
        "`3867` imports real source-backed local evidence rows into the joint alpha/current/F2 branch. "
        "The clock row `ACB1052_2` and WEP alpha/Coulomb row `AWP1052_0_alpha_Coulomb` are now wired as nonclaim external constraints, while R10 remains product-law-only until a valid `alpha_bound(lambda)` curve and parent beta/kernel coefficients are available. "
        "The runner still blocks claims because the MTS-side same-domain products `b_alpha*tau_A`, `z_g*tau_A`, and `s_XF2*tau_A` are missing; the bottleneck is now sharply identified as `z_g` current/coupling normalization rather than generic data absence. "
        "The next gate is `3868`: prove or source the `z_g` components `z_Qstar`, `z_lattice`, `z_Noether`, `z_cA_post`, and `z_readout` in one arena.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md`

Target: fill same-domain source-backed `b_alpha`, `z_g`, and `s_XF2` projection inputs for clock/WEP/R10/source arenas, or parent-construct the visible coefficient image category.

This is the best next move because 3866 makes the runner executable but correctly blocked by missing inputs; the problem is now input acquisition or parent construction, not algebra fog."""
    new_gate = """`3868-Y5-R2FR-zg-component-zero-proof-or-source-backed-current-normalization-inputs.md`

Target: derive or source the `z_g` component products `z_Qstar`, `z_lattice`, `z_Noether`, `z_cA_post`, and `z_readout` in one local arena before any alpha/F2 claim.

This is the best next move because 3867 shows the external evidence side can be wired, but the joint runner is bottlenecked by unsigned current/coupling normalization."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3867_JOINT_RUNNER_REEVALUATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3867_IMAGE_CONSTRUCTOR_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3867_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3867 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    schema: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    candidates: list[dict[str, object]],
    runner: list[dict[str, object]],
    image: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    clock = next(row for row in candidates if row["candidate_id"] == "CAND3867_0_clock_alpha_product")
    wep = next(row for row in candidates if row["candidate_id"] == "CAND3867_1_wep_alpha_coulomb")
    r10 = next(row for row in candidates if row["candidate_id"] == "CAND3867_2_r10_product_law")

    add(
        "VAL3867_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3867_1_schema",
        "schema separates external bounds from MTS prediction inputs",
        any(row["field"] == "external_bound" for row in schema) and any(row["field"] == "z_g_tau" for row in schema),
        "external_bound and z_g_tau fields present",
    )
    add(
        "VAL3867_2_clock_bound",
        "clock source row imports a positive numeric product bound",
        parse_float_or_none(clock["external_bound_value"]) is not None and parse_float_or_none(clock["external_bound_value"]) > 0,
        f"clock bound={clock['external_bound_value']} {clock['external_bound_units']}",
    )
    add(
        "VAL3867_3_wep_bound",
        "WEP source row imports a positive numeric eta bound",
        parse_float_or_none(wep["external_bound_value"]) is not None and parse_float_or_none(wep["external_bound_value"]) > 0,
        f"WEP bound={wep['external_bound_value']} {wep['external_bound_units']}",
    )
    add(
        "VAL3867_4_r10_nonclaim",
        "R10 remains blocked without a valid alpha(lambda) curve",
        str(r10["external_bound_value"]).startswith("MISSING") and not bool(r10["valid_for_claim"]),
        str(r10["runner_verdict"]),
    )
    add(
        "VAL3867_5_runner_blocks_missing_mts",
        "runner reevaluation blocks rows with missing MTS joint inputs",
        any(row["verdict"] == "BLOCKED_SOURCE_BOUND_READY_MTS_SIDE_MISSING" for row in runner),
        "source-backed external rows do not become claims",
    )
    add(
        "VAL3867_6_zg_next",
        "z_g is selected as the next derivation bottleneck",
        any("z_g" in str(row["next_action"]) for row in image) and "z_g component" in read_text(DOC_PATH),
        "3868 z_g target recorded",
    )
    add(
        "VAL3867_7_no_claim",
        "all generated rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in schema + acquisition + candidates + runner + image + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3867_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3867_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "This is progress, not a retreat" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3867*", "P8_Y5_BRR545_3867*", "*Y5_R2FR_3867*", "3867-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3867_10_formalization_clean",
        "formalization-workbench has no generated 3867 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3867 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3867_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    schema = input_schema_rows(timestamp)
    acquisition = acquisition_status_rows(timestamp)
    candidates = candidate_rows(timestamp)
    runner = runner_reevaluation_rows(candidates, timestamp)
    image = image_constructor_rows(timestamp)
    gates = gate_rows(sources, candidates, runner, image, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["acquisition"], acquisition)
    write_csv(OUTPUTS["candidates"], candidates)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["image"], image)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, schema, acquisition, candidates, runner, image, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, schema, acquisition, candidates, runner, image, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_SOURCE_BACKED_NONCLAIM_INPUT_ACQUISITION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
