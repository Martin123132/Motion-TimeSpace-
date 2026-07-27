from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1366"
TITLE = "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
HUNT_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_GAMMA_EFF_SCALAR_DENSITY_HUNT_LEDGER.csv"
MATCH_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_KMETRIC_KHAT_MATCH_LEDGER.csv"
ENVELOPE_PATH = OUT_DIR / f"{PACK_ID}_QLOC_ENVELOPE_INTAKE_ROWS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1366_VALIDATION.csv"


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


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1366_0_1365_doc",
            "source_path": "1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair-or-q_loc-bound-source-row.md",
            "required_anchor": "NEXT1365_0_1366",
            "purpose": "1365 handoff to Gamma_eff scalar-density hunt or q_loc envelope.",
        },
        {
            "source_id": "SRC1366_1_1365_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1365_NEXT_TARGET.csv",
            "required_anchor": "NEXT1365_0_1366",
            "purpose": "machine-readable 1366 target.",
        },
        {
            "source_id": "SRC1366_2_1365_qrepair",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1365_GK_QBASIC_REPAIR_ATTEMPT.csv",
            "required_anchor": "GKR1365_6_verdict",
            "purpose": "q_loc zero remains unproved; metric-response scalar density is best route.",
        },
        {
            "source_id": "SRC1366_3_1365_bound_rows",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
            "required_anchor": "QBR1365_0_q_loc_profile",
            "purpose": "q_loc bound source-row requirements.",
        },
        {
            "source_id": "SRC1366_4_798_gamma_expansion",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_0_definition",
            "purpose": "source-backed Gamma_eff=L_cg^-2 F(m) formula shape and gradient expansion.",
        },
        {
            "source_id": "SRC1366_5_1286_response_row",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv",
            "required_anchor": "RFR1286_0_Gamma_memory_scalar_projection",
            "purpose": "first nonclaim response-field scalar row.",
        },
        {
            "source_id": "SRC1366_6_1289_kmetric_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
            "required_anchor": "KVE1289_2_metric_response_kernels",
            "purpose": "K_metric chain-rule expansion and missing kernels.",
        },
        {
            "source_id": "SRC1366_7_776_kgamma_ledger",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_4_current_Khat_match",
            "purpose": "current Khat/Kgamma match is missing.",
        },
        {
            "source_id": "SRC1366_8_1292_doc",
            "source_path": "1292-Y5-R10-RAB-F-form-and-m-Lcg-parent-source-match-or-residual-runner-input.md",
            "required_anchor": "SDA1292_0_F_form",
            "purpose": "generic F source found but strict double-zero adoption rejected.",
        },
        {
            "source_id": "SRC1366_9_1348_doc",
            "source_path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
            "required_anchor": "BEXT1348_1_conditional_calculus",
            "purpose": "memory branch extremum gives conditional F1 zero only.",
        },
        {
            "source_id": "SRC1366_10_1352_doc",
            "source_path": "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md",
            "required_anchor": "RDA1352_1_scalar_density",
            "purpose": "response/displacement quadratic scalar-density route and blockers.",
        },
        {
            "source_id": "SRC1366_11_223_trace_doc",
            "source_path": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
            "required_anchor": "Gamma_eff = -1/4 trace(P)",
            "purpose": "trace/traceless constitutive clue, not derived owner.",
        },
        {
            "source_id": "SRC1366_12_1188_profile_doc",
            "source_path": "1188-Y5-R10-Gamma-Khat-Ploc-profile-source-ledger-or-q_loc-demotion-row.md",
            "required_anchor": "QDEM1188_0_profile_verdict",
            "purpose": "candidate Gamma/Khat/P_loc profile routes exist but no claim-grade triple.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def hunt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "hunt_id": "HUNT1366_0_memory_scalar_formula_shape",
                "candidate": "Gamma_eff = L_cg^-2 F(m)",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
                "source_anchor": "GSE798_0_definition;GSE798_1_gradient_expansion",
                "evidence_type": "source_backed_formula_shape_nonclaim",
                "q_obs_compatibility": "POSSIBLE_IF_m_AND_Lcg_DESCEND_THROUGH_QOBS",
                "units_status": "L^-2_if_F_dimensionless_but_F_units_and_m_units_missing",
                "metric_response_status": "K_METRIC_NOT_COMPUTED_TO_LIVE_KHAT",
                "local_profile_status": "MISSING_LOCAL_DOMAIN_PROFILE_AND_SUPPORT_POWERS",
                "verdict": "FOUND_FORMULA_SHAPE_NOT_CLAIMABLE_SCALAR_DENSITY",
                "next_required": "derive m,L_cg as q-owned local profiles; fix units; compute K_metric and compare to K_hat",
            },
            {
                "hunt_id": "HUNT1366_1_memory_gradient_identity",
                "candidate": "nabla Gamma_eff = L_cg^-2 F'(m)nabla m - 2 L_cg^-3 F(m)nabla L_cg",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
                "source_anchor": "GSE798_1_gradient_expansion",
                "evidence_type": "derived_product_rule_identity_nonclaim",
                "q_obs_compatibility": "USES_m_AND_Lcg_PROFILES_NOT_YET_PARENT_LOCKED",
                "units_status": "inherits HUNT1366_0 caveats",
                "metric_response_status": "gradient_only_not_metric_variation",
                "local_profile_status": "MISSING_pS_pL_pT_TRANSITION_SUPPORT_POWERS",
                "verdict": "USEFUL_FOR_QLOC_ENVELOPE_NOT_ACTION_DENSITY_PROOF",
                "next_required": "derive support powers and local transition width before PPN/clock/orbital envelope scoring",
            },
            {
                "hunt_id": "HUNT1366_2_first_Kmetric_chain_rule",
                "candidate": "delta Gamma_eff=L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg + hidden metric terms",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
                "source_anchor": "KVE1289_1_chain_rule_scalar_variation;KVE1289_2_metric_response_kernels",
                "evidence_type": "first_metric_variation_kernel_shape_nonclaim",
                "q_obs_compatibility": "depends_on_metric_variation_of_m_Lcg_domain_projectors",
                "units_status": "kernel_units_missing",
                "metric_response_status": "KERNELS_Mm_ML_Kconn_Kdomain_Kboundary_NOT_COMPUTABLE",
                "local_profile_status": "not enough to compare K_hat",
                "verdict": "PARTIAL_KMETRIC_ROUTE_NOT_KHAT_MATCH",
                "next_required": "fill M_m^{mu nu}, M_L^{mu nu}, connection/domain/boundary kernels",
            },
            {
                "hunt_id": "HUNT1366_3_response_doublet_quadratic_density",
                "candidate": "Gamma_eff = Gamma0 + 1/2 Z^A M_AB(g,R_even,D,...) Z^B + O(Z^4)",
                "source_path": "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md",
                "source_anchor": "RDA1352_1_scalar_density;MRI1352_2_double_zero",
                "evidence_type": "formal_conditional_scalar_density_template",
                "q_obs_compatibility": "requires_Z_components_equal_physical_q_loc_residual_vector",
                "units_status": "M_AB_units_and_normalization_missing",
                "metric_response_status": "metric identity conditional; live K_hat symbol match blocked",
                "local_profile_status": "Z-source and boundary silence missing",
                "verdict": "PROMISING_DOUBLE_ZERO_ROUTE_NOT_CURRENT_FORMULA",
                "next_required": "component-lock Z^A and prove no linear source/boundary terms",
            },
            {
                "hunt_id": "HUNT1366_4_memory_branch_extremum",
                "candidate": "Gamma_eff=L_cg^-2[F_L+a_F(R(m;X_B)-R(m_L;X_B))]",
                "source_path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
                "source_anchor": "BEXT1348_1_conditional_calculus",
                "evidence_type": "conditional_F1_calculus_nonclaim",
                "q_obs_compatibility": "requires_trace_projection_and_R_m_XB_parent_ownership",
                "units_status": "inherits L_cg/F_units caveats",
                "metric_response_status": "K_MTS_trace_projection_not_parent_derived",
                "local_profile_status": "full gradient debt retained",
                "verdict": "F1_CALCULUS_PASSES_ONLY_UNDER_ANSATZ",
                "next_required": "derive K_MTS trace projection and R(m;X_B), m_L stability from parent variation",
            },
            {
                "hunt_id": "HUNT1366_5_trace_traceless_constitutive_clue",
                "candidate": "Gamma_eff = -1/4 trace(P); Khat^{mu nu}=P^{mu nu}+Gamma_eff g^{mu nu}",
                "source_path": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
                "source_anchor": "Gamma_eff = -1/4 trace(P)",
                "evidence_type": "constitutive_trace_split_clue",
                "q_obs_compatibility": "requires_parent_owned_P_from_MTS_variables",
                "units_status": "P_units_not_declared_as_action_density",
                "metric_response_status": "trace_split_not_metric_variation",
                "local_profile_status": "P owner bottleneck remains",
                "verdict": "USEFUL_SYMBOL_MATCH_CLUE_NOT_SCALAR_DENSITY",
                "next_required": "derive P owner and show its trace/traceless split is Hilbert-stress metric response",
            },
            {
                "hunt_id": "HUNT1366_6_overall",
                "candidate": "claim-grade Gamma_eff scalar-density definition",
                "source_path": "aggregate_hunt",
                "source_anchor": "HUNT1366_0_to_HUNT1366_5",
                "evidence_type": "hunt_verdict",
                "q_obs_compatibility": "not_yet_parent_signed",
                "units_status": "not_complete",
                "metric_response_status": "Khat_match_missing",
                "local_profile_status": "not_score_ready",
                "verdict": "NO_CLAIM_GRADE_SCALAR_DENSITY_FOUND",
                "next_required": "use Gamma_eff=L_cg^-2F(m) as first nonclaim envelope seed or derive Kmetric/Khat match",
            },
        ]
    )


