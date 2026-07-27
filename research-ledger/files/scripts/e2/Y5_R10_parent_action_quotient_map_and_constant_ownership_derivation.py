from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
EXTERNAL_DIR = ROOT / "source-intake" / "external_papers"

DOC = ROOT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_parent_action_quotient_map_and_constant_ownership_derivation.py"

STATUS = "Y5_R10_parent_action_quotient_derivation_partially_lifted_constants_not_owned_zero_clause_not_adopted"
CLAIM_CEILING = "conditional_parent_quotient_descent_only_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md"

PRIOR_636_DOC = ROOT / "636-Y5-R10-zero-clause-covariance-and-constants-repair-or-finite-input-sourcing.md"
PRIOR_636_VALIDATION = MTS_DIR / "P8_Y5_BRR545_636_VALIDATION.csv"
PRIOR_636_COVARIANCE = MTS_DIR / "P8_Y5_R10_636_COVARIANCE_REPAIR_LEMMA.csv"
PRIOR_636_CONSTANTS = MTS_DIR / "P8_Y5_R10_636_CONSTANT_OWNERSHIP_AUDIT.csv"
PRIOR_636_FINITE = MTS_DIR / "P8_Y5_R10_636_FINITE_INPUT_SOURCING_LEDGER.csv"
PRIOR_565_DOC = ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md"
PRIOR_566_DOC = ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md"
PRIOR_272_DOC = ROOT / "272-quotient-configuration-principle-from-topological-projector.md"
PRIOR_350_DOC = ROOT / "350-parent-PD-ownership-and-cell-state-derivation-gate.md"
PRIOR_407_DOC = ROOT / "407-primitive-relational-quotient-action-sketch.md"
PRIOR_410_DOC = ROOT / "410-quotient-matter-functor-theorem-attempt.md"
PRIOR_401_DOC = ROOT / "401-parent-matter-selector-theorem-attempt.md"
PRIOR_404_DOC = ROOT / "404-selector-blind-matter-axiom-origin.md"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_637_SOURCE_REGISTER.csv"
PARENT_ACTION_ATTEMPT = MTS_DIR / "P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv"
QUOTIENT_MAP_DERIVATION = MTS_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv"
OBS_FUNCTOR_DERIVATION = MTS_DIR / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv"
CONSTANT_OWNERSHIP_THEOREM = MTS_DIR / "P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv"
CONSTANT_STATUS = MTS_DIR / "P8_Y5_R10_637_CONSTANT_STATUS_UPDATE.csv"
ZERO_CLAUSE_STATUS = MTS_DIR / "P8_Y5_R10_637_ZERO_CLAUSE_STATUS.csv"
FINITE_BRANCH_UPDATE = MTS_DIR / "P8_Y5_R10_637_FINITE_BRANCH_UPDATE.csv"
ADOPTION_GATE = MTS_DIR / "P8_Y5_R10_637_ADOPTION_GATE.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_637_DECISION.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_637_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_637_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_637_VALIDATION.csv"


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
        (PRIOR_636_DOC, "immediate 636 checkpoint"),
        (PRIOR_636_VALIDATION, "636 validation gate"),
        (PRIOR_636_COVARIANCE, "636 covariance repair contract"),
        (PRIOR_636_CONSTANTS, "636 constant ownership audit"),
        (PRIOR_636_FINITE, "636 finite input sourcing ledger"),
        (PRIOR_565_DOC, "vertical observation theorem"),
        (PRIOR_566_DOC, "primitive quotient/no-marker clause"),
        (PRIOR_272_DOC, "presymplectic quotient route"),
        (PRIOR_350_DOC, "parent-owned quotient P_D route"),
        (PRIOR_407_DOC, "primitive relational quotient action sketch"),
        (PRIOR_410_DOC, "quotient matter functor attempt"),
        (PRIOR_401_DOC, "parent matter selector counterexample"),
        (PRIOR_404_DOC, "selector-blind axiom origin audit"),
        (EXTERNAL_DIR / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv", "EM/charge constant warning"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC637_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def parent_action_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PA637_0_parent_fields",
            "object": "Phi = (geometry, connection, memory/residual representatives, matter, boundary/domain data)",
            "derivation_attempt": "treat local Xhat as a candidate representative direction v_X inside the parent configuration space, not automatically as an observed scalar",
            "result": "setup_written",
            "why": "needed before q can be derived rather than asserted",
            "remaining_gap": "full primitive field list and parent Lagrangian are still not unique",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PA637_1_presymplectic_test",
            "object": "delta_v S_parent = boundary and Omega(v,delta)=0",
            "derivation_attempt": "use the 272 route: if v_X is relative-exact/topological with vanishing local boundary primitive, the parent presymplectic form has a null direction",
            "result": "conditional_pass",
            "why": "null directions of the presymplectic form define gauge/representative orbits",
            "remaining_gap": "relative-exactness and boundary primitive zero are not proven for all local Xhat variations",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PA637_2_reduced_phase_space",
            "object": "Q_obs = Phi_parent / N_X",
            "derivation_attempt": "define N_X as the integrable null distribution generated by v_X and quotient the parent phase/configuration space",
            "result": "conditional_derivation",
            "why": "this gives q as the canonical projection onto reduced data if the null distribution is parent-owned",
            "remaining_gap": "integrability/global domain conditions and dynamical boundary cases remain open",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PA637_3_action_descent",
            "object": "S_parent",
            "derivation_attempt": "if L_v S_parent=0 up to Ward/exact terms, S_parent factors through q: S_parent = S_red[Q_obs] + retained boundary/domain terms",
            "result": "conditional_theorem",
            "why": "a functional constant on quotient fibres descends to the quotient",
            "remaining_gap": "retained boundary/domain terms are exactly where hidden local sources can survive",
            "valid_for_claim": "false",
        },
    ]


