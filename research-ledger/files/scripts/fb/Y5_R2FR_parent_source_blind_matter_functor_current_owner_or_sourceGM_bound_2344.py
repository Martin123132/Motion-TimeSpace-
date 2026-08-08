from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_SOURCE_BLIND_FUNCTOR_CURRENT_OWNER_OR_SOURCEGM_BOUND_2344"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2344-Y5-R2FR-parent-source-blind-matter-functor-current-owner-or-sourceGM-bound.md"

PATHS = {
    "2343_doc": ROOT / "2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md",
    "2343_validation": OUT / "P8_Y5_BRR545_2343_VALIDATION.csv",
    "2343_next": OUT / "P8_Y5_PARENT_QLOC_2343_NEXT_TARGET.csv",
    "2329_doc": ROOT / "2329-Y5-R2FR-parent-action-source-blind-functor-signature.md",
    "2329_signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "2329_proof": OUT / "P8_Y5_PARENT_QLOC_2329_NOSOURCE_SLOT_THEOREM_PROOF.csv",
    "2329_activation": OUT / "P8_Y5_PARENT_QLOC_2329_PARENT_SIGNATURE_ACTIVATION_MATRIX.csv",
    "953_category": OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
    "953_theorem": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
    "955_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "1065_grammar": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1098_signature": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1098_theorem": OUT / "P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv",
    "1104_doc": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
    "1104_signature": OUT / "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
    "1105_doc": ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
    "1106_doc": ROOT / "1106-Y5-R10-minimal-explicit-closure-pack-independence-audit-or-first-source-backed-coefficient-row.md",
    "1106_pack": OUT / "P8_Y5_R10_1106_MINIMAL_CLOSURE_PACK.csv",
    "990_contract": OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
}

