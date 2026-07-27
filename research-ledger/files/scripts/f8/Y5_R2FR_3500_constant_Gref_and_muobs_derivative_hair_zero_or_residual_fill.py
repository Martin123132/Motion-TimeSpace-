from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3500-Y5-R2FR-constant-Gref-and-muobs-derivative-hair-zero-or-residual-fill.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3500": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3499": {
        "path": ROOT / "3499-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Newton-gate-or-GM-transfer-bound.md",
        "role": "3499 handoff",
    },
    "next_3499": {
        "path": OUT / "P8_Y5_R2FR_3499_NEXT_TARGET.csv",
        "role": "3499 selected next target",
    },
    "delta_newton_3499": {
        "path": OUT / "P8_Y5_R2FR_3499_DELTA_NEWTON_RESIDUAL_VECTOR.csv",
        "role": "3499 Delta_Newton residual vector",
    },
    "constant_gm_zero_attempt": {
        "path": OUT / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "role": "prior constant-GM zero theorem attempt",
    },
    "constant_gm_derivative_gate": {
        "path": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "role": "derivative hair channel gate",
    },
    "constant_gm_bound_matrix": {
        "path": OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "role": "local derivative-hair bound matrix",
    },
    "constant_gm_runner_input": {
        "path": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "role": "local derivative-hair runner input",
    },
    "constant_gm_fill_queue": {
        "path": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
        "role": "priority fill queue",
    },
    "source_normalization_template": {
        "path": OUT / "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
        "role": "numeric input template",
    },
}


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": str(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def constant_gref_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "GREF3500_0_type_separation",
            "object": "G_ref_or_kappa_eff",
            "statement": "A constant parent-action coupling is not the measured orbital product mu_obs. It can be typed as a branch parameter multiplying the same Hilbert source in the EH weak-field equation.",
            "derivation_attempt": "If G_ref is a coupling parameter in the parent action rather than a local readout field, then D_X ln G_ref=0 follows by type for local derivative channels X={t,r,A,lambda,frame,domain}.",
            "status": "CANDIDATE_DERIVED_ZERO_FOR_GREF_ONLY",
            "remaining_gap": "parent action must explicitly own the unique source coupling and forbid post-readout GM absorption",
            "source_path": str(SOURCES["delta_newton_3499"]["path"]),
            "claim_scope": "G_ref derivative silence only; not mu_obs constancy",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GREF3500_1_numeric_value_policy",
            "object": "numerical_Newton_constant",
            "statement": "MTS does not need to derive the measured number G to reduce to Newton/GR; GR also takes its coupling from measurement.",
            "derivation_attempt": "The competitive target is stronger in a different place: derive that one universal parent coupling is used everywhere and cannot be retuned by orbit, species, range, clock, or frame.",
            "status": "POLICY_GUARD_NOT_A_PHYSICS_CLAIM",
            "remaining_gap": "absolute calibration owner remains separate from derivative-hair closure",
            "source_path": str(SOURCES["constant_gm_zero_attempt"]["path"]),
            "claim_scope": "prevents false demand that MTS must derive the decimal value of G",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GREF3500_2_no_orbital_absorption",
            "object": "G_ref_vs_mu_obs",
            "statement": "An orbitally calibrated GM cannot be used to hide source-side residuals; mu_obs must decompose into G_ref M_H plus explicit hair.",
            "derivation_attempt": "Use mu_obs=G_ref M_H(1+epsilon_mu). Any branch that fits mu_obs after readout rather than proving G_ref, M_H and epsilon_mu behavior is a transfer-bound branch, not a Newton derivation.",
            "status": "NO_SHORTCUT_GUARD",
            "remaining_gap": "epsilon_mu and M_H derivative channels still need zero proofs or executable residual rows",
            "source_path": str(SOURCES["constant_gm_derivative_gate"]["path"]),
            "claim_scope": "blocks hidden fitted-GM route",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GREF3500_3_superselection_contract",
            "object": "D_X_ln_G_ref",
            "statement": "The least-scrutiny route is to make G_ref a superselected coupling of the local EH/source block, not an emergent environmental scalar.",
            "derivation_attempt": "Then all derivative pressure shifts to M_H flux and epsilon_mu, where it belongs. This avoids asking a local fifth-force/PPN test to forgive a running Newton coupling.",
            "status": "ADOPT_AS_CANDIDATE_CONTRACT",
            "remaining_gap": "must be integrated into the parent action spine before it becomes a public theorem",
            "source_path": str(SOURCES["constant_gm_bound_matrix"]["path"]),
            "claim_scope": "candidate local action contract",
            "valid_for_claim": "False",
        },
    ]


