from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1554_doc": ROOT / "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
    "1554_validation": OUT / "P8_Y5_BRR545_1554_VALIDATION.csv",
    "1554_next": OUT / "P8_Y5_PARENT_QLOC_1554_NEXT_TARGET.csv",
    "1554_origin": OUT / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_ORIGIN_AUDIT.csv",
    "1554_obstruction": OUT / "P8_Y5_PARENT_QLOC_1554_ORIGIN_OBSTRUCTION_LEDGER.csv",
    "12_doc": ROOT / "12-gauge-noether-origin-audit.md",
    "11_doc": ROOT / "11-cell-current-origin-attempt.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "06_doc": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "05_doc": ROOT / "05-reciprocity-theorem-attempt.md",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1022_doc": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
}

NEEDLES = {
    "12_doc": ["gauge_noether_origin_not_derived_closure_only", "Noether identity derives R_AB=0", "local reciprocity is closure-only"],
    "11_doc": ["cell_current_origin_no_charge_obstruction", "does not prove", "Q_R = 0"],
    "10_doc": ["gauge redundancy of observer splitting", "not merely a coordinate trick"],
    "1023_doc": ["momentum map", "not_derived", "degree count"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1555_SOURCE_REGISTER.csv"
GAUGE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv"
FIRST_CLASS_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"
ZERO_CHARGE_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1555_ZERO_CHARGE_RUNNER_NONCLAIM.csv"
CLOSURE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1555_LOCAL_CLOSURE_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1555_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1555_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1555_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1555_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1555"
QUAR_GAUGE = QUARANTINE / "GAUGE_NOETHER_ROUTE_AUDIT_NONCLAIM.csv"
QUAR_CONTRACT = QUARANTINE / "FIRST_CLASS_CONSTRAINT_CONTRACT_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "ZERO_CHARGE_RUNNER_NONCLAIM.csv"
QUAR_CLOSURE = QUARANTINE / "LOCAL_CLOSURE_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_GAUGE = BRANCH_RESIDUALS / "gauge_noether_route_audit_nonclaim_1555.csv"
BRANCH_CONTRACT = BRANCH_RESIDUALS / "first_class_constraint_contract_nonclaim_1555.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "zero_charge_runner_nonclaim_1555.csv"
BRANCH_CLOSURE = BRANCH_RESIDUALS / "local_closure_ledger_nonclaim_1555.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "gauge_noether_decision_nonclaim_1555.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1555_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for gauge/Noether zero-charge q-sector origin audit",
                **flags(),
            }
        )
    return rows


