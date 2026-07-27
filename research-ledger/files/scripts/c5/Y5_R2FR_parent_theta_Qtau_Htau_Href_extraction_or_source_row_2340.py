from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_THETA_QTAU_HTAU_HREF_EXTRACTION_OR_SOURCE_ROW_2340"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md"

PATHS = {
    "2339_doc": ROOT / "2339-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
    "2339_validation": OUT / "P8_Y5_BRR545_2339_VALIDATION.csv",
    "2339_next": OUT / "P8_Y5_PARENT_QLOC_2339_NEXT_TARGET.csv",
    "2339_mhref": OUT / "P8_Y5_PARENT_QLOC_2339_MHREF_FIRST_ROW.csv",
    "1006_doc": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1008_doc": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
    "1009_doc": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "1016_doc": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "parent_noether_chain": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
    "qtau_decomposition": OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
    "owner_audit_771": OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "noether_test_771": OUT / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
    "integrability_664": OUT / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "mhref_683": OUT / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
    "sector_contract_1009": OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
}

SOURCES = [
    ("SRC2340_00_2339_doc", "2339_doc", PATHS["2339_doc"], ["TQF2339_8_verdict", "MHR2339_0_first_row"], "2339 handoff: parent charge and M_H_ref first-row blocker"),
    ("SRC2340_01_2339_validation", "2339_validation", PATHS["2339_validation"], ["VAL2339_OVERALL", "PASS"], "2339 validation"),
    ("SRC2340_02_2339_next", "2339_next", PATHS["2339_next"], ["NEXT2339_0", "parent-theta-Qtau-Htau-Href"], "machine-readable 2340 target"),
    ("SRC2340_03_2339_mhref", "2339_mhref", PATHS["2339_mhref"], ["MHR2339_0_first_row", "MISSING_H_TAU"], "M_H_ref source-row schema"),
    ("SRC2340_04_1006_doc", "1006_doc", PATHS["1006_doc"], ["MHA1006_1_integrability", "MHS1006_0_Htau_minus_Href"], "positive same-frame denominator prior"),
    ("SRC2340_05_1007_doc", "1007_doc", PATHS["1007_doc"], ["HTA1007_0_target", "SRS1007_0_integrability_formula"], "H_tau integrability/fixed-reference rule"),
    ("SRC2340_06_1008_doc", "1008_doc", PATHS["1008_doc"], ["PVA1008_1_theta_MTS", "QTA1008_8_Q_total"], "theta/Q_tau extraction audit"),
    ("SRC2340_07_1009_doc", "1009_doc", PATHS["1009_doc"], ["PCS1009_9_total_parent_contract", "CG1009_2_Qtau_MTS"], "parent sector current-chain contract"),
    ("SRC2340_08_1016_doc", "1016_doc", PATHS["1016_doc"], ["PSC1016_5_dressed_source_charge", "FIS1016_0_M_H_ref"], "dressed source charge bridge"),
    ("SRC2340_09_parent_noether_chain", "parent_noether_chain", PATHS["parent_noether_chain"], ["D505_2_charge_form", "Q_M["], "parent charge-form chain"),
    ("SRC2340_10_qtau_decomposition", "qtau_decomposition", PATHS["qtau_decomposition"], ["QDEC993_5_total", "not_promoted"], "current Q_tau piece ledger"),
    ("SRC2340_11_owner_audit_771", "owner_audit_771", PATHS["owner_audit_771"], ["TQ771_0_parent_variation", "TQ771_6_owner_verdict"], "theta/Q_tau owner audit"),
    ("SRC2340_12_noether_test_771", "noether_test_771", PATHS["noether_test_771"], ["NET771_0_parent_variation", "NET771_4_verdict"], "Noether extraction test"),
    ("SRC2340_13_integrability_664", "integrability_664", PATHS["integrability_664"], ["HCI664_0_target", "HCI664_2_parent_symplectic_current"], "H_tau integrability attempt"),
    ("SRC2340_14_mhref_683", "mhref_683", PATHS["mhref_683"], ["MH683_0_definition", "M_H_ref := H_tau"], "M_H_ref denominator attempt"),
    ("SRC2340_15_sector_contract_1009", "sector_contract_1009", PATHS["sector_contract_1009"], ["PCS1009_0_EH_core", "PCS1009_9_total_parent_contract"], "machine-readable sector contract"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2340_SOURCE_REGISTER.csv",
    "spine": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
    "sector_matrix": OUT / "P8_Y5_PARENT_QLOC_2340_SECTOR_EXTRACTION_MATRIX.csv",
    "htau_href_row": OUT / "P8_Y5_PARENT_QLOC_2340_HTAU_HREF_SOURCE_ROW.csv",
    "residual_split": OUT / "P8_Y5_PARENT_QLOC_2340_EH_ANCHOR_RESIDUAL_SPLIT.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2340_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2340_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2340_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2340_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2340_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2340_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2340_0_spine", OUTPUTS["spine"], BETA_DOCS / "PARENT_CHARGE_EXTRACTION_SPINE_2340_NONCLAIM.csv"),
    ("COPY2340_1_htau_href", OUTPUTS["htau_href_row"], MICRO_RESIDUALS / "HTAU_HREF_SOURCE_ROW_2340_NONCLAIM.csv"),
    ("COPY2340_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2340_PARENT_CHARGE_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_spine_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_0_parent_split",
            "step": "parent Lagrangian split",
            "formula": "L_parent=L_EH[g_obs;kappa0,Lambda0]+L_matter[psi,g_obs]+dB_ref+L_extra+L_projector+L_glue",
            "meaning": "separates the EH anchor from exactly the retained MTS/coupling/source sectors that can spoil local GR",
            "current_status": "CONTRACT_SHARPENED_NOT_SIGNED",
            "required_to_promote": "single source path with field list, variation variables, boundary class and coupling descent",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_1_variation",
            "step": "first variation",
            "formula": "delta L_parent=sum_i E_i delta Phi_i + d(theta_EH+theta_matter+delta B_ref+theta_extra+theta_projector+theta_glue)",
            "meaning": "defines theta_MTS without hiding non-EH sectors",
            "current_status": "TEMPLATE_EXACT_SECTOR_VARIATIONS_MISSING",
            "required_to_promote": "theta contribution and Euler/stress contribution for every retained sector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_2_Noether_current",
            "step": "tau Noether current",
            "formula": "J_tau=theta_MTS(Phi,L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "meaning": "turns time flow into a parent charge rather than a fitted mass label",
            "current_status": "FORMAL_SHAPE_OWNERSHIP_MISSING",
            "required_to_promote": "tau action on metric, matter, boundary/reference, extra, projector and glue fields",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_3_charge_decomposition",
            "step": "charge split",
            "formula": "Q_tau^MTS=Q_tau^EH+Q_tau^matter+Q_tau^boundary/ref+Q_tau^extra+Q_tau^projector+Q_tau^glue",
            "meaning": "the charge can be EH only when all non-EH pieces are derived zero, topological, fixed, or bounded",
            "current_status": "EH_ANCHOR_PLUS_RESIDUAL_VECTOR",
            "required_to_promote": "each non-EH charge piece has source/equation path and zero/bound status",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_4_Htau_variation",
            "step": "Hamiltonian variation",
            "formula": "delta H_tau[S]=integral_S(delta Q_tau^MTS-i_tau theta_MTS)",
            "meaning": "this is the exact object needed before M_H_ref can be real",
            "current_status": "INTEGRABILITY_BLOCKED",
            "required_to_promote": "closed one-form on field space plus fixed boundary/reference branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_5_reference",
            "step": "fixed reference",
            "formula": "H_ref=H_tau[S_ref;reference_class] fixed before source/readout; d_readout H_ref=0",
            "meaning": "prevents H_ref from becoming a cancellation knob",
            "current_status": "MISSING_FIXED_REFERENCE_SOURCE",
            "required_to_promote": "reference selector, counterterm convention, timestamp/derivation and no-cancellation guard",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_6_MHref",
            "step": "source denominator",
            "formula": "M_H_ref=H_tau[S_outer]-H_ref",
            "meaning": "normalizes Bzero, R_eq, I_commutator and PPN residuals without borrowing orbital GM",
            "current_status": "FIRST_ROW_READY_VALUES_MISSING",
            "required_to_promote": "finite positive same-frame H_tau and H_ref with source/equation paths",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCS2340_7_local_limit",
            "step": "local GR/Newton limit",
            "formula": "Delta_charge_res=0 and M_H_ref -> Poisson/Gauss source charge imply EH local field equations and Newtonian inverse-square readout",
            "meaning": "the target is no longer vague: prove residual charge silence and source-charge equality, or bound their vector",
            "current_status": "DERIVATION_ROUTE_EXACT_BUT_UNSIGNED",
            "required_to_promote": "residual zero/bound theorem plus source-measure bridge",
            "valid_for_claim": "false",
        },
    ]


