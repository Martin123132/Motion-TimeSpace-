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
DOC = ROOT / "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1553_doc": ROOT / "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md",
    "1553_validation": OUT / "P8_Y5_BRR545_1553_VALIDATION.csv",
    "1553_next": OUT / "P8_Y5_PARENT_QLOC_1553_NEXT_TARGET.csv",
    "1553_ansatz": OUT / "P8_Y5_PARENT_QLOC_1553_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv",
    "1553_smoke": OUT / "P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv",
    "1552_template": OUT / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
    "1552_filters": OUT / "P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv",
    "1551_hunt": OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv",
    "1550_dual": OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
    "07_doc": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "08_doc": ROOT / "08-phase-volume-reciprocity-origin.md",
    "09_doc": ROOT / "09-hamiltonian-radial-cell-derivation.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "11_doc": ROOT / "11-cell-current-origin-attempt.md",
}

NEEDLES = {
    "08_doc": ["phase_volume_reciprocity_motivated_not_parent_derived", "Generic volume preservation does not work"],
    "09_doc": ["generic symplectic or Liouville phase-volume preservation does not derive p=1", "not yet a parent derivation"],
    "10_doc": ["observer_map_contract_written_not_satisfied", "must preserve or constrain the radial observer configuration cell separately"],
    "11_doc": ["cell_current_origin_no_charge_obstruction", "does not prove the charge is zero"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1554_SOURCE_REGISTER.csv"
ORIGIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_ORIGIN_AUDIT.csv"
QSECTOR_MAPPING = OUT / "P8_Y5_PARENT_QLOC_1554_QSECTOR_MAPPING_NONCLAIM.csv"
OBSTRUCTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1554_ORIGIN_OBSTRUCTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1554_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1554_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1554_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1554_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1554"
QUAR_ORIGIN = QUARANTINE / "PHASE_VOLUME_ORIGIN_AUDIT_NONCLAIM.csv"
QUAR_MAPPING = QUARANTINE / "QSECTOR_MAPPING_NONCLAIM.csv"
QUAR_OBSTRUCTION = QUARANTINE / "ORIGIN_OBSTRUCTION_LEDGER_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "PHASE_VOLUME_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ORIGIN = BRANCH_RESIDUALS / "phase_volume_origin_audit_nonclaim_1554.csv"
BRANCH_MAPPING = BRANCH_RESIDUALS / "qsector_mapping_nonclaim_1554.csv"
BRANCH_OBSTRUCTION = BRANCH_RESIDUALS / "origin_obstruction_ledger_nonclaim_1554.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "phase_volume_runner_nonclaim_1554.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "phase_volume_decision_nonclaim_1554.csv"


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
                "source_id": f"SRC1554_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for phase-volume/nonpropagating q-sector origin audit",
                **flags(),
            }
        )
    return rows


