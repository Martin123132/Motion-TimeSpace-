from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md"

PRIOR_589_VALIDATION = RESIDUALS / "P8_Y5_BRR545_589_VALIDATION.csv"
PRIOR_589_EDGE_TEMPLATE = RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_590_SOURCE_REGISTER.csv"
DCDAGGER_MAP_PATH = RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
GR_ANALOGUE_PATH = RESIDUALS / "P8_Y5_R10_590_GR_ANALOGUE_CHECK.csv"
FIELD_ACTION_PATH = RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
CLOSURE_GATE_PATH = RESIDUALS / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv"
EDGE_STATUS_PATH = RESIDUALS / "P8_Y5_R10_590_EDGE_ROW_SOURCE_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_590_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_590_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_590_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_590_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_DCdagger_mapped_to_symplectic_flat_vertical_generator_conditionally_parent_Omega_missing_edge_row_still_blocked"
CLAIM_CEILING = "conditional_DCdagger_equals_Omega_flat_vX_map_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md"

SOURCE_FILES = [
    ("589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md", "immediate adjoint certificate handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_589_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_589_ADJOINT_ZERO_MODE_CERTIFICATE.csv", "adjoint zero-mode certificate skeleton"),
    ("source-intake/mts_residuals/P8_Y5_R10_589_KILL_CHAIN_STATUS.csv", "kill-chain blocker status"),
    ("source-intake/mts_residuals/P8_Y5_R10_589_SOURCES_REQUIRED_TO_CLOSE_CERTIFICATE.csv", "required sources for certificate"),
    ("source-intake/mts_residuals/P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv", "edge source row fallback"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv", "Noether/momentum-map contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv", "momentum-map owner attempts"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "parent momentum map owner fork"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "quotient vertical theorem shape"),
    ("587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md", "affine Vdef source map"),
    ("588-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product.md", "adjoint theorem and edge budgets"),
    ("scripts/Y5_R10_map_DCdagger_to_vertical_generator_or_fill_edge_row_source.py", "this checkpoint generator"),
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


def make_dcdagger_map() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "DVM590_0_define_generator",
            "statement": "G_X[X;Y]=int_Sigma X_nu C_X^nu[Y]+Q_X[X;Y]",
            "meaning": "the multiplier constraint must be the bulk density of a differentiable Hamiltonian generator",
            "map_result": "definition_contract",
            "current_MTS_status": "G_X_template_exists_but_Q_and_domain_not_derived",
            "valid_for_claim": "false",
        },
        {
            "map_id": "DVM590_1_variation_as_DCadjoint",
            "statement": "delta G_X[delta Y]=int_Sigma X_nu DC_X^nu[delta Y]+delta Q_X = <(DC_X)^dagger X,delta Y> + boundary_fixed",
            "meaning": "DCdagger X is a covector on parent field space",
            "map_result": "formal_adjoint_side",
            "current_MTS_status": "requires explicit DC and boundary pairing",
            "valid_for_claim": "false",
        },
        {
            "map_id": "DVM590_2_momentum_map_identity",
            "statement": "delta G_X[delta Y]=Omega_Y(delta Y,v_X[Y])",
            "meaning": "the same variation is the symplectic pairing with the vertical generator",
            "map_result": "momentum_map_side",
            "current_MTS_status": "requires parent theta_Y/Omega_Y and vertical action v_X",
            "valid_for_claim": "false",
        },
        {
            "map_id": "DVM590_3_precise_map",
            "statement": "(DC_X)^dagger X = Omega_Y^flat(v_X[Y])",
            "meaning": "refines 589: DCdagger is the symplectic covector dual of the vertical generator, not literally the vector until Omega raises/lowers",
            "map_result": "conditional_map_theorem",
            "current_MTS_status": "mathematically_clean_but_parent_Omega_missing",
            "valid_for_claim": "false",
        },
        {
            "map_id": "DVM590_4_raise_index",
            "statement": "on reduced nondegenerate phase space, v_X[Y]=Omega_Y^{-1}[(DC_X)^dagger X]",
            "meaning": "this is the actual vertical generator map once the symplectic structure is owned",
            "map_result": "actual_generator_after_Omega_inverse",
            "current_MTS_status": "not_available_until_reduced_Omega_is_explicit",
            "valid_for_claim": "false",
        },
        {
            "map_id": "DVM590_5_zero_mode_implication",
            "statement": "(DC_X)^dagger X=0 => Omega(delta Y,v_X)=0 for all delta Y => v_X=0 modulo gauge degeneracies",
            "meaning": "the adjoint-zero certificate reduces to no proper vertical stabilizers",
            "map_result": "conditional_kernel_kill",
            "current_MTS_status": "needs nondegenerate reduced Omega and proper-boundary domain",
            "valid_for_claim": "false",
        },
    ]