def quotient_map_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "QM637_0_topological_projection",
            "candidate_map": "q_top: Phi -> [Phi] relative/topological quotient class",
            "derivation": "from 272 and 350: relative-exact representative variations are presymplectic-null; the physical map is projection to the quotient/cohomology class, not a metric-rank projector",
            "status": "conditionally_parent_owned",
            "closes_636_covariance": "partially",
            "what_it_closes": "q is no longer merely gauge-fixed if v_X is in the parent null distribution",
            "what_remains_open": "does Xhat exactly equal a relative-exact null generator in the local branch?",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "map_id": "QM637_1_equivariance",
            "candidate_map": "q(F.Phi)=F_Q.q(Phi)",
            "derivation": "canonical quotient projections are equivariant by construction when F maps null orbits to null orbits",
            "status": "conditional_math_pass",
            "closes_636_covariance": "yes_if_NX_invariant",
            "what_it_closes": "removes representative-choice dependence from the covariance repair",
            "what_remains_open": "prove diffeo/Lorentz/internal actions preserve N_X for the actual parent variables",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "map_id": "QM637_2_vertical_kernel",
            "candidate_map": "Dq[v_X]=0",
            "derivation": "if v_X is tangent to the null orbit N_X, then the quotient projection has v_X in its differential kernel",
            "status": "conditional_math_pass",
            "closes_636_covariance": "yes_if_vX_null",
            "what_it_closes": "supplies the exact kernel condition used by the 565/566 chain-rule theorem",
            "what_remains_open": "the local Xhat mode may instead be finite physical residual, not null representative",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "map_id": "QM637_3_observed_domain_guard",
            "candidate_map": "q local branch scoped to compact stationary/vacuum exterior domains",
            "derivation": "272 already warns dynamic merger/wall boundaries are not safe to quotient blindly",
            "status": "guarded_scope_required",
            "closes_636_covariance": "scope_only",
            "what_it_closes": "prevents quotient silence from overkilling cosmology/galaxy/memory phenomenology",
            "what_remains_open": "derive domain admissibility and boundary projector silence",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def obs_functor_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obs_id": "OF637_0_observed_geometry",
            "object": "Obs(Q_obs) = E_obs = (e_obs, g_obs, omega[e_obs])",
            "derivation": "if rods, clocks, photons, and ordinary matter are readouts of reduced quotient data, Obs is a natural functor on Q_obs",
            "status": "conditional_descent",
            "matter_zero_use": "DObs(Dq[v_X])=0 for v_X in ker(Dq)",
            "remaining_gap": "ordinary matter readout from reduced data is still a parent selection principle unless the parent action supplies it",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "obs_id": "OF637_1_chain_rule",
            "object": "delta_v S_matter",
            "derivation": "S_matter=Sbar_m[Obs(q(Phi)),Psi,theta] gives delta_v S_matter=(delta Sbar/dE_obs)DObs(Dq[v])+(partial Sbar/partial theta_A)delta_v theta_A",
            "status": "math_pass",
            "matter_zero_use": "metric/frame part vanishes exactly if v is vertical",
            "remaining_gap": "constant/material-marker term survives unless theta_A descends or is fixed representation data",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
        {
            "obs_id": "OF637_2_counterexample_filter",
            "object": "hidden conformal/disformal frame",
            "derivation": "if e_hat=exp(F(Xhat))e_obs changes ordinary matter, then F(Xhat) is an observable channel and must either factor through Q_obs or be finite-coupled; it cannot be hidden",
            "status": "classification_pass_not_zero_proof",
            "matter_zero_use": "rules out fake no-shadow wording",
            "remaining_gap": "does not prove F prime is zero; it only tells us to demote such F to the finite branch",
            "claim_blocker": "true",
            "valid_for_claim": "false",
        },
    ]


