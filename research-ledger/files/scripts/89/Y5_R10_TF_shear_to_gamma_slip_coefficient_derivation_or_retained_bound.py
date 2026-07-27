from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_TF_shear_to_gamma_slip_operator_norm_contract_written_no_numeric_coefficient_nonclaim"
CLAIM_CEILING = "coefficient_derivation_contract_only_no_Cgamma_value_no_Cslip_value_no_sigma_bound_no_PPN_score_no_R10_no_local_GR_claim"
NEXT_TARGET = "694-Y5-R10-epsilon-TF-numerator-denominator-contract-or-first-fill-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "693-Y5-R10-TF-shear-to-gamma-slip-coefficient-derivation-or-retained-bound.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "347_doc": ROOT / "347-local-GR-parent-reduction-theorem-attempt.md",
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "357_doc": ROOT / "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "691_doc": ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md",
    "692_doc": ROOT / "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "691_validation": RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    "691_source_pack": RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv",
    "692_validation": RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv",
    "692_targets": RESIDUALS / "P8_Y5_R10_692_SOURCE_LOCKED_PPN_TARGETS.csv",
    "692_inputs": RESIDUALS / "P8_Y5_R10_692_METRIC_SHEAR_RUNNER_INPUTS.csv",
    "692_evaluator": RESIDUALS / "P8_Y5_R10_692_SYMBOLIC_EVALUATOR.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "r11_template": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "347_doc": "conditional local-GR reduction and gamma residual owner map",
        "352_doc": "symbolic PPN vector with B_TF to gamma/slip terms",
        "357_doc": "retained PPN vector with C_TF epsilon_TF structure",
        "655_doc": "EH/R11 operator gate and observable impact table",
        "691_doc": "metric shear source pack and nohair failure",
        "692_doc": "source-locked PPN guardrail runner predecessor",
        "655_validation": "655 validation gate",
        "691_validation": "691 validation gate",
        "691_source_pack": "metric shear source rows requiring coefficients",
        "692_validation": "692 validation gate",
        "692_targets": "source-locked guardrail targets",
        "692_inputs": "runner input rows with missing coefficients",
        "692_evaluator": "symbolic evaluator rows",
        "boundary_reference_status": "same-frame denominator remains blocked",
        "r11_template": "retained non-EH operator vector template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def coefficient_derivation_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "CDA693_0_observed_metric_gauge",
            "target": "define observed weak-field variables",
            "derivation_step": "choose one observed metric/coframe and a weak-field scalar decomposition with potentials Phi and Psi plus trace-free spatial residuals",
            "result": "conditional_setup_only",
            "coefficient_effect": "C_gamma_TF and C_slip_TF are gauge/convention dependent until this observed-frame map is parent-signed",
            "blocker": "observed frame exists as closure context but not as an EH/PPN completion theorem",
            "valid_for_claim": "false",
            "source_paths": source_list("347_doc", "655_doc", "692_inputs"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_1_EH_TF_field_equation",
            "target": "derive trace-free elliptic slip equation",
            "derivation_step": "in an EH weak-field branch, the trace-free spatial field equation has the form D_ij(Phi-Psi)=kappa_eff Pi_TF_ij plus retained boundary/projector TF sources",
            "result": "conditional_EH_contract",
            "coefficient_effect": "coefficient becomes an operator norm of the inverse trace-free elliptic map",
            "blocker": "EH-only exterior, Levi-Civita compatibility, source normalization, and harmless boundary/projector terms are not derived",
            "valid_for_claim": "false",
            "source_paths": source_list("347_doc", "352_doc", "357_doc", "655_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_2_inverse_operator_norm",
            "target": "construct C_slip_TF",
            "derivation_step": "define C_slip_TF := ||G_TF kappa_eff Pi_TF||_slip / epsilon_TF where G_TF is the sourced inverse operator with boundary conditions",
            "result": "operator_norm_definition_not_numeric",
            "coefficient_effect": "C_slip_TF is well-defined only after Pi_TF normalization, boundary conditions, domain, and denominator are fixed",
            "blocker": "Pi_TF amplitude, boundary profile, and same-frame denominator are missing",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "692_inputs", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_3_gamma_ratio",
            "target": "construct C_gamma_TF",
            "derivation_step": "gamma-1 is the spatial-potential response normalized by the Newtonian/source potential, so C_gamma_TF := ||delta_gamma_TF|| / epsilon_TF",
            "result": "operator_norm_definition_not_numeric",
            "coefficient_effect": "C_gamma_TF needs the Newtonian potential/source normalization U_ref and the slip-to-gamma convention",
            "blocker": "U_ref/M_H_ref and gamma convention are not fixed by the current local branch",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "692_evaluator", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_4_unit_coefficient_identity",
            "target": "test whether C_gamma_TF=1 or C_slip_TF=1 can be claimed",
            "derivation_step": "if epsilon_TF is defined directly as the observable gamma/slip residual, the relevant coefficient can be set to one by normalization",
            "result": "bookkeeping_identity_only",
            "coefficient_effect": "unit coefficient is allowed only as an output-level residual definition; it is not a theory prediction from parent fields",
            "blocker": "using this as a prediction would double-count the observable and erase the MTS source map",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "692_evaluator"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_5_R11_branch",
            "target": "non-EH or retained operator contribution",
            "derivation_step": "if EH operator selection fails, C_gamma_TF and C_slip_TF must be supplied by the retained R11 operator family weak-field map",
            "result": "retained_bound_required",
            "coefficient_effect": "no universal coefficient exists without the operator form and weak-field Green kernel",
            "blocker": "R11 rows are template-only and contain no real coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "r11_template"),
            "generated_utc": now,
        },
        {
            "attempt_id": "CDA693_6_verdict",
            "target": "claim-grade coefficient",
            "derivation_step": "promote C_gamma_TF/C_slip_TF to numeric or theorem-zero",
            "result": "not_derived_current_corpus",
            "coefficient_effect": "693 writes an operator-norm contract and retained-bound template but no scoreable coefficient",
            "blocker": "missing epsilon_TF numerator/denominator, boundary conditions, source normalization, and operator branch",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "692_doc", "692_inputs"),
            "generated_utc": now,
        },
    ]


