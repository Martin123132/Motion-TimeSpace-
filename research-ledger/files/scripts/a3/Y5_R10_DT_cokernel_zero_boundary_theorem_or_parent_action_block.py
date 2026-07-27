from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md"
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
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1196_0_1195_next",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "NEXT1195_0_1196",
            "role": "direct 1196 handoff.",
        },
        {
            "source_id": "SRC1196_1_1195_adjoint",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_1_formal_adjoint",
            "role": "formal D_T adjoint used by the cokernel gate.",
        },
        {
            "source_id": "SRC1196_2_1195_cokernel",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_2_cokernel_characterization",
            "role": "projected conformal-Killing cokernel characterization.",
        },
        {
            "source_id": "SRC1196_3_1195_range",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_3_exact_range_condition",
            "role": "orthogonality/range condition for exact D_T compensation.",
        },
        {
            "source_id": "SRC1196_4_1195_bound",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_5_bound_if_cokernel_survives",
            "role": "fallback residual bound if cokernel survives.",
        },
        {
            "source_id": "SRC1196_5_1195_response",
            "relative_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "FRS1195_0_PPN_gamma_beta_source_row",
            "role": "first response-source row carried into 1196.",
        },
        {
            "source_id": "SRC1196_6_831_variation",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "OC831_2_first_variation",
            "role": "earlier Khat/D_T first-variation route.",
        },
        {
            "source_id": "SRC1196_7_831_projection",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_1_projection_law",
            "role": "residual as projection onto surviving obstruction.",
        },
        {
            "source_id": "SRC1196_8_831_bound",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "cokernel/boundary/regularizer residual bound precedent.",
        },
        {
            "source_id": "SRC1196_9_832_boundary",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "CB832_3_boundary_residual",
            "role": "boundary residual remains a live obstruction.",
        },
        {
            "source_id": "SRC1196_10_1019_domain",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "BE1019_0_domain",
            "role": "domain/boundary exactness certificate requirements.",
        },
        {
            "source_id": "SRC1196_11_1019_verdict",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "BE1019_6_verdict",
            "role": "boundary exactness does not currently close.",
        },
        {
            "source_id": "SRC1196_12_1019_projector",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_6_projector_zero_or_bound",
            "role": "projector zero-or-bound source-pack fallback.",
        },
        {
            "source_id": "SRC1196_13_1170_no_flux",
            "relative_path": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "needle": "PBC1170_1_no_flux_condition",
            "role": "sufficient no-flux condition precedent for boundary silence.",
        },
        {
            "source_id": "SRC1196_14_1171_natural_bc",
            "relative_path": "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md",
            "needle": "NBC1171_5_verdict",
            "role": "generic natural boundary condition rejected as too weak.",
        },
        {
            "source_id": "SRC1196_15_513_parent_action",
            "relative_path": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
            "needle": "GK513_0_action_existence",
            "role": "parent action existence gate.",
        },
        {
            "source_id": "SRC1196_16_517_boundary_terms",
            "relative_path": "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
            "needle": "MR517_3_boundary_terms",
            "role": "metric-response boundary terms precedent.",
        },
        {
            "source_id": "SRC1196_17_756_no_fake_guard",
            "relative_path": "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            "needle": "QCB756_5_no_fake_data_guard",
            "role": "no fake data / no fake response guard.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def cokernel_zero_boundary_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CKZ1196_0_adjoint_kernel_restated",
            "clause": "D_T cokernel",
            "statement": "The obstruction to solving D_T K_T = G_res is Ker(D_T^dagger).",
            "mathematical_form": "D_T^dagger V = -Pi_TF[nabla_(mu)(P_loc V)_(nu)] + A_P[V] plus boundary pairing.",
            "derivation_or_bound": "This restates the 1195 integration-by-parts result with projector-derivative terms collected into A_P.",
            "status": "FORMAL_ADJOINT_RESTATED",
            "missing_for_claim": "fixed parent P_loc; exact domain; boundary condition; source norm",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_1_dirichlet_anchor_kills_kernel",
            "clause": "conditional no-cokernel theorem",
            "statement": "If the local domain anchors the projected conformal-Killing modes and a conformal-Killing/Korn inequality holds, then Ker(D_T^dagger)=0.",
            "mathematical_form": "V|partialD=0 or equivalent residual-sector anchor, ||V||_H1 <= C_CK ||Pi_TF sym nabla(P_loc V)+A_P[V]||_L2, and D_T^dagger V=0 imply V=0.",
            "derivation_or_bound": "Insert D_T^dagger V=0 into the inequality; the right-hand side vanishes, so the anchored H1 norm of V vanishes.",
            "status": "CONDITIONAL_MATH_THEOREM_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent-owned anchor/no-zero-mode certificate; same P_loc, measure, coframe, and boundary class as local tests",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_2_no_anchor_no_generic_zero",
            "clause": "cheap zero rejection",
            "statement": "Without a boundary anchor or quotient rule, the flat/frozen limit admits conformal-Killing-like modes, so zero cokernel is false as a generic theorem.",
            "mathematical_form": "Pi_TF sym nabla V = 0 has rigid conformal solutions unless boundary/domain/readout removes them.",
            "derivation_or_bound": "The same condition that identifies the cokernel also displays the possible zero modes; ignoring them would smuggle in the plateau axiom.",
            "status": "GENERAL_ZERO_REJECTED",
            "missing_for_claim": "explicit quotient removal or boundary anchoring of translations, rotations, boosts/dilations, and local gauge representatives",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_3_projector_perturbation_bound",
            "clause": "P_loc derivative leakage",
            "statement": "If P_loc is not frozen, derivative/projector leakage must either be inside the zero theorem or bounded as a residual.",
            "mathematical_form": "baseline ||V||_H1 <= C0||Pi_TF sym nabla V|| and ||Delta_P[V]|| <= eps_P||V||_H1 give zero only if C0 eps_P < 1.",
            "derivation_or_bound": "Move the projector-leakage term to the right-hand side; the smallness condition absorbs it into the left-hand norm.",
            "status": "PERTURBATIVE_ZERO_CONDITION_STAGED",
            "missing_for_claim": "numeric/source-backed eps_P or exact parent proof that nabla P_loc terms vanish",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_4_boundary_pairing_condition",
            "clause": "range condition with boundary",
            "statement": "Exact compensation also requires the boundary pairing to vanish or be carried as B_T.",
            "mathematical_form": "forall V in Ker(D_T^dagger): int_D V_nu G_res^nu dV + int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS = 0.",
            "derivation_or_bound": "The boundary term is the integration-by-parts remainder in the D_T adjoint identity.",
            "status": "BOUNDARY_ORTHOGONALITY_REQUIRED",
            "missing_for_claim": "boundary source path; no-flux/Dirichlet theorem; sign convention; tracefree boundary stress readout",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_5_bound_if_kernel_survives",
            "clause": "nonclaim fallback",
            "statement": "If any cokernel/boundary mode survives, the local branch becomes a scored residual bound, not a local-GR proof.",
            "mathematical_form": "||q_DT|| <= ||P_coker G_res|| + ||B_T|| + kappa_T C_T ||E_reg|| + ||Delta_P||.",
            "derivation_or_bound": "Carries forward the 831/1195 projection law and adds explicit projector leakage.",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "missing_for_claim": "P_coker fraction; boundary norm; regularizer norm; P_loc leakage; arena response operator",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CKZ1196_6_verdict",
            "clause": "1196 theorem verdict",
            "statement": "The no-cokernel theorem is real but conditional; it is not yet a parent-signed local-vacuum theorem.",
            "mathematical_form": "Ker(D_T^dagger)=0 follows from anchored CK/Korn inequality, not from MTS dynamics alone as currently sourced.",
            "derivation_or_bound": "This is progress because it states the exact mathematical contract the parent action must satisfy.",
            "status": "DERIVATION_CONTRACT_WRITTEN_NO_LOCAL_GR_CLAIM",
            "missing_for_claim": "parent action ownership of anchors, boundary class, and P_loc leakage",
            "valid_for_claim": False,
        },
    ]


