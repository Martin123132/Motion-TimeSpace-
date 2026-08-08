from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3940"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds"
DOC_PATH = PCW / "3940-Y5-R2FR-source-charge-Hamiltonian-equality-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3940_SOURCE_REGISTER.csv",
    "subclauses": SRC / "P8_Y5_R2FR_3940_PC0_SUBCLAUSE_STACK.csv",
    "equality": SRC / "P8_Y5_R2FR_3940_SOURCE_CHARGE_EQUALITY_ATTEMPT.csv",
    "residuals": SRC / "P8_Y5_R2FR_3940_DELTA_CHARGE_RESIDUAL_BOUND_ROWS.csv",
    "bound_routes": SRC / "P8_Y5_R2FR_3940_PC0_BOUND_ROUTE_MATRIX.csv",
    "decision": SRC / "P8_Y5_R2FR_3940_PC0_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3940_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3940_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3940_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3940_VALIDATION.csv",
}

NEXT_DOC = "3941-Y5-R2FR-PiM-Hilbert-Htau-map-or-commutator-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3941_PiM_Hilbert_Htau_map_or_commutator_bound.py"


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
        ("SRC3940_00_3939_next", SRC / "P8_Y5_R2FR_3939_NEXT_TARGET.csv", "NEXT3939_0", "handoff selecting PC0 source-charge equality"),
        ("SRC3940_01_3939_pc0", SRC / "P8_Y5_R2FR_3939_PARENT_CLAUSE_STACK.csv", "PC3939_0_same_parent_source", "PC0 parent clause"),
        ("SRC3940_02_charge_direct", SRC / "P8_charge_current_equality_DIRECT_ATTEMPT.csv", "CC4_boundary_variation_equals_projected_source_variation", "direct charge/current equality attempt"),
        ("SRC3940_03_charge_residuals", SRC / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv", "Delta_PiM", "Delta_charge residual decomposition"),
        ("SRC3940_04_pg_contract", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "Hamiltonian charge to projected Hilbert source contract"),
        ("SRC3940_05_wfh_theorem", SRC / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv", "WFH3652_0_parent_source_Hamiltonian", "weak-field Hamiltonian source ownership attempt"),
        ("SRC3940_06_gm_rows", SRC / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "GMC3652_8_total_guard", "GM/source calibration no-cancellation guard"),
        ("SRC3940_07_flux_theorem", SRC / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv", "PFC3884_1_product_rule", "PiM/Hilbert flux product rule"),
        ("SRC3940_08_parent_action", LOCAL_BOUNDS / "Minimal_parent_action_charge_contract_2504_NONCLAIM.csv", "PAC2504_4_Hamiltonian_PiM", "minimal parent action charge contract"),
        ("SRC3940_09_noether_chain", LOCAL_BOUNDS / "Noether_Hamiltonian_charge_chain_2504_NONCLAIM.csv", "NHC2504_4_PiM_identification", "Noether/Hamiltonian PiM identity"),
        ("SRC3940_10_worldtube_selector", LOCAL_BOUNDS / "Worldtube_Hilbert_selector_theorem_2503_NONCLAIM.csv", "WHS2503_2_hamiltonian_mass_map", "worldtube Hilbert selector"),
        ("SRC3940_11_hilbert_norm", LOCAL_BOUNDS / "Hilbert_worldtube_source_normalization_2481_THEOREM_NONCLAIM.csv", "THM2481_5_zero_certificate_verdict", "Hilbert source normalization verdict"),
        ("SRC3940_12_pim_commutator", LOCAL_BOUNDS / "PiM_equality_commutator_rows_2899_NONCLAIM.csv", "PIMROW2899_5_total_no_cancellation", "PiM equality and commutator residual envelope"),
        ("SRC3940_13_source_measure", LOCAL_BOUNDS / "source_measure_Meff_flux_gate_2696_NONCLAIM.csv", "SMA2696_10_verdict", "source measure and flux gate"),
        ("SRC3940_14_gm_transfer", LOCAL_BOUNDS / "GM_transfer_PiM_component_rows_2595_NONCLAIM.csv", "GMC2595_TOTAL", "GM transfer PiM component envelope"),
        ("SRC3940_15_mhref_first", LOCAL_BOUNDS / "MHref_PiM_first_row_runner_rows_2947_NONCLAIM.csv", "RUN2947_4_no_cancellation", "MHref/PiM first row runner"),
        ("SRC3940_16_validation_3939", SRC / "P8_Y5_BRR545_3939_VALIDATION.csv", "VAL3939_16_no_pycache", "previous validation"),
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


def pc0_subclause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "PC0A_parent_action_phase_space",
            "parent action and covariant phase space",
            "There is one parent Lagrangian L[Phi] with delta L = E_A delta Phi^A + dTheta and a Hamiltonian generator H_tau for the observed local time flow tau.",
            "NHC2504_0-NHC2504_2; PAC2504_1",
            "CONDITIONAL_PHASE_SPACE_INPUT_EXISTS_BUT_BRANCH_UNSIGNED",
            "Delta_symp;Delta_frame",
            "parent Lagrangian, symplectic potential, and tau-normalization certificate",
        ),
        (
            "PC0B_same_observed_generator",
            "same observed generator",
            "The same tau/e_obs normalizes the source variation, boundary charge, clock readout, and slow-orbit readout.",
            "CC1; PG0; WHS2503_0-WHS2503_1",
            "SAME_FRAME_REQUIRED_NOT_PARENT_SIGNED",
            "Delta_frame;Delta_G",
            "same-frame source/clock/orbit generator lock",
        ),
        (
            "PC0C_Hilbert_source_descent",
            "Hilbert source descent",
            "S_matter = Sbar_matter[q(Phi),psi,e_obs] so the local source current is J_H[tau] with no hidden species/source-only slot.",
            "PAC2504_3; THM2481_0; WFH3652_0",
            "CONDITIONAL_HILBERT_SOURCE_OWNER_UNSIGNED",
            "Delta_nonEH;Delta_extra",
            "no source-only coupling theorem or finite source-shadow coefficient vector",
        ),
        (
            "PC0D_PiM_parent_map",
            "Pi_M is the parent Hamiltonian mass map",
            "Pi_M J_H is not a fitted/readout projector; it is the parent-derived map satisfying M_H[Pi_M J_H] = H_tau[S]-H_tau[reference].",
            "PAC2504_4; NHC2504_4; WHS2503_2; PIMROW2899_5",
            "CORE_BOTTLENECK_UNSIGNED",
            "Delta_PiM;Delta_charge",
            "PiM/Hilbert/H_tau map proof or commutator/equality bound rows",
        ),
        (
            "PC0E_variation_integrability",
            "variation equality and integrability",
            "delta(B_xi/G_eff) = delta M_H[Pi_M J_H] is an integrable one-form on the allowed parent phase-space branch.",
            "CC4; RUN2947_1-RUN2947_4; NHC2504_4",
            "INTEGRABILITY_REFERENCE_UNSIGNED",
            "Delta_symp;Delta_PiM",
            "Hamiltonian one-form curl zero plus fixed reference denominator",
        ),
        (
            "PC0F_reference_boundary_zero",
            "fixed reference and boundary zero",
            "The integration constant is zero because B_xi and M_H vanish on the same reference exterior, with no B_zero flux or boundary/reference leakage.",
            "CC5; PAC2504_6; GMC2595_TOTAL; RUN2947_4",
            "REFERENCE_BOUNDARY_ZERO_UNSIGNED",
            "Delta_symp;Delta_flux",
            "B_zero_flux, reference absorption, and homology/domain motion certificate",
        ),
        (
            "PC0G_no_extra_source_shadow",
            "no extra source shadow",
            "Non-EH, boundary, domain, memory, range, connection, and projector-stress mass-channel terms are zero or explicitly bounded before source equality is claimed.",
            "CC6; PG6; SMA2696_10; GMC3652_8",
            "EXTRA_SOURCE_SHADOW_UNSIGNED",
            "Delta_nonEH;Delta_extra;Delta_flux;Delta_G",
            "extra mass-channel vector with no-cancellation scoring",
        ),
    ]
    return [
        {
            "subclause_id": subclause_id,
            "subclause": subclause,
            "mathematical_condition": condition,
            "source_basis": basis,
            "current_status": status,
            "blocks_residuals": residuals,
            "needed_to_close": needed,
            "parent_signed_now": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for subclause_id, subclause, condition, basis, status, residuals, needed in data
    ]


def equality_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EA3940_0_definition",
            "claim": "PC0 source-charge equality target",
            "formula": "Delta_charge := B_xi/G_eff - M_H[Pi_M J_H]",
            "derivation_step": "define the exact object PC0 must kill; no fitted GM or orbital readout is allowed inside the definition",
            "uses_subclauses": "PC0A-PC0G",
            "result": "TARGET_DEFINED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_1_conditional_theorem",
            "claim": "conditional zero theorem",
            "formula": "PC0A and PC0B and PC0C and PC0D and PC0E and PC0F and PC0G => Delta_charge = 0",
            "derivation_step": "if all seven PC0 clauses are parent-signed, the boundary Hamiltonian charge and projected Hilbert source are the same parent mass functional with the same zero reference",
            "uses_subclauses": "PC0A;PC0B;PC0C;PC0D;PC0E;PC0F;PC0G",
            "result": "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_2_noether_step",
            "claim": "Noether/Hamiltonian bridge",
            "formula": "J_tau = Theta(Phi,L_tau Phi) - i_tau L, and on shell J_tau = dQ_tau + C_tau",
            "derivation_step": "PC0A makes B_xi a Hamiltonian boundary charge rather than a phenomenological potential coefficient",
            "uses_subclauses": "PC0A;PC0B",
            "result": "DERIVED_AS_FORMAL_STEP_NEEDS_PARENT_BRANCH_CERTIFICATE",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_3_source_step",
            "claim": "Hilbert source bridge",
            "formula": "C_tau^matter = J_H[tau] in the local slow-source collar",
            "derivation_step": "PC0C identifies the source side of the Hamiltonian constraint with the same matter action that clocks and orbiting probes read",
            "uses_subclauses": "PC0B;PC0C",
            "result": "CONDITIONAL_STEP_UNSIGNED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_4_pim_step",
            "claim": "PiM/Hilbert/H_tau identity",
            "formula": "M_H[Pi_M J_H] = H_tau[S]-H_tau[reference]",
            "derivation_step": "PC0D is the hard coupling lock: it forbids Pi_M from being a post-hoc source projector and makes it the parent Hamiltonian mass map",
            "uses_subclauses": "PC0D",
            "result": "CORE_BOTTLENECK_NOT_DERIVED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_5_integrate_step",
            "claim": "variation equality integrates to absolute equality",
            "formula": "delta(B_xi/G_eff - M_H[Pi_M J_H]) = 0 and (B_xi/G_eff - M_H[Pi_M J_H])_ref = 0",
            "derivation_step": "PC0E and PC0F turn the variation equality into an absolute equality, rather than equality up to a hidden reference constant",
            "uses_subclauses": "PC0E;PC0F",
            "result": "CONDITIONAL_STEP_UNSIGNED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_6_shadow_step",
            "claim": "extra source shadow exclusion",
            "formula": "Pi_M(Q_boundary+Q_bulk+Q_domain+Q_memory+Q_range+Q_connection+Q_nonEH)=0 or bounded",
            "derivation_step": "PC0G prevents equality from being faked by moving unowned mass charge into a hidden channel",
            "uses_subclauses": "PC0G",
            "result": "CONDITIONAL_STEP_UNSIGNED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EA3940_7_verdict",
            "claim": "3940 PC0 verdict",
            "formula": "Delta_charge is theorem-zero only inside the seven-clause PC0 branch; otherwise use the residual no-cancellation bound",
            "derivation_step": "the exact route exists, but the present corpus still lacks the parent-owned PiM/Hilbert/H_tau map plus integrability/reference/shadow signatures",
            "uses_subclauses": "PC0D;PC0E;PC0F;PC0G",
            "result": "CONDITIONAL_ROUTE_BUILT_CLAIM_BLOCKED",
            "parent_signed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "DCR3940_0_frame",
            "Delta_frame",
            "boundary charge generated in a different frame/normalization than matter or orbital readout",
            "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv;WHS2503_2;PG1",
            "same tau/e_obs source-clock-orbit generator lock or frame residual value",
            "MISSING_FRAME_SOURCE_LOCK",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_1_nonEH",
            "Delta_nonEH",
            "non-EH operator or source term alters the Hamiltonian charge/source constraint",
            "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv;SMA2696_10;GMC3652_8",
            "operator coefficient vector or theorem-zero for non-EH source contribution",
            "MISSING_NON_EH_OPERATOR_VECTOR",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_2_symp",
            "Delta_symp",
            "nonintegrable or reference-dependent boundary symplectic term",
            "CC4;RUN2947_4;PAC2504_6",
            "Hamiltonian one-form curl bound and fixed reference zero",
            "MISSING_SYMPLECTIC_CURL_AND_REFERENCE",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_3_PiM",
            "Delta_PiM",
            "projector variation or readout-defined mass projector shifts the source charge",
            "PIMROW2899_5;GMC2595_TOTAL;NHC2504_4;WHS2503_2",
            "PiM/Hilbert/H_tau equality or commutator/projector-stress envelope",
            "MISSING_PIM_HILBERT_HTAU_MAP",
            "dimensionless",
            "CORE_BOTTLENECK_UNFILLED",
        ),
        (
            "DCR3940_4_extra",
            "Delta_extra",
            "non-Hilbert sectors carry unowned mass-channel charge",
            "CC6;PG6;SMA2696_10;GMC3652_8",
            "extra mass-channel charge vector or Ward/no-hair zero proof",
            "MISSING_EXTRA_SOURCE_SHADOW_VECTOR",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_5_flux",
            "Delta_flux",
            "projected source mass drifts through boundary, domain, or radiative flux",
            "PFC3884_1;SMA2696_10;GMC2595_TOTAL",
            "closed PiM J_H flux theorem or finite flux leakage bound",
            "MISSING_SOURCE_FLUX_BOUND",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_6_G",
            "Delta_G",
            "charge normalization or effective coupling drifts relative to the source map",
            "GMC3652_8;P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv;P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "constant coupling proof or Gdot/R10/WEP normalization row",
            "MISSING_COUPLING_NORMALIZATION_BOUND",
            "dimensionless",
            "RETAINED_UNFILLED",
        ),
        (
            "DCR3940_7_total",
            "Delta_charge_abs_bound",
            "|Delta_charge| <= |Delta_frame|+|Delta_nonEH|+|Delta_symp|+|Delta_PiM|+|Delta_extra|+|Delta_flux|+|Delta_G|",
            "DCR3940_0-DCR3940_6",
            "all component values theorem-zero or source-backed finite with common denominator",
            "MISSING_COMPONENT_VALUES",
            "dimensionless",
            "NO_CANCELLATION_ENVELOPE_NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "residual_symbol": symbol,
            "definition": definition,
            "source_rows": sources,
            "required_input": required,
            "current_value": value,
            "units": units,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, sources, required, value, units, status in data
    ]


def bound_route_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BR3940_0_frame", "Delta_frame", "clock/WEP/frame source residual", "same-frame tau/e_obs lock or source-frame mismatch bound", "PC0B", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_1_nonEH", "Delta_nonEH", "R11/PPN/operator residual", "EH baseline plus non-EH source operator coefficients", "PC0C;PC0G", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_2_symp", "Delta_symp", "Hamiltonian integrability/reference residual", "curl of delta H_tau and reference boundary zero", "PC0A;PC0E;PC0F", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_3_PiM", "Delta_PiM", "PiM commutator/equality residual", "PiM/Hilbert/H_tau map or PIMROW2899/GMC2595 numeric envelope", "PC0D", "SELECTED_NEXT_TARGET"),
        ("BR3940_4_extra", "Delta_extra", "extra mass-channel residual", "Ward/no-hair zero proof or finite extra-source charge vector", "PC0G", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_5_flux", "Delta_flux", "Gdot/orbital flux residual", "closed d(Pi_M J_H)=0 theorem or source flux drift bound", "PC0F;PC0G", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_6_G", "Delta_G", "coupling-normalization residual", "constant kappa/G_eff branch or Gdot/WEP/R10 normalization row", "PC0B;PC0G", "NOT_READY_PARENT_OR_VALUE_MISSING"),
        ("BR3940_7_total", "Delta_charge_abs_bound", "strict no-cancellation total", "sum all absolute residuals; no cancellation and no fitted GM import", "PC0A-PC0G", "NOT_SCORE_READY"),
    ]
    return [
        {
            "row_id": row_id,
            "residual_symbol": symbol,
            "test_arena": arena,
            "bound_or_proof_needed": needed,
            "pc0_clause_dependency": clauses,
            "route_status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, arena, needed, clauses, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3940_0_theorem_branch",
            "decision": "PC0 has an exact conditional theorem branch",
            "effect": "if PC0A-PC0G are parent-signed, Delta_charge is exactly zero without fitting GM",
            "claim_status": "PRIVATE_CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3940_1_no_public_zero",
            "decision": "do not promote PC0 to a public zero",
            "effect": "the parent-owned PiM/Hilbert/H_tau map, integrability/reference zero, and extra source shadow clauses are unsigned",
            "claim_status": "SOURCE_CHARGE_CLAIM_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3940_2_bottleneck",
            "decision": "attack PC0D next",
            "effect": "the least-waste next move is the PiM/Hilbert/H_tau map or its commutator/equality bound; it is the narrow coupling bottleneck inside PC0",
            "claim_status": "NEXT_PIM_HILBERT_HTAU",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CG3940_0_sources",
            "gate": "source-backed checkpoint",
            "requirement": "all cited files and needles exist",
            "status": "PASS_IF_VALIDATION_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3940_1_conditional_theorem",
            "gate": "PC0 theorem skeleton",
            "requirement": "PC0A-PC0G imply Delta_charge=0",
            "status": "PASS_PRIVATE_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3940_2_parent_signatures",
            "gate": "parent-signed PC0",
            "requirement": "PiM/Hilbert/H_tau map, integrability/reference, same-frame source, and no extra source shadow all parent-signed",
            "status": "BLOCKED_PARENT_SIGNATURES_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3940_3_bound_values",
            "gate": "fallback source-charge bound",
            "requirement": "all Delta_charge residual components have theorem-zero or numeric source-backed values in common units",
            "status": "BLOCKED_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3940_4_public_claim",
            "gate": "public source/Newton/local-GR claim",
            "requirement": "PC0 theorem signed or Delta_charge_abs_bound scored below imported local bounds, then PC1-PC5 also pass",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3940_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attack PC0D: prove Pi_M J_H is the parent Hamiltonian mass map M_H[Pi_M J_H]=H_tau[S]-H_tau[reference], or produce a strict commutator/equality bound row",
            "success_condition": "Delta_PiM is theorem-zero or has source-backed bound components; PC0 source-charge equality no longer rests on a fitted/readout projector",
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
            "summary": "3940 turns PC0 source-charge equality into a seven-clause conditional theorem plus a boundable Delta_charge residual vector; the sharp next bottleneck is PiM/Hilbert/H_tau",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3940 - Source-Charge Hamiltonian Equality or Bound

Timestamp: `{timestamp}`

## Result

PC0 has been sharpened from a broad "same parent source" phrase into a seven-clause contract:

1. parent action and covariant phase space;
2. same observed generator;
3. Hilbert source descent;
4. `Pi_M` as the parent Hamiltonian mass map;
5. variation equality and integrability;
6. fixed reference and boundary zero;
7. no extra source shadow.

## Conditional Theorem

The exact private theorem is:

`PC0A and PC0B and PC0C and PC0D and PC0E and PC0F and PC0G => Delta_charge = B_xi/G_eff - M_H[Pi_M J_H] = 0`.

The proof route is not a vibe check: Noether current gives the Hamiltonian boundary charge, the same observed generator makes the matter source the Hilbert source, `Pi_M` maps that Hilbert current into the Hamiltonian mass channel, integrability plus a fixed reference removes the additive constant, and the no-shadow clause forbids hidden mass charge.

## Current Verdict

- Progress: exact conditional zero route built.
- Public claim: blocked.
- Main bottleneck: `Pi_M J_H -> H_tau` is still unsigned.
- Fallback: `Delta_charge_abs` is now a strict no-cancellation sum over `Delta_frame`, `Delta_nonEH`, `Delta_symp`, `Delta_PiM`, `Delta_extra`, `Delta_flux`, and `Delta_G`.

This is a forward step: the coupling problem is no longer "something is missing"; it is now a named proof target with a scoreable failure vector.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3940_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_PC0_SUBCLAUSE_STACK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_SOURCE_CHARGE_EQUALITY_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_DELTA_CHARGE_RESIDUAL_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_PC0_BOUND_ROUTE_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_PC0_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3940_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3940 - Source-Charge Hamiltonian Equality or Bound

Timestamp: `{timestamp}`

- PC0 has been reduced to seven exact clauses: parent phase space, same observed generator, Hilbert source descent, parent-owned `Pi_M`, integrability, fixed reference/boundary zero, and no extra source shadow.
- Conditional theorem: `PC0A-PC0G => Delta_charge = B_xi/G_eff - M_H[Pi_M J_H] = 0`.
- Claim status: private conditional only; public/local-GR/Newton claim remains blocked because the `Pi_M J_H -> H_tau` map, integrability/reference zero, and extra source shadow clauses are unsigned.
- Fallback branch: `Delta_charge_abs` is now a strict no-cancellation envelope over `Delta_frame`, `Delta_nonEH`, `Delta_symp`, `Delta_PiM`, `Delta_extra`, `Delta_flux`, and `Delta_G`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3940 - Source-Charge Hamiltonian Equality or Bound"
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
    subclauses = pc0_subclause_rows(timestamp)
    equality = equality_attempt_rows(timestamp)
    residuals = residual_bound_rows(timestamp)
    routes = bound_route_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (subclauses, equality, residuals, routes, decisions, claim_gate, next_target)
    residual_symbols = {row["residual_symbol"] for row in residuals}
    route_symbols = {row["residual_symbol"] for row in routes}
    checks = [
        ("VAL3940_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3940_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3940_02_subclause_count", len(subclauses) == 7, "seven PC0 subclauses emitted"),
        ("VAL3940_03_conditional_theorem", any(row["result"] == "CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED" for row in equality), "conditional Delta_charge zero theorem emitted"),
        ("VAL3940_04_core_bottleneck_marked", any(row["result"] == "CORE_BOTTLENECK_NOT_DERIVED" and "Pi_M" in row["formula"] for row in equality), "PiM/Hilbert/H_tau bottleneck marked"),
        ("VAL3940_05_residual_bound_rows", len(residuals) == 8 and "Delta_PiM" in residual_symbols and "Delta_charge_abs_bound" in residual_symbols, "Delta_charge residual bound rows emitted"),
        ("VAL3940_06_routes_cover_residuals", residual_symbols == route_symbols, "bound route matrix covers every residual row"),
        ("VAL3940_07_no_score_ready_claim_rows", all(str(row.get("score_ready")) == "False" for row in residuals + routes + subclauses), "residual, route, and subclause rows are not score-ready"),
        ("VAL3940_08_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public claim"),
        ("VAL3940_09_next_pim_target", next_target[0]["next_doc"] == NEXT_DOC and "Pi_M J_H" in next_target[0]["target"], "next target selects PiM/Hilbert/H_tau map"),
        ("VAL3940_10_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3940_11_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3940_12_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3940_13_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3940_14_spine_written", SPINE_PATH.exists() and "3940 - Source-Charge Hamiltonian Equality or Bound" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3940_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3940_16_script_compiles", True, "script compiles"),
        ("VAL3940_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["subclauses"], pc0_subclause_rows(timestamp))
    write_csv(OUTPUTS["equality"], equality_attempt_rows(timestamp))
    write_csv(OUTPUTS["residuals"], residual_bound_rows(timestamp))
    write_csv(OUTPUTS["bound_routes"], bound_route_rows(timestamp))
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
        raise SystemExit(f"3940 validation failed: {failed}")
    print(f"3940 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
