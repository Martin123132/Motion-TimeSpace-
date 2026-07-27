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

DOC = ROOT / "2822-Y5-R2FR-first-same-norm-Jq-component-bound-or-zero-row-for-local-lock-under-AX1090.md"

SRC_2821_NEXT = RESIDUALS / "P8_Y5_R2FR_2821_NEXT_TARGET.csv"
SRC_2821_DECISION = RESIDUALS / "P8_Y5_R2FR_2821_DECISION_LEDGER.csv"
SRC_2821_JQ_MAP = RESIDUALS / "P8_Y5_R2FR_2821_JQ_COMPONENT_MAP_FOR_LOCAL_LOCK.csv"
SRC_2821_SAME_NORM = RESIDUALS / "P8_Y5_R2FR_2821_SAME_NORM_PRODUCT_CONTRACT.csv"
SRC_2821_ZERO = RESIDUALS / "P8_Y5_R2FR_2821_ORDINARY_MATTER_ZERO_ROUTE_AUDIT.csv"
SRC_2821_REENTRY = RESIDUALS / "P8_Y5_R2FR_2821_LOCAL_LOCK_REENTRY_DECISION.csv"
SRC_1088_THEOREM = RESIDUALS / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
SRC_1088_SIGNATURE = RESIDUALS / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
SRC_1090_SYNTHESIS = RESIDUALS / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv"
SRC_1090_AXIOMS = RESIDUALS / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
SRC_2795_COVERAGE = RESIDUALS / "P8_Y5_R2FR_2795_MOMS_CLAUSE_COVERAGE_MATRIX.csv"
SRC_2431_ZERO = RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_DESCENT_ZERO_THEOREM.csv"
SRC_2431_BOUND = RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_TO_Q_RESIDUAL_BOUND_LAW.csv"
SRC_2759_PACK = RESIDUALS / "P8_Y5_R2FR_2759_FINITE_JQ_SOURCE_PACK.csv"
SRC_2760_COUNTER = RESIDUALS / "P8_Y5_R2FR_2760_COUNTERMODEL_TO_JQ_MAP.csv"
SRC_2820_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2820_EQ_MU_GAB_EXTRACTION_STATUS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2822_SOURCE_REGISTER.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_2822_ORDINARY_MATTER_ZERO_CERTIFICATE_ATTEMPT.csv",
    "first_row": RESIDUALS / "P8_Y5_R2FR_2822_FIRST_SAME_NORM_JQ_COMPONENT_ROW.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_2822_COMPONENT_BOUND_FALLBACK_VECTOR.csv",
    "impact": RESIDUALS / "P8_Y5_R2FR_2822_LOCAL_LOCK_IMPACT_GATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2822_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2822_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2822_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2822_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2822_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_weight": SOURCE_WEIGHT / "first_same_norm_Jq_component_2822_NONCLAIM.csv",
    "local_bound": LOCAL_BOUNDS / "Jq_component_bound_vector_2822_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2822_SAME_NORM_CARRIER_Q_NORMALIZATION_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_FIRST_SAME_NORM_JQ_COMPONENT_2822"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC2822_0_2821_next", SRC_2821_NEXT, "NEXT2821_0_2822", "2821 handoff to first same-norm Jq component row"),
        ("SRC2822_1_2821_decision", SRC_2821_DECISION, "DEC2821_3_next", "component-row decision"),
        ("SRC2822_2_2821_jq_map", SRC_2821_JQ_MAP, "JQM2821_1_matter;JQM2821_8_same_branch_lock", "component map and branch lock"),
        ("SRC2822_3_2821_same_norm", SRC_2821_SAME_NORM, "SN2821_0_Eq;SN2821_3_product", "same-norm contract and missing E_q"),
        ("SRC2822_4_2821_zero", SRC_2821_ZERO, "ZRO2821_1_moms_transfer;ZRO2821_4_latest_coverage", "ordinary-matter zero route"),
        ("SRC2822_5_2821_reentry", SRC_2821_REENTRY, "RE2821_6_local_lock", "local-lock reentry refusal"),
        ("SRC2822_6_1088_theorem", SRC_1088_THEOREM, "THM1088_5_conclusion;THM1088_6_current_corpus_verdict", "conditional MOMS zero theorem"),
        ("SRC2822_7_1088_signature", SRC_1088_SIGNATURE, "MOMS1088_0_action_form;MOMS1088_7_verdict", "MOMS signature clauses"),
        ("SRC2822_8_1090_synthesis", SRC_1090_SYNTHESIS, "SYN1090_7_zero_theorem_if_axioms;SYN1090_8_verdict", "MOMS synthesis failure"),
        ("SRC2822_9_1090_axioms", SRC_1090_AXIOMS, "AX1090_0_parent_object;AX1090_4_variation_domain_order", "missing axioms not adopted"),
        ("SRC2822_10_2795_coverage", SRC_2795_COVERAGE, "MOMS2794_7_all_in_one", "latest coverage matrix"),
        ("SRC2822_11_2431_zero", SRC_2431_ZERO, "JZT2431_2_bulk_matter_subcase;JZT2431_5_total_verdict", "Jq zero theorem and component-vector requirement"),
        ("SRC2822_12_2431_bound", SRC_2431_BOUND, "JQB2431_0_functional_norm;JQB2431_4_verdict", "component no-cancellation bound law"),
        ("SRC2822_13_2759_pack", SRC_2759_PACK, "JQPACK2759_1_matter;JQPACK2759_8_same_branch_lock", "R2FR source-pack component rows"),
        ("SRC2822_14_2760_counter", SRC_2760_COUNTER, "CM2760_0_alpha;CM2760_5_finite_range", "surviving hidden-visible countermodels"),
        ("SRC2822_15_2820_extraction", SRC_2820_EXTRACTION, "EXT2820_1_GAB;EXT2820_3_Eq", "missing E_q carrier"),
    ]
    return [source_row(*spec) for spec in specs]


