from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2681"
BRANCH_ID = "Y5_R2FR_QUOTIENT_COEFFICIENT_ALGEBRA_EXHAUSTION_OR_SOURCE_PREFACTOR_RESIDUAL_ROW_2681"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2681-Y5-R2FR-quotient-coefficient-algebra-exhaustion-or-source-prefactor-residual-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2681_SOURCE_REGISTER.csv",
    "algebra_audit": RESIDUALS / "P8_Y5_R2FR_2681_COEFFICIENT_ALGEBRA_EXHAUSTION_AUDIT.csv",
    "target_inventory": RESIDUALS / "P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv",
    "prefactor_rows": RESIDUALS / "P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2681_ALGEBRA_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2681_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2681_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2681_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2681_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2681_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_algebra": WEP_COEFF / "quotient_coefficient_algebra_exhaustion_audit_nonclaim_2681.csv",
    "microscope_inventory": WEP_COEFF / "coefficient_target_inventory_nonclaim_2681.csv",
    "microscope_prefactors": WEP_COEFF / "source_prefactor_residual_rows_nonclaim_2681.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "SOURCE_PREFACTOR_RESIDUAL_ROWS_2681_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "source_prefactor_residual_rows_2681_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2681_2680_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2680_NEXT_TARGET.csv",
        "required_needles": ["NEXT2680_0_selected", "quotient-coefficient-algebra-exhaustion", "no source-prefactor target"],
        "purpose": "confirms the selected 2681 target",
    },
    {
        "source_id": "SRC2681_2680_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2680_HOM_EXCLUSION_DERIVATION_AUDIT.csv",
        "required_needles": ["HOM2680_3_forbidden_target_route", "HOM2680_7_scalar_counterexample", "HOM2680_8_verdict"],
        "purpose": "imports Hom exclusion verdict and scalar obstruction",
    },
    {
        "source_id": "SRC2681_2680_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2680_PARENT_LINE_BUNDLE_OBJECT_LANGUAGE_CONTRACT_NONCLAIM.csv",
        "required_needles": ["LBH2680_1_coefficient_algebra", "LBH2680_2_source_prefactor_target_absent", "LBH2680_6_verdict"],
        "purpose": "imports coefficient algebra and source-prefactor target clauses",
    },
    {
        "source_id": "SRC2681_2680_COUNTERMODELS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2680_SUBACTION_HOM_COUNTERMODEL_ROWS_NONCLAIM.csv",
        "required_needles": ["HCR2680_0_hidden_scalar_prefactor", "HCR2680_1_species_source_weight", "HCR2680_6_absolute_envelope"],
        "purpose": "imports finite Hom/source-prefactor residual rows",
    },
    {
        "source_id": "SRC2681_COEFF_HOM",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv",
        "required_needles": ["CDH1480_0_target", "CDH1480_2_target_forbidden", "CDH1480_3_scalar_counterexample", "CDH1480_5_verdict"],
        "purpose": "primary coefficient-domain Hom attempt and counterexample",
    },
    {
        "source_id": "SRC2681_TYPED_GRAMMAR",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv",
        "required_needles": ["TNG1470_0_target", "TNG1470_1_type_theorem", "TNG1470_3_no_extension", "TNG1470_5_verdict"],
        "purpose": "typed visible coefficient grammar and no-extension route",
    },
    {
        "source_id": "SRC2681_TYPED_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_typed_grammar_signing_decision_1470.csv",
        "required_needles": ["SIGN1470_0_typed_grammar", "parent_typed_grammar_signed", "REFUSE_TYPED_GRAMMAR_PROMOTION_FILL_COMPARISON_SOURCES_NONCLAIM"],
        "purpose": "confirms typed grammar is not signed",
    },
    {
        "source_id": "SRC2681_VISIBLE_ALGEBRA",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_visible_algebra_signing_decision_1468.csv",
        "required_needles": ["SIGN1468_0_visible_algebra", "hidden invariant algebra triviality", "REFUSE_VISIBLE_ALGEBRA_PROMOTION_KEEP_RETAINED_ALPHA_BOUND_ROWS"],
        "purpose": "visible coefficient algebra/triviality decision",
    },
    {
        "source_id": "SRC2681_HIDDEN_INVARIANT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_hidden_invariant_signing_decision_1469.csv",
        "required_needles": ["SIGN1469_0_hidden_invariant", "scalar_obstruction_retained", "REFUSE_HIDDEN_ALGEBRA_PROMOTION_WRITE_NONCLAIM_PRODUCT_RUNNER"],
        "purpose": "hidden invariant algebra decision",
    },
    {
        "source_id": "SRC2681_RADIATIVE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_radiative_readout_signing_decision_1471.csv",
        "required_needles": ["SIGN1471_0_radiative_readout", "parent_radiative_closure_signed", "REFUSE_RADIATIVE_READOUT_PROMOTION_FILL_PREDICTION_DEFINITIONS_NONCLAIM"],
        "purpose": "radiative/readout closure decision",
    },
    {
        "source_id": "SRC2681_MOMS",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv",
        "required_needles": ["MOMS1088_4_no_species_weights", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "MOMS1088_6_no_shadow_domain", "NO_SHADOW_DOMAIN_UNSIGNED"],
        "purpose": "ordinary matter signature map and no-shadow/source-weight clauses",
    },
    {
        "source_id": "SRC2681_NO_SOURCE_PREF",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
        "required_needles": ["NST1479_2_operator_domain", "POWERFUL_IF_SIGNED_NOT_REDUCED", "NST1479_3_same_action_limit"],
        "purpose": "source-only prefactor typing theorem",
    },
    {
        "source_id": "SRC2681_AX1090",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv",
        "required_needles": ["AXRED1441_1_no_hidden_visible_hom", "AXRED1441_3_fixed_constants", "NOT_REDUCED"],
        "purpose": "AX1090 coefficient/constant reductions remain unsigned",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def algebra_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ALG2681_0_target",
            "claim_piece": "quotient coefficient algebra exhaustion",
            "candidate_statement": "Every admissible ordinary-matter active coefficient is generated by quotient observables, fixed representation data, in-action gauge/current data, and universal constants.",
            "proof_move": "prove this generator list is exhaustive and contains no active source-prefactor target",
            "current_evidence": "2680 selects this as the least smuggly route; 1470/1480 give conditionals only",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_DERIVED",
            "blocking_clauses": "exhaustiveness; no source-prefactor target; no hidden invariant scalar; no readout/radiative extension",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_NEXT_TARGET.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                ]
            ),
            "exact_conditional": "false",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "inventory allowed and forbidden coefficient targets",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_1_generator_list",
            "claim_piece": "allowed coefficient generators",
            "candidate_statement": "Coeff_allowed = Alg[O(Q_obs), theta_rep, gauge/current data internal to L_A, universal constants].",
            "proof_move": "separate allowed matter/gauge constants from forbidden gravitational source multipliers",
            "current_evidence": "typed grammar and MOMS rows support the shape",
            "current_status": "CONTRACT_CANDIDATE_NOT_EXHAUSTIVE",
            "blocking_clauses": "generator list is plausible but not proven exhaustive by a parent universal property",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv")),
                ]
            ),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "prove no-extension/exhaustion, not merely list accepted examples",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_2_quotient_pullback",
            "claim_piece": "quotient-observable coefficients",
            "candidate_statement": "If c=q_obs^*c_bar, hidden/vertical derivatives vanish by the chain rule.",
            "proof_move": "use quotient pullback to make hidden coefficient maps nonobjects",
            "current_evidence": "2680 records this as an exact conditional lemma",
            "current_status": "EXACT_CONDITIONAL_LEMMA",
            "blocking_clauses": "does not cover coefficients not proven to factor through q_obs",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_HOM_EXCLUSION_DERIVATION_AUDIT.csv")),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "pair pullback lemma with exhaustive coefficient-domain theorem",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_3_forbidden_target",
            "claim_piece": "source-prefactor target absent",
            "candidate_statement": "Coeff_source-prefactor is not an object in the parent algebra; Hom into it is empty/common by target absence.",
            "proof_move": "forbid the target, not the maps into it after the fact",
            "current_evidence": "CDH1480_2 and NST1479_2 mark this as powerful but not reduced",
            "current_status": "POWERFUL_CONDITIONAL_NOT_REDUCED",
            "blocking_clauses": "parent source-prefactor target normal form not written",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                ]
            ),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "write a source-prefactor target normal-form gate",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_4_product_category_route",
            "claim_piece": "visible-hidden product category sequester",
            "candidate_statement": "If C_parent=C_vis x C_hid and S_vis factors through pi_vis, hidden derivatives of visible coefficients vanish.",
            "proof_move": "use product projection as a coefficient-domain separation theorem",
            "current_evidence": "TNG1470_2 states the conditional theorem",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_clauses": "parent product category and projection functors are not constructed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive product/projection category or do not use this route",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_5_hidden_invariant_triviality",
            "claim_piece": "hidden invariant algebra has no nonconstant scalar",
            "candidate_statement": "O(C_hid)^inv=R would collapse hidden source coefficients to common constants.",
            "proof_move": "remove scalar counterexample by proving no nonconstant invariant scalar exists",
            "current_evidence": "1468/1469 refuse hidden/visible algebra promotion and retain scalar obstruction",
            "current_status": "HIDDEN_TRIVIALITY_NOT_PARENT_SIGNED",
            "blocking_clauses": "orbit transitivity; no-extra-invariant; discrete sector; radiative closure",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_visible_algebra_signing_decision_1468.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_hidden_invariant_signing_decision_1469.csv")),
                ]
            ),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "keep c(I_hid) residual until hidden algebra closes",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_6_fixed_representation_constants",
            "claim_piece": "representation constants are fixed non-source data",
            "candidate_statement": "theta_rep can enter L_A as measured nongravitational data, but cannot define active gravitational source prefactors.",
            "proof_move": "classify species constants as representation/superselection data, not source functions",
            "current_evidence": "AX1090_3 and MOMS1088_3 remain partial/unsigned",
            "current_status": "FIXED_CONSTANT_OWNER_INCOMPLETE",
            "blocking_clauses": "alpha/mass/clock/material constants not parent-signed as fixed or explicit residuals",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv")),
                ]
            ),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "retain constant-sector residuals; do not hide source prefactors in theta_rep",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_7_no_extension_radiative",
            "claim_piece": "no readout/radiative extension of coefficient targets",
            "candidate_statement": "S_eff, source-worldtube, detector/readout and counterterms preserve the same coefficient algebra.",
            "proof_move": "prevent source-prefactor target from reappearing after bare parent variation",
            "current_evidence": "1470/1471 mark no-extension/radiative closure unsigned",
            "current_status": "NO_EXTENSION_RADIATIVE_UNSIGNED",
            "blocking_clauses": "readout kernels; threshold/counterterm maps; source-worldtube closure",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_radiative_readout_signing_decision_1471.csv")),
                ]
            ),
            "exact_conditional": "false",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "retain source-tail residuals after bare algebra",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ALG2681_8_verdict",
            "claim_piece": "coefficient algebra exhaustion closes source-prefactor slot",
            "candidate_statement": "Allowed generators exhaustive + source-prefactor target absent + no extension would remove c(I_hid), w_A, c_A, sigma_label and source-tail coefficients as parent objects.",
            "proof_move": "attempt to turn the target inventory into a parent theorem",
            "current_evidence": "exact conditionals exist, but exhaustion and source-prefactor target absence are not parent-signed",
            "current_status": "COEFFICIENT_ALGEBRA_EXHAUSTION_NOT_DERIVED",
            "blocking_clauses": "target normal form; hidden scalar obstruction; fixed constants; radiative/readout closure",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_HOM_EXCLUSION_DERIVATION_AUDIT.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                ]
            ),
            "exact_conditional": "true",
            "counterexample_active": "true",
            "target_exhaustive": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "write parent source-prefactor target normal form or keep finite residual rows",
            "timestamp_utc": stamp(),
        },
    ]


