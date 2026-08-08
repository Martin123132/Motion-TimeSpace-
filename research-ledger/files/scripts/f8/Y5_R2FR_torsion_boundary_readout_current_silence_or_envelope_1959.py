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

DOC_PATH = ROOT / "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1959_VALIDATION.csv"

SOURCES = {
    "1958_doc": {
        "path": ROOT / "1958-Y5-R2FR-current-owner-nonHilbert-silence-or-current-bound.md",
        "needles": ["OWN1958_3_spin_torsion_channel", "OWN1958_4_boundary_current_channel", "NEXT1958_0_primary"],
    },
    "1958_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1958_VALIDATION.csv",
        "needles": ["VAL1958_OVERALL", "PASS"],
    },
    "960_torsion": {
        "path": ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
        "needles": ["LC960_1_metric_formalism_route", "LC960_4_verdict", "REJECTED_P4_CONNECTION_PLACEHOLDER"],
    },
    "943_frame": {
        "path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["CFC943_4_connection_lock", "FRS943_6_nonHilbert_current_projection"],
    },
    "944_descent": {
        "path": ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
        "needles": ["QDG944_4_geometry_stack_descent", "FLB944_4_nonHilbert_current"],
    },
    "1008_boundary": {
        "path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["CDS1008_3_reference_guard", "PVA1008_5_EH_import_limit"],
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
                "purpose": "1959 torsion boundary readout current silence or envelope",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def silence_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SIL1959_0_target",
            "kill or bound every non-Hilbert bypass current feeding the source-side l=2 residual",
            "P_2[J_NH]=P_2[J_TQ]+P_2[J_boundary]+P_2[J_readout]+P_2[J_improvement]=0 or bounded",
            "TARGET_EXACT",
            "This is the source-side counterpart of the Cassini STF residual gate.",
            "all bypass channels must be zero or source-backed bounded",
        ),
        (
            "SIL1959_1_torsion_Levi_Civita_route",
            "spin/torsion/nonmetricity current is zero if the observed connection is Levi-Civita and ordinary matter uses that connection only",
            "Gamma_obs=Gamma_LC[g_obs], hypermomentum_extra=0 -> P_2[J_TQ]=0",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "960 gives the clean LC route but does not close it.",
            "need metric-only parent configuration or Palatini/no-hypermomentum proof",
        ),
        (
            "SIL1959_2_connection_residual_fallback",
            "if the connection is independent, torsion/nonmetricity must be retained as explicit P4/R11 residual current rows",
            "P_2[J_TQ] <= envelope(c_T,c_Q,spin/source maps)",
            "FALLBACK_SCHEMA_PLACEHOLDER_ONLY",
            "P4 connection rows exist as placeholders but are not scoreable.",
            "need coefficients, units, weak-field maps, and source paths",
        ),
        (
            "SIL1959_3_boundary_current_route",
            "boundary/source-worldtube current is zero only if parent boundary flux and improvement flux are fixed before readout and l=2 silent",
            "P_2[J_boundary]+P_2[J_improvement]=0 if Omega_boundary_extra|l=2=0 and counterterm is fixed-before-readout",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "1008 gives a reference guard, not a boundary-current proof.",
            "need parent theta/Q/boundary term or boundary current envelope",
        ),
        (
            "SIL1959_4_readout_reentry_route",
            "readout/domain/frame maps must descend from q(Phi) with no source-label or connection marker re-entry",
            "J_readout=0 if mu,e,g,omega,D are functions of q(Phi) or owned gauge/exact data",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "943/944 identify the route and the non-Hilbert leak channel.",
            "need geometry-stack descent proof through connection/readout order",
        ),
        (
            "SIL1959_5_combined_zero_condition",
            "the source-side non-Hilbert zero theorem requires LC/no-hypermomentum, boundary flux silence, and readout no-reentry together",
            "P_2[J_NH]=0 iff J_TQ=J_boundary=J_readout=J_improvement=0 in the observed branch",
            "ZERO_CONDITION_SHARPENED_NOT_SIGNED",
            "The theorem shape is now exact but not closed.",
            "sign all clauses or use current-envelope fallback",
        ),
        (
            "SIL1959_6_verdict",
            "non-Hilbert bypass silence is not closed at 1959",
            "blocked by unsigned LC/no-hypermomentum, boundary flux, and readout no-reentry clauses",
            "ZERO_PROOF_FAILED_CLEANLY",
            "Not a dead end; the bypass branch is finite and testable as envelopes if derivation fails.",
            "next target: first source-backed envelopes or parent LC/boundary/readout signature",
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


def envelope_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ENV1959_0_combined_nonHilbert",
            "||P_2[J_NH]||",
            "||J_TQ,l2|| + ||J_boundary,l2|| + ||J_readout,l2|| + ||J_improvement,l2||",
            "MISSING_FACTORS",
            "source-current units",
            "combined bypass envelope is assembled but not scoreable",
        ),
        (
            "ENV1959_1_torsion_nonmetricity",
            "||J_TQ,l2||",
            "torsion/nonmetricity/spin-current l=2 envelope",
            "MISSING_COEFFICIENTS_AND_MAPS",
            "source-current units",
            "need LC theorem or P4 connection coefficients/source maps",
        ),
        (
            "ENV1959_2_boundary_current",
            "||J_boundary,l2||",
            "boundary/source-worldtube current l=2 envelope",
            "MISSING_BOUNDARY_CURRENT_SOURCE",
            "source-current units",
            "need parent boundary term or source-worldtube current bound",
        ),
        (
            "ENV1959_3_readout_reentry",
            "||J_readout,l2||",
            "readout/domain/frame marker current re-entry envelope",
            "MISSING_READOUT_MARKER_BOUND",
            "source-current units",
            "need no-reentry theorem or marker/domain residual bound",
        ),
        (
            "ENV1959_4_improvement_flux",
            "||J_improvement,l2||",
            "canonical-Hilbert improvement boundary l=2 flux",
            "MISSING_IMPROVEMENT_FLUX_BOUND",
            "source-current units",
            "need fixed counterterm/boundary convention plus l=2 flux envelope",
        ),
        (
            "ENV1959_5_projection_readout",
            "K_2 W_STF",
            "projection from bypass current envelope to Cassini-visible residual STF slip",
            "MISSING_KERNEL_AND_READOUT_NORMS",
            "dimensionless per source-current unit",
            "needed after current envelopes exist",
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
            "RUN1959_0_zero_theorem",
            "LC/no-hypermomentum + boundary flux silence + readout no-reentry -> P_2[J_NH]=0",
            "source-side non-Hilbert residual zero",
            "MISSING_LC_PARENT_SIGNATURE;MISSING_BOUNDARY_FLUX_ZERO;MISSING_READOUT_NO_REENTRY",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "no source-side/local-GR claim",
        ),
        (
            "RUN1959_1_LC_partial",
            "Levi-Civita route would kill torsion/nonmetricity current",
            "conditional only",
            "MISSING_METRIC_ONLY_OR_NO_HYPERMOMENTUM_PROOF",
            "PASS_NONCLAIM_CONDITIONAL_ROUTE",
            "useful but not sufficient",
        ),
        (
            "RUN1959_2_envelope_bound",
            "||P_2[J_NH]|| <= combined bypass current envelope",
            "projected S_TF_extra <= 6.7e-5 after K_2/W_STF",
            "MISSING_CURRENT_ENVELOPES;MISSING_PROJECTION_NORMS",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback remains unavailable",
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
        ("CG1959_0_target", "Non-Hilbert bypass current target exists.", "PASS_NONCLAIM", "contract only"),
        ("CG1959_1_LC_route", "LC/no-hypermomentum route identified.", "PASS_NONCLAIM", "conditional, not signed"),
        ("CG1959_2_torsion_silent", "Torsion/nonmetricity current is zero.", "FAIL_BLOCKED", "LC/no-hypermomentum proof missing"),
        ("CG1959_3_boundary_current_silent", "Boundary/improvement current l=2 flux is zero.", "FAIL_BLOCKED", "boundary flux proof missing"),
        ("CG1959_4_readout_reentry_silent", "Readout/domain/frame current re-entry is zero.", "FAIL_BLOCKED", "geometry-stack descent/readout no-reentry unsigned"),
        ("CG1959_5_current_envelopes", "Bypass current envelopes are numeric/source-backed.", "FAIL_BLOCKED", "envelope factors missing"),
        ("CG1959_6_source_side_pass", "Source-side non-Hilbert residual is zero/bounded.", "FAIL_BLOCKED", "zero theorem and envelopes missing"),
        ("CG1959_7_local_GR", "MTS derives local GR/Newton.", "FAIL_BLOCKED", "source, EH/R11, measured-GM, PPN gates remain open"),
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
            "DEC1959_0_verdict",
            "BYPASS_ZERO_NOT_PROVED_ENVELOPE_ROUTE_EXPLICIT",
            "torsion, boundary, and readout channels are all conditionally clean but unsigned",
            "do not promote source-side GR; either sign LC/boundary/readout or fill envelopes",
        ),
        (
            "DEC1959_1_best_next",
            "LEVI_CIVITA_NO_HYPERMOMENTUM_FIRST",
            "torsion/nonmetricity is the most upstream bypass because it feeds matter connection, spin current, and non-Hilbert source projection",
            "attempt parent LC/no-hypermomentum proof before external current-envelope acquisition",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1959_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md",
            "target_script": "scripts/Y5_R2FR_Levi_Civita_no_hypermomentum_proof_or_P4_current_envelope_1960.py",
            "objective": "prove observed connection is Levi-Civita/no-hypermomentum for ordinary matter, or fill P4 torsion/nonmetricity current envelope rows",
            "acceptance_output": "parent LC/no-hypermomentum clauses or source-backed P4 current envelopes",
            "nonclaim_rule": "no source-side/local-GR claim unless torsion/nonmetricity current is zero or bounded",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1959_0_project_position")
    row.update(
        {
            "strongest_result": "Non-Hilbert bypass debt is finite: torsion/nonmetricity, boundary/improvement flux, readout re-entry, and projection/readout norms.",
            "what_improved": "the local-GR source-side branch now has a concrete LC/no-hypermomentum upstream target",
            "still_missing": "parent LC/no-hypermomentum proof, boundary flux silence, readout no-reentry, current envelopes, K2/W_STF projection norms",
            "claim_status": "not a source-side/Cassini/local-GR pass; a sharper bypass-current gate",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_SOURCE_REGISTER.csv",
    "silence": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_BYPASS_CURRENT_SILENCE_ATTEMPT.csv",
    "envelopes": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_BYPASS_CURRENT_ENVELOPE_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1959_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "BYPASS_CURRENT_1959_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1959_LEVI_CIVITA_NO_HYPERMOMENTUM_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1959_0_nonclaim_weight"),
            "artifact": "1959 bypass current silence/envelope gate",
            "weight": "CONDITIONAL_GATE_NOT_EVIDENCE",
            "reason": "bypass channels are explicit but not zero or numeric",
        }
    ]
    queue = [
        {
            **base("AQ1959_0_LC_no_hypermomentum"),
            "target": "Levi-Civita/no-hypermomentum proof",
            "needed_inputs": "metric-only parent configuration or Palatini equation; no independent matter hypermomentum; observed connection descent",
            "priority": "HIGH",
        },
        {
            **base("AQ1959_1_P4_current_envelopes"),
            "target": "P4 torsion/nonmetricity current envelopes",
            "needed_inputs": "connection coefficients, units, weak-field/source maps, spin/source projections",
            "priority": "FALLBACK_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "silence": silence_rows(),
        "envelopes": envelope_rows(),
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
    patterns = ("1959-", "*_1959_*", "*Y5*1959*", "*VAL1959*", "*P8*1959*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1959_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "SIL1959_0_target" and row["status"] == "TARGET_EXACT" for row in tables["silence"])
    rows.append(validation_row("VAL1959_01_target", "PASS" if target_ok else "FAIL", "bypass current target recorded"))

    lc_ok = any(row["row_id"] == "SIL1959_1_torsion_Levi_Civita_route" and row["status"] == "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED" for row in tables["silence"])
    rows.append(validation_row("VAL1959_02_LC_route", "PASS" if lc_ok else "FAIL", "LC/no-hypermomentum route recorded as conditional"))

    channels = {"SIL1959_1_torsion_Levi_Civita_route", "SIL1959_3_boundary_current_route", "SIL1959_4_readout_reentry_route"}
    channels_ok = channels.issubset({row["row_id"] for row in tables["silence"]})
    rows.append(validation_row("VAL1959_03_channels", "PASS" if channels_ok else "FAIL", "torsion boundary readout channels recorded"))

    envelopes_ok = any(row["row_id"] == "ENV1959_0_combined_nonHilbert" and row["status"] == "MISSING_FACTORS" for row in tables["envelopes"])
    rows.append(validation_row("VAL1959_04_envelopes", "PASS" if envelopes_ok else "FAIL", "combined bypass envelope recorded but blocked"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONDITIONAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1959_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim branches"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1959_0_target" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1959_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "LEVI_CIVITA_NO_HYPERMOMENTUM_FIRST" for row in tables["decision"])
    rows.append(validation_row("VAL1959_07_decision", "PASS" if decision_ok else "FAIL", "LC/no-hypermomentum selected"))

    next_ok = tables["next"][0]["target_doc"] == "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md"
    rows.append(validation_row("VAL1959_08_next_target", "PASS" if next_ok else "FAIL", "1960 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1959_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1959_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1959_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1959_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1959_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1959_OVERALL", overall, "1959 torsion boundary readout current silence or envelope"))
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
        ("Bypass Current Silence Attempt", tables["silence"]),
        ("Bypass Current Envelope Ledger", tables["envelopes"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1959 Y5 R2FR: Torsion Boundary Readout Current Silence Or Envelope",
        "",
        "Private checkpoint. This attacks the non-Hilbert bypass current channels feeding the source-side local-GR residual.",
        "",
        "Verdict: the bypass-current zero theorem is not closed. The Levi-Civita/no-hypermomentum, boundary-flux, and readout no-reentry routes are clean but unsigned; the fallback envelope route is explicit but missing numeric/source-backed factors.",
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
    print(f"VAL1959_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