def constant_ownership_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CO637_0_descent_criterion",
            "statement": "A matter constant theta_A is silent under v_X iff it is fixed representation data or descends to the quotient: theta_A(Phi)=theta_bar_A(q(Phi)); then delta_v theta_A=Dtheta_bar(Dq[v_X])=0.",
            "proof_status": "math_pass",
            "physical_status": "requires parent classification of each constant",
            "failure_if_not": "theta_A(Xhat) becomes a material marker/source charge",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CO637_1_no_smooth_marker_on_quotient",
            "statement": "A smooth vertical-representative marker m_A(Xhat) is not a well-defined function on Q_obs unless it is constant on null orbits.",
            "proof_status": "math_pass",
            "physical_status": "forbids markers only after ordinary matter is required to live on Q_obs",
            "failure_if_not": "marker-extended matter is a legal finite coupling counterexample",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CO637_2_discrete_topological_escape",
            "statement": "Discrete representation/topological labels can be quotient-owned because local smooth vertical variation cannot change an integer charge/winding/species label.",
            "proof_status": "conditional_pass",
            "physical_status": "useful for charge/species only if the parent action derives those labels as topological/representation data",
            "failure_if_not": "EM charge or species mass parameters remain empirical constants with possible Xhat sensitivity",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CO637_3_universal_unit_rescaling",
            "statement": "A universal constant rescaling is locally silent only if it is pure unit convention and leaves dimensionless observables unchanged.",
            "proof_status": "conditional_pass",
            "physical_status": "does not save alpha_EM, mass ratios, composition sensitivities, or clock ratios",
            "failure_if_not": "clock/WEP channels reopen even when metric pullback vanishes",
            "valid_for_claim": "false",
        },
    ]


