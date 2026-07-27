from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
EXT = ROOT / "source-intake" / "external_sources"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3484-Y5-R2FR-fourth-nonWEP-row-or-QEarth-kernel-exclusion-theorem.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]
SCAN_NAME_HINTS = [
    "CLOCK",
    "ALPHA",
    "MASS",
    "MU",
    "PPN",
    "ORBIT",
    "DD",
    "R2FR_347",
    "R2FR_348",
    "R10_646",
    "R10_647",
    "R10_778",
]
MAX_SCAN_ROWS_TOTAL = 40000
MAX_SCAN_ROWS_PER_FILE = 750

SOURCES: dict[str, dict[str, Any]] = {
    "script_3484": {"path": Path(__file__).resolve(), "role": "generator", "url": ""},
    "doc_3483": {
        "path": ROOT / "3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md",
        "role": "3483 blind direction theorem",
        "url": "",
    },
    "blind_3483": {
        "path": OUT / "P8_Y5_R2FR_3483_BLIND_DIRECTION_LEDGER.csv",
        "role": "one-dimensional current blind vector",
        "url": "",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "current WEP plus clock vectors",
        "url": "",
    },
    "flambaum_tedesco_2006": {
        "path": EXT / "Flambaum_Tedesco_2006_nuclear_magnetic_moments_quark_masses_atomic_clocks.pdf",
        "role": "candidate hyperfine/nuclear magnetic moment quark-mass sensitivity source",
        "url": "https://arxiv.org/abs/nucl-th/0601050",
    },
    "berengut_flambaum_kava_2011": {
        "path": EXT / "Berengut_Flambaum_Kava_2011_isotope_comparisons_quark_mass_variation.pdf",
        "role": "candidate isotope-comparison quark-mass sensitivity source",
        "url": "https://arxiv.org/abs/1109.1893",
    },
    "dinh_dunning_dzuba_flambaum_2009": {
        "path": EXT / "Dinh_Dunning_Dzuba_Flambaum_2009_hyperfine_radius_quark_mass_variation.pdf",
        "role": "candidate hyperfine/radius quark-mass sensitivity source",
        "url": "https://arxiv.org/abs/0903.2090",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if math.isnan(value):
        return "nan"
    return f"{value:.12e}"


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: list[float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: list[float]) -> list[float]:
    length = norm(a)
    return [0.0 for _ in a] if length == 0 else [x / length for x in a]


def rref(matrix: list[list[float]], tol: float = 1e-12) -> tuple[list[list[float]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    pivot_row = 0
    pivots: list[int] = []
    for col in range(len(rows[0])):
        best = max(range(pivot_row, len(rows)), key=lambda idx: abs(rows[idx][col]), default=pivot_row)
        if abs(rows[best][col]) <= tol:
            continue
        rows[pivot_row], rows[best] = rows[best], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for idx in range(len(rows)):
            if idx == pivot_row:
                continue
            factor = rows[idx][col]
            if abs(factor) > tol:
                rows[idx] = [value - factor * pivot for value, pivot in zip(rows[idx], rows[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def rank(matrix: list[list[float]]) -> int:
    return len(rref(matrix)[1])


def blind_vector() -> list[float]:
    for row in read_csv(SOURCES["blind_3483"]["path"]):
        if row["blind_id"] == "BLIND3483_2_QEarth_plus_two_clocks":
            return [
                float(row["unit_null_D_hatm_eff"]),
                float(row["unit_null_D_delta_m_eff"]),
                float(row["unit_null_D_me_eff"]),
                float(row["unit_null_D_e_eff"]),
            ]
    raise ValueError("3483 blind vector not found")


def vector_from_matrix_row(row: dict[str, str], prefix: str = "raw") -> list[float]:
    return [float(row[f"{prefix}_{channel}"]) for channel in CHANNELS]


def current_rows() -> tuple[list[dict[str, str]], list[float], list[list[float]]]:
    rows = read_csv(SOURCES["matrix_3475"]["path"])
    clock_rows = [row for row in rows if row["row_type"].startswith("clock_")]
    q_earth_row = read_csv(OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv")[0]
    q_earth = [
        float(q_earth_row["Q_hatm_full_Earth"]),
        float(q_earth_row["Q_delta_m_Earth"]),
        float(q_earth_row["Q_m_e_Earth"]),
        float(q_earth_row["Q_e_full_Earth"]),
    ]
    return clock_rows, q_earth, [q_earth] + [vector_from_matrix_row(row) for row in clock_rows]


def vector_from_any_row(row: dict[str, str]) -> tuple[list[float] | None, str]:
    prefixes = ["raw", "unit", ""]
    for prefix in prefixes:
        fields = [f"{prefix}_{channel}" if prefix else channel for channel in CHANNELS]
        if all(field in row for field in fields):
            try:
                values = [float(row[field]) for field in fields]
            except (TypeError, ValueError):
                continue
            if norm(values) > 0:
                return values, prefix or "plain"
    aliases = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]
    if all(field in row for field in aliases):
        try:
            values = [float(row[field]) for field in aliases]
        except (TypeError, ValueError):
            return None, ""
        if norm(values) > 0:
            return values, "plain"
    return None, ""


def row_label(path: Path, row: dict[str, str], index: int) -> str:
    for key in ["aug_row_id", "clock_row_id", "row_id", "candidate_id", "source_id", "theorem_id", "fill_id"]:
        if row.get(key):
            return row[key]
    return f"{path.stem}:{index}"


def classify_row(path: Path, row: dict[str, str]) -> tuple[str, bool]:
    text = " ".join([path.name] + [str(value) for value in row.values()]).lower()
    row_type = row.get("row_type", "").lower()
    is_wep = row_type == "wep_material_difference" or ("wep_material" in text and "clock" not in text)
    if is_wep:
        return "wep_row_forbidden_for_same_vector_linear_closure", True
    if "clock" in text:
        return "clock_or_clock_candidate", False
    if "orbit" in text or "ppn" in text:
        return "local_gr_or_orbital_candidate", False
    if "formula" in text or "charge" in text or "dd_" in text:
        return "formula_or_charge_vector_not_observable", False
    return "unclassified_numeric_vector", False


def scan_existing_vectors(blind: list[float], base_rows: list[list[float]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    candidates: list[dict[str, Any]] = []
    scanned_files = 0
    scanned_rows = 0
    numeric_vectors = 0
    skipped_files = 0
    for path in sorted(OUT.glob("*.csv")):
        if path.name.startswith("P8_Y5_R2FR_3484_") or path.name == "P8_Y5_BRR545_3484_VALIDATION.csv":
            continue
        if not any(hint in path.name.upper() for hint in SCAN_NAME_HINTS):
            skipped_files += 1
            continue
        if scanned_rows >= MAX_SCAN_ROWS_TOTAL:
            break
        scanned_files += 1
        try:
            rows = read_csv(path)
        except Exception:
            continue
        for index, row in enumerate(rows[:MAX_SCAN_ROWS_PER_FILE], start=2):
            if scanned_rows >= MAX_SCAN_ROWS_TOTAL:
                break
            scanned_rows += 1
            vector, basis = vector_from_any_row(row)
            if vector is None:
                continue
            numeric_vectors += 1
            vector_unit = normalize(vector)
            projection = dot(vector_unit, blind)
            classification, forbidden = classify_row(path, row)
            new_rank = rank(base_rows + [vector])
            closes_rank = new_rank >= 4 and not forbidden
            source_path = row.get("source_path") or row.get("resolved_path") or str(path)
            candidates.append(
                {
                    "candidate_id": f"SCAN3484_{len(candidates):04d}",
                    "file": str(path),
                    "line_hint": index,
                    "row_label": row_label(path, row, index),
                    "basis": basis,
                    "classification": classification,
                    "forbidden_as_linear_same_vector_WEP": str(forbidden),
                    "D_hatm_eff": fmt(vector[0]),
                    "D_delta_m_eff": fmt(vector[1]),
                    "D_me_eff": fmt(vector[2]),
                    "D_e_eff": fmt(vector[3]),
                    "projection_on_3483_blind": fmt(projection),
                    "abs_projection_on_3483_blind": fmt(abs(projection)),
                    "rank_if_added_to_QEarth_plus_clocks": new_rank,
                    "closes_current_rank_if_source_valid": str(closes_rank),
                    "source_path_or_row_origin": source_path,
                    "row_valid_for_claim": row.get("valid_for_claim", "missing"),
                    "valid_for_claim": "False",
                }
            )
    candidates.sort(key=lambda row: (row["closes_current_rank_if_source_valid"] != "True", -float(row["abs_projection_on_3483_blind"])))
    return candidates[:80], {
        "scanned_files": scanned_files,
        "skipped_files": skipped_files,
        "scanned_rows": scanned_rows,
        "numeric_vectors": numeric_vectors,
    }


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "source_url": meta["url"],
            "valid_for_claim": "False",
        }
        for source_id, meta in SOURCES.items()
    ]


def blind_probe_rows(blind: list[float], base_rows: list[list[float]]) -> list[dict[str, Any]]:
    return [
        {
            "probe_id": "PROBE3484_0_current_blind_vector",
            "D_hatm_eff": fmt(blind[0]),
            "D_delta_m_eff": fmt(blind[1]),
            "D_me_eff": fmt(blind[2]),
            "D_e_eff": fmt(blind[3]),
            "interpretation": "the surviving same-vector blind direction is overwhelmingly D_delta_m_eff-like",
            "valid_for_claim": "False",
        },
        {
            "probe_id": "PROBE3484_1_current_rank",
            "D_hatm_eff": "",
            "D_delta_m_eff": "",
            "D_me_eff": "",
            "D_e_eff": "",
            "interpretation": f"rank(Q_Earth plus current two clock rows)={rank(base_rows)}; need rank 4 or parent exclusion of the blind kernel",
            "valid_for_claim": "False",
        },
    ]


def external_acquisition_rows(blind: list[float]) -> list[dict[str, Any]]:
    return [
        {
            "target_id": "EXT3484_0_hyperfine_nuclear_magnetic_moments",
            "local_source_path": str(SOURCES["flambaum_tedesco_2006"]["path"]),
            "source_url": SOURCES["flambaum_tedesco_2006"]["url"],
            "needed_extraction": "sensitivity vector in DD four-channel basis, especially whether any term maps to D_delta_m_eff rather than only D_hatm_eff",
            "projection_test": "abs(row dot u_blind_3483) > 0 after basis mapping",
            "current_status": "SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING",
            "valid_for_claim": "False",
        },
        {
            "target_id": "EXT3484_1_isotope_comparison_quark_mass",
            "local_source_path": str(SOURCES["berengut_flambaum_kava_2011"]["path"]),
            "source_url": SOURCES["berengut_flambaum_kava_2011"]["url"],
            "needed_extraction": "isotope clock/comparison sensitivity to quark-mass variation and its map to the D_delta_m_eff blind direction",
            "projection_test": "abs(row dot u_blind_3483) > 0 after basis mapping",
            "current_status": "SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING",
            "valid_for_claim": "False",
        },
        {
            "target_id": "EXT3484_2_hyperfine_radius_quark_mass",
            "local_source_path": str(SOURCES["dinh_dunning_dzuba_flambaum_2009"]["path"]),
            "source_url": SOURCES["dinh_dunning_dzuba_flambaum_2009"]["url"],
            "needed_extraction": "hyperfine/radius sensitivity row; reject if it only spans already-covered hatm/me/e directions",
            "projection_test": "abs(row dot u_blind_3483) > 0 after basis mapping",
            "current_status": "SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closing = [row for row in candidates if row["closes_current_rank_if_source_valid"] == "True"]
    valid_closing = [row for row in closing if str(row["row_valid_for_claim"]).lower() == "true"]
    return [
        {
            "theorem_id": "THM3484_0_projection_gate",
            "statement": "A fourth non-WEP row closes the current same-vector blind direction only if its vector has nonzero projection on the 3483 null vector.",
            "proof": "The current row span has codimension one; a new row raises rank from 3 to 4 exactly when it is not orthogonal to the null vector.",
            "result": f"scanner found {len(closing)} row(s) that algebraically close rank before source/claim filtering; {len(valid_closing)} are claim-valid rows.",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3484_1_delta_m_target",
            "statement": "The missing direction is dominantly D_delta_m_eff, so another alpha/me/hatm-only clock row is unlikely to close the local branch.",
            "proof": "The 3483 null vector has unit component nearly entirely in D_delta_m_eff.",
            "result": "target hyperfine/isotope sources must be basis-mapped before use; quark-mass average sensitivity is not automatically D_delta_m_eff sensitivity.",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closing = [row for row in candidates if row["closes_current_rank_if_source_valid"] == "True"]
    return [
        {
            "decision_id": "DEC3484_0_no_existing_claim_row",
            "decision": "No existing row is promoted to a same-vector local-GR/WEP closure claim.",
            "rationale": "the scan is algebraic and source/transport filters remain nonclaim; WEP rows remain forbidden as linear closures on the same-vector branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3484_1_best_attack",
            "decision": "Extract one genuine non-WEP hyperfine/isotope sensitivity vector and test its projection on the 3483 blind vector.",
            "rationale": f"{len(closing)} algebraic closing rows were found in local CSVs before claim filtering; external candidate sources are now local PDFs.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3485-Y5-R2FR-hyperfine-isotope-DD-basis-extraction-or-delta-m-kernel-exclusion.md",
            "next_script": "scripts/Y5_R2FR_3485_hyperfine_isotope_DD_basis_extraction_or_delta_m_kernel_exclusion.py",
            "objective": "Extract a source-backed hyperfine/isotope sensitivity row into the DD four-channel basis and test whether it has nonzero projection on the 3483 blind vector.",
            "success_gate": "rank(Q_Earth, current clock rows, new non-WEP row)=4 with sourced basis map, or parent theorem excludes the D_delta_m_eff-like kernel",
            "forbidden_shortcuts": "mapping average quark-mass sensitivity to D_delta_m_eff without a source; using WEP rows linearly; claiming local GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], stats: dict[str, int], candidates: list[dict[str, Any]], base_rows: list[list[float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3484_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all local and acquired external sources exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3484_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3484_2_scanner_coverage", "passed": stats["scanned_files"] > 20 and stats["numeric_vectors"] > 0, "detail": f"files={stats['scanned_files']}; skipped={stats['skipped_files']}; rows={stats['scanned_rows']}; numeric_vectors={stats['numeric_vectors']}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3484_3_current_rank_still_three", "passed": rank(base_rows) == 3, "detail": f"rank={rank(base_rows)}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3484_4_no_claim_valid_closure", "passed": all(row["valid_for_claim"] == "False" for row in candidates), "detail": "candidate rows are scan/projection rows only", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3484_5_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3484_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(blind: list[float], stats: dict[str, int], probe: list[dict[str, Any]], theorem: list[dict[str, Any]], external: list[dict[str, Any]], candidates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    top_candidates = candidates[:12]
    DOC.write_text(
        "\n".join(
            [
                "# 3484: Fourth Non-WEP Row Or `Q_Earth` Kernel Exclusion Theorem",
                "",
                "## Current Verdict",
                "- The 3483 blind direction is real and is dominantly `D_delta_m_eff`.",
                "- A fourth non-WEP row can close the same-vector branch only if it projects onto that blind vector.",
                "- The local CSV scan was performed instead of guessing; no row is promoted to a claim.",
                "- Three primary hyperfine/isotope candidate sources were acquired locally for the next extraction pass.",
                "",
                "## Blind Probe",
                md_table(probe, ["probe_id", "D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff", "interpretation", "valid_for_claim"]),
                "",
                "## Projection Theorems",
                md_table(theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Scan Summary",
                f"- Files scanned: `{stats['scanned_files']}`",
                f"- Files skipped by targeted name filter: `{stats['skipped_files']}`",
                f"- Rows scanned: `{stats['scanned_rows']}`",
                f"- Numeric four-channel vectors found: `{stats['numeric_vectors']}`",
                f"- Blind vector used: `({fmt(blind[0])}, {fmt(blind[1])}, {fmt(blind[2])}, {fmt(blind[3])})`",
                "",
                "## External Acquisition Targets",
                md_table(external, ["target_id", "local_source_path", "source_url", "needed_extraction", "projection_test", "current_status", "valid_for_claim"]),
                "",
                "## Top Local Projection Candidates",
                md_table(top_candidates, ["candidate_id", "file", "line_hint", "row_label", "classification", "projection_on_3483_blind", "rank_if_added_to_QEarth_plus_clocks", "closes_current_rank_if_source_valid", "row_valid_for_claim", "valid_for_claim"]),
                "",
                "## Decisions",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    blind = normalize(blind_vector())
    clock_rows, q_earth, base_rows = current_rows()
    probe = blind_probe_rows(blind, base_rows)
    candidates, stats = scan_existing_vectors(blind, base_rows)
    external = external_acquisition_rows(blind)
    theorem = theorem_rows(candidates)
    decisions = decision_rows(candidates)
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3484_SOURCE_REGISTER.csv",
        "blind_probe": OUT / "P8_Y5_R2FR_3484_BLIND_PROBE.csv",
        "projection_theorems": OUT / "P8_Y5_R2FR_3484_PROJECTION_THEOREMS.csv",
        "existing_vector_scan": OUT / "P8_Y5_R2FR_3484_EXISTING_VECTOR_SCAN_TOP.csv",
        "external_acquisition": OUT / "P8_Y5_R2FR_3484_EXTERNAL_SOURCE_ACQUISITION_TARGETS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3484_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3484_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "source_url", "valid_for_claim"])
    write_csv(outputs["blind_probe"], probe, ["probe_id", "D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff", "interpretation", "valid_for_claim"])
    write_csv(outputs["projection_theorems"], theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(
        outputs["existing_vector_scan"],
        candidates,
        [
            "candidate_id",
            "file",
            "line_hint",
            "row_label",
            "basis",
            "classification",
            "forbidden_as_linear_same_vector_WEP",
            "D_hatm_eff",
            "D_delta_m_eff",
            "D_me_eff",
            "D_e_eff",
            "projection_on_3483_blind",
            "abs_projection_on_3483_blind",
            "rank_if_added_to_QEarth_plus_clocks",
            "closes_current_rank_if_source_valid",
            "source_path_or_row_origin",
            "row_valid_for_claim",
            "valid_for_claim",
        ],
    )
    write_csv(outputs["external_acquisition"], external, ["target_id", "local_source_path", "source_url", "needed_extraction", "projection_test", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, stats, candidates, base_rows)
    validation_path = OUT / "P8_Y5_BRR545_3484_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(blind, stats, probe, theorem, external, candidates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
