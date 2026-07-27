from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
EXTERNAL_DIR = ROOT / "source-intake" / "external_papers"

DOC = ROOT / "636-Y5-R10-zero-clause-covariance-and-constants-repair-or-finite-input-sourcing.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_zero_clause_covariance_and_constants_repair_or_finite_input_sourcing.py"

STATUS = "Y5_R10_covariance_no_shadow_repair_contract_written_constants_and_parent_inputs_still_block_claim"
CLAIM_CEILING = "repair_contract_and_finite_input_sourcing_only_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md"

PRIOR_635_DOC = ROOT / "635-Y5-R10-zero-clause-consistency-review-or-two-leg-numeric-input-runner.md"
PRIOR_635_VALIDATION = MTS_DIR / "P8_Y5_BRR545_635_VALIDATION.csv"
PRIOR_635_REVIEW = MTS_DIR / "P8_Y5_R10_635_ZERO_CLAUSE_CONSISTENCY_REVIEW.csv"
PRIOR_635_GATE = MTS_DIR / "P8_Y5_R10_635_ZERO_CLAUSE_ADOPTION_GATE.csv"
PRIOR_635_INPUTS = MTS_DIR / "P8_Y5_R10_635_TWO_LEG_INPUT_STATUS.csv"
PRIOR_635_RUNNER = MTS_DIR / "P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv"
PRIOR_634_CLAUSE = MTS_DIR / "P8_Y5_R10_634_ZERO_BRANCH_PARENT_CLAUSE_DRAFT.csv"
PRIOR_634_CHAIN = MTS_DIR / "P8_Y5_R10_634_ZERO_CLAUSE_CONSEQUENCE_CHAIN.csv"
PRIOR_632_ENVELOPE = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_636_SOURCE_REGISTER.csv"
COVARIANCE_REPAIR = MTS_DIR / "P8_Y5_R10_636_COVARIANCE_REPAIR_LEMMA.csv"
NO_SHADOW_GATE = MTS_DIR / "P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv"
CONSTANT_AUDIT = MTS_DIR / "P8_Y5_R10_636_CONSTANT_OWNERSHIP_AUDIT.csv"
REPAIR_STATUS = MTS_DIR / "P8_Y5_R10_636_ZERO_BRANCH_REPAIR_STATUS.csv"
FINITE_INPUT_LEDGER = MTS_DIR / "P8_Y5_R10_636_FINITE_INPUT_SOURCING_LEDGER.csv"
ADOPTION_GATE = MTS_DIR / "P8_Y5_R10_636_ADOPTION_GATE.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_636_DECISION.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_636_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_636_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_636_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_635_DOC, "immediate 635 checkpoint"),
        (PRIOR_635_VALIDATION, "635 validation gate"),
        (PRIOR_635_REVIEW, "635 zero-clause consistency blockers"),
        (PRIOR_635_GATE, "635 adoption gate"),
        (PRIOR_635_INPUTS, "635 finite input missing ledger"),
        (PRIOR_635_RUNNER, "635 pressure-only two-leg runner"),
        (PRIOR_634_CLAUSE, "634 proposed quotient-only parent clause"),
        (PRIOR_634_CHAIN, "634 conditional consequence chain"),
        (PRIOR_632_ENVELOPE, "632 two-leg envelope source"),
        (ROOT / "241-C-silence-screening-or-parent-selection-theorem.md", "conformal/source-frame warning"),
        (ROOT / "360-universal-matter-coupling-theorem-attempt.md", "universal matter coupling attempt"),
        (ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "vertical observation theorem ingredient"),
        (ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "no-marker primitive quotient ingredient"),
        (EXTERNAL_DIR / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv", "EM/charge compatibility warning"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC636_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def covariance_repair_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "CV636_0_parent_quotient_equivariance",
            "object": "q: Phi_parent -> Q_obs",
            "repair_statement": "q must be a parent-defined quotient map equivariant under diffeomorphism, local Lorentz, and internal gauge actions: q(F.Phi)=F_Q.q(Phi).",
            "local_zero_use": "if v_X in ker(Dq)_Phi, then Dq_Phi[v_X]=0 in every representative because equivariance carries zero to zero",
            "closes_635_blocker": "covariance_if_parent_action_supplies_q",
            "remaining_gap": "q is still a selector contract, not derived from the parent action",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "CV636_1_observable_functor_naturality",
            "object": "Obs: Q_obs -> E_obs",
            "repair_statement": "Obs must be a natural observable functor: Obs(F_Q.Q)=F_E.Obs(Q), with observed coframe/metric/connection built only from Q_obs.",
            "local_zero_use": "partial_X e_obs = DObs_Q(Dq[v_X]) = 0 for vertical local Xhat directions",
            "closes_635_blocker": "covariance_if_Obs_is_parent_defined",
            "remaining_gap": "Obs is not yet constructed from primitive MTS variables",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "CV636_2_matter_action_descent",
            "object": "S_matter",
            "repair_statement": "ordinary matter action must descend: S_m[Phi,Psi,theta]=Sbar_m[Obs(q(Phi)),Psi,theta], up to Ward/exact boundary terms.",
            "local_zero_use": "delta_v S_m = (delta Sbar_m/dE_obs) DObs(Dq[v]) + (partial Sbar_m/partial theta_A) delta_v theta_A, so the matter current vanishes only if theta_A is also vertical-silent",
            "closes_635_blocker": "links_covariance_to_constants",
            "remaining_gap": "constant ownership is the remaining live channel",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def no_shadow_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NS636_0_observable_completeness",
            "rule": "any field/function that changes ordinary rods, clocks, masses, charges, or free-fall is an ordinary observable and must factor through Q_obs",
            "effect_on_shadow_frames": "a hidden A_g(Xhat), B_g(Xhat), or material-frame map either factors through q or violates the definition of ordinary observed geometry",
            "status": "candidate_repair_contract",
            "remaining_gap": "requires parent action to prove Q_obs is complete, not merely declared complete",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NS636_1_forbidden_representative_channel",
            "rule": "representative-only Xhat dependence may remain in gravitational/effective sectors, but it cannot enter ordinary matter preparation variables",
            "effect_on_shadow_frames": "prevents a killed fifth-force leg from reappearing as mass normalization, clock normalization, or source geometry",
            "status": "candidate_repair_contract",
            "remaining_gap": "must be checked against EM, particle, time, and material-composition sectors",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NS636_2_honesty_test",
            "rule": "if a proposed extra frame affects an experiment, it is not hidden; it is either quotient-owned or finite-coupled",
            "effect_on_shadow_frames": "turns no-shadow-frame from policy into a falsifiable classification test",
            "status": "useful_gate_not_theorem",
            "remaining_gap": "classification is ready, source derivation is not",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def constant_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "constant_id": "CA636_0_c_light",
            "sector": "geometry/clocks",
            "symbol_or_family": "c",
            "required_ownership": "causal-cone/observed-geometry quotient data",
            "zero_clause_condition": "no independent partial_Xhat c after units and observed metric are fixed",
            "audit_status": "candidate_silent_if_E_obs_parent_owned",
            "failure_mode": "disformal shadow cone creates clock/PPN residuals",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CA636_1_em_charge",
            "sector": "EM/charge",
            "symbol_or_family": "e, alpha_EM, gauge coupling",
            "required_ownership": "quotient/topological/representation data, not a smooth material scalar e(Xhat)",
            "zero_clause_condition": "partial_Xhat alpha_EM=0 or variation is topological/integer and not a fifth-force scalar",
            "audit_status": "open_blocker",
            "failure_mode": "clocks, spectra, WEP composition, and charge-sector work reopen the coupling",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CA636_2_particle_masses",
            "sector": "particle/matter",
            "symbol_or_family": "m_A, Yukawa data, binding energies",
            "required_ownership": "fixed matter representation or quotient-owned low-energy parameter",
            "zero_clause_condition": "partial_Xhat ln m_A=0 for all ordinary species or universal absorbed unit change with no composition residue",
            "audit_status": "open_blocker",
            "failure_mode": "composition-dependent scalar charge gives WEP and clock signals",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CA636_3_clock_transitions",
            "sector": "time/clocks",
            "symbol_or_family": "nu_clock, Rydberg, nuclear transition data",
            "required_ownership": "derived from quotient-owned EM/mass/nuclear parameters",
            "zero_clause_condition": "partial_Xhat ln nu_clock=0 after all underlying constants are audited",
            "audit_status": "open_blocker",
            "failure_mode": "clock drift appears even when direct metric coupling is zero",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CA636_4_material_labels",
            "sector": "composition/source preparation",
            "symbol_or_family": "species label A, isotope fraction, source density normalization",
            "required_ownership": "matter representation/preparation data independent of vertical representative choice",
            "zero_clause_condition": "delta_Xhat theta_A=0 for source and test bodies",
            "audit_status": "open_blocker",
            "failure_mode": "source/test beta legs survive as preparation-dependent charges",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CA636_5_Newton_G_measured",
            "sector": "local gravity/operator",
            "symbol_or_family": "G_N, GM, source normalization",
            "required_ownership": "operator/metric normalization after EH/PPN reduction, not matter fifth-force coupling",
            "zero_clause_condition": "no Xhat-dependent source normalization remains after quotient and boundary terms",
            "audit_status": "open_blocker",
            "failure_mode": "measured GM carries hidden source-normalization residual even if c_g=0",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def repair_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "RS636_0_covariance",
            "635_blocker": "CR635_1_covariance",
            "636_result": "repair_contract_written",
            "why_not_closed": "equivariance/naturality conditions are stated but not derived from a parent action",
            "next_requirement": "construct q and Obs from parent variables and symmetry group action",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "RS636_1_no_shadow_frame",
            "635_blocker": "CR635_2_no_shadow_frame",
            "636_result": "observable_completeness_gate_written",
            "why_not_closed": "ordinary observable completeness is a strong parent principle, not yet a theorem",
            "next_requirement": "prove all matter-affecting frame functions factor through q or are excluded by variation",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "RS636_2_constants",
            "635_blocker": "CR635_3_constants",
            "636_result": "constant_ownership_audit_written",
            "why_not_closed": "EM, particle masses, clock transitions, and source labels remain unsourced",
            "next_requirement": "derive zero constant variations or move them into finite beta/tau rows",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "RS636_3_boundary",
            "635_blocker": "CR635_4_boundary",
            "636_result": "not_repaired_this_checkpoint",
            "why_not_closed": "boundary/projector/domain silence remains outside the covariance/constants pass",
            "next_requirement": "derive Ward/exact/no-hair boundary projection silence",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "RS636_4_gr_limit",
            "635_blocker": "CR635_5_gr_limit",
            "636_result": "not_repaired_this_checkpoint",
            "why_not_closed": "killing direct matter coupling does not prove EH-only or PPN residual zero",
            "next_requirement": "derive local EH/PPN/operator reduction separately",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def finite_input_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "FI636_0_beta_source",
            "symbol": "beta_source",
            "required_if_zero_fails": "source-body scalar charge beta_s = delta ln m_source / delta Xhat or delta S_source / delta Xhat",
            "preferred_source": "parent matter action variation with composition/source model",
            "current_source_status": "missing_parent_numeric",
            "units": "dimensionless",
            "blocks_arena": "R10;WEP;orbital;source_normalization",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_1_beta_test",
            "symbol": "beta_test",
            "required_if_zero_fails": "test-body scalar charge beta_t including composition dependence",
            "preferred_source": "parent matter action variation for ordinary test material",
            "current_source_status": "missing_parent_numeric",
            "units": "dimensionless",
            "blocks_arena": "R10;WEP;clock",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_2_Z_eff",
            "symbol": "Z_eff",
            "required_if_zero_fails": "quadratic normalization of the exchanged local Xhat/residual mode",
            "preferred_source": "second variation/Hessian of parent local action around local vacuum",
            "current_source_status": "missing_parent_numeric",
            "units": "action_normalization",
            "blocks_arena": "all finite-coupling rows",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_3_MX_lambda",
            "symbol": "M_X^2, lambda_X",
            "required_if_zero_fails": "range of the exchanged mode, lambda_X=sqrt(Z_eff/M_X^2) after unit convention is fixed",
            "preferred_source": "parent Hessian plus local boundary/domain spectrum",
            "current_source_status": "missing_parent_numeric",
            "units": "m^-2;m",
            "blocks_arena": "R10;orbital;PPN",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_4_profile_tau_R10",
            "symbol": "profile_factor(lambda), tau_R10",
            "required_if_zero_fails": "geometry/source-shape conversion between beta_s beta_t/Z_eff and alpha(lambda)",
            "preferred_source": "R10 apparatus/source geometry projection plus validated alpha(lambda) curve",
            "current_source_status": "pressure_only_from_632_635",
            "units": "dimensionless",
            "blocks_arena": "R10 scoring",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_5_cross_arena_tau",
            "symbol": "tau_WEP,tau_clock,tau_PPN,tau_orbital",
            "required_if_zero_fails": "same beta law mapped into each local arena",
            "preferred_source": "composition sensitivities, clock sensitivities, weak-field metric map, orbital source normalization",
            "current_source_status": "missing_arena_projection",
            "units": "dimensionless",
            "blocks_arena": "WEP;clock;PPN;orbital",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI636_6_constant_sensitivities",
            "symbol": "d ln alpha_EM/dXhat, d ln m_A/dXhat, d ln nu/dXhat",
            "required_if_zero_fails": "constant-sector beta/tau bridge if constants are not vertical-silent",
            "preferred_source": "EM/particle/time-sector parent derivation",
            "current_source_status": "missing_parent_numeric",
            "units": "dimensionless_per_Xhat_unit",
            "blocks_arena": "WEP;clock;EM",
            "valid_for_claim": "false",
        },
    ]