def gauge_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "GAUGE1555_0_radial_coordinate_gauge",
            "route": "radial coordinate gauge",
            "test": "use radial coordinate freedom to set T^2 S=1",
            "result": "REJECTED_COORDINATE_IMPORT",
            "reason": "areal radius fixes r by sphere area; using this as AB=1 imports GR-like gauge logic",
            "source_paths": source_list("12_doc", "10_doc"),
        },
        {
            "route_id": "GAUGE1555_1_cell_scale_gauge",
            "route": "cell-scale gauge",
            "test": "treat T sqrt(S) as pure observer-splitting gauge",
            "result": "REJECTED_OBSERVABLE_CHANGE",
            "reason": "T and S are clock/routing observables unless a new matter map proves otherwise",
            "source_paths": source_list("12_doc", "10_doc"),
        },
        {
            "route_id": "GAUGE1555_2_reciprocal_split_gauge",
            "route": "reciprocal split gauge",
            "test": "T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S)",
            "result": "REJECTED_IRRELEVANT_TO_RAB",
            "reason": "this leaves T sqrt(S) unchanged and cannot impose R_AB=0",
            "source_paths": source_list("12_doc"),
        },
        {
            "route_id": "GAUGE1555_3_noether_identity",
            "route": "generic Noether identity",
            "test": "use symmetry identity to force R_AB=0",
            "result": "REJECTED_IDENTITY_NOT_CONSTRAINT",
            "reason": "Noether identities relate equations; they do not set a field to zero without a constraint equation",
            "source_paths": source_list("12_doc", "1023_doc"),
        },
        {
            "route_id": "GAUGE1555_4_first_class_constraint",
            "route": "first-class parent constraint",
            "test": "parent action supplies C_R=R_AB with proper/zero boundary charge and degree-count closure",
            "result": "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT",
            "reason": "requires parent symplectic potential, generator, Q_R boundary term, bracket closure, and degree count",
            "source_paths": source_list("12_doc", "1022_doc", "1023_doc"),
        },
        {
            "route_id": "GAUGE1555_5_current_verdict",
            "route": "accepted gauge/Noether zero-charge origin",
            "test": "derive Q_R=0 and R_AB=0 without importing GR",
            "result": "NO_ACCEPTED_ORIGIN",
            "reason": "all current routes are rejected or future-contract only",
            "source_paths": source_list("1554_origin", "12_doc", "11_doc"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in rows]


def first_class_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("FCC1555_0_parent_phase_space", "parent phase space", "fields, symplectic potential, and boundary variables include q/R_AB sector", "MISSING"),
        ("FCC1555_1_constraint", "constraint equation", "C_R=0 or equivalent must contain R_AB=ln(T^2 S) as a primary/secondary constraint", "MISSING"),
        ("FCC1555_2_generator", "differentiable generator", "delta G_R[epsilon]=Omega(delta Phi,v_epsilon), G_R=int epsilon C_R+Q_R", "MISSING"),
        ("FCC1555_3_boundary_charge", "zero/proper boundary charge", "Q_R is zero, exact, or proper on local branch without deleting physical mass/time charges", "MISSING"),
        ("FCC1555_4_bracket_closure", "first-class algebra", "constraint bracket closes with no anomaly/central edge cocycle", "MISSING"),
        ("FCC1555_5_degree_count", "degree count", "constraint removes reciprocal strain pair rather than hiding a physical mode", "MISSING"),
        ("FCC1555_6_matter_map", "matter/readout map", "matter observables descend through the constrained observer split without shadow frames", "MISSING"),
        ("FCC1555_7_no_GR_import", "no GR import", "proof does not use Schwarzschild AB=1 or Einstein vacuum equations", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "needed_object": needed_object,
            "acceptance_requirement": acceptance_requirement,
            "current_status": current_status,
            "source_paths": source_list("12_doc", "1022_doc", "1023_doc"),
            **flags(),
        }
        for contract_id, needed_object, acceptance_requirement, current_status in rows
    ]


def zero_charge_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1555_0_coordinate", "coordinate gauge sets R_AB=0", "REFUSED_COORDINATE_IMPORT", "areal scaffold already fixes radial coordinate"),
        ("RUN1555_1_observer_split", "observer split gauge sets R_AB=0", "REFUSED_OBSERVABLE_CHANGE", "requires new matter map not present"),
        ("RUN1555_2_noether", "Noether identity sets R_AB=0", "REFUSED_IDENTITY_NOT_CONSTRAINT", "identity is not a constraint equation"),
        ("RUN1555_3_current", "cell current conservation sets Q_R=0", "REFUSED_NO_CHARGE_OBSTRUCTION", "current gives constant Q_R not zero"),
        ("RUN1555_4_first_class", "first-class parent constraint exists", "REFUSED_MISSING_PARENT_CONSTRAINT", "contract is known but not supplied"),
        ("RUN1555_5_closure", "closure benchmark status", "PASS_NONCLAIM", "R_AB=0 may be used only as explicit benchmark closure"),
        ("RUN1555_6_score_status", "local GR/Newton claim", "REFUSED_NOT_SCORE_READY", "no gauge/Noether zero-charge origin closes"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": current_status,
            "reason": reason,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
        for runner_id, check, current_status, reason in rows
    ]