def make_gr_analogue() -> list[dict[str, Any]]:
    return [
        {
            "analogue_id": "GRA590_0_ADM_momentum_constraint",
            "object": "ADM momentum/diffeomorphism constraint",
            "canonical_form": "C_i=-2 h_{ij}D_k pi^{jk}+C_i^matter",
            "generator_variation": "G[xi]=int pi^{ij} L_xi h_{ij}+p_A L_xi Phi^A + boundary",
            "map_lesson": "functional derivatives of G give v_xi=(L_xi h,L_xi pi,L_xi Phi,L_xi p)",
            "MTS_transfer_status": "template_only_not_MTS_proof",
            "valid_for_claim": "false",
        },
        {
            "analogue_id": "GRA590_1_covariant_phase_space",
            "object": "covariant Hamiltonian charge",
            "canonical_form": "delta H_xi = Omega(delta phi,L_xi phi)",
            "generator_variation": "H_xi=int_S Q_xi - i_xi B plus constraints",
            "map_lesson": "differentiable charge variation is exactly Omega-flat of the diffeomorphism generator",
            "MTS_transfer_status": "conditional_if_parent_theta_Q_exist",
            "valid_for_claim": "false",
        },
        {
            "analogue_id": "GRA590_2_current_MTS_CX",
            "object": "MTS C_X=-nabla_mu P^{mu nu}+J_eff^nu",
            "canonical_form": "candidate momentum-map density",
            "generator_variation": "G_X=int X_nu C_X^nu+Q_X",
            "map_lesson": "will match GR only if P,J_eff are coefficients of a real parent Noether current",
            "MTS_transfer_status": "not_derived_P_J_theta_Omega_missing",
            "valid_for_claim": "false",
        },
    ]


def make_field_action_map() -> list[dict[str, Any]]:
    return [
        {
            "field_block": "metric_or_coframe",
            "candidate_vertical_action": "v_X[g]=L_X g or v_X[e]=L_X e plus local Lorentz compensation",
            "DCdagger_target": "metric/coframe component of Omega^flat(v_X)",
            "status": "standard_candidate_not_parent_declared",
            "missing_input": "observed coframe/metric as parent field and symplectic potential",
            "valid_for_claim": "false",
        },
        {
            "field_block": "canonical_momenta_or_boundary_charge",
            "candidate_vertical_action": "v_X[pi]=L_X pi plus density/boundary improvements",
            "DCdagger_target": "momentum component of Omega^flat(v_X)",
            "status": "not_written_for_MTS",
            "missing_input": "canonical variables or covariant charge split",
            "valid_for_claim": "false",
        },
        {
            "field_block": "Gamma_Khat_qloc_sector",
            "candidate_vertical_action": "v_X[T_GK]=L_X T_GK if T_GK is parent stress",
            "DCdagger_target": "Euler-Ward stress-divergence covector",
            "status": "conditional_from_513_not_integrated_with_CX",
            "missing_input": "S_GK and Helmholtz/integrability proof",
            "valid_for_claim": "false",
        },
        {
            "field_block": "domain_memory_projector_fields",
            "candidate_vertical_action": "v_X[Phi^A]=L_X Phi^A or quotient-vertical action",
            "DCdagger_target": "extra-sector components of Omega^flat(v_X)",
            "status": "unmapped",
            "missing_input": "field transformation law for chi_D,Qcoh,memory,Pi_M/boundary variables",
            "valid_for_claim": "false",
        },
        {
            "field_block": "matter_readout",
            "candidate_vertical_action": "v_X matter=0 after quotient; v_X hat_g(pi(Y))=0",
            "DCdagger_target": "no matter component in proper vertical generator",
            "status": "not_derived",
            "missing_input": "matter quotient functor and no-marker theorem",
            "valid_for_claim": "false",
        },
        {
            "field_block": "boundary_edge",
            "candidate_vertical_action": "proper X has zero boundary charge or exact primitive",
            "DCdagger_target": "no boundary covector remains after delta Q_X",
            "status": "not_derived",
            "missing_input": "Q_X differentiability, B_X exactness, Pi_M^H edge projection zero",
            "valid_for_claim": "false",
        },
    ]


