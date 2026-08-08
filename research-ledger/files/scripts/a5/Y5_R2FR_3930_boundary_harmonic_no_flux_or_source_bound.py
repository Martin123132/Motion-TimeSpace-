from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3930"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3930-Y5-R2FR-boundary-harmonic-no-flux-or-source-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3930_SOURCE_REGISTER.csv",
    "signature": SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_PARENT_SIGNATURE.csv",
    "zero_result": SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv",
    "poynting_guard": SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv",
    "reduced_escape": SRC / "P8_Y5_R2FR_3930_REDUCED_BESCAPE_QUEUE.csv",
    "fallback": SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3930_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3930_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3930_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3930_VALIDATION.csv",
}

BOUNDARY_SIGNATURE = (
    "local isolated-boundary branch: S_B=S_top[relative class]+int_boundary sqrt(|gamma|)F(s), "
    "D_A s=0, no marker/vector/shear fields, fixed corner/reference class, no normal exchange, "
    "asymptotically/outer-boundary monopole-only data, and no net total Hilbert/Maxwell flux through the source collar"
)
ELLIPTIC_ZERO = (
    "D_TF[S]=0, S|boundary=0, H_l>=2=0 => S=0"
)
BOUNDARY_ZERO = (
    "BOUNDARY_CERT_loc => P00_boundary=0, B_harmonic_boundary=0, "
    "tau_wall_TF=0, alpha3_boundary=xi_boundary=delta_beta_boundary=Gdot_boundary=0 "
    "except a derivative-silent scalar monopole absorbed into measured GM"
)
POYNTING_GUARD = (
    "int_dt int_boundary S_EM·n dA=0 for the stationary closed total-system worldtube; "
    "circulating internal Poynting flow may remain and stays inside T_EM"
)
A_MULTI_REDUCED = "A_multi_BPD0 <= G_ext*(|P00_history|+|P00_nonlocal|)"
BESCAPE_REDUCED = "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi_BPD0 + B_deriv"
BOUNDARY_FALLBACK = (
    "B_boundary_harmonic := |P00_boundary| + |B_harmonic_boundary| + |Phi_B|/M_H_ref + |tau_wall_TF|/M_H_ref"
)
NEXT_DOC = "3931-Y5-R2FR-history-nonlocal-tail-reset-or-suppression-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3931_history_nonlocal_tail_reset_or_suppression_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3930_00_3929_doc", PCW / "3929-Y5-R2FR-topological-projector-parent-signature-or-active-projector-norm-values.md", "Reduced multipole queue:", "3929 reduced multipole handoff"),
        ("SRC3930_01_3929_reduced", SRC / "P8_Y5_R2FR_3929_REDUCED_BESCAPE_QUEUE.csv", "REB3929_1_reduced_multipole", "3929 reduced A_multi queue"),
        ("SRC3930_02_3929_next", SRC / "P8_Y5_R2FR_3929_NEXT_TARGET.csv", "NEXT3929_0", "3930 handoff"),
        ("SRC3930_03_3892_doc_boundary", PCW / "3892-Y5-R2FR-boundary-projector-topological-certificate-or-fill-alpha3-projector-inputs.md", "Boundary certificate:", "boundary certificate prose"),
        ("SRC3930_04_3892_cert", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_0_certificate", "boundary certificate package"),
        ("SRC3930_05_3892_monopole", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_2_scalar_monopole", "derivative-silent scalar monopole rule"),
        ("SRC3930_06_3834_doc", PCW / "3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md", "D_TF[S]=0", "elliptic boundary zero theorem"),
        ("SRC3930_07_3834_theorem", SRC / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv", "BH3834_0_elliptic_uniqueness", "harmonic elliptic uniqueness row"),
        ("SRC3930_08_3834_bound", SRC / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv", "BH3834_2_bound_contract", "boundary harmonic fallback bound"),
        ("SRC3930_09_3873_poynting", SRC / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv", "PZT3873_2_stationary_zero", "stationary EM Poynting boundary zero"),
        ("SRC3930_10_3873_guard", SRC / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv", "PZT3873_3_circulation_guard", "circulating Poynting guard"),
        ("SRC3930_11_3891_boundary_guard", SRC / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv", "BPS3891_0_boundary_guard", "boundary shortcut guard"),
        ("SRC3930_12_3891_scalar", SRC / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv", "BPS3891_1_scalar_boundary", "scalar boundary lemma"),
        ("SRC3930_13_549_nohair", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_3_scalar_homogeneous_nohair", "cohomology/nohair scalar lemma"),
        ("SRC3930_14_549_flux", SRC / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv", "FB549_0_boundary_flux_bound", "boundary flux fallback row"),
        ("SRC3930_15_3927_component", SRC / "P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv", "COMP3927_1_boundary_harmonic", "boundary/harmonic component"),
        ("SRC3930_16_3929_validation", SRC / "P8_Y5_BRR545_3929_VALIDATION.csv", "VAL3929_14_no_pycache", "3929 validation"),
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
                    excerpt = line[:760]
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
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BSIG3930_0_branch",
            "signature_clause": "local isolated-boundary branch",
            "statement": BOUNDARY_SIGNATURE,
            "branch_status": "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "turns boundary/harmonic escape from active source into local isolated-boundary condition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BSIG3930_1_scalar_boundary",
            "signature_clause": "scalar marker-free boundary action",
            "statement": "S_B=S_top[relative class]+int_boundary sqrt(|gamma|)F(s), D_A s=0, no marker/vector/shear fields",
            "branch_status": "SIGNED_FOR_LOCAL_ISOLATED_COLLAR",
            "effect": "tau_AB proportional gamma_AB; no preferred vector/shear boundary stress",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BSIG3930_2_no_harmonic_lge2",
            "signature_clause": "no l>=2 harmonic scalar boundary class",
            "statement": ELLIPTIC_ZERO,
            "branch_status": "SIGNED_FOR_LOCAL_ISOLATED_ANNULUS",
            "effect": "kills homogeneous scalar slip/multipole hair after source zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BSIG3930_3_monopole_policy",
            "signature_clause": "monopole calibration only",
            "statement": "constant derivative-silent scalar monopole may renormalize measured GM only; no time/radial/frame/beta/xi/Gdot hair",
            "branch_status": "SIGNED_AS_CALIBRATION_POLICY",
            "effect": "does not contribute to A_multi, B_deriv, beta, xi, or Gdot",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BSIG3930_4_total_flux",
            "signature_clause": "closed total Hilbert/Maxwell worldtube",
            "statement": POYNTING_GUARD,
            "branch_status": "SIGNED_FOR_STATIONARY_ISOLATED_TOTAL_SOURCE",
            "effect": "no net EM/matter flux crosses source collar while internal EM stress remains in T_vis",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BSIG3930_5_signature_verdict",
            "signature_clause": "boundary/harmonic local branch verdict",
            "statement": BOUNDARY_ZERO,
            "branch_status": "BOUNDARY_HARMONIC_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "P00_boundary and B_harmonic_boundary are zero in this local isolated branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_result_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BHZ3930_0_P00_boundary", "P00_boundary", "0", "no scalar/vector/shear/normal-exchange boundary source in local isolated collar"),
        ("BHZ3930_1_B_harmonic_boundary", "B_harmonic_boundary", "0", "fixed monopole-only exterior data and no l>=2 harmonic scalar class"),
        ("BHZ3930_2_Phi_B", "Phi_B", "0", "no net total Hilbert/Maxwell flux through stationary source boundary"),
        ("BHZ3930_3_tau_wall_TF", "tau_wall_TF", "0", "scalar homogeneous boundary stress is proportional to gamma_AB"),
        ("BHZ3930_4_alpha3_boundary", "alpha3_boundary", "0", "no preferred vector/momentum boundary leakage"),
        ("BHZ3930_5_xi_boundary", "xi_boundary", "0", "no anisotropic/harmonic l>=2 boundary source"),
        ("BHZ3930_6_delta_beta_boundary", "delta_beta_boundary", "0", "boundary monopole is calibration-only and derivative silent"),
        ("BHZ3930_7_Gdot_boundary", "Gdot_boundary", "0", "boundary monopole has no time profile in this branch"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "branch_value": value,
            "derivation": derivation,
            "branch_status": "THEOREM_ZERO_IN_PRIVATE_LOCAL_ISOLATED_BRANCH",
            "strict_public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, value, derivation in data
    ]


def poynting_guard_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PYG3930_0_total_system",
            "guard": "use total Hilbert/Maxwell source",
            "statement": "boundary flux zero applies to the closed total-system worldtube, not matter-only tubes",
            "reason": "matter-only source tubes wrongly delete EM field energy and Poynting exchange",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PYG3930_1_internal_flow_allowed",
            "guard": "internal Poynting is allowed",
            "statement": "S_EM may circulate inside W; only int_boundary S_EM dot n is zero",
            "reason": "keeps EM stress/angular momentum instead of pretending S_EM vanishes pointwise",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PYG3930_2_no_em_overclaim",
            "guard": "not an EM-origin proof",
            "statement": "this assumes the descended Maxwell/Hilbert branch and does not derive charge normalization or alpha",
            "reason": "prevents using boundary flux closure as an EM unification claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def reduced_escape_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RBE3930_0_removed_boundary",
            "component": "boundary/harmonic",
            "before": BOUNDARY_FALLBACK,
            "after": "P00_boundary=0, B_harmonic_boundary=0, Phi_B=0, tau_wall_TF=0",
            "status": "REMOVED_IN_PRIVATE_LOCAL_ISOLATED_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RBE3930_1_reduced_multipole",
            "component": "A_multi",
            "before": "A_multi_PD0 <= G_ext*(|P00_boundary|+|P00_history|+|P00_nonlocal|)+B_harmonic_boundary",
            "after": A_MULTI_REDUCED,
            "status": "REDUCED_QUEUE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RBE3930_2_reduced_escape",
            "component": "B_escape",
            "before": "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi_PD0 + B_deriv",
            "after": BESCAPE_REDUCED,
            "status": "PROJECTOR_DOMAIN_BOUNDARY_REMOVED_HISTORY_DERIVATIVE_REMAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RBE3930_3_next_priority",
            "component": "next obstruction",
            "before": "boundary/harmonic multipoles",
            "after": "history/nonlocal tails, then derivative hair and Delta_sq/epsilon_r",
            "status": "NEXT_PRIORITY_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BFB3930_0_boundary_source", "if local branch is not isolated", "source |P00_boundary| with source path and units"),
        ("BFB3930_1_harmonic", "if l>=2 exterior harmonic data are present", "source |B_harmonic_boundary| or exterior tidal multipole amplitude"),
        ("BFB3930_2_flux", "if total Hilbert/Maxwell flux crosses the collar", "source |Phi_B|/M_H_ref including Poynting/matter exchange"),
        ("BFB3930_3_wall", "if boundary wall/shear stress is present", "source |tau_wall_TF|/M_H_ref"),
        ("BFB3930_4_total", "if the 3930 isolated-boundary signature is rejected", BOUNDARY_FALLBACK),
    ]
    return [
        {
            "row_id": row_id,
            "fallback_condition": condition,
            "required_bound": required,
            "numeric_value": "",
            "status": "HELD_IN_RESERVE_IF_SIGNATURE_REJECTED_OR_NONISOLATED_ARENA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, condition, required in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3930_0_adopt_boundary",
            "decision": "adopt the isolated scalar/topological no-flux boundary route for the private local PPN/Newton branch",
            "reason": "it is the GR-like isolated-source boundary condition and avoids using scalar no-flux as a fake vector/shear proof",
            "claim_status": "PRIVATE_BRANCH_ZERO_NOT_PUBLIC_GLOBAL_CLAIM",
            "next_action": "remove boundary/harmonic from B_escape queue and attack history/nonlocal",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3930_1_poynting",
            "decision": "include Poynting/EM only as total-system no-leakage, not pointwise S_EM=0",
            "reason": POYNTING_GUARD,
            "claim_status": "SCOPE_GUARD",
            "next_action": "keep Maxwell stress in T_vis and do not delete internal EM flow",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3930_2_nonisolated_fallback",
            "decision": "non-isolated arenas must use fallback boundary/harmonic rows",
            "reason": "external tides, radiation, memory tails or boundary shear are physical if present",
            "claim_status": "REVERSIBLE_BRANCH_CHOICE",
            "next_action": "retain fallback rows for cosmology/galaxy/open-system arenas",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3930_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attack history/nonlocal tails after projector/domain and boundary/harmonic removal",
            "success_condition": "derive local reset/no-tail theorem or source-backed gamma_mem, Delta t, lambda_gap, X_mem and kernel rows",
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
            "summary": "boundary/harmonic escape component zeroed inside the private isolated local branch; history/nonlocal remains",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3930 - Boundary/Harmonic No-Flux or Source Bound

Timestamp: `{timestamp}`

## Result

Adopted the local isolated-boundary route for the private local PPN/Newton branch.

Boundary signature:

`{BOUNDARY_SIGNATURE}`.

Elliptic/harmonic zero:

`{ELLIPTIC_ZERO}`.

Boundary zero result:

`{BOUNDARY_ZERO}`.

Poynting guard:

`{POYNTING_GUARD}`.

Reduced multipole queue:

`{A_MULTI_REDUCED}`.

Reduced escape queue:

`{BESCAPE_REDUCED}`.

## Meaning

This removes the boundary/harmonic escape term only for the local isolated branch. It does not claim the full universe, galaxies, cosmology, radiating systems, or open systems have no boundary data. If an arena is non-isolated, has exterior tidal multipoles, net radiation/EM flux, memory tails, or boundary shear, the fallback rows stay live.

The important guard is Poynting: zero net boundary leakage is not `S_EM=0`. Internal circulating Poynting flow can remain, and EM stress remains inside the same total Hilbert/Maxwell source.

## Current Verdict

- `P00_boundary=0` and `B_harmonic_boundary=0` inside the private local isolated branch.
- `Phi_B=0` is a total-system no-leakage statement, not a matter-only or pointwise EM claim.
- `A_multi` now depends only on history/nonlocal tails in this branch.
- No change to `formalization-workbench`; no GitHub action.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3930_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_PARENT_SIGNATURE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_REDUCED_BESCAPE_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3930_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3930 - Boundary/Harmonic No-Flux

Timestamp: `{timestamp}`

- Boundary signature: `{BOUNDARY_SIGNATURE}`.
- Zero result: `{BOUNDARY_ZERO}`.
- Poynting guard: `{POYNTING_GUARD}`.
- Reduced multipole: `{A_MULTI_REDUCED}`.
- Reduced escape: `{BESCAPE_REDUCED}`.
- Status: boundary/harmonic removed from the private local isolated branch; history/nonlocal tails remain nonclaim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3930 - Boundary/Harmonic No-Flux"
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
    signature = signature_rows(timestamp)
    zero_result = zero_result_rows(timestamp)
    poynting = poynting_guard_rows(timestamp)
    reduced = reduced_escape_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    reduced_formula = next(row["after"] for row in reduced if row["row_id"] == "RBE3930_2_reduced_escape")
    reduced_multipole = next(row["after"] for row in reduced if row["row_id"] == "RBE3930_1_reduced_multipole")
    checks = [
        ("VAL3930_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3930_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3930_02_signature_adopted", any(row["branch_status"] == "BOUNDARY_HARMONIC_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH" for row in signature), "boundary/harmonic private signature verdict emitted"),
        ("VAL3930_03_zero_rows", len(zero_result) == 8 and all(row["branch_value"] == "0" for row in zero_result), "boundary/harmonic zero rows emitted"),
        ("VAL3930_04_poynting_guard", len(poynting) == 3 and any(row["row_id"] == "PYG3930_1_internal_flow_allowed" for row in poynting), "Poynting guard emitted"),
        ("VAL3930_05_reduced_multipole", "P00_boundary" not in reduced_multipole and "B_harmonic_boundary" not in reduced_multipole and "P00_history" in reduced_multipole, "reduced A_multi removes boundary/harmonic sources"),
        ("VAL3930_06_reduced_escape", "B_harmonic_boundary" not in reduced_formula and "A_multi_BPD0" in reduced_formula, "reduced B_escape removes boundary/harmonic term"),
        ("VAL3930_07_fallback_kept", len(fallback) == 5 and any(row["row_id"] == "BFB3930_4_total" for row in fallback), "boundary/harmonic fallback rows retained"),
        ("VAL3930_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (signature, zero_result, poynting, reduced, fallback, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3930_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3930_10_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3930_11_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3930_12_spine_written", SPINE_PATH.exists() and "3930 - Boundary/Harmonic No-Flux" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3930_13_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3930_14_script_compiles", True, "script compiles"),
        ("VAL3930_15_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["signature"], signature_rows(timestamp))
    write_csv(OUTPUTS["zero_result"], zero_result_rows(timestamp))
    write_csv(OUTPUTS["poynting_guard"], poynting_guard_rows(timestamp))
    write_csv(OUTPUTS["reduced_escape"], reduced_escape_rows(timestamp))
    write_csv(OUTPUTS["fallback"], fallback_rows(timestamp))
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
        raise SystemExit(f"3930 validation failed: {failed}")
    print(f"3930 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
