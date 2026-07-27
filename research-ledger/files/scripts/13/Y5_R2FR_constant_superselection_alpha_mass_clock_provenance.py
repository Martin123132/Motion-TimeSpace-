from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1804"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1804_0_1803_doc",
        "source_key": "1803_doc",
        "source_path": ROOT / "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md",
        "needles": ["NEXT1803_0_primary", "QCP1803_2_b_alpha"],
        "role": "1803 handoff selecting constant superselection as the next target.",
    },
    {
        "source_id": "SRC1804_1_1803_validation",
        "source_key": "1803_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1803_VALIDATION.csv",
        "needles": ["VAL1803_OVERALL", "PASS"],
        "role": "confirms the prior hidden-coupling checkpoint passed.",
    },
    {
        "source_id": "SRC1804_2_1803_qbar_coefficients",
        "source_key": "1803_qbar_coefficients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_QBAR_COEFFICIENT_PACK.csv",
        "needles": ["QCP1803_2_b_alpha", "QCP1803_8_total_abs_guard"],
        "role": "current branch qbar constant coefficient debt.",
    },
    {
        "source_id": "SRC1804_3_1047_doc",
        "source_key": "1047_doc",
        "source_path": ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
        "needles": ["CST1047_5_verdict", "DEC1047_3_best_next"],
        "role": "older constant-superselection theorem attempt and no-extra-F2 handoff.",
    },
    {
        "source_id": "SRC1804_4_1047_theorem",
        "source_key": "1047_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
        "needles": ["CST1047_0_descent_or_superselection_criterion", "CST1047_5_verdict"],
        "role": "conditional theorem shape for quotient-descended or superselected constants.",
    },
    {
        "source_id": "SRC1804_5_1047_alpha",
        "source_key": "1047_alpha_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv",
        "needles": ["AGN1047_2_kinetic_normalization", "AGN1047_4_verdict"],
        "role": "prior alpha gauge normalization audit.",
    },
    {
        "source_id": "SRC1804_6_1047_mass",
        "source_key": "1047_mass_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1047_MASS_RATIO_SUPERSELECTION_AUDIT.csv",
        "needles": ["MRS1047_1_electron_proton_ratio", "MRS1047_4_verdict"],
        "role": "prior mass-ratio superselection audit.",
    },
    {
        "source_id": "SRC1804_7_1047_clock_rows",
        "source_key": "1047_clock_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_1047_CLOCK_CONSTANT_PROJECTION_ROWS.csv",
        "needles": ["CLK1047_0_CAS646_0_AlHg", "CLK1047_1_CAS646_1_YbE3E2"],
        "role": "prior nonclaim clock projection rows.",
    },
    {
        "source_id": "SRC1804_8_1047_coefficients",
        "source_key": "1047_coefficients",
        "source_path": RESIDUALS / "P8_Y5_R10_1047_COEFFICIENT_PROVENANCE_ROWS.csv",
        "needles": ["CP1047_0_b_alpha", "CP1047_4_qbar_constants_abs"],
        "role": "prior constant-sector coefficient provenance rows.",
    },
    {
        "source_id": "SRC1804_9_638_constant_zero",
        "source_key": "638_constant_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv",
        "needles": ["ZR638_1_alpha_EM", "ZR638_3_clock_transitions"],
        "role": "older alpha, mass and clock zero-route failure audit.",
    },
    {
        "source_id": "SRC1804_10_646_clock_sensitivity",
        "source_key": "646_clock_sensitivity",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed alpha sensitivity values for clock comparison rows.",
    },
    {
        "source_id": "SRC1804_11_646_clock_projection",
        "source_key": "646_clock_projection",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv",
        "needles": ["CPL646_0_pair_ratio", "CPL646_2_gravitational_potential_coupling"],
        "role": "clock projection laws and missing MTS local map.",
    },
    {
        "source_id": "SRC1804_12_988_em_lock",
        "source_key": "988_em_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
        "needles": ["EMLOCK988_1_unique_Maxwell_F2", "EMLOCK988_4_no_alpha_vertex"],
        "role": "EM lock gate showing no-alpha theorem is not signed.",
    },
    {
        "source_id": "SRC1804_13_989_em_signature",
        "source_key": "989_em_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
        "needles": ["ELA989_1_unique_F2", "ELA989_4_no_alpha_vertex"],
        "role": "parent EM signature audit and legal F2 counterexample.",
    },
    {
        "source_id": "SRC1804_14_990_parent_contract",
        "source_key": "990_parent_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC990_2_matter_functor", "PAC990_3_EM_lock"],
        "role": "minimal parent-action contract for matter and EM coupling.",
    },
    {
        "source_id": "SRC1804_15_1399_alpha_prior",
        "source_key": "1399_alpha_prior",
        "source_path": RESIDUALS / "P8_Y5_R10_1399_FINITE_ALPHAEM_PRIOR_VECTOR.csv",
        "needles": ["FAP1399_0_alphaEM_residual", "NONCLAIM_INPUT_MISSING"],
        "role": "finite alpha prior vector showing alpha rows remain nonclaim without derivative map.",
    },
    {
        "source_id": "SRC1804_16_1330_nist_mass",
        "source_key": "1330_nist_mass",
        "source_path": RESIDUALS / "P8_Y5_R10_1330_NIST_ELECTRON_MASS_EXTRACTION.csv",
        "needles": ["CONST1330_0_m_e_u", "AUDIT_EXTRACTED_NONCLAIM"],
        "role": "example real dimensionless mass-ratio constant extraction, still nonclaim for MTS.",
    },
    {
        "source_id": "SRC1804_17_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R2_clock_redshift"],
        "role": "local WEP and clock-redshift anchors for later bound projection.",
    },
    {
        "source_id": "SRC1804_18_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate bound rows, not claim grade.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_SOURCE_REGISTER.csv",
    "constant_superselection_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_CONSTANT_SUPERSELECTION_GATE.csv",
    "alpha_gauge_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_ALPHA_GAUGE_AUDIT.csv",
    "mass_ratio_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_MASS_RATIO_AUDIT.csv",
    "clock_projection_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_CLOCK_PROJECTION_ROWS.csv",
    "coefficient_provenance_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_COEFFICIENT_PROVENANCE_ROWS.csv",
    "bound_links": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_BOUND_LINKS.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1804_VALIDATION.csv",
}

