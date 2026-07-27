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
DOC_PATH = ROOT / "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_BOUNDARY_REFERENCE_AHOM_LOCK_4158"
CHECKPOINT_ID = "4158"
DECISION = "BOUNDARY_REFERENCE_AHOM_LOCK_DERIVED_CONDITIONALLY_PACKET_UNSIGNED_KERNEL_BOUND_ROWS_READY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4158_00_4157_doc": (
        ROOT / "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md",
        "Prove the fixed parent boundary/reference data force",
        "4157 handoff to boundary/reference ahom lock.",
    ),
    "SRC4158_01_4157_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4157_NEXT_TARGET.csv",
        "H_ref, S_in/S_out",
        "4157 machine-readable next-target success gate.",
    ),
    "SRC4158_02_4157_kernel_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM.csv",
        "KZT4157_3_mass_flux",
        "4157 ahom-to-Rkernel amplitude law.",
    ),
    "SRC4158_03_4157_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4157_HOMOGENEOUS_MASS_RESIDUAL.csv",
        "HK4157_0_ahom",
        "4157 residual rows naming a_hom and epsilon_kernel.",
    ),
    "SRC4158_04_4038_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
        "BND4038_1_reference_lock",
        "Boundary/reference source-blind selected branch.",
    ),
    "SRC4158_05_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_2_bound_fields_once",
        "Poynting and bound EM no-extra-flux branch.",
    ),
    "SRC4158_06_4061_boundary_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
        "BND4061_1_reference_lock",
        "4061 boundary/reference kernel theorem.",
    ),
    "SRC4158_07_4054_no_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4054_NATURAL_NO_FLUX_SCALAR_CHARGE_THEOREM.csv",
        "NFL4054_4_energy_identity",
        "Natural no-flux energy-identity template.",
    ),
    "SRC4158_08_4043_domain": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "PZS4043_0_selected_signature",
        "Domain/projector fixed branch.",
    ),
    "SRC4158_09_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_6_boundary_projector_memory",
        "Candidate local parent packet side-channel clause.",
    ),
    "SRC4158_10_4056_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_4_side_channels",
        "Packet adoption gate that remains unsigned.",
    ),
    "SRC4158_11_4048_sufficiency": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_LOCAL_GR_SUFFICIENCY_THEOREM.csv",
        "SFT4048_1_Newton",
        "Conditional local-GR/Newton sufficiency theorem under packet adoption.",
    ),
    "SRC4158_12_4156_same_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "CMG4156_4_same_charge",
        "Same-charge equality condition feeding inner flux lock.",
    ),
    "SRC4158_13_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4158 boundary/reference ahom derivation.",
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
        "P8_Y5_R2FR_4158_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4158_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM.csv",
        "P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES.csv",
        "P8_Y5_R2FR_4158_NEWTON_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4158_NEWTON_IMPACT.csv",
        "P8_Y5_R2FR_4158_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4158_DECISION_GATES.csv",
        "P8_Y5_R2FR_4158_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4158_STATUS.csv",
        "P8_Y5_R2FR_4158_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4158_NEXT_TARGET.csv",
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