def match_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "match_id": "MATCH1366_0_action_convention",
                "object": "S_Gamma",
                "candidate_expression": "S_Gamma=-int sqrt(-g) Gamma_eff",
                "current_evidence": "KVE1289_0 writes the convention branch nonclaim.",
                "match_status": "CONVENTION_WRITTEN_NOT_CLAIM",
                "missing": "overall sign, volume convention, derivative terms, and Khat equality",
                "residual_if_missing": "Delta_K remains active",
            },
            {
                "match_id": "MATCH1366_1_scalar_chain_variation",
                "object": "delta Gamma_eff",
                "candidate_expression": "L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg",
                "current_evidence": "KVE1289_1 gives the first chain-rule variation.",
                "match_status": "PARTIAL_CHAIN_RULE_ONLY",
                "missing": "delta m/delta g, delta L_cg/delta g, domain/projector/connection/boundary metric dependence",
                "residual_if_missing": "K_conn, K_domain, K_boundary, and M_m/M_L kernels remain uncomputed",
            },
            {
                "match_id": "MATCH1366_2_Kmetric_kernel",
                "object": "Kmetric_chain^{mu nu}",
                "candidate_expression": "C_sign[L_cg^-2 F_prime M_m^{mu nu}-2L_cg^-3F M_L^{mu nu}]+K_conn+K_domain+K_boundary",
                "current_evidence": "KVE1289_2 writes the first symbolic derivative component.",
                "match_status": "KERNEL_ROW_WRITTEN_NOT_COMPUTABLE",
                "missing": "M_m, M_L, K_conn, K_domain, K_boundary, sign convention",
                "residual_if_missing": "Delta_K cannot be bounded or zeroed",
            },
            {
                "match_id": "MATCH1366_3_live_Khat_comparison",
                "object": "K_hat - K_metric[Gamma_eff]",
                "candidate_expression": "Delta_K^{mu nu}:=K_hat^{mu nu}-K_gamma^{mu nu}",
                "current_evidence": "KGL776_4 says current Khat match is missing.",
                "match_status": "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH",
                "missing": "live K_hat tensor components and term-by-term comparison",
                "residual_if_missing": "q_loc keeps -P_loc nabla_mu Delta_K^{mu nu}",
            },
            {
                "match_id": "MATCH1366_4_acceptance",
                "object": "Gamma_eff/Kmetric/Khat promotion",
                "candidate_expression": "Gamma_eff source row plus Kmetric kernels plus Khat equality plus no boundary leak",
                "current_evidence": "all current Kmetric/Khat rows are nonclaim.",
                "match_status": "CLAIM_BLOCKED",
                "missing": "all MATCH1366_0..3 promotion inputs",
                "residual_if_missing": "use q_loc envelope rows",
            },
        ]
    )


