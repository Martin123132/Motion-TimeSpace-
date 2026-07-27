from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3094"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3094_00_3093_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3093_NEXT_TARGET.csv",
        "needles": ["NEXT3093_0_primary", "Z_X f_X^2=rho_vac^(1/2)"],
        "role": "3093 selects parent metric/eigenvalue or source-zero return.",
    },
    "SRC3094_01_3093_doc": {
        "path": ROOT / "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md",
        "needles": ["PARENT_METRIC_OR_SOURCE_ZERO_RETURN", "anti-knob rule"],
        "role": "3093 blocks parent Xhat/Hessian ownership and points to metric/source-zero.",
    },
    "SRC3094_02_1848_doc": {
        "path": ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
        "needles": ["parent field-space metric", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
        "role": "1848 precedent for parent metric/eigenvalue demotion and qbar return.",
    },
    "SRC3094_03_1848_metric": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_PARENT_METRIC_ATTEMPT.csv",
        "needles": ["PM1848_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1848 parent metric lock remains unowned.",
    },
    "SRC3094_04_1848_beta": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_BETA_EIGENVALUE_ATTEMPT.csv",
        "needles": ["BE1848_4_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1848 beta/eigenvalue route remains unowned.",
    },
    "SRC3094_05_1848_source_return": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv",
        "needles": ["SZR1848_5_verdict", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
        "role": "1848 selects source-zero or bounded coupling after finite route failure.",
    },
    "SRC3094_06_1848_qbar_handoff": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_QBARXT_HANDOFF_SCHEMA.csv",
        "needles": ["QBH1848_4_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1848 supplies qbar_XT component envelope handoff.",
    },
    "SRC3094_07_1026_metric": {
        "path": RESIDUALS / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
        "needles": ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1026 parent metric/eigenvalue attempt precedent.",
    },
    "SRC3094_08_1026_source_return": {
        "path": RESIDUALS / "P8_Y5_R10_1026_SOURCE_ZERO_RETURN.csv",
        "needles": ["SZR1026_5_verdict", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
        "role": "1026 source-zero return precedent.",
    },
    "SRC3094_09_1027_source_zero": {
        "path": RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1027_0_chain_rule", "CONDITIONAL_THEOREM_VALID"],
        "role": "1027 records qbar_XT/J_X source-zero theorem as conditional.",
    },
    "SRC3094_10_1027_qbar_schema": {
        "path": RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
        "needles": ["BQT1027_3_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1027 supplies bounded qbar_XT row schema.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3094_SOURCE_REGISTER.csv",
    "metric": RESIDUALS / "P8_Y5_R2FR_3094_PARENT_METRIC_ATTEMPT.csv",
    "beta": RESIDUALS / "P8_Y5_R2FR_3094_BETA_EIGENVALUE_ATTEMPT.csv",
    "source_return": RESIDUALS / "P8_Y5_R2FR_3094_SOURCE_ZERO_RETURN.csv",
    "qbar_handoff": RESIDUALS / "P8_Y5_R2FR_3094_QBARXT_HANDOFF_SCHEMA.csv",
    "verdicts": RESIDUALS / "P8_Y5_R2FR_3094_BRANCH_VERDICTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3094_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3094_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3094_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3094_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3094_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "metric_copy": LOCAL_BOUNDS / "parent_metric_attempt_3094_NONCLAIM.csv",
    "source_return_copy": LOCAL_BOUNDS / "source_zero_return_3094_NONCLAIM.csv",
    "qbar_handoff_copy": LOCAL_BOUNDS / "qbarXT_handoff_schema_3094_NONCLAIM.csv",
    "verdicts_copy": LOCAL_BOUNDS / "branch_verdicts_3094_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3094_qbarXT_source_zero_or_bounded_coupling_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def source_parse_ok(path: Path) -> bool:
    return csv_ok(path) if path.suffix.lower() == ".csv" else path.exists()


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def metric_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "metric_id": "PM3094_0_metric_target",
                "target": "derive parent field-space metric restricted to Xhat",
                "candidate_statement": "G_XX := M_AB e_X^A e_X^B and Z_X f_X^2 := G_XX f_X^2",
                "current_evidence": "M_AB repeatedly appears as the correct missing parent metric, not a derived object",
                "status": "TARGET_DEFINED_NOT_OWNED",
                "missing_for_claim": "parent M_AB, normalized Xhat direction e_X, field units and stress variation",
            },
            {
                "metric_id": "PM3094_1_Ward_identity_attempt",
                "target": "derive M_AB from Ward/current norm",
                "candidate_statement": "M_AB=<J_A,J_B> or Hessian/current norm fixed by parent symmetry",
                "current_evidence": "Ward/current norm route assigns ownership but does not prove metric lock",
                "status": "WARD_ROUTE_CONDITIONAL_NOT_METRIC_LOCK",
                "missing_for_claim": "inner product, current basis, sign, units and stress variation",
            },
            {
                "metric_id": "PM3094_2_defect_Hessian_attempt",
                "target": "derive M_AB from defect potential Hessian",
                "candidate_statement": "M_AB=partial_A partial_B V_def|_0",
                "current_evidence": "partial trace/flow support exists but full V_def and M_AB are not parent-derived",
                "status": "PARTIAL_TRACE_FLOW_SUPPORT_NOT_FULL_METRIC",
                "missing_for_claim": "full defect potential, Weyl/Q/J_rel weights, cross terms and positive metric",
            },
            {
                "metric_id": "PM3094_3_response_doublet_attempt",
                "target": "use even response doublets for double-zero and positive metric",
                "candidate_statement": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
                "current_evidence": "double-zero route is coherent only if M_AB and mapping to Xhat are parent-owned",
                "status": "DOUBLE_ZERO_CONDITIONAL_PARENT_MATCH_MISSING",
                "missing_for_claim": "map Z^A to MTS Xhat, parent-owned M_AB, boundary/domain silence and metric variation lock",
            },
            {
                "metric_id": "PM3094_4_canonical_vacuum_lock",
                "target": "lock field metric to vacuum scale",
                "candidate_statement": "Z_X f_X^2=rho_vac^(1/2)",
                "current_evidence": "clean contract retained from 3093, but not signed by parent Ward/metric theorem",
                "status": "CLEAN_CONTRACT_NOT_SIGNED",
                "missing_for_claim": "parent Ward/metric theorem equating Xhat norm to vacuum density scale",
            },
            {
                "metric_id": "PM3094_5_cross_block_guard",
                "target": "make the Xhat scalar truncation legal",
                "candidate_statement": "Hessian block either diagonalizes into Xhat plus positive orthogonal sectors or all cross terms are bounded",
                "current_evidence": "3093 PHA3093_4 says mixed Xhat-sector Hessian proof is missing",
                "status": "MISSING_CROSS_BLOCK_PROOF",
                "missing_for_claim": "block diagonalization, positive Schur complement or sourced cross-term bound",
            },
            {
                "metric_id": "PM3094_6_verdict",
                "target": "parent metric lock",
                "candidate_statement": "parent_signed(M_AB,e_X,V_def) -> Z_X f_X^2=rho_vac^(1/2)",
                "current_evidence": "no inspected active-branch source supplies all objects from one parent branch",
                "status": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "M_AB, e_X, V_def/H_X, units and stress/Bianchi variation",
            },
        ]
    )


def beta_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "beta_id": "BE3094_0_spectral_definition",
                "target": "define beta without post-hoc fitting",
                "candidate_statement": "beta_eff is eigenvalue of H_X := rho_vac^(-1/2) G_X^(-1/2)(partial_X^2 V_eff)G_X^(-1/2)",
                "current_evidence": "beta_eff isolated as invariant target, but G_X and Hessian spectrum are unowned",
                "status": "CONDITIONAL_DEFINITION_ONLY",
                "missing_for_claim": "parent G_X, V_eff, branch spectrum and units",
            },
            {
                "beta_id": "BE3094_1_spatial_trace_beta3",
                "target": "derive U''(0)=3",
                "candidate_statement": "three equal spatial trace channels give beta=3 if Xhat is exactly normalized spatial-trace mode",
                "current_evidence": "beta=3 remains least-posthoc finite theorem target, not signed",
                "status": "BEST_TARGET_NOT_THEOREM",
                "missing_for_claim": "trace projector, isotropic eigenvalue degeneracy, no time/Weyl leakage and parent metric",
            },
            {
                "beta_id": "BE3094_2_time_or_constraint_modes",
                "target": "reject model-chosen beta=4,5,6 promotion",
                "candidate_statement": "extra time/constraint/regular modes can shift beta only if eigenvalues are parent-owned",
                "current_evidence": "candidate mode counts exist with weaker ownership",
                "status": "CANDIDATES_DEMOTED",
                "missing_for_claim": "mode count, constraint algebra and spectral theorem",
            },
            {
                "beta_id": "BE3094_3_direct_backsolve",
                "target": "forbid range backsolve",
                "candidate_statement": "choose beta/lambda to hit a local bound scale after the fact",
                "current_evidence": "direct backsolve is closure-only",
                "status": "FORBIDDEN_AS_DERIVATION",
                "missing_for_claim": "independent parent spectrum reproducing number before local comparison",
            },
            {
                "beta_id": "BE3094_4_verdict",
                "target": "beta eigenvalue ownership",
                "candidate_statement": "parent_signed(H_X spectrum) -> beta_eff, then lambda_X=ell_vac/sqrt(beta_eff)",
                "current_evidence": "no parent-signed spectrum exists in active branch",
                "status": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "normalized Hessian spectrum and trace/eigenvalue theorem",
            },
        ]
    )