def build_sector_matrix() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_0_EH_anchor",
            "sector": "EH anchor",
            "theta_piece": "theta_EH",
            "Q_piece": "Q_tau^EH",
            "owned_status": "conditional_reference",
            "missing_to_claim": "constant kappa0, fixed Lambda subtraction, and proof retained MTS sectors reduce/silence",
            "residual_if_missing": "Delta_EH_anchor",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_1_matter",
            "sector": "universal matter/source",
            "theta_piece": "theta_matter plus Hilbert source current",
            "Q_piece": "C_tau^matter/source glue",
            "owned_status": "conditional_source_input",
            "missing_to_claim": "same observed coframe, matter descent, source Ward identity and no species-dependent extra coupling",
            "residual_if_missing": "Delta_frame_source;B_obs_source_measure_over_MH",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_2_boundary_reference",
            "sector": "boundary/reference",
            "theta_piece": "delta B_ref + theta_boundary",
            "Q_piece": "Q_tau^boundary/ref",
            "owned_status": "fixed_reference_missing",
            "missing_to_claim": "fixed-before-readout reference selector and improvement ambiguity certificate",
            "residual_if_missing": "Delta_ref;B_zero_flux;Delta_symp",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_3_GK_extra",
            "sector": "Gamma/Khat/q_loc extra",
            "theta_piece": "theta_GK",
            "Q_piece": "Q_tau^extra",
            "owned_status": "hard_fail_current_claim",
            "missing_to_claim": "Helmholtz-compatible S_GK, Euler closure, double zero and boundary no-flux",
            "residual_if_missing": "Delta_GK_charge;Delta_q_loc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_4_projector",
            "sector": "Pi_M/source projector",
            "theta_piece": "theta_projector",
            "Q_piece": "Q_tau^projector+[d,Pi_M]J_H",
            "owned_status": "not_parent_derived",
            "missing_to_claim": "parent symplectic projector algebra, product variation and measured-GM calibration",
            "residual_if_missing": "R_eq_integral;I_commutator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_5_worldtube_glue",
            "sector": "worldtube/source glue",
            "theta_piece": "theta_glue",
            "Q_piece": "Q_tau^glue or source constraint",
            "owned_status": "core_missing_piece",
            "missing_to_claim": "pre-readout source support, compact linking surfaces, M_H_ref and boundary/reference lock",
            "residual_if_missing": "Delta_worldtube_domain;epsilon_selector_Meff",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SEM2340_6_total",
            "sector": "total parent charge",
            "theta_piece": "theta_MTS=sum sector pieces",
            "Q_piece": "Q_tau^MTS=sum sector pieces",
            "owned_status": "not_promoted",
            "missing_to_claim": "all sector rows parent-signed or explicitly residualized with finite bounds",
            "residual_if_missing": "epsilon_parent_charge_abs",
            "valid_for_claim": "false",
        },
    ]


