from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "743-Y5-R10-first-q_loc-free-coefficient-row-or-tau-component-zero.md"
NEXT_TARGET = "744-Y5-R10-c_qM-coupling-coefficient-contract-or-Mref-denominator-fill.md"
STATUS = "Y5_R10_743_antisymmetric_tau_component_zeroed_but_q_loc_coefficients_unfilled_nonclaim"
CLAIM_CEILING = "skew_tau_pruning_only_no_Cqmu_no_q_loc_bound_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_743_SOURCE_REGISTER.csv"
TAU_COMPONENT_ZERO_PATH = RESIDUALS / "P8_Y5_R10_743_TAU_COMPONENT_ZERO_ATTEMPT.csv"
QLOC_COEFFICIENT_PATH = RESIDUALS / "P8_Y5_R10_743_QLOC_COEFFICIENT_ROW_ATTEMPT.csv"
PRUNING_RULE_PATH = RESIDUALS / "P8_Y5_R10_743_SKEW_TO_SYMGRAD_PRUNING_RULE.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_743_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_743_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_743_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_743_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_743_VALIDATION.csv"

FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)
Q_PROXY_VALUE = "7.432631961576971e-06"

SOURCES: dict[str, dict[str, Any]] = {
    "742_doc": {
        "path": POST_CHECKPOINT / "742-Y5-R10-observed-tau-owner-or-q_loc-free-coefficient-pack.md",
        "needles": ["observed `tau` is not parent-owned", "q_loc free coefficient pack", "743-Y5-R10-first-q_loc-free-coefficient-row-or-tau-component-zero.md"],
        "role": "immediate handoff to first coefficient row or component zero",
    },
    "742_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_742_VALIDATION.csv",
        "needles": ["V742_10_no_claim_rows_promoted", "V742_13_formalization_workbench_untouched", "V742_14_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "742_free_pack": {
        "path": RESIDUALS / "P8_Y5_R10_742_QLOC_FREE_COEFFICIENT_PACK.csv",
        "needles": ["QFC742_0_scalar_mass", "c_qM", "activated_template_not_filled"],
        "role": "q_loc coefficient templates",
    },
    "740_mass_map": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_MASS_CHANNEL_MAP.csv",
        "needles": ["QMM740_0_define_mass_channel", "C_{q nu} q_loc^nu", "fallback_ready_not_scored"],
        "role": "q_loc mass-channel identity and Cq blocker",
    },
    "740_bound_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv",
        "needles": [Q_PROXY_VALUE, "blocked_Cqmu_missing", "blocked_range_map_missing"],
        "role": "compact-shell q_proxy breadcrumb",
    },
    "q_loc_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": [Q_PROXY_VALUE, "needed_before_claim", "coefficient normalization"],
        "role": "older q_loc bound runner spec",
    },
    "734_hybrid_fill": {
        "path": RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv",
        "needles": ["HQR734_0_compact_shell_budget", "not_scoreable", "HQR734_6_representative_vertical_variation_zero"],
        "role": "hybrid q_loc runner filled rows and narrow zero",
    },
    "688_decomposition": {
        "path": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        "needles": ["vorticity drops from the symmetric part", "MISSING_ALL_COMPONENT_SOURCE_PACK_OR_ZERO_THEOREMS", "T_H_symgrad_tau_contraction"],
        "role": "symgrad tau decomposition and existing vorticity hint",
    },
    "688_num_denom": {
        "path": RESIDUALS / "P8_Y5_R10_688_NUMERATOR_DENOMINATOR_MAP.csv",
        "needles": ["epsilon_nonstationary_tau", "M_ref_candidate", "MISSING_CLAIM_READY_DENOMINATOR"],
        "role": "tau numerator/denominator blocker",
    },
    "689_zero_audit": {
        "path": RESIDUALS / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv",
        "needles": ["ZTA689_1_shear", "fail_current_corpus", "ZTA689_8_coefficients"],
        "role": "prior failed symgrad component-zero audit",
    },
    "690_shear_audit": {
        "path": RESIDUALS / "P8_Y5_R10_690_SHEAR_ZERO_THEOREM_AUDIT.csv",
        "needles": ["SZ690_0_projected_channel", "channel_silence_only", "theorem_zero_rejected"],
        "role": "projected-channel zero versus physical metric shear guard",
    },
    "739_channel_queue": {
        "path": RESIDUALS / "P8_Y5_R10_739_CHANNEL_BOUND_INPUT_QUEUE.csv",
        "needles": ["CBI739_4_q_loc_mass_projection", "C_qmu;q_loc_profile;units", "no_cancellation_flag"],
        "role": "extra-mass q_loc channel bound queue",
    },
    "Y5_source_norm": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "needles": ["Y5B_9_q_loc_projection", "C_qmu q_loc", "mixed_until_projection_fixed"],
        "role": "Y5 source-normalization q_loc row",
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


