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
    read_csv,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2095-Y5-R2FR-ZR-MR2-operator-signature-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2094 = ROOT / "2094-Y5-R2FR-first-finite-local-input-source-row-qR-or-ZR.md"
SRC_2034 = ROOT / "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md"
SRC_2035 = ROOT / "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md"
SRC_1025 = ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
SRC_1577 = ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md"
SCAN_2035 = OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_SCAN.csv"
REQ_2035 = OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_REQUIREMENTS.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def formalization_has_2095_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2095-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2095*",
        "*Y5_R2FR_ZR_MR2_operator_signature_source_row_2095*",
        "*AFRAME_ZR_MR2_OPERATOR_SIGNATURE_2095*",
        "*JR2095_SR_JR_SOURCE_MAP_NEXT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2095_00_2094_handoff",
            SRC_2094,
            ["NEXT2094_0_2095", "MOVE_TO_ZR_MR2_OPERATOR_SIGNATURE", "VAL2094_OVERALL"],
            "2094 selects Z_R/M_R^2 after q_R_hat theorem-zero and prediction rows remain blocked.",
        ),
        (
            "SRC2095_01_2034_row_null",
            SRC_2034,
            ["HESS2034_1_row_null_law", "FZ2034_2_MR2", "VAL2034_OVERALL"],
            "2034 derives the row-null Hessian gate and finite Z/M source formulas as nonclaim.",
        ),
        (
            "SRC2095_02_2035_exhaustion",
            SRC_2035,
            ["EXH2035_8_verdict", "REQ2035_2_MR2", "VAL2035_OVERALL"],
            "2035 rejects current quotient-factorisation exhaustion and requires finite row-null sources.",
        ),
        (
            "SRC2095_03_1025_hessian",
            SRC_1025,
            ["SV1025_2_Hessian_signs", "SV1025_3_range_relation", "V1025_SUMMARY"],
            "1025 gives the generic second-variation/range contract and blocks Hessian ownership.",
        ),
        (
            "SRC2095_04_1577_operator",
            SRC_1577,
            ["FCF1577_1_operator", "MISSING_OPERATOR_SIGNATURE", "VAL1577_OVERALL"],
            "1577 keeps Z_R/M_R^2 as a finite operator input requiring parent kinetic/Hessian evidence.",
        ),
        (
            "SRC2095_05_2035_scan",
            SCAN_2035,
            ["Z_R", "M_R^2", "NO_VALID_SOURCE_ROW_FOUND"],
            "2035 scan found no valid source rows for Z_R, M_R^2, or row-null Hessian components.",
        ),
        (
            "SRC2095_06_2035_requirements",
            REQ_2035,
            ["REQ2035_0_ZRR", "REQ2035_1_ZRY", "REQ2035_2_MR2"],
            "2035 finite source requirements define the exact rows needed for operator scoring.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2095_ZR_MR2_operator_signature",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2095=note,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def operator_signature_rows() -> list[dict[str, object]]:
    return [
        row(
            operator_id="OP2095_0_static_operator",
            object="radial finite operator",
            formula="O_R u = -nabla_i(Z_R^{ij} nabla_j u)+M_R^2 u",
            status="FORMAL_OPERATOR_TEMPLATE",
            required_parent_input="parent second variation in u=R_AB or primitive row-null coordinates",
            current_result="template only; no signed Z_R/M_R^2 values",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            operator_id="OP2095_1_row_null_zero",
            object="exact no-pole route",
            formula="J_u^A Z_AB^{mu nu}=0 for every B,mu,nu",
            status="EXACT_ZERO_CONDITION_IF_FACTORISED",
            required_parent_input="quotient factorisation: no u or D_mu u in L_phys, matter, or boundary except parent-owned Lambda_R u",
            current_result="not parent-signed; cannot spend zero theorem credit",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            operator_id="OP2095_2_scalar_projection_guard",
            object="scalar Z_R guard",
            formula="Z_RR=J_u^A Z_AB J_u^B is insufficient if Z_RY=J_u^A Z_AB J_Y^B survives",
            status="SCRUTINY_GUARD_ACTIVE",
            required_parent_input="full row-null tensor or cross-coupling source rows, not scalar projection alone",
            current_result="prevents false finite-Z shortcut",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            operator_id="OP2095_3_finite_range",
            object="finite residual range",
            formula="lambda_R=sqrt(Z_R/M_R^2) when Z_R and M_R^2 are positive and same-normalized",
            status="RELATION_EXACT_VALUES_MISSING",
            required_parent_input="same-branch kinetic residue, mass Hessian, units, cross-Hessian policy",
            current_result="no lambda_R claim or R10/PPN score allowed",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            operator_id="OP2095_4_positive_nohair",
            object="source-free finite operator theorem",
            formula="int[Z_R|grad u|^2+M_R^2 u^2]=int u J_R + boundary",
            status="CONDITIONAL_THEOREM_ONLY",
            required_parent_input="Z_R>0, M_R^2>0, J_R=0, boundary flux=0 and self-adjoint domain",
            current_result="signs, source and boundary clauses are missing",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            operator_id="OP2095_5_verdict",
            object="Z_R/M_R^2 operator signature",
            formula="operator row is either theorem-zero by row-null Hessian or finite by sourced Z/M coefficients",
            status="OPERATOR_SIGNATURE_BLOCKED_NO_VALID_ZR_MR2_ROW",
            required_parent_input="parent Hessian tensor or signed absence theorem",
            current_result="no source-backed or theorem-zero operator input row found",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def scan_review_rows() -> list[dict[str, object]]:
    scan_rows = safe_read_csv(SCAN_2035)
    wanted = {"Z_RR", "Z_RY", "Z_R", "M_R^2"}
    reviewed: list[dict[str, object]] = []
    for scan_row in scan_rows:
        symbol = scan_row.get("symbol", "")
        if symbol not in wanted:
            continue
        reviewed.append(
            row(
                review_id=f"SCAN2095_{symbol.replace('^', '').replace('_', '').replace(' ', '')}",
                symbol=symbol,
                valid_candidate_count=scan_row.get("valid_candidate_count", ""),
                nonclaim_reference_count=scan_row.get("nonclaim_reference_count", ""),
                valid_candidate_paths=scan_row.get("valid_candidate_paths", ""),
                source_status=scan_row.get("status", ""),
                accepted_for_operator_signature=False,
                score_ready=False,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    if not reviewed:
        reviewed.append(
            row(
                review_id="SCAN2095_missing",
                symbol="Z_R/M_R2",
                valid_candidate_count="0",
                nonclaim_reference_count="0",
                valid_candidate_paths="",
                source_status="SCAN_ROWS_MISSING",
                accepted_for_operator_signature=False,
                score_ready=False,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return reviewed


def finite_input_rows() -> list[dict[str, object]]:
    requirements = {
        "ZRI2095_0_ZRR": ("Z_RR^{mu nu}", "parent kinetic Hessian projected by J_u^A J_u^B", "numeric tensor or theorem-zero row with source path and units"),
        "ZRI2095_1_ZRY": ("Z_RY^{mu nu}", "cross kinetic row-null failure", "numeric cross tensor or theorem-zero row; scalar projection alone is insufficient"),
        "ZRI2095_2_MR2": ("M_R^2", "parent Hessian/effective mass for u", "numeric mass scale or signed absence theorem"),
        "ZRI2095_3_units": ("Z_R/M_R^2 units", "same-normalized lambda_R=sqrt(Z_R/M_R^2)", "field units, coordinate units, and normalization convention"),
        "ZRI2095_4_source_boundary": ("J_R and boundary flux", "source and boundary terms in finite operator identity", "theorem-zero or absolute finite rows"),
    }
    return [
        row(
            input_id=input_id,
            quantity=quantity,
            role=role,
            acceptance_requirement=requirement,
            current_status="SOURCE_REQUIRED_NONCLAIM",
            parent_signed=False,
            numeric_value_present=False,
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for input_id, (quantity, role, requirement) in requirements.items()
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        (
            "GATE2095_0_row_null_zero",
            "row-null Hessian proves no radial operator",
            "FAIL_UNSIGNED",
            "factorisation/exhaustion is not parent-signed",
        ),
        (
            "GATE2095_1_finite_ZM",
            "finite Z_R/M_R^2 operator values are sourced",
            "FAIL_MISSING_VALUES",
            "2035 scan found no valid source rows for Z_RR/Z_RY/Z_R/M_R^2",
        ),
        (
            "GATE2095_2_positive_nohair",
            "positive finite operator implies local silence",
            "FAIL_BLOCKED",
            "Z_R, M_R^2, J_R, boundary flux and domain are not all signed",
        ),
        (
            "GATE2095_3_lambda_R",
            "lambda_R is claim-grade",
            "FAIL_BLOCKED",
            "same-branch values and units are missing",
        ),
        (
            "GATE2095_4_local_tests",
            "R10/PPN/clock/orbital scores are allowed",
            "FAIL_BLOCKED",
            "operator, source, boundary, q_R/Q_R and arena projections remain incomplete",
        ),
    ]
    return [
        row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2095_0_operator_contract",
            decision="ROW_NULL_HESSIAN_CONTRACT_IS_THE_OPERATOR_SIGNATURE",
            basis="2034 shows the exact zero route is J_u^A Z_AB=0, while finite leakage requires Z_RR/Z_RY/M_R2 rows.",
            consequence="do not use scalar Z_R alone as proof; row-null cross terms matter.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2095_1_source_status",
            decision="NO_VALID_ZR_MR2_SOURCE_ROW_FOUND",
            basis="2035 finite scan reports zero valid candidates for Z_RR, Z_RY, Z_R and M_R^2.",
            consequence="no lambda_R, R10, PPN, clock, orbital or local-GR score can be run from this branch.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2095_2_not_circling",
            decision="DO_NOT_REPEAT_OPERATOR_SOURCE_SCAN_WITHOUT_NEW_PARENT_INPUT",
            basis="the missing object is not another wording pass; it is a parent Hessian/generator certificate or finite coefficient source.",
            consequence="move to the source-map/coupling row S_R/J_R, where the micro-kernel equation actually couples to matter/readout.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2095_3_next",
            decision="MOVE_TO_SR_JR_SOURCE_MAP_SILENCE_OR_FINITE_COUPLING_ROW",
            basis="q_R/Q_R and Z_R/M_R^2 are both blocked as prediction inputs; the next independent finite input is the source side S_R/J_R.",
            consequence="2096 should derive, source, or fail S_R/J_R source silence and finite coupling coefficients.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2095_0_2096",
            target_doc="2096-Y5-R2FR-SR-JR-source-map-silence-or-finite-coupling-row.md",
            target_script="scripts/Y5_R2FR_SR_JR_source_map_silence_or_finite_coupling_row_2096.py",
            objective="derive, source, or explicitly fail the S_R/J_R source-map input in C_R'=S_R: source silence, matter/readout descent, or finite coupling coefficient rows",
            success_condition="S_R/J_R becomes parent-signed zero/source-backed finite row, or is blocked with exact missing matter/source/readout inputs; no local-test score without q_R/Q_R, Z_R/M_R^2, boundary and arena rows",
            forbidden_shortcuts="source-free by assertion; WEP-only coupling silence; cancellation against q_R or boundary tails; importing GR source equation; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    operators: list[dict[str, object]],
    scans: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_ZR_MR2_OPERATOR_SIGNATURE_2095_NONCLAIM.csv",
            operators + scans + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2095_ZR_MR2_GATE_NONCLAIM.csv",
            operators + inputs + gates,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2095_SR_JR_SOURCE_MAP_NEXT_QUEUE.csv",
            inputs + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2095_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    operators: list[dict[str, object]],
    scans: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    row_null_ok = any(r["operator_id"] == "OP2095_1_row_null_zero" and r["status"] == "EXACT_ZERO_CONDITION_IF_FACTORISED" for r in operators)
    verdict_ok = any(r["operator_id"] == "OP2095_5_verdict" and r["status"] == "OPERATOR_SIGNATURE_BLOCKED_NO_VALID_ZR_MR2_ROW" for r in operators)
    scan_ok = all(str(r["source_status"]) == "NO_VALID_SOURCE_ROW_FOUND" and str(r["valid_candidate_count"]) == "0" for r in scans)
    inputs_blocked = all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in inputs)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and any(
        r["gate_id"] == "GATE2095_1_finite_ZM" and r["status"] == "FAIL_MISSING_VALUES" for r in gates
    )
    decision_ok = any(r["decision_id"] == "DEC2095_3_next" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2095_0_2096"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, operators, scans, inputs, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2095_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2095_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2095_01_row_null", row_null_ok, "row-null Hessian exact zero condition is recorded"),
        ("VAL2095_02_operator_verdict", verdict_ok, "operator signature remains blocked without valid Z/M row"),
        ("VAL2095_03_scan", scan_ok, "Z_RR/Z_RY/Z_R/M_R2 scan rows report no valid source candidates"),
        ("VAL2095_04_inputs_blocked", inputs_blocked, "finite operator input rows are not source-backed or score-ready"),
        ("VAL2095_05_claim_gates", gates_safe, "claim gates block finite operator/local-test claims"),
        ("VAL2095_06_decision", decision_ok, "decision moves next to S_R/J_R source-map coupling row"),
        ("VAL2095_07_next", next_ok, "next target is 2096 S_R/J_R source map"),
        ("VAL2095_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2095_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2095_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2095_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2095"),
        ("VAL2095_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, claim_allowed=False, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2095_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2095 records the Z_R/M_R^2 operator signature as row-null Hessian or finite source row, finds no valid source row, and pivots to S_R/J_R source-map coupling" if overall else "one or more 2095 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    operators: list[dict[str, object]],
    scans: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2095 - Y5/R2FR ZR/MR2 Operator Signature Source Row",
            "## Current Verdict\n\n2095 locks the radial operator fork without pretending it is solved. The exact zero route is not a scalar `Z_R=0` slogan; it is the row-null Hessian condition `J_u^A Z_AB^{mu nu}=0` for every parent direction. If that fails, the finite branch needs sourced `Z_RR`, `Z_RY`, `M_R^2`, units, source, boundary and arena rows.\n\nThe current corpus gives the formulas, not the parent coefficients. The 2035 scan finds zero valid source candidates for `Z_RR`, `Z_RY`, `Z_R`, and `M_R^2`, so no `lambda_R`, no R10/PPN/clock/orbital score, and no local-GR claim is allowed from this branch. Rather than circling the operator again, the next independent input is the source side of the micro-kernel: `S_R/J_R`.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2095", "claim_allowed", "valid_for_claim"]),
            "## Operator Signature Gate",
            md_table(operators, ["operator_id", "object", "formula", "status", "required_parent_input", "current_result", "claim_allowed", "valid_for_claim"]),
            "## Finite Source Scan Review",
            md_table(scans, ["review_id", "symbol", "valid_candidate_count", "nonclaim_reference_count", "valid_candidate_paths", "source_status", "accepted_for_operator_signature", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Finite Operator Input Rows",
            md_table(inputs, ["input_id", "quantity", "role", "acceptance_requirement", "current_status", "parent_signed", "numeric_value_present", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "status", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "copy_kind", "path", "rows", "parses", "claim_allowed", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    operators = operator_signature_rows()
    scans = scan_review_rows()
    inputs = finite_input_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2095_SOURCE_REGISTER.csv",
        "operators": OUT / "P8_Y5_PARENT_QLOC_2095_OPERATOR_SIGNATURE_GATE.csv",
        "scans": OUT / "P8_Y5_PARENT_QLOC_2095_FINITE_SOURCE_SCAN_REVIEW.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2095_FINITE_OPERATOR_INPUT_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2095_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2095_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2095_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2095_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2095_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["operators"], operators)
    write_csv(paths["scans"], scans)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(operators, scans, inputs, gates, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, operators, scans, inputs, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, operators, scans, inputs, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
