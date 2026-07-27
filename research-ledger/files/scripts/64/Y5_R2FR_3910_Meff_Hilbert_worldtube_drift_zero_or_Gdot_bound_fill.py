from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3910"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3910-Y5-R2FR-Meff-Hilbert-worldtube-drift-zero-or-Gdot-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3910_SOURCE_REGISTER.csv",
    "meff_stack": SRC / "P8_Y5_R2FR_3910_MEFF_ZERO_THEOREM_STACK.csv",
    "obstructions": SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv",
    "gdot_runner": SRC / "P8_Y5_R2FR_3910_GDOT_MEFF_COMPONENT_RUNNER.csv",
    "decision": SRC / "P8_Y5_R2FR_3910_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3910_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3910_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3910_VALIDATION.csv",
}

MEFF_DEF = "M_eff[S] := (4*pi*G_*)^-1 int_S Pi_M^H J_H"
MEFF_DRIFT = "d_t ln M_eff = d_t ln int_S Pi_M^H J_H - d_t ln G_* + boundary_motion[S]"
STATIONARY_ZERO = "if d(Pi_M^H J_H)=0 in the source-free annulus, side flux=0, Pi_M/tau/reference/frame are fixed, and d_t ln G_*=0, then d_t ln M_eff=0"
HILBERT_LEAK_IDENTITY = "nabla_mu J_M^mu=(nabla_mu ell_J)T^{mu nu}tau_nu + ell_J(nabla_mu T^{mu nu})tau_nu + ell_J T^{mu nu}nabla_mu tau_nu"
MEFF_BOUND = "|d_t ln M_eff| <= |R_PiM| + |R_Htau| + |R_Ward| + |R_ref| + |R_W| + |R_frame| + |R_units| + |R_side_flux|"
TOTAL_GDOT_AFTER = "Gdot_total <= 0 + B_Meff + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3910_00_next", SRC / "P8_Y5_R2FR_3909_NEXT_TARGET.csv", "NEXT3909_0", "3909 selected M_eff drift target"),
        ("SRC3910_01_meff_open", SRC / "P8_Y5_R2FR_3909_GDOT_COMPONENT_CLOSURE_MATRIX.csv", "GDC3909_1_Meff", "3909 marks d_t ln M_eff as the next open Gdot component"),
        ("SRC3910_02_gdot_partial", SRC / "P8_Y5_R2FR_3909_GDOT_FALLBACK_COMPONENT_RUNNER.csv", "GDF3909_1_partial_zero", "3909 total Gdot after Gstar zero-form"),
        ("SRC3910_03_hilbert_flux", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM2_mass_flux_closure", "Hilbert projected mass-flux closure contract"),
        ("SRC3910_04_newton_stack", SRC / "P8_source_normalized_Newton_branch_STACK.csv", "SN4_closed_Meff_flux", "source-normalized Newton branch mass flux closure row"),
        ("SRC3910_05_worldtube_transfer", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "MTS transfer condition for EH worldtube source measure"),
        ("SRC3910_06_hilbert_identity", SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv", "THM2568_2_exact_divergence_identity", "exact Hilbert source-current divergence identity"),
        ("SRC3910_07_stationary_branch", SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv", "THM2568_3_stationary_surface_independence", "stationary compact-source surface-independence theorem"),
        ("SRC3910_08_ellj_total", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_0_total", "ell_J/source-current residual decomposition"),
        ("SRC3910_09_pim_obstruction", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_3_R_PiM", "Pi_M source-current commutator obstruction"),
        ("SRC3910_10_htau_obstruction", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_4_R_Htau", "H_tau integrability/source-charge curl obstruction"),
        ("SRC3910_11_hlock_pim", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_5_commutator_stress", "Hamiltonian Pi_M commutator stress row"),
        ("SRC3910_12_hlock_mhref", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_3_MHref", "Hamiltonian M_H_ref denominator guardrail"),
        ("SRC3910_13_htau_gate", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_7_verdict", "H_tau integrability curl gate verdict"),
        ("SRC3910_14_comm_total", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total", "combined Pi_M/H_tau residual law"),
        ("SRC3910_15_comm_curl", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_3_C_curl", "H_tau curl component inside combined law"),
        ("SRC3910_16_worldtube_audit", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_1_same_charge", "worldtube source charge equality audit"),
        ("SRC3910_17_reference_lock", SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_0_MHref_definition", "M_H_ref reference lock contract"),
        ("SRC3910_18_anti_launder", SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_4_no_laundering", "anti-circularity guardrail for measured GM"),
        ("SRC3910_19_validation", SRC / "P8_Y5_BRR545_3909_VALIDATION.csv", "VAL3909_12_next_target", "3909 validation handoff"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        line_number = ""
        line_excerpt = ""
        found = False
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    line_excerpt = line[:500]
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
                "line_excerpt": line_excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def meff_stack_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MZ3910_0_definition",
            "object": "M_eff",
            "statement": MEFF_DEF,
            "derivation_status": "DEFINITION_FROM_HILBERT_SURFACE_CHARGE",
            "requires": "same G_*, same observed source frame, stable Pi_M^H, stable H_tau reference denominator",
            "source_path": str(SRC / "P8_Y5_R2FR_3909_GDOT_COMPONENT_CLOSURE_MATRIX.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MZ3910_1_exact_drift_identity",
            "object": "d_t ln M_eff",
            "statement": MEFF_DRIFT,
            "derivation_status": "EXACT_ACCOUNTING_IDENTITY",
            "requires": "moving-surface and reference terms retained; no cancellation credit",
            "source_path": str(SRC / "P8_Y5_R2FR_3909_GDOT_FALLBACK_COMPONENT_RUNNER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MZ3910_2_stationary_zero_lemma",
            "object": "M_eff stationary branch",
            "statement": STATIONARY_ZERO,
            "derivation_status": "CONDITIONAL_ZERO_LEMMA_DERIVED",
            "requires": "closed Pi_M J_H flux; compact support; fixed tau/frame/reference; no source-shadow or side flux; G_* zero-form branch adopted",
            "source_path": str(SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MZ3910_3_hilbert_leak_identity",
            "object": "J_M",
            "statement": HILBERT_LEAK_IDENTITY,
            "derivation_status": "EXACT_SOURCE_LEAK_IDENTITY_IMPORTED",
            "requires": "ell_J fixed, matter on shell, tau Killing/stationary to make the right-hand side vanish",
            "source_path": str(SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MZ3910_4_no_full_dynamic_zero",
            "object": "unconditional d_t ln M_eff",
            "statement": "dynamic MTS source branches keep nonzero leak terms unless parent exchange currents or Pi_M/H_tau commutation identities are signed",
            "derivation_status": "FULL_ZERO_NOT_PROMOTED",
            "requires": "parent-owned exchange current or numeric bounds for every obstruction row",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def obstruction_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "OBS3910_0_total_bound",
            "component": "B_Meff",
            "meaning": "absolute no-cancellation envelope for measured source-mass drift",
            "formula": MEFF_BOUND,
            "zero_condition": "all component residuals vanish by parent identities or each has a source-backed numeric bound",
            "status": "EXACT_ENVELOPE_NONCLAIM",
            "next_action": "attack R_PiM + R_Htau first",
            "source_path": str(SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_1_R_PiM",
            "component": "R_PiM",
            "meaning": "Pi_M/source-current commutator obstruction",
            "formula": "R_PiM := ([D_X,Pi_M^H]J_H + Pi_M^H[D_X,J_H] - D_X Pi_M^H[J_H]) / Pi_M^H[J_H]",
            "zero_condition": "Pi_M fixed-variable list, source support, Hodge/domain data and reference are parent-owned before readout",
            "status": "OPEN_ALGEBRAIC_HEART",
            "next_action": "derive commutator zero from source-domain connection or carry numeric projector-stress rows",
            "source_path": str(SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_2_R_Htau",
            "component": "R_Htau",
            "meaning": "H_tau nonintegrability/source-charge curl",
            "formula": "R_Htau := normalized curl(delta H_tau) = normalized integral_S i_tau omega_total plus exact/boundary terms",
            "zero_condition": "parent theta/omega owner, tau/surface lock, exact boundary symplectic flux and reference split",
            "status": "OPEN_ALGEBRAIC_HEART",
            "next_action": "derive H_tau curl exactness or bound curl/source-boundary flux",
            "source_path": str(SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_3_R_Ward",
            "component": "R_Ward",
            "meaning": "matter Ward/source exchange failure",
            "formula": "R_Ward := normalized ell_J (nabla_mu T^{mu nu}) tau_nu plus allowed exchange-current remainder",
            "zero_condition": "matter equations hold in the same frame and exchange currents are either absent or exactly included",
            "status": "OPEN_DYNAMICAL_SOURCE_TERM",
            "next_action": "connect matter descent/Ward identity to parent source action",
            "source_path": str(SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_4_R_ref",
            "component": "R_ref",
            "meaning": "reference subtraction fails to commute with Pi_M or D_X",
            "formula": "R_ref := -([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)",
            "zero_condition": "H_ref is source-blind and fixed by boundary/topology/asymptotic coframe only",
            "status": "OPEN_REFERENCE_LOCK",
            "next_action": "derive source-blind H_ref selector after Pi_M/H_tau core",
            "source_path": str(SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_5_R_W",
            "component": "R_W",
            "meaning": "worldtube/domain/support selector drift",
            "formula": "R_W := normalized D_X(W_source, Sigma, Hodge, linked surfaces)",
            "zero_condition": "W_source and linked surfaces are selected from supp J_H[tau] before readout",
            "status": "OPEN_WORLDLINE_SUPPORT_LOCK",
            "next_action": "keep source-support residual explicit until same-charge worldtube theorem closes",
            "source_path": str(SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_6_R_frame",
            "component": "R_frame",
            "meaning": "same-frame/tau/readout mismatch",
            "formula": "R_frame := D_X ln(tau, e_obs, Sigma, readout frame mismatch)",
            "zero_condition": "same observed frame/tau/source support is used in H_tau, Pi_M and readout",
            "status": "OPEN_PARALLEL_FRAME_FACTOR",
            "next_action": "carry into Rframe product gate unless exact frame lock is derived",
            "source_path": str(SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_7_R_units",
            "component": "R_units",
            "meaning": "normalization denominator/source unit leakage",
            "formula": "R_units := D_X ln(Pi_M H_tau denominator units)",
            "zero_condition": "M_H_ref denominator is parent-owned and not defined from measured GM",
            "status": "OPEN_DENOMINATOR_LOCK",
            "next_action": "do not use orbital GM to define the denominator",
            "source_path": str(SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OBS3910_8_R_side_flux",
            "component": "R_side_flux",
            "meaning": "side/boundary flux through moving worldtube or surface collar",
            "formula": "R_side_flux := |int_side Pi_M J_H| / |int_S Pi_M J_H| per unit time",
            "zero_condition": "compact stationary support and fixed linking surfaces make side flux vanish",
            "status": "CLOSED_ONLY_ON_STATIONARY_COLLAR",
            "next_action": "numeric source profile needed for dynamic branch",
            "source_path": str(SRC / "P8_source_normalized_Newton_branch_STACK.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gdot_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GDM3910_0_Gstar_component",
            "branch": "zero-form Gstar branch from 3909",
            "formula": "d_t ln G_* = 0",
            "status": "CONDITIONAL_COMPONENT_ZERO_RETAINED",
            "acceptance": "requires parent adoption of S_G0 zero-form sector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDM3910_1_Meff_component",
            "branch": "Hilbert worldtube measured source mass",
            "formula": MEFF_BOUND,
            "status": "BOUND_FORMULA_FILLED_NUMERIC_ROWS_MISSING",
            "acceptance": "each component must be theorem-zero or source-backed numeric; no cancellation credit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDM3910_2_total_Gdot_after_Meff",
            "branch": "measured Gdot gate",
            "formula": TOTAL_GDOT_AFTER,
            "status": "TOTAL_GDOT_STILL_BLOCKED",
            "acceptance": "B_Meff plus epsilon_mu, Z_Poisson and Z_frame must sum below 9.6e-15 yr^-1",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDM3910_3_stationary_collar",
            "branch": "stationary compact source collar",
            "formula": "B_Meff=0 if MZ3910_2 premises all hold",
            "status": "CONDITIONAL_LOCAL_SOURCE_THEOREM",
            "acceptance": "usable as a derived branch only after Pi_M/H_tau/source support clauses are parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDM3910_4_dynamic_branch",
            "branch": "dynamic or residual-bearing source branch",
            "formula": "B_Meff>0 unless R_PiM, R_Htau, R_Ward, R_ref, R_W, R_frame, R_units, R_side_flux are all closed/bounded",
            "status": "OPEN_NUMERIC_OR_THEOREM_PATH",
            "acceptance": "first attack OBS3910_1 and OBS3910_2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3910_0_stationary_result",
            "decision": "stationary compact Hilbert branch gives a real conditional zero theorem for d_t ln M_eff",
            "claim_status": "PRIVATE_CONDITIONAL_DERIVATION_ONLY",
            "reason": "the zero follows from closed projected source flux plus fixed Pi_M/tau/reference/frame and the 3909 Gstar zero-form",
            "next_action": "do not publish as local-GR pass until parent adoption closes the premises",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3910_1_dynamic_result",
            "decision": "unconditional or dynamic d_t ln M_eff zero is not proved",
            "claim_status": "NO_LOCAL_GR_OR_GDOT_CLAIM",
            "reason": "Pi_M/H_tau commutator, curl, reference, support and frame residuals remain live",
            "next_action": "promote MEFF_BOUND as the executable Gdot component envelope",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3910_2_selected_next",
            "decision": "next target is R_PiM + R_Htau commutator/curl zero or first numeric bound",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "these two are the algebraic heart of the source denominator and block Newton/PPN/R10/Gdot together",
            "next_action": "write 3911 Pi_M/H_tau commutator-zero attempt",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3910_0",
            "next_doc": "3911-Y5-R2FR-PiM-Htau-commutator-zero-or-first-Gdot-numeric-row.md",
            "next_script": "scripts/Y5_R2FR_3911_PiM_Htau_commutator_zero_or_first_Gdot_numeric_row.py",
            "target": "derive R_PiM + R_Htau = 0 from a parent source-domain connection and H_tau exact symplectic flux, or build the first numeric nonclaim Gdot row",
            "why_this_next": "3910 reduced d_t ln M_eff to a precise obstruction vector; Pi_M/H_tau is the common blocker for Gdot, Newton source mass, PPN and R10 denominators",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "M_eff drift reduced to stationary zero lemma plus executable no-cancellation bound",
            "local_gr_claim": False,
            "gdot_claim": False,
            "new_forward_progress": "d_t ln M_eff is no longer just 'missing'; it is split into named source-current obstructions with a next algebraic target",
            "primary_blocker": "R_PiM + R_Htau",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, Any]],
    meff_stack: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    gdot_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    timestamp: str,
) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    obstruction_lines = "\n".join(
        f"- `{row['component']}`: `{row['formula']}` — {row['status']}" for row in obstructions
    )
    doc = f"""# 3910 — Meff Hilbert Worldtube Drift Zero or Gdot Bound Fill

Timestamp: `{timestamp}`

## Result

This pass does move the branch forward: `d_t ln M_eff` is not left as a vague missing term. It is now either a stationary compact-source zero theorem or a concrete no-cancellation residual envelope.

Definition:
`{MEFF_DEF}`

Exact accounting:
`{MEFF_DRIFT}`

Stationary collar zero lemma:
`{STATIONARY_ZERO}`

Hilbert leak identity:
`{HILBERT_LEAK_IDENTITY}`

Executable bound:
`{MEFF_BOUND}`

## What Closed

- The stationary compact Hilbert branch has an honest conditional derivation for `d_t ln M_eff=0`.
- The derivation uses closed `Pi_M^H J_H` flux, fixed source support/surface/tau/reference/frame, no side flux, and the 3909 `d_t ln G_*=0` component.
- This is a real source-mass control theorem inside that collar; it is not yet a public local-GR pass because the parent has not signed every premise.

## What Did Not Close

The dynamic/full local branch still carries:

{obstruction_lines}

## Gdot Gate After 3910

`{TOTAL_GDOT_AFTER}`

So the measured-coupling route remains alive, but total `dot G/G` is not claimable until `B_Meff`, `epsilon_mu`, `Z_Poisson`, and `Z_frame` are theorem-zero or numerically bounded.

## Decision

- `d_t ln M_eff=0` is conditionally derived for the stationary compact-source collar.
- Unconditional/dynamic `d_t ln M_eff=0` is rejected for now.
- First attack next: `R_PiM + R_Htau`, because it blocks the source denominator in Gdot, Newton, PPN, and R10 at once.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['meff_stack'])}`
- `{rel(OUTPUTS['obstructions'])}`
- `{rel(OUTPUTS['gdot_runner'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`
- `{rel(OUTPUTS['status'])}`

## Next Target

`{next_rows[0]['next_doc']}`

Goal: {next_rows[0]['target']}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3910 MEFF HILBERT WORLDTUBE DRIFT -->
## 3910 Meff Hilbert Worldtube Drift

Timestamp: `{timestamp}`

Definition:
`{MEFF_DEF}`

Exact accounting:
`{MEFF_DRIFT}`

Stationary collar zero:
`{STATIONARY_ZERO}`

Dynamic branch bound:
`{MEFF_BOUND}`

Gdot after this pass:
`{TOTAL_GDOT_AFTER}`

Decision: `d_t ln M_eff=0` is conditionally derived for stationary compact Hilbert sources, but the full dynamic/local branch remains blocked by `R_PiM + R_Htau` plus reference/support/frame/unit residuals. Next target: Pi_M/H_tau commutator-curl zero or numeric nonclaim row.
<!-- END 3910 MEFF HILBERT WORLDTUBE DRIFT -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3910 MEFF HILBERT WORLDTUBE DRIFT -->"
    end = "<!-- END 3910 MEFF HILBERT WORLDTUBE DRIFT -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    meff_stack: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    gdot_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(
        (
            "VAL3910_0_sources",
            "all cited local source paths and needles resolve",
            all(row["exists"] and row["needle_found"] for row in sources),
            f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found",
        )
    )
    checks.append(
        (
            "VAL3910_1_meff_definition",
            "M_eff definition row written",
            any(MEFF_DEF in row["statement"] for row in meff_stack),
            rel(OUTPUTS["meff_stack"]),
        )
    )
    checks.append(
        (
            "VAL3910_2_stationary_zero",
            "stationary zero lemma contains closed projected flux condition",
            any("d(Pi_M^H J_H)=0" in row["statement"] for row in meff_stack),
            rel(OUTPUTS["meff_stack"]),
        )
    )
    checks.append(
        (
            "VAL3910_3_hilbert_identity",
            "Hilbert leak identity retained exactly",
            any("nabla_mu J_M^mu" in row["statement"] for row in meff_stack),
            rel(OUTPUTS["meff_stack"]),
        )
    )
    checks.append(
        (
            "VAL3910_4_obstruction_core",
            "R_PiM and R_Htau obstruction rows exist",
            {"R_PiM", "R_Htau"}.issubset({row["component"] for row in obstructions}),
            rel(OUTPUTS["obstructions"]),
        )
    )
    checks.append(
        (
            "VAL3910_5_no_cancel_bound",
            "M_eff no-cancellation bound row exists",
            any(MEFF_BOUND in row["formula"] for row in obstructions + gdot_runner),
            rel(OUTPUTS["gdot_runner"]),
        )
    )
    checks.append(
        (
            "VAL3910_6_no_claim",
            "all generated claim gates remain nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in meff_stack + obstructions + gdot_runner + decisions),
            "valid_for_claim false across theorem, obstruction, runner and decision rows",
        )
    )
    checks.append(
        (
            "VAL3910_7_next_target",
            "next target points to Pi_M/H_tau commutator-curl work",
            "3911-Y5-R2FR-PiM-Htau" in read_text(OUTPUTS["next"]),
            rel(OUTPUTS["next"]),
        )
    )
    checks.append(
        (
            "VAL3910_8_doc",
            "3910 markdown checkpoint written",
            DOC_PATH.exists() and "Meff Hilbert Worldtube Drift" in read_text(DOC_PATH),
            rel(DOC_PATH),
        )
    )
    checks.append(
        (
            "VAL3910_9_spine",
            "local coupling spine updated with 3910 block",
            SPINE_PATH.exists() and "BEGIN 3910 MEFF HILBERT WORLDTUBE DRIFT" in read_text(SPINE_PATH),
            rel(SPINE_PATH),
        )
    )
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details: list[str] = []
    for path in csv_outputs:
        try:
            rows = read_csv_rows(path)
            parse_details.append(f"{path.name}:{len(rows)}")
            csv_parse_ok = csv_parse_ok and bool(rows)
        except Exception as exc:  # pragma: no cover - validation report path
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{type(exc).__name__}:{exc}")
    checks.append(("VAL3910_10_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3910*")) if FWB.exists() else []
    checks.append(
        (
            "VAL3910_11_no_formalization_workbench_edits",
            "no 3910 files generated in formalization-workbench",
            not fwb_hits,
            "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits",
        )
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(
        (
            "VAL3910_12_no_pycache",
            "scripts __pycache__ removed",
            not pycache_hits,
            "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__",
        )
    )
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    meff_stack = meff_stack_rows(timestamp)
    obstructions = obstruction_rows(timestamp)
    gdot_runner = gdot_runner_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_rows = next_target_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["meff_stack"], meff_stack)
    write_csv(OUTPUTS["obstructions"], obstructions)
    write_csv(OUTPUTS["gdot_runner"], gdot_runner)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, meff_stack, obstructions, gdot_runner, decisions, next_rows, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, meff_stack, obstructions, gdot_runner, decisions, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
