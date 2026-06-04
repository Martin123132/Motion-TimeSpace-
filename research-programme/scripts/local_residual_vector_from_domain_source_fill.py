from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "local_residual_vector_from_domain_source_fill_written_retained_components_explicit_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "local_residual_vector_gate_only_no_source_normalized_Newton_no_PPN_no_local_GR_pass"
NEXT_TARGET = "483-parent-action-local-zero-or-fill-decision.md"

DOC_PATH = Path("482-local-residual-vector-from-domain-source-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_SOURCE_REGISTER.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
BOUND_REGISTER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv")
PROMOTION_GATES_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_ROUTE_UPDATE.csv")

ALPHA3_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv")
DOMAIN_SIBLING_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv")
R11_FILL_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv")
QCOH_PARENT_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv")
LOCAL_TEMPLATE_PATH = Path("source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv")
MU_EXTRA_SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
CONSTANT_GM_INPUT_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "14-closure-deviation-PPN-sensitivity.md",
        "role": "internal q_R/beta/clock/matter local deviation dictionary",
    },
    {
        "source_file": "16-local-bounds-gate-runner.md",
        "role": "existing conservative local screening gates and exact Q_R=0 logic",
    },
    {
        "source_file": "469-fill-or-zero-highest-pressure-mu-extra-row.md",
        "role": "highest-pressure alpha3 boundary/domain source-normalization row",
    },
    {
        "source_file": "477-alpha3-bound-product-evaluator.md",
        "role": "strict alpha3 evaluator and no-cancellation policy",
    },
    {
        "source_file": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "R11/domain source zero rejected and fill requirements written",
    },
    {
        "source_file": "480-alpha3-numeric-product-input-template.md",
        "role": "boundary/domain alpha3 product template and domain sibling rows",
    },
    {
        "source_file": "481-Qcoh-parent-projector-algebra-or-closure.md",
        "role": "Qcoh trace projector algebra and parent-action contract",
    },
    {
        "source_file": str(ALPHA3_TEMPLATE_PATH),
        "role": "active boundary/domain/total alpha3 product rows",
    },
    {
        "source_file": str(DOMAIN_SIBLING_TEMPLATE_PATH),
        "role": "domain alpha1/alpha2/alpha3/xi/R11 sibling input rows",
    },
    {
        "source_file": str(R11_FILL_REQUIREMENTS_PATH),
        "role": "domain R11/source-normalization fill requirements",
    },
    {
        "source_file": str(QCOH_PARENT_CONTRACT_PATH),
        "role": "parent action contract rows that must pass before local GR",
    },
    {
        "source_file": str(LOCAL_TEMPLATE_PATH),
        "role": "canonical local residual row names R0-R11",
    },
    {
        "source_file": str(MU_EXTRA_SCORECARD_PATH),
        "role": "local bound scorecard with alpha1/alpha2/alpha3/xi/R11 locks",
    },
    {
        "source_file": str(CONSTANT_GM_INPUT_PATH),
        "role": "source-normalized Newton / measured-GM residual runner input",
    },
    {
        "source_file": "scripts/local_residual_vector_from_domain_source_fill.py",
        "role": "this checkpoint generator",
    },
]


