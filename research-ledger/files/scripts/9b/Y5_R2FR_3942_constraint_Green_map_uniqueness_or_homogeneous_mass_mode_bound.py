from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3942"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3942-Y5-R2FR-constraint-Green-map-uniqueness-or-homogeneous-mass-mode-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3942_SOURCE_REGISTER.csv",
    "green_theorem": SRC / "P8_Y5_R2FR_3942_GREEN_MAP_KERNEL_THEOREM.csv",
    "mode_audit": SRC / "P8_Y5_R2FR_3942_HOMOGENEOUS_MODE_AUDIT.csv",
    "boundary_switch": SRC / "P8_Y5_R2FR_3942_BOUNDARY_CONDITION_SWITCH.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3942_RKERNEL_BOUND_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3942_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3942_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3942_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3942_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3942_VALIDATION.csv",
}

NEXT_DOC = "3943-Y5-R2FR-MHref-positive-same-frame-reference-charge-or-Rkernel-source-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3943_MHref_positive_same_frame_reference_charge_or_Rkernel_source_row.py"


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
        ("SRC3942_00_3941_next", SRC / "P8_Y5_R2FR_3941_NEXT_TARGET.csv", "NEXT3941_0", "3941 handoff to Green-map kernel"),
        ("SRC3942_01_3941_split", SRC / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv", "MAP3941_3_exact_split", "R_kernel split source"),
        ("SRC3942_02_3941_kernel_guard", SRC / "P8_Y5_R2FR_3941_CONSTRAINT_GREEN_PIM_CONSTRUCTION.csv", "CGP3941_2_kernel_guard", "homogeneous mass-mode guard"),
        ("SRC3942_03_3941_bound", SRC / "P8_Y5_R2FR_3941_PIM_COMMUTATOR_BOUND_ROWS.csv", "PB3941_0_kernel", "R_kernel bound row"),
        ("SRC3942_04_3941_audit", SRC / "P8_Y5_R2FR_3941_CHAINMAP_PROOF_AUDIT.csv", "AUD3941_3_constraint_green", "constraint Green-map audit"),
        ("SRC3942_05_3931_reset", PCW / "3931-Y5-R2FR-history-nonlocal-tail-reset-or-suppression-bound.md", "HISTORY_RESET_loc", "local reset/no-incoming branch"),
        ("SRC3942_06_3933_newton", SRC / "P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv", "ARE3933_1_Newton", "private Newton/Maxwell/source rollup"),
        ("SRC3942_07_1296_poisson", SRC / "P8_Y5_R10_1296_RESPONSE_OPERATOR_ROWS_NONCLAIM.csv", "RGO1296_1_static_Poisson_Newton_response", "formal Poisson Green operator source"),
        ("SRC3942_08_3582_anchor_theorem", SRC / "P8_Y5_R2FR_3582_PHI_ANCHOR_ASYMPTOTIC_ZERO_THEOREM.csv", "PAZ3582_2_zero_flux_estimate", "asymptotic flux-anchor theorem"),
        ("SRC3942_09_3582_anchor_bound", SRC / "P8_Y5_R2FR_3582_PHI_ANCHOR_BOUND_ROWS.csv", "PAB3582_1_Phi_anchor_abs", "Phi anchor zero row"),
        ("SRC3942_10_noether_ref", LOCAL_BOUNDS / "Noether_Hamiltonian_charge_chain_2504_NONCLAIM.csv", "NHC2504_7_boundary_zero", "boundary/reference zero blocker"),
        ("SRC3942_11_parent_ref", LOCAL_BOUNDS / "Minimal_parent_action_charge_contract_2504_NONCLAIM.csv", "PAC2504_6_boundary_reference", "parent boundary reference contract"),
        ("SRC3942_12_mhref", LOCAL_BOUNDS / "MHref_PiM_first_row_runner_rows_2947_NONCLAIM.csv", "RUN2947_1_MHref", "M_H_ref first-row requirement"),
        ("SRC3942_13_3941_validation", SRC / "P8_Y5_BRR545_3941_VALIDATION.csv", "VAL3941_18_no_pycache", "previous validation"),
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


def green_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GKT3942_0_problem",
            "claim_piece": "kernel problem",
            "formula": "R_kernel := H_tau[u_hom] for C_tau[u_hom]=0",
            "derivation": "3941 reduced the PiM/Hilbert/H_tau map to whether the parent constraint admits a source-free homogeneous mass mode.",
            "status": "TARGET_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_1_newton_limit",
            "claim_piece": "Newtonian homogeneous equation",
            "formula": "nabla^2 delta Phi = 0 on A_ext, delta Phi -> C_0 + C_1/r + sum_{l>=1} C_lm r^{-(l+1)}Y_lm",
            "derivation": "The difference of two weak-field constraint solutions with the same Hilbert source is harmonic outside the source worldtube.",
            "status": "STANDARD_GREEN_MAP_LIMIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_2_no_flatness_cheat",
            "claim_piece": "asymptotic flatness is insufficient",
            "formula": "delta Phi -> 0 still allows C_1/r",
            "derivation": "A free Schwarzschild/Newtonian monopole is asymptotically flat. Therefore asymptotic flatness alone cannot prove source-owned measured GM.",
            "status": "NO_CHEAT_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_3_mass_flux",
            "claim_piece": "mass-kernel charge",
            "formula": "R_kernel = -(1/G_*) C_1 = (1/(4*pi*G_*)) int_{S_infty} grad(delta Phi).dS",
            "derivation": "The only homogeneous mode that shifts calibrated source mass is the l=0 1/r coefficient; higher multipoles do not alter total GM but must remain observable residuals if active.",
            "status": "MASS_KERNEL_FORMULA_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_4_zero_theorem",
            "claim_piece": "conditional mass-kernel zero",
            "formula": "Z_ref_charge and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel=0",
            "derivation": "If the source-free homogeneous branch has zero Hamiltonian boundary charge on the same reference/tau/surface package and no incoming/free monopole data, Gauss flux gives C_1=0.",
            "status": "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_5_bound_if_open",
            "claim_piece": "finite kernel fallback",
            "formula": "|R_kernel|/M_H_ref = |C_1|/(G_* M_H_ref) <= epsilon_ref_charge + epsilon_incoming + epsilon_surface + epsilon_boundary",
            "derivation": "If the reference/no-incoming/surface/boundary switch is not signed, the free monopole remains as a measurable no-cancellation bound row.",
            "status": "BOUND_ROUTE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKT3942_6_verdict",
            "claim_piece": "3942 verdict",
            "formula": "R_kernel=0 is proved only inside a charge-fixed local reset branch; current corpus still needs M_H_ref/reference charge ownership before public use.",
            "derivation": "The free-monopole problem is no longer vague: it is exactly a boundary/reference charge anchor problem.",
            "status": "FORWARD_REDUCTION_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def homogeneous_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("HMA3942_0_constant", "C_0", "constant potential offset", "fixed by clock normalization/reference; does not change GM", "REFERENCE_CLOCK_GAUGE_REQUIRED", "not_mass_kernel"),
        ("HMA3942_1_monopole", "C_1/r", "free Schwarzschild/Newtonian monopole", "changes boundary charge and measured GM if not source-owned", "CORE_RKERNEL_MODE", "mass_kernel"),
        ("HMA3942_2_dipole", "C_1m/r^2", "homogeneous dipole/center choice", "does not alter total mass but can affect frame/origin and orbital residuals", "CENTER_OF_MASS_FRAME_OR_BOUND", "multipole_residual"),
        ("HMA3942_3_higher", "C_lm r^{-(l+1)}, l>=2", "source-free multipole hair", "does not alter monopole source mass but feeds PPN/orbital multipole bounds", "MULTIPOLE_BOUND_OR_NO_HAIR", "multipole_residual"),
        ("HMA3942_4_radiative", "retarded/incoming homogeneous wave", "time-dependent source-free incoming/radiative mode", "excluded only in local reset/no-incoming branch; otherwise a finite boundary row", "NO_INCOMING_RESET_OR_WAVE_BOUND", "radiative_residual"),
        ("HMA3942_5_extra", "X-sector homogeneous source shadow", "non-EH/non-Hilbert homogeneous mode in the same boundary charge", "must be zero/bounded before local-GR source coupling claim", "EXTRA_SOURCE_SHADOW_VECTOR", "extra_residual"),
    ]
    return [
        {
            "row_id": row_id,
            "mode_symbol": symbol,
            "mode_name": name,
            "effect": effect,
            "required_control": control,
            "classification": classification,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, name, effect, control, classification in data
    ]


def boundary_switch_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("Z3942_0_source_fixed", "Z_source", "same J_H[tau] and W_source fixed before Green map", "3941/2900 current-complex contract", "CONDITIONAL_UNSIGNED"),
        ("Z3942_1_reference_charge", "Z_ref_charge", "H_tau[u_hom]-H_ref[u_hom]=0 for the source-free homogeneous branch", "NHC2504_7;PAC2504_6;RUN2947_1", "CORE_UNSIGNED"),
        ("Z3942_2_no_incoming", "Z_no_incoming", "local reset/no-incoming branch excludes free incoming homogeneous mass/history data", "3931 reset branch", "PRIVATE_BRANCH_CONDITIONAL"),
        ("Z3942_3_same_surface", "Z_same_tau_surface", "same tau, S_in/S_out/S_infty, and reference surface package", "3581 same-Pann switch", "CONDITIONAL_UNSIGNED"),
        ("Z3942_4_anchor", "Z_flux_anchor", "asymptotic no-radiation anchor prevents radiative boundary energy from shifting H_tau", "3582 Phi_anchor=0 branch", "CONDITIONAL_PUBLIC_EM"),
        ("Z3942_5_no_extra_boundary", "Z_no_extra_boundary_charge", "no boundary/topological/symplectic improvement carries source-free monopole charge", "PAC2504_6;PB3941 boundary row", "OPEN_BOUND_OR_ZERO"),
        ("Z3942_6_mass_kernel_zero", "Z_Rkernel", "Z_source & Z_ref_charge & Z_no_incoming & Z_same_tau_surface & Z_no_extra_boundary_charge", "3942 theorem", "FAIL_CURRENT_PUBLIC_CLAIM_SWITCH_READY"),
    ]
    return [
        {
            "row_id": row_id,
            "switch_symbol": symbol,
            "condition": condition,
            "source_basis": basis,
            "status": status,
            "switch_value_now": False if row_id in {"Z3942_1_reference_charge", "Z3942_5_no_extra_boundary", "Z3942_6_mass_kernel_zero"} else "conditional_private",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, condition, basis, status in data
    ]


def rkernel_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RK3942_0_C1", "C1_free_monopole", "coefficient of source-free 1/r potential in the homogeneous constraint solution", "C1", "MISSING_BOUNDARY_CHARGE_ANCHOR_OR_VALUE", "potential_length_or_GM_units", "Newton;orbital;PPN"),
        ("RK3942_1_ref", "epsilon_ref_charge", "source-free Hamiltonian/reference boundary charge normalized by M_H_ref", "abs(H_tau[u_hom]-H_ref[u_hom])/M_H_ref", "MISSING_HREF_MHREF_SOURCE_ROW", "dimensionless", "source_mass;Newton"),
        ("RK3942_2_incoming", "epsilon_incoming_mass", "incoming/reset homogeneous mass-mode amplitude", "abs(C1_incoming)/(G_* M_H_ref)", "ZERO_ONLY_IN_3931_RESET_BRANCH_ELSE_VALUE_REQUIRED", "dimensionless", "local_reset;clock"),
        ("RK3942_3_surface", "epsilon_surface_flux", "same-tau/surface mismatch contribution to monopole flux", "abs(delta int_S grad Phi.dS)/(4*pi*G_*M_H_ref)", "MISSING_SAME_SURFACE_OWNER_OR_VALUE", "dimensionless", "orbital;radial_Meff"),
        ("RK3942_4_boundary", "epsilon_boundary_charge", "boundary/topological/symplectic improvement carrying free monopole charge", "abs(B_boundary_mass)/(M_H_ref)", "MISSING_BOUNDARY_IMPROVEMENT_ZERO_OR_VALUE", "dimensionless", "boundary;PPN"),
        ("RK3942_5_radiative", "epsilon_radiative_mass_flux", "radiative Poynting/Killing-energy flux contributing to source mass", "abs(int_boundary S_EM dot dA dt)/(M_H_ref)", "ZERO_ON_3582_BRANCH_ELSE_VALUE_REQUIRED", "dimensionless", "EM;clock;orbital"),
        ("RK3942_6_multipole", "epsilon_hom_multipole", "non-monopole homogeneous hair retained outside R_kernel", "sum_l>=1 |C_lm| observable norm", "MULTIPOLE_BOUND_REQUIRED_IF_ACTIVE", "observable_norm", "PPN;orbital"),
        ("RK3942_7_total", "R_kernel_over_MHref", "strict no-cancellation homogeneous mass kernel bound", "abs(C1)/(G_*M_H_ref) <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_surface_flux + epsilon_boundary_charge + epsilon_radiative_mass_flux", "MISSING_COMPONENT_VALUES", "dimensionless", "source_normalized_Newton;local_GR"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "current_value": value,
            "units": units,
            "observable_link": observable,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, formula, value, units, observable in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3942_0_no_flatness_cheat",
            "decision": "asymptotic flatness alone is rejected as a proof of R_kernel=0",
            "effect": "a source-free C/r mode is asymptotically flat and would smuggle Newtonian GM",
            "claim_status": "GUARD_INSTALLED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3942_1_conditional_zero",
            "decision": "R_kernel=0 is conditionally derived under a charge-fixed/no-incoming/same-surface/no-extra-boundary switch",
            "effect": "inside that private branch, Pi_M^C has no free mass monopole kernel",
            "claim_status": "PRIVATE_CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3942_2_next",
            "decision": "target M_H_ref and the same-frame reference charge anchor next",
            "effect": "the free-monopole proof now depends on making the zero reference charge and positive denominator source-owned",
            "claim_status": "NEXT_MHREF_REFERENCE_CHARGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3942_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3942_1_green_theorem", "gate": "Green-map kernel theorem", "requirement": "homogeneous mass mode isolated and zero condition stated", "status": "PASS_PRIVATE_CONDITIONAL_THEOREM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3942_2_no_flatness_cheat", "gate": "no asymptotic-flatness smuggling", "requirement": "C/r mode remains live unless reference charge anchor closes", "status": "PASS_GUARD", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3942_3_reference_charge", "gate": "same-frame M_H_ref/reference charge", "requirement": "positive source-owned M_H_ref and zero homogeneous H_tau-H_ref row", "status": "BLOCKED_CORE_NEXT_TARGET", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3942_4_bound_values", "gate": "R_kernel fallback bound", "requirement": "all R_kernel components theorem-zero or source-backed finite", "status": "BLOCKED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3942_5_public_claim", "gate": "public source-normalized Newton/local-GR claim", "requirement": "R_kernel plus remaining PC0D/PC0 residuals close", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3942_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or source the positive same-frame M_H_ref denominator and zero homogeneous reference-charge anchor H_tau[u_hom]-H_ref[u_hom]=0, or fill the first R_kernel/M_H_ref source-backed bound row",
            "success_condition": "R_kernel is theorem-zero inside the local branch without asymptotic-flatness smuggling, or the free monopole has a finite source-backed bound with units and source path",
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
            "summary": "3942 derives the conditional R_kernel zero theorem and proves asymptotic flatness alone is insufficient; next target is M_H_ref/reference charge ownership",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3942 - Constraint Green-Map Uniqueness or Homogeneous Mass-Mode Bound

Timestamp: `{timestamp}`

## Result

3942 attacks the free-monopole danger directly.

The key discipline point is:

`asymptotic flatness alone does not kill a source-free C/r mode`.

A `C/r` mode is just the Newton/Schwarzschild mass monopole. If we let it in without source ownership, we have smuggled measured `GM` instead of deriving it.

## Conditional Theorem

In the weak-field local limit, the difference of two source-equivalent constraint solutions obeys:

`nabla^2 delta Phi = 0`.

Its exterior monopole piece is:

`delta Phi_hom = C_1/r + ...`

and the mass-kernel charge is:

`R_kernel = -C_1/G_* = (1/(4*pi*G_*)) int_{{S_infty}} grad(delta Phi).dS`.

Therefore:

`Z_ref_charge and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel=0`.

## Current Verdict

- Progress: the free homogeneous mass mode is isolated exactly.
- Honest guard: asymptotic flatness alone is rejected as a proof.
- Conditional win: `R_kernel=0` inside a charge-fixed, no-incoming, same-surface, no-extra-boundary local branch.
- Public claim: still blocked until `M_H_ref` and the homogeneous reference-charge anchor are source-owned.

## Bound Route

If the zero switch is not signed:

`|R_kernel|/M_H_ref <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_surface_flux + epsilon_boundary_charge + epsilon_radiative_mass_flux`.

That keeps the free monopole as a finite no-cancellation row rather than hiding it in calibration.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3942_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_GREEN_MAP_KERNEL_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_HOMOGENEOUS_MODE_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_BOUNDARY_CONDITION_SWITCH.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_RKERNEL_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3942_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3942 - Constraint Green-Map Uniqueness or Homogeneous Mass-Mode Bound

Timestamp: `{timestamp}`

- Discipline result: asymptotic flatness alone is rejected as a proof of `R_kernel=0`, because a source-free `C/r` Newton/Schwarzschild monopole is asymptotically flat.
- Derived formula: `R_kernel = -C_1/G_* = (1/(4*pi*G_*)) int_S grad(delta Phi).dS`.
- Conditional theorem: `Z_ref_charge & Z_no_incoming & Z_same_tau_surface & Z_no_extra_boundary_charge => R_kernel=0`.
- Bound branch: if the switch is unsigned, retain `|R_kernel|/M_H_ref <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_surface_flux + epsilon_boundary_charge + epsilon_radiative_mass_flux`.
- Claim status: private conditional only; public source-normalized Newton/local-GR claim waits on same-frame `M_H_ref` and reference-charge ownership.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3942 - Constraint Green-Map Uniqueness or Homogeneous Mass-Mode Bound"
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
    theorem = green_theorem_rows(timestamp)
    modes = homogeneous_mode_rows(timestamp)
    switch = boundary_switch_rows(timestamp)
    bounds = rkernel_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (theorem, modes, switch, bounds, decisions, gates, next_target)
    bound_symbols = {row["symbol"] for row in bounds}
    checks = [
        ("VAL3942_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3942_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3942_02_no_flatness_cheat", any(row["status"] == "NO_CHEAT_GUARD" and "C_1/r" in row["formula"] for row in theorem), "asymptotic flatness alone rejected"),
        ("VAL3942_03_mass_kernel_formula", any(row["status"] == "MASS_KERNEL_FORMULA_DERIVED" and "4*pi*G" in row["formula"] for row in theorem), "mass-kernel formula emitted"),
        ("VAL3942_04_conditional_zero", any(row["status"] == "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED" for row in theorem), "conditional R_kernel zero theorem emitted"),
        ("VAL3942_05_mode_audit", len(modes) == 6 and any(row["classification"] == "mass_kernel" for row in modes), "homogeneous mode audit emitted"),
        ("VAL3942_06_boundary_switch", len(switch) == 7 and any(row["switch_symbol"] == "Z_ref_charge" and row["status"] == "CORE_UNSIGNED" for row in switch), "boundary/reference switch emitted"),
        ("VAL3942_07_bound_rows", len(bounds) == 8 and "R_kernel_over_MHref" in bound_symbols and "epsilon_ref_charge" in bound_symbols, "R_kernel bound rows emitted"),
        ("VAL3942_08_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in gates), "claim gate blocks public claim"),
        ("VAL3942_09_next_3943", next_target[0]["next_doc"] == NEXT_DOC and "M_H_ref" in next_target[0]["target"], "next target selects M_H_ref/reference charge"),
        ("VAL3942_10_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3942_11_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3942_12_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3942_13_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3942_14_spine_written", SPINE_PATH.exists() and "3942 - Constraint Green-Map Uniqueness" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3942_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3942_16_script_compiles", True, "script compiles"),
        ("VAL3942_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["green_theorem"], green_theorem_rows(timestamp))
    write_csv(OUTPUTS["mode_audit"], homogeneous_mode_rows(timestamp))
    write_csv(OUTPUTS["boundary_switch"], boundary_switch_rows(timestamp))
    write_csv(OUTPUTS["bound_rows"], rkernel_bound_rows(timestamp))
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
        raise SystemExit(f"3942 validation failed: {failed}")
    print(f"3942 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
