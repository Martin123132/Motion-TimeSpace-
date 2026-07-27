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

DOC = ROOT / "2887-Y5-R2FR-observed-coframe-functor-or-Cobs-source-row-under-AX1090.md"

SRC_2886_DOC = ROOT / "2886-Y5-R2FR-Qvis-parent-signature-or-first-finite-DqZ-component-row-under-AX1090.md"
SRC_2886_NEXT = RESIDUALS / "P8_Y5_R2FR_2886_NEXT_TARGET.csv"
SRC_2886_COMPONENT = RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv"
SRC_2886_INPUTS = RESIDUALS / "P8_Y5_R2FR_2886_COMPONENT_INPUT_REQUIREMENTS.csv"
SRC_2886_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2886_VALIDATION.csv"

SRC_1671_COBS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_COBS_FACTOR_INPUT_ROWS.csv"
SRC_1674_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"

SRC_2487_KERNEL = RESIDUALS / "P8_Y5_OBS_COFRAME_2487_DOBS_KERNEL_GATE.csv"
SRC_2487_LEAK = RESIDUALS / "P8_Y5_OBS_COFRAME_2487_FINITE_DOBS_LEAK_ROWS.csv"
SRC_2571_KERNEL = RESIDUALS / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv"
SRC_2571_LEAK = RESIDUALS / "P8_Y5_OBS_COFRAME_2571_FINITE_DOBS_LEAK_ROWS.csv"

SRC_2633_GATE = RESIDUALS / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv"
SRC_2633_THEOREM = RESIDUALS / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv"
SRC_2643_GATE = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_2214_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_DQZ_SOURCE_DESCENT_PROOF_ATTEMPT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2887_SOURCE_REGISTER.csv",
    "functor": RESIDUALS / "P8_Y5_R2FR_2887_OBSERVED_COFRAME_FUNCTOR_AUDIT.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2887_DOBS_KERNEL_THEOREM_ATTEMPT.csv",
    "cobs": RESIDUALS / "P8_Y5_R2FR_2887_COBS_OPERATOR_NORM_ROW_NONCLAIM.csv",
    "update": RESIDUALS / "P8_Y5_R2FR_2887_E_DQZ_COFRAME_COMPONENT_UPDATE.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2887_COBS_ARENA_LINKS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2887_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2887_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2887_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2887_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2887_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2887_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "cobs_copy": SOURCE_WEIGHT / "RAB_COBS_OPERATOR_NORM_ROW_2887_NONCLAIM.csv",
    "component_copy": LOCAL_BOUNDS / "RAB_E_DQZ_COFRAME_COMPONENT_UPDATE_2887_NONCLAIM.csv",
    "arena_copy": BETA_DOCS / "RAB_COBS_ARENA_LINKS_2887_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2887_terminal_public_coframe_no_shadow_NEXT.csv",
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
        ("SRC2887_0_2886_doc", SRC_2886_DOC, "Status: `Y5_R2FR_2886_Qvis_parent_signature_unsigned_E_DqZ_coframe_component_2887_next`;## Next Target", "2886 handoff"),
        ("SRC2887_1_2886_next", SRC_2886_NEXT, "NEXT2886_0_2887", "explicit 2887 target"),
        ("SRC2887_2_2886_component", SRC_2886_COMPONENT, "DQC2886_0_E_DqZ_coframe;E_DqZ_coframe", "E_DqZ coframe component"),
        ("SRC2887_3_2886_inputs", SRC_2886_INPUTS, "REQ2886_0_Obs_e;REQ2886_1_Cobs", "component input requirements"),
        ("SRC2887_4_2886_validation", SRC_2886_VALIDATION, "VAL2886_OVERALL", "2886 validation"),
        ("SRC2887_5_1671_cobs", SRC_1671_COBS, "COBS1671_0_operator_norm;COBS1671_2_shadow_frame_guard", "Cobs factor input rows"),
        ("SRC2887_6_1674_matrix", SRC_1674_MATRIX, "DQM1674_0_coframe_metric;MISSING_OBSERVED_COFRAME_FUNCTOR", "DqZ coframe derivative row"),
        ("SRC2887_7_2487_kernel", SRC_2487_KERNEL, "DOK2487_0_exact_kernel;DOK2487_3_current_verdict", "observed coframe kernel gate 2487"),
        ("SRC2887_8_2487_leak", SRC_2487_LEAK, "DLEAK2487_0_vZ;DLEAK2487_4_common_frame_abs", "finite observed coframe leak rows 2487"),
        ("SRC2887_9_2571_kernel", SRC_2571_KERNEL, "DOK2571_0_exact_kernel;DOK2571_4_current_verdict", "observed coframe kernel gate 2571"),
        ("SRC2887_10_2571_leak", SRC_2571_LEAK, "DLEAK2571_0_q_source_readout;DLEAK2571_5_coupling_readout", "finite observed coframe leak rows 2571"),
        ("SRC2887_11_2633_gate", SRC_2633_GATE, "PNFG2633_4_quotient_DObs_no_shadow;PNFG2633_6_full_PPN_vector_closure", "parent normal DObs/EH synthesis gate"),
        ("SRC2887_12_2633_theorem", SRC_2633_THEOREM, "THM2633_3_no_shadow_to_PPN_vector;THM2633_4_local_GR_claim_gate", "conditional local-GR theorem guard"),
        ("SRC2887_13_2643_gate", SRC_2643_GATE, "QVIS2643_5_observed_descent;QVIS2643_6_verdict", "Qvis observed descent gate"),
        ("SRC2887_14_2214_descent", SRC_2214_DESCENT, "DSD2214_1_metric_coframe_channel;DSD2214_5_verdict", "metric/coframe source descent proof attempt"),
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


