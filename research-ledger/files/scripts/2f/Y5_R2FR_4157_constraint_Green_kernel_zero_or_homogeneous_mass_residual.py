from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_CONSTRAINT_GREEN_KERNEL_ZERO_4157"
CHECKPOINT_ID = "4157"
DECISION = "CONSTRAINT_GREEN_KERNEL_ZERO_THEOREM_DERIVED_CONDITIONALLY_HOMOGENEOUS_MASS_RESIDUAL_RETAINED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4157_00_4156_doc": (
        ROOT / "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md",
        "homogeneous unsourced `1/r` mass kernel",
        "4156 handoff naming the homogeneous mass kernel as the sharp blocker.",
    ),
    "SRC4157_01_4156_zero_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_ZERO_THEOREM_GATES.csv",
        "ZG4156_0_kernel",
        "4156 machine-readable kernel gate.",
    ),
    "SRC4157_02_4156_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_NEXT_TARGET.csv",
        "unique exterior Green/constraint solution",
        "4156 next-target success gate.",
    ),
    "SRC4157_03_4156_glue": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "CMG4156_4_same_charge",
        "Same-charge condition requiring kernel zero.",
    ),
    "SRC4157_04_3941_map": (
        SOURCE_DIR / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv",
        "MAP3941_3_exact_split",
        "Earlier exact split where R_kernel first became a named residual.",
    ),
    "SRC4157_05_3942_green_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3942_GREEN_MAP_KERNEL_THEOREM.csv",
        "GKT3942_3_mass_flux",
        "Prior Green-map mass-flux formula.",
    ),
    "SRC4157_06_3942_bound_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3942_RKERNEL_BOUND_ROWS.csv",
        "RK3942_7_total",
        "Prior kernel bound-component rows.",
    ),
    "SRC4157_07_4012_charge_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
        "CHG4012_4_same_charge_equality",
        "Pi_M/H_tau charge-lock theorem requiring no homogeneous mass kernel.",
    ),
    "SRC4157_08_3532_no_laundering": (
        SOURCE_DIR / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "ZP3532_1_RPiM_no_GM_laundering",
        "No fitted-GM laundering guard.",
    ),
    "SRC4157_09_worldtube_source": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "T510_3_Newton_PPN_readout",
        "Worldtube source theorem saying the same charge must control the 1/r metric coefficient.",
    ),
    "SRC4157_10_4061_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
        "BND4061_1_reference_lock",
        "Boundary/reference lock source for killing reference drift.",
    ),
    "SRC4157_11_2717_green": (
        SOURCE_DIR / "P8_Y5_R2FR_2717_GREEN_KERNEL_CERTIFICATE.csv",
        "GRN2717_4_zero_limit",
        "General conditional Green-kernel zero limit.",
    ),
    "SRC4157_12_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4157 kernel-zero theorem attempt.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4157_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4157_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES": SOURCE_DIR / "P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES.csv",
        "P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL": SOURCE_DIR / "P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL.csv",
        "P8_Y5_R2FR_4157_NEWTON_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4157_NEWTON_IMPACT.csv",
        "P8_Y5_R2FR_4157_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4157_DECISION_GATES.csv",
        "P8_Y5_R2FR_4157_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4157_STATUS.csv",
        "P8_Y5_R2FR_4157_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4157_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def kernel_zero_theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "KZT4157_0_problem",
            "claim_piece": "kernel problem",
            "formula": "R_kernel := M_kernel/M_H_ref with M_kernel := H_tau[h]",
            "derivation": "4156 reduces same-charge source glue to whether the source-free exterior constraint problem permits a homogeneous mass charge independent of J_H_total.",
            "result": "HOMOGENEOUS_KERNEL_PROBLEM_DEFINED",
            "proof_status": "derived_setup",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_1_green_split",
            "claim_piece": "Green decomposition",
            "formula": "u_ext = G_ext S[J_H_total] + h; L_ext h=0",
            "derivation": "For fixed operator, gauge, domain, frame and source current, the difference between two exterior constraint solutions is a homogeneous solution.",
            "result": "GREEN_SPLIT_DERIVED",
            "proof_status": "conditional_on_fixed_operator_domain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_2_harmonic_basis",
            "claim_piece": "local Newton/EH weak-field limit",
            "formula": "h=C_0+a_hom/r+sum_{l>=1,m} C_lm r^{-(l+1)}Y_lm(theta,phi)",
            "derivation": "In the source-free stationary weak-field exterior, the mass-shifting part of the homogeneous solution is the l=0 monopole h_0=a_hom/r; C_0 is gauge/reference and l>=1 are multipole hair.",
            "result": "HOMOGENEOUS_1R_MODE_IDENTIFIED",
            "proof_status": "standard_local_limit_conditional",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_3_mass_flux",
            "claim_piece": "mass amplitude law",
            "formula": "M_kernel = -(1/G_ref) a_hom = (1/(4*pi*G_ref)) int_S grad h . dS; epsilon_kernel=|a_hom|/(G_ref M_H_ref)",
            "derivation": "Gauss flux isolates the monopole coefficient. The only homogeneous mode that renormalizes Newtonian source mass is a_hom/r.",
            "result": "AHOM_TO_RKERNEL_AMPLITUDE_LAW_DERIVED",
            "proof_status": "conditional_on_EH_Newton_readout",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_4_dirichlet_zero",
            "claim_piece": "strong boundary zero route",
            "formula": "L_ext h=0 with h|S_in=0 and h|S_out=0 => h=0",
            "derivation": "On a compact exterior annulus, elliptic uniqueness/maximum-principle or energy identity kills the whole homogeneous branch if both boundary representatives are fixed before readout.",
            "result": "KERNEL_ZERO_CONDITIONAL_BY_FIXED_DIRICHLET_BOUNDARIES",
            "proof_status": "conditional_not_parent_signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_5_charge_zero",
            "claim_piece": "monopole zero route",
            "formula": "delta H_tau[h]=0 and no hidden boundary/range/domain charge => a_hom=0",
            "derivation": "Even if higher homogeneous multipoles are retained as shape residuals, zero source-free Hamiltonian/Neumann charge removes the l=0 1/r mass mode.",
            "result": "KERNEL_ZERO_CONDITIONAL_BY_CHARGE_FLUX",
            "proof_status": "conditional_not_parent_signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_6_no_flatness_cheat",
            "claim_piece": "asymptotic-flatness guard",
            "formula": "h -> 0 as r -> infinity does not imply a_hom=0 because a_hom/r -> 0",
            "derivation": "The zero proof cannot use plain asymptotic flatness. It needs charge/reference/boundary data that fix the monopole coefficient.",
            "result": "NO_FLATNESS_CHEAT_GUARD_ACTIVE",
            "proof_status": "discipline_guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "KZT4157_7_verdict",
            "claim_piece": "current kernel verdict",
            "formula": "Z_Green * Z_boundary_reference * Z_no_hidden_charge * Z_no_readout_backfill => R_kernel=0; else retain R_kernel",
            "derivation": "A conditional theorem exists, but the current parent corpus has not signed the operator uniqueness, boundary/reference data, and hidden-charge exclusions needed to make it live.",
            "result": "NOT_LIVE_PARENT_SIGNED_R_KERNEL_RETAINED",
            "proof_status": "forward_reduction_not_public_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def uniqueness_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "GUG4157_0_operator",
            "gate": "same parent exterior operator",
            "condition": "L_ext, gauge, frame and units are fixed by the parent before source/readout variation",
            "why_needed": "otherwise the difference of two solutions includes operator drift, not only L_ext h=0",
            "current_status": "UNSIGNED",
            "residual_if_failed": "R_operator; C_frame; C_units",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_1_function_space",
            "gate": "stationary isolated exterior function space",
            "condition": "source-free annulus/exterior with regularity and falloff strong enough for elliptic uniqueness",
            "why_needed": "without the function-space contract, Green uniqueness is not a theorem",
            "current_status": "PARTIAL_STANDARD_LIMIT_NOT_PARENT_SIGNED",
            "residual_if_failed": "R_function_space; R_tail",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_2_boundary_reference",
            "gate": "fixed boundary/reference data",
            "condition": "S_in, S_out, H_ref, tau and representative boundary values are selected before orbital readout",
            "why_needed": "Dirichlet/charge data are what can kill a_hom; asymptotic flatness alone cannot",
            "current_status": "UNSIGNED_WITH_4061_SELECTED_BRANCH_ONLY",
            "residual_if_failed": "epsilon_ref_charge; epsilon_surface_flux; C_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_3_no_incoming",
            "gate": "no incoming/free monopole data",
            "condition": "the local reset/collar branch supplies no source-free Schwarzschild/Newton monopole",
            "why_needed": "a free a_hom/r mode can be present while still decaying at infinity",
            "current_status": "UNSIGNED",
            "residual_if_failed": "epsilon_incoming_mass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_4_no_hidden_boundary_charge",
            "gate": "no boundary/range/domain homogeneous source",
            "condition": "boundary, topological, symplectic, EM/Poynting and domain terms cannot carry independent mass charge",
            "why_needed": "hidden boundary charge can set a_hom without appearing in J_H_total",
            "current_status": "PARTIAL_EM_FROM_4155_AND_BOUNDARY_FROM_4061_NOT_FULLY_PARENT_SIGNED",
            "residual_if_failed": "epsilon_boundary_charge; R_boundary; R_symp; R_EM_flux; R_domain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_5_same_charge",
            "gate": "inner source charge matching",
            "condition": "delta H_tau[h] equals the Hilbert-source flux difference and is zero for source-free h",
            "why_needed": "Gauss law kills the monopole only when the source-free charge is actually zero",
            "current_status": "CONDITIONAL_FROM_4156_NOT_PARENT_SIGNED",
            "residual_if_failed": "epsilon_source_charge_mismatch; R_kernel",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "GUG4157_6_no_readout_backfill",
            "gate": "no orbital GM backfill",
            "condition": "M_H_ref is not defined as mu_obs/G_ref and Pi_M is not fitted from the orbit",
            "why_needed": "otherwise the free monopole is hidden by definition instead of derived",
            "current_status": "DISCIPLINE_LOCK_ACTIVE",
            "residual_if_failed": "GM_laundering_guard_violation",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def homogeneous_residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "HK4157_0_ahom",
            "quantity": "a_hom",
            "definition": "coefficient of the source-free l=0 homogeneous exterior mode h_0=a_hom/r",
            "formula": "a_hom = -G_ref M_kernel",
            "units": "G_ref*mass or potential_length_units",
            "observable_link": "Newtonian GM; orbital source normalization; PPN 1/r coefficient",
            "current_value": "MISSING_BOUNDARY_REFERENCE_CHARGE_LOCK_OR_NUMERIC_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_1_Rkernel",
            "quantity": "R_kernel_over_MHref",
            "definition": "normalized homogeneous mass-kernel leakage",
            "formula": "epsilon_kernel=|R_kernel|/M_H_ref=|a_hom|/(G_ref M_H_ref)",
            "units": "dimensionless",
            "observable_link": "source-normalized Newton limit; local GR source glue",
            "current_value": "FORMULA_READY_VALUE_MISSING",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_2_reference",
            "quantity": "epsilon_ref_charge",
            "definition": "reference/Hamiltonian boundary charge carried by h",
            "formula": "abs(H_tau[h]-H_ref[h])/M_H_ref",
            "units": "dimensionless",
            "observable_link": "source charge; boundary/reference lock",
            "current_value": "MISSING_PARENT_HREF_ZERO_OR_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_3_incoming",
            "quantity": "epsilon_incoming_mass",
            "definition": "free incoming/reset monopole amplitude not sourced by J_H_total",
            "formula": "abs(a_incoming)/(G_ref M_H_ref)",
            "units": "dimensionless",
            "observable_link": "local reset; clocks; orbital source normalization",
            "current_value": "MISSING_NO_INCOMING_MONOPOLE_CERTIFICATE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_4_hidden_boundary",
            "quantity": "epsilon_hidden_boundary_charge",
            "definition": "boundary/topological/symplectic/EM/domain mass charge not present in J_H_total",
            "formula": "abs(B_mass_hidden)/(M_H_ref)",
            "units": "dimensionless",
            "observable_link": "boundary; EM/Poynting; domain; PPN",
            "current_value": "MISSING_HIDDEN_CHARGE_ZERO_OR_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_5_multipole",
            "quantity": "epsilon_hom_multipole",
            "definition": "higher homogeneous exterior multipoles retained as shape hair rather than mass normalization",
            "formula": "sum_{l>=1,m} ||C_lm r^{-(l+1)}Y_lm||_obs",
            "units": "observable_norm",
            "observable_link": "PPN anisotropy; orbital multipoles",
            "current_value": "MULTIPOLE_BOUND_REQUIRED_IF_ACTIVE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "HK4157_6_total",
            "quantity": "epsilon_kernel_total",
            "definition": "strict no-cancellation kernel envelope",
            "formula": "epsilon_kernel <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_source_charge_mismatch + epsilon_hidden_boundary_charge + epsilon_surface_flux + epsilon_domain_gauge",
            "units": "dimensionless",
            "observable_link": "local GR; Newton; PPN",
            "current_value": "MISSING_COMPONENT_VALUES",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4157_0_Newton_source",
            "component": "Newton source normalization",
            "if_kernel_zero": "mu_obs = G_ref M_H_ref after the remaining 4156 source/charge gates close",
            "if_kernel_open": "mu_obs = G_ref M_H_ref + a_hom + other residual charges",
            "meaning": "the source-mass problem has been reduced to a measurable monopole amplitude instead of an undefined coupling gap",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4157_1_local_GR",
            "component": "local GR reduction",
            "if_kernel_zero": "the 1/r metric coefficient can be sourced by the same Hilbert/Hamiltonian charge",
            "if_kernel_open": "local GR remains blocked by a free Schwarzschild/Newton monopole not owned by the matter source",
            "meaning": "R_kernel is now the exact local-GR bottleneck for source normalization, not a vague missing derivation",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4157_2_PPN",
            "component": "PPN",
            "if_kernel_zero": "PPN can move on to beta/gamma/stress and second-order source stability",
            "if_kernel_open": "PPN fits cannot be interpreted because the first 1/r mass normalization is not source-owned",
            "meaning": "do not score PPN victory while epsilon_kernel is unbounded",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4157_0_derivation",
            "question": "can the homogeneous kernel be derived rather than listed as missing?",
            "answer": "yes conditionally: it is the homogeneous solution h of L_ext h=0, with mass amplitude a_hom/r and Gauss-flux normalization",
            "decision": "DERIVATION_ATTEMPT_SUCCEEDED_CONDITIONALLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4157_1_live_zero",
            "question": "is R_kernel=0 now a live MTS theorem?",
            "answer": "no: parent-signed Green uniqueness, fixed boundary/reference data, no incoming monopole, and no hidden boundary charge are still unsigned",
            "decision": "R_KERNEL_ZERO_NOT_LIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4157_2_next",
            "question": "best next target",
            "answer": "attack the boundary/reference data lock for a_hom, or emit the first numeric/observational epsilon_kernel bound if the lock fails",
            "decision": "NEXT_BOUNDARY_REFERENCE_AHOM_LOCK_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "kernel_zero_theorem_derived_conditional": "True",
            "homogeneous_1r_mode_identified": "True",
            "ahom_amplitude_law_derived": "True",
            "asymptotic_flatness_cheat_blocked": "True",
            "green_uniqueness_parent_signed": "False",
            "boundary_reference_data_signed": "False",
            "no_incoming_monopole_signed": "False",
            "no_hidden_boundary_charge_signed": "False",
            "R_kernel_residual_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4157_0",
            "target_doc": "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md",
            "target_script": "scripts/Y5_R2FR_4158_boundary_reference_data_lock_or_kernel_amplitude_bound.py",
            "objective": "prove fixed parent boundary/reference data kill a_hom before orbital readout, or produce a first strict epsilon_kernel bound row",
            "success_gate": "H_ref, S_in/S_out, tau, frame, gauge and no-incoming/no-hidden-charge clauses force delta H_tau[h]=0 and therefore a_hom=0; otherwise every component of epsilon_kernel has a sourced or observable bound",
            "reason": "4157 reduces the kernel obstruction to the monopole amplitude a_hom and the boundary/reference charge package that sets it.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4157 - Constraint Green Kernel Zero Or Homogeneous Mass Residual

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4156 narrowed the source-normalization problem to one sharp question:

