from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN_SOURCE = ROOT / "source-intake" / "hamiltonian-source"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2907-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row-under-AX1090.md"

SRC_2906_DOC = ROOT / "2906-Y5-R2FR-Y5-Y6-zero-odd-source-lock-or-epsilon-extra-source-split-under-AX1090.md"
SRC_2906_NEXT = RESIDUALS / "P8_Y5_R2FR_2906_NEXT_TARGET.csv"
SRC_2906_SPLIT = RESIDUALS / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv"
SRC_2595_COMPONENTS = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv"
SRC_2595_GATE = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv"
SRC_2460_DOC = ROOT / "2460-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md"
SRC_2460_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_2460_HAMILTONIAN_DENOMINATOR_CONTRACT.csv"
SRC_2460_CANDIDATES = RESIDUALS / "P8_Y5_PARENT_QLOC_2460_DENOMINATOR_CANDIDATE_ROWS.csv"
SRC_2460_LOCAL_BLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_2460_LOCAL_BOUND_SCORING_BLOCK.csv"
SRC_2462_FINAL_BLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_2462_DENOMINATOR_FINAL_BLOCK.csv"
SRC_2462_REOPEN = RESIDUALS / "P8_Y5_PARENT_QLOC_2462_REOPEN_MATERIAL_SPEC.csv"
SRC_2463_TRIAGE = RESIDUALS / "P8_Y5_LOCAL_GR_2463_ROUTE_TRIAGE.csv"
SRC_2463_PREREQ = RESIDUALS / "P8_Y5_LOCAL_GR_2463_PREREQUISITE_MATRIX.csv"
SRC_1006_DOC = ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"
SRC_1007_DOC = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"
SRC_1016_DOC = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
SRC_1017_DOC = ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2907_SOURCE_REGISTER.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_2907_DENOMINATOR_FRAME_LOCK_AUDIT.csv",
    "rows": RESIDUALS / "P8_Y5_R2FR_2907_DENOMINATOR_SOURCE_ROWS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2907_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2907_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2907_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2907_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2907_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2907_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "audit_copy": RAB_QUEUE / "JR2907_DENOMINATOR_FRAME_LOCK_AUDIT_NONCLAIM.csv",
    "rows_copy": HAMILTONIAN_SOURCE / "MHref_tau_source_frame_rows_2907_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2907_PARENT_ACTION_SKELETON_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2907_00_2906_doc", SRC_2906_DOC, "MHREF_TAU_SOURCE_FRAME_SURFACE_LOCK_SELECTED_NEXT;without positive same-frame M_ref, tau and linked surfaces", "handoff selecting M_ref/tau/source-frame/surface lock"),
        ("SRC2907_01_2906_next", SRC_2906_NEXT, "NEXT2906_0_2907;M_ref, tau_frame_lock and surface_homology_lock become parent-owned", "machine-readable 2907 target"),
        ("SRC2907_02_2906_split", SRC_2906_SPLIT, "SPL2906_0_Y5_GM_transfer;SPL2906_TOTAL", "Y5/Y6 split rows requiring a denominator before scoring"),
        ("SRC2907_03_2595_components", SRC_2595_COMPONENTS, "GMC2595_4_MHref;GMC2595_5_surfaces;GMC2595_6_tau_frame;GMC2595_TOTAL", "GM transfer component rows carrying MHref/tau/surface blockers"),
        ("SRC2907_04_2595_gate", SRC_2595_GATE, "GMT2595_6_MHref_tau_surface;GMT2595_7_no_orbital_shortcut;GMT2595_8_total", "anti-circular GM transfer gate"),
        ("SRC2907_05_2460_doc", SRC_2460_DOC, "HDC2460_0_charge_definition;HDC2460_7_current_verdict;No denominator, no scoring", "exact Hamiltonian denominator contract"),
        ("SRC2907_06_2460_contract", SRC_2460_CONTRACT, "HDC2460_0_charge_definition;HDC2460_6_positivity", "machine-readable Hamiltonian denominator clauses"),
        ("SRC2907_07_2460_candidates", SRC_2460_CANDIDATES, "MHD2460_0_Htau_minus_Href_live;MHD2460_3_orbital_GM_substitution", "candidate denominator rows and orbital-GM rejection"),
        ("SRC2907_08_2460_local_block", SRC_2460_LOCAL_BLOCK, "LBS2460_0_finite_Delta_ref_scoring;LBS2460_2_local_GR_PPN", "local-bound scoring block caused by missing denominator"),
        ("SRC2907_09_2462_final_block", SRC_2462_FINAL_BLOCK, "DFB2462_0_MHref_unavailable;DFB2462_3_local_GR_Newton_PPN", "final current-corpus denominator block"),
        ("SRC2907_10_2462_reopen", SRC_2462_REOPEN, "MAT2462_0_action_source;MAT2462_4_source_pack;MAT2462_5_reference_pack", "minimum material required to reopen MHref route"),
        ("SRC2907_11_2463_triage", SRC_2463_TRIAGE, "LGR2463_R0_new_parent_action_skeleton;LGR2463_R4_closure_axiom_or_plateau", "anti-circling route triage after denominator block"),
        ("SRC2907_12_2463_prereq", SRC_2463_PREREQ, "PRE2463_1_variational_origin_q_loc;PRE2463_2_source_bridge;PRE2463_4_local_vacuum_double_zero", "parent-action prerequisites"),
        ("SRC2907_13_1006_doc", SRC_1006_DOC, "MHA1006_0_definition;MHA1006_2_tau_frame_lock;MHA1006_3_fixed_reference", "earlier MHref denominator theorem audit"),
        ("SRC2907_14_1007_doc", SRC_1007_DOC, "HTA1007_0_target;HTA1007_6_integrability_verdict", "H_tau integrability/fixed-reference audit"),
        ("SRC2907_15_1016_doc", SRC_1016_DOC, "PSC1016_3_support_selector;PSC1016_5_dressed_source_charge;PSC1016_9_verdict", "worldtube/source-measure selector contract"),
        ("SRC2907_16_1017_doc", SRC_1017_DOC, "HRL1017_1_integrability_curl;HRL1017_5_MHref_denominator;HPT1017_4_denominator_guard", "Hamiltonian PiM reference-lock law"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DFL2907_0_parent_charge_definition",
            "M_H_ref is a parent Hamiltonian/source charge, not observed GM",
            "M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref) or G_ref^-1*int_S Q_tau^MTS with fixed reference",
            "DEFINITION_CONTRACT_ONLY",
            "definition exists, but Q_tau/H_tau/reference ownership is not promoted",
            "M_H_ref",
            SRC_2460_CONTRACT,
        ),
        (
            "DFL2907_1_theta_Qtau_extraction",
            "parent action supplies theta_MTS, J_tau and Q_tau^MTS for every retained sector",
            "delta L_parent = E_A delta Phi^A + d theta_MTS; J_tau = dQ_tau^MTS + C_tau",
            "BLOCKED_BY_PARENT_ACTION_MATERIAL",
            "EH charge alone cannot stand in for the full MTS charge",
            "epsilon_theta_Qtau_unowned",
            SRC_2460_CONTRACT,
        ),
        (
            "DFL2907_2_integrability_fixed_reference",
            "delta H_tau is finite, differentiable and path-independent with H_ref fixed before readout",
            "field-space curl zero; D_readout H_ref = D_source H_ref = 0",
            "BLOCKED_NONCLAIM",
            "without integrability M_H_ref is a one-form or convention, not a number",
            "epsilon_Htau_integrability_abs",
            SRC_1007_DOC,
        ),
        (
            "DFL2907_3_tau_coframe_lock",
            "same tau/coframe controls source, charge, clocks, rods, boundary and orbital readout",
            "tau_source = tau_charge = tau_clock = tau_boundary = tau_readout; e_source = e_readout = e_obs",
            "MISSING_TAU_COFRAME_LOCK",
            "frame mismatch makes normalized Y5/Y6 residuals meaningless",
            "tau_frame_lock",
            SRC_2595_COMPONENTS,
        ),
        (
            "DFL2907_4_source_worldtube_selector",
            "charge surface links a parent-selected compact source worldtube",
            "W_source = closure(supp J_H[tau]); S_outer links W_source in source-free exterior",
            "CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED",
            "surface can be a fitted mask unless the parent source owns it before readout",
            "source_worldtube_lock",
            SRC_1016_DOC,
        ),
        (
            "DFL2907_5_surface_homology_lock",
            "S1/S2/A_ext/r1/r2/worldtube homology class fixed before readout",
            "partial A = S2 - S1 with A cap W_source empty and exterior homology fixed",
            "MISSING_SURFACE_AND_HOMOLOGY_INPUTS",
            "post-readout surface choices can absorb radial/source normalization residuals",
            "surface_homology_lock",
            SRC_2595_COMPONENTS,
        ),
        (
            "DFL2907_6_positivity",
            "ordinary compact source gives positive nonzero denominator and extra sectors cannot flip sign",
            "int_S Q_tau^MTS - H_ref > 0 with silent or bounded extra/projector/boundary charges",
            "MISSING_PARENT_ENERGY_POSITIVITY_THEOREM",
            "division by M_H_ref is unsafe without source positivity and lower bounds",
            "epsilon_MHref_positivity",
            SRC_2460_CONTRACT,
        ),
        (
            "DFL2907_7_no_orbital_GM_shortcut",
            "observed slow-orbit GM is output only, never denominator/proof input",
            "GM_orbit substitution is rejected until Newton/GR reduction is derived",
            "GUARDRAIL_PASS_NONCLAIM",
            "this guardrail passes, but it is a refusal rule rather than a positive theorem",
            "epsilon_orbital_GM_shortcut",
            SRC_2460_CANDIDATES,
        ),
        (
            "DFL2907_8_2462_final_block",
            "do not reopen M_H_ref/N_E under current evidence without MAT2462 material",
            "single parent action source with owned sector variations, theta/Q pieces, fixed reference and source bridge",
            "FINAL_BLOCK_CURRENT_CORPUS",
            "current MTS lacks the parent action material required to promote the denominator",
            "epsilon_denominator_reopen_material",
            SRC_2462_FINAL_BLOCK,
        ),
        (
            "DFL2907_9_scoreability_verdict",
            "Y5/Y6 and PiM/worldtube rows become scoreable only after all same-branch denominator clauses pass",
            "positive same-frame M_ref plus tau/coframe/worldtube/surface/reference ownership",
            "DENOMINATOR_FRAME_LOCK_NOT_PROVED_ROWS_STAGED",
            "2907 writes honest rows and refuses local-GR/Newton scoring from this branch",
            "epsilon_denominator_scoreability_total",
            SRC_2906_SPLIT,
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "required_clause": required_clause,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "reason": reason,
                "residual_if_missing": residual_if_missing,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "same_branch_certified": False,
                "accepted_for_scoring": False,
            }
        )
        for audit_id, required_clause, mathematical_form, current_status, reason, residual_if_missing, source_path in specs
    ]


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DROW2907_0_MHref",
            "M_H_ref",
            "positive same-frame Hilbert/Hamiltonian source mass denominator",
            "mass_or_energy_units",
            "MISSING_M_H_REF_PARENT_SIGNED_VALUE",
            SRC_2595_COMPONENTS,
            "normalization;Hamiltonian_charge;source_mass;Newton;PPN",
            "M_H_ref;H_tau;H_ref;G_ref;tau_id;coframe_id;surface_outer;reference_rule;source_path;equation_ref",
        ),
        (
            "DROW2907_1_tau_frame_lock",
            "tau_frame_lock",
            "same tau/source/charge/readout frame for J_H, Q_M, M_H_ref, clocks and orbital readout",
            "certificate",
            "MISSING_TAU_FRAME_LOCK",
            SRC_2595_COMPONENTS,
            "clock;source_mass;orbital;PPN",
            "tau_source;tau_charge;tau_clock;tau_readout;parent_boundary_rule;source_path",
        ),
        (
            "DROW2907_2_observed_coframe_lock",
            "observed_coframe_lock",
            "one observed coframe/metric used by matter, clocks, rods, charge and readout",
            "certificate",
            "MISSING_OBSERVED_COFRAME_PARENT_LOCK",
            SRC_1016_DOC,
            "WEP;PPN;source_mass;orbital",
            "e_obs;matter_action;clock_rods_map;orbital_readout_map;source_path",
        ),
        (
            "DROW2907_3_surface_homology_lock",
            "surface_homology_lock",
            "S1/S2/A_ext/r1/r2/worldtube homology class fixed before readout",
            "topological_and_length_metadata",
            "MISSING_SURFACE_AND_HOMOLOGY_INPUTS",
            SRC_2595_COMPONENTS,
            "source_mass;radial_Meff;R10;orbital",
            "surface_inner;surface_outer;annulus;worldtube_id;homology_class;fixed_before_readout;source_path",
        ),
        (
            "DROW2907_4_annulus_metadata",
            "annulus_metadata",
            "compact exterior annulus and boundary metadata needed by I_commutator and B_zero flux rows",
            "length_and_topology_metadata",
            "MISSING_ANNULUS_METADATA",
            SRC_2595_COMPONENTS,
            "radial_Meff;boundary;clock;PPN",
            "r1;r2;A_ext;boundary_conditions;normal_orientation;source_path",
        ),
        (
            "DROW2907_5_Delta_Htau_Href_integrability",
            "Delta_Htau_Href_integrability",
            "field-space curl, fixed reference and symplectic/boundary flux residual for H_tau-H_ref",
            "dimensionless_after_M_H_ref",
            "MISSING_HTAU_INTEGRABILITY_FIXED_REFERENCE",
            SRC_1017_DOC,
            "Hamiltonian_charge;boundary;source_mass;local_GR",
            "delta_H_tau_nonintegrable;Delta_ref;B_zero_flux;Delta_symp;M_H_ref;source_path",
        ),
        (
            "DROW2907_6_source_worldtube_bridge",
            "source_worldtube_bridge",
            "parent source worldtube and measured source charge equality before orbital fitting",
            "mass_or_charge_units",
            "MISSING_PARENT_WORLDTUBE_SOURCE_MEASURE_BRIDGE",
            SRC_1016_DOC,
            "source_mass;Newton;orbital;PPN",
            "W_source;J_H;tau_id;Pi_M_map;linked_surfaces;M_H_ref;source_path",
        ),
        (
            "DROW2907_7_orbital_GM_shortcut_guard",
            "epsilon_orbital_GM_shortcut",
            "1 if observed or fitted orbital GM is used as denominator/proof input before Newton/GR derivation",
            "boolean_guard",
            "ORBITAL_GM_DENOMINATOR_REJECTED_GUARD_ACTIVE",
            SRC_2595_GATE,
            "Newton;orbital;local_GR",
            "must_be_zero_by_construction;source_path;guardrail_justification",
        ),
        (
            "DROW2907_8_denominator_reopen_material",
            "epsilon_denominator_reopen_material",
            "missing parent-action material required to reopen the Hamiltonian denominator route",
            "checklist_residual",
            "MAT2462_ACTION_VARIATION_CHARGE_GK_SOURCE_REFERENCE_PACKS_MISSING",
            SRC_2462_REOPEN,
            "local_GR;Newton;PPN;R10;clock;orbital",
            "MAT2462_0;MAT2462_1;MAT2462_2;MAT2462_3;MAT2462_4;MAT2462_5",
        ),
        (
            "DROW2907_TOTAL",
            "epsilon_denominator_scoreability_total",
            "absolute no-cancellation block: Y5/Y6 source rows cannot be scored until M_H_ref/tau/coframe/surface/reference/source bridge rows are real",
            "dimensionless_gate",
            "COMPONENTS_MISSING",
            SRC_2906_SPLIT,
            "PPN;R10;clock;orbital;local_GR;Newton",
            "all_DROW2907_rows_parent_signed_or_numeric_source_backed",
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "required_columns_before_claim": required_columns,
                "parent_signed": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, current_value, source_path, observable_link, required_columns in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RUN2907_0_zero_lock_attempt",
            "REFUSED_UNSIGNED_DENOMINATOR_FRAME_LOCK",
            "M_H_ref;tau_frame_lock;observed_coframe_lock;surface_homology_lock;source_worldtube_bridge;fixed_reference;positivity",
            0,
            "current corpus has the contract but not parent-signed denominator/frame/surface ownership",
        ),
        (
            "RUN2907_1_first_rows",
            "STAGED_NONCLAIM_DENOMINATOR_SOURCE_ROWS",
            "M_H_ref;tau_frame_lock;observed_coframe_lock;surface_homology_lock;annulus_metadata;Delta_Htau_Href_integrability;source_worldtube_bridge",
            0,
            "rows are source-backed to local files but contain MISSING values and cannot score Y5/Y6",
        ),
        (
            "RUN2907_2_orbital_guard",
            "PASS_REFUSAL_GUARDRAIL",
            "epsilon_orbital_GM_shortcut",
            1,
            "observed orbital GM remains rejected as denominator/proof input",
        ),
        (
            "RUN2907_3_anti_circling_pivot",
            "NEXT_PARENT_ACTION_ROUTE_SELECTED",
            "MAT2462 parent action/variation/charge/GK/source/reference packs plus Y5/Y6 coupling split",
            0,
            "2462 final-block means the next useful work is constructive parent-action material, not another MHref retry",
        ),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2907_0_contract_reused", "Exact M_H_ref/tau/source-frame/surface contract is available", "PASS_AS_CONTRACT_ONLY", "2460/1016/1017 already define the clauses sharply", True),
        ("CG2907_1_MHref_positive", "M_H_ref is positive and same-frame for current MTS", "BLOCKED_NONCLAIM", "theta/Q_tau, integrability, fixed reference, source bridge and positivity are unsigned", False),
        ("CG2907_2_tau_surface_lock", "tau/coframe/surface/worldtube are parent-owned in one branch", "BLOCKED_NONCLAIM", "observed coframe, tau and linked surfaces are not parent-signed before readout", False),
        ("CG2907_3_Y5Y6_scoreability", "Y5/Y6 source split can be scored against local arenas", "BLOCKED_NONCLAIM", "source rows lack numeric same-frame denominator and arena projections", False),
        ("CG2907_4_orbital_GM_shortcut", "orbital GM may fill the denominator", "REFUSED_CIRCULAR_SHORTCUT", "using the target Newtonian readout would smuggle in the theorem", True),
        ("CG2907_5_denominator_reopen", "Hamiltonian denominator route may be reopened now", "FINAL_BLOCK_CURRENT_CORPUS", "2462 says new parent-action material is required first", False),
        ("CG2907_6_local_GR_Newton", "local GR/Newton follows after 2907", "BLOCKED_NONCLAIM", "2907 stages rows and prevents circular scoring; it does not prove local reduction", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2907_0_lock_attempt", "MHREF_TAU_SOURCE_FRAME_SURFACE_LOCK_NOT_PROMOTED", "the necessary clauses exist as contracts but not as one parent-signed branch", "keep denominator/frame/surface rows nonclaim"),
        ("DEC2907_1_rows_staged", "FIRST_DENOMINATOR_ROWS_STAGED_NONCLAIM", "Y5/Y6 residuals need concrete denominator and surface inputs before tests can mean anything", "machine-readable source rows now name every missing quantity"),
        ("DEC2907_2_no_orbital_shortcut", "ORBITAL_GM_DENOMINATOR_REJECTED", "using measured orbital GM would import Newton into the Newton derivation", "guardrail remains active"),
        ("DEC2907_3_anti_circling", "DO_NOT_RETRY_MHREF_UNTIL_MAT2462_EXISTS", "2462 already final-blocked the Hamiltonian denominator under current evidence", "next checkpoint pivots to constructive parent-action skeleton with Y5/Y6 coupling/source ownership"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2907_0_2908",
                "selection_status": "selected_primary",
                "target_file": "2908-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-source-bridge-and-Y5Y6-coupling-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_action_skeleton_for_q_loc_source_bridge_and_Y5Y6_coupling_under_AX1090_2908.py",
                "task": "construct the smallest parent-action skeleton that owns Gamma/Khat/q_loc, Pi_M/worldtube source bridge, Y5 source normalization and Y6 extra-stress coupling in one branch",
                "success_condition": "all retained variables have action, variation, source, boundary and readout owners sufficient to reopen local GR/Newton derivation without M_H_ref circularity",
                "fallback_condition": "write explicit orphan/residual rows for q_loc, Y5 and Y6 with source-bound inputs; keep local-GR claim blocked",
                "guardrails": "no M_H_ref reuse without MAT2462; no orbital-GM denominator; no plateau axiom; no closure-only theorem; no local-GR claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2907_0_audit_copy", OUTPUTS["audit"], BRANCH_OUTPUTS["audit_copy"], "RAB queue copy of denominator/frame/surface lock audit"),
        ("BR2907_1_rows_copy", OUTPUTS["rows"], BRANCH_OUTPUTS["rows_copy"], "Hamiltonian-source copy of first denominator/source-frame rows"),
        ("BR2907_2_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB queue copy of 2908 parent-action skeleton target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows_data = all_rows["sources"]
    audit_rows_data = all_rows["audit"]
    denominator_rows_data = all_rows["rows"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    decision_rows_data = all_rows["decision"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "M_H_ref",
        "tau_frame_lock",
        "observed_coframe_lock",
        "surface_homology_lock",
        "annulus_metadata",
        "Delta_Htau_Href_integrability",
        "source_worldtube_bridge",
        "epsilon_orbital_GM_shortcut",
        "epsilon_denominator_reopen_material",
        "epsilon_denominator_scoreability_total",
    }
    found_symbols = {row["symbol"] for row in denominator_rows_data}
    checks = [
        ("VAL2907_0_sources_exist", all(row["path_exists"] for row in source_rows_data), "all registered source paths exist"),
        ("VAL2907_1_source_anchors", all(row["anchors_found"] for row in source_rows_data), "all registered source anchors were found"),
        ("VAL2907_2_audit_complete", len(audit_rows_data) == 10 and any(row["audit_id"] == "DFL2907_9_scoreability_verdict" for row in audit_rows_data), "denominator/frame/surface audit has all clauses"),
        ("VAL2907_3_audit_nonclaim", all(not row["parent_signed"] and not row["accepted_for_scoring"] for row in audit_rows_data), "audit rows remain unsigned nonclaim"),
        ("VAL2907_4_denominator_symbols_present", required_symbols <= found_symbols, "denominator source symbols are present"),
        ("VAL2907_5_denominator_paths_exist", all(row["source_path_exists"] for row in denominator_rows_data), "denominator rows point to existing local sources"),
        ("VAL2907_6_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in denominator_rows_data), "denominator rows remain non-score-ready and nonclaim"),
        ("VAL2907_7_no_orbital_shortcut_guard", any(row["symbol"] == "epsilon_orbital_GM_shortcut" and "REJECTED" in row["current_value"] for row in denominator_rows_data), "orbital GM denominator shortcut remains rejected"),
        ("VAL2907_8_runner_refuses", any(row["runner_id"] == "RUN2907_0_zero_lock_attempt" and row["status"] == "REFUSED_UNSIGNED_DENOMINATOR_FRAME_LOCK" for row in runner_rows_data), "runner refuses unsigned denominator/frame lock"),
        ("VAL2907_9_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2907_6_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "local-GR/Newton claims remain blocked"),
        ("VAL2907_10_anti_circling_decision", any(row["decision_id"] == "DEC2907_3_anti_circling" and row["decision"] == "DO_NOT_RETRY_MHREF_UNTIL_MAT2462_EXISTS" for row in decision_rows_data), "anti-circling MHref decision is explicit"),
        ("VAL2907_11_next_target_2908", any(row["route_id"] == "NEXT2907_0_2908" and row["selected"] for row in next_rows_data), "2908 parent-action skeleton target selected"),
        ("VAL2907_12_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2907_13_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2907_14_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2907_OVERALL", overall, "2907 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2907 - Y5 R2FR MHref/Tau/Source-Frame/Surface Lock or First Denominator Row Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row-under-AX1090`",
        "Status: `Y5_R2FR_2907_denominator_frame_lock_not_promoted_first_rows_staged_anti_circling_2908_next`",
        "Claim ceiling: `denominator_source_rows_nonclaim_only_no_MHref_no_Y5Y6_scoring_no_PPN_no_R10_no_Newton_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2907 tries the denominator/frame/surface route selected by 2906. It does not promote `M_H_ref`, `tau_frame_lock`, `observed_coframe_lock`, `surface_homology_lock`, or `source_worldtube_bridge` to a current MTS theorem.",
        "",
        "The useful result is anti-circularity. The contract is clear enough to use as a gate, but the current corpus still lacks the parent action, total charge, integrability, fixed reference, source bridge and positivity material required by the old 2462 final block. So this checkpoint stages first denominator rows and refuses to score Y5/Y6 from them.",
        "",
        "That means we should not keep punching the same `M_H_ref` wall. The next move is constructive: write the smallest parent-action skeleton that could own `q_loc`, `Gamma/Khat`, `Pi_M/worldtube`, Y5 source normalization and Y6 extra-stress coupling in one branch.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Denominator Frame Lock Audit",
        "",
        md_table(all_rows["audit"], ["audit_id", "required_clause", "current_status", "mathematical_form", "reason", "residual_if_missing", "valid_for_claim"]),
        "",
        "## First Denominator Source Rows",
        "",
        md_table(all_rows["rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is not a defeat; it is a refusal to launder Newton back into the proof. The old Hamiltonian denominator route is mathematically legitimate as a contract, but current MTS cannot spend it without new parent-action material. The practical gain is that every denominator ingredient is now an explicit row rather than a background excuse.",
        "",
        "So the project is closer in the useful sense: the next derivation does not need to ask 'why local GR?' in the abstract. It must build or reject one parent action that owns the local residual, source bridge and Y5/Y6 coupling channels.",
        "",
        "## Forbidden Claims From 2907",
        "",
        "- `M_H_ref` is positive, same-frame or source-backed for current MTS.",
        "- `tau_frame_lock`, `observed_coframe_lock`, or `surface_homology_lock` is parent-signed.",
        "- Y5/Y6 source split rows are score-ready.",
        "- Observed orbital GM may be used as denominator/proof input.",
        "- Source-normalized Newton, PPN, R10, clock, orbital or local GR is proved.",
        "- The Hamiltonian denominator route may be retried without MAT2462 parent-action material.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["audit"] = audit_rows()
    all_rows["rows"] = source_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "audit", "rows", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2907_OVERALL")
    print(f"2907 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
