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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1720"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1720 - Observed Hilbert Current Norm Source Row Or Matter Functor Signature"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1720_0_1719_doc",
        "source_key": "1719_doc",
        "source_path": ROOT / "1719-Y5-R2FR-JH-source-current-norm-or-dPiM-domain-operator-bound.md",
        "needles": ["NEXT1719_0_primary", "ING1719_0_JH_norm_candidate"],
    },
    {
        "source_id": "SRC1720_1_1719_validation",
        "source_key": "1719_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1719_VALIDATION.csv",
        "needles": ["VAL1719_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1720_2_1719_ingredient_rows",
        "source_key": "1719_ingredient_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
        "needles": ["ING1719_0_JH_norm_candidate", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1720_3_410_doc",
        "source_key": "410_doc",
        "source_path": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": ["conditional_chain_rule_theorem_written", "conditional_theorem_not_parent_derivation"],
    },
    {
        "source_id": "SRC1720_4_449_doc",
        "source_key": "449_doc",
        "source_path": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
        "needles": ["W0_Hilbert_coframe_current", "SC1_Hilbert_source_definition"],
    },
    {
        "source_id": "SRC1720_5_622_contract",
        "source_key": "622_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
        "needles": ["PMC622_5_universal_source", "not_signed"],
    },
    {
        "source_id": "SRC1720_6_684_frame_lock",
        "source_key": "684_frame_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
        "needles": ["FLC684_4_Hilbert_source_before_GM", "definition_conditional_not_source_measure_theorem"],
    },
    {
        "source_id": "SRC1720_7_685_tau_contract",
        "source_key": "685_tau_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_6_verdict", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1720_8_943_doc",
        "source_key": "943_doc",
        "source_path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["DER943_3_one_Hilbert_current", "conditional definition"],
    },
    {
        "source_id": "SRC1720_9_943_contract",
        "source_key": "943_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_2_matter_functor", "not_parent_signed"],
    },
    {
        "source_id": "SRC1720_10_1045_signature",
        "source_key": "1045_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1720_11_1156_signature",
        "source_key": "1156_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["QMF1156_7_verdict", "QUOTIENT_MATTER_FUNCTOR_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1720_12_1487_owner",
        "source_key": "1487_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1487_ORDINARY_MATTER_SUBACTION_OWNER.csv",
        "needles": ["OMSO1487_1_Hilbert_source", "CONDITIONAL_SOURCE_INPUT"],
    },
    {
        "source_id": "SRC1720_13_1488_current_chain",
        "source_key": "1488_current_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
        "needles": ["OMSCC1488_4_current_chain_verdict", "NOT_CLOSED_WA_RESIDUAL_LOCKED"],
    },
    {
        "source_id": "SRC1720_14_716_derivation",
        "source_key": "716_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
        "needles": ["MCD716_6_current_corpus_verdict", "zero_not_derived"],
    },
    {
        "source_id": "SRC1720_15_same_coframe_parent_clause",
        "source_key": "same_coframe_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_3_source_current_definition", "definition_conditional"],
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
                "exists": yesno(exists),
                "needles_present": yesno(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


def sources_for(keys: set[str]) -> str:
    return ";".join(str(item["source_path"]) for item in SOURCES if item["source_key"] in keys)


MATTER_FUNCTOR_SIGNATURE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_0_parent_quotient_map",
        "required_signature": "parent quotient object q: Phi_parent -> Q_obs exists before readout",
        "mathematical_effect": "vertical v has Dq(v)=0, so representative motion can be invisible only by parent kinematics",
        "source_anchor": "410;1045 MFS1045_0;1156 QMF1156_1",
        "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
        "parent_signed": no(),
        "blocks": "Dq(v)=0 cannot be used as evidence for J_H blindness",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_1_observed_coframe_descent",
        "required_signature": "observed coframe descends through q",
        "mathematical_effect": "e_obs(Phi)=Obs_e(q(Phi)) implies Lie_v e_obs = D Obs_e[Dq(v)] = 0",
        "source_anchor": "943 CFC943_1;1045 MFS1045_1;1156 QMF1156_3",
        "current_status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
        "parent_signed": no(),
        "blocks": "source/readout frame can drift; J_H frame is not owned",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_2_ordinary_matter_functor",
        "required_signature": "ordinary matter subaction is a functor of the observed coframe and fixed representation data",
        "mathematical_effect": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "source_anchor": "622 PMC622_0/2/5;943 CFC943_2;1487 OMSO1487_0",
        "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
        "parent_signed": no(),
        "blocks": "Hilbert current is a conditional definition rather than a parent source",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_3_vertical_matter_lift",
        "required_signature": "vertical action on matter fields is fixed or owned gauge/local-Lorentz/diffeomorphism lift",
        "mathematical_effect": "E_Psi terms vanish on shell and lift terms do not create physical qbar charge",
        "source_anchor": "1045 MFS1045_3;1156 QMF1156_2;1488 OMSCC1488_2",
        "current_status": "VERTICAL_LIFT_NOT_PARENT_SIGNED",
        "parent_signed": no(),
        "blocks": "fixed-Psi choice remains convention rather than theorem",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_4_constants_and_material_standards",
        "required_signature": "masses, charges, alpha, and material constants are quotient-owned or retained as explicit residuals",
        "mathematical_effect": "Lie_v theta_A=0 and Lie_v m_A=0, or b_A/b_alpha rows remain finite",
        "source_anchor": "943 CFC943_3;1045 MFS1045_5;1487 OMSO1487_4",
        "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
        "parent_signed": no(),
        "blocks": "clock/WEP/fine-structure channels can re-enter the source norm",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_5_tau_source_normal_lock",
        "required_signature": "tau, source normal, clock time, boundary charge and orbit readout use the same observed frame",
        "mathematical_effect": "J_H[tau] and rho_H=T_obs(n,tau) are comparable to exterior source/support tests",
        "source_anchor": "684 FLC684_1/4;685 TGC685_6;943 CFC943_5",
        "current_status": "TAU_SOURCE_NORMAL_LOCK_UNSIGNED",
        "parent_signed": no(),
        "blocks": "J_H norm has no declared generator or annulus measure",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_6_no_shadow_or_source_prefactor",
        "required_signature": "no hidden conformal/disformal frame, source-only weight, or post-readout matter prefactor enters S_ord",
        "mathematical_effect": "forbids S_ord=sum_A w_A S_A unless w_A is parent-constant/universal or retained as a residual",
        "source_anchor": "716 MCD716_6;943 CFC943_6;1488 OMSCC1488_3/4",
        "current_status": "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
        "parent_signed": no(),
        "blocks": "a single Hilbert-looking current can still carry species/source weights",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_7_nonHilbert_current_silence",
        "required_signature": "independent connection, torsion, boundary, domain, memory, and range currents are absent, exact zero-flux, or retained",
        "mathematical_effect": "active source is only the observed Hilbert current plus explicitly scored residuals",
        "source_anchor": "449 SC4/SC5;622 PMC622_6;943 FRS943_6",
        "current_status": "NONHILBERT_CURRENT_SILENCE_NOT_PARENT_SIGNED",
        "parent_signed": no(),
        "blocks": "q_nonH and source-normalization residuals stay active",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "signature_id": "MFS1720_8_verdict",
        "required_signature": "MFS1720_0 through MFS1720_7 are signed in one parent branch",
        "mathematical_effect": "then ordinary J_H is parent-owned and can receive a norm/bound without source-frame cheating",
        "source_anchor": "1719;943;1045;1156;1488",
        "current_status": "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED",
        "parent_signed": no(),
        "blocks": "fill nonclaim J_H norm row; do not reopen Newton/local-GR",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


JH_CURRENT_THEOREM_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "JHT1720_0_definition",
        "claim_piece": "observed Hilbert current definition",
        "formal_statement": "T_obs^{mu nu}=2/sqrt(-g_obs) delta S_ord/delta g_obs_munu and J_H[tau]=star(T_obs(tau,.))",
        "current_status": "CONDITIONAL_DEFINITION_ONLY",
        "missing_for_claim": "parent matter functor; observed coframe descent; source-prefactor exclusion",
        "theorem_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "JHT1720_1_Ward_identity",
        "claim_piece": "same-frame Ward conservation",
        "formal_statement": "nabla_mu T_obs^{mu nu}=0 on ordinary matter shell if S_ord has no explicit nonmetric/source arguments",
        "current_status": "CONDITIONAL_STANDARD_IDENTITY_NOT_MASS_NORM",
        "missing_for_claim": "no hidden exchange; no non-Hilbert current; absolute mass projector calibration",
        "theorem_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "JHT1720_2_norm_convention",
        "claim_piece": "J_H norm on compact exterior annulus",
        "formal_statement": "||J_H||_A must specify norm type, volume form, annulus, tau, source normal, units, and source path",
        "current_status": "MISSING_NORM_CONVENTION_AND_VALUE",
        "missing_for_claim": "L1/L2/sup/dual norm; A_ext; volume form; numeric/theorem bound",
        "theorem_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "JHT1720_3_source_prefactor_countermodel",
        "claim_piece": "source-prefactor exclusion",
        "formal_statement": "S_ord=sum_A w_A S_A gives ordinary equations with weighted active source T_source=sum_A w_A T_A unless w_A is forbidden or universal",
        "current_status": "COUNTERMODEL_SURVIVES",
        "missing_for_claim": "no Hom(species/source-label -> source prefactor) parent grammar theorem",
        "theorem_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "JHT1720_4_verdict",
        "claim_piece": "claim-safe observed Hilbert current norm",
        "formal_statement": "||J_H||_A is source-backed only after JHT1720_0 through JHT1720_3 plus annulus/norm data close",
        "current_status": "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED",
        "missing_for_claim": "matter signature; prefactor exclusion; tau lock; norm/value/units",
        "theorem_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


JH_NORM_SOURCE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "JHN1720_0_observed_Hilbert_current_norm_candidate",
        "quantity": "J_H_norm",
        "definition": "norm of observed Hilbert source current on a declared compact exterior annulus",
        "formula": "||J_H||_A = ||star(T_obs(tau,.))||_{A_ext,norm}",
        "system_id": "MISSING_SYSTEM_ID",
        "A_ext": "MISSING_COMPACT_EXTERIOR_ANNULUS",
        "annulus_definition": "MISSING_A_EXT_SURFACE_PAIR_AND_VOLUME_FORM",
        "norm_type": "MISSING_NORM_TYPE_L1_L2_SUP_OR_DUAL",
        "volume_form": "MISSING_OBSERVED_VOLUME_FORM",
        "e_obs_id": "MISSING_PARENT_SIGNED_EOBS",
        "tau_id": "MISSING_PARENT_SIGNED_TAU_OBS",
        "n_source_or_tau": "MISSING_SOURCE_NORMAL_OR_TAU_LOCK",
        "S_matter_source": "MISSING_PARENT_SIGNED_S_ORD",
        "T_obs_definition": "CONDITIONAL_TOBS_EQUALS_2_OVER_SQRT_G_DELTA_SORD_DELTA_GOBS",
        "J_H_norm": "MISSING_NUMERIC_OR_THEOREM_BOUND",
        "units": "MISSING_CURRENT_NORM_UNITS",
        "source_path": sources_for(
            {
                "449_doc",
                "622_contract",
                "684_frame_lock",
                "685_tau_contract",
                "943_contract",
                "1045_signature",
                "1156_signature",
                "1487_owner",
                "1488_current_chain",
                "same_coframe_parent_clause",
            }
        ),
        "equation_ref": "449 W0/W2;519 UOC519_3;622 PMC622_5;684 FLC684_4;685 TGC685_6;943 DER943_3/CFC943_2;1045 MFS1045_6;1156 QMF1156_7;1488 OMSCC1488_4",
        "current_status": "SOURCE_ROW_TEMPLATE_ONLY_NOT_SCORE_READY",
        "blocker_codes": "MISSING_PARENT_MATTER_FUNCTOR;MISSING_SOURCE_PREFACTOR_EXCLUSION;MISSING_TAU_LOCK;MISSING_NORM_VALUE;MISSING_UNITS",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    }
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1720_0_matter_functor_signature",
        "quantity": "parent matter-functor signature",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "PARENT_Q_OBJECT_UNSIGNED;EOBS_DESCENT_UNSIGNED;MATTER_FUNCTOR_UNSIGNED;SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1720_1_JH_norm",
        "quantity": "observed Hilbert current norm",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_NORM_TYPE;MISSING_A_EXT;MISSING_TAU_LOCK;MISSING_SOURCE_CURRENT_VALUE_OR_THEOREM;MISSING_UNITS;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1720_2_N_domain",
        "quantity": "factorized N_domain bound",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "JH_NORM_STILL_MISSING;DPIM_OPERATOR_NORM_MISSING;DELTA_D_MISSING;ANNULUS_MEASURE_MISSING",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1720_3_Newton_GR",
        "quantity": "Newton/local-GR source-normalization reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "OBSERVED_HILBERT_CURRENT_NOT_PARENT_OWNED;M_H_REF_MISSING;R_EQ_MISSING;PPN_VECTOR_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


DECISION_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1720_0_current_verdict",
        "decision": "do not claim observed J_H norm or local-GR reopening",
        "because": "Hilbert current is conditionally definable, but parent matter functor, tau/source lock, and source-prefactor exclusion are unsigned",
        "next_action": "attack source-prefactor exclusion or retain explicit w_A/delta_w_A residual rows",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1720_1_best_route",
        "decision": "next target should hit the coupling bottleneck directly",
        "because": "1488 shows S_ord=sum_A w_A S_A can preserve ordinary equations while changing active source",
        "next_action": "derive no Hom(species/source-label -> gravitational-source prefactor), or create finite source-weight coefficient pack",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1720_0_primary",
        "next_target": "1721-Y5-R2FR-source-prefactor-exclusion-or-wA-current-row.md",
        "script": "scripts/Y5_R2FR_source_prefactor_exclusion_or_wA_current_row.py",
        "objective": "try to prove ordinary matter has no source-only prefactor slot; if not, lock w_A/delta_w_A as explicit nonclaim coupling coefficients",
        "selection_status": "selected",
        "success_condition": "no source-only species/source-weight Hom exists in the parent grammar, or every surviving w_A coefficient is sourced and nonclaim",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1720_1_parallel_norm_fill",
        "next_target": "1721b-Y5-R2FR-JH-norm-convention-and-annulus-source-row-fill.md",
        "script": "scripts/Y5_R2FR_JH_norm_convention_and_annulus_source_row_fill.py",
        "objective": "declare norm type, annulus, volume form, tau and units for the J_H source row without claiming the value",
        "selection_status": "held_parallel",
        "success_condition": "the JHN1720 row becomes syntactically complete while remaining valid_for_claim=false until parent coefficients are real",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1720_0_matter_functor",
        "claim": "ordinary matter functor/coframe/tau package is parent-signed",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "q object, e_obs descent, matter subaction, constants, tau lock, and no-shadow/source-prefactor clauses remain unsigned",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1720_1_JH_norm",
        "claim": "observed Hilbert current norm is source-backed or theorem-bounded",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "JHN1720 row is a template only and lacks norm type, annulus, units, tau lock, and numeric/theorem value",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1720_2_source_prefactor",
        "claim": "source-only matter prefactor is excluded",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "1488 countermodel survives; w_A/delta_w_A must be proved absent/universal or retained",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1720_3_N_domain",
        "claim": "N_domain factorized bound is finite and source-backed",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "J_H norm, C_DPiM, delta_D and annulus measure remain missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1720_4_Newton_local_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "observed Hilbert current is not parent-owned and measured-GM/PPN debts remain open",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_SOURCE_REGISTER.csv",
    "matter_functor_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "jh_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
    "jh_norm_source_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1720_VALIDATION.csv",
}


