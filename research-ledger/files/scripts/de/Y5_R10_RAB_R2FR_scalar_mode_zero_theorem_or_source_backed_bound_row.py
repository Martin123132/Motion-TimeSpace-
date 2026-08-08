from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1341"
TITLE = "1341-Y5-R10-RAB-R2FR-scalar-mode-zero-theorem-or-source-backed-bound-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
WEB_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_WEB_SOURCE_LEDGER.csv"
ZERO_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_R2FR_ZERO_THEOREM_ATTEMPT.csv"
SCALAR_MAP_PATH = OUT_DIR / f"{PACK_ID}_SCALAR_MODE_MAP_CONTRACT.csv"
BOUND_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_BACKED_BOUND_ROWS_NONCLAIM.csv"
PREDICTION_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_MTS_R2FR_PREDICTION_TEMPLATE.csv"
RUNNER_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_R2FR_BOUND_RUNNER_DRYRUN.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1341_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1341*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def missing_markers(row: dict[str, object], fields: list[str]) -> list[str]:
    missing = []
    for field in fields:
        value = str(row.get(field, "")).strip()
        if value == "" or value.startswith("MISSING") or value in {"TBD", "PLACEHOLDER"}:
            missing.append(field)
    return missing


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1341_0_1340_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1340_NEXT_TARGET.csv",
            "needle": "NEXT1340_0_1341",
            "role": "selected 1341 target",
        },
        {
            "source_id": "SRC1341_1_1340_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1340_R11_EXECUTABLE_INPUT_SCHEMA.csv",
            "needle": "R11SCHEMA1340_1_R2FR",
            "role": "R2/fR executable schema",
        },
        {
            "source_id": "SRC1341_2_1340_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1340_R11_EXECUTABLE_INPUT_TEMPLATE.csv",
            "needle": "R11IN1340_0_R2FR_prediction_required",
            "role": "R2/fR prediction template",
        },
        {
            "source_id": "SRC1341_3_1340_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1340_VALIDATION.csv",
            "needle": "VAL1340_11_overall",
            "role": "1340 pass gate",
        },
        {
            "source_id": "SRC1341_4_960_zero_attempt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
            "needle": "R2FR960_4_verdict",
            "role": "R2/fR zero-or-bound attempt",
        },
        {
            "source_id": "SRC1341_5_963_derivative_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
            "needle": "DO963_6_verdict",
            "role": "derivative-order audit",
        },
        {
            "source_id": "SRC1341_6_963_runner_spec",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
            "needle": "R2RUN963_4_decision_logic",
            "role": "R2/fR runner spec",
        },
        {
            "source_id": "SRC1341_7_964_minimality",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            "needle": "MIN964_5_verdict",
            "role": "minimality theorem attempt",
        },
        {
            "source_id": "SRC1341_8_964_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
            "needle": "R2IN964_2_Lee2020_anchor",
            "role": "existing R2/fR nonclaim input template",
        },
        {
            "source_id": "SRC1341_9_964_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
            "needle": "R2RUN964_VERDICT",
            "role": "existing strict nonclaim runner",
        },
        {
            "source_id": "SRC1341_10_965_primitive",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
            "needle": "PQ965_5_verdict",
            "role": "primitive quotient theorem attempt",
        },
    ]
    source_register = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    web_sources = [
        {
            "web_id": "WEB1341_0_Lee2020_R10",
            "url": "https://arxiv.org/abs/2002.11761",
            "source_type": "short-range inverse-square/Yukawa bound",
            "source_note": "arXiv abstract gives gravitational-strength Yukawa range limit below 38.6 micrometres at 95 percent confidence",
            "use_in_1341": "anchor-only R10 scalar-mode bound row",
            "extraction_status": "ANCHOR_ONLY_NON_CURVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1341_1_Capozziello2009_fR_Newtonian",
            "url": "https://arxiv.org/abs/0901.0448",
            "source_type": "f(R) Newtonian-limit theory source",
            "source_note": "arXiv abstract states analytic metric f(R) models generally give Yukawa-like corrections and only f(R)=R recovers the standard Newtonian potential",
            "use_in_1341": "conceptual source for R2/fR scalar-mode/Yukawa residual",
            "extraction_status": "THEORY_SOURCE_NOT_NUMERIC_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1341_2_Stabile2010_fR_PPN",
            "url": "https://arxiv.org/abs/1004.1973",
            "source_type": "f(R) post-Newtonian source",
            "source_note": "arXiv abstract states f(R) PN solutions include Yukawa/oscillating corrections and converge to GR when f tends to R",
            "use_in_1341": "PPN map/source requirement for finite scalar branch",
            "extraction_status": "THEORY_SOURCE_NOT_NUMERIC_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "web_id": "WEB1341_3_Cassini_gamma",
            "url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_type": "PPN gamma experimental source",
            "source_note": "PubMed record identifies Bertotti, Iess, Tortora Nature 2003, DOI 10.1038/nature01997",
            "use_in_1341": "PPN gamma source candidate; exact numeric row remains nonclaim until formula/regime map is complete",
            "extraction_status": "SOURCE_STRING_RECORDED_PPN_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_attempt = [
        {
            "attempt_id": "R2ZERO1341_0_target",
            "claim": "R2/fR scalar mode is absent in the local exterior branch",
            "formal_move": "show c_R2=c_fR=0 or that the term is topological/redundant/non-propagating after parent reduction",
            "result": "TARGET_EXACT",
            "gap": "requires parent-signed metric-only second-order no-extra-scalar theorem",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "R2ZERO1341_1_second_order_filter",
            "claim": "second-order metric-only premise kills R2/fR",
            "formal_move": "R2/fR generically creates fourth-order/scalar dynamics unless coefficient vanishes",
            "result": "FILTER_CLEAN",
            "gap": "filter says what must vanish; it does not prove MTS coefficient vanishes",
            "promotion_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "R2ZERO1341_2_topological_escape",
            "claim": "R2/fR term is topological or boundary-harmless",
            "formal_move": "classify the local curvature-squared piece as topological/no-flux",
            "result": "ESCAPE_NOT_AVAILABLE_FOR_GENERIC_R2FR",
            "gap": "R^2 and generic f(R) are not the 4D Gauss-Bonnet topological invariant",
            "promotion_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "R2ZERO1341_3_integrated_out_tower",
            "claim": "eliminated hidden sectors cannot regenerate R2/fR in S_eff[g]",
            "formal_move": "prove solved auxiliary/projector/memory/scalar sectors give no higher-curvature effective action",
            "result": "NOT_DERIVED",
            "gap": "previous audits mark integrated-out f(R), R2, Yukawa, and nonlocal terms as open hazards",
            "promotion_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "R2ZERO1341_4_primitive_minimality",
            "claim": "MTS primitive quotient forbids curvature-squared marker extensions",
            "formal_move": "derive no natural marker/curvature-tower constructor from motion/time/space primitives",
            "result": "NOT_DERIVED",
            "gap": "primitive quotient/no-marker theorem remains unsigned",
            "promotion_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "R2ZERO1341_5_verdict",
            "claim": "c_R2/c_fR is parent-zeroed",
            "formal_move": "combine second-order filter, no integrated-out tower, primitive minimality, and no-extra-scalar clauses",
            "result": "ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "gap": "zero theorem remains conditional; finite scalar bound row is required",
            "promotion_status": "BOUND_ROUTE_SELECTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    scalar_map = [
        {
            "map_id": "SMAP1341_0_generic_yukawa",
            "model_family": "metric_fR_or_quadratic_R2",
            "potential_or_observable_form": "Phi(r) = -G M/r * [1 + alpha_s exp(-r/lambda_s)]",
            "map_status": "STANDARD_FORM_RECORDED_NONCLAIM",
            "source_basis": "WEB1341_1_Capozziello2009_fR_Newtonian;WEB1341_2_Stabile2010_fR_PPN",
            "missing_for_claim": "parent coefficient normalization, source shape, screening regime, and exact equation reference",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "SMAP1341_1_quadratic_convention",
            "model_family": "R + c_R2 R^2 convention",
            "potential_or_observable_form": "candidate unscreened scalar map: alpha_s=1/3, lambda_s=hbar/(m_s c), m_s^2 ~ 1/(6 c_R2) in common normalization",
            "map_status": "CONVENTION_DEPENDENT_NEEDS_PARENT_NORMALIZATION",
            "source_basis": "R2RUN963_1_mass_coupling_map says formula known but MTS inputs missing; external equation source must be pinned before claim",
            "missing_for_claim": "MTS coefficient units/sign and exact convention linking c_R2 to scalaron mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "SMAP1341_2_PPN_regime",
            "model_family": "solar-system scalar PPN",
            "potential_or_observable_form": "gamma/beta depend on scalar range, screening, source profile, and observation regime",
            "map_status": "SOURCE_CANDIDATE_RECORDED_MAP_NOT_FILLED",
            "source_basis": "WEB1341_2_Stabile2010_fR_PPN;WEB1341_3_Cassini_gamma",
            "missing_for_claim": "explicit gamma(beta,lambda,alpha) projection and Cassini-compatible regime selection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_rows = [
        {
            "bound_id": "BOUND1341_0_R10_Lee2020_anchor",
            "arena": "R10_short_range_Yukawa",
            "bound_quantity": "gravitational_strength_Yukawa_range",
            "lambda_value": "38.6",
            "lambda_units": "micrometre",
            "alpha_bound": "1.0",
            "confidence_or_context": "95_percent_confidence_gravitational_strength_anchor",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "extraction_method": "arXiv_abstract_anchor_only",
            "curve_status": "ANCHOR_ONLY_NON_CURVE",
            "missing_for_claim": "full alpha(lambda) curve and interpolation at predicted alpha/lambda",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BOUND1341_1_R10_full_curve_required",
            "arena": "R10_short_range_Yukawa",
            "bound_quantity": "alpha_bound(lambda)",
            "lambda_value": "MISSING_DIGITIZED_CURVE",
            "lambda_units": "micrometre",
            "alpha_bound": "MISSING_DIGITIZED_CURVE",
            "confidence_or_context": "full curve required before any scalar-mode pass/fail claim",
            "source_url": "MISSING_FULL_CURVE_SOURCE_EXTRACTION",
            "extraction_method": "not_acquired",
            "curve_status": "FULL_CURVE_REQUIRED",
            "missing_for_claim": "digitized/source-backed curve rows with units and provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BOUND1341_2_PPN_Cassini_source_candidate",
            "arena": "solar_system_PPN",
            "bound_quantity": "gamma_minus_1",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "confidence_or_context": "Cassini gamma source candidate; formula/regime map missing",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "extraction_method": "source_string_recorded",
            "curve_status": "PPN_SOURCE_CANDIDATE_MAP_MISSING",
            "missing_for_claim": "explicit R2/fR scalar prediction for gamma in Cassini regime and chosen confidence convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    prediction_template = [
        {
            "prediction_id": "PRED1341_0_MTS_coefficient_required",
            "model_id": "MTS_R2FR_scalar_mode_candidate",
            "coefficient_symbol": "c_R2_or_c_fR",
            "coefficient_value": "MISSING_PARENT_INPUT",
            "coefficient_units": "MISSING_UNITS",
            "alpha_predicted": "MISSING_ALPHA",
            "lambda_predicted_um": "MISSING_LAMBDA",
            "mass_eV": "MISSING_MASS",
            "screening_flag": "MISSING_SCREENING_STATUS",
            "source_file": "MISSING_SOURCE_FILE",
            "formula_reference": "MISSING_FORMULA_REFERENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prediction_id": "PRED1341_1_zero_switch",
            "model_id": "MTS_R2FR_zero_route",
            "coefficient_symbol": "c_R2_or_c_fR",
            "coefficient_value": "0_IF_R2ZERO1341_PARENT_THEOREM_SIGNED_ELSE_MISSING",
            "coefficient_units": "not_applicable_if_zero",
            "alpha_predicted": "0_IF_PARENT_SIGNED_ELSE_MISSING",
            "lambda_predicted_um": "not_applicable_if_zero",
            "mass_eV": "infinite_if_parent_signed_else_missing",
            "screening_flag": "not_applicable_if_zero",
            "source_file": "P8_Y5_R10_1341_R2FR_ZERO_THEOREM_ATTEMPT.csv",
            "formula_reference": "R2ZERO1341_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    required_prediction_fields = [
        "coefficient_value",
        "coefficient_units",
        "alpha_predicted",
        "lambda_predicted_um",
        "mass_eV",
        "screening_flag",
        "source_file",
        "formula_reference",
    ]
    full_curve_available = any(row["curve_status"] == "FULL_CURVE_DIGITIZED" and bool_false(row["valid_for_claim"]) is False for row in bound_rows)
    zero_parent_signed = False
    runner_rows = []
    for row in prediction_template:
        missing = missing_markers(row, required_prediction_fields)
        zero_route = row["prediction_id"].endswith("zero_switch")
        accepted = False
        if zero_route and not zero_parent_signed:
            verdict = "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED"
        elif missing:
            verdict = "REJECTED_MISSING_MTS_PREDICTION_INPUTS"
        elif not full_curve_available:
            verdict = "REJECTED_FULL_BOUND_CURVE_MISSING"
        else:
            verdict = "ACCEPTED_NONCLAIM_SMOKE_ONLY"
            accepted = True
        runner_rows.append(
            {
                "run_id": row["prediction_id"].replace("PRED", "RUN"),
                "prediction_id": row["prediction_id"],
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
                "verdict": verdict,
                "missing_fields": ";".join(missing) if missing else "none",
                "reason": "strict R2/fR runner: no pass without parent-zero theorem or complete MTS prediction plus source-backed full bound curve",
                "valid_for_claim": False,
            }
        )
    runner_rows.append(
        {
            "run_id": "RUN1341_VERDICT",
            "prediction_id": "all_rows",
            "accepted_for_scoring": False,
            "claim_allowed": False,
            "verdict": "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "missing_fields": "parent_zero_signature_or_MTS_coefficient_and_full_bound_curve",
            "reason": "zero theorem failed; bound route is prepared but not scoreable",
            "valid_for_claim": False,
        }
    )

    claim_gate = [
        {
            "gate_id": "CLAIM1341_0_zero_theorem",
            "claim": "R2/fR scalar mode zero",
            "allowed_if": "R2ZERO1341_5_verdict becomes parent-signed with no integrated-out tower loophole",
            "current_status": "BLOCKED",
            "reason": "zero theorem not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CLAIM1341_1_bound_pass",
            "claim": "finite R2/fR scalar branch passes R10/PPN bounds",
            "allowed_if": "complete MTS coefficient prediction plus full source-backed alpha(lambda)/PPN bound rows",
            "current_status": "BLOCKED",
            "reason": "MTS coefficient and full curve/regime map missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CLAIM1341_2_EH_core",
            "claim": "EH core/local-GR left-hand side",
            "allowed_if": "R2/fR plus every other R11 family is zeroed or bounded and GM/PPN gates pass",
            "current_status": "BLOCKED",
            "reason": "1341 only handles first scalar family as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1341_0_zero_result",
            "decision": "R2/fR scalar-mode zero theorem is not derived",
            "because": "second-order/no-extra-scalar/minimal quotient premises remain unsigned and integrated-out towers remain possible",
            "effect": "finite scalar bound route must remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1341_1_bound_result",
            "decision": "source-backed bound scaffold is improved but nonclaim",
            "because": "Lee 2020 gives an anchor, Cassini gives a PPN source candidate, but full curve, MTS coefficient, and regime map are missing",
            "effect": "next work should acquire/digitize full R10 curve or derive scalar-mode zero before any scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1341_0_1342",
            "target_file": "1342-Y5-R10-RAB-R2FR-full-bound-curve-acquisition-or-integrated-out-tower-zero-proof.md",
            "target_script": "scripts/Y5_R10_RAB_R2FR_full_bound_curve_acquisition_or_integrated_out_tower_zero_proof.py",
            "task": "either close the integrated-out R2/fR tower loophole or acquire a source-backed full alpha(lambda) bound curve for finite scalar-mode scoring",
            "success_condition": "a parent-zero proof for c_R2/c_fR, or a full nonclaim bound-curve intake with interpolation checks and provenance",
            "do_not": "do not claim from anchor-only rows, do not infer missing MTS coefficient, do not promote EH/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        web_sources,
        zero_attempt,
        scalar_map,
        bound_rows,
        prediction_template,
        runner_rows,
        claim_gate,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    web_sources_recorded = all(str(row["url"]).startswith("https://") for row in web_sources)
    zero_not_derived = any(row["attempt_id"] == "R2ZERO1341_5_verdict" and row["result"] == "ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in zero_attempt)
    scalar_map_nonclaim = all(row["valid_for_claim"] is False for row in scalar_map)
    anchor_only_no_claim = any(row["bound_id"] == "BOUND1341_0_R10_Lee2020_anchor" and row["curve_status"] == "ANCHOR_ONLY_NON_CURVE" for row in bound_rows)
    full_curve_missing = any(row["bound_id"] == "BOUND1341_1_R10_full_curve_required" and row["curve_status"] == "FULL_CURVE_REQUIRED" for row in bound_rows)
    runner_rejects = all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in runner_rows)
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1342 = next_target[0]["target_file"].startswith("1342-")

    validations = [
        validation_row(
            "VAL1341_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1341_1_web_sources_recorded",
            "external source URLs are recorded for theory and bound provenance",
            web_sources_recorded,
            ";".join(row["web_id"] for row in web_sources),
        ),
        validation_row(
            "VAL1341_2_zero_not_derived",
            "R2/fR zero theorem is not promoted",
            zero_not_derived,
            "R2ZERO1341_5_verdict=ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
        ),
        validation_row(
            "VAL1341_3_scalar_map_nonclaim",
            "scalar-mode map rows remain nonclaim and convention-guarded",
            scalar_map_nonclaim,
            ";".join(f"{row['map_id']}={row['map_status']}" for row in scalar_map),
        ),
        validation_row(
            "VAL1341_4_anchor_only_no_claim",
            "R10 Lee 2020 source is anchor-only non-curve and cannot claim",
            anchor_only_no_claim,
            "BOUND1341_0_R10_Lee2020_anchor=ANCHOR_ONLY_NON_CURVE",
        ),
        validation_row(
            "VAL1341_5_full_curve_missing",
            "full source-backed alpha(lambda) curve remains required",
            full_curve_missing,
            "BOUND1341_1_R10_full_curve_required=FULL_CURVE_REQUIRED",
        ),
        validation_row(
            "VAL1341_6_runner_rejects",
            "strict R2/fR dry-run rejects zero switch and missing MTS prediction",
            runner_rejects,
            ";".join(f"{row['run_id']}={row['verdict']}" for row in runner_rows),
        ),
        validation_row(
            "VAL1341_7_claims_blocked",
            "zero, bound-pass, and EH/local-GR claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1341_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1341_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1341_10_next_target_1342",
            "next target routes to full bound curve acquisition or integrated-out tower zero proof",
            next_is_1342,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1341_11_overall",
            "overall 1341 validation",
            all(row["status"] == "PASS" for row in validations),
            "1341 fails the R2/fR zero theorem honestly and prepares source-backed but nonclaim scalar bound rows",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(WEB_SOURCE_PATH, web_sources)
    write_csv(ZERO_ATTEMPT_PATH, zero_attempt)
    write_csv(SCALAR_MAP_PATH, scalar_map)
    write_csv(BOUND_SOURCE_PATH, bound_rows)
    write_csv(PREDICTION_TEMPLATE_PATH, prediction_template)
    write_csv(RUNNER_DRYRUN_PATH, runner_rows)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1341 does not derive the `R2/fR` scalar-mode zero theorem. The second-order filter is clean, but MTS has not parent-signed the no-extra-scalar/no-integrated-out-curvature-tower premises.

**Main progress:** the finite scalar branch is now source-backed but nonclaim: Lee 2020 supplies an anchor-only R10 Yukawa source, Capozziello/Stabile supply f(R) Yukawa/PPN theory sources, and Cassini supplies a PPN source candidate. The runner still rejects every row because the MTS coefficient, full alpha(lambda) curve, and regime map are missing.

**Decision:** next target is `1342`: either close the integrated-out R2/fR tower loophole, or acquire/digitize the full source-backed R10 alpha(lambda) curve before any finite scalar scoring.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Web Source Ledger
{markdown_table(web_sources, ["web_id", "url", "source_type", "source_note", "use_in_1341", "extraction_status", "valid_for_claim", "claim_allowed"])}

## R2FR Zero Theorem Attempt
{markdown_table(zero_attempt, ["attempt_id", "claim", "formal_move", "result", "gap", "promotion_status", "valid_for_claim", "claim_allowed"])}

## Scalar Mode Map Contract
{markdown_table(scalar_map, ["map_id", "model_family", "potential_or_observable_form", "map_status", "source_basis", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## Source Backed Bound Rows Nonclaim
{markdown_table(bound_rows, ["bound_id", "arena", "bound_quantity", "lambda_value", "lambda_units", "alpha_bound", "confidence_or_context", "source_url", "extraction_method", "curve_status", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## MTS R2FR Prediction Template
{markdown_table(prediction_template, ["prediction_id", "model_id", "coefficient_symbol", "coefficient_value", "coefficient_units", "alpha_predicted", "lambda_predicted_um", "mass_eV", "screening_flag", "source_file", "formula_reference", "valid_for_claim", "claim_allowed"])}

## R2FR Bound Runner Dryrun
{markdown_table(runner_rows, ["run_id", "prediction_id", "accepted_for_scoring", "claim_allowed", "verdict", "missing_fields", "reason", "valid_for_claim"])}

## Claim Gate
{markdown_table(claim_gate, ["gate_id", "claim", "allowed_if", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
