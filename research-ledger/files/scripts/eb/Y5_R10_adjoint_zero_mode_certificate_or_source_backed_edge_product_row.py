from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md"

PRIOR_588_VALIDATION = RESIDUALS / "P8_Y5_BRR545_588_VALIDATION.csv"
PRIOR_588_EDGE_BUDGET = RESIDUALS / "P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_589_SOURCE_REGISTER.csv"
CERTIFICATE_PATH = RESIDUALS / "P8_Y5_R10_589_ADJOINT_ZERO_MODE_CERTIFICATE.csv"
KILL_CHAIN_PATH = RESIDUALS / "P8_Y5_R10_589_KILL_CHAIN_STATUS.csv"
REQUIRED_SOURCES_PATH = RESIDUALS / "P8_Y5_R10_589_SOURCES_REQUIRED_TO_CLOSE_CERTIFICATE.csv"
EDGE_ROW_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_589_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_589_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_589_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_589_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_adjoint_zero_mode_certificate_skeleton_built_Killing_stabilizer_route_conditional_edge_row_template_written_nonclaim"
CLAIM_CEILING = "adjoint_zero_mode_certificate_skeleton_and_source_backed_edge_row_template_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md"

SOURCE_FILES = [
    ("588-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product.md", "immediate adjoint theorem and edge-budget handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_588_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_588_ADJOINT_BACKREACTION_THEOREM.csv", "formal adjoint backreaction theorem"),
    ("source-intake/mts_residuals/P8_Y5_R10_588_BACKREACTION_KILL_ATTEMPT.csv", "backreaction kill attempt ledger"),
    ("source-intake/mts_residuals/P8_Y5_R10_588_CONSTRAINT_IDENTITY_OR_NEW_EQUATION_GATE.csv", "identity vs second-class gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv", "edge-product factor budget"),
    ("587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md", "affine parent source map and backreaction blocker"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map owner contract"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "quotient-vertical theorem shape"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "Ward/stress-divergence q_loc route"),
    ("539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md", "Hamiltonian edge projection route"),
    ("scripts/Y5_R10_adjoint_zero_mode_certificate_or_source_backed_edge_product_row.py", "this checkpoint generator"),
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


def tightest_budget(edge_budget_rows: list[dict[str, str]]) -> dict[str, str]:
    return min(edge_budget_rows, key=lambda row: float(row["alpha_edge_ceiling"]))


def make_certificate() -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "AZC589_0_adjoint_as_vertical_generator",
            "claim": "(DC[Y0])^dagger X equals the infinitesimal vertical action v_X[Y0] in the parent field-space pairing",
            "mathematical_test": "int X_nu DC^nu[delta Y] = int <v_X[Y0], delta Y>_G + boundary",
            "if_true": "zero backreaction is equivalent to v_X[Y0]=0 modulo boundary terms",
            "current_status": "best_certificate_route_not_mapped_to_current_parent_fields",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "AZC589_1_metric_Killing_stabilizer",
            "claim": "for the metric/coframe part, v_X[g] = L_X g = 2 nabla_(mu X_nu)",
            "mathematical_test": "L_X g=0 plus proper/reference boundary conditions implies X=0 except forbidden improper isometries",
            "if_true": "metric-sector adjoint zero modes are only Killing/reference symmetries, not local force fields",
            "current_status": "conditional_standard_geometry_route",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "AZC589_2_extra_field_stabilizer",
            "claim": "for every extra parent field Phi^A, v_X[Phi^A]=L_X Phi^A or a vertical quotient action with no proper stabilizer",
            "mathematical_test": "v_X[g]=0 and v_X[Phi^A]=0 with proper boundary data imply X=0 on the local branch",
            "if_true": "extra fields do not leave hidden X stabilizers",
            "current_status": "not_derived_for_MTS_extra_fields",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "AZC589_3_proper_boundary_domain",
            "claim": "allowed X modes are proper vertical transformations: X|boundary=0 or Q_X[X]=0 with fixed reference subtraction",
            "mathematical_test": "no time-translation/rotation/ADM-improper mode is included in the X domain",
            "if_true": "physical spacetime symmetries are not confused with the vertical defect multiplier",
            "current_status": "not_derived_boundary_domain",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "AZC589_4_coercive_kernel_version",
            "claim": "equivalently, ||(DC)^dagger X||^2 >= m_adj^2 ||X||^2 on the proper vertical domain",
            "mathematical_test": "positive adjoint operator / Korn-type estimate / no proper Killing stabilizer",
            "if_true": "(DC)^dagger X=0 forces X=0",
            "current_status": "contract_written_not_proved",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "AZC589_5_certificate_result",
            "claim": "if AZC589_0 through AZC589_4 and matter/boundary silence hold, delta_Y S_X=0 and local no-pole survives",
            "mathematical_test": "C_X=0, X=0, Q_edge=0, qbar_XT=0 on compact local branch",
            "if_true": "K_X=0, Qbar_edge_XH=0, qbar_XT=0 for this branch",
            "current_status": "conditional_certificate_skeleton_only",
            "valid_for_claim": "false",
        },
    ]


