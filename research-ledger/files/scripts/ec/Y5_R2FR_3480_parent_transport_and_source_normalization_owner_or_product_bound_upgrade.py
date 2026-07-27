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
DOC = ROOT / "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3480": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3475": {
        "path": ROOT / "3475-Y5-R2FR-surviving-mass-electron-null-direction-theorem-or-clock-mu-row.md",
        "role": "rank-four handoff",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "full sensitivity-rank matrix",
    },
    "rank_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_RANK_LEDGER.csv",
        "role": "rank-four ledger",
    },
    "claim_gates_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_CLAIM_GATES.csv",
        "role": "no-claim gates",
    },
    "source_leg_2444": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
        "role": "source leg derivation contract",
    },
    "clock_tau_647": {
        "path": OUT / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
        "role": "clock tau product map",
    },
    "clock_readout_3136": {
        "path": OUT / "P8_Y5_R2FR_3136_CLOCK_MATTER_DERIVATION_CHAIN.csv",
        "role": "conditional clock/matter readout derivation",
    },
    "clock_source_score_3227": {
        "path": OUT / "P8_Y5_R2FR_3227_CLOCK_SOURCE_CANDIDATE_SCORECARD.csv",
        "role": "clock source candidate scorecard",
    },
    "source_norm_657": {
        "path": OUT / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
        "role": "source normalization exact decomposition",
    },
    "source_channels_657": {
        "path": OUT / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
        "role": "source normalization retained channels",
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


def matrix_rows() -> list[dict[str, str]]:
    return read_csv(SOURCES["matrix_3475"]["path"])


def matrix_values(rows: list[dict[str, str]]) -> list[list[float]]:
    return [[float(row[f"unit_{channel}"]) for channel in CHANNELS] for row in rows]


def identity(size: int) -> list[list[float]]:
    return [[1.0 if row == col else 0.0 for col in range(size)] for row in range(size)]


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left_row[k] * right[k][col] for k in range(len(right))) for col in range(len(right[0]))]
        for left_row in left
    ]


def invert(matrix: list[list[float]], tol: float = 1e-14) -> list[list[float]]:
    size = len(matrix)
    aug = [row[:] + ident[:] for row, ident in zip(matrix, identity(size))]
    for col in range(size):
        pivot = max(range(col, size), key=lambda idx: abs(aug[idx][col]))
        if abs(aug[pivot][col]) <= tol:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_value = aug[col][col]
        aug[col] = [value / pivot_value for value in aug[col]]
        for row_index in range(size):
            if row_index == col:
                continue
            factor = aug[row_index][col]
            if abs(factor) > tol:
                aug[row_index] = [
                    value - factor * pivot_entry for value, pivot_entry in zip(aug[row_index], aug[col])
                ]
    return [row[size:] for row in aug]


def determinant(matrix: list[list[float]], tol: float = 1e-14) -> float:
    mat = [row[:] for row in matrix]
    size = len(mat)
    det = 1.0
    sign = 1
    for col in range(size):
        pivot = max(range(col, size), key=lambda idx: abs(mat[idx][col]))
        if abs(mat[pivot][col]) <= tol:
            return 0.0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            sign *= -1
        pivot_value = mat[col][col]
        det *= pivot_value
        for row_index in range(col + 1, size):
            factor = mat[row_index][col] / pivot_value
            for next_col in range(col, size):
                mat[row_index][next_col] -= factor * mat[col][next_col]
    return sign * det


def max_abs_residual(left: list[list[float]], right: list[list[float]]) -> float:
    return max(abs(left[row][col] - right[row][col]) for row in range(len(left)) for col in range(len(left[0])))


def infinity_norm(matrix: list[list[float]]) -> float:
    return max(sum(abs(value) for value in row) for row in matrix)


def one_norm(matrix: list[list[float]]) -> float:
    return max(sum(abs(matrix[row][col]) for row in range(len(matrix))) for col in range(len(matrix[0])))


