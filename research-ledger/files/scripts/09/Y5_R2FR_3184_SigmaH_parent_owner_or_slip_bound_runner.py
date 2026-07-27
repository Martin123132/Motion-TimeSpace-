from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3184_INPUTS.csv"
OWNER_LEDGER = OUT / "P8_Y5_R2FR_3184_SIGMAH_PARENT_OWNER_LEDGER.csv"
BOUND_RUNNER = OUT / "P8_Y5_R2FR_3184_SIGMAH_SLIP_BOUND_RUNNER.csv"
SUPPRESSION = OUT / "P8_Y5_R2FR_3184_CHIH_SUPPRESSION_REQUIREMENT.csv"
DECISION = OUT / "P8_Y5_R2FR_3184_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3184_VALIDATION.csv"

PRESSURE_3183 = OUT / "P8_Y5_R2FR_3183_J2_SLIP_PRESSURE_BOUNDS.csv"
COMPARISON_3183 = OUT / "P8_Y5_R2FR_3183_SCALAR_RECAST_VS_SLIP_PRESSURE.csv"
ZERO_AUDIT_3183 = OUT / "P8_Y5_R2FR_3183_ZERO_THEOREM_AUDIT.csv"


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
            "3183-Y5-R2FR-Hessian-slip-amplitude-zero-theorem-or-J2-PPN-bound-under-AX1090.md",
            "3183 Sigma_H normal form, zero audit, and slip pressure",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3183_SIGMA_NORMAL_FORM.csv",
            "canonical Sigma_H=lambda_H*C normal form",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3183_J2_SLIP_PRESSURE_BOUNDS.csv",
            "J2 slip pressure rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3183_SCALAR_RECAST_VS_SLIP_PRESSURE.csv",
            "scalar recast versus slip pressure comparison",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3183_ZERO_THEOREM_AUDIT.csv",
            "zero route audit",
        ),
        (
            "post_checkpoint",
            "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md",
            "weak-field public metric readout",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "projected moment identity and scalar product recast context",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3184_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def owner_ledger_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "owner_id": "OWN3184_0_SigmaH",
            "symbol": "Sigma_H",
            "definition": "canonical exterior public-slip amplitude, Sigma_H=lambda_H*c_ext",
            "current_owner": "3183 normal form only",
            "needed_owner": "parent action/coframe/source matching derivation",
            "status": "NOT_PARENT_OWNED",
            "claim_effect": "cannot claim local-GR pass or numerical bound without owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "owner_id": "OWN3184_1_chiH",
            "symbol": "chi_H",
            "definition": "normalization map in Sigma_H=chi_H*s_K2*kappa_STF*c_ext",
            "current_owner": "introduced as conditional map in 3183",
            "needed_owner": "variation of parent action to public metric plus source-domain matching",
            "status": "MISSING_PARENT_NORMALIZATION",
            "claim_effect": "dominant live bottleneck after 3183",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "owner_id": "OWN3184_2_product",
            "symbol": "P_H := s_K2*kappa_STF*c_ext",
            "definition": "candidate scalar product inherited from 3180 recast",
            "current_owner": "conditional projected-Hessian branch",
            "needed_owner": "prove same normalization as public slip or supply a different map",
            "status": "CONDITIONAL_PRODUCT_ONLY",
            "claim_effect": "scalar recast cannot be used as local-GR safety by itself",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "owner_id": "OWN3184_3_zero_theorem",
            "symbol": "Sigma_H=0",
            "definition": "exact absence of induced public slip",
            "current_owner": "not proved; identity readout rejects lambda_H=0 unless parent improvement overrides it",
            "needed_owner": "closed parent improvement/boundary theorem or exact coupling/source zero",
            "status": "ZERO_THEOREM_MISSING",
            "claim_effect": "local branch remains zero-or-bound, not derived local GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def pressure_by_bound_name() -> dict[str, dict[str, str]]:
    return {row["bound_name"]: row for row in read_csv(PRESSURE_3183)}


def bound_runner_rows() -> list[dict[str, object]]:
    now = stamp()
    pressures = pressure_by_bound_name()
    rows = []
    for comparison in read_csv(COMPARISON_3183):
        pressure = pressures[comparison["bound_name"]]
        sigma_bound = float(pressure["conditional_sigma_bound"])
        scalar_ceiling = float(comparison["scalar_recast_bound"])
        rows.append(
            {
                "run_id": "RUN3184_" + comparison["comparison_id"],
                "bound_name": comparison["bound_name"],
                "assumed_factorization": "Sigma_H=chi_H*P_H, P_H=s_K2*kappa_STF*c_ext",
                "P_H_available_ceiling": f"{scalar_ceiling:.15e}",
                "Sigma_H_slip_pressure": f"{sigma_bound:.15e}",
                "required_condition": "|chi_H*P_H| <= Sigma_H_slip_pressure",
                "if_P_H_saturates_current_ceiling_then_chi_H_abs_max": f"{sigma_bound / scalar_ceiling:.15e}",
                "if_chi_H_equals_1_then_P_H_abs_max": f"{sigma_bound:.15e}",
                "status_if_chi_H_order_one_and_P_H_unbounded": "FAILS_PRESSURE_IF_NORMALIZATION_MATCHES",
                "claim_status": "RUNNER_ONLY_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def suppression_rows() -> list[dict[str, object]]:
    now = stamp()
    runner = bound_runner_rows()
    tightest = min(runner, key=lambda row: float(row["if_P_H_saturates_current_ceiling_then_chi_H_abs_max"]))
    loosest = max(runner, key=lambda row: float(row["if_P_H_saturates_current_ceiling_then_chi_H_abs_max"]))
    return [
        {
            "suppression_id": "SUP3184_0_tightest_chiH",
            "statement": "If the current scalar product ceiling can be saturated and its normalization is identified with public slip, chi_H must be extremely suppressed.",
            "quantity": "|chi_H|",
            "required_bound": tightest["if_P_H_saturates_current_ceiling_then_chi_H_abs_max"],
            "source_bound_name": tightest["bound_name"],
            "interpretation": "parent normalization must be exact-zero or about 25 orders below unity in this worst-case mapping",
            "status": "SUPPRESSION_REQUIREMENT_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "suppression_id": "SUP3184_1_range_chiH",
            "statement": "All current pressure rows give the same chi_H-to-scalar-ceiling ratio because both used the same source amplitude rows.",
            "quantity": "ratio range",
            "required_bound": f"{float(tightest['if_P_H_saturates_current_ceiling_then_chi_H_abs_max']):.15e} to {float(loosest['if_P_H_saturates_current_ceiling_then_chi_H_abs_max']):.15e}",
            "source_bound_name": "all 3170 pressure rows",
            "interpretation": "stable ratio across adopted/current proxy rows; still normalization-gated",
            "status": "RATIO_STABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "suppression_id": "SUP3184_2_required_parent_deliverable",
            "statement": "The next derivation must decide whether chi_H is exactly zero, parametrically suppressed, or order unity.",
            "quantity": "parent deliverable",
            "required_bound": "derive chi_H=0 or prove |chi_H*P_H|<=Sigma_H_slip_pressure",
            "source_bound_name": "3183/3184 slip runner",
            "interpretation": "this is the concrete local-GR gate for the Hessian-slip route",
            "status": "NEXT_DERIVATION_CONTRACT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    tightest = min(bound_runner_rows(), key=lambda row: float(row["if_P_H_saturates_current_ceiling_then_chi_H_abs_max"]))
    return [
        {
            "decision_id": "DEC3184_0_runner_built",
            "finding": "Built Sigma_H slip-bound runner: |chi_H*P_H| must stay below the 3183 J2-slip pressure.",
            "claim_status": "BOUND_RUNNER_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3184_1_chiH_target",
            "finding": f"If P_H saturates the current scalar ceiling, |chi_H| must be <= {tightest['if_P_H_saturates_current_ceiling_then_chi_H_abs_max']} for {tightest['bound_name']}.",
            "claim_status": "PARENT_SUPPRESSION_TARGET_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3184_2_local_GR_gate",
            "finding": "The Hessian-slip branch now needs chi_H=0 by parent theorem, or a source-owned finite P_H small enough to pass slip bounds.",
            "claim_status": "LOCAL_GR_GATE_SHARPENED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3184_3_next_target",
            "finding": "3185-Y5-R2FR-chiH-parent-variation-zero-or-order-estimate-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        OWNER_LEDGER: owner_ledger_rows(),
        BOUND_RUNNER: bound_runner_rows(),
        SUPPRESSION: suppression_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    owners = rows_by_path[OWNER_LEDGER]
    runner = rows_by_path[BOUND_RUNNER]
    suppression = rows_by_path[SUPPRESSION]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    return [
        {
            "check_id": "VAL3184_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3184_1_owner_ledger_blocks_claim",
            "check": "owner ledger records missing parent normalization and zero theorem",
            "pass": str(any(row["status"] == "MISSING_PARENT_NORMALIZATION" for row in owners) and any(row["status"] == "ZERO_THEOREM_MISSING" for row in owners)).lower(),
            "detail": f"{len(owners)} owner rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3184_2_runner_numeric",
            "check": "bound runner rows are positive numeric nonclaim rows",
            "pass": str(len(runner) == 3 and all(float(row["if_P_H_saturates_current_ceiling_then_chi_H_abs_max"]) > 0 and row["valid_for_claim"] == "false" for row in runner)).lower(),
            "detail": f"{len(runner)} runner rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3184_3_suppression_contract",
            "check": "suppression requirement and next derivation contract are present",
            "pass": str(any(row["status"] == "SUPPRESSION_REQUIREMENT_DERIVED_NONCLAIM" for row in suppression) and any(row["status"] == "NEXT_DERIVATION_CONTRACT" for row in suppression)).lower(),
            "detail": "chi_H zero/suppression contract recorded",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3184_4_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3184_5_next_target_selected",
            "check": "decision table selects chi_H parent variation zero or order estimate",
            "pass": str(any("3185-Y5-R2FR-chiH-parent-variation-zero" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3185",
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
