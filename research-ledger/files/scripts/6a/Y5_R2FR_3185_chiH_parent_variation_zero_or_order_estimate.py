from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3185_INPUTS.csv"
CHIH_DERIVATION = OUT / "P8_Y5_R2FR_3185_CHIH_ORDER_DERIVATION.csv"
SATURATION = OUT / "P8_Y5_R2FR_3185_NATURAL_CHIH_SATURATION_CHECK.csv"
PARENT_STATUS = OUT / "P8_Y5_R2FR_3185_PARENT_VARIATION_STATUS.csv"
DECISION = OUT / "P8_Y5_R2FR_3185_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3185_VALIDATION.csv"

J2_BOUNDS_3170 = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
RECAST_3180 = OUT / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"
RUNNER_3184 = OUT / "P8_Y5_R2FR_3184_SIGMAH_SLIP_BOUND_RUNNER.csv"


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


def natural_chih() -> float:
    return 2.0 * c_k2_unit() / 25.0


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3184-Y5-R2FR-SigmaH-parent-owner-or-slip-bound-runner-under-AX1090.md",
            "3184 chi_H suppression target and runner",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3184_SIGMAH_SLIP_BOUND_RUNNER.csv",
            "3184 slip-bound runner rows",
        ),
        (
            "post_checkpoint",
            "3183-Y5-R2FR-Hessian-slip-amplitude-zero-theorem-or-J2-PPN-bound-under-AX1090.md",
            "3183 Sigma_H normal form",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 M2_K2 projected moment formula",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv",
            "3180 scalar product recast rows",
        ),
        (
            "post_checkpoint",
            "3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090.md",
            "3177 public amplitude relation Upsilon_J2=s_K2*C_K2_unit*M2_K2",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "3170 C_K2_unit and public surface P2 bounds",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3185_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def chih_derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    cunit = c_k2_unit()
    chi = natural_chih()
    return [
        {
            "derivation_id": "CHI3185_0_metric_unit",
            "object": "C_K2_unit",
            "statement": "The public metric amplitude unit carried by the K2 lane is already tiny.",
            "formula": "A_metric = C_K2_unit * s_K2 * M2_K2",
            "result": f"C_K2_unit={cunit:.15e}",
            "status": "CARRIED_FROM_3170_3177",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "CHI3185_1_projected_moment",
            "object": "P_H_to_M2",
            "statement": "3180 gives the projected Hessian moment in terms of the exterior product.",
            "formula": "P_H:=s_K2*kappa_STF*c_ext;  s_K2*M2_K2^proj=(4/25)P_H",
            "result": "projection factor 4/25",
            "status": "CARRIED_FROM_3180",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "CHI3185_2_public_metric_amplitude",
            "object": "P_H_to_A_metric",
            "statement": "Combining the 3177 public metric unit and 3180 projected moment maps P_H into a public P2 metric amplitude.",
            "formula": "A_metric(P_H)=C_K2_unit*(4/25)P_H",
            "result": f"A_metric coefficient={(4.0 * cunit / 25.0):.15e}",
            "status": "CONDITIONAL_PUBLIC_AMPLITUDE_MAP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "CHI3185_3_slip_amplitude_match",
            "object": "chi_H_natural",
            "statement": "3183 uses A_slip_surface=2|Sigma_H|. If the slip P2 amplitude is compared to the same public P2 metric amplitude, the natural chi_H is fixed.",
            "formula": "2 Sigma_H=A_metric(P_H)=(4/25)C_K2_unit P_H, so Sigma_H=(2/25)C_K2_unit P_H",
            "result": f"chi_H_natural=2*C_K2_unit/25={chi:.15e}",
            "status": "NATURAL_CHIH_ORDER_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "CHI3185_4_not_fine_tuning",
            "object": "3184_suppression_interpretation",
            "statement": "The 3184 10^-25 suppression target is exactly the metric-unit/projection factor, not an independent tuning demand, under the same-normalization map.",
            "formula": "chi_H_required=(A/2)/[(25/4)A/C_K2_unit]=2*C_K2_unit/25",
            "result": f"required_ratio={chi:.15e}",
            "status": "SUPPRESSION_TARGET_EXPLAINED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def saturation_rows() -> list[dict[str, object]]:
    now = stamp()
    chi = natural_chih()
    rows = []
    for runner in read_csv(RUNNER_3184):
        p_ceiling = float(runner["P_H_available_ceiling"])
        sigma_pressure = float(runner["Sigma_H_slip_pressure"])
        sigma_pred = chi * p_ceiling
        rows.append(
            {
                "sat_id": "SAT3185_" + runner["run_id"],
                "bound_name": runner["bound_name"],
                "P_H_available_ceiling": f"{p_ceiling:.15e}",
                "chi_H_natural": f"{chi:.15e}",
                "Sigma_H_predicted_if_P_H_saturates": f"{sigma_pred:.15e}",
                "Sigma_H_slip_pressure": f"{sigma_pressure:.15e}",
                "predicted_to_pressure_ratio": f"{sigma_pred / sigma_pressure:.15e}",
                "interpretation": "natural chi_H exactly saturates the pressure inherited from the same source row",
                "status": "SATURATES_IF_SCALAR_CEILING_SATURATES",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def parent_status_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "status_id": "PV3185_0_zero_theorem",
            "question": "Is chi_H zero?",
            "answer": "No zero theorem is derived here; the natural same-normalization estimate is nonzero.",
            "blocking_assumption": "closed parent improvement/boundary silence remains unsigned",
            "status": "ZERO_THEOREM_NOT_PROVEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "PV3185_1_order_estimate",
            "question": "Is chi_H order unity?",
            "answer": "No. Under the 3177/3180/3183 same-normalization chain it is order C_K2_unit, specifically 2*C_K2_unit/25.",
            "blocking_assumption": "requires K_L parent adoption, public P2 slip transfer, and no extra hidden-frame/coframe remapping",
            "status": "ORDER_ESTIMATE_AVAILABLE_CONDITIONAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "PV3185_2_local_GR_implication",
            "question": "Does this prove local GR?",
            "answer": "No. Natural chi_H only says the apparent 10^-25 gap is the known metric normalization; actual safety still depends on P_H not saturating pressure, or on a zero/improvement theorem.",
            "blocking_assumption": "source-owned P_H, slip-to-observable transfer, and local-test covariance are still missing",
            "status": "LOCAL_GR_STILL_BOUND_OR_ZERO_GATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "PV3185_3_next_live_object",
            "question": "What is now the live object?",
            "answer": "P_H and the slip observable transfer, not a mysterious order-one chi_H.",
            "blocking_assumption": "derive source-owned P_H or a stricter arena transfer bound",
            "status": "NEXT_OBJECT_PH_OR_TRANSFER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    chi = natural_chih()
    return [
        {
            "decision_id": "DEC3185_0_chiH_order_estimate",
            "finding": f"Conditional same-normalization chain gives chi_H_natural=2*C_K2_unit/25={chi:.15e}.",
            "claim_status": "CHIH_ORDER_DERIVED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3185_1_gap_explained",
            "finding": "The 3184 ~10^-25 suppression target is exactly the metric-unit/projection factor, not a separate fine-tuning, if the 3177/3180/3183 normalizations are identified.",
            "claim_status": "APPARENT_SUPPRESSION_EXPLAINED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3185_2_local_GR_not_closed",
            "finding": "Natural chi_H would saturate the inherited pressure if P_H saturates the scalar ceiling, so local GR still requires source-owned P_H below pressure or a true zero/improvement theorem.",
            "claim_status": "LOCAL_GR_REMAINS_BOUND_OR_ZERO_GATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3185_3_next_target",
            "finding": "3186-Y5-R2FR-source-owned-PH-amplitude-or-slip-transfer-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        CHIH_DERIVATION: chih_derivation_rows(),
        SATURATION: saturation_rows(),
        PARENT_STATUS: parent_status_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    derivation = rows_by_path[CHIH_DERIVATION]
    saturation = rows_by_path[SATURATION]
    parent_status = rows_by_path[PARENT_STATUS]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    chi = natural_chih()
    cunit = c_k2_unit()
    all_saturate = all(
        isclose(float(row["predicted_to_pressure_ratio"]), 1.0, rel_tol=1e-12, abs_tol=1e-12)
        for row in saturation
    )
    return [
        {
            "check_id": "VAL3185_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3185_1_chiH_formula",
            "check": "natural chi_H equals 2*C_K2_unit/25",
            "pass": str(isclose(chi, 2.0 * cunit / 25.0, rel_tol=0.0, abs_tol=0.0) and any(row["status"] == "NATURAL_CHIH_ORDER_DERIVED" for row in derivation)).lower(),
            "detail": f"chi_H_natural={chi:.15e}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3185_2_saturation_identity",
            "check": "natural chi_H saturates each inherited pressure row if P_H saturates scalar ceiling",
            "pass": str(len(saturation) == 3 and all_saturate).lower(),
            "detail": "; ".join(row["predicted_to_pressure_ratio"] for row in saturation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3185_3_parent_status_nonclaim",
            "check": "parent status keeps zero theorem and local GR unclaimed",
            "pass": str(any(row["status"] == "ZERO_THEOREM_NOT_PROVEN" for row in parent_status) and any(row["status"] == "LOCAL_GR_STILL_BOUND_OR_ZERO_GATED" for row in parent_status)).lower(),
            "detail": f"{len(parent_status)} status rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3185_4_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3185_5_next_target_selected",
            "check": "decision table selects source-owned P_H or slip-transfer bound",
            "pass": str(any("3186-Y5-R2FR-source-owned-PH-amplitude" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3186",
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
