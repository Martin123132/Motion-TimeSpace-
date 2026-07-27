from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2202"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2202-Y5-R2FR-alpha-cg-projection-clause-or-readout-zero-theorem.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2202_SOURCE_REGISTER.csv",
    "alpha_projection_attempt": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_PROJECTION_ATTEMPT.csv",
    "alpha_effective_row": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW.csv",
    "readout_zero_attempt": OUT / "P8_Y5_PARENT_QLOC_2202_READOUT_ZERO_THEOREM_ATTEMPT.csv",
    "route_selection": OUT / "P8_Y5_PARENT_QLOC_2202_ROUTE_SELECTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2202_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2202_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2202_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2202_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2202_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2202_ALPHA_CG_BLOCKED_READOUT_NEXT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_READOUT_ZERO_THEOREM_ATTEMPT_2202_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2202_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2202-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2202*",
        "*P8_Y5_BRR545_2202*",
        "*Y5_R2FR_alpha_cg_projection_clause_or_readout_zero_theorem_2202*",
        "*JR2202*",
        "*PARENT_QLOC_READOUT_ZERO_THEOREM_ATTEMPT_2202*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2201_doc",
            ROOT / "2201-Y5-R2FR-PPN-component-owner-matrix-or-alpha-cg-source-row.md",
            ["NEXT2201_0_2202", "ACG2201_6_verdict", "VAL2201_OVERALL"],
            "2201 handoff into alpha_cg projection or readout zero theorem.",
        ),
        (
            "2201_next",
            OUT / "P8_Y5_PARENT_QLOC_2201_NEXT_TARGET.csv",
            ["NEXT2201_0_2202", "do not set tau_PPN or S_PPN to one", "do not cancel vector components"],
            "Machine-readable 2202 target.",
        ),
        (
            "2201_alpha_gate",
            OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_PROJECTION_GATE.csv",
            ["ACG2201_2_normalization", "ACG2201_4_tau_PPN", "ACG2201_6_verdict"],
            "Alpha_cg gate clauses to be tested.",
        ),
        (
            "1853_doc",
            ROOT / "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md",
            ["FORMULA_DERIVED_INPUTS_MISSING", "MISSING_ZX;MISSING_TAU_PPN", "VAL1853_OVERALL"],
            "Canonical normalization and range law: exact conditional, missing inputs.",
        ),
        (
            "1854_doc",
            ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
            ["NO_CLAIM_GRADE_ZX_OR_MX2_FOUND", "EXT1854_0_ZX", "VAL1854_OVERALL"],
            "Parent Hessian scan: Z_X/M_X^2 not extracted.",
        ),
        (
            "2162_doc",
            ROOT / "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md",
            ["PVF2162_0_cg", "constraint/auxiliary route selected", "VAL2162_OVERALL"],
            "Confirms physical scalar route is closure/backstop; finite PPN vector remains nonclaim.",
        ),
        (
            "1012_doc",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["measured-GM/source-normalization ownership is not derived", "CG1012_0_Y5_owner", "DEC1012_0_owner_not_proved"],
            "Measured-GM/readout/source-normalization obstruction relevant to readout route.",
        ),
        (
            "2200_vector_source",
            OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
            ["PVS2200_2_vector_contract", "NONCLAIM_VECTOR_TARGET", "0.005788015401465051"],
            "Cassini vector source ceiling carried into alpha_cg effective row.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def alpha_projection_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="APA2202_0_common_frame",
            clause="universal common matter frame",
            required_statement="ordinary matter sees one A_g(Xhat)^2 g_E frame at Cassini order",
            current_evidence="2201 marks NOT_PARENT_SIGNED; no new parent matter-frame theorem found",
            status="NOT_DERIVED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_1_same_branch",
            clause="same-branch owner",
            required_statement="one Xhat owns c_g, Z_X, M_X^2, lambda_X, tau_PPN, source and readout terms",
            current_evidence="1854 and 2162 keep Xhat/Z_X/M_X^2 owner as closure/backstop only",
            status="MISSING_PARENT_OWNER",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_2_ZX",
            clause="canonical normalization",
            required_statement="Z_X is parent-owned, positive, unit-fixed and same-branch",
            current_evidence="1854 finds formula rows but no claim-grade Z_X",
            status="MISSING_ZX",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_3_lambda_SPPN",
            clause="range/screening transfer",
            required_statement="lambda_X=sqrt(Z_X/M_X^2) and S_PPN(lambda_X,env) route Cassini response",
            current_evidence="1853 derives range law conditionally; 1854 finds M_X^2 missing",
            status="MISSING_LAMBDA_X_AND_S_PPN",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_4_tau_PPN",
            clause="PPN projection coefficient",
            required_statement="tau_PPN maps the parent residual to gamma/Shapiro readout in observed frame",
            current_evidence="1852/1853 require tau_PPN; no parent source row exists",
            status="MISSING_TAU_PPN",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_5_vector_tails",
            clause="other PPN vector tails",
            required_statement="disformal, non-Hilbert, support/domain, boundary, and readout tails are theorem-zero or separately bounded",
            current_evidence="2200/2201 retain all tails in absolute vector; readout route unsigned",
            status="VECTOR_TAILS_UNCONTROLLED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="APA2202_6_verdict",
            clause="alpha_cg projection clause",
            required_statement="APA2202_0 through APA2202_5 all pass",
            current_evidence="every necessary clause remains missing or unsigned",
            status="ALPHA_CG_PROJECTION_NOT_DERIVED",
            blocks_prediction=True,
        ),
    ]