def target_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "TGT2681_0_quotient_observable",
            "target_class": "allowed_if_parent_signed",
            "coefficient_target": "O(Q_obs)",
            "role": "visible quotient observables/coframe/metric response",
            "current_status": "CONDITIONAL_PULLBACK_ONLY",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_HOM_EXCLUSION_DERIVATION_AUDIT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "prove q_obs coefficient pullback covers the retained local branch",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_1_representation_constants",
            "target_class": "allowed_but_not_source_prefactor",
            "coefficient_target": "theta_rep",
            "role": "fixed masses/charges/representation labels inside nongravitational matter terms",
            "current_status": "FIXED_CONSTANT_OWNER_INCOMPLETE",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "separate fixed theta_rep from active source weights",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_2_gauge_current_in_action",
            "target_class": "allowed_if_inside_LA",
            "coefficient_target": "gauge/current data inside L_A",
            "role": "ordinary QED/QCD/current coupling inside the matter action",
            "current_status": "NOT_SOURCE_NORMALIZATION_OWNER",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "do not confuse gauge coupling with active gravitational source prefactor",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_3_universal_constants",
            "target_class": "allowed_common_calibration",
            "coefficient_target": "universal constants/common End(A_ord) scalars",
            "role": "global calibration constants common to the connected ordinary component",
            "current_status": "COMMON_ONLY_IF_LINE_OWNER_SIGNED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "do not promote common mode until line owner is signed",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_4_active_source_prefactor",
            "target_class": "forbidden_target_candidate",
            "coefficient_target": "Coeff_source-prefactor",
            "role": "w_A, c_A, kappa_A, source-only scalar multipliers before variation",
            "current_status": "TARGET_ABSENCE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "write parent normal-form clause declaring this target absent or residual",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_5_hidden_scalar_extension",
            "target_class": "forbidden_or_residual",
            "coefficient_target": "c(I_hid)",
            "role": "hidden invariant scalar feeding an active source coefficient",
            "current_status": "SCALAR_COUNTEREXAMPLE_ACTIVE",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_hidden_invariant_signing_decision_1469.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "prove hidden invariant algebra trivial or retain finite c(I_hid)",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_6_readout_tail_extension",
            "target_class": "forbidden_or_residual",
            "coefficient_target": "C_eff_source_tail",
            "role": "radiative/readout/source-worldtube extension of coefficient domains",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_radiative_readout_signing_decision_1471.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "close readout/radiative no-extension or keep residual tail",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TGT2681_7_verdict",
            "target_class": "inventory_verdict",
            "coefficient_target": "coefficient target inventory exhaustive",
            "role": "all allowed and forbidden targets parent-signed in one normal form",
            "current_status": "INVENTORY_NOT_EXHAUSTIVE_FOR_CLAIM",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_PARENT_LINE_BUNDLE_OBJECT_LANGUAGE_CONTRACT_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "normal-form source-prefactor target gate is next",
            "timestamp_utc": stamp(),
        },
    ]


