from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2223-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_QMAP_CQM_GATE_2223"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2222_doc": ROOT / "2222-Y5-R2FR-current-local-frontier-import-and-Jsrc-Binner-source-bound-gate.md",
    "2222_validation": OUT / "P8_Y5_BRR545_2222_VALIDATION.csv",
    "2222_coupling": OUT / "P8_Y5_PARENT_QLOC_2222_COUPLING_SELECTOR_IMPORT_GATE.csv",
    "2222_next": OUT / "P8_Y5_PARENT_QLOC_2222_NEXT_TARGET.csv",
    "1541_doc": ROOT / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
    "1541_validation": OUT / "P8_Y5_BRR545_1541_VALIDATION.csv",
    "1541_qmap": OUT / "P8_Y5_PARENT_QLOC_1541_QMAP_CANDIDATE_LEDGER.csv",
    "1541_vgen": OUT / "P8_Y5_PARENT_QLOC_1541_VERTICAL_GENERATOR_AUDIT.csv",
    "1541_kernel": OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
    "1541_coupling": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "1542_doc": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
    "1542_validation": OUT / "P8_Y5_BRR545_1542_VALIDATION.csv",
    "1542_qdef": OUT / "P8_Y5_PARENT_QLOC_1542_Q_DEFINITION_AUDIT.csv",
    "1542_vmdef": OUT / "P8_Y5_PARENT_QLOC_1542_VM_DEFINITION_AUDIT.csv",
    "1542_cqm": OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv",
    "1542_scg": OUT / "P8_Y5_PARENT_QLOC_1542_SCG_RUNNER_NONCLAIM.csv",
    "1543_doc": ROOT / "1543-Y5-Cqm-source-norm-local-projection-pack.md",
    "1543_validation": OUT / "P8_Y5_BRR545_1543_VALIDATION.csv",
    "1543_inputs": OUT / "P8_Y5_PARENT_QLOC_1543_FINITE_INPUT_PROVENANCE_PACK.csv",
    "1543_arenas": OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv",
    "1543_runner": OUT / "P8_Y5_PARENT_QLOC_1543_PROJECTION_RUNNER_NONCLAIM.csv",
    "1544_doc": ROOT / "1544-Y5-Cqm-zero-theorem-or-finite-provenance-runner.md",
    "1544_validation": OUT / "P8_Y5_BRR545_1544_VALIDATION.csv",
    "1544_zero": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_ZERO_THEOREM_AUDIT.csv",
    "1544_provenance": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_FINITE_PROVENANCE_REQUIREMENTS.csv",
    "1544_dry": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_DRY_RUNNER_NONCLAIM.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "1545_doc": ROOT / "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2223_SOURCE_REGISTER.csv"
FRONTIER_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2223_QMAP_CQM_FRONTIER_IMPORT.csv"
QMAP_KERNEL_GATE = OUT / "P8_Y5_PARENT_QLOC_2223_QMAP_VERTICAL_KERNEL_GATE.csv"
CQM_RESIDUAL_GATE = OUT / "P8_Y5_PARENT_QLOC_2223_CQM_FINITE_RESIDUAL_GATE.csv"
PROJECTION_GATE = OUT / "P8_Y5_PARENT_QLOC_2223_LOCAL_PROJECTION_BLOCKER_GATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2223_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2223_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2223_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2223_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2223_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2223_QMAP_CQM_FRONTIER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "qmap_cqm_frontier_nonclaim_2223.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_QMAP_CQM_FRONTIER_2223_NONCLAIM.csv",
}


def flags() -> dict[str, bool]:
    return {
        "kernel_proved": False,
        "theorem_zero_adopted": False,
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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "kernel_proved",
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2223_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2223" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "input evidence"
        if key.startswith("2222"):
            role = "current source-boundary handoff selecting q/Dq[v_m]"
        elif key.startswith("1541"):
            role = "q-map/v_m kernel certificate and finite coupling row"
        elif key.startswith("1542"):
            role = "q-definition fork and finite C_qm source pack"
        elif key.startswith("1543"):
            role = "finite C_qm local projection/source-norm pack"
        elif key.startswith("1544"):
            role = "C_qm zero theorem rejection and provenance gate"
        elif key.startswith("1545"):
            role = "known next source-norm/direct residual provenance frontier"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2223_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def frontier_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "FRONT2223_0_1541",
            "1541 q-map/v_m kernel certificate",
            "Dq[v_m]=0 not proved; finite C_qm/S_cg coupling row staged",
            "IMPORT_AS_KERNEL_FAILURE_AND_FINITE_FALLBACK",
            "q_loc and v_m not jointly parent-signed",
        ),
        (
            "FRONT2223_1_1542",
            "1542 q-definition fork",
            "post-hoc q deletion rejected; exact kernel fails current evidence; finite C_qm source pack selected",
            "IMPORT_AS_WORK_ROUTE",
            "C_qm inputs named but missing",
        ),
        (
            "FRONT2223_2_1543",
            "1543 projection pack",
            "finite route is arena-shaped for R10/PPN/clock/orbital, but all projections remain noncomputable",
            "IMPORT_AS_TEST_SHAPE_NONCLAIM",
            "source-side inputs and projection matrices missing",
        ),
        (
            "FRONT2223_3_1544",
            "1544 C_qm zero/provenance runner",
            "C_qm=0 rejected; finite C_qm provenance requirements installed; dry runner rejects current scoring",
            "IMPORT_AS_CURRENT_CQM_GATE",
            "no value, units, norm, source row, derivation status, or projection-ready row",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "frontier_id": frontier_id,
            "checkpoint": checkpoint,
            "imported_result": result,
            "current_2223_use": use,
            "remaining_blocker": blocker,
            **flags(),
        }
        for frontier_id, checkpoint, result, use, blocker in entries
    ]


