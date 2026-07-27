from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3178_INPUTS.csv"
EXTRACTION = OUT / "P8_Y5_R2FR_3178_KERNEL_EXTRACTION_DERIVATION.csv"
KHAT_AUDIT = OUT / "P8_Y5_R2FR_3178_TRACEFREE_KHAT_ROUTE_AUDIT.csv"
MOMENT_NORM = OUT / "P8_Y5_R2FR_3178_DIMENSIONLESS_MOMENT_NORMALIZATION.csv"
PRODUCT_GATE = OUT / "P8_Y5_R2FR_3178_STF_PRODUCT_BOUND_GATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3178_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3178_VALIDATION.csv"

PRODUCT_3177 = OUT / "P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv"


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
            "3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090.md",
            "3177 handoff: M2_K2 Green moment and product bound",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv",
            "3177 numeric nonclaim product bounds on |s_K2*M2_K2|",
        ),
        (
            "post_checkpoint",
            "3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090.md",
            "3176 exact P2 to STF angular lift",
        ),
        (
            "post_checkpoint",
            "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
            "tracefree Hessian/improvement route and missing Kmetric kernels",
        ),
        (
            "post_checkpoint",
            "2219-Y5-R2FR-Khat-source-definition-owner-or-DeltaKhat-component-fill.md",
            "Khat source owner audit: no live source-owned Khat tensor",
        ),
        (
            "post_checkpoint",
            "3066-Y5-R2FR-Khat-component-source-list-and-DeltaK-tensor-slot-fill-or-identity-proof-under-AX1090.md",
            "component source list: tracefree route retained but not adopted",
        ),
        (
            "post_checkpoint",
            "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md",
            "tracefree Khat birth certificate: exact formal route, not parent-signed",
        ),
        (
            "post_checkpoint",
            "1190-Y5-R10-P_loc-parent-domain-commutator-or-tracefree-Khat-solver-gate.md",
            "curved divergence and P_loc/boundary residual guards",
        ),
        (
            "post_checkpoint",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "flat Hessian carrier amplitude law and metric-response warning",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent-v1 effective local equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3178_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def extraction_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "derivation_id": "EXT3178_0_STF_projection_operator",
            "object": "R_K2 extractor",
            "statement": "Given the 3176 basis Y_a^{ij}, the source kernel is the Y_a projection of the Khat tracefree response.",
            "formula": "R_K2(r) := [Y_{a,ij} delta K_hat_STF^{ij}(r)] / [(3/2) s_K2 C_K2_unit (Y_a:Y_a)], with Y_a:Y_a=2/3",
            "result": "R_K2 becomes an extractable projection if delta K_hat_STF is parent-owned",
            "status": "EXTRACTION_FORMULA_DERIVED_PARENT_INPUT_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "EXT3178_1_tracefree_candidate_projection",
            "object": "tracefree_Hessian_candidate",
            "statement": "For the guarded K_L route, the same projection defines the candidate kernel but does not make it live Khat.",
            "formula": "R_K2^cand(r) := [Y_{a,ij} K_L^{ij}] / [(3/2) s_K2 C_K2_unit (Y_a:Y_a)], K_L^{mu nu}=2 nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi",
            "result": "candidate extraction exists; parent adoption remains false per 3067",
            "status": "CANDIDATE_ONLY_NOT_LIVE_KHAT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "EXT3178_2_units",
            "object": "source_kernel_units",
            "statement": "If C_K2_unit is a dimensionless public metric amplitude coefficient, the source kernel in nabla^2 u=S must carry L^-2.",
            "formula": "S_2(r)=kappa_STF*s_K2*C_K2_unit*R_K2(r); [S_2]=L^-2 so [R_K2]=L^-2 if kappa_STF is dimensionless",
            "result": "kernel unit debt is explicit",
            "status": "DIMENSIONAL_GATE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "EXT3178_3_dimensionless_kernel",
            "object": "hat_R_K2",
            "statement": "Use x=r/R_b to separate unknown shape from the required L^-2 source units.",
            "formula": "R_K2(r)=R_b^-2 * hat_R_K2(x), x:=r/R_b, eta:=R_src/R_b",
            "result": "M2_K2 reduces to a dimensionless fourth moment of hat_R_K2",
            "status": "DIMENSIONLESS_KERNEL_NORMALIZATION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def khat_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "KHA3178_0_live_owner",
            "route": "current live K_hat tensor",
            "evidence": "2219 and 3066 find no source-signed live K_hat component list",
            "impact_on_3178": "R_K2 cannot be promoted as parent-owned",
            "status": "LIVE_OWNER_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "KHA3178_1_tracefree_route",
            "route": "tracefree Hessian/improvement candidate",
            "evidence": "1525/3067 give K_L^{mu nu}=2 nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi and exact tracefree identity",
            "impact_on_3178": "candidate kernel extractor can be written but is not live MTS K_hat",
            "status": "FORMAL_CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "KHA3178_2_curved_residuals",
            "route": "curved/local branch",
            "evidence": "1190 retains Ricci leakage, projector commutator, and boundary flux",
            "impact_on_3178": "even a candidate R_K2 needs q_K2/source-balance residual rows",
            "status": "CURVED_BOUNDARY_RESIDUALS_RETAINED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "KHA3178_3_amplitude_warning",
            "route": "Hessian carrier amplitude",
            "evidence": "833 derives ||K||=sqrt(n/(n-1))||Gamma|| in the flat carrier normalization",
            "impact_on_3178": "no automatic metric safety; product bounds must remain active",
            "status": "NO_PARAMETRIC_SUPPRESSION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def moment_norm_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "norm_id": "MOM3178_0_general",
            "kernel_family": "general_parent_kernel",
            "assumption": "R_K2(r)=R_b^-2 hat_R_K2(x), x=r/R_b, eta=R_src/R_b",
            "dimensionless_moment": "I4[hat_R] := integral_0^eta hat_R_K2(x) x^4 dx",
            "M2_formula": "M2_K2 = -(kappa_STF/5) I4[hat_R]",
            "claim_status": "DERIVED_NORMALIZATION_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "norm_id": "MOM3178_1_unit_moment",
            "kernel_family": "unit_fourth_moment_kernel",
            "assumption": "I4[hat_R]=1 by normalization convention only",
            "dimensionless_moment": "I4=1",
            "M2_formula": "M2_K2 = -kappa_STF/5",
            "claim_status": "CONVENTION_ONLY_NOT_PARENT_PROOF",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "norm_id": "MOM3178_2_surface_normalized",
            "kernel_family": "surface_amplitude_normalized_kernel",
            "assumption": "choose I4[hat_R]=-5/kappa_STF so M2_K2=1",
            "dimensionless_moment": "I4=-5/kappa_STF",
            "M2_formula": "M2_K2 = 1",
            "claim_status": "REJECT_AS_PHYSICS_CLAIM_NORMALIZATION_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "norm_id": "MOM3178_3_constant_compact",
            "kernel_family": "constant_inside_eta",
            "assumption": "hat_R_K2(x)=A0 for 0<=x<=eta and 0 outside",
            "dimensionless_moment": "I4=A0*eta^5/5",
            "M2_formula": "M2_K2 = -kappa_STF*A0*eta^5/25",
            "claim_status": "TOY_KERNEL_ONLY_NOT_PARENT_OWNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def product_gate_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for source in read_csv(PRODUCT_3177):
        product_bound = float(source["derived_product_bound"])
        rows.append(
            {
                "gate_id": "PG3178_" + source["source_bound_id"],
                "source_3177_bound": source["bound_id"],
                "bound_name": source["bound_name"],
                "known_bound": f"{product_bound:.15e}",
                "known_bound_quantity": "|s_K2*M2_K2|",
                "I4_form_bound": f"{5.0 * product_bound:.15e}",
                "I4_form_quantity": "|s_K2*kappa_STF*I4[hat_R]|",
                "unit_moment_bound": f"{5.0 * product_bound:.15e}",
                "unit_moment_quantity": "|s_K2*kappa_STF| if I4=1",
                "surface_normalized_bound": f"{product_bound:.15e}",
                "surface_normalized_quantity": "|s_K2| if M2_K2=1 by convention",
                "status": "STF_PRODUCT_BOUND_GATE_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3178_0_main_result",
            "finding": "No parent-owned Khat source kernel is found; the tracefree Hessian route remains the best candidate but is not live Khat.",
            "claim_status": "KERNEL_OWNER_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3178_1_progress",
            "finding": "R_K2 is now dimensionally normalized: R_K2=R_b^-2 hat_R_K2 and M2_K2=-(kappa_STF/5)I4[hat_R].",
            "claim_status": "NORMALIZATION_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3178_2_empirical_gate",
            "finding": "3177 product bounds now also bound |s_K2*kappa_STF*I4| via |s*kappa*I4| <= 5*B_product.",
            "claim_status": "PRODUCT_GATE_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3178_3_next_target",
            "finding": "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        EXTRACTION: extraction_rows(),
        KHAT_AUDIT: khat_audit_rows(),
        MOMENT_NORM: moment_norm_rows(),
        PRODUCT_GATE: product_gate_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    extraction = rows_by_path[EXTRACTION]
    audit = rows_by_path[KHAT_AUDIT]
    moments = rows_by_path[MOMENT_NORM]
    gates = rows_by_path[PRODUCT_GATE]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    gate_bounds_positive = all(float(row["known_bound"]) > 0 and float(row["I4_form_bound"]) > 0 for row in gates)
    return [
        {
            "check_id": "VAL3178_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_1_extractor_written",
            "check": "R_K2 extractor row is present",
            "pass": str(any(row["derivation_id"] == "EXT3178_0_STF_projection_operator" for row in extraction)).lower(),
            "detail": "Y_a projection of delta K_hat_STF defines R_K2 if parent-owned",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_2_live_Khat_not_promoted",
            "check": "Khat audit keeps live owner missing and tracefree route nonclaim",
            "pass": str(any(row["status"] == "LIVE_OWNER_MISSING" for row in audit) and any(row["status"] == "FORMAL_CANDIDATE_NOT_PARENT_SIGNED" for row in audit)).lower(),
            "detail": "no live source-owned Khat kernel is promoted",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_3_dimensionless_moment",
            "check": "dimensionless source-moment normalization is present",
            "pass": str(any(row["norm_id"] == "MOM3178_0_general" and "I4" in row["dimensionless_moment"] for row in moments)).lower(),
            "detail": "M2_K2=-(kappa_STF/5)I4[hat_R]",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_4_product_gate_numeric_nonclaim",
            "check": "STF product gate rows are positive numeric nonclaim rows",
            "pass": str(gate_bounds_positive and all(row["valid_for_claim"] == "false" for row in gates)).lower(),
            "detail": f"{len(gates)} product gates generated",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3178_6_next_target_selected",
            "check": "decision table selects tracefree Hessian K2 kernel projection or DeltaKTF bound",
            "pass": str(any("3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3179",
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
