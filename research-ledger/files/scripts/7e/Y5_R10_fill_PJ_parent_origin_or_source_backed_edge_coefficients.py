from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md"

PRIOR_591_VALIDATION = RESIDUALS / "P8_Y5_BRR545_591_VALIDATION.csv"
PRIOR_591_EDGE_INPUT = RESIDUALS / "P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_592_SOURCE_REGISTER.csv"
NOETHER_FORMULA_PATH = RESIDUALS / "P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv"
PJ_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv"
AMBIGUITY_GATE_PATH = RESIDUALS / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv"
EDGE_SOURCE_PLAN_PATH = RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_592_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_592_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_592_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_592_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_PJ_Noether_origin_formula_derived_conditionally_current_parent_action_missing_edge_coefficients_still_unsourced"
CLAIM_CEILING = "Noether_PJ_origin_template_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "593-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md"

SOURCE_FILES = [
    ("591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md", "immediate P/J parent-origin target"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_591_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv", "formal DC operator"),
    ("source-intake/mts_residuals/P8_Y5_R10_591_DCDAGGER_FORMULA.csv", "formal DCdagger operator"),
    ("source-intake/mts_residuals/P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv", "P/J/Omega comparison blockers"),
    ("source-intake/mts_residuals/P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv", "edge coefficient source status"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv", "Noether/momentum-map owner contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv", "parent owner attempts"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map owner fork"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "Euler-Ward/stress source route"),
    ("538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md", "Euler-Ward chain"),
    ("590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md", "DCdagger symplectic-flat map"),
    ("scripts/Y5_R10_fill_PJ_parent_origin_or_source_backed_edge_coefficients.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
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


def source_register() -> list[dict[str, Any]]:
    return [
        {"source_file": source_file, "exists": str((ROOT / source_file).exists()), "role": role}
        for source_file, role in SOURCE_FILES
    ]


def make_noether_formula() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "NPJ592_0_parent_variation",
            "statement": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y)",
            "meaning": "P and J can be parent-owned only after theta_Y is explicit",
            "derived_status": "standard_variational_identity",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "NPJ592_1_vertical_quasi_symmetry",
            "statement": "delta_X Y^A = R^A_nu[Y] X^nu + R^{A mu}_nu[Y] nabla_mu X^nu + ... and delta_X L_parent=d mu_X",
            "meaning": "the vertical transformation must be a parent symmetry/quotient direction, not a post-readout closure",
            "derived_status": "conditional_symmetry_template",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "NPJ592_2_Noether_current",
            "statement": "j_X = theta_Y(v_X)-mu_X",
            "meaning": "the current is the single object from which both P and J must be read",
            "derived_status": "standard_Noether_definition",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "NPJ592_3_PJ_split",
            "statement": "j_X = X_nu J_eff^nu + (nabla_mu X_nu) P^{mu nu} + dB_improvement",
            "meaning": "P is the coefficient of nabla X; J_eff is the coefficient of X in the same current",
            "derived_status": "conditional_PJ_origin_formula",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "NPJ592_4_constraint_density",
            "statement": "j_X = X_nu(-nabla_mu P^{mu nu}+J_eff^nu)+d(X_nu P^{mu nu} dSigma_mu+B_improvement)",
            "meaning": "C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu is owned only if this integration-by-parts comes from j_X",
            "derived_status": "formal_derivation_of_CX_from_current",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "NPJ592_5_momentum_map_condition",
            "statement": "delta int_Sigma X_nu C_X^nu + delta Q_X = Omega_Y(delta Y,v_X)",
            "meaning": "the P/J split must also match the symplectic-flat vertical generator from 590",
            "derived_status": "closure_condition",
            "valid_for_claim": "false",
        },
    ]


def make_pj_attempts() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PJA592_0_GR_EH_template",
            "candidate_parent_origin": "EH plus matter diffeomorphism Noether current",
            "P_origin": "superpotential/boundary coefficient in Q_xi or ADM momentum constraint",
            "J_origin": "matter and gravitational constraint density from same diffeomorphism current",
            "test_result": "standard_template_only",
            "blocker": "not yet instantiated as the MTS parent action with MTS P,J symbols",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PJA592_1_affine_Vdef_block",
            "candidate_parent_origin": "S_X=int P^{mu nu}(nabla_mu X_nu-A_mu_nu)+X_nu J_eff^nu",
            "P_origin": "coefficient of nabla X by construction",
            "J_origin": "coefficient of X by construction",
            "test_result": "not_parent_origin",
            "blocker": "this only names P and J unless P,J,A are derived from S0/theta_Y",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PJA592_2_GK_stress_Ward_route",
            "candidate_parent_origin": "T_GK Hilbert stress sector from 513",
            "P_origin": "possible improvement/superpotential of stress-divergence current",
            "J_origin": "Euler-Ward source term sum_A E_A nabla^nu Phi^A",
            "test_result": "promising_for_J_not_P",
            "blocker": "S_GK and Helmholtz/integrability proof still absent; P superpotential not identified",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PJA592_3_memory_domain_relative_current",
            "candidate_parent_origin": "relative memory/domain current with P_mem and exact boundary primitive",
            "P_origin": "relative superpotential or projector boundary coefficient",
            "J_origin": "relative/source current S_L+d_rel(P_mem J_rel)",
            "test_result": "not_closed",
            "blocker": "P_mem stress, relative primitive, and local branch exactness are not derived",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PJA592_4_independent_PJ",
            "candidate_parent_origin": "declare P and J independently",
            "P_origin": "free tensor",
            "J_origin": "inserted current",
            "test_result": "rejected",
            "blocker": "moves the closure assumption into symbols and gives no theorem credit",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PJA592_5_current_verdict",
            "candidate_parent_origin": "one current j_X producing P and J",
            "P_origin": "coefficient of nabla X in theta(v_X)-mu_X",
            "J_origin": "coefficient of X in theta(v_X)-mu_X",
            "test_result": "formula_derived_but_not_filled",
            "blocker": "current corpus still lacks explicit L_parent, theta_Y, mu_X and v_X",
            "valid_for_claim": "false",
        },
    ]


