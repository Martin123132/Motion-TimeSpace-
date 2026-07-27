from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


RUN_STARTED = datetime.now(timezone.utc)
RUN_STARTED_TS = RUN_STARTED.timestamp()

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3197_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3197_DOMAIN_STIFFNESS_THEOREM.csv"
MODEL_SCAN = OUT / "P8_Y5_R2FR_3197_DOMAIN_STIFFNESS_MODEL_SCAN.csv"
COMPATIBILITY = OUT / "P8_Y5_R2FR_3197_DOMAIN_STIFFNESS_COMPATIBILITY_RUNNER.csv"
GATES = OUT / "P8_Y5_R2FR_3197_PARENT_DOMAIN_GATE.csv"
CLASSIFICATION = OUT / "P8_Y5_R2FR_3197_ROUTE_CLASSIFICATION.csv"
DECISION = OUT / "P8_Y5_R2FR_3197_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3197_VALIDATION.csv"

MULTIPLIERS_3194 = OUT / "P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv"
VALIDATION_3196 = OUT / "P8_Y5_R2FR_3196_VALIDATION.csv"

DIMENSION = 4
TOL = 1.0e-10


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(base: str, relative: str) -> Path:
    if base == "post_checkpoint":
        return ROOT / relative
    if base == "formalization":
        return FW / relative
    raise ValueError(base)


def identity(size: int = DIMENSION) -> list[list[float]]:
    return [[1.0 if row == column else 0.0 for column in range(size)] for row in range(size)]


def diagonal(values: list[float]) -> list[list[float]]:
    return [[values[row] if row == column else 0.0 for column in range(len(values))] for row in range(len(values))]


def scale_matrix(matrix: list[list[float]], scalar: float) -> list[list[float]]:
    return [[scalar * value for value in row] for row in matrix]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left_row[index] * right[index][column] for index in range(len(right))) for column in range(len(right[0]))]
        for left_row in left
    ]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[index] * vector[index] for index in range(len(vector))) for row in matrix]


def subtract(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [left[row][column] - right[row][column] for column in range(len(left[row]))]
        for row in range(len(left))
    ]


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def frobenius_summary(matrix: list[list[float]]) -> str:
    return ";".join(",".join(f"{value:.6e}" for value in row) for row in matrix)


def symmetric_eigenvalues(matrix: list[list[float]]) -> list[float]:
    work = [row[:] for row in matrix]
    size = len(work)
    for _ in range(100):
        pivot_row = 0
        pivot_column = 1
        max_value = 0.0
        for row in range(size):
            for column in range(row + 1, size):
                value = abs(work[row][column])
                if value > max_value:
                    max_value = value
                    pivot_row = row
                    pivot_column = column
        if max_value < 1.0e-14:
            break
        app = work[pivot_row][pivot_row]
        aqq = work[pivot_column][pivot_column]
        apq = work[pivot_row][pivot_column]
        angle = 0.5 * math.atan2(2.0 * apq, aqq - app)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        for index in range(size):
            if index not in (pivot_row, pivot_column):
                aip = work[index][pivot_row]
                aiq = work[index][pivot_column]
                work[index][pivot_row] = cosine * aip - sine * aiq
                work[pivot_row][index] = work[index][pivot_row]
                work[index][pivot_column] = sine * aip + cosine * aiq
                work[pivot_column][index] = work[index][pivot_column]
        work[pivot_row][pivot_row] = cosine**2 * app - 2.0 * sine * cosine * apq + sine**2 * aqq
        work[pivot_column][pivot_column] = sine**2 * app + 2.0 * sine * cosine * apq + cosine**2 * aqq
        work[pivot_row][pivot_column] = 0.0
        work[pivot_column][pivot_row] = 0.0
    return sorted(work[index][index] for index in range(size))


def matrix_rank(matrix: list[list[float]], tolerance: float = 1.0e-10) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = max(range(rank, rows), key=lambda row: abs(work[row][column]))
        if abs(work[pivot][column]) <= tolerance:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        for entry in range(column, columns):
            work[rank][entry] /= pivot_value
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            for entry in range(column, columns):
                work[row][entry] -= factor * work[rank][entry]
        rank += 1
        if rank == rows:
            break
    return rank


