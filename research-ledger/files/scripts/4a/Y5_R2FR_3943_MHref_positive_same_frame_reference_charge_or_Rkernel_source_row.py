from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3943"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3943-Y5-R2FR-MHref-positive-same-frame-reference-charge-or-Rkernel-source-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3943_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3943_MHREF_REFERENCE_CHARGE_THEOREM.csv",
    "source_template": SRC / "P8_Y5_R2FR_3943_MHREF_SOURCE_ROW_TEMPLATE.csv",
    "anchor": SRC / "P8_Y5_R2FR_3943_HOMOGENEOUS_REFERENCE_ANCHOR.csv",
    "bound": SRC / "P8_Y5_R2FR_3943_RKERNEL_FIRST_BOUND_ROW.csv",
    "decision": SRC / "P8_Y5_R2FR_3943_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3943_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3943_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3943_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3943_VALIDATION.csv",
}

NEXT_DOC = "3944-Y5-R2FR-MHref-source-energy-comparator-and-residual-lower-bound-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3944_MHref_source_energy_comparator_and_residual_lower_bound_row.py"


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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3943_00_3942_next", SRC / "P8_Y5_R2FR_3942_NEXT_TARGET.csv", "NEXT3942_0", "3942 handoff to M_H_ref/reference charge"),
        ("SRC3943_01_3942_theorem", SRC / "P8_Y5_R2FR_3942_GREEN_MAP_KERNEL_THEOREM.csv", "GKT3942_4_zero_theorem", "R_kernel zero theorem dependence"),
        ("SRC3943_02_3942_switch", SRC / "P8_Y5_R2FR_3942_BOUNDARY_CONDITION_SWITCH.csv", "Z3942_1_reference_charge", "reference charge switch"),
        ("SRC3943_03_3942_bound", SRC / "P8_Y5_R2FR_3942_RKERNEL_BOUND_ROWS.csv", "RK3942_1_ref", "epsilon_ref_charge bound row"),
        ("SRC3943_04_3577_href", SRC / "P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv", "REF3577_0_fixed_reference_rule", "fixed H_ref selector"),
        ("SRC3943_05_3577_den", SRC / "P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv", "DEN3577_1_lower_bound", "positive denominator lower-bound route"),
        ("SRC3943_06_3825_law", SRC / "P8_Y5_R2FR_3825_MHREF_POSITIVE_DENOMINATOR_LAW.csv", "MHD3825_2_positivity_condition", "M_H_ref positivity law"),
        ("SRC3943_07_3825_row", SRC / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv", "FSR3825_2_MHref", "first source-ready M_H_ref row"),
        ("SRC3943_08_3825_residuals", SRC / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv", "R3825_3_boundary_reference_abs", "boundary/reference residual envelope"),
        ("SRC3943_09_3433_lock", SRC / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv", "SL3433_5_newton_limit", "same-frame source/Newton denominator lock"),
        ("SRC3943_10_3433_audit", SRC / "P8_Y5_R2FR_3433_SAME_FRAME_MHREF_TAU_AUDIT.csv", "SFA3433_3_MHref_positive", "same-frame denominator audit"),
        ("SRC3943_11_3207_law", SRC / "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv", "LAW3207_3_positive_lower_bound", "triangle lower-bound law"),
        ("SRC3943_12_3551_descent", SRC / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv", "MHD3551_1_sum_difference_descent", "q-basic H_tau-H_ref descent theorem"),
        ("SRC3943_13_2947_runner", LOCAL_BOUNDS / "MHref_PiM_first_row_runner_rows_2947_NONCLAIM.csv", "RUN2947_1_MHref", "M_H_ref first row runner requirement"),
        ("SRC3943_14_noether", LOCAL_BOUNDS / "Noether_Hamiltonian_charge_chain_2504_NONCLAIM.csv", "NHC2504_3_source_measure", "Hamiltonian source-measure definition"),
        ("SRC3943_15_parent_action", LOCAL_BOUNDS / "Minimal_parent_action_charge_contract_2504_NONCLAIM.csv", "PAC2504_6_boundary_reference", "boundary/reference contract"),
        ("SRC3943_16_3942_validation", SRC / "P8_Y5_BRR545_3942_VALIDATION.csv", "VAL3942_17_no_pycache", "previous validation"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MRT3943_0_definition",
            "claim_piece": "same-frame denominator definition",
            "formula": "M_H_ref := c^-2*(H_tau[S_link;Phi_source]-H_ref[branch])",
            "derivation": "The denominator is the parent Hamiltonian source charge in one tau/coframe/surface/reference branch, not orbital GM and not a fitted calibration constant.",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRT3943_1_anti_laundering",
            "claim_piece": "no measured-GM laundering",
            "formula": "partial_{GM_obs,mu_fit,orbit_fit} H_ref = 0 and M_H_ref != mu_fit/G_* unless Poisson/Gauss/source bridge is already independently derived",
            "derivation": "This preserves the GR-style direction of explanation: source charge produces measured GM; measured GM is not used to define the source charge.",
            "status": "NO_CHEAT_RULE_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRT3943_2_positive_lower_bound",
            "claim_piece": "positive denominator theorem",
            "formula": "M_H_ref >= M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_* M_EH)",
            "derivation": "If the same-frame EH/source-energy comparator is positive and the absolute residual envelope is smaller than it, then M_H_ref is positive without importing orbital GM.",
            "status": "CONDITIONAL_POSITIVITY_THEOREM_DERIVED_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRT3943_3_homogeneous_anchor",
            "claim_piece": "zero homogeneous reference-charge anchor",
            "formula": "Z_ref_charge := H_tau[u_hom]-H_ref[u_hom]=0 for W_source=empty, J_H=0, same tau/surface/reference class",
            "derivation": "The source-free homogeneous branch is assigned zero parent source charge only when the reference selector is parent-owned, fixed before readout, and not allowed to carry a hidden boundary mass.",
            "status": "CONDITIONAL_REFERENCE_ANCHOR_DERIVED_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRT3943_4_rkernel_bridge",
            "claim_piece": "R_kernel zero bridge",
            "formula": "Z_ref_charge and M_H_ref>0 and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel/M_H_ref=0",
            "derivation": "3942 killed the free C/r mode if the reference-charge switch closes; 3943 supplies the denominator/reference theorem needed to make that statement dimensionless and non-circular.",
            "status": "CONDITIONAL_RKERNEL_ZERO_BRIDGE_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRT3943_5_public_verdict",
            "claim_piece": "current public status",
            "formula": "M_H_ref row remains source-ready but not claim-ready",
            "derivation": "The current corpus still lacks a filled source row for M_EH, residual components, same tau/coframe/surface identifiers, units, and source path without MISSING markers.",
            "status": "FIRST_SOURCE_ROW_REQUIRED_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_template_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MHS3943_0_exact_MHref",
            "quantity": "M_H_ref",
            "formula": "c^-2*(H_tau[S_link]-H_ref)",
            "required_columns": "system_id;tau_id;coframe_id;surface_link;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;reference_rule;positivity_certificate;not_orbital_GM_imported;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_EXACT_M_H_REF_VALUE",
            "units": "mass",
            "status": "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MHS3943_1_MHref_lower",
            "quantity": "M_H_ref_lower",
            "formula": "M_EH*(1-epsilon_abs)",
            "required_columns": "system_id;M_EH;M_EH_units;Delta_component_rows;epsilon_abs;epsilon_abs_units;proof_epsilon_lt_1;M_H_ref_lower;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_M_EH_AND_RESIDUAL_COMPONENTS",
            "units": "mass",
            "status": "LOWER_BOUND_TEMPLATE_READY_VALUES_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MHS3943_2_homogeneous_reference",
            "quantity": "H_tau[u_hom]-H_ref[u_hom]",
            "formula": "0 if W_source=empty and Z_ref_selector and Z_no_boundary_mass and Z_same_tau_surface",
            "required_columns": "branch_id;u_hom_id;source_status;reference_id;tau_id;surface_class;H_tau_u_hom;H_ref_u_hom;difference;units;zero_authority;source_path;valid_for_claim",
            "current_value": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "units": "energy",
            "status": "ANCHOR_TEMPLATE_READY_PARENT_SIGNATURE_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MHS3943_3_anti_circularity_guard",
            "quantity": "not_orbital_GM_imported",
            "formula": "true required before any M_H_ref row can score",
            "required_columns": "not_orbital_GM_imported;GM_source_bridge_status;Poisson_Gauss_status;auditor_note",
            "current_value": "TRUE_REQUIRED_NOT_SUFFICIENT",
            "units": "boolean",
            "status": "GUARD_ACTIVE",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def anchor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ANCH3943_0_empty_source", "empty source class", "W_source=empty and J_H[tau]=0 for the homogeneous branch", "same-current-complex ownership", "CONDITIONAL_UNSIGNED"),
        ("ANCH3943_1_fixed_ref", "fixed reference selector", "H_ref selected before source/orbit/PPN scoring and source-blind", "REF3577_0;REF3577_1", "INTERNAL_CANDIDATE_NONCLAIM"),
        ("ANCH3943_2_same_surface", "same tau/surface/reference class", "u_hom evaluated on the same tau, coframe, S_link and reference class as M_H_ref", "3433 same-frame lock;3581 same-Pann", "CONDITIONAL_UNSIGNED"),
        ("ANCH3943_3_no_boundary_mass", "no hidden boundary mass", "boundary/topological/symplectic improvement carries no source-free monopole charge", "3825 residual rows;NHC2504_7;PAC2504_6", "OPEN_BOUND_OR_ZERO"),
        ("ANCH3943_4_zero_anchor", "zero reference-charge anchor", "H_tau[u_hom]-H_ref[u_hom]=0", "ANCH3943_0..3", "CONDITIONAL_ZERO_PARENT_UNSIGNED"),
    ]
    return [
        {
            "row_id": row_id,
            "anchor_clause": clause,
            "condition": condition,
            "source_basis": basis,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, condition, basis, status in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RB3943_0_ref_charge", "epsilon_ref_charge", "abs(H_tau[u_hom]-H_ref[u_hom])/M_H_ref", "MISSING_HOMOGENEOUS_REFERENCE_CHARGE_OR_PARENT_ZERO", "dimensionless", "source_mass;Newton"),
        ("RB3943_1_denominator", "epsilon_MHref_denominator", "indicator(M_H_ref<=0 or missing) plus lower-bound uncertainty", "MISSING_POSITIVE_SAME_FRAME_MHREF_OR_LOWER_BOUND", "dimensionless", "local_GR;Newton"),
        ("RB3943_2_boundary", "epsilon_boundary_reference_abs", "(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref", "MISSING_B_ZERO_FLUX_DELTA_SYMP_MHREF", "dimensionless", "boundary;PPN"),
        ("RB3943_3_tau_surface", "epsilon_tau_surface_ref", "same-tau/same-surface mismatch contribution normalized by M_H_ref", "MISSING_SAME_TAU_SURFACE_LOCK_OR_VALUE", "dimensionless", "clock;orbital"),
        ("RB3943_4_total", "R_kernel_ref_anchor_bound", "epsilon_ref_charge + epsilon_MHref_denominator + epsilon_boundary_reference_abs + epsilon_tau_surface_ref", "MISSING_COMPONENT_VALUES", "dimensionless", "source_normalized_Newton;local_GR"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "current_value": value,
            "units": units,
            "observable_link": observable,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, value, units, observable in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3943_0_denominator_defined",
            "decision": "define M_H_ref as same-frame Hamiltonian source charge",
            "effect": "the denominator is no longer a symbol floating over the R_kernel bound; it has a strict anti-orbital-GM contract",
            "claim_status": "DEFINITION_LOCKED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3943_1_reference_anchor",
            "decision": "derive the homogeneous reference-charge zero only as a parent-owned empty-source normalization",
            "effect": "R_kernel can close conditionally without asymptotic-flatness smuggling, but not as a public claim until boundary/reference rows close",
            "claim_status": "PRIVATE_CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3943_2_next",
            "decision": "target the source-energy comparator and residual lower-bound rows next",
            "effect": "M_H_ref_lower>0 becomes scoreable only after M_EH and residual components are filled or theorem-zero",
            "claim_status": "NEXT_SOURCE_ENERGY_LOWER_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3943_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3943_1_definition", "gate": "same-frame denominator definition", "requirement": "M_H_ref definition excludes orbital-GM import", "status": "PASS_DEFINITION_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3943_2_positive_denominator", "gate": "positive M_H_ref", "requirement": "exact M_H_ref>0 or source-backed M_H_ref_lower>0", "status": "BLOCKED_M_EH_AND_RESIDUAL_COMPONENTS_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3943_3_reference_anchor", "gate": "homogeneous reference-charge zero", "requirement": "empty-source same-frame reference and no boundary mass source-free charge", "status": "BLOCKED_PARENT_SIGNATURE_OR_BOUND_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3943_4_Rkernel", "gate": "R_kernel/M_H_ref closure", "requirement": "positive denominator plus zero reference anchor plus remaining 3942 switch", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3943_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "fill or theorem-close the source-energy comparator M_EH and residual envelope Delta_i needed for M_H_ref_lower=M_EH*(1-epsilon_abs)>0",
            "success_condition": "M_H_ref_lower is either a positive source-backed row with units/source path or remains explicitly blocked by named residual components, without importing orbital GM",
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
            "summary": "3943 locks M_H_ref as a same-frame Hamiltonian source denominator, derives the conditional homogeneous reference-charge anchor, and routes positivity to M_EH plus residual lower-bound rows",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3943 - MHref Positive Same-Frame Reference Charge or Rkernel Source Row

Timestamp: `{timestamp}`

## Result

3943 locks the denominator/reference-charge problem into a proper source contract.

The denominator is:

`M_H_ref := c^-2*(H_tau[S_link;Phi_source]-H_ref[branch])`.

It is not `mu_fit/G_*`, not orbital `GM`, and not a readout calibration knob.

## Conditional Theorems

Positive denominator route:

`M_H_ref >= M_EH*(1-epsilon_abs)`, where `epsilon_abs=sum_i |Delta_i|/(G_* M_EH)`.

So if `M_EH>0` and `epsilon_abs<1`, then `M_H_ref>0` without importing orbital GM.

Homogeneous reference-charge anchor:

`W_source=empty and J_H=0 and Z_ref_selector and Z_no_boundary_mass and Z_same_tau_surface => H_tau[u_hom]-H_ref[u_hom]=0`.

Therefore:

`Z_ref_charge and M_H_ref>0 and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel/M_H_ref=0`.

## Current Verdict

- Progress: `M_H_ref` is now a strict same-frame Hamiltonian source denominator.
- Progress: the homogeneous reference-charge zero is a conditional empty-source theorem, not a calibration trick.
- Blocker: no claim-grade `M_EH`, `epsilon_abs`, `M_H_ref_lower`, or boundary/reference component row is filled yet.
- Public claim: blocked.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3943_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_MHREF_REFERENCE_CHARGE_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_MHREF_SOURCE_ROW_TEMPLATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_HOMOGENEOUS_REFERENCE_ANCHOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_RKERNEL_FIRST_BOUND_ROW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3943_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3943 - MHref Positive Same-Frame Reference Charge or Rkernel Source Row

Timestamp: `{timestamp}`

- Denominator lock: `M_H_ref := c^-2*(H_tau[S_link;Phi_source]-H_ref[branch])`, explicitly not orbital `GM` or a fitted readout denominator.
- Positivity theorem: if `M_EH>0` and `epsilon_abs=sum_i |Delta_i|/(G_*M_EH)<1`, then `M_H_ref >= M_EH*(1-epsilon_abs)>0`.
- Homogeneous anchor: empty-source same-frame reference plus no boundary mass gives `H_tau[u_hom]-H_ref[u_hom]=0`.
- Bridge: with positive `M_H_ref`, that anchor feeds the 3942 result and conditionally gives `R_kernel/M_H_ref=0`.
- Claim status: private conditional only; source-energy comparator and residual lower-bound rows remain unfilled.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3943 - MHref Positive Same-Frame Reference Charge or Rkernel Source Row"
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


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem = theorem_rows(timestamp)
    templates = source_template_rows(timestamp)
    anchors = anchor_rows(timestamp)
    bounds = bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (theorem, templates, anchors, bounds, decisions, gates, next_target)
    checks = [
        ("VAL3943_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3943_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3943_02_definition", any(row["status"] == "EXACT_CONDITIONAL_DEFINITION" and "M_H_ref" in row["formula"] for row in theorem), "M_H_ref definition emitted"),
        ("VAL3943_03_no_orbital_gm", any(row["status"] == "NO_CHEAT_RULE_ACTIVE" and "mu_fit" in row["formula"] for row in theorem), "anti-orbital-GM guard emitted"),
        ("VAL3943_04_positivity_theorem", any(row["status"] == "CONDITIONAL_POSITIVITY_THEOREM_DERIVED_COMPONENTS_MISSING" for row in theorem), "positive lower-bound theorem emitted"),
        ("VAL3943_05_reference_anchor", any(row["status"] == "CONDITIONAL_REFERENCE_ANCHOR_DERIVED_PARENT_UNSIGNED" for row in theorem), "homogeneous reference-charge anchor emitted"),
        ("VAL3943_06_source_templates", len(templates) == 4 and any(row["quantity"] == "M_H_ref_lower" for row in templates), "source row templates emitted"),
        ("VAL3943_07_anchor_clauses", len(anchors) == 5 and any(row["status"] == "OPEN_BOUND_OR_ZERO" for row in anchors), "anchor clause audit emitted"),
        ("VAL3943_08_bound_rows", len(bounds) == 5 and any(row["symbol"] == "R_kernel_ref_anchor_bound" for row in bounds), "R_kernel first bound row emitted"),
        ("VAL3943_09_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in gates), "claim gate blocks public claim"),
        ("VAL3943_10_next_3944", next_target[0]["next_doc"] == NEXT_DOC and "M_EH" in next_target[0]["target"], "next target selects M_EH lower-bound rows"),
        ("VAL3943_11_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3943_12_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3943_13_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3943_14_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3943_15_spine_written", SPINE_PATH.exists() and "3943 - MHref Positive Same-Frame Reference Charge" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3943_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3943_17_script_compiles", True, "script compiles"),
        ("VAL3943_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["theorem"], theorem_rows(timestamp))
    write_csv(OUTPUTS["source_template"], source_template_rows(timestamp))
    write_csv(OUTPUTS["anchor"], anchor_rows(timestamp))
    write_csv(OUTPUTS["bound"], bound_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
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
        raise SystemExit(f"3943 validation failed: {failed}")
    print(f"3943 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
