from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_CHARGE_EQUALS_MEASURED_GM_OR_SELECTOR_BOUND_2342"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md"

PATHS = {
    "2341_doc": ROOT / "2341-Y5-R2FR-EH-anchor-residual-charge-zero-or-coefficient-row.md",
    "2341_validation": OUT / "P8_Y5_BRR545_2341_VALIDATION.csv",
    "2341_next": OUT / "P8_Y5_PARENT_QLOC_2341_NEXT_TARGET.csv",
    "2341_components": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COMPONENT_MAP.csv",
    "1016_doc": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hsm_scorecard": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "source_measure_attempt": OUT / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "hilbert_worldtube": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "poisson_gauss": OUT / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "hilbert_mono": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "gm_obstruction": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "source_gm_universality": OUT / "P8_Y5_PARENT_QLOC_2327_SOURCE_GM_UNIVERSALITY_ATTEMPT.csv",
    "gm_absorption_refusal": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
    "same_frame_gate": OUT / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
}

SOURCES = [
    ("SRC2342_00_2341_doc", "2341_doc", PATHS["2341_doc"], ["DEC2341_2_next", "SELECT_SOURCE_MEASURE_BRIDGE_NEXT"], "2341 selected source-charge measured-GM bridge"),
    ("SRC2342_01_2341_validation", "2341_validation", PATHS["2341_validation"], ["VAL2341_OVERALL", "PASS"], "2341 validation"),
    ("SRC2342_02_2341_next", "2341_next", PATHS["2341_next"], ["NEXT2341_0", "source-charge-equals-measured-GM"], "machine-readable 2342 target"),
    ("SRC2342_03_2341_components", "2341_components", PATHS["2341_components"], ["Delta_Q_source_glue", "Delta_Q_coupling_G"], "Delta_Q source/coupling residual components"),
    ("SRC2342_04_1016_doc", "1016_doc", PATHS["1016_doc"], ["PSC1016_5_dressed_source_charge", "FIS1016_0_M_H_ref"], "parent worldtube/source-measure selector"),
    ("SRC2342_05_hsm_contract", "hsm_contract", PATHS["hsm_contract"], ["HSM541_5_Gauss_orbital_readout", "HSM541_6_constant_universal_G"], "Hamiltonian source-measure contract"),
    ("SRC2342_06_hsm_scorecard", "hsm_scorecard", PATHS["hsm_scorecard"], ["HSS541_2_worldtube_source_measure", "fail_current_claim"], "source-measure scorecard"),
    ("SRC2342_07_source_measure_attempt", "source_measure_attempt", PATHS["source_measure_attempt"], ["SMT542_0_conditional_statement", "premises not parent-derived"], "source-measure theorem attempt"),
    ("SRC2342_08_hilbert_worldtube", "hilbert_worldtube", PATHS["hilbert_worldtube"], ["HWT536_0_parent_worldtube_fixed", "HWT536_8_weak_field_readout_after_charge_glue"], "Hilbert worldtube glue attempt"),
    ("SRC2342_09_poisson_gauss", "poisson_gauss", PATHS["poisson_gauss"], ["PG0_Hamiltonian_charge_input", "PG10_retained_residual_fallback"], "Poisson/Gauss orbital bridge contract"),
    ("SRC2342_10_hilbert_mono", "hilbert_mono", PATHS["hilbert_mono"], ["HM0_Hilbert_current_input", "HM8_empirical_retained_fallback"], "Hilbert monopole calibration contract"),
    ("SRC2342_11_gm_obstruction", "gm_obstruction", PATHS["gm_obstruction"], ["MGV2203_0_projected_extra_current", "MGV2203_7_calibration_PPN_tail"], "measured-GM obstruction vector"),
    ("SRC2342_12_source_gm_universality", "source_gm_universality", PATHS["source_gm_universality"], ["UGM2327_6_verdict", "NOT_PROVED_USE_BOUND_ROUTE"], "source-GM universality attempt"),
    ("SRC2342_13_gm_absorption_refusal", "gm_absorption_refusal", PATHS["gm_absorption_refusal"], ["REF2125_1_measured_G_hiding", "REFUSED"], "measured-G/GM hiding refusal"),
    ("SRC2342_14_same_frame_gate", "same_frame_gate", PATHS["same_frame_gate"], ["SFG683_6_final", "fail_blocked"], "same-frame GM denominator gate"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2342_SOURCE_REGISTER.csv",
    "bridge_audit": OUT / "P8_Y5_PARENT_QLOC_2342_SOURCE_GM_BRIDGE_AUDIT.csv",
    "selector_contract": OUT / "P8_Y5_PARENT_QLOC_2342_SELECTOR_SOURCE_MEASURE_CONTRACT.csv",
    "obstruction_vector": OUT / "P8_Y5_PARENT_QLOC_2342_SOURCE_GM_OBSTRUCTION_VECTOR.csv",
    "bound_rows": OUT / "P8_Y5_PARENT_QLOC_2342_SELECTOR_BOUND_ROWS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2342_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2342_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2342_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2342_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2342_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2342_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2342_0_bridge", OUTPUTS["bridge_audit"], BETA_DOCS / "SOURCE_GM_BRIDGE_AUDIT_2342_NONCLAIM.csv"),
    ("COPY2342_1_bounds", OUTPUTS["bound_rows"], MICRO_RESIDUALS / "SELECTOR_BOUND_ROWS_2342_NONCLAIM.csv"),
    ("COPY2342_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2342_SOURCE_GM_DECISION_LEDGER_NONCLAIM.csv"),
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


def build_bridge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_0_target",
            "claim_piece": "source charge equals measured GM",
            "formal_statement": "G_ref M_H_ref = GM_orbit and the same H_tau-H_ref charge sources the weak-field Poisson/Gauss monopole read by orbits.",
            "status": "TARGET_SHARPENED",
            "proof_or_obstruction": "this is the bridge from EH-anchor charge to Newtonian measured mass",
            "fallback": "selector/source-measure residual vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_1_Htau_MHref",
            "claim_piece": "integrable dressed Hamiltonian charge",
            "formal_statement": "M_H_ref := H_tau[S_outer]-H_ref is finite, positive, fixed-reference and same-frame before readout.",
            "status": "MISSING_MHREF_SOURCE_ROW",
            "proof_or_obstruction": "2339/2340 staged the row but H_tau, H_ref and parent certificates are missing",
            "fallback": "epsilon_MHref_missing_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_2_worldtube_selector",
            "claim_piece": "pre-readout source worldtube",
            "formal_statement": "W_source=closure(supp J_H[tau]) and linked surfaces enclose the same source before orbital fitting.",
            "status": "CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "1016/HWT536 keep compactness, support selector and same-frame source measure open",
            "fallback": "epsilon_worldtube_selector_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_3_Hilbert_charge",
            "claim_piece": "Hamiltonian charge equals observed Hilbert/source charge",
            "formal_statement": "M_H_ref = integral_S Q_tau = integral_W J_H[tau] after fixed reference and boundary lock.",
            "status": "MISSING_HILBERT_NOETHER_EQUALITY",
            "proof_or_obstruction": "Pi_M/Hilbert/topological equality, R_eq and I_commutator remain unsigned",
            "fallback": "epsilon_source_measure_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_4_Poisson_Gauss",
            "claim_piece": "Poisson/Gauss/orbital readout",
            "formal_statement": "the same charge appears in nabla^2 Phi=4*pi*G_ref rho and a_r=-G_ref M_H_ref/r^2 for test bodies.",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "PG0-PG10 are contract rows; HSM541 scorecard keeps Gauss/orbital readout failed",
            "fallback": "epsilon_PG_orbit_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_5_constant_G",
            "claim_piece": "constant universal G_ref",
            "formal_statement": "partial_t,r,source,species,range,frame G_ref=0 and no relative source prefactor survives fitted common-mode GM.",
            "status": "MISSING_UNIVERSAL_COUPLING_DESCENT",
            "proof_or_obstruction": "2327 and 2125 keep NoSourceOnlySpeciesSlot and measured-G hiding refusal active",
            "fallback": "epsilon_source_GM_rel_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGM2342_6_verdict",
            "claim_piece": "promote source-charge equals measured-GM bridge now",
            "formal_statement": "SGM2342_1 through SGM2342_5 all parent-signed would permit GM_orbit to be a derived readout of M_H_ref rather than a denominator input.",
            "status": "BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS",
            "proof_or_obstruction": "current corpus has conditional lemmas and obstruction vectors, not the source-GM theorem",
            "fallback": "stage selector/source-GM bound rows",
            "valid_for_claim": "false",
        },
    ]


