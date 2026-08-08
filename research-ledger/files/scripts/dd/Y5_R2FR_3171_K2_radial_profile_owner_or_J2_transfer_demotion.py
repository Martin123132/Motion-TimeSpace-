from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3171_INPUTS.csv"
AUDIT = OUT / "P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv"
NONIDENTIFIABILITY = OUT / "P8_Y5_R2FR_3171_PROFILE_NONIDENTIFIABILITY_PROOF.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv"
DEMOTION = OUT / "P8_Y5_R2FR_3171_J2_SCORING_DEMOTION.csv"
DECISION = OUT / "P8_Y5_R2FR_3171_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3171_VALIDATION.csv"


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
    c_k2_unit = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv",
            "unit_id",
            "KU3165_0_definition",
            "value",
        )
    )
    internal_cap = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv",
            "quantity",
            "K_2",
            "required_bound_l2",
        )
    )
    corrected_half = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "bound_id",
            "CJ3170_2_Rozelot_half_range_proxy",
            "K2_corrected_surface_bound",
        )
    )
    corrected_scale = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "bound_id",
            "CJ3170_0_ZK_adopted_solar_J2_scale",
            "K2_corrected_surface_bound",
        )
    )
    return {
        "c_k2_unit": c_k2_unit,
        "internal_cap": internal_cap,
        "corrected_half": corrected_half,
        "corrected_scale": corrected_scale,
    }


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3170-Y5-R2FR-solar-domain-K2-J2eff-normalization-or-refusal-under-AX1090.md", "3170 corrected J2 normalization handoff"),
        ("3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "K2 residual-vector definition"),
        ("3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090.md", "K2 origin as W2 M_Lambda closure lane"),
        ("3161-Y5-R2FR-Bexact-source-bound-or-Wbar-sensitivity-interface-under-AX1090.md", "l2 boundary primitive/norm origin"),
        ("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "public metric J2 coefficient convention"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv", "corrected conditional J2 bounds"),
    ]
    return [
        {
            "input_id": f"IN3171_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "PO3171_0_K2_origin",
            "object": "K_2",
            "current_owner": "K_2 := |W_2 M_Lambda|",
            "what_is_owned": "a scalar closure lane on the one-dimensional physical l=2 boundary chart",
            "what_is_missing": "a parent field equation or Green map that turns this scalar lane into a public exterior metric profile",
            "verdict": "not_a_radial_profile_owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PO3171_1_CK2_origin",
            "object": "C_K2_unit",
            "current_owner": "C_K2_unit = ||Lambda||_hat(M_Lambda=1) * A_public_full_shell",
            "what_is_owned": "a dimensionless internal residual coefficient assembled from Earth l=2 boundary norm and public full-shell amplitude",
            "what_is_missing": "proof that this coefficient is itself the public metric P2 amplitude at a solar exterior radius",
            "verdict": "not_a_metric_amplitude_without_projection_kernel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PO3171_2_radial_profile",
            "object": "r^-3 exterior J2 profile",
            "current_owner": "3159 owns the public J2 convention once a metric amplitude is already supplied",
            "what_is_owned": "A_metric(r)=2 epsilon J2 rho^-3 for a standard exterior quadrupole",
            "what_is_missing": "MTS proof that the K2 residual obeys the same exterior r^-3 profile and evaluation radius",
            "verdict": "profile_owner_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PO3171_3_source_transfer",
            "object": "Earth first-domain to solar domain transfer",
            "current_owner": "3158-3165 use Earth/source-domain l=2/J2 rows to build C_K2_unit",
            "what_is_owned": "Earth-domain local smoke/closure lane",
            "what_is_missing": "source-domain universality or separate solar-domain K2 construction",
            "verdict": "source_transfer_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PO3171_4_public_metric_injection",
            "object": "Pi_J2_metric",
            "current_owner": "3165 defines generic observable kernels Pi_i,K2",
            "what_is_owned": "formal residual-vector slot Delta_i=Pi_i,K2 K2 C_K2_unit",
            "what_is_missing": "specific Pi_J2_metric/radial kernel mapping K2 into exterior public metric amplitude",
            "verdict": "projection_kernel_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonidentifiability_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "proof_id": "NI3171_0_counterfamily",
            "claim_tested": "current artifacts determine J2_eff from K2",
            "counterfamily": "A_metric_solar(r)=Upsilon_J2*K2*C_K2_unit*(R_s/r)^3 P2(cos theta) for arbitrary Upsilon_J2",
            "why_allowed_by_current_artifacts": "3164-3165 only require the scalar K2 lane and residual-vector placeholder; no row fixes Upsilon_J2",
            "result": "different Upsilon_J2 values preserve existing K2 bookkeeping but give different solar J2_eff",
            "status": "nonidentifiability_proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "proof_id": "NI3171_1_zero_countermodel",
            "claim_tested": "K2 necessarily sources solar exterior J2",
            "counterfamily": "Upsilon_J2=0 with K2 nonzero",
            "why_allowed_by_current_artifacts": "K2 may feed another residual component or be annihilated by the public J2 projection kernel because Pi_J2_metric is not derived",
            "result": "nonzero K2 does not force a solar J2 signal in the current formal state",
            "status": "solar_J2_claim_refuted_current_artifacts",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "proof_id": "NI3171_2_unit_countermodel",
            "claim_tested": "3170 corrected surface bounds are invalid as conditional rows",
            "counterfamily": "Upsilon_J2=1 and standard r^-3 profile",
            "why_allowed_by_current_artifacts": "this is a possible parent completion if the missing metric/radial/source clauses are later signed",
            "result": "3170 rows remain useful conditional pressure rows, but not claim-grade scores",
            "status": "conditional_pressure_survives",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "UJ3171_0_definition",
            "quantity": "Upsilon_J2",
            "definition": "dimensionless transfer kernel from K2*C_K2_unit to solar-surface exterior public metric P2 amplitude",
            "formula": "A_metric_solar_surface = Upsilon_J2*K2*C_K2_unit",
            "current_value": "MISSING_PARENT_PROFILE_AND_METRIC_PROJECTION",
            "claim_status": "required_before_J2_scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "UJ3171_1_corrected_J2_map",
            "quantity": "J2_eff",
            "definition": "solar quadrupole equivalent after Upsilon_J2 is supplied",
            "formula": "J2_eff = Upsilon_J2*K2*C_K2_unit/(2 epsilon_sun_surface) at rho=1",
            "current_value": "symbolic_in_Upsilon_J2",
            "claim_status": "conditional_contract_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "UJ3171_2_bound_scaling_half_range",
            "quantity": "K2_bound_half_range",
            "definition": "3170 half-range corrected surface bound with explicit transfer kernel",
            "formula": f"K2 <= {fmt(v['corrected_half'])}/|Upsilon_J2|",
            "current_value": "not_scoreable_until_Upsilon_J2_exists",
            "claim_status": "conditional_pressure_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "UJ3171_3_owner_clauses",
            "quantity": "J2_transfer_owner_requirements",
            "definition": "minimal clauses needed before any J2-equivalent bound can score K2",
            "formula": "parent Wbar/Lambda owner + public metric injection Pi_J2 + solar source-domain transfer + exterior r^-3 radial Green profile + evaluation radius",
            "current_value": "UNSATISFIED",
            "claim_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def demotion_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "demotion_id": "DM3171_0_3169_shortcut",
            "target": "3169 J2_eff=K2*C_K2_unit",
            "old_status": "conditional shortcut",
            "new_status": "wrong_normalization_smoke_demoted_by_3170",
            "allowed_use": "historical audit only",
            "blocked_use": "numeric J2 scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "demotion_id": "DM3171_1_3170_corrected_bounds",
            "target": "3170 corrected solar-surface J2 bounds",
            "old_status": "conditional corrected transfer",
            "new_status": "conditional_in_Upsilon_J2_transfer_only",
            "allowed_use": f"K2 <= {fmt(v['corrected_half'])}/|Upsilon_J2| pressure row",
            "blocked_use": "direct K2 pass/fail score while Upsilon_J2 is missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "demotion_id": "DM3171_2_local_GR_claim",
            "target": "local-GR/Shapiro safety from quadrupole gate",
            "old_status": "not_claimed",
            "new_status": "still_not_claimed",
            "allowed_use": "use as next derivation target for metric/radial profile owner",
            "blocked_use": "claiming PPN/Shapiro/light-bending safety",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3171_0_no_direct_J2_score",
            "decision": "current artifacts do not identify K2*C_K2_unit with a solar exterior J2-profile metric amplitude",
            "evidence": "PO3171 audit plus NI3171 counterfamily",
            "effect": "3170 numeric J2 pressure rows are demoted to Upsilon_J2-conditional transfer rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3171_1_real_next_derivation",
            "decision": "the next derivation target is the public metric/radial Green profile owner, not another empirical bound hunt",
            "evidence": "UJ3171_3 lists the missing owner clauses",
            "effect": "derive Pi_J2_metric and exterior r^-3 profile from parent equations or abandon J2-equivalent scoring",
            "next_action": "3172-Y5-R2FR-public-metric-radial-Green-owner-or-J2-channel-closure-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    audits: list[dict[str, object]],
    nonident: list[dict[str, object]],
    contracts: list[dict[str, object]],
    demotions: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    profile_missing = any(row["verdict"] == "profile_owner_missing" for row in audits)
    projection_missing = any(row["verdict"] == "projection_kernel_missing" for row in audits)
    counterfamily = any(row["status"] == "nonidentifiability_proof" for row in nonident)
    upsilon_required = any(row["quantity"] == "Upsilon_J2" and "MISSING" in row["current_value"] for row in contracts)
    direct_score_demoted = any(row["demotion_id"] == "DM3171_1_3170_corrected_bounds" for row in demotions)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, audits, nonident, contracts, demotions, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3171_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_1_profile_owner_missing",
            "status": "pass" if profile_missing else "fail",
            "detail": "radial profile owner remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_2_projection_kernel_missing",
            "status": "pass" if projection_missing else "fail",
            "detail": "public metric/J2 projection kernel remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_3_counterfamily_written",
            "status": "pass" if counterfamily else "fail",
            "detail": "Upsilon_J2 counterfamily proves nonidentifiability from current artifacts",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_4_upsilon_contract_required",
            "status": "pass" if upsilon_required else "fail",
            "detail": "Upsilon_J2 required before J2 scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_5_direct_score_demoted",
            "status": "pass" if direct_score_demoted else "fail",
            "detail": "3170 numeric bounds demoted to transfer-only rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3171_6_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3171 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    audits = audit_rows()
    nonident = nonidentifiability_rows()
    contracts = contract_rows(v)
    demotions = demotion_rows(v)
    decisions = decision_rows()
    validations = validation_rows(inputs, audits, nonident, contracts, demotions, decisions)
    write_csv(INPUTS, inputs)
    write_csv(AUDIT, audits)
    write_csv(NONIDENTIFIABILITY, nonident)
    write_csv(CONTRACT, contracts)
    write_csv(DEMOTION, demotions)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3171 validation failed: {failures}")


if __name__ == "__main__":
    main()