def operator_norm_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "ONC693_0_C_slip_TF",
            "C_slip_TF",
            "||G_TF[kappa_eff Pi_TF]||_slip / epsilon_TF",
            "Pi_TF source tensor; kappa_eff; Green operator G_TF; boundary conditions; epsilon_TF normalization",
            "MISSING_OPERATOR_NORM_INPUTS",
            "valid only as retained operator-norm contract",
        ),
        (
            "ONC693_1_C_gamma_TF",
            "C_gamma_TF",
            "||delta_gamma_TF|| / epsilon_TF with delta_gamma_TF derived from slip/spatial-potential response",
            "C_slip_TF or direct gamma map; U_ref/Newtonian potential; same-frame denominator; PPN gauge convention",
            "MISSING_GAMMA_NORMALIZATION_INPUTS",
            "valid only as retained operator-norm contract",
        ),
        (
            "ONC693_2_epsilon_TF",
            "epsilon_TF",
            "dimensionless norm of physical metric trace-free residual, not projected J_C shear silence",
            "B_TF_over_MH;T_projector_TF_over_MH;profile_terms;M_H_ref",
            "MISSING_EPSILON_TF_NUMERATOR_DENOMINATOR",
            "next target because coefficients cannot be evaluated without it",
        ),
        (
            "ONC693_3_identity_coefficient_guard",
            "C_identity",
            "C=1 only when epsilon_TF is defined as the exact same observable residual",
            "explicit label identity_not_prediction; no use in score numerator",
            "SCHEMA_ONLY_NONCLAIM_IDENTITY_GUARD",
            "prevents unit-normalization from becoming an apparent physics prediction",
        ),
        (
            "ONC693_4_R11_retained_map",
            "C_R11_TF",
            "weak-field map coefficient for retained non-EH trace-free operator family",
            "operator form; coefficient units; range/kernel; source path; weak-field solution convention",
            "MISSING_R11_TF_OPERATOR_MAP",
            "fallback if EH/nohair route stays unsigned",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "coefficient": coefficient,
            "formal_definition": definition,
            "required_inputs": required_inputs,
            "current_status": status,
            "allowed_use": allowed_use,
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "692_inputs", "692_evaluator"),
            "generated_utc": now,
        }
        for contract_id, coefficient, definition, required_inputs, status, allowed_use in rows
    ]


