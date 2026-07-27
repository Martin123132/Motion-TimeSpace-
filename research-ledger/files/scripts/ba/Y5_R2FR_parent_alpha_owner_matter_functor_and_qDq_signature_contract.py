from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1811"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1811-Y5-R2FR-parent-alpha-owner-matter-functor-and-qDq-signature-contract.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1811_0_1810_doc",
        "source_key": "1810_doc",
        "source_path": ROOT / "1810-Y5-R2FR-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
        "needles": ["NEXT1810_0_primary", "PSC1810_6_verdict"],
        "role": "1810 handoff to parent alpha-owner/matter-functor/qDq signature contract.",
    },
    {
        "source_id": "SRC1811_1_1810_validation",
        "source_key": "1810_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1810_VALIDATION.csv",
        "needles": ["VAL1810_OVERALL", "PASS"],
        "role": "confirms 1810 passed before 1811 starts.",
    },
    {
        "source_id": "SRC1811_2_1810_parent_contract",
        "source_key": "1810_parent_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_PARENT_SIGNATURE_CONTRACT.csv",
        "needles": ["PSC1810_6_verdict", "PARENT_SIGNATURE_NOT_CLOSED"],
        "role": "current parent signature contract clauses.",
    },
    {
        "source_id": "SRC1811_3_1810_zero_theorem",
        "source_key": "1810_zero_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_BETA_SOURCE_ALPHA_ZERO_THEOREM_AUDIT.csv",
        "needles": ["BZA1810_8_verdict", "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
        "role": "current beta_source_alpha zero-theorem audit.",
    },
    {
        "source_id": "SRC1811_4_1055_doc",
        "source_key": "1055_alpha_matter_contract",
        "source_path": ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
        "needles": ["PAC1055_1_EM_owner", "DEC1055_1_not_derivation_yet"],
        "role": "older alpha-owner and matter-functor parent action contract.",
    },
    {
        "source_id": "SRC1811_5_1055_validation",
        "source_key": "1055_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1055_VALIDATION.csv",
        "needles": ["V1055_SUMMARY", "pass"],
        "role": "confirms old alpha/matter contract was validated as nonclaim.",
    },
    {
        "source_id": "SRC1811_6_1055_parent_action",
        "source_key": "1055_parent_action_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "needles": ["PAC1055_6_single_parent_action", "PAC1055_1_EM_owner"],
        "role": "minimal parent action contract candidate.",
    },
    {
        "source_id": "SRC1811_7_1055_adoption_gates",
        "source_key": "1055_adoption_gates",
        "source_path": RESIDUALS / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
        "needles": ["ADG1055_1_alpha_owner", "BEST_ROUTE_NOT_PROVED"],
        "role": "adoption gates that block using the contract as a theorem.",
    },
    {
        "source_id": "SRC1811_8_1055_consequences",
        "source_key": "1055_consequences",
        "source_path": RESIDUALS / "P8_Y5_R10_1055_THEOREM_CONSEQUENCES.csv",
        "needles": ["TC1055_2_beta_source_alpha", "CONDITIONAL_ONLY"],
        "role": "conditional consequences if parent contract is signed.",
    },
    {
        "source_id": "SRC1811_9_1055_counterexamples",
        "source_key": "1055_counterexamples",
        "source_path": RESIDUALS / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["CE1055_0_gauge_kinetic_function", "CE1055_3_relative_source_weight"],
        "role": "counterexamples that remain legal if contract is unsigned.",
    },
    {
        "source_id": "SRC1811_10_1781_doc",
        "source_key": "1781_qDq_doc",
        "source_path": ROOT / "1781-Y5-R2FR-parent-q-Dq-matrix-first-row-or-Obs-e-factorisation-proof.md",
        "needles": ["QDM1781_7_verdict", "OEF1781_4_current_verdict"],
        "role": "current q/Dq matrix and Obs_e factorisation proof attempt.",
    },
    {
        "source_id": "SRC1811_11_1781_validation",
        "source_key": "1781_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1781_VALIDATION.csv",
        "needles": ["VAL1781_OVERALL", "PASS"],
        "role": "confirms q/Dq checkpoint passed as nonclaim.",
    },
    {
        "source_id": "SRC1811_12_1781_qdq_gate",
        "source_key": "1781_qdq_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_Q_DQ_MATRIX_GATE.csv",
        "needles": ["QDM1781_7_verdict", "Q_DQ_MATRIX_NOT_CONSTRUCTED_OBS_E_FACTORISATION_NOT_SIGNED"],
        "role": "q/Dq matrix gate and current blocker.",
    },
    {
        "source_id": "SRC1811_13_1781_obs_theorem",
        "source_key": "1781_obs_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_OBS_E_FACTORISATION_THEOREM_ATTEMPT.csv",
        "needles": ["OEF1781_0_chain_rule_theorem", "OEF1781_4_current_verdict"],
        "role": "Obs_e(q) chain-rule theorem and current fail verdict.",
    },
    {
        "source_id": "SRC1811_14_1781_first_rows",
        "source_key": "1781_Dq_DObs_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_DQ_OBS_E_FIRST_ROW_SCHEMA.csv",
        "needles": ["DQR1781_5_total_q_dq_obs_abs", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
        "role": "finite Dq/DObs_e fallback row schema.",
    },
    {
        "source_id": "SRC1811_15_1720_doc",
        "source_key": "1720_matter_doc",
        "source_path": ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
        "needles": ["MFS1720_8_verdict", "CG1720_4_Newton_local_GR"],
        "role": "matter functor/Hilbert current source route.",
    },
    {
        "source_id": "SRC1811_16_1720_matter_signature",
        "source_key": "1720_matter_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_8_verdict", "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED"],
        "role": "current matter functor signature blocker.",
    },
    {
        "source_id": "SRC1811_17_1738_doc",
        "source_key": "1738_coframe_doc",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["DEC1738_1_same_coframe_warning", "DEC1738_2_current_status"],
        "role": "same-frame-is-not-enough warning and DObs_e blocker.",
    },
    {
        "source_id": "SRC1811_18_1802_doc",
        "source_key": "1802_readout_doc",
        "source_path": ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
        "needles": ["MRT1802_7_verdict", "CL1802_3_local_GR_Newton"],
        "role": "matter/readout no-reentry theorem and local GR blocker.",
    },
    {
        "source_id": "SRC1811_19_1802_matter_readout",
        "source_key": "1802_matter_readout_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
        "needles": ["MRT1802_7_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "matter/readout theorem gate.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_SOURCE_REGISTER.csv",
    "parent_signature_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_PARENT_SIGNATURE_THEOREM.csv",
    "antecedent_closure_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_ANTECEDENT_CLOSURE_MATRIX.csv",
    "alpha_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_ALPHA_OWNER_AUDIT.csv",
    "matter_functor_qdq_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_MATTER_FUNCTOR_QDQ_AUDIT.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_GR_NEWTON_IMPACT_LEDGER.csv",
    "residual_fallback": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_RESIDUAL_FALLBACK_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_COUNTERMODEL_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1811_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        needles = source["needles"]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def parent_signature_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_0_statement",
            "claim": "parent signature implies alpha/source/matter vertical silence",
            "mathematical_statement": "If q is parent-owned, v in ker(Dq), e_obs=Obs_e(q), S_ord descends through e_obs(q) and fixed theta_A, alpha_EM=alpha_*(ell_EM) with Lie_v ell_EM=0, no source-only/shadow/readout coefficient exists, and tau/readout/boundary maps descend through q, then delta_v S_ord=0, Lie_v alpha_EM=0, beta_source_alpha=0 and ordinary matter contributes no hidden source charge.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "ANTECEDENTS_NOT_JOINTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_1_chain_rule",
            "claim": "observed geometry variation vanishes",
            "mathematical_statement": "delta_v e_obs = DObs_e|_q[Dq[v]], so Dq[v]=0 gives delta_v e_obs=0 when Obs_e(q) is parent-owned.",
            "proof_status": "VALID_DIFFERENTIAL_CHAIN_RULE",
            "current_corpus_status": "QDM1781_7 and OEF1781_4 fail current parent proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_2_matter_variation",
            "claim": "ordinary matter carries no vertical source charge",
            "mathematical_statement": "delta_v S_ord = integral E_Psi delta_v Psi + 1/2 integral sqrt(-g) T_obs^{mu nu} delta_v g_obs_munu + sum_A partial_theta S_A Lie_v theta_A; on shell/gauge lift, delta_v g_obs=0 and Lie_v theta_A=0 imply delta_v S_ord=0.",
            "proof_status": "EXACT_CONDITIONAL_VARIATION",
            "current_corpus_status": "matter functor, vertical lift, constants and no-shadow clauses unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_3_alpha_owner",
            "claim": "alpha_EM is not an Xhat/source marker",
            "mathematical_statement": "alpha_EM=alpha_*(ell_EM) with ell_EM fixed by representation/topological/fibre metric data and Lie_v ell_EM=0; no f(Xhat)F^2 term is allowed.",
            "proof_status": "SUFFICIENT_CONTRACT_WRITTEN",
            "current_corpus_status": "alpha owner route not derived from deeper MTS primitives",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_4_source_functor",
            "claim": "active source is species-blind Hilbert source",
            "mathematical_statement": "T_total=sum_A 2/sqrt(-g_obs) delta S_A/delta g_obs and no map Obj(C_matter)->(T_A,A)->kappa_A T_A is available before source coupling.",
            "proof_status": "SUFFICIENT_CONTRACT_WRITTEN",
            "current_corpus_status": "source-label forgetting and no-source-only slot theorem not parent-derived",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_5_tau_readout_boundary",
            "claim": "arena projections do not reopen the source charge",
            "mathematical_statement": "Dsource_readout[Dq(v)]=0, tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary, and Pi_local delta_v B_A=0, or finite residual rows absorb violations.",
            "proof_status": "SUFFICIENT_CONTRACT_WRITTEN",
            "current_corpus_status": "tau role lock, source/readout and boundary silence missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PST1811_6_verdict",
            "claim": "current corpus proves the parent signature theorem",
            "mathematical_statement": "PST1811_1 through PST1811_5 are all parent-signed in one branch",
            "proof_status": "THEOREM_CONTRACT_NOT_CURRENT_PROOF",
            "current_corpus_status": "FAIL_CURRENT_CLAIM_KEEP_RESIDUAL_ROWS",
            "valid_for_claim": False,
        },
    ]


def antecedent_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_0_parent_field_chart",
            "antecedent": "parent field chart and Q_vis columns are owned",
            "source_anchor": "QDM1781_0_parent_field_chart; QDM1781_1_Qvis_column_contract",
            "current_status": "CANDIDATE_ONLY",
            "would_close": "lets q and Dq be represented as an actual parent matrix rather than prose",
            "needed_evidence": "one parent action chart or chart-equivalent construction with included/excluded variables",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_1_Dq_kernel",
            "antecedent": "retained coupling directions are in ker(Dq)",
            "source_anchor": "QDM1781_2_vertical_basis_rows; QDM1781_3_Dq_matrix_object",
            "current_status": "MISSING_DQ_MATRIX_VALUES_OR_THEOREM_ZEROS",
            "would_close": "permits the chain-rule zero for observed coframe and source/readout columns",
            "needed_evidence": "Dq matrix cells zero by theorem or finite component values with units and norms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_2_Obs_e",
            "antecedent": "observed coframe is Obs_e(q) with no common-frame residual",
            "source_anchor": "QDM1781_4_Obs_e_factorisation; DEC1738_1_same_coframe_warning",
            "current_status": "FACTORISATION_NOT_PARENT_SIGNED",
            "would_close": "turns same-frame structure into real metric invisibility",
            "needed_evidence": "Obs_e(q) owner plus b_g,X=0 theorem or finite b_g row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_3_alpha_owner",
            "antecedent": "EM kinetic normalization is fixed representation/topological data",
            "source_anchor": "PAC1055_1_EM_owner; ADG1055_1_alpha_owner",
            "current_status": "BEST_ROUTE_NOT_PROVED",
            "would_close": "kills b_alpha and alpha-marker source coupling",
            "needed_evidence": "derive g_* from vertical-generator norm, topological level, index, or fixed parent fibre metric",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_4_matter_functor",
            "antecedent": "ordinary matter action descends through e_obs(q), owned connection, and fixed theta_A",
            "source_anchor": "MFS1720_2_ordinary_matter_functor; MRT1802_2_matter_functor_lift",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "would_close": "prevents hidden mass/material/clock beta rows from ordinary matter",
            "needed_evidence": "parent matter bundle/category and fixed/gauge vertical lift for ordinary species",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_5_constants_markers",
            "antecedent": "alpha, masses, clocks, material labels and standards are quotient-owned or residual-bounded",
            "source_anchor": "MFS1720_4_constants_and_material_standards; QRC1802_1_qbar_marker_constants",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "would_close": "blocks marker reentry in clock, WEP and particle sectors",
            "needed_evidence": "constant superselection theorem or source-backed qbar_marker/qbar_constants rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_6_no_source_weight",
            "antecedent": "no source-only species/action prefactor or non-Hilbert bypass",
            "source_anchor": "PAC1055_4_source_label_forgetting; MFS1720_6_no_shadow_or_source_prefactor",
            "current_status": "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
            "would_close": "removes Delta_w_A/source-weight branch without fitting",
            "needed_evidence": "object-language/action-measure/current-owner theorem or finite Delta_w rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_7_readout_boundary",
            "antecedent": "readout, boundary and worldtube maps are pure postprocessing or descend through q",
            "source_anchor": "MRT1802_5_general_readout; QDM1781_5_source_readout_columns",
            "current_status": "GENERAL_THEOREM_BLOCKED",
            "would_close": "stops post-variation regeneration of source/alpha markers",
            "needed_evidence": "readout type theorem per arena or finite C_R[A]/worldtube/boundary rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_8_tau_role_lock",
            "antecedent": "source, charge, clock, orbit and boundary tau roles are one q-projectable generator",
            "source_anchor": "MFS1720_5_tau_source_normal_lock; PSC1810_4_tau_role_lock",
            "current_status": "TAU_SOURCE_NORMAL_LOCK_UNSIGNED",
            "would_close": "permits cross-arena normalization instead of arena-by-arena tau fitting",
            "needed_evidence": "tau pushforward/role-lock certificate or source-backed tau residual rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "antecedent_id": "ACM1811_9_verdict",
            "antecedent": "all parent signature antecedents close together",
            "source_anchor": "PST1811_6_verdict",
            "current_status": "NOT_CLOSED",
            "would_close": "would promote beta_source_alpha=0 and clean part of the source side of GR/Newton",
            "needed_evidence": "ACM1811_0 through ACM1811_8 all theorem-zero/source-backed with no placeholders",
            "valid_for_claim": False,
        },
    ]


