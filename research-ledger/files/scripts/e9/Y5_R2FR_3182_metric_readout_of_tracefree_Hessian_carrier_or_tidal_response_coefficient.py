from __future__ import annotations

import csv
from datetime import datetime, timezone
from math import sqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3182_INPUTS.csv"
READOUT = OUT / "P8_Y5_R2FR_3182_WEAK_FIELD_READOUT_DERIVATION.csv"
METRIC_NULL = OUT / "P8_Y5_R2FR_3182_METRIC_NULL_AUDIT.csv"
SLIP_BOUND = OUT / "P8_Y5_R2FR_3182_SLIP_BOUND_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3182_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3182_VALIDATION.csv"

J2_BOUNDS_3170 = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"


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


def tightest_j2_bound() -> dict[str, str]:
    rows = read_csv(J2_BOUNDS_3170)
    return min(rows, key=lambda row: float(row["A_metric_bound_surface"]))


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3181-Y5-R2FR-exterior-Hessian-tidal-footprint-or-metric-null-bound-under-AX1090.md",
            "3181 exterior Hessian tidal footprint",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3181_EXTERIOR_HESSIAN_TIDAL_DERIVATION.csv",
            "3181 exact exterior Hessian norm and projection constants",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3181_METRIC_NULL_GATE.csv",
            "3181 metric-null gate requiring readout decision",
        ),
        (
            "post_checkpoint",
            "3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090.md",
            "conditional parent-v1 identity metric readout and L_eff scaffold",
        ),
        (
            "post_checkpoint",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "older Hessian metric-response safety gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "corrected solar-surface public metric P2 amplitude pressure rows",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "effective parent-v1 equation G+Lambda g=K_matter+K_MTS",
        ),
    ]
    return [
        {
            "input_id": f"IN3182_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def readout_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "readout_id": "RO3182_0_metric_convention",
            "object": "static_weak_field_scalar_metric",
            "statement": "Use the same public weak-field convention family as the J2 lane.",
            "formula": "ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j",
            "result": "Phi and Psi are the public scalar potentials in c=1 units",
            "status": "SETUP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "RO3182_1_linearized_Einstein_tensor",
            "object": "linearized_Einstein_readout",
            "statement": "For static scalar perturbations, the spatial Einstein tensor contains the gravitational-slip Hessian.",
            "formula": "G_00^(1)=2 nabla^2 Psi; G_ij^(1)=partial_i partial_j(Psi-Phi)+delta_ij nabla^2(Phi-Psi)",
            "result": "operator-level public metric readout derived",
            "status": "WEAK_FIELD_READOUT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "RO3182_2_exterior_harmonic_limit",
            "object": "harmonic_exterior",
            "statement": "In the exterior l=2 harmonic branch, nabla^2 Phi=nabla^2 Psi=0 away from the compact source.",
            "formula": "G_ij^(1)=partial_i partial_j(Psi-Phi)",
            "result": "only the slip Hessian remains in the spatial equation",
            "status": "EXTERIOR_SLIP_OPERATOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "RO3182_3_Hessian_source_match",
            "object": "tracefree_Hessian_carrier",
            "statement": "The 3181 exterior carrier has K_L,00=0 and K_L,ij=2 partial_i partial_j phi_ext.",
            "formula": "G_ij^(1)=Sigma_H K_L,ij gives Psi-Phi=2 Sigma_H phi_ext",
            "result": "identity metric readout maps the Hessian carrier to nonzero gravitational slip",
            "status": "NONZERO_SLIP_RESPONSE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "RO3182_4_operator_response_coefficient",
            "object": "metric_response_coefficient",
            "statement": "Under the conditional 3174 identity readout, the operator response is not missing: the weak-field slip coefficient is fixed.",
            "formula": "if Sigma_H=s_K2*kappa_STF*c_ext times any parent normalization, then (Psi-Phi)_P2=2 Sigma_H r^-3 P2",
            "result": "mu_slip_operator=2 before arena/gauge/source matching",
            "numeric_mu_slip_operator": 2.0,
            "status": "OPERATOR_RESPONSE_FIXED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "RO3182_5_slip_rms",
            "object": "slip_amplitude_rms",
            "statement": "Since <P2^2>_Omega=1/5, the surface RMS of the induced slip is fixed by Sigma_H.",
            "formula": "<(Psi-Phi)^2>_Omega^(1/2)=(2/sqrt(5))|Sigma_H| r^-3",
            "result": "surface coefficient 2/sqrt(5)",
            "numeric_surface_rms_coeff": 2.0 / sqrt(5.0),
            "status": "SLIP_RMS_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def metric_null_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "MN3182_0_identity_readout",
            "route": "conditional parent-v1 identity metric readout",
            "test": "Does K_L_ext vanish from the public metric equation?",
            "finding": "No. It sources gravitational slip through G_ij^(1)=partial_i partial_j(Psi-Phi).",
            "status": "EFFECTIVE_METRIC_NULL_FAILS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "MN3182_1_improvement_silent_escape",
            "route": "parent improvement or boundary-only term",
            "test": "Can a closed parent action move K_L_ext into a non-observed improvement term?",
            "finding": "Not parent-signed in the cited corpus; would override the effective identity readout rather than follow from it.",
            "status": "MISSING_PARENT_IMPROVEMENT_SILENCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "MN3182_2_hidden_frame_escape",
            "route": "non-public frame/coframe branch",
            "test": "Can K_L_ext live in a hidden/source frame not used by clocks, rods, light, and orbital readouts?",
            "finding": "Possible only if the same-frame condition in 3174 is rejected and a solder/coframe map is supplied.",
            "status": "MISSING_COFRAME_SOLDER_MAP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "MN3182_3_gauge_escape",
            "route": "pure gauge",
            "test": "Can the induced slip be dismissed as a pure coordinate artifact?",
            "finding": "No under the scalar weak-field readout: nonzero Psi-Phi is the gauge-invariant scalar slip at linear order once the matter frame is fixed.",
            "status": "PURE_GAUGE_ESCAPE_REJECTED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def slip_bound_rows() -> list[dict[str, object]]:
    now = stamp()
    j2 = tightest_j2_bound()
    surface_bound = float(j2["A_metric_bound_surface"])
    return [
        {
            "bound_id": "SB3182_0_generic_slip_rms_bound",
            "quantity": "Sigma_H",
            "normal_form": "(Psi-Phi)_P2=2 Sigma_H r^-3 P2",
            "candidate_observable": "slip_rms_surface=(2/sqrt(5))|Sigma_H|",
            "conditional_bound": "|Sigma_H| <= (sqrt(5)/2) tau_slip_surface",
            "missing_inputs": "tau_slip_surface;observable_transfer_kernel;source_matching_radius;parent_normalization_of_Sigma_H",
            "status": "TEMPLATE_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "SB3182_1_J2_pressure_if_one_to_one_metric_amplitude",
            "quantity": "Sigma_H",
            "normal_form": "conditional pressure only: if the slip P2 coefficient is bounded like a public metric P2 amplitude",
            "candidate_observable": "A_slip_surface=2|Sigma_H|",
            "conditional_bound": f"|Sigma_H| <= {surface_bound / 2.0:.15e}",
            "source_row": j2["bound_id"],
            "source_bound_name": j2["bound_name"],
            "source_A_metric_bound_surface": f"{surface_bound:.15e}",
            "missing_inputs": "proof that slip amplitude maps one-to-one to the 3170 public J2 metric amplitude;potential_split_boundary_condition",
            "status": "PRESSURE_ONLY_NOT_A_CLAIM_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "SB3182_2_source_amplitude_zero_route",
            "quantity": "Sigma_H",
            "normal_form": "Sigma_H=s_K2*kappa_STF*c_ext times parent normalization",
            "candidate_observable": "any nonzero public slip/r^-3 quadrupole",
            "conditional_bound": "Sigma_H=0 exactly, or finite Sigma_H must satisfy slip/J2/PPN/orbital bounds",
            "missing_inputs": "zero theorem for s_K2 or c_ext or kappa_STF;otherwise calibrated finite source amplitude",
            "status": "ZERO_THEOREM_OR_BOUND_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3182_0_readout_not_missing_under_identity",
            "finding": "Under the conditional 3174 identity metric readout, the exterior Hessian carrier maps to gravitational slip with operator coefficient 2.",
            "claim_status": "CONDITIONAL_OPERATOR_RESPONSE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3182_1_metric_null_rejected_conditionally",
            "finding": "The tracefree Hessian branch is not metric-null in the effective weak-field public metric equation.",
            "claim_status": "EFFECTIVE_METRIC_NULL_FAILS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3182_2_local_GR_implication",
            "finding": "Local GR can still be recovered only if Sigma_H is zero/suppressed, the term is parent-improvement-silent, or the induced slip is bounded below local-test limits.",
            "claim_status": "LOCAL_GR_REQUIRES_ZERO_THEOREM_OR_SLIP_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3182_3_next_target",
            "finding": "3183-Y5-R2FR-Hessian-slip-amplitude-zero-theorem-or-J2-PPN-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        READOUT: readout_rows(),
        METRIC_NULL: metric_null_rows(),
        SLIP_BOUND: slip_bound_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    readout = rows_by_path[READOUT]
    metric_null = rows_by_path[METRIC_NULL]
    slip_bound = rows_by_path[SLIP_BOUND]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    return [
        {
            "check_id": "VAL3182_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_1_weak_field_readout",
            "check": "weak-field Einstein readout formulas are recorded",
            "pass": str(any(row["status"] == "WEAK_FIELD_READOUT_DERIVED" for row in readout) and any(row["status"] == "EXTERIOR_SLIP_OPERATOR" for row in readout)).lower(),
            "detail": "G_ij slip Hessian row present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_2_nonzero_slip_response",
            "check": "Hessian source maps to nonzero slip under identity readout",
            "pass": str(any(row["status"] == "NONZERO_SLIP_RESPONSE" for row in readout)).lower(),
            "detail": "Psi-Phi=2 Sigma_H phi_ext",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_3_metric_null_conditionally_fails",
            "check": "metric-null is rejected for the effective identity-readout branch",
            "pass": str(any(row["status"] == "EFFECTIVE_METRIC_NULL_FAILS" for row in metric_null)).lower(),
            "detail": "only parent-improvement/hidden-frame routes remain open",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_4_bound_templates_nonclaim",
            "check": "slip bound rows remain nonclaim templates with missing inputs declared",
            "pass": str(all(row["valid_for_claim"] == "false" and row["missing_inputs"] for row in slip_bound)).lower(),
            "detail": f"{len(slip_bound)} slip-bound rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_5_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3182_6_next_target_selected",
            "check": "decision table selects zero theorem or J2/PPN bound as next target",
            "pass": str(any("3183-Y5-R2FR-Hessian-slip-amplitude-zero" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3183",
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