def build_htau_href_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2340_0_source_row",
            "quantity": "H_tau_H_ref_source_row",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref",
            "required_columns": "system_id;tau_id;coframe_id;surface_outer;surface_ref;theta_source;Q_tau_source;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;reference_rule;counterterm_convention;integrability_certificate;no_orbital_GM_import;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_THETA_SOURCE;MISSING_Q_TAU_SOURCE;MISSING_H_TAU;MISSING_H_REF;MISSING_M_H_REF",
            "runner_rule": "claim_allowed only if all numeric/source/certificate fields are present, same-frame, positive and not orbital-GM backfilled",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2340_1_integrability_component_row",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "formula": "abs(delta^2 H_tau)/M_H_ref or finite obstruction component from non-closed field-space one-form",
            "required_columns": "system_id;component_id;delta_H_tau_nonintegrable;M_H_ref;units;theta_source;Q_tau_source;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_INTEGRABILITY_COMPONENT",
            "runner_rule": "if theorem-zero fails, this becomes an absolute residual component not a pass",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2340_2_reference_component_row",
            "quantity": "Delta_ref_over_MH",
            "formula": "abs(H_ref_shift_or_unfixed_counterterm)/M_H_ref",
            "required_columns": "system_id;reference_rule;counterterm_convention;H_ref_shift;M_H_ref;units;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_FIXED_REFERENCE_COMPONENT",
            "runner_rule": "unfixed or fitted reference is a residual, never a cancellation",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2340_3_charge_residual_row",
            "quantity": "epsilon_parent_charge_abs",
            "formula": "abs(Delta_H_res)/M_H_ref + abs(Delta_ref)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref",
            "required_columns": "system_id;Delta_H_res;Delta_ref;B_zero_flux;Delta_symp;M_H_ref;units;component_sources;no_cancellation_guard;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "runner_rule": "absolute-sum residual vector; no sign cancellation allowed",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_residual_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ERS2340_0_EH_anchor_law",
            "split_law": "Q_tau^MTS=Q_tau^EH+Delta_Q_res",
            "meaning": "use GR as the comparison shape without smuggling it as the proof",
            "zero_condition": "Delta_Q_res=0 from parent sector certificates, not from assumption",
            "fallback_bound": "epsilon_Qres_abs=abs(integral_S Delta_Q_res)/M_H_ref",
            "status": "ANCHOR_LAW_EXACT_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ERS2340_1_Htau_split",
            "split_law": "delta H_tau^MTS=delta H_tau^EH+integral_S(delta Delta_Q_res-i_tau theta_res)",
            "meaning": "local GR follows only if the residual Hamiltonian variation vanishes or is bounded below PPN/local thresholds",
            "zero_condition": "theta_res and Delta_Q_res have parent-signed silence/topological/fixed-boundary clauses",
            "fallback_bound": "epsilon_Hres_abs",
            "status": "RESIDUAL_VARIATION_LAW_STAGED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ERS2340_2_MHref_split",
            "split_law": "M_H_ref=M_EH_ref+Delta_M_res",
            "meaning": "the same denominator can compare GR/Newton against MTS without hiding normalization drift",
            "zero_condition": "Delta_M_res=0 plus source-measure bridge",
            "fallback_bound": "abs(Delta_M_res)/M_H_ref",
            "status": "DENOMINATOR_SPLIT_STAGED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ERS2340_3_Newton_bridge",
            "split_law": "M_H_ref -> Poisson/Gauss source -> orbital GM",
            "meaning": "Newton is recovered only after the Hamiltonian charge is shown to be the source of the inverse-square field",
            "zero_condition": "R_eq=I_commutator=B_zero_flux=Delta_worldtube_domain=0 or bounded",
            "fallback_bound": "epsilon_selector_Meff plus PPN residual vector",
            "status": "BRIDGE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2340_0_extraction_result",
            "decision": "do not promote parent theta/Q_tau/H_tau/H_ref",
            "reason": "2340 constructs the exact extraction spine but sector theta/Q pieces, fixed H_ref and H_tau integrability remain unsigned",
            "consequence": "M_H_ref and local-GR/Newton claims stay blocked",
            "status": "EXTRACTION_SPINE_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2340_1_real_progress",
            "decision": "use EH-anchor residual split as the next derivation map",
            "reason": "this avoids both extremes: no GR smuggling, no vague all-or-nothing parent action demand",
            "consequence": "prove or bound Delta_Q_res, Delta_H_res and Delta_M_res sector by sector",
            "status": "EH_ANCHOR_RESIDUAL_ROUTE_SELECTED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2340_2_coupling_priority",
            "decision": "treat coupling/source-measure as co-equal with GK residual silence",
            "reason": "even a perfect local residual zero does not prove measured GM unless the Hamiltonian charge is the matter/source charge",
            "consequence": "next proof must hit residual charge silence and source-charge equality together",
            "status": "COUPLING_KEY_CONFIRMED_AS_STRUCTURAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2340_3_public_policy",
            "decision": "no GitHub update from 2340",
            "reason": "this is a private derivation map and claim gate, not a public result",
            "consequence": "continue private goal until derived/conditional/blocked public checkpoint is clean",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2340_0_parent_spine", "parent extraction spine complete", "false", "spine is exact but not sector-signed"),
        ("CG2340_1_sector_theta_Q", "all sector theta/Q pieces owned", "false", "non-EH sectors remain missing or residualized"),
        ("CG2340_2_Htau_integrability", "H_tau integrability derived", "false", "field-space one-form closure and fixed reference not proved"),
        ("CG2340_3_Href_fixed", "H_ref fixed before readout", "false", "reference selector/counterterm source missing"),
        ("CG2340_4_MHref", "positive same-frame M_H_ref exists", "false", "H_tau/H_ref source row remains unfilled"),
        ("CG2340_5_Newton_GR", "GR/Newton local limit derived", "false", "residual charge/source-measure bridge not proved"),
        ("CG2340_6_github", "safe public GitHub update", "false", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "passed": passed,
            "claim_effect": effect,
            "valid_for_claim": "false",
        }
        for row_id, gate, passed, effect in gates
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2340_0_EH_total",
            "claim": "set Q_tau^MTS=Q_tau^EH without residual certificates",
            "allowed": "false",
            "reason": "EH is the anchor, not the total MTS proof; Delta_Q_res must be zero or bounded",
            "blocking_rows": "PCS2340_3_charge_decomposition;ERS2340_0_EH_anchor_law;CG2340_1_sector_theta_Q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2340_1_reference_cancellation",
            "claim": "absorb residual charge into H_ref",
            "allowed": "false",
            "reason": "H_ref must be fixed before readout and cannot cancel source/radius/frame residuals",
            "blocking_rows": "PCS2340_5_reference;HHS2340_2_reference_component_row;CG2340_3_Href_fixed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2340_2_orbital_backfill",
            "claim": "fill M_H_ref from orbital GM now",
            "allowed": "false",
            "reason": "Poisson/Gauss/orbital bridge must be derived before orbital GM can calibrate the denominator",
            "blocking_rows": "PCS2340_6_MHref;ERS2340_3_Newton_bridge;CG2340_4_MHref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2340_3_sign_cancellation",
            "claim": "let residual components cancel by sign",
            "allowed": "false",
            "reason": "the local-GR gate needs an absolute-sum residual vector unless a parent identity proves exact cancellation",
            "blocking_rows": "HHS2340_3_charge_residual_row;ERS2340_1_Htau_split",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2340_4_local_claim",
            "claim": "2340 proves GR/Newton recovery",
            "allowed": "false",
            "reason": "2340 defines the route and source rows; it does not close residual charge silence or source-measure equality",
            "blocking_rows": "CG2340_5_Newton_GR;DEC2340_0_extraction_result",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2340_0",
            "next_target": "2341-Y5-R2FR-EH-anchor-residual-charge-zero-or-coefficient-row.md",
            "why": "the next leap is to prove Delta_Q_res=0/Delta_H_res=0 from the retained non-EH sectors, or create coefficient rows for the residual charge vector.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2340_1",
            "next_target": "2341b-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
            "why": "GR/Newton recovery also needs the Hamiltonian charge to be the measured source charge, not merely a conserved charge.",
            "claim_status": "parallel_coupling_source_measure_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2340_2",
            "next_target": "2341c-Y5-R2FR-Htau-Href-source-row-runner.md",
            "why": "fallback route: keep derivation honest by filling H_tau/H_ref/M_H_ref source rows as nonclaim data.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied_rows = read_csv_rows(destination)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": str(len(copied_rows)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    spine: list[dict[str, Any]],
    sector_matrix: list[dict[str, Any]],
    htau_href: list[dict[str, Any]],
    residual_split: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL2340_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"))
    validations.append(("VAL2340_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"))
    validations.append(("VAL2340_02_spine_written", len(spine) >= 8 and any(row["row_id"] == "PCS2340_7_local_limit" for row in spine), "parent charge extraction spine includes local-limit law"))
    validations.append(("VAL2340_03_sector_matrix_complete", len(sector_matrix) >= 7 and any(row["row_id"] == "SEM2340_6_total" for row in sector_matrix), "sector matrix covers EH, matter, boundary, extra, projector, glue and total"))
    validations.append(("VAL2340_04_htau_href_rows_nonready", len(htau_href) >= 4 and all(row["score_ready"] == "false" for row in htau_href), "Htau/Href source rows remain non-score-ready"))
    validations.append(("VAL2340_05_residual_split_written", len(residual_split) >= 4 and any("Delta_Q_res" in row["split_law"] for row in residual_split), "EH-anchor residual split is written"))
    validations.append(("VAL2340_06_claim_gates_blocked", all(row["passed"] == "false" for row in claims), "all claim gates remain blocked"))
    validations.append(("VAL2340_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal), "shortcut claims refused"))
    validations.append(("VAL2340_08_next_selected", any("2341-Y5-R2FR-EH-anchor-residual-charge-zero" in row["next_target"] for row in next_rows), "2341 residual charge zero target recorded"))
    validations.append(("VAL2340_09_coupling_priority_recorded", any(row["status"] == "COUPLING_KEY_CONFIRMED_AS_STRUCTURAL" for row in decision), "coupling/source-measure priority recorded"))
    validations.append(("VAL2340_10_github_blocked", any(row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision), "public GitHub update not recommended from 2340"))
    validations.append(("VAL2340_11_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copies), "branch copies exist and parse"))

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths.extend(destination for _, _, destination in BRANCH_COPY_SPECS)
    validations.append(("VAL2340_12_outputs_exist", all(path.exists() for path in generated_paths), "CSV outputs and branch copies exist before doc render"))

    no_claim_flags = True
    for path in [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]:
        if path.exists() and path.suffix == ".csv":
            rows = read_csv_rows(path)
            if any(row.get("valid_for_claim", "").lower() == "true" for row in rows):
                no_claim_flags = False
                break
    validations.append(("VAL2340_13_no_claim_flags", no_claim_flags, "no generated row is valid_for_claim=true"))

    formalization_clean = not any(FORMALIZATION.rglob("*2340*")) if FORMALIZATION.exists() else True
    validations.append(("VAL2340_14_formalization_untouched_by_2340", formalization_clean, "no 2340 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in validations
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2340_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2340 builds an exact EH-anchor parent charge extraction spine, stages H_tau/H_ref source rows, refuses shortcut promotion, and selects residual charge zero/source-measure next.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    spine: list[dict[str, Any]],
    sector_matrix: list[dict[str, Any]],
    htau_href: list[dict[str, Any]],
    residual_split: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2340 - parent theta/Q_tau/H_tau/H_ref extraction or source row

## Summary

2340 turns the 2339 blocker into a sharper derivation map.

The useful leap is the EH-anchor residual split:

`Q_tau^MTS = Q_tau^EH + Delta_Q_res`,

`delta H_tau^MTS = delta H_tau^EH + integral_S(delta Delta_Q_res - i_tau theta_res)`,

`M_H_ref = M_EH_ref + Delta_M_res`.

This does not claim GR/Newton recovery. It makes the required proof exact: either derive `Delta_Q_res = 0`,
`Delta_H_res = 0`, and source-charge equality from the parent action/coupling stack, or keep explicit absolute residual
rows. In other words, the coupling/source-measure issue is not side-noise; it is structurally co-equal with the local
residual-charge silence problem.

## Source Register

{markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Parent Charge Extraction Spine

{markdown_table(spine, ["row_id", "step", "formula", "meaning", "current_status", "required_to_promote", "valid_for_claim"])}

## Sector Extraction Matrix

{markdown_table(sector_matrix, ["row_id", "sector", "theta_piece", "Q_piece", "owned_status", "missing_to_claim", "residual_if_missing", "valid_for_claim"])}

## H_tau/H_ref Source Row

{markdown_table(htau_href, ["row_id", "quantity", "formula", "current_value", "runner_rule", "score_ready", "valid_for_claim"])}

## EH Anchor Residual Split

{markdown_table(residual_split, ["row_id", "split_law", "meaning", "zero_condition", "fallback_bound", "status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claims, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(copies, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> int:
    sources = build_sources()
    spine = build_spine_rows()
    sector_matrix = build_sector_matrix()
    htau_href = build_htau_href_rows()
    residual_split = build_residual_split_rows()
    decision = build_decision_rows()
    claims = build_claim_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["spine"], spine)
    write_csv(OUTPUTS["sector_matrix"], sector_matrix)
    write_csv(OUTPUTS["htau_href_row"], htau_href)
    write_csv(OUTPUTS["residual_split"], residual_split)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    copies = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copies)

    validation = build_validation(sources, spine, sector_matrix, htau_href, residual_split, decision, claims, refusal, next_rows, copies)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(sources, spine, sector_matrix, htau_href, residual_split, decision, claims, refusal, next_rows, copies, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"2340 validation failed: {len(failed)} failed rows")
        for row in failed:
            print(f"{row['row_id']}: {row['detail']}")
        return 1

    print(f"2340 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
