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
DOC = ROOT / "2224-Y5-R2FR-source-norm-and-direct-memory-residual-frontier-import.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_SOURCE_RESIDUALS_2224"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2223_doc": ROOT / "2223-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md",
    "2223_validation": OUT / "P8_Y5_BRR545_2223_VALIDATION.csv",
    "2223_cqm": OUT / "P8_Y5_PARENT_QLOC_2223_CQM_FINITE_RESIDUAL_GATE.csv",
    "2223_next": OUT / "P8_Y5_PARENT_QLOC_2223_NEXT_TARGET.csv",
    "1545_doc": ROOT / "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
    "1545_validation": OUT / "P8_Y5_BRR545_1545_VALIDATION.csv",
    "1545_tsource": OUT / "P8_Y5_PARENT_QLOC_1545_TSOURCE_NORM_GATE.csv",
    "1545_direct": OUT / "P8_Y5_PARENT_QLOC_1545_DIRECT_MEMORY_RESIDUAL_GATE.csv",
    "1545_extra": OUT / "P8_Y5_PARENT_QLOC_1545_SOURCE_NORMALIZATION_EXTRA_GATE.csv",
    "1545_boundary": OUT / "P8_Y5_PARENT_QLOC_1545_BOUNDARY_MEMORY_RESIDUAL_GATE.csv",
    "1545_scg": OUT / "P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv",
    "1546_doc": ROOT / "1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md",
    "1546_validation": OUT / "P8_Y5_BRR545_1546_VALIDATION.csv",
    "1546_worldtube": OUT / "P8_Y5_PARENT_QLOC_1546_WORLDTUBE_REQUIREMENTS.csv",
    "1546_tsource_def": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv",
    "1546_arena": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_ARENA_COMPATIBILITY.csv",
    "1547_doc": ROOT / "1547-Y5-compact-worldtube-profile-template-and-arena-map.md",
    "1547_validation": OUT / "P8_Y5_BRR545_1547_VALIDATION.csv",
    "1547_profile": OUT / "P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1547_arena": OUT / "P8_Y5_PARENT_QLOC_1547_ARENA_MAP_REQUIREMENTS.csv",
    "1547_no_retuning": OUT / "P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv",
    "1548_doc": ROOT / "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md",
    "1548_validation": OUT / "P8_Y5_BRR545_1548_VALIDATION.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1548_dimension": OUT / "P8_Y5_PARENT_QLOC_1548_DIMENSION_AND_NORMALIZATION_CONTRACT.csv",
    "1548_acquisition": OUT / "P8_Y5_PARENT_QLOC_1548_SOURCE_ACQUISITION_LEDGER.csv",
    "1548_runner": OUT / "P8_Y5_PARENT_QLOC_1548_ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv",
    "1549_doc": ROOT / "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2224_SOURCE_REGISTER.csv"
FRONTIER_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2224_SOURCE_RESIDUAL_FRONTIER_IMPORT.csv"
SCG_TERM_GATE = OUT / "P8_Y5_PARENT_QLOC_2224_SCG_TERM_PROVENANCE_GATE.csv"
WORLDTUBE_GATE = OUT / "P8_Y5_PARENT_QLOC_2224_WORLDTUBE_PROFILE_GATE.csv"
UNIT_CLOSURE_GATE = OUT / "P8_Y5_PARENT_QLOC_2224_JQ_UNIT_SOURCE_VARIATION_GATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2224_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2224_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2224_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2224_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2224_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2224_SOURCE_RESIDUAL_FRONTIER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "source_residual_frontier_nonclaim_2224.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_SOURCE_RESIDUAL_FRONTIER_2224_NONCLAIM.csv",
}


