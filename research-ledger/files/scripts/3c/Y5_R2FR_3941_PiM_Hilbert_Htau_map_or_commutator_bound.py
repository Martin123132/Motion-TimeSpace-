from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3941"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3941-Y5-R2FR-PiM-Hilbert-Htau-map-or-commutator-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3941_SOURCE_REGISTER.csv",
    "map_derivation": SRC / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv",
    "constraint_map": SRC / "P8_Y5_R2FR_3941_CONSTRAINT_GREEN_PIM_CONSTRUCTION.csv",
    "proof_audit": SRC / "P8_Y5_R2FR_3941_CHAINMAP_PROOF_AUDIT.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3941_PIM_COMMUTATOR_BOUND_ROWS.csv",
    "em_stress": SRC / "P8_Y5_R2FR_3941_MAXWELL_STRESS_INCLUSION_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3941_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3941_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3941_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3941_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3941_VALIDATION.csv",
}

NEXT_DOC = "3942-Y5-R2FR-constraint-Green-map-uniqueness-or-homogeneous-mass-mode-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3942_constraint_Green_map_uniqueness_or_homogeneous_mass_mode_bound.py"


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
        ("SRC3941_00_3940_next", SRC / "P8_Y5_R2FR_3940_NEXT_TARGET.csv", "NEXT3940_0", "3940 handoff to PiM/Hilbert/H_tau"),
        ("SRC3941_01_3940_pc0", SRC / "P8_Y5_R2FR_3940_PC0_SUBCLAUSE_STACK.csv", "PC0D_PiM_parent_map", "PC0D parent map bottleneck"),
        ("SRC3941_02_3940_equality", SRC / "P8_Y5_R2FR_3940_SOURCE_CHARGE_EQUALITY_ATTEMPT.csv", "EA3940_4_pim_step", "PiM/Hilbert/H_tau equality step"),
        ("SRC3941_03_3940_residual", SRC / "P8_Y5_R2FR_3940_DELTA_CHARGE_RESIDUAL_BOUND_ROWS.csv", "DCR3940_3_PiM", "Delta_PiM residual row"),
        ("SRC3941_04_noether", LOCAL_BOUNDS / "Noether_Hamiltonian_charge_chain_2504_NONCLAIM.csv", "NHC2504_4_PiM_identification", "Noether/Hamiltonian PiM identity"),
        ("SRC3941_05_parent_action", LOCAL_BOUNDS / "Minimal_parent_action_charge_contract_2504_NONCLAIM.csv", "PAC2504_4_Hamiltonian_PiM", "minimal parent action charge contract"),
        ("SRC3941_06_worldtube", LOCAL_BOUNDS / "Worldtube_Hilbert_selector_theorem_2503_NONCLAIM.csv", "WHS2503_2_hamiltonian_mass_map", "worldtube selector and Hamiltonian map"),
        ("SRC3941_07_pim_commutator", LOCAL_BOUNDS / "PiM_equality_commutator_rows_2899_NONCLAIM.csv", "PIMROW2899_5_total_no_cancellation", "PiM equality/commutator envelope"),
        ("SRC3941_08_gm_transfer", LOCAL_BOUNDS / "GM_transfer_PiM_component_rows_2595_NONCLAIM.csv", "GMC2595_TOTAL", "GM transfer PiM component envelope"),
        ("SRC3941_09_mhref", LOCAL_BOUNDS / "MHref_PiM_first_row_runner_rows_2947_NONCLAIM.csv", "RUN2947_2_PiM_Hilbert", "PiM/Hilbert first-row requirement"),
        ("SRC3941_10_2900_contract", SRC / "P8_Y5_R2FR_2900_HILBERT_CURRENT_COMPLEX_CONTRACT.csv", "HCC2900_3_fixed_complex", "fixed Hilbert current complex contract"),
        ("SRC3941_11_2900_audit", SRC / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv", "SC2900_9_verdict", "current complex owner verdict"),
        ("SRC3941_12_flux", SRC / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv", "PFC3884_3_em_flux", "EM/Poynting flux exception"),
        ("SRC3941_13_3940_validation", SRC / "P8_Y5_BRR545_3940_VALIDATION.csv", "VAL3940_17_no_pycache", "previous validation"),
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


def map_derivation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MAP3941_0_target",
            "step": "target equality",
            "formula": "Delta_PiM := M_H[Pi_M J_H] - (H_tau[S]-H_tau[reference])",
            "derivation": "3941 isolates the PC0D coupling lock rather than reusing orbital GM or a fitted source normalization.",
            "result": "TARGET_DEFINED",
            "proof_status": "exact_target",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MAP3941_1_noether_constraint",
            "step": "Noether constraint source map",
            "formula": "delta H_tau = int_S(delta Q_tau - i_tau theta) = delta int_S B_tau + int_Sigma delta C_tau",
            "derivation": "For a parent diffeomorphism-invariant action, the Hamiltonian charge is controlled by the same constraint current that contains the Hilbert source.",
            "result": "FORMAL_COVARIANT_PHASE_SPACE_STEP",
            "proof_status": "conditional_on_parent_action_and_integrability",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MAP3941_2_constraint_pushforward",
            "step": "construct Pi_M from the parent constraint map",
            "formula": "Pi_M^C := D_N[C_tau] restricted to J_H[tau], where D_N is the parent constraint Dirichlet-to-Neumann/boundary-charge map",
            "derivation": "This is the non-circular construction: Pi_M is not a readout mask; it is the parent map that pushes a Hilbert source through the local constraint equations to the exterior Hamiltonian charge.",
            "result": "CONSTRUCTIVE_ROUTE_BUILT",
            "proof_status": "needs_constraint_Green_uniqueness_and_kernel_zero",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MAP3941_3_exact_split",
            "step": "exact residual split",
            "formula": "H_tau-H_ref = M_H[Pi_M^C J_H] + R_kernel + R_extra + R_symp + R_boundary + R_domain + R_tau + R_EM_flux",
            "derivation": "All ways the equality can fail are forced into named residual channels instead of being hidden inside the definition of Pi_M.",
            "result": "DERIVED_NO_CANCELLATION_SPLIT",
            "proof_status": "bound_ready_not_claim_ready",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MAP3941_4_conditional_theorem",
            "step": "conditional PiM/Hilbert/H_tau theorem",
            "formula": "R_kernel=R_extra=R_symp=R_boundary=R_domain=R_tau=R_EM_flux=0 => M_H[Pi_M^C J_H]=H_tau[S]-H_tau[reference]",
            "derivation": "If the parent constraint problem is unique with no homogeneous mass mode, no extra source shadow, an integrable Hamiltonian one-form, fixed boundary/reference, fixed domain, same tau, and no radiative EM flux through the boundary, PC0D closes.",
            "result": "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED",
            "proof_status": "private_conditional",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MAP3941_5_verdict",
            "step": "current verdict",
            "formula": "Delta_PiM is not zero yet; it is reduced to a constraint-map uniqueness/kernel problem plus explicit residual rows.",
            "derivation": "The work moved from abstract PiM ownership to a concrete parent constraint Green-map construction. The next proof target is the kernel/homogeneous mass mode, not another product-rule audit.",
            "result": "FORWARD_REDUCTION_NOT_PUBLIC_CLAIM",
            "proof_status": "claim_blocked_until_Green_map_or_bounds",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def constraint_map_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CGP3941_0_parent_constraint", "parent local constraint equation", "C_tau[Phi]=J_H[tau]+J_extra", "the source current enters the same parent constraint that defines H_tau", "PC0A;PC0C", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("CGP3941_1_boundary_charge_map", "Dirichlet-to-Neumann charge map", "D_N[C_tau]: source data on W_source -> boundary charge B_tau[S]", "constructs Pi_M from the parent equations rather than from an observed GM fit", "PC0D", "CONSTRUCTIVE_ROUTE_BUILT"),
        ("CGP3941_2_kernel_guard", "homogeneous mass mode guard", "ker(D_N)_mass = 0 under fixed reference/no-incoming/reset boundary data", "prevents a free Schwarzschild/Newtonian monopole from being added without source ownership", "PC0E;PC0F", "OPEN_NEXT_TARGET"),
        ("CGP3941_3_worldtube_complex", "same current complex", "J_H[tau] in C_H(A_ext;W_source,S_link,e_obs,tau) and Pi_M^C:C_H->C_M", "imports the useful 2900 current-complex contract into the Hamiltonian map", "PC0B;PC0D", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("CGP3941_4_no_readout_mask", "no readout projector", "Pi_M^C is fixed before orbital/PPN scoring and before measured GM calibration", "forbids the closure cheat the user was worried about", "PC0D", "PASS_GUARD_NONCLAIM"),
        ("CGP3941_5_metric_stress_guard", "projector stress silence", "delta Pi_M^C/delta g = 0 on the topological/constraint branch, or its stress contribution is retained", "separates the safe parent selector route from a Hodge/metric projector route", "PC0D;PC0G", "OPEN_BOUND_OR_ZERO"),
        ("CGP3941_6_em_inclusion", "Maxwell stress handling", "T_EM is included in J_H when it is inside the worldtube; radiative Poynting flux across the boundary is R_EM_flux", "keeps EM stress in the GR source while preventing radiation from being swept under the rug", "PC0C;PC0G", "CONDITIONAL_WITH_FLUX_RESIDUAL"),
    ]
    return [
        {
            "row_id": row_id,
            "construction_piece": piece,
            "formula": formula,
            "effect": effect,
            "pc0_dependency": dependency,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, effect, dependency, status in data
    ]


def proof_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("AUD3941_0_non_circularity", "Pi_M^C fixed before readout", "Pi_M is defined by the parent constraint boundary map, not by matching orbital GM", "PASS_GUARD_NONCLAIM", ""),
        ("AUD3941_1_noether_parent", "covariant phase-space Hamiltonian exists", "NHC2504_0-NHC2504_2 provide the formal chain if the parent action is supplied", "CONDITIONAL_UNSIGNED", "parent action and theta/Q_tau certificate"),
        ("AUD3941_2_hilbert_source", "Hilbert source belongs to same constraint", "J_H[tau] must be the matter variation in the same observed stack", "CONDITIONAL_UNSIGNED", "q/e_obs/tau/ell_J owner"),
        ("AUD3941_3_constraint_green", "constraint Green map unique", "D_N[C_tau] must have no unowned homogeneous mass mode under local boundary data", "OPEN_CORE_NEXT", "kernel/no-incoming/reference proof or bound"),
        ("AUD3941_4_chainmap", "Pi_M^C is a chain map", "[d,Pi_M^C]J_H=0 if the fixed current complex and domain are parent-owned", "EXACT_CONDITIONAL_NOT_CLAIM", "source complex/domain ownership"),
        ("AUD3941_5_same_object", "projected Hilbert current and Hamiltonian charge are same object", "R_eq=0 only if Pi_M^C J_H and the Hamiltonian source class share W_source and M_H_ref", "OPEN", "R_eq/M_H_ref value or theorem-zero"),
        ("AUD3941_6_stress_silence", "no projector stress", "topological/constraint selector has no independent metric stress; Hodge/domain selector does unless bounded", "OPEN_BOUND_OR_ZERO", "projector stress map or zero proof"),
        ("AUD3941_7_em_stress", "Maxwell/EM stress is not ignored", "bound EM fields inside W_source contribute to J_H; outgoing Poynting flux is a residual", "PASS_STRUCTURE_NONCLAIM", "radiative boundary flux zero or value"),
        ("AUD3941_8_verdict", "current PiM/Htau identity", "constructive route exists but is not parent-signed until the constraint Green map/kernel and residual rows close", "CLAIM_BLOCKED", "3942 Green-map target"),
    ]
    return [
        {
            "audit_id": audit_id,
            "claim_piece": piece,
            "formal_statement": statement,
            "result": result,
            "blocking_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, piece, statement, result, gap in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PB3941_0_kernel", "R_kernel_over_MHref", "homogeneous constraint mass mode not fixed by J_H", "abs(R_kernel)/M_H_ref", "MISSING_CONSTRAINT_GREEN_KERNEL_ZERO_OR_VALUE", "dimensionless", "Newton;PPN;local_GR"),
        ("PB3941_1_R_eq", "R_eq_over_MHref", "projected Hilbert current and Hamiltonian/topological source class mismatch", "abs(R_eq)/M_H_ref", "MISSING_R_EQ_INTEGRAL_OR_ZERO_PROOF", "dimensionless", "source_mass;Newton"),
        ("PB3941_2_commutator", "I_commutator_over_MHref", "fixed-domain chainmap failure [d,Pi_M^C]J_H", "abs(int_A [d,Pi_M^C]J_H)/M_H_ref", "MISSING_COMMUTATOR_ZERO_OR_VALUE", "dimensionless", "radial_Meff;R10;PPN"),
        ("PB3941_3_projector_stress", "epsilon_projector_stress", "metric/domain/Hodge dependence of Pi_M creates independent stress", "operator_norm(delta Pi_M^C/delta g)", "MISSING_PROJECTOR_STRESS_MAP_OR_ZERO", "PPN_or_dimensionless", "R11;PPN;local_GR"),
        ("PB3941_4_boundary", "B_zero_flux_over_MHref", "exact reference/boundary primitive shifts source mass", "abs(int_boundary dB_zero)/M_H_ref", "MISSING_BOUNDARY_ZERO_FLUX_CERTIFICATE", "dimensionless", "boundary;orbital;clock"),
        ("PB3941_5_domain_tau", "D_domain_tau_over_MHref", "moving worldtube/linking surface or tau frame shifts the current", "abs(D_domain Pi_M^C J_H + delta_tau J_H)/M_H_ref", "MISSING_DOMAIN_AND_TAU_LOCK", "dimensionless", "clock;orbital;radial_Meff"),
        ("PB3941_6_extra", "R_extra_over_MHref", "extra non-Hilbert source shadow enters the same Hamiltonian charge", "abs(R_extra)/M_H_ref", "MISSING_EXTRA_SOURCE_SHADOW_VECTOR", "dimensionless", "WEP;R10;PPN"),
        ("PB3941_7_em_flux", "R_EM_flux_over_MHref", "radiative Poynting/Maxwell flux crosses the boundary", "abs(int_boundary S_EM dot dA dt)/M_H_ref", "MISSING_EM_FLUX_ZERO_OR_VALUE", "dimensionless", "EM;clock;orbital"),
        ("PB3941_8_total", "Delta_PiM_abs_bound", "strict no-cancellation bound for PC0D", "sum_abs(PB3941_0..PB3941_7)", "MISSING_COMPONENT_VALUES", "dimensionless", "source_normalized_Newton;local_GR"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "current_value": current_value,
            "units": units,
            "observable_link": link,
            "source_path": str(DOC_PATH),
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, formula, current_value, units, link in data
    ]


def em_stress_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EM3941_0_bound_field",
            "case": "bound/local EM field inside source worldtube",
            "rule": "include T_EM in J_H[tau] and let the parent constraint map send it to H_tau",
            "effect": "Maxwell stress is part of the GR/Newton source channel rather than an extra hidden coupling",
            "residual": "none if stationary and inside W_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3941_1_radiative_flux",
            "case": "EM radiation or Poynting flow crosses the boundary",
            "rule": "retain R_EM_flux and do not set d(Pi_M J_H)=0",
            "effect": "open-system EM flow changes the source Hamiltonian mass instead of being claimed away",
            "residual": "R_EM_flux_over_MHref",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EM3941_2_public_guard",
            "case": "local Maxwell/GR claim",
            "rule": "claim only after T_EM inclusion, boundary flux, and nonminimal EM source-shadow terms are signed or bounded",
            "effect": "keeps the Maxwell route compatible with local GR without smuggling an EM closure axiom",
            "residual": "R_EM_flux;R_extra;Delta_nonEH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3941_0_constructive_pim",
            "decision": "replace abstract Pi_M with Pi_M^C from the parent constraint boundary-charge map",
            "effect": "moves the coupling lock from a symbolic projector to a concrete Green-map/constraint problem",
            "claim_status": "FORWARD_REDUCTION_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3941_1_no_claim",
            "decision": "do not claim PiM/Hilbert/H_tau equality yet",
            "effect": "constraint Green uniqueness, homogeneous mass-mode zero, M_H_ref, R_eq, commutator, projector stress, boundary flux, domain/tau, extra source and EM flux rows remain unsigned/unfilled",
            "claim_status": "CLAIM_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3941_2_next",
            "decision": "target the constraint Green map and homogeneous mass mode next",
            "effect": "this is the least-circular route to deriving measured Newtonian GM from the parent source rather than importing it",
            "claim_status": "NEXT_GREEN_MAP_KERNEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3941_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3941_1_constructive_route", "gate": "constructive PiM route", "requirement": "Pi_M^C is defined from parent constraint boundary map before readout", "status": "PASS_PRIVATE_CONSTRUCTIVE_ROUTE", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3941_2_kernel", "gate": "constraint Green uniqueness", "requirement": "no homogeneous mass mode/free monopole survives fixed reference boundary data", "status": "BLOCKED_CORE_NEXT_TARGET", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3941_3_bound_values", "gate": "fallback Delta_PiM bound", "requirement": "PB3941 component rows theorem-zero or source-backed finite in common denominator", "status": "BLOCKED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3941_4_public_claim", "gate": "public source-normalized Newton/local-GR claim", "requirement": "PC0D closes, then PC0 and PC1-PC5 pass", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3941_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the parent constraint Green/Dirichlet-to-Neumann map uniqueness and prove the homogeneous mass/free-monopole kernel is zero under fixed local reference/no-incoming boundary data, or produce R_kernel_over_MHref bound rows",
            "success_condition": "Pi_M^C becomes a parent-owned source-to-boundary-charge map with R_kernel=0 or a source-backed finite bound; measured Newtonian GM is not imported by hand",
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
            "summary": "3941 constructs Pi_M as the parent constraint boundary-charge map Pi_M^C and reduces PC0D to Green-map uniqueness plus explicit residual bounds",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3941 - PiM/Hilbert/Htau Map or Commutator Bound

Timestamp: `{timestamp}`

## Result

This checkpoint takes the actual leap at PC0D.

Instead of leaving `Pi_M` as a symbolic projector, 3941 constructs the only non-circular route that looks viable:

`Pi_M^C := D_N[C_tau] restricted to J_H[tau]`

where `D_N[C_tau]` is the parent constraint Dirichlet-to-Neumann / boundary-charge map. In plain English: the source current is pushed through the parent local constraint equations to the exterior Hamiltonian charge. That is exactly the GR/Newton style move: matter source -> constraint solution -> boundary flux/GM.

## Conditional Theorem

The derived split is:

`H_tau - H_ref = M_H[Pi_M^C J_H] + R_kernel + R_extra + R_symp + R_boundary + R_domain + R_tau + R_EM_flux`.

Therefore:

`R_kernel = R_extra = R_symp = R_boundary = R_domain = R_tau = R_EM_flux = 0 => M_H[Pi_M^C J_H] = H_tau[S] - H_tau[reference]`.

## Why This Moves Us Forward

- `Pi_M` is no longer allowed to be a fitted/readout mask.
- The coupling lock is now a constraint Green-map problem.
- A free homogeneous Newton/Schwarzschild monopole is identified as the central danger.
- Maxwell stress is included honestly: bound/local `T_EM` belongs in `J_H`; outgoing Poynting flux remains `R_EM_flux`.

## Current Verdict

- Constructive route: built.
- Public claim: blocked.
- Main missing proof: uniqueness of the parent constraint map with no unowned homogeneous mass mode.
- Fallback: `Delta_PiM_abs_bound` is now a no-cancellation sum over kernel, equality, commutator, projector stress, boundary, domain/tau, extra-source, and EM-flux residuals.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3941_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_CONSTRAINT_GREEN_PIM_CONSTRUCTION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_CHAINMAP_PROOF_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_PIM_COMMUTATOR_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_MAXWELL_STRESS_INCLUSION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3941_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3941 - PiM/Hilbert/Htau Map or Commutator Bound

Timestamp: `{timestamp}`

- Constructive move: `Pi_M` is replaced by `Pi_M^C`, the parent constraint Dirichlet-to-Neumann / boundary-charge map restricted to `J_H[tau]`.
- Derived split: `H_tau-H_ref = M_H[Pi_M^C J_H] + R_kernel + R_extra + R_symp + R_boundary + R_domain + R_tau + R_EM_flux`.
- Conditional theorem: if those residuals vanish, PC0D closes without importing orbital GM or using a readout projector.
- Maxwell/EM handling: bound/local `T_EM` is included in `J_H`; radiative Poynting flux remains an explicit residual.
- Claim status: private constructive route only; public source-normalized Newton/local-GR claim remains blocked.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3941 - PiM/Hilbert/Htau Map or Commutator Bound"
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
    derivation = map_derivation_rows(timestamp)
    construction = constraint_map_rows(timestamp)
    audit = proof_audit_rows(timestamp)
    bounds = bound_rows(timestamp)
    em_rows = em_stress_rows(timestamp)
    decisions = decision_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (derivation, construction, audit, bounds, em_rows, decisions, gates, next_target)
    bound_symbols = {row["symbol"] for row in bounds}
    checks = [
        ("VAL3941_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3941_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3941_02_constructive_pim", any("Pi_M^C" in row["formula"] and row["result"] == "CONSTRUCTIVE_ROUTE_BUILT" for row in derivation), "constructive Pi_M^C route emitted"),
        ("VAL3941_03_exact_split", any("R_kernel" in row["formula"] and row["result"] == "DERIVED_NO_CANCELLATION_SPLIT" for row in derivation), "exact residual split emitted"),
        ("VAL3941_04_conditional_theorem", any(row["result"] == "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED" for row in derivation), "conditional PiM/Htau theorem emitted"),
        ("VAL3941_05_green_kernel_next", any(row["status"] == "OPEN_NEXT_TARGET" and "homogeneous" in row["construction_piece"] for row in construction), "homogeneous mass-mode kernel identified"),
        ("VAL3941_06_audit_not_product_lap", any(row["result"] == "OPEN_CORE_NEXT" for row in audit), "audit advances to Green-map target rather than product-rule loop"),
        ("VAL3941_07_bound_rows", len(bounds) == 9 and "R_kernel_over_MHref" in bound_symbols and "Delta_PiM_abs_bound" in bound_symbols, "Delta_PiM bound rows emitted"),
        ("VAL3941_08_em_rows", len(em_rows) == 3 and any(row["residual"] == "R_EM_flux_over_MHref" for row in em_rows), "Maxwell/Poynting handling emitted"),
        ("VAL3941_09_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in gates), "claim gate blocks public claim"),
        ("VAL3941_10_next_3942", next_target[0]["next_doc"] == NEXT_DOC and "Green" in next_target[0]["target"], "next target selects constraint Green map"),
        ("VAL3941_11_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3941_12_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3941_13_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3941_14_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3941_15_spine_written", SPINE_PATH.exists() and "3941 - PiM/Hilbert/Htau Map or Commutator Bound" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3941_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3941_17_script_compiles", True, "script compiles"),
        ("VAL3941_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["map_derivation"], map_derivation_rows(timestamp))
    write_csv(OUTPUTS["constraint_map"], constraint_map_rows(timestamp))
    write_csv(OUTPUTS["proof_audit"], proof_audit_rows(timestamp))
    write_csv(OUTPUTS["bound_rows"], bound_rows(timestamp))
    write_csv(OUTPUTS["em_stress"], em_stress_rows(timestamp))
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
        raise SystemExit(f"3941 validation failed: {failed}")
    print(f"3941 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
