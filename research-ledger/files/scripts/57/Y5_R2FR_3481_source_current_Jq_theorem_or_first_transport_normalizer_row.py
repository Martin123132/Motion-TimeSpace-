from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]
RAW_COLUMNS = ["raw_D_hatm_eff", "raw_D_delta_m_eff", "raw_D_me_eff", "raw_D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3481": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3480": {
        "path": ROOT / "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md",
        "role": "3480 handoff",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "full rank matrix with raw WEP rows",
    },
    "inverse_3480": {
        "path": OUT / "P8_Y5_R2FR_3480_SENSITIVITY_INVERSE_MATRIX.csv",
        "role": "visible coefficient inverse matrix",
    },
    "row_bounds_3480": {
        "path": OUT / "P8_Y5_R2FR_3480_ROW_BOUND_NORMALIZER_REQUIREMENTS.csv",
        "role": "row bounds and symbolic normalizers",
    },
    "product_3480": {
        "path": OUT / "P8_Y5_R2FR_3480_PRODUCT_BOUND_ENVELOPE_NONCLAIM.csv",
        "role": "symbolic product envelope",
    },
    "source_leg_2444": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
        "role": "source leg derivation contract",
    },
    "jq_attempt_2445": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv",
        "role": "J_q extraction attempt",
    },
    "jq_schema_2445": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA.csv",
        "role": "J_q certificate schema",
    },
    "eh_comparator_2446": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2446_EH_BASELINE_SOURCE_CURRENT_COMPARATOR.csv",
        "role": "EH source-current comparator",
    },
    "residual_pack_2446": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv",
        "role": "MTS residual current families",
    },
    "dd_matrix_3473": {
        "path": OUT / "P8_Y5_R2FR_3473_FULL_DD_MULTIARENA_MATRIX.csv",
        "role": "Damour-Donoghue WEP raw vectors",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": source_id,
            "source_path": str(meta["path"]),
            "exists": meta["path"].exists(),
            "role": meta["role"],
            "valid_for_claim": False,
        }
        for source_id, meta in SOURCES.items()
    ]


def raw_vector(row: dict[str, str]) -> list[float]:
    return [float(row[column]) for column in RAW_COLUMNS]


def norm(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values))


def matrix_rows() -> list[dict[str, str]]:
    return read_csv(SOURCES["matrix_3475"]["path"])


def wep_rows() -> list[dict[str, str]]:
    return [row for row in matrix_rows() if row["bound_units"] == "dimensionless_eta"]


def inverse_coefficients() -> dict[str, dict[str, float]]:
    rows = read_csv(SOURCES["inverse_3480"]["path"])
    coeffs: dict[str, dict[str, float]] = {}
    for row in rows:
        channel = row["solves_for"]
        coeffs[channel] = {}
        for key, value in row.items():
            if key.startswith("Ainv_from_"):
                coeffs[channel][key.removeprefix("Ainv_from_")] = float(value)
    return coeffs


def row_bounds() -> dict[str, dict[str, str]]:
    return {row["aug_row_id"]: row for row in read_csv(SOURCES["row_bounds_3480"]["path"])}


