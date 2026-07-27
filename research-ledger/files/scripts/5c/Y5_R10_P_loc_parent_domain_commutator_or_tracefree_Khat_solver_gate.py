from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1190-Y5-R10-P_loc-parent-domain-commutator-or-tracefree-Khat-solver-gate.md"
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
            "source_id": "SRC1190_0_1189_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1189_NEXT_TARGET.csv",
            "needle": "NEXT1189_0_1190",
            "role": "direct 1190 handoff.",
        },
        {
            "source_id": "SRC1190_1_1189_certificate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1189_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv",
            "needle": "P_loc_parent_domain",
            "role": "theorem-zero certificate clause that 1190 tries to close.",
        },
        {
            "source_id": "SRC1190_2_794_flat_solver",
            "relative_path": "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
            "needle": "TLS794_2_flat_cancellation",
            "role": "flat tracefree Khat solver cancellation.",
        },
        {
            "source_id": "SRC1190_3_794_curved_open",
            "relative_path": "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
            "needle": "TLS794_3_curved_correction",
            "role": "curved correction is open.",
        },
        {
            "source_id": "SRC1190_4_793_route",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv",
            "needle": "GBS793_1_tracefree_longitudinal_solver",
            "role": "tracefree longitudinal Khat route selected.",
        },
        {
            "source_id": "SRC1190_5_795_origin",
            "relative_path": "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
            "needle": "POA795_4_verdict",
            "role": "parent origin for tracefree Khat solver not adopted.",
        },
        {
            "source_id": "SRC1190_6_795_amplitude",
            "relative_path": "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
            "needle": "KAB795_4_acceptance",
            "role": "K_L amplitude/PPN gate still required.",
        },
        {
            "source_id": "SRC1190_7_834_active_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "needle": "GS834_1_refined_amplitude",
            "role": "active Gamma/Khat carrier amplitude law.",
        },
        {
            "source_id": "SRC1190_8_1010_projector",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_5_projector_boundary",
            "role": "P_loc and boundary/symplectic no-flux remain open.",
        },
        {
            "source_id": "SRC1190_9_874_verticality",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_874_PARENT_QLOC_VERTICALITY_SIGNATURE.csv",
            "needle": "QVS874_5_signature_verdict",
            "role": "q_loc parent verticality signature is not signed.",
        },
        {
            "source_id": "SRC1190_10_1014_commutator",
            "relative_path": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "needle": "PCT1014_2_commutator_zero",
            "role": "projector commutator zero is not derived.",
        },
        {
            "source_id": "SRC1190_11_1019_orthogonality",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "PO1019_5_verdict",
            "role": "projector orthogonality route remains conditional.",
        },
        {
            "source_id": "SRC1190_12_1175_projector_shape",
            "relative_path": "1175-Y5-R10-Qcoh-projector-owner-or-projector-leak-bound-row.md",
            "needle": "QPO1175_4_verdict",
            "role": "SO3/trace projector shape exists but no parent ownership.",
        },
        {
            "source_id": "SRC1190_13_1189_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1189_QLOC_COMPONENT_RESIDUAL_INPUT_PACK.csv",
            "needle": "QPACK1189_4_theorem_zero_override",
            "role": "1189 component residual pack remains fallback.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def khat_solver_rows() -> list[dict[str, object]]:
    return [
        {
            "solver_id": "KLS1190_0_tracefree_definition",
            "statement": "In four dimensions K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu} Box phi is tracefree.",
            "derivation": "g_{mu nu}K_L^{mu nu}=2 Box phi-(1/2)*4 Box phi=0.",
            "result": "EXACT_TRACEFREE_IDENTITY",
            "missing_for_claim": "parent source for phi; boundary conditions; amplitude response",
            "valid_for_claim": False,
        },
        {
            "solver_id": "KLS1190_1_exact_curved_divergence",
            "statement": "For scalar phi, nabla_mu K_L^{mu nu}=(3/2)nabla^nu Box phi + 2 R^nu_sigma nabla^sigma phi, up to Riemann-sign convention.",
            "derivation": "commute nabla_mu nabla^mu nabla^nu phi = nabla^nu Box phi + R^nu_sigma nabla^sigma phi, then subtract (1/2)nabla^nu Box phi.",
            "result": "CURVED_RESIDUAL_DERIVED",
            "missing_for_claim": "sign convention lock; Ricci-term suppression/cancellation; parent equation for phi",
            "valid_for_claim": False,
        },
        {
            "solver_id": "KLS1190_2_covariant_cancellation_condition",
            "statement": "To cancel grad Gamma_eff covariantly, phi must satisfy (3/2)nabla^nu Box phi + 2 R^nu_sigma nabla^sigma phi = nabla^nu Gamma_eff plus any retained boundary/source term.",
            "derivation": "set div K_L equal to grad Gamma_eff in the q_loc identity before projection.",
            "result": "REQUIRED_CURVED_SOURCE_EQUATION_WRITTEN",
            "missing_for_claim": "source equation not derived from parent action; boundary/source term not zeroed",
            "valid_for_claim": False,
        },
        {
            "solver_id": "KLS1190_3_flat_patch_limit",
            "statement": "If Ricci term and boundary/source term are negligible and derivatives commute, Box phi=(2/3)Gamma_eff+C gives div K_L=grad Gamma_eff.",
            "derivation": "drop R^nu_sigma nabla^sigma phi and integrate the gradient equation locally.",
            "result": "FLAT_PATCH_FORMAL_PASS_ONLY",
            "missing_for_claim": "error budget for Ricci, boundary, nonlocal Green function, and local compact domain",
            "valid_for_claim": False,
        },
        {
            "solver_id": "KLS1190_4_amplitude_warning",
            "statement": "The same solution has K_L amplitude of order active Gamma_eff on the transition scale, so q_loc cancellation does not imply local metric safety.",
            "derivation": "Box phi~Gamma_eff implies phi~Gamma_eff L^2 and nabla nabla phi~Gamma_eff.",
            "result": "AMPLITUDE_STILL_LIVE",
            "missing_for_claim": "active Gamma bound; Khat-to-metric response; PPN/R10/clock/orbital response matrix",
            "valid_for_claim": False,
        },
        {
            "solver_id": "KLS1190_5_verdict",
            "statement": "Tracefree Khat solver is a serious mathematical route but not a local-GR theorem.",
            "derivation": "tracefree identity and flat cancellation are exact, but parent origin, curvature, boundary, and amplitude gates remain open.",
            "result": "FORMAL_ROUTE_RETAINED_NO_PROMOTION",
            "missing_for_claim": "parent-owned curved source equation and local metric response bound",
            "valid_for_claim": False,
        },
    ]


def ploc_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "ploc_id": "PLC1190_0_pre_readout_definition",
            "clause": "P_loc must be defined on parent configurations before solving/readout.",
            "mathematical_form": "P_loc[U]: T_Phi C_parent -> T_{q_loc[U](Phi)} Q_loc[U], not a post-fit projection.",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "if_missing": "projected zero can hide unprojected force components",
            "valid_for_claim": False,
        },
        {
            "ploc_id": "PLC1190_1_idempotent_covariant_projector",
            "clause": "P_loc is an idempotent covariant projection with declared domain, kernel, and observed-frame convention.",
            "mathematical_form": "P_loc^2=P_loc, P_loc transforms tensorially, ker(P_loc) is physically classified.",
            "current_status": "MISSING_DOMAIN_KERNEL",
            "if_missing": "different local tests can see different hidden components",
            "valid_for_claim": False,
        },
        {
            "ploc_id": "PLC1190_2_derivative_commutator",
            "clause": "P_loc must commute with the divergence/readout limit or the commutator must be retained.",
            "mathematical_form": "nabla_mu(P_loc^nu_rho K^{mu rho}) = P_loc^nu_rho nabla_mu K^{mu rho} + (nabla_mu P_loc^nu_rho)K^{mu rho}.",
            "current_status": "COMMUTATOR_RESIDUAL_RETAINED",
            "if_missing": "q_loc may vanish after projection while boundary/source flux survives through (nabla P)K",
            "valid_for_claim": False,
        },
        {
            "ploc_id": "PLC1190_3_boundary_no_flux",
            "clause": "boundary/symplectic flux through the compact local boundary must vanish or enter the component pack.",
            "mathematical_form": "integral_{partial U} n_mu P_loc^nu_rho K^{mu rho}=0, or source-backed B_P^nu retained.",
            "current_status": "BOUNDARY_NO_FLUX_UNSIGNED",
            "if_missing": "bulk cancellation does not close local source-measure conservation",
            "valid_for_claim": False,
        },
        {
            "ploc_id": "PLC1190_4_projector_shape_progress",
            "clause": "SO3/trace scalar-irrep projector is the cleanest mathematical projector candidate.",
            "mathematical_form": "stationary SO3 local domain would select scalar/volume trace and make tracefree shear orthogonal.",
            "current_status": "MATH_SHAPE_ONLY_FROM_1175",
            "if_missing": "projector remains smoothing/closure unless domain isotropy and volume measure are parent-owned",
            "valid_for_claim": False,
        },
        {
            "ploc_id": "PLC1190_5_verdict",
            "clause": "P_loc parent-domain theorem is not closed.",
            "mathematical_form": "PLC1190_0 through PLC1190_4 all need parent signatures or retained residual rows.",
            "current_status": "PLOC_PARENT_OWNER_BLOCKED",
            "if_missing": "1189 component residual pack remains the safe local-test interface",
            "valid_for_claim": False,
        },
    ]


