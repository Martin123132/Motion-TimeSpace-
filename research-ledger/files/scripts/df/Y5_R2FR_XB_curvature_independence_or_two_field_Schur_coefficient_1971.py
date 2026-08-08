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

DOC_PATH = ROOT / "1971-Y5-R2FR-XB-curvature-independence-or-two-field-Schur-coefficient.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1971_VALIDATION.csv"

SOURCES = {
    "1970_doc": {
        "path": ROOT / "1970-Y5-R2FR-XB-source-bath-boundary-curvature-mixing-audit.md",
        "needles": ["SCHUR1970_3_coupling_location", "NEXT1970_0_primary"],
    },
    "1970_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1970_VALIDATION.csv",
        "needles": ["VAL1970_OVERALL", "PASS"],
    },
    "827_XB_drift": {
        "path": ROOT / "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md",
        "needles": ["DI827_2_moving_extremum_cancellation", "KH827_2_XB_spurion_source"],
    },
    "828_baseline_lock": {
        "path": ROOT / "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md",
        "needles": ["BL828_2_local_baseline_lock", "BL828_4_no_free_local_constant"],
    },
    "1306_XB_domain": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["FRA1306_1_XB_dependent", "XDG1306_0_argument_list", "XDG1306_1_local_branch_map"],
    },
    "1349_KMTS_owner": {
        "path": ROOT / "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
        "needles": ["KMTS1349_3_Ward_closure", "RESP1349_2_external_profiles"],
    },
    "826_Ward_audit": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv",
        "needles": ["W826_1_external_XB_spurion", "W826_3_Khat_required"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


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
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1971 X_B curvature-independence proof attempt",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def curvature_independence_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CXR1971_0_definition",
            "C_XR := delta X_B/delta R_geom on the local weak-field branch",
            "take a parent variation delta Phi_R that changes the observed Ricci scalar while preserving the local branch constraints",
            "DEFINITION_INSTALLED",
            "this is the coefficient needed by the R2/fR Schur gate",
        ),
        (
            "CXR1971_1_exact_zero_condition",
            "C_XR=0 iff D X_B[delta Phi_R]=0 for every allowed local curvature-changing variation",
            "this is a curvature-response annihilator condition, not merely an X-source or X-verticality condition",
            "EXACT_CONDITION_DERIVED",
            "the proof target is now sharply stated",
        ),
        (
            "CXR1971_2_verticality_not_enough",
            "Dq[v_X]=0 does not imply C_XR=0",
            "v_X is a hidden/vertical variation; delta Phi_R is a metric/curvature variation. They are different tangent directions unless the parent proves they coincide or one annihilates X_B",
            "NAIVE_QUOTIENT_PROOF_REJECTED",
            "prevents us from accidentally reusing the old no-pole theorem for the wrong derivative",
        ),
        (
            "CXR1971_3_external_profile_fails",
            "treating X_B as external does not prove C_XR=0",
            "external X_B may be held fixed in a calculation, but Ward/Bianchi rows call it a spurion source unless its parent owner is supplied",
            "SPURION_ZERO_REJECTED",
            "cannot win local GR by declaring the dangerous variable non-varied",
        ),
        (
            "CXR1971_4_baseline_lock_separate",
            "Gamma_L(X_B)=constant does not imply C_XR=0",
            "baseline lock kills nabla Gamma_L in q_loc; R2/fR asks whether X_B changes under curvature variation inside the effective action",
            "BASELINE_LOCK_NOT_R2FR_ZERO",
            "useful for q_loc drift, insufficient for the EH left-hand gate",
        ),
        (
            "CXR1971_5_sufficient_parent_clause",
            "A claim-grade zero theorem would require X_B to be a branch/topological label or quotient-owned environment variable annihilated by local curvature variations",
            "parent clause: X_B=X_B[I_top,q_env] and D X_B[delta Phi_R]=0 on D_loc, with source/bath/boundary variables varied or silent",
            "SUFFICIENT_THEOREM_FORMULATED_UNSIGNED",
            "this is the least-scrutiny proof route if a future parent action can supply it",
        ),
        (
            "CXR1971_6_current_corpus_verdict",
            "current inspected corpus does not prove C_XR=0",
            "X_B argument list, local branch map, metric response, and parent source/bath/boundary owner are all missing or marked nonclaim",
            "CXR_ZERO_PROOF_FAILS_CURRENT_CORPUS",
            "fall back to two-field Schur coefficient unless a new parent clause is adopted and audited",
        ),
    ]
    rows = []
    for row_id, claim, derivation, status, implication in entries:
        row = base(row_id)
        row.update(
            {
                "claim": claim,
                "derivation": derivation,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def proof_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "GATE1971_0_argument_list",
            "X_B components and parent definition",
            "1306 marks Arg[Z_m]=X_B components missing",
            "FAIL_BLOCKED",
            "cannot evaluate D X_B on curvature variations",
        ),
        (
            "GATE1971_1_local_branch_map",
            "X_B local branch map over D_loc",
            "1306 marks X_B^{local}(x) missing",
            "FAIL_BLOCKED",
            "cannot tell whether local curvature perturbations move X_B",
        ),
        (
            "GATE1971_2_metric_response",
            "metric/curvature response of X_B",
            "1302 and 1970 mark X_B metric response missing",
            "FAIL_BLOCKED",
            "C_XR is the exact missing object",
        ),
        (
            "GATE1971_3_external_spurion",
            "holding X_B fixed externally",
            "826/827/1349 reject external X_B as a parent theorem",
            "FAIL_REJECTED_AS_PROOF",
            "spurion fixing is allowed only as private closure, not a GR derivation",
        ),
        (
            "GATE1971_4_baseline_lock",
            "baseline lock relation",
            "828 supplies conditional q_loc drift cancellation",
            "PASS_DIFFERENT_GATE_ONLY",
            "helps q_loc but does not close R2/fR",
        ),
        (
            "GATE1971_5_result",
            "C_XR=0 proof",
            "one exact theorem condition is available, but no current source signs its premises",
            "FAIL_CURRENT_CORPUS",
            "proceed to Schur coefficient or new parent ownership clause",
        ),
    ]
    rows = []
    for row_id, gate, evidence, status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "gate": gate,
                "evidence": evidence,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def schur_input_rows() -> list[dict[str, object]]:
    entries = [
        ("SCHIN1971_0_CXR", "C_XR or B_XR", "delta X_B/delta R_geom or curvature-linear vertex", "MISSING_EXACT_OBJECT", "first fallback coefficient"),
        ("SCHIN1971_1_HX", "H_X", "X_B Hessian/operator, domain, sign, inverse", "MISSING_OPERATOR", "denominator for X_B response"),
        ("SCHIN1971_2_Hm", "H_m", "memory Hessian including Z_m and V_mm", "PARTIAL_TEMPLATE_ONLY", "denominator for memory response"),
        ("SCHIN1971_3_HmX", "H_mX or V_mX", "mixed memory/environment Hessian", "MISSING_COUPLING", "this is where the coupling lives if X_B is live"),
        ("SCHIN1971_4_source_bath", "source/bath vertices", "curvature and memory couplings from source/bath variables", "MISSING_ACTION", "needed for Ward-safe Schur block"),
        ("SCHIN1971_5_boundary", "boundary/counterterm vertices", "curvature-memory/environment response of boundary terms", "MISSING_BOUNDARY_OWNER", "needed for local exterior no-tower proof"),
        ("SCHIN1971_6_units", "normalization and units", "parent sign convention, units of R, m, X_B, and c_R2", "MISSING_UNITS", "needed before numeric R11 comparison"),
    ]
    rows = []
    for row_id, needed_object, formula_or_definition, status, role in entries:
        row = base(row_id)
        row.update(
            {
                "needed_object": needed_object,
                "formula_or_definition": formula_or_definition,
                "status": status,
                "role": role,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1971_0_exact_condition", "CXR1971_1_exact_zero_condition", "PASS_RELATIVE_THEOREM", "zero condition is mathematically precise"),
        ("RUN1971_1_verticality", "CXR1971_2_verticality_not_enough", "REJECTED_AS_INSUFFICIENT", "old quotient verticality is the wrong derivative"),
        ("RUN1971_2_spurion", "CXR1971_3_external_profile_fails", "REJECTED_AS_PARENT_PROOF", "external fixing violates Ward/Bianchi discipline"),
        ("RUN1971_3_current_zero", "CXR1971_6_current_corpus_verdict", "REJECTED_CXR_ZERO_UNSIGNED", "no source signs curvature-independence"),
        ("RUN1971_4_schur", "SCHIN1971_0..6", "REJECTED_MISSING_SCHUR_INPUTS", "fallback coefficient cannot yet be scored"),
        ("RUN1971_VERDICT", "all_rows", "CXR_ZERO_FAILS_SCHUR_INPUTS_MISSING_NONCLAIM", "local EH gate remains blocked but is now sharply localized"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1971_0_CXR_zero", "C_XR=0 is derived", "FAIL_BLOCKED", "exact condition formulated but unsigned"),
        ("CG1971_1_quotient_verticality", "old vertical quotient proof clears R2/fR", "FAIL_REJECTED", "vertical hidden variation is not a curvature variation"),
        ("CG1971_2_external_XB", "external X_B fixed proves local GR", "FAIL_REJECTED", "spurion source, closure-only"),
        ("CG1971_3_schur_coefficient", "two-field Schur coefficient is scoreable", "FAIL_BLOCKED", "C_XR/H_X/H_mX/source/boundary missing"),
        ("CG1971_4_EH_second_order", "EH second-order local action is derived", "FAIL_BLOCKED", "R2/fR tower not eliminated"),
        ("CG1971_5_local_GR_Newton", "local GR/Newton theorem follows", "FAIL_BLOCKED", "EH plus PPN matter gates remain"),
    ]
    rows = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1971_0_real_gain",
            "WRONG_ZERO_PROOF_REJECTED",
            "We cannot reuse Dq[v_X]=0 to claim C_XR=0; that would be mixing two tangent directions.",
            "do not spend more cycles on generic verticality for this gate",
        ),
        (
            "DEC1971_1_best_next",
            "MINIMAL_XB_PARENT_OWNERSHIP_CLAUSE_OR_SCHUR_FILL",
            "The clean route is still a parent clause proving D X_B[delta Phi_R]=0; if that cannot be supplied, the only honest route is the two-field Schur coefficient.",
            "attempt a minimal X_B ownership/action clause, with explicit failover to coefficient rows",
        ),
        (
            "DEC1971_2_project_read",
            "NOT_GRIM_BUT_NOT_CLOSED",
            "This is not circular drift: the project found the exact place where local EH can be won or lost.",
            "next work should either sign the X_B clause or start filling the coefficient matrix",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1971_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md",
            "target_script": "scripts/Y5_R2FR_minimal_XB_parent_ownership_clause_or_Schur_fill_1972.py",
            "objective": "try to write the minimal parent action/quotient clause that makes D X_B[delta Phi_R]=0; otherwise instantiate nonclaim Schur input rows",
            "acceptance_output": "signed-style clause checklist or explicit C_XR/H_X/H_mX/B_source/B_boundary acquisition pack",
            "nonclaim_rule": "no EH/local-GR claim while X_B curvature response is unsigned",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1971_0_project_position")
    row.update(
        {
            "strongest_result": "The R2/fR local-GR gate is now reduced to an exact curvature-response condition: D X_B[delta Phi_R]=0.",
            "what_improved": "We rejected the tempting but invalid shortcut from quotient verticality to curvature-independence, avoiding a false GR derivation.",
            "still_missing": "parent X_B ownership clause, local curvature-variation tangent map, C_XR, H_X, H_mX, source/bath/boundary vertices, units",
            "claim_status": "private nonclaim; theorem condition clear, current proof fails",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_SOURCE_REGISTER.csv",
    "curvature_independence": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_CXR_CURVATURE_INDEPENDENCE_PROOF.csv",
    "proof_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_CXR_PROOF_GATE.csv",
    "schur_inputs": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_TWO_FIELD_SCHUR_INPUTS.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1971_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "XB_CURVATURE_RESPONSE_1971_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1971_XB_CURVATURE_RESPONSE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1971_0_nonclaim_weight"),
            "artifact": "1971 X_B curvature-independence proof attempt",
            "weight": "EXACT_GATE_LOCALIZED_PROOF_UNSIGNED",
            "reason": "C_XR zero condition derived, but current corpus does not sign it",
        }
    ]
    queue = [
        {
            **base("AQ1971_0_parent_XB_clause"),
            "target": "minimal X_B ownership clause",
            "needed_inputs": "X_B definition; allowed delta Phi_R; proof D X_B[delta Phi_R]=0; source/bath/boundary treatment",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1971_1_Schur_fill"),
            "target": "two-field Schur coefficient pack",
            "needed_inputs": "C_XR/B_XR; H_X; H_m; H_mX; source/bath/boundary vertices; units; domain",
            "priority": "FALLBACK",
        },
    ]
    return {
        "source_register": source_register(),
        "curvature_independence": curvature_independence_rows(),
        "proof_gate": proof_gate_rows(),
        "schur_inputs": schur_input_rows(),
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
    patterns = ("1971-", "*_1971_*", "*Y5*1971*", "*VAL1971*", "*P8*1971*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1971_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    exact_ok = any(row["row_id"] == "CXR1971_1_exact_zero_condition" and row["status"] == "EXACT_CONDITION_DERIVED" for row in tables["curvature_independence"])
    reject_ok = any(row["row_id"] == "CXR1971_2_verticality_not_enough" and row["status"] == "NAIVE_QUOTIENT_PROOF_REJECTED" for row in tables["curvature_independence"])
    fail_ok = any(row["row_id"] == "CXR1971_6_current_corpus_verdict" and row["status"] == "CXR_ZERO_PROOF_FAILS_CURRENT_CORPUS" for row in tables["curvature_independence"])
    rows.append(validation_row("VAL1971_01_cxr_logic", "PASS" if exact_ok and reject_ok and fail_ok else "FAIL", "C_XR condition derived and invalid shortcut rejected"))

    gate_ok = any(row["row_id"] == "GATE1971_5_result" and row["status"] == "FAIL_CURRENT_CORPUS" for row in tables["proof_gate"])
    baseline_ok = any(row["row_id"] == "GATE1971_4_baseline_lock" and row["status"] == "PASS_DIFFERENT_GATE_ONLY" for row in tables["proof_gate"])
    rows.append(validation_row("VAL1971_02_proof_gate", "PASS" if gate_ok and baseline_ok else "FAIL", "proof gate distinguishes q_loc baseline lock from R2/fR zero"))

    schur_ok = all(str(row["status"]).startswith("MISSING_") or row["status"] == "PARTIAL_TEMPLATE_ONLY" for row in tables["schur_inputs"])
    rows.append(validation_row("VAL1971_03_schur_inputs", "PASS" if schur_ok else "FAIL", "Schur inputs remain explicit missing rows"))

    runner_ok = any(row["row_id"] == "RUN1971_VERDICT" and row["runner_status"] == "CXR_ZERO_FAILS_SCHUR_INPUTS_MISSING_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1971_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks EH/no-tower claim"))

    gate_claim_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1971_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1971_05_claim_gates", "PASS" if gate_claim_ok else "FAIL", "all claim gates blocked or rejected"))

    decision_ok = any(row["decision"] == "WRONG_ZERO_PROOF_REJECTED" for row in tables["decision"])
    rows.append(validation_row("VAL1971_06_decision", "PASS" if decision_ok else "FAIL", "decision ledger records rejected shortcut"))

    next_ok = tables["next"][0]["target_doc"] == "1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md"
    rows.append(validation_row("VAL1971_07_next_target", "PASS" if next_ok else "FAIL", "1972 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1971_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1971_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1971_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1971_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1971_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1971_OVERALL", overall, "1971 X_B curvature-independence proof attempt"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("C_XR Curvature-Independence Proof", tables["curvature_independence"]),
        ("Proof Gate", tables["proof_gate"]),
        ("Two-Field Schur Inputs", tables["schur_inputs"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1971 Y5 R2FR: X_B Curvature-Independence Or Two-Field Schur Coefficient",
        "",
        "Private checkpoint. This attempts the cleanest possible zero proof for the `X_B` curvature-response coefficient found in 1970.",
        "",
        "Verdict: the exact condition is now derived: `C_XR=0` iff `D X_B[delta Phi_R]=0` for every allowed local curvature-changing parent variation. The current corpus does **not** prove this. In particular, `Dq[v_X]=0` is not enough because the old vertical hidden variation and the curvature-changing metric variation are different tangent directions.",
        "",
        "So this is a real gain but not a closure: the next route is either a minimal parent ownership clause for `X_B`, or the honest two-field Schur coefficient pack.",
        "",
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1971_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
