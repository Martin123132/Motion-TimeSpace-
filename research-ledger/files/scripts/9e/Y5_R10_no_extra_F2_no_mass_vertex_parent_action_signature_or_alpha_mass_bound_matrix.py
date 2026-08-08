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
DOC = ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1048-R10-alpha-mass-clock-bound-matrix-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1048_ALPHA_MASS_CLOCK_MATRIX_TEMPLATE_NONCLAIM.csv"
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
            "SRC1048_0_1047_next",
            "source-intake/mts_residuals/P8_Y5_R10_1047_NEXT_TARGET.csv",
            "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
            "1047 handoff to no-extra-F2/no-mass-vertex parent signature.",
        ),
        (
            "SRC1048_1_1047_superselection",
            "source-intake/mts_residuals/P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
            "CST1047_5_verdict",
            "Constant superselection theorem attempt and blocker.",
        ),
        (
            "SRC1048_2_1047_alpha",
            "source-intake/mts_residuals/P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv",
            "AGN1047_2_kinetic_normalization",
            "Alpha gauge normalization audit retaining b_alpha.",
        ),
        (
            "SRC1048_3_1047_provenance",
            "source-intake/mts_residuals/P8_Y5_R10_1047_COEFFICIENT_PROVENANCE_ROWS.csv",
            "CP1047_0_b_alpha",
            "1047 coefficient provenance rows.",
        ),
        (
            "SRC1048_4_989_signature",
            "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "ELA989_1_unique_F2",
            "EM-lock signature audit and unique-F2 counterexample.",
        ),
        (
            "SRC1048_5_990_contract",
            "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "PAC990_3_EM_lock",
            "Minimal parent action contract.",
        ),
        (
            "SRC1048_6_988_gate",
            "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "EMLOCK988_4_no_alpha_vertex",
            "EM-lock and no-alpha-vertex gate.",
        ),
        (
            "SRC1048_7_638_zero_route",
            "source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv",
            "ZR638_2_particle_masses",
            "Particle mass zero-route attempt.",
        ),
        (
            "SRC1048_8_clock_sensitivities",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_1_YbE3E2",
            "Clock sensitivity rows for alpha channel.",
        ),
        (
            "SRC1048_9_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "Local WEP/source, clock, PPN, and Gdot anchors.",
        ),
        (
            "SRC1048_10_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1048_11_R10_runner",
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


def parent_vertex_signature_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PVS1048_0_field_domain",
            "signature_clause": "parent action has a declared field domain and allowed local operators before fitting local tests",
            "minimal_form": "S_parent[Phi,Psi]=S_grav[q(Phi)] + S_gauge[A^Q T_Q,q(Phi)] + S_matter[Psi,e_obs(q),omega(e_obs),theta_rep]",
            "would_buy": "prevents changing the theory per arena by adding hidden constant/source vertices",
            "current_status": "CONTRACT_NEEDED_NOT_PARENT_SIGNED",
            "blocks_if_missing": "alpha/mass/clock source terms can be inserted after the fact",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PVS1048_1_no_extra_F2",
            "signature_clause": "no independent gauge kinetic operator or scalar gauge-kinetic function",
            "minimal_form": "Allowed: -C_P/4 int mu_obs <F,F>_P; Forbidden: -1/4 int mu_obs f_X(Xhat) F_Q^2 or lambda_A F_Q^2",
            "would_buy": "b_alpha=0 from fixed parent gauge norm instead of phenomenological alpha fitting",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "blocks_if_missing": "alpha_EM remains a retained b_alpha coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PVS1048_2_no_mass_vertex",
            "signature_clause": "no explicit Xhat-dependent masses, Yukawas, or Higgs/QCD/binding response functions",
            "minimal_form": "Allowed: theta_rep fixed or theta_bar(q); Forbidden: m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat)",
            "would_buy": "b_mA and b_mu can be theorem-zero rather than bounded",
            "current_status": "NOT_DERIVED",
            "blocks_if_missing": "mass ratios and composition sensitivities remain physical channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PVS1048_3_no_clock_readout_vertex",
            "signature_clause": "clock and spectral readout descend from quotient-owned coframe/Hodge/matter constants",
            "minimal_form": "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) with no nu_i(Xhat) readout slot",
            "would_buy": "b_clock_i is inherited from zero upstream coefficients",
            "current_status": "UNSIGNED",
            "blocks_if_missing": "clocks remain a separate local readout residual even if WEP is quiet",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PVS1048_4_no_material_marker_vertex",
            "signature_clause": "source/test material labels are discrete representation data or quotient-owned densities, not smooth Xhat markers",
            "minimal_form": "material_A in Rep(P) and rho_A=rho_bar_A(q,Psi_A); Forbidden: s_A(Xhat), preparation_A(Xhat), kappa_A(Xhat)",
            "would_buy": "prevents composition-dependent qbar leakage from sneaking through source definitions",
            "current_status": "UNSIGNED",
            "blocks_if_missing": "WEP/R10 source-test channels stay retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PVS1048_5_verdict",
            "signature_clause": "parent action forbids all alpha/mass/clock hidden vertices",
            "minimal_form": "PVS1048_0 through PVS1048_4 parent-signed with no EFT/post-readout re-entry",
            "would_buy": "qbar_constants_abs=0 and the local constant sector closes structurally",
            "current_status": "FAIL_CURRENT_CLAIM_BOUND_MATRIX_REQUIRED",
            "blocks_if_missing": "build alpha/mass/clock projection matrix; no local-GR/R10/WEP/clock claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_extra_f2_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "F2T1048_0_unique_norm",
            "claim_piece": "unique Maxwell kinetic normalization",
            "mathematical_form": "S_Q=-(C_P/4) int mu_obs <F_Q T_Q,F_Q T_Q>_P and Lie_v(C_P<T_Q,T_Q>_P)=0",
            "proof_step": "If the charge generator and inner product are parent-owned representation data, the gauge kinetic coefficient has no vertical derivative.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "parent-signed T_Q owner and fixed inner product/norm",
            "if_missing": "b_alpha retains a normalization term",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "F2T1048_1_no_scalar_counterterm",
            "claim_piece": "forbid f_X(Xhat) F_Q^2",
            "mathematical_form": "delta S_forbidden=-(1/4) int mu_obs f_X(Xhat) F_Q^2; require f_X constant or absent",
            "proof_step": "A local scalar gauge-kinetic function is covariant and dimensionless; it is not eliminated by units, so it needs a symmetry/field-domain ban.",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_NOT_FORBIDDEN",
            "missing_for_claim": "operator classification or symmetry that excludes f_X F_Q^2",
            "if_missing": "b_alpha = Lie_v ln(g_EM^-2) can be finite",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "F2T1048_2_no_radiative_reentry",
            "claim_piece": "no EFT/readout re-entry of alpha",
            "mathematical_form": "renormalized alpha_eff(q,Xhat) must also factor through q or be fixed by the same parent owner",
            "proof_step": "Even if the tree-level action is clean, loops or readout normalizations cannot be credited as zero unless covered by the same symmetry.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "renormalization/readout ownership statement",
            "if_missing": "clock and EM spectra rows reopen b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "F2T1048_3_verdict",
            "claim_piece": "no-extra-F2 theorem promotion",
            "mathematical_form": "F2T1048_0 + F2T1048_1 + F2T1048_2 => b_alpha=0",
            "proof_step": "The conditional theorem is clean, but the corpus currently fails the no-counterterm clause.",
            "current_status": "FAIL_CURRENT_CLAIM_RETAIN_B_ALPHA",
            "missing_for_claim": "no f_X F^2 theorem or numeric/source-backed b_alpha bound",
            "if_missing": "alpha/mass/clock bound matrix remains required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_mass_vertex_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "MVT1048_0_fixed_rep_spectrum",
            "claim_piece": "fixed matter representation spectrum",
            "mathematical_form": "theta_mass(Phi)=theta_rep or theta_bar(q(Phi)); Dq[v_X]=0 => Lie_v ln(m_A/m_B)=0",
            "proof_step": "Mass-ratio silence follows if the entire dimensionless matter spectrum is representation/quotient data.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "parent derivation of electron/proton/nuclear mass-ratio data",
            "if_missing": "b_mu and b_mA retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "MVT1048_1_no_yukawa_or_mass_X",
            "claim_piece": "forbid Xhat-dependent masses/Yukawas",
            "mathematical_form": "Forbidden: m_A(Xhat) psi_Abar psi_A, y_A(Xhat) psi_A H psi_B, Lambda_QCD(Xhat), B_A(Xhat)",
            "proof_step": "These vertices are local and covariant; without a parent symmetry, they are legal finite couplings.",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "allowed operator list or symmetry excluding all mass/binding Xhat vertices",
            "if_missing": "composition-dependent WEP/R10 and clock mass channels stay live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "MVT1048_2_binding_response",
            "claim_piece": "forbid hidden binding-response functions",
            "mathematical_form": "B_A(Phi)=Bbar_A(q(Phi),theta_rep) and no B_A(Xhat) material response",
            "proof_step": "Even fixed particle masses are not enough; observable bodies carry EM/nuclear binding fractions.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "composition sensitivity matrix or theorem-zero binding response",
            "if_missing": "b_mA beta_A rows required for WEP/R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "MVT1048_3_verdict",
            "claim_piece": "no-mass-vertex theorem promotion",
            "mathematical_form": "MVT1048_0 + MVT1048_1 + MVT1048_2 => b_mA=b_mu=b_nuc=0",
            "proof_step": "The conditional proof is clear, but the current corpus does not derive the matter spectrum or forbid all Xhat mass vertices.",
            "current_status": "FAIL_CURRENT_CLAIM_RETAIN_MASS_MATRIX",
            "missing_for_claim": "parent matter-spectrum theorem or numeric/source-backed mass/composition coefficients",
            "if_missing": "alpha/mass/clock bound matrix remains required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def vertex_table_rows() -> list[dict[str, str]]:
    return [
        {
            "vertex_id": "VT1048_0_parent_curvature_F2",
            "sector": "EM",
            "operator_or_slot": "<F_Q T_Q,F_Q T_Q>_P",
            "classification": "allowed_if_parent_owned",
            "coefficient": "C_P<T_Q,T_Q>_P",
            "claim_effect": "can support b_alpha=0 only if no extra F2/readout re-entry",
            "current_status": "conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_1_scalar_F2",
            "sector": "EM",
            "operator_or_slot": "f_X(Xhat) F_Q^2 or lambda_A F_Q^2",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_alpha",
            "claim_effect": "finite alpha drift and Coulomb/source pressure",
            "current_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_2_fixed_charge_lattice",
            "sector": "EM/source",
            "operator_or_slot": "n_A in fixed compact charge representation",
            "classification": "allowed_if_parent_owned",
            "coefficient": "n_A",
            "claim_effect": "helps source/current normalization only after T_Q owner signs",
            "current_status": "partial",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_3_mass_X",
            "sector": "matter",
            "operator_or_slot": "m_A(Xhat) psi_bar_A psi_A",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_mA",
            "claim_effect": "composition, clocks, and source mass drift",
            "current_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_4_yukawa_X",
            "sector": "matter",
            "operator_or_slot": "y_A(Xhat) psi_A H psi_B",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_mu;b_mA",
            "claim_effect": "dimensionless mass-ratio drift",
            "current_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_5_binding_X",
            "sector": "composite matter",
            "operator_or_slot": "B_A(Xhat), Lambda_QCD(Xhat), nuclear/EM binding response",
            "classification": "forbidden_required_or_bounded",
            "coefficient": "b_nuc;beta_A",
            "claim_effect": "WEP/R10 composition pressure even if point-particle masses are fixed",
            "current_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "VT1048_6_clock_readout_X",
            "sector": "readout",
            "operator_or_slot": "nu_i(Xhat) or clock frame/readout normalization",
            "classification": "forbidden_required_or_bounded",
            "coefficient": "b_clock_i",
            "claim_effect": "clock/redshift residual independent of WEP silence",
            "current_status": "blocks_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bound_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "matrix_id": "BM1048_0_alpha_clock",
            "arena": "clock_frequency_ratios",
            "observable": "d ln(nu_a/nu_b)",
            "bound_or_sensitivity_source": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "projection_formula": "d ln R_ab = DeltaK_alpha_ab*b_alpha*dXhat + DeltaK_mu_ab*b_mu*dXhat + DeltaK_nuc_ab*b_nuc*dXhat + ...",
            "required_mts_inputs": "b_alpha or theorem-zero; b_mu/b_nuc; tau_clock/local dXhat; clock K_mu/K_nuc sources",
            "current_status": "SOURCE_SENSITIVITY_PARTIAL_MTS_INPUTS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "BM1048_1_clock_redshift",
            "arena": "redshift_LPI_clocks",
            "observable": "alpha_clock_redshift",
            "bound_or_sensitivity_source": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "projection_formula": "alpha_clock_redshift = P_clock[b_clock_i, metric_readout_residual, source potential map]",
            "required_mts_inputs": "clock readout map; local potential/source normalization; b_clock_i or theorem-zero",
            "current_status": "BOUND_ANCHOR_READY_PROJECTION_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "BM1048_2_WEP_alpha_mass",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_AB",
            "bound_or_sensitivity_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "projection_formula": "eta_AB = DeltaQ_alpha_AB*beta_source_alpha*b_alpha*tau_WEP + DeltaQ_mass_AB*b_mA*tau_WEP + DeltaQ_nuc_AB*b_nuc*tau_WEP + ...",
            "required_mts_inputs": "composition charge matrix; source/test beta vectors; tau_WEP; b_alpha/b_mA/b_nuc or theorem-zero",
            "current_status": "BOUND_ANCHOR_READY_COMPOSITION_MATRIX_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "BM1048_3_R10_yukawa",
            "arena": "R10_short_range_fifth_force",
            "observable": "alpha_X(lambda_X)",
            "bound_or_sensitivity_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "projection_formula": "alpha_X(lambda_X) ~ K_X Qbar_source(lambda_X) Qbar_test(lambda_X)/(4*pi*Z_X*G_obs) with Qbar containing alpha/mass/clock terms",
            "required_mts_inputs": "lambda_X; Z_X; K_X; Qbar_source/test; b_alpha/b_mA/b_nuc; promoted bound curve",
            "current_status": "BOUND_REVIEW_CANDIDATE_AND_MTS_COMPONENTS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "BM1048_4_PPN_source",
            "arena": "local_GR_PPN",
            "observable": "gamma,beta,alpha_i,xi,Gdot",
            "bound_or_sensitivity_source": "source-intake/local_bounds/local_bound_claims.csv:R3_gamma through R9_Gdot",
            "projection_formula": "PPN vector receives metric/source/readout residuals plus constant-sector source normalization leakage",
            "required_mts_inputs": "weak-field solution; source Hamiltonian owner; constant leakage theorem-zero or bound vector",
            "current_status": "LOCAL_GR_NOT_SCORE_READY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def arena_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "APR1048_0_no_cancellation_policy",
            "requirement": "alpha, mass, clock, marker, and source residuals must be bounded as an envelope unless a theorem forces cancellation",
            "why": "otherwise a tuned cancellation can fake local silence",
            "status": "ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "APR1048_1_shared_domain",
            "requirement": "same local domain/screen/projection rule must be used for WEP, R10, clocks, and PPN",
            "why": "clock-only or WEP-only screening would be a hidden patch",
            "status": "MISSING_PARENT_RULE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "APR1048_2_dimensionless_guard",
            "requirement": "dimensionless alpha, mass ratios, and clock ratios cannot be removed by unit conventions",
            "why": "unit choices only fix dimensionful coordinates/scales",
            "status": "PASSED_GUARD",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "APR1048_3_source_paths",
            "requirement": "every promoted bound row must cite source paths and contain no MISSING markers",
            "why": "keeps private smoke rows separate from claim rows",
            "status": "ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "alpha_mass_clock_bound_matrix_template",
            "curve_id": "MTS_1048_ALPHA_MASS_CLOCK_MATRIX_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QSOURCE_QTEST_FROM_B_ALPHA_B_MASS_B_CLOCK_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "alpha_X(lambda_X) projects the no-cancellation alpha/mass/clock source-test charge envelope into R10",
            "derivation_status": "template_invalid_no_extra_F2_no_mass_vertex_signature_or_bound_matrix_inputs_missing",
            "formula_reference": "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md::BM1048_3_R10_yukawa",
            "source_file": "MISSING_ALPHA_MASS_CLOCK_BOUND_MATRIX_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; no local-GR/R10/WEP/clock pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject until lambda_X, Z_X, K_X, source/test charges, and promoted bound curve exist.",
        }
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1048_0_parent_signature",
            "object": "no-extra-F2/no-mass-vertex parent action signature",
            "current_status": "FAIL_CURRENT_CLAIM_BOUND_MATRIX_REQUIRED",
            "refusal_status": "blocked",
            "failure_reasons": "PVS1048_1_no_extra_F2;PVS1048_2_no_mass_vertex;PVS1048_3_no_clock_readout_vertex;PVS1048_5_verdict",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1048_1_bound_matrix",
            "object": "alpha/mass/clock bound projection matrix",
            "current_status": "SOURCE_READY_BUT_MTS_INPUTS_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": "lambda_X;Z_X;K_X;Qbar_source/test;composition matrix;tau_clock/tau_WEP;tau_R10",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1048_2_R10_runner",
            "object": "R10 alpha/mass/clock placeholder smoke row",
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
            "gate_id": "CG1048_0_no_extra_F2",
            "claim": "independent f_X F^2 and lambda_A F^2 are forbidden by parent action",
            "gate_pass": "false",
            "reason": "counterterm is still legal in current corpus unless parent symmetry/operator list forbids it",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1048_1_no_mass_vertex",
            "claim": "m_A(Xhat), y_A(Xhat), and binding-response vertices are forbidden",
            "gate_pass": "false",
            "reason": "matter spectrum and binding response ownership are not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1048_2_bound_matrix_score",
            "claim": "alpha/mass/clock bound matrix can score WEP/R10/clock",
            "gate_pass": "false",
            "reason": "source sensitivities and bounds are staged, but MTS-side local projections and coefficients are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1048_3_local_GR",
            "claim": "local-GR/Newton branch is closed by 1048",
            "gate_pass": "false",
            "reason": "constant-sector closure is only one upstream prerequisite; PPN/source Hamiltonian gates remain separate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1048_0_parent_signature",
            "decision": "no-extra-F2/no-mass-vertex route is the correct throat but not signed",
            "because": "the theorem would zero alpha/mass/clock leakage, but current corpus still allows the key countervertices",
            "next_action": "either derive a symmetry/operator-classification ban or use bound matrix as retained residual machinery",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1048_1_alpha_status",
            "decision": "b_alpha remains live",
            "because": "f_X F^2 is covariant and dimensionless, so unit choices cannot remove it",
            "next_action": "target parent gauge symmetry/connection-norm uniqueness or numeric b_alpha projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1048_2_mass_status",
            "decision": "b_mA/b_mu/b_nuc remain live",
            "because": "mass ratios and binding fractions are observable and not supplied by the parent action",
            "next_action": "target matter-spectrum ownership or source composition sensitivity matrix",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1048_3_best_next",
            "decision": "move one level deeper to operator-classification symmetry",
            "because": "we now know exactly which vertices must be absent for the derivation path to win",
            "next_action": "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
            "objective": "try to derive a parent symmetry/operator-classification rule that forbids f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), and clock-readout Xhat vertices; if it fails, assign nonclaim residual-prior slots for the alpha/mass/clock bound matrix",
            "include": "parent field-domain rule, gauge inner-product uniqueness, matter spectrum ownership, radiative/readout re-entry guard, residual coefficient prior placeholders",
            "exclude": "unit-rescaling cheat, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    f2_rows: list[dict[str, str]],
    mass_rows: list[dict[str, str]],
    vertex_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
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
    signature_ok = any(row["clause_id"] == "PVS1048_5_verdict" and row["current_status"].startswith("FAIL_CURRENT_CLAIM") for row in signature_rows)
    f2_ok = any(row["theorem_id"] == "F2T1048_1_no_scalar_counterterm" and row["current_status"].startswith("FAIL_CURRENT") for row in f2_rows)
    mass_ok = any(row["theorem_id"] == "MVT1048_3_verdict" and row["current_status"].startswith("FAIL_CURRENT") for row in mass_rows)
    vertex_ok = {"VT1048_1_scalar_F2", "VT1048_3_mass_X", "VT1048_4_yukawa_X", "VT1048_5_binding_X", "VT1048_6_clock_readout_X"}.issubset({row["vertex_id"] for row in vertex_rows})
    matrix_ok = no_claim(matrix_rows) and {"BM1048_0_alpha_clock", "BM1048_2_WEP_alpha_mass", "BM1048_3_R10_yukawa"}.issubset({row["matrix_id"] for row in matrix_rows})
    arena_ok = any(row["requirement_id"] == "APR1048_2_dimensionless_guard" and row["status"] == "PASSED_GUARD" for row in arena_rows)
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1049" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1048_SUMMARY", True, "1048 no-extra-F2/no-mass-vertex parent signature or bound matrix validation summary"),
        ("V1048_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1048_2_parent_signature_blocked", signature_ok, "parent vertex signature attempt remains blocked"),
        ("V1048_3_no_extra_F2_blocked", f2_ok, "no-extra-F2 theorem fails current corpus because scalar/counterterm F2 is not forbidden"),
        ("V1048_4_no_mass_vertex_blocked", mass_ok, "no-mass-vertex theorem fails current corpus because matter spectrum and binding response are not parent-derived"),
        ("V1048_5_forbidden_vertices_catalogued", vertex_ok, "key alpha/mass/clock hidden vertices are catalogued"),
        ("V1048_6_bound_matrix_nonclaim", matrix_ok, "alpha/mass/clock bound matrix is staged as nonclaim"),
        ("V1048_7_arena_guards_present", arena_ok, "dimensionless guard and arena policies are present"),
        ("V1048_8_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS R10 template has runner schema and no claim-valid rows"),
        ("V1048_9_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1048 placeholder rows"),
        ("V1048_10_claim_gates_blocked", gates_ok, "all no-extra-F2/no-mass/local test claim gates remain blocked"),
        ("V1048_11_next_target_written", next_ok, "next target row is present"),
        ("V1048_12_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1048_13_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
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
        "# 1048 Y5 R10 no-extra-F2 no-mass-vertex parent action signature or alpha mass bound matrix",
        "",
        "**Progress:** the parent-action throat is now explicit. If the parent action signs a unique EM curvature norm, forbids `f_X F^2`, and forbids `m_A(Xhat)`, `y_A(Xhat)`, binding, and clock-readout vertices, then the constant sector can be zeroed by derivation rather than fitted.",
        "",
        "**Current verdict:** the route is mathematically clean but not signed. The scalar gauge-kinetic counterterm and mass/binding vertices are still legal in the current corpus, so `b_alpha`, `b_mA`, `b_mu`, `b_nuc`, and `b_clock_i` remain retained residuals.",
        "",
        "**Fallback:** a nonclaim alpha/mass/clock bound projection matrix is now staged for clocks, WEP, R10, and PPN/source arenas. It is not score-ready until MTS supplies local projections, source/test charges, and coefficient values or theorem-zero certificates.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    signature_rows = parent_vertex_signature_rows()
    f2_rows = no_extra_f2_rows()
    mass_rows = no_mass_vertex_rows()
    vertex_rows = vertex_table_rows()
    matrix_rows = bound_matrix_rows()
    arena_rows = arena_requirement_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1048_0_R10_runner_refusal",
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
        (OUT / "P8_Y5_R10_1048_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", signature_rows),
        (OUT / "P8_Y5_R10_1048_NO_EXTRA_F2_THEOREM_ATTEMPT.csv", f2_rows),
        (OUT / "P8_Y5_R10_1048_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv", mass_rows),
        (OUT / "P8_Y5_R10_1048_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv", vertex_rows),
        (OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", matrix_rows),
        (OUT / "P8_Y5_R10_1048_ARENA_PROJECTION_REQUIREMENTS.csv", arena_rows),
        (OUT / "P8_Y5_R10_1048_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1048_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1048_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1048_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1048_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        signature_rows,
        f2_rows,
        mass_rows,
        vertex_rows,
        matrix_rows,
        arena_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1048_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("Parent vertex signature audit", signature_rows, ["clause_id", "signature_clause", "minimal_form", "would_buy", "current_status", "blocks_if_missing", "valid_for_claim"]),
            ("No-extra-F2 theorem attempt", f2_rows, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            ("No-mass-vertex theorem attempt", mass_rows, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            ("Allowed/forbidden vertex table", vertex_rows, ["vertex_id", "sector", "operator_or_slot", "classification", "coefficient", "claim_effect", "current_status", "valid_for_claim"]),
            ("Alpha/mass/clock bound matrix", matrix_rows, ["matrix_id", "arena", "observable", "bound_or_sensitivity_source", "projection_formula", "required_mts_inputs", "current_status", "claim_allowed", "valid_for_claim"]),
            ("Arena projection requirements", arena_rows, ["requirement_id", "requirement", "why", "status", "valid_for_claim"]),
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
        raise SystemExit(f"1048 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
