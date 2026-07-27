from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3191_INPUTS.csv"
TRANSFER_RUNNER = OUT / "P8_Y5_R2FR_3191_SELECTED_PROFILE_TRANSFER_RUNNER.csv"
TRANSFER_CRITICALS = OUT / "P8_Y5_R2FR_3191_TRANSFER_TIGHTENING_CRITICALS.csv"
PARENT_EQUATION = OUT / "P8_Y5_R2FR_3191_PARENT_PROFILE_EQUATION_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3191_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3191_VALIDATION.csv"

SELECTION_3190 = OUT / "P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv"
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


def selected_profile() -> dict[str, str]:
    rows = read_csv(SELECTION_3190)
    return next(row for row in rows if row["selection_id"] == "SEL3190_0_min_N4_candidate")


def tightest_bound() -> dict[str, str]:
    rows = read_csv(PH_MARGIN_3186)
    return min(rows, key=lambda row: float(row["P_H_bound_from_slip"]))


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3190-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade-under-AX1090.md",
            "3190 selected smooth profile and transfer/profile fork",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv",
            "3190 selected profile row",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3190_PPN_TRANSFER_UPGRADE_CONTRACT.csv",
            "3190 transfer/profile/coupling contract",
        ),
        (
            "post_checkpoint",
            "3189-Y5-R2FR-live-source-profile-row-or-transfer-bound-upgrade-under-AX1090.md",
            "3189 smooth finite-transition profiles",
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
            "input_id": f"IN3191_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def transfer_runner_rows() -> list[dict[str, object]]:
    now = stamp()
    profile = selected_profile()
    tight = tightest_bound()
    width = float(profile["selected_width"])
    n4 = float(profile["selected_N4_D2"])
    bound = float(tight["P_H_bound_from_slip"])
    couplings = [1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e10, float(profile["critical_abs_sK2_kappaSTF_for_tight_proxy"]), 1.0e11]
    transfer_factors = [1.0, 1.0e-3, 1.0e-6, 1.0e-9, 1.0e-12]
    rows = []
    for coupling in couplings:
        ph_envelope = 1.25 * coupling * n4
        for factor in transfer_factors:
            effective_bound = factor * bound
            rows.append(
                {
                    "run_id": f"RUN3191_c{coupling:.6e}_tf{factor:.0e}",
                    "profile_width": f"{width:.15e}",
                    "N4_D2": f"{n4:.15e}",
                    "abs_sK2_kappaSTF": f"{coupling:.15e}",
                    "PH_envelope": f"{ph_envelope:.15e}",
                    "base_PH_bound": f"{bound:.15e}",
                    "transfer_bound_factor": f"{factor:.15e}",
                    "effective_PH_bound": f"{effective_bound:.15e}",
                    "fraction_of_effective_bound": f"{ph_envelope / effective_bound:.15e}" if effective_bound else "inf",
                    "pressure_pass_if_sourced": str(ph_envelope <= effective_bound).lower(),
                    "status": "SELECTED_PROFILE_TRANSFER_RUNNER_NONCLAIM",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def transfer_critical_rows() -> list[dict[str, object]]:
    now = stamp()
    profile = selected_profile()
    tight = tightest_bound()
    n4 = float(profile["selected_N4_D2"])
    bound = float(tight["P_H_bound_from_slip"])
    couplings = [1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e10, 1.0e11]
    rows = []
    for coupling in couplings:
        ph_envelope = 1.25 * coupling * n4
        minimum_transfer_factor = ph_envelope / bound
        rows.append(
            {
                "critical_id": f"CRIT3191_c{coupling:.0e}",
                "abs_sK2_kappaSTF": f"{coupling:.15e}",
                "N4_D2": f"{n4:.15e}",
                "PH_envelope": f"{ph_envelope:.15e}",
                "base_PH_bound": f"{bound:.15e}",
                "minimum_transfer_bound_factor_to_pass": f"{minimum_transfer_factor:.15e}",
                "equivalent_max_tightening_factor": f"{1.0 / minimum_transfer_factor:.15e}",
                "interpretation": "future transfer bound may be tightened by this factor before this coupling/profile cell fails",
                "status": "TRANSFER_TIGHTENING_CRITICAL_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def parent_equation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "equation_id": "PE3191_0_D2_operator",
            "object": "profile_operator",
            "statement": "The profile source operator is the same projected Hessian operator used since 3179.",
            "formula": "D2[F]=(2/5)F''+2F'/x+6F/(5x^2)",
            "status": "CARRIED_OPERATOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "equation_id": "PE3191_1_quadratic_profile_functional",
            "object": "candidate_parent_profile_functional",
            "statement": "If a parent profile equation minimizes quadratic projected source stress, the natural toy functional is J[F]=int x^4(D2[F])^2 dx.",
            "formula": "J[F]=integral x^4 (D2[F])^2 dx with fixed core/exterior boundary data",
            "status": "CANDIDATE_FUNCTIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "equation_id": "PE3191_2_Euler_Lagrange_contract",
            "object": "profile_EL_equation",
            "statement": "The Euler-Lagrange equation for the quadratic toy functional is the adjoint-normal equation.",
            "formula": "D2^dagger[x^4 D2[F]]=0, where D2^dagger[u]=(2/5)u''-(2u/x)'+6u/(5x^2)",
            "status": "EL_CONTRACT_DERIVED_NOT_MTS_PARENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "equation_id": "PE3191_3_smoothstep_status",
            "object": "selected_smoothstep_profile",
            "statement": "The selected w=0.435 smoothstep profile is a min-N4 candidate within an ansatz family, not a solution of the parent Euler-Lagrange equation.",
            "formula": "parent closure requires deriving F(x), boundary conditions, and coupling product from S_parent",
            "status": "ANSATZ_CANDIDATE_PARENT_EQUATION_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    crit_order_one = next(row for row in transfer_critical_rows() if row["abs_sK2_kappaSTF"] == "1.000000000000000e+00")
    crit_1e9 = next(row for row in transfer_critical_rows() if row["abs_sK2_kappaSTF"] == "1.000000000000000e+09")
    return [
        {
            "decision_id": "DEC3191_0_runner_built",
            "finding": "Built selected-profile transfer runner across coupling products and transfer-bound tightening factors.",
            "claim_status": "TRANSFER_SENSITIVITY_RUNNER_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3191_1_order_one_transfer_margin",
            "finding": f"For |s_K2*kappa_STF|=1, the current transfer proxy can tighten by {crit_order_one['equivalent_max_tightening_factor']} before failure.",
            "claim_status": "ORDER_ONE_TRANSFER_MARGIN_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3191_2_large_coupling_margin",
            "finding": f"For |s_K2*kappa_STF|=1e9, the current transfer proxy can tighten by {crit_1e9['equivalent_max_tightening_factor']} before failure.",
            "claim_status": "LARGE_COUPLING_TRANSFER_MARGIN_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3191_3_parent_equation_contract",
            "finding": "Derived the toy parent-profile EL contract D2^dagger[x^4D2[F]]=0; selected smoothstep remains ansatz-only until parent-signed.",
            "claim_status": "PARENT_PROFILE_EQUATION_CONTRACT_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3191_4_next_target",
            "finding": "3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        TRANSFER_RUNNER: transfer_runner_rows(),
        TRANSFER_CRITICALS: transfer_critical_rows(),
        PARENT_EQUATION: parent_equation_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    runner = rows_by_path[TRANSFER_RUNNER]
    criticals = rows_by_path[TRANSFER_CRITICALS]
    parent_eq = rows_by_path[PARENT_EQUATION]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    order_one_1e9 = [
        row for row in runner
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+00"
        and row["transfer_bound_factor"] == "1.000000000000000e-09"
    ]
    order_one_1e12 = [
        row for row in runner
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+00"
        and row["transfer_bound_factor"] == "1.000000000000000e-12"
    ]
    coupling_1e9_base = [
        row for row in runner
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+09"
        and row["transfer_bound_factor"] == "1.000000000000000e+00"
    ]
    coupling_1e9_1e3 = [
        row for row in runner
        if row["abs_sK2_kappaSTF"] == "1.000000000000000e+09"
        and row["transfer_bound_factor"] == "1.000000000000000e-03"
    ]
    return [
        {
            "check_id": "VAL3191_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_1_runner_shape",
            "check": "transfer runner has 7 coupling cases x 5 transfer factors",
            "pass": str(len(runner) == 35).lower(),
            "detail": f"runner_rows={len(runner)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_2_order_one_sensitivity",
            "check": "order-one coupling passes 1e-9 transfer factor but fails 1e-12 factor",
            "pass": str(order_one_1e9 and order_one_1e9[0]["pressure_pass_if_sourced"] == "true" and order_one_1e12 and order_one_1e12[0]["pressure_pass_if_sourced"] == "false").lower(),
            "detail": "selected profile transfer sensitivity bracketed",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_3_large_coupling_sensitivity",
            "check": "1e9 coupling passes current proxy but fails 1e-3 transfer factor",
            "pass": str(coupling_1e9_base and coupling_1e9_base[0]["pressure_pass_if_sourced"] == "true" and coupling_1e9_1e3 and coupling_1e9_1e3[0]["pressure_pass_if_sourced"] == "false").lower(),
            "detail": "1e9 coupling has only ~57x transfer-tightening margin",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_4_critical_rows",
            "check": "critical transfer rows are present for six coupling cases",
            "pass": str(len(criticals) == 6 and all(float(row["minimum_transfer_bound_factor_to_pass"]) > 0 for row in criticals)).lower(),
            "detail": f"critical_rows={len(criticals)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_5_parent_equation_contract",
            "check": "parent profile Euler-Lagrange contract is recorded as nonclaim",
            "pass": str(any(row["status"] == "EL_CONTRACT_DERIVED_NOT_MTS_PARENT" for row in parent_eq) and any(row["status"] == "ANSATZ_CANDIDATE_PARENT_EQUATION_REQUIRED" for row in parent_eq)).lower(),
            "detail": "D2^dagger[x^4D2[F]]=0",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_6_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3191_7_next_target_selected",
            "check": "decision table selects quadratic profile EL solve or transfer upgrade",
            "pass": str(any("3192-Y5-R2FR-solve-quadratic-profile-EL" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3192",
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
