from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md"

PRIOR_580_VALIDATION = RESIDUALS / "P8_Y5_BRR545_580_VALIDATION.csv"
PRIOR_580_SUMMARY = RESIDUALS / "P8_Y5_R10_580_NONCLAIM_SUMMARY.csv"
BRANCH_DECISION_580 = RESIDUALS / "P8_Y5_R10_580_NOPOLE_OR_SOURCE_BRANCH_DECISION.csv"
PARENT_CANDIDATES_580 = RESIDUALS / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv"
RESIDUAL_TEMPLATE_580 = RESIDUALS / "P8_Y5_R10_580_RESIDUAL_SCORE_TEMPLATE.csv"
SOURCE_CHARGE_579 = RESIDUALS / "P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_581_SOURCE_REGISTER.csv"
THEOREM_CHAIN_PATH = RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv"
NO_POLE_CERTIFICATE_PATH = RESIDUALS / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv"
BOUNDARY_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_581_COUNTEREXAMPLE_STRESS_TESTS.csv"
CONSTRAINT_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_581_CONSTRAINT_ALGEBRA_REQUIREMENTS.csv"
RESIDUAL_FALLBACK_PATH = RESIDUALS / "P8_Y5_R10_581_FINITE_RESIDUAL_FALLBACK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_581_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_581_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_581_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_581_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_quotient_vertical_no_pole_theorem_shape_proved_conditionally_parent_premises_unfilled"
CLAIM_CEILING = "conditional_no_pole_theorem_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md"

SOURCE_FILES = [
    {
        "source_file": "580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md",
        "role": "immediate no-pole route selection",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_580_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_580_NONCLAIM_SUMMARY.csv",
        "role": "prior nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_580_NOPOLE_OR_SOURCE_BRANCH_DECISION.csv",
        "role": "selected no-pole route and fallback branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
        "role": "candidate parent X blocks",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_580_RESIDUAL_SCORE_TEMPLATE.csv",
        "role": "finite residual fallback template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv",
        "role": "source/test charge functionals to be killed by no-pole theorem",
    },
    {
        "source_file": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "quotient matter functor conditional theorem and counterexamples",
    },
    {
        "source_file": "414-local-quotient-invariant-algebra-triviality-gate.md",
        "role": "local invariant algebra burden",
    },
    {
        "source_file": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "role": "readout-after-variation no-cheat contract",
    },
    {
        "source_file": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "no-extension/universal-property blocker",
    },
    {
        "source_file": "222-parent-X-sector-degree-count-and-boundary-action.md",
        "role": "first-order X route and boundary momentum",
    },
    {
        "source_file": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
        "role": "multiplier constraint algebra and P owner blocker",
    },
    {
        "source_file": "235-projector-stress-variation-or-nohair-constraint-algebra.md",
        "role": "projector stress and no-hair rank/bracket tests",
    },
    {
        "source_file": "scripts/Y5_R10_quotient_vertical_no_pole_parent_theorem_attempt.py",
        "role": "this checkpoint generator",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, object]]:
    return [
        {
            "source_file": item["source_file"],
            "exists": str((ROOT / str(item["source_file"])).exists()),
            "role": item["role"],
        }
        for item in SOURCE_FILES
    ]


