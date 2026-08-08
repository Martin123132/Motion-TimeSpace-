from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1053-R10-beta-source-alpha-tau-WEP-R10-source-chain-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1053_BETA_TAU_SOURCE_CHAIN_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1053_0_1052_next", "source-intake/mts_residuals/P8_Y5_R10_1052_NEXT_TARGET.csv", "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md", "1052 handoff to beta-source/tau source chain."),
        ("SRC1053_1_1052_wep", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "1052 alpha WEP projection pressure rows."),
        ("SRC1053_2_1052_r10", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", "RAP1052_0_product_law", "1052 R10 alpha projection ledger."),
        ("SRC1053_3_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "1052 best clock product bound."),
        ("SRC1053_4_989_beta_owner", "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv", "BSO989_0_definition", "beta_source_alpha owner ledger."),
        ("SRC1053_5_1036_beta_derivation", "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv", "BETA1036_0_point_particle_source", "standard variation beta definition and product law."),
        ("SRC1053_6_1037_beta_template", "source-intake/mts_residuals/P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv", "BB1037_2_beta_source_marker", "bounded beta source/test template."),
        ("SRC1053_7_1038_beta_acquisition", "source-intake/mts_residuals/P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv", "BBA1038_1_WEP_marker_diff", "beta bound acquisition anchors."),
        ("SRC1053_8_1035_charge_split", "source-intake/mts_residuals/P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv", "BETA1035_0_product_law", "R10 source/test charge split."),
        ("SRC1053_9_1033_tau_R10", "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_6_verdict", "tau_R10 derivation audit."),
        ("SRC1053_10_1035_KX", "source-intake/mts_residuals/P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv", "KXF1035_4_total", "K_X factorization rows."),
        ("SRC1053_11_562_ZX", "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv", "PR562_4_prefactor", "Z_X/lambda/K_X conditional formula register."),
        ("SRC1053_12_651_DD_charge", "source-intake/mts_residuals/P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv", "Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb", "Damour-Donoghue WEP charge smoke matrix."),
        ("SRC1053_13_988_WEP", "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "WEP alpha pressure import."),
        ("SRC1053_14_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1053_15_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "Existing R10 runner and schema."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def beta_source_alpha_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "BSA1053_0_variational_definition",
            "object": "beta_i",
            "formula": "beta_i := partial_Xhat ln(m_i^eff)",
            "support": "BETA1036_0_point_particle_source",
            "derivation_status": "CONDITIONAL_STANDARD_VARIATION",
            "missing_for_claim": "parent-owned Xhat normalization; matter mass functional m_i^eff[Xhat]; readout convention; source path",
            "usable_now": "defines what beta would mean if the parent matter action supplies m_i^eff",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BSA1053_1_alpha_marker_source",
            "object": "beta_source_alpha",
            "formula": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP under the alpha-marker WEP convention",
            "support": "BSO989_0_definition; WEP988_WAS651_0_alpha_Coulomb",
            "derivation_status": "OWNER_NOT_DERIVED",
            "missing_for_claim": "EM-lock/no-alpha theorem or numeric source normalization; tau_WEP map; shared alpha domain",
            "usable_now": "pressure-test target only, not a standalone beta_source_alpha value",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BSA1053_2_alpha_Coulomb_bound_target",
            "object": "normalized_alpha_WEP_factor",
            "formula": "|beta_source_alpha * b_alpha * tau_WEP| <= eta_bound / unit_source_eta_prediction = 4.797780522732e-05 for the alpha/Coulomb smoke row",
            "support": "AWP1052_0_alpha_Coulomb; BSO989_1_alpha_only_target",
            "derivation_status": "NUMERIC_TARGET_ONLY_NOT_MTS_VALUE",
            "missing_for_claim": "separate beta_source_alpha, b_alpha, and tau_WEP ownership; full material model; no-cancellation rule",
            "usable_now": "hard target for the finite alpha branch if it survives",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BSA1053_3_surface_binding_target",
            "object": "robust_normalized_WEP_factor",
            "formula": "|beta_source_alpha_or_binding_factor * b_A * tau_WEP| <= 2.887280314062e-05 if surface/binding survives",
            "support": "AWP1052_1_surface_binding; BSO989_2_robust_surface_including_target",
            "derivation_status": "NUMERIC_TARGET_ONLY_NOT_MTS_VALUE",
            "missing_for_claim": "binding coefficient theorem/prior; tau_WEP; full composition matrix",
            "usable_now": "more conservative robust target if binding tails are retained",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BSA1053_4_zero_theorem_route",
            "object": "beta_source_alpha = 0",
            "formula": "beta_source_alpha vanishes if visible EM/matter/readout descends only through q and no hidden invariant may enter alpha_EM or binding coefficients",
            "support": "BETA1035_2_quotient_zero; BB1037_2_beta_source_marker",
            "derivation_status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "missing_for_claim": "parent-signed no-marker/no-alpha/no-shadow theorem and radiative closure",
            "usable_now": "best derivation route, but not a current pass",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BSA1053_5_verdict",
            "object": "beta_source_alpha source chain",
            "formula": "derive beta_source_alpha or keep alpha WEP/R10 finite branch nonclaim",
            "support": "1052 projection ledgers plus 989 owner ledger",
            "derivation_status": "SOURCE_CHAIN_BLOCKED_NO_STANDALONE_BETA",
            "missing_for_claim": "theorem-zero or source-backed numeric prior with tau_WEP/tau_R10",
            "usable_now": "write gates and refuse promotion",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def wep_composition_charge_rows() -> list[dict[str, str]]:
    charge_rows = read_csv(OUT / "P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv")
    wanted_ids = {
        "Q651_PtRh10_alpha",
        "Q651_TA6V_alpha",
        "Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb",
        "Q651_PtRh10_surface",
        "Q651_TA6V_surface",
        "Q651_delta_TA6V_minus_PtRh10_surface_binding",
    }
    out_rows: list[dict[str, str]] = []
    for charge_row in charge_rows:
        if charge_row.get("charge_row_id") not in wanted_ids:
            continue
        charge_id = charge_row.get("charge_row_id", "")
        channel = charge_row.get("charge_kind", "")
        charge_value = charge_row.get("charge_value", "")
        if "delta" in charge_id.lower():
            delta_abs = str(abs(float(charge_value)))
            role = "differential_test_pair_charge"
        else:
            delta_abs = ""
            role = "material_charge_component"
        out_rows.append(
            {
                "matrix_id": f"WCM1053_{len(out_rows)}",
                "source_row_id": charge_id,
                "test_pair": "TA6V_minus_PtRh10" if "delta" in charge_id.lower() else "MICROSCOPE_material_component",
                "material_or_pair": charge_row.get("material_id", ""),
                "channel": channel,
                "charge_value": charge_value,
                "delta_Q_abs_for_pair": delta_abs,
                "formula": charge_row.get("formula", ""),
                "role": role,
                "provenance": charge_row.get("source", ""),
                "claim_grade": charge_row.get("claim_grade", ""),
                "full_material_model": "false",
                "score_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    out_rows.append(
        {
            "matrix_id": f"WCM1053_{len(out_rows)}",
            "source_row_id": "WCM1053_required_upgrade",
            "test_pair": "TA6V_minus_PtRh10",
            "material_or_pair": "full MICROSCOPE source/test/environment stack",
            "channel": "all_alpha_mass_binding_channels",
            "charge_value": "MISSING_FULL_MATERIAL_TENSOR",
            "delta_Q_abs_for_pair": "MISSING_FULL_MATERIAL_TENSOR",
            "formula": "Q_A^full = composition, binding, EM, nuclear, source/readout, and environment sensitivities in one convention",
            "role": "promotion_requirement",
            "provenance": "stress-test smoke matrix only so far",
            "claim_grade": "upgrade_required",
            "full_material_model": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return out_rows


def tau_projection_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "tau_id": "TPR1053_0_clock_product",
            "arena": "clock",
            "definition_or_formula": "d ln(alpha_EM)/dt = b_alpha * tau_clock_time",
            "support": "ACB1052_2",
            "current_status": "PRODUCT_BOUND_ONLY",
            "missing_for_claim": "tau_clock_time parent derivation and Xhat/chi_X normalization",
            "unity_shortcut": "not_applicable",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TPR1053_1_tau_WEP_definition",
            "arena": "MICROSCOPE_WEP",
            "definition_or_formula": "tau_WEP := normalized lab/source/orbit projection converting the alpha-branch X variation into differential acceleration",
            "support": "BSO989_0_definition; AWP1052_0_alpha_Coulomb",
            "current_status": "DEFINITION_REQUIRED_NOT_FOUND",
            "missing_for_claim": "lab source worldtube; Earth/source charge normalization; spacecraft orbit/environment profile; material tensor; parent Xhat normalization",
            "unity_shortcut": "rejected",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TPR1053_2_tau_R10_definition",
            "arena": "R10_short_range",
            "definition_or_formula": "tau_R10 := normalized test-leg/material/readout projection under the selected Yukawa profile convention",
            "support": "TAUR1033_2_tau_definition; TAUR1033_6_verdict",
            "current_status": "DEFINITION_ONLY",
            "missing_for_claim": "profile integral; finite-source correction; readout trace convention; Xhat normalization; source/test beta split",
            "unity_shortcut": "do_not_set_tau_R10_to_one",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TPR1053_3_shared_normalization_contract",
            "arena": "cross_arena",
            "definition_or_formula": "the same parent Xhat/chi_X normalization must feed clock, WEP, and R10 if one alpha branch is being tested",
            "support": "RAP1052_2_clock_to_R10_transfer; AWP1052_2_clock_screen_warning",
            "current_status": "CONTRACT_WRITTEN_NOT_SATISFIED",
            "missing_for_claim": "map tau_clock_time to tau_WEP and tau_R10 or explicitly prove separate branch-zero theorems",
            "unity_shortcut": "forbidden",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TPR1053_4_verdict",
            "arena": "cross_arena",
            "definition_or_formula": "b_alpha clock product cannot be exported to WEP/R10 until tau_WEP, tau_R10, beta_source/test, and K_X/Z_X are owned",
            "support": "1052 transfer gates and 1033 tau audit",
            "current_status": "TRANSFER_BLOCKED",
            "missing_for_claim": "source chain rather than rescaling",
            "unity_shortcut": "rejected",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def kx_zx_placeholder_rows() -> list[dict[str, str]]:
    return [
        {
            "placeholder_id": "KZ1053_0_ZX",
            "object": "Z_X",
            "conditional_formula": "E_X includes 1/2 int d^3x Z_X |grad X|^2",
            "support": "PR562_0_static_quadratic_energy; PR562_1_static_operator",
            "current_status": "PARENT_INPUT_MISSING",
            "missing_for_claim": "positive kinetic normalization from parent action",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "placeholder_id": "KZ1053_1_lambda_X",
            "object": "lambda_X",
            "conditional_formula": "lambda_X = sqrt(Z_X/M_X^2) in the healthy finite-range branch",
            "support": "PR562_2_canonical_mass_and_range; KXF1035_1_range",
            "current_status": "PARENT_RANGE_RELATION_MISSING",
            "missing_for_claim": "M_X^2, Z_X, units, and healthy sign",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "placeholder_id": "KZ1053_2_KX_point",
            "object": "K_X^pt",
            "conditional_formula": "K_X^pt = s_X/(4*pi*Z_X*G_obs) if beta units do not already absorb Z_X/G_obs",
            "support": "PR562_4_prefactor; KXF1035_0_KX_point",
            "current_status": "SYMBOLIC_CONDITIONAL",
            "missing_for_claim": "charge-unit convention and sign s_X",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "placeholder_id": "KZ1053_3_KX_R10",
            "object": "K_X^R10(lambda)",
            "conditional_formula": "K_X^R10(lambda)=K_X^pt * F_ST(lambda) * Pi_R10(lambda)",
            "support": "KXF1035_4_total",
            "current_status": "NOT_NUMERIC_CURRENT_CORPUS",
            "missing_for_claim": "finite-source overlap, R10 harmonic kernel, beta convention, promoted bound curve",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def cross_arena_alpha_chain_rows() -> list[dict[str, str]]:
    return [
        {
            "chain_id": "CAC1053_0_clock",
            "arena": "clock",
            "observable_bound": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "MTS_factor_needed": "b_alpha*tau_clock_time",
            "current_numeric_input": "2.1e-18 yr^-1 product bound",
            "missing_for_claim": "tau_clock_time parent derivation for standalone b_alpha",
            "transfer_status": "usable_only_as_clock_product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "CAC1053_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "observable_bound": "eta <= 2.8e-15 with DeltaQ_alpha_abs=1.989808886825e-03",
            "MTS_factor_needed": "beta_source_alpha*b_alpha*tau_WEP in one material convention",
            "current_numeric_input": "required normalized factor <= 4.797780522732e-05 under the smoke convention",
            "missing_for_claim": "beta_source_alpha owner; tau_WEP map; full material model",
            "transfer_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "CAC1053_2_WEP_surface",
            "arena": "MICROSCOPE_WEP",
            "observable_bound": "eta <= 2.8e-15 with DeltaQ_surface_abs=3.306456347405e-03",
            "MTS_factor_needed": "binding/source coefficient times tau_WEP",
            "current_numeric_input": "required normalized factor <= 2.887280314062e-05 if surface channel survives",
            "missing_for_claim": "binding coefficient theorem/prior and same WEP tau map",
            "transfer_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "CAC1053_3_R10",
            "arena": "R10_short_range",
            "observable_bound": "alpha_X(lambda) <= alpha_bound(lambda)",
            "MTS_factor_needed": "K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "current_numeric_input": "review-candidate bound curve exists but valid_for_claim=false",
            "missing_for_claim": "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; tau_R10; promoted bound curve",
            "transfer_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def transfer_promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "TPG1053_0_clock_product",
            "claim_piece": "clock product bound retained",
            "gate_pass": "true_nonclaim_only",
            "reason": "source-backed clock rows bound only b_alpha*tau_clock_time",
            "promotion_requirement": "parent tau_clock_time if standalone b_alpha is claimed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TPG1053_1_beta_source_alpha",
            "claim_piece": "beta_source_alpha derived or numerically sourced",
            "gate_pass": "false",
            "reason": "standard beta definition exists, but parent matter/alpha functional and source normalization are missing",
            "promotion_requirement": "theorem-zero or sourced numeric prior with units and source path",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TPG1053_2_tau_WEP",
            "claim_piece": "tau_WEP map derived",
            "gate_pass": "false",
            "reason": "no arena projection from parent Xhat/chi_X into MICROSCOPE differential acceleration is available",
            "promotion_requirement": "source/test/environment projection tensor in the same convention as DeltaQ",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TPG1053_3_tau_R10",
            "claim_piece": "tau_R10 profile/material projection derived",
            "gate_pass": "false",
            "reason": "tau_R10 is definition-only and unity shortcut is explicitly rejected",
            "promotion_requirement": "finite-source R10 profile integral and readout convention",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TPG1053_4_KX_ZX_lambda",
            "claim_piece": "K_X/Z_X/lambda_X numeric branch",
            "gate_pass": "false",
            "reason": "Z_X, M_X^2, sign, charge units, and R10 harmonic projection remain placeholders",
            "promotion_requirement": "parent finite-range branch and R10 kernel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TPG1053_5_cross_arena_export",
            "claim_piece": "export clock alpha product to WEP/R10",
            "gate_pass": "false",
            "reason": "clock, WEP, and R10 use different projection factors until a shared parent map is proved",
            "promotion_requirement": "shared normalization theorem or independent theorem-zero in each arena",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "beta_tau_source_chain_template",
        "curve_id": "MTS_1053_beta_tau_source_chain_nonclaim",
        "lambda_value": "MISSING_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_BETA_SOURCE_ALPHA_TAU_R10_KX_ZX",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "alpha_X(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda); WEP needs DeltaQ*beta_source_alpha*b_alpha*tau_WEP",
        "derivation_status": "template_invalid_beta_tau_source_chain_unsigned",
        "formula_reference": "P8_Y5_R10_1053_CROSS_ARENA_ALPHA_CHAIN.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1053_CROSS_ARENA_ALPHA_CHAIN.csv",
        "assumptions": "nonclaim placeholder; no unit-rescaling; no cancellation; no tau unity shortcut",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until beta_source_alpha, tau_WEP, tau_R10, K_X/Z_X, lambda_X, and a promoted bound curve are real.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1053_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject beta/tau/KX/Z_X placeholders and review-only bound rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1053_0_beta_source_alpha",
            "object": "beta_source_alpha",
            "current_status": "OWNER_NOT_DERIVED",
            "refusal_status": "blocked",
            "failure_reasons": "parent matter/alpha functional missing; no-marker/no-alpha theorem unsigned; no numeric prior",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1053_1_tau_WEP",
            "object": "tau_WEP",
            "current_status": "DEFINITION_REQUIRED_NOT_FOUND",
            "refusal_status": "blocked",
            "failure_reasons": "WEP lab/source/orbit/material projection not derived",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1053_2_tau_R10",
            "object": "tau_R10",
            "current_status": "DEFINITION_ONLY",
            "refusal_status": "blocked",
            "failure_reasons": "profile integral, readout trace, Xhat normalization, and finite-source correction missing",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1053_3_KX_ZX_lambda",
            "object": "K_X, Z_X, lambda_X",
            "current_status": "SYMBOLIC_CONDITIONAL",
            "refusal_status": "blocked",
            "failure_reasons": "parent finite-range coefficients and R10 projection kernel missing",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1053_4_R10_runner",
            "object": "R10 beta/tau source-chain placeholder smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={status.get('valid_mts_rows')}; valid_bound_rows={status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1053_0_beta_source_alpha",
            "claim": "beta_source_alpha is derived or sourced",
            "gate_pass": "false",
            "reason": "only a conditional variational definition exists; parent alpha/matter source functional is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1053_1_WEP",
            "claim": "alpha WEP branch passes",
            "gate_pass": "false",
            "reason": "WEP gives a pressure target for a normalized product, but beta_source_alpha and tau_WEP are not owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1053_2_R10",
            "claim": "finite R10 alpha(lambda) branch passes",
            "gate_pass": "false",
            "reason": "R10 needs beta_s beta_t K_X/Z_X tau_R10 lambda_X and a promoted bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1053_3_cross_arena",
            "claim": "clock alpha product can be transferred to WEP/R10",
            "gate_pass": "false",
            "reason": "tau_clock_time, tau_WEP, and tau_R10 are not linked by a parent normalization theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1053_4_local_claims",
            "claim": "local-GR/R10/WEP/clock branch is claim-ready",
            "gate_pass": "false",
            "reason": "source chain remains blocked; this is a private checkpoint only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1053_0_derivation_attempt",
            "decision": "beta_source_alpha not derived in the current corpus",
            "because": "the standard beta definition needs a parent matter/alpha functional and source normalization, which are not signed",
            "next_action": "try theorem-zero before relying on numeric priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1053_1_empirical_pressure",
            "decision": "WEP pressure target is real but nonclaim",
            "because": "DeltaQ smoke rows and MICROSCOPE eta bound yield a hard normalized-factor target, not a theory value",
            "next_action": "source tau_WEP/material tensor if zero theorem fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1053_2_R10_status",
            "decision": "R10 remains a schema/refusal smoke branch",
            "because": "K_X/Z_X/lambda_X/tau_R10/beta_s beta_t are placeholders and the bound curve is review-candidate only",
            "next_action": "do not score R10 until all placeholders are replaced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1053_3_best_next",
            "decision": "next target is beta_source_alpha theorem-zero or first numeric prior-width",
            "because": "the coupling/source normalization is the choke point across WEP, R10, and clock transfer",
            "next_action": "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md",
            "objective": "either prove beta_source_alpha=0 from the parent quotient/product/no-marker chain, or source the first numeric beta_source_alpha/tau_WEP prior-width with units and material convention",
            "include": "no-alpha/no-marker theorem attempt, matter/readout functor ownership, WEP tau map, first numeric prior source, shared clock-WEP-R10 normalization gate",
            "exclude": "unit-rescaling cheat, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    kx_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1053_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    beta_blocked = any(row.get("audit_id") == "BSA1053_5_verdict" and row.get("derivation_status") == "SOURCE_CHAIN_BLOCKED_NO_STANDALONE_BETA" for row in beta_rows)
    beta_nonclaim = all(not flag(row.get("valid_for_claim", "")) and not flag(row.get("score_ready", "")) for row in beta_rows)
    add("V1053_2_beta_source_alpha_blocked", beta_blocked and beta_nonclaim, "beta_source_alpha remains unsigned and nonclaim")
    delta_rows = [row for row in wep_rows if row.get("role") == "differential_test_pair_charge"]
    delta_ok = len(delta_rows) >= 2 and all(float(row.get("delta_Q_abs_for_pair", "0")) > 0 for row in delta_rows)
    add("V1053_3_WEP_charge_matrix_nonclaim", delta_ok and all(not flag(row.get("valid_for_claim", "")) for row in wep_rows), "WEP composition charge smoke matrix has positive differential charges and remains nonclaim")
    tau_blocked = any(row.get("tau_id") == "TPR1053_1_tau_WEP_definition" and row.get("current_status") == "DEFINITION_REQUIRED_NOT_FOUND" for row in tau_rows)
    tau_r10_blocked = any(row.get("tau_id") == "TPR1053_2_tau_R10_definition" and row.get("unity_shortcut") == "do_not_set_tau_R10_to_one" for row in tau_rows)
    add("V1053_4_tau_WEP_R10_blocked", tau_blocked and tau_r10_blocked, "tau_WEP is missing and tau_R10 remains definition-only")
    kx_nonclaim = all(not flag(row.get("valid_for_claim", "")) and not flag(row.get("score_ready", "")) for row in kx_rows)
    add("V1053_5_KX_ZX_placeholders_nonclaim", kx_nonclaim, "K_X/Z_X/lambda_X rows remain placeholders")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(not flag(row.get("valid_for_claim", "")) for row in template_rows)
    add("V1053_6_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1053_7_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1053 placeholder rows")
    gates_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1053_8_claim_gates_blocked", gates_blocked, "all beta/WEP/R10/cross-arena claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1054-Y5-R10-beta-source-alpha-zero-theorem")
    add("V1053_9_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1053_10_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1053_11_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(
        0,
        {
            "check_id": "V1053_SUMMARY",
            "result": "pass" if summary_pass else "fail",
            "detail": "1053 beta-source-alpha and tau WEP/R10 source-chain validation summary",
            "generated_utc": stamp(),
        },
    )
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    kx_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1053 Y5 R10 beta source alpha and tau WEP R10 source chain",
            "",
            "**Progress:** the coupling choke point is now explicit. The corpus gives a clean conditional definition `beta_i := partial_Xhat ln(m_i^eff)`, but it does not yet give a parent-owned `beta_source_alpha`, `tau_WEP`, or `tau_R10`.",
            "",
            "**Current verdict:** this is not grim, but it is a hard gate. The WEP rows give a real pressure target for the normalized alpha/source product, while R10 still needs `beta_s beta_t K_X/Z_X tau_R10 lambda_X` and a promoted bound curve. No local-GR, WEP, clock, or R10 pass is claimed.",
            "",
            "**Best next move:** try the theorem-zero route first: prove that visible EM/matter/readout coefficients descend through the quotient with no hidden alpha marker. If that fails, source a numeric prior-width for `beta_source_alpha*tau_WEP` in one material convention.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Beta source alpha derivation audit",
            md_table(beta_rows, ["audit_id", "object", "derivation_status", "formula", "missing_for_claim", "usable_now", "valid_for_claim"]),
            "",
            "## WEP composition charge matrix",
            md_table(wep_rows, ["matrix_id", "source_row_id", "material_or_pair", "channel", "charge_value", "delta_Q_abs_for_pair", "claim_grade", "valid_for_claim"]),
            "",
            "## Tau WEP R10 projection audit",
            md_table(tau_rows, ["tau_id", "arena", "current_status", "definition_or_formula", "missing_for_claim", "unity_shortcut", "valid_for_claim"]),
            "",
            "## KX ZX placeholder ledger",
            md_table(kx_rows, ["placeholder_id", "object", "current_status", "conditional_formula", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Cross-arena alpha chain",
            md_table(chain_rows, ["chain_id", "arena", "observable_bound", "MTS_factor_needed", "current_numeric_input", "missing_for_claim", "transfer_status", "valid_for_claim"]),
            "",
            "## Transfer promotion gates",
            md_table(gate_rows, ["gate_id", "claim_piece", "gate_pass", "reason", "promotion_requirement", "claim_allowed", "valid_for_claim"]),
            "",
            "## MTS R10 smoke template",
            md_table(template_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            "",
            "## Runner smoke status",
            md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "",
            "## Placeholder refusal runner",
            md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "",
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    beta_rows = beta_source_alpha_audit_rows()
    wep_rows = wep_composition_charge_rows()
    tau_rows = tau_projection_audit_rows()
    kx_rows = kx_zx_placeholder_rows()
    chain_rows = cross_arena_alpha_chain_rows()
    gate_rows = transfer_promotion_gate_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1053_SOURCE_REGISTER.csv",
        "beta_audit": OUT / "P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv",
        "wep_matrix": OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
        "tau_audit": OUT / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv",
        "kx_zx": OUT / "P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv",
        "cross_arena": OUT / "P8_Y5_R10_1053_CROSS_ARENA_ALPHA_CHAIN.csv",
        "transfer_gates": OUT / "P8_Y5_R10_1053_TRANSFER_PROMOTION_GATES.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1053_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1053_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1053_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1053_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1053_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1053_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["beta_audit"], beta_rows)
    write_csv(outputs["wep_matrix"], wep_rows)
    write_csv(outputs["tau_audit"], tau_rows)
    write_csv(outputs["kx_zx"], kx_rows)
    write_csv(outputs["cross_arena"], chain_rows)
    write_csv(outputs["transfer_gates"], gate_rows)
    write_csv(outputs["mts_template"], template_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    smoke_rows = runner_smoke_rows(runner_status)
    refusal_rows = placeholder_refusal_rows(runner_status)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(outputs["runner_smoke"], smoke_rows)
    write_csv(outputs["placeholder_refusal"], refusal_rows)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        beta_rows,
        wep_rows,
        tau_rows,
        kx_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        beta_rows,
        wep_rows,
        tau_rows,
        kx_rows,
        chain_rows,
        gate_rows,
        template_rows,
        smoke_rows,
        refusal_rows,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
