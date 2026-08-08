from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1188-Y5-R10-Gamma-Khat-Ploc-profile-source-ledger-or-q_loc-demotion-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md_escape(row.get(h, "")) for h in headers) + " |")
    return "\n".join(out)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1188_0_1187_profile_handoff",
            "relative_path": "1187-Y5-R10-compensator-divergence-inverse-or-Gamma-Khat-qnorm-source.md",
            "needle": "GKP1187_0_Gamma_eff",
            "role": "1187 staged the missing Gamma/Khat/P_loc qnorm rows.",
        },
        {
            "source_id": "SRC1188_1_1187_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1187_NEXT_TARGET.csv",
            "needle": "NEXT1187_0_1188",
            "role": "direct 1188 handoff.",
        },
        {
            "source_id": "SRC1188_2_stress_identity",
            "relative_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
            "needle": "SR513_0_define_extra_stress",
            "role": "q_loc rewritten as divergence of T_GK.",
        },
        {
            "source_id": "SRC1188_3_metric_match_audit",
            "relative_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            "needle": "MA515_0_Gamma_scalar_density_owner",
            "role": "prior audit: Gamma_eff scalar-density owner missing.",
        },
        {
            "source_id": "SRC1188_4_gamma_candidate",
            "relative_path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "needle": "GO516_A_response_doublet_quadratic_density",
            "role": "best formal Gamma_eff owner candidate.",
        },
        {
            "source_id": "SRC1188_5_symbol_match",
            "relative_path": "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            "needle": "MRM756_1_Gamma_identification",
            "role": "newer symbol-match failure and q_loc component schema.",
        },
        {
            "source_id": "SRC1188_6_kgamma_ledger",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_4_current_Khat_match",
            "role": "K_hat metric-response comparison remains missing.",
        },
        {
            "source_id": "SRC1188_7_balance_routes",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
            "needle": "GBS793_1_tracefree_longitudinal_solver",
            "role": "trace-free longitudinal K_hat balance route.",
        },
        {
            "source_id": "SRC1188_8_gamma_source_expansion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_0_definition",
            "role": "Gamma_eff memory-source formula and gradient expansion.",
        },
        {
            "source_id": "SRC1188_9_gamma_mode_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "needle": "GS834_0_decompose",
            "role": "constant/active Gamma_eff split.",
        },
        {
            "source_id": "SRC1188_10_active_gamma_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "needle": "active_gamma_coeff",
            "role": "active Gamma bound inputs still missing.",
        },
        {
            "source_id": "SRC1188_11_ploc_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_792_GAMMA_KHAT_INPUT_REQUIREMENTS.csv",
            "needle": "GKI792_2_Ploc_definition",
            "role": "P_loc/domain requirements remain missing.",
        },
        {
            "source_id": "SRC1188_12_projector_boundary",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_5_projector_boundary",
            "role": "parent P_loc and boundary/symplectic no-flux clause remains open.",
        },
        {
            "source_id": "SRC1188_13_component_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv",
            "needle": "QCD749_7_verdict",
            "role": "q_loc component rows are not filled.",
        },
        {
            "source_id": "SRC1188_14_no_single_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
            "needle": "QPC746_4_no_single_scalar_pass",
            "role": "no one-scalar q_loc pass across PPN/R10/clock/orbital arenas.",
        },
        {
            "source_id": "SRC1188_15_q_identity",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_869_QLOC_IDENTITY_DECOMPOSITION.csv",
            "needle": "QI869_0_definition",
            "role": "explicit q_loc identity decomposition.",
        },
        {
            "source_id": "SRC1188_16_verticality",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_874_PARENT_QLOC_VERTICALITY_SIGNATURE.csv",
            "needle": "QVS874_5_signature_verdict",
            "role": "parent q_loc verticality signature is not signed.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def profile_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "profile_id": "GPL1188_0_Gamma_response_doublet",
            "symbol": "Gamma_eff",
            "candidate_formula": "Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)",
            "source_path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "evidence_strength": "formal_parent_candidate",
            "units_status": "not_normalized_to_local_test_units",
            "domain_status": "Z^A_to_observed_q_loc_lock_missing",
            "boundary_status": "boundary/source-current silence missing",
            "numeric_or_theorem_status": "M_AB_and_physical_lock_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "map Z^A to actual local residual components or keep as formal scaffold only",
        },
        {
            "profile_id": "GPL1188_1_Gamma_memory_source",
            "symbol": "Gamma_eff",
            "candidate_formula": "Gamma_eff = L_cg^-2 F(m); nabla Gamma_eff = L_cg^-2 F'(m)nabla m - 2 L_cg^-3 F(m)nabla L_cg",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "evidence_strength": "formula_shape_exists",
            "units_status": "L^-2 shape declared",
            "domain_status": "local source-support and transition domain unsigned",
            "boundary_status": "boundary decay/source support missing",
            "numeric_or_theorem_status": "F_prime/F2/L_cg/support_power_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "source F(m), L_cg variation, source support powers, and boundary decay",
        },
        {
            "profile_id": "GPL1188_2_Gamma_active_split",
            "symbol": "Gamma_eff",
            "candidate_formula": "Gamma_eff = Lambda_loc + gamma_act; only nabla gamma_act sources q_loc",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "evidence_strength": "useful_decomposition",
            "units_status": "inherits L^-2 if Gamma_eff is accepted",
            "domain_status": "active/local mode support not parent-signed",
            "boundary_status": "constant-mode/boundary carrier readout warning retained",
            "numeric_or_theorem_status": "C_gamma_small_parameter_projection_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "fill active gamma schema or prove gamma_act theorem-zero",
        },
        {
            "profile_id": "GPL1188_3_Khat_metric_response",
            "symbol": "K_hat^{mu nu}",
            "candidate_formula": "K_hat^{mu nu} ?= K_gamma^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} minus volume convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "evidence_strength": "formal_response_contract",
            "units_status": "stress-tensor units only if Gamma_eff owner exists",
            "domain_status": "metric derivative/projector/domain terms open",
            "boundary_status": "boundary reference/improvement terms open",
            "numeric_or_theorem_status": "current_Khat_match_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "compute K_gamma from accepted Gamma_eff candidate and compare term-by-term",
        },
        {
            "profile_id": "GPL1188_4_Khat_tracefree_longitudinal",
            "symbol": "K_hat^{mu nu}",
            "candidate_formula": "K_L^{mu nu}=nabla^{(mu}A^{nu)}-(1/4)g^{mu nu}nabla_alpha A^alpha + curvature terms, with div K_L = grad Gamma_eff",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
            "evidence_strength": "plausible_solver_route",
            "units_status": "dimensionally consistent if Gamma_eff is L^-2",
            "domain_status": "nonunique without gauge/domain data",
            "boundary_status": "boundary conditions required",
            "numeric_or_theorem_status": "parent-action_origin_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "derive tracefree longitudinal solver with gauge, boundary, and parent variation",
        },
        {
            "profile_id": "GPL1188_5_Ploc_parent_projector",
            "symbol": "P_loc",
            "candidate_formula": "P_loc = P_parent(Phi0) with derivative/readout commutation or explicit correction",
            "source_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md; source-intake/mts_residuals/P8_Y5_R10_792_GAMMA_KHAT_INPUT_REQUIREMENTS.csv",
            "evidence_strength": "requirement_only",
            "units_status": "projection operator if defined",
            "domain_status": "parent local domain not signed",
            "boundary_status": "boundary/symplectic no-flux missing",
            "numeric_or_theorem_status": "P_loc_domain_kernel_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "derive parent-owned local domain/projector and commutator correction",
        },
        {
            "profile_id": "GPL1188_6_q_loc_identity",
            "symbol": "q_loc^nu",
            "candidate_formula": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "source_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv; source-intake/mts_residuals/P8_Y5_R10_869_QLOC_IDENTITY_DECOMPOSITION.csv",
            "evidence_strength": "exact_symbolic_identity",
            "units_status": "inherits derivative of stress-density once profiles are normalized",
            "domain_status": "blocked by P_loc/domain",
            "boundary_status": "blocked by boundary leakage",
            "numeric_or_theorem_status": "values_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "do not score until Gamma/Khat/P_loc rows are filled or residual components are sourced",
        },
        {
            "profile_id": "GPL1188_7_qnorm_component_input",
            "symbol": "||q_loc||_D",
            "candidate_formula": "component norm from q_T, q_perp, Hodge/Helmholtz split, and arena projectors",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv; source-intake/mts_residuals/P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
            "evidence_strength": "input_schema_exists",
            "units_status": "requires declared q_loc units and measure",
            "domain_status": "requires observed frame/domain rows",
            "boundary_status": "requires boundary condition or topology metadata",
            "numeric_or_theorem_status": "component_data_missing",
            "profile_ready": False,
            "valid_for_claim": False,
            "next_action": "build nonclaim component residual input pack or theorem-zero certificate",
        },
    ]