def make_theorem_chain() -> list[dict[str, object]]:
    return [
        {
            "step_id": "QVT581_0_parent_projection",
            "claim": "there is a parent configuration space Conf_parent and a projection pi: Conf_parent -> Q_obs",
            "mathematical_form": "d pi(v_X)=0 for the local vertical generator v_X",
            "derivation_status": "theorem_premise_open",
            "consequence": "X is a representative direction, not observed data",
            "if_missing": "X can be a real field and R10 remains finite",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_1_action_factorization",
            "claim": "bulk parent action factors through the quotient",
            "mathematical_form": "S_bulk[Phi]=S_red[pi(Phi)]",
            "derivation_status": "conditional_theorem_step",
            "consequence": "i_{v_X} dS_bulk=0 identically before field equations",
            "if_missing": "a conformal or marker coupling can source X",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_2_matter_factorization",
            "claim": "ordinary matter sees only observed quotient geometry and universal constants",
            "mathematical_form": "S_matter=S_matter[psi,hat_g(pi(Phi)),theta_univ] with v_X(theta_univ)=0",
            "derivation_status": "conditional_theorem_step_not_parent_derived",
            "consequence": "delta_X S_matter=0 and qbar_XT=0",
            "if_missing": "WEP-safe universal fifth force can still exist",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_3_Hessian_degeneracy",
            "claim": "the Hessian has no invertible vertical block",
            "mathematical_form": "H(v_X,.)=0 modulo constraints and gauge fixing; no Z_X |grad X|^2 + M_X^2 X^2 physical block",
            "derivation_status": "conditional_theorem_step",
            "consequence": "no X Green function and K_X=0",
            "if_missing": "a physical massive X pole exists and alpha(lambda) must be scored",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_4_Hamiltonian_constraints",
            "claim": "vertical variables are removed by first-class constraints",
            "mathematical_form": "pi_X ~= 0, C_X ~= 0, and {C_X,C_X} closes weakly on parent constraints",
            "derivation_status": "required_not_computed",
            "consequence": "X contributes zero local propagating degrees",
            "if_missing": "zero Hessian may mean under-specified dynamics, not gauge",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_5_boundary_charge",
            "claim": "vertical transformations carry no physical boundary charge in compact local systems",
            "mathematical_form": "Q_X[epsilon]=int_boundary epsilon B_X = 0 for allowed local vertical transformations",
            "derivation_status": "required_not_derived",
            "consequence": "no edge mode/source charge leaks into Qbar_XH",
            "if_missing": "X becomes boundary hair or an edge charge, not theorem-zero",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_6_readout_order",
            "claim": "readout/projectors are applied only after parent variation",
            "mathematical_form": "R_read: Sol(S_parent) -> Observables; delta S_parent/delta R_read is not a parent equation",
            "derivation_status": "conditional_no_cheat_rule",
            "consequence": "post-readout closure cannot create fake theorem-zero",
            "if_missing": "post-readout EFT can reintroduce active X source terms",
            "valid_for_claim": "false",
        },
        {
            "step_id": "QVT581_7_alpha_result",
            "claim": "if QVT581_0 through QVT581_6 hold, R10 has no active X alpha row",
            "mathematical_form": "K_X=0, qbar_XT=0, Qbar_XH=0, alpha_X(lambda) inactive",
            "derivation_status": "conditional_theorem_proved_but_premises_unfilled",
            "consequence": "this would be a real local-GR-style reduction for R10",
            "if_missing": "fall back to finite residual score",
            "valid_for_claim": "false",
        },
    ]


def make_no_pole_certificate() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "NPC581_0_configuration_space",
            "needed_clause": "Conf_parent is a quotient bundle or equivalent constrained space with X vertical",
            "proof_obligation": "construct pi and show d pi(v_X)=0",
            "current_status": "not_constructed",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_1_bulk_invariance",
            "needed_clause": "bulk action is invariant along v_X before gauge fixing/readout",
            "proof_obligation": "S_bulk=S_red o pi and no vertical kinetic/potential residue",
            "current_status": "conditional_only",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_2_matter_blindness",
            "needed_clause": "matter and constants factor through observed quotient data",
            "proof_obligation": "delta_X S_matter=0 and v_X(theta_A)=0 for all ordinary sectors",
            "current_status": "not_parent_derived",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_3_constraint_rank",
            "needed_clause": "vertical variables are first-class gauge/constraint variables",
            "proof_obligation": "rank Hessian(dot X,dot X)=0 plus bracket closure and correct degree count",
            "current_status": "rank_route_known_bracket_open",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_4_boundary_silence",
            "needed_clause": "vertical transformations have zero local boundary charge",
            "proof_obligation": "B_X=n_mu P^{mu nu} is zero, exact, pure gauge, or proper-gauge killed on compact boundary",
            "current_status": "open",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_5_no_extension",
            "needed_clause": "no covariant material marker extension is allowed to couple to X",
            "proof_obligation": "universal-property/no-natural-marker theorem or extension variation tax",
            "current_status": "no_extension_theorem_missing",
            "theorem_credit": "false",
        },
        {
            "certificate_id": "NPC581_6_claim_gate",
            "needed_clause": "all certificate clauses pass together",
            "proof_obligation": "only then set R10 X row to theorem-zero/no-pole",
            "current_status": "unfilled_certificate",
            "theorem_credit": "false",
        },
    ]


