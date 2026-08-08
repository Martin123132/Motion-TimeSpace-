from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
EXTERNAL = ROOT / "source-intake" / "external_sources"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3475-Y5-R2FR-surviving-mass-electron-null-direction-theorem-or-clock-mu-row.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

NPL_SOURCE_URL = "https://eprintspublications.npl.co.uk/9887/1/eid9887.pdf"
NPL_SOURCE_LOCAL = EXTERNAL / "Sherrill_2023_NJP_atomic_clock_variations_alpha_mu.pdf"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3475": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3474": {
        "path": ROOT / "3474-Y5-R2FR-nullspace-killing-source-owner-contract-or-clock-R10-row.md",
        "role": "3474 handoff",
    },
    "matrix_3474": {
        "path": OUT / "P8_Y5_R2FR_3474_AUGMENTED_WEP_CLOCK_MATRIX.csv",
        "role": "rank-three WEP plus alpha-clock matrix",
    },
    "nullspace_3474": {
        "path": OUT / "P8_Y5_R2FR_3474_AUGMENTED_NULLSPACE_BASIS.csv",
        "role": "surviving mass/electron null direction",
    },
    "rank_3474": {
        "path": OUT / "P8_Y5_R2FR_3474_AUGMENTED_RANK_LEDGER.csv",
        "role": "previous rank ledger",
    },
    "mass_theorem_2442": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2442_MASS_ZERO_THEOREM_ATTEMPT.csv",
        "role": "conditional matter-spectrum zero theorem",
    },
    "matter_owner_2442": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2442_MATTER_SPECTRUM_OWNER_AUDIT.csv",
        "role": "matter spectrum owner audit",
    },
    "matter_signature_2443": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2443_PARENT_MATTER_SPECTRUM_SIGNATURE_AUDIT.csv",
        "role": "parent matter-spectrum signature audit",
    },
    "constant_audit_1921": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1921_CONSTANT_SUPERSELECTION_PROOF_AUDIT.csv",
        "role": "constant-sector no-unit-cheat audit",
    },
    "clock_alpha_646": {
        "path": OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "role": "previous alpha clock source",
    },
    "clock_bound_647": {
        "path": OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
        "role": "previous alpha clock product bounds",
    },
    "npl_sr_cs_pdf": {
        "path": NPL_SOURCE_LOCAL,
        "role": "Sr/Cs alpha and proton-electron mass-ratio sensitivity source",
        "source_url": NPL_SOURCE_URL,
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


def normalize(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values))
    if norm <= 0:
        raise ValueError("cannot normalize zero vector")
    return [value / norm for value in values]


def rref(matrix: list[list[float]], tol: float = 1e-12) -> tuple[list[list[float]], list[int]]:
    mat = [row[:] for row in matrix]
    row_count = len(mat)
    col_count = len(mat[0])
    pivots: list[int] = []
    row_index = 0
    for col in range(col_count):
        if row_index >= row_count:
            break
        pivot = max(range(row_index, row_count), key=lambda idx: abs(mat[idx][col]))
        if abs(mat[pivot][col]) <= tol:
            continue
        mat[row_index], mat[pivot] = mat[pivot], mat[row_index]
        pivot_value = mat[row_index][col]
        mat[row_index] = [value / pivot_value for value in mat[row_index]]
        for idx in range(row_count):
            if idx == row_index:
                continue
            factor = mat[idx][col]
            if abs(factor) > tol:
                mat[idx] = [value - factor * pivot_entry for value, pivot_entry in zip(mat[idx], mat[row_index])]
        pivots.append(col)
        row_index += 1
    return mat, pivots


def matrix_rank(matrix: list[list[float]], tol: float = 1e-12) -> int:
    _, pivots = rref(matrix, tol)
    return len(pivots)


