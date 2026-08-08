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
DOC = ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1047-R10-constant-superselection-provenance-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1047_CONSTANT_PROVENANCE_TEMPLATE_NONCLAIM.csv"
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
            "SRC1047_0_1046_next",
            "source-intake/mts_residuals/P8_Y5_R10_1046_NEXT_TARGET.csv",
            "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
            "1046 handoff to constant-superselection and coefficient provenance.",
        ),
        (
            "SRC1047_1_1046_constant_audit",
            "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "CMA1046_0_alpha_EM",
            "1046 constant/marker split audit.",
        ),
        (
            "SRC1047_2_1046_qbar_constants",
            "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "QCC1046_0_b_alpha",
            "1046 qbar_constants template rows.",
        ),
        (
            "SRC1047_3_637_constant_theorem",
            "source-intake/mts_residuals/P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv",
            "CO637_0_descent_criterion",
            "Conditional constant ownership theorem.",
        ),
        (
            "SRC1047_4_638_constant_zero",
            "source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv",
            "ZR638_1_alpha_EM",
            "Prior alpha/mass/clock zero-route attempt.",
        ),
        (
            "SRC1047_5_646_clock_sensitivities",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_0_AlHg",
            "Source-backed clock alpha sensitivity rows.",
        ),
        (
            "SRC1047_6_988_em_lock",
            "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "EMLOCK988_4_no_alpha_vertex",
            "EM-lock theorem gate and no-alpha vertex blocker.",
        ),
        (
            "SRC1047_7_988_joint_alpha",
            "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "JAV988_0_alpha_slot",
            "Joint clock/WEP alpha variable gate.",
        ),
        (
            "SRC1047_8_989_signature",
            "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "ELA989_1_unique_F2",
            "EM lock signature audit showing unique-F2 counterexample.",
        ),
        (
            "SRC1047_9_990_parent_contract",
            "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "PAC990_3_EM_lock",
            "Minimal parent action contract linking matter functor and EM lock.",
        ),
        (
            "SRC1047_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R2_clock_redshift",
            "Local WEP/source, PPN, clock and Gdot bound anchors.",
        ),
        (
            "SRC1047_11_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1047_12_R10_runner",
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


def constant_superselection_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "CST1047_0_descent_or_superselection_criterion",
            "claim_piece": "exact local criterion for a constant to be silent",
            "mathematical_form": "theta(Phi)=theta_bar(q_loc(Phi)) or theta in a discrete/topological representation sector; Dq_loc[v_X]=0 => Lie_v theta=0",
            "derivation_step": "The chain rule proves silence for quotient-descended constants; locality proves smooth vertical flows cannot change discrete labels.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "parent classification that alpha_EM, all mass ratios, and clock constants are only quotient/topological data",
            "if_missing": "retain b_alpha, b_mA, b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST1047_1_alpha_EM",
            "claim_piece": "alpha_EM vertical silence",
            "mathematical_form": "b_alpha := Lie_v ln alpha_EM = 0 if unique parent F_Q^2 normalization, fixed charge lattice, and quotient-owned readout are signed",
            "derivation_step": "alpha_EM is dimensionless, so only parent ownership/superselection can kill its vertical derivative; unit choice cannot.",
            "current_status": "FAIL_CURRENT_CLAIM_UNIQUE_F2_AND_READOUT_UNSIGNED",
            "missing_for_claim": "T_Q owner, unique Maxwell kinetic normalization, no f_X F^2 counterterm, hbar*c/readout descent",
            "if_missing": "b_alpha is a real retained local coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST1047_2_mass_ratios",
            "claim_piece": "particle mass-ratio vertical silence",
            "mathematical_form": "b_mA := Lie_v ln(m_A/m_ref) = 0 if Yukawa/Higgs/binding/nuclear response data are quotient-owned or representation-superselected",
            "derivation_step": "Dimensionful masses can be moved by units, but ratios and binding fractions cannot; the proof must act on dimensionless spectra.",
            "current_status": "FAIL_CURRENT_CLAIM_MATTER_SPECTRUM_NOT_PARENT_DERIVED",
            "missing_for_claim": "parent matter spectrum, binding-energy decomposition, no m_A(Xhat) or y_A(Xhat) vertices",
            "if_missing": "b_mA and composition beta_A remain retained coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST1047_3_clock_transitions",
            "claim_piece": "clock-ratio vertical silence",
            "mathematical_form": "b_clock_i = K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...; zero only if every upstream dimensionless constant is zero",
            "derivation_step": "Clock constants are not independent theorem-zero objects; they inherit alpha, mass-ratio, and nuclear-sector debts.",
            "current_status": "FAIL_CURRENT_CLAIM_INHERITS_ALPHA_MASS_NUCLEAR_DEBT",
            "missing_for_claim": "K matrix beyond alpha rows, b_alpha/b_mu/b_nuc theorem-zero or numeric provenance, local dXhat projection",
            "if_missing": "b_clock_i remains a retained readout coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST1047_4_no_unit_rescaling_cheat",
            "claim_piece": "dimensionless observable guard",
            "mathematical_form": "Lie_v ln(alpha_EM), Lie_v ln(m_A/m_B), and Lie_v ln(nu_i/nu_j) are observable and cannot be erased by choosing c, hbar, or a mass unit",
            "derivation_step": "A unit convention can fix one dimensionful scale, not all dimensionless ratios simultaneously.",
            "current_status": "GUARD_PASSED_RETAINED_IN_VALIDATION",
            "missing_for_claim": "none as guard; it forbids a false proof route",
            "if_missing": "would accidentally hide physical clock/WEP/EM channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST1047_5_verdict",
            "claim_piece": "constant superselection theorem promoted for local branch",
            "mathematical_form": "CST1047_0 + signed alpha/mass/clock parent ownership => qbar_constants_abs=0",
            "derivation_step": "The proof skeleton is exact, but the current corpus has not signed the parent ownership clauses for the actual Standard-Model-like constants.",
            "current_status": "FAIL_CURRENT_CLAIM_COEFFICIENT_PROVENANCE_REQUIRED",
            "missing_for_claim": "parent action or source-backed numerical coefficients",
            "if_missing": "build b_alpha, b_mA, b_clock_i provenance rows and keep local-GR/R10/WEP/clock claims blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_gauge_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "AGN1047_0_definition",
            "object": "alpha_EM",
            "normal_form": "alpha_EM = e_eff^2/(4*pi*hbar*c) with e_eff and F_Q^2 normalization owned by the same parent gauge block",
            "needed_parent_signature": "fixed compact charge generator T_Q; unique F_Q^2 norm; no independent f_X F_Q^2; quotient-owned hbar*c/readout",
            "current_evidence": "988 and 989 identify the route, but ELA989_1 records a legal lambda_A F_Q^2 counterterm.",
            "verdict": "NOT_SIGNED",
            "fallback_coefficient": "b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AGN1047_1_charge_lattice",
            "object": "charge labels",
            "normal_form": "n_A in a discrete representation/lattice sector, Lie_v n_A=0",
            "needed_parent_signature": "T_Q as varied parent-action object with fixed lattice normalization",
            "current_evidence": "conditional theorem shape exists; current owner remains unsigned.",
            "verdict": "PARTIAL_ONLY",
            "fallback_coefficient": "beta_source_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AGN1047_2_kinetic_normalization",
            "object": "gauge kinetic normalization",
            "normal_form": "g_EM^-2 = C_P <T_Q,T_Q>_P and Lie_v g_EM^-2=0",
            "needed_parent_signature": "unique parent curvature norm and no branch-dependent EM counterterm",
            "current_evidence": "989 marks unique-F2 as failed in current corpus.",
            "verdict": "FAILS_CURRENT_CORPUS",
            "fallback_coefficient": "b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AGN1047_3_readout",
            "object": "dimensionless EM readout",
            "normal_form": "Hodge star, coframe, hbar*c, and spectral readout all descend through q_loc",
            "needed_parent_signature": "observed coframe/readout functor is quotient-owned and no shadow clock frame remains",
            "current_evidence": "1046 no-shadow route is exact conditional but not parent signed.",
            "verdict": "UNSIGNED",
            "fallback_coefficient": "b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AGN1047_4_verdict",
            "object": "alpha theorem-zero",
            "normal_form": "b_alpha=0",
            "needed_parent_signature": "AGN1047_0 through AGN1047_3 all signed",
            "current_evidence": "At least unique-F2 and readout/no-alpha-vertex are unsigned or failed.",
            "verdict": "BLOCKED_RETAIN_B_ALPHA",
            "fallback_coefficient": "b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mass_ratio_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "MRS1047_0_mass_unit_guard",
            "object": "dimensionful masses",
            "zero_route": "one universal mass scale can be conventional only if all mass ratios and binding fractions are invariant",
            "current_status": "GUARD_ONLY",
            "missing_for_claim": "dimensionless spectrum theorem",
            "fallback_coefficient": "b_mass_scale_common_mode_not_scored",
            "observable_links": "none if truly universal unit mode; otherwise clocks/WEP/source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "MRS1047_1_electron_proton_ratio",
            "object": "mu = m_e/m_p and related mass ratios",
            "zero_route": "quotient-owned matter spectrum or representation-superselected mass ratios",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_for_claim": "Yukawa/Higgs/QCD/nuclear binding ownership in parent action",
            "fallback_coefficient": "b_mu",
            "observable_links": "clock;WEP;composition;source_charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "MRS1047_2_binding_fractions",
            "object": "nuclear/electromagnetic binding fractions",
            "zero_route": "binding response functions descend through quotient-owned alpha/mass/nuclear constants",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_for_claim": "material sensitivity matrix and no material-marker theorem",
            "fallback_coefficient": "b_nuc; beta_A",
            "observable_links": "WEP_source_charge;clock;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "MRS1047_3_species_weights",
            "object": "source/test material mass response",
            "zero_route": "species labels are discrete but source density and preparation normalization are quotient-owned",
            "current_status": "PARTIAL_ONLY",
            "missing_for_claim": "source density/marker no-shadow theorem and source-normalization owner",
            "fallback_coefficient": "b_mA; beta_source; beta_test",
            "observable_links": "MICROSCOPE;R10;Newton_GM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "MRS1047_4_verdict",
            "object": "mass-ratio theorem-zero",
            "zero_route": "b_mA=0 for every observable mass ratio and binding contribution",
            "current_status": "BLOCKED_RETAIN_B_MA",
            "missing_for_claim": "parent matter spectrum and material sensitivity proof",
            "fallback_coefficient": "b_mA",
            "observable_links": "WEP;clock;composition;R10;local_GR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def clock_projection_rows() -> list[dict[str, str]]:
    clock_rows = read_csv(OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv")
    rows: list[dict[str, str]] = []
    for row in clock_rows:
        pair_id = row.get("clock_pair_id", "")
        rows.append(
            {
                "projection_id": f"CLK1047_{len(rows)}_{pair_id}",
                "clock_pair": row.get("clock_pair", ""),
                "source_delta_K_alpha": row.get("delta_K_alpha_used", ""),
                "source_status": row.get("delta_K_alpha_source_status", ""),
                "projection_formula": "d ln R_pair = delta_K_alpha*b_alpha*dXhat + delta_K_mu*b_mu*dXhat + delta_K_nuc*b_nuc*dXhat + ...",
                "MTS_missing": "b_alpha theorem-zero or numeric; b_mu/b_nuc rows; tau_clock/local dXhat projection",
                "coefficient_row": "CP1047_3_b_clock_i",
                "numeric_score_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "projection_id": "CLK1047_2_clock_redshift_anchor",
            "clock_pair": "Galileo eccentric-satellite redshift/LPI bound",
            "source_delta_K_alpha": "not a sensitivity pair; direct redshift alpha_clock_redshift anchor",
            "source_status": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "projection_formula": "alpha_clock_redshift constrains the full local clock/readout residual, not b_alpha alone",
            "MTS_missing": "clock readout residual map from local MTS state to alpha_clock_redshift",
            "coefficient_row": "CP1047_3_b_clock_i",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def coefficient_provenance_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "CP1047_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative d ln alpha_EM/dXhat or equivalent gauge kinetic/readout derivative",
            "units": "Xhat^-1",
            "formula_or_bound": "b_alpha=0 only if alpha_EM is quotient-owned/superselected; otherwise clocks/WEP/R10 bound products of b_alpha with local projections and sensitivities",
            "required_parent_inputs": "T_Q owner; unique F_Q^2; no f_X F^2; quotient readout; Xhat normalization; tau_clock/tau_WEP/tau_R10",
            "current_value": "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv; source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "observable_links": "clock;EM spectra;WEP;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "CP1047_1_b_mu",
            "symbol": "b_mu",
            "definition": "vertical derivative of dimensionless mass ratios such as m_e/m_p",
            "units": "Xhat^-1",
            "formula_or_bound": "b_mu=0 only if mass ratios are quotient-owned/superselected; otherwise clock and composition rows must include K_mu*b_mu",
            "required_parent_inputs": "matter spectrum owner; Yukawa/Higgs/QCD map; mass-ratio source paths; Xhat normalization; clock K_mu rows",
            "current_value": "MISSING_B_MU_OR_PARENT_ZERO_THEOREM",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv; source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "observable_links": "clock;WEP;composition;source_charge",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "CP1047_2_b_mA",
            "symbol": "b_mA",
            "definition": "vertical derivative of material/species mass and binding response after removing unit-only common mode",
            "units": "Xhat^-1",
            "formula_or_bound": "eta_AB and R10 source/test charge rows contain Delta sensitivity_AB*b_mA*tau_arena plus alpha and nuclear terms",
            "required_parent_inputs": "composition sensitivity matrix; binding fractions; no material-marker theorem; source/test projection; Xhat normalization",
            "current_value": "MISSING_B_MASS_OR_COMPOSITION_SENSITIVITY_MATRIX",
            "source_paths": "source-intake/local_bounds/local_bound_claims.csv; source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "observable_links": "MICROSCOPE;R10;clock;Newton_GM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "CP1047_3_b_clock_i",
            "symbol": "b_clock_i",
            "definition": "vertical derivative of a clock transition or clock ratio after alpha, mass, and nuclear sensitivities are projected",
            "units": "Xhat^-1",
            "formula_or_bound": "b_clock_pair = DeltaK_alpha*b_alpha + DeltaK_mu*b_mu + DeltaK_nuc*b_nuc + ...",
            "required_parent_inputs": "clock sensitivity matrix; b_alpha; b_mu; b_nuc; tau_clock/local dXhat projection; source path per clock pair",
            "current_value": "MISSING_CLOCK_CONSTANT_PROJECTION",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv; source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "observable_links": "clock comparison;redshift/LPI;alpha drift",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "CP1047_4_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "definition": "no-cancellation envelope for all constant-sector leakage into local source/readout observables",
            "units": "dimensionless observable charge envelope after arena projection",
            "formula_or_bound": "|qbar_constants| <= |s_alpha b_alpha| + |s_mu b_mu| + sum_A |s_A b_mA| + sum_i |s_clock_i b_clock_i|",
            "required_parent_inputs": "all constant coefficients theorem-zero or numeric/source-backed; sensitivities; no-cancellation policy; arena projections",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "observable_links": "WEP;clock;R10;EM;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bound_link_rows() -> list[dict[str, str]]:
    return [
        {
            "anchor_id": "BL1047_0_clock_alpha_sensitivities",
            "observable": "clock frequency-ratio alpha sensitivities",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "bound_value": "DeltaK_alpha=2.95 for Al/Hg; -6.95 for Yb+ E3/E2",
            "link_to_component": "b_alpha;b_clock_i",
            "score_status": "SENSITIVITIES_AVAILABLE_MTS_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BL1047_1_clock_redshift",
            "observable": "alpha_clock_redshift",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "bound_value": "2.48e-05 dimensionless 1sigma anchor",
            "link_to_component": "b_clock_i;clock_readout_residual",
            "score_status": "ANCHOR_AVAILABLE_CLOCK_MAP_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BL1047_2_WEP",
            "observable": "eta_WEP_source_charge",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "bound_value": "2.8e-15 dimensionless 1sigma proxy",
            "link_to_component": "b_alpha;b_mA;qbar_constants_abs",
            "score_status": "ANCHOR_AVAILABLE_COMPOSITION_MATRIX_AND_SOURCE_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BL1047_3_R10",
            "observable": "alpha_X(lambda_X)",
            "bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "bound_value": "review_candidate_curve_only",
            "link_to_component": "qbar_constants_abs;b_alpha;b_mA",
            "score_status": "BOUND_AND_MTS_COMPONENTS_NOT_CLAIM_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "constant_alpha_template",
            "curve_id": "MTS_1047_B_ALPHA_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_B_ALPHA_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "alpha_X(lambda_X) receives constant-sector contribution from b_alpha after source/test sensitivity and arena projection",
            "derivation_status": "template_invalid_b_alpha_missing_or_not_parent_zero",
            "formula_reference": "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md::CP1047_0",
            "source_file": "MISSING_B_ALPHA_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; no local-GR/R10 pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject until b_alpha is theorem-zero or numeric/source-backed with lambda and arena projection.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "constant_mass_clock_template",
            "curve_id": "MTS_1047_B_MASS_CLOCK_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_QBAR_CONSTANTS_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge; source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "force_law_form": "qbar_constants_abs projects through b_mA and b_clock_i sensitivities into WEP/R10/clock rows",
            "derivation_status": "template_invalid_mass_clock_coefficients_missing",
            "formula_reference": "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md::CP1047_4",
            "source_file": "MISSING_QBAR_CONSTANTS_SOURCE_FILE",
            "assumptions": "private nonclaim constant fallback",
            "valid_for_claim": "false",
            "notes": "No source-backed mass or clock MTS coefficient values are present.",
        },
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1047_0_superselection",
            "object": "constant superselection theorem",
            "current_status": "FAIL_CURRENT_CLAIM_COEFFICIENT_PROVENANCE_REQUIRED",
            "refusal_status": "blocked",
            "failure_reasons": "CST1047_1_alpha_EM;CST1047_2_mass_ratios;CST1047_3_clock_transitions;CST1047_5_verdict",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1047_1_coefficients",
            "object": "b_alpha/b_mA/b_clock_i coefficient provenance rows",
            "current_status": "COMPONENT_VALUES_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": "CP1047_0_b_alpha;CP1047_1_b_mu;CP1047_2_b_mA;CP1047_3_b_clock_i;CP1047_4_qbar_constants_abs",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1047_2_R10_runner",
            "object": "R10 constant-sector placeholder smoke rows",
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
            "gate_id": "CG1047_0_alpha_zero",
            "claim": "alpha_EM is vertically silent",
            "gate_pass": "false",
            "reason": "unique-F2, charge owner, readout descent, and no-alpha vertex remain unsigned or failed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1047_1_mass_zero",
            "claim": "observable mass ratios and binding fractions are vertically silent",
            "gate_pass": "false",
            "reason": "parent matter spectrum and material sensitivity theorem are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1047_2_clock_zero",
            "claim": "clock transition ratios are vertically silent",
            "gate_pass": "false",
            "reason": "clock rows inherit alpha/mass/nuclear debts and need a local dXhat projection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1047_3_coefficients",
            "claim": "constant coefficients are source-backed bounded",
            "gate_pass": "false",
            "reason": "all coefficient rows contain MISSING markers and no theorem-zero certificate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1047_4_local_tests",
            "claim": "R10/WEP/clock branches can be scored from 1047",
            "gate_pass": "false",
            "reason": "anchors exist but MTS-side coefficient values and arena projections are absent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1047_0_theorem_shape",
            "decision": "constant silence theorem is exact only as a conditional",
            "because": "quotient descent or discrete/topological superselection kills vertical derivatives by chain rule/locality",
            "next_action": "do not claim until alpha/mass/clock objects are parent-classified",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1047_1_no_alpha_promotion",
            "decision": "alpha_EM cannot be zeroed by units or wishful EM-lock",
            "because": "alpha is dimensionless and unique-F2/readout/no-alpha-vertex clauses are unsigned",
            "next_action": "retain b_alpha and require parent no-extra-F2 proof or numeric bound projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1047_2_no_mass_clock_promotion",
            "decision": "mass and clock channels remain physical residuals",
            "because": "dimensionless mass ratios and clock ratios are observables, not unit conventions",
            "next_action": "retain b_mA and b_clock_i with no-cancellation envelope",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1047_3_best_next",
            "decision": "target no-extra-F2/no-mass-vertex parent signature or build bound matrix",
            "because": "the proof bottleneck is now the parent action's allowed vertex list, not the algebra",
            "next_action": "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
            "objective": "attempt a parent-action signature that forbids independent f_X F^2, m_A(Xhat), y_A(Xhat), and binding-response vertices; if it fails, build a source-ready alpha/mass/clock bound projection matrix",
            "include": "allowed parent vertex list, gauge kinetic uniqueness, matter spectrum ownership, composition sensitivity placeholders, WEP/R10/clock projection matrix",
            "exclude": "unit-rescaling of dimensionless constants, cancellation between channels, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    mass_rows: list[dict[str, str]],
    clock_rows: list[dict[str, str]],
    provenance_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
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
    theorem_ok = any(row["theorem_id"] == "CST1047_0_descent_or_superselection_criterion" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows) and any(
        row["theorem_id"] == "CST1047_5_verdict" and row["current_status"].startswith("FAIL_CURRENT_CLAIM") for row in theorem_rows
    )
    alpha_ok = any(row["fallback_coefficient"] == "b_alpha" and row["verdict"] == "BLOCKED_RETAIN_B_ALPHA" for row in alpha_rows)
    mass_ok = any(row["fallback_coefficient"] == "b_mA" and row["current_status"] == "BLOCKED_RETAIN_B_MA" for row in mass_rows)
    clock_ok = bool(clock_rows) and all(row["numeric_score_ready"] == "false" for row in clock_rows)
    provenance_ok = no_claim(provenance_rows) and all("MISSING" in row["current_value"] for row in provenance_rows)
    bound_ok = no_claim(bound_rows) and any(row["anchor_id"] == "BL1047_3_R10" for row in bound_rows)
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1048" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1047_SUMMARY", True, "1047 constant-superselection alpha/mass/clock theorem or coefficient provenance validation summary"),
        ("V1047_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1047_2_superselection_theorem_blocked", theorem_ok, "conditional theorem is exact but current claim remains blocked"),
        ("V1047_3_alpha_audit_retain_b_alpha", alpha_ok, "alpha audit retains b_alpha because unique-F2/readout/no-alpha clauses are unsigned"),
        ("V1047_4_mass_audit_retain_b_mA", mass_ok, "mass-ratio audit retains b_mA because matter spectrum is not parent-derived"),
        ("V1047_5_clock_rows_nonclaim", clock_ok, "clock projection rows import sensitivities but remain nonclaim"),
        ("V1047_6_provenance_rows_nonclaim", provenance_ok, "coefficient provenance rows are source-ready but missing theorem-zero or numeric values"),
        ("V1047_7_bound_links_nonclaim", bound_ok, "WEP/R10/clock anchors are linked but nonclaim"),
        ("V1047_8_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS template has runner schema and no claim-valid rows"),
        ("V1047_9_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1047 placeholder rows"),
        ("V1047_10_claim_gates_blocked", gates_ok, "all alpha/mass/clock/R10/WEP claim gates remain blocked"),
        ("V1047_11_next_target_written", next_ok, "next target row is present"),
        ("V1047_12_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1047_13_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
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
        "# 1047 Y5 R10 constant superselection alpha mass clock theorem or coefficient provenance",
        "",
        "**Progress:** the exact theorem shape is now isolated: a dimensionless constant is locally silent only if it is quotient-descended or truly superselected/topological. That proof is clean, but it does not yet apply to the actual alpha/mass/clock constants in the current parent action.",
        "",
        "**Current verdict:** no local-GR/R10/WEP/clock claim. `alpha_EM`, mass ratios, and clock transition constants remain live residual channels because unique EM kinetic normalization, matter spectrum ownership, and readout descent are not parent-signed.",
        "",
        "**Fallback:** source-ready nonclaim provenance rows now exist for `b_alpha`, `b_mu`, `b_mA`, `b_clock_i`, and `qbar_constants_abs`. These rows are ready for either a theorem-zero proof or later numeric coefficient sourcing.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = constant_superselection_rows()
    alpha_rows = alpha_gauge_rows()
    mass_rows = mass_ratio_rows()
    clock_rows = clock_projection_rows()
    provenance_rows = coefficient_provenance_rows()
    bound_rows = bound_link_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1047_0_R10_runner_refusal",
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
        (OUT / "P8_Y5_R10_1047_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv", theorem_rows),
        (OUT / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", alpha_rows),
        (OUT / "P8_Y5_R10_1047_MASS_RATIO_SUPERSELECTION_AUDIT.csv", mass_rows),
        (OUT / "P8_Y5_R10_1047_CLOCK_CONSTANT_PROJECTION_ROWS.csv", clock_rows),
        (OUT / "P8_Y5_R10_1047_COEFFICIENT_PROVENANCE_ROWS.csv", provenance_rows),
        (OUT / "P8_Y5_R10_1047_BOUND_LINKS.csv", bound_rows),
        (OUT / "P8_Y5_R10_1047_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1047_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1047_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1047_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1047_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        theorem_rows,
        alpha_rows,
        mass_rows,
        clock_rows,
        provenance_rows,
        bound_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1047_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("Constant superselection theorem attempt", theorem_rows, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            ("Alpha gauge normalization audit", alpha_rows, ["audit_id", "object", "normal_form", "needed_parent_signature", "verdict", "fallback_coefficient", "valid_for_claim"]),
            ("Mass ratio superselection audit", mass_rows, ["audit_id", "object", "zero_route", "current_status", "missing_for_claim", "fallback_coefficient", "valid_for_claim"]),
            ("Clock constant projection rows", clock_rows, ["projection_id", "clock_pair", "source_delta_K_alpha", "projection_formula", "MTS_missing", "numeric_score_ready", "valid_for_claim"]),
            ("Coefficient provenance rows", provenance_rows, ["row_id", "symbol", "definition", "units", "current_value", "source_paths", "observable_links", "valid_for_claim"]),
            ("Bound links", bound_rows, ["anchor_id", "observable", "bound_source", "bound_value", "link_to_component", "score_status", "valid_for_claim"]),
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
        raise SystemExit(f"1047 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