def boundary_lock_theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "BRL4158_0_annulus",
            "claim_piece": "exterior annulus monopole model",
            "formula": "Omega_ext={R_in<r<R_out}; h_0(r)=A+a_hom/r",
            "derivation": "The l=0 source-free solution on the compact local exterior annulus is a constant reference mode plus a free Newton/Schwarzschild monopole.",
            "result": "ANNULUS_MONOPOLE_MODEL_DERIVED",
            "proof_status": "standard_stationary_local_limit",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_1_two_dirichlet",
            "claim_piece": "two-boundary value lock",
            "formula": "a_hom=(h_in-h_out)/(1/R_in-1/R_out)",
            "derivation": "If both inner and outer representative values are fixed for the source-free difference h, then h_in=h_out=0 gives a_hom=0 and A=0.",
            "result": "AHOM_ZERO_IF_TWO_DIRICHLET_REFERENCES_FIXED",
            "proof_status": "conditional_on_parent_boundary_values",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_2_outer_plus_flux",
            "claim_piece": "outer reference plus inner charge lock",
            "formula": "Phi_h(S)=int_S grad h . dS=-4*pi*a_hom",
            "derivation": "Outer reference/falloff fixes A. The source-free inner Gauss/Hamiltonian flux fixes the monopole. If Phi_h(S_in)=0, then a_hom=0.",
            "result": "AHOM_ZERO_IF_SOURCE_FREE_FLUX_ZERO",
            "proof_status": "conditional_on_inner_charge_matching",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_3_Htau",
            "claim_piece": "Hamiltonian charge lock",
            "formula": "delta H_tau[h]=-(1/G_ref)a_hom + B_hidden[h]",
            "derivation": "For the EH/Newton charge readout, the homogeneous monopole is exactly the source-free Hamiltonian mass charge unless boundary/domain/EM/symplectic hidden charge terms are present.",
            "result": "HTAU_AHOM_LOCK_DERIVED_WITH_HIDDEN_CHARGE_TERM",
            "proof_status": "conditional_on_same_tau_frame_and_no_hidden_charge",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_4_4038_4061_import",
            "claim_piece": "what prior boundary rows supply",
            "formula": "D_source H_ref=D_readout H_ref=0; Phi_EM_rad=0; K_boundary_parent=0 on selected branch",
            "derivation": "4038/4061 suppress source-dependent reference drift and local boundary/Poynting leakage. They do not by themselves prove the gravitational source-free monopole charge is zero unless adopted as the parent boundary/charge condition.",
            "result": "PRIOR_BOUNDARY_BRANCH_IMPORTED_NOT_SUFFICIENT_ALONE",
            "proof_status": "honest_nonclaim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_5_packet_route",
            "claim_piece": "candidate parent packet route",
            "formula": "EH + same-source matter/EM + source-blind boundary/reference + fixed domain/projector + readout firewall => a_hom=0",
            "derivation": "If the 4056 packet is formally adopted, the outer reference, inner same-source charge, no-hidden-boundary, no-domain and no-readout-backfill clauses together kill the free monopole.",
            "result": "AHOM_ZERO_UNDER_FULL_PACKET_ADOPTION",
            "proof_status": "conditional_packet_unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_6_bound_if_unsigned",
            "claim_piece": "finite fallback",
            "formula": "epsilon_kernel <= epsilon_ref_value + epsilon_inner_charge + epsilon_Href + epsilon_hidden_boundary + epsilon_domain_gauge + epsilon_incoming",
            "derivation": "If any boundary/reference clause remains unsigned, the free monopole is retained as a strict no-cancellation amplitude bound rather than erased.",
            "result": "AHOM_BOUND_ROWS_READY_VALUES_MISSING",
            "proof_status": "bound_ready_not_score_ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "BRL4158_7_verdict",
            "claim_piece": "current verdict",
            "formula": "Z_outer_ref * Z_inner_charge * Z_Href * Z_no_hidden * Z_no_incoming * Z_no_backfill => a_hom=0; else bound epsilon_kernel",
            "derivation": "The exact boundary/reference contract for killing the kernel is now known. Current corpus has candidate selected branches, but full parent adoption and inner gravitational charge matching remain unsigned.",
            "result": "CONDITIONAL_LOCK_DERIVED_PACKET_UNSIGNED_BOUND_FALLBACK_ACTIVE",
            "proof_status": "forward_reduction_not_public_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "AB4158_0_dirichlet",
            "quantity": "epsilon_kernel_dirichlet",
            "formula": "epsilon_kernel <= (|delta h_in|+|delta h_out|)/(G_ref*M_H_ref*|1/R_in-1/R_out|)",
            "inputs_required": "R_in; R_out; delta h_in; delta h_out; G_ref; M_H_ref; source paths",
            "current_value": "MISSING_BOUNDARY_VALUE_ROWS",
            "units": "dimensionless",
            "observable_link": "boundary/reference; Newton 1/r coefficient",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "AB4158_1_flux",
            "quantity": "epsilon_kernel_flux",
            "formula": "epsilon_kernel <= |delta Phi_h(S_in)|/(4*pi*G_ref*M_H_ref)",
            "inputs_required": "source-free inner flux mismatch; G_ref; M_H_ref; same surface and tau",
            "current_value": "MISSING_INNER_SOURCE_FREE_FLUX_BOUND",
            "units": "dimensionless",
            "observable_link": "Gauss charge; source matching; orbital GM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "AB4158_2_Htau",
            "quantity": "epsilon_kernel_Htau",
            "formula": "epsilon_kernel <= |delta H_tau[h]-delta H_ref[h]|/M_H_ref + epsilon_hidden_boundary",
            "inputs_required": "delta H_tau source-free branch; delta H_ref; M_H_ref; hidden boundary estimate",
            "current_value": "MISSING_HTAU_SOURCE_FREE_CHARGE_BOUND",
            "units": "dimensionless",
            "observable_link": "Hamiltonian source charge; local GR",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "AB4158_3_hidden",
            "quantity": "epsilon_hidden_boundary",
            "formula": "epsilon_hidden_boundary <= epsilon_boundary_charge + epsilon_EM_flux + epsilon_symp + epsilon_domain_gauge",
            "inputs_required": "boundary charge bound; EM flux bound; symplectic/corner bound; domain/gauge bound",
            "current_value": "PARTIAL_ZERO_BRANCHES_EXIST_NOT_PARENT_ADOPTED",
            "units": "dimensionless",
            "observable_link": "EM/Poynting; boundary; PPN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "AB4158_4_incoming",
            "quantity": "epsilon_incoming_mass",
            "formula": "epsilon_incoming_mass=|a_incoming|/(G_ref*M_H_ref)",
            "inputs_required": "no-incoming/reset certificate or observational upper bound on incoming free monopole",
            "current_value": "MISSING_NO_INCOMING_MONOPOLE_CERTIFICATE",
            "units": "dimensionless",
            "observable_link": "local reset; source normalization",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "AB4158_5_total",
            "quantity": "epsilon_kernel_total",
            "formula": "epsilon_kernel <= route_bound(delta h or delta Phi_h or delta H_tau) + epsilon_hidden_boundary + epsilon_incoming_mass + epsilon_readout_backfill_guard",
            "inputs_required": "one fully sourced route bound plus hidden/incoming/readout guard values",
            "current_value": "BOUND_FORMULA_READY_COMPONENT_VALUES_MISSING",
            "units": "dimensionless",
            "observable_link": "Newton; local GR; PPN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "AG4158_0_outer_reference",
            "gate": "outer/reference value fixed",
            "requirement": "h_out or H_ref for the source-free difference is fixed before source/readout variation",
            "current_status": "SELECTED_BRANCH_EXISTS_FROM_4038_4061_NOT_FULL_PARENT_ADOPTION",
            "residual_if_failed": "epsilon_ref_value; C_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_1_inner_charge",
            "gate": "inner source-free charge matching",
            "requirement": "delta Phi_h(S_in)=0 or delta H_tau[h]=0 for h with no change in J_H_total",
            "current_status": "CONDITIONAL_FROM_4156_SAME_CHARGE_NOT_PARENT_SIGNED",
            "residual_if_failed": "epsilon_inner_charge; R_kernel",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_2_no_hidden_boundary",
            "gate": "no hidden boundary/domain/EM/symplectic mass charge",
            "requirement": "all side-channel mass charges are zero or bounded on the compact local collar",
            "current_status": "PARTIAL_SELECTED_BRANCHES_4038_4043_4054_4061_NOT_PACKET_SIGNED",
            "residual_if_failed": "epsilon_hidden_boundary",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_3_no_incoming",
            "gate": "no incoming/free monopole",
            "requirement": "the parent local reset excludes an externally supplied source-free Schwarzschild/Newton mass mode",
            "current_status": "UNSIGNED",
            "residual_if_failed": "epsilon_incoming_mass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_4_same_tau_surface",
            "gate": "same tau/surface/frame/units",
            "requirement": "the inner and outer charge comparisons use the same tau, linked surfaces, frame and units",
            "current_status": "UNSIGNED_EXCEPT_DISCIPLINE_ROWS",
            "residual_if_failed": "epsilon_surface_flux; C_frame; C_units",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_5_readout_firewall",
            "gate": "no orbital readout backfill",
            "requirement": "M_H_ref and boundary conditions are not fitted from mu_obs/G_ref",
            "current_status": "DISCIPLINE_LOCK_ACTIVE",
            "residual_if_failed": "epsilon_readout_backfill_guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4158_6_packet_adoption",
            "gate": "single parent packet adoption",
            "requirement": "4056 local parent packet is formally adopted as the MTS local branch before claims",
            "current_status": "CANDIDATE_PACKET_READY_NOT_FORMALLY_ADOPTED",
            "residual_if_failed": "closure_only_or_bound_branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4158_0_Newton",
            "component": "Newton source normalization",
            "result": "AHOM_IS_NOW_BOUNDARY_CHARGE_CONTROLLED",
            "meaning": "if the parent signs outer reference plus inner source-free charge zero, the free 1/r kernel cannot renormalize source mass",
            "still_needed": "inner charge matching and full parent packet adoption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4158_1_GR",
            "component": "local GR",
            "result": "FIRST_ORDER_SOURCE_GLUE_CONTRACT_SHARPENED",
            "meaning": "local GR no longer needs a vague source-coupling miracle at first order; it needs the a_hom boundary/charge clauses",
            "still_needed": "prove or bound those clauses before claiming local GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4158_2_testing",
            "component": "test path",
            "result": "BOUND_RUNNER_READY_NOT_NUMERIC",
            "meaning": "epsilon_kernel can now be tested once boundary value, flux or Hamiltonian mismatch rows exist",
            "still_needed": "numeric/source-backed rows for one route_bound and hidden/incoming terms",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4158_0_derivation",
            "question": "does boundary/reference data mathematically control a_hom?",
            "answer": "yes: on the annulus, a_hom is fixed by two boundary values or by an outer reference plus an inner source-free flux/Hamiltonian charge",
            "decision": "AHOM_CONTROL_LAW_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4158_1_live_zero",
            "question": "is a_hom=0 now live for MTS?",
            "answer": "not yet: 4038/4061 give selected boundary/reference silence, but full parent adoption and gravitational inner charge matching remain unsigned",
            "decision": "AHOM_ZERO_NOT_LIVE_PACKET_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4158_2_bound",
            "question": "what if the lock is not signed?",
            "answer": "retain epsilon_kernel with route-specific Dirichlet, flux or Hamiltonian bound rows and hidden/incoming no-cancellation add-ons",
            "decision": "STRICT_KERNEL_BOUND_FALLBACK_READY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4158_3_next",
            "question": "best next target",
            "answer": "prove the inner source-free Gauss/Hamiltonian charge matching condition, or populate the first source-backed epsilon_kernel bound row",
            "decision": "NEXT_INNER_GAUSS_CHARGE_MATCH_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "annulus_ahom_control_law_derived": "True",
            "two_dirichlet_zero_route_derived": "True",
            "outer_reference_plus_flux_zero_route_derived": "True",
            "Htau_ahom_lock_derived": "True",
            "prior_boundary_rows_imported": "True",
            "packet_adoption_parent_signed": "False",
            "inner_charge_matching_parent_signed": "False",
            "no_incoming_monopole_signed": "False",
            "kernel_bound_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4158_0",
            "target_doc": "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md",
            "target_script": "scripts/Y5_R2FR_4159_inner_Gauss_charge_matching_or_epsilon_kernel_bound.py",
            "objective": "prove that a source-free homogeneous exterior difference has zero inner Gauss/Hamiltonian charge under the same-source Hilbert branch, or populate the first source-backed epsilon_kernel bound",
            "success_gate": "delta Phi_h(S_in)=0 or delta H_tau[h]=0 is derived from same J_H_total, same tau/surface/frame/units, no hidden boundary charge and no readout backfill; otherwise a numeric/source-backed bound row is emitted",
            "reason": "4158 shows a_hom is killed by inner charge matching plus fixed outer reference; inner charge matching is the remaining sharp mathematical hinge.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4158 - Boundary Reference Data Lock Or Kernel Amplitude Bound

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4157 identified the exact obstruction:

