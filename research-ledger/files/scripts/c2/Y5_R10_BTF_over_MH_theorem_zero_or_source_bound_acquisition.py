from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_BTF_over_MH_zero_theorem_failed_source_bound_row_written_unfilled_nonclaim"
CLAIM_CEILING = "BTF_over_MH_zero_or_source_bound_acquisition_only_no_BTF_value_no_epsilon_TF_no_PPN_score_no_R10_no_local_GR_claim"
NEXT_TARGET = "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "695-Y5-R10-BTF-over-MH-theorem-zero-or-source-bound-acquisition.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "353_doc": ROOT / "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
    "354_doc": ROOT / "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
    "357_doc": ROOT / "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
    "549_doc": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "678_doc": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
    "691_doc": ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md",
    "692_doc": ROOT / "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md",
    "693_doc": ROOT / "693-Y5-R10-TF-shear-to-gamma-slip-coefficient-derivation-or-retained-bound.md",
    "694_doc": ROOT / "694-Y5-R10-epsilon-TF-numerator-denominator-contract-or-first-fill-row.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "691_validation": RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    "692_validation": RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv",
    "693_validation": RESIDUALS / "P8_Y5_BRR545_693_VALIDATION.csv",
    "694_validation": RESIDUALS / "P8_Y5_BRR545_694_VALIDATION.csv",
    "691_source_pack": RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv",
    "692_targets": RESIDUALS / "P8_Y5_R10_692_SOURCE_LOCKED_PPN_TARGETS.csv",
    "693_retained_template": RESIDUALS / "P8_Y5_R10_693_RETAINED_BOUND_TEMPLATE.csv",
    "694_contract": RESIDUALS / "P8_Y5_R10_694_EPSILON_TF_DEFINITION_CONTRACT.csv",
    "694_numerator": RESIDUALS / "P8_Y5_R10_694_NUMERATOR_COMPONENTS.csv",
    "694_first_fill": RESIDUALS / "P8_Y5_R10_694_FIRST_FILL_ROW.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
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
        "352_doc": "B_TF symbolic PPN source and boundary no-hair opening",
        "353_doc": "boundary no-hair contract and explicit B_TF failure",
        "354_doc": "source-locked gamma target and no-hair debt sharpening",
        "357_doc": "retained PPN residual map with C_TF epsilon_TF",
        "549_doc": "boundary cohomology/nohair certificate failure pattern",
        "678_doc": "boundary-class/nohair/projector silence stack failure",
        "691_doc": "metric shear B_TF source-pack predecessor",
        "692_doc": "source-locked gamma/beta guardrail runner",
        "693_doc": "coefficient operator-norm contract predecessor",
        "694_doc": "epsilon_TF numerator/denominator contract predecessor",
        "549_validation": "549 validation gate",
        "678_validation": "678 validation gate",
        "691_validation": "691 validation gate",
        "692_validation": "692 validation gate",
        "693_validation": "693 validation gate",
        "694_validation": "694 validation gate",
        "691_source_pack": "B_TF_over_MH source-pack row",
        "692_targets": "source-locked gamma/beta target table",
        "693_retained_template": "coefficient retained bound template",
        "694_contract": "epsilon_TF contract",
        "694_numerator": "B_TF numerator component row",
        "694_first_fill": "epsilon_TF first fill row",
        "boundary_reference_status": "M_H_ref denominator status",
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


