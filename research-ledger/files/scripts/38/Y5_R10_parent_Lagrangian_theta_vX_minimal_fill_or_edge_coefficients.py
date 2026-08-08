from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "593-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md"

PRIOR_592_VALIDATION = RESIDUALS / "P8_Y5_BRR545_592_VALIDATION.csv"
PRIOR_592_EDGE_PLAN = RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_593_SOURCE_REGISTER.csv"
FILL_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_593_MINIMAL_PARENT_FILL_CANDIDATES.csv"
THETA_FORMS_PATH = RESIDUALS / "P8_Y5_R10_593_THETA_MU_VX_FILLED_FORMS.csv"
PJ_EXTRACTION_PATH = RESIDUALS / "P8_Y5_R10_593_PJ_EXTRACTION_TEST.csv"
EDGE_INPUT_PATH = RESIDUALS / "P8_Y5_R10_593_EDGE_COEFFICIENT_INPUT_ROWS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_593_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_593_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_593_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_593_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_minimal_parent_fill_attempt_written_diffeo_and_quotient_routes_conditional_affine_route_rejected_edge_coefficients_missing"
CLAIM_CEILING = "minimal_L_theta_mu_vX_fill_attempt_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "594-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md"

SOURCE_FILES = [
    ("592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md", "immediate Noether P/J origin handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_592_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv", "Noether P/J origin formula"),
    ("source-intake/mts_residuals/P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv", "P/J parent-origin attempts"),
    ("source-intake/mts_residuals/P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv", "improvement ambiguity gates"),
    ("source-intake/mts_residuals/P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv", "edge coefficient source plan"),
    ("511-minimal-parent-action-local-GR-fixed-point-ansatz.md", "minimal EH plus silent parent action contract"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "strict quotient no-pole theorem shape"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map/edge fork"),
    ("590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md", "DCdagger symplectic-flat map"),
    ("591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md", "formal DC/Omega formulas"),
    ("scripts/Y5_R10_parent_Lagrangian_theta_vX_minimal_fill_or_edge_coefficients.py", "this checkpoint generator"),
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


def make_fill_candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "MPF593_A_diffeomorphism_parent",
            "L_parent": "L_EH[g]+L_silent[g,Phi]+L_matter[psi,hat_g(q(Y))]+dB_ref",
            "vX": "v_X[Y]=Lie_X Y on metric/coframe, extra fields, and matter representatives",
            "theta": "theta_parent=theta_EH+theta_silent+theta_matter+delta B_ref",
            "mu_X": "mu_X=i_X L_parent for a diffeomorphism-covariant Lagrangian",
            "what_it_fills": "standard Noether current j_X=theta(L_XY)-i_XL",
            "claim_result": "conditional_template_only",
            "blocker": "must prove MTS C_X is this diffeomorphism/momentum constraint, not a separate defect closure",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MPF593_B_strict_quotient_zero",
            "L_parent": "L_red[pi(Y)] with d pi(v_X)=0 and matter also factors through pi",
            "vX": "v_X is vertical to the observed quotient, not an ordinary spacetime diffeomorphism",
            "theta": "theta_Y(v_X)=0 up to exact terms because the action factors through pi",
            "mu_X": "mu_X=0 or exact improvement after quotient factorization",
            "what_it_fills": "P=0 and J_eff=0 theorem-zero rather than nonzero P/J",
            "claim_result": "best_no_pole_if_pi_is_constructed",
            "blocker": "parent quotient map pi and matter functor blindness are not explicit",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MPF593_C_affine_topological_block",
            "L_parent": "L0[Y]+P^{mu nu}(nabla_mu X_nu-A_mu_nu[Y])+X_nu J_eff^nu[Y]",
            "vX": "shift or multiplier variation of X",
            "theta": "theta_X^mu=P^{mu nu} delta X_nu plus possible parent theta0",
            "mu_X": "chosen so the affine block is invariant only after P/J equations",
            "what_it_fills": "P and J appear as coefficients by construction",
            "claim_result": "rejected_as_parent_origin",
            "blocker": "P/J are inserted unless derived from L0, theta0, and v_X before this block",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MPF593_D_EH_plus_quotient_extra",
            "L_parent": "L_EH[g_obs]+L_extra[g_obs,Phi_red]+L_matter[psi,g_obs] with Y=(representatives,pi(Y))",
            "vX": "Lie_X on representative variables but v_X[g_obs]=0 and v_X[Phi_red]=0",
            "theta": "theta_EH sees only quotient fields; representative-sector theta must be exact/topological",
            "mu_X": "zero/exact for representative-only vertical moves",
            "what_it_fills": "tries to combine local GR metric with strict vertical MTS redundancy",
            "claim_result": "promising_hybrid_contract",
            "blocker": "needs explicit representative/quotient split for MTS motion-time-space variables",
            "valid_for_claim": "false",
        },
    ]


