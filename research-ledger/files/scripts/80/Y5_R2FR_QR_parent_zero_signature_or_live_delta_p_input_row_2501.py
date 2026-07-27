from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_QR_PARENT_ZERO_OR_LIVE_DELTA_P_INPUT_2501"
CHECKPOINT_ID = "2501"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QR_RAW = ROOT / "source-intake" / "qr-hat" / "raw"
QR_ACCEPTED = ROOT / "source-intake" / "qr-hat" / "accepted"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

RAW_QRHAT = QR_RAW / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"

DOC = ROOT / "2501-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-input-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2501_SOURCE_REGISTER.csv",
    "parent_zero": OUT / "P8_Y5_NO_SHADOW_2501_QR_PARENT_ZERO_SIGNATURE_AUDIT.csv",
    "live_input": OUT / "P8_Y5_NO_SHADOW_2501_LIVE_DELTA_P_QRHAT_INPUT_ROW.csv",
    "input_validation": OUT / "P8_Y5_NO_SHADOW_2501_DELTA_P_INPUT_VALIDATION.csv",
    "ppn_vector": OUT / "P8_Y5_NO_SHADOW_2501_PPN_VECTOR_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2501_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2501_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2501_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2501_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2501_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_zero": LOCAL_BOUNDS / "QR_parent_zero_signature_audit_2501_NONCLAIM.csv",
    "live_input": LOCAL_BOUNDS / "Live_delta_p_qRhat_input_row_2501_NONCLAIM.csv",
    "input_validation": LOCAL_BOUNDS / "Delta_p_input_validation_2501_NONCLAIM.csv",
    "ppn_vector": LOCAL_BOUNDS / "PPN_vector_binding_status_2501_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2501_PARENT_HCORE_QR_SOURCE_EQUATION_OR_BOUNDARY_CHARGE_OWNER.csv",
}

