from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4254"
CLAIM_ID = "L-095"
BRANCH = "MTS_R2FR_Y5_FILL_SOURCE_PROBE_RANK_OR_PARENT_PI4_JACOBIAN_ROW_4254"
DECISION = "SOURCE_PROBE_SVD_RANK_RUNNER_BUILT_CURRENT_DQ_VALUES_MISSING_NONCLAIM"
MARKER = "PPC4161_SOURCE_PROBE_RANK_OR_PARENT_PI4_JACOBIAN_4254"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_PROBE_RANK_OR_PARENT_PI4_JACOBIAN_4254"
NEXT_TARGET = "4255-Y5-R2FR-fill-first-Dq-probe-matrix-row-or-parent-Pi4-source-row.md"

FORMAL_PATH = FORMAL / "270-PPC4161-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md"
DOC_PATH = POST / "4254-Y5-R2FR-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4254_VALIDATION.csv"

MATRIX_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_SOURCE_PROBE_MATRIX_CANDIDATE.csv"
COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CONSTANT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_TOMOGRAPHY_CONSTANTS_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
TOL = 1.0e-14


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4254_00_4253_formal": SourceSpec(
        "SRC4254_00_4253_formal",
        FORMAL / "269-PPC4161-source-Jacobian-or-first-direct-Hperp-profile-fill.md",
        "sigma_S := lower singular value of S",
        "4253 source-probe tomography bridge.",
    ),
    "SRC4254_01_4253_next": SourceSpec(
        "SRC4254_01_4253_next",
        SOURCE_DIR / "P8_Y5_R2FR_4253_NEXT_TARGET.csv",
        "Fill source-probe rank/tomography rows",
        "4253 selected rank/tomography fill or Pi4 source row.",
    ),
    "SRC4254_02_4243_matrix": SourceSpec(
        "SRC4254_02_4243_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4243_DQ_COMPONENT_BOUND_MATRIX.csv",
        "Dq_geom[H_L]",
        "Current Dq component matrix to audit for numeric values.",
    ),
    "SRC4254_03_4243_bound": SourceSpec(
        "SRC4254_03_4243_bound",
        SOURCE_DIR / "P8_Y5_R2FR_4243_SOURCE_DEFECT_BOUND_ROWS.csv",
        "C_S C_perp E_Dq,H",
        "4243 source-defect envelope.",
    ),
    "SRC4254_04_259_formal": SourceSpec(
        "SRC4254_04_259_formal",
        FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "E_Dq,H^2 := sum_i",
        "Formal weighted Dq envelope definition.",
    ),
    "SRC4254_05_4249_schema": SourceSpec(
        "SRC4254_05_4249_schema",
        SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUT_SCHEMA.csv",
        "h_U_C1",
        "4249 input row that receives computed h_U_C1.",
    ),
    "SRC4254_06_4252_template": SourceSpec(
        "SRC4254_06_4252_template",
        SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_TEMPLATE.csv",
        "derivative_direction",
        "Alternative parent Pi4/Jacobian route.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


def parse_float(value: str) -> Optional[float]:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def contains_missing_marker(values: Iterable[str]) -> bool:
    return any("MISSING_" in str(value) or "PLACEHOLDER" in str(value) for value in values)


def split_paths(value: str) -> List[Path]:
    if not value:
        return []
    return [Path(piece.strip()) for piece in str(value).split(";") if piece.strip()]


def all_source_paths_exist(value: str) -> bool:
    paths = split_paths(value)
    return bool(paths) and all(path.exists() for path in paths)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def current_dq_audit_rows() -> List[Dict[str, str]]:
    rows = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4243_DQ_COMPONENT_BOUND_MATRIX.csv")
    if not rows:
        return [
            {
                **common(),
                "component_id": "NO_4243_MATRIX",
                "component": "",
                "numeric_value": "",
                "audit_status": "MISSING_4243_MATRIX",
                "can_fill_4254": "False",
                "valid_for_claim": "False",
            }
        ]
    output: List[Dict[str, str]] = []
    for row in rows:
        numeric = parse_float(row.get("numeric_value", ""))
        source_path = row.get("source_path", "")
        can_fill = numeric is not None and all_source_paths_exist(source_path) and truthy(row.get("valid_for_claim", ""))
        output.append(
            {
                **common(),
                "component_id": row.get("component_id", ""),
                "component": row.get("component", ""),
                "numeric_value": row.get("numeric_value", ""),
                "bound_status": row.get("bound_status", ""),
                "source_path": source_path,
                "audit_status": "NUMERIC_SOURCE_BACKED" if can_fill else "NOT_NUMERIC_SOURCE_BACKED",
                "can_fill_4254": str(can_fill),
                "valid_for_claim": "False",
            }
        )
    return output


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SPR4254_0_weighted_rank_gate",
            "weighted source-probe rank gate",
            "For source-probe matrix S and probe weights W=diag(w_i), sigma_S^2=lambda_min(S^T W S). The Dq-defect profile route can bound the whole live Hperp sector only if sigma_S>0.",
            "EXACT_FINITE_DIMENSIONAL_RANK_CRITERION",
            "No spanning source-probe rank, no direct Hperp profile claim.",
            "MISSING_SOURCE_PROBE_MATRIX_OR_RANK",
        ),
        (
            "SPR4254_1_weighted_defect_envelope",
            "weighted Dq envelope",
            "E_Dq,H = sqrt(sum_i w_i epsilon_i^2), with epsilon_i source-backed bounds for Dq_i[Hperp] or Dq_i[H_L] after the 4245 split.",
            "DERIVED_EXECUTABLE_ENVELOPE",
            "Turns the 4243 component ledger into a computable norm.",
            "MISSING_EPSILON_I_VALUES",
        ),
        (
            "SPR4254_2_AH_bound",
            "tomographic amplitude bound",
            "If sigma_S>0, A_H <= (C_S C_perp/sigma_S) E_Dq,H + eta_domain.",
            "DERIVED_BOUND_RUNNER_FORM",
            "A direct Hperp profile can be sourced without fabricating Hperp itself.",
            "MISSING_C_S_C_PERP_SIGMA_E_DQ",
        ),
        (
            "SPR4254_3_C1_bound",
            "tomographic C1 bound",
            "For differentiated source-probe matrix S1, h_U_C1 <= (C_S1 C_perp/sigma_S1) E_Dq,H_C1 + (nabla_S_norm/sigma_S1) A_H + eta_C1.",
            "DERIVED_C1_RUNNER_FORM",
            "Feeds the 4249 local C1 response gate.",
            "MISSING_C1_PROBE_MATRIX_AND_DERIVATIVE_VALUES",
        ),
        (
            "SPR4254_4_parent_Pi4_alternative",
            "parallel parent-Jacobian route",
            "If parent Pi4/X_m/X_a rows are sourced first, 4252 computes C_mZ and C_ZZ directly; if source-probe rank rows are sourced first, 4254 computes A_H and h_U_C1 directly.",
            "ROUTE_SPLIT_CLARIFIED",
            "Both routes lead to 4249 but forbid hand-picked Pi4 or unsourced Hperp.",
            "MISSING_EITHER_ROUTE_INPUTS",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, result, missing in raw
    ]