Can the parent exterior constraint Green map contain a homogeneous unsourced `1/r` mass mode independent of `J_H_total`?

If no, the Newton source-glue branch moves forward. If yes or unsigned, the mode must be retained as `R_kernel`; it cannot be hidden inside fitted `GM`.

## Actual Derivation
Let `u_ext` denote the exterior Newton/EH weak-field charge/readout variable controlled by the parent constraint map. For fixed parent operator, gauge, frame, units, source domain and source current,

`L_ext u_ext = S[J_H_total]`.

If two candidate exterior solutions have the same `J_H_total`, their difference `h` obeys:

`L_ext h = 0`.

So the exact Green split is:

`u_ext = G_ext S[J_H_total] + h`.

In the stationary local weak-field exterior, the source-free scalar part has the harmonic form:

`h=C_0+a_hom/r+sum_{{l>=1,m}} C_lm r^{{-(l+1)}}Y_lm(theta,phi)`.

`C_0` is a reference/gauge constant. The higher multipoles are shape hair. The dangerous Newton-source term is:

`h_0=a_hom/r`.

The Gauss-flux amplitude law is:

`M_kernel = -(1/G_ref) a_hom = (1/(4*pi*G_ref)) int_S grad h . dS`,

so

`epsilon_kernel=|R_kernel|/M_H_ref=|a_hom|/(G_ref M_H_ref)`.

