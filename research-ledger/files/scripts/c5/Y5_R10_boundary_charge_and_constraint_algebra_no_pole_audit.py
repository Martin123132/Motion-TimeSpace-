from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md"

PRIOR_581_VALIDATION = RESIDUALS / "P8_Y5_BRR545_581_VALIDATION.csv"
PRIOR_581_SUMMARY = RESIDUALS / "P8_Y5_R10_581_NONCLAIM_SUMMARY.csv"
THEOREM_CHAIN_581 = RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv"
CERTIFICATE_581 = RESIDUALS / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv"
BOUNDARY_581 = RESIDUALS / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv"
CONSTRAINT_581 = RESIDUALS / "P8_Y5_R10_581_CONSTRAINT_ALGEBRA_REQUIREMENTS.csv"
FALLBACK_581 = RESIDUALS / "P8_Y5_R10_581_FINITE_RESIDUAL_FALLBACK.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_582_SOURCE_REGISTER.csv"
MOMENTUM_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv"
DIRAC_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv"
BOUNDARY_DETAIL_PATH = RESIDUALS / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv"
NOPOLE_GATE_PATH = RESIDUALS / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv"
FAILURE_ROUTER_PATH = RESIDUALS / "P8_Y5_R10_582_FAILURE_ROUTER_TO_RESIDUALS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_582_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_582_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_582_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_582_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_boundary_charge_and_constraint_algebra_audit_momentum_map_closure_conditional_boundary_not_silenced"
CLAIM_CEILING = "momentum_map_gate_and_boundary_audit_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md"

SOURCE_FILES = [
    {
        "source_file": "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "role": "immediate quotient-vertical no-pole theorem handoff",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_581_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_NONCLAIM_SUMMARY.csv",
        "role": "prior nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
        "role": "conditional no-pole theorem chain",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
        "role": "no-pole certificate obligations",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
        "role": "boundary charge blocker list",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_CONSTRAINT_ALGEBRA_REQUIREMENTS.csv",
        "role": "Dirac/bracket closure obligations",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_581_FINITE_RESIDUAL_FALLBACK.csv",
        "role": "fallback router from no-pole failure",
    },
    {
        "source_file": "222-parent-X-sector-degree-count-and-boundary-action.md",
        "role": "first-order X boundary momentum B_X",
    },
    {
        "source_file": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
        "role": "composite P[Y] and bracket-closure blocker",
    },
    {
        "source_file": "235-projector-stress-variation-or-nohair-constraint-algebra.md",
        "role": "P_mem/projector stress and no-hair bracket tests",
    },
    {
        "source_file": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "no-extension blocker for material marker leakage",
    },
    {
        "source_file": "scripts/Y5_R10_boundary_charge_and_constraint_algebra_no_pole_audit.py",
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


def make_momentum_theorem() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "MMT582_0_constraint_generator",
            "claim": "smeared constraint G[epsilon] generates the vertical X symmetry",
            "mathematical_form": "G[epsilon]=int_Sigma epsilon_nu C_X^nu + Q_boundary[epsilon]",
            "required_input": "parent symplectic form Omega_Y and parent-owned C_X[Y]",
            "result_if_true": "delta_epsilon F={F,G[epsilon]} is a gauge transformation",
            "current_status": "template_not_parent_owned",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MMT582_1_differentiability",
            "claim": "G[epsilon] is functionally differentiable",
            "mathematical_form": "delta G has no uncancelled int_boundary epsilon delta B_X",
            "required_input": "proper gauge epsilon|boundary=0, or Q_boundary cancels variation, or B_X=0/exact/pure gauge",
            "result_if_true": "Hamiltonian generator exists without hidden edge source",
            "current_status": "boundary_not_silenced",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MMT582_2_equivariance",
            "claim": "C_X is an equivariant momentum map",
            "mathematical_form": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "required_input": "Noether/momentum-map owner for P[Y], J_eff[Y], and P_mem[Y]",
            "result_if_true": "constraints are first class if K_boundary=0",
            "current_status": "parent_owner_missing",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MMT582_3_abelian_vertical_case",
            "claim": "for vertical shift symmetry, algebra should be abelian",
            "mathematical_form": "[epsilon,eta]=0 so {G[epsilon],G[eta]}=K_boundary[epsilon,eta]",
            "required_input": "vanishing boundary cocycle K_boundary",
            "result_if_true": "bracket closure reduces to boundary silence",
            "current_status": "K_boundary_uncomputed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MMT582_4_no_pole_result",
            "claim": "first-class differentiable vertical constraints remove X as a local pole",
            "mathematical_form": "rank H(dot X,dot X)=0 plus first-class pi_X,C_X and Q_boundary=0",
            "required_input": "degree count and boundary-silent momentum map",
            "result_if_true": "K_X=0; no alpha_X(lambda) row",
            "current_status": "conditional_theorem_only",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MMT582_5_failure_result",
            "claim": "boundary cocycle or nonclosing bracket demotes no-pole",
            "mathematical_form": "K_boundary!=0 or {C_X,C_X} not weakly proportional to constraints",
            "required_input": "explicit bracket/boundary calculation",
            "result_if_true": "edge mode, second-class remnant, or finite residual must be scored",
            "current_status": "failure_router_written",
            "valid_for_claim": "false",
        },
    ]


