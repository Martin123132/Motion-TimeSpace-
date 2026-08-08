from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3188_INPUTS.csv"
ENVELOPE_GRID = OUT / "P8_Y5_R2FR_3188_ABSOLUTE_ENVELOPE_PRIOR_GRID.csv"
CRITICALS = OUT / "P8_Y5_R2FR_3188_CRITICAL_PROFILE_NORM_ROWS.csv"
ZERO_AUDIT = OUT / "P8_Y5_R2FR_3188_COUPLING_ZERO_AUDIT.csv"
DECISION = OUT / "P8_Y5_R2FR_3188_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3188_VALIDATION.csv"

PH_MARGIN_3186 = OUT / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"
ESTIMATOR_3187 = OUT / "P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv"


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
            "3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090.md",
            "3187 P_H source-profile estimator",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv",
            "3187 estimator formulas",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3187_SHARP_SHELL_CALIBRATION.csv",
            "3187 sharp shell calibration",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv",
            "3186 P_H pressure ceilings",
        ),
        (
            "post_checkpoint",
            "3186-Y5-R2FR-source-owned-PH-amplitude-or-slip-transfer-bound-under-AX1090.md",
            "3186 source-amplitude fork",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 projected moment identity",
        ),
        (
            "post_checkpoint",
            "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md",
            "3178 missing live Khat/source adoption",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3188_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def tightest_bound() -> dict[str, str]:
    rows = read_csv(PH_MARGIN_3186)
    return min(rows, key=lambda row: float(row["P_H_bound_from_slip"]))


def envelope_grid_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    couplings = [0.0, 1.0e-12, 1.0e-9, 1.0e-6, 1.0e-3, 1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12]
    norms = [0.0, 1.0e-12, 1.0e-6, 1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12]
    for bound in read_csv(PH_MARGIN_3186):
        ceiling = float(bound["P_H_bound_from_slip"])
        source_norm_limit = 0.8 * ceiling
        for coupling in couplings:
            for norm in norms:
                ph_envelope = 1.25 * coupling * norm
                rows.append(
                    {
                        "grid_id": f"GRID3188_{bound['bound_name']}_c{coupling:.0e}_n{norm:.0e}",
                        "bound_name": bound["bound_name"],
                        "abs_sK2_kappaSTF": f"{coupling:.15e}",
                        "N4_D2": f"{norm:.15e}",
                        "abs_sK2_kappaSTF_times_N4": f"{coupling * norm:.15e}",
                        "source_norm_limit_4over5_BPH": f"{source_norm_limit:.15e}",
                        "PH_envelope_5over4_product": f"{ph_envelope:.15e}",
                        "PH_bound": f"{ceiling:.15e}",
                        "fraction_of_bound": f"{(ph_envelope / ceiling) if ceiling else 0.0:.15e}",
                        "pressure_pass_if_sourced": str(ph_envelope <= ceiling).lower(),
                        "status": "PRIOR_GRID_NONCLAIM",
                        "valid_for_claim": "false",
                        "generated_utc": now,
                    }
                )
    return rows


def critical_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    couplings = [1.0e-12, 1.0e-9, 1.0e-6, 1.0e-3, 1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12]
    for bound in read_csv(PH_MARGIN_3186):
        ceiling = float(bound["P_H_bound_from_slip"])
        source_norm_limit = 0.8 * ceiling
        for coupling in couplings:
            rows.append(
                {
                    "critical_id": f"CRIT3188_{bound['bound_name']}_c{coupling:.0e}",
                    "bound_name": bound["bound_name"],
                    "abs_sK2_kappaSTF": f"{coupling:.15e}",
                    "max_N4_D2_for_pressure": f"{source_norm_limit / coupling:.15e}",
                    "equivalent_condition": "|s_K2*kappa_STF|*N4_D2 <= (4/5)B_PH",
                    "PH_bound": f"{ceiling:.15e}",
                    "status": "CRITICAL_NORM_NONCLAIM",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def zero_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "zero_id": "CZ3188_0_exact_coupling_zero",
            "route": "s_K2*kappa_STF=0",
            "condition": "parent variation or boundary basis symmetry forces the product coupling to vanish",
            "effect": "P_H=0 for any source profile; local slip lane silent",
            "status": "PARENT_ZERO_WOULD_CLOSE_LANE_IF_PROVEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "CZ3188_1_source_STF_zero",
            "route": "N4_D2=I4_D2=0",
            "condition": "source profile has no projected l=2/STF component in this parent channel",
            "effect": "P_H=0 but the K2 exterior branch also vanishes",
            "status": "SOURCE_SYMMETRY_ZERO_WOULD_CLOSE_BRANCH_IF_PROVEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "CZ3188_2_parametric_small_coupling",
            "route": "small nonzero |s_K2*kappa_STF|",
            "condition": "parent variation produces a small dimensionless coupling product",
            "effect": "large profile norms can still pass if |s*kappa|*N4 stays below (4/5)B_PH",
            "status": "PARAMETRIC_SMALLNESS_RUNNER_AVAILABLE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "CZ3188_3_no_zero_order_one_profile",
            "route": "no zero, order-one coupling/profile",
            "condition": "|s_K2*kappa_STF|~1 and N4_D2~1",
            "effect": "passes current pressure by large margin, but still nonclaim until source-owned",
            "status": "ORDER_ONE_BRANCH_PRESSURE_SAFE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    tight = tightest_bound()
    tight_ceiling = float(tight["P_H_bound_from_slip"])
    limit = 0.8 * tight_ceiling
    return [
        {
            "decision_id": "DEC3188_0_grid_built",
            "finding": "Built absolute-envelope grid for |P_H| <= (5/4)|s_K2*kappa_STF|N4_D2 against all current pressure rows.",
            "claim_status": "PRIOR_GRID_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3188_1_tight_condition",
            "finding": f"Tightest current proxy requires |s_K2*kappa_STF|N4_D2 <= {limit:.15e}.",
            "claim_status": "TIGHT_CONDITION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3188_2_order_one_safe",
            "finding": "The order-one coupling/profile cell passes current pressure; failures require huge coupling*profile products or tighter future transfer bounds.",
            "claim_status": "ORDER_ONE_CELL_SAFE_AS_PRESSURE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3188_3_next_target",
            "finding": "3189-Y5-R2FR-live-source-profile-row-or-transfer-bound-upgrade-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        ENVELOPE_GRID: envelope_grid_rows(),
        CRITICALS: critical_rows(),
        ZERO_AUDIT: zero_audit_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    grid = rows_by_path[ENVELOPE_GRID]
    criticals = rows_by_path[CRITICALS]
    zeros = rows_by_path[ZERO_AUDIT]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    tight = tightest_bound()["bound_name"]
    order_one = [
        row for row in grid
        if row["bound_name"] == tight and float(row["abs_sK2_kappaSTF"]) == 1.0 and float(row["N4_D2"]) == 1.0
    ]
    huge_fail = [
        row for row in grid
        if row["bound_name"] == tight and float(row["abs_sK2_kappaSTF"]) == 1.0e12 and float(row["N4_D2"]) == 1.0
    ]
    return [
        {
            "check_id": "VAL3188_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_1_grid_shape",
            "check": "prior grid has 3 bounds x 10 couplings x 8 norms",
            "pass": str(len(grid) == 240).lower(),
            "detail": f"grid_rows={len(grid)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_2_order_one_cell_passes",
            "check": "tight-bound order-one coupling/profile cell passes",
            "pass": str(len(order_one) == 1 and order_one[0]["pressure_pass_if_sourced"] == "true").lower(),
            "detail": order_one[0]["fraction_of_bound"] if order_one else "missing",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_3_huge_coupling_cell_fails",
            "check": "tight-bound huge coupling/profile cell fails",
            "pass": str(len(huge_fail) == 1 and huge_fail[0]["pressure_pass_if_sourced"] == "false").lower(),
            "detail": huge_fail[0]["fraction_of_bound"] if huge_fail else "missing",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_4_critical_rows",
            "check": "critical norm rows cover 3 bounds x 9 nonzero couplings",
            "pass": str(len(criticals) == 27).lower(),
            "detail": f"critical_rows={len(criticals)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_5_zero_audit_nonclaim",
            "check": "coupling/source zero audit remains nonclaim",
            "pass": str(len(zeros) == 4 and all(row["valid_for_claim"] == "false" for row in zeros)).lower(),
            "detail": "zero/smallness/order-one routes audited",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_6_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3188_7_next_target_selected",
            "check": "decision table selects live source profile row or transfer bound upgrade",
            "pass": str(any("3189-Y5-R2FR-live-source-profile-row" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3189",
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
