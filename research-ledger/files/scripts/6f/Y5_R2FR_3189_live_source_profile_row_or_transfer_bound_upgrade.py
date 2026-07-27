from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3189_INPUTS.csv"
PROFILE_FAMILY = OUT / "P8_Y5_R2FR_3189_SMOOTH_PROFILE_FAMILY.csv"
PROFILE_MARGINS = OUT / "P8_Y5_R2FR_3189_SMOOTH_PROFILE_MARGIN_ROWS.csv"
TRANSFER_STATUS = OUT / "P8_Y5_R2FR_3189_TRANSFER_BOUND_STATUS.csv"
DECISION = OUT / "P8_Y5_R2FR_3189_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3189_VALIDATION.csv"

PH_MARGIN_3186 = OUT / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"
CRITICALS_3188 = OUT / "P8_Y5_R2FR_3188_CRITICAL_PROFILE_NORM_ROWS.csv"


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


def smoothstep(t: float) -> float:
    return 6.0 * t**5 - 15.0 * t**4 + 10.0 * t**3


def smoothstep_prime(t: float) -> float:
    return 30.0 * t**4 - 60.0 * t**3 + 30.0 * t**2


def smoothstep_second(t: float) -> float:
    return 120.0 * t**3 - 180.0 * t**2 + 60.0 * t


def profile_derivatives(x: float, width: float, amplitude: float = 1.0) -> tuple[float, float, float]:
    left = 1.0 - width
    right = 1.0 + width
    if x <= left:
        return amplitude * x**2, amplitude * 2.0 * x, amplitude * 2.0
    if x >= right:
        return amplitude * x**-3, amplitude * (-3.0 * x**-4), amplitude * (12.0 * x**-5)

    t = (x - left) / (2.0 * width)
    blend = smoothstep(t)
    blend_prime = smoothstep_prime(t) / (2.0 * width)
    blend_second = smoothstep_second(t) / (4.0 * width**2)

    core = x**2
    core_prime = 2.0 * x
    core_second = 2.0
    exterior = x**-3
    exterior_prime = -3.0 * x**-4
    exterior_second = 12.0 * x**-5

    value = core + blend * (exterior - core)
    first = core_prime + blend_prime * (exterior - core) + blend * (exterior_prime - core_prime)
    second = (
        core_second
        + blend_second * (exterior - core)
        + 2.0 * blend_prime * (exterior_prime - core_prime)
        + blend * (exterior_second - core_second)
    )
    return amplitude * value, amplitude * first, amplitude * second


def d2_value(x: float, width: float, amplitude: float = 1.0) -> float:
    value, first, second = profile_derivatives(x, width, amplitude)
    return (2.0 / 5.0) * second + 2.0 * first / x + 6.0 * value / (5.0 * x**2)


def simpson_transition_integral(width: float, absolute: bool, steps: int = 20000) -> float:
    if steps % 2:
        steps += 1
    left = 1.0 - width
    right = 1.0 + width
    step = (right - left) / steps
    total = 0.0
    for index in range(steps + 1):
        x = left + index * step
        value = d2_value(x, width) * x**4
        if absolute:
            value = abs(value)
        coefficient = 1 if index in (0, steps) else (4 if index % 2 else 2)
        total += coefficient * value
    return total * step / 3.0


def profile_integrals(width: float) -> dict[str, float]:
    left = 1.0 - width
    core_signed = 6.0 * left**5 / 5.0
    transition_signed = simpson_transition_integral(width, absolute=False)
    transition_abs = simpson_transition_integral(width, absolute=True)
    signed = core_signed + transition_signed
    absolute = abs(core_signed) + transition_abs
    c_ext_est = -5.0 * signed / 4.0
    return {
        "transition_width": width,
        "core_signed": core_signed,
        "transition_signed": transition_signed,
        "I4_D2": signed,
        "N4_D2": absolute,
        "c_ext_est": c_ext_est,
        "signed_to_absolute_ratio": abs(signed) / absolute,
    }


