from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3190_INPUTS.csv"
WIDTH_SCAN = OUT / "P8_Y5_R2FR_3190_SMOOTHSTEP_WIDTH_SCAN.csv"
SELECTION = OUT / "P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv"
TRANSFER_CONTRACT = OUT / "P8_Y5_R2FR_3190_PPN_TRANSFER_UPGRADE_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3190_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3190_VALIDATION.csv"

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


def smoothstep(t: float) -> float:
    return 6.0 * t**5 - 15.0 * t**4 + 10.0 * t**3


def smoothstep_prime(t: float) -> float:
    return 30.0 * t**4 - 60.0 * t**3 + 30.0 * t**2


def smoothstep_second(t: float) -> float:
    return 120.0 * t**3 - 180.0 * t**2 + 60.0 * t


def d2_transition(x: float, width: float) -> float:
    left = 1.0 - width
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
    return (2.0 / 5.0) * second + 2.0 * first / x + 6.0 * value / (5.0 * x**2)


def simpson_transition(width: float, absolute: bool, steps: int = 4000) -> float:
    if steps % 2:
        steps += 1
    left = 1.0 - width
    right = 1.0 + width
    step = (right - left) / steps
    total = 0.0
    for index in range(steps + 1):
        x = left + index * step
        value = d2_transition(x, width) * x**4
        if absolute:
            value = abs(value)
        coefficient = 1 if index in (0, steps) else (4 if index % 2 else 2)
        total += coefficient * value
    return total * step / 3.0