That is the precise residual, not a vague missing coupling.

## Conditional Zero Theorem
`R_kernel=0` follows if the parent supplies either of the following before orbital readout:

1. **Strong Dirichlet/energy route:** `L_ext h=0` on the fixed exterior annulus with `h|S_in=0` and `h|S_out=0`, giving `h=0` by uniqueness/maximum principle/energy identity.
2. **Charge-flux route:** `delta H_tau[h]=0` for every source-free homogeneous branch, with no hidden boundary/range/domain/EM/symplectic charge, giving `a_hom=0` by Gauss flux.

The guardrail is important:

`h -> 0` as `r -> infinity` does **not** prove `a_hom=0`, because `a_hom/r -> 0`.

So plain asymptotic flatness is not enough. The theory needs a fixed boundary/reference/charge package that kills the monopole.

## Current Verdict
The derivation succeeds conditionally, but not as a live MTS claim yet.

| Item | Status | Meaning |
|---|---|---|
| Green split `u=G_ext S+h` | DERIVED CONDITIONAL | requires fixed parent operator/domain |
| homogeneous `1/r` mode | IDENTIFIED | exact source-normalization obstruction |
| amplitude law | DERIVED CONDITIONAL | `epsilon_kernel=|a_hom|/(G_ref M_H_ref)` |
| asymptotic-flatness shortcut | BLOCKED | decay alone still allows `a_hom/r` |
| parent boundary/reference zero | UNSIGNED | next target |
| Newton/local GR claim | NOT CLAIMED | `R_kernel` retained |

