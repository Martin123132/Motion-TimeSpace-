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

DOC_PATH = ROOT / "1961-Y5-R2FR-parent-metric-only-variable-signature-or-P4-fill.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1961_VALIDATION.csv"

SOURCES = {
    "1960_doc": {
        "path": ROOT / "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md",
        "needles": ["LC1960_1_metric_only_parent_route", "P4C1960_5_hypermomentum", "NEXT1960_0_primary"],
    },
    "1960_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1960_VALIDATION.csv",
        "needles": ["VAL1960_OVERALL", "PASS"],
    },
    "785_stack": {
        "path": ROOT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
        "needles": ["PMC785_5_matter_metric_only_coupling", "PMC785_6_parent_action_metric_ownership", "BGL785_2_connection_trigger"],
    },
    "786_parent_action": {
        "path": ROOT / "786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md",
        "needles": ["PAO786_0_composite_metric_action", "PAO786_3_multifield_pregeometry", "VRG786_5_verdict"],
    },
    "943_coframe": {
        "path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["CFC943_2_matter_functor", "CFC943_4_connection_lock", "DER943_3_one_Hilbert_current"],
    },
    "944_descent": {
        "path": ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
        "needles": ["QDG944_0_parent_q_map", "QDG944_4_geometry_stack_descent", "QDG944_7_total"],
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
                "purpose": "1961 parent metric-only variable signature or P4 fill",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def signature_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MVS1961_0_target",
            "parent action has no independent observed-branch connection variable and ordinary matter sees only the descended metric/coframe stack",
            "Phi_parent -> q(Phi) -> (g_obs,e_obs,omega[e_obs]); no independent Gamma_obs in S_matter/source/readout",
            "TARGET_EXACT",
            "This is the cleanest LC/no-hypermomentum win.",
            "parent variable list, q map, and matter functor must be signed",
        ),
        (
            "MVS1961_1_parent_variable_list",
            "observed branch variable list contains g/e or pregeometry that induces g/e, but no independent Gamma/omega field",
            "Vars_obs={Phi_pregeom or g/e, Psi_matter, gauge}; Gamma_obs:=Gamma_LC[g_obs]",
            "NOT_PARENT_SIGNED",
            "Current corpus has conditional stack rows, not an action-owned variable list.",
            "need parent action/object language declaration",
        ),
        (
            "MVS1961_2_metric_ownership_rank",
            "metric map must be action-owned and have enough rank to support EH-like variations",
            "g_obs=G[Phi]; rank(delta G/delta Phi) must cover local metric variations or declare independent metric branch",
            "BLOCKED_BY_RANK_AND_COVARIANCE",
            "786 blocks scalar-only metric ownership and points to multifield/independent metric branch.",
            "need rank gate or explicit independent metric/coframe field",
        ),
        (
            "MVS1961_3_quotient_geometry_stack",
            "measure, metric/coframe, connection, and derivative operator descend through q(Phi)",
            "mu,e,g,omega,D = functions of q(Phi) or owned gauge/exact data",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "944 has the exact descent proof shape but does not parent-sign q or geometry stack.",
            "need q map and observed coframe functor ownership",
        ),
        (
            "MVS1961_4_matter_blindness",
            "ordinary matter action depends only on e_obs, omega[e_obs], owned gauge fields, and constants",
            "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "943/785 give the right contract; direct psi/Gamma/q_loc dependencies remain legal until excluded.",
            "need parent-signed matter functor and no-spurion/no-marker audit",
        ),
        (
            "MVS1961_5_no_Gamma_readout_reentry",
            "source/readout/worldtube maps do not reintroduce independent Gamma/connection markers after variation",
            "delta S/delta Gamma_obs=0 and q/readout has no Gamma/source marker slot",
            "UNSIGNED_REENTRY_BLOCKER",
            "This is the hypermomentum/readout side of the same theorem.",
            "need no-Gamma matter/source/readout proof",
        ),
        (
            "MVS1961_6_metric_only_verdict",
            "metric-only/no-independent-connection signature is not closed at 1961",
            "blocked by parent variable list, metric ownership rank, q-stack descent, matter blindness, and no-Gamma readout",
            "ZERO_PROOF_FAILED_CLEANLY",
            "The clean route remains viable but unsigned; P4 fallback must stay alive.",
            "either declare/sign parent metric-only branch or fill P4 rows",
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


def p4_fill_rows() -> list[dict[str, object]]:
    entries = [
        (
            "P4F1961_0_fill_contract",
            "P4 connection residual rows become mandatory if metric-only signature is not signed",
            "every P4 row needs coefficient, units, weak-field map, source path, and assumptions",
            "FALLBACK_CONTRACT_ACTIVE",
            "This prevents an unsigned metric-only assumption from hiding connection forces.",
        ),
        (
            "P4F1961_1_first_priority",
            "independent_connection_hypermomentum",
            "Delta_lambda^{mu nu} source/readout connection charge",
            "MISSING_NO_GAMMA_PROOF_OR_BOUND",
            "highest priority because it directly blocks LC/no-hypermomentum",
        ),
        (
            "P4F1961_2_second_priority",
            "axial_torsion_spin_coupling",
            "spin/axial torsion current",
            "MISSING_SPIN_TORSION_MAP",
            "spinor matter is the obvious escape route",
        ),
        (
            "P4F1961_3_third_priority",
            "nonmetricity_shear_lightcone",
            "trace-free nonmetricity lightcone/clock residual",
            "MISSING_LIGHTCONE_CLOCK_MAP",
            "metric lightcone cannot be assumed if this survives",
        ),
        (
            "P4F1961_4_remaining",
            "combined/projective/Weyl nonmetricity rows",
            "torsion_nonmetricity_combined; torsion_trace_projective_mode; nonmetricity_weyl_trace",
            "MISSING_COEFFICIENTS_AND_MAPS",
            "must be filled if theorem route fails",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, channel, definition, status, next_action in entries:
        row = base(row_id)
        row.update(
            {
                "channel": channel,
                "definition": definition,
                "status": status,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1961_0_metric_only_zero",
            "parent metric-only variable signature + matter blindness + no-Gamma readout -> Gamma=Gamma_LC",
            "P4 connection residual zero",
            "MISSING_PARENT_VARIABLE_LIST;MISSING_METRIC_RANK_GATE;MISSING_Q_STACK_DESCENT;MISSING_MATTER_BLINDNESS;MISSING_NO_GAMMA_READOUT",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "no LC/local-GR claim",
        ),
        (
            "RUN1961_1_conditional_stack",
            "if g_obs/e_obs are owned and smooth Lorentzian, coframe and LC stack are standard",
            "conditional route",
            "MISSING_PARENT_OWNERSHIP",
            "PASS_NONCLAIM_CONDITIONAL_ROUTE",
            "mathematical foothold retained",
        ),
        (
            "RUN1961_2_P4_fill",
            "if metric-only proof fails, P4 residual rows must be filled",
            "source-side/local residual bound possible after P4 coefficients/maps",
            "MISSING_P4_COEFFICIENTS_UNITS_MAPS",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback remains non-scoreable",
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
        ("CG1961_0_target", "Metric-only variable-signature target exists.", "PASS_NONCLAIM", "contract only"),
        ("CG1961_1_conditional_stack", "Metric/coframe/LC stack is mathematically available if owned.", "PASS_NONCLAIM", "parent ownership missing"),
        ("CG1961_2_metric_only_signed", "Parent action has no independent observed-branch connection.", "FAIL_BLOCKED", "variable list not parent-signed"),
        ("CG1961_3_metric_ownership", "Observed metric/coframe map is action-owned and rank-sufficient.", "FAIL_BLOCKED", "rank/covariance gate open"),
        ("CG1961_4_matter_blindness", "Ordinary matter sees only e_obs/omega[e_obs].", "FAIL_BLOCKED", "matter functor not parent-signed"),
        ("CG1961_5_no_Gamma_reentry", "Matter/source/readout have no independent Gamma charge.", "FAIL_BLOCKED", "no-Gamma readout proof missing"),
        ("CG1961_6_P4_bound", "P4 connection rows are numeric/source-backed.", "FAIL_BLOCKED", "P4 rows remain missing coefficients/maps"),
        ("CG1961_7_local_GR", "MTS derives local GR/Newton.", "FAIL_BLOCKED", "connection, EH/R11, source mass, and PPN gates remain open"),
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
            "DEC1961_0_verdict",
            "METRIC_ONLY_SIGNATURE_NOT_SIGNED_P4_ACTIVE",
            "the clean LC route remains the best theorem path, but the corpus does not yet parent-sign the variable list or matter blindness",
            "do not claim LC; attack parent q/metric/matter ownership or start P4 fill",
        ),
        (
            "DEC1961_1_best_next",
            "PARENT_Q_METRIC_MATTER_OWNERSHIP_GATE",
            "this single gate can sign metric-only LC, source-map Hilbert current, and readout no-reentry together",
            "attempt a unified q -> g/e -> S_matter ownership signature before P4 numerical fallback",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1961_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md",
            "target_script": "scripts/Y5_R2FR_parent_q_metric_matter_ownership_or_P4_fallback_1962.py",
            "objective": "prove q->g/e->matter ownership and no-Gamma reentry, or begin P4 residual fill with hypermomentum first",
            "acceptance_output": "signed ownership clauses, or first P4 hypermomentum/source-map residual envelope rows",
            "nonclaim_rule": "no LC/source-side/local-GR claim unless ownership stack is signed or P4 residual bounds are live",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1961_0_project_position")
    row.update(
        {
            "strongest_result": "Metric-only LC is a clean route but remains unsigned; the necessary ownership stack is q->g/e->omega[e]->S_matter with no Gamma reentry.",
            "what_improved": "the connection problem is now tied to the same parent ownership gate as source-map and readout-frame closure",
            "still_missing": "parent variable list, metric rank/covariance, quotient geometry stack, matter blindness, no-Gamma readout, or P4 coefficients/maps",
            "claim_status": "not an LC/source-side/local-GR pass; a parent ownership gate",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_SOURCE_REGISTER.csv",
    "signature": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_METRIC_ONLY_SIGNATURE_ATTEMPT.csv",
    "p4": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_P4_FILL_PRIORITY_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1961_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "METRIC_ONLY_SIGNATURE_1961_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1961_PARENT_Q_METRIC_MATTER_OWNERSHIP_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1961_0_nonclaim_weight"),
            "artifact": "1961 metric-only variable signature gate",
            "weight": "OWNERSHIP_GATE_NOT_EVIDENCE",
            "reason": "metric-only route is exact but parent ownership remains unsigned",
        }
    ]
    queue = [
        {
            **base("AQ1961_0_q_metric_matter"),
            "target": "q->g/e->matter ownership stack",
            "needed_inputs": "parent q map, observed metric/coframe functor, rank gate, matter functor, no-Gamma readout",
            "priority": "HIGH",
        },
        {
            **base("AQ1961_1_p4_hypermomentum"),
            "target": "P4 hypermomentum fallback",
            "needed_inputs": "coefficient, units, source/readout Gamma map, weak-field residual projection",
            "priority": "FALLBACK_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "signature": signature_rows(),
        "p4": p4_fill_rows(),
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
    patterns = ("1961-", "*_1961_*", "*Y5*1961*", "*VAL1961*", "*P8*1961*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1961_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "MVS1961_0_target" and row["status"] == "TARGET_EXACT" for row in tables["signature"])
    rows.append(validation_row("VAL1961_01_target", "PASS" if target_ok else "FAIL", "metric-only signature target recorded"))

    rank_ok = any(row["row_id"] == "MVS1961_2_metric_ownership_rank" and row["status"] == "BLOCKED_BY_RANK_AND_COVARIANCE" for row in tables["signature"])
    rows.append(validation_row("VAL1961_02_rank_gate", "PASS" if rank_ok else "FAIL", "metric ownership rank blocker retained"))

    matter_ok = any(row["row_id"] == "MVS1961_4_matter_blindness" and row["status"] == "CONDITIONAL_NOT_PARENT_SIGNED" for row in tables["signature"])
    rows.append(validation_row("VAL1961_03_matter_blindness", "PASS" if matter_ok else "FAIL", "matter blindness condition retained"))

    p4_ok = any(row["row_id"] == "P4F1961_1_first_priority" and row["channel"] == "independent_connection_hypermomentum" for row in tables["p4"])
    rows.append(validation_row("VAL1961_04_p4_fallback", "PASS" if p4_ok else "FAIL", "P4 hypermomentum fallback prioritized"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONDITIONAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1961_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claims and preserves conditional stack"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1961_0_target" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1961_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "PARENT_Q_METRIC_MATTER_OWNERSHIP_GATE" for row in tables["decision"])
    rows.append(validation_row("VAL1961_07_decision", "PASS" if decision_ok else "FAIL", "parent q metric matter ownership selected"))

    next_ok = tables["next"][0]["target_doc"] == "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md"
    rows.append(validation_row("VAL1961_08_next_target", "PASS" if next_ok else "FAIL", "1962 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1961_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1961_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1961_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1961_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1961_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1961_OVERALL", overall, "1961 parent metric-only variable signature or P4 fill"))
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
        ("Metric-Only Signature Attempt", tables["signature"]),
        ("P4 Fill Priority Ledger", tables["p4"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1961 Y5 R2FR: Parent Metric-Only Variable Signature Or P4 Fill",
        "",
        "Private checkpoint. This tries to sign the clean metric-only/no-independent-connection route that would make the observed connection Levi-Civita by construction.",
        "",
        "Verdict: the route is exact but unsigned. The parent action must own the q->g/e->omega[e]->S_matter stack with enough metric rank and no Gamma/readout re-entry. Until then, P4 connection residuals remain active fallback rows.",
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
    print(f"VAL1961_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
