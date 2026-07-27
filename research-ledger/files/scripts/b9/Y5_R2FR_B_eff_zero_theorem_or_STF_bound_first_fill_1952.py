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

DOC_PATH = ROOT / "1952-Y5-R2FR-B_eff-zero-theorem-or-STF-bound-first-fill.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1952_VALIDATION.csv"

SOURCE_FILES = {
    "1951_doc": {
        "path": ROOT / "1951-Y5-R2FR-STF-response-functional-or-common-mode-router.md",
        "needles": ["FUNC1951_2_dimensionless_STF_response", "FUNC1951_4_zero_theorem", "NEXT1951_0_primary"],
    },
    "1951_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1951_VALIDATION.csv",
        "needles": ["VAL1951_OVERALL", "PASS"],
    },
    "1951_functional": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_STF_RESPONSE_FUNCTIONAL.csv",
        "needles": ["FUNC1951_1_hessian_amplitude_law", "FUNC1951_3_norm_bound"],
    },
    "1951_inputs": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_STF_INPUT_LEDGER.csv",
        "needles": ["MISSING_PARENT_STF_AMPLITUDE_PROFILE", "MISSING_CASSINI_STF_READOUT_NORM"],
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def row_base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": now(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCE_FILES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing_needles = [needle for needle in needles if needle not in text]
        row = row_base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1952 B_eff zero theorem or STF bound first fill",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing_needles else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing_needles),
            }
        )
        rows.append(row)
    return rows


