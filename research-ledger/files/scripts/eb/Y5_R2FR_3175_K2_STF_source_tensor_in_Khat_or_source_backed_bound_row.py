from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3175_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3175_STF_SOURCE_TENSOR_DERIVATION.csv"
AUDIT = OUT / "P8_Y5_R2FR_3175_K2_SCALAR_TO_TENSOR_AUDIT.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3175_STF_SOURCE_CONTRACT.csv"
BOUND_ROWS = OUT / "P8_Y5_R2FR_3175_SOURCE_READY_BOUND_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3175_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3175_VALIDATION.csv"


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
        for row in rows:
            writer.writerow(row)


def resolve(base: str, relative: str) -> Path:
    if base == "post_checkpoint":
        return ROOT / relative
    if base == "formalization":
        return FW / relative
    raise ValueError(base)


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("post_checkpoint", "3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090.md", "3174 handoff: S_K2_STF is live bottleneck"),
        ("post_checkpoint", "source-intake/mts_residuals/P8_Y5_R2FR_3174_READOUT_AND_SOURCE_STATUS.csv", "3174 source status row naming missing S_K2"),
        ("post_checkpoint", "3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090.md", "K2 := |W2 M_Lambda| scalar lane"),
        ("post_checkpoint", "3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "K2 residual-vector interface"),
        ("post_checkpoint", "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md", "Gamma/Khat action-existence and q_loc residual guard"),
        ("post_checkpoint", "1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md", "tracefree metric transfer not owned by scalar Qcoh"),
        ("post_checkpoint", "1182-Y5-R10-symbolic-PPN-KS-prediction-map-or-numeric-comparator-runner.md", "STF channel separated from scalar gamma"),
        ("post_checkpoint", "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "Khat/Gamma constitutive owner clue"),
        ("formalization", "83-parent-equations-v1.md", "K_MTS trace/tensor split and effective parent scaffold"),
        ("formalization", "133-exact-transition-cancellation-or-projector-theorem.md", "Khat cancellation not derived"),
    ]
    return [
        {
            "input_id": f"IN3175_{index}",
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
    return [
        {
            "derivation_id": "STF3175_0_exact_definition",
            "object": "S_K2_STF",
            "statement": "The K2 source tensor is the l=2 tracefree projection of the K_MTS response to sigma_K2 := K2*C_K2_unit.",
            "formula": "S_K2_STF^{mu nu} := P_STF,l2[delta K_MTS^{mu nu}/delta sigma_K2]|_0 = P_l2[delta K_hat^{mu nu}/delta sigma_K2]|_0",
            "result": "exact definition available",
            "status": "DERIVED_DEFINITION_NOT_INSTANTIATED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "STF3175_1_tracefree_projector",
            "object": "tracefree_projection",
            "statement": "At fixed background metric, the four-dimensional tracefree projector removes the Gamma_eff/trace lane.",
            "formula": "P_TF^{mu nu}_{alpha beta}=delta^{(mu}_alpha delta^{nu)}_beta - (1/4) g^{mu nu} g_{alpha beta}",
            "result": "K_hat response is the tracefree part of the MTS source response",
            "status": "PROJECTOR_FORMULA_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "STF3175_2_spatial_l2_basis",
            "object": "static_spatial_STF_basis",
            "statement": "For an axisymmetric static quadrupole, a signed spatial basis requires an axis and orientation.",
            "formula": "Y_STF^{ij}(a)=a^i a^j - delta^{ij}/3; delta_ij Y_STF^{ij}=0",
            "result": "a public J2-like source needs signed STF tensor data, not only a scalar magnitude",
            "status": "BASIS_REQUIREMENT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "STF3175_3_conditional_source_ansatz",
            "object": "conditional_K2_source_tensor",
            "statement": "If a parent supplies signed amplitude, axis, radial kernel, and source normalization, K2 can be lifted into K_hat as a source tensor.",
            "formula": "delta K_hat_STF^{ij}(x)=sigma_K2 * A_STF * R_K2(r) * (a^i a^j-delta^{ij}/3)",
            "result": "this would instantiate S_K2_STF^{ij}=A_STF R_K2(r) Y_STF^{ij}",
            "status": "CONDITIONAL_ANSATZ_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "STF3175_4_conservation_constraint",
            "object": "source_conservation_residual",
            "statement": "A tracefree source tensor is not automatically conservation-safe; its divergence feeds the retained q_loc/source-normalization residual unless parent-balanced.",
            "formula": "q_K2^nu := -nabla_mu(delta K_hat_STF^{mu nu}) + trace/exchange companions",
            "result": "source tensor claim requires q_K2^nu=0, a boundary theorem, or a source-backed residual bound",
            "status": "CONSERVATION_GUARD_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "STF3175_5_exterior_metric_response",
            "object": "conditional_Upsilon_source_moment",
            "statement": "Under the 3174 effective operator scaffold, the exterior public quadrupole is determined by the source moment of S_K2_STF.",
            "formula": "Upsilon_J2 = P_surf,l2 L_eff^{-1}[S_K2_STF] = source_moment(S_K2_STF; boundary, gauge, radius)",
            "result": "Upsilon reduces to a source-moment problem if S_K2_STF is supplied",
            "status": "CONDITIONAL_EFFECTIVE_SOURCE_MOMENT_ROUTE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "AUD3175_0_K2_is_magnitude",
            "object": "K_2",
            "current_artifact": "3164 defines K_2 := |W_2 M_Lambda|",
            "missing_for_tensor": "signed amplitude s_K2, axis/orientation, tensor basis, source-domain support",
            "verdict": "SCALAR_MAGNITUDE_CANNOT_DEFINE_STF_TENSOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AUD3175_1_Wbar_lane",
            "object": "W_2",
            "current_artifact": "3164 derives one-dimensional l=2 sensitivity only if Wbar is Frechet differentiable",
            "missing_for_tensor": "parent Wbar functional and signed projection convention",
            "verdict": "SIGNED_PROJECTION_OWNER_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AUD3175_2_MLambda_lane",
            "object": "M_Lambda",
            "current_artifact": "3165 uses ||Lambda||_hat(M_Lambda=1) inside C_K2_unit",
            "missing_for_tensor": "parent Lambda map into K_hat_STF, source-domain normalization, units L^-2 for source tensor",
            "verdict": "NORMALIZATION_AND_UNITS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AUD3175_3_Khat_action",
            "object": "K_hat",
            "current_artifact": "1010 keeps Gamma/Khat action existence, metric response, Helmholtz, and q_loc zero unproved",
            "missing_for_tensor": "S_GK or constitutive owner proving Khat is a variational stress/source sector",
            "verdict": "KHAT_PARENT_OWNER_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AUD3175_4_Qcoh_scalar_guard",
            "object": "Qcoh/tracefree_transfer",
            "current_artifact": "1180 rejects scalar Qcoh as owner of tracefree spin-2 transfer",
            "missing_for_tensor": "separate tracefree parent variable or metric transfer theorem",
            "verdict": "SCALAR_PROJECTOR_CANNOT_SUPPLY_STF_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "AUD3175_5_PPN_STF_channel",
            "object": "public comparator",
            "current_artifact": "1182 splits pure tracefree channel away from scalar gamma at first order",
            "missing_for_tensor": "direct STF/preferred-frame/tidal comparator and q_loc_TF norm",
            "verdict": "TEST_CHANNEL_NONSCALAR_AND_UNSOURCED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "CON3175_0_signed_amplitude",
            "quantity": "s_K2",
            "definition": "signed l=2 amplitude before absolute-value closure",
            "required_form": "s_K2 = W_2 M_Lambda with sign convention and source path; K_2=|s_K2| only after scoring envelope",
            "current_status": "MISSING_SIGNED_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CON3175_1_STF_basis",
            "quantity": "Y_STF^{mu nu}",
            "definition": "parent-owned l=2 tracefree tensor basis/source orientation",
            "required_form": "Y_STF^{ij}=a^i a^j-delta^{ij}/3 or equivalent tensor harmonic with axis/frame/source-domain lock",
            "current_status": "MISSING_AXIS_AND_FRAME",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CON3175_2_radial_kernel",
            "quantity": "R_K2(r)",
            "definition": "compact source radial/profile kernel whose source moment produces exterior r^-3 field",
            "required_form": "R_K2 has units/source normalization so sigma_K2*R_K2 has curvature units L^-2",
            "current_status": "MISSING_RADIAL_SOURCE_KERNEL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CON3175_3_Khat_embedding",
            "quantity": "delta K_hat_STF",
            "definition": "embedding of K2 lane into tracefree MTS source tensor",
            "required_form": "delta K_hat_STF^{mu nu}=sigma_K2 A_STF R_K2 Y_STF^{mu nu} plus declared time/vector components",
            "current_status": "MISSING_PARENT_KHAT_EMBEDDING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "CON3175_4_conservation",
            "quantity": "q_K2^nu",
            "definition": "divergence/source-balance residual of the proposed K2 tensor",
            "required_form": "nabla_mu delta K_hat_STF^{mu nu} cancelled by owned trace/exchange/boundary term or explicitly bounded",
            "current_status": "MISSING_CONSERVATION_BALANCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "row_id": "BR3175_0_S_K2_STF_source_tensor",
            "quantity": "S_K2_STF",
            "definition": "P_STF,l2[delta K_MTS^{mu nu}/delta sigma_K2]",
            "value_or_formula": "MISSING_SIGNED_STF_SOURCE_TENSOR",
            "units": "L^-2 per dimensionless sigma_K2",
            "source_path": "MISSING_PARENT_KHAT_SOURCE_PATH",
            "equation_ref": "MISSING_DELTA_KHAT_DELTA_SIGMA_EQUATION",
            "claim_blockers": "MISSING_SIGNED_AMPLITUDE;MISSING_STF_BASIS;MISSING_RADIAL_KERNEL;MISSING_UNITS;MISSING_CONSERVATION_BALANCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BR3175_1_source_moment_Upsilon",
            "quantity": "Upsilon_J2_source_moment",
            "definition": "P_surf,l2 L_eff^{-1}[S_K2_STF]",
            "value_or_formula": "MISSING_SOURCE_MOMENT_INTEGRAL",
            "units": "dimensionless transfer kernel",
            "source_path": "MISSING_COMPACT_SOURCE_PROFILE",
            "equation_ref": "MISSING_GREEN_NORMALIZATION_AND_BOUNDARY_CONDITIONS",
            "claim_blockers": "MISSING_S_K2_STF;MISSING_SOURCE_RADIUS;MISSING_GAUGE;MISSING_PUBLIC_METRIC_NORMALIZATION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BR3175_2_q_K2_conservation_residual",
            "quantity": "q_K2^nu",
            "definition": "-nabla_mu(delta K_hat_STF^{mu nu}) plus owned companion terms",
            "value_or_formula": "MISSING_CONSERVATION_RESIDUAL_BOUND",
            "units": "L^-3",
            "source_path": "MISSING_KHAT_DIVERGENCE_OR_BOUNDARY_SOURCE",
            "equation_ref": "MISSING_SOURCE_BALANCE_EQUATION",
            "claim_blockers": "MISSING_DIVERGENCE_ZERO_THEOREM;MISSING_BOUND;MISSING_OBSERVABLE_MAP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BR3175_3_direct_STF_PPN_comparator",
            "quantity": "H_TF_metric_or_preferred_frame_bound",
            "definition": "direct non-scalar comparator for tracefree metric/STF residual channel",
            "value_or_formula": "MISSING_PRIMARY_STF_OR_PREFERRED_FRAME_SOURCE",
            "units": "PPN_or_metric_amplitude_units",
            "source_path": "MISSING_PRIMARY_COMPARATOR_SOURCE",
            "equation_ref": "MISSING_STF_TO_OBSERVABLE_MAP",
            "claim_blockers": "MISSING_S_K2_STF;MISSING_COMPARATOR;MISSING_Q_LOC_TF_NORM;MISSING_NO_CANCELLATION_GUARD",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3175_0_definition_success",
            "decision": "S_K2_STF has an exact definition as a projected source derivative",
            "because": "K_MTS trace/tensor split plus 3174 effective operator scaffold define the correct object",
            "effect": "future rows must target delta K_hat_STF/delta sigma_K2 rather than vague coupling",
            "next_action": "instantiate signed STF source basis or source-backed bound row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3175_1_current_derivation_fails",
            "decision": "current K2 scalar lane cannot instantiate a tracefree source tensor",
            "because": "K2 is an absolute magnitude and lacks sign, axis, radial profile, source units, and conservation balance",
            "effect": "no J2/PPN/local-GR scoring from K2 source tensor is allowed",
            "next_action": "derive signed W2*M_Lambda tensor owner or keep rows as nonclaim bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3175_2_next_target",
            "decision": "attack the signed K2 STF basis/source moment next",
            "because": "this is now the minimal missing object between the effective operator scaffold and public J2/PPN tests",
            "effect": "radial Green/profile and L_eff are conditionally handled; source tensor ownership is not",
            "next_action": "3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    derivations: list[dict[str, object]],
    audits: list[dict[str, object]],
    contracts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    exact_definition = any(row["object"] == "S_K2_STF" and "DERIVED_DEFINITION" in row["status"] for row in derivations)
    magnitude_obstruction = any(row["verdict"] == "SCALAR_MAGNITUDE_CANNOT_DEFINE_STF_TENSOR" for row in audits)
    contract_missing = all("MISSING" in row["current_status"] for row in contracts)
    source_rows_refused = all(row["valid_for_claim"] == "false" and "MISSING" in row["claim_blockers"] for row in bounds)
    next_target = any("3176" in row["next_action"] for row in decisions)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, derivations, audits, contracts, bounds, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3175_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_1_exact_definition_written",
            "status": "pass" if exact_definition else "fail",
            "detail": "S_K2_STF projected derivative definition exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_2_magnitude_obstruction_logged",
            "status": "pass" if magnitude_obstruction else "fail",
            "detail": "K2 absolute magnitude cannot define signed STF tensor",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_3_contract_objects_missing",
            "status": "pass" if contract_missing else "fail",
            "detail": "signed amplitude, STF basis, radial kernel, Khat embedding, and conservation balance remain missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_4_source_rows_refused",
            "status": "pass" if source_rows_refused else "fail",
            "detail": "all source-ready bound rows remain nonclaim with MISSING blockers",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_5_next_target_selected",
            "status": "pass" if next_target else "fail",
            "detail": "3176 signed STF basis/source moment target selected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3175_6_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3175 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    derivations = derivation_rows()
    audits = audit_rows()
    contracts = contract_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, derivations, audits, contracts, bounds, decisions)
    write_csv(INPUTS, inputs)
    write_csv(DERIVATION, derivations)
    write_csv(AUDIT, audits)
    write_csv(CONTRACT, contracts)
    write_csv(BOUND_ROWS, bounds)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3175 validation failed: {failures}")


if __name__ == "__main__":
    main()
