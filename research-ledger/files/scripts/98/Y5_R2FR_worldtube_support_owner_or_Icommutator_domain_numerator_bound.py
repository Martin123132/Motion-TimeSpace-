from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1718"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1718 - Worldtube Support Owner Or I_commutator Domain Numerator Bound"
UTC = datetime.now(timezone.utc).isoformat()


def false() -> str:
    return "False"


def true_false(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1718_0_1717_doc",
        "source_key": "1717_doc",
        "source_path": ROOT / "1717-Y5-R2FR-parent-domain-selector-or-Icommutator-domain-row-fill.md",
        "needles": ["NEXT1717_0_primary", "IDR1717_0_parent_worldtube_exterior_annulus_candidate"],
    },
    {
        "source_id": "SRC1718_1_1717_validation",
        "source_key": "1717_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1717_VALIDATION.csv",
        "needles": ["VAL1717_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1718_2_1717_domain_row",
        "source_key": "1717_domain_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_ICOMMUTATOR_DOMAIN_FIRST_SOURCE_ROW.csv",
        "needles": ["IDR1717_0_parent_worldtube_exterior_annulus_candidate", "SOURCE_READY_STRUCTURE_VALUE_MISSING"],
    },
    {
        "source_id": "SRC1718_3_1016_doc",
        "source_key": "1016_doc",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["W_source = closure(supp J_H[tau])", "Current MTS has not yet signed those clauses"],
    },
    {
        "source_id": "SRC1718_4_1016_parent_contract",
        "source_key": "1016_parent_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv",
        "needles": ["PSC1016_3_support_selector", "formal_selector_definition_available_conditional"],
    },
    {
        "source_id": "SRC1718_5_1016_selector_attempt",
        "source_key": "1016_selector_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["PST1016_0_selector_lemma", "conditional_lemma_pass"],
    },
    {
        "source_id": "SRC1718_6_1016_first_schema",
        "source_key": "1016_first_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_FIRST_INPUT_SCHEMA.csv",
        "needles": ["FIS1016_2_worldtube_domain_shift", "MISSING_PARENT_WORLDTUBE_SELECTOR"],
    },
    {
        "source_id": "SRC1718_7_1016_claim_gate",
        "source_key": "1016_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_CLAIM_GATE.csv",
        "needles": ["CG1016_1_selector_lemma_claim", "parent action, same-frame source current, tau, and compactness are unsigned"],
    },
    {
        "source_id": "SRC1718_8_1015_doc",
        "source_key": "1015_doc",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_0_domain", "conditional_reference_lemma"],
    },
    {
        "source_id": "SRC1718_9_hamiltonian_source_measure",
        "source_key": "hamiltonian_source_measure",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_2_observed_worldtube_source", "not_derived"],
    },
    {
        "source_id": "SRC1718_10_hilbert_worldtube_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_0_parent_worldtube_fixed", "not_derived_for_current_MTS"],
    },
    {
        "source_id": "SRC1718_11_hilbert_worldtube_certificate",
        "source_key": "hilbert_worldtube_certificate",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "needles": ["HWG535_0_worldtube_fixed_before_readout", "missing_certificate"],
    },
    {
        "source_id": "SRC1718_12_worldtube_measure_theorem",
        "source_key": "worldtube_measure_theorem",
        "source_path": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_2_MTS_transfer_condition", "premises_open"],
    },
    {
        "source_id": "SRC1718_13_parent_action_1009",
        "source_key": "parent_action_1009",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_8_worldtube_source_glue", "core_missing_piece"],
    },
    {
        "source_id": "SRC1718_14_mhref_1006",
        "source_key": "mhref_1006",
        "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": ["positive same-frame M_H_ref theorem attempted, not closed", "MHA1006_5_anti_circularity"],
    },
    {
        "source_id": "SRC1718_15_qtau_1008",
        "source_key": "qtau_1008",
        "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["QTA1008_7_Q_matter_source", "conditional_not_glued"],
    },
]


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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": true_false(exists),
                "needles_present": true_false(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


WORLDTUBE_OWNER_AUDIT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_0_parent_action",
        "required_owner_clause": "explicit diffeomorphism-covariant parent action supplies J_H and Q_tau",
        "mathematical_form": "delta L = E_A delta Phi^A + dTheta; J_tau=dQ_tau+C_tau; J_H=delta S_matter/delta e_obs",
        "source_anchor": "PSC1016_0;PVA1008_6;PCS1009_9",
        "current_status": "CONTRACT_ONLY_NO_FULL_CURRENT_LAGRANGIAN",
        "owner_signed": false(),
        "failure_if_missing": "J_H support and Q_tau charge remain placeholders",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_1_same_observed_coframe",
        "required_owner_clause": "matter, clocks, rods and orbit readout use one observed coframe",
        "mathematical_form": "S_matter=S_matter[e_obs,psi_m]; J_H[tau]=delta S_matter/delta e_obs contracted with tau",
        "source_anchor": "PSC1016_1;HWT536_1;HEA1015_1",
        "current_status": "SAME_FRAME_MEASURE_NOT_PARENT_SIGNED",
        "owner_signed": false(),
        "failure_if_missing": "frame/source-measure residual Delta_frame_source remains live",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_2_tau_lock",
        "required_owner_clause": "time/Hamiltonian generator tau is fixed before source/readout fitting",
        "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout; L_tau e_obs controlled on local stationary branch",
        "source_anchor": "PSC1016_2;MHA1006_2;HTA1007_4",
        "current_status": "TAU_SOURCE_READOUT_LOCK_OPEN",
        "owner_signed": false(),
        "failure_if_missing": "worldtube support depends on readout time choice",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_3_support_selector",
        "required_owner_clause": "compact source worldtube is Hilbert support, not fitted radius",
        "mathematical_form": "W_source := closure(supp J_H[tau]); S1,S2 link W_source in source-free exterior",
        "source_anchor": "PSC1016_3;PST1016_0;HWT536_0;HWG535_0",
        "current_status": "FORMAL_SELECTOR_CONDITIONAL_NOT_PARENT_SIGNED",
        "owner_signed": false(),
        "failure_if_missing": "domain numerator may be retuned by source-support choice",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_4_compactness_regular_support",
        "required_owner_clause": "support is compact/regular and admits linked exterior surfaces",
        "mathematical_form": "closure(supp J_H[tau]) compact; A_ext cap W_source=empty; [S1]=[S2] in exterior homology",
        "source_anchor": "PSC1016_3;PSC1016_4;W504_0",
        "current_status": "CONDITIONAL_TOPOLOGICAL_STEP",
        "owner_signed": false(),
        "failure_if_missing": "linked-surface class can drift into I_commutator_domain",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_5_dressed_charge_denominator",
        "required_owner_clause": "worldtube source is normalized by dressed Hamiltonian charge",
        "mathematical_form": "M_H_ref := H_tau[S_outer]-H_ref, not bare mass or orbital GM backfill",
        "source_anchor": "PSC1016_5;HSM541_1;HSM541_2;MHA1006_5",
        "current_status": "DEFINITION_GUARDRAIL_PASS_BUT_MHREF_MISSING",
        "owner_signed": false(),
        "failure_if_missing": "numerator cannot be converted to a dimensionless source-normalization bound",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_6_PiM_H_map",
        "required_owner_clause": "Pi_M is the Hamiltonian mass-charge map on this worldtube branch",
        "mathematical_form": "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H, with ell_H tied to int_S Q_tau",
        "source_anchor": "PSC1016_6;HSM541_0;HWT536_3",
        "current_status": "CANDIDATE_ONLY_NOT_PARENT_ADOPTED",
        "owner_signed": false(),
        "failure_if_missing": "old topological Pi_M may still conserve the wrong object",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_7_coupling_descent",
        "required_owner_clause": "matter/source/readout couplings descend through the same observed variables",
        "mathematical_form": "delta_vertical S_matter=delta_vertical S_readout=0 or finite B_obs_source_measure/M_H bound",
        "source_anchor": "PSC1016_7;QTA1008_7;SMO1653_0",
        "current_status": "NOT_SIGNED_COUPLING_BOUND_SCHEMA_ONLY",
        "owner_signed": false(),
        "failure_if_missing": "ordinary coupling leakage can mimic worldtube/source-measure failure",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "WTO1718_8_verdict",
        "required_owner_clause": "W_M is parent-owned Hilbert/source-support worldtube for current MTS",
        "mathematical_form": "PSC1016_0 through PSC1016_8 are signed, so W_source=closure(supp J_H[tau]) before readout",
        "source_anchor": "CG1016_1;PST1016_5;PDS1717_8",
        "current_status": "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED",
        "owner_signed": false(),
        "failure_if_missing": "fallback to I_commutator_domain numerator-bound contract",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
]


