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
DOC_PATH = ROOT / "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_INNER_GAUSS_CHARGE_MATCH_4159"
CHECKPOINT_ID = "4159"
DECISION = "INNER_GAUSS_CHARGE_MATCH_DERIVED_CONDITIONALLY_HIDDEN_INNER_CHARGE_RESIDUAL_RETAINED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4159_00_4158_doc": (
        ROOT / "4158-Y5-R2FR-boundary-reference-data-lock-or-kernel-amplitude-bound.md",
        "Prove `delta Phi_h(S_in)=0`",
        "4158 handoff to inner Gauss/Hamiltonian charge matching.",
    ),
    "SRC4159_01_4158_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4158_NEXT_TARGET.csv",
        "delta Phi_h(S_in)=0 or delta H_tau[h]=0",
        "4158 machine-readable next target.",
    ),
    "SRC4159_02_4158_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4158_BOUNDARY_REFERENCE_LOCK_THEOREM.csv",
        "BRL4158_2_outer_plus_flux",
        "4158 flux route showing inner charge kills a_hom.",
    ),
    "SRC4159_03_4158_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4158_PARENT_ADOPTION_GATES.csv",
        "AG4158_1_inner_charge",
        "4158 adoption gate naming inner charge as the hinge.",
    ),
    "SRC4159_04_4157_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4157_KERNEL_ZERO_THEOREM.csv",
        "KZT4157_3_mass_flux",
        "4157 Gauss flux amplitude law.",
    ),
    "SRC4159_05_4156_glue": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "CMG4156_2_chainmap",
        "Pi_M fixed chain-map condition.",
    ),
    "SRC4159_06_4155_worldtube": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "WT4155_1_total_current",
        "Total Hilbert current assembled once.",
    ),
    "SRC4159_07_4155_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK.csv",
        "PY4155_2_once_only",
        "Poynting once-only source-functional guard.",
    ),
    "SRC4159_08_4154_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK.csv",
        "MFL4154_2_flux_closure",
        "Hilbert mass flux closure condition.",
    ),
    "SRC4159_09_4154_mu": (
        SOURCE_DIR / "P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM.csv",
        "MZ4154_2_mass_flux",
        "Closed Hilbert mass flux result.",
    ),
    "SRC4159_10_worldtube_reference": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "T510_0_EH_reference_glue",
        "EH-style on-shell exterior charge reference.",
    ),
    "SRC4159_11_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_2_bound_fields_once",
        "Bound EM energy included once in total source.",
    ),
    "SRC4159_12_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_2_same_source_matter",
        "Candidate same-source matter clause.",
    ),
    "SRC4159_13_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4159 inner charge matching derivation.",
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
        "P8_Y5_R2FR_4159_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4159_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM.csv",
        "P8_Y5_R2FR_4159_HAMILTONIAN_MATCH_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4159_HAMILTONIAN_MATCH_ROWS.csv",
        "P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4159_REMAINING_GATES": SOURCE_DIR / "P8_Y5_R2FR_4159_REMAINING_GATES.csv",
        "P8_Y5_R2FR_4159_NEWTON_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4159_NEWTON_IMPACT.csv",
        "P8_Y5_R2FR_4159_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4159_STATUS.csv",
        "P8_Y5_R2FR_4159_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4159_NEXT_TARGET.csv",
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


