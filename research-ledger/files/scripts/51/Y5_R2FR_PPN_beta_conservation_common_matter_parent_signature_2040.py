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


DOC = ROOT / "2040-Y5-R2FR-PPN-beta-conservation-common-matter-parent-signature.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2040_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2040-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2040*",
            "*Y5_R2FR_PPN_beta_conservation_common_matter_parent_signature_2040*",
        )
        return any(
            path.is_file()
            for pattern in artifact_patterns
            for path in FORMALIZATION.rglob(pattern)
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
            "SRC2040_00_2039_handoff",
            ROOT / "2039-Y5-R2FR-QR-tail-envelope-or-parent-nocharge-row.md",
            ["NEXT2039_0_2040", "VAL2039_OVERALL", "gamma-only"],
            "2039 locks Q_R/gamma as a subgate and selects beta/conservation/common matter.",
        ),
        (
            "SRC2040_01_2039_next",
            OUT / "P8_Y5_PARENT_QLOC_2039_NEXT_TARGET.csv",
            ["NEXT2039_0_2040", "beta weak-field coefficient map"],
            "machine-readable 2040 target.",
        ),
        (
            "SRC2040_02_2039_localgr",
            OUT / "P8_Y5_PARENT_QLOC_2039_LOCAL_GR_COMPLETION_MAP.csv",
            ["LGR2039_1_beta", "LGR2039_2_conservation", "LGR2039_4_newton"],
            "post-gamma local GR completion map.",
        ),
        (
            "SRC2040_03_1584_doc",
            ROOT / "1584-Y5-PPN-beta-conservation-common-matter-gate.md",
            ["BETA1584_4_verdict", "CONS1584_4_verdict", "VAL1584_OVERALL"],
            "older beta/conservation/common matter gate.",
        ),
        (
            "SRC2040_04_1585_doc",
            ROOT / "1585-Y5-EH-source-normalized-parent-action-owner-or-beta-residual-ledger.md",
            ["OWN1585_5_verdict", "BRL1585_7_total_no_cancellation", "VAL1585_OVERALL"],
            "EH source-normalized parent owner contract and beta residual ledger.",
        ),
        (
            "SRC2040_05_1585_beta_ledger",
            OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv",
            ["BRL1585_0_delta_beta_source", "BRL1585_7_total_no_cancellation"],
            "machine-readable beta residual no-cancellation ledger.",
        ),
        (
            "SRC2040_06_1585_runner",
            OUT / "P8_Y5_PARENT_QLOC_1585_LOCAL_GR_REDUCTION_RUNNER.csv",
            ["RUN1585_4_current_local_gr", "BLOCKED_NO_CLAIM"],
            "local-GR runner refusing conditional-owner promotion.",
        ),
        (
            "SRC2040_07_956_spine",
            ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
            ["SSG956_5_source_side_verdict", "LHG956_5_PPN_completion", "DEC956_2_project_overview"],
            "source-side and left-hand EH/Newton gate map.",
        ),
        (
            "SRC2040_08_957_spine",
            ROOT / "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
            ["PLG957_2_EH_operator", "ORD957_1", "DEC957_0_branch_choice"],
            "ordered local-GR spine selecting EH/operator before measured GM.",
        ),
        (
            "SRC2040_09_958_eh",
            ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
            ["EH958_5_verdict", "R11REV958_1", "DEC958_2_next_route"],
            "EH operator selection attempt and R11/nonEH fallback priority.",
        ),
        (
            "SRC2040_10_957_csv",
            OUT / "P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
            ["PLG957_2_EH_operator", "PLG957_5_PPN_completion"],
            "machine-readable local-GR spine ledger.",
        ),
        (
            "SRC2040_11_956_left_hand",
            OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
            ["LHG956_0_EH_core_selection", "LHG956_5_PPN_completion"],
            "machine-readable left-hand EH/Newton gate map.",
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


def integrated_spine_rows() -> list[dict[str, object]]:
    data = [
        (
            "SPINE2040_0_observed_frame",
            "one observed frame",
            "matter, clocks, photons, source masses, orbital readout and PPN coordinates use one observed coframe through O(U^2)",
            "conditional_from_prior_source_side",
            "coframe/tau/readout lock remains unsigned",
            "required_before_all",
        ),
        (
            "SPINE2040_1_gamma_QR",
            "gamma/Q_R massless tail",
            "2039 budget: |C_R_norm| + 2 sum_abs_tail <= 4.6e-05 or Q_R=0 and tails=0",
            "LOCKED_SUBGATE_NOT_CLOSED",
            "Q_R theorem/value and tail vector missing",
            "do_not_reopen_without_new_QR_input",
        ),
        (
            "SPINE2040_2_beta",
            "PPN beta",
            "beta_minus_1=0 from EH one-parameter exterior or finite no-cancellation beta residual ledger below bound",
            "MISSING_DERIVATION",
            "delta_beta_source/R11/q_loc/boundary/readout/conservation/source-normalization rows missing",
            "active_gate",
        ),
        (
            "SPINE2040_3_conservation",
            "Bianchi/source conservation",
            "observed Hilbert source conservation with projected extra-current, commutator and anomaly terms zero or retained",
            "MISSING_PROJECTED_CONSERVATION_THEOREM",
            "total Ward identity is insufficient",
            "active_gate",
        ),
        (
            "SPINE2040_4_common_matter",
            "universal matter coupling",
            "all matter sectors use same observed coframe with fixed constants and no source-only marker/readout shadow",
            "MISSING_PARENT_SIGNATURE",
            "coframe ownership, tau lock, no-marker and matter descent unsigned",
            "active_gate",
        ),
        (
            "SPINE2040_5_newton_GM",
            "Newtonian measured-GM source normalization",
            "EH mass/source charge equals measured orbital GM with no derivative/range/species/frame hair",
            "MISSING_SOURCE_NORMALIZATION",
            "worldtube/Gauss/orbital/source-current scorecard unfilled",
            "active_gate_downstream_of_EH",
        ),
        (
            "SPINE2040_6_EH_operator",
            "EH/no-extra-field operator owner",
            "local exterior operator is EH plus harmless Lambda/background; all nonEH/R11 families zero or bounded",
            "NOT_PARENT_DERIVED_HIGHEST_PRIORITY",
            "second-order metric-only/no-extra-field premises remain open",
            "upstream_next_attack",
        ),
        (
            "SPINE2040_7_verdict",
            "derived local GR/Newton branch",
            "all spine rows parent-signed or every residual row source-backed below bounds without cancellation",
            "FAIL_BLOCKED",
            "conditional route is clear but current corpus does not derive it",
            "no_claim",
        ),
    ]
    rows = []
    for row_id, layer, requirement, status, blocker, role in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "layer": layer,
                "requirement": requirement,
                "status": status,
                "blocker": blocker,
                "role": role,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def parent_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "THM2040_0_parent_owner",
            "single parent action owns observed metric/coframe, matter, source normalization, EH/local operator, boundary policy and residual sectors",
            "prevents combining imported GR dynamics with MTS source/readout assumptions",
            "CONDITIONAL_TARGET_NOT_SIGNED",
        ),
        (
            "THM2040_1_EH_operator",
            "local 4D diffeomorphism-invariant metric-only second-order exterior action with no extra exterior fields",
            "selects EH+Lambda operator up to normalization and harmless boundary terms",
            "CENTRAL_BLOCKER_NOT_DERIVED",
        ),
        (
            "THM2040_2_matter_source",
            "universal Hilbert matter action and same observed coframe for clocks/EM/source/orbital readout",
            "gives common matter coupling and observed source current",
            "MISSING_COMMON_MATTER_SIGNATURE",
        ),
        (
            "THM2040_3_conservation",
            "parent diffeomorphism/Ward identity projects to observed Hilbert source conservation with no hidden flux",
            "makes Bianchi/source compatibility physical, not a bookkeeping trick",
            "MISSING_PROJECTED_CONSERVATION_ZERO",
        ),
        (
            "THM2040_4_newton_GM",
            "worldtube/source charge equals EH mass parameter and measured orbital GM",
            "derives Newtonian mechanics source denominator rather than borrowing it",
            "MISSING_MEASURED_GM_CALIBRATION",
        ),
        (
            "THM2040_5_beta",
            "one-parameter EH exterior has no independent U^2 leakage",
            "yields beta=1 after measured-GM normalization",
            "MISSING_SECOND_ORDER_RESIDUAL_CONTROL",
        ),
        (
            "THM2040_6_gamma_subgate",
            "2039 Q_R/tail subgate closes or finite absolute budget passes",
            "keeps gamma/light-time channel compatible with the same parent branch",
            "LOCKED_SUBGATE_NOT_CLOSED",
        ),
        (
            "THM2040_7_local_GR_corollary",
            "THM2040_0 through THM2040_6 all parent-signed or source-bounded",
            "then local GR/Newton branch becomes a serious derivation candidate",
            "FAIL_CURRENT_CLAIM_NOT_DERIVED",
        ),
    ]
    rows = []
    for row_id, premise, effect_if_signed, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "premise": premise,
                "effect_if_signed": effect_if_signed,
                "status": status,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def beta_residual_import_rows() -> list[dict[str, object]]:
    source_rows = read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv")
    rows = []
    for source in source_rows:
        row = base_row()
        row.update(
            {
                "row_id": source.get("residual_id", "MISSING_ID"),
                "symbol": source.get("symbol", ""),
                "formula_or_map": source.get("formula_or_map", ""),
                "current_status": source.get("current_status", ""),
                "units": source.get("units", ""),
                "bound_or_target": source.get("bound_or_target", ""),
                "no_cancellation": source.get("no_cancellation", "True"),
                "source_backed": source.get("source_backed", "False"),
                "score_ready": source.get("score_ready", "False"),
                "valid_prediction_row": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def route_selection_rows() -> list[dict[str, object]]:
    data = [
        (
            "ROUTE2040_0_gamma",
            "Q_R/gamma subgate",
            "locked_subgate",
            "do not spend more turns circling gamma unless a new Q_R theorem/value or tail row appears",
            "carry forward as prerequisite",
        ),
        (
            "ROUTE2040_1_EH_operator",
            "EH/no-extra-field operator owner",
            "selected_next",
            "upstream of beta=1, measured-GM charge transfer and PPN residual completion",
            "attempt second-order metric-only no-extra-field parent clause",
        ),
        (
            "ROUTE2040_2_R11_fallback",
            "R11/nonEH residual vector",
            "fallback_if_EH_unsigned",
            "all current R11 rows are rejected as non-executable but priority families are known",
            "fill R2/fR scalar and torsion/nonmetricity rows first",
        ),
        (
            "ROUTE2040_3_GM",
            "measured-GM/worldtube calibration",
            "queued_second",
            "essential for Newton but depends on EH charge baseline and extra-sector silence",
            "derive immediately after EH/no-extra-field decision",
        ),
        (
            "ROUTE2040_4_beta_score",
            "Will/LLR beta comparator",
            "not_run",
            "external bound exists but no MTS beta prediction or residual component values exist",
            "only score after beta residual ledger is filled",
        ),
    ]
    rows = []
    for row_id, route, selection, rationale, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "selection": selection,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    data = [
        ("RUN2040_0_gamma_only", "claim local GR from 2039 gamma/Q_R budget", "REFUSED_GAMMA_ONLY_SHORTCUT", "beta, conservation, common matter and Newton-GM gates remain open"),
        ("RUN2040_1_conditional_EH_owner", "use source-normalized EH parent theorem as current MTS evidence", "REFUSED_REFERENCE_PROMOTION", "the theorem target is exact but owner clauses are not parent-signed"),
        ("RUN2040_2_total_Ward", "use total Ward identity as observed conservation proof", "REFUSED_PROJECTED_CONSERVATION_SHORTCUT", "projected extra-current/commutator/anomaly obstruction remains"),
        ("RUN2040_3_beta_score", "score beta comparator", "NOT_RUN_PREDICTION_MISSING", "beta residual ledger has no source-backed component values"),
        ("RUN2040_4_newton_first_order", "promote first-order Newton-looking limit to GR", "REFUSED_FIRST_ORDER_SHORTCUT", "measured GM and second-order beta/source normalization are separate gates"),
        ("RUN2040_5_local_GR", "claim derived local GR/Newton", "BLOCKED_NO_CLAIM", "EH/no-extra-field, GM, beta, conservation and common matter gates are all unresolved"),
    ]
    rows = []
    for row_id, branch, status, reason in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "runner_status": status,
                "reason": reason,
                "score_attempted": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2040_0_gamma_subgate", "Q_R/gamma local bound", "FAIL_LOCKED_SUBGATE_OPEN", "2039 budget exists but prediction/theorem/tails missing"),
        ("GATE2040_1_beta", "beta=1 or beta residual below bound", "FAIL_BLOCKED", "beta residual ledger unfilled"),
        ("GATE2040_2_conservation", "source-compatible Bianchi conservation", "FAIL_BLOCKED", "projected obstruction not zero"),
        ("GATE2040_3_common_matter", "universal matter coframe/coupling", "FAIL_BLOCKED", "coframe/tau/no-marker/matter descent unsigned"),
        ("GATE2040_4_newton_GM", "Newtonian measured-GM normalization", "FAIL_BLOCKED", "worldtube/Gauss/source-current calibration open"),
        ("GATE2040_5_EH_operator", "EH/no-extra-field operator owner", "FAIL_BLOCKED", "second-order metric-only no-extra-field premise unsigned"),
        ("GATE2040_6_local_GR", "derived local GR/Newton branch", "FAIL_BLOCKED", "conditional spine is ordered but not derived"),
        ("GATE2040_7_public_claim", "public local-GR/PPN/R10 claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
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
            "DEC2040_0_integrated_spine",
            "The local-GR bridge is now ordered rather than foggy.",
            "Gamma/Q_R is a locked subgate; beta, conservation, common matter, Newton-GM and EH/no-extra-field are the remaining live gates.",
        ),
        (
            "DEC2040_1_conditional_theorem",
            "A serious derivation route exists as a parent-action theorem target.",
            "If one parent action signs EH/no-extra-field, universal matter, conservation, measured GM, no U2 leakage and the 2039 gamma subgate, local GR becomes a real candidate.",
        ),
        (
            "DEC2040_2_current_status",
            "The current corpus does not yet derive the parent-action theorem.",
            "The blockers are not vague anymore: EH/no-extra-field is upstream, measured-GM is next, and beta residual rows are fallback evidence only.",
        ),
        (
            "DEC2040_3_next",
            "Attack EH/no-extra-field before measured-GM.",
            "This matches the 957/958 dependency order and prevents borrowing Newtonian GM before the local operator/charge baseline is owned.",
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
            "target_id": "NEXT2040_0_2041",
            "target_doc": "2041-Y5-R2FR-second-order-no-extra-field-parent-clause-or-R11-priority-fill.md",
            "objective": "try to derive the local second-order metric-only no-extra-field parent clause that selects EH; if unsigned, produce first priority executable R11/nonEH rows, starting with R2/fR scalar mode and torsion/nonmetricity, with source paths, units, weak-field maps and no-claim gates",
            "must_include": "Lovelock-style premise audit; no-extra-field theorem attempt; R2/fR scalar mode; torsion/nonmetricity; source-normalization/projector residual watch; refusal of local-GR claim",
            "excluded": "measured-GM claim before EH baseline; beta score without prediction; gamma-only shortcut; invented coefficients; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    spine: list[dict[str, object]],
    theorem: list[dict[str, object]],
    route: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2040_0_source_weight_spine",
            SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_GR_SPINE_2040_NONCLAIM.csv",
            spine,
        ),
        (
            "COPY2040_1_wep_theorem_contract",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2040_PARENT_THEOREM_CONTRACT_NONCLAIM.csv",
            theorem,
        ),
        (
            "COPY2040_2_rab_route_selection",
            QUEUE / "JR2040_EH_OPERATOR_NEXT_ROUTE_NONCLAIM.csv",
            route,
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
    spine: list[dict[str, object]],
    theorem: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    route: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    spine_verdict = next(row for row in spine if row["row_id"] == "SPINE2040_7_verdict")
    theorem_verdict = next(row for row in theorem if row["row_id"] == "THM2040_7_local_GR_corollary")
    route_selected = next(row for row in route if row["row_id"] == "ROUTE2040_1_EH_operator")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2040_6_local_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2040_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2040_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2040_02_spine_integrated", spine_verdict["status"] == "FAIL_BLOCKED", "integrated local-GR spine exists and remains blocked"))
    checks.append(("VAL2040_03_theorem_not_promoted", theorem_verdict["status"] == "FAIL_CURRENT_CLAIM_NOT_DERIVED", "conditional parent-action theorem is not promoted"))
    checks.append(("VAL2040_04_beta_ledger_imported", any(row["row_id"] == "BRL1585_7_total_no_cancellation" for row in beta_rows), "beta residual no-cancellation ledger imported"))
    checks.append(("VAL2040_05_runner_blocks", all(str(row["runner_status"]).startswith(("REFUSED", "NOT_RUN", "BLOCKED")) for row in runner), "runner blocks gamma-only, reference theorem, Ward-only, beta-score and local-GR shortcuts"))
    checks.append(("VAL2040_06_route_selected", route_selected["selection"] == "selected_next", "EH/no-extra-field route selected next"))
    checks.append(("VAL2040_07_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local GR claim gate remains closed"))
    checks.append(("VAL2040_08_next_selected", next_rows_[0]["target_id"] == "NEXT2040_0_2041", "2041 EH/no-extra-field or R11 priority fill target selected"))
    checks.append(("VAL2040_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2040_10_no_formalization_2040_artifacts", not formalization_has_2040_artifacts(), "no 2040 artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2040_OVERALL", overall_ok, "2040 integrates the post-gamma local-GR spine and selects EH/no-extra-field next"))
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
    spine: list[dict[str, object]],
    theorem: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    route: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2040 Y5 R2FR PPN Beta Conservation Common Matter Parent Signature",
        "",
        "## Current Verdict",
        "",
        "2040 integrates the post-gamma local-GR spine. The `Q_R`/gamma problem is now a locked subgate from 2039, not the whole fight. The remaining local-GR bridge requires beta control, source-compatible Bianchi conservation, universal matter/coframe coupling, Newtonian measured-`GM` normalization, and an EH/no-extra-field local operator owner.",
        "",
        "A clean parent-action theorem target exists, but the current corpus does not parent-sign it. The next upstream attack is the EH/no-extra-field clause; if that stays unsigned, the fallback is executable R11/nonEH residual rows. No local-GR, Newton, PPN, R10, WEP, clock, orbital, beta, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Integrated Local-GR Spine",
        md_table(spine, ["row_id", "layer", "requirement", "status", "blocker", "role", "claim_allowed"]),
        "## Parent Theorem Contract",
        md_table(theorem, ["row_id", "premise", "effect_if_signed", "status", "parent_signed", "claim_allowed"]),
        "## Beta Residual Ledger Import",
        md_table(beta_rows, ["row_id", "symbol", "formula_or_map", "current_status", "units", "bound_or_target", "no_cancellation", "score_ready", "claim_allowed"]),
        "## Route Selection",
        md_table(route, ["row_id", "route", "selection", "rationale", "next_action", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["row_id", "branch", "runner_status", "reason", "score_attempted", "claim_allowed"]),
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
    source_rows = source_register_rows()
    spine = integrated_spine_rows()
    theorem = parent_theorem_rows()
    beta_rows = beta_residual_import_rows()
    route = route_selection_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2040_SOURCE_REGISTER.csv",
        "spine": OUT / "P8_Y5_PARENT_QLOC_2040_INTEGRATED_LOCAL_GR_SPINE.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2040_PARENT_THEOREM_CONTRACT.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2040_BETA_RESIDUAL_LEDGER_IMPORT.csv",
        "route": OUT / "P8_Y5_PARENT_QLOC_2040_ROUTE_SELECTION.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2040_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2040_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2040_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2040_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2040_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2040_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["spine"], spine)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["route"], route)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(spine, theorem, route)
    write_csv(paths["branch"], copies)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, spine, theorem, beta_rows, route, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, spine, theorem, beta_rows, route, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(source_rows, spine, theorem, beta_rows, route, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
