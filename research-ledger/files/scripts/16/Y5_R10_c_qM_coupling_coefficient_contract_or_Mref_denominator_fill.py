from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "744-Y5-R10-c_qM-coupling-coefficient-contract-or-Mref-denominator-fill.md"
NEXT_TARGET = "745-Y5-R10-c_qM-engineering-smoke-row-or-source-backed-Mref-hunt.md"
STATUS = "Y5_R10_744_cqM_operator_norm_contract_written_Mref_claim_denominator_still_blocked_nonclaim"
CLAIM_CEILING = "cqM_contract_and_denominator_audit_only_no_numeric_q_loc_score_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"
Q_PROXY_VALUE = "7.432631961576971e-06"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_744_SOURCE_REGISTER.csv"
CQM_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_744_CQM_COUPLING_CONTRACT.csv"
MREF_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_744_MREF_DENOMINATOR_FILL_ATTEMPT.csv"
SCALAR_ROW_PATH = RESIDUALS / "P8_Y5_R10_744_SCALAR_MASS_ROW_STATUS.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_744_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_744_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_744_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_744_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_744_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "743_doc": {
        "path": POST_CHECKPOINT / "743-Y5-R10-first-q_loc-free-coefficient-row-or-tau-component-zero.md",
        "needles": ["QCR743_1_c_qM_scalar_mass", "blocked_not_filled", "744-Y5-R10-c_qM-coupling-coefficient-contract-or-Mref-denominator-fill.md"],
        "role": "immediate c_qM/Mref handoff",
    },
    "743_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_743_VALIDATION.csv",
        "needles": ["V743_7_cqM_not_filled", "V743_14_formalization_workbench_untouched", "V743_15_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "743_coeff_row": {
        "path": RESIDUALS / "P8_Y5_R10_743_QLOC_COEFFICIENT_ROW_ATTEMPT.csv",
        "needles": ["QCR743_1_c_qM_scalar_mass", Q_PROXY_VALUE, "C_qmu normalization"],
        "role": "c_qM blocked row",
    },
    "740_mass_map": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_MASS_CHANNEL_MAP.csv",
        "needles": ["QMM740_0_define_mass_channel", "I_q[A]=int_A C_{q nu} q_loc^nu dV", "fallback_ready_not_scored"],
        "role": "q_loc mass-channel identity",
    },
    "741_owner_fork": {
        "path": RESIDUALS / "P8_Y5_R10_741_CQMU_OWNER_FORK.csv",
        "needles": ["CQM741_0_parent_tau_contraction", "C_qnu=N_M tau_nu", "best_conditional_route_not_current_derived"],
        "role": "Cqmu owner candidate and blocker",
    },
    "742_tau_owner": {
        "path": RESIDUALS / "P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv",
        "needles": ["TOA742_4_owner_verdict", "rejected_for_current_claim", "tau owner"],
        "role": "tau owner rejection",
    },
    "683_MHref": {
        "path": RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
        "needles": ["MH683_0_definition", "GM_orbit / G_ref", "blocked_nonclaim"],
        "role": "M_H_ref denominator attempt",
    },
    "696_MHref_audit": {
        "path": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
        "needles": ["MHA696_6_verdict", "fail_current_corpus", "M_H_ref remains unfilled"],
        "role": "M_H_ref denominator audit",
    },
    "697_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv",
        "needles": ["SNC697_9_verdict", "fail_current_corpus", "denominator fill row remains unfilled"],
        "role": "M_H_ref source-normalization certificate failure",
    },
    "698_bridge": {
        "path": RESIDUALS / "P8_Y5_R10_698_PG_MHREF_BRIDGE_THEOREM_ATTEMPT.csv",
        "needles": ["BT698_8_MHref_calibration", "fail_current_corpus", "GM_orbit=G_ref M_H_ref"],
        "role": "Poisson/Gauss/MHref bridge attempt",
    },
    "Y5_bound_input": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "needles": ["Y5B_9_q_loc_projection", "mixed_until_projection_fixed", "fill_q_loc_to_mu_projection_operator"],
        "role": "Y5 source-normalization q_loc row",
    },
    "Y5_owner_theorem": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "needles": ["Y5O_8_owner_theorem", "theorem_written_current_MTS_does_not_satisfy_premises", "mu_obs = G0 M_H"],
        "role": "source-normalization owner theorem",
    },
    "Y5_amplitude_law": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_AMPLITUDE_LAW.csv",
        "needles": ["AL518_0_source_split", "epsilon_mu := mu_extra/(G_eff M_H)", "bound_runner_policy"],
        "role": "source-normalization amplitude law",
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
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def cqm_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CQM744_0_operator_norm_definition",
            "clause": "c_qM is an operator norm, not a fitted scalar",
            "mathematical_form": "c_qM[A] := (1/M_ref) sup_{q!=0} |int_A C_{q nu} q^nu dV| / q_proxy",
            "required_inputs": "domain A; measure dV; C_qnu; q_proxy definition; M_ref; units",
            "current_status": "contract_written_no_value",
            "claim_effect": "prevents scoring compact-shell q_proxy directly as a mass fraction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CQM744_1_Cqmu_owner",
            "clause": "C_qnu must be parent-owned before coefficient scoring",
            "mathematical_form": "preferred route C_qnu=N_M tau_nu only if tau and N_M are parent-selected",
            "required_inputs": "tau owner; N_M units; no-readout proof; C_q not chosen after fit",
            "current_status": "blocked_by_741_742",
            "claim_effect": "no c_qM value can be inferred from tau contraction yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CQM744_2_denominator_lock",
            "clause": "M_ref must be same-frame and positive",
            "mathematical_form": "epsilon_q_loc=|I_q[A]|/M_ref",
            "required_inputs": "M_H_ref or explicitly labelled engineering M_ref; same source/clock/metric/boundary frame; positivity; anti-circularity guard",
            "current_status": "claim_MHref_blocked_engineering_candidate_allowed_only_for_smoke",
            "claim_effect": "denominator laundering through observed GM is forbidden for claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CQM744_3_unit_map",
            "clause": "q_proxy must be converted into the same units as I_q",
            "mathematical_form": f"q_proxy={Q_PROXY_VALUE} is dimensionless_proxy, not source-mass units",
            "required_inputs": "profile normalization; shell/domain volume; C_q units; relation to P_loc d_rel J_rel",
            "current_status": "missing_unit_map",
            "claim_effect": "q_proxy remains a breadcrumb, not a local bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CQM744_4_no_cancellation_gate",
            "clause": "q_loc channel must pass independently",
            "mathematical_form": "|epsilon_extra| <= sum_i |epsilon_i| and epsilon_q_loc is one separate epsilon_i",
            "required_inputs": "absolute channel row; no_cancellation_flag=true; arena-specific bound",
            "current_status": "policy_active",
            "claim_effect": "q_loc cannot be hidden behind boundary/projector/coupling residuals",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CQM744_5_acceptance_rule",
            "clause": "first claim-grade c_qM row",
            "mathematical_form": "valid_for_claim=true only if c_qM numeric or theorem-zero, M_ref valid, source paths real, units compatible, and |c_qM q_proxy| <= bound",
            "required_inputs": "CQM744_0 through CQM744_4 plus Y5/PPN/R10 arena lock",
            "current_status": "not_satisfied",
            "claim_effect": "no numeric q_loc score or local claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def mref_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "MRF744_0_claim_denominator",
            "target": "M_H_ref",
            "candidate": "M_H_ref := H_tau[S_link]-H_ref",
            "status": "blocked_current_chain",
            "blocker": "integrable charge, fixed reference, tau lock, same frame, positivity, and Poisson/Gauss/orbit bridge remain unsigned",
            "allowed_use": "denominator target only",
            "forbidden_use": "claim-grade q_loc/Y5/R10/PPN denominator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "MRF744_1_empirical_engineering_denominator",
            "target": "M_ref_eng",
            "candidate": "M_ref_eng := GM_orbit/G_ref",
            "status": "allowed_only_as_private_smoke_denominator",
            "blocker": "using orbital GM as source mass is circular until PG/MHref bridge is derived",
            "allowed_use": "nonclaim engineering smoke row labelled empirical_readout_denominator",
            "forbidden_use": "derivation of Newton/local GR or claim-valid c_qM",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "MRF744_2_positive_same_frame_guard",
            "target": "M_ref > 0 in one observed frame",
            "candidate": "same-frame positive denominator certificate",
            "status": "missing",
            "blocker": "same coframe/source/clock/boundary certificate and source-independent reference subtraction are not signed",
            "allowed_use": "schema guard",
            "forbidden_use": "division by assumed positive M_H_ref",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "MRF744_3_anti_circularity",
            "target": "no Newton borrowed to prove Newton",
            "candidate": "GM_orbit/G_ref legal after H_tau -> Poisson/Gauss -> orbit is derived in that order",
            "status": "rule_retained",
            "blocker": "BT698 bridge fails current corpus",
            "allowed_use": "quarantine engineering smoke from derivation claims",
            "forbidden_use": "backfilling source charge from Kepler readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "MRF744_4_verdict",
            "target": "first denominator fill",
            "candidate": "claim M_H_ref or smoke M_ref_eng",
            "status": "claim_fill_failed_smoke_candidate_staged",
            "blocker": "claim denominator remains absent; engineering denominator needs explicit quarantine row next",
            "allowed_use": NEXT_TARGET,
            "forbidden_use": "local arena pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def scalar_row_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SMR744_0_cqM_contract_status",
            "target": "Y5B_9_q_loc_projection",
            "formula": "epsilon_q_loc_Y5=abs(c_qM*q_proxy)",
            "known": f"q_proxy={Q_PROXY_VALUE}; c_qM contract defined as operator norm",
            "missing": "numeric/theorem c_qM; M_ref; unit map; arena bound",
            "row_status": "contract_ready_value_blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "SMR744_1_theorem_zero_option",
            "target": "c_qM=0",
            "formula": "int_A C_qnu q_loc^nu dV=0 for all admissible q_loc",
            "known": "would follow from parent-owned C_q orthogonal to q_loc or q_loc exact zero",
            "missing": "tau/Cq owner and observed q_loc orthogonality theorem",
            "row_status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "SMR744_2_bound_option",
            "target": "finite c_qM bound",
            "formula": "abs(c_qM*q_proxy)<=Y5_or_arena_bound",
            "known": "compact-shell proxy is numeric",
            "missing": "C_q units and denominator before comparison to any arena lock",
            "row_status": "not_scoreable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "SMR744_3_next_smoke_schema",
            "target": "private engineering smoke row",
            "formula": "epsilon_q_loc_smoke=abs(c_qM_smoke*q_proxy) using M_ref_eng quarantine",
            "known": "allowed only as labelled empirical denominator test",
            "missing": "selected system/arena, G_ref convention, c_qM_smoke source/assumption, no-claim flag",
            "row_status": "queued_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R744_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_744": "c_qM_contract_written_value_blocked",
            "zero_or_input": "c_qM must be operator norm of C_q acting on q_loc divided by M_ref",
            "still_missing": "C_q owner; unit map; M_H_ref or quarantined M_ref_eng; arena comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R744_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_744": "q_loc_remains_separate_channel",
            "zero_or_input": "no-cancellation channel survives; no direct q_proxy score",
            "still_missing": "source-backed c_qM row or exact orthogonality theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R744_MHref",
            "source_row": "M_H_ref denominator",
            "status_after_744": "claim_denominator_blocked_smoke_denominator_queued",
            "zero_or_input": "GM_orbit/G_ref may be used only as empirical_readout_denominator in private smoke",
            "still_missing": "integrable Hamiltonian charge; tau lock; same frame; PG bridge; positivity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D744_0_cqM_contract",
            "decision": "define c_qM as an operator-norm contract",
            "meaning": "c_qM is now mathematically specified without pretending the value is known",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D744_1_MHref",
            "decision": "do not fill claim M_H_ref",
            "meaning": "older denominator audits still block integrability, same-frame, positivity, and PG/orbit bridge",
            "claim_status": "blocked_current_chain",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D744_2_smoke_denominator",
            "decision": "allow GM_orbit/G_ref only as quarantined smoke denominator",
            "meaning": "useful for private testing but not a derivation, not a GitHub/journal claim",
            "claim_status": "engineering_smoke_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D744_3_next",
            "decision": "build first quarantined smoke row or source-backed Mref hunt",
            "meaning": "now the next step can either quantify a nonclaim c_qM smoke envelope or hunt a real source-backed denominator",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU744_0_allowed",
            "allowed_after_744": "say c_qM has a precise operator-norm contract",
            "forbidden_after_744": "say c_qM is numerically filled or q_loc passes Y5",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU744_1_allowed",
            "allowed_after_744": "use GM_orbit/G_ref only in a private empirical smoke row",
            "forbidden_after_744": "use observed GM as a derived source denominator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU744_2_allowed",
            "allowed_after_744": "keep q_loc in the no-cancellation extra-mass envelope",
            "forbidden_after_744": "cancel q_loc against boundary/projector/coupling channels",
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
            "main_result": "c_qM contract is now exact enough to stop coefficient laundering; claim M_H_ref remains blocked; GM_orbit/G_ref smoke route is quarantined",
            "hard_blocker": "C_q owner, M_H_ref denominator, unit map, and arena transfer remain unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    mref: list[dict[str, Any]],
    scalar_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_743_VALIDATION.csv")
    all_rows = contract + mref + scalar_rows + y5_update + decisions + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V744_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V744_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V744_2_prior_743_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "743 validation has no failures"})
    validation.append({"check_id": "V744_3_operator_norm_contract", "result": "pass" if any("sup_{q!=0}" in row["mathematical_form"] for row in contract) else "fail", "detail": "c_qM operator-norm contract written"})
    validation.append({"check_id": "V744_4_Cq_owner_blocked", "result": "pass" if any(row["current_status"] == "blocked_by_741_742" for row in contract) else "fail", "detail": "Cqmu owner not promoted"})
    validation.append({"check_id": "V744_5_MHref_claim_blocked", "result": "pass" if any(row["target"] == "M_H_ref" and row["status"] == "blocked_current_chain" for row in mref) else "fail", "detail": "claim M_H_ref remains blocked"})
    validation.append({"check_id": "V744_6_engineering_denominator_quarantined", "result": "pass" if any(row["target"] == "M_ref_eng" and row["status"] == "allowed_only_as_private_smoke_denominator" for row in mref) else "fail", "detail": "GM_orbit/G_ref is smoke-only"})
    validation.append({"check_id": "V744_7_q_proxy_not_scored", "result": "pass" if any(row["row_status"] == "not_scoreable" for row in scalar_rows) else "fail", "detail": f"q_proxy={Q_PROXY_VALUE} remains not scoreable"})
    validation.append({"check_id": "V744_8_scalar_row_contract_ready_value_blocked", "result": "pass" if any(row["row_status"] == "contract_ready_value_blocked" for row in scalar_rows) else "fail", "detail": "c_qM row has contract but no value"})
    validation.append({"check_id": "V744_9_Y5_rows_retained", "result": "pass" if {"Y5R744_9_q_loc_projection", "Y5R744_5_extra_mass_projection"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "q_loc and extra-mass Y5 rows retained"})
    validation.append({"check_id": "V744_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V744_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V744_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V744_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V744_14_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V744_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    mref: list[dict[str, Any]],
    scalar_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 744 - Y5 R10 c_qM Coupling Coefficient Contract Or Mref Denominator Fill

Start point: 743 proved a scoped tau-current pruning theorem, but left the first source-mass coefficient row blocked:

```text
epsilon_q_loc_Y5 = |c_qM q_proxy|
q_proxy = {Q_PROXY_VALUE}
```

Current result: **`c_qM` can now be stated exactly as a contract, but not filled as a number**. The honest definition is an operator norm:

```text
c_qM[A] := (1/M_ref) sup_{{q != 0}} |int_A C_qnu q^nu dV| / q_proxy
```

That is useful because it stops coefficient laundering. The compact-shell proxy cannot be scored directly; it needs `C_qnu`, units, domain, measure, and a same-frame denominator. Claim-grade `M_H_ref` still fails the old source-normalization certificate. The only denominator we can stage now is `M_ref_eng := GM_orbit/G_ref`, and that is quarantined as private engineering smoke only.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | c_qM operator-norm contract written; claim M_H_ref blocked; smoke denominator quarantined |
| Next target | `{NEXT_TARGET}` |

## c_qM Coupling Contract

{markdown_table(contract, ["contract_id", "clause", "mathematical_form", "required_inputs", "current_status", "claim_effect", "valid_for_claim"])}

## Mref Denominator Fill Attempt

{markdown_table(mref, ["attempt_id", "target", "candidate", "status", "blocker", "allowed_use", "forbidden_use", "valid_for_claim"])}

## Scalar Mass Row Status

{markdown_table(scalar_rows, ["row_id", "target", "formula", "known", "missing", "row_status", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_744", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_744", "forbidden_after_744", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is not a pass, but it is a useful tightening. `c_qM` is no longer a vague coupling knob; it has to be the norm of a specific projection operator divided by a specific source mass. That means the theory cannot hide behind “choose the coupling small.” Good. The grim bit is the same beast as before: `M_H_ref` is still not derivable in the current chain, so any numeric test must be quarantined as engineering smoke with `GM_orbit/G_ref`, not sold as derived local GR. The next move is to either run that quarantined smoke row cleanly or hunt a real source-backed denominator.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    contract = cqm_contract_rows(generated_utc)
    mref = mref_attempt_rows(generated_utc)
    scalar_rows = scalar_row_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        CQM_CONTRACT_PATH,
        MREF_ATTEMPT_PATH,
        SCALAR_ROW_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, contract, mref, scalar_rows, y5_update, decisions, routes, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CQM_CONTRACT_PATH, contract, ["contract_id", "clause", "mathematical_form", "required_inputs", "current_status", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(MREF_ATTEMPT_PATH, mref, ["attempt_id", "target", "candidate", "status", "blocker", "allowed_use", "forbidden_use", "valid_for_claim", "generated_utc"])
    write_csv(SCALAR_ROW_PATH, scalar_rows, ["row_id", "target", "formula", "known", "missing", "row_status", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_744", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_744", "forbidden_after_744", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, contract, mref, scalar_rows, y5_update, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote={OUTPUT_DOC}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
