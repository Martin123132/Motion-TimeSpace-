from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1365"
TITLE = "1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair-or-q_loc-bound-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
QREPAIR_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_GK_QBASIC_REPAIR_ATTEMPT.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_QLOC_ZERO_THEOREM.csv"
BOUND_ROW_PATH = OUT_DIR / f"{PACK_ID}_QLOC_BOUND_SOURCE_ROW.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1365_VALIDATION.csv"


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
            "source_id": "SRC1365_0_1364_doc",
            "source_path": "1364-Y5-R10-RAB-quotient-basic-parent-action-sector-audit-or-Htau-Href-source-acquisition.md",
            "required_anchor": "NEXT1364_0_1365",
            "purpose": "1364 handoff to Gamma/Khat q-basic repair or q_loc bound row.",
        },
        {
            "source_id": "SRC1365_1_1364_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1364_NEXT_TARGET.csv",
            "required_anchor": "NEXT1364_0_1365",
            "purpose": "machine-readable 1365 target.",
        },
        {
            "source_id": "SRC1365_2_1364_sector_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1364_QUOTIENT_BASIC_SECTOR_AUDIT.csv",
            "required_anchor": "QBA1364_4_Gamma_Khat_extra",
            "purpose": "Gamma/Khat hard-blocker row.",
        },
        {
            "source_id": "SRC1365_3_1010_doc",
            "source_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "required_anchor": "GKT1010_6_verdict",
            "purpose": "previous q_loc zero theorem attempt and residual retention.",
        },
        {
            "source_id": "SRC1365_4_1010_residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv",
            "required_anchor": "QRES1010_0_q_loc_vector",
            "purpose": "q_loc residual definition and observable map.",
        },
        {
            "source_id": "SRC1365_5_metric_response_contract",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "required_anchor": "MR514_1_Khat_metric_response",
            "purpose": "metric-response contract for K_hat.",
        },
        {
            "source_id": "SRC1365_6_metric_response_audit",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            "required_anchor": "MA515_1_Khat_metric_response",
            "purpose": "metric-response match currently fails.",
        },
        {
            "source_id": "SRC1365_7_stress_candidates",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "required_anchor": "GK514_A_metric_response_scalar_density",
            "purpose": "candidate S_GK routes.",
        },
        {
            "source_id": "SRC1365_8_fixed_point_gates",
            "source_path": "source-intake/mts_residuals/P8_GK_LOCAL_FIXED_POINT_GATES.csv",
            "required_anchor": "FG514_3_double_zero",
            "purpose": "local fixed-point/double-zero gates.",
        },
        {
            "source_id": "SRC1365_9_1280_action_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1280_GK_ACTION_EXISTENCE_GATE.csv",
            "required_anchor": "GKA1280_6_verdict",
            "purpose": "recent GK action-existence gate.",
        },
        {
            "source_id": "SRC1365_10_1280_bound_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1280_EPSILON_GK_QLOC_BOUND_CONTRACT.csv",
            "required_anchor": "BND1280_0_definition",
            "purpose": "epsilon_GK_q_loc bound contract.",
        },
        {
            "source_id": "SRC1365_11_1281_profile_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1281_EPSILON_GK_QLOC_PROFILE_TEMPLATE_NONCLAIM.csv",
            "required_anchor": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "purpose": "nonclaim q_loc profile template.",
        },
        {
            "source_id": "SRC1365_12_733_reduced_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_733_REDUCED_GK_OWNER_ATTEMPT.csv",
            "required_anchor": "RGA733_A_hybrid_reduced_scalar_density_owner",
            "purpose": "reduced q-basic owner candidates.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def repair_attempt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "attempt_id": "GKR1365_0_metric_response_scalar_density",
                "route": "S_GK = -int sqrt(-g_obs) gamma(q,nabla q,D,topological data)",
                "required_identity": "Gamma_eff=gamma(q,...) and K_hat^{mu nu}=K_metric^{mu nu}[gamma]",
                "q_basic_status": "CONDITIONAL_FORM_VALID",
                "current_match": "FAIL_CURRENT_SYMBOL_MATCH",
                "what_would_follow": "Gamma_eff and K_hat become one variational object and q_loc becomes a Ward residual.",
                "blocker": "no current scalar-density formula for Gamma_eff and no metric-response derivation of K_hat.",
                "result": "NOT_PROVED_FOR_CURRENT_MTS",
            },
            {
                "attempt_id": "GKR1365_1_response_doublet_density",
                "route": "gamma = gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)",
                "required_identity": "Z fields are q-owned, source-free locally, and K_hat is the metric response of gamma.",
                "q_basic_status": "PROMISING_CONDITIONAL_TEMPLATE",
                "current_match": "FORMAL_CANDIDATE_Y5_Y6_BLOCKED",
                "what_would_follow": "F_1=0/double-zero follows by evenness if Z=0 is a parent local fixed point.",
                "blocker": "source normalization, PPN lock, boundary response, and physical component map remain unsigned.",
                "result": "NOT_PROVED_FOR_CURRENT_MTS",
            },
            {
                "attempt_id": "GKR1365_2_positive_auxiliary_nohair",
                "route": "gamma = V(Phi_red) + 1/2 G_AB nabla Phi_red^A nabla Phi_red^B",
                "required_identity": "positive self-adjoint local operator plus source-free boundary conditions force Phi_red=Phi0.",
                "q_basic_status": "CONDITIONAL_NOHAIR_ROUTE",
                "current_match": "CANDIDATE_NOT_COMPONENT_LOCKED",
                "what_would_follow": "Euler closure plus positive energy identity would make q_loc zero in compact local vacuum.",
                "blocker": "no source-free Euler theorem, no-marker theorem, no-boundary/no-flux certificate for current MTS.",
                "result": "NOT_PROVED_FOR_CURRENT_MTS",
            },
            {
                "attempt_id": "GKR1365_3_topological_improvement",
                "route": "T_GK = divergence/improvement stress or S_GK = int dB_GK",
                "required_identity": "bulk stress vanishes and all boundary/corner/source flux is fixed or zero.",
                "q_basic_status": "CONDITIONAL_TOPOLOGICAL_ROUTE",
                "current_match": "BOUNDARY_RISK_OPEN",
                "what_would_follow": "bulk q_loc can vanish without propagating local auxiliary fields.",
                "blocker": "boundary/source-measure flux, corner symplectic flux, and reference subtraction remain open.",
                "result": "NOT_PROVED_FOR_CURRENT_MTS",
            },
            {
                "attempt_id": "GKR1365_4_plateau_or_bookkeeping_rejected",
                "route": "set q_loc=0 by local plateau or treat Gamma/Khat as bookkeeping stress",
                "required_identity": "none; this is a shortcut not a derivation",
                "q_basic_status": "REJECTED",
                "current_match": "INVALID_ROUTE",
                "what_would_follow": "nothing claimable; it would hide the local-force residual.",
                "blocker": "not an action, not a metric response, not a Helmholtz proof.",
                "result": "REFUSED_SHORTCUT",
            },
            {
                "attempt_id": "GKR1365_5_bound_branch",
                "route": "retain q_loc profile and bound epsilon_GK_q_loc",
                "required_identity": "q_loc_profile, units, P_loc, Gamma/Khat formulas, normalization, arena projection, and threshold are sourced.",
                "q_basic_status": "FALLBACK_REQUIRED",
                "current_match": "PROFILE_AND_NORMALIZATION_MISSING",
                "what_would_follow": "local tests become scoreable only after sourced profile rows replace missing fields.",
                "blocker": "no numeric/symbolic source-backed profile or arena threshold is filled yet.",
                "result": "RETAIN_NONCLAIM_BOUND_ROW",
            },
            {
                "attempt_id": "GKR1365_6_verdict",
                "route": "derive q_loc zero from q-basic Gamma/Khat sector",
                "required_identity": "GKR1365_0 or equivalent route plus Helmholtz, Euler, double-zero, P_loc, and no-flux passes",
                "q_basic_status": "NOT_CLOSED",
                "current_match": "CURRENT_MTS_DOES_NOT_MATCH_S_GK",
                "what_would_follow": "q_loc local-force residual could be theorem-zero and local-GR gates could reopen.",
                "blocker": "metric-response scalar density remains the best route, but no current MTS formula matches it.",
                "result": "QLOC_ZERO_NOT_DERIVED",
            },
        ]
    )


