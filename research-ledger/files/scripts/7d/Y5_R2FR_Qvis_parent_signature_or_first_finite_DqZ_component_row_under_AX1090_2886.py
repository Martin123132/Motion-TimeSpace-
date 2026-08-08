from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2886-Y5-R2FR-Qvis-parent-signature-or-first-finite-DqZ-component-row-under-AX1090.md"

SRC_2885_DOC = ROOT / "2885-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill-under-AX1090.md"
SRC_2885_NEXT = RESIDUALS / "P8_Y5_R2FR_2885_NEXT_TARGET.csv"
SRC_2885_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_ZERO_THEOREM_CONTRACT.csv"
SRC_2885_LEAKS = RESIDUALS / "P8_Y5_R2FR_2885_SURVIVING_LEAK_ACQUISITION_ROWS.csv"
SRC_2885_FACTOR = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv"
SRC_2885_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2885_VALIDATION.csv"

SRC_2644_VECTOR = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_FINITE_JH_DQZ_VECTOR_CONTRACT.csv"
SRC_2644_GATES = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_CLAIM_GATES.csv"
SRC_2644_DECISION = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_DECISION_LEDGER.csv"

SRC_2645_ATTEMPT = RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv"
SRC_2645_COMPONENT = RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_FIRST_XI_JH_DQZ_COMPONENT_ROW_NONCLAIM.csv"

SRC_2615_HILBERT = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
SRC_2614_SPECIES = RESIDUALS / "P8_Y5_SPECIES_FORGETTING_GATE_2614_SOURCE_ZERO_STATUS.csv"
SRC_2635_UNIVERSAL = RESIDUALS / "P8_Y5_UNIVERSAL_PROPERTY_HUNT_2635_SOURCE_HUNT_VERDICT.csv"

