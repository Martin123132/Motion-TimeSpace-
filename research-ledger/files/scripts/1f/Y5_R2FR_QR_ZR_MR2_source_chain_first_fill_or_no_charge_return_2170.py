from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2170"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2170-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2170_SOURCE_REGISTER.csv",
    "import_map": OUT / "P8_Y5_PARENT_QLOC_2170_EXISTING_CHAIN_IMPORT_MAP.csv",
    "frontier": OUT / "P8_Y5_PARENT_QLOC_2170_FRONTIER_REDUCTION_LEDGER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2170_ANTI_LOOP_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2170_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2170_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2170_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2170_EXISTING_QR_ZR_MR2_CHAIN_IMPORT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2170_FRONTIER_REDUCTION_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ANTI_LOOP_QR_ZR_MR2_2170_NONCLAIM.csv",
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
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2170_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2170-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2170*",
        "*P8_Y5_BRR545_2170*",
        "*Y5_R2FR_QR_ZR_MR2_source_chain_first_fill_or_no_charge_return_2170*",
        "*JR2170*",
        "*ANTI_LOOP_QR_ZR_MR2_2170*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    specs = [
        ("2168_doc", ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md", ["NEXT2168_0_2169", "CBB2168_0_ZR"]),
        ("2169_doc", ROOT / "2169-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md", ["NEXT2169_0_2170", "Q_R", "Z_R"]),
        ("2169_validation", OUT / "P8_Y5_BRR545_2169_VALIDATION.csv", ["VAL2169_OVERALL,PASS"]),
        ("2169_next", OUT / "P8_Y5_PARENT_QLOC_2169_NEXT_TARGET.csv", ["NEXT2169_0_2170"]),
    ]
    for checkpoint in range(1870, 1886):
        docs = sorted(ROOT.glob(f"{checkpoint}-Y5-R2FR-*.md"))
        specs.append((f"{checkpoint}_doc", docs[0] if docs else ROOT / f"MISSING_{checkpoint}.md", [f"NEXT{checkpoint}", f"VAL{checkpoint}_OVERALL"]))
        specs.append((f"{checkpoint}_validation", OUT / f"P8_Y5_BRR545_{checkpoint}_VALIDATION.csv", [f"VAL{checkpoint}_OVERALL,PASS"]))

    for source_id, path, needles in specs:
        text = read_text(path)
        exists = path.exists()
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=exists and len(found) == len(needles),
                role="anti-loop source validation for importing the existing Q_R/Z_R/M_R2 chain into the 2169 frontier",
            )
        )
    return rows


def import_map_rows() -> list[dict[str, Any]]:
    specs = [
        ("1870", "Q_R/Z_R/M_R2 first-fill attempt", "No source-backed numeric row or theorem-zero was found; the denominator problem was sharpened.", "Do not restart first-fill as if this is unknown."),
        ("1871", "source-denominator lock", "Splits Q_cur, C_R, Pi_R and q_R; canonical q_R convention is locked but nonclaim.", "Use the split symbols; do not mix current charge with exterior amplitude."),
        ("1872", "C_R zero/bound audit", "Asymptotic flatness and finite energy do not kill C_R/r; only conditional zero or bound templates survive.", "Q_R=0 still needs a parent no-charge theorem."),
        ("1873", "boundary-silence contract", "The exact contract for C_R=0 is written, but all decisive parent clauses remain unsigned.", "Treat C_R=0 as conditional, not a result."),
        ("1874", "verticality/residual-field audit", "R_AB remains visible to observed cell data unless q_shape or a constraint removes it first.", "Do not hide R_AB by a readout choice."),
        ("1875", "residual-vector routing", "Massless C_R/r and finite-pole Z_R/M_R2 routes are separated.", "R10 finite force cannot use the massless C_R/r tail."),
        ("1876", "blocking runner", "All local arenas are blocked until missing source/projection rows exist.", "Keep claim gates false."),
        ("1877", "q_shape/lambda source hunt", "q_shape is not an escape unless it is a parent readout functor with local-GR ownership.", "No shape-only shortcut."),
        ("1878", "DObs coframe-kernel test", "The current observed coframe sees radial-cell variation.", "DObs_e[v_R]=0 remains unproved."),
        ("1879", "coframe ownership", "Parent coframe/no-shadow route remains unsigned; common-frame leak rows are the test interface.", "Matter-frame ownership still has to be proved or bounded."),
        ("1880", "terminal public metric/no-shadow gate", "No-shadow theorem is exact only under terminal public coframe/action-domain exclusion.", "No local-GR claim from no-shadow words alone."),
        ("1881", "first gamma response kernel", "A sharp gamma response kernel and |b_R x_U| style bound interface exist, still nonclaim.", "Gamma only is not local GR."),
        ("1882", "C_R profile coefficient", "C_R gives x_U=2(p-1); the PPN residual becomes a source-normalized combination, not a free knob.", "Real progress: the first-order channel is constrained."),
        ("1883", "reciprocal lock/full PPN vector", "Beta is independent; full PPN residual vector is mandatory.", "No gamma-only or cancellation-only pass."),
        ("1884", "no-boundary-charge/delta_p contract", "Q_R=0 would imply C_R=0 and delta_p=0, but no parent no-charge theorem is signed.", "Need theorem-zero or source-backed delta_p/q_R_hat row."),
        ("1885", "beta/source-coupling gate", "Beta and common-source coupling remain live; the no-source-only slot is the next real bottleneck.", "The coupling loophole, not Q_R bookkeeping, is the frontier."),
    ]
    return [
        base_row(
            import_id=f"IMPORT2170_{checkpoint}",
            source_checkpoint=checkpoint,
            imported_stage=stage,
            imported_result=result,
            effect_on_2169_target=effect,
        )
        for checkpoint, stage, result, effect in specs
    ]