def conditional_theorem_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "theorem_step": "QTZ1365_0_action",
                "hypothesis": "There exists a diffeomorphism-invariant q-basic sector action S_GK[q] = -int sqrt(-g_obs) gamma(q,dq,D) + int dB_GK(q).",
                "derives": "delta S_GK = E_A delta y^A + 1/2 int sqrt(-g) T_GK^{mu nu} delta g_mu nu + boundary",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "missing_to_promote": "explicit gamma/Gamma_eff formula and q map field list",
            },
            {
                "theorem_step": "QTZ1365_1_metric_response",
                "hypothesis": "K_hat^{mu nu} equals the metric-response part of gamma under one fixed sign/volume convention.",
                "derives": "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} and Gamma/Khat are not independent knobs.",
                "current_status": "FAIL_CURRENT_SYMBOL_MATCH",
                "missing_to_promote": "K_hat metric variation calculation including derivative and boundary terms",
            },
            {
                "theorem_step": "QTZ1365_2_Helmholtz",
                "hypothesis": "The proposed T_GK satisfies Helmholtz second-variation symmetry up to fixed boundary terms.",
                "derives": "a local action exists for the stress response rather than a bookkeeping tensor.",
                "current_status": "NOT_CHECKED_FOR_CURRENT_SYMBOLS",
                "missing_to_promote": "antisymmetric second-variation obstruction H_GK",
            },
            {
                "theorem_step": "QTZ1365_3_Ward_identity",
                "hypothesis": "S_GK is diffeomorphism invariant and tau/P_loc are parent-owned.",
                "derives": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) = P_loc(sum_A E_A nabla^nu y^A + boundary/source terms)",
                "current_status": "CONDITIONAL_NOT_SPECIFIC_MATCH",
                "missing_to_promote": "sector-specific Ward identity with P_loc and boundary terms",
            },
            {
                "theorem_step": "QTZ1365_4_Euler_double_zero",
                "hypothesis": "Local compact vacuum obeys E_A=0, source terms vanish, boundary no-flux holds, and T_GK(Phi0)=partial_A T_GK(Phi0)=0 after fixed background subtraction.",
                "derives": "q_loc^nu=0 to the required local order; F_1=0 and no linear PPN/source-normalization hair from this sector.",
                "current_status": "DOUBLE_ZERO_NOT_DERIVED",
                "missing_to_promote": "local fixed-point expansion, positive/no-hair theorem, and no-flux certificate",
            },
            {
                "theorem_step": "QTZ1365_5_verdict",
                "hypothesis": "QTZ1365_0 through QTZ1365_4 all pass with source paths.",
                "derives": "Gamma/Khat sector is q-basic/current-owned and q_loc can be theorem-zero.",
                "current_status": "THEOREM_CONDITIONAL_ONLY",
                "missing_to_promote": "all parent-signature inputs above",
            },
        ]
    )


