from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3172_INPUTS.csv"
GREEN = OUT / "P8_Y5_R2FR_3172_GREEN_OWNER_ATTEMPT.csv"
CHANNEL = OUT / "P8_Y5_R2FR_3172_CHANNEL_STATUS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3172_CLOSURE_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3172_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3172_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def csv_value(path: Path, key: str, value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == value:
            return row[column]
    raise KeyError(f"missing {key}={value} in {path}")


def values() -> dict[str, float]:
    corrected_half = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "bound_id",
            "CJ3170_2_Rozelot_half_range_proxy",
            "K2_corrected_surface_bound",
        )
    )
    c_k2_unit = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv",
            "unit_id",
            "KU3165_0_definition",
            "value",
        )
    )
    return {"corrected_half": corrected_half, "c_k2_unit": c_k2_unit}


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3171-Y5-R2FR-K2-radial-profile-owner-or-J2-transfer-demotion-under-AX1090.md", "3171 Upsilon_J2 nonidentifiability handoff"),
        ("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "public weak-field J2 metric convention"),
        ("3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "K2 residual-vector definition"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv", "3171 Upsilon_J2 owner-clause contract"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv", "3171 missing profile/projection audit"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv", "3170 corrected surface pressure bounds"),
        ("000-private-fork-heuristics-for-martin-style-search.md", "private fork discipline for not rejecting time/flow branches on wording alone"),
    ]
    return [
        {
            "input_id": f"IN3172_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def green_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "attempt_id": "GO3172_0_public_exterior_equation",
            "object": "public_exterior_l2_metric_potential",
            "derivation": "Assume the exterior public weak-field quadrupole channel obeys source-free Laplace equation outside the source body.",
            "formula": "nabla^2[f_l(r) P_l(cos theta)] = 0",
            "result": "this is a public GR/Newton Green statement, not yet an MTS parent-coupling proof",
            "status": "conditional_public_math_start",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "GO3172_1_radial_ode",
            "object": "radial_l_mode",
            "derivation": "Separation of variables gives the exterior radial equation for each spherical harmonic mode.",
            "formula": "r^2 f_l'' + 2 r f_l' - l(l+1) f_l = 0",
            "result": "Euler equation with powers r^l and r^(-l-1)",
            "status": "derived_public_green_radial_ode",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "GO3172_2_l2_solution",
            "object": "l_equals_2_profile",
            "derivation": "For l=2, the two source-free exterior powers are the growing and decaying quadrupole branches.",
            "formula": "f_2(r)=a r^2 + b r^-3",
            "result": "asymptotic flatness removes a r^2 for isolated solar-system exterior fields",
            "status": "derived_public_r_minus_3_profile",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "GO3172_3_surface_to_radius_rule",
            "object": "public_metric_amplitude_transport",
            "derivation": "If A_surface is the public l=2 metric amplitude at R_s, then the decaying exterior amplitude at r is fixed.",
            "formula": "A_metric(r)=A_surface*(R_s/r)^3",
            "result": "the public radial Green profile owner is available after the metric amplitude is already owned",
            "status": "conditional_profile_transport_closed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "GO3172_4_public_metric_factor",
            "object": "J2_metric_convention",
            "derivation": "Using the 3159 convention, public solar J2 maps to metric amplitude through the weak-field factor.",
            "formula": "A_metric(r)=2 epsilon_sun_surface J2 (R_s/r)^3",
            "result": "J2_eff=A_surface/(2 epsilon_sun_surface) at rho=1 once A_surface is owned",
            "status": "conditional_public_metric_map_closed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "attempt_id": "GO3172_5_parent_operator_gap",
            "object": "MTS_K2_to_public_Laplace_channel",
            "derivation": "The missing step is proving that K2*C_K2_unit enters the same exterior public l=2 metric channel governed by the Laplace/linearized-Einstein operator.",
            "formula": "K2*C_K2_unit --Pi_J2_metric*T_source--> A_surface",
            "result": "the public r^-3 theorem does not by itself derive Pi_J2_metric, T_source, or Upsilon_J2",
            "status": "MISSING_PARENT_OPERATOR_AND_PROJECTION_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def channel_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "channel_id": "CS3172_0_public_radial_profile",
            "clause": "exterior r^-3 radial Green profile",
            "status": "conditional_math_pass",
            "owned_by": "public source-free Laplace/weak-field GR exterior theorem",
            "missing_before_claim": "parent proof that MTS K2 inhabits this public channel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CS3172_1_parent_operator_match",
            "clause": "parent exterior operator reduces to public source-free l=2 Laplace channel",
            "status": "missing_parent_derivation",
            "owned_by": "not_owned",
            "missing_before_claim": "linearized parent field equation and projection onto the public metric quadrupole",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CS3172_2_metric_projection",
            "clause": "Pi_J2_metric maps K2 residual into public metric amplitude",
            "status": "missing_projection_kernel",
            "owned_by": "not_owned",
            "missing_before_claim": "explicit Pi_J2_metric row from parent variables to metric perturbation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CS3172_3_source_domain_transfer",
            "clause": "Earth/local K2 lane transfers to solar exterior source domain",
            "status": "missing_source_transfer",
            "owned_by": "not_owned",
            "missing_before_claim": "solar-source construction or universality theorem for K2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CS3172_4_Upsilon_J2",
            "clause": "Upsilon_J2 numeric/symbolic owner",
            "status": "missing_composite_transfer",
            "owned_by": "not_owned",
            "missing_before_claim": "Pi_J2_metric * T_source * G_ext_l2_surface with source-backed normalization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CS3172_5_direct_J2_scoring",
            "clause": "score K2 directly against solar J2/PPN bounds",
            "status": "blocked",
            "owned_by": "no_direct_owner",
            "missing_before_claim": "all channel clauses CS3172_1 through CS3172_4",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "CL3172_0_Upsilon_decomposition",
            "quantity": "Upsilon_J2",
            "contract": "minimal composite transfer from internal K2 residual to solar-surface public metric amplitude",
            "formula": "Upsilon_J2 = Pi_J2_metric * T_source * G_ext_l2_surface",
            "current_value": "MISSING_Pi_J2_metric_AND_T_source",
            "claim_status": "not_claimable",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CL3172_1_Green_factor",
            "quantity": "G_ext_l2_surface",
            "contract": "public exterior radial transport for an already-owned l=2 surface metric amplitude",
            "formula": "A_metric(r)=A_surface*(R_s/r)^3; if evaluated at R_s then G_ext_l2_surface=1",
            "current_value": "conditional_math_owned_only_after_A_surface_exists",
            "claim_status": "conditional_not_sufficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CL3172_2_K2_pressure_bound",
            "quantity": "K2_bound_half_range",
            "contract": "3171/3170 pressure row with explicit composite transfer kernel",
            "formula": f"K2 <= {fmt(v['corrected_half'])}/|Pi_J2_metric*T_source*G_ext_l2_surface|",
            "current_value": "not_scoreable_until_composite_transfer_exists",
            "claim_status": "conditional_pressure_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CL3172_3_no_smuggling_rule",
            "quantity": "J2_channel_claim_guardrail",
            "contract": "Do not set Pi_J2_metric=1 or T_source=1 by convention; those are parent-owned transfer claims.",
            "formula": "A_surface != K2*C_K2_unit unless Pi_J2_metric*T_source*G_ext_l2_surface is derived or sourced",
            "current_value": "guardrail_active",
            "claim_status": "blocks_direct_J2_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3172_0_public_Green_profile_result",
            "decision": "the exterior r^-3 profile is derivable in the public weak-field channel",
            "evidence": "GO3172_1 through GO3172_3",
            "effect": "one owner clause is now mathematically sharp, but only conditionally",
            "next_action": "use the r^-3 theorem only after the parent K2-to-public-metric channel is signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3172_1_J2_channel_status",
            "decision": "the J2 channel remains transfer-only, not claim-grade",
            "evidence": "CS3172_1 through CS3172_4 remain missing",
            "effect": "no local-GR, PPN, Shapiro, clock, orbital, or R10 pass can be claimed from J2 rows",
            "next_action": "derive the parent exterior operator match or produce a source-backed Pi_J2_metric/T_source row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3172_2_next_derivation_target",
            "decision": "the next target should attack the parent coupling/projection, not another bound table",
            "evidence": "the public Green factor is not the bottleneck anymore; Pi_J2_metric and T_source are",
            "effect": "3173 should try parent exterior operator match first, then source row fallback",
            "next_action": "3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    green: list[dict[str, object]],
    channels: list[dict[str, object]],
    contracts: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    r_minus_3 = any(row["status"] == "derived_public_r_minus_3_profile" for row in green)
    parent_gap = any("PARENT_OPERATOR" in row["status"] for row in green)
    composite_missing = any(row["quantity"] == "Upsilon_J2" and "MISSING" in row["current_value"] for row in contracts)
    direct_blocked = any(row["channel_id"] == "CS3172_5_direct_J2_scoring" and row["status"] == "blocked" for row in channels)
    next_target = any("3173" in row["next_action"] for row in decisions)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, green, channels, contracts, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3172_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_1_public_r_minus_3_profile_derived",
            "status": "pass" if r_minus_3 else "fail",
            "detail": "public l=2 exterior decaying branch is r^-3 after asymptotic flatness",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_2_parent_operator_gap_preserved",
            "status": "pass" if parent_gap else "fail",
            "detail": "script refuses to identify K2*C_K2_unit with public metric amplitude",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_3_Upsilon_still_missing",
            "status": "pass" if composite_missing else "fail",
            "detail": "Upsilon_J2 requires Pi_J2_metric and T_source",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_4_direct_J2_scoring_blocked",
            "status": "pass" if direct_blocked else "fail",
            "detail": "direct solar J2/PPN scoring remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_5_next_target_selected",
            "status": "pass" if next_target else "fail",
            "detail": "3173 parent exterior operator/projection target selected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3172_6_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3172 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    green = green_rows()
    channels = channel_rows()
    contracts = contract_rows(v)
    decisions = decision_rows()
    validations = validation_rows(inputs, green, channels, contracts, decisions)
    write_csv(INPUTS, inputs)
    write_csv(GREEN, green)
    write_csv(CHANNEL, channels)
    write_csv(CONTRACT, contracts)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3172 validation failed: {failures}")


if __name__ == "__main__":
    main()
