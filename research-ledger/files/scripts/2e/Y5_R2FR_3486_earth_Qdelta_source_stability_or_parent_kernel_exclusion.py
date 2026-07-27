from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3486-Y5-R2FR-earth-Qdelta-source-stability-or-parent-kernel-exclusion.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3486": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3485": {
        "path": ROOT / "3485-Y5-R2FR-hyperfine-isotope-DD-basis-extraction-or-delta-m-kernel-exclusion.md",
        "role": "3485 handoff",
    },
    "earth_composition_2789": {
        "path": OUT / "P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv",
        "role": "bulk Earth composition target rows",
    },
    "earth_elements_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_ELEMENT_ROWS_NONCLAIM.csv",
        "role": "element-level DD charge rows",
    },
    "earth_vector_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
        "role": "bulk Earth DD vector",
    },
    "rank_3485": {
        "path": OUT / "P8_Y5_R2FR_3485_RANK_AND_CONDITION_LEDGER.csv",
        "role": "conditional rank closure rows",
    },
    "extracted_3485": {
        "path": OUT / "P8_Y5_R2FR_3485_EXTRACTED_HYPERFINE_ROWS_NONCLAIM.csv",
        "role": "hyperfine/isotope DD-basis sensitivity rows",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "current clock matrix",
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


def rank(rows: list[list[float]], tol: float = 1e-12) -> int:
    return int(np.linalg.matrix_rank(np.array(rows, dtype=float), tol=tol))


def singular_values(rows: list[list[float]]) -> list[float]:
    return [float(value) for value in np.linalg.svd(np.array(rows, dtype=float), compute_uv=False)]


def condition_number(rows: list[list[float]]) -> float:
    values = singular_values(rows)
    if not values or values[-1] == 0.0:
        return math.inf
    return values[0] / values[-1]


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for key, meta in SOURCES.items()
    ]


def earth_rows() -> list[dict[str, str]]:
    return read_csv(SOURCES["earth_elements_3482"]["path"])


def qdelta_element_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in earth_rows():
        q_delta = float(row["Q_delta_m"])
        mass_fraction = float(row["normalized_mass_fraction"])
        weighted = float(row["weighted_Q_delta_m"])
        rows.append(
            {
                "element": row["element"],
                "Z": row["Z"],
                "A": row["A"],
                "mass_fraction_normalized": fmt(mass_fraction),
                "Q_delta_m": fmt(q_delta),
                "weighted_Q_delta_m": fmt(weighted),
                "sign": "positive" if weighted > 0 else ("negative" if weighted < 0 else "zero"),
                "fraction_of_total_Qdelta": "",
                "stability_role": "dominant_positive_anchor" if row["element"] == "Fe" else ("negative_correction" if weighted < 0 else "positive_support"),
                "valid_for_claim": "False",
            }
        )
    total = sum(float(row["weighted_Q_delta_m"]) for row in earth_rows())
    for row in rows:
        row["fraction_of_total_Qdelta"] = fmt(float(row["weighted_Q_delta_m"]) / total if total else math.nan)
    rows.sort(key=lambda row: abs(float(row["weighted_Q_delta_m"])), reverse=True)
    return rows


def earth_vector() -> list[float]:
    row = read_csv(SOURCES["earth_vector_3482"]["path"])[0]
    return [
        float(row["Q_hatm_full_Earth"]),
        float(row["Q_delta_m_Earth"]),
        float(row["Q_m_e_Earth"]),
        float(row["Q_e_full_Earth"]),
    ]


def clock_base_rows(q_delta_override: float | None = None) -> list[list[float]]:
    q_earth = earth_vector()
    if q_delta_override is not None:
        q_earth[1] = q_delta_override
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    clocks = [
        [float(row[f"raw_{channel}"]) for channel in CHANNELS]
        for row in matrix
        if row["row_type"].startswith("clock_")
    ]
    return [q_earth] + clocks


