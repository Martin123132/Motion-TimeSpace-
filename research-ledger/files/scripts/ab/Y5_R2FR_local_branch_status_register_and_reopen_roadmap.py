from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1616"
INPUT_1616 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1616-Y5-R2FR-local-branch-status-register-and-reopen-roadmap.md"

SOURCE_FILES = {
    "1615_doc": ROOT / "1615-Y5-R2FR-generator-positivity-certificate-or-local-branch-demotion.md",
    "1615_validation": OUT / "P8_Y5_BRR545_1615_VALIDATION.csv",
    "1615_next": OUT / "P8_Y5_PARENT_QLOC_1615_NEXT_TARGET.csv",
    "1615_demotion": OUT / "P8_Y5_PARENT_QLOC_1615_LOCAL_BRANCH_DEMOTION_LEDGER.csv",
    "1615_reopen": OUT / "P8_Y5_PARENT_QLOC_1615_REOPEN_CONDITIONS.csv",
    "1615_ceiling": OUT / "P8_Y5_PARENT_QLOC_1615_CLAIM_CEILING_MATRIX.csv",
    "1615_gate": OUT / "P8_Y5_PARENT_QLOC_1615_CLAIM_GATE.csv",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1010_claim_gate": OUT / "P8_Y5_R10_1010_CLAIM_GATE.csv",
    "1009_doc": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "1009_claim_gate": OUT / "P8_Y5_R10_1009_CLAIM_GATE.csv",
    "100_cosmo": ROOT / "100-canonical-R-T1-primary-fullcov-scorecard.md",
}