def make_ambiguity_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "IAG592_0_superpotential_improvement",
            "ambiguity": "P^{mu nu}->P^{mu nu}+nabla_rho S^{rho mu nu}",
            "risk": "same C_X in bulk but different edge charge Q_X",
            "required_fix": "parent boundary/reference choice must fix the representative",
            "status": "open",
        },
        {
            "gate_id": "IAG592_1_current_improvement",
            "ambiguity": "j_X->j_X+dB_X",
            "risk": "bulk P/J split shifts while boundary alpha_edge changes",
            "required_fix": "differentiable Hamiltonian generator with fixed Q_X",
            "status": "open",
        },
        {
            "gate_id": "IAG592_2_density_convention",
            "ambiguity": "P tensor versus densitized Ptilde",
            "risk": "DC and DCdagger connection terms change",
            "required_fix": "choose convention from parent theta/current before computing DCdagger",
            "status": "open",
        },
        {
            "gate_id": "IAG592_3_on_shell_trivial_current",
            "ambiguity": "Noether current can be shifted by Euler-equation terms",
            "risk": "J_eff may vanish on shell but not as an off-shell generator coefficient",
            "required_fix": "off-shell current decomposition and constraint algebra",
            "status": "open",
        },
        {
            "gate_id": "IAG592_4_matter_improper_charge",
            "ambiguity": "improper boundary symmetries carry physical mass/rotation charge",
            "risk": "vertical X accidentally eats real ADM/Hamiltonian charges",
            "required_fix": "proper vertical domain and Pi_M^H edge projection audit",
            "status": "open",
        },
    ]


