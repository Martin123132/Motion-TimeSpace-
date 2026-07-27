from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "742-Y5-R10-observed-tau-owner-or-q_loc-free-coefficient-pack.md"
NEXT_TARGET = "743-Y5-R10-first-q_loc-free-coefficient-row-or-tau-component-zero.md"
STATUS = "Y5_R10_742_observed_tau_owner_rejected_for_current_chain_q_loc_free_coefficient_pack_activated_nonclaim"
CLAIM_CEILING = "observed_tau_owner_failed_current_chain_q_loc_free_coefficients_template_only_no_q_loc_bound_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_742_SOURCE_REGISTER.csv"
TAU_OWNER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv"
TAU_PROOF_PATH = RESIDUALS / "P8_Y5_R10_742_TAU_PROOF_VERDICT.csv"
FREE_PACK_PATH = RESIDUALS / "P8_Y5_R10_742_QLOC_FREE_COEFFICIENT_PACK.csv"
TAU_CQ_LINK_PATH = RESIDUALS / "P8_Y5_R10_742_EPSILON_TAU_TO_CQ_LINK.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_742_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_742_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_742_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_742_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_742_VALIDATION.csv"

FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES: dict[str, dict[str, Any]] = {
    "741_doc": {
        "path": POST_CHECKPOINT / "741-Y5-R10-Cqmu-parent-owner-or-compact-shell-unit-map.md",
        "needles": [OUTPUT_DOC.name, "C_qmu=N_M tau_mu", "free coefficient pack"],
        "role": "immediate Cqmu/tau handoff",
    },
    "741_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_741_VALIDATION.csv",
        "needles": ["V741_11_next_target_selected", "V741_13_formalization_workbench_untouched", "V741_14_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "741_owner_fork": {
        "path": RESIDUALS / "P8_Y5_R10_741_CQMU_OWNER_FORK.csv",
        "needles": ["CQM741_0_parent_tau_contraction", "C_qnu=N_M tau_nu", "CQM741_3_free_projection_coefficient"],
        "role": "Cqmu owner fork",
    },
    "741_free_pack": {
        "path": RESIDUALS / "P8_Y5_R10_741_FREE_COEFFICIENT_PACK_QUEUE.csv",
        "needles": ["FCQ741_0_Cq_scalar_mass", "c_qM", "template_only"],
        "role": "prior free coefficient pack queue",
    },
    "684_tau_audit": {
        "path": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "needles": ["TGA684_6_total", "NO_PARENT_SIGNED_TAU_LOCK", "blocked_nonclaim"],
        "role": "tau role audit",
    },
    "685_contract": {
        "path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_6_verdict", "tau_source=tau_charge=tau_clock", "blocked_nonclaim"],
        "role": "tau generator contract",
    },
    "685_gate": {
        "path": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        "needles": ["KCG685_0_observed_vector", "MISSING_PARENT_SELECTED_TAU_OBS", "KCG685_7_total"],
        "role": "Killing/clock/tau gate",
    },
    "686_identity": {
        "path": RESIDUALS / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
        "needles": ["KIA686_1_Killing_zero", "KIA686_2_current_MTS_gap", "KIA686_3_residual_definition"],
        "role": "Killing current identity and fallback",
    },
    "686_residual": {
        "path": RESIDUALS / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
        "needles": ["NTR686_0_epsilon_nonstationary_tau", "M_ref_candidate", "MISSING_STATIONARY_KILLING_CERTIFICATE_OR_SOURCE_BACKED_BOUND"],
        "role": "nonstationary tau residual row",
    },
    "687_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv",
        "needles": ["OBS687_1_trace_not_Killing", "OBS687_2_domain_not_clock", "OBS687_5_denominator_open"],
        "role": "stationarity obstruction ledger",
    },
    "688_decomposition": {
        "path": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        "needles": ["SGT688_0_exact_congruence_identity", "SGT688_8_verdict", "MISSING_ALL_COMPONENT_SOURCE_PACK_OR_ZERO_THEOREMS"],
        "role": "symgrad tau decomposition",
    },
    "688_input_template": {
        "path": RESIDUALS / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
        "needles": ["CSI688_5_tau_mismatch", "CSI688_7_denominator", "MISSING_CLAIM_READY_M_REF_CANDIDATE"],
        "role": "component input template",
    },
    "688_num_denom": {
        "path": RESIDUALS / "P8_Y5_R10_688_NUMERATOR_DENOMINATOR_MAP.csv",
        "needles": ["NDM688_2_dimensionless_epsilon", "MISSING_CLAIM_READY_DENOMINATOR", "NDM688_3_claim_acceptance"],
        "role": "epsilon tau numerator/denominator map",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > FORMALIZATION_CUTOFF:
                count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCES.items():
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_string(path.exists()),
                "needle_check": bool_string(text_contains(path, spec["needles"])),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def tau_owner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "TOA742_0_same_tau_roles",
            "target": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "required_theorem": "one parent-selected observed generator appears before readout in source variation, Hamiltonian charge, clock normalization, orbit readout, and boundary reference",
            "prior_evidence": "684/685 keep the total tau lock blocked_nonclaim",
            "current_verdict": "not_parent_owned",
            "missing": "NO_PARENT_SIGNED_TAU_LOCK; MISSING_PARENT_SELECTED_TAU_OBS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TOA742_1_Killing_stationarity",
            "target": "nabla_(mu tau_nu)=0 or admissible stationary Hamiltonian generator",
            "required_theorem": "local compact exterior is stationary/Killing in the observed metric with fixed clock normalization",
            "prior_evidence": "686 identity is exact but current MTS gap remains; 687 rejects selector-to-Killing upgrade",
            "current_verdict": "not_derived",
            "missing": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE; MISSING_SYMGRAD_TAU_AND_STRESS_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TOA742_2_Hamiltonian_integrability",
            "target": "delta H_tau finite/integrable/reference-subtracted",
            "required_theorem": "H_tau and H_ref are parent boundary objects with no source-dependent reference drift",
            "prior_evidence": "685 gate keeps integrable charge and reference lock failed",
            "current_verdict": "not_derived",
            "missing": "MISSING_INTEGRABLE_CHARGE_AND_REFERENCE_LOCK; MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TOA742_3_denominator",
            "target": "M_ref_candidate or M_H_ref",
            "required_theorem": "same-frame denominator has mass/energy units and is valid before q_loc coefficient scoring",
            "prior_evidence": "688 denominator row remains MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "current_verdict": "not_claim_ready",
            "missing": "MISSING_CLAIM_READY_DENOMINATOR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "TOA742_4_owner_verdict",
            "target": "C_qnu=N_M tau_nu",
            "required_theorem": "tau and N_M are parent-owned and not chosen after readout",
            "prior_evidence": "741 identifies the route but keeps it conditional",
            "current_verdict": "rejected_for_current_claim",
            "missing": "tau owner, N_M units, M_eff_ref, no-readout proof, tau.q_loc theorem or bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def tau_proof_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "TPV742_0_clean_identity",
            "claim": "Killing tau would close the tau-current leakage",
            "formula": "nabla_mu(T_H^{mu nu}tau_nu)=tau_nu nabla_mu T_H^{mu nu}+T_H^{mu nu}nabla_(mu tau_nu)",
            "status": "conditional_identity_accepted",
            "claim_effect": "mathematically clean if same-frame Hilbert conservation and Killing tau are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "TPV742_1_current_tau_zero",
            "claim": "current MTS proves symgrad(tau)=0",
            "formula": "nabla_(mu tau_nu)=0",
            "status": "rejected_current_chain",
            "claim_effect": "epsilon_nonstationary_tau remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "TPV742_2_selector_shortcut",
            "claim": "domain/selector silence proves Killing stationarity",
            "formula": "A_D=0 or theta_D=0 => symgrad(tau)=0",
            "status": "rejected_counterexamples_retained",
            "claim_effect": "shear, lapse, shift, boundary motion, tau mismatch, stress, and denominator components remain",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "TPV742_3_tau_owner_result",
            "claim": "observed tau can be used to derive C_qmu now",
            "formula": "C_qmu=N_M tau_mu",
            "status": "blocked_nonclaim",
            "claim_effect": "Cqmu remains a coefficient target, not a derived coupling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def free_pack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "QFC742_0_scalar_mass",
            "target_row": "Y5B_9_q_loc_projection",
            "coefficient": "c_qM",
            "formula": "epsilon_q_loc_Y5=abs(c_qM*q_proxy)",
            "required_inputs": "c_qM;units;q_proxy;M_eff_ref_or_denominator;source_file;prior_or_derivation;no_cancellation_flag",
            "current_status": "activated_template_not_filled",
            "claim_gate": "valid_for_claim only after coefficient and denominator are source-backed and compared to a specific Y5/local bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "QFC742_1_time_drift",
            "target_row": "Y5B_0/Y5B_1/R9_Gdot",
            "coefficient": "c_qt",
            "formula": "dln_mu_dt|_q=c_qt*q_proxy/Delta_t",
            "required_inputs": "c_qt;Delta_t;time_profile;units_yr^-1;Gdot_bound;source_file;no_cancellation_flag",
            "current_status": "activated_template_not_filled",
            "claim_gate": "requires a time profile; static q_proxy alone cannot score Gdot/Mdot",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "QFC742_2_R10_range",
            "target_row": "R10_fifth_force",
            "coefficient": "c_q_alpha(lambda)",
            "formula": "alpha_q_loc(lambda)=c_q_alpha(lambda)*q_proxy",
            "required_inputs": "lambda;alpha_predicted;alpha_bound;real_curve_source;c_q_alpha_source;no_cancellation_flag",
            "current_status": "activated_template_not_filled",
            "claim_gate": "requires full alpha(lambda) curve or theorem-zero range proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "QFC742_3_PPN_vector",
            "target_row": "Y5B_8/R3-R8",
            "coefficient": "c_q_PPN_vector",
            "formula": "Delta_PPN_q=c_q_PPN_vector*q_proxy",
            "required_inputs": "component;coefficient;units;PPN_bound;weak_field_map;source_file;no_cancellation_flag",
            "current_status": "activated_template_not_filled",
            "claim_gate": "each PPN component must pass separately with no total-vector cancellation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "QFC742_4_tau_mismatch",
            "target_row": "epsilon_nonstationary_tau",
            "coefficient": "c_tau_q",
            "formula": "epsilon_tau_to_q <= c_tau_q * epsilon_nonstationary_tau",
            "required_inputs": "epsilon_nonstationary_tau;component_bounds;M_ref_candidate;c_tau_q;source_file;no_cancellation_flag",
            "current_status": "activated_template_not_filled",
            "claim_gate": "requires the 688 component pack and denominator to stop carrying MISSING markers",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def tau_cq_link_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "link_id": "TQL742_0_if_tau_succeeds",
            "condition": "parent-owned observed tau and N_M",
            "effect_on_Cq": "C_qmu=N_M tau_mu becomes a derivation candidate",
            "effect_on_q_loc": "q_loc mass projection can be tested through tau.q_loc or tau-orthogonality",
            "current_status": "condition_failed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "link_id": "TQL742_1_if_tau_nonstationary",
            "condition": "symgrad(tau) nonzero or unbounded",
            "effect_on_Cq": "C_q remains free/retained coefficient",
            "effect_on_q_loc": "epsilon_q_loc must include tau-role mismatch or nonstationarity coefficient rows",
            "current_status": "active_fallback",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "link_id": "TQL742_2_if_denominator_missing",
            "condition": "M_ref_candidate invalid",
            "effect_on_Cq": "no dimensionless q_loc bound can be claim-grade",
            "effect_on_q_loc": "compact-shell proxy stays breadcrumb only",
            "current_status": "active_blocker",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R742_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_742": "tau_owner_failed_free_coeff_pack_activated",
            "zero_or_input": "C_qmu=N_M tau_mu not derived; q_loc coefficients c_qM,c_qt,c_q_alpha,c_q_PPN queued",
            "still_missing": "source-backed coefficient values, denominator, unit map, q_proxy equivalence, arena bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R742_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_742": "tau_nonstationarity_residual_retained",
            "zero_or_input": "epsilon_nonstationary_tau remains numerator/denominator residual",
            "still_missing": "symgrad component source pack and M_ref_candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R742_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_742": "q_loc_channel_open_as_free_coefficients",
            "zero_or_input": "q_loc stays separate no-cancellation channel in mu_extra envelope",
            "still_missing": "first source-backed q_loc coefficient row or theorem-zero tau/q_loc branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D742_0_tau_owner",
            "decision": "reject observed tau parent-owner for current claim",
            "meaning": "the old tau trail blocks same-tau roles, Killing stationarity, Hamiltonian integrability, reference lock, and denominator",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D742_1_Cqmu",
            "decision": "do not derive C_qmu=N_M tau_mu yet",
            "meaning": "Cqmu remains a clean target but not an owned coupling",
            "claim_status": "conditional_route_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D742_2_free_pack",
            "decision": "activate q_loc free-coefficient pack",
            "meaning": "since tau owner fails, the non-cheat route is explicit coefficients with units and no-cancellation gates",
            "claim_status": "template_only_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D742_3_next",
            "decision": "try first q_loc coefficient row or tau component zero",
            "meaning": "next work should either fill one coefficient row honestly or derive one component theorem-zero from the symgrad-tau pack",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU742_0_allowed",
            "allowed_after_742": "say tau-owner route failed for current chain and why",
            "forbidden_after_742": "say tau_obs or Cqmu is parent-owned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU742_1_allowed",
            "allowed_after_742": "use q_loc free-coefficient templates as falsifiable residual rows",
            "forbidden_after_742": "score template coefficients or use cancellation between rows",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU742_2_allowed",
            "allowed_after_742": "derive a tau component zero if possible before filling coefficients",
            "forbidden_after_742": "use selector silence or trace zero as full Killing stationarity",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "observed tau owner rejected for current chain; q_loc free coefficient pack activated as the honest fallback",
            "hard_blocker": "same tau roles, Killing stationarity, Hamiltonian integrability, boundary reference, denominator, and symgrad-tau component pack remain unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    tau_owner: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    free_pack: list[dict[str, Any]],
    link_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V742_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V742_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_741_VALIDATION.csv")
    validation.append({"check_id": "V742_2_prior_741_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "741 validation has no failures"})
    validation.append({"check_id": "V742_3_741_selected_742", "result": "pass" if text_contains(SOURCES["741_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name})
    validation.append({"check_id": "V742_4_tau_owner_rows_complete", "result": "pass" if len(tau_owner) == 5 else "fail", "detail": f"tau_owner_rows={len(tau_owner)}"})
    validation.append({"check_id": "V742_5_tau_owner_rejected", "result": "pass" if any(row["current_verdict"] == "rejected_for_current_claim" for row in tau_owner) else "fail", "detail": "Cq/tau owner not promoted"})
    validation.append({"check_id": "V742_6_Killing_shortcut_rejected", "result": "pass" if any(row["status"] == "rejected_counterexamples_retained" for row in proof) else "fail", "detail": "selector/trace shortcut rejected"})
    validation.append({"check_id": "V742_7_free_pack_activated", "result": "pass" if len(free_pack) == 5 and all(row["current_status"] == "activated_template_not_filled" for row in free_pack) else "fail", "detail": f"free_pack_rows={len(free_pack)}"})
    validation.append({"check_id": "V742_8_tau_Cq_link_blocked", "result": "pass" if any(row["current_status"] == "active_blocker" for row in link_rows) else "fail", "detail": "denominator/tau link blocker retained"})
    validation.append({"check_id": "V742_9_Y5_rows_retained", "result": "pass" if {"Y5R742_9_q_loc_projection", "Y5R742_5_extra_mass_projection"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "q_loc and extra mass rows retained"})
    all_rows = tau_owner + proof + free_pack + link_rows + y5_update + decisions
    validation.append({"check_id": "V742_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V742_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V742_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V742_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V742_14_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V742_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    tau_owner: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    free_pack: list[dict[str, Any]],
    link_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 742 - Y5 R10 Observed Tau Owner Or q_loc Free Coefficient Pack

Start point: 741 found the clean coupling candidate:

```text
C_qmu = N_M tau_mu
```

Current verdict: **observed `tau` is not parent-owned for the current chain**. The Killing identity is real, but the package needed to use it is not derived: same tau roles, stationary/Killing branch, Hamiltonian integrability, boundary reference, denominator, and symgrad-tau component zeros all remain unsigned.

So `q_loc` must fall back to explicit free coefficient rows until one tau component is genuinely zeroed or sourced.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | tau owner rejected for current chain; q_loc free coefficient pack activated |
| Next target | `{NEXT_TARGET}` |

## Observed Tau Owner Audit

{markdown_table(tau_owner, ["audit_id", "target", "required_theorem", "prior_evidence", "current_verdict", "missing", "valid_for_claim"])}

## Tau Proof Verdict

{markdown_table(proof, ["proof_id", "claim", "formula", "status", "claim_effect", "valid_for_claim"])}

## q_loc Free Coefficient Pack

{markdown_table(free_pack, ["pack_id", "target_row", "coefficient", "formula", "required_inputs", "current_status", "claim_gate", "valid_for_claim"])}

## Tau-to-Cq Link

{markdown_table(link_rows, ["link_id", "condition", "effect_on_Cq", "effect_on_q_loc", "current_status", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_742", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_742", "forbidden_after_742", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the coupling bottleneck showing its teeth. The pretty route is still pretty: if one parent-selected `tau` controls source, charge, clock, orbit, and boundary reference, then `C_qmu=N_M tau_mu` is exactly the right shape. But the older tau audit already blocks that route, and 742 carries that verdict forward rather than laundering it. The next honest move is either one small tau-component zero theorem, or the first real q_loc coefficient row with units and a bound. No magic mask; no mystery GM.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    tau_owner = tau_owner_rows(generated_utc)
    proof = tau_proof_rows(generated_utc)
    free_pack = free_pack_rows(generated_utc)
    link_rows = tau_cq_link_rows(generated_utc)
    y5_update = y5_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        TAU_OWNER_AUDIT_PATH,
        TAU_PROOF_PATH,
        FREE_PACK_PATH,
        TAU_CQ_LINK_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, tau_owner, proof, free_pack, link_rows, y5_update, decisions, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TAU_OWNER_AUDIT_PATH, tau_owner, ["audit_id", "target", "required_theorem", "prior_evidence", "current_verdict", "missing", "valid_for_claim", "generated_utc"])
    write_csv(TAU_PROOF_PATH, proof, ["proof_id", "claim", "formula", "status", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(FREE_PACK_PATH, free_pack, ["pack_id", "target_row", "coefficient", "formula", "required_inputs", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(TAU_CQ_LINK_PATH, link_rows, ["link_id", "condition", "effect_on_Cq", "effect_on_q_loc", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_742", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_742", "forbidden_after_742", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, tau_owner, proof, free_pack, link_rows, y5_update, decisions, routes, summary, validation)

    print(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "next_target": NEXT_TARGET,
                "doc": str(OUTPUT_DOC),
                "validation": str(VALIDATION_PATH),
                "all_validation_pass": all(row["result"] == "pass" for row in validation),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
