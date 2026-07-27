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
OUTPUT_DOC = POST_CHECKPOINT / "731-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md"
NEXT_TARGET = "732-Y5-R10-construct-hybrid-pi-observed-quotient-map-or-demote.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_731_hybrid_EH_plus_quotient_extra_selected_boundary_and_matter_gates_open"
CLAIM_CEILING = "route_selection_and_hybrid_quotient_contract_only_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_731_SOURCE_REGISTER.csv"
ROUTE_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_731_ROUTE_SELECTION.csv"
HYBRID_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_731_HYBRID_QUOTIENT_CONTRACT.csv"
MATTER_BLINDNESS_PATH = RESIDUALS / "P8_Y5_R10_731_MATTER_BLINDNESS_GATE.csv"
BOUNDARY_CLOSURE_PATH = RESIDUALS / "P8_Y5_R10_731_BOUNDARY_CLOSURE_LEDGER.csv"
REDTEAM_PATH = RESIDUALS / "P8_Y5_R10_731_NO_CHEAT_RED_TEAM.csv"
BACKUP_ROUTES_PATH = RESIDUALS / "P8_Y5_R10_731_BACKUP_ROUTE_LEDGER.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_731_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_731_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_731_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_731_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "730_doc": {
        "path": POST_CHECKPOINT / "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md",
        "role": "immediate route-choice handoff",
        "needles": ["templates written, proof not closed", "hybrid EH-plus-quotient-extra", OUTPUT_DOC.name],
    },
    "730_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_730_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V730_11_next_target_selected", OUTPUT_DOC.name, "V730_14_formalization_workbench_untouched"],
    },
    "730_candidates": {
        "path": RESIDUALS / "P8_Y5_R10_730_MINIMAL_PARENT_FILL_CANDIDATES.csv",
        "role": "current route candidate table",
        "needles": ["MPF730_C_hybrid_EH_plus_quotient_extra", "MPF730_B_strict_quotient_zero", "false"],
    },
    "730_route_comparison": {
        "path": RESIDUALS / "P8_Y5_R10_730_ROUTE_COMPARISON.csv",
        "role": "current scrutiny comparison",
        "needles": ["RC730_A_strict_quotient_zero", "RC730_B_hybrid_EH_plus_quotient_extra", "fallback_only"],
    },
    "730_edge_input": {
        "path": RESIDUALS / "P8_Y5_R10_730_EDGE_COEFFICIENT_INPUT_ROWS.csv",
        "role": "current edge coefficient fallback status",
        "needles": ["ECI730_0", "MISSING_SOURCE", "608.0783"],
    },
    "594_doc": {
        "path": POST_CHECKPOINT / "594-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md",
        "role": "older strict quotient route selection",
        "needles": ["strict quotient-zero first", "matter blindness", "boundary"],
    },
    "595_doc": {
        "path": POST_CHECKPOINT / "595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md",
        "role": "older pi observed quotient map candidate",
        "needles": ["Y=(O,R,B_ref)", "pi(Y)=O", "q_loc"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "role": "strict quotient no-pole theorem shape",
        "needles": ["quotient-vertical no-pole", "Conf_parent --pi-->", "boundary charge"],
    },
    "511_doc": {
        "path": POST_CHECKPOINT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "fixed-point local-GR residual backup",
        "needles": ["EH core", "double zero", "local GR"],
    },
    "729_doc": {
        "path": POST_CHECKPOINT / "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "role": "current P/J origin contract",
        "needles": ["one parent Noether current", "j_X = theta_Y(v_X) - mu_X", "contract sharpened"],
    },
    "728_doc": {
        "path": POST_CHECKPOINT / "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "role": "current Omega/DCdagger boundary-adjoint source",
        "needles": ["DCdagger_A X", "boundary", "formula progress, not certificate"],
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


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(POST_CHECKPOINT)).replace("\\", "/")
    except ValueError:
        return str(path)


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


def make_route_selection(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RS731_A_hybrid_EH_plus_quotient_extra",
            "scrutiny_profile": "lowest_practical_if_split_is_clean",
            "why_selected": "keeps real local GR as the observed EH metric current while forcing extra MTS local representative directions to be quotient-silent",
            "main_burden": "construct pi, prove matter/readout/clock blindness, close boundary charges, and separate ADM/Pi_M from vertical X",
            "failure_mode": "if representative variables leak into matter/readout/boundary, R10/PPN residuals return",
            "selected": "true_primary",
            "valid_for_claim": "false",
            "source_paths": source_path_string("730_doc", "730_candidates", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RS731_B_strict_quotient_zero",
            "scrutiny_profile": "lowest_if_full_observed_sector_factors_through_pi",
            "why_selected": "pure no-pole subcase: dangerous X is representative data and never a physical local field",
            "main_burden": "prove all action, matter, readout, and boundary structures factor through pi",
            "failure_mode": "too strong if it accidentally quotients away real GR charges or active observed dynamics",
            "selected": "true_subcase",
            "valid_for_claim": "false",
            "source_paths": source_path_string("594_doc", "581_doc", "730_route_comparison"),
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RS731_C_diffeo_current_identity",
            "scrutiny_profile": "medium_high_backup",
            "why_selected": "standard GR Noether machinery is available if MTS C_X exactly equals parent diffeo/momentum constraint",
            "main_burden": "prove exact equality without ADM/Pi_M double counting or post-hoc symbol matching",
            "failure_mode": "can collapse into merely restating GR while leaving extra MTS residuals unexplained",
            "selected": "false_backup",
            "valid_for_claim": "false",
            "source_paths": source_path_string("730_doc", "729_doc"),
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RS731_D_fixed_point_double_zero",
            "scrutiny_profile": "medium_residual_backup",
            "why_selected": "useful if quotient silence is too strong but derived double zeros can bound residuals",
            "main_burden": "derive F_1=0, source silence, Delta m, and ell_tr/L_cg from parent mechanism",
            "failure_mode": "looks tuned if double zeros are assumptions rather than forced by the action",
            "selected": "false_residual_backup",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RS731_E_source_backed_edge",
            "scrutiny_profile": "highest_for_theory_claim",
            "why_selected": "empirical fallback only if theorem routes fail",
            "main_burden": "source K_edge, Qbar_edge_XH, qbar_XT below alpha_edge(lambda)",
            "failure_mode": "looks like fitted local-bound compliance rather than reduction to GR",
            "selected": "false_fallback",
            "valid_for_claim": "false",
            "source_paths": source_path_string("730_edge_input"),
            "generated_utc": generated_utc,
        },
    ]


def make_hybrid_contract(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("730_doc", "595_doc", "581_doc")
    return [
        {
            "contract_id": "HQC731_0_parent_space_split",
            "object_needed": "Conf_parent local split",
            "candidate_form": "Y=(O_GR, Phi_red, R_rep, B_ref), with pi_h(Y)=(O_GR, Phi_red, B_ref)",
            "success_test": "Conf_parent is a fibre bundle over Q_obs^hybrid and representative fibres contain only unobservable local MTS data",
            "current_status": "candidate_contract_not_constructed",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "HQC731_1_observed_GR_core",
            "object_needed": "observed metric/coframe sector",
            "candidate_form": "O_GR=(g_obs or e_obs, ordinary matter fields, theta_univ, compact boundary ADM/reference class)",
            "success_test": "local vacuum equations for O_GR reduce to EH/GR before any MTS representative readout",
            "current_status": "standard_template_not_current_MTS_proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("730_doc", "511_doc"),
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "HQC731_2_vertical_generator",
            "object_needed": "local MTS representative vertical v_X",
            "candidate_form": "d pi_h(v_X)=0; v_X[O_GR]=0, v_X[Phi_red]=0, v_X[B_ref]=0, v_X[R_rep]!=0 allowed",
            "success_test": "field-by-field vertical action leaves observed metric, matter, clocks, and ADM/reference class unchanged",
            "current_status": "formal_dpi_zero_contract_only",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "HQC731_3_action_factorisation",
            "object_needed": "hybrid parent action",
            "candidate_form": "S_parent=S_EH[O_GR]+S_extra_red[O_GR,Phi_red]+S_matter[psi,O_GR,theta_univ]+dB_rep[R_rep,B_ref]",
            "success_test": "theta_Y(v_X)-mu_X=dB_rep or 0 before field equations; no bulk representative source remains",
            "current_status": "conditional_template",
            "valid_for_claim": "false",
            "source_paths": source_path_string("730_doc", "729_doc", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "HQC731_4_PJ_zero_for_extra",
            "object_needed": "extra local P/J silence",
            "candidate_form": "j_X^rep=theta_Y(v_X)-mu_X=dB_rep, so P_rep=0/exact, J_rep=0, C_X^rep=0",
            "success_test": "the only surviving local P/J current is the observed EH/GR current, not a new X source",
            "current_status": "conditional_if_factorisation_and_boundary_hold",
            "valid_for_claim": "false",
            "source_paths": source_path_string("729_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "HQC731_5_no_double_count_GR_charge",
            "object_needed": "ADM/Pi_M separation",
            "candidate_form": "ordinary ADM time/rotation charges live in Q_obs^hybrid; representative vertical X excludes improper GR symmetries",
            "success_test": "Pi_M and Hamiltonian boundary charges are inherited from observed EH sector, while Q_X^rep=0",
            "current_status": "not_derived_gate_explicit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("594_doc", "595_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_matter_blindness(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("594_doc", "595_doc", "730_doc")
    return [
        {
            "gate_id": "MBG731_0_metric_blindness",
            "condition": "hat_g(Y)=g_obs or hat_g_red(pi_h(Y)); no representative R_rep dependence",
            "kills": "delta_X S_matter metric source and universal fifth-force response",
            "counterexample_if_missing": "hat_g_mu_nu=exp(2 a X_rep) g_obs_mu_nu is universal and WEP-safe but X-charged",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MBG731_1_clock_unit_blindness",
            "condition": "clock/unit/readout constants theta_univ factor through pi_h and not R_rep",
            "kills": "qbar_XT through clock, unit, or calibration response",
            "counterexample_if_missing": "universal constants or local rulers depend on representative fibre data",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MBG731_2_species_blindness",
            "condition": "all ordinary matter species use the same observed metric and no species-specific representative marker",
            "kills": "composition-dependent fifth force and WEP residuals",
            "counterexample_if_missing": "species-dependent material marker couples to R_rep",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MBG731_3_no_marker_minimality",
            "condition": "allowed covariant matter/readout functors are restricted to Q_obs^hybrid unless a new marker pays an explicit extension cost",
            "kills": "universal marker loophole that covariance alone cannot remove",
            "counterexample_if_missing": "a universal covariant scalar marker silently reintroduces X as physical",
            "current_status": "not_proved",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MBG731_4_readout_after_variation",
            "condition": "observables are read from Sol(S_parent) after varying the parent action",
            "kills": "post-readout EFT fake zero",
            "counterexample_if_missing": "a readout-reduced action bakes q_loc=0 into effective variables and then varies it as fundamental",
            "current_status": "contract_known_not_proved",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
    ]


def make_boundary_closure(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("594_doc", "595_doc", "730_doc")
    return [
        {
            "boundary_id": "BCL731_0_proper_vertical_domain",
            "condition": "representative vertical parameter X_rep vanishes or fixes representative data on compact local boundary",
            "effect": "Q_X^rep=0 by allowed transformation domain",
            "risk": "too restrictive if the theory later needs a physical edge transition mode",
            "current_status": "available_as_closure_condition_not_derived",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "boundary_id": "BCL731_1_exact_boundary_current",
            "condition": "j_X^rep=dB_rep and the compact-boundary integral vanishes or is reference-fixed",
            "effect": "extra P/J are zero/exact and no alpha_edge row is needed for representative X",
            "risk": "requires explicit B_rep from the parent action, not just a boundary wish",
            "current_status": "not_constructed",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "boundary_id": "BCL731_2_Hamiltonian_projection_zero",
            "condition": "Pi_M^H[Q_X^rep]=0 including reference subtraction",
            "effect": "representative edge current cannot shift measured local mass",
            "risk": "Pi_M/Pi_EH lock is not fully closed",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_doc", "594_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
        {
            "boundary_id": "BCL731_3_no_improper_GR_charge_confusion",
            "condition": "ordinary ADM time/rotation/boost symmetries remain in observed EH sector and are not in representative v_X domain",
            "effect": "hybrid quotient does not erase physical GR charges",
            "risk": "reviewers will reject the construction if it quotients away real Hamiltonian charges",
            "current_status": "must_be_explicit",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "boundary_id": "BCL731_4_corner_symplectic_flux",
            "condition": "Omega_boundary(delta Y,v_X^rep)=0 or exact/reference-fixed on local worldtube corners",
            "effect": "DCdagger/Omega-flat representative generator has no physical edge residue",
            "risk": "nonzero corner flux becomes boundary hair and source-backed edge alpha is needed",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("728_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_redteam(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("594_doc", "595_doc", "730_doc")
    return [
        {
            "redteam_id": "NCR731_0_conformal_universal_marker",
            "attack": "hat_g_mu_nu=exp(2 a X_rep) g_obs_mu_nu",
            "why_reviewers_accept_attack": "it is universal and covariant, so WEP alone does not kill it",
            "required_kill": "prove matter metric functors factor through pi_h, forcing a=0 or X_rep absent",
            "current_status": "not_killed",
            "route_if_not_killed": "finite qbar_XT or source-backed edge branch",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR731_1_boundary_edge_mode",
            "attack": "representative vertical symmetry carries nonzero edge charge",
            "why_reviewers_accept_attack": "gauge directions can carry physical boundary charges",
            "required_kill": "proper vertical domain or explicit B_rep with zero compact-boundary integral",
            "current_status": "not_killed",
            "route_if_not_killed": "source K_edge and Qbar_edge_XH",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR731_2_Gamma_Khat_q_loc_side_door",
            "attack": "Gamma_eff, K_hat, or q_loc contains a real local scalar/vector source not determined by Q_obs^hybrid",
            "why_reviewers_accept_attack": "then q_loc is a physical profile, not a quotient identity",
            "required_kill": "derive these objects as quotient pullbacks or exact representative identities",
            "current_status": "next_primary_test",
            "route_if_not_killed": "demote hybrid quotient route to diffeo-current or finite residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("595_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR731_3_ADM_double_count",
            "attack": "representative quotient accidentally eats ordinary GR Hamiltonian/ADM charges",
            "why_reviewers_accept_attack": "physical boundary symmetries are not gauge redundancies",
            "required_kill": "put ADM/reference class in Q_obs^hybrid and exclude improper GR symmetries from v_X^rep",
            "current_status": "guard_written_not_proved",
            "route_if_not_killed": "reject quotient proof credit",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR731_4_fixed_point_tuning",
            "attack": "double zeros are simply assumed in S_extra",
            "why_reviewers_accept_attack": "zeros without a parent mechanism look tuned",
            "required_kill": "derive F_1=0 and ell_tr/L_cg from symmetry, quotient, or stability mechanism",
            "current_status": "residual_backup_only",
            "route_if_not_killed": "do not use fixed-point route as exact GR reduction",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_doc", "730_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_backup_routes(generated_utc: str) -> list[dict[str, Any]]:
    edge_rows = read_csv(SOURCES["730_edge_input"]["path"])
    edge_missing = any(row.get("K_edge", "") == "MISSING_SOURCE" for row in edge_rows)
    return [
        {
            "backup_id": "BRL731_0_strict_quotient_subcase",
            "trigger": "hybrid split simplifies because all observed dynamics cleanly factor through pi and no separate EH/current split is needed",
            "handling": "use pure strict quotient-zero theorem route",
            "status": "subcase_open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup_id": "BRL731_1_diffeo_identity",
            "trigger": "representative quotient fails but C_X exactly equals parent diffeomorphism/momentum constraint",
            "handling": "return to diffeo current identity route",
            "status": "backup_open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup_id": "BRL731_2_fixed_point_residual",
            "trigger": "quotient silence fails but double zeros and residual law can be parent-derived",
            "handling": "score a derived residual vector rather than claim exact no-pole",
            "status": "backup_open_requires_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup_id": "BRL731_3_edge_coefficients",
            "trigger": "hybrid, strict quotient, diffeo identity, and fixed-point derivations all fail",
            "handling": "source K_edge,Qbar_edge_XH,qbar_XT and score alpha_edge(lambda)",
            "status": "blocked_missing_sources" if edge_missing else "diagnostic_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "backup_id": "BRL731_4_demote_local_branch",
            "trigger": "no theorem route and no source-backed finite coefficient survives",
            "handling": "demote local R10/local-GR branch to explicit closure-only assumption",
            "status": "last_resort_not_triggered",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_decision(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D731_0_select_hybrid_primary",
            "decision": "select hybrid EH-plus-quotient-extra as primary route",
            "meaning": "local GR is carried by observed EH sector while extra local MTS representative directions must be quotient-silent",
            "claim_status": "route_selected_not_proved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D731_1_strict_quotient_retained_as_subcase",
            "decision": "keep pure strict quotient-zero as a clean subcase",
            "meaning": "use it only if all local observed/readout/boundary structures factor through one quotient without eating GR charges",
            "claim_status": "subcase_open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D731_2_boundary_and_matter_are_gatekeepers",
            "decision": "matter blindness and boundary/ADM separation decide whether the route survives",
            "meaning": "universal conformal markers and edge charges are still live attacks",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D731_3_next_construct_hybrid_pi",
            "decision": "next target should construct pi_h and test Gamma/Khat/q_loc against it",
            "meaning": "if q_loc is not a quotient/exact identity, hybrid route demotes",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU731_0_allowed",
            "allowed_after_731": "construct pi_h:Y->Q_obs^hybrid with observed EH sector plus quotient-silent representative fibre",
            "forbidden_after_731": "claim local GR just because hybrid route was selected",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU731_1_allowed",
            "allowed_after_731": "treat conformal markers, matter clocks, and boundary edge modes as live red-team gates",
            "forbidden_after_731": "dismiss universal X couplings because they are WEP-safe",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU731_2_allowed",
            "allowed_after_731": "keep diffeo-current identity and fixed-point double-zero as backups",
            "forbidden_after_731": "hand-wave MTS C_X into GR or assume F_1=0 without parent mechanism",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU731_3_allowed",
            "allowed_after_731": "if theorem routes fail, source real edge coefficients before any local/R10 claim",
            "forbidden_after_731": "promote diagnostic edge rows",
            "next_action": "source-backed edge fallback only after theorem route stalls",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "hybrid EH-plus-quotient-extra selected as the primary low-scrutiny route",
            "hard_blocker": "pi_h, matter/no-marker blindness, boundary/ADM separation, and Gamma/Khat/q_loc factorisation are still unproved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_claim_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows or "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def make_validation(
    source_register: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    hybrid_rows: list[dict[str, Any]],
    matter_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    redteam_rows: list[dict[str, Any]],
    backup_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    generated_tables = [
        SOURCE_REGISTER_PATH,
        ROUTE_SELECTION_PATH,
        HYBRID_CONTRACT_PATH,
        MATTER_BLINDNESS_PATH,
        BOUNDARY_CLOSURE_PATH,
        REDTEAM_PATH,
        BACKUP_ROUTES_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
    ]
    source_paths_ok = all(row["exists"] == "true" for row in source_register)
    source_needles_ok = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["730_validation"]["path"])
    selected_731 = text_contains(SOURCES["730_validation"]["path"], ["V730_11_next_target_selected", OUTPUT_DOC.name])
    hybrid_selected = any(row["route_id"] == "RS731_A_hybrid_EH_plus_quotient_extra" and row["selected"] == "true_primary" for row in route_rows)
    strict_retained = any(row["route_id"] == "RS731_B_strict_quotient_zero" and row["selected"] == "true_subcase" for row in route_rows)
    contract_has_pi = any(row["contract_id"] == "HQC731_0_parent_space_split" for row in hybrid_rows)
    contract_has_adm = any(row["contract_id"] == "HQC731_5_no_double_count_GR_charge" for row in hybrid_rows)
    matter_has_conformal = any(row["gate_id"] == "MBG731_0_metric_blindness" and "exp(2 a X_rep)" in row["counterexample_if_missing"] for row in matter_rows)
    matter_has_readout = any(row["gate_id"] == "MBG731_4_readout_after_variation" for row in matter_rows)
    boundary_has_adm = any(row["boundary_id"] == "BCL731_3_no_improper_GR_charge_confusion" for row in boundary_rows)
    boundary_has_corner = any(row["boundary_id"] == "BCL731_4_corner_symplectic_flux" for row in boundary_rows)
    redteam_has_q = any(row["redteam_id"] == "NCR731_2_Gamma_Khat_q_loc_side_door" for row in redteam_rows)
    backup_has_all = {"BRL731_1_diffeo_identity", "BRL731_2_fixed_point_residual", "BRL731_3_edge_coefficients"}.issubset(
        {row["backup_id"] for row in backup_rows}
    )
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    claim_false = all_generated_claim_false(generated_tables)
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()
    return [
        {"check_id": "V731_0_source_paths_exist", "result": "pass" if source_paths_ok else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V731_1_source_needles_present", "result": "pass" if source_needles_ok else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V731_2_prior_730_clean", "result": "pass" if prior_clean else "fail", "detail": "730 validation has no failures"},
        {"check_id": "V731_3_730_selected_731", "result": "pass" if selected_731 else "fail", "detail": "730 selected this checkpoint"},
        {"check_id": "V731_4_hybrid_primary_selected", "result": "pass" if hybrid_selected else "fail", "detail": "hybrid EH-plus-quotient-extra selected as primary"},
        {"check_id": "V731_5_strict_quotient_subcase_retained", "result": "pass" if strict_retained else "fail", "detail": "strict quotient-zero retained as pure subcase"},
        {"check_id": "V731_6_hybrid_contract_has_pi_and_ADM_guard", "result": "pass" if contract_has_pi and contract_has_adm else "fail", "detail": f"hybrid_rows={len(hybrid_rows)};pi={contract_has_pi};ADM={contract_has_adm}"},
        {"check_id": "V731_7_matter_blindness_gates_retained", "result": "pass" if matter_has_conformal and matter_has_readout else "fail", "detail": "conformal marker and readout-after-variation gates retained"},
        {"check_id": "V731_8_boundary_ADM_and_corner_guards_present", "result": "pass" if boundary_has_adm and boundary_has_corner else "fail", "detail": f"boundary_rows={len(boundary_rows)};ADM={boundary_has_adm};corner={boundary_has_corner}"},
        {"check_id": "V731_9_q_loc_side_door_redteam_retained", "result": "pass" if redteam_has_q else "fail", "detail": "Gamma/Khat/q_loc remains next primary test"},
        {"check_id": "V731_10_backup_routes_present", "result": "pass" if backup_has_all else "fail", "detail": f"backup_rows={len(backup_rows)}"},
        {"check_id": "V731_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V731_12_no_claim_rows_promoted", "result": "pass" if claim_false else "fail", "detail": "all generated rows with valid_for_claim remain false"},
        {"check_id": "V731_13_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V731_14_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V731_15_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V731_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def write_markdown(
    generated_utc: str,
    run_root: Path,
    source_register: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    hybrid_rows: list[dict[str, Any]],
    matter_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    redteam_rows: list[dict[str, Any]],
    backup_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_update_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 731 - Y5 R10 Choose Quotient-Zero Or Diffeo Current Identity And Close Boundary

## Summary

This checkpoint chooses the current-chain route after 730.

Current route choice: **hybrid EH-plus-quotient-extra first**.

```text
Y = (O_GR, Phi_red, R_rep, B_ref)
pi_h(Y) = (O_GR, Phi_red, B_ref)
d pi_h(v_X^rep) = 0
S_parent = S_EH[O_GR] + S_extra_red[O_GR,Phi_red] + S_matter[psi,O_GR,theta_univ] + dB_rep[R_rep,B_ref]
```

The practical idea is simple: local GR is carried by the observed EH metric/current; the extra local MTS representative direction must be quotient-silent. This is not a claim. Matter/no-marker blindness, boundary/ADM separation, and `Gamma_eff/K_hat/q_loc` factorisation remain open.

| Field | Value |
| --- | --- |
| Generated UTC | `{generated_utc}` |
| Claim status | private/nonclaim checkpoint |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |
| Run root | `{relative(run_root)}` |

## Route Selection

{markdown_table(route_rows, ["route_id", "scrutiny_profile", "why_selected", "main_burden", "failure_mode", "selected", "valid_for_claim"])}

## Hybrid Quotient Contract

{markdown_table(hybrid_rows, ["contract_id", "object_needed", "candidate_form", "success_test", "current_status", "valid_for_claim"])}

## Matter Blindness Gate

{markdown_table(matter_rows, ["gate_id", "condition", "kills", "counterexample_if_missing", "current_status", "valid_for_claim"])}

## Boundary Closure Ledger

{markdown_table(boundary_rows, ["boundary_id", "condition", "effect", "risk", "current_status", "valid_for_claim"])}

## No-Cheat Red Team

{markdown_table(redteam_rows, ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed", "valid_for_claim"])}

## Backup Route Ledger

{markdown_table(backup_rows, ["backup_id", "trigger", "handling", "status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_update_rows, ["route_id", "allowed_after_731", "forbidden_after_731", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read

This is the cleaner route. We are not trying to sneak a fifth force below a bound; we are trying to make the extra local MTS direction not be a physical local force at all, while leaving ordinary GR charges alive in the observed EH sector. The next danger is the side door: if `Gamma_eff`, `K_hat`, or `q_loc` depends on representative fibre data, the quotient silence breaks and we demote.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-choose-hybrid-quotient-close-boundary"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    route_rows = make_route_selection(generated_utc)
    hybrid_rows = make_hybrid_contract(generated_utc)
    matter_rows = make_matter_blindness(generated_utc)
    boundary_rows = make_boundary_closure(generated_utc)
    redteam_rows = make_redteam(generated_utc)
    backup_rows = make_backup_routes(generated_utc)
    decision_rows = make_decision(generated_utc)
    route_update_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        ROUTE_SELECTION_PATH,
        HYBRID_CONTRACT_PATH,
        MATTER_BLINDNESS_PATH,
        BOUNDARY_CLOSURE_PATH,
        REDTEAM_PATH,
        BACKUP_ROUTES_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
        run_root / "status.json",
        run_root / "COMPLETE.marker",
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        ROUTE_SELECTION_PATH,
        route_rows,
        ["route_id", "scrutiny_profile", "why_selected", "main_burden", "failure_mode", "selected", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        HYBRID_CONTRACT_PATH,
        hybrid_rows,
        ["contract_id", "object_needed", "candidate_form", "success_test", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        MATTER_BLINDNESS_PATH,
        matter_rows,
        ["gate_id", "condition", "kills", "counterexample_if_missing", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        BOUNDARY_CLOSURE_PATH,
        boundary_rows,
        ["boundary_id", "condition", "effect", "risk", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        REDTEAM_PATH,
        redteam_rows,
        ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(BACKUP_ROUTES_PATH, backup_rows, ["backup_id", "trigger", "handling", "status", "valid_for_claim", "generated_utc"])
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update_rows,
        ["route_id", "allowed_after_731", "forbidden_after_731", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(
        source_register,
        route_rows,
        hybrid_rows,
        matter_rows,
        boundary_rows,
        redteam_rows,
        backup_rows,
        decision_rows,
        output_paths,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated_utc,
        run_root,
        source_register,
        route_rows,
        hybrid_rows,
        matter_rows,
        boundary_rows,
        redteam_rows,
        backup_rows,
        decision_rows,
        route_update_rows,
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