def make_boundary_audit() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "BCA581_0_proper_gauge",
            "boundary_case": "vertical parameter vanishes or is fixed on compact boundary",
            "mathematical_test": "epsilon|boundary=0 or allowed variations keep Q_X[epsilon]=0",
            "effect_on_no_pole": "safe_if_parent_boundary_conditions_are_derived",
            "current_status": "not_derived",
            "fallback": "retain boundary source row",
        },
        {
            "audit_id": "BCA581_1_large_vertical_transform",
            "boundary_case": "vertical transformation has nonzero boundary parameter",
            "mathematical_test": "Q_X[epsilon]=int_boundary epsilon B_X",
            "effect_on_no_pole": "fails_no_pole_if_Q_X_nonzero",
            "current_status": "open_edge_mode",
            "fallback": "treat as boundary hair/source charge",
        },
        {
            "audit_id": "BCA581_2_first_order_X_boundary_momentum",
            "boundary_case": "first-order X multiplier route",
            "mathematical_test": "B_X^nu=n_mu P[Y]^{mu nu}",
            "effect_on_no_pole": "safe_only_if_B_X_is_zero_exact_or_pure_gauge",
            "current_status": "known_from_222_not_closed",
            "fallback": "score Q_boundary contribution inside Q_X^H(lambda)",
        },
        {
            "audit_id": "BCA581_3_projector_boundary_stress",
            "boundary_case": "P_mem/projector variation creates stress or source leakage",
            "mathematical_test": "delta P_mem destinations are owned and no uncarried stress remains",
            "effect_on_no_pole": "fails_if_projector_source_is_unowned",
            "current_status": "safe_conditions_written_not_derived",
            "fallback": "retain projector/source residual",
        },
        {
            "audit_id": "BCA581_4_mass_channel_projection",
            "boundary_case": "boundary charge projects into measured Hamiltonian mass",
            "mathematical_test": "Pi_M^H[Q_boundary]=0 including reference-boundary terms",
            "effect_on_no_pole": "fails_R10_zero_if_projection_nonzero",
            "current_status": "not_derived",
            "fallback": "retain epsilon_PiM_X(lambda)",
        },
        {
            "audit_id": "BCA581_5_verdict",
            "boundary_case": "local compact boundary silence",
            "mathematical_test": "all BCA581_0 through BCA581_4 are safe",
            "effect_on_no_pole": "required_before_theorem_credit",
            "current_status": "blocked",
            "fallback": NEXT_TARGET,
        },
    ]


