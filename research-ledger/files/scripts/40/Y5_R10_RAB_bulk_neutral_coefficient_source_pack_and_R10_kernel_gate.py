from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1391-Y5-R10-RAB-bulk-neutral-coefficient-source-pack-and-R10-kernel-gate.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1391_SOURCE_REGISTER.csv"
BULK_ZERO_PATH = SRC_DIR / "P8_Y5_R10_1391_BULK_NEUTRAL_ZERO_THEOREM_ATTEMPT.csv"
BULK_PACK_PATH = SRC_DIR / "P8_Y5_R10_1391_BULK_NEUTRAL_COEFFICIENT_SOURCE_PACK.csv"
R10_KERNEL_PATH = SRC_DIR / "P8_Y5_R10_1391_R10_BULK_MATERIAL_KERNEL_GATE.csv"
RUNNER_REFUSAL_PATH = SRC_DIR / "P8_Y5_R10_1391_R10_RUNNER_REFUSAL_AUDIT.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1391_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1391_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1391_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1391_VALIDATION.csv"

STATUS = (
    "bulk_neutral_source_pack_and_R10_kernel_gate_written_"
    "theorem_zero_unsigned_R10_scoring_blocked"
)
CLAIM_CEILING = (
    "bulk_neutral_coefficient_pack_and_R10_kernel_gate_only_no_bulk_zero_no_numeric_alpha_"
    "no_R10_no_WEP_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1391_0_1390_doc",
        "source_path": "1390-Y5-R10-RAB-common-calibration-silence-or-first-material-coefficient-bound.md",
        "required_anchor": "NEXT1390_0_1391",
        "purpose": "handoff to bulk neutral coefficient pack and R10 kernel gate",
    },
    {
        "source_id": "SRC1391_1_1390_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1390_NEXT_TARGET.csv",
        "required_anchor": "NEXT1390_0_1391",
        "purpose": "machine-readable 1391 target",
    },
    {
        "source_id": "SRC1391_2_1390_silence",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1390_COMMON_CALIBRATION_SILENCE_PROOF.csv",
        "required_anchor": "CCS1390_7_verdict",
        "purpose": "common calibration silence remains unsigned",
    },
    {
        "source_id": "SRC1391_3_1390_bulk_rows",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1390_BULK_MATERIAL_COEFFICIENT_BOUND_ROWS.csv",
        "required_anchor": "BMB1390_6_bound_verdict",
        "purpose": "bulk material coefficient rows to refine",
    },
    {
        "source_id": "SRC1391_4_1389_bulk_class",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv",
        "required_anchor": "MSC1389_0_bulk_neutral_baryonic",
        "purpose": "bulk neutral baryonic material/source class",
    },
    {
        "source_id": "SRC1391_5_1389_convention",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_COUPLING_EXPANSION_CONVENTION.csv",
        "required_anchor": "CEC1389_5_verdict",
        "purpose": "Delta_w/beta expansion convention",
    },
    {
        "source_id": "SRC1391_6_563_doc",
        "source_path": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "required_anchor": "B563_0_no_full_bound_curve",
        "purpose": "R10 real-source anchor pass says full curve is missing",
    },
    {
        "source_id": "SRC1391_7_563_blockers",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_563_BLOCKER_LEDGER.csv",
        "required_anchor": "B563_1_no_numeric_MTS_alpha",
        "purpose": "R10 blocker for symbolic MTS alpha rows",
    },
    {
        "source_id": "SRC1391_8_563_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_563_RUNNER_SUMMARY.csv",
        "required_anchor": "R10_RUNNER_563_LIVE_PLACEHOLDER_RECHECK",
        "purpose": "existing R10 runner blocks placeholders",
    },
    {
        "source_id": "SRC1391_9_563_evaluator",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_563_EVALUATOR.csv",
        "required_anchor": "E563_1_full_curve_missing",
        "purpose": "anchor-only bound rows are not R10 evidence",
    },
    {
        "source_id": "SRC1391_10_anchor_bound",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "required_anchor": "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "purpose": "source-backed nonclaim R10 threshold anchor",
    },
    {
        "source_id": "SRC1391_11_live_bound_placeholder",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_anchor": "R10_BOUND_PLACEHOLDER_0",
        "purpose": "live claim curve remains placeholder invalid",
    },
    {
        "source_id": "SRC1391_12_1036_beta_product",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "source-test beta product rule",
    },
    {
        "source_id": "SRC1391_13_this_script",
        "source_path": "scripts/Y5_R10_RAB_bulk_neutral_coefficient_source_pack_and_R10_kernel_gate.py",
        "required_anchor": "STATUS",
        "purpose": "1391 generator",
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


def bulk_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "BZT1391_0_target",
            "claim": "bulk neutral matter has no residual action-weight coupling",
            "attempted_derivation": "try to reduce Delta_w_bulk and beta_w,bulk to the ordinary-matter universal owner theorem",
            "result": "TARGET_DEFINED",
            "gap": "none for target definition",
            "next_action": "test ordinary-matter universality clauses",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BZT1391_1_common_owner_route",
            "claim": "bulk matter inherits one common parent action owner",
            "attempted_derivation": "combine common w_* theorem with bulk neutral matter class MSC1389_0",
            "result": "CONDITIONAL_ROUTE",
            "gap": "common w_* global-constant signature is not parent-signed",
            "next_action": "retain beta_* and Delta_w_bulk rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BZT1391_2_binding_inheritance",
            "claim": "bulk neutral matter has no independent electronic, nuclear, or EM binding source weight",
            "attempted_derivation": "treat bulk mass as a composition of common ordinary-matter sub-actions",
            "result": "BINDING_INHERITANCE_NOT_DERIVED",
            "gap": "electronic, nuclear, and EM binding rows in 1389 are not theorem-zero",
            "next_action": "keep inherited binding terms inside observed charge Q_bulk^w",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BZT1391_3_source_test_equality",
            "claim": "bulk R10 source and test bodies have identical coupling legs",
            "attempted_derivation": "identify both as neutral bulk baryonic matter",
            "result": "SOURCE_TEST_EQUALITY_NOT_ENOUGH",
            "gap": "even identical legs require a numeric or zero beta_w,bulk and real material composition",
            "next_action": "stage separate source and test rows with a possible equality constraint",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BZT1391_4_product_zero_condition",
            "claim": "R10 bulk alpha vanishes if both source and test beta legs vanish and tails vanish",
            "attempted_derivation": "alpha_bulk,ST(lambda)=K_ST(lambda) beta_bulk,S beta_bulk,T + epsilon_tail(lambda)",
            "result": "EXACT_CONDITIONAL_ZERO",
            "gap": "beta_bulk,S, beta_bulk,T, K_ST, and epsilon_tail are not parent-filled",
            "next_action": "use this as the R10 zero certificate shape, not as evidence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BZT1391_5_current_verdict",
            "claim": "bulk theorem-zero is currently claim-ready",
            "attempted_derivation": "compare 1390 common silence, 1389 material map, 563 R10 blockers, and 1036 product rule",
            "result": "BULK_ZERO_NOT_PARENT_SIGNED",
            "gap": "ordinary-matter universality, binding inheritance, beta zero, and tail silence are still unsigned",
            "next_action": "use nonclaim bulk coefficient source pack and R10 kernel gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bulk_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "pack_id": "BCP1391_0_beta_star",
            "coefficient": "beta_*",
            "source_role": "universal common-factor derivative inherited by bulk source/test legs",
            "formula_or_handle": "beta_* := partial_phi_c ln w_*",
            "required_provenance": "parent theorem beta_*=0 or sourced local/R10 bound",
            "current_value": "MISSING",
            "source_backing_status": "1390_row_exists_not_value_backed",
            "current_status": "MISSING_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_1_Delta_w_bulk",
            "coefficient": "Delta_w_bulk",
            "source_role": "bulk neutral source normalization after common calibration",
            "formula_or_handle": "Delta_w_bulk := w_bulk/w_* - 1",
            "required_provenance": "parent theorem Delta_w_bulk=0 or composition/source bound",
            "current_value": "MISSING",
            "source_backing_status": "1390_row_exists_not_value_backed",
            "current_status": "MISSING_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_2_beta_bulk_source",
            "coefficient": "beta_bulk,S",
            "source_role": "R10/PPN/orbital bulk source leg",
            "formula_or_handle": "beta_bulk,S = beta_* + beta_w,bulk,S + inherited binding terms",
            "required_provenance": "source material composition; canonical phi convention; theorem-zero or bound",
            "current_value": "MISSING",
            "source_backing_status": "material_class_defined_value_missing",
            "current_status": "MISSING_SOURCE_LEG",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_3_beta_bulk_test",
            "coefficient": "beta_bulk,T",
            "source_role": "R10/WEP test body leg",
            "formula_or_handle": "beta_bulk,T = beta_* + beta_w,bulk,T + inherited binding terms",
            "required_provenance": "test material composition; canonical phi convention; theorem-zero or bound",
            "current_value": "MISSING",
            "source_backing_status": "material_class_defined_value_missing",
            "current_status": "MISSING_TEST_LEG",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_4_K_bulk_ST",
            "coefficient": "K_bulk,ST(lambda)",
            "source_role": "R10 finite-size/profile/kernel factor",
            "formula_or_handle": "kernel multiplying beta_bulk,S beta_bulk,T in alpha_bulk,ST(lambda)",
            "required_provenance": "source/test geometry, density model, finite-size correction, lambda convention",
            "current_value": "MISSING",
            "source_backing_status": "kernel_schema_only",
            "current_status": "MISSING_KERNEL",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_5_epsilon_tail",
            "coefficient": "epsilon_tail(lambda)",
            "source_role": "unmodelled tail/nonbulk remainder envelope",
            "formula_or_handle": "alpha_bulk,ST(lambda)=K_bulk,ST beta_bulk,S beta_bulk,T + epsilon_tail(lambda)",
            "required_provenance": "tail theorem-zero or conservative envelope bound",
            "current_value": "MISSING",
            "source_backing_status": "tail_schema_only",
            "current_status": "MISSING_TAIL_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_6_bound_curve_handle",
            "coefficient": "alpha_bound(lambda)",
            "source_role": "external R10 comparison bound",
            "formula_or_handle": "use live digitized curve only when valid_for_claim=true; anchor smoke rows remain nonclaim",
            "required_provenance": "full digitized/source-backed alpha(lambda) curve, not alpha=1 threshold only",
            "current_value": "ANCHOR_ONLY_NONCLAIM_AVAILABLE",
            "source_backing_status": "Eot-Wash 2020/2007 anchors source-backed but not full curve",
            "current_status": "BOUND_CURVE_NOT_CLAIM_READY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "pack_id": "BCP1391_7_pack_verdict",
            "coefficient": "bulk neutral coefficient source pack",
            "source_role": "first explicit bulk channel for R10/Newton/WEP/PPN/orbital/local-GR gates",
            "formula_or_handle": "all rows above must be theorem-zero or source-backed before scoring",
            "required_provenance": "beta_*, Delta_w_bulk, beta source/test, K, tail, material pair, and real bound curve",
            "current_value": "MISSING",
            "source_backing_status": "pack_ready_nonclaim",
            "current_status": "BULK_SOURCE_PACK_READY_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def r10_kernel_rows() -> list[dict[str, str]]:
    return [
        {
            "kernel_id": "R10K1391_0_force_law",
            "gate": "force law convention",
            "requirement": "bulk residual must be expressed as a Yukawa/inverse-square strength ratio alpha_bulk,ST(lambda)",
            "current_status": "SCHEMA_READY",
            "blocks_if_missing": "R10 comparator cannot read the prediction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_1_source_leg",
            "gate": "bulk source leg",
            "requirement": "beta_bulk,S or theorem-zero certificate, with material/source geometry",
            "current_status": "MISSING_SOURCE_LEG",
            "blocks_if_missing": "no R10 alpha prediction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_2_test_leg",
            "gate": "bulk test leg",
            "requirement": "beta_bulk,T or theorem-zero certificate, with test-body material composition",
            "current_status": "MISSING_TEST_LEG",
            "blocks_if_missing": "no WEP/R10 test response",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_3_profile_kernel",
            "gate": "K_bulk,ST(lambda) profile factor",
            "requirement": "finite-size/source-test geometry kernel in the same lambda convention as the bound curve",
            "current_status": "MISSING_PROFILE_KERNEL",
            "blocks_if_missing": "no comparison at a physical lambda",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_4_bound_curve",
            "gate": "external alpha(lambda) bound",
            "requirement": "dense positive numeric alpha_bound(lambda) curve or official machine-readable table",
            "current_status": "ANCHOR_ONLY_NOT_CLAIM_READY",
            "blocks_if_missing": "anchor-only threshold cannot support R10 score",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_5_comparator",
            "gate": "strict comparator",
            "requirement": "abs(alpha_bulk,ST(lambda)) <= alpha_bound(lambda) for all valid rows, with both sides valid_for_claim=true",
            "current_status": "COMPARATOR_AVAILABLE_BUT_NO_VALID_ROWS",
            "blocks_if_missing": "runner must keep R10_pass_for_claim=false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "R10K1391_6_verdict",
            "gate": "R10 kernel gate verdict",
            "requirement": "all source/test/kernel/bound/comparator gates close before any R10 claim",
            "current_status": "R10_KERNEL_GATE_READY_SCORING_BLOCKED",
            "blocks_if_missing": "R10, Newton, PPN, WEP, and local-GR promotion remain blocked",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RRF1391_0_live_placeholder",
            "input_pair": "R10_alpha_lambda_curve_MTS_source_normalization.csv vs R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "prior_evidence": "R10_RUNNER_563_LIVE_PLACEHOLDER_RECHECK",
            "required_status": "R10_pass_for_claim=False",
            "current_reason": "live files still contain placeholder/nonvalid rows",
            "next_action": "do not rerun as claim; fill real MTS alpha and real bound curve first",
            "claim_allowed": "False",
        },
        {
            "runner_id": "RRF1391_1_anchor_smoke",
            "input_pair": "R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv vs R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            "prior_evidence": "R10_RUNNER_563_ANCHOR_SMOKE_RECHECK",
            "required_status": "R10_pass_for_claim=False",
            "current_reason": "MTS alpha is symbolic and anchors are valid provenance but not claim curve rows",
            "next_action": "use only for plumbing until parent coefficients and full curve exist",
            "claim_allowed": "False",
        },
        {
            "runner_id": "RRF1391_2_bulk_candidate",
            "input_pair": "future bulk neutral alpha candidate vs future R10 full curve",
            "prior_evidence": "BCP1391 and R10K1391 gates",
            "required_status": "not runnable for claim",
            "current_reason": "beta source/test, K kernel, tail, material pair, and full curve are missing",
            "next_action": "create candidate rows only with valid_for_claim=false until every field is sourced",
            "claim_allowed": "False",
        },
        {
            "runner_id": "RRF1391_3_verdict",
            "input_pair": "all R10 bulk routes",
            "prior_evidence": "563 blockers plus 1391 kernel gate",
            "required_status": "BLOCKED_NO_SCORE",
            "current_reason": "both theory side and bound side lack claim-ready numeric rows",
            "next_action": "move to first fill of beta_bulk/K/tail schema or full-curve digitization",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1391_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus and local bound files",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1391_1_bulk_zero",
            "gate": "bulk neutral coefficients are theorem-zero",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "ordinary-matter universality, binding inheritance, beta zero, and tail silence are not signed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1391_2_bulk_pack",
            "gate": "bulk neutral coefficient source pack exists",
            "status": "PASS_NONCLAIM_PACK",
            "reason": "source/test roles, units, formulas, and provenance requirements are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1391_3_R10_kernel",
            "gate": "R10 material-kernel gate exists",
            "status": "PASS_SCHEMA_ONLY",
            "reason": "source leg, test leg, kernel, bound curve, and comparator gates are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1391_4_R10_score",
            "gate": "R10 score may be reported",
            "status": "BLOCKED_NO_VALID_ROWS",
            "reason": "MTS alpha remains symbolic and external curve is anchor-only/placeholder",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1391_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1391 is a bulk/R10 gate, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1391_0_bulk_zero_status",
            "decision": "bulk theorem-zero is not claimed",
            "because": "bulk universality inherits the same unsigned action-measure/common-calibration clauses",
            "next_action": "continue with explicit finite rows rather than hiding the coupling",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1391_1_R10_gate_status",
            "decision": "R10 can now see the exact missing theory and data legs",
            "because": "alpha_bulk needs beta source, beta test, profile kernel, tail, material pair, and full bound curve",
            "next_action": "choose between first beta/kernel fill and real full-curve digitization",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1391_2_best_next_move",
            "decision": "fill the theory-side bulk alpha template before scoring",
            "because": "without a predicted alpha(lambda), even a perfect bound curve cannot test MTS",
            "next_action": "build beta_bulk/K/tail candidate template with hard nonclaim gates",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1391_0_1392",
            "next_doc": "1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md",
            "next_script": "scripts/Y5_R10_RAB_bulk_alpha_template_beta_kernel_tail_fill_or_zero_proof.py",
            "task": "attempt theorem-zero for beta_bulk/K/tail; otherwise create a strict nonclaim bulk alpha(lambda) template compatible with the existing R10 runner",
            "success_condition": "candidate alpha rows expose beta source/test, K(lambda), epsilon tail, lambda units, source files, and claim flags; runner remains blocked until numeric/provenance fields are real",
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
    zero: list[dict[str, str]],
    pack: list[dict[str, str]],
    kernel: list[dict[str, str]],
    refusal: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    zero_blocked = any(
        row["zero_id"] == "BZT1391_5_current_verdict"
        and row["result"] == "BULK_ZERO_NOT_PARENT_SIGNED"
        and row["claim_allowed"] == "False"
        for row in zero
    )
    conditional_zero = any(
        row["zero_id"] == "BZT1391_4_product_zero_condition"
        and row["result"] == "EXACT_CONDITIONAL_ZERO"
        and row["valid_for_claim"] == "False"
        for row in zero
    )
    pack_ready = any(
        row["pack_id"] == "BCP1391_7_pack_verdict"
        and row["current_status"] == "BULK_SOURCE_PACK_READY_SCORING_BLOCKED"
        and row["valid_for_claim"] == "False"
        for row in pack
    )
    pack_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in pack)
    kernel_blocked = any(
        row["kernel_id"] == "R10K1391_6_verdict"
        and row["current_status"] == "R10_KERNEL_GATE_READY_SCORING_BLOCKED"
        and row["claim_allowed"] == "False"
        for row in kernel
    )
    runner_blocked = any(
        row["runner_id"] == "RRF1391_3_verdict"
        and row["required_status"] == "BLOCKED_NO_SCORE"
        and row["claim_allowed"] == "False"
        for row in refusal
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1391_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_bound = csv_rows(Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv"))
    live_bound_invalid = all(row.get("valid_for_claim", "").lower() == "false" for row in prior_bound)
    prior_1390 = csv_rows(Path("source-intake/mts_residuals/P8_Y5_R10_1390_CLAIM_GATE.csv"))
    prior_local_blocked = any(
        row["gate_id"] == "GATE1390_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1390
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        BULK_ZERO_PATH,
        BULK_PACK_PATH,
        R10_KERNEL_PATH,
        RUNNER_REFUSAL_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_bulk_neutral_coefficient_source_pack_and_R10_kernel_gate.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and zero_blocked
        and conditional_zero
        and pack_ready
        and pack_nonclaim
        and kernel_blocked
        and runner_blocked
        and local_claim_blocked
        and prior_local_blocked
        and live_bound_invalid
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1391_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1391_1_bulk_zero_refusal",
            "check": "bulk zero theorem is conditional and not claimed",
            "status": "PASS" if zero_blocked and conditional_zero else "FAIL",
            "details": "BZT1391_4 gives the conditional product zero; BZT1391_5 keeps bulk zero unsigned.",
        },
        {
            "validation_id": "VAL1391_2_bulk_pack",
            "check": "bulk coefficient source pack is explicit and nonclaim",
            "status": "PASS" if pack_ready and pack_nonclaim else "FAIL",
            "details": f"pack_rows={len(pack)}; all_nonclaim={pack_nonclaim}",
        },
        {
            "validation_id": "VAL1391_3_R10_kernel_refusal",
            "check": "R10 material-kernel gate blocks scoring",
            "status": "PASS" if kernel_blocked and runner_blocked and live_bound_invalid else "FAIL",
            "details": "R10K1391_6 and RRF1391_3 block scoring; live digitized bound rows remain invalid for claim.",
        },
        {
            "validation_id": "VAL1391_4_claim_refusal",
            "check": "local and arena claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1391_5 and prior GATE1390_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1391_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1391_6_overall",
            "check": "overall 1391 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1391 writes the bulk neutral source pack and R10 material-kernel gate while keeping all R10/local claims blocked.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    zero: list[dict[str, str]],
    pack: list[dict[str, str]],
    kernel: list[dict[str, str]],
    refusal: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1391 - Y5 R10 RAB Bulk Neutral Coefficient Source Pack And R10 Kernel Gate

**Generated:** {generated}

**Current verdict:** bulk neutral matter now has an explicit coefficient source pack and R10 material-kernel gate. The clean zero route exists only conditionally: `alpha_bulk,ST(lambda)=0` if the source leg, test leg, and tail are theorem-zero. The current corpus does not yet sign those zero clauses.

**Discipline move:** R10 is now gated by five visible legs: bulk source beta, bulk test beta, profile kernel `K_bulk,ST(lambda)`, tail envelope, and a real alpha(lambda) bound curve. The Eot-Wash anchor rows are source-backed provenance, not a claim-ready curve.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Bulk Neutral Zero Theorem Attempt

{md_table(zero)}

## Bulk Neutral Coefficient Source Pack

{md_table(pack)}

## R10 Bulk Material Kernel Gate

{md_table(kernel)}

## R10 Runner Refusal Audit

{md_table(refusal)}

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
    zero = bulk_zero_rows()
    pack = bulk_pack_rows()
    kernel = r10_kernel_rows()
    refusal = runner_refusal_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, zero, pack, kernel, refusal, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(BULK_ZERO_PATH, zero)
    write_csv(BULK_PACK_PATH, pack)
    write_csv(R10_KERNEL_PATH, kernel)
    write_csv(RUNNER_REFUSAL_PATH, refusal)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, zero, pack, kernel, refusal, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1391 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
