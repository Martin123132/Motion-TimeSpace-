from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1707"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1707-Y5-R2FR-local-GR-remaining-gates-rollup-after-WEP-demotion.md"

SOURCE_FILES = {
    "1706_doc": ROOT / "1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
    "1706_validation": OUT / "P8_Y5_BRR545_1706_VALIDATION.csv",
    "1706_next": OUT / "P8_Y5_PARENT_QLOC_1706_NEXT_TARGET.csv",
    "1706_zero_result": OUT / "P8_Y5_PARENT_QLOC_1706_ZERO_THEOREM_RESULT.csv",
    "1706_split_demotion": OUT / "P8_Y5_PARENT_QLOC_1706_SPLIT_DELTA_W_ROUTE_DEMOTION.csv",
    "1706_direct_contract": OUT / "P8_Y5_PARENT_QLOC_1706_DIRECT_PRODUCT_ONLY_CONTRACT.csv",
    "1705_source_blocker": OUT / "P8_Y5_PARENT_QLOC_1705_SOURCE_ACQUISITION_BLOCKER.csv",
    "1704_drop_contract": OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_CONTRACT.csv",
    "1702_product_runner": OUT / "P8_Y5_PARENT_QLOC_1702_FIRST_ARENA_PRODUCT_RUNNER.csv",
    "1702_r10_ppn": OUT / "P8_Y5_PARENT_QLOC_1702_R10_PPN_PROJECTION_ROWS.csv",
    "956_doc": ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
    "957_doc": ROOT / "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
    "958_doc": ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
    "958_validation": OUT / "P8_Y5_BRR545_958_VALIDATION.csv",
}