`h_0=a_hom/r`

with

`epsilon_kernel=|a_hom|/(G_ref M_H_ref)`.

4158 asks whether fixed boundary/reference data kill `a_hom`, or whether the monopole must remain as a strict bound row.

## Annulus Calculation
Work on the compact local exterior annulus:

`Omega_ext={{R_in<r<R_out}}`.

For the `l=0` source-free difference:

`h_0(r)=A+a_hom/r`.

Two boundary values give:

`a_hom=(h_in-h_out)/(1/R_in-1/R_out)`.

Therefore, if the parent fixes both source-free representative values before readout,

`h_in=0` and `h_out=0 => a_hom=0`.

There is a second, more physical route. The monopole flux is:

`Phi_h(S)=int_S grad h . dS=-4*pi*a_hom`.

So an outer/reference branch plus source-free inner charge matching gives:

`Phi_h(S_in)=0 => a_hom=0`.

Equivalently, in Hamiltonian-charge language:

`delta H_tau[h]=-(1/G_ref)a_hom+B_hidden[h]`.

If `delta H_tau[h]=0` and `B_hidden[h]=0`, then `a_hom=0`.

## What The Existing Corpus Supplies
The earlier boundary rows are useful but not yet sufficient for a live claim:

- 4038/4061 supply a selected source-blind reference branch: `D_source H_ref=D_readout H_ref=0`.
- 4038/4155 supply local stationary Poynting/bound-EM no-extra-flux accounting.
- 4043 supplies a fixed domain/projector selected branch.
- 4054 supplies a no-flux energy-identity template.
- 4056 assembles these as a candidate local parent packet.

