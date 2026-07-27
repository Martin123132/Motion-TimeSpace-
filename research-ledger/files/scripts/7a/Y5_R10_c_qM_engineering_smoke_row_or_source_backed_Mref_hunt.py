from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "745-Y5-R10-c_qM-engineering-smoke-row-or-source-backed-Mref-hunt.md"
NEXT_TARGET = "746-Y5-R10-q_loc-to-PPN-or-alpha3-projection-map-contract.md"
STATUS = "Y5_R10_745_unit_cqM_engineering_smoke_row_written_source_backed_Mref_absent_nonclaim"
CLAIM_CEILING = "engineering_smoke_and_Mref_hunt_only_no_claim_denominator_no_q_loc_pass_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_745_SOURCE_REGISTER.csv"
SMOKE_ROW_PATH = RESIDUALS / "P8_Y5_R10_745_CQM_ENGINEERING_SMOKE_ROW.csv"
MREF_HUNT_PATH = RESIDUALS / "P8_Y5_R10_745_SOURCE_BACKED_MREF_HUNT.csv"
LOCK_COMPARISON_PATH = RESIDUALS / "P8_Y5_R10_745_NAIVE_LOCK_COMPARISON.csv"
SMOKE_RULES_PATH = RESIDUALS / "P8_Y5_R10_745_SMOKE_EVALUATION_RULES.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_745_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_745_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_745_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_745_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_745_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "744_doc": {
        "path": POST_CHECKPOINT / "744-Y5-R10-c_qM-coupling-coefficient-contract-or-Mref-denominator-fill.md",
        "needles": ["SMR744_3_next_smoke_schema", "GM_orbit/G_ref", "745-Y5-R10-c_qM-engineering-smoke-row-or-source-backed-Mref-hunt.md"],
        "role": "immediate engineering-smoke handoff",
    },
    "744_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_744_VALIDATION.csv",
        "needles": ["V744_6_engineering_denominator_quarantined", "V744_13_formalization_workbench_untouched", "V744_14_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "744_contract": {
        "path": RESIDUALS / "P8_Y5_R10_744_CQM_COUPLING_CONTRACT.csv",
        "needles": ["CQM744_0_operator_norm_definition", "contract_written_no_value", "CQM744_5_acceptance_rule"],
        "role": "c_qM operator-norm contract",
    },
    "744_mref": {
        "path": RESIDUALS / "P8_Y5_R10_744_MREF_DENOMINATOR_FILL_ATTEMPT.csv",
        "needles": ["MRF744_1_empirical_engineering_denominator", "allowed_only_as_private_smoke_denominator", "MRF744_4_verdict"],
        "role": "Mref claim block and engineering denominator permission",
    },
    "744_scalar": {
        "path": RESIDUALS / "P8_Y5_R10_744_SCALAR_MASS_ROW_STATUS.csv",
        "needles": ["SMR744_0_cqM_contract_status", "contract_ready_value_blocked", "SMR744_3_next_smoke_schema"],
        "role": "scalar mass row status",
    },
    "boundary_first_status": {
        "path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["M_H_ref", "claim_valid_data_rows", "missing_claim_valid_source_or_zero_theorem"],
        "role": "boundary-reference M_H_ref hunt result",
    },
    "boundary_first_fill": {
        "path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv",
        "needles": ["MISSING_M_H_REF", "reference_zero_not_MTS_evidence", "valid_for_claim"],
        "role": "unfilled M_H_ref fill pack",
    },
    "boundary_first_eval": {
        "path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_EVALUATOR.csv",
        "needles": ["not_computed_missing_numeric_inputs", "reference-only zero is not MTS evidence", "valid_for_claim"],
        "role": "first-row evaluator nonclaim",
    },
    "696_mhref_audit": {
        "path": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
        "needles": ["MHA696_6_verdict", "fail_current_corpus", "M_H_ref remains unfilled"],
        "role": "M_H_ref denominator audit",
    },
    "697_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv",
        "needles": ["SNC697_9_verdict", "fail_current_corpus", "denominator fill row remains unfilled"],
        "role": "source-normalization certificate failure",
    },
    "698_bridge": {
        "path": RESIDUALS / "P8_Y5_R10_698_PG_MHREF_BRIDGE_THEOREM_ATTEMPT.csv",
        "needles": ["BT698_8_MHref_calibration", "fail_current_corpus", "GM_orbit=G_ref M_H_ref"],
        "role": "PG/MHref bridge failure",
    },
    "q_loc_bound_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": [f"{Q_PROXY}", "alpha3-equivalent channel", "needed_before_claim"],
        "role": "q_loc proxy and lock reminders",
    },
    "Y5_bound_input": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "needles": ["Y5B_9_q_loc_projection", "mixed_until_projection_fixed", "alpha3 <= 4e-20"],
        "role": "Y5/PPN lock context",
    },
}