def origin_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "origin_id": "ORG1554_0_radial_cell_rule",
            "candidate_origin": "radial t-r observer-cell preservation",
            "mathematical_form": "J_q=T sqrt(S)=1 <=> T^2 S=1 <=> R_AB=0",
            "what_it_derives": "selects p=1 exactly for S=(1-L)^(-p)",
            "failure_or_limit": "separate radial cell preservation is not derived from parent action",
            "current_status": "MOTIVATED_NOT_PARENT_DERIVED",
            "source_paths": source_list("08_doc", "09_doc", "10_doc"),
        },
        {
            "origin_id": "ORG1554_1_generic_phase_volume",
            "candidate_origin": "generic Liouville/canonical phase-volume preservation",
            "mathematical_form": "J_q J_p=(T sqrt(S))*(1/(T sqrt(S)))=1",
            "what_it_derives": "canonical phase volume is preserved for every p",
            "failure_or_limit": "does not select GR lane p=1",
            "current_status": "REJECTED_TOO_WEAK",
            "source_paths": source_list("08_doc", "09_doc", "10_doc"),
        },
        {
            "origin_id": "ORG1554_2_nonpropagating_constraint",
            "candidate_origin": "hard nonpropagating constraint",
            "mathematical_form": "S_constraint=int lambda_R ln(T^2 S) dV",
            "what_it_derives": "R_AB=0 without exterior reciprocal kinetic hair",
            "failure_or_limit": "lambda_R parent origin remains missing",
            "current_status": "CLOSURE_ROUTE_NOT_PARENT_DERIVED",
            "source_paths": source_list("07_doc", "10_doc", "1553_ansatz"),
        },
        {
            "origin_id": "ORG1554_3_cell_current",
            "candidate_origin": "conserved radial observer-cell current",
            "mathematical_form": "partial_r(W partial_r R_AB)=0 => W partial_r R_AB=Q_R",
            "what_it_derives": "conserved reciprocal charge",
            "failure_or_limit": "does not prove Q_R=0 and permits exterior Q_R/r hair",
            "current_status": "REJECTED_NO_CHARGE_OBSTRUCTION",
            "source_paths": source_list("11_doc", "10_doc"),
        },
        {
            "origin_id": "ORG1554_4_motion_capacity_balance",
            "candidate_origin": "motion-capacity balance",
            "mathematical_form": "clock-capacity loss d ln T is compensated by radial routing d ln sqrt(S)",
            "what_it_derives": "could motivate d ln(T sqrt(S))=0",
            "failure_or_limit": "needs a parent conservation/no-charge theorem, not just a story",
            "current_status": "PROMISING_BUT_UNSIGNED",
            "source_paths": source_list("08_doc", "09_doc", "1553_ansatz"),
        },
        {
            "origin_id": "ORG1554_5_current_verdict",
            "candidate_origin": "accepted phase-volume q-sector origin",
            "mathematical_form": "none accepted",
            "what_it_derives": "no parent q-norm or lambda origin yet",
            "failure_or_limit": "phase-volume motivates nonpropagating q but does not derive parent action/norm",
            "current_status": "NO_ACCEPTED_ORIGIN",
            "source_paths": source_list("1553_ansatz", "08_doc", "09_doc", "11_doc"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in rows]


def qsector_mapping_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MAP1554_0_q_variable",
            "q := R_AB = ln(T^2 S)",
            "maps the scalar reciprocal strain into the q-sector candidate",
            "CONDITIONAL_SYMBOLIC_MAP",
            "does not define full q^A field family or tracefree/PPN sectors",
        ),
        (
            "MAP1554_1_auxiliary_constraint",
            "S_lambda=int lambda_q q dV",
            "nonpropagating closure can force q=0",
            "CLOSURE_ONLY",
            "no positive q-norm E follows from multiplier alone",
        ),
        (
            "MAP1554_2_auxiliary_penalty",
            "S_penalty=1/2 int mu_q^2 q^2 dV",
            "would supply an algebraic q-norm without gradient hair",
            "NOT_PARENT_DERIVED",
            "mu_q^2/G_AB coefficient is inserted unless phase-volume theorem supplies it",
        ),
        (
            "MAP1554_3_source_current",
            "J_q=delta S_matter/delta q",
            "needed for T_source_norm",
            "MISSING_PARENT_COUPLING",
            "phase-volume route does not provide matter q-variation",
        ),
        (
            "MAP1554_4_Cqm",
            "C_qm=||Dq[v_m]||_E",
            "needed for same-norm envelope",
            "MISSING_PARENT_NORM",
            "no accepted E from phase-volume alone",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": map_id,
            "qsector_object": qsector_object,
            "role": role,
            "current_status": current_status,
            "blocker": blocker,
            "source_paths": source_list("1550_dual", "1552_template", "1553_smoke"),
            **flags(),
        }
        for map_id, qsector_object, role, current_status, blocker in rows
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS1554_0_generic_volume", "generic phase-volume fails", "too weak; true for all p or selects wrong p", "REJECTED"),
        ("OBS1554_1_separate_cell", "separate radial cell is extra", "J_q=1 is exactly the missing theorem", "OPEN"),
        ("OBS1554_2_lambda_origin", "lambda_R origin missing", "constraint works only as closure unless parent supplies multiplier principle", "OPEN"),
        ("OBS1554_3_no_charge", "cell-current no-charge theorem missing", "current conservation gives Q_R constant not zero", "OPEN"),
        ("OBS1554_4_norm", "positive q-norm missing", "constraint gives q=0 but not E for T_source_norm*C_qm", "OPEN"),
        ("OBS1554_5_matter", "matter coupling missing", "phase-volume does not derive J_q", "OPEN"),
        ("OBS1554_6_tracefree", "scalar scope only", "T^2 S=1 does not derive tracefree metric transfer", "OPEN"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "reason": reason,
            "current_status": current_status,
            "source_paths": source_list("08_doc", "09_doc", "10_doc", "11_doc"),
            **flags(),
        }
        for obstruction_id, obstruction, reason, current_status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1554_0_radial_cell", "radial t-r cell selects p=1", "PASS_CONDITIONAL_NONCLAIM", "works algebraically but origin is unsigned"),
        ("RUN1554_1_generic_phase_volume", "generic phase-volume derives p=1", "REFUSED_REJECTED_TOO_WEAK", "Liouville/canonical volume works for every p"),
        ("RUN1554_2_constraint", "nonpropagating constraint derives q=0", "PASS_CLOSURE_NONCLAIM", "valid closure form but lambda origin missing"),
        ("RUN1554_3_penalty_norm", "phase-volume derives algebraic q-norm", "REFUSED_MISSING_COEFFICIENT_ORIGIN", "mu_q/G_AB not supplied"),
        ("RUN1554_4_cell_current", "cell-current kills reciprocal charge", "REFUSED_NO_CHARGE_OBSTRUCTION", "Q_R hair remains possible"),
        ("RUN1554_5_source_norm", "phase-volume supplies J_q and C_qm", "REFUSED_MISSING_PARENT_COUPLING_AND_NORM", "source current and norm still absent"),
        ("RUN1554_6_score_status", "local GR/Newton score", "REFUSED_NOT_SCORE_READY", "no parent origin accepted"),
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


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1554_0_origin_audit", "phase-volume origin audit", "PASS_NONCLAIM", "origin routes and obstructions are explicit"),
        ("GATE1554_1_radial_cell", "radial cell selects p=1", "PASS_CONDITIONAL_NONCLAIM", "algebraic selection only"),
        ("GATE1554_2_parent_origin", "parent phase-volume theorem", "BLOCKED", "separate radial cell conservation not derived"),
        ("GATE1554_3_qnorm", "positive q-norm E", "BLOCKED", "constraint/phase-volume route does not supply E"),
        ("GATE1554_4_source", "J_q matter source", "BLOCKED", "matter q-variation missing"),
        ("GATE1554_5_local_tests", "local arena claims", "BLOCKED_NO_CLAIM", "no local scoring from phase-volume motivation"),
        ("GATE1554_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "lambda/norm/source/tracefree gates remain open"),
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
        ("DEC1554_0_progress", "Phase-volume origin is clarified but not closed.", "MOTIVATED_NOT_DERIVED", "radial cell rule selects p=1 but is not a parent theorem"),
        ("DEC1554_1_closure", "Keep nonpropagating q=R_AB closure available but explicit.", "CLOSURE_ONLY", "it avoids hair but lacks lambda/norm/source origin"),
        ("DEC1554_2_next", "Next target is gauge/Noether zero-charge origin for q=R_AB.", "NEXT_1555_GAUGE_NOETHER_ORIGIN", "only a true gauge/no-charge theorem can kill Q_R without inserting the constraint"),
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
            "next_id": "NEXT1554_0_1555",
            "next_target": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
            "script": "scripts/Y5_gauge_noether_zero_charge_qsector_origin_audit.py",
            "objective": "test whether observer-splitting gauge symmetry or a Noether identity can force Q_R=0 and supply a nonpropagating q-sector origin without importing GR",
            "do_not": "do not treat coordinate gauge as physical proof; do not drop boundary charge; do not claim GR/Newton reduction",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ORIGIN_AUDIT, QUAR_ORIGIN),
        (QSECTOR_MAPPING, QUAR_MAPPING),
        (OBSTRUCTION_LEDGER, QUAR_OBSTRUCTION),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (ORIGIN_AUDIT, BRANCH_ORIGIN),
        (QSECTOR_MAPPING, BRANCH_MAPPING),
        (OBSTRUCTION_LEDGER, BRANCH_OBSTRUCTION),
        (RUNNER, BRANCH_RUNNER),
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
    origin_rows = read_csv(ORIGIN_AUDIT)
    mapping_rows = read_csv(QSECTOR_MAPPING)
    obstruction = read_csv(OBSTRUCTION_LEDGER)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1554_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1554 source paths exist"),
        ("VAL1554_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1554_2_origin_audit", any(row["origin_id"] == "ORG1554_5_current_verdict" and row["current_status"] == "NO_ACCEPTED_ORIGIN" for row in origin_rows), "phase-volume audit records no accepted origin"),
        ("VAL1554_3_mapping_nonclaim", any(row["map_id"] == "MAP1554_2_auxiliary_penalty" and row["current_status"] == "NOT_PARENT_DERIVED" for row in mapping_rows), "q-sector mapping remains nonclaim"),
        ("VAL1554_4_obstructions", len(obstruction) >= 7 and any(row["obstruction_id"] == "OBS1554_3_no_charge" for row in obstruction), "origin obstructions recorded"),
        ("VAL1554_5_runner_refuses_score", any(row["runner_id"] == "RUN1554_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in run_rows), "phase-volume runner refuses local scoring"),
        ("VAL1554_6_claim_gates_block", any(row["gate_id"] == "GATE1554_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1554_7_decision_next", any(row["result"] == "NEXT_1555_GAUGE_NOETHER_ORIGIN" for row in decision_items), "decision selects gauge/Noether zero-charge origin next"),
        ("VAL1554_8_next_target", any("1555-Y5-gauge-noether" in row["next_target"] for row in next_rows), "next target is gauge/Noether zero-charge q-sector origin audit"),
        ("VAL1554_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1554 CSVs parse cleanly"),
        ("VAL1554_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1554_11_branch_copies", all(path.exists() for path in [QUAR_ORIGIN, QUAR_MAPPING, QUAR_OBSTRUCTION, QUAR_RUNNER, QUAR_DECISION, BRANCH_ORIGIN, BRANCH_MAPPING, BRANCH_OBSTRUCTION, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1554_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1554_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1554_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1554 clarifies phase-volume as motivated not derived, keeps nonpropagating q-sector closure explicit, and selects gauge/Noether zero-charge origin next"
            if overall
            else "1554 validation failed; inspect failed rows before continuing",
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
    origin_rows: list[dict[str, Any]],
    mapping_rows: list[dict[str, Any]],
    obstruction: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1554 - Phase-Volume Nonpropagating q-sector Origin or Rejection",
                "",
                "## Verdict",
                "- Phase-volume/radial-cell balance motivates the nonpropagating q-sector route, but it does not yet derive the parent action or q-norm.",
                "- The radial cell rule `T sqrt(S)=1` still selects the GR scalar lane `p=1`; generic Liouville or canonical phase-volume preservation does not.",
                "- Mapping `q := R_AB = ln(T^2 S)` gives a clean closure variable, but the multiplier origin, positive q-norm, matter source current, and no-charge theorem remain missing.",
                "- A conserved cell current is not enough because it permits `Q_R/r` reciprocal hair unless a true zero-charge theorem exists.",
                "- Next target is a gauge/Noether zero-charge origin audit.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Phase-Volume Origin Audit",
                md_table(origin_rows, ["origin_id", "candidate_origin", "mathematical_form", "current_status", "failure_or_limit"]),
                "",
                "## q-sector Mapping",
                md_table(mapping_rows, ["map_id", "qsector_object", "role", "current_status", "blocker"]),
                "",
                "## Obstruction Ledger",
                md_table(obstruction, ["obstruction_id", "obstruction", "reason", "current_status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "check", "current_status", "reason"]),
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
    origin_rows = origin_audit_rows()
    mapping_rows = qsector_mapping_rows()
    obstruction = obstruction_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ORIGIN_AUDIT, origin_rows)
    write_csv(QSECTOR_MAPPING, mapping_rows)
    write_csv(OBSTRUCTION_LEDGER, obstruction)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ORIGIN_AUDIT,
        QSECTOR_MAPPING,
        OBSTRUCTION_LEDGER,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, origin_rows, mapping_rows, obstruction, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