def closure_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL1555_0_closure_statement", "explicit local closure", "assume R_AB=ln(T^2 S)=0 only as a benchmark closure", "ALLOWED_NONCLAIM"),
        ("CL1555_1_what_it_tests", "test use", "separate whether MTS can match local PPN/solar-system conditions under the closure", "BENCHMARK_ONLY"),
        ("CL1555_2_what_it_does_not_prove", "derivation limit", "does not prove parent q-sector, zero charge, q-norm, beta, conservation, or matter universality", "LIMIT_EXPLICIT"),
        ("CL1555_3_no_public_claim", "claim policy", "do not advertise local GR/Newton reduction as derived from this branch", "PASS_GUARD_NONCLAIM"),
        ("CL1555_4_reentry", "future reentry", "only a first-class constraint/no-charge theorem can promote closure to derivation", "REENTRY_CONTRACT"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "item": item,
            "statement": statement,
            "current_status": current_status,
            "source_paths": source_list("12_doc", "1554_obstruction", "10_doc"),
            **flags(),
        }
        for closure_id, item, statement, current_status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1555_0_audit", "gauge/Noether route audit", "PASS_NONCLAIM", "routes are tested and rejected or quarantined"),
        ("GATE1555_1_contract", "first-class constraint contract", "PASS_NONCLAIM", "future proof requirements are explicit"),
        ("GATE1555_2_closure", "closure benchmark ledger", "PASS_NONCLAIM", "R_AB=0 closure use is explicit"),
        ("GATE1555_3_zero_charge", "Q_R=0 theorem", "BLOCKED", "no parent no-charge theorem exists"),
        ("GATE1555_4_parent_constraint", "first-class parent constraint", "BLOCKED", "not supplied"),
        ("GATE1555_5_local_tests", "local arena score", "BLOCKED_NO_CLAIM", "benchmark not yet computed here"),
        ("GATE1555_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "closure is not derivation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1555_0_result", "Gauge/Noether zero-charge origin is not derived.", "NO_ACCEPTED_ZERO_CHARGE_ORIGIN", "coordinate, cell-scale, reciprocal split, Noether, and current routes all fail"),
        ("DEC1555_1_closure", "Use R_AB=0 only as an explicit local closure benchmark.", "CLOSURE_BENCHMARK_NEXT", "this preserves empirical testing without overclaiming derivation"),
        ("DEC1555_2_next", "Next target is local closure PPN benchmark.", "NEXT_1556_LOCAL_CLOSURE_PPN", "compute what the closure would need for gamma, beta, conservation, and matter universality"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1555_0_1556",
            "next_target": "1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
            "script": "scripts/Y5_local_closure_PPN_benchmark_and_derived_vs_assumed_ledger.py",
            "objective": "formalize the honest R_AB=0 closure benchmark and separate derived, assumed, and test-required PPN/Newton conditions",
            "do_not": "do not claim the closure is derived; do not skip beta/conservation/matter-universality gates; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (GAUGE_AUDIT, QUAR_GAUGE),
        (FIRST_CLASS_CONTRACT, QUAR_CONTRACT),
        (ZERO_CHARGE_RUNNER, QUAR_RUNNER),
        (CLOSURE_LEDGER, QUAR_CLOSURE),
        (DECISION, QUAR_DECISION),
        (GAUGE_AUDIT, BRANCH_GAUGE),
        (FIRST_CLASS_CONTRACT, BRANCH_CONTRACT),
        (ZERO_CHARGE_RUNNER, BRANCH_RUNNER),
        (CLOSURE_LEDGER, BRANCH_CLOSURE),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    audit_rows = read_csv(GAUGE_AUDIT)
    contract_rows = read_csv(FIRST_CLASS_CONTRACT)
    run_rows = read_csv(ZERO_CHARGE_RUNNER)
    closure_rows = read_csv(CLOSURE_LEDGER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1555_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1555 source paths exist"),
        ("VAL1555_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1555_2_no_origin", any(row["route_id"] == "GAUGE1555_5_current_verdict" and row["result"] == "NO_ACCEPTED_ORIGIN" for row in audit_rows), "gauge/Noether audit records no accepted origin"),
        ("VAL1555_3_contract", len(contract_rows) >= 8 and any(row["contract_id"] == "FCC1555_3_boundary_charge" for row in contract_rows), "first-class zero-charge contract written"),
        ("VAL1555_4_runner_refuses", any(row["runner_id"] == "RUN1555_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in run_rows), "zero-charge runner refuses local claim"),
        ("VAL1555_5_closure_ledger", any(row["closure_id"] == "CL1555_0_closure_statement" and row["current_status"] == "ALLOWED_NONCLAIM" for row in closure_rows), "closure benchmark ledger written"),
        ("VAL1555_6_claim_gates_block", any(row["gate_id"] == "GATE1555_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1555_7_decision_next", any(row["result"] == "NEXT_1556_LOCAL_CLOSURE_PPN" for row in decision_items), "decision selects local closure PPN benchmark next"),
        ("VAL1555_8_next_target", any("1556-Y5-local-closure-PPN" in row["next_target"] for row in next_rows), "next target is local closure PPN benchmark"),
        ("VAL1555_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1555 CSVs parse cleanly"),
        ("VAL1555_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1555_11_branch_copies", all(path.exists() for path in [QUAR_GAUGE, QUAR_CONTRACT, QUAR_RUNNER, QUAR_CLOSURE, QUAR_DECISION, BRANCH_GAUGE, BRANCH_CONTRACT, BRANCH_RUNNER, BRANCH_CLOSURE, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1555_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1555_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1555_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1555 rejects gauge/Noether shortcuts as current derivations, writes the first-class zero-charge contract, and selects local closure PPN benchmark next"
            if overall
            else "1555 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1555 - Gauge Noether Zero-Charge q-sector Origin Audit",
                "",
                "## Verdict",
                "- Gauge/Noether language does not currently derive `Q_R=0` or `R_AB=0`.",
                "- Radial coordinate gauge, cell-scale gauge, reciprocal split gauge, generic Noether identity, and cell-current conservation all fail as derivations.",
                "- The only viable future route is a genuine first-class parent constraint with differentiable generator, zero/proper boundary charge, bracket closure, degree count, and matter-map descent.",
                "- Current local use of `R_AB=0` is therefore an explicit closure benchmark, not a derived GR/Newton limit.",
                "- Next target is the local closure PPN benchmark: separate what is assumed from what must still be tested.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Gauge/Noether Route Audit",
                md_table(audit_rows, ["route_id", "route", "test", "result", "reason"]),
                "",
                "## First-Class Constraint Contract",
                md_table(contract_rows, ["contract_id", "needed_object", "acceptance_requirement", "current_status"]),
                "",
                "## Zero-Charge Runner",
                md_table(run_rows, ["runner_id", "check", "current_status", "reason"]),
                "",
                "## Closure Ledger",
                md_table(closure_rows, ["closure_id", "item", "statement", "current_status"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    audit_rows = gauge_audit_rows()
    contract_rows = first_class_contract_rows()
    run_rows = zero_charge_runner_rows()
    closure_rows = closure_ledger_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(GAUGE_AUDIT, audit_rows)
    write_csv(FIRST_CLASS_CONTRACT, contract_rows)
    write_csv(ZERO_CHARGE_RUNNER, run_rows)
    write_csv(CLOSURE_LEDGER, closure_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        GAUGE_AUDIT,
        FIRST_CLASS_CONTRACT,
        ZERO_CHARGE_RUNNER,
        CLOSURE_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, audit_rows, contract_rows, run_rows, closure_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
