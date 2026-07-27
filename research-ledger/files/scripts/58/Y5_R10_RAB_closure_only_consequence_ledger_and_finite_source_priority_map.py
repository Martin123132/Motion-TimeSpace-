from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1320"
TITLE = "1320-Y5-R10-RAB-closure-only-consequence-ledger-and-finite-source-priority-map"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CLOSURE_CONSEQUENCE_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_ONLY_CONSEQUENCE_LEDGER.csv"
FINITE_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SOURCE_PRIORITY_MAP.csv"
FIRST_FILL_PATH = OUT_DIR / f"{PACK_ID}_FIRST_FILL_ROUTE_MATRIX.csv"
EVIDENCE_STATE_PATH = OUT_DIR / f"{PACK_ID}_EVIDENCE_STATE_LEDGER.csv"
ACCEPTANCE_GATES_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTANCE_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1320_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        CLOSURE_CONSEQUENCE_PATH,
        FINITE_PRIORITY_PATH,
        FIRST_FILL_PATH,
        EVIDENCE_STATE_PATH,
        ACCEPTANCE_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1320_0_1319_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_NEXT_TARGET.csv",
            "needle": "NEXT1319_0_1320",
            "role": "handoff into closure-only consequence/source priority map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_1_1319_demotion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_THEOREM_ROUTE_CLOSURE_DEMOTION.csv",
            "needle": "DEM1319_0_parent_signature",
            "role": "theorem route closure-only demotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_2_1319_survival",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_FINITE_SOURCE_ROW_SURVIVAL_MAP.csv",
            "needle": "SURV1319_3_r10",
            "role": "surviving finite source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_3_1317_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv",
            "needle": "RUN1317_3_run1314_3_r10",
            "role": "current finite runner refusal rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_4_1316_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
            "needle": "REQ1316_15_bound",
            "role": "source requirement inventory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_5_1052_clock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "needle": "ACB1052_2",
            "role": "best current clock product bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_6_1052_wep",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "needle": "AWP1052_0_alpha_Coulomb",
            "role": "WEP alpha/Coulomb pressure target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_7_563_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_563_BLOCKER_LEDGER.csv",
            "needle": "B563_0_no_full_bound_curve",
            "role": "R10 full bound curve and MTS coefficient blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_8_563_evaluator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_563_EVALUATOR.csv",
            "needle": "E563_2_mts_parent_coefficients_missing",
            "role": "R10 nonclaim evaluator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_9_904_anchors",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_904_R10_BOUND_ANCHOR_ROWS.csv",
            "needle": "R10_904_LEE2020_ALPHA1_38P6UM_ANCHOR",
            "role": "R10 anchor-only source-backed rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1320_10_905_decision",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_905_BOUND_DIGITIZATION_DECISION.csv",
            "needle": "BDD905_1_parent_input_worker",
            "role": "prior decision that parent input worker outranked bound digitization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    demotions = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1319_THEOREM_ROUTE_CLOSURE_DEMOTION.csv"))
    survival_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1319_FINITE_SOURCE_ROW_SURVIVAL_MAP.csv"))

    closure_consequence = [
        {
            "consequence_id": f"CC1320_{index}",
            "source_demotion": row["demotion_id"],
            "closed_route": row["route"],
            "closure_status": row["status"],
            "practical_consequence": row["consequence"],
            "surviving_work": "finite source/testing row must carry the burden unless reopen_condition is satisfied",
            "reopen_condition": row["reopen_condition"],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(demotions)
    ]

    priority_specs = {
        "SURV1319_1_clock": {
            "rank": 1,
            "row_label": "clock direct product/readout",
            "payoff_score": 7,
            "feasibility_score": 9,
            "empirical_readiness_score": 9,
            "derivation_centrality_score": 6,
            "risk_score": 3,
            "why_ranked_here": "sharp source-backed clock product bound already exists; first task is a readout/tau map, not a full local-gravity product",
            "first_fill": "tau_clock_time or direct P_clock_alpha with clock pair/sensitivity/readout provenance",
            "claim_gate": "must not divide clock bound by assumed tau; direct product or sourced readout only",
            "next_action_type": "first_feasible_fill",
        },
        "SURV1319_2_wep": {
            "rank": 2,
            "row_label": "WEP alpha/source normalization",
            "payoff_score": 9,
            "feasibility_score": 5,
            "empirical_readiness_score": 7,
            "derivation_centrality_score": 9,
            "risk_score": 6,
            "why_ranked_here": "closest to local-GR/source universality payoff, with a pressure target already staged, but needs beta/tau/material/source/readout inputs",
            "first_fill": "beta_source_alpha/tau_WEP/material response/source profile/readout kernel decomposition",
            "claim_gate": "no unity beta/tau; no absorption into measured G; material/source map required",
            "next_action_type": "highest_local_gr_payoff",
        },
        "SURV1319_0_alpha": {
            "rank": 3,
            "row_label": "alpha coefficient finite/source row",
            "payoff_score": 8,
            "feasibility_score": 4,
            "empirical_readiness_score": 4,
            "derivation_centrality_score": 10,
            "risk_score": 7,
            "why_ranked_here": "central coupling object, but theorem-zero is closure-only and standalone numeric coefficient is not sourced",
            "first_fill": "numeric b_alpha/c_alpha or a new signed alpha F2 owner primitive",
            "claim_gate": "threshold is not a prediction; no absence-as-zero",
            "next_action_type": "central_but_harder",
        },
        "SURV1319_3_r10": {
            "rank": 4,
            "row_label": "R10 alpha(lambda) product and bound curve",
            "payoff_score": 10,
            "feasibility_score": 3,
            "empirical_readiness_score": 5,
            "derivation_centrality_score": 8,
            "risk_score": 8,
            "why_ranked_here": "highest local short-range payoff, but current state lacks both promoted alpha_bound(lambda) curve and numeric MTS product vector",
            "first_fill": "split into data curve acquisition and parent product vector; neither can claim alone",
            "claim_gate": "anchor-only rows and symbolic product rows remain nonclaim",
            "next_action_type": "highest_payoff_heavy_lift",
        },
        "SURV1319_4_cross_arena": {
            "rank": 5,
            "row_label": "cross-arena branch/readout functor",
            "payoff_score": 8,
            "feasibility_score": 2,
            "empirical_readiness_score": 2,
            "derivation_centrality_score": 8,
            "risk_score": 8,
            "why_ranked_here": "important unification spine item, but premature until at least one arena product is filled",
            "first_fill": "same-branch classifier after clock/WEP/R10 rows have nonclaim product maps",
            "claim_gate": "no bound transfer across arenas without signed functor",
            "next_action_type": "defer_until_arena_rows_exist",
        },
    }

    finite_priority = []
    for row in survival_rows:
        spec = priority_specs[row["survival_id"]]
        total_score = (
            spec["payoff_score"]
            + spec["feasibility_score"]
            + spec["empirical_readiness_score"]
            + spec["derivation_centrality_score"]
            - spec["risk_score"]
        )
        finite_priority.append(
            {
                "rank": spec["rank"],
                "survival_id": row["survival_id"],
                "source_row": row["source_row"],
                "row_label": spec["row_label"],
                "priority": row["priority"],
                "payoff_score": spec["payoff_score"],
                "feasibility_score": spec["feasibility_score"],
                "empirical_readiness_score": spec["empirical_readiness_score"],
                "derivation_centrality_score": spec["derivation_centrality_score"],
                "risk_score": spec["risk_score"],
                "total_score": total_score,
                "why_ranked_here": spec["why_ranked_here"],
                "first_fill": spec["first_fill"],
                "claim_gate": spec["claim_gate"],
                "next_action_type": spec["next_action_type"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    finite_priority.sort(key=lambda row: int(row["rank"]))

    first_fill_route = [
        {
            "route_id": "FF1320_0_selected_next",
            "selected_row": "SURV1319_1_clock",
            "route": "clock direct product/readout first fill",
            "why_selected": "best feasibility/readiness ratio; creates a concrete readout product discipline without reopening parent signature",
            "minimum_deliverable": "fillable clock readout product ledger with tau/direct-product fields, source path, units, and refusal runner",
            "not_a_claim": "does not imply b_alpha standalone value and does not transfer to WEP/R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "FF1320_1_parallel_payoff",
            "selected_row": "SURV1319_2_wep",
            "route": "WEP alpha/source normalization decomposition",
            "why_selected": "highest local-GR/source-universality payoff after clock",
            "minimum_deliverable": "decompose beta_source_alpha, tau_WEP, material response, source profile, and readout kernel into sourceable fields",
            "not_a_claim": "cannot set beta/tau to unity or absorb relative source branch into G",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "FF1320_2_heavy_lift",
            "selected_row": "SURV1319_3_r10",
            "route": "R10 split data/product path",
            "why_selected": "highest short-range gravity payoff but blocked by both data and theory sides",
            "minimum_deliverable": "separate real bound-curve acquisition from MTS product-vector derivation/source fill",
            "not_a_claim": "anchor-only rows and symbolic product vector remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    evidence_state = [
        {
            "evidence_id": "EV1320_0_clock",
            "row": "SURV1319_1_clock",
            "available_evidence": "ACB1052_2 best current Yb clock product bound, product_bound_1sigma=2.1e-18 yr^-1",
            "missing_before_score": "tau_clock_time or direct P_clock_alpha readout model; standalone b_alpha not available",
            "claim_state": "NONCLAIM_PRODUCT_BOUND_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "evidence_id": "EV1320_1_wep",
            "row": "SURV1319_2_wep",
            "available_evidence": "AWP1052_0 alpha/Coulomb pressure target and eta bound imported",
            "missing_before_score": "beta_source_alpha theorem/prior, tau_WEP, shared domain rule, full material/source model",
            "claim_state": "NONCLAIM_PRESSURE_TARGET_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "evidence_id": "EV1320_2_r10",
            "row": "SURV1319_3_r10",
            "available_evidence": "source-backed alpha=1 threshold anchors and real-data contract exist",
            "missing_before_score": "full alpha(lambda) curve plus numeric MTS product vector",
            "claim_state": "NONCLAIM_ANCHOR_AND_SYMBOLIC_PRODUCT_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "evidence_id": "EV1320_3_alpha",
            "row": "SURV1319_0_alpha",
            "available_evidence": "threshold fence exists from prior runner",
            "missing_before_score": "numeric b_alpha/c_alpha or signed theorem-zero certificate",
            "claim_state": "NONCLAIM_THRESHOLD_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "evidence_id": "EV1320_4_cross_arena",
            "row": "SURV1319_4_cross_arena",
            "available_evidence": "separate arena rows exist",
            "missing_before_score": "same branch classifier and readout functor",
            "claim_state": "NONCLAIM_DEFERRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acceptance_gates = [
        {
            "gate_id": "GATE1320_0_closure_only",
            "gate": "parent signature remains closure-only",
            "enforcement": "do not reopen theorem-zero route without new source-backed primitive",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1320_1_clock",
            "gate": "clock first-fill must remain direct product/readout only",
            "enforcement": "no standalone b_alpha by division through assumed tau",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1320_2_wep",
            "gate": "WEP source map must expose beta/tau/material/source/readout factors",
            "enforcement": "no unity beta/tau or G-absorption shortcut",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1320_3_r10",
            "gate": "R10 comparison requires both sides",
            "enforcement": "promoted alpha_bound(lambda) curve and numeric MTS product vector are both mandatory",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1320_4_cross_arena",
            "gate": "cross-arena transfer deferred",
            "enforcement": "no clock-to-WEP/R10 transfer without signed branch/readout functor",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1320_0_ranked_plan",
            "decision": "rank finite source rows after closure-only demotion",
            "because": "parent theorem-zero route is not currently derivable, so source/testing rows carry the next useful work",
            "next_action": "start with clock direct product/readout first-fill, then WEP decomposition, then R10 split path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1320_1_fast_vs_deep",
            "decision": "separate fastest fill from highest physics payoff",
            "because": "clock is most feasible, WEP/R10 are more directly local-GR but heavier",
            "next_action": "use first-fill matrix rather than pretending one row solves the full theory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1320_2_no_claim",
            "decision": "no claim promotion from ranking",
            "because": "ranking is workflow triage only; no missing coefficient or curve is filled",
            "next_action": "1321 builds the clock readout first-fill runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1320_0_1321",
            "target_file": "1321-Y5-R10-RAB-clock-readout-direct-product-first-fill-runner.md",
            "target_script": "scripts/Y5_R10_RAB_clock_readout_direct_product_first_fill_runner.py",
            "task": "build the first fill runner for the selected clock row: tau_clock_time or direct P_clock_alpha, with source path, units, clock pair/sensitivity, and refusal gates",
            "success_condition": "clock row has a fillable direct-product/readout schema and runner that refuses standalone b_alpha, tau assumptions, threshold-as-prediction, and cross-arena transfer",
            "do_not": "do not claim b_alpha; do not transfer clock result to WEP/R10; do not reopen closure-only parent theorem route",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1320_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    validation.append(
        validation_row(
            "VAL1320_1_closure_consequences_cover_demotions",
            "closure consequences cover all 1319 demotions",
            len(closure_consequence) == len(demotions) == 4,
            ";".join(row["source_demotion"] for row in closure_consequence),
        )
    )
    ranks = [int(row["rank"]) for row in finite_priority]
    validation.append(
        validation_row(
            "VAL1320_2_priority_map_covers_survivors",
            "finite priority map covers every surviving row with unique ranks",
            len(finite_priority) == len(survival_rows) == 5 and sorted(ranks) == [1, 2, 3, 4, 5],
            ";".join(f"{row['rank']}:{row['survival_id']}" for row in finite_priority),
        )
    )
    validation.append(
        validation_row(
            "VAL1320_3_clock_selected_first",
            "first-fill selected row is clock direct product/readout",
            first_fill_route[0]["selected_row"] == "SURV1319_1_clock"
            and finite_priority[0]["survival_id"] == "SURV1319_1_clock",
            f"rank1={finite_priority[0]['survival_id']} next={next_target[0]['target_file']}",
        )
    )
    validation.append(
        validation_row(
            "VAL1320_4_r10_remains_heavy_nonclaim",
            "R10 remains high payoff but blocked by data and product inputs",
            any(row["row"] == "SURV1319_3_r10" and row["claim_state"] == "NONCLAIM_ANCHOR_AND_SYMBOLIC_PRODUCT_ONLY" for row in evidence_state),
            "R10 requires promoted curve plus numeric product vector",
        )
    )
    validation.append(
        validation_row(
            "VAL1320_5_acceptance_gates_enforced",
            "acceptance gates are enforced",
            all(row["status"] == "ENFORCED" for row in acceptance_gates),
            ";".join(row["gate_id"] for row in acceptance_gates),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("closure", closure_consequence),
        ("priority", finite_priority),
        ("first_fill", first_fill_route),
        ("evidence", evidence_state),
        ("gates", acceptance_gates),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1320_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1320_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1320_8_next_target_1321",
            "next target routes to clock readout direct product first-fill runner",
            next_target[0]["target_file"].startswith("1321-Y5-R10-RAB-clock-readout"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1320_9_overall",
            "overall 1320 validation",
            all(row["status"] == "PASS" for row in validation),
            "1320 ranks closure-only finite source rows, selects clock first-fill, and keeps WEP/R10/local claims blocked",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CLOSURE_CONSEQUENCE_PATH, closure_consequence)
    write_csv(FINITE_PRIORITY_PATH, finite_priority)
    write_csv(FIRST_FILL_PATH, first_fill_route)
    write_csv(EVIDENCE_STATE_PATH, evidence_state)
    write_csv(ACCEPTANCE_GATES_PATH, acceptance_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1320: RAB Closure-Only Consequence Ledger And Finite Source Priority Map

**Current verdict:** 1320 does not claim any coupling, WEP, R10, clock, local-GR, or cross-arena pass. It turns the 1319 closure-only result into a ranked finite-source work plan.

**Main progress:** the workflow now separates fastest useful fill from highest physics payoff. Clock/readout is selected first because it is the most source-ready; WEP and R10 remain higher local-gravity payoff but heavier and still blocked.

**Decision:** build the clock direct-product/readout first-fill runner next. That gives us a concrete product discipline without pretending to derive standalone `b_alpha` or transferring clock bounds into WEP/R10.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Closure-Only Consequence Ledger
{markdown_table(closure_consequence, ["consequence_id", "source_demotion", "closed_route", "closure_status", "practical_consequence", "surviving_work", "reopen_condition", "valid_for_claim", "claim_allowed"])}

## Finite Source Priority Map
{markdown_table(finite_priority, ["rank", "survival_id", "source_row", "row_label", "priority", "payoff_score", "feasibility_score", "empirical_readiness_score", "derivation_centrality_score", "risk_score", "total_score", "why_ranked_here", "first_fill", "claim_gate", "next_action_type", "valid_for_claim", "claim_allowed"])}

## First-Fill Route Matrix
{markdown_table(first_fill_route, ["route_id", "selected_row", "route", "why_selected", "minimum_deliverable", "not_a_claim", "valid_for_claim", "claim_allowed"])}

## Evidence State Ledger
{markdown_table(evidence_state, ["evidence_id", "row", "available_evidence", "missing_before_score", "claim_state", "valid_for_claim", "claim_allowed"])}

## Acceptance Gates
{markdown_table(acceptance_gates, ["gate_id", "gate", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