def tau_component_zero_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "TCZ743_0_skew_vorticity_silence",
            "component": "antisymmetric_part_of_nabla_tau",
            "candidate_theorem": "For symmetric Hilbert stress T_H^{mu nu}, T_H^{mu nu} nabla_[mu tau_nu]=0.",
            "derivation_status": "exact_algebraic_zero",
            "proof_sketch": "Contracting a symmetric tensor with an antisymmetric tensor gives zero: T^{mu nu}A_{mu nu}=1/2(T^{mu nu}-T^{nu mu})A_{mu nu}=0.",
            "what_it_prunes": "vorticity/skew derivative terms cannot enter the tau-current leakage numerator",
            "what_remains": "symgrad(tau), stress exchange, denominator, C_qmu, and q_loc mass projection remain open",
            "component_zero_established": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "TCZ743_1_symgrad_survivor",
            "component": "nabla_(mu tau_nu)",
            "candidate_theorem": "Promote skew silence into full tau-current closure",
            "derivation_status": "rejected_scope_error",
            "proof_sketch": "The exact identity leaves T_H^{mu nu}nabla_(mu tau_nu); skew silence does not remove trace, shear, lapse, shift, boundary, or tau-mismatch pieces.",
            "what_it_prunes": "nothing beyond the already-skew part",
            "what_remains": "all 688/689/690 symgrad component rows and M_ref_candidate",
            "component_zero_established": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "TCZ743_2_projected_channel_guard",
            "component": "projected_tracefree_shear_in_J_C",
            "candidate_theorem": "Use P_coh/Q_coh projected shear silence as metric shear zero",
            "derivation_status": "channel_zero_only_not_local_metric_zero",
            "proof_sketch": "690 allows projected scalar-channel silence, but rejects promotion to physical sigma_mu_nu=0 in the observed metric.",
            "what_it_prunes": "projected coherent scalar-current shear bookkeeping only",
            "what_remains": "physical metric shear and local Killing residual",
            "component_zero_established": "true_scoped_channel_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "TCZ743_3_verdict",
            "component": "epsilon_nonstationary_tau",
            "candidate_theorem": "Set epsilon_nonstationary_tau=0",
            "derivation_status": "blocked_nonclaim",
            "proof_sketch": "One exact skew zero is real, but the numerator was already symgrad/stress weighted. No full tau-current zero follows.",
            "what_it_prunes": "future runners should not carry vorticity as a live tau-current leakage bound",
            "what_remains": "B_trace, B_shear, B_lapse, B_shift, B_boundary, B_tau_mismatch, stress envelope, denominator",
            "component_zero_established": "partial_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qloc_coefficient_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QCR743_0_tau_skew_zero_row",
            "coefficient": "c_tau_q_skew",
            "target": "epsilon_tau_to_q skew/vorticity contribution",
            "formula": "epsilon_tau_skew_to_q=0",
            "known_input": "TCZ743_0 exact algebraic zero",
            "missing_input": "none for the skew subcomponent, but this is not the q_loc mass/source coefficient",
            "row_status": "filled_theorem_zero_subcomponent",
            "numeric_or_symbolic": "0",
            "no_cancellation_flag": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "QCR743_1_c_qM_scalar_mass",
            "coefficient": "c_qM",
            "target": "Y5B_9_q_loc_projection",
            "formula": "epsilon_q_loc_Y5=abs(c_qM*q_proxy)",
            "known_input": f"q_proxy={Q_PROXY_VALUE} dimensionless_proxy",
            "missing_input": "C_qmu normalization; M_eff_ref_or_denominator; units; arena bound; source-backed c_qM",
            "row_status": "blocked_not_filled",
            "numeric_or_symbolic": "symbolic_template_only",
            "no_cancellation_flag": "true_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "QCR743_2_c_qt_time_drift",
            "coefficient": "c_qt",
            "target": "Y5B_0/Y5B_1/R9_Gdot",
            "formula": "dln_mu_dt|_q=c_qt*q_proxy/Delta_t",
            "known_input": f"q_proxy={Q_PROXY_VALUE} but no time profile",
            "missing_input": "Delta_t; time profile; clock/source frame; Gdot or GMdot arena row",
            "row_status": "blocked_not_filled",
            "numeric_or_symbolic": "symbolic_template_only",
            "no_cancellation_flag": "true_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "QCR743_3_c_q_alpha_R10",
            "coefficient": "c_q_alpha(lambda)",
            "target": "R10_fifth_force",
            "formula": "alpha_q_loc(lambda)=c_q_alpha(lambda)*q_proxy",
            "known_input": "R10 row infrastructure exists but q_loc-to-alpha map is absent",
            "missing_input": "lambda map; real bound curve; c_q_alpha source; no-range theorem or units",
            "row_status": "blocked_not_filled",
            "numeric_or_symbolic": "symbolic_template_only",
            "no_cancellation_flag": "true_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "QCR743_4_c_q_PPN_vector",
            "coefficient": "c_q_PPN_vector",
            "target": "Y5B_8/R3-R8",
            "formula": "Delta_PPN_q=c_q_PPN_vector*q_proxy",
            "known_input": "PPN target vector exists in Y5 source-normalization ledger",
            "missing_input": "weak-field Green operator; gauge convention; component coefficients; PPN comparison row",
            "row_status": "blocked_not_filled",
            "numeric_or_symbolic": "symbolic_template_only",
            "no_cancellation_flag": "true_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "QCR743_5_c_tau_q_symgrad",
            "coefficient": "c_tau_q",
            "target": "epsilon_nonstationary_tau to q_loc coupling",
            "formula": "epsilon_tau_to_q <= c_tau_q*epsilon_nonstationary_tau",
            "known_input": "skew/vorticity subcomponent is zero",
            "missing_input": "symgrad component bounds; same-frame stress envelope; denominator; tau-role lock",
            "row_status": "blocked_not_filled",
            "numeric_or_symbolic": "symbolic_template_only",
            "no_cancellation_flag": "true_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def pruning_rule_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "SPR743_0_decompose_current",
            "statement": "T_H^{mu nu}nabla_mu tau_nu = T_H^{mu nu}nabla_(mu tau_nu) for symmetric Hilbert stress",
            "allowed_use": "remove antisymmetric/vorticity pieces from tau-current leakage accounting",
            "forbidden_use": "declare tau Killing, q_loc zero, or C_qmu q_loc zero",
            "claim_status": "exact_pruning_rule_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "SPR743_1_preserve_symgrad_debt",
            "statement": "epsilon_nonstationary_tau is still sourced by the symgrad/stress/denominator chain",
            "allowed_use": "carry only trace/shear/lapse/shift/boundary/tau-mismatch/stress/denominator rows forward",
            "forbidden_use": "reintroduce vorticity as a bound debt or cancel it against another channel",
            "claim_status": "debt_narrowed_not_closed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "SPR743_2_q_loc_distinction",
            "statement": "skew tau silence is not q_loc source-mass silence",
            "allowed_use": "treat c_tau_q_skew=0 as a subcomponent theorem only",
            "forbidden_use": "fill c_qM, c_qt, c_q_alpha, or c_q_PPN with zero from this theorem",
            "claim_status": "scope_guard_active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R743_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_743": "first_subcomponent_zeroed_but_scalar_mass_coefficient_unfilled",
            "zero_or_input": "c_tau_q_skew=0 exact; c_qM still requires C_qmu, units, denominator, and arena bound",
            "still_missing": "C_qmu normalization; M_eff_ref; q_loc-to-source unit map; c_qM source; no-cancellation bound row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R743_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_743": "epsilon_nonstationary_tau_narrowed_not_closed",
            "zero_or_input": "antisymmetric/vorticity terms removed; symgrad/stress denominator retained",
            "still_missing": "B_trace; B_shear; B_lapse; B_shift; B_boundary; B_tau_mismatch; stress envelope; M_ref_candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R743_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_743": "q_loc_channel_still_open_in_no_cancellation_envelope",
            "zero_or_input": "one tau skew subcomponent cannot cancel or erase the q_loc mass channel",
            "still_missing": "first source-backed c_qM row or parent-owned C_qmu/Mref contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D743_0_exact_skew_zero",
            "decision": "accept antisymmetric tau derivative silence",
            "meaning": "vorticity/skew pieces do not contribute to the symmetric-stress tau-current numerator",
            "claim_status": "exact_internal_pruning_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D743_1_no_tau_promotion",
            "decision": "do not promote skew zero to tau Killing or local GR",
            "meaning": "symgrad(tau), stress exchange, and denominator remain the actual physical bottleneck",
            "claim_status": "promotion_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D743_2_no_first_cqM_row",
            "decision": "do not fill c_qM from the compact-shell proxy",
            "meaning": "q_proxy is numeric but coefficient normalization, denominator, and arena transfer are missing",
            "claim_status": "blocked_not_filled",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D743_3_next",
            "decision": "attack scalar mass coupling coefficient and denominator together",
            "meaning": "the first claim-like q_loc row needs c_qM, C_qmu units, q_proxy equivalence, and M_ref/M_eff normalization",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU743_0_allowed",
            "allowed_after_743": "say the skew/vorticity part of the tau-current leakage is exactly zero",
            "forbidden_after_743": "say epsilon_nonstationary_tau, q_loc, C_qmu q_loc, or local-GR is zero",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU743_1_allowed",
            "allowed_after_743": "drop vorticity from future tau-current bound ledgers",
            "forbidden_after_743": "use projected channel silence as physical metric shear zero",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU743_2_allowed",
            "allowed_after_743": "focus next on c_qM/C_qmu/M_ref because this is the coupling bottleneck",
            "forbidden_after_743": "score q_proxy directly as a source-normalization pass",
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
            "main_result": "exact antisymmetric tau derivative/vorticity silence is established as a scoped pruning theorem; q_loc coefficients remain unfilled",
            "hard_blocker": "c_qM/C_qmu/M_ref/unit map and symgrad-tau component bounds remain unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    tau_zero: list[dict[str, Any]],
    qloc_coeffs: list[dict[str, Any]],
    pruning: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_742_VALIDATION.csv")
    all_rows = tau_zero + qloc_coeffs + pruning + y5_update + decisions + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V743_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V743_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V743_2_prior_742_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "742 validation has no failures"})
    validation.append({"check_id": "V743_3_exact_skew_zero_present", "result": "pass" if any(row["derivation_status"] == "exact_algebraic_zero" and row["component_zero_established"] == "true" for row in tau_zero) else "fail", "detail": "antisymmetric tau derivative contraction zero"})
    validation.append({"check_id": "V743_4_symgrad_not_promoted", "result": "pass" if any(row["derivation_status"] == "rejected_scope_error" for row in tau_zero) else "fail", "detail": "skew zero not promoted to symgrad/tau Killing"})
    validation.append({"check_id": "V743_5_projected_shear_guard_retained", "result": "pass" if any(row["derivation_status"] == "channel_zero_only_not_local_metric_zero" for row in tau_zero) else "fail", "detail": "projected channel not physical metric shear"})
    validation.append({"check_id": "V743_6_q_proxy_recorded", "result": "pass" if any(Q_PROXY_VALUE in row["known_input"] for row in qloc_coeffs) else "fail", "detail": f"q_proxy={Q_PROXY_VALUE}"})
    validation.append({"check_id": "V743_7_cqM_not_filled", "result": "pass" if any(row["coefficient"] == "c_qM" and row["row_status"] == "blocked_not_filled" for row in qloc_coeffs) else "fail", "detail": "c_qM remains blocked until unit/coupling contract"})
    validation.append({"check_id": "V743_8_skew_zero_not_q_loc_claim", "result": "pass" if any(row["coefficient"] == "c_tau_q_skew" and row["valid_for_claim"] == "false" for row in qloc_coeffs) else "fail", "detail": "theorem-zero subcomponent is nonclaim"})
    validation.append({"check_id": "V743_9_pruning_scope_guard", "result": "pass" if any("not q_loc source-mass silence" in row["statement"] for row in pruning) else "fail", "detail": "q_loc distinction preserved"})
    validation.append({"check_id": "V743_10_Y5_rows_retained", "result": "pass" if {"Y5R743_9_q_loc_projection", "Y5R743_5_extra_mass_projection"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "q_loc and extra-mass Y5 rows retained"})
    validation.append({"check_id": "V743_11_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V743_12_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V743_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V743_14_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V743_15_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V743_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    tau_zero: list[dict[str, Any]],
    qloc_coeffs: list[dict[str, Any]],
    pruning: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 743 - Y5 R10 First q_loc Free Coefficient Row Or Tau Component Zero

Start point: 742 activated the q_loc free coefficient pack because the pretty route,

```text
C_qmu = N_M tau_mu
```

is still conditional rather than parent-owned.

Current result: **one exact component-zero exists, but it is a pruning theorem, not a local-GR pass**. Since the Hilbert stress is symmetric, the antisymmetric/skew part of `nabla tau` cannot contribute to the tau-current leakage:

```text
T_H^{{mu nu}} nabla_mu tau_nu = T_H^{{mu nu}} nabla_(mu tau_nu)
```

That is a real little win. It means vorticity/skew bookkeeping should not be carried as a live tau-current residual. But it does **not** fill `c_qM`, `c_qt`, `c_q_alpha(lambda)`, or `c_q_PPN_vector`, because the surviving obstruction is still the symmetric part, the stress envelope, the denominator, and the `C_qmu q_loc` coupling.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | skew/vorticity tau-current subcomponent zeroed; q_loc coefficients remain unfilled |
| Next target | `{NEXT_TARGET}` |

## Tau Component Zero Attempt

{markdown_table(tau_zero, ["attempt_id", "component", "candidate_theorem", "derivation_status", "what_it_prunes", "what_remains", "component_zero_established", "valid_for_claim"])}

## q_loc Coefficient Row Attempt

{markdown_table(qloc_coeffs, ["row_id", "coefficient", "target", "formula", "known_input", "missing_input", "row_status", "numeric_or_symbolic", "valid_for_claim"])}

## Skew-to-Symgrad Pruning Rule

{markdown_table(pruning, ["rule_id", "statement", "allowed_use", "forbidden_use", "claim_status", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_743", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_743", "forbidden_after_743", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

We got a proper small derivation, not fireworks: the skew/vorticity part of the tau-current leakage is mathematically dead because symmetric stress cannot contract with an antisymmetric derivative. That trims the debt ledger cleanly. But the coupling bottleneck is still the dragon in the doorway: `c_qM` cannot be filled from the compact-shell proxy until `C_qmu`, units, denominator, and source-normalization map are owned. Next target should hit `c_qM/C_qmu/M_ref` directly.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()

    sources = make_source_register(generated_utc)
    tau_zero = tau_component_zero_rows(generated_utc)
    qloc_coeffs = qloc_coefficient_rows(generated_utc)
    pruning = pruning_rule_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        TAU_COMPONENT_ZERO_PATH,
        QLOC_COEFFICIENT_PATH,
        PRUNING_RULE_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(sources, tau_zero, qloc_coeffs, pruning, y5_update, decisions, routes, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TAU_COMPONENT_ZERO_PATH, tau_zero, ["attempt_id", "component", "candidate_theorem", "derivation_status", "proof_sketch", "what_it_prunes", "what_remains", "component_zero_established", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_COEFFICIENT_PATH, qloc_coeffs, ["row_id", "coefficient", "target", "formula", "known_input", "missing_input", "row_status", "numeric_or_symbolic", "no_cancellation_flag", "valid_for_claim", "generated_utc"])
    write_csv(PRUNING_RULE_PATH, pruning, ["rule_id", "statement", "allowed_use", "forbidden_use", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_743", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_743", "forbidden_after_743", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, tau_zero, qloc_coeffs, pruning, y5_update, decisions, routes, summary, validation)

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