def probe_matrix_template_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row_type in ("amplitude", "C1"):
        for probe_id in ("Dq_geom", "Dq_tau", "Dq_matter", "Dq_source_readout", "Dq_theta_marker", "Dq_boundary_projector", "Dq_EM", "Dq_coeff"):
            for basis_id in ("Hbasis_0", "Hbasis_1"):
                rows.append(
                    {
                        **common(),
                        "candidate_id": "TEMPLATE_ONLY",
                        "row_type": row_type,
                        "probe_id": probe_id,
                        "basis_id": basis_id,
                        "coefficient": "MISSING_PROBE_MATRIX_COEFFICIENT",
                        "units": "normalized_probe_per_Hbasis",
                        "source_path": "MISSING_SOURCE_PATH",
                        "valid_for_claim": "False",
                    }
                )
    return rows


def component_template_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for probe_id in ("Dq_geom", "Dq_tau", "Dq_matter", "Dq_source_readout", "Dq_theta_marker", "Dq_boundary_projector", "Dq_EM", "Dq_coeff"):
        rows.append(
            {
                **common(),
                "candidate_id": "TEMPLATE_ONLY",
                "probe_id": probe_id,
                "weight": "1.0",
                "epsilon": "MISSING_DQ_EPSILON",
                "epsilon_C1": "MISSING_DQ_C1_EPSILON",
                "source_path": "MISSING_SOURCE_PATH",
                "valid_for_claim": "False",
            }
        )
    return rows