def retained_bound_template_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "RBT693_0_C_gamma_TF_bound",
            "C_gamma_TF_bound",
            "upper_bound_numeric_or_theorem_zero",
            "MISSING_C_GAMMA_TF_BOUND",
            "needed to convert source-locked gamma target into epsilon_TF limit",
        ),
        (
            "RBT693_1_C_slip_TF_bound",
            "C_slip_TF_bound",
            "upper_bound_numeric_or_theorem_zero",
            "MISSING_C_SLIP_TF_BOUND",
            "needed for direct lensing/slip residual map",
        ),
        (
            "RBT693_2_G_TF_kernel",
            "G_TF_kernel_norm",
            "domain_and_boundary_condition_specific_kernel_norm",
            "MISSING_G_TF_KERNEL_NORM",
            "operator norm cannot be numeric without local boundary conditions",
        ),
        (
            "RBT693_3_kappa_eff",
            "kappa_eff_or_source_coupling",
            "same-frame gravitational/source coupling in the branch",
            "MISSING_KAPPA_EFF_SOURCE_NORMALIZATION",
            "ties Pi_TF stress to observed metric potentials",
        ),
        (
            "RBT693_4_U_ref",
            "U_ref_or_M_H_ref",
            "Newtonian potential or same-frame mass denominator for gamma normalization",
            "MISSING_U_REF_OR_M_H_REF",
            "gamma coefficient cannot be dimensionless without reference normalization",
        ),
        (
            "RBT693_5_gauge_convention",
            "PPN_gauge_slip_convention",
            "explicit mapping between Phi/Psi/spatial metric and gamma_minus_1",
            "MISSING_PPN_GAUGE_CONVENTION",
            "prevents gauge artifacts from entering coefficient claims",
        ),
        (
            "RBT693_6_identity_guard",
            "identity_coefficient_use",
            "C=1 rows allowed only for observable-level residual definitions",
            "SCHEMA_ONLY_NONCLAIM_IDENTITY_GUARD",
            "unit coefficient cannot be cited as derived MTS prediction",
        ),
    ]
    return [
        {
            "template_id": template_id,
            "field": field,
            "required_evidence": evidence,
            "current_status": status,
            "why_needed": why_needed,
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "655_doc", "692_inputs"),
            "generated_utc": now,
        }
        for template_id, field, evidence, status, why_needed in rows
    ]