But the current corpus has not yet formally adopted that packet as the parent MTS branch, and it has not yet proved the gravitational source-free inner charge condition for `h`.

So 4158 derives the lock contract, but does not claim the lock is live.

## Conditional Lock Theorem
The exact contract is:

`Z_outer_ref * Z_inner_charge * Z_Href * Z_no_hidden * Z_no_incoming * Z_no_backfill => a_hom=0`.

Where:

- `Z_outer_ref`: outer/reference value is fixed before source/readout variation;
- `Z_inner_charge`: `delta Phi_h(S_in)=0` or `delta H_tau[h]=0` for source-free `h`;
- `Z_Href`: reference subtraction is source-blind and q-basic;
- `Z_no_hidden`: no boundary/domain/EM/symplectic hidden mass charge;
- `Z_no_incoming`: no externally supplied free monopole branch;
- `Z_no_backfill`: no orbital `GM` is used to define `M_H_ref`.

## Bound Fallback
If the lock is unsigned, retain route-specific bounds:

`epsilon_kernel <= (|delta h_in|+|delta h_out|)/(G_ref*M_H_ref*|1/R_in-1/R_out|)`,

or

`epsilon_kernel <= |delta Phi_h(S_in)|/(4*pi*G_ref*M_H_ref)`,

or

