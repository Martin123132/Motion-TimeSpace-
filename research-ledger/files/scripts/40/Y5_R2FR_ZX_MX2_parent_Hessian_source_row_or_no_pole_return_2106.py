from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2106-Y5-R2FR-ZX-MX2-parent-Hessian-source-row-or-no-pole-return.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2105_DOC = ROOT / "2105-Y5-R2FR-cg-canonical-normalization-and-gamma-bound-runner.md"
CSV_2105_INPUTS = OUT / "P8_Y5_PARENT_QLOC_2105_INPUT_EXTRACTION_ROWS.csv"
CSV_2105_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2105_GAMMA_RUNNER.csv"
CSV_2105_DEC = OUT / "P8_Y5_PARENT_QLOC_2105_DECISION_LEDGER.csv"
CSV_2105_NEXT = OUT / "P8_Y5_PARENT_QLOC_2105_NEXT_TARGET.csv"
CSV_2105_VAL = OUT / "P8_Y5_BRR545_2105_VALIDATION.csv"

SRC_1847_DOC = ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"
CSV_1847_HESSIAN = OUT / "P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv"
SRC_1848_DOC = ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
CSV_1848_SOURCE_ZERO = OUT / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv"
SRC_1854_DOC = ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md"
CSV_1854_RESULT = OUT / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv"
CSV_2023_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv"
SRC_2034_DOC = ROOT / "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md"
CSV_2034_HESSIAN = OUT / "P8_Y5_PARENT_QLOC_2034_ROW_NULL_HESSIAN_GATE.csv"
SRC_2035_DOC = ROOT / "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md"
CSV_2035_SCAN = OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_SCAN.csv"
CSV_2035_REQ = OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_REQUIREMENTS.csv"
CSV_2035_DEC = OUT / "P8_Y5_PARENT_QLOC_2035_DECISION_LEDGER.csv"
CSV_2035_VAL = OUT / "P8_Y5_BRR545_2035_VALIDATION.csv"
SRC_2079_DOC = ROOT / "2079-Y5-R2FR-kfloor-topological-Hessian-owner-or-finite-noncoercive-Robin-demotion.md"
CSV_2079_HUNT = OUT / "P8_Y5_PARENT_QLOC_2079_KFLOOR_SOURCE_ATTEMPTS.csv"
CSV_2079_ACQ = OUT / "P8_Y5_PARENT_QLOC_2079_FINITE_BRANCH_ACQUISITION_ROWS.csv"
CSV_2079_VAL = OUT / "P8_Y5_BRR545_2079_VALIDATION.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2106_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2106-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2106*",
        "*Y5_R2FR_ZX_MX2_parent_Hessian_source_row_or_no_pole_return_2106*",
        "*AFRAME_ZX_MX2_HESSIAN_2106*",
        "*JR2106_NO_POLE*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2106_00_2105_doc",
            SRC_2105_DOC,
            ["NEXT2105_0_2106", "ZX_MX2_PARENT_HESSIAN_SOURCE_ROW_NEXT", "VAL2105_OVERALL"],
            "2105 selects Z_X/M_X^2 parent Hessian source row or no-pole return.",
        ),
        (
            "SRC2106_01_2105_inputs",
            CSV_2105_INPUTS,
            ["IN2105_0_ZX", "MISSING_ZX", "IN2105_1_MX2"],
            "2105 input ledger says Z_X and M_X^2 are missing.",
        ),
        (
            "SRC2106_02_2105_runner",
            CSV_2105_RUNNER,
            ["RUN2105_VERDICT", "REFUSES_SCORE", "missing parent inputs"],
            "2105 runner refuses gamma scoring without Hessian/range inputs.",
        ),
        (
            "SRC2106_03_2105_decision",
            CSV_2105_DEC,
            ["DEC2105_1_best_next", "ZX_MX2_PARENT_HESSIAN_SOURCE_ROW_NEXT"],
            "2105 decision identifies the Hessian bottleneck.",
        ),
        (
            "SRC2106_04_2105_next",
            CSV_2105_NEXT,
            ["NEXT2105_0_2106", "2106-Y5-R2FR-ZX-MX2-parent-Hessian-source-row-or-no-pole-return.md"],
            "2105 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2106_05_2105_validation",
            CSV_2105_VAL,
            ["VAL2105_OVERALL", "PASS", "Z_X/M_X^2 parent Hessian next"],
            "2105 validation is clean and nonclaim.",
        ),
        (
            "SRC2106_06_1847_doc",
            SRC_1847_DOC,
            ["lambda_X=sqrt(Z_X/M_X^2)", "current MTS does not yet own", "PHA1847_8_verdict"],
            "1847 derives the exact relation but not ownership.",
        ),
        (
            "SRC2106_07_1847_hessian",
            CSV_1847_HESSIAN,
            ["PHA1847_1_ZX_positive", "PHA1847_2_MX2_positive", "PHA1847_8_verdict"],
            "1847 Hessian audit lists the missing claim-grade evidence.",
        ),
        (
            "SRC2106_08_1848_doc",
            SRC_1848_DOC,
            ["finite range route", "NOT_PARENT_SIGNED", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
            "1848 demotes the finite metric/eigenvalue route and returns to source-zero/bounded coupling.",
        ),
        (
            "SRC2106_09_1848_return",
            CSV_1848_SOURCE_ZERO,
            ["SZR1848_5_verdict", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW", "SZR1848_2_qbar_XT"],
            "1848 source-zero return row is the natural fallback if finite Hessian fails.",
        ),
        (
            "SRC2106_10_1854_doc",
            SRC_1854_DOC,
            ["NO_CLAIM_GRADE_ZX_OR_MX2_FOUND", "N_X=1/sqrt(Z_X)", "HCA1854_6_verdict"],
            "1854 extraction proves the corpus had formulae but not claim-grade inputs.",
        ),
        (
            "SRC2106_11_1854_result",
            CSV_1854_RESULT,
            ["EXT1854_0_ZX", "MISSING_ZX", "EXT1854_5_verdict"],
            "1854 machine-readable extraction result leaves Z_X and M_X^2 unextracted.",
        ),
        (
            "SRC2106_12_2023_schema",
            CSV_2023_SCHEMA,
            ["ZMR2023_3_ZX", "ZMR2023_4_MX2", "ZMR2023_10_acceptance"],
            "2023 provides a schema for future rows but no valid claim row.",
        ),
        (
            "SRC2106_13_2034_doc",
            SRC_2034_DOC,
            ["Row Null Hessian Gate", "HESS2034_6_verdict", "FAIL_MISSING_VALUES"],
            "2034 derives the row-null Hessian gate as an exact conditional route.",
        ),
        (
            "SRC2106_14_2034_hessian",
            CSV_2034_HESSIAN,
            ["HESS2034_1_row_null_law", "HESS2034_3_finite_Z_formula", "HESS2034_6_verdict"],
            "2034 row-null Hessian table gives finite-source formulas if factorisation fails.",
        ),
        (
            "SRC2106_15_2035_doc",
            SRC_2035_DOC,
            ["NO_VALID_SOURCE_ROW_FOUND", "DEC2035_2_finite_scan", "VAL2035_OVERALL"],
            "2035 scans for finite row-null source candidates and finds none.",
        ),
        (
            "SRC2106_16_2035_scan",
            CSV_2035_SCAN,
            ["Z_RR", "M_R^2", "0"],
            "2035 scan has zero valid finite Hessian/source candidates.",
        ),
        (
            "SRC2106_17_2035_requirements",
            CSV_2035_REQ,
            ["REQ2035_0_ZRR", "REQ2035_2_MR2", "REQ2035_6_no_cancellation"],
            "2035 requirements are the finite fallback rows if no-pole fails.",
        ),
        (
            "SRC2106_18_2035_decision",
            CSV_2035_DEC,
            ["DEC2035_0_exhaustion_result", "DEC2035_2_finite_scan", "DEC2035_3_best_next"],
            "2035 decision blocks exhaustion and says finite rows are still missing.",
        ),
        (
            "SRC2106_19_2035_validation",
            CSV_2035_VAL,
            ["VAL2035_OVERALL", "PASS", "quotient-factorisation exhaustion"],
            "2035 validation is clean and nonclaim.",
        ),
        (
            "SRC2106_20_2079_doc",
            SRC_2079_DOC,
            ["parent Hessian/gap owner remains missing", "STRICT_ROBIN_DEMOTED_FINITE_BRANCH_NEXT", "VAL2079_OVERALL"],
            "2079 confirms topology/floor shortcuts do not source the missing Hessian gap.",
        ),
        (
            "SRC2106_21_2079_hunt",
            CSV_2079_HUNT,
            ["KFS2079_1_parent_Hessian_gap", "MISSING_PARENT_HESSIAN_GAP_FOR_CAP", "KFS2079_3_constructor_exhaustion"],
            "2079 source hunt rejects the k-floor/Hessian shortcut.",
        ),
        (
            "SRC2106_22_2079_acq",
            CSV_2079_ACQ,
            ["ACQ2079_0_kfloor_min", "ACQ2079_1_cap_Hessian", "MISSING"],
            "2079 finite branch acquisition rows remain placeholders.",
        ),
        (
            "SRC2106_23_2079_validation",
            CSV_2079_VAL,
            ["VAL2079_OVERALL", "PASS", "parent Hessian/gap owner remains missing"],
            "2079 validation is clean and nonclaim.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2106_ZX_MX2_or_no_pole_return",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2106=use,
                valid_for_claim=False,
            )
        )
    return rows


def hessian_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "HSA2106_0_scalar_block",
            "finite scalar Hessian block",
            "S_X = 1/2 int sqrt(h)[Z_X |grad Xhat|^2 + M_X^2 Xhat^2] - int sqrt(h) Xhat J_X",
            "1847 derives relation; 1854 extraction fails",
            "FORMULA_DERIVED_NOT_OWNED",
            "Z_X/M_X^2 are not claim-grade inputs",
        ),
        (
            "HSA2106_1_ZX",
            "Z_X",
            "positive kinetic Hessian coefficient in the same Xhat normalization as c_g",
            "MISSING_ZX in 1854/2105; schema in 2023 only",
            "MISSING_PARENT_INPUT",
            "blocks N_X and alpha_eff",
        ),
        (
            "HSA2106_2_MX2",
            "M_X^2",
            "positive local Hessian curvature/mass gap in same Xhat normalization",
            "MISSING_MX2 in 1854/2105; relation only",
            "MISSING_PARENT_INPUT",
            "blocks lambda_X and range response",
        ),
        (
            "HSA2106_3_row_null",
            "row-null Hessian",
            "J_u^A Z_AB^{mu nu}=0 for every B,mu,nu under quotient factorisation",
            "2034 exact conditional law; 2035 exhaustion fails current proof",
            "CONDITIONAL_NOT_CURRENT",
            "no-pole route still strongest if parent action signs factorisation",
        ),
        (
            "HSA2106_4_finite_scan",
            "finite row-null fallback",
            "Z_RR, Z_RY, M_R^2, J_R, Q_R, B_R as finite source rows",
            "2035 scan found zero valid source rows",
            "NO_VALID_SOURCE_ROW_FOUND",
            "finite score cannot proceed",
        ),
        (
            "HSA2106_5_kfloor_shortcut",
            "topological/k-floor repair",
            "positive additive floor would rescue strict Robin activation",
            "2079 demotes strict Robin; kfloor/Hessian owner missing",
            "SHORTCUT_REJECTED",
            "does not supply Z_X/M_X^2",
        ),
        (
            "HSA2106_6_verdict",
            "Z_X/M_X^2 parent Hessian source row",
            "claim-grade finite Hessian route requires same-branch Z_X, M_X^2, cross-block silence, J_X/tails, units and source path",
            "current corpus has formulae and schemas but no valid row",
            "FAIL_CURRENT_CLAIM",
            "return to no-pole/source-zero certificate rather than finite c_g scoring",
        ),
    ]
    return [
        row(
            attempt_id=attempt_id,
            object=object_,
            formula_or_claim=formula,
            evidence=evidence,
            status=status,
            consequence=consequence,
            valid_for_claim=False,
        )
        for attempt_id, object_, formula, evidence, status, consequence in specs
    ]


