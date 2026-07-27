from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_MHref_same_frame_denominator_missing_BTF_product_bound_guard_written_nonclaim"
CLAIM_CEILING = "MHref_denominator_and_BTF_product_guard_only_no_MHref_value_no_BTF_value_no_epsilon_TF_no_PPN_score_no_R10_no_local_GR_claim"
NEXT_TARGET = "697-Y5-R10-MHref-source-normalization-certificate-or-denominator-fill-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "678_doc": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
    "691_doc": ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md",
    "692_doc": ROOT / "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md",
    "693_doc": ROOT / "693-Y5-R10-TF-shear-to-gamma-slip-coefficient-derivation-or-retained-bound.md",
    "694_doc": ROOT / "694-Y5-R10-epsilon-TF-numerator-denominator-contract-or-first-fill-row.md",
    "695_doc": ROOT / "695-Y5-R10-BTF-over-MH-theorem-zero-or-source-bound-acquisition.md",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "691_validation": RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    "692_validation": RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv",
    "693_validation": RESIDUALS / "P8_Y5_BRR545_693_VALIDATION.csv",
    "694_validation": RESIDUALS / "P8_Y5_BRR545_694_VALIDATION.csv",
    "695_validation": RESIDUALS / "P8_Y5_BRR545_695_VALIDATION.csv",
    "678_bx_gate": RESIDUALS / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "692_targets": RESIDUALS / "P8_Y5_R10_692_SOURCE_LOCKED_PPN_TARGETS.csv",
    "693_operator_contract": RESIDUALS / "P8_Y5_R10_693_OPERATOR_NORM_CONTRACT.csv",
    "693_retained_template": RESIDUALS / "P8_Y5_R10_693_RETAINED_BOUND_TEMPLATE.csv",
    "694_contract": RESIDUALS / "P8_Y5_R10_694_EPSILON_TF_DEFINITION_CONTRACT.csv",
    "694_denominator": RESIDUALS / "P8_Y5_R10_694_DENOMINATOR_COMPONENTS.csv",
    "694_first_fill": RESIDUALS / "P8_Y5_R10_694_FIRST_FILL_ROW.csv",
    "695_btf_fill": RESIDUALS / "P8_Y5_R10_695_BTF_FIRST_FILL_ROW.csv",
    "695_product_smoke": RESIDUALS / "P8_Y5_R10_695_PRODUCT_BOUND_SMOKE.csv",
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


