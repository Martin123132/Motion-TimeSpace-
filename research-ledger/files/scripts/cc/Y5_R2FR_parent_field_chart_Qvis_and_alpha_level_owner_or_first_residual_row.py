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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1812"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1812-Y5-R2FR-parent-field-chart-Qvis-and-alpha-level-owner-or-first-residual-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1812_0_1811_doc",
        "source_key": "1811_handoff_doc",
        "source_path": ROOT / "1811-Y5-R2FR-parent-alpha-owner-matter-functor-and-qDq-signature-contract.md",
        "needles": ["NEXT1811_0_primary", "DEC1811_3_best_next"],
        "role": "1811 selects field-chart/Qvis and alpha-level owner as the next source-side target.",
    },
    {
        "source_id": "SRC1812_1_1811_validation",
        "source_key": "1811_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1811_VALIDATION.csv",
        "needles": ["VAL1811_OVERALL", "PASS"],
        "role": "confirms the parent-signature contract checkpoint passed as nonclaim.",
    },
    {
        "source_id": "SRC1812_2_1811_alpha_owner",
        "source_key": "1811_alpha_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_ALPHA_OWNER_AUDIT.csv",
        "needles": ["AO1811_3_verdict", "ALPHA_OWNER_NOT_DERIVED"],
        "role": "latest alpha-owner blocker to be sharpened.",
    },
    {
        "source_id": "SRC1812_3_1811_matter_qdq",
        "source_key": "1811_matter_functor_qdq_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1811_MATTER_FUNCTOR_QDQ_AUDIT.csv",
        "needles": ["MFQ1811_4_verdict", "PACKAGE_UNSIGNED"],
        "role": "current q/Dq and matter-functor package remains unsigned.",
    },
    {
        "source_id": "SRC1812_4_1782_doc",
        "source_key": "1782_field_chart_qvis_doc",
        "source_path": ROOT / "1782-Y5-R2FR-parent-field-chart-Qvis-column-owner-or-Dq-first-component-row.md",
        "needles": ["FCO1782_6_verdict", "QCO1782_9_verdict"],
        "role": "field-chart and Q_vis owner audit that 1812 continues.",
    },
    {
        "source_id": "SRC1812_5_1782_validation",
        "source_key": "1782_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1782_VALIDATION.csv",
        "needles": ["VAL1782_OVERALL", "PASS"],
        "role": "confirms 1782 stayed nonclaim and hygiene-clean.",
    },
    {
        "source_id": "SRC1812_6_1782_field_chart",
        "source_key": "1782_field_chart_owner_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_FIELD_CHART_OWNER_GATE.csv",
        "needles": ["FCO1782_1_chart_version_consistency", "CHART_VERSION_MISMATCH_A_OWNED_UNSIGNED"],
        "role": "exact A_owned chart-placement mismatch and parent chart blocker.",
    },
    {
        "source_id": "SRC1812_7_1782_qvis",
        "source_key": "1782_qvis_column_owner_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_QVIS_COLUMN_OWNER_MATRIX.csv",
        "needles": ["QCO1782_4_A_owned", "QCO1782_9_verdict"],
        "role": "Q_vis column matrix with A_owned undecided and residual exclusions unsigned.",
    },
    {
        "source_id": "SRC1812_8_1782_dq_first_rows",
        "source_key": "1782_dq_first_component_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_DQ_FIRST_COMPONENT_ROW_SCHEMA.csv",
        "needles": ["DQF1782_5_total_DqZ_abs", "epsilon_DqZ_Qvis_abs"],
        "role": "prior Dq first-component fallback rows.",
    },
    {
        "source_id": "SRC1812_9_1667_field_chart",
        "source_key": "1667_parent_field_chart_candidate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
        "needles": ["PFC1667_7_chart_verdict", "not an adopted"],
        "role": "older parent field chart candidate and non-adoption verdict.",
    },
    {
        "source_id": "SRC1812_10_1667_q_audit",
        "source_key": "1667_quotient_map_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
        "needles": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
        "role": "q-map computability blocker.",
    },
    {
        "source_id": "SRC1812_11_1667_dq_tests",
        "source_key": "1667_dq_on_zphi_tests",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "needles": ["DQT1667_6_verdict", "Dq[Z/phi]=0"],
        "role": "Z/phi Dq-zero or constraint-first test status.",
    },
    {
        "source_id": "SRC1812_12_1056_doc",
        "source_key": "1056_alpha_owner_doc",
        "source_path": ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
        "needles": ["VNA1056_6_verdict", "ALPHA_OWNER_NOT_DERIVED"],
        "role": "alpha-owner route through vertical-generator norm/topological level.",
    },
    {
        "source_id": "SRC1812_13_1056_validation",
        "source_key": "1056_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1056_VALIDATION.csv",
        "needles": ["V1056_SUMMARY", "pass"],
        "role": "confirms 1056 refused alpha promotion.",
    },
    {
        "source_id": "SRC1812_14_1056_vertical_norm",
        "source_key": "1056_vertical_generator_norm",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "needles": ["VNA1056_6_verdict", "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA"],
        "role": "fixed generator norm route is conditional but not parent-signed.",
    },
    {
        "source_id": "SRC1812_15_1056_topological_level",
        "source_key": "1056_topological_level_route",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv",
        "needles": ["TL1056_4_verdict", "topological alpha owner"],
        "role": "topology fixes charge labels but not the 4D Maxwell kinetic coefficient by itself.",
    },
    {
        "source_id": "SRC1812_16_1056_promotion_gates",
        "source_key": "1056_promotion_gates",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_PROMOTION_GATES.csv",
        "needles": ["PG1056_4_alpha_zero", "requires all upstream alpha-owner gates"],
        "role": "alpha-zero promotion gate remains blocked.",
    },
    {
        "source_id": "SRC1812_17_1235_unique_f2",
        "source_key": "1235_unique_F2_typed_domain",
        "source_path": RESIDUALS / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
        "needles": ["UF21235_7_verdict", "UNIQUE_F2_NOT_CLOSED"],
        "role": "unique F_Q^2 theorem is exact conditional only.",
    },
    {
        "source_id": "SRC1812_18_1235_requirements",
        "source_key": "1235_typed_domain_requirements",
        "source_path": RESIDUALS / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
        "needles": ["TREQ1235_3_unique_curvature_norm", "UNIQUE_CURVATURE_NORM"],
        "role": "typed-domain and unique-curvature-norm requirements for alpha ownership.",
    },
    {
        "source_id": "SRC1812_19_1480_hom",
        "source_key": "1480_hom_exclusion_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1480_COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT.csv",
        "needles": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED"],
        "role": "coefficient-domain Hom exclusion is not parent-derived.",
    },
    {
        "source_id": "SRC1812_20_1480_hom_obstructions",
        "source_key": "1480_hom_obstruction_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv",
        "needles": ["HOB1480_0_scalar_I", "COUNTEREXAMPLE_PROVED"],
        "role": "scalar/source/readout Hom obstructions that keep residual rows live.",
    },
    {
        "source_id": "SRC1812_21_1414_beta_source_alpha",
        "source_key": "1414_beta_source_alpha_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
        "needles": ["BSA1414_5_verdict", "OWNER_NOT_DERIVED"],
        "role": "source-alpha current owner blocker.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_SOURCE_REGISTER.csv",
    "conditional_owner_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_CONDITIONAL_OWNER_THEOREM.csv",
    "field_chart_qvis_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_FIELD_CHART_QVIS_OWNER_AUDIT.csv",
    "alpha_level_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
    "dq_dobs_alpha_first_residual": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_DQ_DOBS_ALPHA_FIRST_RESIDUAL_ROW_SCHEMA.csv",
    "coefficient_domain_hom_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_COEFFICIENT_DOMAIN_HOM_GATE.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_GR_NEWTON_SOURCE_IMPACT.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_COUNTERMODEL_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1812_VALIDATION.csv",
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
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def conditional_owner_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "COT1812_0_target",
            "claim": "one parent owner package silences Q_vis and alpha-level leakage",
            "mathematical_statement": "If a parent action owns Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc), q projects only to canonical Q_vis columns, residual variables are removed by constraints/gauge or have Dq=0, and alpha_EM=alpha_*(ell_EM) with Lie_v ell_EM=0 and no Hom(C_hid,Coeff(F_Q^2)), then Dq[v] on Q_vis, DObs_e[Dq(v)], and D_v alpha_EM vanish for retained local vertical directions.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "ANTECEDENTS_NOT_JOINTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "COT1812_1_qvis_chain_rule",
            "claim": "Q_vis invisibility follows from owned quotient columns",
            "mathematical_statement": "For any retained direction v, DObs[Dq(v)]=0 follows by chain rule only after q, Q_vis, and Obs_e are parent-owned maps and v is in ker(Dq) for every ordinary-matter column.",
            "proof_status": "VALID_CHAIN_RULE_CONDITIONAL",
            "current_corpus_status": "FIELD_CHART_QVIS_NOT_PARENT_OWNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "COT1812_2_A_owned_choice",
            "claim": "A_owned placement must be unique before Dq/alpha rows can be theorem-zero",
            "mathematical_statement": "A_owned must be exactly one of parent field, quotient data, fixed representation/level data, or finite residual row; mixed placement reopens Dq_A and alpha-level marker leakage.",
            "proof_status": "NECESSARY_CONSISTENCY_CONDITION",
            "current_corpus_status": "A_OWNED_PLACEMENT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "COT1812_3_alpha_level",
            "claim": "alpha owner follows from fixed EM level only if F_Q^2 coefficient domain is exhausted",
            "mathematical_statement": "A compact charge generator or topological level fixes labels/periods, but measured alpha is fixed only if the Maxwell kinetic norm and current normalization descend from the same parent owner and no independent lambda_A F_Q^2 or f(I_hid)F_Q^2 term is legal.",
            "proof_status": "EXACT_CONDITIONAL_ROUTE",
            "current_corpus_status": "UNIQUE_F2_AND_HOM_EXCLUSION_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "COT1812_4_verdict",
            "claim": "1812 proves the owner package in the current corpus",
            "mathematical_statement": "COT1812_1 through COT1812_3 are all parent-signed in one action/domain package",
            "proof_status": "OWNER_PACKAGE_CONTRACT_NOT_CURRENT_PROOF",
            "current_corpus_status": "FAIL_CURRENT_CLAIM_BUILD_FIRST_RESIDUAL_ROWS",
            "valid_for_claim": False,
        },
    ]