def make_edge_plan(edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in edge_rows:
        out.append(
            {
                "plan_id": f"ESP592_{len(out)}",
                "edge_row_id": row["edge_row_id"],
                "lambda_um": row["lambda_um"],
                "alpha_edge_ceiling": row["alpha_edge_ceiling"],
                "coefficient_needed": "K_edge;Qbar_edge_XH;qbar_XT",
                "source_status": row["current_source_status"],
                "acceptable_source": "parent theorem-zero, parent kernel/projection coefficient, or external source-backed numeric bound",
                "current_status": "missing" if "missing" in row["current_source_status"] else "diagnostic_only",
                "valid_for_claim": "false",
            }
        )
    return out


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D592_0_Noether_PJ_formula_derived",
            "decision": "P and J_eff can be parent-owned only as coefficients of one Noether current j_X=theta(v_X)-mu_X",
            "meaning": "P is coefficient of nabla X; J_eff is coefficient of X; C_X follows by integration by parts",
            "claim_status": "conditional_formula_not_filled",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D592_1_current_MTS_PJ_not_filled",
            "decision": "current corpus still lacks L_parent, theta_Y, mu_X, and v_X needed to extract P and J",
            "meaning": "affine Vdef names P/J but does not derive them from the pre-existing parent action",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D592_2_edge_coefficients_still_missing",
            "decision": "source-backed edge coefficients remain absent",
            "meaning": "fallback requires K_edge, Qbar_edge_XH, and qbar_XT or theorem-zero rows",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU592_0_allowed",
            "allowed_after_592": "use j_X=theta(v_X)-mu_X as the exact P/J origin contract",
            "forbidden_after_592": "count P/J as parent-owned because they appear in affine Vdef",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU592_1_allowed",
            "allowed_after_592": "try to fill minimal L_parent, theta_Y, mu_X, and v_X",
            "forbidden_after_592": "ignore improvement ambiguity in P and Q_X",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU592_2_allowed",
            "allowed_after_592": "switch to source-backed edge coefficients if the parent current cannot be filled",
            "forbidden_after_592": "mark diagnostic edge coefficients valid_for_claim",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S592_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "P/J origin has an exact Noether contract now, but it is not filled. The branch needs L_parent, theta, mu_X, v_X, and a fixed boundary representative.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    pj_rows: list[dict[str, Any]],
    ambiguity_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_591_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in formula_rows if row["valid_for_claim"] == "true"],
        *[row for row in pj_rows if row["valid_for_claim"] == "true"],
        *[row for row in edge_rows if row["valid_for_claim"] == "true"],
    ]
    has_split = any(row["formula_id"] == "NPJ592_3_PJ_split" for row in formula_rows)
    has_constraint = any(row["formula_id"] == "NPJ592_4_constraint_density" for row in formula_rows)
    rejected_independent = any(row["attempt_id"] == "PJA592_4_independent_PJ" and row["test_result"] == "rejected" for row in pj_rows)
    ambiguity_open = all(row["status"] == "open" for row in ambiguity_rows)
    edge_missing = any(row["current_status"] == "missing" for row in edge_rows)
    return [
        {
            "check_id": "V592_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V592_1_prior_591_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V592_2_Noether_PJ_split_written",
            "result": "pass" if has_split and has_constraint else "fail",
            "detail": f"formula_rows={len(formula_rows)}",
        },
        {
            "check_id": "V592_3_independent_PJ_rejected",
            "result": "pass" if rejected_independent else "fail",
            "detail": "independent P/J gets no theorem credit",
        },
        {
            "check_id": "V592_4_improvement_ambiguity_retained",
            "result": "pass" if ambiguity_rows and ambiguity_open else "fail",
            "detail": f"ambiguity_rows={len(ambiguity_rows)};all_open={ambiguity_open}",
        },
        {
            "check_id": "V592_5_edge_coefficients_still_nonclaim",
            "result": "pass" if edge_rows and edge_missing and not any(row["valid_for_claim"] == "true" for row in edge_rows) else "fail",
            "detail": f"edge_rows={len(edge_rows)};edge_missing={edge_missing}",
        },
        {
            "check_id": "V592_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V592_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    pj_rows: list[dict[str, Any]],
    ambiguity_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 592 Y5 R10 fill PJ parent origin or source-backed edge coefficients

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The derivation gives a clean contract: `P` and `J_eff` must be read from one Noether current `j_X=theta_Y(v_X)-mu_X`.
- The required split is `j_X = X_nu J_eff^nu + (nabla_mu X_nu)P^{{mu nu}} + dB`, so integration by parts gives `C_X^nu=-nabla_mu P^{{mu nu}}+J_eff^nu`.
- This is useful, but it is not filled for current MTS: we still need explicit `L_parent`, `theta_Y`, `mu_X`, `v_X`, and a fixed boundary representative.
- Independent `P`/`J` is rejected as theorem credit; source-backed edge coefficients are still missing.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Noether PJ Origin Formula
{markdown_table(formula_rows, ["formula_id", "statement", "meaning", "derived_status", "valid_for_claim"])}

## PJ Parent Origin Attempt
{markdown_table(pj_rows, ["attempt_id", "candidate_parent_origin", "P_origin", "J_origin", "test_result", "blocker", "valid_for_claim"])}

## Improvement Ambiguity Gate
{markdown_table(ambiguity_rows, ["gate_id", "ambiguity", "risk", "required_fix", "status"])}

## Edge Coefficient Source Plan
{markdown_table(edge_rows, ["plan_id", "edge_row_id", "lambda_um", "alpha_edge_ceiling", "coefficient_needed", "source_status", "acceptable_source", "current_status", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_592", "forbidden_after_592", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is exactly the sort of fork we want. The theorem route now has a precise parent-origin contract, not a vibe: give me `L_parent`, `theta`, `mu_X`, and `v_X`, and I can extract `P/J`. Without those, affine `V_def` is only a naming layer and the honest move is edge coefficients.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    prior_edge_rows = read_csv(PRIOR_591_EDGE_INPUT)
    formula_rows = make_noether_formula()
    pj_rows = make_pj_attempts()
    ambiguity_rows = make_ambiguity_gate()
    edge_rows = make_edge_plan(prior_edge_rows)
    decision_rows = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, formula_rows, pj_rows, ambiguity_rows, edge_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        NOETHER_FORMULA_PATH,
        formula_rows,
        ["formula_id", "statement", "meaning", "derived_status", "valid_for_claim"],
    )
    write_csv(
        PJ_ATTEMPT_PATH,
        pj_rows,
        ["attempt_id", "candidate_parent_origin", "P_origin", "J_origin", "test_result", "blocker", "valid_for_claim"],
    )
    write_csv(AMBIGUITY_GATE_PATH, ambiguity_rows, ["gate_id", "ambiguity", "risk", "required_fix", "status"])
    write_csv(
        EDGE_SOURCE_PLAN_PATH,
        edge_rows,
        [
            "plan_id",
            "edge_row_id",
            "lambda_um",
            "alpha_edge_ceiling",
            "coefficient_needed",
            "source_status",
            "acceptable_source",
            "current_status",
            "valid_for_claim",
        ],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_592", "forbidden_after_592", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["summary_id", "claim_allowed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "best_private_read", "next_target"],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        formula_rows,
        pj_rows,
        ambiguity_rows,
        edge_rows,
        decision_rows,
        route_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
