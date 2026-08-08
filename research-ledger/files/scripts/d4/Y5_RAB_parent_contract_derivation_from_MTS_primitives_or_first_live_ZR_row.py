from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB / "docs"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
RAB_QUEUE = RAB / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1567_doc": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
    "1567_validation": OUT / "P8_Y5_BRR545_1567_VALIDATION.csv",
    "1567_contract": OUT / "P8_Y5_PARENT_QLOC_1567_PARENT_PROTECTION_CONTRACT.csv",
    "1567_theorem": OUT / "P8_Y5_PARENT_QLOC_1567_CONDITIONAL_THEOREM.csv",
    "1567_acquisition": OUT / "P8_Y5_PARENT_QLOC_1567_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
    "1567_web": OUT / "P8_Y5_PARENT_QLOC_1567_WEB_SOURCE_REGISTER.csv",
    "1237_doc": ROOT / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md",
    "1237_primitive": OUT / "P8_Y5_R10_1237_MTS_PRIMITIVE_DERIVATION_AUDIT.csv",
    "1237_chain": OUT / "P8_Y5_R10_1237_SORTED_GRAMMAR_DERIVATION_CHAIN.csv",
    "1237_closure": OUT / "P8_Y5_R10_1237_CLOSURE_DEMOTION_LEDGER.csv",
    "1237_local": OUT / "P8_Y5_R10_1237_LOCAL_GR_CONNECTION_STATUS.csv",
    "1237_tests": OUT / "P8_Y5_R10_1237_FINITE_RESIDUAL_TEST_TRACK.csv",
    "1237_validation": OUT / "P8_Y5_BRR545_1237_VALIDATION.csv",
}

NEEDLES = {
    "1567_doc": ["The contract is not yet derived from MTS primitives", "fallback is now live but nonclaim"],
    "1567_validation": ["VAL1567_OVERALL", "PASS"],
    "1567_contract": ["CON1567_6_joint_contract", "CONTRACT_WRITTEN_NOT_SIGNED"],
    "1567_theorem": ["THM1567_0_statement", "EXACT_IF_CONTRACT_PARENT_SIGNED"],
    "1567_acquisition": ["ACQ1567_1_ZR", "MISSING_ZR_THEOREM_OR_COEFFICIENT"],
    "1567_web": ["WEB1567_R10_EOTWASH_PRL_2021", "EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM"],
    "1237_doc": ["does **not** derive the sorted parent action grammar", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED"],
    "1237_primitive": ["PRIM1237_8_verdict", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED"],
    "1237_chain": ["CHAIN1237_7_verdict", "FAIL_DEMOTE_TO_CLOSURE"],
    "1237_closure": ["CLOSE1237_0_typed_object_language", "EXPLICIT_CLOSURE_ASSUMPTION"],
    "1237_local": ["LGR1237_5_verdict", "NOT_DERIVED"],
    "1237_tests": ["TEST1237_0_QR_hair", "FINITE_RESIDUAL_REQUIRED_UNLESS_FIRST_CLASS_CONSTRAINT"],
    "1237_validation": ["VAL1237_12_overall", "PASS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1568_SOURCE_REGISTER.csv"
PRIMITIVE_RECHECK = OUT / "P8_Y5_PARENT_QLOC_1568_PRIMITIVE_DERIVATION_RECHECK.csv"
CONTRACT_GAP = OUT / "P8_Y5_PARENT_QLOC_1568_CONTRACT_TO_PRIMITIVE_GAP.csv"
FIRST_BOUND_ROW = OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv"
FIRST_COEFF_STATUS = OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv"
QUEUE_COPY = RAB_QUEUE / "ZR1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1568_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1568_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1568_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1568_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1568_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1568"
COPY_TARGETS = {
    PRIMITIVE_RECHECK: [
        QUARANTINE / "PRIMITIVE_DERIVATION_RECHECK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "primitive_derivation_recheck_nonclaim_1568.csv",
    ],
    CONTRACT_GAP: [
        QUARANTINE / "CONTRACT_TO_PRIMITIVE_GAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "contract_to_primitive_gap_nonclaim_1568.csv",
    ],
    FIRST_BOUND_ROW: [
        QUARANTINE / "FIRST_EXTERNAL_BOUND_SOURCE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "first_external_bound_source_row_nonclaim_1568.csv",
        QUEUE_COPY,
    ],
    FIRST_COEFF_STATUS: [
        QUARANTINE / "FIRST_INTERNAL_COEFFICIENT_ROW_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "first_internal_coefficient_row_status_nonclaim_1568.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "parent_contract_derivation_decision_nonclaim_1568.csv",
    ],
}


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
        "ready_for_raw",
        "ready_for_accepted",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1568_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "primitive derivation recheck or first external bound source row",
                **flags(),
            }
        )
    return rows


def primitive_recheck_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PRIM1568_0_motion_load",
            "motion-load/local observer scaffold",
            "partial Q_obs and Newtonian-lane support",
            "DOES_NOT_DERIVE_CONTRACT",
            "does not yield typed parent action exhaustion, matter descent, boundary silence, readout closure, or operator exclusion",
        ),
        (
            "PRIM1568_1_reciprocity",
            "R_AB=0/local reciprocity route",
            "useful local-GR closure benchmark",
            "CLOSURE_ONLY_CURRENT_STATE",
            "1237 records R_AB=0 as not parent-derived",
        ),
        (
            "PRIM1568_2_typed_grammar",
            "sorted parent object language",
            "exact rule that would protect coefficients",
            "SCHEMA_VALID_NOT_PRIMITIVE_DERIVED",
            "1236/1237 make the contract precise but not fundamental",
        ),
        (
            "PRIM1568_3_parent_contract",
            "CON1567_0-5",
            "jointly sufficient local protection contract",
            "DERIVATION_FAILS_CURRENT_EVIDENCE",
            "1237 already proves the primitive route fails for sorted grammar",
        ),
        (
            "PRIM1568_4_verdict",
            "derive contract from MTS primitives",
            "not achieved",
            "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL",
            "do not spend theorem-zero credit from the contract",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "recheck_id": recheck_id,
            "primitive_route": primitive_route,
            "what_it_supplies": what_it_supplies,
            "result": result,
            "reason": reason,
            "source_paths": source_list("1237_doc", "1237_primitive", "1237_chain", "1567_contract"),
            **flags(),
        }
        for recheck_id, primitive_route, what_it_supplies, result, reason in rows
    ]