SELECTOR_THEOREM_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "WST1718_0_legal_selector",
        "statement": "If parent action, same observed coframe, fixed tau, compact support, and linked exterior surfaces are signed, W_source=closure(supp J_H[tau]) is a pre-readout selector.",
        "status": "CONDITIONAL_LEMMA_PASS",
        "current_blocker": "parent action and same-frame source current are unsigned",
        "effect_if_signed": "worldtube/domain selection becomes derived rather than fitted",
        "valid_for_claim": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "WST1718_1_domain_variation_zero",
        "statement": "If W_source and linked surfaces are fixed under allowed variations, delta_D=0 and the domain part of dPi_M vanishes.",
        "status": "CONDITIONAL_ONLY",
        "current_blocker": "compactness, support regularity, and linking-class lock are not parent-signed",
        "effect_if_signed": "N_domain=int_A(dPi_M)_domain J_H becomes theorem-zero",
        "valid_for_claim": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "WST1718_2_current_verdict",
        "statement": "Apply the worldtube selector to current MTS source-normalization branch.",
        "status": "NOT_PROVED_FOR_CURRENT_MTS",
        "current_blocker": "WTO1718_8 remains false",
        "effect_if_signed": "would remove the first I_commutator_domain numerator",
        "valid_for_claim": false(),
    },
]