def constants_template_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "TEMPLATE_ONLY",
            "C_S": "MISSING_C_S",
            "C_perp": "MISSING_C_PERP",
            "eta_domain": "MISSING_ETA_DOMAIN_OR_ZERO",
            "C_S1": "MISSING_C_S1",
            "nabla_S_norm": "MISSING_NABLA_S_NORM",
            "eta_C1": "MISSING_ETA_C1_OR_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "False",
        }
    ]


def jacobi_eigenvalues_symmetric(matrix: List[List[float]]) -> List[float]:
    n = len(matrix)
    if n == 0:
        return []
    a = [row[:] for row in matrix]
    for _ in range(100 * n * n):
        p, q = 0, 1 if n > 1 else 0
        max_offdiag = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                value = abs(a[i][j])
                if value > max_offdiag:
                    max_offdiag = value
                    p, q = i, j
        if max_offdiag < 1.0e-12:
            break
        if p == q:
            break
        if abs(a[p][p] - a[q][q]) < 1.0e-30:
            angle = math.pi / 4.0
        else:
            angle = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * a[p][p] - 2.0 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2.0 * s * c * a[p][q] + c * c * a[q][q]
        a[p][q] = 0.0
        a[q][p] = 0.0
        for k in range(n):
            if k in (p, q):
                continue
            akp = c * a[k][p] - s * a[k][q]
            akq = s * a[k][p] + c * a[k][q]
            a[k][p] = akp
            a[p][k] = akp
            a[k][q] = akq
            a[q][k] = akq
        a[p][p] = app
        a[q][q] = aqq
    return sorted(a[i][i] for i in range(n))


def weighted_sigma(matrix: List[List[float]], weights: List[float]) -> Tuple[float, str]:
    if not matrix or not matrix[0]:
        return 0.0, "EMPTY_MATRIX"
    columns = len(matrix[0])
    if len(matrix) < columns:
        return 0.0, "ROW_RANK_LT_COLUMNS"
    gram = [[0.0 for _ in range(columns)] for _ in range(columns)]
    for row, weight in zip(matrix, weights):
        for i in range(columns):
            for j in range(columns):
                gram[i][j] += weight * row[i] * row[j]
    eigenvalues = jacobi_eigenvalues_symmetric(gram)
    min_eval = min(eigenvalues) if eigenvalues else 0.0
    if min_eval <= TOL:
        return 0.0, "SINGULAR_OR_UNDERDETERMINED"
    return math.sqrt(min_eval), "FULL_RANK"


