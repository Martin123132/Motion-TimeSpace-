from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3605"
BRANCH_ID = "MTS_R2FR_Y5_VQ_FIRST_CLASS_SOURCE_SILENCE_3605"
DOC = ROOT / "3605-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3604": (RESIDUALS / "P8_Y5_R2FR_3604_NEXT_TARGET.csv", "NEXT3604_0"),
        "status_3604": (RESIDUALS / "P8_Y5_R2FR_3604_STATUS.csv", "ACTUAL_QMAP_VERTICAL_BASIS"),
        "bounds_3604": (RESIDUALS / "P8_Y5_R2FR_3604_DQ_LEAK_BOUND_ROWS.csv", "DQB3604_1_v_q_private"),
        "candidate_vertical_basis": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_VERTICAL_BASIS.csv", "VB3517_0_v_q_private"),
        "vq_status": (RESIDUALS / "P8_EM_vq_private_firstclass_source_silence_status.csv", "STAT3518_0_Z_vq_first_class"),
        "vq_normal_form": (RESIDUALS / "P8_EM_vq_parent_object_language_normal_form_candidate.csv", "NF3519_2_matter_functor"),
        "qap_status": (RESIDUALS / "P8_EM_quotient_action_derives_q_normal_form_status.csv", "STAT3520_1_CqT"),
        "primitives_qap": (RESIDUALS / "P8_EM_MTS_primitives_to_QAP_status.csv", "STAT3521_1_QAP_parent_owned"),
        "qmap_private": (RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_6_private_q"),
        "q_source_vector": (RESIDUALS / "P8_Y5_NO_SHADOW_2529_Q_SOURCE_VECTOR_IMPORT.csv", "QSV2529_0_normal_form"),
        "bqweyl_first": (RESIDUALS / "P8_Y5_NO_SHADOW_2529_FIRST_DANGEROUS_BQWEYL_ROW.csv", "FDQ2529_0_BqWeyl"),
        "bqweyl_status": (RESIDUALS / "P8_Y5_NO_SHADOW_2530_BQWEYL_BOUND_ROW_STATUS.csv", "BQB2530_1_parent_coefficient"),
        "bqweyl_zero": (RESIDUALS / "P8_Y5_NO_SHADOW_2530_LINEAR_BQWEYL_ZERO_AUDIT.csv", "LBZ2530_0_metric_trace"),
        "dqweyl2": (RESIDUALS / "P8_Y5_NO_SHADOW_2531_DQWEYL2_COEFFICIENT_AUDIT.csv", "DQC2531_1_zero_route"),
        "common_descent": (RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv", "QVIS2643_0_chain_rule_theorem"),
        "common_leaks": (RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv", "LEAK2643_0_eps_JH_Z_abs"),
        "arena_map": (RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_ARENA_LEAK_MAP.csv", "AM2643_0_Newton"),
        "field_residual_split": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_RESIDUAL_OWNER_SPLIT.csv", "RS2570_1_q_source"),
        "first_class_contract": (RESIDUALS / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv", "FCC1555_2_generator"),
        "constraint_elimination": (RESIDUALS / "P8_Y5_CONSTRAINT_ELIMINATION_2628_CONSTRAINT_ELIMINATION_THEOREM_GATE.csv", "CET2628_2_first_class_route"),
        "dqz_kernel": (RESIDUALS / "P8_Y5_PARENT_QLOC_1671_DQZ_KERNEL_THEOREM_ATTEMPT.csv", "KT1671_0_kernel_theorem_statement"),
        "dqz_zero_attempt": (RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_ATTEMPT.csv", "ZTA1673_3_verdict"),
        "dqz_zero_conditions": (RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_CONDITIONS.csv", "ZC1673_1_quotient_map"),
        "constraint_first": (RESIDUALS / "P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv", "CFD1675_6_verdict"),
        "dqz_leaks": (RESIDUALS / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv", "LEAK1675_1_source_weight"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3605_SOURCE_REGISTER.csv",
        "vq_theorem": RESIDUALS / "P8_Y5_R2FR_3605_VQ_FIRST_CLASS_SOURCE_SILENCE_THEOREM.csv",
        "source_vector_decomposition": RESIDUALS / "P8_Y5_R2FR_3605_VQ_SOURCE_VECTOR_DECOMPOSITION.csv",
        "dq_vq_bound_rows": RESIDUALS / "P8_Y5_R2FR_3605_DQ_VQ_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3605_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3605_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3605_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_vq_first_class_source_silence_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3605_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "VQ3605_0_target",
            "3605 target",
            "Prove v_q is first-class/source-silent across geometry, tau, matter, boundary and readout q-components, or retain epsilon_Dq_vq.",
            "3604 selected v_q as the highest-priority Dq direction feeding A_X and local closure.",
            "TARGET_IMPORTED",
            "next_3604",
        ),
        (
            "VQ3605_1_first_class_zero_theorem",
            "first-class verticality theorem",
            "If v_q is generated by a differentiable first-class G_q with zero/proper local boundary charge, closed bracket, correct degree count and matter/readout descent, then Dq[v_q]=0.",
            "A true gauge/quotient generator moves only along a reduced-phase-space fibre.  Its charge and brackets must be parent-owned; otherwise it is only a named direction.",
            "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "first_class_contract",
        ),
        (
            "VQ3605_2_constraint_first_route",
            "constraint-first elimination theorem",
            "If q_private is removed by a parent constraint or auxiliary equation before q, matter and readout are formed, then v_q is not a physical source direction and Dq[v_q]=0 on the reduced branch.",
            "This is the clean fallback to first-class gauge: eliminate before readout, not after tests fail.",
            "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "constraint_elimination",
        ),
        (
            "VQ3605_3_source_vector_normal_form",
            "q source-vector decomposition",
            "E_q=L_q q+B_qRic R_Ricci+B_qW C_Weyl+C_qT T_H+epsilon_q_source sigma_source+Q_q_body delta_body+Pi_q delta_boundary+tail_q.",
            "This makes source silence termwise.  Local exterior vacuum does not kill Weyl, boundary/readout or tail terms.",
            "EXACT_SOURCE_VECTOR_DECOMPOSITION",
            "q_source_vector",
        ),
        (
            "VQ3605_4_source_silence_bound_law",
            "epsilon_Dq_vq bound law",
            "epsilon_Dq_vq <= E_first_class + E_BqWeyl + E_CqT + E_q_source + E_body + E_boundary + E_readout + E_tail + E_norm.",
            "If first-class/source-silence fails, v_q becomes a no-cancellation bound vector, not a hidden closure assumption.",
            "EXACT_BOUND_LAW_NONCLAIM",
            "bounds_3604",
        ),
        (
            "VQ3605_5_BqWeyl_zero_route",
            "linear Weyl zero route",
            "B_qWeyl=0 if q_private dependence is forbidden by QAP and the parent object language has no Weyl spurion, projector, hidden tensor or readout kernel.",
            "Metric/epsilon-only one-Weyl scalar terms vanish by index symmetry, but the no-spurion clause is not parent-signed.",
            "CONDITIONAL_ZERO_ROUTE_NOT_LIVE",
            "bqweyl_zero",
        ),
        (
            "VQ3605_6_CqT_zero_route",
            "matter trace/direct q-source zero route",
            "C_qT=0 if the matter functor has no q_private argument, no q_private T_H vertex and no source-only action prefactor before variation.",
            "The normal-form route is clear, but parent object-language/QAP ownership is unsigned.",
            "CONDITIONAL_ZERO_ROUTE_NOT_LIVE",
            "vq_normal_form",
        ),
        (
            "VQ3605_7_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS cannot set Dq[v_q]=0: first-class, source-silence, B_qWeyl, C_qT, source-normalization, boundary/readout and tail gates all remain nonclaim.",
            "v_q remains the best route, but epsilon_Dq_vq must be carried as a component bound.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "vq_status",
        ),
        (
            "VQ3605_8_best_next_move",
            "next mathematical pressure point",
            "Attack B_qWeyl first: it is the first dangerous source-vector row because Weyl/tidal curvature survives local exterior vacuum.",
            "A B_qWeyl theorem or finite row gives the biggest immediate gain for PPN, orbital and local-GR closure discipline.",
            "NEXT_TARGET_SELECTED",
            "bqweyl_first",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def decomposition_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("VQR3605_0_total", "epsilon_Dq_vq", "E_first_class+E_BqWeyl+E_CqT+E_q_source+E_body+E_boundary+E_readout+E_tail+E_norm", "total v_q quotient leak", "ACTIVE_NONCLAIM_BOUND_VECTOR", "bounds_3604"),
        ("VQR3605_1_E_first_class", "E_first_class", "failure of G_q generator, zero/proper charge, bracket closure, degree count or matter map", "first-class/gauge failure", "OPEN_FIRST_CLASS_PACKAGE_REQUIRED", "first_class_contract"),
        ("VQR3605_2_E_constraint_first", "E_constraint_first", "failure of parent constraint/auxiliary elimination before q and readout", "constraint-first elimination failure", "OPEN_CONSTRAINT_OR_AUXILIARY_ROUTE", "constraint_first"),
        ("VQR3605_3_E_BqWeyl", "E_BqWeyl", "|B_qWeyl| ||G_q C_Weyl|| plus no-spurion failure", "linear Weyl/tidal source-vector leakage", "OPEN_BQWEYL_ZERO_OR_BOUND_REQUIRED", "bqweyl_status"),
        ("VQR3605_4_E_DqWeyl2", "E_DqWeyl2", "|D_qWeyl2| ||G_q C^2||", "quadratic Weyl/higher-curvature q leakage", "OPEN_HIGHER_CURVATURE_BOUND_REQUIRED", "dqweyl2"),
        ("VQR3605_5_E_CqT", "E_CqT", "|C_qT| ||G_q T_H|| plus direct qT/source matter vertex", "matter trace/direct source q leakage", "OPEN_CQT_ZERO_OR_BOUND_REQUIRED", "qap_status"),
        ("VQR3605_6_E_q_source", "E_q_source", "epsilon_q_source sigma_source + c_q_source", "source-normalization q leakage", "OPEN_SOURCE_NORMALIZATION_BOUND_REQUIRED", "field_residual_split"),
        ("VQR3605_7_E_matter", "E_matter", "eps_JH_Z_abs <= C_matter Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary", "ordinary Hilbert source/matter descent leak", "OPEN_MATTER_DESCENT_REQUIRED", "common_leaks"),
        ("VQR3605_8_E_boundary", "E_boundary", "Q_q_body delta_body + Pi_q delta_boundary + boundary/projector/source-measure tails", "body/boundary/projector leakage", "OPEN_BOUNDARY_PROJECTOR_SILENCE_REQUIRED", "dqz_leaks"),
        ("VQR3605_9_E_readout", "E_readout", "readout/firewall/order leakage into q source vector", "post-variation readout re-entry", "OPEN_READOUT_FIREWALL_REQUIRED", "vq_normal_form"),
        ("VQR3605_10_E_tail", "E_tail", "tail_q and retained non-Hilbert/nonlocal source-vector terms", "remaining q-tail leakage", "OPEN_TAIL_BOUND_REQUIRED", "q_source_vector"),
        ("VQR3605_11_E_norm", "E_norm", "missing q operator normalization, G_q/L_q domain and q norm", "operator/norm ownership gap", "OPEN_Q_OPERATOR_NORM_REQUIRED", "bqweyl_status"),
        ("VQR3605_12_arena_transfer", "E_arena_transfer", "Pi_arena(epsilon_Dq_vq + eps_JH + E_DqZ_A)", "Newton/PPN/R10/WEP/clock/orbital transfer schema", "ARENA_ROWS_NONCLAIM", "arena_map"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, formula, meaning, status, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("VQB3605_0_total", "epsilon_Dq_vq", "E_first_class+E_BqWeyl+E_CqT+E_q_source+E_body+E_boundary+E_readout+E_tail+E_norm", "q_component_norm", "MISSING_VQ_DQ_NORM", "all v_q source-vector components theorem-zero or source-backed; no cancellation", "bounds_3604", "BOUND_REQUIRED_HIGHEST_PRIORITY"),
        ("VQB3605_1_E_first_class", "E_first_class", "||Dq[v_q]|| from missing G_q/charge/bracket/degree/matter-map first-class package", "q_component_norm", "MISSING_FIRST_CLASS_PACKAGE", "parent phase space, constraint, differentiable generator, zero/proper charge, bracket closure, degree count, matter map", "first_class_contract", "BOUND_REQUIRED"),
        ("VQB3605_2_E_constraint_first", "E_constraint_first", "residual if q_private is not eliminated before q/matter/readout", "q_component_norm", "MISSING_CONSTRAINT_FIRST_ELIMINATION", "parent constraint or auxiliary solve before q/readout with no tails", "constraint_elimination", "BOUND_REQUIRED"),
        ("VQB3605_3_E_BqWeyl", "E_BqWeyl", "|B_qWeyl| ||G_q C_Weyl||", "q_source_vector_norm", "MISSING_BQWEYL_ZERO_OR_NUMERIC_BOUND", "no-Weyl-spurion theorem or B_qWeyl coefficient, q operator, Weyl profile and arena projection", "bqweyl_status", "BOUND_REQUIRED_FIRST_DANGEROUS"),
        ("VQB3605_4_E_DqWeyl2", "E_DqWeyl2", "|D_qWeyl2| ||G_q C_abcd C^abcd||", "q_source_vector_norm", "MISSING_DQWEYL2_COEFFICIENT_OR_BOUND", "no-higher-curvature theorem or finite D_qWeyl2 coefficient and q kernel", "dqweyl2", "BOUND_REQUIRED"),
        ("VQB3605_5_E_CqT", "E_CqT", "|C_qT| ||G_q T_H||", "q_source_vector_norm", "MISSING_CQT_ZERO_OR_BOUND", "QAP/matter normal form or direct source matter coefficient bound", "qap_status", "BOUND_REQUIRED"),
        ("VQB3605_6_E_q_source", "E_q_source", "epsilon_q_source sigma_source + c_q_source", "source_normalization_norm", "MISSING_Q_SOURCE_NORMALIZATION_BOUND", "source-normalization theorem or finite coefficient/source profile", "field_residual_split", "BOUND_REQUIRED"),
        ("VQB3605_7_E_matter", "E_matter", "eps_JH_Z_abs matter descent leak", "source_normalized", "MISSING_MATTER_DESCENT_BOUND", "no source-only slot, no marker, matter boundary silence and Dq norm", "common_leaks", "BOUND_REQUIRED"),
        ("VQB3605_8_E_boundary", "E_boundary", "Q_q_body delta_body + Pi_q delta_boundary", "boundary_source_norm", "MISSING_BODY_BOUNDARY_TAIL_BOUND", "worldtube/body and boundary/projector tail rows", "dqz_leaks", "BOUND_REQUIRED"),
        ("VQB3605_9_E_readout", "E_readout", "readout re-entry tail into q source vector", "readout_norm", "MISSING_READOUT_FIREWALL_BOUND", "variation-before-readout and post-variation firewall", "vq_normal_form", "BOUND_REQUIRED"),
        ("VQB3605_10_E_norm", "E_norm", "q operator, L_q/G_q, q norm and domain normalization defect", "operator_norm", "MISSING_Q_OPERATOR_NORMALIZATION", "same-domain q Green operator and q-component norm", "bqweyl_status", "BOUND_REQUIRED"),
        ("VQB3605_11_Ax_transfer", "epsilon_AX_from_vq", "||dYbar|| epsilon_Dq_vq + E_Y", "source_coordinate_connection_norm", "NOT_SCORE_READY_TRANSFER", "feeds 3603 A_X only after dYbar/E_Y/source-coordinate rows are source-backed", "bounds_3604", "TRANSFER_ROW_NONCLAIM"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": p[source_id],
            "score_status": score_status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_id, score_status in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3605_0_first_class_route", "v_q first-class theorem", "PASS_CONDITIONAL_THEOREM", "first-class generator with proper charge/brackets would prove Dq[v_q]=0", "first_class_contract"),
        ("PROM3605_1_source_vector_decomposition", "q source-vector decomposition", "PASS_EXACT_DECOMPOSITION", "B_qWeyl, C_qT, source, body, boundary, readout and tail channels are explicit", "q_source_vector"),
        ("PROM3605_2_bound_law", "epsilon_Dq_vq bound law", "PASS_EXACT_BOUND_LAW", "failed zero route becomes no-cancellation component bound vector", "bounds_3604"),
        ("PROM3605_3_current_vq_zero_claim", "current Dq[v_q]=0 claim", "FAIL_CURRENT_CLAIM", "first-class and source-silence gates both fail in current source hierarchy", "vq_status"),
        ("PROM3605_4_current_source_silence_claim", "current J_q_total=0 claim", "FAIL_CURRENT_CLAIM", "B_qWeyl, C_qT, source-normalization, boundary/readout and tail channels remain live", "vq_status"),
        ("PROM3605_5_BqWeyl_priority", "B_qWeyl first dangerous row", "PASS_ROUTE_SELECTED", "Weyl/tidal curvature survives exterior vacuum, so B_qWeyl is the first source-vector row to attack", "bqweyl_first"),
        ("PROM3605_6_QAP_not_live", "QAP/normal-form route", "PASS_CONDITIONAL_NOT_LIVE", "QAP would kill q_private source operators, but QAP is not parent-owned yet", "primitives_qap"),
        ("PROM3605_7_no_Newton_GR_claim", "Newton/PPN/local-GR promotion", "FAIL_CURRENT_CLAIM", "v_q is not certified vertical and epsilon_Dq_vq is not sourced", "status_3604"),
        ("PROM3605_8_bound_pack", "v_q bound pack complete", "PASS_NONCLAIM", "epsilon_Dq_vq component rows are source-ready but not score-ready", "bounds_3604"),
        ("PROM3605_9_next_target", "next target selected", "PASS_ROUTE_SELECTED", "attack B_qWeyl zero or finite Weyl-bound next", "bqweyl_first"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "VQ_FIRST_CLASS_SOURCE_SILENCE_NOT_LIVE_BQWEYL_NEXT",
            "strongest_result": "3605 derives the exact v_q route: Dq[v_q]=0 would follow from a parent-owned first-class/constraint-first package or from termwise q source-vector silence. Current MTS has neither live, so epsilon_Dq_vq is a component bound vector.",
            "decision": "keep v_q as the highest-priority vertical candidate, retain first-class, B_qWeyl, C_qT, source-normalization, matter, boundary, readout, tail and norm rows as nonclaim bounds, and attack B_qWeyl next because it survives exterior vacuum",
            "still_missing": "parent G_q/constraint generator, zero/proper boundary charge, bracket closure, degree count, q operator normalization, QAP parent ownership, no-Weyl-spurion theorem, C_qT matter normal form, source normalization, body/boundary/readout tail silence and arena projections",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["vq_status"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3605_0",
            "target_doc": "3606-Y5-R2FR-BqWeyl-no-spurion-zero-or-finite-Weyl-bound.md",
            "target_script": "scripts/Y5_R2FR_3606_BqWeyl_no_spurion_zero_or_finite_Weyl_bound.py",
            "objective": "try to prove B_qWeyl=0 from QAP plus the no-Weyl-spurion/index theorem; if not, retain finite B_qWeyl rows with q operator normalization, Weyl profile, units and arena projections",
            "success_gate": "v_q source silence cannot advance until B_qWeyl is theorem-zero or source-backed finite, because exterior vacuum does not kill Weyl/tidal curvature",
            "reason": "3605 keeps v_q as the best vertical candidate and identifies B_qWeyl as the first dangerous source-vector component",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3605_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3605 source paths exist"))
    validations.append(("VAL3605_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3605 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3605_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3605 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3605_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3605_4_first_class_route_present", any(row["theorem_id"] == "VQ3605_1_first_class_zero_theorem" for row in theorem), "v_q first-class zero theorem present"))
    validations.append(("VAL3605_5_source_vector_decomposition_present", {"E_BqWeyl", "E_CqT", "E_q_source", "E_boundary", "E_readout", "E_tail"}.issubset({str(row["symbol"]) for row in decomposition}), "critical source-vector components present"))
    validations.append(("VAL3605_6_bound_rows_present", {"epsilon_Dq_vq", "E_first_class", "E_BqWeyl", "E_CqT", "E_boundary", "E_readout", "E_norm"}.issubset({str(row["symbol"]) for row in bounds}), "critical v_q bound rows present"))
    validations.append(("VAL3605_7_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3605_3_current_vq_zero_claim", "PROM3605_4_current_source_silence_claim", "PROM3605_7_no_Newton_GR_claim"]), "v_q/source/local-GR claims are blocked"))
    validations.append(("VAL3605_8_BqWeyl_next", any(row["next_id"] == "NEXT3605_0" for row in next_target), "3606 BqWeyl target selected"))
    validations.append(("VAL3605_9_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, decomposition, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, decomposition, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3605_10_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3605*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3605-") or path.name.startswith("Y5_R2FR_3605") or "P8_Y5_R2FR_3605" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3605_11_formalization_workbench_untouched", len(formal_hits) == 0, "no 3605 checkpoint output appears in formalization-workbench outside package/venv noise"))
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(theorem, decomposition, bounds, gates, status, next_target, validation) -> None:
    lines = [
        "# 3605 - vq first-class source-vector silence or Dq_vq bound",
        "",
        "## Verdict",
        "3605 keeps the derivation-first route alive but refuses the shortcut: `Dq[v_q]=0` would follow from a real first-class/constraint-first package or from termwise q-source-vector silence, but current MTS has neither signed.",
        "",
        "The concrete nonclaim law is now `epsilon_Dq_vq <= E_first_class + E_BqWeyl + E_CqT + E_q_source + E_body + E_boundary + E_readout + E_tail + E_norm`.",
        "",
        "`B_qWeyl` is the first dangerous component because Weyl/tidal curvature survives exterior vacuum.  So the next useful attack is not another global audit; it is the no-Weyl-spurion zero proof or a finite Weyl-bound row.",
        "",
        "## v_q Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Source-Vector Decomposition"])
    for row in decomposition:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Dq_vq Bound Rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` / `{row['symbol']}`: {row['score_status']} - {row['formula']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    theorem = theorem_rows(source_map)
    decomposition = decomposition_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["vq_theorem"], theorem)
    write_csv(out_paths["source_vector_decomposition"], decomposition)
    write_csv(out_paths["dq_vq_bound_rows"], bounds)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, decomposition, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, decomposition, bounds, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