def first_row_with(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(field) == value:
            return row
    return {}


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
        "678_doc": "boundary class/projector predecessor showing source normalization is not filled",
        "691_doc": "metric shear source-pack predecessor",
        "692_doc": "source-locked PPN target predecessor",
        "693_doc": "operator-norm coefficient predecessor",
        "694_doc": "epsilon_TF numerator/denominator contract predecessor",
        "695_doc": "B_TF_over_MH theorem-zero/source-bound predecessor",
        "678_validation": "678 validation gate",
        "691_validation": "691 validation gate",
        "692_validation": "692 validation gate",
        "693_validation": "693 validation gate",
        "694_validation": "694 validation gate",
        "695_validation": "695 validation gate",
        "678_bx_gate": "BX source row gate with M_H_ref dependency",
        "boundary_reference_status": "current M_H_ref claim-valid status",
        "692_targets": "source-locked gamma/beta target table",
        "693_operator_contract": "C_gamma_TF/C_slip_TF operator contract",
        "693_retained_template": "retained coefficient bound template",
        "694_contract": "epsilon_TF denominator contract",
        "694_denominator": "denominator component ledger",
        "694_first_fill": "epsilon_TF first fill row",
        "695_btf_fill": "B_TF_over_MH first fill row",
        "695_product_smoke": "gamma/slip product-bound smoke rows",
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


def mhref_denominator_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "MHA696_0_target",
            "clause": "M_H_ref is the denominator for B_TF_over_MH and epsilon_TF",
            "required_state": "positive Hilbert/source mass denominator tied to measured GM",
            "observed_state": "claim_valid_data_rows=0; status=missing_claim_valid_source_or_zero_theorem",
            "result": "fail_missing_claim_ready_M_H_ref",
            "blocker": "boundary reference first-row status has no claim-valid M_H_ref data row",
            "allowed_use_now": "nonclaim_denominator_target_only",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_denominator", "695_btf_fill"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_1_same_frame",
            "clause": "numerator and denominator are read in one source/metric/clock/boundary frame",
            "required_state": "same_frame_certificate with source_frame=metric_frame=clock_frame=boundary_domain",
            "observed_state": "MISSING_SAME_FRAME_CERTIFICATE",
            "result": "fail_missing_same_frame_certificate",
            "blocker": "694 denominator ledger and 695 fill row keep same-frame convention missing",
            "allowed_use_now": "nonclaim_schema_guard_only",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator", "695_btf_fill"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_2_counterterm",
            "clause": "boundary exact/counterterm convention does not subtract physical source mass",
            "required_state": "counterterm_reference_guard with physical GM preserved",
            "observed_state": "MISSING_COUNTERTERM_REFERENCE_GUARD",
            "result": "fail_missing_counterterm_guard",
            "blocker": "denominator could otherwise be altered by the same boundary convention being tested",
            "allowed_use_now": "nonclaim_schema_guard_only",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_3_measured_GM",
            "clause": "M_H_ref is tied to observed mass/GM normalization",
            "required_state": "measured_GM_link and equation_ref are source-backed",
            "observed_state": "MISSING_MEASURED_GM_LINK",
            "result": "fail_missing_observed_mass_link",
            "blocker": "no row identifies whether the denominator is Hilbert mass, Keplerian GM, ADM-like mass, or a local source convention",
            "allowed_use_now": "nonclaim_denominator_target_only",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_denominator"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_4_domain",
            "clause": "denominator belongs to the same boundary/projector/arena domain as B_TF_obs",
            "required_state": "boundary_domain and arena_projection are explicit",
            "observed_state": "MISSING_BOUNDARY_DOMAIN",
            "result": "fail_missing_domain",
            "blocker": "B_TF numerator and M_H denominator cannot be divided if they come from different domains",
            "allowed_use_now": "nonclaim_schema_guard_only",
            "valid_for_claim": "false",
            "source_paths": source_list("678_bx_gate", "694_denominator", "695_btf_fill"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_5_Mref_candidate",
            "clause": "fallback M_ref candidate is allowed only as an explicitly labelled nonclaim engineering denominator",
            "required_state": "same-frame M_ref candidate with warning label and no promotion to claim",
            "observed_state": "MISSING_SAME_FRAME_M_REF_CANDIDATE",
            "result": "fail_missing_fallback_candidate",
            "blocker": "fallback denominator is not present either",
            "allowed_use_now": "nonclaim_template_only",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator"),
            "generated_utc": now,
        },
        {
            "audit_id": "MHA696_6_verdict",
            "clause": "claim-ready M_H_ref",
            "required_state": "MHA696_0 through MHA696_5 pass",
            "observed_state": "M_H_ref remains unfilled",
            "result": "fail_current_corpus",
            "blocker": "no positive value, no theorem-owned source normalization, no same-frame certificate, and no counterterm guard",
            "allowed_use_now": "source_normalization_certificate_or_first_fill_row_next",
            "valid_for_claim": "false",
            "source_paths": source_list("694_doc", "695_doc", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def same_frame_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "contract_id": "SFC696_0_required_columns",
            "contract_clause": "claim-ready denominator row schema",
            "required_columns": "M_H_ref;units;source_frame;metric_frame;clock_frame;boundary_domain;counterterm_convention;measured_GM_link;equation_ref;source_path;valid_for_claim",
            "acceptance_rule": "all columns numeric or source-backed where appropriate; no MISSING markers",
            "current_status": "MISSING_CLAIM_READY_DENOMINATOR_ROW",
            "failure_effect": "B_TF_over_MH and epsilon_TF remain unscoreable",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator", "695_btf_fill"),
            "generated_utc": now,
        },
        {
            "contract_id": "SFC696_1_same_frame_acceptance",
            "contract_clause": "source, metric, clock, and boundary frame equality",
            "required_columns": "source_frame;metric_frame;clock_frame;boundary_domain",
            "acceptance_rule": "same declared convention and source path for all four frame/domain fields",
            "current_status": "MISSING_SAME_FRAME_CERTIFICATE",
            "failure_effect": "prevents numerator/denominator mixing",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator"),
            "generated_utc": now,
        },
        {
            "contract_id": "SFC696_2_counterterm_acceptance",
            "contract_clause": "counterterm convention cannot remove measured mass",
            "required_columns": "counterterm_convention;measured_GM_link;equation_ref",
            "acceptance_rule": "explicit proof or source row says boundary convention preserves physical source normalization",
            "current_status": "MISSING_COUNTERTERM_REFERENCE_GUARD",
            "failure_effect": "blocks denominator promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_denominator"),
            "generated_utc": now,
        },
        {
            "contract_id": "SFC696_3_nonclaim_candidate",
            "contract_clause": "fallback denominator may be used for smoke only",
            "required_columns": "M_ref_candidate;warning_label;valid_for_claim=false",
            "acceptance_rule": "candidate is never used as MTS evidence unless upgraded by SFC696_0 through SFC696_2",
            "current_status": "MISSING_SAME_FRAME_M_REF_CANDIDATE",
            "failure_effect": "no smoke denominator available yet",
            "valid_for_claim": "false",
            "source_paths": source_list("694_denominator"),
            "generated_utc": now,
        },
    ]