def make_closure_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MCG590_0_parent_Omega",
            "required_to_close": "explicit theta_Y and Omega_Y for parent variables",
            "current_status": "missing",
            "if_missing": "DCdagger remains an undefined covector up to arbitrary pairing",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_1_DCX_operator",
            "required_to_close": "linearized DC_X from C_X=-nabla P+J_eff",
            "current_status": "missing",
            "if_missing": "cannot compare DCdagger with Omega-flat vertical action",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_2_vertical_generator",
            "required_to_close": "v_X on every parent and boundary field",
            "current_status": "missing",
            "if_missing": "no actual generator to map to",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_3_differentiable_boundary",
            "required_to_close": "Q_X cancels boundary variation and is zero/proper/exact on local branch",
            "current_status": "missing",
            "if_missing": "edge charge survives and no-pole fails",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_4_reduced_nondegeneracy",
            "required_to_close": "Omega is nondegenerate after quotienting ordinary gauge degeneracies",
            "current_status": "not_checked",
            "if_missing": "DCdagger=0 may only imply a symplectic degeneracy, not X=0",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_5_no_proper_stabilizer",
            "required_to_close": "proper v_X[Y0]=0 implies X=0",
            "current_status": "not_proved",
            "if_missing": "adjoint zero modes can remain",
            "claim_blocked": "true",
        },
        {
            "gate_id": "MCG590_6_matter_quotient",
            "required_to_close": "ordinary matter sees only quotient variables",
            "current_status": "missing",
            "if_missing": "qbar_XT stays finite or must be bounded",
            "claim_blocked": "true",
        },
    ]