def btf_zero_theorem_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "BZA695_0_target",
            "zero_clause": "B_TF_over_MH = 0",
            "mathematical_test": "physical observed trace-free boundary stress/shear vanishes before PPN readout",
            "current_result": "target_defined",
            "blocker": "target definition is not proof",
            "fallback_row": "BFA695_0_B_TF_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "691_source_pack", "694_numerator"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_1_class_only_boundary",
            "zero_clause": "boundary action has no angular/marker trace-free channel",
            "mathematical_test": "S_boundary depends only on total class/charge/scalar volume so variation is pure trace/monopole",
            "current_result": "conditional_not_parent_signed",
            "blocker": "353/354 sharpen this route but do not derive it from parent action",
            "fallback_row": "BFA695_0_B_TF_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "354_doc", "691_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_2_relative_class",
            "zero_clause": "relative boundary class trivial before local readout",
            "mathematical_test": "exact/improvement boundary terms carry no finite linked trace-free charge",
            "current_result": "not_signed",
            "blocker": "549/678 keep relative class selection as a contract, not a parent-selected theorem",
            "fallback_row": "BFA695_1_boundary_class_factor",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_3_no_vector_tensor_marker_hair",
            "zero_clause": "no physical vector/tensor/shear/radial/time boundary hair",
            "mathematical_test": "Pi_vector=Pi_TF=Pi_shear=Pi_radial=Pi_time=0 on the allowed local shell",
            "current_result": "not_derived",
            "blocker": "current corpus explicitly says scalar/trace silence does not remove vector/tensor/shear hair",
            "fallback_row": "BFA695_2_hair_profile",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "678_doc", "691_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_4_Ward_Bianchi",
            "zero_clause": "boundary flux obeys owned Ward/Bianchi closure",
            "mathematical_test": "trace-free boundary flux is zero or exactly balanced by a conserved owned boundary charge",
            "current_result": "conditional_open",
            "blocker": "Ward maps exist, but signs/couplings/local boundary flux equation are not parent-derived",
            "fallback_row": "BFA695_3_Ward_flux_factor",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "549_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_5_denominator_guard",
            "zero_clause": "B_TF_over_MH uses fixed same-frame denominator",
            "mathematical_test": "M_H_ref/source mass is fixed and not altered by boundary counterterms",
            "current_result": "blocked",
            "blocker": "boundary reference status still lacks claim-ready M_H_ref",
            "fallback_row": "BFA695_4_MH_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_contract"),
            "generated_utc": now,
        },
        {
            "audit_id": "BZA695_6_verdict",
            "zero_clause": "B_TF_over_MH theorem-zero",
            "mathematical_test": "all BZA695_1 through BZA695_5 pass",
            "current_result": "fail_current_corpus",
            "blocker": "class-only action, relative class, no-hair, Ward closure, and denominator are not jointly signed",
            "fallback_row": "BFA695_source_bound_required",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "694_contract"),
            "generated_utc": now,
        },
    ]


def source_bound_acquisition_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "BFA695_0_B_TF_over_MH",
            "B_TF_over_MH",
            "value_or_theorem_zero;units;boundary_domain;frame_convention;M_H_ref;source_path;equation_ref;extraction_method;valid_for_claim",
            "MISSING_VALUE_OR_THEOREM_ZERO",
            "direct fill for first epsilon_TF numerator component",
        ),
        (
            "BFA695_1_boundary_class_factor",
            "boundary_class_or_exactness_factor",
            "relative_class;exact_improvement_guard;proper_charge_guard;source_path;valid_for_claim",
            "MISSING_BOUNDARY_CLASS_CERTIFICATE",
            "required before exact boundary terms can be treated as zero",
        ),
        (
            "BFA695_2_hair_profile",
            "B_TF_time_radial_frame_profile",
            "partial_t;partial_r;frame_dependence;l_ge_2_profile;source_path;valid_for_claim",
            "MISSING_B_TF_PROFILE",
            "keeps beta/Gdot/preferred-frame leakage explicit",
        ),
        (
            "BFA695_3_Ward_flux_factor",
            "Ward_Bianchi_TF_flux_closure",
            "flux_equation;balanced_charge;conservation_status;source_path;valid_for_claim",
            "MISSING_WARD_BIANCHI_TF_FLUX_CLOSURE",
            "needed to forbid hidden trace-free exchange",
        ),
        (
            "BFA695_4_MH_ref",
            "M_H_ref_denominator",
            "M_H_ref;units;source_frame;counterterm_convention;source_path;valid_for_claim",
            "MISSING_CLAIM_READY_M_H_REF",
            "B_TF_over_MH is meaningless without same-frame denominator",
        ),
        (
            "BFA695_5_gamma_product_guard",
            "C_gamma_TF_times_B_TF_over_MH",
            "C_gamma_TF;B_TF_over_MH;gamma_target;all_other_residuals_zero_assumption;valid_for_claim",
            "PRODUCT_BOUND_ONLY_NOT_BTF_VALUE",
            "gamma target can constrain only a product unless coefficient and denominator are real",
        ),
    ]
    return [
        {
            "acquisition_id": acquisition_id,
            "quantity": quantity,
            "required_columns": required_columns,
            "current_status": current_status,
            "why_needed": why_needed,
            "source_strategy": "parent_theorem_zero_or_source_backed_numeric_bound_no_proxy_claim",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "694_numerator", "boundary_reference_status"),
            "generated_utc": now,
        }
        for acquisition_id, quantity, required_columns, current_status, why_needed in rows
    ]