def bound_source_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "row_id": "QBR1365_0_q_loc_profile",
                "residual_component": "epsilon_GK_q_loc",
                "q_loc_profile_formula": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
                "q_loc_units": "MISSING_Q_LOC_UNITS",
                "norm_definition": "MISSING_LOCAL_NORM_DEFINITION",
                "normalization_reference": "MISSING_A_REF_OR_DIMENSIONLESS_GATE",
                "P_loc_definition": "MISSING_P_LOC_DEFINITION",
                "Gamma_eff_formula": "MISSING_GAMMA_EFF_FORMULA",
                "K_hat_formula": "MISSING_K_HAT_FORMULA",
                "K_metric_formula": "MISSING_K_METRIC_VARIATION_FORMULA",
                "Delta_K_formula": "Delta_K := K_hat - K_metric[Gamma_eff]",
                "Helmholtz_gap": "H_GK := antisymmetric_second_variation_obstruction",
                "source_boundary_gap": "J_GK_plus_B_GK := retained source-current/boundary work",
                "arena_projection": "PPN;clock;orbital;local_GR",
                "bound_threshold": "MISSING_ARENA_BOUND_THRESHOLD",
                "bound_units": "MISSING_BOUND_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "equation_ref": "MISSING_EQUATION_REF",
                "theorem_zero_certificate": "MISSING_PARENT_ZERO_CERTIFICATE",
                "no_cancellation_guard": True,
                "status": "CLAIM_BLOCKED_PROFILE_TEMPLATE",
            },
            {
                "row_id": "QBR1365_1_metric_response_gap",
                "residual_component": "Delta_K",
                "q_loc_profile_formula": "feeds q_loc through -P_loc nabla_mu Delta_K^{mu nu}",
                "q_loc_units": "MISSING_STRESS_DIVERGENCE_UNITS",
                "norm_definition": "MISSING_LOCAL_NORM_DEFINITION",
                "normalization_reference": "MISSING_A_REF_OR_DIMENSIONLESS_GATE",
                "P_loc_definition": "MISSING_P_LOC_DEFINITION",
                "Gamma_eff_formula": "REQUIRED",
                "K_hat_formula": "REQUIRED",
                "K_metric_formula": "REQUIRED",
                "Delta_K_formula": "REQUIRED_NUMERIC_OR_SYMBOLIC_DELTA_K",
                "Helmholtz_gap": "OPTIONAL_IF_METRIC_RESPONSE_PROVES_ACTION",
                "source_boundary_gap": "MISSING_BOUNDARY_TERMS",
                "arena_projection": "PPN;local_GR",
                "bound_threshold": "MISSING_DELTA_K_BOUND",
                "bound_units": "MISSING_BOUND_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "equation_ref": "MISSING_EQUATION_REF",
                "theorem_zero_certificate": "MISSING_METRIC_RESPONSE_CERTIFICATE",
                "no_cancellation_guard": True,
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "row_id": "QBR1365_2_Helmholtz_gap",
                "residual_component": "H_GK",
                "q_loc_profile_formula": "if H_GK != 0, no S_GK exists for the proposed stress",
                "q_loc_units": "MISSING_SECOND_VARIATION_UNITS",
                "norm_definition": "MISSING_HELMHOLTZ_NORM",
                "normalization_reference": "MISSING_REFERENCE",
                "P_loc_definition": "NA",
                "Gamma_eff_formula": "REQUIRED",
                "K_hat_formula": "REQUIRED",
                "K_metric_formula": "REQUIRED",
                "Delta_K_formula": "MISSING_UNTIL_METRIC_RESPONSE",
                "Helmholtz_gap": "REQUIRED_ANTISYMMETRIC_SECOND_VARIATION",
                "source_boundary_gap": "MISSING_BOUNDARY_SYMMETRY",
                "arena_projection": "action_existence;local_GR",
                "bound_threshold": "MISSING_HELMHOLTZ_ACCEPTANCE_THRESHOLD",
                "bound_units": "MISSING_BOUND_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "equation_ref": "MISSING_EQUATION_REF",
                "theorem_zero_certificate": "MISSING_HELMHOLTZ_CERTIFICATE",
                "no_cancellation_guard": True,
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "row_id": "QBR1365_3_source_boundary_gap",
                "residual_component": "J_GK_plus_B_GK",
                "q_loc_profile_formula": "P_loc(source_current_terms + boundary_no_flux_failure)",
                "q_loc_units": "MISSING_FORCE_DENSITY_UNITS",
                "norm_definition": "MISSING_LOCAL_BOUNDARY_NORM",
                "normalization_reference": "MISSING_BOUNDARY_REFERENCE",
                "P_loc_definition": "MISSING_P_LOC_DEFINITION",
                "Gamma_eff_formula": "REQUIRED_IF_SOURCE_CURRENT_FROM_S_GK",
                "K_hat_formula": "REQUIRED_IF_BOUNDARY_FROM_METRIC_RESPONSE",
                "K_metric_formula": "REQUIRED",
                "Delta_K_formula": "MISSING",
                "Helmholtz_gap": "MISSING",
                "source_boundary_gap": "REQUIRED_SOURCE_AND_BOUNDARY_PROFILE",
                "arena_projection": "clock;orbital;PPN;worldtube_source",
                "bound_threshold": "MISSING_BOUNDARY_FLUX_BOUND",
                "bound_units": "MISSING_BOUND_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "equation_ref": "MISSING_EQUATION_REF",
                "theorem_zero_certificate": "MISSING_NO_FLUX_CERTIFICATE",
                "no_cancellation_guard": True,
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "row_id": "QBR1365_4_acceptance_gate",
                "residual_component": "epsilon_GK_q_loc_acceptance",
                "q_loc_profile_formula": "claimable only if theorem_zero_certificate passes or all profile/bound rows are source-backed",
                "q_loc_units": "REQUIRED",
                "norm_definition": "REQUIRED",
                "normalization_reference": "REQUIRED",
                "P_loc_definition": "REQUIRED",
                "Gamma_eff_formula": "REQUIRED",
                "K_hat_formula": "REQUIRED",
                "K_metric_formula": "REQUIRED",
                "Delta_K_formula": "REQUIRED_OR_ZERO_CERTIFICATE",
                "Helmholtz_gap": "REQUIRED_OR_ZERO_CERTIFICATE",
                "source_boundary_gap": "REQUIRED_OR_ZERO_CERTIFICATE",
                "arena_projection": "PPN;clock;orbital;local_GR",
                "bound_threshold": "REQUIRED",
                "bound_units": "REQUIRED",
                "source_path": "REQUIRED_REAL_SOURCE_PATH",
                "source_anchor": "REQUIRED_REAL_SOURCE_ANCHOR",
                "equation_ref": "REQUIRED",
                "theorem_zero_certificate": "PARENT_SIGNED_QLOC_ZERO_OR_SOURCE_BOUND_TRUE",
                "no_cancellation_guard": True,
                "status": "CLAIM_BLOCKED",
            },
        ]
    )


