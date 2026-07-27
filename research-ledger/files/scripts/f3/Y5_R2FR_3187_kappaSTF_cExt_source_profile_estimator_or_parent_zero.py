from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3187_INPUTS.csv"
ESTIMATOR = OUT / "P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv"
SHARP_SHELL = OUT / "P8_Y5_R2FR_3187_SHARP_SHELL_CALIBRATION.csv"
MARGIN = OUT / "P8_Y5_R2FR_3187_SOURCE_PRODUCT_MARGIN_RUNNER.csv"
ZERO_AUDIT = OUT / "P8_Y5_R2FR_3187_PARENT_ZERO_AUDIT.csv"
DECISION = OUT / "P8_Y5_R2FR_3187_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3187_VALIDATION.csv"

PH_MARGIN_3186 = OUT / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"


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
            "3186-Y5-R2FR-source-owned-PH-amplitude-or-slip-transfer-bound-under-AX1090.md",
            "3186 P_H source-amplitude fork",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv",
            "3186 P_H margin rows",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 boundary identity and sharp shell calibration",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_PROJECTED_MOMENT_IDENTITY.csv",
            "3180 projected moment identity rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_SHELL_TRANSITION_LEDGER.csv",
            "3180 sharp shell ledger",
        ),
        (
            "post_checkpoint",
            "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.md",
            "3179 D2 operator and leakage warning",
        ),
        (
            "post_checkpoint",
            "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md",
            "3178 source-kernel normalization and missing live Khat adoption",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3187_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def estimator_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "estimator_id": "EST3187_0_signed_source_moment",
            "object": "I4_D2",
            "statement": "Use the 3180 boundary identity to make c_ext a source-profile readout.",
            "formula": "I4_D2 := integral_0^infty D2[F](x) x^4 dx = -4 c_ext/5",
            "result": "c_ext = -5 I4_D2/4",
            "status": "CEXT_ESTIMATOR_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "estimator_id": "EST3187_1_PH_signed_estimator",
            "object": "P_H",
            "statement": "The source product can be estimated from the signed projected source moment once s_K2*kappa_STF is parent-owned.",
            "formula": "P_H=s_K2*kappa_STF*c_ext=-(5/4)s_K2*kappa_STF*I4_D2",
            "result": "signed source-profile estimator",
            "status": "PH_SIGNED_ESTIMATOR_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "estimator_id": "EST3187_2_absolute_norm_envelope",
            "object": "N4_D2",
            "statement": "A conservative envelope follows from the absolute projected-source norm.",
            "formula": "N4_D2:=integral |D2[F](x)| x^4 dx; |P_H| <= (5/4)|s_K2*kappa_STF| N4_D2",
            "result": "absolute-norm sufficient bound",
            "status": "PH_ABSOLUTE_ENVELOPE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "estimator_id": "EST3187_3_pass_condition",
            "object": "source_profile_pass_gate",
            "statement": "Given a pressure ceiling B_PH, a source profile passes the scalar/slip pressure envelope if this inequality is source-owned.",
            "formula": "|s_K2*kappa_STF*I4_D2| <= (4/5)B_PH, or conservatively |s_K2*kappa_STF|N4_D2 <= (4/5)B_PH",
            "result": "profile estimator becomes executable when I4/N4 and coupling are sourced",
            "status": "PASS_GATE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "estimator_id": "EST3187_4_zero_condition",
            "object": "parent_zero",
            "statement": "The projected branch is zero exactly if the signed projected moment or coupling product vanishes.",
            "formula": "P_H=0 iff s_K2*kappa_STF*I4_D2=0 in this branch",
            "result": "zero theorem must target coupling, source symmetry, or exterior coefficient",
            "status": "ZERO_CONDITION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def sharp_shell_rows() -> list[dict[str, object]]:
    now = stamp()
    a2 = 1.0
    core_signed = 6.0 * a2 / 5.0
    shell_signed = -2.0 * a2
    total_signed = core_signed + shell_signed
    abs_norm = abs(core_signed) + abs(shell_signed)
    c_ext = a2
    return [
        {
            "cal_id": "CAL3187_0_normalized_profile",
            "profile": "quadratic_core_plus_sharp_shell",
            "statement": "In normalized x=r/R_b units, F_in=a2 x^2 and F_out=c_ext x^-3 with value matching gives c_ext=a2.",
            "formula": "F_in(1)=a2; F_out(1)=c_ext; hence c_ext=a2",
            "a2": f"{a2:.15e}",
            "c_ext": f"{c_ext:.15e}",
            "status": "VALUE_MATCH_CALIBRATION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cal_id": "CAL3187_1_signed_moment",
            "profile": "quadratic_core_plus_sharp_shell",
            "statement": "The 3180 core plus shell signed projected moment matches the boundary identity.",
            "formula": "I4_D2 = 6a2/5 - 2a2 = -4a2/5",
            "core_signed": f"{core_signed:.15e}",
            "shell_signed": f"{shell_signed:.15e}",
            "total_signed": f"{total_signed:.15e}",
            "status": "SIGNED_MOMENT_CALIBRATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cal_id": "CAL3187_2_absolute_norm",
            "profile": "quadratic_core_plus_sharp_shell",
            "statement": "The absolute projected-source norm is larger because core and shell partially cancel.",
            "formula": "N4_D2 = |6a2/5|+|2a2| = 16|a2|/5",
            "N4_D2": f"{abs_norm:.15e}",
            "signed_to_absolute_ratio": f"{abs(total_signed) / abs_norm:.15e}",
            "status": "CANCELLATION_FACTOR_ONE_QUARTER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cal_id": "CAL3187_3_PH_for_sharp_shell",
            "profile": "quadratic_core_plus_sharp_shell",
            "statement": "For the normalized sharp-shell profile, P_H reduces to the compact product s_K2*kappa_STF*a2.",
            "formula": "P_H=s_K2*kappa_STF*c_ext=s_K2*kappa_STF*a2",
            "c_ext": f"{c_ext:.15e}",
            "status": "SHARP_SHELL_PH_ESTIMATOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def margin_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    scenarios = [
        ("order_one_profile", 1.0),
        ("large_profile_1e6", 1.0e6),
        ("large_profile_1e9", 1.0e9),
        ("near_tight_proxy_1e11", 1.0e11),
        ("above_tight_proxy_1e12", 1.0e12),
    ]
    for bound in read_csv(PH_MARGIN_3186):
        ceiling = float(bound["P_H_bound_from_slip"])
        for scenario_id, ph_value in scenarios:
            rows.append(
                {
                    "margin_id": f"MR3187_{bound['bound_name']}_{scenario_id}",
                    "bound_name": bound["bound_name"],
                    "scenario": scenario_id,
                    "assumed_abs_PH": f"{ph_value:.15e}",
                    "PH_bound": f"{ceiling:.15e}",
                    "fraction_of_bound": f"{ph_value / ceiling:.15e}",
                    "pressure_pass_if_sourced": str(ph_value <= ceiling).lower(),
                    "interpretation": "illustrative only: pass requires source-owned s_K2,kappa_STF,c_ext and accepted transfer",
                    "status": "SMOKE_MARGIN_NONCLAIM",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def zero_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "zero_id": "ZERO3187_0_isotropic_source",
            "zero_route": "STF source symmetry",
            "condition": "kappa_STF*c_ext=0 because the compact source has no parent-owned l=2/STF component",
            "effect": "P_H=0 and local slip branch is silent, but no K2 exterior signal remains in this lane",
            "status": "PARENT_SYMMETRY_CAN_ZERO_BRANCH_IF_PROVEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZERO3187_1_cExt_zero",
            "zero_route": "exterior coefficient zero",
            "condition": "I4_D2=0 and hence c_ext=0",
            "effect": "projected K2 branch vanishes by 3180 identity",
            "status": "ZERO_KILLS_PROJECTED_BRANCH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZERO3187_2_coupling_zero",
            "zero_route": "kappa_STF or s_K2 zero",
            "condition": "parent variation or boundary basis proves s_K2*kappa_STF=0",
            "effect": "P_H=0 without needing c_ext=0, but also removes this source-channel coupling",
            "status": "COUPLING_ZERO_OPEN_NOT_PROVEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZERO3187_3_transition_cancellation",
            "zero_route": "core/shell cancellation",
            "condition": "try to cancel signed I4_D2 while retaining exterior c_ext",
            "effect": "not available for fixed regular origin plus exterior coefficient: boundary identity fixes I4_D2=-4c_ext/5",
            "status": "CANCELLATION_CANNOT_HIDE_FIXED_CEXT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    tightest = min(read_csv(PH_MARGIN_3186), key=lambda row: float(row["P_H_bound_from_slip"]))
    return [
        {
            "decision_id": "DEC3187_0_estimator_built",
            "finding": "Derived c_ext=-5I4_D2/4 and P_H=-(5/4)s_K2*kappa_STF*I4_D2, with an absolute-norm envelope.",
            "claim_status": "SOURCE_PROFILE_ESTIMATOR_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3187_1_sharp_shell_calibration",
            "finding": "For normalized quadratic-core plus sharp-shell profile, c_ext=a2 and P_H=s_K2*kappa_STF*a2; signed/absolute projected-source ratio is 1/4.",
            "claim_status": "PROFILE_CALIBRATION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3187_2_margin_scale",
            "finding": f"Tightest current pressure allows |P_H| <= {float(tightest['P_H_bound_from_slip']):.15e}; illustrative P_H=1,1e6,1e9,1e11 pass but 1e12 fails the tight proxy.",
            "claim_status": "MARGIN_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3187_3_next_target",
            "finding": "3188-Y5-R2FR-PH-source-profile-prior-grid-or-parent-coupling-zero-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        ESTIMATOR: estimator_rows(),
        SHARP_SHELL: sharp_shell_rows(),
        MARGIN: margin_rows(),
        ZERO_AUDIT: zero_audit_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    estimator = rows_by_path[ESTIMATOR]
    shell = rows_by_path[SHARP_SHELL]
    margins = rows_by_path[MARGIN]
    zero = rows_by_path[ZERO_AUDIT]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    shell_total = next(row for row in shell if row["cal_id"] == "CAL3187_1_signed_moment")
    shell_abs = next(row for row in shell if row["cal_id"] == "CAL3187_2_absolute_norm")
    tight_proxy_passes = [
        row for row in margins if row["bound_name"] == "solar_J2_half_range_proxy" and row["pressure_pass_if_sourced"] == "true"
    ]
    tight_proxy_fails = [
        row for row in margins if row["bound_name"] == "solar_J2_half_range_proxy" and row["pressure_pass_if_sourced"] == "false"
    ]
    return [
        {
            "check_id": "VAL3187_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_1_estimator_present",
            "check": "c_ext and P_H signed estimators are recorded",
            "pass": str(any(row["status"] == "CEXT_ESTIMATOR_DERIVED" for row in estimator) and any(row["status"] == "PH_SIGNED_ESTIMATOR_DERIVED" for row in estimator)).lower(),
            "detail": "c_ext=-5I4/4; P_H=-(5/4)s*kappa*I4",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_2_sharp_shell_calibration",
            "check": "sharp-shell signed and absolute calibration matches 3180",
            "pass": str(isclose(float(shell_total["total_signed"]), -0.8, rel_tol=1e-12) and isclose(float(shell_abs["signed_to_absolute_ratio"]), 0.25, rel_tol=1e-12)).lower(),
            "detail": "I4=-4/5; N4=16/5; ratio=1/4",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_3_margin_smoke",
            "check": "tight proxy passes order-one through 1e11 scenarios and fails 1e12 scenario",
            "pass": str(len(tight_proxy_passes) == 4 and len(tight_proxy_fails) == 1).lower(),
            "detail": f"tight_proxy_passes={len(tight_proxy_passes)}; tight_proxy_fails={len(tight_proxy_fails)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_4_zero_audit_retained",
            "check": "zero audit keeps parent-zero routes nonclaim",
            "pass": str(len(zero) == 4 and all(row["valid_for_claim"] == "false" for row in zero)).lower(),
            "detail": "symmetry/c_ext/coupling/cancellation routes audited",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3187_6_next_target_selected",
            "check": "decision table selects PH profile prior grid or coupling zero",
            "pass": str(any("3188-Y5-R2FR-PH-source-profile-prior-grid" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3188",
            "generated_utc": now,
        },
    ]


def main() -> None:
    rows_by_path = all_output_rows()
    rows_by_path[VALIDATION] = validation_rows(rows_by_path)
    for path, rows in rows_by_path.items():
        write_csv(path, rows)
    for path in rows_by_path:
        print(path)


if __name__ == "__main__":
    main()
