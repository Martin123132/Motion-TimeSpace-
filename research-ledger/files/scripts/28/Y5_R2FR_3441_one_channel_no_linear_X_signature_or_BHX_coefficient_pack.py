from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "3441-Y5-R2FR-one-channel-no-linear-X-signature-or-BHX-coefficient-pack-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3440": ROOT / "3440-Y5-R2FR-no-linear-X-parent-grammar-or-explicit-closure-demotion-under-AX1090.md",
    "next_3440": OUT / "P8_Y5_R2FR_3440_NEXT_TARGET.csv",
    "forbidden_vertices_3440": OUT / "P8_Y5_R2FR_3440_FORBIDDEN_VERTEX_LEDGER.csv",
    "closure_demotion_3440": OUT / "P8_Y5_R2FR_3440_CLOSURE_DEMOTION_LEDGER.csv",
    "bhx_route_3440": OUT / "P8_Y5_R2FR_3440_BHX_ROUTE_UPDATE.csv",
    "bhx_input_3439": OUT / "P8_Y5_R2FR_3439_BHX_INPUT_ROW.csv",
    "metric_mixing_3438": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_SCHUR_THEOREM.csv",
    "alpha_template_3438": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_ALPHA_TEMPLATE.csv",
    "moms_doc_1088": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "moms_clause_1088": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "moms_theorem_1088": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "moms_countermodels_1088": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "matter_pullback_doc_1044": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
    "matter_pullback_1044": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
    "qbar_components_1044": OUT / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
    "qbar_fallback_1044": OUT / "P8_Y5_R10_1044_QBARXT_BOUND_FALLBACK_ROWS.csv",
    "public_metric_doc_1030": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "public_metric_contract_1030": OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
    "cg_provenance_1030": OUT / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
    "local_bounds": LOCAL_BOUNDS,
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3441_SOURCE_REGISTER.csv",
    "channel_selection": OUT / "P8_Y5_R2FR_3441_CHANNEL_SELECTION.csv",
    "one_channel_proof_attempt": OUT / "P8_Y5_R2FR_3441_ONE_CHANNEL_NO_LINEAR_X_PROOF_ATTEMPT.csv",
    "trace_coefficient_definition": OUT / "P8_Y5_R2FR_3441_TRACE_COUPLING_COEFFICIENT_DEFINITION.csv",
    "bhx_coefficient_pack": OUT / "P8_Y5_R2FR_3441_BHX_COEFFICIENT_PACK.csv",
    "r10_ppn_score_interface": OUT / "P8_Y5_R2FR_3441_R10_PPN_SCORE_INTERFACE.csv",
    "newton_gr_impact": OUT / "P8_Y5_R2FR_3441_NEWTON_GR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3441_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3441_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3441_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3441_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3441_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3440": "handoff: no-linear-X grammar demoted to closure-only",
        "next_3440": "machine-readable 3441 target",
        "forbidden_vertices_3440": "linear-X vertices that can produce finite B_HX",
        "closure_demotion_3440": "B_i=0 closure-only status",
        "bhx_route_3440": "finite B_HX route retained",
        "bhx_input_3439": "prior clean/fallback B_HX row source",
        "metric_mixing_3438": "Schur/metric-mixing formula source",
        "alpha_template_3438": "R10 alpha numerator template",
        "moms_doc_1088": "ordinary matter signature proof attempt",
        "moms_clause_1088": "minimal ordinary matter signature clauses",
        "moms_theorem_1088": "conditional zero theorem for J_X/qbar_XT",
        "moms_countermodels_1088": "surviving ordinary-sector countermodels",
        "matter_pullback_doc_1044": "matter-pullback chain-rule derivation",
        "matter_pullback_1044": "qbar_XT exact conditional theorem",
        "qbar_components_1044": "absolute component envelope for qbar_XT",
        "qbar_fallback_1044": "R10/WEP/clock fallback observable map",
        "public_metric_doc_1030": "single public metric/no-shadow-frame contract",
        "public_metric_contract_1030": "public metric parent-action contract",
        "cg_provenance_1030": "finite c_g/tau provenance gates",
        "local_bounds": "local arena bound anchors: WEP, Cassini gamma, R10",
    }
    rows = []
    for source_id, path in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": roles[source_id],
                "valid_for_claim": False,
            }
        )
    return rows


