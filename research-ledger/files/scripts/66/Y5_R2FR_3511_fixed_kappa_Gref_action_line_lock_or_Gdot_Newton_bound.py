from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3511-Y5-R2FR-fixed-kappa-Gref-action-line-lock-or-Gdot-Newton-bound.md"
CANONICAL_KAPPA_LOCK = OUT / "P8_EM_fixed_kappa_Gref_action_line_lock.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3511": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3510": {
        "path": ROOT / "3510-Y5-R2FR-common-action-density-line-owner-or-universal-source-scale-bound.md",
        "role": "3510 common-scale handoff",
    },
    "residual_3510": {
        "path": OUT / "P8_EM_common_action_density_line_universal_source_scale.csv",
        "role": "3510 universal common-scale residual",
    },
    "theorem_3510": {
        "path": OUT / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv",
        "role": "3510 action-line theorem stack",
    },
    "gref_3500": {
        "path": OUT / "P8_Y5_R2FR_3500_CONSTANT_GREF_SIGNATURE.csv",
        "role": "constant G_ref signature",
    },
    "kappa_theorem_2723": {
        "path": OUT / "P8_Y5_R2FR_2723_KAPPA_GREF_THEOREM_ATTEMPT.csv",
        "role": "kappa/Gref theorem attempt",
    },
    "kappa_audit_2723": {
        "path": OUT / "P8_Y5_R2FR_2723_KAPPA_GREF_OWNERSHIP_AUDIT.csv",
        "role": "kappa/Gref ownership audit",
    },
    "kappa_lock_702": {
        "path": OUT / "P8_Y5_R10_702_KAPPA_GREF_LOCK_AUDIT.csv",
        "role": "kappa/Gref lock audit",
    },
    "constant_kappa_theorem": {
        "path": OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
        "role": "constant kappa superselection theorem",
    },
    "topological_kappa_clause": {
        "path": OUT / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
        "role": "topological kappa zero-form/three-form clause",
    },
    "universal_kappa_contract": {
        "path": OUT / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "constant universal Geff/kappa contract",
    },
    "topological_kappa_3047": {
        "path": OUT / "P8_Y5_R2FR_3047_TOPOLOGICAL_KAPPA_SIGNATURE_ATTEMPT.csv",
        "role": "topological kappa signature attempt",
    },
    "gref_kappa_residual_3377": {
        "path": OUT / "P8_Y5_R2FR_3377_GREF_KAPPA_RESIDUAL_ROWS_NONCLAIM.csv",
        "role": "Gref/kappa residual rows",
    },
    "gdot_gate_2933": {
        "path": OUT / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv",
        "role": "dotG/kappa projection gate",
    },
    "gdot_projection_2934": {
        "path": OUT / "P8_Y5_R2FR_2934_DOTG_TO_KAPPA_PROJECTION_THEOREM_ATTEMPT.csv",
        "role": "dotG to kappa projection attempt",
    },
    "newton_chain_3382": {
        "path": OUT / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "role": "Newton source normalization chain",
    },
    "clock_bound_1052": {
        "path": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock alpha product bound ledger",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def lock_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "KGL3511_0_Gref_type_silence",
            "claim_piece": "G_ref/kappa as parent constant",
            "statement": "If G_ref or kappa_eff is a parent-action coupling/superselection label rather than a local readout field, local derivative channels do not act on it.",
            "mathematical_form": "G_ref=kappa_eff c^4/(8*pi); D_X ln kappa_eff=0 for X={t,r,lambda,frame,domain,species} if kappa_eff in K_global",
            "derivation": "A local variation acts on dynamic fields, not on a fixed branch label or superselected coupling sector.",
            "payoff": "kills kappa-side Gdot/radial/range/species drift if parent-signed",
            "gap": "parent action must explicitly own the coupling before readout",
            "status": "CONDITIONAL_ZERO_ROUTE_FOR_KAPPA_ONLY",
            "source_path": str(SOURCES["gref_3500"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_1_topological_kappa_route",
            "claim_piece": "derive d kappa = 0 by topological sector",
            "statement": "A metric-independent zero-form/three-form sector can derive local constancy of kappa_eff on connected domains.",
            "mathematical_form": "S_kappa_top=int kappa_eff dA_3; delta_A3 S=-int d kappa_eff wedge delta A_3 => d kappa_eff=0",
            "derivation": "Variation of the three-form enforces the zero-gradient equation if boundary variations are fixed/topological and the sector carries no local stress.",
            "payoff": "upgrades kappa constancy from assumption to derivable parent option",
            "gap": "the topological sector is a candidate, not adopted as the active MTS parent signature; companion equation/stress silence remain open",
            "status": "DERIVATION_ROUTE_CONSTRUCTED_NOT_ADOPTED",
            "source_path": str(SOURCES["topological_kappa_3047"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_2_product_lock_identity",
            "claim_piece": "local tests see product G_ref w_common",
            "statement": "Even if kappa is fixed, local Newton/Gdot/source tests see the product of the EH coupling and common matter-source scale.",
            "mathematical_form": "D_X ln G_eff = D_X ln G_ref + D_X ln w_common + D_X ln ell_J + D_X ln R_frame + retained source terms",
            "derivation": "The weak-field source coefficient is set by the EH coefficient times the source-current/action normalization entering T_H.",
            "payoff": "prevents a false local-GR claim from kappa constancy alone",
            "gap": "w_common/action line, ell_J/source-current and frame/reference locks are not all signed",
            "status": "EXACT_BOOKKEEPING_IDENTITY",
            "source_path": str(SOURCES["gdot_projection_2934"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_3_no_GM_backfill",
            "claim_piece": "anti-circular Newton coefficient",
            "statement": "Measured orbital GM may calibrate an already-fixed branch, but it cannot define G_ref, kappa_eff, w_common, ell_J or M_H for the theorem.",
            "mathematical_form": "mu_obs = G_ref w_common M_H (1+epsilon_mu); epsilon_mu must be zero/bounded before Newton recovery is claimed",
            "derivation": "Using the observed orbital product to choose the coupling would hide the exact residual that local GR/Newton recovery is supposed to derive.",
            "payoff": "keeps Newton reduction from becoming an amplitude fit",
            "gap": "M_H flux/projector and epsilon_mu remain separate gates",
            "status": "ANTI_CIRCULAR_GUARD_EXACT",
            "source_path": str(SOURCES["kappa_theorem_2723"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_4_finite_Gdot_bound_interface",
            "claim_piece": "first finite bound interface",
            "statement": "If the product lock is not derived, the common-scale/kappa residual must be scored against finite Gdot/Newton/clock bounds rather than claimed zero.",
            "mathematical_form": "|D_t ln G_eff| = |D_t ln(G_ref w_common ell_J R_frame ...)| <= bound_Gdot",
            "derivation": "A finite solar-system comparator exists, but the MTS projection into kappa/w_common/source-current pieces is not fully derived.",
            "payoff": "turns symbolic coupling drift into a numeric-ready non-claim row",
            "gap": "prediction side still missing D_t ln components and arena-transfer proof",
            "status": "BOUND_INTERFACE_READY_NOT_SCORE_READY",
            "source_path": str(SOURCES["gdot_gate_2933"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_5_Newton_coefficient_payoff",
            "claim_piece": "Newton coefficient without fit",
            "statement": "If kappa/G_ref, w_common, ell_J and the Hilbert mass projector are fixed before readout, the Poisson coefficient follows algebraically.",
            "mathematical_form": "nabla^2 Phi_N = 4*pi G_ref rho_H with rho_H from the same T_H/M_H branch",
            "derivation": "Linearized EH gives the left-hand coefficient; common source-current/action normalization supplies the same right-hand source object.",
            "payoff": "local Newton recovery becomes a conditional derivation instead of a fitted GM match",
            "gap": "extra-sector stress and boundary/reference locks remain retained",
            "status": "EXACT_CONDITIONAL_PAYOFF",
            "source_path": str(SOURCES["newton_chain_3382"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "KGL3511_6_verdict",
            "claim_piece": "3511 status",
            "statement": "The best route is not to derive the decimal value of G; it is to derive one fixed parent coupling product used by EH, matter source, Hamiltonian charge, Newton and clocks.",
            "mathematical_form": "D_X ln(G_ref w_common ell_J R_frame)=0 is the local-GR/Newton coupling gate",
            "derivation": "Combine constant-kappa route, topological option, common-action-line identity and dotG projection guard.",
            "payoff": "coupling frontier is now a product-lock theorem with numeric fallback",
            "gap": "no live claim until product-lock or bound rows are sourced on the prediction side",
            "status": "PRODUCT_LOCK_CONSTRUCTED_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["universal_kappa_contract"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "KGLR3511_0_delta_kappa",
            "residual": "delta_kappa",
            "definition": "D_X ln kappa_eff or mismatch kappa_eff/kappa_ref",
            "3511_result": "conditional zero if superselection/topological kappa sector is parent-adopted",
            "zero_condition": "kappa_eff in global/topological parent sector and no source/frame/range labels",
            "maps_to": "Gdot/radial/range/source coupling drift if unsigned",
            "observable_links": "Gdot; R10; PPN; Newton",
            "claim_allowed": "False",
        },
        {
            "row_id": "KGLR3511_1_zeta_w_common",
            "residual": "zeta_w_common",
            "definition": "D_X ln w_common",
            "3511_result": "not killed by kappa constancy; requires action-line/hbar/measure owner",
            "zero_condition": "fixed common ordinary-matter action-density line",
            "maps_to": "universal source/G calibration drift",
            "observable_links": "Gdot; Newton_GM; clocks",
            "claim_allowed": "False",
        },
        {
            "row_id": "KGLR3511_2_delta_ellJ",
            "residual": "delta_ellJ",
            "definition": "D_X ln source-current/Hilbert charge normalization",
            "3511_result": "retained product-lock component",
            "zero_condition": "source current extracted from same Hilbert action before readout",
            "maps_to": "Newton source normalization and WEP/source drift",
            "observable_links": "Newton; WEP; PPN; orbital_GM",
            "claim_allowed": "False",
        },
        {
            "row_id": "KGLR3511_3_R_frame",
            "residual": "R_frame",
            "definition": "frame/reference/readout normalization factor",
            "3511_result": "retained unless same observed frame/source/clock branch is signed",
            "zero_condition": "same-frame EH/source/clock/readout lock",
            "maps_to": "frame calibration split and clock/source drift",
            "observable_links": "clock; PPN; orbital_GM",
            "claim_allowed": "False",
        },
        {
            "row_id": "KGLR3511_4_Geff_product",
            "residual": "Geff_product",
            "definition": "D_X ln(G_ref w_common ell_J R_frame)",
            "3511_result": "the actual local coupling product gate",
            "zero_condition": "all product factors constant by one parent identity or independently zero without tuning",
            "maps_to": "Gdot/G and Newton coefficient residual",
            "observable_links": "Gdot; Newton; PPN; clocks",
            "claim_allowed": "False",
        },
        {
            "row_id": "KGLR3511_5_epsilon_Gref_match",
            "residual": "epsilon_Gref_match",
            "definition": "mismatch between EH, Hamiltonian, Poisson and PPN coupling normalizations",
            "3511_result": "anti-backfill guard retained",
            "zero_condition": "G_ref fixed before readout and used by all comparison maps",
            "maps_to": "Poisson/Newton amplitude mismatch",
            "observable_links": "Newton; PPN; local_GR",
            "claim_allowed": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "KGBIN3511_0_Gdot_product",
            "arena": "Gdot/time drift",
            "residual": "Geff_product",
            "predicted_value": "MISSING_DTLN_GREF_WCOMMON_ELLJ_RFRAME",
            "predicted_units": "yr^-1",
            "bound_value": "4.0e-14",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["gdot_gate_2933"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "KGBIN3511_1_delta_kappa",
            "arena": "kappa/Gref lock",
            "residual": "delta_kappa",
            "predicted_value": "MISSING_DLN_KAPPA_OR_MISMATCH",
            "predicted_units": "dimensionless_or_derivative",
            "bound_value": "MISSING_KAPPA_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["gref_kappa_residual_3377"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "KGBIN3511_2_delta_ellJ",
            "arena": "source-current normalization",
            "residual": "delta_ellJ",
            "predicted_value": "MISSING_DLN_ELLJ",
            "predicted_units": "dimensionless_or_derivative",
            "bound_value": "MISSING_ELLJ_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["gref_kappa_residual_3377"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "KGBIN3511_3_epsilon_Gref_match",
            "arena": "Newton/PPN coefficient match",
            "residual": "epsilon_Gref_match",
            "predicted_value": "MISSING_EPSILON_GREF_MATCH",
            "predicted_units": "dimensionless",
            "bound_value": "MISSING_NEWTON_PPN_MATCH_BOUND",
            "bound_units": "dimensionless",
            "source_path": str(SOURCES["gref_kappa_residual_3377"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "KGBIN3511_4_clock_product",
            "arena": "clock/action product",
            "residual": "R_frame_or_w_common_clock",
            "predicted_value": "MISSING_CLOCK_PRODUCT_PROJECTION",
            "predicted_units": "yr^-1",
            "bound_value": "3.2e-18",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["clock_bound_1052"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_bound_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        predicted = parse_float(str(row["predicted_value"]))
        bound = parse_float(str(row["bound_value"]))
        if row["valid_for_claim"] != "True":
            verdict = "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
            passes = "False"
        elif predicted is None or bound is None or bound <= 0:
            verdict = "BLOCKED_MISSING_NUMERIC_PREDICTION_OR_BOUND"
            passes = "False"
        else:
            passes = bool_text(abs(predicted) <= bound)
            verdict = "PASS_NUMERIC_KAPPA_LOCK_BOUND" if passes == "True" else "FAIL_NUMERIC_KAPPA_LOCK_BOUND"
        results.append(
            {
                "row_id": row["row_id"].replace("KGBIN", "KGRUN"),
                "arena": row["arena"],
                "residual": row["residual"],
                "predicted_value": row["predicted_value"],
                "bound_value": row["bound_value"],
                "pass_condition": "abs(predicted_value) <= bound_value with sourced numeric rows",
                "runner_verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return results


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3511_0_kappa_not_enough",
            "decision": "A constant/topological kappa route is useful but not sufficient for local GR/Newton.",
            "rationale": "Local tests see the product G_ref*w_common*ell_J*R_frame, not kappa alone.",
            "effect": "Future work should prove product-lock or fill product-bound rows, not celebrate kappa constancy in isolation.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3511_1_topological_route_kept",
            "decision": "Keep the zero-form/three-form kappa route as a serious candidate parent mechanism.",
            "rationale": "It can genuinely derive d kappa=0 if adopted with boundary and stress silence, unlike a pure convention.",
            "effect": "It remains a derivation route, but not a current claim.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3511_2_best_next_target",
            "decision": "Attack the product-lock factors as one vector.",
            "rationale": "The clean local-GR coupling gate is D_X ln(G_ref*w_common*ell_J*R_frame)=0.",
            "effect": "Next step should either derive ell_J/R_frame/action-line locks or make the Gdot/Newton bound runner prediction-side executable.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3512-Y5-R2FR-product-lock-factor-vector-ellJ-Rframe-or-Gdot-runner.md",
            "next_script": "scripts/Y5_R2FR_3512_product_lock_factor_vector_ellJ_Rframe_or_Gdot_runner.py",
            "objective": "Derive or bound the full product-lock vector D_X ln(G_ref*w_common*ell_J*R_frame), focusing on ell_J source-current normalization and same-frame/reference readout.",
            "success_gate": "Either ell_J and R_frame are parent-signed constants, reducing Gdot/Newton residuals to already-owned kappa/action-line factors, or the product vector has executable non-claim prediction rows.",
            "forbidden_shortcuts": "Do not use kappa constancy alone as local-GR coupling closure; do not absorb frame/source drift into measured GM.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_ids = {row["theorem_id"] for row in theorem_rows}
    residual_names = {row["residual"] for row in residuals}
    all_claim_false = all(
        row.get("valid_for_claim") == "False"
        for table in [sources, theorem_rows, bound_inputs, runner_results, decisions, next_rows]
        for row in table
    ) and all(row.get("claim_allowed") == "False" for row in residuals)
    all_blocked = all("BLOCKED" in row["runner_verdict"] for row in runner_results)
    finite_bounds_present = any(row["row_id"] == "KGBIN3511_0_Gdot_product" and parse_float(str(row["bound_value"])) for row in bound_inputs)
    validation = [
        {
            "check_id": "VAL3511_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_1_lock_theorems_present",
            "passed": bool_text({"KGL3511_0_Gref_type_silence", "KGL3511_1_topological_kappa_route", "KGL3511_2_product_lock_identity"}.issubset(theorem_ids)),
            "detail": "Gref, topological kappa, and product-lock identities written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_2_product_residuals_present",
            "passed": bool_text({"delta_kappa", "zeta_w_common", "delta_ellJ", "R_frame", "Geff_product", "epsilon_Gref_match"}.issubset(residual_names)),
            "detail": "product-lock residual vector complete",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_3_finite_bound_interface",
            "passed": bool_text(finite_bounds_present),
            "detail": "finite Gdot bound row carried as non-claim interface",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_4_bound_runner_blocks_placeholders",
            "passed": bool_text(all_blocked),
            "detail": "all kappa/product bound rows remain blocked until prediction inputs are valid",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_5_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3511 output row is valid_for_claim=True or claim_allowed=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_6_next_target_product_vector",
            "passed": bool_text(next_rows[0]["next_doc"].startswith("3512") and "product-lock" in next_rows[0]["objective"]),
            "detail": "product-lock factor vector selected next",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3511_7_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3511_SUMMARY",
            "passed": bool_text(all(row["passed"] == "True" for row in validation)),
            "detail": "PASS" if all(row["passed"] == "True" for row in validation) else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    theorem_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3511 - Fixed kappa/Gref Action-Line Lock Or Gdot/Newton Bound",
                "",
                "## Summary",
                "- **Derived gain:** `G_ref`/`kappa_eff` can be locally silent if owned as a parent constant, superselection label, or topological zero-form/three-form integration constant.",
                "- **Hard correction:** kappa constancy alone is not local-GR closure; tests see the product `G_ref*w_common*ell_J*R_frame` plus retained source terms.",
                "- **Finite bound path:** a sourced `Gdot` comparator is carried forward, but prediction rows remain blocked until the product factors are derived or filled.",
                "- **Next best move:** build the full product-lock vector, especially `ell_J` and same-frame/reference `R_frame`.",
                "",
                "## Kappa/Gref Lock Theorem Stack",
                markdown_table(
                    theorem_rows,
                    ["theorem_id", "claim_piece", "statement", "mathematical_form", "payoff", "gap", "status"],
                ),
                "",
                "## Product-Lock Residual Vector",
                markdown_table(
                    residuals,
                    ["row_id", "residual", "definition", "3511_result", "zero_condition", "maps_to", "claim_allowed"],
                ),
                "",
                "## Bound Input Template",
                markdown_table(
                    bound_inputs,
                    ["row_id", "arena", "residual", "predicted_value", "bound_value", "source_path", "valid_for_claim"],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runner_results,
                    ["row_id", "arena", "residual", "pass_condition", "runner_verdict", "passes_bound", "claim_allowed"],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"],
                ),
                "",
                "## Validation",
                markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {now_utc()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    theorem_rows = lock_theorem_rows()
    residuals = residual_rows()
    bound_inputs = bound_input_rows()
    runner_results = run_bound_rows(bound_inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, theorem_rows, residuals, bound_inputs, runner_results, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3511_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv",
        theorem_rows,
        ["theorem_id", "claim_piece", "statement", "mathematical_form", "derivation", "payoff", "gap", "status", "source_path", "valid_for_claim"],
    )
    residual_fields = [
        "row_id",
        "residual",
        "definition",
        "3511_result",
        "zero_condition",
        "maps_to",
        "observable_links",
        "claim_allowed",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3511_PRODUCT_LOCK_RESIDUAL_VECTOR.csv", residuals, residual_fields)
    write_csv(CANONICAL_KAPPA_LOCK, residuals, residual_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_BOUND_INPUT_TEMPLATE.csv",
        bound_inputs,
        ["row_id", "arena", "residual", "predicted_value", "predicted_units", "bound_value", "bound_units", "source_path", "valid_for_claim"],
    )
    runner_fields = [
        "row_id",
        "arena",
        "residual",
        "predicted_value",
        "bound_value",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_BOUND_RUNNER_RESULTS.csv", runner_results, runner_fields)
    write_csv(OUT / "P8_EM_kappa_Gref_product_bound_runner_results.csv", runner_results, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3511_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3511_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3511_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(theorem_rows, residuals, bound_inputs, runner_results, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