def btf_product_bound_guard_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "guard_id": "PBG696_0_gamma_product",
            "observable": "gamma_minus_1",
            "source_locked_bound": "2.3e-5",
            "product_expression": "abs(C_gamma_TF * B_TF_over_MH) <= 2.3e-5",
            "required_assumptions": "all other residuals vanish; C_gamma_TF is fixed; B_TF_over_MH is already defined",
            "observed_state": "PRODUCT_BOUND_ONLY_NOT_BTF_VALUE",
            "why_not_invertible": "C_gamma_TF and M_H_ref are missing, and other residuals are not separated",
            "allowed_use_now": "pressure_test_only",
            "valid_for_claim": "false",
            "source_paths": source_list("692_targets", "693_operator_contract", "695_product_smoke"),
            "generated_utc": now,
        },
        {
            "guard_id": "PBG696_1_uninvertible_without_C",
            "observable": "gamma_minus_1",
            "source_locked_bound": "2.3e-5",
            "product_expression": "B_TF_over_MH <= 2.3e-5 / abs(C_gamma_TF)",
            "required_assumptions": "numeric parent-derived nonzero C_gamma_TF bound",
            "observed_state": "MISSING_C_GAMMA_TF_BOUND",
            "why_not_invertible": "operator-norm coefficient is a contract, not a number",
            "allowed_use_now": "no_bound_extraction",
            "valid_for_claim": "false",
            "source_paths": source_list("693_operator_contract", "693_retained_template"),
            "generated_utc": now,
        },
        {
            "guard_id": "PBG696_2_uninvertible_without_MH",
            "observable": "B_TF_over_MH",
            "source_locked_bound": "MISSING_DIRECT_BOUND",
            "product_expression": "B_TF_over_MH = norm(B_TF_obs)/M_H_ref",
            "required_assumptions": "positive same-frame M_H_ref",
            "observed_state": "MISSING_CLAIM_READY_M_H_REF",
            "why_not_invertible": "dimensionless ratio cannot be formed without the denominator",
            "allowed_use_now": "source_row_only",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "695_btf_fill"),
            "generated_utc": now,
        },
        {
            "guard_id": "PBG696_3_no_shortcut",
            "observable": "local_GR_or_PPN_pass",
            "source_locked_bound": "blocked",
            "product_expression": "gamma product guard cannot replace M_H_ref, B_TF_over_MH, or epsilon_TF",
            "required_assumptions": "all numerator and denominator branches are claim-ready",
            "observed_state": "guardrail_active",
            "why_not_invertible": "a product pressure is not a prediction and cannot be counted as a pass",
            "allowed_use_now": "prevents_false_promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "693_doc", "694_doc", "695_doc"),
            "generated_utc": now,
        },
    ]


