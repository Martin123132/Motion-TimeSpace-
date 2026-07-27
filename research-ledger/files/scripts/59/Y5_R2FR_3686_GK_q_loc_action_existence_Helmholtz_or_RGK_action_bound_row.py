from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3686"
BRANCH_ID = "MTS_R2FR_Y5_GK_QLOC_ACTION_EXISTENCE_HELMHOLTZ_OR_RGK_ACTION_BOUND_ROW_3686"
DOC = ROOT / "3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md"


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
        ("handoff_3685", RESIDUALS / "P8_Y5_R2FR_3685_NEXT_TARGET.csv", "S_GK", "3685 selected GK/q_loc action existence as first hard sector"),
        ("sector_3685", RESIDUALS / "P8_Y5_R2FR_3685_SECTOR_CERTIFICATE_ROWS.csv", "SEC3685_3_GK", "GK sector certificate marks action existence and first variation as the blocker"),
        ("spine_3685", RESIDUALS / "P8_Y5_R2FR_3685_TRIAL_PARENT_ACTION_SPINE_ROWS.csv", "SPN3685_3_GK_q_loc", "trial parent spine contains the GK/q_loc sector but does not adopt it"),
        ("bound_3685", RESIDUALS / "P8_Y5_R2FR_3685_RPARENT_LTHETAQ_BOUND_ROWS.csv", "RPB3685_1_GK_action", "R_GK_action is the component residual to fill or derive away"),
        ("gk_contract", RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "original first-variation contract for Gamma/Khat/q_loc"),
        ("response_3540", RESIDUALS / "P8_Y5_R2FR_3540_PARENT_RESPONSE_ACTION.csv", "PAC3540_4_Ward_reduction", "clean response-action Ward route"),
        ("parent_clause_3630", RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv", "PAC3630_2_even_response", "single parent-action clause with even response sector"),
        ("ward_3539", RESIDUALS / "P8_Y5_R2FR_3539_METRIC_RESPONSE_WARD_ROUTE.csv", "WRT3539_3_qloc_identity", "metric-response Ward identity for q_loc"),
        ("qloc_tests_3539", RESIDUALS / "P8_Y5_R2FR_3539_QLOC_ZERO_TESTS.csv", "QZT3539_7_verdict", "signed-gate list for q_loc theorem zero"),
        ("scalar_3628", RESIDUALS / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv", "GSD3628_2_even_response_doublet", "best clean scalar-density candidate"),
        ("kcompare_3628", RESIDUALS / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv", "KMC3628_5_verdict", "Khat versus metric-response comparison"),
        ("double_zero_3628", RESIDUALS / "P8_Y5_R2FR_3628_FIXED_POINT_DOUBLE_ZERO_GATE.csv", "FPG3628_2_F1_zero", "F1=0 double-zero gate for the even response template"),
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


def action_existence_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "GKA3686_0_target",
            "derive live parent S_GK",
            "Find an MTS-owned diffeomorphism-invariant S_GK whose first variation supplies theta_GK, Q_tau^GK, C_tau^GK and P_loc(nabla Gamma_eff - div K_hat - J_M)=0.",
            "TARGET_NOT_PROVED",
            "the target is exact; the live parent action is not yet signed",
            False,
        ),
        (
            "GKA3686_1_clean_response_candidate",
            "construct clean response-action template",
            "S_GK^clean[Y;g] = -int sqrt(-g)[Gamma0 + 1/2 G_AB g^{mu nu} D_mu Y^A D_nu Y^B + 1/2 M_AB Y^A Y^B + O(Y^4)].",
            "CLEAN_CONDITIONAL_ACTION_WRITTEN",
            "this is an actual variational object, not a plateau axiom",
            True,
        ),
        (
            "GKA3686_2_first_variation",
            "extract Euler, stress and symplectic current from the clean template",
            "delta S_GK^clean = int sqrt(-g)[E_A delta Y^A - 1/2 T_GK^{mu nu} delta g_{mu nu}] + int dTheta_GK.",
            "EXACT_FOR_CLEAN_TEMPLATE",
            "theta_GK and stress exist if Y^A, G_AB, M_AB, D_mu and the boundary class are parent-owned",
            True,
        ),
        (
            "GKA3686_3_Ward_identity",
            "route q_loc through an Euler/Ward residual",
            "If K_hat=K_metric[Gamma_eff], then q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho) up to the locked stress sign convention.",
            "EXACT_IF_KMATCH_AND_NOFLUX",
            "this is the legal replacement for a hand-inserted local-vacuum plateau",
            True,
        ),
        (
            "GKA3686_4_live_ownership",
            "show current MTS owns the response variables and coefficients",
            "Y^A, G_AB, M_AB, D_mu, Gamma0, source support and local quotient must be declared before variation, not chosen after readout.",
            "NOT_SIGNED",
            "without ownership the clean action remains a derivation candidate, not current MTS evidence",
            False,
        ),
        (
            "GKA3686_5_Helmholtz",
            "prove actual Gamma_eff/K_hat are variational",
            "The live K_hat/Gamma_eff pair must satisfy Helmholtz symmetry: the proposed stress must be the metric response of one scalar density.",
            "NOT_PROVED_FOR_LIVE_SYMBOLS",
            "a non-variational K_hat cannot be hidden inside an action-derived local-GR proof",
            False,
        ),
        (
            "GKA3686_6_double_zero",
            "derive F1=0 rather than assume it",
            "In the even response template Gamma_eff-Gamma0=O(Y^2), T_GK(Phi0)=0 after subtraction and partial_A T_GK|0=0.",
            "DERIVED_FOR_TEMPLATE_PARENT_MAPPING_MISSING",
            "the double zero is real mathematics for the template, but not yet live MTS unless Y maps to the physical residual",
            True,
        ),
        (
            "GKA3686_7_verdict",
            "claim S_GK action existence for current MTS",
            "All ownership, Helmholtz, Delta_K, no-linear-source, coercivity, boundary and P_loc gates must pass.",
            "S_GK_LIVE_THEOREM_NOT_CLAIMED_RGK_ACTION_RETAINED",
            "promote R_GK_action as the finite residual vector for local-GR/Newton/source-coupling discipline",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "formal_template_passed": formal_template_passed,
            "claim_allowed": False,
            "score_ready": False,
        }
        for audit_id, claim, mathematical_statement, status, consequence, formal_template_passed in specs
    ]


def response_action_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RAC3686_0_clean_action",
            "clean variational spine",
            "S_GK^clean[Y;g] = -int sqrt(-g)[Gamma0 + 1/2 G_AB g^{mu nu} D_mu Y^A D_nu Y^B + 1/2 M_AB Y^A Y^B + O(Y^4)]",
            "Y^A response variables, G_AB kinetic metric, M_AB mass/coercivity matrix, D_mu connection/projector",
            "all objects declared in parent before fitting or local readout",
            "CANDIDATE_READY_NOT_ADOPTED",
        ),
        (
            "RAC3686_1_Euler_operator",
            "response Euler equation",
            "E_A = L_AB Y^B - J_A - B_A, with L_AB = -D_mu(G_AB D^mu) + M_AB + curvature/projector terms",
            "compact source-free branch gives Y=0 if L_AB is positive and J_A=B_A=0",
            "positive/self-adjoint operator and no hidden linear source",
            "FORMAL_ROUTE_READY_INPUTS_UNSIGNED",
        ),
        (
            "RAC3686_2_metric_response",
            "metric stress response",
            "T_GK^{mu nu} = Gamma_eff g^{mu nu} - K_metric^{mu nu}, K_metric^{mu nu}=G_AB D^mu Y^A D^nu Y^B + coefficient-response terms",
            "K_hat must equal K_metric in the live MTS branch",
            "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}=0",
            "KMETRIC_FORMULA_READY_KHAT_MATCH_UNSIGNED",
        ),
        (
            "RAC3686_3_q_loc_Ward",
            "local force residual route",
            "q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})",
            "q_loc vanishes only on shell, no-flux, and Delta_K=0",
            "E_A=0, B_GK=0, Delta_K=0, P_loc parent-owned",
            "WARD_REDUCTION_EXACT_CONDITIONAL",
        ),
        (
            "RAC3686_4_fixed_point",
            "double-zero local-vacuum branch",
            "Y=0, D_mu Y=0, Gamma_eff-Gamma0=O(Y^2), partial_A T_GK|0=0",
            "F1=0 comes from evenness and background subtraction",
            "Y must be physical local residual, not a bookkeeping shadow",
            "F1_ZERO_DERIVED_FOR_TEMPLATE_ONLY",
        ),
        (
            "RAC3686_5_EM_Poynting_separation",
            "wave/Poynting stress handling",
            "If flux fields F^A_{mu nu} are present, S_flux=-int sqrt(-g) 1/4 W_AB F^A_{rho sigma}F^{B rho sigma} contributes ordinary physical stress/current.",
            "Poynting/vector flux may be an owned physical sector, but cannot be used as a hidden q_loc zero proof",
            "F, W, J and boundary flux declared; no double-counting against EM stress",
            "USEFUL_PHYSICAL_BRANCH_SEPARATE_FROM_LOCAL_ZERO_CLAIM",
        ),
        (
            "RAC3686_6_verdict",
            "clean response action as current MTS S_GK",
            "The clean action can be used for algebraic continuation, but current MTS has not signed ownership and Helmholtz/Khat equality.",
            "R_GK_action remains nonzero until the live-symbol match is completed",
            "all Helmholtz gate rows must pass",
            "NOT_ADOPTED_NONCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "candidate_id": candidate_id,
            "object": object_name,
            "mathematical_statement": mathematical_statement,
            "derived_use": derived_use,
            "required_signature": required_signature,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for candidate_id, object_name, mathematical_statement, derived_use, required_signature, status in specs
    ]


