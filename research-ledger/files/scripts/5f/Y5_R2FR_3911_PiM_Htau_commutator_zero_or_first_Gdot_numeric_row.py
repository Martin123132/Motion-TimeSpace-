from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3911"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3911-Y5-R2FR-PiM-Htau-commutator-zero-or-first-Gdot-numeric-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3911_SOURCE_REGISTER.csv",
    "connection": SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv",
    "curl": SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv",
    "combined": SRC / "P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv",
    "gdot": SRC / "P8_Y5_R2FR_3911_FIRST_GDOT_NUMERIC_NONCLAIM_ROW.csv",
    "decision": SRC / "P8_Y5_R2FR_3911_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3911_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3911_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3911_VALIDATION.csv",
}

SOURCE_CHART = "z^A=(M,s^a,r^I) with Pi_M^H=partial_M at fixed shape s^a, reference/surface/frame r^I"
HORIZONTAL_LIFT = "D_X^H = D_X + A_X^M partial_M + A_X^a partial_a + A_X^I partial_I"
COMMUTATOR_ID = "[D_X^H,Pi_M^H]H = -(partial_M A_X^M) partial_M H -(partial_M A_X^a) partial_a H -(partial_M A_X^I) partial_I H"
MASS_FLAT_ZERO = "if partial_M A_X^M=partial_M A_X^a=partial_M A_X^I=0 and D_X^H keeps tau,Sigma,H_ref fixed, then [D_X^H,Pi_M^H]H=0"
CURL_ID = "curl(delta H_tau)(delta_1,delta_2)=int_S i_tau omega_MTS(delta_1,delta_2)+int_partialS corner_tau(delta_1,delta_2)"
HTAU_ZERO = "if tau is fixed/stationary, omega_MTS has zero or exact boundary flux on the source collar, and reference/corner terms are source-blind, then R_Htau=0"
COMBINED_BOUND = "|R_PiM+R_Htau| <= K_M|partial_M A_X^M| + K_shape||partial_M A_X^a|| + K_ref||partial_M A_X^I|| + |Pi_M int_S i_tau omega_MTS|/|Pi_M H_tau| + |corner_tau|/|Pi_M H_tau|"
GDOT_BOUND = "Gdot_total <= 0 + (|R_PiM+R_Htau| + |R_Ward| + |R_ref| + |R_W| + |R_frame| + |R_units| + |R_side_flux|) + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3911_00_next", SRC / "P8_Y5_R2FR_3910_NEXT_TARGET.csv", "NEXT3910_0", "3910 selected Pi_M/H_tau commutator-curl target"),
        ("SRC3911_01_obs_total", SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv", "OBS3910_0_total_bound", "3910 measured-source drift obstruction envelope"),
        ("SRC3911_02_obs_pim", SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv", "OBS3910_1_R_PiM", "3910 Pi_M commutator obstruction"),
        ("SRC3911_03_obs_htau", SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv", "OBS3910_2_R_Htau", "3910 H_tau curl obstruction"),
        ("SRC3911_04_3514_total", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total", "combined Pi_M/H_tau residual law"),
        ("SRC3911_05_3514_CM", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_1_C_M", "mass-coordinate connection curvature row"),
        ("SRC3911_06_3514_shape", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_2_C_shape", "shape leakage row"),
        ("SRC3911_07_3514_curl", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_3_C_curl", "H_tau curl row"),
        ("SRC3911_08_2665_pim", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_4_PiM", "Hamiltonian Pi_M definition"),
        ("SRC3911_09_2665_stress", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_5_commutator_stress", "Pi_M commutator stress source row"),
        ("SRC3911_10_2667_owner", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_1_theta_omega", "theta/omega owner missing gate"),
        ("SRC3911_11_2667_boundary", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_3_boundary_exact", "boundary exactness gate"),
        ("SRC3911_12_2667_verdict", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_7_verdict", "H_tau curl not claim-ready verdict"),
        ("SRC3911_13_2611_support", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector", "worldtube support selector condition"),
        ("SRC3911_14_2611_charge", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_1_same_charge", "worldtube same-charge blocker"),
        ("SRC3911_15_2938_mhref", SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_0_MHref_definition", "M_H_ref denominator definition"),
        ("SRC3911_16_2938_href", SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_1_Href_selector", "H_ref source-blind selector contract"),
        ("SRC3911_17_2938_guard", SRC / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_4_no_laundering", "anti-circularity guardrail"),
        ("SRC3911_18_3910_gdot", SRC / "P8_Y5_R2FR_3910_GDOT_MEFF_COMPONENT_RUNNER.csv", "GDM3910_2_total_Gdot_after_Meff", "3910 Gdot after M_eff runner"),
        ("SRC3911_19_validation", SRC / "P8_Y5_BRR545_3910_VALIDATION.csv", "VAL3910_12_no_pycache", "3910 validation handoff"),
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
                    excerpt = line[:500]
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


def connection_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CON3911_0_source_chart",
            "object": "source chart",
            "formula": SOURCE_CHART,
            "derivation_status": "COORDINATE_GAUGE_DECLARED_NOT_PHYSICS_ASSUMED",
            "zero_condition": "M is the parent Hamiltonian mass coordinate and s^a,r^I are fixed readout variables before scoring",
            "source_path": str(SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CON3911_1_horizontal_lift",
            "object": "source-domain connection",
            "formula": HORIZONTAL_LIFT,
            "derivation_status": "CONNECTION_PARAMETERIZATION",
            "zero_condition": "parent action or source-domain geometry must own A_X^A, not fit it from the observable residual",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CON3911_2_commutator_identity",
            "object": "[D_X^H,Pi_M^H]",
            "formula": COMMUTATOR_ID,
            "derivation_status": "DERIVED_EXACT_LOCAL_CHART_IDENTITY",
            "zero_condition": "mass-flat connection and fixed reference/surface/frame variables",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CON3911_3_mass_flat_zero",
            "object": "R_PiM",
            "formula": MASS_FLAT_ZERO,
            "derivation_status": "CONDITIONAL_ZERO_THEOREM",
            "zero_condition": "partial_M A_X^A=0 for A=M,a,I and D_X^H H_ref=D_X^H tau=D_X^H Sigma=0",
            "source_path": str(SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CON3911_4_nonzero_bound",
            "object": "R_PiM bound",
            "formula": "|R_PiM| <= K_M|partial_M A_X^M| + K_shape||partial_M A_X^a|| + K_ref||partial_M A_X^I||",
            "derivation_status": "EXACT_NORM_BOUND_FROM_COMMUTATOR",
            "zero_condition": "all connection mass-derivatives vanish, or the K-weighted envelope is source-backed numeric",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def curl_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CURL3911_0_covariant_phase_space_identity",
            "object": "curl(delta H_tau)",
            "formula": CURL_ID,
            "derivation_status": "STANDARD_COVARIANT_PHASE_SPACE_IDENTITY_IMPORTED_AS_CONTRACT",
            "zero_condition": "omega_MTS and corner terms are parent-derived with declared units",
            "source_path": str(SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CURL3911_1_stationary_exact_flux_zero",
            "object": "R_Htau",
            "formula": HTAU_ZERO,
            "derivation_status": "CONDITIONAL_ZERO_THEOREM",
            "zero_condition": "stationary isolated source collar, fixed tau/surface pair, exact or zero boundary symplectic flux, source-blind reference",
            "source_path": str(SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CURL3911_2_nonzero_bound",
            "object": "R_Htau bound",
            "formula": "|R_Htau| <= |Pi_M int_S i_tau omega_MTS|/|Pi_M H_tau| + |corner_tau|/|Pi_M H_tau| + |reference_curl|/|Pi_M H_tau|",
            "derivation_status": "EXACT_NORM_BOUND_FROM_CURL_IDENTITY",
            "zero_condition": "symplectic/corner/reference curls vanish or get source-backed numeric rows",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CURL3911_3_parent_gap",
            "object": "theta/omega owner",
            "formula": "theta_MTS, omega_MTS, tau lock, surface lock, boundary exactness and reference split are required before claim",
            "derivation_status": "PARENT_OWNERSHIP_GAP_EXPLICIT",
            "zero_condition": "future parent action supplies theta/omega and exact flux theorem",
            "source_path": str(SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def combined_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "COM3911_0_combined_exact_bound",
            "object": "R_PiM_plus_R_Htau",
            "formula": COMBINED_BOUND,
            "derivation_status": "DERIVED_COMBINED_BOUND",
            "claim_status": "NONCLAIM_UNTIL_COEFFICIENTS_OR_ZERO_THEOREMS_ARE_PARENT_SIGNED",
            "next_action": "try to derive source-domain connection from quotient/product chart before numeric scoring",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COM3911_1_double_zero_branch",
            "object": "R_PiM_plus_R_Htau zero branch",
            "formula": "R_PiM+R_Htau=0 if the source connection is mass-flat and H_tau has exact/zero source-collar symplectic curl",
            "derivation_status": "CONDITIONAL_DOUBLE_ZERO_THEOREM",
            "claim_status": "PROMISING_INTERNAL_BRANCH_NOT_PARENT_ADOPTED",
            "next_action": "derive mass-flat source-domain connection from q(Phi) rather than declaring it",
            "source_path": str(SRC / "P8_Y5_R2FR_3910_PIM_HTAU_OBSTRUCTION_SPLIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "COM3911_2_unconditional_verdict",
            "object": "unconditional local source denominator",
            "formula": "unconditional R_PiM+R_Htau=0 is not proved because A_X^A and omega_MTS are not parent-owned here",
            "derivation_status": "UNCONDITIONAL_ZERO_REJECTED_FOR_NOW",
            "claim_status": "NO_GDOT_NEWTON_PPN_R10_CLAIM_FROM_3911",
            "next_action": "3912 should derive A_X^A from source quotient/product geometry or demote to numeric bound input",
            "source_path": str(SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gdot_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GDN3911_0_numeric_slot",
            "quantity": "B_PiM_Htau",
            "formula": COMBINED_BOUND,
            "numeric_value_per_year": "",
            "unit": "yr^-1 for Gdot use after D_X is chosen as time drift",
            "coefficient_requirements": "K_M,K_shape,K_ref,Pi_M H_tau,Pi_M int_S i_tau omega_MTS,corner_tau",
            "source_status": "NUMERIC_SLOT_CREATED_NO_PARENT_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDN3911_1_acceptance_budget",
            "quantity": "dotG/G acceptance budget",
            "formula": GDOT_BOUND,
            "numeric_value_per_year": "9.6e-15",
            "unit": "yr^-1 upper target for full residual sum",
            "coefficient_requirements": "B_PiM_Htau plus other 3910 residuals must be numeric or theorem-zero",
            "source_status": "TARGET_ONLY_NOT_A_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GDN3911_2_zero_smoke",
            "quantity": "stationary-collar smoke value",
            "formula": "if CON3911_3 and CURL3911_1 both hold, B_PiM_Htau=0",
            "numeric_value_per_year": "0",
            "unit": "yr^-1",
            "coefficient_requirements": "mass-flat connection and exact/zero H_tau curl must be parent-signed first",
            "source_status": "SYMBOLIC_SMOKE_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3911_0_progress",
            "decision": "R_PiM+R_Htau has been reduced to a mass-flat source connection plus exact H_tau symplectic-curl condition",
            "claim_status": "REAL_DERIVATION_PROGRESS_NONCLAIM",
            "reason": "the commutator identity and curl identity give a precise route to zero or a precise coefficient bound",
            "next_action": "derive the source-domain connection from q(Phi)/product chart",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3911_1_rejection",
            "decision": "do not claim unconditional source-denominator closure",
            "claim_status": "UNCONDITIONAL_ZERO_REJECTED",
            "reason": "A_X^A and omega_MTS are still not parent-owned by an explicit source-sector action",
            "next_action": "do not publish local-GR/Newton/PPN/R10 pass from this branch yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3911_2_selected_next",
            "decision": "next target is the parent source-domain connection derivation",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "one derived mass-flat connection would simultaneously kill C_M and C_shape and make the bound smaller before numeric scoring",
            "next_action": "3912-source-domain-connection-from-product-quotient-geometry-or-bound-input.md",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3911_0",
            "next_doc": "3912-Y5-R2FR-source-domain-connection-from-product-quotient-geometry-or-bound-input.md",
            "next_script": "scripts/Y5_R2FR_3912_source_domain_connection_from_product_quotient_geometry_or_bound_input.py",
            "target": "derive A_X^A mass-flatness from the parent quotient/product chart and source support selector; if it fails, create the first coefficient-bound input rows for K_M, K_shape and K_ref",
            "why_this_next": "3911 shows the double-zero route is mathematically clean, but it needs parent ownership of the source-domain connection rather than a declared horizontal lift",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "Pi_M/H_tau obstruction converted into exact commutator identity, exact curl identity, conditional double-zero theorem and coefficient bound slot",
            "local_gr_claim": False,
            "gdot_claim": False,
            "new_forward_progress": "the algebraic heart now has a concrete mass-flat connection target, not just a missing-coupling label",
            "primary_blocker": "parent ownership of A_X^A and omega_MTS/source-collar exactness",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, Any]],
    timestamp: str,
) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3911 — PiM/Htau Commutator Zero or First Gdot Numeric Row

Timestamp: `{timestamp}`

## Result

This pass attacks the source-coupling algebra directly. The `R_PiM + R_Htau` blocker is now a two-part derivation target:

1. a source-domain connection commutator;
2. a covariant-phase-space `H_tau` curl.

Source chart:
`{SOURCE_CHART}`

Horizontal lift:
`{HORIZONTAL_LIFT}`

Exact commutator:
`{COMMUTATOR_ID}`

Mass-flat zero condition:
`{MASS_FLAT_ZERO}`

Hamiltonian curl identity:
`{CURL_ID}`

Htau zero condition:
`{HTAU_ZERO}`

Combined executable bound:
`{COMBINED_BOUND}`

## What This Means

- If the parent source geometry forces a mass-flat horizontal lift and an exact/zero source-collar symplectic curl, then `R_PiM+R_Htau=0`.
- If not, the same equations give coefficient rows for a nonclaim `dotG/G` bound.
- The result is not a local-GR/Newton/PPN/R10 claim yet because `A_X^A` and `omega_MTS` are not parent-owned in this checkpoint.

## First Nonclaim Gdot Slot

`{GDOT_BOUND}`

The `0` smoke row exists only for the double-zero branch. It remains `valid_for_claim=false` until the parent action signs the source-domain connection and `H_tau` curl exactness.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['connection'])}`
- `{rel(OUTPUTS['curl'])}`
- `{rel(OUTPUTS['combined'])}`
- `{rel(OUTPUTS['gdot'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`3912-Y5-R2FR-source-domain-connection-from-product-quotient-geometry-or-bound-input.md`

Goal: derive `A_X^A` mass-flatness from the parent quotient/product chart, or demote that part to explicit coefficient-bound inputs.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3911 PIM HTAU COMMUTATOR CURL -->
## 3911 PiM/Htau Commutator-Curl Gate

Timestamp: `{timestamp}`

Source-domain chart:
`{SOURCE_CHART}`

Commutator identity:
`{COMMUTATOR_ID}`

Mass-flat zero:
`{MASS_FLAT_ZERO}`

Hamiltonian curl identity:
`{CURL_ID}`

Combined bound:
`{COMBINED_BOUND}`

Decision: the double-zero route is mathematically clean but still parent-conditional. Next target is deriving the mass-flat source-domain connection from the product/quotient geometry instead of declaring the horizontal lift.
<!-- END 3911 PIM HTAU COMMUTATOR CURL -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3911 PIM HTAU COMMUTATOR CURL -->"
    end = "<!-- END 3911 PIM HTAU COMMUTATOR CURL -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    connection: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    combined: list[dict[str, Any]],
    gdot: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(
        (
            "VAL3911_0_sources",
            "all cited source paths and needles resolve",
            all(row["exists"] and row["needle_found"] for row in sources),
            f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found",
        )
    )
    checks.append(
        (
            "VAL3911_1_commutator_identity",
            "exact Pi_M commutator identity emitted",
            any(COMMUTATOR_ID in row["formula"] for row in connection),
            rel(OUTPUTS["connection"]),
        )
    )
    checks.append(
        (
            "VAL3911_2_mass_flat_zero",
            "mass-flat zero condition emitted",
            any("partial_M A_X^M" in row["formula"] and "[D_X^H,Pi_M^H]H=0" in row["formula"] for row in connection),
            rel(OUTPUTS["connection"]),
        )
    )
    checks.append(
        (
            "VAL3911_3_curl_identity",
            "H_tau curl identity emitted",
            any(CURL_ID in row["formula"] for row in curl),
            rel(OUTPUTS["curl"]),
        )
    )
    checks.append(
        (
            "VAL3911_4_combined_bound",
            "combined Pi_M/H_tau bound emitted",
            any(COMBINED_BOUND in row["formula"] for row in combined + gdot),
            rel(OUTPUTS["combined"]),
        )
    )
    checks.append(
        (
            "VAL3911_5_nonclaim_numeric_slot",
            "first Gdot numeric slot remains nonclaim",
            any(row["row_id"] == "GDN3911_0_numeric_slot" for row in gdot) and all(str(row.get("valid_for_claim")) == "False" for row in gdot),
            rel(OUTPUTS["gdot"]),
        )
    )
    checks.append(
        (
            "VAL3911_6_no_claim",
            "all generated rows remain nonclaim",
            all(str(row.get("valid_for_claim")) == "False" for row in connection + curl + combined + gdot + decision),
            "valid_for_claim false across derivation, curl, combined, gdot and decision rows",
        )
    )
    checks.append(
        (
            "VAL3911_7_next_target",
            "next target is source-domain connection from product/quotient geometry",
            "3912-Y5-R2FR-source-domain-connection" in read_text(OUTPUTS["next"]),
            rel(OUTPUTS["next"]),
        )
    )
    checks.append(
        (
            "VAL3911_8_doc",
            "3911 markdown checkpoint written",
            DOC_PATH.exists() and "PiM/Htau Commutator" in read_text(DOC_PATH),
            rel(DOC_PATH),
        )
    )
    checks.append(
        (
            "VAL3911_9_spine",
            "spine updated with 3911 block",
            SPINE_PATH.exists() and "BEGIN 3911 PIM HTAU COMMUTATOR CURL" in read_text(SPINE_PATH),
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
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{type(exc).__name__}:{exc}")
    checks.append(("VAL3911_10_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3911*")) if FWB.exists() else []
    checks.append(
        (
            "VAL3911_11_no_formalization_workbench_edits",
            "no 3911 files generated in formalization-workbench",
            not fwb_hits,
            "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits",
        )
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(
        (
            "VAL3911_12_no_pycache",
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
    connection = connection_rows(timestamp)
    curl = curl_rows(timestamp)
    combined = combined_rows(timestamp)
    gdot = gdot_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["connection"], connection)
    write_csv(OUTPUTS["curl"], curl)
    write_csv(OUTPUTS["combined"], combined)
    write_csv(OUTPUTS["gdot"], gdot)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, connection, curl, combined, gdot, decision, timestamp)
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