NUMERATOR_BOUND_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "bound_id": "NDB1718_0_domain_numerator_contract",
        "quantity": "N_domain",
        "definition": "domain/linking-surface numerator for I_commutator_domain",
        "formula": "N_domain := int_{A_ext} (dPi_M)_domain J_H",
        "bound_form": "abs(N_domain) <= ||(dPi_M)_domain||_{A<-H} * ||J_H||_A",
        "required_inputs": "system_id;W_source;A_ext;S_pair;delta_D;operator_norm_dPiM_domain;J_H_norm;annulus_measure;numerator_units;source_path;equation_ref",
        "current_status": "SOURCE_READY_BOUND_CONTRACT_VALUE_MISSING",
        "missing_inputs": "MISSING_OPERATOR_NORM;MISSING_JH_NORM;MISSING_DELTA_D;MISSING_ANNULUS_MEASURE;MISSING_NUMERATOR_VALUE",
        "source_paths": ";".join(
            str(Path(item["source_path"]))
            for item in SOURCES
            if item["source_key"]
            in {
                "1717_domain_row",
                "1016_doc",
                "1016_parent_contract",
                "1016_selector_attempt",
                "1016_first_schema",
                "hilbert_worldtube_attempt",
                "hilbert_worldtube_certificate",
                "worldtube_measure_theorem",
            }
        ),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "bound_id": "NDB1718_1_dimensionless_domain_bound",
        "quantity": "I_commutator_domain_abs",
        "definition": "dimensionless/source-normalized domain contribution",
        "formula": "abs(I_commutator_domain) <= abs(N_domain)/M_H_ref",
        "bound_form": "requires positive same-frame M_H_ref from Hamiltonian source charge",
        "required_inputs": "N_domain_bound;M_H_ref;M_H_ref_units;tau_id;frame_id;normalization;no_orbital_GM_import_guard",
        "current_status": "BLOCKED_BY_MHREF_AND_NUMERATOR",
        "missing_inputs": "MISSING_N_DOMAIN_BOUND;MISSING_SAME_FRAME_POSITIVE_MHREF",
        "source_paths": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
]


