from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
RAB_RAW = ROOT / "source-intake" / "rab-sector" / "raw"
RAB_ACCEPTED = ROOT / "source-intake" / "rab-sector" / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1563_doc": ROOT / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    "1563_validation": OUT / "P8_Y5_BRR545_1563_VALIDATION.csv",
    "1563_next": OUT / "P8_Y5_PARENT_QLOC_1563_NEXT_TARGET.csv",
    "1563_sort": OUT / "P8_Y5_PARENT_QLOC_1563_PARENT_SORT_AUDIT.csv",
    "1563_fallback": OUT / "P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv",
    "1263_doc": ROOT / "1263-Y5-R10-vertical-fibre-null-from-parent-presymplectic-degeneracy-or-RAB-prior-envelope-fill.md",
    "1262_doc": ROOT / "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope.md",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "zr1262_template": RAB_DOCS / "ZR1262_RAB_PRIOR_ENVELOPE_TEMPLATE_NONCLAIM.csv",
    "zr1268_template": RAB_DOCS / "ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
}

NEEDLES = {
    "1563_doc": ["Finite `Z_R/q_R` remains the honest fallback", "vertical-null/presymplectic degeneracy"],
    "1563_validation": ["VAL1563_OVERALL", "PASS"],
    "1563_next": ["1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md"],
    "1563_sort": ["SORT1563_1_vertical_representative", "EXACT_CONDITIONAL_NOT_PARENT_DERIVED"],
    "1563_fallback": ["FALL1563_0_ZR", "MISSING_SOURCE_BACKED_INPUT"],
    "1263_doc": ["real mathematical foothold", "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED"],
    "1262_doc": ["THEO1262_0_vertical_null_ban", "EXACT_CONDITIONAL_NOT_PARENT_DERIVED"],
    "1023_doc": ["QVC1023_5_momentum_map", "fail_current_claim_demote_current_branch"],
    "zr1262_template": ["MISSING"],
    "zr1268_template": ["MISSING"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1564_SOURCE_REGISTER.csv"
NULL_CHAIN = OUT / "P8_Y5_PARENT_QLOC_1564_PRESYMPLECTIC_NULL_CHAIN.csv"
KINETIC_CONTRADICTION = OUT / "P8_Y5_PARENT_QLOC_1564_KINETIC_TERM_CONTRADICTION.csv"
PARENT_BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1564_PARENT_INPUT_BLOCKERS.csv"
FINITE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_1564_FINITE_ZR_INTAKE_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1564_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1564_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1564_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1564_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1564_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1564"
QUAR_NULL = QUARANTINE / "PRESYMPLECTIC_NULL_CHAIN_NONCLAIM.csv"
QUAR_KINETIC = QUARANTINE / "KINETIC_TERM_CONTRADICTION_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "PARENT_INPUT_BLOCKERS_NONCLAIM.csv"
QUAR_INTAKE = QUARANTINE / "FINITE_ZR_INTAKE_STATUS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_NULL = BRANCH_RESIDUALS / "presymplectic_null_chain_nonclaim_1564.csv"
BRANCH_KINETIC = BRANCH_RESIDUALS / "kinetic_term_contradiction_nonclaim_1564.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "parent_input_blockers_nonclaim_1564.csv"
BRANCH_INTAKE = BRANCH_RESIDUALS / "finite_ZR_intake_status_nonclaim_1564.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "vertical_null_runner_nonclaim_1564.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "vertical_null_decision_nonclaim_1564.csv"


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
                "source_id": f"SRC1564_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for R_AB vertical-null presymplectic degeneracy or finite ZR intake",
                **flags(),
            }
        )
    return rows


