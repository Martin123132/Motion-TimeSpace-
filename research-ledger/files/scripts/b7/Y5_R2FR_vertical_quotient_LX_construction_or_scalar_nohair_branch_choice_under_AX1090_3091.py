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

CHECKPOINT = "3091"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3091-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice-under-AX1090.md"

SOURCES = {
    "SRC3091_00_3090_doc": {
        "path": ROOT / "3090-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-under-AX1090.md",
        "needles": ["vertical quotient route", "scalar positive no-hair"],
        "role": "3090 selects vertical quotient first and scalar no-hair as fallback.",
    },
    "SRC3091_01_3090_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3090_NEXT_TARGET.csv",
        "needles": ["NEXT3090_0_3091", "q(Phi+epsilon v_X)=q(Phi)"],
        "role": "3090 handoff names this vertical quotient / scalar branch target.",
    },
    "SRC3091_02_3090_branch": {
        "path": RESIDUALS / "P8_Y5_R2FR_3090_BRANCH_SEPARATION.csv",
        "needles": ["BRS3090_0_vertical_quotient", "BRS3090_2_scalar_nohair"],
        "role": "3090 branch separation guardrail.",
    },
    "SRC3091_03_1845_precedent": {
        "path": ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["q/v_X/action descent certificate does not close", "scalar no-hair input pack"],
        "role": "1845 precedent tests the active parent-q_loc quotient certificate.",
    },
    "SRC3091_04_1022_vertical": {
        "path": RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
        "needles": ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"],
        "role": "1022 vertical quotient construction clauses.",
    },
    "SRC3091_05_1022_scalar": {
        "path": RESIDUALS / "P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv",
        "needles": ["SNH1022_6_verdict", "fallback_not_next_best"],
        "role": "1022 scalar no-hair fallback construction.",
    },
    "SRC3091_06_1023_qvx": {
        "path": RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv",
        "needles": ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"],
        "role": "1023 q/v_X/action/matter/boundary/degree certificate.",
    },
    "SRC3091_07_1023_coupling": {
        "path": RESIDUALS / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "needles": ["CDA1023_4_verdict", "coupling_not_theorem_zero"],
        "role": "1023 coupling descent audit.",
    },
    "SRC3091_08_1023_scalar_inputs": {
        "path": RESIDUALS / "P8_Y5_R10_1023_SCALAR_SOURCE_INPUT_PACK.csv",
        "needles": ["SNH1023_0_Z_X", "MISSING_PARENT_INPUT"],
        "role": "1023 scalar/source input pack.",
    },
    "SRC3091_09_1023_next": {
        "path": RESIDUALS / "P8_Y5_R10_1023_NEXT_TARGET.csv",
        "needles": ["scalar-nohair-input-pack", "residual-alpha-coefficient-runner"],
        "role": "1023 selects scalar no-hair input pack or residual alpha runner.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3091_SOURCE_REGISTER.csv",
    "branch_matrix": RESIDUALS / "P8_Y5_R2FR_3091_BRANCH_DECISION_MATRIX.csv",
    "qvx_certificate": RESIDUALS / "P8_Y5_R2FR_3091_QVX_CERTIFICATE.csv",
    "coupling_audit": RESIDUALS / "P8_Y5_R2FR_3091_COUPLING_DESCENT_AUDIT.csv",
    "scalar_pack": RESIDUALS / "P8_Y5_R2FR_3091_SCALAR_SOURCE_INPUT_PACK.csv",
    "fallback_rows": RESIDUALS / "P8_Y5_R2FR_3091_FALLBACK_SOURCE_ROWS.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_3091_DEMOTION_LEDGER.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_3091_GR_BRIDGE_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3091_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3091_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3091_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3091_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3091_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qvx_copy": LOCAL_BOUNDS / "qvx_certificate_3091_NONCLAIM.csv",
    "coupling_copy": LOCAL_BOUNDS / "coupling_descent_audit_3091_NONCLAIM.csv",
    "scalar_pack_copy": LOCAL_BOUNDS / "scalar_source_input_pack_3091_NONCLAIM.csv",
    "bridge_copy": LOCAL_BOUNDS / "GR_bridge_status_3091_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3091_scalar_nohair_or_residual_alpha_NEXT_NONCLAIM.csv",
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


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


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


def branch_matrix_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "matrix_id": "BDM3091_0_vertical_quotient",
                "candidate": "quotient/vertical removal before variation",
                "core_test": "q, v_X, action descent, matter descent, boundary silence and degree count close together",
                "scrutiny_level": "least_post_hoc_if_successful",
                "current_status": "TESTED_NOT_CLOSED",
                "missing": "single parent certificate for field-by-field vertical action and descended matter/boundary terms",
                "decision": "demote current local branch; keep quotient route as future parent-action theorem target",
            },
            {
                "matrix_id": "BDM3091_1_scalar_nohair",
                "candidate": "positive scalar no-hair/source-free local silence",
                "core_test": "Z_X>0, M_X^2>=0, J_X=0 and boundary_flux_X=0 imply X=0 in compact exterior",
                "scrutiny_level": "honest_fallback_if_coefficients_are_real",
                "current_status": "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM",
                "missing": "Z_X, M_X2, J_X, boundary flux and lambda_X source rows",
                "decision": "attempt next because it is executable after quotient certificate failure",
            },
            {
                "matrix_id": "BDM3091_2_finite_residual",
                "candidate": "bounded residual coupling/source branch",
                "core_test": "K_X, Qbar_XH, qbar_XT, EDGEBOUND, FB5540 and R11 rows form no-cancellation envelope",
                "scrutiny_level": "empirical_score_route",
                "current_status": "FALLBACK_IF_NOHAIR_FAILS",
                "missing": "source-backed coefficient rows and local arena projection",
                "decision": "score residual instead of asserting local silence",
            },
        ]
    )