def qmap_gate_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "QGATE2223_0_q_definition",
            "q_loc parent definition",
            "q_loc must be parent-owned before tests and cannot be defined by deleting failed couplings",
            "NOT_PARENT_SIGNED",
            "conditional q contracts exist, but no terminal same-branch q_loc definition is signed",
        ),
        (
            "QGATE2223_1_v_generator",
            "v_m field-by-field action",
            "v_m must specify variations of m, L_cg, Pi_B, q components, source normalization, domain and boundary data",
            "NOT_DEFINED_STRONGLY_ENOUGH",
            "current v_m is a named direction, not a parent null/gauge generator",
        ),
        (
            "QGATE2223_2_kernel",
            "Dq[v_m]=0",
            "requires q_loc definition plus v_m action with every visible/source/readout component silent",
            "KERNEL_NOT_PROVED",
            "1541/1542 reject exact kernel with current evidence",
        ),
        (
            "QGATE2223_3_observed_functor",
            "DObs_e[Dq[v_m]]=0",
            "observed coframe/no-shadow-frame descent must be parent-signed",
            "UNSIGNED",
            "covariance/WEP/Ward shortcuts do not prove it",
        ),
        (
            "QGATE2223_4_boundary_direct",
            "direct and boundary memory silence",
            "direct_m S=0, source-normalization descent, and Q_m^H=0 must close with q-kernel",
            "OPEN",
            "even q-kernel alone would not remove direct/source/boundary terms",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "object": obj,
            "required_statement": statement,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, obj, statement, status, reason in entries
    ]


def cqm_residual_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "CQM2223_0_definition",
            "C_qm",
            "C_qm := ||DObs_e[Dq[v_m]]||_loc",
            "DEFINITION_ONLY",
            "norm and v_m normalization still missing",
        ),
        (
            "CQM2223_1_zero",
            "C_qm=0",
            "parent q_loc + v_m kernel + observed coframe/no-shadow theorem + norm normalization",
            "THEOREM_ZERO_NOT_CLOSED",
            "1544 rejects zero branch under current evidence",
        ),
        (
            "CQM2223_2_finite_provenance",
            "finite C_qm residual",
            "value/interval, units, local norm, source path+row, derivation status, projection contract",
            "PROVENANCE_REQUIRED_MISSING",
            "no placeholder or inference-only value can score",
        ),
        (
            "CQM2223_3_Sgeom",
            "S_geom_m",
            "S_geom_m <= 1/2*T_source_norm*C_qm",
            "FORMULA_ONLY_INPUTS_MISSING",
            "C_qm and T_source_norm missing",
        ),
        (
            "CQM2223_4_Scg_envelope",
            "S_cg_norm",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "SCHEMA_READY_NOT_COMPUTABLE",
            "all finite inputs are missing or unproved",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition_or_formula": formula,
            "status": status,
            "blocker": blocker,
            **flags(),
        }
        for residual_id, symbol, formula, status, blocker in entries
    ]


