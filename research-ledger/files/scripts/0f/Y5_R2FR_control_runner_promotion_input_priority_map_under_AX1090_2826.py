from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2826-Y5-R2FR-control-runner-promotion-input-priority-map-under-AX1090.md"

SRC_2825_NEXT = RESIDUALS / "P8_Y5_R2FR_2825_NEXT_TARGET.csv"
SRC_2825_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2825_CONTROL_INPUT_SCHEMA.csv"
SRC_2825_PLACEHOLDERS = RESIDUALS / "P8_Y5_R2FR_2825_PLACEHOLDER_INPUT_ROWS_NONCLAIM.csv"
SRC_2825_FORMULAS = RESIDUALS / "P8_Y5_R2FR_2825_LOCAL_LOCK_CONTROL_FORMULAS.csv"
SRC_2825_DRYRUN = RESIDUALS / "P8_Y5_R2FR_2825_DRYRUN_RESULTS_NONCLAIM.csv"
SRC_2825_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2825_PROMOTION_REQUIREMENTS.csv"
SRC_2825_GATES = RESIDUALS / "P8_Y5_R2FR_2825_CLAIM_GATES.csv"
SRC_2825_DECISION = RESIDUALS / "P8_Y5_R2FR_2825_DECISION_LEDGER.csv"
SRC_2824_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2824_COVARIANCE_HESSIAN_SOURCE_EXTRACTION_STATUS.csv"
SRC_2823_UNITS = RESIDUALS / "P8_Y5_R2FR_2823_Q_NORMALIZATION_AND_DUAL_UNITS_GATE.csv"
SRC_2823_IMPACT = RESIDUALS / "P8_Y5_R2FR_2823_COMPONENT_ROW_REENTRY_IMPACT.csv"
SRC_2822_JQ_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2822_COMPONENT_BOUND_FALLBACK_VECTOR.csv"
SRC_2818_INTERFACE = RESIDUALS / "P8_Y5_R2FR_2818_FIRST_NLOCK_INPUT_INTERFACE.csv"
SRC_2818_AMPLITUDE = RESIDUALS / "P8_Y5_R2FR_2818_LOCAL_LOCK_AMPLITUDE_LAW.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2826_SOURCE_REGISTER.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2826_BLOCKER_DEPENDENCY_MAP.csv",
    "ranking": RESIDUALS / "P8_Y5_R2FR_2826_PRIORITY_RANKING.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2826_ROUTE_SELECTION_LEDGER.csv",
    "micro_contract": RESIDUALS / "P8_Y5_R2FR_2826_FIRST_FILL_MICRO_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2826_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2826_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2826_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2826_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2826_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "priority_copy": SOURCE_WEIGHT / "Eq_control_runner_promotion_priority_map_2826_NONCLAIM.csv",
    "micro_contract_copy": LOCAL_BOUNDS / "Dqvm_q_normalization_first_fill_contract_2826_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2826_VERTICAL_GENERATOR_DQVM_Q_NORMALIZATION_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_CONTROL_RUNNER_PROMOTION_INPUT_PRIORITY_2826"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2826_0_2825_next", SRC_2825_NEXT, "NEXT2825_0_2826", "2825 handoff selecting promotion-input priority map"),
        ("SRC2826_1_2825_schema", SRC_2825_SCHEMA, "SCH2825_16_Cqm;SCH2825_17_Dqvm", "control schema showing response/coupling blockers"),
        ("SRC2826_2_2825_placeholders", SRC_2825_PLACEHOLDERS, "PH2825_16_Cqm;PH2825_17_Dqvm", "placeholder inputs remain nonclaim"),
        ("SRC2826_3_2825_formulas", SRC_2825_FORMULAS, "FORM2825_5_Scg;FORM2825_9_Delta", "control formulas linking coupling to local-lock amplitude"),
        ("SRC2826_4_2825_dryrun", SRC_2825_DRYRUN, "DRY2825_1_numeric_eval;DRY2825_2_claim_status", "dry-run refusal and claim block"),
        ("SRC2826_5_2825_promotion", SRC_2825_PROMOTION, "PROM2825_7_Dqvm;PROM2825_10_norm_coherence", "promotion requirements for Dq[v_m] and norm coherence"),
        ("SRC2826_6_2825_gates", SRC_2825_GATES, "CG2825_6_GR_Newton;CG2825_7_PPN_R10", "local and arena claims blocked"),
        ("SRC2826_7_2825_decision", SRC_2825_DECISION, "DEC2825_2_best_gain;DEC2825_3_next", "priority-map rationale"),
        ("SRC2826_8_2824_extraction", SRC_2824_EXTRACTION, "EXT2824_2_HAB;EXT2824_6_selector", "carrier and selector blockers"),
        ("SRC2826_9_2823_units", SRC_2823_UNITS, "QNG2823_2_Eq_units;QNG2823_6_Newton_source", "q normalization and Newton-source debt"),
        ("SRC2826_10_2823_impact", SRC_2823_IMPACT, "RI2823_3_Cqm;RI2823_4_Nlock", "C_qm and local-lock reentry blockers"),
        ("SRC2826_11_2822_jq", SRC_2822_JQ_FALLBACK, "FB2822_0_total", "J_q component-source vector blocker"),
        ("SRC2826_12_2818_interface", SRC_2818_INTERFACE, "FPI2818_0_Nsrc;FPI2818_2_Npair", "worldtube/local-lock input interface"),
        ("SRC2826_13_2818_amplitude", SRC_2818_AMPLITUDE, "ALA2818_1_Nlock;ALA2818_4_chain_insert", "amplitude law and local transition chain"),
    ]
    return [source_row(*spec) for spec in specs]


def blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("BLK2826_0_norm", "q_units_flag + no mixed norm", "normalization", "PROM2825_3_qunits;PROM2825_10_norm_coherence", "every E_q/J_q/Dq[v_m]/arena row", "one q normalization across carrier, source vector, response, and arenas", "MISSING_Q_UNITS_NORMALIZATION", SRC_2825_PROMOTION, "PROM2825_10_norm_coherence"),
        ("BLK2826_1_Dqvm", "Dq[v_m] + C_qm", "response_coupling", "PROM2825_7_Dqvm", "local-lock reentry, S_cg, Delta_m, K_alg residual", "actual vertical generator and bounded q-to-m response", "MISSING_DQ_VERTICAL_GENERATOR", SRC_2825_SCHEMA, "SCH2825_17_Dqvm"),
        ("BLK2826_2_selector", "q=0 selector", "normalization", "PROM2825_2_selector", "local GR/Newton branch", "parent-signed local branch selector or theorem-zero closure", "MISSING_PARENT_SELECTOR", SRC_2824_EXTRACTION, "EXT2824_6_selector"),
        ("BLK2826_3_newton", "Newton/source normalization", "normalization", "PROM2825_5_newton", "GR-to-Newton limit and measured GM", "source-measure equality and universal G bridge", "MISSING_NEWTON_SOURCE_NORMALIZATION", SRC_2823_UNITS, "QNG2823_6_Newton_source"),
        ("BLK2826_4_HAB", "H_AB effective action/lift", "carrier", "PROM2825_0_HAB", "E_q mass/stiffness, J_q dual norm, range relation", "source-backed parent Hessian in same q branch", "MISSING_SOURCE_BACKED_H_AB", SRC_2824_EXTRACTION, "EXT2824_2_HAB"),
        ("BLK2826_5_xiq", "xi_q and lambda_q", "carrier", "PROM2825_1_xiq", "range/suppression scale and local-bound translation", "numeric or theorem-fixed smoothing/correlation scale", "MISSING_SOURCE_BACKED_XI_Q", SRC_2824_EXTRACTION, "EXT2824_4_xiq"),
        ("BLK2826_6_Jq", "J_q components", "source_vector", "PROM2825_6_Jq", "source norm T_source_norm and arena residuals", "every component source-backed or theorem-zero in E_q dual norm", "MISSING_TOTAL_JQ_BOUND", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("BLK2826_7_boundary", "boundary/domain class", "normalization", "PROM2825_4_boundary", "operator self-adjointness, integration by parts, no hidden boundary charge", "signed boundary/corner/cohomology/kernel certificate", "MISSING_BOUNDARY_DOMAIN_CERTIFICATE", SRC_2824_EXTRACTION, "EXT2824_7_boundary"),
        ("BLK2826_8_worldtube", "worldtube/profile constants", "local_lock", "PROM2825_8_worldtube", "N_src, N_pair, N_lock, Delta_m numerical closure", "U_B,max, C_inner, Q_m^H, domain/zero/rest terms sourced", "MISSING_WORLD_TUBE_CONSTANTS", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("BLK2826_9_arena", "arena projection kernels", "empirical", "PROM2825_9_arena", "R10/PPN/clock/orbital score rows", "projection maps in same q/E_q normalization", "MISSING_ARENA_PROJECTION_KERNELS", SRC_2825_GATES, "CG2825_7_PPN_R10"),
    ]
    rows: list[dict[str, Any]] = []
    for blocker_id, blocker, group, promotion_ids, unlocks, needed, status, source_path, anchor in specs:
        rows.append(
            nonclaim(
                {
                    "branch_id": BRANCH_ID,
                    "blocker_id": blocker_id,
                    "blocker": blocker,
                    "input_group": group,
                    "promotion_ids": promotion_ids,
                    "unlocks": unlocks,
                    "needed_evidence": needed,
                    "current_status": status,
                    "source_path": str(source_path),
                    "source_anchor": anchor,
                    "anchor_found": anchor in read_text(source_path),
                    "satisfied": False,
                    "control_only": True,
                }
            )
        )
    return rows


def ranking_rows() -> list[dict[str, Any]]:
    specs = [
        ("PRI2826_1", 1, "Dq[v_m] plus q-normalization", "response_coupling", "DERIVATION_FIRST", 5, 5, 4, 5, 3, "actual coupling is the choke-point: without it the local-lock chain cannot talk to matter, and with it we can decide zero/finite coupling without data-fitting", "derive vertical generator action on q and lock q units/norm coherence", "SELECTED_FIRST_FILL"),
        ("PRI2826_2", 2, "q=0 selector plus Newton/source normalization", "normalization", "DERIVATION_FIRST", 5, 5, 5, 4, 5, "this is the local-GR/Newton bridge, but it is too exposed to attempt before the coupling and q-normalization are pinned", "attempt after Dq[v_m] contract clarifies the local branch", "NEXT_FOUNDATIONAL"),
        ("PRI2826_3", 3, "H_AB effective Hessian plus xi_q range", "carrier", "PARENT_ACTION_SOURCE", 4, 4, 5, 3, 5, "this promotes E_q itself, but it demands a parent action/lift/density convention and is the heaviest derivation target", "keep as carrier-source branch after coupling route", "HIGH_VALUE_HEAVY"),
        ("PRI2826_4", 4, "J_q component theorem-zero or source-backed vector", "source_vector", "DERIVATION_OR_SOURCE", 4, 3, 3, 3, 3, "important for residual size, but component values depend on the E_q norm and Dq coupling being coherent first", "defer until q/E_q/Dq normalization is fixed", "DEPENDENT"),
        ("PRI2826_5", 5, "boundary/domain certificate", "normalization", "GEOMETRY_CERTIFICATE", 3, 3, 4, 3, 4, "needed for rigorous integration by parts and no hidden boundary charge, but not the first unknown in the coupling chain", "carry as parallel audit after first-fill route is selected", "PARALLEL_AUDIT"),
        ("PRI2826_6", 6, "worldtube/profile constants", "local_lock", "SOURCE_BOUND", 3, 2, 2, 2, 2, "only becomes numerically useful after Dq/C_qm and J_q source norm exist", "defer until response/source vector exists", "LATER_NUMERIC_CLOSURE"),
        ("PRI2826_7", 7, "arena projection kernels", "empirical", "EMPIRICAL_LAST", 2, 1, 2, 2, 2, "R10/PPN/clock/orbital tests are premature until the local theory branch is sourced", "do not test claims yet; maintain blocked score rows", "DEFER_EMPIRICAL"),
    ]
    rows: list[dict[str, Any]] = []
    for priority_id, rank, target, group, route_type, local_unlock, dependency_unlock, scrutiny_pressure, derivability, near_term_feasibility, rationale, next_action, status in specs:
        score = 3 * local_unlock + 3 * dependency_unlock + 2 * derivability + near_term_feasibility - scrutiny_pressure
        rows.append(
            nonclaim(
                {
                    "priority_id": priority_id,
                    "rank": rank,
                    "target": target,
                    "input_group": group,
                    "route_type": route_type,
                    "local_GR_Newton_unlock": local_unlock,
                    "dependency_unlock": dependency_unlock,
                    "scrutiny_pressure": scrutiny_pressure,
                    "derivability_score": derivability,
                    "near_term_feasibility": near_term_feasibility,
                    "priority_score": score,
                    "rationale": rationale,
                    "next_action": next_action,
                    "status": status,
                    "selected": rank == 1,
                    "control_only": True,
                }
            )
        )
    return rows


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2826_0_selected", "geometry-first vertical generator route", "SELECTED", "derive Dq[v_m] and q-normalization before any numeric source/vector fit", "least fakeable route: either the quotient geometry gives a coupling/zero theorem or the local-lock path is demoted cleanly", "2827 Dq[v_m]/q-normalization derivation contract"),
        ("ROUTE2826_1_defer_HAB", "parent Hessian/range route", "DEFER", "attempt H_AB and xi_q extraction from parent action first", "too many upstream conventions remain unsigned; high risk of hand-inserted stiffness", "return after Dq/q normalization pins the response channel"),
        ("ROUTE2826_2_defer_empirical", "empirical arena route", "FORBIDDEN_FOR_NOW", "try R10/PPN/clock/orbital tests using placeholders", "would turn control sensitivity into fake evidence", "wait for sourced local branch"),
        ("ROUTE2826_3_parallel_boundary", "boundary/domain certificate route", "PARALLEL_LATER", "tighten boundary class first", "important but does not identify the missing matter coupling by itself", "use after selected route defines the local operator channel"),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "route": route,
                "status": status,
                "proposal": proposal,
                "reason": reason,
                "next_action": next_action,
                "selected": status == "SELECTED",
                "control_only": True,
            }
        )
        for route_id, route, status, proposal, reason, next_action in specs
    ]