def grouped_candidate_rows(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        candidate_id = row.get("candidate_id", "").strip()
        if candidate_id:
            grouped.setdefault(candidate_id, []).append(row)
    return grouped


def build_matrix(rows: List[Dict[str, str]], row_type: str, probe_ids: List[str], basis_ids: List[str]) -> Optional[List[List[float]]]:
    entries: Dict[Tuple[str, str], float] = {}
    for row in rows:
        if row.get("row_type", "").strip() != row_type:
            continue
        probe_id = row.get("probe_id", "").strip()
        basis_id = row.get("basis_id", "").strip()
        coefficient = parse_float(row.get("coefficient", ""))
        if probe_id and basis_id and coefficient is not None:
            entries[(probe_id, basis_id)] = coefficient
    matrix: List[List[float]] = []
    for probe_id in probe_ids:
        row_values: List[float] = []
        for basis_id in basis_ids:
            value = entries.get((probe_id, basis_id))
            if value is None:
                return None
            row_values.append(value)
        matrix.append(row_values)
    return matrix


def row_group_valid(rows: List[Dict[str, str]]) -> bool:
    return (
        bool(rows)
        and all(truthy(row.get("valid_for_claim", "")) for row in rows)
        and all(all_source_paths_exist(row.get("source_path", "")) for row in rows)
        and not contains_missing_marker(value for row in rows for value in row.values())
    )


def tomography_results() -> List[Dict[str, str]]:
    missing_files = [
        str(path)
        for path in (MATRIX_CANDIDATE_PATH, COMPONENT_CANDIDATE_PATH, CONSTANT_CANDIDATE_PATH)
        if not path.exists()
    ]
    if missing_files:
        return [
            {
                **common(),
                "candidate_id": "NO_TOMOGRAPHY_CANDIDATE_FILES",
                "status": "BLOCKED_MISSING_CANDIDATE_FILES",
                "missing_files": ";".join(missing_files),
                "sigma_S": "",
                "E_Dq_H": "",
                "A_H_bound": "",
                "sigma_S1": "",
                "E_Dq_H_C1": "",
                "h_U_C1_bound": "",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]

    matrix_groups = grouped_candidate_rows(csv_rows(MATRIX_CANDIDATE_PATH))
    component_groups = grouped_candidate_rows(csv_rows(COMPONENT_CANDIDATE_PATH))
    constant_groups = grouped_candidate_rows(csv_rows(CONSTANT_CANDIDATE_PATH))
    candidate_ids = sorted(set(matrix_groups) | set(component_groups) | set(constant_groups))
    output: List[Dict[str, str]] = []
    for candidate_id in candidate_ids:
        matrix_rows = matrix_groups.get(candidate_id, [])
        component_rows = component_groups.get(candidate_id, [])
        constant_rows = constant_groups.get(candidate_id, [])
        if not matrix_rows or not component_rows or not constant_rows:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_INCOMPLETE_CANDIDATE_GROUP",
                    "missing": ";".join(
                        name
                        for name, rows in (("matrix", matrix_rows), ("components", component_rows), ("constants", constant_rows))
                        if not rows
                    ),
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        constants = constant_rows[0]
        parsed_constants = {field: parse_float(constants.get(field, "")) for field in ("C_S", "C_perp", "eta_domain", "C_S1", "nabla_S_norm", "eta_C1")}
        missing_constants = [field for field, value in parsed_constants.items() if value is None]
        probe_ids = sorted({row.get("probe_id", "").strip() for row in component_rows if row.get("probe_id", "").strip()})
        basis_ids = sorted({row.get("basis_id", "").strip() for row in matrix_rows if row.get("basis_id", "").strip()})
        weights: List[float] = []
        epsilons: List[float] = []
        epsilons_c1: List[float] = []
        missing_components: List[str] = []
        component_by_probe = {row.get("probe_id", "").strip(): row for row in component_rows}
        for probe_id in probe_ids:
            component = component_by_probe[probe_id]
            weight = parse_float(component.get("weight", ""))
            epsilon = parse_float(component.get("epsilon", ""))
            epsilon_c1 = parse_float(component.get("epsilon_C1", ""))
            if weight is None or epsilon is None or epsilon_c1 is None:
                missing_components.append(probe_id)
                continue
            weights.append(weight)
            epsilons.append(epsilon)
            epsilons_c1.append(epsilon_c1)
        matrix = build_matrix(matrix_rows, "amplitude", probe_ids, basis_ids)
        matrix_c1 = build_matrix(matrix_rows, "C1", probe_ids, basis_ids)
        if missing_constants or missing_components or matrix is None or matrix_c1 is None:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_MISSING_NUMERIC_MATRIX_OR_COMPONENTS",
                    "missing": ";".join(missing_constants + missing_components + ([] if matrix is not None else ["amplitude_matrix"]) + ([] if matrix_c1 is not None else ["C1_matrix"])),
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        sigma, rank_status = weighted_sigma(matrix, weights)
        sigma_c1, rank_status_c1 = weighted_sigma(matrix_c1, weights)
        E_dq = math.sqrt(sum(weight * epsilon * epsilon for weight, epsilon in zip(weights, epsilons)))
        E_dq_c1 = math.sqrt(sum(weight * epsilon * epsilon for weight, epsilon in zip(weights, epsilons_c1)))
        if sigma <= 0.0 or sigma_c1 <= 0.0:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_SOURCE_PROBE_RANK",
                    "rank_status": rank_status,
                    "rank_status_C1": rank_status_c1,
                    "sigma_S": f"{sigma:.12e}",
                    "E_Dq_H": f"{E_dq:.12e}",
                    "sigma_S1": f"{sigma_c1:.12e}",
                    "E_Dq_H_C1": f"{E_dq_c1:.12e}",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        C_S = parsed_constants["C_S"] or 0.0
        C_perp = parsed_constants["C_perp"] or 0.0
        eta_domain = parsed_constants["eta_domain"] or 0.0
        C_S1 = parsed_constants["C_S1"] or 0.0
        nabla_S_norm = parsed_constants["nabla_S_norm"] or 0.0
        eta_C1 = parsed_constants["eta_C1"] or 0.0
        A_H_bound = (C_S * C_perp / sigma) * E_dq + eta_domain
        h_U_C1_bound = (C_S1 * C_perp / sigma_c1) * E_dq_c1 + (nabla_S_norm / sigma_c1) * A_H_bound + eta_C1
        input_valid = row_group_valid(matrix_rows) and row_group_valid(component_rows) and row_group_valid(constant_rows)
        output.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "status": "SOURCE_PROBE_TOMOGRAPHY_COMPUTED_NONCLAIM",
                "rank_status": rank_status,
                "rank_status_C1": rank_status_c1,
                "basis_count": str(len(basis_ids)),
                "probe_count": str(len(probe_ids)),
                "sigma_S": f"{sigma:.12e}",
                "E_Dq_H": f"{E_dq:.12e}",
                "A_H_bound": f"{A_H_bound:.12e}",
                "sigma_S1": f"{sigma_c1:.12e}",
                "E_Dq_H_C1": f"{E_dq_c1:.12e}",
                "h_U_C1_bound": f"{h_U_C1_bound:.12e}",
                "claim_allowed": "False",
                "valid_for_claim": str(input_valid),
            }
        )
    return output or [
        {
            **common(),
            "candidate_id": "NO_CANDIDATE_ROWS",
            "status": "BLOCKED_EMPTY_CANDIDATE_FILES",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def bridge_rows(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    computed = [row for row in results if row.get("status") == "SOURCE_PROBE_TOMOGRAPHY_COMPUTED_NONCLAIM"]
    if not computed:
        return [
            {
                **common(),
                "candidate_id": "NO_4254_TO_4249_BRIDGE",
                "bridge_status": "BLOCKED_NO_TOMOGRAPHY_RESULT",
                "A_H": "MISSING_4254_A_H_BOUND",
                "h_U_C1": "MISSING_4254_h_U_C1_BOUND",
                "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]
    return [
        {
            **common(),
            "candidate_id": row["candidate_id"],
            "bridge_status": "PARTIAL_4249_BRIDGE_READY_NONCLAIM",
            "A_H": row.get("A_H_bound", ""),
            "h_U_C1": row.get("h_U_C1_bound", ""),
            "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in computed
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4254_0_current_audit",
            "Current 4243 Dq component rows are not numeric/source-backed.",
            "The direct profile route cannot score from existing rows.",
            "Fill component candidate rows rather than inventing E_Dq,H.",
        ),
        (
            "DEC4254_1_rank_runner",
            "4254 installs the weighted SVD/rank gate for source-probe tomography.",
            "A positive sigma_S is now an executable condition, not prose.",
            "Use matrix, component, and constant candidate files.",
        ),
        (
            "DEC4254_2_parallel_routes",
            "There are now two concrete routes to 4249: parent Pi4 Jacobian or source-probe tomography.",
            "Either route can produce A_H/h_U_C1 without scalar-memory smuggling.",
            "Pursue whichever gets sourced first.",
        ),
        (
            "DEC4254_3_next",
            "The next source fill is one real matrix row pack or parent Pi4 row pack.",
            "This is the smallest non-circular data/proof object needed.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4254_0_rank", "using source-probe tomography with sigma_S=0 or absent", "SOURCE_PROBE_RANK_REQUIRED", "False"),
        ("FW4254_1_components", "using E_Dq,H without numeric epsilon_i rows", "Dq_COMPONENT_VALUES_REQUIRED", "False"),
        ("FW4254_2_constants", "using C_S/C_perp/eta values without source paths", "TOMOGRAPHY_CONSTANTS_REQUIRED", "False"),
        ("FW4254_3_Pi4", "using hand-picked parent Pi4 instead of source-backed Jacobian rows", "POSTHOC_SELECTOR_FORBIDDEN", "False"),
        ("FW4254_4_claim", "local-GR/PPN/R10/clock/orbital closure", "NONCLAIM_PRIVATE_GATE", "False"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_shortcut": shortcut,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "False",
        }
        for firewall_id, shortcut, reason, claim_allowed in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4254 builds the weighted source-probe rank/SVD runner for the Dq-defect tomography route, audits existing 4243 Dq rows as nonnumeric, and keeps the parent Pi4/Jacobian route open as a parallel source path.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Fill either a source-probe matrix/component/constants pack for 4254 or a parent Pi4/X_m/X_a Jacobian pack for 4252.",
            "avoid": "Do not set sigma_S, E_Dq,H, Pi4, or C constants by convenience; source or prove them.",
            "valid_for_claim": "False",
        }
    ]


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4254 builds the weighted source-probe SVD/rank runner for the Dq-defect tomography route: sigma_S^2=lambda_min(S^T W S), E_Dq,H=sqrt(sum_i w_i epsilon_i^2), and A_H/h_U_C1 bounds are computed only when matrix, component, and constant rows are source-backed.",
        "4254 source register, current Dq audit, weighted rank theorem, probe matrix/component/constants templates, tomography runner, 4249 bridge rows, decision and firewall.",
        "private_source_probe_rank_runner_ready_current_Dq_values_missing_nonclaim",
        "Fill a real source-probe matrix/component/constants pack or a parent Pi4/X_m/X_a Jacobian pack, then rerun 4254/4252 and feed A_H/h_U_C1 into 4249.",
        "Treating a rank-deficient probe set, missing epsilon_i rows, or convenience constants as a direct Hperp profile would smuggle local-GR safety.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    text = f"""
# 270 - PPC4161 fill source-probe rank or parent Pi4 Jacobian row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4254 does not prove local GR, PPN, R10, clock, or orbital safety.

## Main Result

4254 turns the 4253 source-probe bridge into an executable rank gate.

For a source-probe matrix `S` and weights `W=diag(w_i)`:

```text
sigma_S^2 = lambda_min(S^T W S).
```

The direct `Hperp` profile route can bound the full live sector only if:

```text
sigma_S > 0.
```

The Dq envelope is:

```text
E_Dq,H = sqrt(sum_i w_i epsilon_i^2).
```

Then:

```text
A_H <= (C_S C_perp/sigma_S) E_Dq,H + eta_domain.
```

For the C1 route:

```text
h_U_C1 <= (C_S1 C_perp/sigma_S1) E_Dq,H_C1
          + (nabla_S_norm/sigma_S1) A_H
          + eta_C1.
```

## Current Evidence

The existing 4243 Dq component rows are not numeric/source-backed. They remain required input rows, not evidence.

## Parallel Route

The parent `Pi4/X_m/X_a` Jacobian route remains open through 4252. Whichever route is filled first can feed `A_H/h_U_C1` into 4249.

## Next Target

`{NEXT_TARGET}` should fill one real source-probe matrix/component/constants pack or one parent `Pi4/X_m/X_a` Jacobian pack.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4254 - Fill source-probe rank or parent Pi4 Jacobian row

**Status:** `{DECISION}`.

## Result

4254 builds the executable weighted rank runner:

```text
sigma_S^2 = lambda_min(S^T W S),
E_Dq,H = sqrt(sum_i w_i epsilon_i^2),
A_H <= (C_S C_perp/sigma_S) E_Dq,H + eta_domain.
```

The existing 4243 Dq rows are explicit `MISSING`, so the runner is ready but not scoreable.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 source-probe rank or parent Pi4 Jacobian

Marker: `{MARKER}`

4254 installs the weighted source-probe rank runner:

```text
sigma_S^2 = lambda_min(S^T W S),
E_Dq,H = sqrt(sum_i w_i epsilon_i^2),
A_H <= (C_S C_perp/sigma_S) E_Dq,H + eta_domain.
```

The current Dq rows are not numeric, so this remains nonclaim. The parallel parent `Pi4/X_m/X_a` route from 4252 remains open.
"""
    packet_block = f"""
## Packet Update - source-probe rank or parent Pi4 Jacobian

Marker: `{PACKET_MARKER}`

The local packet now has an executable source-probe SVD/rank gate. A direct `Hperp` profile requires a positive `sigma_S`, sourced Dq component envelopes, and sourced tomography constants; otherwise use the parent `Pi4/X_m/X_a` Jacobian path.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    theorems = theorem_rows()
    results = csv_rows(outputs["tomography_results"])
    audit = current_dq_audit_rows()
    validations = [
        ("VAL4254_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4254_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4254_2_rank_theorem", any(row["theorem_id"] == "SPR4254_0_weighted_rank_gate" for row in theorems), "weighted rank theorem emitted"),
        ("VAL4254_3_envelope_theorem", any(row["theorem_id"] == "SPR4254_1_weighted_defect_envelope" for row in theorems), "weighted Dq envelope theorem emitted"),
        ("VAL4254_4_current_audit", any(row["audit_status"] == "NOT_NUMERIC_SOURCE_BACKED" for row in audit), "current 4243 Dq audit performed"),
        ("VAL4254_5_results_nonclaim", all(row.get("claim_allowed", "False") == "False" for row in results), "tomography runner does not claim closure"),
        ("VAL4254_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4254_7_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4254_8_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4254_9_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4254_10_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4254_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4254_SOURCE_REGISTER.csv",
        "current_dq_audit": SOURCE_DIR / "P8_Y5_R2FR_4254_CURRENT_DQ_NUMERIC_AUDIT.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4254_SOURCE_PROBE_RANK_THEOREMS.csv",
        "probe_matrix_template": SOURCE_DIR / "P8_Y5_R2FR_4254_SOURCE_PROBE_MATRIX_TEMPLATE.csv",
        "component_template": SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_TEMPLATE.csv",
        "constants_template": SOURCE_DIR / "P8_Y5_R2FR_4254_TOMOGRAPHY_CONSTANTS_TEMPLATE.csv",
        "tomography_results": SOURCE_DIR / "P8_Y5_R2FR_4254_TOMOGRAPHY_RESULTS.csv",
        "bridge_rows": SOURCE_DIR / "P8_Y5_R2FR_4254_TO_4249_BRIDGE_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4254_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4254_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4254_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4254_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    results = tomography_results()
    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["current_dq_audit"], current_dq_audit_rows())
    write_csv(outputs["theorems"], theorem_rows())
    write_csv(outputs["probe_matrix_template"], probe_matrix_template_rows())
    write_csv(outputs["component_template"], component_template_rows())
    write_csv(outputs["constants_template"], constants_template_rows())
    write_csv(outputs["tomography_results"], results)
    write_csv(outputs["bridge_rows"], bridge_rows(results))
    write_csv(outputs["decision"], decision_rows())
    write_csv(outputs["firewall"], firewall_rows())
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(VALIDATION_PATH, validation_rows(outputs))

    validation = csv_rows(VALIDATION_PATH)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(outputs)} csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
