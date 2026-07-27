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
DOC = ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1044-R10-matter-pullback-qbarXT-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1044_QBARXT_TEMPLATE_NONCLAIM.csv"
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
            "SRC1044_0_1043_next",
            "source-intake/mts_residuals/P8_Y5_R10_1043_NEXT_TARGET.csv",
            "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
            "1043 handoff to matter pullback or qbarXT bound row.",
        ),
        (
            "SRC1044_1_1043_matter_channel",
            "source-intake/mts_residuals/P8_Y5_R10_1043_JX_ZERO_CHANNEL_AUDIT.csv",
            "JX1043_0_matter_pullback",
            "Prior J_X audit identifying ordinary matter as the next clean channel.",
        ),
        (
            "SRC1044_2_pullback_charge_map",
            "source-intake/mts_residuals/P8_Y5_R10_564_MATTER_PULLBACK_CHARGE_MAP.csv",
            "MP564_0_particle_action",
            "Existing expression for point-particle and continuum X charge.",
        ),
        (
            "SRC1044_3_matter_blindness_gate",
            "source-intake/mts_residuals/P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv",
            "MBG594_0_metric_blindness",
            "Matter blindness gate and counterexamples.",
        ),
        (
            "SRC1044_4_parent_matter_contract",
            "source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
            "PMC622_8_contract_verdict",
            "Parent matter contract verdict.",
        ),
        (
            "SRC1044_5_matter_coupling_derivation",
            "source-intake/mts_residuals/P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
            "MCD716_6_current_corpus_verdict",
            "Matter coupling derivation and retained coefficients.",
        ),
        (
            "SRC1044_6_no_marker_contract",
            "source-intake/mts_residuals/P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
            "NMC736_5_limit",
            "No-marker contract limit.",
        ),
        (
            "SRC1044_7_vertical_action_contract",
            "source-intake/mts_residuals/P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
            "MVA761_5_evaluability_verdict",
            "Vertical matter action evaluability gate.",
        ),
        (
            "SRC1044_8_functor_reaudit",
            "source-intake/mts_residuals/P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            "PMR767_5_domain_selection_predata",
            "Parent matter functor re-audit with still-unsigned clauses.",
        ),
        (
            "SRC1044_9_descent_signature",
            "source-intake/mts_residuals/P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
            "MDS898_5_verdict",
            "Matter descent signature and verdict.",
        ),
        (
            "SRC1044_10_force_silence",
            "source-intake/mts_residuals/P8_Y5_R10_918_MATTER_FORCE_SILENCE_AUDIT.csv",
            "F918_1_species_charge",
            "Matter force silence audit.",
        ),
        (
            "SRC1044_11_minimal_matter_lemma",
            "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "MMA955_6_verdict",
            "Minimal matter action source-coupling lemma.",
        ),
        (
            "SRC1044_12_constant_source_certificate",
            "source-intake/mts_residuals/P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "CSC977_7_verdict",
            "Constant/source universality certificate.",
        ),
        (
            "SRC1044_13_bounded_qbar_schema",
            "source-intake/mts_residuals/P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
            "BQT1027_3_total_abs_guard",
            "Bounded qbarXT component schema.",
        ),
        (
            "SRC1044_14_qbar_residual_template",
            "source-intake/mts_residuals/P8_Y5_R10_619_QBARXT_RESIDUAL_FILL_TEMPLATE.csv",
            "QXT619_6_total",
            "Older qbarXT residual fill template.",
        ),
        (
            "SRC1044_15_no_species_contract",
            "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "S1_matter_factorization",
            "No species/source charge contract.",
        ),
        (
            "SRC1044_16_constant_sector_contract",
            "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "C7_empirical_fallback",
            "Constant-sector universality and fallback policy.",
        ),
        (
            "SRC1044_17_min_parent_blocks",
            "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "A511_2_universal_matter",
            "Minimal parent local-GR universal matter block.",
        ),
        (
            "SRC1044_18_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "WEP/source-charge local bound anchor.",
        ),
        (
            "SRC1044_19_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve used only for smoke validation.",
        ),
        (
            "SRC1044_20_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 alpha(lambda) runner.",
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


def matter_pullback_derivation_rows() -> list[dict[str, str]]:
    return [
        {
            "derivation_id": "MPD1044_0_target",
            "claim_piece": "ordinary test-body X charge",
            "formula": "qbar_XT := M_T^-1 delta_{v_X} S_T",
            "derivation_result": "TARGET_RESTATED",
            "proof_status": "not_a_claim",
            "gap": "requires parent-owned vertical action on matter and matter functor descent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_1_chain_rule_identity",
            "claim_piece": "chain-rule variation",
            "formula": "delta_v S_T = 1/2 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge/E_Psi terms",
            "derivation_result": "DERIVED_STANDARD_ON_SHELL_IDENTITY",
            "proof_status": "conditional_math_ok",
            "gap": "only becomes zero if geometry, constants, matter lift, and boundary terms descend",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_2_geometry_pullback_zero",
            "claim_piece": "observed geometry X-blindness",
            "formula": "if ghat = ghat(q_loc(Phi)) and Dq_loc[v_X]=0, then Lie_v ghat_munu = 0 up to owned gauge",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "parent_functor_unsigned",
            "gap": "unique observed coframe/metric functor not parent-derived in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_3_constants_zero",
            "claim_piece": "matter constants X-blindness",
            "formula": "Lie_v theta_a = 0 for masses, charges, alpha_EM, clocks, representation labels, and material standards",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "constant_superselection_unsigned",
            "gap": "fixed representation data route exists but no parent theorem excludes theta_a(X), theta_a(I_Q), or material-marker dependence",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_4_matter_lift",
            "claim_piece": "ordinary matter vertical lift",
            "formula": "delta_v Psi_T = 0 or delta_v Psi_T is an owned gauge/Lorentz/diffeomorphism lift with delta_v S_T boundary-only",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "matter_category_unsigned",
            "gap": "parent action has not constructed the ordinary matter bundle/category as the only allowed matter domain",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_5_boundary_support",
            "claim_piece": "matter boundary silence",
            "formula": "boundary/gauge terms vanish for compact-support matter variations or are owned exact/topological terms with zero local projection",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "boundary_support_unsigned",
            "gap": "source worldtube and edge-current behaviour remain separate active residuals",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_6_source_current_universality",
            "claim_piece": "source-current equality",
            "formula": "same S_matter gives E_Psi=delta S/delta Psi and T_munu=2/sqrt(-g) delta S/delta g_obs^{munu}; one global kappa multiplies sum_A T_A",
            "derivation_result": "RELATIVE_CERTIFICATE_READY",
            "proof_status": "parent_schema_unsigned",
            "gap": "relative species prefactors, non-Hilbert currents, and measured-GM calibration are not removed by Ward symmetry alone",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_7_exact_theorem_if_signed",
            "claim_piece": "conditional matter-pullback theorem",
            "formula": "MPD1044_2 and MPD1044_3 and MPD1044_4 and MPD1044_5 imply delta_v S_T=0, hence qbar_XT=0 and J_matter=0 for ordinary matter",
            "derivation_result": "EXACT_CONDITIONAL_THEOREM",
            "proof_status": "not_parent_signed",
            "gap": "this is a strong future parent-action contract, not a current MTS proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "MPD1044_8_current_verdict",
            "claim_piece": "current MTS matter-pullback zero",
            "formula": "qbar_XT=0 and J_matter=0 cannot be promoted until the parent matter functor and no-marker/source-current clauses are signed",
            "derivation_result": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
            "proof_status": "residual_required",
            "gap": "build nonclaim qbarXT component envelope and keep WEP/R10/clock links active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def premise_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "MPG1044_0_parent_matter_functor",
            "premise": "S_matter = sum_A S_A[Psi_A, e_obs(q_loc(Phi)), omega[e_obs], theta_A]",
            "needed_for": "geometry and matter-domain pullback",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "qbar_geom and frame/source residuals remain active",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_1_vertical_kernel",
            "premise": "v_X in ker(Dq_loc) with owned fixed/gauge lift on Psi_A",
            "needed_for": "Lie_v e_obs=0 and no physical matter transformation",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "representative motion may be a physical fifth-force/source charge",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_2_constant_superselection",
            "premise": "Lie_v theta_A=0 for masses, charges, alpha_EM, clocks, and representation labels",
            "needed_for": "no constant/clock/material qbar channel",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "qbar_marker and clock/fine-structure rows remain active",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_3_no_marker_extension",
            "premise": "no direct material marker, hidden conformal/disformal frame, source-only coefficient, or post-readout EFT counterterm",
            "needed_for": "no hidden fifth-force loophole",
            "current_status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "if_missing": "relative species/source charges survive even when Ward identities hold",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_4_boundary_support_silence",
            "premise": "matter edge/worldtube boundary terms vanish or are separately retained with source-backed bounds",
            "needed_for": "chain-rule boundary term cannot hide qbarXT",
            "current_status": "OPEN",
            "if_missing": "qbar_nonH and boundary/source support residuals remain active",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_5_universal_source_current",
            "premise": "one Hilbert/coframe matter source and one global/superselected kappa, with no source-only species weights",
            "needed_for": "source-charge WEP and measured-source consistency",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "if_missing": "R1 WEP source-charge and measured-GM residual rows stay live",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "MPG1044_6_verdict",
            "premise": "all matter-pullback gates pass simultaneously",
            "needed_for": "J_matter=0 and qbar_XT=0 claim",
            "current_status": "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED",
            "if_missing": "qbarXT bound fallback is mandatory",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_component_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "QBC1044_0_qbar_geom",
            "symbol": "qbar_geom",
            "definition": "ordinary test-body X charge from observed metric/coframe leakage",
            "formula_or_bound": "qbar_geom = (2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu",
            "required_input": "Lie_v ghat_munu or theorem-zero geometry descent certificate",
            "current_value": "MISSING_LIE_V_GHAT",
            "units": "dimensionless_after_normalization",
            "observable_links": "R10;PPN;clock;WEP_direct_geometry",
            "status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QBC1044_1_qbar_constants",
            "symbol": "qbar_constants",
            "definition": "ordinary test-body X charge from masses, charges, alpha_EM, clock, or representation constants",
            "formula_or_bound": "qbar_constants = M_T^-1 sum_a int J_theta^a Lie_v theta_a",
            "required_input": "constant-superselection theorem or dtheta_a/dX coefficients with source paths",
            "current_value": "MISSING_DTHETA_DX",
            "units": "dimensionless_after_sensitivity_normalization",
            "observable_links": "WEP;clock;fine_structure;R10",
            "status": "MISSING_NO_MARKER_CONSTANT_THEOREM_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QBC1044_2_qbar_marker",
            "symbol": "qbar_marker",
            "definition": "source/test charge from material markers, hidden frames, direct MTS vertices, or post-readout masks",
            "formula_or_bound": "|qbar_marker| <= sum |s_marker b_marker| over declared material/marker channels",
            "required_input": "no-marker theorem or marker sensitivities and coefficients",
            "current_value": "MISSING_MARKER_COEFFICIENTS",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;clock;R11;R10",
            "status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QBC1044_3_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "relative species or class source-only weight in the active gravitational source",
            "formula_or_bound": "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| plus measured-GM calibration tail",
            "required_input": "minimal matter action source-current theorem or source-weight split values",
            "current_value": "MISSING_DELTA_KAPPA_A",
            "units": "dimensionless",
            "observable_links": "R1_WEP_source_charge;Newton_GM;R10",
            "status": "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QBC1044_4_qbar_nonH",
            "symbol": "qbar_nonH",
            "definition": "non-Hilbert, boundary, connection, domain, or support-shift contribution to test/source charge",
            "formula_or_bound": "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
            "required_input": "hidden-source zero theorem or component numeric bounds",
            "current_value": "MISSING_NONHILBERT_BOUND",
            "units": "dimensionless",
            "observable_links": "R10;orbital;source_normalization;local_GR",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QBC1044_5_total_abs_guard",
            "symbol": "qbar_XT_bound_abs",
            "definition": "no-cancellation envelope for ordinary test-body X charge",
            "formula_or_bound": "|qbar_XT| <= |qbar_geom| + |qbar_constants| + |qbar_marker| + |qbar_source_weight| + |qbar_nonH|",
            "required_input": "all components theorem-zero or source-backed numeric bounds",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless",
            "observable_links": "R10;WEP;clock;PPN;local_GR",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_bound_fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "QBF1044_0_WEP_source_proxy",
            "observable": "eta_WEP_source_charge",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "bound_value": "2.8e-15",
            "units": "dimensionless",
            "mts_quantity": "eta_source_AB approximately 2|qbar_XA-qbar_XB|/|qbar_XA+qbar_XB+2| in weak source-charge limit",
            "required_inputs": "material-pair qbar components, sensitivities, source paths, and same-frame normalization",
            "current_status": "BOUND_ANCHOR_AVAILABLE_MTS_INPUTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "QBF1044_1_R10_fifth_force",
            "observable": "alpha_X(lambda_X)",
            "bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "bound_value": "review_candidate_curve_only",
            "units": "dimensionless_alpha_vs_lambda",
            "mts_quantity": "alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT/(4 pi Z_X G_obs) or declared equivalent normalization",
            "required_inputs": "K_X, Qbar_XH(lambda), qbar_XT, Z_X, lambda_X, source paths, promoted bound curve",
            "current_status": "BOUND_AND_MTS_INPUTS_NOT_CLAIM_READY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "QBF1044_2_clock_constant",
            "observable": "clock/fine-structure response",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift plus future alpha_EM rows",
            "bound_value": "requires observable-specific source",
            "units": "dimensionless_or_rate",
            "mts_quantity": "qbar_constants projected onto clock/alpha_EM sensitivities",
            "required_inputs": "clock sensitivities, dtheta/dX coefficients, units, source paths",
            "current_status": "TEMPLATE_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "QBF1044_3_total_no_cancellation",
            "observable": "qbar_XT total",
            "bound_source": "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "bound_value": "sum_abs_components",
            "units": "dimensionless",
            "mts_quantity": "|qbar_XT| <= sum component absolute values",
            "required_inputs": "component values or theorem-zero certificates for every component",
            "current_status": "NO_CANCELLATION_GUARD_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbarXT_symbolic_component_template",
            "curve_id": "MTS_1044_QBARXT_R10_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_QBAR_XT_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT/(4*pi*Z_X*G_obs)",
            "derivation_status": "template_invalid_qbarXT_and_parent_coefficients_missing",
            "formula_reference": "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md::QBF1044_1",
            "source_file": "MISSING_QBARXT_COMPONENT_SOURCE_FILE",
            "assumptions": "private nonclaim qbarXT fallback; no cancellation; no local-GR pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject this row until qbarXT components and R10 curve are claim-ready.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbarXT_zero_theorem_candidate",
            "curve_id": "MTS_1044_QBARXT_ZERO_CANDIDATE",
            "lambda_value": "MISSING_NOT_RANGE_SCORABLE",
            "lambda_units": "m",
            "alpha_predicted": "0_IF_MPD1044_7_PARENT_SIGNED",
            "alpha_bound": "not_applicable_until_theorem_signed",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv::MPD1044_7_exact_theorem_if_signed",
            "force_law_form": "if qbar_XT=0 by signed parent theorem, ordinary test-body matter charge vanishes in this channel",
            "derivation_status": "theorem_candidate_parent_unsigned",
            "formula_reference": "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md::MPD1044_7",
            "source_file": "MISSING_PARENT_MATTER_FUNCTOR_SIGNATURE",
            "assumptions": "not a claim; records theorem route only",
            "valid_for_claim": "false",
            "notes": "Zero route is exact only after all matter-pullback gates pass.",
        },
    ]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1044_0_R10_runner_refusal",
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
    derivation_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    premise_blockers = [row["gate_id"] for row in premise_rows if row["gate_pass"] == "false"]
    qbar_blockers = [row["component_id"] for row in qbar_rows if "MISSING" in row["current_value"]]
    return [
        {
            "refusal_id": "REF1044_0_qbar_zero",
            "object": "qbar_XT=0",
            "current_status": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(premise_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1044_1_Jmatter_zero",
            "object": "J_matter=0",
            "current_status": derivation_rows[-1]["derivation_result"],
            "refusal_status": "blocked",
            "failure_reasons": "parent matter functor and no-marker/source-current clauses unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1044_2_qbar_bound_values",
            "object": "qbar_XT_bound_abs",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(qbar_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1044_3_R10_runner",
            "object": "R10 qbarXT placeholder smoke rows",
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
            "gate_id": "CG1044_0_Jmatter_zero",
            "claim": "ordinary matter channel gives J_matter=0",
            "gate_pass": "false",
            "reason": "matter functor descent, constant superselection, matter lift, and boundary support clauses are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1044_1_qbarXT_zero",
            "claim": "ordinary test-body qbar_XT=0",
            "gate_pass": "false",
            "reason": "conditional chain-rule theorem exists but parent has not signed all no-marker/source-current clauses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1044_2_qbarXT_bound",
            "claim": "qbar_XT has a source-backed absolute bound",
            "gate_pass": "false",
            "reason": "component values are missing and only templates are filled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1044_3_R10_claim",
            "claim": "R10 fifth-force branch passes",
            "gate_pass": "false",
            "reason": "MTS alpha row is symbolic and review-candidate R10 curve is nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1044_4_local_GR_reduction",
            "claim": "matter-pullback closes local-GR source side",
            "gate_pass": "false",
            "reason": "source normalization, boundary, domain, and positive-X RHS gates remain open beyond ordinary matter pullback",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1044_0_derivation",
            "decision": "exact conditional matter-pullback theorem written",
            "because": "chain rule proves qbar_XT=0 if matter action descends through X-blind observed geometry, X-blind constants, owned matter lift, and silent boundary terms",
            "next_action": "try to sign parent matter functor/observed coframe descent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1044_1_current_status",
            "decision": "zero claim fails in current corpus",
            "because": "existing audits keep parent matter functor, no-marker constants, and source-current universality conditional or unsigned",
            "next_action": "carry qbarXT component envelope",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1044_2_fallback",
            "decision": "qbarXT bound row staged as nonclaim",
            "because": "R1/R10 bound anchors exist but MTS-side qbar components and source paths are missing",
            "next_action": "fill components only from theorem-zero certificates or sourced coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1044_3_best_next",
            "decision": "target parent matter functor descent signature",
            "because": "this is the narrowest upstream clause that would kill qbar_geom and make the remaining constants/no-marker debt explicit",
            "next_action": "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            "objective": "try to sign the parent ordinary-matter functor S_A[Psi_A,e_obs(q_loc(Phi)),theta_A] and vertical lift so qbar_geom=0; if this fails, fill nonclaim qbar_geom/qbar_marker component rows",
            "include": "observed coframe functor, v_X in ker(Dq_loc), fixed/gauge matter lift, no hidden conformal/disformal frame, constants/marker split, source paths",
            "exclude": "closure axiom, post-readout EFT proof credit, source-current cancellation, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1044_1_sources_exist_and_needles",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "every cited source path exists and every source needle was found",
        )
    )
    checks.append(
        (
            "V1044_2_chain_rule_and_verdict",
            any(row["derivation_id"] == "MPD1044_1_chain_rule_identity" and row["derivation_result"] == "DERIVED_STANDARD_ON_SHELL_IDENTITY" for row in derivation_rows)
            and any(row["derivation_id"] == "MPD1044_7_exact_theorem_if_signed" and row["derivation_result"] == "EXACT_CONDITIONAL_THEOREM" for row in derivation_rows)
            and any(row["derivation_id"] == "MPD1044_8_current_verdict" and row["derivation_result"] == "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED" for row in derivation_rows)
            and all(not flag(row["valid_for_claim"]) for row in derivation_rows),
            "chain-rule zero theorem is exact but current qbarXT zero claim remains blocked",
        )
    )
    checks.append(
        (
            "V1044_3_premise_gates_blocked",
            any(row["gate_id"] == "MPG1044_6_verdict" and row["gate_pass"] == "false" for row in premise_rows)
            and all(row["gate_pass"] == "false" and not flag(row["valid_for_claim"]) for row in premise_rows),
            "matter-pullback premise gates are explicit and blocked",
        )
    )
    checks.append(
        (
            "V1044_4_qbar_components_nonclaim",
            any(row["component_id"] == "QBC1044_5_total_abs_guard" and row["current_value"] == "MISSING_COMPONENT_VALUES" for row in qbar_rows)
            and all("MISSING" in row["current_value"] and not flag(row["valid_for_claim"]) for row in qbar_rows),
            "qbarXT component envelope is staged with missing values and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1044_5_fallback_bounds_nonclaim",
            any(row["fallback_id"] == "QBF1044_0_WEP_source_proxy" and row["bound_value"] == "2.8e-15" for row in fallback_rows)
            and any(row["fallback_id"] == "QBF1044_1_R10_fifth_force" for row in fallback_rows)
            and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in fallback_rows),
            "WEP/R10 fallback anchors are present but nonclaim",
        )
    )
    checks.append(
        (
            "V1044_6_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1044_7_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1044 placeholder rows",
        )
    )
    checks.append(
        (
            "V1044_8_claim_gates_blocked",
            all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all qbar/local-GR/R10 claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1044_9_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1044_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv",
        OUT / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
        OUT / "P8_Y5_R10_1044_QBARXT_BOUND_FALLBACK_ROWS.csv",
        OUT / "P8_Y5_R10_1044_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1044_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1044_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1044_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1044_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1044_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1044_10_generated_files_in_post_checkpoint",
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
            "V1044_11_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1044_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1044 matter pullback J_X zero or qbarXT bound row validation summary",
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
    derivation_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1044 Y5 R10 matter pullback J_X zero or qbarXT bound row",
        "",
        "**Progress:** the ordinary-matter chain-rule route is now exact. If matter sees only `e_obs(q_loc(Phi))`, constants are vertical-trivial, matter fields have an owned fixed/gauge lift, and boundary terms are silent, then `delta_v S_T=0`, so `qbar_XT=0` and `J_matter=0` for this channel.",
        "",
        "**Current verdict:** the theorem is not yet an MTS claim because the parent matter functor, no-marker/constant sector, universal source-current, and boundary-support clauses are still unsigned in the corpus.",
        "",
        "**Fallback:** a no-cancellation `qbar_XT` component envelope is staged for WEP/R10/clock links, but every MTS component remains value-missing and invalid for claim scoring.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Matter pullback derivation",
        md_table(derivation_rows, ["derivation_id", "claim_piece", "formula", "derivation_result", "proof_status", "gap", "claim_allowed", "valid_for_claim"]),
        "## Matter pullback premise gate",
        md_table(premise_rows, ["gate_id", "premise", "needed_for", "current_status", "if_missing", "gate_pass", "valid_for_claim"]),
        "## qbarXT component envelope",
        md_table(qbar_rows, ["component_id", "symbol", "definition", "formula_or_bound", "required_input", "current_value", "status", "valid_for_claim"]),
        "## qbarXT bound fallback rows",
        md_table(fallback_rows, ["fallback_id", "observable", "bound_source", "bound_value", "mts_quantity", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
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
    derivation_rows = matter_pullback_derivation_rows()
    premise_rows = premise_gate_rows()
    qbar_rows = qbar_component_rows()
    fallback_rows = qbar_bound_fallback_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(derivation_rows, premise_rows, qbar_rows, smoke_rows)
    claim_rows_ = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        derivation_rows,
        premise_rows,
        qbar_rows,
        fallback_rows,
        mts_rows,
        smoke_rows,
        claim_rows_,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1044_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", derivation_rows)
    write_csv(OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv", premise_rows)
    write_csv(OUT / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv", qbar_rows)
    write_csv(OUT / "P8_Y5_R10_1044_QBARXT_BOUND_FALLBACK_ROWS.csv", fallback_rows)
    write_csv(OUT / "P8_Y5_R10_1044_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1044_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1044_CLAIM_GATES.csv", claim_rows_)
    write_csv(OUT / "P8_Y5_R10_1044_DECISION_LEDGER.csv", decision_rows_)
    write_csv(OUT / "P8_Y5_R10_1044_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1044_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        derivation_rows,
        premise_rows,
        qbar_rows,
        fallback_rows,
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
        raise SystemExit(f"1044 validation failed: {failed}")


if __name__ == "__main__":
    main()
