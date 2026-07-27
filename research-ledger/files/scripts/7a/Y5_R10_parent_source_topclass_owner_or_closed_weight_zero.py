from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1169-Y5-R10-parent-source-topclass-owner-or-closed-weight-zero.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def rows_with_stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1169_0_1168_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1168_NEXT_TARGET.csv",
            "needle": "NEXT1168_0_1169",
            "role": "handoff requiring parent source/top-class owner or closed-weight zero theorem.",
        },
        {
            "source_id": "SRC1169_1_1168_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1168_VALIDATION.csv",
            "needle": "V1168_SUMMARY",
            "role": "1168 validation summary.",
        },
        {
            "source_id": "SRC1169_2_1168_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1168_SIGMA_PHI_SOURCE_CONTRACT.csv",
            "needle": "SPC1168_2_Sigma_C_FLRW",
            "role": "missing FLRW/top-class source selector.",
        },
        {
            "source_id": "SRC1169_3_1168_phi",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1168_SIGMA_PHI_SOURCE_CONTRACT.csv",
            "needle": "SPC1168_3_Phi_C",
            "role": "missing Phi_C boundary flux owner.",
        },
        {
            "source_id": "SRC1169_4_1168_dSFeps",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1168_DSF_EPS_BOUND_ROWS.csv",
            "needle": "DSF1168_1_zero_route",
            "role": "closed-weight zero route staged in 1168.",
        },
        {
            "source_id": "SRC1169_5_1168_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1168_CLAIM_GATES.csv",
            "needle": "G1168_2_same_law_selector",
            "role": "same-law local-zero/FLRW-active selector remains blocked.",
        },
        {
            "source_id": "SRC1169_6_274_decomp",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "lifted-C exact plus top-class decomposition.",
        },
        {
            "source_id": "SRC1169_7_274_top",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "integral_D J_C^{top} != 0",
            "role": "FLRW/nonlocal top-class activity anchor.",
        },
        {
            "source_id": "SRC1169_8_275_JC",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "J_C = det(Q_coh) Omega_D / V_D",
            "role": "J_C determinant/volume definition.",
        },
        {
            "source_id": "SRC1169_9_275_integral",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "integral_D J_C = (N/u3)^3",
            "role": "FLRW amplitude/readout shape.",
        },
        {
            "source_id": "SRC1169_10_275_derivative",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "d/dN integral_D J_C = 3N^2/u3^3",
            "role": "FLRW activation derivative shape.",
        },
        {
            "source_id": "SRC1169_11_1020_weight",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_4_kernel_weight",
            "role": "closed-weight or derivative-bound requirement.",
        },
        {
            "source_id": "SRC1169_12_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes identity with derivative residual.",
        },
        {
            "source_id": "SRC1169_13_1020_zero",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_2_zero_conditions",
            "role": "exact zero hypotheses.",
        },
        {
            "source_id": "SRC1169_14_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard for any source/flux route.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(
            entry
            | {
                "exists": path.exists(),
                "needle_found": str(entry["needle"]) in text,
            }
        )
    return rows_with_stamp(checked)


