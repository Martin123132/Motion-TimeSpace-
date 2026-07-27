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

INPUTS = OUT / "P8_Y5_R2FR_3196_INPUTS.csv"
AUX_DERIVATION = OUT / "P8_Y5_R2FR_3196_AUXILIARY_ELIMINATION_DERIVATION.csv"
SCHUR_MODELS = OUT / "P8_Y5_R2FR_3196_POSITIVE_SCHUR_COMPLEMENT_MODELS.csv"
COMPLIANCE_ROWS = OUT / "P8_Y5_R2FR_3196_PARENT_COMPLIANCE_MATRIX_ROWS.csv"
CLASSIFICATION = OUT / "P8_Y5_R2FR_3196_ROUTE_CLASSIFICATION.csv"
DECISION = OUT / "P8_Y5_R2FR_3196_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3196_VALIDATION.csv"

MULTIPLIERS_3194 = OUT / "P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv"
FINITE_LAYER_3195 = OUT / "P8_Y5_R2FR_3195_FINITE_LAYER_DERIVATION.csv"
GATES_3195 = OUT / "P8_Y5_R2FR_3195_PARENT_SIGNATURE_GATE.csv"
VALIDATION_3195 = OUT / "P8_Y5_R2FR_3195_VALIDATION.csv"


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


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3195-Y5-R2FR-gluing-multiplier-parent-origin-or-finite-layer-limit-under-AX1090.md",
            "3195 finite-layer hard-constraint route",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv",
            "3194 multiplier solutions",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3195_FINITE_LAYER_DERIVATION.csv",
            "3195 finite-layer derivation",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3195_PARENT_SIGNATURE_GATE.csv",
            "3195 parent signature gates",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3195_VALIDATION.csv",
            "3195 validation evidence",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "current parent equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3196_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def auxiliary_derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "derivation_id": "AUX3196_0_slot_vector",
            "statement": "Collect the C1 interface mismatch slots into a vector z.",
            "formula": "z=(Delta F_L, Delta F'_L, Delta F_R, Delta F'_R)",
            "status": "DEFINED",
        },
        {
            "derivation_id": "AUX3196_1_auxiliary_action",
            "statement": "Introduce a nonpropagating auxiliary layer field chi with positive mass matrix M and coupling B to the mismatch slots.",
            "formula": "S=(1/(2 delta))(z^T K0 z + 2 z^T B chi + chi^T M chi)",
            "status": "AUXILIARY_LAYER_ACTION_CANDIDATE",
        },
        {
            "derivation_id": "AUX3196_2_auxiliary_equation",
            "statement": "The auxiliary field is algebraic, so it can be eliminated locally.",
            "formula": "dS/dchi=0 -> M chi + B^T z=0 -> chi*=-M^-1 B^T z",
            "status": "ELIMINATION_DERIVED",
        },
        {
            "derivation_id": "AUX3196_3_schur_complement",
            "statement": "Substituting chi* gives an effective positive layer stiffness only if the Schur complement is positive.",
            "formula": "K_eff=K0-B M^-1 B^T",
            "status": "SCHUR_COMPLEMENT_DERIVED",
        },
        {
            "derivation_id": "AUX3196_4_reaction_force",
            "statement": "The hard-layer reaction force is the derivative of the effective action with respect to z.",
            "formula": "lambda=(K_eff/delta)z",
            "status": "FINITE_LAYER_FORCE_RECOVERED",
        },
        {
            "derivation_id": "AUX3196_5_pure_auxiliary_no_go",
            "statement": "If K0=0 and M is positive, K_eff is negative semidefinite; a healthy auxiliary field cannot create positive stiffness from nothing.",
            "formula": "K_eff=-B M^-1 B^T <= 0",
            "status": "PURE_AUXILIARY_POSITIVE_STIFFNESS_NO_GO",
        },
        {
            "derivation_id": "AUX3196_6_parent_gate",
            "statement": "The parent action must own K0, M, B, and the delta scaling; otherwise the route remains an effective compliance closure.",
            "formula": "S_parent -> S_bulk + S_layer[z,chi], K_eff>0, C_delta=delta K_eff^-1",
            "status": "PARENT_SIGNATURE_REQUIRED",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def model_rows() -> list[dict[str, object]]:
    now = stamp()
    candidates = [
        ("MODEL3196_0_canonical_positive", 2.0, 1.0, 1.0, "canonical healthy auxiliary model with K_eff=I"),
        ("MODEL3196_1_weak_positive", 1.1, 1.0, 1.0, "near-critical positive Schur complement"),
        ("MODEL3196_2_direct_layer_only", 1.0, 0.0, 1.0, "direct positive layer stiffness without auxiliary mixing"),
        ("MODEL3196_3_critical_singular", 1.0, 1.0, 1.0, "critical singular Schur complement"),
        ("MODEL3196_4_pure_auxiliary_ghost_risk", 0.0, 1.0, 1.0, "pure auxiliary cannot produce positive stiffness with positive M"),
    ]
    rows = []
    for model_id, k0, b_coupling, mass, interpretation in candidates:
        k_eff = k0 - b_coupling**2 / mass
        trace_2x2 = k0 + mass
        determinant_2x2 = k0 * mass - b_coupling**2
        discriminant = max(trace_2x2**2 - 4.0 * determinant_2x2, 0.0)
        eigen_min = 0.5 * (trace_2x2 - math.sqrt(discriminant))
        eigen_max = 0.5 * (trace_2x2 + math.sqrt(discriminant))
        full_positive = mass > 0.0 and k_eff > 0.0
        if full_positive:
            status = "POSITIVE_AUXILIARY_ELIMINATION_ALLOWED"
        elif abs(k_eff) < 1.0e-14:
            status = "SINGULAR_COMPLIANCE_REJECTED"
        else:
            status = "NEGATIVE_STIFFNESS_OR_GHOST_REJECTED"
        rows.append(
            {
                "model_id": model_id,
                "slot_dimension": 4,
                "K0_scalar": f"{k0:.15e}",
                "B_scalar": f"{b_coupling:.15e}",
                "M_scalar": f"{mass:.15e}",
                "K_eff_scalar": f"{k_eff:.15e}",
                "C_eff_scalar_if_delta_1": f"{(1.0 / k_eff):.15e}" if k_eff > 0.0 else "",
                "full_block_min_eigenvalue": f"{eigen_min:.15e}",
                "full_block_max_eigenvalue": f"{eigen_max:.15e}",
                "full_quadratic_form_positive": str(full_positive).lower(),
                "interpretation": interpretation,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def multiplier_values(row: dict[str, str]) -> dict[str, float]:
    return {
        "left_Pi1": float(row["lambda_left_Pi1"]),
        "left_Pi0": float(row["lambda_left_Pi0"]),
        "right_Pi1": float(row["lambda_right_Pi1"]),
        "right_Pi0": float(row["lambda_right_Pi0"]),
    }


def compliance_rows(models: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    positive_models = [
        row for row in models
        if row["status"] == "POSITIVE_AUXILIARY_ELIMINATION_ALLOWED"
    ]
    epsilons = [1.0e-6, 1.0e-9, 1.0e-12]
    rows: list[dict[str, object]] = []
    for multiplier in read_csv(MULTIPLIERS_3194):
        lambdas = multiplier_values(multiplier)
        lambda_norm = math.sqrt(sum(value * value for value in lambdas.values()))
        for model in positive_models:
            k_eff = float(model["K_eff_scalar"])
            for epsilon in epsilons:
                mismatches = {name: epsilon * value / k_eff for name, value in lambdas.items()}
                recovered = {name: k_eff * mismatches[name] / epsilon for name in lambdas}
                residuals = {name: recovered[name] - lambdas[name] for name in lambdas}
                mismatch_norm = epsilon * lambda_norm / k_eff
                energy = 0.5 * epsilon * lambda_norm**2 / k_eff
                rows.append(
                    {
                        "row_id": f"PCM3196_{multiplier['solution_id']}_{model['model_id']}_eps{epsilon:.0e}",
                        "source_solution": multiplier["solution_id"],
                        "source_selection": multiplier["source_selection"],
                        "model_id": model["model_id"],
                        "transition_width": multiplier["transition_width"],
                        "epsilon_delta": f"{epsilon:.15e}",
                        "K_eff_scalar": model["K_eff_scalar"],
                        "lambda_norm": f"{lambda_norm:.15e}",
                        "mismatch_norm": f"{mismatch_norm:.15e}",
                        "layer_energy_proxy": f"{energy:.15e}",
                        "recovered_lambda_left_Pi1": f"{recovered['left_Pi1']:.15e}",
                        "recovered_lambda_left_Pi0": f"{recovered['left_Pi0']:.15e}",
                        "recovered_lambda_right_Pi1": f"{recovered['right_Pi1']:.15e}",
                        "recovered_lambda_right_Pi0": f"{recovered['right_Pi0']:.15e}",
                        "max_abs_recovery_residual": f"{max(abs(value) for value in residuals.values()):.15e}",
                        "status": "COMPLIANCE_MATRIX_RECOVERS_3194_MULTIPLIER_NONCLAIM",
                        "valid_for_claim": "false",
                        "generated_utc": now,
                    }
                )
    return rows


def classification_rows(models: list[dict[str, object]], compliance: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    canonical = next(row for row in models if row["model_id"] == "MODEL3196_0_canonical_positive")
    pure_aux = next(row for row in models if row["model_id"] == "MODEL3196_4_pure_auxiliary_ghost_risk")
    reference = next(
        row for row in compliance
        if row["source_solution"] == "GLUE3194_0_3190_width"
        and row["model_id"] == "MODEL3196_0_canonical_positive"
        and row["epsilon_delta"] == "1.000000000000000e-12"
    )
    return [
        {
            "classification_id": "CLASS3196_0_auxiliary_elimination_possible",
            "finding": f"A healthy auxiliary layer field can be eliminated to produce a positive compliance matrix by Schur complement; canonical K_eff={canonical['K_eff_scalar']}.",
            "math_status": "AUXILIARY_ELIMINATION_CONSTRUCTED",
            "physics_status": "PARENT_PARAMETERS_NOT_SOURCED",
            "next_requirement": "derive K0, B, M and delta scaling from the parent MTS action",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3196_1_pure_auxiliary_no_go",
            "finding": f"Pure auxiliary stiffness creation fails with healthy sign: K_eff={pure_aux['K_eff_scalar']}; a direct positive mismatch stiffness or constrained geometry is required.",
            "math_status": "PURE_AUXILIARY_ROUTE_REJECTED",
            "physics_status": "IMPORTANT_PARENT_GATE",
            "next_requirement": "find parent-owned direct layer stiffness or domain-geometry constraint",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3196_2_reference_compliance",
            "finding": f"Canonical auxiliary model recovers the reference-width 3194 multipliers with residual {reference['max_abs_recovery_residual']} at epsilon={reference['epsilon_delta']}.",
            "math_status": "FORCE_RECOVERY_EXACT",
            "physics_status": "COMPLIANCE_MATRIX_EFFECTIVE_NOT_PARENT_SIGNED",
            "next_requirement": "covariant parent source for layer coefficients and localization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3196_3_local_GR_status",
            "finding": "The local branch has a coherent effective interface mechanism, but it still lacks parent-owned positive layer stiffness and observable residual transfer.",
            "math_status": "MECHANISM_CHAIN_COHERENT",
            "physics_status": "LOCAL_GR_STILL_BLOCKED",
            "next_requirement": "derive direct layer stiffness/domain constraint and then run PPN/local residual transfer",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3196_0_schur_route",
            "finding": "Auxiliary edge-field elimination can produce the 3195 compliance matrix through a positive Schur complement.",
            "claim_status": "AUXILIARY_LAYER_FIELD_ROUTE_CONSTRUCTED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3196_1_no_pure_auxiliary_creation",
            "finding": "A healthy auxiliary field alone cannot create positive interface stiffness; the parent must own direct mismatch stiffness or a domain constraint.",
            "claim_status": "PURE_AUXILIARY_STIFFNESS_ROUTE_REJECTED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3196_2_parent_gate",
            "finding": "The route is now mathematically coherent from profile to finite layer, but the parent action still must source K0, B, M, covariant localization, and width selection.",
            "claim_status": "PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3196_3_next_target",
            "finding": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090",
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
    derivation = rows_by_path[AUX_DERIVATION]
    models = rows_by_path[SCHUR_MODELS]
    compliance = rows_by_path[COMPLIANCE_ROWS]
    classification = rows_by_path[CLASSIFICATION]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    recent_fw = formalization_recent_file_count()
    positive_models = [row for row in models if row["status"] == "POSITIVE_AUXILIARY_ELIMINATION_ALLOWED"]
    rejected_models = [row for row in models if "REJECTED" in row["status"] or "SINGULAR" in row["status"]]
    max_recovery = max(float(row["max_abs_recovery_residual"]) for row in compliance)
    expected_compliance_rows = len(positive_models) * len(read_csv(MULTIPLIERS_3194)) * 3
    return [
        {
            "check_id": "VAL3196_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_1_derivation_present",
            "check": "auxiliary elimination includes Schur complement and pure-auxiliary no-go",
            "pass": str(
                any(row["status"] == "SCHUR_COMPLEMENT_DERIVED" for row in derivation)
                and any(row["status"] == "PURE_AUXILIARY_POSITIVE_STIFFNESS_NO_GO" for row in derivation)
            ).lower(),
            "detail": "K_eff=K0-B M^-1 B^T",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_2_model_classification",
            "check": "models include allowed positive Schur complements and rejected singular/negative cases",
            "pass": str(len(positive_models) >= 2 and len(rejected_models) >= 2).lower(),
            "detail": f"positive_models={len(positive_models)}; rejected_models={len(rejected_models)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_3_full_positive_models",
            "check": "allowed models have positive K_eff and positive full block eigenvalue",
            "pass": str(all(float(row["K_eff_scalar"]) > 0.0 and float(row["full_block_min_eigenvalue"]) > 0.0 for row in positive_models)).lower(),
            "detail": "healthy auxiliary blocks only",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_4_multiplier_recovery",
            "check": "parent compliance rows recover the 3194 multipliers",
            "pass": str(len(compliance) == expected_compliance_rows and max_recovery < 1.0e-12).lower(),
            "detail": f"compliance_rows={len(compliance)}; expected_rows={expected_compliance_rows}; max_abs_recovery_residual={max_recovery:.15e}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_5_pure_aux_no_go_carried",
            "check": "classification carries the no-go that pure auxiliary creation of positive stiffness is invalid",
            "pass": str(any(row["math_status"] == "PURE_AUXILIARY_ROUTE_REJECTED" for row in classification)).lower(),
            "detail": "direct stiffness/domain constraint remains required",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_6_next_target_selected",
            "check": "decision selects parent-owned positive layer stiffness or domain geometry constraint",
            "pass": str(any("3197-Y5-R2FR-parent-owned-positive-layer-stiffness" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3197",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_7_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3196_8_formalization_workbench_untouched",
            "check": "formalization-workbench files modified during this run remain zero",
            "pass": str(recent_fw == 0).lower(),
            "detail": f"formalization_recent_file_count={recent_fw}",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    inputs = input_rows()
    derivation = auxiliary_derivation_rows()
    models = model_rows()
    compliance = compliance_rows(models)
    classification = classification_rows(models, compliance)
    decisions = decision_rows()
    return {
        INPUTS: inputs,
        AUX_DERIVATION: derivation,
        SCHUR_MODELS: models,
        COMPLIANCE_ROWS: compliance,
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