SOURCES = [
    ("SRC2344_00_2343_doc", "2343_doc", ["NSS2343_3_source_blind_functor", "DEC2343_3_next"], "2343 selected the parent source-blind functor/current-owner route"),
    ("SRC2344_01_2343_validation", "2343_validation", ["VAL2343_OVERALL", "PASS"], "2343 validation"),
    ("SRC2344_02_2343_next", "2343_next", ["NEXT2343_0", "parent grammar/current owner"], "machine-readable 2344 target"),
    ("SRC2344_03_2329_doc", "2329_doc", ["source-only species weight", "not an admissible parent-action argument"], "2329 conditional source-blind signature narrative"),
    ("SRC2344_04_2329_signature", "2329_signature", ["SBF2329_1_source_blind_functor", "SBF2329_4_hilbert_before_readout"], "source-blind functor signature rows"),
    ("SRC2344_05_2329_proof", "2329_proof", ["NST2329_0_no_slot_from_signature", "NST2329_6_verdict"], "conditional no-source-slot proof rows"),
    ("SRC2344_06_2329_activation", "2329_activation", ["ACT2329_1_inherited_from_prior_primitives", "NO"], "activation audit separating signature from derivation"),
    ("SRC2344_07_953_category", "953_category", ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"], "source label-forgetting parent-category contract"),
    ("SRC2344_08_953_theorem", "953_theorem", ["NSF953_3_additivity_limit", "NSF953_5_verdict"], "source functor theorem attempt and additivity limit"),
    ("SRC2344_09_955_lemma", "955_lemma", ["MMA955_3_relative_prefactor", "MMA955_6_verdict"], "minimal matter action lemma and relative-prefactor obstruction"),
    ("SRC2344_10_1065_grammar", "1065_grammar", ["PGG1065_1_no_inert_species_scalar", "PGG1065_5_verdict"], "parent grammar no-source-only-slot audit"),
    ("SRC2344_11_1066_source_scalar", "1066_source_scalar", ["SSE1066_4_quantum_action_scale_obstruction", "SSE1066_5_verdict"], "source-scalar exclusion lemma"),
    ("SRC2344_12_1098_signature", "1098_signature", ["OCS1098_4_source_weight_exclusion", "OCS1098_6_verdict"], "ordinary constant owner/source-weight exclusion signature"),
    ("SRC2344_13_1098_theorem", "1098_theorem", ["OCT1098_2_vertex_counterexample", "OCT1098_3_verdict"], "ordinary-constant owner theorem not promoted"),
    ("SRC2344_14_1104_doc", "1104_doc", ["ordinary-sector parent signature", "not derived"], "parent ordinary-sector signature narrative"),
    ("SRC2344_15_1104_signature", "1104_signature", ["SIG1104_4_source_weight_exclusion", "SIG1104_7_radiative_readout_closure"], "parent signature ledger"),
    ("SRC2344_16_1105_doc", "1105_doc", ["master no-hidden-visible coefficient morphism", "not derived"], "master closure pack obstruction"),
    ("SRC2344_17_1106_doc", "1106_doc", ["common action-measure/current/source ownership", "not a derivation"], "minimal closure independence audit"),
    ("SRC2344_18_1106_pack", "1106_pack", ["MIN1106_B", "MIN1106_D"], "minimal closure pack"),
    ("SRC2344_19_990_contract", "990_contract", ["PAC990_2_matter_functor", "PAC990_4_source_charge"], "compact parent action contract"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2344_SOURCE_REGISTER.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2344_PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION.csv",
    "current_owner": OUT / "P8_Y5_PARENT_QLOC_2344_CURRENT_OWNER_DERIVATION_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2344_COUNTERMODEL_KILL_MATRIX.csv",
    "bounds": OUT / "P8_Y5_PARENT_QLOC_2344_SOURCEGM_BOUND_ACQUISITION_SCHEMA.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2344_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2344_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2344_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2344_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2344_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2344_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2344_0_proof", OUTPUTS["proof"], BETA_DOCS / "PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION_2344_NONCLAIM.csv"),
    ("COPY2344_1_bounds", OUTPUTS["bounds"], MICRO_RESIDUALS / "SOURCEGM_BOUND_ACQUISITION_SCHEMA_2344_NONCLAIM.csv"),
    ("COPY2344_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2344_CURRENT_OWNER_DECISION_LEDGER_NONCLAIM.csv"),
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
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


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_0_target",
            "proof_piece": "parent source-blind matter functor/current-owner theorem",
            "formal_statement": "If S_matter is generated only by Matter(Q_obs,SpeciesRep) with no Coeff_active_source(A) target, one observed measure, and source current J_src := delta S_matter/delta e_obs before readout, then relative source-only weights w_A or kappa_A are inadmissible.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_proves": "relative source-GM coefficients collapse to zero inside the signed parent action language",
            "what_remains_unsigned": "why the current MTS parent must have exactly this object language rather than adopting it as a closure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_1_absent_target",
            "proof_piece": "no coefficient target",
            "formal_statement": "Coeff_active_source(A) notin Obj(Language_parent) and Hom_parent(SpeciesLabel,Coeff_active_source)=empty.",
            "status": "PROOF_STEP_CONDITIONAL_ON_PARENT_LANGUAGE",
            "what_it_proves": "a source-only species multiplier is not set small; it is not typable",
            "what_remains_unsigned": "parent object-language exhaustion / no hidden-visible coefficient morphism",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_2_same_action_owner",
            "proof_piece": "same-action current owner",
            "formal_statement": "J_src[e_obs] = delta S_matter[Psi,e_obs,theta_rep]/delta e_obs and no independent S_src or kappa_A T_A functional exists.",
            "status": "EXACT_AFTER_ACTION_SELECTION",
            "what_it_proves": "Hilbert/coframe variation inherits only terms admitted in the matter action",
            "what_remains_unsigned": "non-Hilbert current, boundary source and readout-current silence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_3_label_forgetting",
            "proof_piece": "source label forgetting before coupling",
            "formal_statement": "q_src({(T_A,A)})=T_total=sum_A T_A before applying the gravitational coupling constant.",
            "status": "EXACT_IF_SOURCE_FUNCTOR_SIGNED",
            "what_it_proves": "there is no remaining label A on which kappa_A can depend",
            "what_remains_unsigned": "source functor descent from parent quotient rather than a chosen map",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_4_common_mode",
            "proof_piece": "common coupling mode",
            "formal_statement": "E[g_obs] = kappa_ref lambda_common T_total is equivalent to E[g_obs] = kappa_measured T_total after one local G/GM calibration.",
            "status": "EXACT_COMMON_MODE_ONLY",
            "what_it_proves": "one universal scale is calibration, not a WEP/PPN/R10 residual",
            "what_remains_unsigned": "range/time/species/frame/readout-dependent pieces cannot be absorbed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_5_relative_counterexample",
            "proof_piece": "relative weights are legal unless parent grammar forbids them",
            "formal_statement": "S_matter=sum_A w_A S_A is diffeomorphism-covariant and additive, and Hilbert variation gives T_src=sum_A w_A T_A.",
            "status": "LIVE_COUNTERMODEL_TO_UNSIGNED_PARENT_LANGUAGE",
            "what_it_proves": "covariance, additivity and Hilbert variation alone do not derive source universality",
            "what_remains_unsigned": "source-only slot exclusion must be syntax/current-owner, not a symmetry afterthought",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSBF2344_6_verdict",
            "proof_piece": "derive parent source-blind functor from current corpus",
            "formal_statement": "Current evidence gives a sharp conditional theorem and proof obligation, not a parent-derived theorem-zero.",
            "status": "NOT_DERIVED_EXACT_CONTRACT_READY",
            "what_it_proves": "we are not circling: the remaining missing object is now one explicit parent action/current-owner normal form",
            "what_remains_unsigned": "derive/adopt the normal form or move to sourceGM residual acquisition",
            "valid_for_claim": "false",
        },
    ]


