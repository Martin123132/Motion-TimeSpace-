from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_REAL_LOCAL_ARENA_COEFFICIENT_SOURCE_ACQUISITION_2475"
CHECKPOINT_ID = "2475"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2475-Y5-R2FR-first-real-local-arena-coefficient-source-acquisition.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_SOURCE_REGISTER.csv",
    "acquisition_ledger": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_ACQUISITION_LEDGER.csv",
    "candidate_bound_rows": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS.csv",
    "runner_input_candidates": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv",
    "units_validation": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_UNITS_VALIDATION.csv",
    "claim_gates": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2475_VALIDATION.csv",
}

COPY_TARGETS = {
    "candidate_bound_rows": LOCAL_BOUNDS / "GK_first_real_local_bound_candidates_2475_NONCLAIM.csv",
    "runner_input_candidates": LOCAL_BOUNDS / "GK_first_real_runner_input_candidates_2475_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2475_FIRST_REAL_LOCAL_BOUND_ACQUISITION_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2475_00_2474_doc",
        "source_path": ROOT / "2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md",
        "needles": ["NEXT2474_0_selected", "GATE2474_3_claim_rows", "VAL2474_OVERALL"],
        "role": "handoff selecting first real coefficient/bound source acquisition",
    },
    {
        "source_id": "SRC2475_01_2473_missing",
        "source_path": OUT / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
        "needles": ["MISS2473_6_Karena", "MISS2473_7_thresholds", "MISSING_BOUND_DATA"],
        "role": "missing local arena kernel/bound inputs",
    },
    {
        "source_id": "SRC2475_02_R10_provenance",
        "source_path": LOCAL_BOUNDS / "P8_Y5_R10_BOUND_SOURCE_PROVENANCE.csv",
        "needles": ["EOTWASH_2020_PRL124101101", "38.6", "10.1103/PhysRevLett.124.101101"],
        "role": "R10 source-backed threshold provenance",
    },
    {
        "source_id": "SRC2475_03_R10_candidate_QA",
        "source_path": LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
        "needles": ["QA570_1_anchor_recovery", "pass_review_candidate", "valid_for_claim"],
        "role": "local QA for vector curve review candidate",
    },
    {
        "source_id": "SRC2475_04_R10_review_candidate",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["R10_VECTOR_2020_REVIEW_0154", "review_candidate_only_requires_official_supplement"],
        "role": "nonclaim digitized candidate curve with recovered alpha=1 anchor",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def acquisition_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ2475_0_R10_anchor",
            "R10_short_range",
            "EOTWASH_2020_PRL124101101",
            "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
            "https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761; https://doi.org/10.1103/PhysRevLett.124.101101",
            "10.1103/PhysRevLett.124.101101",
            "95_percent_gravitational_strength_Yukawa_threshold_anchor",
            "alpha=1 excluded for lambda >= 38.6 micrometers",
            "SOURCE_BACKED_ANCHOR_NONCURVE",
            "nonclaim because this is an external bound anchor, not an MTS stress prediction coefficient",
        ),
        (
            "ACQ2475_1_R10_review_curve",
            "R10_short_range",
            "R10_VECTOR_2020_REVIEW_CANDIDATE",
            "Eot-Wash 2020 Fig. 5b vector candidate",
            "local file: source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "10.1103/PhysRevLett.124.101101",
            "axis_calibrated_vector_path_extraction_review_candidate",
            "390 candidate alpha(lambda) rows; alpha=1 anchor recovery passes review candidate QA",
            "REVIEW_CANDIDATE_NONCLAIM",
            "requires official supplemental table or human visual QA before any live claim use",
        ),
        (
            "ACQ2475_2_PPN",
            "PPN_solar_system",
            "not_acquired",
            "PPN bound source",
            "",
            "",
            "not_attempted_this_checkpoint",
            "deferred because R10 source hierarchy was already locally staged",
            "BLOCKED_DEFERRED",
            "future source acquisition needed",
        ),
    ]
    return [
        {
            **base_row(),
            "acquisition_id": i,
            "arena": arena,
            "source_id": source_id,
            "title": title,
            "source_url": source_url,
            "doi": doi,
            "extraction_method": method,
            "acquired_content": content,
            "acquisition_status": status,
            "notes": notes,
        }
        for i, arena, source_id, title, source_url, doi, method, content, status, notes in rows
    ]