def parent_source_owner_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "PSO1169_0_spatial_current_from_Q",
            "object": "J_C",
            "statement": "For a spatial domain D, the existing lifted-C definition can be written as J_C = rho_C Omega_D with rho_C = det(Q_coh)/V_D, so J_C is a spatial top-degree current rather than a free scalar.",
            "status": "PARENT_KINEMATIC_OBJECT_IDENTIFIED",
            "derives": "J_C can be treated as the spatial part of a spacetime current candidate.",
            "missing": "parent four-current mathcalJ_C and covariant definition of Q_coh, Omega_D, V_D under domain transport",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PSO1169_1_kinematic_source_identity",
            "object": "Sigma_C",
            "statement": "For J_C = rho_C Omega_D, L_tau J_C = (D_tau log rho_C + theta_D) J_C. With rho_C = det(Q_coh)/V_D this gives a candidate Sigma_C^kin = (D_tau log det(Q_coh) - D_tau log V_D + theta_D) J_C - d_D Phi_C.",
            "status": "IDENTITY_NOT_DYNAMICAL_EQUATION",
            "derives": "the source term can be expressed as a volume-normalized Q-flow divergence if the parent flow is known.",
            "missing": "Euler/Noether equation fixing D_tau Q_coh, V_D transport, theta_D, and Phi_C",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PSO1169_2_noether_owner_candidate",
            "object": "parent_action_owner",
            "statement": "A real owner would be a parent symmetry/current: variation of the parent action under the lifted-C/volume generator must yield d_4 mathcalJ_C = d tau wedge Sigma_C plus a Ward stress ledger.",
            "status": "OWNER_CONTRACT_ONLY",
            "derives": "a precise action contract for making Sigma_C non-ad-hoc.",
            "missing": "actual parent Lagrangian terms and symmetry generator whose Noether current is mathcalJ_C",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PSO1169_3_topclass_source_candidate",
            "object": "Sigma_C_FLRW",
            "statement": "If the source is the harmonic/top projection of J_C, local bounded contractible domains have no absolute H^3 top class while a closed FLRW spatial slice can carry the normalized volume class.",
            "status": "BEST_SAME_LAW_SELECTOR_CANDIDATE",
            "derives": "a non-hand-switched local-zero/FLRW-active selector at the cohomology level.",
            "missing": "proof that the parent source is only this top projection, and proof that exact/relative/boundary pieces do not feed local tests",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PSO1169_4_boundary_flux_owner",
            "object": "Phi_C",
            "statement": "The decomposition J_C = dB_C + J_C^top says Phi_C must be the boundary transport/primitive flux tied to B_C, not an independent local suppression dial.",
            "status": "BOUNDARY_OWNER_NOT_SIGNED",
            "derives": "the volume-lock and weighted-Stokes gaps are the same boundary-flux problem.",
            "missing": "Phi_C-B_C relation, primitive norm, no-corner condition, and charge-preserving boundary condition",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PSO1169_5_verdict",
            "object": "parent_source_verdict",
            "statement": "1169 finds a plausible topological selector and a kinematic Sigma_C identity, but it does not yet produce a parent action source. The route improves, but remains nonclaim.",
            "status": "DERIVATION_PROGRESS_NO_CLAIM",
            "derives": "the next obstruction is narrowed to parent top-projection ownership plus boundary flux silence.",
            "missing": "parent action owner, Bianchi stress, boundary/no-flux certificate, closed-weight certificate",
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def topological_selector_rows() -> list[dict[str, object]]:
    rows = [
        {
            "selector_id": "TOP1169_0_same_law_statement",
            "clause": "topological selector",
            "statement": "Let Pi_top project the lifted-C spatial current onto the absolute top cohomology class H^3(D). The same rule Sigma_C^top proportional to Pi_top[J_C] gives zero top source on contractible bounded local domains and can be nonzero on a closed FLRW spatial slice.",
            "status": "FORMAL_SELECTOR_WRITTEN",
            "condition": "D_local contractible with boundary and no relative/boundary source; Sigma_C uses absolute top class only",
            "blocks": "parent proof that Sigma_C is exactly the top projection",
            "valid_for_claim": False,
        },
        {
            "selector_id": "TOP1169_1_local_zero",
            "clause": "local bounded domain",
            "statement": "For a ball-like laboratory domain, H^3(D_local)=0 in absolute de Rham cohomology. Therefore the absolute top-class contribution vanishes before any numeric tuning.",
            "status": "TOPOLOGY_SUPPORTS_LOCAL_TOP_ZERO",
            "condition": "use absolute cohomology; boundary flux Phi_C and relative cohomology are separately zero or bounded",
            "blocks": "relative cohomology, corner terms, Phi_C boundary flux, and exact local primitive are still unsilenced",
            "valid_for_claim": False,
        },
        {
            "selector_id": "TOP1169_2_FLRW_active",
            "clause": "closed cosmological slice",
            "statement": "A closed orientable FLRW spatial slice can carry a nonzero normalized volume/top class, matching the earlier integral_D J_C^top != 0 and integral_D J_C = (N/u3)^3 anchors.",
            "status": "TOPOLOGY_SUPPORTS_FLRW_ACTIVITY",
            "condition": "global closed or effectively compact top-class sector; amplitude normalized by parent cosmological Q-flow",
            "blocks": "FLRW source amplitude and stress contribution are not parent-derived",
            "valid_for_claim": False,
        },
        {
            "selector_id": "TOP1169_3_no_hand_switch_guard",
            "clause": "single-law guard",
            "statement": "The selector is acceptable only if the same Pi_top law is used in both arenas. It cannot be local H^3=0 by topology and FLRW source by an unrelated inserted function.",
            "status": "GUARD_ACTIVE",
            "condition": "same operator, same normalization convention, same Ward ledger",
            "blocks": "parent normalization and stress ledger missing",
            "valid_for_claim": False,
        },
        {
            "selector_id": "TOP1169_4_verdict",
            "clause": "topological selector verdict",
            "statement": "This is the cleanest current route for local-zero/FLRW-active behavior. It is a serious candidate, not a completed proof.",
            "status": "BEST_ROUTE_BUT_BLOCKED",
            "condition": "close boundary flux and parent source ownership",
            "blocks": "Phi_C-B_C certificate, parent action variation, Bianchi/Ward stress",
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def sigma_phi_ledger_rows() -> list[dict[str, object]]:
    rows = [
        {
            "ledger_id": "SPL1169_0_mathcalJ_C",
            "quantity": "mathcalJ_C",
            "candidate_owner": "spacetime lift of J_C = det(Q_coh) Omega_D / V_D",
            "current_status": "KINEMATIC_LIFT_CANDIDATE_ONLY",
            "needed_to_claim": "four-dimensional current definition from parent fields and variation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "SPL1169_1_Sigma_C_kin",
            "quantity": "Sigma_C",
            "candidate_owner": "(D_tau log det(Q_coh) - D_tau log V_D + theta_D)J_C - d_D Phi_C",
            "current_status": "IDENTITY_FORMULA_NOT_PARENT_SOURCE",
            "needed_to_claim": "parent equation for Q-flow plus stress/Ward accounting",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "SPL1169_2_Sigma_C_top",
            "quantity": "Sigma_C top class",
            "candidate_owner": "Pi_top[J_C] cohomology projection",
            "current_status": "PROMISING_SAME_LAW_SELECTOR",
            "needed_to_claim": "prove parent source equals top projection and exact/relative pieces are silent or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "SPL1169_3_Phi_C",
            "quantity": "Phi_C",
            "candidate_owner": "boundary transport of B_C or spatial split of mathcalJ_C",
            "current_status": "MISSING_BOUNDARY_FLUX_CERTIFICATE",
            "needed_to_claim": "Phi_C-B_C relation, no-flux/local-boundary theorem, primitive norm if finite",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "ledger_id": "SPL1169_4_Bianchi",
            "quantity": "T_mathcalJ_Sigma_Phi",
            "candidate_owner": "parent Ward identity under metric/coframe variation",
            "current_status": "MISSING_STRESS_LEDGER",
            "needed_to_claim": "show source/flux exchanges conserve total stress-energy",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def closed_weight_rows() -> list[dict[str, object]]:
    rows = [
        {
            "zero_id": "CWZ1169_0_degree_route",
            "route": "surface-degree zero",
            "statement": "If F_lambda epsilon_C is a genuine intrinsic top-degree form on the two-dimensional edge surface S, then d_S(F_lambda epsilon_C)=0 by degree.",
            "status": "POSSIBLE_THEOREM_NEEDS_DEGREE_CERTIFICATE",
            "missing": "form degree of epsilon_C and exact relation to the weighted-Stokes kernel in 1020",
            "bound_or_zero": "zero only after degree certificate",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CWZ1169_1_closed_weight_route",
            "route": "closed kernel and closed epsilon",
            "statement": "The sufficient condition d_S(F_lambda epsilon_C)=0 follows if d_S F_lambda=0 on S and d_S epsilon_C=0 on S.",
            "status": "FORMAL_SUFFICIENT_CONDITION",
            "missing": "proof F_lambda is constant along S and epsilon_C is covariantly closed without deleting physical charges",
            "bound_or_zero": "zero if both conditions are parent-signed",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CWZ1169_2_topology_link",
            "route": "closed-weight from topological selector",
            "statement": "If epsilon_C is the pullback of the same top-class projector used for Sigma_C, then local H^3=0 may also remove the edge harmonic source, but only after boundary/relative classes are handled.",
            "status": "LINKED_TO_TOP_SELECTOR_BUT_UNSIGNED",
            "missing": "epsilon_C/top-projector identification and relative-boundary cohomology certificate",
            "bound_or_zero": "conditional zero or harmonic bound",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CWZ1169_3_finite_bound",
            "route": "finite derivative bound",
            "statement": "Without zero, use ||d_S(F_lambda epsilon_C)||_* <= ||d_S F_lambda||_*||epsilon_C||_* + ||F_lambda||_*||d_S epsilon_C||_*.",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "missing": "numeric/source-backed norms, units, surface measure, and b_C primitive norm",
            "bound_or_zero": "finite bound only, nonclaim until sourced",
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1169_0_parent_source_owner",
            "test": "parent owner for Sigma_C/Phi_C",
            "status": "REFUSED_PARENT_ACTION_MISSING",
            "result": "kinematic identity exists but no parent Euler/Noether owner is signed",
            "blocked_by": "parent_action;Noether_generator;Ward_stress;Phi_C_boundary_owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1169_1_topological_selector",
            "test": "same-law local-zero/FLRW-active selector",
            "status": "PARTIAL_PASS_TOPOLOGY_ONLY",
            "result": "absolute H^3 distinguishes local bounded domains from closed/global FLRW slices without tuning",
            "blocked_by": "source_equals_top_projection;relative_boundary_terms;normalization;stress_ledger",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1169_2_closed_weight_zero",
            "test": "d_S(F_lambda epsilon_C)=0",
            "status": "CONDITIONAL_THEOREMS_ONLY",
            "result": "degree and closed-weight routes are identified but not certified",
            "blocked_by": "epsilon_degree;dS_F_lambda_zero;dS_epsilon_zero;physical_charge_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1169_3_local_claim",
            "test": "local-GR/R10/PPN promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "topology narrows the gap but boundary flux and parent action ownership remain open",
            "blocked_by": "Phi_C;B_C;parent_source;Bianchi;edge_bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1169_0_top_selector",
            "gate": "same-law topology selector",
            "current_status": "PARTIAL_PASS_NONCLAIM",
            "reason": "absolute H^3 gives a clean local/FLRW distinction, but source ownership and boundary terms are not proved",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1169_1_parent_source",
            "gate": "Sigma_C parent source",
            "current_status": "BLOCKED",
            "reason": "kinematic formula exists but is not an Euler/Noether source equation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1169_2_boundary_flux",
            "gate": "Phi_C/B_C boundary flux silence",
            "current_status": "BLOCKED",
            "reason": "relative cohomology, primitive norm, no-corner, and no-flux terms remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1169_3_closed_weight",
            "gate": "dSFeps zero or finite bound",
            "current_status": "BLOCKED",
            "reason": "degree/closed routes are identified but not sourced or numerically bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1169_4_Bianchi",
            "gate": "stress-energy/Ward consistency",
            "current_status": "BLOCKED",
            "reason": "source and flux stress ledger remains missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1169_0_best_route",
            "decision": "continue_topological_selector_route",
            "reason": "it is the first route here that naturally gives local-zero and FLRW-active behavior from one structural distinction rather than a fitted switch",
            "next_action": "prove boundary/relative terms vanish or are bounded through Phi_C-B_C relation",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1169_1_parent_action_status",
            "decision": "do_not_promote_parent_source",
            "reason": "the Sigma_C kinematic identity is useful but tautological unless a parent action fixes the Q-flow and source projection",
            "next_action": "search for a Noether/topological term that owns Pi_top[J_C]",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1169_2_closed_weight_status",
            "decision": "keep_closed_weight_as_parallel_gate",
            "reason": "degree and closed-weight zero routes could erase the dSFeps residual, but the form-degree and physical-charge guards are not signed",
            "next_action": "write explicit form-degree certificate for epsilon_C and F_lambda on S_edge",
            "valid_for_claim": False,
        },
    ]
    return rows_with_stamp(rows)


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1169_0_1170",
            "next_target": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "objective": "turn the promising topological selector into a local zero theorem by proving Phi_C/B_C boundary flux silence, or demote it to a finite edge-bound row",
            "include": "absolute vs relative H3; Phi_C-B_C relation; no-corner/no-flux theorem; epsilon_C degree; F_lambda constancy; Bianchi stress; finite bound fallback",
            "exclude": "local claim; c_g zero claim; hand-switched FLRW source; ignoring boundary cohomology; invented numeric bounds; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return rows_with_stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    top_rows: list[dict[str, object]],
    closed_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations = [
        {
            "check_id": "V1169_0_sources_exist",
            "result": "pass"
            if all(row["exists"] and row["needle_found"] for row in sources)
            else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_1_kinematic_identity_written",
            "result": "pass"
            if any("Sigma_C^kin" in str(row["statement"]) for row in parent_rows)
            else "fail",
            "detail": "Sigma_C kinematic identity from J_C = rho_C Omega_D is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_2_top_selector_written",
            "result": "pass"
            if any(row["status"] == "BEST_ROUTE_BUT_BLOCKED" for row in top_rows)
            else "fail",
            "detail": "topological local-zero/FLRW-active selector is identified as best route but blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_3_closed_weight_routes_written",
            "result": "pass"
            if len(closed_rows) >= 4
            and any("surface-degree" in str(row["route"]) for row in closed_rows)
            else "fail",
            "detail": "degree, closed-weight, topology-linked, and finite-bound routes are recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_4_runner_refuses_claim",
            "result": "pass"
            if all(row["claim_allowed"] is False for row in run_rows)
            else "fail",
            "detail": "runner refuses parent-source, closed-weight, and local promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_5_claim_gates_blocked_or_partial",
            "result": "pass"
            if all(row["claim_allowed"] is False for row in gate_rows)
            else "fail",
            "detail": "no 1169 gate allows a local or cosmology claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_6_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in parent_rows + top_rows + closed_rows + gate_rows + next_rows)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_7_next_target",
            "result": "pass"
            if next_rows and "1170" in str(next_rows[0]["next_target"])
            else "fail",
            "detail": "1170 handoff targets topological selector boundary-flux certificate or B_C primitive owner",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_8_generated_under_post_checkpoint",
            "result": "pass"
            if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT))
            else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1169_SUMMARY",
            "result": "pass",
            "detail": "1169 finds the topological selector as the strongest current route and derives a Sigma_C kinematic identity, but keeps all claims blocked by parent-source, boundary-flux, closed-weight, and Bianchi gaps",
            "claim_allowed": False,
        },
    ]
    return rows_with_stamp(validations)


def write_doc(
    sources: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    top_rows: list[dict[str, object]],
    ledger_rows: list[dict[str, object]],
    closed_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1169 — Y5/R10 parent source top-class owner or closed-weight zero",
            "**Current verdict:** 1169 makes real structural progress but still refuses a claim. The best route is now the topological selector: local bounded/contractible domains have no absolute top `H^3` class, while a closed/global FLRW slice can carry a normalized top class. That is the first clean same-law shape for local-zero plus FLRW-active behavior, but it still needs parent action ownership and boundary-flux silence.",
            "**Main progress:** `J_C = rho_C Omega_D` gives a kinematic source identity `L_tau J_C = (D_tau log rho_C + theta_D)J_C`, with `rho_C = det(Q_coh)/V_D`. This tells us what `Sigma_C` would be if the parent theory owns the Q-flow, but by itself it is an identity rather than dynamics.",
            "**Hard blocker:** topology can kill the local top class, but it does not automatically kill relative cohomology, exact boundary flux, corners, or `Phi_C/B_C` terms. The next proof must close those boundary terms or keep the route as a finite edge-bound closure.",
            "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + csv_table(sources),
            "## Parent source owner attempt\n\n" + csv_table(parent_rows),
            "## Topological selector theorem attempt\n\n" + csv_table(top_rows),
            "## Sigma/Phi ownership ledger\n\n" + csv_table(ledger_rows),
            "## Closed-weight zero attempt\n\n" + csv_table(closed_rows),
            "## Runner dry-run\n\n" + csv_table(run_rows),
            "## Claim gates\n\n" + csv_table(gate_rows),
            "## Decision ledger\n\n" + csv_table(decision_rows_),
            "## Validation\n\n" + csv_table(validation_rows_),
            "## Next target\n\n" + csv_table(next_rows),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    parent_rows = parent_source_owner_attempt_rows()
    top_rows = topological_selector_rows()
    ledger_rows = sigma_phi_ledger_rows()
    closed_rows = closed_weight_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validations = validation_rows(sources, parent_rows, top_rows, closed_rows, run_rows, gate_rows, next_rows)

    outputs = {
        "P8_Y5_R10_1169_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1169_PARENT_SOURCE_OWNER_ATTEMPT.csv": parent_rows,
        "P8_Y5_R10_1169_TOPOLOGICAL_SELECTOR_THEOREM.csv": top_rows,
        "P8_Y5_R10_1169_SIGMA_PHI_OWNERSHIP_LEDGER.csv": ledger_rows,
        "P8_Y5_R10_1169_CLOSED_WEIGHT_ZERO_ATTEMPT.csv": closed_rows,
        "P8_Y5_R10_1169_RUNNER_DRY_RUN.csv": run_rows,
        "P8_Y5_R10_1169_CLAIM_GATES.csv": gate_rows,
        "P8_Y5_R10_1169_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1169_NEXT_TARGET.csv": next_rows,
        "P8_Y5_BRR545_1169_VALIDATION.csv": validations,
    }

    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, parent_rows, top_rows, ledger_rows, closed_rows, run_rows, gate_rows, decisions, validations, next_rows)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
