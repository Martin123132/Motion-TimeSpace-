from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1369"
TITLE = "1369-Y5-R10-RAB-Lcg-parent-definition-metric-silence-or-q_loc-gamma-projection-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LCG_HUNT_PATH = OUT_DIR / f"{PACK_ID}_LCG_PARENT_DEFINITION_HUNT.csv"
LCG_RESPONSE_PATH = OUT_DIR / f"{PACK_ID}_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv"
PROJECTION_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_QLOC_GAMMA_RUNNER_SCHEMA.csv"
SMOKE_RESULT_PATH = OUT_DIR / f"{PACK_ID}_QLOC_GAMMA_SMOKE_RESULT.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1369_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1369_0_1368_doc",
            "source_path": "1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels-or-q_loc-projection-map.md",
            "required_anchor": "NEXT1368_0_1369",
            "purpose": "1368 handoff to L_cg metric-silence hunt or q_loc gamma projection runner.",
        },
        {
            "source_id": "SRC1369_1_1368_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1368_NEXT_TARGET.csv",
            "required_anchor": "NEXT1368_0_1369",
            "purpose": "machine-readable 1369 target.",
        },
        {
            "source_id": "SRC1369_2_1368_kernel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
            "required_anchor": "KERN1368_4_Lcg_metric_composite_branch",
            "purpose": "1368 L_cg fixed-scale branch and metric-composite counterbranch.",
        },
        {
            "source_id": "SRC1369_3_1368_projection",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
            "required_anchor": "PROJ1368_5_projection_verdict",
            "purpose": "blocked q_loc-to-gamma projection requirements.",
        },
        {
            "source_id": "SRC1369_4_798_gamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_1_gradient_expansion",
            "purpose": "Gamma_eff=L_cg^-2 F(m) and gradient product-rule dependence on L_cg.",
        },
        {
            "source_id": "SRC1369_5_1289_chain",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "required_anchor": "KDR1289_1_local_zero_condition_for_chain_kernel",
            "purpose": "M_L zero/silence condition and full chain-kernel blocker.",
        },
        {
            "source_id": "SRC1369_6_1299_trace",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
            "required_anchor": "STK1299_1_Lcg_spatial_trace",
            "purpose": "spatial trace bound showing missing L_cg value, lower bound, and M_L response.",
        },
        {
            "source_id": "SRC1369_7_776_kgamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "connection/projector/boundary metric-response terms that remain open.",
        },
        {
            "source_id": "SRC1369_8_1181_cassini",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "required_anchor": "SRC1181W_0_Cassini_gamma",
            "purpose": "source-backed Cassini PPN gamma comparator.",
        },
        {
            "source_id": "SRC1369_9_1244_policy",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict one-sigma gamma policy and q_R guardrail, not automatically q_loc.",
        },
        {
            "source_id": "SRC1369_10_1244_doc",
            "source_path": "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md",
            "required_anchor": "QBD1244_0_projection",
            "purpose": "q_R-to-gamma convention that must not be imported without a q_loc bridge.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def lcg_hunt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "hunt_id": "LCGH1369_0_registered_formula",
                "candidate_definition": "Gamma_eff=L_cg^-2 F(m)",
                "derivation_or_test": "registered evidence defines how L_cg enters Gamma_eff, not what L_cg is as a parent object",
                "metric_response": "M_L remains undefined",
                "status": "FORMULA_DEPENDENCE_FOUND_PARENT_DEFINITION_NOT_FOUND",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchors": "GSE798_0_definition;KDR1289_0_Gamma_m_L_chain_kernel_00",
                "missing_to_promote": "parent declaration of L_cg; units; lower bound; metric variation rule",
            },
            {
                "hunt_id": "LCGH1369_1_fixed_parameter_route",
                "candidate_definition": "L_cg=L0, a parent-fixed scalar length parameter held fixed in Hilbert variation",
                "derivation_or_test": "For a metric-independent parameter L0, delta_g L_cg=0 by definition, hence M_L^{mu nu}:=delta L_cg/delta g_{mu nu}=0.",
                "metric_response": "zero under fixed-parameter contract",
                "status": "EXACT_CONDITIONAL_SILENCE_LEMMA_UNSIGNED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchors": "KERN1368_3_Lcg_fixed_scale_branch;KDR1289_1_local_zero_condition_for_chain_kernel",
                "missing_to_promote": "source-backed parent action must choose this route and explain covariance/local-scale meaning",
            },
            {
                "hunt_id": "LCGH1369_2_cell_volume_route",
                "candidate_definition": "L_cg=(V_D)^(1/3), V_D=int_D sqrt(h) d^3x",
                "derivation_or_test": "delta L_cg/L_cg=(1/3)delta V_D/V_D=(1/6)<h^{ij} delta h_ij>_D plus domain-motion terms.",
                "metric_response": "generically nonzero",
                "status": "COUNTEREXAMPLE_TO_AUTOMATIC_SILENCE",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv;source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
                "source_anchors": "KERN1368_4_Lcg_metric_composite_branch;STK1299_1_Lcg_spatial_trace",
                "missing_to_promote": "if this route is chosen, M_L and domain-boundary terms must be bounded, not deleted",
            },
            {
                "hunt_id": "LCGH1369_3_curvature_length_route",
                "candidate_definition": "L_cg=|I[g]|^(-1/2) for a curvature invariant I[g]",
                "derivation_or_test": "delta L_cg=-(1/2)L_cg I^-1 delta I plus absolute-value/sign and boundary terms where I is nonzero.",
                "metric_response": "generically nonzero and higher-derivative",
                "status": "COUNTEREXAMPLE_TO_AUTOMATIC_SILENCE",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
                "source_anchors": "KERN1368_4_Lcg_metric_composite_branch",
                "missing_to_promote": "explicit invariant, regularity domain, boundary terms, units, and weak-field response",
            },
            {
                "hunt_id": "LCGH1369_4_density_or_source_length_route",
                "candidate_definition": "L_cg=(M_cell/rho)^(1/3) or another matter/source-derived coarse-grain length",
                "derivation_or_test": "metric response depends on the density convention, volume measure, source conservation law, and whether M_cell is held fixed.",
                "metric_response": "not zero without a matter/source descent theorem",
                "status": "COUNTERBRANCH_RETAINED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
                "source_anchors": "STK1299_1_Lcg_spatial_trace;KGL776_2_derivative_terms",
                "missing_to_promote": "source descent, conserved mass convention, density units, and local-support/boundary theorem",
            },
            {
                "hunt_id": "LCGH1369_5_parent_definition_verdict",
                "candidate_definition": "live L_cg parent definition",
                "derivation_or_test": "registered 1368 source set gives formula dependence and response requirements, but no signed parent definition selecting fixed parameter vs metric-composite scale",
                "metric_response": "M_L unresolved",
                "status": "NOT_FOUND_IN_REGISTERED_SOURCES",
                "source_paths": "aggregate_1369_source_register",
                "source_anchors": "SRC1369_0_to_SRC1369_10",
                "missing_to_promote": "a parent action clause for L_cg, or a source-backed response/bound row with units",
            },
        ]
    )