def channel_selection() -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "OC3441_trace_mass_source",
            "selected_field_projection": "X_T := local scalar/trace projection of the finite MTS X-sector",
            "why_this_channel": "it is the minimal branch that can spoil Newton/GR through ordinary mass density and is directly visible to R10, Cassini PPN gamma, WEP/source-charge and measured-GM tests",
            "3440_vertices_hit": "FV3440_0_XR;FV3440_1_XT;FV3440_3_class_metric;FV3440_5_effective_readout",
            "zero_target": "C_trace=0 and B_HX^trace=0",
            "finite_target": "source-normalized C_trace coefficient pack with no-cancellation absolute envelope",
            "status": "SELECTED_FOR_ONE_CHANNEL_ATTACK",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def one_channel_proof_attempt() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "OCP3441_0_parent_signature_assumption",
            "step": "assume the ordinary matter parent signature",
            "derivation": "S_matter=sum_A S_A[Psi_A,e_pub(q(Phi)),omega[e_pub],A_obs(q(Phi)),theta_A] with no X_T, no A_X(X_T)g_pub, no w_A(X_T), and variation before readout",
            "result_if_signed": "delta_X S_matter=0 up to owned gauge/boundary terms",
            "current_status": "CONDITIONAL_ONLY_SOURCE_1088_1044_1030",
            "blocks_promotion": "minimal ordinary matter functor, no-shadow-frame slot, and current/source normalization owner are not parent-signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCP3441_1_even_local_X_block",
            "step": "try to kill the geometric part",
            "derivation": "S_XT=-1/2 int sqrt(-g)[Z_T nabla X_T nabla X_T + M_T^2 X_T^2]+O(X_T^2 R) is even in X_T about X_T=0",
            "result_if_signed": "delta_X S_XT|0=0 and delta_h delta_X S_XT|0=0",
            "current_status": "CONDITIONAL_ONLY_SOURCE_3439_3440",
            "blocks_promotion": "the parent grammar has not forbidden odd/linear X_T R, X_T T, source-weight, boundary, or readout terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCP3441_2_trace_current_chain_rule",
            "step": "apply matter pullback identity",
            "derivation": "delta_v S_T = 1/2 int sqrt(-g) T^{mu nu} Lie_v g_m,munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge terms",
            "result_if_signed": "Lie_v g_m=0, Lie_v theta=0, and silent boundary imply qbar_XT=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM_SOURCE_1044",
            "blocks_promotion": "geometry pullback, constant superselection and boundary support silence are all unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCP3441_3_BHX_zero_condition",
            "step": "differentiate parent action twice",
            "derivation": "B_HX^trace := delta_h delta_X S_parent|0 vanishes if no term linear in X_T has a metric/source/readout variation",
            "result_if_signed": "B_HX^trace=0 and alpha_trace(lambda)=0 in this channel",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "blocks_promotion": "X_T R, X_T T, common conformal frame, source-only normalization and boundary/source support tails remain legal countervertices",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCP3441_4_current_verdict",
            "step": "compare against current corpus",
            "derivation": "the theorem shape is correct, but the parent object-language does not yet rule out the finite trace channel",
            "result_if_signed": "one-channel local trace branch would close cleanly",
            "current_status": "ZERO_PROOF_NOT_PROMOTED",
            "blocks_promotion": "C_trace must be derived zero in a parent action or bounded as a finite coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def trace_coefficient_definition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CT3441_0_C_trace",
            "symbol": "C_trace",
            "definition": "C_trace := C_XR + C_XT + C_conf + C_src + C_bdy, evaluated in one fixed parent branch and one source-normalization convention",
            "formula_or_bound": "|C_trace| <= |C_XR|+|C_XT|+|C_conf|+|C_src|+|C_bdy|",
            "required_parent_input": "same-branch coefficient values, units, source paths, and no-cancellation guard",
            "current_value": "MISSING_COMPONENT_VALUES",
            "status": "ABSOLUTE_ENVELOPE_DEFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CT3441_1_C_XR",
            "symbol": "C_XR",
            "definition": "linear curvature vertex contribution from int sqrt(-g) b_R X_T R[g]",
            "formula_or_bound": "C_XR := projection_R10_PPN[b_R delta R/delta h] or theorem-zero if X_T R is parent-forbidden",
            "required_parent_input": "b_R, X_T normalization, curvature convention, source path, equation reference",
            "current_value": "MISSING_b_R",
            "status": "MISSING_LINEAR_CURVATURE_COEFFICIENT_OR_ZERO_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CT3441_2_C_XT",
            "symbol": "C_XT",
            "definition": "direct ordinary trace coupling from int sqrt(-g) b_T X_T T_obs",
            "formula_or_bound": "C_XT := b_T after fixing T_obs normalization",
            "required_parent_input": "b_T, T_obs convention, branch id, source path",
            "current_value": "MISSING_b_T",
            "status": "MISSING_DIRECT_TRACE_COEFFICIENT_OR_NO_TRACE_SLOT_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CT3441_3_C_conf",
            "symbol": "C_conf",
            "definition": "common conformal shadow-frame contribution from g_m=exp(2 a_T X_T) g_pub",
            "formula_or_bound": "C_conf := a_T for nonrelativistic trace response, with sign convention fixed by S_matter variation",
            "required_parent_input": "a_T or terminal-public-metric/no-shadow-frame theorem",
            "current_value": "MISSING_a_T",
            "status": "MISSING_COMMON_FRAME_COEFFICIENT_OR_TERMINAL_METRIC_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CT3441_4_C_src",
            "symbol": "C_src",
            "definition": "source-only normalization leak from kappa(X_T), G_eff(X_T), M_eff(X_T), or species/source weights",
            "formula_or_bound": "C_src := partial_X ln(kappa_eff M_eff) in the same branch, or zero by source-owner theorem",
            "required_parent_input": "source owner, measured-GM convention, conserved parent mass flux, source path",
            "current_value": "MISSING_SOURCE_OWNER_DERIVATIVE",
            "status": "MISSING_SOURCE_NORMALIZATION_COEFFICIENT_OR_OWNER_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "CT3441_5_C_bdy",
            "symbol": "C_bdy",
            "definition": "boundary/domain/readout/source-support contribution linear in X_T",
            "formula_or_bound": "C_bdy := local projection of boundary/domain/readout X_T current, or zero by exact/topological silence",
            "required_parent_input": "boundary class, support variation, projector/readout order, source path",
            "current_value": "MISSING_BOUNDARY_DOMAIN_READOUT_COEFFICIENT",
            "status": "MISSING_BOUNDARY_ZERO_OR_NUMERIC_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bhx_coefficient_pack() -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "BHP3441_0_quadratic_action_template",
            "quantity": "S_trace_quad",
            "formula": "S=-1/2 int sqrt(-g)[Z_T (partial X_T)^2 + M_T^2 X_T^2] + int sqrt(-g) X_T[C_XR R + C_XT T_obs + C_conf T_obs + C_src T_source + C_bdy]",
            "required_columns": "branch_id;Z_T;M_T2;lambda_T_m;C_XR;C_XT;C_conf;C_src;C_bdy;units;source_paths;equation_refs;valid_for_claim",
            "status": "SOURCE_READY_TEMPLATE_VALUES_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "pack_id": "BHP3441_1_BHX_formula",
            "quantity": "B_HX^trace",
            "formula": "B_HX^trace = delta_h int sqrt(-g)[C_XR R + (C_XT+C_conf+C_src)T_obs + C_bdy]|background",
            "required_columns": "weak-field gauge;T_obs convention;R convention;source worldtube;operator normalization;no-cancellation envelope",
            "status": "FORMULA_DERIVED_NUMERIC_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "pack_id": "BHP3441_2_profile_equation",
            "quantity": "X_T local profile",
            "formula": "(Z_T nabla^2 - M_T^2) X_T = -[C_trace rho_obs + C_XR R_lin + C_bdy_source] in weak static limit",
            "required_columns": "Z_T;M_T2;lambda_T_m;rho_obs normalization;R_lin convention;boundary/source support",
            "status": "PROFILE_READY_BUT_COEFFICIENTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "pack_id": "BHP3441_3_R10_alpha",
            "quantity": "alpha_trace(lambda_T)",
            "formula": "alpha_trace(lambda_T)=K_R10(lambda_T) Qbar_XH^trace(lambda_T) qbar_XT^trace /(4*pi*G_obs*Z_T)",
            "required_columns": "K_R10;Qbar_XH^trace;qbar_XT^trace;Z_T;lambda_T_m;R10 bound curve;source paths",
            "status": "MATCHES_3438_1044_TEMPLATE_VALUES_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "pack_id": "BHP3441_4_PPN_vector",
            "quantity": "r_PPN^trace",
            "formula": "r_PPN^trace=(gamma-1,beta-1,alpha1,alpha2,xi,Gdot/G)_trace = Pi_PPN[Z_T,M_T2,C_trace,screening,readout]",
            "required_columns": "PPN projection matrix;gauge;screening rule;source normalization;Cassini/LLR bound rows",
            "status": "ARENA_PROJECTION_MATRIX_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def r10_ppn_score_interface() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "SPI3441_0_R10",
            "arena": "R10 inverse-square/fifth-force",
            "bound_anchor": "local_bound_claims.csv:R10_fifth_force plus promoted alpha(lambda) curve",
            "mts_quantity": "alpha_trace(lambda_T)",
            "required_inputs": "lambda_T_m;Z_T;C_trace or theorem-zero;K_R10;Qbar_XH^trace;qbar_XT^trace;claim-valid bound curve",
            "current_status": "BOUND_ANCHOR_EXISTS_MTS_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "SPI3441_1_Cassini_gamma",
            "arena": "PPN gamma / Shapiro delay",
            "bound_anchor": "local_bound_claims.csv:R3_gamma",
            "mts_quantity": "(gamma-1)_trace",
            "required_inputs": "common-frame coefficient C_conf or theorem-zero;range/screening;PPN projection matrix",
            "current_status": "BOUND_ANCHOR_EXISTS_PPN_PROJECTION_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "SPI3441_2_WEP_source_charge",
            "arena": "MICROSCOPE/source-charge proxy",
            "bound_anchor": "local_bound_claims.csv:R1_WEP_source_charge",
            "mts_quantity": "Delta qbar_XT^trace and source/test material response",
            "required_inputs": "material sensitivities;source vector;C_src/C_conf split;no-cancellation guard",
            "current_status": "BOUND_ANCHOR_EXISTS_MATERIAL_VECTOR_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "SPI3441_3_Newton_GM",
            "arena": "Newtonian source normalization / measured GM",
            "bound_anchor": "local_bound_claims.csv:R9_Gdot plus source-normalization residual ledgers",
            "mts_quantity": "C_src and effective G/M source drift",
            "required_inputs": "kappa_eff derivative;M_eff flux theorem;measured-GM calibration convention",
            "current_status": "SOURCE_OWNER_AND_FLUX_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def newton_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "NGI3441_0_if_zero_signed",
            "condition": "C_trace=0, B_HX^trace=0, qbar_XT^trace=0, and no boundary/readout tail",
            "consequence": "ordinary trace channel cannot add a Yukawa fifth force or common scalar PPN gamma slip",
            "what_remains": "left-hand EH/Newton limit, EM stress/Hilbert source, memory/projector/domain residuals",
            "status": "CLEAN_LOCAL_GR_BRIDGE_COMPONENT_IF_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "impact_id": "NGI3441_1_if_finite",
            "condition": "any C_trace component survives",
            "consequence": "local GR/Newton can still survive only by bounding the induced R10/PPN/WEP residual vector below empirical limits",
            "what_remains": "source-backed values for Z_T, M_T2, C_trace components, arena projections",
            "status": "FINITE_BOUND_ROUTE_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "impact_id": "NGI3441_2_project_status",
            "condition": "current corpus",
            "consequence": "one major coupling gap is now compressed into a trace coefficient vector instead of a vague local-GR complaint",
            "what_remains": "derive terminal public metric/no-shadow trace slot or fill/bound C_trace",
            "status": "FORWARD_PROGRESS_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3441_0_sources",
            "claim": "all 3441 local sources exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3441_1_zero_theorem",
            "claim": "ordinary trace channel has parent-signed C_trace=0",
            "gate_pass": False,
            "reason": "MOMS/SPM/no-shadow/source-owner clauses remain conditional, not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3441_2_finite_pack",
            "claim": "finite trace coefficient pack can be scored",
            "gate_pass": False,
            "reason": "C_trace components, Z_T, M_T2, lambda_T and PPN/R10 projections are not numeric/source-backed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3441_3_local_GR",
            "claim": "local GR/Newton source coupling is established",
            "gate_pass": False,
            "reason": "one channel is formalized, but zero theorem/bound and left-hand EH/Newton gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3441_0_channel",
            "decision": "Attack the ordinary trace/mass-source scalar channel first.",
            "because": "it is the smallest channel that can directly affect Newtonian source coupling, PPN gamma and R10 Yukawa strength",
            "next_action": "derive or bound C_trace rather than auditing every local residual at once",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3441_1_zero_route",
            "decision": "Do not promote C_trace=0.",
            "because": "the proof is exact only under parent-signed no-XT/no-XR/no-shadow/source-owner grammar",
            "next_action": "try the strongest subclause first: common conformal trace coefficient C_conf",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3441_2_finite_route",
            "decision": "Keep the finite branch executable.",
            "because": "if C_trace is nonzero, R10/PPN/WEP can bound it; this is the honest alternative to closure",
            "next_action": "turn C_conf into either a terminal-public-metric zero theorem or a Cassini/R10 bound input",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3442-Y5-R2FR-common-conformal-trace-coefficient-zero-or-Cassini-R10-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3442_common_conformal_trace_coefficient_zero_or_Cassini_R10_bound_input.py",
            "objective": "try to derive C_conf=a_T=0 from terminal public metric/no-shadow-frame naturality; if that fails, stage a nonclaim Cassini/R10/WEP bound input for the common trace coefficient",
            "success_condition": "C_conf is either parent-signed zero for the selected channel or represented by a schema-valid nonclaim bound row linked to R3_gamma/R10/R1",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3441_0_trace_channel",
            "branch_id": "OC3441_trace_mass_source",
            "zero_claim": False,
            "finite_score": False,
            "result": "NOT_SCORED",
            "why": "zero proof is conditional and finite coefficient values are missing",
            "valid_for_claim": False,
        }
    ]