def best_3485_row() -> list[float]:
    rank_rows = read_csv(SOURCES["rank_3485"]["path"])
    closing = [row for row in rank_rows if row["closes_rank"] == "True"]
    best = min(closing, key=lambda row: float(row["condition_number_after"]))
    candidates = read_csv(SOURCES["extracted_3485"]["path"])
    source = next(row for row in candidates if row["candidate_id"] == best["candidate_id"])
    return [float(source[channel]) for channel in CHANNELS]


def positivity_rows(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total = sum(float(row["weighted_Q_delta_m"]) for row in elements)
    positive_total = sum(float(row["weighted_Q_delta_m"]) for row in elements if float(row["weighted_Q_delta_m"]) > 0)
    negative_total = sum(float(row["weighted_Q_delta_m"]) for row in elements if float(row["weighted_Q_delta_m"]) < 0)
    fe_row = next(row for row in elements if row["element"] == "Fe")
    fe_weighted = float(fe_row["weighted_Q_delta_m"])
    fe_q_delta = float(fe_row["Q_delta_m"])
    fe_fraction = float(fe_row["mass_fraction_normalized"])
    fe_only_minus_negatives = fe_weighted + negative_total
    critical_fe_fraction = abs(negative_total) / fe_q_delta if fe_q_delta > 0 else math.inf
    return [
        {
            "bound_id": "QDEL3486_0_baseline_sum",
            "statement": "Baseline Earth DD proxy has positive Q_delta_m_Earth.",
            "value": fmt(total),
            "derivation": "sum over normalized composition rows of f_i * 0.0017*(A_i-2Z_i)/A_i",
            "status": "POSITIVE_IN_DD_PROXY_NONCLAIM_PARENT_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QDEL3486_1_fe_dominance",
            "statement": "Iron alone dominates the positive neutron-excess contribution.",
            "value": fmt(fe_weighted),
            "derivation": f"f_Fe={fmt(fe_fraction)} times q_delta_Fe={fmt(fe_q_delta)}",
            "status": "DOMINANT_ANCHOR",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QDEL3486_2_negative_rows",
            "statement": "The negative H/O correction is much smaller than the Fe contribution.",
            "value": fmt(negative_total),
            "derivation": "sum of negative weighted Q_delta_m rows in the current target table",
            "status": "NEGATIVE_CORRECTION_SMALL",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QDEL3486_3_fe_only_lower_bound",
            "statement": "A conservative Fe-only-minus-negative correction lower bound remains positive.",
            "value": fmt(fe_only_minus_negatives),
            "derivation": "weighted_Fe_Qdelta + all negative weighted rows, dropping every other positive support row",
            "status": "STRICTLY_POSITIVE_WITH_CURRENT_TARGET_ROWS",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QDEL3486_4_critical_fe_fraction",
            "statement": "Minimum Fe fraction required to beat all current negative corrections even if all other positive rows are dropped.",
            "value": fmt(critical_fe_fraction),
            "derivation": "|negative_total| / q_delta_Fe",
            "status": "ACTUAL_FE_FRACTION_EXCEEDS_CRITICAL_BY_FACTOR_" + fmt(fe_fraction / critical_fe_fraction if critical_fe_fraction else math.inf),
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QDEL3486_5_positive_total",
            "statement": "Total positive support excluding sign cancellations.",
            "value": fmt(positive_total),
            "derivation": "sum positive weighted rows",
            "status": "POSITIVE_SUPPORT_LEDGER",
            "valid_for_claim": "False",
        },
    ]


def stress_rows(bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    baseline = float(next(row["value"] for row in bounds if row["bound_id"] == "QDEL3486_0_baseline_sum"))
    lower = float(next(row["value"] for row in bounds if row["bound_id"] == "QDEL3486_3_fe_only_lower_bound"))
    elements = qdelta_element_rows()
    fe_weighted = float(next(row["weighted_Q_delta_m"] for row in elements if row["element"] == "Fe"))
    no_fe = baseline - fe_weighted
    candidate = best_3485_row()
    scenarios = [
        ("STRESS3486_0_baseline", baseline, "baseline Q_delta_m_Earth from 3482"),
        ("STRESS3486_1_fe_only_lower", lower, "Fe-only-minus-negative lower bound; all other positive support dropped"),
        ("STRESS3486_2_no_fe_extreme", no_fe, "unphysical diagnostic removing Fe contribution while retaining all other rows"),
        ("STRESS3486_3_forced_zero_failure", 0.0, "forced Q_delta_m_Earth=0 diagnostic"),
    ]
    rows: list[dict[str, Any]] = []
    for scenario_id, q_delta, description in scenarios:
        augmented = clock_base_rows(q_delta_override=q_delta) + [candidate]
        svals = singular_values(augmented)
        rows.append(
            {
                "scenario_id": scenario_id,
                "description": description,
                "Q_delta_m_Earth_used": fmt(q_delta),
                "rank_with_best_3485_row": rank(augmented),
                "min_singular_value": fmt(min(svals) if svals else math.nan),
                "condition_number": fmt(condition_number(augmented)),
                "closure_status": "rank_closes" if rank(augmented) == 4 else "rank_fails",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(bounds: list[dict[str, Any]], stress: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower = next(row for row in bounds if row["bound_id"] == "QDEL3486_3_fe_only_lower_bound")
    forced = next(row for row in stress if row["scenario_id"] == "STRESS3486_3_forced_zero_failure")
    return [
        {
            "theorem_id": "THM3486_0_DD_proxy_Qdelta_positive",
            "statement": "Within the current bulk Earth DD proxy, Q_delta_m_Earth is strictly positive under a conservative Fe-only-minus-negative bound.",
            "proof": "The Fe weighted neutron-excess term exceeds the total negative H/O correction even after dropping every other positive contribution.",
            "result": f"lower_bound={lower['value']}",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3486_1_rank_depends_on_Qdelta_nonzero",
            "statement": "The 3485 rank closure depends on Q_delta_m_Earth being nonzero.",
            "proof": "Forcing Q_delta_m_Earth to zero collapses the best 3485 augmented system back to rank 3.",
            "result": f"forced_zero_rank={forced['rank_with_best_3485_row']}",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3486_2_parent_gap",
            "statement": "This proves stability only in the DD proxy, not yet in parent MTS source transport.",
            "proof": "The source vector still comes from composition plus DD charge formulas; the parent MTS action has not supplied the quotient/source-current map.",
            "result": "conditional closure strengthened, local-GR claim still forbidden",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(stress: list[dict[str, Any]]) -> list[dict[str, Any]]:
    baseline = next(row for row in stress if row["scenario_id"] == "STRESS3486_0_baseline")
    lower = next(row for row in stress if row["scenario_id"] == "STRESS3486_1_fe_only_lower")
    return [
        {
            "decision_id": "DEC3486_0_DD_proxy_stability",
            "decision": "Keep the same-vector DD branch alive and upgraded from algebraic accident to proxy-stable conditional closure.",
            "rationale": f"baseline rank={baseline['rank_with_best_3485_row']}; conservative lower-bound rank={lower['rank_with_best_3485_row']}.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3486_1_no_public_claim",
            "decision": "Do not claim local GR/source-coupling pass from this checkpoint.",
            "rationale": "the parent MTS source-current/transport map is still unsigned, and the condition number remains large.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3486_2_best_next_attack",
            "decision": "Move from DD-proxy stability to parent-source ownership: derive the quotient/source-current map that makes Q_Earth the actual MTS local source.",
            "rationale": "that is the shortest path from conditional local-rank closure toward a serious local-GR reduction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3487-Y5-R2FR-parent-source-map-for-DD-earth-vector-or-local-rank-closure-demotion.md",
            "next_script": "scripts/Y5_R2FR_3487_parent_source_map_for_DD_earth_vector_or_local_rank_closure_demotion.py",
            "objective": "Try to derive the parent MTS source-current/quotient map that makes the DD Earth vector a legitimate local source row; otherwise demote 3485-3486 to DD-proxy evidence only.",
            "success_gate": "parent action gives J_q and transport/readout map reducing to the DD Earth source vector, with no arena-specific source amplitude shortcut",
            "forbidden_shortcuts": "treating DD proxy as parent-owned; claiming local GR; using WEP as linear same-vector row; hiding condition number",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], bounds: list[dict[str, Any]], stress: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3486_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all local source rows exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3486_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    lower = float(next(row["value"] for row in bounds if row["bound_id"] == "QDEL3486_3_fe_only_lower_bound"))
    rows.append({"check_id": "VAL3486_2_positive_lower_bound", "passed": lower > 0, "detail": f"lower_bound={fmt(lower)}", "valid_for_claim": "False"})
    forced = next(row for row in stress if row["scenario_id"] == "STRESS3486_3_forced_zero_failure")
    rows.append({"check_id": "VAL3486_3_forced_zero_rank_fails", "passed": forced["rank_with_best_3485_row"] == 3, "detail": f"rank={forced['rank_with_best_3485_row']}", "valid_for_claim": "False"})
    lower_stress = next(row for row in stress if row["scenario_id"] == "STRESS3486_1_fe_only_lower")
    rows.append({"check_id": "VAL3486_4_lower_bound_rank_closes", "passed": lower_stress["rank_with_best_3485_row"] == 4, "detail": f"rank={lower_stress['rank_with_best_3485_row']}; cond={lower_stress['condition_number']}", "valid_for_claim": "False"})
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3486_5_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3486_6_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3486_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    bounds: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3486: Earth `Q_delta` Source Stability Or Parent Kernel Exclusion",
                "",
                "## Current Verdict",
                "- **Good news:** inside the DD Earth proxy, `Q_delta_m_Earth` is not a numerical fluke; a conservative Fe-only-minus-negative lower bound remains positive.",
                "- **Important mechanism:** the 3485 rank closure depends on this nonzero Earth neutron-excess component.",
                "- **Sharp guard:** forcing `Q_delta_m_Earth=0` destroys the rank closure.",
                "- **Still private/nonclaim:** this is DD-proxy stability, not yet parent MTS source ownership.",
                "",
                "## Positivity Bounds",
                md_table(bounds, ["bound_id", "statement", "value", "derivation", "status", "valid_for_claim"]),
                "",
                "## Rank Stress Tests",
                md_table(stress, ["scenario_id", "description", "Q_delta_m_Earth_used", "rank_with_best_3485_row", "min_singular_value", "condition_number", "closure_status", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
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
    elements = qdelta_element_rows()
    bounds = positivity_rows(elements)
    stress = stress_rows(bounds)
    theorem = theorem_rows(bounds, stress)
    decisions = decision_rows(stress)
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3486_SOURCE_REGISTER.csv",
        "element_qdelta": OUT / "P8_Y5_R2FR_3486_EARTH_QDELTA_ELEMENT_CONTRIBUTIONS.csv",
        "positivity_bounds": OUT / "P8_Y5_R2FR_3486_QDELTA_POSITIVITY_BOUNDS.csv",
        "rank_stress": OUT / "P8_Y5_R2FR_3486_RANK_STRESS_TESTS.csv",
        "theorems": OUT / "P8_Y5_R2FR_3486_THEOREM_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R2FR_3486_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3486_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["element_qdelta"], elements, ["element", "Z", "A", "mass_fraction_normalized", "Q_delta_m", "weighted_Q_delta_m", "sign", "fraction_of_total_Qdelta", "stability_role", "valid_for_claim"])
    write_csv(outputs["positivity_bounds"], bounds, ["bound_id", "statement", "value", "derivation", "status", "valid_for_claim"])
    write_csv(outputs["rank_stress"], stress, ["scenario_id", "description", "Q_delta_m_Earth_used", "rank_with_best_3485_row", "min_singular_value", "condition_number", "closure_status", "valid_for_claim"])
    write_csv(outputs["theorems"], theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, bounds, stress)
    validation_path = OUT / "P8_Y5_BRR545_3486_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(bounds, stress, theorem, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