def claim_gates() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1365_0_conditional_qzero_theorem",
                "claim": "if q-basic S_GK, metric response, Helmholtz, Ward, Euler double-zero, and no-flux pass, then q_loc=0",
                "gate_pass": True,
                "reason": "conditional theorem structure is mathematically coherent.",
            },
            {
                "gate_id": "GATE1365_1_current_S_GK_match",
                "claim": "current MTS supplies accepted q-basic S_GK",
                "gate_pass": False,
                "reason": "Gamma_eff scalar-density owner and K_hat metric-response match are missing.",
            },
            {
                "gate_id": "GATE1365_2_current_q_loc_zero",
                "claim": "q_loc is theorem-zero for current MTS",
                "gate_pass": False,
                "reason": "Helmholtz, Ward, Euler double-zero, P_loc ownership, and boundary no-flux remain unsigned.",
            },
            {
                "gate_id": "GATE1365_3_q_loc_bound_score_ready",
                "claim": "q_loc residual bound row can be scored",
                "gate_pass": False,
                "reason": "profile formula, units, norm, normalization, source path, and arena threshold are still missing.",
            },
            {
                "gate_id": "GATE1365_4_shortcuts_rejected",
                "claim": "plateau axiom or bookkeeping stress may set q_loc=0",
                "gate_pass": False,
                "reason": "shortcuts are explicitly refused.",
            },
            {
                "gate_id": "GATE1365_5_local_GR_reopen",
                "claim": "local-GR/PPN/Newton gates can reopen",
                "gate_pass": False,
                "reason": "q_loc remains retained and H_tau/M_H_ref/Pi_M/source equality/matter coupling are still blocked.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1365_0_best_route_metric_response",
                "decision": "Keep metric-response scalar-density S_GK as the best derivation route.",
                "why": "it ties Gamma_eff and K_hat into one variational object and gives a Ward route to q_loc.",
                "next_action": "try to construct an explicit Gamma_eff scalar density on Q_obs and calculate K_metric.",
            },
            {
                "decision_id": "DEC1365_1_current_claim_blocked",
                "decision": "Do not claim q_loc zero for current MTS.",
                "why": "no current formula matches Gamma_eff/K_hat to a q-basic action with Helmholtz and double-zero.",
                "next_action": "retain q_loc as source-facing residual with component gaps Delta_K, H_GK, and source/boundary flux.",
            },
            {
                "decision_id": "DEC1365_2_bound_row_now_concrete",
                "decision": "Use the 1365 q_loc profile row as the next testing intake.",
                "why": "it names exactly which quantities must be sourced before PPN/clock/orbital/local-GR scoring.",
                "next_action": "either fill Gamma_eff/K_hat formulas from corpus or create conservative source-backed q_loc envelopes.",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1365_0_1366",
                "target_file": "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
                "target_script": "scripts/Y5_R10_RAB_Gamma_eff_scalar_density_definition_hunt_or_q_loc_envelope.py",
                "task": "hunt the corpus for an explicit Gamma_eff scalar-density definition that can live on Q_obs and generate K_hat by metric variation; if absent, build the conservative q_loc envelope intake rows",
                "success_condition": "either a source-backed Gamma_eff/K_metric/K_hat match candidate is found, or q_loc envelope rows have units, norm, P_loc, observable map, thresholds, and missing fields explicit",
                "do_not": "do not use plateau axiom, bookkeeping stress, EH-only import, fitted cancellation, local-GR claim, formalization-workbench edits, or GitHub action",
            }
        ]
    )