def qvx_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "certificate_id": "QVC3091_0_parent_q",
                "required_object": "parent quotient map q",
                "pass_condition": "q is canonical parent reduction, not post-readout projection; Dq[v_X]=0 for actual local X direction",
                "current_evidence": "conditional q pieces exist if v_X is in the parent null distribution",
                "current_status": "PARTIAL_CONDITIONAL",
                "missing_for_claim": "prove actual local Xhat variations equal the null/relative-exact generator",
                "claim_effect_if_signed": "X is representative data, not a physical local field",
            },
            {
                "certificate_id": "QVC3091_1_NX_integrability",
                "required_object": "integrable null distribution N_X",
                "pass_condition": "N_X is parent-owned, invariant under parent symmetries and integrable on compact local domain",
                "current_evidence": "construction condition is stated conditionally in prior quotient files",
                "current_status": "NOT_PARENT_SIGNED",
                "missing_for_claim": "field-space distribution and global/domain admissibility",
                "claim_effect_if_signed": "q fibres are legitimate representative orbits",
            },
            {
                "certificate_id": "QVC3091_2_action_descent",
                "required_object": "parent action descent",
                "pass_condition": "S_parent[Phi]=S_red[q(Phi)]+fixed boundary/topological terms before variation",
                "current_evidence": "conditional theorem retains boundary/domain terms",
                "current_status": "CONDITIONAL_ONLY",
                "missing_for_claim": "explicit parent Lagrangian and proof retained boundary/domain terms are silent",
                "claim_effect_if_signed": "no independent X Hessian, Green function or K_X",
            },
            {
                "certificate_id": "QVC3091_3_matter_descent",
                "required_object": "ordinary matter quotient functor",
                "pass_condition": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and L_vX theta_A=0 for constants/material markers",
                "current_evidence": "chain rule is math-pass for metric/frame part only",
                "current_status": "CONDITIONAL_THEOREM_ONLY",
                "missing_for_claim": "no-marker constants, EM/material labels and hidden conformal/disformal channel exclusion",
                "claim_effect_if_signed": "qbar_XT=0 and no ordinary matter X source",
            },
            {
                "certificate_id": "QVC3091_4_vertical_action",
                "required_object": "field-by-field v_X",
                "pass_condition": "v_X specified on metric/coframe, canonical data, memory/projector/domain, matter readout and boundary fields",
                "current_evidence": "candidate maps exist only as partial route language",
                "current_status": "MISSING",
                "missing_for_claim": "actual MTS parent transformation law on every field class",
                "claim_effect_if_signed": "DCdagger/Omega-flat map becomes a calculation",
            },
            {
                "certificate_id": "QVC3091_5_momentum_map",
                "required_object": "differentiable first-class generator",
                "pass_condition": "delta G_X=Omega(delta Phi,v_X), G_X=int epsilon C_X+Q_X, bracket closes with no active K_boundary",
                "current_evidence": "theta/Omega/DC_X/Q_X and edge differentiability remain unsigned",
                "current_status": "NOT_DERIVED",
                "missing_for_claim": "parent symplectic potential, DC_X, Q_X differentiability and algebra closure",
                "claim_effect_if_signed": "X is constraint/gauge, not physical source field",
            },
            {
                "certificate_id": "QVC3091_6_boundary_silence",
                "required_object": "local boundary/edge silence",
                "pass_condition": "Q_X=0/proper/exact and Pi_M^H[Q_X]=0 with no edge cocycle on compact branch",
                "current_evidence": "B_X primitive and projector orthogonality remain unsigned",
                "current_status": "BLOCKED",
                "missing_for_claim": "B_X primitive, weighted-Stokes zero/bound, projector orthogonality and cocycle",
                "claim_effect_if_signed": "Qbar_XH=0 and no edge alpha branch",
            },
            {
                "certificate_id": "QVC3091_7_degree_count",
                "required_object": "constraint rank and reduced nondegeneracy",
                "pass_condition": "primary+secondary first-class pair removes X pair; reduced Omega has no proper X stabilizer",
                "current_evidence": "rank calculation required but not computed",
                "current_status": "NOT_CHECKED",
                "missing_for_claim": "rank calculation, no-stabilizer theorem and reduced phase-space proof",
                "claim_effect_if_signed": "zero Hessian becomes gauge evidence rather than under-specified dynamics",
            },
            {
                "certificate_id": "QVC3091_8_verdict",
                "required_object": "single q/v_X/action descent certificate",
                "pass_condition": "QVC3091_0 through QVC3091_7 all parent-signed together",
                "current_evidence": "conditional pieces exist, but no single parent certificate closes",
                "current_status": "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH",
                "missing_for_claim": "q, v_X, action, matter, boundary and degree certificates in one source-backed row",
                "claim_effect_if_signed": "K_X=qbar_XT=Qbar_XH=0 and local X alpha inactive",
            },
        ]
    )


