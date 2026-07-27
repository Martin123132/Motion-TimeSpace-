from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1049-R10-residual-prior-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1049_RESIDUAL_PRIOR_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1049_0_1048_next",
            "source-intake/mts_residuals/P8_Y5_R10_1048_NEXT_TARGET.csv",
            "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
            "1048 handoff to parent operator-classification symmetry ban.",
        ),
        (
            "SRC1049_1_1048_parent_signature",
            "source-intake/mts_residuals/P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv",
            "PVS1048_5_verdict",
            "1048 parent vertex signature audit.",
        ),
        (
            "SRC1049_2_1048_F2",
            "source-intake/mts_residuals/P8_Y5_R10_1048_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
            "F2T1048_1_no_scalar_counterterm",
            "1048 no-extra-F2 theorem attempt.",
        ),
        (
            "SRC1049_3_1048_mass",
            "source-intake/mts_residuals/P8_Y5_R10_1048_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv",
            "MVT1048_3_verdict",
            "1048 no-mass-vertex theorem attempt.",
        ),
        (
            "SRC1049_4_1048_matrix",
            "source-intake/mts_residuals/P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
            "BM1048_3_R10_yukawa",
            "1048 alpha/mass/clock bound matrix.",
        ),
        (
            "SRC1049_5_operator_requirements",
            "source-intake/mts_residuals/P8_OPERATOR_CLASSIFICATION_REQUIREMENTS.csv",
            "retained_residual",
            "Existing local operator classification requirements.",
        ),
        (
            "SRC1049_6_marker_symmetry",
            "source-intake/mts_residuals/P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv",
            "NL609_4_no_linear_verdict",
            "Earlier no-linear-marker symmetry gate.",
        ),
        (
            "SRC1049_7_989_signature",
            "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "ELA989_1_unique_F2",
            "EM-lock signature audit showing unique-F2 counterexample.",
        ),
        (
            "SRC1049_8_990_contract",
            "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "PAC990_3_EM_lock",
            "Minimal parent action contract.",
        ),
        (
            "SRC1049_9_clock_sensitivity",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_0_AlHg",
            "Clock alpha sensitivity source rows.",
        ),
        (
            "SRC1049_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "Local WEP/source, clock, PPN, and Gdot anchors.",
        ),
        (
            "SRC1049_11_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1049_12_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 runner and schema.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def operator_classification_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_id": "OCR1049_0_declared_parent_domain",
            "candidate_rule": "Every local operator must be generated from the declared parent fields, quotient map, and representation data before empirical fitting.",
            "mathematical_form": "Op_allowed subset Alg[q(Phi), Dq(Phi), F_parent, theta_rep, topological classes] with no arbitrary scalar coefficient functions of Xhat.",
            "would_forbid": "post-hoc f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), clock-readout_Xhat unless they are declared retained residuals",
            "derivation_status": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
            "failure_mode": "without this rule, any neutral scalar can multiply gauge/matter operators",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "OCR1049_1_quotient_descent_selection",
            "candidate_rule": "Ordinary visible-sector coefficients must descend through q_loc or be discrete/topological representation labels.",
            "mathematical_form": "c_i(Phi)=cbar_i(q_loc(Phi)) or c_i in Rep_top; Dq[v_X]=0 => Lie_v c_i=0",
            "would_forbid": "smooth vertical coefficient functions in visible matter/EM/readout sectors",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "failure_mode": "does not prove the actual parent action classifies alpha/mass/clock constants this way",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "OCR1049_2_product_sequestration",
            "candidate_rule": "Hidden/local-relaxation fields are sequestered from visible kinetic and mass coefficients except through the quotient geometry.",
            "mathematical_form": "S_parent=S_vis[q(Phi),Psi,theta_rep]+S_hidden[Xhat,...]+S_coupling_allowed[q] and excludes Xhat*O_vis",
            "would_forbid": "f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), nu_i(Xhat)",
            "derivation_status": "POWERFUL_BUT_PARENT_AXIOM_IF_UNSIGNED",
            "failure_mode": "sequestration is exactly the missing thing; cannot be smuggled in after failed local tests",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "OCR1049_3_symmetry_filter",
            "candidate_rule": "A shift/parity/internal symmetry for Xhat forbids visible-sector coefficient functions unless broken only inside the hidden sector.",
            "mathematical_form": "Xhat -> Xhat + const or Xhat -> -Xhat; require O_vis neutral and coefficient f_X invariant/constant",
            "would_forbid": "linear Xhat*O_vis under shift/parity; full f_X only under stronger shift/sequestration",
            "derivation_status": "INSUFFICIENT_BY_ITSELF",
            "failure_mode": "parity allows Xhat^2 F^2; broken shift allows radiative/readoout re-entry; hidden-sector mass terms may break the symmetry",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "OCR1049_4_naturalness_guard",
            "candidate_rule": "If a forbidden vertex is not symmetry-forbidden, it must be retained as a residual with prior/source provenance.",
            "mathematical_form": "not symmetry_banned(Op_i) => coefficient_i in residual vector R_const with prior/status/source gates",
            "would_forbid": "claiming zero from aesthetic minimality or absence in the current draft",
            "derivation_status": "VALID_AUDIT_POLICY",
            "failure_mode": "prevents the theory from passing local tests by omission",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "OCR1049_5_verdict",
            "candidate_rule": "operator-classification symmetry ban closes alpha/mass/clock vertices",
            "mathematical_form": "OCR1049_0+1+2 plus symmetry/radiative closure => b_alpha=b_mu=b_mA=b_nuc=b_clock_i=0",
            "would_forbid": "all 1048 hidden constant vertices",
            "derivation_status": "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED",
            "failure_mode": "current corpus has conditional contracts, not a derived parent symmetry/operator classification",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def symmetry_ban_rows() -> list[dict[str, str]]:
    return [
        {
            "test_id": "SBT1049_0_diffeomorphism_covariance",
            "symmetry_or_principle": "diffeomorphism covariance",
            "operator_tested": "f_X(Xhat) F_Q^2; m_A(Xhat) psi_bar psi; y_A(Xhat) psi H psi; B_A(Xhat)",
            "result": "DOES_NOT_FORBID",
            "reason": "all are scalar densities/covariant local terms when Xhat is a scalar field or representative marker",
            "residual_if_fail": "b_alpha;b_mA;b_mu;b_nuc",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SBT1049_1_gauge_invariance",
            "symmetry_or_principle": "visible U(1)/gauge invariance",
            "operator_tested": "f_X(Xhat) F_Q^2",
            "result": "DOES_NOT_FORBID",
            "reason": "gauge invariance allows scalar gauge kinetic functions unless a stronger parent connection-norm uniqueness rule excludes them",
            "residual_if_fail": "b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SBT1049_2_shift_symmetry",
            "symmetry_or_principle": "exact vertical shift symmetry",
            "operator_tested": "all non-derivative Xhat coefficient functions",
            "result": "WOULD_FORBID_IF_EXACT_BUT_UNSIGNED",
            "reason": "an exact shift can ban f_X, m_X, y_X, B_X, and clock_X terms, but the current local branch uses profiles/potentials/projections that are not proven shift-invariant",
            "residual_if_fail": "all constant residual coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SBT1049_3_parity_evenness",
            "symmetry_or_principle": "Xhat -> -Xhat parity",
            "operator_tested": "linear Xhat*O_vis",
            "result": "INSUFFICIENT",
            "reason": "parity kills only odd terms; Xhat^2 F^2 and even mass/binding responses still survive unless Xhat=0 is separately proved",
            "residual_if_fail": "quadratic/even residual coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SBT1049_4_product_functor",
            "symmetry_or_principle": "visible/hidden product functor or sequestering",
            "operator_tested": "Xhat*O_vis and f_X(Xhat)O_vis",
            "result": "WOULD_FORBID_IF_PARENT_SIGNED",
            "reason": "this is the strongest clean route: visible matter/EM only see q_loc, hidden sector only couples through permitted quotient geometry",
            "residual_if_fail": "all alpha/mass/clock bound matrix rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "test_id": "SBT1049_5_radiative_readout_closure",
            "symmetry_or_principle": "renormalization and readout closure",
            "operator_tested": "loop-induced f_X F^2 and effective clock/readout Xhat dependence",
            "result": "UNSIGNED",
            "reason": "even a tree-level ban needs the same rule to survive effective/readout reductions",
            "residual_if_fail": "b_alpha;b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_table_rows() -> list[dict[str, str]]:
    return [
        {
            "operator_id": "ODT1049_0_fX_F2",
            "operator": "f_X(Xhat) F_Q^2 or lambda_A F_Q^2",
            "classification_needed": "forbidden by product/sequester or exact shift symmetry",
            "current_classification": "retained_residual",
            "why": "covariant and gauge-invariant; not excluded by current parent action",
            "residual_slot": "RP1049_0_b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "ODT1049_1_mass_X",
            "operator": "m_A(Xhat) psi_bar_A psi_A",
            "classification_needed": "forbidden by fixed matter spectrum or exact shift/sequester",
            "current_classification": "retained_residual",
            "why": "local covariant matter term; no derived spectrum owner",
            "residual_slot": "RP1049_2_b_mA",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "ODT1049_2_yukawa_X",
            "operator": "y_A(Xhat) psi_A H psi_B",
            "classification_needed": "forbidden by representation-owned Yukawa/mass-ratio data",
            "current_classification": "retained_residual",
            "why": "dimensionless mass ratios are observable and unowned",
            "residual_slot": "RP1049_1_b_mu",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "ODT1049_3_binding_X",
            "operator": "B_A(Xhat), Lambda_QCD(Xhat), nuclear/EM binding response",
            "classification_needed": "forbidden by composite matter response theorem or bounded sensitivity matrix",
            "current_classification": "retained_residual",
            "why": "composite bodies can carry WEP/R10 charge even when point-particle masses are quiet",
            "residual_slot": "RP1049_3_b_nuc",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "ODT1049_4_clock_X",
            "operator": "nu_i(Xhat), clock frame/readout Xhat dependence",
            "classification_needed": "forbidden by quotient-owned readout functor and upstream constants",
            "current_classification": "retained_residual",
            "why": "clock rows can reopen through readout even if WEP is silent",
            "residual_slot": "RP1049_4_b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def residual_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "RP1049_0_b_alpha",
            "symbol": "b_alpha",
            "residual_definition": "vertical derivative of dimensionless EM/gauge kinetic/readout alpha channel",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock alpha drift/sensitivity; WEP composition alpha charge; R10 source/test projection; parent Xhat normalization",
            "promotion_rule": "valid only if parent theorem-zero signs or numeric prior width and projection are source-backed",
            "observable_links": "clock;WEP;R10;EM spectra",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RP1049_1_b_mu",
            "symbol": "b_mu",
            "residual_definition": "vertical derivative of dimensionless mass ratios such as m_e/m_p",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock K_mu sensitivities; mass-ratio variation constraints; parent spectrum normalization",
            "promotion_rule": "valid only if mass-ratio theorem-zero signs or K_mu/b_mu prior rows are source-backed",
            "observable_links": "clock;WEP;composition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RP1049_2_b_mA",
            "symbol": "b_mA",
            "residual_definition": "vertical derivative of material/species mass response after removing unit common mode",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "composition sensitivity matrix; source/test material charges; MICROSCOPE/R10 projection; parent Xhat normalization",
            "promotion_rule": "valid only if composition matrix and local projection are sourced",
            "observable_links": "WEP;R10;Newton_GM;clock",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RP1049_3_b_nuc",
            "symbol": "b_nuc",
            "residual_definition": "vertical derivative of nuclear/QCD/electromagnetic binding response",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "nuclear sensitivity coefficients; material response table; clock nuclear sensitivity rows",
            "promotion_rule": "valid only if binding-response theorem-zero signs or sensitivity/prior rows are source-backed",
            "observable_links": "WEP;R10;clock",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RP1049_4_b_clock_i",
            "symbol": "b_clock_i",
            "residual_definition": "vertical derivative of direct clock/readout residual not already covered by alpha/mass/nuclear constants",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock pair sensitivity matrix; redshift/LPI readout model; tau_clock projection",
            "promotion_rule": "valid only if readout theorem-zero signs or clock residual prior is source-backed",
            "observable_links": "clock comparison;redshift/LPI",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RP1049_5_qbar_constants_abs_prior",
            "symbol": "qbar_constants_abs_prior",
            "residual_definition": "absolute-envelope prior for all constant-sector source/readout leakage",
            "prior_shape": "sum_abs_components_no_cancellation",
            "prior_width_status": "MISSING_COMPONENT_PRIORS",
            "required_sources": "RP1049_0 through RP1049_4; arena projection matrices; no-cancellation envelope",
            "promotion_rule": "valid only if every component is theorem-zero or numeric/source-backed",
            "observable_links": "WEP;R10;clock;PPN;local_GR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prior_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "matrix_id": "PM1049_0_clock_alpha_mu",
            "arena": "clock_frequency_ratios",
            "prior_vector": "[b_alpha,b_mu,b_nuc,b_clock_i]",
            "projection_formula": "d ln R_ab = DeltaK_alpha*b_alpha*dXhat + DeltaK_mu*b_mu*dXhat + DeltaK_nuc*b_nuc*dXhat + b_clock_ab*dXhat",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "missing_for_score": "K_mu/K_nuc rows; tau_clock; b priors/theorem-zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "PM1049_1_WEP_composition",
            "arena": "MICROSCOPE_WEP",
            "prior_vector": "[b_alpha,b_mA,b_mu,b_nuc]",
            "projection_formula": "eta_AB = DeltaQ_AB dot beta_source_test[b_alpha,b_mA,b_mu,b_nuc] * tau_WEP",
            "source_anchor": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "missing_for_score": "composition charge matrix; source/test beta vectors; tau_WEP; b priors/theorem-zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "PM1049_2_R10_short_range",
            "arena": "R10_short_range_fifth_force",
            "prior_vector": "[b_alpha,b_mA,b_mu,b_nuc,qbar_marker,qbar_source]",
            "projection_formula": "alpha_X(lambda_X)=K_X Q_source(lambda_X) Q_test(lambda_X)/(4*pi*Z_X*G_obs)",
            "source_anchor": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "missing_for_score": "lambda_X;Z_X;K_X;Q_source/test;promoted bound curve; b priors/theorem-zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "PM1049_3_PPN_source",
            "arena": "local_GR_PPN_source",
            "prior_vector": "[metric_residual,source_Hamiltonian_residual,qbar_constants_abs_prior]",
            "projection_formula": "PPN/local source vector = P_metric[source charge, constant leakage, readout residual]",
            "source_anchor": "source-intake/local_bounds/local_bound_claims.csv:R3_gamma through R9_Gdot",
            "missing_for_score": "weak-field solution; source Hamiltonian owner; constant-sector residual vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PG1049_0_theorem_zero_gate",
            "promotion_condition": "A coefficient can be set to zero only if the parent action symmetry/operator classification forbids the corresponding vertex including radiative/readout re-entry.",
            "current_status": "not_satisfied",
            "why": "no signed product/sequester or exact shift symmetry currently covers all visible sectors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1049_1_numeric_prior_gate",
            "promotion_condition": "A retained coefficient prior can be used only with source path, units, normalization, and arena projection.",
            "current_status": "not_satisfied",
            "why": "prior slots are named but have MISSING_PRIOR_WIDTH and missing local projections",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1049_2_no_cancellation_gate",
            "promotion_condition": "Multi-coefficient residuals must be tested as absolute envelopes unless a theorem enforces cancellation.",
            "current_status": "active_guard",
            "why": "prevents tuned cancellations between alpha, mass, clock, marker, and source leakage",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1049_3_shared_domain_gate",
            "promotion_condition": "The same local domain/projection rule must be used for WEP, R10, clocks, and PPN.",
            "current_status": "not_satisfied",
            "why": "domain/screen rule remains a parent-level open clause",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "residual_prior_alpha_mass_clock_template",
            "curve_id": "MTS_1049_RESIDUAL_PRIOR_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_PRIOR_VECTOR_AND_QSOURCE_QTEST_PROJECTION",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "R10 alpha(lambda) from residual-prior vector [b_alpha,b_mA,b_mu,b_nuc,qbar_marker,qbar_source] through source/test charge projection",
            "derivation_status": "template_invalid_operator_ban_failed_and_prior_widths_missing",
            "formula_reference": "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md::PM1049_2_R10_short_range",
            "source_file": "MISSING_RESIDUAL_PRIOR_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; no local-GR/R10/WEP/clock pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject until theorem-zero or source-backed priors, lambda_X, Z_X, K_X, and source/test charges exist.",
        }
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1049_0_operator_ban",
            "object": "parent operator-classification symmetry ban",
            "current_status": "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED",
            "refusal_status": "blocked",
            "failure_reasons": "OCR1049_2_product_sequestration unsigned; OCR1049_3_symmetry_filter insufficient; SBT1049_0/1 do not forbid; SBT1049_5 unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1049_1_prior_slots",
            "object": "residual coefficient prior slots",
            "current_status": "MISSING_PRIOR_WIDTH_AND_PROJECTION",
            "refusal_status": "blocked",
            "failure_reasons": "RP1049_0_b_alpha;RP1049_1_b_mu;RP1049_2_b_mA;RP1049_3_b_nuc;RP1049_4_b_clock_i",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1049_2_R10_runner",
            "object": "R10 residual-prior placeholder smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={runner_status.get('valid_mts_rows')}; valid_bound_rows={runner_status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1049_0_operator_ban",
            "claim": "parent symmetry/operator classification forbids alpha/mass/clock hidden vertices",
            "gate_pass": "false",
            "reason": "diffeomorphism/gauge invariance do not forbid the vertices; stronger sequester/shift rule is unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1049_1_zero_coefficients",
            "claim": "b_alpha,b_mu,b_mA,b_nuc,b_clock_i can be set to zero",
            "gate_pass": "false",
            "reason": "theorem-zero promotion gate is not satisfied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1049_2_prior_scoring",
            "claim": "residual priors can score WEP/R10/clock/PPN",
            "gate_pass": "false",
            "reason": "prior widths, source/test charge projections, and local domain maps are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1049_3_local_GR",
            "claim": "local-GR/Newton branch closes from 1049",
            "gate_pass": "false",
            "reason": "operator-classification/prior stage does not replace source Hamiltonian and PPN weak-field derivations",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1049_0_symmetry_result",
            "decision": "ordinary covariance and gauge symmetry are insufficient",
            "because": "the unwanted vertices are legal scalar/gauge-invariant operators",
            "next_action": "do not claim zero from minimality; require signed sequester/shift rule or priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1049_1_best_theorem_route",
            "decision": "product/sequester parent functor is the clean theorem route",
            "because": "it would make visible matter/EM depend only on q_loc and representation data",
            "next_action": "attempt to derive product functor from parent quotient/readout architecture",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1049_2_fallback_route",
            "decision": "residual-prior slots are now explicit but not score-ready",
            "because": "coefficient names, arenas, and promotion rules exist but prior widths/projections are missing",
            "next_action": "source prior widths or derive zero before running empirical score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1049_3_best_next",
            "decision": "target product functor derivation before numeric priors",
            "because": "deriving sequester would collapse the constant-sector debt more cleanly than fitting many priors",
            "next_action": "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
            "objective": "try to derive the visible/hidden product functor that makes visible matter and EM depend only on q_loc and representation data; if it fails, source prior-width packs for b_alpha, b_mu, b_mA, b_nuc, and b_clock_i",
            "include": "sequester/product functor theorem, quotient-owned visible algebra, radiative/readout closure, residual-prior width source checklist, WEP/R10/clock/PPN projection readiness",
            "exclude": "unit-rescaling cheat, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    symmetry_rows: list[dict[str, str]],
    decision_table: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    prior_matrix: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    generated_paths: list[Path],
) -> list[dict[str, str]]:
    def status(result: bool) -> str:
        return "pass" if result else "fail"

    def no_claim(rows: list[dict[str, str]]) -> bool:
        return all(not flag(row.get("valid_for_claim", "false")) for row in rows)

    source_ok = all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows)
    operator_ok = any(row["rule_id"] == "OCR1049_1_quotient_descent_selection" and row["derivation_status"] == "EXACT_CONDITIONAL_THEOREM" for row in operator_rows) and any(
        row["rule_id"] == "OCR1049_5_verdict" and row["derivation_status"].startswith("FAIL_CURRENT_CLAIM") for row in operator_rows
    )
    symmetry_ok = any(row["test_id"] == "SBT1049_0_diffeomorphism_covariance" and row["result"] == "DOES_NOT_FORBID" for row in symmetry_rows) and any(
        row["test_id"] == "SBT1049_4_product_functor" and row["result"] == "WOULD_FORBID_IF_PARENT_SIGNED" for row in symmetry_rows
    )
    decision_ok = {"ODT1049_0_fX_F2", "ODT1049_1_mass_X", "ODT1049_2_yukawa_X", "ODT1049_3_binding_X", "ODT1049_4_clock_X"}.issubset(
        {row["operator_id"] for row in decision_table}
    )
    prior_ok = no_claim(prior_rows) and all("MISSING" in row["prior_width_status"] or row["prior_id"].endswith("qbar_constants_abs_prior") for row in prior_rows)
    matrix_ok = no_claim(prior_matrix) and {"PM1049_0_clock_alpha_mu", "PM1049_1_WEP_composition", "PM1049_2_R10_short_range"}.issubset({row["matrix_id"] for row in prior_matrix})
    promotion_ok = any(row["gate_id"] == "PG1049_0_theorem_zero_gate" and row["current_status"] == "not_satisfied" for row in promotion_rows)
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1050" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1049_SUMMARY", True, "1049 parent operator-classification symmetry ban or residual prior validation summary"),
        ("V1049_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1049_2_operator_rule_attempt_blocked", operator_ok, "operator-classification rule has exact conditional piece but current claim remains blocked"),
        ("V1049_3_symmetry_tests_blocked", symmetry_ok, "ordinary symmetries do not forbid vertices; product functor would if signed"),
        ("V1049_4_decision_table_complete", decision_ok, "all alpha/mass/clock forbidden vertices have retained residual decisions"),
        ("V1049_5_prior_slots_nonclaim", prior_ok, "residual-prior slots are present and not claim-valid"),
        ("V1049_6_prior_matrix_nonclaim", matrix_ok, "clock/WEP/R10/PPN prior matrix is staged as nonclaim"),
        ("V1049_7_promotion_gates_blocked", promotion_ok, "theorem-zero and numeric-prior promotion gates remain blocked"),
        ("V1049_8_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS R10 template has runner schema and no claim-valid rows"),
        ("V1049_9_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1049 placeholder rows"),
        ("V1049_10_claim_gates_blocked", gates_ok, "all operator-ban/prior/local-GR claim gates remain blocked"),
        ("V1049_11_next_target_written", next_ok, "next target row is present"),
        ("V1049_12_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1049_13_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
    ]
    return [
        {
            "check_id": check_id,
            "result": status(result),
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, result, detail in checks
    ]


def write_doc(sections: list[tuple[str, list[dict[str, object]], list[str]]]) -> None:
    lines = [
        "# 1049 Y5 R10 parent operator-classification symmetry ban or residual coefficient prior",
        "",
        "**Progress:** the operator-classification route is now sharpened. A quotient-descent/product-functor rule would forbid the dangerous visible-sector coefficient functions, but ordinary covariance and gauge invariance do not.",
        "",
        "**Current verdict:** no theorem-zero promotion. `f_X F^2`, `m_A(Xhat)`, `y_A(Xhat)`, binding-response, and clock-readout vertices remain legal unless a stronger parent sequester/shift rule is signed.",
        "",
        "**Fallback:** nonclaim residual-prior slots now exist for `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `b_clock_i`, and the absolute constant-sector envelope. They are not score-ready until prior widths and local projections are sourced.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    operator_rows = operator_classification_rows()
    symmetry_rows = symmetry_ban_rows()
    decision_table = decision_table_rows()
    prior_rows = residual_prior_rows()
    prior_matrix = prior_matrix_rows()
    promotion_rows = promotion_gate_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1049_0_R10_runner_refusal",
            "valid_mts_rows": runner_status.get("valid_mts_rows"),
            "valid_bound_rows": runner_status.get("valid_bound_rows"),
            "comparison_rows": runner_status.get("comparison_rows"),
            "R10_pass_for_claim": str(runner_status.get("R10_pass_for_claim")).lower(),
            "claim_allowed": str(runner_status.get("claim_allowed")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]
    refusal_rows = placeholder_refusal_rows(runner_status)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_map: list[tuple[Path, list[dict[str, object]]]] = [
        (OUT / "P8_Y5_R10_1049_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", operator_rows),
        (OUT / "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", symmetry_rows),
        (OUT / "P8_Y5_R10_1049_OPERATOR_DECISION_TABLE.csv", decision_table),
        (OUT / "P8_Y5_R10_1049_RESIDUAL_PRIOR_SLOTS.csv", prior_rows),
        (OUT / "P8_Y5_R10_1049_ALPHA_MASS_CLOCK_PRIOR_MATRIX.csv", prior_matrix),
        (OUT / "P8_Y5_R10_1049_PRIOR_PROMOTION_GATES.csv", promotion_rows),
        (OUT / "P8_Y5_R10_1049_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1049_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1049_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1049_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1049_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        operator_rows,
        symmetry_rows,
        decision_table,
        prior_rows,
        prior_matrix,
        promotion_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1049_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("Operator classification rule attempt", operator_rows, ["rule_id", "candidate_rule", "mathematical_form", "would_forbid", "derivation_status", "failure_mode", "valid_for_claim"]),
            ("Symmetry ban theorem attempt", symmetry_rows, ["test_id", "symmetry_or_principle", "operator_tested", "result", "reason", "residual_if_fail", "valid_for_claim"]),
            ("Operator decision table", decision_table, ["operator_id", "operator", "classification_needed", "current_classification", "why", "residual_slot", "valid_for_claim"]),
            ("Residual prior slots", prior_rows, ["prior_id", "symbol", "residual_definition", "prior_shape", "prior_width_status", "required_sources", "promotion_rule", "valid_for_claim"]),
            ("Alpha/mass/clock prior matrix", prior_matrix, ["matrix_id", "arena", "prior_vector", "projection_formula", "source_anchor", "missing_for_score", "claim_allowed", "valid_for_claim"]),
            ("Prior promotion gates", promotion_rows, ["gate_id", "promotion_condition", "current_status", "why", "valid_for_claim"]),
            ("MTS R10 smoke template", mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            ("Runner smoke status", runner_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            ("Placeholder refusal runner", refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            ("Claim gates", claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            ("Decision ledger", decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            ("Validation", validation, ["check_id", "result", "detail", "generated_utc"]),
            ("Next target", next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        ]
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"1049 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