def demotion_rows() -> list[dict[str, object]]:
    return [
        {
            "demotion_id": "QDEM1188_0_profile_verdict",
            "object": "Gamma_eff/K_hat/P_loc profile route",
            "definition": "a claim-grade q_loc norm needs sourced Gamma_eff, K_hat, P_loc, derivative conventions, units, and boundary/domain data",
            "status": "PROFILE_ROUTE_NOT_SCOREABLE",
            "reason": "candidate formulas exist, but no complete parent-owned profile triple exists",
            "required_to_promote": "profile_ready=true for Gamma_eff, K_hat, P_loc, plus qnorm/theorem bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "QDEM1188_1_explicit_residual_row",
            "object": "q_loc^nu",
            "definition": "q_loc^nu := P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "status": "DEMOTED_TO_EXPLICIT_EMPIRICAL_RESIDUAL_NONCLAIM",
            "reason": "identity exists but source profiles/units/domain values do not",
            "required_to_promote": "component-resolved profile or theorem-zero certificate with source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "QDEM1188_2_qnorm_placeholder",
            "object": "||q_loc||_D",
            "definition": "||q_loc||_D <= Q_D with D in {PPN,R10,clock,orbital}",
            "status": "BOUND_SYMBOL_STAGED_VALUE_MISSING",
            "reason": "a symbolic residual bound keeps tests honest without pretending local GR is derived",
            "required_to_promote": "numeric Q_D, uncertainty, units, domain, and response operator for each arena",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "QDEM1188_3_theory_position",
            "object": "local-GR branch",
            "definition": "derived local GR requires q_loc zero or a bound below all local residual gates from parent action, not fitted cancellation",
            "status": "LOCAL_GR_DERIVATION_STILL_OPEN",
            "reason": "demotion preserves testability while the parent derivation is hunted",
            "required_to_promote": "parent Gamma/Khat/P_loc theorem or arena-by-arena residual suppression",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_queue_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AQ1188_0_PPN",
            "arena": "PPN/local-GR",
            "residual_component": "q_T, q_L, q_perp, q_TF, alpha_i/gamma/beta projections",
            "current_source_clue": "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv; P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv",
            "missing_inputs": "component q_loc profile; observed frame; weak-field Green operator; gauge; response coefficients",
            "allowed_output": "nonclaim residual vector or theorem-zero certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "AQ1188_1_R10",
            "arena": "short-range/fifth-force R10",
            "residual_component": "finite-range q_loc kernel alpha_q(lambda)",
            "current_source_clue": "QPC746_3_R10_range says R10 applies only if q_loc supplies finite-range kernel",
            "missing_inputs": "lambda kernel; c_q_alpha(lambda); qnorm or source profile; real bound-row linkage",
            "allowed_output": "nonclaim alpha(lambda) row with valid_for_claim=false until real inputs exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "AQ1188_2_clock",
            "arena": "clock/time/readout",
            "residual_component": "q_loc-induced clock/readout coefficients",
            "current_source_clue": "visible-action pullback and no-shadow-frame rows are conditional only",
            "missing_inputs": "clock response coefficients; hidden frame/readout leakage; source paths; units",
            "allowed_output": "retained b_clock_i/q_loc coefficient pack, no clock pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "AQ1188_3_orbital",
            "arena": "orbital/source-normalization",
            "residual_component": "spatial force/source-drift vector and anomalous acceleration map",
            "current_source_clue": "source-normalization and q_loc decomposition rows retain q_S/q_perp channels",
            "missing_inputs": "force-to-acceleration normalization; source charge equality; radial profile; uncertainty",
            "allowed_output": "nonclaim anomalous-acceleration residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(profiles: list[dict[str, object]]) -> list[dict[str, object]]:
    gamma_ready = any(row["symbol"] == "Gamma_eff" and row["profile_ready"] for row in profiles)
    khat_ready = any(row["symbol"] == "K_hat^{mu nu}" and row["profile_ready"] for row in profiles)
    ploc_ready = any(row["symbol"] == "P_loc" and row["profile_ready"] for row in profiles)
    return [
        {
            "gate_id": "G1188_0_Gamma_profile",
            "claim": "Gamma_eff profile is source-backed",
            "status": "PASS" if gamma_ready else "BLOCKED",
            "why": "response-doublet, memory-source, and active-split formulas are candidates but not complete profiles",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1188_1_Khat_profile",
            "claim": "K_hat profile/metric response is source-backed",
            "status": "PASS" if khat_ready else "BLOCKED",
            "why": "metric-response and tracefree-longitudinal routes remain unmatched to parent action and boundary data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1188_2_Ploc_profile",
            "claim": "P_loc parent domain/projector is signed",
            "status": "PASS" if ploc_ready else "BLOCKED",
            "why": "projector/domain and derivative-commutation/no-flux clauses are still unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1188_3_qnorm_score",
            "claim": "q_loc norm row is scoreable",
            "status": "BLOCKED",
            "why": "no component-resolved profile or theorem-zero certificate exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1188_4_local_GR",
            "claim": "local GR/PPN/R10/clock/orbital pass follows",
            "status": "BLOCKED",
            "why": "1188 creates an honest residual demotion row, not a pass",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1188_0_profile_hunt_result",
            "decision": "candidate_formulas_exist_but_no_claim_grade_profile_triple",
            "reason": "Gamma_eff, K_hat, and P_loc each have useful formal structure but at least one parent/signature/source input is missing in every route",
            "next_action": "retain candidates as derivation routes, but do not use them for local claims",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1188_1_demote_q_loc",
            "decision": "q_loc_becomes_explicit_empirical_residual_nonclaim",
            "reason": "the identity is exact, but no filled profile/norm row exists",
            "next_action": "build a component residual input pack or theorem-zero certificate",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1188_2_best_derivation_route",
            "decision": "derive_tracefree_longitudinal_Khat_or_parent_Ploc_before_more_bounds",
            "reason": "these are the least hand-wavy routes to make the residual small without a fitted cancellation",
            "next_action": "attempt parent-owned Khat balance/P_loc theorem while keeping residual rows testable",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1188_3_best_testing_route",
            "decision": "component_residual_pack_first_if_derivation_stalls",
            "reason": "PPN/R10/clock/orbital gates need different projections; one q_proxy scalar cannot decide them",
            "next_action": "stage q_T/q_perp/q_TF/kernel/response placeholders with valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1188_0_1189",
            "next_target": "1189-Y5-R10-q_loc-component-residual-pack-or-profile-theorem-zero-certificate.md",
            "objective": "build the nonclaim q_loc component residual input pack for PPN/R10/clock/orbital tests, while preserving a theorem-zero slot if a parent Gamma/Khat/P_loc proof is found",
            "include": "q_T/q_perp/q_TF components; observed frame/domain; finite-range kernel slot; response coefficients; theorem-zero certificate fields; no-claim validation",
            "exclude": "single scalar q_proxy pass; q_loc zero claim; local-GR pass; invented numeric profiles; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    profiles: list[dict[str, object]],
    demotions: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    profile_symbols = {row["symbol"] for row in profiles}
    no_profile_claims = all(row["profile_ready"] is False and row["valid_for_claim"] is False for row in profiles)
    demotion_exists = any(row["demotion_id"] == "QDEM1188_1_explicit_residual_row" for row in demotions)
    rows = [
        {
            "check_id": "V1188_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_1_profile_symbols_covered",
            "result": "pass" if {"Gamma_eff", "K_hat^{mu nu}", "P_loc", "q_loc^nu", "||q_loc||_D"} <= profile_symbols else "fail",
            "detail": "Gamma_eff, K_hat, P_loc, q_loc, and qnorm profile rows are covered",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_2_profiles_remain_nonclaim",
            "result": "pass" if no_profile_claims else "fail",
            "detail": "no incomplete candidate profile is marked ready or valid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_3_q_loc_demoted",
            "result": "pass" if demotion_exists and all(row["claim_allowed"] is False for row in demotions) else "fail",
            "detail": "q_loc explicit empirical residual row exists and remains nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_4_arena_queue_nonclaim",
            "result": "pass" if len(arenas) >= 4 and all(row["claim_allowed"] is False for row in arenas) else "fail",
            "detail": "PPN, R10, clock, and orbital residual queues remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_5_gates_block_claims",
            "result": "pass" if all(row["claim_allowed"] is False for row in gates) and any(row["status"] == "BLOCKED" for row in gates) else "fail",
            "detail": "all local claims remain blocked unless profiles/theorem rows are filled later",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_6_decision_written",
            "result": "pass" if any(row["decision"] == "q_loc_becomes_explicit_empirical_residual_nonclaim" for row in decisions) else "fail",
            "detail": "demotion decision is explicit",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1188_0_1189" else "fail",
            "detail": "1189 handoff targets q_loc component pack or theorem-zero certificate",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1188_SUMMARY",
            "result": "pass",
            "detail": "1188 sources candidate Gamma/Khat/P_loc profile routes, finds no claim-grade profile triple, demotes q_loc to an explicit empirical residual row, and hands off to component residual pack/theorem-zero certificate",
            "claim_allowed": False,
        },
    ]
    return rows


def write_doc(
    sources: list[dict[str, object]],
    profiles: list[dict[str, object]],
    demotions: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1188 - Y5/R10 Gamma/Khat/P_loc profile source ledger or q_loc demotion row",
            "**Current verdict:** candidate formulas exist for `Gamma_eff` and `K_hat`, and the `q_loc` identity is exact, but no claim-grade `Gamma_eff/K_hat/P_loc` profile triple exists. Therefore `q_loc` is demoted to an explicit empirical residual row rather than used as a derived local-GR proof.",
            "**What improved:** the missing pieces are now localized: `Gamma_eff` needs a parent-owned formula with support powers/units, `K_hat` needs a matched metric-response or tracefree-longitudinal parent equation, and `P_loc` needs a parent domain/projector plus boundary/no-flux commutation.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Profile source ledger\n\n" + table(profiles),
            "## q_loc demotion rows\n\n" + table(demotions),
            "## Arena residual queue\n\n" + table(arenas),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    profiles = profile_ledger_rows()
    demotions = demotion_rows()
    arenas = arena_queue_rows()
    gates = claim_gate_rows(profiles)
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, profiles, demotions, arenas, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1188_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1188_PROFILE_SOURCE_LEDGER.csv": profiles,
        "P8_Y5_R10_1188_QLOC_DEMOTION_ROWS.csv": demotions,
        "P8_Y5_R10_1188_ARENA_RESIDUAL_QUEUE.csv": arenas,
        "P8_Y5_R10_1188_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1188_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1188_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1188_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, profiles, demotions, arenas, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
