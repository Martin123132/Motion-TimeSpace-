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


DOC = ROOT / "2038-Y5-R2FR-first-real-u-residual-source-row-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2038_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return (
            any(FORMALIZATION.rglob("*2038*"))
            or any(FORMALIZATION.rglob("*first*real*u*"))
            or any(FORMALIZATION.rglob("*QR*tail*"))
        )
    except Exception:
        return False


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2038_00_2037_handoff",
            ROOT / "2037-Y5-R2FR-finite-local-residual-runner-and-bound-map.md",
            ["NEXT2037_0_2038", "VAL2037_OVERALL", "REFUSED_MISSING_INPUTS"],
            "2037 selects first real finite u-residual row acquisition after refusing placeholders.",
        ),
        (
            "SRC2038_01_2037_next",
            OUT / "P8_Y5_PARENT_QLOC_2037_NEXT_TARGET.csv",
            ["NEXT2037_0_2038", "first real finite u-residual row"],
            "machine-readable 2038 target.",
        ),
        (
            "SRC2038_02_2037_candidates",
            OUT / "P8_Y5_PARENT_QLOC_2037_CANDIDATE_INPUTS.csv",
            ["CAND2037_4_QR", "CAND2037_5_BR", "CAND2037_3_JR"],
            "2037 finite residual candidate rows.",
        ),
        (
            "SRC2038_03_1240_qr_map",
            OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            ["QMAP1240_3_gamma_projection", "gamma_minus_1_QR approximately -q_R_hat/2"],
            "Q_R to PPN gamma projection schema.",
        ),
        (
            "SRC2038_04_1244_stat_policy",
            OUT / "P8_Y5_R10_1244_PPN_GAMMA_STATISTICAL_POLICY.csv",
            ["STAT1244_0_default_smoke", "2.3e-5"],
            "strict one-sigma nonclaim Cassini/PPN gamma smoke policy.",
        ),
        (
            "SRC2038_05_1244_qr_bound",
            OUT / "P8_Y5_R10_1244_QR_BOUND_DERIVATION_NONCLAIM.csv",
            ["QBD1244_0_projection", "4.6e-05"],
            "existing algebraic q_R_hat bound derivation.",
        ),
        (
            "SRC2038_06_1581_doc",
            ROOT / "1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md",
            ["CB1581_0_qRhat", "4.6e-05", "GATE1581_1_Cassini_bound"],
            "conditional Cassini bound row and profile derivation.",
        ),
        (
            "SRC2038_07_1581_bound_csv",
            OUT / "P8_Y5_PARENT_QLOC_1581_CASSINI_QR_BOUND_ROW_NONCLAIM.csv",
            ["CB1581_0_qRhat", "CONDITIONAL_BOUND_ROW_NONCLAIM"],
            "machine-readable conditional Cassini Q_R bound row.",
        ),
        (
            "SRC2038_08_1870_chain",
            OUT / "P8_Y5_PARENT_QLOC_1870_QR_ZR_MR2_SOURCE_CHAIN_AUDIT.csv",
            ["SCA1870_6_denominator", "CONDITIONAL_FORMULA_FOUND_NONCLAIM"],
            "later source-chain audit confirming denominator formula exists but inputs are missing.",
        ),
        (
            "SRC2038_09_1875_vector",
            OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
            ["RV1875_5_massless_tail", "MISSING_C_R_PIR_KAPPA_MSTAR_OR_ZERO_THEOREM"],
            "residual-vector row naming the massless tail blocker.",
        ),
        (
            "SRC2038_10_1876_arena",
            OUT / "P8_Y5_PARENT_QLOC_1876_ARENA_BLOCKING_DRYRUN.csv",
            ["AR1876_1_PPN_light_time", "BLOCKED_NONCLAIM"],
            "arena dry-run showing PPN/light-time score remains blocked.",
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


def scalar_from_1244_policy() -> tuple[float, int, float]:
    rows = read_csv_dicts(OUT / "P8_Y5_R10_1244_PPN_GAMMA_STATISTICAL_POLICY.csv")
    policy = next((row for row in rows if row.get("policy_id") == "STAT1244_0_default_smoke"), {})
    sigma = float(policy.get("sigma", "2.3e-5"))
    n_sigma = int(float(policy.get("N_sigma", "1")))
    c_r_norm_abs_max = 2.0 * n_sigma * sigma
    return sigma, n_sigma, c_r_norm_abs_max


def convention_rows(c_r_norm_abs_max: float) -> list[dict[str, object]]:
    data = [
        (
            "CONV2038_0_problem",
            "q_R_hat name collision",
            "1240 uses q_R_hat = Q_R c^2/(GM) with gamma_minus_1_QR ~ -q_R_hat/2; 1581 uses q_R_hat=-Q_R/(2 kappa_W G M)+tails.",
            "Do not merge q_R_hat rows by name.",
            "FACTOR_TWO_COLLISION_DETECTED",
        ),
        (
            "CONV2038_1_locked_symbol",
            "C_R_norm",
            "C_R_norm := Q_R/(kappa_W G M_*) in geometric units, or Q_R c^2/(kappa_W G M_*) if Q_R is stored as a length.",
            "Cassini gamma route uses gamma_minus_1_tail = -C_R_norm/2 + delta_tail.",
            "CANONICAL_2038_SYMBOL",
        ),
        (
            "CONV2038_2_bound",
            "C_R_norm absolute smoke bound",
            f"|C_R_norm + 2 delta_tail| <= {c_r_norm_abs_max:.6g} under the strict one-sigma smoke policy.",
            "If every tail is parent-zero, |C_R_norm| <= 4.6e-5.",
            "BOUND_TARGET_LOCKED_NONCLAIM",
        ),
    ]
    rows = []
    for row_id, item, statement, implication, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "statement": statement,
                "implication": implication,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def acquisition_rows(c_r_norm_abs_max: float) -> list[dict[str, object]]:
    data = [
        (
            "ACQ2038_0_C_R_norm_bound_target",
            "C_R_norm_abs_max",
            "external_bound_target",
            "abs(C_R_norm + 2 delta_tail) <= 2 N_sigma sigma_gamma",
            f"{c_r_norm_abs_max:.6g}",
            "dimensionless",
            "SRC2038_04_1244_stat_policy;SRC2038_05_1244_qr_bound;SRC2038_06_1581_doc;SRC2038_07_1581_bound_csv",
            "QBD1244_0_projection;CB1581_0_qRhat",
            "PPN_gamma;Cassini_light_time;orbital_massless_tail",
            "ACQUIRED_REAL_BOUND_TARGET_NONCLAIM",
            True,
            False,
            "not a prediction; no MTS source coefficient supplied",
        ),
        (
            "ACQ2038_1_Q_R_prediction_value",
            "Q_R or C_R_norm",
            "MTS_prediction_or_theorem_zero",
            "Q_R=0 from parent no-charge theorem or finite source-backed C_R_norm value",
            "MISSING_VALUE",
            "dimensionless after C_R_norm normalization",
            "SRC2038_08_1870_chain;SRC2038_09_1875_vector",
            "SCA1870_0_QR;RV1875_5_massless_tail",
            "PPN_gamma;local_GR;orbital",
            "MISSING_QR_VALUE_OR_PARENT_NO_CHARGE_THEOREM",
            False,
            False,
            "this is still the key missing theory row",
        ),
        (
            "ACQ2038_2_delta_tail_envelope",
            "delta_tail",
            "gauge_source_boundary_tail",
            "delta_tail = delta_gauge + delta_source + delta_boundary + delta_readout",
            "MISSING_COMPONENT_VECTOR",
            "dimensionless",
            "SRC2038_09_1875_vector;SRC2038_10_1876_arena",
            "RV1875_6_boundary_readout_tail;RV1875_9_no_cancellation",
            "PPN_gamma;R10;clock;orbital;local_GR",
            "MISSING_TAIL_ENVELOPE_AND_NO_CANCELLATION_GUARD",
            False,
            False,
            "without this, a small C_R_norm could be fake cancellation",
        ),
        (
            "ACQ2038_3_denominator_convention",
            "kappa_W and M_*",
            "normalization_denominator",
            "C_R_norm := Q_R/(kappa_W G M_*)",
            "SYMBOLIC_FORMULA_ONLY",
            "dimensionless target after normalization",
            "SRC2038_08_1870_chain",
            "SCA1870_6_denominator",
            "PPN_gamma;orbital_massless_tail",
            "FORMULA_PRESENT_INPUTS_MISSING",
            False,
            False,
            "source mass and kappa_W must be same-frame before score",
        ),
        (
            "ACQ2038_4_J_R_source_row",
            "J_R",
            "bulk_source_current",
            "Euler/source projection onto u=R_AB",
            "MISSING_VALUE",
            "MISSING_UNITS",
            "SRC2038_02_2037_candidates;SRC2038_09_1875_vector",
            "CAND2037_3_JR;RV1875_4_bulk_source_charges",
            "WEP;R10;clock;source_charge",
            "MISSING_SOURCE_CURRENT_OR_MATTER_DESCENT_ZERO",
            False,
            False,
            "not selected as first row because Q_R has the sharper PPN bound target",
        ),
        (
            "ACQ2038_5_B_R_boundary_row",
            "B_R/Pi_R",
            "boundary_source_current",
            "boundary functional derivative or momentum feeding Q_R",
            "MISSING_VALUE",
            "MISSING_UNITS",
            "SRC2038_02_2037_candidates;SRC2038_09_1875_vector",
            "CAND2037_5_BR;RV1875_6_boundary_readout_tail",
            "PPN;clock;orbital;R10;local_GR",
            "MISSING_BOUNDARY_RESOLUTION_OR_ABSOLUTE_TAIL_ENVELOPE",
            False,
            False,
            "second-best target after C_R_norm/Q_R because it owns tail silence",
        ),
    ]
    rows = []
    for (
        row_id,
        symbol,
        row_type,
        formula,
        value,
        units,
        source_paths,
        equation_refs,
        arena_targets,
        status,
        source_backed,
        prediction_ready,
        blocker,
    ) in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "row_type": row_type,
                "formula": formula,
                "value": value,
                "units": units,
                "normalization": "C_R_norm=Q_R/(kappa_W G M_*) canonical 2038 massless-tail convention",
                "source_paths": source_paths,
                "equation_refs": equation_refs,
                "arena_targets": arena_targets,
                "status": status,
                "source_backed": source_backed,
                "prediction_ready": prediction_ready,
                "score_ready": bool(source_backed and row_type == "external_bound_target"),
                "valid_prediction_row": False,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def score_readiness_rows(acquisition: list[dict[str, object]]) -> list[dict[str, object]]:
    bound_ready = any(row["row_id"] == "ACQ2038_0_C_R_norm_bound_target" and row["score_ready"] for row in acquisition)
    prediction_ready = any(row["prediction_ready"] for row in acquisition)
    tail_ready = any(row["symbol"] == "delta_tail" and row["status"] == "ACQUIRED_COMPONENT_VECTOR" for row in acquisition)
    data = [
        (
            "SCORE2038_0_bound_target",
            "Cassini/PPN bound target exists",
            "PASS_NONCLAIM" if bound_ready else "FAIL",
            "C_R_norm_abs_max is source-backed as an external guardrail.",
        ),
        (
            "SCORE2038_1_prediction",
            "MTS Q_R/C_R_norm prediction exists",
            "FAIL_MISSING_THEORY_ROW" if not prediction_ready else "REVIEW_REQUIRED",
            "No parent no-charge theorem and no finite predicted reciprocal charge value exist.",
        ),
        (
            "SCORE2038_2_tail_envelope",
            "tail/no-cancellation envelope exists",
            "FAIL_MISSING_TAIL_VECTOR" if not tail_ready else "REVIEW_REQUIRED",
            "Gauge/source/boundary/readout tail components remain missing.",
        ),
        (
            "SCORE2038_3_score_attempt",
            "PPN/Cassini score allowed",
            "NOT_RUN_BLOCKED",
            "Scoring requires prediction row plus tail envelope; bound target alone is not an MTS score.",
        ),
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


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2038_0_first_real_row",
            "first real row acquired",
            "PASS_BOUND_TARGET_ONLY",
            "A source-backed external C_R_norm bound target is acquired; this is not a prediction.",
        ),
        (
            "GATE2038_1_QR_prediction",
            "Q_R/C_R_norm source value or zero theorem",
            "FAIL_BLOCKED",
            "no parent no-charge theorem, no finite source value, no same-frame kappa_W/M_* convention.",
        ),
        (
            "GATE2038_2_factor_two",
            "q_R_hat convention collision resolved",
            "PASS_NONCLAIM",
            "2038 uses C_R_norm to prevent merging incompatible q_R_hat conventions.",
        ),
        (
            "GATE2038_3_local_GR",
            "derived local GR/Newton reduction",
            "FAIL_BLOCKED",
            "Q_R and tail silence remain unsigned; beta/source/common matter coupling still open.",
        ),
        (
            "GATE2038_4_public_claim",
            "R10/PPN/local-GR claim",
            "FAIL_BLOCKED",
            "bound target cannot be sold as an MTS prediction.",
        ),
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


def decision_rows(c_r_norm_abs_max: float) -> list[dict[str, object]]:
    data = [
        (
            "DEC2038_0_not_circling",
            "2038 takes the leap from placeholder residual slots to a real external bound target.",
            f"The massless reciprocal tail now has a concrete strict-smoke ceiling |C_R_norm| <= {c_r_norm_abs_max:.6g} if all tails vanish.",
        ),
        (
            "DEC2038_1_not_a_prediction",
            "The acquired row is a ruler, not an MTS hit.",
            "It lets us judge a future derived Q_R/C_R_norm value, but it does not provide that value.",
        ),
        (
            "DEC2038_2_best_next",
            "Next route should attack Q_R=0/tail silence or produce a finite C_R_norm prediction.",
            "This is sharper than more broad quotient-factorisation loops because it targets the massless PPN tail directly.",
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


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2038_0_2039",
            "target_doc": "2039-Y5-R2FR-QR-tail-envelope-or-parent-nocharge-row.md",
            "objective": "either prove parent-signed Q_R=0 with delta_tail=0, or derive a finite C_R_norm prediction plus absolute tail envelope and compare it to the 2038 Cassini/PPN bound target",
            "must_include": "Q_R no-charge theorem clauses; C_R_norm value route; kappa_W/M_* same-frame convention; delta_gauge/source/boundary/readout envelope; no-cancellation guard; PPN score refusal if missing",
            "excluded": "using Cassini central value as a fit target; closure benchmark as evidence; cancelling unknown tails; local-GR claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    convention: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    score: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2038_0_source_weight_bound",
            SOURCE_WEIGHT_DOCS / "AFRAME_C_R_NORM_BOUND_TARGET_2038_NONCLAIM.csv",
            acquisition,
        ),
        (
            "COPY2038_1_wep_score_block",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2038_SCORE_READINESS_NONCLAIM.csv",
            score,
        ),
        (
            "COPY2038_2_rab_queue_convention",
            QUEUE / "JR2038_C_R_NORM_CONVENTION_AND_QR_TARGET_NONCLAIM.csv",
            convention,
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
    convention: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    score: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    bound_row = next(row for row in acquisition if row["row_id"] == "ACQ2038_0_C_R_norm_bound_target")
    prediction_rows = [row for row in acquisition if row["prediction_ready"]]
    local_gate = next(row for row in gates if row["row_id"] == "GATE2038_3_local_GR")
    public_gate = next(row for row in gates if row["row_id"] == "GATE2038_4_public_claim")
    score_attempt = next(row for row in score if row["row_id"] == "SCORE2038_3_score_attempt")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2038_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2038_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2038_02_factor_two_locked", any(row["status"] == "CANONICAL_2038_SYMBOL" for row in convention), "C_R_norm convention locks the q_R_hat factor-of-two collision"))
    checks.append(("VAL2038_03_bound_numeric", float(bound_row["value"]) > 0.0 and bound_row["units"] == "dimensionless", "external C_R_norm bound target is positive and dimensionless"))
    checks.append(("VAL2038_04_bound_not_prediction", not bool(bound_row["valid_prediction_row"]) and not bool(bound_row["claim_allowed"]), "bound target is not promoted as an MTS prediction"))
    checks.append(("VAL2038_05_prediction_missing", len(prediction_rows) == 0, "no MTS Q_R/C_R_norm prediction row is accepted"))
    checks.append(("VAL2038_06_score_blocked", score_attempt["status"] == "NOT_RUN_BLOCKED", "PPN score is blocked until prediction and tail envelope exist"))
    checks.append(("VAL2038_07_local_claim_blocked", local_gate["status"] == "FAIL_BLOCKED" and public_gate["status"] == "FAIL_BLOCKED", "local/public claim gates remain blocked"))
    checks.append(("VAL2038_08_next_selected", next_rows_[0]["target_id"] == "NEXT2038_0_2039", "2039 target is selected"))
    checks.append(("VAL2038_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2038_10_no_formalization_2038_artifacts", not formalization_has_2038_artifacts(), "no 2038 artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2038_OVERALL", overall_ok, "2038 acquires a real external C_R_norm bound target and keeps theory claims blocked"))
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
    sigma_gamma: float,
    n_sigma: int,
    c_r_norm_abs_max: float,
    source_rows: list[dict[str, object]],
    convention: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    score: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2038 Y5 R2FR First Real u-Residual Source Row Acquisition",
        "",
        "## Current Verdict",
        "",
        f"2038 acquires the first real source-backed row in this local branch: a Cassini/PPN external bound target for the massless reciprocal tail, `|C_R_norm| <= {c_r_norm_abs_max:.6g}` under the strict one-sigma smoke policy (`sigma_gamma={sigma_gamma:.6g}`, `N_sigma={n_sigma}`), if all gauge/source/boundary/readout tails vanish.",
        "",
        "This is a real ruler, not a prediction. `Q_R`, `B_R`, `J_R`, the same-frame `kappa_W/M_*` normalization, and the absolute tail/no-cancellation vector remain missing. No local-GR, Newton, R10, PPN, WEP, clock, orbital, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Convention Lock",
        md_table(convention, ["row_id", "item", "statement", "implication", "status", "claim_allowed"]),
        "## Acquisition Rows",
        md_table(acquisition, ["row_id", "symbol", "row_type", "formula", "value", "units", "source_paths", "equation_refs", "status", "source_backed", "prediction_ready", "score_ready", "valid_prediction_row", "claim_allowed"]),
        "## Score Readiness",
        md_table(score, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sigma_gamma, n_sigma, c_r_norm_abs_max = scalar_from_1244_policy()
    source_rows = source_register_rows()
    convention = convention_rows(c_r_norm_abs_max)
    acquisition = acquisition_rows(c_r_norm_abs_max)
    score = score_readiness_rows(acquisition)
    gates = claim_gate_rows()
    decisions = decision_rows(c_r_norm_abs_max)
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2038_SOURCE_REGISTER.csv",
        "convention": OUT / "P8_Y5_PARENT_QLOC_2038_C_R_NORM_CONVENTION_LOCK.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv",
        "score": OUT / "P8_Y5_PARENT_QLOC_2038_SCORE_READINESS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2038_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2038_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2038_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2038_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2038_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["convention"], convention)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["score"], score)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(convention, acquisition, score)
    write_csv(paths["branch"], copies)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, convention, acquisition, score, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, convention, acquisition, score, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(
        sigma_gamma,
        n_sigma,
        c_r_norm_abs_max,
        source_rows,
        convention,
        acquisition,
        score,
        gates,
        decisions,
        next_rows_,
        copies,
        validation,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
