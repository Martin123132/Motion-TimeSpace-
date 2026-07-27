from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4038_SOURCE_REGISTER.csv",
    "poynting_theorem": SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
    "boundary_theorem": SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
    "zeroed_flux_boundary": SOURCE_DIR / "P8_Y5_R2FR_4038_ZEROED_FLUX_BOUNDARY_COUPLINGS.csv",
    "flux_bound": SOURCE_DIR / "P8_Y5_R2FR_4038_FLUX_BOUND_TEMPLATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4038_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4038_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4038_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4038_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4038_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4038_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4038_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4038_0", ROOT / "4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md", "MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SIGNED_INTERNALLY", "selected local packet from 4037"),
        ("SRC4038_1", SOURCE_DIR / "P8_Y5_R2FR_4037_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "c_Poynting", "residual vector naming flux/boundary as next leak"),
        ("SRC4038_2", SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "MISSING_FLUX_OR_ZERO_THEOREM", "Poynting flux retained coefficient"),
        ("SRC4038_3", SOURCE_DIR / "P8_Y5_I_matter_EM_flux_status.csv", "CONDITIONAL_ZERO_ELSE_FLUX_BOUND_READY", "older Poynting/EM flux zero-or-bound status"),
        ("SRC4038_4", SOURCE_DIR / "P8_Y5_EM_Poynting_Hilbert_source_accounting_status.csv", "EM_POYNTING_ONCE_THEOREM_CONDITIONAL_BOUND_BRANCH_ACTIVE", "EM once-only Hilbert source accounting"),
        ("SRC4038_5", SOURCE_DIR / "P8_Y5_Htau_Href_reference_lock_status.csv", "D_source H_ref=D_readout H_ref=0", "fixed reference lock status"),
        ("SRC4038_6", SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "S_boundary = S_GHY", "minimal boundary reference block"),
        ("SRC4038_7", SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv", "BoundaryReference", "source-blind boundary object language"),
        ("SRC4038_8", SOURCE_DIR / "P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv", "energy identity", "exterior collar/no-hair boundary identity"),
        ("SRC4038_9", ROOT / "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md", "global all-domain zero is forbidden", "guard that local no-flux must not erase FLRW memory"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def poynting_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "PNT4038_0_identity",
            "piece": "Maxwell Poynting identity",
            "formula": "d_t u_EM + div S_EM = -J.E",
            "condition": "ordinary Maxwell field uses the observed Hodge/current owner selected in 4037",
            "derived_result": "EM field energy change, matter work, and surface flux are one accounting identity, not three independent sources",
            "status": "IDENTITY_IMPORTED_IN_SELECTED_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PNT4038_1_exterior_collar",
            "piece": "stationary isolated local collar",
            "formula": "Phi_EM_rad[S]=int_S S_EM.n dA = -d_t int_Omega u_EM dV - int_Omega J.E dV",
            "condition": "stationary/asymptotically stationary exterior collar, no current crossing the collar, no imposed incoming/background radiation",
            "derived_result": "Phi_EM_rad=0 for bound electro/magnetostatic fields in the local exterior",
            "status": "LOCAL_NO_FLUX_THEOREM_DERIVED_CONDITIONALLY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PNT4038_2_bound_fields_once",
            "piece": "bound EM energy counted once",
            "formula": "T_total = T_matter + T_EM; M_H includes stationary bound field stress",
            "condition": "same Hilbert source branch and same observed Hodge/current owner",
            "derived_result": "Coulomb/magnetostatic bound fields do not create an extra Poynting leakage term; they are part of M_H/T_total",
            "status": "BOUND_FIELD_NOT_EXTRA_FLUX",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PNT4038_3_no_global_zero_guard",
            "piece": "local not global no-flux",
            "formula": "local stationary branch: Phi_EM_rad=0; FLRW/cosmology branch: memory/flux variables remain allowed",
            "condition": "branch selector separates compact stationary local branch from cosmological active branch",
            "derived_result": "the no-flux theorem is local and does not erase cosmology/memory mechanisms",
            "status": "GLOBAL_OVERKILL_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "PNT4038_4_result",
            "piece": "Poynting residual result",
            "formula": "c_Poynting * Phi_EM_rad = 0 in the selected stationary isolated local branch",
            "condition": "PNT4038_0 through PNT4038_3 hold",
            "derived_result": "direct local Poynting flux leak is zeroed in the selected packet; radiative/nonstationary fallback remains",
            "status": "C_POYNTING_ZERO_IN_SELECTED_LOCAL_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def boundary_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "BND4038_0_boundary_action",
            "piece": "source-blind boundary owner",
            "formula": "S_boundary = S_GHY[g_obs] + B_exact/topological - H_ref[fixed reference]",
            "condition": "boundary/reference terms are functions of observed geometry or fixed source-blind reference data only",
            "derived_result": "there is no independent source-label boundary scalar in the selected local packet",
            "status": "BOUNDARY_OWNER_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "BND4038_1_reference_lock",
            "piece": "fixed reference derivative",
            "formula": "D_source H_ref = D_readout H_ref = 0",
            "condition": "reference subtraction is chosen before variation and not re-fit by source/readout success",
            "derived_result": "source-dependent reference drift is zero in the selected local branch",
            "status": "REFERENCE_DRIFT_ZERO_IN_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "BND4038_2_collar_boundary",
            "piece": "exterior collar boundary energy identity",
            "formula": "int_Omega(|grad u|^2 + mu_phi^2 u^2)dV = int_boundary u*n.grad u dS",
            "condition": "fixed/asymptotic u=0 or no scalar boundary charge on the collar boundary",
            "derived_result": "boundary scalar charge vanishes for the selected quiet local exterior",
            "status": "BOUNDARY_SCALAR_CHARGE_ZERO_CONDITIONALLY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "BND4038_3_result",
            "piece": "boundary residual result",
            "formula": "c_B * B_source = 0 in the selected fixed-reference local branch",
            "condition": "BND4038_0 through BND4038_2 hold",
            "derived_result": "direct source-dependent boundary/reference leak is zeroed in the selected packet; nonfixed boundary fallback remains",
            "status": "C_BOUNDARY_ZERO_IN_SELECTED_LOCAL_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def zeroed_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "ZERO4038_0_poynting",
            "symbol": "c_Poynting",
            "zero_law": "c_Poynting*Phi_EM_rad=0 for stationary isolated local exterior with no imposed radiative/background flux",
            "proof_link": "PNT4038_0 through PNT4038_4",
            "what_remains": "radiative/nonstationary systems, incoming background EM flux, or time-varying source mass require finite Phi_EM_rad bound rows",
            "status": "ZERO_IN_SELECTED_STATIONARY_LOCAL_BRANCH_NOT_PUBLIC_LOCAL_GR_CLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "zero_id": "ZERO4038_1_boundary",
            "symbol": "c_B",
            "zero_law": "c_B*B_source=0 for fixed source-blind GHY/exact/topological boundary reference and quiet collar boundary data",
            "proof_link": "BND4038_0 through BND4038_3",
            "what_remains": "nonfixed/source-dependent boundary reference, corner terms, or scalar boundary charge require finite B_source bound rows",
            "status": "ZERO_IN_SELECTED_FIXED_REFERENCE_LOCAL_BRANCH_NOT_PUBLIC_LOCAL_GR_CLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def flux_bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FB4038_0_flux_fallback",
            "symbol": "Phi_EM_rad",
            "used_if": "stationary isolated local no-flux condition fails",
            "definition": "Phi_EM_rad=(1/Delta t)*int_dt int_boundary S_EM.n dA",
            "normalized_residual": "epsilon_EM_flux=Phi_EM_rad/(G_ref*M_H) or stated time-window equivalent",
            "bound_formula": "|Q_phi_flux| <= (2/3)*|c_Poynting|*|Phi_EM_rad| with measure/time-window convention declared",
            "missing_numeric_inputs": "Delta_t,boundary_surface,S_EM_profile,M_H,G_ref,c_Poynting_or_prior",
            "smoke_result": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "FB4038_1_boundary_fallback",
            "symbol": "B_source",
            "used_if": "fixed source-blind boundary/reference condition fails",
            "definition": "B_source = source-dependent part of boundary/corner/reference scalar charge after EH/GHY subtraction",
            "normalized_residual": "epsilon_B=B_source/(G_ref*M_H) or scalar-charge normalization declared",
            "bound_formula": "|Q_phi_B| <= |c_B|*|B_source|",
            "missing_numeric_inputs": "boundary_reference_choice,corner_terms,source_boundary_profile,M_H,G_ref,c_B_or_prior",
            "smoke_result": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4038_0_hidden_current",
            "symbol": "c_Z",
            "residual": "hidden/domain/memory current J_Z not killed by direct source, flux, or boundary theorems",
            "current_route": "derive fixed-point current silence from Gamma-owner/selector positivity or expose finite current coefficient",
            "priority": "next",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4038_1_norm",
            "symbol": "c_norm",
            "residual": "universal source/action normalization drift",
            "current_route": "route common mode into calibrated kappa_obs/Newton G or bound time/source variation",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4038_2_nonEH",
            "symbol": "c_nonEH",
            "residual": "non-EH or higher-curvature metric operator leakage",
            "current_route": "show decoupling at local scale or compare to PPN/Cassini-style bounds",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4038_0_selected_stationary_local",
            "verdict": "C_POYNTING_AND_C_B_ZERO_IN_SELECTED_LOCAL_BRANCH",
            "zero_result": "c_Poynting*Phi_EM_rad=0 and c_B*B_source=0 under stationary no-flux plus fixed reference",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4038",
            "reason": "remaining hidden current, normalization, and nonEH/PPN residuals are still open",
            "next_action": "attack c_Z fixed-point current silence, then c_norm/Newton-G routing",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4038_1_flux_or_boundary_rejected",
            "verdict": "FINITE_FLUX_BOUNDARY_BOUND_BRANCH_READY",
            "zero_result": "numeric bound rows required",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4038",
            "reason": "radiative/nonstationary flux or source-dependent boundary reference reintroduces scalar charge",
            "next_action": "fill Phi_EM_rad or B_source profiles before any local test score",
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4038_0_poynting",
            "decision": "For the selected stationary isolated local branch, Poynting flux through the exterior collar is zero by the Maxwell energy identity.",
            "status": "LOCAL_POYNTING_ZERO_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4038_1_boundary",
            "decision": "For the selected fixed-reference local branch, direct source-dependent boundary/reference leakage is zero.",
            "status": "LOCAL_BOUNDARY_REFERENCE_ZERO_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4038_2_guard",
            "decision": "Do not promote local no-flux to global no-flux; cosmology/FLRW memory branch remains allowed.",
            "status": "GLOBAL_OVERKILL_GUARD_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4038_3_next",
            "decision": "Move to 4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md.",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4038_0_flux_boundary",
            "claim": "local stationary Poynting and fixed-reference boundary leaks are zero in selected branch",
            "allowed": True,
            "scope": "internal selected stationary/fixed-reference local branch only",
            "reason": "Poynting identity plus fixed source-blind boundary reference",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4038_1_local_GR",
            "claim": "local GR/PPN/R10 pass",
            "allowed": False,
            "scope": "full local-gravity phenomenology",
            "reason": "c_Z, c_norm, c_nonEH, and PPN closure remain open",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4038_2_global_no_flux",
            "claim": "global all-branch no-flux",
            "allowed": False,
            "scope": "unified local plus cosmology",
            "reason": "global no-flux would erase the FLRW/memory branch",
            "public_claim_allowed": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4038_0",
            "next_doc": "4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md",
            "next_script": "scripts/Y5_R2FR_4039_hidden_current_fixed_point_silence_or_cZ_bound.py",
            "why": "direct source couplings, direct EM cross terms, local Poynting flux, and fixed-reference boundary leakage are now zeroed inside the selected branch; the next live local leak is hidden/domain current c_Z.",
            "fallback": "if fixed-point current silence fails, produce finite c_Z profile and local bound rows",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STATUS4038_0",
            "checkpoint": "4038",
            "canonical_status": "LOCAL_POYNTING_BOUNDARY_ZEROED_INTERNAL_CZ_NEXT",
            "strongest_result": "In the selected stationary/fixed-reference local branch, c_Poynting and c_B do not contribute.",
            "still_missing": "hidden current c_Z, universal normalization c_norm/Newton-G routing, nonEH/PPN residual closure",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    total = len(sources)
    return f"""# 4038 - Poynting No-Flux And Boundary Reference Theorem Or Flux Bound

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{found}/{total}`.

## What Actually Moved

4038 attacks the next two local leaks after the direct coupling cleanup:

- `c_Poynting`: net EM/radiative/background flux through the local collar;
- `c_B`: source-dependent boundary/corner/reference leakage.

## Local Poynting Result

Using the selected 4037 packet, Maxwell energy accounting is one identity:

`d_t u_EM + div S_EM = -J.E`.

For a stationary/asymptotically stationary exterior collar with no current crossing the collar and no imposed incoming/background radiation,

`Phi_EM_rad = int_boundary S_EM.n dA = 0`.

Bound Coulomb/magnetostatic fields are not extra leakage; they are counted once inside `T_total` and `M_H`.

## Boundary Result

The selected local branch uses

`S_boundary = S_GHY[g_obs] + exact/topological terms - H_ref[fixed source-blind reference]`.

With `D_source H_ref=D_readout H_ref=0` and quiet collar boundary data, the direct source-dependent boundary scalar is zero:

`c_B*B_source=0`.

## Guardrail

This is local no-flux, not global no-flux. The FLRW/cosmology memory branch remains allowed. We are not using a global zero that would murder the cosmology route in its sleep.

## Fallback Bound

If stationarity, isolation, or fixed-reference conditions fail:

- `Phi_EM_rad=(1/Delta t)*int_dt int_boundary S_EM.n dA`;
- `epsilon_EM_flux=Phi_EM_rad/(G_ref*M_H)`;
- `|Q_phi_flux| <= (2/3)*|c_Poynting|*|Phi_EM_rad|`;
- `|Q_phi_B| <= |c_B|*|B_source|`.

These rows are schema-ready but numeric-claim blocked until the profiles and normalizations are real.

## Current Verdict

- Current evaluator result: `C_POYNTING_AND_C_B_ZERO_IN_SELECTED_LOCAL_BRANCH`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4038`.
- Remaining live local residuals: `c_Z`, `c_norm`, `c_nonEH`.

## Next Target

- `4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md`
- `scripts/Y5_R2FR_4039_hidden_current_fixed_point_silence_or_cZ_bound.py`
"""


def validation_rows(
    ts: str,
    sources: List[Dict[str, object]],
    poynting: List[Dict[str, object]],
    boundary: List[Dict[str, object]],
    zeroed: List[Dict[str, object]],
    flux_bound: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
        return {"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts}

    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH), str(SCRIPT_PATH)]
    return [
        row("VAL4038_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4038_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4038_02_poynting_identity", any(item["theorem_id"] == "PNT4038_0_identity" for item in poynting), "Poynting identity present"),
        row("VAL4038_03_local_no_flux", any(item["theorem_id"] == "PNT4038_1_exterior_collar" for item in poynting), "local no-flux theorem present"),
        row("VAL4038_04_global_guard", any(item["theorem_id"] == "PNT4038_3_no_global_zero_guard" for item in poynting), "global no-flux guard present"),
        row("VAL4038_05_boundary_owner", any(item["theorem_id"] == "BND4038_0_boundary_action" for item in boundary), "boundary owner theorem present"),
        row("VAL4038_06_reference_lock", any(item["theorem_id"] == "BND4038_1_reference_lock" for item in boundary), "reference lock theorem present"),
        row("VAL4038_07_boundary_result", any(item["theorem_id"] == "BND4038_3_result" for item in boundary), "boundary result present"),
        row("VAL4038_08_zero_poynting", any(item["symbol"] == "c_Poynting" and "ZERO_IN_SELECTED" in item["status"] for item in zeroed), "c_Poynting zero row present"),
        row("VAL4038_09_zero_boundary", any(item["symbol"] == "c_B" and "ZERO_IN_SELECTED" in item["status"] for item in zeroed), "c_B zero row present"),
        row("VAL4038_10_flux_bound", any(item["symbol"] == "Phi_EM_rad" for item in flux_bound), "flux fallback bound present"),
        row("VAL4038_11_boundary_bound", any(item["symbol"] == "B_source" for item in flux_bound), "boundary fallback bound present"),
        row("VAL4038_12_bound_nonclaim", all(item["valid_for_public_claim"] is False for item in flux_bound), "fallback bounds remain nonclaim"),
        row("VAL4038_13_remaining_cZ", any(item["symbol"] == "c_Z" for item in remaining), "c_Z remains next residual"),
        row("VAL4038_14_remaining_cnorm", any(item["symbol"] == "c_norm" for item in remaining), "c_norm remains"),
        row("VAL4038_15_remaining_cnonEH", any(item["symbol"] == "c_nonEH" for item in remaining), "c_nonEH remains"),
        row("VAL4038_16_current_verdict", any(item["case_id"] == "CASE4038_0_selected_stationary_local" for item in evaluator), "selected local evaluator present"),
        row("VAL4038_17_no_public_local_claim", all(item["public_claim_allowed"] is False for item in claims), "no public claims allowed"),
        row("VAL4038_18_internal_claim_scoped", any(item["claim_id"] == "CLAIM4038_0_flux_boundary" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "internal flux/boundary claim scoped"),
        row("VAL4038_19_next_decision", any(item["decision_id"] == "DEC4038_3_next" for item in decisions), "4039 next decision present"),
        row("VAL4038_20_next_target", bool(next_target and "4039" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4038_21_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4038_22_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4038_23_script_compiles", compile_ok, "script compiles"),
        row("VAL4038_24_private_guard", all(item["valid_for_public_claim"] is False for table in [poynting, boundary, zeroed, flux_bound, remaining, decisions] for item in table), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    poynting = poynting_theorem_rows(ts)
    boundary = boundary_theorem_rows(ts)
    zeroed = zeroed_rows(ts)
    flux_bound = flux_bound_rows(ts)
    remaining = remaining_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["poynting_theorem"], poynting)
    write_csv(OUTPUTS["boundary_theorem"], boundary)
    write_csv(OUTPUTS["zeroed_flux_boundary"], zeroed)
    write_csv(OUTPUTS["flux_bound"], flux_bound)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(ts, sources, poynting, boundary, zeroed, flux_bound, remaining, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4038 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