def prefactor_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SPR2681_0_hidden_scalar_source_prefactor",
            "symbol": "c(I_hid)",
            "residual_meaning": "hidden invariant scalar feeds active source-prefactor target",
            "formula_or_contract": "c(I_hid)=constant or absent only if hidden algebra triviality or target absence is parent-signed",
            "arena_links": "WEP;R10;clock;PPN;local-GR",
            "status": "COUNTERMODEL_ACTIVE_NONCLAIM",
            "units": "dimensionless or declared source coefficient",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_SUBACTION_HOM_COUNTERMODEL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove target absence or keep finite source coefficient",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SPR2681_1_species_action_weight",
            "symbol": "Delta_w_AB",
            "residual_meaning": "species/action source weight survives coefficient algebra",
            "formula_or_contract": "Delta_w_AB=0 only if source-prefactor target absent and line owner/common mode signed",
            "arena_links": "WEP;Newton-source;R10;local-GR",
            "status": "SOURCE_PREFACTOR_TARGET_OPEN",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "normal-form forbid w_A or source finite row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SPR2681_2_current_rescaling_prefactor",
            "symbol": "c_A or kappa_A",
            "residual_meaning": "post/pre-variation current normalization scalar remains live",
            "formula_or_contract": "current rescaling is illegal only after variation-order and coefficient target absence are signed",
            "arena_links": "WEP;PPN;clock;source-normalization",
            "status": "CURRENT_SOURCE_PREFACTOR_OPEN",
            "units": "dimensionless after source normalization",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "separate current owner proof from coefficient target absence",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SPR2681_3_readout_tail_prefactor",
            "symbol": "C_eff_source_tail",
            "residual_meaning": "readout/radiative/counterterm extension creates source coefficient",
            "formula_or_contract": "C_eff_source_tail=0 only if no-extension/radiative closure is parent-signed",
            "arena_links": "EM;clock;R10;WEP",
            "status": "READOUT_RADIATIVE_TAIL_OPEN",
            "units": "declared per effective coefficient",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_radiative_readout_signing_decision_1471.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive no-extension closure or source finite tail row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SPR2681_4_no_cancellation_envelope",
            "symbol": "epsilon_source_prefactor_total",
            "residual_meaning": "absolute source-prefactor residual envelope",
            "formula_or_contract": "abs(epsilon_total)>=abs(c(I_hid))+abs(Delta_w_AB)+abs(c_A/kappa_A)+abs(C_eff_source_tail)",
            "arena_links": "all local source arenas",
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "units": "dimensionless/envelope",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2680_SUBACTION_HOM_COUNTERMODEL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only after every component is zero or source-backed",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SPR2681_5_acquisition_template",
            "symbol": "K_pref * tau_arena * epsilon_source_prefactor_total",
            "residual_meaning": "future finite source-prefactor arena projection",
            "formula_or_contract": "arena score requires K_pref, tau_arena, source paths, units and no-cancellation statement",
            "arena_links": "WEP;R10;PPN;clock;orbital",
            "status": "ACQUISITION_TEMPLATE_NONCLAIM",
            "units": "declared per arena",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_reduction_gates_1480.csv")),
            "score_ready": "false",
            "parent_zero_available": "false",
            "has_numeric_value": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill only if normal-form theorem fails and projections are sourced",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], inventory_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2681_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "coefficient_algebra_audit",
                "target_exhaustive": row["target_exhaustive"],
                "counterexample_active": row["counterexample_active"],
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(path).exists() for path in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_COEFFICIENT_ALGEBRA_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in inventory_rows:
        rows.append(
            {
                "runner_id": f"RUN2681_{row['target_id']}",
                "target_id": row["target_id"],
                "stage": "target_inventory",
                "target_exhaustive": "false",
                "counterexample_active": "true",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_TARGET_INVENTORY_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in residual_rows:
        rows.append(
            {
                "runner_id": f"RUN2681_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "source_prefactor_residual",
                "target_exhaustive": "false",
                "counterexample_active": "true",
                "has_parent_zero": row["parent_zero_available"],
                "has_numeric_bound": row["has_numeric_value"],
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_SOURCE_PREFACTOR_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2681_0_conditionals",
            "claim": "coefficient-domain conditionals are useful",
            "status": "PASS_CONDITIONAL_ONLY",
            "blocking_rows": "ALG2681_2_quotient_pullback;ALG2681_3_forbidden_target;ALG2681_4_product_category_route",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2681_1_exhaustion",
            "claim": "allowed coefficient generator list is exhaustive",
            "status": "FAIL_EXHAUSTION_NOT_PARENT_SIGNED",
            "blocking_rows": "ALG2681_1_generator_list;TGT2681_7_verdict",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2681_2_source_prefactor_target",
            "claim": "active source-prefactor target is absent",
            "status": "FAIL_TARGET_ABSENCE_UNSIGNED",
            "blocking_rows": "ALG2681_3_forbidden_target;TGT2681_4_active_source_prefactor",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2681_3_scalar_counterexample",
            "claim": "hidden scalar source-prefactor counterexample is killed",
            "status": "FAIL_COUNTEREXAMPLE_ACTIVE",
            "blocking_rows": "ALG2681_5_hidden_invariant_triviality;SPR2681_0_hidden_scalar_source_prefactor",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2681_4_residual_scoring",
            "claim": "source-prefactor residual vector can be scored",
            "status": "FAIL_COMPONENTS_MISSING_NUMERIC_OR_THEOREM_ZERO",
            "blocking_rows": "SPR2681_0_hidden_scalar_source_prefactor;SPR2681_1_species_action_weight;SPR2681_4_no_cancellation_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2681_5_local_GR",
            "claim": "local GR/PPN can use coefficient algebra to silence source prefactors",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "ALG2681_8_verdict;CG2681_1_exhaustion;CG2681_2_source_prefactor_target;CG2681_3_scalar_counterexample",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2681_0_derivation_attempt",
            "question": "Can 2681 prove coefficient algebra exhaustion?",
            "result": "not_yet",
            "reason": "allowed-generator list is plausible and conditionally useful, but no parent theorem proves it exhaustive or excludes source-prefactor target objects",
            "action": "do not promote Hom/source-prefactor theorem-zero",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2681_1_best_progress",
            "question": "What was gained?",
            "result": "normal-form target identified",
            "reason": "the missing claim is not vague coupling; it is the absence of a specific target object Coeff_source-prefactor",
            "action": "write a source-prefactor target normal-form gate next",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2681_2_fallback",
            "question": "What if normal-form target absence fails?",
            "result": "finite source-prefactor rows remain",
            "reason": "c(I_hid), Delta_w_AB, c_A/kappa_A and readout tails are explicit nonclaim components",
            "action": "source numeric residuals only after projection and no-cancellation inputs exist",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2681_3_next_route",
            "question": "Best next target?",
            "result": "parent_source_prefactor_target_normal_form",
            "reason": "normal-form absence of the target is the cleanest way to beat the scalar counterexample without assuming WEP",
            "action": "select 2682",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2681_0_selected",
            "kind": "selected",
            "target_doc": "2682-Y5-R2FR-parent-source-prefactor-target-normal-form-or-finite-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_parent_source_prefactor_target_normal_form_or_finite_coefficient_row_2682.py",
            "purpose": "write the parent ordinary-matter coefficient target normal form and decide whether active source-prefactor targets are absent, forbidden, or retained as finite nonclaim coefficients",
            "acceptance_gate": "every ordinary coefficient target is classified as allowed, forbidden, or residual; Coeff_source-prefactor absent by parent normal form or explicit finite rows carry source paths, units, arena projections, and no-cancellation guards",
            "forbidden_shortcuts": "assuming EEP/WEP; deleting scalar counterexample; treating allowed examples as exhaustive; importing Delta_w=0; bound inversion; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2681_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2681_1_progress",
            "field": "coefficient_algebra_route",
            "value": "allowed-generator list separated from forbidden source-prefactor target",
            "status": "sharpened_not_claimed",
            "note": "the next real proof is target normal form, not a WEP-facing fit",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2681_2_next",
            "field": "next_derivation",
            "value": "parent_source_prefactor_target_normal_form",
            "status": "selected",
            "note": "classify Coeff_source-prefactor as absent/forbidden/residual",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2681_0_algebra",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["algebra_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_algebra"]),
            "contents": "coefficient algebra exhaustion audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2681_1_inventory",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["target_inventory"]),
            "destination": str(BRANCH_OUTPUTS["microscope_inventory"]),
            "contents": "coefficient target inventory retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2681_2_prefactors",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["prefactor_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_prefactors"]),
            "contents": "source-prefactor residual rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2681_3_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["prefactor_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight source-prefactor rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2681_4_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["prefactor_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local bound source-prefactor rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_sources_exist_and_needles_found", "passed": as_bool(source_ok), "details": "all cited source paths exist and required needles are present"})

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_nonclaim_guard", "passed": as_bool(all_nonclaim), "details": "all generated rows carry valid_for_claim=false"})

    verdict_blocks = any(row["audit_id"] == "ALG2681_8_verdict" and row["current_status"] == "COEFFICIENT_ALGEBRA_EXHAUSTION_NOT_DERIVED" for row in rows["algebra_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_verdict_blocks_claim", "passed": as_bool(verdict_blocks), "details": "coefficient algebra exhaustion is not promoted"})

    allowed_not_exhaustive = any(row["audit_id"] == "ALG2681_1_generator_list" and row["current_status"] == "CONTRACT_CANDIDATE_NOT_EXHAUSTIVE" for row in rows["algebra_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_allowed_list_not_overclaimed", "passed": as_bool(allowed_not_exhaustive), "details": "allowed generator list is not treated as exhaustive"})

    target_open = any(row["target_id"] == "TGT2681_4_active_source_prefactor" and row["current_status"] == "TARGET_ABSENCE_NOT_PARENT_SIGNED" for row in rows["target_inventory"])
    counterexample_open = any(row["target_id"] == "TGT2681_5_hidden_scalar_extension" and row["current_status"] == "SCALAR_COUNTEREXAMPLE_ACTIVE" for row in rows["target_inventory"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_target_and_counterexample_open", "passed": as_bool(target_open and counterexample_open), "details": "source-prefactor target and hidden scalar obstruction remain open"})

    residual_ids = {row["row_id"] for row in rows["prefactor_rows"]}
    residuals_complete = {"SPR2681_0_hidden_scalar_source_prefactor", "SPR2681_1_species_action_weight", "SPR2681_2_current_rescaling_prefactor", "SPR2681_4_no_cancellation_envelope"}.issubset(residual_ids)
    residuals_nonclaim = all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in rows["prefactor_rows"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_prefactor_rows_complete_nonclaim", "passed": as_bool(residuals_complete and residuals_nonclaim), "details": "source-prefactor residual rows exist and remain nonclaim"})

    gates_ok = any(row["gate_id"] == "CG2681_5_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and any(row["gate_id"] == "CG2681_1_exhaustion" and row["status"] == "FAIL_EXHAUSTION_NOT_PARENT_SIGNED" for row in rows["claim_gates"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_claim_gates_correct", "passed": as_bool(gates_ok), "details": "local-GR remains blocked and exhaustion gate fails"})

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_runner_refuses_unsigned_rows", "passed": as_bool(runner_refuses), "details": "runner refuses scoring without parent zero or numeric residuals"})

    next_selected = any(row["target_id"] == "NEXT2681_0_selected" and "2682-Y5-R2FR-parent-source-prefactor-target-normal-form-or-finite-coefficient-row.md" in row["target_doc"] for row in rows["next_target"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_next_target_selected", "passed": as_bool(next_selected), "details": "next target selects source-prefactor target normal form"})

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_csv_parse", "passed": as_bool(csv_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))})

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_branch_copies_parse", "passed": as_bool(branch_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse))})

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_formalization_write_guard", "passed": as_bool(formalization_guard), "details": "generated path allowlist excludes formalization-workbench"})

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_pycache_absent_at_validation_time", "passed": as_bool(pycache_absent), "details": "scripts/__pycache__ absent when validation rows were produced"})

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2681_pycache_absent_at_validation_time")
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2681_OVERALL", "passed": as_bool(overall), "details": "2681 refuses to treat allowed coefficient examples as exhaustive, keeps the source-prefactor target open, and selects normal-form target classification next"})
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} - Quotient Coefficient Algebra Exhaustion Or Source-Prefactor Residual Row",
        "",
        "## Private Verdict",
        "",
        "2681 is useful because it stops a subtle cheat. A list of allowed coefficient generators is not a proof that no other generator exists. To close the coupling slot, the parent theory must prove the ordinary coefficient algebra is exhausted by quotient observables, fixed representation data, in-action gauge/current data, and universal constants, while the active source-prefactor target is absent.",
        "",
        "Current status: not closed. The quotient pullback, product-category, and forbidden-target routes are clean conditionals, but none is parent-signed. The scalar counterexample remains active: if `Coeff_source-prefactor` exists and a nonconstant `I_hid` is admissible, `c(I_hid) O_source` is legal.",
        "",
        "Therefore `Delta_w_AB=0`, WEP, R10, PPN, clock, orbital and local-GR source-silence claims remain blocked. The next target is the source-prefactor target normal form: classify every coefficient target as allowed, forbidden, or explicit residual.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Coefficient Algebra Exhaustion Audit",
        "",
        markdown_table(rows["algebra_audit"]),
        "",
        "## Coefficient Target Inventory",
        "",
        markdown_table(rows["target_inventory"]),
        "",
        "## Source-Prefactor Residual Rows",
        "",
        markdown_table(rows["prefactor_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["algebra_audit"] = algebra_audit_rows()
    rows["target_inventory"] = target_inventory_rows()
    rows["prefactor_rows"] = prefactor_rows()
    rows["runner_results"] = runner_results_rows(rows["algebra_audit"], rows["target_inventory"], rows["prefactor_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "algebra_audit",
        "target_inventory",
        "prefactor_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_algebra"], rows["algebra_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_inventory"], rows["target_inventory"])
    write_csv(BRANCH_OUTPUTS["microscope_prefactors"], rows["prefactor_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["prefactor_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["prefactor_rows"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