def field_chart_qvis_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_0_parent_action_chart",
            "object": "Phi_parent chart",
            "candidate": "Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc)",
            "current_status": "CANDIDATE_ONLY_NOT_ACTION_SIGNED",
            "source_anchor": "FCO1782_0_parent_action_chart; PFC1667_7_chart_verdict",
            "missing_for_claim": "parent action or theorem-equivalent construction names chart blocks, gauge redundancies and exclusions before readout",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_1_A_owned_placement",
            "object": "A_owned",
            "candidate": "owned gauge/charge representation data",
            "current_status": "BLOCKING_MISMATCH",
            "source_anchor": "FCO1782_1_chart_version_consistency; QCO1782_4_A_owned",
            "missing_for_claim": "single canonical placement: parent field, quotient column, fixed level/representation data, or residual row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_2_Qvis_columns",
            "object": "Q_vis",
            "candidate": "e_obs,g_obs,measure/connection,source/readout,theta_A,A_owned/tau roles",
            "current_status": "USEFUL_MATRIX_NOT_CANONICAL_OWNER",
            "source_anchor": "QCO1782_0_e_obs_g_obs through QCO1782_9_verdict",
            "missing_for_claim": "canonical parent quotient map with owned included columns and theorem-level excluded columns",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_3_residual_exclusion",
            "object": "Z,phi,R_AB,J_q,R_phys",
            "candidate": "exclude residual variables from ordinary quotient data",
            "current_status": "CONSTRAINT_OR_DQ_ZERO_NOT_DERIVED",
            "source_anchor": "FCO1782_3_residual_exclusion_grammar; DQT1667_6_verdict",
            "missing_for_claim": "constraint/no-pole/gauge proof or Dq-zero cells with norms and no-cancellation envelope",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_4_boundary_tau_support",
            "object": "B_edge,P_loc,Q_X,tau roles",
            "candidate": "q-basic boundary/projector/source support and role-locked tau",
            "current_status": "BOUNDARY_TAU_QBASIC_UNSIGNED",
            "source_anchor": "FCO1782_4_boundary_support; FCO1782_5_tau_source_normal_lock",
            "missing_for_claim": "boundary/projector descent plus tau pushforward/role-lock certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FCQ1812_5_verdict",
            "object": "field-chart plus Q_vis owner",
            "candidate": "owned ordinary-matter quotient package",
            "current_status": "FIELD_CHART_QVIS_NOT_PARENT_OWNED",
            "source_anchor": "FCO1782_6_verdict; QCO1782_9_verdict",
            "missing_for_claim": "FCQ1812_0 through FCQ1812_4 closed in one parent branch",
            "valid_for_claim": False,
        },
    ]


