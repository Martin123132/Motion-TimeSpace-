from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1848"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1848_0_1847_next",
        "source_key": "1847_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_NEXT_TARGET.csv",
        "needles": ["NEXT1847_0_primary", "1848-Y5-R2FR-parent-metric"],
        "role": "1847 selects parent metric/eigenvalue or source-zero return.",
    },
    {
        "source_id": "SRC1848_1_1847_validation",
        "source_key": "1847_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1847_VALIDATION.csv",
        "needles": ["VAL1847_OVERALL", "PASS"],
        "role": "confirms 1847 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1848_2_1847_normalization",
        "source_key": "1847_normalization_locks",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv",
        "needles": ["FNL1847_1_canonical_metric", "CLEAN_CONTRACT_NOT_SIGNED"],
        "role": "1847 keeps the field metric/vacuum lock as unsigned target.",
    },
    {
        "source_id": "SRC1848_3_1026_metric",
        "source_key": "1026_parent_metric_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
        "needles": ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1026 supplies parent metric/eigenvalue attempt precedent.",
    },
    {
        "source_id": "SRC1848_4_1026_beta",
        "source_key": "1026_beta_eigenvalue_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1026_BETA_EIGENVALUE_ATTEMPT.csv",
        "needles": ["BE1026_4_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1026 keeps beta=3 as private target but not theorem.",
    },
    {
        "source_id": "SRC1848_5_1026_source_return",
        "source_key": "1026_source_zero_return",
        "source_path": RESIDUALS / "P8_Y5_R10_1026_SOURCE_ZERO_RETURN.csv",
        "needles": ["SZR1026_5_verdict", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
        "role": "1026 selects source-zero or bounded coupling after finite route fails.",
    },
    {
        "source_id": "SRC1848_6_1027_source_zero",
        "source_key": "1027_source_zero_proof",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1027 records the qbar_XT/J_X source-zero theorem as conditional only.",
    },
    {
        "source_id": "SRC1848_7_1027_qbar_schema",
        "source_key": "1027_bounded_qbar_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
        "needles": ["BQT1027_3_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1027 supplies bounded qbar_XT component schema.",
    },
    {
        "source_id": "SRC1848_8_1027_branch",
        "source_key": "1027_branch_verdicts",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_BRANCH_VERDICTS.csv",
        "needles": ["BV1027_3_next_target", "first_bound_input_or_marker_theorem"],
        "role": "1027 selects frame/marker coupling bound inputs or no-marker theorem after qbar zero fails.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_SOURCE_REGISTER.csv",
    "parent_metric": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_PARENT_METRIC_ATTEMPT.csv",
    "beta_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_BETA_EIGENVALUE_ATTEMPT.csv",
    "source_zero_return": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv",
    "qbar_handoff": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_QBARXT_HANDOFF_SCHEMA.csv",
    "branch_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_BRANCH_VERDICTS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1848_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def parent_metric_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_0_metric_target",
            "target": "derive parent field-space metric restricted to Xhat",
            "candidate_statement": "G_XX := M_AB e_X^A e_X^B and Z_X f_X^2 := G_XX f_X^2",
            "current_evidence": "M_AB repeatedly appears as missing parent metric, not derived object",
            "status": "TARGET_DEFINED_NOT_OWNED",
            "missing_for_claim": "parent M_AB, normalized Xhat direction e_X, field units and stress variation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_1_Ward_identity_attempt",
            "target": "derive M_AB from Ward/current norm",
            "candidate_statement": "M_AB=<J_A,J_B> or Hessian/current norm fixed by parent symmetry",
            "current_evidence": "Ward/current norm route assigns ownership but does not prove metric lock",
            "status": "WARD_ROUTE_CONDITIONAL_NOT_METRIC_LOCK",
            "missing_for_claim": "inner product, current basis, sign, units and stress variation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_2_defect_Hessian_attempt",
            "target": "derive M_AB from defect potential Hessian",
            "candidate_statement": "M_AB=partial_A partial_B V_def|_0",
            "current_evidence": "partial trace/flow support exists but full V_def and M_AB are not parent-derived",
            "status": "PARTIAL_TRACE_FLOW_SUPPORT_NOT_FULL_METRIC",
            "missing_for_claim": "full defect potential, Weyl/Q/J_rel weights, cross terms and positive metric",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_3_response_doublet_attempt",
            "target": "use even response doublets for double-zero and positive metric",
            "candidate_statement": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "current_evidence": "double-zero route is coherent only if M_AB and mapping to Xhat are parent-owned",
            "status": "DOUBLE_ZERO_CONDITIONAL_PARENT_MATCH_MISSING",
            "missing_for_claim": "map Z^A to MTS Xhat, parent-owned M_AB, boundary/domain silence and metric variation lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_4_canonical_vacuum_lock",
            "target": "lock field metric to vacuum scale",
            "candidate_statement": "Z_X f_X^2=rho_vac^(1/2)",
            "current_evidence": "clean contract retained from 1847, but not signed by parent Ward/metric theorem",
            "status": "CLEAN_CONTRACT_NOT_SIGNED",
            "missing_for_claim": "parent Ward/metric theorem equating Xhat norm to vacuum density scale",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_5_cross_block_guard",
            "target": "make scalar truncation legal",
            "candidate_statement": "Hessian block diagonalizes into Xhat plus positive orthogonal sectors or all cross terms are bounded",
            "current_evidence": "1847 mixed Xhat-sector Hessian proof is missing",
            "status": "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF",
            "missing_for_claim": "cross-Hessian matrix, eigenvectors and positive orthogonal block",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "metric_id": "PM1848_6_verdict",
            "target": "parent metric lock",
            "candidate_statement": "parent_signed(M_AB,e_X,V_def) -> Z_X f_X^2=rho_vac^(1/2)",
            "current_evidence": "no inspected active-branch source supplies all objects from one parent branch",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "M_AB, e_X, V_def/H_X, units and stress/Bianchi variation",
            "valid_for_claim": False,
        },
    ]


def beta_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "beta_id": "BE1848_0_spectral_definition",
            "target": "define beta without post-hoc fitting",
            "candidate_statement": "beta_eff is eigenvalue of H_X := rho_vac^(-1/2) G_X^(-1/2)(partial_X^2 V_eff)G_X^(-1/2)",
            "current_evidence": "beta_eff isolated as invariant target, but G_X and Hessian spectrum are unowned",
            "status": "CONDITIONAL_DEFINITION_ONLY",
            "missing_for_claim": "parent G_X, V_eff, branch spectrum and units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "beta_id": "BE1848_1_spatial_trace_beta3",
            "target": "derive U''(0)=3",
            "candidate_statement": "three equal spatial trace channels give beta=3 if Xhat is exactly normalized spatial-trace mode",
            "current_evidence": "beta=3 remains least-posthoc finite theorem target, not signed",
            "status": "BEST_TARGET_NOT_THEOREM",
            "missing_for_claim": "trace projector, isotropic eigenvalue degeneracy, no time/Weyl leakage and parent metric",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "beta_id": "BE1848_2_time_or_constraint_modes",
            "target": "reject model-chosen beta=4,5,6 promotion",
            "candidate_statement": "extra time/constraint/regular modes can shift beta only if eigenvalues are parent-owned",
            "current_evidence": "candidate mode counts exist with weaker ownership",
            "status": "CANDIDATES_DEMOTED",
            "missing_for_claim": "mode count, constraint algebra and spectral theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "beta_id": "BE1848_3_direct_backsolve",
            "target": "forbid range backsolve",
            "candidate_statement": "choose beta/lambda to hit a local bound scale after the fact",
            "current_evidence": "direct backsolve is closure-only",
            "status": "FORBIDDEN_AS_DERIVATION",
            "missing_for_claim": "independent parent spectrum reproducing number before local comparison",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "beta_id": "BE1848_4_verdict",
            "target": "beta eigenvalue ownership",
            "candidate_statement": "parent_signed(H_X spectrum) -> beta_eff, then lambda_X=ell_vac/sqrt(beta_eff)",
            "current_evidence": "no parent-signed spectrum exists in active branch",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "normalized Hessian spectrum and trace/eigenvalue theorem",
            "valid_for_claim": False,
        },
    ]


