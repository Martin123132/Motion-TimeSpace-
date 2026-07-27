from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1957_VALIDATION.csv"

SOURCES = {
    "1956_doc": {
        "path": ROOT / "1956-Y5-R2FR-parent-action-variation-signature-for-local-EH-map.md",
        "needles": ["SIG1956_2_total_Hilbert_source", "RES1956_1_DeltaT_w", "NEXT1956_0_primary"],
    },
    "1956_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1956_VALIDATION.csv",
        "needles": ["VAL1956_OVERALL", "PASS"],
    },
    "956_source_spine": {
        "path": ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
        "needles": ["SSG956_1_no_species_source_functor", "SSG956_2_total_Hilbert_source", "HCG956_2_nonHilbert_current"],
    },
    "1476_source_label": {
        "path": ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
        "needles": ["SLF1476_0_target", "SLP1476_3_current_owner", "SLP1476_4_nonHilbert_silence"],
    },
    "1465_matter_graph": {
        "path": ROOT / "1465-Y5-R10-RAB-ordinary-matter-graph-certificate-or-CMSM-session-filelist-capture.md",
        "needles": ["GC1465_0_template_connected", "GC1465_1_parent_graph_certificate"],
    },
    "990_parent_contract": {
        "path": ROOT / "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
        "needles": ["PAC990_2_matter_functor", "PAC990_5_Ward_Bianchi"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1957 source-map signature or residual current bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def theorem_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SM1957_0_target",
            "ordinary matter contributes the GR/EH Hilbert source only",
            "DeltaT_source = DeltaT_w + DeltaT_nonHilbert + DeltaT_readout = 0",
            "THEOREM_TARGET_EXACT",
            "This is the source-side route needed by the residual l=2/Cassini branch.",
            "all source-map clauses must be parent-signed",
        ),
        (
            "SM1957_1_source_functor_domain",
            "source functor has no species/source-label slot and varies before readout",
            "F_source(Phi_matter)=delta S_matter/delta e_obs, not F(A,material,readout)",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "If signed, species labels become bookkeeping rather than physical source weights.",
            "parent-sign variation-before-readout and readout no-reentry",
        ),
        (
            "SM1957_2_connected_matter_category",
            "ordinary matter graph is connected enough that a natural action-density/source weight collapses to one constant",
            "w_B F(f)=F(f) w_A with connected nonzero graph -> w_A=w_*",
            "EXACT_CONDITIONAL_THEOREM_GRAPH_UNSIGNED",
            "The algebraic theorem is good; the parent-owned graph certificate is not complete.",
            "parent-owned nonzero morphisms for ordinary matter graph",
        ),
        (
            "SM1957_3_current_owner",
            "active current is the Hilbert/coframe variation of the same matter action",
            "J_active = J_Hilbert[S_matter,e_obs]",
            "CURRENT_OWNER_NOT_SIGNED",
            "This is the main current-owner debt: no separate active current may bypass Hilbert stress.",
            "derive Noether/Hilbert/readout current owner stack",
        ),
        (
            "SM1957_4_nonHilbert_silence",
            "spin/torsion/boundary/non-Hilbert current bypass is absent, exact/projected silent, or bounded",
            "P_2[J_NH]=0 or |P_2[J_NH]| <= sourced envelope",
            "OPEN_PARALLEL_GATE",
            "This cannot be killed by source-label forgetting alone.",
            "prove J_NH=0/exact/projected-silent or emit numeric residual",
        ),
        (
            "SM1957_5_readout_no_reentry",
            "source weights do not re-enter after variation through readout/frame/domain markers",
            "DeltaT_readout=0 if readout map has no source-label/domain spurion",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "This blocks fake passes where source labels disappear during variation but return in measurement.",
            "parent no-reentry theorem or retained marker residual rows",
        ),
        (
            "SM1957_6_verdict",
            "the source-map theorem is not closed at 1957",
            "DeltaT_source=0 blocked by graph owner, current owner, non-Hilbert silence, and readout no-reentry",
            "ZERO_PROOF_FAILED_CLEANLY",
            "Still useful: the source-side debt is now a finite residual-current vector, not a fog bank.",
            "next attack current-owner/non-Hilbert silence or residual current envelopes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def residual_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CUR1957_0_DeltaT_source_bound",
            "||DeltaT_source,l2||",
            "||DeltaT_w,l2|| + ||DeltaT_NH,l2|| + ||DeltaT_readout,l2||",
            "MISSING_FACTORS",
            "source-current units",
            "combined source-side residual bound; not scoreable yet",
        ),
        (
            "CUR1957_1_DeltaT_w",
            "||DeltaT_w,l2||",
            "species/source-label/source-weight residual current after GR baseline subtraction",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "source-current units",
            "prove source-label forgetting or source delta_w envelope",
        ),
        (
            "CUR1957_2_DeltaT_NH",
            "||DeltaT_NH,l2||",
            "non-Hilbert active current l=2 bypass residual",
            "MISSING_NONHILBERT_SILENCE_OR_BOUND",
            "source-current units",
            "prove absent/exact/projected-silent or source numeric envelope",
        ),
        (
            "CUR1957_3_DeltaT_readout",
            "||DeltaT_readout,l2||",
            "post-variation readout/domain/frame re-entry residual",
            "MISSING_READOUT_NO_REENTRY_OR_BOUND",
            "source-current units",
            "prove readout no-reentry or source marker envelope",
        ),
        (
            "CUR1957_4_projection_to_STF",
            "DeltaB_source2",
            "kernel projection of residual source current into Cassini-visible STF profile",
            "MISSING_KERNEL_NORM_AND_SOURCE_ENVELOPE",
            "dimensionless profile units",
            "requires residual current envelopes plus K_2/W_STF readout",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, status, units, next_action in entries:
        row = base(row_id)
        row.update(
            {
                "symbol": symbol,
                "definition": definition,
                "status": status,
                "units": units,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1957_0_source_zero",
            "source-functor + connected graph + current owner + non-Hilbert silence + no readout reentry -> DeltaT_source=0",
            "DeltaB_source2=0",
            "MISSING_GRAPH_OWNER;MISSING_CURRENT_OWNER;MISSING_NONHILBERT_SILENCE;MISSING_READOUT_NO_REENTRY",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "cannot claim same-source map",
        ),
        (
            "RUN1957_1_conditional_label_forgetting",
            "connected natural source functor kills relative source weights",
            "DeltaT_w=0 conditionally",
            "MISSING_PARENT_GRAPH_AND_CURRENT_SIGNATURE",
            "PASS_NONCLAIM_CONDITIONAL_ROUTE",
            "useful route, not a source-map proof",
        ),
        (
            "RUN1957_2_residual_current_bound",
            "||DeltaT_source,l2|| <= sum residual current envelopes",
            "projected S_TF_extra <= 6.7e-5 after K_2/W_STF",
            "MISSING_RESIDUAL_CURRENT_ENVELOPES;MISSING_KERNEL_NORM;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback empirical route not scoreable",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1957_0_theorem_target", "Exact ordinary source-map theorem target exists.", "PASS_NONCLAIM", "contract only"),
        ("CG1957_1_label_forgetting_conditional", "Source-label forgetting route is exact conditionally.", "PASS_NONCLAIM", "parent graph/current signatures missing"),
        ("CG1957_2_source_functor_signed", "Source-functor domain is parent-signed.", "FAIL_BLOCKED", "variation-before-readout/readout no-reentry missing"),
        ("CG1957_3_current_owner_signed", "Hilbert current owner is parent-signed.", "FAIL_BLOCKED", "Noether/Hilbert current owner stack missing"),
        ("CG1957_4_nonHilbert_silent", "Non-Hilbert current bypass is zero/silent.", "FAIL_BLOCKED", "J_NH zero/exact/bound missing"),
        ("CG1957_5_residual_bound", "Residual source current bound is numeric and source-backed.", "FAIL_BLOCKED", "residual current envelopes missing"),
        ("CG1957_6_Cassini_source_residual", "Source-side contribution to Cassini residual is zero/bounded.", "FAIL_BLOCKED", "source current and projection/readout factors missing"),
        ("CG1957_7_local_GR", "MTS derives local GR/Newton.", "FAIL_BLOCKED", "source side plus EH/R11/operator and measured-GM gates remain open"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1957_0_verdict",
            "SOURCE_MAP_ZERO_NOT_PROVED_BUT_FINITE_VECTOR_BUILT",
            "conditional label-forgetting is clean, but current owner/non-Hilbert/readout clauses remain unsigned",
            "do not loop on label forgetting; attack current-owner and non-Hilbert silence directly",
        ),
        (
            "DEC1957_1_best_next",
            "CURRENT_OWNER_AND_NONHILBERT_SILENCE",
            "these two clauses are the hard source-side blockers that can actually unlock DeltaT_source=0",
            "build 1958 current-owner/non-Hilbert silence proof attempt or emit first residual current envelopes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1957_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1958-Y5-R2FR-current-owner-nonHilbert-silence-or-current-bound.md",
            "target_script": "scripts/Y5_R2FR_current_owner_nonHilbert_silence_or_current_bound_1958.py",
            "objective": "prove Hilbert current ownership and non-Hilbert current silence, or emit residual current envelope rows",
            "acceptance_output": "current-owner proof clauses or numeric/sourced DeltaT_NH and DeltaT_readout bound rows",
            "nonclaim_rule": "no source-side/Cassini/local-GR claim unless residual currents are theorem-zero or source-backed below bound",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1957_0_project_position")
    row.update(
        {
            "strongest_result": "Ordinary matter source-map debt is now a finite residual-current vector: DeltaT_w, DeltaT_NH, DeltaT_readout.",
            "what_improved": "source-label forgetting is kept as a clean conditional theorem without pretending it kills non-Hilbert current bypass",
            "still_missing": "parent source-functor domain, parent-owned matter graph/current owner, non-Hilbert silence, readout no-reentry, and source-backed residual envelopes",
            "claim_status": "not a source-side/Cassini/local-GR pass; a narrower current-owner target",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_SOURCE_REGISTER.csv",
    "theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_SOURCE_MAP_THEOREM_ATTEMPT.csv",
    "residuals": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_RESIDUAL_CURRENT_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1957_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "SOURCE_MAP_SIGNATURE_1957_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1957_CURRENT_OWNER_NONHILBERT_SILENCE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1957_0_nonclaim_weight"),
            "artifact": "1957 source-map theorem attempt",
            "weight": "CONDITIONAL_THEOREM_AND_RESIDUAL_VECTOR_NOT_EVIDENCE",
            "reason": "source-side vector is sharper but not theorem-zero or numeric",
        }
    ]
    queue = [
        {
            **base("AQ1957_0_current_owner"),
            "target": "Hilbert current owner stack",
            "needed_inputs": "parent matter action variation; Noether/Hilbert current equality; no post-readout current rewrite",
            "priority": "HIGH",
        },
        {
            **base("AQ1957_1_nonHilbert_silence"),
            "target": "non-Hilbert current silence or bound",
            "needed_inputs": "spin/torsion/boundary current theorem; projected l=2 silence; residual envelope",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "theorem": theorem_rows(),
        "residuals": residual_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1957-", "*_1957_*", "*Y5*1957*", "*VAL1957*", "*P8*1957*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1957_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "SM1957_0_target" and row["status"] == "THEOREM_TARGET_EXACT" for row in tables["theorem"])
    rows.append(validation_row("VAL1957_01_target", "PASS" if target_ok else "FAIL", "source-map theorem target recorded"))

    conditional_ok = any(row["row_id"] == "SM1957_2_connected_matter_category" and row["status"] == "EXACT_CONDITIONAL_THEOREM_GRAPH_UNSIGNED" for row in tables["theorem"])
    rows.append(validation_row("VAL1957_02_conditional_theorem", "PASS" if conditional_ok else "FAIL", "conditional label-forgetting theorem retained"))

    blockers = {"SM1957_3_current_owner", "SM1957_4_nonHilbert_silence", "SM1957_5_readout_no_reentry"}
    blocker_ok = blockers.issubset({row["row_id"] for row in tables["theorem"] if row["status"] in {"CURRENT_OWNER_NOT_SIGNED", "OPEN_PARALLEL_GATE", "CONDITIONAL_NOT_PARENT_SIGNED"}})
    rows.append(validation_row("VAL1957_03_blockers", "PASS" if blocker_ok else "FAIL", "current/non-Hilbert/readout blockers retained"))

    residual_symbols = {"||DeltaT_source,l2||", "||DeltaT_w,l2||", "||DeltaT_NH,l2||", "||DeltaT_readout,l2||"}
    residual_ok = residual_symbols.issubset({row["symbol"] for row in tables["residuals"]})
    rows.append(validation_row("VAL1957_04_residual_vector", "PASS" if residual_ok else "FAIL", "residual current vector built"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONDITIONAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1957_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks live claims and keeps conditional route nonclaim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1957_0_theorem_target" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1957_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "CURRENT_OWNER_AND_NONHILBERT_SILENCE" for row in tables["decision"])
    rows.append(validation_row("VAL1957_07_decision", "PASS" if decision_ok else "FAIL", "current owner/non-Hilbert route selected"))

    next_ok = tables["next"][0]["target_doc"] == "1958-Y5-R2FR-current-owner-nonHilbert-silence-or-current-bound.md"
    rows.append(validation_row("VAL1957_08_next_target", "PASS" if next_ok else "FAIL", "1958 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1957_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1957_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1957_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1957_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1957_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1957_OVERALL", overall, "1957 source-map signature or residual current bound"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Source Map Theorem Attempt", tables["theorem"]),
        ("Residual Current Ledger", tables["residuals"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1957 Y5 R2FR: Source Map Signature Or Residual Current Bound",
        "",
        "Private checkpoint. This attacks the ordinary-matter source side of the local EH/GR bridge.",
        "",
        "Verdict: source-label forgetting remains a clean conditional theorem, but the full source-map theorem is not closed because current ownership, non-Hilbert current silence, and readout no-reentry are not parent-signed. The debt is now an explicit residual-current vector.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for name, path in OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1957_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