def adoption_gate_rows(repair_rows: list[dict[str, Any]], constant_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = [row for row in repair_rows if row.get("claim_blocker") == "true"]
    open_constants = [row for row in constant_rows if row.get("audit_status") == "open_blocker"]
    return [
        {
            "gate_id": "AG636_0_repair_attempted",
            "requirement": "covariance, no-shadow, and constants blockers attempted before finite scoring",
            "result": "pass" if len(repair_rows) == 5 and len(constant_rows) == 6 else "fail",
            "detail": f"repair_rows={len(repair_rows)};constant_rows={len(constant_rows)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG636_1_parent_signed_zero_clause",
            "requirement": "q, Obs, matter descent, constant silence, boundary silence, and GR/operator limit are parent-signed",
            "result": "blocked",
            "detail": f"claim_blockers={len(blockers)};open_constants={len(open_constants)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG636_2_finite_branch_scoreable",
            "requirement": "all beta/Z/lambda/profile/cross-arena finite inputs are numeric and source-owned",
            "result": "blocked",
            "detail": "finite input ledger remains source-ready but non-numeric",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG636_3_claim_status",
            "requirement": "no local-test claim is made from a repair contract",
            "result": "pass",
            "detail": "c_g_zero_claimed=false;finite_branch_scoreable=false;local_GR=false",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D636_0_main_verdict",
            "decision": STATUS,
            "meaning": "the zero branch now has a sharper covariant/observable-completeness contract, but the parent action and constants still have to earn it",
            "status": "derivation_progress_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D636_1_covariance",
            "decision": "repair_contract_written_not_theorem",
            "meaning": "equivariance of q and naturality of Obs would stop gauge-fixed smuggling, but q and Obs are not yet derived",
            "status": "candidate_repair",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D636_2_constants",
            "decision": "constants_are_the_live_coupling_channel",
            "meaning": "EM charge, masses, clocks, and source labels are the places Xhat can still sneak back into matter",
            "status": "core_blocker",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D636_3_finite_branch",
            "decision": "finite_input_sourcing_ledger_ready_nonclaim",
            "meaning": "if the zero branch fails, the exact beta/Z/lambda/tau inputs needed for R10/WEP/PPN/clock/orbital pressure are now named",
            "status": "source_ready_not_scoreable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC636_0_parent_q_derivation",
            "required_output": "derive q and Obs from the parent action/symmetry structure, not from a post-hoc readout convention",
            "success_condition": "equivariance and naturality are consequences of the parent variational setup",
            "if_success": "covariance/no-shadow blockers can be downgraded",
            "if_fail": "zero clause remains closure-only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC636_1_constant_ownership",
            "required_output": "prove or reject vertical silence for EM charge, masses, clock frequencies, species labels, and measured GM",
            "success_condition": "all ordinary matter constants either factor through Q_obs/topological data or become finite beta/tau inputs",
            "if_success": "constants blocker closes or becomes numeric finite branch",
            "if_fail": "local branch cannot claim WEP/clock silence",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC636_2_finite_numeric_inputs",
            "required_output": "fill beta_source,beta_test,Z_eff,M_X^2,lambda_X,profile_factor,tau_arena if zero branch cannot close",
            "success_condition": "finite branch becomes scoreable without placeholder source legs",
            "if_success": "run private R10/WEP/PPN/clock/orbital pressure matrix",
            "if_fail": "finite branch remains qualitative only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(
    repair_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim_blockers = [row for row in repair_rows if row.get("claim_blocker") == "true"]
    open_constants = [row for row in constant_rows if row.get("audit_status") == "open_blocker"]
    missing_finite = [row for row in finite_rows if row.get("current_source_status", "").startswith("missing")]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "covariance_contract_written": "true",
            "observable_completeness_gate_written": "true",
            "constants_closed": "false",
            "zero_clause_adopted": "false",
            "claim_blockers": len(claim_blockers),
            "open_constant_rows": len(open_constants),
            "finite_missing_rows": len(missing_finite),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    covariance_rows: list[dict[str, Any]],
    no_shadow_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_635_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    covariance_claim_rows = [row for row in covariance_rows if row.get("valid_for_claim") == "true"]
    no_shadow_claim_rows = [row for row in no_shadow_rows if row.get("valid_for_claim") == "true"]
    constant_claim_rows = [row for row in constant_rows if row.get("valid_for_claim") == "true"]
    repair_claim_rows = [row for row in repair_rows if row.get("valid_for_claim") == "true"]
    finite_claim_rows = [row for row in finite_rows if row.get("valid_for_claim") == "true"]
    adoption_allowed = any(row.get("adoption_allowed") == "true" for row in gate_rows)
    open_constants = [row for row in constant_rows if row.get("audit_status") == "open_blocker"]
    missing_finite = [row for row in finite_rows if row.get("current_source_status", "").startswith("missing")]
    return [
        {
            "check_id": "V636_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V636_1_prior_635_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V636_2_covariance_contract_complete_nonclaim",
            "result": "pass" if len(covariance_rows) == 3 and not covariance_claim_rows else "fail",
            "detail": f"covariance_rows={len(covariance_rows)};claim_rows={len(covariance_claim_rows)}",
        },
        {
            "check_id": "V636_3_no_shadow_gate_complete_nonclaim",
            "result": "pass" if len(no_shadow_rows) == 3 and not no_shadow_claim_rows else "fail",
            "detail": f"no_shadow_rows={len(no_shadow_rows)};claim_rows={len(no_shadow_claim_rows)}",
        },
        {
            "check_id": "V636_4_constants_audited_open_nonclaim",
            "result": "pass" if len(constant_rows) == 6 and len(open_constants) >= 4 and not constant_claim_rows else "fail",
            "detail": f"constant_rows={len(constant_rows)};open_constants={len(open_constants)};claim_rows={len(constant_claim_rows)}",
        },
        {
            "check_id": "V636_5_repair_status_blocks_claim",
            "result": "pass" if len(repair_rows) == 5 and len(repair_claim_rows) == 0 and all(row.get("claim_blocker") == "true" for row in repair_rows) else "fail",
            "detail": f"repair_rows={len(repair_rows)};claim_rows={len(repair_claim_rows)}",
        },
        {
            "check_id": "V636_6_finite_input_ledger_nonclaim_missing",
            "result": "pass" if len(finite_rows) == 7 and len(missing_finite) >= 5 and not finite_claim_rows else "fail",
            "detail": f"finite_rows={len(finite_rows)};missing_finite={len(missing_finite)};claim_rows={len(finite_claim_rows)}",
        },
        {
            "check_id": "V636_7_adoption_blocked",
            "result": "pass" if len(gate_rows) == 4 and not adoption_allowed else "fail",
            "detail": f"gate_rows={len(gate_rows)};adoption_allowed={bool_text(adoption_allowed)}",
        },
        {
            "check_id": "V636_8_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V636_9_no_local_claim",
            "result": "pass",
            "detail": "zero_clause_adopted=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_doc(
    source_rows: list[dict[str, Any]],
    covariance_rows: list[dict[str, Any]],
    no_shadow_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = "\n".join(
        [
            "# 636 Y5 R10 zero clause covariance and constants repair or finite input sourcing",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Next target: `{NEXT_TARGET}`",
            "",
            "## Verdict",
            "- This checkpoint improves the zero branch: covariance is no longer vague once `q` is required to be equivariant and `Obs` natural.",
            "- The no-shadow-frame rule is now a sharper observable-completeness gate: anything that changes ordinary matter is either quotient-owned or a finite coupling, not hidden.",
            "- The route still does **not** close because the parent action has not derived `q/Obs`, and EM/particle/clock/material constants remain live coupling channels.",
            "- Therefore `c_g=0` is still not claimed; the finite branch remains pressure-only until beta/Z/lambda/tau inputs are sourced.",
            "",
            "## Source Register",
            markdown_table(source_rows),
            "## Covariance Repair Lemma",
            markdown_table(covariance_rows),
            "## No Shadow Frame Gate",
            markdown_table(no_shadow_rows),
            "## Constant Ownership Audit",
            markdown_table(constant_rows),
            "## Zero Branch Repair Status",
            markdown_table(repair_rows),
            "## Finite Input Sourcing Ledger",
            markdown_table(finite_rows),
            "## Adoption Gate",
            markdown_table(gate_rows),
            "## Decision",
            markdown_table(decision),
            "## Next Contract",
            markdown_table(contract_rows),
            "## Nonclaim Summary",
            markdown_table(summary_rows),
            "## Validation",
            markdown_table(validation),
            "## Interpretation",
            "The clean mathematical shape is now visible: if ordinary matter is a functor of the observed quotient only, then vertical local representative motion has no matter current. That is the elegant route. The price is that constants cannot be allowed to ride along as hidden material markers. If charge, mass, clock frequency, or source normalization varies with `Xhat`, the zero branch fails and the theory must use the finite two-leg branch.",
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    covariance_rows = covariance_repair_rows()
    no_shadow_rows = no_shadow_gate_rows()
    constant_rows = constant_audit_rows()
    repair_rows = repair_status_rows()
    finite_rows = finite_input_ledger_rows()
    gate_rows = adoption_gate_rows(repair_rows, constant_rows)
    decision = decision_rows()
    contract_rows = next_contract_rows()
    summary_rows = nonclaim_summary_rows(repair_rows, constant_rows, finite_rows)
    validation = validation_rows(
        source_rows,
        covariance_rows,
        no_shadow_rows,
        constant_rows,
        repair_rows,
        finite_rows,
        gate_rows,
        contract_rows,
    )

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(COVARIANCE_REPAIR, covariance_rows)
    write_csv(NO_SHADOW_GATE, no_shadow_rows)
    write_csv(CONSTANT_AUDIT, constant_rows)
    write_csv(REPAIR_STATUS, repair_rows)
    write_csv(FINITE_INPUT_LEDGER, finite_rows)
    write_csv(ADOPTION_GATE, gate_rows)
    write_csv(DECISION, decision)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary_rows)
    write_csv(VALIDATION, validation)
    write_doc(
        source_rows,
        covariance_rows,
        no_shadow_rows,
        constant_rows,
        repair_rows,
        finite_rows,
        gate_rows,
        decision,
        contract_rows,
        summary_rows,
        validation,
    )

    failed = [row for row in validation if row["result"] != "pass"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "doc": str(DOC),
                "failed_checks": failed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
