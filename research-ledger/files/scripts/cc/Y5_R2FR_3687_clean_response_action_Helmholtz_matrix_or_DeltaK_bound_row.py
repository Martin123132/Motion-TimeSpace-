from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3687"
BRANCH_ID = "MTS_R2FR_Y5_CLEAN_RESPONSE_ACTION_HELMHOLTZ_MATRIX_OR_DELTAK_BOUND_ROW_3687"
DOC = ROOT / "3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3686", RESIDUALS / "P8_Y5_R2FR_3686_NEXT_TARGET.csv", "Delta_K", "3686 selected Helmholtz/Delta_K as next target"),
        ("candidate_3686", RESIDUALS / "P8_Y5_R2FR_3686_RESPONSE_ACTION_CANDIDATE_ROWS.csv", "RAC3686_2_metric_response", "clean response action and K_metric formula"),
        ("gate_3686", RESIDUALS / "P8_Y5_R2FR_3686_HELMHOLTZ_GATE_ROWS.csv", "HLG3686_2_DeltaK_zero", "live Helmholtz and Delta_K gate remains open"),
        ("bound_3686", RESIDUALS / "P8_Y5_R2FR_3686_RGK_ACTION_BOUND_ROWS.csv", "RGB3686_3_DeltaK", "R_Helmholtz/R_DeltaK bound placeholders"),
        ("metric_3627", RESIDUALS / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv", "MRD3627_3_Helmholtz_obstruction", "metric response route and Helmholtz obstruction"),
        ("helmholtz_3627", RESIDUALS / "P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv", "Helmholtz", "S_GK Helmholtz gate from prior pass"),
        ("audit_3432", RESIDUALS / "P8_Y5_R2FR_3432_GAMMA_KHAT_OWNER_AUDIT.csv", "GOA3432_2_integrability", "owner audit says Helmholtz/integrability not checked for live tensor"),
        ("match_2807", RESIDUALS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv", "GKM2807_0_metric_response_identity", "older direct metric-response match failure"),
        ("match_audit", RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "MA515_1_Khat_metric_response", "source audit for Gamma scalar owner and Khat metric response"),
        ("response_variation", RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "AV517_2_first_variation_Z", "response doublet first variation and double-zero"),
        ("response_metric", RESIDUALS / "P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv", "MR517_2_Z_metric_lock", "metric response ledger for response doublet"),
        ("khat_2409", RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv", "KMR2409_2_Khat_identity", "formal variation passes but live Khat identity missing"),
        ("helmholtz_3419", RESIDUALS / "P8_Y5_R2FR_3419_HELMHOLTZ_AUDIT.csv", "HMA3419_0_action_defined_bulk", "bulk Helmholtz closes only in parent response branch"),
        ("coupling_3629", RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv", "CL3629_1_linearized_Z_Euler", "source coupling law for later J_A target"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def helmholtz_matrix_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "HMX3687_0_clean_bulk_operator",
            "field Euler operator",
            "H_AB := delta E_A/delta Y^B - (delta E_B/delta Y^A)^dagger",
            "H_AB^clean_bulk=0 if G_AB=G_BA, M_AB=M_BA, D_mu is G-compatible/self-adjoint after constraints, and boundary adjoint terms vanish.",
            "R_H_clean_bulk := antisym(M_AB)+antisym(G_AB)+D_mu pairing defect+boundary adjoint defect",
            "BULK_HELMHOLTZ_DERIVED_CONDITIONALLY",
            "This is genuine progress: integrability is automatic for the clean action, not a new empirical axiom.",
        ),
        (
            "HMX3687_1_mass_matrix",
            "zeroth-order Helmholtz block",
            "delta(M_AC Y^C)/delta Y^B - adjoint(A<->B) = M_AB - M_BA",
            "M_AB=M_BA",
            "R_H_M := antisym(M_AB)",
            "ZERO_IF_SYMMETRIC_MASS_MATRIX",
            "A parent even response sector must choose a symmetric/coercive M_AB.",
        ),
        (
            "HMX3687_2_kinetic_matrix",
            "second-order Helmholtz block",
            "-D_mu(G_AB D^mu .) + [D_mu(G_BA D^mu .)]^dagger",
            "G_AB=G_BA and D_mu preserves the internal pairing, up to declared gauge/projector terms",
            "R_H_G := antisym(G_AB) + D_mu G-compatibility defect",
            "ZERO_IF_SYMMETRIC_COMPATIBLE_KINETIC_PAIRING",
            "This is the exact mathematical condition under the 'motion field' language: the response medium must have a self-adjoint local stiffness.",
        ),
        (
            "HMX3687_3_connection_projector",
            "connection/readout Helmholtz block",
            "commutator terms from D_mu, P_loc and q-readout must be adjoint-symmetric or explicitly retained",
            "[D_mu,D_nu], delta_g P_loc and representative dependence are q-basic or canceled by constraints",
            "R_H_conn := connection/projector adjoint defect",
            "OPEN_LIVE_PROJECTOR_INPUT",
            "The clean action can absorb a connection only if the connection is part of the parent geometry, not a fitted readout.",
        ),
        (
            "HMX3687_4_metric_Helmholtz",
            "metric response integrability",
            "H_K^{mu nu|alpha beta}:=delta(sqrt(-g)K_hat^{mu nu})/delta g_alpha_beta - delta(sqrt(-g)K_hat^{alpha beta})/delta g_mu_nu",
            "H_K=0 up to fixed-reference boundary terms if K_hat=K_metric[Gamma_eff]",
            "R_H_K := live metric second-variation asymmetry",
            "CLOSED_FOR_ACTION_DEFINED_KMETRIC_NOT_FOR_LIVE_KHAT",
            "This separates the theorem branch from the old-symbol branch.",
        ),
        (
            "HMX3687_5_boundary",
            "boundary adjoint block",
            "integration-by-parts terms from D_mu, moving support, corners and reference subtraction must be fixed or no-flux",
            "delta B_GK is fixed-reference/exact and P_loc annihilates it",
            "R_H_boundary := boundary adjoint and flux residue",
            "OPEN_BOUNDARY_CONVENTION",
            "Bulk Helmholtz closure does not silence linked-surface mass/force leakage.",
        ),
        (
            "HMX3687_6_verdict",
            "Helmholtz status",
            "H_clean_bulk=0 under symmetric/coercive parent response data; H_live is not computable/proved from current K_hat symbols.",
            "adopt clean response branch and prove K_hat=K_metric, or carry H_live residual",
            "R_Helmholtz = R_H_live_symbol + R_H_conn + R_H_boundary",
            "BULK_THEOREM_PROGRESS_LIVE_CLAIM_BLOCKED",
            "3687 closes the formal bulk Helmholtz rung but does not close the live local-GR branch.",
        ),
    ]
    return [
        {
            **base(ts),
            "matrix_id": matrix_id,
            "block": block,
            "operator_or_test": operator_or_test,
            "zero_condition": zero_condition,
            "residual_if_failed": residual_if_failed,
            "status": status,
            "interpretation": interpretation,
            "claim_allowed": False,
            "score_ready": False,
        }
        for matrix_id, block, operator_or_test, zero_condition, residual_if_failed, status, interpretation in specs
    ]


def deltak_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DK3687_0_definition",
            "total Delta_K",
            "Delta_K^{mu nu} := K_hat_live^{mu nu} - K_metric^{mu nu}[Gamma_eff]",
            "K_metric^{mu nu}=G_AB D^mu Y^A D^nu Y^B + K_coeff^{mu nu}+K_projector^{mu nu}+K_boundary^{mu nu}+K_flux^{mu nu}",
            "Delta_K must vanish in the same convention used by T_GK=Gamma_eff g-K_metric",
            "DEFINITION_READY",
        ),
        (
            "DK3687_1_gradient_piece",
            "gradient/elastic piece",
            "Delta_K_grad := K_hat_grad - G_AB D^mu Y^A D^nu Y^B",
            "requires live K_hat tensor to expose a gradient/elastic anisotropic stress piece",
            "R_DeltaK_grad",
            "OPEN_COMPONENT_MATCH",
        ),
        (
            "DK3687_2_coefficient_response",
            "metric-dependent coefficients",
            "Delta_K_coeff := K_hat_coeff - K_coeff[delta_g G_AB, delta_g M_AB, delta_g D_mu]",
            "metric dependence of G_AB, M_AB and D_mu must be declared before variation",
            "R_DeltaK_coeff",
            "OPEN_COEFFICIENT_RESPONSE",
        ),
        (
            "DK3687_3_projector_readout",
            "projector/readout piece",
            "Delta_K_projector := K_hat_projector - K_projector[delta_g P_loc, delta_g q, delta_g Y]",
            "P_loc and q-readout must be parent-owned and commute with the fixed-point limit",
            "R_DeltaK_projector",
            "OPEN_PROJECTOR_OWNER",
        ),
        (
            "DK3687_4_boundary",
            "boundary/improvement piece",
            "Delta_K_boundary := K_hat_boundary - K_boundary[Theta_GK,B_GK,corners,reference]",
            "boundary class fixed; exact terms no-flux or annihilated by P_loc",
            "R_DeltaK_boundary",
            "OPEN_BOUNDARY_NO_FLUX",
        ),
        (
            "DK3687_5_flux",
            "physical EM/Poynting/wave flux piece",
            "Delta_K_flux := K_hat_flux - W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}",
            "flux stress must be explicit physical stress/current, not hidden q_loc closure",
            "R_DeltaK_flux",
            "SEPARATE_EM_BRANCH_NOT_LOCAL_ZERO_PROOF",
        ),
        (
            "DK3687_6_live_verdict",
            "live symbol match",
            "Delta_K=0 is not proved because current source files do not expose a complete live K_hat component decomposition under one convention.",
            "build a live Gamma/Khat symbol map or retain component residuals",
            "R_DeltaK = R_DeltaK_grad+R_DeltaK_coeff+R_DeltaK_projector+R_DeltaK_boundary+R_DeltaK_flux",
            "DELTAK_ZERO_NOT_CLAIMED_COMPONENT_VECTOR_STAGED",
        ),
    ]
    return [
        {
            **base(ts),
            "deltak_id": deltak_id,
            "component": component,
            "formula": formula,
            "required_match": required_match,
            "residual_if_failed": residual_if_failed,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for deltak_id, component, formula, required_match, residual_if_failed, status in specs
    ]


def live_match_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("LMA3687_0_clean_bulk", "bulk clean response action", "H_clean_bulk=0 under symmetric M/G and G-compatible D", "proved conditionally by the matrix rows", True, "not enough to claim live K_hat"),
        ("LMA3687_1_formal_Kmetric", "formal K_metric formula", "K_metric exists by varying the clean scalar density", "3627/2409/3686 agree this formal step is available", True, "compare to live K_hat"),
        ("LMA3687_2_live_Khat_identity", "live K_hat=K_metric", "source-backed identity under one sign/volume convention", "2807/3432/515/2409 say no live identity is present", False, "R_DeltaK"),
        ("LMA3687_3_live_Helmholtz", "live K_hat Helmholtz test", "second metric variations of live K_hat commute up to fixed boundary terms", "3419 says old/live symbols are not evaluable with current components", False, "R_H_live_symbol"),
        ("LMA3687_4_boundary_projector", "boundary/projector compatibility", "boundary and P_loc terms are parent-owned and no-flux", "open in 3419/3686", False, "R_H_conn+R_H_boundary+R_DeltaK_projector"),
        ("LMA3687_5_source_coupling", "J_A local source silence", "J_A=0 or source-backed finite bound", "3629 gives the law but not the zero or coefficient", False, "R_linear_source"),
        ("LMA3687_6_verdict", "live local-GR branch", "clean bulk theorem plus live Khat identity plus no source/boundary/projector leak", "only the clean bulk/formal response part passes", False, "local-GR/Newton claim remains blocked"),
    ]
    return [
        {
            **base(ts),
            "match_id": match_id,
            "target": target,
            "requirement": requirement,
            "current_evidence": current_evidence,
            "pass_now": pass_now,
            "residual_if_failed": residual_if_failed,
            "claim_allowed": False,
            "score_ready": False,
        }
        for match_id, target, requirement, current_evidence, pass_now, residual_if_failed in specs
    ]