def lcg_response_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "response_id": "ML1369_0_exact_fixed_scale_silence",
                "target": "M_L^{mu nu}",
                "identity_or_bound": "If L_cg is a metric-independent parent scalar parameter, M_L^{mu nu}=0.",
                "status": "DERIVED_CONDITIONAL_ONLY",
                "needed_inputs": "SIGNED_PARENT_FIXED_LCG;LCG_UNITS;LCG_DOMAIN_MEANING;VARIATION_BEFORE_READOUT",
                "claim_effect": "would remove the algebraic L_cg chain term, but not K_conn/K_domain/K_boundary",
            },
            {
                "response_id": "ML1369_1_volume_scale_bound",
                "target": "sum_i |M_L^{ii}|",
                "identity_or_bound": "For L_cg=(V_D)^(1/3), |delta L_cg|/L_cg <= (1/6)<sum_i |delta h_ii|>_D + domain-motion terms in local orthonormal gauge.",
                "status": "DERIVED_TEMPLATE_NOT_SOURCE_SELECTED",
                "needed_inputs": "DOMAIN_D;GAUGE;HYPERSURFACE;DOMAIN_MOTION_BOUND;LCG_LOWER_BOUND",
                "claim_effect": "metric-composite L_cg needs a real numerical/domain bound",
            },
            {
                "response_id": "ML1369_2_curvature_scale_bound",
                "target": "M_L^{mu nu}",
                "identity_or_bound": "For L_cg=|I[g]|^-1/2, |delta L_cg| <= 0.5 L_cg |delta I|/|I| away from I=0, with boundary/derivative terms retained.",
                "status": "DERIVED_TEMPLATE_NOT_SOURCE_SELECTED",
                "needed_inputs": "INVARIANT_I;LOWER_BOUND_ON_|I|;DELTA_I_KERNEL;BOUNDARY_TERMS;REGULARITY_DOMAIN",
                "claim_effect": "curvature-defined L_cg is unsafe for local-GR unless tightly bounded",
            },
            {
                "response_id": "ML1369_3_chain_zero_gate_update",
                "target": "Kmetric_chain^{00}",
                "identity_or_bound": "Kmetric_chain^{00}=C_sign[L_cg^-2 F_prime(m)M_m^{00}-2L_cg^-3F(m)M_L^{00}]+K_cdb.",
                "status": "ZERO_GATE_REQUIRES_LCG_SILENCE_OR_F_ZERO",
                "needed_inputs": "F_prime(m_*)=0;M_L=0_OR_F(m_*)=0;K_cdb=0_OR_BOUNDED;C_sign;units",
                "claim_effect": "fixed-field m progress is insufficient without the L_cg gate",
            },
            {
                "response_id": "ML1369_4_best_route",
                "target": "parent action contract",
                "identity_or_bound": "Least-scrutiny route is to make L_cg a renormalization/coarse-graining scale external to Hilbert variation while observable domain readouts are treated after variation.",
                "status": "PROPOSED_PARENT_CONTRACT_NOT_YET_SOURCE_SIGNED",
                "needed_inputs": "write parent action clause; prove covariance/descent; route readout/domain dependence outside Kmetric chain",
                "claim_effect": "could close M_L cleanly if signed, but currently only a closure candidate",
            },
        ]
    )