def build_selector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSC2342_0_selector",
            "selector_clause": "source worldtube",
            "formula": "W_source := closure(supp J_H[tau])",
            "required_for_claim": "same observed coframe, compact support, linked surfaces and pre-readout rule",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "residual_if_missing": "Delta_worldtube_domain",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSC2342_1_charge",
            "selector_clause": "dressed charge",
            "formula": "M_source[W]=M_H_ref=H_tau[S_outer]-H_ref",
            "required_for_claim": "integrable H_tau, fixed H_ref, positive same-frame M_H_ref",
            "current_status": "MISSING_M_H_REF",
            "residual_if_missing": "epsilon_MHref_missing_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSC2342_2_Hilbert",
            "selector_clause": "Hilbert/source equality",
            "formula": "M_H_ref = integral_W J_H[tau] = integral_S Q_tau",
            "required_for_claim": "parent Hilbert current, Pi_M/source map, R_eq=0 and I_commutator=0 or bounds",
            "current_status": "MISSING_SOURCE_MEASURE_EQUALITY",
            "residual_if_missing": "epsilon_source_measure_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSC2342_3_Gauss",
            "selector_clause": "orbital readout",
            "formula": "GM_orbit=G_ref M_H_ref after Poisson/Gauss bridge",
            "required_for_claim": "PG0-PG10 and HM0-HM8 pass; no non-Hilbert channels",
            "current_status": "MISSING_POISSON_GAUSS_BRIDGE",
            "residual_if_missing": "epsilon_PG_orbit_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSC2342_4_universal_G",
            "selector_clause": "universal coupling",
            "formula": "D_source,species,range,frame G_ref = 0 up to a single common-mode calibration",
            "required_for_claim": "NoSourceOnlySpeciesSlot and source/profile GM universality",
            "current_status": "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT",
            "residual_if_missing": "epsilon_source_GM_rel_abs",
            "valid_for_claim": "false",
        },
    ]