def muobs_derivative_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "MU3500_0_master_decomposition",
            "object": "mu_obs",
            "exact_identity": "mu_obs = G_ref M_H (1+epsilon_mu)",
            "derivative_law": "D_X ln mu_obs = D_X ln G_ref + D_X ln M_H + D_X ln(1+epsilon_mu)",
            "zero_condition": "D_X ln G_ref=0, D_X ln M_H=0, and D_X epsilon_mu=0 for every active local channel X",
            "derived_status": "EXACT_IDENTITY_ONLY",
            "remaining_gap": "M_H flux conservation and epsilon_mu vector are not closed",
            "valid_for_claim": "False",
        },
        {
            "identity_id": "MU3500_1_after_Gref_contract",
            "object": "mu_obs_given_candidate_Gref",
            "exact_identity": "D_X ln mu_obs = D_X ln M_H + D_X ln(1+epsilon_mu)",
            "derivative_law": "G_ref drops out only if the parent coupling is a true superselected parameter",
            "zero_condition": "D_X ln M_H=0 and D_X epsilon_mu=0",
            "derived_status": "CONDITIONAL_REDUCTION",
            "remaining_gap": "local worldtube/source measure must prove no M_H leakage and no epsilon_mu hair",
            "valid_for_claim": "False",
        },
        {
            "identity_id": "MU3500_2_no_cancellation_credit",
            "object": "mu_obs_derivative_zero",
            "exact_identity": "0 = D_X ln G_ref + D_X ln M_H + D_X ln(1+epsilon_mu)",
            "derivative_law": "A cancellation among the three terms counts only if it is a parent Ward/superselection identity, not a fitted balance.",
            "zero_condition": "identity-level cancellation source path or row-by-row zero/bound",
            "derived_status": "GUARDRAIL",
            "remaining_gap": "no parent cancellation identity is currently supplied",
            "valid_for_claim": "False",
        },
        {
            "identity_id": "MU3500_3_first_order_boundary",
            "object": "Newton_branch",
            "exact_identity": "Newton first order requires constant source-normalized mu_obs, not merely a constant G_ref symbol.",
            "derivative_law": "Poisson/Gauss survives only if the source mass and residual hair are derivative-silent over the tested exterior domain.",
            "zero_condition": "CGM1-CGM6 theorem-zero or numerically score below local locks",
            "derived_status": "NEWTON_GATE_RETAINED",
            "remaining_gap": "epsilon_mu vector is the highest-pressure missing row",
            "valid_for_claim": "False",
        },
    ]