def make_dirac_audit() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "DA582_0_rank",
            "object": "X kinetic Hessian",
            "test": "rank d^2L/d(dot X)d(dot X)=0",
            "required_pass": "no regular X wave operator",
            "current_status": "necessary_condition_available_from_222",
            "verdict": "conditional_pass_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "DA582_1_primary_constraint",
            "object": "pi_X",
            "test": "pi_X~=0 or pi_X-sqrt(h)P^{0nu}~=0 depending on first-order convention",
            "required_pass": "X momentum constrained",
            "current_status": "template_known",
            "verdict": "conditional",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "DA582_2_secondary_constraint",
            "object": "C_X[Y]",
            "test": "C_X=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu~=0",
            "required_pass": "X enforces parent identity only",
            "current_status": "template_known_from_223",
            "verdict": "conditional",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "DA582_3_P_owner",
            "object": "P[Y], J_eff[Y], P_mem[Y]",
            "test": "all are variationally owned composites or momentum-map current components",
            "required_pass": "no free tensor or inserted source identity",
            "current_status": "not_derived",
            "verdict": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "DA582_4_bracket_closure",
            "object": "{C_X,C_X}",
            "test": "weakly closes on parent constraints with no nonzero boundary cocycle",
            "required_pass": "first-class gauge constraint",
            "current_status": "not_computed_parent_symplectic_missing",
            "verdict": "blocked_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "DA582_5_degree_count",
            "object": "local X phase-space pair",
            "test": "primary+secondary first-class pair removes the X pair; second-class count audited if not",
            "required_pass": "zero local propagating X degrees",
            "current_status": "not_completed",
            "verdict": "blocked_current_claim",
            "valid_for_claim": "false",
        },
    ]


def make_boundary_detail() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "BD582_0_bulk_variation",
            "boundary_term": "delta G_bulk -> int_boundary epsilon_nu n_mu delta P^{mu nu}",
            "silence_route": "epsilon|boundary=0 or add Q_boundary[epsilon]=-int_boundary epsilon_nu n_mu P^{mu nu}",
            "risk_if_open": "generator not differentiable; edge source hidden",
            "current_status": "open",
            "residual_if_fails": "Q_boundary_memory(lambda)",
        },
        {
            "audit_id": "BD582_1_charge_value",
            "boundary_term": "Q_X[epsilon]=int_boundary epsilon_nu B_X^nu",
            "silence_route": "proper gauge or B_X^nu=0/exact/pure gauge on compact shell",
            "risk_if_open": "large vertical transformations carry physical charge",
            "current_status": "not_zeroed",
            "residual_if_fails": "Qbar_XH(lambda)",
        },
        {
            "audit_id": "BD582_2_central_term",
            "boundary_term": "K_boundary[epsilon,eta] in {G[epsilon],G[eta]}",
            "silence_route": "boundary cocycle vanishes under compact-shell conditions",
            "risk_if_open": "first-class algebra fails or gains edge mode",
            "current_status": "uncomputed",
            "residual_if_fails": "edge_alpha_envelope(lambda)",
        },
        {
            "audit_id": "BD582_3_Pmem_projector",
            "boundary_term": "delta P_mem and projector stress at boundary/source split",
            "silence_route": "all projector variations have owned destinations or vanish by symmetry",
            "risk_if_open": "projector becomes a source term while pretending to be readout",
            "current_status": "safe_conditions_written_not_derived",
            "residual_if_fails": "epsilon_PiM_X(lambda)",
        },
        {
            "audit_id": "BD582_4_reference_boundary",
            "boundary_term": "reference subtraction and mass-channel projection",
            "silence_route": "Pi_M^H[Q_boundary]=0 including reference terms",
            "risk_if_open": "measured mass projector sees X edge charge",
            "current_status": "not_derived",
            "residual_if_fails": "Qbar_XH(lambda)",
        },
        {
            "audit_id": "BD582_5_verdict",
            "boundary_term": "full no-pole boundary certificate",
            "silence_route": "BD582_0 through BD582_4 pass together",
            "risk_if_open": "no-pole theorem remains conditional only",
            "current_status": "blocked_current_claim",
            "residual_if_fails": "finite_or_edge_residual_branch",
        },
    ]