`epsilon_kernel <= |delta H_tau[h]-delta H_ref[h]|/M_H_ref + epsilon_hidden_boundary`.

The strict total fallback is:

`epsilon_kernel <= route_bound(delta h or delta Phi_h or delta H_tau) + epsilon_hidden_boundary + epsilon_incoming_mass + epsilon_readout_backfill_guard`.

No cancellation credit is allowed.

## Verdict
This is progress: `a_hom` is now controlled by a concrete boundary/charge equation. The problem is no longer "find a coupling." It is:

1. prove the inner source-free Gauss/Hamiltonian charge is zero on the same-source branch; or
2. source a numerical/observational bound for that charge mismatch.

Newton/local GR are still not claimed.

## Outputs
- `{outputs["P8_Y5_R2FR_4158_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4158_NEWTON_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4158_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4158_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4158_NEXT_TARGET"]}`

## Next Target
- `4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md`
- Prove `delta Phi_h(S_in)=0` / `delta H_tau[h]=0` for a source-free homogeneous difference under same `J_H_total`, or populate the first source-backed `epsilon_kernel` bound.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4158_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM"], boundary_lock_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES"], adoption_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_NEWTON_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4158_NEXT_TARGET"], next_rows())
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
        "VAL4158_0_sources",
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
    add("VAL4158_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "h_0(r)=A+a_hom/r",
        "a_hom=(h_in-h_out)/(1/R_in-1/R_out)",
        "Phi_h(S)=int_S grad h . dS=-4*pi*a_hom",
        "Z_outer_ref * Z_inner_charge",
        "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md",
    ]
    add("VAL4158_2_doc_tokens", "document records annulus law, flux law, lock contract, bounds and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM"]))
    theorem_tokens = [
        "ANNULUS_MONOPOLE_MODEL_DERIVED",
        "AHOM_ZERO_IF_TWO_DIRICHLET_REFERENCES_FIXED",
        "AHOM_ZERO_IF_SOURCE_FREE_FLUX_ZERO",
        "HTAU_AHOM_LOCK_DERIVED_WITH_HIDDEN_CHARGE_TERM",
        "PRIOR_BOUNDARY_BRANCH_IMPORTED_NOT_SUFFICIENT_ALONE",
        "AHOM_ZERO_UNDER_FULL_PACKET_ADOPTION",
        "AHOM_BOUND_ROWS_READY_VALUES_MISSING",
        "CONDITIONAL_LOCK_DERIVED_PACKET_UNSIGNED_BOUND_FALLBACK_ACTIVE",
    ]
    add("VAL4158_3_theorem", "theorem rows derive ahom control, conditional zero routes and nonclaim verdict", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    bounds_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4158_AHOM_AMPLITUDE_BOUND_ROWS"]))
    bound_tokens = [
        "epsilon_kernel_dirichlet",
        "epsilon_kernel_flux",
        "epsilon_kernel_Htau",
        "epsilon_hidden_boundary",
        "epsilon_incoming_mass",
        "epsilon_kernel_total",
        "BOUND_FORMULA_READY_COMPONENT_VALUES_MISSING",
    ]
    add("VAL4158_4_bounds", "bound rows include Dirichlet, flux, Hamiltonian, hidden, incoming and total fallbacks", all(token in bounds_text for token in bound_tokens), "bound tokens checked")

    gates_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES"]))
    gate_tokens = [
        "outer/reference value fixed",
        "inner source-free charge matching",
        "no hidden boundary/domain/EM/symplectic mass charge",
        "no incoming/free monopole",
        "same tau/surface/frame/units",
        "no orbital readout backfill",
        "single parent packet adoption",
    ]
    add("VAL4158_5_gates", "adoption gates identify exact clauses needed to make ahom zero live", all(token in gates_text for token in gate_tokens), "gate tokens checked")

    decisions_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4158_DECISION_GATES"]))
    decision_tokens = ["AHOM_CONTROL_LAW_DERIVED", "AHOM_ZERO_NOT_LIVE_PACKET_UNSIGNED", "STRICT_KERNEL_BOUND_FALLBACK_READY", "NEXT_INNER_GAUSS_CHARGE_MATCH_OR_BOUND"]
    add("VAL4158_6_decisions", "decision rows distinguish derived control law from live claim and next target", all(token in decisions_text for token in decision_tokens), "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4158_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("annulus_ahom_control_law_derived") == "True"
        and status[0].get("two_dirichlet_zero_route_derived") == "True"
        and status[0].get("outer_reference_plus_flux_zero_route_derived") == "True"
        and status[0].get("Htau_ahom_lock_derived") == "True"
        and status[0].get("packet_adoption_parent_signed") == "False"
        and status[0].get("inner_charge_matching_parent_signed") == "False"
        and status[0].get("kernel_bound_rows_emitted") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4158_7_status", "status records derived ahom law, unsigned packet/inner-charge gates and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4158_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md"
    add("VAL4158_8_next", "next target attacks inner Gauss/Hamiltonian charge matching or epsilon_kernel bound", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4158_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4158-Y5-R2FR" in item.name or "R2FR_4158" in item.name or "P8_Y5_R2FR_4158" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4158_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4158_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4158_VALIDATION.csv"
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