def build_current_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_0_variational_owner",
            "current_owner_clause": "source is the coframe/Hilbert derivative of one ordinary matter action",
            "test": "J_src := delta S_matter/delta e_obs before arena/readout projection",
            "status": "CONDITIONAL_EXACT",
            "failure_mode": "an independent S_src, J_NH or kappa_A T_A bypasses the source-blind functor",
            "next_action": "derive from parent stationary-action normal form or retain residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_1_noether_bianchi_limit",
            "current_owner_clause": "Ward/Bianchi conservation",
            "test": "nabla_mu E_geom^{mu nu}=0 implies compatible source conservation on shell",
            "status": "HELPFUL_BUT_INSUFFICIENT",
            "failure_mode": "conservation permits sum_A w_A T_A when each T_A is separately conserved",
            "next_action": "do not use conservation as universality proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_2_quantum_action_scale",
            "current_owner_clause": "relative action scale is not automatically redundant",
            "test": "S_A -> w_A S_A can preserve some classical EOM form but changes Hilbert source and quantum weighting",
            "status": "OBSTRUCTION_RETAINED",
            "failure_mode": "field rescaling can move w_A into interactions/normalizations rather than eliminate it",
            "next_action": "exclude w_A by typed source-blind parent language or bound it",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_3_readout_order",
            "current_owner_clause": "variation before readout/projection",
            "test": "arena maps K_R10,K_WEP,K_PPN,K_clock act after J_src is fixed",
            "status": "UNSIGNED_STABILITY_CLAUSE",
            "failure_mode": "readout can reintroduce material/source labels after variation",
            "next_action": "tie to radiative/readout closure or retain epsilon_readout_reentry_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_4_nonhilbert_silence",
            "current_owner_clause": "non-Hilbert/boundary currents are zero or explicit residuals",
            "test": "J_src = J_Hilbert + J_NH + J_boundary + J_readout with J_NH=J_boundary=J_readout=0 by theorem",
            "status": "NOT_SIGNED",
            "failure_mode": "source-GM equality can fail even if relative w_A is killed",
            "next_action": "stage current-owner residual row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CO2344_5_verdict",
            "current_owner_clause": "promote source current owner",
            "test": "all owner clauses jointly signed",
            "status": "CURRENT_OWNER_NOT_PARENT_DERIVED",
            "failure_mode": "local Newton/GR source side remains blocked",
            "next_action": "2345 should attack current-owner normal form before empirical bounds",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_0_relative_wA",
            "countermodel": "S_matter=sum_A w_A S_A",
            "killed_if": "PSBF2344_1_absent_target plus PSBF2344_2_same_action_owner plus common action-scale rule",
            "current_status": "SURVIVES_UNSIGNED_PARENT_LANGUAGE",
            "residual_if_survives": "epsilon_source_GM_rel_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_1_kappaA_TA",
            "countermodel": "J_src=sum_A kappa_A T_A with species/source class coefficients",
            "killed_if": "PSBF2344_3_label_forgetting before coupling selection",
            "current_status": "SURVIVES_UNSIGNED_SOURCE_FUNCTOR",
            "residual_if_survives": "epsilon_kappaA_source_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_2_species_measure",
            "countermodel": "species-dependent measure/current Jacobian J_A",
            "killed_if": "one observed measure and coframe descent are parent-signed",
            "current_status": "SURVIVES_COMMON_MEASURE_UNSIGNED",
            "residual_if_survives": "epsilon_measure_species_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_3_readout_reentry",
            "countermodel": "source-worldtube or arena readout selector reattaches species/source labels",
            "killed_if": "variation-before-readout plus radiative/readout stability",
            "current_status": "SURVIVES_READOUT_STABILITY_UNSIGNED",
            "residual_if_survives": "epsilon_readout_reentry_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_4_nonhilbert_current",
            "countermodel": "J_NH or boundary source current contributes to local active mass",
            "killed_if": "non-Hilbert/boundary current silence theorem",
            "current_status": "SURVIVES_CURRENT_OWNER_UNSIGNED",
            "residual_if_survives": "epsilon_current_owner_NH_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CKM2344_5_verdict",
            "countermodel": "all source-GM coupling countermodels",
            "killed_if": "PSBF2344 exact contract is parent-derived/adopted and non-Hilbert residuals are theorem-zero",
            "current_status": "NOT_KILLED_AS_CLAIM",
            "residual_if_survives": "sourceGM acquisition schema required",
            "valid_for_claim": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2344_0_relative_weight",
            "quantity": "epsilon_source_GM_rel_abs",
            "formula": "norm((I-P_common){w_A,kappa_A,J_A})",
            "required_parent_input": "parent source-blind functor or source-weight vector basis",
            "required_numeric_inputs": "relative source/species weights with normalization convention",
            "source_needed": "MISSING_PARENT_ZERO_OR_SOURCE_BACKED_RELATIVE_WEIGHTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2344_1_current_owner",
            "quantity": "epsilon_current_owner_NH_abs",
            "formula": "||J_NH+J_boundary+J_readout|| / ||J_Hilbert||",
            "required_parent_input": "current-owner theorem or explicit non-Hilbert current decomposition",
            "required_numeric_inputs": "arena-normalized J_NH, boundary flux and readout-current coefficients",
            "source_needed": "MISSING_CURRENT_OWNER_ZERO_OR_NUMERIC_CURRENT_ROWS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2344_2_measure_species",
            "quantity": "epsilon_measure_species_abs",
            "formula": "max_A |J_A/J_common - 1|",
            "required_parent_input": "common observed measure/coframe descent",
            "required_numeric_inputs": "species measure/current Jacobian bounds",
            "source_needed": "MISSING_COMMON_MEASURE_ZERO_OR_JACOBIAN_BOUNDS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2344_3_readout_reentry",
            "quantity": "epsilon_readout_reentry_abs",
            "formula": "||K_readout_after_variation(source labels)||",
            "required_parent_input": "readout/radiative stability and variation-before-readout theorem",
            "required_numeric_inputs": "arena readout selector leakage coefficients",
            "source_needed": "MISSING_READOUT_STABILITY_ZERO_OR_LEAKAGE_ROWS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2344_4_total",
            "quantity": "epsilon_sourceGM_total_abs",
            "formula": "epsilon_source_GM_rel_abs + epsilon_current_owner_NH_abs + epsilon_measure_species_abs + epsilon_readout_reentry_abs",
            "required_parent_input": "all parent zeros above or all numeric bound components",
            "required_numeric_inputs": "all SGB2344_0..3 components with units/source paths",
            "source_needed": "MISSING_COMPONENT_INPUTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2344_0_result",
            "decision": "do not claim parent source-blind matter functor/current-owner theorem as derived",
            "reason": "the conditional theorem is exact, but object-language exhaustion/common current owner/readout stability are still unsigned parent-normal-form clauses",
            "consequence": "source-GM coupling and local Newton/GR source side remain blocked",
            "status": "THEOREM_NOT_DERIVED_CONTRACT_READY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2344_1_real_progress",
            "decision": "keep the exact conditional proof as the clean theorem route",
            "reason": "if the parent normal form is signed, relative source weights are untypable rather than tuned small",
            "consequence": "the coupling problem has a single sharp target instead of many loose arena failures",
            "status": "CONDITIONAL_THEOREM_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2344_2_no_loop",
            "decision": "stop retesting covariance/additivity as if they could kill w_A",
            "reason": "2343/2344 show those routes cannot exclude covariant relative prefactors",
            "consequence": "next derivation must attack parent normal form/current owner directly",
            "status": "ROUTE_PRUNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2344_3_fallback",
            "decision": "if 2345 cannot sign current-owner normal form, begin sourceGM residual acquisition",
            "reason": "unsigned coupling residuals must become source-backed numeric rows rather than hidden assumptions",
            "consequence": "R10/WEP/PPN/orbital branches remain nonclaim until the residual vector is bounded",
            "status": "BOUND_FALLBACK_PREPARED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2344_4_public_policy",
            "decision": "no GitHub update from 2344",
            "reason": "2344 is private coupling theorem triage and proof-obligation narrowing",
            "consequence": "continue private goal work",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2344_0_parent_source_blind", "gate": "parent source-blind matter functor derived", "passed": "false", "claim_effect": "exact conditional theorem only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_1_current_owner", "gate": "same-action Hilbert/current owner parent-signed", "passed": "false", "claim_effect": "non-Hilbert and independent source currents remain residuals", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_2_no_relative_weights", "gate": "relative source/species weights theorem-zero", "passed": "false", "claim_effect": "w_A/kappa_A countermodels survive unsigned grammar", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_3_readout_stability", "gate": "variation-before-readout/radiative stability parent-signed", "passed": "false", "claim_effect": "readout label reentry remains blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_4_sourceGM_bounds", "gate": "sourceGM residual vector score-ready", "passed": "false", "claim_effect": "numeric rows still missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_5_local_GR_Newton", "gate": "local Newton/GR source side derived", "passed": "false", "claim_effect": "cannot claim GR/Newton reduction yet", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2344_6_github", "gate": "safe public GitHub update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2344_0_conditional_to_claim", "claim": "conditional source-blind theorem is a derived MTS theorem", "allowed": "false", "reason": "parent object-language/current-owner clauses remain unsigned", "blocking_rows": "PSBF2344_6_verdict;CG2344_0_parent_source_blind", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2344_1_conservation_universality", "claim": "Bianchi/Noether conservation proves universal source coupling", "allowed": "false", "reason": "separately conserved species currents with relative weights remain possible", "blocking_rows": "CO2344_1_noether_bianchi_limit;CKM2344_0_relative_wA", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2344_2_field_rescale", "claim": "field rescaling removes all relative source weights", "allowed": "false", "reason": "rescaling can move weights into interactions/normalizations and does not prove absence from parent syntax", "blocking_rows": "CO2344_2_quantum_action_scale;MMA955_4_field_rescaling_limit", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2344_3_measured_G_absorb", "claim": "measured G/GM absorbs source-GM coupling residuals", "allowed": "false", "reason": "only one common mode is calibratable; relative/range/time/frame/readout components remain observable", "blocking_rows": "PSBF2344_4_common_mode;SGB2344_4_total", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2344_4_local_claim", "claim": "2344 proves local GR/Newton recovery", "allowed": "false", "reason": "2344 narrows the coupling theorem obligation but does not close source current ownership or gravitational operator/readout gates", "blocking_rows": "CG2344_5_local_GR_Newton;DEC2344_0_result", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2344_0",
            "next_target": "2345-Y5-R2FR-current-owner-normal-form-from-parent-variation-or-sourceGM-residual-first-row.md",
            "why": "the shortest derivation path now is to prove that ordinary matter has one variational current owner and no independent source functional before readout",
            "route_type": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2344_1",
            "next_target": "2345b-Y5-R2FR-sourceGM-residual-vector-acquisition.md",
            "why": "fallback if the current-owner normal form cannot be parent-derived/adopted",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2344_2",
            "next_target": "2345c-Y5-R2FR-parent-action-normal-form-adoption-decision.md",
            "why": "decision route if derivation stalls but the exact conditional theorem is judged to be the minimal parent action definition",
            "route_type": "closure_or_adoption_decision",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        row_count = len(read_csv_rows(destination))
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": row_count,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    current_rows: list[dict[str, Any]],
    counter_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2344_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2344_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2344_02_conditional_theorem_present", any(row["row_id"] == "PSBF2344_0_target" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in proof_rows), "exact conditional theorem recorded")
    add("VAL2344_03_not_promoted", any(row["row_id"] == "PSBF2344_6_verdict" and "NOT_DERIVED" in row["status"] for row in proof_rows), "parent theorem not promoted as derived")
    add("VAL2344_04_current_owner_not_promoted", any(row["row_id"] == "CO2344_5_verdict" and row["status"] == "CURRENT_OWNER_NOT_PARENT_DERIVED" for row in current_rows), "current-owner theorem remains unclaimed")
    add("VAL2344_05_countermodels_retained", all("SURVIVES" in row["current_status"] or row["row_id"] == "CKM2344_5_verdict" for row in counter_rows), "source-GM countermodels retained unless parent contract signed")
    add("VAL2344_06_bound_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in bound_rows), "bound acquisition rows remain non-score-ready")
    add("VAL2344_07_claim_gates_blocked", all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows), "all claim gates remain blocked")
    add("VAL2344_08_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2344_09_next_selected", any(row["row_id"] == "NEXT2344_0" and "current-owner-normal-form" in row["next_target"] for row in next_rows), "2345 current-owner normal form target recorded")
    add("VAL2344_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, proof_rows, current_rows, counter_rows, bound_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2344_11_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION_2344",
        "SOURCEGM_BOUND_ACQUISITION_SCHEMA_2344",
        "JR2344_CURRENT_OWNER",
        "Y5_R2FR_parent_source_blind_matter_functor",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(
                    ["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2344_12_formalization_untouched_by_2344", not formalization_hits, "no 2344 checkpoint output appears in formalization-workbench")
    add("VAL2344_13_no_github_policy", any(row["row_id"] == "DEC2344_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2344")

    overall_pass = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2344_OVERALL",
        overall_pass,
        "2344 converts the coupling issue into an exact parent source-blind/current-owner proof obligation, rejects shortcut promotion, stages sourceGM residual acquisition, and selects current-owner normal form as 2345.",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    current_rows: list[dict[str, Any]],
    counter_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2344 - Parent Source-Blind Matter Functor Current Owner Or SourceGM Bound",
        "",
        "## Summary",
        "",
        "2344 is the anti-loop checkpoint: it stops asking covariance/additivity to do a job they cannot do.",
        "",
        "The clean theorem is real but conditional. If ordinary matter is generated by a parent source-blind functor,",
        "there is no `Coeff_active_source(A)` object, there is one observed measure, and the active source is the",
        "Hilbert/coframe derivative of the same matter action before readout, then relative source weights `w_A` or",
        "`kappa_A` are not merely small; they are not typable.",
        "",
        "But the current corpus has not derived that parent normal form from deeper MTS primitives. Therefore 2344 does",
        "not claim local GR/Newton recovery. It narrows the missing coupling problem to one exact proof obligation:",
        "derive the current-owner/source-blind parent action normal form, or admit a finite `sourceGM` residual vector.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Parent Source-Blind Functor Proof Obligation",
        "",
        markdown_table(proof_rows, ["row_id", "proof_piece", "formal_statement", "status", "what_it_proves", "what_remains_unsigned", "valid_for_claim"]),
        "",
        "## Current Owner Derivation Audit",
        "",
        markdown_table(current_rows, ["row_id", "current_owner_clause", "test", "status", "failure_mode", "next_action", "valid_for_claim"]),
        "",
        "## Countermodel Kill Matrix",
        "",
        markdown_table(counter_rows, ["row_id", "countermodel", "killed_if", "current_status", "residual_if_survives", "valid_for_claim"]),
        "",
        "## SourceGM Bound Acquisition Schema",
        "",
        markdown_table(bound_rows, ["row_id", "quantity", "formula", "required_parent_input", "required_numeric_inputs", "source_needed", "score_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    proof_rows = build_proof_rows()
    current_rows = build_current_owner_rows()
    counter_rows = build_countermodel_rows()
    bound_rows = build_bound_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["proof"], proof_rows)
    write_csv(OUTPUTS["current_owner"], current_rows)
    write_csv(OUTPUTS["countermodels"], counter_rows)
    write_csv(OUTPUTS["bounds"], bound_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(
        sources,
        proof_rows,
        current_rows,
        counter_rows,
        bound_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        sources,
        proof_rows,
        current_rows,
        counter_rows,
        bound_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )
    print(f"2344 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
