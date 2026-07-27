from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2209"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2209-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2209_SOURCE_REGISTER.csv",
    "source_map": OUT / "P8_Y5_PARENT_QLOC_2209_QLOC_TO_YUKAWA_SOURCE_MAP_ATTEMPT.csv",
    "quartet_audit": OUT / "P8_Y5_PARENT_QLOC_2209_R10_INPUT_QUARTET_AUDIT.csv",
    "bound_curve": OUT / "P8_Y5_PARENT_QLOC_2209_BOUND_CURVE_STATUS.csv",
    "score_readiness": OUT / "P8_Y5_PARENT_QLOC_2209_R10_SCORE_READINESS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2209_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2209_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2209_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2209_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2209_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2209_R10_INPUT_QUARTET_BLOCKER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2209_QLOC_TO_YUKAWA_SOURCE_MAP_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_R10_BOUND_CURVE_STATUS_2209_NONCLAIM.csv",
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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


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


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2209_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2209-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2209*",
        "*P8_Y5_BRR545_2209*",
        "*Y5_R2FR_R10_q_loc_Yukawa_source_map_or_bound_curve_blocker_2209*",
        "*JR2209*",
        "*PARENT_QLOC_R10_BOUND_CURVE_STATUS_2209*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2208_handoff",
            ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
            ["NEXT2208_0_2209", "R10K2208_0_yukawa_kernel_form", "VAL2208_OVERALL"],
            "2208 selects R10 q_loc-to-Yukawa source-map/bound-curve blocker next.",
        ),
        (
            "2208_kernel_scaffold",
            OUT / "P8_Y5_PARENT_QLOC_2208_R10_RANGE_KERNEL_SCAFFOLD.csv",
            ["R10K2208_0_yukawa_kernel_form", "R10K2208_2_bound_curve_link"],
            "machine-readable finite-range/Yukawa kernel scaffold.",
        ),
        (
            "1688_bulk_data_pack",
            OUT / "P8_Y5_PARENT_QLOC_1688_R10_BULK_BOUND_DATA_PACK.csv",
            ["RDP1688_5_bound_anchor", "RDP1688_7_verdict"],
            "R10 bulk data pack: schema ready, scoring blocked by theory legs and full curve.",
        ),
        (
            "563_bound_curve_checkpoint",
            ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            ["B563_0_no_full_bound_curve", "E563_2_mts_parent_coefficients_missing", "V563_10_no_overclaim"],
            "real Eot-Wash anchors staged as nonclaim; full curve and MTS alpha still missing.",
        ),
        (
            "563_blocker_ledger",
            OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv",
            ["B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha"],
            "blocker ledger for missing full curve and numeric MTS alpha.",
        ),
        (
            "947_projection_fill",
            ROOT / "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
            ["PFA947_0_R10_projection", "BI947_0_cg_R10", "CGATE947_0_R10_score"],
            "older projection fill records missing tau_R10, K_X(lambda), Qbar_XH and parent c_g.",
        ),
        (
            "1012_source_normalization",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["Y5C1012_3_bulk_X_Yukawa_tail", "Y5O1012_8_verdict", "V1012_SUMMARY"],
            "source-normalization/range-dependence channels remain retained unfilled.",
        ),
        (
            "2191_component_runner",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["QCS2191_2_R10", "RUN2191_1_R10", "VAL2191_OVERALL"],
            "q_loc R10 finite-range kernel template and failure reasons.",
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


def source_map_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            map_id="YSM2209_0_target_equation",
            object="R10 Yukawa source equation",
            conditional_form="(nabla^2-lambda_X^-2) Phi_X = -4*pi*G_ref rho_X^eff",
            required_mts_map="rho_X^eff = C_q(lambda_X,frame,source,test) * S_q[q_loc or T_GK]",
            current_status="FORMAL_TARGET_WRITTEN_NOT_PARENT_SIGNED",
            missing_inputs="MISSING_QLOC_TO_SCALAR_SOURCE_MAP;MISSING_TGK_OR_INVERSE_DIVERGENCE;MISSING_UNITS",
            score_ready=False,
        ),
        base_row(
            map_id="YSM2209_1_vector_to_scalar_problem",
            object="q_loc vector to scalar charge density",
            conditional_form="S_q[q_loc] could be tau_R10_nu q_loc^nu, divergence inverse of T_GK, or projected source-current defect",
            required_mts_map="parent must select tau_R10/projector/domain before readout, not by fit",
            current_status="NOT_DERIVED",
            missing_inputs="MISSING_TAU_R10;MISSING_PROJECTOR_DOMAIN;MISSING_SOURCE_CURRENT_OWNER",
            score_ready=False,
        ),
        base_row(
            map_id="YSM2209_2_lambda_owner",
            object="lambda_X",
            conditional_form="lambda_X=sqrt(Z_X/M_X^2) or parent mass-gap/range theorem",
            required_mts_map="Z_X and M_X^2 must be parent-sourced with units and branch convention",
            current_status="MISSING_PARENT_RANGE_OWNER",
            missing_inputs="MISSING_Z_X;MISSING_M_X_SQUARED;MISSING_RANGE_SCREENING_TRANSFER",
            score_ready=False,
        ),
        base_row(
            map_id="YSM2209_3_charge_normalization",
            object="source/test charge normalization",
            conditional_form="alpha_R10_q(lambda)=C_geom(lambda)*Q_source^q(lambda)*Q_test^q(lambda)",
            required_mts_map="Q_source and Q_test must be source-normalized in the same frame as Newtonian mass",
            current_status="MISSING_SOURCE_TEST_CHARGES",
            missing_inputs="MISSING_Q_SOURCE;MISSING_Q_TEST;MISSING_Y5_SOURCE_NORMALIZATION",
            score_ready=False,
        ),
        base_row(
            map_id="YSM2209_4_bound_curve",
            object="alpha_bound(lambda)",
            conditional_form="abs(alpha_R10_q(lambda)) <= alpha_bound(lambda)",
            required_mts_map="full positive numeric bound curve or official table, with interpolation rule and provenance",
            current_status="ANCHOR_ONLY_NONCLAIM_AVAILABLE_FULL_CURVE_MISSING",
            missing_inputs="MISSING_FULL_DIGITIZED_BOUND_CURVE",
            score_ready=False,
        ),
        base_row(
            map_id="YSM2209_5_verdict",
            object="q_loc-to-Yukawa source map",
            conditional_form="R10 score requires YSM2209_0..4 together",
            required_mts_map="source map + lambda_X + charges + bound curve",
            current_status="R10_SCORE_BLOCKED_QUARTET_INCOMPLETE",
            missing_inputs="MISSING_QLOC_TO_SOURCE_MAP;MISSING_LAMBDA_X;MISSING_CHARGES;MISSING_FULL_CURVE",
            score_ready=False,
        ),
    ]