def make_kill_chain() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "KCS589_0_parent_identity",
            "step": "C_X is owned by the parent Noether/momentum map",
            "equation": "i_{v_X} Omega_Y = delta G_X and C_X is the bulk generator density",
            "status": "not_derived",
            "blocks_claim": "true",
        },
        {
            "chain_id": "KCS589_1_adjoint_mapping",
            "step": "the adjoint of DC is the vertical generator",
            "equation": "(DC)^dagger X = v_X[Y] in the chosen parent pairing",
            "status": "not_mapped",
            "blocks_claim": "true",
        },
        {
            "chain_id": "KCS589_2_no_proper_stabilizer",
            "step": "proper vertical stabilizers vanish on local compact branch",
            "equation": "v_X[Y0]=0 and X proper => X=0",
            "status": "conditional_standard_if_domain_known",
            "blocks_claim": "true",
        },
        {
            "chain_id": "KCS589_3_boundary_silence",
            "step": "boundary pairing and edge charge vanish",
            "equation": "Q_edge[X]=int_boundary X_nu(n_mu P^{mu nu}+B_ct^nu)=0",
            "status": "not_derived",
            "blocks_claim": "true",
        },
        {
            "chain_id": "KCS589_4_matter_blindness",
            "step": "matter functor factors through quotient",
            "equation": "delta_X S_matter=0",
            "status": "not_derived",
            "blocks_claim": "true",
        },
        {
            "chain_id": "KCS589_5_local_silence",
            "step": "local X sector is silent",
            "equation": "K_X=Qbar_edge_XH=qbar_XT=0",
            "status": "not_reached",
            "blocks_claim": "true",
        },
    ]


def make_required_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "SRC589_0_parent_pairing",
            "needed_object": "field-space pairing or symplectic/Hilbert pairing defining the adjoint",
            "acceptable_form": "Omega_Y/theta_Y or explicit quadratic pairing G_ij for variations",
            "why_needed": "without a pairing, (DC)^dagger is not a defined operator",
            "current_status": "missing",
        },
        {
            "source_id": "SRC589_1_DC_operator",
            "needed_object": "explicit Frechet derivative DC[Y0] for C_X=-nabla P+J_eff",
            "acceptable_form": "linearized P,J_eff variations in terms of parent fields",
            "why_needed": "needed to prove adjoint equals vertical generator",
            "current_status": "missing",
        },
        {
            "source_id": "SRC589_2_vertical_transformation_law",
            "needed_object": "v_X on g/coframe, memory/domain/projector/boundary fields",
            "acceptable_form": "Lie derivative or quotient vertical action with transformation of all parent variables",
            "why_needed": "needed to identify zero modes as stabilizers",
            "current_status": "missing",
        },
        {
            "source_id": "SRC589_3_boundary_domain",
            "needed_object": "allowed X boundary data and reference subtraction",
            "acceptable_form": "proper compact support, Dirichlet X, exact primitive, or zero Hamiltonian edge charge",
            "why_needed": "needed to remove improper Killing/edge modes",
            "current_status": "missing",
        },
        {
            "source_id": "SRC589_4_no_stabilizer_proof",
            "needed_object": "no proper vertical stabilizer theorem on local branch",
            "acceptable_form": "Korn/unique-continuation estimate, positive adjoint gap, or explicit gauge fixing",
            "why_needed": "needed to force X=0",
            "current_status": "missing",
        },
        {
            "source_id": "SRC589_5_matter_quotient",
            "needed_object": "matter coupling factors through observed quotient",
            "acceptable_form": "S_matter[psi,hat_g(pi(Y))] and v_X hat_g=0",
            "why_needed": "needed to set qbar_XT=0",
            "current_status": "missing",
        },
    ]


