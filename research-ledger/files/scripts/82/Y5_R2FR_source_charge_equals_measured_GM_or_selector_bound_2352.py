from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_CHARGE_MEASURED_GM_SYNTHESIS_2352"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md"

PATHS = {
    "2351_doc": ROOT / "2351-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
    "2351_validation": OUT / "P8_Y5_BRR545_2351_VALIDATION.csv",
    "2351_source_measure": OUT / "P8_Y5_PARENT_QLOC_2351_SOURCE_MEASURE_BRIDGE_TARGET.csv",
    "2351_residual_handoff": OUT / "P8_Y5_PARENT_QLOC_2351_RESIDUAL_CHARGE_HANDOFF.csv",
    "2351_htau_href": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
    "2342_doc": ROOT / "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
    "2342_bridge": OUT / "P8_Y5_PARENT_QLOC_2342_SOURCE_GM_BRIDGE_AUDIT.csv",
    "2342_selector_contract": OUT / "P8_Y5_PARENT_QLOC_2342_SELECTOR_SOURCE_MEASURE_CONTRACT.csv",
    "2342_bounds": OUT / "P8_Y5_PARENT_QLOC_2342_SELECTOR_BOUND_ROWS.csv",
    "2343_doc": ROOT / "2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md",
    "2343_nospecies": OUT / "P8_Y5_PARENT_QLOC_2343_NOSOURCEONLYSPECIES_AUDIT.csv",
    "2343_same_frame": OUT / "P8_Y5_PARENT_QLOC_2343_SAME_FRAME_GM_DESCENT_AUDIT.csv",
    "2344_doc": ROOT / "2344-Y5-R2FR-parent-source-blind-matter-functor-current-owner-or-sourceGM-bound.md",
    "2344_functor": OUT / "P8_Y5_PARENT_QLOC_2344_PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION.csv",
    "2344_current_owner": OUT / "P8_Y5_PARENT_QLOC_2344_CURRENT_OWNER_DERIVATION_AUDIT.csv",
    "2344_bounds": OUT / "P8_Y5_PARENT_QLOC_2344_SOURCEGM_BOUND_ACQUISITION_SCHEMA.csv",
    "2345_doc": ROOT / "2345-Y5-R2FR-current-owner-normal-form-from-parent-variation-or-sourceGM-residual-first-row.md",
    "2345_normal_form": OUT / "P8_Y5_PARENT_QLOC_2345_CURRENT_OWNER_NORMAL_FORM_AUDIT.csv",
    "2345_residual": OUT / "P8_Y5_PARENT_QLOC_2345_SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW.csv",
    "2346_doc": ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md",
    "2346_zero": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_SOURCE_PROJECTION_ZERO_AUDIT.csv",
    "2346_components": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
    "2346_priority": OUT / "P8_Y5_PARENT_QLOC_2346_COMPONENT_PRIORITY_LEDGER.csv",
    "2347_srng": OUT / "P8_Y5_PARENT_QLOC_2347_SRNG_ADOPTION_AND_SCOPE_AUDIT.csv",
    "2348_spin": OUT / "P8_Y5_PARENT_QLOC_2348_SPIN_CONNECTION_COFRAME_OWNED_AUDIT.csv",
    "2349_projective": OUT / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_TRACE_SILENCE_AUDIT.csv",
    "2350_boundary": OUT / "P8_Y5_PARENT_QLOC_2350_BOUNDARY_IMPROVEMENT_ZERO_AUDIT.csv",
    "2350_stack": OUT / "P8_Y5_PARENT_QLOC_2350_PRIVATE_BRANCH_RESIDUAL_STACK.csv",
}