SRC_2214_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_DQZ_SOURCE_DESCENT_PROOF_ATTEMPT.csv"
SRC_2643_GATE = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_1671_COBS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_COBS_FACTOR_INPUT_ROWS.csv"
SRC_1674_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2886_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_2886_QVIS_PARENT_SIGNATURE_AUDIT.csv",
    "collapse": RESIDUALS / "P8_Y5_R2FR_2886_QVIS_COLLAPSE_THEOREM_ATTEMPT.csv",
    "component": RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv",
    "inputs": RESIDUALS / "P8_Y5_R2FR_2886_COMPONENT_INPUT_REQUIREMENTS.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2886_ARENA_COMPONENT_LINKS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2886_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2886_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2886_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2886_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2886_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2886_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "component_copy": LOCAL_BOUNDS / "RAB_FIRST_FINITE_DQZ_COMPONENT_ROW_2886_NONCLAIM.csv",
    "input_copy": SOURCE_WEIGHT / "RAB_DQZ_COMPONENT_INPUT_REQUIREMENTS_2886_NONCLAIM.csv",
    "arena_copy": BETA_DOCS / "RAB_DQZ_COMPONENT_ARENA_LINKS_2886_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2886_observed_coframe_functor_or_Cobs_row_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2886_0_2885_doc", SRC_2885_DOC, "Status: `Y5_R2FR_2885_DqZ_zero_not_closed_factor_value_blocker_2886_Qvis_next`;## Next Target", "2885 handoff"),
        ("SRC2886_1_2885_next", SRC_2885_NEXT, "NEXT2885_0_2886", "explicit 2886 target"),
        ("SRC2886_2_2885_contract", SRC_2885_CONTRACT, "DZC2885_5_source_readout;DZC2885_9_verdict", "DqZ theorem contract"),
        ("SRC2886_3_2885_leaks", SRC_2885_LEAKS, "LEAK2885_0_coframe;LEAK2885_5_residual_lock", "surviving leak ledger"),
        ("SRC2886_4_2885_factor", SRC_2885_FACTOR, "DQZF2885_0_Dq_Z_norm;DQZF2885_2_C_Obs_e", "factor blocker ledger"),
        ("SRC2886_5_2885_validation", SRC_2885_VALIDATION, "VAL2885_OVERALL", "2885 validation"),
        ("SRC2886_6_2644_vector", SRC_2644_VECTOR, "FJV2644_0_master_vector;FJV2644_3_E_DqZ", "Qvis finite vector contract"),
        ("SRC2886_7_2644_gates", SRC_2644_GATES, "CG2644_0_Qvis_signature;CG2644_3_finite_vector_score", "Qvis claim gates"),
        ("SRC2886_8_2644_decision", SRC_2644_DECISION, "DEC2644_0_main_result;DEC2644_2_fallback", "Qvis decision ledger"),
        ("SRC2886_9_2645_attempt", SRC_2645_ATTEMPT, "NSP2645_0_target;NSP2645_7_verdict", "no-source-prefactor parent clause attempt"),
        ("SRC2886_10_2645_component", SRC_2645_COMPONENT, "XIC2645_1_Delta_w_species;XIC2645_3_DqZ_injection", "first Xi component row"),
        ("SRC2886_11_2615_hilbert", SRC_2615_HILBERT, "THO2615_3_source_shadow_ban;THO2615_5_owner_verdict", "total Hilbert source owner audit"),
        ("SRC2886_12_2614_species", SRC_2614_SPECIES, "SZ2614_1_no_w_A;SZ2614_5_local_GR", "species forgetting/source-zero status"),
        ("SRC2886_13_2635_universal", SRC_2635_UNIVERSAL, "SHV2635_0_overall;SHV2635_2_repetition_guard", "universal-property hunt verdict"),
        ("SRC2886_14_2214_descent", SRC_2214_DESCENT, "DSD2214_0_exact_chain_rule;DSD2214_5_verdict", "DqZ source descent proof attempt"),
        ("SRC2886_15_2643_gate", SRC_2643_GATE, "QVIS2643_1_visible_quotient;QVIS2643_6_verdict", "common descent parent signature gate"),
        ("SRC2886_16_1671_cobs", SRC_1671_COBS, "COBS1671_0_operator_norm;COBS1671_2_shadow_frame_guard", "Cobs input rows"),
        ("SRC2886_17_1674_matrix", SRC_1674_MATRIX, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "DqZ component derivative matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def signature_rows() -> list[dict[str, Any]]:
    statement = (
        "Ordinary matter, constants, source normalization, readouts and boundary/projector data "
        "are constructed only from Q_vis, and all selected v_Z directions are either eliminated "
        "before Q_vis or vertical for Q_vis."
    )
    specs = [
        ("QVS2886_0_exact_signature", "Q_vis parent signature target", statement, "TARGET_EXACT", "would make Dq_Z, eps_JH_Z_abs, theta/source/readout and boundary direct terms collapse together", "must be parent grammar, not an ansatz"),
        ("QVS2886_1_parent_chart", "field chart and live/eliminated sort", "Phi=(Q_vis,Z,gauge,theta,source/readout,boundary) with declared constructor order", "NOT_PARENT_SIGNED", "required before v_Z or Dq_Z can be evaluated", "2885 keeps parent chart and computable q missing"),
        ("QVS2886_2_qvis_constructor", "Q_vis constructor list", "Q_vis=(e_obs,g_obs,mu_m,D_m,source/readout data,theta_owned,A_owned) with no representative Z arguments", "MINIMAL_ANSATZ_ONLY", "would give DQ_vis[v_Z]=0", "2643/2644 keep object-language constructor list unsigned"),
        ("QVS2886_3_no_source_prefactor", "no source-only/action prefactor", "w_A(Z)S_A, kappa_A(Z)T_A and source-only species weights are ill-typed or common-mode only", "NOT_DERIVED", "would collapse Delta_w_species and source side of Xi_JH_DqZ_A", "2645 keeps pre-action weighted countermodel alive"),
        ("QVS2886_4_total_hilbert_owner", "single total Hilbert source owner", "ordinary source is delta S_matter/delta Q_vis after one common action/measure owner is fixed", "CONDITIONAL_NOT_EXCLUSIVE", "would prevent post-readout source-shadow selection", "2615 keeps source-shadow/non-Hilbert bypass open"),
        ("QVS2886_5_no_marker_theta", "no marker/theta hidden slot", "theta, material labels and standards are quotient/superselection data, not Z-dependent source labels", "NO_MARKER_THEOREM_NOT_SIGNED", "would collapse clock/EM/WEP marker tails", "2643 and 2644 retain marker coefficients"),
        ("QVS2886_6_readout_stability", "readout-after-variation stability", "clock, photon, orbit, PPN and EM readouts are functors of Q_vis and cannot reintroduce representative labels", "READOUT_DESCENT_UNSIGNED", "would collapse E_readout_A", "2214 and 2885 retain readout terms"),
        ("QVS2886_7_boundary_projector", "boundary/projector descent", "proper boundary primitives, source worldtube corners and local projectors are Q_vis-owned or separately bounded", "BOUNDARY_PROJECTOR_UNSIGNED", "would collapse boundary_projector_A", "1675/2214/2885 keep boundary/projector terms live"),
        ("QVS2886_8_universal_property", "global no-extension/universal property", "no legal parent constructor exists outside Q_vis for ordinary local matter/source/readout data", "NO_CLAIM_GRADE_SOURCE_FOUND", "would close the whole Q_vis route at once", "2635 says do not retry without new source evidence"),
        ("QVS2886_9_verdict", "parent-sign Q_vis", "all clauses close in one parent branch", "QVIS_PARENT_SIGNATURE_NOT_SIGNED", "do not claim Dq_Z/J_H/source/readout collapse", "fallback to finite component rows"),
    ]
    return [
        add_common(
            {
                "signature_id": signature_id,
                "clause": clause,
                "formal_statement": formal,
                "current_status": status,
                "if_signed": if_signed,
                "current_blocker": blocker,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for signature_id, clause, formal, status, if_signed, blocker in specs
    ]


def collapse_rows() -> list[dict[str, Any]]:
    specs = [
        ("QVC2886_0_chain_rule", "exact conditional collapse", "delta_vZ S_matter = D Sbar[DQ_vis(v_Z)] + J_theta Lie_vZ(theta) + J_direct[Z] + delta_vZ B", "EXACT_CONDITIONAL_ONLY", "2214/2643 support the formula but not all zero clauses"),
        ("QVC2886_1_DqZ", "Dq_Z collapse", "DQ_vis(v_Z)=0 implies C_A_obs*Dq_Z_norm*N_Z=0", "NOT_ADOPTED", "Q_vis constructor, v_Z basis and q/Z norms unsigned"),
        ("QVC2886_2_JH", "Hilbert source leak collapse", "eps_JH_Z_abs=0 if matter source descends through Q_vis and no source-only prefactor exists", "NOT_ADOPTED", "no-source-prefactor and total-source owner not parent-signed"),
        ("QVC2886_3_theta_source_readout", "direct theta/source/readout collapse", "J_theta Lie_Z(theta), Delta_w, qbar_marker and E_readout terms vanish", "NOT_ADOPTED", "theta/no-marker, source-label forgetting and readout stability unsigned"),
        ("QVC2886_4_boundary", "boundary/projector collapse", "delta_vZ B=0 and local projector terms descend through Q_vis", "NOT_ADOPTED", "boundary/projector no-flux not signed"),
        ("QVC2886_5_verdict", "Qvis collapse theorem", "all collapse heads are zero in one branch", "COLLAPSE_THEOREM_NOT_CLOSED", "install first finite DqZ component row"),
    ]
    return [
        add_common(
            {
                "collapse_id": collapse_id,
                "target": target,
                "mathematical_statement": statement,
                "current_status": status,
                "failure_reason": reason,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for collapse_id, target, statement, status, reason in specs
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "component_id": "DQC2886_0_E_DqZ_coframe",
                "vector": "Xi_JH_DqZ_A",
                "symbol": "E_DqZ_coframe",
                "component": "observed coframe/metric/measure/connection descent leak",
                "formula": "E_DqZ_coframe <= Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z + E_theta_coframe + E_readout_coframe + E_boundary_coframe",
                "coefficient_origin": "LEAK2885_0_coframe plus FJV2644_3_E_DqZ and DQM1674_0_coframe_metric",
                "units": "dimensionless coframe/metric residual after declared q/e/Z norms, or mapped PPN/metric units per arena",
                "current_value": "MISSING_COMPONENT_VALUES",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "status": "NONCLAIM_COMPONENT_DEFINED_NUMERIC_VALUE_MISSING",
                "source_paths": f"{SRC_2885_LEAKS}; {SRC_2644_VECTOR}; {SRC_1671_COBS}; {SRC_1674_MATRIX}",
                "required_to_score": "Obs_e(Q_vis); C_Obs_e operator norm; Dq_Z_norm or theorem-zero; N_Z; Pi_coframe arena map; theta/readout/boundary tail zeros or source-backed bounds",
                "arenas": "R0_WEP;PPN_gamma_beta;R11_operator;clock_metric_bridge;orbital_metric_readout",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def input_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2886_0_Obs_e", "Obs_e(Q_vis)", "observed coframe/metric functor", "MISSING_OBSERVED_COFRAME_FUNCTOR", "derive observed coframe from Q_vis or declare finite functor row", "blocks C_Obs_e and coframe arena projection"),
        ("REQ2886_1_Cobs", "C_Obs_e", "operator norm ||DObs_e||_{q->e}", "MISSING_OPERATOR_NORM", "source-backed theorem-zero, finite interval, or norm convention", "blocks E_DqZ_coframe upper bound"),
        ("REQ2886_2_DqZ", "Dq_Z_norm", "operator norm ||Dq[v_Z]||/||v_Z||", "MISSING_NUMERIC_OR_THEOREM_ZERO", "Q_vis vertical theorem or finite Dq matrix/norm", "blocks all DqZ-mediated components"),
        ("REQ2886_3_NZ", "N_Z", "selected Z tangent normalization", "MISSING_Z_DIRECTION_NORMALIZATION", "unified Z basis and selected direction", "blocks factor product normalization"),
        ("REQ2886_4_Pi_coframe", "Pi_coframe", "arena projection from coframe leak to observable residual", "MISSING_ARENA_PROJECTION", "R0/PPN/R11/clock/orbital projection row", "blocks comparison to local tests"),
        ("REQ2886_5_direct_tails", "E_theta/readout/boundary_coframe", "additive tails not mediated by Dq_Z", "MISSING_DIRECT_TAIL_ZERO_OR_BOUNDS", "independent theorem-zero or finite coefficient rows", "no-cancellation guard forbids hiding them"),
    ]
    return [
        add_common(
            {
                "requirement_id": requirement_id,
                "symbol": symbol,
                "definition": definition,
                "current_status": status,
                "next_input": next_input,
                "why_needed": why_needed,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for requirement_id, symbol, definition, status, next_input, why_needed in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2886_0_R0_WEP", "R0/WEP source-frame coframe route", "eta_AB or source-frame residual <= Pi_R0(E_DqZ_coframe + Delta_w + marker tails)", "MISSING_PI_R0_AND_COMPONENT_VALUES"),
        ("ARENA2886_1_PPN", "PPN gamma/beta/common frame", "Delta_gamma,Delta_beta <= Pi_PPN(E_DqZ_coframe) plus no-other-channel guard", "MISSING_COBS_DQZ_PI_PPN"),
        ("ARENA2886_2_R11", "R11/EH operator local residual", "operator residual <= Pi_R11(C_Obs_e*Dq_Z_norm*N_Z)", "MISSING_R11_OPERATOR_PROJECTION"),
        ("ARENA2886_3_clock", "clock/time metric readout", "Delta_clock <= Pi_clock(E_DqZ_coframe + theta/readout standard tails)", "MISSING_CLOCK_READOUT_DESCENT"),
        ("ARENA2886_4_orbital", "orbital metric/GM readout", "Delta_orbit <= Pi_orbit(E_DqZ_coframe + source-current tail)", "MISSING_ORBITAL_READOUT_AND_GM_GUARD"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "projection_formula": formula,
                "current_status": status,
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "accepted_for_scoring": False,
            }
        )
        for arena_id, arena, formula, status in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2886_0_Qvis_signed", "Q_vis parent signature is signed", "FAIL", "constructor list, no-source-prefactor, no-marker/readout and boundary clauses remain unsigned"),
        ("GATE2886_1_collapse", "Dq_Z/J_H/theta/source/readout/boundary collapse together", "FAIL", "only exact conditional chain rule is available"),
        ("GATE2886_2_component_defined", "first finite DqZ component row is defined", "PASS_NONCLAIM", "E_DqZ_coframe row exists but contains missing values and cannot score"),
        ("GATE2886_3_component_score", "first component row is numeric/source-backed", "FAIL", "C_Obs_e, Dq_Z_norm, N_Z, Pi_coframe and direct tails are missing"),
        ("GATE2886_4_local_claim", "local GR/Newton/PPN/WEP claim follows", "FAIL", "physical lock and source/readout/coupling gates remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2886_0_component_runner",
                "status": "REFUSED_QVIS_UNSIGNED_COMPONENT_VALUES_MISSING",
                "accepted_qvis_signatures": 0,
                "accepted_component_rows": 0,
                "accepted_arena_rows": 0,
                "reason": "E_DqZ_coframe is defined as a nonclaim component row, but value/projection inputs are missing",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2886_0_signature", "QVIS_PARENT_SIGNATURE_NOT_SIGNED", "The exact route is clear, but current evidence keeps the parent grammar and no-source/no-marker/readout/boundary clauses unsigned.", "do not adopt DqZ/JH collapse"),
        ("DEC2886_1_component", "INSTALL_E_DQZ_COFRAME_COMPONENT_ROW", "LEAK2885_0_coframe is the first surviving DqZ-mediated component and maps naturally into PPN/R0/R11/clock/orbital tests.", "use it as the first finite nonclaim component row"),
        ("DEC2886_2_next", "SELECT_OBSERVED_COFRAME_FUNCTOR_OR_COBS_ROW", "The first missing input for the new component is Obs_e(Q_vis)/C_Obs_e; without it no coframe branch can score.", "derive observed coframe functor or fill C_Obs_e source row next"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2886_0_2887",
                "status": "selected_primary",
                "target_doc": "2887-Y5-R2FR-observed-coframe-functor-or-Cobs-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_observed_coframe_functor_or_Cobs_source_row_under_AX1090_2887.py",
                "mission": "derive Obs_e(Q_vis) and C_Obs_e for the first E_DqZ_coframe component, or fill a source-ready nonclaim C_Obs_e/operator-norm row with units, projection requirements, and explicit blockers",
                "forbidden_shortcuts": "no Qvis signature from ansatz alone; no coframe-only local-GR claim; no numeric C_Obs_e without source-backed norm; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2886_0_component_copy", OUTPUTS["component"], BRANCH_OUTPUTS["component_copy"], "local-bounds copy of first finite DqZ component row"),
        ("BR2886_1_input_copy", OUTPUTS["inputs"], BRANCH_OUTPUTS["input_copy"], "source-weight copy of component input requirements"),
        ("BR2886_2_arena_copy", OUTPUTS["arena"], BRANCH_OUTPUTS["arena_copy"], "beta-source docs copy of arena component links"),
        ("BR2886_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows = []
    for copy_id, source, destination, purpose in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    signature = rows_by_name["signature"]
    collapse = rows_by_name["collapse"]
    component = rows_by_name["component"]
    inputs = rows_by_name["inputs"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2886_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2886_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2886_2_signature_audited", len(signature) == 10 and any(row["current_status"] == "QVIS_PARENT_SIGNATURE_NOT_SIGNED" for row in signature), "Q_vis parent signature is audited and unsigned"),
        ("VAL2886_3_collapse_not_adopted", any(row["current_status"] == "COLLAPSE_THEOREM_NOT_CLOSED" for row in collapse), "collapse theorem is not adopted"),
        ("VAL2886_4_component_row_defined", component[0]["symbol"] == "E_DqZ_coframe" and component[0]["status"] == "NONCLAIM_COMPONENT_DEFINED_NUMERIC_VALUE_MISSING", "first finite DqZ component row is defined as nonclaim"),
        ("VAL2886_5_component_values_missing", component[0]["current_value"] == "MISSING_COMPONENT_VALUES" and component[0]["upper_bound"] == "MISSING_SOURCE_BACKED_UPPER_BOUND", "component row cannot score"),
        ("VAL2886_6_inputs_blocked", len(inputs) == 6 and all("MISSING" in row["current_status"] for row in inputs), "component input requirements remain explicit blockers"),
        ("VAL2886_7_arena_nonclaim", len(arena) == 5 and all(row["comparison_ready"] is False for row in arena), "arena component links are mapped but not scored"),
        ("VAL2886_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2886_9_runner_refused", runner[0]["status"] == "REFUSED_QVIS_UNSIGNED_COMPONENT_VALUES_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2886_10_next_target_2887", next_target[0]["next_id"] == "NEXT2886_0_2887" and next_target[0]["selected"] is True, "2887 target selected"),
        ("VAL2886_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2886_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2886_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2886_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2886_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2886_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2886_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2886_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2886 refused to parent-sign Q_vis from unsigned grammar clauses, installed E_DqZ_coframe as the first finite nonclaim DqZ component row, and selected observed coframe functor/C_Obs_e for 2887.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2886 - Y5 R2FR Qvis Parent Signature Or First Finite DqZ Component Row Under AX1090

Status: `Y5_R2FR_2886_Qvis_parent_signature_unsigned_E_DqZ_coframe_component_2887_next`

## Private Verdict

2886 tests the best single-stroke route: parent-sign `Q_vis` so ordinary matter, sources, constants, readouts, and boundary/projector data all descend through one visible quotient.

If this signed, it would be a serious leap: `Dq_Z`, `eps_JH_Z_abs`, theta/material marker leakage, source-prefactor leakage, readout leakage, and boundary/projector leakage would collapse together.

It does not sign from the current corpus. The exact grammar is written, but the parent field chart, constructor list, no-source-prefactor clause, total Hilbert owner exclusivity, no-marker theorem, readout stability, and boundary/projector descent are still unsigned together.

So 2886 takes the fallback seriously instead of circling: it installs the first concrete finite nonclaim component row, `E_DqZ_coframe`, sourced from the 2885 coframe leak, 2644 finite-vector contract, 1671 `C_Obs_e` rows, and 1674 DqZ component matrix.

This is not a local-GR/Newton/PPN/WEP pass. It is the next scoreable skeleton once `Obs_e(Q_vis)`, `C_Obs_e`, `Dq_Z_norm`, `N_Z`, direct tails, and arena projections are sourced or derived.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Qvis Parent Signature Audit

{md_table(rows_by_name["signature"], ["signature_id", "clause", "current_status", "if_signed", "current_blocker", "parent_signed", "valid_for_claim"])}

## Qvis Collapse Theorem Attempt

{md_table(rows_by_name["collapse"], ["collapse_id", "target", "current_status", "failure_reason", "valid_for_claim"])}

## First Finite DqZ Component Row

{md_table(rows_by_name["component"], ["component_id", "symbol", "component", "formula", "current_value", "upper_bound", "status", "valid_for_claim"])}

## Component Input Requirements

{md_table(rows_by_name["inputs"], ["requirement_id", "symbol", "definition", "current_status", "next_input", "why_needed", "valid_for_claim"])}

## Arena Component Links

{md_table(rows_by_name["arena"], ["arena_id", "arena", "projection_formula", "current_status", "comparison_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_qvis_signatures", "accepted_component_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "signature": signature_rows(),
        "collapse": collapse_rows(),
        "component": component_rows(),
        "inputs": input_rows(),
        "arena": arena_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2886_OVERALL")
    print(f"VAL2886_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