def quartet_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "R10Q2209_0_source_map",
            "q_loc_to_Yukawa_source_map",
            "rho_X^eff or Q_source^q as a parent-selected scalar/range source built from q_loc or T_GK",
            "MISSING_PARENT_SOURCE_MAP",
            "2208 gives Yukawa kernel; 1011/2191 keep q_loc profile/projection missing",
            "derive source-current owner theorem or source finite map row",
        ),
        (
            "R10Q2209_1_range",
            "lambda_X",
            "lambda_X=sqrt(Z_X/M_X^2) or theorem-zero no-range branch with units",
            "MISSING_LAMBDA_X",
            "563 says Z_X/M_X^2 parent coefficients are missing; 947 says K_X(lambda) missing",
            "derive mass gap/range owner or classify as PPN/R10/screened branch",
        ),
        (
            "R10Q2209_2_charge_norm",
            "source_test_charge_normalization",
            "Q_source, Q_test, tau_R10 and source/test profiles in same Newtonian frame",
            "MISSING_Q_SOURCE_Q_TEST_TAU_R10",
            "947 R10 projection is blocked by missing tau_R10, Qbar_XH, K_X(lambda), c_g",
            "fill tau_R10/source-test charge row or prove matter/source charge silence",
        ),
        (
            "R10Q2209_3_bound_curve",
            "alpha_bound_lambda_curve",
            "dense digitized/source-backed positive alpha_bound(lambda) rows with interpolation rule",
            "MISSING_FULL_BOUND_CURVE",
            "563 records Eot-Wash 2020/2007 anchors only; full curve not acquired",
            "digitize 2020 PRL bound figure or locate official machine-readable table",
        ),
        (
            "R10Q2209_4_prediction_row",
            "alpha_R10_q_prediction",
            "numeric alpha_R10_q(lambda) with source path, units, uncertainty/prior and no-cancellation vector",
            "MISSING_NUMERIC_ALPHA_PREDICTION",
            "1688 bulk data pack says source/test/kernel/tail rows are missing",
            "stage finite nonclaim prediction only after source map/range/charges are real",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            required_input=required_input,
            pass_condition=pass_condition,
            current_status=current_status,
            evidence=evidence,
            next_action=next_action,
            passes_now=False,
            score_ready=False,
        )
        for audit_id, required_input, pass_condition, current_status, evidence, next_action in specs
    ]