def source_zero_return_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_0_route_trigger",
            "route": "finite metric/eigenvalue route",
            "current_status": "NOT_PROMOTED",
            "because": "M_AB, e_X, Z_X f_X^2 and beta are not signed",
            "next_use": "return to source-zero/no-pole before alpha or finite-range claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_1_no_pole",
            "route": "quotient/no-pole",
            "current_status": "STILL_STRONGEST_IF_CLOSED",
            "because": "no physical X Green function would make K_X=0 instead of merely small",
            "next_use": "requires parent projection, first-class constraint and zero boundary charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_2_qbar_XT",
            "route": "matter source-zero",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "because": "qbar_XT=0 follows if matter descends through observed quotient and Lie_vX(theta_A)=0",
            "next_use": "parent-sign matter/coframe descent or write bounded qbar_XT row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_3_Qbar_XH",
            "route": "Hamiltonian/source projection zero",
            "current_status": "NOT_DERIVED",
            "because": "boundary charge and Pi_M^H projection remain open",
            "next_use": "retain Qbar_XH source row unless boundary/projector theorem closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_4_KX",
            "route": "no Green function",
            "current_status": "CONDITIONAL_ONLY",
            "because": "K_X=0 needs no physical X pole after first-class quotient and boundary audit",
            "next_use": "retain K_X row unless no-pole certificate closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "return_id": "SZR1848_5_verdict",
            "route": "next target",
            "current_status": "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW",
            "because": "finite metric/eigenvalue ownership failed current claim; coupling is the live route",
            "next_use": "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": False,
        },
    ]