def extraction_matrix_rows() -> list[dict[str, object]]:
    specs = [
        ("EXM2106_0_ZX", "Z_X", "MISSING_ZX", "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv:EXT1854_0_ZX", "kinetic Hessian coefficient not extracted", "finite c_g/alpha_eff blocked"),
        ("EXM2106_1_MX2", "M_X^2", "MISSING_MX2", "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv:EXT1854_1_MX2", "mass/range Hessian not extracted", "lambda_X and Y_gamma blocked"),
        ("EXM2106_2_NX", "N_X", "RELATION_ONLY", "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv:EXT1854_3_NX", "N_X=1/sqrt(Z_X) exists only as formula", "raw c_g cannot be bounded"),
        ("EXM2106_3_lambda_X", "lambda_X", "RELATION_ONLY", "1847/1854 relation rows", "lambda_X=sqrt(Z_X/M_X^2) but values/units missing", "PPN range response blocked"),
        ("EXM2106_4_ZRR", "Z_RR", "NO_VALID_SOURCE_ROW_FOUND", "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_SCAN.csv:Z_RR", "row-null finite fallback has zero valid candidates", "finite residual source blocked"),
        ("EXM2106_5_MR2", "M_R^2", "NO_VALID_SOURCE_ROW_FOUND", "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_SCAN.csv:M_R^2", "row-null mass fallback has zero valid candidates", "finite reciprocal pole blocked"),
        ("EXM2106_6_kfloor", "k_floor_min", "MISSING_PARENT_OWNER", "P8_Y5_PARENT_QLOC_2079_KFLOOR_SOURCE_ATTEMPTS.csv:KFS2079_1", "topological/floor shortcut fails", "strict Robin zero not available"),
    ]
    return [
        row(
            extraction_id=extraction_id,
            quantity=quantity,
            current_value=value,
            evidence_pointer=evidence,
            meaning=meaning,
            blocks=blocks,
            score_ready=False,
            valid_for_claim=False,
        )
        for extraction_id, quantity, value, evidence, meaning, blocks in specs
    ]