def coupling_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "audit_id": "CDA3091_0_metric_chain_rule",
                "object": "metric/coframe matter variation",
                "result": "CONDITIONAL_MATH_PASS",
                "reason": "DObs(Dq[v_X])=0 kills metric/frame pullback only if v_X is truly vertical",
                "remaining_coupling": "none from metric/frame channel if q/v_X closes",
                "demotion_effect": "if q/v_X fails, retain qbar_XT rows",
            },
            {
                "audit_id": "CDA3091_1_constants_markers",
                "object": "theta_A constants/material labels",
                "result": "NOT_CLOSED",
                "reason": "L_vX theta_A is not parent-owned for EM, clocks, masses or material labels",
                "remaining_coupling": "constant/material marker X-dependence",
                "demotion_effect": "retain clock/EM/WEP/source rows",
            },
            {
                "audit_id": "CDA3091_2_hidden_frame",
                "object": "hidden conformal/disformal X channel",
                "result": "COUNTEREXAMPLE_FILTER_ONLY",
                "reason": "hidden X-frame dependence is observable unless it factors through q or is finite-coupled",
                "remaining_coupling": "F_X prime or disformal coefficient if present",
                "demotion_effect": "source/coefficient pack required",
            },
            {
                "audit_id": "CDA3091_3_projector_boundary",
                "object": "projector/boundary coupling",
                "result": "OPEN",
                "reason": "B_X, Pi_M^H[Q_edge], K_boundary and source split remain unsigned",
                "remaining_coupling": "edge/source projection into measured Hamiltonian mass",
                "demotion_effect": "retain EDGEBOUND and Qbar_edge rows",
            },
            {
                "audit_id": "CDA3091_4_verdict",
                "object": "coupling descent verdict",
                "result": "COUPLING_NOT_THEOREM_ZERO",
                "reason": "matter descent and boundary/projector descent are conditional, not parent-signed",
                "remaining_coupling": "qbar_XT;Qbar_XH;edge terms;clock/WEP channels",
                "demotion_effect": "move to scalar no-hair/source coefficient input pack",
            },
        ]
    )


