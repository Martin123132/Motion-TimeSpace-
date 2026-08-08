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

INPUT = OUT / "P8_Y5_R2FR_3133_ABSENT_QUOTIENT_PROFILE_INPUTS.csv"
QUOTIENT = OUT / "P8_Y5_R2FR_3133_ABSENT_QUOTIENT_ATTEMPT.csv"
PROFILE = OUT / "P8_Y5_R2FR_3133_RHO_PROFILE_WORLDTUBE_FIRST_ROW.csv"
GATE = OUT / "P8_Y5_R2FR_3133_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3133_VALIDATION.csv"


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
    text = str(value).strip()
    if text.lower() == "inf":
        return math.inf
    try:
        parsed = float(text)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed):
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
    beta = "source-intake\\beta-source\\docs\\"
    return [
        {
            "source_id": "SRC3133_0",
            "role": "3132_best_next",
            "source_file": residual + "P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_GATE.csv",
            "source_row_id": "PBAG3132_2",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "3132 handoff: absent quotient or first allocator component.",
        },
        {
            "source_id": "SRC3133_1",
            "role": "3132_profile_allocator",
            "source_file": residual + "P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv",
            "source_row_id": "ALLOC3132_8",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "rho_profile_worldtube allocator component.",
        },
        {
            "source_id": "SRC3133_2",
            "role": "3130_surface_cap",
            "source_file": residual + "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv",
            "source_row_id": "BBS3130_1",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "surface/binding cap and bulk coefficient.",
        },
        {
            "source_id": "SRC3133_3",
            "role": "2790_profile_grid",
            "source_file": residual + "P8_Y5_R2FR_2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
            "source_row_id": "PROFILE2790_long_range_mass_average",
            "row_id_column": "profile_row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "numeric two-layer DD profile smoke grid.",
        },
        {
            "source_id": "SRC3133_4",
            "role": "2790_profile_kernel",
            "source_file": residual + "P8_Y5_R2FR_2790_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
            "source_row_id": "K2790_1_effective_source_charge",
            "row_id_column": "kernel_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "profile-weighted effective source charge rule.",
        },
        {
            "source_id": "SRC3133_5",
            "role": "2790_profile_gate",
            "source_file": residual + "P8_Y5_R2FR_2790_PROFILE_CLOSURE_GATES.csv",
            "source_row_id": "PCG2790_1_finite_range_profile",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "PREM/profile/lambda owner gate.",
        },
        {
            "source_id": "SRC3133_6",
            "role": "2790_readout_gate",
            "source_file": residual + "P8_Y5_R2FR_2790_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "source_row_id": "RIG2790_0_CMSM_arrays",
            "row_id_column": "readout_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "official MICROSCOPE readout array gate.",
        },
        {
            "source_id": "SRC3133_7",
            "role": "2792_chain_rule_zero",
            "source_file": beta + "WEP_SOURCE_CURRENT_OR_DD_MAP_2792_NONCLAIM.csv",
            "source_row_id": "SCZ2792_0_chain_rule_zero",
            "row_id_column": "attempt_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "conditional quotient/matter descent source-current zero.",
        },
        {
            "source_id": "SRC3133_8",
            "role": "2792_counterexample",
            "source_file": beta + "WEP_SOURCE_CURRENT_OR_DD_MAP_2792_NONCLAIM.csv",
            "source_row_id": "SCZ2792_2_pre_action_weight_leak",
            "row_id_column": "attempt_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "pre-action species/source weight counterexample.",
        },
        {
            "source_id": "SRC3133_9",
            "role": "2792_verdict",
            "source_file": beta + "WEP_SOURCE_CURRENT_OR_DD_MAP_2792_NONCLAIM.csv",
            "source_row_id": "SCZ2792_6_verdict",
            "row_id_column": "attempt_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "WEP source/test current zero verdict.",
        },
        {
            "source_id": "SRC3133_10",
            "role": "2796_synthesis_zero",
            "source_file": beta + "WEP_SIGNATURE_SYNTHESIS_OR_CLOSURE_2796_NONCLAIM.csv",
            "source_row_id": "SYN2796_7_zero_theorem_if_signed",
            "row_id_column": "synthesis_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "assembled quotient/object-language zero theorem if signed.",
        },
        {
            "source_id": "SRC3133_11",
            "role": "2796_verdict",
            "source_file": beta + "WEP_SIGNATURE_SYNTHESIS_OR_CLOSURE_2796_NONCLAIM.csv",
            "source_row_id": "SYN2796_8_verdict",
            "row_id_column": "synthesis_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "synthesis verdict: parent signature still unsigned.",
        },
        {
            "source_id": "SRC3133_12",
            "role": "2772_forbidden_slot",
            "source_file": beta + "NO_SOURCE_ONLY_SLOT_2772_NONCLAIM.csv",
            "source_row_id": "AAG2772_4_source_only_species_scalar",
            "row_id_column": "grammar_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "candidate grammar forbids inert source-only species scalar, but not parent signed.",
        },
    ]


