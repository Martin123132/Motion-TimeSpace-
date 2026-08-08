from __future__ import annotations

import csv
import re
from pathlib import Path


PACK_ID = "P8_Y5_R10_1317"
TITLE = "1317-Y5-R10-RAB-P0-alpha-source-intake-template-and-priority-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_P0_SOURCE_INTAKE_TEMPLATE.csv"
THEOREM_CERT_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv"
VALIDATION_RULES_PATH = OUT_DIR / f"{PACK_ID}_INPUT_VALIDATION_RULES.csv"
PRIORITY_RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRIORITY_RUNNER_REFUSAL_TABLE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_AUDIT.csv"
PROMOTION_QUEUE_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_QUEUE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1317_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        INTAKE_TEMPLATE_PATH,
        THEOREM_CERT_TEMPLATE_PATH,
        VALIDATION_RULES_PATH,
        PRIORITY_RUNNER_PATH,
        ANTI_SHORTCUT_PATH,
        PROMOTION_QUEUE_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def field_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def requirement_ids_by_arena(requirements: list[dict[str, str]], arena: str) -> list[str]:
    return [row["requirement_id"] for row in requirements if arena in row.get("arena", "").split(";")]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1317_0_1316_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_NEXT_TARGET.csv",
            "needle": "NEXT1316_0_1317",
            "role": "handoff into fillable source-intake runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1317_1_1316_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_PRODUCT_FORMULA_REQUIREMENTS.csv",
            "needle": "FORM1316_3_r10",
            "role": "canonical product formulas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1317_2_1316_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
            "needle": "REQ1316_15_bound",
            "role": "P0 source requirement ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1317_3_1316_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_PROMOTION_GATES.csv",
            "needle": "GATE1316_4_r10",
            "role": "promotion gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1317_4_1316_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv",
            "needle": "HSC1313_1_alpha",
            "role": "counterexample locks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1317_5_1315_shortcuts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_ANTI_SHORTCUT_GATES.csv",
            "needle": "SHORT1315_0_no_unity",
            "role": "anti-shortcut policy inherited from first runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    formulas = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1316_P0_PRODUCT_FORMULA_REQUIREMENTS.csv"))
    requirements = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv"))

    validation_rules = []
    intake_template = []
    for index, row in enumerate(requirements):
        slug = field_slug(row["needed_object"])
        rule_id = f"RULE1317_{index}_{field_slug(row['requirement_id'])}"
        validation_rules.append(
            {
                "rule_id": rule_id,
                "requirement_id": row["requirement_id"],
                "needed_object": row["needed_object"],
                "accepted_evidence": "numeric_source;direct_product_source;signed_theorem_zero_certificate",
                "required_fields": "value_or_certificate;units_or_dimensionless;source_path;source_anchor;provenance_note;normalization_or_branch",
                "reject_if": "blank;MISSING_*;threshold_value;unity_default;anchor_only_bound;review_candidate;unsourced_certificate",
                "refusal_reason": row["current_status"],
                "claim_effect_if_failed": "score_ready=false;valid_for_claim=false",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        intake_template.append(
            {
                "template_id": f"TPL1317_{index}_{slug}",
                "requirement_id": row["requirement_id"],
                "needed_object": row["needed_object"],
                "arena": row["arena"],
                "minimum_usable_form": row["minimum_usable_form"],
                "value_field": f"{slug}_value_or_certificate",
                "value_placeholder": "MISSING_INPUT_REQUIRED",
                "units_field": f"{slug}_units_or_dimensionless",
                "units_placeholder": "MISSING_UNITS_OR_DIMENSIONLESS_DECLARATION",
                "normalization_field": f"{slug}_normalization_or_branch",
                "normalization_placeholder": "MISSING_NORMALIZATION_OR_BRANCH",
                "source_path_field": f"{slug}_source_path",
                "source_path_placeholder": "MISSING_SOURCE_PATH",
                "source_anchor_field": f"{slug}_source_anchor",
                "source_anchor_placeholder": "MISSING_SOURCE_ANCHOR",
                "provenance_status_field": f"{slug}_provenance_status",
                "provenance_placeholder": "MISSING_PROVENANCE",
                "validation_rule_id": rule_id,
                "refusal_if_unfilled": row["current_status"],
                "claim_allowed_if_blank": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    theorem_cert_template = [
        {
            "certificate_id": "CERT1317_0_parent_object_language",
            "route": "global parent theorem-zero",
            "would_close": "REQ1316_2_no_hidden;REQ1316_3_radiative;REQ1316_16_branch",
            "required_clauses": "parent_action_clause;typed_visible_coefficient_domain;no_hidden_argument_rule;radiative_closure;readout_closure;source_path",
            "current_certificate_status": "MISSING_SIGNED_PARENT_OBJECT_LANGUAGE",
            "certificate_placeholder": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "certificate_id": "CERT1317_1_alpha_F2_zero",
            "route": "b_alpha/c_alpha theorem-zero",
            "would_close": "REQ1316_0_balpha;REQ1316_1_norm;REQ1316_2_no_hidden;REQ1316_3_radiative",
            "required_clauses": "fixed_EM_current_normalization;no_lambda_F2;no_f_Ihid_F2;same_current_owner;radiative_readout_closure;source_path",
            "current_certificate_status": "MISSING_ALPHA_F2_ZERO_CERTIFICATE",
            "certificate_placeholder": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "certificate_id": "CERT1317_2_clock_readout",
            "route": "clock readout theorem/direct product",
            "would_close": "REQ1316_4_tau_clock;REQ1316_5_clock_model",
            "required_clauses": "clock_pair;transition_sensitivity;readout_functor;tau_clock_time_or_direct_product;units;source_path",
            "current_certificate_status": "MISSING_CLOCK_READOUT_CERTIFICATE",
            "certificate_placeholder": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "certificate_id": "CERT1317_3_source_weight_zero",
            "route": "WEP/R10 source normalization theorem",
            "would_close": "REQ1316_6_beta_source;REQ1316_7_tau_wep;REQ1316_8_material;REQ1316_9_source_profile",
            "required_clauses": "source_weight_domain;species_weight_rule;material_response;worldtube_profile;readout_kernel;source_path",
            "current_certificate_status": "MISSING_SOURCE_WEIGHT_CERTIFICATE",
            "certificate_placeholder": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "certificate_id": "CERT1317_4_r10_product_vector",
            "route": "finite R10 product vector",
            "would_close": "REQ1316_10_lambda;REQ1316_11_ZX;REQ1316_12_KX;REQ1316_13_beta_test;REQ1316_14_tail;REQ1316_15_bound",
            "required_clauses": "lambda_X;Z_X;K_X(lambda);beta_source(lambda);beta_test(lambda);tau_R10;epsilon_tail;promoted_alpha_bound_curve;source_path",
            "current_certificate_status": "MISSING_R10_VECTOR_OR_BOUND_CURVE",
            "certificate_placeholder": "MISSING_NUMERIC_VECTOR_AND_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "certificate_id": "CERT1317_5_cross_arena_functor",
            "route": "cross-arena transfer theorem",
            "would_close": "REQ1316_16_branch",
            "required_clauses": "same_parent_branch_id;readout_functor;F_clock;F_WEP;F_R10;F_local;nontransfer_exceptions;source_path",
            "current_certificate_status": "MISSING_CROSS_ARENA_FUNCTOR_CERTIFICATE",
            "certificate_placeholder": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    formula_requirements = {
        "RUN1314_0_alpha": ["REQ1316_0_balpha", "REQ1316_1_norm", "REQ1316_2_no_hidden", "REQ1316_3_radiative"],
        "RUN1314_1_clock": ["REQ1316_0_balpha", "REQ1316_3_radiative", "REQ1316_4_tau_clock", "REQ1316_5_clock_model"],
        "RUN1314_2_wep": ["REQ1316_0_balpha", "REQ1316_6_beta_source", "REQ1316_7_tau_wep", "REQ1316_8_material", "REQ1316_9_source_profile"],
        "RUN1314_3_r10": ["REQ1316_0_balpha", "REQ1316_6_beta_source", "REQ1316_9_source_profile", "REQ1316_10_lambda", "REQ1316_11_ZX", "REQ1316_12_KX", "REQ1316_13_beta_test", "REQ1316_14_tail", "REQ1316_15_bound"],
        "RUN1314_4_cross_arena": ["REQ1316_16_branch"],
    }
    template_status = {row["requirement_id"]: row["value_placeholder"] for row in intake_template}
    priority_runner = []
    for index, row in enumerate(formulas):
        runner_id = row["runner_row_id"]
        reqs = formula_requirements.get(runner_id, [])
        missing = [req_id for req_id in reqs if template_status.get(req_id, "").startswith("MISSING")]
        priority_runner.append(
            {
                "runner_id": f"RUN1317_{index}_{field_slug(runner_id)}",
                "source_runner_row_id": runner_id,
                "canonical_product": row["canonical_product"],
                "required_requirement_ids": ";".join(reqs),
                "filled_requirement_count": len(reqs) - len(missing),
                "missing_requirement_count": len(missing),
                "missing_requirement_ids": ";".join(missing),
                "predicted_abs_value": "MISSING_PREDICTED_VALUE",
                "threshold_policy": "comparison_fence_only",
                "runner_status": "REFUSED",
                "refusal_reason": "template_inputs_blank_or_missing;no_numeric_prediction;no_signed_theorem_certificate",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    anti_shortcut = [
        {
            "gate_id": "SHORT1317_0_no_unity_defaults",
            "shortcut": "fill missing beta/tau/readout/kernel factors with 1",
            "enforcement": "REFUSE_UNLESS_SOURCE_OR_THEOREM_DERIVES_UNITY",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1317_1_no_threshold_as_prediction",
            "shortcut": "use empirical threshold/bound as MTS predicted value",
            "enforcement": "threshold_policy remains comparison_fence_only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1317_2_no_blank_source_path",
            "shortcut": "accept a value without source path/anchor/provenance",
            "enforcement": "source_path and source_anchor fields are mandatory for claim promotion",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1317_3_no_partial_theorem_certificate",
            "shortcut": "treat a conditional theorem as signed parent proof",
            "enforcement": "certificate requires every listed clause and source path",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1317_4_no_anchor_curve_claim",
            "shortcut": "use anchor-only/review-candidate alpha_bound(lambda) as full R10 curve",
            "enforcement": "R10 requires promoted digitized/source-backed curve",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1317_5_no_cross_arena_transfer",
            "shortcut": "transfer clock/WEP/R10 bounds without shared parent branch functor",
            "enforcement": "cross-arena row remains separate until branch functor is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_queue = [
        {
            "queue_id": "PROMQ1317_0_parent_first",
            "target": "parent theorem-zero certificate",
            "why_first": "one signed parent primitive could close alpha F2, source weights, readout, and cross-arena transfer more cleanly than many fitted coefficients",
            "required_rows": "CERT1317_0_parent_object_language;CERT1317_1_alpha_F2_zero;CERT1317_3_source_weight_zero;CERT1317_5_cross_arena_functor",
            "current_status": "EMPTY_TEMPLATE_ONLY",
            "next_action": "attempt to fill or reject parent object-language certificate from existing corpus before numeric source hunting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "PROMQ1317_1_r10_bound",
            "target": "R10 promoted alpha_bound(lambda) curve",
            "why_first": "R10 cannot score without the empirical curve even if a numeric product is later derived",
            "required_rows": "REQ1316_15_bound;CERT1317_4_r10_product_vector",
            "current_status": "EMPTY_TEMPLATE_ONLY",
            "next_action": "acquire/digitize real curve only after preserving nonclaim status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "PROMQ1317_2_clock_direct",
            "target": "direct clock product or readout map",
            "why_first": "clock row has a sharp bound but cannot be inverted into b_alpha",
            "required_rows": "REQ1316_4_tau_clock;REQ1316_5_clock_model;CERT1317_2_clock_readout",
            "current_status": "EMPTY_TEMPLATE_ONLY",
            "next_action": "source or derive clock readout map if parent route fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1317_0_template",
            "decision": "source-intake template created",
            "because": "1316 produced exact product/source requirements but no fillable interface",
            "next_action": "use template rows for any future numeric coefficient or theorem-zero certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1317_1_runner",
            "decision": "priority runner refuses every current row",
            "because": "all template fields are intentionally blank/missing until sourced or derived",
            "next_action": "attempt parent theorem certificate first, then source hunt only for rows not closed by proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1317_2_next",
            "decision": "route to parent-certificate-first fill attempt",
            "because": "derivability is the project priority, and a signed parent primitive beats coefficient patching",
            "next_action": "1318 should try to fill the parent theorem certificate from existing corpus or explicitly reject it before numeric source hunting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1317_0_1318",
            "target_file": "1318-Y5-R10-RAB-parent-theorem-certificate-first-fill-or-reject.md",
            "target_script": "scripts/Y5_R10_RAB_parent_theorem_certificate_first_fill_or_reject.py",
            "task": "try to fill the 1317 parent theorem-zero certificate from the existing corpus; if any required clause is unsigned, reject the certificate and leave numeric source-hunt rows active",
            "success_condition": "parent object-language, alpha F2 zero, source-weight, readout, and cross-arena clauses are either source-signed with paths or explicitly refused with exact missing clauses",
            "do_not": "do not turn empty templates into claims; do not use unity or threshold defaults; do not claim R10/WEP/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1317_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    template_required_columns = {
        "requirement_id",
        "value_field",
        "value_placeholder",
        "units_field",
        "source_path_field",
        "source_anchor_field",
        "provenance_status_field",
        "validation_rule_id",
        "refusal_if_unfilled",
    }
    template_ok = len(intake_template) == len(requirements) and all(
        template_required_columns.issubset(row.keys()) and str(row["value_placeholder"]).startswith("MISSING")
        for row in intake_template
    )
    validation.append(
        validation_row(
            "VAL1317_1_template_covers_requirements",
            "every 1316 P0 requirement has a fillable template row",
            template_ok,
            f"template_rows={len(intake_template)} requirements={len(requirements)}",
        )
    )
    template_rule_ids = {row["validation_rule_id"] for row in intake_template}
    rule_ids = {row["rule_id"] for row in validation_rules}
    validation.append(
        validation_row(
            "VAL1317_2_validation_rules_cover_template",
            "every template row has a matching validation rule",
            template_rule_ids == rule_ids and len(rule_ids) == len(requirements),
            f"rules={len(rule_ids)} template_rule_ids={len(template_rule_ids)}",
        )
    )
    validation.append(
        validation_row(
            "VAL1317_3_theorem_certificates_blank",
            "theorem-zero certificate templates exist but are unsigned",
            len(theorem_cert_template) == 6
            and all(row["current_certificate_status"].startswith("MISSING") for row in theorem_cert_template),
            ";".join(row["certificate_id"] for row in theorem_cert_template),
        )
    )
    validation.append(
        validation_row(
            "VAL1317_4_runner_refuses_all",
            "priority runner refuses all current product rows",
            len(priority_runner) == len(formulas) and all(row["runner_status"] == "REFUSED" for row in priority_runner),
            ";".join(f"{row['source_runner_row_id']}:{row['missing_requirement_count']}" for row in priority_runner),
        )
    )
    validation.append(
        validation_row(
            "VAL1317_5_no_threshold_or_unity_shortcuts",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    validation.append(
        validation_row(
            "VAL1317_6_promotion_queue_nonclaim",
            "promotion queue remains source/certificate work only",
            all(row["current_status"] == "EMPTY_TEMPLATE_ONLY" for row in promotion_queue),
            ";".join(row["queue_id"] for row in promotion_queue),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("template", intake_template),
        ("certs", theorem_cert_template),
        ("rules", validation_rules),
        ("runner", priority_runner),
        ("shortcuts", anti_shortcut),
        ("queue", promotion_queue),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1317_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1317_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1317_9_next_target_1318",
            "next target routes to parent theorem certificate first fill/reject",
            next_target[0]["target_file"].startswith("1318-Y5_R10") is False
            and next_target[0]["target_file"].startswith("1318-Y5-R10-RAB-parent-theorem-certificate"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1317_10_overall",
            "overall 1317 validation",
            all(row["status"] == "PASS" for row in validation),
            "1317 creates fillable P0 source/certificate templates, a refusing priority runner, and a parent-certificate-first next target",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(INTAKE_TEMPLATE_PATH, intake_template)
    write_csv(THEOREM_CERT_TEMPLATE_PATH, theorem_cert_template)
    write_csv(VALIDATION_RULES_PATH, validation_rules)
    write_csv(PRIORITY_RUNNER_PATH, priority_runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(PROMOTION_QUEUE_PATH, promotion_queue)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1317: RAB P0 Alpha Source Intake Template And Priority Runner

**Current verdict:** 1317 does not fill the coupling. It builds the fillable intake system that future proof/source work must pass through.

**Main progress:** every P0 missing object from 1316 now has a template field, units/provenance/source fields, a validation rule, and a refusal reason. The priority runner refuses all current alpha, clock, WEP, R10, and cross-arena rows because the templates are intentionally empty.

**Decision:** attempt the parent theorem-zero certificate first. If that certificate cannot be signed from the corpus, the numeric source-hunt rows remain active without pretending they are derivations.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## P0 Source Intake Template
{markdown_table(intake_template, ["template_id", "requirement_id", "needed_object", "arena", "value_field", "value_placeholder", "units_field", "source_path_field", "source_anchor_field", "provenance_status_field", "validation_rule_id", "refusal_if_unfilled", "valid_for_claim", "claim_allowed"])}

## Theorem-Zero Certificate Template
{markdown_table(theorem_cert_template, ["certificate_id", "route", "would_close", "required_clauses", "current_certificate_status", "certificate_placeholder", "valid_for_claim", "claim_allowed"])}

## Input Validation Rules
{markdown_table(validation_rules, ["rule_id", "requirement_id", "needed_object", "accepted_evidence", "required_fields", "reject_if", "refusal_reason", "valid_for_claim", "claim_allowed"])}

## Priority Runner Refusal Table
{markdown_table(priority_runner, ["runner_id", "source_runner_row_id", "canonical_product", "required_requirement_ids", "missing_requirement_count", "missing_requirement_ids", "predicted_abs_value", "threshold_policy", "runner_status", "refusal_reason", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Audit
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Promotion Queue
{markdown_table(promotion_queue, ["queue_id", "target", "why_first", "required_rows", "current_status", "next_action", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