def residual_update_rows() -> list[dict[str, object]]:
    return [
        {
            "residual_id": "RES1190_0_Ricci_Khat_residual",
            "source": "tracefree Khat curved divergence",
            "formula": "R_K^nu := 2 R^nu_sigma nabla^sigma phi plus sign-convention/curvature corrections",
            "feeds": "q_loc^nu contains -P_loc R_K^nu unless parent source equation cancels it",
            "status": "RETAINED_NONCLAIM_RESIDUAL",
            "needed_to_score": "Ricci scale; phi gradient bound; sign convention; source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1190_1_projector_commutator",
            "source": "P_loc derivative/readout commutator",
            "formula": "C_P^nu := (nabla_mu P_loc^nu_rho)K^{mu rho}",
            "feeds": "boundary/source flux and component residual pack",
            "status": "RETAINED_NONCLAIM_RESIDUAL",
            "needed_to_score": "P_loc formula; domain variation; Khat profile; boundary measure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1190_2_boundary_flux",
            "source": "compact local boundary",
            "formula": "B_P^nu := integral_{partial U} n_mu P_loc^nu_rho K^{mu rho}",
            "feeds": "PPN alpha_i, orbital/source-normalization, R10 if finite-range support exists",
            "status": "RETAINED_NONCLAIM_RESIDUAL",
            "needed_to_score": "boundary condition; no-flux theorem or finite boundary row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1190_3_Khat_metric_footprint",
            "source": "K_L amplitude",
            "formula": "||K_L|| ~ ||gamma_act||, and ||Khat_H|| <= sqrt(n/(n-1))||gamma_act|| for compatible active modes",
            "feeds": "Newton/PPN gamma beta alpha_i, clock/orbital response, WEP if matter frame sees the carrier",
            "status": "RETAINED_NONCLAIM_RESIDUAL",
            "needed_to_score": "C_gamma, small parameter, support power, metric response matrix",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def certificate_update_rows() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "metric_response_owner",
            "1190_update": "unchanged",
            "new_evidence": "tracefree solver is a Khat candidate but not a Hilbert-stress metric-response owner",
            "passes_after_1190": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "Euler_double_zero",
            "1190_update": "partial_math_only",
            "new_evidence": "flat-patch K_L can cancel grad Gamma_eff algebraically, but phi equation is not parent Euler dynamics",
            "passes_after_1190": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "P_loc_parent_domain",
            "1190_update": "blocked_with_commutator_residual",
            "new_evidence": "P_loc derivative commutator C_P=(nabla P)K must vanish or be retained",
            "passes_after_1190": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "boundary_no_flux",
            "1190_update": "blocked_with_boundary_residual",
            "new_evidence": "bulk cancellation does not silence integral_boundary n.P.K",
            "passes_after_1190": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "arena_projection_silence",
            "1190_update": "blocked_with_component_pack",
            "new_evidence": "1189 residual pack remains required for Ricci, commutator, boundary, and metric-footprint components",
            "passes_after_1190": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1190_0_tracefree_solver",
            "claim": "tracefree Khat solver derives q_loc=0",
            "status": "BLOCKED_FORMAL_ONLY",
            "why": "flat algebra passes, but curved source equation, parent origin, boundary, and amplitude gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1190_1_Ploc_parent",
            "claim": "P_loc is parent-owned and commutes with readout",
            "status": "BLOCKED_COMMUTATOR_RETAINED",
            "why": "P_loc domain/kernel and nabla P commutator are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1190_2_boundary_no_flux",
            "claim": "local boundary flux is silent",
            "status": "BLOCKED_BOUNDARY_RESIDUAL_RETAINED",
            "why": "bulk cancellation does not prove boundary/symplectic no-flux",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1190_3_metric_safety",
            "claim": "Khat carrier is local-metric/PPN safe",
            "status": "BLOCKED_RESPONSE_MATRIX_MISSING",
            "why": "K_L amplitude is of order active Gamma_eff unless sourced small; metric response matrix missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1190_4_local_GR",
            "claim": "local GR/Newton/PPN/R10/clock/orbital pass follows",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why": "1189 component residual pack remains active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1190_0_best_math_progress",
            "decision": "curved_Khat_residual_written_exactly",
            "reason": "the flat solver is real, but its exact curved leakage is now explicit",
            "next_action": "bound or derive away Ricci_Khat residual instead of claiming flat-patch cancellation",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1190_1_Ploc_status",
            "decision": "P_loc_parent_domain_not_closed",
            "reason": "projector shape exists, but pre-readout domain/kernel/commutator/no-flux clauses are unsigned",
            "next_action": "carry C_P and B_P residuals into local component pack unless parent theorem closes",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1190_2_Khat_status",
            "decision": "tracefree_Khat_solver_retained_as_formal_route",
            "reason": "it can cancel divergence without violating tracefree status, but may still gravitate",
            "next_action": "derive parent phi/K_L source or score Khat metric-footprint residual",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1190_3_next_route",
            "decision": "build_curvature_commutator_boundary_residual_bound_pack",
            "reason": "these are now the exact leftovers after the best current derivation attempt",
            "next_action": "1191 should convert R_K, C_P, B_P, and Khat metric footprint into theorem-zero or nonclaim bound rows",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1190_0_1191",
            "next_target": "1191-Y5-R10-curved-Khat-P_loc-commutator-bound-pack-or-parent-zero.md",
            "objective": "derive or bound the exact leftovers from 1190: Ricci Khat residual, P_loc commutator, boundary flux, and Khat metric footprint; keep 1189 component pack active until these are theorem-zero or source-backed",
            "include": "R_K residual; C_P commutator; B_P boundary flux; active Gamma/Khat amplitude; arena projection slots; no-claim validation",
            "exclude": "flat-patch q_loc zero claim; post-readout projector tuning; q_proxy-only pass; local-GR pass; invented numeric profiles; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    khat: list[dict[str, object]],
    ploc: list[dict[str, object]],
    residuals: list[dict[str, object]],
    certs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    khat_ids = {row["solver_id"] for row in khat}
    ploc_ids = {row["ploc_id"] for row in ploc}
    residual_ids = {row["residual_id"] for row in residuals}
    all_nonclaim = all(
        row.get("valid_for_claim") is False
        for row in khat + ploc + residuals + certs + gates + decisions + nexts
    )
    return [
        {
            "check_id": "V1190_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_1_khat_solver_rows",
            "result": "pass" if {"KLS1190_0_tracefree_definition", "KLS1190_1_exact_curved_divergence", "KLS1190_5_verdict"} <= khat_ids else "fail",
            "detail": "tracefree definition, exact curved divergence, and verdict rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_2_ploc_gate_rows",
            "result": "pass" if {"PLC1190_0_pre_readout_definition", "PLC1190_2_derivative_commutator", "PLC1190_5_verdict"} <= ploc_ids else "fail",
            "detail": "P_loc pre-readout, commutator, and verdict gates are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_3_residuals_created",
            "result": "pass" if {"RES1190_0_Ricci_Khat_residual", "RES1190_1_projector_commutator", "RES1190_2_boundary_flux", "RES1190_3_Khat_metric_footprint"} <= residual_ids else "fail",
            "detail": "exact leftover residual rows are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_4_certificate_not_promoted",
            "result": "pass" if all(row["passes_after_1190"] is False for row in certs) else "fail",
            "detail": "theorem-zero certificate remains blocked after 1190",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_5_claim_gates_blocked",
            "result": "pass" if all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all local claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_6_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1190_0_1191" else "fail",
            "detail": "1191 handoff targets curved Khat/P_loc commutator residual bounds or parent-zero theorem",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1190_SUMMARY",
            "result": "pass",
            "detail": "1190 derives the exact curved Khat residual, writes the P_loc commutator/no-flux gate, refuses theorem-zero promotion, and hands off to residual bound pack or parent-zero theorem",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    khat: list[dict[str, object]],
    ploc: list[dict[str, object]],
    residuals: list[dict[str, object]],
    certs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1190 - Y5/R10 P_loc parent-domain commutator or tracefree Khat solver gate",
            "**Current verdict:** the tracefree `K_hat` route is mathematically real but still not a local-GR theorem. 1190 derives the exact curved leftover and isolates the `P_loc` commutator/boundary leakage that must be parent-zero or retained.",
            "**Main progress:** the flat solver becomes a precise residual equation: `nabla_mu K_L^{mu nu}=(3/2)nabla^nu Box phi+2 R^nu_sigma nabla^sigma phi`; therefore Ricci leakage, `P_loc` commutator, boundary flux, and carrier amplitude are the exact next debts.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Tracefree Khat solver gate\n\n" + table(khat),
            "## P_loc parent-domain and commutator gate\n\n" + table(ploc),
            "## Exact residual update rows\n\n" + table(residuals),
            "## Theorem-zero certificate update\n\n" + table(certs),
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
    khat = khat_solver_rows()
    ploc = ploc_gate_rows()
    residuals = residual_update_rows()
    certs = certificate_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, khat, ploc, residuals, certs, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1190_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1190_TRACEFREE_KHAT_SOLVER_GATE.csv": khat,
        "P8_Y5_R10_1190_PLOC_PARENT_COMMUTATOR_GATE.csv": ploc,
        "P8_Y5_R10_1190_EXACT_RESIDUAL_UPDATE_ROWS.csv": residuals,
        "P8_Y5_R10_1190_THEOREM_ZERO_CERTIFICATE_UPDATE.csv": certs,
        "P8_Y5_R10_1190_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1190_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1190_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1190_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, khat, ploc, residuals, certs, gates, decisions, validations, nexts)

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