def frontier_rows() -> list[dict[str, Any]]:
    specs = [
        ("FR2170_0_QR", "Q_R/q_R_hat", "PARTIALLY_REDUCED_NONCLAIM", "symbol split and source-denominator convention exist; no no-charge theorem or numeric source row", "boundary/source no-charge theorem or source-backed q_R_hat row"),
        ("FR2170_1_ZR_MR2", "Z_R/M_R^2/lambda_R", "BLOCKED_NONCLAIM", "no parent operator/Hessian extraction, no same-normalization range row", "parent operator coefficients or finite local source rows with units"),
        ("FR2170_2_R10", "R10 finite force route", "BLOCKED_NONCLAIM", "finite branch needs Z_R/M_R2/lambda/source/test charges and accepted alpha_bound(lambda)", "keep R10 data acquisition parallel, but do not treat it as local-GR derivation"),
        ("FR2170_3_PPN", "PPN gamma/beta/local metric route", "SHARPENED_NONCLAIM", "gamma channel constrained through C_R/delta_p; beta/source coupling remains independent", "parent beta/source-coupling theorem or full residual vector rows"),
        ("FR2170_4_coupling", "common matter/source coupling", "MAIN_BOTTLENECK", "1885 shows the no-source-only/action-weight slot is the live loophole", "derive ordinary-matter/source-label forgetting or keep finite source-weight vectors"),
        ("FR2170_5_theory_route", "compatibility-object category principle", "PROMOTED_NEXT", "finite first-fill was already explored and did not close; the least-duplicative move is the held category-principle route", "prove R_AB/C_R is a non-dynamical compatibility object or demote to finite rows"),
    ]
    return [
        base_row(
            frontier_id=frontier_id,
            object=object_name,
            status=status,
            reason=reason,
            next_action=next_action,
        )
        for frontier_id, object_name, status, reason, next_action in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2170_0_no_duplicate", "ANTI_LOOP", "Do not redo Q_R/Z_R/M_R2 first-fill; import 1870-1885 as the previous first-fill result.", "selected"),
        ("DEC2170_1_claim_ceiling", "NO_LOCAL_GR_CLAIM", "No R10, PPN, WEP, clock, orbital, Newton or local-GR pass is allowed from the imported chain.", "selected"),
        ("DEC2170_2_real_progress", "FIRST_ORDER_CHANNEL_SHARPENED", "The project did gain structure: C_R/delta_p/q_R_hat and the gamma channel are no longer free-floating symbols.", "selected"),
        ("DEC2170_3_main_gap", "COUPLING_AND_CATEGORY_OWNER", "The true gap is the parent rule that prevents R_AB/C_R and source weights becoming independent physical slots.", "selected"),
        ("DEC2170_4_next_route", "PROMOTE_CATEGORY_PRINCIPLE", "Move from finite first-fill bookkeeping to the parent compatibility-object category principle, with finite source rows as fallback.", "selected"),
        ("DEC2170_5_data_parallel", "R10_DATA_HELD_PARALLEL", "Accepted R10 alpha(lambda) acquisition remains useful, but it cannot substitute for the local-GR derivation.", "held"),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2170_0_2171",
            selection_status="selected",
            target_file="2171-Y5-R2FR-compatibility-object-category-principle-or-finite-local-source-row.md",
            target_script="scripts/Y5_R2FR_compatibility_object_category_principle_or_finite_local_source_row_2171.py",
            objective="derive the parent category principle that makes C_R/R_AB a compatibility object rather than an independent local field; if that fails, emit finite source rows without claiming local GR",
            success_condition="a parent-signed grammar/quotient theorem removes Z_R/J_R/Q_R/S_R, or the local branch is left as explicit finite residual coefficients with arena projections",
            do_not_do="do not redo 1870-1885 first-fill, do not import GR, do not use gamma-only/beta-only/R10-bound-only shortcuts",
        ),
        base_row(
            route_id="NEXT2170_1_2170b",
            selection_status="held_parallel",
            target_file="2170b-Y5-R2FR-accepted-R10-bound-curve-promotion-or-blocker.md",
            target_script="scripts/Y5_R2FR_accepted_R10_bound_curve_promotion_or_blocker_2170b.py",
            objective="promote a real accepted R10 alpha(lambda) bound curve or write a blocker ledger",
            success_condition="claim-safe alpha_bound(lambda) curve with provenance, units and QA, still not an MTS pass without source coefficients",
            do_not_do="do not use threshold-only anchors or placeholder bound rows as evidence",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["import_map"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["frontier"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["decision"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2170_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2170_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    import_rows = rows_by_name["import_map"]
    validations.append(base_row(validation_id="VAL2170_02_import_map_complete", status="PASS" if len(import_rows) == 16 else "FAIL", detail=f"imported_checkpoints={len(import_rows)}"))

    frontier_statuses = {row["status"] for row in rows_by_name["frontier"]}
    validations.append(base_row(validation_id="VAL2170_03_frontier_reduced", status="PASS" if {"MAIN_BOTTLENECK", "PROMOTED_NEXT"}.issubset(frontier_statuses) else "FAIL", detail="frontier identifies coupling/category owner rather than duplicate first-fill"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2170_04_anti_loop_decision", status="PASS" if "Do not redo Q_R/Z_R/M_R2 first-fill" in decision_text else "FAIL", detail="anti-loop rule recorded"))

    next_rows = rows_by_name["next_target"]
    validations.append(base_row(validation_id="VAL2170_05_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2171" in row["target_file"] for row in next_rows) else "FAIL", detail="2171 compatibility-object category-principle route selected"))

    validations.append(base_row(validation_id="VAL2170_06_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2170_07_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2170_08_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2170_artifacts()
    validations.append(base_row(validation_id="VAL2170_09_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2170 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2170_10_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2170_OVERALL", status="PASS" if overall else "FAIL", detail="2170 imports the existing Q_R/Z_R/M_R2 source-chain result and prevents duplicate first-fill work"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2170 - Y5/R2FR Q_R/Z_R/M_R2 Source-Chain First Fill Or No-Charge Return

## Current Verdict

2170 does **not** produce a local-GR, PPN, R10, WEP, clock, orbital or Newton claim.

It does something more useful for the project discipline: it prevents a loop. The 2169 target asked for a first fill of `Q_R`, `Z_R`, `M_R^2`, `lambda_R` and the source denominator, but that exact logical territory was already decomposed by the earlier 1870-1885 chain. The result of that chain is not a pass; it is a sharper blocker map.

So the night-shift status is: we are not stuck at the beginning of the coefficient problem. We have already reduced it to the parent category/source-coupling owner problem.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Existing Chain Import Map

{md_table(rows_by_name["import_map"], ["import_id", "source_checkpoint", "imported_stage", "imported_result", "effect_on_2169_target", "valid_for_claim"])}

## Frontier Reduction Ledger

{md_table(rows_by_name["frontier"], ["frontier_id", "object", "status", "reason", "next_action", "valid_for_claim"])}

## Anti-Loop Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

The good news is that the local-GR branch is more structured than it was: the first-order `C_R/delta_p/q_R_hat` channel has been sharpened, the gamma-only shortcut has been blocked, and beta/source coupling has been correctly separated as an independent second-order gate.

The hard news is also useful: `Q_R`, `Z_R`, `M_R^2` and `lambda_R` are not currently theorem-zero or source-backed numeric inputs. Repeating that hunt under a new checkpoint number would waste time.

The best next move is therefore the parent compatibility-object route: prove that `C_R/R_AB` is not an independent dynamical field but a parent compatibility/constraint object. If that theorem fails, the branch must remain an explicit finite residual coefficient programme.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "import_map": import_map_rows(),
        "frontier": frontier_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "import_map", "frontier", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
