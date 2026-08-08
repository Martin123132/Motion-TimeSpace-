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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"

INPUT = OUT / "P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3131_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_GATE.csv"


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
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    residual_candidate = OUT / path_text
    if residual_candidate.exists():
        return residual_candidate
    return SOURCE_WEIGHT / path_text


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
    source_weight = "source-intake\\source-weight\\docs\\"
    return [
        {
            "source_id": "SRC3131_0",
            "role": "3130_zero_route",
            "source_file": residual + "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv",
            "source_row_id": "BBS3130_0",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "3130 exact boundary/common-worldtube zero route is conditional and unsigned.",
        },
        {
            "source_id": "SRC3131_1",
            "role": "3130_rho_cap",
            "source_file": residual + "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv",
            "source_row_id": "BBS3130_1",
            "row_id_column": "row_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "3130 finite residual cap for surface/binding mismatch.",
        },
        {
            "source_id": "SRC3131_2",
            "role": "Hilbert_EM_measure",
            "source_file": residual + "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
            "source_row_id": "WGT3127_0",
            "row_id_column": "derivation_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Hilbert EM energy measure is conditional on stationary source boundary choices.",
        },
        {
            "source_id": "SRC3131_3",
            "role": "Poynting_guard",
            "source_file": residual + "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
            "source_row_id": "WGT3127_4",
            "row_id_column": "derivation_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Poynting balance blocks using wave/flux channels as static source mass without closure.",
        },
        {
            "source_id": "SRC3131_4",
            "role": "source_descent_conditional",
            "source_file": source_weight + "AFRAME_GM_SOURCE_DESCENT_2125_NONCLAIM.csv",
            "source_row_id": "CMD2125_0_exact_conditional",
            "row_id_column": "descent_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Common-mode source descent theorem is written but conditional.",
        },
        {
            "source_id": "SRC3131_5",
            "role": "NoSourceOnlySpeciesSlot_missing",
            "source_file": source_weight + "AFRAME_GM_SOURCE_DESCENT_2125_NONCLAIM.csv",
            "source_row_id": "CMD2125_1_minimal_missing_clause",
            "row_id_column": "descent_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Minimal missing source-descent premise remains live.",
        },
        {
            "source_id": "SRC3131_6",
            "role": "measured_G_guard",
            "source_file": source_weight + "AFRAME_GM_SOURCE_DESCENT_2125_NONCLAIM.csv",
            "source_row_id": "CMD2125_3_measured_G_guard",
            "row_id_column": "descent_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Universal common mode can be calibrated once, but relative residuals cannot be hidden.",
        },
        {
            "source_id": "SRC3131_7",
            "role": "worldtube_reference_boundary",
            "source_file": residual + "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "source_row_id": "WG510_6_reference_zero_and_boundary",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Reference background, inner boundary, and outer linking surface compatibility is required.",
        },
        {
            "source_id": "SRC3131_8",
            "role": "parent_worldtube_glue",
            "source_file": residual + "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "source_row_id": "W504_4_worldtube_source_measure_glue",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Worldtube source measure and exterior Noether charge must read the same mass.",
        },
        {
            "source_id": "SRC3131_9",
            "role": "source_flux_closure",
            "source_file": residual + "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
            "source_row_id": "SM509_3_flux_closure",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Projected Hilbert mass current must close in source-free exterior domains.",
        },
        {
            "source_id": "SRC3131_10",
            "role": "source_worldtube_measure",
            "source_file": residual + "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
            "source_row_id": "SM509_4_worldtube_source_measure",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Worldtube source measure must equal exterior parent charge on linking spheres.",
        },
        {
            "source_id": "SRC3131_11",
            "role": "no_extra_channel",
            "source_file": residual + "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
            "source_row_id": "SM509_5_no_extra_channel",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Boundary, non-Hilbert, projector, memory, domain, range, and connection channels must carry no independent mass charge.",
        },
        {
            "source_id": "SRC3131_12",
            "role": "boundary_improvement_obstruction",
            "source_file": residual + "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
            "source_row_id": "OB501_2_boundary_improvement",
            "row_id_column": "obstruction_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Boundary/improvement term may have nonzero compact flux unless exact with zero integral or universally calibrated.",
        },
        {
            "source_id": "SRC3131_13",
            "role": "hidden_exchange_obstruction",
            "source_file": residual + "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
            "source_row_id": "OB501_3_hidden_exchange",
            "row_id_column": "obstruction_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Observed Hilbert matter may exchange mass-channel current with hidden/bulk/domain/non-EH sectors.",
        },
        {
            "source_id": "SRC3131_14",
            "role": "stationarity_or_flux_obstruction",
            "source_file": residual + "P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv",
            "source_row_id": "O504_3_stationarity_or_flux",
            "row_id_column": "obstruction_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Nonstationary systems can radiate or exchange charge through the annulus.",
        },
    ]


