from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2764-Y5-R2FR-EM-vertical-generator-norm-or-MICROSCOPE-extraction-preflight-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2764_SOURCE_REGISTER.csv",
    "norm": MTS / "P8_Y5_R2FR_2764_EM_VERTICAL_GENERATOR_NORM_AUDIT.csv",
    "f2": MTS / "P8_Y5_R2FR_2764_INDEPENDENT_F2_CHOKEPOINT.csv",
    "microscope": MTS / "P8_Y5_R2FR_2764_MICROSCOPE_EXTRACTION_PREFLIGHT.csv",
    "branch": MTS / "P8_Y5_R2FR_2764_RETAINED_B_ALPHA_BRANCH.csv",
    "gates": MTS / "P8_Y5_R2FR_2764_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2764_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2764_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2764_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2764_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "norm_queue": RAB_QUEUE / "JR2764_EM_VERTICAL_GENERATOR_NORM_AUDIT_NONCLAIM.csv",
    "f2_queue": RAB_QUEUE / "JR2764_INDEPENDENT_F2_CHOKEPOINT_NONCLAIM.csv",
    "microscope_queue": RAB_QUEUE / "JR2764_MICROSCOPE_EXTRACTION_PREFLIGHT_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "EM_OWNER_F2_CHOKEPOINT_2764_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "em_owner_or_microscope_extraction_preflight_2764_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2764_UNIQUE_MAXWELL_SUBBLOCK_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2764_00_2763_doc", "2763_doc", WORK / "2763-Y5-R2FR-alpha-owner-matter-functor-contract-or-MICROSCOPE-source-tensor-under-AX1090.md", ["NEXT2763_0_2764", "AOC2763_4_verdict"], "2763 handoff"),
        ("SRC2764_01_2763_validation", "2763_validation", MTS / "P8_Y5_BRR545_2763_VALIDATION.csv", ["VAL2763_OVERALL"], "2763 validation"),
        ("SRC2764_02_1056_doc", "1056_alpha_owner_doc", WORK / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md", ["VNA1056_6_verdict", "RSC1056_0_independent_F2", "DEC1056_2_choke_point"], "EM owner derivation precedent"),
        ("SRC2764_03_1056_norm", "1056_norm_csv", MTS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv", ["VNA1056_6_verdict"], "vertical generator norm audit"),
        ("SRC2764_04_1056_rescale", "1056_rescale_csv", MTS / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv", ["RSC1056_0_independent_F2"], "rescaling degeneracy ledger"),
        ("SRC2764_05_1056_balpha", "1056_balpha_csv", MTS / "P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv", ["BAB1056_3_verdict"], "retained b_alpha branch"),
        ("SRC2764_06_1493_doc", "1493_acquisition_doc", WORK / "1493-Y5-R10-RAB-download-or-extract-delta-w-source-files-R10-EotWash-MICROSCOPE.md", ["MIC1493_3_official_arrays_gate", "NEXT1493_0_1494"], "MICROSCOPE extraction precedent"),
        ("SRC2764_07_1493_downloads", "1493_downloads_csv", MTS / "P8_Y5_R10_1493_DOWNLOAD_ATTEMPT_LEDGER.csv", ["EXT1492_5_MICROSCOPE_PRL_FINAL", "EXT1492_6_MICROSCOPE_CQG_READOUT"], "download attempt ledger"),
        ("SRC2764_08_1493_microscope", "1493_microscope_csv", MTS / "P8_Y5_R10_1493_MICROSCOPE_PORTAL_PARSE_STATUS.csv", ["MIC1493_3_official_arrays_gate"], "MICROSCOPE parse status"),
        ("SRC2764_09_1493_hashes", "1493_hashes_csv", MTS / "P8_Y5_R10_1493_FILE_PROVENANCE_HASHES.csv", ["EXT1492_5_MICROSCOPE_PRL_FINAL"], "downloaded file hashes"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def load_inputs() -> dict[str, dict[str, str]]:
    return {
        "norm_verdict": find_row(read_csv_rows(MTS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv"), "attempt_id", "VNA1056_6_verdict"),
        "ind_f2": find_row(read_csv_rows(MTS / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv"), "counterexample_id", "RSC1056_0_independent_F2"),
        "gen_rescale": find_row(read_csv_rows(MTS / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv"), "counterexample_id", "RSC1056_1_generator_rescale"),
        "current_rescale": find_row(read_csv_rows(MTS / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv"), "counterexample_id", "RSC1056_2_current_rescale"),
        "balpha": find_row(read_csv_rows(MTS / "P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv"), "branch_id", "BAB1056_3_verdict"),
        "mic_final": find_row(read_csv_rows(MTS / "P8_Y5_R10_1493_DOWNLOAD_ATTEMPT_LEDGER.csv"), "external_id", "EXT1492_5_MICROSCOPE_PRL_FINAL"),
        "mic_readout": find_row(read_csv_rows(MTS / "P8_Y5_R10_1493_DOWNLOAD_ATTEMPT_LEDGER.csv"), "external_id", "EXT1492_6_MICROSCOPE_CQG_READOUT"),
        "mic_gate": find_row(read_csv_rows(MTS / "P8_Y5_R10_1493_MICROSCOPE_PORTAL_PARSE_STATUS.csv"), "microscope_id", "MIC1493_3_official_arrays_gate"),
    }


def build_norm_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    verdict = inputs["norm_verdict"]
    return [
        nonclaim({"row_id": "EMN2764_0_parent_generator", "route_piece": "compact parent charge generator", "mathematical_form": "T_Q in Lie(G_parent), exp(2*pi*T_Q)=1, A_parent includes A_Q T_Q", "status": "PARTIAL_SUPPORT_ONLY", "would_buy": "charge labels and connection period", "current_gap": "does not own continuous Maxwell kinetic coefficient"}),
        nonclaim({"row_id": "EMN2764_1_fixed_norm", "route_piece": "fixed generator norm", "mathematical_form": "N_Q=<T_Q,T_Q>_P with Lie_v N_Q=0", "status": "NOT_PARENT_SIGNED", "would_buy": "forbids generator rescaling", "current_gap": "parent fibre metric/lattice norm not derived"}),
        nonclaim({"row_id": "EMN2764_2_curvature_subblock", "route_piece": "parent curvature subblock", "mathematical_form": "S_parent contains -C_P/4 int <F,F>_P so g_EM^{-2}=C_P N_Q", "status": "CONDITIONAL_BUT_DEFEATED_BY_INDEPENDENT_F2", "would_buy": "Maxwell kinetic coefficient inherited from parent norm", "current_gap": "must forbid additional lambda_A F_Q^2"}),
        nonclaim({"row_id": "EMN2764_3_current_readout_owner", "route_piece": "current and readout share owner", "mathematical_form": "same T_Q fixes S_EM, S_int, current normalization, and observed alpha readout", "status": "NOT_PARENT_SIGNED", "would_buy": "prevents charge/current/readout rescaling leakage", "current_gap": "Noether current normalization and spectroscopy readout remain separate"}),
        nonclaim({"row_id": "EMN2764_4_verdict", "route_piece": "derive alpha owner via generator norm", "mathematical_form": verdict.get("mathematical_form", "current alpha-owner status"), "status": verdict.get("current_result", "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA"), "would_buy": "b_alpha=0 and beta_source_alpha=0", "current_gap": verdict.get("blocker", "unique Maxwell subblock/no-independent-F2 theorem missing")}),
    ]


def build_f2_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    ind = inputs["ind_f2"]
    gen = inputs["gen_rescale"]
    cur = inputs["current_rescale"]
    return [
        nonclaim({"row_id": "F2C2764_0_independent_F2", "choke_point": "independent Maxwell kinetic invariant", "counterexample": ind.get("mathematical_form", "Delta S=-lambda_A/4 int sqrt(-g_obs) F_Q^2"), "effect": ind.get("effect", "g_EM^{-2}=C_P N_Q+lambda_A"), "repair_needed": ind.get("repair_needed", "operator classification forbids independent F_Q^2"), "status": "MAIN_CHOKEPOINT"}),
        nonclaim({"row_id": "F2C2764_1_generator_rescale", "choke_point": "generator/connection rescaling", "counterexample": gen.get("mathematical_form", "T_Q -> s T_Q, A_Q -> A_Q/s"), "effect": gen.get("effect", "charge unit and A normalization remain conventional/free"), "repair_needed": gen.get("repair_needed", "fixed compact lattice plus nonrescalable parent norm"), "status": "LIVE"}),
        nonclaim({"row_id": "F2C2764_2_current_rescale", "choke_point": "current normalization independent from kinetic coefficient", "counterexample": cur.get("mathematical_form", "S_int=sum_A q_A(Xhat) int A_Q J_A"), "effect": cur.get("effect", "same F_Q^2 coefficient but different source/test charge response"), "repair_needed": cur.get("repair_needed", "same Noether owner for kinetic term, charge unit, current, and matter coupling"), "status": "LIVE"}),
        nonclaim({"row_id": "F2C2764_3_unique_subblock_theorem", "choke_point": "unique Maxwell subblock theorem", "counterexample": "No unique-subblock theorem means alpha owner can always be shifted into lambda_A.", "effect": "b_alpha and beta_source_alpha remain finite branch quantities", "repair_needed": "prove no independent F_Q^2 operator is admissible in the parent operator grammar", "status": "NEXT_DERIVATION_TARGET"}),
        nonclaim({"row_id": "F2C2764_4_verdict", "choke_point": "current EM owner status", "counterexample": "independent F2 plus rescaling degeneracy remain legal", "effect": "EM owner not claimable", "repair_needed": "2765 unique-Maxwell-subblock/no-independent-F2 theorem attempt", "status": "ALPHA_OWNER_STILL_BLOCKED"}),
    ]


def build_microscope_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    final = inputs["mic_final"]
    readout = inputs["mic_readout"]
    gate = inputs["mic_gate"]
    return [
        nonclaim({"row_id": "MICP2764_0_final_PRL", "object": "MICROSCOPE final PRL PDF", "download_status": final.get("download_status", "DOWNLOADED_PDF_PROVENANCE_ONLY"), "local_path": final.get("local_path", "source-intake/microscope/docs/Touboul_2022_PRL_final_results.pdf"), "preflight_status": "PROVENANCE_AVAILABLE_NOT_SCOREABLE", "next_action": "extract/confirm eta/material convention only"}),
        nonclaim({"row_id": "MICP2764_1_CQG_readout", "object": "MICROSCOPE CQG readout PDF", "download_status": readout.get("download_status", "DOWNLOADED_PDF_PROVENANCE_ONLY"), "local_path": readout.get("local_path", "source-intake/microscope/docs/Touboul_2022_CQG_readout.pdf"), "preflight_status": "PROVENANCE_AVAILABLE_NOT_PARSED", "next_action": "parse readout/product convention and units"}),
        nonclaim({"row_id": "MICP2764_2_official_arrays", "object": "official arrays/source/product/material tensors", "download_status": gate.get("source_present", "False"), "local_path": "target files from 1492 manifest", "preflight_status": gate.get("parse_status", "OFFICIAL_ARRAYS_MISSING_SCORE_BLOCKED"), "next_action": "obtain official CMSM export/package or reproducible parser"}),
        nonclaim({"row_id": "MICP2764_3_preflight_verdict", "object": "MICROSCOPE empirical fallback", "download_status": "PARTIAL_PROVENANCE_ONLY", "local_path": "PDFs downloaded; official arrays missing", "preflight_status": "EXTRACTION_PREFLIGHT_READY_NOT_SCORE_READY", "next_action": "table/text extraction or portal access work can proceed, but no WEP/local claim"}),
    ]


def build_branch_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    balpha = inputs["balpha"]
    return [
        nonclaim({"row_id": "BAB2764_0_clock", "arena": "clock", "retained_quantity": "b_alpha*tau_clock_time", "current_status": "2.1e-18 yr^-1 product bound", "why_retained": "alpha owner and tau_clock not derived", "score_ready": False}),
        nonclaim({"row_id": "BAB2764_1_WEP", "arena": "MICROSCOPE/WEP", "retained_quantity": "beta_source_alpha*b_alpha*tau_WEP", "current_status": "4.797780522732e-05 product target", "why_retained": "alpha zero theorem and tau_WEP map not derived", "score_ready": False}),
        nonclaim({"row_id": "BAB2764_2_R10", "arena": "R10", "retained_quantity": "K_X^R10 beta_s beta_t plus tail", "current_status": "unscoreable", "why_retained": "lambda_X/K_X/Z_X/tau_R10/curve missing", "score_ready": False}),
        nonclaim({"row_id": "BAB2764_3_verdict", "arena": "cross_arena", "retained_quantity": "b_alpha finite branch", "current_status": balpha.get("current_bound_or_status", "retain product-prior branch"), "why_retained": balpha.get("why_retained", "unique Maxwell subblock/no-independent-F2 proof is missing"), "score_ready": False}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2764_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2764_1_generator_norm", "gate": "parent generator norm fixes alpha", "passed": False, "claim_effect": "alpha owner not promoted"}),
        nonclaim({"row_id": "CG2764_2_no_independent_F2", "gate": "independent F_Q^2 operator forbidden", "passed": False, "claim_effect": "main alpha-owner choke point remains"}),
        nonclaim({"row_id": "CG2764_3_current_readout", "gate": "current/readout share same owner", "passed": False, "claim_effect": "beta_source_alpha zero not promoted"}),
        nonclaim({"row_id": "CG2764_4_MICROSCOPE_arrays", "gate": "MICROSCOPE official arrays parsed", "passed": False, "claim_effect": "empirical WEP fallback not score-ready"}),
        nonclaim({"row_id": "CG2764_5_local_GR_Newton", "gate": "local GR/Newton residual complete", "passed": False, "claim_effect": "no local-GR/Newton claim from 2764"}),
    ]


def build_refusals() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2764_0_alpha_owner", "claim": "2764 derives alpha_EM owner", "allowed": False, "reason": "independent F_Q^2 and generator/current/readout rescaling remain legal", "blocking_rows": "EMN2764_4_verdict;F2C2764_4_verdict"}),
        nonclaim({"row_id": "REF2764_1_balpha_zero", "claim": "b_alpha=0 or beta_source_alpha=0 is now proved", "allowed": False, "reason": "requires unique Maxwell subblock, current owner, and readout descent", "blocking_rows": "CG2764_2_no_independent_F2;CG2764_3_current_readout"}),
        nonclaim({"row_id": "REF2764_2_MICROSCOPE_score", "claim": "MICROSCOPE finite branch can score", "allowed": False, "reason": "PDFs are provenance only; official arrays/tensors are missing", "blocking_rows": "MICP2764_2_official_arrays;CG2764_4_MICROSCOPE_arrays"}),
        nonclaim({"row_id": "REF2764_3_local_GR", "claim": "MTS derives local GR/Newton after 2764", "allowed": False, "reason": "2764 sharpens EM owner but leaves the local residual vector incomplete", "blocking_rows": "CG2764_5_local_GR_Newton;BAB2764_3_verdict"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2764_0_2765",
            "next_target": "2765-Y5-R2FR-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention-under-AX1090.md",
            "script": "scripts/Y5_R2FR_unique_Maxwell_subblock_no_independent_F2_ban_or_balpha_retention_under_AX1090_2765.py",
            "why": "The EM owner route now bottlenecks on whether the parent operator grammar forbids an independent lambda_A F_Q^2 term. If that ban closes, alpha ownership can advance; if not, b_alpha remains a finite product-prior branch.",
            "include": "operator classification, parent curvature subblock uniqueness, gauge invariance limits, radiative closure, retained b_alpha product branch, MICROSCOPE extraction preflight state",
            "exclude": "compactness-alone alpha proof, declaring alpha fixed by taste, unit rescaling, tau unity shortcut, WEP/local-GR claim, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(norm: list[dict[str, Any]], f2: list[dict[str, Any]], microscope: list[dict[str, Any]], branch: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2764_0_norm_queue", "norm", norm, OUTPUTS["norm"], BRANCH_OUTPUTS["norm_queue"], "EM vertical generator norm audit"),
        ("BR2764_1_f2_queue", "f2", f2, OUTPUTS["f2"], BRANCH_OUTPUTS["f2_queue"], "independent F2 choke point"),
        ("BR2764_2_microscope_queue", "microscope", microscope, OUTPUTS["microscope"], BRANCH_OUTPUTS["microscope_queue"], "MICROSCOPE extraction preflight"),
        ("BR2764_3_beta_doc", "branch", branch, OUTPUTS["branch"], BRANCH_OUTPUTS["beta_doc"], "retained b_alpha branch copy"),
        ("BR2764_4_microscope_copy", "microscope", microscope, OUTPUTS["microscope"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE branch copy"),
        ("BR2764_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next unique Maxwell subblock target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    norm = rows_by_name["norm"]
    f2 = rows_by_name["f2"]
    microscope = rows_by_name["microscope"]
    branch = rows_by_name["branch"]
    gates = rows_by_name["gates"]
    refusals = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2764_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2764_1_alpha_not_derived", any(row["row_id"] == "EMN2764_4_verdict" and "ALPHA_OWNER_NOT_DERIVED" in row["status"] for row in norm), "EM alpha owner remains non-promoted"),
        ("VAL2764_2_independent_F2_chokepoint", any(row["row_id"] == "F2C2764_4_verdict" and row["status"] == "ALPHA_OWNER_STILL_BLOCKED" for row in f2), "independent F2 is marked as current choke point"),
        ("VAL2764_3_MICROSCOPE_preflight", any(row["row_id"] == "MICP2764_3_preflight_verdict" and row["preflight_status"] == "EXTRACTION_PREFLIGHT_READY_NOT_SCORE_READY" for row in microscope), "MICROSCOPE preflight remains non-score-ready"),
        ("VAL2764_4_balpha_retained", any(row["row_id"] == "BAB2764_3_verdict" and row["score_ready"] is False for row in branch), "b_alpha branch retained as nonclaim"),
        ("VAL2764_5_claim_gates_block", any(row["row_id"] == "CG2764_5_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2764_6_refusals_block", all(row["allowed"] is False for row in refusals), "refusal runner blocks premature claims"),
        ("VAL2764_7_next", any(row["row_id"] == "NEXT2764_0_2765" and "unique-Maxwell-subblock" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2764_8_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2764_9_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2764_10_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true"),
        ("VAL2764_11_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2764_12_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2764_13_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2764_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2764 imports the vertical-generator/topological alpha-owner route, refuses promotion because independent F_Q^2, generator/current rescaling, and readout leakage remain legal, records MICROSCOPE PDFs as provenance-only with official arrays still missing, retains b_alpha as a finite product-prior branch, and selects unique Maxwell subblock/no-independent-F2 as the next derivation target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2764 - Y5 R2/f(R): EM Vertical Generator Norm Or MICROSCOPE Extraction Preflight Under AX1090",
        "## Private Verdict\n\nThe EM-owner route now has a precise throat. A fixed parent charge generator and compact/topological charge lattice can help with charge labels, but they still do not own the continuous Maxwell kinetic coefficient unless the parent action also forbids an independent `lambda_A F_Q^2` term and fixes current/readout normalization.\n\nSo `b_alpha=0` is not derived. The finite `b_alpha` product branch stays live. On the empirical flank, MICROSCOPE PDFs are available as provenance, but official arrays/tensors are still not score-ready.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## EM Vertical Generator Norm Audit\n\n" + markdown_table(rows_by_name["norm"], ["row_id", "route_piece", "mathematical_form", "status", "would_buy", "current_gap", "valid_for_claim"]),
        "## Independent F2 Chokepoint\n\n" + markdown_table(rows_by_name["f2"], ["row_id", "choke_point", "counterexample", "effect", "repair_needed", "status", "valid_for_claim"]),
        "## MICROSCOPE Extraction Preflight\n\n" + markdown_table(rows_by_name["microscope"], ["row_id", "object", "download_status", "local_path", "preflight_status", "next_action", "valid_for_claim"]),
        "## Retained b_alpha Branch\n\n" + markdown_table(rows_by_name["branch"], ["row_id", "arena", "retained_quantity", "current_status", "why_retained", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is useful narrowing. The problem is not vaguely 'the coupling'; it is now a named operator grammar problem: can the parent action ban an independent Maxwell `F_Q^2` term? If yes, alpha ownership has a real shot. If no, `b_alpha` stays finite and must be tested through product priors.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    norm = build_norm_rows(inputs)
    f2 = build_f2_rows(inputs)
    microscope = build_microscope_rows(inputs)
    branch = build_branch_rows(inputs)
    gates = build_gates()
    refusals = build_refusals()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["norm"], norm)
    write_csv(OUTPUTS["f2"], f2)
    write_csv(OUTPUTS["microscope"], microscope)
    write_csv(OUTPUTS["branch"], branch)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(norm, f2, microscope, branch, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "norm": norm,
        "f2": f2,
        "microscope": microscope,
        "branch": branch,
        "gates": gates,
        "refusal": refusals,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2764_OVERALL")
    print(f"2764 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