def alpha_effective_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="AER2202_0_effective_target",
            object="alpha_cg_eff",
            formula="tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            source_ceiling="abs(alpha_cg_eff) <= 0.005788015401465051",
            source_basis="Cassini gamma proxy carried through 2200/2201",
            prediction_value="MISSING_ZX_LAMBDA_TAU_SPPN",
            units="dimensionless",
            status="SOURCE_BACKED_TARGET_NOT_PREDICTION",
            score_ready=False,
            issue="target exists; MTS value does not",
        ),
        base_row(
            row_id="AER2202_1_raw_cg",
            object="raw_c_g",
            formula="c_g alone",
            source_ceiling="none",
            source_basis="raw c_g excluded by normalization guard",
            prediction_value="REFUSED",
            units="per_Xhat_convention",
            status="NOT_INVARIANT_NOT_SCOREABLE",
            score_ready=False,
            issue="field rescaling changes raw c_g",
        ),
    ]


def readout_zero_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="RZT2202_0_target",
            theorem_piece="fixed-before-readout PPN functor",
            statement="observed gamma, measured GM, clocks and source normalization are fixed functors of parent variables before fitting local-test residuals",
            current_status="TARGET_SHARP",
            obstruction="no parent readout functor certificate",
            effect_if_signed="could remove alpha_readout as an adjustable residual tail",
        ),
        base_row(
            theorem_id="RZT2202_1_variation_order",
            theorem_piece="variation before readout",
            statement="Hilbert/source variations are evaluated at fixed parent fields before projection to measured GM/gamma",
            current_status="CONDITIONAL_NOT_SIGNED",
            obstruction="post-variation projector/readout terms can regenerate residuals",
            effect_if_signed="prevents readout from hiding or cancelling alpha_cg",
        ),
        base_row(
            theorem_id="RZT2202_2_measured_GM",
            theorem_piece="measured-GM/source normalization owner",
            statement="Pi_M J_H flux/source-measure map is parent-owned and cannot be tuned after orbital/PPN readout",
            current_status="NOT_DERIVED",
            obstruction="1012/1013 measured-GM owner/flux closure remains unsigned",
            effect_if_signed="reopens Newton/GR source-normalization route",
        ),
        base_row(
            theorem_id="RZT2202_3_no_absorption",
            theorem_piece="no post-fit absorption",
            statement="readout/calibration constants are fixed before Cassini/GM data and cannot cancel alpha_cg or other vector components",
            current_status="GUARD_NEEDED_NOT_DERIVED",
            obstruction="fixed-before-readout certificate missing",
            effect_if_signed="protects no-cancellation vector scoring",
        ),
        base_row(
            theorem_id="RZT2202_4_verdict",
            theorem_piece="readout zero theorem",
            statement="RZT2202_0 through RZT2202_3 all pass",
            current_status="READOUT_ZERO_THEOREM_NOT_DERIVED",
            obstruction="measured-GM/readout functor and flux closure are unsigned",
            effect_if_signed="best next clean route toward Newton/GR reduction",
        ),
    ]