SOURCES = [
    ("SRC2352_00_2351_doc", "2351_doc", ["PCR2351_6_coupling_source_measure_priority", "NEXT2351_0"], "2351 selected source-charge/measured-GM bridge after parent-charge reconciliation"),
    ("SRC2352_01_2351_validation", "2351_validation", ["VAL2351_OVERALL", "PASS"], "2351 validation"),
    ("SRC2352_02_2351_source_measure", "2351_source_measure", ["SMB2351_0_target", "SELECTED_NEXT_DERIVATION_TARGET"], "2351 source-measure target rows"),
    ("SRC2352_03_2351_residual_handoff", "2351_residual_handoff", ["RCH2351_4_source_glue_coupling", "MAIN_LIVE_BOTTLENECK"], "2351 residual charge handoff"),
    ("SRC2352_04_2351_htau_href", "2351_htau_href", ["HHS2351_3_MHref", "MISSING_H_TAU_H_REF_MHREF"], "2351 M_H_ref status"),
    ("SRC2352_05_2342_doc", "2342_doc", ["SGM2342_6_verdict", "BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS"], "first source-GM bridge attempt"),
    ("SRC2352_06_2342_bridge", "2342_bridge", ["SGM2342_6_verdict", "BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS"], "machine-readable source-GM bridge audit"),
    ("SRC2352_07_2342_selector_contract", "2342_selector_contract", ["SSC2342_4_universal_G", "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT"], "selector/source-measure contract"),
    ("SRC2352_08_2342_bounds", "2342_bounds", ["SGB2342_3_total_bridge_abs", "MISSING_COMPONENT_INPUTS"], "selector/source-GM bound rows"),
    ("SRC2352_09_2343_doc", "2343_doc", ["NSS2343_5_verdict", "NOT_DERIVED_RETAIN_SOURCEGM_BOUND"], "NoSourceOnlySpeciesSlot attempt"),
    ("SRC2352_10_2343_nospecies", "2343_nospecies", ["NSS2343_5_verdict", "NOT_DERIVED_RETAIN_SOURCEGM_BOUND"], "relative source/species slot audit"),
    ("SRC2352_11_2343_same_frame", "2343_same_frame", ["SFGD2343_4_final", "DESCENT_NOT_DERIVED"], "same-frame GM descent audit"),
    ("SRC2352_12_2344_doc", "2344_doc", ["PSBF2344_6_verdict", "NOT_DERIVED_EXACT_CONTRACT_READY"], "source-blind functor/current-owner proof obligation"),
    ("SRC2352_13_2344_functor", "2344_functor", ["PSBF2344_6_verdict", "NOT_DERIVED_EXACT_CONTRACT_READY"], "parent source-blind functor proof rows"),
    ("SRC2352_14_2344_current_owner", "2344_current_owner", ["CO2344_5_verdict", "CURRENT_OWNER_NOT_PARENT_DERIVED"], "current-owner derivation audit"),
    ("SRC2352_15_2344_bounds", "2344_bounds", ["SGB2344_4_total", "MISSING_COMPONENT_INPUTS"], "sourceGM bound acquisition schema"),
    ("SRC2352_16_2345_doc", "2345_doc", ["CNF2345_6_verdict", "PARTIAL_THEOREM_NOT_CLOSED"], "current-owner normal-form attempt"),
    ("SRC2352_17_2345_normal_form", "2345_normal_form", ["CNF2345_1_hilbert_owner", "EXACT_CONDITIONAL_SUBTHEOREM"], "partial Hilbert-owner subtheorem"),
    ("SRC2352_18_2345_residual", "2345_residual", ["RCO2345_0_schema", "MISSING_COMPONENT_VALUES"], "first current-owner residual row"),
    ("SRC2352_19_2346_doc", "2346_doc", ["NHZ2346_5_verdict", "ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED"], "non-Hilbert source projection attempt"),
    ("SRC2352_20_2346_zero", "2346_zero", ["NHZ2346_5_verdict", "ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED"], "non-Hilbert source projection zero audit"),
    ("SRC2352_21_2346_components", "2346_components", ["NHC2346_5_no_cancellation", "ACTIVE_GUARD"], "non-Hilbert component bound pack"),
    ("SRC2352_22_2346_priority", "2346_priority", ["PRI2346_2_readout_third", "readout reentry"], "unclosed readout/source-label reentry priority"),
    ("SRC2352_23_2347_srng", "2347_srng", ["SRNG2347_4_verdict", "NOT_PROMOTED_PRIVATE_SCOPE_ONLY"], "private no-Gamma/SRNG narrowing"),
    ("SRC2352_24_2348_spin", "2348_spin", ["SPIN2348_6_verdict", "NOT_PUBLICLY_DERIVED_RETAIN_AXIAL_TORSION_P4_ROW"], "spin connection partial route"),
    ("SRC2352_25_2349_projective", "2349_projective", ["PROJ2349_5_verdict", "PRIVATE_ZERO_PUBLIC_FALLBACK_RETAINED"], "projective trace private zero/public fallback"),
    ("SRC2352_26_2350_boundary", "2350_boundary", ["BIC2350_7_verdict", "ZERO_THEOREM_NOT_DERIVED_RETAIN_P4_BOUNDARY_ROW"], "boundary/improvement current result"),
    ("SRC2352_27_2350_stack", "2350_stack", ["PRS2350_4_next_order", "ORDERED_BUT_NOT_CLOSED"], "ordered local-GR bridge stack"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2352_SOURCE_REGISTER.csv",
    "synthesis": OUT / "P8_Y5_PARENT_QLOC_2352_SOURCE_GM_SYNTHESIS_AUDIT.csv",
    "residuals": OUT / "P8_Y5_PARENT_QLOC_2352_BRIDGE_RESIDUAL_STATUS.csv",
    "selector_stack": OUT / "P8_Y5_PARENT_QLOC_2352_SELECTOR_BOUND_STACK.csv",
    "fork": OUT / "P8_Y5_PARENT_QLOC_2352_NEXT_FORK_DECISION.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2352_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2352_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2352_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2352_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2352_VALIDATION.csv",
}


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needles(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "source_key": key,
            "source_path": str(PATHS[key]),
            "exists": b(PATHS[key].exists()),
            "required_needles": ";".join(needles),
            "needles_found": b(has_needles(PATHS[key], needles)),
            "source_role": role,
            "valid_for_claim": "false",
        }
        for row_id, key, needles, role in SOURCES
    ]