def projection_schema_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "schema_id": "QG1369_0_inputs",
                "field": "q_loc_hat",
                "required_value": "finite dimensionless local residual amplitude after source averaging",
                "unit": "dimensionless",
                "status": "MISSING_QLOC_VALUE",
                "source_requirement": "source path to q_loc computation and normalization",
            },
            {
                "schema_id": "QG1369_1_response_coefficient",
                "field": "C_qgamma",
                "required_value": "gamma_minus_1_q_loc = C_qgamma*q_loc_hat + C_DeltaK*DeltaK_hat + retained residual terms",
                "unit": "dimensionless",
                "status": "MISSING_WEAK_FIELD_RESPONSE",
                "source_requirement": "linearized solve, gauge, trace reversal, sign, and GM convention",
            },
            {
                "schema_id": "QG1369_2_comparator",
                "field": "sigma_gamma",
                "required_value": "2.3e-5 at N_sigma=1 from Cassini policy feed",
                "unit": "dimensionless",
                "status": "SOURCE_BACKED_COMPARATOR",
                "source_requirement": "SRC1181W_0_Cassini_gamma;RPF1244_0_policy",
            },
            {
                "schema_id": "QG1369_3_nonimport_rule",
                "field": "q_R_to_q_loc_bridge",
                "required_value": "proof q_loc uses the same normalization as q_R before using gamma_minus_1_QR=-q_R_hat/2",
                "unit": "logic",
                "status": "MISSING_BRIDGE",
                "source_requirement": "q_loc-to-q_R reduction theorem or separate q_loc projection",
            },
            {
                "schema_id": "QG1369_4_pass_policy",
                "field": "acceptance",
                "required_value": "only pass if every response coefficient is numeric/source-backed and |gamma_minus_1_q_loc| <= N_sigma*sigma_gamma",
                "unit": "logic",
                "status": "POLICY_READY_INPUTS_MISSING",
                "source_requirement": "all QG1369 inputs resolved, no cancellation assumptions",
            },
        ]
    )


