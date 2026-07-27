from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3176_INPUTS.csv"
BASIS = OUT / "P8_Y5_R2FR_3176_STF_BASIS_DERIVATION.csv"
SIGNED_AUDIT = OUT / "P8_Y5_R2FR_3176_SIGNED_AMPLITUDE_AUDIT.csv"
SOURCE_CONTRACT = OUT / "P8_Y5_R2FR_3176_SOURCE_MOMENT_CONTRACT.csv"
BOUND_TEMPLATE = OUT / "P8_Y5_R2FR_3176_BOUND_ROW_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3176_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3176_VALIDATION.csv"


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
            "3175-Y5-R2FR-K2-STF-source-tensor-in-Khat-or-source-backed-bound-row-under-AX1090.md",
            "3175 handoff: K2 scalar magnitude cannot instantiate S_K2_STF",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3175_STF_SOURCE_CONTRACT.csv",
            "3175 contract rows for signed amplitude, STF basis, radial kernel, Khat embedding, conservation",
        ),
        (
            "post_checkpoint",
            "3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090.md",
            "3164 l=2 boundary lane e2 := P2(cos theta), W2 sensitivity, K2 := |W2 M_Lambda|",
        ),
        (
            "post_checkpoint",
            "3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md",
            "3165 C_K2_unit and residual-vector gate shape",
        ),
        (
            "post_checkpoint",
            "3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md",
            "3159 public J2/P2 convention and weak-field metric projection coefficient",
        ),
        (
            "post_checkpoint",
            "3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090.md",
            "3173 exact extractor Upsilon_J2 = -P_surf,l2 E_metric L_parent^-1 S_K2",
        ),
        (
            "post_checkpoint",
            "3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090.md",
            "3174 conditional effective operator and live S_K2 bottleneck",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent effective scaffold and K_MTS trace/tensor split",
        ),
        (
            "formalization",
            "133-exact-transition-cancellation-or-projector-theorem.md",
            "guardrail: Khat cancellation/projector theorem not closed",
        ),
    ]
    return [
        {
            "input_id": f"IN3176_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def basis_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "basis_id": "BAS3176_0_axis_definition",
            "object": "axisymmetric_l2_axis",
            "statement": "The 3164 boundary lane e2 := P2(cos theta) implicitly chooses a unit axis a, with cos theta = a_i n^i on the local Euclidean spatial background.",
            "formula": "x := a.n; e2(n)=P2(x)=(3*x^2-1)/2",
            "result": "a public boundary-chart axis is available conditionally",
            "status": "PUBLIC_AXIS_AVAILABLE_PARENT_SOURCE_AXIS_NOT_YET_OWNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "basis_id": "BAS3176_1_STF_tensor",
            "object": "Y_a^{ij}",
            "statement": "The canonical axisymmetric spatial STF tensor built from the same axis is tracefree and has fixed norm.",
            "formula": "Y_a^{ij}:=a^i a^j-delta^{ij}/3; delta_ij Y_a^{ij}=0; Y_a: Y_a = 2/3",
            "result": "STF angular basis is derived, not assumed",
            "status": "DERIVED_ANGULAR_STF_BASIS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "basis_id": "BAS3176_2_P2_STF_identity",
            "object": "P2_to_STF_lift",
            "statement": "Contracting the STF tensor with the radial unit vector reproduces the Legendre l=2 lane with a fixed normalization.",
            "formula": "Y_a^{ij} n_i n_j = (a.n)^2 - 1/3 = (2/3) P2(a.n), hence P2(a.n) = (3/2) Y_a^{ij} n_i n_j",
            "result": "the missing angular normalization is closed",
            "status": "DERIVED_EXACT_IDENTITY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "basis_id": "BAS3176_3_scalar_boundary_to_tensor_boundary",
            "object": "signed_boundary_lift",
            "statement": "A signed scalar boundary perturbation delta z = s_K2*C_K2_unit*P2(a.n) can be represented by an STF boundary tensor with coefficient 3/2.",
            "formula": "T_K2^{ij}|_boundary = (3/2) s_K2*C_K2_unit*Y_a^{ij}; T_K2^{ij} n_i n_j = s_K2*C_K2_unit*P2(a.n)",
            "result": "boundary angular lift is available if s_K2 and the axis are supplied",
            "status": "CONDITIONAL_SIGNED_BOUNDARY_LIFT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "basis_id": "BAS3176_4_not_source_moment",
            "object": "source_moment_gap",
            "statement": "The angular lift does not determine the compact-source radial kernel or the Green-function moment that sets the exterior J2 amplitude.",
            "formula": "Upsilon_J2 = P_surf,l2 L_eff^{-1}[(3/2) s_K2*C_K2_unit*R_K2(r)*Y_a^{ij}]",
            "result": "the live blocker moves from STF basis to signed source moment M2_K2",
            "status": "SOURCE_MOMENT_STILL_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def signed_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "SIG3176_0_replace_abs_with_signed_product",
            "object": "s_K2",
            "current_artifact": "3164 defines K_2 := |W_2 M_Lambda|",
            "derived_requirement": "define s_K2 := W_2 M_Lambda before taking the absolute envelope",
            "consequence": "K2 bounds may use |s_K2|, but a prediction/sign claim needs s_K2 itself",
            "status": "MISSING_SIGNED_PARENT_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3176_1_sign_degeneracy",
            "object": "sign(s_K2)",
            "current_artifact": "K2 scoring lane loses sign information by construction",
            "derived_requirement": "source W_2 sign, M_Lambda sign, and their convention relative to the public P2/J2 sign",
            "consequence": "without this, predicted J2 sign is at best a two-branch envelope",
            "status": "SIGN_BRANCH_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3176_2_axis_parent_vs_public_chart",
            "object": "a^i",
            "current_artifact": "e2 := P2(cos theta) supplies a public boundary axis",
            "derived_requirement": "prove that the same axis is the parent source-domain orientation entering K_hat_STF",
            "consequence": "angular maths is closed, but parent/source ownership of orientation is still conditional",
            "status": "PUBLIC_AXIS_CONDITIONAL_PARENT_AXIS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3176_3_CK2_unit_signed_use",
            "object": "sigma_K2",
            "current_artifact": "3175 used sigma_K2 := K2*C_K2_unit for magnitude source rows",
            "derived_requirement": "for prediction work use sigma_K2_signed := s_K2*C_K2_unit; reserve K2*C_K2_unit for absolute bounds",
            "consequence": "prevents hiding the missing sign inside a positive parameter",
            "status": "SIGNED_NORMALIZATION_DEFINED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def source_contract_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "MOM3176_0_angular_basis",
            "quantity": "Y_a^{ij}",
            "required_form": "Y_a^{ij}=a^i a^j-delta^{ij}/3 with P2(a.n)=(3/2)Y_a^{ij}n_i n_j",
            "current_status": "DERIVED_ANGULAR_BASIS_AVAILABLE",
            "blocks_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MOM3176_1_signed_amplitude",
            "quantity": "s_K2",
            "required_form": "s_K2 = W_2 M_Lambda in the parent convention, with source paths for W_2 and M_Lambda",
            "current_status": "MISSING_SIGNED_PARENT_OWNER",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MOM3176_2_source_profile",
            "quantity": "R_K2(r)",
            "required_form": "compact radial/source kernel with units that make s_K2*C_K2_unit*R_K2 enter K_hat_STF as a curvature/source density",
            "current_status": "MISSING_RADIAL_KERNEL_AND_UNITS",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MOM3176_3_source_moment",
            "quantity": "M2_K2",
            "required_form": "M2_K2 := P_surf,l2 L_eff^{-1}[(3/2)R_K2(r)Y_a^{ij}] in the selected gauge/readout",
            "current_status": "MISSING_GREEN_SOURCE_MOMENT",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "MOM3176_4_conservation_balance",
            "quantity": "q_K2^nu",
            "required_form": "nabla_mu delta K_hat_STF^{mu nu} cancelled by trace/exchange terms or bounded in PPN/orbital/clock arenas",
            "current_status": "MISSING_SOURCE_BALANCE",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_template_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "row_id": "BT3176_0_signed_prediction_template",
            "arena": "solar_J2_or_STF_metric",
            "prediction_form": "Upsilon_J2_pred = s_K2*C_K2_unit*M2_K2",
            "bound_form": "|s_K2| <= bound_J2 / (C_K2_unit*|M2_K2|)",
            "required_inputs": "signed s_K2; numeric C_K2_unit; sourced M2_K2; public J2 bound/readout convention",
            "current_status": "MISSING_M2_K2_AND_SIGNED_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BT3176_1_abs_envelope_template",
            "arena": "nonclaim_upper_bound",
            "prediction_form": "|Upsilon_J2_pred| <= K2*C_K2_unit*|M2_K2|",
            "bound_form": "K2 <= bound_J2 / (C_K2_unit*|M2_K2|)",
            "required_inputs": "numeric M2_K2 or conservative source-moment bound",
            "current_status": "MISSING_SOURCE_MOMENT_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BT3176_2_direct_STF_comparator",
            "arena": "PPN_clock_orbital_STF",
            "prediction_form": "Delta_i = Pi_i,STF * s_K2*C_K2_unit*M2_K2 + exchange terms",
            "bound_form": "|Delta_i| <= empirical_bound_i",
            "required_inputs": "Pi_i,STF kernel, source moment, conservation/exchange residual, empirical convention",
            "current_status": "MISSING_PROJECTION_KERNELS_AND_BALANCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3176_0_main_result",
            "finding": "The scalar P2 lane can be lifted exactly to a signed spatial STF angular basis: P2(a.n)=(3/2)Y_a^{ij}n_i n_j.",
            "claim_status": "PARTIAL_DERIVATION_WIN_NOT_A_LOCAL_GR_OR_J2_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3176_1_live_blocker",
            "finding": "The live blocker is now the signed source moment: s_K2, R_K2(r), M2_K2, and q_K2^nu/source balance.",
            "claim_status": "SOURCE_MOMENT_AND_CONSERVATION_STILL_BLOCKED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3176_2_next_target",
            "finding": "3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        BASIS: basis_rows(),
        SIGNED_AUDIT: signed_audit_rows(),
        SOURCE_CONTRACT: source_contract_rows(),
        BOUND_TEMPLATE: bound_template_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    basis = rows_by_path[BASIS]
    signed = rows_by_path[SIGNED_AUDIT]
    source = rows_by_path[SOURCE_CONTRACT]
    bounds = rows_by_path[BOUND_TEMPLATE]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    validation = [
        {
            "check_id": "VAL3176_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_1_STF_identity_closed",
            "check": "basis derivation includes exact P2 to STF identity",
            "pass": str(any(row["basis_id"] == "BAS3176_2_P2_STF_identity" and row["status"] == "DERIVED_EXACT_IDENTITY" for row in basis)).lower(),
            "detail": "P2(a.n)=(3/2)Y_a^{ij}n_i n_j",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_2_no_abs_sign_claim",
            "check": "signed audit keeps K2 absolute envelope separate from signed s_K2 prediction",
            "pass": str(any(row["audit_id"] == "SIG3176_0_replace_abs_with_signed_product" and row["status"] == "MISSING_SIGNED_PARENT_OWNER" for row in signed)).lower(),
            "detail": "K2 remains nonclaim envelope until s_K2 is parent-owned",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_3_source_moment_still_blocked",
            "check": "source contract explicitly blocks claim without R_K2, M2_K2, and source balance",
            "pass": str(all(row["valid_for_claim"] == "false" for row in source) and any(row["quantity"] == "M2_K2" and row["blocks_claim"] == "true" for row in source)).lower(),
            "detail": "M2_K2 and conservation rows remain blocking",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_4_bound_templates_nonclaim",
            "check": "all bound templates remain nonclaim rows",
            "pass": str(all(row["valid_for_claim"] == "false" for row in bounds)).lower(),
            "detail": "no empirical pass or local-GR pass is emitted",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3176_6_next_target_selected",
            "check": "decision table selects source-moment/direct-STF comparator target",
            "pass": str(any("3177-Y5-R2FR-K2-source-moment-normalization" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3177 source moment normalization or direct STF comparator bound",
            "generated_utc": now,
        },
    ]
    return validation


def main() -> None:
    rows_by_path = all_output_rows()
    rows_by_path[VALIDATION] = validation_rows(rows_by_path)
    for path, rows in rows_by_path.items():
        write_csv(path, rows)
    for path in rows_by_path:
        print(path)


if __name__ == "__main__":
    main()