def inner_gauss_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "IG4159_0_same_source_difference",
            "claim_piece": "same-source exterior difference",
            "formula": "delta J_H_total=0; delta W_H=0; delta Pi_M^C=0; delta tau=0",
            "derivation": "A genuine source-free homogeneous comparison must keep the total Hilbert current, source worldtube, parent mass projector and time generator fixed before readout.",
            "result": "SAME_SOURCE_DIFFERENCE_CONTRACT_DEFINED",
            "proof_status": "contract_derived",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_1_integrated_constraint",
            "claim_piece": "inner Gauss law split",
            "formula": "Phi_h(S_in)=int_{S_in} grad h . dS = 4*pi*G_ref*delta M_H_inner + Phi_hidden_inner",
            "derivation": "Integrating the linearized parent constraint over the source worldtube/collar gives the inner flux as the Hilbert source-charge difference plus any hidden inner boundary/domain/EM/symplectic charge.",
            "result": "INNER_GAUSS_SPLIT_DERIVED",
            "proof_status": "conditional_on_EH_Newton_constraint_readout",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_2_Hilbert_zero",
            "claim_piece": "Hilbert source contribution",
            "formula": "delta M_H_inner=ell_M(Pi_M^C delta J_H_total)+ell_M(delta Pi_M^C J_H_total)",
            "derivation": "Because J_H_total is the once-only matter+EM+binding Hilbert current, the first term is zero for a same-source comparison. A residual remains only if Pi_M is not fixed by the parent map.",
            "result": "HILBERT_INNER_CHARGE_ZERO_IF_PIM_FIXED",
            "proof_status": "conditional_on_PiM_chainmap_fixedness",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_3_hidden_zero",
            "claim_piece": "hidden inner charge condition",
            "formula": "Phi_hidden_inner=Phi_boundary+Phi_domain+Phi_symp+Phi_EM_extra+Phi_incoming",
            "derivation": "All non-Hilbert ways to source the inner flux are forced into named channels. Bound EM stress is already in J_H_total; only radiative/nonminimal leakage can remain outside.",
            "result": "HIDDEN_INNER_CHARGE_VECTOR_ISOLATED",
            "proof_status": "conditional_zero_or_bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_4_inner_match",
            "claim_piece": "inner charge matching",
            "formula": "delta J_H_total=0 and delta Pi_M^C=0 and Phi_hidden_inner=0 => Phi_h(S_in)=0",
            "derivation": "The same-source branch kills the Hilbert contribution; parent fixedness of Pi_M kills projector leakage; hidden-channel silence kills the remaining source-free inner charge.",
            "result": "INNER_GAUSS_CHARGE_MATCH_DERIVED_CONDITIONAL",
            "proof_status": "conditional_not_parent_signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_5_ahom",
            "claim_piece": "a_hom consequence",
            "formula": "Phi_h(S_in)=-4*pi*a_hom; Phi_h(S_in)=0 => a_hom=0",
            "derivation": "Combining the inner charge match with 4158's monopole flux law removes the homogeneous Newton/Schwarzschild mass kernel.",
            "result": "AHOM_ZERO_FOLLOWS_IF_INNER_MATCH_AND_OUTER_REFERENCE",
            "proof_status": "conditional_on_4158_outer_reference",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "IG4159_6_verdict",
            "claim_piece": "current verdict",
            "formula": "epsilon_kernel <= |ell_M(delta Pi_M^C J_H_total)|/M_H_ref + |Phi_hidden_inner|/(4*pi*G_ref*M_H_ref)",
            "derivation": "The Hilbert source part is no longer the mystery: same J_H_total kills it. The remaining obstruction is parent fixedness of Pi_M and hidden inner charge silence/adoption.",
            "result": "CONDITIONAL_MATCH_DERIVED_HIDDEN_INNER_RESIDUAL_RETAINED",
            "proof_status": "forward_reduction_not_public_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def hamiltonian_rows() -> List[dict]:
    return [
        {
            **common(),
            "row_id": "HM4159_0_surface_charge",
            "quantity": "delta_Htau_inner",
            "formula": "delta H_tau[S_in;h]=delta M_H_inner + H_hidden_inner",
            "meaning": "Hamiltonian language matches the Gauss split: the source-free inner charge is zero only if the Hilbert source difference and hidden charge are zero.",
            "status": "HAMILTONIAN_GAUSS_EQUIVALENCE_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "HM4159_1_once_only_EM",
            "quantity": "EM contribution",
            "formula": "delta J_EM=0 for same bound/minimal EM stress already included in J_H_total",
            "meaning": "Poynting/bound EM is not a second source of inner charge unless radiative or nonminimal leakage is present.",
            "status": "BOUND_EM_NOT_EXTRA_INNER_CHARGE_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "HM4159_2_improvement",
            "quantity": "exact improvement",
            "formula": "delta int_{W_H} dB_impr = delta int_{S_in} B_impr",
            "meaning": "Exact improvements are harmless only when the same representative/boundary value is fixed; otherwise they are part of Phi_hidden_inner.",
            "status": "IMPROVEMENT_SURFACE_TERM_EXPLICIT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "HM4159_3_no_backfill",
            "quantity": "readout firewall",
            "formula": "delta M_H_inner is computed from J_H_total, not from mu_obs/G_ref",
            "meaning": "The proof does not define the inner charge from the measured orbit; the orbit tests the derived charge.",
            "status": "NO_GM_LAUNDERING_GUARD_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "KB4159_0_projector",
            "quantity": "epsilon_Pi_inner",
            "formula": "epsilon_Pi_inner=|ell_M(delta Pi_M^C J_H_total)|/M_H_ref",
            "inputs_required": "parent-fixed Pi_M certificate or bound on delta Pi_M^C acting on J_H_total",
            "current_value": "MISSING_PIM_FIXEDNESS_CERTIFICATE_OR_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "KB4159_1_hidden_flux",
            "quantity": "epsilon_hidden_inner",
            "formula": "epsilon_hidden_inner=|Phi_hidden_inner|/(4*pi*G_ref*M_H_ref)",
            "inputs_required": "boundary/domain/symplectic/EM-extra/incoming inner charge zeros or bounds",
            "current_value": "MISSING_HIDDEN_INNER_CHARGE_ZERO_OR_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "KB4159_2_surface",
            "quantity": "epsilon_surface_mismatch",
            "formula": "epsilon_surface_mismatch=|delta_{S,tau,frame,units} Phi_h|/(4*pi*G_ref*M_H_ref)",
            "inputs_required": "same linked surface, tau, frame and units certificate or mismatch bound",
            "current_value": "MISSING_SURFACE_TAU_FRAME_UNITS_CERTIFICATE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "KB4159_3_source_difference",
            "quantity": "epsilon_delta_JH",
            "formula": "epsilon_delta_JH=|ell_M(Pi_M^C delta J_H_total)|/M_H_ref",
            "inputs_required": "same-source certificate; if comparing different sources, measured delta J_H_total",
            "current_value": "ZERO_ON_SAME_SOURCE_BRANCH_ELSE_INPUT_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "KB4159_4_total",
            "quantity": "epsilon_kernel_inner_bound",
            "formula": "epsilon_kernel <= epsilon_delta_JH + epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
            "inputs_required": "all component zeros or source-backed bounds",
            "current_value": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def remaining_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "RG4159_0_PiM_fixed",
            "gate": "Pi_M parent fixedness",
            "needed_for_zero": "delta Pi_M^C=0 on the same-source comparison",
            "current_status": "CONDITIONAL_FROM_4156_NOT_PARENT_SIGNED",
            "residual_if_failed": "epsilon_Pi_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "RG4159_1_hidden_inner",
            "gate": "hidden inner charge silence",
            "needed_for_zero": "Phi_boundary=Phi_domain=Phi_symp=Phi_EM_extra=Phi_incoming=0",
            "current_status": "PARTIAL_SELECTED_BRANCHES_NOT_PACKET_SIGNED",
            "residual_if_failed": "epsilon_hidden_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "RG4159_2_same_surface",
            "gate": "same S_in/tau/frame/units",
            "needed_for_zero": "the compared inner charge is the same geometric surface and generator",
            "current_status": "UNSIGNED_EXCEPT_DISCIPLINE_GUARD",
            "residual_if_failed": "epsilon_surface_mismatch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "RG4159_3_parent_packet",
            "gate": "single parent local packet adoption",
            "needed_for_zero": "same-source matter/EM, source-blind boundary, fixed domain and readout firewall are adopted as one action packet",
            "current_status": "CANDIDATE_PACKET_READY_NOT_FORMALLY_ADOPTED",
            "residual_if_failed": "closure_only_or_bound_branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "RG4159_4_numeric_bound",
            "gate": "first executable epsilon_kernel bound",
            "needed_for_zero": "if proof route is not adopted, component bounds must be numeric and source-backed",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "residual_if_failed": "epsilon_kernel_inner_bound_unscored",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4159_0_Hilbert",
            "component": "Hilbert source",
            "result": "HILBERT_PART_OF_INNER_CHARGE_ZERO_ON_SAME_SOURCE_BRANCH",
            "meaning": "the free monopole is not being fed by ordinary matter/EM/binding source current if J_H_total and Pi_M are fixed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4159_1_kernel",
            "component": "kernel obstruction",
            "result": "R_KERNEL_REDUCED_TO_PIM_AND_HIDDEN_INNER_CHARGE",
            "meaning": "a_hom now depends on projector fixedness and side-channel charge, not an undefined source coupling",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4159_2_Newton",
            "component": "Newton/local GR",
            "result": "NOT_CLAIMED_BUT_FIRST_ORDER_PATH_SHARPENED",
            "meaning": "if Pi_M fixedness and hidden inner charge silence are adopted, 4158 gives a_hom=0 and the first-order Newton source normalization closes conditionally",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "inner_Gauss_split_derived": "True",
            "Hilbert_inner_charge_zero_if_same_source": "True",
            "projector_fixedness_required": "True",
            "hidden_inner_charge_vector_isolated": "True",
            "ahom_zero_conditional_from_4158": "True",
            "PiM_fixedness_parent_signed": "False",
            "hidden_inner_charge_parent_signed": "False",
            "numeric_epsilon_kernel_bound_populated": "False",
            "epsilon_kernel_bound_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4159_0",
            "target_doc": "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_4160_PiM_fixedness_and_hidden_inner_charge_zero_or_bound.py",
            "objective": "prove Pi_M^C is fixed on the same-source local branch and hidden inner boundary/domain/EM/symplectic charges vanish, or populate numeric source-backed component bounds for epsilon_kernel",
            "success_gate": "delta Pi_M^C=0 and Phi_hidden_inner=0 are parent-derived from the local action packet; otherwise epsilon_Pi_inner and epsilon_hidden_inner have source-backed values",
            "reason": "4159 kills the Hilbert source part of the inner charge; the remaining kernel obstruction is projector fixedness plus hidden inner charge silence.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4159 - Inner Gauss Charge Matching Or Epsilon Kernel Bound

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4158 showed that the homogeneous monopole is killed if:

`Phi_h(S_in)=0`

or equivalently `delta H_tau[h]=0`, with fixed outer reference data.

4159 derives the inner charge matching condition from the same-source Hilbert branch.

## Same-Source Contract
A genuine source-free homogeneous comparison must keep:

`delta J_H_total=0; delta W_H=0; delta Pi_M^C=0; delta tau=0`.

The `delta Pi_M^C=0` clause matters. Otherwise the source current is the same but the source projector has changed, which is not a same-charge comparison.

## Inner Gauss Split
Integrating the linearized local constraint over the source worldtube/collar gives:

`Phi_h(S_in)=int_S_in grad h . dS = 4*pi*G_ref*delta M_H_inner + Phi_hidden_inner`.

The source-charge variation is:

`delta M_H_inner=ell_M(Pi_M^C delta J_H_total)+ell_M(delta Pi_M^C J_H_total)`.

On the same-source, fixed-projector branch:

`delta J_H_total=0` and `delta Pi_M^C=0 => delta M_H_inner=0`.

Therefore:

`Phi_h(S_in)=Phi_hidden_inner`.

If the hidden inner charge also vanishes,

`Phi_hidden_inner=0 => Phi_h(S_in)=0`.

Then 4158 gives:

`Phi_h(S_in)=-4*pi*a_hom => a_hom=0`.

## Hamiltonian Version
The same result in charge language is:

`delta H_tau[S_in;h]=delta M_H_inner+H_hidden_inner`.

For same `J_H_total`, fixed `Pi_M^C`, same `tau`, same surface/frame/units, and no hidden inner charge:

`delta H_tau[S_in;h]=0`.

This is the inner Hamiltonian charge match needed by 4158.

## What Actually Moved
The Hilbert source part is no longer vague. Ordinary matter, minimal EM stress, binding energy, and exact improvements are already inside `J_H_total` from 4155. If that total current is unchanged, it cannot source the homogeneous monopole.

The remaining obstruction is narrower:

- `delta Pi_M^C J_H_total` if the mass projector is not parent-fixed;
- `Phi_hidden_inner` from boundary/domain/symplectic/nonminimal-EM/incoming channels;
- surface/tau/frame/units mismatch.

## Bound Fallback
If the zero proof is not adopted, keep:

`epsilon_kernel <= epsilon_delta_JH + epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

On the same-source branch, `epsilon_delta_JH=0`, leaving:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

No numeric bound is claimed yet because the component values are not source-backed.

## Verdict
4159 conditionally proves the inner charge match up to two sharp clauses: parent fixedness of `Pi_M^C` and hidden inner charge silence. Newton/local GR remain unclaimed, but the first-order source-normalization problem is now much tighter.

## Outputs
- `{outputs["P8_Y5_R2FR_4159_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4159_HAMILTONIAN_MATCH_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4159_REMAINING_GATES"]}`
- `{outputs["P8_Y5_R2FR_4159_NEWTON_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4159_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4159_NEXT_TARGET"]}`

## Next Target
- `4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md`
- Prove `delta Pi_M^C=0` and `Phi_hidden_inner=0`, or populate source-backed bounds for `epsilon_Pi_inner` and `epsilon_hidden_inner`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4159_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM"], inner_gauss_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_HAMILTONIAN_MATCH_ROWS"], hamiltonian_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_REMAINING_GATES"], remaining_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_NEWTON_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4159_NEXT_TARGET"], next_rows())
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
        "VAL4159_0_sources",
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
    add("VAL4159_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "delta J_H_total=0; delta W_H=0; delta Pi_M^C=0; delta tau=0",
        "Phi_h(S_in)=int_S_in grad h . dS",
        "delta M_H_inner=ell_M(Pi_M^C delta J_H_total)+ell_M(delta Pi_M^C J_H_total)",
        "Phi_hidden_inner=0 => Phi_h(S_in)=0",
        "epsilon_kernel <= epsilon_delta_JH + epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
        "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md",
    ]
    add("VAL4159_2_doc_tokens", "document records same-source contract, Gauss split, Hamiltonian match, bound and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM"]))
    theorem_tokens = [
        "SAME_SOURCE_DIFFERENCE_CONTRACT_DEFINED",
        "INNER_GAUSS_SPLIT_DERIVED",
        "HILBERT_INNER_CHARGE_ZERO_IF_PIM_FIXED",
        "HIDDEN_INNER_CHARGE_VECTOR_ISOLATED",
        "INNER_GAUSS_CHARGE_MATCH_DERIVED_CONDITIONAL",
        "AHOM_ZERO_FOLLOWS_IF_INNER_MATCH_AND_OUTER_REFERENCE",
        "CONDITIONAL_MATCH_DERIVED_HIDDEN_INNER_RESIDUAL_RETAINED",
    ]
    add("VAL4159_3_theorem", "inner Gauss rows derive source split, Hilbert zero, hidden vector and ahom consequence", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    ham_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4159_HAMILTONIAN_MATCH_ROWS"]))
    ham_tokens = ["HAMILTONIAN_GAUSS_EQUIVALENCE_CONDITIONAL", "BOUND_EM_NOT_EXTRA_INNER_CHARGE_CONDITIONAL", "IMPROVEMENT_SURFACE_TERM_EXPLICIT", "NO_GM_LAUNDERING_GUARD_ACTIVE"]
    add("VAL4159_4_hamiltonian", "Hamiltonian rows include charge equivalence, EM once-only, improvement and no-laundering guard", all(token in ham_text for token in ham_tokens), "hamiltonian tokens checked")

    bounds_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS"]))
    bound_tokens = ["epsilon_Pi_inner", "epsilon_hidden_inner", "epsilon_surface_mismatch", "epsilon_delta_JH", "epsilon_kernel_inner_bound", "FORMULA_READY_COMPONENT_VALUES_MISSING"]
    add("VAL4159_5_bounds", "bound rows retain PiM, hidden, surface, source-difference and total epsilon_kernel components", all(token in bounds_text for token in bound_tokens), "bound tokens checked")

    gates_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4159_REMAINING_GATES"]))
    gate_tokens = ["Pi_M parent fixedness", "hidden inner charge silence", "same S_in/tau/frame/units", "single parent local packet adoption", "first executable epsilon_kernel bound"]
    add("VAL4159_6_gates", "remaining gates are narrowed to PiM fixedness, hidden charge, surface matching, packet adoption and numeric bound", all(token in gates_text for token in gate_tokens), "gate tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4159_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("inner_Gauss_split_derived") == "True"
        and status[0].get("Hilbert_inner_charge_zero_if_same_source") == "True"
        and status[0].get("projector_fixedness_required") == "True"
        and status[0].get("hidden_inner_charge_vector_isolated") == "True"
        and status[0].get("ahom_zero_conditional_from_4158") == "True"
        and status[0].get("PiM_fixedness_parent_signed") == "False"
        and status[0].get("hidden_inner_charge_parent_signed") == "False"
        and status[0].get("numeric_epsilon_kernel_bound_populated") == "False"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4159_7_status", "status records derived inner match, unsigned remaining clauses, no numeric bound and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4159_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md"
    add("VAL4159_8_next", "next target attacks PiM fixedness and hidden inner charge zero or bound", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4159_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4159-Y5-R2FR" in item.name or "R2FR_4159" in item.name or "P8_Y5_R2FR_4159" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4159_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4159_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4159_VALIDATION.csv"
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