def bound_curve_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            curve_id="BCS2209_0_EotWash_2020_anchor",
            source="Eot-Wash 2020 PRL / PubMed 32216404 / arXiv:2002.11761",
            lambda_value="3.86e-5",
            lambda_units="m",
            alpha_bound="1.0",
            data_status="ANCHOR_ONLY_NON_CURVE",
            valid_bound_curve_row=False,
            claim_use="provenance_only",
            blocker="single threshold anchor cannot bound arbitrary MTS lambda",
        ),
        base_row(
            curve_id="BCS2209_1_EotWash_2007_anchor",
            source="Eot-Wash 2007 PRL / arXiv:hep-ph/0611184",
            lambda_value="5.6e-5",
            lambda_units="m",
            alpha_bound="1.0",
            data_status="ANCHOR_ONLY_NON_CURVE",
            valid_bound_curve_row=False,
            claim_use="continuity_only",
            blocker="older threshold anchor cannot replace modern dense curve",
        ),
        base_row(
            curve_id="BCS2209_2_live_digitized_curve",
            source="source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            lambda_value="MISSING_DENSE_ROWS",
            lambda_units="m",
            alpha_bound="MISSING_ALPHA_BOUND_CURVE",
            data_status="PLACEHOLDER_INVALID_FOR_CLAIM",
            valid_bound_curve_row=False,
            claim_use="blocked",
            blocker="full digitized/source-backed curve still missing per 563 and 1688",
        ),
        base_row(
            curve_id="BCS2209_3_curve_verdict",
            source="563+1688 curve status",
            lambda_value="not_scoreable",
            lambda_units="not_scoreable",
            alpha_bound="not_scoreable",
            data_status="BOUND_CURVE_NOT_CLAIM_READY",
            valid_bound_curve_row=False,
            claim_use="blocked",
            blocker="R10 score must wait for a real curve or official table",
        ),
    ]


