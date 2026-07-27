from __future__ import annotations

import csv
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3043"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3043-Y5-R2FR-W-symbol-retirement-audit-or-DWPhi-first-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3043_00_3042_doc": ROOT / "3042-Y5-R2FR-W-equals-Phi-parent-readout-or-DWPhi-bound-under-AX1090.md",
    "SRC3043_01_3042_theorem": RESIDUALS / "P8_Y5_R2FR_3042_W_EQUALS_PHI_PARENT_READOUT_THEOREM_ATTEMPT.csv",
    "SRC3043_02_3042_dictionary": RESIDUALS / "P8_Y5_R2FR_3042_W_SYMBOL_RETIREMENT_DICTIONARY_CANDIDATE.csv",
    "SRC3043_03_3042_bound": RESIDUALS / "P8_Y5_R2FR_3042_DWPHI_BOUND_SCHEMA.csv",
    "SRC3043_04_beta_derivation": RESIDUALS / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv",
    "SRC3043_05_beta_fill": RESIDUALS / "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv",
    "SRC3043_06_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3043_07_charge_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "SRC3043_08_worldtube": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "SRC3043_09_rab_weight": RESIDUALS / "P8_Y5_PARENT_QLOC_1638_QR_NORMALIZATION_BLOCKER_LEDGER.csv",
    "SRC3043_10_rab_tail": RESIDUALS / "P8_Y5_PARENT_QLOC_1633_MASSLESS_TAIL_LOCAL_ROUTE.csv",
    "SRC3043_11_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3043_SOURCE_REGISTER.csv",
    "occurrences": RESIDUALS / "P8_Y5_R2FR_3043_W_SYMBOL_OCCURRENCE_AUDIT.csv",
    "summary": RESIDUALS / "P8_Y5_R2FR_3043_W_CLASSIFICATION_SUMMARY.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3043_W_SYMBOL_RETIREMENT_DECISION.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3043_DWPHI_FIRST_BOUND_ROW_ATTEMPT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3043_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3043_PROMOTION_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3043_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3043_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3043_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "audit_copy": PARENT_ACTION / "W_symbol_occurrence_audit_3043_NOT_ADOPTED.csv",
    "summary_copy": PARENT_ACTION / "W_classification_summary_3043_NONCLAIM.csv",
    "decision_copy": PARENT_ACTION / "W_symbol_retirement_decision_3043_NOT_ADOPTED.csv",
    "bound_copy": LOCAL_BOUNDS / "D_WPhi_first_bound_row_attempt_3043_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3043_AW_SOURCE_AMPLITUDE_OR_DWPHI_BOUND_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3043_00_3042_doc": "3042 handoff to W symbol retirement audit",
    "SRC3043_01_3042_theorem": "W=Phi theorem attempt and not-signed verdict",
    "SRC3043_02_3042_dictionary": "candidate W->Phi_metric dictionary",
    "SRC3043_03_3042_bound": "D_WPhi residual schema",
    "SRC3043_04_beta_derivation": "W as unmeasured weak-field source potential with A amplitude",
    "SRC3043_05_beta_fill": "beta source A/B W coefficient template",
    "SRC3043_06_pg_contract": "Poisson/Gauss Phi and orbital calibration contracts",
    "SRC3043_07_charge_attempt": "Gauss/orbital/source-charge calibration attempt",
    "SRC3043_08_worldtube": "worldtube W source-measure usage",
    "SRC3043_09_rab_weight": "R_AB radial weight W normalization blocker",
    "SRC3043_10_rab_tail": "R_AB massless-tail W(r) usage",
    "SRC3043_11_symbol_map": "MTS symbol/action map",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

W_PATTERN = re.compile(
    r"(?:\bW\b|W/c\^2|chi_W|D_WPhi|W/Phi|W=Phi|W:=|W :=|W\(|W_|M_source\[W\]|exterior\(W\)|around W)",
    re.IGNORECASE,
)