def load_sources(inputs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for input_row in inputs:
        path = source_path(str(input_row["source_file"]))
        row = find_row(read_csv(path), str(input_row["source_row_id"]), str(input_row["row_id_column"]))
        sources[str(input_row["role"])] = {
            "input": input_row,
            "path": path,
            "row": row,
            "exists": path.exists(),
            "found": row is not None,
        }
    return sources


def source_paths(sources: dict[str, dict[str, Any]], *roles: str) -> str:
    return ";".join(str(sources[role]["path"]) for role in roles)


def cap_values(sources: dict[str, dict[str, Any]]) -> dict[str, float | None]:
    cap_row = sources.get("3130_surface_cap", {}).get("row") or {}
    alloc_row = sources.get("3132_profile_allocator", {}).get("row") or {}
    return {
        "bulk_surface": parse_float(cap_row.get("coefficient_abs", "")),
        "rho_total_cap": parse_float(cap_row.get("residual_factor_max", "")),
        "rho_equal_budget": parse_float(alloc_row.get("rho_abs_budget_if_equal_split", "")),
        "delta_c_equal_budget": parse_float(alloc_row.get("DeltaC_abs_budget_if_equal_split", "")),
        "eta_equal_budget": parse_float(alloc_row.get("predicted_eta_abs_budget_if_equal_split", "")),
        "delta_j_bound": parse_float(cap_row.get("deltaJ_bound_abs", "")),
    }


def quotient_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    values = cap_values(sources)
    now = stamp()
    return [
        {
            "row_id": "AQ3133_0",
            "route": "absent_nonprimitive_quotient_target",
            "statement": "If the surface/binding response is only a quotient/readout coordinate and not an independent parent field, its vertical variation has no source current.",
            "mathematical_form": "S_matter=Sbar[q(Phi),Psi,theta_A], Dq[v_X]=0, Lie_vX(theta_A)=0 => delta_vX S_matter=0 and qbar_XT=0",
            "current_status": "conditional_chain_rule_available",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_profile_budget": values["rho_equal_budget"] if values["rho_equal_budget"] is not None else "",
            "issues": "QUOTIENT_MAP_NOT_PARENT_SIGNED;MATTER_DESCENT_NOT_PARENT_SIGNED",
            "next_action": "construct the actual parent quotient map and matter pullback, or keep profile allocator active",
            "source_paths": source_paths(sources, "2792_chain_rule_zero", "2796_synthesis_zero"),
            "generated_utc": now,
        },
        {
            "row_id": "AQ3133_1",
            "route": "object_language_no_source_slot",
            "statement": "An inert source-only species scalar would be forbidden by the candidate object language, but the grammar is not yet a parent action theorem.",
            "mathematical_form": "no independent w_A S_A or w_source q_surface slot unless carried by observable fields/currents/representation data",
            "current_status": "grammar_contract_not_parent_signed",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_profile_budget": values["rho_equal_budget"] if values["rho_equal_budget"] is not None else "",
            "issues": "NO_SOURCE_ONLY_SLOT_UNSIGNED;ACTION_MEASURE_OWNER_UNSIGNED",
            "next_action": "derive action-measure/current owner that removes source labels before variation",
            "source_paths": source_paths(sources, "2772_forbidden_slot", "2796_synthesis_zero"),
            "generated_utc": now,
        },
        {
            "row_id": "AQ3133_2",
            "route": "countermodel_guard",
            "statement": "If species/source weights are inserted before variation, a Hilbert current can carry the binding/source label even though post-variation rescaling is forbidden.",
            "mathematical_form": "S_matter=sum_A w_A S_A remains a legal countermodel unless the parent grammar/measure forbids w_A before variation",
            "current_status": "countermodel_live",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_profile_budget": values["rho_equal_budget"] if values["rho_equal_budget"] is not None else "",
            "issues": "PRE_ACTION_WEIGHT_LEAK_LIVE;POST_VARIATION_OWNER_NOT_ENOUGH",
            "next_action": "do not promote quotient zero until pre-action source weights are excluded by parent syntax",
            "source_paths": source_paths(sources, "2792_counterexample", "2792_verdict"),
            "generated_utc": now,
        },
        {
            "row_id": "AQ3133_3",
            "route": "quotient_verdict",
            "statement": "The absent/nonprimitive quotient route remains the cleanest route, but it is not closed; the first profile allocator diagnostic is therefore active.",
            "mathematical_form": "zero_route=false; use rho_profile_worldtube diagnostic row while qbar_XT/source descent remains unsigned",
            "current_status": "zero_route_failed_for_claim_profile_allocator_active",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_profile_budget": values["rho_equal_budget"] if values["rho_equal_budget"] is not None else "",
            "issues": "PARENT_SIGNATURE_UNSIGNED;PROFILE_ALLOCATOR_REQUIRED",
            "next_action": "3134 should either write the parent quotient map or upgrade rho_profile_worldtube with PREM/lambda/readout inputs",
            "source_paths": source_paths(sources, "3132_best_next", "2796_verdict", "3132_profile_allocator"),
            "generated_utc": now,
        },
    ]


def profile_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    values = cap_values(sources)
    grid_path = sources["2790_profile_grid"]["path"]
    grid = read_csv(grid_path)
    bulk_abs = values["bulk_surface"]
    total_cap = values["rho_total_cap"]
    equal_budget = values["rho_equal_budget"]
    delta_j = values["delta_j_bound"]
    rows: list[dict[str, Any]] = []
    profile_values: list[dict[str, Any]] = []
    for grid_row in grid:
        delta_surface = parse_float(grid_row.get("delta_surface_vs_2789_bulk", ""))
        rho_profile_abs = abs(delta_surface) / bulk_abs if delta_surface is not None and bulk_abs not in (None, 0.0) else None
        delta_c_abs = abs(delta_surface) if delta_surface is not None else None
        eta_abs = delta_c_abs * delta_j if delta_c_abs is not None and delta_j is not None else None
        profile_values.append(
            {
                "grid_row": grid_row,
                "rho_profile_abs": rho_profile_abs,
                "delta_c_abs": delta_c_abs,
                "eta_abs": eta_abs,
            }
        )
    max_profile = max(
        (entry for entry in profile_values if entry["rho_profile_abs"] is not None),
        key=lambda entry: entry["rho_profile_abs"],
        default=None,
    )
    max_rho = max_profile["rho_profile_abs"] if max_profile is not None else None
    max_delta = max_profile["delta_c_abs"] if max_profile is not None else None
    max_eta = max_profile["eta_abs"] if max_profile is not None else None
    max_label = max_profile["grid_row"].get("lambda_label", "") if max_profile is not None else ""
    now = stamp()
    rows.append(
        {
            "row_id": "RHO3133_0_profile_worldtube_summary",
            "lambda_label": "max_abs_over_2790_smoke_grid",
            "lambda_over_R_E": "",
            "Q_surface_binding_bulk_abs": bulk_abs if bulk_abs is not None else "",
            "Q_surface_binding_eff": "",
            "delta_surface_vs_bulk": max_delta if max_delta is not None else "",
            "rho_profile_abs": max_rho if max_rho is not None else "",
            "rho_equal_component_budget": equal_budget if equal_budget is not None else "",
            "rho_total_cap": total_cap if total_cap is not None else "",
            "within_equal_budget": str(max_rho is not None and equal_budget is not None and max_rho <= equal_budget).lower(),
            "within_total_cap": str(max_rho is not None and total_cap is not None and max_rho <= total_cap).lower(),
            "predicted_eta_abs_at_deltaJ": max_eta if max_eta is not None else "",
            "profile_model": "two_layer_uniform_core_mantle_candidate",
            "status": "diagnostic_profile_component_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SMOKE_GRID_NOT_PREM;LAMBDA_WEP_NOT_PARENT_OWNED;OFFICIAL_READOUT_NOT_IMPORTED;PARENT_TO_DD_MAP_UNSIGNED",
            "next_action": f"upgrade max row {max_label} with parent lambda, PREM/shell profile, official readout, and parent-to-DD map",
            "source_paths": source_paths(sources, "2790_profile_grid", "2790_profile_gate", "2790_readout_gate", "2790_profile_kernel"),
            "generated_utc": now,
        }
    )
    for index, entry in enumerate(profile_values, start=1):
        grid_row = entry["grid_row"]
        rho = entry["rho_profile_abs"]
        rows.append(
            {
                "row_id": f"RHO3133_{index}_{grid_row.get('lambda_label', 'profile')}",
                "lambda_label": grid_row.get("lambda_label", ""),
                "lambda_over_R_E": grid_row.get("lambda_over_R_E", ""),
                "Q_surface_binding_bulk_abs": bulk_abs if bulk_abs is not None else "",
                "Q_surface_binding_eff": grid_row.get("Q_surface_binding_eff", ""),
                "delta_surface_vs_bulk": grid_row.get("delta_surface_vs_2789_bulk", ""),
                "rho_profile_abs": rho if rho is not None else "",
                "rho_equal_component_budget": equal_budget if equal_budget is not None else "",
                "rho_total_cap": total_cap if total_cap is not None else "",
                "within_equal_budget": str(rho is not None and equal_budget is not None and rho <= equal_budget).lower(),
                "within_total_cap": str(rho is not None and total_cap is not None and rho <= total_cap).lower(),
                "predicted_eta_abs_at_deltaJ": entry["eta_abs"] if entry["eta_abs"] is not None else "",
                "profile_model": grid_row.get("profile_model", ""),
                "status": "profile_smoke_row_nonclaim",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "issues": "TWO_LAYER_SMOKE_ONLY;PHYSICAL_PROFILE_INPUTS_MISSING",
                "next_action": "replace with PREM/shell profile and parent-owned lambda/readout before scoring",
                "source_paths": str(grid_path),
                "generated_utc": now,
            }
        )
    return rows


def gate_rows(quotient: list[dict[str, Any]], profile: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    summary = profile[0] if profile else {}
    return [
        {
            "gate_id": "AQPG3133_0",
            "gate": "absent_quotient_zero",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "Quotient/matter descent chain-rule zero is conditional but parent signature and no-source-only-slot theorem remain unsigned.",
            "diagnostic_rho_profile_abs": summary.get("rho_profile_abs", ""),
            "next_action": "write the parent quotient map and matter pullback, or keep finite allocator scoring",
            "source_paths": source_paths(sources, "2792_chain_rule_zero", "2796_verdict", "2772_forbidden_slot"),
        },
        {
            "gate_id": "AQPG3133_1",
            "gate": "rho_profile_worldtube_first_row",
            "status": "diagnostic_nonclaim",
            "claim_allowed": "false",
            "reason": "Two-layer profile smoke gives a numeric rho_profile diagnostic, but not a claim-grade source profile.",
            "diagnostic_rho_profile_abs": summary.get("rho_profile_abs", ""),
            "next_action": "upgrade to parent-owned lambda plus PREM/shell profile plus MICROSCOPE readout arrays",
            "source_paths": source_paths(sources, "2790_profile_grid", "2790_profile_gate", "2790_readout_gate"),
        },
        {
            "gate_id": "AQPG3133_2",
            "gate": "next_target",
            "status": "queued",
            "claim_allowed": "false",
            "reason": "Best next move is a concrete parent quotient map; best data fallback is a PREM/lambda/readout rho_profile upgrade.",
            "diagnostic_rho_profile_abs": summary.get("rho_profile_abs", ""),
            "next_action": "3134 parent quotient map or PREM/source-shell profile import",
            "source_paths": source_paths(sources, "3132_best_next", "3132_profile_allocator"),
        },
    ]


def validate(
    inputs: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    quotient: list[dict[str, Any]],
    profile: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_columns = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    input_columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required_columns if column not in input_columns]
    unresolved = [role for role, payload in sources.items() if not payload["exists"] or not payload["found"]]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    grid = read_csv(sources["2790_profile_grid"]["path"])
    numeric_profile_rows = [
        row
        for row in profile[1:]
        if parse_float(row.get("rho_profile_abs", "")) is not None
    ]
    summary = profile[0] if profile else {}
    max_rho_summary = parse_float(summary.get("rho_profile_abs", ""))
    recomputed_max = max(
        (parse_float(row.get("rho_profile_abs", "")) or 0.0 for row in profile[1:]),
        default=0.0,
    )
    total_cap = parse_float(summary.get("rho_total_cap", ""))
    quotient_promoted = any(str(row.get("zero_promoted", "")).lower() == "true" for row in quotient)
    claim_leaks = [
        row.get("row_id", "")
        for row in [*quotient, *profile]
        if str(row.get("claim_allowed", "")).lower() != "false"
        or str(row.get("valid_for_claim", "")).lower() != "false"
    ]
    return [
        {
            "check_id": "VAL3133_0_input_schema",
            "status": "pass" if not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_1_source_rows_resolve",
            "status": "pass" if not unresolved else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_2_quotient_not_promoted",
            "status": "pass" if not quotient_promoted else "fail",
            "details": "absent/nonprimitive quotient remains conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_3_profile_grid_numeric",
            "status": "pass" if len(grid) >= 7 and len(numeric_profile_rows) == len(grid) else "fail",
            "details": json.dumps({"grid_rows": len(grid), "numeric_profile_rows": len(numeric_profile_rows)}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_4_profile_summary_max_recomputes",
            "status": "pass" if max_rho_summary is not None and abs(max_rho_summary - recomputed_max) <= max(1e-15, abs(recomputed_max) * 1e-12) else "fail",
            "details": json.dumps({"summary_max": max_rho_summary, "recomputed_max": recomputed_max}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_5_profile_within_total_cap_as_diagnostic",
            "status": "pass" if max_rho_summary is not None and total_cap is not None and max_rho_summary <= total_cap else "fail",
            "details": json.dumps({"summary_max": max_rho_summary, "rho_total_cap": total_cap}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3133_6_no_claim_leak",
            "status": "pass" if not claim_leaks else "fail",
            "details": ";".join(claim_leaks),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def main() -> None:
    inputs = base_inputs()
    write_csv(INPUT, inputs)
    sources = load_sources(inputs)
    quotient = quotient_rows(sources)
    profile = profile_rows(sources)
    gates = gate_rows(quotient, profile, sources)
    validations = validate(inputs, sources, quotient, profile)
    write_csv(QUOTIENT, quotient)
    write_csv(PROFILE, profile)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)
    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