def candidate_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BOUND2475_R10_ANCHOR_ALPHA1_38P6UM",
            "R10_short_range",
            "lambda_threshold",
            "3.86e-05",
            "m",
            "alpha_bound",
            "1.0",
            "dimensionless",
            "95_percent",
            "EOTWASH_2020_PRL124101101",
            "https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761",
            "10.1103/PhysRevLett.124.101101",
            "source-backed threshold anchor; not full alpha(lambda) curve",
            "anchor_only_non_curve",
            False,
        ),
        (
            "BOUND2475_R10_REVIEW_NEAREST_ALPHA1",
            "R10_short_range",
            "lambda_candidate_nearest_alpha1",
            "3.866316691563022e-05",
            "m",
            "alpha_bound",
            "0.9915372447041295",
            "dimensionless",
            "review_candidate",
            "R10_VECTOR_2020_REVIEW_0154",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "10.1103/PhysRevLett.124.101101",
            "local review candidate recovered alpha=1 anchor with lambda_relative_error about 0.00164",
            "review_candidate_requires_human_or_official_QA",
            False,
        ),
    ]
    return [
        {
            **base_row(),
            "bound_id": i,
            "arena": arena,
            "bound_kind": kind,
            "lambda_value": lambda_value,
            "lambda_units": lambda_units,
            "bound_symbol": symbol,
            "bound_value": bound_value,
            "bound_units": units,
            "confidence": confidence,
            "source_id": source_id,
            "source_path_or_url": source,
            "doi": doi,
            "notes": notes,
            "data_status": status,
            "valid_for_claim": valid,
            "claim_allowed": False,
        }
        for i, arena, kind, lambda_value, lambda_units, symbol, bound_value, units, confidence, source_id, source, doi, notes, status, valid in rows
    ]


def runner_input_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN2475_R10_ANCHOR_INPUT",
            "R10_short_range",
            "",
            "",
            "",
            "1.0",
            "dimensionless",
            "BOUND2475_R10_ANCHOR_ALPHA1_38P6UM",
            False,
            "MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;ANCHOR_ONLY_NONCURVE",
        ),
        (
            "RUN2475_R10_REVIEW_INPUT",
            "R10_short_range",
            "",
            "",
            "",
            "0.9915372447041295",
            "dimensionless",
            "BOUND2475_R10_REVIEW_NEAREST_ALPHA1",
            False,
            "MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;REVIEW_CANDIDATE_NONCLAIM",
        ),
    ]
    return [
        {
            **base_row(),
            "runner_input_id": i,
            "arena": arena,
            "E_GK_bound": egk,
            "C_metric": cmetric,
            "K_arena": karena,
            "arena_bound": arena_bound,
            "units": units,
            "bound_row_id": bound_row_id,
            "valid_for_claim": valid,
            "block_reasons": block_reasons,
            "claim_allowed": False,
        }
        for i, arena, egk, cmetric, karena, arena_bound, units, bound_row_id, valid, block_reasons in rows
    ]