DOC_PATH = ROOT / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": source["role"],
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(str(by_key[key]) for key in keys)


def clock_source_rows() -> list[dict[str, str]]:
    path = next(source["source_path"] for source in SOURCES if source["source_key"] == "646_clock_sensitivity")
    rows = read_csv(path)
    return [row for row in rows if row["clock_pair_id"] in {"CAS646_0_AlHg", "CAS646_1_YbE3E2"}]


def constant_superselection_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_0_exact_criterion",
            "claim_piece": "constant vertical silence criterion",
            "mathematical_statement": "theta(Phi)=theta_bar(q(Phi)) or theta is discrete/topological superselection, with Dq[v_X]=0, implies Lie_v theta=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "MISSING_PARENT_CLASSIFICATION_FOR_ALPHA_MASS_CLOCK_CONSTANTS",
            "if_missing": "retain b_alpha;b_mu;b_mA;b_nuc;b_clock_i",
            "source_paths": src("1047_theorem", "638_constant_zero"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_1_no_unit_rescaling_cheat",
            "claim_piece": "dimensionless observable guard",
            "mathematical_statement": "Lie_v ln(alpha_EM), Lie_v ln(m_A/m_B), and Lie_v ln(nu_i/nu_j) are invariant claims about ratios, not removable unit conventions",
            "current_status": "GUARD_PASSED_RETAINS_CONSTANT_CHANNELS",
            "missing_for_claim": "none_as_guard",
            "if_missing": "would falsely hide EM, WEP, and clock channels",
            "source_paths": src("1047_theorem", "638_constant_zero", "1330_nist_mass"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_2_alpha_EM",
            "claim_piece": "alpha_EM vertical silence",
            "mathematical_statement": "b_alpha := Lie_v ln(alpha_EM)=0 only if charge generator, Maxwell kinetic normalization, current owner, and readout all descend from the parent quotient",
            "current_status": "FAIL_CURRENT_CLAIM_UNIQUE_F2_AND_READOUT_UNSIGNED",
            "missing_for_claim": "MISSING_TQ_OWNER;MISSING_UNIQUE_F2;MISSING_NO_ALPHA_VERTEX;MISSING_READOUT_DESCENT",
            "if_missing": "retain b_alpha as physical local coefficient",
            "source_paths": src("1047_alpha_audit", "988_em_lock", "989_em_signature", "990_parent_contract"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_3_mass_ratios",
            "claim_piece": "mass ratio and binding vertical silence",
            "mathematical_statement": "b_mA := Lie_v ln(m_A/m_ref) and b_mu vanish only if matter spectrum, Yukawa/Higgs/QCD/binding data and no-mass vertices are parent-owned",
            "current_status": "FAIL_CURRENT_CLAIM_MATTER_SPECTRUM_NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_MATTER_SPECTRUM_OWNER;MISSING_BINDING_DECOMPOSITION;MISSING_NO_MASS_VERTEX",
            "if_missing": "retain b_mu;b_mA;b_nuc and composition sensitivity rows",
            "source_paths": src("1047_mass_audit", "638_constant_zero", "990_parent_contract", "1330_nist_mass"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_4_clock_constants",
            "claim_piece": "clock transition vertical silence",
            "mathematical_statement": "b_clock_i = K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...; zero follows only after all upstream constants and the clock readout map are closed",
            "current_status": "FAIL_CURRENT_CLAIM_INHERITS_ALPHA_MASS_NUCLEAR_DEBT",
            "missing_for_claim": "MISSING_B_ALPHA_ZERO_OR_VALUE;MISSING_B_MU_B_NUC;MISSING_TAU_CLOCK;MISSING_LOCAL_DXHAT_MAP",
            "if_missing": "retain b_clock_i and source-backed sensitivity rows",
            "source_paths": src("1047_clock_rows", "646_clock_sensitivity", "646_clock_projection", "local_bounds"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CSG1804_5_verdict",
            "claim_piece": "constant superselection promoted for local branch",
            "mathematical_statement": "qbar_constants_abs=0 only if CSG1804_0 plus alpha, mass, nuclear, and clock ownership clauses are parent-signed",
            "current_status": "CONSTANT_SUPERSELECTION_NOT_PROVED_COEFFICIENT_PROVENANCE_REQUIRED",
            "missing_for_claim": "MISSING_PARENT_NO_EXTRA_F2_NO_MASS_VERTEX_SIGNATURE",
            "if_missing": "build no-extra-F2/no-mass-vertex signature or alpha/mass/clock bound matrix",
            "source_paths": src("1803_qbar_coefficients", "1047_coefficients", "990_parent_contract"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def alpha_gauge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AGA1804_0_charge_generator",
            "object": "T_Q charge generator and charge lattice",
            "required_parent_signature": "T_Q is a compact parent-action generator with fixed lattice and norm data",
            "current_evidence": "the shape exists in earlier audits, but T_Q is not supplied as a varied parent-action object",
            "verdict": "UNSIGNED_RETAIN_B_ALPHA",
            "fallback_coefficient": "b_alpha;beta_source_alpha",
            "source_paths": src("988_em_lock", "989_em_signature"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AGA1804_1_unique_F2",
            "object": "Maxwell kinetic normalization",
            "required_parent_signature": "observed F_Q^2 is inherited uniquely from the parent curvature norm with no independent f_X F_Q^2 or lambda_A F_Q^2 counterterm",
            "current_evidence": "legal F2 counterexample remains active in the current corpus",
            "verdict": "FAILS_CURRENT_CORPUS_RETAIN_B_ALPHA",
            "fallback_coefficient": "b_alpha",
            "source_paths": src("988_em_lock", "989_em_signature", "990_parent_contract"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AGA1804_2_current_owner",
            "object": "matter current and source normalization",
            "required_parent_signature": "matter current, charge labels, Maxwell source normalization and EM readout descend from the same owner",
            "current_evidence": "current rescaling and beta_source_alpha remain unowned",
            "verdict": "UNSIGNED_RETAIN_SOURCE_ALPHA_ROW",
            "fallback_coefficient": "beta_source_alpha;b_alpha",
            "source_paths": src("988_em_lock", "989_em_signature", "1399_alpha_prior"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AGA1804_3_readout_descent",
            "object": "dimensionless alpha readout",
            "required_parent_signature": "Hodge star, coframe, hbar*c and spectral readout descend through q without a shadow clock frame",
            "current_evidence": "readout descent remains unsigned and clock rows still need tau_clock/local dXhat",
            "verdict": "UNSIGNED_RETAIN_B_CLOCK_I",
            "fallback_coefficient": "b_clock_i",
            "source_paths": src("646_clock_projection", "1047_alpha_audit", "1047_clock_rows"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AGA1804_4_verdict",
            "object": "alpha theorem-zero",
            "required_parent_signature": "AGA1804_0 through AGA1804_3 signed and no alpha_EM(Xhat) or f_X F^2 vertex survives",
            "current_evidence": "unique-F2, current owner, readout descent and no-alpha vertex are not signed",
            "verdict": "BLOCKED_RETAIN_B_ALPHA",
            "fallback_coefficient": "b_alpha",
            "source_paths": src("1047_alpha_audit", "988_em_lock", "989_em_signature", "990_parent_contract"),
            "valid_for_claim": False,
        },
    ]


def mass_ratio_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MRA1804_0_unit_guard",
            "object": "dimensionful mass scale",
            "zero_route": "one common mass scale can be conventional, but dimensionless mass ratios and binding fractions remain observable",
            "current_status": "GUARD_ONLY",
            "missing_for_claim": "MISSING_DIMENSIONLESS_SPECTRUM_THEOREM",
            "fallback_coefficient": "b_mass_common_mode_not_scored;b_mu;b_mA",
            "source_paths": src("1047_mass_audit", "1330_nist_mass"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MRA1804_1_mass_ratios",
            "object": "m_e/m_p and related particle ratios",
            "zero_route": "quotient-owned matter spectrum or representation-superselected dimensionless mass ratios",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_YUKAWA_HIGGS_QCD_MAP;MISSING_NO_MASS_VERTEX",
            "fallback_coefficient": "b_mu",
            "source_paths": src("638_constant_zero", "1047_mass_audit", "990_parent_contract", "1330_nist_mass"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MRA1804_2_binding_fractions",
            "object": "nuclear/electromagnetic binding and composition response",
            "zero_route": "binding response descends through quotient-owned alpha, mass and nuclear constants",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_BINDING_ENERGY_DECOMPOSITION;MISSING_MATERIAL_SENSITIVITY_MATRIX",
            "fallback_coefficient": "b_nuc;b_mA;beta_A",
            "source_paths": src("1047_mass_audit", "local_bounds", "1399_alpha_prior"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MRA1804_3_species_source_response",
            "object": "source/test material mass response",
            "zero_route": "species labels are discrete, and source density/preparation normalization must be quotient-owned",
            "current_status": "PARTIAL_ONLY_SOURCE_MARKER_OPEN",
            "missing_for_claim": "MISSING_NO_MARKER_THEOREM;MISSING_SOURCE_NORMALIZATION_OWNER",
            "fallback_coefficient": "b_mA;beta_source;beta_test",
            "source_paths": src("1803_qbar_coefficients", "local_bounds"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MRA1804_4_verdict",
            "object": "mass-ratio theorem-zero",
            "zero_route": "b_mu=b_mA=b_nuc=0 for every observable mass ratio and binding contribution",
            "current_status": "BLOCKED_RETAIN_B_MA",
            "missing_for_claim": "MISSING_PARENT_MATTER_SPECTRUM_AND_NO_MASS_VERTEX_SIGNATURE",
            "fallback_coefficient": "b_mu;b_mA;b_nuc;qbar_constants_abs",
            "source_paths": src("1047_mass_audit", "1047_coefficients", "990_parent_contract"),
            "valid_for_claim": False,
        },
    ]


def clock_projection_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, source_row in enumerate(clock_source_rows()):
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "projection_id": f"CLK1804_{index}_{source_row['clock_pair_id']}",
                "clock_pair": source_row["clock_pair"],
                "K_alpha_1": source_row["K_alpha_1"],
                "K_alpha_2": source_row["K_alpha_2"],
                "source_delta_K_alpha": source_row["delta_K_alpha_used"],
                "source_status": source_row["delta_K_alpha_source_status"],
                "source_urls": source_row["source_urls"],
                "projection_formula": "d ln R_pair = DeltaK_alpha*b_alpha*dXhat + DeltaK_mu*b_mu*dXhat + DeltaK_nuc*b_nuc*dXhat + ...",
                "MTS_missing": "MISSING_B_ALPHA_ZERO_OR_VALUE;MISSING_B_MU_B_NUC;MISSING_TAU_CLOCK;MISSING_LOCAL_DXHAT_MAP",
                "coefficient_row": "CPR1804_4_b_clock_i",
                "numeric_score_ready": False,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "projection_id": "CLK1804_2_clock_redshift_anchor",
            "clock_pair": "Galileo eccentric-satellite redshift/LPI bound",
            "K_alpha_1": "not_applicable",
            "K_alpha_2": "not_applicable",
            "source_delta_K_alpha": "not_a_pair_sensitivity",
            "source_status": "local_bound_anchor",
            "source_urls": "https://arxiv.org/abs/1812.03711;doi:10.1103/PhysRevLett.121.231101",
            "projection_formula": "alpha_clock_redshift constrains the full clock/readout residual, not b_alpha alone",
            "MTS_missing": "MISSING_CLOCK_READOUT_RESIDUAL_MAP;MISSING_CHI_X_PHI_OR_LOCAL_POTENTIAL_PROJECTION",
            "coefficient_row": "CPR1804_4_b_clock_i",
            "numeric_score_ready": False,
            "valid_for_claim": False,
        }
    )
    return rows


def coefficient_provenance_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative d ln alpha_EM/dXhat or equivalent gauge kinetic/readout derivative",
            "units": "Xhat^-1_or_declared_dimensionless_after_Xhat_normalization",
            "formula_or_bound": "b_alpha=0 only if alpha_EM is quotient-owned/superselected; otherwise clocks/WEP/R10 use b_alpha times local projections and sensitivities",
            "required_parent_inputs": "T_Q owner; unique F_Q^2; no f_X F^2; current owner; quotient readout; Xhat normalization; tau_clock/tau_WEP/tau_R10",
            "current_value": "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM",
            "source_paths": src("1803_qbar_coefficients", "646_clock_sensitivity", "989_em_signature", "1399_alpha_prior"),
            "observable_links": "clock;EM_spectra;WEP;R10;local_GR",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_1_b_mu",
            "symbol": "b_mu",
            "definition": "vertical derivative of dimensionless mass ratios such as m_e/m_p",
            "units": "Xhat^-1_or_declared_dimensionless_after_Xhat_normalization",
            "formula_or_bound": "clock and composition rows contain K_mu*b_mu unless the parent matter spectrum proves b_mu=0",
            "required_parent_inputs": "matter spectrum owner; Yukawa/Higgs/QCD map; no mass vertex; mass-ratio source paths; clock K_mu rows",
            "current_value": "MISSING_B_MU_OR_PARENT_ZERO_THEOREM",
            "source_paths": src("638_constant_zero", "1047_coefficients", "990_parent_contract", "1330_nist_mass"),
            "observable_links": "clock;WEP;composition;source_charge",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_2_b_mA",
            "symbol": "b_mA",
            "definition": "vertical derivative of material/species mass and binding response after removing a unit-only common mode",
            "units": "Xhat^-1_or_declared_dimensionless_after_Xhat_normalization",
            "formula_or_bound": "eta_AB and R10 source/test charge rows contain Delta sensitivity_AB*b_mA*tau_arena plus alpha and nuclear terms",
            "required_parent_inputs": "composition sensitivity matrix; binding fractions; no material marker theorem; source/test projection; Xhat normalization",
            "current_value": "MISSING_B_MASS_OR_COMPOSITION_SENSITIVITY_MATRIX",
            "source_paths": src("1803_qbar_coefficients", "1047_coefficients", "local_bounds"),
            "observable_links": "MICROSCOPE;R10;clock;Newton_GM;source_charge",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_3_b_nuc",
            "symbol": "b_nuc",
            "definition": "vertical derivative of nuclear binding or nuclear-sector clock sensitivity parameters not captured by b_mu",
            "units": "Xhat^-1_or_declared_dimensionless_after_Xhat_normalization",
            "formula_or_bound": "clock and WEP rows contain K_nuc*b_nuc or material nuclear sensitivity times b_nuc",
            "required_parent_inputs": "nuclear sensitivity matrix; binding-energy decomposition; no nuclear-response vertex; source/test material map",
            "current_value": "MISSING_B_NUC_OR_PARENT_ZERO_THEOREM",
            "source_paths": src("1047_mass_audit", "646_clock_projection", "local_bounds"),
            "observable_links": "clock;WEP;composition;source_charge",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_4_b_clock_i",
            "symbol": "b_clock_i",
            "definition": "vertical derivative of a clock transition or clock ratio after alpha, mass and nuclear sensitivities are projected",
            "units": "Xhat^-1_or_declared_dimensionless_after_Xhat_normalization",
            "formula_or_bound": "b_clock_pair = DeltaK_alpha*b_alpha + DeltaK_mu*b_mu + DeltaK_nuc*b_nuc + ...",
            "required_parent_inputs": "clock sensitivity matrix; b_alpha; b_mu; b_nuc; tau_clock/local dXhat projection; source path per clock pair",
            "current_value": "MISSING_CLOCK_CONSTANT_PROJECTION",
            "source_paths": src("646_clock_sensitivity", "646_clock_projection", "1047_clock_rows", "local_bounds"),
            "observable_links": "clock_comparison;redshift_LPI;alpha_drift",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CPR1804_5_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "definition": "no-cancellation envelope for all constant-sector leakage into local source/readout observables",
            "units": "dimensionless_observable_charge_envelope_after_arena_projection",
            "formula_or_bound": "|qbar_constants| <= |s_alpha b_alpha| + |s_mu b_mu| + sum_A |s_A b_mA| + |s_nuc b_nuc| + sum_i |s_clock_i b_clock_i|",
            "required_parent_inputs": "all constant coefficients theorem-zero or numeric/source-backed; sensitivities; no-cancellation policy; arena projections",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_paths": src("1803_qbar_coefficients", "1047_coefficients", "646_clock_sensitivity", "local_bounds", "R10_review_curve"),
            "observable_links": "WEP;clock;R10;EM;local_GR;Newton_GM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_links_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "BL1804_0_clock_alpha_sensitivities",
            "observable": "clock frequency-ratio alpha sensitivities",
            "bound_source": str(next(source["source_path"] for source in SOURCES if source["source_key"] == "646_clock_sensitivity")),
            "bound_value": "DeltaK_alpha=2.95 for Al/Hg; DeltaK_alpha=-6.95 for Yb+ E3/E2",
            "link_to_component": "b_alpha;b_clock_i",
            "score_status": "SENSITIVITIES_AVAILABLE_MTS_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "BL1804_1_clock_redshift",
            "observable": "alpha_clock_redshift",
            "bound_source": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R2_clock_redshift",
            "bound_value": "2.48e-05 dimensionless 1sigma anchor",
            "link_to_component": "b_clock_i;clock_readout_residual",
            "score_status": "ANCHOR_AVAILABLE_CLOCK_MAP_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "BL1804_2_WEP",
            "observable": "eta_WEP_source_charge",
            "bound_source": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R1_WEP_source_charge",
            "bound_value": "2.8e-15 dimensionless 1sigma proxy",
            "link_to_component": "b_alpha;b_mu;b_mA;b_nuc;qbar_constants_abs",
            "score_status": "ANCHOR_AVAILABLE_COMPOSITION_MATRIX_AND_SOURCE_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "BL1804_3_R10",
            "observable": "alpha_X(lambda_X)",
            "bound_source": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"),
            "bound_value": "review_candidate_curve_only_not_claim_grade",
            "link_to_component": "qbar_constants_abs;b_alpha;b_mA",
            "score_status": "BOUND_AND_MTS_COMPONENTS_NOT_CLAIM_READY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "BL1804_4_EM_spectra",
            "observable": "dimensionless EM spectral constants",
            "bound_source": str(RESIDUALS / "P8_Y5_R10_1399_FINITE_ALPHAEM_PRIOR_VECTOR.csv"),
            "bound_value": "finite alpha prior vector is target-only/nonclaim",
            "link_to_component": "b_alpha;beta_source_alpha",
            "score_status": "DERIVATIVE_MAP_AND_PARENT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1804_0_sources",
            "gate": "all 1804 sources exist and needles are present",
            "current_status": "CHECKED_BY_VALIDATION",
            "reason": "source register is the provenance lock for this private checkpoint",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1804_1_theorem_zero",
            "gate": "constant-sector theorem-zero",
            "current_status": "BLOCKED",
            "reason": "alpha/mass/clock clauses are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1804_2_numeric_bound_matrix",
            "gate": "constant-sector rows scoreable by R10/WEP/clock bounds",
            "current_status": "BLOCKED",
            "reason": "coefficient values, local dXhat maps, sensitivities and arena projections remain missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1804_3_verdict",
            "gate": "local constant leakage closed",
            "current_status": "CONSTANT_COUPLING_BRANCH_NOT_ZERO_AND_NOT_BOUNDED",
            "reason": "dimensionless alpha, mass ratios, nuclear response and clocks remain live until the parent action forbids vertices or bound rows are sourced",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1804_0_alpha_F2_counterterm",
            "countermodel": "an independent f_X F_Q^2 or lambda_A F_Q^2 term changes alpha_EM while leaving the quotient geometry intact",
            "survives_current_constraints": True,
            "why_survives": "unique-F2/no-alpha-vertex parent signature is not signed",
            "what_kills_it": "parent curvature normal form proving one unique EM kinetic normalization",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1804_1_mass_vertex",
            "countermodel": "m_A(Xhat), y_A(Xhat), or binding-response functions alter mass ratios/composition without violating covariance",
            "survives_current_constraints": True,
            "why_survives": "matter spectrum and no-mass-vertex clauses are explicit closures, not derivations",
            "what_kills_it": "parent matter functor deriving spectrum and forbidding Xhat-dependent mass vertices",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1804_2_clock_readout_shadow",
            "countermodel": "clock readout inherits alpha/mass/nuclear sensitivities or a shadow coframe/time map",
            "survives_current_constraints": True,
            "why_survives": "tau_clock/local dXhat map and readout descent are missing",
            "what_kills_it": "clock readout descent plus source-backed sensitivity projection matrix",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1804_3_nuclear_binding",
            "countermodel": "nuclear binding sensitivity creates WEP/clock source charge even if alpha-only channel is quiet",
            "survives_current_constraints": True,
            "why_survives": "nuclear response matrix and material sensitivity decomposition are not derived",
            "what_kills_it": "binding-energy ownership theorem or finite source-backed b_nuc/b_mA rows",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1804_0_alpha_zero",
            "claim": "alpha_EM is vertically silent",
            "status": "BLOCKED",
            "reason": "charge generator, unique-F2, current owner, no-alpha vertex and readout descent are not all parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1804_1_mass_zero",
            "claim": "observable mass ratios and binding fractions are vertically silent",
            "status": "BLOCKED",
            "reason": "parent matter spectrum, binding decomposition and no-mass-vertex proof are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1804_2_clock_zero",
            "claim": "clock transition ratios are vertically silent",
            "status": "BLOCKED",
            "reason": "clock rows inherit alpha/mass/nuclear debts and require tau_clock/local dXhat projection",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1804_3_bound_scoring",
            "claim": "constant leakage is bounded strongly enough for local-GR/Newton branch",
            "status": "BLOCKED",
            "reason": "coefficient values and arena projections are absent; R10 curve remains review-candidate nonclaim",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1804_4_local_GR_Newton",
            "claim": "constant coupling branch supports local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "qbar_constants_abs is not theorem-zero and not numerically bounded",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1804_0_theorem_shape",
            "decision": "CONSTANT_SILENCE_THEOREM_EXACT_CONDITIONAL",
            "reason": "quotient descent or discrete/topological superselection plus Dq[v_X]=0 kills vertical derivatives by chain rule/locality",
            "next_action": "do not promote until alpha/mass/clock objects are parent-classified",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1804_1_no_constant_promotion",
            "decision": "ALPHA_MASS_CLOCK_CHANNELS_RETAINED",
            "reason": "dimensionless constants and ratios cannot be hidden by unit choices, and parent ownership clauses are unsigned",
            "next_action": "retain b_alpha, b_mu, b_mA, b_nuc, b_clock_i and qbar_constants_abs",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1804_2_best_next",
            "decision": "NO_EXTRA_F2_NO_MASS_VERTEX_SIGNATURE_OR_ALPHA_MASS_BOUND_MATRIX_NEXT",
            "reason": "the proof bottleneck is now the parent action's allowed vertex list for EM kinetic, mass and binding terms",
            "next_action": "build 1805 to try the parent signature first, then fall back to alpha/mass/clock bound matrix",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1804_0_primary",
            "next_target": "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md",
            "script": "scripts/Y5_R2FR_no_extra_F2_no_mass_vertex_signature_or_alpha_mass_bound_matrix.py",
            "objective": "attempt a parent-action signature forbidding independent f_X F^2, m_A(Xhat), y_A(Xhat), and binding-response vertices; if it fails, build an alpha/mass/clock bound projection matrix",
            "selection_status": "selected",
            "success_condition": "parent no-extra-F2/no-mass-vertex theorem-zero or source-backed finite b_alpha/b_mu/b_mA/b_nuc/b_clock_i bound matrix with arena projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1804_1_parallel_clock",
            "next_target": "1805b-Y5-R2FR-clock-readout-descent-or-tau-clock-bound.md",
            "script": "scripts/Y5_R2FR_clock_readout_descent_or_tau_clock_bound.py",
            "objective": "prove clock readout descends through q or emit tau_clock/local dXhat projection rows",
            "selection_status": "held_parallel",
            "success_condition": "clock readout theorem or source-backed tau_clock rows",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "constant_superselection_gate": constant_superselection_gate_rows(),
        "alpha_gauge_audit": alpha_gauge_audit_rows(),
        "mass_ratio_audit": mass_ratio_audit_rows(),
        "clock_projection_rows": clock_projection_rows(),
        "coefficient_provenance_rows": coefficient_provenance_rows(),
        "bound_links": bound_links_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1804_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "score_ready",
        "numeric_score_ready",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            for flag in claim_flags:
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ready_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "score_ready",
        "numeric_score_ready",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in ready_flags:
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1804_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1804_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1804_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1804_2_theorem_not_promoted",
            any(
                row["gate_id"] == "CSG1804_5_verdict"
                and row["current_status"] == "CONSTANT_SUPERSELECTION_NOT_PROVED_COEFFICIENT_PROVENANCE_REQUIRED"
                and not boolish(row["theorem_zero"])
                for row in rows_map["constant_superselection_gate"]
            ),
            "constant superselection theorem remains unpromoted",
        ),
        (
            "VAL1804_3_alpha_retain_b_alpha",
            any(
                row["audit_id"] == "AGA1804_4_verdict"
                and row["verdict"] == "BLOCKED_RETAIN_B_ALPHA"
                and not boolish(row["valid_for_claim"])
                for row in rows_map["alpha_gauge_audit"]
            ),
            "alpha audit retains b_alpha",
        ),
        (
            "VAL1804_4_mass_retain_b_mA",
            any(
                row["audit_id"] == "MRA1804_4_verdict"
                and row["current_status"] == "BLOCKED_RETAIN_B_MA"
                and not boolish(row["valid_for_claim"])
                for row in rows_map["mass_ratio_audit"]
            ),
            "mass audit retains b_mA",
        ),
        (
            "VAL1804_5_clock_rows_source_backed_nonclaim",
            len(rows_map["clock_projection_rows"]) >= 3
            and any(row["source_delta_K_alpha"] == "2.95" for row in rows_map["clock_projection_rows"])
            and any(row["source_delta_K_alpha"] == "-6.95" for row in rows_map["clock_projection_rows"])
            and all(not boolish(row["numeric_score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["clock_projection_rows"]),
            "clock projection rows import source-backed sensitivities but remain nonclaim",
        ),
        (
            "VAL1804_6_provenance_rows_nonclaim_missing",
            all(
                not boolish(row["score_ready"]) and not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"])
                for row in rows_map["coefficient_provenance_rows"]
            )
            and all("MISSING" in row["current_value"] for row in rows_map["coefficient_provenance_rows"]),
            "coefficient provenance rows remain nonclaim and value-missing",
        ),
        (
            "VAL1804_7_bound_links_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["bound_links"])
            and any(row["anchor_id"] == "BL1804_3_R10" and "NOT_CLAIM_READY" in row["score_status"] for row in rows_map["bound_links"]),
            "bound links are present but nonclaim",
        ),
        (
            "VAL1804_8_acceptance_blocks",
            any(
                row["gate_id"] == "AC1804_3_verdict"
                and row["current_status"] == "CONSTANT_COUPLING_BRANCH_NOT_ZERO_AND_NOT_BOUNDED"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks constant coupling closure",
        ),
        (
            "VAL1804_9_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "constant-sector countermodels remain live",
        ),
        (
            "VAL1804_10_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all alpha/mass/clock/local claim gates are blocked",
        ),
        ("VAL1804_11_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1804_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1804_13_decision_next",
            any(
                row["decision_id"] == "DEC1804_2_best_next"
                and row["decision"] == "NO_EXTRA_F2_NO_MASS_VERTEX_SIGNATURE_OR_ALPHA_MASS_BOUND_MATRIX_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects no-extra-F2/no-mass-vertex signature or bound matrix next",
        ),
        (
            "VAL1804_14_next_selected",
            any(row["route_id"] == "NEXT1804_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1804_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1804 CSVs parse"),
        ("VAL1804_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1804_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1804_18_formalization_untouched", formalization_untouched(), "no 1804 outputs found under formalization-workbench"),
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
            "check_id": "VAL1804_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1804 constant superselection alpha mass clock provenance checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1804 - Y5/R2FR Constant Superselection, Alpha/Mass/Clock Provenance",
            "",
            "## Verdict",
            "",
            "1804 proves the exact local shape of the constant-silence theorem, but it does not promote the local branch. If a constant is quotient-descended, `theta(Phi)=theta_bar(q(Phi))`, or lives in a truly discrete/topological superselection sector, and `Dq[v_X]=0`, then the vertical derivative vanishes by the chain rule/locality.",
            "",
            "That proof is not enough for the actual physical constants. `alpha_EM`, mass ratios, binding/nuclear response, and clock transition ratios are dimensionless observables. They cannot be deleted by choosing units, and their parent ownership is not signed in the current action grammar.",
            "",
            "So this checkpoint keeps `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `b_clock_i`, and `qbar_constants_abs` as live nonclaim rows. The useful win is that the coupling problem is now sharply localized: the next branch must either forbid independent EM kinetic/mass/binding vertices from the parent action or build a finite alpha/mass/clock bound matrix.",
            "",
            "**Claim ceiling:** no alpha theorem-zero, no mass-ratio theorem-zero, no clock-readout theorem-zero, no qbar_constants_abs score, no local-GR/Newton reduction claim, no R10/WEP/clock claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1804.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Constant Superselection Gate",
            markdown_table(rows_map["constant_superselection_gate"], ["gate_id", "claim_piece", "mathematical_statement", "current_status", "missing_for_claim", "theorem_zero", "valid_for_claim"]),
            "",
            "## Alpha Gauge Audit",
            markdown_table(rows_map["alpha_gauge_audit"], ["audit_id", "object", "required_parent_signature", "current_evidence", "verdict", "fallback_coefficient", "valid_for_claim"]),
            "",
            "## Mass Ratio Audit",
            markdown_table(rows_map["mass_ratio_audit"], ["audit_id", "object", "zero_route", "current_status", "missing_for_claim", "fallback_coefficient", "valid_for_claim"]),
            "",
            "## Clock Projection Rows",
            markdown_table(rows_map["clock_projection_rows"], ["projection_id", "clock_pair", "source_delta_K_alpha", "source_status", "projection_formula", "MTS_missing", "numeric_score_ready", "valid_for_claim"]),
            "",
            "## Coefficient Provenance Rows",
            markdown_table(rows_map["coefficient_provenance_rows"], ["row_id", "symbol", "definition", "current_value", "observable_links", "score_ready", "valid_for_claim"]),
            "",
            "## Bound Links",
            markdown_table(rows_map["bound_links"], ["anchor_id", "observable", "bound_value", "link_to_component", "score_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
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
            "This is the coupling bottleneck in clean form. It is not a disaster; it is the exact place a serious field theory has to earn its keep. If the parent action forbids the extra `F^2`, mass, Yukawa, and binding-response vertices, the local route gets dramatically stronger. If it cannot, the theory must carry finite coefficients and beat/stand with the data honestly.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1804 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