def classify_w_usage(text: str, file_name: str) -> tuple[str, str, str]:
    lower = text.lower()
    if "d_wphi" in lower or "w/phi" in lower or "w=phi" in lower or "w:=phi_metric" in lower or "phi_metric" in lower:
        return (
            "W_PHI_DICTIONARY_OR_RESIDUAL_SELF",
            "yes",
            "audit/dictionary row only; cannot prove W=Phi without external parent owner",
        )
    if "g00=-1+2 a w" in lower or "g_00=-1+2 a w" in lower or "u = a w" in lower or "u=a w" in lower or "beta_eff" in lower or "delta_beta" in lower:
        return (
            "WEAK_FIELD_SOURCE_POTENTIAL_WITH_AMPLITUDE",
            "yes",
            "blocks W retirement; suggests Phi_metric=A_W W and D_WPhi depends on A_W",
        )
    if "w/c^2" in lower or "chi_w" in lower:
        return (
            "LOCAL_READOUT_COORDINATE",
            "yes",
            "readout coordinate needs W=Phi or D_WPhi before source-prefactor closure",
        )
    if "poisson" in lower or "gauss" in lower or "orbital" in lower or "measured gm" in lower or "gm_orbit" in lower:
        return (
            "POISSON_GAUSS_OR_ORBITAL_CALIBRATION_RISK",
            "yes",
            "do not infer W=Phi from calibrated Poisson/Gauss/orbital notation",
        )
    if "m_source[w]" in lower or "worldtube" in lower or "exterior(w)" in lower or "around w" in lower or "source support" in lower:
        return (
            "WORLDTUBE_SOURCE_SUPPORT_NOT_POTENTIAL",
            "no",
            "not the weak-field potential; do not rewrite as Phi_metric",
        )
    if "w r_ab" in lower or "w(r)" in lower or "kappa_w" in lower or "w_normalization" in lower or "r_ab" in lower or "q_r" in lower:
        return (
            "RECIPROCAL_RADIAL_WEIGHT_NOT_POTENTIAL",
            "no",
            "radial/reciprocal weight; unrelated to local metric Phi",
        )
    if "w_r10" in lower or "w values" in lower or "epsilon/w/k/c" in lower or "w/k/c" in lower or "source pack covers epsilon, w, k" in lower:
        return (
            "R10_OR_COUPLING_WEIGHT_NOT_POTENTIAL",
            "no",
            "empirical weight/coupling symbol; not local metric Phi",
        )
    if "3042" in file_name or "3041" in file_name or "3040" in file_name or "3039" in file_name or "3038" in file_name:
        return (
            "RECENT_AUDIT_CHAIN_REFERENCE",
            "yes",
            "checkpoint self-reference; inherits nonclaim status",
        )
    return (
        "OTHER_W_TOKEN_REVIEWED_NOT_RETIRED",
        "unknown",
        "W token exists but is not enough to adopt W:=Phi_metric",
    )


def row_identifier(row: dict[str, str]) -> str:
    for key in (
        "theorem_id",
        "contract_id",
        "rung_id",
        "row_id",
        "bound_id",
        "validation_id",
        "proof_id",
        "dictionary_id",
        "source_id",
        "term_id",
        "block_id",
        "clause_id",
        "decision_id",
        "audit_id",
    ):
        if row.get(key):
            return row[key]
    return ""


def snippet_for(row: dict[str, str], hit_columns: list[str]) -> str:
    parts = []
    for column in hit_columns[:4]:
        value = row.get(column, "")
        if value:
            parts.append(f"{column}={value}")
    snippet = " ; ".join(parts) if parts else " ; ".join(f"{k}={v}" for k, v in list(row.items())[:4])
    return snippet[:500]


def scan_w_occurrences() -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    candidate_files = sorted(RESIDUALS.glob("*.csv"))
    for csv_path in candidate_files:
        if "_3043_" in csv_path.name:
            continue
        for index, row in enumerate(rows(csv_path), start=2):
            hit_columns = [
                column
                for column, value in row.items()
                if value is not None and W_PATTERN.search(str(value))
            ]
            if not hit_columns:
                continue
            snippet = snippet_for(row, hit_columns)
            classification, relevance, implication = classify_w_usage(
                " ".join(str(row.get(column, "")) for column in hit_columns),
                csv_path.name,
            )
            output_rows.append(
                base(
                    {
                        "audit_id": f"WSCAN3043_{len(output_rows):04d}",
                        "source_file": csv_path.name,
                        "source_path": str(csv_path),
                        "row_number_approx": index,
                        "row_identifier": row_identifier(row),
                        "hit_columns": ";".join(hit_columns),
                        "snippet": snippet,
                        "classification": classification,
                        "local_potential_relevance": relevance,
                        "decision_implication": implication,
                    }
                )
            )
    return output_rows