def qbar_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "QBH1848_0_conditional_chain_rule",
            "object": "qbar_XT=0/J_matter_pullback=0 theorem",
            "status": "CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED",
            "required_next": "q, Obs_e, S_matter, theta_A and hidden tails parent-owned together",
            "if_missing": "retain qbar_XT as finite source/test coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "QBH1848_1_visible_geometry",
            "object": "qbar_geom",
            "status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "required_next": "prove Lie_vX observed frame zero or source c_g/b_dis bounds",
            "if_missing": "common Weyl/disformal coupling remains live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "QBH1848_2_marker_constants",
            "object": "qbar_marker",
            "status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "required_next": "prove constant/material marker triviality or source b_A/b_alpha coefficients",
            "if_missing": "composition/clock/EM marker channels remain live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "QBH1848_3_nonHilbert_tail",
            "object": "qbar_nonH",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "required_next": "prove non-Hilbert/source/domain tail zero or source q_nonH/support/domain coefficients",
            "if_missing": "hidden source-normalization tail remains live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "QBH1848_4_total_abs_guard",
            "object": "qbar_XT_bound_abs",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "required_next": "component absolute envelope with source paths, units and no-cancellation policy",
            "if_missing": "local tests cannot score qbar_XT or alpha product",
            "valid_for_claim": False,
        },
    ]


