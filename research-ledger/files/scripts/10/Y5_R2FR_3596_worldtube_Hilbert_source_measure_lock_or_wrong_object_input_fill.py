from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3596"
BRANCH_ID = "MTS_R2FR_Y5_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK_3596"
DOC = ROOT / "3596-Y5-R2FR-worldtube-Hilbert-source-measure-lock-or-wrong-object-input-fill.md"


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
        "next_3595": (RESIDUALS / "P8_Y5_R2FR_3595_NEXT_TARGET.csv", "NEXT3595_0"),
        "status_3595": (
            RESIDUALS / "P8_Y5_R2FR_3595_STATUS.csv",
            "CONDITIONAL_HILBERT_TO_TOPO_GLUE_DERIVED_WRONG_OBJECT_BOUND_ACTIVE",
        ),
        "glue_3595": (
            RESIDUALS / "P8_Y5_R2FR_3595_HILBERT_TO_TOPOLOGICAL_GLUE_THEOREM.csv",
            "HGT3595_4_worldtube_dressed_source",
        ),
        "wrong_3595": (
            RESIDUALS / "P8_Y5_R2FR_3595_WRONG_OBJECT_RESIDUAL_DECOMPOSITION.csv",
            "R_worldtube",
        ),
        "bounds_3595": (
            RESIDUALS / "P8_Y5_R2FR_3595_EPSILON_PIM_PARENT_WRONG_OBJECT_BOUND_ROWS.csv",
            "epsilon_EM_once",
        ),
        "validation_3595": (
            RESIDUALS / "P8_Y5_BRR545_3595_VALIDATION.csv",
            "VAL3595_12_formalization_workbench_untouched",
        ),
        "worldtube_theorem": (
            RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "T510_1_worldtube_source_measure",
        ),
        "worldtube_proof": (
            RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
            "P510_5",
        ),
        "worldtube_clauses": (
            RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "WG510_7_dressed_source_definition",
        ),
        "worldtube_gates": (
            RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_GATE_TESTS.csv",
            "G510_2_bare_mass_guardrail",
        ),
        "worldtube_decision": (
            RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_DECISION.csv",
            "D510_2",
        ),
        "parent_noether": (
            RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
            "T505_source_measure_matching",
        ),
        "parent_noether_chain": (
            RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "D505_6_worldtube_readout",
        ),
        "source_measure_theorem": (
            RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            "T509_0_charge_identity_needed",
        ),
        "em_hodge_bound": (
            RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
            "EMB3503_6_Delta_J_total",
        ),
        "em_current_source": (
            RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
            "CSR3508_4_postvariation_rescaling",
        ),
        "em_ellj_law": (
            RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
            "EJR3513_6_R_W",
        ),
        "q_map": (
            RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
            "QMAP3517_8_projector_readout",
        ),
        "kappa_gref_lock": (
            RESIDUALS / "P8_EM_fixed_kappa_Gref_action_line_lock.csv",
            "KGLR3511_2_delta_ellJ",
        ),
        "charge_direct": (
            RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            "CC7_closed_flux_and_Gauss_calibration",
        ),
        "charge_residuals": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_cal",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3596_SOURCE_REGISTER.csv",
        "source_measure_lock": RESIDUALS / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv",
        "residual_decomposition": RESIDUALS / "P8_Y5_R2FR_3596_QM_WORLD_TUBE_EM_RESIDUAL_DECOMPOSITION.csv",
        "input_rows": RESIDUALS / "P8_Y5_R2FR_3596_QM_WORLD_TUBE_EM_INPUT_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3596_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3596_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3596_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_worldtube_Hilbert_source_measure_lock_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3596_VALIDATION.csv",
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


