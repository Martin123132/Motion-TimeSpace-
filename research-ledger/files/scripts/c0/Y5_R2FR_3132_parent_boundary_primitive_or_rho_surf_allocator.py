from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUT = OUT / "P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_OUTPUT.csv"
ALLOCATOR = OUT / "P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3132_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_GATE.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    candidate = ROOT / path_text
    if candidate.exists():
        return candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str, row_id_column: str) -> dict[str, str] | None:
    if not row_id:
        return None
    if row_id_column:
        for row in rows:
            if row.get(row_id_column, "") == row_id:
                return row
    for row in rows:
        if row_id in row.values():
            return row
    return None


def base_inputs() -> list[dict[str, Any]]:
    residual = "source-intake\\mts_residuals\\"
    return [
        {
            "source_id": "SRC3132_0",
            "role": "3131_next_fork",
            "source_file": residual + "P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_OUTPUT.csv",
            "source_row_id": "BEX3131_8",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "3131 handoff: parent boundary exactness or rho_surf allocator.",
        },
        {
            "source_id": "SRC3132_1",
            "role": "3131_retained_cap",
            "source_file": residual + "P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_OUTPUT.csv",
            "source_row_id": "BEX3131_7",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Retained rho_surf finite cap from 3130/3131.",
        },
        {
            "source_id": "SRC3132_2",
            "role": "3130_surface_cap",
            "source_file": residual + "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv",
            "source_row_id": "BBS3130_1",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Original surface/binding cap with coefficient and WEP threshold.",
        },
        {
            "source_id": "SRC3132_3",
            "role": "1040_charge_formula",
            "source_file": residual + "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
            "source_row_id": "BX1040_1_candidate_charge_density",
            "row_id_column": "formula_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Concrete B_X surface density formula shape.",
        },
        {
            "source_id": "SRC3132_4",
            "role": "1040_exactness_route",
            "source_file": residual + "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
            "source_row_id": "BX1040_3_exactness_route",
            "row_id_column": "formula_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Exact/pure boundary repair route.",
        },
        {
            "source_id": "SRC3132_5",
            "role": "1040_owner_verdict",
            "source_file": residual + "P8_Y5_R10_1040_BX_OWNER_GATE.csv",
            "source_row_id": "BXG1040_5_verdict",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Claim-grade B_X owner package gate.",
        },
        {
            "source_id": "SRC3132_6",
            "role": "1020_weighted_stokes",
            "source_file": residual + "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
            "source_row_id": "ETB1020_2_zero_conditions",
            "row_id_column": "theorem_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Weighted Stokes zero conditions.",
        },
        {
            "source_id": "SRC3132_7",
            "role": "1020_residual_bound",
            "source_file": residual + "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
            "source_row_id": "ETB1020_3_residual_bound",
            "row_id_column": "theorem_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Finite residual bound if exact zero fails.",
        },
        {
            "source_id": "SRC3132_8",
            "role": "1020_domain_verdict",
            "source_file": residual + "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
            "source_row_id": "BDC1020_5_verdict",
            "row_id_column": "certificate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Boundary domain/cohomology verdict.",
        },
        {
            "source_id": "SRC3132_9",
            "role": "1021_variation_to_primitive",
            "source_file": residual + "P8_Y5_R10_1021_PARENT_VARIATION_TEMPLATE.csv",
            "source_row_id": "PVT1021_5_verdict",
            "row_id_column": "template_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Parent variation to primitive map.",
        },
        {
            "source_id": "SRC3132_10",
            "role": "1021_primitive_gate",
            "source_file": residual + "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv",
            "source_row_id": "BXG1021_5_verdict",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "B_X primitive closure verdict.",
        },
        {
            "source_id": "SRC3132_11",
            "role": "1041_absent_quotient",
            "source_file": residual + "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv",
            "source_row_id": "XC1041_0_absent_quotient",
            "row_id_column": "candidate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Absent/nonprimitive quotient route.",
        },
        {
            "source_id": "SRC3132_12",
            "role": "1041_vertical_constraint",
            "source_file": residual + "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv",
            "source_row_id": "XC1041_1_first_class_vertical_constraint",
            "row_id_column": "candidate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "First-class vertical/constraint route.",
        },
        {
            "source_id": "SRC3132_13",
            "role": "1041_owner_gate",
            "source_file": residual + "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv",
            "source_row_id": "TOG1041_5_verdict",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Theta_X/P_X owner verdict.",
        },
        {
            "source_id": "SRC3132_14",
            "role": "1041_noflux_exact",
            "source_file": residual + "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv",
            "source_row_id": "NFR1041_1_topological_exact",
            "row_id_column": "route_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Topological/exact boundary no-flux route.",
        },
        {
            "source_id": "SRC3132_15",
            "role": "3127_poynting_guard",
            "source_file": residual + "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
            "source_row_id": "WGT3127_4",
            "row_id_column": "derivation_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Static versus radiative EM/Poynting guard.",
        },
    ]


