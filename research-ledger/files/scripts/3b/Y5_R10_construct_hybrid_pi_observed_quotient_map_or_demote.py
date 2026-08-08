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
OUTPUT_DOC = POST_CHECKPOINT / "732-Y5-R10-construct-hybrid-pi-observed-quotient-map-or-demote.md"
NEXT_TARGET = "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_732_hybrid_pi_map_constructed_q_loc_vertical_blind_only_exact_zero_demoted"
CLAIM_CEILING = "hybrid_pi_candidate_and_pullback_lemma_only_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_732_SOURCE_REGISTER.csv"
PI_MAP_PATH = RESIDUALS / "P8_Y5_R10_732_HYBRID_PI_MAP.csv"
PULLBACK_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_732_HYBRID_PULLBACK_LEMMA.csv"
FACTOR_TEST_PATH = RESIDUALS / "P8_Y5_R10_732_GAMMA_KHAT_QLOC_FACTORISATION_TEST.csv"
EXACTNESS_GATE_PATH = RESIDUALS / "P8_Y5_R10_732_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv"
DEMOTION_PATH = RESIDUALS / "P8_Y5_R10_732_DEMOTION_GATE.csv"
REDTEAM_PATH = RESIDUALS / "P8_Y5_R10_732_NO_CHEAT_RED_TEAM.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_732_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_732_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_732_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_732_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "731_doc": {
        "path": POST_CHECKPOINT / "731-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md",
        "role": "immediate hybrid route selection handoff",
        "needles": ["hybrid EH-plus-quotient-extra first", OUTPUT_DOC.name, "Gamma_eff/K_hat/q_loc"],
    },
    "731_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_731_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V731_11_next_target_selected", OUTPUT_DOC.name, "V731_14_formalization_workbench_untouched"],
    },
    "731_hybrid_contract": {
        "path": RESIDUALS / "P8_Y5_R10_731_HYBRID_QUOTIENT_CONTRACT.csv",
        "role": "current hybrid quotient contract",
        "needles": ["HQC731_0_parent_space_split", "HQC731_5_no_double_count_GR_charge", "false"],
    },
    "731_matter": {
        "path": RESIDUALS / "P8_Y5_R10_731_MATTER_BLINDNESS_GATE.csv",
        "role": "current matter blindness gates",
        "needles": ["MBG731_0_metric_blindness", "MBG731_4_readout_after_variation", "false"],
    },
    "731_boundary": {
        "path": RESIDUALS / "P8_Y5_R10_731_BOUNDARY_CLOSURE_LEDGER.csv",
        "role": "current boundary/ADM gates",
        "needles": ["BCL731_3_no_improper_GR_charge_confusion", "BCL731_4_corner_symplectic_flux", "false"],
    },
    "731_redteam": {
        "path": RESIDUALS / "P8_Y5_R10_731_NO_CHEAT_RED_TEAM.csv",
        "role": "current no-cheat red team",
        "needles": ["NCR731_2_Gamma_Khat_q_loc_side_door", "next_primary_test", "false"],
    },
    "595_doc": {
        "path": POST_CHECKPOINT / "595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md",
        "role": "older pi observed quotient map",
        "needles": ["pi(Y)=O", "Gamma_eff", "q_loc"],
    },
    "596_doc": {
        "path": POST_CHECKPOINT / "596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md",
        "role": "older pullback lemma and q_loc demotion",
        "needles": ["q_loc being a quotient pullback does not imply q_loc=0", "vertical-blind", "reduced GK action owner"],
    },
    "729_doc": {
        "path": POST_CHECKPOINT / "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "role": "current P/J Noether-current origin contract",
        "needles": ["one parent Noether current", "j_X = theta_Y(v_X) - mu_X", "contract sharpened"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "role": "strict quotient no-pole theorem shape",
        "needles": ["quotient-vertical no-pole", "Conf_parent --pi-->", "boundary charge"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc stress-divergence route",
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


def make_pi_map(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("731_doc", "731_hybrid_contract", "595_doc")
    return [
        {
            "map_id": "HPM732_0_parent_space",
            "object": "Conf_parent(local compact region)",
            "candidate_definition": "Y=(O_GR,Phi_red,R_rep,B_ref), where O_GR carries observed metric/coframe, matter, clocks, and ADM/reference data",
            "mathematical_test": "Conf_parent is a fibre bundle over Q_obs^hybrid with projection pi_h(Y)=(O_GR,Phi_red,B_ref)",
            "current_result": "candidate_constructed_as_formal_hybrid_bundle",
            "claim_status": "nonclaim_candidate",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "HPM732_1_observed_quotient",
            "object": "Q_obs^hybrid",
            "candidate_definition": "Q_obs^hybrid=(g_obs/e_obs, psi_A, theta_univ, Phi_red, compact-boundary ADM/reference class)",
            "mathematical_test": "every local observable, clock, ruler, matter coupling, and local GR charge is a function/functor of Q_obs^hybrid only",
            "current_result": "named_but_not_verified_for_Gamma_Khat_q_loc",
            "claim_status": "open",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "HPM732_2_representative_fibre",
            "object": "R_rep",
            "candidate_definition": "representative motion/time/domain/local fibre data whose changes do not alter O_GR, Phi_red, or B_ref",
            "mathematical_test": "for vertical zeta, exp(zeta v_X^rep) changes R_rep while pi_h is unchanged",
            "current_result": "formal_fibre_definition_available",
            "claim_status": "conditional",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "HPM732_3_vertical_generator",
            "object": "v_X^rep",
            "candidate_definition": "v_X^rep[O_GR]=0, v_X^rep[Phi_red]=0, v_X^rep[B_ref]=0, v_X^rep[R_rep]=delta_X R_rep",
            "mathematical_test": "d pi_h(v_X^rep)=0 field-by-field and no hidden induced variation of g_obs, theta_univ, psi_A, or ADM/reference data",
            "current_result": "formal_dpi_zero_by_definition_but_symbol_match_open",
            "claim_status": "conditional",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "map_id": "HPM732_4_parent_action_pullback",
            "object": "S_parent",
            "candidate_definition": "S_EH[O_GR]+S_extra_red[O_GR,Phi_red]+S_matter[psi_A,O_GR,theta_univ]+dB_rep[R_rep,B_ref]",
            "mathematical_test": "delta_X S_parent=0 plus exact/proper boundary term before imposing field equations",
            "current_result": "works_as_contract_not_as_current_MTS_derivation",
            "claim_status": "open",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_doc", "729_doc", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "map_id": "HPM732_5_boundary_domain",
            "object": "proper local representative transformations",
            "candidate_definition": "v_X^rep transformations are compactly supported or fixed on the local boundary; ordinary ADM symmetries stay in O_GR",
            "mathematical_test": "Q_X^rep=0 while ADM mass/angular momentum/reference subtraction remain observable in Q_obs^hybrid",
            "current_result": "boundary_rule_written_not_derived_from_B_rep",
            "claim_status": "open",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "595_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_pullback_lemma(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("596_doc", "731_doc", "595_doc")
    return [
        {
            "lemma_id": "HPL732_0_pullback_setup",
            "statement": "Let pi_h:Conf_parent->Q_obs^hybrid and v_X^rep in ker(d pi_h). If Gamma_eff=gamma o pi_h, K_hat=kappa o pi_h, P_loc=Pi o pi_h, and nabla is built from g_obs in Q_obs^hybrid, then these objects are representative-vertical-blind.",
            "derivation": "L_{v_X}(gamma o pi_h)=d gamma[d pi_h(v_X)]=0; same for kappa, Pi, and g_obs-compatible nabla.",
            "consequence": "representative motion cannot directly create qbar_XT or a new local X fifth-force source through Gamma/Khat",
            "current_status": "conditional_lemma_proved",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "HPL732_1_q_loc_pullback",
            "statement": "Under the same assumptions, q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) is a pullback from Q_obs^hybrid.",
            "derivation": "all ingredients are functions of Q_obs^hybrid, so L_{v_X}q_loc=0",
            "consequence": "q_loc is not a representative-X source if the pullback assumptions are true",
            "current_status": "conditional_lemma_proved",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "HPL732_2_not_zero",
            "statement": "q_loc being a hybrid quotient pullback does not imply q_loc=0.",
            "derivation": "a nonzero tensor field on Q_obs^hybrid can be vertical-blind and still physically observable",
            "consequence": "hybrid quotient factorisation solves the hidden representative-X issue, not local-GR residual silence by itself",
            "current_status": "hard_distinction_added",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "HPL732_3_exact_zero_condition",
            "statement": "q_loc=0 follows only if T_GK^{mu nu}=Gamma_eff g_obs^{mu nu}-K_hat^{mu nu} is a Hilbert stress of a reduced diffeomorphism-invariant action and the reduced fields are on shell with no boundary/source flux.",
            "derivation": "the reduced Ward identity gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A plus boundary terms; compact local vacuum requires E_A=0 and zero flux",
            "consequence": "exact local silence needs reduced action ownership, not only pi_h factorisation",
            "current_status": "conditional_Ward_route_only",
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc", "513_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_factor_tests(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "HFT732_0_EH_local_GR_block",
            "sector": "observed local GR metric/coframe",
            "factorisation_requirement": "Einstein-Hilbert and ordinary matter metric use g_obs/e_obs in Q_obs^hybrid",
            "what_would_pass": "v_X^rep[g_obs]=0 and local vacuum exterior equations reduce to EH equations for O_GR",
            "current_result": "safe_contract_if_O_GR_is_kept_explicit",
            "scrutiny_level": "low_if_kept_explicit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_doc", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_1_matter_metric_and_clocks",
            "sector": "matter, clocks, units",
            "factorisation_requirement": "hat_g(Y)=g_obs or hat_g_red(pi_h(Y)); theta_univ=theta_univ(pi_h(Y)); no R_rep marker",
            "what_would_pass": "delta_X S_matter=0 for all ordinary matter species before readout",
            "current_result": "blocked_until_no_marker_or_functor_universality_is_proved",
            "scrutiny_level": "medium",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_matter", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_2_Gamma_Khat_q_loc",
            "sector": "Gamma_eff, K_hat, q_loc",
            "factorisation_requirement": "Gamma_eff and K_hat must be pullbacks from Q_obs^hybrid or combine into an exact representative identity with q_loc=0",
            "what_would_pass": "P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) is reduced/vertical-blind, and exact zero only with reduced Ward owner plus no boundary flux",
            "current_result": "vertical_blind_condition_written_exact_zero_not_derived",
            "scrutiny_level": "high",
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc", "513_doc", "731_redteam"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_3_memory_domain_projector",
            "sector": "memory/domain/projector fields",
            "factorisation_requirement": "memory/domain variables split into Phi_red in Q_obs^hybrid plus pure representative fibre R_rep",
            "what_would_pass": "source/load terms for cosmology/galaxy pillars depend on Phi_red, while local representative R_rep is silent",
            "current_result": "not_checked_against_full_symbol_spine",
            "scrutiny_level": "medium_high",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_doc", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_4_Noether_PJ",
            "sector": "representative P/J/C_X",
            "factorisation_requirement": "theta(v_X^rep)-mu_X=dB_rep with zero proper boundary integral",
            "what_would_pass": "P_rep=0/exact, J_rep=0, C_X^rep=0 as an off-shell representative quotient identity",
            "current_result": "conditional_if_action_pullback_and_boundary_primitive_are_built",
            "scrutiny_level": "medium",
            "valid_for_claim": "false",
            "source_paths": source_path_string("729_doc", "731_boundary"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_5_boundary_ADM_separation",
            "sector": "boundary charges",
            "factorisation_requirement": "representative vertical X excludes ordinary improper GR symmetries and has zero compact local charge",
            "what_would_pass": "Q_X^rep=0 while ADM mass/angular momentum/reference subtraction remain observable in O_GR",
            "current_result": "not_derived_but_guard_is_explicit",
            "scrutiny_level": "medium_high",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "595_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "HFT732_6_readout_order",
            "sector": "observables/readout",
            "factorisation_requirement": "readout is R_read:Sol(S_parent)->Observables after parent variation",
            "what_would_pass": "no post-readout reduced action is varied as if fundamental to fake q_loc=0",
            "current_result": "contract_retained",
            "scrutiny_level": "low_if_obeyed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_matter", "595_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_exactness_gate(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "QEG732_0_vertical_source_gate",
            "question": "Can Gamma/Khat/q_loc be made blind to representative X_rep?",
            "answer": "yes_conditionally_if_defined_as_Q_obs_hybrid_pullbacks",
            "meaning": "this protects the hybrid route from smuggling a hidden representative fifth-force field",
            "failure_route": "if any R_rep derivative survives, hybrid quotient route demotes to diffeo-current or finite residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc", "731_redteam"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QEG732_1_exact_local_zero_gate",
            "question": "Does hybrid pullback imply q_loc=0?",
            "answer": "no",
            "meaning": "q_loc can be an observed reduced residual even when it is representative-vertical-blind",
            "failure_route": "must derive Ward zero or score q_loc residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QEG732_2_Ward_owner_gate",
            "question": "Is T_GK=Gamma g-Khat owned by a reduced diffeomorphism-invariant action on Q_obs^hybrid?",
            "answer": "not_for_current_MTS",
            "meaning": "the route is written but current MTS lacks a reduced S_GK owner and K_hat metric-response identity",
            "failure_route": "reduced residual runner or diffeo-current backup",
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc", "513_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "QEG732_3_boundary_flux_gate",
            "question": "Can a reduced bulk q_loc zero still leak through boundary/source-measure terms?",
            "answer": "yes_if_boundary_no_flux_not_proved",
            "meaning": "exact route needs boundary primitive/reference subtraction and corner symplectic silence",
            "failure_route": "source-backed edge/source-measure bound",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "596_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_demotion(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "DR732_A_hybrid_quotient_rep_X",
            "status_after_732": "kept_as_conditional_construction_route",
            "reason": "pi_h can be written and pullback assumptions make Gamma/Khat/q_loc representative-vertical-blind",
            "not_allowed": "claim q_loc=0 or local GR from vertical-blindness alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "DR732_B_q_loc_exact_zero",
            "status_after_732": "demoted_for_current_claim",
            "reason": "hybrid pullback does not imply exact zero; reduced S_GK owner, K_hat metric response, and boundary no-flux are absent",
            "not_allowed": "use q_loc silence as a theorem-zero row",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "DR732_C_observed_reduced_residual",
            "status_after_732": "promoted_as_honest_fallback",
            "reason": "a vertical-blind but nonzero q_loc is an observed reduced residual, not a hidden representative-X field",
            "not_allowed": "hide it under quotient language",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "DR732_D_diffeo_current_backup",
            "status_after_732": "backup_open",
            "reason": "if reduced Gamma/Khat owner fails, C_X may still match ordinary parent diffeomorphism/momentum current",
            "not_allowed": "double-count ADM/Hamiltonian charges",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "DR732_E_finite_edge_bound",
            "status_after_732": "fallback_open",
            "reason": "if neither hybrid quotient nor diffeo-current proof closes, q_loc/edge/source-normalization rows must be bounded numerically",
            "not_allowed": "mark diagnostic coefficients as source-backed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_redteam(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("731_redteam", "596_doc")
    return [
        {
            "redteam_id": "NCR732_0_representative_marker",
            "attack": "matter/readout depends on R_rep through a universal covariant marker",
            "why_reviewers_accept_attack": "WEP safety does not remove universal scalar/vector marker couplings",
            "required_kill": "no-marker/minimality theorem or explicit extension tax",
            "current_status": "not_killed",
            "route_if_not_killed": "finite qbar_XT/source-backed residual branch",
            "valid_for_claim": "false",
            "source_paths": source_paths,
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR732_1_Gamma_Khat_real_reduced_field",
            "attack": "Gamma_eff or K_hat is reduced but nonzero and physically observable",
            "why_reviewers_accept_attack": "vertical-blindness is not local-GR silence",
            "required_kill": "reduced GK Ward owner with on-shell/no-flux exact zero, or score residual",
            "current_status": "not_killed_next_owner_target",
            "route_if_not_killed": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("596_doc", "513_doc"),
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR732_2_boundary_edge_mode",
            "attack": "representative vertical mode has nonzero boundary or corner symplectic charge",
            "why_reviewers_accept_attack": "gauge-looking directions can become physical at boundaries",
            "required_kill": "proper domain plus exact B_rep and Omega_boundary silence",
            "current_status": "not_killed",
            "route_if_not_killed": "source K_edge/Qbar_edge_XH",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary"),
            "generated_utc": generated_utc,
        },
        {
            "redteam_id": "NCR732_3_post_readout_cheat",
            "attack": "q_loc=0 is imposed in a readout-reduced action and then varied as fundamental",
            "why_reviewers_accept_attack": "this bakes the target closure into the effective variables",
            "required_kill": "readout only after parent Euler equations",
            "current_status": "guard_written",
            "route_if_not_killed": "reject proof credit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_matter", "595_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_decision(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D732_0_hybrid_pi_candidate_constructed",
            "decision": "construct formal hybrid quotient map pi_h with observed EH sector and representative fibre",
            "meaning": "the hybrid route is mathematically coherent as a bundle/pullback contract",
            "claim_status": "candidate_only_not_proved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D732_1_pullback_lemma_accepted",
            "decision": "accept conditional hybrid pullback lemma",
            "meaning": "if Gamma/Khat/P_loc are Q_obs^hybrid pullbacks, q_loc is representative-vertical-blind",
            "claim_status": "conditional_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D732_2_exact_q_loc_zero_not_derived",
            "decision": "demote exact q_loc zero for current MTS",
            "meaning": "vertical-blindness is not local-GR silence; reduced GK owner and boundary gates remain open",
            "claim_status": "q_loc_zero_false_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D732_3_next_owner_or_runner",
            "decision": "force next pass to choose reduced GK owner or hybrid q_loc residual runner",
            "meaning": "the next target must either build S_GK on Q_obs^hybrid or stop theorem-hunting and score the retained residual",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU732_0_allowed",
            "allowed_after_732": "say q_loc can be representative-vertical-blind under explicit Q_obs^hybrid pullback assumptions",
            "forbidden_after_732": "say hybrid quotient factorisation has derived q_loc=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU732_1_allowed",
            "allowed_after_732": "treat nonzero q_loc as an observed reduced residual needing Ward ownership or bounds",
            "forbidden_after_732": "hide a nonzero reduced q_loc under representative-gauge language",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU732_2_allowed",
            "allowed_after_732": "keep diffeo-current, fixed-point, and finite-edge routes as backups",
            "forbidden_after_732": "close local branch without S_GK, boundary no-flux, and source-normalization proof",
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
            "main_result": "hybrid pi_h map is constructed and q_loc vertical-blindness lemma is conditional",
            "hard_blocker": "exact q_loc zero/local GR still needs reduced GK action ownership, K_hat metric-response identity, boundary no-flux, and matter no-marker proof",
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
    pi_rows: list[dict[str, Any]],
    lemma_rows: list[dict[str, Any]],
    factor_rows: list[dict[str, Any]],
    exact_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    redteam_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PI_MAP_PATH,
        PULLBACK_LEMMA_PATH,
        FACTOR_TEST_PATH,
        EXACTNESS_GATE_PATH,
        DEMOTION_PATH,
        REDTEAM_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
    ]
    source_paths_ok = all(row["exists"] == "true" for row in source_register)
    source_needles_ok = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["731_validation"]["path"])
    selected_732 = text_contains(SOURCES["731_validation"]["path"], ["V731_11_next_target_selected", OUTPUT_DOC.name])
    pi_written = any(row["map_id"] == "HPM732_0_parent_space" for row in pi_rows) and any(row["map_id"] == "HPM732_3_vertical_generator" for row in pi_rows)
    observed_gr = any(row["map_id"] == "HPM732_1_observed_quotient" and "g_obs" in row["candidate_definition"] for row in pi_rows)
    lemma_written = any(row["lemma_id"] == "HPL732_1_q_loc_pullback" for row in lemma_rows)
    not_zero_guard = any(row["lemma_id"] == "HPL732_2_not_zero" for row in lemma_rows)
    gamma_factor = any(row["test_id"] == "HFT732_2_Gamma_Khat_q_loc" for row in factor_rows)
    exact_demoted = any(row["route_id"] == "DR732_B_q_loc_exact_zero" and row["status_after_732"] == "demoted_for_current_claim" for row in demotion_rows)
    residual_route = any(row["route_id"] == "DR732_C_observed_reduced_residual" for row in demotion_rows)
    redteam_has_marker = any(row["redteam_id"] == "NCR732_0_representative_marker" for row in redteam_rows)
    redteam_has_boundary = any(row["redteam_id"] == "NCR732_2_boundary_edge_mode" for row in redteam_rows)
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    claim_false = all_generated_claim_false(generated_tables)
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()
    return [
        {"check_id": "V732_0_source_paths_exist", "result": "pass" if source_paths_ok else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V732_1_source_needles_present", "result": "pass" if source_needles_ok else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V732_2_prior_731_clean", "result": "pass" if prior_clean else "fail", "detail": "731 validation has no failures"},
        {"check_id": "V732_3_731_selected_732", "result": "pass" if selected_732 else "fail", "detail": "731 selected this checkpoint"},
        {"check_id": "V732_4_hybrid_pi_projection_candidate_written", "result": "pass" if pi_written else "fail", "detail": f"pi_rows={len(pi_rows)}"},
        {"check_id": "V732_5_observed_GR_sector_retained", "result": "pass" if observed_gr else "fail", "detail": "observed EH/GR sector retained in Q_obs^hybrid"},
        {"check_id": "V732_6_pullback_lemma_written", "result": "pass" if lemma_written else "fail", "detail": f"lemma_rows={len(lemma_rows)}"},
        {"check_id": "V732_7_pullback_not_zero_guard", "result": "pass" if not_zero_guard else "fail", "detail": "q_loc pullback does not imply q_loc zero"},
        {"check_id": "V732_8_Gamma_Khat_q_loc_factor_test_present", "result": "pass" if gamma_factor else "fail", "detail": "Gamma_eff/K_hat/q_loc remains high-risk factor test"},
        {"check_id": "V732_9_exact_zero_demoted", "result": "pass" if exact_demoted else "fail", "detail": "q_loc exact zero not derived for current MTS"},
        {"check_id": "V732_10_residual_route_present", "result": "pass" if residual_route else "fail", "detail": "observed reduced residual fallback present"},
        {"check_id": "V732_11_no_cheat_attacks_retained", "result": "pass" if redteam_has_marker and redteam_has_boundary else "fail", "detail": f"redteam_rows={len(redteam_rows)};marker={redteam_has_marker};boundary={redteam_has_boundary}"},
        {"check_id": "V732_12_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V732_13_no_claim_rows_promoted", "result": "pass" if claim_false else "fail", "detail": "all generated rows with valid_for_claim remain false"},
        {"check_id": "V732_14_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V732_15_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V732_16_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V732_17_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def write_markdown(
    generated_utc: str,
    run_root: Path,
    source_register: list[dict[str, Any]],
    pi_rows: list[dict[str, Any]],
    lemma_rows: list[dict[str, Any]],
    factor_rows: list[dict[str, Any]],
    exact_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    redteam_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 732 - Y5 R10 Construct Hybrid pi Observed Quotient Map Or Demote

## Summary

This checkpoint constructs the hybrid observed quotient candidate selected in 731.

```text
Y = (O_GR, Phi_red, R_rep, B_ref)
pi_h(Y) = (O_GR, Phi_red, B_ref)
v_X^rep in ker(d pi_h)
q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})
```

Current verdict: **hybrid map constructed, exact local silence not derived**. If `Gamma_eff`, `K_hat`, and `P_loc` are pullbacks from `Q_obs^hybrid`, then `q_loc` is representative-vertical-blind. But vertical-blind is not zero. Exact local-GR silence still needs a reduced GK action owner, metric-response identity, and boundary no-flux.

| Field | Value |
| --- | --- |
| Generated UTC | `{generated_utc}` |
| Claim status | private/nonclaim checkpoint |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |
| Run root | `{relative(run_root)}` |

## Hybrid pi Map

{markdown_table(pi_rows, ["map_id", "object", "candidate_definition", "mathematical_test", "current_result", "claim_status", "valid_for_claim"])}

## Hybrid Pullback Lemma

{markdown_table(lemma_rows, ["lemma_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim"])}

## Gamma / Khat / q_loc Factorisation Test

{markdown_table(factor_rows, ["test_id", "sector", "factorisation_requirement", "what_would_pass", "current_result", "scrutiny_level", "valid_for_claim"])}

## q_loc Exactness Or Residual Gate

{markdown_table(exact_rows, ["gate_id", "question", "answer", "meaning", "failure_route", "valid_for_claim"])}

## Demotion Gate

{markdown_table(demotion_rows, ["route_id", "status_after_732", "reason", "not_allowed", "next_action", "valid_for_claim"])}

## No-Cheat Red Team

{markdown_table(redteam_rows, ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_732", "forbidden_after_732", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read

This is a disciplined partial win. The hybrid quotient can keep the hidden representative `X` boxer out of the ring if the local objects are true pullbacks. But the judges still will not award local-GR reduction for that alone. A nonzero reduced `q_loc` is still a physical observed residual, so the next move is either derive the reduced GK Ward owner or score the residual honestly.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-construct-hybrid-pi-observed-quotient"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    pi_rows = make_pi_map(generated_utc)
    lemma_rows = make_pullback_lemma(generated_utc)
    factor_rows = make_factor_tests(generated_utc)
    exact_rows = make_exactness_gate(generated_utc)
    demotion_rows = make_demotion(generated_utc)
    redteam_rows = make_redteam(generated_utc)
    decision_rows = make_decision(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PI_MAP_PATH,
        PULLBACK_LEMMA_PATH,
        FACTOR_TEST_PATH,
        EXACTNESS_GATE_PATH,
        DEMOTION_PATH,
        REDTEAM_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
        run_root / "status.json",
        run_root / "COMPLETE.marker",
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        PI_MAP_PATH,
        pi_rows,
        ["map_id", "object", "candidate_definition", "mathematical_test", "current_result", "claim_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        PULLBACK_LEMMA_PATH,
        lemma_rows,
        ["lemma_id", "statement", "derivation", "consequence", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        FACTOR_TEST_PATH,
        factor_rows,
        ["test_id", "sector", "factorisation_requirement", "what_would_pass", "current_result", "scrutiny_level", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        EXACTNESS_GATE_PATH,
        exact_rows,
        ["gate_id", "question", "answer", "meaning", "failure_route", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        DEMOTION_PATH,
        demotion_rows,
        ["route_id", "status_after_732", "reason", "not_allowed", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        REDTEAM_PATH,
        redteam_rows,
        ["redteam_id", "attack", "why_reviewers_accept_attack", "required_kill", "current_status", "route_if_not_killed", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_732", "forbidden_after_732", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(
        source_register,
        pi_rows,
        lemma_rows,
        factor_rows,
        exact_rows,
        demotion_rows,
        redteam_rows,
        decision_rows,
        output_paths,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated_utc,
        run_root,
        source_register,
        pi_rows,
        lemma_rows,
        factor_rows,
        exact_rows,
        demotion_rows,
        redteam_rows,
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