def lock_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "WSL3596_0_target",
            "3596 target",
            "Lock Q_M=ell_M(Pi_M J_H)=M_source[W] as a dressed Hilbert/Hamiltonian source measure, or retain epsilon_Qlabel/epsilon_worldtube/epsilon_EM_once.",
            "3595 showed the topological route is only legal if Q_M is not an independent label.",
            "TARGET_IMPORTED",
            "next_3595",
        ),
        (
            "WSL3596_1_dressed_definition",
            "dressed source definition",
            "M_source^dress[W;tau] := H_tau[S_outer] - H_tau[S_ref]",
            "The source mass used by gravity is the Hamiltonian/Noether charge difference, not bare rest matter. This includes gravitational binding, field dressing and boundary reference bookkeeping.",
            "DEFINITION_LOCK_CONDITIONAL",
            "worldtube_theorem",
        ),
        (
            "WSL3596_2_Hilbert_source_scalar",
            "Hilbert source scalar",
            "Q_M := ell_M(Pi_M J_H_total) := M_source^dress[W;tau]",
            "This kills the independent-label failure by defining the topological scalar from the same projected Hilbert source before orbital readout.",
            "CONDITIONAL_Q_LABEL_ZERO",
            "source_measure_theorem",
        ),
        (
            "WSL3596_3_constraint_bridge",
            "Hamiltonian constraint bridge",
            "delta H_tau = integral_W T_H,total(n,tau) + boundary/reference terms + Delta_nonEH + Delta_symp + Delta_extra + Delta_frame",
            "In EH/minimal matter this is the standard source-measure route; MTS inherits it only if non-EH and frame/projector residuals are zero or bounded.",
            "CONDITIONAL_PARENT_TRANSFER",
            "parent_noether_chain",
        ),
        (
            "WSL3596_4_EM_once",
            "EM/Poynting/binding once-only source",
            "J_H_total = J_matter + J_EM + J_Poynting + J_binding + improvements_exact_zero",
            "The Poynting vector is not decoration: radiative/background EM flux and binding energy must enter the Hilbert source once, not zero times and not twice.",
            "OPEN_CRITICAL_GUARD",
            "em_hodge_bound",
        ),
        (
            "WSL3596_5_readout_order",
            "readout after variation",
            "J_parent := delta S/delta e_obs and T_parent := delta S/delta g before readout; orbital GM cannot define Q_M.",
            "This prevents a post-fit mass calibration from masquerading as a source theorem.",
            "ANTI_TAUTOLOGY_GUARD",
            "em_current_source",
        ),
        (
            "WSL3596_6_conditional_lock_theorem",
            "worldtube-Hilbert-source lock theorem",
            "If H_tau is parent integrable, tau/source frame/reference are fixed, Pi_M is fixed before variation, extra sectors have zero mass charge, and J_H_total includes EM/Poynting/binding once, then Q_M=ell_M(Pi_M J_H_total)=M_source^dress[W;tau].",
            "This is the cleanest route from topology to actual source mass. It is conditional, not a current local-GR pass.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "worldtube_proof",
        ),
        (
            "WSL3596_7_current_MTS_verdict",
            "current corpus verdict",
            "The definition can be adopted as the only non-cheat branch, but current MTS has not parent-signed H_tau integrability, same source frame, extra-sector silence, EM once-only accounting, or Gauss/orbital calibration.",
            "So epsilon_Qlabel is conditionally zero if the branch is adopted; epsilon_worldtube and epsilon_EM_once remain active nonclaim inputs.",
            "PARTIAL_LOCK_REMAINING_INPUTS_ACTIVE",
            "worldtube_decision",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "lock_id": lock_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for lock_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def residual_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("WMR3596_0_total", "R_worldtube_total", "M_source^dress[W;tau] - ell_M(Pi_M J_H_total)", "total source-measure mismatch", "ACTIVE_NONCLAIM", "wrong_3595"),
        ("WMR3596_1_Qlabel", "R_Qlabel", "Q_M - ell_M(Pi_M J_H_total)", "independent topological label not sourced by Hilbert current", "CONDITIONAL_ZERO_IF_DEFINITION_ADOPTED", "glue_3595"),
        ("WMR3596_2_Htau_integrability", "R_Htau", "curl(delta H_tau) or nonintegrable boundary symplectic term", "Hamiltonian charge not a source scalar unless integrable", "OPEN_BOUND_REQUIRED", "em_ellj_law"),
        ("WMR3596_3_reference", "R_ref", "D_X H_ref/(H_tau-H_ref)", "reference subtraction/source-blindness not signed", "OPEN_BOUND_REQUIRED", "em_ellj_law"),
        ("WMR3596_4_worldtube_support", "R_W", "D_X ln W_source - D_X ln closure(supp J_H[tau])", "worldtube/support selector drift", "OPEN_BOUND_REQUIRED", "em_ellj_law"),
        ("WMR3596_5_frame_tau", "R_frame_tau", "source/readout frame or tau mismatch", "same observed frame/time must apply to source, clocks and orbits", "OPEN_FRAME_BLOCKER", "q_map"),
        ("WMR3596_6_extra_charge", "R_extra_charge", "Delta_nonEH + Delta_symp + Delta_extra + Delta_frame", "MTS charge differs from EH/Hilbert charge through extra sectors", "OPEN_MTS_TRANSFER_BLOCKER", "worldtube_theorem"),
        ("WMR3596_7_EM_once", "R_EM_once", "Pi_M[J_H_total - J_matter - J_EM - J_Poynting - J_binding]", "EM/Poynting/binding source accounting not closed", "OPEN_CRITICAL_GUARD", "em_hodge_bound"),
        ("WMR3596_8_Gref_units", "R_Gref_units", "mismatch in G_ref, ell_J, action-line, or source units", "same coupling normalization must be used before readout", "OPEN_PRODUCT_LOCK", "kappa_gref_lock"),
        ("WMR3596_9_calibration_downstream", "R_calibration", "M_source^dress - M_Gauss_orbital", "source lock still needs Poisson/Gauss/orbital calibration", "DOWNSTREAM_OPEN", "charge_direct"),
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


def input_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("WIN3596_0_epsilon_Qlabel", "epsilon_Qlabel", "abs(Q_M-ell_M(Pi_M J_H_total))/abs(M_H_ref)", "dimensionless", "0 if Q_M is definitionally ell_M(Pi_M J_H_total) in parent action; otherwise missing", "parent-owned Q_M definition before readout", "glue_3595", "CONDITIONAL_ZERO_BRANCH"),
        ("WIN3596_1_epsilon_worldtube", "epsilon_worldtube", "abs(M_source^dress[W;tau]-ell_M(Pi_M J_H_total))/abs(M_H_ref)", "dimensionless", "MISSING_PARENT_SOURCE_MEASURE_LOCK", "H_tau integrability, source worldtube/support selector, reference subtraction, tau/frame lock", "worldtube_theorem", "BOUND_REQUIRED"),
        ("WIN3596_2_epsilon_Htau", "epsilon_Htau_integrability", "abs(curl(delta H_tau))/abs(M_H_ref)", "dimensionless or source-charge curl units", "MISSING_HTAU_INTEGRABILITY_BOUND", "symplectic potential, boundary flux, reference terms, source path", "em_ellj_law", "BOUND_REQUIRED"),
        ("WIN3596_3_epsilon_ref", "epsilon_reference_source_blind", "abs(D_X H_ref)/abs(H_tau-H_ref)", "dimensionless", "MISSING_REFERENCE_SOURCE_BLINDNESS", "reference topology/asymptotic coframe proof or derivative bound", "em_ellj_law", "BOUND_REQUIRED"),
        ("WIN3596_4_epsilon_W", "epsilon_worldtube_support", "abs(D_X ln W_source - D_X ln closure(supp J_H[tau]))", "dimensionless", "MISSING_WORLDTUBE_SUPPORT_LOCK", "source support selector theorem or domain/support bound", "em_ellj_law", "BOUND_REQUIRED"),
        ("WIN3596_5_epsilon_frame_tau", "epsilon_frame_tau", "abs(R_frame_tau)", "dimensionless", "MISSING_SAME_SOURCE_FRAME_TAU_THEOREM", "single q/e_obs/tau branch for source, clocks, orbits, references", "q_map", "BOUND_REQUIRED"),
        ("WIN3596_6_epsilon_EM_once", "epsilon_EM_once", "abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding])/abs(M_H_ref)", "dimensionless EM source-accounting residual", "MISSING_ONCE_ONLY_EM_STRESS_ACCOUNTING", "Hilbert EM stress, Poynting flux, binding energy and no-double-count proof", "em_hodge_bound", "BOUND_REQUIRED_CRITICAL"),
        ("WIN3596_7_epsilon_Gref_units", "epsilon_Gref_units", "abs(R_Gref_units)", "dimensionless", "MISSING_GREF_ELLJ_ACTION_LINE_LOCK", "G_ref/ell_J/action-line/source-unit parent lock", "kappa_gref_lock", "BOUND_REQUIRED"),
        ("WIN3596_8_epsilon_source_measure_total", "epsilon_source_measure_total", "sum of epsilon_Qlabel, epsilon_worldtube, epsilon_Htau, epsilon_ref, epsilon_W, epsilon_frame_tau, epsilon_EM_once, epsilon_Gref_units", "dimensionless", "NOT_SCORE_READY_TOTAL", "all component zeros or numeric/source-backed bounds", "bounds_3595", "TOTAL_BOUND_BRANCH_ACTIVE"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
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
        for input_id, symbol, formula, units, current_value, required_inputs, source_id, score_status in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3596_0_Qlabel", "Q_M independent-label failure", "PASS_CONDITIONAL_ZERO_BRANCH", "zero only if Q_M is parent-defined as ell_M(Pi_M J_H_total)", "glue_3595"),
        ("PROM3596_1_worldtube_lock", "M_source[W]=ell_M(Pi_M J_H_total)", "FAIL_CURRENT_CLAIM", "H_tau/reference/support/frame/extra-sector premises remain open", "worldtube_clauses"),
        ("PROM3596_2_EM_once", "EM/Poynting/binding included once", "FAIL_CURRENT_CLAIM", "critical Poynting/source-accounting row remains open", "em_hodge_bound"),
        ("PROM3596_3_bound_pack", "source-measure input rows complete", "PASS_NONCLAIM", "inputs are source-ready but not numeric/score-ready", "bounds_3595"),
        ("PROM3596_4_no_Newton_claim", "no measured-GM/Newton/PPN/local-GR promotion", "PASS_GUARD", "Gauss/orbital calibration remains downstream", "charge_residuals"),
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
            "status": "QM_LABEL_CONDITIONALLY_ZERO_WORLDTUBE_EM_ONCE_INPUTS_ACTIVE",
            "strongest_result": "3596 locks the non-cheat definition: Q_M may be identified with ell_M(Pi_M J_H_total) only when M_source[W] is the dressed Hamiltonian/Noether source charge before orbital readout. This conditionally kills the independent topological-label failure, but current MTS still lacks parent-signed H_tau integrability, reference/source support, same frame/tau, extra-sector charge silence, and EM/Poynting/binding once-only accounting.",
            "decision": "adopt the dressed-source definition as the only viable branch, keep epsilon_worldtube and epsilon_EM_once active, and do not claim Newton/PPN/local-GR until Gauss/orbital calibration and EM source accounting are closed",
            "still_missing": "H_tau integrability, H_ref source-blindness, worldtube support selector, same source frame/tau, extra-sector charge silence, EM/Poynting/binding once-only Hilbert source map, G_ref/ell_J units lock, Gauss/orbital calibration",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["worldtube_theorem"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3596_0",
            "target_doc": "3597-Y5-R2FR-EM-Poynting-Hilbert-source-accounting-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3597_EM_Poynting_Hilbert_source_accounting_or_bound.py",
            "objective": "prove that EM stress, Poynting flux, and binding energy enter J_H_total exactly once in the source-measure branch, or fill epsilon_EM_once/Phi_EM_rad/source-accounting bound rows",
            "success_gate": "visible EM/Poynting contribution is owned by the same Hilbert source current before Pi_M and readout, with no missing radiative flux and no double count; otherwise source-backed nonclaim bounds remain active",
            "reason": "3596 makes the dressed source definition the viable route, but EM/Poynting once-only accounting is now the most physics-critical open source-measure component",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    lock: list[dict[str, object]],
    residuals: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3596_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3596 source paths exist"))
    validations.append(("VAL3596_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3596 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3596_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3596 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3596_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3596_4_definition_lock_present", any(row["lock_id"] == "WSL3596_1_dressed_definition" and row["status"] == "DEFINITION_LOCK_CONDITIONAL" for row in lock), "dressed source definition lock row present"))
    validations.append(("VAL3596_5_Qlabel_conditional_zero", any(row["symbol"] == "epsilon_Qlabel" and row["score_status"] == "CONDITIONAL_ZERO_BRANCH" for row in inputs), "epsilon_Qlabel has conditional-zero branch"))
    validations.append(("VAL3596_6_worldtube_EM_inputs_active", {"epsilon_worldtube", "epsilon_EM_once", "epsilon_source_measure_total"}.issubset({str(row["symbol"]) for row in inputs}), "worldtube and EM once inputs are active"))
    validations.append(("VAL3596_7_EM_once_claim_blocked", any(row["gate_id"] == "PROM3596_2_EM_once" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "EM/Poynting once-only claim remains blocked"))
    validations.append(("VAL3596_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [lock, residuals, inputs, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3596_9_no_local_gr_claim", any(row["gate_id"] == "PROM3596_4_no_Newton_claim" and row["status"] == "PASS_GUARD" for row in gates), "measured-GM/Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3596_10_next_target_selected", any(row["next_id"] == "NEXT3596_0" for row in next_target), "3597 EM/Poynting source accounting target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [lock, residuals, inputs, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3596_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = list(FORMALIZATION.rglob("*3596*")) if FORMALIZATION.exists() else []
    validations.append(("VAL3596_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3596 checkpoint output appears in formalization-workbench"))
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


def write_doc(lock, residuals, inputs, gates, status, next_target, validation) -> None:
    lines = [
        "# 3596 - Worldtube Hilbert source measure lock or wrong-object input fill",
        "",
        "## Verdict",
        "3596 locks the only non-cheat definition: `Q_M` can stop being a wrong topological label only if it is defined as `ell_M(Pi_M J_H_total)=M_source^dress[W;tau]` before orbital readout.",
        "",
        "This conditionally kills the independent-label failure, but not the whole source-coupling problem.  `H_tau` integrability, reference/source support, same frame/tau, extra-sector silence, and especially EM/Poynting/binding once-only accounting remain live.",
        "",
        "## Source-Measure Lock",
    ]
    for row in lock:
        lines.append(f"- `{row['lock_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Residual Decomposition"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Input Rows"])
    for row in inputs:
        lines.append(f"- `{row['input_id']}` / `{row['symbol']}`: {row['score_status']} - {row['formula']}")
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
    lock = lock_rows(source_map)
    residuals = residual_rows(source_map)
    inputs = input_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["source_measure_lock"], lock)
    write_csv(out_paths["residual_decomposition"], residuals)
    write_csv(out_paths["input_rows"], inputs)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, lock, residuals, inputs, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(lock, residuals, inputs, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