def envelope_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "envelope_id": "ENV1366_0_total_epsilon_GK_q_loc",
                "arena": "local_GR_all",
                "quantity": "epsilon_GK_q_loc",
                "formula": "||P_loc(nabla Gamma_eff - div K_hat)||_local / a_ref",
                "seed_source": "HUNT1366_0 Gamma_eff=L_cg^-2F(m); MATCH1366 residuals",
                "units": "MISSING_FORCE_OR_ACCELERATION_NORMALIZATION",
                "norm": "MISSING_LOCAL_NORM",
                "threshold": "MISSING_ARENA_THRESHOLD",
                "required_inputs": "Gamma_eff_profile;Khat_profile;P_loc;Delta_K;H_GK;J_GK_plus_B_GK;a_ref;domain;boundary",
                "current_status": "ENVELOPE_TEMPLATE_NONCLAIM",
                "no_cancellation_guard": True,
            },
            {
                "envelope_id": "ENV1366_1_memory_gradient_envelope",
                "arena": "PPN;clock;orbital",
                "quantity": "epsilon_grad_Gamma",
                "formula": "|P_loc[L_cg^-2 F_prime nabla m - 2L_cg^-3F nabla L_cg]| / a_ref",
                "seed_source": "GSE798_1_gradient_expansion",
                "units": "MISSING_AFTER_F_m_Lcg_UNITS",
                "norm": "MISSING_COMPONENT_NORM",
                "threshold": "MISSING_PPN_CLOCK_ORBITAL_THRESHOLD",
                "required_inputs": "F;F_prime;m_profile;L_cg_profile;pS;pL;pT;transition_width;local_domain",
                "current_status": "PROFILE_MISSING",
                "no_cancellation_guard": True,
            },
            {
                "envelope_id": "ENV1366_2_metric_response_gap_envelope",
                "arena": "PPN;local_GR",
                "quantity": "epsilon_Delta_K",
                "formula": "||P_loc nabla_mu Delta_K^{mu nu}||_local / a_ref",
                "seed_source": "KGL776_4_current_Khat_match;KVE1289_2_metric_response_kernels",
                "units": "MISSING_STRESS_DIVERGENCE_UNITS",
                "norm": "MISSING_DELTAK_NORM",
                "threshold": "MISSING_DELTAK_BOUND",
                "required_inputs": "K_hat;Kmetric;M_m;M_L;K_conn;K_domain;K_boundary;sign_convention",
                "current_status": "KMETRIC_KHAT_MATCH_MISSING",
                "no_cancellation_guard": True,
            },
            {
                "envelope_id": "ENV1366_3_Helmholtz_gap_envelope",
                "arena": "action_existence;local_GR",
                "quantity": "epsilon_H_GK",
                "formula": "||antisym delta(sqrt(-g)T_GK)/delta g|| / H_ref",
                "seed_source": "QBR1365_2_Helmholtz_gap",
                "units": "MISSING_SECOND_VARIATION_UNITS",
                "norm": "MISSING_HELMHOLTZ_NORM",
                "threshold": "MISSING_HELMHOLTZ_THRESHOLD",
                "required_inputs": "T_GK;variation_domain;boundary_symmetry;source_path",
                "current_status": "HELMHOLTZ_NOT_CHECKED_FOR_CURRENT_SYMBOLS",
                "no_cancellation_guard": True,
            },
            {
                "envelope_id": "ENV1366_4_source_boundary_flux_envelope",
                "arena": "clock;orbital;worldtube_source;PPN",
                "quantity": "epsilon_JGKB",
                "formula": "||P_loc(J_GK+B_GK)||_local / a_ref",
                "seed_source": "QBR1365_3_source_boundary_gap",
                "units": "MISSING_FORCE_DENSITY_UNITS",
                "norm": "MISSING_BOUNDARY_NORM",
                "threshold": "MISSING_BOUNDARY_FLUX_BOUND",
                "required_inputs": "source_current;boundary_no_flux;corner_terms;reference_subtraction;domain",
                "current_status": "SOURCE_BOUNDARY_PROFILE_MISSING",
                "no_cancellation_guard": True,
            },
            {
                "envelope_id": "ENV1366_5_acceptance_gate",
                "arena": "all_local_tests",
                "quantity": "q_loc_envelope_acceptance",
                "formula": "claimable only if every envelope row has sourced values or theorem-zero certificates",
                "seed_source": "ENV1366_0_to_ENV1366_4",
                "units": "REQUIRED",
                "norm": "REQUIRED",
                "threshold": "REQUIRED",
                "required_inputs": "no MISSING fields; sources verified; units compatible; no cancellation; arena thresholds sourced",
                "current_status": "CLAIM_BLOCKED",
                "no_cancellation_guard": True,
            },
        ]
    )


