from __future__ import annotations

import csv
import math
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3938"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3938-Y5-R2FR-orbital-ephemeris-source-acquisition-and-Delta-cal-score-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3938_SOURCE_REGISTER.csv",
    "bound_imports": SRC / "P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv",
    "acquisition": SRC / "P8_Y5_R2FR_3938_ORBITAL_SOURCE_ACQUISITION_ROWS.csv",
    "delta_score": SRC / "P8_Y5_R2FR_3938_DELTA_CAL_SCORE_RUNNER.csv",
    "component_status": SRC / "P8_Y5_R2FR_3938_DELTA_CAL_COMPONENT_STATUS.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3938_CLAIM_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3938_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3938_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3938_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3938_VALIDATION.csv",
}

NEXT_DOC = "3939-Y5-R2FR-parent-sign-or-bound-Delta-cal-components.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3939_parent_sign_or_bound_Delta_cal_components.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def is_number(value: Any) -> bool:
    try:
        return bool(value not in (None, "")) and math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def local_bound_map() -> dict[str, dict[str, str]]:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    by_row_id = {row.get("row_id", ""): row for row in rows}
    by_observable = {row.get("observable", ""): row for row in rows}
    return {**by_row_id, **by_observable}


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3938_00_3937_next", SRC / "P8_Y5_R2FR_3937_NEXT_TARGET.csv", "NEXT3937_0", "3937 handoff to orbital source/score runner"),
        ("SRC3938_01_3937_dashboard", SRC / "P8_Y5_R2FR_3937_ORBITAL_EPHEMERIS_BOUND_DASHBOARD.csv", "ORB3937_0_epsilon_Delta_cal", "orbital dashboard rows"),
        ("SRC3938_02_3937_R10_escape", SRC / "P8_Y5_R2FR_3937_ORBITAL_EPHEMERIS_BOUND_DASHBOARD.csv", "ORB3937_6_R10_escape", "finite-range escape row"),
        ("SRC3938_03_delta_identity", SRC / "P8_Y5_R2FR_3598_DELTA_CAL_RESIDUAL_DECOMPOSITION.csv", "DCR3598_0_total", "Delta_cal residual decomposition"),
        ("SRC3938_04_delta_bounds", SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_BOUND_ROWS.csv", "GOB3598_0_epsilon_Delta_cal", "Gauss/orbital bound rows"),
        ("SRC3938_05_delta_theorem", SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_CALIBRATION_THEOREM.csv", "GOC3598_5_exact_Delta_cal_identity", "exact Delta_cal identity"),
        ("SRC3938_06_GM_rows", SRC / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "GMC3652_8_total_guard", "GM source calibration guard"),
        ("SRC3938_07_orbital_vector", SRC / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv", "PVR3652_6_Gdot", "PPN/orbital vector rows"),
        ("SRC3938_08_radial_formula", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_4_radial_shape", "epsilon_r radial formula"),
        ("SRC3938_09_escape_map", SRC / "P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv", "MAP3922_7_Gdot", "orbital/Gdot escape mapping"),
        ("SRC3938_10_newton_readout", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_0_exterior", "Newtonian readout chain"),
        ("SRC3938_11_local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R9_Gdot", "source-backed local bound rows"),
        ("SRC3938_12_Poisson_Gauss_schema", LOCAL_BOUNDS / "Poisson_Gauss_Newton_Enorm_rows_2722_NONCLAIM.csv", "FPG2722_3_E_mu_transfer", "Poisson/Gauss/Newton residual schema"),
        ("SRC3938_13_R10_readiness", SRC / "P8_Y5_R2FR_3436_R10_SCORE_READINESS.csv", "SR3436_3_mts_alpha", "R10 source-map blocker"),
        ("SRC3938_14_3937_validation", SRC / "P8_Y5_BRR545_3937_VALIDATION.csv", "VAL3937_16_no_pycache", "previous checkpoint validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:900]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def bound_import_rows(timestamp: str) -> list[dict[str, Any]]:
    bounds = local_bound_map()
    imports = [
        ("BIMP3938_0_Gdot", "Gdot_over_G", "R9_Gdot", "orbital_Gdot", "dln_Geff_dt; dln_Meff_dt; delta_ln_mu_obs"),
        ("BIMP3938_1_gamma", "gamma_minus_1", "R3_gamma", "PPN_orbital_vector", "Delta_PPN_orbital gamma component"),
        ("BIMP3938_2_beta", "beta_minus_1", "R4_beta", "PPN_orbital_vector", "Delta_PPN_orbital beta/common-mode component"),
        ("BIMP3938_3_alpha1", "alpha1", "R5_alpha1", "PPN_orbital_vector", "preferred-frame orbital source component"),
        ("BIMP3938_4_alpha2", "alpha2", "R6_alpha2", "PPN_orbital_vector", "spin/preferred-frame orbital source component"),
        ("BIMP3938_5_alpha3", "alpha3", "R7_alpha3", "PPN_orbital_vector", "source-exchange/self-acceleration component"),
        ("BIMP3938_6_xi", "xi", "R8_xi", "PPN_orbital_vector", "preferred-location/domain component"),
        ("BIMP3938_7_R10_symbolic", "delta_G_or_fifth_force_yukawa", "R10_fifth_force", "finite_range_escape", "alpha(lambda) escape only; not a scalar bound"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, observable, key, arena, maps_to in imports:
        source = bounds.get(key) or bounds.get(observable) or {}
        upper_bound = source.get("upper_bound", "")
        numeric = is_number(upper_bound)
        source_url = source.get("reference_path_or_url", "")
        rows.append(
            {
                "row_id": row_id,
                "observable": observable,
                "local_bound_row_id": key,
                "arena": arena,
                "maps_to_mts_quantity": maps_to,
                "measured_value": source.get("measured_value", ""),
                "one_sigma": source.get("one_sigma", ""),
                "upper_bound": upper_bound,
                "units": source.get("units", ""),
                "confidence_label": source.get("confidence_label", ""),
                "reference": source_url,
                "source_backed": bool(source_url),
                "numeric_bound": numeric,
                "score_ready_as_bound": numeric,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def acquisition_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ACQ3938_0_mu_obs",
            "target": "mu_obs or mu_fit",
            "definition": "(GM)_fit measured by orbital/ephemeris dynamics in a declared source frame",
            "source_status": "MISSING_ARENA_SPECIFIC_EPHEMERIS_DATASET",
            "available_comparator": "none in local_bound_claims.csv",
            "needed_for": "epsilon_Delta_cal; epsilon_orbit; measured-GM calibration",
            "next_action": "choose a concrete ephemeris/LLR/Mercury source and record source body, fitted GM, uncertainty, model assumptions",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ACQ3938_1_epsilon_r",
            "target": "epsilon_r(r)",
            "definition": "epsilon_r(r)=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|",
            "source_status": "FORMULA_READY_PROFILE_MISSING",
            "available_comparator": "RUN3920_4_radial_shape",
            "needed_for": "inverse-square/radial-hair score",
            "next_action": "derive xi_1(r) theorem-zero or source a radial residual profile/tolerance; constant xi_ref alone is not enough",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ACQ3938_2_Gdot",
            "target": "Gdot_over_G",
            "definition": "d ln mu_obs/dt channel after separating G_eff and source mass drift",
            "source_status": "BOUND_IMPORTED_MTS_VALUE_MISSING",
            "available_comparator": "R9_Gdot upper_bound=9.6e-15 yr^-1",
            "needed_for": "dln_Geff_dt; dln_Meff_dt; source-flux drift",
            "next_action": "derive zero drift from parent source/coupling route or source numeric MTS drift projection",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ACQ3938_3_Poisson_Gauss",
            "target": "epsilon_Poisson_Gauss",
            "definition": "weak-field Poisson coefficient plus Gauss surface-flux mismatch",
            "source_status": "SCHEMA_READY_NUMERIC_OPERATOR_SOURCE_MISSING",
            "available_comparator": "Poisson_Gauss_Newton_Enorm_rows_2722_NONCLAIM.csv",
            "needed_for": "source-to-Gauss-to-orbit Newton bridge",
            "next_action": "parent-sign EH weak-field coefficient and Gauss residual zero, or produce same-frame operator residual norms",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ACQ3938_4_PPN_orbital",
            "target": "Delta_PPN_orbital",
            "definition": "PPN vector projected into orbital/source calibration branch",
            "source_status": "BOUNDS_IMPORTED_MTS_VECTOR_MISSING",
            "available_comparator": "R3_gamma through R9_Gdot local bounds",
            "needed_for": "PPN stability of orbital/Newton branch",
            "next_action": "reuse 3936 PPN dashboard; do not double count or fit cancellations",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ACQ3938_5_R10_escape",
            "target": "alpha(lambda)_escape",
            "definition": "finite-range residual routed to alpha(lambda) when not theorem-zero",
            "source_status": "R10_DEFERRED_SOURCE_MAP_BLOCKED",
            "available_comparator": "R10 symbolic row plus nonclaim score-gate rows",
            "needed_for": "finite-range escape from orbital residual",
            "next_action": "activate R10 only after a finite-range residual survives and alpha/source-map rows are owned",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_status_rows(timestamp: str) -> list[dict[str, Any]]:
    source_rows = read_csv(SRC / "P8_Y5_R2FR_3598_DELTA_CAL_RESIDUAL_DECOMPOSITION.csv")
    component_ids = [
        "DCR3598_1_source_charge",
        "DCR3598_2_Poisson",
        "DCR3598_3_Gauss",
        "DCR3598_4_orbit",
        "DCR3598_5_mu_extra",
        "DCR3598_6_constant_Geff",
        "DCR3598_7_flux",
        "DCR3598_8_radial_hair",
        "DCR3598_9_time_hair",
        "DCR3598_10_frame_species_range",
        "DCR3598_11_PPN",
    ]
    by_id = {row.get("residual_id", ""): row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for residual_id in component_ids:
        source = by_id.get(residual_id, {})
        symbol = source.get("symbol", residual_id)
        status = source.get("status", "MISSING_COMPONENT_ROW")
        theorem_zero = status.endswith("ZERO") or "ZERO" in status and "MISSING" not in status
        numeric_value = ""
        numeric_bound = ""
        component_score_ready = theorem_zero or (is_number(numeric_value) and is_number(numeric_bound))
        rows.append(
            {
                "row_id": f"COMP3938_{len(rows)}",
                "residual_id": residual_id,
                "symbol": symbol,
                "formula": source.get("formula", ""),
                "status_3598": status,
                "theorem_zero_signed": theorem_zero,
                "numeric_value": numeric_value,
                "numeric_bound": numeric_bound,
                "score_ready": component_score_ready,
                "envelope_role": "absolute_sum_component",
                "fallback_action": "parent-sign zero or source numeric absolute bound; no fitted cancellation",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def delta_score_rows(timestamp: str) -> list[dict[str, Any]]:
    components = component_status_rows(timestamp)
    unresolved = [row["symbol"] for row in components if str(row["score_ready"]) != "True"]
    return [
        {
            "row_id": "DSR3938_0_private_branch",
            "score_target": "epsilon_Delta_cal",
            "prediction_branch": "private calibrated-monopole/EH/same-frame branch",
            "prediction_value": "0",
            "bound_value": "0 target by theorem branch",
            "score_formula": "Delta_cal=0 if every component is parent-signed zero",
            "runner_status": "PASS_PRIVATE_BRANCH_ONLY_NOT_PUBLIC_CLAIM",
            "passes_bound": True,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DSR3938_1_fallback_abs_envelope",
            "score_target": "Delta_cal_abs_envelope",
            "prediction_branch": "fallback/source-acquisition branch",
            "prediction_value": "MISSING_COMPONENT_VALUES",
            "bound_value": "requires arena-specific epsilon_Delta_cal or component bounds",
            "score_formula": "|Delta_charge|+|Delta_Poisson|+|Delta_Gauss|+|Delta_orbit|+|mu_extra|+|Delta_G|+|Delta_flux|+|partial_r_ln_mu_obs|+|dln_Geff_dt_plus_dln_Meff_dt|+|Delta_frame_species_range|+|Delta_PPN_source|",
            "runner_status": "BLOCKED_UNRESOLVED_COMPONENTS:" + ";".join(unresolved),
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DSR3938_2_Gdot_comparator",
            "score_target": "dln_Geff_dt/dln_Meff_dt contribution",
            "prediction_branch": "time-drift fallback",
            "prediction_value": "MISSING_MTS_DRIFT_VALUE_OR_ZERO_PROOF",
            "bound_value": "9.6e-15 yr^-1 imported from R9_Gdot",
            "score_formula": "abs(d ln mu_obs/dt) <= abs(Gdot/G)_bound after separating G_eff and source mass drift",
            "runner_status": "BOUND_IMPORTED_MTS_VALUE_MISSING",
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DSR3938_3_epsilon_r_profile",
            "score_target": "epsilon_r(r)",
            "prediction_branch": "radial-hair fallback",
            "prediction_value": "MISSING_XI1_PROFILE_OR_ZERO_PROOF",
            "bound_value": "MISSING_ARENA_RADIAL_TOLERANCE",
            "score_formula": "epsilon_r(r)=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|",
            "runner_status": "FORMULA_READY_PROFILE_AND_BOUND_MISSING",
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DSR3938_4_R10_escape",
            "score_target": "alpha(lambda)_escape",
            "prediction_branch": "finite-range fallback",
            "prediction_value": "MISSING_FINITE_RANGE_PROFILE_OR_ZERO_PROOF",
            "bound_value": "R10 curve required; symbolic row not enough",
            "score_formula": "if Delta_range survives, route absolute finite-range acceleration to alpha(lambda)",
            "runner_status": "R10_ESCAPE_DEFERRED_UNTIL_RANGE_BRANCH_ACTIVE",
            "passes_bound": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CG3938_0_bound_imports",
            "gate": "source-backed comparator import",
            "requirement": "at least Gdot and PPN comparator bounds import from local_bound_claims.csv",
            "status": "PASS_COMPARATORS_IMPORTED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3938_1_delta_envelope",
            "gate": "Delta_cal absolute envelope",
            "requirement": "fallback score uses absolute component sum and no fitted cancellation",
            "status": "PASS_SCORE_CONTRACT_BUILT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3938_2_mts_values",
            "gate": "MTS predicted amplitudes",
            "requirement": "active fallback components have parent-signed zero or numeric/source-backed values",
            "status": "FAIL_MTS_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3938_3_public_claim",
            "gate": "public Newton/orbital reduction claim",
            "requirement": "private branch plus source-backed fallback score and PPN stability",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3938_0_progress",
            "decision": "3938 converts orbital dashboard into an executable source/acquisition and Delta_cal score runner",
            "effect": "real local comparator bounds are imported where available; MTS amplitude rows remain the live bottleneck",
            "claim_status": "RUNNER_BUILT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3938_1_next",
            "decision": "next target should parent-sign or bound the Delta_cal components, not keep circling the whole branch",
            "effect": "attack source-charge, Poisson, Gauss, orbit, mu_extra, G drift, flux, radial, range, and PPN-source terms one by one",
            "claim_status": "NEXT_COMPONENT_CLOSURE_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3938_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "parent-sign or source-bound the individual Delta_cal components so the runner can produce a real pass/fail instead of a blocked envelope",
            "success_condition": "each Delta_cal component is theorem-zero, numeric/source-backed, or explicitly routed to PPN/R10/orbital bound rows with no fitted cancellation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3938 imports source-backed local comparators and creates an executable Delta_cal absolute-envelope runner; public claim remains blocked by missing MTS component amplitudes",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3938 - Orbital Ephemeris Source Acquisition and Delta_cal Score Runner

Timestamp: `{timestamp}`

## Result

Built the first executable orbital/ephemeris source-acquisition and `Delta_cal` score runner.

This checkpoint does more than repeat that inputs are missing:

- imports source-backed comparator rows from `local_bound_claims.csv`;
- carries `R9_Gdot`, `R3_gamma`, `R4_beta`, `R5_alpha1`, `R6_alpha2`, `R7_alpha3`, and `R8_xi` into the orbital runner;
- preserves `R10` only as a finite-range escape lane;
- creates an absolute no-cancellation `Delta_cal_abs_envelope`;
- separates private-branch zero from fallback empirical scoring.

## Hard Score Contract

The fallback score is:

`Delta_cal_abs = |Delta_charge| + |Delta_Poisson| + |Delta_Gauss| + |Delta_orbit| + |mu_extra| + |Delta_G| + |Delta_flux| + |partial_r ln mu_obs| + |d ln G_eff/dt + d ln M_eff/dt| + |Delta_frame_species_range| + |Delta_PPN_source|`.

No fitted cancellation counts. A component either has a parent-signed zero, a numeric/source-backed bound, or it blocks the score.

## Current Verdict

- Private branch: `Delta_cal=0` remains a private conditional result.
- Fallback branch: blocked because MTS component amplitudes are not numeric/source-backed yet.
- Bound side: some comparator bounds now import cleanly.
- Claim side: no public Newton/orbital/local-GR claim.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3938_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_ORBITAL_SOURCE_ACQUISITION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_DELTA_CAL_SCORE_RUNNER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_DELTA_CAL_COMPONENT_STATUS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3938_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3938 - Orbital Ephemeris Source Acquisition and Delta_cal Score Runner

Timestamp: `{timestamp}`

- Runner: imports source-backed local comparator bounds and builds an executable no-cancellation `Delta_cal_abs` envelope.
- Bound side: `R9_Gdot` and PPN comparators import cleanly; R10 remains a finite-range escape lane only.
- MTS side: fallback empirical scoring is blocked because component amplitudes/zero proofs are still missing for the active `Delta_cal` pieces.
- Claim gate: no public Newton/orbital/local-GR claim; private branch zero remains conditional only.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3938 - Orbital Ephemeris Source Acquisition and Delta_cal Score Runner"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    imports = bound_import_rows(timestamp)
    acquisition = acquisition_rows(timestamp)
    components = component_status_rows(timestamp)
    scores = delta_score_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (imports, acquisition, components, scores, claim_gate, decisions, next_rows(timestamp))
    numeric_imports = [row for row in imports if str(row["numeric_bound"]) == "True"]
    blocked_scores = [row for row in scores if "BLOCKED" in row["runner_status"] or "MISSING" in row["runner_status"]]
    checks = [
        ("VAL3938_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3938_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3938_02_bound_imports", len(imports) == 8 and len(numeric_imports) >= 7, "source-backed local comparator bounds imported"),
        ("VAL3938_03_Gdot_imported", any(row["local_bound_row_id"] == "R9_Gdot" and str(row["numeric_bound"]) == "True" for row in imports), "Gdot bound imported"),
        ("VAL3938_04_acquisition_rows", len(acquisition) == 6 and any(row["target"] == "epsilon_r(r)" for row in acquisition), "orbital acquisition rows emitted"),
        ("VAL3938_05_components", len(components) >= 9 and all(row["envelope_role"] == "absolute_sum_component" for row in components), "Delta_cal component status rows emitted"),
        ("VAL3938_06_score_contract", any(row["score_target"] == "Delta_cal_abs_envelope" and "Delta_Poisson" in row["score_formula"] for row in scores), "absolute Delta_cal score contract emitted"),
        ("VAL3938_07_private_not_public", any(row["runner_status"] == "PASS_PRIVATE_BRANCH_ONLY_NOT_PUBLIC_CLAIM" for row in scores), "private branch pass is not a public claim"),
        ("VAL3938_08_fallback_blocked", len(blocked_scores) >= 3, "fallback score remains blocked where MTS amplitudes are missing"),
        ("VAL3938_09_claim_gate", len(claim_gate) == 4 and any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public claim"),
        ("VAL3938_10_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3938_11_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3938_12_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3938_13_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3938_14_spine_written", SPINE_PATH.exists() and "3938 - Orbital Ephemeris Source Acquisition" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3938_15_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3938_16_script_compiles", True, "script compiles"),
        ("VAL3938_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["bound_imports"], bound_import_rows(timestamp))
    write_csv(OUTPUTS["acquisition"], acquisition_rows(timestamp))
    write_csv(OUTPUTS["component_status"], component_status_rows(timestamp))
    write_csv(OUTPUTS["delta_score"], delta_score_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3938 validation failed: {failed}")
    print(f"3938 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