def source_return_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "return_id": "SZR3094_0_route_trigger",
                "route": "finite metric/eigenvalue route",
                "current_status": "NOT_PROMOTED",
                "because": "M_AB, e_X, Z_X f_X^2 and beta are not signed",
                "next_use": "return to source-zero/no-pole before alpha or finite-range claim",
            },
            {
                "return_id": "SZR3094_1_no_pole",
                "route": "quotient/no-pole",
                "current_status": "STILL_STRONGEST_IF_CLOSED",
                "because": "no physical X Green function would make K_X=0 instead of merely small",
                "next_use": "requires parent projection, first-class constraint and zero boundary charge",
            },
            {
                "return_id": "SZR3094_2_qbar_XT",
                "route": "matter source-zero",
                "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
                "because": "qbar_XT=0 follows if matter descends through observed quotient and Lie_vX(theta_A)=0",
                "next_use": "parent-sign matter/coframe descent or write bounded qbar_XT row",
            },
            {
                "return_id": "SZR3094_3_Qbar_XH",
                "route": "Hamiltonian/source projection zero",
                "current_status": "NOT_DERIVED",
                "because": "boundary charge and Pi_M^H projection remain open",
                "next_use": "retain Qbar_XH source row unless boundary/projector theorem closes",
            },
            {
                "return_id": "SZR3094_4_edge_tail",
                "route": "edge/non-Hilbert/domain tail",
                "current_status": "NOT_DERIVED_OR_BOUNDED",
                "because": "hidden/source/domain support terms can carry residual coupling",
                "next_use": "component absolute envelope with no-cancellation guard",
            },
            {
                "return_id": "SZR3094_5_verdict",
                "route": "next target",
                "current_status": "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW",
                "because": "finite metric/eigenvalue ownership failed current claim; coupling is the live route",
                "next_use": "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md",
            },
        ]
    )


