from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3161_INPUTS.csv"
IDENTITIES = OUT / "P8_Y5_R2FR_3161_L2_MODE_IDENTITIES.csv"
BEXACT = OUT / "P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv"
GATES = OUT / "P8_Y5_R2FR_3161_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_R2FR_3161_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3161_VALIDATION.csv"


L_MODE = 2
INT_P2_SQUARED = 4.0 * math.pi / 5.0
INT_GRAD_P2_SQUARED = L_MODE * (L_MODE + 1.0) * INT_P2_SQUARED
C_HODGE_GENERAL = 1.0 / math.sqrt(2.0)
C_HODGE_L2 = 1.0 / math.sqrt(6.0)


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


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3160-Y5-R2FR-LWphysLambda-parent-product-bound-or-zero-theorem-under-AX1090.md", "3160 Hodge/product contract"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3160_PRODUCT_CLOSURE_CONTRACT.csv", "direct and factorized product caps"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3160_HODGE_SPHERE_PRODUCT_BOUND.csv", "round-sphere Hodge constant"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv", "metric l=2 source amplitudes and reverse caps"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3158_SOURCE_VALUES.csv", "source provenance for Earth/tide rows"),
    ]
    return [
        {
            "input_id": f"IN3161_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def numeric_rows_3159() -> list[dict[str, str]]:
    return read_csv(OUT / "P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv")


def selected_components() -> list[dict[str, str]]:
    wanted = {
        "Earth_J2_full_shell_metric_projection",
        "Sun_plus_Moon_tide_metric_projection",
        "Moon_tide_metric_projection",
        "Sun_tide_metric_projection",
    }
    return [row for row in numeric_rows_3159() if row.get("component") in wanted]


def identity_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "identity_id": "ID3161_0_P2_L2_norm",
            "object": "P2(cos theta)",
            "formula": "integral_S2 P2^2 dOmega = 4*pi/5",
            "numeric_value": fmt(INT_P2_SQUARED),
            "units": "dimensionless",
            "status": "exact_identity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID3161_1_grad_P2_L2_norm",
            "object": "angular_gradient_P2",
            "formula": "integral_S2 |grad_Omega P2|^2 dOmega = l(l+1) 4*pi/(2l+1) with l=2",
            "numeric_value": fmt(INT_GRAD_P2_SQUARED),
            "units": "dimensionless",
            "status": "exact_identity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID3161_2_l2_mode_hodge_constant",
            "object": "C_Hodge_l2",
            "formula": "||Lambda_l2||_L2/R = (1/sqrt(6)) ||d_S Lambda_l2||_L2",
            "numeric_value": fmt(C_HODGE_L2),
            "units": "dimensionless",
            "status": "exact_l2_mode_constant",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID3161_3_general_zero_mean_hodge_constant",
            "object": "C_Hodge_general",
            "formula": "||Lambda||_L2/R <= (1/sqrt(2)) ||d_S Lambda||_L2 on S2_R",
            "numeric_value": fmt(C_HODGE_GENERAL),
            "units": "dimensionless",
            "status": "3160_general_constant_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bexact_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source in selected_components():
        amplitude = float(source["projected_B_metric"])
        reverse_cap = float(source["single_cap_required_LWlambda"])
        primitive_norm_hat = amplitude * math.sqrt(INT_P2_SQUARED)
        b_exact = amplitude * math.sqrt(INT_GRAD_P2_SQUARED)
        general_lw_cap = reverse_cap / (C_HODGE_GENERAL * b_exact)
        l2_lw_cap = reverse_cap / (C_HODGE_L2 * b_exact)
        rows.append(
            {
                "bexact_id": f"BE3161_{len(rows)}",
                "component": source["component"],
                "assumed_boundary_profile": "Lambda(theta)=A P2(cos theta) in public metric-component l=2 profile",
                "amplitude_A": fmt(amplitude),
                "primitive_norm_hat": fmt(primitive_norm_hat),
                "B_exact_L2": fmt(b_exact),
                "C_Hodge_general": fmt(C_HODGE_GENERAL),
                "C_Hodge_l2_mode": fmt(C_HODGE_L2),
                "L_W_phys_cap_general_C": fmt(general_lw_cap),
                "L_W_phys_cap_l2_C": fmt(l2_lw_cap),
                "source_reverse_cap_LWphysLambda": fmt(reverse_cap),
                "formula": "B_exact=|A| sqrt(24*pi/5); ||Lambda||_hat=|A| sqrt(4*pi/5)",
                "parent_map_status": "conditional_public_metric_profile_to_parent_Lambda_map_not_signed",
                "status": "B_exact_source_domain_bound_ready_nonclaim",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    rows.sort(key=lambda row: float(str(row["L_W_phys_cap_l2_C"])))
    for index, row in enumerate(rows):
        row["bexact_id"] = f"BE3161_{index}"
    return rows


def gate_rows(bexact: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    tightest = bexact[0]
    return [
        {
            "gate_id": "G3161_0_l2_identities",
            "gate": "P2 L2 and angular-gradient identities",
            "status": "pass_nonclaim",
            "detail": "integral P2^2=4pi/5 and integral |grad P2|^2=24pi/5",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3161_1_Bexact_numeric",
            "gate": "first-domain B_exact numeric rows",
            "status": "pass_nonclaim",
            "detail": f"tightest row {tightest['component']} has B_exact={tightest['B_exact_L2']}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3161_2_parent_Lambda_map",
            "gate": "public l=2 metric profile equals parent exact primitive",
            "status": "fail_for_claim",
            "detail": "the source-domain B_exact rows are conditional until the MTS parent boundary map identifies Lambda with the public l=2 boundary profile",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3161_3_Wbar_sensitivity",
            "gate": "L_W_phys parent sensitivity",
            "status": "fail_for_claim",
            "detail": "numeric L_W_phys cap is now available, but L_W_phys itself is not derived or sourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(bexact: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    tightest = bexact[0]
    return [
        {
            "decision_id": "D3161_0_Bexact_result",
            "decision": "B_exact is no longer pure fog for the first l=2 public metric boundary profile",
            "evidence": f"{tightest['component']} tightest row has B_exact={tightest['B_exact_L2']}",
            "effect": "the remaining local product obstruction moves to the parent Lambda map and Wbar sensitivity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3161_1_LWphys_cap",
            "decision": "using the l=2 mode Hodge constant, the tightest source-domain cap is on L_W_phys itself",
            "evidence": f"L_W_phys <= {tightest['L_W_phys_cap_l2_C']} for {tightest['component']}",
            "effect": "not numerically fatal, but still not derivable without Wbar",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3161_2_next_attack",
            "decision": "derive the public l=2 metric profile to parent Lambda map before trying to estimate Wbar sensitivity",
            "evidence": "G3161_2_parent_Lambda_map fail_for_claim",
            "effect": "if the map fails, B_exact rows remain source-domain smoke only; if it passes, L_W_phys becomes the last local product factor",
            "next_action": "3162-Y5-R2FR-parent-Lambda-map-for-public-l2-boundary-profile-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    identities: list[dict[str, object]],
    bexact: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    identity_map = {row["identity_id"]: float(str(row["numeric_value"])) for row in identities}
    identities_ok = (
        math.isclose(identity_map["ID3161_0_P2_L2_norm"], 4.0 * math.pi / 5.0, rel_tol=1e-12)
        and math.isclose(identity_map["ID3161_1_grad_P2_L2_norm"], 24.0 * math.pi / 5.0, rel_tol=1e-12)
        and math.isclose(identity_map["ID3161_2_l2_mode_hodge_constant"], 1.0 / math.sqrt(6.0), rel_tol=1e-12)
    )
    bexact_ok = True
    mode_relation_ok = True
    for row in bexact:
        amplitude = float(str(row["amplitude_A"]))
        primitive = float(str(row["primitive_norm_hat"]))
        b_exact = float(str(row["B_exact_L2"]))
        if amplitude <= 0.0 or primitive <= 0.0 or b_exact <= 0.0:
            bexact_ok = False
        if not math.isclose(C_HODGE_L2 * b_exact, primitive, rel_tol=1e-12):
            mode_relation_ok = False
    tightest_ok = bexact[0]["component"] == "Earth_J2_full_shell_metric_projection"
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, identities, bexact, gates, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3161_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3161_1_l2_identities",
            "status": "pass" if identities_ok else "fail",
            "detail": "P2 norms and C_Hodge_l2 identities match analytic values",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3161_2_Bexact_positive",
            "status": "pass" if bexact_ok else "fail",
            "detail": "all amplitudes, primitive norms, and B_exact rows are positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3161_3_mode_relation",
            "status": "pass" if mode_relation_ok else "fail",
            "detail": "C_Hodge_l2 * B_exact equals primitive_norm_hat for every l=2 row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3161_4_tightest_row_expected",
            "status": "pass" if tightest_ok else "fail",
            "detail": str(bexact[0]["component"]),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3161_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3161 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    identities = identity_rows()
    bexact = bexact_rows()
    gates = gate_rows(bexact)
    decisions = decision_rows(bexact)
    validations = validation_rows(inputs, identities, bexact, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(IDENTITIES, identities)
    write_csv(BEXACT, bexact)
    write_csv(GATES, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3161 validation failed: {failures}")


if __name__ == "__main__":
    main()