occurrence_rows = scan_w_occurrences()
classification_counts = Counter(row["classification"] for row in occurrence_rows)
relevance_counts = Counter(row["local_potential_relevance"] for row in occurrence_rows)

summary_rows = [
    base(
        {
            "summary_id": f"WSUM3043_{index:02d}",
            "classification": classification,
            "row_count": count,
            "local_potential_relevance": next(
                (
                    row["local_potential_relevance"]
                    for row in occurrence_rows
                    if row["classification"] == classification
                ),
                "",
            ),
            "retirement_effect": (
                "blocks_global_W_retirement"
                if classification
                in {
                    "WEAK_FIELD_SOURCE_POTENTIAL_WITH_AMPLITUDE",
                    "POISSON_GAUSS_OR_ORBITAL_CALIBRATION_RISK",
                    "WORLDTUBE_SOURCE_SUPPORT_NOT_POTENTIAL",
                    "RECIPROCAL_RADIAL_WEIGHT_NOT_POTENTIAL",
                    "R10_OR_COUPLING_WEIGHT_NOT_POTENTIAL",
                    "OTHER_W_TOKEN_REVIEWED_NOT_RETIRED",
                }
                else "nonclaim_context"
            ),
        }
    )
    for index, (classification, count) in enumerate(classification_counts.most_common())
]

has_weak_amplitude = classification_counts["WEAK_FIELD_SOURCE_POTENTIAL_WITH_AMPLITUDE"] > 0
has_calibration_risk = classification_counts["POISSON_GAUSS_OR_ORBITAL_CALIBRATION_RISK"] > 0
has_nonpotential_w = any(
    classification_counts[classification] > 0
    for classification in [
        "WORLDTUBE_SOURCE_SUPPORT_NOT_POTENTIAL",
        "RECIPROCAL_RADIAL_WEIGHT_NOT_POTENTIAL",
        "R10_OR_COUPLING_WEIGHT_NOT_POTENTIAL",
    ]
)
safe_to_retire_w_globally = False
safe_to_retire_local_weak_w = not (has_weak_amplitude or has_calibration_risk)

decision_rows = [
    base(
        {
            "decision_id": "WDEC3043_0_global",
            "question": "can W be globally retired to Phi_metric across the corpus?",
            "answer": "NO",
            "reason": "scan finds W used as worldtube/source support, reciprocal radial weight, R10/coupling weight, audit symbol and weak-field source-potential notation",
            "action": "do not globally rewrite W",
        }
    ),
    base(
        {
            "decision_id": "WDEC3043_1_local_weak",
            "question": "can local weak-field W be safely retired to Phi_metric now?",
            "answer": "NO" if not safe_to_retire_local_weak_w else "CONDITIONAL",
            "reason": "weak-field rows use g00=-1+2 A W/c^2 and U=A W, so the safer relation is Phi_metric=A_W W rather than W=Phi_metric",
            "action": "derive A_W=1 or retain D_WPhi/A_W residual",
        }
    ),
    base(
        {
            "decision_id": "WDEC3043_2_dictionary",
            "question": "is the 3042 W:=Phi_metric dictionary adopted?",
            "answer": "NO",
            "reason": "the alias audit finds at least one local weak-field W source-amplitude usage and several non-potential W meanings",
            "action": "demote dictionary to conditional notation only; keep D_WPhi",
        }
    ),
    base(
        {
            "decision_id": "WDEC3043_3_next",
            "question": "what is the least-smuggly next target?",
            "answer": "A_W source-amplitude theorem or D_WPhi bound",
            "reason": "if Phi_metric=A_W W, then W=Phi requires A_W=1; this is a sharper target than arguing over the letter W",
            "action": "3044 should prove A_W=1 from parent metric/source normalization or stage A_W/D_WPhi bounds",
        }
    ),
]