def local_bound_row_ids() -> set[str]:
    return {row.get("row_id", "") for row in read_csv(LOCAL_BOUNDS)}


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if row.get("valid_for_claim") is True or str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if row.get("claim_allowed") is True or str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    bound_ids = local_bound_row_ids()
    validations = [
        {
            "check_id": "VAL3441_0_sources_exist",
            "condition": "all cited 3441 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3441_1_selected_one_channel",
            "condition": "exactly one finite local channel is selected",
            "passed": len(rows_by_name["channel_selection"]) == 1 and rows_by_name["channel_selection"][0]["channel_id"] == "OC3441_trace_mass_source",
            "detail": rows_by_name["channel_selection"][0]["channel_id"],
        },
        {
            "check_id": "VAL3441_2_zero_not_overclaimed",
            "condition": "zero theorem remains conditional and not promoted",
            "passed": any(row["proof_id"] == "OCP3441_4_current_verdict" and row["current_status"] == "ZERO_PROOF_NOT_PROMOTED" for row in rows_by_name["one_channel_proof_attempt"]),
            "detail": "C_trace=0 not claimed",
        },
        {
            "check_id": "VAL3441_3_trace_components_complete",
            "condition": "C_trace absolute envelope contains all retained components",
            "passed": {"CT3441_1_C_XR", "CT3441_2_C_XT", "CT3441_3_C_conf", "CT3441_4_C_src", "CT3441_5_C_bdy"}.issubset(
                {row["component_id"] for row in rows_by_name["trace_coefficient_definition"]}
            ),
            "detail": "XR/XT/common-frame/source/boundary components retained",
        },
        {
            "check_id": "VAL3441_4_bhx_pack_ready_not_score_ready",
            "condition": "finite B_HX pack exists but is not numerically score-ready",
            "passed": any(row["pack_id"] == "BHP3441_1_BHX_formula" for row in rows_by_name["bhx_coefficient_pack"])
            and all(row["score_ready"] is False for row in rows_by_name["bhx_coefficient_pack"]),
            "detail": "formula pack exists; values missing",
        },
        {
            "check_id": "VAL3441_5_bound_anchors_available",
            "condition": "local bound anchors for WEP, Cassini gamma and R10 are present",
            "passed": {"R1_WEP_source_charge", "R3_gamma", "R10_fifth_force"}.issubset(bound_ids),
            "detail": "R1/R3/R10 anchors checked",
        },
        {
            "check_id": "VAL3441_6_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3441_7_next_target",
            "condition": "next target attacks C_conf rather than broad recircling",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3442-Y5-R2FR-common-conformal-trace-coefficient"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3441_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3441_9_overall",
            "condition": "3441 one-channel trace-coupling checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3441 - One-Channel No-Linear-X Signature or BHX Coefficient Pack

## Summary
- This checkpoint stops the local-GR coupling hunt from spreading sideways and selects one concrete channel: the ordinary trace/mass-source scalar projection `X_T`.
- The attempted zero theorem is exact but conditional: if ordinary matter only sees the terminal public metric/coframe and the parent grammar forbids `X_T R`, `X_T T`, shadow-frame, source-weight, boundary and readout slots, then `C_trace=0` and `B_HX^trace=0`.
- The current corpus does not sign those clauses, so no local-GR, Newton, R10 or PPN pass is claimed.
- The forward progress is that the finite obstruction is now compressed into a scoreable coefficient vector `C_trace = C_XR + C_XT + C_conf + C_src + C_bdy`.
- The next step is not another broad audit: attack `C_conf` first, because it is the common conformal trace coefficient that Cassini gamma and R10 can hit hardest if it survives.

## Source Register
{md_table(rows_by_name["source_register"])}

## Channel Selection
{md_table(rows_by_name["channel_selection"])}

## One-Channel Proof Attempt
{md_table(rows_by_name["one_channel_proof_attempt"])}

## Trace Coupling Coefficient Definition
{md_table(rows_by_name["trace_coefficient_definition"])}

## BHX Coefficient Pack
{md_table(rows_by_name["bhx_coefficient_pack"])}

## R10 / PPN Score Interface
{md_table(rows_by_name["r10_ppn_score_interface"])}

## Newton / GR Impact
{md_table(rows_by_name["newton_gr_impact"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is the useful kind of narrowing: not "we do not know coupling" in the fog, but "derive or bound `C_trace`, starting with `C_conf`." If `C_conf` is killed by terminal-public-metric naturality, the local-GR route gains a real theorem brick. If it survives, Cassini/R10/WEP become the immediate boxing judges for how small it must be.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "channel_selection": channel_selection(),
        "one_channel_proof_attempt": one_channel_proof_attempt(),
        "trace_coefficient_definition": trace_coefficient_definition(),
        "bhx_coefficient_pack": bhx_coefficient_pack(),
        "r10_ppn_score_interface": r10_ppn_score_interface(),
        "newton_gr_impact": newton_gr_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3441 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
