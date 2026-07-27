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
DOC = ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1046-R10-no-shadow-marker-constant-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv"
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
            "SRC1046_0_1045_next",
            "source-intake/mts_residuals/P8_Y5_R10_1045_NEXT_TARGET.csv",
            "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "1045 handoff to no-shadow-frame and marker/constant split.",
        ),
        (
            "SRC1046_1_1045_functor",
            "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "MFS1045_4_no_shadow_frame",
            "1045 parent matter functor audit naming the no-shadow-frame gap.",
        ),
        (
            "SRC1046_2_1045_components",
            "source-intake/mts_residuals/P8_Y5_R10_1045_QBAR_COMPONENT_FILL_ROWS.csv",
            "QCF1045_2_qbar_marker_shadow_frame",
            "1045 qbar marker component template.",
        ),
        (
            "SRC1046_3_594_blindness",
            "source-intake/mts_residuals/P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv",
            "MBG594_0_metric_blindness",
            "Matter blindness gates and conformal counterexample.",
        ),
        (
            "SRC1046_4_736_no_marker",
            "source-intake/mts_residuals/P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
            "NMC736_3_shadow_frame_forbidden",
            "No-marker/no-shadow-frame contract.",
        ),
        (
            "SRC1046_5_736_third_zero",
            "source-intake/mts_residuals/P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv",
            "TZA736_3_universal_conformal_marker_loophole",
            "Previous no-marker attempt and universal conformal loophole.",
        ),
        (
            "SRC1046_6_767_reaudit",
            "source-intake/mts_residuals/P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            "PMR767_3_no_alpha_mass_vertex",
            "Matter functor re-audit: alpha/mass vertex hard blocker.",
        ),
        (
            "SRC1046_7_898_signature",
            "source-intake/mts_residuals/P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
            "MDS898_2_no_marker_constants",
            "Matter descent signature for constants and markers.",
        ),
        (
            "SRC1046_8_constant_contract",
            "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "C2_no_direct_constant_vertices",
            "Constant-sector no direct vertex contract.",
        ),
        (
            "SRC1046_9_no_species_contract",
            "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "S3_no_material_marker_extension",
            "No species/source marker extension contract.",
        ),
        (
            "SRC1046_10_977_constant_source",
            "source-intake/mts_residuals/P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "CSC977_2_no_constant_vertices",
            "Constant/source certificate and forbidden vertices.",
        ),
        (
            "SRC1046_11_1028_no_marker",
            "source-intake/mts_residuals/P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv",
            "NM1028_4_no_shadow_frame",
            "Recent no-marker theorem audit.",
        ),
        (
            "SRC1046_12_1028_pack",
            "source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv",
            "FMB1028_6_b_A",
            "Frame/marker bound input pack.",
        ),
        (
            "SRC1046_13_1029_shadow",
            "source-intake/mts_residuals/P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
            "NST1029_6_verdict",
            "No-shadow-frame theorem audit.",
        ),
        (
            "SRC1046_14_636_shadow_gate",
            "source-intake/mts_residuals/P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv",
            "NS636_2_honesty_test",
            "Older no-shadow-frame classification gate.",
        ),
        (
            "SRC1046_15_637_constant_theorem",
            "source-intake/mts_residuals/P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv",
            "CO637_0_descent_criterion",
            "Constant ownership theorem.",
        ),
        (
            "SRC1046_16_638_constant_zero",
            "source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv",
            "ZR638_1_alpha_EM",
            "Constant zero route attempt for alpha/masses/clocks.",
        ),
        (
            "SRC1046_17_646_clock_sensitivity",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_0_AlHg",
            "Source-backed clock alpha sensitivity rows.",
        ),
        (
            "SRC1046_18_646_clock_projection",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv",
            "CPL646_0_pair_ratio",
            "Clock projection ledger.",
        ),
        (
            "SRC1046_19_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "Local WEP/source and clock bound anchors.",
        ),
        (
            "SRC1046_20_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1046_21_R10_runner",
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


def no_shadow_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "NSF1046_0_define_shadow_frame",
            "claim_piece": "shadow frame definition",
            "mathematical_form": "e_A = A_A(Xhat) e_obs or g_A = A_A(Xhat)^2 g_obs + D_A(Xhat) U_mu U_nu + ...",
            "derivation_step": "A shadow frame is any ordinary matter/readout frame not uniquely equal to the quotient-owned observed coframe.",
            "current_status": "DEFINITION_SHARP",
            "missing_for_claim": "none at definition level",
            "if_missing": "cannot name the retained matter-frame coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF1046_1_conditional_chain_rule_zero",
            "claim_piece": "quotient-owned frame derivative",
            "mathematical_form": "A_A(Phi)=Abar_A(q_loc(Phi)) and Dq_loc[v_X]=0 => Lie_v ln A_A = D ln Abar_A[Dq_loc(v_X)] = 0",
            "derivation_step": "The no-shadow coefficient is zero if every matter-frame function factors through the quotient.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "parent-signed quotient kernel and frame-function factorization",
            "if_missing": "c_g/b_conf/b_dis remain finite retained coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF1046_2_no_extra_frame_slot",
            "claim_piece": "action-domain exclusion",
            "mathematical_form": "Allowed[S_A] = S_A[Psi_A,e_obs(q),omega[e_obs],theta_A] and excludes S_A[Psi_A,A_A(Xhat)e_obs,D_A(Xhat),...]",
            "derivation_step": "A no-shadow theorem needs exclusion from the parent action, not only a chosen readout frame.",
            "current_status": "CONTRACT_AVAILABLE_NOT_PARENT_DERIVED",
            "missing_for_claim": "single-public-metric/no-extra-frame parent action clause",
            "if_missing": "universal scalar-tensor-like frame coupling remains legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF1046_3_common_mode_limit",
            "claim_piece": "constant common calibration is not finite coupling",
            "mathematical_form": "A_A=A_0 can be unit/G calibration, but c_A:=Lie_v ln A_A or d_A:=Lie_v D_A is physical when X varies",
            "derivation_step": "WEP-safe common coupling does not imply c_A=0; it can still source R10, clocks, source normalization, and local weak-field rows.",
            "current_status": "PHYSICS_GUARD_RETAINED",
            "missing_for_claim": "arena projections and parent proof that the common mode is constant",
            "if_missing": "do not treat WEP silence as no-shadow-frame proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF1046_4_honesty_test",
            "claim_piece": "observable completeness",
            "mathematical_form": "if a frame/constant/marker changes rods, clocks, masses, charges, free fall, source readout, or spectra, it is either quotient-owned or an explicit residual",
            "derivation_step": "This converts the no-shadow rule into a falsifiable classification gate.",
            "current_status": "USEFUL_GATE_NOT_THEOREM",
            "missing_for_claim": "parent proof that Q_obs is complete",
            "if_missing": "field redefinitions can hide the same coupling in masses, alpha_EM, G_eff, or source normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF1046_5_verdict",
            "claim_piece": "no-shadow-frame theorem",
            "mathematical_form": "NSF1046_1 + NSF1046_2 + NSF1046_4 with parent signatures => c_g=b_conf=b_dis=0 for ordinary matter frame slots",
            "derivation_step": "The theorem shape is exact, but the current corpus has not parent-signed the action-domain exclusion.",
            "current_status": "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED",
            "missing_for_claim": "parent-signed no-extra-frame clause and quotient-owned observable-completeness theorem",
            "if_missing": "fill qbar_marker/qbar_geom coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def constant_marker_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CMA1046_0_alpha_EM",
            "object": "alpha_EM and gauge couplings",
            "zero_route": "topological/representation ownership or quotient-descended gauge kinetic data with Lie_v alpha_EM=0",
            "current_status": "NOT_PARENT_DERIVED_OPEN",
            "why_dangerous": "alpha_EM is dimensionless, so unit rescaling cannot hide d ln alpha_EM/dXhat; clock/EM/WEP rows reopen.",
            "fallback_symbol": "b_alpha",
            "observable_links": "clock;EM spectra;WEP;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CMA1046_1_particle_masses",
            "object": "particle masses, mass ratios, Yukawa/binding data",
            "zero_route": "fixed representation data or quotient-owned mass spectrum with Lie_v m_A=0 for every observable ratio",
            "current_status": "NOT_PARENT_DERIVED_OPEN",
            "why_dangerous": "dimensionful masses can be unit-scaled, but mass ratios and composition-dependent binding fractions are observable.",
            "fallback_symbol": "b_mA; b_mass_ratio; beta_A",
            "observable_links": "WEP;composition;clock;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CMA1046_2_clock_transitions",
            "object": "clock transitions, Rydberg, hyperfine/nuclear ratios",
            "zero_route": "derived from quotient-owned alpha_EM and mass/nuclear ratios",
            "current_status": "INHERITS_ALPHA_AND_MASS_DEBT",
            "why_dangerous": "clock ratios measure dimensionless combinations and can respond even when metric descent is clean.",
            "fallback_symbol": "b_clock_i; tau_clock",
            "observable_links": "R2_clock_redshift; clock comparisons; alpha drift",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CMA1046_3_material_markers",
            "object": "material labels, isotope fractions, preparation data, source/test markers",
            "zero_route": "absent, pure gauge, source-independent auxiliary, discrete representation data, or explicitly retained residual field",
            "current_status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "why_dangerous": "species/source labels can preserve covariance while creating composition-dependent qbar charge.",
            "fallback_symbol": "b_marker; s_A b_A",
            "observable_links": "WEP_source_charge;composition;clock;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CMA1046_4_source_only_weights",
            "object": "relative matter/source prefactors w_A or kappa_A",
            "zero_route": "minimal parent matter action with no source-only slots and one universal/global kappa",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "why_dangerous": "constant species weights can satisfy Ward identities while changing active gravitational source charge.",
            "fallback_symbol": "delta_kappa_A; qbar_source_weight",
            "observable_links": "R1_WEP_source_charge;Newton_GM;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CMA1046_5_verdict",
            "object": "constant/marker split",
            "zero_route": "CMA1046_0 through CMA1046_4 are classified as quotient-owned/superselected or explicit residuals with no hidden branch",
            "current_status": "FAIL_CURRENT_CLAIM_CONSTANT_MARKER_ZERO_NOT_SIGNED",
            "why_dangerous": "qbar_constants and qbar_marker cannot be erased by metric descent alone.",
            "fallback_symbol": "qbar_constants_abs; qbar_marker_abs",
            "observable_links": "WEP;R10;clock;PPN;local_GR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def forbidden_vertex_rows() -> list[dict[str, str]]:
    return [
        {
            "vertex_id": "FV1046_0_conformal_frame",
            "forbidden_vertex": "S_A[Psi_A, exp(2 b_A Xhat) g_obs]",
            "coefficient": "b_conf",
            "why_forbidden_or_retained": "universal conformal coupling is WEP-safe at leading order but still produces trace/fifth-force/source-normalization pressure",
            "current_status": "FORBIDDEN_IF_NO_SHADOW_THEOREM_SIGNED_ELSE_RETAIN",
            "fallback_row": "QMC1046_0_b_conf",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_1_disformal_frame",
            "forbidden_vertex": "S_A[Psi_A, g_obs + b_dis Xhat U_mu U_nu + ...]",
            "coefficient": "b_dis",
            "why_forbidden_or_retained": "disformal matter frame can hit PPN, clocks, preferred-frame, and orbital/source rows",
            "current_status": "FORBIDDEN_IF_NO_SHADOW_THEOREM_SIGNED_ELSE_RETAIN",
            "fallback_row": "QMC1046_1_b_dis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_2_alpha_EM",
            "forbidden_vertex": "alpha_EM(Xhat) F_munu F^munu or gauge kinetic f(Xhat)F^2",
            "coefficient": "b_alpha",
            "why_forbidden_or_retained": "dimensionless EM constant variations are directly observable in clocks/spectra and composition",
            "current_status": "FORBIDDEN_IF_CONSTANT_SUPERSELECTION_SIGNED_ELSE_RETAIN",
            "fallback_row": "QCC1046_0_b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_3_mass_vertex",
            "forbidden_vertex": "m_A(Xhat) psi_bar_A psi_A or Yukawa/binding coefficient y_A(Xhat)",
            "coefficient": "b_mA",
            "why_forbidden_or_retained": "mass ratios and binding fractions feed WEP, clocks, and source charge",
            "current_status": "FORBIDDEN_IF_CONSTANT_SUPERSELECTION_SIGNED_ELSE_RETAIN",
            "fallback_row": "QCC1046_1_b_mA",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_4_clock_vertex",
            "forbidden_vertex": "nu_i(Xhat), Rydberg(Xhat), hyperfine/nuclear ratio Xhat dependence",
            "coefficient": "b_clock_i",
            "why_forbidden_or_retained": "clock ratios can see constant drift even if free-fall metric is clean",
            "current_status": "INHERITED_FROM_ALPHA_AND_MASS_DEBT",
            "fallback_row": "QCC1046_2_b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_5_material_marker",
            "forbidden_vertex": "material_marker_A(Xhat), isotope/preparation/source labels, or post-readout P_active marker",
            "coefficient": "b_marker",
            "why_forbidden_or_retained": "a material marker can be covariant and still composition-dependent",
            "current_status": "FORBIDDEN_IF_NO_MARKER_THEOREM_SIGNED_ELSE_RETAIN",
            "fallback_row": "QMC1046_2_b_marker",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "vertex_id": "FV1046_6_source_only_weight",
            "forbidden_vertex": "S_source = sum_A kappa_A J_A or S_matter = sum_A w_A S_A with relative w_A",
            "coefficient": "delta_kappa_A",
            "why_forbidden_or_retained": "relative source-only weights can preserve matter equations while changing gravitational source",
            "current_status": "FORBIDDEN_IF_MINIMAL_SOURCE_CURRENT_SIGNED_ELSE_RETAIN",
            "fallback_row": "future qbar_source_weight row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_marker_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "QMC1046_0_b_conf",
            "symbol": "b_conf",
            "definition": "vertical derivative of hidden conformal matter/source frame, d ln A_A/dXhat",
            "formula_or_bound": "|qbar_marker| contains |b_conf| times declared matter/source sensitivity and arena projection",
            "required_inputs": "Xhat normalization; species/source scope; b_conf value or theorem-zero source; tau_R10/tau_clock/tau_PPN",
            "current_value": "MISSING_B_CONF_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "R10;WEP;clock;PPN;source_normalization",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QMC1046_1_b_dis",
            "symbol": "b_dis",
            "definition": "vertical derivative of disformal/profile-normalized matter frame slot",
            "formula_or_bound": "|qbar_marker| contains |tau_dis b_dis| plus preferred-frame/orbital projections",
            "required_inputs": "disformal tensor profile; normalization; b_dis value or theorem-zero source; arena projections",
            "current_value": "MISSING_B_DIS_OR_THEOREM_ZERO",
            "units": "model_dependent_declared",
            "observable_links": "PPN;preferred_frame;clock;orbital;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QMC1046_2_b_marker",
            "symbol": "b_marker",
            "definition": "vertical derivative of material/source/preparation marker",
            "formula_or_bound": "|qbar_marker| contains sum_A |s_A b_marker,A|",
            "required_inputs": "marker taxonomy; material pair; sensitivities; b_marker values; source paths",
            "current_value": "MISSING_MARKER_COEFFICIENTS",
            "units": "dimensionless_after_sensitivity_normalization",
            "observable_links": "WEP_source_charge;composition;clock;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QMC1046_3_qbar_marker_abs",
            "symbol": "qbar_marker_abs",
            "definition": "no-cancellation marker envelope",
            "formula_or_bound": "|qbar_marker| <= |b_conf| + |tau_dis b_dis| + sum_A |s_A b_marker,A| + hidden post-readout marker terms",
            "required_inputs": "all marker/frame coefficients theorem-zero or numeric/source-backed with no-cancellation policy",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_or_declared_profile_units",
            "observable_links": "WEP;R10;clock;PPN;R11",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_constants_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "QCC1046_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative d ln alpha_EM/dXhat or equivalent EM/gauge kinetic marker",
            "formula_or_bound": "clock pair response d ln R_ab = Delta K_alpha_ab b_alpha dXhat plus WEP/EM binding sensitivity terms",
            "required_inputs": "b_alpha value or theorem-zero source; Xhat normalization; clock/WEP sensitivities; source paths",
            "current_value": "MISSING_B_ALPHA_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "clock;EM spectra;WEP;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QCC1046_1_b_mA",
            "symbol": "b_mA",
            "definition": "vertical derivative of particle masses, mass ratios, Yukawa/binding constants, or nuclear response",
            "formula_or_bound": "|qbar_constants| contains sum_A |s_mA b_mA| over declared material/clock/source sensitivities",
            "required_inputs": "species/material sensitivities; b_mA values or theorem-zero source; normalization; source paths",
            "current_value": "MISSING_B_MASS_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "WEP;composition;clock;source_charge;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QCC1046_2_b_clock_i",
            "symbol": "b_clock_i",
            "definition": "vertical derivative of a clock transition after alpha/mass/nuclear sensitivities are projected",
            "formula_or_bound": "b_clock_i = K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...",
            "required_inputs": "clock sensitivity matrix; b_alpha/b_mu/b_nuc; local dXhat projection; source paths",
            "current_value": "MISSING_CLOCK_CONSTANT_PROJECTION",
            "units": "dimensionless",
            "observable_links": "R2_clock_redshift; alpha drift; clock comparison",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "QCC1046_3_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "definition": "no-cancellation constant-sector envelope",
            "formula_or_bound": "|qbar_constants| <= |s_alpha b_alpha| + sum_A |s_mA b_mA| + sum_i |s_clock_i b_clock_i| + retained charge/source constants",
            "required_inputs": "all constant coefficients theorem-zero or numeric/source-backed with no-cancellation policy",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_or_declared_clock_units",
            "observable_links": "WEP;clock;R10;EM;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bound_anchor_rows() -> list[dict[str, str]]:
    return [
        {
            "anchor_id": "BA1046_0_WEP_source",
            "observable": "eta_WEP_source_charge",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "bound_value": "2.8e-15",
            "link_to_component": "qbar_marker_abs; qbar_constants_abs; qbar_source_weight",
            "score_status": "ANCHOR_AVAILABLE_COMPONENTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BA1046_1_R10",
            "observable": "alpha_X(lambda_X)",
            "bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "bound_value": "review_candidate_curve_only",
            "link_to_component": "qbar_marker_abs; qbar_constants_abs; qbar_XT",
            "score_status": "BOUND_AND_COMPONENTS_NOT_CLAIM_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BA1046_2_clock_redshift",
            "observable": "alpha_clock_redshift",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "bound_value": "2.48e-05",
            "link_to_component": "b_clock_i; b_alpha; b_mA",
            "score_status": "ANCHOR_AVAILABLE_CLOCK_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BA1046_3_clock_alpha_sensitivity",
            "observable": "clock alpha sensitivity rows",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "bound_value": "source_backed_sensitivities_not_MTS_projection",
            "link_to_component": "b_alpha; b_clock_i",
            "score_status": "SENSITIVITIES_AVAILABLE_MTS_DX_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbar_marker_shadow_frame_template",
            "curve_id": "MTS_1046_QBAR_MARKER_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_QBAR_MARKER_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "alpha_X(lambda_X) contains K_X Qbar_XH(lambda_X) qbar_marker_abs/(4*pi*Z_X*G_obs) unless no-shadow/no-marker theorem is signed",
            "derivation_status": "template_invalid_no_shadow_theorem_or_marker_coefficients_missing",
            "formula_reference": "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md::QMC1046_3",
            "source_file": "MISSING_QBAR_MARKER_SOURCE_FILE",
            "assumptions": "private nonclaim marker fallback; no cancellation; no local-GR pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject this row until marker/frame coefficients or theorem-zero certificates are real.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbar_constants_template",
            "curve_id": "MTS_1046_QBAR_CONSTANTS_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_QBAR_CONSTANTS_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge; source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift",
            "force_law_form": "qbar_constants_abs projects to WEP/R10/clock rows through declared material and clock sensitivities",
            "derivation_status": "template_invalid_constant_superselection_or_coefficients_missing",
            "formula_reference": "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md::QCC1046_3",
            "source_file": "MISSING_QBAR_CONSTANTS_SOURCE_FILE",
            "assumptions": "private nonclaim constants fallback",
            "valid_for_claim": "false",
            "notes": "No source-backed constant coefficients are present.",
        },
    ]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1046_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(
    theorem_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    marker_rows: list[dict[str, str]],
    constant_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1046_0_no_shadow",
            "object": "no-shadow-frame theorem",
            "current_status": "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(row["theorem_id"] for row in theorem_rows if row["current_status"] in {"CONTRACT_AVAILABLE_NOT_PARENT_DERIVED", "USEFUL_GATE_NOT_THEOREM", "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED"}),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1046_1_constants_markers",
            "object": "constant/marker zero theorem",
            "current_status": "FAIL_CURRENT_CLAIM_CONSTANT_MARKER_ZERO_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(row["audit_id"] for row in audit_rows if row["current_status"] != "WRITTEN_DEFINITION"),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1046_2_coefficients",
            "object": "qbar_marker/qbar_constants coefficients",
            "current_status": "COMPONENT_VALUES_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(row["row_id"] for row in [*marker_rows, *constant_rows] if row["score_ready"] == "false"),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1046_3_R10_runner",
            "object": "R10 marker/constant placeholder smoke rows",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": "valid_mts_rows=" + smoke_rows[0]["valid_mts_rows"],
            "score_eligible": "false",
            "claim_allowed": smoke_rows[0]["claim_allowed"],
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1046_0_no_shadow_frame",
            "claim": "hidden conformal/disformal matter frame is absent by theorem",
            "gate_pass": "false",
            "reason": "no-extra-frame parent action clause and observable-completeness theorem are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1046_1_constant_superselection",
            "claim": "alpha_EM/mass/clock constants are vertical-silent",
            "gate_pass": "false",
            "reason": "constant ownership is a conditional route; alpha_EM, masses, and clock ratios remain unproved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1046_2_material_marker",
            "claim": "material/source/preparation markers are absent or gauge",
            "gate_pass": "false",
            "reason": "no-marker theorem is not parent-signed and marker coefficients are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1046_3_qbar_coefficients",
            "claim": "qbar_marker/qbar_constants are source-backed bounded",
            "gate_pass": "false",
            "reason": "all coefficient rows contain MISSING markers and no source-backed values",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1046_4_R10_WEP_clock_score",
            "claim": "R10/WEP/clock rows can be scored from 1046",
            "gate_pass": "false",
            "reason": "anchors exist but MTS projections and coefficient values are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1046_0_theorem_shape",
            "decision": "no-shadow theorem shape is exact",
            "because": "if every matter-frame function factors through q_loc and v_X is vertical, all frame derivatives vanish by chain rule",
            "next_action": "do not claim; seek parent no-extra-frame action clause or source coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1046_1_current_status",
            "decision": "no-shadow/constant-marker zero is not parent-signed",
            "because": "universal conformal/disformal slots, alpha_EM(X), m_A(X), clock responses, and material markers are legal countermodels unless excluded by parent action",
            "next_action": "retain qbar_marker/qbar_constants envelopes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1046_2_fallback",
            "decision": "marker and constant coefficient rows filled as nonclaim",
            "because": "WEP/R10/clock anchors exist but MTS-side coefficients and local projections are missing",
            "next_action": "prioritize alpha_EM/mass/clock coefficient provenance or parent constant superselection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1046_3_best_next",
            "decision": "target constant superselection and alpha/mass/clock source provenance",
            "because": "the no-shadow frame is structurally handled; the next sharp channel is dimensionless constants and clock/mass sensitivities",
            "next_action": "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
            "objective": "try to prove alpha_EM, mass ratios, and clock transition constants are quotient-owned/superselected and vertically silent; if this fails, build source-ready nonclaim coefficient provenance rows for b_alpha, b_mA, and b_clock_i",
            "include": "constant ownership theorem, alpha_EM gauge kinetic normalization, particle mass ratios, clock sensitivity rows, WEP/R10/clock bounds, units and source paths",
            "exclude": "unit-rescaling cheat for dimensionless constants, closure axiom, post-readout EFT proof credit, cancellation with frame/source rows, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    vertex_rows: list[dict[str, str]],
    marker_rows: list[dict[str, str]],
    constant_rows: list[dict[str, str]],
    anchor_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1046_1_sources_exist_and_needles",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "every cited source path exists and every source needle was found",
        )
    )
    checks.append(
        (
            "V1046_2_no_shadow_theorem_blocked",
            any(row["theorem_id"] == "NSF1046_1_conditional_chain_rule_zero" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows)
            and any(row["theorem_id"] == "NSF1046_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED" for row in theorem_rows)
            and all(not flag(row["valid_for_claim"]) for row in theorem_rows),
            "no-shadow theorem shape is exact but current claim remains blocked",
        )
    )
    checks.append(
        (
            "V1046_3_constant_marker_audit_blocked",
            any(row["audit_id"] == "CMA1046_0_alpha_EM" for row in audit_rows)
            and any(row["audit_id"] == "CMA1046_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_CONSTANT_MARKER_ZERO_NOT_SIGNED" for row in audit_rows)
            and all(not flag(row["valid_for_claim"]) for row in audit_rows),
            "constant/marker split audit covers alpha, masses, clocks, markers, source weights and remains blocked",
        )
    )
    checks.append(
        (
            "V1046_4_forbidden_vertices_catalogued",
            {"b_conf", "b_dis", "b_alpha", "b_mA", "b_clock_i", "b_marker", "delta_kappa_A"}.issubset({row["coefficient"] for row in vertex_rows})
            and all(not flag(row["valid_for_claim"]) for row in vertex_rows),
            "forbidden vertex catalog covers the main shadow/constant/marker routes",
        )
    )
    checks.append(
        (
            "V1046_5_marker_coefficients_nonclaim",
            any(row["row_id"] == "QMC1046_3_qbar_marker_abs" and row["current_value"] == "MISSING_COMPONENT_VALUES" for row in marker_rows)
            and all("MISSING" in row["current_value"] and row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in marker_rows),
            "qbar_marker rows are filled as missing-value nonclaim templates",
        )
    )
    checks.append(
        (
            "V1046_6_constant_coefficients_nonclaim",
            any(row["row_id"] == "QCC1046_3_qbar_constants_abs" and row["current_value"] == "MISSING_COMPONENT_VALUES" for row in constant_rows)
            and all("MISSING" in row["current_value"] and row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in constant_rows),
            "qbar_constants rows are filled as missing-value nonclaim templates",
        )
    )
    checks.append(
        (
            "V1046_7_bound_anchors_nonclaim",
            any(row["anchor_id"] == "BA1046_0_WEP_source" and row["bound_value"] == "2.8e-15" for row in anchor_rows)
            and any(row["anchor_id"] == "BA1046_1_R10" for row in anchor_rows)
            and any(row["anchor_id"] == "BA1046_2_clock_redshift" and row["bound_value"] == "2.48e-05" for row in anchor_rows)
            and all(not flag(row["valid_for_claim"]) for row in anchor_rows),
            "WEP/R10/clock anchors are linked but nonclaim",
        )
    )
    checks.append(
        (
            "V1046_8_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1046_9_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1046 placeholder rows",
        )
    )
    checks.append(
        (
            "V1046_10_claim_gates_blocked",
            all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all no-shadow/constant/marker/R10/WEP/clock claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1046_11_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1046_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv",
        OUT / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
        OUT / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv",
        OUT / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv",
        OUT / "P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
        OUT / "P8_Y5_R10_1046_BOUND_ANCHOR_LINKS.csv",
        OUT / "P8_Y5_R10_1046_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1046_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1046_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1046_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1046_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1046_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1046_12_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files if path.exists() or path.parent.exists()),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1046_13_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1046_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1046 no-shadow-frame constant marker theorem or coefficient validation summary",
            "generated_utc": stamp(),
        }
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    return rows


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    vertex_rows: list[dict[str, str]],
    marker_rows: list[dict[str, str]],
    constant_rows: list[dict[str, str]],
    anchor_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1046 Y5 R10 no-shadow-frame constant marker theorem or qbar marker coefficients",
        "",
        "**Progress:** the no-shadow theorem is now exact as a conditional statement. If every matter-frame/constant/marker function factors through `q_loc` and `v_X in ker(Dq_loc)`, the vertical derivative vanishes by chain rule.",
        "",
        "**Current verdict:** this is not yet a parent-signed MTS theorem. Universal conformal/disformal frames, `alpha_EM(X)`, `m_A(X)`, clock-ratio sensitivity, material markers, and source-only weights remain legal countermodels unless excluded by the parent action.",
        "",
        "**Fallback:** `qbar_marker` and `qbar_constants` coefficient rows are filled as nonclaim templates. WEP/R10/clock anchors are linked, but no MTS coefficient is source-backed.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## No-shadow-frame theorem attempt",
        md_table(theorem_rows, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
        "## Constant marker split audit",
        md_table(audit_rows, ["audit_id", "object", "zero_route", "current_status", "why_dangerous", "fallback_symbol", "observable_links", "valid_for_claim"]),
        "## Forbidden vertex catalog",
        md_table(vertex_rows, ["vertex_id", "forbidden_vertex", "coefficient", "why_forbidden_or_retained", "current_status", "fallback_row", "valid_for_claim"]),
        "## qbar marker coefficient rows",
        md_table(marker_rows, ["row_id", "symbol", "definition", "formula_or_bound", "required_inputs", "current_value", "observable_links", "score_ready", "valid_for_claim"]),
        "## qbar constants coefficient rows",
        md_table(constant_rows, ["row_id", "symbol", "definition", "formula_or_bound", "required_inputs", "current_value", "observable_links", "score_ready", "valid_for_claim"]),
        "## Bound anchor links",
        md_table(anchor_rows, ["anchor_id", "observable", "bound_source", "bound_value", "link_to_component", "score_status", "valid_for_claim"]),
        "## MTS R10 smoke template",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
        "## Next target",
        md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    theorem_rows = no_shadow_theorem_rows()
    audit_rows = constant_marker_audit_rows()
    vertex_rows = forbidden_vertex_rows()
    marker_rows = qbar_marker_rows()
    constant_rows = qbar_constants_rows()
    anchor_rows = bound_anchor_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(theorem_rows, audit_rows, marker_rows, constant_rows, smoke_rows)
    claim_rows_ = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        theorem_rows,
        audit_rows,
        vertex_rows,
        marker_rows,
        constant_rows,
        anchor_rows,
        mts_rows,
        smoke_rows,
        claim_rows_,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1046_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv", audit_rows)
    write_csv(OUT / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv", vertex_rows)
    write_csv(OUT / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv", marker_rows)
    write_csv(OUT / "P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv", constant_rows)
    write_csv(OUT / "P8_Y5_R10_1046_BOUND_ANCHOR_LINKS.csv", anchor_rows)
    write_csv(OUT / "P8_Y5_R10_1046_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1046_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1046_CLAIM_GATES.csv", claim_rows_)
    write_csv(OUT / "P8_Y5_R10_1046_DECISION_LEDGER.csv", decision_rows_)
    write_csv(OUT / "P8_Y5_R10_1046_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1046_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        theorem_rows,
        audit_rows,
        vertex_rows,
        marker_rows,
        constant_rows,
        anchor_rows,
        mts_rows,
        smoke_rows,
        refusal_rows,
        claim_rows_,
        decision_rows_,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1046 validation failed: {failed}")


if __name__ == "__main__":
    main()
