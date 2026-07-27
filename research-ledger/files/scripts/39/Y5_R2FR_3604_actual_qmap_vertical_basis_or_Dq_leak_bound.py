from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3604"
BRANCH_ID = "MTS_R2FR_Y5_ACTUAL_QMAP_VERTICAL_BASIS_3604"
DOC = ROOT / "3604-Y5-R2FR-actual-qmap-vertical-basis-or-Dq-leak-bound.md"


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
        "next_3603": (RESIDUALS / "P8_Y5_R2FR_3603_NEXT_TARGET.csv", "NEXT3603_0"),
        "status_3603": (RESIDUALS / "P8_Y5_R2FR_3603_STATUS.csv", "SOURCE_COORDINATE_QBASIC_AX"),
        "bounds_3603": (RESIDUALS / "P8_Y5_R2FR_3603_AX_BOUND_ROWS.csv", "AXB3603_1_Dq_vX"),
        "candidate_q_map": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_Q_MAP.csv", "QMAP3517_0_public_geometry"),
        "qmap_anti_tautology": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_Q_MAP.csv", "QMAP3517_5_source_coordinates_Y"),
        "candidate_vertical_basis": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_VERTICAL_BASIS.csv", "VB3517_0_v_q_private"),
        "dq_matrix_skeleton": (RESIDUALS / "P8_Y5_R2FR_3517_DQ_MATRIX_SKELETON.csv", "DQM3517_v_q_Y_target"),
        "dq_norm_template": (RESIDUALS / "P8_Y5_R2FR_3517_DQ_NORM_BOUND_TEMPLATE.csv", "DQB3517_0_v_q_private"),
        "field_quotient_theorem": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_THEOREM_ATTEMPT.csv", "THM2570_0_chain_rule_descent"),
        "field_signature": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv", "FSIG2570_2_q_private"),
        "field_claim_gates": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_CLAIM_GATES.csv", "GATE2570_1_q_parent_signed"),
        "field_residual_split": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_RESIDUAL_OWNER_SPLIT.csv", "RS2570_1_q_source"),
        "field_readout_order": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_READOUT_ORDER_GATE.csv", "RO2570_1_same_frame"),
        "field_coeff_descent": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_COEFFICIENT_DESCENT_GATE.csv", "CD2570_0_descent_theorem"),
        "qmap_kernel_audit": (RESIDUALS / "P8_Y5_R2FR_2970_QMAP_KERNEL_AUDIT.csv", "QMAP2970_2_source"),
        "qloc_kernel_gate": (RESIDUALS / "P8_Y5_PARENT_QLOC_2223_QMAP_VERTICAL_KERNEL_GATE.csv", "QGATE2223_2_kernel"),
        "vertical_kernel_certificate": (RESIDUALS / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv", "VKC2392_0_vertical_basis"),
        "vertical_kernel_condition": (RESIDUALS / "P8_Y5_R2FR_2827_VERTICAL_KERNEL_CONDITION.csv", "KER2827_4_q_nonkernel"),
        "source_coordinate_certificate": (RESIDUALS / "P8_Y5_R2FR_3516_QUOTIENT_SOURCE_COORDINATE_DESCENT_CERTIFICATE.csv", "QSC3516_0_master_theorem"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3604_SOURCE_REGISTER.csv",
        "vertical_theorem": RESIDUALS / "P8_Y5_R2FR_3604_QMAP_VERTICAL_THEOREM.csv",
        "direction_matrix": RESIDUALS / "P8_Y5_R2FR_3604_DIRECTION_DQ_MATRIX_AUDIT.csv",
        "dq_leak_bounds": RESIDUALS / "P8_Y5_R2FR_3604_DQ_LEAK_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3604_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3604_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3604_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_actual_qmap_vertical_basis_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3604_VALIDATION.csv",
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
            "DQV3604_0_target",
            "3604 target",
            "Construct the actual q-map/Dq matrix and certify which residual directions are vertical; otherwise retain Dq leak bounds direction by direction.",
            "3603 showed every q-basic zero theorem depends on the same live condition Dq(v_X)=0.",
            "TARGET_IMPORTED",
            "next_3603",
        ),
        (
            "DQV3604_1_vertical_criterion",
            "q-map verticality criterion",
            "For q=(q_geom,q_tau,q_matter,q_boundary,q_coeff,q_projector,readout), a direction v is vertical iff every listed Dq_a[v] is zero on the same branch.",
            "Verticality is a matrix statement, not a label. Conditional zeros with different blockers do not certify v in ker(Dq).",
            "EXACT_MATRIX_CRITERION",
            "dq_matrix_skeleton",
        ),
        (
            "DQV3604_2_norm_bound_law",
            "Dq leak norm law",
            "epsilon_Dq[v] := ||Dq[v]||_q/||v|| <= sum_a epsilon_a[v] using a declared q-component norm; zero requires every component epsilon_a[v]=0.",
            "This gives a no-cancellation bound path for q-basic theorem leakage into A_X, H_tau, density, support, clocks, PPN and source normalization.",
            "EXACT_BOUND_LAW_NONCLAIM",
            "dq_norm_template",
        ),
        (
            "DQV3604_3_vq_candidate",
            "v_q private/source-vector candidate",
            "v_q can be vertical only if q_private is first-class or source-silent across geometry, tau, matter, boundary and readout q-components.",
            "The current matrix marks its entries as zero-conditional, not zero-owned; source-vector/Weyl/matter/boundary tails remain live.",
            "CANDIDATE_HIGHEST_PRIORITY_NOT_CERTIFIED",
            "candidate_vertical_basis",
        ),
        (
            "DQV3604_4_memory_tau_candidate",
            "v_memory_tau candidate",
            "Private memory/time/coframe directions can be vertical only if the public tau/coframe/readout functor is fixed before clocks, source support, R10 and orbits.",
            "The same-frame rule is a guardrail, but the parent tau-frame lock is not signed.",
            "CANDIDATE_NOT_CERTIFIED",
            "field_readout_order",
        ),
        (
            "DQV3604_5_coeff_candidate",
            "v_coeff candidate",
            "Hidden coefficient directions can be vertical only if visible constants and source/current scales are q-basic constants or parent normal-form slots.",
            "Coefficient descent exists as a conditional theorem, but kappa/G/ell_J/source-scale ownership is still unsigned.",
            "CANDIDATE_NOT_CERTIFIED",
            "field_coeff_descent",
        ),
        (
            "DQV3604_6_boundary_candidate",
            "v_boundary local candidate",
            "Boundary/reference directions are at best locally vertical after fixed boundary class, zero compact flux, source-blind H_ref and corner silence.",
            "Local verticality is not enough for source-coordinate silence unless the same support/reference branch is fixed.",
            "LOCAL_CANDIDATE_NOT_CERTIFIED",
            "vertical_kernel_certificate",
        ),
        (
            "DQV3604_7_RAB_rejection",
            "v_RAB rejection under current observer map",
            "R_AB/lambda_R is not eligible for the q-basic zero theorem under the current observer-cell map because Dq[v_RAB] is nonzero unless the observer map is rebuilt or the field is constraint-eliminated first.",
            "This prevents pretending an auxiliary compatibility field is vertical by analogy.",
            "REJECTED_CURRENT_BRANCH",
            "vertical_kernel_condition",
        ),
        (
            "DQV3604_8_projector_direction",
            "delta_projector/readout obstruction",
            "delta Pi_M or readout-kernel variation is not a vertical direction unless projectors are fixed before variation or every projector derivative is retained separately.",
            "The variation-before-readout guard keeps projector movement out of q-basic zero proofs.",
            "OBSTRUCTION_NOT_VERTICAL",
            "field_signature",
        ),
        (
            "DQV3604_9_current_MTS_verdict",
            "current corpus verdict",
            "No candidate residual direction has a fully source-backed Dq[v]=0 certificate.  v_q remains the best first target, but it needs first-class/source-vector silence or a Dq leak bound.",
            "Therefore 3604 does not promote q-basic source-coordinate, H_tau, density, support, Newton, PPN, R10 or local-GR claims.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "qmap_kernel_audit",
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


def matrix_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("DQM3604_0_v_q_private", "v_q_private", "q_private representative/source-vector slot", "zero_conditional", "E_first_class+E_matter+E_boundary+E_readout", "MISSING_Q_MAP_AND_SOURCE_SILENCE", "highest", "candidate_vertical_basis"),
        ("DQM3604_1_v_memory_tau", "v_memory_tau", "private memory/time/coframe residual slots", "zero_conditional", "E_tau_lock+E_clock+E_frame+E_source_support", "MISSING_TAU_FRAME_LOCK", "medium", "candidate_vertical_basis"),
        ("DQM3604_2_v_coeff", "v_coeff", "hidden coefficient/coupling slots", "zero_conditional", "E_coeff_descent+E_source_scale+E_clock_constants", "MISSING_COEFFICIENT_DESCENT", "medium", "candidate_vertical_basis"),
        ("DQM3604_3_v_boundary", "v_boundary_reference", "boundary/corner/reference class", "local_zero_conditional", "E_boundary_flux+E_Href_source+E_corner", "MISSING_BOUNDARY_REFERENCE_SILENCE", "medium_local_only", "candidate_vertical_basis"),
        ("DQM3604_4_v_RAB", "v_RAB", "R_AB/lambda_R auxiliary compatibility field", "rejected_nonzero_current_map", "DObs_e_R+c_aux+Z_R+q_R", "REJECTED_FOR_CURRENT_OBSERVER_CELL_MAP", "rejected", "vertical_kernel_condition"),
        ("DQM3604_5_delta_projector", "delta_projector", "Pi_M/P_loc/readout kernels", "obstruction_not_vertical", "c_projector_operator+Delta_support+readout_order", "MISSING_PROJECTOR_FIXEDNESS", "medium_obstruction", "field_signature"),
        ("DQM3604_6_Y_target", "Y_target", "M_H_ref,sigma^a source coordinates", "target_not_q_primitive", "A_X=dYbar(Dq[v])+E_Y", "ANTI_TAUTOLOGY_GUARD_ACTIVE", "derived_target", "qmap_anti_tautology"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "matrix_id": matrix_id,
            "direction": direction,
            "acts_on": acts_on,
            "Dq_status": dq_status,
            "Dq_leak_bound_formula": leak_formula,
            "current_blocker": blocker,
            "candidate_priority": priority,
            "eligible_for_qbasic_zero": dq_status in {"zero_proved"},
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for matrix_id, direction, acts_on, dq_status, leak_formula, blocker, priority, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("DQB3604_0_total", "epsilon_Dq_total", "max_i ||Dq[v_i]||_q/||v_i|| or declared component norm envelope", "q_component_norm", "MISSING_ACTUAL_DQ_MATRIX", "component Dq entries for every candidate direction; no cancellation across q-components", "dq_matrix_skeleton", "BOUND_REQUIRED_CRITICAL"),
        ("DQB3604_1_v_q_private", "epsilon_Dq_vq", "||Dq[v_q]||_q/||v_q|| <= E_first_class+E_matter+E_boundary+E_readout", "q_component_norm", "MISSING_VQ_DQ_NORM", "first-class/source-vector silence, matter descent, boundary silence and readout no-reentry", "dq_norm_template", "BOUND_REQUIRED_HIGHEST_PRIORITY"),
        ("DQB3604_2_v_memory_tau", "epsilon_Dq_memory_tau", "||Dq[v_memory]|| <= E_tau_lock+E_clock+E_frame+E_source_support", "q_component_norm", "MISSING_MEMORY_TAU_DQ_NORM", "public tau/coframe/readout functor and source-support lock", "dq_norm_template", "BOUND_REQUIRED"),
        ("DQB3604_3_v_coeff", "epsilon_Dq_coeff", "||Dq[v_coeff]|| <= E_coeff_descent+E_source_scale+E_clock_constants", "q_component_norm", "MISSING_COEFF_DQ_NORM", "coefficient descent theorem, parent normal form and no source-scale laundering", "dq_norm_template", "BOUND_REQUIRED"),
        ("DQB3604_4_v_boundary", "epsilon_Dq_boundary", "||Dq[v_boundary]||_local <= E_boundary_flux+E_Href_source+E_corner", "q_component_norm", "MISSING_BOUNDARY_DQ_NORM", "fixed boundary class, zero compact flux, source-blind H_ref and corner silence", "dq_norm_template", "BOUND_REQUIRED_LOCAL_ONLY"),
        ("DQB3604_5_v_RAB", "epsilon_Dq_RAB", "Dq[v_RAB] retained nonzero unless observer-cell map rebuilt or constraint-first elimination is proved", "q_component_norm", "REJECTED_NOT_NUMERIC", "new observer-cell map or constraint-first elimination; otherwise do not use q-basic theorem", "dq_norm_template", "REJECTED_BOUND_REQUIRED_IF_REUSED"),
        ("DQB3604_6_delta_projector", "epsilon_Dq_projector", "||Dq[delta Pi_M]|| <= c_projector_operator+Delta_support+readout_order", "projector_readout_norm", "MISSING_PROJECTOR_FIXEDNESS", "Pi_M/P_loc fixed before variation or projector derivative retained", "field_signature", "BOUND_REQUIRED_OBSTRUCTION"),
        ("DQB3604_7_q_parent_definition", "epsilon_q_parent", "q(Phi)=Q_vis projection ownership defect", "q_definition_norm", "MISSING_PARENT_OWNED_QMAP", "parent q definition and field list before tests; cannot define by deleting failed couplings", "qmap_kernel_audit", "BOUND_REQUIRED_CRITICAL"),
        ("DQB3604_8_Ax_transfer", "epsilon_AX_from_Dq", "||dYbar|| epsilon_Dq + E_Y", "source_coordinate_connection_norm", "NOT_SCORE_READY_TRANSFER", "feeds AXB3603_0 only after dYbar norm and E_Y rows are source-backed", "bounds_3603", "TRANSFER_ROW_NONCLAIM"),
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
        ("PROM3604_0_vertical_matrix_criterion", "Dq matrix verticality criterion", "PASS_EXACT_CRITERION", "v is vertical only if every q-component derivative vanishes on the same branch", "dq_matrix_skeleton"),
        ("PROM3604_1_Dq_bound_law", "Dq leak bound law", "PASS_EXACT_BOUND_LAW", "unsigned verticality becomes epsilon_Dq component bounds with no cancellation", "dq_norm_template"),
        ("PROM3604_2_current_vertical_basis_claim", "current vertical basis certificate", "FAIL_CURRENT_CLAIM", "no candidate direction has source-backed Dq[v]=0 across all q-components", "candidate_vertical_basis"),
        ("PROM3604_3_vq_priority", "v_q route priority", "PASS_ROUTE_SELECTED", "v_q is the highest-priority candidate but requires first-class/source-vector silence or Dq leak bound", "dq_norm_template"),
        ("PROM3604_4_RAB_guard", "R_AB rejected under current observer map", "PASS_GUARD", "v_RAB cannot be used in q-basic zero theorems unless the observer map is rebuilt or constraint-first elimination is proved", "vertical_kernel_condition"),
        ("PROM3604_5_anti_tautology_guard", "Y not primitive q", "PASS_GUARD", "source coordinates are derived targets, not q-map components inserted to force A_X=0", "qmap_anti_tautology"),
        ("PROM3604_6_no_Newton_GR_claim", "Newton/PPN/local-GR promotion", "FAIL_CURRENT_CLAIM", "q-basic source-coordinate/H_tau/density/support zeros stay conditional while Dq matrix is unsigned", "status_3603"),
        ("PROM3604_7_bound_pack", "Dq bound pack complete", "PASS_NONCLAIM", "all candidate direction rows are source-ready but not score-ready", "bounds_3603"),
        ("PROM3604_8_next_target", "next target selected", "PASS_ROUTE_SELECTED", "attack v_q first-class/source-vector silence or fill epsilon_Dq_vq bound", "field_residual_split"),
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
            "status": "ACTUAL_QMAP_VERTICAL_BASIS_UNSIGNED_DQ_LEAK_BOUNDS_INSTALLED",
            "strongest_result": "3604 turns verticality into an explicit Dq matrix problem: v is in ker(Dq) only if every q-component derivative vanishes on the same branch. No candidate direction currently passes; v_q is the best first attack, while v_RAB is rejected under the current observer map.",
            "decision": "keep q-basic zero theorems conditional, retain epsilon_Dq rows for v_q, v_memory_tau, v_coeff, v_boundary, v_RAB and delta_projector, and move next to the v_q first-class/source-vector silence proof or bound",
            "still_missing": "parent-owned q definition, residual basis action, Dq entries, first-class/source-vector silence for v_q, tau/frame lock for memory directions, coefficient descent, compact boundary/reference silence, projector fixedness and a declared q-component norm",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["dq_matrix_skeleton"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3604_0",
            "target_doc": "3605-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md",
            "target_script": "scripts/Y5_R2FR_3605_vq_first_class_source_vector_silence_or_Dq_vq_bound.py",
            "objective": "try to prove v_q is first-class/source-silent across geometry, tau, matter, boundary and readout q-components; if not, retain epsilon_Dq_vq with B_qW, C_qT, matter, boundary and readout tail bounds",
            "success_gate": "v_q can enter q-basic zero theorems only if Dq[v_q]=0 is parent-owned on the same q map, or if a source-backed epsilon_Dq_vq bound is available",
            "reason": "3604 identifies v_q as the highest-priority candidate direction and the first Dq leak row feeding A_X and local-GR closure",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    matrix: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3604_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3604 source paths exist"))
    validations.append(("VAL3604_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3604 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3604_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3604 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3604_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3604_4_vertical_criterion_present", any(row["theorem_id"] == "DQV3604_1_vertical_criterion" and row["status"] == "EXACT_MATRIX_CRITERION" for row in theorem), "Dq matrix verticality criterion present"))
    validations.append(("VAL3604_5_direction_rows_present", {"v_q_private", "v_memory_tau", "v_coeff", "v_boundary_reference", "v_RAB", "delta_projector", "Y_target"}.issubset({str(row["direction"]) for row in matrix}), "all candidate direction matrix rows present"))
    validations.append(("VAL3604_6_Dq_bound_rows_present", {"epsilon_Dq_vq", "epsilon_Dq_memory_tau", "epsilon_Dq_coeff", "epsilon_Dq_boundary", "epsilon_Dq_RAB", "epsilon_Dq_projector"}.issubset({str(row["symbol"]) for row in bounds}), "all candidate Dq leak bound rows present"))
    validations.append(("VAL3604_7_no_vertical_claims", not any(str(row.get("eligible_for_qbasic_zero", "False")).lower() == "true" for row in matrix), "no direction is certified eligible for q-basic zero"))
    validations.append(("VAL3604_8_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3604_2_current_vertical_basis_claim", "PROM3604_6_no_Newton_GR_claim"]), "vertical basis and Newton/GR claims are blocked"))
    validations.append(("VAL3604_9_RAB_guard", any(row["gate_id"] == "PROM3604_4_RAB_guard" and row["status"] == "PASS_GUARD" for row in gates), "R_AB rejection guard present"))
    validations.append(("VAL3604_10_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, matrix, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3604_11_next_target_selected", any(row["next_id"] == "NEXT3604_0" for row in next_target), "3605 v_q target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, matrix, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3604_12_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3604*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3604-") or path.name.startswith("Y5_R2FR_3604") or "P8_Y5_R2FR_3604" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3604_13_formalization_workbench_untouched", len(formal_hits) == 0, "no 3604 checkpoint output appears in formalization-workbench outside package/venv noise"))
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


def write_doc(theorem, matrix, bounds, gates, status, next_target, validation) -> None:
    lines = [
        "# 3604 - actual qmap vertical basis or Dq leak bound",
        "",
        "## Verdict",
        "3604 turns `Dq(v_X)=0` from a slogan into a matrix gate.  A direction is vertical only when every q-component derivative vanishes on the same parent q-map and branch.",
        "",
        "No candidate direction passes that gate yet.  `v_q` is the best first attack, `v_memory_tau`, `v_coeff`, and `v_boundary` are conditional, `delta_projector` is an obstruction rather than a vertical direction, and `v_RAB` is rejected under the current observer-cell map.",
        "",
        "The useful nonzero law is now `epsilon_Dq[v] := ||Dq[v]||_q/||v|| <= sum_a epsilon_a[v]`.  This is the row that feeds the 3603 `A_X` bound instead of pretending verticality is already proven.",
        "",
        "## Qmap Vertical Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Direction Matrix Audit"])
    for row in matrix:
        lines.append(f"- `{row['matrix_id']}` / `{row['direction']}`: {row['Dq_status']} - {row['Dq_leak_bound_formula']}")
    lines.extend(["", "## Dq Leak Bound Rows"])
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
    matrix = matrix_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["vertical_theorem"], theorem)
    write_csv(out_paths["direction_matrix"], matrix)
    write_csv(out_paths["dq_leak_bounds"], bounds)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, matrix, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, matrix, bounds, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