def scalar_pack_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"input_id": "SNH3091_0_Z_X", "quantity": "Z_X", "needed_for": "positive kinetic term", "required_source": "parent Hessian second variation with field units", "current_status": "MISSING_PARENT_INPUT", "if_missing": "no scalar no-hair theorem; score residual"},
            {"input_id": "SNH3091_1_M_X2", "quantity": "M_X^2", "needed_for": "positive mass gap and lambda_X", "required_source": "parent Hessian curvature/range derivation with units", "current_status": "MISSING_PARENT_INPUT", "if_missing": "zero/long-range/tachyonic mode remains possible"},
            {"input_id": "SNH3091_2_J_X_zero", "quantity": "J_X=0", "needed_for": "source-free exterior equation", "required_source": "matter/hidden/source variation proof or sourced current bound", "current_status": "MISSING_SOURCE_ZERO_PROOF", "if_missing": "qbar_XT/source coupling row required"},
            {"input_id": "SNH3091_3_boundary_flux_zero", "quantity": "boundary_flux_X=0", "needed_for": "positive energy identity conclusion", "required_source": "boundary class/no-hair/projector silence or flux bound", "current_status": "MISSING_BOUNDARY_LOCK", "if_missing": "EDGEBOUND and Qbar_edge rows remain live"},
            {"input_id": "SNH3091_4_lambda_X", "quantity": "lambda_X", "needed_for": "R10/R11 range if scalar no-hair fails", "required_source": "sqrt(Z_X/M_X^2) with units", "current_status": "MISSING_RANGE", "if_missing": "no local alpha row can score"},
            {"input_id": "SNH3091_5_alpha_coefficients", "quantity": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda)", "needed_for": "residual scoring if no-hair fails", "required_source": "source-normalized coefficient rows with units and no-cancellation envelope", "current_status": "MISSING_ARENA_PROJECTION", "if_missing": "no local empirical pass"},
        ]
    )


def fallback_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"row_id": "FBR3091_0_quotient_certificate", "quantity": "q_vX_action_matter_boundary_certificate", "required_columns": "q_id;vX_id;action_descent;matter_descent;boundary_silence;degree_count;source_path;valid_for_claim", "current_status": "MISSING_CERTIFICATE", "used_if": "quotient/vertical route is reopened"},
            {"row_id": "FBR3091_1_scalar_operator_pack", "quantity": "Z_X;M_X2;J_X;boundary_flux_X;lambda_X", "required_columns": "system_id;Z_X;M_X2;J_X;boundary_flux_X;lambda_X;units;source_path;valid_for_claim", "current_status": "MISSING_PARENT_INPUT", "used_if": "scalar no-hair route selected next"},
            {"row_id": "FBR3091_2_sourced_alpha_pack", "quantity": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda)", "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X;units;source_path;valid_for_claim", "current_status": "MISSING_ARENA_PROJECTION", "used_if": "scalar/source route remains nonzero"},
            {"row_id": "FBR3091_3_edge_bound_pack", "quantity": "EDGEBOUND terms", "required_columns": "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim", "current_status": "MISSING_EDGE_BOUND_TERMS", "used_if": "boundary/edge charge route remains live"},
            {"row_id": "FBR3091_4_total_guard", "quantity": "absolute no-cancellation local residual envelope", "required_columns": "abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_R11;component_sum_abs;bound_curve;valid_for_claim", "current_status": "NOT_COMPUTED_COMPONENTS_MISSING", "used_if": "any theorem-zero branch fails"},
        ]
    )


def demotion_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "demotion_id": "DEM3091_0_scope",
                "demoted_object": "current quotient/vertical no-pole route",
                "demotion": "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS",
                "reason": "single certificate fails at field-by-field v_X, action descent, matter/no-marker descent, boundary silence and degree count",
                "what_survives": "conditional theorem target for a future parent action",
            },
            {
                "demotion_id": "DEM3091_1_scalar_operator",
                "demoted_object": "scalar no-hair fallback",
                "demotion": "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM",
                "reason": "it is the honest executable branch after quotient certificate failure",
                "what_survives": "positive energy identity if Z_X, M_X2, J_X and boundary flux are sourced",
            },
            {
                "demotion_id": "DEM3091_2_sourced_residual",
                "demoted_object": "finite coupling/source branch",
                "demotion": "RETAINED_AS_SCOREABLE_IF_SCALAR_NOHAIR_FAILS",
                "reason": "nonzero J_X or matter coupling must be tested rather than hidden",
                "what_survives": "R10/R11 alpha/source-bound runner",
            },
            {
                "demotion_id": "DEM3091_3_claim_ceiling",
                "demoted_object": "local-GR/R10/R11 local silence",
                "demotion": "BLOCKED",
                "reason": "no theorem-zero branch or valid source-bound branch closes",
                "what_survives": "discipline: no public/local claim from this branch yet",
            },
        ]
    )


