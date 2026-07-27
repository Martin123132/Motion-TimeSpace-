from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1097-constant-sector-universality" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1097_CONSTANT_COEFFICIENT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1097_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv"
DD_ALPHA_COEFF_MAX = 8.320244933243533e-10
DD_SURFACE_COEFF_MAX = 6.987501646143863e-11
DD_COMMON_COEFF_MAX = 6.446142229433907e-11


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


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


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1097_0_1096_next", "source-intake/mts_residuals/P8_Y5_R10_1096_NEXT_TARGET.csv", "NEXT1096_0_1097", "1096 handoff."),
        ("SRC1097_1_1096_zero", "source-intake/mts_residuals/P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv", "CZ1096_4_verdict", "coefficient zero failure."),
        ("SRC1097_2_1096_policy", "source-intake/mts_residuals/P8_Y5_R10_1096_COEFFICIENT_PRIOR_POLICY.csv", "POL1096_0_no_unsourced_priors", "coefficient prior policy."),
        ("SRC1097_3_1096_prior", "source-intake/mts_residuals/P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv", "PRI1096_0_alpha", "DD threshold-bounded prior template."),
        ("SRC1097_4_1047_constant", "source-intake/mts_residuals/P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv", "CST1047_5_verdict", "constant superselection theorem attempt."),
        ("SRC1097_5_764_constant", "source-intake/mts_residuals/P8_Y5_R10_764_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv", "CST764_4_verdict", "constant superselection reattempt."),
        ("SRC1097_6_948_constant", "source-intake/mts_residuals/P8_Y5_R10_948_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv", "CST948_5_total_verdict", "constant/source no-marker theorem."),
        ("SRC1097_7_576_universality", "source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv", "P576_3_constant_trivial_action", "universality premise ledger."),
        ("SRC1097_8_constant_contract", "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv", "C1_superselection_independence", "constant-sector universality contract."),
        ("SRC1097_9_1091_operator", "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODH1091_2_scalar_obstruction", "hidden-visible coefficient obstruction."),
        ("SRC1097_10_1092_generators", "source-intake/mts_residuals/P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv", "GEN1092_5_species_constants", "species constants generator debt."),
        ("SRC1097_11_1047_alpha", "source-intake/mts_residuals/P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_4_verdict", "alpha owner audit."),
        ("SRC1097_12_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha radiative/readout closure audit."),
        ("SRC1097_13_1058_alpha", "source-intake/mts_residuals/P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv", "ACP1058_4_counterterm_policy", "alpha counterterm finite branch."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def universality_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "CSU1097_0_target",
            "claim_piece": "ordinary constant-sector universality",
            "mathematical_statement": "for every local vertical v in ker(Dq), Lie_v theta_A = 0 for alpha, mass ratios, binding fractions, clock standards, and source weights",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "would make WEP/clock/R10 constant coefficients theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CSU1097_1_descent_superselection",
            "claim_piece": "exact sufficient criterion",
            "mathematical_statement": "theta_A(Phi)=theta_bar_A(q(Phi)) or theta_A is discrete/topological representation data with trivial smooth vertical action",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "chain rule/locality gives Lie_v theta_A=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CSU1097_2_dimensionless_guard",
            "claim_piece": "unit rescaling cannot hide constant drift",
            "mathematical_statement": "Lie_v ln alpha_EM, Lie_v ln(m_A/m_B), Lie_v binding fractions, and Lie_v ln(nu_i/nu_j) are dimensionless observables",
            "status": "PHYSICS_GUARD_PROVED",
            "proof_or_obstruction": "one unit convention cannot remove all observable dimensionless ratios",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CSU1097_3_counterexample",
            "claim_piece": "metric descent does not force constant universality",
            "mathematical_statement": "q(Phi) fixed but theta_A=theta_0 exp(epsilon I_hid) gives Lie_v theta_A != 0 when I_hid survives",
            "status": "COUNTEREXAMPLE_RETAINED",
            "proof_or_obstruction": "hidden scalar and species-constant generator debts survive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CSU1097_4_readout_radiative",
            "claim_piece": "bare constants must survive effective/readout reduction",
            "mathematical_statement": "S_bare constant-sector silence does not imply S_eff/readout silence without radiative and readout closure",
            "status": "CLOSURE_UNSIGNED",
            "proof_or_obstruction": "alpha counterterm and readout branches remain retained nonclaim branches",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CSU1097_5_verdict",
            "claim_piece": "promote constant-sector universality for current MTS",
            "mathematical_statement": "ordinary constants/response coefficients are parent superselection data independent of hidden invariants",
            "status": "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
            "proof_or_obstruction": "alpha owner, mass spectrum, species constants, hidden scalar, and radiative/readout closure are unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def channel_audit_rows() -> list[dict[str, str]]:
    specs = [
        ("CHA1097_0_alpha", "alpha_EM/gauge kinetic normalization", "b_alpha = Lie_v ln alpha_EM", "RETAIN_FINITE_BRANCH", "unique F_Q^2/g_EM owner and no independent f_X F^2 are unsigned", "clock;WEP;R10;EM spectra"),
        ("CHA1097_1_mass_ratios", "mass ratios/Yukawa/Higgs sector", "b_mu,b_mA = Lie_v ln(m_A/m_ref) plus binding response", "RETAIN_FINITE_BRANCH", "parent matter spectrum and material sensitivity theorem are missing", "WEP;clock;R10;composition"),
        ("CHA1097_2_QCD_binding", "QCD/nuclear/binding fractions", "b_nuc,b_surface,b_binding", "RETAIN_FINITE_BRANCH", "binding fractions are dimensionless and not unit-removable", "WEP;clock;nuclear spectra"),
        ("CHA1097_3_clock", "clock transition ratios", "b_clock_i = K_alpha b_alpha + K_mu b_mu + K_nuc b_nuc + ...", "INHERITS_UPSTREAM_DEBT", "clock rows inherit alpha/mass/nuclear debts and tau_clock projection", "clock comparisons;redshift/LPI"),
        ("CHA1097_4_source_weights", "source normalization/species weights", "kappa_A(Xhat), w_A(Xhat), qbar_source_weight", "RETAIN_FINITE_BRANCH", "one universal Hilbert source/current owner is not parent-signed", "WEP;Newton_GM;R10;PPN"),
        ("CHA1097_5_species_constants", "species charge/constant labels", "theta_A(I_hid) or representation constants with nontrivial vertical action", "NOT_UNIVERSALIZED", "GEN1092_5 remains a surviving generator debt", "WEP;clock;source charge"),
    ]
    return [
        {
            "channel_id": channel_id,
            "constant_sector_channel": channel,
            "coefficient_symbol": symbol,
            "current_status": status,
            "why_not_zero": why,
            "observable_arenas": arenas,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for channel_id, channel, symbol, status, why, arenas in specs
    ]


def finite_source_prior_rows() -> list[dict[str, str]]:
    specs = [
        ("FSP1097_0_c_alpha_DD", "c_alpha_DD", DD_ALPHA_COEFF_MAX, "PRI1096_0_alpha", "DD alpha/Coulomb WEP coefficient threshold"),
        ("FSP1097_1_c_surface_DD", "c_surface_DD", DD_SURFACE_COEFF_MAX, "PRI1096_1_surface", "DD surface/binding WEP coefficient threshold"),
        ("FSP1097_2_c_common_abs", "c_common_abs_if_single_combined_scale", DD_COMMON_COEFF_MAX, "PRI1096_2_common_abs", "DD combined absolute WEP coefficient threshold"),
    ]
    return [
        {
            "prior_id": prior_id,
            "coefficient": coefficient,
            "threshold_abs": f"{threshold:.16e}",
            "source_row": source_row,
            "interpretation": interpretation,
            "source_status": "THRESHOLD_ONLY_NOT_THEORY_PRIOR",
            "promotion_rule": "requires parent derivation or external source-backed coefficient value; threshold alone is not a prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for prior_id, coefficient, threshold, source_row, interpretation in specs
    ]


def finite_source_requirements_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "FSR1097_0_parent_owner",
            "needed_item": "constant-sector parent owner",
            "required_evidence": "action clause showing alpha/mass/binding/source constants are representation/superselection data",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "theorem-zero and claim-valid finite coefficient priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FSR1097_1_external_prior",
            "needed_item": "external source-backed coefficient prior",
            "required_evidence": "literature/source row for actual c_alpha_DD, c_surface_DD, or coefficient vector value with units",
            "current_status": "NOT_ACQUIRED",
            "blocks": "finite coefficient prediction row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FSR1097_2_readout_closure",
            "needed_item": "radiative/effective/readout closure",
            "required_evidence": "proof that bare constant-sector silence survives S_eff and post-variation readout",
            "current_status": "UNSIGNED",
            "blocks": "promoting bare-action zero to observed WEP/clock/R10 zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FSR1097_3_no_cancellation",
            "needed_item": "all-material no-cancellation policy",
            "required_evidence": "parent coefficient vector fixed before material/readout selection",
            "current_status": "POLICY_ACTIVE_NOT_PARENT_THEOREM",
            "blocks": "pair-specific WEP cancellation claims",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1097_0_missing_constant_sector_alpha_prior",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_CONSTANT_SECTOR_ZERO_THEOREM_OR_SOURCE_BACKED_C_ALPHA_PRIOR",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "inputs_present": "conditional theorem; hidden scalar obstruction; DD threshold template",
            "required_inputs": "signed constant-sector zero theorem or external source-backed c_alpha_DD value",
            "derivation_status": "MISSING_SCOREABLE_CONSTANT_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "threshold-only finite prior is not a prediction",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1097_0_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv",
            "source_row": "PRI1096_0_alpha",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only; no source-backed MTS coefficient value",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1097_0_constant_sector_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing constant-sector zero theorem or sourced finite coefficient prior",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1097_0_universality",
            "claim_component": "constant-sector universality theorem",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CSU1097_5_verdict=CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1097_1_finite_prior",
            "claim_component": "finite coefficient prior row",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "threshold templates exist but no external coefficient value/source exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1097_2_product_runner",
            "claim_component": "constant coefficient runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1097_0_theorem",
            "decision": "constant-sector universality is not derived for current MTS",
            "because": "the exact descent/superselection theorem needs alpha, mass, source-weight, hidden scalar, and readout clauses that remain unsigned",
            "next_action": "attack the concrete parent action vertex list or keep finite coefficients explicit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1097_1_finite_route",
            "decision": "finite coefficient source priors remain threshold-only",
            "because": "1096 gives allowed magnitudes but not actual coefficient values",
            "next_action": "require source-backed coefficient values or a parent zero theorem before scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1097_2_best_next",
            "decision": "try the ordinary-constant owner action signature next",
            "because": "universality reduces to forbidding no-extra-F2, no mass-ratio, no binding, and no source-weight vertices in one parent matter action",
            "next_action": "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1097_0_1098",
            "next_target": "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
            "objective": "derive a parent ordinary-constant owner action signature forbidding independent f_X F^2, m_A(Xhat), binding, clock, and source-weight vertices; if it fails, require external source-backed coefficient priors",
            "include": "unique EM kinetic owner; matter spectrum owner; binding/QCD response owner; source-weight exclusion; radiative/readout closure; DD coefficient threshold templates",
            "exclude": "unit-rescaling of dimensionless constants; unsourced priors; one-pair cancellation; tau_WEP=1; clock transfer; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1097_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1097_1_universality_not_derived", any(row["theorem_id"] == "CSU1097_5_verdict" and row["status"] == "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED" for row in theorem_rows), "constant-sector universality verdict is explicit"))
    checks.append(("V1097_2_dimensionless_guard", any(row["theorem_id"] == "CSU1097_2_dimensionless_guard" and row["status"] == "PHYSICS_GUARD_PROVED" for row in theorem_rows), "dimensionless unit-rescaling guard is retained"))
    checks.append(("V1097_3_counterexample_retained", any(row["theorem_id"] == "CSU1097_3_counterexample" and row["status"] == "COUNTEREXAMPLE_RETAINED" for row in theorem_rows), "hidden scalar counterexample is retained"))
    checks.append(("V1097_4_channels_nonclaim", len(channel_rows) == 6 and all(row["valid_for_claim"] == "false" for row in channel_rows), "constant channels remain nonclaim and audited"))
    checks.append(("V1097_5_prior_thresholds_numeric", len(prior_rows) == 3 and all(parse_float(row["threshold_abs"]) is not None and float(row["threshold_abs"]) > 0 for row in prior_rows), "finite source-prior thresholds are positive numeric"))
    checks.append(("V1097_6_requirements_blocked", requirement_rows and all(row["valid_for_claim"] == "false" for row in requirement_rows), "finite source requirements remain blocked/nonclaim"))
    checks.append(("V1097_7_prediction_missing_nonclaim", any("MISSING_CONSTANT_SECTOR" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing zero theorem or source-backed prior"))
    checks.append(("V1097_8_bound_threshold_positive", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0, "coefficient threshold bound is positive numeric"))
    checks.append(("V1097_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1097_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local claim"))
    checks.append(("V1097_11_next_target", any(row["next_target"].startswith("1098-Y5-R10-ordinary-constant-owner") for row in next_rows), "1098 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1097_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1097_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1097 CSV outputs parse cleanly"))
    checks.append(("V1097_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1097_SUMMARY", True, "constant-sector universality not derived; finite coefficients remain explicit; ordinary-constant owner signature is next"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1097-Y5-R10 constant-sector universality theorem or finite coefficient source prior",
            "",
            "## Current verdict",
            "1097 reaches the central coupling lock. The constant-sector theorem is exact as a conditional: if ordinary constants descend through the observed quotient or are fixed representation/superselection data, then their vertical derivatives vanish. But the current corpus does not sign that premise for alpha, mass ratios, binding/QCD response, clock standards, or source weights. A surviving hidden invariant scalar still gives the countermodel `theta_A=theta_0 exp(epsilon I_hid)`. So constant-sector universality is not a current MTS theorem. The finite route remains explicit: source-backed coefficient values or parent zero theorems are required before any WEP/clock/R10 claim.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Constant-sector universality attempt",
            md_table(theorem_rows, ["theorem_id", "claim_piece", "mathematical_statement", "status", "proof_or_obstruction"]),
            "## Channel audit",
            md_table(channel_rows, ["channel_id", "constant_sector_channel", "coefficient_symbol", "current_status", "why_not_zero", "observable_arenas"]),
            "## Finite coefficient source-prior ledger",
            md_table(prior_rows, ["prior_id", "coefficient", "threshold_abs", "source_row", "interpretation", "source_status", "promotion_rule"]),
            "## Source-prior requirements",
            md_table(requirement_rows, ["requirement_id", "needed_item", "required_evidence", "current_status", "blocks"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = universality_theorem_rows()
    channel_rows = channel_audit_rows()
    prior_rows = finite_source_prior_rows()
    requirement_rows = finite_source_requirements_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1097_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
        "channels": OUT / "P8_Y5_R10_1097_CONSTANT_CHANNEL_AUDIT.csv",
        "priors": OUT / "P8_Y5_R10_1097_FINITE_COEFFICIENT_SOURCE_PRIOR_LEDGER.csv",
        "requirements": OUT / "P8_Y5_R10_1097_SOURCE_PRIOR_REQUIREMENTS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1097_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1097_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1097_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1097_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1097_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1097_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["channels"], channel_rows)
    write_csv(outputs["priors"], prior_rows)
    write_csv(outputs["requirements"], requirement_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        theorem_rows,
        channel_rows,
        prior_rows,
        requirement_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem_rows,
        channel_rows,
        prior_rows,
        requirement_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