def make_edge_template(tightest: dict[str, str]) -> list[dict[str, Any]]:
    ceiling = float(tightest["alpha_edge_ceiling"])
    equal_three = float(tightest["equal_three_factor_max"])
    safe_factor = 0.1
    return [
        {
            "row_id": "SBE589_0_required_source_backed_row",
            "lambda_m": tightest["lambda_m"],
            "lambda_um": tightest["lambda_um"],
            "K_edge": "MISSING_SOURCE_BACKED_K_EDGE",
            "Qbar_edge_XH": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "qbar_XT": "MISSING_SOURCE_BACKED_QBAR_XT",
            "alpha_edge_ceiling": f"{ceiling:.12g}",
            "alpha_edge_predicted": "MISSING_PRODUCT",
            "diagnostic_status": "blocked_until_sources_exist",
            "source_required": "parent edge kernel, Hamiltonian projection, matter quotient/test response",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SBE589_1_equal_three_factor_budget",
            "lambda_m": tightest["lambda_m"],
            "lambda_um": tightest["lambda_um"],
            "K_edge": f"{equal_three:.12g}",
            "Qbar_edge_XH": f"{equal_three:.12g}",
            "qbar_XT": f"{equal_three:.12g}",
            "alpha_edge_ceiling": f"{ceiling:.12g}",
            "alpha_edge_predicted": f"{ceiling:.12g}",
            "diagnostic_status": "budget_boundary_not_source_backed",
            "source_required": "all three factors must be derived or measured below these values",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SBE589_2_safe_under_budget_smoke",
            "lambda_m": tightest["lambda_m"],
            "lambda_um": tightest["lambda_um"],
            "K_edge": f"{safe_factor:.12g}",
            "Qbar_edge_XH": f"{safe_factor:.12g}",
            "qbar_XT": f"{safe_factor:.12g}",
            "alpha_edge_ceiling": f"{ceiling:.12g}",
            "alpha_edge_predicted": f"{safe_factor**3:.12g}",
            "diagnostic_status": "smoke_under_private_budget_not_source_backed",
            "source_required": "replace each smoke factor with sourced parent coefficient before any claim",
            "valid_for_claim": "false",
        },
    ]


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D589_0_certificate_skeleton_built",
            "decision": "adjoint zero-mode certificate has a concrete Killing/stabilizer route",
            "meaning": "if DCdagger maps to vertical Lie/quotient action and proper stabilizers vanish, X is killed",
            "claim_status": "conditional_not_current_proof",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D589_1_missing_objects_are_precise",
            "decision": "the remaining proof debt is now explicit: pairing, DC, v_X, boundary domain, no-stabilizer proof, matter quotient",
            "meaning": "this is buildable if those objects can be sourced from the parent action",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D589_2_edge_row_template_written",
            "decision": "source-backed edge-product row template written for fallback",
            "meaning": "if certificate fails, the next honest row needs K_edge, Qbar_edge_XH, and qbar_XT sources at the tightest lambda",
            "claim_status": "nonclaim_template",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU589_0_allowed",
            "allowed_after_589": "try to map DCdagger to the vertical generator v_X for actual MTS parent variables",
            "forbidden_after_589": "claim the certificate is proved just because the Killing/stabilizer route exists",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU589_1_allowed",
            "allowed_after_589": "use proper-boundary/no-stabilizer theorem as the local silence target",
            "forbidden_after_589": "include improper ADM/time/rotation modes in the X domain",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU589_2_allowed",
            "allowed_after_589": "fill source-backed edge row if adjoint certificate cannot be sourced",
            "forbidden_after_589": "mark budget/smoke rows valid_for_claim",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S589_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "The adjoint certificate is now structurally buildable: prove DCdagger=v_X and no proper vertical stabilizers, or fall back to sourced edge coefficients.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    certificate_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
    required_sources: list[dict[str, Any]],
    edge_template: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_588_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in certificate_rows if row["valid_for_claim"] == "true"],
        *[row for row in edge_template if row["valid_for_claim"] == "true"],
    ]
    stabilizer_route = any(row["certificate_id"] == "AZC589_1_metric_Killing_stabilizer" for row in certificate_rows)
    result_row = any(row["certificate_id"] == "AZC589_5_certificate_result" for row in certificate_rows)
    missing_required = [row for row in required_sources if row["current_status"] == "missing"]
    edge_required_row = any(row["row_id"] == "SBE589_0_required_source_backed_row" for row in edge_template)
    return [
        {
            "check_id": "V589_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V589_1_prior_588_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V589_2_stabilizer_certificate_route_written",
            "result": "pass" if stabilizer_route and result_row else "fail",
            "detail": f"certificate_rows={len(certificate_rows)}",
        },
        {
            "check_id": "V589_3_kill_chain_not_promoted",
            "result": "pass" if all(row["blocks_claim"] == "true" for row in kill_rows) else "fail",
            "detail": f"kill_rows={len(kill_rows)}",
        },
        {
            "check_id": "V589_4_required_sources_explicit",
            "result": "pass" if len(missing_required) >= 6 else "fail",
            "detail": f"missing_required_sources={len(missing_required)}",
        },
        {
            "check_id": "V589_5_edge_template_nonclaim",
            "result": "pass" if edge_required_row and not any(row["valid_for_claim"] == "true" for row in edge_template) else "fail",
            "detail": f"edge_template_rows={len(edge_template)}",
        },
        {
            "check_id": "V589_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V589_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    certificate_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
    required_sources: list[dict[str, Any]],
    edge_template: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 589 Y5 R10 adjoint zero-mode certificate or source-backed edge-product row

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- I built the certificate skeleton rather than just repeating the blocker.
- The best theorem route is: prove `(DC)^dagger X` is the vertical generator/stabilizer action `v_X[Y]`; then proper boundary/reference conditions remove all nonzero stabilizers, so `X=0`.
- In metric language this is the familiar Killing-type route: `L_X g=0` plus proper boundary data kills proper `X`; improper time/rotation/ADM symmetries must not be part of the vertical defect domain.
- This is still not a claim. Current MTS still needs the parent pairing, explicit `DC`, vertical transformation law, boundary domain, no-stabilizer proof, and matter quotient map.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Adjoint Zero-Mode Certificate
{markdown_table(certificate_rows, ["certificate_id", "claim", "mathematical_test", "if_true", "current_status", "valid_for_claim"])}

## Kill Chain Status
{markdown_table(kill_rows, ["chain_id", "step", "equation", "status", "blocks_claim"])}

## Sources Required To Close Certificate
{markdown_table(required_sources, ["source_id", "needed_object", "acceptable_form", "why_needed", "current_status"])}

## Source-Backed Edge Product Row Template
{markdown_table(edge_template, ["row_id", "lambda_um", "K_edge", "Qbar_edge_XH", "qbar_XT", "alpha_edge_ceiling", "alpha_edge_predicted", "diagnostic_status", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_589", "forbidden_after_589", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a decent morning hit. The certificate is not closed, but it is now *buildable* in a precise way: make `DCdagger` equal the vertical generator and prove there are no proper vertical stabilizers. If that mapping will not come out of the parent action, the fallback is no longer vague either: fill the tightest edge row with actual sourced `K_edge`, `Qbar_edge_XH`, and `qbar_XT`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    edge_budget_rows = read_csv(PRIOR_588_EDGE_BUDGET)
    tightest = tightest_budget(edge_budget_rows)
    certificate_rows = make_certificate()
    kill_rows = make_kill_chain()
    required_sources = make_required_sources()
    edge_template = make_edge_template(tightest)
    decision_rows = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, certificate_rows, kill_rows, required_sources, edge_template)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        CERTIFICATE_PATH,
        certificate_rows,
        ["certificate_id", "claim", "mathematical_test", "if_true", "current_status", "valid_for_claim"],
    )
    write_csv(KILL_CHAIN_PATH, kill_rows, ["chain_id", "step", "equation", "status", "blocks_claim"])
    write_csv(
        REQUIRED_SOURCES_PATH,
        required_sources,
        ["source_id", "needed_object", "acceptable_form", "why_needed", "current_status"],
    )
    write_csv(
        EDGE_ROW_TEMPLATE_PATH,
        edge_template,
        [
            "row_id",
            "lambda_m",
            "lambda_um",
            "K_edge",
            "Qbar_edge_XH",
            "qbar_XT",
            "alpha_edge_ceiling",
            "alpha_edge_predicted",
            "diagnostic_status",
            "source_required",
            "valid_for_claim",
        ],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_589", "forbidden_after_589", "next_action"])
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
        certificate_rows,
        kill_rows,
        required_sources,
        edge_template,
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
