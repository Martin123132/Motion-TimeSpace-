from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3179_INPUTS.csv"
PROJECTION = OUT / "P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv"
PURE_CONDITION = OUT / "P8_Y5_R2FR_3179_PURE_KERNEL_CONDITION.csv"
LEAKAGE_AUDIT = OUT / "P8_Y5_R2FR_3179_TRACEFREE_LEAKAGE_AUDIT.csv"
PRODUCT_CARRY = OUT / "P8_Y5_R2FR_3179_PRODUCT_BOUND_CARRY_FORWARD.csv"
DECISION = OUT / "P8_Y5_R2FR_3179_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3179_VALIDATION.csv"

PRODUCT_3178 = OUT / "P8_Y5_R2FR_3178_STF_PRODUCT_BOUND_GATE.csv"


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
            "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md",
            "3178 handoff: dimensionless R_K2 and product-bound gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3178_STF_PRODUCT_BOUND_GATE.csv",
            "3178 product-bound rows for |s_K2*kappa_STF*I4|",
        ),
        (
            "post_checkpoint",
            "3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090.md",
            "3176 STF angular basis normalization",
        ),
        (
            "post_checkpoint",
            "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md",
            "tracefree Hessian candidate and non-adoption guard",
        ),
        (
            "post_checkpoint",
            "1190-Y5-R10-P_loc-parent-domain-commutator-or-tracefree-Khat-solver-gate.md",
            "curved divergence, commutator, and boundary residuals",
        ),
        (
            "post_checkpoint",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "Hessian carrier amplitude law and metric-response warning",
        ),
        (
            "post_checkpoint",
            "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
            "tracefree improvement parent-origin route and missing coefficient/boundary",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent-v1 effective local equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3179_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def projection_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "projection_id": "HP3179_0_scalar_l2_setup",
            "object": "phi_l2",
            "statement": "Use the tracefree Hessian candidate on an axisymmetric scalar l=2 carrier.",
            "formula": "phi(r,n)=F(r)P2(a.n)=(3/2)F(r)Y_a^{kl}n_k n_l",
            "result": "the same Y_a basis from 3176 can be used",
            "status": "SETUP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "HP3179_1_auxiliary_B",
            "object": "B(r)",
            "statement": "Write phi as a quadratic Cartesian STF seed with a radial prefactor.",
            "formula": "phi=B(r)Y_a^{kl}x_kx_l, B(r):=(3/2)F(r)/r^2",
            "result": "radial variation of B is exactly the source of tensor-harmonic leakage",
            "status": "DERIVED_REWRITE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "HP3179_2_angular_average_projection",
            "object": "P_Y[K_L]",
            "statement": "The angular-averaged pure Y_a projection of the spatial tracefree Hessian candidate has a closed radial operator.",
            "formula": "P_Y[K_L]^{ij}=D2[F](r)Y_a^{ij}, D2[F]=(2/5)F''+2F'/r+6F/(5r^2)",
            "result": "candidate source kernel can be projected if K_L is adopted",
            "status": "DERIVED_AVERAGED_STF_PROJECTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "HP3179_3_harmonic_exterior_check",
            "object": "D2[F_ext]",
            "statement": "The operator vanishes for the source-free exterior l=2 profile.",
            "formula": "F_ext=C*r^-3 => D2[F_ext]=(2/5)*12C*r^-5+2*(-3C*r^-4)/r+6C*r^-3/(5r^2)=0",
            "result": "consistent with 3172 exterior source-free r^-3 branch",
            "status": "EXTERIOR_ZERO_CHECK_PASS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "HP3179_4_quadratic_core_check",
            "object": "D2[F_core]",
            "statement": "A quadratic l=2 core gives a pure constant Y_a kernel.",
            "formula": "F_core=A*r^2 => D2[F_core]=6A",
            "result": "pure source kernel is possible only in this special core-like profile",
            "status": "QUADRATIC_CORE_CHECK_PASS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def pure_condition_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "condition_id": "PK3179_0_full_Hessian_terms",
            "condition": "The full Hessian of B(r)Y_xx contains n_i n_j Y_nn, delta_ij Y_nn, n_i(Yn)_j+n_j(Yn)_i, and Y_ij pieces.",
            "formula": "partial_i partial_j[B Y_ab x_a x_b] = B'' n_i n_j S +(B'/r)(delta_ij-n_i n_j)S+2rB'[n_iY_j+n_jY_i]+2B Y_ij",
            "consequence": "unless B'=0, extra tensor-harmonic pieces accompany the pure Y_ij kernel",
            "status": "FULL_TENSOR_LEAKAGE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "condition_id": "PK3179_1_pure_Y_condition",
            "condition": "Pointwise pure R(r)Y_ij source form requires the derivative-generated tensor harmonics to vanish.",
            "formula": "B'(r)=0, hence B''(r)=0, equivalently d(F/r^2)/dr=0",
            "consequence": "F(r)=A r^2 on the region where the simple 3175 source ansatz is exact",
            "status": "PURE_KERNEL_CONDITION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "condition_id": "PK3179_2_compact_support_warning",
            "condition": "A compact source cannot be globally F=A r^2 and exterior F=C r^-3 without a transition/boundary layer.",
            "formula": "F=A r^2 in core, F=C r^-3 outside => transition layer contributes K_perp/boundary source unless parent-matched",
            "consequence": "the next target must own or bound the boundary-layer tensor leakage",
            "status": "BOUNDARY_LAYER_REQUIRED_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def leakage_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "leak_id": "LEAK3179_0_nonpure_tensor_harmonics",
            "quantity": "K_perp^{ij}",
            "definition": "full tracefree Hessian candidate minus its angular-averaged pure Y_a projection",
            "formula": "K_perp^{ij}:=K_L^{ij}-P_Y[K_L]^{ij}",
            "status": "MISSING_BOUND_OR_PARENT_ZERO",
            "feeds": "DeltaK_TF, q_K2^nu, PPN/preferred-frame/tidal comparator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "leak_id": "LEAK3179_1_parent_adoption",
            "quantity": "K_hat-K_L",
            "definition": "failure of formal K_L candidate to be live MTS K_hat",
            "formula": "DeltaK_TF^{ij}=K_hat^{<ij>}-K_L^{<ij>}+K_perp^{ij}",
            "status": "MISSING_LIVE_KHAT_ADOPTION",
            "feeds": "all local-GR/Newton/PPN claims",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "leak_id": "LEAK3179_2_metric_response",
            "quantity": "metric_footprint[K_L]",
            "definition": "metric response of the Hessian carrier even when divergence cancellation works",
            "formula": "||K_L||=sqrt(n/(n-1))||Gamma|| in flat carrier normalization",
            "status": "NO_PARAMETRIC_SUPPRESSION",
            "feeds": "Newton/PPN/clock/orbital bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def product_carry_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for source in read_csv(PRODUCT_3178):
        rows.append(
            {
                "carry_id": "CF3179_" + source["gate_id"],
                "bound_name": source["bound_name"],
                "known_bound_quantity": source["I4_form_quantity"],
                "known_bound": source["I4_form_bound"],
                "candidate_substitution": "I4[hat_R] -> integral_0^eta D2[hat_F](x) x^4 dx if K_L is parent-adopted and K_perp is zero/bounded",
                "candidate_formula": "|s_K2*kappa_STF*integral D2[hat_F]x^4dx| <= " + source["I4_form_bound"],
                "status": "CARRIED_FORWARD_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3179_0_main_result",
            "finding": "The tracefree Hessian candidate has a derived pure-Y projection D2[F]=(2/5)F''+2F'/r+6F/(5r^2).",
            "claim_status": "PROJECTION_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3179_1_important_catch",
            "finding": "The full Hessian is not generally a pure R(r)Y_ij source; pure form requires F/r^2 constant, so compact sources need a boundary-layer/leakage owner.",
            "claim_status": "PURE_KERNEL_NOT_GENERIC",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3179_2_route_status",
            "finding": "K_L remains a candidate only; without parent adoption and K_perp/DeltaK_TF bounds the route is a product-bound component, not local GR.",
            "claim_status": "DELTAKTF_BOUND_ROUTE_ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3179_3_next_target",
            "finding": "3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        PROJECTION: projection_rows(),
        PURE_CONDITION: pure_condition_rows(),
        LEAKAGE_AUDIT: leakage_rows(),
        PRODUCT_CARRY: product_carry_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    projection = rows_by_path[PROJECTION]
    pure = rows_by_path[PURE_CONDITION]
    leakage = rows_by_path[LEAKAGE_AUDIT]
    carry = rows_by_path[PRODUCT_CARRY]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    return [
        {
            "check_id": "VAL3179_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_1_projection_formula",
            "check": "D2[F] projection formula is present",
            "pass": str(any(row["projection_id"] == "HP3179_2_angular_average_projection" and "D2[F]" in row["formula"] for row in projection)).lower(),
            "detail": "D2[F]=(2/5)F''+2F'/r+6F/(5r^2)",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_2_exterior_zero",
            "check": "exterior r^-3 source-free check is present",
            "pass": str(any(row["status"] == "EXTERIOR_ZERO_CHECK_PASS" for row in projection)).lower(),
            "detail": "F=C*r^-3 gives D2=0",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_3_pure_kernel_condition",
            "check": "pure R(r)Y_ij condition is derived",
            "pass": str(any(row["status"] == "PURE_KERNEL_CONDITION_DERIVED" for row in pure)).lower(),
            "detail": "pure source form requires d(F/r^2)/dr=0",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_4_leakage_retained",
            "check": "K_perp and DeltaK_TF leakage rows remain nonclaim",
            "pass": str(all(row["valid_for_claim"] == "false" for row in leakage) and any(row["quantity"] == "K_perp^{ij}" for row in leakage)).lower(),
            "detail": "nonpure tensor harmonics are retained",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_5_product_carry_nonclaim",
            "check": "product bounds are carried forward as nonclaim rows",
            "pass": str(all(row["valid_for_claim"] == "false" for row in carry) and len(carry) == 3).lower(),
            "detail": f"{len(carry)} product rows carried forward",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_6_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3179_7_next_target_selected",
            "check": "decision table selects quadratic-core boundary-layer or DeltaKTF leakage bound",
            "pass": str(any("3180-Y5-R2FR-quadratic-core-boundary-layer" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3180",
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
