from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1218"
TITLE = "1218-Y5-R10-parent-alpha-surface-operator-owner-or-coefficient-prior-source"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OPERATOR_OWNER_PATH = OUT_DIR / f"{PACK_ID}_ALPHA_SURFACE_OPERATOR_OWNER_AUDIT.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_ZERO_THEOREM_PACK.csv"
PRIOR_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_PRIOR_SOURCE_LEDGER.csv"
COUNTEREXAMPLE_PATH = OUT_DIR / f"{PACK_ID}_COUNTEREXAMPLE_RETENTION_LEDGER.csv"
THRESHOLD_CARRY_PATH = OUT_DIR / f"{PACK_ID}_THRESHOLD_CARRY_FORWARD_NONCLAIM.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_COUPLING_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1218_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def is_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return value is False
    return str(value).strip().lower() == "false"


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1218_0_1217_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1217_NEXT_TARGET.csv",
            "needle": "1218-Y5-R10-parent-alpha-surface-operator-owner-or-coefficient-prior-source.md",
            "purpose": "1217 handoff to parent alpha/surface owner target",
        },
        {
            "source_id": "SRC1218_1_1217_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1217_CPARENT_MAP_ATTEMPT.csv",
            "needle": "CMAP1217_5_verdict",
            "purpose": "C_parent map not derived",
        },
        {
            "source_id": "SRC1218_2_1217_prior",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1217_FINITE_COEFFICIENT_PRIOR_CONTRACT.csv",
            "needle": "CPRIOR1217_0_alpha",
            "purpose": "threshold-bounded prior contract",
        },
        {
            "source_id": "SRC1218_3_1099_EM_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "UEM1099_3_verdict",
            "purpose": "unique EM kinetic owner theorem attempt",
        },
        {
            "source_id": "SRC1218_4_1099_counterterm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
            "needle": "EXC1099_5_radiative",
            "purpose": "no-extra-F2 and radiative counterterm audit",
        },
        {
            "source_id": "SRC1218_5_1099_alpha_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
            "needle": "ASR1099_3_DD_alpha_threshold",
            "purpose": "alpha coefficient source rows remain nonclaim",
        },
        {
            "source_id": "SRC1218_6_1100_TQ",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
            "needle": "TQT1100_4_verdict",
            "purpose": "T_Q/gauge-norm route verdict",
        },
        {
            "source_id": "SRC1218_7_1100_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "needle": "TQS1100_6_verdict",
            "purpose": "gauge norm signature clauses",
        },
        {
            "source_id": "SRC1218_8_1100_acquisition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_REQUIRED_SOURCE_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1100_2_norm",
            "purpose": "required alpha/gauge source acquisition rows",
        },
        {
            "source_id": "SRC1218_9_1101_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
            "needle": "GFT1101_4_verdict",
            "purpose": "gauge norm owner not derived",
        },
        {
            "source_id": "SRC1218_10_1101_candidates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv",
            "needle": "GNO1101_6_unification_embedding",
            "purpose": "candidate alpha owner routes",
        },
        {
            "source_id": "SRC1218_11_1101_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv",
            "needle": "ROUTE1101_2_finite_alpha_products",
            "purpose": "finite alpha route discipline",
        },
        {
            "source_id": "SRC1218_12_1108_F2",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1108_EM_F2_IMAGE_THEOREM_ATTEMPT.csv",
            "needle": "EMF1108_6_verdict",
            "purpose": "EM F2 image exhaustion not derived",
        },
        {
            "source_id": "SRC1218_13_1108_acquisition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1108_EM_ALPHA_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1108_5_external_alpha_coefficient",
            "purpose": "alpha coefficient source acquisition row",
        },
        {
            "source_id": "SRC1218_14_1088_MOMS",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_7_verdict",
            "purpose": "ordinary matter signature not derived",
        },
        {
            "source_id": "SRC1218_15_1088_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
            "needle": "THM1088_6_current_corpus_verdict",
            "purpose": "conditional matter zero theorem not promoted",
        },
        {
            "source_id": "SRC1218_16_1089_coverage",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv",
            "needle": "MOMS1088_7_all_in_one",
            "purpose": "no single source signs all ordinary matter clauses",
        },
        {
            "source_id": "SRC1218_17_1087_coeff_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv",
            "needle": "DDSP1087_1_c_surface",
            "purpose": "surface coefficient source requirement",
        },
        {
            "source_id": "SRC1218_18_1098_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_1_c_surface",
            "purpose": "source-backed coefficient requirements",
        },
        {
            "source_id": "SRC1218_19_1114_no_hom",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "purpose": "no hidden-visible coefficient morphism attempt",
        },
        {
            "source_id": "SRC1218_20_1114_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1114_3_radiative",
            "purpose": "coupling obstruction ledger",
        },
        {
            "source_id": "SRC1218_21_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LIA1115_6_verdict",
            "purpose": "local invariant algebra not derived",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    prior_1217 = read_csv(OUT_DIR / "P8_Y5_R10_1217_FINITE_COEFFICIENT_PRIOR_CONTRACT.csv")
    alpha_prior = find_row(prior_1217, "prior_id", "CPRIOR1217_0_alpha")
    surface_prior = find_row(prior_1217, "prior_id", "CPRIOR1217_1_surface")
    common_prior = find_row(prior_1217, "prior_id", "CPRIOR1217_2_common_abs")
    tail_prior = find_row(prior_1217, "prior_id", "CPRIOR1217_3_tail")

    operator_rows = [
        {
            "owner_id": "OWNER1218_0_alpha_EM_F2_image",
            "coefficient": "c_alpha_DD / b_alpha",
            "candidate_owner": "parent EM-F2 image exhaustion",
            "operator_statement": "Z_Q = C_P <T_Q,T_Q>_P and every visible F_Q^2 coefficient descends from this parent image",
            "needed_to_close": "T_Q parent object; fixed norm/level; no lambda_A F_Q^2; no f(I_hid)F_Q^2; radiative/readout closure",
            "current_status": "NOT_DERIVED",
            "best_evidence": "EMF1108_6_verdict and TQS1100_6_verdict",
            "claim_effect": "alpha coefficient remains finite/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_1_alpha_current_Ward_limit",
            "coefficient": "c_alpha_DD / beta_source_alpha",
            "candidate_owner": "Ward/Noether current normalization",
            "operator_statement": "J_Q is conserved and owned by T_Q",
            "needed_to_close": "fixed kinetic norm or level tying J_Q normalization to F_Q^2 plus no-extra-F2",
            "current_status": "CURRENT_OWNER_SUPPORT_NOT_KINETIC_OWNER",
            "best_evidence": "GFT1101_2_Ward_limit and GNO1101_4_Ward_identity",
            "claim_effect": "current route cannot by itself fix alpha or WEP coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_2_alpha_counterterm_obstruction",
            "coefficient": "c_alpha_DD / b_alpha",
            "candidate_owner": "no hidden-visible coefficient morphism",
            "operator_statement": "f(I_hid)F_Q^2 and lambda_A F_Q^2 are absent or forbidden",
            "needed_to_close": "typed/product-category parent grammar, invariant-algebra triviality, no-extension rule, and radiative/readout closure",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "best_evidence": "UEM1099_2_counterterm; NHV1114_6_verdict; LIA1115_6_verdict",
            "claim_effect": "alpha theorem-zero cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_3_surface_binding_superselection",
            "coefficient": "c_surface_DD",
            "candidate_owner": "ordinary-matter constant/surface-binding superselection",
            "operator_statement": "surface/binding constants theta_A are fixed representation/superselection data with Lie_v theta_A=0",
            "needed_to_close": "single parent ordinary-matter action signature; fixed nuclear/binding constants; no hidden coefficient arguments; readout closure",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "best_evidence": "MOMS1088_3_constant_superselection; THM1088_3_constants; MOMS1088_7_all_in_one",
            "claim_effect": "surface coefficient remains finite/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_4_surface_hidden_coefficient_obstruction",
            "coefficient": "c_surface_DD",
            "candidate_owner": "no hidden coefficient map into binding/surface sector",
            "operator_statement": "a_surface(I_hid) or binding-energy coefficient maps are not well-typed or are constant",
            "needed_to_close": "typed visible coefficient functor or local invariant algebra triviality",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "best_evidence": "NHV1114_4_scalar_obstruction and LIA1115_3_continuous_scalar_obstruction",
            "claim_effect": "binding/surface coefficient cannot be zero-claimed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_5_tail_basis",
            "coefficient": "q_tail(A)",
            "candidate_owner": "complete material response basis",
            "operator_statement": "alpha/surface DD rows span all composition response or the residual tail has a sourced envelope",
            "needed_to_close": "basis completeness theorem or empirical all-material tail envelope",
            "current_status": "NOT_DERIVED",
            "best_evidence": "DDSP1087_2_q_tail and CPRIOR1217_3_tail",
            "claim_effect": "tail remains a separate coefficient debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWNER1218_6_verdict",
            "coefficient": "C_parent -> c_alpha,c_surface,q_tail",
            "candidate_owner": "parent-owned alpha/surface material-response operator set",
            "operator_statement": "both alpha and surface operators are parent-owned, hidden-silent, and same-branch normalized",
            "needed_to_close": "OWNER1218_0 through OWNER1218_5 promoted, plus same-branch range/profile/readout packet",
            "current_status": "PARENT_ALPHA_SURFACE_OPERATOR_OWNER_NOT_DERIVED",
            "best_evidence": "1218 audit",
            "claim_effect": "continue finite nonclaim route; no WEP/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_rows = [
        {
            "theorem_id": "THM1218_0_alpha_zero_conditional",
            "statement": "If EM-F2 image exhaustion, no independent visible/hidden F2 coefficient, fixed T_Q norm/level, and radiative/readout closure all hold, then c_alpha_DD=b_alpha=0.",
            "proof_status": "EXACT_CONDITIONAL_RESTATED",
            "missing_for_promotion": "T_Q/norm/no-extra-F2/no-hidden-f/readout clauses are not all signed",
            "consequence_if_signed": "alpha clock/WEP/R10 coefficient can be demoted to theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1218_1_surface_zero_conditional",
            "statement": "If the ordinary-matter action has fixed representation/superselection constants and no hidden-visible coefficient morphisms, then c_surface_DD=0 for the local vertical direction.",
            "proof_status": "EXACT_CONDITIONAL_RESTATED",
            "missing_for_promotion": "single parent matter signature, typed coefficient grammar, invariant-algebra triviality, and readout closure",
            "consequence_if_signed": "surface/binding WEP coefficient can be demoted to theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1218_2_tail_zero_conditional",
            "statement": "If visible material response functors exhaust the parent basis and hidden/local invariants are trivial or typed out, then q_tail(A)=0.",
            "proof_status": "CONDITIONAL_NOT_COMPLETE",
            "missing_for_promotion": "basis completeness and no-extension/no-marker theorem",
            "consequence_if_signed": "two-channel DD basis becomes enough for this local WEP audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1218_3_combined_Cparent_zero_conditional",
            "statement": "If THM1218_0 through THM1218_2 hold in one same-branch packet, then C_parent has no local composition channel in WEP.",
            "proof_status": "COMBINED_CONDITIONAL_ONLY",
            "missing_for_promotion": "each channel theorem plus same-branch normalization and readout/profile closure",
            "consequence_if_signed": "local WEP coefficient branch would become a derived zero rather than a finite prior branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    prior_source_rows = [
        {
            "prior_source_id": "PSRC1218_0_alpha_parent",
            "coefficient": "c_alpha_DD / b_alpha",
            "candidate_source_type": "parent derivation",
            "needed_evidence": "signed EM-F2 image exhaustion or no-extra-F2 theorem-zero",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": "alpha owner theorem is conditional and counterterms remain legal",
            "threshold_abs": alpha_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_source_id": "PSRC1218_1_alpha_external",
            "coefficient": "c_alpha_DD / b_alpha",
            "candidate_source_type": "external/source-backed coefficient prior",
            "needed_evidence": "numeric alpha coefficient value independent of the target WEP threshold, with units, branch, projection, and provenance",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": "WEP threshold is a bound, not a theory coefficient prior",
            "threshold_abs": alpha_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_source_id": "PSRC1218_2_surface_parent",
            "coefficient": "c_surface_DD",
            "candidate_source_type": "parent derivation",
            "needed_evidence": "ordinary-matter binding/surface operator owner plus no hidden coefficient argument",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": "MOMS/constant superselection is conditional, not parent-derived",
            "threshold_abs": surface_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_source_id": "PSRC1218_3_surface_external",
            "coefficient": "c_surface_DD",
            "candidate_source_type": "external/source-backed coefficient prior",
            "needed_evidence": "numeric surface/binding coefficient value independent of the target WEP threshold, with units and provenance",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": "no source-backed surface coefficient exists in current corpus",
            "threshold_abs": surface_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_source_id": "PSRC1218_4_common_vector_norm",
            "coefficient": "C_parent vector norm",
            "candidate_source_type": "same-branch parent/vector prior",
            "needed_evidence": "one branch fixes vector norm and channel weights before seeing the material pair",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": "common threshold is a diagnostic scale, not a coefficient-vector theorem",
            "threshold_abs": common_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_source_id": "PSRC1218_5_tail_envelope",
            "coefficient": "q_tail(A)",
            "candidate_source_type": "basis-completeness theorem or empirical envelope",
            "needed_evidence": "all-material residual basis coverage or sourced tail bound",
            "current_status": "NOT_ACQUIRED",
            "why_not_claim": tail_prior["value"],
            "threshold_abs": tail_prior["allowed_abs_threshold_from_1216"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexample_rows = [
        {
            "counterexample_id": "CX1218_0_lambda_A",
            "operator_or_map": "lambda_A F_Q^2",
            "blocks": "alpha owner theorem",
            "retention_reason": "constant visible F2 counterterm remains legal unless operator-domain exhaustion is derived",
            "repair_route": "derive unique EM-F2 image exhaustion or no-extra-F2 theorem",
            "status": "RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CX1218_1_hidden_F2",
            "operator_or_map": "f(I_hid) F_Q^2",
            "blocks": "alpha hidden-silence theorem",
            "retention_reason": "surviving hidden invariant scalar can feed continuous visible coefficient",
            "repair_route": "typed/product-category no-hidden-visible theorem plus invariant algebra triviality",
            "status": "RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CX1218_2_binding_coefficient",
            "operator_or_map": "a_surface(I_hid) or binding coefficient c(I_hid)",
            "blocks": "surface/binding coefficient zero",
            "retention_reason": "continuous hidden scalar coefficient maps are not typed out by current corpus",
            "repair_route": "parent matter coefficient functor with no hidden argument slots",
            "status": "RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CX1218_3_readout_radiative",
            "operator_or_map": "effective/readout coefficient after reduction",
            "blocks": "bare-action zero to observable zero transfer",
            "retention_reason": "radiative/readout closure remains unsigned for EM and matter constants",
            "repair_route": "renormalized/readout functor closure",
            "status": "RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    threshold_rows = [
        {
            "threshold_id": "TCF1218_0_alpha",
            "coefficient": alpha_prior["coefficient"],
            "threshold_abs": alpha_prior["allowed_abs_threshold_from_1216"],
            "source_row": "CPRIOR1217_0_alpha",
            "use_allowed": "private nonclaim scale discipline only",
            "promotion_rule": alpha_prior["promotion_rule"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "threshold_id": "TCF1218_1_surface",
            "coefficient": surface_prior["coefficient"],
            "threshold_abs": surface_prior["allowed_abs_threshold_from_1216"],
            "source_row": "CPRIOR1217_1_surface",
            "use_allowed": "private nonclaim scale discipline only",
            "promotion_rule": surface_prior["promotion_rule"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "threshold_id": "TCF1218_2_common_abs",
            "coefficient": common_prior["coefficient"],
            "threshold_abs": common_prior["allowed_abs_threshold_from_1216"],
            "source_row": "CPRIOR1217_2_common_abs",
            "use_allowed": "diagnostic only; not a vector-norm prediction",
            "promotion_rule": common_prior["promotion_rule"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "FEED1218_0_to_CMAP1217_1",
            "target_row": "CMAP1217_1_alpha_operator_owner",
            "update": "alpha operator owner remains not derived; exact missing clauses listed",
            "source_rows": "OWNER1218_0_alpha_EM_F2_image;OWNER1218_2_alpha_counterterm_obstruction",
            "current_status": "ALPHA_OWNER_BLOCKED_BY_F2_IMAGE_AND_COUNTERTERM_GATES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1218_1_to_CMAP1217_2",
            "target_row": "CMAP1217_2_surface_operator_owner",
            "update": "surface/binding operator owner remains not derived; exact missing clauses listed",
            "source_rows": "OWNER1218_3_surface_binding_superselection;OWNER1218_4_surface_hidden_coefficient_obstruction",
            "current_status": "SURFACE_OWNER_BLOCKED_BY_MATTER_SIGNATURE_AND_HIDDEN_COEFFICIENT_GATES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1218_2_to_CPRIOR1217",
            "target_row": "CPRIOR1217_0_alpha;CPRIOR1217_1_surface;CPRIOR1217_3_tail",
            "update": "no source-backed coefficient prior acquired; threshold rows remain nonclaim",
            "source_rows": "PSRC1218_0_alpha_parent;PSRC1218_3_surface_external;PSRC1218_5_tail_envelope",
            "current_status": "COEFFICIENT_PRIOR_SOURCE_NOT_ACQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1218_0_operator_owner_stub",
            "valid_operator_owner_rows": 0,
            "valid_coefficient_prior_rows": 0,
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject WEP/local-GR product; retain exact conditional theorems and finite nonclaim thresholds",
            "reason": "alpha owner, surface owner, tail basis, and source-backed coefficient prior are all unclosed",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1218_0_operator_owner",
            "decision": "do not promote alpha or surface operator owners",
            "because": "every viable route is still conditional or has a retained counterexample",
            "next_action": "derive the typed visible coefficient functor/no-hidden-argument rule or keep finite rows explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1218_1_prior_source",
            "decision": "reject threshold-as-prior promotion",
            "because": "bounds constrain possible coefficients but do not source a theory coefficient value",
            "next_action": "only promote source-backed coefficient priors if independent provenance exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1218_2_best_route",
            "decision": "next attack should target typed coefficient grammar",
            "because": "one grammar/no-hidden-visible theorem can kill alpha, surface, clock, WEP, and source-weight leaks together",
            "next_action": "try to derive or explicitly demote the typed visible coefficient functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1218_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1218 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1218_1_alpha_owner",
            "gate": "parent-owned alpha operator",
            "status": "BLOCKED",
            "reason": "EM-F2 image exhaustion, no-extra-F2, hidden-f, and readout/radiative closure are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1218_2_surface_owner",
            "gate": "parent-owned surface/binding operator",
            "status": "BLOCKED",
            "reason": "ordinary-matter signature and no hidden coefficient argument are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1218_3_tail_basis",
            "gate": "complete material response basis or tail envelope",
            "status": "BLOCKED",
            "reason": "q_tail(A) basis/envelope remains missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1218_4_prior_source",
            "gate": "source-backed finite coefficient prior",
            "status": "BLOCKED",
            "reason": "no independent coefficient value/source was acquired; thresholds remain bounds only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1218_5_product",
            "gate": "claim-valid WEP/local-GR product",
            "status": "BLOCKED",
            "reason": "valid_operator_owner_rows=0 and valid_prediction_rows=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1218_0_1219",
            "target_file": "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md",
            "target_script": "scripts/Y5_R10_typed_visible_coefficient_functor_or_hidden_scalar_counterexample_lock.py",
            "task": "try to derive the typed visible coefficient functor/no-hidden-argument rule that would kill alpha, surface, clock, WEP, and source-weight coefficient maps; if it fails, lock the hidden-scalar counterexample as an explicit finite-coupling closure debt",
            "success_condition": "visible coefficient functors are parent-typed to exclude hidden/local scalar arguments, or all finite coupling rows explicitly carry the retained hidden-scalar counterexample",
            "do_not_do": "do not infer no-coupling from covariance alone; do not promote threshold bounds to theory priors; do not claim WEP/local-GR/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    owner_fields = ["owner_id", "coefficient", "candidate_owner", "operator_statement", "needed_to_close", "current_status", "best_evidence", "claim_effect", "valid_for_claim", "claim_allowed"]
    theorem_fields = ["theorem_id", "statement", "proof_status", "missing_for_promotion", "consequence_if_signed", "valid_for_claim", "claim_allowed"]
    prior_source_fields = ["prior_source_id", "coefficient", "candidate_source_type", "needed_evidence", "current_status", "why_not_claim", "threshold_abs", "valid_for_claim", "claim_allowed"]
    counterexample_fields = ["counterexample_id", "operator_or_map", "blocks", "retention_reason", "repair_route", "status", "valid_for_claim", "claim_allowed"]
    threshold_fields = ["threshold_id", "coefficient", "threshold_abs", "source_row", "use_allowed", "promotion_rule", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "update", "source_rows", "current_status", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "valid_operator_owner_rows", "valid_coefficient_prior_rows", "valid_prediction_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(OPERATOR_OWNER_PATH, operator_rows, owner_fields)
    write_csv(CONDITIONAL_THEOREM_PATH, theorem_rows, theorem_fields)
    write_csv(PRIOR_SOURCE_PATH, prior_source_rows, prior_source_fields)
    write_csv(COUNTEREXAMPLE_PATH, counterexample_rows, counterexample_fields)
    write_csv(THRESHOLD_CARRY_PATH, threshold_rows, threshold_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        OPERATOR_OWNER_PATH,
        CONDITIONAL_THEOREM_PATH,
        PRIOR_SOURCE_PATH,
        COUNTEREXAMPLE_PATH,
        THRESHOLD_CARRY_PATH,
        FEED_PATH,
        RUNNER_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = read_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    alpha_owner_blocked = any(row["owner_id"] == "OWNER1218_0_alpha_EM_F2_image" and row["current_status"] == "NOT_DERIVED" for row in operator_rows)
    surface_owner_blocked = any(row["owner_id"] == "OWNER1218_3_surface_binding_superselection" and row["current_status"] == "CONDITIONAL_NOT_PARENT_DERIVED" for row in operator_rows)
    combined_not_derived = any(row["owner_id"] == "OWNER1218_6_verdict" and row["current_status"] == "PARENT_ALPHA_SURFACE_OPERATOR_OWNER_NOT_DERIVED" for row in operator_rows)
    counterexamples_retained = all(row["status"] == "RETAINED" for row in counterexample_rows)
    no_prior_acquired = all(row["current_status"] == "NOT_ACQUIRED" for row in prior_source_rows)
    threshold_rows_positive = all(float(row["threshold_abs"]) > 0 for row in threshold_rows)
    threshold_not_promoted = all("nonclaim" in row["use_allowed"].lower() or "diagnostic" in row["use_allowed"].lower() for row in threshold_rows)
    missing_rows_nonclaim = all(not (has_missing(row) and not is_false(row, "valid_for_claim")) for row in prior_source_rows + feed_rows)
    runner_refuses = runner_rows[0]["valid_operator_owner_rows"] == 0 and runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    claim_locks_blocked = all(
        any(row["gate_id"] == gate_id and row["status"] == "BLOCKED" for row in claim_gates)
        for gate_id in ["GATE1218_1_alpha_owner", "GATE1218_2_surface_owner", "GATE1218_3_tail_basis", "GATE1218_4_prior_source", "GATE1218_5_product"]
    )
    no_claim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for row in operator_rows + theorem_rows + prior_source_rows + counterexample_rows + threshold_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1219 = next_rows[0]["target_file"].startswith("1219-")

    validation_rows = [
        validation_row("VAL1218_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1218_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1218_2_alpha_owner_blocked", "alpha operator owner remains unproved", alpha_owner_blocked, "OWNER1218_0_alpha_EM_F2_image=NOT_DERIVED"),
        validation_row("VAL1218_3_surface_owner_blocked", "surface operator owner remains unproved", surface_owner_blocked, "OWNER1218_3_surface_binding_superselection=CONDITIONAL_NOT_PARENT_DERIVED"),
        validation_row("VAL1218_4_combined_not_derived", "combined operator owner not overclaimed", combined_not_derived, "OWNER1218_6_verdict=PARENT_ALPHA_SURFACE_OPERATOR_OWNER_NOT_DERIVED"),
        validation_row("VAL1218_5_counterexamples_retained", "live counterexamples are retained", counterexamples_retained, "; ".join(row["counterexample_id"] for row in counterexample_rows)),
        validation_row("VAL1218_6_no_prior_acquired", "no coefficient prior is falsely acquired", no_prior_acquired, "all prior-source rows current_status=NOT_ACQUIRED"),
        validation_row("VAL1218_7_thresholds_positive", "carried thresholds are positive", threshold_rows_positive, "; ".join(f"{row['threshold_id']}={row['threshold_abs']}" for row in threshold_rows)),
        validation_row("VAL1218_8_threshold_not_promoted", "thresholds remain nonclaim", threshold_not_promoted, "thresholds are scale discipline only"),
        validation_row("VAL1218_9_missing_rows_nonclaim", "no MISSING row is valid for claim", missing_rows_nonclaim, "missing source/prior/feed values are quarantined"),
        validation_row("VAL1218_10_runner_refuses", "runner stub refuses missing full product", runner_refuses, "valid_operator_owner_rows=0 and valid_prediction_rows=0"),
        validation_row("VAL1218_11_claim_locks_blocked", "claim locks remain blocked", claim_locks_blocked, "alpha, surface, tail, prior, and product gates blocked"),
        validation_row("VAL1218_12_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1218_13_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1218_14_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1218_15_next_target", "next target is staged", next_1219, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1218_16_overall",
            "overall 1218 validation",
            validation_pass,
            "1218 alpha/surface operator-owner pack is reproducible, nonclaim, and claim-locked" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1218 Y5/R10 Parent Alpha Surface Operator Owner Or Coefficient Prior Source

**Current verdict:** 1218 does **not** identify a parent-owned alpha/surface material-response operator and does **not** acquire a source-backed coefficient prior. The coupling branch remains finite, explicit, and nonclaim.

**Main progress:** the missing coupling is now split into four exact debts: EM-F2 image exhaustion for alpha, ordinary-matter constant/surface-binding superselection for the surface channel, material-basis/tail closure, and a typed no-hidden-visible coefficient rule. Threshold rows remain useful scale discipline, not theory priors.

**Best next attack:** derive the typed visible coefficient functor/no-hidden-argument rule. That is the cleanest route because it would hit alpha, surface/binding, clock constants, WEP material coefficients, and source weights with one structural theorem.

## Source Register

{markdown_table(source_rows, source_fields)}

## Alpha/Surface Operator Owner Audit

{markdown_table(operator_rows, owner_fields)}

## Conditional Zero Theorem Pack

{markdown_table(theorem_rows, theorem_fields)}

## Coefficient Prior Source Ledger

{markdown_table(prior_source_rows, prior_source_fields)}

## Counterexample Retention Ledger

{markdown_table(counterexample_rows, counterexample_fields)}

## Threshold Carry-Forward Nonclaim

{markdown_table(threshold_rows, threshold_fields)}

## Coupling Feed Update

{markdown_table(feed_rows, feed_fields)}

## Product Runner Stub

{markdown_table(runner_rows, runner_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("parent_alpha_surface_operator_owner_derived=false")
    print("source_backed_coefficient_prior_acquired=false")
    print("valid_prediction_rows=0")


if __name__ == "__main__":
    main()