def synthesis_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_0_target",
            "topic": "source charge equals measured GM after 2351",
            "result": "TARGET_REOPENED_WITH_FULL_CHAIN_CONTEXT",
            "finding": "2351 selected the bridge, but 2342 already proved the shortcut fails; 2352 consolidates all later narrowing rather than repeating 2342.",
            "remaining_gap": "source-measure equality, M_H_ref, readout no-reentry and Poisson/Gauss readout are still unsigned",
            "next_action": "select the cleanest remaining source-selector/readout no-reentry target",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_1_2342_bridge",
            "topic": "first source-GM bridge attempt",
            "result": "BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS",
            "finding": "2342 already decomposed measured GM into M_H_ref, worldtube selector, Hilbert/source equality, Poisson/Gauss and universal-G gates.",
            "remaining_gap": "none of those gates became claim-grade",
            "next_action": "reuse 2342 selector/bound stack as the source-GM scaffold",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_2_2343_2344_coupling",
            "topic": "relative source/species/profile coupling",
            "result": "CONDITIONAL_THEOREM_EXACT_PARENT_SIGNATURE_UNSIGNED",
            "finding": "a single common GM scale is calibratable, but relative source/species/profile weights survive unless the parent source-blind functor/current-owner normal form is signed.",
            "remaining_gap": "NoSourceOnlySpeciesSlot and common measure/current owner remain proof obligations",
            "next_action": "do not let measured GM absorb relative coupling residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_3_2345_partial_win",
            "topic": "Hilbert/coframe current owner",
            "result": "PARTIAL_THEOREM_RETAINED",
            "finding": "post-variation source rescaling is pruned: after a common matter action is selected, the Hilbert/coframe derivative is the ordinary matter source.",
            "remaining_gap": "pre-action weights, non-Hilbert tails and readout reentry remain live",
            "next_action": "preserve this as real progress without promoting it to local GR/Newton",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_4_2346_nonhilbert_pack",
            "topic": "non-Hilbert source projection",
            "result": "ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED",
            "finding": "the source-current obstruction is split into connection/spin, boundary/improvement, readout reentry and shadow/projector components with absolute-sum policy.",
            "remaining_gap": "component values and parent zero theorems are missing",
            "next_action": "do not hide non-Hilbert source projection inside fitted GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_5_2347_2350_squeeze",
            "topic": "connection/projective/boundary squeeze",
            "result": "PRIVATE_NARROWING_PUBLIC_FALLBACKS_RETAINED",
            "finding": "SRNG/OFC, coframe-owned spin and projective trace give useful private/conditional narrowing; boundary/improvement survives and needs parent charge/source-measure inputs.",
            "remaining_gap": "public spin/projective rows, boundary row, M_H_ref and source-measure equality remain nonclaim",
            "next_action": "treat connection progress as narrowing, not a source-GM pass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_6_live_bridge",
            "topic": "live source-GM bridge after all narrowing",
            "result": "NOT_CLOSED_BUT_NOW_FACTORISED",
            "finding": "the bridge is now an absolute residual vector, not a fog bank: M_H_ref, selector/source equality, relative sourceGM, current-owner NH, readout reentry and Poisson/Gauss.",
            "remaining_gap": "readout/source-selector no-reentry is the least-treated clean subgate after connection and boundary passes",
            "next_action": "2353 readout no-reentry/source-selector zero or component row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGS2352_7_verdict",
            "topic": "promote source charge equals measured GM",
            "result": "PROMOTION_REJECTED_NEXT_SUBGATE_SELECTED",
            "finding": "Current corpus does not prove measured GM equality, but it has isolated the remaining source-selector/readout reentry throat cleanly.",
            "remaining_gap": "source-selector/readout no-reentry, Poisson/Gauss and M_H_ref remain open",
            "next_action": "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_0_total",
            "residual": "epsilon_sourceGM_bridge_abs",
            "formula": "epsilon_MHref + epsilon_selector + epsilon_source_GM_rel + epsilon_current_owner_NH + epsilon_readout_reentry + epsilon_PG_orbit",
            "status": "ABSOLUTE_SUM_NONCLAIM",
            "why_live": "each component is either theorem-open or missing numeric/source-backed rows",
            "next_action": "bound or zero components one at a time; no sign cancellation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_1_MHref",
            "residual": "epsilon_MHref_missing_abs",
            "formula": "M_H_ref := H_tau[S_outer]-H_ref",
            "status": "MISSING_H_TAU_H_REF_MHREF",
            "why_live": "parent current chain, fixed reference, positivity and same-frame certificate are unsigned",
            "next_action": "carry from 2351; never fill from orbital GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_2_selector_source",
            "residual": "epsilon_selector_GM_abs",
            "formula": "abs(Delta_worldtube_domain)+abs(R_eq)/M_H_ref+abs(I_commutator)/M_H_ref+abs(B_zero_flux)/M_H_ref",
            "status": "MISSING_SELECTOR_SOURCE_EQUALITY",
            "why_live": "worldtube selector, Hilbert/topological equality and projector commutator are not closed",
            "next_action": "readout/source-selector no-reentry target plus R_eq/I_commutator parallel branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_3_relative_sourceGM",
            "residual": "epsilon_source_GM_rel_abs",
            "formula": "norm((I-P_common){w_A,kappa_A,J_A})",
            "status": "PARENT_SOURCE_BLIND_SIGNATURE_UNSIGNED",
            "why_live": "a single common scale is absorbable, relative source/species/profile weights are not",
            "next_action": "retain NoSourceOnlySpeciesSlot proof obligation or acquire sourceGM vector rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_4_current_owner_NH",
            "residual": "epsilon_current_owner_NH_abs",
            "formula": "||P_source[J_spin/torsion+J_boundary+J_readout+J_improvement+J_shadow+J_projector]|| / ||P_source[J_Hilbert]||",
            "status": "PARTIAL_HILBERT_WIN_NONHILBERT_LIVE",
            "why_live": "ordinary Hilbert owner is conditionally exact after action selection, but non-Hilbert tails remain",
            "next_action": "reuse 2346 component pack; source readout component is now sharpest unworked head",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_5_readout_reentry",
            "residual": "epsilon_readout_reentry_abs",
            "formula": "||K_readout_after_variation(source labels)|| or arena leakage coefficients",
            "status": "LIVE_SELECTED_NEXT",
            "why_live": "readout/source-worldtube kernels can recreate species/source labels after variation unless forbidden by parent functor",
            "next_action": "2353 zero theorem or component row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRS2352_6_PG_orbit",
            "residual": "epsilon_PG_orbit_abs",
            "formula": "same charge gives nabla^2 Phi=4*pi*G_ref rho_H and a_r=-G_ref M_H_ref/r^2",
            "status": "PARALLEL_NEWTON_READOUT_GATE",
            "why_live": "source equality alone is not the inverse-square orbital readout",
            "next_action": "parallel Poisson/Gauss-orbital bridge after source-selector gate",
            "valid_for_claim": "false",
        },
    ]