def helmholtz_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "HLG3686_0_action_ownership",
            "parent ownership of clean variables",
            "Y^A, G_AB, M_AB, D_mu, Gamma0, support and quotient data are present in S_parent before variation",
            "not parent-signed in current corpus",
            "R_action_ownership",
            "FAIL_LIVE_CLAIM",
        ),
        (
            "HLG3686_1_Helmholtz_symmetry",
            "variational integrability of live Gamma_eff/K_hat",
            "second functional variations commute for the proposed metric/source response",
            "candidate formula exists; actual live K_hat pair not checked/signed",
            "R_Helmholtz",
            "OPEN",
        ),
        (
            "HLG3686_2_DeltaK_zero",
            "K_hat equals K_metric[Gamma_eff]",
            "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}=0 under one sign/volume convention",
            "3628 says Kmetric constructed, Khat match not claimed",
            "R_DeltaK",
            "OPEN_HIGH_VALUE",
        ),
        (
            "HLG3686_3_no_linear_source",
            "no hidden J_A Y^A source spurion",
            "J_A=0 in compact local vacuum or J_A is Hilbert/physical-stress-owned and bounded",
            "coupling/source silence remains the gut-level hard gap",
            "R_linear_source",
            "OPEN_CORE_COUPLING_GAP",
        ),
        (
            "HLG3686_4_coercivity",
            "positive/self-adjoint local operator",
            "M_AB positive and H/G_AB elliptic after constraints and gauge removal",
            "formal requirement written, no parent proof or numeric lower bound",
            "R_coercivity",
            "OPEN",
        ),
        (
            "HLG3686_5_boundary_no_flux",
            "boundary/symplectic no-flux",
            "B_GK^nu=0 or P_loc annihilates exact boundary/domain flux on the local branch",
            "boundary handoff remains open",
            "R_boundary",
            "OPEN",
        ),
        (
            "HLG3686_6_Ploc_owner",
            "projector ownership",
            "P_loc is parent-owned by the same quotient/readout stack and is not data-chosen",
            "P_loc owner still conditional",
            "R_Ploc",
            "OPEN",
        ),
        (
            "HLG3686_7_verdict",
            "live S_GK theorem pass",
            "all HLG3686_0 through HLG3686_6 pass",
            "several hard clauses fail or are unsigned",
            "R_GK_action",
            "THEOREM_FAILS_RESIDUAL_RETAINED",
        ),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "exact_requirement": exact_requirement,
            "current_evidence": current_evidence,
            "residual_if_failed": residual_if_failed,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for gate_id, gate, exact_requirement, current_evidence, residual_if_failed, status in specs
    ]