def make_counterexamples() -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CEX581_0_conformal_universal",
            "legal_leak": "hat_g_mu_nu=exp(2 a X) g_mu_nu",
            "why_it_survives_without_theorem": "universal and covariant but not quotient-blind unless a=0 follows from pi",
            "blocks": "matter_pullback_zero",
            "required_kill": "prove hat_g=hat_g(pi(Phi)) and v_X hat_g=0",
        },
        {
            "counterexample_id": "CEX581_1_boundary_edge_mode",
            "legal_leak": "vertical symmetry with nonzero boundary charge",
            "why_it_survives_without_theorem": "bulk gauge can still carry edge degrees on the boundary",
            "blocks": "K_X_or_Qbar_zero",
            "required_kill": "proper-gauge restriction or exact/pure-gauge boundary primitive",
        },
        {
            "counterexample_id": "CEX581_2_material_marker_extension",
            "legal_leak": "Q_tilde=(Q,m)/G_rel with m transforming covariantly",
            "why_it_survives_without_theorem": "strict covariance does not forbid a new material marker field",
            "blocks": "matter_blindness_and_no_extension",
            "required_kill": "universal-property/no-natural-marker theorem",
        },
        {
            "counterexample_id": "CEX581_3_post_readout_EFT",
            "legal_leak": "readout-selected reduced action varied as if fundamental",
            "why_it_survives_without_theorem": "closure-zero can be baked into an effective action and then backreact",
            "blocks": "readout_after_variation",
            "required_kill": "readout map only on Sol(S_parent)",
        },
        {
            "counterexample_id": "CEX581_4_second_class_constraint",
            "legal_leak": "rank-zero X sector but constraints become second class or leave an edge pair",
            "why_it_survives_without_theorem": "zero kinetic rank alone is not a first-class gauge proof",
            "blocks": "no_pole_degree_count",
            "required_kill": "Dirac bracket closure and degree-count audit",
        },
        {
            "counterexample_id": "CEX581_5_vertical_invariant_generator",
            "legal_leak": "local quotient-invariant scalar depends on the would-be vertical sector",
            "why_it_survives_without_theorem": "quotient language can still contain extra invariant generators",
            "blocks": "trivial local invariant algebra",
            "required_kill": "I_loc(Q)=I_geom[J^k(e_obs)] tensor universal constants",
        },
    ]


def make_constraint_requirements() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "CAR581_0_rank",
            "constraint_test": "rank Hessian(dot X,dot X)=0",
            "needed_result": "no regular X wave operator",
            "current_status": "known_as_necessary_from_222",
            "if_fails": "physical X pole; finite residual branch",
        },
        {
            "requirement_id": "CAR581_1_primary",
            "constraint_test": "pi_X ~= 0 or pi_X - sqrt(h)P^{0nu} ~= 0 depending on first-order form",
            "needed_result": "vertical coordinate has constrained momentum",
            "current_status": "template_written_not_closed",
            "if_fails": "X has phase-space degrees",
        },
        {
            "requirement_id": "CAR581_2_secondary",
            "constraint_test": "C_X=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu ~= 0",
            "needed_result": "X enforces a parent identity rather than propagating",
            "current_status": "conditional_from_223",
            "if_fails": "source identity is inserted rather than derived",
        },
        {
            "requirement_id": "CAR581_3_bracket_closure",
            "constraint_test": "{C_X(x),C_X(y)} closes weakly on parent constraints",
            "needed_result": "first-class/no-pole status",
            "current_status": "not_computed_parent_symplectic_missing",
            "if_fails": "second-class residual or new physical mode",
        },
        {
            "requirement_id": "CAR581_4_constitutive_owner",
            "constraint_test": "P[Y], J_eff[Y], P_mem[Y] are parent-owned composites",
            "needed_result": "no free tensor P or hand-inserted source identity",
            "current_status": "owner_missing",
            "if_fails": "the theory moved the insertion from X to P",
        },
        {
            "requirement_id": "CAR581_5_boundary_generator",
            "constraint_test": "constraint generator is differentiable with zero allowed boundary charge",
            "needed_result": "proper gauge rather than edge mode",
            "current_status": "open",
            "if_fails": "boundary charge enters Qbar_XH(lambda)",
        },
    ]