def first_fill_row() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fill_id": "BTF695_0_first_B_TF_over_MH_fill",
            "target_epsilon_row": "ETF694_0_epsilon_TF_first_fill",
            "quantity": "B_TF_over_MH",
            "formula": "norm(B_TF_obs)/M_H_ref",
            "value_or_theorem_zero": "MISSING_VALUE_OR_THEOREM_ZERO",
            "B_TF_obs_norm": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "M_H_ref": "MISSING_CLAIM_READY_M_H_REF",
            "units": "dimensionless",
            "boundary_domain": "MISSING_BOUNDARY_DOMAIN",
            "frame_convention": "MISSING_SAME_FRAME_CONVENTION",
            "equation_ref": "MISSING_EQUATION_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "unfilled_after_zero_theorem_failure",
            "valid_for_claim": "false",
            "source_paths": source_list("694_first_fill", "691_source_pack", "boundary_reference_status"),
            "generated_utc": now,
        }
    ]


def product_bound_smoke_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "smoke_id": "PBS695_0_gamma_product",
            "observable": "gamma_minus_1",
            "source_locked_target": "2.3e-5",
            "product_bound": "abs(C_gamma_TF * B_TF_over_MH) <= 2.3e-5 only if all other residuals vanish",
            "why_not_BTF_bound": "C_gamma_TF, M_H_ref, B_TF source, and other residual separation are missing",
            "claim_status": "not_a_BTF_value_not_a_prediction_not_a_pass",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "692_targets", "693_retained_template"),
            "generated_utc": now,
        },
        {
            "smoke_id": "PBS695_1_slip_product",
            "observable": "Phi_minus_Psi_or_lensing_slip",
            "source_locked_target": "MISSING_DIRECT_SOURCE_LOCK",
            "product_bound": "abs(C_slip_TF * B_TF_over_MH) requires direct slip target or model-specific map",
            "why_not_BTF_bound": "slip target and C_slip_TF are missing",
            "claim_status": "not_a_BTF_value_not_a_prediction_not_a_pass",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "692_targets"),
            "generated_utc": now,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "E695_0_zero_theorem",
            "target": "B_TF_over_MH theorem-zero",
            "observed_state": "BZA695 audit contains failed/conditional clauses",
            "result": "fail_current_corpus",
            "claim_effect": "cannot set B_TF_over_MH=0",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "549_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "eval_id": "E695_1_source_bound",
            "target": "B_TF_over_MH source-bound acquisition",
            "observed_state": "first fill row contains missing value, denominator, domain, frame, equation, and source path",
            "result": "not_evaluated",
            "claim_effect": "no B_TF_over_MH value",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "694_first_fill"),
            "generated_utc": now,
        },
        {
            "eval_id": "E695_2_product_bound",
            "target": "gamma product guard",
            "observed_state": "source-locked gamma gives only product pressure, not B_TF value",
            "result": "smoke_only_nonclaim",
            "claim_effect": "no epsilon_TF or PPN score",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "692_targets", "693_retained_template"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG695_0_zero_theorem",
            "gate": "B_TF_over_MH zero theorem",
            "required_state": "class-only boundary action, relative class, no tensor hair, Ward closure, and denominator all signed",
            "observed_state": "audit remains failed/conditional",
            "result": "fail_blocked",
            "claim_effect": "B_TF_over_MH cannot be theorem-zeroed",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "549_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG695_1_source_bound",
            "gate": "B_TF_over_MH source-bound row",
            "required_state": "numeric or theorem-zero value with units, domain, frame, denominator, source path, equation ref",
            "observed_state": "first row unfilled with MISSING fields",
            "result": "fail_blocked",
            "claim_effect": "no B_TF value",
            "valid_for_claim": "false",
            "source_paths": source_list("694_first_fill"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG695_2_product_bound_guard",
            "gate": "gamma product-bound shortcut guard",
            "required_state": "product-bound smoke never promoted to B_TF value",
            "observed_state": "product smoke rows explicitly nonclaim",
            "result": "pass_guard_only",
            "claim_effect": "prevents false B_TF/M_H acquisition",
            "valid_for_claim": "false",
            "source_paths": source_list("692_targets", "693_retained_template"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG695_3_epsilon_runner",
            "gate": "epsilon_TF runner update",
            "required_state": "B_TF_over_MH and remaining numerator/denominator rows filled",
            "observed_state": "B_TF row unfilled and denominator missing",
            "result": "fail_blocked",
            "claim_effect": "epsilon_TF remains uncomputed",
            "valid_for_claim": "false",
            "source_paths": source_list("694_contract", "694_first_fill"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG695_4_local_claims",
            "gate": "PPN/R10/local-GR promotion",
            "required_state": "B_TF value, epsilon_TF, coefficients, and denominator scoreable",
            "observed_state": "B_TF value missing",
            "result": "fail_policy",
            "claim_effect": "no PPN score, R10, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "693_doc", "694_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG695_5_next",
            "gate": "next target selection",
            "required_state": "choose missing input blocking B_TF_over_MH acquisition",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "attack M_H_ref denominator or product-bound guard next",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "694_contract"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D695_0_zero",
            "target": "B_TF_over_MH zero theorem",
            "result": "failed_current_corpus",
            "reason": "boundary no-hair/class-only/relative-class/Ward/denominator stack is not parent-signed",
            "next_action": "do not set B_TF_over_MH=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D695_1_source_bound",
            "target": "B_TF_over_MH source-bound row",
            "result": "written_unfilled_nonclaim",
            "reason": "the exact acquisition columns are now explicit, but value, denominator, domain, frame, equation, and source path are missing",
            "next_action": "use BTF695_0 as the fill row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D695_2_next",
            "target": "M_H_ref or product-bound guard",
            "result": "selected",
            "reason": "without same-frame M_H_ref, B_TF_over_MH cannot become a dimensionless physical row; gamma gives only product pressure",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S695_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "B_TF_over_MH zero theorem fails for current corpus; source-bound acquisition row is written but unfilled",
            "hardest_blocker": "same-frame M_H_ref plus parent-signed boundary no-hair/class-only action",
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
    zero_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    product_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "zero": zero_rows,
        "acquisition": acquisition_rows,
        "fill": fill_rows,
        "product": product_rows,
        "evaluator": evaluator_rows_,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["549_validation", "678_validation", "691_validation", "692_validation", "693_validation", "694_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    zero_complete = len(zero_rows) == 7 and all(row["valid_for_claim"] == "false" for row in zero_rows)
    zero_not_promoted = not any(row["current_result"] in {"theorem_zero", "pass", "proved"} for row in zero_rows)
    acquisition_complete = len(acquisition_rows) == 6 and all(row["valid_for_claim"] == "false" for row in acquisition_rows)
    acquisition_missing = all(
        "MISSING_" in row["current_status"] or row["current_status"].startswith("PRODUCT_BOUND_ONLY") for row in acquisition_rows
    )
    fill_complete = len(fill_rows) == 1 and fill_rows[0]["valid_for_claim"] == "false"
    fill_missing = all(
        "MISSING_" in fill_rows[0][key]
        for key in ["value_or_theorem_zero", "B_TF_obs_norm", "M_H_ref", "boundary_domain", "frame_convention", "equation_ref", "source_path"]
    )
    product_nonclaim = len(product_rows) == 2 and all(row["claim_status"] == "not_a_BTF_value_not_a_prediction_not_a_pass" for row in product_rows)
    evaluator_blocks = len(evaluator_rows_) == 3 and all(row["valid_for_claim"] == "false" for row in evaluator_rows_)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_695_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_695_BTF_ZERO_THEOREM_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_695_BTF_SOURCE_BOUND_ACQUISITION_LEDGER.csv",
        RESIDUALS / "P8_Y5_R10_695_BTF_FIRST_FILL_ROW.csv",
        RESIDUALS / "P8_Y5_R10_695_PRODUCT_BOUND_SMOKE.csv",
        RESIDUALS / "P8_Y5_R10_695_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_695_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_695_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_695_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_695_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V695_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V695_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V695_2_zero_audit_complete", zero_complete, f"zero_rows={len(zero_rows)}"),
        ("V695_3_zero_not_promoted", zero_not_promoted, "no B_TF theorem-zero row"),
        ("V695_4_acquisition_ledger_complete", acquisition_complete, f"acquisition_rows={len(acquisition_rows)}"),
        ("V695_5_acquisition_missing_markers_retained", acquisition_missing, "acquisition rows keep missing/product-only status"),
        ("V695_6_first_fill_row_complete", fill_complete and fill_missing, "first fill row written with missing fields retained"),
        ("V695_7_product_bound_nonclaim", product_nonclaim, "product-bound smoke is not a B_TF value"),
        ("V695_8_evaluator_blocks", evaluator_blocks, "zero/source/product evaluators remain nonclaim"),
        ("V695_9_claim_gates_block", gates_block, "claim gates block B_TF and local promotion"),
        ("V695_10_no_claim_rows_promoted", no_claim_rows, "all generated 695 rows remain valid_for_claim=false"),
        ("V695_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V695_12_generated_outputs_scoped", scoped_outputs, "all 695 outputs target post-checkpoint-work"),
        ("V695_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V695_14_status_nonclaim", "no_BTF_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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
    zero_rows: list[dict[str, str]],
    acquisition_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    product_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 695 - Y5 R10 BTF Over MH Theorem Zero Or Source Bound Acquisition

## Verdict

695 attacks the first `epsilon_TF` numerator component:

```text
B_TF_over_MH = ||B_TF_obs|| / M_H_ref
```

The theorem-zero route fails for the current corpus. The boundary no-hair route is clean but unsigned: class-only boundary action, relative boundary class, no vector/tensor/shear hair, Ward/Bianchi closure, and same-frame denominator are not jointly derived.

So 695 writes the source-bound acquisition row for `B_TF_over_MH`, but keeps it unfilled. A source-locked gamma target can only produce a product pressure such as `C_gamma_TF * B_TF_over_MH`; it is not a `B_TF` value.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## BTF Zero Theorem Audit

{markdown_table(zero_rows, ["audit_id", "zero_clause", "current_result", "blocker", "fallback_row", "valid_for_claim"])}

## BTF Source Bound Acquisition Ledger

{markdown_table(acquisition_rows, ["acquisition_id", "quantity", "current_status", "why_needed", "valid_for_claim"])}

## BTF First Fill Row

{markdown_table(fill_rows, ["fill_id", "quantity", "formula", "value_or_theorem_zero", "M_H_ref", "source_path", "valid_for_claim"])}

## Product Bound Smoke

{markdown_table(product_rows, ["smoke_id", "observable", "source_locked_target", "product_bound", "why_not_BTF_bound", "claim_status", "valid_for_claim"])}

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
    zero_rows = btf_zero_theorem_audit_rows()
    acquisition_rows = source_bound_acquisition_rows()
    fill_rows = first_fill_row()
    product_rows = product_bound_smoke_rows()
    evaluator_rows_ = evaluator_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        zero_rows,
        acquisition_rows,
        fill_rows,
        product_rows,
        evaluator_rows_,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_695_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_BTF_ZERO_THEOREM_AUDIT.csv", zero_rows, ["audit_id", "zero_clause", "mathematical_test", "current_result", "blocker", "fallback_row", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_BTF_SOURCE_BOUND_ACQUISITION_LEDGER.csv", acquisition_rows, ["acquisition_id", "quantity", "required_columns", "current_status", "why_needed", "source_strategy", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_BTF_FIRST_FILL_ROW.csv", fill_rows, ["fill_id", "target_epsilon_row", "quantity", "formula", "value_or_theorem_zero", "B_TF_obs_norm", "M_H_ref", "units", "boundary_domain", "frame_convention", "equation_ref", "source_path", "derivation_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_PRODUCT_BOUND_SMOKE.csv", product_rows, ["smoke_id", "observable", "source_locked_target", "product_bound", "why_not_BTF_bound", "claim_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_EVALUATOR.csv", evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_695_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_695_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, zero_rows, acquisition_rows, fill_rows, product_rows, evaluator_rows_, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"zero_rows={len(zero_rows)}")
    print(f"acquisition_rows={len(acquisition_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