def channel_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CGM3500_1_time_drift",
            "channel": "time",
            "symbol": "dln_mu_obs_dt",
            "after_Gref_contract": "dln_M_H_dt + partial_t_epsilon_mu/(1+epsilon_mu)",
            "gref_status": "candidate_zero_by_parent_parameter_type",
            "MH_status": "open_requires_Pi_M_flux_conservation",
            "epsilon_mu_status": "open_requires_mu_extra_channel_vector",
            "minimum_artifact": "P8_time_drift_residual_or_zero.csv",
            "artifact_exists": str((OUT / "P8_time_drift_residual_or_zero.csv").exists()),
            "current_result": "retained_no_claim",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_2_radial_hair",
            "channel": "radius",
            "symbol": "partial_r_ln_mu_obs",
            "after_Gref_contract": "partial_r_ln_M_H + partial_r_epsilon_mu/(1+epsilon_mu)",
            "gref_status": "candidate_zero_by_parent_parameter_type",
            "MH_status": "open_requires_exterior_no_leakage_or_profile",
            "epsilon_mu_status": "open_requires_radial_mu_extra_support_theorem_or_profile",
            "minimum_artifact": "P8_radial_mu_profile_or_zero.csv",
            "artifact_exists": str((OUT / "P8_radial_mu_profile_or_zero.csv").exists()),
            "current_result": "retained_no_claim",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_3_species_source",
            "channel": "source_species",
            "symbol": "eta_source_AB",
            "after_Gref_contract": "Delta_AB ln M_H + Delta_AB epsilon_mu/(1+epsilon_mu)",
            "gref_status": "candidate_species_blind_parameter",
            "MH_status": "open_requires_selector_blind_Hilbert_source",
            "epsilon_mu_status": "open_requires_no_species_mu_extra_coupling",
            "minimum_artifact": "P8_species_source_charge_residual_or_zero.csv",
            "artifact_exists": str((OUT / "P8_species_source_charge_residual_or_zero.csv").exists()),
            "current_result": "retained_no_claim",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_4_range_dependence",
            "channel": "range_lambda",
            "symbol": "alpha(lambda)",
            "after_Gref_contract": "D_lambda ln M_H + D_lambda epsilon_mu/(1+epsilon_mu)",
            "gref_status": "candidate_no_range_dependence",
            "MH_status": "open_requires_no_finite_range_source_leakage",
            "epsilon_mu_status": "open_requires_alpha_lambda_curve_or_no_range_theorem",
            "minimum_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "artifact_exists": str((OUT / "R10_alpha_lambda_curve_MTS_source_normalization.csv").exists()),
            "current_result": "retained_no_claim",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_5_frame_domain",
            "channel": "frame_domain",
            "symbol": "delta_frame_source",
            "after_Gref_contract": "Delta_frame ln M_H + Delta_frame epsilon_mu/(1+epsilon_mu)",
            "gref_status": "candidate_one_parent_coupling",
            "MH_status": "open_requires_same_pullback_for_source_variation_and_motion",
            "epsilon_mu_status": "open_requires_no_domain_projector_residual",
            "minimum_artifact": "P8_frame_source_split_residual_or_zero.csv",
            "artifact_exists": str((OUT / "P8_frame_source_split_residual_or_zero.csv").exists()),
            "current_result": "retained_no_claim",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_6_mu_extra_amplitude",
            "channel": "all_channels",
            "symbol": "epsilon_mu",
            "after_Gref_contract": "mu_extra/(G_ref M_H)",
            "gref_status": "candidate_denominator_parameter",
            "MH_status": "open_requires_positive_same_source_measure",
            "epsilon_mu_status": "open_highest_pressure_missing_vector",
            "minimum_artifact": "P8_mu_extra_over_Geff_Meff_vector.csv",
            "artifact_exists": str((OUT / "P8_mu_extra_over_Geff_Meff_vector.csv").exists()),
            "current_result": "not_filled_primary_next_target",
            "blocks_newton_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CGM3500_7_second_order_ppn",
            "channel": "second_order",
            "symbol": "delta_beta_source",
            "after_Gref_contract": "second-order source-normalized residue after first-order rows close",
            "gref_status": "candidate_zero_not_sufficient",
            "MH_status": "deferred_until_first_order_closes",
            "epsilon_mu_status": "deferred_until_first_order_closes",
            "minimum_artifact": "P8_second_order_source_normalized_PPN_vector.csv",
            "artifact_exists": str((OUT / "P8_second_order_source_normalized_PPN_vector.csv").exists()),
            "current_result": "deferred_not_local_GR_claim",
            "blocks_newton_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "FILL3500_1_mu_extra_vector",
            "channel_id": "CGM3500_6_mu_extra_amplitude",
            "component": "boundary_bulk_domain_memory_nonEH",
            "symbol": "epsilon_mu = mu_extra/(G_ref M_H)",
            "formula": "epsilon_mu=sum_i c_i O_i/(G_ref M_H)",
            "units": "dimensionless",
            "bound_or_target": "zero theorem or component locks from PPN/R10/R11/Gdot",
            "required_columns": "component;coefficient;operator;normalization;units;source_path;derivative_tags;valid_for_claim",
            "artifact": "P8_mu_extra_over_Geff_Meff_vector.csv",
            "current_value": "MISSING_VECTOR",
            "score_status": "not_scoreable",
            "next_action": "try parent no-hair/Ward zero; otherwise fill coefficient vector",
        },
        {
            "fill_id": "FILL3500_2_time",
            "channel_id": "CGM3500_1_time_drift",
            "component": "time_drift",
            "symbol": "dln_G_ref_dt;dln_M_H_dt;partial_t_epsilon_mu",
            "formula": "dln_mu_obs_dt=dln_M_H_dt+partial_t_epsilon_mu/(1+epsilon_mu)",
            "units": "yr^-1",
            "bound_or_target": "abs(predicted drift)<=9.6e-15 yr^-1 or theorem-zero",
            "required_columns": "term;value;units;bound;source_path;status;valid_for_claim",
            "artifact": "P8_time_drift_residual_or_zero.csv",
            "current_value": "existing_nonclaim_or_missing_numeric_terms",
            "score_status": "retained_nonclaim",
            "next_action": "separate G_ref superselection from M_H flux and mu_extra drift",
        },
        {
            "fill_id": "FILL3500_3_radial",
            "channel_id": "CGM3500_2_radial_hair",
            "component": "radial_profile",
            "symbol": "partial_r_ln_mu_obs",
            "formula": "partial_r_ln_M_H+partial_r_epsilon_mu/(1+epsilon_mu)",
            "units": "inverse_length_or_dimensionless_envelope",
            "bound_or_target": "zero exterior radial hair or profile envelope below PPN/R10 mappings",
            "required_columns": "r;partial_r_ln_M_H;partial_r_epsilon_mu;units;bound_map;source_path;valid_for_claim",
            "artifact": "P8_radial_mu_profile_or_zero.csv",
            "current_value": "existing_nonclaim_or_missing_profile",
            "score_status": "retained_nonclaim",
            "next_action": "derive Gauss exterior no-hair or fill radial envelope",
        },
        {
            "fill_id": "FILL3500_4_range",
            "channel_id": "CGM3500_4_range_dependence",
            "component": "finite_range",
            "symbol": "alpha(lambda)",
            "formula": "alpha(lambda) <- D_lambda epsilon_mu and source-normalized finite-range carrier",
            "units": "dimensionless_vs_length",
            "bound_or_target": "alpha(lambda) below real R10 curve or theorem-zero",
            "required_columns": "lambda;alpha_predicted;alpha_bound;units;source_path;valid_for_claim",
            "artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "current_value": "existing_nonclaim_template",
            "score_status": "retained_nonclaim",
            "next_action": "upgrade from smoke/template to sourced curve or no-range theorem",
        },
        {
            "fill_id": "FILL3500_5_species",
            "channel_id": "CGM3500_3_species_source",
            "component": "source_species",
            "symbol": "eta_source_AB",
            "formula": "Delta_AB ln M_H + Delta_AB epsilon_mu/(1+epsilon_mu)",
            "units": "dimensionless",
            "bound_or_target": "abs(eta_source_AB)<=2.8e-15 or selector-blind theorem",
            "required_columns": "species_pair;eta_source_AB;terms;bound;source_path;valid_for_claim",
            "artifact": "P8_species_source_charge_residual_or_zero.csv",
            "current_value": "existing_nonclaim_or_missing_prediction",
            "score_status": "retained_nonclaim",
            "next_action": "prove source action has no species selector or fill eta residual",
        },
        {
            "fill_id": "FILL3500_6_frame",
            "channel_id": "CGM3500_5_frame_domain",
            "component": "frame_domain_split",
            "symbol": "delta_frame_source",
            "formula": "Delta_frame ln M_H + Delta_frame epsilon_mu/(1+epsilon_mu)",
            "units": "dimensionless",
            "bound_or_target": "same parent pullback or residual below WEP/clock locks",
            "required_columns": "frame_pair;delta_frame_source;source_pullback;matter_pullback;bound;source_path;valid_for_claim",
            "artifact": "P8_frame_source_split_residual_or_zero.csv",
            "current_value": "existing_nonclaim_or_missing_same_source_variation_theorem",
            "score_status": "retained_nonclaim",
            "next_action": "attach same-frame theorem to source variation, not only geodesic readout",
        },
    ]
    for row in rows:
        artifact_path = OUT / row["artifact"]
        row["artifact_path"] = str(artifact_path)
        row["artifact_exists"] = str(artifact_path.exists())
        row["valid_for_claim"] = "False"
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3500_0_Gref_progress",
            "decision": "Promote G_ref derivative silence to a candidate parent-action contract, not a live claim.",
            "rationale": "Typing G_ref as the unique local EH/source coupling gives D_X ln G_ref=0 without pretending to derive the measured decimal value of G.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3500_1_muobs_not_closed",
            "decision": "Do not promote constant measured GM/Newton yet.",
            "rationale": "mu_obs still contains M_H flux and epsilon_mu hair; both must be theorem-zero or explicitly bounded channel-by-channel.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3500_2_best_next_target",
            "decision": "Attack epsilon_mu directly before more orbit/cosmology testing.",
            "rationale": "The missing mu_extra vector is the common bottleneck for Gdot, radial hair, R10, PPN beta/gamma and R11 non-EH spillover.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3500_3_no_tuned_cancellation",
            "decision": "No cancellation credit without a parent identity.",
            "rationale": "A fitted balance between M_H drift and epsilon_mu drift would preserve a curve but not a theory; it must be a Ward/superselection/source identity.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3501-Y5-R2FR-mu-extra-over-Gref-MH-vector-zero-or-coefficient-fill.md",
            "next_script": "scripts/Y5_R2FR_3501_mu_extra_over_Gref_MH_vector_zero_or_coefficient_fill.py",
            "objective": "Prove epsilon_mu=mu_extra/(G_ref M_H)=0 from parent no-hair/Ward/source descent, or fill the component coefficient vector with units and nonclaim status.",
            "success_gate": "Every boundary, bulk, domain, memory, range and non-EH contribution is theorem-zero or has a sourced coefficient row with derivative tags.",
            "forbidden_shortcuts": "no orbital GM absorption; no alpha3/PPN cancellation by hand; no universal-constant absorption unless all D_X epsilon_mu vanish",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3500_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3500_CONSTANT_GREF_SIGNATURE.csv",
        OUT / "P8_Y5_R2FR_3500_MUOBS_DERIVATIVE_IDENTITY.csv",
        OUT / "P8_Y5_R2FR_3500_DERIVATIVE_CHANNEL_GATE.csv",
        OUT / "P8_Y5_R2FR_3500_RESIDUAL_FILL_ROWS.csv",
        OUT / "P8_Y5_R2FR_3500_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3500_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *signatures, *identities, *channels, *fills, *decisions, *next_rows]
    checks = [
        {
            "check_id": "VAL3500_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local source-register paths exist",
        },
        {
            "check_id": "VAL3500_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3500_2_gref_candidate_zero",
            "passed": any(row["status"] == "CANDIDATE_DERIVED_ZERO_FOR_GREF_ONLY" for row in signatures),
            "detail": "G_ref derivative silence is isolated as candidate zero only",
        },
        {
            "check_id": "VAL3500_3_muobs_identity",
            "passed": any("D_X ln mu_obs" in row["derivative_law"] for row in identities),
            "detail": "master mu_obs derivative identity present",
        },
        {
            "check_id": "VAL3500_4_channel_gates",
            "passed": len(channels) >= 7 and sum(1 for row in channels if row["blocks_newton_claim"] == "True") >= 6,
            "detail": f"channel_rows={len(channels)}; blocking_rows={sum(1 for row in channels if row['blocks_newton_claim'] == 'True')}",
        },
        {
            "check_id": "VAL3500_5_residual_fill_nonclaim",
            "passed": len(fills) >= 6 and all(row["valid_for_claim"] == "False" for row in fills),
            "detail": f"fill_rows={len(fills)}; all nonclaim",
        },
        {
            "check_id": "VAL3500_6_missing_mu_extra_vector_recorded",
            "passed": any(row["artifact"] == "P8_mu_extra_over_Geff_Meff_vector.csv" and row["artifact_exists"] == "False" for row in fills),
            "detail": "primary epsilon_mu vector is recorded as absent instead of assumed",
        },
        {
            "check_id": "VAL3500_7_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3500_8_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs stay under post-checkpoint-work/source-intake",
        },
        {
            "check_id": "VAL3500_9_next_target",
            "passed": len(next_rows) == 1 and "3501" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3500_SUMMARY",
            "passed": all(bool(check["passed"]) for check in checks),
            "detail": "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL",
        }
    )
    return [
        {
            "check_id": check["check_id"],
            "passed": str(bool(check["passed"])),
            "detail": check["detail"],
            "valid_for_claim": "False",
        }
        for check in checks
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    signatures: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3500 - Constant Gref and Muobs Derivative-Hair Zero or Residual Fill",
                "",
                "## Current Verdict",
                "- **Actual progress:** `G_ref` can be cleanly typed as a parent-action coupling, giving a candidate `D_X ln G_ref=0` route without pretending to derive the measured decimal value of Newton's constant.",
                "- **Still not Newton:** measured `mu_obs=GM` is not closed because `M_H` flux and `epsilon_mu=mu_extra/(G_ref M_H)` can still carry time, radial, species, range, frame, or domain hair.",
                "- **No fudge allowed:** a cancellation between source mass and residual hair only counts if it is a parent Ward/superselection identity, not a fitted orbit-by-orbit balance.",
                "- **Next best move:** attack the `epsilon_mu` vector directly; that is the common knot behind R10, Gdot, PPN, R11 and source-normalized Newton.",
                "",
                "## Constant Gref Signature",
                markdown_table(
                    signatures,
                    ["signature_id", "object", "statement", "status", "remaining_gap", "claim_scope", "valid_for_claim"],
                ),
                "",
                "## Muobs Derivative Identity",
                markdown_table(
                    identities,
                    ["identity_id", "object", "exact_identity", "derivative_law", "zero_condition", "derived_status", "remaining_gap", "valid_for_claim"],
                ),
                "",
                "## Derivative Channel Gates",
                markdown_table(
                    channels,
                    [
                        "gate_id",
                        "channel",
                        "symbol",
                        "gref_status",
                        "MH_status",
                        "epsilon_mu_status",
                        "minimum_artifact",
                        "artifact_exists",
                        "current_result",
                        "blocks_newton_claim",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Residual Fill Rows",
                markdown_table(
                    fills,
                    [
                        "fill_id",
                        "channel_id",
                        "symbol",
                        "bound_or_target",
                        "artifact",
                        "artifact_exists",
                        "score_status",
                        "next_action",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {generated_timestamp()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    signature_rows = constant_gref_signature_rows()
    identity_rows = muobs_derivative_identity_rows()
    channel_rows = channel_gate_rows()
    fill_rows = residual_fill_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    write_csv(
        OUT / "P8_Y5_R2FR_3500_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_CONSTANT_GREF_SIGNATURE.csv",
        signature_rows,
        [
            "signature_id",
            "object",
            "statement",
            "derivation_attempt",
            "status",
            "remaining_gap",
            "source_path",
            "claim_scope",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_MUOBS_DERIVATIVE_IDENTITY.csv",
        identity_rows,
        [
            "identity_id",
            "object",
            "exact_identity",
            "derivative_law",
            "zero_condition",
            "derived_status",
            "remaining_gap",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_DERIVATIVE_CHANNEL_GATE.csv",
        channel_rows,
        [
            "gate_id",
            "channel",
            "symbol",
            "after_Gref_contract",
            "gref_status",
            "MH_status",
            "epsilon_mu_status",
            "minimum_artifact",
            "artifact_exists",
            "current_result",
            "blocks_newton_claim",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_RESIDUAL_FILL_ROWS.csv",
        fill_rows,
        [
            "fill_id",
            "channel_id",
            "component",
            "symbol",
            "formula",
            "units",
            "bound_or_target",
            "required_columns",
            "artifact",
            "artifact_path",
            "artifact_exists",
            "current_value",
            "score_status",
            "next_action",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3500_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation_rows = validate(
        source_rows,
        signature_rows,
        identity_rows,
        channel_rows,
        fill_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3500_VALIDATION.csv",
        validation_rows,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(
        signature_rows,
        identity_rows,
        channel_rows,
        fill_rows,
        decision_ledger_rows,
        next_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