def make_nopole_gate() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "NPG582_0_momentum_map_owner",
            "gate": "C_X is parent momentum map",
            "needed_for": "bracket closure and true gauge ownership",
            "current_status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "NPG582_1_boundary_differentiable",
            "gate": "G[epsilon] differentiable with no hidden edge source",
            "needed_for": "legal Hamiltonian generator",
            "current_status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "NPG582_2_boundary_charge_zero",
            "gate": "Q_X[epsilon]=0 for allowed compact-local vertical transformations",
            "needed_for": "no Qbar_XH edge leakage",
            "current_status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "NPG582_3_bracket_closure",
            "gate": "{C_X,C_X} closes weakly with K_boundary=0",
            "needed_for": "first-class no-pole status",
            "current_status": "not_computed",
            "gate_result": "blocked_current_claim",
        },
        {
            "gate_id": "NPG582_4_degree_count",
            "gate": "primary/secondary constraints remove X local pair",
            "needed_for": "zero X local degrees",
            "current_status": "not_completed",
            "gate_result": "blocked_current_claim",
        },
        {
            "gate_id": "NPG582_5_no_pole_claim",
            "gate": "all no-pole gates pass",
            "needed_for": "K_X=0 theorem credit",
            "current_status": "not_passed",
            "gate_result": "no_claim",
        },
    ]