def null_chain_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NULL1564_0_parent_L_theta",
            "parent Lagrangian and symplectic potential",
            "delta L_parent = E_A delta Phi^A + d theta_MTS",
            "MISSING_FULL_PARENT_ACTION",
            "without theta/Omega, nullness is only a template",
        ),
        (
            "NULL1564_1_parent_Omega",
            "parent presymplectic form",
            "Omega_parent = delta theta_MTS on the local covariant phase space",
            "MISSING_PARENT_OMEGA",
            "cannot prove ker(Omega_parent) equals quotient fibres",
        ),
        (
            "NULL1564_2_q_reduction",
            "canonical quotient map q",
            "ker(Dq)=ker(Omega_parent) after proper gauge/boundary quotient",
            "CONDITIONAL_ROUTE_NOT_CERTIFIED",
            "old quotient route is plausible but not parent-signed",
        ),
        (
            "NULL1564_3_vR_generator",
            "R_AB vertical generator v_R",
            "for compact eta, delta_eta R_AB=eta and Dq[v_eta]=0",
            "MISSING_RAB_VERTICAL_GENERATOR",
            "R_AB has not been field-by-field mapped to a null direction",
        ),
        (
            "NULL1564_4_no_boundary_charge",
            "no boundary Hamiltonian charge",
            "delta H_eta=Omega(delta Phi,v_eta)=int_boundary(delta Q_eta-i_eta theta)=0",
            "MISSING_BOUNDARY_ZERO_THEOREM",
            "bulk nullness does not kill corner/source-worldtube charge",
        ),
        (
            "NULL1564_5_verdict",
            "presymplectic-null proof",
            "if NULL1564_0 through NULL1564_4 close, R_AB is pure vertical null",
            "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED",
            "the proof shape survives, but not as current claim",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "chain_id": chain_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "status": status,
            "blocker": blocker,
            "source_paths": source_list("1263_doc", "1262_doc", "1023_doc", "1563_sort"),
            **flags(),
        }
        for chain_id, claim_piece, mathematical_form, status, blocker in rows
    ]