def bridge_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"status_id": "GB3091_0_quotient_no_pole", "bridge_piece": "remove local X before variation", "current_status": "CERTIFICATE_FAILS_CURRENT_BRANCH", "evidence": "QVC3091_8", "remaining_gap": "single parent q/v_X/action/matter/boundary/degree certificate", "bridge_claim": False},
            {"status_id": "GB3091_1_coupling_zero", "bridge_piece": "matter and boundary coupling zero", "current_status": "NOT_THEOREM_ZERO", "evidence": "CDA3091_4", "remaining_gap": "constants/material markers, hidden frames, projector and boundary silence", "bridge_claim": False},
            {"status_id": "GB3091_2_scalar_nohair", "bridge_piece": "positive scalar no-hair fallback", "current_status": "NEXT_INPUT_TARGET_NOT_CLAIM", "evidence": "SNH3091 rows", "remaining_gap": "Z_X, M_X2, J_X, boundary_flux_X, lambda_X and alpha rows", "bridge_claim": False},
            {"status_id": "GB3091_3_local_GR_Newton", "bridge_piece": "derived local GR/Newton reduction", "current_status": "BLOCKED", "evidence": "DEM3091_3", "remaining_gap": "no quotient no-pole theorem and no scalar no-hair theorem", "bridge_claim": False},
            {"status_id": "GB3091_4_next", "bridge_piece": "next derivation owner", "current_status": "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT", "evidence": "DEC3091_3;NEXT3091_0", "remaining_gap": "try positive energy/no-hair with real inputs; otherwise score residual", "bridge_claim": False},
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"gate_id": "CG3091_0_sources_registered", "claim": "3091 source chain exists", "gate_pass": True, "reason": "sources prove audit continuity only, not quotient closure", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_1_q_vX_certificate", "claim": "q/v_X/action certificate closes", "gate_pass": False, "reason": "single certificate fails at multiple required clauses", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_2_coupling_zero", "claim": "matter/coupling descent theorem-zero", "gate_pass": False, "reason": "constants/markers, hidden frame and boundary/projector coupling remain open", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_3_scalar_nohair_claim", "claim": "scalar no-hair theorem", "gate_pass": False, "reason": "Z_X, M_X2, J_X=0 and boundary_flux_X=0 remain missing", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_4_residual_score_claim", "claim": "finite residual score", "gate_pass": False, "reason": "alpha/source coefficient rows are missing", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_5_demotion_written", "claim": "current quotient route demoted", "gate_pass": True, "reason": "current MTS keeps quotient route conditional and moves executable work to scalar/source inputs", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_6_local_GR_Newton", "claim": "local GR/Newton reduction", "gate_pass": False, "reason": "no local branch closes theorem-zero or source-bound pass", "claim_allowed_for_physics": False},
            {"gate_id": "CG3091_7_guardrail", "claim": "no fake quotient credit", "gate_pass": True, "reason": "post-readout quotient and scalar-as-edge-proof are forbidden", "claim_allowed_for_physics": False},
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"decision_id": "DEC3091_0_certificate_result", "decision": "QVX_ACTION_DESCENT_CERTIFICATE_DOES_NOT_CLOSE", "reason": "conditional q-map pieces exist but no field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence or degree count is signed", "next_action": "do not spend no-pole credit from quotient route"},
            {"decision_id": "DEC3091_1_demotion", "decision": "DEMOTE_CURRENT_LOCAL_BRANCH_TO_SCALAR_NOHAIR_SOURCE_COEFFICIENT_WORK", "reason": "this is the honest executable route after quotient certificate failure in current files", "next_action": "fill scalar positive operator/source/boundary inputs before testing"},
            {"decision_id": "DEC3091_2_future_reopen", "decision": "QUOTIENT_ROUTE_REOPENS_ONLY_WITH_REAL_PARENT_CERTIFICATE", "reason": "future q/v_X proof remains the cleanest local-GR route if all missing clauses arrive together", "next_action": "require q, v_X, action descent, matter descent, boundary silence and degree count in one source-backed row"},
            {"decision_id": "DEC3091_3_next_target", "decision": "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT", "reason": "Z_X, M_X2, J_X=0, boundary_flux_X=0 and alpha coefficients are now the executable local branch inputs", "next_action": "3092-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner-under-AX1090.md"},
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "next_id": "NEXT3091_0_3092",
                "next_checkpoint": "3092-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner-under-AX1090.md",
                "script": "scripts/Y5_R2FR_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner_under_AX1090_3092.py",
                "mission": "fill or reject the scalar no-hair input pack: Z_X, M_X^2, J_X=0, boundary_flux_X=0, lambda_X and fallback alpha coefficients with units and source paths",
                "starting_equation": "int_A(Z_X|grad X|^2+M_X^2X^2)=int_A XJ_X+boundary_flux_X; if not zero, alpha_X(lambda)=K_X Qbar_XH qbar_XT",
                "claim_policy": "no scalar no-hair, residual alpha pass, R10/R11, PPN, clock, orbital, Newton or local-GR claim unless inputs are theorem-zero or source-backed with no-cancellation guard",
            }
        ]
    )