def branch_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1848_0_parent_metric",
            "branch": "M_AB / field-space metric",
            "status": "NOT_PARENT_SIGNED",
            "because": "M_AB is the right ownership target but no source derives it with Xhat direction, sign, units and stress variation",
            "allowed_statement": "M_AB/e_X is the finite-route ownership target",
            "forbidden_statement": "M_AB is already derived for MTS local Xhat",
            "next_action": "do not promote finite lambda until M_AB/e_X is signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1848_1_beta",
            "branch": "beta eigenvalue",
            "status": "NOT_PARENT_SIGNED",
            "because": "beta=3 is a clean spatial-trace target but not a spectrum theorem",
            "allowed_statement": "beta=3 remains least-posthoc finite theorem target",
            "forbidden_statement": "beta=3 or lambda_X is a prediction",
            "next_action": "reopen beta only after parent metric/spectrum source exists",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1848_2_finite_route",
            "branch": "finite R10/local route",
            "status": "DEMOTED_TO_CLOSURE_SIDECAR",
            "because": "range and amplitude remain independently choosable without one normalization ledger",
            "allowed_statement": "finite route is useful private pressure testing",
            "forbidden_statement": "finite route derives local GR",
            "next_action": "freeze finite route until source rows are real",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1848_3_source_zero_return",
            "branch": "source-zero/no-pole",
            "status": "SELECTED_NEXT",
            "because": "removing/silencing the source is cleaner GR-reduction route than tuning finite range",
            "allowed_statement": "next work attacks qbar_XT/J_X or bounded coupling rows",
            "forbidden_statement": "WEP/covariance alone proves source-zero",
            "next_action": "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_0_sources_registered",
            "claim": "1848 source chain exists",
            "gate_pass": False,
            "reason": "source chain supports audit continuity only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_1_parent_metric_lock",
            "claim": "Z_X f_X^2=rho_vac^(1/2) is parent-signed",
            "gate_pass": False,
            "reason": "M_AB/e_X/units/stress variation are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_2_beta_eigenvalue",
            "claim": "U''(0)=3 or beta_eff is parent-signed",
            "gate_pass": False,
            "reason": "no normalized Hessian spectrum theorem exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_3_finite_lambda_claim",
            "claim": "lambda_X is a finite prediction",
            "gate_pass": False,
            "reason": "metric/eigenvalue lock failed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_4_source_zero",
            "claim": "J_X/qbar_XT source-zero is parent-signed",
            "gate_pass": False,
            "reason": "matter descent/no-marker/hidden-tail clauses remain conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1848_5_local_GR_claim",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "finite route and source-zero/no-pole routes are still unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1848_0_metric_result",
            "decision": "The parent metric route remains unowned.",
            "because": "M_AB is the right object, but current corpus does not derive M_AB restricted to Xhat with units, sign and stress variation.",
            "next_action": "do not claim Z_X f_X^2 or lambda_X from finite route",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1848_1_beta_result",
            "decision": "Beta=3 survives as a private theorem target only.",
            "because": "spatial trace is the cleanest story, but not a parent spectrum theorem.",
            "next_action": "freeze beta claims until parent metric/spectrum source appears",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1848_2_finite_route",
            "decision": "The finite Hessian/local route is demoted to closure sidecar.",
            "because": "range and amplitude still lack one normalization ledger.",
            "next_action": "use finite route only as nonclaim pressure testing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1848_3_next_target",
            "decision": "Next target is qbar_XT/J_X source-zero or bounded coupling row.",
            "because": "local-GR reduction is stronger if matter source coupling vanishes by parent descent or is explicitly bounded.",
            "next_action": "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1848_0_primary",
            "next_target": "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            "script": "scripts/Y5_R2FR_qbarXT_source_zero_or_bounded_coupling_row_1849.py",
            "objective": "derive qbar_XT=0/J_X=0 from parent matter/coframe descent, or create claim-blocked bounded qbar_XT source rows with units, source paths, arena links and no-cancellation guard",
            "selection_status": "selected",
            "success_condition": "matter/coframe/no-marker/hidden-tail clauses close together, or qbar_XT component envelope is staged as nonclaim bounded residual",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1848_1_future_reopen",
            "next_target": "1849b-Y5-R2FR-parent-metric-spectrum-reopen.md",
            "script": "scripts/Y5_R2FR_parent_metric_spectrum_reopen_1849b.py",
            "objective": "reopen finite route only if a source supplies parent M_AB, e_X, Hessian spectrum and units",
            "selection_status": "held",
            "success_condition": "one parent metric/spectrum source replaces the conditional metric/eigenvalue ledger",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_metric": parent_metric_rows(),
        "beta_attempt": beta_attempt_rows(),
        "source_zero_return": source_zero_return_rows(),
        "qbar_handoff": qbar_handoff_rows(),
        "branch_verdicts": branch_verdict_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1848_{key.upper()}.csv",
        ]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1848_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1848-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1848",
        "P8_Y5_BRR545_1848",
        "Y5_R2FR_parent_metric_ZXfX2_beta_eigenvalue_or_source_zero_return_1848",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready", "pass_for_claim"]:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "score_ready", "pass_for_claim"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1848_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1848_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1848_2_parent_metric_blocks",
            any(row["metric_id"] == "PM1848_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["parent_metric"]),
            "parent metric lock remains nonclaim",
        ),
        (
            "VAL1848_3_beta_blocks",
            any(row["beta_id"] == "BE1848_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["beta_attempt"]),
            "beta eigenvalue remains nonclaim",
        ),
        (
            "VAL1848_4_source_return_selected",
            any(row["return_id"] == "SZR1848_5_verdict" and row["current_status"] == "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW" for row in rows_map["source_zero_return"]),
            "source-zero/bounded coupling route selected",
        ),
        (
            "VAL1848_5_qbar_handoff_nonclaim",
            any(row["handoff_id"] == "QBH1848_4_total_abs_guard" and row["status"] == "SCHEMA_READY_VALUES_MISSING" for row in rows_map["qbar_handoff"])
            and all(row["valid_for_claim"] is False for row in rows_map["qbar_handoff"]),
            "qbar_XT handoff schema remains nonclaim",
        ),
        (
            "VAL1848_6_branch_next_selected",
            any(row["verdict_id"] == "BV1848_3_source_zero_return" and row["status"] == "SELECTED_NEXT" for row in rows_map["branch_verdicts"]),
            "branch verdict selects qbarXT source-zero/bounded coupling next",
        ),
        (
            "VAL1848_7_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1848_8_decision_next",
            any(row["decision_id"] == "DEC1848_3_next_target" and "qbar_XT" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects qbarXT source-zero target",
        ),
        (
            "VAL1848_9_next_target_selected",
            any(row["route_id"] == "NEXT1848_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1848_10_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1848_11_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1848_12_csv_parse", csv_parse_all(), "all generated 1848 CSVs parse"),
        ("VAL1848_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1848_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1848_15_formalization_untouched", no_formalization_outputs(), "no 1848 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1848_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1848 parent metric ZXfX2 beta eigenvalue or source-zero return",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1848 Y5 R2FR parent metric ZXfX2 beta eigenvalue or source-zero return",
            "",
            "**Progress:** 1848 tries the finite scalar route one level deeper: parent field-space metric `M_AB`, normalized `Xhat` direction `e_X`, vacuum metric lock `Z_X f_X^2`, and beta/eigenvalue spectrum. This is the right way to avoid range backsolving.",
            "",
            "**Current verdict:** the parent metric and beta/eigenvalue route remains unowned. The finite range route is demoted to a private closure sidecar; the serious local-GR route now returns to `qbar_XT/J_X` source-zero or bounded coupling rows.",
            "",
            "**Claim ceiling:** no `Z_X f_X^2` lock, no beta prediction, no finite lambda claim, no alpha/product pass, no R10/PPN pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1848.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Parent Metric Attempt",
            markdown_table(rows_map["parent_metric"], ["metric_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Beta Eigenvalue Attempt",
            markdown_table(rows_map["beta_attempt"], ["beta_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Source Zero Return",
            markdown_table(rows_map["source_zero_return"], ["return_id", "route", "current_status", "because", "next_use", "valid_for_claim"]),
            "",
            "## qbar_XT Handoff Schema",
            markdown_table(rows_map["qbar_handoff"], ["handoff_id", "object", "status", "required_next", "if_missing", "valid_for_claim"]),
            "",
            "## Branch Verdicts",
            markdown_table(rows_map["branch_verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful demotion, not a retreat. The finite route is not thrown away; it is frozen until the parent metric and spectrum exist. For local GR recovery, source-zero is now cleaner: either matter sees only quotient observables and `qbar_XT` dies by theorem, or every surviving coupling becomes a scored residual component.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1848 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