LOCAL_VECTOR_COLUMNS = [
    "component_id",
    "sector",
    "source_channel",
    "target_row",
    "observable",
    "residual_symbol",
    "residual_expression",
    "predicted_value_or_certificate",
    "units",
    "bound_or_gate",
    "source_artifact",
    "theorem_zero_certificate",
    "numeric_source_file",
    "current_status",
    "passes_required_gate",
    "valid_for_local_GR_claim",
    "blocks_Newton",
    "blocks_PPN",
    "blocks_local_GR",
    "next_action",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_REGISTER:
        path = ROOT / source["source_file"]
        rows.append(
            {
                "source_file": source["source_file"],
                "exists": str(path.exists()),
                "role": source["role"],
            }
        )
    return rows


def row_by(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {key}={value}, found {len(matches)}")
    return matches[0]


def build_local_vector() -> list[dict[str, str]]:
    alpha3_products = read_csv(ALPHA3_TEMPLATE_PATH)
    siblings = read_csv(DOMAIN_SIBLING_TEMPLATE_PATH)
    qcoh_contract = read_csv(QCOH_PARENT_CONTRACT_PATH)

    boundary_alpha3 = row_by(alpha3_products, "input_id", "A3_BOUNDARY_NUMERIC_OR_ZERO")
    domain_alpha3 = row_by(alpha3_products, "input_id", "A3_DOMAIN_NUMERIC_OR_ZERO")
    total_alpha3 = row_by(alpha3_products, "input_id", "A3_TOTAL_GUARD")

    sibling_by_row = {row["target_row"]: row for row in siblings}
    contract_by_id = {row["contract_id"]: row for row in qcoh_contract}

    rows: list[dict[str, str]] = [
        {
            "component_id": "LRV_BOUNDARY_R7_ALPHA3",
            "sector": "boundary_source_normalization",
            "source_channel": boundary_alpha3["channel"],
            "target_row": boundary_alpha3["target_row"],
            "observable": boundary_alpha3["observable"],
            "residual_symbol": "alpha3_boundary",
            "residual_expression": boundary_alpha3["product_symbol"],
            "predicted_value_or_certificate": boundary_alpha3["explicit_product_value"],
            "units": boundary_alpha3["product_units"],
            "bound_or_gate": f"abs(alpha3_boundary) <= {boundary_alpha3['target_bound']} {boundary_alpha3['bound_units']}",
            "source_artifact": str(ALPHA3_TEMPLATE_PATH),
            "theorem_zero_certificate": boundary_alpha3["theorem_zero_certificate"],
            "numeric_source_file": boundary_alpha3["numeric_source_file"],
            "current_status": boundary_alpha3["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "indirect_source_normalization",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": boundary_alpha3["next_action"],
        },
        {
            "component_id": "LRV_DOMAIN_R5_ALPHA1",
            "sector": "domain_projector_source",
            "source_channel": sibling_by_row["R5_alpha1"]["channel"],
            "target_row": "R5_alpha1",
            "observable": "alpha1",
            "residual_symbol": "alpha1_domain",
            "residual_expression": sibling_by_row["R5_alpha1"]["coefficient_or_product"],
            "predicted_value_or_certificate": sibling_by_row["R5_alpha1"]["candidate_value"],
            "units": sibling_by_row["R5_alpha1"]["candidate_units"],
            "bound_or_gate": f"abs(alpha1_domain) <= {sibling_by_row['R5_alpha1']['target_bound']}",
            "source_artifact": str(DOMAIN_SIBLING_TEMPLATE_PATH),
            "theorem_zero_certificate": sibling_by_row["R5_alpha1"]["theorem_zero_certificate"],
            "numeric_source_file": sibling_by_row["R5_alpha1"]["numeric_source_file"],
            "current_status": sibling_by_row["R5_alpha1"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "false",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": sibling_by_row["R5_alpha1"]["next_action"],
        },
        {
            "component_id": "LRV_DOMAIN_R6_ALPHA2",
            "sector": "domain_projector_source",
            "source_channel": sibling_by_row["R6_alpha2"]["channel"],
            "target_row": "R6_alpha2",
            "observable": "alpha2",
            "residual_symbol": "alpha2_domain",
            "residual_expression": sibling_by_row["R6_alpha2"]["coefficient_or_product"],
            "predicted_value_or_certificate": sibling_by_row["R6_alpha2"]["candidate_value"],
            "units": sibling_by_row["R6_alpha2"]["candidate_units"],
            "bound_or_gate": f"abs(alpha2_domain) <= {sibling_by_row['R6_alpha2']['target_bound']}",
            "source_artifact": str(DOMAIN_SIBLING_TEMPLATE_PATH),
            "theorem_zero_certificate": sibling_by_row["R6_alpha2"]["theorem_zero_certificate"],
            "numeric_source_file": sibling_by_row["R6_alpha2"]["numeric_source_file"],
            "current_status": sibling_by_row["R6_alpha2"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "false",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": sibling_by_row["R6_alpha2"]["next_action"],
        },
        {
            "component_id": "LRV_DOMAIN_R7_ALPHA3",
            "sector": "domain_projector_source",
            "source_channel": domain_alpha3["channel"],
            "target_row": domain_alpha3["target_row"],
            "observable": domain_alpha3["observable"],
            "residual_symbol": "alpha3_domain",
            "residual_expression": domain_alpha3["product_symbol"],
            "predicted_value_or_certificate": domain_alpha3["explicit_product_value"],
            "units": domain_alpha3["product_units"],
            "bound_or_gate": f"abs(alpha3_domain) <= {domain_alpha3['target_bound']} {domain_alpha3['bound_units']}",
            "source_artifact": str(ALPHA3_TEMPLATE_PATH),
            "theorem_zero_certificate": domain_alpha3["theorem_zero_certificate"],
            "numeric_source_file": domain_alpha3["numeric_source_file"],
            "current_status": domain_alpha3["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "indirect_source_normalization",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": domain_alpha3["next_action"],
        },
        {
            "component_id": "LRV_DOMAIN_R8_XI",
            "sector": "domain_projector_source",
            "source_channel": sibling_by_row["R8_xi"]["channel"],
            "target_row": "R8_xi",
            "observable": "xi",
            "residual_symbol": "xi_domain",
            "residual_expression": sibling_by_row["R8_xi"]["coefficient_or_product"],
            "predicted_value_or_certificate": sibling_by_row["R8_xi"]["candidate_value"],
            "units": sibling_by_row["R8_xi"]["candidate_units"],
            "bound_or_gate": f"abs(xi_domain) <= {sibling_by_row['R8_xi']['target_bound']}",
            "source_artifact": str(DOMAIN_SIBLING_TEMPLATE_PATH),
            "theorem_zero_certificate": sibling_by_row["R8_xi"]["theorem_zero_certificate"],
            "numeric_source_file": sibling_by_row["R8_xi"]["numeric_source_file"],
            "current_status": sibling_by_row["R8_xi"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "false",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": sibling_by_row["R8_xi"]["next_action"],
        },
        {
            "component_id": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
            "sector": "domain_projector_source",
            "source_channel": sibling_by_row["R11_EH_operator_ledger"]["channel"],
            "target_row": "R11_EH_operator_ledger",
            "observable": "non_EH_operator_coefficients",
            "residual_symbol": "c_domain_source_normalization_operator",
            "residual_expression": sibling_by_row["R11_EH_operator_ledger"]["coefficient_or_product"],
            "predicted_value_or_certificate": sibling_by_row["R11_EH_operator_ledger"]["candidate_value"],
            "units": sibling_by_row["R11_EH_operator_ledger"]["candidate_units"],
            "bound_or_gate": sibling_by_row["R11_EH_operator_ledger"]["target_bound"],
            "source_artifact": str(DOMAIN_SIBLING_TEMPLATE_PATH),
            "theorem_zero_certificate": sibling_by_row["R11_EH_operator_ledger"]["theorem_zero_certificate"],
            "numeric_source_file": sibling_by_row["R11_EH_operator_ledger"]["numeric_source_file"],
            "current_status": sibling_by_row["R11_EH_operator_ledger"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "true",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": sibling_by_row["R11_EH_operator_ledger"]["next_action"],
        },
        {
            "component_id": "LRV_QCOH_PARENT_VARIABLE",
            "sector": "parent_projector_contract",
            "source_channel": "Qcoh_parent",
            "target_row": "parent_action_Q",
            "observable": "Q_mu_nu_owner",
            "residual_symbol": "delta_Q_parent",
            "residual_expression": contract_by_id["C0_parent_variable"]["acceptance_test"],
            "predicted_value_or_certificate": contract_by_id["C0_parent_variable"]["current_status"],
            "units": "theorem_gate",
            "bound_or_gate": "Q_mu_nu must be variational/Noether-owned before local residuals can pass as derivation",
            "source_artifact": str(QCOH_PARENT_CONTRACT_PATH),
            "theorem_zero_certificate": "MISSING_PARENT_Q_OWNER",
            "numeric_source_file": "not_numeric",
            "current_status": contract_by_id["C0_parent_variable"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": contract_by_id["C0_parent_variable"]["valid_for_local_GR_claim"],
            "blocks_Newton": "true",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": contract_by_id["C0_parent_variable"]["next_action"],
        },
        {
            "component_id": "LRV_QCOH_PROJECTOR_OWNERSHIP",
            "sector": "parent_projector_contract",
            "source_channel": "Qcoh_parent",
            "target_row": "P_coh_owner",
            "observable": "projector_ownership",
            "residual_symbol": "delta_Pcoh_parent",
            "residual_expression": contract_by_id["C1_projector_ownership"]["acceptance_test"],
            "predicted_value_or_certificate": contract_by_id["C1_projector_ownership"]["current_status"],
            "units": "theorem_gate",
            "bound_or_gate": "trace projector must be forced by parent local symmetry/Ward/Euler equation",
            "source_artifact": str(QCOH_PARENT_CONTRACT_PATH),
            "theorem_zero_certificate": "MISSING_PARENT_PROJECTOR_OWNER",
            "numeric_source_file": "not_numeric",
            "current_status": contract_by_id["C1_projector_ownership"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": contract_by_id["C1_projector_ownership"]["valid_for_local_GR_claim"],
            "blocks_Newton": "true",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": contract_by_id["C1_projector_ownership"]["next_action"],
        },
        {
            "component_id": "LRV_QCOH_DOMAIN_SELECTOR",
            "sector": "parent_projector_contract",
            "source_channel": "Qcoh_parent",
            "target_row": "chi_D_owner",
            "observable": "local_zero_class",
            "residual_symbol": "X_D",
            "residual_expression": contract_by_id["C2_domain_selector"]["acceptance_test"],
            "predicted_value_or_certificate": contract_by_id["C2_domain_selector"]["current_status"],
            "units": "theorem_gate",
            "bound_or_gate": "compact local vacuum must force X_D=Tr_h Q_D=0 through PPN order",
            "source_artifact": str(QCOH_PARENT_CONTRACT_PATH),
            "theorem_zero_certificate": "MISSING_LOCAL_ZERO_CLASS_CERTIFICATE",
            "numeric_source_file": "not_numeric",
            "current_status": contract_by_id["C2_domain_selector"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": contract_by_id["C2_domain_selector"]["valid_for_local_GR_claim"],
            "blocks_Newton": "true",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": contract_by_id["C2_domain_selector"]["next_action"],
        },
        {
            "component_id": "LRV_PROJECTOR_STRESS_ACCOUNTING",
            "sector": "parent_projector_contract",
            "source_channel": "Qcoh_parent",
            "target_row": "projector_domain_stress",
            "observable": "Bianchi_PPN_stress",
            "residual_symbol": "delta_g_Pcoh_chiD",
            "residual_expression": contract_by_id["C3_stress_accounting"]["acceptance_test"],
            "predicted_value_or_certificate": contract_by_id["C3_stress_accounting"]["current_status"],
            "units": "theorem_or_retained_stress",
            "bound_or_gate": "projector/domain metric stress must vanish/topologically cancel or be retained in residual vector",
            "source_artifact": str(QCOH_PARENT_CONTRACT_PATH),
            "theorem_zero_certificate": "MISSING_PROJECTOR_STRESS_LEDGER",
            "numeric_source_file": "not_numeric",
            "current_status": contract_by_id["C3_stress_accounting"]["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": contract_by_id["C3_stress_accounting"]["valid_for_local_GR_claim"],
            "blocks_Newton": "true",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": contract_by_id["C3_stress_accounting"]["next_action"],
        },
        {
            "component_id": "LRV_TOTAL_ALPHA3_GUARD",
            "sector": "no_cancellation_guard",
            "source_channel": total_alpha3["channel"],
            "target_row": total_alpha3["target_row"],
            "observable": total_alpha3["observable"],
            "residual_symbol": "alpha3_total_guard",
            "residual_expression": total_alpha3["product_symbol"],
            "predicted_value_or_certificate": total_alpha3["explicit_product_value"],
            "units": total_alpha3["product_units"],
            "bound_or_gate": total_alpha3["acceptance_gate"],
            "source_artifact": str(ALPHA3_TEMPLATE_PATH),
            "theorem_zero_certificate": total_alpha3["theorem_zero_certificate"],
            "numeric_source_file": total_alpha3["numeric_source_file"],
            "current_status": total_alpha3["current_status"],
            "passes_required_gate": "false",
            "valid_for_local_GR_claim": "false",
            "blocks_Newton": "indirect_source_normalization",
            "blocks_PPN": "true",
            "blocks_local_GR": "true",
            "next_action": total_alpha3["next_action"],
        },
    ]
    return rows


def build_bound_register(local_vector: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "component_id": row["component_id"],
            "target_row": row["target_row"],
            "observable": row["observable"],
            "bound_or_gate": row["bound_or_gate"],
            "current_status": row["current_status"],
            "passes_required_gate": row["passes_required_gate"],
            "valid_for_local_GR_claim": row["valid_for_local_GR_claim"],
            "source_artifact": row["source_artifact"],
        }
        for row in local_vector
    ]


def build_promotion_gates(local_vector: list[dict[str, str]]) -> list[dict[str, str]]:
    failed_components = [row["component_id"] for row in local_vector if row["passes_required_gate"] != "true"]
    return [
        {
            "gate_id": "G482_boundary_alpha3",
            "requirement": "boundary alpha3 product is theorem-zero or numerically below 4e-20",
            "current_result": "fail_for_claim",
            "evidence": "LRV_BOUNDARY_R7_ALPHA3 template_unfilled",
            "claim_effect": "no total alpha3 or local-GR pass",
        },
        {
            "gate_id": "G482_domain_siblings",
            "requirement": "domain alpha1/alpha2/alpha3/xi/R11 rows are theorem-zero or numerically scored",
            "current_result": "fail_for_claim",
            "evidence": "R5/R6/R7/R8/R11 domain sibling rows are template_unfilled",
            "claim_effect": "domain channel blocks PPN/local-GR",
        },
        {
            "gate_id": "G482_Qcoh_parent",
            "requirement": "Qcoh/Pcoh/chi_D are parent-owned and local X_D=0 is derived",
            "current_result": "fail_for_claim",
            "evidence": "481 passes trace-projector algebra but fails parent ownership",
            "claim_effect": "Qcoh remains theorem target/closure",
        },
        {
            "gate_id": "G482_no_cancellation",
            "requirement": "alpha3 total cannot pass by post-fit cancellation",
            "current_result": "pass_guard_active",
            "evidence": "LRV_TOTAL_ALPHA3_GUARD retained",
            "claim_effect": "individual rows must pass first",
        },
        {
            "gate_id": "G482_source_normalized_Newton",
            "requirement": "source-normalization/R11 rows are zero or scored before Newtonian reduction is claimed",
            "current_result": "fail_for_claim",
            "evidence": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION not scoreable",
            "claim_effect": "no source-normalized Newton promotion",
        },
        {
            "gate_id": "G482_local_GR_vector",
            "requirement": "every component in the local residual vector passes",
            "current_result": "fail_for_claim",
            "evidence": f"failed_components={len(failed_components)}",
            "claim_effect": "no PPN/local-GR promotion",
        },
    ]


def build_validation_rows(
    source_register: list[dict[str, str]],
    local_vector: list[dict[str, str]],
    promotion_gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_register if row["exists"] != "True"]
    required_components = {
        "LRV_BOUNDARY_R7_ALPHA3",
        "LRV_DOMAIN_R5_ALPHA1",
        "LRV_DOMAIN_R6_ALPHA2",
        "LRV_DOMAIN_R7_ALPHA3",
        "LRV_DOMAIN_R8_XI",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "LRV_QCOH_PARENT_VARIABLE",
        "LRV_QCOH_PROJECTOR_OWNERSHIP",
        "LRV_QCOH_DOMAIN_SELECTOR",
        "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "LRV_TOTAL_ALPHA3_GUARD",
    }
    present_components = {row["component_id"] for row in local_vector}
    claim_valid_rows = [row for row in local_vector if row["valid_for_local_GR_claim"] == "true"]
    failed_gates = [row for row in promotion_gates if row["current_result"] == "fail_for_claim"]
    return [
        {
            "rule_id": "V482_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V482_1_components",
            "rule": "local residual vector includes boundary alpha3, domain siblings, Qcoh parent gates, stress, and total guard",
            "result": "pass" if required_components <= present_components else "fail",
            "evidence": f"components={len(local_vector)}",
            "claim_effect": "residual vector is explicit",
        },
        {
            "rule_id": "V482_2_no_hidden_claim_rows",
            "rule": "no local residual vector row is valid for local-GR claim while unfilled",
            "result": "pass" if not claim_valid_rows else "fail",
            "evidence": f"valid_for_local_GR_claim_rows={len(claim_valid_rows)}",
            "claim_effect": "no hidden PPN/local-GR promotion",
        },
        {
            "rule_id": "V482_3_promotion_gates",
            "rule": "promotion gates fail where source-normalized Newton/PPN/local-GR evidence is missing",
            "result": "pass",
            "evidence": f"fail_for_claim_gates={len(failed_gates)}",
            "claim_effect": "failure is recorded rather than smuggled",
        },
        {
            "rule_id": "V482_4_no_cancellation_guard",
            "rule": "total alpha3 remains guard-only until individual rows pass or parent identity exists",
            "result": "pass",
            "evidence": "LRV_TOTAL_ALPHA3_GUARD passes_required_gate=false",
            "claim_effect": "no tuned cancellation",
        },
        {
            "rule_id": "V482_5_next_route",
            "rule": "next step chooses derive/fill decision rather than rerunning evaluator with missing inputs",
            "result": "pass",
            "evidence": NEXT_TARGET,
            "claim_effect": "alpha3 evaluator refresh deferred until inputs exist",
        },
    ]


DECISION_ROWS = [
    {
        "decision_id": "D0_vector_written",
        "status": "written",
        "meaning": "boundary alpha3, domain alpha1/alpha2/alpha3/xi/R11, Qcoh parent gates, projector stress, and total guard are now one local residual vector",
        "next_action": "use P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv as the local-GR fail/pass checklist",
    },
    {
        "decision_id": "D1_Newton",
        "status": "not_promoted",
        "meaning": "source-normalized Newtonian reduction remains blocked by R11/source-normalization and measured-GM residual debt",
        "next_action": "derive R11 silence or fill the source-normalization operator vector",
    },
    {
        "decision_id": "D2_PPN",
        "status": "not_promoted",
        "meaning": "preferred-frame/location alpha1/alpha2/alpha3/xi rows are unfilled or parent-unowned",
        "next_action": "derive theorem-zero certificates or fill numeric products under row locks",
    },
    {
        "decision_id": "D3_Qcoh",
        "status": "closure_retained",
        "meaning": "trace projector algebra is useful, but parent ownership/local X_D=0 is still not derived",
        "next_action": "attempt parent-action local-zero clause before closure fill if pursuing derivation first",
    },
    {
        "decision_id": "D4_local_GR",
        "status": "forbidden",
        "meaning": "no local-GR claim is allowed until every residual vector component is theorem-zero or scored",
        "next_action": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "LOCAL_VECTOR",
        "target": "derived local GR/Newton branch",
        "current_status": "explicit_residual_vector_written",
        "accepted_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
    {
        "route_id": "ALPHA3_REFRESH",
        "target": "483-alpha3-product-evaluator-refresh.md",
        "current_status": "deferred_inputs_missing",
        "accepted_for_claim": "false",
        "next_action": "run only after theorem-zero certificates or numeric products exist",
    },
    {
        "route_id": "PARENT_DERIVATION",
        "target": "Qcoh/Pcoh/chi_D/R11 local-zero clause",
        "current_status": "best_derivation_route",
        "accepted_for_claim": "false",
        "next_action": NEXT_TARGET,
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    source_register: list[dict[str, str]],
    local_vector: list[dict[str, str]],
    bound_register: list[dict[str, str]],
    promotion_gates: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> str:
    return f"""# 482 - Local Residual Vector From Domain Source Fill

Private local-GR/Newton residual-vector checkpoint. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `481` gave a useful algebra result:

```text
P_coh must be the trace projector if the Qcoh route is used.
```

But it did not parent-own `Q_coh`, `P_coh`, `chi_D`, local `X_D=0`, or R11 silence.

This checkpoint converts that into a single local residual vector. The point is simple:

```text
local GR is not allowed to pass unless every retained source/projector component is zero by theorem or scored below its bound.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_residual_vector_from_domain_source_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Local Residual Vector

{markdown_table(local_vector, LOCAL_VECTOR_COLUMNS)}

The compact rule is:

```text
V_local = 0
```

only if each component above is either:

```text
derived theorem-zero from the parent action
```

or:

```text
numerically scored below its source-locked bound with source path, units, assumptions, and no tuned cancellation.
```

## 5. Bound Register

{markdown_table(bound_register)}

## 6. Promotion Gates

{markdown_table(promotion_gates)}

## 7. Validation

{markdown_table(validation_rows)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The local-GR/Newton failure mode is now explicit as a residual vector.
The trace-projector route has a precise parent-action contract.
The alpha3/domain/R11 fill rows are machine-readable.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived the Newtonian limit.
MTS passes PPN.
MTS has alpha3=0 or mu_extra=0.
MTS can use total alpha3 cancellation to pass.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | decide whether to attempt a parent local-zero clause or begin explicit numeric closure fills |
| 2 | `483-alpha3-product-evaluator-refresh.md` | rerun only after at least one product/theorem-zero row is actually filled |
| 3 | long-run local-data runner | only after the residual vector has numeric candidate values |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-local-residual-vector-from-domain-source-fill"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    local_vector = build_local_vector()
    bound_register = build_bound_register(local_vector)
    promotion_gates = build_promotion_gates(local_vector)
    validations = build_validation_rows(sources, local_vector, promotion_gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LOCAL_VECTOR_PATH, local_vector, LOCAL_VECTOR_COLUMNS)
    write_csv(BOUND_REGISTER_PATH, bound_register)
    write_csv(PROMOTION_GATES_PATH, promotion_gates)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, local_vector, bound_register, promotion_gates, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_components = [row["component_id"] for row in local_vector if row["passes_required_gate"] != "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "local_vector": str(ROOT / LOCAL_VECTOR_PATH),
        "bound_register": str(ROOT / BOUND_REGISTER_PATH),
        "promotion_gates": str(ROOT / PROMOTION_GATES_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "local_vector_rows": len(local_vector),
        "bound_register_rows": len(bound_register),
        "promotion_gate_rows": len(promotion_gates),
        "validation_rows": len(validations),
        "decision_rows": len(DECISION_ROWS),
        "route_update_rows": len(ROUTE_UPDATE_ROWS),
        "failed_component_count": len(failed_components),
        "failed_components": failed_components,
        "claim_valid_component_count": sum(1 for row in local_vector if row["valid_for_local_GR_claim"] == "true"),
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "alpha3_passed": False,
        "mu_extra_zero_promoted": False,
        "local_GR_claim_allowed": False,
        "alpha3_evaluator_refresh_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