def selector_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_0_worldtube",
            "gate": "pre-readout source worldtube",
            "condition": "W_source=closure(supp J_H[tau]) with same observed frame and linked compact surfaces",
            "status": "CONDITIONAL_NOT_SIGNED",
            "residual_if_missing": "Delta_worldtube_domain",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_1_Hilbert_topological",
            "gate": "Hilbert/topological equality",
            "condition": "Pi_M J_H = J_M_top + dB_zero",
            "status": "MISSING_R_EQ_THEOREM_OR_BOUND",
            "residual_if_missing": "R_eq_integral/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_2_commutator",
            "gate": "projector/source commutator",
            "condition": "[d,Pi_M]J_H=0",
            "status": "MISSING_I_COMMUTATOR_THEOREM_OR_BOUND",
            "residual_if_missing": "I_commutator/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_3_readout",
            "gate": "readout no-reentry",
            "condition": "readout kernels act after source variation and cannot create source/species labelled active current",
            "status": "LIVE_SELECTED_NEXT",
            "residual_if_missing": "epsilon_readout_reentry_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_4_universal_G",
            "gate": "universal source-blind coupling",
            "condition": "only one common kappa/G mode, no relative source/species/range/frame coefficients",
            "status": "PARENT_SIGNATURE_UNSIGNED",
            "residual_if_missing": "epsilon_source_GM_rel_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBS2352_5_Poisson_Gauss",
            "gate": "same charge creates Newtonian orbital readout",
            "condition": "M_H_ref sources Poisson/Gauss monopole and orbital acceleration",
            "status": "PARALLEL_GATE_OPEN",
            "residual_if_missing": "epsilon_PG_orbit_abs",
            "valid_for_claim": "false",
        },
    ]


def fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORK2352_0_primary",
            "candidate": "readout no-reentry/source-selector zero",
            "decision": "SELECT_PRIMARY_NEXT",
            "reason": "connection and boundary were squeezed; readout/source-label reentry is the clean remaining source-measure head that can still hide coupling in measured GM",
            "next_target": "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORK2352_1_parallel",
            "candidate": "Poisson-Gauss orbital bridge",
            "decision": "KEEP_PARALLEL",
            "reason": "Newton recovery also needs the same charge to generate the inverse-square orbital field, but source-selector honesty comes first",
            "next_target": "2353b-Y5-R2FR-Poisson-Gauss-orbital-bridge-or-DeltaPG-row.md",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FORK2352_2_fallback",
            "candidate": "sourceGM residual vector acquisition",
            "decision": "KEEP_FALLBACK",
            "reason": "if readout/source-selector theorem-zero fails, build numeric rows instead of claiming equality",
            "next_target": "2353c-Y5-R2FR-sourceGM-residual-vector-acquisition-pack.md",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claim_gate_specs = [
        ("CG2352_0_2342_bridge", "source-charge equals measured GM theorem", "false", "2342/2352 both reject promotion"),
        ("CG2352_1_hilbert_owner_partial", "Hilbert owner after action selection", "true", "partial conditional theorem only; not local GR/Newton"),
        ("CG2352_2_MHref", "positive same-frame M_H_ref", "false", "H_tau/H_ref/M_H_ref missing"),
        ("CG2352_3_selector", "worldtube/source selector equality", "false", "selector/R_eq/I_commutator open"),
        ("CG2352_4_relative_sourceGM", "NoSourceOnlySpeciesSlot/source-blind coupling", "false", "parent signature unsigned"),
        ("CG2352_5_nonhilbert", "non-Hilbert source projection zero", "false", "component pack nonclaim"),
        ("CG2352_6_readout", "readout/source-label no-reentry", "false", "selected next target"),
        ("CG2352_7_Poisson_Gauss", "Poisson/Gauss/orbital readout", "false", "parallel Newton gate open"),
        ("CG2352_8_local_GR_Newton", "local GR/Newton source side recovered", "false", "requires all above public gates"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "passes_private_or_partial": partial,
            "passes_public_claim": "false",
            "why": why,
            "valid_for_claim": "false",
        }
        for row_id, gate, partial, why in claim_gate_specs
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2352_0_reclaim_2342",
            "shortcut": "repeat 2342 as if it proves measured-GM equality",
            "allowed": "false",
            "reason": "2342 explicitly rejected the bridge and staged nonclaim selector bounds",
            "source_rows": "SGM2342_6_verdict;VAL2342_OVERALL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2352_1_orbital_GM_backfill",
            "shortcut": "fill M_H_ref from observed orbital GM",
            "allowed": "false",
            "reason": "this borrows Newton before deriving Newton/source normalization",
            "source_rows": "HHS2351_4_anti_circularity_guard;PRS2350_3_anti_circularity",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2352_2_partial_owner_to_full",
            "shortcut": "Hilbert-owner partial theorem proves full current/source side",
            "allowed": "false",
            "reason": "pre-action weights, non-Hilbert tails and readout reentry survive",
            "source_rows": "CNF2345_6_verdict;NHZ2346_5_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2352_3_measured_G_absorbs_all",
            "shortcut": "measured G/GM absorbs every sourceGM residual",
            "allowed": "false",
            "reason": "one common mode can be calibrated, relative/source/profile/readout components cannot be hidden",
            "source_rows": "PSBF2344_4_common_mode;BRS2352_3_relative_sourceGM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2352_4_private_connection_to_public_sourceGM",
            "shortcut": "private connection narrowing proves public source-GM bridge",
            "allowed": "false",
            "reason": "SRNG/spin/projective progress narrows terms but public fallback rows and boundary/source-measure gates remain",
            "source_rows": "SRNG2347_4_verdict;SPIN2348_6_verdict;PROJ2349_5_verdict;BIC2350_7_verdict",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2352_0",
            "next_target": "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md",
            "why": "after the connection and boundary squeeze, readout/source-label reentry is the cleanest remaining source-measure obstruction that can hide coupling in measured GM",
            "route_type": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2352_1",
            "next_target": "2353b-Y5-R2FR-Poisson-Gauss-orbital-bridge-or-DeltaPG-row.md",
            "why": "parallel Newton route: even a correct source charge must still generate the Poisson/Gauss inverse-square readout",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2352_2",
            "next_target": "2353c-Y5-R2FR-sourceGM-residual-vector-acquisition-pack.md",
            "why": "fallback route if readout/source-selector proof fails: source the residual vector with units, bounds and arena maps",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_rows() -> list[dict[str, Any]]:
    copies = [
        (
            "COPY2352_0_synthesis",
            OUTPUTS["synthesis"],
            BETA_DOCS / "SOURCE_GM_SYNTHESIS_AUDIT_2352_NONCLAIM.csv",
            "beta-source source-GM synthesis notes",
        ),
        (
            "COPY2352_1_residuals",
            OUTPUTS["residuals"],
            MICRO_RESIDUALS / "SOURCE_GM_BRIDGE_RESIDUAL_STATUS_2352_NONCLAIM.csv",
            "local residual and WEP/PPN source-GM gate inputs",
        ),
        (
            "COPY2352_2_decision",
            OUTPUTS["fork"],
            RAB_QUEUE / "JR2352_SOURCE_GM_FORK_DECISION_NONCLAIM.csv",
            "RAB acquisition/derivation fork decision",
        ),
    ]
    rows = []
    for row_id, src, dst, purpose in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "purpose": purpose,
                "valid_for_claim": "false",
            }
        )
    return rows


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*2352*") if path.is_file()]


