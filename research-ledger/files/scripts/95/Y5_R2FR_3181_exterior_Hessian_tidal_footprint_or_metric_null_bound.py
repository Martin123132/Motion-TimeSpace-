from __future__ import annotations

import csv
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3181_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3181_EXTERIOR_HESSIAN_TIDAL_DERIVATION.csv"
METRIC_NULL = OUT / "P8_Y5_R2FR_3181_METRIC_NULL_GATE.csv"
TIDAL_BOUND = OUT / "P8_Y5_R2FR_3181_TIDAL_BOUND_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3181_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3181_VALIDATION.csv"

PRODUCT_RECAST_3180 = OUT / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"


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


def integrate_even_polynomial(coefficients: dict[int, Fraction]) -> Fraction:
    total = Fraction(0, 1)
    for power, coefficient in coefficients.items():
        if power % 2:
            raise ValueError(f"expected even power, got mu^{power}")
        total += coefficient / Fraction(power + 1, 1)
    return total


def derived_constants() -> dict[str, Fraction]:
    norm_average = Fraction(18, 1) * integrate_even_polynomial(
        {
            4: Fraction(45, 1),
            2: Fraction(-10, 1),
            0: Fraction(13, 1),
        }
    )
    yk_average = Fraction(3, 1) * integrate_even_polynomial(
        {
            4: Fraction(35, 1),
            2: Fraction(-30, 1),
            0: Fraction(3, 1),
        }
    )
    projection_coeff_square_average = Fraction(81, 4) * integrate_even_polynomial(
        {
            8: Fraction(1225, 1),
            6: Fraction(-2100, 1),
            4: Fraction(1110, 1),
            2: Fraction(-180, 1),
            0: Fraction(9, 1),
        }
    )
    return {
        "D2_C_r_minus_3": Fraction(2, 5) * 12 - 6 + Fraction(6, 5),
        "trace": Fraction(0, 1),
        "norm_average_constant": norm_average,
        "basis_projection_average_constant": yk_average,
        "basis_projection_coeff_square_average_constant": projection_coeff_square_average,
        "basis_projection_fraction_of_full_norm": projection_coeff_square_average / norm_average,
    }


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.md",
            "3180 handoff: projected moment closes conditionally, full tensor leakage remains open",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_DECISION.csv",
            "3180 decision table selecting exterior Hessian tidal footprint as next target",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv",
            "3180 scalar-projection product bound recast",
        ),
        (
            "post_checkpoint",
            "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.md",
            "3179 tracefree Hessian projection and full-tensor leakage warning",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3179_PURE_KERNEL_CONDITION.csv",
            "3179 pure R(r)Y condition",
        ),
        (
            "post_checkpoint",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "earlier Hessian carrier amplitude and metric-response warning",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent-v1 effective local equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3181_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    constants = derived_constants()
    return [
        {
            "derivation_id": "DER3181_0_exterior_potential",
            "object": "exterior_l2_harmonic_carrier",
            "statement": "Use axis a and mu=a.n with phi_ext=C r^-3 P2(mu).",
            "formula": "phi_ext=C(3z^2-r^2)/(2r^5) for a=z",
            "result": "source-free exterior carrier",
            "status": "SETUP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_1_projected_D2_zero",
            "object": "projected_source_operator",
            "statement": "The 3179 projected source operator vanishes on the exterior branch.",
            "formula": "D2[C r^-3]=(2/5)(12C r^-5)+2(-3C r^-4)/r+6(C r^-3)/(5r^2)=0",
            "result": str(constants["D2_C_r_minus_3"]),
            "status": "D2_ZERO_CONFIRMED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_2_nonzero_hessian",
            "object": "full_tracefree_hessian",
            "statement": "D2=0 does not imply the full exterior Hessian is zero.",
            "formula": "K_L^{ij}=2 partial_i partial_j phi_ext,  delta_ij K_L^{ij}=0",
            "result": "trace=" + str(constants["trace"]) + "; tensor norm nonzero",
            "status": "TRACEFREE_BUT_NONZERO",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_3_pointwise_norm",
            "object": "tidal_tensor_footprint",
            "statement": "With y=0, z=r mu, x=r sqrt(1-mu^2), the Euclidean tensor norm is a positive angular polynomial.",
            "formula": "K_L^{ij}K^L_{ij}=18 C^2 r^-10(45 mu^4 - 10 mu^2 + 13)",
            "result": "positive for all mu in [-1,1]",
            "status": "NONZERO_TIDAL_FOOTPRINT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_4_angular_average",
            "object": "rms_tidal_tensor",
            "statement": "The full exterior footprint has a fixed angular RMS.",
            "formula": "<K_L^{ij}K^L_{ij}>_Omega=336 C^2 r^-10",
            "result": "K_rms=4 sqrt(21)|C| r^-5",
            "numeric_constant": float(constants["norm_average_constant"]),
            "status": "RMS_FOOTPRINT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_5_basis_projection",
            "object": "constant_STF_basis_direction",
            "statement": "Projection onto Y_a^{ij}=a^i a^j-delta^{ij}/3 has zero angular mean but nonzero RMS.",
            "formula": "Y_a:K_L=3C r^-5(35 mu^4 - 30 mu^2 + 3);  <Y_a:K_L>_Omega=0",
            "result": "<P_Y[K_L]^2>_Omega=144 C^2 r^-10",
            "numeric_constant": float(constants["basis_projection_coeff_square_average_constant"]),
            "status": "ZERO_MEAN_NONZERO_RMS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "DER3181_6_projection_fraction",
            "object": "basis_projection_vs_full_norm",
            "statement": "The constant-STF-basis coefficient is only one slice of the full tensor footprint.",
            "formula": "<P_Y[K_L]^2>/<K_L:K_L>=144/336=3/7",
            "result": str(constants["basis_projection_fraction_of_full_norm"]),
            "numeric_constant": float(constants["basis_projection_fraction_of_full_norm"]),
            "status": "FULL_TENSOR_BOUND_STILL_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def metric_null_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "MN3181_0_D2_not_enough",
            "clause": "projected source silence",
            "required_for_zero_claim": "D2[C r^-3]=0 plus no public metric response to the remaining tracefree Hessian tensor",
            "current_evidence": "D2 zero is derived, but K_L^{ij}K^L_{ij} has nonzero RMS 336 C^2 r^-10",
            "status": "INSUFFICIENT_FOR_METRIC_NULL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MN3181_1_metric_readout",
            "clause": "public metric response",
            "required_for_zero_claim": "derive delta g_public[K_L_ext]=0 or classify K_L_ext as gauge/exact/improvement-silent in the parent action",
            "current_evidence": "no parent-owned metric-null theorem found in cited inputs",
            "status": "MISSING_METRIC_NULL_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MN3181_2_response_coefficient",
            "clause": "bounded nonzero route",
            "required_for_zero_claim": "if not null, provide source-owned response coefficient mu_tidal and local observable transfer kernel",
            "current_evidence": "mu_tidal, tau_tidal, and arena transfer kernel are not parent-owned",
            "status": "MISSING_TIDAL_RESPONSE_COEFFICIENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MN3181_3_scalar_bound_limitation",
            "clause": "3180 scalar recast",
            "required_for_zero_claim": "prove the scalar-projection product bound controls the full tensor tidal footprint",
            "current_evidence": "3180 only bounds the projected moment branch; 3181 shows a nonzero exterior tensor RMS",
            "status": "SCALAR_RECAST_DOES_NOT_CLOSE_FULL_TENSOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def tightest_3180_recast() -> dict[str, str]:
    rows = read_csv(PRODUCT_RECAST_3180)
    return min(rows, key=lambda row: float(row["recast_bound"]))


def tidal_bound_rows() -> list[dict[str, object]]:
    now = stamp()
    tightest = tightest_3180_recast()
    return [
        {
            "bound_id": "TB3181_0_surface_rms_template",
            "quantity": "surface_exterior_tidal_rms",
            "normal_form": "K_rms(x=1)=4 sqrt(21)|c_ext| in the same exterior coefficient normalization as 3180",
            "candidate_observable": "A_tidal_surface=4 sqrt(21)|s_K2*kappa_STF*c_ext*mu_tidal|",
            "required_bound": "|s_K2*kappa_STF*c_ext*mu_tidal| <= tau_tidal/(4 sqrt(21))",
            "missing_inputs": "mu_tidal;tau_tidal;arena_transfer_kernel;source_path",
            "status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "TB3181_1_radial_falloff_template",
            "quantity": "exterior_tidal_rms_at_x",
            "normal_form": "K_rms(x)=4 sqrt(21)|c_ext|x^-5",
            "candidate_observable": "A_tidal(x)=4 sqrt(21)|s_K2*kappa_STF*c_ext*mu_tidal|x^-5",
            "required_bound": "|s_K2*kappa_STF*c_ext*mu_tidal| <= tau_tidal(x)x^5/(4 sqrt(21))",
            "missing_inputs": "mu_tidal;tau_tidal(x);source_geometry;arena_transfer_kernel",
            "status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "TB3181_2_scalar_recast_carried_not_sufficient",
            "quantity": "scalar_projection_product_bound",
            "normal_form": "3180 tightest scalar-projection recast",
            "candidate_observable": tightest["recast_quantity"],
            "required_bound": tightest["recast_bound"],
            "missing_inputs": "proof that scalar projection controls full tensor response, or independent tensor norm bound",
            "source_row": tightest["recast_id"],
            "status": "CARRIED_BOUND_NOT_FULL_TENSOR_CLOSURE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3181_0_real_derivation",
            "finding": "The exterior l=2 Hessian branch is not harmless just because D2[C r^-3]=0.",
            "claim_status": "D2_ZERO_BUT_TIDAL_FOOTPRINT_NONZERO",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3181_1_quantified_footprint",
            "finding": "<K_L:K_L>_Omega=336 C^2 r^-10, so K_rms=4 sqrt(21)|C|r^-5.",
            "claim_status": "EXTERIOR_TIDAL_RMS_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3181_2_metric_null_needed",
            "finding": "A metric-null/improvement-silent theorem is now mandatory if the tracefree Hessian route is to preserve local GR without adding a tensor bound.",
            "claim_status": "MISSING_METRIC_NULL_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3181_3_bound_route",
            "finding": "If metric-null fails, the next valid route is a source-owned tidal response coefficient mu_tidal and arena bound tau_tidal.",
            "claim_status": "TIDAL_RESPONSE_BOUND_ROUTE_OPEN_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3181_4_next_target",
            "finding": "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        DERIVATION: derivation_rows(),
        METRIC_NULL: metric_null_rows(),
        TIDAL_BOUND: tidal_bound_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    derivation = rows_by_path[DERIVATION]
    metric_null = rows_by_path[METRIC_NULL]
    tidal_bound = rows_by_path[TIDAL_BOUND]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    constants = derived_constants()
    return [
        {
            "check_id": "VAL3181_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_1_D2_zero",
            "check": "exterior D2[C r^-3] vanishes exactly",
            "pass": str(constants["D2_C_r_minus_3"] == 0 and any(row["status"] == "D2_ZERO_CONFIRMED" for row in derivation)).lower(),
            "detail": "D2 constant=" + str(constants["D2_C_r_minus_3"]),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_2_nonzero_norm",
            "check": "full exterior Hessian footprint is nonzero and angular RMS constant is 336",
            "pass": str(constants["norm_average_constant"] == 336 and any(row["status"] == "RMS_FOOTPRINT_DERIVED" for row in derivation)).lower(),
            "detail": "<K:K>_Omega coefficient=" + str(constants["norm_average_constant"]),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_3_zero_mean_nonzero_basis_rms",
            "check": "constant STF basis projection has zero mean but nonzero RMS",
            "pass": str(constants["basis_projection_average_constant"] == 0 and constants["basis_projection_coeff_square_average_constant"] == 144).lower(),
            "detail": "mean=0; rms coefficient square=144",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_4_metric_null_still_blocked",
            "check": "metric-null gate remains blocked unless theorem or response coefficient exists",
            "pass": str(any(row["status"] == "MISSING_METRIC_NULL_THEOREM" for row in metric_null) and any(row["status"] == "MISSING_TIDAL_RESPONSE_COEFFICIENT" for row in metric_null)).lower(),
            "detail": "nonzero footprint requires null theorem or tensor bound",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_5_templates_nonclaim",
            "check": "all tidal bound rows are templates/nonclaims with missing inputs declared",
            "pass": str(all(row["valid_for_claim"] == "false" and row["missing_inputs"] for row in tidal_bound)).lower(),
            "detail": f"{len(tidal_bound)} bound/template rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_6_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3181_7_next_target_selected",
            "check": "decision table selects metric readout or tidal response coefficient as next target",
            "pass": str(any("3182-Y5-R2FR-metric-readout" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3182",
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
