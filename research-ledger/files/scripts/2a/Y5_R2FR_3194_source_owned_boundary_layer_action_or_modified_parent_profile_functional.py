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

INPUTS = OUT / "P8_Y5_R2FR_3194_INPUTS.csv"
ACTION_REGISTER = OUT / "P8_Y5_R2FR_3194_BOUNDARY_ACTION_CANDIDATE_REGISTER.csv"
GLUING_DERIVATION = OUT / "P8_Y5_R2FR_3194_C1_GLUING_MULTIPLIER_DERIVATION.csv"
MULTIPLIERS = OUT / "P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv"
CLASSIFICATION = OUT / "P8_Y5_R2FR_3194_CLOSURE_CLASSIFICATION.csv"
DECISION = OUT / "P8_Y5_R2FR_3194_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3194_VALIDATION.csv"

SELECTION_3193 = OUT / "P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_SELECTION.csv"
LAYER_3193 = OUT / "P8_Y5_R2FR_3193_REQUIRED_BOUNDARY_LAYER_COUNTERMOMENTA.csv"
VALIDATION_3193 = OUT / "P8_Y5_R2FR_3193_VALIDATION.csv"


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
            "3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090.md",
            "3193 interface no-go and required counter-momenta",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3193_INTERFACE_CONDITION_DERIVATION.csv",
            "3193 Pi_1/Pi_0 natural interface conditions",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_SELECTION.csv",
            "3193 boundary momentum selection rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3193_REQUIRED_BOUNDARY_LAYER_COUNTERMOMENTA.csv",
            "3193 required counter-momenta rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3193_VALIDATION.csv",
            "3193 validation evidence",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "current parent equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3194_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def action_register_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "candidate_id": "ACT3194_0_linear_counterterm",
            "candidate": "localized linear boundary counterterm",
            "action": "S_bl=sum_i(tau_i z_i) with z_i in {F,F'} at each interface",
            "variation_result": "deltaS_bl=sum_i tau_i delta z_i, so any required counter-momentum can be supplied",
            "strength": "mathematically integrable at a point",
            "failure_or_gate": "tau_i are arbitrary unless sourced by parent geometry or edge matter",
            "status": "WORKS_BUT_CLOSURE_ONLY",
        },
        {
            "candidate_id": "ACT3194_1_quadratic_mismatch_penalty",
            "candidate": "quadratic penalty on C1 mismatch",
            "action": "S_bl=(1/2)k0[F]^2+(1/2)k1[F']^2+k01[F][F']",
            "variation_result": "gradient is proportional to [F] and [F']",
            "strength": "source-neutral and common in interface matching",
            "failure_or_gate": "the 3192 branch already enforces [F]=0 and [F']=0, so this gives zero counter-momentum and cannot cancel the 3193 Pi jumps",
            "status": "FAILS_FOR_C1_MATCHED_BRANCH",
        },
        {
            "candidate_id": "ACT3194_2_C1_gluing_multiplier",
            "candidate": "C1 gluing multiplier action",
            "action": "S_glue=sum_interfaces(lambda_0[F]+lambda_1[F'])",
            "variation_result": "variation in lambda enforces C1 continuity; variation in boundary fields supplies reaction momenta lambda_i=-[Pi_i]",
            "strength": "multipliers are solved by the variational stationarity equations, not picked as fixed numbers",
            "failure_or_gate": "parent must justify constrained gluing or derive lambda_i as a finite boundary-layer stress before public local-GR claims",
            "status": "CONDITIONALLY_CLOSES_INTERFACE_EQUATIONS",
        },
        {
            "candidate_id": "ACT3194_3_modified_bulk_functional",
            "candidate": "modify the parent bulk profile functional",
            "action": "replace J=int x^4(D2F)^2 dx by a parent-derived functional whose natural boundary momenta match core and exterior without edge multipliers",
            "variation_result": "would change both interior EL equation and interface momenta",
            "strength": "cleanest if derivable from parent field theory",
            "failure_or_gate": "no parent-owned modified bulk density has yet been derived",
            "status": "OPEN_PARENT_DERIVATION_ROUTE",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def gluing_derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "derivation_id": "GLUE3194_0_boundary_variables",
            "statement": "Use z_0=F and z_1=F' as the C1 variables at each interface.",
            "formula": "z=(F,F')",
            "status": "DEFINED",
        },
        {
            "derivation_id": "GLUE3194_1_jump_constraints",
            "statement": "Impose C1 continuity as variational constraints rather than fixed external patching.",
            "formula": "[F]=0 and [F']=0",
            "status": "DEFINED",
        },
        {
            "derivation_id": "GLUE3194_2_gluing_action",
            "statement": "Add Lagrange multipliers for the C1 constraints at each interface.",
            "formula": "S_glue=sum_interfaces(lambda_0[F]+lambda_1[F'])",
            "status": "ACTION_CANDIDATE",
        },
        {
            "derivation_id": "GLUE3194_3_constraint_variation",
            "statement": "Varying lambda enforces the C1 constraints exactly.",
            "formula": "delta_lambda S_glue=0 -> [F]=0, [F']=0",
            "status": "DERIVED",
        },
        {
            "derivation_id": "GLUE3194_4_boundary_field_variation",
            "statement": "Varying the boundary fields gives force-balance between bulk momenta and multiplier reaction forces.",
            "formula": "[Pi_0]+lambda_0=0 and [Pi_1]+lambda_1=0",
            "status": "DERIVED",
        },
        {
            "derivation_id": "GLUE3194_5_multiplier_solution",
            "statement": "The multiplier values are fixed by the already-derived 3193 momentum jumps.",
            "formula": "lambda_i=-[Pi_i]",
            "status": "SOLVED_BY_STATIONARITY",
        },
        {
            "derivation_id": "GLUE3194_6_parent_gate",
            "statement": "This closes the interface equations only if the parent theory permits constrained gluing domains or derives these multipliers as finite edge stress.",
            "formula": "parent signature required: S_parent -> S_bulk + S_glue or finite-layer limit",
            "status": "PARENT_SIGNATURE_REQUIRED",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def multiplier_solution_rows() -> list[dict[str, object]]:
    now = stamp()
    selections = {row["selection_id"]: row for row in read_csv(SELECTION_3193)}
    layers = read_csv(LAYER_3193)
    rows: list[dict[str, object]] = []
    for layer in layers:
        selection_id = layer["source_selection"]
        selection = selections[selection_id]
        pairs = [
            ("left_Pi1", "left_jump_Pi1", "required_tau_left_Pi1"),
            ("left_Pi0", "left_jump_Pi0", "required_tau_left_Pi0"),
            ("right_Pi1", "right_jump_Pi1", "required_tau_right_Pi1"),
            ("right_Pi0", "right_jump_Pi0", "required_tau_right_Pi0"),
        ]
        residuals = {
            name: float(selection[jump_key]) + float(layer[tau_key])
            for name, jump_key, tau_key in pairs
        }
        max_abs_residual = max(abs(value) for value in residuals.values())
        tau_norm = math.sqrt(
            sum(float(layer[tau_key]) ** 2 for _, _, tau_key in pairs)
        )
        rows.append(
            {
                "solution_id": layer["layer_id"].replace("BL3193", "GLUE3194"),
                "source_selection": selection_id,
                "transition_width": layer["transition_width"],
                "N4_D2": selection["N4_D2"],
                "lambda_left_Pi1": layer["required_tau_left_Pi1"],
                "lambda_left_Pi0": layer["required_tau_left_Pi0"],
                "lambda_right_Pi1": layer["required_tau_right_Pi1"],
                "lambda_right_Pi0": layer["required_tau_right_Pi0"],
                "lambda_norm": f"{tau_norm:.15e}",
                "cancellation_residual_left_Pi1": f"{residuals['left_Pi1']:.15e}",
                "cancellation_residual_left_Pi0": f"{residuals['left_Pi0']:.15e}",
                "cancellation_residual_right_Pi1": f"{residuals['right_Pi1']:.15e}",
                "cancellation_residual_right_Pi0": f"{residuals['right_Pi0']:.15e}",
                "max_abs_cancellation_residual": f"{max_abs_residual:.15e}",
                "continuity_residual_F": "0.000000000000000e+00",
                "continuity_residual_Fprime": "0.000000000000000e+00",
                "closure_status": "INTERFACE_EQUATIONS_CLOSE_IF_GLUING_MULTIPLIERS_PARENT_ALLOWED",
                "source_status": "MULTIPLIERS_SOLVED_NOT_PARENT_SIGNED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def classification_rows(multiplier_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    reference = next(row for row in multiplier_rows if row["source_selection"] == "SEL3193_0_3190_width")
    balanced = next(row for row in multiplier_rows if row["source_selection"] == "SEL3193_1_balanced_Fpp_jump")
    minimum = min(multiplier_rows, key=lambda row: float(row["lambda_norm"]))
    return [
        {
            "classification_id": "CLASS3194_0_arbitrary_counterterm",
            "finding": "A linear boundary counterterm can always be written, but it is just the 3193 tau ledger repackaged as an action.",
            "mathematical_status": "INTEGRABLE",
            "physics_status": "CLOSURE_ONLY",
            "next_requirement": "derive tau coefficients from parent geometry, finite layer, or source charges",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3194_1_quadratic_penalty",
            "finding": "A source-neutral quadratic penalty on [F] and [F'] cannot supply the needed momentum because the exact branch already has [F]=[F']=0.",
            "mathematical_status": "FAILS_ON_C1_MATCHED_BRANCH",
            "physics_status": "REJECTED_AS_INTERFACE_FIX",
            "next_requirement": "use multipliers, curvature-dependent edge terms, or a modified bulk functional",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3194_2_gluing_multiplier",
            "finding": f"C1 gluing multipliers cancel the 3193 jumps exactly; reference-width multiplier norm is {reference['lambda_norm']}.",
            "mathematical_status": "CLOSES_INTERFACE_EQUATIONS",
            "physics_status": "PARENT_SIGNATURE_REQUIRED",
            "next_requirement": "prove the parent action produces constrained gluing domains or finite edge stresses",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3194_3_balanced_candidate",
            "finding": f"The balanced curvature row closes with multiplier norm {balanced['lambda_norm']} and keeps N4_D2={balanced['N4_D2']}.",
            "mathematical_status": "CLOSES_IF_GLUING_ALLOWED",
            "physics_status": "WIDTH_SELECTION_NOT_PARENT_DERIVED",
            "next_requirement": "derive width/profile selection rather than choosing by balancing heuristic",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "classification_id": "CLASS3194_4_minimum_multiplier_candidate",
            "finding": f"The smallest multiplier norm among generated rows is {minimum['lambda_norm']} at width {minimum['transition_width']}, but this inherits the 3193 scan-edge/curvature-jump issue.",
            "mathematical_status": "LOWER_EDGE_FORCE_BUT_NOT_CLEAN",
            "physics_status": "NOT_A_DERIVED_SELECTION",
            "next_requirement": "derive layer energy/regularity weights if width is to be selected variationally",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3194_0_not_arbitrary_tau_only",
            "finding": "3194 upgrades the 3193 tau ledger into an explicit variational gluing mechanism: lambda_i=-[Pi_i].",
            "claim_status": "ACTION_MECHANISM_CONSTRUCTED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3194_1_quadratic_penalty_rejected",
            "finding": "A simple quadratic continuity penalty cannot help because the profile is already C1-matched; its gradient vanishes where the counter-momentum must be nonzero.",
            "claim_status": "SOURCE_NEUTRAL_PENALTY_ROUTE_REJECTED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3194_2_gluing_is_best_current_route",
            "finding": "The C1 gluing multiplier action is the least-smuggled current route: it derives the needed counter-momenta as reaction forces, but still needs a parent origin.",
            "claim_status": "BEST_ROUTE_PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3194_3_local_GR_status",
            "finding": "Local-GR/PPN claims remain blocked until the parent action justifies gluing multipliers or replaces the toy bulk functional with a naturally matched one.",
            "claim_status": "LOCAL_GR_STILL_BLOCKED_BUT_NARROWER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3194_4_next_target",
            "finding": "3195-Y5-R2FR-gluing-multiplier-parent-origin-or-finite-layer-limit-under-AX1090",
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
    actions = rows_by_path[ACTION_REGISTER]
    derivation = rows_by_path[GLUING_DERIVATION]
    multipliers = rows_by_path[MULTIPLIERS]
    classification = rows_by_path[CLASSIFICATION]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    recent_fw = formalization_recent_file_count()
    max_cancellation = max(float(row["max_abs_cancellation_residual"]) for row in multipliers)
    return [
        {
            "check_id": "VAL3194_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_1_action_candidates_present",
            "check": "linear, quadratic, gluing, and modified-bulk candidates are registered",
            "pass": str({row["candidate_id"] for row in actions} == {"ACT3194_0_linear_counterterm", "ACT3194_1_quadratic_mismatch_penalty", "ACT3194_2_C1_gluing_multiplier", "ACT3194_3_modified_bulk_functional"}).lower(),
            "detail": f"action_rows={len(actions)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_2_gluing_derivation_present",
            "check": "gluing derivation includes constraints, multiplier action, and lambda solution",
            "pass": str(
                any(row["status"] == "ACTION_CANDIDATE" for row in derivation)
                and any(row["status"] == "SOLVED_BY_STATIONARITY" for row in derivation)
                and any(row["status"] == "PARENT_SIGNATURE_REQUIRED" for row in derivation)
            ).lower(),
            "detail": "S_glue=sum(lambda_0[F]+lambda_1[F'])",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_3_multiplier_cancellation",
            "check": "all generated multipliers cancel the 3193 momentum jumps numerically",
            "pass": str(max_cancellation < 1.0e-12).lower(),
            "detail": f"max_abs_cancellation_residual={max_cancellation:.15e}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_4_multiplier_rows_nonclaim",
            "check": "multiplier rows are generated for the three 3193 boundary-layer rows and remain nonclaim",
            "pass": str(len(multipliers) == 3 and all(row["source_status"] == "MULTIPLIERS_SOLVED_NOT_PARENT_SIGNED" for row in multipliers)).lower(),
            "detail": f"multiplier_rows={len(multipliers)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_5_quadratic_penalty_rejected",
            "check": "classification rejects source-neutral quadratic penalty for the C1 matched branch",
            "pass": str(any(row["mathematical_status"] == "FAILS_ON_C1_MATCHED_BRANCH" for row in classification)).lower(),
            "detail": "zero continuity residual gives zero penalty gradient",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_6_next_target_selected",
            "check": "decision selects parent origin or finite layer limit for gluing multipliers",
            "pass": str(any("3195-Y5-R2FR-gluing-multiplier-parent-origin" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3195",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_7_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3194_8_formalization_workbench_untouched",
            "check": "formalization-workbench files modified during this run remain zero",
            "pass": str(recent_fw == 0).lower(),
            "detail": f"formalization_recent_file_count={recent_fw}",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    inputs = input_rows()
    actions = action_register_rows()
    derivation = gluing_derivation_rows()
    multipliers = multiplier_solution_rows()
    classification = classification_rows(multipliers)
    decisions = decision_rows()
    return {
        INPUTS: inputs,
        ACTION_REGISTER: actions,
        GLUING_DERIVATION: derivation,
        MULTIPLIERS: multipliers,
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
