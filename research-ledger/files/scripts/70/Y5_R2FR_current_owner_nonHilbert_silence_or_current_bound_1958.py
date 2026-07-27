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

DOC_PATH = ROOT / "1958-Y5-R2FR-current-owner-nonHilbert-silence-or-current-bound.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1958_VALIDATION.csv"

SOURCES = {
    "1957_doc": {
        "path": ROOT / "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md",
        "needles": ["SM1957_3_current_owner", "SM1957_4_nonHilbert_silence", "NEXT1957_0_primary"],
    },
    "1957_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1957_VALIDATION.csv",
        "needles": ["VAL1957_OVERALL", "PASS"],
    },
    "1476_source_label": {
        "path": ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
        "needles": ["SLP1476_3_current_owner", "SLP1476_4_nonHilbert_silence"],
    },
    "1008_variation": {
        "path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["PVA1008_0_parent_action", "PVA1008_1_theta_MTS", "PVA1008_5_EH_import_limit"],
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
                "purpose": "1958 current owner nonHilbert silence or current bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def owner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "OWN1958_0_target",
            "current-owner theorem target",
            "J_active = J_Hilbert[S_matter,e_obs] and P_2[J_NH]=0",
            "THEOREM_TARGET_EXACT",
            "This would close the hardest source-side residual current branch.",
            "needs parent matter variation and non-Hilbert silence",
        ),
        (
            "OWN1958_1_matter_variation_owner",
            "all ordinary active source currents arise by varying the same matter action with respect to the observed coframe/metric",
            "delta S_matter = 1/2 int sqrt(-g) T_H^{mu nu} delta g_mu nu + matter EOM",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "If signed, the active source is Hilbert by construction.",
            "parent matter action and observed coframe map must be explicit",
        ),
        (
            "OWN1958_2_canonical_to_Hilbert_improvement",
            "canonical/Noether stress differences are improvement terms and do not create independent source charge when boundary flux is zero",
            "T_can - T_H = nabla_lambda B^{lambda mu nu}; P_2 boundary flux must vanish or be bounded",
            "CONDITIONAL_IMPROVEMENT_NOT_BOUNDARY_SIGNED",
            "This handles ordinary field-theory current ambiguity without pretending boundary terms vanish.",
            "boundary/improvement l=2 flux needs zero theorem or envelope",
        ),
        (
            "OWN1958_3_spin_torsion_channel",
            "spin/torsion currents are not silent unless the parent local geometry is torsionless/Levi-Civita or their projection is exact/bounded",
            "J_NH,spin -> 0 only if torsion/nonmetricity independent source channel is absent or constrained",
            "OPEN_NONHILBERT_CHANNEL",
            "This is the dangerous non-Hilbert bypass.",
            "prove torsion/nonmetricity absence or retain spin-current envelope",
        ),
        (
            "OWN1958_4_boundary_current_channel",
            "boundary/source-worldtube current terms can carry l=2 unless parent boundary flux is zero or source-bounded",
            "P_2[J_NH,boundary]=0 or ||P_2[J_NH,boundary]|| sourced",
            "OPEN_BOUNDARY_CURRENT_CHANNEL",
            "This links source-side debt to the boundary flux debt from 1956.",
            "extract parent boundary current or bound it",
        ),
        (
            "OWN1958_5_readout_current_reentry",
            "readout/domain/frame maps must not rewrite Hilbert current after variation into a source-labelled current",
            "J_readout_reentry=0 if q/readout has no species/domain marker source slot",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "This protects the theorem from post-variation smuggling.",
            "parent readout no-reentry proof or retained marker current",
        ),
        (
            "OWN1958_6_verdict",
            "current-owner/non-Hilbert silence is not closed at 1958",
            "J_active=J_Hilbert remains blocked by parent matter variation, spin/torsion silence, boundary current, and readout no-reentry",
            "ZERO_PROOF_FAILED_CLEANLY",
            "The source-side obstruction is now down to three physical current channels, not a vague coupling worry.",
            "derive torsion/boundary/readout silence or emit residual current envelopes",
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


def bound_rows() -> list[dict[str, object]]:
    entries = [
        (
            "NB1958_0_nonHilbert_bound",
            "||P_2[J_NH]||",
            "||J_spin/torsion,l2|| + ||J_boundary,l2|| + ||J_readout,l2|| + ||J_improvement_flux,l2||",
            "MISSING_FACTORS",
            "source-current units",
            "combined non-Hilbert current bound not scoreable",
        ),
        (
            "NB1958_1_spin_torsion",
            "||J_spin/torsion,l2||",
            "spin/torsion/nonmetricity source-current l=2 envelope",
            "MISSING_ZERO_OR_ENVELOPE",
            "source-current units",
            "prove torsionless/Levi-Civita source silence or source envelope",
        ),
        (
            "NB1958_2_boundary_current",
            "||J_boundary,l2||",
            "boundary/source-worldtube current l=2 envelope",
            "MISSING_ZERO_OR_ENVELOPE",
            "source-current units",
            "prove boundary flux zero or source envelope",
        ),
        (
            "NB1958_3_readout_reentry",
            "||J_readout,l2||",
            "post-variation readout/domain/frame current reentry envelope",
            "MISSING_ZERO_OR_ENVELOPE",
            "source-current units",
            "prove no-reentry or source marker envelope",
        ),
        (
            "NB1958_4_improvement_flux",
            "||J_improvement_flux,l2||",
            "canonical-to-Hilbert improvement boundary flux envelope",
            "MISSING_ZERO_OR_ENVELOPE",
            "source-current units",
            "prove improvement flux silence or source envelope",
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
            "RUN1958_0_current_owner_zero",
            "matter variation owner + improvement flux zero + non-Hilbert/readout silence -> P_2[J_NH]=0",
            "DeltaT_NH=0",
            "MISSING_PARENT_MATTER_VARIATION;MISSING_SPIN_TORSION_SILENCE;MISSING_BOUNDARY_CURRENT_SILENCE;MISSING_READOUT_NO_REENTRY",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "cannot close source-side current residual",
        ),
        (
            "RUN1958_1_improvement_only",
            "canonical-Hilbert difference is a boundary improvement",
            "not enough without boundary l=2 flux zero",
            "MISSING_IMPROVEMENT_BOUNDARY_FLUX",
            "PASS_NONCLAIM_CONDITIONAL_ROUTE",
            "keeps a useful theorem but blocks promotion",
        ),
        (
            "RUN1958_2_current_bound",
            "||P_2[J_NH]|| <= sum non-Hilbert current envelopes",
            "projected S_TF_extra <= 6.7e-5 after K_2/W_STF",
            "MISSING_CURRENT_ENVELOPES;MISSING_KERNEL_NORM;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback current-bound route not scoreable",
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
        ("CG1958_0_target", "Current-owner/non-Hilbert theorem target exists.", "PASS_NONCLAIM", "contract only"),
        ("CG1958_1_improvement_route", "Canonical-Hilbert ambiguity is classified as improvement/boundary flux.", "PASS_NONCLAIM", "boundary flux still open"),
        ("CG1958_2_matter_variation_owner", "Parent matter variation owner is signed.", "FAIL_BLOCKED", "explicit parent matter variation missing"),
        ("CG1958_3_spin_torsion_silent", "Spin/torsion/nonmetricity non-Hilbert current is silent.", "FAIL_BLOCKED", "torsion/connection source channel unresolved"),
        ("CG1958_4_boundary_current_silent", "Boundary current l=2 flux is silent.", "FAIL_BLOCKED", "boundary current zero theorem/envelope missing"),
        ("CG1958_5_readout_no_reentry", "Readout current re-entry is forbidden.", "FAIL_BLOCKED", "readout no-reentry theorem missing"),
        ("CG1958_6_source_side_pass", "Source-side residual current is zero/bounded.", "FAIL_BLOCKED", "zero theorem and current envelopes missing"),
        ("CG1958_7_local_GR", "MTS derives local GR/Newton.", "FAIL_BLOCKED", "source, EH/R11, measured-GM, and PPN gates remain open"),
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
            "DEC1958_0_verdict",
            "CURRENT_OWNER_ZERO_NOT_PROVED_CHANNELS_IDENTIFIED",
            "ordinary current ambiguity is reduced to improvement flux, spin/torsion, boundary current, and readout re-entry",
            "do not loop on source labels; attack geometry/connection/boundary current clauses",
        ),
        (
            "DEC1958_1_best_next",
            "TORSION_BOUNDARY_READOUT_CURRENT_TRIAGE",
            "the matter variation theorem can only close after these non-Hilbert bypass channels are killed or bounded",
            "build 1959 torsion-boundary-readout current silence gate or emit first non-Hilbert current envelopes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1958_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md",
            "target_script": "scripts/Y5_R2FR_torsion_boundary_readout_current_silence_or_envelope_1959.py",
            "objective": "prove or bound the non-Hilbert bypass channels: spin/torsion, boundary current, and readout re-entry",
            "acceptance_output": "zero clauses or source-backed envelope rows for each bypass current",
            "nonclaim_rule": "no source-side/local-GR claim until every bypass current is zero or bounded",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1958_0_project_position")
    row.update(
        {
            "strongest_result": "Current-owner debt is now reduced to explicit bypass channels: spin/torsion, boundary current, readout re-entry, and improvement flux.",
            "what_improved": "the source-side GR bridge no longer treats non-Hilbert currents as a vague maybe",
            "still_missing": "parent matter variation owner, torsion/connection silence, boundary-current silence, readout no-reentry, and current envelopes",
            "claim_status": "not a source-side/Cassini/local-GR pass; a current-channel triage",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_SOURCE_REGISTER.csv",
    "owner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
    "bounds": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_NONHILBERT_CURRENT_BOUND_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1958_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "CURRENT_OWNER_NONHILBERT_1958_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1958_TORSION_BOUNDARY_READOUT_CURRENT_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1958_0_nonclaim_weight"),
            "artifact": "1958 current-owner/non-Hilbert silence attempt",
            "weight": "CHANNEL_TRIAGE_NOT_EVIDENCE",
            "reason": "bypass channels are classified but not zero or numeric",
        }
    ]
    queue = [
        {
            **base("AQ1958_0_torsion_connection"),
            "target": "spin/torsion/nonmetricity current silence",
            "needed_inputs": "parent connection choice; torsion/nonmetricity constraints; spin-current projection",
            "priority": "HIGH",
        },
        {
            **base("AQ1958_1_boundary_readout"),
            "target": "boundary current and readout re-entry silence",
            "needed_inputs": "boundary current term; improvement flux; readout/domain marker theorem",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "owner": owner_rows(),
        "bounds": bound_rows(),
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
    patterns = ("1958-", "*_1958_*", "*Y5*1958*", "*VAL1958*", "*P8*1958*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1958_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "OWN1958_0_target" and row["status"] == "THEOREM_TARGET_EXACT" for row in tables["owner"])
    rows.append(validation_row("VAL1958_01_target", "PASS" if target_ok else "FAIL", "current-owner theorem target recorded"))

    improvement_ok = any(row["row_id"] == "OWN1958_2_canonical_to_Hilbert_improvement" and row["status"] == "CONDITIONAL_IMPROVEMENT_NOT_BOUNDARY_SIGNED" for row in tables["owner"])
    rows.append(validation_row("VAL1958_02_improvement", "PASS" if improvement_ok else "FAIL", "canonical-Hilbert improvement handled conditionally"))

    channels = {"OWN1958_3_spin_torsion_channel", "OWN1958_4_boundary_current_channel", "OWN1958_5_readout_current_reentry"}
    channels_ok = channels.issubset({row["row_id"] for row in tables["owner"]})
    rows.append(validation_row("VAL1958_03_channels", "PASS" if channels_ok else "FAIL", "non-Hilbert bypass channels identified"))

    bounds_ok = any(row["row_id"] == "NB1958_0_nonHilbert_bound" and row["status"] == "MISSING_FACTORS" for row in tables["bounds"])
    rows.append(validation_row("VAL1958_04_bounds", "PASS" if bounds_ok else "FAIL", "non-Hilbert bound formula recorded but blocked"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONDITIONAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1958_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim branches"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1958_0_target" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1958_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "TORSION_BOUNDARY_READOUT_CURRENT_TRIAGE" for row in tables["decision"])
    rows.append(validation_row("VAL1958_07_decision", "PASS" if decision_ok else "FAIL", "torsion/boundary/readout route selected"))

    next_ok = tables["next"][0]["target_doc"] == "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md"
    rows.append(validation_row("VAL1958_08_next_target", "PASS" if next_ok else "FAIL", "1959 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1958_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1958_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1958_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1958_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1958_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1958_OVERALL", overall, "1958 current owner nonHilbert silence or current bound"))
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
        ("Current Owner Non-Hilbert Attempt", tables["owner"]),
        ("Non-Hilbert Current Bound Ledger", tables["bounds"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1958 Y5 R2FR: Current Owner Non-Hilbert Silence Or Current Bound",
        "",
        "Private checkpoint. This attacks the current-owner and non-Hilbert bypass branch in the source-side GR reduction.",
        "",
        "Verdict: current ownership is not closed. The bypass channels are now explicit: spin/torsion/nonmetricity, boundary current, readout re-entry, and improvement flux. No source-side, Cassini, Newton, or local-GR claim is made.",
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
    print(f"VAL1958_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