def jq_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "JQT3481_0_exact_variational_target",
            "claim_tested": "derive parent source current J_q from the matter action",
            "formal_statement": "J_q^A := delta S_matter,A / delta q before arena projection",
            "result": "TARGET_DEFINED_NOT_EXTRACTED",
            "advance": "fixes the object whose Earth integral would become S_E^q",
            "blocker": "no explicit parent L_matter(q,psi,e,theta) term is available",
            "source_path": str(SOURCES["jq_attempt_2445"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "JQT3481_1_GR_limit_zero_route",
            "claim_tested": "show the GR/Newton limit has no independent q-source leg",
            "formal_statement": "pure EH plus q-blind minimally-coupled matter => J_q^EH=0",
            "result": "COMPARATOR_CONFIRMED_NOT_MTS_PROOF",
            "advance": "sets the target: local GR is recovered if all residual J_q families vanish",
            "blocker": "MTS residual-current families in 2446 are not zero-derived",
            "source_path": str(SOURCES["eh_comparator_2446"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "JQT3481_2_WEP_factorization",
            "claim_tested": "extract a first transport normalizer from WEP row structure without setting source charge to unity",
            "formal_statement": "eta_AB = S_E^q (DeltaQ_AB · C); Y_AB = (DeltaQ_AB/||DeltaQ_AB||)·C; so |Y_AB| <= B_eta/(|S_E^q| ||DeltaQ_AB||)",
            "result": "PARTIAL_NORMALIZER_DERIVED",
            "advance": "N_0 and N_1 collapse to numeric row factors times one shared symbolic Earth source amplitude |S_E^q|^-1",
            "blocker": "the Earth source amplitude S_E^q itself is not parent-derived or bounded",
            "source_path": str(SOURCES["dd_matrix_3473"]["path"]),
            "valid_for_claim": False,
        },
    ]


def wep_normalizer_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(wep_rows()):
        raw = raw_vector(row)
        raw_norm = norm(raw)
        rows.append(
            {
                "normalizer_id": f"WEN3481_{index}_{row['aug_row_id']}",
                "row_symbol": f"Y_{index}",
                "aug_row_id": row["aug_row_id"],
                "arena": row["arena"],
                "raw_deltaQ_norm": f"{raw_norm:.12e}",
                "numeric_factor_per_abs_S_Eq_inv": f"{1.0 / raw_norm:.12e}",
                "derived_normalizer": f"N_{index}_{row['arena']} = |S_Eq|^-1 / ||DeltaQ_{index}||",
                "shared_symbol": "abs_S_Eq_inv",
                "derivation": "eta_AB=S_Eq*(DeltaQ_AB dot C), Y_AB=(DeltaQ_AB/||DeltaQ_AB||) dot C",
                "source_path": row["source_path"],
                "claim_status": "PARTIAL_NUMERIC_NORMALIZER_SOURCE_AMPLITUDE_RETAINED",
                "valid_for_claim": False,
            }
        )
    return rows


def collapsed_wep_bound_rows() -> list[dict[str, Any]]:
    coeffs = inverse_coefficients()
    bounds = row_bounds()
    normalizers = {row["aug_row_id"]: row for row in wep_normalizer_rows()}
    rows: list[dict[str, Any]] = []
    for channel in CHANNELS:
        wep_sum = 0.0
        term_text: list[str] = []
        for aug_row_id, normalizer in normalizers.items():
            coefficient = abs(coeffs[channel][aug_row_id])
            bound = float(bounds[aug_row_id]["numeric_bound_if_scalar"])
            row_factor = float(normalizer["numeric_factor_per_abs_S_Eq_inv"])
            contribution = coefficient * bound * row_factor
            wep_sum += contribution
            term_text.append(
                f"{coefficient:.6e}*{bound:.6e}*{row_factor:.6e}*abs_S_Eq_inv"
            )
        rows.append(
            {
                "collapsed_bound_id": f"CWB3481_{channel}",
                "coefficient": channel,
                "wep_only_bound_piece": " + ".join(term_text),
                "wep_only_numeric_prefactor_times_abs_S_Eq_inv": f"{wep_sum:.12e}",
                "meaning": f"|{channel}| receives <= {wep_sum:.12e} * |S_Eq|^-1 from the two WEP rows before clock terms",
                "claim_status": "PARTIAL_PRODUCT_BOUND_NONCLAIM_SOURCE_AMPLITUDE_RETAINED",
                "valid_for_claim": False,
            }
        )
    return rows


def updated_envelope_rows() -> list[dict[str, Any]]:
    coeffs = inverse_coefficients()
    bounds = row_bounds()
    norm_rows = {row["aug_row_id"]: row for row in wep_normalizer_rows()}
    matrix = matrix_rows()
    wep_ids = set(norm_rows)
    rows: list[dict[str, Any]] = []
    for channel in CHANNELS:
        terms: list[str] = []
        for row in matrix:
            aug_id = row["aug_row_id"]
            coefficient = abs(coeffs[channel][aug_id])
            if aug_id in wep_ids:
                bound = float(bounds[aug_id]["numeric_bound_if_scalar"])
                factor = float(norm_rows[aug_id]["numeric_factor_per_abs_S_Eq_inv"])
                terms.append(f"{coefficient * bound * factor:.12e}*abs_S_Eq_inv")
            elif bounds[aug_id]["numeric_bound_if_scalar"]:
                bound = float(bounds[aug_id]["numeric_bound_if_scalar"])
                terms.append(f"{coefficient * bound:.12e}*{bounds[aug_id]['required_normalizer']}")
            else:
                terms.append(f"{coefficient:.12e}*{bounds[aug_id]['required_normalizer']}*B({aug_id})")
        rows.append(
            {
                "envelope_id": f"UPE3481_{channel}",
                "coefficient": channel,
                "updated_product_bound": " + ".join(terms),
                "upgrade_over_3480": "WEP row normalizers replaced by row-norm factors times one shared abs_S_Eq_inv",
                "still_missing": "abs_S_Eq plus clock normalizers N_2/N_3",
                "valid_for_claim": False,
            }
        )
    return rows


def remaining_normalizer_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["row_bounds_3480"]["path"]):
        if row["bound_units"] == "dimensionless_eta":
            status = "PARTIALLY_FILLED_BY_3481_SHARED_WEP_FACTOR"
            next_input = "derive or bound abs_S_Eq from J_q/H_tau/source-current package"
        elif row["bound_units"] == "yr^-1_product_bound":
            status = "OPEN_CLOCK_DRIFT_NORMALIZER"
            next_input = "derive tau_clock_time or parent chi_X time map"
        else:
            status = "OPEN_CLOCK_INSTABILITY_NORMALIZER"
            next_input = "derive sigma_phi/tau stochastic-to-parent-amplitude map"
        rows.append(
            {
                "normalizer": row["required_normalizer"],
                "row_symbol": row["row_symbol"],
                "arena": row["arena"],
                "status_after_3481": status,
                "next_input": next_input,
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    normalizers = wep_normalizer_rows()
    collapsed = collapsed_wep_bound_rows()
    return [
        {
            "gate_id": "CG3481_0_jq_extracted",
            "requirement": "J_q extracted from explicit parent matter action",
            "passed": False,
            "evidence": "2445 still says target defined not extracted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3481_1_wep_factorization",
            "requirement": "two WEP rows factor into known DeltaQ row norms and one shared Earth source amplitude",
            "passed": len(normalizers) == 2 and all(float(row["raw_deltaQ_norm"]) > 0 for row in normalizers),
            "evidence": f"normalizer_rows={len(normalizers)}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3481_2_partial_numeric_envelope",
            "requirement": "3480 product envelope updated with numeric WEP prefactors",
            "passed": len(collapsed) == 4,
            "evidence": f"collapsed_channel_rows={len(collapsed)}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3481_3_source_amplitude_owned",
            "requirement": "|S_Eq| derived or bounded from parent current/Hamiltonian source charge",
            "passed": False,
            "evidence": "abs_S_Eq_inv retained symbolically; no unity shortcut",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3481_4_no_claim",
            "requirement": "no local-GR/WEP/R10/clock pass claimed",
            "passed": True,
            "evidence": "all 3481 rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3481_0_actual_progress",
            "decision": "Two independent WEP normalizer knobs are reduced to one shared Earth-source amplitude plus known row norms.",
            "rationale": "MICROSCOPE and Eöt-Wash rows are both Earth-field WEP rows with known DeltaQ vector norms.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3481_1_no_smuggling",
            "decision": "Do not set |S_Eq|=1; keep abs_S_Eq_inv as the source-current bottleneck.",
            "rationale": "2444/2445 make clear that source normalization must be derived from J_q or H_tau, not chosen by convention.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3481_2_best_next_attack",
            "decision": "Go after abs_S_Eq via the residual current pack, especially matter/source glue and coupling-constant families.",
            "rationale": "this is the single scalar that would turn the WEP part of the inverse envelope from symbolic to empirical.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3482-Y5-R2FR-earth-source-amplitude-SEq-current-bound-or-zero-theorem.md",
            "next_script": "scripts/Y5_R2FR_3482_earth_source_amplitude_SEq_current_bound_or_zero_theorem.py",
            "objective": "Derive or bound the shared Earth source amplitude |S_Eq| from J_q/H_tau/residual-current families; if not, create a source-ready nonclaim row for abs_S_Eq_inv.",
            "success_gate": "abs_S_Eq is zero-derived, bounded, or reduced to a smaller named residual family rather than left as a free WEP normalizer",
            "exclude": "setting S_Eq=1; adding more visible sensitivity rows; GitHub; formalization-workbench edits; local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def csv_outputs() -> dict[str, Path]:
    return {
        "source_register": OUT / "P8_Y5_R2FR_3481_SOURCE_REGISTER.csv",
        "jq_attempt": OUT / "P8_Y5_R2FR_3481_JQ_SOURCE_CURRENT_THEOREM_ATTEMPT.csv",
        "wep_normalizers": OUT / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv",
        "collapsed_wep": OUT / "P8_Y5_R2FR_3481_WEP_COLLAPSED_BOUND_FACTORS.csv",
        "updated_envelope": OUT / "P8_Y5_R2FR_3481_PRODUCT_BOUND_ENVELOPE_PARTIAL_WEP_NONCLAIM.csv",
        "remaining": OUT / "P8_Y5_R2FR_3481_REMAINING_NORMALIZER_MATRIX.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3481_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3481_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3481_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3481_VALIDATION.csv",
    }


def git_formalization_status() -> str:
    if not (FORMALIZATION / ".git").exists():
        return "NOT_A_GIT_REPOSITORY"
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "GIT_NOT_AVAILABLE"
    if result.returncode != 0:
        return f"GIT_STATUS_FAILED:{result.stderr.strip()}"
    return result.stdout.strip() or "CLEAN"


def validation_rows(outputs: dict[str, Path], rows_by_output: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []
    source_rows = source_register()
    validation.append(
        {
            "check_id": "VAL3481_0_sources_exist",
            "passed": all(parse_bool(row["exists"]) for row in source_rows),
            "detail": "all local sources exist",
            "valid_for_claim": False,
        }
    )
    parsed_ok = True
    parse_detail: list[str] = []
    for name, path in outputs.items():
        if name == "validation" and not path.exists():
            parse_detail.append("validation:pending")
            continue
        try:
            parsed = read_csv(path)
            parse_detail.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parsed_ok = False
            parse_detail.append(f"{name}:{type(exc).__name__}")
    validation.append(
        {
            "check_id": "VAL3481_1_csv_parse",
            "passed": parsed_ok,
            "detail": "; ".join(parse_detail),
            "valid_for_claim": False,
        }
    )
    normalizers = rows_by_output["wep_normalizers"]
    validation.append(
        {
            "check_id": "VAL3481_2_two_wep_normalizers",
            "passed": len(normalizers) == 2,
            "detail": f"rows={len(normalizers)}",
            "valid_for_claim": False,
        }
    )
    positive_norms = all(float(row["raw_deltaQ_norm"]) > 0 for row in normalizers)
    validation.append(
        {
            "check_id": "VAL3481_3_positive_row_norms",
            "passed": positive_norms,
            "detail": "; ".join(f"{row['aug_row_id']}={row['raw_deltaQ_norm']}" for row in normalizers),
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3481_4_collapsed_bounds",
            "passed": len(rows_by_output["collapsed_wep"]) == 4,
            "detail": f"collapsed_rows={len(rows_by_output['collapsed_wep'])}",
            "valid_for_claim": False,
        }
    )
    retained_symbol = all("abs_S_Eq_inv" in row["updated_product_bound"] for row in rows_by_output["updated_envelope"][:3])
    validation.append(
        {
            "check_id": "VAL3481_5_source_symbol_retained",
            "passed": retained_symbol,
            "detail": "abs_S_Eq_inv retained; no S_Eq=1 shortcut",
            "valid_for_claim": False,
        }
    )
    all_rows: list[dict[str, Any]] = []
    for rows in rows_by_output.values():
        all_rows.extend(rows)
    no_claim = all(not parse_bool(row.get("valid_for_claim", False)) for row in all_rows)
    validation.append(
        {
            "check_id": "VAL3481_6_no_claim",
            "passed": no_claim,
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        }
    )
    no_formalization_output = all(not str(path).startswith(str(FORMALIZATION)) for path in outputs.values())
    validation.append(
        {
            "check_id": "VAL3481_7_no_formalization_outputs",
            "passed": no_formalization_output,
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": False,
        }
    )
    formalization_status = git_formalization_status()
    validation.append(
        {
            "check_id": "VAL3481_8_git_formalization_clean",
            "passed": formalization_status in {"CLEAN", "NOT_A_GIT_REPOSITORY"},
            "detail": formalization_status,
            "valid_for_claim": False,
        }
    )
    passed = all(parse_bool(row["passed"]) for row in validation)
    validation.append(
        {
            "check_id": "VAL3481_SUMMARY",
            "passed": passed,
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": False,
        }
    )
    return validation


def write_doc(rows_by_output: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 3481: Source Current Jq Theorem Or First Transport Normalizer Row

## Current Verdict
- **Real gain:** the two WEP normalizers are no longer independent symbols. They collapse to known row-norm factors times one shared Earth source amplitude `|S_Eq|^-1`.
- **Derived relation:** `N_AB = |S_Eq|^-1 / ||DeltaQ_AB||` for Earth-field WEP rows, because `eta_AB = S_Eq (DeltaQ_AB · C)` and 3475 used unit vectors.
- **Still no claim:** `S_Eq` itself is not derived or bounded; this checkpoint refuses the forbidden shortcut `S_Eq=1`.
- **Next throat:** derive or bound `S_Eq` from `J_q`, `H_tau`, or the residual-current families.

## Jq Source Current Attempt
{md_table(rows_by_output["jq_attempt"])}

## WEP Shared Earth Normalizer Rows
{md_table(rows_by_output["wep_normalizers"])}

## WEP Collapsed Bound Factors
{md_table(rows_by_output["collapsed_wep"])}

## Updated Product Envelope
{md_table(rows_by_output["updated_envelope"])}

## Remaining Normalizer Matrix
{md_table(rows_by_output["remaining"])}

## Claim Gates
{md_table(rows_by_output["claim_gates"])}

## Decision
{md_table(rows_by_output["decision"])}

## Next Target
{md_table(rows_by_output["next"])}

## Source Register
{md_table(rows_by_output["source_register"])}

## Validation
{md_table(rows_by_output["validation"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = csv_outputs()
    rows_by_output: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "jq_attempt": jq_theorem_attempt_rows(),
        "wep_normalizers": wep_normalizer_rows(),
        "collapsed_wep": collapsed_wep_bound_rows(),
        "updated_envelope": updated_envelope_rows(),
        "remaining": remaining_normalizer_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(outputs[key], rows)
    validation = validation_rows(outputs, rows_by_output)
    rows_by_output["validation"] = validation
    write_csv(outputs["validation"], validation)
    write_doc(rows_by_output)


if __name__ == "__main__":
    main()