def constant_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "constant_id": "CS637_0_c_light",
            "sector": "geometry/clocks",
            "ownership_update": "can be quotient-owned if defined by E_obs causal structure and units",
            "status_after_637": "partially_repaired",
            "remaining_gap": "exclude disformal shadow cone and prove observed geometry is parent-owned",
            "finite_if_fail": "tau_clock;gamma_minus_1",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CS637_1_em_charge_alpha",
            "sector": "EM/charge",
            "ownership_update": "mathematically silent only if alpha_EM/e descends to Q_obs or is topological/discrete representation data",
            "status_after_637": "open_blocker",
            "remaining_gap": "derive charge/gauge coupling as quotient/topological object; Andersen clue remains analogy only",
            "finite_if_fail": "d_ln_alpha_EM_dXhat;tau_clock;tau_WEP",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CS637_2_particle_masses",
            "sector": "particle/matter",
            "ownership_update": "silent only if all mass ratios/Yukawa/binding contributions are quotient-owned or fixed representation data",
            "status_after_637": "open_blocker",
            "remaining_gap": "no parent derivation of mass spectrum or composition-independent unit-only variation",
            "finite_if_fail": "beta_source;beta_test;composition_sensitivity",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CS637_3_clock_transitions",
            "sector": "time/clocks",
            "ownership_update": "inherits EM/mass/nuclear status; not independently closed",
            "status_after_637": "open_blocker",
            "remaining_gap": "clock ratios depend on alpha_EM and mass/nuclear constants",
            "finite_if_fail": "tau_clock;d_ln_nu_dXhat",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CS637_4_material_labels",
            "sector": "composition/source preparation",
            "ownership_update": "species labels can be discrete representation data, but density/source normalization may still carry Xhat",
            "status_after_637": "open_blocker",
            "remaining_gap": "prove material preparation data is quotient-independent for source and test bodies",
            "finite_if_fail": "beta_source;beta_test;WEP_charge_vector",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "CS637_5_measured_GM",
            "sector": "local gravity/operator",
            "ownership_update": "not a matter constant; must be owned by EH/PPN/source-normalization branch",
            "status_after_637": "open_blocker",
            "remaining_gap": "derive measured GM and operator residual vector from local GR limit",
            "finite_if_fail": "source_normalization_residual;PPN_vector",
            "valid_for_claim": "false",
        },
    ]


def zero_clause_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "ZCS637_0_q_Obs",
            "ingredient": "q and Obs parent-owned",
            "637_result": "partially_lifted",
            "reason": "presymplectic null/reduced quotient route can derive q conditionally; Obs naturality follows if readout is quotient data",
            "still_blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "status_id": "ZCS637_1_matter_descent",
            "ingredient": "S_matter descends to quotient",
            "637_result": "conditional_theorem_only",
            "reason": "chain-rule descent is exact if matter is a quotient functor, but parent action has not forced all matter sectors onto that functor",
            "still_blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "status_id": "ZCS637_2_constants",
            "ingredient": "constant/material-marker silence",
            "637_result": "not_closed",
            "reason": "descent criterion is proven as math, but EM/mass/clock/material labels are not parent-classified",
            "still_blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "status_id": "ZCS637_3_boundary",
            "ingredient": "boundary/projector/domain silence",
            "637_result": "not_closed",
            "reason": "presymplectic quotient route requires vanishing boundary primitive; dynamic boundary cases remain open",
            "still_blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "status_id": "ZCS637_4_GR_operator",
            "ingredient": "EH/PPN/operator local reduction",
            "637_result": "not_touched",
            "reason": "matter current silence is not the same as proving the metric operator is EH with zero residuals",
            "still_blocks_claim": "true",
            "valid_for_claim": "false",
        },
    ]


def finite_branch_update_rows() -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_636_FINITE)
    out: list[dict[str, Any]] = []
    for row in prior_rows:
        symbol = row.get("symbol", "")
        if "alpha_EM" in symbol or "m_A" in symbol or "nu" in symbol:
            update = "promote_priority_constant_sector_bridge"
        elif symbol in {"beta_source", "beta_test"}:
            update = "still_required_if_constant_or_marker_channel_survives"
        elif "Z_eff" in symbol or "lambda" in symbol or "M_X" in symbol:
            update = "still_required_if_Xhat_is_physical_not_null"
        else:
            update = "still_required_for_cross_arena_scoring"
        out.append(
            {
                "input_id": row.get("input_id", f"FI637_{len(out)}"),
                "symbol": symbol,
                "637_update": update,
                "source_status_after_637": row.get("current_source_status", "missing"),
                "why": row.get("required_if_zero_fails", ""),
                "valid_for_claim": "false",
            }
        )
    return out