def smoke_result_rows() -> list[dict[str, object]]:
    qloc_value: float | None = None
    response_coefficient: float | None = None
    sigma_gamma = 2.3e-5
    n_sigma = 1.0
    if qloc_value is None or response_coefficient is None:
        gamma_residual = "MISSING"
        pass_fail = "BLOCKED_MISSING_QLOC_OR_RESPONSE"
    else:
        gamma_residual_value = response_coefficient * qloc_value
        gamma_residual = f"{gamma_residual_value:.12g}"
        pass_fail = "PASS_NONCLAIM_SMOKE" if abs(gamma_residual_value) <= n_sigma * sigma_gamma else "FAIL_NONCLAIM_SMOKE"
    return mark_nonclaim(
        [
            {
                "run_id": "SMOKE1369_0_placeholder_block",
                "model_branch": "q_loc_to_gamma_nonclaim_schema",
                "q_loc_hat": "MISSING_QLOC_VALUE" if qloc_value is None else qloc_value,
                "C_qgamma": "MISSING_WEAK_FIELD_RESPONSE" if response_coefficient is None else response_coefficient,
                "gamma_minus_1_predicted": gamma_residual,
                "sigma_gamma": sigma_gamma,
                "N_sigma": n_sigma,
                "result": pass_fail,
                "claim_effect": "runner schema works by refusing to score missing inputs",
            }
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1369_0_parent_Lcg_definition",
                "gate": "source-backed parent definition of L_cg exists",
                "status": "BLOCKED",
                "reason": "registered sources define L_cg dependence but do not select fixed parameter, cell volume, curvature scale, or source-density route",
            },
            {
                "gate_id": "GATE1369_1_ML_silence_or_bound",
                "gate": "M_L is zero-derived or bounded with units",
                "status": "BLOCKED",
                "reason": "fixed-scale silence lemma is exact but unsigned; metric-composite routes are generically nonzero",
            },
            {
                "gate_id": "GATE1369_2_Kcdb_resolved",
                "gate": "connection/domain/boundary terms are zero-derived or bounded",
                "status": "BLOCKED",
                "reason": "K_conn, K_domain, and K_boundary remain retained after the algebraic chain analysis",
            },
            {
                "gate_id": "GATE1369_3_q_loc_gamma_runner",
                "gate": "q_loc-to-gamma runner can score a finite branch",
                "status": "BLOCKED_SCHEMA_READY",
                "reason": "schema and comparator exist, but q_loc_hat and C_qgamma are missing",
            },
            {
                "gate_id": "GATE1369_4_local_GR_or_PPN_claim",
                "gate": "local GR / PPN pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "L_cg parent status and q_loc projection are unresolved",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1369_0_exact_but_unsigned",
                "decision": "keep the fixed-parameter L_cg silence lemma as the clean derivation route",
                "why": "delta_g L_cg=0 is exact if L_cg is genuinely external to Hilbert variation",
                "next_action": "write a parent action contract that either signs this route or explicitly rejects it",
            },
            {
                "decision_id": "DEC1369_1_counterexamples_matter",
                "decision": "do not call L_cg silent if it is a cell volume, curvature, or density scale",
                "why": "all common geometric/coarse-graining definitions have nonzero metric response unless bounded",
                "next_action": "if choosing a metric-composite L_cg, compute M_L and domain terms instead of deleting them",
            },
            {
                "decision_id": "DEC1369_2_projection_runner_ready_not_score_ready",
                "decision": "use the q_loc gamma schema as the next empirical discipline lane",
                "why": "Cassini gives a clean comparator, but only after q_loc has a signed weak-field response coefficient",
                "next_action": "derive C_qgamma or prove q_loc reduces to the existing q_R convention",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1369_0_1370",
                "next_doc": "1370-Y5-R10-RAB-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
                "next_script": "scripts/Y5_R10_RAB_parent_Lcg_contract_or_q_loc_weak_field_response_coefficient.py",
                "task": "attempt to sign a parent L_cg contract as fixed external scale under Hilbert variation; if not defensible, derive the weak-field response coefficient C_qgamma for q_loc using a linearized PPN ansatz",
                "success_condition": "either M_L=0 becomes parent-signed without covariance cheating, or the q_loc gamma runner receives a real symbolic/numeric response coefficient and remains nonclaim until q_loc_hat exists",
                "do_not_claim": "local GR;PPN pass;q_loc=0;Khat match;GitHub-ready result",
            }
        ]
    )


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            rows = read_csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    lcg_hunt: list[dict[str, object]],
    lcg_response: list[dict[str, object]],
    projection_schema: list[dict[str, object]],
    smoke_results: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + lcg_hunt + lcg_response + projection_schema + smoke_results + gates
    )
    fixed_lemma = any(row["hunt_id"] == "LCGH1369_1_fixed_parameter_route" and row["status"] == "EXACT_CONDITIONAL_SILENCE_LEMMA_UNSIGNED" for row in lcg_hunt)
    parent_missing = any(row["hunt_id"] == "LCGH1369_5_parent_definition_verdict" and row["status"] == "NOT_FOUND_IN_REGISTERED_SOURCES" for row in lcg_hunt)
    counterexamples = all(
        any(row["hunt_id"] == hunt_id and row["status"] in {"COUNTEREXAMPLE_TO_AUTOMATIC_SILENCE", "COUNTERBRANCH_RETAINED"} for row in lcg_hunt)
        for hunt_id in ["LCGH1369_2_cell_volume_route", "LCGH1369_3_curvature_length_route", "LCGH1369_4_density_or_source_length_route"]
    )
    schema_ready = any(row["schema_id"] == "QG1369_4_pass_policy" and row["status"] == "POLICY_READY_INPUTS_MISSING" for row in projection_schema)
    smoke_blocks = any(row["run_id"] == "SMOKE1369_0_placeholder_block" and row["result"] == "BLOCKED_MISSING_QLOC_OR_RESPONSE" for row in smoke_results)
    local_claim_blocked = any(row["gate_id"] == "GATE1369_4_local_GR_or_PPN_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1369_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1369_1_fixed_scale_lemma",
            "check": "fixed-parameter L_cg silence lemma is captured as exact but unsigned",
            "status": "PASS" if fixed_lemma else "FAIL",
            "details": "LCGH1369_1 derives M_L=0 only under a parent-fixed parameter contract",
        },
        {
            "validation_id": "VAL1369_2_no_parent_definition",
            "check": "registered evidence does not yet contain a live L_cg parent definition",
            "status": "PASS" if parent_missing else "FAIL",
            "details": "LCGH1369_5 remains NOT_FOUND_IN_REGISTERED_SOURCES",
        },
        {
            "validation_id": "VAL1369_3_counterbranches",
            "check": "metric-composite L_cg counterbranches are retained",
            "status": "PASS" if counterexamples else "FAIL",
            "details": "volume, curvature, and density/source routes are not automatically silent",
        },
        {
            "validation_id": "VAL1369_4_projection_schema",
            "check": "q_loc-to-gamma runner schema exists but refuses missing inputs",
            "status": "PASS" if schema_ready and smoke_blocks else "FAIL",
            "details": "QG1369 schema plus SMOKE1369 placeholder block prevent false PPN scoring",
        },
        {
            "validation_id": "VAL1369_5_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1369 is a derivation/projection discipline checkpoint",
        },
        {
            "validation_id": "VAL1369_6_local_claim_blocked",
            "check": "local GR / PPN claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1369_4_local_GR_or_PPN_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1369_7_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1369_8_overall",
            "check": "overall 1369 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1369 proves the fixed-scale route conditionally, rejects automatic silence for geometric L_cg routes, and builds a blocked q_loc-gamma schema.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    lcg_hunt: list[dict[str, object]],
    lcg_response: list[dict[str, object]],
    projection_schema: list[dict[str, object]],
    smoke_results: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1369 derives an exact but conditional `L_cg` silence lemma: if `L_cg` is a parent-fixed scalar length parameter held fixed in Hilbert variation, then `delta_g L_cg=0` and `M_L^{{mu nu}}=0`. That is real progress, but it is not yet a live MTS claim because the registered sources do not parent-sign that definition.

**Main progress:** the branch fork is now explicit. Fixed-parameter `L_cg` can close the algebraic `M_L` term cleanly; geometric/coarse-graining versions such as cell-volume, curvature-length, or density/source scales are generically metric-composite and therefore not automatically silent. The fallback `q_loc -> gamma` runner schema now exists and correctly refuses to score missing `q_loc_hat` or `C_qgamma`.

**Still blocked:** no local-GR, PPN, R10, clock, or orbital pass is allowed. The next real fork is either to sign a parent `L_cg` contract without covariance cheating, or to derive the weak-field response coefficient `C_qgamma` so the Cassini comparator can actually be used.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `L_cg` Parent Definition Hunt

{table(["hunt_id", "candidate_definition", "status", "derivation_or_test", "metric_response", "missing_to_promote", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], lcg_hunt)}

## `L_cg` Metric-Response Derivation Ledger

{table(["response_id", "target", "status", "identity_or_bound", "needed_inputs", "claim_effect", "valid_for_claim", "claim_allowed"], lcg_response)}

## `q_loc -> gamma` Runner Schema

{table(["schema_id", "field", "required_value", "unit", "status", "source_requirement", "valid_for_claim", "claim_allowed"], projection_schema)}

## Nonclaim Smoke Result

{table(["run_id", "model_branch", "q_loc_hat", "C_qgamma", "gamma_minus_1_predicted", "sigma_gamma", "N_sigma", "result", "claim_effect", "valid_for_claim", "claim_allowed"], smoke_results)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    lcg_hunt = lcg_hunt_rows()
    lcg_response = lcg_response_rows()
    projection_schema = projection_schema_rows()
    smoke_results = smoke_result_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LCG_HUNT_PATH, lcg_hunt)
    write_csv(LCG_RESPONSE_PATH, lcg_response)
    write_csv(PROJECTION_SCHEMA_PATH, projection_schema)
    write_csv(SMOKE_RESULT_PATH, smoke_results)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        LCG_HUNT_PATH,
        LCG_RESPONSE_PATH,
        PROJECTION_SCHEMA_PATH,
        SMOKE_RESULT_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, lcg_hunt, lcg_response, projection_schema, smoke_results, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, lcg_hunt, lcg_response, projection_schema, smoke_results, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