def functor_rows() -> list[dict[str, Any]]:
    statement = "Obs_e = E_obs(Q_vis) with metric, measure and connection inherited from the same terminal public coframe."
    specs = [
        ("OFA2887_0_target", "observed coframe functor", statement, "TARGET_EXACT", "would define C_Obs_e and let DObs_e[v_Z]=DE_obs[DQ_vis(v_Z)]", "must be parent-owned, not selected after the fact"),
        ("OFA2887_1_exact_kernel", "conditional kernel theorem", "If Obs_e=E(q_parent(Phi)) and v in ker(Dq_parent), then DObs_e[v]=0.", "PROVED_CONDITIONALLY", "2487/2571 prove the chain-rule kernel", "q_parent, E(q), ordinary readout domain and v_Z are not parent-signed simultaneously"),
        ("OFA2887_2_metric_measure_connection", "metric/measure/connection ownership", "g_obs, mu_m, D_m and the spin/metric connection inherit from Obs_e(Q_vis).", "MISSING_CONNECTION_DESCENT", "would suppress connection-level PPN/light-cone leakage", "connection/coframe ownership and hidden-frame coupling clauses unsigned"),
        ("OFA2887_3_no_shadow_frame", "no representative Weyl/disformal/source frame", "there is no independent hidden frame C_shadow that matter/readouts can see.", "MISSING_NO_SHADOW_FRAME_OR_BOUND", "would stop common-frame leakage", "C_shadow remains a live finite residual route"),
        ("OFA2887_4_source_coupling", "source/coupling readout follows coframe", "Hilbert mass/source, kappa_MTS, ell_J and visible coefficients are q-basic or separately bounded.", "MISSING_SOURCE_COUPLING_DESCENT", "would protect Newton/GM and source normalization from coframe hiding", "2571 keeps coupling_readout_abs live"),
        ("OFA2887_5_boundary_endpoint", "boundary/reference endpoint silence", "boundary, reference, corner and endpoint coframe data have zero local projection or finite bounds.", "BOUNDARY_ENDPOINT_SILENCE_NOT_PARENT_SIGNED", "would prevent endpoint leakage into clocks/PPN/orbits", "2487/2571 endpoint rows remain missing"),
        ("OFA2887_6_verdict", "Obs_e(Q_vis) parent functor", "all rows above close together", "OBSERVED_COFRAME_FUNCTOR_NOT_PARENT_SIGNED", "do not claim DObs_e kernel zero or C_Obs_e value", "stage C_Obs_e source-ready row"),
    ]
    return [
        add_common(
            {
                "functor_id": functor_id,
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
        for functor_id, clause, formal, status, if_signed, blocker in specs
    ]


def kernel_rows() -> list[dict[str, Any]]:
    specs = [
        ("DOK2887_0_exact", "DObs_e[v]=DE_obs[Dq(v)]", "exact chain-rule statement if Obs_e=E_obs(q)", "EXACT_CONDITIONAL_THEOREM", "useful but conditional"),
        ("DOK2887_1_vZ", "DObs_e[v_Z]=0", "would follow from v_Z in ker(Dq) and terminal Obs_e", "NOT_ADOPTED", "Dq_Z_norm and Q_vis verticality remain unsigned"),
        ("DOK2887_2_Cobs_zero", "C_Obs_e_on_im_DqZ=0", "annihilator route if DObs_e kills im(Dq[v_Z])", "NOT_ADOPTED", "image basis and annihilator certificate missing"),
        ("DOK2887_3_Cobs_finite", "C_Obs_e finite row", "operator norm row is source-ready if q/e norms and E_obs derivative are declared", "SOURCE_READY_TEMPLATE_VALUE_MISSING", "no numeric/source-backed bound available"),
        ("DOK2887_4_verdict", "DObs/Cobs kernel verdict", "derive or fill C_Obs_e", "KERNEL_ZERO_NOT_SIGNED_COBS_VALUE_NOT_FILLED", "stage C_Obs_e as nonclaim operator row"),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "target": target,
                "mathematical_statement": statement,
                "current_status": status,
                "reason": reason,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for kernel_id, target, statement, status, reason in specs
    ]


def cobs_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "COBS2887_0_operator_norm",
                "symbol": "C_Obs_e",
                "definition": "operator norm ||DObs_e||_{q->e} for the observed coframe/metric/measure/connection functor",
                "units": "dimensionless after q/e norm declarations; arena-specific mapping supplies PPN/clock/orbital units",
                "value_type": "theorem_zero_or_source_backed_interval_required",
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_1671_COBS}; {SRC_2487_KERNEL}; {SRC_2571_KERNEL}; {SRC_2633_GATE}",
                "required_source_inputs": "Obs_e(Q_vis); q norm; e norm; derivative DE_obs; no-shadow-frame certificate; connection/measure descent; boundary endpoint guard",
                "projection_formula": "E_DqZ_coframe <= Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z + E_theta_coframe + E_readout_coframe + E_boundary_coframe",
                "current_status": "SOURCE_READY_TEMPLATE_VALUE_MISSING",
                "promotion_rule": "promote only if Obs_e is parent-signed and C_Obs_e is theorem-zero/finite with no MISSING_* markers; coframe-only success still cannot claim local GR",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "row_id": "COBS2887_1_annihilator",
                "symbol": "C_Obs_e_on_im_DqZ",
                "definition": "operator norm of DObs_e restricted to im(Dq[v_Z])",
                "units": "dimensionless coframe response factor",
                "value_type": "annihilator_certificate_or_source_bound_required",
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_1671_COBS}; {SRC_1674_MATRIX}; {SRC_2487_KERNEL}",
                "required_source_inputs": "image basis for Dq_Z; DObs_e derivative; proof DObs_e kills image or finite bound",
                "projection_formula": "if C_Obs_e_on_im_DqZ=0 then coframe-mediated E_DqZ vanishes, but direct tails remain",
                "current_status": "MISSING_IMAGE_DQZ_AND_ANNIHILATOR_CERTIFICATE",
                "promotion_rule": "may kill coframe leak only, not source/readout/boundary tails",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "row_id": "COBS2887_2_shadow_frame_guard",
                "symbol": "C_shadow",
                "definition": "operator norm for representative Weyl/disformal/source/readout frame leakage not captured by Obs_e(Q_vis)",
                "units": "dimensionless",
                "value_type": "no_shadow_theorem_or_finite_bound_required",
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_1671_COBS}; {SRC_2571_LEAK}; {SRC_2633_THEOREM}",
                "required_source_inputs": "terminal public coframe theorem; no extra Weyl/disformal/common-frame grammar; finite b_g/d_R/w_R envelope if not zero",
                "projection_formula": "E_DqZ_coframe_total <= C_Obs_e*Dq_Z_norm*N_Z + C_shadow + endpoint/readout tails",
                "current_status": "MISSING_NO_SHADOW_FRAME_OR_BOUND",
                "promotion_rule": "must be independently zeroed/bounded before PPN/clock/local-GR scoring",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def update_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "EDQZ2887_0_component_update",
                "component_id": "DQC2886_0_E_DqZ_coframe",
                "symbol": "E_DqZ_coframe",
                "previous_status": "NONCLAIM_COMPONENT_DEFINED_NUMERIC_VALUE_MISSING",
                "new_information": "C_Obs_e is now a source-ready operator-norm row, but Obs_e(Q_vis), no-shadow frame, q/e norms and direct tails remain unsigned",
                "updated_formula": "E_DqZ_coframe <= Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z + C_shadow + E_theta_coframe + E_readout_coframe + E_boundary_coframe",
                "current_value": "MISSING_COMPONENT_VALUES",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "current_status": "COMPONENT_SCHEMA_SHARPENED_COBS_VALUE_MISSING",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2887_0_R0_WEP", "R0/WEP", "eta_AB <= Pi_R0(C_Obs_e*Dq_Z_norm*N_Z + C_shadow + source/marker tails)", "MISSING_PI_R0_AND_COBS_VALUE"),
        ("ARENA2887_1_PPN", "PPN gamma/beta", "Delta_PPN <= Pi_PPN(C_Obs_e*Dq_Z_norm*N_Z + C_shadow + endpoint/readout tails)", "MISSING_PPN_PROJECTION_AND_NO_SHADOW"),
        ("ARENA2887_2_R11", "R11/EH operator", "DeltaE_R11 <= Pi_R11(C_Obs_e*Dq_Z_norm*N_Z)", "MISSING_R11_OPERATOR_PROJECTION"),
        ("ARENA2887_3_clock", "clock/time", "Delta_clock <= Pi_clock(C_Obs_e*Dq_Z_norm*N_Z + theta/readout tails)", "MISSING_CLOCK_READOUT_DESCENT"),
        ("ARENA2887_4_orbital", "orbital/GM", "Delta_orbit <= Pi_orbit(C_Obs_e*Dq_Z_norm*N_Z + source-current tail)", "MISSING_ORBITAL_READOUT_AND_SOURCE_GUARD"),
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
        ("GATE2887_0_Obs_e", "Obs_e(Q_vis) parent functor is signed", "FAIL", "conditional theorem exists but parent q/E/readout domain/v_Z are not signed together"),
        ("GATE2887_1_Cobs", "C_Obs_e is theorem-zero or finite/source-backed", "FAIL", "operator norm row is source-ready but value remains missing"),
        ("GATE2887_2_no_shadow", "no-shadow/common-frame guard is zero or bounded", "FAIL", "C_shadow remains missing"),
        ("GATE2887_3_component_score", "E_DqZ_coframe can score", "FAIL", "C_Obs_e, Dq_Z_norm, N_Z, Pi_coframe and direct tails remain missing"),
        ("GATE2887_4_local_claim", "coframe result proves local GR/Newton", "FAIL", "coframe-only success would still not close source/readout/boundary/physical-lock gates"),
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
                "runner_id": "RUN2887_0_cobs_runner",
                "status": "REFUSED_COBS_VALUE_AND_NO_SHADOW_MISSING",
                "accepted_functors": 0,
                "accepted_cobs_rows": 0,
                "accepted_arena_rows": 0,
                "reason": "C_Obs_e row is source-ready but contains MISSING_* markers; no coframe arena comparison is allowed",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2887_0_functor", "OBS_E_FUNCTOR_NOT_PARENT_SIGNED", "2487/2571 give the exact conditional kernel theorem, but current MTS does not sign q_parent, E_obs, v_Z and readout domain together.", "do not adopt DObs_e[v_Z]=0"),
        ("DEC2887_1_cobs", "INSTALL_COBS_OPERATOR_ROW", "The first coframe component now has a concrete operator-norm slot rather than an unnamed blocker.", "use C_Obs_e/C_shadow rows as the next acquisition interface"),
        ("DEC2887_2_next", "SELECT_TERMINAL_PUBLIC_COFRAME_NO_SHADOW", "The highest leverage route is to prove there is no representative common-frame/Weyl/disformal shadow outside the terminal public coframe.", "try no-shadow certificate or finite C_shadow bound next"),
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
                "next_id": "NEXT2887_0_2888",
                "status": "selected_primary",
                "target_doc": "2888-Y5-R2FR-terminal-public-coframe-no-shadow-or-Cshadow-bound-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_terminal_public_coframe_no_shadow_or_Cshadow_bound_row_under_AX1090_2888.py",
                "mission": "try to derive the terminal public coframe/no-shadow certificate that makes C_shadow=0 and protects Obs_e(Q_vis); if it fails, fill a source-ready nonclaim C_shadow/common-frame bound row with units and arena projections",
                "forbidden_shortcuts": "no coframe-only local-GR claim; no C_shadow=0 from preferred ansatz; no numeric bound without source-backed operator/norm; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2887_0_cobs_copy", OUTPUTS["cobs"], BRANCH_OUTPUTS["cobs_copy"], "source-weight copy of C_Obs_e/C_shadow operator rows"),
        ("BR2887_1_component_copy", OUTPUTS["update"], BRANCH_OUTPUTS["component_copy"], "local-bounds copy of E_DqZ coframe component update"),
        ("BR2887_2_arena_copy", OUTPUTS["arena"], BRANCH_OUTPUTS["arena_copy"], "beta-source docs copy of Cobs arena links"),
        ("BR2887_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
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
    functor = rows_by_name["functor"]
    kernel = rows_by_name["kernel"]
    cobs = rows_by_name["cobs"]
    update = rows_by_name["update"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2887_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2887_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2887_2_functor_unsigned", any(row["current_status"] == "OBSERVED_COFRAME_FUNCTOR_NOT_PARENT_SIGNED" for row in functor), "observed coframe functor is not parent-signed"),
        ("VAL2887_3_kernel_not_adopted", any(row["current_status"] == "KERNEL_ZERO_NOT_SIGNED_COBS_VALUE_NOT_FILLED" for row in kernel), "DObs kernel zero is not adopted"),
        ("VAL2887_4_cobs_rows", len(cobs) == 3 and cobs[0]["symbol"] == "C_Obs_e" and cobs[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO", "C_Obs_e and guard rows are staged nonclaim"),
        ("VAL2887_5_component_updated", update[0]["current_status"] == "COMPONENT_SCHEMA_SHARPENED_COBS_VALUE_MISSING", "E_DqZ_coframe component was sharpened but not scored"),
        ("VAL2887_6_arena_nonclaim", len(arena) == 5 and all(row["comparison_ready"] is False for row in arena), "Cobs arena links are mapped but not scored"),
        ("VAL2887_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2887_8_runner_refused", runner[0]["status"] == "REFUSED_COBS_VALUE_AND_NO_SHADOW_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2887_9_next_target_2888", next_target[0]["next_id"] == "NEXT2887_0_2888" and next_target[0]["selected"] is True, "2888 target selected"),
        ("VAL2887_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2887_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2887_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2887_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2887_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2887_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2887_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2887_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2887 retained the exact conditional DObs kernel theorem, refused to parent-sign Obs_e(Q_vis) or C_Obs_e, staged C_Obs_e/C_shadow operator rows, and selected terminal public coframe no-shadow or C_shadow bound for 2888.",
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
    text = f"""# 2887 - Y5 R2FR Observed Coframe Functor Or Cobs Source Row Under AX1090

Status: `Y5_R2FR_2887_Obs_e_functor_unsigned_Cobs_Cshadow_rows_2888_next`

## Private Verdict

2887 tests the observed-coframe route.

There is a clean conditional theorem already in the corpus:

`Obs_e=E_obs(q_parent(Phi))` and `v in ker(Dq_parent)` imply `DObs_e[v]=DE_obs[Dq_parent[v]]=0`.

That is real mathematical structure, but it is not yet a parent-signed local-GR result. Current evidence still does not sign `q_parent`, terminal `E_obs`, ordinary readout domain, `v_Z`, connection/measure descent, no-shadow frame, and boundary endpoint silence together.

So `C_Obs_e` is not assigned a value and no coframe-only victory lap is allowed. The useful progress is sharper plumbing: `C_Obs_e`, `C_Obs_e_on_im_DqZ`, and `C_shadow` are now explicit source-ready nonclaim operator rows feeding the existing `E_DqZ_coframe` component.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Observed Coframe Functor Audit

{md_table(rows_by_name["functor"], ["functor_id", "clause", "current_status", "if_signed", "current_blocker", "parent_signed", "valid_for_claim"])}

## DObs Kernel Theorem Attempt

{md_table(rows_by_name["kernel"], ["kernel_id", "target", "current_status", "reason", "valid_for_claim"])}

## Cobs Operator Norm Rows

{md_table(rows_by_name["cobs"], ["row_id", "symbol", "definition", "candidate_value", "upper_bound", "current_status", "valid_for_claim"])}

## E DqZ Coframe Component Update

{md_table(rows_by_name["update"], ["update_id", "symbol", "new_information", "updated_formula", "current_status", "valid_for_claim"])}

## Cobs Arena Links

{md_table(rows_by_name["arena"], ["arena_id", "arena", "projection_formula", "current_status", "comparison_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_functors", "accepted_cobs_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "functor": functor_rows(),
        "kernel": kernel_rows(),
        "cobs": cobs_rows(),
        "update": update_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2887_OVERALL")
    print(f"VAL2887_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
