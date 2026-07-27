from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SOURCE_FEEDBACK_EPSILON_SIGMA_OR_PPN_GAUGE_BOUND_2371"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2371-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"
ALPHA_READOUT_TARGET = "0.005788015401465051"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2371_2370_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2370_NEXT_TARGET.csv", "NEXT2370_0_selected", "2370 selected source-feedback epsilon_sigma / PPN gauge branch"),
        ("SRC2371_2370_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2370_VALIDATION.csv", "VAL2370_OVERALL", "2370 validation"),
        ("SRC2371_2325_feedback", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2325_EPSILON_SIGMA_FEEDBACK_CONTRACT.csv", "ESC2325_2_feedback_bound", "epsilon_sigma feedback contract"),
        ("SRC2371_2325_ppn_gauge", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2325_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv", "PGB2325_3_bound_contract", "PPN gauge/calibration fallback contract"),
        ("SRC2371_2325_score", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2325_ALPHA_READOUT_SCORE_READINESS.csv", "SRS2325_2_first_numeric_priority", "alpha_readout first numeric priority"),
        ("SRC2371_2326_eps_zero", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_EPSILON_SIGMA_ZERO_CERTIFICATE_ATTEMPT.csv", "ESZ2326_4_verdict", "epsilon_sigma zero certificate attempt"),
        ("SRC2371_2326_leak", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_FIRST_PROTOCOL_LEAKAGE_ROW.csv", "PLR2326_0_source_GM", "first protocol leakage row"),
        ("SRC2371_2326_inputs", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_PROTOCOL_INPUT_REQUIREMENTS.csv", "PIR2326_2_L_source_GM", "protocol input requirements"),
        ("SRC2371_2326_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_NEXT_TARGET.csv", "NEXT2326_0", "source_GM profile route selected"),
        ("SRC2371_2327_universality", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2327_SOURCE_GM_UNIVERSALITY_ATTEMPT.csv", "UGM2327_6_verdict", "source_GM universality attempt"),
        ("SRC2371_2327_lsource", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2327_LSOURCEGM_BOUND_ROW.csv", "LSGM2327_0_bound_contract", "L_source_GM finite bound row"),
        ("SRC2371_2327_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2327_NEXT_TARGET.csv", "NEXT2327_0", "NoSourceOnlySpeciesSlot selected by source_GM audit"),
        ("SRC2371_2328_nosource", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2328_NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT.csv", "NSOS2328_6_verdict", "NoSourceOnlySpeciesSlot derivation attempt"),
        ("SRC2371_2328_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2328_NEXT_TARGET.csv", "NEXT2328_0", "parent-action source-blind functor route"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def epsilon_sigma_zero_audit() -> list[dict[str, object]]:
    rows = [
        (
            "ESZA2371_0_definition",
            "epsilon_sigma_A",
            "epsilon_sigma_A := ||D_v sigma_A|| for source/readout protocol variables sigma_A and vertical v in ker(Dq)",
            "DEFINITION_LOCKED",
            "zero requires sigma_A=sigma_bar_A(q,e_obs,theta) or fixed external protocol before variation",
        ),
        (
            "ESZA2371_1_exact_zero",
            "descent/fixed-protocol zero",
            "If sigma_A descends through fixed observed quotient data or is declared fixed before variation, then D_v sigma_A=0 and the corresponding feedback tail vanishes.",
            "EXACT_CONDITIONAL_THEOREM",
            "not active because source profile, GM calibration, masks/support and boundary protocol are not parent-signed together",
        ),
        (
            "ESZA2371_2_source_profile",
            "sigma_source_profile",
            "source density, composition, support/worldtube and weighting basis must be quotient-owned or fixed protocol",
            "NOT_PARENT_SIGNED",
            "relative profile/composition residual can still feed C_source_GM",
        ),
        (
            "ESZA2371_3_GM_common_mode",
            "sigma_GM_common_mode",
            "one universal source normalization can be absorbed into measured G/GM, but relative source factors cannot",
            "GUARD_ACTIVE_NOT_NUMERIC",
            "same-branch calibration equation and relative source basis are missing",
        ),
        (
            "ESZA2371_4_protocol_boundary",
            "mask/orbit/boundary protocol",
            "support masks, orbit windows, attitude and boundary transport must either be fixed protocol or quotient descendants",
            "CLOSURE_OR_SOURCE_REQUIRED",
            "official protocol arrays or parent descent certificate missing",
        ),
        (
            "ESZA2371_5_verdict",
            "active epsilon_sigma zero",
            "all source/readout protocol variables required by alpha_readout have epsilon_sigma_A=0",
            "NOT_DERIVED_RETAIN_LEAKAGE_ROW",
            "source_GM channel remains the first live feedback input",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "sigma_piece": piece,
            "statement": statement,
            "status": status,
            "gap_or_effect": gap,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def first_protocol_leakage_row() -> list[dict[str, object]]:
    rows = [
        (
            "PLR2371_0_source_GM",
            "C_source_GM",
            "|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM",
            "L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||",
            "epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||",
            ALPHA_READOUT_TARGET,
            "dimensionless alpha_PPN_total_abs_vector budget",
            "CONTRACT_READY_VALUES_MISSING",
            "needs L_source_GM and epsilon_sigma_source_GM numeric or theorem-zero rows",
        ),
        (
            "PLR2371_1_LsourceGM_input",
            "L_source_GM",
            "operator/source-current Lipschitz norm in the Pi_gamma-projected source_GM channel",
            "requires norm convention, J_source norm, D_sigma Pi_source and D_sigma J_source",
            "not applicable",
            "MISSING_OPERATOR_NORM_AND_SOURCE_CURRENT_NORM",
            "declared protocol norm after PPN normalization",
            "INPUT_MISSING",
            "cannot produce alpha_readout prediction without units, basis and projection",
        ),
        (
            "PLR2371_2_epsilon_input",
            "epsilon_sigma_source_GM",
            "source profile/GM protocol leakage norm",
            "zero if source_GM universality and NoSourceOnlySpeciesSlot are parent-signed",
            "||D_v(sigma_source_profile, sigma_GM_common_mode)||",
            "MISSING_ZERO_CERTIFICATE_OR_NUMERIC_BOUND",
            "declared protocol norm",
            "INPUT_MISSING",
            "finite source-profile vector remains fallback",
        ),
        (
            "PLR2371_3_no_cancellation_policy",
            "source_GM absolute contribution",
            "source_GM must pass by absolute budget, not cancellation against alpha_cg, disformal, non-Hilbert, support, boundary or readout tails",
            "absolute-vector policy inherited from PPN vector source row",
            "epsilon_sigma_source_GM",
            ALPHA_READOUT_TARGET,
            "dimensionless ceiling before sibling tails",
            "NONCLAIM_TARGET_ONLY",
            "local-GR branch remains blocked until the whole absolute vector is complete",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_bound": formula,
            "lipschitz_factor": lipschitz,
            "epsilon_symbol": epsilon,
            "target_or_value": target,
            "units": units,
            "status": status,
            "missing_for_score": missing,
        }
        for row_id, quantity, formula, lipschitz, epsilon, target, units, status, missing in rows
    ]


def ppn_gauge_calibration_bound_row() -> list[dict[str, object]]:
    rows = [
        (
            "PGB2371_0_source_target",
            "PPN_gauge_calibration_readout_tail_target",
            f"abs(Pi_gamma[Delta_cal+Delta_PPN]) <= {ALPHA_READOUT_TARGET} as a nonclaim target",
            ALPHA_READOUT_TARGET,
            "dimensionless",
            "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv::PVS2200_2_vector_contract",
        ),
        (
            "PGB2371_1_delta_cal",
            "Delta_cal",
            "M_eff[Pi_M J_H] - M_Gauss_orbital projected into gamma/readout channel",
            "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL",
            "dimensionless_or_declared_projection_units",
            "INPUT_MISSING",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv::MGV2203_7_calibration_PPN_tail",
        ),
        (
            "PGB2371_2_delta_ppn",
            "Delta_PPN",
            "PPN gauge/source-normalization residual after fixing G_ref and observed source mass",
            "MISSING_PPN_GAUGE_TRANSFORM_AND_SOURCE_NORMALIZATION",
            "dimensionless_or_declared_projection_units",
            "INPUT_MISSING",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv::PPNB2208_2_source_normalization;PPNB2208_3_PPN_gauge",
        ),
        (
            "PGB2371_3_bound_contract",
            "gauge_calibration_abs_envelope",
            "abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN) <= target after same-frame source normalization",
            "MISSING_TERM_BOUNDS",
            "dimensionless",
            "BOUND_CONTRACT_READY_VALUES_MISSING",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2208_PPN_GREEN_OPERATOR_LOWERING.csv::PPNL2208_3_source_normalization",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_bound": formula,
            "numeric_value": value,
            "units": units,
            "status": status,
            "source_anchor": source,
        }
        for row_id, quantity, formula, value, units, status, source in rows
    ]


def source_gm_universality_audit() -> list[dict[str, object]]:
    rows = [
        (
            "UGM2371_0_target",
            "source_GM profile universality",
            "D_v(sigma_source_profile, sigma_GM_common_mode)=0, hence epsilon_sigma_source_GM=0, if source profile/support and GM calibration descend through the same observed quotient data.",
            "TARGET_SHARPENED",
            "this is the exact zero route for the first source_GM leakage channel",
        ),
        (
            "UGM2371_1_common_monopole",
            "universal exterior common-mode monopole",
            "If J_H is conserved, source support is fixed, one G_ref/source measure is used and all source response is common-mode, the leading exterior source leg is calibrated GM/r^2 plus bounded multipoles.",
            "EXACT_CONDITIONAL_LEMMA",
            "works only for universal source factor, not relative profile/composition residuals",
        ),
        (
            "UGM2371_2_no_source_only_species_slot",
            "NoSourceOnlySpeciesSlot",
            "The parent object language must not admit species/material source weights w_A that multiply active gravitational source strength independently of non-gravitational normalization.",
            "SHARPEST_MISSING_PREMISE",
            "otherwise S_m=sum_A(1+epsilon_A)S_A remains a covariant countermodel",
        ),
        (
            "UGM2371_3_GM_calibration",
            "measured GM common-mode guard",
            "Fitted GM may absorb one universal source normalization, but it cannot absorb relative source/profile/composition residuals.",
            "GUARD_ACTIVE_NOT_NUMERIC",
            "calibration equation and relative source basis are not source-filled",
        ),
        (
            "UGM2371_4_profile_weighting",
            "orbit/worldtube-weighted source profile",
            "sigma_source_profile must be quotient-owned/fixed-protocol data or a source-backed orbit/profile/worldtube vector in the same basis as response projection.",
            "SOURCE_PROFILE_AND_COMPOSITION_OBSTRUCTION_ACTIVE",
            "bulk source composition is not enough; support/worldtube weighting or cancellation theorem is needed",
        ),
        (
            "UGM2371_5_same_frame_pullback",
            "same-frame source pullback",
            "force law, source variation, clocks, orbit and eta/PPN readout must use the same observed coframe/time generator or retain a frame-source residual.",
            "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED",
            "profile theorem cannot close local GR if source and readout legs live in different effective frames",
        ),
        (
            "UGM2371_6_verdict",
            "promote epsilon_sigma_source_GM=0",
            "Current parent primitives prove source_GM profile/GM universality strongly enough to set epsilon_sigma_source_GM=0.",
            "NOT_PROVED_USE_BOUND_OR_PARENT_SYNTAX_ROUTE",
            "NoSourceOnlySpeciesSlot, profile/source vector, GM calibration equation, finite-source/multipole handling and same-frame pullback remain open",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_or_obstruction": obstruction,
        }
        for row_id, piece, statement, status, obstruction in rows
    ]


def no_source_only_parallel_route() -> list[dict[str, object]]:
    rows = [
        (
            "NSOS2371_0_countermodel",
            "covariant source-only weights survive unless excluded",
            "Diffeomorphism covariance alone permits S_m=sum_A w_A S_A with constant scalar species weights.",
            "COUNTERMODEL_ACTIVE",
            "do not claim WEP/local-GR descent from covariance alone",
        ),
        (
            "NSOS2371_1_hilbert_current",
            "Hilbert-current ownership",
            "Once S_matter is fixed, the gravitational source is the Hilbert variation with respect to e_obs/g_obs before readout.",
            "EXACT_SUBTHEOREM_BUT_NOT_ENOUGH",
            "kills post-variation source rescaling, not pre-variation w_A inside S_matter",
        ),
        (
            "NSOS2371_2_source_blind_functor",
            "source-blind matter functor theorem",
            "If ordinary matter is a source-blind descended functor with one observed measure, one Hilbert-source natural transformation and no independent SpeciesLabel -> Coeff_active_source object, then w_A is common calibration, ordinary theta_A data, or inadmissible.",
            "EXACT_CONDITIONAL_THEOREM",
            "this is the cleanest parent-action signature to try next",
        ),
        (
            "NSOS2371_3_common_scale",
            "common source scale quotient",
            "A single common factor multiplying total T_matter is absorbed into kappa/G_N/GM calibration once.",
            "EXACT_IF_SINGLE_SCALE",
            "relative species/source coefficients still require parent syntax or finite source vector",
        ),
        (
            "NSOS2371_4_verdict",
            "NoSourceOnlySpeciesSlot active branch",
            "The active corpus already signs the source-blind functor/admissibility clauses strongly enough to remove source-only species weights.",
            "NOT_PARENT_SIGNED",
            "write the parent-action signature or stage finite source-profile vector",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route_piece": piece,
            "formal_statement": statement,
            "status": status,
            "effect_or_gap": gap,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2371_0_feedback_contract",
            "C_feedback/source_GM leakage row",
            1,
            "LOCKED_NONCLAIM_CONTRACT",
            "the useful normal form is now |Pi_gamma C_source_GM| <= |Pi_gamma| L_source_GM epsilon_sigma_source_GM",
        ),
        (
            "DEC2371_1_epsilon_zero",
            "epsilon_sigma zero theorem",
            1,
            "KEEP_CONDITIONAL_UNSIGNED",
            "exact if source/readout protocol variables descend or are fixed before variation; not signed for source_GM",
        ),
        (
            "DEC2371_2_ppn_gauge",
            "Delta_cal/Delta_PPN fallback",
            2,
            "STAGE_PARALLEL_NONCLAIM",
            "keeps a concrete PPN target but does not create an MTS prediction",
        ),
        (
            "DEC2371_3_nosource",
            "NoSourceOnlySpeciesSlot parent syntax",
            1,
            "SELECT_NEXT_DERIVATION_TARGET",
            "this is the least hand-wavy route: remove the source-only coupling countermodel at parent-action level",
        ),
        (
            "DEC2371_4_finite_source",
            "finite source-profile vector",
            2,
            "FALLBACK_IF_PARENT_SIGNATURE_FAILS",
            "honest bound route if source-blind functor cannot be signed",
        ),
        (
            "DEC2371_5_local_gr",
            "local GR/PPN pass",
            5,
            "DEFER",
            "absolute PPN vector still lacks alpha_readout component values and sibling tails",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        (
            "GATE2371_0_epsilon_zero",
            "epsilon_sigma_source_GM zero active",
            "FAIL",
            "NoSourceOnlySpeciesSlot/source-blind functor and source_GM descent are not parent-signed",
        ),
        (
            "GATE2371_1_feedback_prediction",
            "C_source_GM numeric prediction or zero theorem",
            "FAIL",
            "L_source_GM and epsilon_sigma_source_GM are missing values or active zero",
        ),
        (
            "GATE2371_2_ppn_gauge",
            "Delta_cal/Delta_PPN same-frame bound",
            "FAIL",
            "target exists but term bounds and same-frame source normalization are missing",
        ),
        (
            "GATE2371_3_vector_completion",
            "absolute local PPN vector complete",
            "FAIL",
            "sibling PPN/local tails remain unclosed",
        ),
        (
            "GATE2371_4_public_claim",
            "R10/WEP/PPN/local-GR public pass",
            "FAIL",
            "2371 is private scaffolding and refusal-runner evidence only",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        (
            "REF2371_0_no_zero_promotion",
            "Refuse to set epsilon_sigma_source_GM=0 from covariance/common-mode language alone.",
            "relative source-only species weights remain a countermodel",
        ),
        (
            "REF2371_1_no_numeric_alpha",
            "Refuse to publish alpha_readout or alpha_PPN_total as a numeric MTS prediction.",
            "C_feedback, Delta_cal, Delta_PPN, C_protocol and sibling tails lack values",
        ),
        (
            "REF2371_2_no_github_claim",
            "Refuse to describe the local branch as GR-derived/pass-ready.",
            "this checkpoint is private derivation discipline, not public claim text",
        ),
        (
            "REF2371_3_no_data_substitution",
            "Refuse to replace parent-action coupling derivation with a fitted source leakage parameter.",
            "finite source-profile vectors are fallback bounds, not the desired derivation",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "refusal": refusal,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, refusal, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2371_0_selected",
            "2372-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md",
            "scripts/Y5_R2FR_parent_action_source_blind_functor_signature_or_source_profile_vector_2372.py",
            "prove the parent matter action is a source-blind descended functor with no SpeciesLabel -> Coeff_active_source object, so NoSourceOnlySpeciesSlot becomes parent-signed",
            "if this cannot be signed, stage a finite source-profile/vector acquisition row with basis, units, frame, GM calibration and L_source_GM",
        ),
        (
            "NEXT2371_1_parallel",
            "2372b-Y5-R2FR-LsourceGM-bound-row-and-PPN-gauge-calibration-residual.md",
            "scripts/Y5_R2FR_LsourceGM_bound_row_and_PPN_gauge_calibration_residual_2372b.py",
            "fill L_source_GM, epsilon_sigma_source_GM, Delta_cal or Delta_PPN from source-backed same-frame inputs",
            "keep alpha_readout nonclaim if any value is a target, placeholder or differently framed source",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_SOURCE_REGISTER.csv",
        "epsilon_sigma_zero_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_EPSILON_SIGMA_ZERO_AUDIT.csv",
        "first_protocol_leakage_row": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_FIRST_PROTOCOL_LEAKAGE_ROW.csv",
        "ppn_gauge_calibration_bound_row": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv",
        "source_gm_universality_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_SOURCE_GM_UNIVERSALITY_AUDIT.csv",
        "nosourceonly_parallel_route": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_NOSOURCEONLY_PARALLEL_ROUTE.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_DECISION_LEDGER.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2371_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2371_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    epsilon_rows = read_csv(outputs["epsilon_sigma_zero_audit"])
    leak_rows = read_csv(outputs["first_protocol_leakage_row"])
    gauge_rows = read_csv(outputs["ppn_gauge_calibration_bound_row"])
    ugm_rows = read_csv(outputs["source_gm_universality_audit"])
    nsos_rows = read_csv(outputs["nosourceonly_parallel_route"])
    decision_rows = read_csv(outputs["decision_ledger"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        (
            "VAL2371_00_required_sources_exist",
            all(row["path_exists"] == "true" for row in source_rows),
            "all required source paths exist",
        ),
        (
            "VAL2371_01_required_needles_found",
            all(row["needle_found"] == "true" for row in source_rows),
            "all source needles found",
        ),
        (
            "VAL2371_02_outputs_exist",
            all(path.exists() for path in generated_paths),
            "all 2371 output files written",
        ),
        (
            "VAL2371_03_csv_parse",
            parsed_ok,
            "all generated CSV files parse and contain rows",
        ),
        (
            "VAL2371_04_epsilon_definition_locked",
            any(row["row_id"] == "ESZA2371_0_definition" and row["status"] == "DEFINITION_LOCKED" for row in epsilon_rows),
            "epsilon_sigma definition locked",
        ),
        (
            "VAL2371_05_epsilon_zero_not_promoted",
            any(row["row_id"] == "ESZA2371_5_verdict" and row["status"].startswith("NOT_DERIVED") for row in epsilon_rows),
            "epsilon_sigma zero remains nonclaim",
        ),
        (
            "VAL2371_06_feedback_contract_ready",
            any(row["row_id"] == "PLR2371_0_source_GM" and "L_source_GM" in row["lipschitz_factor"] for row in leak_rows),
            "source_GM feedback bound contract written",
        ),
        (
            "VAL2371_07_feedback_values_missing",
            any(row["row_id"] == "PLR2371_1_LsourceGM_input" and row["status"] == "INPUT_MISSING" for row in leak_rows),
            "L_source_GM numeric input remains missing",
        ),
        (
            "VAL2371_08_ppn_gauge_fallback_nonclaim",
            any(row["row_id"] == "PGB2371_0_source_target" and row["status"] == "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION" for row in gauge_rows),
            "PPN gauge fallback imported as target only",
        ),
        (
            "VAL2371_09_source_gm_not_proved",
            any(row["row_id"] == "UGM2371_6_verdict" and row["status"].startswith("NOT_PROVED") for row in ugm_rows),
            "source_GM universality not promoted",
        ),
        (
            "VAL2371_10_nosource_route_selected",
            any(row["row_id"] == "NSOS2371_2_source_blind_functor" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in nsos_rows)
            and any(row["row_id"] == "DEC2371_3_nosource" and row["decision"] == "SELECT_NEXT_DERIVATION_TARGET" for row in decision_rows),
            "NoSourceOnlySpeciesSlot/source-blind functor selected next",
        ),
        (
            "VAL2371_11_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2371_12_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
        (
            "VAL2371_13_next_selected",
            any(row["row_id"] == "NEXT2371_0_selected" and "source_blind_functor" in row["next_script"] for row in next_rows),
            "2372 parent-action source-blind functor target selected",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2371_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2371 valid: source-feedback equation locked, epsilon_sigma zero not promoted, NoSourceOnlySpeciesSlot parent-action route selected"
            if overall_ok
            else "2371 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    eps = read_csv(outputs["epsilon_sigma_zero_audit"])
    leak = read_csv(outputs["first_protocol_leakage_row"])
    gauge = read_csv(outputs["ppn_gauge_calibration_bound_row"])
    ugm = read_csv(outputs["source_gm_universality_audit"])
    nsos = read_csv(outputs["nosourceonly_parallel_route"])
    decision = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    generated = [rel(path) for path in outputs.values()]
    text = f"""# 2371 - Source-Feedback epsilon_sigma Or PPN Gauge Bound Row

## Result

`C_feedback` has been tightened into the first concrete source-channel nonclaim contract:

`|Pi_gamma C_source_GM| <= |Pi_gamma| * L_source_GM * epsilon_sigma_source_GM`.

with

`L_source_GM = ||D_sigma Pi_source||||J_source|| + ||Pi_source||||D_sigma J_source||`

and

`epsilon_sigma_source_GM = ||D_v(sigma_source_profile, sigma_GM_common_mode)||`.

This does **not** close local GR.  The exact zero theorem exists only conditionally: if source/readout protocol variables descend through `(q,e_obs,theta)` or are fixed external protocol before variation, then `epsilon_sigma_A=0`.  The source_GM channel is not parent-signed, because relative source-only species/coupling weights still survive as a countermodel.

The best derivation route is now the coupling route: prove a parent-action `NoSourceOnlySpeciesSlot` / source-blind matter-functor signature.  The finite fallback is to acquire a source-profile vector plus `L_source_GM`, same-frame GM calibration, and PPN gauge residual bounds.

## epsilon_sigma Zero Audit

{md_table(eps, ["row_id", "sigma_piece", "status", "gap_or_effect"])}

## First Protocol Leakage Row

{md_table(leak, ["row_id", "quantity", "formula_or_bound", "target_or_value", "status", "missing_for_score"])}

## PPN Gauge / Calibration Fallback

{md_table(gauge, ["row_id", "quantity", "numeric_value", "status"])}

## Source_GM Universality Audit

{md_table(ugm, ["row_id", "claim_piece", "status", "proof_or_obstruction"])}

## NoSourceOnlySpeciesSlot Parallel Route

{md_table(nsos, ["row_id", "route_piece", "status", "effect_or_gap"])}

## Decision Ledger

{md_table(decision, ["row_id", "route", "rank", "decision", "reason"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "reason"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is a useful narrowing.  The local-GR problem is no longer a vague "PPN residue" problem; it is a coupling/source-ownership problem.  If the parent action forbids independent source-only species weights, the source_GM leakage route can collapse by theorem.  If it does not, the branch must carry finite source-profile and calibration vectors as explicit nonclaim bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["epsilon_sigma_zero_audit"], epsilon_sigma_zero_audit())
    write_csv(outputs["first_protocol_leakage_row"], first_protocol_leakage_row())
    write_csv(outputs["ppn_gauge_calibration_bound_row"], ppn_gauge_calibration_bound_row())
    write_csv(outputs["source_gm_universality_audit"], source_gm_universality_audit())
    write_csv(outputs["nosourceonly_parallel_route"], no_source_only_parallel_route())
    write_csv(outputs["decision_ledger"], decision_ledger())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