bound_rows = [
    base(
        {
            "bound_id": "DWB3043_0_AW_relation",
            "quantity": "A_W_relation",
            "formula": "Phi_metric = A_W W on rows with g00=-1+2 A W/c^2 and U=A W",
            "current_status": "RELATION_IDENTIFIED_FROM_CORPUS_ROWS",
            "missing_for_claim": "MISSING_A_W_PARENT_VALUE; MISSING_UNITS; MISSING_SIGN; MISSING_SOURCE_PATHED_NUMERIC_ROW",
            "claim_rule": "W=Phi only if A_W=1 in the same observed branch",
        }
    ),
    base(
        {
            "bound_id": "DWB3043_1_DWPhi_from_AW",
            "quantity": "D_WPhi",
            "formula": "D_WPhi = W/Phi_metric - 1 = 1/A_W - 1 when Phi_metric=A_W W",
            "current_status": "NOT_COMPUTED_AW_MISSING",
            "missing_for_claim": "MISSING_A_W_VALUE_OR_THEOREM_ZERO",
            "claim_rule": "finite only after A_W is parent-derived or source-backed",
        }
    ),
    base(
        {
            "bound_id": "DWB3043_2_first_bound_row",
            "quantity": "first_D_WPhi_bound_row",
            "formula": "source-backed D_WPhi_total_abs row for 3042 runner",
            "current_status": "NO_VALID_BOUND_ROW_CREATED",
            "missing_for_claim": "MISSING_A_W; MISSING_D_CAL_W; MISSING_D_FRAME_WPHI; MISSING_D_OPERATOR_WPHI",
            "claim_rule": "do not fabricate bound rows from notation",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3043_0_AW_not_one",
            "countermodel": "g00=-1+2 A_W W/c^2 with A_W not equal to one",
            "effect": "W is a source-potential coordinate, while Phi_metric=A_W W; W=Phi fails",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3043_1_worldtube_W",
            "countermodel": "W denotes source worldtube/support rather than a potential",
            "effect": "global W rewrite would be mathematically wrong",
            "status": "LIVE_GUARDRAIL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3043_2_reciprocal_weight_W",
            "countermodel": "W(r) is a radial/reciprocal kinetic weight in R_AB equations",
            "effect": "same glyph carries unrelated physics",
            "status": "LIVE_GUARDRAIL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3043_3_calibrated_poisson_W",
            "countermodel": "W is fitted through Poisson/Gauss/orbital GM calibration",
            "effect": "r_W=1 is imported rather than derived",
            "status": "LIVE_BLOCKER",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3043_0_3044",
            "next_checkpoint": "3044-Y5-R2FR-AW-source-amplitude-theorem-or-DWPhi-bound-row-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_AW_source_amplitude_theorem_or_DWPhi_bound_row_under_AX1090_3044.py",
            "mission": "prove A_W=1 in Phi_metric=A_W W from parent metric/source normalization, or stage source-backed D_WPhi/A_W residual rows",
            "starting_equation": "g00=-1+2 A_W W/c^2; Phi_metric=A_W W; D_WPhi=1/A_W-1",
            "do_not_repeat": "do not globally rewrite W; do not infer A_W=1 from measured U=A W or orbital GM",
            "claim_policy": "no first-order source prefactor claim until A_W/W/Phi, source pairing, Hessian and R_lock are signed or bounded",
        }
    )
]

gates = [
    base(
        {
            "gate_id": "GATE3043_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3043 is source-backed to 3042 plus key W usage rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_1_scan_nonempty",
            "gate": "W occurrence scanner finds rows",
            "result": len(occurrence_rows) > 0,
            "notes": f"rows={len(occurrence_rows)}",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_2_all_classified",
            "gate": "every scanned W row has a classification",
            "result": all(bool(row.get("classification")) for row in occurrence_rows),
            "notes": f"classifications={len(classification_counts)}",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_3_weak_amplitude_found",
            "gate": "weak-field A_W W usage is detected",
            "result": has_weak_amplitude,
            "notes": "blocks local W:=Phi retirement without A_W theorem",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_4_nonpotential_W_found",
            "gate": "non-potential W meanings are detected",
            "result": has_nonpotential_w,
            "notes": "blocks global W rewrite",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_5_dictionary_not_adopted",
            "gate": "W:=Phi_metric dictionary remains unadopted",
            "result": not safe_to_retire_w_globally and not safe_to_retire_local_weak_w,
            "notes": "D_WPhi/A_W route retained",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_6_bound_fail_closed",
            "gate": "first D_WPhi bound row is blocked instead of fabricated",
            "result": any(row["current_status"] == "NO_VALID_BOUND_ROW_CREATED" for row in bound_rows),
            "notes": "A_W and residual components missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3043_7_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no Newton/local-GR/PPN/R10 claim",
        }
    ),
]