def build_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_0_extra_current",
            "obstruction": "projected extra current",
            "symbol": "-Pi_M dJ_extra",
            "source_anchor": "MGV2203_0_projected_extra_current",
            "blocks": "fixed-before-readout GM/PPN map",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_1_PiM_commutator",
            "obstruction": "projector commutator",
            "symbol": "[d,Pi_M]J_H",
            "source_anchor": "MGV2203_1_PiM_commutator",
            "blocks": "source charge equality and R_eq normalization",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_2_R_eq",
            "obstruction": "topological/Hilbert equality residual",
            "symbol": "R_eq",
            "source_anchor": "MGV2203_3_topological_equality_residual",
            "blocks": "closed charge equals observed mass",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_3_boundary",
            "obstruction": "boundary zero flux",
            "symbol": "B_zero_flux",
            "source_anchor": "MGV2203_4_boundary_zero_flux",
            "blocks": "fixed reference/source charge equality",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_4_flux_leak",
            "obstruction": "radial/time source-measure flux leakage",
            "symbol": "dln_Meff_dt or epsilon_radial_Meff",
            "source_anchor": "MGV2203_6_flux_leak",
            "blocks": "radially stable measured GM",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_5_calibration_tail",
            "obstruction": "Gauss/orbital/PPN calibration tail",
            "symbol": "Delta_cal + Delta_PPN",
            "source_anchor": "MGV2203_7_calibration_PPN_tail",
            "blocks": "Newton/PPN followthrough",
            "current_status": "retained_unfilled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGO2342_6_relative_source_GM",
            "obstruction": "relative source/profile/composition GM residual",
            "symbol": "epsilon_sigma_source_GM",
            "source_anchor": "UGM2327_6_verdict",
            "blocks": "universal coupling and source-label forgetting",
            "current_status": "not_proved_use_bound_route",
            "valid_for_claim": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2342_0_selector_abs",
            "quantity": "epsilon_selector_GM_abs",
            "formula": "abs(Delta_worldtube_domain)+abs(Delta_frame_source)+abs(R_eq)/M_H_ref+abs(I_commutator)/M_H_ref+abs(B_zero_flux)/M_H_ref",
            "required_columns": "system_id;W_source_rule;tau_id;coframe_id;surface_pair;M_H_ref;R_eq;I_commutator;B_zero_flux;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2342_1_source_GM_abs",
            "quantity": "epsilon_source_GM_abs",
            "formula": "abs(GM_orbit/G_ref/M_H_ref - 1) with no orbital-GM backfill",
            "required_columns": "system_id;GM_orbit;G_ref;M_H_ref;calibration_method;poisson_gauss_certificate;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_GM_BRIDGE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2342_2_relative_G_abs",
            "quantity": "epsilon_source_GM_rel_abs",
            "formula": "norm(relative source/species/profile weights after one common GM calibration)",
            "required_columns": "system_id;source_profile_basis;species_weights;common_mode_removed;relative_residual;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT;MISSING_PROFILE_VECTOR",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2342_3_total_bridge_abs",
            "quantity": "epsilon_GM_bridge_abs",
            "formula": "epsilon_selector_GM_abs + epsilon_source_GM_abs + epsilon_source_GM_rel_abs + epsilon_PG_orbit_abs",
            "required_columns": "system_id;component_values;component_sources;no_cancellation_guard;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2342_0_bridge_result",
            "decision": "do not claim source charge equals measured GM",
            "reason": "M_H_ref, worldtube selector, Hilbert/source equality, Poisson/Gauss readout and universal-G descent are all unsigned",
            "consequence": "Newton/local-GR recovery remains blocked by the source-measure bridge",
            "status": "SOURCE_GM_BRIDGE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2342_1_bound_rows",
            "decision": "stage selector/source-GM bound rows",
            "reason": "the failed bridge decomposes into executable selector, calibration and relative-source residuals",
            "consequence": "future work can prove or fill one source-measure component at a time",
            "status": "SELECTOR_BOUND_ROWS_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2342_2_next",
            "decision": "attack NoSourceOnlySpeciesSlot plus same-frame GM descent next",
            "reason": "a single fitted GM can hide only common mode; relative source weights are the sharpest coupling countermodel",
            "consequence": "next target goes after the coupling key directly before using measured GM as evidence",
            "status": "SELECT_COUPLING_SOURCE_GM_DESCENT_NEXT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2342_3_public_policy",
            "decision": "no GitHub update from 2342",
            "reason": "this is private bridge triage and residual plumbing, not a public claim checkpoint",
            "consequence": "continue private derivation sequence",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2342_0_MHref", "M_H_ref exists as positive fixed source charge", "false", "H_tau/H_ref row remains unfilled"),
        ("CG2342_1_worldtube_selector", "source worldtube selector parent-signed", "false", "support/same-frame/linking clauses conditional"),
        ("CG2342_2_Hilbert_charge", "Hamiltonian charge equals Hilbert/source charge", "false", "R_eq/I_commutator/projector still open"),
        ("CG2342_3_Poisson_Gauss", "same charge gives orbital GM", "false", "PG/HM bridge remains conditional"),
        ("CG2342_4_universal_G", "constant universal source-blind G_ref", "false", "NoSourceOnlySpeciesSlot not parent-signed"),
        ("CG2342_5_bridge_score", "selector/source-GM bound rows score-ready", "false", "component values and M_H_ref missing"),
        ("CG2342_6_local_GR_Newton", "local GR/Newton recovery derived", "false", "source-measure bridge remains open"),
        ("CG2342_7_github", "safe public GitHub update", "false", "private checkpoint only"),
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
            "row_id": "REF2342_0_orbital_GM_backfill",
            "claim": "use observed GM_orbit/G_ref to fill M_H_ref",
            "allowed": "false",
            "reason": "this borrows Newton to prove the Newton/source normalization bridge",
            "blocking_rows": "SGM2342_1_Htau_MHref;SGM2342_4_Poisson_Gauss",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2342_1_common_mode_hiding",
            "claim": "absorb all source/coupling differences into fitted GM",
            "allowed": "false",
            "reason": "only one universal common mode can be calibrated; relative source/profile/species components remain observable",
            "blocking_rows": "SGM2342_5_constant_G;SGB2342_2_relative_G_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2342_2_bulk_profile_shortcut",
            "claim": "use bulk composition/profile as the source worldtube vector",
            "allowed": "false",
            "reason": "the source profile must be orbit/worldtube/support weighted or theorem-cancelled",
            "blocking_rows": "SSC2342_0_selector;SGB2342_2_relative_G_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2342_3_closed_charge_equals_measured_mass",
            "claim": "a conserved charge is automatically measured GM",
            "allowed": "false",
            "reason": "closed charge can be the wrong conserved object without Hilbert/source and Poisson/Gauss bridges",
            "blocking_rows": "SGM2342_3_Hilbert_charge;SGM2342_4_Poisson_Gauss",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2342_4_local_claim",
            "claim": "2342 proves Newton/local-GR recovery",
            "allowed": "false",
            "reason": "2342 stages a nonclaim bridge and bound rows; it does not derive measured-GM equality",
            "blocking_rows": "DEC2342_0_bridge_result;CG2342_6_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2342_0",
            "next_target": "2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md",
            "why": "relative source weights are the sharpest coupling countermodel; proving their absence is the cleanest next derivation step.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2342_1",
            "next_target": "2343b-Y5-R2FR-Poisson-Gauss-orbital-bridge-or-DeltaPG-row.md",
            "why": "parallel bridge: derive that the same charge produces the Poisson/Gauss monopole read by orbits.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2342_2",
            "next_target": "2343c-Y5-R2FR-selector-sourceGM-bound-row-runner.md",
            "why": "fallback route: fill selector/source-GM residual rows with units, source paths and component maps.",
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
    bridge_audit: list[dict[str, Any]],
    selector_contract: list[dict[str, Any]],
    obstruction_vector: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL2342_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"))
    validations.append(("VAL2342_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"))
    validations.append(("VAL2342_02_bridge_not_promoted", any(row["status"] == "BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS" for row in bridge_audit), "source-GM bridge not promoted"))
    validations.append(("VAL2342_03_selector_contract_written", len(selector_contract) >= 5 and any(row["row_id"] == "SSC2342_4_universal_G" for row in selector_contract), "selector/source-measure contract includes universal-G clause"))
    validations.append(("VAL2342_04_obstruction_vector_written", len(obstruction_vector) >= 7 and any(row["symbol"] == "epsilon_sigma_source_GM" for row in obstruction_vector), "measured-GM obstruction vector includes relative source residual"))
    validations.append(("VAL2342_05_bound_rows_nonready", len(bound_rows) >= 4 and all(row["score_ready"] == "false" for row in bound_rows), "selector/source-GM bound rows remain non-score-ready"))
    validations.append(("VAL2342_06_claim_gates_blocked", all(row["passed"] == "false" for row in claims), "all claim gates remain blocked"))
    validations.append(("VAL2342_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal), "shortcut claims refused"))
    validations.append(("VAL2342_08_next_selected", any("NoSourceOnlySpeciesSlot" in row["next_target"] for row in next_rows), "2343 NoSourceOnlySpeciesSlot next target recorded"))
    validations.append(("VAL2342_09_github_blocked", any(row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision), "public GitHub update not recommended from 2342"))
    validations.append(("VAL2342_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copies), "branch copies exist and parse"))

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths.extend(destination for _, _, destination in BRANCH_COPY_SPECS)
    validations.append(("VAL2342_11_outputs_exist", all(path.exists() for path in generated_paths), "CSV outputs and branch copies exist before doc render"))

    no_claim_flags = True
    for path in [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]:
        if path.exists() and path.suffix == ".csv":
            rows = read_csv_rows(path)
            if any(row.get("valid_for_claim", "").lower() == "true" for row in rows):
                no_claim_flags = False
                break
    validations.append(("VAL2342_12_no_claim_flags", no_claim_flags, "no generated row is valid_for_claim=true"))

    formalization_clean = not any(FORMALIZATION.rglob("*2342*")) if FORMALIZATION.exists() else True
    validations.append(("VAL2342_13_formalization_untouched_by_2342", formalization_clean, "no 2342 checkpoint output appears in formalization-workbench"))

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
            "row_id": "VAL2342_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2342 tests the source-charge measured-GM bridge, rejects shortcut promotion, stages selector/source-GM bounds, and selects coupling/source-GM descent next.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    bridge_audit: list[dict[str, Any]],
    selector_contract: list[dict[str, Any]],
    obstruction_vector: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2342 - source charge equals measured GM or selector bound

## Summary

2342 attacks the bridge that decides whether the EH-anchor/Hamiltonian charge is the **measured** Newtonian source.

The desired theorem is:

`GM_orbit = G_ref M_H_ref`,

where `M_H_ref = H_tau[S_outer] - H_ref` is selected before orbital fitting and equals the observed Hilbert/source
charge in the same frame.

That bridge is not derived yet. The blocker is not cosmetic: a conserved charge is not automatically measured `GM`.
The theory still needs a parent-signed worldtube selector, same-frame Hilbert source current, fixed `M_H_ref`,
Poisson/Gauss orbital readout, and a constant universal coupling with no relative source/species/profile prefactors.

So 2342 stages selector/source-GM bound rows and chooses the coupling/source-GM descent theorem as the next best attack.

## Source Register

{markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Source-GM Bridge Audit

{markdown_table(bridge_audit, ["row_id", "claim_piece", "formal_statement", "status", "proof_or_obstruction", "fallback", "valid_for_claim"])}

## Selector Source-Measure Contract

{markdown_table(selector_contract, ["row_id", "selector_clause", "formula", "required_for_claim", "current_status", "residual_if_missing", "valid_for_claim"])}

## Source-GM Obstruction Vector

{markdown_table(obstruction_vector, ["row_id", "obstruction", "symbol", "source_anchor", "blocks", "current_status", "valid_for_claim"])}

## Selector Bound Rows

{markdown_table(bound_rows, ["row_id", "quantity", "formula", "current_value", "score_ready", "valid_for_claim"])}

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
    bridge_audit = build_bridge_audit_rows()
    selector_contract = build_selector_contract_rows()
    obstruction_vector = build_obstruction_rows()
    bound_rows = build_bound_rows()
    decision = build_decision_rows()
    claims = build_claim_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["bridge_audit"], bridge_audit)
    write_csv(OUTPUTS["selector_contract"], selector_contract)
    write_csv(OUTPUTS["obstruction_vector"], obstruction_vector)
    write_csv(OUTPUTS["bound_rows"], bound_rows)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    copies = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copies)

    validation = build_validation(sources, bridge_audit, selector_contract, obstruction_vector, bound_rows, decision, claims, refusal, next_rows, copies)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(sources, bridge_audit, selector_contract, obstruction_vector, bound_rows, decision, claims, refusal, next_rows, copies, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"2342 validation failed: {len(failed)} failed rows")
        for row in failed:
            print(f"{row['row_id']}: {row['detail']}")
        return 1

    print(f"2342 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
