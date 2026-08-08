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

DOC_PATH = ROOT / "1953-Y5-R2FR-parent-B_eff-profile-or-kernel-bound.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1953_VALIDATION.csv"

SOURCES = {
    "1952_doc": {
        "path": ROOT / "1952-Y5-R2FR-B_eff-zero-theorem-or-STF-bound-first-fill.md",
        "needles": ["ZB1952_3_kernel_STF_silence", "ZB1952_6_verdict", "NEXT1952_0_primary"],
    },
    "1952_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1952_VALIDATION.csv",
        "needles": ["VAL1952_OVERALL", "PASS"],
    },
    "1952_bound": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_STF_BOUND_FACTOR_LEDGER.csv",
        "needles": ["BF1952_0_bound_formula", "BF1952_3_B_kernel_envelope"],
    },
    "1952_zero": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_BEFF_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["ZB1952_1_hessian_double_zero", "ZERO_PROOF_FAILED_CLEANLY"],
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
                "purpose": "1953 parent B_eff profile or kernel bound",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def profile_rows() -> list[dict[str, object]]:
    entries = [
        (
            "PB1953_0_parent_profile",
            "The Cassini-dangerous profile decomposes into hessian, kernel-carried, boundary-carried, and source-carried l=2/STF amplitudes.",
            "B_eff(r)=B_H(r)+B_K2(r)+B_boundary2(r)+B_source2(r)",
            "PROFILE_DECOMPOSITION_BUILT",
            "The local-GR problem is now an l=2 profile problem, not a generic residual cloud.",
            "nonclaim profile map only",
        ),
        (
            "PB1953_1_kernel_selection_rule",
            "An SO(3)-equivariant scalar kernel on an SO(3)-invariant local domain cannot create l=2 output from pure l=0 input.",
            "J=J_0(r) and [K,R]=0 for all R in SO(3) -> P_2 K[J_0]=0",
            "CONDITIONAL_KERNEL_CREATION_ZERO",
            "This is the first real kernel-cleaning result: kernel creation is killed by representation selection.",
            "requires parent-signed kernel equivariance and l=0-only input",
        ),
        (
            "PB1953_2_kernel_transport_caveat",
            "The same kernel can transport existing l=2 input, so B_K2 is not generally zero.",
            "B_K2(r)=K_2[J_2](r); if J_2 != 0 then B_K2 may survive",
            "LIVE_CAVEAT_RETAINED",
            "This prevents a fake theorem: symmetry kills creation, not inherited anisotropy.",
            "need J_2=0 theorem or envelope",
        ),
        (
            "PB1953_3_boundary_profile",
            "Boundary/matching data enters as an l=2 homogeneous profile unless parent boundary silence is signed.",
            "B_boundary2(r)=H_2[h_boundary2](r)",
            "OPEN_PROFILE_CHANNEL",
            "Boundary terms are now explicit objects that can be proved zero or bounded.",
            "need h_boundary2=0 theorem or envelope",
        ),
        (
            "PB1953_4_source_worldtube_profile",
            "Extended-source anisotropy and solar multipoles enter as source-worldtube l=2 input.",
            "B_source2(r)=K_2[J_source2](r)",
            "OPEN_PROFILE_CHANNEL",
            "A real solar source is not ignored; it is isolated into a boundable l=2 channel.",
            "need source projection theorem or conservative multipole envelope",
        ),
        (
            "PB1953_5_full_zero_condition",
            "The live sufficient zero theorem is J_2=0, h_boundary2=0, source2=0, plus the hessian double-zero branch.",
            "B_eff=0 if B_H=0 and J_2=h_boundary2=J_source2=0 under SO(3)-equivariant kernel/readout",
            "ZERO_THEOREM_CONDITION_SHARPENED_NOT_SIGNED",
            "The proof target is now much sharper and plausibly derivable from a parent local-vacuum theorem.",
            "still not a live Cassini pass",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, statement, math_form, status, implication, claim_scope in entries:
        row = base(row_id)
        row.update(
            {
                "statement": statement,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "claim_scope": claim_scope,
            }
        )
        rows.append(row)
    return rows


def envelope_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ENV1953_0_combined_bound",
            "S_TF_bound",
            "||W_STF||_1 (|B_H|_sup + |K_2[J_2]|_sup + |H_2[h_boundary2]|_sup + |K_2[J_source2]|_sup)",
            "MISSING_FACTORS",
            "dimensionless",
            "Same acceptance as 1952, but with source of each l=2 contribution named.",
        ),
        (
            "ENV1953_1_kernel_creation",
            "P_2 K[J_0]",
            "0 if kernel and domain are SO(3)-equivariant and input is l=0",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "dimensionless",
            "Promising zero branch; needs parent kernel/domain signature.",
        ),
        (
            "ENV1953_2_kernel_transport",
            "K_2[J_2]",
            "operator norm ||K_2|| times source l=2 envelope ||J_2||",
            "MISSING_SOURCE_L2_ENVELOPE",
            "dimensionless",
            "Boundable once source l=2 is known or proved zero.",
        ),
        (
            "ENV1953_3_boundary_transport",
            "H_2[h_boundary2]",
            "homogeneous l=2 response norm times boundary l=2 envelope",
            "MISSING_BOUNDARY_L2_ENVELOPE",
            "dimensionless",
            "Boundable once local matching conditions are specified.",
        ),
        (
            "ENV1953_4_source_worldtube",
            "K_2[J_source2]",
            "source-worldtube projection norm times solar/source anisotropy envelope",
            "MISSING_SOURCE_WORLDTUBE_L2_ENVELOPE",
            "dimensionless",
            "This is the realistic source correction branch.",
        ),
        (
            "ENV1953_5_readout_norm",
            "||W_STF||_1",
            "Cassini readout norm for radial STF profile",
            "MISSING_READOUT_NORM",
            "inverse profile units",
            "Needed only after parent profile/envelopes exist.",
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
            "RUN1953_0_kernel_creation_zero",
            "P_2 K[J_0]=0",
            "conditional theorem branch",
            "MISSING_PARENT_KERNEL_EQUIVARIANCE;MISSING_L0_ONLY_INPUT_CERTIFICATE",
            "WOULD_CLOSE_KERNEL_CREATION_IF_SIGNED",
            "kernel creation is no longer the main mystery once symmetry is signed",
        ),
        (
            "RUN1953_1_live_Beff_zero",
            "B_eff=0",
            "B_H=0 and J_2=h_boundary2=J_source2=0",
            "MISSING_J2_ZERO;MISSING_BOUNDARY2_ZERO;MISSING_SOURCE2_ZERO",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "full zero proof still blocked",
        ),
        (
            "RUN1953_2_finite_bound",
            "abs(S_TF) <= ||W_STF||_1 sum l=2 envelopes",
            "bound <= 6.7e-5",
            "MISSING_L2_ENVELOPES;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "finite bound is structured but not scoreable",
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
        (
            "CG1953_0_profile_decomposition",
            "Parent B_eff profile decomposition exists.",
            "PASS_NONCLAIM",
            "B_eff split into hessian, kernel l=2, boundary l=2, and source l=2 channels.",
        ),
        (
            "CG1953_1_kernel_creation_zero",
            "Kernel cannot create STF/l=2 from monopole input.",
            "PASS_CONDITIONAL_NONCLAIM",
            "true under SO(3)-equivariant kernel/domain and l=0 input; parent signature still needed.",
        ),
        (
            "CG1953_2_full_Beff_zero",
            "Parent proves B_eff=0.",
            "FAIL_BLOCKED",
            "J_2, boundary2, and source2 zero clauses are unsigned.",
        ),
        (
            "CG1953_3_finite_bound",
            "MTS has a finite source-backed S_TF bound.",
            "FAIL_BLOCKED",
            "l=2 envelopes and W_STF norm are missing.",
        ),
        (
            "CG1953_4_Cassini_pass",
            "MTS passes Cassini gamma.",
            "FAIL_BLOCKED",
            "no live zero theorem or finite bound exists.",
        ),
        (
            "CG1953_5_local_GR",
            "MTS derives local GR/Newton.",
            "FAIL_BLOCKED",
            "gamma and common-mode Newtonian gates remain open.",
        ),
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
            "DEC1953_0_progress",
            "KERNEL_CREATION_PARTLY_CLEANED",
            "SO(3) equivariance kills l=2 creation from l=0, but does not kill transported l=2 source/boundary data",
            "turn the conditional kernel theorem into a parent-signed lemma or move straight to l=2 zero/envelope clauses",
        ),
        (
            "DEC1953_1_best_next",
            "SOURCE_AND_BOUNDARY_L2_ZERO_OR_ENVELOPE",
            "after kernel creation is conditionally controlled, the live danger is inherited anisotropy",
            "derive J_2=0/h_boundary2=0/source2=0 from local-vacuum parent conditions, or assign conservative envelopes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base("NEXT1953_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1954-Y5-R2FR-l2-source-boundary-zero-or-envelope.md",
            "target_script": "scripts/Y5_R2FR_l2_source_boundary_zero_or_envelope_1954.py",
            "objective": "derive or bound the inherited l=2 source and boundary amplitudes that feed B_eff",
            "acceptance_output": "J_2/h_boundary2/source2 zero clauses or finite envelope rows",
            "nonclaim_rule": "do not claim Cassini/local GR until l=2 channels and W_STF give a live S_TF pass",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1953_0_project_position")
    row.update(
        {
            "strongest_result": "Kernel creation of l=2 from monopole input is conditionally killed by SO(3) representation selection.",
            "what_improved": "B_eff is now a profile decomposition with inherited l=2 source and boundary channels isolated",
            "still_missing": "parent signature for kernel equivariance/l=0 input, plus zero/envelope rows for J_2, h_boundary2, source2, and W_STF",
            "claim_status": "not a Cassini/local-GR pass; a narrowed proof target",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_SOURCE_REGISTER.csv",
    "profile": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_BEFF_PROFILE_DECOMPOSITION.csv",
    "envelopes": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_L2_ENVELOPE_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "BEFF_PROFILE_1953_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1953_L2_SOURCE_BOUNDARY_ZERO_OR_ENVELOPE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1953_0_nonclaim_weight"),
            "artifact": "1953 B_eff profile decomposition",
            "weight": "CONDITIONAL_DERIVATION_NOT_EVIDENCE",
            "reason": "profile split and kernel selection rule are useful but not a live bound or full zero proof",
        }
    ]
    queue = [
        {
            **base("AQ1953_0_parent_kernel_signature"),
            "target": "SO(3)-equivariant kernel/domain certificate",
            "needed_inputs": "parent local operator; Green kernel/domain; rotation action; l=0 input certificate",
            "priority": "HIGH",
        },
        {
            **base("AQ1953_1_l2_source_boundary"),
            "target": "inherited l=2 zero/envelope",
            "needed_inputs": "J_2, h_boundary2, source-worldtube2 definitions and zero/bound clauses",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "profile": profile_rows(),
        "envelopes": envelope_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
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
    patterns = ("1953-", "*_1953_*", "*Y5*1953*", "*VAL1953*", "*P8*1953*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1953_00_sources", "PASS" if sources_ok else "FAIL", "all source files exist and needles found"))

    profile_ok = any(row["row_id"] == "PB1953_0_parent_profile" and "B_H" in str(row["math_form"]) for row in tables["profile"])
    rows.append(validation_row("VAL1953_01_profile", "PASS" if profile_ok else "FAIL", "B_eff profile decomposition recorded"))

    kernel_ok = any(row["row_id"] == "PB1953_1_kernel_selection_rule" and row["status"] == "CONDITIONAL_KERNEL_CREATION_ZERO" for row in tables["profile"])
    rows.append(validation_row("VAL1953_02_kernel_selection", "PASS" if kernel_ok else "FAIL", "kernel creation zero condition recorded"))

    caveat_ok = any(row["row_id"] == "PB1953_2_kernel_transport_caveat" and row["status"] == "LIVE_CAVEAT_RETAINED" for row in tables["profile"])
    rows.append(validation_row("VAL1953_03_transport_caveat", "PASS" if caveat_ok else "FAIL", "kernel transport caveat retained"))

    envelope_ok = any(row["row_id"] == "ENV1953_0_combined_bound" and row["status"] == "MISSING_FACTORS" for row in tables["envelopes"])
    rows.append(validation_row("VAL1953_04_envelopes", "PASS" if envelope_ok else "FAIL", "combined l=2 envelope formula recorded but blocked"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"WOULD_CLOSE_KERNEL_CREATION_IF_SIGNED", "BLOCKED_ZERO_THEOREM_NOT_CLOSED", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1953_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks live branches and isolates kernel theorem"))

    gate_ok = any(row["row_id"] == "CG1953_0_profile_decomposition" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"]) and all(
        row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]
    )
    rows.append(validation_row("VAL1953_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "SOURCE_AND_BOUNDARY_L2_ZERO_OR_ENVELOPE" for row in tables["decision"])
    rows.append(validation_row("VAL1953_07_decision", "PASS" if decision_ok else "FAIL", "l=2 source/boundary next route selected"))

    next_ok = tables["next"][0]["target_doc"] == "1954-Y5-R2FR-l2-source-boundary-zero-or-envelope.md"
    rows.append(validation_row("VAL1953_08_next_target", "PASS" if next_ok else "FAIL", "1954 l=2 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1953_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = True
    for path in OUTPUTS.values():
        if not read_csv(path):
            csv_ok = False
    rows.append(validation_row("VAL1953_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1953_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1953_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1953_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1953_OVERALL", overall, "1953 parent B_eff profile or kernel bound"))
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
        ("B_eff Profile Decomposition", tables["profile"]),
        ("L2 Envelope Ledger", tables["envelopes"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1953 Y5 R2FR: Parent B_eff Profile Or Kernel Bound",
        "",
        "Private checkpoint. This attacks the remaining Cassini-visible STF profile, not the galaxy branch.",
        "",
        "Result: kernel creation of l=2/STF response from pure monopole input is conditionally killed by SO(3) representation selection, but inherited l=2 source and boundary channels remain live. This narrows the next proof target without making a Cassini/local-GR claim.",
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
    print(f"VAL1953_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