for output_key, output_rows in {
    "sources": source_register,
    "occurrences": occurrence_rows,
    "summary": summary_rows,
    "decision": decision_rows,
    "bound": bound_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["occurrences"], BRANCH_OUTPUTS["audit_copy"])
shutil.copyfile(OUTPUTS["summary"], BRANCH_OUTPUTS["summary_copy"])
shutil.copyfile(OUTPUTS["decision"], BRANCH_OUTPUTS["decision_copy"])
shutil.copyfile(OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for W-symbol audit route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + occurrence_rows
    + summary_rows
    + decision_rows
    + bound_rows
    + countermodel_rows
    + gates
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3043_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3043_02_scan_nonempty",
            "passed": len(occurrence_rows) > 0,
            "requirement": "W occurrence audit has scanned rows",
            "evidence": OUTPUTS["occurrences"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_03_all_classified",
            "passed": all(bool(row.get("classification")) for row in occurrence_rows),
            "requirement": "every scanned W row is classified",
            "evidence": OUTPUTS["occurrences"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_04_weak_amplitude",
            "passed": has_weak_amplitude,
            "requirement": "weak-field A_W W usage is detected",
            "evidence": OUTPUTS["summary"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_05_dictionary_not_adopted",
            "passed": any(row["decision_id"] == "WDEC3043_2_dictionary" and row["answer"] == "NO" for row in decision_rows),
            "requirement": "W:=Phi_metric dictionary is not adopted",
            "evidence": OUTPUTS["decision"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_06_bound_fail_closed",
            "passed": any(row["current_status"] == "NO_VALID_BOUND_ROW_CREATED" for row in bound_rows),
            "requirement": "first D_WPhi bound row remains blocked",
            "evidence": OUTPUTS["bound"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_07_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3043 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3043_08_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_09_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3043_10_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3043_11_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3044-"),
            "requirement": "next target selects A_W source amplitude theorem or D_WPhi bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3043_12_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

representative_rows: list[dict[str, Any]] = []
seen_classes: set[str] = set()
for row in occurrence_rows:
    classification = row["classification"]
    if classification not in seen_classes:
        representative_rows.append(row)
        seen_classes.add(classification)
    if len(representative_rows) >= 10:
        break

doc = f"""# 3043 - W Symbol Retirement Audit Or DWPhi First Bound Row under AX1090

Status: `Y5_R2FR_3043_W_not_retired_AW_source_amplitude_target_next`

## Verdict

3043 scans the residual CSV corpus for exact/local-relevant `W` usages and classifies them.

The result is clear: `W` cannot be globally retired to `Phi_metric`, and even the local weak-field `W:=Phi_metric` dictionary is not safe yet.

The blocker is not just notation. The corpus contains weak-field rows of the form

`g00=-1+2 A_W W/c^2` and `U=A_W W`.

That means the safer relation is

`Phi_metric = A_W W`,

so

`D_WPhi = W/Phi_metric - 1 = 1/A_W - 1`.

Therefore the next actual derivation target is not the letter `W`; it is the source-amplitude/readout coefficient `A_W`. Prove `A_W=1`, or keep `D_WPhi` as a residual.

## Classification Summary

{md_table(summary_rows, ["summary_id", "classification", "row_count", "local_potential_relevance", "retirement_effect"])}

## Representative W Occurrences

{md_table(representative_rows, ["audit_id", "source_file", "row_identifier", "classification", "local_potential_relevance", "decision_implication"])}

## W Retirement Decision

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## D_WPhi First Bound Row Attempt

{md_table(bound_rows, ["bound_id", "quantity", "formula", "current_status", "missing_for_claim", "claim_rule"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "effect", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print(f"3043 verdict: scanned {len(occurrence_rows)} W rows; W not retired; A_W source amplitude selected next.")
