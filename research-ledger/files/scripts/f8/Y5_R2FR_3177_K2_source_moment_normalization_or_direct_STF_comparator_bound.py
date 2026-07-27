from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3177_INPUTS.csv"
GREEN_DERIVATION = OUT / "P8_Y5_R2FR_3177_GREEN_SOURCE_MOMENT_DERIVATION.csv"
M2_CONTRACT = OUT / "P8_Y5_R2FR_3177_M2_NORMALIZATION_CONTRACT.csv"
PRODUCT_BOUND = OUT / "P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv"
COMPARATOR_TEMPLATE = OUT / "P8_Y5_R2FR_3177_DIRECT_STF_COMPARATOR_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3177_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3177_VALIDATION.csv"

BOUNDS_3170 = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"


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
            "3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090.md",
            "3176 handoff: exact P2 to STF angular lift and source-moment bottleneck",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3176_SOURCE_MOMENT_CONTRACT.csv",
            "3176 source-moment contract rows for s_K2, R_K2, M2_K2, q_K2",
        ),
        (
            "post_checkpoint",
            "3172-Y5-R2FR-public-metric-radial-Green-owner-or-J2-channel-closure-under-AX1090.md",
            "3172 exterior source-free l=2 radial profile f2(r)=b r^-3",
        ),
        (
            "post_checkpoint",
            "3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090.md",
            "3173 parent-action extractor Upsilon_J2 = -P_surf,l2 E_metric L_parent^-1 S_K2",
        ),
        (
            "post_checkpoint",
            "3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090.md",
            "3174 effective local operator L_eff and identity metric readout condition",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "3170 corrected solar-surface public metric amplitude bounds",
        ),
        (
            "post_checkpoint",
            "3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md",
            "3165 C_K2_unit value and local residual-vector gate form",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent-v1 local effective field equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3177_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def green_derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "derivation_id": "GRN3177_0_source_equation",
            "object": "scalar_l2_Green_problem",
            "statement": "Compress the effective STF metric response to the public scalar l=2 channel after the 3176 angular projection.",
            "formula": "nabla^2[u_2(r)P2(a.n)] = S_2(r)P2(a.n), with S_2(r)=kappa_STF*s_K2*C_K2_unit*R_K2(r)",
            "result": "all unknown tensor/operator/readout normalization is isolated in kappa_STF and R_K2",
            "status": "CONDITIONAL_PUBLIC_CHANNEL_REDUCTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GRN3177_1_radial_equation",
            "object": "l2_radial_operator",
            "statement": "For l=2 the radial Green equation is fixed by the Laplacian.",
            "formula": "(1/r^2)(r^2 u_2')' - 6*u_2/r^2 = S_2(r)",
            "result": "no fitted radial exponent is allowed in the public exterior channel",
            "status": "DERIVED_RADIAL_OPERATOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GRN3177_2_compact_source_moment",
            "object": "exterior_l2_moment",
            "statement": "For a compact source inside R_src and equation nabla^2 u=S, the asymptotically flat exterior l=2 coefficient is the r^4 source moment.",
            "formula": "u_2(r>R_src) = -(1/5) r^-3 integral_0^Rsrc S_2(r') r'^4 dr'",
            "result": "source-moment normalization is exact up to the sign convention of L_eff and kappa_STF",
            "status": "DERIVED_GREEN_MOMENT_FORM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GRN3177_3_surface_amplitude",
            "object": "M2_K2_surface",
            "statement": "At surface radius R_b, compress the source response into a dimensionless transfer coefficient M2_K2.",
            "formula": "A_surface = s_K2*C_K2_unit*M2_K2, with M2_K2 := -kappa_STF/(5 R_b^3) integral_0^Rsrc R_K2(r') r'^4 dr'",
            "result": "the empirical gate should bound the product s_K2*M2_K2 until M2_K2 is parent-owned",
            "status": "DERIVED_PRODUCT_GATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GRN3177_4_relation_to_3172",
            "object": "exterior_r_minus_3",
            "statement": "3177 supplies the source coefficient b for the 3172 exterior f2(r)=b r^-3 solution.",
            "formula": "b = -(1/5) s_K2*C_K2_unit*kappa_STF integral R_K2(r') r'^4 dr'",
            "result": "3172 radial profile plus 3176 STF basis now reduce the branch to source normalization",
            "status": "SOURCE_COEFFICIENT_FORM_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def m2_contract_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "M2C3177_0_operator_sign",
            "quantity": "kappa_STF",
            "required_form": "signed projection from delta K_hat_STF into the public l=2 scalar metric equation, including L_eff sign/readout convention",
            "current_status": "MISSING_PARENT_OPERATOR_PROJECTION",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "M2C3177_1_radial_kernel",
            "quantity": "R_K2(r)",
            "required_form": "parent-owned compact source profile with units such that kappa_STF*C_K2_unit*R_K2 enters the l=2 source equation",
            "current_status": "MISSING_PARENT_RADIAL_KERNEL",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "M2C3177_2_moment_integral",
            "quantity": "M2_K2",
            "required_form": "M2_K2 = -kappa_STF/(5 R_b^3) integral_0^Rsrc R_K2(r) r^4 dr",
            "current_status": "FORMULA_DERIVED_INPUTS_MISSING",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "M2C3177_3_signed_amplitude",
            "quantity": "s_K2",
            "required_form": "s_K2 = W_2 M_Lambda with sign convention tied to public P2/J2 convention",
            "current_status": "MISSING_SIGNED_PARENT_OWNER",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "M2C3177_4_product_gate",
            "quantity": "|s_K2*M2_K2|",
            "required_form": "|s_K2*M2_K2| <= A_metric_bound_surface/C_K2_unit",
            "current_status": "DIRECT_PRODUCT_BOUND_AVAILABLE_NONCLAIM",
            "blocks_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def product_bound_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for source in read_csv(BOUNDS_3170):
        a_bound = float(source["A_metric_bound_surface"])
        c_k2 = float(source["C_K2_unit"])
        product_bound = a_bound / c_k2
        rows.append(
            {
                "bound_id": "PB3177_" + source["bound_id"],
                "source_bound_id": source["bound_id"],
                "bound_name": source["bound_name"],
                "A_metric_bound_surface": f"{a_bound:.15e}",
                "C_K2_unit": f"{c_k2:.15e}",
                "derived_bound_quantity": "|s_K2*M2_K2|",
                "derived_product_bound": f"{product_bound:.15e}",
                "formula": "|s_K2*M2_K2| <= A_metric_bound_surface/C_K2_unit",
                "interpretation": "This is not a K2 pass; it is a bound on the signed amplitude times the unknown source moment.",
                "status": "PRODUCT_BOUND_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def comparator_template_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "template_id": "CMP3177_0_solar_J2_surface",
            "arena": "solar_surface_J2_metric",
            "observable": "A_surface,l2 public metric amplitude",
            "prediction": "A_surface_pred = s_K2*C_K2_unit*M2_K2",
            "gate": "|s_K2*M2_K2| <= A_surface_bound/C_K2_unit",
            "missing_inputs": "M2_K2 numeric/source-owned; sign(s_K2); convention match",
            "status": "BOUNDABLE_PRODUCT_NO_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "CMP3177_1_direct_STF_PPN",
            "arena": "PPN_clock_orbital_STF",
            "observable": "Delta_i in gamma, beta, preferred-frame, clock, orbit, or conservation channel",
            "prediction": "Delta_i = Pi_i,STF*C_K2_unit*s_K2*M2_K2 + exchange/source-balance terms",
            "gate": "|Delta_i| <= bound_i",
            "missing_inputs": "Pi_i,STF; M2_K2; q_K2^nu/exchange terms; empirical convention",
            "status": "COMPARATOR_TEMPLATE_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "CMP3177_2_conservation_guard",
            "arena": "Bianchi_Ward_source_balance",
            "observable": "q_K2^nu",
            "prediction": "q_K2^nu = -nabla_mu delta K_hat_STF^{mu nu} + trace/exchange companions",
            "gate": "q_K2^nu = 0 by parent theorem or ||q_K2|| <= local empirical residual bound",
            "missing_inputs": "parent exchange term or explicit residual bound",
            "status": "CONSERVATION_BLOCKS_LOCAL_GR_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3177_0_main_result",
            "finding": "The source moment has an exact Green-function form in the public l=2 channel: M2_K2 = -kappa_STF/(5 R_b^3) integral R_K2(r) r^4 dr.",
            "claim_status": "PARTIAL_DERIVATION_WIN_NOT_A_LOCAL_GR_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3177_1_empirical_use",
            "finding": "3170 solar-surface rows now bound the product |s_K2*M2_K2| directly; the tightest carried row is the half-range proxy, but all rows remain nonclaim.",
            "claim_status": "PRODUCT_BOUND_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3177_2_live_blocker",
            "finding": "The live missing objects are kappa_STF, R_K2(r), signed s_K2, and the q_K2 conservation/exchange closure.",
            "claim_status": "SOURCE_NORMALIZATION_AND_BALANCE_STILL_BLOCKED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3177_3_next_target",
            "finding": "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        GREEN_DERIVATION: green_derivation_rows(),
        M2_CONTRACT: m2_contract_rows(),
        PRODUCT_BOUND: product_bound_rows(),
        COMPARATOR_TEMPLATE: comparator_template_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    green = rows_by_path[GREEN_DERIVATION]
    m2 = rows_by_path[M2_CONTRACT]
    product = rows_by_path[PRODUCT_BOUND]
    comparator = rows_by_path[COMPARATOR_TEMPLATE]
    decision = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    numeric_product_ok = all(float(row["derived_product_bound"]) > 0 for row in product)
    return [
        {
            "check_id": "VAL3177_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_1_Green_moment_derived",
            "check": "derivation table includes compact l=2 source moment formula",
            "pass": str(any(row["derivation_id"] == "GRN3177_2_compact_source_moment" and row["status"] == "DERIVED_GREEN_MOMENT_FORM" for row in green)).lower(),
            "detail": "u2(r>Rsrc)=-(1/5)r^-3 integral S2 r^4 dr",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_2_M2_inputs_still_block_claim",
            "check": "M2 contract keeps kappa_STF, R_K2, and s_K2 blocking claims",
            "pass": str(all(row["valid_for_claim"] == "false" for row in m2) and any(row["quantity"] == "M2_K2" and row["blocks_claim"] == "true" for row in m2)).lower(),
            "detail": "M2 formula exists but parent inputs are not sourced",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_3_product_bounds_numeric_nonclaim",
            "check": "product bounds are positive numeric rows and remain nonclaim",
            "pass": str(numeric_product_ok and all(row["valid_for_claim"] == "false" for row in product)).lower(),
            "detail": f"{len(product)} product-bound rows generated",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_4_comparators_nonclaim",
            "check": "direct STF comparator templates remain nonclaim",
            "pass": str(all(row["valid_for_claim"] == "false" for row in comparator)).lower(),
            "detail": "PPN/clock/orbital/conservation comparators are templates only",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3177_6_next_target_selected",
            "check": "decision table selects Khat source-kernel normalization or STF product-bound gate",
            "pass": str(any("3178-Y5-R2FR-Khat-source-kernel-normalization" in row["finding"] for row in decision)).lower(),
            "detail": "next target is 3178",
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