def zero_theorem_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ZB1952_0_target",
            "Close the Cassini zero route by proving B_eff(r)=0 for the extra MTS STF residual.",
            "B_eff = B_H + B_kernel + B_boundary + B_source",
            "OPEN",
            "This is the right target; it is stronger and cleaner than merely tuning gamma.",
            "all four pieces must be zero or bounded",
        ),
        (
            "ZB1952_1_hessian_double_zero",
            "The scalar Hessian channel is zero exactly when f''=f'/r.",
            "B_H=f''-f'/r=0 -> f(r)=a r^2/2 + b",
            "CONDITIONAL_DERIVED",
            "This is a real derivation, but only for the scalar Hessian piece.",
            "parent must prove the residual really enters through this branch",
        ),
        (
            "ZB1952_2_localized_branch",
            "If the scalar Hessian branch is bounded/localized/decaying, the quadratic mode is excluded and B_H=0.",
            "f=a r^2/2+b; localized exterior requires a=0; Hessian constant mode vanishes",
            "CONDITIONAL_DERIVED",
            "This gives a plausible local-vacuum kill route for Hessian leakage.",
            "parent must sign the boundary condition and exclude a cosmological quadratic remnant locally",
        ),
        (
            "ZB1952_3_kernel_STF_silence",
            "The nonlocal/local inverse kernel must not reintroduce an STF radial coefficient.",
            "B_kernel=0",
            "UNSIGNED",
            "This cannot be assumed from spherical symmetry alone.",
            "need kernel equivariance plus no derivative/tidal STF output, or a finite bound",
        ),
        (
            "ZB1952_4_boundary_STF_silence",
            "Boundary and matching terms must be STF-silent in the local solar-system domain.",
            "B_boundary=0",
            "UNSIGNED",
            "This is a real open gate because boundary conditions can carry quadrupolar information.",
            "need parent boundary condition or measured envelope",
        ),
        (
            "ZB1952_5_source_worldtube_STF_silence",
            "Extended-source anisotropy and solar multipoles must not source the extra MTS STF residual.",
            "B_source=0 or |B_source| bounded",
            "UNSIGNED",
            "A real Sun is not an exact point monopole; this cannot be swept under the rug.",
            "need source-worldtube projection theorem or conservative bound",
        ),
        (
            "ZB1952_6_verdict",
            "The B_eff=0 theorem is not closed at 1952.",
            "B_eff=0 is blocked by unsigned kernel, boundary, and source-worldtube clauses",
            "ZERO_PROOF_FAILED_CLEANLY",
            "Not grim, but honest: the route narrows to a three-clause parent proof or finite bound.",
            "move to parent-kernel/boundary/source proof or bound acquisition",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, result, required_fix in entries:
        row = row_base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "result": result,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def bound_factor_rows() -> list[dict[str, object]]:
    entries = [
        (
            "BF1952_0_bound_formula",
            "S_TF_bound",
            "||W_STF||_1 (|B_H|_sup + |B_kernel|_sup + |B_boundary|_sup + |B_source|_sup)",
            "MISSING_FACTORS",
            "dimensionless",
            "First finite-bound formula assembled, but not scoreable.",
        ),
        (
            "BF1952_1_W_STF_norm",
            "||W_STF||_1",
            "Cassini STF readout norm in the 1951 convention",
            "MISSING",
            "inverse B_eff units",
            "Need standard PPN/Cassini normalization or internal readout derivation.",
        ),
        (
            "BF1952_2_B_H_envelope",
            "|B_H|_sup",
            "scalar Hessian STF amplitude envelope",
            "CONDITIONAL_ZERO_IF_PARENT_SIGNED",
            "dimensionless",
            "Zero if scalar Hessian branch plus localized double-zero law is parent-signed.",
        ),
        (
            "BF1952_3_B_kernel_envelope",
            "|B_kernel|_sup",
            "kernel-generated STF amplitude envelope",
            "MISSING",
            "dimensionless",
            "Need zero theorem or conservative kernel bound.",
        ),
        (
            "BF1952_4_B_boundary_envelope",
            "|B_boundary|_sup",
            "boundary/matching STF amplitude envelope",
            "MISSING",
            "dimensionless",
            "Need local boundary condition or measured matching bound.",
        ),
        (
            "BF1952_5_B_source_envelope",
            "|B_source|_sup",
            "source-worldtube anisotropy/multipole STF amplitude envelope",
            "MISSING",
            "dimensionless",
            "Need source projection theorem or solar-system multipole bound.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, status, units, next_action in entries:
        row = row_base(row_id)
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
            "RUN1952_0_zero_theorem",
            "B_eff=0 -> S_TF=0",
            "0 <= 6.7e-5",
            "UNSIGNED_KERNEL_BOUNDARY_SOURCE_CLAUSES",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "cannot claim Cassini pass from zero theorem",
        ),
        (
            "RUN1952_1_finite_bound",
            "abs(S_TF) <= ||W_STF||_1 sum_i |B_i|_sup",
            "bound <= 6.7e-5",
            "MISSING_W_STF;MISSING_B_KERNEL;MISSING_B_BOUNDARY;MISSING_B_SOURCE",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "cannot score finite bound yet",
        ),
        (
            "RUN1952_2_hessian_only_toy",
            "if only B_H exists and parent signs localized double-zero, S_TF=0",
            "0 <= 6.7e-5",
            "MISSING_PARENT_BRANCH_EXCLUSIVITY",
            "TOY_BRANCH_WOULD_PASS_BUT_NOT_LIVE",
            "useful as theorem target, invalid as live claim",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = row_base(row_id)
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
            "CG1952_0_hessian_double_zero_law",
            "Hessian STF zero law is derived.",
            "PASS_NONCLAIM",
            "the law is correct but conditional on branch ownership",
        ),
        (
            "CG1952_1_B_eff_zero",
            "Parent proves B_eff=0.",
            "FAIL_BLOCKED",
            "kernel, boundary, and source-worldtube clauses are unsigned",
        ),
        (
            "CG1952_2_finite_bound",
            "MTS has a finite source-backed bound on S_TF.",
            "FAIL_BLOCKED",
            "W_STF and several B envelopes are missing",
        ),
        (
            "CG1952_3_Cassini_pass",
            "MTS passes Cassini gamma.",
            "FAIL_BLOCKED",
            "no live zero proof or finite bound exists",
        ),
        (
            "CG1952_4_local_GR",
            "MTS derives local GR/Newton.",
            "FAIL_BLOCKED",
            "Cassini gamma and common-mode Newtonian gates remain open",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = row_base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1952_0_verdict",
            "B_EFF_ZERO_NOT_PROVED_BUT_REDUCED",
            "the hessian piece has a real double-zero law, but live B_eff also has kernel, boundary, and source pieces",
            "do not keep asserting a plateau; attack the unsigned clauses or fill finite bound factors",
        ),
        (
            "DEC1952_1_best_route",
            "PARENT_PROFILE_FIRST_THEN_READOUT_NORM",
            "W_STF is external/technical, but without a parent B_eff profile it only creates an empty bound",
            "derive B_kernel/B_boundary/B_source zero or envelopes from the parent local action",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = row_base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = row_base("NEXT1952_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1953-Y5-R2FR-parent-B_eff-profile-or-kernel-bound.md",
            "target_script": "scripts/Y5_R2FR_parent_B_eff_profile_or_kernel_bound_1953.py",
            "objective": "derive the parent B_eff profile decomposition for kernel, boundary, and source-worldtube channels, or assign conservative nonclaim envelopes",
            "acceptance_output": "B_kernel/B_boundary/B_source zero clauses or finite envelope rows",
            "nonclaim_rule": "no Cassini/local-GR claim unless combined S_TF zero or finite bound is live and sourced",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = row_base("SNAP1952_0_project_position")
    row.update(
        {
            "strongest_result": "The hessian STF channel has an exact double-zero law, but full B_eff=0 is not proved.",
            "what_improved": "the live Cassini blocker is now three named clauses: kernel STF, boundary STF, and source-worldtube STF",
            "still_missing": "parent-signed zero clauses or finite envelopes for B_kernel, B_boundary, B_source, plus W_STF if using bounds",
            "claim_status": "not a Cassini/local-GR pass; a cleaner failure that tells us exactly where to strike next",
        }
    )
    return [row]


CSV_OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_SOURCE_REGISTER.csv",
    "zero_theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_BEFF_ZERO_THEOREM_ATTEMPT.csv",
    "bound_factors": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_STF_BOUND_FACTOR_LEDGER.csv",
    "runner_update": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_CLAIM_GATE.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1952_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "BEFF_ZERO_THEOREM_1952_NONCLAIM.csv",
    "acquisition_queue": RAB_QUEUE / "JR1952_PARENT_BEFF_PROFILE_OR_KERNEL_BOUND_QUEUE.csv",
}


def rows_by_name() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **row_base("SW1952_0_nonclaim_weight"),
            "artifact": "1952 B_eff zero theorem attempt",
            "weight": "PARTIAL_DERIVATION_NOT_EVIDENCE",
            "reason": "hessian double-zero is useful, but full B_eff zero and finite bound remain missing",
        }
    ]
    acquisition_queue = [
        {
            **row_base("AQ1952_0_kernel_clause"),
            "target": "B_kernel zero or envelope",
            "needed_inputs": "parent local inverse operator; kernel symmetry; support/boundary domain",
            "priority": "HIGH",
        },
        {
            **row_base("AQ1952_1_boundary_clause"),
            "target": "B_boundary zero or envelope",
            "needed_inputs": "local matching condition; boundary support; cosmology/local split",
            "priority": "HIGH",
        },
        {
            **row_base("AQ1952_2_source_clause"),
            "target": "B_source zero or envelope",
            "needed_inputs": "source-worldtube projection; solar multipole/anisotropy coupling route",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register_rows(),
        "zero_theorem": zero_theorem_rows(),
        "bound_factors": bound_factor_rows(),
        "runner_update": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "acquisition_queue": acquisition_queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1952-", "*_1952_*", "*Y5*1952*", "*VAL1952*", "*P8*1952*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1952_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found"))

    hessian_ok = any(row["row_id"] == "ZB1952_1_hessian_double_zero" and row["status"] == "CONDITIONAL_DERIVED" for row in tables["zero_theorem"])
    rows.append(validation_row("VAL1952_01_hessian_law", "PASS" if hessian_ok else "FAIL", "hessian double-zero law retained"))

    verdict_ok = any(row["row_id"] == "ZB1952_6_verdict" and row["status"] == "ZERO_PROOF_FAILED_CLEANLY" for row in tables["zero_theorem"])
    rows.append(validation_row("VAL1952_02_zero_verdict", "PASS" if verdict_ok else "FAIL", "zero proof failure recorded cleanly"))

    unsigned_ids = {"ZB1952_3_kernel_STF_silence", "ZB1952_4_boundary_STF_silence", "ZB1952_5_source_worldtube_STF_silence"}
    unsigned_ok = unsigned_ids.issubset({row["row_id"] for row in tables["zero_theorem"] if row["status"] == "UNSIGNED"})
    rows.append(validation_row("VAL1952_03_unsigned_clauses", "PASS" if unsigned_ok else "FAIL", "kernel boundary source clauses remain unsigned"))

    bound_ok = any(row["row_id"] == "BF1952_0_bound_formula" and row["status"] == "MISSING_FACTORS" for row in tables["bound_factors"])
    rows.append(validation_row("VAL1952_04_bound_formula", "PASS" if bound_ok else "FAIL", "finite bound formula assembled but blocked"))

    runner_statuses = {row["runner_status"] for row in tables["runner_update"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "BLOCKED_MISSING_BOUND_FACTORS", "TOY_BRANCH_WOULD_PASS_BUT_NOT_LIVE"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1952_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks live branches and marks toy branch nonlive"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1952_0_hessian_double_zero_law" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1952_06_claim_gates", "PASS" if gate_ok else "FAIL", "only hessian law passes nonclaim; claims blocked"))

    decision_ok = any(row["decision"] == "PARENT_PROFILE_FIRST_THEN_READOUT_NORM" for row in tables["decision_ledger"])
    rows.append(validation_row("VAL1952_07_decision", "PASS" if decision_ok else "FAIL", "parent profile selected before readout norm"))

    next_ok = tables["next_target"][0]["target_doc"] == "1953-Y5-R2FR-parent-B_eff-profile-or-kernel-bound.md"
    rows.append(validation_row("VAL1952_08_next_target", "PASS" if next_ok else "FAIL", "1953 parent B_eff profile target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1952_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_parse_ok = True
    for output_path in CSV_OUTPUTS.values():
        if not read_csv(output_path):
            csv_parse_ok = False
    rows.append(validation_row("VAL1952_10_csv_parse", "PASS" if csv_parse_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    rows.append(validation_row("VAL1952_11_pycache_absent", "PASS" if not pycache_path.exists() else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_artifact_count()
    rows.append(validation_row("VAL1952_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1952_artifact_count={formalization_count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1952_OVERALL", overall, "1952 B_eff zero theorem or STF bound first fill"))
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
        ("B_eff Zero Theorem Attempt", tables["zero_theorem"]),
        ("STF Bound Factor Ledger", tables["bound_factors"]),
        ("Runner Update", tables["runner_update"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision_ledger"]),
        ("Next Target", tables["next_target"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1952 Y5 R2FR: B_eff Zero Theorem Or STF Bound First Fill",
        "",
        "Private checkpoint. This tries the derivation-first route for the Cassini-visible STF amplitude.",
        "",
        "Verdict: the scalar Hessian channel has a real double-zero law, but full `B_eff=0` is not yet proved because kernel, boundary, and source-worldtube STF clauses remain unsigned. The fallback finite-bound route is assembled but not scoreable.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = rows_by_name()
    for name, path in CSV_OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1952_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
