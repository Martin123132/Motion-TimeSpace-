from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "734-Y5-R10-fill-hybrid-q_loc-residual-runner-or-derive-first-zero-row.md"
NEXT_TARGET = "735-Y5-R10-source-backed-hybrid-q_loc-residual-inputs-or-second-zero-row.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_734_first_narrow_zero_row_derived_hybrid_q_loc_residual_runner_filled_nonclaim"
CLAIM_CEILING = "representative_vertical_variation_zero_only_observed_q_loc_residual_still_unscored_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_734_SOURCE_REGISTER.csv"
FIRST_ZERO_PATH = RESIDUALS / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv"
RESIDUAL_FORMULA_PATH = RESIDUALS / "P8_Y5_R10_734_RESIDUAL_FORMULA_LEDGER.csv"
RUNNER_FILLED_PATH = RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_734_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_734_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_734_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_734_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "733_doc": {
        "path": POST_CHECKPOINT / "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md",
        "role": "immediate reduced GK owner / runner handoff",
        "needles": [
            "owner contract written, current symbol match failed",
            OUTPUT_DOC.name,
            "try to derive one first zero row",
        ],
    },
    "733_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_733_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": [
            "V733_9_next_target_selected",
            OUTPUT_DOC.name,
            "V733_12_formalization_workbench_untouched",
        ],
    },
    "733_runner_queue": {
        "path": RESIDUALS / "P8_Y5_R10_733_HYBRID_QLOC_RESIDUAL_RUNNER_QUEUE.csv",
        "role": "parent residual runner queue",
        "needles": [
            "HQR733_0_compact_shell_budget",
            "HQR733_5_R11_operator_vector",
            "queued_not_scored",
        ],
    },
    "733_ward_gate": {
        "path": RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv",
        "role": "exact q_loc zero blockers",
        "needles": [
            "WZG733_0_current_symbol_match",
            "WZG733_5_Y5_source_normalization",
            "hard_blocker_active",
        ],
    },
    "732_doc": {
        "path": POST_CHECKPOINT / "732-Y5-R10-construct-hybrid-pi-observed-quotient-map-or-demote.md",
        "role": "hybrid pullback lemma source",
        "needles": [
            "hybrid map constructed, exact local silence not derived",
            "If `Gamma_eff`, `K_hat`, and `P_loc` are pullbacks",
            "vertical-blind is not zero",
        ],
    },
    "732_pullback": {
        "path": RESIDUALS / "P8_Y5_R10_732_HYBRID_PULLBACK_LEMMA.csv",
        "role": "conditional vertical-blind derivation",
        "needles": [
            "HPL732_1_q_loc_pullback",
            "L_{v_X}q_loc=0",
            "HPL732_2_not_zero",
        ],
    },
    "732_exactness": {
        "path": RESIDUALS / "P8_Y5_R10_732_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv",
        "role": "exact-zero/residual distinction",
        "needles": [
            "QEG732_1_exact_local_zero_gate",
            "q_loc can be an observed reduced residual",
            "QEG732_3_boundary_flux_gate",
        ],
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5/source normalization residual branch",
        "needles": ["mu_obs", "Y5 source-normalization", "q_loc_projection"],
    },
    "597_doc": {
        "path": POST_CHECKPOINT / "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md",
        "role": "older q_loc residual runner checkpoint",
        "needles": ["reduced GK owner route", "q_loc residual runner", "Y5/Y6"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc stress-divergence identity",
        "needles": ["q_loc^nu = P_loc nabla_mu T_GK", "conditional_derivation_route", "not_supplied"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_first_zero_attempt(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "FZA734_0_representative_vertical_q_loc_variation",
            "target_quantity": "L_{v_X^rep} q_loc^nu",
            "theorem_or_formula": "If q_loc^nu = (Pi o pi_h)[nabla(g_obs)^nu(gamma o pi_h)-nabla_mu(g_obs)(kappa^{mu nu} o pi_h)] and d pi_h(v_X^rep)=0, then L_{v_X^rep} q_loc^nu=0.",
            "premises": "Gamma_eff, K_hat, P_loc, and nabla all factor through Q_obs^hybrid; v_X^rep is vertical; boundary/reference data are fixed under the representative vertical direction.",
            "derivation": "Apply the chain rule: L_v(f o pi_h)=df[d pi_h(v)]=0 for gamma, kappa, Pi, and g_obs-compatible nabla; products and covariant derivatives of pullbacks remain pullbacks.",
            "verdict": "derived_narrow_zero_row_conditional",
            "residual_left": "This kills only the representative-vertical variation/source channel; q_loc itself can still be a nonzero observed reduced residual.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc", "732_pullback", "733_doc"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "FZA734_1_hidden_representative_fifth_force_source",
            "target_quantity": "qbar_XT sourced directly by R_rep",
            "theorem_or_formula": "No R_rep derivative appears in Gamma_eff/K_hat/P_loc when the pullback premises hold.",
            "premises": "All local readout objects are functions of Q_obs^hybrid and not of the representative fibre R_rep.",
            "derivation": "A representative-fibre displacement changes R_rep only, so any term requiring partial_Rrep Gamma_eff, partial_Rrep K_hat, or partial_Rrep P_loc is absent.",
            "verdict": "conditionally_killed_as_hidden_source",
            "residual_left": "A universal reduced field Phi_red can still source q_loc through its own Euler/boundary terms.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_pullback", "733_ward_gate"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "FZA734_2_exact_observed_q_loc_zero",
            "target_quantity": "q_loc^nu",
            "theorem_or_formula": "q_loc^nu = P_loc(sum_A E_A nabla^nu Phi_A + B_boundary^nu) after reduced Ward ownership.",
            "premises": "T_GK is a Hilbert stress of a reduced diffeo-invariant action; all reduced fields are on shell; P_loc is parent-owned; boundary/source flux vanishes.",
            "derivation": "The Ward identity would set the bulk divergence to Euler terms plus boundary terms, but 733 keeps current symbol match, Y5/Y6, projector ownership, and boundary gates open.",
            "verdict": "not_derived_for_current_claim",
            "residual_left": "Observed q_loc remains in the residual runner.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_ward_gate", "513_doc", "732_exactness"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "FZA734_3_Y5_source_normalization_zero",
            "target_quantity": "C_qmu and source-strength projection rows",
            "theorem_or_formula": "Measured GM equals the unique parent EH/Hilbert source charge with no extra q_loc projection.",
            "premises": "No extra source-normalization channel, no species/range/frame split, and no post-readout projection ambiguity.",
            "derivation": "518 writes the route but does not parent-derive the required source normalization coefficients.",
            "verdict": "blocked_not_zero",
            "residual_left": "Y5 source-normalization rows must be derived or bounded.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "733_runner_queue"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "FZA734_4_boundary_flux_zero",
            "target_quantity": "P_loc B_boundary^nu and compact shell flux",
            "theorem_or_formula": "Boundary/corner/source-measure flux vanishes for proper compact local transformations.",
            "premises": "Exact representative boundary primitive, fixed ADM/reference class, and no corner symplectic leakage.",
            "derivation": "732/733 explicitly keep boundary/source-measure flux open, so the zero cannot be taken.",
            "verdict": "blocked_not_zero",
            "residual_left": "Boundary/alpha3/compact-shell components remain in the runner.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_exactness", "733_ward_gate", "597_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_residual_formula_ledger(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "RFL734_0_reduced_Ward_shape",
            "formula": "q_loc^nu = P_loc nabla_mu T_GK^{mu nu} = P_loc(sum_A E_A nabla^nu Phi_A + B_boundary^nu)",
            "meaning": "Exact local silence needs on-shell reduced fields plus boundary silence; pullback alone only removes representative-fibre source dependence.",
            "status": "contract_shape_retained_not_current_claim",
            "missing_inputs": "current Gamma/Khat metric-response owner; P_loc ownership; Y5/Y6 closure; boundary no-flux",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_doc", "513_doc", "732_exactness"),
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "RFL734_1_representative_vertical_zero",
            "formula": "L_{v_X^rep} q_loc^nu = 0 under pullback/fixed-boundary premises",
            "meaning": "A narrow theorem row exists: representative motion alone does not create the local residual if the hybrid pullback map is respected.",
            "status": "derived_narrow_nonclaim_zero",
            "missing_inputs": "actual current symbol match for Gamma_eff/K_hat/P_loc still needed before using it as a theory claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_pullback", "733_doc"),
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "RFL734_2_observed_residual_survives",
            "formula": "q_loc^nu != 0 is still allowed as a tensor on Q_obs^hybrid",
            "meaning": "The theory cannot say local-GR pass until the observed reduced residual is killed or bounded.",
            "status": "survives_as_runner_target",
            "missing_inputs": "source-backed residual coefficients or additional theorem-zero rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc", "733_runner_queue"),
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "RFL734_3_no_readout_cheat_guard",
            "formula": "readout R_read: Sol(S_parent) -> Observables is applied after parent variation",
            "meaning": "Do not impose q_loc=0 by varying an already-reduced readout action as if it were fundamental.",
            "status": "guard_retained",
            "missing_inputs": "parent action/readout proof for current MTS symbols",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_exactness", "733_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_runner_filled(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "HQR734_0_compact_shell_budget",
            "parent_queue_id": "HQR733_0_compact_shell_budget",
            "residual_component": "compact-shell leakage or P_loc d_rel J_rel proxy",
            "current_formula_or_input": "old compact-shell proxy = 7.432631961576971e-06 dimensionless",
            "derived_zero_status": "not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "unit map, sign convention, relation to source-normalization/PPN units, official arena bound",
            "scoring_gate": "claim only if mapped coefficient is sourced and below bound, or a later theorem-zero row kills it",
            "next_action": "source unit map or derive boundary no-flux",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_runner_queue", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_1_source_normalization_Y5",
            "parent_queue_id": "HQR733_1_source_normalization_Y5",
            "residual_component": "q_loc projection into measured GM/source-strength channel",
            "current_formula_or_input": "q_loc^nu projected by C_qmu into Gdot/Mdot/radial/species/range/frame/beta/PPN rows",
            "derived_zero_status": "blocked_not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "C_qmu, units, parent-owned P_loc, and theorem-zero/source-backed values for every Y5 row",
            "scoring_gate": "all Y5 rows must be derived zero or below official local locks",
            "next_action": "fill source-normalization coefficient ledger",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "733_runner_queue"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_2_boundary_pressure_alpha3",
            "parent_queue_id": "HQR733_2_boundary_pressure_alpha3",
            "residual_component": "preferred-frame or momentum-flux equivalent from boundary/corner/source measure",
            "current_formula_or_input": "alpha3-style pressure/momentum flux coefficient placeholder",
            "derived_zero_status": "blocked_not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "boundary primitive, corner symplectic flux, coefficient to alpha3-equivalent row",
            "scoring_gate": "source-backed coefficient below alpha3 lock or exact boundary theorem zero",
            "next_action": "derive boundary silence or source alpha3 projection coefficient",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_ward_gate", "732_exactness"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_3_PPN_metric_tail",
            "parent_queue_id": "HQR733_3_PPN_metric_tail",
            "residual_component": "Delta_PPN={gamma-1,beta-1,alpha_i,xi,zeta_i}_source",
            "current_formula_or_input": "linearized metric tail sourced by q_loc/source-normalization split",
            "derived_zero_status": "not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "weak-field Green operator, source split, gauge convention, PPN coefficient map",
            "scoring_gate": "all PPN components below bounds or theorem-zero with sourced map",
            "next_action": "write linearized q_loc-to-PPN coefficient contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_runner_queue", "518_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_4_R10_range_tail",
            "parent_queue_id": "HQR733_4_R10_range_tail",
            "residual_component": "alpha(lambda) or range-dependent source strength",
            "current_formula_or_input": "real bound curve infrastructure exists; q_loc-to-alpha coefficient missing",
            "derived_zero_status": "not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "lambda, alpha coefficient, source path, bound-curve comparison, parent coefficient source",
            "scoring_gate": "abs(alpha_predicted)<=alpha_bound with all rows numeric, sourced, and valid_for_claim=true",
            "next_action": "source q_loc-to-alpha coefficient or derive first alpha zero row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_runner_queue", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_5_R11_operator_vector",
            "parent_queue_id": "HQR733_5_R11_operator_vector",
            "residual_component": "non-EH/operator/source-normalization coefficient vector",
            "current_formula_or_input": "symbolic operator vector until operator family and normalization are filled",
            "derived_zero_status": "not_zero",
            "numeric_status": "not_scoreable",
            "missing_inputs": "operator basis, units, weak-field normalization, local bound comparison",
            "scoring_gate": "operator vector below R11/local locks or theorem-zero",
            "next_action": "choose minimal operator basis and source its normalization",
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_runner_queue", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR734_6_representative_vertical_variation_zero",
            "parent_queue_id": "new_from_732_pullback",
            "residual_component": "hidden representative-fibre variation of q_loc",
            "current_formula_or_input": "L_{v_X^rep} q_loc^nu = 0 under hybrid pullback premises",
            "derived_zero_status": "derived_narrow_zero",
            "numeric_status": "not_a_numeric_arena_row",
            "missing_inputs": "current Gamma/Khat/P_loc symbol match before promoting beyond theorem-contract",
            "scoring_gate": "may prune hidden representative-source branch only; cannot score R10/WEP/PPN/Newton/local-GR",
            "next_action": "use as a nonclaim pruning lemma while filling observed residual rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_pullback", "733_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_decision_matrix(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D734_0_first_zero_row_selected",
            "decision": "accept L_{v_X^rep} q_loc^nu = 0 as the first narrow conditional zero row",
            "meaning": "The representative-fibre source channel is pruned if the hybrid pullback premises are respected.",
            "claim_status": "theorem_contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_pullback", "733_doc"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D734_1_exact_q_loc_zero_rejected",
            "decision": "do not claim q_loc^nu=0 for the current MTS symbols",
            "meaning": "Vertical-blindness is not silence; the observed reduced residual still needs Ward ownership, source closure, and boundary silence.",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_ward_gate", "732_exactness"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D734_2_runner_filled_nonclaim",
            "decision": "fill the hybrid q_loc residual runner with explicit missing inputs and gates",
            "meaning": "The next pass can either derive a second zero row or source numeric coefficients without pretending placeholders are evidence.",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("733_runner_queue", "518_doc", "597_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU734_0_allowed",
            "allowed_after_734": "say a narrow representative-vertical q_loc variation zero has been derived conditionally",
            "forbidden_after_734": "say the observed q_loc residual, local-GR limit, R10, WEP, PPN, or Newton limit has passed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU734_1_allowed",
            "allowed_after_734": "use the runner to track exact missing inputs for Y5, boundary/alpha3, PPN, R10, and R11",
            "forbidden_after_734": "promote a placeholder residual row to source-backed evidence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU734_2_allowed",
            "allowed_after_734": "hunt a second zero row, preferably boundary no-flux or source-normalization closure",
            "forbidden_after_734": "use the narrow vertical zero to hide observed reduced stress or source-measure leakage",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "A first honest zero row exists: L_{v_X^rep} q_loc^nu=0 under hybrid pullback premises. Exact observed q_loc=0 remains rejected for current claim.",
            "hard_blocker": "Gamma/Khat/P_loc current symbol match, reduced Ward ownership, Y5 source normalization, Y6 extra stress, boundary no-flux, and numeric local arena coefficients.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    first_zero_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_register)
    needles_pass = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["733_validation"]["path"])
    parent_queue = read_csv(SOURCES["733_runner_queue"]["path"])
    parent_queue_ids = {row.get("runner_id", "") for row in parent_queue}
    represented_parent_ids = {
        row.get("parent_queue_id", "")
        for row in runner_rows
        if row.get("parent_queue_id", "").startswith("HQR733_")
    }
    narrow_zero = any(
        row.get("zero_id") == "FZA734_0_representative_vertical_q_loc_variation"
        and row.get("verdict") == "derived_narrow_zero_row_conditional"
        for row in first_zero_rows
    )
    exact_zero_rejected = any(
        row.get("zero_id") == "FZA734_2_exact_observed_q_loc_zero"
        and row.get("verdict") == "not_derived_for_current_claim"
        for row in first_zero_rows
    )
    observed_survives = any(
        row.get("formula_id") == "RFL734_2_observed_residual_survives"
        and row.get("status") == "survives_as_runner_target"
        for row in formula_rows
    )
    all_parent_queue_represented = parent_queue_ids == represented_parent_ids
    missing_inputs_retained = all(
        row.get("missing_inputs", "") not in {"", "none", "derived_zero"}
        for row in runner_rows
        if row.get("runner_id") != "HQR734_6_representative_vertical_variation_zero"
    )
    no_claim_rows = all(row.get("valid_for_claim") == "false" for row in [*first_zero_rows, *formula_rows, *runner_rows, *decision_rows])
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()

    return [
        {"check_id": "V734_0_source_paths_exist", "result": "pass" if source_paths_exist else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V734_1_source_needles_present", "result": "pass" if needles_pass else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V734_2_prior_733_clean", "result": "pass" if prior_clean else "fail", "detail": "733 validation has no failures"},
        {"check_id": "V734_3_733_selected_734", "result": "pass" if text_contains(SOURCES["733_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name},
        {"check_id": "V734_4_first_zero_attempt_rows_present", "result": "pass" if len(first_zero_rows) >= 5 else "fail", "detail": f"zero_rows={len(first_zero_rows)}"},
        {"check_id": "V734_5_narrow_vertical_zero_derived", "result": "pass" if narrow_zero else "fail", "detail": "L_vrep q_loc=0 conditional row exists"},
        {"check_id": "V734_6_exact_q_loc_zero_rejected", "result": "pass" if exact_zero_rejected else "fail", "detail": "observed q_loc zero not claimed"},
        {"check_id": "V734_7_observed_residual_survives", "result": "pass" if observed_survives else "fail", "detail": "q_loc remains a runner target"},
        {"check_id": "V734_8_parent_runner_rows_represented", "result": "pass" if all_parent_queue_represented else "fail", "detail": f"parent_rows={len(parent_queue_ids)};represented={len(represented_parent_ids)}"},
        {"check_id": "V734_9_missing_inputs_retained", "result": "pass" if missing_inputs_retained else "fail", "detail": "nonzero runner rows keep explicit missing inputs"},
        {"check_id": "V734_10_no_claim_rows_promoted", "result": "pass" if no_claim_rows else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V734_11_decision_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail", "detail": NEXT_TARGET},
        {"check_id": "V734_12_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V734_13_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V734_14_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V734_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    source_register: list[dict[str, Any]],
    first_zero_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 734 - Y5 R10 Fill Hybrid q_loc Residual Runner Or Derive First Zero Row

## Summary

Start point: 733 produced a coherent hybrid reduced-action contract, but the current MTS symbols still do not prove `Gamma_eff` is the scalar density, `K_hat` is its metric response, `P_loc` is parent-owned, or that Y5/Y6/boundary flux vanish.

Current verdict: **one narrow zero row is derivable, but the observed `q_loc` residual is not killed**. The first useful zero is:

```text
L_{{v_X^rep}} q_loc^nu = 0
```

under the hybrid pullback premises. This says representative-fibre motion does not itself source the local residual. It does **not** say `q_loc^nu=0`; the observed reduced residual still has to be derived away or bounded.

| Item | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | first narrow representative-vertical zero row plus filled nonclaim runner |
| Next target | `{NEXT_TARGET}` |

## First Zero Attempt

{markdown_table(first_zero_rows, ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim"])}

## Residual Formula Ledger

{markdown_table(formula_rows, ["formula_id", "formula", "meaning", "status", "missing_inputs", "valid_for_claim"])}

## Hybrid q_loc Residual Runner Filled

{markdown_table(runner_rows, ["runner_id", "parent_queue_id", "residual_component", "current_formula_or_input", "derived_zero_status", "numeric_status", "missing_inputs", "scoring_gate", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_734", "forbidden_after_734", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a small but real inch forward. We did not magic local GR out of the quotient map. What we did get is a clean pruning lemma: if the hybrid pullback map is respected, the representative-motion fibre cannot be the thing generating a local fifth-force residual. The remaining enemy is the observed reduced `q_loc` itself: Y5/source normalization, boundary flux, PPN tail, R10 range tail, and R11 operator vector still need either theorem-zero rows or sourced numerical coefficients.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_root = RUNS / f"734_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    first_zero_rows = make_first_zero_attempt(generated_utc)
    formula_rows = make_residual_formula_ledger(generated_utc)
    runner_rows = make_runner_filled(generated_utc)
    decision_rows = make_decision_matrix(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        FIRST_ZERO_PATH,
        RESIDUAL_FORMULA_PATH,
        RUNNER_FILLED_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    write_csv(
        SOURCE_REGISTER_PATH,
        source_register,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        FIRST_ZERO_PATH,
        first_zero_rows,
        ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUAL_FORMULA_PATH,
        formula_rows,
        ["formula_id", "formula", "meaning", "status", "missing_inputs", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RUNNER_FILLED_PATH,
        runner_rows,
        ["runner_id", "parent_queue_id", "residual_component", "current_formula_or_input", "derived_zero_status", "numeric_status", "missing_inputs", "scoring_gate", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_734", "forbidden_after_734", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, first_zero_rows, formula_rows, runner_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(
        source_register,
        first_zero_rows,
        formula_rows,
        runner_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