def parent_action_block_rows() -> list[dict[str, object]]:
    return [
        {
            "block_id": "PAB1196_0_candidate_action",
            "component": "effective D_T balance block",
            "statement": "A possible parent block would make K_T an owned tracefree tensor response, not an added closure variable.",
            "mathematical_form": "S_T = (2 kappa_T)^-1 ||D_T K_T - G_res||^2 + (mu_T^2/2)||K_T||^2 + S_boundary + S_Ward.",
            "closure_status": "CANDIDATE_BLOCK_ONLY",
            "missing_for_claim": "derive this block from S_MTS or locate it in the corpus; define K_T, G_res, kappa_T, mu_T, P_loc, measure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "PAB1196_1_variation_equation",
            "component": "Euler equation",
            "statement": "The candidate action yields a tracefree tensor equation that can drive D_TK_T toward G_res.",
            "mathematical_form": "D_T^dagger(D_T K_T - G_res) + kappa_T mu_T^2 K_T + boundary_variation + Ward_terms = 0.",
            "closure_status": "FORMAL_VARIATION_DERIVED_FOR_CANDIDATE",
            "missing_for_claim": "parent variation; boundary term cancellation; stress tensor/Ward ledger",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "PAB1196_2_tracefree_projection",
            "component": "tracefree ownership",
            "statement": "The tracefree projection must be built into the parent configuration space or enforced by a multiplier.",
            "mathematical_form": "K_T in Gamma(S^2_0 T*D) or S_T includes int lambda_T g_mn K_T^mn.",
            "closure_status": "STRUCTURE_NEEDED",
            "missing_for_claim": "parent field definition; no double counting with metric stress; units of lambda_T",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "PAB1196_3_natural_boundary_warning",
            "component": "boundary variation",
            "statement": "A generic natural boundary condition controls the conjugate boundary momentum, not automatically the cokernel pairing.",
            "mathematical_form": "delta S_T boundary = int_partialD delta K_T^(mu nu) Pi_T_mu nu, while range pairing needs int_partialD n_mu K_T^(mu nu)(P_loc V)_nu.",
            "closure_status": "NATURAL_BC_TOO_WEAK_BY_DEFAULT",
            "missing_for_claim": "specific parent boundary action proving the needed pairing is zero or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "PAB1196_4_parent_ownership_clauses",
            "component": "promotion gate",
            "statement": "Promotion requires the same parent action to own the operator, sources, response readout, and conservation ledger.",
            "mathematical_form": "S_MTS -> {D_T, K_T, G_res, P_loc, dV, boundary class, delta_g S_T, nabla_mu T_T^mu nu}.",
            "closure_status": "PROMOTION_GATE_EXPLICIT",
            "missing_for_claim": "all entries real source paths with no MISSING_* markers",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "PAB1196_5_verdict",
            "component": "parent action verdict",
            "statement": "1196 does not find a parent-owned D_T action; it only writes the exact block such an action must contain.",
            "mathematical_form": "candidate S_T is a contract for future derivation, not an adopted MTS term.",
            "closure_status": "CANDIDATE_EFFECTIVE_NOT_PARENT_SOURCED",
            "missing_for_claim": "parent source or explicit demotion to closure-only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def boundary_pairing_rows() -> list[dict[str, object]]:
    return [
        {
            "boundary_id": "BP1196_0_tracefree_adjoint_boundary",
            "boundary_object": "D_T integration-by-parts boundary",
            "formula": "B_T[V,K_T] = int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS.",
            "zero_route": "V|partialD=0, or n_mu K_T^(mu nu)=0 on the residual boundary, or parent boundary action cancels the pairing.",
            "bound_route": "|B_T| <= ||n.K_T||_H-1/2(partialD) ||P_loc V||_H1/2(partialD).",
            "status": "BOUNDARY_PAIRING_EXPLICIT",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BP1196_1_no_flux_anchor",
            "boundary_object": "residual-sector no-flux/Dirichlet anchor",
            "formula": "pullback(P_loc V)=0 or n_mu K_T^(mu nu)=0 on partialD.",
            "zero_route": "sufficient to kill the adjoint boundary term and remove anchored conformal-Killing zero modes.",
            "bound_route": "if not zero, source the trace norm and include it in B_T.",
            "status": "SUFFICIENT_NOT_DERIVED_FROM_PARENT",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BP1196_2_projector_boundary_leakage",
            "boundary_object": "projector/coframe leakage",
            "formula": "Delta_P = terms from nabla P_loc, boundary pullback(P_loc), and domain-motion/coframe variation.",
            "zero_route": "parent proves P_loc is frozen/tangent/silent on the selected local boundary.",
            "bound_route": "||Delta_P|| <= eps_P ||V||_H1 or as an arena-specific boundary source row.",
            "status": "PROJECTOR_LEAKAGE_LIVE",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BP1196_3_boundary_exactness_precedent",
            "boundary_object": "1019/1170/1171 boundary lesson",
            "formula": "exact boundary/topological arguments do not erase local boundary primitives unless the same boundary class is certified.",
            "zero_route": "corner-free, harmonic-free, parent-signed exactness plus closed/controlled kernel.",
            "bound_route": "source-pack finite boundary row with surface norm, kernel derivative, harmonic, residual, and corner terms.",
            "status": "NO_CHEAP_BOUNDARY_SHORTCUT",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BP1196_4_first_source_columns",
            "boundary_object": "future coker/boundary runner row",
            "formula": "q_DT_bound = coker_fraction*||G_res|| + boundary_norm + kappa_T*C_T*regularizer_norm + projector_leakage_norm.",
            "zero_route": "all zero certificates source-backed in the same gauge/domain.",
            "bound_route": "columns: domain_id;arena;P_coker_basis_path;coker_fraction;G_res_profile_path;boundary_norm_path;eps_P_path;response_operator_path;bound_source_path.",
            "status": "SOURCE_COLUMNS_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BP1196_5_verdict",
            "boundary_object": "boundary verdict",
            "formula": "boundary silence is now a precise theorem target, not an assumption.",
            "zero_route": "derive parent-owned local anchor/no-flux condition.",
            "bound_route": "implement nonclaim finite-bound runner if zero proof cannot be sourced.",
            "status": "BOUNDARY_GATE_OPEN",
            "valid_for_claim": False,
        },
    ]


def response_source_continuity_rows() -> list[dict[str, object]]:
    return [
        {
            "response_id": "RSC1196_0_PPN_gamma_beta_DT",
            "arena": "PPN gamma/beta",
            "observable": "Delta_PPN_DT",
            "formula": "||Delta_PPN_DT|| <= ||W_PPN|| (||P_coker G_res|| + ||B_T|| + kappa_T C_T||E_reg|| + ||Delta_P||).",
            "required_sources": "W_PPN_source_path;P_coker_basis_path;G_res_profile_path;boundary_norm_path;regularizer_source_path;projector_leakage_path;gamma_beta_bound_source_path",
            "missing": "MISSING_W_PPN;MISSING_P_COKER;MISSING_G_RES;MISSING_BOUNDARY;MISSING_REGULARIZER;MISSING_PROJECTOR_LEAKAGE;MISSING_BOUNDS",
            "status": "blocked_missing_inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "response_id": "RSC1196_1_R10_alpha_lambda_DT",
            "arena": "R10",
            "observable": "alpha_DT(lambda)",
            "formula": "alpha_DT(lambda)=W_R10(lambda)[P_coker G_res, B_T, E_reg, Delta_P].",
            "required_sources": "W_R10_lambda_source_path;alpha_bound_curve_path;range_profile_path;boundary_profile_path;source_normalization_path;projector_leakage_path",
            "missing": "MISSING_W_R10;MISSING_ALPHA_BOUND_CURVE;MISSING_RANGE_PROFILE;MISSING_BOUNDARY_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_PROJECTOR_LEAKAGE",
            "status": "blocked_missing_inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "response_id": "RSC1196_2_clock_orbital",
            "arena": "clock_orbital",
            "observable": "Delta_clock_DT; Delta_orbital_DT",
            "formula": "Delta_arena <= ||W_arena|| q_DT_bound with q_DT_bound carrying coker, boundary, regularizer, and projector leakage terms.",
            "required_sources": "W_clock_path;W_orbital_path;clock_bound_path;orbital_bound_path;domain_geometry_path;source_profile_path",
            "missing": "MISSING_CLOCK_RESPONSE;MISSING_ORBITAL_RESPONSE;MISSING_DOMAIN_GEOMETRY;MISSING_BOUNDS",
            "status": "blocked_missing_inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "response_id": "RSC1196_3_no_fake_response_guard",
            "arena": "all_local",
            "observable": "claim_guard",
            "formula": "valid_for_claim can be true only if parent D_T, no-cokernel/boundary certificate, response operator, source profile, and external bound are real.",
            "required_sources": "all source paths exist; units declared; same frame/gauge/domain; no MISSING_* markers",
            "missing": "GUARD_ACTIVE",
            "status": "nonclaim_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1196_0_no_cokernel_zero",
            "claim": "Ker(D_T^dagger)=0 in local matter domains",
            "status": "BLOCKED_PARENT_BOUNDARY_ANCHOR_MISSING",
            "why": "the theorem is conditional on anchored conformal-Killing/Korn inequality and parent-owned boundary/readout",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1196_1_boundary_zero",
            "claim": "D_T boundary pairing vanishes",
            "status": "BLOCKED_BOUNDARY_PAIRING_NOT_SOURCED",
            "why": "B_T is explicit but no parent no-flux/Dirichlet/cancellation theorem is sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1196_2_parent_action_block",
            "claim": "candidate S_T is an MTS parent action sector",
            "status": "BLOCKED_CANDIDATE_ONLY",
            "why": "1196 writes the required block but does not locate or derive it from S_MTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1196_3_response_score",
            "claim": "PPN/R10/clock/orbital residuals pass",
            "status": "BLOCKED_RESPONSE_INPUTS_MISSING",
            "why": "W_arena, P_coker, G_res, B_T, Delta_P, regularizer, and bound rows are not sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1196_4_local_GR",
            "claim": "MTS reduces to GR/Newton locally through D_T",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "no-cokernel, boundary, parent action, and response gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1196_0_theorem_contract",
            "decision": "conditional_no_cokernel_theorem_written",
            "reason": "anchored conformal-Killing/Korn inequality would kill the D_T cokernel exactly",
            "next_action": "source the parent boundary/domain anchor or demote to finite coker bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1196_1_general_zero_rejected",
            "decision": "no_unanchored_zero_claim",
            "reason": "conformal-Killing-like modes survive without a boundary/readout quotient",
            "next_action": "do not claim local vacuum plateau from D_T without the parent anchor",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1196_2_parent_block_status",
            "decision": "candidate_action_block_staged_not_adopted",
            "reason": "S_T gives the right Euler structure but is not sourced as a parent MTS sector",
            "next_action": "hunt for parent action ownership or explicitly label closure-only",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1196_3_best_next_route",
            "decision": "source_boundary_condition_or_build_cokernel_bound_runner",
            "reason": "the project now needs either a signed boundary/no-zero-mode theorem or a nonclaim numeric residual envelope",
            "next_action": "1197 should attempt parent boundary source first, then implement P_coker/B_T bound rows if it fails",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1196_0_1197",
            "next_target": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "objective": "source a parent-owned D_T boundary/no-cokernel certificate, or build the first nonclaim P_coker/B_T residual-bound runner for PPN/R10/clocks/orbits",
            "include": "boundary condition source hunt; CK/Korn anchor contract; P_coker source columns; B_T finite-bound schema; projector leakage eps_P; response rows; no-claim validation",
            "exclude": "local-GR pass; unanchored zero claim; parentless S_T adoption; scalar branch overuse; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    theorem_ids = {row["theorem_id"] for row in theorem_rows}
    parent_statuses = {row["closure_status"] for row in parent_rows}
    boundary_ids = {row["boundary_id"] for row in boundary_rows}
    response_ids = {row["response_id"] for row in response_rows}
    all_science_rows = theorem_rows + parent_rows + boundary_rows + response_rows + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in all_science_rows)
    all_blocked = all(row.get("claim_allowed") is False for row in parent_rows + response_rows + gates + nexts)
    return [
        {
            "check_id": "V1196_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_1_cokernel_zero_theorem_contract",
            "result": "pass" if {"CKZ1196_1_dirichlet_anchor_kills_kernel", "CKZ1196_2_no_anchor_no_generic_zero", "CKZ1196_3_projector_perturbation_bound"} <= theorem_ids else "fail",
            "detail": "conditional zero theorem, generic-zero rejection, and projector leakage bound are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_2_boundary_pairing_explicit",
            "result": "pass" if {"BP1196_0_tracefree_adjoint_boundary", "BP1196_4_first_source_columns"} <= boundary_ids else "fail",
            "detail": "D_T boundary pairing and first source columns are explicit",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_3_parent_action_not_promoted",
            "result": "pass" if "CANDIDATE_EFFECTIVE_NOT_PARENT_SOURCED" in parent_statuses else "fail",
            "detail": "candidate S_T block is not adopted as parent action",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_4_response_rows_blocked",
            "result": "pass" if {"RSC1196_0_PPN_gamma_beta_DT", "RSC1196_1_R10_alpha_lambda_DT", "RSC1196_3_no_fake_response_guard"} <= response_ids and all(row["claim_allowed"] is False for row in response_rows) else "fail",
            "detail": "PPN/R10 response continuity rows remain blocked and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_5_claim_gates_blocked",
            "result": "pass" if all_blocked and all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all 1196 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_6_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1196_0_1197" else "fail",
            "detail": "1197 handoff targets boundary source or finite cokernel-bound runner",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1196_SUMMARY",
            "result": "pass",
            "detail": "1196 writes the exact conditional no-cokernel/boundary contract for D_T, rejects the unanchored zero shortcut, stages a candidate S_T block without promotion, and hands off to boundary-source or finite-bound runner work",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1196 - Y5/R10 D_T cokernel zero-boundary theorem or parent action block",
            "**Current verdict:** 1196 gets the D_T route into its cleanest honest form: the cokernel can be killed by a parent-owned boundary/no-zero-mode theorem, but that theorem is not yet sourced. No local-GR claim follows.",
            "**Main progress:** the exact contract is now explicit: anchored conformal-Killing/Korn inequality, projector-leakage control, and boundary pairing silence. If any clause fails, D_T must become a finite residual-bound runner.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## D_T cokernel zero-boundary theorem\n\n" + table(theorem_rows),
            "## Parent action block attempt\n\n" + table(parent_rows),
            "## Boundary pairing rows\n\n" + table(boundary_rows),
            "## Response source continuity\n\n" + table(response_rows),
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
    theorem_rows = cokernel_zero_boundary_rows()
    parent_rows = parent_action_block_rows()
    boundary_rows = boundary_pairing_rows()
    response_rows = response_source_continuity_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(
        sources,
        theorem_rows,
        parent_rows,
        boundary_rows,
        response_rows,
        gates,
        decisions,
        nexts,
    )

    outputs = {
        "P8_Y5_R10_1196_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1196_COKERNEL_ZERO_BOUNDARY_THEOREM.csv": theorem_rows,
        "P8_Y5_R10_1196_PARENT_ACTION_BLOCK_ATTEMPT.csv": parent_rows,
        "P8_Y5_R10_1196_BOUNDARY_PAIRING_ROWS.csv": boundary_rows,
        "P8_Y5_R10_1196_RESPONSE_SOURCE_CONTINUITY.csv": response_rows,
        "P8_Y5_R10_1196_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1196_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1196_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1196_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, theorem_rows, parent_rows, boundary_rows, response_rows, gates, decisions, validations, nexts)

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