def tightest_bound() -> dict[str, str]:
    rows = read_csv(PH_MARGIN_3186)
    return min(rows, key=lambda row: float(row["P_H_bound_from_slip"]))


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3188-Y5-R2FR-PH-source-profile-prior-grid-or-parent-coupling-zero-under-AX1090.md",
            "3188 prior grid and coupling/profile gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3188_CRITICAL_PROFILE_NORM_ROWS.csv",
            "3188 critical profile norm rows",
        ),
        (
            "post_checkpoint",
            "3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090.md",
            "3187 source-profile estimator",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv",
            "3187 estimator formulas",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv",
            "3186 P_H pressure ceilings",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 boundary identity",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3189_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def profile_family_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for width in [0.02, 0.05, 0.10, 0.20, 0.40, 0.70]:
        integrals = profile_integrals(width)
        rows.append(
            {
                "profile_id": f"SP3189_width_{width:.2f}",
                "profile_family": "C2_smoothstep_core_to_exterior",
                "definition": "F=x^2 for x<=1-w; F=(1-S)x^2+S*x^-3 for 1-w<x<1+w; F=x^-3 for x>=1+w; S=6t^5-15t^4+10t^3",
                "transition_width": f"{width:.15e}",
                "I4_D2": f"{integrals['I4_D2']:.15e}",
                "N4_D2": f"{integrals['N4_D2']:.15e}",
                "c_ext_est": f"{integrals['c_ext_est']:.15e}",
                "signed_to_absolute_ratio": f"{integrals['signed_to_absolute_ratio']:.15e}",
                "core_signed": f"{integrals['core_signed']:.15e}",
                "transition_signed": f"{integrals['transition_signed']:.15e}",
                "status": "LIVE_SMOOTH_PROFILE_ROW_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def profile_margin_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    tight = tightest_bound()
    ceiling = float(tight["P_H_bound_from_slip"])
    source_norm_limit = 0.8 * ceiling
    coupling_cases = [1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12]
    for profile in profile_family_rows():
        norm = float(profile["N4_D2"])
        for coupling in coupling_cases:
            product = coupling * norm
            ph_envelope = 1.25 * product
            rows.append(
                {
                    "margin_id": f"PM3189_{profile['profile_id']}_c{coupling:.0e}",
                    "profile_id": profile["profile_id"],
                    "bound_name": tight["bound_name"],
                    "abs_sK2_kappaSTF": f"{coupling:.15e}",
                    "N4_D2": f"{norm:.15e}",
                    "source_norm_product": f"{product:.15e}",
                    "source_norm_limit_4over5_BPH": f"{source_norm_limit:.15e}",
                    "PH_envelope": f"{ph_envelope:.15e}",
                    "PH_bound": f"{ceiling:.15e}",
                    "fraction_of_bound": f"{ph_envelope / ceiling:.15e}",
                    "pressure_pass_if_sourced": str(ph_envelope <= ceiling).lower(),
                    "status": "SMOOTH_PROFILE_MARGIN_NONCLAIM",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def transfer_status_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "transfer_id": "TR3189_0_current_proxy",
            "object": "current_transfer_bound",
            "statement": "Current local bound is still a public solar P2 pressure proxy, not a covariance-grade PPN/orbital transfer.",
            "needed_upgrade": "derive Shapiro/orbital/PPN observable transfer for the induced slip, or source an accepted conservative public P2 comparator",
            "status": "TRANSFER_PROXY_RETAINED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3189_1_live_profile_rows",
            "object": "smooth_profile_family",
            "statement": "Smooth finite-transition profiles give live I4/N4 rows and preserve the boundary identity I4=-4/5 for c_ext=1.",
            "needed_upgrade": "parent action must select or derive the transition profile and coupling product",
            "status": "PROFILE_ROWS_READY_FOR_PARENT_SELECTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3189_2_next_empirical_gate",
            "object": "local_GR_gate",
            "statement": "For the tested profiles, order-one through 1e9 coupling products pass tight current pressure; 1e12 fails.",
            "needed_upgrade": "test real parent-derived coupling/profile scale rather than broad priors",
            "status": "EMPIRICAL_PRESSURE_GATE_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    profiles = profile_family_rows()
    norms = [float(row["N4_D2"]) for row in profiles]
    return [
        {
            "decision_id": "DEC3189_0_profile_rows_built",
            "finding": f"Built {len(profiles)} C2 finite-transition profile rows; all preserve c_ext≈1 and I4_D2≈-4/5.",
            "claim_status": "LIVE_PROFILE_ROWS_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3189_1_norm_range",
            "finding": f"Smooth-profile N4_D2 range is {min(norms):.15e} to {max(norms):.15e}, so order-one coupling/profile is comfortably below current pressure.",
            "claim_status": "PROFILE_NORM_RANGE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3189_2_transfer_status",
            "finding": "Transfer remains pressure-proxy, but profile rows are now concrete enough for parent selection or future PPN/orbital transfer upgrade.",
            "claim_status": "TRANSFER_UPGRADE_STILL_NEEDED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3189_3_next_target",
            "finding": "3190-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        PROFILE_FAMILY: profile_family_rows(),
        PROFILE_MARGINS: profile_margin_rows(),
        TRANSFER_STATUS: transfer_status_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    profiles = rows_by_path[PROFILE_FAMILY]
    margins = rows_by_path[PROFILE_MARGINS]
    transfer = rows_by_path[TRANSFER_STATUS]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    identity_ok = all(
        abs(float(row["I4_D2"]) + 0.8) < 1.0e-9 and abs(float(row["c_ext_est"]) - 1.0) < 1.0e-9
        for row in profiles
    )
    order_one_pass = all(
        row["pressure_pass_if_sourced"] == "true"
        for row in margins
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+00"
    )
    trillion_fail = all(
        row["pressure_pass_if_sourced"] == "false"
        for row in margins
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+12"
    )
    return [
        {
            "check_id": "VAL3189_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3189_1_profile_identity",
            "check": "all smooth profiles preserve I4=-4/5 and c_ext=1",
            "pass": str(len(profiles) == 6 and identity_ok).lower(),
            "detail": f"profile_rows={len(profiles)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3189_2_profile_margins",
            "check": "order-one coupling rows pass and 1e12 coupling rows fail the tight proxy",
            "pass": str(order_one_pass and trillion_fail).lower(),
            "detail": f"margin_rows={len(margins)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3189_3_transfer_status_nonclaim",
            "check": "transfer proxy and upgrade need remain explicit",
            "pass": str(any(row["status"] == "TRANSFER_PROXY_RETAINED_NONCLAIM" for row in transfer)).lower(),
            "detail": f"transfer_rows={len(transfer)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3189_4_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3189_5_next_target_selected",
            "check": "decision table selects parent profile selection or PPN transfer upgrade",
            "pass": str(any("3190-Y5-R2FR-parent-profile-selection" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3190",
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