def adoption_gate_rows(
    quotient_rows: list[dict[str, Any]],
    obs_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    open_constants = [row for row in constant_rows if row.get("status_after_637") == "open_blocker"]
    zero_blockers = [row for row in zero_rows if row.get("still_blocks_claim") == "true"]
    return [
        {
            "gate_id": "AG637_0_derivation_attempted",
            "requirement": "parent quotient, Obs functor, and constant ownership derivation attempted",
            "result": "pass" if len(quotient_rows) == 4 and len(obs_rows) == 3 and len(constant_rows) == 6 else "fail",
            "detail": f"quotient_rows={len(quotient_rows)};obs_rows={len(obs_rows)};constant_rows={len(constant_rows)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG637_1_zero_clause_parent_signed",
            "requirement": "all zero-clause ingredients are parent-derived without open constant/boundary/operator blockers",
            "result": "blocked",
            "detail": f"zero_blockers={len(zero_blockers)};open_constants={len(open_constants)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG637_2_q_derivation_status",
            "requirement": "q derived from null presymplectic parent action, not selected post-hoc",
            "result": "partial",
            "detail": "conditional derivation exists if v_X is relative-exact/null with vanishing boundary primitive",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG637_3_claim_status",
            "requirement": "no R10/WEP/PPN/clock/orbital/local-GR claim from conditional descent",
            "result": "pass",
            "detail": "c_g_zero_claimed=false;finite_branch_scoreable=false;local_GR=false",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D637_0_main_verdict",
            "decision": STATUS,
            "meaning": "q can be partially derived if local Xhat is a presymplectic-null representative, but constant ownership is still not closed",
            "status": "partial_derivation_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D637_1_best_news",
            "decision": "quotient_map_has_real_parent_route",
            "meaning": "the 272/350 presymplectic/topological route can make q a canonical reduced-space projection rather than a vibe",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D637_2_bad_news",
            "decision": "constants_still_hold_the_coupling_knife",
            "meaning": "alpha_EM, masses, clock ratios, material labels, and measured GM are not parent-owned yet",
            "status": "core_blocker",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D637_3_next",
            "decision": "attack_constant_sector_or_fill_finite_beta",
            "meaning": "the next best derivation is to prove constants descend/topological, otherwise convert them into explicit finite beta/tau rows",
            "status": "next_route_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC637_0_constant_sector_zero",
            "required_output": "prove alpha_EM, mass ratios, clock ratios, and species labels descend to Q_obs or are discrete/topological representation data",
            "success_condition": "delta_Xhat theta_A=0 is parent-classified for all ordinary matter constants",
            "if_success": "constants blocker closes for ordinary local matter",
            "if_fail": "constant sensitivities become finite beta/tau inputs",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC637_1_null_generator_certificate",
            "required_output": "prove local Xhat is exactly a relative-exact presymplectic-null generator with vanishing local boundary primitive",
            "success_condition": "Dq[v_Xhat]=0 is parent-derived in the local branch",
            "if_success": "q/Obs covariance blocker can close conditionally",
            "if_fail": "Xhat remains physical finite residual",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC637_2_boundary_and_operator_debt",
            "required_output": "separately derive boundary silence and EH/PPN/operator local reduction",
            "success_condition": "zero matter current is not mistaken for full local GR",
            "if_success": "local branch gets closer to GR reduction",
            "if_fail": "R10 silence alone cannot save local tests",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(
    quotient_rows: list[dict[str, Any]],
    constant_status: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    open_constants = [row for row in constant_status if row.get("status_after_637") == "open_blocker"]
    partial_q = [row for row in quotient_rows if row.get("status") in {"conditionally_parent_owned", "conditional_math_pass"}]
    zero_blockers = [row for row in zero_rows if row.get("still_blocks_claim") == "true"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "quotient_route_partially_derived": "true",
            "quotient_partial_rows": len(partial_q),
            "constants_closed": "false",
            "open_constant_rows": len(open_constants),
            "zero_clause_adopted": "false",
            "zero_blockers": len(zero_blockers),
            "finite_rows_retained": len(finite_rows),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    parent_rows: list[dict[str, Any]],
    quotient_rows: list[dict[str, Any]],
    obs_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row.get("exists") != "true"]
    prior_rows = read_csv(PRIOR_636_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_rows = [
        row
        for group in (parent_rows, quotient_rows, obs_rows, theorem_rows, constant_rows, zero_rows, finite_rows, gate_rows)
        for row in group
        if row.get("valid_for_claim") == "true"
    ]
    partial_q = [row for row in quotient_rows if row.get("status") in {"conditionally_parent_owned", "conditional_math_pass"}]
    open_constants = [row for row in constant_rows if row.get("status_after_637") == "open_blocker"]
    zero_blockers = [row for row in zero_rows if row.get("still_blocks_claim") == "true"]
    adoption_allowed = any(row.get("adoption_allowed") == "true" for row in gate_rows)
    return [
        {
            "check_id": "V637_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V637_1_prior_636_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V637_2_parent_action_attempt_complete",
            "result": "pass" if len(parent_rows) == 4 else "fail",
            "detail": f"parent_rows={len(parent_rows)}",
        },
        {
            "check_id": "V637_3_quotient_derivation_partial_not_claim",
            "result": "pass" if len(quotient_rows) == 4 and len(partial_q) >= 3 else "fail",
            "detail": f"quotient_rows={len(quotient_rows)};partial_q={len(partial_q)}",
        },
        {
            "check_id": "V637_4_obs_functor_chain_rule_written",
            "result": "pass" if len(obs_rows) == 3 else "fail",
            "detail": f"obs_rows={len(obs_rows)}",
        },
        {
            "check_id": "V637_5_constant_descent_theorem_written",
            "result": "pass" if len(theorem_rows) == 4 else "fail",
            "detail": f"theorem_rows={len(theorem_rows)}",
        },
        {
            "check_id": "V637_6_constants_remain_open",
            "result": "pass" if len(constant_rows) == 6 and len(open_constants) >= 5 else "fail",
            "detail": f"constant_rows={len(constant_rows)};open_constants={len(open_constants)}",
        },
        {
            "check_id": "V637_7_zero_clause_blocked",
            "result": "pass" if len(zero_rows) == 5 and len(zero_blockers) == 5 else "fail",
            "detail": f"zero_rows={len(zero_rows)};zero_blockers={len(zero_blockers)}",
        },
        {
            "check_id": "V637_8_finite_branch_retained",
            "result": "pass" if len(finite_rows) >= 6 else "fail",
            "detail": f"finite_rows={len(finite_rows)}",
        },
        {
            "check_id": "V637_9_adoption_blocked_no_claim_rows",
            "result": "pass" if len(gate_rows) == 4 and not adoption_allowed and not claim_rows else "fail",
            "detail": f"gate_rows={len(gate_rows)};adoption_allowed={bool_text(adoption_allowed)};claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V637_10_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V637_11_no_local_claim",
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
    parent_rows: list[dict[str, Any]],
    quotient_rows: list[dict[str, Any]],
    obs_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    constant_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = "\n".join(
        [
            "# 637 Y5 R10 parent action quotient map and constant ownership derivation",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Next target: `{NEXT_TARGET}`",
            "",
            "## Verdict",
            "- The quotient map route is stronger after this pass: if local `Xhat` is a relative-exact presymplectic-null representative, then `q` is the canonical reduced-space projection and `Dq[v_Xhat]=0` follows as math.",
            "- The observed-functor/chain-rule part is also clean: if matter descends through `Obs(q(Phi))`, the metric/frame coupling vanishes along vertical `Xhat` directions.",
            "- The derivation still does **not** close the local branch because constants are the live knife: `alpha_EM`, masses, clock ratios, material labels, and measured `GM` are not parent-owned yet.",
            "- Therefore `c_g=0`, R10, WEP, PPN, clocks, orbital, and local-GR remain nonclaim.",
            "",
            "## Derivation Core",
            "Let `N_X` be the candidate parent null distribution generated by local vertical `Xhat` variations. If the parent action satisfies",
            "",
            "`delta_v S_parent = dB_v` and `Omega(v,delta)=0` for all `v in N_X`,",
            "",
            "then `N_X` is gauge/representative data, the quotient map is the canonical projection",
            "",
            "`q: Phi_parent -> Q_obs = Phi_parent / N_X`,",
            "",
            "and every `v_X in N_X` obeys `Dq[v_X]=0`. For matter of the descended form",
            "",
            "`S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]`,",
            "",
            "the vertical variation is",
            "",
            "`delta_v S_matter = (delta Sbar_m/dE_obs) DObs(Dq[v]) + (partial Sbar_m/partial theta_A) delta_v theta_A`.",
            "",
            "So the geometry term is killed by the quotient. The constants term is killed only if `theta_A` is fixed representation data or descends to the quotient.",
            "",
            "## Source Register",
            markdown_table(source_rows),
            "## Parent Action Derivation Attempt",
            markdown_table(parent_rows),
            "## Quotient Map Derivation",
            markdown_table(quotient_rows),
            "## Observed Functor Derivation",
            markdown_table(obs_rows),
            "## Constant Ownership Theorem",
            markdown_table(theorem_rows),
            "## Constant Status Update",
            markdown_table(constant_rows),
            "## Zero Clause Status",
            markdown_table(zero_rows),
            "## Finite Branch Update",
            markdown_table(finite_rows),
            "## Adoption Gate",
            markdown_table(gate_rows),
            "## Decision",
            markdown_table(decision),
            "## Next Contract",
            markdown_table(contract_rows),
            "## Nonclaim Summary",
            markdown_table(summary),
            "## Validation",
            markdown_table(validation),
            "## Interpretation",
            "This is the best derivation progress so far on the local coupling route. The quotient map no longer has to be pure axiom if `Xhat` can be identified with a parent presymplectic-null representative. But the theory still cannot walk into the ring claiming local GR until the constants are owned. If constants descend, the zero branch becomes much more serious. If they do not, they become the finite two-leg coupling branch.",
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_rows = parent_action_attempt_rows()
    quotient_rows = quotient_map_derivation_rows()
    obs_rows = obs_functor_derivation_rows()
    theorem_rows = constant_ownership_theorem_rows()
    constant_rows = constant_status_rows()
    zero_rows = zero_clause_status_rows()
    finite_rows = finite_branch_update_rows()
    gate_rows = adoption_gate_rows(quotient_rows, obs_rows, constant_rows, zero_rows)
    decision = decision_rows()
    contract_rows = next_contract_rows()
    summary = nonclaim_summary_rows(quotient_rows, constant_rows, zero_rows, finite_rows)
    validation = validation_rows(
        source_rows,
        parent_rows,
        quotient_rows,
        obs_rows,
        theorem_rows,
        constant_rows,
        zero_rows,
        finite_rows,
        gate_rows,
        contract_rows,
    )

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(PARENT_ACTION_ATTEMPT, parent_rows)
    write_csv(QUOTIENT_MAP_DERIVATION, quotient_rows)
    write_csv(OBS_FUNCTOR_DERIVATION, obs_rows)
    write_csv(CONSTANT_OWNERSHIP_THEOREM, theorem_rows)
    write_csv(CONSTANT_STATUS, constant_rows)
    write_csv(ZERO_CLAUSE_STATUS, zero_rows)
    write_csv(FINITE_BRANCH_UPDATE, finite_rows)
    write_csv(ADOPTION_GATE, gate_rows)
    write_csv(DECISION, decision)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validation)
    write_doc(
        source_rows,
        parent_rows,
        quotient_rows,
        obs_rows,
        theorem_rows,
        constant_rows,
        zero_rows,
        finite_rows,
        gate_rows,
        decision,
        contract_rows,
        summary,
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
