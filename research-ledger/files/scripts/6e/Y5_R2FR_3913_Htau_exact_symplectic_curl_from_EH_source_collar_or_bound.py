from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3913"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3913-Y5-R2FR-Htau-exact-symplectic-curl-from-EH-source-collar-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3913_SOURCE_REGISTER.csv",
    "curl": SRC / "P8_Y5_R2FR_3913_HTAU_EXACT_CURL_THEOREM.csv",
    "extra": SRC / "P8_Y5_R2FR_3913_EXTRA_SECTOR_FLUX_SILENCE.csv",
    "meff": SRC / "P8_Y5_R2FR_3913_MEFF_STATIONARY_SOURCE_CLOSURE_STACK.csv",
    "remaining": SRC / "P8_Y5_R2FR_3913_REMAINING_LOCAL_GR_RESIDUALS.csv",
    "decision": SRC / "P8_Y5_R2FR_3913_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3913_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3913_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3913_VALIDATION.csv",
}

CURL_ID = "curl(delta H_tau)(delta_1,delta_2)=int_S i_tau omega_MTS(delta_1,delta_2)+int_partialS corner_tau(delta_1,delta_2)"
EH_CURL_ZERO = "on the EH local stationary source collar, L_tau Q=0 and variations preserve tau,Sigma,H_ref, so int_S i_tau omega_EH(delta_1,delta_2)=0"
EXTRA_FLUX_ZERO = "at Y_loc=H_priv=0 with S_int^{>=2} and source-silent variations, omega_Y+omega_H+omega_int has no linear source-collar flux"
REF_CORNER_ZERO = "q_src fixes R_ref=(tau,Sigma,H_ref), so reference and corner curl terms vanish for source-silent vertical variations"
RHTAU_ZERO = "R_Htau=0 for the EH/product/source-silent stationary collar"
PIM_HTAU_ZERO = "R_PiM+R_Htau=0 by 3912 R_PiM=0 plus 3913 R_Htau=0"
MEFF_ZERO = "B_Meff=0 if Ward conservation, q_src-fixed reference/support/frame/units, stationary side-flux silence, R_PiM=0 and R_Htau=0 all hold"
GDOT_AFTER = "Gdot_total <= 0 + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| on the stationary source-silent collar"


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
        ("SRC3913_00_next", SRC / "P8_Y5_R2FR_3912_NEXT_TARGET.csv", "NEXT3912_0", "3912 selected H_tau curl target"),
        ("SRC3913_01_3912_pim", SRC / "P8_Y5_R2FR_3912_MASS_FLAT_CONNECTION_BRANCH_GATE.csv", "MF3912_1_PiM_commutator", "3912 R_PiM zero theorem"),
        ("SRC3913_02_3912_reduce", SRC / "P8_Y5_R2FR_3912_MASS_FLAT_CONNECTION_BRANCH_GATE.csv", "MF3912_2_combined_reduction", "3912 combined reduction to R_Htau"),
        ("SRC3913_03_3912_qsrc", SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv", "BUN3912_0_source_quotient", "3912 q_src source quotient"),
        ("SRC3913_04_3912_vertical", SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv", "BUN3912_1_source_silent_vertical", "3912 source-silent vertical"),
        ("SRC3913_05_3911_curl", SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv", "CURL3911_0_covariant_phase_space_identity", "3911 curl identity"),
        ("SRC3913_06_3911_zero", SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv", "CURL3911_1_stationary_exact_flux_zero", "3911 stationary Htau zero condition"),
        ("SRC3913_07_2667_owner", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_1_theta_omega", "theta/omega owner gate"),
        ("SRC3913_08_2667_boundary", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_3_boundary_exact", "boundary exactness gate"),
        ("SRC3913_09_2667_verdict", SRC / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_7_verdict", "H_tau curl old verdict"),
        ("SRC3913_10_EH_glue", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_0_EH_reference_glue", "EH Noether/source collar reference glue"),
        ("SRC3913_11_MTS_transfer", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "MTS transfer condition"),
        ("SRC3913_12_normal_form", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_0_action", "3905 parent action normal form"),
        ("SRC3913_13_no_linear", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_2_interactions", "no linear extra-sector interactions"),
        ("SRC3913_14_boundary", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_3_boundary", "boundary/reference class"),
        ("SRC3913_15_GR", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_1_GR_equation", "conditional GR equation"),
        ("SRC3913_16_conservation", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_2_conservation", "visible matter conservation"),
        ("SRC3913_17_bridge", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert source bridge"),
        ("SRC3913_18_bianchi", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_3_Bianchi", "Bianchi consistency gate"),
        ("SRC3913_19_validation", SRC / "P8_Y5_BRR545_3912_VALIDATION.csv", "VAL3912_14_no_pycache", "3912 validation handoff"),
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


def curl_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HC3913_0_identity",
            "object": "H_tau curl",
            "formula": CURL_ID,
            "derivation_status": "COVARIANT_PHASE_SPACE_IDENTITY_RETAINED",
            "zero_condition": "surface symplectic flux plus corner/reference terms vanish",
            "source_path": str(SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HC3913_1_EH_stationary_flux",
            "object": "EH symplectic flux",
            "formula": EH_CURL_ZERO,
            "derivation_status": "CONDITIONAL_EH_STATIONARY_CURL_ZERO",
            "zero_condition": "EH local branch, stationary source collar, fixed tau/surface/reference, variations remain in stationary family",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HC3913_2_reference_corner",
            "object": "reference/corner curl",
            "formula": REF_CORNER_ZERO,
            "derivation_status": "DERIVED_FROM_QSRC_FIXED_REFERENCE",
            "zero_condition": "q_src adopted and source-silent vertical variations used",
            "source_path": str(SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HC3913_3_RHtau",
            "object": "R_Htau",
            "formula": RHTAU_ZERO,
            "derivation_status": "CONDITIONAL_RHTAU_ZERO_THEOREM",
            "zero_condition": "HC3913_1 plus HC3913_2 plus extra-sector flux silence",
            "source_path": str(SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def extra_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EXF3913_0_extra_flux",
            "sector": "Y_loc/H_priv/S_int",
            "formula": EXTRA_FLUX_ZERO,
            "derivation_status": "DERIVED_FROM_NORMAL_FORM_AT_BRANCH",
            "condition": "Y_loc=H_priv=0, no linear visible shadow/source-prefactor terms, source-silent variations",
            "source_path": str(SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EXF3913_1_nonEH_residual",
            "sector": "non-EH/topological residual",
            "formula": "non-EH residual flux must be topological, field-redefinition redundant, zero, or separately bounded",
            "derivation_status": "RESIDUAL_FILTER_RETAINED",
            "condition": "do not hide non-EH symplectic flux inside H_tau",
            "source_path": str(SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EXF3913_2_MTS_transfer",
            "sector": "MTS-to-EH charge transfer",
            "formula": "Q_MTS_tau = Q_EH_tau when Delta_nonEH=Delta_symp=Delta_extra=Delta_frame=Delta_PiM=0 on the source-silent collar",
            "derivation_status": "CONDITIONAL_TRANSFER_STACK",
            "condition": "requires the 3905/3906 EH branch and the 3912 R_PiM zero branch",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def meff_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MSC3913_0_PiM_Htau_core",
            "object": "Pi_M/H_tau core",
            "formula": PIM_HTAU_ZERO,
            "derivation_status": "CONDITIONAL_CORE_ZERO_STACK",
            "required_inputs": "3912 R_PiM zero; 3913 R_Htau zero",
            "claim_status": "PRIVATE_CONDITIONAL_BRANCH_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MSC3913_1_Ward",
            "object": "R_Ward",
            "formula": "R_Ward=0 when Diff_Q invariance and visible matter equations give nabla_mu T_vis^{mu nu}=0",
            "derivation_status": "CONDITIONAL_FROM_3905_CONSERVATION",
            "required_inputs": "same-frame Hilbert source bridge and constant kappa branch",
            "claim_status": "PRIVATE_CONDITIONAL_BRANCH_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MSC3913_2_reference_support_frame",
            "object": "R_ref+R_W+R_frame+R_units",
            "formula": "R_ref=R_W=R_frame=R_units=0 when q_src fixes tau,Sigma,H_ref,W_source and source units before readout",
            "derivation_status": "CONDITIONAL_FROM_3912_QSRC",
            "required_inputs": "source quotient adopted; no readout-domain mask; no orbital GM laundering",
            "claim_status": "PRIVATE_CONDITIONAL_BRANCH_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MSC3913_3_side_flux",
            "object": "R_side_flux",
            "formula": "R_side_flux=0 for compact stationary support and fixed linking surfaces in the exterior source-free annulus",
            "derivation_status": "CONDITIONAL_STATIONARY_COLLAR_ZERO",
            "required_inputs": "stationary compact source collar and no boundary/corner leak",
            "claim_status": "PRIVATE_CONDITIONAL_BRANCH_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MSC3913_4_BMeff",
            "object": "B_Meff",
            "formula": MEFF_ZERO,
            "derivation_status": "CONDITIONAL_MEFF_DRIFT_ZERO_STACK",
            "required_inputs": "MSC3913_0 through MSC3913_3",
            "claim_status": "NOT_PUBLIC_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MSC3913_5_Gdot_after",
            "object": "Gdot residual",
            "formula": GDOT_AFTER,
            "derivation_status": "REDUCED_GDOT_STACK",
            "required_inputs": "3909 Gstar zero plus 3913 B_Meff zero",
            "claim_status": "TOTAL_GDOT_STILL_BLOCKED_BY_REMAINING_READOUT_FACTORS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def remaining_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "REM3913_0_epsilon_mu",
            "remaining": "epsilon_mu",
            "meaning": "extra effective Poisson/source strength not contained in Hilbert mass",
            "why_not_closed": "requires separate residual silence or bound",
            "next_action": "assemble stationary local source stack and attack epsilon_mu first",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REM3913_1_Z_Poisson",
            "remaining": "Z_Poisson",
            "meaning": "weak-field 00/Poisson readout normalization",
            "why_not_closed": "requires source-normalized weak-field reduction with no non-EH operator leakage",
            "next_action": "verify against 3906 Poisson bridge and 3905 Newton limit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REM3913_2_Z_frame",
            "remaining": "Z_frame",
            "meaning": "same-frame clock/source/orbital readout mismatch",
            "why_not_closed": "requires exact observed-frame lock across clocks, source charge and metric readout",
            "next_action": "map to q_src/q_pub frame inheritance",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REM3913_3_parent_adoption",
            "remaining": "parent adoption",
            "meaning": "3904/3905/3912/3913 branches must be adopted by deeper MTS action",
            "why_not_closed": "currently a serious conditional branch, not a final parent derivation",
            "next_action": "state the branch contract and remaining empirical gates cleanly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3913_0_RHtau",
            "decision": "derive R_Htau=0 for the EH/product/source-silent stationary source collar",
            "claim_status": "CONDITIONAL_DERIVATION_NOT_PUBLIC_CLAIM",
            "reason": "EH stationary symplectic flux, q_src fixed reference/corner terms and extra-sector linear flux silence make the curl vanish",
            "next_action": "combine with 3912 R_PiM zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3913_1_BMeff",
            "decision": "conditionally close B_Meff=0 on the stationary source-silent collar",
            "claim_status": "MAJOR_INTERNAL_STACK_RESULT",
            "reason": "Pi_M/H_tau core, Ward conservation, reference/support/frame/unit locks and side flux all have conditional zero routes",
            "next_action": "do not overclaim; total Gdot/local-GR still needs epsilon_mu, Z_Poisson and Z_frame",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3913_2_selected_next",
            "decision": "next assemble the stationary local source-coupling stack and attack remaining readout factors",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "the source denominator core is now conditionally closed, so the remaining blockers are readout/Poisson/frame factors",
            "next_action": "3914-stationary-local-source-coupling-stack-or-readout-residual-map.md",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3913_0",
            "next_doc": "3914-Y5-R2FR-stationary-local-source-coupling-stack-or-readout-residual-map.md",
            "next_script": "scripts/Y5_R2FR_3914_stationary_local_source_coupling_stack_or_readout_residual_map.py",
            "target": "assemble the stationary local source-coupling theorem stack, show exactly what is closed, then attack epsilon_mu, Z_Poisson and Z_frame without claiming local GR yet",
            "why_this_next": "3913 conditionally closes B_Meff; the next honest move is to compress the remaining local-GR/Newton source-coupling blockers",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "R_Htau conditionally closed; Pi_M/H_tau core and B_Meff conditionally close on the stationary source-silent EH/product branch",
            "local_gr_claim": False,
            "gdot_claim": False,
            "new_forward_progress": "the source-denominator algebra is now a genuine conditional theorem stack rather than an unfilled coupling hole",
            "primary_blocker": "epsilon_mu, Z_Poisson, Z_frame and parent adoption",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3913 — Htau Exact Symplectic Curl from EH Source Collar or Bound

Timestamp: `{timestamp}`

## Result

This is the other half of the 3911/3912 source-denominator core.

Curl identity:
`{CURL_ID}`

EH stationary flux:
`{EH_CURL_ZERO}`

Extra-sector flux:
`{EXTRA_FLUX_ZERO}`

Reference/corner:
`{REF_CORNER_ZERO}`

Htau result:
`{RHTAU_ZERO}`

PiM/Htau core:
`{PIM_HTAU_ZERO}`

Stationary source-mass stack:
`{MEFF_ZERO}`

Gdot after this stack:
`{GDOT_AFTER}`

## Meaning

- `R_PiM` is closed by 3912 for source-silent q_src verticals.
- `R_Htau` is closed here for the EH/product/source-silent stationary source collar.
- Together, the PiM/Htau source-denominator core is conditionally zero.
- With Ward conservation, q_src-fixed reference/support/frame/units, and side-flux silence, `B_Meff=0` is also conditionally closed.
- This is still not a public local-GR claim: the remaining gates are `epsilon_mu`, `Z_Poisson`, `Z_frame`, and parent adoption of the branch.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['curl'])}`
- `{rel(OUTPUTS['extra'])}`
- `{rel(OUTPUTS['meff'])}`
- `{rel(OUTPUTS['remaining'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`3914-Y5-R2FR-stationary-local-source-coupling-stack-or-readout-residual-map.md`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3913 HTAU EXACT CURL SOURCE COLLAR -->
## 3913 Htau Exact Curl Source Collar

Timestamp: `{timestamp}`

EH stationary flux:
`{EH_CURL_ZERO}`

Extra-sector flux:
`{EXTRA_FLUX_ZERO}`

Reference/corner:
`{REF_CORNER_ZERO}`

Htau result:
`{RHTAU_ZERO}`

PiM/Htau core:
`{PIM_HTAU_ZERO}`

Stationary source-mass stack:
`{MEFF_ZERO}`

Gdot after this stack:
`{GDOT_AFTER}`

Decision: the source-denominator algebra conditionally closes on the EH/product/source-silent stationary collar. Remaining blockers are `epsilon_mu`, `Z_Poisson`, `Z_frame`, and parent adoption.
<!-- END 3913 HTAU EXACT CURL SOURCE COLLAR -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3913 HTAU EXACT CURL SOURCE COLLAR -->"
    end = "<!-- END 3913 HTAU EXACT CURL SOURCE COLLAR -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    extra: list[dict[str, Any]],
    meff: list[dict[str, Any]],
    remaining: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL3913_0_sources", "all cited source paths and needles resolve", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found"))
    checks.append(("VAL3913_1_EH_curl_zero", "EH stationary curl zero row emitted", any(EH_CURL_ZERO in row["formula"] for row in curl), rel(OUTPUTS["curl"])))
    checks.append(("VAL3913_2_extra_flux", "extra-sector flux silence row emitted", any(EXTRA_FLUX_ZERO in row["formula"] for row in extra), rel(OUTPUTS["extra"])))
    checks.append(("VAL3913_3_RHtau_zero", "R_Htau zero row emitted", any(RHTAU_ZERO in row["formula"] for row in curl), rel(OUTPUTS["curl"])))
    checks.append(("VAL3913_4_core_zero", "Pi_M/H_tau core zero row emitted", any(PIM_HTAU_ZERO in row["formula"] for row in meff), rel(OUTPUTS["meff"])))
    checks.append(("VAL3913_5_BMeff_zero", "B_Meff conditional zero stack emitted", any(MEFF_ZERO in row["formula"] for row in meff), rel(OUTPUTS["meff"])))
    checks.append(("VAL3913_6_remaining", "remaining readout factors listed", {"epsilon_mu", "Z_Poisson", "Z_frame"}.issubset({row["remaining"] for row in remaining}), rel(OUTPUTS["remaining"])))
    checks.append(("VAL3913_7_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in curl + extra + meff + remaining + decision), "valid_for_claim false across generated rows"))
    checks.append(("VAL3913_8_next_target", "next target is stationary source-coupling/readout map", "3914-Y5-R2FR-stationary-local-source" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3913_9_doc", "3913 markdown checkpoint written", DOC_PATH.exists() and "Htau Exact Symplectic Curl" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3913_10_spine", "spine updated with 3913 block", SPINE_PATH.exists() and "BEGIN 3913 HTAU EXACT CURL SOURCE COLLAR" in read_text(SPINE_PATH), rel(SPINE_PATH)))
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
    checks.append(("VAL3913_11_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3913*")) if FWB.exists() else []
    checks.append(("VAL3913_12_no_formalization_workbench_edits", "no 3913 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3913_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
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
    curl = curl_rows(timestamp)
    extra = extra_rows(timestamp)
    meff = meff_rows(timestamp)
    remaining = remaining_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["curl"], curl)
    write_csv(OUTPUTS["extra"], extra)
    write_csv(OUTPUTS["meff"], meff)
    write_csv(OUTPUTS["remaining"], remaining)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, curl, extra, meff, remaining, decision, timestamp)
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