def contract_gap_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAP1568_0_sorts", "typed parent sorts", "CON1567_0", "CHAIN1237_1/2 hidden-visible disjointness and visible coefficient domain fail", "MISSING_PRIMITIVE_SORT_DERIVATION"),
        ("GAP1568_1_action_image", "ParentGenerate image exhaustion", "CON1567_1", "CHAIN1237_6 total parent action fails", "MISSING_TOTAL_PARENT_ACTION"),
        ("GAP1568_2_matter", "J_R=0 matter descent", "CON1567_2", "CHAIN1237_5 source-label forgetting fails", "MISSING_MATTER_CATEGORY_DERIVATION"),
        ("GAP1568_3_boundary", "B_R=Pi_Rn=0 boundary descent", "CON1567_3", "1237 does not derive boundary/corner silence", "MISSING_BOUNDARY_GRAMMAR"),
        ("GAP1568_4_readout", "readout/radiative closure", "CON1567_4", "CHAIN1237_4 readout/radiative closure fails", "MISSING_READOUT_CLOSURE"),
        ("GAP1568_5_operator", "Z_R derivative operator exclusion", "CON1567_5", "CHAIN1237_2/6 and 1269 keep operator exclusion conditional", "MISSING_OPERATOR_EXHAUSTION"),
        ("GAP1568_6_joint", "local-GR second-class protection package", "CON1567_6", "any missing gap leaves finite residual route live", "FAILED_CURRENT_PARENT_PROOF"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gap_id": gap_id,
            "needed_contract_piece": needed_contract_piece,
            "contract_clause": contract_clause,
            "current_evidence": current_evidence,
            "status": status,
            "source_paths": source_list("1237_chain", "1237_local", "1567_contract"),
            **flags(),
        }
        for gap_id, needed_contract_piece, contract_clause, current_evidence, status in rows
    ]