def make_theta_forms() -> list[dict[str, Any]]:
    return [
        {
            "form_id": "TMV593_0_EH_theta",
            "candidate": "theta_EH^mu=(2 kappa)^-1 sqrt(-g)(nabla_nu delta g^{mu nu}-nabla^mu delta g)",
            "vX_inserted": "delta g_{mu nu}=Lie_X g_{mu nu}=2 nabla_(mu X_{nu)}",
            "current_split": "theta_EH(L_Xg)-i_X L_EH = X_nu J_EH^nu + nabla_mu X_nu P_EH^{mu nu}+dB",
            "status": "standard_GR_template",
            "missing_for_MTS": "identify MTS P/J with EH/current components or declare quotient-zero route",
            "valid_for_claim": "false",
        },
        {
            "form_id": "TMV593_1_extra_theta",
            "candidate": "theta_extra^mu=sum_A Pi_A^mu delta Phi^A plus improvement terms",
            "vX_inserted": "delta Phi^A=Lie_X Phi^A or quotient-vertical action",
            "current_split": "Pi_A^mu Lie_X Phi^A contributes X J_extra + nabla X P_extra depending on tensor type",
            "status": "formal_template",
            "missing_for_MTS": "explicit extra Lagrangian and momenta for memory/domain/projector fields",
            "valid_for_claim": "false",
        },
        {
            "form_id": "TMV593_2_matter_theta",
            "candidate": "theta_matter from matter equations or zero if matter fields fixed in local vacuum",
            "vX_inserted": "delta psi=Lie_X psi for ordinary diffeo or delta_X matter=0 for quotient vertical",
            "current_split": "diffeo route gives matter momentum/stress current; quotient route gives qbar_XT=0",
            "status": "fork_not_resolved",
            "missing_for_MTS": "matter quotient map and source-frame theorem",
            "valid_for_claim": "false",
        },
        {
            "form_id": "TMV593_3_muX",
            "candidate": "mu_X=i_X L_parent for ordinary diffeo; mu_X=0/exact for strict quotient vertical",
            "vX_inserted": "delta_X L_parent=d mu_X",
            "current_split": "fixes the subtraction in j_X=theta(v_X)-mu_X",
            "status": "conditional",
            "missing_for_MTS": "must choose diffeo route or quotient route and keep boundary charges consistent",
            "valid_for_claim": "false",
        },
    ]


def make_pj_extraction() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "PJE593_0_diffeo_extracts_PJ",
            "candidate_id": "MPF593_A_diffeomorphism_parent",
            "P_result": "P is the derivative-of-X/superpotential coefficient in the diffeo Noether current",
            "J_result": "J is the X coefficient: gravitational plus matter/extra constraint density",
            "pass_status": "conditional_pass_as_standard_geometry",
            "why_not_claim": "does not prove the MTS C_X/P/J symbols are this current",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PJE593_1_quotient_zero_extracts_zero",
            "candidate_id": "MPF593_B_strict_quotient_zero",
            "P_result": "P=0 or exact improvement",
            "J_result": "J_eff=0",
            "pass_status": "conditional_pass_if_pi_exists",
            "why_not_claim": "pi and matter quotient are not constructed",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PJE593_2_affine_block_not_origin",
            "candidate_id": "MPF593_C_affine_topological_block",
            "P_result": "P appears by declaration",
            "J_result": "J appears by declaration",
            "pass_status": "fail_as_origin",
            "why_not_claim": "naming coefficients in a new block does not derive them from parent Noether current",
            "valid_for_claim": "false",
        },
        {
            "test_id": "PJE593_3_hybrid_needs_split",
            "candidate_id": "MPF593_D_EH_plus_quotient_extra",
            "P_result": "EH P may be owned; vertical-extra P should be zero/exact",
            "J_result": "EH J may be owned; vertical-extra J should be zero",
            "pass_status": "promising_but_unfilled",
            "why_not_claim": "requires explicit observed/representative split of MTS variables",
            "valid_for_claim": "false",
        },
    ]