def claim_gates() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1366_0_formula_shape_found",
                "claim": "a nonclaim Gamma_eff formula shape exists",
                "gate_pass": True,
                "reason": "Gamma_eff=L_cg^-2F(m) and gradient expansion are source-backed as formula shapes.",
            },
            {
                "gate_id": "GATE1366_1_claim_grade_scalar_density",
                "claim": "current corpus contains a claim-grade q-basic Gamma_eff scalar density",
                "gate_pass": False,
                "reason": "units, q-owned m/L_cg profiles, local domain, support powers, and parent action adoption are missing.",
            },
            {
                "gate_id": "GATE1366_2_Kmetric_Khat_match",
                "claim": "K_hat equals K_metric[Gamma_eff]",
                "gate_pass": False,
                "reason": "metric-response kernels and live K_hat component comparison remain missing.",
            },
            {
                "gate_id": "GATE1366_3_q_loc_envelope_score_ready",
                "claim": "q_loc envelope can be scored against local arenas",
                "gate_pass": False,
                "reason": "units, norms, thresholds, profiles, and source/boundary values are missing.",
            },
            {
                "gate_id": "GATE1366_4_local_GR_reopen",
                "claim": "local-GR/PPN/Newton gates can reopen",
                "gate_pass": False,
                "reason": "Gamma_eff source shape is nonclaim and K_hat/P_loc/H_tau/M_H_ref/source glue remain blocked.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1366_0_formula_shape_is_real_progress",
                "decision": "Retain Gamma_eff=L_cg^-2F(m) as the first live nonclaim scalar seed.",
                "why": "it is source-backed enough to build envelopes, unlike a purely symbolic Gamma placeholder.",
                "next_action": "derive q-owned m/L_cg profiles and compute Kmetric kernels.",
            },
            {
                "decision_id": "DEC1366_1_no_scalar_density_claim",
                "decision": "Do not promote the scalar seed to S_GK.",
                "why": "scalar-density/action status requires units, domain, boundary, parent adoption, and Khat metric response.",
                "next_action": "attack Kmetric memory-scalar chain kernels before any q_loc zero claim.",
            },
            {
                "decision_id": "DEC1366_2_envelope_replaces_guessing",
                "decision": "Use the q_loc envelope intake rows for future local tests.",
                "why": "they expose each missing component instead of hiding it in one q_proxy.",
                "next_action": "fill envelope rows only with sourced profiles, units, and arena thresholds.",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1366_0_1367",
                "target_file": "1367-Y5-R10-RAB-Kmetric-memory-scalar-chain-kernel-or-q_loc-arena-thresholds.md",
                "target_script": "scripts/Y5_R10_RAB_Kmetric_memory_scalar_chain_kernel_or_q_loc_arena_thresholds.py",
                "task": "attempt the first K_metric chain-kernel computation for Gamma_eff=L_cg^-2F(m); if kernels remain missing, source arena thresholds and units for the q_loc envelope rows",
                "success_condition": "either M_m/M_L/K_conn/K_domain/K_boundary rows become source-backed nonclaim kernels, or q_loc envelope thresholds/units are source-acquisition ready",
                "do_not": "do not claim q_loc zero, local GR, EH-only import, fitted cancellation, q_proxy-only pass, formalization-workbench edits, or GitHub action",
            }
        ]
    )


