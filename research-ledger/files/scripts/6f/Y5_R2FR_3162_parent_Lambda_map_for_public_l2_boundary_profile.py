from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3162_INPUTS.csv"
MAP_AUDIT = OUT / "P8_Y5_R2FR_3162_PARENT_LAMBDA_MAP_AUDIT.csv"
COEFFICIENT = OUT / "P8_Y5_R2FR_3162_MLAMBDA_COEFFICIENT_CONTRACT.csv"
COUNTERMODELS = OUT / "P8_Y5_R2FR_3162_COUNTERMODEL_GUARDS.csv"
DECISION = OUT / "P8_Y5_R2FR_3162_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3162_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


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
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def bexact_j2_row() -> dict[str, str]:
    for row in read_csv(OUT / "P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv"):
        if row.get("component") == "Earth_J2_full_shell_metric_projection":
            return row
    raise KeyError("missing 3161 Earth_J2_full_shell_metric_projection row")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3161-Y5-R2FR-Bexact-source-bound-or-Wbar-sensitivity-interface-under-AX1090.md", "3161 conditional B_exact interface"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv", "conditional l=2 B_exact rows"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_OUTPUT.csv", "parent boundary primitive status"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3134_QUOTIENT_MAP_ATTEMPT.csv", "candidate q map and boundary_class_obs"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3140_THETA_DESCENT_THEOREM.csv", "strong q-basic action to boundary primitive relation"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3141_TOTAL_ACTION_CONTRACT.csv", "boundary sector total-action contract"),
    ]
    return [
        {
            "input_id": f"IN3162_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def map_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "LM3162_0_public_l2_in_q",
            "clause": "public l=2 metric boundary profile belongs to Q_obs",
            "statement": "q(Phi) includes g_obs and boundary_class_obs, so the public metric l=2 profile has a declared readout slot",
            "status": "declared_not_parent_owned",
            "effect": "profile can be named, but not yet used as parent primitive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_1_boundary_primitive_exists",
            "clause": "parent boundary primitive B_surf=d_S Lambda+h+r exists",
            "statement": "3132 gives the formula shape and weighted-Stokes conditions, but says the parent primitive is not derived",
            "status": "formula_shape_available_not_parent_signed",
            "effect": "Lambda is a valid target object but not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_2_round_sphere_exact_projector",
            "clause": "round S2 l=2 scalar profile has a canonical exact primitive",
            "statement": "for Lambda=A P2, d_S Lambda is exact; l=2 has zero mean and no constant ambiguity after zero-mean gauge",
            "status": "exact_math_pass",
            "effect": "the mathematical exact map is well-defined on the selected first-domain sphere",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_3_no_harmonic_1form_on_S2",
            "clause": "harmonic 1-form mixing is absent on S2",
            "statement": "H^1(S2)=0, so closed 1-form ambiguity does not create an l=2 harmonic 1-form channel",
            "status": "exact_math_pass",
            "effect": "harmonic 1-form leakage is not the obstruction for this first-domain l=2 map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_4_map_scale_coefficient",
            "clause": "parent Lambda equals public l=2 metric profile with fixed scale",
            "statement": "write Lambda_parent = M_Lambda A_public P2; M_Lambda=1 is not signed by current parent action material",
            "status": "coefficient_required_not_signed",
            "effect": "3161 B_exact rows become conditional on |M_Lambda|",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_5_no_residual_mixing",
            "clause": "no residual/counterterm/reference mixing into Lambda",
            "statement": "3132 and 3141 still retain boundary/counterterm/reference ownership gaps",
            "status": "fail_for_claim",
            "effect": "cannot promote public profile -> parent Lambda map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "LM3162_6_physical_not_gauge_guard",
            "clause": "public l=2 metric drift is not quotiented away as pure gauge",
            "statement": "3154 explicitly keeps metric multipole/tide drift physical until separately zeroed or bounded",
            "status": "guard_pass_nonclaim",
            "effect": "the map must bound a physical component, not erase it",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def coefficient_rows(source: dict[str, str]) -> list[dict[str, object]]:
    now = stamp()
    amplitude = float(source["amplitude_A"])
    primitive_norm = float(source["primitive_norm_hat"])
    bexact = float(source["B_exact_L2"])
    cap_lw_l2 = float(source["L_W_phys_cap_l2_C"])
    cap_lw_general = float(source["L_W_phys_cap_general_C"])
    return [
        {
            "contract_id": "MC3162_0_map_definition",
            "quantity": "M_Lambda",
            "definition": "Lambda_parent := M_Lambda A_public P2(cos theta)",
            "value_status": "MISSING_PARENT_MAP_SCALE",
            "formula": "M_Lambda=1 only if the parent boundary primitive is exactly the public metric-component l=2 profile",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MC3162_1_Bexact_with_MLambda",
            "quantity": "B_exact(M_Lambda)",
            "definition": "exact boundary norm as a function of parent map scale",
            "value_status": "conditional_formula_ready",
            "formula": f"B_exact = |M_Lambda| * {fmt(bexact)}",
            "reference_M1_value": fmt(bexact),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MC3162_2_primitive_norm_with_MLambda",
            "quantity": "||Lambda||_hat(M_Lambda)",
            "definition": "normalized primitive norm as a function of parent map scale",
            "value_status": "conditional_formula_ready",
            "formula": f"||Lambda||_hat = |M_Lambda| * {fmt(primitive_norm)}",
            "reference_M1_value": fmt(primitive_norm),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MC3162_3_LWphys_MLambda_cap_l2",
            "quantity": "L_W_phys_times_abs_M_Lambda",
            "definition": "tightest first-domain l=2 product cap after exposing the parent Lambda map scale",
            "value_status": "numeric_cap_ready",
            "formula": f"L_W_phys * |M_Lambda| <= {fmt(cap_lw_l2)}",
            "reference_M1_LWphys_cap": fmt(cap_lw_l2),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MC3162_4_LWphys_MLambda_cap_general",
            "quantity": "L_W_phys_times_abs_M_Lambda_general_Hodge",
            "definition": "same cap using the general S2 zero-mean Hodge constant",
            "value_status": "numeric_cap_ready",
            "formula": f"L_W_phys * |M_Lambda| <= {fmt(cap_lw_general)}",
            "reference_M1_LWphys_cap": fmt(cap_lw_general),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MC3162_5_public_amplitude_reference",
            "quantity": "A_public_J2_full_shell",
            "definition": "public metric-component l=2 full-shell amplitude used in 3161",
            "value_status": "source_domain_value_from_3159",
            "formula": "A_public = projected_B_metric for Earth_J2_full_shell_metric_projection",
            "reference_M1_value": fmt(amplitude),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def countermodel_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "countermodel_id": "CM3162_0_scale_not_one",
            "countermodel": "Lambda_parent = M_Lambda A_public P2 with M_Lambda != 1",
            "damage": "3161 B_exact values are rescaled and M_Lambda must be bounded with L_W_phys",
            "blocked_by": "parent boundary primitive/readout normalization theorem",
            "status": "live_countermodel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "CM3162_1_residual_mixing",
            "countermodel": "Lambda_parent = M_Lambda A_public P2 + Lambda_ref + Lambda_corner + Lambda_residual",
            "damage": "B_exact is not just the source-domain l=2 norm",
            "blocked_by": "boundary class, counterterm, corner and residual silence theorem",
            "status": "live_countermodel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "CM3162_2_readout_only_profile",
            "countermodel": "public l=2 profile is produced by q/readout but is not the parent boundary primitive",
            "damage": "B_exact rows remain smoke/interface rows only",
            "blocked_by": "strong q-basic total action plus owned boundary primitive",
            "status": "live_countermodel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "CM3162_3_illegal_gauge_erasure",
            "countermodel": "public l=2 multipole/tide drift is declared pure gauge",
            "damage": "would delete physical observables and violate 3154 guard",
            "blocked_by": "metric multipole/tide physical-drift guard",
            "status": "forbidden_shortcut",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(source: dict[str, str]) -> list[dict[str, object]]:
    now = stamp()
    cap_lw_l2 = float(source["L_W_phys_cap_l2_C"])
    return [
        {
            "decision_id": "D3162_0_map_verdict",
            "decision": "the round-sphere l=2 exact projection is mathematically clean, but parent M_Lambda=1 is not signed",
            "evidence": "exact S2 identities pass; parent boundary primitive and residual silence fail for claim",
            "effect": "3161 values become M_Lambda-scaled interface rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3162_1_new_gate",
            "decision": "replace the unsigned map with the product gate L_W_phys |M_Lambda|",
            "evidence": f"L_W_phys |M_Lambda| <= {fmt(cap_lw_l2)} for Earth J2 full-shell l=2",
            "effect": "the local branch now needs either M_Lambda=1 theorem, a direct M_Lambda bound, or a combined Wbar sensitivity bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3162_2_next_attack",
            "decision": "derive M_Lambda from the strong q-basic boundary primitive before estimating Wbar sensitivity",
            "evidence": "M_Lambda is upstream of B_exact and closer to the parent-action boundary map",
            "effect": "if M_Lambda closes, L_W_phys is the last local product factor; if not, closure parameter remains explicit",
            "next_action": "3163-Y5-R2FR-MLambda-scale-from-qbasic-boundary-primitive-or-closure-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    audit: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    exact_pass = any(row["status"] == "exact_math_pass" for row in audit)
    fail_for_claim = any(row["status"] == "fail_for_claim" for row in audit)
    coeff_formulas_ok = all(
        row["value_status"] != "numeric_cap_ready" or "<=" in str(row["formula"])
        for row in coefficients
    )
    mlambda_missing = any(row["quantity"] == "M_Lambda" and row["value_status"] == "MISSING_PARENT_MAP_SCALE" for row in coefficients)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, audit, coefficients, countermodels, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3162_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3162_1_exact_math_and_claim_block_present",
            "status": "pass" if exact_pass and fail_for_claim else "fail",
            "detail": "requires at least one exact math pass and at least one fail_for_claim parent clause",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3162_2_coefficient_contract_ready",
            "status": "pass" if coeff_formulas_ok and mlambda_missing else "fail",
            "detail": "M_Lambda is explicit and product caps are formulas, not claims",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3162_3_countermodels_retained",
            "status": "pass" if len(countermodels) >= 3 else "fail",
            "detail": "scale, residual, and readout-only countermodels retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3162_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3162 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    source = bexact_j2_row()
    inputs = input_rows()
    audit = map_audit_rows()
    coefficients = coefficient_rows(source)
    countermodels = countermodel_rows()
    decisions = decision_rows(source)
    validations = validation_rows(inputs, audit, coefficients, countermodels, decisions)
    write_csv(INPUTS, inputs)
    write_csv(MAP_AUDIT, audit)
    write_csv(COEFFICIENT, coefficients)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3162 validation failed: {failures}")


if __name__ == "__main__":
    main()