def alpha_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "AO1811_0_fixed_level",
            "candidate_owner": "fixed representation/topological/fibre metric level ell_EM",
            "would_imply": "Lie_v alpha_EM=0 and no b_alpha from ordinary vertical motion",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "missing_for_claim": "explicit map alpha_EM=alpha_*(ell_EM) and proof Lie_v ell_EM=0 from MTS primitives",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "AO1811_1_forbid_fX_F2",
            "candidate_owner": "operator-domain ban on f(Xhat)F_Q^2",
            "would_imply": "no scalar gauge kinetic counterterm reopens alpha drift",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "hidden-visible Hom ban or typed coefficient-domain exhaustion theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "AO1811_2_radiative_readout",
            "candidate_owner": "radiative/EFT/readout closure preserves alpha owner",
            "would_imply": "loops/clock maps do not regenerate f_X F^2 or clock_Xhat marker",
            "current_status": "UNSIGNED",
            "missing_for_claim": "renormalized visible sector closure and clock/readout domain theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "AO1811_3_verdict",
            "candidate_owner": "alpha_EM parent owner",
            "would_imply": "b_alpha=0 for the source-alpha branch and removes the alpha WEP/R10 marker route",
            "current_status": "ALPHA_OWNER_NOT_DERIVED",
            "missing_for_claim": "AO1811_0 through AO1811_2 closed from parent primitives",
            "valid_for_claim": False,
        },
    ]