def micro_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("MC2826_0_target", "target", "derive or reject Dq[v_m] plus q-normalization", "work out the actual vertical generator action on q in the quotient/observer-cell variables", "must end in EXACT_ZERO_THEOREM, SIGNED_NONZERO_COUPLING, or LOCAL_LOCK_DEMOTION", "2827"),
        ("MC2826_1_inputs", "required_inputs", "q definition, quotient map, vertical generator candidate, local branch variables", "source each object from existing parent/q-local files before algebra", "no new symbols without source row", "2827"),
        ("MC2826_2_derivation", "derivation_steps", "compute Dq[v_m], units of q, induced E_q dual normalization, and C_qm bound status", "keep symbolic if no parent coefficient is signed", "no numeric placeholders", "2827"),
        ("MC2826_3_zero_case", "allowed_outcome", "Dq[v_m]=0 theorem", "if exact zero follows from quotient invariance, local-lock source coupling closes to zero and route demotes/redirects", "do not call it GR pass", "2827"),
        ("MC2826_4_nonzero_case", "allowed_outcome", "Dq[v_m] nonzero sourced formula", "if nonzero, record the exact coupling functional and what remains to source for C_qm", "still no PPN/R10 claim", "2827"),
        ("MC2826_5_fail_case", "allowed_outcome", "unresolved representative-dependent coupling", "if representative/Weyl/disformal choices enter unsourced, demote local-lock path to closure-only again", "no hidden closure axiom", "2827"),
        ("MC2826_6_acceptance", "acceptance", "all cited paths exist, no claim flags, formalization-workbench untouched", "validation must prove nonclaim discipline and selected next handoff", "private checkpoint only", "2827"),
    ]
    return [
        nonclaim(
            {
                "contract_id": contract_id,
                "contract_group": group,
                "item": item,
                "instruction": instruction,
                "acceptance_or_forbidden": acceptance,
                "target_checkpoint": target,
                "selected_for_next": True,
                "control_only": True,
            }
        )
        for contract_id, group, item, instruction, acceptance, target in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    blockers_ok = all(row["anchor_found"] and not row["satisfied"] for row in rows["blockers"])
    ranking_ok = any(row["selected"] and row["rank"] == 1 and "Dq[v_m]" in row["target"] for row in rows["ranking"])
    routes_ok = sum(1 for row in rows["routes"] if row["selected"]) == 1
    contract_ok = all(row["selected_for_next"] and row["control_only"] for row in rows["micro_contract"])
    specs = [
        ("CG2826_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2826_1_blockers", "blocker dependency map is complete", blockers_ok, "every blocker cites an anchor and remains unsatisfied"),
        ("CG2826_2_ranking", "priority ranking selects Dq[v_m]/q-normalization first", ranking_ok, "vertical coupling route has maximum dependency unlock"),
        ("CG2826_3_route", "exactly one first-fill route selected", routes_ok, "geometry-first vertical generator route selected"),
        ("CG2826_4_contract", "2827 micro-contract emitted", contract_ok, "next step is derivation/zero/demotion, not data fitting"),
        ("CG2826_5_no_numeric", "no numeric coefficients inserted", True, "all rows are symbolic/nonclaim"),
        ("CG2826_6_GR_Newton", "local GR/Newton claim allowed", False, "Dq[v_m], q=0 selector, and Newton-source normalization remain missing"),
        ("CG2826_7_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "arena projection and source vector remain blocked"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2826_0_map", "The missing inputs are now ranked.", "PRIORITY_MAP_BUILT", "2825 made the placeholders explicit; 2826 orders them by local-GR/Newton unlock and derivability", "do not start empirical testing yet"),
        ("DEC2826_1_first", "First route is Dq[v_m] plus q-normalization.", "SELECT_VERTICAL_GENERATOR_ROUTE", "this is the coupling choke-point and decides whether local lock has a real source channel", "attempt exact derivation before H_AB numerics"),
        ("DEC2826_2_not_HAB_first", "Do not start with H_AB/xi_q.", "DEFER_PARENT_HESSIAN_ROUTE", "that route is heavier and invites hand-inserted stiffness before the response channel is known", "return after q/Dq normalization is pinned"),
        ("DEC2826_3_not_data", "Do not run PPN/R10/clock/orbital claims yet.", "EMPIRICAL_DEFERRED", "current rows are control skeleton only", "keep claim gates false"),
        ("DEC2826_4_next", "Next target is 2827 Dq[v_m]/q-normalization derivation contract.", "NEXT_2827_VERTICAL_GENERATOR", "a clean derivation can either prove zero, produce a sourced nonzero coupling, or demote the local-lock route", "write 2827 derivation/zero/demotion checkpoint"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2826_0_2827",
                "status": "selected_primary",
                "target_doc": "2827-Y5-R2FR-vertical-generator-Dqvm-and-q-normalization-derivation-contract-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_vertical_generator_Dqvm_and_q_normalization_derivation_contract_under_AX1090_2827.py",
                "mission": "derive or reject the actual vertical generator coupling Dq[v_m] and q-normalization needed by the local-lock branch, ending in exact zero theorem, sourced nonzero coupling formula, or explicit demotion",
                "acceptance": "all cited sources exist; no numeric placeholders are inserted; no local GR/Newton/PPN/R10 claim is allowed; formalization-workbench remains untouched",
                "forbidden": "do not treat a representative-dependent coupling as derived; do not use empirical fits; do not promote the control runner",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2826_0_priority_copy", OUTPUTS["ranking"], BRANCH_OUTPUTS["priority_copy"], "source-weight copy of priority ranking"),
        ("BR2826_1_micro_contract_copy", OUTPUTS["micro_contract"], BRANCH_OUTPUTS["micro_contract_copy"], "local-bounds copy of first-fill micro-contract"),
        ("BR2826_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for vertical-generator/q-normalization target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_numeric_keys = {"numeric_value", "coefficient", "alpha", "beta", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2826_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2826_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2826_2_blocker_anchors", all(row["anchor_found"] for row in rows_by_name["blockers"]), "all blocker rows cite found anchors"),
        ("VAL2826_3_all_blockers_unsatisfied", not any(row["satisfied"] for row in rows_by_name["blockers"]), "no blocker is falsely marked satisfied"),
        ("VAL2826_4_priority_selected", any(row["selected"] and row["rank"] == 1 and "Dq[v_m]" in row["target"] for row in rows_by_name["ranking"]), "Dq[v_m]/q-normalization selected first"),
        ("VAL2826_5_one_route_selected", sum(1 for row in rows_by_name["routes"] if row["selected"]) == 1, "exactly one route selected"),
        ("VAL2826_6_contract_selected", all(row["selected_for_next"] for row in rows_by_name["micro_contract"]), "all micro-contract rows point to 2827"),
        ("VAL2826_7_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local GR/Newton/PPN/R10"),
        ("VAL2826_8_no_numeric_insertions", no_numeric_insertions(rows_by_name), "no numeric coefficients or prediction values inserted"),
        ("VAL2826_9_next_target_2827", any(row["next_id"] == "NEXT2826_0_2827" and row["selected"] for row in rows_by_name["next"]), "vertical-generator/q-normalization target selected next"),
        ("VAL2826_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2826_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2826_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2826_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2826_14_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2826_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2826_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2826_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2826_OVERALL",
            "passed": overall,
            "detail": "2826 ranks the 2825 promotion blockers, selects the Dq[v_m]/q-normalization vertical-generator route as first-fill, keeps all claims blocked, and emits a 2827 derivation/zero/demotion contract.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2826 - Y5 R2FR Control Runner Promotion Input Priority Map Under AX1090

Status: `Y5_R2FR_2826_priority_map_selects_vertical_generator_Dqvm_q_normalization_route`

## Private Verdict

2826 answers the "what is the best route?" question: go after the coupling, but do it geometrically.

The first-fill route is **not** to invent `H_AB`, `xi_q`, `J_q`, or arena numbers. The first-fill route is:

`Dq[v_m] + q-normalization`

That is the choke-point. If the actual vertical generator makes `Dq[v_m]=0`, the local-lock source path demotes cleanly. If it gives a sourced nonzero coupling, `C_qm`, `S_cg`, `N_lock`, `Delta_m`, and the local transition residual can finally be tied to the parent geometry. If it stays representative-dependent, the route is closure-only.

This is why 2827 should derive, zero, or demote the vertical-generator coupling before another empirical or stiffness pass.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Blocker Dependency Map

{markdown_table(rows["blockers"], ["blocker_id", "blocker", "input_group", "unlocks", "needed_evidence", "current_status", "satisfied", "valid_for_claim"])}

## Priority Ranking

{markdown_table(rows["ranking"], ["priority_id", "rank", "target", "route_type", "priority_score", "rationale", "next_action", "selected", "valid_for_claim"])}

## Route Selection Ledger

{markdown_table(rows["routes"], ["route_id", "route", "status", "proposal", "reason", "next_action", "selected", "valid_for_claim"])}

## First Fill Micro Contract

{markdown_table(rows["micro_contract"], ["contract_id", "contract_group", "item", "instruction", "acceptance_or_forbidden", "target_checkpoint", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["blockers"] = blocker_rows()
    rows["ranking"] = ranking_rows()
    rows["routes"] = route_rows()
    rows["micro_contract"] = micro_contract_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "blockers", "ranking", "routes", "micro_contract", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2826_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2826_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