NAIVE_LOCKS: list[dict[str, Any]] = [
    {"lock_id": "NLC745_gamma", "observable": "gamma_minus_1", "bound": 2.3e-5, "source": "Y5B_8_full_PPN_source_vector"},
    {"lock_id": "NLC745_beta", "observable": "beta_minus_1", "bound": 7.8e-5, "source": "Y5B_8_full_PPN_source_vector"},
    {"lock_id": "NLC745_alpha1", "observable": "alpha1", "bound": 1.0e-4, "source": "Y5B_8_full_PPN_source_vector"},
    {"lock_id": "NLC745_xi", "observable": "xi", "bound": 4.0e-9, "source": "Y5B_8_full_PPN_source_vector"},
    {"lock_id": "NLC745_alpha2", "observable": "alpha2", "bound": 2.0e-9, "source": "Y5B_8_full_PPN_source_vector"},
    {"lock_id": "NLC745_alpha3", "observable": "alpha3", "bound": 4.0e-20, "source": "P8_QLOC_BOUND_RUNNER_SPEC/Y5B_8"},
]


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


def claim_valid_mhref_rows() -> int:
    rows = read_csv_rows(RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv")
    for row in rows:
        if row.get("quantity") == "M_H_ref":
            try:
                return int(row.get("claim_valid_data_rows", "0"))
            except ValueError:
                return -1
    return -1


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


def smoke_rows(generated_utc: str) -> list[dict[str, Any]]:
    c_qm_smoke = 1.0
    epsilon = abs(c_qm_smoke * Q_PROXY)
    return [
        {
            "smoke_id": "ESM745_0_unit_cqM",
            "system_id": "unit_coefficient_private_smoke",
            "denominator": "M_ref_eng := GM_orbit/G_ref",
            "denominator_status": "empirical_readout_denominator_quarantined",
            "c_qM_smoke": f"{c_qm_smoke:.1f}",
            "q_proxy": f"{Q_PROXY:.15g}",
            "epsilon_q_loc_smoke": f"{epsilon:.15g}",
            "units": "dimensionless_if_and_only_if_Cq_and_Mref_eng_unit_map_are_accepted_for_smoke",
            "source_path": str(RESIDUALS / "P8_Y5_R10_744_SCALAR_MASS_ROW_STATUS.csv"),
            "interpretation": "scale-test only; asks what unit q_loc-to-mass projection would imply",
            "claim_status": "private_engineering_smoke_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "smoke_id": "ESM745_1_zero_cqM",
            "system_id": "theorem_zero_counterfactual",
            "denominator": "any valid M_ref",
            "denominator_status": "irrelevant_if_exact_zero_were_proved",
            "c_qM_smoke": "0",
            "q_proxy": f"{Q_PROXY:.15g}",
            "epsilon_q_loc_smoke": "0",
            "units": "dimensionless",
            "source_path": str(RESIDUALS / "P8_Y5_R10_744_SCALAR_MASS_ROW_STATUS.csv"),
            "interpretation": "counterfactual only; exact C_q q_loc orthogonality is not derived",
            "claim_status": "not_current_branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "smoke_id": "ESM745_2_required_real_row",
            "system_id": "future_claim_grade_or_bound_row",
            "denominator": "M_H_ref or sourced M_ref with same-frame certificate",
            "denominator_status": "missing",
            "c_qM_smoke": "MISSING_SOURCE_BACKED_CQM",
            "q_proxy": f"{Q_PROXY:.15g}",
            "epsilon_q_loc_smoke": "not_computed",
            "units": "must match source-normalization arena",
            "source_path": "MISSING_CQM_SOURCE_PATH",
            "interpretation": "real row requires C_q owner/unit map and arena projection",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def mref_hunt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "MRH745_0_boundary_status",
            "candidate": "M_H_ref from boundary-reference first-row status",
            "evidence": "claim_valid_data_rows=0 for M_H_ref",
            "result": "no_source_backed_claim_denominator",
            "next_action": "derive minimal parent boundary/reference clause or fill residual row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "MRH745_1_fill_pack",
            "candidate": "M_H_ref from first-row fill pack",
            "evidence": "MISSING_M_H_REF in MTS_Hamiltonian_PiM_local_branch",
            "result": "template_unfilled",
            "next_action": "source B_zero_flux, Delta_symp, M_H_ref together before scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "MRH745_2_reference_zero",
            "candidate": "reference-only M_H_ref=1 row",
            "evidence": "reference_zero_not_MTS_evidence is explicitly not claimable",
            "result": "rejected_as_evidence",
            "next_action": "do not use reference-only zero to normalize MTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "MRH745_3_MHref_certificate",
            "candidate": "source-normalization certificate",
            "evidence": "SNC697_9_verdict=fail_current_corpus",
            "result": "certificate_failed",
            "next_action": "integrable charge, tau lock, same-frame, PG bridge, and extra-sector silence still needed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "MRH745_4_engineering_denominator",
            "candidate": "M_ref_eng := GM_orbit/G_ref",
            "evidence": "allowed by 744 only as empirical_readout_denominator",
            "result": "usable_for_private_smoke_only",
            "next_action": "carry quarantine labels and valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def lock_comparison_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    epsilon = Q_PROXY
    for lock in NAIVE_LOCKS:
        bound = float(lock["bound"])
        ratio = epsilon / bound
        rows.append(
            {
                "lock_id": lock["lock_id"],
                "observable": lock["observable"],
                "epsilon_unit_cqM_smoke": f"{epsilon:.15g}",
                "naive_bound": f"{bound:.15g}",
                "naive_ratio": f"{ratio:.15g}",
                "naive_1to1_result": "below_bound" if epsilon <= bound else "above_bound",
                "why_not_claim": "projection from q_loc to this observable is not derived; 1-to-1 map is only a danger-scale diagnostic",
                "source": lock["source"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    rows.append(
        {
            "lock_id": "NLC745_R10",
            "observable": "alpha(lambda)",
            "epsilon_unit_cqM_smoke": f"{epsilon:.15g}",
            "naive_bound": "not_selected_without_lambda",
            "naive_ratio": "not_computed",
            "naive_1to1_result": "not_scoreable",
            "why_not_claim": "R10 needs lambda, c_q_alpha(lambda), and real alpha(lambda) bound curve",
            "source": "Y5B_4/R10 rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def smoke_rule_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "SER745_0_quarantine",
            "rule": "Every smoke row must say empirical_readout_denominator and valid_for_claim=false.",
            "allowed": "private intuition, debugging projection maps, magnitude triage",
            "forbidden": "public claim, local-GR pass, Newton derivation, R10/PPN pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "SER745_1_no_direct_qproxy_score",
            "rule": "q_proxy cannot be compared directly to an arena lock.",
            "allowed": "naive 1-to-1 danger-scale diagnostic with explicit warning",
            "forbidden": "treat below gamma/beta as evidence or alpha3 failure as decisive without projection map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "SER745_2_next_projection_map",
            "rule": "The next real bottleneck is the q_loc-to-observable projection map.",
            "allowed": "derive/map to PPN, alpha3, R10, or source-normalization components separately",
            "forbidden": "single scalar c_qM standing in for all observable channels",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R745_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_745": "unit_cqM_smoke_written_nonclaim",
            "zero_or_input": f"epsilon_q_loc_smoke={Q_PROXY:.15g} for c_qM_smoke=1 only",
            "still_missing": "real C_q owner; unit map; claim M_ref; projection to actual observable locks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R745_MHref",
            "source_row": "M_H_ref denominator",
            "status_after_745": "source_backed_Mref_hunt_failed",
            "zero_or_input": f"claim_valid_MHref_rows={claim_valid_mhref_rows()}",
            "still_missing": "claim-valid M_H_ref or same-frame source-backed M_ref row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R745_projection_map",
            "source_row": "Y5B_8/Y5B_9/R10",
            "status_after_745": "next_projection_map_selected",
            "zero_or_input": "naive locks show why channel projection matters",
            "still_missing": "q_loc-to-PPN/alpha3/R10 map with separate coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D745_0_smoke_written",
            "decision": "write unit-c_qM engineering smoke row",
            "meaning": "unit coupling gives epsilon scale 7.432631961576971e-06, useful only for magnitude triage",
            "claim_status": "private_smoke_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D745_1_Mref_hunt",
            "decision": "no source-backed M_ref found",
            "meaning": "M_H_ref still has zero claim-valid rows; reference-only row rejected",
            "claim_status": "blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D745_2_naive_locks",
            "decision": "record naive lock comparison as danger-scale only",
            "meaning": "unit smoke is below loose gamma/beta-like locks but above preferred-frame locks if mapped 1-to-1, proving projection map is essential",
            "claim_status": "diagnostic_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D745_3_next",
            "decision": "derive q_loc-to-PPN or alpha3 projection map",
            "meaning": "without the projection map, c_qM smoke cannot tell whether the danger channel is gamma/beta, alpha3, xi, R10, or none",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU745_0_allowed",
            "allowed_after_745": "quote the unit-cqM smoke number as private magnitude triage",
            "forbidden_after_745": "call it a pass, prediction, or evidence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU745_1_allowed",
            "allowed_after_745": "say no source-backed M_H_ref is available",
            "forbidden_after_745": "use reference-only M_H_ref=1 or observed GM as derived denominator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU745_2_allowed",
            "allowed_after_745": "move next to channelwise q_loc projection maps",
            "forbidden_after_745": "let a single scalar c_qM decide PPN/R10/alpha3 at once",
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
            "main_result": "unit-c_qM engineering smoke row written; source-backed M_ref hunt found no claim denominator; projection-map bottleneck selected",
            "hard_blocker": "q_loc-to-observable projection map and claim M_H_ref remain missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    mref_hunt: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_744_VALIDATION.csv")
    all_rows = smoke + mref_hunt + locks + rules + y5_update + decisions + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V745_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V745_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V745_2_prior_744_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "744 validation has no failures"})
    validation.append({"check_id": "V745_3_unit_smoke_number_written", "result": "pass" if any(row["smoke_id"] == "ESM745_0_unit_cqM" and row["epsilon_q_loc_smoke"] == f"{Q_PROXY:.15g}" for row in smoke) else "fail", "detail": f"unit epsilon={Q_PROXY:.15g}"})
    validation.append({"check_id": "V745_4_smoke_quarantined", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in smoke) else "fail", "detail": "all smoke rows nonclaim"})
    validation.append({"check_id": "V745_5_MHref_claim_rows_zero", "result": "pass" if claim_valid_mhref_rows() == 0 else "fail", "detail": f"claim_valid_MHref_rows={claim_valid_mhref_rows()}"})
    validation.append({"check_id": "V745_6_reference_zero_rejected", "result": "pass" if any(row["result"] == "rejected_as_evidence" for row in mref_hunt) else "fail", "detail": "reference-only denominator not accepted"})
    validation.append({"check_id": "V745_7_naive_lock_mixed_results", "result": "pass" if {"below_bound", "above_bound"}.issubset({row["naive_1to1_result"] for row in locks}) else "fail", "detail": "naive lock comparison has both below and above rows"})
    validation.append({"check_id": "V745_8_R10_not_scoreable", "result": "pass" if any(row["observable"] == "alpha(lambda)" and row["naive_1to1_result"] == "not_scoreable" for row in locks) else "fail", "detail": "R10 requires lambda/projection map"})
    validation.append({"check_id": "V745_9_rules_forbid_claims", "result": "pass" if all(row["valid_for_claim"] == "false" for row in rules) and any("projection map" in row["rule"] for row in rules) else "fail", "detail": "smoke rules enforce projection-map next"})
    validation.append({"check_id": "V745_10_Y5_rows_retained", "result": "pass" if {"Y5R745_9_q_loc_projection", "Y5R745_MHref", "Y5R745_projection_map"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "q_loc/MHref/projection rows retained"})
    validation.append({"check_id": "V745_11_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V745_12_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V745_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V745_14_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V745_15_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V745_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    mref_hunt: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 745 - Y5 R10 c_qM Engineering Smoke Row Or Source-Backed Mref Hunt

Start point: 744 made `c_qM` precise as an operator-norm contract, but refused to fill it as a claim value.

Current result: **a quarantined unit-coupling smoke row is written, and no source-backed `M_ref` is found**.

The smoke number is:

```text
c_qM_smoke = 1
epsilon_q_loc_smoke = |c_qM_smoke q_proxy| = {Q_PROXY:.15g}
```

This is not evidence. It is a danger-scale diagnostic using `M_ref_eng := GM_orbit/G_ref`, explicitly labelled as an empirical readout denominator. The useful lesson is that a unit projection is not automatically harmless: it sits below loose gamma/beta-scale locks under a naive map, but above tight preferred-frame locks under the same naive map. Therefore the next serious target is not more scalar smoke; it is the **q_loc-to-observable projection map**.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | unit-cqM smoke row written; source-backed Mref absent; projection map selected |
| Next target | `{NEXT_TARGET}` |

## Engineering Smoke Row

{markdown_table(smoke, ["smoke_id", "system_id", "denominator", "denominator_status", "c_qM_smoke", "q_proxy", "epsilon_q_loc_smoke", "interpretation", "claim_status", "valid_for_claim"])}

## Source-Backed Mref Hunt

{markdown_table(mref_hunt, ["hunt_id", "candidate", "evidence", "result", "next_action", "valid_for_claim"])}

## Naive Lock Comparison

{markdown_table(locks, ["lock_id", "observable", "epsilon_unit_cqM_smoke", "naive_bound", "naive_ratio", "naive_1to1_result", "why_not_claim", "valid_for_claim"])}

## Smoke Evaluation Rules

{markdown_table(rules, ["rule_id", "rule", "allowed", "forbidden", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_745", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_745", "forbidden_after_745", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is one of those useful-but-not-glamorous checkpoints. The unit smoke row says: if the missing projection coefficient were order-one, the q_loc residue would be around `7.4e-6`. That is not instantly fatal for every loose PPN-like scale, but it is wildly too big for ultra-tight preferred-frame style locks if the map hits them directly. So the branch is neither dead nor safe. The next punch is obvious: derive the channel map so we know whether q_loc feeds gamma/beta, alpha3/xi, R10, or only a quarantined source-normalization residual.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    smoke = smoke_rows(generated_utc)
    mref_hunt = mref_hunt_rows(generated_utc)
    locks = lock_comparison_rows(generated_utc)
    rules = smoke_rule_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        SMOKE_ROW_PATH,
        MREF_HUNT_PATH,
        LOCK_COMPARISON_PATH,
        SMOKE_RULES_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, smoke, mref_hunt, locks, rules, y5_update, decisions, routes, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SMOKE_ROW_PATH, smoke, ["smoke_id", "system_id", "denominator", "denominator_status", "c_qM_smoke", "q_proxy", "epsilon_q_loc_smoke", "units", "source_path", "interpretation", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(MREF_HUNT_PATH, mref_hunt, ["hunt_id", "candidate", "evidence", "result", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(LOCK_COMPARISON_PATH, locks, ["lock_id", "observable", "epsilon_unit_cqM_smoke", "naive_bound", "naive_ratio", "naive_1to1_result", "why_not_claim", "source", "valid_for_claim", "generated_utc"])
    write_csv(SMOKE_RULES_PATH, rules, ["rule_id", "rule", "allowed", "forbidden", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_745", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_745", "forbidden_after_745", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, smoke, mref_hunt, locks, rules, y5_update, decisions, routes, summary, validation)

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