def units_validation_rows(bounds: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bound in bounds:
        lambda_ok = bound["lambda_units"] == "m" and float(bound["lambda_value"]) > 0
        bound_ok = bound["bound_units"] == "dimensionless" and float(bound["bound_value"]) > 0
        rows.append({**base_row(), "validation_id": f"UNIT2475_{bound['bound_id']}", "target_id": bound["bound_id"], "lambda_units_ok": lambda_ok, "bound_units_ok": bound_ok, "status": "PASS_UNITS_NONCLAIM" if lambda_ok and bound_ok else "FAIL_UNITS", "claim_allowed": False})
    for runner in runners:
        numeric_missing = any(runner[field] == "" for field in ["E_GK_bound", "C_metric", "K_arena"])
        units_ok = runner["units"] == "dimensionless"
        rows.append({**base_row(), "validation_id": f"UNIT2475_{runner['runner_input_id']}", "target_id": runner["runner_input_id"], "lambda_units_ok": "not_applicable", "bound_units_ok": units_ok, "status": "BLOCKED_MISSING_RUNNER_COEFFICIENTS" if numeric_missing else "PASS_RUNNER_UNITS", "claim_allowed": False})
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2475_0_real_bound_anchor", "A real source-backed R10 bound anchor is recorded.", "PASS_AS_BOUND_SOURCE", "Eot-Wash 2020 alpha=1 threshold anchor recorded with DOI/URLs", True, False),
        ("GATE2475_1_full_curve", "A full valid-for-claim alpha(lambda) curve is acquired.", "BLOCKED", "digitized curve remains review_candidate_nonclaim", False, False),
        ("GATE2475_2_runner_claim", "Runner has enough sourced MTS coefficients to claim local compatibility.", "BLOCKED", "E_GK_bound, C_metric and K_R10 missing", False, False),
        ("GATE2475_3_no_fitted_GM", "No fitted-GM shortcut used.", "PASS_GUARDRAIL", "R10 source anchor does not define MTS source strength by orbital GM", True, False),
        ("GATE2475_4_local_GR", "local GR/PPN branch passes.", "BLOCKED", "external bound acquisition is not a GR derivation", False, False),
        ("GATE2475_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private source acquisition only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2475_0_anchor_acquired", "Keep Eöt-Wash 2020 as first real R10 bound anchor.", "source-backed DOI/URL and threshold value are available", "bound source gap partially reduced"),
        ("DEC2475_1_no_curve_promotion", "Do not promote the digitized curve.", "review candidate still needs official supplemental table or human visual QA", "claim discipline retained"),
        ("DEC2475_2_next", "Next source or derive K_R10/C_metric/E_GK_bound mapping.", "external bound alone cannot run the stress-bound test", "2476 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2475_0_selected",
            "selection_status": "selected",
            "target_file": "2476-Y5-R2FR-R10-kernel-and-Cmetric-source-map-or-blocker.md",
            "target_script": "scripts/Y5_R2FR_R10_kernel_and_Cmetric_source_map_or_blocker_2476.py",
            "task": "try to source or derive the R10 arena kernel K_R10 and C_metric mapping from GK stress bound to alpha(lambda); if absent, write a blocker ledger",
            "acceptance_target": "kernel/mapping source audit, dimensional bridge, missing coefficient blocker, no fitted-GM guardrail, claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["candidate_bound_rows"], COPY_TARGETS["candidate_bound_rows"])
    shutil.copyfile(OUTPUTS["runner_input_candidates"], COPY_TARGETS["runner_input_candidates"])
    shutil.copyfile(OUTPUTS["acquisition_ledger"], COPY_TARGETS["acquisition_queue"])
    source_map = {
        "candidate_bound_rows": OUTPUTS["candidate_bound_rows"],
        "runner_input_candidates": OUTPUTS["runner_input_candidates"],
        "acquisition_queue": OUTPUTS["acquisition_ledger"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2475_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited local source paths exist and needles are present")
    add("VAL2475_01_real_anchor", any(row["bound_id"] == "BOUND2475_R10_ANCHOR_ALPHA1_38P6UM" for row in data["bounds"]), "R10 alpha=1 threshold anchor recorded")
    add("VAL2475_02_urls_doi", any("10.1103/PhysRevLett.124.101101" in row["doi"] and "arxiv.org" in row["source_path_or_url"] for row in data["bounds"]), "source URL and DOI recorded")
    add("VAL2475_03_units", all(row["status"] in {"PASS_UNITS_NONCLAIM", "BLOCKED_MISSING_RUNNER_COEFFICIENTS"} for row in data["units"]), "units validation rows pass or block as expected")
    add("VAL2475_04_runner_blocked", all(row["valid_for_claim"] is False or str(row["valid_for_claim"]) == "False" for row in data["runners"]), "runner input candidates remain nonclaim")
    add("VAL2475_05_missing_coefficients", all("MISSING" in row["block_reasons"] for row in data["runners"]), "runner rows still block missing MTS coefficients")
    add("VAL2475_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/R10 claim")
    add("VAL2475_07_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2475_0_selected", "2476 R10 kernel/Cmetric source map selected")
    add("VAL2475_08_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2475-Y5", "P8_Y5_GK_BOUND_SOURCE_2475", "P8_Y5_BRR545_2475", "JR2475")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2475_09_no_formalization_artifacts", not formal_hits, "no 2475 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2475_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2475_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2475_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2475_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2475_OVERALL", all(row["status"] == "PASS" for row in rows), "2475 acquires a real R10 bound anchor but keeps MTS runner claims blocked pending kernel/Cmetric/E_GK coefficients")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2475 Y5 R2FR First Real Local Arena Coefficient Source Acquisition",
        "",
        "**Status:** first real local arena bound anchor acquired, but no MTS local-test claim is allowed. The R10/Eöt-Wash 2020 alpha=1 threshold at lambda 38.6 micrometers is source-backed by PRL/PubMed/arXiv metadata. The stress-bound runner remains blocked because `E_GK_bound`, `C_metric`, and `K_R10` are still missing.",
        "",
        "**Meaning:** this reduces the external-bound side of the local test pipeline. It does not reduce the theory-side coefficient gap. The next step is the harder bridge: map GK stress residuals to a Yukawa alpha(lambda) kernel without fitted-GM or M_H_ref shortcuts.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Acquisition Ledger",
        markdown_table(data["acquisition"], ["acquisition_id", "arena", "source_id", "title", "source_url", "doi", "extraction_method", "acquired_content", "acquisition_status", "notes"]),
        "",
        "## Candidate Bound Rows",
        markdown_table(data["bounds"], ["bound_id", "arena", "bound_kind", "lambda_value", "lambda_units", "bound_symbol", "bound_value", "bound_units", "confidence", "source_id", "source_path_or_url", "data_status", "valid_for_claim"]),
        "",
        "## Runner Input Candidates",
        markdown_table(data["runners"], ["runner_input_id", "arena", "E_GK_bound", "C_metric", "K_arena", "arena_bound", "units", "bound_row_id", "valid_for_claim", "block_reasons", "claim_allowed"]),
        "",
        "## Units Validation",
        markdown_table(data["units"], ["validation_id", "target_id", "lambda_units_ok", "bound_units_ok", "status", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    bounds = candidate_bound_rows()
    runners = runner_input_candidate_rows()
    data = {
        "sources": source_register(),
        "acquisition": acquisition_ledger_rows(),
        "bounds": bounds,
        "runners": runners,
        "units": units_validation_rows(bounds, runners),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["acquisition_ledger"], data["acquisition"])
    write_csv(OUTPUTS["candidate_bound_rows"], data["bounds"])
    write_csv(OUTPUTS["runner_input_candidates"], data["runners"])
    write_csv(OUTPUTS["units_validation"], data["units"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
