from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1879"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md"

INPUTS = {
    "1878_doc": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
    "1878_validation": OUT / "P8_Y5_BRR545_1878_VALIDATION.csv",
    "1878_finite_dobs": OUT / "P8_Y5_PARENT_QLOC_1878_FINITE_DOBS_E_LEAK_ROWS.csv",
    "1878_next": OUT / "P8_Y5_PARENT_QLOC_1878_NEXT_TARGET.csv",
    "1739_doc": ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md",
    "1739_bg_rows": OUT / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
    "1029_no_shadow": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "1030_spm_gate": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "1088_matter_signature": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
}

SOURCE_NEEDLES = {
    "1878_doc": [
        "physics cannot forget what clocks and rulers actually read",
        "PARENT_COFRAME_OWNERSHIP_OR_BG_BOUND_SELECTED_NEXT",
    ],
    "1878_validation": [
        "VAL1878_OVERALL,PASS",
    ],
    "1878_finite_dobs": [
        "FDOBS1878_1_common_weyl",
        "MISSING_B_R_ZERO_THEOREM_OR_BOUND",
    ],
    "1878_next": [
        "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
        "selected",
    ],
    "1739_doc": [
        "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
        "BG_ROW_IS_THE_TESTABLE_INTERFACE",
    ],
    "1739_bg_rows": [
        "BG1739_3_RAB_Jq",
        "RETAINED_NONCLAIM_BG_ROW",
    ],
    "1029_no_shadow": [
        "Current MTS does not yet prove c_g=0.",
        "common-frame counterexample blocks WEP-only c_g zero",
    ],
    "1030_spm_gate": [
        "Ward identities do not derive the single public metric",
        "EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
    ],
    "1088_matter_signature": [
        "e_obs=E(q(Phi))",
        "CONDITIONAL_GEOMETRY_SUBLEMMA",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1879_SOURCE_REGISTER.csv",
    "ownership_stack": OUT / "P8_Y5_PARENT_QLOC_1879_PARENT_COFRAME_OWNERSHIP_STACK.csv",
    "no_shadow_tests": OUT / "P8_Y5_PARENT_QLOC_1879_NO_SHADOW_FRAME_TESTS.csv",
    "leak_bound_rows": OUT / "P8_Y5_PARENT_QLOC_1879_COMMON_FRAME_LEAK_BOUND_ROWS.csv",
    "arena_interface": OUT / "P8_Y5_PARENT_QLOC_1879_ARENA_BOUND_INTERFACE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1879_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1879_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1879_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1879_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1879": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def ownership_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_0_parent_q",
            "clause": "parent observed quotient Q_vis is constructed before local readout",
            "mathematical_test": "q: Phi_parent -> Q_vis and Dq are parent-owned, not postselected for local tests",
            "current_status": "MISSING_PARENT_Q_CONSTRUCTION",
            "effect_if_closed": "lets chain-rule kernel tests become meaningful",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_1_coframe_owner",
            "clause": "observed coframe has no C_R/J_q argument",
            "mathematical_test": "e_obs=E(Q_vis) with C_R/R_AB/J_q excluded or already constrained before readout",
            "current_status": "MISSING_PARENT_COFRAME_OWNERSHIP",
            "effect_if_closed": "kills epsilon_R_cell by ownership rather than fitting",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_2_no_weyl_shadow",
            "clause": "no common Weyl shadow frame",
            "mathematical_test": "A_R'(0)=0 or no independent A_R(C_R) slot exists in S_matter/readout",
            "current_status": "MISSING_NO_SHADOW_FRAME_THEOREM",
            "effect_if_closed": "sets b_R=0",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_3_no_disformal_shadow",
            "clause": "no common disformal or preferred-frame shadow",
            "mathematical_test": "B_R'(0)=0 or no U_mu U_nu disformal/current slot exists",
            "current_status": "MISSING_DISFORMAL_ZERO_THEOREM",
            "effect_if_closed": "sets d_R=0 and protects preferred-frame PPN",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_4_source_prefactor",
            "clause": "no source-only matter prefactor hidden inside one public frame",
            "mathematical_test": "delta w_A(C_R)=0 or source-weight current has zero local projection",
            "current_status": "MISSING_SOURCE_PREFACTOR_ZERO_THEOREM",
            "effect_if_closed": "prevents WEP-clean but Hilbert-source-active coupling",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_5_connection_boundary_tau",
            "clause": "connection, boundary endpoints, source normals, and tau descend through Q_vis",
            "mathematical_test": "Domega, P_loc endpoint derivative, source support, and tau pushforward have no C_R leak",
            "current_status": "MISSING_CONNECTION_BOUNDARY_TAU_DESCENT",
            "effect_if_closed": "prevents coframe zero from being reopened by readout/endpoints",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stack_id": "PCO1879_6_verdict",
            "clause": "parent coframe ownership closes common-frame leak",
            "mathematical_test": "PCO1879_0 through PCO1879_5 all parent-signed",
            "current_status": "PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS",
            "effect_if_closed": "returns to local-GR derivation path with DObs_e branch silenced",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def no_shadow_tests_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_0_chain_rule",
            "test": "chain-rule no-shadow theorem",
            "calculation": "if e_obs=E(Q_vis) and C_R is excluded from Q_vis or in ker(Dq), then D_C_R e_obs=0 and b_R=0",
            "result": "EXACT_CONDITIONAL",
            "blocker": "parent Q_vis and coframe ownership not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_1_covariance",
            "test": "diffeomorphism covariance forbids shadow frame",
            "calculation": "S_m[Psi,A_R(C_R)^2 g_obs] is covariant",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "blocker": "covariance does not forbid common conformal/disformal factors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_2_WEP",
            "test": "WEP universality forbids common-frame leak",
            "calculation": "universal A_R(C_R) can preserve composition universality while shifting clocks/PPN/source normalization",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "blocker": "WEP alone can miss common-mode metric/source shifts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_3_Ward",
            "test": "Ward conservation forbids shadow frame",
            "calculation": "nabla_mu T^{mu nu}=0 holds in the chosen matter geometry even with A_R(C_R)",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "blocker": "Ward identities are homogeneous under hidden common-frame/source-weight choices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_4_terminal_public_metric",
            "test": "terminal public coframe object excludes extra frame slots",
            "calculation": "Allowed[S_matter] excludes A_R(C_R), B_R(C_R), source weights, and endpoint coframe arguments",
            "result": "BEST_CONDITIONAL_ROUTE_NOT_PARENT_DERIVED",
            "blocker": "terminal/quotient naturality clause remains a closure contract, not a derived parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NSF1879_5_verdict",
            "test": "current corpus proves no-shadow-frame and b_R=d_R=0",
            "calculation": "NSF1879_0 through NSF1879_4 close with parent signatures",
            "result": "NO_SHADOW_FRAME_NOT_DERIVED_CURRENT_CORPUS",
            "blocker": "finite common-frame leak rows remain mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def leak_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFL1879_0_bR",
            "symbol": "b_R",
            "meaning": "common Weyl/log-coframe derivative with respect to C_R/R_AB",
            "formula": "b_R := d ln A_R(C_R)/dC_R | local background, or ||e_obs^-1 D_C_R e_obs||",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_links": "PPN;clock;WEP;orbital;local_GR",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFL1879_1_dR",
            "symbol": "d_R",
            "meaning": "common disformal/preferred-frame derivative",
            "formula": "d_R := dD_R(C_R)/dC_R or declared norm of U_mu U_nu shadow-frame response",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless_or_declared_disformal_scale",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_links": "PPN_preferred_frame;clock;orbital;local_GR",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFL1879_2_wR",
            "symbol": "w_R",
            "meaning": "source-only matter prefactor derivative",
            "formula": "w_R := d ln w_A(C_R)/dC_R or absolute source-weight envelope across ordinary matter sectors",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_links": "WEP;R10_source_leg;PPN_source_normalization;clock",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFL1879_3_endpoint",
            "symbol": "epsilon_endpoint_R",
            "meaning": "boundary/endpoint local coframe projection",
            "formula": "epsilon_endpoint_R := ||P_loc partial_{Q_endpoint}E(Q_vis,Q_endpoint)||",
            "status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless_projection_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_links": "PPN;clock;orbital;local_GR",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFL1879_4_total_abs",
            "symbol": "epsilon_common_frame_abs",
            "meaning": "absolute no-cancellation common-frame leak envelope",
            "formula": "|b_R|+|d_R|+|w_R|+|epsilon_endpoint_R| plus any sourced coframe/tau/readout leaks",
            "status": "MISSING_ABSOLUTE_ENVELOPE",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_links": "all_local_arenas",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ABI1879_0_local_GR",
            "arena": "local_GR/Newton",
            "required_inputs": "epsilon_common_frame_abs=0 or source-backed bound; plus source normalization, beta, conservation",
            "current_status": "BLOCKED_NONCLAIM",
            "blocking_rows": "CFL1879_0_bR;CFL1879_1_dR;CFL1879_4_total_abs",
            "route_note": "common-frame leak must be zero/bounded before local metric inheritance is credible",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ABI1879_1_PPN",
            "arena": "PPN_gamma_beta_preferred_frame",
            "required_inputs": "b_R,d_R,q_R_hat,boundary tails and PPN projection matrix in same source frame",
            "current_status": "BLOCKED_NONCLAIM",
            "blocking_rows": "CFL1879_0_bR;CFL1879_1_dR;RV1875_5_massless_tail;RV1875_8_projection_kernels",
            "route_note": "common Weyl/disformal terms can affect gamma/beta/preferred-frame observables",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ABI1879_2_clock_WEP",
            "arena": "clock/WEP/material",
            "required_inputs": "b_R,w_R,material sensitivities, constants superselection and tau_clock/tau_WEP",
            "current_status": "BLOCKED_NONCLAIM",
            "blocking_rows": "CFL1879_0_bR;CFL1879_2_wR;RV1875_7_constants_markers;RV1875_8_projection_kernels",
            "route_note": "WEP-clean common-mode shifts can still show up in clocks/source normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ABI1879_3_orbital",
            "arena": "orbital/light-time",
            "required_inputs": "b_R,d_R,endpoint leak, orbital projection and no-cancellation envelope",
            "current_status": "BLOCKED_NONCLAIM",
            "blocking_rows": "CFL1879_0_bR;CFL1879_1_dR;CFL1879_3_endpoint;RV1875_8_projection_kernels",
            "route_note": "finite common-frame terms must be projected into acceleration/light-time residuals",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "arena_id": "ABI1879_4_R10",
            "arena": "R10 finite range",
            "required_inputs": "finite Z_R/M_R^2/lambda_R plus source/test charges; common-frame source leg cannot replace range",
            "current_status": "BLOCKED_NONCLAIM_WRONG_ROUTE_GUARD",
            "blocking_rows": "RV1875_2_operator_ZR;RV1875_3_operator_MR2_lambda;RV1875_4_bulk_source_charges;CFL1879_2_wR",
            "route_note": "b_R/w_R may be a coupling leg only after the finite range/operator branch is sourced",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1879_0_internal",
            "claim": "1879 ownership/leak audit may guide next derivation",
            "status": "ALLOW_INTERNAL_NONCLAIM_AUDIT",
            "reason": "it imports prior no-shadow tests and keeps all local claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1879_1_parent_coframe",
            "claim": "parent action owns e_obs=E(Q_vis)",
            "status": "BLOCKED",
            "reason": "parent q/coframe ownership and no C_R/J_q argument are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1879_2_no_shadow",
            "claim": "b_R=d_R=w_R=0 by no-shadow-frame theorem",
            "status": "BLOCKED",
            "reason": "covariance, WEP and Ward identities fail as unconditional derivations; terminal public metric is conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1879_3_bound_score",
            "claim": "finite common-frame leak is below local bounds",
            "status": "BLOCKED",
            "reason": "numeric leak values, units, source paths and arena projections are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1879_4_local_GR",
            "claim": "local GR/Newton follows from coframe ownership",
            "status": "BLOCKED",
            "reason": "coframe/no-shadow is necessary but still not sufficient without beta, conservation and source gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1879_0_result",
            "decision": "PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS",
            "basis": "the exact chain-rule b_R=0 theorem exists, but parent Q_vis/e_obs ownership and no C_R/J_q readout argument remain unsigned",
            "consequence": "common-frame leak rows stay live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1879_1_shortcuts",
            "decision": "COVARIANCE_WEP_WARD_SHORTCUTS_REJECTED",
            "basis": "common Weyl/disformal/source-prefactor countermodels remain covariant, can be WEP-clean, and obey Ward identities in their own matter geometry",
            "consequence": "do not use these slogans to claim no-shadow-frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1879_2_testing_interface",
            "decision": "COMMON_FRAME_LEAK_ROWS_ARE_NOW_THE_LOCAL_TEST_INTERFACE",
            "basis": "b_R,d_R,w_R,endpoint and total envelope are the finite residuals if parent ownership fails",
            "consequence": "future runners must source or theorem-zero these rows before local claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1879_3_next",
            "decision": "NO_SHADOW_TERMINAL_PUBLIC_METRIC_OR_BG_PROJECTION_SELECTED_NEXT",
            "basis": "the clean theorem target is terminal public metric/coframe; fallback is projection-ready b_R/d_R/w_R bound rows",
            "consequence": "1880 should try terminal-public-metric proof once, then build bound projection rows if it fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1879_0_primary",
            "target_doc": "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
            "target_script": "scripts/Y5_R2FR_terminal_public_coframe_no_shadow_frame_or_bg_bound_projection_1880.py",
            "objective": "try to derive a terminal public coframe/ordinary-matter domain that excludes C_R/J_q Weyl, disformal, and source-prefactor slots; if not, build projection-ready b_R/d_R/w_R bound rows.",
            "selection_status": "selected",
            "success_condition": "no-shadow theorem with parent source, or nonclaim bound projection rows for PPN/WEP/clock/orbital/R10 guards.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1879_1_later",
            "target_doc": "1880b-Y5-R2FR-source-readout-marker-boundary-qbasicity-after-coframe.md",
            "target_script": "scripts/Y5_R2FR_source_readout_marker_boundary_qbasicity_after_coframe_1880b.py",
            "objective": "after no-shadow/coframe ownership, test source/readout/marker/boundary q-basicity so C_R cannot reenter through endpoints or materials.",
            "selection_status": "held_later",
            "success_condition": "q-basic theorem or finite leak rows for source/readout/marker/boundary.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "ownership_stack": ownership_stack_rows(),
        "no_shadow_tests": no_shadow_tests_rows(),
        "leak_bound_rows": leak_bound_rows(),
        "arena_interface": arena_interface_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "proof_closed",
                "score_ready",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def missing_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values())
            if "MISSING_" in joined:
                checked += 1
                for column in ["score_ready", "valid_for_claim", "claim_allowed"]:
                    if column in row and bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true_on_missing_row"
    return checked > 0, f"checked_missing_rows={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["ownership_stack"], QUEUE / "JR1879_PARENT_COFRAME_OWNERSHIP_STACK_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["leak_bound_rows"], QUEUE / "JR1879_COMMON_FRAME_LEAK_BOUND_ROWS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1879_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1879_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1879"]) == "true" for row in sources) else "FAIL",
            "detail": "1878/1739/no-shadow/single-public-metric sources are available",
            "valid_for_claim": False,
        }
    )

    ownership = rows_by_name["ownership_stack"]
    checks.append(
        {
            "validation_id": "VAL1879_1_ownership_stack",
            "status": "PASS"
            if len(ownership) == 7
            and any(row["current_status"] == "PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS" for row in ownership)
            and all(bool_string(row["proof_closed"]) == "false" for row in ownership)
            else "FAIL",
            "detail": "parent q/coframe/no-shadow/source/boundary/tau stack is explicit and unsigned",
            "valid_for_claim": False,
        }
    )

    shadow = rows_by_name["no_shadow_tests"]
    shadow_results = {row["result"] for row in shadow}
    checks.append(
        {
            "validation_id": "VAL1879_2_no_shadow_tests",
            "status": "PASS"
            if {
                "EXACT_CONDITIONAL",
                "FAILS_UNCONDITIONAL_DERIVATION",
                "BEST_CONDITIONAL_ROUTE_NOT_PARENT_DERIVED",
                "NO_SHADOW_FRAME_NOT_DERIVED_CURRENT_CORPUS",
            }.issubset(shadow_results)
            else "FAIL",
            "detail": "no-shadow theorem is conditional and covariance/WEP/Ward shortcuts are rejected",
            "valid_for_claim": False,
        }
    )

    leak_rows = rows_by_name["leak_bound_rows"]
    checks.append(
        {
            "validation_id": "VAL1879_3_leak_rows",
            "status": "PASS"
            if len(leak_rows) == 5
            and any(row["row_id"] == "CFL1879_0_bR" for row in leak_rows)
            and any(row["row_id"] == "CFL1879_4_total_abs" for row in leak_rows)
            and all("MISSING_" in row["status"] for row in leak_rows)
            else "FAIL",
            "detail": "b_R/d_R/w_R/endpoint/total finite rows are staged as missing nonclaim rows",
            "valid_for_claim": False,
        }
    )

    arena = rows_by_name["arena_interface"]
    checks.append(
        {
            "validation_id": "VAL1879_4_arena_interface",
            "status": "PASS"
            if len(arena) == 5
            and all("BLOCKED" in row["current_status"] for row in arena)
            and any(row["arena"] == "R10 finite range" and "WRONG_ROUTE_GUARD" in row["current_status"] for row in arena)
            else "FAIL",
            "detail": "local_GR, PPN, clock/WEP, orbital and R10 interfaces stay blocked with route guards",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1879_5_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_AUDIT" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim audit is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1879_6_decision",
            "status": "PASS"
            if any(row["decision"] == "PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS" for row in decisions)
            and any(row["decision"] == "NO_SHADOW_TERMINAL_PUBLIC_METRIC_OR_BG_PROJECTION_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger records no-ownership verdict and selects terminal-public-metric/bound projection next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1879_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1879_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1880 terminal public coframe/no-shadow target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1879_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1879_9_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1879_10_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["ownership_stack"].name,
        QUARANTINE / OUTPUTS["leak_bound_rows"].name,
        QUEUE / "JR1879_PARENT_COFRAME_OWNERSHIP_STACK_NONCLAIM.csv",
        QUEUE / "JR1879_COMMON_FRAME_LEAK_BOUND_ROWS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1879_11_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1879_12_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1879*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1879_13_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1879_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1879_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1879 parent coframe ownership or common-frame leak bound",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
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


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1879 - Parent Coframe Ownership Or Common-Frame Leak Bound

**Private status:** nonclaim derivation checkpoint. No local-GR, PPN, WEP, clock, orbital, R10, or public claim is made.

## Result

The exact clean theorem is still alive:

```text
e_obs = E(Q_vis)
C_R excluded from Q_vis or killed before readout
=> D_C_R e_obs = 0
=> b_R = 0
```

But the current corpus does not parent-sign the ownership stack. The old shortcut routes also fail: covariance, WEP and Ward identities do not forbid a hidden universal Weyl/disformal/source-prefactor slot.

So the live local interface is now explicit:

```text
b_R, d_R, w_R, epsilon_endpoint_R, epsilon_common_frame_abs
```

These are not claims. They are the finite residual rows that future local PPN/WEP/clock/orbital/R10 guards must either theorem-zero or source-bound.

## Parent Coframe Ownership Stack

{markdown_table(rows_by_name["ownership_stack"])}

## No-Shadow-Frame Tests

{markdown_table(rows_by_name["no_shadow_tests"])}

## Common-Frame Leak Bound Rows

{markdown_table(rows_by_name["leak_bound_rows"])}

## Arena Bound Interface

{markdown_table(rows_by_name["arena_interface"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