def load_sources(inputs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for row in inputs:
        path = source_path(str(row["source_file"]))
        source = find_row(read_csv(path), str(row["source_row_id"]), str(row["row_id_column"]))
        loaded[str(row["role"])] = {
            "input": row,
            "path": path,
            "row": source,
            "exists": path.exists(),
            "found": source is not None,
        }
    return loaded


def source_paths(sources: dict[str, dict[str, Any]], *roles: str) -> str:
    return ";".join(str(sources[role]["path"]) for role in roles)


def issue_join(*issues: str) -> str:
    return ";".join(issue for issue in issues if issue)


def row_status(sources: dict[str, dict[str, Any]], role: str) -> str:
    row = sources.get(role, {}).get("row") or {}
    return str(row.get("status") or row.get("current_result") or row.get("claim") or row.get("statement") or "")


def rho_cap(sources: dict[str, dict[str, Any]]) -> tuple[float | None, float | None, float | None, float | None]:
    row = sources.get("3130_rho_cap", {}).get("row") or {}
    cap = parse_float(row.get("residual_factor_max", ""))
    suppression = parse_float(row.get("suppression_min", ""))
    coefficient = parse_float(row.get("coefficient_abs", ""))
    threshold = parse_float(row.get("WEP_kernel_threshold_abs", ""))
    return cap, suppression, coefficient, threshold


def clause_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cap, suppression, coefficient, threshold = rho_cap(sources)
    live_blockers = [
        "boundary_exactness_cohomology",
        "same_worldtube_source_measure",
        "same_calibration_functional",
        "stationary_no_poynting_flux",
        "no_hidden_extra_mass_channel",
        "profile_readout_no_reentry",
    ]
    equal_budget = cap / len(live_blockers) if cap is not None else None
    now = stamp()
    theorem_conditions = [
        "B_surf is exact or cohomologically silent on the compact boundary partition",
        "source and calibration use the same fixed Hilbert-stress worldtube functional",
        "reference zero, boundary orientation, and normalization are shared before readout",
        "Poynting/radiative flux is zero, averaged, or explicitly separated from static ADM mass",
        "hidden/domain/non-EH channels carry no independent mass-channel exchange",
        "profile/readout/source labels do not re-enter after common-mode calibration",
    ]
    return [
        {
            "row_id": "BEX3131_0",
            "layer": "theorem_target",
            "clause": "boundary_exact_common_worldtube_zero",
            "statement": "If every 3131 clause is parent-signed, DeltaC_Scal,surf=0 and rho_surf=0 for the surface/binding common mode.",
            "mathematical_form": "C_surf[B]=int_{partial W_B} B_surf; DeltaC_Scal,surf=C_surf[S]-C_surf[cal]=0 under exact/common-worldtube/shared-calibration conditions",
            "evidence_status": "conditional_target_written",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": "",
            "issues": issue_join("ALL_CLAUSES_NOT_PARENT_SIGNED", "ZERO_ROUTE_CONDITIONAL_ONLY"),
            "next_action": "audit each theorem clause; if any stays unsigned, retain rho_surf finite cap",
            "source_paths": source_paths(sources, "3130_zero_route", "3130_rho_cap"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_1",
            "layer": "proof_clause",
            "clause": "boundary_exactness_cohomology",
            "statement": "The surface/binding contribution must be an exact boundary partition term or have zero compact boundary integral.",
            "mathematical_form": "int_{partial W} B_surf = int_{partial W} d_{partial} Lambda = int_{partial(partial W)} Lambda = 0, or a universal calibrated boundary constant",
            "evidence_status": "unsigned_obstruction_live",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("BOUNDARY_EXACTNESS_UNSIGNED", "BOUNDARY_IMPROVEMENT_NONZERO_FLUX_NOT_EXCLUDED"),
            "next_action": "derive B_surf=d_boundary Lambda with zero compact integral, or keep this as a residual component of rho_surf",
            "source_paths": source_paths(sources, "3130_zero_route", "boundary_improvement_obstruction"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_2",
            "layer": "proof_clause",
            "clause": "same_worldtube_source_measure",
            "statement": "Source and calibration must be evaluated on the same compact Hilbert/Noether worldtube measure before observable readout.",
            "mathematical_form": "M_source[W]=int_S Q_M[tau]=M_eff and the calibration body uses the same Q_M[tau], reference zero, and linking-surface convention",
            "evidence_status": "partial_downstream_route_not_signed",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("SAME_WORLDTUBE_CALIBRATION_UNSIGNED", "REFERENCE_ZERO_AND_BOUNDARY_COMPATIBILITY_REQUIRED"),
            "next_action": "map the surface/binding term into the parent worldtube charge rather than a separately weighted Earth bulk DD row",
            "source_paths": source_paths(sources, "worldtube_reference_boundary", "parent_worldtube_glue", "source_worldtube_measure"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_3",
            "layer": "proof_clause",
            "clause": "same_calibration_functional",
            "statement": "A universal common-mode source factor can be calibrated once, but a relative source/binding label cannot be hidden in measured G.",
            "mathematical_form": "DeltaC_Scal=C_J,S^ADM-C_J,cal^ADM; common factors cancel only if NoSourceOnlySpeciesSlot/source-label forgetting is parent-owned",
            "evidence_status": "conditional_common_mode_but_missing_species_slot",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("NOSOURCEONLYSPECIESSLOT_MISSING", "RELATIVE_SOURCE_VECTOR_LIVE", "MEASURED_G_GUARD_ACTIVE"),
            "next_action": "prove source-label forgetting before readout, or carry the binding mismatch as finite rho_surf",
            "source_paths": source_paths(sources, "source_descent_conditional", "NoSourceOnlySpeciesSlot_missing", "measured_G_guard"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_4",
            "layer": "proof_clause",
            "clause": "stationary_no_poynting_flux",
            "statement": "Static ADM/source-mass scoring requires no unresolved Poynting/radiative flux through the worldtube boundary, or a separate flux/readout coefficient.",
            "mathematical_form": "dE_EM/dt=-int_{partial Sigma} S dot dA - int_{Sigma} J dot E dV; static C_J^ADM uses only zero/averaged/closed flux branch",
            "evidence_status": "guard_present_not_zero_theorem",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("POYNTING_GUARD_PRESENT", "RADIATIVE_CLOSURE_NOT_SIGNED", "STATIONARITY_OR_FLUX_OBSTRUCTION_LIVE"),
            "next_action": "split static binding energy from wave/Poynting transport before allowing boundary cancellation to score",
            "source_paths": source_paths(sources, "Hilbert_EM_measure", "Poynting_guard", "source_flux_closure", "stationarity_or_flux_obstruction"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_5",
            "layer": "proof_clause",
            "clause": "no_hidden_extra_mass_channel",
            "statement": "Boundary, domain, memory, non-EH, projector, range, and connection channels must carry no independent mass-charge exchange in the local exterior.",
            "mathematical_form": "Delta_nonEH=Delta_symp=Delta_PiM=Delta_extra=0, or each retained channel enters rho_surf with a sourced coefficient",
            "evidence_status": "unsigned_extra_channel_silence",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("EXTRA_CHANNEL_SILENCE_UNSIGNED", "HIDDEN_EXCHANGE_OBSTRUCTION_LIVE"),
            "next_action": "derive no-exchange/no-hair for the local exterior or add channelwise residual coefficients",
            "source_paths": source_paths(sources, "no_extra_channel", "hidden_exchange_obstruction"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_6",
            "layer": "proof_clause",
            "clause": "profile_readout_no_reentry",
            "statement": "Bulk Earth DD rows cannot stand in for MICROSCOPE/orbit/source profile weighting; readout must not reintroduce source labels after calibration.",
            "mathematical_form": "rho_surf = P_profile[source worldtube, orbit, shell, calibration] acting on Q_surface_binding_Earth, not raw bulk Q_surface_binding_Earth",
            "evidence_status": "profile_factor_missing",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("PROFILE_WEIGHTED_VALUE_MISSING", "BULK_AS_PROFILE_REFUSED", "READOUT_REENTRY_NOT_EXCLUDED"),
            "next_action": "derive or fill rho_surf profile/worldtube factor; required cap remains exactly the 3130 value",
            "source_paths": source_paths(sources, "3130_rho_cap", "NoSourceOnlySpeciesSlot_missing"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_7",
            "layer": "finite_cap_retention",
            "clause": "rho_surf_retained_bound",
            "statement": "Because at least one zero-proof clause remains unsigned, the surface/binding branch must retain the 3130 finite residual cap.",
            "mathematical_form": "|rho_surf Q_surface_binding_Earth| <= DeltaC_threshold, so |rho_surf| <= DeltaC_threshold/|Q_surface_binding_Earth|",
            "evidence_status": "finite_bound_retained_nonclaim",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("ZERO_PROOF_FAILED_FOR_CLAIM", "RHO_SURF_PROFILE_OR_CALIBRATION_FACTOR_REQUIRED"),
            "next_action": "either close all six theorem clauses or derive a profile/calibration rho_surf below the cap",
            "source_paths": source_paths(sources, "3130_rho_cap"),
            "generated_utc": now,
        },
        {
            "row_id": "BEX3131_8",
            "layer": "decision",
            "clause": "next_fork",
            "statement": "The non-cheat route is now sharply split: prove exact boundary/common-worldtube cancellation, or derive the finite profile/worldtube suppression factor.",
            "mathematical_form": "zero_route=false unless all theorem_conditions are parent-signed; otherwise score rho_surf with cap retained",
            "evidence_status": "move_to_profile_or_parent_action_clause",
            "zero_promoted": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "suppression_min_retained": suppression if suppression is not None else "",
            "equal_no_cancellation_component_budget": equal_budget if equal_budget is not None else "",
            "issues": issue_join("NEXT_TARGET_REQUIRED", "CLAIM_BLOCKED"),
            "next_action": "3132 should attempt a parent-action boundary exactness clause; if not found, build executable rho_surf profile/worldtube allocator",
            "source_paths": source_paths(sources, "3130_zero_route", "3130_rho_cap", "Poynting_guard", "source_descent_conditional"),
            "generated_utc": now,
        },
    ]


def gate_rows(outputs: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cap, suppression, coefficient, threshold = rho_cap(sources)
    unsigned = [
        row["clause"]
        for row in outputs
        if row.get("layer") == "proof_clause" and row.get("zero_promoted") != "true"
    ]
    return [
        {
            "gate_id": "BEXG3131_0",
            "gate": "boundary_exact_zero_promotion",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "Zero theorem is not promoted because proof clauses remain unsigned.",
            "live_blockers": ";".join(unsigned),
            "rho_surf_cap_retained": cap if cap is not None else "",
            "next_action": "close all proof clauses from parent action/worldtube identity or keep finite rho_surf scoring",
            "source_paths": source_paths(sources, "3130_zero_route", "boundary_improvement_obstruction"),
        },
        {
            "gate_id": "BEXG3131_1",
            "gate": "finite_surface_binding_cap",
            "status": "pass_as_nonclaim_bound",
            "claim_allowed": "false",
            "reason": "3130 cap is retained as the strict finite fallback.",
            "live_blockers": "rho_surf_profile_or_calibration_factor_unfilled",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "next_action": f"derive rho_surf <= {cap}" if cap is not None else "derive rho_surf below retained cap",
            "source_paths": source_paths(sources, "3130_rho_cap"),
        },
        {
            "gate_id": "BEXG3131_2",
            "gate": "method_fork_guard",
            "status": "active",
            "claim_allowed": "false",
            "reason": "Do not reject a branch only because its internal time/flow variable looks opposite to GR; first map the observed clock/metric limit and residual channel.",
            "live_blockers": "observed_limit_map_required_before_time_language_rejection",
            "rho_surf_cap_retained": cap if cap is not None else "",
            "next_action": "apply this as a fork heuristic only; it is not evidence and cannot promote a physics claim",
            "source_paths": source_paths(sources, "3130_zero_route"),
        },
        {
            "gate_id": "BEXG3131_3",
            "gate": "next_target",
            "status": "queued",
            "claim_allowed": "false",
            "reason": "Best next target is parent-action boundary exactness; fallback is executable rho_surf profile/worldtube allocation.",
            "live_blockers": ";".join(unsigned),
            "rho_surf_cap_retained": cap if cap is not None else "",
            "next_action": "3132 parent-action boundary exactness clause or rho_surf allocator",
            "source_paths": source_paths(sources, "worldtube_reference_boundary", "source_flux_closure", "no_extra_channel"),
        },
    ]


def validate(inputs: list[dict[str, Any]], sources: dict[str, dict[str, Any]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    input_columns = set(inputs[0].keys()) if inputs else set()
    missing = [column for column in required if column not in input_columns]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    unresolved = [role for role, payload in sources.items() if not payload["exists"] or not payload["found"]]
    cap, suppression, coefficient, threshold = rho_cap(sources)
    recomputed = threshold / abs(coefficient) if threshold is not None and coefficient not in (None, 0.0) else None
    cap_matches = (
        cap is not None
        and recomputed is not None
        and abs(cap - recomputed) <= max(1e-15, abs(recomputed) * 1e-12)
    )
    zero_promoted = any(str(row.get("zero_promoted", "")).lower() == "true" for row in outputs)
    claim_leak = [
        row.get("row_id", "")
        for row in outputs
        if str(row.get("claim_allowed", "")).lower() != "false"
        or str(row.get("valid_for_claim", "")).lower() != "false"
    ]
    live_clause_count = len([row for row in outputs if row.get("layer") == "proof_clause"])
    return [
        {
            "check_id": "VAL3131_0_input_schema",
            "status": "pass" if not missing else "fail",
            "details": ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3131_1_source_rows_resolve",
            "status": "pass" if not unresolved else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3131_2_zero_not_promoted",
            "status": "pass" if not zero_promoted else "fail",
            "details": "zero theorem remains conditional because at least one proof clause is unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3131_3_rho_cap_reproduces_3130",
            "status": "pass" if cap_matches else "fail",
            "details": json.dumps(
                {
                    "rho_surf_cap": cap,
                    "recomputed_threshold_over_coefficient": recomputed,
                    "coefficient_abs": coefficient,
                    "threshold_abs": threshold,
                    "suppression_min": suppression,
                },
                sort_keys=True,
            ),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3131_4_no_claim_leak",
            "status": "pass" if not claim_leak else "fail",
            "details": ";".join(claim_leak),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3131_5_live_clause_count",
            "status": "pass" if live_clause_count == 6 else "fail",
            "details": str(live_clause_count),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def main() -> None:
    inputs = base_inputs()
    write_csv(INPUT, inputs)
    sources = load_sources(inputs)
    outputs = clause_rows(sources)
    gates = gate_rows(outputs, sources)
    validations = validate(inputs, sources, outputs)
    write_csv(OUTPUT, outputs)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)
    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