SOURCES = [
    {
        "source_id": "SRC2501_00_2500_handoff",
        "source_path": ROOT / "2500-Y5-R2FR-delta-p-beta-disformal-PPN-vector-or-parent-no-shadow-proof.md",
        "needles": ["NEXT2500_0_selected", "DPP2500_1_zero_flux_lemma", "VAL2500_OVERALL"],
        "role": "current handoff selecting Q_R parent-zero or live delta_p input row",
    },
    {
        "source_id": "SRC2501_01_1884_contract",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "DPQR1884_2_delta_p", "VAL1884_OVERALL"],
        "role": "delta_p/q_R_hat bridge and strict input contract",
    },
    {
        "source_id": "SRC2501_02_1240_zero_attempt",
        "source_path": OUT / "P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
        "needles": ["ZQR1240_5_verdict", "ZERO_CHARGE_THEOREM_NOT_DERIVED"],
        "role": "earlier Q_R zero-charge theorem failure map",
    },
    {
        "source_id": "SRC2501_03_1255_doc",
        "source_path": ROOT / "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md",
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "not an MTS prediction", "VAL1255_13_overall"],
        "role": "first live q_R_hat raw row as nonclaim Cassini ceiling",
    },
    {
        "source_id": "SRC2501_04_qrhat_raw",
        "source_path": RAW_QRHAT,
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "phenomenological_upper_bound_not_theory_prediction"],
        "role": "raw live nonclaim q_R_hat ceiling row",
    },
    {
        "source_id": "SRC2501_05_1249_candidate_results",
        "source_path": OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
        "needles": ["ACCEPTED_NONCLAIM_FINITE_QRHAT", "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM"],
        "role": "finite q_R_hat validator acceptance snapshot",
    },
    {
        "source_id": "SRC2501_06_1249_policy_results",
        "source_path": OUT / "P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv",
        "needles": ["READY_NONCLAIM_NUMERIC_PASS", "2.3e-05"],
        "role": "nonclaim gamma smoke policy result",
    },
    {
        "source_id": "SRC2501_07_1244_gm",
        "source_path": OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
        "needles": ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)"],
        "role": "GM/source normalization convention for raw Q_R conversion",
    },
    {
        "source_id": "SRC2501_08_11_cell_current",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["W partial_r R_AB = Q_R", "topological_zero_charge", "Q_R"],
        "role": "cell-current conservation and no-charge obstruction",
    },
    {
        "source_id": "SRC2501_09_2500_validation",
        "source_path": OUT / "P8_Y5_BRR545_2500_VALIDATION.csv",
        "needles": ["VAL2500_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv_first_row(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def parent_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "signature_id": "QRZ2501_0_parent_generator",
            "needed_clause": "parent reciprocal generator G_R exists before readout",
            "current_evidence": "cell-current branch gives W partial_r C_R=Q_R, but generator ownership is not parent-signed",
            "status": "GENERATOR_OWNER_UNSIGNED",
            "would_close": "defines what charge Q_R is and what symmetry/constraint could set it to zero",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2501_1_boundary_charge_zero",
            "needed_clause": "reciprocal boundary charge vanishes or is pure gauge for allowed local source class",
            "current_evidence": "1240/1884 show conservation and asymptotic flatness do not kill Q_R hair",
            "status": "BOUNDARY_CHARGE_ZERO_NOT_DERIVED",
            "would_close": "Q_R=0 in local exterior",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2501_2_source_descent",
            "needed_clause": "ordinary matter carries no reciprocal R_AB charge",
            "current_evidence": "topological/source zero-charge is named as a possible route but not derived",
            "status": "SOURCE_DESCENT_UNSIGNED",
            "would_close": "J_R integrates to zero and source bodies cannot generate Q_R",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2501_3_matter_readout_descent",
            "needed_clause": "matter/readout descends through Q_vis without Weyl, disformal, source-prefactor or endpoint re-entry",
            "current_evidence": "2488-2500 keep b_R,d_R,w_R,endpoint/readout tails as live nonclaim rows",
            "status": "MATTER_READOUT_DESCENT_UNSIGNED",
            "would_close": "delta_p/gamma channel cannot be reopened through local rods, clocks, photons or source normalization",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2501_4_projection_silence",
            "needed_clause": "boundary, endpoint, tau and PPN gauge projection silence is parent-owned",
            "current_evidence": "2500 stages endpoint/readout kernels as missing templates",
            "status": "PROJECTION_SILENCE_UNSIGNED",
            "would_close": "finite Q_R or zero theorem becomes usable in full PPN vector",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2501_5_verdict",
            "needed_clause": "current MTS parent signs Q_R=0",
            "current_evidence": "no single parent package signs generator, boundary, source, matter/readout and projection clauses together",
            "status": "QR_PARENT_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "would_close": "Q_R=0 -> C_R=0 -> delta_p=0",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def live_input_rows() -> list[dict[str, Any]]:
    raw = read_csv_first_row(RAW_QRHAT)
    exists = bool(raw)
    q_value = raw.get("q_R_hat", "MISSING_Q_R_HAT")
    try:
        q_float = float(q_value)
        delta_p_abs_bound = abs(q_float) / 2.0
        numeric_status = "FINITE_NUMERIC"
        delta_p_bound_text = f"{delta_p_abs_bound:.12e}"
    except (TypeError, ValueError):
        numeric_status = "MISSING_OR_NONNUMERIC"
        delta_p_bound_text = "MISSING_DELTA_P_BOUND"

    rows = [
        {
            "input_id": "LIVE2501_0_QRHAT1255_Cassini_ceiling",
            "source_file": str(RAW_QRHAT),
            "source_exists": RAW_QRHAT.exists(),
            "candidate_id": raw.get("candidate_id", "MISSING_CANDIDATE_ID"),
            "route_type": raw.get("route_type", "MISSING_ROUTE_TYPE"),
            "q_R_hat_value_or_bound": q_value,
            "q_R_hat_status": numeric_status,
            "delta_p_relation": "delta_p=-q_R_hat/2 for signed finite prediction; here only abs(delta_p)<=abs(q_R_hat)/2 is used",
            "delta_p_abs_bound": delta_p_bound_text,
            "input_kind": raw.get("input_kind", "MISSING_INPUT_KIND"),
            "derivation_status": raw.get("derivation_status", "MISSING_DERIVATION_STATUS"),
            "prediction_status": "PHENOMENOLOGICAL_CEILING_NOT_MTS_PREDICTION" if exists else "MISSING_LIVE_ROW",
            "full_vector_role": "guardrail_ceiling_only_not_score_ready",
            "valid_pipeline_row": exists and numeric_status == "FINITE_NUMERIC",
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "LIVE2501_1_parent_zero_template",
            "source_file": "MISSING_PARENT_QR_ZERO_SIGNATURE",
            "source_exists": False,
            "candidate_id": "QR_PARENT_ZERO_REQUIRED",
            "route_type": "parent_zero_theorem",
            "q_R_hat_value_or_bound": "0",
            "q_R_hat_status": "ZERO_ONLY_IF_PARENT_SIGNED",
            "delta_p_relation": "Q_R=0 -> C_R=0 -> delta_p=0",
            "delta_p_abs_bound": "0",
            "input_kind": "theorem_zero",
            "derivation_status": "MISSING_BOUNDARY_SOURCE_MATTER_PROJECTION_SIGNATURE",
            "prediction_status": "NOT_ACCEPTED_UNTIL_PARENT_SIGNED",
            "full_vector_role": "would_close_delta_p_component",
            "valid_pipeline_row": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "LIVE2501_2_no_live_mts_prediction",
            "source_file": str(QR_ACCEPTED),
            "source_exists": QR_ACCEPTED.exists(),
            "candidate_id": "NO_ACCEPTED_MTS_PREDICTION_ROW",
            "route_type": "finite_qR_hat_prediction",
            "q_R_hat_value_or_bound": "MISSING_PARENT_PREDICTED_QRHAT",
            "q_R_hat_status": "MISSING_MTS_PREDICTION",
            "delta_p_relation": "delta_p=-q_R_hat/2 would apply after a sourced finite prediction",
            "delta_p_abs_bound": "MISSING_PREDICTED_DELTA_P",
            "input_kind": "prediction_required",
            "derivation_status": "MISSING_PARENT_COEFFICIENT_OR_BOUNDARY_FLUX_MODEL",
            "prediction_status": "NO_LIVE_PREDICTION_ROW_ACCEPTED",
            "full_vector_role": "blocks_full_ppn_score",
            "valid_pipeline_row": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def input_validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    live = data["live_input"]
    rows = [
        {
            "validation_id": "DVAL2501_0_raw_row_exists",
            "test": "raw QRHAT1255 row exists and parses",
            "status": "PASS" if any(row["input_id"] == "LIVE2501_0_QRHAT1255_Cassini_ceiling" and row["valid_pipeline_row"] is True for row in live) else "FAIL",
            "notes": "usable as nonclaim pipeline ceiling only",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2501_1_not_prediction",
            "test": "live row is not promoted as MTS prediction",
            "status": "PASS" if any(row["prediction_status"] == "PHENOMENOLOGICAL_CEILING_NOT_MTS_PREDICTION" and row["valid_prediction_row"] is False for row in live) else "FAIL",
            "notes": "Cassini-derived ceiling cannot prove local GR",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2501_2_delta_p_bound",
            "test": "delta_p ceiling is computed only as abs(delta_p)<=abs(q_R_hat)/2",
            "status": "PASS" if any(row["input_id"] == "LIVE2501_0_QRHAT1255_Cassini_ceiling" and row["delta_p_abs_bound"] != "MISSING_DELTA_P_BOUND" for row in live) else "FAIL",
            "notes": "sign is not assigned; it is a ceiling not a prediction",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2501_3_parent_zero_rejected",
            "test": "parent zero template remains blocked",
            "status": "PASS" if any(row["input_id"] == "LIVE2501_1_parent_zero_template" and row["valid_prediction_row"] is False for row in live) else "FAIL",
            "notes": "Q_R=0 still needs parent signature",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2501_4_full_score_refused",
            "test": "no row is score-ready or claim-ready",
            "status": "PASS" if all(row["score_ready"] is False and row["valid_for_claim"] is False for row in live) else "FAIL",
            "notes": "full PPN vector still lacks beta, b_R, d_R, w_R and endpoint/readout closure",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "PVBS2501_0_delta_p",
            "input_status": "NONCLAIM_CEILING_EXISTS_NOT_PREDICTION",
            "current_input": "QRHAT1255 gives abs(q_R_hat)<=4.6e-5, hence abs(delta_p)<=2.3e-5 as a pipeline ceiling",
            "still_missing": "parent Q_R=0 theorem or parent-predicted finite q_R_hat",
            "claim_effect": "blocks local-GR/PPN score",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_1_beta",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "beta=1 theorem or finite delta_beta_total row",
            "claim_effect": "gamma/delta_p ceiling cannot imply beta",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_2_bR",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "b_R theorem-zero or finite coefficient in C_R normalization",
            "claim_effect": "no-shadow common Weyl channel remains open",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_3_dR_preferred",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "d_R preferred-frame response kernel and alpha_i bounds",
            "claim_effect": "alpha1/alpha2/preferred-frame gates remain blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_4_wR_source",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "source-prefactor zero theorem or finite source-normalization kernel",
            "claim_effect": "source/GM/beta transfer remains blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_5_endpoint_readout",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "endpoint projection, tau, measured-GM and PPN-gauge tail kernels",
            "claim_effect": "gamma/beta extraction and orbital/light-time gates remain blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2501_6_total_abs",
            "input_status": "VECTOR_NOT_SCORE_READY",
            "current_input": "one nonclaim ceiling only",
            "still_missing": "all active components zero/bounded componentwise with no cancellation shortcut",
            "claim_effect": "all PPN/local-GR claims blocked",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2501_0_internal",
            "claim": "2501 may import the QRHAT1255 ceiling as private nonclaim pipeline input",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "source-backed ceiling exists and parses, but claim flags remain false",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2501_1_parent_zero",
            "claim": "MTS parent derives Q_R=0",
            "gate_status": "BLOCKED",
            "reason": "generator, boundary charge, source descent, matter/readout descent and projection silence are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2501_2_live_prediction",
            "claim": "live q_R_hat/delta_p row is an MTS prediction",
            "gate_status": "BLOCKED",
            "reason": "QRHAT1255 is a Cassini-derived phenomenological ceiling, not a parent coefficient prediction",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2501_3_ppn_vector",
            "claim": "full PPN vector can be scored",
            "gate_status": "BLOCKED",
            "reason": "delta_p has only a ceiling; beta, b_R, d_R, w_R, endpoint/readout rows remain missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2501_4_local_GR_Newton",
            "claim": "local GR/Newton is derived",
            "gate_status": "BLOCKED",
            "reason": "Q_R parent-zero/live-prediction, beta, no-shadow and source/readout gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2501_5_no_shortcuts",
            "claim": "closure zero, comparator-only, gamma-only or cancellation-only row can pass",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "2501 keeps the live row as ceiling-only and blocks score/claim use",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2501_0_parent_zero",
            "decision": "QR_PARENT_ZERO_STILL_UNSIGNED",
            "reason": "zero-flux lemma is exact but no parent package signs Q_R=0",
            "effect": "keep Q_R=0 as the highest-leverage derivation target",
        },
        {
            "decision_id": "DEC2501_1_live_input",
            "decision": "LIVE_NONCLAIM_QRHAT_CEILING_IMPORTED",
            "reason": "QRHAT1255 exists, has no missing markers, and is accepted by the 1249 runner as nonclaim smoke",
            "effect": "the PPN pipeline has a ceiling guardrail: abs(q_R_hat)<=4.6e-5, abs(delta_p)<=2.3e-5",
        },
        {
            "decision_id": "DEC2501_2_no_prediction",
            "decision": "NO_MTS_QRHAT_PREDICTION_ROW_EXISTS",
            "reason": "the imported row is derived from the Cassini comparator rather than from parent MTS coefficients or boundary flux",
            "effect": "do not treat the ceiling as evidence that MTS passes local GR",
        },
        {
            "decision_id": "DEC2501_3_next",
            "decision": "PARENT_HCORE_QR_SOURCE_EQUATION_SELECTED_NEXT",
            "reason": "the next real leap is an equation for Q_R or boundary/source owner, not another comparator translation",
            "effect": "2502 should attempt parent H_core reciprocal source equation/boundary charge owner",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2501_0_selected",
            "selection_status": "selected",
            "target_file": "2502-Y5-R2FR-parent-Hcore-QR-source-equation-or-boundary-charge-owner.md",
            "target_script": "scripts/Y5_R2FR_parent_Hcore_QR_source_equation_or_boundary_charge_owner_2502.py",
            "task": "derive or reject the parent reciprocal H_core source equation and boundary-charge owner that would produce Q_R=0, a parent-predicted finite Q_R, or a strict no-go; keep the QRHAT1255 ceiling as nonclaim guardrail only",
            "acceptance_target": "parent-owned E_R=delta H_core/delta C_R equation with boundary/source terms, or explicit blocker naming the missing action block; no local-GR claim",
            "guardrails": "do not treat Cassini ceiling as prediction; no closure zero; no GR Schwarzschild import; no gamma-only pass; no fitted GM shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "parent_zero": OUTPUTS["parent_zero"],
        "live_input": OUTPUTS["live_input"],
        "input_validation": OUTPUTS["input_validation"],
        "ppn_vector": OUTPUTS["ppn_vector"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2501_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2501_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2501_01_parent_zero_blocked",
        any(row["signature_id"] == "QRZ2501_5_verdict" and row["status"] == "QR_PARENT_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["parent_zero"]),
        "Q_R parent-zero signature remains blocked",
    )
    add(
        "VAL2501_02_live_ceiling_imported",
        any(row["input_id"] == "LIVE2501_0_QRHAT1255_Cassini_ceiling" and row["valid_pipeline_row"] is True for row in data["live_input"]),
        "live QRHAT1255 ceiling row imported as nonclaim pipeline input",
    )
    add(
        "VAL2501_03_ceiling_not_prediction",
        any(row["prediction_status"] == "PHENOMENOLOGICAL_CEILING_NOT_MTS_PREDICTION" and row["valid_prediction_row"] is False for row in data["live_input"]),
        "Cassini ceiling is not promoted as an MTS prediction",
    )
    add(
        "VAL2501_04_delta_p_bound_computed",
        any(row["input_id"] == "LIVE2501_0_QRHAT1255_Cassini_ceiling" and row["delta_p_abs_bound"] != "MISSING_DELTA_P_BOUND" for row in data["live_input"]),
        "delta_p ceiling computed from q_R_hat ceiling without assigning sign",
    )
    add(
        "VAL2501_05_input_validation",
        all(row["status"] == "PASS" for row in data["input_validation"]),
        "input validation refuses prediction/score use",
    )
    add(
        "VAL2501_06_vector_not_score_ready",
        any(row["component_id"] == "PVBS2501_6_total_abs" and row["input_status"] == "VECTOR_NOT_SCORE_READY" for row in data["ppn_vector"]),
        "full PPN vector remains not score-ready",
    )
    add(
        "VAL2501_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "no gate allows Q_R zero, q_R_hat prediction, PPN, local-GR or Newton claim",
    )
    add(
        "VAL2501_08_next_target_written",
        any(row["route_id"] == "NEXT2501_0_selected" for row in data["next"]),
        "2502 parent Hcore QR source equation target selected",
    )
    add("VAL2501_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2501*", "*P8_Y5_NO_SHADOW_2501*", "*JR2501*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2501_10_no_formalization_artifacts", not formalization_artifacts, "no 2501 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2501_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2501_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2501_OVERALL",
        overall,
        "2501 blocks Q_R parent-zero, imports QRHAT1255 as live nonclaim ceiling, refuses prediction use, and selects parent Hcore QR source-equation next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2501 Y5 R2FR QR Parent-Zero Signature Or Live Delta_p Input Row",
        "",
        "**Status:** private nonclaim checkpoint. `Q_R=0` is still not parent-derived. However, the existing QRHAT1255 Cassini-derived row is now imported into the current local-GR branch as a live **nonclaim ceiling**.",
        "",
        "**Main result:** we do have a live finite `q_R_hat` ceiling: `abs(q_R_hat)<=4.6e-5`, hence `abs(delta_p)<=2.3e-5` under `delta_p=-q_R_hat/2`. But this is a comparator-derived ceiling, not an MTS prediction. It can test the pipeline and set a target scale; it cannot prove local GR. The next real derivation move is the parent `H_core` reciprocal source equation or boundary-charge owner.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## QR Parent-Zero Signature Audit",
        markdown_table(data["parent_zero"], ["signature_id", "needed_clause", "current_evidence", "status", "would_close", "valid_for_claim"]),
        "",
        "## Live Delta_p / q_R_hat Input Row",
        markdown_table(data["live_input"], ["input_id", "source_file", "source_exists", "candidate_id", "route_type", "q_R_hat_value_or_bound", "q_R_hat_status", "delta_p_relation", "delta_p_abs_bound", "input_kind", "derivation_status", "prediction_status", "full_vector_role", "valid_pipeline_row", "valid_prediction_row", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Input Validation",
        markdown_table(data["input_validation"], ["validation_id", "test", "status", "notes", "valid_for_claim"]),
        "",
        "## PPN Vector Binding Status",
        markdown_table(data["ppn_vector"], ["component_id", "input_status", "current_input", "still_missing", "claim_effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QR_RAW.mkdir(parents=True, exist_ok=True)
    QR_ACCEPTED.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "parent_zero": parent_zero_rows(),
        "live_input": live_input_rows(),
        "ppn_vector": ppn_vector_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    data["input_validation"] = input_validation_rows(data)
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["parent_zero"], data["parent_zero"])
    write_csv(OUTPUTS["live_input"], data["live_input"])
    write_csv(OUTPUTS["input_validation"], data["input_validation"])
    write_csv(OUTPUTS["ppn_vector"], data["ppn_vector"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
