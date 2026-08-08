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
DOC = ROOT / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1052-R10-tau-clock-alpha-projection-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1052_TAU_CLOCK_ALPHA_PROJECTION_TEMPLATE_NONCLAIM.csv"
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
        ("SRC1052_0_1051_next", "source-intake/mts_residuals/P8_Y5_R10_1051_NEXT_TARGET.csv", "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md", "1051 handoff to tau-clock/Xhat normalization."),
        ("SRC1052_1_1051_chain", "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv", "BAP1051_2_best_current_product", "1051 b_alpha clock-product chain."),
        ("SRC1052_2_tau_clock", "source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv", "TAU647_0_time_drift", "Tau-clock map definitions."),
        ("SRC1052_3_chix_definition", "source-intake/mts_residuals/P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv", "CHX647_1_finite_alpha_pressure_coordinate", "chi_X definition/status."),
        ("SRC1052_4_chix_dynamics", "source-intake/mts_residuals/P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv", "LCD648_3_parent_vertical_norm", "Local chi_X dynamics/silence attempts."),
        ("SRC1052_5_clock_product_647", "source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv", "CPB647_1_YbE3E2", "Original clock product bound ledger."),
        ("SRC1052_6_clock_product_988", "source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv", "CLOCK988_CAS646_1_YbE3E2", "Imported clock product bound ledger."),
        ("SRC1052_7_alpha_wep_pressure", "source-intake/mts_residuals/P8_Y5_R10_767_ALPHA_WEP_PRESSURE_IMPORT.csv", "AWP767_2_MICROSCOPE_beta_target", "Alpha WEP pressure import."),
        ("SRC1052_8_wep_alpha_import", "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "WEP alpha pressure imported rows."),
        ("SRC1052_9_dd_charge", "source-intake/mts_residuals/P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv", "Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb", "Damour-Donoghue alpha/composition charge smoke estimates."),
        ("SRC1052_10_source_test_charge", "source-intake/mts_residuals/P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv", "BETA1035_0_product_law", "R10 source/test charge split/product law."),
        ("SRC1052_11_tau_R10", "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_6_verdict", "tau_R10 derivation audit."),
        ("SRC1052_12_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "Local WEP/source, clock, PPN, and Gdot anchors."),
        ("SRC1052_13_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 nonclaim review-candidate curve for smoke only."),
        ("SRC1052_14_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "Existing R10 runner and schema."),
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


def tau_clock_rows() -> list[dict[str, str]]:
    return [
        {
            "tau_id": "TCN1052_0_product_definition",
            "claim_piece": "tau_clock_time definition",
            "mathematical_form": "tau_clock_time := d chi_X / dt and d ln(alpha_EM)/dt = b_alpha * tau_clock_time",
            "derivation_status": "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED",
            "support": "TAU647_0_time_drift",
            "blocking_gap": "chi_X parent state and local time projection are not derived",
            "usable_now": "clock data bound b_alpha*tau_clock_time only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TCN1052_1_H0_diagnostic",
            "claim_piece": "H0-normalized diagnostic",
            "mathematical_form": "tau_clock_time = H0 * d chi_X/dN with nominal H0=7.16e-11 yr^-1",
            "derivation_status": "DIAGNOSTIC_ONLY",
            "support": "TAU647_1_H0_normalized_drift; AWP767_1_H0_screen",
            "blocking_gap": "no parent proof that lab clock tau equals H0 dchi_X/dN",
            "usable_now": "dimensionless diagnostic |b_alpha*dchi_X/dN| <= 2.93296e-08 for best row if H0 assumption is made",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TCN1052_2_chix_closure_coordinate",
            "claim_piece": "chi_X normalization",
            "mathematical_form": "d ln(alpha_EM)=b_alpha d chi_X",
            "derivation_status": "CLOSURE_COORDINATE_ONLY",
            "support": "CHX647_1_finite_alpha_pressure_coordinate",
            "blocking_gap": "chi_X is not identified with a parent-owned local field or normalized vertical norm",
            "usable_now": "finite-runner product-bound coordinate, not standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TCN1052_3_local_silence",
            "claim_piece": "tau_clock_time = 0 local silence branch",
            "mathematical_form": "tau_clock_time=0 if strict local coframe or closed/gapped local boundary state is parent-selected",
            "derivation_status": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "support": "LCD648_0 and LCD648_1",
            "blocking_gap": "strict-local representative and closed/gapped split remain unproved",
            "usable_now": "cannot use local silence to evade clock bounds",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_id": "TCN1052_4_verdict",
            "claim_piece": "standalone b_alpha from clocks",
            "mathematical_form": "b_alpha = (d ln R/dt)/(DeltaK_alpha*tau_clock_time)",
            "derivation_status": "FAIL_CURRENT_CLAIM_TAU_NOT_DERIVED",
            "support": "1051 clock product chain plus 647 tau map",
            "blocking_gap": "tau_clock_time, Xhat/chi_X normalization, and shared WEP/R10 projection",
            "usable_now": "retain source-backed product bound only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_clock_bound_rows() -> list[dict[str, str]]:
    products = read_csv(OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv")
    rows: list[dict[str, str]] = []
    for product in products:
        if product.get("chain_id") == "BAP1051_2_best_current_product":
            row_type = "best_current"
        else:
            row_type = "imported_clock_pair"
        rows.append(
            {
                "bound_id": f"ACB1052_{len(rows)}",
                "row_type": row_type,
                "clock_pair": product.get("clock_pair", ""),
                "delta_K_alpha": product.get("delta_K_alpha", ""),
                "product_bound_1sigma_yr_inv": product.get("product_bound_1sigma_yr_inv", ""),
                "product_bound_2sigma_yr_inv": product.get("product_bound_2sigma_yr_inv", ""),
                "H0_normalized_diagnostic": product.get("H0_normalized_diagnostic", ""),
                "interpretation": "bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived",
                "standalone_balpha_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def alpha_wep_projection_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "AWP1052_0_alpha_Coulomb",
            "arena": "MICROSCOPE_WEP",
            "channel": "alpha/Coulomb composition channel",
            "source_row": "WEP988_WAS651_0_alpha_Coulomb",
            "delta_Q_abs": "1.989808886825e-03",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "5.836031862511e-11",
            "overshoot_factor": "2.084297e+04",
            "required_abs_beta_source_max": "4.797780522732e-05",
            "missing_for_claim": "beta_source_alpha theorem/prior; tau_WEP; shared domain rule; full material model",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "AWP1052_1_surface_binding",
            "arena": "MICROSCOPE_WEP",
            "channel": "surface/binding composition channel",
            "source_row": "WEP988_WAS651_1_surface_binding",
            "delta_Q_abs": "3.306456347405e-03",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "9.697707515141e-11",
            "overshoot_factor": "3.463467e+04",
            "required_abs_beta_source_max": "2.887280314062e-05",
            "missing_for_claim": "binding coefficient theorem/prior; tau_WEP; shared domain rule; full material model",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "AWP1052_2_clock_screen_warning",
            "arena": "cross_arena_policy",
            "channel": "clock-screen-only branch",
            "source_row": "WEP988_WAS651_2_clock_screen_only; JAV988_3_cross_arena_policy",
            "delta_Q_abs": "not_applicable",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "not_applicable",
            "overshoot_factor": "not_applicable",
            "required_abs_beta_source_max": "not_applicable",
            "missing_for_claim": "same alpha domain/projection must be used in clock/WEP/R10 unless theorem-zero closes branch",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def r10_alpha_projection_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "RAP1052_0_product_law",
            "arena": "R10_short_range",
            "formula": "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)",
            "support": "BETA1035_0_product_law",
            "available_inputs": "review-candidate nonclaim R10 bound curve",
            "missing_inputs": "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; alpha composition projection; promoted bound curve",
            "unity_shortcut": "rejected",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "RAP1052_1_tau_R10",
            "arena": "R10_short_range",
            "formula": "tau_R10 := normalized test-leg/material/readout projection under selected Yukawa profile convention",
            "support": "TAUR1033_2_tau_definition; TAUR1033_6_verdict",
            "available_inputs": "definition-only tau_R10 rows",
            "missing_inputs": "material/readout trace convention; Xhat normalization; finite-source correction; profile integral",
            "unity_shortcut": "do_not_set_tau_R10_to_one",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "RAP1052_2_clock_to_R10_transfer",
            "arena": "clock_to_R10_transfer",
            "formula": "clock product bound cannot determine alpha_X(lambda) without beta_s beta_t and tau_R10",
            "support": "1051 claim gate plus 1035/1033 projection rows",
            "available_inputs": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "missing_inputs": "relation between tau_clock_time and tau_R10; source/test alpha charges; K_X/Z_X",
            "unity_shortcut": "forbidden",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def transfer_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "TG1052_0_clock_product_retained",
            "claim": "clock b_alpha product bound is usable as a nonclaim constraint row",
            "gate_status": "true_nonclaim_only",
            "reason": "source-backed product rows exist and are numerically populated",
            "promotion_blocker": "not standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TG1052_1_standalone_balpha",
            "claim": "derive standalone b_alpha from clock product",
            "gate_status": "false",
            "reason": "tau_clock_time and Xhat/chi_X normalization are not parent-derived",
            "promotion_blocker": "TCN1052_4_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TG1052_2_WEP_transfer",
            "claim": "transfer clock b_alpha product to WEP",
            "gate_status": "false",
            "reason": "requires alpha composition charges, beta_source_alpha, tau_WEP, and shared domain; stress-test rows show pressure but not pass",
            "promotion_blocker": "AWP1052 rows nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TG1052_3_R10_transfer",
            "claim": "transfer clock b_alpha product to R10 alpha(lambda)",
            "gate_status": "false",
            "reason": "requires beta_s beta_t product, tau_R10, K_X/Z_X, lambda_X, and promoted bound curve",
            "promotion_blocker": "RAP1052 rows nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "tau_clock_alpha_projection_template",
            "curve_id": "MTS_1052_TAU_CLOCK_ALPHA_PROJECTION_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_TAU_R10_BETA_SOURCE_BETA_TEST_KX_ZX_FROM_CLOCK_PRODUCT",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "clock product bound constrains b_alpha*tau_clock_time; R10 needs beta_s beta_t K_X/Z_X tau_R10 and cannot be inferred directly",
            "derivation_status": "template_invalid_tau_clock_not_derived_and_R10_projection_missing",
            "formula_reference": "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md::RAP1052",
            "source_file": "MISSING_TAU_CLOCK_ALPHA_R10_PROJECTION_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; no clock-only screening transfer",
            "valid_for_claim": "false",
            "notes": "Runner must reject until standalone projection values and promoted bound curve exist.",
        }
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1052_0_tau_clock",
            "object": "tau_clock_time and Xhat/chi_X normalization",
            "current_status": "FAIL_CURRENT_CLAIM_TAU_NOT_DERIVED",
            "refusal_status": "blocked_for_standalone_balpha",
            "failure_reasons": "chi_X closure coordinate only; tau_clock_time product map only; H0 normalization diagnostic only",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1052_1_WEP_R10_transfer",
            "object": "clock product transfer to WEP/R10",
            "current_status": "PROJECTION_INPUTS_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": "beta_source_alpha;tau_WEP;tau_R10;K_X;Z_X;source/test charges;promoted R10 curve",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1052_2_R10_runner",
            "object": "R10 tau-clock alpha projection placeholder smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={runner_status.get('valid_mts_rows')}; valid_bound_rows={runner_status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1052_0_tau_clock",
            "claim": "tau_clock_time is derived from MTS parent dynamics",
            "gate_pass": "false",
            "reason": "tau_clock_time is currently a product map dchi_X/dt, not a parent-derived local projection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1052_1_H0",
            "claim": "H0-normalized diagnostic is a theory prediction",
            "gate_pass": "false",
            "reason": "H0 normalization is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1052_2_WEP",
            "claim": "alpha WEP pressure branch passes",
            "gate_pass": "false",
            "reason": "stress-test rows require beta_source_alpha <= 4.8e-05 or theorem-zero and remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1052_3_R10",
            "claim": "clock product bound provides R10 alpha(lambda)",
            "gate_pass": "false",
            "reason": "R10 needs source/test charges, K_X, Z_X, tau_R10, lambda_X, and promoted bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1052_0_tau_result",
            "decision": "tau_clock_time remains product-defined, not parent-derived",
            "because": "647 defines the product map but 648 leaves local chi_X dynamics conditional/demoted",
            "next_action": "do not promote standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1052_1_projection_result",
            "decision": "WEP/R10 projection ledgers are now explicit",
            "because": "alpha composition stress rows and R10 product-law rows exist but missing companion factors",
            "next_action": "derive/source beta_source_alpha and tau_WEP/tau_R10 before transfer",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1052_2_best_next",
            "decision": "target beta_source_alpha or tau_R10/tau_WEP source chain",
            "because": "standalone clock b_alpha is blocked; next empirical bridge is the source/test projection",
            "next_action": "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
            "objective": "derive or source beta_source_alpha, tau_WEP, and tau_R10 so the b_alpha product branch can be tested consistently across clock, WEP, and R10 rather than as a clock-only screen",
            "include": "beta_source_alpha theorem/prior, WEP composition charge matrix, tau_WEP map, tau_R10 profile/material projection, K_X/Z_X placeholders, promotion/refusal gates",
            "exclude": "unit-rescaling cheat, cancellation, clock-only screening pass, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    clock_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    r10_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    generated_paths: list[Path],
) -> list[dict[str, str]]:
    def status(result: bool) -> str:
        return "pass" if result else "fail"

    def no_claim(rows: list[dict[str, str]]) -> bool:
        return all(not flag(row.get("valid_for_claim", "false")) for row in rows)

    source_ok = all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows)
    tau_ok = any(row["tau_id"] == "TCN1052_0_product_definition" and row["derivation_status"] == "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED" for row in tau_rows) and any(
        row["tau_id"] == "TCN1052_4_verdict" and row["derivation_status"].startswith("FAIL_CURRENT_CLAIM") for row in tau_rows
    )
    clock_ok = no_claim(clock_rows) and any(row["row_type"] == "best_current" and row["product_bound_1sigma_yr_inv"] == "2.1e-18" for row in clock_rows)
    wep_ok = no_claim(wep_rows) and any(row["projection_id"] == "AWP1052_0_alpha_Coulomb" and row["required_abs_beta_source_max"] == "4.797780522732e-05" for row in wep_rows)
    r10_ok = no_claim(r10_rows) and any(row["projection_id"] == "RAP1052_2_clock_to_R10_transfer" and row["score_ready"] == "false" for row in r10_rows)
    transfer_ok = no_claim(transfer_rows) and all(row["valid_for_claim"] == "false" for row in transfer_rows)
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1053" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1052_SUMMARY", True, "1052 tau-clock/Xhat normalization or alpha WEP/R10 projection validation summary"),
        ("V1052_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1052_2_tau_clock_blocked", tau_ok, "tau_clock_time is product-defined but not parent-derived"),
        ("V1052_3_clock_product_retained", clock_ok, "best b_alpha*tau_clock product bound remains nonclaim and numeric"),
        ("V1052_4_WEP_projection_nonclaim", wep_ok, "alpha WEP stress projection rows are staged as nonclaim"),
        ("V1052_5_R10_projection_nonclaim", r10_ok, "R10 alpha projection rows are staged as nonclaim"),
        ("V1052_6_transfer_gates_blocked", transfer_ok, "transfer gates keep standalone, WEP, and R10 claims blocked"),
        ("V1052_7_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS R10 template has runner schema and no claim-valid rows"),
        ("V1052_8_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1052 placeholder rows"),
        ("V1052_9_claim_gates_blocked", gates_ok, "all tau/H0/WEP/R10 claim gates remain blocked"),
        ("V1052_10_next_target_written", next_ok, "next target row is present"),
        ("V1052_11_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1052_12_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
    ]
    return [
        {
            "check_id": check_id,
            "result": status(result),
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, result, detail in checks
    ]


def write_doc(sections: list[tuple[str, list[dict[str, object]], list[str]]]) -> None:
    lines = [
        "# 1052 Y5 R10 tau clock Xhat normalization or alpha WEP R10 projection source",
        "",
        "**Progress:** the clock side is now pinned down. `tau_clock_time=d chi_X/dt` is a valid product-map definition, and the best clock row gives `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1`, but `tau_clock_time` and `chi_X` are not parent-derived.",
        "",
        "**Current verdict:** no standalone `b_alpha`, no H0-normalized theory claim, and no clock-to-WEP/R10 transfer. The WEP/R10 side needs source/test projection factors before the clock bound can be used outside clocks.",
        "",
        "**Fallback:** alpha WEP and R10 projection ledgers are now explicit. The alpha/Coulomb WEP stress row requires `|beta_source_alpha| <= 4.797780522732e-05` or a theorem-zero, and R10 needs `beta_s beta_t K_X/Z_X tau_R10` plus a promoted bound curve.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    tau_rows = tau_clock_rows()
    clock_rows = alpha_clock_bound_rows()
    wep_rows = alpha_wep_projection_rows()
    r10_rows = r10_alpha_projection_rows()
    transfer_rows = transfer_gate_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1052_0_R10_runner_refusal",
            "valid_mts_rows": runner_status.get("valid_mts_rows"),
            "valid_bound_rows": runner_status.get("valid_bound_rows"),
            "comparison_rows": runner_status.get("comparison_rows"),
            "R10_pass_for_claim": str(runner_status.get("R10_pass_for_claim")).lower(),
            "claim_allowed": str(runner_status.get("claim_allowed")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]
    refusal_rows = placeholder_refusal_rows(runner_status)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_map: list[tuple[Path, list[dict[str, object]]]] = [
        (OUT / "P8_Y5_R10_1052_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv", tau_rows),
        (OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", clock_rows),
        (OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", wep_rows),
        (OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", r10_rows),
        (OUT / "P8_Y5_R10_1052_TRANSFER_CLAIM_GATES.csv", transfer_rows),
        (OUT / "P8_Y5_R10_1052_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1052_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1052_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1052_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1052_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        tau_rows,
        clock_rows,
        wep_rows,
        r10_rows,
        transfer_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1052_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("Tau clock Xhat normalization audit", tau_rows, ["tau_id", "claim_piece", "mathematical_form", "derivation_status", "blocking_gap", "usable_now", "valid_for_claim"]),
            ("Alpha clock product bound ledger", clock_rows, ["bound_id", "row_type", "clock_pair", "product_bound_1sigma_yr_inv", "H0_normalized_diagnostic", "interpretation", "standalone_balpha_ready", "valid_for_claim"]),
            ("Alpha WEP projection ledger", wep_rows, ["projection_id", "arena", "channel", "delta_Q_abs", "eta_bound", "unit_source_eta_prediction", "required_abs_beta_source_max", "missing_for_claim", "valid_for_claim"]),
            ("Alpha R10 projection ledger", r10_rows, ["projection_id", "arena", "formula", "support", "available_inputs", "missing_inputs", "unity_shortcut", "score_ready", "valid_for_claim"]),
            ("Transfer claim gates", transfer_rows, ["gate_id", "claim", "gate_status", "reason", "promotion_blocker", "valid_for_claim"]),
            ("MTS R10 smoke template", mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            ("Runner smoke status", runner_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            ("Placeholder refusal runner", refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            ("Claim gates", claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            ("Decision ledger", decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            ("Validation", validation, ["check_id", "result", "detail", "generated_utc"]),
            ("Next target", next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        ]
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"1052 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