def residual_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RGB3686_0_total",
            "abs(R_GK_action)/N_H",
            "(|R_action_ownership|+|R_Helmholtz|+|R_DeltaK|+|R_linear_source|+|R_coercivity|+|R_boundary|+|R_Ploc|)/N_H",
            "dimensionless no-cancellation envelope",
            "FORMULA_READY_INPUTS_MISSING",
            "finite GK action residual vector; no local-GR/Newton claim until every component is zero or bounded",
            "HLG3686_7_verdict",
        ),
        (
            "RGB3686_1_action_ownership",
            "abs(R_action_ownership)/N_H",
            "MISSING_PARENT_OWNED_Y_G_M_D_SUPPORT_QUOTIENT",
            "dimensionless",
            "MISSING_PARENT_INPUT",
            "clean variables are not yet live MTS fields",
            "HLG3686_0_action_ownership",
        ),
        (
            "RGB3686_2_Helmholtz",
            "abs(R_Helmholtz)/N_H",
            "MISSING_HELMHOLTZ_SECOND_VARIATION_MATRIX",
            "dimensionless",
            "MISSING_VARIATIONAL_INTEGRABILITY_INPUT",
            "actual Gamma/Khat may still be non-variational",
            "HLG3686_1_Helmholtz_symmetry",
        ),
        (
            "RGB3686_3_DeltaK",
            "abs(R_DeltaK)/N_H",
            "MISSING_DELTA_K_TENSOR_NORM",
            "dimensionless",
            "MISSING_KHAT_METRIC_RESPONSE_MATCH",
            "K_hat=K_metric is the highest-value next target",
            "HLG3686_2_DeltaK_zero",
        ),
        (
            "RGB3686_4_linear_source",
            "abs(R_linear_source)/N_H",
            "MISSING_J_A_SOURCE_COUPLING_BOUND",
            "dimensionless",
            "MISSING_SOURCE_COUPLING_INPUT",
            "ordinary matter must not linearly re-source the local residual field",
            "HLG3686_3_no_linear_source",
        ),
        (
            "RGB3686_5_coercivity",
            "abs(R_coercivity)/N_H",
            "MISSING_OPERATOR_GAP_OR_POSITIVITY_BOUND",
            "dimensionless",
            "MISSING_OPERATOR_BOUND",
            "without a positive operator, local hair may survive",
            "HLG3686_4_coercivity",
        ),
        (
            "RGB3686_6_boundary",
            "abs(R_boundary)/N_H",
            "MISSING_BOUNDARY_NO_FLUX_OR_PROJECTED_EXACT_TERM",
            "dimensionless",
            "MISSING_BOUNDARY_INPUT",
            "bulk action silence cannot leak through linking surfaces or source mass handoff",
            "HLG3686_5_boundary_no_flux",
        ),
        (
            "RGB3686_7_Ploc",
            "abs(R_Ploc)/N_H",
            "MISSING_PARENT_PLOC_OWNER_AND_COMMUTATOR_BOUND",
            "dimensionless",
            "MISSING_PROJECTOR_INPUT",
            "projection cannot be a fit/readout trick",
            "HLG3686_6_Ploc_owner",
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
        ("DEC3686_0_result", "CLEAN_ACTION_CONSTRUCTED_LIVE_SGK_NOT_CLAIMED", "clean response-action template exists and derives the right kind of Ward identity", "do not claim local-GR/Newton; use it as the next algebraic ladder"),
        ("DEC3686_1_progress", "REAL_DERIVATION_PROGRESS", "F1=0 is derived for the even response template instead of asserted", "focus next on live-symbol matching rather than another broad source sweep"),
        ("DEC3686_2_blocker", "COUPLING_AND_KHAT_MATCH_ARE_CORE", "R_linear_source and R_DeltaK are the most important surviving components", "derive or bound source coupling and Khat=Kmetric first"),
        ("DEC3686_3_EM_policy", "POYNTING_STRESS_SEPARATED", "wave/EM flux is allowed as a physical stress sector, not as hidden q_loc closure", "later EM branch can use S_flux with explicit F,W,J and boundary flux"),
        ("DEC3686_4_next", "NEXT_BEST_TARGET", "test the actual live Gamma_eff/K_hat symbols against the clean response action", "run 3687 Helmholtz matrix plus Delta_K bound row"),
        ("DEC3686_5_private", "PRIVATE_NONCLAIM", "no public/GitHub/local-GR claim follows from this checkpoint", "continue framework derivation privately"),
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
        ("CG3686_0_live_SGK", "claim current MTS owns S_GK", "BLOCKED_OWNERSHIP_AND_HELMHOLTZ", "clean candidate is not yet the signed live parent sector"),
        ("CG3686_1_q_loc_zero", "claim q_loc^nu=0 in local vacuum", "BLOCKED_DELTAK_SOURCE_BOUNDARY_PLOC", "Ward zero needs Delta_K=0, E_A=0, no-flux and parent P_loc"),
        ("CG3686_2_Newton_GR", "claim derived local GR/Newton limit", "BLOCKED_RGK_ACTION", "R_GK_action remains a finite nonclaim residual vector"),
        ("CG3686_3_source_coupling", "claim ordinary matter does not source Y linearly", "BLOCKED_JA_COUPLING", "J_A=0 or bounded coupling is not derived"),
        ("CG3686_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "this is a private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3686_0",
            "status": "CLEAN_RESPONSE_ACTION_DERIVED_CONDITIONALLY_LIVE_SGK_NOT_CLAIMED_RGK_ACTION_BOUND_VECTOR_STAGED",
            "summary": "3686 builds the real variational candidate for Gamma/Khat/q_loc, derives the conditional Ward/double-zero route, and retains R_GK_action because live ownership, Helmholtz, Khat matching, coupling silence, coercivity, boundary and P_loc gates are unsigned.",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3686_0",
            "target_doc": "3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3687_clean_response_action_Helmholtz_matrix_or_DeltaK_bound_row.py",
            "objective": "test actual Gamma_eff/K_hat against the clean response action by building the Helmholtz/second-variation symmetry matrix and Delta_K=K_hat-K_metric[Gamma_eff] gate; if unmatched, retain R_Helmholtz+R_DeltaK bound rows",
            "success_gate": "live Gamma_eff/K_hat passes Helmholtz and Delta_K=0 under one convention, or the unmatched pieces are converted into explicit nonclaim bound rows",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    candidates: list[dict[str, object]],
    gates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3686 - GK q_loc action existence Helmholtz or R_GK_action bound row",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint takes the hard sector from 3685 and tries the derivation route first. It constructs the clean response-action branch explicitly, derives the conditional Ward/double-zero route, and refuses to claim the live MTS `S_GK` because the live ownership and Helmholtz/Khat/coupling/boundary gates are still unsigned.",
        "",
        "## Main result",
        "",
        "Clean action candidate:",
        "",
        "`S_GK^clean[Y;g] = -int sqrt(-g)[Gamma0 + 1/2 G_AB g^{mu nu} D_mu Y^A D_nu Y^B + 1/2 M_AB Y^A Y^B + O(Y^4)]`.",
        "",
        "First variation route:",
        "",
        "`delta S_GK^clean = int sqrt(-g)[E_A delta Y^A - 1/2 T_GK^{mu nu} delta g_{mu nu}] + int dTheta_GK`.",
        "",
        "Ward/q_loc route:",
        "",
        "`q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})`.",
        "",
        "where",
        "",
        "`Delta_K^{mu nu} := K_hat^{mu nu} - K_metric^{mu nu}[Gamma_eff]`.",
        "",
        "Even-template double zero:",
        "",
        "`Gamma_eff-Gamma0=O(Y^2)` and `partial_A T_GK^{mu nu}|0=0` for the clean even response template.",
        "",
        "Non-adoption verdict:",
        "",
        "`R_GK_action != 0` is retained because live parent ownership, Helmholtz symmetry, `Delta_K=0`, source-coupling silence, coercivity, boundary no-flux and `P_loc` ownership are not signed.",
        "",
        "Residual vector:",
        "",
        "`abs(R_GK_action)/N_H <= (|R_action_ownership|+|R_Helmholtz|+|R_DeltaK|+|R_linear_source|+|R_coercivity|+|R_boundary|+|R_Ploc|)/N_H`.",
        "",
        "## Action existence audit",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## Response action candidates"])
    for row in candidates:
        lines.append(f"- `{row['candidate_id']}`: {row['status']} - {row['object']} -> {row['derived_use']}")
    lines.extend(["", "## Helmholtz and live-symbol gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Residual bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    candidates: list[dict[str, object]],
    gates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
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
    generated = sources + audit + candidates + gates + bounds + decisions + claim_gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3686*", "3686-Y5-R2FR-*", "P8_Y5*3686*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    audit_by_id = {str(row["audit_id"]): row for row in audit}
    candidate_by_id = {str(row["candidate_id"]): row for row in candidates}
    gate_by_id = {str(row["gate_id"]): row for row in gates}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}

    required_components = ["R_action_ownership", "R_Helmholtz", "R_DeltaK", "R_linear_source", "R_coercivity", "R_boundary", "R_Ploc"]
    total_formula = str(bound_by_id["RGB3686_0_total"]["bound_or_formula"])

    add("VAL3686_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3686_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3686_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3686 outputs written")
    add("VAL3686_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3686_4_clean_action", "S_GK^clean" in candidate_by_id["RAC3686_0_clean_action"]["mathematical_statement"] and "Gamma0" in candidate_by_id["RAC3686_0_clean_action"]["mathematical_statement"], "clean response action candidate is written")
    add("VAL3686_5_first_variation", "delta S_GK^clean" in audit_by_id["GKA3686_2_first_variation"]["mathematical_statement"] and audit_by_id["GKA3686_2_first_variation"]["formal_template_passed"] is True, "first variation exists for clean template")
    add("VAL3686_6_ward_reduction", "q_loc^nu" in candidate_by_id["RAC3686_3_q_loc_Ward"]["mathematical_statement"] and "Delta_K" in candidate_by_id["RAC3686_3_q_loc_Ward"]["mathematical_statement"], "q_loc Ward route includes Euler, boundary and Delta_K terms")
    add("VAL3686_7_double_zero", audit_by_id["GKA3686_6_double_zero"]["status"] == "DERIVED_FOR_TEMPLATE_PARENT_MAPPING_MISSING", "F1=0 is derived only for the even template")
    add("VAL3686_8_live_not_claimed", audit_by_id["GKA3686_7_verdict"]["status"] == "S_GK_LIVE_THEOREM_NOT_CLAIMED_RGK_ACTION_RETAINED" and gate_by_id["HLG3686_7_verdict"]["status"] == "THEOREM_FAILS_RESIDUAL_RETAINED", "live S_GK theorem is not claimed")
    add("VAL3686_9_bound_components", all(component in total_formula for component in required_components), "R_GK_action envelope contains every required component")
    add("VAL3686_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in claim_gates), "claim gates remain blocked")
    add("VAL3686_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3686_12_doc_written", "S_GK^clean" in doc_text and "R_GK_action != 0" in doc_text and "Delta_K" in doc_text, "doc records clean action, non-adoption and residual vector")
    add("VAL3686_13_next_target", next_target[0]["target_doc"].startswith("3687-") and "Delta_K" in next_target[0]["objective"], "3687 targets Helmholtz/Delta_K")
    add("VAL3686_14_no_formalization_leak", not leaks, "no 3686 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = action_existence_audit_rows(ts)
    candidates = response_action_rows(ts)
    gates = helmholtz_gate_rows(ts)
    bounds = residual_bound_rows(ts)
    decisions = decision_rows(ts)
    claim_gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3686_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3686_GK_ACTION_EXISTENCE_AUDIT.csv",
        "candidates": RESIDUALS / "P8_Y5_R2FR_3686_RESPONSE_ACTION_CANDIDATE_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3686_HELMHOLTZ_GATE_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3686_RGK_ACTION_BOUND_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3686_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3686_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3686_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3686_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3686_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["candidates"], candidates)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, candidates, gates, bounds, decisions, claim_gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, candidates, gates, bounds, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3686 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3686 checkpoint: clean GK action derived conditionally; live S_GK not claimed; R_GK_action vector staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
