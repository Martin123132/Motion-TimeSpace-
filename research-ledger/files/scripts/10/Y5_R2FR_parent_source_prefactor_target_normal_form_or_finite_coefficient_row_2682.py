from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2682"
BRANCH_ID = "Y5_R2FR_PARENT_SOURCE_PREFACTOR_TARGET_NORMAL_FORM_OR_FINITE_COEFFICIENT_ROW_2682"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2682-Y5-R2FR-parent-source-prefactor-target-normal-form-or-finite-coefficient-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2682_SOURCE_REGISTER.csv",
    "normal_form_audit": RESIDUALS / "P8_Y5_R2FR_2682_SOURCE_PREFACTOR_TARGET_NORMAL_FORM_AUDIT.csv",
    "target_classification": RESIDUALS / "P8_Y5_R2FR_2682_COEFFICIENT_TARGET_CLASSIFICATION_NONCLAIM.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2682_FINITE_SOURCE_PREFACTOR_COEFFICIENT_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2682_NORMAL_FORM_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2682_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2682_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2682_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2682_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2682_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_normal_form": WEP_COEFF / "source_prefactor_target_normal_form_audit_nonclaim_2682.csv",
    "microscope_classification": WEP_COEFF / "coefficient_target_classification_nonclaim_2682.csv",
    "microscope_finite": WEP_COEFF / "finite_source_prefactor_coefficient_rows_nonclaim_2682.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "FINITE_SOURCE_PREFACTOR_COEFFICIENT_ROWS_2682_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "finite_source_prefactor_coefficient_rows_2682_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2682_2681_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2681_NEXT_TARGET.csv",
        "required_needles": ["NEXT2681_0_selected", "Coeff_source-prefactor absent by parent normal form", "explicit finite rows"],
        "purpose": "confirms selected 2682 normal-form target",
    },
    {
        "source_id": "SRC2682_2681_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_ALGEBRA_EXHAUSTION_AUDIT.csv",
        "required_needles": ["ALG2681_3_forbidden_target", "COEFFICIENT_ALGEBRA_EXHAUSTION_NOT_DERIVED", "ALG2681_8_verdict"],
        "purpose": "imports coefficient algebra exhaustion failure",
    },
    {
        "source_id": "SRC2682_2681_TARGETS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv",
        "required_needles": ["TGT2681_4_active_source_prefactor", "TARGET_ABSENCE_NOT_PARENT_SIGNED", "TGT2681_7_verdict"],
        "purpose": "imports target inventory",
    },
    {
        "source_id": "SRC2682_2681_PREF_ROWS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv",
        "required_needles": ["SPR2681_0_hidden_scalar_source_prefactor", "SPR2681_1_species_action_weight", "SPR2681_4_no_cancellation_envelope"],
        "purpose": "imports finite source-prefactor residual rows",
    },
    {
        "source_id": "SRC2682_CDH1480",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv",
        "required_needles": ["CDH1480_2_target_forbidden", "COUNTEREXAMPLE_PROVED", "CDH1480_5_verdict"],
        "purpose": "imports Hom target-forbidden route and scalar counterexample",
    },
    {
        "source_id": "SRC2682_TNG1470",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv",
        "required_needles": ["TNG1470_3_no_extension", "TNG1470_4_radiative_limit", "NOT_PARENT_DERIVED_START_SOURCE_FILL"],
        "purpose": "imports typed grammar and no-extension clauses",
    },
    {
        "source_id": "SRC2682_MOMS1486",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv",
        "required_needles": ["MOMS1088_4_no_species_weights", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "MOMS1088_6_no_shadow_domain"],
        "purpose": "imports ordinary matter source-weight/no-shadow blockers",
    },
    {
        "source_id": "SRC2682_EVAL1449",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_evaluation_decision_1449.csv",
        "required_needles": ["DO_NOT_EVALUATE_OR_IMPORT_C_PARENT_WEP", "source-only", "countermodels"],
        "purpose": "keeps C_parent_WEP evaluation blocked",
    },
    {
        "source_id": "SRC2682_COUNTERMODELS2676",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/action_scale_measure_owner_countermodels_nonclaim_2676.csv",
        "required_needles": ["CM2676_0_species_action_weight", "CM2676_2_pre_variation_source_rescaling", "COUNTERMODEL_RETAINED_NONCLAIM"],
        "purpose": "imports w_A and c_A source-prefactor countermodels",
    },
    {
        "source_id": "SRC2682_NO_SOURCE_PREF1479",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
        "required_needles": ["NST1479_0_target", "NST1479_2_operator_domain", "NST1479_3_same_action_limit"],
        "purpose": "imports source-only prefactor typing theorem",
    },
    {
        "source_id": "SRC2682_CURRENT1453",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_4_post_variation_rescaling", "CSO1453_5_pre_variation_weight", "CSO1453_7_verdict"],
        "purpose": "imports post/pre-variation current split",
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


def normal_form_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NF2682_0_target",
            "claim_piece": "parent source-prefactor target normal form",
            "normal_form_statement": "Every ordinary coefficient target is classified as allowed, forbidden, or residual before WEP/R10/local-GR evaluation.",
            "classification": "TARGET_SHARPENED_NOT_PARENT_DERIVED",
            "current_evidence": "2681 selected this gate after coefficient-algebra exhaustion failed",
            "blocking_clauses": "normal-form owner; exhaustive target list; no source-prefactor target; no scalar/readout extension",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_NEXT_TARGET.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "classify source-prefactor target explicitly",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_1_allowed_targets",
            "claim_piece": "allowed ordinary coefficient targets",
            "normal_form_statement": "Allowed targets include quotient observables, fixed representation data, in-action gauge/current couplings, and common universal constants.",
            "classification": "ALLOWED_LIST_NOT_EXHAUSTIVE",
            "current_evidence": "2681 records this list as plausible but not exhaustive",
            "blocking_clauses": "no parent universal property proving no other coefficient target exists",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_ALGEBRA_EXHAUSTION_AUDIT.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "use allowed list as inventory, not proof",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_2_source_prefactor_target",
            "claim_piece": "Coeff_source-prefactor",
            "normal_form_statement": "Active source-prefactor target would host w_A, c_A, kappa_A and source-only scalar multipliers before variation.",
            "classification": "FORBIDDEN_TARGET_CANDIDATE_NOT_SIGNED",
            "current_evidence": "2681 target inventory keeps target absence not parent-signed",
            "blocking_clauses": "normal-form clause declaring this target absent is not derived from parent action/object language",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "retain finite coefficient rows for every source-prefactor occupant",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_3_scalar_extension",
            "claim_piece": "hidden scalar target extension",
            "normal_form_statement": "If nonconstant I_hid and Coeff_source-prefactor both exist, c(I_hid) O_source is a legal source coupling.",
            "classification": "COUNTEREXAMPLE_ACTIVE",
            "current_evidence": "CDH1480_3 and 2681 keep scalar obstruction active",
            "blocking_clauses": "hidden invariant algebra triviality or target absence not signed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "do not erase c(I_hid) without target absence or finite row",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_4_pre_action_weight",
            "claim_piece": "pre-action species weight",
            "normal_form_statement": "If S_matter already contains sum_A w_A S_A, the Hilbert source inherits w_A.",
            "classification": "PRE_ACTION_COUNTERMODEL_ACTIVE",
            "current_evidence": "2676 and 1479 keep same-action/current-owner routes insufficient",
            "blocking_clauses": "no-source-only target and action-line owner are unsigned",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/action_scale_measure_owner_countermodels_nonclaim_2676.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                ]
            ),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "retain Delta_w_AB as finite nonclaim row",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_5_post_current_rescale",
            "claim_piece": "post/pre-current c_A or kappa_A",
            "normal_form_statement": "Post-variation rescaling is conditionally harmless, but pre-variation/current-slot rescaling remains a source-prefactor occupant.",
            "classification": "SPLIT_CONDITIONAL_RETAIN_RESIDUAL",
            "current_evidence": "current-owner theorem kills post-variation only conditionally and keeps pre-action weights live",
            "blocking_clauses": "variation-before-readout, no source slot, source-worldtube and current owner not jointly signed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "split c_A into post-current conditional and pre-current residual rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_6_readout_tail",
            "claim_piece": "readout/radiative source-tail target",
            "normal_form_statement": "Observed effective/readout maps cannot enlarge coefficient domains only if no-extension and radiative/readout closure are signed.",
            "classification": "READOUT_EXTENSION_RESIDUAL_OPEN",
            "current_evidence": "1470 says no-extension/radiative closure is unsigned",
            "blocking_clauses": "readout kernels; source-worldtube; counterterms; no-spurion return",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "retain C_eff_source_tail row",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "NF2682_7_verdict",
            "claim_piece": "source-prefactor target absent",
            "normal_form_statement": "Coeff_source-prefactor is absent/forbidden in the parent normal form, or every occupant is retained as finite residual.",
            "classification": "TARGET_ABSENCE_NOT_DERIVED_RESIDUAL_BRANCH_ACTIVE",
            "current_evidence": "normal-form classification is written but not parent-signed",
            "blocking_clauses": "source-prefactor target absence; scalar obstruction; pre-action weights; readout tails",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_evaluation_decision_1449.csv")),
                ]
            ),
            "parent_signed": "false",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "next_action": "move to finite source-prefactor coefficient source pack",
            "timestamp_utc": stamp(),
        },
    ]