def inverse_rows(inverse: list[list[float]], matrix_input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    row_ids = [row["aug_row_id"] for row in matrix_input_rows]
    rows: list[dict[str, Any]] = []
    for channel_index, channel in enumerate(CHANNELS):
        row: dict[str, Any] = {
            "inverse_row_id": f"INV3480_{channel_index}_{channel}",
            "solves_for": channel,
            "formula": f"{channel} = sum_r Ainv[{channel},r] Y_r",
            "valid_for_claim": False,
        }
        for source_index, row_id in enumerate(row_ids):
            row[f"Ainv_from_{row_id}"] = f"{inverse[channel_index][source_index]:.12e}"
        row["l1_row_sum_for_bound"] = f"{sum(abs(value) for value in inverse[channel_index]):.12e}"
        rows.append(row)
    return rows


def row_bound_entries(matrix_input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for index, row in enumerate(matrix_input_rows):
        bound_text = row["bound"]
        numeric_bound: float | None = None
        try:
            numeric_bound = float(bound_text)
        except ValueError:
            numeric_bound = None
        entries.append(
            {
                "row_symbol": f"Y_{index}",
                "aug_row_id": row["aug_row_id"],
                "arena": row["arena"],
                "bound_observable": bound_text,
                "bound_units": row["bound_units"],
                "required_normalizer": f"N_{index}_{row['arena']}",
                "numeric_bound_if_scalar": "" if numeric_bound is None else f"{numeric_bound:.12e}",
                "claim_policy": "normalizer must be parent-owned before this row joins a shared coefficient bound",
                "valid_for_claim": False,
            }
        )
    return entries


def product_bound_rows(
    inverse: list[list[float]],
    matrix_input_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    entries = row_bound_entries(matrix_input_rows)
    rows: list[dict[str, Any]] = []
    for channel_index, channel in enumerate(CHANNELS):
        terms: list[str] = []
        unit_one_numeric = 0.0
        unit_one_ready = True
        for row_index, entry in enumerate(entries):
            coeff = abs(inverse[channel_index][row_index])
            terms.append(
                f"{coeff:.6e}*{entry['required_normalizer']}*B({entry['aug_row_id']})"
            )
            if entry["numeric_bound_if_scalar"]:
                unit_one_numeric += coeff * float(entry["numeric_bound_if_scalar"])
            else:
                unit_one_ready = False
        rows.append(
            {
                "bound_id": f"PB3480_{channel_index}_{channel}",
                "coefficient": channel,
                "derived_bound_formula": " + ".join(terms),
                "unit_one_smoke_value": "" if not unit_one_ready else f"{unit_one_numeric:.12e}",
                "unit_one_smoke_policy": "diagnostic only; mixed WEP/clock units make it nonclaim",
                "required_for_claim": "every N_r must be derived from the same parent source/transport map with compatible units",
                "valid_for_claim": False,
            }
        )
    return rows


def inversion_theorem_rows(
    det_value: float,
    inv_residual: float,
    norm_a_inf: float,
    norm_inv_inf: float,
    condition_inf: float,
) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "FIT3480_0_full_rank_visible_inversion",
            "statement": "For rank-four visible sensitivity matrix A, row residual vector Y determines the visible source-coefficient vector C by C=A^{-1}Y.",
            "proof": "3475 proves det(A) nonzero; finite-dimensional linear algebra gives unique inverse.",
            "numeric_evidence": f"det(A)={det_value:.12e}; max|Ainv*A-I|={inv_residual:.12e}",
            "status": "DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FIT3480_1_product_bound_envelope",
            "statement": "If |Y_r| <= N_r B_r for parent-owned row normalizers N_r, then |C_i| <= sum_r |A^{-1}_{ir}| N_r B_r.",
            "proof": "Apply triangle inequality to C_i=sum_r A^{-1}_{ir}Y_r.",
            "numeric_evidence": f"||A||_inf={norm_a_inf:.12e}; ||Ainv||_inf={norm_inv_inf:.12e}; cond_inf={condition_inf:.12e}",
            "status": "DERIVED_AS_PRODUCT_FORMULA",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FIT3480_2_no_mixed_unit_shortcut",
            "statement": "WEP eta rows, clock drift rows, and clock instability rows cannot be numerically combined until their transport normalizers put them in one parent residual unit.",
            "proof": "A^{-1}Y is meaningful only when Y components live in the same declared vector space; otherwise the inverse is rank geometry, not an empirical coefficient bound.",
            "numeric_evidence": "bound_units include dimensionless_eta, yr^-1_product_bound, and fractional_instability_product",
            "status": "GUARD_DERIVED",
            "valid_for_claim": False,
        },
    ]


def transport_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "TSO3480_0_source_current_route",
            "claim_tested": "derive one source current J_q whose projection feeds WEP/R10/clock rows",
            "formal_requirement": "J_q=delta S_matter/delta q; S_A^q=P_arena[G_q J_q]/N_A with q, G_q, P_arena, N_A parent-owned",
            "result": "EXACT_CONTRACT_NOT_FILLED",
            "why_not_claim": "2444 defines the object but lacks explicit q, parent matter action, Green/screen kernel, and normalization",
            "source_path": str(SOURCES["source_leg_2444"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "TSO3480_1_clock_transport_route",
            "claim_tested": "derive clock row normalizers from the same parent time/source transport",
            "formal_requirement": "Y_clock=N_clock P_clock[C_visible] with tau_clock_time or sigma_phi map tied to same parent residual amplitude",
            "result": "PRODUCT_ONLY",
            "why_not_claim": "647/3227 give product maps and real bounds, not standalone tau or parent amplitude",
            "source_path": str(SOURCES["clock_tau_647"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "TSO3480_2_source_normalization_route",
            "claim_tested": "derive local GR/Newton source normalization from a finite channel decomposition",
            "formal_requirement": "mu_obs=G_obs M_obs(1+c_mu); c_mu=sum_i epsilon_i with each epsilon_i zero-derived or bounded",
            "result": "DECOMPOSITION_EXACT_CHANNELS_UNFILLED",
            "why_not_claim": "657 gives exact sum rule, but all eight epsilon_i channels remain theorem/numeric inputs",
            "source_path": str(SOURCES["source_norm_657"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "TSO3480_3_conditional_parent_payoff",
            "claim_tested": "if source/clock transport is signed, 3475 becomes a real local-test coefficient bound",
            "formal_requirement": "one shared parent vector space for Y plus parent-owned N_r normalizers",
            "result": "DERIVED_PAYOFF",
            "why_not_claim": "this checkpoint proves the algebraic payoff, not the missing parent transport signatures",
            "source_path": str(SOURCES["matrix_3475"]["path"]),
            "valid_for_claim": False,
        },
    ]


def requirement_rows(matrix_input_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    entries = row_bound_entries(matrix_input_rows)
    rows: list[dict[str, Any]] = []
    for entry in entries:
        if entry["bound_units"] == "dimensionless_eta":
            missing = "source charge S_E^q, test-body transport, Earth-field normalization, no species/readout leakage"
        elif entry["bound_units"] == "yr^-1_product_bound":
            missing = "tau_clock_time, chi_X time map, clock readout normalization, parent amplitude unit"
        else:
            missing = "sigma_phi/tau conversion, stochastic-to-parent-amplitude map, clock instability transport"
        rows.append(
            {
                "requirement_id": f"REQ3480_{entry['row_symbol']}",
                "row_symbol": entry["row_symbol"],
                "arena": entry["arena"],
                "required_normalizer": entry["required_normalizer"],
                "missing_parent_inputs": missing,
                "status": "MISSING_PARENT_TRANSPORT_NORMALIZER",
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows(rank: int, inverse_residual: float, product_rows_ready: bool) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3480_0_rank_four_input",
            "requirement": "3475 matrix is rank four",
            "passed": rank == 4,
            "evidence": f"rank={rank}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3480_1_inverse_checked",
            "requirement": "A inverse reconstructs identity",
            "passed": inverse_residual < 1e-9,
            "evidence": f"max|Ainv*A-I|={inverse_residual:.12e}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3480_2_product_bound_formula",
            "requirement": "visible coefficient product-bound formula written for every channel",
            "passed": product_rows_ready,
            "evidence": "four coefficient envelopes generated",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3480_3_parent_transport_owned",
            "requirement": "all row normalizers N_r parent-owned and unit-compatible",
            "passed": False,
            "evidence": "2444/647/657 remain product/contract only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3480_4_no_claim",
            "requirement": "no local-GR/Newton/WEP/R10/clock pass claimed from mixed-unit inversion",
            "passed": True,
            "evidence": "all 3480 rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3480_0_leap_forward",
            "decision": "The local-test visible coefficient problem is now algebraically closed: C=A^{-1}Y.",
            "rationale": "3475 rank four plus 3480 inverse theorem removes the remaining source-direction degeneracy.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3480_1_real_bottleneck",
            "decision": "The remaining hard problem is not another visible sensitivity row; it is parent transport/source normalization.",
            "rationale": "without N_r, mixed WEP and clock bounds cannot be combined as a physical coefficient vector.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3480_2_best_next_attack",
            "decision": "Target one source-current theorem for J_q and one clock/source normalizer rather than adding more arena rows.",
            "rationale": "a single parent-owned transport map would upgrade the full-rank product formula into a testable local bound.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md",
            "next_script": "scripts/Y5_R2FR_3481_source_current_Jq_theorem_or_first_transport_normalizer_row.py",
            "objective": "Try to derive J_q=delta S_matter/delta q and the first parent-owned row normalizer N_r; if the theorem fails, fill one nonclaim normalizer row with explicit units.",
            "success_gate": "at least one N_r is derived or source-filled without arena-specific fitting, and the 3480 inverse envelope updates from symbolic to partially numeric product-bound form",
            "exclude": "more sensitivity rows; Github; formalization-workbench edits; setting N_r=1 by convention; claiming local GR from product rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def csv_outputs() -> dict[str, Path]:
    return {
        "source_register": OUT / "P8_Y5_R2FR_3480_SOURCE_REGISTER.csv",
        "transport_attempt": OUT / "P8_Y5_R2FR_3480_TRANSPORT_OWNER_THEOREM_ATTEMPT.csv",
        "inversion_theorem": OUT / "P8_Y5_R2FR_3480_FULL_RANK_INVERSION_THEOREM.csv",
        "inverse_matrix": OUT / "P8_Y5_R2FR_3480_SENSITIVITY_INVERSE_MATRIX.csv",
        "row_bounds": OUT / "P8_Y5_R2FR_3480_ROW_BOUND_NORMALIZER_REQUIREMENTS.csv",
        "product_bounds": OUT / "P8_Y5_R2FR_3480_PRODUCT_BOUND_ENVELOPE_NONCLAIM.csv",
        "requirements": OUT / "P8_Y5_R2FR_3480_TRANSPORT_SOURCE_REQUIREMENT_MATRIX.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3480_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3480_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3480_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3480_VALIDATION.csv",
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


def validation_rows(
    outputs: dict[str, Path],
    rows_by_output: dict[str, list[dict[str, Any]]],
    rank: int,
    determinant_value: float,
    inverse_residual: float,
) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []
    source_rows = source_register()
    validation.append(
        {
            "check_id": "VAL3480_0_sources_exist",
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
            "check_id": "VAL3480_1_csv_parse",
            "passed": parsed_ok,
            "detail": "; ".join(parse_detail),
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3480_2_rank_four_input",
            "passed": rank == 4,
            "detail": f"rank={rank}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3480_3_nonzero_determinant",
            "passed": abs(determinant_value) > 1e-12,
            "detail": f"det={determinant_value:.12e}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3480_4_inverse_identity",
            "passed": inverse_residual < 1e-9,
            "detail": f"max_residual={inverse_residual:.12e}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3480_5_product_rows",
            "passed": len(rows_by_output["product_bounds"]) == 4,
            "detail": f"product_rows={len(rows_by_output['product_bounds'])}",
            "valid_for_claim": False,
        }
    )
    all_rows: list[dict[str, Any]] = []
    for rows in rows_by_output.values():
        all_rows.extend(rows)
    no_claim = all(not parse_bool(row.get("valid_for_claim", False)) for row in all_rows)
    validation.append(
        {
            "check_id": "VAL3480_6_no_claim",
            "passed": no_claim,
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        }
    )
    no_formalization_output = all(not str(path).startswith(str(FORMALIZATION)) for path in outputs.values())
    validation.append(
        {
            "check_id": "VAL3480_7_no_formalization_outputs",
            "passed": no_formalization_output,
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": False,
        }
    )
    formalization_status = git_formalization_status()
    validation.append(
        {
            "check_id": "VAL3480_8_git_formalization_clean",
            "passed": formalization_status in {"CLEAN", "NOT_A_GIT_REPOSITORY"},
            "detail": formalization_status,
            "valid_for_claim": False,
        }
    )
    passed = all(parse_bool(row["passed"]) for row in validation)
    validation.append(
        {
            "check_id": "VAL3480_SUMMARY",
            "passed": passed,
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": False,
        }
    )
    return validation


def write_doc(rows_by_output: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 3480: Parent Transport And Source-Normalization Owner Or Product-Bound Upgrade

## Current Verdict
- **Main advance:** the 3475 full-rank sensitivity matrix gives an exact inverse: visible coefficient vector `C = A^-1 Y`.
- **Derived bound:** if row residuals satisfy `|Y_r| <= N_r B_r`, then every visible coefficient has a product-bound envelope `|C_i| <= sum_r |A^-1_ir| N_r B_r`.
- **No shortcut:** the current `Y_r` rows mix WEP eta, clock drift, and clock instability units; the `N_r` transport normalizers are still the physics throat.
- **Best next attack:** derive or source-fill the first parent-owned normalizer, starting with the source current `J_q` or the clock-time/source map.

## Transport Owner Attempt
{md_table(rows_by_output["transport_attempt"])}

## Full-Rank Inversion Theorem
{md_table(rows_by_output["inversion_theorem"])}

## Sensitivity Inverse Matrix
{md_table(rows_by_output["inverse_matrix"])}

## Row Bound Normalizer Requirements
{md_table(rows_by_output["row_bounds"])}

## Product Bound Envelope
{md_table(rows_by_output["product_bounds"])}

## Transport/Source Requirement Matrix
{md_table(rows_by_output["requirements"])}

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
    input_rows = matrix_rows()
    matrix = matrix_values(input_rows)
    rank = int(read_csv(SOURCES["rank_3475"]["path"])[0]["rank"])
    inverse = invert(matrix)
    det_value = determinant(matrix)
    identity_residual = max_abs_residual(matmul(inverse, matrix), identity(len(matrix)))
    norm_a_inf = infinity_norm(matrix)
    norm_inv_inf = infinity_norm(inverse)
    condition_inf = norm_a_inf * norm_inv_inf
    rows_by_output: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "transport_attempt": transport_attempt_rows(),
        "inversion_theorem": inversion_theorem_rows(
            det_value,
            identity_residual,
            norm_a_inf,
            norm_inv_inf,
            condition_inf,
        ),
        "inverse_matrix": inverse_rows(inverse, input_rows),
        "row_bounds": row_bound_entries(input_rows),
        "product_bounds": product_bound_rows(inverse, input_rows),
        "requirements": requirement_rows(input_rows),
        "claim_gates": claim_gate_rows(rank, identity_residual, True),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(outputs[key], rows)
    validation = validation_rows(outputs, rows_by_output, rank, det_value, identity_residual)
    rows_by_output["validation"] = validation
    write_csv(outputs["validation"], validation)
    write_doc(rows_by_output)


if __name__ == "__main__":
    main()