def validate_outputs(
    sources: list[dict[str, object]],
    repair: list[dict[str, object]],
    theorem: list[dict[str, object]],
    bounds: list[dict[str, object]],
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
        "VAL1365_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in repair if row["attempt_id"] == "GKR1365_6_verdict")
    add(
        "VAL1365_1_qzero_not_promoted",
        "q_loc zero is not promoted for current MTS",
        str(verdict["result"]) == "QLOC_ZERO_NOT_DERIVED" and not bool(verdict["claim_allowed"]),
        str(verdict["blocker"]),
    )

    add(
        "VAL1365_2_conditional_theorem_complete",
        "conditional theorem has action, metric-response, Helmholtz, Ward, Euler/double-zero, and verdict steps",
        {row["theorem_step"] for row in theorem} == {
            "QTZ1365_0_action",
            "QTZ1365_1_metric_response",
            "QTZ1365_2_Helmholtz",
            "QTZ1365_3_Ward_identity",
            "QTZ1365_4_Euler_double_zero",
            "QTZ1365_5_verdict",
        },
        f"theorem_steps={len(theorem)}",
    )

    add(
        "VAL1365_3_shortcuts_refused",
        "plateau/bookkeeping shortcut route is refused",
        any(row["attempt_id"] == "GKR1365_4_plateau_or_bookkeeping_rejected" and row["result"] == "REFUSED_SHORTCUT" for row in repair),
        "plateau and bookkeeping stress are not accepted routes",
    )

    required_bounds = {
        "QBR1365_0_q_loc_profile",
        "QBR1365_1_metric_response_gap",
        "QBR1365_2_Helmholtz_gap",
        "QBR1365_3_source_boundary_gap",
        "QBR1365_4_acceptance_gate",
    }
    add(
        "VAL1365_4_bound_rows_complete",
        "q_loc bound/source rows cover profile, metric gap, Helmholtz gap, source/boundary gap, and acceptance",
        required_bounds.issubset({str(row["row_id"]) for row in bounds}),
        f"bound_rows={len(bounds)}",
    )

    add(
        "VAL1365_5_bounds_nonclaim_missing",
        "q_loc bound rows remain missing or blocked rather than scored",
        all(not row["claim_allowed"] and str(row["status"]) in {"CLAIM_BLOCKED_PROFILE_TEMPLATE", "MISSING_SOURCE_INPUT", "CLAIM_BLOCKED"} for row in bounds),
        ";".join(f"{row['row_id']}={row['status']}" for row in bounds),
    )

    add(
        "VAL1365_6_no_cancellation_guard",
        "all q_loc residual rows keep no-cancellation guard true",
        all(str(row["no_cancellation_guard"]) == "True" or row["no_cancellation_guard"] is True for row in bounds),
        "component residuals cannot cancel each other to pass",
    )

    add(
        "VAL1365_7_claim_gates_block_claim",
        "claim gates block current S_GK, q_loc zero, scoring, shortcuts, and local-GR claims",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1365_0_conditional_qzero_theorem") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + repair + theorem + bounds + gates + decisions + next_target
    add(
        "VAL1365_8_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1365*", "*1365-Y5-R10-RAB-Gamma-Khat*", "*Y5_R10_RAB_Gamma_Khat*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1365_9_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1365_10_next_target_1366",
        "next target routes to Gamma_eff scalar-density hunt or q_loc envelope",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1365_11_overall",
        "overall 1365 validation",
        all(row["status"] == "PASS" for row in validations),
        "1365 keeps q_loc zero conditional and stages source-facing bound rows",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    repair: list[dict[str, object]],
    theorem: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1365 does not derive `q_loc^nu=0` for current MTS. The best route remains a q-basic metric-response scalar-density action `S_GK`, but current corpus evidence does not yet supply `Gamma_eff` as a scalar density or `K_hat` as its metric response.",
            "**Main progress:** the exact theorem route is now isolated from the fallback test route. If `S_GK`, metric-response, Helmholtz, Ward, Euler/double-zero, `P_loc`, and no-flux all close, `q_loc` can go theorem-zero. Until then, `q_loc`, `Delta_K`, `H_GK`, and source/boundary flux stay as explicit nonclaim residual rows.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Gamma/Khat q-basic repair attempt",
            table(["attempt_id", "route", "required_identity", "q_basic_status", "current_match", "what_would_follow", "blocker", "result"], repair),
            "## Conditional qloc-zero theorem",
            table(["theorem_step", "hypothesis", "derives", "current_status", "missing_to_promote"], theorem),
            "## qloc bound/source rows",
            table(
                [
                    "row_id",
                    "residual_component",
                    "q_loc_profile_formula",
                    "q_loc_units",
                    "norm_definition",
                    "normalization_reference",
                    "P_loc_definition",
                    "Gamma_eff_formula",
                    "K_hat_formula",
                    "K_metric_formula",
                    "Delta_K_formula",
                    "Helmholtz_gap",
                    "source_boundary_gap",
                    "arena_projection",
                    "bound_threshold",
                    "source_path",
                    "theorem_zero_certificate",
                    "no_cancellation_guard",
                    "status",
                ],
                bounds,
            ),
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
    repair = repair_attempt_rows()
    theorem = conditional_theorem_rows()
    bounds = bound_source_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, repair, theorem, bounds, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(QREPAIR_ATTEMPT_PATH, repair)
    write_csv(CONDITIONAL_THEOREM_PATH, theorem)
    write_csv(BOUND_ROW_PATH, bounds)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, repair, theorem, bounds, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