def flags() -> dict[str, bool]:
    return {
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


def formalization_2224_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2224" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "input evidence"
        if key.startswith("2223"):
            role = "current finite Cqm/S_cg handoff"
        elif key.startswith("1545"):
            role = "source-norm/direct/source-normalization/boundary residual gates"
        elif key.startswith("1546"):
            role = "T_source worldtube normalization gate"
        elif key.startswith("1547"):
            role = "compact worldtube profile template and no-retuning guard"
        elif key.startswith("1548"):
            role = "shared symbolic profile and source acquisition frontier"
        elif key.startswith("1549"):
            role = "known next J_q unit/source variation closure target"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2224_{index}_{key}",
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
            "FRONT2224_0_1545",
            "1545 source residual provenance",
            "T_source_norm, S_direct_m, S_source_norm_extra, and S_boundary_m all have zero/finite provenance gates",
            "IMPORT_AS_SCG_TERM_GATES",
            "all remain missing/unsigned; S_cg_norm noncomputable",
        ),
        (
            "FRONT2224_1_1546",
            "1546 T_source worldtube",
            "T_source_norm is a same-frame Hilbert/Noether worldtube norm problem; orbital GM import rejected",
            "IMPORT_AS_SOURCE_NORMALIZATION_GUARD",
            "profile, units, dual norm, source path and arena map missing",
        ),
        (
            "FRONT2224_2_1547",
            "1547 compact profile template",
            "shared W_src/J_q/T_source_norm template covers R10, PPN, clock, orbital and local_GR with no per-arena retuning",
            "IMPORT_AS_FILLABLE_TEMPLATE",
            "numeric/source-backed profile and arena kernels missing",
        ),
        (
            "FRONT2224_3_1548",
            "1548 symbolic profile runner",
            "smooth bump, regulated distributional, Hilbert-projector and Noether-charge routes are routable but nonclaim",
            "IMPORT_AS_CURRENT_PROFILE_FRONTIER",
            "parent J_q, q dimension, regulator, unit pairing and arena kernels missing",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "frontier_id": frontier_id,
            "checkpoint": checkpoint,
            "imported_result": result,
            "current_2224_use": use,
            "remaining_blocker": blocker,
            **flags(),
        }
        for frontier_id, checkpoint, result, use, blocker in entries
    ]


def scg_term_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "SCGTERM2224_0_Cqm",
            "C_qm",
            "observed quotient derivative norm from 2223/1544",
            "BLOCKED_UPSTREAM",
            "zero theorem and finite provenance both missing",
        ),
        (
            "SCGTERM2224_1_Tsource",
            "T_source_norm",
            "same-frame compact source Hilbert/Noether worldtube norm",
            "PROFILE_UNITS_AND_NORM_MISSING",
            "not zero; cannot import orbital GM; needs parent J_q/source profile",
        ),
        (
            "SCGTERM2224_2_direct",
            "S_direct_m",
            "direct memory dependence in matter/source action",
            "ZERO_OR_FINITE_ROUTE_UNSIGNED",
            "no parent no-direct-memory object-language theorem and no finite coefficient",
        ),
        (
            "SCGTERM2224_3_source_norm_extra",
            "S_source_norm_extra",
            "memory leakage in source calibration beyond Hilbert q-pullback",
            "ZERO_OR_FINITE_ROUTE_UNSIGNED",
            "source-normalization descent not parent-derived and no finite residual",
        ),
        (
            "SCGTERM2224_4_boundary",
            "S_boundary_m",
            "compact inner/domain/boundary memory leakage",
            "ZERO_OR_FINITE_ROUTE_UNSIGNED",
            "Q_mH/no-flux/domain support not signed and no finite boundary norm",
        ),
        (
            "SCGTERM2224_5_envelope",
            "S_cg_norm",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "SCHEMA_READY_NOT_COMPUTABLE",
            "every input term is missing, unsigned, or upstream-blocked",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "term_id": term_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "blocker": blocker,
            **flags(),
        }
        for term_id, symbol, meaning, status, blocker in entries
    ]


def worldtube_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "WT2224_0_shared_core",
            "W_src/J_q shared core",
            "one compact profile should feed all local arenas through projection operators only",
            "TEMPLATE_EXISTS_NO_PROFILE",
            "no parent-sourced W_src/J_q profile",
        ),
        (
            "WT2224_1_no_orbital_import",
            "no orbital GM source normalization",
            "Kepler/ephemeris GM is a comparison output, not T_source_norm",
            "PASS_GUARD_NONCLAIM",
            "prevents Newtonian readout smuggling",
        ),
        (
            "WT2224_2_no_retuning",
            "shared theta_src",
            "profile parameters fixed before R10/PPN/clock/orbital projections",
            "PASS_GUARD_NONCLAIM",
            "if arenas need different theta_src, branch must split as closure",
        ),
        (
            "WT2224_3_symbolic_profiles",
            "smooth/distributional/Hilbert/Noether candidates",
            "symbolic families can be written without scoring",
            "CONDITIONAL_SYMBOLIC_ONLY",
            "parent source variation, regulator, charge and unit closure missing",
        ),
        (
            "WT2224_4_arena_maps",
            "Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local",
            "arena maps may project shared W_src but cannot redefine it",
            "MISSING_ARENA_KERNELS",
            "no local arena score-ready projection",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "worldtube_id": worldtube_id,
            "object": obj,
            "rule": rule,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for worldtube_id, obj, rule, status, reason in entries
    ]


