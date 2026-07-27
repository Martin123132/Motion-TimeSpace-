from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3912"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3912-Y5-R2FR-source-domain-connection-from-product-quotient-geometry-or-bound-input.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3912_SOURCE_REGISTER.csv",
    "bundle": SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv",
    "massflat": SRC / "P8_Y5_R2FR_3912_MASS_FLAT_CONNECTION_BRANCH_GATE.csv",
    "excluded": SRC / "P8_Y5_R2FR_3912_SOURCE_ACTIVE_EXCLUSION_ROWS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3912_CONNECTION_COEFFICIENT_BOUND_INPUT_ROWS.csv",
    "impact": SRC / "P8_Y5_R2FR_3912_LOCAL_ARENA_IMPACT.csv",
    "decision": SRC / "P8_Y5_R2FR_3912_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3912_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3912_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3912_VALIDATION.csv",
}

SOURCE_QUOTIENT = "Phi_src <-> (Q_pub, S_src=(M,s^a), R_ref=(tau,Sigma,H_ref), Y_loc, H_priv), q_src(Phi_src)=(Q_pub,S_src,R_ref)"
SOURCE_SILENT_VERTICAL = "X_v in ker(Dq_src) => D_X Q_pub=0, D_X M=0, D_X s^a=0, D_X tau=0, D_X Sigma=0, D_X H_ref=0"
CONNECTION_ZERO = "for source-silent vertical X_v, the product-chart horizontal lift has A_X^M=A_X^a=A_X^I=0, hence partial_M A_X^A=0"
PIM_ZERO = "[D_Xv,Pi_M^H]H=0 and R_PiM=0 for the source-silent vertical class"
FAILURE_CLASS = "source-active X not in ker(Dq_src) keeps R_PiM <= K_M|partial_M A_X^M|+K_shape||partial_M A_X^a||+K_ref||partial_M A_X^I||"


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
        ("SRC3912_00_next", SRC / "P8_Y5_R2FR_3911_NEXT_TARGET.csv", "NEXT3911_0", "3911 selected source-domain connection target"),
        ("SRC3912_01_3911_chart", SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv", "CON3911_0_source_chart", "3911 source chart"),
        ("SRC3912_02_3911_lift", SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv", "CON3911_1_horizontal_lift", "3911 horizontal lift"),
        ("SRC3912_03_3911_zero", SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv", "CON3911_3_mass_flat_zero", "3911 mass-flat zero condition"),
        ("SRC3912_04_3911_combined", SRC / "P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv", "COM3911_1_double_zero_branch", "3911 double-zero branch"),
        ("SRC3912_05_product_chart", SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv", "PCH3904_0_chart", "3904 product chart"),
        ("SRC3912_06_Dq_zero", SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv", "PCH3904_1_Dq", "3904 Dq verticality proof"),
        ("SRC3912_07_projector", SRC / "P8_Y5_R2FR_3904_DQ_MEMORY_VERTICALITY_MATRIX.csv", "DQM3904_5_projector_readout", "projector/readout order zero clause"),
        ("SRC3912_08_coefficients", SRC / "P8_Y5_R2FR_3904_DQ_MEMORY_VERTICALITY_MATRIX.csv", "DQM3904_4_coupling_slots", "coefficient descent clause"),
        ("SRC3912_09_normal_form", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_0_action", "3905 parent action normal form"),
        ("SRC3912_10_no_linear", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_2_interactions", "no linear visible shadow rule"),
        ("SRC3912_11_constants", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_4_constants", "visible constants owner clause"),
        ("SRC3912_12_GR", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_1_GR_equation", "conditional local GR reduction"),
        ("SRC3912_13_Newton", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_3_Newton", "conditional Newtonian limit"),
        ("SRC3912_14_support", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector", "worldtube support selector"),
        ("SRC3912_15_no_mask", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_2_no_readout_domain_mask", "source domain not selected after readout"),
        ("SRC3912_16_worldtube", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_3_matter_worldtube_verdict", "worldtube vertical silence unsigned"),
        ("SRC3912_17_pim", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_4_PiM", "Hamiltonian Pi_M definition"),
        ("SRC3912_18_comm", SRC / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_5_commutator_stress", "Pi_M commutator stress"),
        ("SRC3912_19_validation", SRC / "P8_Y5_BRR545_3911_VALIDATION.csv", "VAL3911_12_no_pycache", "3911 validation handoff"),
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


def bundle_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BUN3912_0_source_quotient",
            "object": "q_src",
            "formula": SOURCE_QUOTIENT,
            "derivation_status": "PRODUCT_QUOTIENT_EXTENSION_CONSTRUCTED",
            "what_is_derived": "source mass, source shape and reference data are base labels rather than hidden fibre readouts",
            "failure_mode": "if M,s^a,tau,Sigma,H_ref depend on Y_loc/H_priv, the connection is source-active and must be bounded",
            "source_path": str(SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUN3912_1_source_silent_vertical",
            "object": "ker(Dq_src)",
            "formula": SOURCE_SILENT_VERTICAL,
            "derivation_status": "DIRECT_FROM_QSRC_PROJECTION",
            "what_is_derived": "source-silent residual directions cannot move the mass coordinate, source shape, tau, surface or reference subtraction",
            "failure_mode": "source-active coupling or support variation is not in ker(Dq_src)",
            "source_path": str(SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUN3912_2_worldtube_basic",
            "object": "W_source",
            "formula": "W_source=closure(supp J_H[tau]) is q_src-basic when J_H,tau and compact support descend to (Q_pub,S_src,R_ref)",
            "derivation_status": "CONDITIONAL_SELECTOR_DESCENT",
            "what_is_derived": "the source support is not chosen after orbital/PPN/R10 readout inside the source-silent branch",
            "failure_mode": "support mask or Hodge/surface pair depends on hidden fibre variables",
            "source_path": str(SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def massflat_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MF3912_0_connection_coefficients",
            "object": "A_X^A",
            "formula": CONNECTION_ZERO,
            "derivation_status": "DERIVED_FOR_SOURCE_SILENT_VERTICAL_CLASS",
            "claim_scope": "local stationary/source-silent residual directions only",
            "remaining_gap": "parent must adopt q_src as the source quotient, not merely a bookkeeping chart",
            "source_path": str(SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MF3912_1_PiM_commutator",
            "object": "R_PiM",
            "formula": PIM_ZERO,
            "derivation_status": "CONDITIONAL_RPIM_ZERO_THEOREM",
            "claim_scope": "source-silent vertical class with fixed Pi_M variable list and fixed H_ref/tau/Sigma",
            "remaining_gap": "H_tau curl still open; source-active branches excluded",
            "source_path": str(SRC / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MF3912_2_combined_reduction",
            "object": "R_PiM_plus_R_Htau",
            "formula": "under q_src source-silent verticality, R_PiM+R_Htau reduces to R_Htau",
            "derivation_status": "DERIVED_REDUCTION_OF_3911_DOUBLE_ZERO_ROUTE",
            "claim_scope": "source-silent branch only",
            "remaining_gap": "derive or bound H_tau source-collar symplectic curl",
            "source_path": str(SRC / "P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def excluded_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EX3912_0_source_coupling",
            "excluded_direction": "X changes ell_J, masses, charges, alpha, C_source or matter coupling slots",
            "reason": "not source-silent; D_X S_src or D_X coefficient slots may be nonzero",
            "fallback": FAILURE_CLASS,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EX3912_1_support_shape",
            "excluded_direction": "X changes W_source, source shape s^a, Hodge domain or linked surfaces",
            "reason": "source support is no longer q_src-basic",
            "fallback": FAILURE_CLASS,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EX3912_2_reference_frame",
            "excluded_direction": "X changes tau, Sigma, H_ref, asymptotic coframe or readout frame",
            "reason": "reference/frame variables are not fixed base labels",
            "fallback": FAILURE_CLASS,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EX3912_3_dynamic_time",
            "excluded_direction": "cosmological or genuinely dynamic time drift of source data",
            "reason": "stationary source collar assumption fails",
            "fallback": FAILURE_CLASS,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CB3912_0_KM",
            "coefficient": "K_M",
            "definition": "K_M := |partial_M H|/|Pi_M H_tau| for the chosen source surface and branch",
            "numeric_value": "",
            "unit": "dimensionless after D_X is assigned units",
            "source_status": "MISSING_PARENT_NUMERIC_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CB3912_1_Kshape",
            "coefficient": "K_shape",
            "definition": "K_shape := ||partial_a H||/|Pi_M H_tau| for source-shape leakage",
            "numeric_value": "",
            "unit": "dimensionless after D_X is assigned units",
            "source_status": "MISSING_PARENT_NUMERIC_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CB3912_2_Kref",
            "coefficient": "K_ref",
            "definition": "K_ref := ||partial_I H||/|Pi_M H_tau| for reference/surface/frame leakage",
            "numeric_value": "",
            "unit": "dimensionless after D_X is assigned units",
            "source_status": "MISSING_PARENT_NUMERIC_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CB3912_3_A_mass_slope",
            "coefficient": "partial_M A_X^M",
            "definition": "mass-connection slope of source-active residual direction",
            "numeric_value": "",
            "unit": "per source mass in the selected coordinate convention",
            "source_status": "ZERO_IN_SOURCE_SILENT_BRANCH_ELSE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CB3912_4_A_shape_slope",
            "coefficient": "partial_M A_X^a",
            "definition": "shape-leakage slope of source-active residual direction",
            "numeric_value": "",
            "unit": "shape-coordinate per source mass",
            "source_status": "ZERO_IN_SOURCE_SILENT_BRANCH_ELSE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CB3912_5_A_ref_slope",
            "coefficient": "partial_M A_X^I",
            "definition": "reference/surface/frame leakage slope of source-active residual direction",
            "numeric_value": "",
            "unit": "reference-coordinate per source mass",
            "source_status": "ZERO_IN_SOURCE_SILENT_BRANCH_ELSE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def impact_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "IMP3912_0_local_stationary_PPN",
            "arena": "local stationary PPN/Newton",
            "impact": "R_PiM can be theorem-zero inside q_src source-silent branch",
            "remaining_blocker": "R_Htau curl exactness plus Z_Poisson/Z_frame/epsilon_mu",
            "claim_status": "NOT_A_PASS_YET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IMP3912_1_R10",
            "arena": "R10 short-range/source denominator",
            "impact": "Qbar_XH denominator no longer gets Pi_M commutator leakage for source-silent verticals",
            "remaining_blocker": "H_tau integrability, H_ref, source-shadow/edge split, real alpha(lambda) bounds",
            "claim_status": "NOT_A_PASS_YET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IMP3912_2_Gdot",
            "arena": "dotG/G",
            "impact": "B_PiM_Htau reduces to B_Htau for source-silent stationary collar",
            "remaining_blocker": "dynamic source branches and H_tau curl/bound rows",
            "claim_status": "NOT_A_PASS_YET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3912_0_closed_piece",
            "decision": "derive R_PiM=0 for source-silent vertical residuals in the q_src product-quotient branch",
            "claim_status": "CONDITIONAL_DERIVATION_NOT_PUBLIC_CLAIM",
            "reason": "mass/source/reference labels are base coordinates, so vertical fibre motion cannot generate mass-connection slope",
            "next_action": "attack R_Htau exact symplectic-curl theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3912_1_rejected_scope",
            "decision": "do not extend R_PiM=0 to source-active coupling/support/reference/time directions",
            "claim_status": "SCOPE_RESTRICTED",
            "reason": "those directions are not in ker(Dq_src) and require coefficient bounds",
            "next_action": "retain coefficient-bound rows for those branches",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3912_2_selected_next",
            "decision": "next target is H_tau exact symplectic-curl/source-collar theorem",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "after R_PiM is killed for source-silent branch, R_Htau is the remaining algebraic heart of the double-zero route",
            "next_action": "3913-Htau-exact-symplectic-curl-from-EH-source-collar-or-bound.md",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3912_0",
            "next_doc": "3913-Y5-R2FR-Htau-exact-symplectic-curl-from-EH-source-collar-or-bound.md",
            "next_script": "scripts/Y5_R2FR_3913_Htau_exact_symplectic_curl_from_EH_source_collar_or_bound.py",
            "target": "derive R_Htau=0 from EH/Iyer-Wald source-collar exactness plus extra-sector flux silence, or produce source-backed curl bound rows",
            "why_this_next": "3912 conditionally kills R_PiM for source-silent residuals; R_Htau is now the remaining Pi_M/H_tau core blocker",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "R_PiM conditionally closed for source-silent q_src verticals; source-active directions demoted to coefficient-bound rows",
            "local_gr_claim": False,
            "gdot_claim": False,
            "new_forward_progress": "one half of the Pi_M/H_tau obstruction is now derivable in a named branch rather than merely missing",
            "primary_blocker": "R_Htau exact symplectic-curl/source-collar theorem",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3912 — Source-Domain Connection from Product/Quotient Geometry or Bound Input

Timestamp: `{timestamp}`

## Result

This checkpoint derives the mass-flat connection for the source-silent branch instead of just declaring it.

Source quotient:
`{SOURCE_QUOTIENT}`

Source-silent vertical:
`{SOURCE_SILENT_VERTICAL}`

Connection consequence:
`{CONNECTION_ZERO}`

PiM result:
`{PIM_ZERO}`

Failure class:
`{FAILURE_CLASS}`

## Meaning

- For residual directions genuinely vertical to the public/source quotient, `R_PiM=0`.
- The proof is conditional on adopting `q_src`; it is not a public local-GR claim.
- Source-active coupling, support, reference/frame and dynamic-time directions are excluded and get coefficient-bound rows instead.
- The combined 3911 blocker reduces from `R_PiM+R_Htau` to `R_Htau` only in the source-silent stationary branch.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['bundle'])}`
- `{rel(OUTPUTS['massflat'])}`
- `{rel(OUTPUTS['excluded'])}`
- `{rel(OUTPUTS['bounds'])}`
- `{rel(OUTPUTS['impact'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`3913-Y5-R2FR-Htau-exact-symplectic-curl-from-EH-source-collar-or-bound.md`

Goal: derive `R_Htau=0` from EH/Iyer-Wald source-collar exactness plus extra-sector flux silence, or make the curl a source-backed numeric bound.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3912 SOURCE DOMAIN MASS FLAT CONNECTION -->
## 3912 Source-Domain Mass-Flat Connection

Timestamp: `{timestamp}`

Source quotient:
`{SOURCE_QUOTIENT}`

Source-silent vertical:
`{SOURCE_SILENT_VERTICAL}`

Connection consequence:
`{CONNECTION_ZERO}`

PiM result:
`{PIM_ZERO}`

Scope rule:
`{FAILURE_CLASS}`

Decision: `R_PiM=0` is derived for source-silent q_src verticals, while source-active directions remain coefficient-bound. The local source-denominator core now reduces to `R_Htau` in the stationary source-silent branch.
<!-- END 3912 SOURCE DOMAIN MASS FLAT CONNECTION -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3912 SOURCE DOMAIN MASS FLAT CONNECTION -->"
    end = "<!-- END 3912 SOURCE DOMAIN MASS FLAT CONNECTION -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    bundle: list[dict[str, Any]],
    massflat: list[dict[str, Any]],
    excluded: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(
        (
            "VAL3912_0_sources",
            "all cited source paths and needles resolve",
            all(row["exists"] and row["needle_found"] for row in sources),
            f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found",
        )
    )
    checks.append(("VAL3912_1_qsrc", "q_src source quotient row emitted", any(SOURCE_QUOTIENT in row["formula"] for row in bundle), rel(OUTPUTS["bundle"])))
    checks.append(("VAL3912_2_vertical", "source-silent vertical row emitted", any(SOURCE_SILENT_VERTICAL in row["formula"] for row in bundle), rel(OUTPUTS["bundle"])))
    checks.append(("VAL3912_3_massflat", "mass-flat connection consequence emitted", any(CONNECTION_ZERO in row["formula"] for row in massflat), rel(OUTPUTS["massflat"])))
    checks.append(("VAL3912_4_rpim_zero", "R_PiM zero row emitted", any(PIM_ZERO in row["formula"] for row in massflat), rel(OUTPUTS["massflat"])))
    checks.append(("VAL3912_5_scope_exclusions", "source-active exclusions present", len(excluded) >= 4 and all("source-active" in row["fallback"] for row in excluded), rel(OUTPUTS["excluded"])))
    checks.append(("VAL3912_6_bound_inputs", "coefficient-bound rows remain nonclaim", len(bounds) >= 6 and all(str(row.get("valid_for_claim")) == "False" for row in bounds), rel(OUTPUTS["bounds"])))
    checks.append(("VAL3912_7_impact", "arena impact rows include Gdot/R10/PPN", {"dotG/G", "R10 short-range/source denominator", "local stationary PPN/Newton"}.issubset({row["arena"] for row in impact}), rel(OUTPUTS["impact"])))
    checks.append(("VAL3912_8_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in bundle + massflat + excluded + bounds + impact + decision), "valid_for_claim false across all generated rows"))
    checks.append(("VAL3912_9_next_target", "next target attacks H_tau curl", "3913-Y5-R2FR-Htau" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3912_10_doc", "3912 markdown checkpoint written", DOC_PATH.exists() and "Source-Domain Connection" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3912_11_spine", "spine updated with 3912 block", SPINE_PATH.exists() and "BEGIN 3912 SOURCE DOMAIN MASS FLAT CONNECTION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
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
    checks.append(("VAL3912_12_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3912*")) if FWB.exists() else []
    checks.append(("VAL3912_13_no_formalization_workbench_edits", "no 3912 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3912_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
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
    bundle = bundle_rows(timestamp)
    massflat = massflat_rows(timestamp)
    excluded = excluded_rows(timestamp)
    bounds = bound_rows(timestamp)
    impact = impact_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["bundle"], bundle)
    write_csv(OUTPUTS["massflat"], massflat)
    write_csv(OUTPUTS["excluded"], excluded)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["impact"], impact)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, bundle, massflat, excluded, bounds, impact, decision, timestamp)
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