def score_readiness_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            score_id="R10S2209_0_minimum_formula",
            formula="alpha_R10_q(lambda)=C_geom(lambda)*Q_source^q(lambda)*Q_test^q(lambda)+epsilon_tail(lambda)",
            required_inputs="C_geom;Q_source;Q_test;lambda_X;epsilon_tail;alpha_bound(lambda);units;source_paths",
            current_status="FORMULA_SCHEMA_READY_VALUES_MISSING",
            score_ready=False,
            failure_reasons="MISSING_QLOC_TO_SOURCE_MAP;MISSING_LAMBDA_X;MISSING_Q_SOURCE;MISSING_Q_TEST;MISSING_FULL_BOUND_CURVE",
        ),
        base_row(
            score_id="R10S2209_1_no_cancellation",
            formula="abs(alpha_total)<=alpha_bound only after absolute envelope over q_loc,c_g,b_A,boundary,tail components",
            required_inputs="component vector and signed correlation theorem or absolute sum",
            current_status="NO_CANCELLATION_VECTOR_MISSING",
            score_ready=False,
            failure_reasons="MISSING_COMPONENT_VALUES;MISSING_CORRELATION_THEOREM",
        ),
        base_row(
            score_id="R10S2209_2_claim_runner",
            formula="R10_pass = all numeric prediction rows valid and abs(alpha_predicted)<=alpha_bound at each lambda",
            required_inputs="valid prediction rows and valid bound rows",
            current_status="RUNNER_MUST_BLOCK",
            score_ready=False,
            failure_reasons="VALID_PREDICTION_ROWS_FALSE;VALID_BOUND_ROWS_FALSE",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2209_0_source_map",
            gate="q_loc-to-Yukawa source map exists",
            status="BLOCKED_NONCLAIM",
            implication="R10 alpha prediction remains symbolic",
        ),
        base_row(
            gate_id="CG2209_1_lambda",
            gate="lambda_X/range owner exists",
            status="BLOCKED_NONCLAIM",
            implication="R10/PPN/screened branch cannot be selected quantitatively",
        ),
        base_row(
            gate_id="CG2209_2_charges",
            gate="source/test charges and tau_R10 are normalized",
            status="BLOCKED_NONCLAIM",
            implication="alpha(lambda) cannot be compared to apparatus bounds",
        ),
        base_row(
            gate_id="CG2209_3_bound_curve",
            gate="claim-valid alpha_bound(lambda) curve exists",
            status="BLOCKED_NONCLAIM",
            implication="anchor-only rows remain provenance, not evidence",
        ),
        base_row(
            gate_id="CG2209_4_R10_score",
            gate="R10 score can be run as MTS evidence",
            status="BLOCKED_NONCLAIM",
            implication="input quartet incomplete; no R10/local-GR claim",
        ),
        base_row(
            gate_id="CG2209_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private goal work only; no GitHub action",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2209_0_gain",
            decision="R10_INPUT_QUARTET_DEFINED",
            rationale="The R10 route is now reduced to four explicit requirements: q_loc source map, lambda_X, charge normalization, and full bound curve.",
            next_action="fill the first quartet member instead of broad re-audits",
        ),
        base_row(
            decision_id="DEC2209_1_limit",
            decision="R10_SCORE_BLOCKED_BY_INCOMPLETE_QUARTET",
            rationale="Existing sources provide kernel scaffolds and anchor provenance but no complete source map, range owner, charge normalization, or claim-valid curve.",
            next_action="do not run alpha(lambda) scoring from placeholders",
        ),
        base_row(
            decision_id="DEC2209_2_best_next",
            decision="LAMBDA_X_OR_SOURCE_MAP_SELECTED_NEXT",
            rationale="Without lambda_X the theory cannot choose R10 versus PPN/screened branch; without source map alpha is symbolic. Lambda/range is the cleanest next discriminator.",
            next_action="2210 should derive/source lambda_X= sqrt(Z_X/M_X^2) or declare the range branch blocked",
        ),
        base_row(
            decision_id="DEC2209_3_no_claim",
            decision="NO_R10_LOCAL_GR_CLAIM",
            rationale="2209 is blocker discipline and source-map lowering, not evidence of fifth-force success.",
            next_action="keep all rows valid_for_claim=false until quartet closes",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2209_0_2210",
            selection_status="selected",
            target_file="2210-Y5-R2FR-lambda-X-range-owner-or-R10-source-map-first-row.md",
            target_script="scripts/Y5_R2FR_lambda_X_range_owner_or_R10_source_map_first_row_2210.py",
            objective="derive or source lambda_X from Z_X/M_X^2 and decide whether the q_loc mode belongs to R10, PPN, screened, or still blocked; if range remains missing, stage the first q_loc-to-source map row as nonclaim",
            success_condition="one quartet member is filled beyond schema level with source path and valid_for_claim=false, or the range/source-map blocker is proven explicit",
            do_not_do="do not set lambda_X by convenience, do not score anchor-only bounds, do not claim R10/local GR, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2209_1_data_parallel",
            selection_status="held_parallel",
            target_file="2210b-Y5-R2FR-EotWash-2020-bound-curve-digitization-ledger.md",
            target_script="scripts/Y5_R2FR_EotWash_2020_bound_curve_digitization_ledger_2210b.py",
            objective="digitize or locate official machine-readable Eot-Wash 2020 alpha(lambda) curve rows",
            success_condition="dense positive alpha_bound(lambda) rows with provenance and interpolation policy, still nonclaim until theory alpha exists",
            do_not_do="do not promote threshold anchors as a full bound curve",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["quartet_audit"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["source_map"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["bound_curve"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        row_count = 0
        if source.exists():
            shutil.copy2(source, target)
            copied = target.exists()
            parse_ok, row_count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=row_count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    source_map_rows_: list[dict[str, Any]],
    quartet_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(
            base_row(
                validation_id=validation_id,
                status="PASS" if status else "FAIL",
                detail=detail,
            )
        )

    sources_exist = all(truthy(row.get("path_exists")) for row in source_rows)
    needles_found = all(truthy(row.get("needles_found")) for row in source_rows)
    add("VAL2209_00_sources_exist", sources_exist, f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2209_01_needles_found", needles_found, f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    source_map_ok = any(row.get("map_id") == "YSM2209_5_verdict" and "QUARTET_INCOMPLETE" in str(row.get("current_status")) for row in source_map_rows_)
    add("VAL2209_02_source_map_attempt", source_map_ok, "q_loc-to-Yukawa source map target written and blocked by incomplete quartet")

    quartet_ok = len(quartet_rows) == 5 and all(not truthy(row.get("passes_now")) and not truthy(row.get("score_ready")) for row in quartet_rows)
    add("VAL2209_03_quartet_audit", quartet_ok, f"quartet/input rows={len(quartet_rows)} all blocked")

    bound_ok = any(row.get("curve_id") == "BCS2209_0_EotWash_2020_anchor" and row.get("data_status") == "ANCHOR_ONLY_NON_CURVE" for row in bound_rows)
    curve_blocked = any(row.get("curve_id") == "BCS2209_3_curve_verdict" and row.get("data_status") == "BOUND_CURVE_NOT_CLAIM_READY" for row in bound_rows)
    add("VAL2209_04_bound_curve_status", bound_ok and curve_blocked, "Eot-Wash anchors retained as nonclaim; full curve blocked")

    score_ok = all(not truthy(row.get("score_ready")) for row in score_rows) and any("MISSING_QLOC_TO_SOURCE_MAP" in str(row.get("failure_reasons")) for row in score_rows)
    add("VAL2209_05_score_readiness", score_ok, "R10 scoring remains blocked by missing theory/data inputs")

    claim_ok = any(row.get("gate_id") == "CG2209_4_R10_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2209_06_claim_gate", claim_ok, "R10/local claims remain blocked")

    decision_ok = any(row.get("decision") == "R10_INPUT_QUARTET_DEFINED" for row in decision_rows_) and any(row.get("decision") == "LAMBDA_X_OR_SOURCE_MAP_SELECTED_NEXT" for row in decision_rows_)
    add("VAL2209_07_decision", decision_ok, "decision ledger defines input quartet and selects lambda/source-map next")

    next_ok = any(row.get("route_id") == "NEXT2209_0_2210" and "lambda_X" in str(row.get("objective")) for row in next_rows)
    add("VAL2209_08_next_target", next_ok, "2210 lambda_X range owner or source-map first row selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2209_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2209_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, source_map_rows_, quartet_rows, bound_rows, score_rows, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2209_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2209_artifacts()
    add("VAL2209_12_formalization_clean", formalization_clean, "formalization-workbench has no 2209 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2209_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2209_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2209 defines the R10 input quartet, blocks alpha(lambda) scoring, and selects lambda_X/range owner or source-map first row next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    source_map_rows_: list[dict[str, Any]],
    quartet_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2209 - Y5/R2FR R10 q_loc Yukawa Source Map Or Bound Curve Blocker",
        "",
        "## Current Verdict",
        "",
        "2209 turns the R10 lane into a four-lock gate. A score needs all four locks closed:",
        "",
        "1. a parent `q_loc -> Yukawa source` map,",
        "2. a range owner `lambda_X`,",
        "3. source/test charge normalization in the same Newtonian frame,",
        "4. a real full `alpha_bound(lambda)` curve.",
        "",
        "Current MTS has the kernel scaffold and real Eot-Wash threshold anchors, but the quartet is incomplete. Therefore no `alpha(lambda)` score, no R10 pass, and no local-GR/Newton claim follows.",
        "",
        "The best next derivation target is `lambda_X`: without the range, we cannot even decide whether the live mode belongs in R10, PPN, a screened branch, or a blocked branch.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## q_loc To Yukawa Source Map Attempt",
        "",
        md_table(source_map_rows_, ["map_id", "object", "conditional_form", "required_mts_map", "current_status", "missing_inputs", "score_ready", "valid_for_claim"]),
        "",
        "## R10 Input Quartet Audit",
        "",
        md_table(quartet_rows, ["audit_id", "required_input", "pass_condition", "current_status", "evidence", "next_action", "passes_now", "score_ready", "valid_for_claim"]),
        "",
        "## Bound Curve Status",
        "",
        md_table(bound_rows, ["curve_id", "source", "lambda_value", "lambda_units", "alpha_bound", "data_status", "valid_bound_curve_row", "claim_use", "blocker", "valid_for_claim"]),
        "",
        "## R10 Score Readiness",
        "",
        md_table(score_rows, ["score_id", "formula", "required_inputs", "current_status", "score_ready", "failure_reasons", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branch_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is cleaner than it looks. R10 is no longer just a vague fifth-force hope; it has an exact input contract. The theory side has to provide `lambda_X` and a source map, while the data side still needs a real curve. Either path can now be worked without pretending the other is solved.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    source_map_rows_ = source_map_rows()
    quartet_rows = quartet_audit_rows()
    bound_rows = bound_curve_rows()
    score_rows = score_readiness_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["source_map"], source_map_rows_),
        (OUTPUTS["quartet_audit"], quartet_rows),
        (OUTPUTS["bound_curve"], bound_rows),
        (OUTPUTS["score_readiness"], score_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        source_map_rows_,
        quartet_rows,
        bound_rows,
        score_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        source_map_rows_,
        quartet_rows,
        bound_rows,
        score_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