def matter_functor_qdq_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MFQ1811_0_parent_qDq",
            "object": "q/Dq matrix",
            "current_status": "Q_DQ_MATRIX_NOT_CONSTRUCTED_OBS_E_FACTORISATION_NOT_SIGNED",
            "mathematical_role": "defines which parent variations are genuinely invisible to observed matter/source/readout",
            "missing_for_claim": "field chart, Q_vis columns, vertical basis, Dq cells and norms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MFQ1811_1_coframe",
            "object": "e_obs(q)",
            "current_status": "DOBS_E_KERNEL_NOT_CLOSED",
            "mathematical_role": "turns representative vertical motion into zero observed metric variation",
            "missing_for_claim": "parent coframe ownership and no common-frame derivative b_g,X",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MFQ1811_2_matter",
            "object": "S_ord matter functor",
            "current_status": "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED",
            "mathematical_role": "makes Hilbert current a parent-owned source rather than a definition with hidden prefactors",
            "missing_for_claim": "matter category, fixed vertical lift, constants/markers and no source-prefactor theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MFQ1811_3_readout",
            "object": "readout/no-reentry",
            "current_status": "JMatter_READOUT_NOT_ZERO_AND_NOT_BOUNDED",
            "mathematical_role": "prevents detector/source/orbit maps from recreating source charges after variation",
            "missing_for_claim": "pure postprocessing typing or finite readout/source-worldtube coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MFQ1811_4_verdict",
            "object": "matter functor plus q/Dq package",
            "current_status": "PACKAGE_UNSIGNED",
            "mathematical_role": "would be the actual source-side bridge toward GR/Newton",
            "missing_for_claim": "MFQ1811_0 through MFQ1811_3 closed simultaneously",
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1811_0_WEP",
            "if_signed": "beta_source_alpha=0 and no source-only Delta_w_A branch for ordinary matter",
            "would_buy": "WEP alpha/source marker route is killed by theorem rather than tuned",
            "still_missing": "tau_WEP/readout/material rows for any retained non-alpha residual channel",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1811_1_R10",
            "if_signed": "alpha-marker beta_s beta_t branch vanishes before Yukawa comparison",
            "would_buy": "R10 alpha-marker branch demoted to zero theorem, leaving only independently retained tails",
            "still_missing": "lambda/Z/K/tau_R10 and claim-valid bound curve for non-alpha finite channels",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1811_2_Newton_source",
            "if_signed": "ordinary matter source is universal Hilbert current in the observed frame",
            "would_buy": "source side of Newton/GR becomes cleaner: no species source prefactor or hidden active mass",
            "still_missing": "left-hand Einstein/EH limit, Poisson normalization, measured-G guard and boundary/support terms",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1811_3_PPN",
            "if_signed": "q/Dq/coframe/tau/source roles become one parent signature",
            "would_buy": "PPN residual vector can be organized as finite tails rather than arbitrary couplings",
            "still_missing": "PPN response matrix, gauge/profile split and no-cancellation envelope",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1811_4_verdict",
            "if_signed": "1811 would close a major source-side bridge",
            "would_buy": "serious progress toward MTS -> GR/Newton, but not the full reduction by itself",
            "still_missing": "parent antecedents are not signed, so all local claims remain refused",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_0_Dq_matrix",
            "quantity": "epsilon_Dq_abs",
            "definition": "absolute no-cancellation norm of retained Dq cells over Q_vis columns",
            "required_columns": "direction_id; q_column; Dq_value_or_zero_theorem; norm; units; source_path; valid_for_claim",
            "current_status": "MISSING_DQ_MATRIX_VALUES_OR_THEOREM_ZEROS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_1_DObs_e",
            "quantity": "epsilon_DObs_e_abs",
            "definition": "coframe/common-frame leakage including b_g,X if Obs_e(q) does not close",
            "required_columns": "direction_id; DObs_e_value; b_g_component; coframe_norm; units; source_path; valid_for_claim",
            "current_status": "MISSING_PARENT_Q_DQ_OBS_E_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_2_alpha_marker",
            "quantity": "epsilon_alpha_owner_abs",
            "definition": "absolute alpha/charge/clock/material marker leakage along retained directions",
            "required_columns": "marker_id; Lie_v_marker; coefficient; units; source_path; valid_for_claim",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_3_source_weight",
            "quantity": "epsilon_source_weight_abs",
            "definition": "source-only action prefactor or non-Hilbert source bypass envelope",
            "required_columns": "species_or_source_id; Delta_w_A; beta_w; zeta_nonH; units; source_path; valid_for_claim",
            "current_status": "MISSING_SOURCE_PREFACTOR_THEOREM_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_4_tau_readout_boundary",
            "quantity": "epsilon_tau_readout_boundary_abs",
            "definition": "tau role split, readout reentry, worldtube and boundary leakage",
            "required_columns": "tau_role_components; C_R[A]; worldtube_support; boundary_term; units; source_path; valid_for_claim",
            "current_status": "MISSING_TAU_READOUT_BOUNDARY_COMPONENTS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RFB1811_5_total",
            "quantity": "epsilon_parent_signature_abs",
            "definition": "absolute no-cancellation envelope for failed parent signature",
            "required_columns": "RFB1811_0..RFB1811_4 values; common normalizer; units; no_cancellation_flag; source_paths",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1811_0_gauge_kinetic",
            "countermodel": "f(Xhat)F_Q^2",
            "why_it_defeats_claim": "gauge/diffeomorphism invariance allow scalar gauge kinetic functions unless coefficient domain forbids them",
            "blocked_by": "alpha owner plus no hidden-visible coefficient theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1811_1_common_frame",
            "countermodel": "e_obs=exp(b_g X)e0(q)",
            "why_it_defeats_claim": "all matter can see one frame while that frame still depends on residual variables",
            "blocked_by": "Obs_e(q) parent factorisation and b_g=0 theorem or finite b_g row",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1811_2_shadow_matter",
            "countermodel": "A_A(X)^2 g_obs, D_A(X), or m_A(X) psi_bar psi",
            "why_it_defeats_claim": "ordinary covariance does not forbid shadow frames/mass functions",
            "blocked_by": "matter functor/no-shadow theorem or finite coefficients",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1811_3_source_weight",
            "countermodel": "sum_A w_A(X) S_A or kappa_A T_A source coupling",
            "why_it_defeats_claim": "same-looking matter equations can carry different active source weights",
            "blocked_by": "source-label forgetting, no-source-only slot and current-owner theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1811_4_readout_reentry",
            "countermodel": "pre-action readout/effective map regenerates marker/source coefficients",
            "why_it_defeats_claim": "pure postprocessing is safe, but general readout/effective action is not automatically pure",
            "blocked_by": "readout no-reentry theorem per arena or finite C_R[A] rows",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1811_0_theorem_contract",
            "gate": "parent signature theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "PST1811 exact conditional theorem is explicit",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1811_1_parent_antecedents",
            "gate": "all antecedents are parent-signed",
            "current_status": "BLOCKED",
            "reason": "ACM1811_9 remains NOT_CLOSED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1811_2_residual_rows",
            "gate": "failed antecedents have source-backed residual values",
            "current_status": "BLOCKED",
            "reason": "RFB1811 rows contain MISSING component values/norms/source paths",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1811_3_local_promotion",
            "gate": "local GR/Newton/WEP/R10 promotion is allowed",
            "current_status": "REFUSED",
            "reason": "theorem antecedents and finite residual fallbacks are both incomplete",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1811_0_parent_signature",
            "claim": "parent alpha-owner/matter-functor/qDq signature is proved",
            "status": "BLOCKED",
            "reason": "PST1811_6 is contract-only and ACM1811_9 is not closed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1811_1_beta_source_alpha",
            "claim": "beta_source_alpha=0 is a current theorem",
            "status": "BLOCKED",
            "reason": "alpha owner, matter functor, qDq and no-source-only clauses remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1811_2_WEP_R10",
            "claim": "WEP/R10 alpha/source branches pass",
            "status": "BLOCKED",
            "reason": "parent zero theorem not signed and finite arena residual rows remain missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1811_3_Newton_source",
            "claim": "Newton source side is derived",
            "status": "BLOCKED",
            "reason": "Hilbert source owner, no source weights, tau/source normal and boundary support remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1811_4_local_GR",
            "claim": "local GR/PPN follows",
            "status": "REFUSED",
            "reason": "even signed source-side theorem would still need left-hand EH/PPN response closure",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1811_0_theorem_result",
            "decision": "PARENT_SIGNATURE_THEOREM_EXACT_CONDITIONAL",
            "reason": "chain rule plus matter variation gives the desired zero result if q/Dq, Obs_e, alpha owner, matter functor, source, tau and readout clauses are parent-signed",
            "next_action": "keep theorem as a contract, not a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1811_1_current_status",
            "decision": "PARENT_SIGNATURE_NOT_SIGNED",
            "reason": "the exact theorem's antecedents are still candidate-only, unsigned, or missing source-backed values",
            "next_action": "do not promote beta_source_alpha, WEP, R10, PPN or local-GR claims",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1811_2_residual_status",
            "decision": "RESIDUAL_FALLBACK_SCHEMA_READY_NONCLAIM",
            "reason": "failed antecedents now map to concrete residual rows: Dq, DObs_e, alpha markers, source weights and tau/readout/boundary leakage",
            "next_action": "fill no residual without units, source paths, common normalizer and no-cancellation flag",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1811_3_best_next",
            "decision": "FIELD_CHART_QVIS_AND_ALPHA_LEVEL_OWNER_NEXT",
            "reason": "q/Dq cells cannot be filled until parent chart/Q_vis columns are owned, and alpha cannot be silenced until ell_EM/g_* ownership is derived",
            "next_action": "1812-Y5-R2FR-parent-field-chart-Qvis-and-alpha-level-owner-or-first-residual-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1811_0_primary",
            "next_target": "1812-Y5-R2FR-parent-field-chart-Qvis-and-alpha-level-owner-or-first-residual-row.md",
            "script": "scripts/Y5_R2FR_parent_field_chart_Qvis_and_alpha_level_owner_or_first_residual_row.py",
            "objective": "try to parent-own the field chart, Q_vis columns, and EM level/fibre metric owner in one package; if not, emit the first source-backed residual row for Dq/DObs_e or alpha-marker leakage",
            "selection_status": "selected",
            "success_condition": "field chart/Q_vis/ell_EM owner is theorem-zero, or at least one residual component row has units, source path, common normalizer, and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1811_1_parallel",
            "next_target": "1812b-Y5-R2FR-no-source-weight-and-readout-boundary-component-pack.md",
            "script": "scripts/Y5_R2FR_no_source_weight_and_readout_boundary_component_pack.py",
            "objective": "prepare source-weight, readout, worldtube and boundary residual rows if the parent signature cannot be theorem-zero",
            "selection_status": "held_parallel",
            "success_condition": "Delta_w/C_R/worldtube/boundary rows are source-backed or explicitly blocked",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_signature_theorem": parent_signature_theorem_rows(),
        "antecedent_closure_matrix": antecedent_closure_rows(),
        "alpha_owner_audit": alpha_owner_rows(),
        "matter_functor_qdq_audit": matter_functor_qdq_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "residual_fallback": residual_fallback_rows(),
        "countermodel_ledger": countermodel_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if row.get("gate_id") == "AC1811_0_theorem_contract":
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("claim_allowed_now", False))
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1811_0_theorem_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1811_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1811_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1811_2_theorem_contract_exact",
            any(row["theorem_id"] == "PST1811_0_statement" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["parent_signature_theorem"]),
            "parent signature theorem is written as an exact conditional",
        ),
        (
            "VAL1811_3_theorem_not_promoted",
            any(row["theorem_id"] == "PST1811_6_verdict" and row["proof_status"] == "THEOREM_CONTRACT_NOT_CURRENT_PROOF" for row in rows_map["parent_signature_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["parent_signature_theorem"]),
            "parent signature theorem is not promoted as a current proof",
        ),
        (
            "VAL1811_4_antecedents_complete_blocked",
            any(row["antecedent_id"] == "ACM1811_9_verdict" and row["current_status"] == "NOT_CLOSED" for row in rows_map["antecedent_closure_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["antecedent_closure_matrix"]),
            "all required antecedents are represented and verdict remains blocked",
        ),
        (
            "VAL1811_5_alpha_owner_not_derived",
            any(row["alpha_id"] == "AO1811_3_verdict" and row["current_status"] == "ALPHA_OWNER_NOT_DERIVED" for row in rows_map["alpha_owner_audit"]),
            "alpha owner remains not derived",
        ),
        (
            "VAL1811_6_matter_qdq_unsigned",
            any(row["audit_id"] == "MFQ1811_4_verdict" and row["current_status"] == "PACKAGE_UNSIGNED" for row in rows_map["matter_functor_qdq_audit"]),
            "matter-functor plus qDq package remains unsigned",
        ),
        (
            "VAL1811_7_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1811_8_residual_fallback_nonclaim",
            any(row["residual_id"] == "RFB1811_5_total" for row in rows_map["residual_fallback"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["residual_fallback"]),
            "residual fallback schema is staged and nonclaim",
        ),
        (
            "VAL1811_9_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "known countermodels remain retained",
        ),
        (
            "VAL1811_10_acceptance_blocks",
            any(row["gate_id"] == "AC1811_0_theorem_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate allows contract-only progress but blocks claims",
        ),
        (
            "VAL1811_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all signature/local claim gates remain blocked",
        ),
        ("VAL1811_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1811_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1811_14_decision_next",
            any(row["decision_id"] == "DEC1811_3_best_next" and row["decision"] == "FIELD_CHART_QVIS_AND_ALPHA_LEVEL_OWNER_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects field-chart/Qvis and alpha-level owner next",
        ),
        (
            "VAL1811_15_next_selected",
            any(row["route_id"] == "NEXT1811_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1811_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1811 CSVs parse"),
        ("VAL1811_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1811_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1811_19_formalization_untouched", formalization_untouched(), "no 1811 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1811_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1811 parent alpha-owner matter-functor qDq signature contract checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1811 Y5 R2FR parent alpha-owner matter-functor and qDq signature contract",
            "",
            "**Progress:** the parent-signature route is now a theorem contract, not a vague hope. If `q`, `Dq`, `Obs_e(q)`, the matter functor, the EM owner, source-label forgetting, tau role-lock, and readout/boundary silence are all signed by one parent action, the source-alpha coupling vanishes by chain rule and ordinary matter variation.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. The work is getting sharper: we now know precisely what must be derived before MTS can claim the source side of the GR/Newton limit. The missing pieces are not random anymore; they are named antecedents and residual rows.",
            "",
            "**Claim ceiling:** no beta_source_alpha zero claim, no WEP/R10/PPN/local-GR/Newton pass, no source-current closure, no unity tau shortcut, no GitHub action, and no `formalization-workbench` edit is allowed from 1811.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Parent Signature Theorem",
            markdown_table(rows_map["parent_signature_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Antecedent Closure Matrix",
            markdown_table(rows_map["antecedent_closure_matrix"], ["antecedent_id", "antecedent", "current_status", "would_close", "needed_evidence", "valid_for_claim"]),
            "",
            "## Alpha Owner Audit",
            markdown_table(rows_map["alpha_owner_audit"], ["alpha_id", "candidate_owner", "would_imply", "current_status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Matter Functor qDq Audit",
            markdown_table(rows_map["matter_functor_qdq_audit"], ["audit_id", "object", "current_status", "mathematical_role", "missing_for_claim", "valid_for_claim"]),
            "",
            "## GR/Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_signed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Residual Fallback Schema",
            markdown_table(rows_map["residual_fallback"], ["residual_id", "quantity", "definition", "required_columns", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "why_it_defeats_claim", "blocked_by", "retained", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is genuinely useful. The bridge to GR/Newton is no longer 'make the coupling small'; it is 'derive the parent signature that makes the dangerous coupling illegal'. If that fails, the fallback is not defeat either: it becomes a finite residual vector with units, source paths, and no-cancellation guards. That is the disciplined route.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1811 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