def projection_rows() -> list[dict[str, Any]]:
    entries = [
        ("PROJ2223_0_R10", "R10", "alpha_R10(lambda)=Pi_R10(lambda)*N_pair", "NOT_COMPUTABLE", "C_qm/S_cg/N_pair and valid projection rows missing"),
        ("PROJ2223_1_PPN", "PPN", "Delta_PPN<=Pi_PPN*N_lock", "NOT_COMPUTABLE", "N_lock, response matrix, hidden kernels missing"),
        ("PROJ2223_2_clock", "clock/redshift/constants", "delta ln nu<=Pi_clock*N_lock plus readout sensitivities", "NOT_COMPUTABLE", "clock projection and constants/readout split missing"),
        ("PROJ2223_3_orbital", "orbital/source-GM", "delta a/a or delta GM/GM<=Pi_orbital*N_lock", "NOT_COMPUTABLE", "worldtube/source profile and same-frame mass charge missing"),
        ("PROJ2223_4_local_GR", "local GR/Newton", "local residual vector<=Pi_local*N_lock plus hidden kernels", "BLOCKED_NO_CLAIM", "no q-kernel, finite C_qm, source envelope, or projection pass"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "arena": arena,
            "projection_formula": formula,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for projection_id, arena, formula, status, reason in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2223_0_frontier_import", "1541-1544 quotient/C_qm frontier imported", "PASS_NONCLAIM", "validated old frontier is connected to current R2FR numbering"),
        ("CG2223_1_Dq_kernel", "Dq[v_m]=0", "BLOCKED_NONCLAIM", "q_loc and v_m are not jointly parent-signed"),
        ("CG2223_2_Cqm_zero", "C_qm=0", "BLOCKED_NONCLAIM", "parent q/v_m/observed-coframe/norm theorem missing"),
        ("CG2223_3_Cqm_finite", "finite C_qm score-ready", "BLOCKED_NONCLAIM", "value, units, norm, source row, derivation status and projection contract missing"),
        ("CG2223_4_Scg", "S_cg_norm computable", "BLOCKED_NONCLAIM", "finite source inputs missing"),
        ("CG2223_5_arenas", "R10/PPN/clock/orbital score-ready", "BLOCKED_NONCLAIM", "arena projection rows and N_lock missing"),
        ("CG2223_6_local_GR", "derived local GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "q-kernel/finite coupling/source/projection gates all remain open"),
        ("CG2223_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private branch remains mid-proof"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2223_0_import",
            "Import 1541-1544 as the current q/C_qm frontier.",
            "FRONTIER_CONNECTED",
            "the old chain already tested the exact kernel, finite fork, projection pack, and C_qm provenance gate",
        ),
        (
            "DEC2223_1_exact",
            "Do not claim Dq[v_m]=0 or C_qm=0.",
            "EXACT_KERNEL_FAILS_CURRENT_EVIDENCE",
            "q_loc/v_m/observed coframe/norm clauses are not parent-signed together",
        ),
        (
            "DEC2223_2_finite",
            "Retain the finite C_qm/S_cg residual branch.",
            "FINITE_COUPLING_BRANCH_REQUIRED",
            "S_cg_norm must be bounded through C_qm and direct/source/boundary terms unless a future parent action signs the kernel",
        ),
        (
            "DEC2223_3_next",
            "Move to source-norm/direct residual provenance.",
            "NEXT_SOURCE_RESIDUAL_PACK",
            "1544 already installed C_qm provenance requirements; the remaining S_cg terms need the same discipline",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2223_0_2224",
            "target_file": "2224-Y5-R2FR-source-norm-and-direct-memory-residual-frontier-import.md",
            "target_script": "scripts/Y5_R2FR_source_norm_and_direct_memory_residual_frontier_import_2224.py",
            "objective": "inspect/import the existing 1545 source-norm/direct-memory residual provenance pack and decide whether T_source_norm, S_direct_m, S_source_norm_extra, or S_boundary_m can be theorem-zero, source-backed finite, or must remain retained residuals",
            "success_condition": "each non-Cqm term in the S_cg_norm envelope has a theorem-zero gate or finite provenance row with missing clauses explicit",
            "do_not": "do not insert placeholder values; do not cancel terms; do not claim q-kernel silence, local lock, local GR, or arena passes",
            **flags(),
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for copy_id, destination in COPY_TARGETS.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CQM_RESIDUAL_GATE, destination)
        copied.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(CQM_RESIDUAL_GATE),
                "target_path": rel(destination),
                "copied": destination.exists(),
                "parse_ok": parse_csv(destination),
                **flags(),
            }
        )
    return copied


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    frontier = read_csv(FRONTIER_IMPORT)
    qgate = read_csv(QMAP_KERNEL_GATE)
    residual = read_csv(CQM_RESIDUAL_GATE)
    projection = read_csv(PROJECTION_GATE)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    copies = read_csv(BRANCH_COPIES)
    checks = [
        ("VAL2223_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited 2223 source paths exist"),
        ("VAL2223_01_prior_validations", all(row["validation_overall_pass"] in {"", "True"} for row in sources), "all imported validation files pass overall"),
        ("VAL2223_02_frontier_import", len(frontier) == 4 and any(row["checkpoint"].startswith("1544") for row in frontier), "1541-1544 quotient/C_qm frontier imported"),
        ("VAL2223_03_kernel_blocked", any(row["object"] == "Dq[v_m]=0" and row["status"] == "KERNEL_NOT_PROVED" for row in qgate), "Dq[v_m]=0 remains blocked"),
        ("VAL2223_04_Cqm_zero_blocked", any(row["symbol"] == "C_qm=0" and row["status"] == "THEOREM_ZERO_NOT_CLOSED" for row in residual), "C_qm zero theorem remains unclosed"),
        ("VAL2223_05_Cqm_finite_gate", any(row["symbol"] == "finite C_qm residual" and row["status"] == "PROVENANCE_REQUIRED_MISSING" for row in residual), "finite C_qm provenance gate retained"),
        ("VAL2223_06_projection_blocked", all(row["status"] in {"NOT_COMPUTABLE", "BLOCKED_NO_CLAIM"} for row in projection), "arena projections remain blocked"),
        ("VAL2223_07_claims_blocked", any(row["gate_id"] == "CG2223_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in claims), "local GR claim remains blocked"),
        ("VAL2223_08_decision_finite", any(row["result"] == "FINITE_COUPLING_BRANCH_REQUIRED" for row in decisions), "finite coupling branch selected"),
        ("VAL2223_09_next_target", any("2224-Y5-R2FR-source-norm" in row["target_file"] for row in next_target), "next target imports source-norm/direct residual frontier"),
        ("VAL2223_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2223 CSVs parse cleanly"),
        ("VAL2223_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated flags remain nonclaim"),
        ("VAL2223_12_branch_copies", all(row["copied"] == "True" and row["parse_ok"] == "True" for row in copies), "branch copies written and parse"),
        ("VAL2223_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2223_14_formalization_no_2223", formalization_2223_artifacts_absent(), "formalization-workbench has no 2223 artifacts"),
        ("VAL2223_15_formalization_untouched", formalization_untouched_since_start(), "formalization-workbench untouched during 2223 run"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            **flags(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2223_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2223 imports the 1541-1544 q/C_qm frontier, refuses Dq[v_m]=0 and C_qm=0 under current evidence, retains finite C_qm/S_cg residual gates, and selects source-norm/direct residual import next"
            if overall
            else "2223 validation failed; inspect failed rows before continuing",
            **flags(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    frontier: list[dict[str, Any]],
    qgate: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2223 - Y5/R2FR Quotient Map Vertical Generator Frontier Import Or Finite Coupling Row",
                "",
                "## Verdict",
                "- 2223 imports the existing `1541-1544` q-map / vertical-generator / `C_qm` frontier into the current R2FR line.",
                "- Exact source silence does not close: `Dq[v_m]=0` and `C_qm=0` are both rejected under current evidence.",
                "- The finite route is retained: `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.",
                "- `C_qm` may only enter later scoring with value/interval, units, local norm, source path+row, derivation status, and projection contract.",
                "- Local GR/Newton/PPN/R10/clock/orbital claims remain blocked/nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
                "",
                "## Frontier Import Audit",
                md_table(frontier, ["frontier_id", "checkpoint", "imported_result", "current_2223_use", "remaining_blocker"]),
                "",
                "## Qmap Vertical Kernel Gate",
                md_table(qgate, ["gate_id", "object", "required_statement", "status", "reason"]),
                "",
                "## Cqm Finite Residual Gate",
                md_table(residual, ["residual_id", "symbol", "definition_or_formula", "status", "blocker"]),
                "",
                "## Local Projection Blocker Gate",
                md_table(projection, ["projection_id", "arena", "projection_formula", "status", "reason"]),
                "",
                "## Claim Gate",
                md_table(claims, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision Ledger",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Next Target",
                md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
                "",
                "## Branch Copies",
                md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Working Interpretation",
                "",
                "This is a real narrowing. The theory cannot get local-GR safety from rhetoric about hidden variables: either the parent action gives a true quotient-kernel generator, or the finite coupling residual must be carried and tested. Current evidence chooses the second route.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    frontier = frontier_rows()
    qgate = qmap_gate_rows()
    residual = cqm_residual_rows()
    projection = projection_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FRONTIER_IMPORT, frontier)
    write_csv(QMAP_KERNEL_GATE, qgate)
    write_csv(CQM_RESIDUAL_GATE, residual)
    write_csv(PROJECTION_GATE, projection)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_outputs()
    write_csv(BRANCH_COPIES, copies)
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        FRONTIER_IMPORT,
        QMAP_KERNEL_GATE,
        CQM_RESIDUAL_GATE,
        PROJECTION_GATE,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
        BRANCH_COPIES,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, frontier, qgate, residual, projection, claims, decisions, next_target, copies, validation)


if __name__ == "__main__":
    main()