def make_edge_input(prior_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in prior_rows:
        out.append(
            {
                "edge_input_id": f"ECI593_{len(out)}",
                "edge_row_id": row["edge_row_id"],
                "lambda_um": row["lambda_um"],
                "alpha_edge_ceiling": row["alpha_edge_ceiling"],
                "K_edge": "MISSING_SOURCE" if row["current_status"] == "missing" else "diagnostic_only",
                "Qbar_edge_XH": "MISSING_SOURCE" if row["current_status"] == "missing" else "diagnostic_only",
                "qbar_XT": "MISSING_SOURCE" if row["current_status"] == "missing" else "diagnostic_only",
                "source_status": row["current_status"],
                "action": "source parent theorem-zero or numeric coefficient before claim",
                "valid_for_claim": "false",
            }
        )
    return out


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D593_0_minimal_fill_attempt_complete",
            "decision": "minimal L/theta/mu/vX fills are written for diffeo, quotient-zero, affine, and hybrid routes",
            "meaning": "the parent data can be filled as templates, but not yet as current-MTS proof",
            "claim_status": "nonclaim_fill_attempt",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D593_1_affine_origin_rejected",
            "decision": "affine block does not derive P/J by itself",
            "meaning": "it only names the coefficients unless L0/theta0/vX already produce them",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D593_2_best_routes_are_diffeo_or_quotient",
            "decision": "choose between ordinary diffeo current identity and strict quotient-zero current",
            "meaning": "diffeo route needs C_X identity; quotient route needs pi and matter blindness",
            "claim_status": "fork_open",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D593_3_edge_coefficients_still_missing",
            "decision": "edge coefficient fallback remains unsourced",
            "meaning": "K_edge, Qbar_edge_XH, and qbar_XT are not filled",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU593_0_allowed",
            "allowed_after_593": "use ordinary diffeomorphism Noether current as a conditional template",
            "forbidden_after_593": "claim it is the MTS vertical defect current without proving C_X equality",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU593_1_allowed",
            "allowed_after_593": "use strict quotient-zero as the clean no-pole target",
            "forbidden_after_593": "claim quotient-zero without explicit pi and matter blindness",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU593_2_allowed",
            "allowed_after_593": "reject affine-only P/J origin as theorem credit",
            "forbidden_after_593": "count declared affine coefficients as derived parent data",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S593_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "The minimal parent data can be filled as templates. The next decisive fork is diffeo-current identity versus strict quotient-zero; affine-only origin is rejected.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    theta_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_592_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in candidates if row["valid_for_claim"] == "true"],
        *[row for row in theta_rows if row["valid_for_claim"] == "true"],
        *[row for row in extraction_rows if row["valid_for_claim"] == "true"],
        *[row for row in edge_rows if row["valid_for_claim"] == "true"],
    ]
    has_diffeo = any(row["candidate_id"] == "MPF593_A_diffeomorphism_parent" for row in candidates)
    has_quotient = any(row["candidate_id"] == "MPF593_B_strict_quotient_zero" for row in candidates)
    affine_rejected = any(row["candidate_id"] == "MPF593_C_affine_topological_block" and "rejected" in row["claim_result"] for row in candidates)
    extraction_blocks = any(row["pass_status"] == "fail_as_origin" for row in extraction_rows)
    edge_missing = any(row["K_edge"] == "MISSING_SOURCE" for row in edge_rows)
    return [
        {
            "check_id": "V593_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V593_1_prior_592_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V593_2_diffeo_and_quotient_candidates_present",
            "result": "pass" if has_diffeo and has_quotient else "fail",
            "detail": f"candidates={len(candidates)};diffeo={has_diffeo};quotient={has_quotient}",
        },
        {
            "check_id": "V593_3_affine_origin_rejected",
            "result": "pass" if affine_rejected and extraction_blocks else "fail",
            "detail": "affine coefficients do not count as parent origin",
        },
        {
            "check_id": "V593_4_theta_mu_vX_forms_nonclaim",
            "result": "pass" if theta_rows and not any(row["valid_for_claim"] == "true" for row in theta_rows) else "fail",
            "detail": f"theta_rows={len(theta_rows)}",
        },
        {
            "check_id": "V593_5_edge_coefficients_still_nonclaim",
            "result": "pass" if edge_rows and edge_missing and not any(row["valid_for_claim"] == "true" for row in edge_rows) else "fail",
            "detail": f"edge_rows={len(edge_rows)};edge_missing={edge_missing}",
        },
        {
            "check_id": "V593_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V593_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    theta_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 593 Y5 R10 parent Lagrangian theta vX minimal fill or edge coefficients

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- Minimal parent data can be filled as templates, but not yet as current-MTS proof.
- The ordinary diffeomorphism fill gives standard `L`, `theta`, `mu_X=i_XL`, and `v_X=Lie_X`, but we still must prove MTS `C_X` is exactly that constraint/current.
- The strict quotient fill is cleaner for no-pole: if `L_parent=L_red[pi(Y)]` and `d pi(v_X)=0`, then `P=J=0` up to exact terms. But `pi` and matter blindness are not built.
- The affine block is rejected as a parent origin: it declares `P/J`; it does not derive them.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Minimal Parent Fill Candidates
{markdown_table(candidates, ["candidate_id", "L_parent", "vX", "theta", "mu_X", "what_it_fills", "claim_result", "blocker", "valid_for_claim"])}

## Theta Mu vX Filled Forms
{markdown_table(theta_rows, ["form_id", "candidate", "vX_inserted", "current_split", "status", "missing_for_MTS", "valid_for_claim"])}

## PJ Extraction Test
{markdown_table(extraction_rows, ["test_id", "candidate_id", "P_result", "J_result", "pass_status", "why_not_claim", "valid_for_claim"])}

## Edge Coefficient Input Rows
{markdown_table(edge_rows, ["edge_input_id", "edge_row_id", "lambda_um", "alpha_edge_ceiling", "K_edge", "Qbar_edge_XH", "qbar_XT", "source_status", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_593", "forbidden_after_593", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a useful fork, chume. The theory route is not dead; it has two honest doors. Door one: prove MTS `C_X` is just the parent diffeomorphism/momentum current in disguise. Door two: construct the quotient map `pi` so the vertical sector is theorem-zero. The affine door is painted on the wall unless `P/J` are already sourced upstream.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    edge_plan_rows = read_csv(PRIOR_592_EDGE_PLAN)
    candidates = make_fill_candidates()
    theta_rows = make_theta_forms()
    extraction_rows = make_pj_extraction()
    edge_rows = make_edge_input(edge_plan_rows)
    decision_rows = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, candidates, theta_rows, extraction_rows, edge_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        FILL_CANDIDATES_PATH,
        candidates,
        ["candidate_id", "L_parent", "vX", "theta", "mu_X", "what_it_fills", "claim_result", "blocker", "valid_for_claim"],
    )
    write_csv(
        THETA_FORMS_PATH,
        theta_rows,
        ["form_id", "candidate", "vX_inserted", "current_split", "status", "missing_for_MTS", "valid_for_claim"],
    )
    write_csv(
        PJ_EXTRACTION_PATH,
        extraction_rows,
        ["test_id", "candidate_id", "P_result", "J_result", "pass_status", "why_not_claim", "valid_for_claim"],
    )
    write_csv(
        EDGE_INPUT_PATH,
        edge_rows,
        ["edge_input_id", "edge_row_id", "lambda_um", "alpha_edge_ceiling", "K_edge", "Qbar_edge_XH", "qbar_XT", "source_status", "action", "valid_for_claim"],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_593", "forbidden_after_593", "next_action"])
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
        candidates,
        theta_rows,
        extraction_rows,
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