def no_pole_return_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NPR2106_0_reason",
            "finite Hessian route failed current claim",
            "Z_X/M_X^2, row-null finite source rows and kfloor shortcuts are all missing or nonclaim",
            "return to structural no-pole/source-zero route",
            "SELECTED",
        ),
        (
            "NPR2106_1_no_pole_route",
            "no physical X pole",
            "prove parent quotient/action factorisation so the dangerous X direction is representative/gauge data, not a local propagating pole",
            "would remove need for finite c_g/R10/PPN scoring of X pole",
            "BEST_GR_LIKE_ROUTE",
        ),
        (
            "NPR2106_2_source_zero_route",
            "J_X/qbar_XT=0",
            "prove ordinary matter/readout/source/boundary channels descend so the X source vanishes",
            "would silence coupling without tuning tiny coefficients",
            "PARALLEL_ROUTE",
        ),
        (
            "NPR2106_3_required_certificate",
            "parent no-pole/source-zero certificate",
            "must include q-map, field-by-field v_X action, action descent, matter/no-marker descent, boundary silence, degree count and no hidden tails",
            "single certificate should replace isolated partial wins",
            "NEXT_INPUT_CONTRACT",
        ),
        (
            "NPR2106_4_fallback_if_fails",
            "finite residual retention",
            "if no-pole/source-zero fails again, retain finite rows as explicit nonclaim source acquisition: Z_X/M_X^2/J_X/Qbar/K_X/qbar/tails",
            "no local-GR claim until source rows are real",
            "NONCLAIM_FALLBACK",
        ),
    ]
    return [
        row(
            return_id=return_id,
            route=route,
            statement=statement,
            consequence=consequence,
            status=status,
            valid_for_claim=False,
        )
        for return_id, route, statement, consequence, status in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2106_0_hessian_formula", "Z_X/M_X^2 relation/formula exists", True, "1847/1854 supply exact formulae and contracts"),
        ("GATE2106_1_ZX_value", "claim-grade Z_X exists", False, "Z_X remains MISSING_ZX"),
        ("GATE2106_2_MX2_value", "claim-grade M_X^2 exists", False, "M_X^2 remains MISSING_MX2"),
        ("GATE2106_3_row_null_finite", "row-null finite fallback has valid source rows", False, "2035 scan finds zero valid candidates"),
        ("GATE2106_4_kfloor_shortcut", "kfloor/topological Hessian shortcut closes", False, "2079 rejects topology/floor shortcut as parent owner"),
        ("GATE2106_5_finite_cg_score", "finite c_g->PPN/R10 score can proceed", False, "canonical normalization and range response remain missing"),
        ("GATE2106_6_no_pole_return", "no-pole/source-zero route selected as next", True, "finite Hessian route is blocked; structural route is least tuning-heavy"),
        ("GATE2106_7_local_GR", "derived local GR/Newton reduction follows", False, "next certificate still must be proven"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2106_0_hessian_result",
            "NO_CLAIM_GRADE_ZX_MX2_SOURCE_ROW_FOUND",
            "The exact Hessian/range algebra is present, but every source check leaves Z_X/M_X^2 relation-only or missing.",
            "finite c_g scoring remains blocked",
        ),
        (
            "DEC2106_1_no_pole_return",
            "RETURN_TO_NO_POLE_SOURCE_ZERO_CERTIFICATE",
            "A derived GR-like local limit should remove the extra pole/source structurally instead of fitting a tiny finite coupling.",
            "build one consolidated certificate from q-map/action descent/matter descent/boundary silence/degree count",
        ),
        (
            "DEC2106_2_fallback_policy",
            "FINITE_BRANCH_RETAINED_ONLY_AS_NONCLAIM_ACQUISITION",
            "If the structural certificate fails, finite rows must be source-backed and absolute-summed before any empirical score.",
            "do not delete finite branch, but do not score it yet",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2106_0_2107",
            next_target="2107-Y5-R2FR-consolidated-no-pole-source-zero-certificate-or-finite-residual-retention.md",
            script="scripts/Y5_R2FR_consolidated_no_pole_source_zero_certificate_or_finite_residual_retention_2107.py",
            objective="Build the consolidated no-pole/source-zero certificate: q-map, field-by-field v_X action, action descent, matter/no-marker descent, boundary silence, degree count, and hidden-tail silence; if any clause fails, retain finite residual rows explicitly.",
            forbidden_shortcuts="quotient by notation; WEP-only source zero; covariance-only source zero; invented Z_X/M_X^2; local-GR claim from conditional no-pole; cancellation against finite tails",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    attempts: list[dict[str, object]],
    extraction: list[dict[str, object]],
    no_pole: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2106_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_ZX_MX2_HESSIAN_2106_NONCLAIM.csv",
            attempts + extraction + decisions,
        ),
        (
            "COPY2106_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2106_ZX_MX2_STATUS_NONCLAIM.csv",
            extraction + no_pole,
        ),
        (
            "COPY2106_2_acquisition_queue",
            QUEUE / "JR2106_NO_POLE_SOURCE_ZERO_CERTIFICATE_QUEUE.csv",
            no_pole + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    extraction: list[dict[str, object]],
    no_pole: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    attempts_ok = any(row_.get("attempt_id") == "HSA2106_6_verdict" and row_.get("status") == "FAIL_CURRENT_CLAIM" for row_ in attempts)
    extraction_ok = any(row_.get("extraction_id") == "EXM2106_0_ZX" and row_.get("current_value") == "MISSING_ZX" for row_ in extraction) and any(row_.get("extraction_id") == "EXM2106_4_ZRR" and row_.get("current_value") == "NO_VALID_SOURCE_ROW_FOUND" for row_ in extraction)
    no_pole_ok = any(row_.get("return_id") == "NPR2106_1_no_pole_route" and row_.get("status") == "BEST_GR_LIKE_ROUTE" for row_ in no_pole)
    gates_ok = all(not truthy(row_.get("claim_allowed")) for row_ in gates) and any(not truthy(row_.get("gate_pass")) for row_ in gates)
    decision_ok = any(row_.get("decision") == "RETURN_TO_NO_POLE_SOURCE_ZERO_CERTIFICATE" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2106_0_2107" and "2107-Y5-R2FR" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, attempts, extraction, no_pole, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2106_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2106_00_sources", sources_ok, "2105 plus Hessian/no-pole source paths exist with required needles"),
        ("VAL2106_01_hessian_attempt", attempts_ok, "Z_X/M_X^2 source-row attempt fails current claim honestly"),
        ("VAL2106_02_extraction", extraction_ok, "extraction matrix records missing Z_X and zero valid finite row-null candidates"),
        ("VAL2106_03_no_pole_return", no_pole_ok, "no-pole/source-zero route is selected as the next GR-like route"),
        ("VAL2106_04_claim_gates", gates_ok, "claim gates block finite c_g score and local-GR promotion"),
        ("VAL2106_05_decision", decision_ok, "decision returns to no-pole/source-zero certificate"),
        ("VAL2106_06_next", next_ok, "next target is 2107 consolidated no-pole/source-zero certificate"),
        ("VAL2106_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2106_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2106_09_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2106_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2106"),
        ("VAL2106_11_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2106_OVERALL",
            overall,
            "2106 rejects finite Z_X/M_X^2 scoring from current evidence and returns to no-pole/source-zero certificate work",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    extraction: list[dict[str, object]],
    no_pole: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2106 - Y5/R2FR Z_X/M_X2 Parent Hessian Source Row Or No-Pole Return",
        "",
        "## Current Verdict",
        "",
        "2106 tries the finite Hessian route honestly and rejects it for current-claim use. The corpus has the right equations: `N_X=1/sqrt(Z_X)` and `lambda_X=sqrt(Z_X/M_X^2)`. But it still has no claim-grade same-branch `Z_X`, `M_X^2`, row-null finite source row, or topological/k-floor Hessian owner.",
        "",
        "That means the finite `c_g -> PPN/R10` branch remains a nonclaim acquisition branch. The best GR-like route is now structural: prove no physical X pole/source in the local branch by a consolidated no-pole/source-zero certificate, rather than fitting a small finite coupling.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2106", "valid_for_claim"]),
        "## Hessian Source Attempt",
        md_table(attempts, ["attempt_id", "object", "status", "formula_or_claim", "evidence", "consequence", "valid_for_claim"]),
        "## Extraction Matrix",
        md_table(extraction, ["extraction_id", "quantity", "current_value", "evidence_pointer", "meaning", "blocks", "score_ready", "valid_for_claim"]),
        "## No-Pole Return Ledger",
        md_table(no_pole, ["return_id", "route", "status", "statement", "consequence", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    attempts = hessian_attempt_rows()
    extraction = extraction_matrix_rows()
    no_pole = no_pole_return_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2106_SOURCE_REGISTER.csv",
        "attempts": OUT / "P8_Y5_PARENT_QLOC_2106_HESSIAN_SOURCE_ATTEMPT.csv",
        "extraction": OUT / "P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv",
        "no_pole": OUT / "P8_Y5_PARENT_QLOC_2106_NO_POLE_RETURN_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2106_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2106_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2106_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2106_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2106_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["attempts"], attempts)
    write_csv(paths["extraction"], extraction)
    write_csv(paths["no_pole"], no_pole)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(attempts, extraction, no_pole, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, attempts, extraction, no_pole, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, attempts, extraction, no_pole, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