def first_denominator_fill_row() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fill_id": "MHR696_0_first_M_H_ref_fill",
            "target_rows": "DEN694_0_M_H_ref;BTF695_0_first_B_TF_over_MH_fill",
            "quantity": "M_H_ref",
            "formula": "positive Hilbert/source mass denominator tied to measured GM in same frame",
            "value": "MISSING_POSITIVE_M_H_REF_VALUE",
            "units": "MISSING_UNITS",
            "positive_required": "true",
            "source_frame": "MISSING_SOURCE_FRAME",
            "metric_frame": "MISSING_METRIC_FRAME",
            "clock_frame": "MISSING_CLOCK_FRAME",
            "boundary_domain": "MISSING_BOUNDARY_DOMAIN",
            "counterterm_convention": "MISSING_COUNTERTERM_CONVENTION",
            "measured_GM_link": "MISSING_MEASURED_GM_LINK",
            "equation_ref": "MISSING_EQUATION_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "unfilled_after_same_frame_audit",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_denominator", "695_btf_fill"),
            "generated_utc": now,
        }
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "E696_0_MHref_denominator",
            "target": "M_H_ref",
            "observed_state": "claim_valid_data_rows=0; MISSING_CLAIM_READY_M_H_REF",
            "result": "fail_blocked",
            "claim_effect": "no denominator value",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_denominator"),
            "generated_utc": now,
        },
        {
            "eval_id": "E696_1_BTF_over_MH",
            "target": "B_TF_over_MH",
            "observed_state": "B_TF_obs_norm and M_H_ref missing",
            "result": "fail_blocked",
            "claim_effect": "no B_TF_over_MH value or theorem-zero",
            "valid_for_claim": "false",
            "source_paths": source_list("695_btf_fill"),
            "generated_utc": now,
        },
        {
            "eval_id": "E696_2_gamma_product",
            "target": "C_gamma_TF * B_TF_over_MH",
            "observed_state": "gamma target source-locked but coefficient and denominator missing",
            "result": "nonclaim_product_pressure_only",
            "claim_effect": "cannot infer B_TF_over_MH or score gamma",
            "valid_for_claim": "false",
            "source_paths": source_list("692_targets", "693_operator_contract", "695_product_smoke"),
            "generated_utc": now,
        },
        {
            "eval_id": "E696_3_epsilon_TF",
            "target": "epsilon_TF",
            "observed_state": "physical numerator and denominator both missing",
            "result": "fail_blocked",
            "claim_effect": "no epsilon_TF, PPN, R10, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("694_contract", "694_first_fill", "695_btf_fill"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    gates = [
        (
            "CG696_0_MHref_source",
            "M_H_ref source normalization",
            "positive source-backed denominator",
            "MISSING_POSITIVE_M_H_REF_VALUE",
            "fail_blocked",
            "blocks B_TF_over_MH",
            "boundary_reference_status",
        ),
        (
            "CG696_1_same_frame_certificate",
            "same-frame certificate",
            "source/metric/clock/boundary frames match",
            "MISSING_SAME_FRAME_CERTIFICATE",
            "fail_blocked",
            "blocks numerator/denominator division",
            "694_denominator",
        ),
        (
            "CG696_2_counterterm_guard",
            "counterterm guard",
            "physical GM not subtracted by reference convention",
            "MISSING_COUNTERTERM_REFERENCE_GUARD",
            "fail_blocked",
            "blocks denominator promotion",
            "694_denominator",
        ),
        (
            "CG696_3_BTF_value",
            "B_TF_over_MH value",
            "numeric value or theorem-zero",
            "MISSING_VALUE_OR_THEOREM_ZERO",
            "fail_blocked",
            "blocks epsilon_TF numerator",
            "695_btf_fill",
        ),
        (
            "CG696_4_product_bound_inversion",
            "gamma product inversion",
            "numeric C_gamma_TF and isolated residual branch",
            "PRODUCT_BOUND_ONLY_NOT_BTF_VALUE",
            "fail_nonclaim",
            "prevents using gamma bound as B_TF value",
            "695_product_smoke",
        ),
        (
            "CG696_5_local_claim",
            "PPN/R10/local-GR claim",
            "M_H_ref, B_TF_over_MH, epsilon_TF, and coefficient rows all valid",
            "no_MHref_value_no_BTF_value_no_epsilon_TF",
            "fail_blocked",
            "no PPN score, no R10 pass, no local-GR claim",
            "692_targets",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "required_state": required_state,
            "observed_state": observed_state,
            "result": result,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list(source_id),
            "generated_utc": now,
        }
        for gate_id, gate, required_state, observed_state, result, claim_effect, source_id in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D696_0_zero_or_value",
            "target": "M_H_ref",
            "result": "not_filled",
            "reason": "denominator has no positive value, same-frame certificate, measured-GM link, or counterterm guard",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D696_1_product_shortcut",
            "target": "gamma product bound",
            "result": "rejected_as_claim_route",
            "reason": "gamma can bound only C_gamma_TF * B_TF_over_MH under strong assumptions; it cannot supply M_H_ref or B_TF_over_MH",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D696_2_next",
            "target": "source normalization certificate or denominator fill row",
            "result": "selected",
            "reason": "the shortest honest route is now to fill/certify the denominator before trying another PPN score",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S696_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "M_H_ref remains missing; product-bound guard prevents gamma pressure from being misread as a B_TF_over_MH value",
            "hardest_blocker": "same-frame positive denominator tied to measured GM and protected from boundary counterterm ambiguity",
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
    denominator_rows: list[dict[str, str]],
    same_frame_rows: list[dict[str, str]],
    product_guard_rows: list[dict[str, str]],
    first_fill_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "denominator": denominator_rows,
        "same_frame": same_frame_rows,
        "product_guard": product_guard_rows,
        "first_fill": first_fill_rows,
        "evaluator": evaluator_rows_,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["678_validation", "691_validation", "692_validation", "693_validation", "694_validation", "695_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    boundary_status = first_row_with(read_csv(SOURCE_PATHS["boundary_reference_status"]), "quantity", "M_H_ref")
    btf_fill = read_csv(SOURCE_PATHS["695_btf_fill"])[0]
    product_smoke = read_csv(SOURCE_PATHS["695_product_smoke"])
    denominator_complete = len(denominator_rows) == 7 and all(row["valid_for_claim"] == "false" for row in denominator_rows)
    same_frame_complete = len(same_frame_rows) == 4 and all(row["valid_for_claim"] == "false" for row in same_frame_rows)
    same_frame_missing = all("MISSING_" in row["current_status"] for row in same_frame_rows)
    product_guard_complete = len(product_guard_rows) == 4 and all(row["valid_for_claim"] == "false" for row in product_guard_rows)
    product_nonclaim = any(row["observed_state"] == "PRODUCT_BOUND_ONLY_NOT_BTF_VALUE" for row in product_guard_rows)
    first_fill_complete = len(first_fill_rows) == 1 and first_fill_rows[0]["valid_for_claim"] == "false"
    missing_fields = [
        "value",
        "units",
        "source_frame",
        "metric_frame",
        "clock_frame",
        "boundary_domain",
        "counterterm_convention",
        "measured_GM_link",
        "equation_ref",
        "source_path",
    ]
    first_fill_missing = all("MISSING_" in first_fill_rows[0][field] for field in missing_fields)
    mhref_boundary_blocked = (
        boundary_status.get("claim_valid_data_rows") == "0"
        and boundary_status.get("status") == "missing_claim_valid_source_or_zero_theorem"
        and boundary_status.get("valid_for_claim") == "false"
    )
    btf_still_blocked = (
        btf_fill.get("M_H_ref") == "MISSING_CLAIM_READY_M_H_REF"
        and btf_fill.get("valid_for_claim") == "false"
    )
    product_not_inverted = all(row.get("valid_for_claim") == "false" for row in product_smoke) and any(
        row.get("claim_status") == "not_a_BTF_value_not_a_prediction_not_a_pass" for row in product_smoke
    )
    evaluator_blocks = len(evaluator_rows_) == 4 and all(row["valid_for_claim"] == "false" for row in evaluator_rows_)
    gates_block = len(gate_rows) == 6 and all(row["valid_for_claim"] == "false" for row in gate_rows) and all(
        row["result"].startswith("fail") for row in gate_rows
    )
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_696_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_696_SAME_FRAME_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_696_BTF_PRODUCT_BOUND_GUARD.csv",
        RESIDUALS / "P8_Y5_R10_696_FIRST_DENOMINATOR_FILL_ROW.csv",
        RESIDUALS / "P8_Y5_R10_696_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_696_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_696_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_696_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_696_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V696_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V696_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V696_2_boundary_MHref_status_blocks", mhref_boundary_blocked, f"M_H_ref_status={boundary_status.get('status', 'missing_row')};claim_valid_data_rows={boundary_status.get('claim_valid_data_rows', 'missing')}"),
        ("V696_3_denominator_audit_complete", denominator_complete, f"denominator_rows={len(denominator_rows)}"),
        ("V696_4_same_frame_contract_complete", same_frame_complete and same_frame_missing, f"same_frame_rows={len(same_frame_rows)}"),
        ("V696_5_product_bound_guard_complete", product_guard_complete and product_nonclaim, f"product_guard_rows={len(product_guard_rows)}"),
        ("V696_6_first_denominator_fill_unfilled", first_fill_complete and first_fill_missing, "first denominator fill row written with missing fields retained"),
        ("V696_7_BTF_fill_remains_blocked", btf_still_blocked, f"BTF_M_H_ref={btf_fill.get('M_H_ref', 'missing')}"),
        ("V696_8_gamma_product_not_inverted", product_not_inverted, "product smoke remains not_a_BTF_value_not_a_prediction_not_a_pass"),
        ("V696_9_evaluator_and_gates_block", evaluator_blocks and gates_block, "evaluators and gates block local promotion"),
        ("V696_10_no_claim_rows_promoted", no_claim_rows, "all generated 696 rows remain valid_for_claim=false"),
        ("V696_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V696_12_generated_outputs_scoped", scoped_outputs, "all 696 outputs target post-checkpoint-work"),
        ("V696_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V696_14_status_nonclaim", "no_MHref_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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
    denominator_rows: list[dict[str, str]],
    same_frame_rows: list[dict[str, str]],
    product_guard_rows: list[dict[str, str]],
    first_fill_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 696 - Y5 R10 MHref Same Frame Denominator Or BTF Product Bound Guard

## Verdict

696 checks whether the missing denominator can be filled before the local PPN branch tries to use the trace-free shear channel:

```text
B_TF_over_MH = ||B_TF_obs|| / M_H_ref
epsilon_TF   = N_TF / D_TF
```

The answer is still no. `M_H_ref` has no claim-valid positive value, no same-frame source/metric/clock/boundary certificate, no measured-GM normalization link, and no counterterm guard.

The useful result is a guardrail: the source-locked gamma target can only impose a product pressure such as `abs(C_gamma_TF * B_TF_over_MH) <= 2.3e-5` under strong assumptions. It cannot be inverted into a `B_TF_over_MH` value while `C_gamma_TF` and `M_H_ref` are missing.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## MHref Denominator Audit

{markdown_table(denominator_rows, ["audit_id", "clause", "observed_state", "result", "blocker", "allowed_use_now", "valid_for_claim"])}

## Same Frame Contract

{markdown_table(same_frame_rows, ["contract_id", "contract_clause", "required_columns", "current_status", "failure_effect", "valid_for_claim"])}

## BTF Product Bound Guard

{markdown_table(product_guard_rows, ["guard_id", "observable", "source_locked_bound", "product_expression", "observed_state", "why_not_invertible", "valid_for_claim"])}

## First Denominator Fill Row

{markdown_table(first_fill_rows, ["fill_id", "quantity", "formula", "value", "units", "source_frame", "measured_GM_link", "source_path", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim"])}

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
    denominator_rows = mhref_denominator_audit_rows()
    same_frame_rows = same_frame_contract_rows()
    product_guard_rows = btf_product_bound_guard_rows()
    first_fill_rows = first_denominator_fill_row()
    evaluator_rows_ = evaluator_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        denominator_rows,
        same_frame_rows,
        product_guard_rows,
        first_fill_rows,
        evaluator_rows_,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_696_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv", denominator_rows, ["audit_id", "clause", "required_state", "observed_state", "result", "blocker", "allowed_use_now", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_SAME_FRAME_CONTRACT.csv", same_frame_rows, ["contract_id", "contract_clause", "required_columns", "acceptance_rule", "current_status", "failure_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_BTF_PRODUCT_BOUND_GUARD.csv", product_guard_rows, ["guard_id", "observable", "source_locked_bound", "product_expression", "required_assumptions", "observed_state", "why_not_invertible", "allowed_use_now", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_FIRST_DENOMINATOR_FILL_ROW.csv", first_fill_rows, ["fill_id", "target_rows", "quantity", "formula", "value", "units", "positive_required", "source_frame", "metric_frame", "clock_frame", "boundary_domain", "counterterm_convention", "measured_GM_link", "equation_ref", "source_path", "derivation_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_EVALUATOR.csv", evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_696_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_696_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, denominator_rows, same_frame_rows, product_guard_rows, first_fill_rows, evaluator_rows_, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"denominator_rows={len(denominator_rows)}")
    print(f"same_frame_rows={len(same_frame_rows)}")
    print(f"product_guard_rows={len(product_guard_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