def residual_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RHB3687_0_Helmholtz_reduced",
            "abs(R_Helmholtz)/N_H",
            "(|R_H_live_symbol|+|R_H_conn|+|R_H_boundary|)/N_H",
            "dimensionless no-cancellation envelope",
            "BULK_HELMHOLTZ_ZERO_CLEAN_BRANCH_LIVE_INPUTS_MISSING",
            "clean bulk Helmholtz is no longer the gap; live symbol, connection/projector and boundary pieces remain",
            "HMX3687_6_verdict",
        ),
        (
            "RHB3687_1_DeltaK_total",
            "abs(R_DeltaK)/N_H",
            "(|R_DeltaK_grad|+|R_DeltaK_coeff|+|R_DeltaK_projector|+|R_DeltaK_boundary|+|R_DeltaK_flux|)/N_H",
            "dimensionless no-cancellation envelope",
            "FORMULA_READY_COMPONENT_INPUTS_MISSING",
            "explicit tensor mismatch vector replacing the vague Khat-match blocker",
            "DK3687_6_live_verdict",
        ),
        (
            "RHB3687_2_q_loc_profile",
            "q_loc^nu",
            "q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})",
            "local force/profile units after source normalization",
            "WARD_PROFILE_READY_NUMERIC_INPUTS_MISSING",
            "testing can proceed once E_A/J_A, B_GK, Delta_K and P_loc coefficients are sourced",
            "RAC3686_3_q_loc_Ward",
        ),
        (
            "RHB3687_3_live_tensor_input",
            "K_hat_live component table",
            "MISSING_KHAT_LIVE_COMPONENT_ROWS",
            "tensor components under one convention",
            "MISSING_SOURCE_INPUT",
            "the next work must build a component map, not another free-form prose audit",
            "LMA3687_2_live_Khat_identity",
        ),
        (
            "RHB3687_4_coupling_input",
            "J_A source coupling coefficient",
            "MISSING_J_A_ZERO_THEOREM_OR_BOUND",
            "source coupling/vector units",
            "MISSING_COUPLING_INPUT",
            "the coupling suspicion is now a concrete Euler-source row",
            "LMA3687_5_source_coupling",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": status,
            "interpretation": interpretation,
            "source_anchor": source_anchor,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, status, interpretation, source_anchor in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3687_0_result", "BULK_HELMHOLTZ_CLOSED_CONDITIONALLY", "the clean response action passes the bulk Helmholtz test under explicit symmetry/self-adjointness clauses", "stop treating Helmholtz as mystical; the live problem is Khat matching and source/boundary leakage"),
        ("DEC3687_1_DeltaK", "DELTAK_VECTOR_STAGED", "Khat mismatch is decomposed into gradient, coefficient, projector, boundary and flux components", "next build the live component map and try to collapse pieces"),
        ("DEC3687_2_coupling", "COUPLING_REMAINS_CORE", "J_A enters q_loc through the derived Euler source law", "later target J_A=0 theorem or finite source-backed coefficient"),
        ("DEC3687_3_EM", "POYNTING_VECTOR_ALLOWED_AS_PHYSICAL_STRESS", "flux can live in K_flux only as explicit EM/wave stress", "do not use Poynting stress as hidden local-GR closure"),
        ("DEC3687_4_next", "NEXT_BEST_TARGET", "live Gamma/Khat component map is now the route with least ambiguity", "run 3688 Khat component map to clean response or Delta_K component bound"),
        ("DEC3687_5_private", "PRIVATE_NONCLAIM", "no local-GR/Newton/public claim follows yet", "continue derivation privately"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "status": status,
            "decision": decision,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, status, decision, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3687_0_Helmholtz_live", "claim live Gamma/Khat variational integrability", "BLOCKED_LIVE_COMPONENTS", "bulk clean branch passes, but live Khat components are not source-matched"),
        ("CG3687_1_DeltaK_zero", "claim Delta_K=0", "BLOCKED_COMPONENT_MATCH", "gradient/coefficient/projector/boundary/flux pieces are not matched under one convention"),
        ("CG3687_2_q_loc_zero", "claim local q_loc^nu=0", "BLOCKED_DELTAK_JA_BOUNDARY_PLOC", "Ward profile still contains E_A/J_A, boundary and Delta_K terms"),
        ("CG3687_3_Newton_GR", "claim derived Newton/local-GR limit", "BLOCKED_LOCAL_BRANCH", "Khat match and source coupling are not closed"),
        ("CG3687_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3687_0",
            "status": "CLEAN_BULK_HELMHOLTZ_DERIVED_LIVE_KHAT_MATCH_NOT_CLAIMED_DELTAK_COMPONENT_VECTOR_STAGED",
            "summary": "3687 proves the clean bulk response action has Helmholtz symmetry under explicit symmetric/coercive/self-adjoint parent data, then decomposes the live Khat mismatch into Delta_K components. The live local-GR/Newton claim remains blocked by missing Khat component matching, source coupling, boundary and projector ownership.",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3687_0",
            "target_doc": "3688-Y5-R2FR-live-Gamma-Khat-component-map-to-clean-response-or-DeltaK-component-bound.md",
            "target_script": "scripts/Y5_R2FR_3688_live_Gamma_Khat_component_map_to_clean_response_or_DeltaK_component_bound.py",
            "objective": "build a live Gamma_eff/K_hat component map under one convention and try to match each piece to clean response terms K_grad, K_coeff, K_projector, K_boundary and K_flux; if unmatched, keep explicit Delta_K component bounds",
            "success_gate": "at least one live K_hat component is matched to K_metric or every unmatched component is carried as a named nonclaim Delta_K residual with source path and next coefficient need",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    matrix: list[dict[str, object]],
    deltak: list[dict[str, object]],
    live: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3687 - Clean response action Helmholtz matrix or DeltaK bound row",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint does the promised Helmholtz/`Delta_K` test. It closes the formal bulk Helmholtz problem for the clean response action under explicit symmetry/self-adjointness clauses, then separates that theorem from the still-unmatched live `K_hat` symbols.",
        "",
        "## Main result",
        "",
        "Clean bulk Euler operator:",
        "",
        "`E_A = -D_mu(G_AB D^mu Y^B) + M_AB Y^B + O(Y^3) - J_A - B_A`.",
        "",
        "Helmholtz matrix:",
        "",
        "`H_AB := delta E_A/delta Y^B - (delta E_B/delta Y^A)^dagger`.",
        "",
        "Bulk theorem:",
        "",
        "`H_AB^clean_bulk=0` if `G_AB=G_BA`, `M_AB=M_BA`, `D_mu` is compatible with the internal pairing, constraints/gauge modes are removed, and boundary adjoint terms vanish.",
        "",
        "Metric response obstruction:",
        "",
        "`H_K^{mu nu|alpha beta}:=delta(sqrt(-g)K_hat^{mu nu})/delta g_alpha_beta - delta(sqrt(-g)K_hat^{alpha beta})/delta g_mu_nu` is zero automatically only for an action-defined `K_metric`, not for the old/live `K_hat` symbols unless they are matched.",
        "",
        "DeltaK split:",
        "",
        "`Delta_K^{mu nu} := K_hat_live^{mu nu} - K_metric^{mu nu}[Gamma_eff]`.",
        "",
        "`R_DeltaK = R_DeltaK_grad+R_DeltaK_coeff+R_DeltaK_projector+R_DeltaK_boundary+R_DeltaK_flux`.",
        "",
        "Reduced residual:",
        "",
        "`abs(R_Helmholtz)/N_H <= (|R_H_live_symbol|+|R_H_conn|+|R_H_boundary|)/N_H`.",
        "",
        "## Helmholtz matrix rows",
    ]
    for row in matrix:
        lines.append(f"- `{row['matrix_id']}`: {row['status']} - {row['block']} -> {row['interpretation']}")
    lines.extend(["", "## DeltaK decomposition"])
    for row in deltak:
        lines.append(f"- `{row['deltak_id']}`: {row['status']} - {row['component']} -> `{row['residual_if_failed']}`")
    lines.extend(["", "## Live symbol match audit"])
    for row in live:
        lines.append(f"- `{row['match_id']}`: pass_now={row['pass_now']} - {row['target']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Residual bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    matrix: list[dict[str, object]],
    deltak: list[dict[str, object]],
    live: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + matrix + deltak + live + bounds + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3687*", "3687-Y5-R2FR-*", "P8_Y5*3687*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    matrix_by_id = {str(row["matrix_id"]): row for row in matrix}
    deltak_by_id = {str(row["deltak_id"]): row for row in deltak}
    live_by_id = {str(row["match_id"]): row for row in live}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}
    delta_components = ["R_DeltaK_grad", "R_DeltaK_coeff", "R_DeltaK_projector", "R_DeltaK_boundary", "R_DeltaK_flux"]
    delta_formula = str(bound_by_id["RHB3687_1_DeltaK_total"]["bound_or_formula"])

    add("VAL3687_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3687_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3687_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3687 outputs written")
    add("VAL3687_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3687_4_bulk_Helmholtz", matrix_by_id["HMX3687_0_clean_bulk_operator"]["status"] == "BULK_HELMHOLTZ_DERIVED_CONDITIONALLY" and "H_AB^clean_bulk=0" in matrix_by_id["HMX3687_0_clean_bulk_operator"]["zero_condition"], "clean bulk Helmholtz theorem recorded")
    add("VAL3687_5_metric_obstruction", matrix_by_id["HMX3687_4_metric_Helmholtz"]["status"] == "CLOSED_FOR_ACTION_DEFINED_KMETRIC_NOT_FOR_LIVE_KHAT", "metric Helmholtz separates action-defined Kmetric from live Khat")
    add("VAL3687_6_DeltaK_definition", "Delta_K" in deltak_by_id["DK3687_0_definition"]["formula"] and "K_hat_live" in deltak_by_id["DK3687_0_definition"]["formula"], "Delta_K definition written")
    add("VAL3687_7_DeltaK_components", all(component in delta_formula for component in delta_components), "Delta_K residual contains every component")
    add("VAL3687_8_live_match_blocked", live_by_id["LMA3687_2_live_Khat_identity"]["pass_now"] is False and live_by_id["LMA3687_3_live_Helmholtz"]["pass_now"] is False, "live Khat identity/Helmholtz are not claimed")
    add("VAL3687_9_q_loc_profile", "q_loc^nu" in bound_by_id["RHB3687_2_q_loc_profile"]["bound_or_formula"] and "Delta_K" in bound_by_id["RHB3687_2_q_loc_profile"]["bound_or_formula"], "q_loc profile keeps Delta_K term")
    add("VAL3687_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3687_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3687_12_doc_written", "H_AB^clean_bulk=0" in doc_text and "Delta_K" in doc_text and "R_DeltaK" in doc_text, "doc records Helmholtz theorem and DeltaK split")
    add("VAL3687_13_next_target", next_target[0]["target_doc"].startswith("3688-") and "component map" in next_target[0]["objective"], "3688 targets live component mapping")
    add("VAL3687_14_no_formalization_leak", not leaks, "no 3687 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    matrix = helmholtz_matrix_rows(ts)
    deltak = deltak_rows(ts)
    live = live_match_rows(ts)
    bounds = residual_bound_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3687_SOURCE_REGISTER.csv",
        "matrix": RESIDUALS / "P8_Y5_R2FR_3687_HELMHOLTZ_MATRIX_ROWS.csv",
        "deltak": RESIDUALS / "P8_Y5_R2FR_3687_DELTAK_DECOMPOSITION_ROWS.csv",
        "live": RESIDUALS / "P8_Y5_R2FR_3687_LIVE_SYMBOL_MATCH_AUDIT.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3687_REDUCED_RESIDUAL_BOUND_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3687_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3687_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3687_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3687_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3687_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["matrix"], matrix)
    write_csv(outputs["deltak"], deltak)
    write_csv(outputs["live"], live)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, matrix, deltak, live, bounds, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, matrix, deltak, live, bounds, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3687 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3687 checkpoint: clean bulk Helmholtz closed conditionally; live Khat match blocked; DeltaK component vector staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