def branch_copy_rows() -> list[dict[str, Any]]:
    mapping = {
        "BR3091_0_qvx": (OUTPUTS["qvx_certificate"], BRANCH_OUTPUTS["qvx_copy"]),
        "BR3091_1_coupling": (OUTPUTS["coupling_audit"], BRANCH_OUTPUTS["coupling_copy"]),
        "BR3091_2_scalar_pack": (OUTPUTS["scalar_pack"], BRANCH_OUTPUTS["scalar_pack_copy"]),
        "BR3091_3_bridge": (OUTPUTS["bridge"], BRANCH_OUTPUTS["bridge_copy"]),
        "BR3091_4_next": (OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    }
    return with_meta(
        [
            {"copy_id": copy_id, "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False}
            for copy_id, (source, destination) in mapping.items()
        ]
    )


def table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in output_rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    branch_matrix: list[dict[str, Any]],
    qvx: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    scalar_pack: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 3091 - Vertical Quotient L_X Construction or Scalar Nohair Branch Choice

Status: `Y5_R2FR_3091_qvx_certificate_fails_scalar_inputs_next`

## Verdict

The single `q/v_X/action` certificate still does not close for current MTS. Conditional quotient pieces exist, but the field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence, and degree count are not parent-signed together.

That means the cleanest theoretical route remains a future target, but current executable work must move to the scalar no-hair/source-coefficient branch. This is a demotion of claim strength, not a death sentence: it prevents fake quotient credit and forces the local branch into theorem-zero inputs or measurable residual coefficients.

## Source Register

{table(sources, ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"])}

## Branch Decision Matrix

{table(branch_matrix, ["matrix_id", "candidate", "core_test", "scrutiny_level", "current_status", "missing", "decision"])}

## q/v_X Certificate

{table(qvx, ["certificate_id", "required_object", "pass_condition", "current_status", "missing_for_claim", "claim_effect_if_signed"])}

## Coupling Descent Audit

{table(coupling, ["audit_id", "object", "result", "reason", "remaining_coupling", "demotion_effect"])}

## Scalar/Source Input Pack

{table(scalar_pack, ["input_id", "quantity", "needed_for", "required_source", "current_status", "if_missing"])}

## Fallback Source Rows

{table(fallback, ["row_id", "quantity", "required_columns", "current_status", "used_if"])}

## Demotion Ledger

{table(demotion, ["demotion_id", "demoted_object", "demotion", "reason", "what_survives"])}

## GR Bridge Status

{table(bridge, ["status_id", "bridge_piece", "current_status", "remaining_gap", "bridge_claim"])}

## Claim Gates

{table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics"])}

## Decisions

{table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{table(next_target, ["next_id", "next_checkpoint", "script", "mission", "starting_equation", "claim_policy"])}

## Validation

{table(validation, ["validation_id", "passed", "requirement", "evidence"])}
"""
    DOC.write_text(body, encoding="utf-8")


def validate(generated_paths: list[Path], branch_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows(OUTPUTS["sources"])
    branch_matrix = rows(OUTPUTS["branch_matrix"])
    qvx = rows(OUTPUTS["qvx_certificate"])
    coupling = rows(OUTPUTS["coupling_audit"])
    scalar_pack = rows(OUTPUTS["scalar_pack"])
    fallback = rows(OUTPUTS["fallback_rows"])
    demotion = rows(OUTPUTS["demotion"])
    bridge = rows(OUTPUTS["bridge"])
    gates = rows(OUTPUTS["gates"])
    decisions = rows(OUTPUTS["decisions"])
    next_target = rows(OUTPUTS["next"])

    checks = [
        ("VAL3091_00_sources_exist", all(boolish(row["exists"]) for row in sources), "all cited source paths exist", "P8_Y5_R2FR_3091_SOURCE_REGISTER.csv"),
        ("VAL3091_01_needles_present", all(boolish(row["needles_present"]) for row in sources), "all cited source needles are present", "P8_Y5_R2FR_3091_SOURCE_REGISTER.csv"),
        ("VAL3091_02_sources_parse", all(boolish(row["parse_ok"]) for row in sources), "all cited CSV sources parse and markdown sources exist", "P8_Y5_R2FR_3091_SOURCE_REGISTER.csv"),
        ("VAL3091_03_csv_parse", all(csv_ok(path) for path in generated_paths + branch_paths), "all generated and branch-copy CSVs parse cleanly", "csv.DictReader parse check"),
        ("VAL3091_04_branch_matrix_demotes", any(row["matrix_id"] == "BDM3091_0_vertical_quotient" and row["current_status"] == "TESTED_NOT_CLOSED" for row in branch_matrix), "branch matrix tests quotient first but does not claim it", "P8_Y5_R2FR_3091_BRANCH_DECISION_MATRIX.csv"),
        ("VAL3091_05_qvx_certificate_complete", len(qvx) >= 9 and any(row["certificate_id"] == "QVC3091_8_verdict" for row in qvx), "q/v_X/action/matter/boundary/degree certificate clauses are complete", "P8_Y5_R2FR_3091_QVX_CERTIFICATE.csv"),
        ("VAL3091_06_qvx_certificate_fails", any(row["certificate_id"] == "QVC3091_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH" for row in qvx), "single quotient certificate fails current claim", "P8_Y5_R2FR_3091_QVX_CERTIFICATE.csv"),
        ("VAL3091_07_coupling_audit_complete", len(coupling) >= 5 and any(row["audit_id"] == "CDA3091_4_verdict" for row in coupling), "coupling descent audit covers metric, markers, hidden frame, boundary/projector and verdict", "P8_Y5_R2FR_3091_COUPLING_DESCENT_AUDIT.csv"),
        ("VAL3091_08_coupling_nonzero_open", any(row["result"] == "COUPLING_NOT_THEOREM_ZERO" for row in coupling), "coupling is not theorem-zero", "P8_Y5_R2FR_3091_COUPLING_DESCENT_AUDIT.csv"),
        ("VAL3091_09_scalar_inputs_complete", len(scalar_pack) >= 6 and any(row["input_id"] == "SNH3091_5_alpha_coefficients" for row in scalar_pack), "scalar no-hair/source input rows are complete", "P8_Y5_R2FR_3091_SCALAR_SOURCE_INPUT_PACK.csv"),
        ("VAL3091_10_scalar_inputs_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in scalar_pack), "scalar/source inputs remain missing and nonclaim", "P8_Y5_R2FR_3091_SCALAR_SOURCE_INPUT_PACK.csv"),
        ("VAL3091_11_fallback_rows_complete", len(fallback) >= 5 and any(row["row_id"] == "FBR3091_4_total_guard" for row in fallback), "fallback rows cover quotient certificate, scalar pack, sourced alpha, edge bound and total guard", "P8_Y5_R2FR_3091_FALLBACK_SOURCE_ROWS.csv"),
        ("VAL3091_12_fallback_rows_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in fallback), "fallback rows remain nonclaim", "P8_Y5_R2FR_3091_FALLBACK_SOURCE_ROWS.csv"),
        ("VAL3091_13_demotion_complete", len(demotion) >= 4 and any(row["demotion"] == "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS" for row in demotion), "demotion rows cover quotient, scalar, sourced and claim ceiling effects", "P8_Y5_R2FR_3091_DEMOTION_LEDGER.csv"),
        ("VAL3091_14_bridge_next_selected", any(row["status_id"] == "GB3091_4_next" and "SCALAR_NOHAIR" in row["current_status"] for row in bridge), "bridge status selects scalar no-hair/residual runner next", "P8_Y5_R2FR_3091_GR_BRIDGE_STATUS.csv"),
        ("VAL3091_15_bridge_nonclaim", all(str(row["bridge_claim"]).lower() == "false" for row in bridge), "GR bridge rows remain nonclaim", "P8_Y5_R2FR_3091_GR_BRIDGE_STATUS.csv"),
        ("VAL3091_16_claim_gates_blocked", all(str(row["claim_allowed_for_physics"]).lower() == "false" for row in gates), "all claim gates remain blocked", "P8_Y5_R2FR_3091_CLAIM_GATE.csv"),
        ("VAL3091_17_demotion_gate_written", any(row["gate_id"] == "CG3091_5_demotion_written" and str(row["gate_pass"]).lower() == "true" for row in gates), "demotion gate is installed", "P8_Y5_R2FR_3091_CLAIM_GATE.csv"),
        ("VAL3091_18_local_GR_gate_false", any(row["gate_id"] == "CG3091_6_local_GR_Newton" and str(row["gate_pass"]).lower() == "false" for row in gates), "local GR/Newton gate remains false", "P8_Y5_R2FR_3091_CLAIM_GATE.csv"),
        ("VAL3091_19_decision_next", any(row["decision"] == "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT" for row in decisions), "decision ledger selects scalar no-hair input pack next", "P8_Y5_R2FR_3091_DECISION_LEDGER.csv"),
        ("VAL3091_20_next_target_selected", len(next_target) == 1 and next_target[0]["next_id"] == "NEXT3091_0_3092", "next target selected", "P8_Y5_R2FR_3091_NEXT_TARGET.csv"),
        ("VAL3091_21_branch_copies_exist", all(path.exists() for path in branch_paths), "branch copy CSVs exist", "P8_Y5_R2FR_3091_BRANCH_COPIES.csv"),
        ("VAL3091_22_formalization_untouched", not any(FORMALIZATION.rglob("*3091*")) if FORMALIZATION.exists() else True, "no 3091 files exist under formalization-workbench", str(FORMALIZATION)),
        ("VAL3091_23_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ removed", str(PYCACHE)),
        ("VAL3091_24_doc_written", DOC.exists() and "qvx_certificate_fails_scalar_inputs_next" in read_text(DOC), "checkpoint markdown is written with nonclaim verdict", str(DOC)),
    ]
    return with_meta(
        [{"validation_id": validation_id, "passed": passed, "requirement": requirement, "evidence": evidence} for validation_id, passed, requirement, evidence in checks]
    )


def main() -> None:
    remove_pycache()
    for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
        path.parent.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    branch_matrix = branch_matrix_rows()
    qvx = qvx_rows()
    coupling = coupling_rows()
    scalar_pack = scalar_pack_rows()
    fallback = fallback_rows()
    demotion = demotion_rows()
    bridge = bridge_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["branch_matrix"], branch_matrix)
    write_csv(OUTPUTS["qvx_certificate"], qvx)
    write_csv(OUTPUTS["coupling_audit"], coupling)
    write_csv(OUTPUTS["scalar_pack"], scalar_pack)
    write_csv(OUTPUTS["fallback_rows"], fallback)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    copy_map = {
        OUTPUTS["qvx_certificate"]: BRANCH_OUTPUTS["qvx_copy"],
        OUTPUTS["coupling_audit"]: BRANCH_OUTPUTS["coupling_copy"],
        OUTPUTS["scalar_pack"]: BRANCH_OUTPUTS["scalar_pack_copy"],
        OUTPUTS["bridge"]: BRANCH_OUTPUTS["bridge_copy"],
        OUTPUTS["next"]: BRANCH_OUTPUTS["next_copy"],
    }
    for source, destination in copy_map.items():
        shutil.copyfile(source, destination)
    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branch_copies)

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    validation = validate(generated_paths, branch_paths)
    write_doc(sources, branch_matrix, qvx, coupling, scalar_pack, fallback, demotion, bridge, gates, decisions, next_target, validation)
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, branch_matrix, qvx, coupling, scalar_pack, fallback, demotion, bridge, gates, decisions, next_target, validation)

    remove_pycache()
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, branch_matrix, qvx, coupling, scalar_pack, fallback, demotion, bridge, gates, decisions, next_target, validation)

    failed = [row for row in validation if not boolish(row["passed"])]
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    print(f"Validation passed {len(validation) - len(failed)}/{len(validation)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['validation_id']}: {row['requirement']} ({row['evidence']})")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