def validation_rows(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims = read_csv(OUTPUTS["claims"])
    residuals = read_csv(OUTPUTS["residuals"])
    synthesis = read_text(OUTPUTS["synthesis"])
    next_text = read_text(OUTPUTS["next"])
    produced = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows = [
        ("VAL2352_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2352_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2352_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2352 outputs written"),
        ("VAL2352_03_2342_not_duplicated", "SGS2352_1_2342_bridge" in synthesis, "2342 bridge imported as prior failed attempt"),
        ("VAL2352_04_partial_win_preserved", "SGS2352_3_2345_partial_win" in synthesis, "2345 Hilbert-owner partial theorem preserved"),
        ("VAL2352_05_residuals_nonclaim", residuals and all(row.get("valid_for_claim") == "false" for row in residuals), "bridge residual vector remains nonclaim"),
        ("VAL2352_06_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2352_07_next_selected", "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md" in next_text, "readout no-reentry/source-selector target selected"),
        ("VAL2352_08_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2352_09_formalization_untouched", not formalization_hits(), "no 2352 checkpoint output appears in formalization-workbench"),
        ("VAL2352_10_no_claim_flags", "valid_for_claim,true" not in "".join(read_text(path) for path in produced), "no generated row is valid_for_claim=true"),
        ("VAL2352_11_no_github_policy", True, "public GitHub update not recommended from 2352"),
    ]
    output = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in rows
    ]
    overall = all(row["status"] == "PASS" for row in output)
    output.append(
        {
            "row_id": "VAL2352_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2352 synthesizes the source-GM bridge chain, preserves the 2345 partial theorem, rejects promotion, and selects readout no-reentry/source-selector as 2353.",
            "valid_for_claim": "false",
        }
    )
    return output


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |\n"
    separator = "| " + " | ".join("---" for _ in columns) + " |\n"
    body = ""
    for row in rows:
        body += "| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |\n"
    return header + separator + body