def zero_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "OMZ2822_0_target",
            "ordinary-matter J_q component",
            "j_matter = 0 under full MOMS/AX1090 signature",
            "TARGET_CONDITIONAL_ZERO",
            "MOMS1088 clauses would kill the ordinary matter source leg",
            SRC_1088_THEOREM,
            "THM1088_5_conclusion",
        ),
        (
            "OMZ2822_1_signature",
            "MOMS/AX1090 signature adoption",
            "MOMS1088_0..6 all parent-derived in one action",
            "SIGNATURE_NOT_PARENT_DERIVED",
            "the exact clause exists only as a future contract",
            SRC_1088_SIGNATURE,
            "MOMS1088_7_verdict",
        ),
        (
            "OMZ2822_2_synthesis",
            "derive MOMS from existing contracts",
            "compose parent action object, quotient coframe, matter bundle, constants, measure, no-shadow, variation order",
            "SYNTHESIS_FAILS_MISSING_AXIOMS",
            "contract repetition does not derive the common parent owner",
            SRC_1090_SYNTHESIS,
            "SYN1090_8_verdict",
        ),
        (
            "OMZ2822_3_latest_coverage",
            "latest MOMS coverage",
            "no single source signs all clauses",
            "NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "ordinary matter zero cannot be promoted",
            SRC_2795_COVERAGE,
            "MOMS2794_7_all_in_one",
        ),
        (
            "OMZ2822_4_bound_fallback",
            "ordinary-matter finite bound",
            "||J_q^matter||_{E_q*} <= B_matter^q",
            "BOUND_ROW_REQUIRED_NONCLAIM",
            "same-norm carrier E_q and numeric/source-backed B_matter^q are missing",
            SRC_2431_BOUND,
            "JQB2431_0_functional_norm",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "attempt_id": attempt_id,
                "target": target,
                "formula_or_clause": formula,
                "status": status,
                "reason": reason,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "theorem_zero_adopted": False,
                "component_bound_ready": False,
            }
        )
        for attempt_id, target, formula, status, reason, source_path, anchor in specs
    ]