FIRST_NUMERATOR_ROW = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "NDR1718_0_worldtube_support_numerator_bound_candidate",
        "quantity": "N_domain",
        "system_id": "local_compact_source_branch_R2FR",
        "worldtube_rule": "W_source=closure(supp J_H[tau]) if PSC1016_0-PSC1016_4 are signed; currently conditional",
        "A_ext": "source-free exterior annulus between S1,S2 linked to W_source",
        "S_pair": "MISSING_SURFACE_PAIR_WITH_HOMOLOGY_CERTIFICATE",
        "delta_D": "MISSING_DOMAIN_VARIATION_AMPLITUDE_OR_ZERO_THEOREM",
        "operator_norm_dPiM_domain": "MISSING_OPERATOR_NORM_OR_PARENT_ZERO",
        "J_H_norm": "MISSING_SOURCE_CURRENT_NORM",
        "annulus_measure": "MISSING_ANNULUS_MEASURE",
        "numerator_bound": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "numerator_units": "same_units_as_projected_source_current_integral",
        "source_path": ";".join(
            str(Path(item["source_path"]))
            for item in SOURCES
            if item["source_key"]
            in {
                "1717_domain_row",
                "1016_parent_contract",
                "1016_selector_attempt",
                "hilbert_worldtube_attempt",
                "hilbert_worldtube_certificate",
                "hamiltonian_source_measure",
            }
        ),
        "equation_ref": "NDB1718_0;PSC1016_3;PST1016_0;HWT536_0;HWG535_0",
        "no_cancellation_guard": "ABS_SUM_NUMERATOR_NO_CANCELLATION_REQUIRED",
        "row_status": "SOURCE_BACKED_SCHEMA_NUMERATOR_MISSING",
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
        "generated_utc": UTC,
    }
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1718_0_worldtube_support_owner",
        "quantity": "W_source=closure(supp J_H[tau]) parent-owned worldtube",
        "runner_decision": "REFUSE_CLAIM",
        "refusal_reasons": "MISSING_PARENT_ACTION;MISSING_SAME_FRAME_JH;MISSING_TAU_LOCK;MISSING_COMPACTNESS_CERTIFICATE;MISSING_COUPLING_DESCENT",
        "accepted_for_scoring": false(),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1718_1_domain_numerator_zero",
        "quantity": "N_domain theorem-zero",
        "runner_decision": "REFUSE_ZERO_THEOREM",
        "refusal_reasons": "WST1718_0_AND_WST1718_1_ANTECEDENTS_UNSIGNED",
        "accepted_for_scoring": false(),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1718_2_domain_numerator_bound",
        "quantity": "N_domain finite numerator bound",
        "runner_decision": "REFUSE_SCORING_VALUE_MISSING",
        "refusal_reasons": "MISSING_OPERATOR_NORM;MISSING_JH_NORM;MISSING_DELTA_D;MISSING_ANNULUS_MEASURE;MISSING_NUMERIC_BOUND;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": false(),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1718_3_dimensionless_Icommutator_domain",
        "quantity": "abs(I_commutator_domain)<=abs(N_domain)/M_H_ref",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "N_DOMAIN_MISSING;M_H_REF_MISSING;NO_ORBITAL_GM_IMPORT",
        "accepted_for_scoring": false(),
        "score_ready": false(),
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1718_0_primary",
        "next_target": "1719-Y5-R2FR-JH-source-current-norm-or-dPiM-domain-operator-bound.md",
        "script": "scripts/Y5_R2FR_JH_source_current_norm_or_dPiM_domain_operator_bound.py",
        "objective": "try to source or derive the two numerator ingredients: Hilbert source-current norm and domain-variation operator norm; if either fails, keep N_domain as an explicit nonclaim bound row",
        "selection_status": "selected",
        "success_condition": "source-backed J_H norm and dPiM_domain operator norm, or explicit blockers for both with no scoring",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1718_1_parallel_MHref",
        "next_target": "1719b-Y5-R2FR-MHref-same-frame-denominator-fill.md",
        "script": "scripts/Y5_R2FR_MHref_same_frame_denominator_fill.py",
        "objective": "parallel denominator route after N_domain has a numerator bound",
        "selection_status": "held_until_numerator_bound_exists",
        "success_condition": "positive same-frame M_H_ref with no orbital-GM import",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1718_0_worldtube_owner",
        "claim": "W_source=closure(supp J_H[tau]) is parent-owned for current MTS",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "parent action, same-frame J_H, tau lock, compactness, M_H_ref, Pi_M^H and coupling descent are unsigned",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1718_1_N_domain_zero",
        "claim": "domain numerator N_domain is theorem-zero",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "worldtube support owner theorem and fixed-domain variation theorem are conditional only",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1718_2_N_domain_bound",
        "claim": "domain numerator has source-backed finite bound",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "operator norm, J_H norm, domain variation and annulus measure are missing",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1718_3_Newton_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "N_domain, M_H_ref, R_eq, Pi_M_H and PPN residual vector remain open",
        "valid_for_claim": false(),
        "claim_allowed": false(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_SOURCE_REGISTER.csv",
    "worldtube_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv",
    "selector_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SELECTOR_THEOREM_ATTEMPT.csv",
    "numerator_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv",
    "first_numerator_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_NDOMAIN_FIRST_NUMERATOR_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_RUNNER_REFUSAL.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1718_VALIDATION.csv",
}


