from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2799-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-residual-retention-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2799_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2799_GK_ACTION_EXISTENCE_THEOREM_ATTEMPT.csv",
    "schema": MTS / "P8_Y5_R2FR_2799_HELMHOLTZ_ACTION_SCHEMA.csv",
    "candidates": MTS / "P8_Y5_R2FR_2799_GK_CANDIDATE_ROWS.csv",
    "runner": MTS / "P8_Y5_R2FR_2799_GK_ACTION_RUNNER.csv",
    "residual": MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv",
    "bound_interface": MTS / "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv",
    "product_candidate": MTS / "P8_Y5_R2FR_2799_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "product_runner": MTS / "P8_Y5_R2FR_2799_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2799_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2799_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2799_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2799_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2799_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2799_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2799_GK_ACTION_EXISTENCE_ATTEMPT_NONCLAIM.csv",
    "residual_queue": RAB_QUEUE / "JR2799_QLOC_RESIDUAL_RETENTION_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2799_QLOC_BOUND_INTERFACE_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_gk_qloc_action_existence_2799_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2799_RESPONSE_DOUBLET_SOURCE_CURRENT_OR_QLOC_BOUND_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def source_entries() -> list[tuple[str, Path, str]]:
    return [
        ("2798_next", MTS / "P8_Y5_R2FR_2798_NEXT_TARGET.csv", "authoritative 2799 target"),
        ("2798_sector_pack", MTS / "P8_Y5_R2FR_2798_MINIMAL_SECTOR_CERTIFICATE_PACK.csv", "Gamma/Khat/q_loc hardest blocker"),
        ("2798_priority", MTS / "P8_Y5_R2FR_2798_NEXT_SECTOR_PRIORITY_LEDGER.csv", "priority selection"),
        ("1010_theorem_analogue", MTS / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv", "R10 action-existence theorem analogue"),
        ("1010_schema_analogue", MTS / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv", "R10 Helmholtz schema analogue"),
        ("1010_candidates_analogue", MTS / "P8_Y5_R10_1010_CANDIDATE_ROWS.csv", "R10 candidate row analogue"),
        ("1010_residual_analogue", MTS / "P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv", "R10 residual retention analogue"),
        ("2733_bound_interface", MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "R2FR q_loc residual bound interface"),
        ("2733_zero_gate", MTS / "P8_Y5_R2FR_2733_ZERO_THEOREM_GATE.csv", "R2FR q_loc zero theorem gates"),
        ("2729_memory_signature", MTS / "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv", "parent memory signature contract"),
        ("2728_JX_audit", MTS / "P8_Y5_R2FR_2728_JX_ZERO_COMPONENT_AUDIT.csv", "source-current component audit"),
    ]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("GKT2799_0_variational_route", "metric-response action route", "S_GK=-int_D sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)+boundary", "K_hat becomes metric response and q_loc is a Ward/Euler residual", "R2FR has residual interfaces and R10 analogue; no current R2FR source signs S_GK", "CANDIDATE_CONTRACT_NOT_CLAIM"),
        ("GKT2799_1_metric_response_identity", "K_hat^{mu nu}=K_metric^{mu nu}", "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} with derivative and boundary conventions", "nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu}) is variational stress divergence", "2733 keeps Delta_K and metric-response gates blocked", "NOT_MATCHED_TO_CURRENT_R2FR_SYMBOLS"),
        ("GKT2799_2_Helmholtz_integrability", "T_GK is variational", "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} symmetric under exchange of metric variations up to boundary", "there exists an S_GK whose metric variation gives the proposed stress", "no R2FR second-variation symmetry calculation exists", "NOT_CHECKED_CURRENT_CLAIM"),
        ("GKT2799_3_Euler_closure", "q_loc vanishes on local compact vacuum equations", "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary; E_A=0 and boundary=0 imply q_loc^nu=0", "local force residual is derived zero rather than plateau-axiom zero", "2728 J_X components and 2733 Ward gates remain unsigned", "NOT_DERIVED"),
        ("GKT2799_4_double_zero", "local fixed point has zero amplitude and zero first variation", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0, equivalently Gamma0 subtracted and K_hat response matched", "PPN/source-normalization hair starts only at bounded higher order", "memory/response double-zero remains conditional and not parent-promoted", "NOT_MATCHED"),
        ("GKT2799_5_projector_boundary", "P_loc and boundary/symplectic no-flux are parent-owned", "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, integral_boundary Delta(theta_GK,Q_GK,tau)=0", "projection and boundary cannot hide/tune force components", "2733/2729 retain projector/domain/boundary missing inputs", "OPEN"),
        ("GKT2799_6_verdict", "derive q_loc^nu=0 from S_GK", "GKT2799_0 through GKT2799_5 all pass with source/equation paths and parent signatures", "local PPN/WEP branch can reopen at residual-vector gate", "route is precise but current R2FR lacks S_GK, metric-response match, Helmholtz, Euler closure, double-zero, projector, and boundary certificates", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "theorem_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "what_would_follow": row[3],
            "current_evidence": row[4],
            "status": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("HGS2799_0_candidate_action", "S_GK", "action_source; scalar_density; field_content; boundary_terms; variation_variables; sign_convention", "S_GK is explicit and diffeomorphism-invariant on the local compact branch"),
        ("HGS2799_1_metric_response", "K_hat", "K_metric_formula; Gamma_eff_formula; volume_convention; derivative_term_accounting; source_path", "existing K_hat equals metric response of sqrt(-g) Gamma_eff including derivative/boundary terms"),
        ("HGS2799_2_Helmholtz", "variational stress", "second_variation_symmetry; boundary_symmetry; variable_domain; gauge_constraints", "stress satisfies Helmholtz integrability, not merely Ward bookkeeping"),
        ("HGS2799_3_Euler_double_zero", "q_loc zero", "Euler_equations; local_fixed_point; source_zero; boundary_zero; T_zero; dT_zero", "q_loc^nu vanishes on shell and first variation vanishes at local fixed point"),
        ("HGS2799_4_residual_retention", "q_loc residual", "q_loc_profile; units; normalization; observable_map; bound_or_gate; source_path; valid_for_claim", "if derivation fails, q_loc is retained as explicit local residual instead of claimed zero"),
    ]
    return [
        {
            "schema_id": row[0],
            "target": row[1],
            "required_fields": row[2],
            "pass_condition": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    base = {
        "target": "Gamma_Khat_q_loc_action_existence",
        "metric_response_certificate": "MISSING_METRIC_RESPONSE_CERTIFICATE",
        "Helmholtz_certificate": "MISSING_HELMHOLTZ_CERTIFICATE",
        "Euler_closure_certificate": "MISSING_EULER_CLOSURE_CERTIFICATE",
        "double_zero_certificate": "MISSING_DOUBLE_ZERO_CERTIFICATE",
        "P_loc_certificate": "MISSING_P_LOC_CERTIFICATE",
        "boundary_no_flux_certificate": "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE",
        "source_current_zero_certificate": "MISSING_SOURCE_CURRENT_ZERO_CERTIFICATE",
        "valid_for_claim": False,
        "generated_utc": utc_now(),
    }
    rows = [
        ("GKC2799_0_metric_response_scalar_density", "S_GK=-int sqrt(-g) Gamma_eff with K_hat as metric response", "P8_GK_STRESS_ACTION_CANDIDATES.csv", "DERIVE_OR_RETAIN"),
        ("GKC2799_1_response_doublet_even_density", "exchange-response doublet makes Gamma_eff even and locally double-zero", "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv", "DERIVE_OR_RETAIN"),
        ("GKC2799_2_positive_auxiliary_fields", "positive auxiliary operator forces Phi=Phi0 on compact source-free collars", "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "DERIVE_OR_RETAIN"),
        ("GKC2799_3_topological_exact_sector", "Gamma/Khat contribution is exact/topological and bulk force-free", "P8_GK_STRESS_ACTION_CANDIDATES.csv", "DERIVE_OR_RETAIN"),
        ("GKC2799_4_plateau_axiom_attempt", "q_loc is set to zero by local plateau assumption", "PLATEAU_AXIOM", "FORBIDDEN_PLATEAU_AXIOM"),
        ("GKC2799_5_bookkeeping_stress_attempt", "Gamma_eff and K_hat are treated as stress pieces without variational action", "BOOKKEEPING_ONLY", "FORBIDDEN_BOOKKEEPING_STRESS"),
        ("GKC2799_6_residual_retention", "q_loc retained as explicit residual profile for local tests", "NOT_REQUIRED_FOR_RESIDUAL", "RETAIN_Q_LOC_AS_EXPLICIT_RESIDUAL"),
    ]
    output = []
    for candidate_id, candidate, action_source, residual_policy in rows:
        row = dict(base)
        row.update(
            {
                "candidate_id": candidate_id,
                "candidate": candidate,
                "action_source": action_source,
                "Gamma_formula_source": "MISSING_GAMMA_FORMULA_SOURCE" if "FORBIDDEN" in residual_policy else "R2FR_SOURCE_REQUIRED",
                "Khat_formula_source": "MISSING_KHAT_FORMULA_SOURCE" if "FORBIDDEN" in residual_policy else "R2FR_SOURCE_REQUIRED",
                "q_loc_profile_source": "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv" if candidate_id.endswith("6_residual_retention") else "MISSING_Q_LOC_PROFILE_SOURCE",
                "observable_map_source": "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv" if candidate_id.endswith("6_residual_retention") else "MISSING_OBSERVABLE_MAP_SOURCE",
                "residual_policy": residual_policy,
                "claim_type": "residual_retention" if candidate_id.endswith("6_residual_retention") else "derivation",
            }
        )
        output.append(row)
    return output


def build_runner_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, candidate in enumerate(candidates):
        is_residual = candidate["claim_type"] == "residual_retention"
        rows.append(
            {
                "runner_id": f"GKR2799_{index}",
                "candidate_id": candidate["candidate_id"],
                "claim_type": candidate["claim_type"],
                "verdict": "RETAINED_NONCLAIM_Q_LOC_RESIDUAL" if is_residual else "REFUSED_DERIVED_Q_LOC_ZERO",
                "score_ready": is_residual,
                "q_loc_zero_derived": False,
                "residual_retained": is_residual,
                "claim_allowed": False,
                "failure_reasons": "VALID_FOR_CLAIM_FALSE" if is_residual else "MISSING_PARENT_SIGNED_METRIC_RESPONSE_CERTIFICATE;MISSING_PARENT_SIGNED_HELMHOLTZ_CERTIFICATE;MISSING_PARENT_SIGNED_EULER_CLOSURE_CERTIFICATE;MISSING_PARENT_SIGNED_DOUBLE_ZERO_CERTIFICATE;MISSING_PARENT_SIGNED_P_LOC_CERTIFICATE;MISSING_PARENT_SIGNED_BOUNDARY_NO_FLUX_CERTIFICATE;MISSING_PARENT_SIGNED_SOURCE_CURRENT_ZERO_CERTIFICATE;VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRES2799_0_q_loc_vector", "q_loc^nu", "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})", "retained_until_S_GK_proved", "PPN alpha_i/xi; WEP local force; source-normalization; clock/orbital residuals", "PARENT_SIGNED_S_GK_METRIC_RESPONSE_HELMHOLTZ_EULER_DOUBLE_ZERO_BOUNDARY_TRUE"),
        ("QRES2799_1_Gamma_metric_response_gap", "Delta_K", "K_hat - K_metric[Gamma_eff]", "retained_symbolic_gap", "if nonzero, enters q_loc and PPN/source-normalization rows", "explicit metric-response match including derivative/boundary terms"),
        ("QRES2799_2_Helmholtz_gap", "H_GK", "antisymmetric second-variation obstruction for proposed T_GK", "retained_symbolic_gap", "if nonzero, no action exists for the claimed stress", "Helmholtz symmetry calculation"),
        ("QRES2799_3_source_boundary_gap", "J_GK + B_GK", "source-current and boundary work in response doublet/Euler identity", "retained_symbolic_gap", "PPN preferred-frame/source hair and local boundary flux", "zero source-current and no-flux theorem"),
        ("QRES2799_4_projector_gap", "[P_loc,nabla]Delta_K", "projector/domain commutator contribution", "retained_symbolic_gap", "domain/projector leakage into local tests", "parent P_loc ownership and commutator bound"),
    ]
    return [
        {
            "residual_id": row[0],
            "residual_symbol": row[1],
            "definition": row[2],
            "status": row[3],
            "observable_map": row[4],
            "required_to_claim_zero": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_bound_interface_rows() -> list[dict[str, Any]]:
    rows = [
        ("QB2799_0_vector_envelope", "||q_loc||_D", "||q_loc|| <= ||P_loc|| (||W_metric|| + C_div ||Delta_K|| + ||[P_loc,nabla]Delta_K||)", "ROLLED_FORWARD_FROM_2733", "P_loc norm; W_metric; C_div; Delta_K norms; projector commutator; units", False),
        ("QB2799_1_00_projection", "q_loc component sourced by Delta_K00", "||q_loc||_00 <= ||P_loc|| (C_0 ||partial_0 Delta_K00|| + C_i ||partial_i Delta_K00|| + component mixing)", "SCHEMA_ONLY_STATIC_REDUCTION_NOT_SIGNED", "stationary domain rule; derivative scale; units; local projection", False),
        ("QB2799_2_observable_projection", "PPN/WEP/R10/clock/orbital readout", "residual_arena <= K_arena ||q_loc|| or K_arena ||Delta_K||", "PROJECTION_MISSING", "K_PPN; K_WEP; K_R10; K_clock; K_orbital; source normalization", False),
        ("QB2799_3_verdict", "first q_loc residual bound", "symbolic envelope exists but no numeric/source-backed score row exists", "NOT_SCORE_READY_REDUCED_TO_KERNELS", "kernel norms, arena projections, source-backed constants", False),
    ]
    return [
        {
            "bound_id": row[0],
            "quantity": row[1],
            "bound_form": row[2],
            "known_status": row[3],
            "missing_inputs": row[4],
            "score_ready": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_product_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2799_0_no_claim_product",
            "observable": "local WEP/PPN response from q_loc",
            "prediction_status": "NO_NUMERIC_PREDICTION",
            "claim_blocker": "q_loc retained as nonclaim residual; no source-backed arena projection",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_product_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2799_0_refuse_q_loc_claim",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_LOCAL_GR_CLAIM",
            "reason": "q_loc zero is not derived and residual bound rows are not score-ready",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2799_0_no_numeric_local_response",
            "baseline": "local-GR/WEP/PPN compatibility",
            "prediction": "MTS q_loc residual",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "q_loc residual has symbolic envelope only",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2799_0_S_GK_action", "S_GK exists as accepted R2FR parent sector", False, False, "candidate routes are contracts but not matched to current symbols"),
        ("CG2799_1_metric_response", "K_hat is metric response of Gamma_eff", False, False, "metric-response identity is not matched including derivative/boundary terms"),
        ("CG2799_2_Helmholtz", "T_GK satisfies Helmholtz integrability", False, False, "second variation symmetry is not checked"),
        ("CG2799_3_Euler_double_zero", "q_loc vanishes by Euler closure and double-zero", False, False, "source-current, boundary, projector, and local fixed-point certificates are missing"),
        ("CG2799_4_plateau_guard", "local plateau axiom may set q_loc=0", False, False, "plateau axiom is rejected"),
        ("CG2799_5_local_GR_reopen", "local-GR/WEP/PPN gates can reopen", False, False, "q_loc remains retained residual"),
        ("CG2799_6_residual_retention", "q_loc residual is retained rather than hidden", True, False, "explicit nonclaim residual row is installed"),
        ("CG2799_7_guardrail", "Gamma/Khat action-existence guardrail is installed", True, False, "derivation shortcuts are refused and q_loc is retained"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2799_0_derivation_route_precise", "The derivation route is precise: S_GK plus metric-response K_hat plus Helmholtz plus Euler/double-zero would derive q_loc=0.", "Ward identity then turns q_loc into an on-shell variational residual rather than an axiom.", "try the response-doublet source-current/boundary zero route, because it is the most concrete route to Gamma double-zero"),
        ("DEC2799_1_not_currently_proved", "Current R2FR corpus does not prove the route.", "metric-response match, Helmholtz symmetry, source-current zero, P_loc ownership, and boundary no-flux are missing.", "do not reopen local-GR/WEP/PPN until these are sourced or residual-bounded"),
        ("DEC2799_2_residual_kept_honest", "q_loc is retained as an explicit residual instead of being hidden.", "this keeps PPN/WEP/source-normalization testing honest if derivation fails.", "either prove response-doublet zero-source/boundary theorem or fill q_loc observable coefficients"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2799_0_2800",
            "next_target": "2800-Y5-R2FR-response-doublet-source-current-zero-or-q_loc-bound-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_response_doublet_source_current_zero_or_q_loc_bound_fill_under_AX1090_2800.py",
            "objective": "try to prove the response-doublet source-current and boundary terms vanish for the local compact branch; if not, produce q_loc residual bound-fill rows",
            "include": "R_plus/R_minus; exchange symmetry; Gamma_eff even density; positive operator; J_Z=0; B_Z=0; PPN/WEP/source-normalization map; q_loc units and bounds",
            "exclude": "plateau axiom; bookkeeping stress; fitted cancellation; H_tau pass; M_H_ref pass; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "theorem_queue"),
        (OUTPUTS["residual"], BRANCH_OUTPUTS["residual_queue"], "residual_queue"),
        (OUTPUTS["bound_interface"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["theorem"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append({"copy_id": f"BC2799_{label}", "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False, "generated_utc": utc_now()})
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2799_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2799_1_theorem_attempted", any(row["theorem_id"] == "GKT2799_6_verdict" for row in sections["theorem"]), "GK/q_loc theorem attempt exists"),
        ("VAL2799_2_zero_not_derived", any(row["theorem_id"] == "GKT2799_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["theorem"]), "q_loc zero is not claimed"),
        ("VAL2799_3_schema_complete", {row["schema_id"] for row in sections["schema"]} >= {"HGS2799_0_candidate_action", "HGS2799_1_metric_response", "HGS2799_2_Helmholtz", "HGS2799_3_Euler_double_zero", "HGS2799_4_residual_retention"}, "Helmholtz/action schema has all gates"),
        ("VAL2799_4_runner_retains_residual", any(row["verdict"] == "RETAINED_NONCLAIM_Q_LOC_RESIDUAL" and row["residual_retained"] == True for row in sections["runner"]), "q_loc residual is retained"),
        ("VAL2799_5_forbidden_routes_refused", any(row["candidate_id"] == "GKC2799_4_plateau_axiom_attempt" and row["residual_policy"] == "FORBIDDEN_PLATEAU_AXIOM" for row in sections["candidates"]) and any(row["candidate_id"] == "GKC2799_5_bookkeeping_stress_attempt" and row["residual_policy"] == "FORBIDDEN_BOOKKEEPING_STRESS" for row in sections["candidates"]), "plateau and bookkeeping shortcuts are refused"),
        ("VAL2799_6_q_loc_formula_retained", any(row["residual_id"] == "QRES2799_0_q_loc_vector" and "P_loc" in row["definition"] for row in sections["residual"]), "physical q_loc formula is retained"),
        ("VAL2799_7_bound_interface_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in sections["bound_interface"]), "bound interface remains nonclaim"),
        ("VAL2799_8_product_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_LOCAL_GR_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["product_runner"]), "product runner refuses claim"),
        ("VAL2799_9_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2799_10_next_target_2800", any(row["next_id"] == "NEXT2799_0_2800" for row in sections["next"]), "next target is 2800"),
        ("VAL2799_11_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2799_12_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2799_13_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2799_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2799_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2799_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2799_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2799_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2799 tests Gamma/Khat/q_loc action-existence. The derivation route is precise but not proven; plateau/bookkeeping shortcuts are refused; q_loc is retained as an explicit nonclaim residual with a rolled-forward bound interface.", "generated_utc": utc_now()})
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2799 — Y5 R2FR Gamma/Khat/q_loc Action Existence Helmholtz Or Residual Retention Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2799 gives the clean action-existence ladder for the local residual sector. If an explicit `S_GK` exists, `K_hat` matches the metric response of `Gamma_eff`, Helmholtz symmetry holds, Euler closure gives a double-zero local fixed point, and projector/boundary terms are silent, then `q_loc^nu` can be derived zero.",
        "",
        "The current R2FR corpus does not close that ladder. Therefore `q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})` is retained as an explicit nonclaim residual. Plateau axioms and bookkeeping stress shortcuts are rejected.",
        "",
        "## Theorem Attempt",
        markdown_table(sections["theorem"], ["theorem_id", "claim_piece", "status", "current_evidence"]),
        "",
        "## Helmholtz Action Schema",
        markdown_table(sections["schema"], ["schema_id", "target", "required_fields", "pass_condition"]),
        "",
        "## Candidate Rows",
        markdown_table(sections["candidates"], ["candidate_id", "candidate", "residual_policy", "claim_type", "valid_for_claim"]),
        "",
        "## Action Runner",
        markdown_table(sections["runner"], ["runner_id", "candidate_id", "verdict", "q_loc_zero_derived", "residual_retained", "claim_allowed"]),
        "",
        "## q_loc Residual Ledger",
        markdown_table(sections["residual"], ["residual_id", "residual_symbol", "definition", "status", "required_to_claim_zero"]),
        "",
        "## Bound Interface",
        markdown_table(sections["bound_interface"], ["bound_id", "quantity", "known_status", "missing_inputs", "score_ready"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "theorem": build_theorem_rows(),
        "schema": build_schema_rows(),
        "candidates": build_candidate_rows(),
    }
    sections["runner"] = build_runner_rows(sections["candidates"])
    sections["residual"] = build_residual_rows()
    sections["bound_interface"] = build_bound_interface_rows()
    sections["product_candidate"] = build_product_candidate_rows()
    sections["product_runner"] = build_product_runner_rows()
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