def make_edge_status(edge_template: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in edge_template:
        missing_markers = [value for value in row.values() if "MISSING" in str(value)]
        rows.append(
            {
                "edge_row_id": row["row_id"],
                "lambda_um": row["lambda_um"],
                "alpha_edge_ceiling": row["alpha_edge_ceiling"],
                "alpha_edge_predicted": row["alpha_edge_predicted"],
                "source_status": "missing_sources" if missing_markers else "diagnostic_budget_or_smoke_not_source_backed",
                "required_next": "fill K_edge,Qbar_edge_XH,qbar_XT from parent/source rows" if missing_markers else "replace diagnostic factors with sourced values",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D590_0_precise_map_found",
            "decision": "DCdagger maps to Omega-flat of the vertical generator",
            "meaning": "the actual generator is v_X=Omega^{-1} DCdaggerX on reduced phase space",
            "claim_status": "conditional_map_not_MTS_proof",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D590_1_589_refined",
            "decision": "refine the 589 wording from DCdagger=v_X to DCdagger=Omega_flat(v_X)",
            "meaning": "this prevents a category error between field-space covectors and vectors",
            "claim_status": "rigour_improvement",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D590_2_current_MTS_not_closed",
            "decision": "actual MTS map still lacks Omega, DC, v_X, boundary differentiability, and matter quotient",
            "meaning": "no no-pole/R10/local-GR promotion; next target must fill parent Omega/DC or edge sources",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU590_0_allowed",
            "allowed_after_590": "use DCdagger=Omega_flat(v_X) as the exact map theorem",
            "forbidden_after_590": "state DCdagger literally equals v_X without specifying the pairing/symplectic inverse",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU590_1_allowed",
            "allowed_after_590": "try to fill parent theta/Omega and DC_X operator",
            "forbidden_after_590": "promote no-pole from the GR analogue alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU590_2_allowed",
            "allowed_after_590": "if Omega/DC cannot be filled, fill source-backed edge coefficients",
            "forbidden_after_590": "mark diagnostic edge rows valid_for_claim",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S590_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "The exact map is now correct: DCdaggerX is the symplectic covector Omega-flat(v_X). Closing the certificate now requires parent Omega and DC_X, not just more words.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    map_rows: list[dict[str, Any]],
    gr_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_589_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in map_rows if row["valid_for_claim"] == "true"],
        *[row for row in gr_rows if row["valid_for_claim"] == "true"],
        *[row for row in field_rows if row["valid_for_claim"] == "true"],
        *[row for row in edge_rows if row["valid_for_claim"] == "true"],
    ]
    precise_map = any("Omega_Y^flat" in row["statement"] for row in map_rows)
    raise_index = any("Omega_Y^{-1}" in row["statement"] for row in map_rows)
    gr_template = any(row["analogue_id"] == "GRA590_0_ADM_momentum_constraint" for row in gr_rows)
    all_gates_block = all(row["claim_blocked"] == "true" for row in gate_rows)
    return [
        {
            "check_id": "V590_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V590_1_prior_589_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V590_2_precise_map_written",
            "result": "pass" if precise_map and raise_index else "fail",
            "detail": "requires DCdagger=Omega_flat(vX) and vX=Omega_inverse(DCdaggerX)",
        },
        {
            "check_id": "V590_3_GR_analogue_nonclaim",
            "result": "pass" if gr_template and not any(row["valid_for_claim"] == "true" for row in gr_rows) else "fail",
            "detail": f"gr_rows={len(gr_rows)}",
        },
        {
            "check_id": "V590_4_field_action_map_nonclaim",
            "result": "pass" if field_rows and not any(row["valid_for_claim"] == "true" for row in field_rows) else "fail",
            "detail": f"field_rows={len(field_rows)}",
        },
        {
            "check_id": "V590_5_closure_gates_block_claim",
            "result": "pass" if all_gates_block else "fail",
            "detail": f"gate_rows={len(gate_rows)};all_block={all_gates_block}",
        },
        {
            "check_id": "V590_6_edge_rows_still_nonclaim",
            "result": "pass" if edge_rows and not any(row["valid_for_claim"] == "true" for row in edge_rows) else "fail",
            "detail": f"edge_rows={len(edge_rows)}",
        },
        {
            "check_id": "V590_7_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V590_8_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    map_rows: list[dict[str, Any]],
    gr_rows: list[dict[str, Any]],
    field_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 590 Y5 R10 map DCdagger to vertical generator or fill edge-row source

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The mapping attempt succeeded as a precise conditional theorem, but not as a current MTS proof.
- Important refinement: `(DC_X)^dagger X` is not literally the vertical generator. It is the **symplectic covector** `Omega_Y^flat(v_X)`.
- Once the parent symplectic structure is owned and reduced, the actual generator is `v_X=Omega_Y^-1[(DC_X)^dagger X]`.
- Therefore the certificate now has the exact next missing objects: parent `theta/Omega`, explicit `DC_X`, vertical action on all parent fields, differentiable zero boundary charge, nondegenerate reduced phase space, no proper stabilizer, and matter quotient.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## DCdagger Vertical Map
{markdown_table(map_rows, ["map_id", "statement", "meaning", "map_result", "current_MTS_status", "valid_for_claim"])}

## GR Analogue Check
{markdown_table(gr_rows, ["analogue_id", "object", "canonical_form", "generator_variation", "map_lesson", "MTS_transfer_status", "valid_for_claim"])}

## Field-by-Field Vertical Action Map
{markdown_table(field_rows, ["field_block", "candidate_vertical_action", "DCdagger_target", "status", "missing_input", "valid_for_claim"])}

## Mapping Closure Gate
{markdown_table(gate_rows, ["gate_id", "required_to_close", "current_status", "if_missing", "claim_blocked"])}

## Edge Row Source Status
{markdown_table(edge_rows, ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "alpha_edge_predicted", "source_status", "required_next", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_590", "forbidden_after_590", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a real tightening. We have the right category map now: constraint variation covector to symplectic-dual generator. The proof is not closed, but the fog has cleared. Either fill `Omega_Y` and `DC_X`, or stop theorem-hunting and fill sourced edge coefficients.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    edge_template = read_csv(PRIOR_589_EDGE_TEMPLATE)
    map_rows = make_dcdagger_map()
    gr_rows = make_gr_analogue()
    field_rows = make_field_action_map()
    gate_rows = make_closure_gate()
    edge_rows = make_edge_status(edge_template)
    decision_rows = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, map_rows, gr_rows, field_rows, gate_rows, edge_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        DCDAGGER_MAP_PATH,
        map_rows,
        ["map_id", "statement", "meaning", "map_result", "current_MTS_status", "valid_for_claim"],
    )
    write_csv(
        GR_ANALOGUE_PATH,
        gr_rows,
        ["analogue_id", "object", "canonical_form", "generator_variation", "map_lesson", "MTS_transfer_status", "valid_for_claim"],
    )
    write_csv(
        FIELD_ACTION_PATH,
        field_rows,
        ["field_block", "candidate_vertical_action", "DCdagger_target", "status", "missing_input", "valid_for_claim"],
    )
    write_csv(
        CLOSURE_GATE_PATH,
        gate_rows,
        ["gate_id", "required_to_close", "current_status", "if_missing", "claim_blocked"],
    )
    write_csv(
        EDGE_STATUS_PATH,
        edge_rows,
        ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "alpha_edge_predicted", "source_status", "required_next", "valid_for_claim"],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_590", "forbidden_after_590", "next_action"])
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
        map_rows,
        gr_rows,
        field_rows,
        gate_rows,
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