def first_component_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "component_row_id": "JQC2822_0_j_matter_first_row",
                "component": "j_matter",
                "component_definition": "ordinary-matter vertical source leg in J_q",
                "same_norm_quantity": "||J_q^matter||_{E_q*}",
                "same_norm_carrier": "E_q",
                "same_norm_status": "MISSING_PARENT_EQ_NORM",
                "zero_formula": "MOMS/AX1090 signed => j_matter=0",
                "zero_status": "CONDITIONAL_ZERO_NOT_PROMOTED",
                "finite_bound_formula": "||J_q^matter||_{E_q*} <= B_matter^q",
                "value_or_bound": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
                "units_or_normalization": "dual E_q units; unresolved until G_AB/mu_q/q-normalization are parent-owned",
                "source_path": str(SRC_2759_PACK) + ";" + str(SRC_1088_THEOREM) + ";" + str(SRC_2821_SAME_NORM),
                "source_anchor": "JQPACK2759_1_matter;THM1088_5_conclusion;SN2821_0_Eq",
                "source_backed": False,
                "numeric_value_present": False,
                "theorem_zero_adopted": False,
                "branch_locked": True,
                "feeds_2818_reentry": False,
            }
        )
    ]


def fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("FB2822_0_total", "j_q_total", "sum_i ||J_q^i||_{E_q*}", "COMPONENT_SUM_REQUIRED", "needs all component zero/bound rows", "bookkeeping"),
        ("FB2822_1_matter", "j_matter", "||J_q^matter||_{E_q*} <= B_matter^q", "FIRST_ROW_STAGED_NONCLAIM", "ordinary zero not promoted and B_matter^q missing", "PPN/WEP/clock source silence"),
        ("FB2822_2_const", "j_const", "||J_q^const||_{E_q*} <= B_const^q", "BOUND_ROW_REQUIRED", "constant-sector superselection or sensitivities missing", "EM/clocks/WEP/particle ratios"),
        ("FB2822_3_weight", "j_weight", "||J_q^weight||_{E_q*} <= B_weight^q", "BOUND_ROW_REQUIRED", "common action measure/source-label forgetting theorem missing", "source normalization/WEP/orbital"),
        ("FB2822_4_shadow", "j_shadow", "||J_q^shadow||_{E_q*} <= B_shadow^q", "BOUND_ROW_REQUIRED", "no-shadow operator-domain theorem missing", "PPN gamma/WEP/clocks"),
        ("FB2822_5_readout", "j_readout", "||J_q^readout||_{E_q*} <= B_readout^q", "BOUND_ROW_REQUIRED", "variation-before-readout plus detector/source model missing", "calibration/source selection"),
        ("FB2822_6_boundary", "j_boundary", "||J_q^boundary||_{E_q*} <= B_boundary^q", "BOUND_ROW_REQUIRED", "body charge/no-flux theorem or explicit bound missing", "finite-range/orbital/local force"),
        ("FB2822_7_curvature", "j_curvature", "||J_q^curvature||_{E_q*} <= B_curvature^q", "BOUND_ROW_REQUIRED", "D_q curvature coefficient or bound missing", "R10/local geometry residual"),
    ]
    return [
        nonclaim(
            {
                "fallback_id": fallback_id,
                "component": component,
                "bound_or_zero_row": formula,
                "status": status,
                "missing_for_claim": missing,
                "arena_risk": arena,
                "same_norm_carrier": "E_q",
                "same_norm_status": "MISSING_PARENT_EQ_NORM",
                "source_path": str(SRC_2759_PACK),
                "source_anchor": component if component != "j_q_total" else "JQPACK2759_0_total",
                "source_backed": False,
                "numeric_value_present": False,
                "theorem_zero_adopted": False,
            }
        )
        for fallback_id, component, formula, status, missing, arena in specs
    ]


def impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("IMP2822_0_zero_attempt", "ordinary matter zero", "REFUSED_NOT_PARENT_SIGNED", "MOMS/AX1090 signature is conditional only", False),
        ("IMP2822_1_first_row", "first same-norm component row", "WRITTEN_NONCLAIM", "j_matter row exists with theorem-zero premises and finite-bound placeholder", False),
        ("IMP2822_2_Eq", "same-norm carrier E_q", "BLOCKED", "G_AB/mu_q/q normalization remain missing", False),
        ("IMP2822_3_component_vector", "J_q component vector", "SCHEMA_READY_VALUES_MISSING", "remaining components need zero theorem or source-backed bound", False),
        ("IMP2822_4_Nlock", "2818 N_lock", "NO_REENTRY", "T_source_norm and C_qm cannot be source-backed", False),
        ("IMP2822_5_claims", "local GR/Newton/PPN/R10", "BLOCKED_NO_CLAIM", "component row is not a prediction", False),
    ]
    return [
        nonclaim(
            {
                "impact_id": impact_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "reentry_allowed": allowed,
            }
        )
        for impact_id, obj, status, reason, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    zero_adopted = any(row["theorem_zero_adopted"] for row in rows["zero_attempt"])
    first_row_exists = len(rows["first_row"]) == 1
    eq_ready = any(row["same_norm_status"] != "MISSING_PARENT_EQ_NORM" for row in rows["first_row"])
    source_backed = any(row["source_backed"] for row in rows["first_row"])
    reentry = any(row["reentry_allowed"] for row in rows["impact"])
    specs = [
        ("CG2822_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2822_1_first_row", "first same-norm component row written", first_row_exists, "j_matter row is staged as nonclaim"),
        ("CG2822_2_ordinary_zero", "ordinary matter theorem-zero promoted", zero_adopted, "MOMS/AX1090 signature not parent-derived"),
        ("CG2822_3_Eq", "same-norm E_q carrier accepted", eq_ready, "E_q/q-normalization missing"),
        ("CG2822_4_bound_value", "component bound source-backed", source_backed, "B_matter^q has no numeric/source-backed value"),
        ("CG2822_5_local_lock_reentry", "local-lock reentry allowed", reentry, "T_source_norm*C_qm remains nonclaim"),
        ("CG2822_6_local_claim", "local GR/Newton/PPN/R10 claim allowed", False, "no sourced local branch exists"),
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
        ("DEC2822_0_zero_attempt", "Ordinary-matter zero was attempted first.", "CONDITIONAL_ZERO_NOT_PROMOTED", "MOMS/AX1090 is exact as a contract but not parent-derived", "keep j_matter finite row live"),
        ("DEC2822_1_first_row", "First same-norm component row now exists.", "J_MATTER_ROW_STAGED_NONCLAIM", "the row names theorem-zero premises, bound formula, units problem, and branch lock", "use it as the template for remaining components"),
        ("DEC2822_2_blocker", "The new bottleneck is not algebra; it is the same-norm carrier.", "EQ_NORMALIZATION_BLOCKER", "without E_q/G_AB/mu_q/q normalization, no component row can feed 2818", "derive or fix the E_q carrier next"),
        ("DEC2822_3_next", "Next target is same-norm carrier and q-normalization.", "NEXT_2823_EQ_CARRIER", "component bounds need a shared norm before they become testable residual inputs", "derive E_q or explicitly demote component rows to external control-only ledgers"),
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
                "next_id": "NEXT2822_0_2823",
                "status": "selected_primary",
                "target_doc": "2823-Y5-R2FR-same-norm-Eq-carrier-and-q-normalization-for-Jq-component-rows-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_same_norm_Eq_carrier_and_q_normalization_for_Jq_component_rows_under_AX1090_2823.py",
                "mission": "derive or reject the shared E_q carrier, G_AB/mu_q coefficient, q normalization, and dual units needed for J_q component rows to feed the 2818 local-lock amplitude law",
                "acceptance": "either provide a parent-signed same-norm carrier for J_q and Dq[v_m], or record that component rows remain control-only placeholders with valid_for_claim=false",
                "forbidden": "do not hand-insert E_q coefficients; do not mix branch denominators and source numerators; do not claim local GR/Newton/PPN/R10; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2822_0_source_weight", OUTPUTS["first_row"], BRANCH_OUTPUTS["source_weight"], "source-weight copy of first same-norm Jq component row"),
        ("BR2822_1_local_bound", OUTPUTS["fallback"], BRANCH_OUTPUTS["local_bound"], "local-bound copy of component fallback vector"),
        ("BR2822_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for same-norm carrier/q-normalization target"),
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
                    if not item or item.startswith("http"):
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


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2822_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2822_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2822_2_zero_not_promoted", not any(row["theorem_zero_adopted"] for row in rows_by_name["zero_attempt"]), "ordinary-matter zero theorem was not promoted"),
        ("VAL2822_3_first_row_exists", len(rows_by_name["first_row"]) == 1, "one first same-norm component row was written"),
        ("VAL2822_4_first_row_nonclaim", not any(row["source_backed"] or row["numeric_value_present"] or row["theorem_zero_adopted"] for row in rows_by_name["first_row"]), "first row remains nonclaim and unsourced"),
        ("VAL2822_5_Eq_blocked", all(row.get("same_norm_status") == "MISSING_PARENT_EQ_NORM" for row in rows_by_name["first_row"]), "first row correctly records missing E_q carrier"),
        ("VAL2822_6_impact_blocks_reentry", not any(row["reentry_allowed"] for row in rows_by_name["impact"]), "local-lock reentry remains blocked"),
        ("VAL2822_7_next_target_2823", any(row["next_id"] == "NEXT2822_0_2823" and row["selected"] for row in rows_by_name["next"]), "same-norm carrier/q-normalization selected next"),
        ("VAL2822_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2822_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2822_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2822_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2822_12_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2822_13_generated_under_post_checkpoint", all(str(path).startswith(str(ROOT)) for path in output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2822_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2822_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2822_OVERALL",
            "passed": overall,
            "detail": "2822 attempts ordinary-matter theorem-zero first, refuses promotion because MOMS/AX1090 is unsigned, writes the first nonclaim same-norm j_matter component row, and selects E_q carrier/q-normalization next.",
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
    content = f"""# 2822 - Y5 R2FR First Same-Norm Jq Component Bound Or Zero Row For Local Lock Under AX1090

Status: `Y5_R2FR_2822_first_jmatter_component_row_nonclaim_Eq_carrier_selected_next`

## Private Verdict

2822 takes the first concrete component shot.

The ordinary-matter zero theorem is mathematically clean: under the full MOMS/AX1090 signature, ordinary matter contributes no vertical `J_q` source leg. But the current corpus still does not derive that signature from one parent action, so `j_matter=0` cannot be adopted.

The useful progress is that the first component row now exists in a branch-locked form:

`||J_q^matter||_{{E_q*}} <= B_matter^q`

with the conditional zero route recorded and the finite-bound placeholder retained. This is not claim-ready because `E_q`, `G_AB`, `mu_q`, q-normalization, and a numeric/source-backed `B_matter^q` are still missing.

So the next move is not more verbal coupling work. It is the same-norm carrier: derive or reject the shared `E_q` norm that lets `J_q` and `Dq[v_m]` live in the same branch.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Ordinary Matter Zero Certificate Attempt

{markdown_table(rows["zero_attempt"], ["attempt_id", "target", "status", "reason", "theorem_zero_adopted", "component_bound_ready", "valid_for_claim"])}

## First Same Norm Jq Component Row

{markdown_table(rows["first_row"], ["component_row_id", "component", "same_norm_status", "zero_status", "finite_bound_formula", "value_or_bound", "branch_locked", "feeds_2818_reentry", "valid_for_claim"])}

## Component Bound Fallback Vector

{markdown_table(rows["fallback"], ["fallback_id", "component", "status", "bound_or_zero_row", "missing_for_claim", "same_norm_status", "valid_for_claim"])}

## Local Lock Impact Gate

{markdown_table(rows["impact"], ["impact_id", "object", "status", "reason", "reentry_allowed", "valid_for_claim"])}

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
    rows["zero_attempt"] = zero_attempt_rows()
    rows["first_row"] = first_component_rows()
    rows["fallback"] = fallback_rows()
    rows["impact"] = impact_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "zero_attempt", "first_row", "fallback", "impact", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2822_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2822_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