def route_selection_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="SEL2202_0_alpha_cg",
            route="continue alpha_cg projection",
            selection_status="blocked_for_now",
            reason="Z_X/M_X^2/tau_PPN/S_PPN have repeatedly failed as sourced parent inputs",
            next_use="return only if parent action supplies Z_X/lambda/tau or a theorem-zero route",
        ),
        base_row(
            route_id="SEL2202_1_readout",
            route="fixed-before-readout zero theorem",
            selection_status="selected_next",
            reason="readout/source-normalization is closer to GR/Newton reduction and can stop calibration from hiding vector tails",
            next_use="build the parent observed-metric/measured-GM functor contract",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2202_0_alpha_target",
            gate="alpha_cg source target exists",
            status="PASS_NONCLAIM",
            implication="Cassini ceiling is carried as a target, not as an MTS prediction.",
        ),
        base_row(
            gate_id="CG2202_1_alpha_prediction",
            gate="alpha_cg prediction is score-ready",
            status="BLOCKED_NONCLAIM",
            implication="Z_X, lambda_X/S_PPN, tau_PPN, common frame and vector tails are not signed.",
        ),
        base_row(
            gate_id="CG2202_2_readout_zero",
            gate="readout tail theorem-zero",
            status="BLOCKED_NONCLAIM",
            implication="fixed-before-readout and measured-GM/source-normalization functor are not derived.",
        ),
        base_row(
            gate_id="CG2202_3_raw_cg",
            gate="raw c_g bound",
            status="BLOCKED_NONCLAIM",
            implication="raw c_g remains non-invariant and excluded.",
        ),
        base_row(
            gate_id="CG2202_4_local_gr_newton",
            gate="local GR/Newton recovery claim",
            status="BLOCKED_NONCLAIM",
            implication="no PPN/local-GR/Newton, WEP, R10, clock, orbital or public claim follows from 2202.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2202_0_alpha_result",
            decision="ALPHA_CG_PROJECTION_NOT_DERIVED",
            rationale="the source ceiling is real, but every projection/owner clause needed to turn it into a prediction is still missing.",
            next_action="do not loop raw c_g; keep alpha_cg as nonclaim target row",
        ),
        base_row(
            decision_id="DEC2202_1_readout_result",
            decision="READOUT_ZERO_THEOREM_NOT_DERIVED_BUT_BEST_NEXT",
            rationale="fixed-before-readout is unsigned, but it attacks measured-GM/source-normalization and GR/Newton recovery more directly than another Z_X pass.",
            next_action="build the observed-metric/measured-GM readout functor contract",
        ),
        base_row(
            decision_id="DEC2202_2_next",
            decision="MOVE_TO_FIXED_BEFORE_READOUT_PPN_MAP",
            rationale="alpha_cg is blocked on old missing parent Hessian/projection inputs; readout functor is the next clean route.",
            next_action="2203 should derive or reject the fixed-before-readout PPN map and measured-GM obstruction row",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2202_0_2203",
            selection_status="selected",
            target_file="2203-Y5-R2FR-fixed-before-readout-PPN-map-or-measured-GM-obstruction-row.md",
            target_script="scripts/Y5_R2FR_fixed_before_readout_PPN_map_or_measured_GM_obstruction_row_2203.py",
            objective="derive the fixed-before-readout map from parent metric/source variables to observed gamma and measured GM, or stage the measured-GM/readout obstruction vector as nonclaim",
            success_condition="alpha_readout becomes theorem-zero conditional with fixed functor clauses, or measured-GM/readout obstruction rows become explicit nonclaim source fields",
            do_not_do="do not absorb residuals into fitted GM/gamma calibration, do not claim local GR, do not cancel alpha_cg with readout, do not use raw c_g",
        )
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["route_selection"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["alpha_effective_row"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["readout_zero_attempt"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        parse_ok, row_count, parse_detail = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=target.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    alpha_attempt_rows: list[dict[str, Any]],
    alpha_effective_rows_data: list[dict[str, Any]],
    readout_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail))

    add("VAL2202_00_sources_exist", all(truthy(r["path_exists"]) for r in source_rows), f"{sum(truthy(r['path_exists']) for r in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2202_01_needles_found", all(truthy(r["needles_found"]) for r in source_rows), f"{sum(truthy(r['needles_found']) for r in source_rows)}/{len(source_rows)} source needle sets found")
    add("VAL2202_02_alpha_projection_blocks", len(alpha_attempt_rows) == 7 and all(truthy(r["blocks_prediction"]) for r in alpha_attempt_rows), "all alpha_cg projection clauses block prediction")
    add("VAL2202_03_alpha_target_nonclaim", any(r["row_id"] == "AER2202_0_effective_target" and r["status"] == "SOURCE_BACKED_TARGET_NOT_PREDICTION" for r in alpha_effective_rows_data), "alpha_cg effective row is target-only")
    add("VAL2202_04_raw_cg_refused", any(r["row_id"] == "AER2202_1_raw_cg" and r["status"] == "NOT_INVARIANT_NOT_SCOREABLE" for r in alpha_effective_rows_data), "raw c_g remains refused")
    add("VAL2202_05_readout_not_derived", any(r["theorem_id"] == "RZT2202_4_verdict" and r["current_status"] == "READOUT_ZERO_THEOREM_NOT_DERIVED" for r in readout_rows), "readout zero theorem attempted and not promoted")
    add("VAL2202_06_route_selection", any(r["route_id"] == "SEL2202_1_readout" and r["selection_status"] == "selected_next" for r in route_rows), "fixed-before-readout selected next")
    add("VAL2202_07_claim_gate", any(r["gate_id"] == "CG2202_4_local_gr_newton" and r["status"] == "BLOCKED_NONCLAIM" for r in claim_rows), "local-GR remains blocked")
    add("VAL2202_08_decision", any(r["decision"] == "MOVE_TO_FIXED_BEFORE_READOUT_PPN_MAP" for r in decision_rows_data), "decision selects fixed-before-readout PPN map")
    add("VAL2202_09_next_target", len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2202_0_2203", "2203 target selected")

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["alpha_projection_attempt"],
        OUTPUTS["alpha_effective_row"],
        OUTPUTS["readout_zero_attempt"],
        OUTPUTS["route_selection"],
        OUTPUTS["claim_gate"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    parse_ok_all = True
    parse_parts: list[str] = []
    for path in generated_csvs:
        parse_ok, count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok and count > 0
        parse_parts.append(f"{path.name}:{count if parse_ok else detail}")
    add("VAL2202_10_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add("VAL2202_11_branch_copies", len(copy_rows) == 3 and all(truthy(r["copied"]) and truthy(r["parse_ok"]) for r in copy_rows), ";".join(str(r["target_path"]) for r in copy_rows))

    all_generated_rows = [
        *source_rows,
        *alpha_attempt_rows,
        *alpha_effective_rows_data,
        *readout_rows,
        *route_rows,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add("VAL2202_12_claim_flags_false", all(not truthy(r.get("valid_for_claim", False)) and not truthy(r.get("claim_allowed", False)) for r in all_generated_rows), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2202_13_score_flags_false", all(not truthy(r.get("score_ready", False)) for r in alpha_effective_rows_data), "no alpha effective row is score-ready")
    add("VAL2202_14_formalization_clean", not formalization_has_2202_artifacts(), "formalization-workbench has no 2202 artifacts")
    add("VAL2202_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), str(ROOT / "scripts" / "__pycache__"))
    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2202_OVERALL", overall, "2202 rejects alpha_cg projection as current prediction and selects fixed-before-readout PPN map next")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    alpha_attempt_rows: list[dict[str, Any]],
    alpha_effective_rows_data: list[dict[str, Any]],
    readout_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2202 - Y5/R2FR Alpha-Cg Projection Clause Or Readout Zero Theorem",
        "",
        "## Current Verdict",
        "",
        "2202 tries the `alpha_cg` projection route first. The result is sharp but negative: Cassini gives a real source ceiling, and the effective object is known, but MTS still does not provide the same-branch `Z_X`, `lambda_X/S_PPN`, `tau_PPN`, common matter frame, and vector-tail controls needed to turn the ceiling into a prediction.",
        "",
        "So `alpha_cg` stays as a source-backed nonclaim target, not a score-ready row. Raw `c_g` remains refused. The next route is the fixed-before-readout theorem because it attacks measured-GM/source-normalization and GR/Newton recovery more directly than another Hessian pass.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Alpha-Cg Projection Attempt",
        "",
        md_table(alpha_attempt_rows, ["clause_id", "clause", "required_statement", "status", "blocks_prediction", "valid_for_claim"]),
        "",
        "## Alpha-Cg Effective Row",
        "",
        md_table(alpha_effective_rows_data, ["row_id", "object", "formula", "source_ceiling", "prediction_value", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Readout Zero Theorem Attempt",
        "",
        md_table(readout_rows, ["theorem_id", "theorem_piece", "statement", "current_status", "obstruction", "effect_if_signed", "valid_for_claim"]),
        "",
        "## Route Selection",
        "",
        md_table(route_rows, ["route_id", "route", "selection_status", "reason", "next_use", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_data, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_data, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is not a retreat from GR reduction. It is pruning a bad loop. The `alpha_cg` route is clean as a formula but currently blocked by the same missing parent Hessian/projection inputs. The readout route is now the better attack because GR/Newton recovery ultimately needs measured mass, source normalization, and observed metric maps fixed before comparison.",
        "",
        "Best next attack: `2203` should derive or reject the fixed-before-readout PPN map from parent variables to observed `gamma` and measured `GM`, with no post-fit absorption and no cancellation against `alpha_cg`.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    alpha_attempt_rows = alpha_projection_attempt_rows()
    alpha_effective_rows_data = alpha_effective_rows()
    readout_rows = readout_zero_attempt_rows()
    route_rows = route_selection_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["alpha_projection_attempt"], alpha_attempt_rows)
    write_csv(OUTPUTS["alpha_effective_row"], alpha_effective_rows_data)
    write_csv(OUTPUTS["readout_zero_attempt"], readout_rows)
    write_csv(OUTPUTS["route_selection"], route_rows)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)

    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        alpha_attempt_rows,
        alpha_effective_rows_data,
        readout_rows,
        route_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        alpha_attempt_rows,
        alpha_effective_rows_data,
        readout_rows,
        route_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )


if __name__ == "__main__":
    main()