def alpha_level_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_0_fixed_level_target",
            "candidate_owner": "fixed representation/topological/fibre metric level ell_EM or g_*",
            "would_imply": "Lie_v alpha_EM=0 before WEP/R10/clock/source tests see alpha-marker leakage",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "source_anchor": "AO1811_0_fixed_level; TL1056_4_verdict",
            "missing_for_claim": "explicit alpha_EM=alpha_*(ell_EM,g_*) map and Lie_v ell_EM=0 from MTS primitives",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_1_vertical_generator_norm",
            "candidate_owner": "compact T_Q with fixed parent norm",
            "would_imply": "connection period, charge labels, kinetic coefficient, and current normalization share one parent owner",
            "current_status": "NORM_ROUTE_CONDITIONAL_NOT_SIGNED",
            "source_anchor": "VNA1056_0_parent_charge_generator through VNA1056_6_verdict",
            "missing_for_claim": "parent fibre metric/lattice/symplectic norm plus same current owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_2_unique_F2",
            "candidate_owner": "unique parent Maxwell curvature norm",
            "would_imply": "no independent lambda_A F_Q^2 shifts alpha_EM away from the parent level",
            "current_status": "UNIQUE_F2_NOT_CLOSED",
            "source_anchor": "UF21235_7_verdict; TREQ1235_3_unique_curvature_norm",
            "missing_for_claim": "typed coefficient-domain certificate or one-parent-curvature-norm theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_3_Hom_exclusion",
            "candidate_owner": "no Hom(C_hid,Coeff(F_Q^2)) and no source/current rescaling",
            "would_imply": "hidden/local scalars and source labels cannot become alpha or current-normalization coefficients",
            "current_status": "HOM_EXCLUSION_NOT_PARENT_DERIVED",
            "source_anchor": "CDH1480_5_verdict; HOB1480_0_scalar_I; BSA1414_5_verdict",
            "missing_for_claim": "hidden invariant triviality, coefficient target exclusion, current owner and radiative/readout closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_4_readout_radiative",
            "candidate_owner": "observed alpha readout remains quotient-fixed under clocks/spectroscopy/EFT",
            "would_imply": "fixed abstract EM norm becomes fixed measured alpha and does not reappear through hbar*c or Hodge/readout maps",
            "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "source_anchor": "PG1056_3_readout; RSC1056_3_readout_leak",
            "missing_for_claim": "renormalized visible-sector/readout closure theorem or finite alpha-marker residual row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "alpha_id": "ALO1812_5_verdict",
            "candidate_owner": "alpha_EM parent level owner",
            "would_imply": "b_alpha=0 and alpha source/test marker leakage removed structurally",
            "current_status": "ALPHA_LEVEL_OWNER_NOT_DERIVED",
            "source_anchor": "AO1811_3_verdict; VNA1056_6_verdict; PG1056_4_alpha_zero",
            "missing_for_claim": "ALO1812_0 through ALO1812_4 closed together",
            "valid_for_claim": False,
        },
    ]