def write_doc(
    sources: list[dict[str, Any]],
    synthesis: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    selector_stack: list[dict[str, Any]],
    fork: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    content = f"""# 2352 — Y5 R2FR Source Charge Equals Measured GM Or Selector Bound

Generated: `{now}`

## Summary

2352 is a synthesis checkpoint after 2351 reopened the source-charge/measured-GM bridge. The important finding is
that this bridge was already attacked in 2342 and then refined through 2343–2346. The later 2347–2351 sequence did
not make that work obsolete; it narrowed the connection and boundary sides and showed what still survives.

Current verdict: **measured `GM` equality is not derived**, but the coupling problem is now factorised. The clean
partial win is the 2345 Hilbert-owner subtheorem: once the ordinary matter action is selected and variation happens
before readout, the Hilbert/coframe derivative is the ordinary matter source. The live source-GM blockers are
pre-action/source-blind syntax, non-Hilbert tails, readout/source-selector reentry, `M_H_ref`, and Poisson/Gauss readout.

The next best derivation target is therefore **readout no-reentry / source-selector zero**, not GitHub, not empirical
scoring, and not another generic “connect to GR” pass.

## Output Files

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["synthesis"]}`
- `{OUTPUTS["residuals"]}`
- `{OUTPUTS["selector_stack"]}`
- `{OUTPUTS["fork"]}`
- `{OUTPUTS["claims"]}`
- `{OUTPUTS["refusal"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["copies"]}`
- `{OUTPUTS["validation"]}`

## Source Register

{table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Source-GM Synthesis Audit

{table(synthesis, ["row_id", "topic", "result", "finding", "remaining_gap", "next_action", "valid_for_claim"])}

## Bridge Residual Status

{table(residuals, ["row_id", "residual", "status", "why_live", "next_action", "valid_for_claim"])}

## Selector Bound Stack

{table(selector_stack, ["row_id", "gate", "condition", "status", "residual_if_missing", "valid_for_claim"])}

## Next Fork Decision

{table(fork, ["row_id", "candidate", "decision", "reason", "next_target", "valid_for_claim"])}

## Claim Gates

{table(claims, ["row_id", "gate", "passes_private_or_partial", "passes_public_claim", "why", "valid_for_claim"])}

## Refusal Runner

{table(refusal, ["row_id", "shortcut", "allowed", "reason", "source_rows", "valid_for_claim"])}

## Next Targets

{table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Working Read

This is where the project looks better than it did several passes ago. We do **not** have local GR/Newton yet, but we
do have a much sharper map of what must be true. The bridge is no longer “maybe the coupling is wrong”; it is:

`M_H_ref + selector/source equality + relative sourceGM silence + non-Hilbert source projection silence + readout no-reentry + Poisson/Gauss`.

That is a hard list, but it is a real list. The next useful strike is to prove that readout/source-worldtube maps cannot
recreate source/species labels after variation, or else turn that leakage into a first explicit component row.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    synthesis = synthesis_rows()
    residuals = residual_rows()
    selector_stack = selector_stack_rows()
    fork = fork_rows()
    claims = claim_gate_rows()
    refusal = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["synthesis"], synthesis)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["selector_stack"], selector_stack)
    write_csv(OUTPUTS["fork"], fork)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_targets)
    copies = copy_rows()
    write_csv(OUTPUTS["copies"], copies)
    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, synthesis, residuals, selector_stack, fork, claims, refusal, next_targets, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["row_id"] for row in failed)
        raise SystemExit(f"2352 validation failed: {failed_ids}")
    print(f"2352 checkpoint written: {DOC}")


if __name__ == "__main__":
    main()