def make_failure_router() -> list[dict[str, object]]:
    return [
        {
            "failure_id": "FR582_0_no_momentum_map_owner",
            "failure_condition": "C_X is not derived as a momentum map/current of parent symmetry",
            "route_to": "parent_momentum_map_owner_attempt",
            "residual_payload": "none yet; ownership blocker",
            "claim_effect": "no no-pole credit",
        },
        {
            "failure_id": "FR582_1_boundary_charge_nonzero",
            "failure_condition": "Q_X[epsilon] nonzero for allowed local vertical transformations",
            "route_to": "edge_residual_branch",
            "residual_payload": "Q_boundary_memory(lambda) and Qbar_XH(lambda)",
            "claim_effect": "finite/boundary residual score",
        },
        {
            "failure_id": "FR582_2_boundary_cocycle_nonzero",
            "failure_condition": "K_boundary[epsilon,eta] nonzero",
            "route_to": "edge_mode_or_central_extension",
            "residual_payload": "edge_alpha_envelope(lambda)",
            "claim_effect": "no first-class no-pole theorem",
        },
        {
            "failure_id": "FR582_3_second_class_remnant",
            "failure_condition": "constraints are second class or leave a reduced X pair",
            "route_to": "finite_auxiliary_residual",
            "residual_payload": "K_X or equivalent reduced propagator coefficient",
            "claim_effect": "score alpha(lambda) if propagator exists",
        },
        {
            "failure_id": "FR582_4_projector_stress_unowned",
            "failure_condition": "P_mem/projector variation has no owned stress destination",
            "route_to": "projector_source_residual",
            "residual_payload": "epsilon_PiM_X(lambda), Qbar_XH(lambda)",
            "claim_effect": "R10/R11 retained",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D582_0_momentum_map_gate_written",
            "decision": "accept momentum-map closure as the exact no-pole algebra gate",
            "meaning": "first-class no-pole requires C_X to be an equivariant parent momentum map with zero boundary cocycle",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D582_1_boundary_not_silenced",
            "decision": "do not claim boundary charge silence",
            "meaning": "B_X, Q_X, K_boundary, and Pi_M projection are not zeroed",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D582_2_no_pole_not_promoted",
            "decision": "do not promote no-pole/local-GR/R10",
            "meaning": "momentum-map owner and boundary differentiability remain unfilled",
            "status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D582_3_next_best_target",
            "decision": "derive parent momentum-map owner or demote edge charge",
            "meaning": "the next checkpoint must either own C_X as a real Noether/momentum map or route boundary charge to residual rows",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU582_0_allowed",
            "allowed_after_582": "use momentum-map closure as the formal criterion for no-pole",
            "forbidden_after_582": "treat rank-zero X alone as a first-class/no-pole proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU582_1_allowed",
            "allowed_after_582": "route nonzero boundary charges into explicit residual rows",
            "forbidden_after_582": "drop edge terms or hide them inside gauge language",
            "next_action": "compute or bound Q_boundary_memory(lambda)",
        },
        {
            "route_id": "RU582_2_allowed",
            "allowed_after_582": "keep the finite branch alive until all no-pole gates pass",
            "forbidden_after_582": "claim R10/local-GR from conditional algebra alone",
            "next_action": "parent momentum-map owner or edge residual demotion",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    momentum_theorem: list[dict[str, object]],
    dirac_audit: list[dict[str, object]],
    boundary_detail: list[dict[str, object]],
    nopole_gate: list[dict[str, object]],
    failure_router: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    prior_claim_allowed = any(row.get("claim_allowed") == "true" for row in prior_summary)
    has_equivariance = any(row["theorem_id"] == "MMT582_2_equivariance" for row in momentum_theorem)
    has_boundary_verdict = any(row["audit_id"] == "BD582_5_verdict" for row in boundary_detail)
    has_bracket = any(row["audit_id"] == "DA582_4_bracket_closure" for row in dirac_audit)
    no_gate_pass = all(row["gate_result"] != "pass" for row in nopole_gate)
    has_edge_router = any(row["failure_id"] == "FR582_1_boundary_charge_nonzero" for row in failure_router)
    claim_decisions = [row for row in decisions if "pass" in str(row["status"]).lower()]

    return [
        {
            "check_id": "V582_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V582_1_prior_581_clean",
            "result": "pass" if not prior_failures and not prior_claim_allowed else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};prior_claim_allowed={prior_claim_allowed}",
        },
        {
            "check_id": "V582_2_momentum_map_gate_written",
            "result": "pass" if has_equivariance and len(momentum_theorem) >= 6 else "fail",
            "detail": f"theorem_rows={len(momentum_theorem)};equivariance={has_equivariance}",
        },
        {
            "check_id": "V582_3_dirac_bracket_blocker_visible",
            "result": "pass" if has_bracket else "fail",
            "detail": f"dirac_rows={len(dirac_audit)};bracket_row={has_bracket}",
        },
        {
            "check_id": "V582_4_boundary_detail_written",
            "result": "pass" if has_boundary_verdict else "fail",
            "detail": f"boundary_rows={len(boundary_detail)};verdict_row={has_boundary_verdict}",
        },
        {
            "check_id": "V582_5_no_nopole_gate_promoted",
            "result": "pass" if no_gate_pass else "fail",
            "detail": f"gate_rows={len(nopole_gate)};gate_pass_rows=0",
        },
        {
            "check_id": "V582_6_failure_router_retains_edge_residual",
            "result": "pass" if has_edge_router else "fail",
            "detail": f"router_rows={len(failure_router)};edge_router={has_edge_router}",
        },
        {
            "check_id": "V582_7_no_R10_or_local_GR_claim",
            "result": "pass" if not claim_decisions else "fail",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    momentum_theorem: list[dict[str, object]],
    dirac_audit: list[dict[str, object]],
    boundary_detail: list[dict[str, object]],
    nopole_gate: list[dict[str, object]],
    failure_router: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 582 Y5 R10 boundary-charge and constraint-algebra no-pole audit

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The no-pole branch now has a precise algebraic gate: `C_X` must be an equivariant parent momentum map, and the smeared generator must be differentiable with zero boundary cocycle.
- This gives the exact theorem shape:

```text
G[epsilon] = int_Sigma epsilon_nu C_X^nu + Q_boundary[epsilon]
{{G[epsilon],G[eta]}} = G[[epsilon,eta]] + K_boundary[epsilon,eta]

first-class no-pole iff
C_X is parent-owned,
G is differentiable,
K_boundary = 0,
Q_X[epsilon] = 0 for allowed compact-local vertical transformations.
```

- Current verdict: conditional progress, not closure. Rank-zero `X` is not enough. Boundary charge and parent momentum-map ownership remain open, so no R10/local-GR claim is promoted.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Momentum-Map Closure Theorem
{markdown_table(momentum_theorem, ["theorem_id", "claim", "mathematical_form", "required_input", "result_if_true", "current_status", "valid_for_claim"])}

## Dirac Bracket Audit
{markdown_table(dirac_audit, ["audit_id", "object", "test", "required_pass", "current_status", "verdict", "valid_for_claim"])}

## Boundary Differentiability Audit
{markdown_table(boundary_detail, ["audit_id", "boundary_term", "silence_route", "risk_if_open", "current_status", "residual_if_fails"])}

## No-Pole Gate Status
{markdown_table(nopole_gate, ["gate_id", "gate", "needed_for", "current_status", "gate_result"])}

## Failure Router to Residuals
{markdown_table(failure_router, ["failure_id", "failure_condition", "route_to", "residual_payload", "claim_effect"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_582", "forbidden_after_582", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is a proper engineering gate. If `C_X` is a real parent momentum map and the boundary charge vanishes, then the no-pole route has teeth. If the boundary term survives, it is not a philosophical embarrassment; it is simply edge hair, and we score it. The next checkpoint should either derive the parent momentum-map owner for `P[Y]`, `J_eff[Y]`, and `P_mem[Y]`, or demote the edge term into an explicit residual coefficient.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_validation = read_csv(PRIOR_581_VALIDATION)
    prior_summary = read_csv(PRIOR_581_SUMMARY)
    theorem_chain_581 = read_csv(THEOREM_CHAIN_581)
    certificate_581 = read_csv(CERTIFICATE_581)
    boundary_581 = read_csv(BOUNDARY_581)
    constraint_581 = read_csv(CONSTRAINT_581)
    fallback_581 = read_csv(FALLBACK_581)

    momentum_theorem = make_momentum_theorem()
    dirac_audit = make_dirac_audit()
    boundary_detail = make_boundary_detail()
    nopole_gate = make_nopole_gate()
    failure_router = make_failure_router()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        momentum_theorem,
        dirac_audit,
        boundary_detail,
        nopole_gate,
        failure_router,
        decisions,
    )

    summary_rows = [
        {
            "summary_id": "S582_0_result",
            "status": STATUS,
            "momentum_map_gate_written": "true",
            "parent_momentum_map_owner_derived": "false",
            "boundary_charge_silenced": "false",
            "bracket_closure_computed": "false",
            "no_pole_theorem_claim": "false",
            "finite_branch_retained": "true",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "theorem_chain_rows_reused": len(theorem_chain_581),
            "certificate_rows_reused": len(certificate_581),
            "boundary_rows_reused": len(boundary_581),
            "constraint_rows_reused": len(constraint_581),
            "fallback_rows_reused": len(fallback_581),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        MOMENTUM_THEOREM_PATH,
        momentum_theorem,
        ["theorem_id", "claim", "mathematical_form", "required_input", "result_if_true", "current_status", "valid_for_claim"],
    )
    write_csv(
        DIRAC_AUDIT_PATH,
        dirac_audit,
        ["audit_id", "object", "test", "required_pass", "current_status", "verdict", "valid_for_claim"],
    )
    write_csv(
        BOUNDARY_DETAIL_PATH,
        boundary_detail,
        ["audit_id", "boundary_term", "silence_route", "risk_if_open", "current_status", "residual_if_fails"],
    )
    write_csv(NOPOLE_GATE_PATH, nopole_gate, ["gate_id", "gate", "needed_for", "current_status", "gate_result"])
    write_csv(
        FAILURE_ROUTER_PATH,
        failure_router,
        ["failure_id", "failure_condition", "route_to", "residual_payload", "claim_effect"],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update, ["route_id", "allowed_after_582", "forbidden_after_582", "next_action"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "momentum_map_gate_written",
            "parent_momentum_map_owner_derived",
            "boundary_charge_silenced",
            "bracket_closure_computed",
            "no_pole_theorem_claim",
            "finite_branch_retained",
            "claim_allowed",
            "R10_pass_for_claim",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "theorem_chain_rows_reused",
            "certificate_rows_reused",
            "boundary_rows_reused",
            "constraint_rows_reused",
            "fallback_rows_reused",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        momentum_theorem,
        dirac_audit,
        boundary_detail,
        nopole_gate,
        failure_router,
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
                "momentum_map_gate_written": True,
                "parent_momentum_map_owner_derived": False,
                "boundary_charge_silenced": False,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