def first_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "BOUND1568_R10_EOTWASH_PRL_2021",
            "row_type": "external_arena_bound_only",
            "arena": "R10",
            "quantity": "alpha(lambda) Yukawa bound",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.126.211101",
            "source_title": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Scale",
            "source_anchor": "strongest bound on the magnitude alpha of Yukawa-type deviations in the range of 5-500 mm",
            "local_source_path": "NOT_DOWNLOADED_THIS_CHECKPOINT",
            "extraction_status": "SOURCE_URL_IDENTIFIED_NEEDS_LOCAL_DIGITIZATION_OR_TABLE",
            "why_not_scoreable": "external bound is not an MTS Z_R/J_R/B_R/tau coefficient and no MTS projection kernel is supplied",
            "external_reference_status": "WEB_SOURCE_IDENTIFIED_NONCLAIM",
            **flags(),
        }
    ]


def first_coeff_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("COEFF1568_0_ZR", "Z_R", "no theorem-zero and no numeric parent coefficient", "MISSING_INTERNAL_COEFFICIENT"),
        ("COEFF1568_1_JR", "J_R", "matter descent not derived and no finite source-current row", "MISSING_INTERNAL_COEFFICIENT"),
        ("COEFF1568_2_BR", "B_R_or_Pi_Rn", "boundary silence not derived and no finite boundary row", "MISSING_INTERNAL_COEFFICIENT"),
        ("COEFF1568_3_tau_R10", "tau_R10", "external R10 bound source exists, but no MTS residual-to-alpha projection kernel", "MISSING_PROJECTION_KERNEL"),
        ("COEFF1568_4_verdict", "first live MTS finite row", "not filled; only first external bound-source row queued", "NO_INTERNAL_ROW_READY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "current_evidence": current_evidence,
            "status": status,
            "source_paths": source_list("1567_acquisition", "1567_web", "1237_tests"),
            **flags(),
        }
        for status_id, target, current_evidence, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1568_0_sources", "load 1567 and 1237 evidence", "PASS", "all registered sources loaded"),
        ("RUN1568_1_primitive_contract", "derive contract from primitives", "FAILED_CURRENT_PARENT_PROOF", "1237 already demotes sorted grammar to closure"),
        ("RUN1568_2_first_bound", "first external bound source row", "PASS_NONCLAIM_SOURCE_URL_ROW", "R10 PRL source URL queued but not digitized/localized"),
        ("RUN1568_3_first_internal_coeff", "first internal MTS coefficient row", "NO_INTERNAL_ROW_READY", "Z_R/J_R/B_R/tau remain missing"),
        ("RUN1568_4_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1568_5_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "contract derivation failed and first bound row is external-only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1568_0_primitive_contract", "contract derived from MTS primitives", "BLOCKED_NO_CLAIM", "1237 current-state evidence says derivation fails and demotes to closure"),
        ("GATE1568_1_theorem_zero", "J_R=B_R=readout_regen=Z_R=0", "BLOCKED_NO_CLAIM", "zero theorem depends on unsigned contract"),
        ("GATE1568_2_first_bound", "external R10 bound row", "PASS_SOURCE_QUEUE_NONCLAIM", "source URL queued but not connected to MTS coefficient"),
        ("GATE1568_3_first_coeff", "first internal finite residual coefficient row", "BLOCKED_NO_CLAIM", "no internal source-backed coefficient/projection row exists"),
        ("GATE1568_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED_NO_CLAIM", "neither theorem-zero nor finite residual scoring is ready"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1237_doc", "1567_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1568_0_derivation",
            "decision": "derive contract from primitives",
            "result": "FAILED_CURRENT_EVIDENCE_REUSE_1237",
            "reason": "1237 already tested the primitive route and demoted sorted grammar to closure",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1568_1_bound",
            "decision": "first source row",
            "result": "FIRST_EXTERNAL_BOUND_ROW_QUEUED_NONCLAIM",
            "reason": "R10 bound source URL is identified but not a MTS finite coefficient/projection",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1568_2_coeff",
            "decision": "first internal coefficient row",
            "result": "NOT_READY",
            "reason": "Z_R/J_R/B_R/tau need parent theorem-zero or source-backed projections",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1568_3_next",
            "decision": "next target",
            "result": "NEXT_1569_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW",
            "reason": "the next executable step is either Z_R theorem-zero/finite coefficient or tau_R10 projection kernel linked to the R10 bound",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1568_0_1569",
            "next_target": "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md",
            "script": "scripts/Y5_RAB_first_internal_ZR_or_tauR10_projection_row.py",
            "objective": "try to fill the first internal nonclaim row: either theorem-zero/numeric Z_R from parent grammar, or a tau_R10 projection kernel connecting finite R_AB residuals to the external R10 alpha(lambda) bound row",
            "do_not": "do not treat external bounds as MTS coefficients; do not move rows to accepted until local source path, source anchor, units, normalization, and projection are real; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
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
    recheck = read_csv(PRIMITIVE_RECHECK)
    gaps = read_csv(CONTRACT_GAP)
    bound = read_csv(FIRST_BOUND_ROW)
    coeff = read_csv(FIRST_COEFF_STATUS)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1568_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1568 source paths exist"),
        ("VAL1568_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1568_2_primitive_derivation_fails", any(row["recheck_id"] == "PRIM1568_4_verdict" and row["result"] == "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL" for row in recheck), "primitive derivation is refused"),
        ("VAL1568_3_contract_gaps", len(gaps) >= 7 and any(row["gap_id"] == "GAP1568_6_joint" and row["status"] == "FAILED_CURRENT_PARENT_PROOF" for row in gaps), "contract-to-primitive gaps are explicit"),
        ("VAL1568_4_first_external_bound", any(row["row_id"] == "BOUND1568_R10_EOTWASH_PRL_2021" and row["row_type"] == "external_arena_bound_only" for row in bound), "first external bound row queued"),
        ("VAL1568_5_no_internal_coeff", any(row["status_id"] == "COEFF1568_4_verdict" and row["status"] == "NO_INTERNAL_ROW_READY" for row in coeff), "no internal coefficient row is ready"),
        ("VAL1568_6_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1568_7_runner_blocks_claim", any(row["runner_id"] == "RUN1568_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1568_8_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1568_9_decision_next", any(row["result"] == "NEXT_1569_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW" for row in decision_items), "decision selects first internal ZR or tau_R10 row"),
        ("VAL1568_10_next_target", any("1569-Y5-RAB-first-internal-ZR" in row["next_target"] for row in next_rows), "next target is first internal ZR/tauR10 row"),
        ("VAL1568_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1568 CSVs parse cleanly"),
        ("VAL1568_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1568_13_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1568_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1568_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1568_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1568 parent contract derivation from MTS primitives or first live ZR row validation",
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
    recheck: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    coeff: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1568 - R_AB Parent Contract Derivation from MTS Primitives or First Live Z_R Row",
                "",
                "## Verdict",
                "- The parent-protection contract from 1567 cannot currently be derived from MTS primitives: 1237 already tested this route and demoted the sorted grammar to explicit closure.",
                "- This does not kill the route; it changes its status. The contract is a clean target theorem or closure benchmark, not local-GR evidence.",
                "- The first external bound source row is now queued for R10, but it is only an arena-bound source, not an MTS coefficient or projection kernel.",
                "- No internal `Z_R`, `J_R`, `B_R`, or `tau_R10` row is source-ready.",
                "- No `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, WEP, clock, or orbital claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Primitive Derivation Recheck",
                md_table(recheck, ["recheck_id", "primitive_route", "what_it_supplies", "result", "reason"]),
                "",
                "## Contract To Primitive Gap",
                md_table(gaps, ["gap_id", "needed_contract_piece", "contract_clause", "current_evidence", "status"]),
                "",
                "## First External Bound Source Row",
                md_table(bound, ["row_id", "row_type", "arena", "quantity", "source_url", "source_title", "extraction_status", "why_not_scoreable"]),
                "",
                "## First Internal Coefficient Row Status",
                md_table(coeff, ["status_id", "target", "current_evidence", "status"]),
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
    recheck = primitive_recheck_rows()
    gaps = contract_gap_rows()
    bound = first_bound_rows()
    coeff = first_coeff_status_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PRIMITIVE_RECHECK, recheck)
    write_csv(CONTRACT_GAP, gaps)
    write_csv(FIRST_BOUND_ROW, bound)
    write_csv(FIRST_COEFF_STATUS, coeff)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PRIMITIVE_RECHECK,
        CONTRACT_GAP,
        FIRST_BOUND_ROW,
        FIRST_COEFF_STATUS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, recheck, gaps, bound, coeff, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
