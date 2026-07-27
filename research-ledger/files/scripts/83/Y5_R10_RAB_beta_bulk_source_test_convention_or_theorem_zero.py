from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1393-Y5-R10-RAB-beta-bulk-source-test-convention-or-theorem-zero.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1393_SOURCE_REGISTER.csv"
CONVENTION_PROOF_PATH = SRC_DIR / "P8_Y5_R10_1393_BETA_BULK_CONVENTION_PROOF_ATTEMPT.csv"
BETA_ROWS_PATH = SRC_DIR / "P8_Y5_R10_1393_BETA_BULK_SOURCE_TEST_COEFFICIENT_ROWS.csv"
RUNNER_INTERFACE_PATH = SRC_DIR / "P8_Y5_R10_1393_BETA_RUNNER_INTERFACE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1393_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1393_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1393_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1393_VALIDATION.csv"

STATUS = (
    "beta_bulk_source_test_convention_written_theorem_zero_unsigned_"
    "coefficient_rows_nonclaim_runner_blocked"
)
CLAIM_CEILING = (
    "beta_bulk_source_test_convention_and_nonclaim_rows_only_no_beta_zero_no_numeric_alpha_"
    "no_R10_no_WEP_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1393_0_1392_doc",
        "source_path": "1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md",
        "required_anchor": "NEXT1392_0_1393",
        "purpose": "handoff to beta_bulk source/test convention or theorem-zero",
    },
    {
        "source_id": "SRC1393_1_1392_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1392_NEXT_TARGET.csv",
        "required_anchor": "NEXT1392_0_1393",
        "purpose": "machine-readable 1393 target",
    },
    {
        "source_id": "SRC1393_2_1392_zero",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1392_BETA_KERNEL_TAIL_ZERO_ATTEMPT.csv",
        "required_anchor": "BKT1392_5_current_verdict",
        "purpose": "beta/kernel/tail zero proof remains unsigned",
    },
    {
        "source_id": "SRC1393_3_1392_template",
        "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        "required_anchor": "beta_bulk_S",
        "purpose": "runner-compatible bulk alpha template exposes beta source/test handles",
    },
    {
        "source_id": "SRC1393_4_1392_register",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1392_BULK_ALPHA_TEMPLATE_REGISTER.csv",
        "required_anchor": "ATR1392_3_runner_expectation",
        "purpose": "runner must reject symbolic beta rows",
    },
    {
        "source_id": "SRC1393_5_1392_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1392_R10_RUNNER_SMOKE_SUMMARY.csv",
        "required_anchor": "RUN1392_0_anchor_smoke",
        "purpose": "runner smoke shows no valid MTS rows",
    },
    {
        "source_id": "SRC1393_6_1391_pack",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_BULK_NEUTRAL_COEFFICIENT_SOURCE_PACK.csv",
        "required_anchor": "BCP1391_2_beta_bulk_source",
        "purpose": "bulk source beta source-pack row",
    },
    {
        "source_id": "SRC1393_7_1391_kernel",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_R10_BULK_MATERIAL_KERNEL_GATE.csv",
        "required_anchor": "R10K1391_6_verdict",
        "purpose": "R10 kernel gate remains blocked",
    },
    {
        "source_id": "SRC1393_8_1389_convention",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_COUPLING_EXPANSION_CONVENTION.csv",
        "required_anchor": "CEC1389_4_observed_mass_charge",
        "purpose": "observed charge convention from coupling expansion",
    },
    {
        "source_id": "SRC1393_9_1036_beta_product",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "source-test beta product convention split",
    },
    {
        "source_id": "SRC1393_10_1036_verdict",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_5_verdict",
        "purpose": "beta rows remain unowned",
    },
    {
        "source_id": "SRC1393_11_this_script",
        "source_path": "scripts/Y5_R10_RAB_beta_bulk_source_test_convention_or_theorem_zero.py",
        "required_anchor": "STATUS",
        "purpose": "1393 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def convention_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "BBC1393_0_canonical_field",
            "target": "one beta convention for source and test",
            "attempted_derivation": "define all bulk beta legs using the same canonical local field phi_c",
            "result": "CONVENTION_REQUIRED",
            "gap": "canonical phi_c normalization is still inherited from the unsigned mass-gap/coupling branch",
            "coefficient_consequence": "all beta rows keep convention_lock=canonical_phi_c_required",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "BBC1393_1_observed_mass_charge",
            "target": "bulk beta as observed-source log derivative",
            "attempted_derivation": "set Q_bulk^w := partial_phi_c ln M_bulk^obs and split it into common, action-weight, and binding pieces",
            "result": "FORMAL_DECOMPOSITION_READY",
            "gap": "M_bulk decomposition and inherited binding fractions are not sourced",
            "coefficient_consequence": "beta_bulk,A = beta_* + beta_w,bulk,A + beta_bind,A",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "BBC1393_2_source_test_separation",
            "target": "source and test legs are separate inputs",
            "attempted_derivation": "R10 product law uses beta_bulk,S beta_bulk,T; source/test equality may be an extra material assumption but cannot replace values",
            "result": "PRODUCT_LEGS_SEPARATED",
            "gap": "actual source/test material composition and equality certificate are missing",
            "coefficient_consequence": "create beta_bulk_S and beta_bulk_T rows separately",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "BBC1393_3_zero_route",
            "target": "beta_bulk,S=beta_bulk,T=0",
            "attempted_derivation": "if common owner, bulk action-weight zero, binding inheritance zero, and readout marker silence all hold, both beta legs vanish",
            "result": "EXACT_CONDITIONAL_BETA_ZERO",
            "gap": "common owner, binding inheritance, and readout marker silence are unsigned",
            "coefficient_consequence": "zero certificate shape exists but is not claim-ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "BBC1393_4_no_linear_shortcut",
            "target": "no linear beta or packed source-leg shortcut",
            "attempted_derivation": "R10 alpha must use beta_source*beta_test plus tail, not beta_source alone or an absorbed c_g",
            "result": "PRODUCT_GUARD_ACTIVE",
            "gap": "none for guard; numeric/product values still missing",
            "coefficient_consequence": "runner interface must block unless both beta legs are numeric/zero-certified",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "BBC1393_5_current_verdict",
            "target": "beta_bulk source/test convention claim status",
            "attempted_derivation": "compare 1392 template, 1391 pack, 1389 convention, and 1036 product law",
            "result": "CONVENTION_WRITTEN_ZERO_UNSIGNED",
            "gap": "beta source/test rows lack values, zero certificates, material composition, and canonical normalization",
            "coefficient_consequence": "write explicit nonclaim beta source/test rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def beta_coefficient_rows() -> list[dict[str, str]]:
    return [
        {
            "beta_id": "BBS1393_0_beta_star",
            "coefficient": "beta_*",
            "role": "common-factor derivative shared by source and test",
            "definition": "beta_* := partial_phi_c ln w_*",
            "units": "canonical inverse-field or locked dimensionless beta convention",
            "formula_component": "beta_bulk,A includes beta_*",
            "required_for_claim": "parent theorem beta_*=0 or sourced beta_* bound",
            "current_value": "MISSING",
            "convention_lock": "canonical_phi_c_required",
            "current_status": "MISSING_COMMON_BETA_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_1_beta_w_bulk_source",
            "coefficient": "beta_w,bulk,S",
            "role": "bulk source action-weight derivative",
            "definition": "partial_phi_c ln w_bulk,S after common calibration",
            "units": "canonical inverse-field or locked dimensionless beta convention",
            "formula_component": "beta_bulk,S = beta_* + beta_w,bulk,S + beta_bind,S",
            "required_for_claim": "source material action map or theorem beta_w,bulk,S=0",
            "current_value": "MISSING",
            "convention_lock": "canonical_phi_c_required",
            "current_status": "MISSING_SOURCE_ACTION_WEIGHT_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_2_beta_w_bulk_test",
            "coefficient": "beta_w,bulk,T",
            "role": "bulk test action-weight derivative",
            "definition": "partial_phi_c ln w_bulk,T after common calibration",
            "units": "canonical inverse-field or locked dimensionless beta convention",
            "formula_component": "beta_bulk,T = beta_* + beta_w,bulk,T + beta_bind,T",
            "required_for_claim": "test material action map or theorem beta_w,bulk,T=0",
            "current_value": "MISSING",
            "convention_lock": "canonical_phi_c_required",
            "current_status": "MISSING_TEST_ACTION_WEIGHT_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_3_beta_bind_source",
            "coefficient": "beta_bind,S",
            "role": "source inherited electronic/nuclear/EM binding charge",
            "definition": "sum_i f_i,S beta_i for source bulk composition in observed mass convention",
            "units": "same beta convention as beta_*",
            "formula_component": "adds to beta_bulk,S",
            "required_for_claim": "source composition fractions and inherited sector beta rows or theorem-zero",
            "current_value": "MISSING",
            "convention_lock": "observed_mass_decomposition_required",
            "current_status": "MISSING_SOURCE_BINDING_DECOMPOSITION",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_4_beta_bind_test",
            "coefficient": "beta_bind,T",
            "role": "test inherited electronic/nuclear/EM binding charge",
            "definition": "sum_i f_i,T beta_i for test bulk composition in observed mass convention",
            "units": "same beta convention as beta_*",
            "formula_component": "adds to beta_bulk,T",
            "required_for_claim": "test composition fractions and inherited sector beta rows or theorem-zero",
            "current_value": "MISSING",
            "convention_lock": "observed_mass_decomposition_required",
            "current_status": "MISSING_TEST_BINDING_DECOMPOSITION",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_5_beta_bulk_source",
            "coefficient": "beta_bulk,S",
            "role": "R10/PPN/orbital source leg",
            "definition": "beta_* + beta_w,bulk,S + beta_bind,S",
            "units": "same beta convention as beta_*",
            "formula_component": "alpha_bulk,ST(lambda)=K(lambda) beta_bulk,S beta_bulk,T + epsilon_tail(lambda)",
            "required_for_claim": "all source components numeric/zero-certified plus material source map",
            "current_value": "MISSING",
            "convention_lock": "canonical_phi_c_required;observed_mass_decomposition_required",
            "current_status": "MISSING_SOURCE_LEG_VALUE_OR_ZERO_CERTIFICATE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_6_beta_bulk_test",
            "coefficient": "beta_bulk,T",
            "role": "R10/WEP test leg",
            "definition": "beta_* + beta_w,bulk,T + beta_bind,T",
            "units": "same beta convention as beta_*",
            "formula_component": "alpha_bulk,ST(lambda)=K(lambda) beta_bulk,S beta_bulk,T + epsilon_tail(lambda)",
            "required_for_claim": "all test components numeric/zero-certified plus material test map",
            "current_value": "MISSING",
            "convention_lock": "canonical_phi_c_required;observed_mass_decomposition_required",
            "current_status": "MISSING_TEST_LEG_VALUE_OR_ZERO_CERTIFICATE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_7_beta_product",
            "coefficient": "beta_bulk,S*beta_bulk,T",
            "role": "R10 finite-exchange product",
            "definition": "source-test product in the same beta convention",
            "units": "dimensionless after convention-specific normalization",
            "formula_component": "K_bulk,ST(lambda) beta_bulk,S beta_bulk,T",
            "required_for_claim": "both beta legs numeric/zero-certified; no linear shortcut; no sign-cancellation credit without source",
            "current_value": "MISSING",
            "convention_lock": "product_law_required",
            "current_status": "MISSING_PRODUCT_INPUTS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "beta_id": "BBS1393_8_beta_verdict",
            "coefficient": "beta_bulk source/test coefficient pack",
            "role": "nonclaim beta convention and coefficient routing",
            "definition": "all beta rows above must be theorem-zero or source-backed before alpha scoring",
            "units": "per-row units above",
            "formula_component": "feeds 1392 bulk alpha template",
            "required_for_claim": "BBS1393_0 through BBS1393_7 complete with source paths and no MISSING markers",
            "current_value": "MISSING",
            "convention_lock": "all_locks_required",
            "current_status": "BETA_SOURCE_TEST_ROWS_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def runner_interface_rows() -> list[dict[str, str]]:
    return [
        {
            "interface_id": "BRI1393_0_template_dependency",
            "runner_input": "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
            "required_beta_condition": "replace symbolic beta_bulk_S and beta_bulk_T only after BBS1393 rows are claim-ready",
            "current_status": "BLOCKED_SYMBOLIC_BETA_HANDLES",
            "runner_effect": "valid_mts_rows remains zero",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BRI1393_1_zero_certificate",
            "runner_input": "future theorem-zero alpha row",
            "required_beta_condition": "beta_bulk,S=0 and beta_bulk,T=0 with signed source/test certificates plus epsilon_tail=0",
            "current_status": "BLOCKED_ZERO_CERTIFICATE_UNSIGNED",
            "runner_effect": "do not write alpha_predicted=0 as claim row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BRI1393_2_numeric_product",
            "runner_input": "future numeric alpha row",
            "required_beta_condition": "both beta legs numeric, same units/convention, source-backed, and paired with K(lambda) and tail",
            "current_status": "BLOCKED_NUMERIC_VALUES_MISSING",
            "runner_effect": "no numeric alpha(lambda) may be emitted",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BRI1393_3_WEP_link",
            "runner_input": "source/test beta contrast",
            "required_beta_condition": "if beta_bulk,S != beta_bulk,T or material composition differs, WEP/source-charge gate opens",
            "current_status": "BLOCKED_MATERIAL_MAP_MISSING",
            "runner_effect": "R10 score cannot be isolated from WEP/PPN gates",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BRI1393_4_verdict",
            "runner_input": "all beta-to-runner routes",
            "required_beta_condition": "beta rows complete or zero-certified before R10 runner promotion",
            "current_status": "BETA_RUNNER_INTERFACE_READY_SCORING_BLOCKED",
            "runner_effect": "runner remains a blocker until beta rows become real",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1393_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1393_1_beta_zero",
            "gate": "beta_bulk source/test legs are theorem-zero",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "zero route is exact but common owner, binding inheritance, and readout marker silence remain unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1393_2_beta_rows",
            "gate": "beta source/test coefficient rows exist",
            "status": "PASS_NONCLAIM_ROWS",
            "reason": "source/test beta decomposition and required provenance are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1393_3_runner_interface",
            "gate": "beta rows can promote the R10 alpha template",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "beta rows still contain MISSING values and no zero certificates",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1393_4_R10_score",
            "gate": "R10 score may be reported",
            "status": "BLOCKED_NO_NUMERIC_ALPHA",
            "reason": "no beta product, K(lambda), tail, or full bound curve is claim-ready",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1393_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1393 is a beta convention checkpoint, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1393_0_convention",
            "decision": "use observed-mass log derivative in one canonical field convention",
            "because": "source/test beta legs must be comparable and runner-compatible",
            "next_action": "fill canonical phi normalization or keep convention lock active",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1393_1_source_test",
            "decision": "keep source and test beta legs separate",
            "because": "R10 is a product law and WEP/material dependence can hide in leg differences",
            "next_action": "build source/test material-composition map or zero certificates",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1393_2_next",
            "decision": "go after material composition and binding inheritance next",
            "because": "beta_bulk rows are blocked mainly by beta_bind and material/source decomposition",
            "next_action": "derive/bound beta_bind,S and beta_bind,T or prove binding inherits common owner",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1393_0_1394",
            "next_doc": "1394-Y5-R10-RAB-bulk-binding-inheritance-or-material-composition-map.md",
            "next_script": "scripts/Y5_R10_RAB_bulk_binding_inheritance_or_material_composition_map.py",
            "task": "derive binding inheritance for bulk neutral matter or create nonclaim material composition rows for beta_bind,S and beta_bind,T",
            "success_condition": "binding beta terms are either theorem-zero under signed owner premises or explicit nonclaim composition rows linked to electronic, nuclear, and EM binding sectors",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    convention_written = any(
        row["proof_id"] == "BBC1393_5_current_verdict"
        and row["result"] == "CONVENTION_WRITTEN_ZERO_UNSIGNED"
        and row["claim_allowed"] == "False"
        for row in proof
    )
    zero_conditional = any(
        row["proof_id"] == "BBC1393_3_zero_route"
        and row["result"] == "EXACT_CONDITIONAL_BETA_ZERO"
        and row["valid_for_claim"] == "False"
        for row in proof
    )
    beta_verdict = any(
        row["beta_id"] == "BBS1393_8_beta_verdict"
        and row["current_status"] == "BETA_SOURCE_TEST_ROWS_READY_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in beta_rows
    )
    no_values = all(row["current_value"] == "MISSING" for row in beta_rows)
    beta_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in beta_rows)
    interface_blocked = any(
        row["interface_id"] == "BRI1393_4_verdict"
        and row["current_status"] == "BETA_RUNNER_INTERFACE_READY_SCORING_BLOCKED"
        and row["claim_allowed"] == "False"
        for row in interface
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1393_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_1392 = csv_rows(SRC_DIR / "P8_Y5_R10_1392_CLAIM_GATE.csv")
    prior_local_blocked = any(
        row["gate_id"] == "GATE1392_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1392
    )
    template_rows = csv_rows(SRC_DIR / "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv")
    template_still_nonclaim = all(row.get("valid_for_claim", "").lower() == "false" for row in template_rows)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        CONVENTION_PROOF_PATH,
        BETA_ROWS_PATH,
        RUNNER_INTERFACE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_beta_bulk_source_test_convention_or_theorem_zero.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and convention_written
        and zero_conditional
        and beta_verdict
        and no_values
        and beta_nonclaim
        and interface_blocked
        and local_claim_blocked
        and prior_local_blocked
        and template_still_nonclaim
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1393_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1393_1_convention",
            "check": "beta convention is written and zero route remains unsigned",
            "status": "PASS" if convention_written and zero_conditional else "FAIL",
            "details": "BBC1393_3 records the exact conditional beta zero route; BBC1393_5 keeps it unsigned.",
        },
        {
            "validation_id": "VAL1393_2_beta_rows",
            "check": "beta source/test coefficient rows are explicit and nonclaim",
            "status": "PASS" if beta_verdict and no_values and beta_nonclaim else "FAIL",
            "details": f"beta_rows={len(beta_rows)}; all_values_missing={no_values}; all_nonclaim={beta_nonclaim}",
        },
        {
            "validation_id": "VAL1393_3_runner_interface",
            "check": "beta rows cannot promote the R10 template yet",
            "status": "PASS" if interface_blocked and template_still_nonclaim else "FAIL",
            "details": "BRI1393_4 blocks runner promotion; 1392 alpha template remains valid_for_claim=false.",
        },
        {
            "validation_id": "VAL1393_4_claim_refusal",
            "check": "R10 and local claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1393_5 and prior GATE1392_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1393_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1393_6_overall",
            "check": "overall 1393 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1393 writes the beta_bulk source/test convention and nonclaim coefficient rows without enabling R10/local scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1393 - Y5 R10 RAB Beta Bulk Source-Test Convention Or Theorem-Zero

**Generated:** {generated}

**Current verdict:** the beta convention is now explicit: `beta_bulk,S` and `beta_bulk,T` are observed-mass log derivatives in one canonical `phi_c` convention, split into common, action-weight, and inherited binding pieces. The zero route is exact but unsigned.

**Discipline move:** keep source and test beta legs separate. R10 uses `beta_bulk,S * beta_bulk,T`; equality of material class is not a value, and no linear beta shortcut is allowed. Every beta row remains nonclaim until values or zero certificates are real.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Beta Bulk Convention Proof Attempt

{md_table(proof)}

## Beta Bulk Source/Test Coefficient Rows

{md_table(beta_rows)}

## Beta Runner Interface Gate

{md_table(interface)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    proof = convention_proof_rows()
    beta_rows = beta_coefficient_rows()
    interface = runner_interface_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, proof, beta_rows, interface, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CONVENTION_PROOF_PATH, proof)
    write_csv(BETA_ROWS_PATH, beta_rows)
    write_csv(RUNNER_INTERFACE_PATH, interface)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, proof, beta_rows, interface, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1393 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