def validate_outputs(
    sources: list[dict[str, object]],
    hunt: list[dict[str, object]],
    matches: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, details: str) -> None:
        validations.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "details": details,
            }
        )

    add(
        "VAL1366_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    memory = next(row for row in hunt if row["hunt_id"] == "HUNT1366_0_memory_scalar_formula_shape")
    add(
        "VAL1366_1_formula_shape_found_nonclaim",
        "Gamma_eff=L_cg^-2F(m) formula shape is found but nonclaim",
        "L_cg^-2 F(m)" in str(memory["candidate"])
        and str(memory["verdict"]) == "FOUND_FORMULA_SHAPE_NOT_CLAIMABLE_SCALAR_DENSITY"
        and not bool(memory["claim_allowed"]),
        str(memory["next_required"]),
    )

    overall = next(row for row in hunt if row["hunt_id"] == "HUNT1366_6_overall")
    add(
        "VAL1366_2_no_claim_grade_scalar_density",
        "no claim-grade Gamma_eff scalar-density definition is promoted",
        str(overall["verdict"]) == "NO_CLAIM_GRADE_SCALAR_DENSITY_FOUND" and not bool(overall["claim_allowed"]),
        str(overall["next_required"]),
    )

    add(
        "VAL1366_3_Kmetric_match_blocked",
        "Kmetric/Khat match ledger keeps Delta_K active",
        any(row["match_id"] == "MATCH1366_3_live_Khat_comparison" and row["match_status"] == "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH" for row in matches),
        ";".join(f"{row['match_id']}={row['match_status']}" for row in matches),
    )

    required_envelopes = {
        "ENV1366_0_total_epsilon_GK_q_loc",
        "ENV1366_1_memory_gradient_envelope",
        "ENV1366_2_metric_response_gap_envelope",
        "ENV1366_3_Helmholtz_gap_envelope",
        "ENV1366_4_source_boundary_flux_envelope",
        "ENV1366_5_acceptance_gate",
    }
    add(
        "VAL1366_4_envelope_rows_complete",
        "q_loc envelope rows cover total, gradient, Delta_K, Helmholtz, source/boundary, and acceptance",
        required_envelopes.issubset({str(row["envelope_id"]) for row in envelopes}),
        f"envelope_rows={len(envelopes)}",
    )

    add(
        "VAL1366_5_envelopes_nonclaim_missing",
        "q_loc envelope rows remain missing or blocked rather than scored",
        all(not row["claim_allowed"] and str(row["current_status"]) in {
            "ENVELOPE_TEMPLATE_NONCLAIM",
            "PROFILE_MISSING",
            "KMETRIC_KHAT_MATCH_MISSING",
            "HELMHOLTZ_NOT_CHECKED_FOR_CURRENT_SYMBOLS",
            "SOURCE_BOUNDARY_PROFILE_MISSING",
            "CLAIM_BLOCKED",
        } for row in envelopes),
        ";".join(f"{row['envelope_id']}={row['current_status']}" for row in envelopes),
    )

    add(
        "VAL1366_6_no_cancellation_guard",
        "all q_loc envelope rows keep no-cancellation guard true",
        all(str(row["no_cancellation_guard"]) == "True" or row["no_cancellation_guard"] is True for row in envelopes),
        "component envelopes cannot cancel each other to pass",
    )

    add(
        "VAL1366_7_claim_gates_block_claim",
        "claim gates block scalar-density, Khat match, q_loc envelope scoring, and local-GR claims",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1366_0_formula_shape_found") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + hunt + matches + envelopes + gates + decisions + next_target
    add(
        "VAL1366_8_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1366*", "*1366-Y5-R10-RAB-Gamma-eff*", "*Y5_R10_RAB_Gamma_eff*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1366_9_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1366_10_next_target_1367",
        "next target routes to Kmetric memory scalar chain-kernel or q_loc arena thresholds",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1367-Y5-R10-RAB-Kmetric-memory-scalar-chain-kernel"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1366_11_overall",
        "overall 1366 validation",
        all(row["status"] == "PASS" for row in validations),
        "1366 finds a nonclaim Gamma_eff formula shape, blocks scalar-density promotion, and stages q_loc envelopes",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    hunt: list[dict[str, object]],
    matches: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1366 finds a real nonclaim formula-shape seed, `Gamma_eff=L_cg^-2 F(m)`, but it does not find a claim-grade q-basic scalar-density action. The missing pieces are still units, q-owned `m/L_cg` profiles, local domain/support powers, boundary/no-flux data, and the term-by-term `K_hat=K_metric[Gamma_eff]` match.",
            "**Main progress:** the local branch is less foggy now. `Gamma_eff` is no longer merely a symbol in this lane; it has one source-backed shape that can drive a conservative `q_loc` envelope. But the envelope, not a local-GR theorem, is the honest current object.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Gamma_eff scalar-density hunt ledger",
            table(
                [
                    "hunt_id",
                    "candidate",
                    "source_path",
                    "source_anchor",
                    "evidence_type",
                    "q_obs_compatibility",
                    "units_status",
                    "metric_response_status",
                    "local_profile_status",
                    "verdict",
                    "next_required",
                ],
                hunt,
            ),
            "## Kmetric/Khat match ledger",
            table(["match_id", "object", "candidate_expression", "current_evidence", "match_status", "missing", "residual_if_missing"], matches),
            "## qloc envelope intake rows",
            table(["envelope_id", "arena", "quantity", "formula", "seed_source", "units", "norm", "threshold", "required_inputs", "current_status", "no_cancellation_guard"], envelopes),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    hunt = hunt_rows()
    matches = match_rows()
    envelopes = envelope_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, hunt, matches, envelopes, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(HUNT_LEDGER_PATH, hunt)
    write_csv(MATCH_LEDGER_PATH, matches)
    write_csv(ENVELOPE_PATH, envelopes)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, hunt, matches, envelopes, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