NEEDLES = {
    "1706_doc": ["DEMOTED_TO_DIAGNOSTIC_ONLY", "NEXT1706_0_primary"],
    "1706_validation": ["VAL1706_OVERALL", "PASS"],
    "1706_next": ["1707-Y5-R2FR-local-GR-remaining-gates-rollup-after-WEP-demotion.md", "selected"],
    "1706_zero_result": ["ZTR1706_3_final_verdict", "DEMOTE_SPLIT_DELTA_W_ROUTE"],
    "1706_split_demotion": ["DEM1706_0_split_formula", "DEMOTED_TO_DIAGNOSTIC_ONLY"],
    "1706_direct_contract": ["DPC1706_0_observable", "LIVE_NONCLAIM_BRANCH_OBJECT"],
    "1705_source_blocker": ["BLK1705_3_manual_request", "continue theory route privately"],
    "1704_drop_contract": ["ART1704_0_readout", "P_WEP_tau_parser_manifest.json"],
    "1702_product_runner": ["PR1702_0_WEP_source_weight", "PR1702_2_PPN_gamma_beta"],
    "1702_r10_ppn": ["RP1702_0_R10_lambda_mass", "RP1702_3_PPN_response"],
    "956_doc": ["LHG956_0_EH_core_selection", "LHG956_5_PPN_completion"],
    "957_doc": ["select_EH_operator_first_GM_second", "PLG957_2_EH_operator"],
    "958_doc": ["EH-core operator selection theorem", "not_parent_derived_current_corpus"],
    "958_validation": ["V958_8_next_target_selected", "pass"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1707_SOURCE_REGISTER.csv"
LOCAL_GR_GATE_ROLLUP = OUT / "P8_Y5_PARENT_QLOC_1707_LOCAL_GR_GATE_ROLLUP.csv"
POST_WEP_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1707_POST_WEP_DEMOTION_UPDATE.csv"
PRIORITY_SCORECARD = OUT / "P8_Y5_PARENT_QLOC_1707_PRIORITY_SCORECARD.csv"
NEXT_DERIVATION_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1707_NEXT_DERIVATION_CONTRACT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1707_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1707_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1707_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1707_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    LOCAL_GR_GATE_ROLLUP,
    POST_WEP_UPDATE,
    PRIORITY_SCORECARD,
    NEXT_DERIVATION_CONTRACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    LOCAL_GR_GATE_ROLLUP,
    POST_WEP_UPDATE,
    PRIORITY_SCORECARD,
    NEXT_DERIVATION_CONTRACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    LOCAL_GR_GATE_ROLLUP: [
        QUARANTINE / "LOCAL_GR_GATE_ROLLUP.csv",
        BRANCH_RESIDUALS / "R2FR_local_GR_gate_rollup_1707.csv",
        QUEUE / "JR1707_LOCAL_GR_GATE_ROLLUP.csv",
    ],
    POST_WEP_UPDATE: [
        QUARANTINE / "POST_WEP_DEMOTION_UPDATE.csv",
        BRANCH_RESIDUALS / "R2FR_post_WEP_demotion_update_1707.csv",
        QUEUE / "JR1707_POST_WEP_DEMOTION_UPDATE.csv",
    ],
    PRIORITY_SCORECARD: [
        QUARANTINE / "PRIORITY_SCORECARD.csv",
        BRANCH_RESIDUALS / "R2FR_priority_scorecard_1707.csv",
        QUEUE / "JR1707_PRIORITY_SCORECARD.csv",
    ],
    NEXT_DERIVATION_CONTRACT: [
        QUARANTINE / "NEXT_DERIVATION_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_next_derivation_contract_1707.csv",
        QUEUE / "JR1707_NEXT_DERIVATION_CONTRACT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1707.csv",
        QUEUE / "JR1707_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1707.csv",
        QUEUE / "JR1707_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1707_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1707": "local-GR remaining gate rollup after WEP split-route demotion",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def local_gr_gate_rows() -> list[dict[str, Any]]:
    gates = [
        (
            "LGG1707_0_observed_frame",
            "frame/readout",
            "one observed coframe/metric through matter, source, clocks, photons, orbital and PPN readout",
            "CONDITIONAL_NOT_FULL_PPN_PARENT_CLOSURE",
            "same-frame/readout theorem through O(U^2)",
            "input_to_all",
            7,
        ),
        (
            "LGG1707_1_source_side",
            "right-hand/source",
            "one common kappa times total Hilbert matter current with no hidden species/source tail",
            "CONDITIONAL_SPINE_SHARP_BUT_WEP_SPLIT_DEMOTED",
            "direct product or parent source theorem; no split Delta_w default",
            "blocks_Newton_WEP_source_normalization",
            8,
        ),
        (
            "LGG1707_2_WEP_direct_product",
            "WEP empirical/source",
            "direct P_WEP_source_weight branch only",
            "LIVE_NONCLAIM_EXTERNAL_OR_PARENT_INPUTS_BLOCKED",
            "1704 drop contract or parent direct product theorem",
            "empirical_pillar_not_local_GR_proof",
            5,
        ),
        (
            "LGG1707_3_EH_operator",
            "left-hand/operator",
            "local exterior operator reduces to EH plus harmless Lambda/background",
            "NOT_PARENT_DERIVED_HIGHEST_UPSTREAM",
            "metric-only second-order no-extra-field parent clause or executable R11 vector",
            "blocks_EH_charge_GM_PPN",
            12,
        ),
        (
            "LGG1707_4_extra_sector_silence",
            "hidden/extra sectors",
            "motion/time/domain/memory/projector/boundary/connection sectors carry no independent local charge/stress",
            "ACTIVE_PRIMARY_OBSTRUCTION",
            "sector no-hair/topological/gauge silence or sourced residual rows",
            "blocks_EH_nohair_PPN_source_mass",
            11,
        ),
        (
            "LGG1707_5_GM_worldtube",
            "Newton/source-measure",
            "exterior charge equals dressed source charge and measured orbital GM",
            "QUEUED_DOWNSTREAM_OF_EH_CHARGE_TRANSFER",
            "Noether/Hamiltonian charge inheritance, fixed Pi_M, flux closure, Gauss/orbital calibration",
            "blocks_Newton_measured_GM",
            9,
        ),
        (
            "LGG1707_6_PPN_vector",
            "solar-system/local tests",
            "gamma, beta, alpha_i, xi, Gdot/range/source terms theorem-zero or bounded without cancellation",
            "PROMOTION_GATES_FAIL_FOR_CLAIM",
            "response matrices, tail split, no-cancellation envelope",
            "blocks_local_GR_claim",
            10,
        ),
        (
            "LGG1707_7_R10_alpha_lambda",
            "short-range empirical",
            "lambda/Z/K/Qbar/tau and claim-valid alpha(lambda) curve",
            "MISSING_R10_PROJECTION_INPUTS",
            "projection fill runner and source-backed bound curve",
            "empirical_fifth_force_pillar",
            6,
        ),
        (
            "LGG1707_8_clock_orbital",
            "clock/orbital empirical",
            "clock alpha product and orbital GM/source product",
            "MISSING_CLOCK_ORBITAL_PRODUCT_INPUTS",
            "clock/direct product and orbital source-measure residual rows",
            "empirical_consistency_pillars",
            6,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "layer": layer,
            "requirement": requirement,
            "current_status": status,
            "next_needed": next_needed,
            "blocks": blocks,
            "priority_score": priority,
            "gate_pass": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, layer, requirement, status, next_needed, blocks, priority in gates
    ]


def post_wep_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "update_id": "PWU1707_0_split_removed",
            "object": "Delta_w_TiPt*tau_WEP split",
            "old_role": "possible WEP source-weight product route",
            "new_role": "diagnostic-only identity if both factors later become source-backed",
            "effect_on_local_GR": "removes a half-owned source-side zero claim from local-GR roadmap",
            "current_status": "DEMOTED_AFTER_1706",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "update_id": "PWU1707_1_direct_retained",
            "object": "P_WEP_source_weight",
            "old_role": "direct product fallback",
            "new_role": "only live WEP product branch object",
            "effect_on_local_GR": "keeps WEP testable without smuggling Delta_w=0 or tau_WEP=1",
            "current_status": "LIVE_NONCLAIM_BLOCKED_BY_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "update_id": "PWU1707_2_priority_shift",
            "object": "local-GR next derivation",
            "old_role": "WEP coupling/source-weight branch under active audit",
            "new_role": "EH/operator and R11/no-extra-field branch resumes upstream priority",
            "effect_on_local_GR": "returns to the left-hand GR limit instead of waiting on external MICROSCOPE files",
            "current_status": "EH_OPERATOR_SELECTED_NEXT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def priority_scorecard_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PSC1707_0_EH_R11",
            "EH/operator selection or executable R11/nonEH vector",
            "selected",
            12,
            "upstream of GM/worldtube, PPN and local-GR operator claim; 957/958 already identify it as highest leverage",
            "hard but broad payoff",
        ),
        (
            "PSC1707_1_PPN",
            "PPN residual vector response/tail split",
            "held_second_after_EH_shape",
            10,
            "required for serious local-GR claim and solar-system credibility",
            "needs operator/source split first",
        ),
        (
            "PSC1707_2_GM",
            "measured-GM/worldtube calibration",
            "held_downstream",
            9,
            "essential for Newton but depends on EH charge/symplectic transfer",
            "narrower but dependency-heavy",
        ),
        (
            "PSC1707_3_R10",
            "R10 alpha(lambda) projection fill",
            "held_empirical_fallback",
            6,
            "good empirical fifth-force pillar after WEP data branch paused",
            "does not by itself derive GR/Newton",
        ),
        (
            "PSC1707_4_WEP_direct",
            "direct WEP product branch",
            "held_external_dependency",
            5,
            "clean parser exists but no public files; manual request path ready",
            "blocked by source files or parent direct-product theorem",
        ),
        (
            "PSC1707_5_clock_orbital",
            "clock/orbital products",
            "held_later_empirical",
            6,
            "important cross-arena checks after operator/source gates stabilize",
            "missing product inputs",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "scorecard_id": scorecard_id,
            "candidate_branch": branch,
            "selection_status": status,
            "priority_score": priority,
            "reason": reason,
            "risk": risk,
            "selected_next": status == "selected",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for scorecard_id, branch, status, priority, reason, risk in rows
    ]


def next_derivation_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NDC1707_0_target",
            "EH-core operator refresh after WEP demotion",
            "test whether local exterior MTS reduces to local 4D metric-only second-order EH+Lambda under parent-signed clauses",
            "do not use WEP split-route silence as evidence for EH/operator selection",
            "if any premise unsigned, produce executable nonEH/R11 residual row requirements",
        ),
        (
            "NDC1707_1_no_extra_field",
            "no extra exterior fields",
            "scalar/vector/domain/projector/memory/torsion/nonmetricity/boundary families absent, gauge, topological/no-haired, or retained",
            "do not bury fields in readout or measured-G calibration",
            "family-by-family zero-or-bound ledger",
        ),
        (
            "NDC1707_2_second_order",
            "second-order local metric equations",
            "higher derivative/R2/fR/Ricci/Weyl/nonlocal operators excluded or residualized",
            "do not invoke Lovelock route without parent premises",
            "R2/fR and torsion/nonmetricity first rows if theorem fails",
        ),
        (
            "NDC1707_3_symplectic_charge",
            "extra-sector symplectic flux silence",
            "omega_extra=0/gauge/topological/no-flux or bounded before GM transfer",
            "do not claim measured-GM from EH baseline alone",
            "charge-transfer blocker ledger",
        ),
        (
            "NDC1707_4_claim_guard",
            "no-promotion policy",
            "EH route can be conditional or residualized only",
            "no local-GR/Newton/PPN claim from 1708",
            "claim gates false",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "deliverable": deliverable,
            "acceptance_gate": gate,
            "forbidden_shortcut": shortcut,
            "failure_output": failure,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, deliverable, gate, shortcut, failure in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1707_0_local_gr", "claim local GR/Newton after WEP demotion", "BLOCKED_NO_CLAIM", "WEP split route is demoted and left-hand EH/GM/PPN gates remain open"),
        ("RUN1707_1_eh", "claim EH operator selected", "REJECT_EH_CLAIM", "958 says EH route is conditional and not parent-derived"),
        ("RUN1707_2_wep", "score WEP direct product", "REJECT_WEP_SCORE", "1704/1705 direct-product inputs absent"),
        ("RUN1707_3_ppn", "score PPN vector", "REJECT_PPN_SCORE", "response matrix/tail split missing"),
        ("RUN1707_4_r10", "score R10 alpha(lambda)", "REJECT_R10_SCORE", "lambda/Z/K/Qbar/tau/bound-curve inputs missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1707_0_primary",
            "next_target": "1708-Y5-R2FR-EH-core-operator-refresh-after-WEP-demotion-or-R11-priority-fill.md",
            "script": "scripts/Y5_R2FR_EH_core_operator_refresh_after_WEP_demotion_or_R11_priority_fill.py",
            "objective": "reopen the EH/operator branch after WEP split demotion: prove local metric-only second-order no-extra-field premises, or produce executable R11/nonEH priority rows",
            "selection_status": "selected",
            "success_condition": "EH theorem remains conditional unless all premises parent-sign; otherwise R11 priority rows are explicit and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1707_1_r10",
            "next_target": "1708a-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "script": "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "objective": "fill R10 projection inputs as empirical fallback after EH refresh",
            "selection_status": "held_fallback",
            "success_condition": "R10 projection inputs or explicit blockers are source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1707_2_manual_wep",
            "next_target": "1708b-Y5-R2FR-MICROSCOPE-direct-product-import-if-files-exist.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_direct_product_import_if_files_exist.py",
            "objective": "import WEP direct-product files only if externally supplied",
            "selection_status": "held_external_dependency",
            "success_condition": "live files supplied; no invented arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1707_0_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "EH/operator, extra sector, GM/worldtube, PPN and source-side direct product gates remain open"),
        ("CG1707_1_EH", "EH operator selected by parent MTS", "BLOCKED_NO_CLAIM", "958 route is conditional and 1707 only reorders gates"),
        ("CG1707_2_WEP", "WEP source branch passes", "BLOCKED_NO_CLAIM", "split route demoted; direct product retained but unfilled"),
        ("CG1707_3_PPN", "PPN vector reaches GR", "BLOCKED_NO_CLAIM", "PPN response/tail split missing"),
        ("CG1707_4_Newton_GM", "Newtonian measured-GM calibration derived", "BLOCKED_NO_CLAIM", "queued downstream of EH charge transfer"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in gates
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


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
            for field in ("gate_pass", "selected_next", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and truthy(row[field]):
                    if field == "selected_next":
                        continue
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = (
        "1707-Y5",
        "P8_Y5_PARENT_QLOC_1707",
        "P8_Y5_BRR545_1707",
        "Y5_R2FR_local_GR_remaining_gates_rollup_after_WEP_demotion",
    )
    for path in FORMALIZATION.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if any(marker in path.name for marker in markers):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    gates = read_csv(LOCAL_GR_GATE_ROLLUP)
    updates = read_csv(POST_WEP_UPDATE)
    scorecard = read_csv(PRIORITY_SCORECARD)
    contract = read_csv(NEXT_DERIVATION_CONTRACT)
    runner = read_csv(RUNNER_REFUSAL)
    next_rows_ = read_csv(NEXT_TARGET)
    claims = read_csv(CLAIM_GATE)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1707_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1707_1_needles_present", all(truthy(row["needles_present"]) for row in sources), "all required source needles are present"),
        ("VAL1707_2_gate_rollup_complete", {"LGG1707_1_source_side", "LGG1707_2_WEP_direct_product", "LGG1707_3_EH_operator", "LGG1707_5_GM_worldtube", "LGG1707_6_PPN_vector", "LGG1707_7_R10_alpha_lambda"}.issubset({row["gate_id"] for row in gates}), "local-GR rollup covers source, WEP, EH, GM, PPN, and R10 gates"),
        ("VAL1707_3_all_gates_blocked", gates and all(not truthy(row["gate_pass"]) for row in gates), "all local-GR gates remain nonclaim/blocked"),
        ("VAL1707_4_wep_update", any(row["update_id"] == "PWU1707_0_split_removed" and row["current_status"] == "DEMOTED_AFTER_1706" for row in updates), "post-WEP demotion update recorded"),
        ("VAL1707_5_eh_selected", any(row["scorecard_id"] == "PSC1707_0_EH_R11" and row["selection_status"] == "selected" for row in scorecard), "EH/R11 branch selected as next highest payoff"),
        ("VAL1707_6_next_contract_ready", len(contract) >= 5 and any(row["contract_id"] == "NDC1707_2_second_order" for row in contract), "next EH/R11 derivation contract written"),
        ("VAL1707_7_runner_blocks", runner and all(not truthy(row["can_score"]) and not truthy(row["accepted_for_scoring"]) for row in runner), "runner blocks local-GR/EH/WEP/PPN/R10 scores"),
        ("VAL1707_8_next_selected", any(row["route_id"] == "NEXT1707_0_primary" and row["selection_status"] == "selected" for row in next_rows_), "next target selected"),
        ("VAL1707_9_claim_gates_blocked", claims and all(row["status"] == "BLOCKED_NO_CLAIM" and not truthy(row["claim_allowed"]) for row in claims), "all claim gates remain blocked"),
        ("VAL1707_10_csv_parse", csv_parses(GENERATED_CSVS), "all generated 1707 CSVs parse"),
        ("VAL1707_11_no_claim_flags", no_claim_flags(CLAIM_CHECKED_CSVS), "all generated score/prediction/claim flags remain false"),
        ("VAL1707_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine/queue copies exist"),
        ("VAL1707_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1707_14_formalization_untouched", formalization_untouched(), "no 1707 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1707_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1707 local-GR remaining gates rollup after WEP demotion validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1707 - Local GR Remaining Gates Rollup After WEP Demotion",
                "## Verdict\n"
                "- 1707 updates the local-GR/Newton roadmap after the WEP split route was demoted.\n"
                "- WEP remains alive only as a direct product branch; it is not a source-side theorem and not a local-GR proof.\n"
                "- The highest-payoff next derivation is back on the left-hand side: EH/operator selection or executable R11/nonEH residual vector.\n"
                "- Measured-GM/worldtube remains essential for Newton, but it is downstream of EH/symplectic charge transfer and extra-sector silence.\n"
                "- R10, PPN, clocks and orbital products remain empirical pillars/fallbacks, not replacements for deriving GR/Newton.\n"
                "- No local-GR/Newton, WEP, EH, PPN, R10, clock or orbital claim is made.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
                "## Local-GR Gate Rollup",
                markdown_table(gates, ["gate_id", "layer", "current_status", "next_needed", "priority_score"]),
                "## Post-WEP Demotion Update",
                markdown_table(updates, ["update_id", "object", "new_role", "effect_on_local_GR", "current_status"]),
                "## Priority Scorecard",
                markdown_table(scorecard, ["scorecard_id", "candidate_branch", "selection_status", "priority_score", "reason"]),
                "## Next Derivation Contract",
                markdown_table(contract, ["contract_id", "deliverable", "acceptance_gate", "failure_output"]),
                "## Runner Refusal",
                markdown_table(runner, ["runner_id", "case", "status", "reason"]),
                "## Next Target",
                markdown_table(next_rows_, ["route_id", "next_target", "objective", "selection_status"]),
                "## Claim Gates",
                markdown_table(claims, ["claim_id", "claim", "status", "reason"]),
                "## Validation",
                markdown_table(validation, ["check_id", "result", "detail"]),
                "## Working Interpretation\n"
                "This puts the project back on the main bridge: source-side cleanup helped, WEP is now cleanly external/direct-product, and the serious GR/Newton problem is the left-hand operator. If MTS can earn EH/operator selection or a disciplined R11 residual vector, then measured-GM and PPN become meaningful next rounds rather than wishful promotion.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    gates = local_gr_gate_rows()
    updates = post_wep_update_rows()
    scorecard = priority_scorecard_rows()
    contract = next_derivation_contract_rows()
    runner = runner_refusal_rows()
    next_rows_ = next_target_rows()
    claims = claim_gate_rows()
    write_csv(SOURCE_REGISTER, sources)
    write_csv(LOCAL_GR_GATE_ROLLUP, gates)
    write_csv(POST_WEP_UPDATE, updates)
    write_csv(PRIORITY_SCORECARD, scorecard)
    write_csv(NEXT_DERIVATION_CONTRACT, contract)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claims)
    copy_outputs()
    remove_pycache()
    validation = validation_rows()
    write_csv(VALIDATION, validation)
    write_doc(sources, gates, updates, scorecard, contract, runner, next_rows_, claims, validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1707 validation PASS")


if __name__ == "__main__":
    main()