def runner_update_rule_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "rule_id": "RUR693_0_gamma_score",
            "target_runner": "future_metric_shear_bound_runner",
            "rule": "score gamma only if epsilon_TF, C_gamma_TF, U_ref/M_H_ref, and source-locked target are all non-missing and same-frame",
            "failure_mode": "otherwise emit not_evaluated_missing_prediction_inputs",
            "valid_for_claim": "false",
            "source_paths": source_list("692_targets", "692_evaluator"),
            "generated_utc": now,
        },
        {
            "rule_id": "RUR693_1_slip_score",
            "target_runner": "future_metric_shear_bound_runner",
            "rule": "score slip only if a direct slip target or model-specific slip-to-observable map exists plus C_slip_TF and epsilon_TF",
            "failure_mode": "otherwise keep slip target quarantined",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "692_targets"),
            "generated_utc": now,
        },
        {
            "rule_id": "RUR693_2_identity_guard",
            "target_runner": "future_metric_shear_bound_runner",
            "rule": "if C=1 arises from defining epsilon_TF as the observable residual, mark identity_only and forbid independent prediction credit",
            "failure_mode": "prevents unit coefficient smoke from becoming a claim",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "692_evaluator"),
            "generated_utc": now,
        },
        {
            "rule_id": "RUR693_3_R11_fallback",
            "target_runner": "future_R11_or_EH_operator_runner",
            "rule": "if EH/nohair remains unsigned, require retained R11 operator coefficient, units, kernel, and weak-field map before scoring",
            "failure_mode": "otherwise no R10/PPN/local-GR promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "r11_template"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG693_0_derivation",
            "gate": "C_gamma_TF/C_slip_TF derivation",
            "required_state": "numeric coefficient or theorem-derived operator norm with all inputs fixed",
            "observed_state": "operator-norm contract only; required inputs missing",
            "result": "fail_blocked",
            "claim_effect": "no coefficient value",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "692_inputs"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG693_1_identity",
            "gate": "unit coefficient identity guard",
            "required_state": "C=1 never counted as prediction unless independently derived from source map",
            "observed_state": "C=1 allowed only as observable-level normalization identity",
            "result": "pass_guard_only",
            "claim_effect": "unit coefficient cannot produce PPN score",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "692_evaluator"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG693_2_EH_branch",
            "gate": "EH trace-free operator branch",
            "required_state": "EH metric-only exterior plus source normalization plus boundary/projector harmlessness",
            "observed_state": "EH route remains conditional or blocked",
            "result": "fail_blocked",
            "claim_effect": "EH operator norm is a contract, not a derived coefficient",
            "valid_for_claim": "false",
            "source_paths": source_list("347_doc", "655_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG693_3_R11_branch",
            "gate": "retained non-EH operator branch",
            "required_state": "real R11 trace-free operator coefficient/kernel/weak-field map",
            "observed_state": "R11 template exists but no real TF coefficient rows",
            "result": "fail_blocked",
            "claim_effect": "no R11 shear/slip score",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "r11_template"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG693_4_local_claims",
            "gate": "PPN/R10/local-GR promotion",
            "required_state": "coefficient, epsilon_TF, target, denominator, and operator branch scoreable",
            "observed_state": "coefficient and epsilon_TF remain missing",
            "result": "fail_policy",
            "claim_effect": "no sigma bound, PPN score, R10, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("692_targets", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG693_5_next",
            "gate": "next target selection",
            "required_state": "choose highest-leverage missing input after coefficient derivation stalls",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "fill epsilon_TF numerator/denominator before coefficient evaluation",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "692_inputs"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D693_0_coefficient",
            "target": "C_gamma_TF/C_slip_TF",
            "result": "operator_norm_contract_written_nonclaim",
            "reason": "EH weak-field logic gives the right operator-norm shape, but not a numeric coefficient without branch, boundary, source, and denominator inputs",
            "next_action": "do not score gamma/slip yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D693_1_identity_guard",
            "target": "unit coefficient route",
            "result": "allowed_only_as_bookkeeping",
            "reason": "C=1 is valid only if epsilon_TF is defined as the observable residual itself, which is not an independent prediction",
            "next_action": "keep unit coefficient smoke rows nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D693_2_next",
            "target": "epsilon_TF numerator/denominator",
            "result": "selected",
            "reason": "coefficient evaluation cannot proceed until physical B_TF/projector TF numerator and same-frame denominator are fixed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S693_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "C_gamma_TF/C_slip_TF derivation reaches an operator-norm contract, not a numeric claim-ready coefficient",
            "hardest_blocker": "epsilon_TF numerator/denominator plus EH/R11 operator branch and boundary conditions",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    retained_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "derivation": derivation_rows,
        "contract": contract_rows,
        "retained": retained_rows,
        "rules": rule_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["655_validation", "691_validation", "692_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    derivation_complete = len(derivation_rows) == 7 and all(row["valid_for_claim"] == "false" for row in derivation_rows)
    operator_contract_complete = len(contract_rows) == 5 and all(row["valid_for_claim"] == "false" for row in contract_rows)
    retained_complete = len(retained_rows) == 7 and all(row["valid_for_claim"] == "false" for row in retained_rows)
    missing_or_schema_retained = all(
        "MISSING_" in row["current_status"] or row["current_status"].startswith("SCHEMA_ONLY") for row in retained_rows
    )
    identity_guard_present = any(row["attempt_id"] == "CDA693_4_unit_coefficient_identity" for row in derivation_rows) and any(
        row["contract_id"] == "ONC693_3_identity_coefficient_guard" for row in contract_rows
    )
    no_numeric_coefficients = not any(
        row["result"] in {"numeric_coefficient", "theorem_zero", "claim_ready"} for row in derivation_rows
    )
    rules_complete = len(rule_rows) == 4 and all(row["valid_for_claim"] == "false" for row in rule_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_693_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_693_COEFFICIENT_DERIVATION_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_693_OPERATOR_NORM_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_693_RETAINED_BOUND_TEMPLATE.csv",
        RESIDUALS / "P8_Y5_R10_693_RUNNER_UPDATE_RULES.csv",
        RESIDUALS / "P8_Y5_R10_693_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_693_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_693_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_693_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V693_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V693_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V693_2_derivation_attempt_complete", derivation_complete, f"derivation_rows={len(derivation_rows)}"),
        ("V693_3_operator_contract_complete", operator_contract_complete, f"contract_rows={len(contract_rows)}"),
        ("V693_4_retained_template_complete", retained_complete, f"retained_rows={len(retained_rows)}"),
        ("V693_5_missing_markers_retained", missing_or_schema_retained, "retained rows keep MISSING or SCHEMA_ONLY status"),
        ("V693_6_identity_guard_present", identity_guard_present, "C=1 route labelled bookkeeping identity only"),
        ("V693_7_no_numeric_coefficients_promoted", no_numeric_coefficients, "no C_gamma_TF/C_slip_TF numeric or theorem-zero row"),
        ("V693_8_runner_rules_complete", rules_complete, f"rule_rows={len(rule_rows)}"),
        ("V693_9_claim_gates_block", gates_block, "claim gates block coefficients and local promotion"),
        ("V693_10_no_claim_rows_promoted", no_claim_rows, "all generated 693 rows remain valid_for_claim=false"),
        ("V693_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V693_12_generated_outputs_scoped", scoped_outputs, "all 693 outputs target post-checkpoint-work"),
        ("V693_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V693_14_status_nonclaim", "no_Cgamma_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    retained_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 693 - Y5 R10 TF Shear To Gamma Slip Coefficient Derivation Or Retained Bound

## Verdict

693 tries to derive the missing bridge:

```text
delta_gamma_TF = C_gamma_TF * epsilon_TF
delta_slip_TF  = C_slip_TF  * epsilon_TF
```

The honest result is an operator-norm contract, not a numeric coefficient. In an EH weak-field branch the trace-free spatial equation gives the right shape: a trace-free source acted on by an inverse elliptic/Green operator produces slip, and `gamma-1` is a normalization of that response against the Newtonian/source potential. But the current corpus does not yet fix the physical `epsilon_TF`, same-frame denominator, boundary conditions, source normalization, or EH/R11 operator branch.

Important guardrail: `C=1` is allowed only as a bookkeeping identity if `epsilon_TF` is defined as the observable residual itself. That is not an independent MTS prediction.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Coefficient Derivation Attempt

{markdown_table(derivation_rows, ["attempt_id", "target", "result", "coefficient_effect", "blocker", "valid_for_claim"])}

## Operator Norm Contract

{markdown_table(contract_rows, ["contract_id", "coefficient", "formal_definition", "required_inputs", "current_status", "allowed_use", "valid_for_claim"])}

## Retained Bound Template

{markdown_table(retained_rows, ["template_id", "field", "required_evidence", "current_status", "why_needed", "valid_for_claim"])}

## Runner Update Rules

{markdown_table(rule_rows, ["rule_id", "target_runner", "rule", "failure_mode", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    derivation_rows = coefficient_derivation_rows()
    contract_rows = operator_norm_contract_rows()
    retained_rows = retained_bound_template_rows()
    rule_rows = runner_update_rule_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        derivation_rows,
        contract_rows,
        retained_rows,
        rule_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_693_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_COEFFICIENT_DERIVATION_ATTEMPT.csv", derivation_rows, ["attempt_id", "target", "derivation_step", "result", "coefficient_effect", "blocker", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_OPERATOR_NORM_CONTRACT.csv", contract_rows, ["contract_id", "coefficient", "formal_definition", "required_inputs", "current_status", "allowed_use", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_RETAINED_BOUND_TEMPLATE.csv", retained_rows, ["template_id", "field", "required_evidence", "current_status", "why_needed", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_RUNNER_UPDATE_RULES.csv", rule_rows, ["rule_id", "target_runner", "rule", "failure_mode", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_693_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_693_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, derivation_rows, contract_rows, retained_rows, rule_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"derivation_rows={len(derivation_rows)}")
    print(f"contract_rows={len(contract_rows)}")
    print(f"retained_rows={len(retained_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
