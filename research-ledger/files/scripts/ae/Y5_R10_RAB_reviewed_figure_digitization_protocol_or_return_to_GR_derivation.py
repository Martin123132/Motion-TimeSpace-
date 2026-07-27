from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1510-Y5-R10-RAB-reviewed-figure-digitization-protocol-or-return-to-GR-derivation.md"
START_TS = datetime.now(timezone.utc).timestamp()

FIG5B = R10 / "raw" / "1509" / "arxiv_2002_11761_source" / "fig5b1.pdf"
SOURCE_TEX = R10 / "raw" / "1509" / "arxiv_2002_11761_source" / "FB_ISL_pdf.tex"
ANCHOR_CURVE = R10 / "candidates" / "R10_alpha_lambda_bound_curve_1509_SOURCE_ANCHORS_NONCLAIM.csv"
TAU_SCHEMA = R10 / "candidates" / "R10_delta_w_kernel_lambda_1509_SCHEMA_NONCLAIM.csv"
LIVE_BOUND_CURVE = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
LIVE_TAU_KERNEL = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"

SOURCE_FILES = {
    "1509_validation": OUT / "P8_Y5_BRR545_1509_VALIDATION.csv",
    "1509_claim_gate": OUT / "P8_Y5_R10_1509_R10_CLAIM_GATE.csv",
    "1509_freeze": OUT / "P8_Y5_R10_1509_FREEZE_OR_PROCEED_LEDGER.csv",
    "1509_next": OUT / "P8_Y5_R10_1509_NEXT_TARGET.csv",
    "1509_anchor_curve": ANCHOR_CURVE,
    "1509_tau_schema": TAU_SCHEMA,
    "fig5b": FIG5B,
    "source_tex": SOURCE_TEX,
}

DIGITIZATION_PROTOCOL = OUT / "P8_Y5_R10_1510_DIGITIZATION_PROTOCOL.csv"
ROUTE_DECISION = OUT / "P8_Y5_R10_1510_ROUTE_DECISION.csv"
FREEZE_CONFIRMATION = OUT / "P8_Y5_R10_1510_R10_FREEZE_CONFIRMATION.csv"
GR_REENTRY_PLAN = OUT / "P8_Y5_R10_1510_PARENT_GR_DERIVATION_REENTRY_PLAN.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1510_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1510_DELTA_W_SCORE_READINESS.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1510_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1510_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1510_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1510_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1510_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1510"
QUAR_PROTOCOL = QUARANTINE / "R10_DIGITIZATION_PROTOCOL_NONCLAIM.csv"
QUAR_ROUTE = QUARANTINE / "ROUTE_DECISION_RETURN_TO_GR_NONCLAIM.csv"
QUAR_GR_PLAN = QUARANTINE / "PARENT_GR_REENTRY_PLAN_NONCLAIM.csv"
BRANCH_PROTOCOL = BRANCH_RESIDUALS / "r10_digitization_protocol_nonclaim_1510.csv"
BRANCH_ROUTE = BRANCH_RESIDUALS / "r10_route_decision_return_to_gr_nonclaim_1510.csv"
BRANCH_GR_PLAN = BRANCH_RESIDUALS / "parent_gr_reentry_plan_nonclaim_1510.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "R10_pass_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def protocol_rows() -> list[dict[str, Any]]:
    rows = [
        ("DIG1510_0_source_lock", "lock source artifact", "use local fig5b1.pdf and FB_ISL_pdf.tex; record hashes/bytes before extraction", "READY_SOURCE_LOCAL"),
        ("DIG1510_1_axis_calibration", "calibrate axes", "independently identify log10(lambda/m) and log10(|alpha|) axis ticks from the plotted figure", "NOT_DONE"),
        ("DIG1510_2_curve_trace", "trace 2020 upper envelope", "extract the 95 percent alpha-bound curve using at least two independent digitization passes", "NOT_DONE"),
        ("DIG1510_3_review_delta", "review discrepancy", "require pointwise agreement or bounded digitization uncertainty before accepting rows", "NOT_DONE"),
        ("DIG1510_4_metadata", "write provenance", "each row needs source pdf, calibration points, method, uncertainty, reviewer, and confidence", "NOT_DONE"),
        ("DIG1510_5_tau", "derive tau_R10(lambda)", "digitized bound curve is still insufficient without finite-source response kernel", "NOT_DONE"),
        ("DIG1510_6_parent_alpha", "connect parent alpha_predicted(lambda)", "bound curve is still insufficient without parent MTS alpha prediction or zero theorem", "NOT_DONE"),
        ("DIG1510_7_acceptance", "promote to live R10 curve", "only after DIG1510_1 through DIG1510_6 close", "BLOCKED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "protocol_id": protocol_id,
            "step": step,
            "requirement": requirement,
            "current_status": status,
            "source_file": rel(FIG5B) if "DIG1510" in protocol_id else "",
            **flags(),
        }
        for protocol_id, step, requirement, status in rows
    ]