def nullspace_basis(matrix: list[list[float]], tol: float = 1e-12) -> list[list[float]]:
    reduced, pivots = rref(matrix, tol)
    col_count = len(matrix[0])
    free_cols = [col for col in range(col_count) if col not in pivots]
    basis: list[list[float]] = []
    for free_col in free_cols:
        vector = [0.0] * col_count
        vector[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row_index][free_col]
        basis.append(normalize(vector))
    return basis


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        rows.append(
            {
                "timestamp_utc": stamp,
                "source_id": source_id,
                "source_path": str(meta["path"]),
                "exists": meta["path"].exists(),
                "source_url": meta.get("source_url", ""),
                "role": meta["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def previous_matrix_rows() -> list[dict[str, Any]]:
    return [dict(row) for row in read_csv(SOURCES["matrix_3474"]["path"])]


def previous_matrix_values(rows: list[dict[str, Any]]) -> list[list[float]]:
    return [[float(row[f"unit_{channel}"]) for channel in CHANNELS] for row in rows]


def previous_null_vector() -> list[float]:
    rows = read_csv(SOURCES["nullspace_3474"]["path"])
    if len(rows) != 1:
        raise ValueError(f"expected exactly one 3474 null vector, found {len(rows)}")
    row = rows[0]
    return [float(row[channel]) for channel in CHANNELS]


def theorem_attempt_rows(survivor: list[float]) -> list[dict[str, Any]]:
    survivor_law = (
        f"N_surv = {survivor[1]:.12e} D_delta_m_eff + "
        f"{survivor[2]:.12e} D_me_eff"
    )
    return [
        {
            "attempt_id": "MRO3475_0_exact_conditional_owner",
            "route": "derive_zero",
            "claim_tested": "mass and electron-ratio vertical derivatives vanish if visible matter constants descend from the quotient or are superselected",
            "mathematical_form": "theta_vis=theta_bar(q(Phi),Rep) and v in ker(Dq) => Lie_v ln theta_vis=0",
            "result": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "survivor_law": survivor_law,
            "blocker": "parent action still permits hidden mass/Yukawa/QCD/binding coefficient functions",
            "source_path": str(SOURCES["mass_theorem_2442"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRO3475_1_survivor_zero_contract",
            "route": "derive_zero",
            "claim_tested": "remaining null direction is killed by D_me_eff=0 and D_delta_m_eff=0, or by the exact survivor linear relation",
            "mathematical_form": survivor_law + " = 0",
            "result": "CONTRACT_READY",
            "survivor_law": survivor_law,
            "blocker": "no parent-owned matter-spectrum signature proves either component or the linear combination zero",
            "source_path": str(SOURCES["matter_signature_2443"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRO3475_2_countervertex_guard",
            "route": "reject_shortcut",
            "claim_tested": "mass-sector silence can be asserted without forbidding extra hidden-visible coefficient morphisms",
            "mathematical_form": "DeltaS contains m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), or B_A(Xhat) countervertices",
            "result": "REJECTED_FOR_NOW",
            "survivor_law": survivor_law,
            "blocker": "countervertices are legal unless the parent operator grammar forbids them",
            "source_path": str(SOURCES["matter_owner_2442"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MRO3475_3_empirical_sensitivity_route",
            "route": "source_row",
            "claim_tested": "a sourced Sr/Cs mass-ratio clock sensitivity row has nonzero projection on the surviving null direction",
            "mathematical_form": "(delta r/r)_Sr/Cs = -(2.77 d_gamma + (d_me-d_g) + 0.07(d_q-d_g)) (kappa phi)^n",
            "result": "PROCEED_TO_RANK_TEST",
            "survivor_law": survivor_law,
            "blocker": "this is sensitivity rank only; standalone MTS coefficient and transport/time map remain absent",
            "source_path": str(NPL_SOURCE_LOCAL),
            "valid_for_claim": False,
        },
    ]


def sr_cs_source_rows() -> tuple[list[dict[str, Any]], list[float]]:
    raw_vector = [-0.07, 0.0, -1.0, -2.77]
    unit_vector = normalize(raw_vector)
    rows = [
        {
            "clock_row_id": "CLK3475_0_SrCs_mu_q_alpha",
            "arena": "CLOCK_SrCs_MASS_RATIO_INSTABILITY",
            "clock_pair": "87Sr optical clock / 133Cs microwave fountain",
            "observable": "fractional frequency ratio perturbation",
            "published_formula": "(delta r/r)_Sr/Cs = -(2.77 d_gamma + (d_me-d_g) + 0.07(d_q-d_g)) (kappa phi)^n",
            "D_hatm_eff_mapping": "d_q-d_g mapped as mean-light-quark/QCD sensitivity proxy, not D_delta_m",
            "raw_D_hatm_eff": f"{raw_vector[0]:.12e}",
            "raw_D_delta_m_eff": f"{raw_vector[1]:.12e}",
            "raw_D_me_eff": f"{raw_vector[2]:.12e}",
            "raw_D_e_eff": f"{raw_vector[3]:.12e}",
            "unit_D_hatm_eff": f"{unit_vector[0]:.12e}",
            "unit_D_delta_m_eff": f"{unit_vector[1]:.12e}",
            "unit_D_me_eff": f"{unit_vector[2]:.12e}",
            "unit_D_e_eff": f"{unit_vector[3]:.12e}",
            "bound_expression": "kappa_n |d_Sr/Cs^(n)| sigma_phi_n(tau) <= 1.6e-13/sqrt(tau/s)",
            "bound_timescale": "600 s <= tau <= 80000 s",
            "bound_policy": "published instability product only; no standalone MTS D_me/D_hatm coefficient without clock transport and source normalization",
            "source_path": str(NPL_SOURCE_LOCAL),
            "source_url": NPL_SOURCE_URL,
            "source_page": "paper page 11 / PDF page 12; equations 16-22",
            "source_confidence": "source_backed_published_clock_sensitivity",
            "rank_use": "sensitivity_vector_only",
            "valid_for_claim": False,
        }
    ]
    return rows, raw_vector


def augmented_rows(previous_rows: list[dict[str, Any]], sr_cs_vector: list[float]) -> list[dict[str, Any]]:
    rows = [dict(row) for row in previous_rows]
    unit = normalize(sr_cs_vector)
    rows.append(
        {
            "aug_row_id": "MATRIX3475_3_CLOCK_SrCs_mu_q_alpha",
            "arena": "CLOCK_SrCs_MASS_RATIO_INSTABILITY",
            "row_type": "clock_mu_q_alpha_sensitivity",
            "raw_D_hatm_eff": f"{sr_cs_vector[0]:.12e}",
            "raw_D_delta_m_eff": f"{sr_cs_vector[1]:.12e}",
            "raw_D_me_eff": f"{sr_cs_vector[2]:.12e}",
            "raw_D_e_eff": f"{sr_cs_vector[3]:.12e}",
            "unit_D_hatm_eff": f"{unit[0]:.12e}",
            "unit_D_delta_m_eff": f"{unit[1]:.12e}",
            "unit_D_me_eff": f"{unit[2]:.12e}",
            "unit_D_e_eff": f"{unit[3]:.12e}",
            "bound": "1.6e-13/sqrt(tau/s)",
            "bound_units": "fractional_instability_product",
            "source_path": str(NPL_SOURCE_LOCAL),
            "valid_for_claim": False,
        }
    )
    return rows


def rank_ledger_rows(previous_rank: int, previous_null_dim: int, matrix: list[list[float]]) -> tuple[list[dict[str, Any]], list[list[float]]]:
    rank = matrix_rank(matrix)
    basis = nullspace_basis(matrix)
    rows = [
        {
            "rank_id": "RANK3475_0_WEP_alpha_clock_plus_SrCs_mu",
            "rows": len(matrix),
            "columns": len(CHANNELS),
            "rank": rank,
            "nullspace_dimension": len(basis),
            "previous_rank": previous_rank,
            "previous_nullspace_dimension": previous_null_dim,
            "rank_gain": rank - previous_rank,
            "status": "FULL_SENSITIVITY_RANK_CONDITIONAL_NO_CLAIM" if rank == len(CHANNELS) else "NULL_DIRECTION_REMAINS",
            "valid_for_claim": False,
        }
    ]
    return rows, basis


def nullspace_rows(basis: list[list[float]]) -> list[dict[str, Any]]:
    if not basis:
        return [
            {
                "basis_id": "NULL3475_NONE",
                "D_hatm_eff": "0.000000000000e+00",
                "D_delta_m_eff": "0.000000000000e+00",
                "D_me_eff": "0.000000000000e+00",
                "D_e_eff": "0.000000000000e+00",
                "check": "rank-four sensitivity matrix has no algebraic null direction",
                "status": "NO_NULLSPACE_REMAINS_CONDITIONALLY",
                "valid_for_claim": False,
            }
        ]
    rows: list[dict[str, Any]] = []
    for index, vector in enumerate(basis):
        rows.append(
            {
                "basis_id": f"NULL3475_{index}",
                "D_hatm_eff": f"{vector[0]:.12e}",
                "D_delta_m_eff": f"{vector[1]:.12e}",
                "D_me_eff": f"{vector[2]:.12e}",
                "D_e_eff": f"{vector[3]:.12e}",
                "check": "augmented_matrix*v approximately zero",
                "status": "SURVIVING_UNCONSTRAINED_SOURCE_DIRECTION",
                "valid_for_claim": False,
            }
        )
    return rows


def impact_rows(survivor: list[float], sr_cs_vector: list[float]) -> list[dict[str, Any]]:
    unit = normalize(sr_cs_vector)
    dot_raw = dot(sr_cs_vector, survivor)
    dot_unit = dot(unit, survivor)
    return [
        {
            "impact_id": "IMPACT3475_0_survivor_vs_SrCs",
            "previous_basis_id": "NULL3474_0",
            "raw_row_dot_previous_null": f"{dot_raw:.12e}",
            "unit_row_dot_previous_null": f"{dot_unit:.12e}",
            "abs_unit_dot": f"{abs(dot_unit):.12e}",
            "effect": "KILLED_BY_MASS_RATIO_CLOCK_ROW" if abs(dot_unit) > 1e-10 else "SURVIVES",
            "reason": "Sr/Cs row has direct D_me support; survivor is dominated by D_me_eff",
            "valid_for_claim": False,
        }
    ]


def claim_gates(rank: int, null_dim: int, impact: list[dict[str, Any]]) -> list[dict[str, Any]]:
    killed = impact[0]["effect"] == "KILLED_BY_MASS_RATIO_CLOCK_ROW"
    return [
        {
            "gate_id": "CG3475_0_parent_mass_theorem",
            "requirement": "parent matter-spectrum owner signs D_me/D_delta or survivor linear combination zero",
            "passed": False,
            "evidence": "2442/2443 prove only an exact conditional; countervertices remain legal",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3475_1_mu_row_source_backed",
            "requirement": "Sr/Cs mass-ratio sensitivity row has a real published source and local source file",
            "passed": NPL_SOURCE_LOCAL.exists(),
            "evidence": str(NPL_SOURCE_LOCAL),
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3475_2_survivor_killed",
            "requirement": "new row has nonzero projection on NULL3474_0",
            "passed": killed,
            "evidence": f"abs_unit_dot={impact[0]['abs_unit_dot']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3475_3_full_sensitivity_rank",
            "requirement": "WEP+alpha-clock+Sr/Cs sensitivity matrix reaches rank 4",
            "passed": rank == 4 and null_dim == 0,
            "evidence": f"rank={rank}; nullspace_dimension={null_dim}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3475_4_no_standalone_bound_shortcut",
            "requirement": "do not convert clock instability product into standalone local-GR/WEP coefficient",
            "passed": True,
            "evidence": "clock transport, source normalization, and MTS field-time map remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3475_5_no_claim",
            "requirement": "no local-GR, WEP, R10, clock, or orbital pass claimed",
            "passed": True,
            "evidence": "all 3475 rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows(rank: int, null_dim: int) -> list[dict[str, Any]]:
    if rank == 4 and null_dim == 0:
        decision = "The algebraic source-direction hole is closed at sensitivity-rank level."
        next_target = "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md"
    else:
        decision = "A source direction remains; seek a second mass/nuclear sensitivity row or stronger theorem."
        next_target = "3476-Y5-R2FR-second-mass-nuclear-sensitivity-row-or-parent-zero-retry.md"
    return [
        {
            "decision_id": "DEC3475_0_best_result",
            "decision": decision,
            "rationale": "Sr/Cs has direct D_me sensitivity and nonzero projection on NULL3474_0.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3475_1_remaining_missing",
            "decision": "The missing object has changed from an algebraic null direction to a transport/source-normalization proof.",
            "rationale": "full sensitivity rank does not by itself provide MTS coefficient values, tau_clock map, source leg, or local field amplitude.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3475_2_next_target",
            "decision": next_target,
            "rationale": "next step should bind the rank-complete visible source vector to one parent transport/source amplitude rather than adding more ledgers.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md",
            "next_script": "scripts/Y5_R2FR_3480_parent_transport_and_source_normalization_owner_or_product_bound_upgrade.py",
            "objective": "Turn full visible sensitivity rank into a real MTS local test by deriving one parent transport/source-normalization map or producing product-bound rows that keep all coefficients nonclaim.",
            "success_gate": "one shared source vector S_X and clock/WEP transport map links D_hatm,D_delta,D_me,D_e to the parent residual without arena-specific fitting",
            "exclude": "GitHub action; formalization-workbench edits; standalone coefficient claims from clock rows; treating d_q proxy as D_delta_m without a separate source",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def csv_outputs() -> dict[str, Path]:
    return {
        "source_register": OUT / "P8_Y5_R2FR_3475_SOURCE_REGISTER.csv",
        "theorem_attempt": OUT / "P8_Y5_R2FR_3475_MASS_RATIO_OWNER_THEOREM_ATTEMPT.csv",
        "mu_source": OUT / "P8_Y5_R2FR_3475_CLOCK_MU_SENSITIVITY_SOURCE.csv",
        "matrix": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "rank": OUT / "P8_Y5_R2FR_3475_RANK_LEDGER.csv",
        "nullspace": OUT / "P8_Y5_R2FR_3475_NULLSPACE_BASIS.csv",
        "impact": OUT / "P8_Y5_R2FR_3475_PREVIOUS_NULL_DIRECTION_IMPACT.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3475_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3475_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3475_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3475_VALIDATION.csv",
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
    matrix: list[list[float]],
    rank: int,
    null_dim: int,
    impact: list[dict[str, Any]],
    rows_by_output: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []
    source_rows = source_register()
    validation.append(
        {
            "check_id": "VAL3475_0_sources_exist",
            "passed": all(parse_bool(row["exists"]) for row in source_rows),
            "detail": "all local sources exist",
            "valid_for_claim": False,
        }
    )
    parsed_ok = True
    parse_detail = []
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
            "check_id": "VAL3475_1_csv_parse",
            "passed": parsed_ok,
            "detail": "; ".join(parse_detail),
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3475_2_augmented_shape",
            "passed": len(matrix) == 4 and len(matrix[0]) == 4,
            "detail": f"rows={len(matrix)}; cols={len(matrix[0])}",
            "valid_for_claim": False,
        }
    )
    finite = all(math.isfinite(value) for row in matrix for value in row)
    validation.append(
        {
            "check_id": "VAL3475_3_augmented_finite",
            "passed": finite,
            "detail": "all normalized matrix entries finite",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3475_4_rank_four",
            "passed": rank == 4,
            "detail": f"rank={rank}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3475_5_nullspace_dim_zero",
            "passed": null_dim == 0,
            "detail": f"dim={null_dim}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3475_6_kills_previous_survivor",
            "passed": impact[0]["effect"] == "KILLED_BY_MASS_RATIO_CLOCK_ROW",
            "detail": f"abs_unit_dot={impact[0]['abs_unit_dot']}",
            "valid_for_claim": False,
        }
    )
    all_rows: list[dict[str, Any]] = []
    for rows in rows_by_output.values():
        all_rows.extend(rows)
    no_claim = all(not parse_bool(row.get("valid_for_claim", False)) for row in all_rows)
    validation.append(
        {
            "check_id": "VAL3475_7_no_claim",
            "passed": no_claim,
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        }
    )
    no_formalization_output = all(not str(path).startswith(str(FORMALIZATION)) for path in outputs.values())
    validation.append(
        {
            "check_id": "VAL3475_8_no_formalization_outputs",
            "passed": no_formalization_output,
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": False,
        }
    )
    formalization_status = git_formalization_status()
    validation.append(
        {
            "check_id": "VAL3475_9_git_formalization_clean",
            "passed": formalization_status in {"CLEAN", "NOT_A_GIT_REPOSITORY"},
            "detail": formalization_status,
            "valid_for_claim": False,
        }
    )
    passed = all(parse_bool(row["passed"]) for row in validation)
    validation.append(
        {
            "check_id": "VAL3475_SUMMARY",
            "passed": passed,
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": False,
        }
    )
    return validation


def write_doc(rows_by_output: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 3475: Surviving Mass/Electron Null Direction Theorem Or Clock Mu Row

## Current Verdict
- **Actual movement:** the Sr/Cs clock mass-ratio sensitivity row kills the last algebraic null direction left by 3474.
- **Rank result:** WEP + Yb alpha-clock + Sr/Cs mass-ratio sensitivity reaches conditional rank `4` in the four visible Damour-Dodonoghue-style channels.
- **No claim:** this is sensitivity-rank closure only. It is not a local-GR/WEP/R10/clock pass until parent transport, source normalization, and MTS field-time maps are signed.
- **Best interpretation:** the visible coefficient vector is now boxed in; the hard missing piece is the parent-owned coupling/transport from MTS residuals into those visible coefficients.

## Mass-Ratio Owner Theorem Attempt
{md_table(rows_by_output["theorem_attempt"])}

## Sr/Cs Mu Sensitivity Source Row
{md_table(rows_by_output["mu_source"])}

## Augmented Full-Rank Matrix
{md_table(rows_by_output["matrix"])}

## Rank Ledger
{md_table(rows_by_output["rank"])}

## Nullspace
{md_table(rows_by_output["nullspace"])}

## Previous Survivor Impact
{md_table(rows_by_output["impact"])}

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
    previous_rows = previous_matrix_rows()
    previous_rank_row = read_csv(SOURCES["rank_3474"]["path"])[0]
    previous_rank = int(previous_rank_row["rank"])
    previous_null_dim = int(previous_rank_row["nullspace_dimension"])
    survivor = previous_null_vector()
    sr_cs_rows, sr_cs_vector = sr_cs_source_rows()
    matrix_rows = augmented_rows(previous_rows, sr_cs_vector)
    matrix = previous_matrix_values(matrix_rows)
    rank_rows, basis = rank_ledger_rows(previous_rank, previous_null_dim, matrix)
    null_rows = nullspace_rows(basis)
    impact = impact_rows(survivor, sr_cs_vector)
    rank = int(rank_rows[0]["rank"])
    null_dim = int(rank_rows[0]["nullspace_dimension"])
    rows_by_output: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "theorem_attempt": theorem_attempt_rows(survivor),
        "mu_source": sr_cs_rows,
        "matrix": matrix_rows,
        "rank": rank_rows,
        "nullspace": null_rows,
        "impact": impact,
        "claim_gates": claim_gates(rank, null_dim, impact),
        "decision": decision_rows(rank, null_dim),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(outputs[key], rows)
    validation = validation_rows(outputs, matrix, rank, null_dim, impact, rows_by_output)
    rows_by_output["validation"] = validation
    write_csv(outputs["validation"], validation)
    write_doc(rows_by_output)


if __name__ == "__main__":
    main()
