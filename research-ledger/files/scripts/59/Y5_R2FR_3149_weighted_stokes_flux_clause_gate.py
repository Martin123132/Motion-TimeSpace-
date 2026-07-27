from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3149_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3149_WEIGHTED_STOKES_FLUX_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3149_CLAUSE_GATES.csv"
BOUND = OUT / "P8_Y5_R2FR_3149_STOKES_FLUX_BOUND_SCHEMA.csv"
SCORES = OUT / "P8_Y5_R2FR_3149_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3149_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3149_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def find_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(column) == value:
            return row
    return None


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3149_0_3148_doc",
            "path": source_path("3148-Y5-R2FR-local-projector-surface-null-theorem-under-AX1090.md"),
            "role": "surface-null theorem handoff",
        },
        {
            "source_id": "SRC3149_1_3148_scores",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3148_SURFACE_NULL_SCORECARD.csv"),
            "role": "active/surface-null score impact",
        },
        {
            "source_id": "SRC3149_2_3089_doc",
            "path": source_path("3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md"),
            "role": "weighted-Stokes identity and bound precedent",
        },
        {
            "source_id": "SRC3149_3_3089_stokes",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"),
            "role": "weighted-Stokes theorem rows",
        },
        {
            "source_id": "SRC3149_4_3127_doc",
            "path": source_path("3127-Y5-R2FR-Hilbert-EM-weight-measure-and-Poynting-guard-under-AX1090.md"),
            "role": "Poynting/static flux guard",
        },
        {
            "source_id": "SRC3149_5_3142_poynting",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv"),
            "role": "owned EM stress/Poynting readout",
        },
        {
            "source_id": "SRC3149_6_3132_allocator",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"),
            "role": "allocator terms for derivative/corner/harmonic/residual/reference/readout/flux",
        },
        {
            "source_id": "SRC3149_7_3131_gate",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_GATE.csv"),
            "role": "surface zero remains blocked",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def extracted_values() -> dict[str, float | None]:
    scores = read_csv(OUT / "P8_Y5_R2FR_3148_SURFACE_NULL_SCORECARD.csv")
    active = find_row(scores, "score_id", "PS3148_0_active_absolute_fallback")
    surface_zero = find_row(scores, "score_id", "PS3148_1_if_surface_projector_zero")
    raw_surface = find_row(scores, "score_id", "PS3148_4_raw_surface_hazard")
    profile = find_row(scores, "score_id", "PS3148_5_profile_target_if_theorem_fails")
    return {
        "active_coeff": parse_float(active.get("coefficient_abs")) if active else None,
        "active_eta": parse_float(active.get("eta_abs")) if active else None,
        "coulomb_only_coeff": parse_float(surface_zero.get("coefficient_abs")) if surface_zero else None,
        "coulomb_only_eta": parse_float(surface_zero.get("eta_abs")) if surface_zero else None,
        "threshold_coeff": parse_float(active.get("threshold_abs")) if active else None,
        "wep_eta_bound": parse_float(active.get("eta_bound")) if active else None,
        "raw_surface_coeff": parse_float(raw_surface.get("coefficient_abs")) if raw_surface else None,
        "raw_surface_eta": parse_float(raw_surface.get("eta_abs")) if raw_surface else None,
        "current_profile_rho": parse_float(profile.get("coefficient_abs")) if profile else None,
        "required_profile_rho": parse_float(profile.get("threshold_abs")) if profile else None,
    }


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "WSF3149_0_decomposition",
            "statement": "Surface/profile stress source decomposes into exact, harmonic and residual pieces before local projection.",
            "formula": "P_surface = d_S Lambda + h_surface + r_surface",
            "result": "formal_decomposition_required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WSF3149_1_weighted_stokes_identity",
            "statement": "Exactness alone is insufficient; weighted Stokes exposes corner and kernel-derivative terms.",
            "formula": "Int_S W d_S Lambda = Int_partialS W Lambda - Int_S d_S(W) wedge Lambda",
            "result": "exact_identity_imported_from_3089",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WSF3149_2_zero_conditions",
            "statement": "Surface projector zero follows if the boundary is corner-free/common-calibrated, harmonic and residual pieces vanish, the weight is closed, and static flux is separated.",
            "formula": "partialS=0; h=r=0; d_S(W)=0; Phi_Poynting_static=0 => Pi_local P_surface=0",
            "result": "conditional_zero_theorem_shape",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WSF3149_3_flux_separation",
            "statement": "Poynting flux may exist as a dynamic/radiative branch, but it cannot be silently folded into static GM.",
            "formula": "DeltaK_static = DeltaK_Hilbert_stationary; DeltaK_flux = Int_partialW S_EM dot dA dt / M_H separated",
            "result": "conditional_flux_split_theorem_shape",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WSF3149_4_bound_if_unsigned",
            "statement": "If any zero condition is unsigned, the surface branch becomes a finite absolute bound row instead of a zero.",
            "formula": "|Q_surface| <= C_corner + ||d_S W|| ||Lambda|| + |<W,h>| + |<W,r>| + |Phi_Poynting| + |C_ref| + |C_readout|",
            "result": "bound_schema_ready_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3149_0_B_primitive",
            "gate": "P_surface_exact_primitive_Lambda",
            "status": "fail_for_claim",
            "reason": "3132 has formula shape B_surf=d_S Lambda+h+r but no parent primitive proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_1_corner_free",
            "gate": "partialS_empty_or_corner_terms_bounded",
            "status": "fail_for_claim",
            "reason": "weighted Stokes corner term has no theorem-zero or source-backed value",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_2_closed_weight",
            "gate": "d_S(W)=0_or_bound",
            "status": "fail_for_claim",
            "reason": "kernel/gauge/source weight closedness is not parent-signed; derivative norm missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_3_harmonic_residual_zero",
            "gate": "h_surface=r_surface=0_or_bound",
            "status": "fail_for_claim",
            "reason": "cohomology/harmonic and residual terms remain allocator heads",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_4_static_flux",
            "gate": "Poynting_flux_zero_or_dynamic_channel_separated",
            "status": "fail_for_claim",
            "reason": "3142 defines Poynting readout and 3127 guard, but no zero/separation coefficient is signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_5_ref_readout_silence",
            "gate": "reference_and_readout_counterterms_silent",
            "status": "fail_for_claim",
            "reason": "3132 retains rho_reference_counterterm and rho_projector_readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3149_6_surface_zero",
            "gate": "Pi_local_P_surface_zero",
            "status": "not_claim_ready",
            "reason": "all weighted-Stokes and flux gates must close before surface branch can be removed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "bound_id": "B3149_0_corner",
            "term": "C_corner",
            "formula": "|Int_partialS W Lambda|",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "allocator_component": "rho_corner_joint",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "B3149_1_kernel_derivative",
            "term": "norm_dS_W_times_norm_Lambda",
            "formula": "||d_S(W)||_* ||Lambda||_*",
            "status": "MISSING_CLOSED_WEIGHT_OR_DERIVATIVE_NORM",
            "allocator_component": "rho_kernel_derivative",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "B3149_2_harmonic",
            "term": "harmonic_surface_abs",
            "formula": "|Int_S W h_surface|",
            "status": "MISSING_COHOMOLOGY_ZERO_OR_BOUND",
            "allocator_component": "rho_harmonic_cohomology",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "B3149_3_residual",
            "term": "residual_surface_abs",
            "formula": "|Int_S W r_surface|",
            "status": "MISSING_RESIDUAL_ZERO_OR_BOUND",
            "allocator_component": "rho_nonexact_residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "B3149_4_flux",
            "term": "poynting_flux_abs",
            "formula": "|Int_partialW S_EM dot dA dt|/M_H",
            "status": "MISSING_STATIONARY_ZERO_OR_DYNAMIC_FLUX_BOUND",
            "allocator_component": "rho_flux_poynting",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "B3149_5_reference_readout",
            "term": "reference_readout_abs",
            "formula": "|C_ref|+|C_readout|",
            "status": "MISSING_REFERENCE_READOUT_SILENCE_OR_BOUND",
            "allocator_component": "rho_reference_counterterm;rho_projector_readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    active_coeff = values["active_coeff"]
    active_eta = values["active_eta"]
    coulomb_coeff = values["coulomb_only_coeff"]
    coulomb_eta = values["coulomb_only_eta"]
    threshold = values["threshold_coeff"]
    eta_bound = values["wep_eta_bound"]
    current_profile = values["current_profile_rho"]
    required_profile = values["required_profile_rho"]
    return [
        {
            "score_id": "SI3149_0_current_active",
            "scenario": "current_absolute_surface_retained",
            "coefficient_abs": fmt(active_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(active_eta),
            "eta_bound": fmt(eta_bound),
            "score": "above_threshold_pressure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "WEIGHTED_STOKES_ZERO_UNSIGNED;FLUX_GUARD_UNSIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "SI3149_1_if_all_stokes_flux_gates_close",
            "scenario": "surface_removed_Coulomb_only",
            "coefficient_abs": fmt(coulomb_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(coulomb_eta),
            "eta_bound": fmt(eta_bound),
            "score": "would_pass_if_weighted_stokes_and_flux_clauses_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "CONDITIONAL_ONLY",
            "generated_utc": now,
        },
        {
            "score_id": "SI3149_2_if_clauses_fail",
            "scenario": "finite_profile_or_bound_fallback",
            "coefficient_abs": fmt(current_profile),
            "threshold_abs": fmt(required_profile),
            "eta_abs": "rho_ratio=" + fmt(None if current_profile is None or required_profile in (None, 0) else current_profile / required_profile),
            "eta_bound": "not_eta_row",
            "score": "profile_or_bound_must_tighten",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SOURCE_BACKED_BOUND_TERMS_OR_PREM_PROFILE_REQUIRED",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3149_0_identity",
            "decision": "weighted-Stokes identity is the exact local clause; exactness alone is not enough",
            "effect": "surface-zero proof must also close corner, closed-weight, harmonic/residual, flux and readout/reference terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3149_1_claim",
            "decision": "Pi_local P_surface=0 is still not claim-ready",
            "effect": "active absolute pressure row remains retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3149_2_next",
            "decision": "next target should choose closed-weight theorem or first finite bound term",
            "effect": "3150 should derive d_S(W)=0 from parent/source class, or fill norm_dS_W*norm_Lambda / Poynting flux bound rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    bounds: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_cover = {"WSF3149_1_weighted_stokes_identity", "WSF3149_2_zero_conditions", "WSF3149_3_flux_separation", "WSF3149_4_bound_if_unsigned"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    bound_cover = {"C_corner", "norm_dS_W_times_norm_Lambda", "harmonic_surface_abs", "residual_surface_abs", "poynting_flux_abs", "reference_readout_abs"}.issubset(
        {row["term"] for row in bounds}
    )
    conditional_pass = any(
        row["score_id"] == "SI3149_1_if_all_stokes_flux_gates_close"
        and row["score"] == "would_pass_if_weighted_stokes_and_flux_clauses_signed"
        and row["claim_allowed"] == "false"
        for row in scores
    )
    active_retained = any(
        row["score_id"] == "SI3149_0_current_active"
        and row["score"] == "above_threshold_pressure"
        for row in scores
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    numerics = all(value is not None for value in values.values())
    return [
        {
            "check_id": "V3149_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3149_1_theorem_shapes_present",
            "status": "pass" if theorem_cover else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3149_2_bound_schema_complete",
            "status": "pass" if bound_cover else "fail",
            "details": json.dumps([row["term"] for row in bounds], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3149_3_conditional_pass_nonclaim",
            "status": "pass" if conditional_pass else "fail",
            "details": "if every Stokes/flux clause closes, score reduces to Coulomb-only pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3149_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "active pressure row remains because clauses are unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3149_5_no_claim_leak",
            "status": "pass" if gates_block and decisions_nonclaim and numerics else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = extracted_values()
    theorem = theorem_rows()
    gates = gate_rows()
    bounds = bound_rows()
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, bounds, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(BOUND, bounds)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
