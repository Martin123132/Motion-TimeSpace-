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
DOC = ROOT / "1096-Y5-R10-parent-coefficient-vector-zero-theorem-or-DD-coefficient-prior-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1096-parent-coefficient-vector-zero" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1096_WEP_COEFFICIENT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1096_WEP_COEFFICIENT_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15
DD_ALPHA_COEFF_MAX = 8.320244933243533e-10
DD_SURFACE_COEFF_MAX = 6.987501646143863e-11
DD_COMBINED_COEFF_MAX = 6.446142229433907e-11


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
        ("SRC1096_0_1095_next", "source-intake/mts_residuals/P8_Y5_R10_1095_NEXT_TARGET.csv", "NEXT1095_0_1096", "1095 handoff."),
        ("SRC1096_1_1095_thresholds", "source-intake/mts_residuals/P8_Y5_R10_1095_DD_COEFFICIENT_THRESHOLDS.csv", "THR1095_0_alpha", "1095 DD coefficient thresholds."),
        ("SRC1096_2_1095_action", "source-intake/mts_residuals/P8_Y5_R10_1095_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv", "PAC1095_4_verdict", "parent Xhat WEP action clause failure."),
        ("SRC1096_3_1091_operator", "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODH1091_6_verdict", "hidden-visible coefficient hom theorem failure."),
        ("SRC1096_4_1092_triviality", "source-intake/mts_residuals/P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv", "HIT1092_5_verdict", "hidden invariant algebra triviality failure."),
        ("SRC1096_5_1077_WEP_owner", "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv", "WCO1077_5_verdict", "WEP owner theorem attempt."),
        ("SRC1096_6_1081_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "PB1081_4_verdict", "parent WEP basis failure."),
        ("SRC1096_7_1087_no_cancel", "source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv", "AMC1087_0_pair_line_forbidden", "no cancellation policy."),
        ("SRC1096_8_1083_DD_product", "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT1083_0_alpha", "DD source-material product rows."),
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


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "CZ1096_0_target",
            "claim_piece": "DD/material coefficient vector zero",
            "mathematical_statement": "c_I = partial_Xhat ln theta_I = 0 for all ordinary matter response basis coefficients",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "would remove WEP alpha/surface/source product residuals at the coefficient level",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "CZ1096_1_sufficient_conditions",
            "claim_piece": "constant-sector universality plus no hidden-visible hom",
            "mathematical_statement": "theta_I are parent superselection constants and Hom(C_hid,Coeff(O_vis)) is trivial",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "then every c_I vanishes by differentiation along Xhat",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "CZ1096_2_current_obstruction",
            "claim_piece": "hidden scalar coefficient counterexample",
            "mathematical_statement": "if I_hid survives, c_alpha(I_hid)=epsilon or c_alpha=c0+epsilon I_hid is allowed by ordinary symmetries",
            "status": "COUNTEREXAMPLE_RETAINED",
            "proof_or_obstruction": "1091 and 1092 retain the scalar obstruction and hidden invariant generator debt",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "CZ1096_3_WEP_owner_limit",
            "claim_piece": "WEP coupling owner theorem",
            "mathematical_statement": "P_WEP=0 after object language, species-blind action measure, current owner, and readout/source closure are signed",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "1077 gives the shape but not the parent signatures",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "CZ1096_4_verdict",
            "claim_piece": "derive c_I=0 now",
            "mathematical_statement": "coefficient vector zero follows for current MTS corpus",
            "status": "COEFFICIENT_ZERO_NOT_DERIVED",
            "proof_or_obstruction": "constant-sector universality, no hidden-visible hom, basis ownership, and readout closure are unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "COB1096_0_hidden_scalar",
            "obstruction": "surviving hidden invariant scalar",
            "effect": "permits nonzero c_alpha, c_surface, mass, clock, or source coefficients",
            "source_basis": "ODH1091_2_scalar_obstruction; HIT1092_3_scalar_counterexample",
            "needed_to_clear": "prove O(C_hid)^inv=R or exact scalar nohair with source/readout closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "COB1096_1_constant_sector",
            "obstruction": "constant-sector universality not parent-signed",
            "effect": "ordinary alpha/QCD/mass/binding constants can carry Xhat dependence",
            "source_basis": "ODH1091_6_verdict; PAC1095_4_verdict",
            "needed_to_clear": "parent ordinary matter constants as fixed representation/superselection data",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "COB1096_2_basis_owner",
            "obstruction": "DD alpha/surface basis is external comparator, not proven MTS parent basis",
            "effect": "DD thresholds are useful tests but not a derived MTS coefficient basis",
            "source_basis": "PB1081_2_DD_embedding; PB1081_4_verdict",
            "needed_to_clear": "functor from MTS parent matter response to DD/material basis with units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "COB1096_3_readout",
            "obstruction": "effective/readout closure not signed",
            "effect": "bare zero can re-enter through source/readout/material projection",
            "source_basis": "ODH1091_5_radiative_readout_limit; WCO1077_5_verdict",
            "needed_to_clear": "readout-after-variation and same-frame source map theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prior_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "POL1096_0_no_unsourced_priors",
            "rule": "do not invent coefficient priors just to pass WEP",
            "allowed": "false",
            "acceptable_replacement": "derive c_I=0, cite a source-backed prior, or keep threshold-only nonclaim rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "POL1096_1_no_pair_cancellation",
            "rule": "do not tune c_alpha and c_surface to cancel for TA6V-PtRh10 only",
            "allowed": "false",
            "acceptable_replacement": "parent coefficient vector fixed before material pair, checked across materials",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "POL1096_2_threshold_scan",
            "rule": "threshold-bounded scan rows may be used as private robustness diagnostics",
            "allowed": "true_nonclaim_only",
            "acceptable_replacement": "mark valid_for_claim=false until coefficients are derived or sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prior_template_rows() -> list[dict[str, str]]:
    specs = [
        ("PRI1096_0_alpha", "c_alpha_DD", DD_ALPHA_COEFF_MAX, "THR1095_0_alpha"),
        ("PRI1096_1_surface", "c_surface_DD", DD_SURFACE_COEFF_MAX, "THR1095_1_surface"),
        ("PRI1096_2_common_abs", "c_common_abs_if_single_combined_scale", DD_COMBINED_COEFF_MAX, "THR1095_2_combined_abs"),
    ]
    rows: list[dict[str, str]] = []
    for prior_id, coefficient, threshold, source_row in specs:
        rows.append(
            {
                "prior_id": prior_id,
                "coefficient": coefficient,
                "suggested_nonclaim_scan_min": f"{-threshold:.16e}",
                "suggested_nonclaim_scan_max": f"{threshold:.16e}",
                "threshold_abs": f"{threshold:.16e}",
                "source_row": source_row,
                "status": "THRESHOLD_BOUNDED_PRIOR_TEMPLATE_NONCLAIM",
                "promotion_rule": "requires parent derivation or external source for coefficient; threshold alone is not a prediction",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1096_0_missing_c_alpha_DD",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_C_ALPHA_DD_ZERO_THEOREM_OR_SOURCE_PRIOR",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
            "inputs_present": "1095 thresholds; 1091/1092 obstructions; 1077 conditional WEP owner theorem",
            "required_inputs": "signed c_alpha_DD=0 theorem or source-backed numeric c_alpha_DD row",
            "derivation_status": "MISSING_SCOREABLE_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "threshold-bounded prior template is not a prediction",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1096_0_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1095_DD_COEFFICIENT_THRESHOLDS.csv",
            "source_row": "THR1095_0_alpha",
            "bound_type": "absolute_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "private threshold only; no MTS coefficient prediction",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1096_0_coefficient_zero_or_prior_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing c_alpha zero theorem or sourced prior",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1096_0_zero_theorem",
            "claim_component": "c_I=0 coefficient vector theorem",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CZ1096_4_verdict=COEFFICIENT_ZERO_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1096_1_prior",
            "claim_component": "DD coefficient prior row",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "prior template is threshold-bounded but unsourced as a theory coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1096_2_product_runner",
            "claim_component": "coefficient runner",
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
            "decision_id": "DEC1096_0_zero_result",
            "decision": "coefficient-vector zero theorem is not derived",
            "because": "hidden scalar, constant-sector, parent basis, and readout closure obstructions remain live",
            "next_action": "attack constant-sector universality directly or keep finite coefficients explicit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1096_1_prior_result",
            "decision": "threshold-bounded DD prior templates are staged but nonclaim",
            "because": "thresholds constrain what a coefficient may be, but do not derive or source what it is",
            "next_action": "do not use them as evidence unless coefficient provenance is supplied",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1096_2_best_next",
            "decision": "constant-sector universality is the next derivation target",
            "because": "all WEP coefficient-zero routes reduce to whether ordinary constants can depend on hidden invariants",
            "next_action": "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1096_0_1097",
            "next_target": "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
            "objective": "try to derive that ordinary constants/response coefficients are parent superselection data independent of hidden invariants; if not, require external source-backed finite coefficient priors",
            "include": "constant-sector owner; alpha/QCD/mass/binding coefficients; hidden invariant scalar obstruction; radiative/readout closure; DD threshold templates",
            "exclude": "unsourced coefficient priors; one-pair cancellation; tau_WEP=1; clock transfer; WEP/local-GR claim; GitHub; formalization edits",
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
    zero_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    policy_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1096_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1096_1_zero_not_derived", any(row["zero_id"] == "CZ1096_4_verdict" and row["status"] == "COEFFICIENT_ZERO_NOT_DERIVED" for row in zero_rows), "coefficient-zero verdict is explicit"))
    checks.append(("V1096_2_obstructions_retained", len(obstruction_rows) == 4 and all(row["valid_for_claim"] == "false" for row in obstruction_rows), "coefficient obstructions retained as nonclaim"))
    checks.append(("V1096_3_prior_policy_safe", any(row["policy_id"] == "POL1096_0_no_unsourced_priors" and row["allowed"] == "false" for row in policy_rows), "unsourced priors are forbidden"))
    checks.append(("V1096_4_prior_templates_numeric", len(prior_rows) == 3 and all(parse_float(row["threshold_abs"]) is not None and float(row["threshold_abs"]) > 0 for row in prior_rows), "prior templates carry positive threshold bounds"))
    checks.append(("V1096_5_prediction_missing_nonclaim", any("MISSING_C_ALPHA" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing c_alpha source/zero theorem"))
    checks.append(("V1096_6_bound_threshold_positive", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0, "coefficient bound threshold is positive numeric"))
    checks.append(("V1096_7_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1096_8_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local claim"))
    checks.append(("V1096_9_next_target", any(row["next_target"].startswith("1097-Y5-R10-constant-sector") for row in next_rows), "1097 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1096_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1096_11_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1096 CSV outputs parse cleanly"))
    checks.append(("V1096_12_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1096_SUMMARY", True, "coefficient-zero theorem not derived; nonclaim DD prior templates staged; constant-sector universality is next"))
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
    zero_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    policy_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1096-Y5-R10 parent coefficient-vector zero theorem or DD coefficient prior row",
            "",
            "## Current verdict",
            "1096 tries to kill the WEP coefficient vector directly. The exact theorem is simple: if ordinary constants/response coefficients are parent superselection data and no hidden-visible coefficient morphism exists, then every DD/material coefficient `c_I` vanishes. But the present corpus still has the hidden scalar obstruction, unsigned constant-sector universality, external DD-basis ownership, and readout closure gaps. So `c_I=0` is not promoted. The fallback is a nonclaim prior template bounded by the 1095 thresholds, not a prediction.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Coefficient-zero theorem attempt",
            md_table(zero_rows, ["zero_id", "claim_piece", "mathematical_statement", "status", "proof_or_obstruction"]),
            "## Coefficient obstruction ledger",
            md_table(obstruction_rows, ["obstruction_id", "obstruction", "effect", "source_basis", "needed_to_clear"]),
            "## Prior policy",
            md_table(policy_rows, ["policy_id", "rule", "allowed", "acceptable_replacement"]),
            "## DD coefficient prior templates",
            md_table(prior_rows, ["prior_id", "coefficient", "suggested_nonclaim_scan_min", "suggested_nonclaim_scan_max", "threshold_abs", "status", "promotion_rule"]),
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
    zero_rows = zero_theorem_rows()
    obstruction_rows = coefficient_obstruction_rows()
    policy_rows = prior_policy_rows()
    prior_rows = prior_template_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1096_SOURCE_REGISTER.csv",
        "zero_theorem": OUT / "P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_R10_1096_COEFFICIENT_OBSTRUCTION_LEDGER.csv",
        "policy": OUT / "P8_Y5_R10_1096_COEFFICIENT_PRIOR_POLICY.csv",
        "prior_template": OUT / "P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1096_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1096_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1096_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1096_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1096_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1096_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["zero_theorem"], zero_rows)
    write_csv(outputs["obstructions"], obstruction_rows)
    write_csv(outputs["policy"], policy_rows)
    write_csv(outputs["prior_template"], prior_rows)
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
        zero_rows,
        obstruction_rows,
        policy_rows,
        prior_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        zero_rows,
        obstruction_rows,
        policy_rows,
        prior_rows,
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