def residual_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_0_DqZ_Qvis",
            "quantity": "epsilon_DqZ_Qvis_abs",
            "component": "Dq[v_Z] over all Q_vis columns",
            "formal_expression": "sum_i ||Dq_i[v_Z]|| over e_obs,g_obs,mu_m,D_m,source/readout,theta_A,A_owned,tau columns",
            "zero_condition": "Q_vis is parent-owned and Z is constrained/gauge/Dq-zero for every ordinary column",
            "required_inputs": "direction_id; q_column; Dq_value_or_zero_theorem; norm; units; source_path; no_cancellation_flag",
            "current_status": "MISSING_DQ_VALUE_OR_THEOREM_ZERO",
            "units": "dimensionless_norm_or_column_units",
            "source_path": "",
            "common_normalizer": "MISSING_COMMON_QVIS_NORM",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_1_DObs_e",
            "quantity": "epsilon_DObs_e_abs",
            "component": "DObs_e[Dq(v)] plus common-frame derivative b_g,X",
            "formal_expression": "||DObs_e|_q[Dq(v)]||+|b_g,X|",
            "zero_condition": "Obs_e factors through q and no common-frame residual exists",
            "required_inputs": "direction_id; DObs_e_value_or_zero_theorem; b_g_component; coframe_norm; units; source_path",
            "current_status": "MISSING_OBS_E_FACTORISATION_OR_FINITE_VALUE",
            "units": "dimensionless_metric_or_coframe_norm",
            "source_path": "",
            "common_normalizer": "MISSING_COF_FRAME_NORM",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_2_Dtheta_marker",
            "quantity": "epsilon_theta_marker_abs",
            "component": "Lie_v theta_A and material/clock/charge marker drift",
            "formal_expression": "sum_A |Lie_v theta_A|+|D_v marker_A|",
            "zero_condition": "ordinary constants/material labels are quotient-owned or superselected",
            "required_inputs": "marker_id; Lie_v_marker_or_zero_theorem; units; source_path; material/readout context",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_MARKER_VALUE",
            "units": "dimensionless_fractional_marker_norm",
            "source_path": "",
            "common_normalizer": "MISSING_MARKER_NORM",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_3_A_owned_alpha_level",
            "quantity": "epsilon_A_level_abs",
            "component": "D_v A_owned, D_v ell_EM, D_v g_*",
            "formal_expression": "||D_v A_owned||+|D_v ell_EM|+|D_v g_*|",
            "zero_condition": "A_owned placement is unique and EM level/fibre metric is parent-fixed",
            "required_inputs": "A_owned_role; level_owner; derivative_or_zero_theorem; units; source_path",
            "current_status": "MISSING_A_OWNED_PLACEMENT_AND_ALPHA_LEVEL_OWNER",
            "units": "representation_level_or_fractional_coupling_norm",
            "source_path": "",
            "common_normalizer": "MISSING_LEVEL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_4_alpha_counterterm",
            "quantity": "epsilon_alpha_counterterm_abs",
            "component": "lambda_A F_Q^2 or f(I_hid)F_Q^2 leakage",
            "formal_expression": "|lambda_A|+sup|D_hid f| over local branch",
            "zero_condition": "unique F_Q^2 typed coefficient domain and Hom(C_hid,Coeff(F_Q^2)) exclusion",
            "required_inputs": "coefficient_domain_certificate_or_bound; hidden scalar status; units; source_path",
            "current_status": "MISSING_UNIQUE_F2_OR_COEFFICIENT_BOUND",
            "units": "fractional_alpha_response",
            "source_path": "",
            "common_normalizer": "MISSING_ALPHA_RESPONSE_NORM",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DQA1812_5_total",
            "quantity": "epsilon_qvis_alpha_total_abs",
            "component": "total field-chart/Qvis/alpha owner residual envelope",
            "formal_expression": "abs(DQA1812_0)+abs(DQA1812_1)+abs(DQA1812_2)+abs(DQA1812_3)+abs(DQA1812_4)",
            "zero_condition": "all owner clauses theorem-zero, or all finite rows source-backed with no-cancellation guard",
            "required_inputs": "all DQA1812 component values; common normalizer; arena projection; source paths",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def coefficient_domain_hom_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CDG1812_0_typed_domain",
            "claim_piece": "visible Maxwell coefficient domain excludes hidden arguments",
            "mathematical_form": "Arg(Coeff(F_Q^2))=Q_vis x Rep_Q x Top_Q with no C_hid object",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "obstruction": "parent object-language/action-domain certificate missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CDG1812_1_unique_curvature_norm",
            "claim_piece": "one parent curvature norm fixes g_EM^{-2}",
            "mathematical_form": "S_parent contains one -C_P/4 <F,F>_P subblock and no independent visible counterterm",
            "current_status": "UNIQUE_CURVATURE_NORM_NOT_DERIVED",
            "obstruction": "lambda_A F_Q^2 remains legal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CDG1812_2_hidden_scalar_Hom",
            "claim_piece": "Hom(C_hid,Coeff(F_Q^2)) absent or constant",
            "mathematical_form": "I_hid -> c0+epsilon I_hid is forbidden or O(C_hid)^inv=R",
            "current_status": "SCALAR_COUNTEREXAMPLE_RETAINED",
            "obstruction": "hidden invariant triviality not proved",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CDG1812_3_current_rescaling",
            "claim_piece": "same Noether owner fixes kinetic and current normalization",
            "mathematical_form": "delta S_m/delta A_Q=J_Q with charges as fixed T_Q representation weights",
            "current_status": "CURRENT_OWNER_UNSIGNED",
            "obstruction": "J_A -> c_A J_A/source-normalization counterexample survives",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CDG1812_4_verdict",
            "claim_piece": "coefficient-domain/Hom gate closes alpha-level owner",
            "mathematical_form": "CDG1812_0 through CDG1812_3 all close in one branch",
            "current_status": "COEFFICIENT_DOMAIN_HOM_GATE_BLOCKED",
            "obstruction": "keep alpha counterterm residual rows live",
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1812_0_chart_qvis",
            "if_closed": "field chart and Q_vis columns are parent-owned",
            "would_buy": "Dq/DObs_e residual vector becomes computable instead of prose; visible ordinary matter columns are defined before fitting",
            "still_missing": "vertical basis, numeric/theorem-zero Dq cells, Obs_e factorisation and boundary/tau support",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1812_1_alpha_level",
            "if_closed": "alpha_EM is fixed level/fibre-metric data with no independent F_Q^2 coefficient",
            "would_buy": "b_alpha and alpha source/test marker branches are structurally removed rather than bounded arena by arena",
            "still_missing": "unique F2, Hom exclusion, current owner and readout/radiative closure",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1812_2_Newton_GR_source",
            "if_closed": "chart/Qvis/alpha package plus 1811 matter functor signature closes",
            "would_buy": "source side of GR/Newton reduction loses the sharpest arbitrary-coupling route",
            "still_missing": "EH/Einstein left-hand limit, measured-G guard, PPN response matrix and finite tails",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1812_3_R10_WEP_clock",
            "if_closed": "alpha-level marker leakage is theorem-zero",
            "would_buy": "R10/WEP/clock alpha-marker branches can be demoted before data comparison",
            "still_missing": "non-alpha finite channels and source-backed arena projections",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1812_4_verdict",
            "if_closed": "1812 owner package closes",
            "would_buy": "major local-source bridge toward MTS -> GR/Newton, not the full reduction",
            "still_missing": "owner package not closed, so local-GR/PPN/WEP/R10 claims remain refused",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1812_0_chart_relabel",
            "countermodel": "rename a useful test chart as parent action data without action ownership",
            "why_it_defeats_claim": "Dq and Q_vis zeros become coordinate convention, not theorem",
            "blocked_by": "parent action chart or theorem-equivalent quotient construction",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1812_1_A_owned_double_role",
            "countermodel": "A_owned is both quotient column and hidden parent/gauge residual",
            "why_it_defeats_claim": "alpha/current normalization can leak through the placement ambiguity",
            "blocked_by": "single A_owned placement rule and residual row for any leftover derivative",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1812_2_scalar_gauge_kinetic",
            "countermodel": "f(I_hid)F_Q^2 or lambda_A F_Q^2",
            "why_it_defeats_claim": "standard covariance and U(1) gauge invariance allow this unless coefficient domain forbids it",
            "blocked_by": "unique F2 typed-domain/curvature-norm theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1812_3_current_rescale",
            "countermodel": "J_A -> c_A J_A with compensating charge/source convention",
            "why_it_defeats_claim": "fixed Maxwell coefficient does not by itself fix source/test charge response",
            "blocked_by": "same Noether/current owner for kinetic, interaction, charge labels and WEP/R10 readout",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1812_4_readout_reentry",
            "countermodel": "clock/spectroscopy/EFT readout regenerates alpha or marker dependence",
            "why_it_defeats_claim": "fixed abstract level can still produce varying measured alpha if readout carries vertical data",
            "blocked_by": "radiative/readout closure or finite alpha-marker residual row",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1812_0_conditional_package",
            "gate": "conditional owner package theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "COT1812 gives an exact sufficient theorem if chart/Qvis/alpha/Hom antecedents are signed",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1812_1_field_chart_qvis",
            "gate": "field chart and Q_vis owner close",
            "current_status": "BLOCKED",
            "reason": "FCQ1812_5 remains FIELD_CHART_QVIS_NOT_PARENT_OWNED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1812_2_alpha_level",
            "gate": "alpha level/fibre metric owner closes",
            "current_status": "BLOCKED",
            "reason": "ALO1812_5 remains ALPHA_LEVEL_OWNER_NOT_DERIVED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1812_3_residual_rows",
            "gate": "first residual rows are source-backed and score-ready",
            "current_status": "BLOCKED",
            "reason": "DQA1812 rows are schema-ready but have MISSING values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1812_4_local_promotion",
            "gate": "local GR/WEP/R10/PPN promotion is allowed",
            "current_status": "REFUSED",
            "reason": "owner theorem and finite residual fallback are both incomplete",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1812_0_owner_package",
            "claim": "field-chart/Qvis/alpha-level owner package is proved",
            "status": "BLOCKED",
            "reason": "COT1812 is exact conditional, but FCQ1812_5 and ALO1812_5 fail current proof",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1812_1_Dq_DObs_zero",
            "claim": "Dq and DObs_e leakage vanish",
            "status": "BLOCKED",
            "reason": "Q_vis owner, residual exclusion and Obs_e factorisation remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1812_2_alpha_zero",
            "claim": "b_alpha and alpha-marker source/test leakage vanish",
            "status": "BLOCKED",
            "reason": "alpha level owner, unique F2, Hom exclusion and readout/radiative closure remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1812_3_WEP_R10_clock",
            "claim": "WEP/R10/clock alpha branches pass",
            "status": "BLOCKED",
            "reason": "alpha marker is not theorem-zero and no source-backed finite arena projection is present",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1812_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "source-side owner package is not closed and EH/PPN/Poisson/measured-G gates remain outside 1812",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1812_0_theorem_result",
            "decision": "OWNER_PACKAGE_EXACT_CONDITIONAL",
            "reason": "a clean theorem exists if one parent action owns Q_vis/A_owned/alpha level and forbids hidden-visible F2/current coefficient maps",
            "next_action": "keep the theorem as contract-only unless all antecedents are signed",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1812_1_current_status",
            "decision": "OWNER_PACKAGE_NOT_SIGNED",
            "reason": "parent chart/Qvis ownership and alpha-level owner remain separately unsigned and not yet fused into one parent action",
            "next_action": "do not promote Dq, alpha, WEP, R10, PPN or local-GR claims",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1812_2_residual_status",
            "decision": "FIRST_RESIDUAL_SCHEMA_READY_NONCLAIM",
            "reason": "failed owner clauses now have explicit Dq/DObs/theta/A-owned/alpha-counterterm rows, but values and normalizers are missing",
            "next_action": "fill no row without a source path, units, common normalizer and no-cancellation flag",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1812_3_best_next",
            "decision": "A_OWNED_PLACEMENT_AND_EM_LEVEL_OWNER_NEXT",
            "reason": "A_owned placement is the common blocker between Q_vis ownership and alpha-level ownership; resolving it is less diffuse than attacking all Dq cells at once",
            "next_action": "1813-Y5-R2FR-A-owned-placement-and-EM-level-owner-or-alpha-marker-residual-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1812_0_primary",
            "next_target": "1813-Y5-R2FR-A-owned-placement-and-EM-level-owner-or-alpha-marker-residual-row.md",
            "script": "scripts/Y5_R2FR_A_owned_placement_and_EM_level_owner_or_alpha_marker_residual_row.py",
            "objective": "choose or reject the unique A_owned placement and EM level/fibre-metric owner; if it cannot close, source the first alpha-marker/A-owned residual row with units and no-cancellation guard",
            "selection_status": "selected",
            "success_condition": "single A_owned/ell_EM owner theorem-zero, or D_v A_owned/D_v ell_EM residual row is source-backed and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1812_1_parallel",
            "next_target": "1813b-Y5-R2FR-Qvis-Dq-column-values-or-constraint-first-exclusion.md",
            "script": "scripts/Y5_R2FR_Qvis_Dq_column_values_or_constraint_first_exclusion.py",
            "objective": "begin finite Q_vis Dq rows only after A_owned placement is decided or explicitly residualized",
            "selection_status": "held_parallel",
            "success_condition": "at least one Dq column has theorem-zero or source-backed finite value with common normalizer",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "conditional_owner_theorem": conditional_owner_theorem_rows(),
        "field_chart_qvis_owner_audit": field_chart_qvis_rows(),
        "alpha_level_owner_audit": alpha_level_owner_rows(),
        "dq_dobs_alpha_first_residual": residual_schema_rows(),
        "coefficient_domain_hom_gate": coefficient_domain_hom_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
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
    allowed_gate_pass = {"AC1812_0_conditional_package"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if field == "gate_pass" and row.get("gate_id") in allowed_gate_pass:
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1812_0_conditional_package")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1812_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1812_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1812_2_conditional_theorem_written",
            any(row["theorem_id"] == "COT1812_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["conditional_owner_theorem"]),
            "field-chart/Qvis/alpha owner theorem is written as an exact conditional",
        ),
        (
            "VAL1812_3_theorem_not_promoted",
            any(row["theorem_id"] == "COT1812_4_verdict" and row["proof_status"] == "OWNER_PACKAGE_CONTRACT_NOT_CURRENT_PROOF" for row in rows_map["conditional_owner_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["conditional_owner_theorem"]),
            "conditional theorem is not promoted as a current proof",
        ),
        (
            "VAL1812_4_field_chart_qvis_blocked",
            any(row["audit_id"] == "FCQ1812_5_verdict" and row["current_status"] == "FIELD_CHART_QVIS_NOT_PARENT_OWNED" for row in rows_map["field_chart_qvis_owner_audit"]),
            "field chart and Q_vis owner remain blocked",
        ),
        (
            "VAL1812_5_alpha_level_not_derived",
            any(row["alpha_id"] == "ALO1812_5_verdict" and row["current_status"] == "ALPHA_LEVEL_OWNER_NOT_DERIVED" for row in rows_map["alpha_level_owner_audit"]),
            "alpha level owner remains not derived",
        ),
        (
            "VAL1812_6_coefficient_hom_gate_blocked",
            any(row["gate_id"] == "CDG1812_4_verdict" and row["current_status"] == "COEFFICIENT_DOMAIN_HOM_GATE_BLOCKED" for row in rows_map["coefficient_domain_hom_gate"]),
            "unique-F2/Hom gate remains blocked",
        ),
        (
            "VAL1812_7_residual_schema_nonclaim",
            any(row["residual_id"] == "DQA1812_5_total" for row in rows_map["dq_dobs_alpha_first_residual"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["dq_dobs_alpha_first_residual"]),
            "first residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1812_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1812_9_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1812_10_acceptance_blocks",
            any(row["gate_id"] == "AC1812_0_conditional_package" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1812_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all owner/local claim gates remain blocked or refused",
        ),
        ("VAL1812_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1812_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1812_14_decision_next",
            any(row["decision_id"] == "DEC1812_3_best_next" and row["decision"] == "A_OWNED_PLACEMENT_AND_EM_LEVEL_OWNER_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects A_owned placement and EM level owner next",
        ),
        (
            "VAL1812_15_next_selected",
            any(row["route_id"] == "NEXT1812_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1812_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1812 CSVs parse"),
        ("VAL1812_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1812_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1812_19_formalization_untouched", formalization_untouched(), "no 1812 outputs found under formalization-workbench"),
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
            "check_id": "VAL1812_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1812 parent field-chart Qvis alpha-level owner or first residual row checkpoint",
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
            "# 1812 Y5 R2FR parent field-chart Qvis and alpha-level owner or first residual row",
            "",
            "**Progress:** 1812 pins the next domino down: the local source-side bridge cannot be promoted until the same parent action owns the field chart, the `Q_vis` columns, the `A_owned` placement, and the EM level/fibre metric that fixes measured `alpha_EM`.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. The clean route is real: if `Q_vis` and `alpha_EM` are owned by one parent package and hidden-visible `F_Q^2` coefficient maps are illegal, the dangerous `Dq/DObs_e/alpha` leakage vanishes by chain rule and coefficient-domain typing. The corpus does not yet sign those antecedents.",
            "",
            "**Claim ceiling:** no parent chart claim, no canonical `Q_vis` owner claim, no `A_owned` placement claim, no `b_alpha=0`, no `Dq/DObs_e=0`, no WEP/R10/clock/PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1812.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Conditional Owner Theorem",
            markdown_table(rows_map["conditional_owner_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Field Chart Qvis Owner Audit",
            markdown_table(rows_map["field_chart_qvis_owner_audit"], ["audit_id", "object", "candidate", "current_status", "source_anchor", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Alpha Level Owner Audit",
            markdown_table(rows_map["alpha_level_owner_audit"], ["alpha_id", "candidate_owner", "would_imply", "current_status", "source_anchor", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Dq DObs Alpha First Residual Row Schema",
            markdown_table(rows_map["dq_dobs_alpha_first_residual"], ["residual_id", "quantity", "component", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
            "",
            "## Coefficient Domain Hom Gate",
            markdown_table(rows_map["coefficient_domain_hom_gate"], ["gate_id", "claim_piece", "mathematical_form", "current_status", "obstruction", "valid_for_claim"]),
            "",
            "## GR Newton Source Impact",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
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
            "The best next attack is not 'more data' yet. It is the coupling owner: decide whether `A_owned` is a parent field, quotient data, fixed representation/level data, or a finite residual row. That choice is the hinge between the `Q_vis` branch and the alpha branch. If it closes, we get a structural zero route; if it fails, we get a clean alpha-marker residual instead of a vague loophole.",
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
    print(f"1812 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