def profile_integrals(width: float) -> dict[str, float]:
    left = 1.0 - width
    core_signed = 6.0 * left**5 / 5.0
    transition_signed = simpson_transition(width, absolute=False)
    transition_abs = simpson_transition(width, absolute=True)
    signed = core_signed + transition_signed
    absolute = abs(core_signed) + transition_abs
    return {
        "width": width,
        "I4_D2": signed,
        "N4_D2": absolute,
        "c_ext_est": -5.0 * signed / 4.0,
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
            "3189-Y5-R2FR-live-source-profile-row-or-transfer-bound-upgrade-under-AX1090.md",
            "3189 smooth source-profile rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3189_SMOOTH_PROFILE_FAMILY.csv",
            "3189 smooth profile family rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3189_SMOOTH_PROFILE_MARGIN_ROWS.csv",
            "3189 smooth profile margin rows",
        ),
        (
            "post_checkpoint",
            "3188-Y5-R2FR-PH-source-profile-prior-grid-or-parent-coupling-zero-under-AX1090.md",
            "3188 profile/coupling product gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv",
            "3186 P_H pressure ceilings",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3190_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def width_scan_rows() -> list[dict[str, object]]:
    now = stamp()
    tight = tightest_bound()
    ceiling = float(tight["P_H_bound_from_slip"])
    source_norm_limit = 0.8 * ceiling
    rows = []
    for index in range(20, 801, 5):
        width = index / 1000.0
        integrals = profile_integrals(width)
        critical_coupling = source_norm_limit / integrals["N4_D2"]
        rows.append(
            {
                "scan_id": f"SCAN3190_w{width:.3f}",
                "transition_width": f"{width:.15e}",
                "I4_D2": f"{integrals['I4_D2']:.15e}",
                "N4_D2": f"{integrals['N4_D2']:.15e}",
                "c_ext_est": f"{integrals['c_ext_est']:.15e}",
                "signed_to_absolute_ratio": f"{integrals['signed_to_absolute_ratio']:.15e}",
                "critical_abs_sK2_kappaSTF_for_tight_proxy": f"{critical_coupling:.15e}",
                "status": "WIDTH_SCAN_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def selection_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = width_scan_rows()
    best = min(rows, key=lambda row: float(row["N4_D2"]))
    return [
        {
            "selection_id": "SEL3190_0_min_N4_candidate",
            "criterion": "minimize N4_D2 within C2 smoothstep family, width in [0.020,0.800]",
            "selected_width": best["transition_width"],
            "selected_N4_D2": best["N4_D2"],
            "selected_I4_D2": best["I4_D2"],
            "selected_c_ext_est": best["c_ext_est"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": best["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "PROFILE_SELECTION_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "selection_id": "SEL3190_1_parent_selection_condition",
            "criterion": "parent action must derive profile, not choose by convenience",
            "selected_width": best["transition_width"],
            "selected_N4_D2": best["N4_D2"],
            "selected_I4_D2": best["I4_D2"],
            "selected_c_ext_est": best["c_ext_est"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": best["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "PARENT_SELECTION_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def transfer_contract_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "PT3190_0_observable_transfer",
            "needed_object": "Delta observable from Psi-Phi=2 Sigma_H r^-3 P2",
            "minimum_deliverable": "derive mapping to Shapiro/orbital/PPN quadrupole observable in same normalization as current P2 pressure",
            "why_needed": "current pressure proxy may be conservative or loose; local-GR claim needs actual observable transfer",
            "status": "TRANSFER_UPGRADE_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PT3190_1_parent_profile_equation",
            "needed_object": "Euler-Lagrange or matching equation selecting F(x)",
            "minimum_deliverable": "derive transition width/profile class from parent action or boundary condition",
            "why_needed": "min-N4 profile is a candidate, not a parent derivation",
            "status": "PARENT_PROFILE_EQUATION_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PT3190_2_coupling_product",
            "needed_object": "s_K2*kappa_STF",
            "minimum_deliverable": "source-owned sign and magnitude, or exact zero/symmetry theorem",
            "why_needed": "profile rows only become evidence when coupling product is derived",
            "status": "COUPLING_PRODUCT_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    selected = selection_rows()[0]
    return [
        {
            "decision_id": "DEC3190_0_profile_candidate",
            "finding": f"Within the scanned C2 smoothstep family, min-N4 candidate is width={selected['selected_width']} with N4_D2={selected['selected_N4_D2']}.",
            "claim_status": "PROFILE_SELECTION_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3190_1_coupling_margin",
            "finding": f"Selected profile allows |s_K2*kappa_STF| up to {selected['critical_abs_sK2_kappaSTF_for_tight_proxy']} under the tight pressure proxy.",
            "claim_status": "COUPLING_MARGIN_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3190_2_transfer_needed",
            "finding": "The remaining high-value fork is parent profile equation versus PPN/orbital transfer upgrade.",
            "claim_status": "LOCAL_GR_STILL_TRANSFER_OR_PARENT_GATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3190_3_next_target",
            "finding": "3191-Y5-R2FR-selected-profile-transfer-runner-or-parent-action-profile-equation-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        WIDTH_SCAN: width_scan_rows(),
        SELECTION: selection_rows(),
        TRANSFER_CONTRACT: transfer_contract_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    scan = rows_by_path[WIDTH_SCAN]
    selection = rows_by_path[SELECTION]
    transfer = rows_by_path[TRANSFER_CONTRACT]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    selected = selection[0]
    identity_ok = all(
        abs(float(row["I4_D2"]) + 0.8) < 1.0e-8 and abs(float(row["c_ext_est"]) - 1.0) < 1.0e-8
        for row in scan
    )
    selected_width = float(selected["selected_width"])
    selected_norm = float(selected["selected_N4_D2"])
    return [
        {
            "check_id": "VAL3190_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_1_scan_shape",
            "check": "width scan covers 0.020 to 0.800 in 0.005 increments",
            "pass": str(len(scan) == 157).lower(),
            "detail": f"scan_rows={len(scan)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_2_identity_preserved",
            "check": "all scanned profiles preserve I4=-4/5 and c_ext=1",
            "pass": str(identity_ok).lower(),
            "detail": "boundary identity preserved across scan",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_3_selected_width_range",
            "check": "selected min-N4 width is in the expected broad minimum around 0.4-0.5",
            "pass": str(0.40 <= selected_width <= 0.50 and selected_norm < 3.40).lower(),
            "detail": f"width={selected_width:.3f}; N4={selected_norm:.15e}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_4_transfer_contract_nonclaim",
            "check": "transfer/profile/coupling contracts remain nonclaim",
            "pass": str(len(transfer) == 3 and all(row["valid_for_claim"] == "false" for row in transfer)).lower(),
            "detail": "observable transfer, parent profile equation, coupling product",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3190_6_next_target_selected",
            "check": "decision table selects selected-profile transfer runner or parent action equation",
            "pass": str(any("3191-Y5-R2FR-selected-profile-transfer-runner" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3191",
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