def target_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "TC2682_0_OQobs",
            "coefficient_target": "O(Q_obs)",
            "classification": "allowed_conditional",
            "normal_form_rule": "quotient-observable coefficients allowed if q_obs/coframe descent is parent-signed",
            "risk_if_unsigned": "does not prove source-prefactor target absent",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "retain as allowed inventory only",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_1_theta_rep",
            "coefficient_target": "theta_rep",
            "classification": "allowed_but_not_source_prefactor",
            "normal_form_rule": "fixed representation constants may enter matter terms but cannot be active gravitational source weights",
            "risk_if_unsigned": "source weights can be hidden inside material constants",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "keep fixed-constant owner separate",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_2_gauge_current",
            "coefficient_target": "gauge/current data inside L_A",
            "classification": "allowed_if_inside_action",
            "normal_form_rule": "ordinary gauge coupling is allowed inside L_A but does not authorize active gravitational source prefactors",
            "risk_if_unsigned": "gauge-current owner confused with Hilbert source owner",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "do not count gauge edge as source-prefactor proof",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_3_common_constant",
            "coefficient_target": "common End(A_ord) scalar",
            "classification": "allowed_common_only_if_line_owner_signed",
            "normal_form_rule": "common calibration constants may survive only after action-line owner and connectedness are signed",
            "risk_if_unsigned": "relative w_A imported as common mode without proof",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "do not promote common mode",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_4_source_prefactor",
            "coefficient_target": "Coeff_source-prefactor",
            "classification": "forbidden_candidate_retained_residual",
            "normal_form_rule": "must be absent by parent normal form; currently not signed, so retained as residual target",
            "risk_if_unsigned": "w_A, c_A, kappa_A and c(I_hid) source couplings remain legal",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "emit finite coefficient source pack",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_5_readout_tail",
            "coefficient_target": "C_eff_source_tail",
            "classification": "forbidden_candidate_retained_residual",
            "normal_form_rule": "readout/radiative maps must not extend coefficient domains; currently unsigned",
            "risk_if_unsigned": "bare parent grammar does not transfer to observed tests",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "retain readout-tail coefficient",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "TC2682_6_verdict",
            "coefficient_target": "target classification complete enough for claim",
            "classification": "classification_complete_nonclaim_only",
            "normal_form_rule": "classification table exists but target absence is not parent-signed",
            "risk_if_unsigned": "no local-GR/WEP source silence claim",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_COEFFICIENT_TARGET_INVENTORY_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "source finite residuals or derive target absence",
            "timestamp_utc": stamp(),
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FSP2682_0_cIhid",
            "symbol": "c(I_hid)",
            "coefficient_role": "hidden scalar source-prefactor",
            "normal_form_status": "RESIDUAL_TARGET_OPEN",
            "formula_or_bound_contract": "zero only if hidden invariant algebra triviality or Coeff_source-prefactor absence is parent-signed",
            "arena_links": "WEP;R10;clock;PPN;local-GR",
            "units": "dimensionless or declared source coefficient",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "supply theorem-zero or finite source value independent of WEP bound",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "FSP2682_1_Delta_w_AB",
            "symbol": "Delta_w_AB",
            "coefficient_role": "pre-action species/source weight",
            "normal_form_status": "RESIDUAL_TARGET_OPEN",
            "formula_or_bound_contract": "zero only if no source-prefactor target and action-line owner are parent-signed",
            "arena_links": "WEP;Newton-source;R10;local-GR",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/action_scale_measure_owner_countermodels_nonclaim_2676.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive target absence or fill source-backed Delta_w row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "FSP2682_2_cA_pre",
            "symbol": "c_A_pre or kappa_A",
            "coefficient_role": "pre-current/current-source normalization scalar",
            "normal_form_status": "RESIDUAL_TARGET_OPEN",
            "formula_or_bound_contract": "post-current c_A can be conditionally downstream, but pre-current c_A remains target-open",
            "arena_links": "WEP;PPN;clock;source-normalization",
            "units": "dimensionless current/source fraction",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "split pre/post current rows before scoring",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "FSP2682_3_Ceff_tail",
            "symbol": "C_eff_source_tail",
            "coefficient_role": "readout/radiative source-prefactor tail",
            "normal_form_status": "RESIDUAL_TARGET_OPEN",
            "formula_or_bound_contract": "zero only if no-extension/radiative closure is parent-signed",
            "arena_links": "EM;clock;R10;WEP",
            "units": "declared effective coefficient units",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive no-extension closure or source finite tail",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "FSP2682_4_total_envelope",
            "symbol": "epsilon_prefactor_total",
            "coefficient_role": "absolute no-cancellation source-prefactor envelope",
            "normal_form_status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "formula_or_bound_contract": "abs(epsilon_prefactor_total)>=abs(c(I_hid))+abs(Delta_w_AB)+abs(c_A_pre/kappa_A)+abs(C_eff_source_tail)",
            "arena_links": "all local source arenas",
            "units": "dimensionless/envelope after common source normalization",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only after every component is zero or source-backed",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "FSP2682_5_acquisition_template",
            "symbol": "K_pref * tau_arena * epsilon_prefactor_total",
            "coefficient_role": "future finite arena projection",
            "normal_form_status": "ACQUISITION_TEMPLATE_NONCLAIM",
            "formula_or_bound_contract": "requires K_pref, tau_arena, units, source path, sign convention and no-cancellation guard",
            "arena_links": "WEP;R10;PPN;clock;orbital",
            "units": "declared per arena",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv")),
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "build source pack only after normal-form theorem fails",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], class_rows: list[dict[str, Any]], finite_rows_: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2682_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "normal_form_audit",
                "parent_signed": row["parent_signed"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(path).exists() for path in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_NORMAL_FORM_NOT_PARENT_SIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in class_rows:
        rows.append(
            {
                "runner_id": f"RUN2682_{row['target_id']}",
                "target_id": row["target_id"],
                "stage": "target_classification",
                "parent_signed": row["parent_signed"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_CLASSIFICATION_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in finite_rows_:
        rows.append(
            {
                "runner_id": f"RUN2682_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "finite_coefficient_row",
                "parent_signed": row["parent_zero_available"],
                "has_numeric_bound": row["has_numeric_value"],
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_FINITE_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2682_0_classification_written",
            "claim": "coefficient targets are classified",
            "status": "PASS_NONCLAIM_CLASSIFICATION_ONLY",
            "blocking_rows": "TC2682_4_source_prefactor;TC2682_6_verdict",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2682_1_source_prefactor_absence",
            "claim": "Coeff_source-prefactor is absent/forbidden",
            "status": "FAIL_TARGET_ABSENCE_NOT_PARENT_SIGNED",
            "blocking_rows": "NF2682_2_source_prefactor_target;TC2682_4_source_prefactor",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2682_2_countermodels",
            "claim": "source-prefactor countermodels are eliminated",
            "status": "FAIL_COUNTERMODELS_ACTIVE",
            "blocking_rows": "NF2682_3_scalar_extension;NF2682_4_pre_action_weight;FSP2682_0_cIhid;FSP2682_1_Delta_w_AB",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2682_3_finite_rows",
            "claim": "finite source-prefactor rows can be scored",
            "status": "FAIL_MISSING_NUMERIC_OR_THEOREM_ZERO",
            "blocking_rows": "FSP2682_0_cIhid;FSP2682_1_Delta_w_AB;FSP2682_4_total_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2682_4_local_GR",
            "claim": "local GR/PPN can use normal form to silence source-prefactor couplings",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "NF2682_7_verdict;CG2682_1_source_prefactor_absence;CG2682_2_countermodels;CG2682_3_finite_rows",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2682_0_normal_form_attempt",
            "question": "Does 2682 parent-sign source-prefactor target absence?",
            "result": "not_yet",
            "reason": "classification is written, but the parent object language has not derived that Coeff_source-prefactor is absent",
            "action": "do not import Delta_w_AB=0 or source silence",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2682_1_actual_gain",
            "question": "What improved?",
            "result": "target classification complete as nonclaim",
            "reason": "the dangerous occupants c(I_hid), Delta_w_AB, c_A/kappa_A and C_eff_tail are now separated",
            "action": "use finite rows if theorem route fails",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2682_2_next_route",
            "question": "Best next target?",
            "result": "finite_source_prefactor_coefficient_source_pack",
            "reason": "target absence is not derived; the honest next move is source-pack criteria for finite coefficients while still allowing a later theorem-zero route",
            "action": "select 2683",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2682_0_selected",
            "kind": "selected",
            "target_doc": "2683-Y5-R2FR-finite-source-prefactor-coefficient-source-pack-or-theorem-zero-return.md",
            "target_script": "scripts/Y5_R2FR_finite_source_prefactor_coefficient_source_pack_or_theorem_zero_return_2683.py",
            "purpose": "build strict source-pack requirements for c(I_hid), Delta_w_AB, c_A/kappa_A and C_eff_tail while preserving a possible later theorem-zero route",
            "acceptance_gate": "each finite coefficient has units, source path, arena projection, sign convention, common normalizer and no-cancellation guard; no row can be score-ready from WEP-bound inversion",
            "forbidden_shortcuts": "claiming normal-form absence; deleting scalar/pre-action countermodels; using WEP bounds as theory values; importing Delta_w=0; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2682_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2682_1_progress",
            "field": "coupling_gap",
            "value": "source-prefactor target classified but not absent",
            "status": "sharpened_not_claimed",
            "note": "the honest branch is now finite source-prefactor coefficients unless a later theorem-zero closes the target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2682_0_normal_form",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["normal_form_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_normal_form"]),
            "contents": "source-prefactor target normal-form audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2682_1_classification",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["target_classification"]),
            "destination": str(BRANCH_OUTPUTS["microscope_classification"]),
            "contents": "coefficient target classification retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2682_2_finite",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["finite_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_finite"]),
            "contents": "finite source-prefactor coefficient rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2682_3_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["finite_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight finite prefactor rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2682_4_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["finite_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local finite prefactor rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_sources_exist_and_needles_found", "passed": as_bool(source_ok), "details": "all cited source paths exist and required needles are present"})

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_nonclaim_guard", "passed": as_bool(all_nonclaim), "details": "all generated rows carry valid_for_claim=false"})

    verdict_blocks = any(row["audit_id"] == "NF2682_7_verdict" and row["classification"] == "TARGET_ABSENCE_NOT_DERIVED_RESIDUAL_BRANCH_ACTIVE" for row in rows["normal_form_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_verdict_blocks_claim", "passed": as_bool(verdict_blocks), "details": "source-prefactor target absence is not promoted"})

    source_pref_open = any(row["target_id"] == "TC2682_4_source_prefactor" and row["classification"] == "forbidden_candidate_retained_residual" for row in rows["target_classification"])
    class_complete = any(row["target_id"] == "TC2682_6_verdict" and row["classification"] == "classification_complete_nonclaim_only" for row in rows["target_classification"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_classification_complete_nonclaim", "passed": as_bool(source_pref_open and class_complete), "details": "target classification exists but remains nonclaim"})

    countermodels = any(row["audit_id"] == "NF2682_3_scalar_extension" and row["classification"] == "COUNTEREXAMPLE_ACTIVE" for row in rows["normal_form_audit"]) and any(row["audit_id"] == "NF2682_4_pre_action_weight" and row["classification"] == "PRE_ACTION_COUNTERMODEL_ACTIVE" for row in rows["normal_form_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_countermodels_retained", "passed": as_bool(countermodels), "details": "scalar and pre-action source-weight countermodels remain active"})

    finite_ids = {row["row_id"] for row in rows["finite_rows"]}
    finite_complete = {"FSP2682_0_cIhid", "FSP2682_1_Delta_w_AB", "FSP2682_2_cA_pre", "FSP2682_4_total_envelope"}.issubset(finite_ids)
    finite_nonclaim = all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in rows["finite_rows"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_finite_rows_complete_nonclaim", "passed": as_bool(finite_complete and finite_nonclaim), "details": "finite source-prefactor rows exist and remain nonclaim"})

    gates_ok = any(row["gate_id"] == "CG2682_4_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and any(row["gate_id"] == "CG2682_1_source_prefactor_absence" and row["status"] == "FAIL_TARGET_ABSENCE_NOT_PARENT_SIGNED" for row in rows["claim_gates"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_claim_gates_correct", "passed": as_bool(gates_ok), "details": "local-GR remains blocked and target-absence gate fails"})

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_runner_refuses_unsigned_rows", "passed": as_bool(runner_refuses), "details": "runner refuses scoring without parent zero or numeric residuals"})

    next_selected = any(row["target_id"] == "NEXT2682_0_selected" and "2683-Y5-R2FR-finite-source-prefactor-coefficient-source-pack-or-theorem-zero-return.md" in row["target_doc"] for row in rows["next_target"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_next_target_selected", "passed": as_bool(next_selected), "details": "next target selects finite source-prefactor coefficient source pack"})

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_csv_parse", "passed": as_bool(csv_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))})

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_branch_copies_parse", "passed": as_bool(branch_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse))})

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_formalization_write_guard", "passed": as_bool(formalization_guard), "details": "generated path allowlist excludes formalization-workbench"})

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_pycache_absent_at_validation_time", "passed": as_bool(pycache_absent), "details": "scripts/__pycache__ absent when validation rows were produced"})

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2682_pycache_absent_at_validation_time")
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2682_OVERALL", "passed": as_bool(overall), "details": "2682 classifies source-prefactor targets, refuses target-absence promotion, and stages finite coefficient rows"})
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} - Parent Source-Prefactor Target Normal Form Or Finite Coefficient Row",
        "",
        "## Private Verdict",
        "",
        "2682 writes the normal-form gate we needed: coefficient targets are now classified as allowed, forbidden-candidate, or residual. The dangerous target is `Coeff_source-prefactor`, the slot that would host `w_A`, `c_A`, `kappa_A`, and hidden scalar source multipliers.",
        "",
        "Current verdict: not absent yet. The classification is useful, but the parent object language has not derived that `Coeff_source-prefactor` is missing from the theory. Therefore the scalar counterexample, pre-action species weight, current/source rescaling, and readout-tail channels remain explicit finite nonclaim rows.",
        "",
        "No WEP, R10, PPN, clock, orbital, Newton, or local-GR source-silence claim is made. The next honest route is a finite source-prefactor source pack, while leaving a future theorem-zero return route open.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Source-Prefactor Target Normal-Form Audit",
        "",
        markdown_table(rows["normal_form_audit"]),
        "",
        "## Coefficient Target Classification",
        "",
        markdown_table(rows["target_classification"]),
        "",
        "## Finite Source-Prefactor Coefficient Rows",
        "",
        markdown_table(rows["finite_rows"]),
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
    rows["normal_form_audit"] = normal_form_audit_rows()
    rows["target_classification"] = target_classification_rows()
    rows["finite_rows"] = finite_rows()
    rows["runner_results"] = runner_results_rows(rows["normal_form_audit"], rows["target_classification"], rows["finite_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "normal_form_audit",
        "target_classification",
        "finite_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_normal_form"], rows["normal_form_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_classification"], rows["target_classification"])
    write_csv(BRANCH_OUTPUTS["microscope_finite"], rows["finite_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["finite_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["finite_rows"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