def unit_rows() -> list[dict[str, Any]]:
    entries = [
        ("UNIT2224_0_q_dimension", "dim(q_loc)", "field dimension of q_loc required before J_q units are meaningful", "MISSING_PARENT_FIELD_DIMENSION"),
        ("UNIT2224_1_source_variation", "J_q=delta S_matter/delta q", "must come from parent matter variation in the observed frame", "MISSING_PARENT_VARIATION"),
        ("UNIT2224_2_observed_measure", "dV_e_obs", "worldtube measure must descend to observed frame and be shared by readouts", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("UNIT2224_3_dual_norm", "||J_q||_{source,W,E*}", "must pair with C_qm so 1/2*T_source_norm*C_qm has S_cg units", "MISSING_NORM_PAIRING"),
        ("UNIT2224_4_arena_units", "Pi_arena output units", "projection kernels must map N_lock/N_pair to observable residual units", "MISSING_ARENA_KERNEL_UNITS"),
        ("UNIT2224_5_next", "J_q unit/source variation closure", "derive source-current units or record missing parent input", "NEXT_1549_IMPORT"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "unit_id": unit_id,
            "object": obj,
            "requirement": requirement,
            "status": status,
            **flags(),
        }
        for unit_id, obj, requirement, status in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2224_0_frontier_import", "1545-1548 source residual/worldtube frontier imported", "PASS_NONCLAIM", "validated old frontier is connected to current R2FR numbering"),
        ("CG2224_1_Scg_terms", "all non-Cqm S_cg terms theorem-zero or finite sourced", "BLOCKED_NONCLAIM", "T_source/direct/source-normalization/boundary terms remain unsigned or missing"),
        ("CG2224_2_Tsource", "T_source_norm score-ready", "BLOCKED_NONCLAIM", "worldtube profile, units, norm, and arena map missing"),
        ("CG2224_3_profile", "shared source profile score-ready", "BLOCKED_NONCLAIM", "symbolic candidates are not parent sourced"),
        ("CG2224_4_no_retuning", "no-retuning guard active", "PASS_GUARD_NONCLAIM", "shared theta_src and no orbital-GM import rules are recorded"),
        ("CG2224_5_arena_scores", "R10/PPN/clock/orbital score-ready", "BLOCKED_NO_CLAIM", "arena kernels and source profile missing"),
        ("CG2224_6_local_GR", "derived local GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "S_cg/N_pair/N_lock/projection gates remain open"),
        ("CG2224_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private branch remains mid-proof"),
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
            "DEC2224_0_import",
            "Import 1545-1548 as the current source-residual frontier.",
            "FRONTIER_CONNECTED",
            "the old chain already installed provenance gates, worldtube rules, shared profile template, and symbolic acquisition ledger",
        ),
        (
            "DEC2224_1_no_score",
            "Do not score S_cg_norm or T_source_norm.",
            "SOURCE_PROFILE_NOT_READY",
            "symbolic profile rows are scaffolding; source variation, units, regulator and arena kernels are missing",
        ),
        (
            "DEC2224_2_guard",
            "Keep no-retuning and no orbital-GM import guards.",
            "PATCHWORK_GUARD_ACTIVE",
            "this prevents the local branch becoming separate R10/PPN/clock/orbit patches",
        ),
        (
            "DEC2224_3_next",
            "Move to J_q unit/source variation closure.",
            "NEXT_UNIT_CLOSURE",
            "without dim(q_loc) and delta S_matter/delta q, the source norm is only notation",
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
            "next_id": "NEXT2224_0_2225",
            "target_file": "2225-Y5-R2FR-Jq-unit-dimension-and-parent-source-variation-frontier-import.md",
            "target_script": "scripts/Y5_R2FR_Jq_unit_dimension_and_parent_source_variation_frontier_import_2225.py",
            "objective": "inspect/import the existing 1549 J_q unit/dimension and parent source variation closure; decide whether dim(q_loc), J_q=delta S_matter/delta q, and T_source_norm*C_qm unit pairing can close or must remain missing parent inputs",
            "success_condition": "J_q/source-current unit law is parent-derived or the exact missing parent q/action/norm inputs are emitted as retained nonclaim blockers",
            "do_not": "do not assign units by convenience; do not import orbital, PPN, clock, or R10 data as source normalization; do not claim local tests",
            **flags(),
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for copy_id, destination in COPY_TARGETS.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SCG_TERM_GATE, destination)
        copied.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(SCG_TERM_GATE),
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
    terms = read_csv(SCG_TERM_GATE)
    worldtube = read_csv(WORLDTUBE_GATE)
    units = read_csv(UNIT_CLOSURE_GATE)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    copies = read_csv(BRANCH_COPIES)
    required_terms = {"C_qm", "T_source_norm", "S_direct_m", "S_source_norm_extra", "S_boundary_m", "S_cg_norm"}
    checks = [
        ("VAL2224_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited 2224 source paths exist"),
        ("VAL2224_01_prior_validations", all(row["validation_overall_pass"] in {"", "True"} for row in sources), "all imported validation files pass overall"),
        ("VAL2224_02_frontier_import", len(frontier) == 4 and any(row["checkpoint"].startswith("1548") for row in frontier), "1545-1548 frontier imported"),
        ("VAL2224_03_scg_terms", required_terms.issubset({row["symbol"] for row in terms}), "all S_cg envelope terms recorded"),
        ("VAL2224_04_envelope_noncomputable", any(row["symbol"] == "S_cg_norm" and row["status"] == "SCHEMA_READY_NOT_COMPUTABLE" for row in terms), "S_cg envelope remains noncomputable"),
        ("VAL2224_05_no_retuning_guard", any(row["object"] == "shared theta_src" and row["status"] == "PASS_GUARD_NONCLAIM" for row in worldtube), "shared-profile no-retuning guard retained"),
        ("VAL2224_06_unit_gap", any(row["object"] == "J_q=delta S_matter/delta q" and row["status"] == "MISSING_PARENT_VARIATION" for row in units), "parent source variation remains missing"),
        ("VAL2224_07_claims_blocked", any(row["gate_id"] == "CG2224_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in claims), "local GR claim remains blocked"),
        ("VAL2224_08_decision_next", any(row["result"] == "NEXT_UNIT_CLOSURE" for row in decisions), "decision selects J_q unit/source variation closure next"),
        ("VAL2224_09_next_target", any("2225-Y5-R2FR-Jq-unit" in row["target_file"] for row in next_target), "next target imports 1549 unit/source variation frontier"),
        ("VAL2224_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2224 CSVs parse cleanly"),
        ("VAL2224_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated flags remain nonclaim"),
        ("VAL2224_12_branch_copies", all(row["copied"] == "True" and row["parse_ok"] == "True" for row in copies), "branch copies written and parse"),
        ("VAL2224_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2224_14_formalization_no_2224", formalization_2224_artifacts_absent(), "formalization-workbench has no 2224 artifacts"),
        ("VAL2224_15_formalization_untouched", formalization_untouched_since_start(), "formalization-workbench untouched during 2224 run"),
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
            "check_id": "VAL2224_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2224 imports the 1545-1548 source residual/worldtube frontier, keeps S_cg noncomputable, preserves no-retuning/no-orbital-GM guards, and selects J_q unit/source variation closure next"
            if overall
            else "2224 validation failed; inspect failed rows before continuing",
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
    terms: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    units: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2224 - Y5/R2FR Source Norm And Direct Memory Residual Frontier Import",
                "",
                "## Verdict",
                "- 2224 imports the existing `1545-1548` source-residual/worldtube frontier into the current R2FR line.",
                "- The full finite source envelope is guarded: `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.",
                "- Nothing in that envelope is score-ready: source variation, compact profile, q dimension, units, regulator, boundary terms, and arena kernels remain missing.",
                "- Important guardrails survive: no orbital `GM` import, no per-arena retuning, no using R10/PPN/clock/orbit data to define source normalization.",
                "- Local GR/Newton/PPN/R10/clock/orbital claims remain blocked/nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
                "",
                "## Source Residual Frontier Import",
                md_table(frontier, ["frontier_id", "checkpoint", "imported_result", "current_2224_use", "remaining_blocker"]),
                "",
                "## S_cg Term Provenance Gate",
                md_table(terms, ["term_id", "symbol", "meaning", "status", "blocker"]),
                "",
                "## Worldtube Profile Gate",
                md_table(worldtube, ["worldtube_id", "object", "rule", "status", "reason"]),
                "",
                "## J_q Unit Source Variation Gate",
                md_table(units, ["unit_id", "object", "requirement", "status"]),
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
                "This is the anti-patchwork gate. The branch can carry one shared compact-source profile through multiple arenas, but only if `J_q`, its units, the worldtube profile, and the projection kernels are parent/source-backed before testing. Otherwise the local-GR route remains a retained residual framework, not a derivation.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    frontier = frontier_rows()
    terms = scg_term_rows()
    worldtube = worldtube_rows()
    units = unit_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FRONTIER_IMPORT, frontier)
    write_csv(SCG_TERM_GATE, terms)
    write_csv(WORLDTUBE_GATE, worldtube)
    write_csv(UNIT_CLOSURE_GATE, units)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_outputs()
    write_csv(BRANCH_COPIES, copies)
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        FRONTIER_IMPORT,
        SCG_TERM_GATE,
        WORLDTUBE_GATE,
        UNIT_CLOSURE_GATE,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
        BRANCH_COPIES,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, frontier, terms, worldtube, units, claims, decisions, next_target, copies, validation)


if __name__ == "__main__":
    main()