def solve_linear(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(matrix)
    work = [row[:] + [value] for row, value in zip(matrix, vector)]
    for pivot_index in range(size):
        pivot_row = max(range(pivot_index, size), key=lambda row: abs(work[row][pivot_index]))
        work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
        pivot = work[pivot_index][pivot_index]
        if abs(pivot) < 1.0e-14:
            raise ValueError("singular linear system")
        for column in range(pivot_index, size + 1):
            work[pivot_index][column] /= pivot
        for row in range(size):
            if row == pivot_index:
                continue
            factor = work[row][pivot_index]
            for column in range(pivot_index, size + 1):
                work[row][column] -= factor * work[pivot_index][column]
    return [work[index][size] for index in range(size)]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3196-Y5-R2FR-auxiliary-layer-field-elimination-or-parent-compliance-matrix-under-AX1090.md",
            "3196 auxiliary layer field and Schur complement gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3196_AUXILIARY_ELIMINATION_DERIVATION.csv",
            "3196 auxiliary elimination derivation",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3196_POSITIVE_SCHUR_COMPLEMENT_MODELS.csv",
            "3196 healthy/rejected Schur models",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3196_VALIDATION.csv",
            "3196 validation evidence",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv",
            "3194 multiplier solutions to recover",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "current parent scaffold; no explicit layer/domain map yet",
        ),
    ]
    return [
        {
            "input_id": f"IN3197_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def theorem_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "theorem_id": "THM3197_0_domain_map",
            "statement": "Let parent domain geometry define a covariant mismatch/constraint map C^A(Phi) whose zero set is the allowed C1 interface.",
            "formula": "C^A(Phi)=0",
            "status": "DOMAIN_CONSTRAINT_TARGET",
        },
        {
            "theorem_id": "THM3197_1_linearization",
            "statement": "Near a matched interface, expand the constraint map in mismatch slots z.",
            "formula": "C=J z + O(z^2)",
            "status": "DERIVED_LOCAL_LINEARIZATION",
        },
        {
            "theorem_id": "THM3197_2_normal_metric",
            "statement": "If the parent supplies a positive normal metric G_N on the constraint codomain, the domain-distance action is positive before pullback.",
            "formula": "S_domain=(1/(2 delta)) C^T G_N C, G_N>0",
            "status": "POSITIVE_NORMAL_METRIC_CONDITION",
        },
        {
            "theorem_id": "THM3197_3_pullback_stiffness",
            "statement": "The induced direct layer stiffness on C1 mismatch slots is the pullback of the normal metric.",
            "formula": "K0=J^T G_N J",
            "status": "PARENT_DOMAIN_STIFFNESS_FORMULA",
        },
        {
            "theorem_id": "THM3197_4_positivity_condition",
            "statement": "K0 is positive definite iff G_N is positive definite and J has full column rank on the mismatch slots.",
            "formula": "v^T K0 v=(Jv)^T G_N (Jv)>0 for all v!=0",
            "status": "POSITIVITY_THEOREM_DERIVED",
        },
        {
            "theorem_id": "THM3197_5_failure_modes",
            "statement": "Rank-deficient J leaves unpenalized mismatch modes; indefinite G_N creates ghost/negative stiffness modes.",
            "formula": "rank(J)<dim(z) or minEig(G_N)<=0 -> no parent-owned positive K0",
            "status": "FAILURE_MODES_DERIVED",
        },
        {
            "theorem_id": "THM3197_6_parent_gate",
            "statement": "The current corpus still must identify C, J, and G_N from MTS parent variables; otherwise K0 remains an effective closure.",
            "formula": "S_parent -> C(Phi), G_N(Phi), J=dC/dz",
            "status": "PARENT_SIGNATURE_REQUIRED",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def domain_models() -> list[dict[str, object]]:
    now = stamp()
    model_specs = [
        ("DOM3197_0_identity_strong", identity(), scale_matrix(identity(), 2.0), 1.0, 1.0, "full-rank identity domain map with strong positive normal metric"),
        ("DOM3197_1_identity_weak", identity(), scale_matrix(identity(), 1.1), 1.0, 1.0, "full-rank identity domain map barely survives auxiliary mixing"),
        ("DOM3197_2_direct_no_aux", identity(), identity(), 0.0, 1.0, "direct parent domain stiffness with no auxiliary mixing"),
        ("DOM3197_3_critical_overcancel", identity(), identity(), 1.0, 1.0, "positive domain stiffness is exactly overcancelled by auxiliary mixing"),
        (
            "DOM3197_4_mixed_full_rank",
            [
                [1.0, 0.2, 0.0, 0.0],
                [0.0, 1.0, 0.2, 0.0],
                [0.0, 0.0, 1.0, 0.2],
                [0.2, 0.0, 0.0, 1.0],
            ],
            scale_matrix(identity(), 1.5),
            0.5,
            1.0,
            "non-diagonal full-rank domain map with positive normal metric",
        ),
        ("DOM3197_5_rank_deficient", diagonal([1.0, 1.0, 1.0, 0.0]), scale_matrix(identity(), 2.0), 0.0, 1.0, "rank-deficient domain map leaves one C1 mismatch slot unowned"),
        ("DOM3197_6_indefinite_metric", identity(), diagonal([1.0, 1.0, 1.0, -1.0]), 0.0, 1.0, "indefinite normal metric produces a ghost stiffness direction"),
    ]
    rows = []
    for model_id, jacobian, normal_metric, b_scalar, mass_scalar, interpretation in model_specs:
        stiffness = matmul(transpose(jacobian), matmul(normal_metric, jacobian))
        auxiliary_subtraction = scale_matrix(identity(), b_scalar**2 / mass_scalar if mass_scalar else 0.0)
        effective_stiffness = subtract(stiffness, auxiliary_subtraction)
        jacobian_rank = matrix_rank(jacobian)
        normal_eigs = symmetric_eigenvalues(normal_metric)
        stiffness_eigs = symmetric_eigenvalues(stiffness)
        effective_eigs = symmetric_eigenvalues(effective_stiffness)
        if min(normal_eigs) <= TOL:
            status = "INDEFINITE_OR_NULL_NORMAL_METRIC_REJECTED"
        elif jacobian_rank < DIMENSION:
            status = "RANK_DEFICIENT_DOMAIN_MAP_REJECTED"
        elif min(stiffness_eigs) <= TOL:
            status = "NONPOSITIVE_PULLBACK_STIFFNESS_REJECTED"
        elif min(effective_eigs) <= TOL:
            status = "AUXILIARY_MIXING_OVERCANCELS_PARENT_STIFFNESS"
        else:
            status = "PARENT_DOMAIN_STIFFNESS_CONDITIONALLY_HEALTHY"
        rows.append(
            {
                "model_id": model_id,
                "slot_dimension": DIMENSION,
                "J_rank": jacobian_rank,
                "G_min_eigenvalue": f"{min(normal_eigs):.15e}",
                "G_max_eigenvalue": f"{max(normal_eigs):.15e}",
                "K0_min_eigenvalue": f"{min(stiffness_eigs):.15e}",
                "K0_max_eigenvalue": f"{max(stiffness_eigs):.15e}",
                "B_scalar": f"{b_scalar:.15e}",
                "M_scalar": f"{mass_scalar:.15e}",
                "Keff_min_eigenvalue": f"{min(effective_eigs):.15e}",
                "Keff_max_eigenvalue": f"{max(effective_eigs):.15e}",
                "K0_matrix": frobenius_summary(stiffness),
                "Keff_matrix": frobenius_summary(effective_stiffness),
                "interpretation": interpretation,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def multiplier_vector(row: dict[str, str]) -> list[float]:
    return [
        float(row["lambda_left_Pi1"]),
        float(row["lambda_left_Pi0"]),
        float(row["lambda_right_Pi1"]),
        float(row["lambda_right_Pi0"]),
    ]


def parse_matrix(summary: str) -> list[list[float]]:
    return [[float(value) for value in row.split(",")] for row in summary.split(";")]


def compatibility_rows(models: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    healthy_models = [row for row in models if row["status"] == "PARENT_DOMAIN_STIFFNESS_CONDITIONALLY_HEALTHY"]
    rows: list[dict[str, object]] = []
    epsilons = [1.0e-9, 1.0e-12]
    for multiplier in read_csv(MULTIPLIERS_3194):
        lambda_vector = multiplier_vector(multiplier)
        lambda_norm = math.sqrt(dot(lambda_vector, lambda_vector))
        for model in healthy_models:
            stiffness = parse_matrix(str(model["Keff_matrix"]))
            for epsilon in epsilons:
                mismatch = [epsilon * value for value in solve_linear(stiffness, lambda_vector)]
                recovered = [value / epsilon for value in matvec(stiffness, mismatch)]
                residuals = [recovered[index] - lambda_vector[index] for index in range(DIMENSION)]
                layer_energy = 0.5 * dot(lambda_vector, [value / epsilon for value in mismatch]) * epsilon
                rows.append(
                    {
                        "run_id": f"DG3197_{multiplier['solution_id']}_{model['model_id']}_eps{epsilon:.0e}",
                        "source_solution": multiplier["solution_id"],
                        "source_selection": multiplier["source_selection"],
                        "domain_model_id": model["model_id"],
                        "transition_width": multiplier["transition_width"],
                        "epsilon_delta": f"{epsilon:.15e}",
                        "lambda_norm": f"{lambda_norm:.15e}",
                        "mismatch_norm": f"{math.sqrt(dot(mismatch, mismatch)):.15e}",
                        "layer_energy_proxy": f"{layer_energy:.15e}",
                        "recovered_lambda_norm": f"{math.sqrt(dot(recovered, recovered)):.15e}",
                        "max_abs_recovery_residual": f"{max(abs(value) for value in residuals):.15e}",
                        "status": "DOMAIN_STIFFNESS_RECOVERS_MULTIPLIERS_NONCLAIM",
                        "valid_for_claim": "false",
                        "generated_utc": now,
                    }
                )
    return rows


def gate_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "gate_id": "GATE3197_0_parent_domain_map",
            "requirement": "Identify the parent covariant domain/constraint map C(Phi) whose zero set is the allowed local interface.",
            "current_evidence": "3197 derives the required form but does not find a parent-owned C(Phi) in the current scaffold.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
        {
            "gate_id": "GATE3197_1_full_rank_jacobian",
            "requirement": "Prove J=dC/dz has full rank on the four C1 mismatch slots.",
            "current_evidence": "Model scan shows full-rank works and rank-deficient maps fail.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
        {
            "gate_id": "GATE3197_2_positive_normal_metric",
            "requirement": "Derive a positive normal metric G_N from parent field-space/domain geometry.",
            "current_evidence": "Model scan shows positivity is sufficient, but G_N is not parent-sourced.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
        {
            "gate_id": "GATE3197_3_auxiliary_mixing_bound",
            "requirement": "Show auxiliary mixing B M^-1 B^T does not overcancel K0.",
            "current_evidence": "3197 includes healthy, weak, and overcancelled cases.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
        {
            "gate_id": "GATE3197_4_covariant_layer_measure",
            "requirement": "Lift the radial mismatch map to a covariant hypersurface/domain measure.",
            "current_evidence": "Current construction remains profile-level.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
        {
            "gate_id": "GATE3197_5_observable_transfer",
            "requirement": "Propagate any residual finite-layer/domain terms into PPN, clocks, WEP, orbital, and R10/local-G tests.",
            "current_evidence": "No empirical residual transfer has been run for the domain-stiffness route.",
            "status": "OPEN",
            "blocks_claim": "true",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def classification_rows(models: list[dict[str, object]], compatibility: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    healthy = [row for row in models if row["status"] == "PARENT_DOMAIN_STIFFNESS_CONDITIONALLY_HEALTHY"]
    rank_fail = next(row for row in models if row["status"] == "RANK_DEFICIENT_DOMAIN_MAP_REJECTED")
    metric_fail = next(row for row in models if row["status"] == "INDEFINITE_OR_NULL_NORMAL_METRIC_REJECTED")
    overcancel = next(row for row in models if row["status"] == "AUXILIARY_MIXING_OVERCANCELS_PARENT_STIFFNESS")
    max_recovery = max(float(row["max_abs_recovery_residual"]) for row in compatibility)
    return [
        {
            "classification_id": "CLASS3197_0_theorem_status",
            "finding": "Positive direct layer stiffness can be parent-owned if it is the pullback K0=J^T G_N J of a positive normal metric by a full-rank domain map.",
            "math_status": "DOMAIN_STIFFNESS_THEOREM_DERIVED",
            "physics_status": "PARENT_DOMAIN_OBJECTS_NOT_IDENTIFIED",
            "next_requirement": "extract C(Phi), J, and G_N from the parent MTS object language",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3197_1_healthy_models",
            "finding": f"{len(healthy)} model rows satisfy positivity and recover the multiplier chain with max residual {max_recovery:.15e}.",
            "math_status": "CONDITIONAL_MODELS_PASS",
            "physics_status": "EFFECTIVE_NOT_PARENT_SIGNED",
            "next_requirement": "source the model coefficients from MTS rather than choosing matrices",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3197_2_rank_failure",
            "finding": f"Rank-deficient model {rank_fail['model_id']} is rejected: J_rank={rank_fail['J_rank']} leaves an unowned mismatch slot.",
            "math_status": "RANK_GATE_SHARP",
            "physics_status": "PREVENTS_PARTIAL_GLUING_CLAIM",
            "next_requirement": "prove full-rank domain control of all C1 mismatch slots",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3197_3_metric_failure",
            "finding": f"Indefinite normal metric model {metric_fail['model_id']} is rejected: minEig(G_N)={metric_fail['G_min_eigenvalue']}.",
            "math_status": "GHOST_GATE_SHARP",
            "physics_status": "PREVENTS_NEGATIVE_STIFFNESS_CLAIM",
            "next_requirement": "derive positive parent normal metric",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3197_4_overcancel_failure",
            "finding": f"Auxiliary mixing can overcancel otherwise positive K0: {overcancel['model_id']} has minEig(Keff)={overcancel['Keff_min_eigenvalue']}.",
            "math_status": "SCHUR_BOUND_GATE_SHARP",
            "physics_status": "AUXILIARY_MIXING_BOUND_REQUIRED",
            "next_requirement": "derive a lower bound K0 > B M^-1 B^T from parent dynamics",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3197_0_positive_stiffness_route",
            "finding": "A parent-owned positive layer stiffness route exists in theorem form: K0=J^T G_N J with G_N>0 and rank(J)=4.",
            "claim_status": "DOMAIN_GEOMETRY_ROUTE_DERIVED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3197_1_not_parent_signed",
            "finding": "The current scaffold does not yet identify the parent domain map C(Phi), normal metric G_N, or full-rank Jacobian J.",
            "claim_status": "PARENT_SIGNATURE_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3197_2_local_GR_status",
            "finding": "Local-GR remains blocked, but the obstruction is now narrowed to parent domain-object extraction plus residual transfer.",
            "claim_status": "LOCAL_GR_STILL_BLOCKED_NARROWER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3197_3_next_target",
            "finding": "3198-Y5-R2FR-parent-domain-map-extraction-or-local-closure-demotion-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def formalization_recent_file_count() -> int:
    if not FW.exists():
        return -1
    count = 0
    for path in FW.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= RUN_STARTED_TS:
            count += 1
    return count


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    theorem = rows_by_path[THEOREM]
    models = rows_by_path[MODEL_SCAN]
    compatibility = rows_by_path[COMPATIBILITY]
    gates = rows_by_path[GATES]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    recent_fw = formalization_recent_file_count()
    healthy = [row for row in models if row["status"] == "PARENT_DOMAIN_STIFFNESS_CONDITIONALLY_HEALTHY"]
    rejected = [row for row in models if row["status"] != "PARENT_DOMAIN_STIFFNESS_CONDITIONALLY_HEALTHY"]
    max_recovery = max(float(row["max_abs_recovery_residual"]) for row in compatibility)
    expected_compatibility = len(healthy) * len(read_csv(MULTIPLIERS_3194)) * 2
    return [
        {
            "check_id": "VAL3197_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_1_theorem_present",
            "check": "domain stiffness theorem records pullback formula, positivity condition, and failure modes",
            "pass": str(
                any(row["status"] == "PARENT_DOMAIN_STIFFNESS_FORMULA" for row in theorem)
                and any(row["status"] == "POSITIVITY_THEOREM_DERIVED" for row in theorem)
                and any(row["status"] == "FAILURE_MODES_DERIVED" for row in theorem)
            ).lower(),
            "detail": "K0=J^T G_N J",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_2_model_scan",
            "check": "model scan contains healthy and rejected domain-stiffness cases",
            "pass": str(len(healthy) >= 3 and len(rejected) >= 3).lower(),
            "detail": f"healthy={len(healthy)}; rejected={len(rejected)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_3_healthy_positive",
            "check": "healthy models have full rank, positive normal metric, and positive effective stiffness",
            "pass": str(all(int(row["J_rank"]) == DIMENSION and float(row["G_min_eigenvalue"]) > 0.0 and float(row["Keff_min_eigenvalue"]) > 0.0 for row in healthy)).lower(),
            "detail": "rank/metric/Schur gates pass for healthy rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_4_rejected_failure_modes",
            "check": "rank, metric, and overcancel failure modes are all represented",
            "pass": str(
                any(row["status"] == "RANK_DEFICIENT_DOMAIN_MAP_REJECTED" for row in models)
                and any(row["status"] == "INDEFINITE_OR_NULL_NORMAL_METRIC_REJECTED" for row in models)
                and any(row["status"] == "AUXILIARY_MIXING_OVERCANCELS_PARENT_STIFFNESS" for row in models)
            ).lower(),
            "detail": "all no-go guards present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_5_multiplier_recovery",
            "check": "domain stiffness compatibility rows recover the 3194 multipliers",
            "pass": str(len(compatibility) == expected_compatibility and max_recovery < 1.0e-10).lower(),
            "detail": f"compatibility_rows={len(compatibility)}; expected_rows={expected_compatibility}; max_recovery={max_recovery:.15e}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_6_parent_gates_open",
            "check": "parent domain gates remain explicit blockers",
            "pass": str(len(gates) == 6 and all(row["status"] == "OPEN" and row["blocks_claim"] == "true" for row in gates)).lower(),
            "detail": f"open_gates={len(gates)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_7_next_target_selected",
            "check": "decision selects parent-domain-map extraction or closure demotion",
            "pass": str(any("3198-Y5-R2FR-parent-domain-map-extraction" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3198",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_8_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3197_9_formalization_workbench_untouched",
            "check": "formalization-workbench files modified during this run remain zero",
            "pass": str(recent_fw == 0).lower(),
            "detail": f"formalization_recent_file_count={recent_fw}",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    inputs = input_rows()
    theorem = theorem_rows()
    models = domain_models()
    compatibility = compatibility_rows(models)
    gates = gate_rows()
    classification = classification_rows(models, compatibility)
    decisions = decision_rows()
    return {
        INPUTS: inputs,
        THEOREM: theorem,
        MODEL_SCAN: models,
        COMPATIBILITY: compatibility,
        GATES: gates,
        CLASSIFICATION: classification,
        DECISION: decisions,
    }


def main() -> None:
    rows_by_path = all_output_rows()
    rows_by_path[VALIDATION] = validation_rows(rows_by_path)
    for path, rows in rows_by_path.items():
        write_csv(path, rows)
    for path in rows_by_path:
        print(path)


if __name__ == "__main__":
    main()