## Residual Law
Until the boundary/reference lock is parent-signed, retain:

`epsilon_kernel <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_source_charge_mismatch + epsilon_hidden_boundary_charge + epsilon_surface_flux + epsilon_domain_gauge`.

No cancellation credit is allowed unless a parent identity proves the cancellation.

## What This Moves
This does move the framework forward: the kernel problem is no longer "something missing in the coupling." It is the exact question of whether the parent action fixes or forbids the source-free monopole coefficient `a_hom` before readout.

If `a_hom=0`, the same Hilbert/Hamiltonian source can control the Newtonian `1/r` term. If `a_hom` is nonzero or unbounded, local GR remains blocked at first order.

## Outputs
- `{outputs["P8_Y5_R2FR_4157_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES"]}`
- `{outputs["P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL"]}`
- `{outputs["P8_Y5_R2FR_4157_NEWTON_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4157_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4157_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4157_NEXT_TARGET"]}`

## Next Target
- `4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md`
- Prove the fixed parent boundary/reference data force `a_hom=0`, or produce the first strict `epsilon_kernel` bound row.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4157_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM"], kernel_zero_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES"], uniqueness_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL"], homogeneous_residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_NEWTON_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4157_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4157_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4157_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "L_ext h = 0",
        "h_0=a_hom/r",
        "epsilon_kernel=|R_kernel|/M_H_ref",
        "asymptotic flatness is not enough",
        "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md",
    ]
    add("VAL4157_2_doc_tokens", "document records Green split, ahom mode, amplitude law, guardrail and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM"]))
    theorem_tokens = [
        "GREEN_SPLIT_DERIVED",
        "HOMOGENEOUS_1R_MODE_IDENTIFIED",
        "AHOM_TO_RKERNEL_AMPLITUDE_LAW_DERIVED",
        "KERNEL_ZERO_CONDITIONAL_BY_FIXED_DIRICHLET_BOUNDARIES",
        "KERNEL_ZERO_CONDITIONAL_BY_CHARGE_FLUX",
        "NO_FLATNESS_CHEAT_GUARD_ACTIVE",
        "NOT_LIVE_PARENT_SIGNED_R_KERNEL_RETAINED",
    ]
    add("VAL4157_3_theorem", "kernel-zero theorem rows derive split, 1/r mode, amplitude law and nonclaim verdict", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    gates_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4157_GREEN_UNIQUENESS_GATES"]))
    gates_tokens = [
        "same parent exterior operator",
        "fixed boundary/reference data",
        "no incoming/free monopole data",
        "no boundary/range/domain homogeneous source",
        "inner source charge matching",
        "no orbital GM backfill",
    ]
    add("VAL4157_4_gates", "Green uniqueness gates include operator, function-space, reference, incoming, hidden charge and no-backfill clauses", all(token in gates_text for token in gates_tokens), "gate tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL"]))
    residual_tokens = [
        "a_hom",
        "R_kernel_over_MHref",
        "epsilon_ref_charge",
        "epsilon_incoming_mass",
        "epsilon_hidden_boundary_charge",
        "epsilon_kernel_total",
        "MISSING_COMPONENT_VALUES",
    ]
    add("VAL4157_5_residual", "homogeneous residual rows retain ahom, Rkernel and strict no-cancellation bound", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    impact_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4157_NEWTON_IMPACT"]))
    impact_tokens = ["Newton source normalization", "local GR reduction", "PPN", "mu_obs = G_ref M_H_ref + a_hom"]
    add("VAL4157_6_impact", "impact rows state Newton, local-GR and PPN consequences without claiming pass", all(token in impact_text for token in impact_tokens), "impact tokens checked")

    decisions_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4157_DECISION_GATES"]))
    decision_tokens = ["DERIVATION_ATTEMPT_SUCCEEDED_CONDITIONALLY", "R_KERNEL_ZERO_NOT_LIVE", "NEXT_BOUNDARY_REFERENCE_AHOM_LOCK_OR_BOUND"]
    add("VAL4157_7_decisions", "decision rows distinguish conditional derivation from live zero and select next target", all(token in decisions_text for token in decision_tokens), "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4157_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("kernel_zero_theorem_derived_conditional") == "True"
        and status[0].get("homogeneous_1r_mode_identified") == "True"
        and status[0].get("ahom_amplitude_law_derived") == "True"
        and status[0].get("asymptotic_flatness_cheat_blocked") == "True"
        and status[0].get("green_uniqueness_parent_signed") == "False"
        and status[0].get("boundary_reference_data_signed") == "False"
        and status[0].get("R_kernel_residual_rows_emitted") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4157_8_status", "status records conditional theorem, unsigned parent clauses and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4157_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md"
    add("VAL4157_9_next", "next target attacks boundary/reference ahom lock or bound", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4157_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4157-Y5-R2FR" in item.name or "R2FR_4157" in item.name or "P8_Y5_R2FR_4157" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4157_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4157_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4157_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