NEEDLES = {
    "1615_doc": ["CLOSURE_OR_SOURCE_DATA_DEPENDENT_NOT_DERIVED", "NEXT_1616_LOCAL_BRANCH_STATUS_REGISTER_AND_REOPEN_ROADMAP"],
    "1615_validation": ["VAL1615_OVERALL", "PASS"],
    "1615_next": ["1616-Y5-R2FR-local-branch-status-register-and-reopen-roadmap.md", "rank reopen routes"],
    "1615_demotion": ["LBD1615_0_status", "CLOSURE_OR_SOURCE_DATA_DEPENDENT_NOT_DERIVED"],
    "1615_reopen": ["ROC1615_6_q_loc", "MISSING"],
    "1615_ceiling": ["CCM1615_5_public_claim", "BLOCKED"],
    "1615_gate": ["CG1615_4_derived_local_GR", "BLOCKED"],
    "1010_doc": ["DEC1010_0_derivation_route_precise", "q_loc=0"],
    "1010_claim_gate": ["CG1010_5_Htau_MHref_local_GR", "q_loc remains retained residual"],
    "1009_doc": ["CG1009_5_Htau_MHref_local_GR", "total parent current chain remains incomplete"],
    "1009_claim_gate": ["CG1009_5_Htau_MHref_local_GR", "total parent current chain remains incomplete"],
    "100_cosmo": ["empirical_closure_scorecard_only", "not a field-theory promotion"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1616_SOURCE_REGISTER.csv"
STATUS_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1616_LOCAL_BRANCH_STATUS_REGISTER.csv"
REOPEN_ROADMAP = OUT / "P8_Y5_PARENT_QLOC_1616_REOPEN_ROADMAP.csv"
ROUTE_RANKING = OUT / "P8_Y5_PARENT_QLOC_1616_ROUTE_PRIORITY_RANKING.csv"
CLAIM_DRIFT_GUARD = OUT / "P8_Y5_PARENT_QLOC_1616_CLAIM_DRIFT_GUARD.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1616_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1616_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1616_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1616_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1616_VALIDATION.csv"

COPY_TARGETS = {
    STATUS_REGISTER: [
        QUARANTINE / "LOCAL_BRANCH_STATUS_REGISTER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_local_branch_status_register_nonclaim_1616.csv",
    ],
    REOPEN_ROADMAP: [
        QUARANTINE / "REOPEN_ROADMAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_reopen_roadmap_nonclaim_1616.csv",
    ],
    ROUTE_RANKING: [
        QUARANTINE / "ROUTE_PRIORITY_RANKING_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_route_priority_ranking_nonclaim_1616.csv",
    ],
    CLAIM_DRIFT_GUARD: [
        QUARANTINE / "CLAIM_DRIFT_GUARD_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_claim_drift_guard_nonclaim_1616.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1616.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1616_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1616_local_branch_status_register_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def status_register_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LBS1616_0_local_GR_derivation",
            "derived local GR/Newton recovery",
            "BLOCKED_DEMOTED",
            "1615 demoted this route to closure/source-data dependency",
            "q_loc action/residual, source-measure bridge, and c_min/tau gates all reopen",
            "not allowed",
        ),
        (
            "LBS1616_1_q_loc_action",
            "q_loc action/Helmholtz/Euler double-zero",
            "OPEN_HIGHEST_LEVERAGE_DERIVATION",
            "1010 gives exact derivation route and retains q_loc residual",
            "S_GK action, metric response, Helmholtz, Euler/double-zero, boundary/source-current certificates",
            "private derivation target only",
        ),
        (
            "LBS1616_2_source_measure",
            "worldtube/source-measure/GM bridge",
            "OPEN_PARALLEL_ROOT_DERIVATION",
            "1009 keeps total parent current chain and source-measure incomplete",
            "Pi_M/worldtube/current-chain ownership before measured-GM calibration",
            "private derivation target only",
        ),
        (
            "LBS1616_3_cmin_generator",
            "generator positivity / c_min WEP branch",
            "OPEN_BUT_DEMOTED_SECONDARY",
            "1615 generator positivity certificate not signed",
            "parent basis, generators, readout lower bounds, material projection, covariance, domain order",
            "private theorem/data target only",
        ),
        (
            "LBS1616_4_official_CMSM",
            "official CMSM source-data route",
            "OPEN_DATA_DEPENDENCY",
            "ONERA pointer known but no CMSM rows captured",
            "official readout/material/mask/alignment arrays in quarantine",
            "quarantined nonclaim computation only",
        ),
        (
            "LBS1616_5_cosmology_closure",
            "canonical cosmology closure scorecards",
            "SEPARATE_EMPIRICAL_CLOSURE",
            "100 records a competitive empirical closure but not field-theory promotion",
            "continued robustness plus parent-action derivation for fitted closure terms",
            "empirical closure scorecard only",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "route": route,
            "current_status": current_status,
            "evidence": evidence,
            "reopen_condition": reopen,
            "claim_ceiling": ceiling,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for status_id, route, current_status, evidence, reopen, ceiling in rows
    ]


def reopen_roadmap_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RRM1616_0_q_loc",
            "q_loc action route",
            "derive S_GK or bounded q_loc residual",
            "parent action density; K_hat metric response; Helmholtz symmetry; Euler/double-zero; source-current and boundary no-flux",
            "best direct route to derived local GR instead of closure",
        ),
        (
            "RRM1616_1_source_measure",
            "source-measure route",
            "derive worldtube/source-measure/GM bridge",
            "Pi_M parent origin; current-chain theta/Q_tau; source worldtube equality; measured-GM calibration rule",
            "needed even if q_loc zero closes, because Newton normalization must be owned",
        ),
        (
            "RRM1616_2_generator_cmin",
            "c_min generator route",
            "derive generator positivity certificate or compute c_min from official data",
            "basis; generator list; K lower bounds; material projection; covariance; domain order",
            "useful WEP/local empirical pillar but currently secondary after demotion",
        ),
        (
            "RRM1616_3_CMSM",
            "official CMSM acquisition",
            "capture official source-pack/readout/material/alignment rows",
            "filelist; checksums; K_CMSM; material tensor; masks; alignment_result",
            "data route for c_min, not a parent derivation by itself",
        ),
        (
            "RRM1616_4_closure",
            "closure/cosmology route",
            "continue scorecards only under closure label",
            "robustness tests; ablations; no public derivation claim",
            "keeps empirical programme alive without overclaiming local GR",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "roadmap_id": roadmap_id,
            "route": route,
            "task": task,
            "required_inputs": required,
            "why_it_matters": why,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for roadmap_id, route, task, required, why in rows
    ]


def route_ranking_rows() -> list[dict[str, Any]]:
    rows = [
        (1, "q_loc_action_reopen_pack", "highest", "attacks the local residual at parent-action level", "build q_loc action/residual reopen pack"),
        (2, "source_measure_bridge", "high", "owns Newton/GM normalization after local residual route", "derive worldtube/source-measure bridge"),
        (3, "generator_cmin_certificate", "medium", "important WEP/local empirical pillar but now secondary", "continue only after parent basis/source data appears"),
        (4, "official_CMSM_acquisition", "medium", "can compute c_min but depends on external data access", "keep quarantine loader ready"),
        (5, "cosmology_closure_robustness", "parallel", "empirically valuable but not local GR derivation", "continue as closure scorecard only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "priority_rank": rank,
            "route_id": route,
            "priority": priority,
            "reason": reason,
            "recommended_next_action": next_action,
            "selected_next": rank == 1,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rank, route, priority, reason, next_action in rows
    ]


def claim_drift_guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("CDG1616_0_label", "any local-GR statement must state closure/source-data/derivation status", "BLOCK_IF_UNLABELLED"),
        ("CDG1616_1_closure", "closure models may be discussed only as closure benchmarks", "BLOCK_IF_CALLED_DERIVED"),
        ("CDG1616_2_data", "official source data may be imported only as nonclaim quarantine rows", "BLOCK_IF_PROMOTED_FROM_POINTER_OR_TEMPLATE"),
        ("CDG1616_3_q_loc", "derived local GR requires q_loc zero or bounded residual from parent route", "BLOCK_IF_QLOC_RETAINED"),
        ("CDG1616_4_source_measure", "Newton/GM normalization requires parent source-measure bridge", "BLOCK_IF_MEASURED_G_BORROWED"),
        ("CDG1616_5_public", "public claim MTS reduces to GR requires all reopen conditions pass", "BLOCK_UNTIL_ALL_GATES_PASS"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guard_rule": rule,
            "failure_mode": failure,
            "guard_active": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, rule, failure in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1616_0_status_register",
            "input_state": "1615 demotion and reopen conditions imported",
            "runner_result": "STATUS_REGISTER_WRITTEN",
            "effect": "local branch claim drift is now centrally controlled",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1616_1_priority",
            "input_state": "q_loc, source-measure, c_min, CMSM and closure routes ranked",
            "runner_result": "SELECT_QLOC_ACTION_ROUTE_NEXT",
            "effect": "next work returns to parent-action derivation rather than WEP closure scoring",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1616_0_status_register", "status register installed", "GUARD_ONLY", "register controls labels but does not prove local GR"),
        ("CG1616_1_q_loc", "q_loc route reopens local claim", "BLOCKED", "q_loc retained residual remains open"),
        ("CG1616_2_source_measure", "source-measure route reopens local claim", "BLOCKED", "worldtube/GM bridge incomplete"),
        ("CG1616_3_cmin", "c_min/tau route reopens local claim", "BLOCKED", "generator certificate and official arrays absent"),
        ("CG1616_4_derived_local_GR", "derived local GR/Newton claim", "BLOCKED", "1615 demotion remains active"),
        ("CG1616_5_public_claim", "public MTS reduces to GR claim", "BLOCKED", "all reopen routes still nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1616_0_register",
            "decision": "LOCAL_BRANCH_STATUS_REGISTER_INSTALLED",
            "reason": "1615 demotion is now connected to q_loc/source-measure/cmin/CMSM/closure routes",
            "next_action": "use register before any local-GR wording or test promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1616_1_priority",
            "decision": "QLOC_ACTION_ROUTE_SELECTED_NEXT",
            "reason": "q_loc action/residual route is closest to deriving local GR from parent structure",
            "next_action": "build q_loc action reopen pack or residual bound roadmap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1616_2_next",
            "decision": "NEXT_1617_QLOC_ACTION_REOPEN_PACK_OR_RESIDUAL_BOUND_ROADMAP",
            "reason": "the project should attack the local residual root rather than continue WEP closure scaffolding",
            "next_action": "collect S_GK, metric-response, Helmholtz, Euler/double-zero and residual-bound requirements into a new pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1617-Y5-R2FR-q_loc-action-reopen-pack-or-residual-bound-roadmap.md",
            "script": "scripts/Y5_R2FR_q_loc_action_reopen_pack_or_residual_bound_roadmap.py",
            "objective": "return to the parent q_loc route: assemble the action/metric-response/Helmholtz/Euler-double-zero pack or a strict residual-bound roadmap",
            "success_condition": "q_loc reopen pack identifies every required parent certificate and either closes one clause or ranks residual-bound inputs without local-GR promotion",
            "do_not": "do not use plateau axiom, bookkeeping stress, EH-only import, fitted cancellation, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1616() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1616-Y5",
        "P8_Y5_PARENT_QLOC_1616",
        "P8_Y5_BRR545_1616",
        "Y5_R2FR_local_branch_status_register_and_reopen_roadmap",
        "R2FR_local_branch_status_register",
        "R2FR_reopen_roadmap",
        "R2FR_route_priority",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    status = read_csv(STATUS_REGISTER)
    roadmap = read_csv(REOPEN_ROADMAP)
    ranking = read_csv(ROUTE_RANKING)
    guard = read_csv(CLAIM_DRIFT_GUARD)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1616_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1616 local source paths exist"),
        ("VAL1616_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1616 source needles found"),
        ("VAL1616_2_input_dir_ready", INPUT_1616.exists(), "1616 quarantine input directory exists"),
        ("VAL1616_3_status_register", any(row["status_id"] == "LBS1616_0_local_GR_derivation" and row["current_status"] == "BLOCKED_DEMOTED" for row in status), "status register records demoted local GR derivation"),
        ("VAL1616_4_roadmap_complete", len(roadmap) >= 5 and all(row["claim_allowed"].lower() == "false" for row in roadmap), "roadmap covers q_loc/source-measure/cmin/CMSM/closure routes"),
        ("VAL1616_5_q_loc_ranked_first", any(row["priority_rank"] == "1" and row["route_id"] == "q_loc_action_reopen_pack" and row["selected_next"].lower() == "true" for row in ranking), "q_loc action route ranked first"),
        ("VAL1616_6_guard_active", len(guard) >= 6 and all(row["guard_active"].lower() == "true" for row in guard), "claim drift guard is active"),
        ("VAL1616_7_runner_selects_q_loc", any(row["runner_id"] == "RUN1616_1_priority" and row["runner_result"] == "SELECT_QLOC_ACTION_ROUTE_NEXT" for row in runner), "runner selects q_loc action route next"),
        ("VAL1616_8_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1616 claim gates remain nonclaim"),
        ("VAL1616_9_decision_next", any(row["decision"] == "NEXT_1617_QLOC_ACTION_REOPEN_PACK_OR_RESIDUAL_BOUND_ROADMAP" for row in decisions), "decision selects 1617 q_loc route"),
        ("VAL1616_10_csv_parse", csv_parses(generated_csvs), "all generated 1616 CSVs parse"),
        ("VAL1616_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1616 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1616_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1616_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1616_14_formalization_untouched", no_formalization_1616(), "no 1616 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1616_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1616 local branch status register and reopen roadmap validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    status: list[dict[str, Any]],
    roadmap: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    guard: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1616 - R2/fR Local Branch Status Register And Reopen Roadmap",
                "## Verdict\n"
                "- 1616 centralizes the post-demotion local-GR branch status so claim drift is harder.\n"
                "- Derived local GR/Newton remains blocked and demoted; closure/cosmology remains allowed only as labelled empirical closure work.\n"
                "- The selected next derivation target is the parent `q_loc` action route, not another WEP/CMSM scaffold pass.\n"
                "- Source-measure/GM, generator/c_min, and official CMSM acquisition remain live parallel reopen routes, but none promotes a claim.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Local Branch Status Register",
                md_table(status, ["status_id", "route", "current_status", "evidence", "reopen_condition", "claim_ceiling"]),
                "## Reopen Roadmap",
                md_table(roadmap, ["roadmap_id", "route", "task", "required_inputs", "why_it_matters"]),
                "## Route Priority Ranking",
                md_table(ranking, ["priority_rank", "route_id", "priority", "reason", "recommended_next_action", "selected_next"]),
                "## Claim Drift Guard",
                md_table(guard, ["guard_id", "guard_rule", "failure_mode", "guard_active"]),
                "## Runner",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1616.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    status = status_register_rows()
    roadmap = reopen_roadmap_rows()
    ranking = route_ranking_rows()
    guard = claim_drift_guard_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        STATUS_REGISTER,
        REOPEN_ROADMAP,
        ROUTE_RANKING,
        CLAIM_DRIFT_GUARD,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(STATUS_REGISTER, status)
    write_csv(REOPEN_ROADMAP, roadmap)
    write_csv(ROUTE_RANKING, ranking)
    write_csv(CLAIM_DRIFT_GUARD, guard)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, status, roadmap, ranking, guard, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
