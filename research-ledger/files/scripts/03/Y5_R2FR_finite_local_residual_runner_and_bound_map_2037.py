from __future__ import annotations

import csv
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


DOC = ROOT / "2037-Y5-R2FR-finite-local-residual-runner-and-bound-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2037_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2037*finite*")) or any(FORMALIZATION.rglob("*2037*residual*")) or any(FORMALIZATION.rglob("*2037*bound*"))
    except Exception:
        return False


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2037_00_2036_handoff",
            ROOT / "2036-Y5-R2FR-minimal-u-domain-certificate-or-finite-local-residual-acquisition.md",
            ["NEXT2036_0_2037", "FACQ2036_0_branch_policy", "VAL2036_OVERALL"],
            "2036 activates finite local residual acquisition.",
        ),
        (
            "SRC2037_01_2036_next",
            OUT / "P8_Y5_PARENT_QLOC_2036_NEXT_TARGET.csv",
            ["NEXT2036_0_2037"],
            "machine-readable 2037 target.",
        ),
        (
            "SRC2037_02_2036_schema",
            OUT / "P8_Y5_PARENT_QLOC_2036_ACCEPTED_ROW_SCHEMA.csv",
            ["valid_for_claim", "no_cancellation_components"],
            "accepted finite residual row schema from 2036.",
        ),
        (
            "SRC2037_03_local_template",
            OUT / "MTS_local_residual_predictions_TEMPLATE.csv",
            ["R10_fifth_force", "R11_EH_operator_ledger"],
            "local residual prediction template and arena row names.",
        ),
        (
            "SRC2037_04_arena_map",
            OUT / "P8_Y5_R10_1434_ARENA_BOUND_MAP.csv",
            ["ABM1434_0_R10", "ABM1434_2_PPN", "ABM1434_4_ORBITAL_NEWTON"],
            "cross-arena bound map; all current arena maps nonclaim/not scoreable.",
        ),
        (
            "SRC2037_05_local_baselines",
            OUT / "P8_Y5_R10_713_LOCAL_BOUND_BASELINES.csv",
            ["LBB713_7_R10_fifth_force", "LBB713_4_R3_gamma"],
            "local baseline guardrails, including R10 curve-required rule.",
        ),
        (
            "SRC2037_06_r10_curve",
            OUT / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv",
            ["REVIEWED_QA_CANDIDATE_NONCLAIM", "accepted_for_scoring"],
            "reviewed internal R10 digitization candidate; not claim-valid or score-ready.",
        ),
        (
            "SRC2037_07_qr_schema",
            OUT / "P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv",
            ["QB1240_0_qR_input", "QB1240_1_gamma_projection", "MISSING_QR_VALUE"],
            "existing Q_R to PPN gamma nonclaim schema.",
        ),
        (
            "SRC2037_08_1239_runner",
            ROOT / "scripts" / "Y5_R10_local_residual_vector_runner_input_schema_and_source_priority.py",
            ["1239-Y5-R10-local-residual-vector-runner-input-schema-and-source-priority", "build PPN_QR residual bound schema before any local-GR score"],
            "older local residual vector runner discipline.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def candidate_input_rows() -> list[dict[str, object]]:
    data = [
        ("CAND2037_0_ZRR", "Z_RR", "J_u^A Z_AB J_u^B", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "R10;R11;PPN_if_long_range"),
        ("CAND2037_1_ZRY", "Z_RY", "J_u^A Z_AB J_Y^B", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "R10;R11;PPN_cross_response"),
        ("CAND2037_2_MR2", "M_R2", "partial^2 V_eff/partial u^2", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "R10_range;screening"),
        ("CAND2037_3_JR", "J_R", "Euler/source projection onto u", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "WEP;R10;PPN;source_charge"),
        ("CAND2037_4_QR", "Q_R", "exterior reciprocal boundary charge", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "PPN_gamma;R10;orbital"),
        ("CAND2037_5_BR", "B_R", "boundary functional derivative/source", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "PPN;clock;orbital;R10"),
        ("CAND2037_6_tau_maps", "tau_R10/tau_PPN/tau_clock/tau_orbital", "arena projection maps", "MISSING_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH", "MISSING_EQUATION_REF", "all_local_arenas"),
    ]
    rows = []
    for candidate_id, symbol, formula, value, units, source_path, equation_ref, arenas in data:
        row = base_row()
        row.update(
            {
                "candidate_id": candidate_id,
                "symbol": symbol,
                "formula": formula,
                "value": value,
                "units": units,
                "normalization": "u=R_AB=2ln(J_q); same-frame parent Hessian convention required",
                "source_path": source_path,
                "equation_ref": equation_ref,
                "arena_targets": arenas,
                "theorem_zero": False,
                "theorem_zero_authority": "MISSING_PARENT_SIGNED_TRUE",
                "no_cancellation_components": "MISSING_COMPONENT_VECTOR",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def is_missing(value: object) -> bool:
    text = str(value).strip()
    return text == "" or text.upper().startswith("MISSING") or "FILL" in text.upper() or "PLACEHOLDER" in text.upper()


def validate_candidate(row: dict[str, object]) -> tuple[str, str]:
    if boolish(row.get("theorem_zero")):
        if row.get("theorem_zero_authority") != "PARENT_SIGNED_TRUE":
            return "REFUSED_THEOREM_ZERO_UNSIGNED", "theorem_zero requires PARENT_SIGNED_TRUE"
        if is_missing(row.get("source_path")) or is_missing(row.get("equation_ref")):
            return "REFUSED_THEOREM_ZERO_SOURCE_MISSING", "theorem zero still needs source path and equation"
        return "ACCEPTED_ZERO_ROW_REVIEW_REQUIRED", "zero row source appears complete but remains nonclaim pending review"
    required = ["value", "units", "source_path", "equation_ref", "normalization", "no_cancellation_components"]
    missing = [field for field in required if is_missing(row.get(field))]
    if missing:
        return "REFUSED_MISSING_INPUTS", ";".join(f"MISSING_{field.upper()}" for field in missing)
    try:
        float(str(row["value"]))
    except Exception:
        return "REFUSED_NON_NUMERIC_VALUE", f"value={row['value']}"
    return "ACCEPTED_FINITE_ROW_REVIEW_REQUIRED", "numeric row appears complete but remains nonclaim pending review"


def runner_result_rows(candidate_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for candidate in candidate_rows:
        status, reason = validate_candidate(candidate)
        row = base_row()
        row.update(
            {
                "candidate_id": candidate["candidate_id"],
                "symbol": candidate["symbol"],
                "runner_status": status,
                "reason": reason,
                "score_attempted": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def arena_projection_rows() -> list[dict[str, object]]:
    data = [
        (
            "AP2037_0_R10",
            "R10_short_range_inverse_square",
            "alpha(lambda)",
            "Z_RR,Z_RY,M_R2,J_R,Q_R,B_R,tau_R10",
            "requires full alpha(lambda) prediction curve and claim-ready bound curve; 1572 R10 curve is internal QA nonclaim",
            "NOT_SCOREABLE",
        ),
        (
            "AP2037_1_PPN",
            "PPN_radio_and_ephemerides",
            "gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi",
            "Q_R,B_R,J_R,Z_RY,tau_PPN plus metric/source normalization maps",
            "requires explicit residual-to-PPN vector map; scalar projection alone refused",
            "NOT_SCOREABLE",
        ),
        (
            "AP2037_2_CLOCK",
            "clock_redshift",
            "redshift_fractional_deviation",
            "B_R,J_R,tau_clock plus clock functional",
            "requires clock/readout functional and same-frame mapping",
            "NOT_SCOREABLE",
        ),
        (
            "AP2037_3_ORBITAL",
            "orbital_and_Newton_source_normalization",
            "Gdot_over_G;delta_GM;anomalous_radial_acceleration",
            "J_R,Q_R,B_R,tau_orbital plus source-worldtube/time/radial law",
            "requires source normalization and no post-fit GM calibration",
            "NOT_SCOREABLE",
        ),
        (
            "AP2037_4_WEP",
            "WEP_MICROSCOPE",
            "eta_Ti_Pt",
            "J_R/material-source projection/tau_WEP",
            "requires material tensor/source worldtube; direct geometry alone is not enough",
            "NOT_SCOREABLE",
        ),
    ]
    rows = []
    for row_id, arena, observable, required_inputs, block_reason, score_status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "observable": observable,
                "required_inputs": required_inputs,
                "block_reason": block_reason,
                "score_status": score_status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def bound_asset_status_rows() -> list[dict[str, object]]:
    r10_rows = read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv")
    arena_rows = read_csv_dicts(OUT / "P8_Y5_R10_1434_ARENA_BOUND_MAP.csv")
    source_backed = sum(1 for row in r10_rows if boolish(row.get("source_backed")))
    score_ready = sum(1 for row in r10_rows if boolish(row.get("score_ready")) or boolish(row.get("accepted_for_scoring")))
    claim_ready = sum(1 for row in r10_rows if boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")))
    arena_scoreable = sum(1 for row in arena_rows if str(row.get("score_status", "")).upper() == "SCOREABLE")
    data = [
        ("BSTAT2037_0_R10_curve_rows", "R10 reviewed candidate rows", len(r10_rows), "reviewed internal digitization exists", "NONCLAIM"),
        ("BSTAT2037_1_R10_source_backed", "R10 source-backed rows", source_backed, "must be >0 before scoring", "BLOCKED" if source_backed == 0 else "REVIEW_REQUIRED"),
        ("BSTAT2037_2_R10_score_ready", "R10 score-ready rows", score_ready, "must be >0 before scoring", "BLOCKED" if score_ready == 0 else "REVIEW_REQUIRED"),
        ("BSTAT2037_3_R10_claim_ready", "R10 claim-ready rows", claim_ready, "must be 0 until independent provenance passes", "PASS_NONCLAIM" if claim_ready == 0 else "REVIEW_DANGER"),
        ("BSTAT2037_4_arena_scoreable", "arena scoreable maps", arena_scoreable, "must be >0 before cross-arena score", "BLOCKED" if arena_scoreable == 0 else "REVIEW_REQUIRED"),
    ]
    rows = []
    for row_id, item, count, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "count": count,
                "requirement": requirement,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows(result_rows: list[dict[str, object]], bound_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted = [row for row in result_rows if str(row["runner_status"]).startswith("ACCEPTED")]
    data = [
        (
            "DEC2037_0_runner_built",
            "Finite local residual runner is now implemented as a refusal/scoring interface.",
            "This converts the failed exact u-domain route into a testable input contract.",
        ),
        (
            "DEC2037_1_current_inputs",
            "No finite local residual input is accepted in the smoke run." if not accepted else "At least one finite input needs review.",
            "Current candidate rows are placeholders/theorem-unsigned and therefore not scoreable.",
        ),
        (
            "DEC2037_2_bound_assets",
            "Arena bound assets exist but remain nonclaim/not scoreable for this branch.",
            "R10 has internal digitized candidates, but no accepted source-backed score-ready row is used here.",
        ),
        (
            "DEC2037_3_next",
            "Next target is first real source row acquisition, not more theorem loops.",
            "Prioritize Q_R/B_R or J_R because they connect directly to PPN gamma, fifth force, WEP/source, and orbital channels.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(result_rows: list[dict[str, object]], bound_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted_count = sum(1 for row in result_rows if str(row["runner_status"]).startswith("ACCEPTED"))
    score_ready_count = sum(1 for row in bound_rows if row["status"] == "REVIEW_REQUIRED")
    data = [
        ("GATE2037_0_runner_schema", "finite residual runner schema exists", "PASS_NONCLAIM", "candidate validation and arena maps written"),
        ("GATE2037_1_candidate_inputs", "at least one accepted finite residual row", "FAIL_MISSING_INPUTS" if accepted_count == 0 else "REVIEW_REQUIRED", f"accepted_count={accepted_count}"),
        ("GATE2037_2_bound_assets", "at least one score-ready arena bound map", "FAIL_NOT_SCOREABLE" if score_ready_count == 0 else "REVIEW_REQUIRED", f"review_required_bound_assets={score_ready_count}"),
        ("GATE2037_3_no_cancellation", "component no-cancellation guard available", "FAIL_MISSING_COMPONENTS", "all candidate component vectors missing"),
        ("GATE2037_4_local_claim", "local GR/Newton/R10/PPN/clock/orbital pass", "FAIL_BLOCKED", "runner refused inputs and bound maps are not scoreable"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2037_0_2038",
            "target_doc": "2038-Y5-R2FR-first-real-u-residual-source-row-acquisition.md",
            "objective": "acquire or derive the first real finite u-residual row, prioritizing Q_R/B_R or J_R, with source path, units, normalization, no-cancellation components, and arena projection hooks; rerun the 2037 validator after acquisition",
            "must_include": "one candidate finite row; source path/equation; units; theorem_zero authority if zero; PPN gamma/R10/WEP/orbital projection target; refusal if placeholder; no claim",
            "excluded": "symbolic placeholders; broad object-language proof; scoring internal R10 curve as claim-ready; local-GR claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    candidate_rows: list[dict[str, object]],
    result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2037_0_source_weight_results",
            SOURCE_WEIGHT_DOCS / "AFRAME_FINITE_LOCAL_RESIDUAL_RUNNER_2037_NONCLAIM.csv",
            result_rows,
        ),
        (
            "COPY2037_1_wep_arena_map",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2037_ARENA_PROJECTION_MAP_NONCLAIM.csv",
            arena_rows,
        ),
        (
            "COPY2037_2_rab_candidates",
            QUEUE / "JR2037_FINITE_U_RESIDUAL_CANDIDATE_INPUTS_NONCLAIM.csv",
            candidate_rows,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2037_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2037_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2037_02_candidates_refused", all(str(row["runner_status"]).startswith("REFUSED") for row in result_rows), "smoke candidates are refused because inputs are missing"))
    checks.append(("VAL2037_03_arena_maps_blocked", all(row["score_status"] == "NOT_SCOREABLE" for row in arena_rows), "arena projection maps remain not scoreable"))
    claim_ready = next(row for row in bound_rows if row["row_id"] == "BSTAT2037_3_R10_claim_ready")
    checks.append(("VAL2037_04_r10_nonclaim", int(claim_ready["count"]) == 0, "R10 reviewed curve rows are not claim-ready"))
    local_gate = next(row for row in gate_rows if row["row_id"] == "GATE2037_4_local_claim")
    checks.append(("VAL2037_05_local_claim_blocked", local_gate["status"] == "FAIL_BLOCKED", "local claim remains blocked"))
    checks.append(("VAL2037_06_next_selected", next_rows[0]["target_id"] == "NEXT2037_0_2038", "next target is selected"))
    checks.append(("VAL2037_07_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2037_08_no_formalization_2037_artifacts", not formalization_has_2037_artifacts(), "no 2037 finite/residual/bound artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2037_OVERALL", overall_ok, "2037 finite local residual runner checkpoint is internally valid and nonclaim"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 2037 Y5 R2FR Finite Local Residual Runner And Bound Map",
        "",
        "## Current Verdict",
        "",
        "The finite local residual runner now exists as a strict nonclaim interface. It refuses placeholder `Z_RR/Z_RY/M_R2/J_R/Q_R/B_R/tau` inputs, keeps R10/PPN/WEP/clock/orbital maps not-scoreable until real source rows exist, and prevents the internal R10 digitization candidate from being treated as claim-ready evidence.",
        "",
        "No local-GR, Newton, R10, PPN, WEP, clock, orbital, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Candidate Inputs",
        md_table(candidate_rows, ["candidate_id", "symbol", "formula", "value", "units", "source_path", "equation_ref", "arena_targets", "valid_for_claim"]),
        "## Runner Results",
        md_table(result_rows, ["candidate_id", "symbol", "runner_status", "reason", "score_attempted", "valid_for_claim", "claim_allowed"]),
        "## Arena Projection Map",
        md_table(arena_rows, ["row_id", "arena", "observable", "required_inputs", "block_reason", "score_status", "claim_allowed"]),
        "## Bound Asset Status",
        md_table(bound_rows, ["row_id", "item", "count", "requirement", "status", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    candidate_rows = candidate_input_rows()
    result_rows = runner_result_rows(candidate_rows)
    arena_rows = arena_projection_rows()
    bound_rows = bound_asset_status_rows()
    decision_rows_ = decision_rows(result_rows, bound_rows)
    gate_rows = claim_gate_rows(result_rows, bound_rows)
    next_rows = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2037_SOURCE_REGISTER.csv",
        "candidates": OUT / "P8_Y5_PARENT_QLOC_2037_CANDIDATE_INPUTS.csv",
        "results": OUT / "P8_Y5_PARENT_QLOC_2037_RUNNER_RESULTS.csv",
        "arena": OUT / "P8_Y5_PARENT_QLOC_2037_ARENA_PROJECTION_MAP.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2037_BOUND_ASSET_STATUS.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2037_DECISION_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2037_CLAIM_GATE.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2037_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2037_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2037_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["candidates"], candidate_rows)
    write_csv(paths["results"], result_rows)
    write_csv(paths["arena"], arena_rows)
    write_csv(paths["bounds"], bound_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(candidate_rows, result_rows, arena_rows)
    write_csv(paths["branch"], branch_rows)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        candidate_rows,
        result_rows,
        arena_rows,
        bound_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        candidate_rows,
        result_rows,
        arena_rows,
        bound_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        candidate_rows,
        result_rows,
        arena_rows,
        bound_rows,
        decision_rows_,
        gate_rows,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