def make_residual_fallback() -> list[dict[str, object]]:
    return [
        {
            "fallback_id": "RFB581_0_no_pole_success",
            "condition": "all no-pole certificate clauses pass",
            "R10_handling": "remove physical X alpha row; K_X=0 by no Green function",
            "local_GR_meaning": "real theorem-zero candidate for fifth-force sector only",
            "current_status": "not_reached",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "RFB581_1_boundary_edge_fail",
            "condition": "bulk vertical but boundary charge nonzero",
            "R10_handling": "score boundary contribution inside Q_X^H(lambda) or a boundary range envelope",
            "local_GR_meaning": "finite/boundary residual, not GR derivation",
            "current_status": "retained_if_audit_fails",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "RFB581_2_constraint_closure_fail",
            "condition": "rank-zero route does not close as first-class",
            "R10_handling": "demote to auxiliary/residual branch until degrees are counted",
            "local_GR_meaning": "no no-pole credit",
            "current_status": "retained_if_bracket_fails",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "RFB581_3_matter_marker_fail",
            "condition": "matter or constants carry X/marker dependence",
            "R10_handling": "fill qbar_XT and possible species split",
            "local_GR_meaning": "WEP/R10 retained",
            "current_status": "retained_if_no_extension_fails",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "RFB581_4_physical_X_fail",
            "condition": "explicit parent has Z_X>0 and M_X^2>0 physical block",
            "R10_handling": "score alpha_X(lambda_X)=K_X Qbar_XH qbar_XT",
            "local_GR_meaning": "empirical survival only",
            "current_status": "finite_fallback_retained",
            "valid_for_claim": "false",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D581_0_conditional_no_pole_theorem",
            "decision": "accept quotient-vertical no-pole as a valid conditional theorem shape",
            "meaning": "if the parent quotient/action/matter/boundary/constraint premises are proven, X has no physical local fifth-force pole",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D581_1_no_claim_upgrade",
            "decision": "do not promote R10/local GR",
            "meaning": "the parent projection, no-extension, constraint closure, and boundary charge premises are not derived",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D581_2_boundary_and_constraint_are_next",
            "decision": "attack boundary charge plus Dirac closure next",
            "meaning": "these are the most concrete no-pole blockers left after the theorem shape",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D581_3_finite_branch_retained",
            "decision": "keep finite residual branch as fallback",
            "meaning": "any failed no-pole premise routes the theory back to alpha(lambda) scoring",
            "status": "fallback_retained",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU581_0_allowed",
            "allowed_after_581": "cite the quotient-vertical theorem as conditional mathematics",
            "forbidden_after_581": "call it a parent-derived no-pole theorem without projection, constraint, and boundary certificates",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU581_1_allowed",
            "allowed_after_581": "use boundary charge as the first red-team gate for no-pole",
            "forbidden_after_581": "drop boundary terms from a first-order X route",
            "next_action": "derive or retain B_X=n_mu P^{mu nu}",
        },
        {
            "route_id": "RU581_2_allowed",
            "allowed_after_581": "use finite residual score whenever no-pole premises fail",
            "forbidden_after_581": "hide edge modes, marker couplings, or second-class remnants as gauge",
            "next_action": "route failure into Qbar/qbar/K_X coefficient rows",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    theorem_chain: list[dict[str, object]],
    certificate: list[dict[str, object]],
    boundary_audit: list[dict[str, object]],
    counterexamples: list[dict[str, object]],
    constraint_requirements: list[dict[str, object]],
    residual_fallback: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    prior_claim_allowed = any(row.get("claim_allowed") == "true" for row in prior_summary)
    theorem_result = any(row["step_id"] == "QVT581_7_alpha_result" for row in theorem_chain)
    certificate_credit = [row for row in certificate if row.get("theorem_credit") == "true"]
    has_boundary_verdict = any(row["audit_id"] == "BCA581_5_verdict" for row in boundary_audit)
    has_conformal_counterexample = any(row["counterexample_id"] == "CEX581_0_conformal_universal" for row in counterexamples)
    has_bracket_requirement = any(row["requirement_id"] == "CAR581_3_bracket_closure" for row in constraint_requirements)
    fallback_all_nonclaim = all(row["valid_for_claim"] == "false" for row in residual_fallback)
    promoted_decisions = [row for row in decisions if "pass" in str(row["status"]).lower()]

    return [
        {
            "check_id": "V581_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V581_1_prior_580_clean",
            "result": "pass" if not prior_failures and not prior_claim_allowed else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};prior_claim_allowed={prior_claim_allowed}",
        },
        {
            "check_id": "V581_2_conditional_theorem_chain_written",
            "result": "pass" if len(theorem_chain) >= 8 and theorem_result else "fail",
            "detail": f"theorem_steps={len(theorem_chain)};alpha_result={theorem_result}",
        },
        {
            "check_id": "V581_3_no_certificate_promotion",
            "result": "pass" if not certificate_credit else "fail",
            "detail": f"certificate_rows={len(certificate)};theorem_credit_rows={len(certificate_credit)}",
        },
        {
            "check_id": "V581_4_boundary_charge_gate_written",
            "result": "pass" if has_boundary_verdict else "fail",
            "detail": f"boundary_rows={len(boundary_audit)};verdict_row={has_boundary_verdict}",
        },
        {
            "check_id": "V581_5_counterexamples_retained",
            "result": "pass" if has_conformal_counterexample and len(counterexamples) >= 6 else "fail",
            "detail": f"counterexamples={len(counterexamples)};conformal_guardrail={has_conformal_counterexample}",
        },
        {
            "check_id": "V581_6_constraint_algebra_blocker_visible",
            "result": "pass" if has_bracket_requirement else "fail",
            "detail": "bracket_closure_requirement_present",
        },
        {
            "check_id": "V581_7_finite_fallback_retained",
            "result": "pass" if fallback_all_nonclaim else "fail",
            "detail": f"fallback_rows={len(residual_fallback)};claim_rows=0",
        },
        {
            "check_id": "V581_8_no_R10_or_local_GR_claim",
            "result": "pass" if not promoted_decisions else "fail",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    theorem_chain: list[dict[str, object]],
    certificate: list[dict[str, object]],
    boundary_audit: list[dict[str, object]],
    counterexamples: list[dict[str, object]],
    constraint_requirements: list[dict[str, object]],
    residual_fallback: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 581 Y5 R10 quotient-vertical no-pole parent theorem attempt

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The no-pole route now has a clean conditional theorem: if `X` is genuinely vertical to a parent quotient before variation, the bulk action and matter action factor through that quotient, the constraint algebra removes the vertical pair, and the boundary charge vanishes, then `X` has no physical local Green function.
- In that conditional case, `K_X=0`, `qbar_XT=0`, `Qbar_XH=0`, and the R10 `alpha_X(lambda)` row is inactive for a real structural reason.
- The current corpus still cannot claim that result. The missing pieces are concrete: parent projection/universal property, matter/no-marker factorization, Dirac bracket closure, and boundary charge silence.

## Conditional Theorem
```text
Conf_parent --pi--> Q_obs
v_X in ker(d pi)
S_bulk[Phi]=S_red[pi(Phi)]
S_matter=S_matter[psi, hat_g(pi(Phi)), theta_univ]
Q_X[epsilon]=0 on the compact local boundary
pi_X ~= 0, C_X ~= 0, {{C_X,C_X}} closes weakly

=> i_{{v_X}} dS_parent = 0
=> H(v_X,.) = 0 modulo first-class constraints
=> no invertible X Green function
=> K_X=0 and no active alpha_X(lambda) row.
```

This is good theorem shape. It is not yet theorem ownership. The boundary/constraint part is where the dragon is sleeping with one eye open.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Quotient-Vertical Theorem Chain
{markdown_table(theorem_chain, ["step_id", "claim", "mathematical_form", "derivation_status", "consequence", "if_missing", "valid_for_claim"])}

## No-Pole Certificate Template
{markdown_table(certificate, ["certificate_id", "needed_clause", "proof_obligation", "current_status", "theorem_credit"])}

## Boundary Charge Audit
{markdown_table(boundary_audit, ["audit_id", "boundary_case", "mathematical_test", "effect_on_no_pole", "current_status", "fallback"])}

## Counterexample Stress Tests
{markdown_table(counterexamples, ["counterexample_id", "legal_leak", "why_it_survives_without_theorem", "blocks", "required_kill"])}

## Constraint Algebra Requirements
{markdown_table(constraint_requirements, ["requirement_id", "constraint_test", "needed_result", "current_status", "if_fails"])}

## Finite Residual Fallback
{markdown_table(residual_fallback, ["fallback_id", "condition", "R10_handling", "local_GR_meaning", "current_status", "valid_for_claim"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_581", "forbidden_after_581", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is a real tightening. We did not just say "maybe X is gauge"; we wrote the exact gauge/no-pole certificate and the exact things that can ruin it. If the boundary and Dirac algebra close, this is the kind of move that starts looking like a genuine GR-reduction mechanism. If they do not close, no shame, no mysticism: the branch becomes a finite residual and gets scored.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_validation = read_csv(PRIOR_580_VALIDATION)
    prior_summary = read_csv(PRIOR_580_SUMMARY)
    branch_decision_580 = read_csv(BRANCH_DECISION_580)
    parent_candidates_580 = read_csv(PARENT_CANDIDATES_580)
    residual_template_580 = read_csv(RESIDUAL_TEMPLATE_580)
    source_charge_579 = read_csv(SOURCE_CHARGE_579)

    theorem_chain = make_theorem_chain()
    certificate = make_no_pole_certificate()
    boundary_audit = make_boundary_audit()
    counterexamples = make_counterexamples()
    constraint_requirements = make_constraint_requirements()
    residual_fallback = make_residual_fallback()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        theorem_chain,
        certificate,
        boundary_audit,
        counterexamples,
        constraint_requirements,
        residual_fallback,
        decisions,
    )

    summary_rows = [
        {
            "summary_id": "S581_0_result",
            "status": STATUS,
            "conditional_no_pole_theorem_shape": "true",
            "parent_projection_derived": "false",
            "constraint_algebra_closed": "false",
            "boundary_charge_silenced": "false",
            "no_pole_theorem_claim": "false",
            "finite_branch_retained": "true",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "branch_rows_reused": len(branch_decision_580),
            "parent_candidate_rows_reused": len(parent_candidates_580),
            "residual_template_rows_reused": len(residual_template_580),
            "source_charge_rows_reused": len(source_charge_579),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        THEOREM_CHAIN_PATH,
        theorem_chain,
        ["step_id", "claim", "mathematical_form", "derivation_status", "consequence", "if_missing", "valid_for_claim"],
    )
    write_csv(
        NO_POLE_CERTIFICATE_PATH,
        certificate,
        ["certificate_id", "needed_clause", "proof_obligation", "current_status", "theorem_credit"],
    )
    write_csv(
        BOUNDARY_AUDIT_PATH,
        boundary_audit,
        ["audit_id", "boundary_case", "mathematical_test", "effect_on_no_pole", "current_status", "fallback"],
    )
    write_csv(
        COUNTEREXAMPLE_PATH,
        counterexamples,
        ["counterexample_id", "legal_leak", "why_it_survives_without_theorem", "blocks", "required_kill"],
    )
    write_csv(
        CONSTRAINT_REQUIREMENTS_PATH,
        constraint_requirements,
        ["requirement_id", "constraint_test", "needed_result", "current_status", "if_fails"],
    )
    write_csv(
        RESIDUAL_FALLBACK_PATH,
        residual_fallback,
        ["fallback_id", "condition", "R10_handling", "local_GR_meaning", "current_status", "valid_for_claim"],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update, ["route_id", "allowed_after_581", "forbidden_after_581", "next_action"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "conditional_no_pole_theorem_shape",
            "parent_projection_derived",
            "constraint_algebra_closed",
            "boundary_charge_silenced",
            "no_pole_theorem_claim",
            "finite_branch_retained",
            "claim_allowed",
            "R10_pass_for_claim",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "branch_rows_reused",
            "parent_candidate_rows_reused",
            "residual_template_rows_reused",
            "source_charge_rows_reused",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        theorem_chain,
        certificate,
        boundary_audit,
        counterexamples,
        constraint_requirements,
        residual_fallback,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "conditional_no_pole_theorem_shape": True,
                "no_pole_theorem_claim": False,
                "finite_branch_retained": True,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
