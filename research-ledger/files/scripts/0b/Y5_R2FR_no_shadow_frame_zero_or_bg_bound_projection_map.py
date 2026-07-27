from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1740"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1740 - No Shadow Frame Zero Or b_g Bound Projection Map"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1740_0_1739_doc",
        "source_key": "1739_handoff_doc",
        "source_path": ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
        "needles": ["NEXT1739_0_primary", "VAL1739_OVERALL"],
    },
    {
        "source_id": "SRC1740_1_1739_shadow_gate",
        "source_key": "1739_shadow_frame_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_SHADOW_FRAME_COUNTERMODEL_GATE.csv",
        "needles": ["SFC1739_0_Weyl", "SFC1739_2_source_prefactor"],
    },
    {
        "source_id": "SRC1740_2_1739_bg_rows",
        "source_key": "1739_bg_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
        "needles": ["BG1739_5_total_abs", "RETAINED_NONCLAIM_BG_ROW"],
    },
    {
        "source_id": "SRC1740_3_1739_bound_schema",
        "source_key": "1739_bound_projection_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_BG_LOCAL_BOUND_PROJECTION_SCHEMA.csv",
        "needles": ["BGP1739_4_R10", "BLOCKED_PENDING_BG_AND_ARENA_MAP"],
    },
    {
        "source_id": "SRC1740_4_943_coframe_contract",
        "source_key": "943_coframe_coupling_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_6_no_shadow_frame_rule", "candidate_repair_contract_not_theorem"],
    },
    {
        "source_id": "SRC1740_5_1045_matter_functor",
        "source_key": "1045_matter_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_4_no_shadow_frame", "GUARD_WRITTEN_NOT_PARENT_DERIVED"],
    },
    {
        "source_id": "SRC1740_6_1504_countermodel",
        "source_key": "1504_common_frame_countermodel",
        "source_path": RESIDUALS / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv",
        "needles": ["OC1504_3_universal_conformal_countermodel", "COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1740_7_1229_counterexamples",
        "source_key": "1229_source_counterexamples",
        "source_path": RESIDUALS / "P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["CEX1229_0_action_multiplier", "ACTIVE"],
    },
    {
        "source_id": "SRC1740_8_1229_finite_residual",
        "source_key": "1229_finite_source_residual_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1229_FINITE_SOURCE_RESIDUAL_CONTRACT.csv",
        "needles": ["FR1229_2_qsource", "DERIVED_AS_REQUIRED_OBJECT_NOT_ZERO"],
    },
    {
        "source_id": "SRC1740_9_local_bounds",
        "source_key": "local_bound_claims",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R10_fifth_force", "alpha(lambda)"],
    },
    {
        "source_id": "SRC1740_10_R10_curve",
        "source_key": "R10_alpha_lambda_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needles": ["MISSING_DIGITIZED_ALPHA_BOUND", "valid_for_claim"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_SOURCE_REGISTER.csv",
    "no_shadow_clause_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
    "zero_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_ZERO_THEOREM_ATTEMPT.csv",
    "bg_projection_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_PROJECTION_MAP.csv",
    "bg_bound_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_INPUT_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1740_VALIDATION.csv",
}


COPY_MAP = {
    "no_shadow_clause_gate": "R2FR_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
    "zero_theorem_attempt": "R2FR_1740_NO_SHADOW_FRAME_ZERO_THEOREM_ATTEMPT.csv",
    "bg_projection_map": "R2FR_1740_BG_BOUND_PROJECTION_MAP.csv",
    "bg_bound_rows": "R2FR_1740_BG_BOUND_INPUT_ROWS.csv",
    "runner_refusal": "R2FR_1740_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1740_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1740_CLAIM_GATE.csv",
    "next_target": "R2FR_1740_NEXT_TARGET.csv",
}


NO_SHADOW_CLAUSES = [
    {
        "clause_id": "NSF1740_0_parent_matter_domain",
        "clause": "ordinary matter domain",
        "required_statement": "ordinary matter fields are sections over the owned observed coframe, not over residual/shadow frames.",
        "mathematical_test": "S_A=S_A[Psi_A,e_obs,omega[e_obs],theta_A] and no X-dependent frame argument appears.",
        "current_status": "MATTER_FUNCTOR_NOT_PARENT_SIGNED",
        "blocker": "1045 keeps the matter functor signature unsigned.",
    },
    {
        "clause_id": "NSF1740_1_no_Weyl_shadow",
        "clause": "no common Weyl shadow frame",
        "required_statement": "A(X)^2 g_obs or exp(b_g X)e_obs is forbidden unless A is quotient-owned constant/gauge or retained.",
        "mathematical_test": "partial_X ln A = 0 or b_g,X finite row is scored.",
        "current_status": "WEYL_COUNTERMODEL_SURVIVES",
        "blocker": "1504/1739 keep universal conformal dependence legal.",
    },
    {
        "clause_id": "NSF1740_2_no_disformal_shadow",
        "clause": "no common disformal shadow frame",
        "required_statement": "C(X)g_obs+D(X)u_mu u_nu is forbidden unless C_X,D_X are zero-derived or retained.",
        "mathematical_test": "partial_X C=0 and partial_X D=0, or PPN/clock/preferred-frame rows carry the residual.",
        "current_status": "DISFORMAL_COUNTERMODEL_SURVIVES",
        "blocker": "943 frames this as an exact repair contract, not a current theorem.",
    },
    {
        "clause_id": "NSF1740_3_no_source_prefactor",
        "clause": "no hidden source-only prefactor",
        "required_statement": "w_A(X)S_A cannot survive unless w_A is universal/quotient-owned or retained as source residual.",
        "mathematical_test": "delta w_A=0 or q_source^nu=P_loc nabla_mu[sum_A delta w_A T_A^munu]+... is bounded.",
        "current_status": "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
        "blocker": "1229 shows source weights alter Hilbert source even when equations look classical.",
    },
    {
        "clause_id": "NSF1740_4_no_post_readout_frame",
        "clause": "no post-readout detector/source frame",
        "required_statement": "detector, ruler, clock and source projections cannot apply X-dependent frame kernels after variation.",
        "mathematical_test": "Dreadout_frame[X]=0 or finite readout residual rows are required.",
        "current_status": "READOUT_FRAME_REOPENING_NOT_EXCLUDED",
        "blocker": "readout/marker branch remains held parallel from 1739.",
    },
    {
        "clause_id": "NSF1740_5_boundary_endpoint",
        "clause": "no boundary endpoint shadow coframe",
        "required_statement": "endpoint/cosmological boundary data do not create a local X-dependent coframe.",
        "mathematical_test": "P_loc partial_Q_endpoint e_obs=0 or finite endpoint b_g row.",
        "current_status": "BOUNDARY_ENDPOINT_SILENCE_OPEN",
        "blocker": "1738/1739 keep boundary endpoint row finite nonclaim.",
    },
    {
        "clause_id": "NSF1740_6_verdict",
        "clause": "no-shadow-frame verdict",
        "required_statement": "NSF1740_0 through NSF1740_5 all close in the same parent action branch.",
        "mathematical_test": "all Weyl/disformal/source-prefactor/readout/endpoint shadow derivatives vanish or are explicitly finite residuals.",
        "current_status": "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED",
        "blocker": "the rule is correct as a contract, but current parent action evidence does not forbid all shadow routes.",
    },
]


PROJECTIONS = [
    {
        "projection_id": "BMAP1740_0_WEP",
        "arena": "WEP",
        "observable": "eta_AB",
        "mapping_formula": "|eta_AB| <= K_WEP_bg |epsilon_bg_abs| + K_WEP_w |Delta w_AB| + K_marker |b_marker_AB|",
        "bound_row": "R0_identity_coframe_direct;R1_WEP_source_charge",
        "required_inputs": "epsilon_bg_abs;K_WEP_bg;Delta_w_AB;marker/source readout map",
    },
    {
        "projection_id": "BMAP1740_1_gamma_beta",
        "arena": "PPN_metric",
        "observable": "gamma_minus_1;beta_minus_1",
        "mapping_formula": "|Delta_PPN_metric| <= K_gamma_bg |epsilon_bg_abs| + K_source |delta w_source|",
        "bound_row": "R3_gamma;R4_beta",
        "required_inputs": "epsilon_bg_abs;weak_field_metric_response;source_normalization_map",
    },
    {
        "projection_id": "BMAP1740_2_preferred_frame",
        "arena": "PPN_preferred_frame",
        "observable": "alpha1;alpha2;alpha3;xi",
        "mapping_formula": "|alpha_i| <= K_disformal_i |b_disformal| + K_tau_i |Delta tau| + K_boundary_i |b_boundary|",
        "bound_row": "R5_alpha1;R6_alpha2;R7_alpha3;R8_xi",
        "required_inputs": "disformal coefficients;tau pushforward row;boundary endpoint row",
    },
    {
        "projection_id": "BMAP1740_3_clock_orbital",
        "arena": "clock_orbital",
        "observable": "alpha_clock;Gdot_over_G",
        "mapping_formula": "|clock/orbit residual| <= K_clock_bg |epsilon_bg_abs| + K_const |b_theta| + K_tau |Delta tau|",
        "bound_row": "R2_clock_redshift;R9_Gdot",
        "required_inputs": "clock standards map;constant owner row;tau/orbit projection",
    },
    {
        "projection_id": "BMAP1740_4_R10",
        "arena": "R10_short_range",
        "observable": "alpha(lambda)",
        "mapping_formula": "|alpha_pred(lambda)| = |K_R10(lambda) epsilon_bg_abs + K_w(lambda) delta w + K_marker(lambda)b_marker| <= alpha_bound(lambda)",
        "bound_row": "R10_fifth_force",
        "required_inputs": "digitized alpha(lambda) curve;lambda map;material geometry;source/test legs;epsilon_bg_abs",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def no_shadow_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **clause,
            "parent_signed": no(),
            "zero_theorem_closed": no(),
            "finite_row_required": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for clause in NO_SHADOW_CLAUSES
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NSF1740_THM0_exact_contract",
            "statement": "If the parent matter/coframe action has no residual frame, no source prefactor, no post-readout frame, and no endpoint projection, then b_g and shadow-frame rows vanish.",
            "mathematical_form": "partial_X A=partial_X C=partial_X D=delta w_A=P_loc partial_Qendpoint e_obs=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "MISSING_PARENT_MATTER_FUNCTOR;MISSING_NO_SHADOW_FRAME_RULE;MISSING_SOURCE_PREFACTOR_ZERO;MISSING_ENDPOINT_SILENCE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NSF1740_THM1_current_claim",
            "statement": "Current MTS proves no-shadow-frame zero for all local residual routes.",
            "mathematical_form": "NSF1740_0..NSF1740_5 all parent-signed in one action branch",
            "proof_status": "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED",
            "missing_for_current_claim": "WEYL_DISFORMAL_SOURCE_PREFACTOR_READOUT_ENDPOINT_ROUTES_OPEN",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NSF1740_THM2_bound_fallback",
            "statement": "If no-shadow-frame zero is unsigned, b_g and related shadow coefficients become finite local residuals.",
            "mathematical_form": "epsilon_shadow_abs=|epsilon_bg_abs|+|b_disformal|+|delta w|+|b_readout|+|b_endpoint|",
            "proof_status": "FINITE_BOUND_MAP_REQUIRED_NONCLAIM",
            "missing_for_current_claim": "MISSING_NUMERIC_COEFFICIENTS;MISSING_ARENA_RESPONSE_MAPS;MISSING_R10_CURVE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    rows = []
    for projection in PROJECTIONS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **projection,
                "input_status": "MISSING_BG_OR_SHADOW_COEFFICIENTS",
                "bound_status": "R10_CURVE_PLACEHOLDER_OR_LOCAL_BOUND_SYMBOLIC" if projection["projection_id"] == "BMAP1740_4_R10" else "LOCAL_BOUND_AVAILABLE_RESPONSE_MAP_MISSING",
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def bg_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BBR1740_0_epsilon_shadow_abs",
            "quantity": "epsilon_shadow_abs",
            "definition": "absolute no-cancellation envelope for common Weyl/disformal/source-prefactor/readout/endpoint leakage",
            "formula": "|epsilon_bg_abs|+|b_disformal|+|delta w|+|b_readout|+|b_endpoint|",
            "units": "dimensionless_or_declared_response_norm_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "RETAINED_NONCLAIM_BOUND_INPUT",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BBR1740_1_R10_alpha_pred",
            "quantity": "alpha_pred(lambda)",
            "definition": "short-range Yukawa-style projection of shadow-frame residuals",
            "formula": "|K_R10(lambda) epsilon_shadow_abs|",
            "units": "dimensionless_alpha_MISSING",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "status": "RETAINED_NONCLAIM_R10_INPUT",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1740_0_bg_local_bound_runner",
            "runner": "b_g to local bound comparison",
            "required_inputs": "epsilon_shadow_abs;arena response maps;local bounds;source paths",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "b_g/shadow coefficients and arena response maps are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1740_1_R10_alpha_runner",
            "runner": "R10 alpha(lambda) comparison",
            "required_inputs": "alpha_pred(lambda);digitized alpha_bound(lambda);lambda map;material source/test legs",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "R10 bound curve is placeholder/nonclaim and alpha_pred is missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1740_0_exact_route",
            "decision": "NO_SHADOW_FRAME_ZERO_IS_AN_EXACT_CONTRACT",
            "reason": "a parent-owned matter/coframe action can forbid Weyl/disformal/source-prefactor/readout endpoint routes",
            "next_action": "continue deriving the parent matter/coframe action if possible",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1740_1_current_verdict",
            "decision": "NO_SHADOW_FRAME_ZERO_NOT_SIGNED",
            "reason": "current evidence keeps Weyl, disformal, source-prefactor, readout and endpoint countermodels open",
            "next_action": "retain finite shadow-frame residual rows",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1740_2_bound_map",
            "decision": "BOUND_PROJECTION_MAP_STAGED_NONCLAIM",
            "reason": "local bounds exist for WEP/PPN/clocks/Gdot, but response maps and R10 curve/alpha prediction are missing",
            "next_action": "fill first source-backed response map or acquire real R10 curve before scoring",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1740_3_best_next_domino",
            "decision": "TARGET_FIRST_BG_RESPONSE_MAP_OR_R10_CURVE",
            "reason": "after theorem route fails for claim, the fastest empirical discipline is one real response map and one real bound curve",
            "next_action": "build first source-backed b_g-to-PPN/WEP response row or replace placeholder R10 curve",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1740_0_no_shadow_zero",
            "claim": "all shadow-frame routes are theorem-zero",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1740_1_bg_projection_score",
            "claim": "b_g/shadow rows are score-ready",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_NUMERIC_COEFFICIENTS_AND_RESPONSE_MAPS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1740_2_R10_score",
            "claim": "R10 alpha(lambda) shadow-frame comparison is score-ready",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_DIGITIZED_R10_CURVE_AND_ALPHA_PREDICTION",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1740_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_NO_SHADOW_FRAME_ZERO_NO_EINSTEIN_REDUCTION",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1740_0_primary",
            "next_target": "1741-Y5-R2FR-first-bg-response-map-or-real-R10-bound-curve.md",
            "script": "scripts/Y5_R2FR_first_bg_response_map_or_real_R10_bound_curve.py",
            "objective": "source one concrete b_g response map for WEP/PPN/clock or replace the placeholder R10 alpha(lambda) curve before any scoring",
            "success_condition": "first source-backed nonclaim response-map row or real digitized R10 bound curve with schema checks",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1740_1_derivation_retry",
            "next_target": "1741b-Y5-R2FR-parent-matter-coframe-action-no-shadow-proof-retry.md",
            "script": "scripts/Y5_R2FR_parent_matter_coframe_action_no_shadow_proof_retry.py",
            "objective": "retry the exact parent action route for no-shadow-frame zero if a new action clause is found",
            "success_condition": "new parent action clause signs no Weyl/disformal/source-prefactor/readout route",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1740_2_later_tau",
            "next_target": "1742-Y5-R2FR-tau-pushforward-on-qvis-or-finite-Dtau-row.md",
            "script": "scripts/Y5_R2FR_tau_pushforward_on_qvis_or_finite_Dtau_row.py",
            "objective": "prove observed-time generator is pushforward of one parent tau on Q_vis",
            "success_condition": "tau pushforward theorem or finite Dtau row for commutator and PPN gates",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "no_shadow_clause_gate": no_shadow_clause_rows(),
        "zero_theorem_attempt": zero_theorem_rows(),
        "bg_projection_map": projection_rows(),
        "bg_bound_rows": bg_bound_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1740_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1740_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "gate_pass",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
        "zero_theorem_closed",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "gate_pass",
        "parent_signed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
        "zero_theorem_closed",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1740_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1740_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1740*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    clauses = rows_map["no_shadow_clause_gate"]
    theorem_rows = rows_map["zero_theorem_attempt"]
    projection = rows_map["bg_projection_map"]
    bound_rows = rows_map["bg_bound_rows"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1740_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1740_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1740_2_clauses_complete", {row["clause_id"] for row in clauses} == {row["clause_id"] for row in NO_SHADOW_CLAUSES}, "no-shadow-frame gate covers all required clauses", "no-shadow-frame gate missing clause"),
        check("VAL1740_3_zero_not_signed", all(row["zero_theorem_closed"] == "False" and row["claim_allowed"] == "False" for row in clauses), "no no-shadow-frame clause signs a claim zero", "a no-shadow-frame clause opened a claim"),
        check("VAL1740_4_exact_contract_recorded", any(row["theorem_id"] == "NSF1740_THM0_exact_contract" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "exact no-shadow-frame conditional contract is recorded", "exact no-shadow theorem row missing"),
        check("VAL1740_5_current_zero_blocked", any(row["theorem_id"] == "NSF1740_THM1_current_claim" and row["proof_status"] == "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED" for row in theorem_rows), "current no-shadow-frame claim is explicitly blocked", "current blocked theorem row missing"),
        check("VAL1740_6_projection_nonclaim", all(row["comparison_ready"] == "False" and row["claim_allowed"] == "False" for row in projection), "b_g projection rows are blocked nonclaim", "projection row opened comparison/claim"),
        check("VAL1740_7_bound_inputs_nonclaim", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in bound_rows), "bound input rows remain nonclaim and not score-ready", "bound input row became score-ready"),
        check("VAL1740_8_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse missing b_g/R10 inputs", "runner refusal missing or opened claim"),
        check("VAL1740_9_decision_next_domino", any(row["decision_id"] == "DEC1740_3_best_next_domino" and row["decision"] == "TARGET_FIRST_BG_RESPONSE_MAP_OR_R10_CURVE" for row in decision), "decision selects first b_g response map or real R10 curve", "decision ledger did not select response-map/R10 route"),
        check("VAL1740_10_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1740_11_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1740_12_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1740_13_next_selected", any(row["route_id"] == "NEXT1740_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects first b_g response map or real R10 bound curve", "next target missing selected primary route"),
        check("VAL1740_14_csv_parse", parsed_ok, "all generated 1740 CSVs parse", "one or more generated 1740 CSVs failed to parse"),
        check("VAL1740_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1740_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1740_17_formalization_untouched", formalization_untouched(), "no 1740 outputs found under formalization-workbench", "1740 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1740_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1740 no-shadow-frame zero or b_g bound projection map validation" if overall else "one or more 1740 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- The no-shadow-frame rule is exactly the right contract, but it is not yet parent-signed.",
        "- Weyl, disformal, source-prefactor, post-readout, and boundary-endpoint routes all remain live countermodels.",
        "- The finite fallback is now explicit: project `b_g`/shadow coefficients into WEP, PPN, clock/orbital, and R10 bounds.",
        "- Local bounds exist for several arenas, but response maps and a real R10 digitized curve are not yet score-ready.",
        "- No local-GR, Newton, WEP, PPN, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## No Shadow Frame Clause Gate",
        markdown_table(rows_map["no_shadow_clause_gate"], ["clause_id", "clause", "mathematical_test", "current_status", "blocker"]),
        "",
        "## Zero Theorem Attempt",
        markdown_table(rows_map["zero_theorem_attempt"], ["theorem_id", "statement", "mathematical_form", "proof_status", "missing_for_current_claim"]),
        "",
        "## b_g Bound Projection Map",
        markdown_table(rows_map["bg_projection_map"], ["projection_id", "arena", "observable", "mapping_formula", "input_status", "bound_status"]),
        "",
        "## Bound Input Rows",
        markdown_table(rows_map["bg_bound_rows"], ["row_id", "quantity", "formula", "value_or_formula", "status"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The local-GR route is still alive but has become a fork with teeth. Either the parent action bans shadow frames, or `b_g` is an empirical residual that has to fit the same WEP/PPN/clock/R10 ring as everyone else. That is exactly the discipline we wanted.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1740_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1740 validation FAIL")
    print("1740 validation PASS")


if __name__ == "__main__":
    main()
