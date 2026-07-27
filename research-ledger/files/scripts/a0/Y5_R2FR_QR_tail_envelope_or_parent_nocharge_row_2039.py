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


DOC = ROOT / "2039-Y5-R2FR-QR-tail-envelope-or-parent-nocharge-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def formalization_has_2039_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2039*")) or any(FORMALIZATION.rglob("*QR*tail*nocharge*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2039_00_2038_handoff",
            ROOT / "2038-Y5-R2FR-first-real-u-residual-source-row-acquisition.md",
            ["NEXT2038_0_2039", "C_R_norm", "VAL2038_OVERALL"],
            "2038 selects Q_R no-charge or finite C_R_norm plus absolute tail envelope.",
        ),
        (
            "SRC2039_01_2038_next",
            OUT / "P8_Y5_PARENT_QLOC_2038_NEXT_TARGET.csv",
            ["NEXT2038_0_2039", "delta_gauge/source/boundary/readout envelope"],
            "machine-readable 2039 target.",
        ),
        (
            "SRC2039_02_2038_bound",
            OUT / "P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv",
            ["ACQ2038_0_C_R_norm_bound_target", "4.6e-05"],
            "real external Cassini/PPN C_R_norm bound target.",
        ),
        (
            "SRC2039_03_2038_convention",
            OUT / "P8_Y5_PARENT_QLOC_2038_C_R_NORM_CONVENTION_LOCK.csv",
            ["CONV2038_1_locked_symbol", "CANONICAL_2038_SYMBOL"],
            "C_R_norm factor-of-two convention lock.",
        ),
        (
            "SRC2039_04_1582_doc",
            ROOT / "1582-Y5-QR-no-charge-source-denominator-and-tail-envelope.md",
            ["NCS1582_4_verdict", "TAIL1582_5_higher_order", "VAL1582_OVERALL"],
            "older Q_R no-charge and absolute PPN tail-envelope checkpoint.",
        ),
        (
            "SRC2039_05_1582_nocharge_csv",
            OUT / "P8_Y5_PARENT_QLOC_1582_NO_CHARGE_SIGNATURE_AUDIT.csv",
            ["NCS1582_4_verdict", "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED"],
            "machine-readable no-charge signature audit.",
        ),
        (
            "SRC2039_06_1582_denominator_csv",
            OUT / "P8_Y5_PARENT_QLOC_1582_SOURCE_DENOMINATOR_CONTRACT.csv",
            ["SD1582_0_QR", "SD1582_1_kappaW", "SD1582_2_GM"],
            "source denominator contract for Q_R/(kappa_W GM).",
        ),
        (
            "SRC2039_07_1582_tail_csv",
            OUT / "P8_Y5_PARENT_QLOC_1582_PPN_TAIL_ENVELOPE.csv",
            ["TAIL1582_0_core", "TAIL1582_4_readout", "MISSING_SECOND_ORDER_CONTROL"],
            "absolute no-cancellation PPN tail envelope.",
        ),
        (
            "SRC2039_08_1583_tail_zero_csv",
            OUT / "P8_Y5_PARENT_QLOC_1583_PPN_TAIL_ZERO_THEOREM_ATTEMPT.csv",
            ["TZ1583_5_verdict", "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED"],
            "tail-zero theorem attempt remains unsigned.",
        ),
        (
            "SRC2039_09_1875_vector",
            OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
            ["RV1875_5_massless_tail", "RV1875_9_no_cancellation"],
            "later local residual vector confirming massless tail and no-cancellation blockers.",
        ),
        (
            "SRC2039_10_06_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Q_R = -Pi_R", "Pi_R = 0 -> Q_R = 0"],
            "original source-neutrality route: sufficient but not parent-signed.",
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


def c_r_norm_bound_value() -> float:
    rows = read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv")
    bound = next((row for row in rows if row.get("row_id") == "ACQ2038_0_C_R_norm_bound_target"), {})
    try:
        return float(bound.get("value", "4.6e-05"))
    except Exception:
        return 4.6e-05


def nocharge_contract_rows() -> list[dict[str, object]]:
    data = [
        (
            "NC2039_0_boundary_variation",
            "boundary stationarity relation",
            "delta S_boundary=[W R_AB' + Pi_R] delta R_AB|_surface",
            "Q_R=-Pi_R after exterior current integration and boundary convention lock",
            "FORMAL_RELATION_AVAILABLE",
            "does not by itself set Pi_R=0",
            False,
        ),
        (
            "NC2039_1_matter_descent",
            "ordinary matter descends through observed quotient geometry",
            "delta_{R_AB} S_matter_boundary=0",
            "no hidden matter/source reciprocal momentum",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "matter descent and source boundary class remain unsigned",
            False,
        ),
        (
            "NC2039_2_no_marker",
            "no source-only reciprocal marker",
            "partial S_source/partial R_AB=0 and no Weyl/disformal/shadow-frame source marker",
            "prevents source terms from regenerating Q_R",
            "CONTRACT_WRITTEN_NOT_DERIVED",
            "current parent action grammar still does not forbid every marker term",
            False,
        ),
        (
            "NC2039_3_boundary_class",
            "proper/free/exact source boundary class",
            "Pi_R=0 or exact/proper term has no exterior contribution",
            "Q_R=0 follows from Q_R=-Pi_R",
            "OPEN_NOT_SIGNED",
            "boundary/worldtube/corner class is not parent-owned",
            False,
        ),
        (
            "NC2039_4_denominator_lock",
            "same-frame kappa_W and M_*",
            "C_R_norm=Q_R/(kappa_W G M_*)",
            "finite route can be compared to Cassini target if Q_R is not zero",
            "FORMULA_PRESENT_INPUTS_MISSING",
            "kappa_W, M_*, domain and sign conventions remain missing",
            False,
        ),
        (
            "NC2039_5_theorem_verdict",
            "parent Q_R no-charge theorem",
            "NC2039_0 through NC2039_4 all parent-signed",
            "Q_R=0 and C_R_norm=0 before PPN tail corrections",
            "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED",
            "Pi_R=0/source-boundary neutrality is sufficient but not derived",
            False,
        ),
    ]
    rows = []
    for row_id, clause, equation, effect_if_signed, status, blocker, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "equation": equation,
                "effect_if_signed": effect_if_signed,
                "status": status,
                "blocker": blocker,
                "parent_signed": parent_signed,
                "valid_prediction_row": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def tail_zero_rows() -> list[dict[str, object]]:
    data = [
        (
            "TZ2039_0_gauge",
            "delta_gauge",
            "observed coframe/PPN radial gauge fixed before readout in same source frame",
            "delta_gauge=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "q/Obs_e/coframe tau lock remains unsigned",
        ),
        (
            "TZ2039_1_source",
            "delta_source",
            "same-frame Newtonian source denominator, no hidden source reciprocal momentum, matched source boundary",
            "delta_source=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "Q_R/Pi_R, kappa_W, M_*, and domain map are missing",
        ),
        (
            "TZ2039_2_boundary",
            "delta_boundary",
            "scalar-only stationary boundary collar with no vector/shear/normal flux and Ward flux closure",
            "delta_boundary=0",
            "CONDITIONAL_LEMMA_PARENT_OWNER_MISSING",
            "boundary no-flux theorem is conditional and not parent-owned",
        ),
        (
            "TZ2039_3_readout",
            "delta_readout",
            "ordinary matter/constants/readout descend through one observed coframe; no marker/shadow frame",
            "delta_readout=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "matter descent, no-marker and tau lock remain unsigned",
        ),
        (
            "TZ2039_4_higher_order",
            "delta_second_order",
            "beta=1, Bianchi-like conservation, and common matter coupling close post-linear PPN tail",
            "O(U_N) tail=0",
            "NOT_DERIVED",
            "beta, conservation and universal matter coupling remain open",
        ),
        (
            "TZ2039_5_verdict",
            "delta_tail",
            "TZ2039_0 through TZ2039_4 all parent-signed",
            "delta_tail=0",
            "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED",
            "at least gauge/source/boundary/readout/second-order clauses remain unsigned",
        ),
    ]
    rows = []
    for row_id, tail_component, zero_condition, effect_if_signed, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "tail_component": tail_component,
                "zero_condition": zero_condition,
                "effect_if_signed": effect_if_signed,
                "status": status,
                "blocker": blocker,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def budget_rows(bound: float) -> list[dict[str, object]]:
    data = [
        (
            "BUD2039_0_master",
            "absolute Cassini/PPN gamma budget",
            "|C_R_norm| + 2(|delta_gauge|+|delta_source|+|delta_boundary|+|delta_readout|+|delta_second_order|) <= C_R_norm_abs_max",
            bound,
            "dimensionless",
            "ACQUIRED_EXTERNAL_TARGET",
            "all component values are missing except the external ceiling",
        ),
        (
            "BUD2039_1_C_R_norm",
            "reciprocal massless tail",
            "|C_R_norm|",
            "MISSING_VALUE_OR_ZERO_THEOREM",
            "dimensionless",
            "MISSING_QR_VALUE_OR_PARENT_NOCHARGE",
            "requires Q_R=0 theorem or finite Q_R/kappa_W/M_* row",
        ),
        (
            "BUD2039_2_gauge",
            "gauge tail",
            "2|delta_gauge|",
            "MISSING_BOUND_OR_ZERO",
            "dimensionless",
            "MISSING_GAUGE_ZERO_OR_BOUND",
            "cannot cancel against C_R_norm",
        ),
        (
            "BUD2039_3_source",
            "source/interior tail",
            "2|delta_source|",
            "MISSING_BOUND_OR_ZERO",
            "dimensionless",
            "MISSING_SOURCE_ZERO_OR_BOUND",
            "requires same-frame source denominator and no hidden reciprocal momentum",
        ),
        (
            "BUD2039_4_boundary",
            "boundary/worldtube tail",
            "2|delta_boundary|",
            "MISSING_BOUND_OR_ZERO",
            "dimensionless",
            "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "must include Pi_R/B_R absolutely",
        ),
        (
            "BUD2039_5_readout",
            "matter/readout tail",
            "2|delta_readout|",
            "MISSING_BOUND_OR_ZERO",
            "dimensionless",
            "MISSING_READOUT_ZERO_OR_BOUND",
            "matter descent/no-marker/tau lock required",
        ),
        (
            "BUD2039_6_second_order",
            "post-linear PPN tail",
            "2|delta_second_order|",
            "MISSING_BOUND_OR_ZERO",
            "dimensionless",
            "MISSING_BETA_CONSERVATION_COMMON_MATTER",
            "gamma-channel control alone cannot prove local GR",
        ),
    ]
    rows = []
    for row_id, item, formula, value, units, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "formula": formula,
                "value": value,
                "units": units,
                "status": status,
                "blocker": blocker,
                "score_ready": row_id == "BUD2039_0_master",
                "valid_prediction_row": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def score_refusal_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2039_0_zero_branch",
            "Q_R=0 and delta_tail=0",
            "gamma_minus_1_tail=0",
            "REFUSED_UNSIGNED_THEOREM",
            "Q_R no-charge theorem and all tail-zero clauses are not parent-signed",
        ),
        (
            "RUN2039_1_finite_branch",
            "finite C_R_norm plus absolute tails",
            "|C_R_norm| + 2 sum_abs_tail <= 4.6e-05",
            "REFUSED_MISSING_COMPONENT_VALUES",
            "C_R_norm and every tail component value/bound are missing",
        ),
        (
            "RUN2039_2_cancellation_branch",
            "signed cancellation between C_R_norm and tails",
            "-C_R_norm/2 + delta_tail accidentally small",
            "REFUSED_NO_CANCELLATION_POLICY",
            "only absolute component budget is allowed",
        ),
        (
            "RUN2039_3_claim_branch",
            "local-GR/Newton/PPN claim",
            "gamma channel passes",
            "REFUSED_GAMMA_ONLY_SHORTCUT",
            "beta, conservation, Newton source normalization and universal matter coupling remain open",
        ),
    ]
    rows = []
    for row_id, branch, formula, runner_status, reason in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "formula": formula,
                "runner_status": runner_status,
                "reason": reason,
                "score_attempted": False,
                "score_allowed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def local_gr_completion_rows() -> list[dict[str, object]]:
    data = [
        ("LGR2039_0_gamma", "PPN gamma/light-time", "Q_R=0 or finite absolute C_R_norm/tail budget below bound", "BOUND_TARGET_EXISTS_PREDICTION_MISSING"),
        ("LGR2039_1_beta", "PPN beta/nonlinear metric", "derive beta=1 from same parent weak-field expansion", "MISSING_DERIVATION"),
        ("LGR2039_2_conservation", "Bianchi/source conservation", "derive conservation identity compatible with observed matter source", "MISSING_DERIVATION"),
        ("LGR2039_3_common_matter", "universal matter coframe/coupling", "ordinary matter, clocks, EM constants and source masses use one observed coframe", "MISSING_PARENT_SIGNATURE"),
        ("LGR2039_4_newton", "Newtonian source-normalized limit", "T^2=1-2U/c^2 and acceleration/source denominator match measured GM without post-fit absorption", "MISSING_SOURCE_NORMALIZATION"),
        ("LGR2039_5_verdict", "derived GR/Newton local branch", "all rows LGR2039_0 through LGR2039_4 parent-signed or absolutely bounded", "FAIL_BLOCKED"),
    ]
    rows = []
    for row_id, item, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "requirement": requirement,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2039_0_QR_nocharge", "parent-signed Q_R=0 theorem", "FAIL_BLOCKED", "Pi_R=0/source-boundary neutrality is sufficient but unsigned"),
        ("GATE2039_1_tail_zero", "delta_tail=0 theorem", "FAIL_BLOCKED", "gauge/source/boundary/readout/second-order zero clauses are unsigned"),
        ("GATE2039_2_finite_budget", "finite C_R_norm absolute budget score", "FAIL_MISSING_VALUES", "only external ceiling exists; no MTS component values"),
        ("GATE2039_3_gamma_channel", "PPN gamma score", "FAIL_BLOCKED", "zero and finite branches are both refused"),
        ("GATE2039_4_local_GR", "derived local GR/Newton branch", "FAIL_BLOCKED", "gamma-only route is insufficient; beta/conservation/common matter/Newton source normalization remain open"),
        ("GATE2039_5_public_claim", "public R10/PPN/local-GR claim", "FAIL_BLOCKED", "2039 is a private nonclaim theorem/score contract"),
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


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2039_0_nocharge_result",
            "Q_R=0 remains sufficient but not derived.",
            "The exact parent theorem now has explicit clauses; the current corpus does not parent-sign Pi_R=0 or boundary/source silence.",
        ),
        (
            "DEC2039_1_budget_result",
            "The Cassini target is now an absolute no-cancellation budget.",
            "A future finite branch must satisfy |C_R_norm| + 2 sum_abs_tail <= 4.6e-05; signed cancellation is refused.",
        ),
        (
            "DEC2039_2_not_circling",
            "The gamma-channel local blocker is now compressed into two missing artifacts.",
            "Missing artifact A: parent Q_R/tail-zero theorem. Missing artifact B: finite C_R_norm plus absolute tail component values.",
        ),
        (
            "DEC2039_3_next",
            "Move to beta/conservation/common matter rather than looping gamma again.",
            "Even a closed gamma channel would not prove GR reduction without beta=1, conservation/Bianchi structure, universal matter coframe and Newtonian source normalization.",
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
            "target_id": "NEXT2039_0_2040",
            "target_doc": "2040-Y5-R2FR-PPN-beta-conservation-common-matter-parent-signature.md",
            "objective": "derive or reject the parent signatures needed for beta=1, Bianchi-like conservation, universal observed matter coframe/coupling, and Newtonian source normalization, while carrying the 2039 gamma/Q_R budget as a locked subgate",
            "must_include": "beta weak-field coefficient map; conservation identity; matter coframe descent; clock/EM/source-mass common coupling; Newtonian GM denominator; refusal of gamma-only GR shortcut",
            "excluded": "reopening C_R_norm convention; using Cassini as a prediction; claiming local GR from gamma alone; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    nocharge: list[dict[str, object]],
    budget: list[dict[str, object]],
    local_gr: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2039_0_source_weight_nocharge",
            SOURCE_WEIGHT_DOCS / "AFRAME_QR_NOCHARGE_CONTRACT_2039_NONCLAIM.csv",
            nocharge,
        ),
        (
            "COPY2039_1_wep_budget",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2039_ABSOLUTE_BUDGET_NONCLAIM.csv",
            budget,
        ),
        (
            "COPY2039_2_rab_local_gr_completion",
            QUEUE / "JR2039_LOCAL_GR_COMPLETION_MAP_NONCLAIM.csv",
            local_gr,
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
    nocharge: list[dict[str, object]],
    tail_zero: list[dict[str, object]],
    budget: list[dict[str, object]],
    runner: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    master_budget = next(row for row in budget if row["row_id"] == "BUD2039_0_master")
    qr_verdict = next(row for row in nocharge if row["row_id"] == "NC2039_5_theorem_verdict")
    tail_verdict = next(row for row in tail_zero if row["row_id"] == "TZ2039_5_verdict")
    local_verdict = next(row for row in local_gr if row["row_id"] == "LGR2039_5_verdict")
    public_gate = next(row for row in gates if row["row_id"] == "GATE2039_5_public_claim")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2039_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2039_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2039_02_nocharge_not_promoted", qr_verdict["status"] == "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED", "Q_R no-charge theorem remains unsigned"))
    checks.append(("VAL2039_03_tail_zero_not_promoted", tail_verdict["status"] == "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED", "tail-zero theorem remains unsigned"))
    checks.append(("VAL2039_04_budget_numeric", float(master_budget["value"]) > 0.0 and master_budget["units"] == "dimensionless", "absolute C_R_norm budget ceiling is numeric and dimensionless"))
    checks.append(("VAL2039_05_runner_refuses", all(str(row["runner_status"]).startswith("REFUSED") for row in runner), "zero, finite, cancellation and gamma-only score branches are refused"))
    checks.append(("VAL2039_06_local_gr_blocked", local_verdict["status"] == "FAIL_BLOCKED", "local GR completion map remains blocked"))
    checks.append(("VAL2039_07_claim_gates_closed", public_gate["status"] == "FAIL_BLOCKED", "public claim gate remains closed"))
    checks.append(("VAL2039_08_next_selected", next_rows_[0]["target_id"] == "NEXT2039_0_2040", "2040 beta/conservation/common matter target is selected"))
    checks.append(("VAL2039_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2039_10_no_formalization_2039_artifacts", not formalization_has_2039_artifacts(), "no 2039 artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2039_OVERALL", overall_ok, "2039 compresses Q_R/tail gamma blocker and selects beta/conservation/common matter next"))
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
    bound: float,
    source_rows: list[dict[str, object]],
    nocharge: list[dict[str, object]],
    tail_zero: list[dict[str, object]],
    budget: list[dict[str, object]],
    runner: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2039 Y5 R2FR QR Tail Envelope Or Parent Nocharge Row",
        "",
        "## Current Verdict",
        "",
        f"2039 does **not** prove `Q_R=0`, but it compresses the gamma-channel blocker into a precise theorem-or-budget contract. The theorem route requires parent-signed `Pi_R=0` plus all PPN tails zero. The finite route must satisfy the no-cancellation budget `|C_R_norm| + 2Σ|delta_tail_i| <= {bound:.6g}`.",
        "",
        "The current corpus supplies the external bound target and formal relations, but not the MTS prediction row, not the `Pi_R=0` theorem, and not the absolute tail component values. No local-GR, Newton, R10, PPN, WEP, clock, orbital, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Parent No-Charge Contract",
        md_table(nocharge, ["row_id", "clause", "equation", "effect_if_signed", "status", "blocker", "parent_signed", "claim_allowed"]),
        "## Tail-Zero Audit",
        md_table(tail_zero, ["row_id", "tail_component", "zero_condition", "effect_if_signed", "status", "blocker", "parent_signed", "claim_allowed"]),
        "## Absolute Budget",
        md_table(budget, ["row_id", "item", "formula", "value", "units", "status", "blocker", "score_ready", "valid_prediction_row", "claim_allowed"]),
        "## Score Refusal Runner",
        md_table(runner, ["row_id", "branch", "formula", "runner_status", "reason", "score_allowed", "claim_allowed"]),
        "## Local GR Completion Map",
        md_table(local_gr, ["row_id", "item", "requirement", "status", "claim_allowed"]),
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
    bound = c_r_norm_bound_value()
    source_rows = source_register_rows()
    nocharge = nocharge_contract_rows()
    tail_zero = tail_zero_rows()
    budget = budget_rows(bound)
    runner = score_refusal_rows()
    local_gr = local_gr_completion_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2039_SOURCE_REGISTER.csv",
        "nocharge": OUT / "P8_Y5_PARENT_QLOC_2039_PARENT_NOCHARGE_THEOREM_CONTRACT.csv",
        "tailzero": OUT / "P8_Y5_PARENT_QLOC_2039_TAIL_ZERO_AUDIT.csv",
        "budget": OUT / "P8_Y5_PARENT_QLOC_2039_CASSINI_ABSOLUTE_BUDGET.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2039_SCORE_REFUSAL_RUNNER.csv",
        "localgr": OUT / "P8_Y5_PARENT_QLOC_2039_LOCAL_GR_COMPLETION_MAP.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2039_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2039_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2039_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2039_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2039_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["nocharge"], nocharge)
    write_csv(paths["tailzero"], tail_zero)
    write_csv(paths["budget"], budget)
    write_csv(paths["runner"], runner)
    write_csv(paths["localgr"], local_gr)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(nocharge, budget, local_gr)
    write_csv(paths["branch"], copies)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, nocharge, tail_zero, budget, runner, local_gr, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, nocharge, tail_zero, budget, runner, local_gr, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(bound, source_rows, nocharge, tail_zero, budget, runner, local_gr, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