def route_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ROUTE1510_0_digitize_now",
            "route": "reviewed R10 Fig. 5 digitization now",
            "benefit": "would improve empirical plumbing for one short-range test",
            "cost_or_limit": "still does not supply tau_R10 or parent alpha_predicted; risks token sink away from GR/Newton derivability",
            "decision": "DEFER",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ROUTE1510_1_return_to_gr",
            "route": "return to parent GR/Newton derivation spine",
            "benefit": "directly attacks the core theory requirement: recover GR/Newton the way GR recovers Newton",
            "cost_or_limit": "R10 remains frozen until curve/tau/alpha inputs are acquired",
            "decision": "SELECTED",
            **flags(),
        },
    ]


def freeze_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "freeze_id": "FREEZE1510_0",
            "object": "R10/local fifth-force scoring branch",
            "status": "FROZEN_NONCLAIM_CONFIRMED",
            "reason": "1509 proved only source-backed anchors, not a full curve/tau/parent-alpha package",
            "unfreeze_condition": "complete reviewed digitization or supplemental table, tau kernel, and parent alpha prediction/zero theorem",
            **flags(),
        }
    ]


def gr_reentry_rows() -> list[dict[str, Any]]:
    rows = [
        ("GR1510_0_inventory", "inventory existing EH/Newton/local-GR files", "find the strongest current parent-spine documents and residual ledgers", "NEXT"),
        ("GR1510_1_parent_action", "minimal parent action contract", "identify which fields remain fundamental and which must descend/decouple locally", "PENDING"),
        ("GR1510_2_bianchi", "Bianchi/conservation gate", "show extra residual stress is conserved, constrained, or zero in local branch", "PENDING"),
        ("GR1510_3_eh_limit", "Einstein-Hilbert local limit", "derive when the metric sector reduces to EH/Levi-Civita dynamics", "PENDING"),
        ("GR1510_4_newton_limit", "Newton/PPN weak-field limit", "derive Poisson equation, PPN residual vector, and zero/bound conditions", "PENDING"),
        ("GR1510_5_reopen_tests", "reopen empirical local tests", "only after parent GR/Newton branch supplies alpha/PPN residual predictions", "PENDING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reentry_id": reentry_id,
            "target": target,
            "objective": objective,
            "current_status": status,
            **flags(),
        }
        for reentry_id, target, objective, status in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLOCK1510_0", "digitization not performed and cannot be claim-ready without review"),
        ("BLOCK1510_1", "tau_R10 and parent alpha remain missing"),
        ("BLOCK1510_2", "R10 live derived curve/kernel files remain absent"),
        ("BLOCK1510_3", "parent GR/Newton derivation still incomplete"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": "return to derivation spine while preserving R10 freeze",
            **flags(),
        }
        for blocker_id, blocker in rows
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1510_0",
            "status": "NOT_SCORE_READY",
            "missing_blockers": "; ".join(row["blocker"] for row in blockers),
            "selected_route": "RETURN_TO_GR_NEWTON_DERIVATION",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1510_0",
            "object": "R10 scoring",
            "status": "FROZEN_NONCLAIM",
            "effect": "not abandoned, just not allowed to make claims",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1510_1",
            "object": "parent GR/Newton route",
            "status": "REENTRY_SELECTED",
            "effect": "next work should target derivability rather than more R10 plumbing",
            **flags(),
        },
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": blocker["blocker_id"].replace("BLOCK", prefix.upper()),
            "status": "RETAIN_BLOCKER",
            "item": blocker["blocker"],
            "reason": blocker["effect"],
            **flags(),
        }
        for blocker in blockers
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1510_0",
            "decision": "do not spend next work chunk on figure digitization",
            "rationale": "R10 needs full curve, tau, and parent alpha; digitization alone cannot unlock the claim gate",
            "next_action": "return to parent GR/Newton reentry spine",
            **flags(),
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1510_0_1511",
            "next_target": "1511-Y5-parent-GR-Newton-reentry-spine-inventory-and-strongest-local-limit-contract.md",
            "script": "scripts/Y5_parent_GR_Newton_reentry_spine_inventory_and_strongest_local_limit_contract.py",
            "objective": "inventory the strongest existing EH/Newton/local-GR derivation artifacts, extract the minimal local-limit contract, and select the next derivation target",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (DIGITIZATION_PROTOCOL, QUAR_PROTOCOL),
        (ROUTE_DECISION, QUAR_ROUTE),
        (GR_REENTRY_PLAN, QUAR_GR_PLAN),
        (DIGITIZATION_PROTOCOL, BRANCH_PROTOCOL),
        (ROUTE_DECISION, BRANCH_ROUTE),
        (GR_REENTRY_PLAN, BRANCH_GR_PLAN),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], protocol: list[dict[str, Any]], routes: list[dict[str, Any]], freeze: list[dict[str, Any]], gr_plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    fig_available = FIG5B.exists() and FIG5B.stat().st_size > 0
    protocol_blocks_live = any(row["protocol_id"] == "DIG1510_7_acceptance" and row["current_status"] == "BLOCKED" for row in protocol)
    route_selected = any(row["route_id"] == "ROUTE1510_1_return_to_gr" and row["decision"] == "SELECTED" for row in routes)
    r10_frozen = any(row["status"] == "FROZEN_NONCLAIM_CONFIRMED" for row in freeze)
    gr_next = any(row["reentry_id"] == "GR1510_0_inventory" and row["current_status"] == "NEXT" for row in gr_plan)
    live_targets_absent = not LIVE_BOUND_CURVE.exists() and not LIVE_TAU_KERNEL.exists()
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_PROTOCOL, QUAR_ROUTE, QUAR_GR_PLAN, BRANCH_PROTOCOL, BRANCH_ROUTE, BRANCH_GR_PLAN])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1510_0_sources", source_paths_exist, "all cited 1509 and R10 figure source paths exist"),
        ("VAL1510_1_fig_available", fig_available, "Fig. 5b source artifact is local and nonempty"),
        ("VAL1510_2_protocol_blocks_live", protocol_blocks_live, "digitization acceptance remains blocked until reviewed steps close"),
        ("VAL1510_3_route_selected", route_selected, "return-to-GR/Newton route selected"),
        ("VAL1510_4_r10_frozen", r10_frozen, "R10 scoring freeze confirmed"),
        ("VAL1510_5_gr_next", gr_next, "GR reentry inventory is the next derivation action"),
        ("VAL1510_6_live_targets_absent", live_targets_absent, "live R10 curve/kernel files remain absent"),
        ("VAL1510_7_csv_parse", csv_parse_ok, "all generated 1510 CSVs parse cleanly"),
        ("VAL1510_8_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
        ("VAL1510_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1510_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1510_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1510_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1510 froze R10 scoring, preserved a reviewed digitization protocol, and selected GR/Newton derivation reentry"
            if overall
            else "1510 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    protocol: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    freeze: list[dict[str, Any]],
    gr_plan: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1510 - Reviewed Figure Digitization Protocol or Return to GR Derivation",
                "",
                "## Verdict",
                "- Fig. 5b is local and can be digitized later, but digitization alone cannot unlock R10 because tau_R10(lambda) and parent alpha_predicted(lambda) are still missing.",
                "- The R10 scoring branch stays frozen as nonclaim; this is a scoring freeze, not a theory failure.",
                "- The selected next route is to return to the parent GR/Newton derivation spine and inventory the strongest local-limit artifacts.",
                "",
                "## Digitization Protocol",
                md_table(protocol, ["protocol_id", "step", "current_status"]),
                "",
                "## Route Decision",
                md_table(routes, ["route_id", "route", "decision", "cost_or_limit"]),
                "",
                "## Freeze Confirmation",
                md_table(freeze, ["freeze_id", "object", "status", "unfreeze_condition"]),
                "",
                "## GR/Newton Reentry Plan",
                md_table(gr_plan, ["reentry_id", "target", "current_status", "objective"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    protocol = protocol_rows()
    routes = route_decision_rows()
    freeze = freeze_rows()
    gr_plan = gr_reentry_rows()
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    local_rows = local_status_rows()
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(DIGITIZATION_PROTOCOL, protocol)
    write_csv(ROUTE_DECISION, routes)
    write_csv(FREEZE_CONFIRMATION, freeze)
    write_csv(GR_REENTRY_PLAN, gr_plan)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        DIGITIZATION_PROTOCOL,
        ROUTE_DECISION,
        FREEZE_CONFIRMATION,
        GR_REENTRY_PLAN,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, protocol, routes, freeze, gr_plan)
    write_csv(VALIDATION, validation)
    write_doc(protocol, routes, freeze, gr_plan, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
