from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import sqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3183_INPUTS.csv"
NORMAL_FORM = OUT / "P8_Y5_R2FR_3183_SIGMA_NORMAL_FORM.csv"
ZERO_AUDIT = OUT / "P8_Y5_R2FR_3183_ZERO_THEOREM_AUDIT.csv"
J2_PRESSURE = OUT / "P8_Y5_R2FR_3183_J2_SLIP_PRESSURE_BOUNDS.csv"
BOUND_COMPARISON = OUT / "P8_Y5_R2FR_3183_SCALAR_RECAST_VS_SLIP_PRESSURE.csv"
DECISION = OUT / "P8_Y5_R2FR_3183_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3183_VALIDATION.csv"

J2_BOUNDS_3170 = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
RECAST_3180 = OUT / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"


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
            "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md",
            "3182 weak-field metric readout and slip response",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3182_WEAK_FIELD_READOUT_DERIVATION.csv",
            "3182 readout rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3182_SLIP_BOUND_TEMPLATE.csv",
            "3182 slip-bound template rows",
        ),
        (
            "post_checkpoint",
            "3181-Y5-R2FR-exterior-Hessian-tidal-footprint-or-metric-null-bound-under-AX1090.md",
            "3181 nonzero exterior Hessian footprint",
        ),
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 exterior coefficient and projected moment identity",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv",
            "3180 scalar-projection recast bound",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "3170 public solar-surface metric P2 pressure rows",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3183_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def normal_form_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "normal_id": "NF3183_0_notation_repair",
            "object": "lambda_H_vs_Sigma_H",
            "statement": "Separate the operator multiplier from the exterior slip amplitude so the 3182 notation cannot double-count C.",
            "formula": "K_L,ij[C]=2 partial_i partial_j(C x^-3 P2); G_ij=lambda_H K_L,ij[C]; Sigma_H:=lambda_H*C",
            "result": "Psi-Phi=2 Sigma_H x^-3 P2",
            "status": "CANONICAL_NORMAL_FORM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "normal_id": "NF3183_1_surface_amplitude",
            "object": "public_slip_P2_coefficient",
            "statement": "The surface-normalized P2 coefficient of the induced slip is twice the canonical Sigma_H amplitude.",
            "formula": "A_slip_surface=2|Sigma_H|",
            "result": "local metric pressure can bound Sigma_H directly if the slip-to-public-P2 map is signed",
            "numeric_coefficient": 2.0,
            "status": "SURFACE_SLIP_COEFFICIENT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "normal_id": "NF3183_2_surface_rms",
            "object": "surface_slip_rms",
            "statement": "The angular RMS form is equivalent to the P2 coefficient form.",
            "formula": "slip_rms_surface=(2/sqrt(5))|Sigma_H|",
            "result": "RMS coefficient 2/sqrt(5)",
            "numeric_coefficient": 2.0 / sqrt(5.0),
            "status": "RMS_NORMAL_FORM_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "normal_id": "NF3183_3_candidate_factorization",
            "object": "Sigma_H_candidate_factorization",
            "statement": "If the 3180 Hessian product branch and 3176 signed K2 basis are adopted in the same normalization, Sigma_H is proportional to the same exterior product.",
            "formula": "Sigma_H = chi_H * s_K2 * kappa_STF * c_ext",
            "result": "chi_H must be parent-owned before any numeric claim",
            "status": "FACTOR_MAP_CONDITIONAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def zero_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "zero_id": "ZT3183_0_lambda_zero",
            "zero_route": "lambda_H=0",
            "test": "Can the effective identity-readout branch make the Hessian carrier metric-null?",
            "finding": "No under 3182: G_ij^(1)=partial_i partial_j(Psi-Phi) reads the carrier as slip with coefficient 2.",
            "survives": "false",
            "status": "REJECTED_UNDER_IDENTITY_READOUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3183_1_parent_improvement_silence",
            "zero_route": "parent improvement or boundary silence",
            "test": "Can a closed parent action override identity readout and make the term improvement-only?",
            "finding": "Possible in principle, but no parent-signed improvement theorem exists in the cited inputs.",
            "survives": "conditional_open",
            "status": "MISSING_PARENT_IMPROVEMENT_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3183_2_c_ext_zero",
            "zero_route": "c_ext=0",
            "test": "Can the exterior coefficient vanish while keeping a nontrivial projected K2 source moment?",
            "finding": "No for the 3180 branch: I4_D2=-4c_ext/5 and M2_K2^proj=(4/25)kappa_STF c_ext, so c_ext=0 kills the projected branch.",
            "survives": "false_for_nontrivial_branch",
            "status": "ZERO_KILLS_PROJECTED_MOMENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3183_3_basis_or_coupling_zero",
            "zero_route": "s_K2=0 or kappa_STF=0",
            "test": "Can signed basis/coupling zero remove Sigma_H?",
            "finding": "It would remove the branch, but no parent-owned zero theorem for s_K2 or kappa_STF is present.",
            "survives": "conditional_open",
            "status": "MISSING_COUPLING_ZERO_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3183_4_angular_mean_zero",
            "zero_route": "angular mean cancellation",
            "test": "Can the zero angular mean of the constant-STF projection be used as local safety?",
            "finding": "No. 3181 gives zero mean but nonzero RMS, and local observables respond to anisotropic P2 amplitude, not only angular average.",
            "survives": "false",
            "status": "MEAN_ZERO_NOT_LOCAL_GR_ZERO",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3183_5_extra_sector_cancellation",
            "zero_route": "additional signed sector cancels slip",
            "test": "Can another sector cancel Psi-Phi exactly?",
            "finding": "Only with a parent-owned signed counterterm and symmetry/identity enforcing equality; otherwise it is fine tuning.",
            "survives": "conditional_open",
            "status": "MISSING_SIGNED_COUNTERSECTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def j2_pressure_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for source in read_csv(J2_BOUNDS_3170):
        metric_bound = float(source["A_metric_bound_surface"])
        sigma_bound = metric_bound / 2.0
        rows.append(
            {
                "pressure_id": "JP3183_" + source["bound_id"],
                "source_bound_id": source["bound_id"],
                "bound_name": source["bound_name"],
                "source_A_metric_bound_surface": f"{metric_bound:.15e}",
                "normal_form": "A_slip_surface=2|Sigma_H|",
                "conditional_sigma_bound": f"{sigma_bound:.15e}",
                "rms_equivalent": "slip_rms_surface=(2/sqrt(5))|Sigma_H| gives the same Sigma_H bound if tau_rms=A_metric/sqrt(5)",
                "required_for_claim": "signed slip-to-public-P2 transfer;source matching radius;parent normalization chi_H",
                "status": "J2_SLIP_PRESSURE_ONLY_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def comparison_rows() -> list[dict[str, object]]:
    now = stamp()
    pressure_by_name = {row["bound_name"]: row for row in j2_pressure_rows()}
    rows = []
    for recast in read_csv(RECAST_3180):
        pressure = pressure_by_name[recast["bound_name"]]
        sigma_pressure = float(pressure["conditional_sigma_bound"])
        scalar_recast = float(recast["recast_bound"])
        rows.append(
            {
                "comparison_id": "BC3183_" + recast["recast_id"],
                "bound_name": recast["bound_name"],
                "scalar_recast_quantity": recast["recast_quantity"],
                "scalar_recast_bound": f"{scalar_recast:.15e}",
                "slip_pressure_quantity": "|Sigma_H|",
                "slip_pressure_bound": f"{sigma_pressure:.15e}",
                "ratio_slip_pressure_to_scalar_recast": f"{sigma_pressure / scalar_recast:.15e}",
                "interpretation": "direct slip pressure would dominate scalar projected-moment recast if the normalizations are identified",
                "required_for_claim": "prove Sigma_H equals the scalar recast product in the same public metric normalization",
                "status": "NORMALIZATION_MISMATCH_BLOCKS_CLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    tightest = min(j2_pressure_rows(), key=lambda row: float(row["conditional_sigma_bound"]))
    return [
        {
            "decision_id": "DEC3183_0_normal_form_fixed",
            "finding": "Canonicalized the slip branch: Sigma_H=lambda_H*C and Psi-Phi=2 Sigma_H x^-3 P2.",
            "claim_status": "AMPLITUDE_NORMAL_FORM_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3183_1_zero_theorem_not_proven",
            "finding": "Under identity readout, lambda_H=0 is rejected; c_ext=0 kills the nontrivial projected branch; remaining zero routes require parent-owned improvement/coupling theorems.",
            "claim_status": "ZERO_THEOREM_OPEN_NOT_CLAIMED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3183_2_tightest_pressure",
            "finding": f"Tightest current J2-slip pressure is |Sigma_H| <= {tightest['conditional_sigma_bound']} from {tightest['bound_name']}, conditional/nonclaim.",
            "claim_status": "J2_SLIP_PRESSURE_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3183_3_next_target",
            "finding": "3184-Y5-R2FR-SigmaH-parent-owner-or-slip-bound-runner-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        NORMAL_FORM: normal_form_rows(),
        ZERO_AUDIT: zero_audit_rows(),
        J2_PRESSURE: j2_pressure_rows(),
        BOUND_COMPARISON: comparison_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    normal = rows_by_path[NORMAL_FORM]
    zero = rows_by_path[ZERO_AUDIT]
    pressure = rows_by_path[J2_PRESSURE]
    comparison = rows_by_path[BOUND_COMPARISON]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    tightest = min(pressure, key=lambda row: float(row["conditional_sigma_bound"]))
    return [
        {
            "check_id": "VAL3183_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_1_normal_form_present",
            "check": "Sigma_H normal form separates lambda_H and C",
            "pass": str(any(row["status"] == "CANONICAL_NORMAL_FORM" for row in normal)).lower(),
            "detail": "Psi-Phi=2 Sigma_H x^-3 P2",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_2_zero_routes_audited",
            "check": "zero theorem routes are audited and nonclaim",
            "pass": str(any(row["status"] == "REJECTED_UNDER_IDENTITY_READOUT" for row in zero) and any(row["status"] == "ZERO_KILLS_PROJECTED_MOMENT" for row in zero) and all(row["valid_for_claim"] == "false" for row in zero)).lower(),
            "detail": f"{len(zero)} zero-route rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_3_J2_pressure_numeric",
            "check": "J2-slip pressure rows are positive numeric nonclaim rows",
            "pass": str(len(pressure) == 3 and all(float(row["conditional_sigma_bound"]) > 0 and row["valid_for_claim"] == "false" for row in pressure)).lower(),
            "detail": f"tightest={tightest['conditional_sigma_bound']}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_4_comparison_numeric",
            "check": "scalar recast vs slip pressure comparison rows are numeric and nonclaim",
            "pass": str(len(comparison) == 3 and all(float(row["ratio_slip_pressure_to_scalar_recast"]) > 0 and row["valid_for_claim"] == "false" for row in comparison)).lower(),
            "detail": "normalization mismatch retained",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3183_6_next_target_selected",
            "check": "decision table selects SigmaH parent owner or slip-bound runner",
            "pass": str(any("3184-Y5-R2FR-SigmaH-parent-owner" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3184",
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