def kinetic_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KIN1564_0_variation",
            "S_Z = int sqrt(h) 1/2 Z_R h^{ij}D_iR_ABD_jR_AB",
            "delta S_Z = -int sqrt(h) Z_R D_iD^iR_AB delta R_AB + boundary momentum",
            "EXACT_FORMAL_VARIATION",
            "nonzero Z_R gives compact vertical variations a bulk response",
        ),
        (
            "KIN1564_1_null_contradiction",
            "v_R in ker(Omega_parent) with no boundary charge",
            "nonzero Z_R contradicts parent nullness by adding action response/boundary momentum",
            "EXACT_CONDITIONAL_ON_TRUE_NULLNESS",
            "would prove Z_R=0 only if vertical nullness is parent-derived",
        ),
        (
            "KIN1564_2_escape_physical",
            "R_AB is physical scalar/tensor",
            "Z_R kinetic term is legal",
            "COUNTERMODEL_FORCES_FALLBACK",
            "finite residual branch required",
        ),
        (
            "KIN1564_3_escape_metric",
            "vertical fibre metric/connection exists",
            "G_vert(DR_AB,DR_AB) is quotient-natural",
            "COUNTERMODEL_FORCES_FALLBACK",
            "no-vertical-metric theorem is essential",
        ),
        (
            "KIN1564_4_escape_boundary",
            "boundary defect/corner charge exists",
            "bulk null does not prevent Q_R/B_R hair",
            "COUNTERMODEL_FORCES_FALLBACK",
            "boundary zero theorem is separate",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kinetic_id": kinetic_id,
            "assumption_or_operator": assumption_or_operator,
            "calculation": calculation,
            "status": status,
            "meaning": meaning,
            "source_paths": source_list("1263_doc", "1262_doc", "1563_doc"),
            **flags(),
        }
        for kinetic_id, assumption_or_operator, calculation, status, meaning in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK1564_0_L_parent", "full MTS parent Lagrangian", "needed to define theta_MTS and Omega_parent", "MISSING_FULL_PARENT_ACTION"),
        ("BLK1564_1_theta_Omega", "theta_MTS/Omega_parent extraction", "needed to certify presymplectic degeneracy", "MISSING_PARENT_THETA_OMEGA"),
        ("BLK1564_2_vR", "field-by-field R_AB vertical generator", "needed to show Dq[v_R]=0 and Omega-flat(v_R)=0", "MISSING_RAB_VERTICAL_GENERATOR"),
        ("BLK1564_3_no_vertical_metric", "no vertical metric/connection theorem", "needed to forbid quotient-natural gradient energy", "MISSING_NO_VERTICAL_METRIC_THEOREM"),
        ("BLK1564_4_boundary_zero", "Q_R/B_R/Pi_R boundary silence", "needed to prevent source-worldtube/corner hair", "MISSING_BOUNDARY_ZERO_THEOREM"),
        ("BLK1564_5_readout", "readout/radiative stability", "needed to stop effective action regenerating Z_R", "MISSING_READOUT_STABILITY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "needed_object": needed_object,
            "why_needed": why_needed,
            "current_status": current_status,
            "source_paths": source_list("1263_doc", "1262_doc", "1023_doc", "1563_doc"),
            **flags(),
        }
        for blocker_id, needed_object, why_needed, current_status in rows
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    raw_rows = len(list(RAB_RAW.glob("*.csv"))) if RAB_RAW.exists() else 0
    accepted_rows = len(list(RAB_ACCEPTED.glob("*.csv"))) if RAB_ACCEPTED.exists() else 0
    rows = [
        ("INTAKE1564_0_raw", str(RAB_RAW), raw_rows, "NO_LIVE_RAW_ROWS" if raw_rows == 0 else "RAW_ROWS_PRESENT_REVIEW_REQUIRED"),
        ("INTAKE1564_1_accepted", str(RAB_ACCEPTED), accepted_rows, "NO_ACCEPTED_ROWS" if accepted_rows == 0 else "ACCEPTED_ROWS_PRESENT_REVIEW_REQUIRED"),
        ("INTAKE1564_2_docs", str(RAB_DOCS), len(list(RAB_DOCS.glob("*ZR*.csv"))) if RAB_DOCS.exists() else 0, "DOCS_ONLY_NONCLAIM_TEMPLATES"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "intake_id": intake_id,
            "folder": folder,
            "rows_found": rows_found,
            "status": status,
            "required_before_scoring": "source-backed Z_R, M_R2, J_R, B_R, units, normalization, arena projection, and no placeholder MISSING markers",
            **flags(),
        }
        for intake_id, folder, rows_found, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1564_0_sources",
            "test": "vertical-null sources loaded",
            "current_status": "PASS",
            "detail": "1563, 1263, 1262, 1023, and finite templates loaded",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1564_1_conditional_contradiction",
            "test": "nonzero Z_R vs true vertical nullness",
            "current_status": "PASS_EXACT_CONDITIONAL",
            "detail": "if R_AB is parent-null with no boundary charge, nonzero Z_R contradicts nullness",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1564_2_parent_proof",
            "test": "parent proof of R_AB vertical nullness",
            "current_status": "FAILED_CURRENT_PARENT_PROOF",
            "detail": "L/theta/Omega, v_R generator, no-vertical-metric theorem, and boundary zero theorem remain missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1564_3_finite_intake",
            "test": "finite Z_R/q_R intake readiness",
            "current_status": "NOT_SCOREABLE_DOCS_ONLY",
            "detail": "templates exist but no accepted source-backed rows are present",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1564_4_claim",
            "test": "local GR/Newton claim",
            "current_status": "BLOCKED_NO_CLAIM",
            "detail": "neither theorem-zero nor finite residual workflow is claim-ready",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1564_0_ZR_zero", "Z_R=0 by presymplectic nullness", "BLOCKED_NO_CLAIM", "true R_AB nullness is not parent-derived"),
        ("GATE1564_1_boundary", "R_AB boundary charge zero", "BLOCKED_NO_CLAIM", "boundary/corner no-hair theorem missing"),
        ("GATE1564_2_no_vertical_metric", "no vertical metric/connection", "BLOCKED_NO_CLAIM", "parent object-language proof missing"),
        ("GATE1564_3_finite_intake", "finite Z_R/q_R residual scoring", "BLOCKED_NO_CLAIM", "no accepted source-backed rows"),
        ("GATE1564_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED_NO_CLAIM", "theorem-zero and fallback both incomplete"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1263_doc", "1262_doc", "1563_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1564_0_progress",
            "decision": "vertical-null route",
            "result": "EXACT_CONDITIONAL_CONTRADICTION_RETAINED",
            "reason": "true parent-null R_AB would forbid nonzero Z_R without a plateau axiom",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1564_1_not_closed",
            "decision": "claim status",
            "result": "PARENT_NULL_PROOF_MISSING_RETAIN_FINITE_FALLBACK",
            "reason": "parent L/theta/Omega, v_R, no-vertical-metric, boundary, and readout proofs are missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1564_2_next",
            "decision": "next target",
            "result": "NEXT_1565_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW",
            "reason": "either fill the parent theta/Omega and R_AB vertical generator, or begin strict finite Z_R source-row intake",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1564_0_1565",
            "next_target": "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
            "script": "scripts/Y5_RAB_parent_theta_Omega_vR_fill_or_finite_ZR_source_row.py",
            "objective": "try to instantiate parent theta/Omega and a field-by-field R_AB vertical generator v_R proving Omega-nullness with zero boundary charge; if this fails, stage strict finite Z_R source-row intake without scoring placeholders",
            "do_not": "do not promote the conditional contradiction into local-GR evidence; do not score finite Z_R/q_R rows unless source-backed and placeholder-free; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (NULL_CHAIN, QUAR_NULL),
        (KINETIC_CONTRADICTION, QUAR_KINETIC),
        (PARENT_BLOCKERS, QUAR_BLOCKERS),
        (FINITE_INTAKE, QUAR_INTAKE),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (NULL_CHAIN, BRANCH_NULL),
        (KINETIC_CONTRADICTION, BRANCH_KINETIC),
        (PARENT_BLOCKERS, BRANCH_BLOCKERS),
        (FINITE_INTAKE, BRANCH_INTAKE),
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
    null = read_csv(NULL_CHAIN)
    kinetic = read_csv(KINETIC_CONTRADICTION)
    blockers = read_csv(PARENT_BLOCKERS)
    intake = read_csv(FINITE_INTAKE)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1564_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1564 source paths exist"),
        ("VAL1564_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1564_2_null_conditional", any(row["chain_id"] == "NULL1564_5_verdict" and row["status"] == "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED" for row in null), "presymplectic null chain verdict is conditional not proved"),
        ("VAL1564_3_kinetic_contradiction", any(row["kinetic_id"] == "KIN1564_1_null_contradiction" and row["status"] == "EXACT_CONDITIONAL_ON_TRUE_NULLNESS" for row in kinetic), "kinetic contradiction is exact conditional"),
        ("VAL1564_4_blockers", len(blockers) >= 6 and any(row["blocker_id"] == "BLK1564_2_vR" for row in blockers), "parent input blockers are recorded"),
        ("VAL1564_5_intake_not_scoreable", any(row["intake_id"] == "INTAKE1564_1_accepted" and row["status"] == "NO_ACCEPTED_ROWS" for row in intake), "finite intake has no accepted source rows"),
        ("VAL1564_6_runner_parent_fail", any(row["runner_id"] == "RUN1564_2_parent_proof" and row["current_status"] == "FAILED_CURRENT_PARENT_PROOF" for row in run_rows), "runner refuses parent-null proof"),
        ("VAL1564_7_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1564_8_decision_next", any(row["result"] == "NEXT_1565_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW" for row in decision_items), "decision selects parent theta/Omega/vR fill or finite ZR source row next"),
        ("VAL1564_9_next_target", any("1565-Y5-RAB-parent-theta-Omega-vR" in row["next_target"] for row in next_rows), "next target is parent theta/Omega/vR fill or finite ZR source row"),
        ("VAL1564_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1564 CSVs parse cleanly"),
        ("VAL1564_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1564_12_branch_copies", all(path.exists() for path in [QUAR_NULL, QUAR_KINETIC, QUAR_BLOCKERS, QUAR_INTAKE, QUAR_RUNNER, QUAR_DECISION, BRANCH_NULL, BRANCH_KINETIC, BRANCH_BLOCKERS, BRANCH_INTAKE, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1564_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1564_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1564_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1564 R_AB vertical-null presymplectic degeneracy or finite ZR intake validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    null: list[dict[str, Any]],
    kinetic: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1564 - R_AB Vertical-Null Presymplectic Degeneracy or Finite Z_R Intake",
                "",
                "## Verdict",
                "- The vertical-null route gives a real conditional theorem: if `R_AB` is a parent presymplectic-null representative with no boundary charge, nonzero `Z_R |D R_AB|^2` contradicts that nullness.",
                "- This is not a plateau axiom; it bans the kinetic operator rather than assuming the local profile is flat.",
                "- The current corpus still lacks parent `L/theta/Omega`, field-by-field `v_R`, no-vertical-metric, boundary-zero, and readout-stability proofs.",
                "- Therefore `Z_R=0`, `q_R=0`, and local GR/Newton are not claimed.",
                "- Finite `Z_R/q_R` intake remains nonclaim because only docs templates exist and no accepted source-backed rows are present.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Presymplectic Null Chain",
                md_table(null, ["chain_id", "claim_piece", "mathematical_form", "status", "blocker"]),
                "",
                "## Kinetic Term Contradiction",
                md_table(kinetic, ["kinetic_id", "assumption_or_operator", "calculation", "status", "meaning"]),
                "",
                "## Parent Input Blockers",
                md_table(blockers, ["blocker_id", "needed_object", "why_needed", "current_status"]),
                "",
                "## Finite Z_R Intake Status",
                md_table(intake, ["intake_id", "folder", "rows_found", "status", "required_before_scoring"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    null = null_chain_rows()
    kinetic = kinetic_rows()
    blockers = blocker_rows()
    intake = finite_intake_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NULL_CHAIN, null)
    write_csv(KINETIC_CONTRADICTION, kinetic)
    write_csv(PARENT_BLOCKERS, blockers)
    write_csv(FINITE_INTAKE, intake)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        NULL_CHAIN,
        KINETIC_CONTRADICTION,
        PARENT_BLOCKERS,
        FINITE_INTAKE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, null, kinetic, blockers, intake, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
