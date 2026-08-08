from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3186_INPUTS.csv"
PH_RUNNER = OUT / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"
OWNER_GAPS = OUT / "P8_Y5_R2FR_3186_PH_SOURCE_OWNER_GAPS.csv"
TRANSFER_COLLAPSE = OUT / "P8_Y5_R2FR_3186_SLIP_TRANSFER_COLLAPSE_CHECK.csv"
DECISION = OUT / "P8_Y5_R2FR_3186_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3186_VALIDATION.csv"

J2_BOUNDS_3170 = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
RECAST_3180 = OUT / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"
CHIH_3185 = OUT / "P8_Y5_R2FR_3185_CHIH_ORDER_DERIVATION.csv"


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


def c_k2_unit() -> float:
    rows = read_csv(J2_BOUNDS_3170)
    values = {float(row["C_K2_unit"]) for row in rows}
    if len(values) != 1:
        raise ValueError(f"expected one C_K2_unit value, got {values}")
    return values.pop()


def chi_h_natural() -> float:
    return 2.0 * c_k2_unit() / 25.0


def recast_by_bound_name() -> dict[str, dict[str, str]]:
    return {row["bound_name"]: row for row in read_csv(RECAST_3180)}


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3185-Y5-R2FR-chiH-parent-variation-zero-or-order-estimate-under-AX1090.md",
            "3185 natural chi_H derivation",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3185_CHIH_ORDER_DERIVATION.csv",
            "3185 chi_H order rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3185_NATURAL_CHIH_SATURATION_CHECK.csv",
            "3185 saturation identity rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv",
            "3180 scalar recast P_H ceilings",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "3170 public metric P2 pressure rows",
        ),
        (
            "post_checkpoint",
            "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md",
            "3178 Khat source-kernel and missing live source owner",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 P_H branch and leakage gates",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3186_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def ph_runner_rows() -> list[dict[str, object]]:
    now = stamp()
    chi = chi_h_natural()
    recast = recast_by_bound_name()
    rows = []
    for source in read_csv(J2_BOUNDS_3170):
        a_bound = float(source["A_metric_bound_surface"])
        sigma_bound = a_bound / 2.0
        p_h_bound = sigma_bound / chi
        p_h_recast = float(recast[source["bound_name"]]["recast_bound"])
        sigma_if_ph1 = chi
        a_slip_if_ph1 = 2.0 * chi
        rows.append(
            {
                "run_id": "PH3186_" + source["bound_id"],
                "bound_name": source["bound_name"],
                "A_metric_bound_surface": f"{a_bound:.15e}",
                "chi_H_natural": f"{chi:.15e}",
                "Sigma_H_bound": f"{sigma_bound:.15e}",
                "P_H_bound_from_slip": f"{p_h_bound:.15e}",
                "P_H_bound_from_3180_recast": f"{p_h_recast:.15e}",
                "bound_ratio_slip_to_recast": f"{p_h_bound / p_h_recast:.15e}",
                "Sigma_H_if_P_H_equals_1": f"{sigma_if_ph1:.15e}",
                "A_slip_if_P_H_equals_1": f"{a_slip_if_ph1:.15e}",
                "safety_margin_for_P_H_equals_1": f"{p_h_bound:.15e}",
                "interpretation": "P_H~1 is far below current pressure; saturation requires a very large dimensionless source product",
                "status": "ORDER_ONE_PH_SAFE_UNDER_CURRENT_PRESSURE_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def owner_gap_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gap_id": "GAP3186_0_sK2",
            "object": "s_K2",
            "current_status": "signed boundary lift exists, magnitude not parent-fixed",
            "needed_for_claim": "derive sign/magnitude from parent boundary basis or source symmetry",
            "effect_if_missing": "P_H cannot be claimed small or zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "GAP3186_1_kappaSTF",
            "object": "kappa_STF",
            "current_status": "formal coupling/source-moment coefficient",
            "needed_for_claim": "derive from parent variation and source tensor normalization",
            "effect_if_missing": "P_H remains a symbolic product",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "GAP3186_2_cExt",
            "object": "c_ext",
            "current_status": "exterior coefficient tied to projected moment but not source-owned",
            "needed_for_claim": "derive from compact source profile, matching layer, and exterior boundary condition",
            "effect_if_missing": "cannot know whether P_H is O(1), tiny, or near ceiling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "GAP3186_3_tensorLeakage",
            "object": "DeltaK_TF / non-D2 tensor leakage",
            "current_status": "known nonzero exterior footprint; metric slip map conditionally handled",
            "needed_for_claim": "bound or parent-null any remaining tensor response not captured by scalar P2 pressure",
            "effect_if_missing": "local-GR claim remains blocked even if P_H runner is numerically plausible",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "GAP3186_4_transfer",
            "object": "slip-to-observable transfer",
            "current_status": "current bound is public P2 pressure proxy",
            "needed_for_claim": "PPN/orbital/light-time transfer with covariance or accepted conservative proxy",
            "effect_if_missing": "pressure rows stay nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def transfer_collapse_rows() -> list[dict[str, object]]:
    now = stamp()
    chi = chi_h_natural()
    cunit = c_k2_unit()
    return [
        {
            "collapse_id": "TC3186_0_bound_equivalence",
            "statement": "With chi_H=2*C_K2_unit/25, the slip bound on P_H is algebraically identical to the 3180 scalar recast bound.",
            "formula": "P_H_bound=(A_metric/2)/(2*C_K2_unit/25)=(25/4)A_metric/C_K2_unit",
            "numeric_chi_H": f"{chi:.15e}",
            "numeric_C_K2_unit": f"{cunit:.15e}",
            "status": "SLIP_BOUND_COLLAPSES_TO_SCALAR_RECAST_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TC3186_1_order_one_margin",
            "statement": "If P_H is naturally order one, the predicted surface slip is A_slip=4*C_K2_unit/25.",
            "formula": "A_slip(P_H=1)=2*chi_H=4*C_K2_unit/25",
            "numeric_A_slip_if_PH1": f"{2.0 * chi:.15e}",
            "numeric_C_K2_unit": f"{cunit:.15e}",
            "status": "ORDER_ONE_PH_HAS_TINY_SLIP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TC3186_2_live_task",
            "statement": "The live empirical/theory task is now source-owning P_H and validating the transfer, not inventing another metric response coefficient.",
            "formula": "P_H=s_K2*kappa_STF*c_ext",
            "numeric_chi_H": f"{chi:.15e}",
            "numeric_C_K2_unit": f"{cunit:.15e}",
            "status": "SOURCE_PRODUCT_AND_TRANSFER_ARE_LIVE_TASKS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    tightest = min(ph_runner_rows(), key=lambda row: float(row["P_H_bound_from_slip"]))
    return [
        {
            "decision_id": "DEC3186_0_bound_collapse",
            "finding": "Using chi_H=2*C_K2_unit/25, the slip pressure reproduces the 3180 P_H recast bound exactly.",
            "claim_status": "TRANSFER_COLLAPSE_DERIVED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3186_1_order_one_PH_margin",
            "finding": f"If P_H=1, the tightest current pressure margin is {tightest['safety_margin_for_P_H_equals_1']} in P_H units.",
            "claim_status": "ORDER_ONE_PH_SAFE_AS_PRESSURE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3186_2_missing_owner",
            "finding": "P_H itself is not source-owned: s_K2, kappa_STF, c_ext, leakage, and transfer remain the live gates.",
            "claim_status": "SOURCE_OWNER_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3186_3_next_target",
            "finding": "3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        PH_RUNNER: ph_runner_rows(),
        OWNER_GAPS: owner_gap_rows(),
        TRANSFER_COLLAPSE: transfer_collapse_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    ph_runner = rows_by_path[PH_RUNNER]
    gaps = rows_by_path[OWNER_GAPS]
    transfer = rows_by_path[TRANSFER_COLLAPSE]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    bound_equivalence = all(
        isclose(float(row["bound_ratio_slip_to_recast"]), 1.0, rel_tol=1e-12, abs_tol=1e-12)
        for row in ph_runner
    )
    order_one_safe = all(float(row["safety_margin_for_P_H_equals_1"]) > 1.0 for row in ph_runner)
    return [
        {
            "check_id": "VAL3186_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_1_bound_equivalence",
            "check": "P_H slip bound equals 3180 scalar recast under natural chi_H",
            "pass": str(len(ph_runner) == 3 and bound_equivalence).lower(),
            "detail": "; ".join(row["bound_ratio_slip_to_recast"] for row in ph_runner),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_2_order_one_margin",
            "check": "P_H=1 is below current pressure rows",
            "pass": str(order_one_safe).lower(),
            "detail": "; ".join(row["safety_margin_for_P_H_equals_1"] for row in ph_runner),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_3_owner_gaps_retained",
            "check": "source-owner and transfer gaps remain explicit",
            "pass": str(len(gaps) == 5 and all(row["valid_for_claim"] == "false" for row in gaps)).lower(),
            "detail": "s_K2;kappa_STF;c_ext;DeltaK_TF;transfer",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_4_transfer_collapse_recorded",
            "check": "transfer-collapse rows record conditional equivalence and live task",
            "pass": str(any(row["status"] == "SLIP_BOUND_COLLAPSES_TO_SCALAR_RECAST_CONDITIONALLY" for row in transfer) and any(row["status"] == "SOURCE_PRODUCT_AND_TRANSFER_ARE_LIVE_TASKS" for row in transfer)).lower(),
            "detail": f"{len(transfer)} transfer rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3186_6_next_target_selected",
            "check": "decision table selects kappa_STF/c_ext source profile estimator or parent zero",
            "pass": str(any("3187-Y5-R2FR-kappaSTF-cExt-source-profile" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3187",
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