COPY_MAP = {
    "matter_functor_audit": "R2FR_matter_functor_signature_audit_1720.csv",
    "jh_theorem": "R2FR_JH_current_definition_theorem_1720.csv",
    "jh_norm_source_row": "R2FR_JH_norm_first_source_row_1720.csv",
    "runner_refusal": "R2FR_runner_refusal_1720.csv",
    "decision": "R2FR_decision_ledger_1720.csv",
    "next_target": "R2FR_next_target_1720.csv",
    "claim_gate": "R2FR_claim_gate_1720.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "matter_functor_audit": MATTER_FUNCTOR_SIGNATURE_ROWS,
        "jh_theorem": JH_CURRENT_THEOREM_ROWS,
        "jh_norm_source_row": JH_NORM_SOURCE_ROWS,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "decision": DECISION_ROWS,
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1720_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1720_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "parent_signed",
        "theorem_ready",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def jh_source_paths_exist() -> bool:
    for row in JH_NORM_SOURCE_ROWS:
        paths = [Path(item) for item in row["source_path"].split(";") if item]
        if not paths or any(not path.exists() for path in paths):
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1720_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1720_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1720*"):
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
    audit_rows = rows_map["matter_functor_audit"]
    theorem_rows = rows_map["jh_theorem"]
    norm_rows = rows_map["jh_norm_source_row"]
    runner_rows = rows_map["runner_refusal"]
    decision_rows = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1720_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1720_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1720_2_1719_handoff_preserved",
            any(row["source_key"] == "1719_doc" and row["needles_present"] == "True" for row in source_rows),
            "1719 selected 1720 as primary J_H route",
            "1719 handoff missing",
        ),
        check(
            "VAL1720_3_matter_functor_unsigned",
            any(row["signature_id"] == "MFS1720_8_verdict" and row["current_status"] == "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED" for row in audit_rows),
            "matter-functor signature remains unsigned",
            "matter-functor verdict missing or promoted",
        ),
        check(
            "VAL1720_4_JH_theorem_conditional_only",
            any(row["theorem_id"] == "JHT1720_4_verdict" and row["current_status"] == "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED" for row in theorem_rows),
            "observed Hilbert current theorem remains conditional only",
            "J_H theorem was promoted or verdict missing",
        ),
        check(
            "VAL1720_5_source_prefactor_block_retained",
            any(row["theorem_id"] == "JHT1720_3_source_prefactor_countermodel" and row["current_status"] == "COUNTERMODEL_SURVIVES" for row in theorem_rows),
            "source-prefactor countermodel remains retained",
            "source-prefactor countermodel not recorded",
        ),
        check(
            "VAL1720_6_JH_norm_row_nonclaim",
            len(norm_rows) == 1 and all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in norm_rows),
            "first J_H norm source row exists and remains nonclaim",
            "J_H norm source row missing or claim-enabled",
        ),
        check(
            "VAL1720_7_JH_source_paths_exist",
            jh_source_paths_exist(),
            "all source paths listed in J_H norm row exist",
            "one or more J_H norm source paths missing",
        ),
        check(
            "VAL1720_8_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses matter functor, J_H norm, N_domain and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1720_9_decision_selects_coupling_route",
            any(row["decision_id"] == "DEC1720_1_best_route" and "prefactor" in row["next_action"] for row in decision_rows),
            "decision ledger selects source-prefactor/coupling route",
            "decision ledger does not select coupling route",
        ),
        check(
            "VAL1720_10_next_selected",
            any(row["route_id"] == "NEXT1720_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects source-prefactor exclusion or w_A row",
            "next target missing selected primary route",
        ),
        check(
            "VAL1720_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1720_12_csv_parse", parsed_ok, "all generated 1720 CSVs parse", "one or more generated 1720 CSVs failed to parse"),
        check("VAL1720_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1720_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1720_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1720_16_formalization_untouched", formalization_untouched(), "no 1720 outputs found under formalization-workbench", "1720 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1720_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1720 observed Hilbert current norm and matter-functor signature validation" if overall else "one or more 1720 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1720 attacks the `J_H` side of the 1719 factorized numerator bound.",
        "- The observed Hilbert current is mathematically definable only conditionally: `T_obs` comes from varying the ordinary matter action with respect to the same observed coframe, and `J_H[tau]=star(T_obs(tau,.))` only becomes physical after the parent matter functor, coframe descent, tau/source lock, and no-shadow/source-prefactor clauses are signed.",
        "- The strongest obstruction is now the coupling slot: a source-only prefactor `S_ord=sum_A w_A S_A` can leave ordinary matter equations looking acceptable while changing the active gravitational source.",
        "- Therefore `||J_H||_A` is not source-backed yet. A first nonclaim source row is created with the missing annulus, norm, tau, units, and parent-source fields explicit.",
        "- No Newton, local-GR, R10, PPN, WEP, clock, orbital, source-normalization or `q_loc`-zero claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Matter-Functor Signature Audit",
        markdown_table(rows_map["matter_functor_audit"], ["signature_id", "required_signature", "mathematical_effect", "current_status", "parent_signed", "blocks"]),
        "",
        "## Observed Hilbert Current Theorem",
        markdown_table(rows_map["jh_theorem"], ["theorem_id", "claim_piece", "formal_statement", "current_status", "missing_for_claim", "theorem_ready"]),
        "",
        "## JH Norm First Source Row",
        markdown_table(rows_map["jh_norm_source_row"], ["row_id", "quantity", "formula", "norm_type", "tau_id", "J_H_norm", "units", "current_status", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1720 is a useful failure, not a defeat. It says the Hilbert-current route is real, but the project cannot yet treat `J_H` as the unique parent-owned source because the matter functor and coupling grammar are not signed. The next best move is to attack the source-only prefactor: prove the parent language has no `w_A` slot, or keep `w_A/delta w_A` as explicit finite coupling coefficients. That is the cleanest way to avoid smuggling GR/local-source universality by assumption.",
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
    doc_path = ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1720_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1720 validation FAIL")
    print("1720 validation PASS")


if __name__ == "__main__":
    main()