def qbar_handoff_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "handoff_id": "QBH3094_0_conditional_chain_rule",
                "object": "qbar_XT=0/J_matter_pullback=0 theorem",
                "status": "CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED",
                "required_next": "q, Obs_e, S_matter, theta_A and hidden tails parent-owned together",
                "if_missing": "retain qbar_XT as finite source/test coupling",
            },
            {
                "handoff_id": "QBH3094_1_visible_geometry",
                "object": "qbar_geom",
                "status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
                "required_next": "prove Lie_vX observed frame zero or source c_g/b_dis bounds",
                "if_missing": "common Weyl/disformal coupling remains live",
            },
            {
                "handoff_id": "QBH3094_2_marker_constants",
                "object": "qbar_marker",
                "status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
                "required_next": "prove constant/material marker triviality or source b_A/b_alpha coefficients",
                "if_missing": "composition/clock/EM marker channels remain live",
            },
            {
                "handoff_id": "QBH3094_3_nonHilbert_tail",
                "object": "qbar_nonH",
                "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
                "required_next": "prove non-Hilbert/source/domain tail zero or source q_nonH/support/domain coefficients",
                "if_missing": "hidden source-normalization tail remains live",
            },
            {
                "handoff_id": "QBH3094_4_total_abs_guard",
                "object": "qbar_XT_bound_abs",
                "status": "SCHEMA_READY_VALUES_MISSING",
                "required_next": "component absolute envelope with source paths, units and no-cancellation policy",
                "if_missing": "local tests cannot score qbar_XT or alpha product",
            },
        ]
    )


def verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "verdict_id": "BV3094_0_parent_metric",
                "branch": "M_AB / field-space metric",
                "status": "NOT_PARENT_SIGNED",
                "because": "M_AB is the right ownership target but no source derives it with Xhat direction, sign, units and stress variation",
                "allowed_statement": "M_AB/e_X is the finite-route ownership target",
                "forbidden_statement": "M_AB is already derived for MTS local Xhat",
                "next_action": "do not promote finite lambda until M_AB/e_X is signed",
            },
            {
                "verdict_id": "BV3094_1_beta",
                "branch": "beta eigenvalue",
                "status": "NOT_PARENT_SIGNED",
                "because": "beta=3 is a clean spatial-trace target but not a spectrum theorem",
                "allowed_statement": "beta=3 remains least-posthoc finite theorem target",
                "forbidden_statement": "beta=3 or lambda_X is a prediction",
                "next_action": "reopen beta only after parent metric/spectrum source exists",
            },
            {
                "verdict_id": "BV3094_2_finite_route",
                "branch": "finite scalar range route",
                "status": "FROZEN_AS_CLOSURE_SIDECAR",
                "because": "range/eigenvalue ownership failed current claim",
                "allowed_statement": "finite route remains a private theorem target",
                "forbidden_statement": "finite range supports local-GR or R10 pass",
                "next_action": "do not run claim comparisons until metric/spectrum owner exists",
            },
            {
                "verdict_id": "BV3094_3_source_zero_return",
                "branch": "source-zero/no-pole",
                "status": "SELECTED_NEXT",
                "because": "removing/silencing the source is cleaner GR-reduction route than tuning finite range",
                "allowed_statement": "next work attacks qbar_XT/J_X or bounded coupling rows",
                "forbidden_statement": "WEP/covariance alone proves source-zero",
                "next_action": "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md",
            },
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3094_0_sources_registered", "3094 source chain exists", "source chain supports audit continuity only"),
        ("CG3094_1_parent_metric_lock", "Z_X f_X^2=rho_vac^(1/2) is parent-signed", "M_AB/e_X/units/stress variation are missing"),
        ("CG3094_2_beta_eigenvalue", "U''(0)=3 or beta_eff is parent-signed", "no normalized Hessian spectrum theorem exists"),
        ("CG3094_3_finite_lambda_claim", "lambda_X is a finite prediction", "metric/eigenvalue lock failed"),
        ("CG3094_4_source_zero", "J_X/qbar_XT source-zero is parent-signed", "matter descent/no-marker/hidden-tail clauses remain conditional"),
        ("CG3094_5_qbar_bound_claim", "bounded qbar_XT row is score-ready", "component values and source paths are missing"),
        ("CG3094_6_local_GR_claim", "local GR/Newton reduction is derived", "finite route and source-zero/no-pole routes are still unsigned"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "reason": reason,
                "claim_allowed": False,
                "claim_allowed_for_physics": False,
            }
            for gate_id, claim, reason in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3094_0_metric_result",
                "decision": "The parent metric route remains unowned.",
                "because": "M_AB is the right object, but current corpus does not derive M_AB restricted to Xhat with units, sign and stress variation",
                "next_action": "do not claim Z_X f_X^2 or lambda_X from finite route",
            },
            {
                "decision_id": "DEC3094_1_beta_result",
                "decision": "Beta=3 survives as a private theorem target only.",
                "because": "spatial trace is the cleanest story, but not a parent spectrum theorem",
                "next_action": "freeze beta claims until parent metric/spectrum source appears",
            },
            {
                "decision_id": "DEC3094_2_finite_route",
                "decision": "Finite lambda route is demoted to closure sidecar.",
                "because": "range can be meaningful only after parent metric/eigenvalue ownership",
                "next_action": "do not use local bounds as derivation for lambda",
            },
            {
                "decision_id": "DEC3094_3_next_target",
                "decision": "Next target is qbar_XT/J_X source-zero or bounded coupling row.",
                "because": "local-GR reduction is stronger if matter source coupling vanishes by parent descent or is explicitly bounded",
                "next_action": "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3094_0_primary",
                "next_checkpoint": "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md",
                "script": "scripts/Y5_R2FR_qbarXT_source_zero_or_bounded_coupling_row_under_AX1090_3095.py",
                "objective": "derive qbar_XT=0/J_X=0 from parent matter/coframe descent, or create claim-blocked bounded qbar_XT source rows with units, source paths, arena links and no-cancellation guard",
                "selection_status": "selected",
                "success_condition": "matter/coframe/no-marker/hidden-tail clauses close together, or qbar_XT component envelope is staged as nonclaim bounded residual",
            },
            {
                "route_id": "NEXT3094_1_future_reopen",
                "next_checkpoint": "3095b-Y5-R2FR-parent-metric-spectrum-reopen-under-AX1090.md",
                "script": "scripts/Y5_R2FR_parent_metric_spectrum_reopen_under_AX1090_3095b.py",
                "objective": "reopen finite route only if a source supplies parent M_AB, e_X, Hessian spectrum and units",
                "selection_status": "held",
                "success_condition": "one parent metric/spectrum source replaces the conditional metric/eigenvalue ledger",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "metric_copy": OUTPUTS["metric"],
        "source_return_copy": OUTPUTS["source_return"],
        "qbar_handoff_copy": OUTPUTS["qbar_handoff"],
        "verdicts_copy": OUTPUTS["verdicts"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3094_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3094 Y5 R2FR parent metric ZXfX2 beta eigenvalue or source-zero return under AX1090",
        "",
        "**Progress:** 3094 tries the finite scalar route one level deeper: parent field-space metric `M_AB`, normalized `Xhat` direction `e_X`, vacuum metric lock `Z_X f_X^2`, and beta/eigenvalue spectrum. This is the right way to avoid range backsolving.",
        "",
        "**Current verdict:** the parent metric and beta/eigenvalue route remains unowned. The finite range route is frozen as a private closure sidecar; the serious local-GR route now returns to `qbar_XT/J_X` source-zero or bounded coupling rows.",
        "",
        "**Claim ceiling:** no `Z_X f_X^2` lock, beta prediction, finite lambda claim, alpha/product pass, R10/R11 pass, WEP/PPN/clock/orbital pass, local-GR/Newton reduction, GitHub action, or `formalization-workbench` edit is allowed from 3094.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## Parent Metric Attempt",
        markdown_table(data["metric"], ["metric_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Beta Eigenvalue Attempt",
        markdown_table(data["beta"], ["beta_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Source-Zero Return",
        markdown_table(data["source_return"], ["return_id", "route", "current_status", "because", "next_use", "valid_for_claim"]),
        "",
        "## qbar_XT Handoff Schema",
        markdown_table(data["qbar_handoff"], ["handoff_id", "object", "status", "required_next", "if_missing", "valid_for_claim"]),
        "",
        "## Branch Verdicts",
        markdown_table(data["verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
        "## Working Interpretation",
        "This is a useful demotion, not a retreat. The finite route is not thrown away; it is frozen until the parent metric and spectrum exist. For local GR recovery, source-zero is cleaner: either matter sees only quotient observables and `qbar_XT` dies by theorem, or every surviving coupling becomes a scored residual component.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def validation_rows() -> list[dict[str, Any]]:
    formalization_3094 = list(FORMALIZATION.rglob("*3094*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3094_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3094_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3094_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3094_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3094_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3094_05_metric_parse", csv_ok(OUTPUTS["metric"]), "parent metric attempt parses", OUTPUTS["metric"]),
        ("VAL3094_06_metric_blocks", contains_status(OUTPUTS["metric"], "status", "FAIL_CURRENT_CLAIM"), "parent metric lock remains nonclaim", OUTPUTS["metric"]),
        ("VAL3094_07_beta_parse", csv_ok(OUTPUTS["beta"]), "beta eigenvalue attempt parses", OUTPUTS["beta"]),
        ("VAL3094_08_beta_blocks", contains_status(OUTPUTS["beta"], "status", "FAIL_CURRENT_CLAIM"), "beta eigenvalue remains nonclaim", OUTPUTS["beta"]),
        ("VAL3094_09_source_return_parse", csv_ok(OUTPUTS["source_return"]), "source-zero return parses", OUTPUTS["source_return"]),
        ("VAL3094_10_source_return_selected", contains_status(OUTPUTS["source_return"], "current_status", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"), "source-zero/bounded coupling route selected", OUTPUTS["source_return"]),
        ("VAL3094_11_qbar_handoff_parse", csv_ok(OUTPUTS["qbar_handoff"]), "qbar handoff schema parses", OUTPUTS["qbar_handoff"]),
        ("VAL3094_12_qbar_handoff_nonclaim", contains_status(OUTPUTS["qbar_handoff"], "status", "SCHEMA_READY_VALUES_MISSING") and all_false(OUTPUTS["qbar_handoff"], "valid_for_claim"), "qbar_XT handoff schema remains nonclaim", OUTPUTS["qbar_handoff"]),
        ("VAL3094_13_verdicts_parse", csv_ok(OUTPUTS["verdicts"]), "branch verdicts parse", OUTPUTS["verdicts"]),
        ("VAL3094_14_verdict_next", contains_status(OUTPUTS["verdicts"], "status", "SELECTED_NEXT"), "branch verdict selects qbarXT source-zero/bounded coupling next", OUTPUTS["verdicts"]),
        ("VAL3094_15_gates_parse", csv_ok(OUTPUTS["gates"]), "claim gates parse", OUTPUTS["gates"]),
        ("VAL3094_16_gates_blocked", all_false(OUTPUTS["gates"], "claim_allowed_for_physics"), "all claim gates remain blocked", OUTPUTS["gates"]),
        ("VAL3094_17_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3094_18_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3094_19_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3094_20_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3094_21_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3094_22_no_formalization_edit", len(formalization_3094) == 0, "no 3094 files created under formalization-workbench", FORMALIZATION),
        ("VAL3094_23_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "metric": metric_rows(),
        "beta": beta_rows(),
        "source_return": source_return_rows(),
        "qbar_handoff": qbar_handoff_rows(),
        "verdicts": verdict_rows(),
        "gates": gate_rows(),
        "decisions": decision_rows(),
        "next": next_rows(),
    }

    for key, output_rows in data.items():
        write_csv(OUTPUTS[key], output_rows)

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3094 parent metric/source-zero checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