def load_sources(inputs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for input_row in inputs:
        path = source_path(str(input_row["source_file"]))
        source = find_row(read_csv(path), str(input_row["source_row_id"]), str(input_row["row_id_column"]))
        sources[str(input_row["role"])] = {
            "input": input_row,
            "path": path,
            "row": source,
            "exists": path.exists(),
            "found": source is not None,
        }
    return sources


def source_paths(sources: dict[str, dict[str, Any]], *roles: str) -> str:
    return ";".join(str(sources[role]["path"]) for role in roles)


def cap_values(sources: dict[str, dict[str, Any]]) -> dict[str, float | None]:
    cap_row = sources.get("3130_surface_cap", {}).get("row") or {}
    retained_row = sources.get("3131_retained_cap", {}).get("row") or {}
    rho_cap = parse_float(cap_row.get("residual_factor_max", "")) or parse_float(retained_row.get("rho_surf_cap_retained", ""))
    coefficient = parse_float(cap_row.get("coefficient_abs", ""))
    threshold = parse_float(cap_row.get("WEP_kernel_threshold_abs", ""))
    delta_bound = parse_float(cap_row.get("deltaJ_bound_abs", ""))
    suppression = parse_float(cap_row.get("suppression_min", "")) or parse_float(retained_row.get("suppression_min_retained", ""))
    eta_at_cap = threshold * delta_bound if threshold is not None and delta_bound is not None else None
    return {
        "rho_cap": rho_cap,
        "surface_coefficient_abs": coefficient,
        "threshold_abs": threshold,
        "deltaJ_bound_abs": delta_bound,
        "suppression_min": suppression,
        "eta_at_cap": eta_at_cap,
    }


def proof_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    values = cap_values(sources)
    now = stamp()
    return [
        {
            "row_id": "PBA3132_0",
            "route": "parent_boundary_charge_formula",
            "object": "B_surf_or_B_X",
            "derived_or_attempted_form": "B_surf^nu := sigma n_mu P_X^{mu nu} + B_ct^nu + B_ref^nu + B_exact^nu",
            "what_would_close_zero": "derive P_X, B_ct, B_ref, and B_exact from one parent variation and show B_surf=d_boundary Lambda plus no harmonic/residual/corner/kernel terms",
            "current_status": "formula_shape_available_not_parent_signed",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "PARENT_LX_THETAX_PX_NOT_SELECTED;COUNTERTERM_REFERENCE_OWNER_MISSING;BOUNDARY_CLASS_UNSIGNED",
            "next_action": "select an absent-quotient or first-class vertical parent route, or use allocator rows",
            "source_paths": source_paths(sources, "1040_charge_formula", "1040_owner_verdict"),
            "generated_utc": now,
        },
        {
            "row_id": "PBA3132_1",
            "route": "absent_quotient_zero_route",
            "object": "nonprimitive_boundary_variable",
            "derived_or_attempted_form": "If X/surface sector is not a primitive parent field, delta X is not varied independently, so Theta_X=P_X=B_surf=0 before readout.",
            "what_would_close_zero": "prove the relevant MTS boundary/source variable is a quotient/readout coordinate, not a parent degree of freedom",
            "current_status": "best_clean_route_not_parent_proved",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "ABSENT_QUOTIENT_NOT_PROVED;READOUT_DELETE_ROUTE_FORBIDDEN_WITHOUT_PARENT_MAP",
            "next_action": "try to construct the quotient map and show surface/binding belongs to calibration/readout data, not an independent source current",
            "source_paths": source_paths(sources, "1041_absent_quotient", "1041_owner_gate"),
            "generated_utc": now,
        },
        {
            "row_id": "PBA3132_2",
            "route": "first_class_vertical_zero_route",
            "object": "vertical_boundary_generator",
            "derived_or_attempted_form": "Omega_flat(v_X)=delta C_X with Q_X=K_boundary=0 for proper compact transformations; improper physical ADM/time charges remain outside the killed sector.",
            "what_would_close_zero": "derive the vertical generator, its momentum map, and a proper/source boundary class split from the same parent action",
            "current_status": "mathematically_plausible_not_parent_signed",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "VERTICAL_GENERATOR_NOT_MAPPED;PROPER_SOURCE_BOUNDARY_SPLIT_MISSING;DO_NOT_KILL_GR_CHARGES",
            "next_action": "map DCdagger/vertical generator to the actual parent variation if this route is chosen",
            "source_paths": source_paths(sources, "1041_vertical_constraint", "1021_variation_to_primitive"),
            "generated_utc": now,
        },
        {
            "row_id": "PBA3132_3",
            "route": "weighted_stokes_zero_conditions",
            "object": "boundary_exactness",
            "derived_or_attempted_form": "B_surf=d_S Lambda+h+r and int_S F epsilon d_S Lambda = int_partialS F epsilon Lambda - int_S d_S(F epsilon) wedge Lambda",
            "what_would_close_zero": "partial S=empty, h=0, r=0, d_S(F epsilon)=0, fixed reference, and same source/calibration boundary class",
            "current_status": "exact_zero_conditions_derived_but_unsigned",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "PRIMITIVE_NOT_CONSTRUCTED;HARMONIC_ZERO_UNSIGNED;KERNEL_DERIVATIVE_UNSIGNED;CORNER_AUDIT_UNSIGNED",
            "next_action": "either prove all zero conditions or bound each term in the rho_surf allocator",
            "source_paths": source_paths(sources, "1020_weighted_stokes", "1020_residual_bound", "1020_domain_verdict", "1021_primitive_gate"),
            "generated_utc": now,
        },
        {
            "row_id": "PBA3132_4",
            "route": "topological_exact_boundary_route",
            "object": "source_boundary_no_flux",
            "derived_or_attempted_form": "L_boundary=dB or class-only topological density with no local metric/source variation; edge flux is fixed reference subtraction or exact on the certified boundary class.",
            "what_would_close_zero": "derive boundary class owner, harmonic/corner control, reference subtraction, and source/test independence",
            "current_status": "route_open_not_closed",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "BOUNDARY_CLASS_OWNER_MISSING;REFERENCE_SUBTRACTION_NOT_SIGNED;SOURCE_TEST_INDEPENDENCE_NOT_SIGNED",
            "next_action": "treat topological exactness as a theorem target; do not use it as a closure axiom",
            "source_paths": source_paths(sources, "1041_noflux_exact", "1040_exactness_route"),
            "generated_utc": now,
        },
        {
            "row_id": "PBA3132_5",
            "route": "parent_primitive_verdict",
            "object": "3132_parent_action_boundary_primitive",
            "derived_or_attempted_form": "Parent primitive not derived from current corpus; concrete fallback is rho_surf=sum_i rho_i with sum_i |rho_i| <= retained cap.",
            "what_would_close_zero": "one parent route closes PBA3132_0 through PBA3132_4 in a single action/boundary class",
            "current_status": "zero_route_failed_for_claim_allocator_active",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": values["rho_cap"] if values["rho_cap"] is not None else "",
            "issues": "PARENT_PRIMITIVE_NOT_SIGNED;ALLOCATOR_REQUIRED",
            "next_action": "3133 should either prove absent-quotient parent map or fill first nonzero allocator component",
            "source_paths": source_paths(sources, "3131_next_fork", "3131_retained_cap", "1040_owner_verdict", "1021_primitive_gate", "1041_owner_gate"),
            "generated_utc": now,
        },
    ]


def allocator_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    values = cap_values(sources)
    rho_cap = values["rho_cap"]
    coefficient = values["surface_coefficient_abs"]
    threshold = values["threshold_abs"]
    delta_bound = values["deltaJ_bound_abs"]
    components = [
        ("ALLOC3132_1", "rho_nonexact_residual", "non-exact boundary residual r_surf", "prove r_surf=0 from parent variation or source a residual_edge_abs bound", "1021_primitive_gate"),
        ("ALLOC3132_2", "rho_corner_joint", "corner/joint charge from non-closed boundary or regulator surface", "prove partial boundary is empty or source a corner/joint charge bound", "1020_domain_verdict"),
        ("ALLOC3132_3", "rho_harmonic_cohomology", "harmonic/non-exact cohomology class h_surf", "prove H_edge projection vanishes or source harmonic_edge_abs", "1020_domain_verdict"),
        ("ALLOC3132_4", "rho_kernel_derivative", "weighted-Stokes derivative term d_S(F epsilon)", "prove d_S(F epsilon)=0 on allowed class or source norm_dS_Feps and norm_b", "1020_residual_bound"),
        ("ALLOC3132_5", "rho_reference_counterterm", "reference/counterterm mismatch between source and calibration", "prove fixed-before-readout reference silence or source Delta_ref coefficient", "1040_owner_verdict"),
        ("ALLOC3132_6", "rho_projector_readout", "Pi_M/readout mismatch feeding boundary charge into source mass", "prove Pi_M is fixed EH/Hamiltonian projector or source projector norm/residual", "1040_owner_verdict"),
        ("ALLOC3132_7", "rho_flux_poynting", "Poynting/radiative flux leakage through the worldtube boundary", "prove zero/averaged flux balance or source flux coefficient separately from static ADM mass", "3127_poynting_guard"),
        ("ALLOC3132_8", "rho_profile_worldtube", "profile/orbit/worldtube support mismatch between bulk Earth DD and actual source readout", "derive profile/worldtube projection or source an arena-specific rho_profile", "3130_surface_cap"),
    ]
    component_count = len(components)
    equal_budget = rho_cap / component_count if rho_cap is not None else None
    coefficient_budget = threshold / component_count if threshold is not None else None
    eta_budget = coefficient_budget * delta_bound if coefficient_budget is not None and delta_bound is not None else None
    now = stamp()
    rows: list[dict[str, Any]] = [
        {
            "row_id": "ALLOC3132_0",
            "component": "rho_surf_total_budget",
            "physical_meaning": "All retained boundary/profile/calibration leakage terms must fit inside the finite surface/binding cap.",
            "decomposition": "rho_surf = sum_i rho_i; pass only if sum_i |rho_i| <= rho_surf_cap",
            "rho_abs_budget_if_equal_split": equal_budget if equal_budget is not None else "",
            "DeltaC_abs_budget_if_equal_split": coefficient_budget if coefficient_budget is not None else "",
            "predicted_eta_abs_budget_if_equal_split": eta_budget if eta_budget is not None else "",
            "rho_surf_cap": rho_cap if rho_cap is not None else "",
            "surface_coefficient_abs": coefficient if coefficient is not None else "",
            "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "allocator_rule": "equal split is a diagnostic only; actual scoring uses the sum-absolute inequality, not cancellation",
            "status": "allocator_ready_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_or_proof_required": "all component rho_i rows require theorem-zero or numeric source-backed values",
            "source_paths": source_paths(sources, "3130_surface_cap", "3131_retained_cap"),
            "generated_utc": now,
        }
    ]
    for row_id, component, meaning, required, source_role in components:
        rows.append(
            {
                "row_id": row_id,
                "component": component,
                "physical_meaning": meaning,
                "decomposition": f"|{component}| contributes to sum_i |rho_i| <= rho_surf_cap",
                "rho_abs_budget_if_equal_split": equal_budget if equal_budget is not None else "",
                "DeltaC_abs_budget_if_equal_split": coefficient_budget if coefficient_budget is not None else "",
                "predicted_eta_abs_budget_if_equal_split": eta_budget if eta_budget is not None else "",
                "rho_surf_cap": rho_cap if rho_cap is not None else "",
                "surface_coefficient_abs": coefficient if coefficient is not None else "",
                "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
                "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
                "allocator_rule": "set to zero only by theorem; otherwise provide a numeric sourced value and add by absolute value",
                "status": "unfilled_component_nonclaim",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "source_or_proof_required": required,
                "source_paths": source_paths(sources, source_role, "3130_surface_cap"),
                "generated_utc": now,
            }
        )
    return rows


def gate_rows(proofs: list[dict[str, Any]], allocators: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    values = cap_values(sources)
    live_components = [row["component"] for row in allocators if row["row_id"] != "ALLOC3132_0"]
    return [
        {
            "gate_id": "PBAG3132_0",
            "gate": "parent_boundary_primitive_zero",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "B_surf/Q_X formula shape exists, but parent L_X/Theta_X/P_X, boundary class, reference, and primitive are not signed by one action.",
            "rho_surf_cap": values["rho_cap"] if values["rho_cap"] is not None else "",
            "live_components": ";".join(live_components),
            "next_action": "attempt absent-quotient parent map or first-class vertical generator before coefficient sourcing",
            "source_paths": source_paths(sources, "1040_charge_formula", "1040_owner_verdict", "1021_primitive_gate", "1041_owner_gate"),
        },
        {
            "gate_id": "PBAG3132_1",
            "gate": "rho_surf_allocator",
            "status": "active_nonclaim",
            "claim_allowed": "false",
            "reason": "Fallback is now executable as sum_i |rho_i| <= 0.3283734585378189; no cancellation between unknown components is allowed.",
            "rho_surf_cap": values["rho_cap"] if values["rho_cap"] is not None else "",
            "live_components": ";".join(live_components),
            "next_action": "fill or theorem-zero one allocator component at a time",
            "source_paths": source_paths(sources, "3130_surface_cap", "3131_retained_cap"),
        },
        {
            "gate_id": "PBAG3132_2",
            "gate": "best_next_route",
            "status": "queued",
            "claim_allowed": "false",
            "reason": "The least-scrutiny route is absent/nonprimitive quotient if it can be proven; second-best is vertical first-class constraint; fallback is first numeric allocator component.",
            "rho_surf_cap": values["rho_cap"] if values["rho_cap"] is not None else "",
            "live_components": ";".join(live_components),
            "next_action": "3133 absent-quotient source/readout map for surface/binding, or first allocator component fill",
            "source_paths": source_paths(sources, "1041_absent_quotient", "1041_vertical_constraint", "1020_residual_bound"),
        },
    ]


def validate(
    inputs: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    proofs: list[dict[str, Any]],
    allocators: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_columns = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    input_columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required_columns if column not in input_columns]
    unresolved = [role for role, payload in sources.items() if not payload["exists"] or not payload["found"]]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    values = cap_values(sources)
    rho_cap = values["rho_cap"]
    equal_rows = [row for row in allocators if row["row_id"] != "ALLOC3132_0"]
    equal_sum = sum(parse_float(row.get("rho_abs_budget_if_equal_split", "")) or 0.0 for row in equal_rows)
    equal_sum_matches = rho_cap is not None and abs(equal_sum - rho_cap) <= max(1e-15, abs(rho_cap) * 1e-12)
    primitive_promoted = any(str(row.get("zero_promoted", "")).lower() == "true" for row in proofs)
    claim_leaks = [
        row.get("row_id", "")
        for row in [*proofs, *allocators]
        if str(row.get("claim_allowed", "")).lower() != "false"
        or str(row.get("valid_for_claim", "")).lower() != "false"
    ]
    positive_numeric = (
        rho_cap is not None
        and rho_cap > 0
        and values["surface_coefficient_abs"] is not None
        and values["surface_coefficient_abs"] > 0
        and values["threshold_abs"] is not None
        and values["threshold_abs"] > 0
    )
    return [
        {
            "check_id": "VAL3132_0_input_schema",
            "status": "pass" if not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_1_source_rows_resolve",
            "status": "pass" if not unresolved else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_2_parent_primitive_not_promoted",
            "status": "pass" if not primitive_promoted else "fail",
            "details": "zero route remains unpromoted until one parent action owns L_X/Theta_X/P_X/boundary class/reference/primitive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_3_allocator_equal_budget_sums_to_cap",
            "status": "pass" if equal_sum_matches else "fail",
            "details": json.dumps({"equal_component_sum": equal_sum, "rho_surf_cap": rho_cap}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_4_no_claim_leak",
            "status": "pass" if not claim_leaks else "fail",
            "details": ";".join(claim_leaks),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_5_positive_numeric_gate",
            "status": "pass" if positive_numeric else "fail",
            "details": json.dumps(values, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3132_6_allocator_component_count",
            "status": "pass" if len(equal_rows) == 8 else "fail",
            "details": str(len(equal_rows)),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def main() -> None:
    inputs = base_inputs()
    write_csv(INPUT, inputs)
    sources = load_sources(inputs)
    proofs = proof_rows(sources)
    allocators = allocator_rows(sources)
    gates = gate_rows(proofs, allocators, sources)
    validations = validate(inputs, sources, proofs, allocators)
    write_csv(OUTPUT, proofs)
    write_csv(ALLOCATOR, allocators)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)
    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