COPY_MAP = {
    "worldtube_audit": "R2FR_worldtube_support_owner_audit_1718.csv",
    "selector_theorem": "R2FR_worldtube_selector_theorem_attempt_1718.csv",
    "numerator_bound": "R2FR_Icommutator_domain_numerator_bound_contract_1718.csv",
    "first_numerator_row": "R2FR_Ndomain_first_numerator_row_1718.csv",
    "runner_refusal": "R2FR_runner_refusal_1718.csv",
    "next_target": "R2FR_next_target_1718.csv",
    "claim_gate": "R2FR_claim_gate_1718.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "worldtube_audit": WORLDTUBE_OWNER_AUDIT_ROWS,
        "selector_theorem": SELECTOR_THEOREM_ROWS,
        "numerator_bound": NUMERATOR_BOUND_ROWS,
        "first_numerator_row": FIRST_NUMERATOR_ROW,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1718_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1718_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "owner_signed"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def source_paths_exist_in_bound_rows() -> bool:
    rows = NUMERATOR_BOUND_ROWS + FIRST_NUMERATOR_ROW
    for row in rows:
        paths = [Path(item) for item in str(row.get("source_paths", row.get("source_path", ""))).split(";") if item]
        if not paths or any(not path.exists() for path in paths):
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1718_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1718_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1718*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_rows = rows_map["source_register"]
    audit_rows = rows_map["worldtube_audit"]
    theorem_rows = rows_map["selector_theorem"]
    bound_rows = rows_map["numerator_bound"]
    first_rows = rows_map["first_numerator_row"]
    runner_rows = rows_map["runner_refusal"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check(
            "VAL1718_0_sources_exist",
            all(row["exists"] == "True" for row in source_rows),
            "all cited source paths exist",
            "one or more cited source paths missing",
        ),
        check(
            "VAL1718_1_needles_present",
            all(row["needles_present"] == "True" for row in source_rows),
            "required source needles are present",
            "one or more required source needles missing",
        ),
        check(
            "VAL1718_2_worldtube_owner_not_proved",
            any(row["audit_id"] == "WTO1718_8_verdict" and row["current_status"] == "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED" for row in audit_rows),
            "worldtube support owner remains unproved",
            "worldtube support owner verdict missing or promoted",
        ),
        check(
            "VAL1718_3_selector_theorem_conditional",
            any(row["theorem_id"] == "WST1718_0_legal_selector" and row["status"] == "CONDITIONAL_LEMMA_PASS" for row in theorem_rows)
            and any(row["theorem_id"] == "WST1718_2_current_verdict" and row["status"] == "NOT_PROVED_FOR_CURRENT_MTS" for row in theorem_rows),
            "selector theorem retained as conditional and not applied to current MTS",
            "selector theorem missing, failed as math, or promoted",
        ),
        check(
            "VAL1718_4_numerator_bound_contract_present",
            any(row["bound_id"] == "NDB1718_0_domain_numerator_contract" and row["current_status"] == "SOURCE_READY_BOUND_CONTRACT_VALUE_MISSING" for row in bound_rows),
            "domain numerator bound contract is present and value-missing",
            "domain numerator bound contract missing or score-ready",
        ),
        check(
            "VAL1718_5_first_numerator_row_nonclaim",
            any(row["row_id"] == "NDR1718_0_worldtube_support_numerator_bound_candidate" and row["row_status"] == "SOURCE_BACKED_SCHEMA_NUMERATOR_MISSING" and row["valid_for_claim"] == "False" for row in first_rows),
            "first numerator row is source-backed schema and nonclaim",
            "first numerator row missing or claim-enabled",
        ),
        check(
            "VAL1718_6_bound_source_paths_exist",
            source_paths_exist_in_bound_rows(),
            "all source paths listed in numerator-bound rows exist",
            "one or more source paths listed in numerator-bound rows missing",
        ),
        check(
            "VAL1718_7_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses worldtube, zero, numerator, denominator and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1718_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check(
            "VAL1718_9_next_selected",
            any(row["route_id"] == "NEXT1718_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects J_H norm or dPiM domain operator bound",
            "next target missing selected primary route",
        ),
        check(
            "VAL1718_10_csv_parse",
            parsed_ok,
            "all generated 1718 CSVs parse",
            "one or more generated 1718 CSVs failed to parse",
        ),
        check(
            "VAL1718_11_no_claim_flags",
            no_claim_flags(rows_map),
            "all generated scoring and claim flags remain false",
            "one or more generated flags enabled a claim",
        ),
        check(
            "VAL1718_12_branch_copies",
            branch_copies_exist(),
            "branch/quarantine/queue copies exist",
            "one or more branch/quarantine/queue copies missing",
        ),
        check(
            "VAL1718_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
            "scripts __pycache__ still exists",
        ),
        check(
            "VAL1718_14_formalization_untouched",
            formalization_untouched(),
            "no 1718 outputs found under formalization-workbench",
            "1718 output leaked into formalization-workbench",
        ),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1718_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1718 worldtube support owner and I_commutator_domain numerator-bound validation"
            if overall
            else "one or more 1718 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1718 tries the theorem route first: make `W_source = closure(supp J_H[tau])` a parent-owned Hilbert/source-support worldtube.",
        "- The selector theorem is mathematically clean but remains conditional: the parent action, same-frame `J_H`, fixed `tau`, compact support, `M_H_ref`, `Pi_M^H`, boundary/reference lock, and coupling descent are still unsigned.",
        "- Therefore `W_M` is not claimed as a parent-owned support selector for current MTS.",
        "- The fallback is now sharper: the numerator `N_domain = int_A (dPi_M)_domain J_H` has a source-backed bound contract, but its operator norm, source-current norm, domain variation, annulus measure, and numeric/theorem-zero value are missing.",
        "- No Newton, local-GR, R10, PPN, clock, orbital, source-normalization or `q_loc`-zero claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Worldtube Support Owner Audit",
        markdown_table(
            rows_map["worldtube_audit"],
            ["audit_id", "required_owner_clause", "mathematical_form", "current_status", "owner_signed", "failure_if_missing"],
        ),
        "",
        "## Worldtube Selector Theorem Attempt",
        markdown_table(
            rows_map["selector_theorem"],
            ["theorem_id", "statement", "status", "current_blocker", "effect_if_signed"],
        ),
        "",
        "## I_commutator Domain Numerator Bound Contract",
        markdown_table(
            rows_map["numerator_bound"],
            ["bound_id", "quantity", "formula", "bound_form", "current_status", "missing_inputs", "score_ready"],
        ),
        "",
        "## First Numerator Row",
        markdown_table(
            rows_map["first_numerator_row"],
            [
                "row_id",
                "quantity",
                "worldtube_rule",
                "S_pair",
                "delta_D",
                "operator_norm_dPiM_domain",
                "J_H_norm",
                "numerator_bound",
                "row_status",
                "valid_for_claim",
            ],
        ),
        "",
        "## Runner Refusal",
        markdown_table(
            rows_map["runner_refusal"],
            ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"],
        ),
        "",
        "## Next Target",
        markdown_table(
            rows_map["next_target"],
            ["route_id", "next_target", "script", "objective", "selection_status"],
        ),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This checkpoint closes a bit of fog. The right support selector is not arbitrary: it should be the closure of the observed Hilbert source-current support. But that only becomes physics after the parent action owns the current, coframe, tau, compactness and charge map. Since that is still unsigned, the honest next target is the numerator itself: source or bound `J_H` and the domain-variation operator instead of pretending the domain term is zero.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1718_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1718 validation FAIL")
    print("1718 validation PASS")


if __name__ == "__main__":
    main()
