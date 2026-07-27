from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_QR_PARENT_ZERO_OR_LIVE_DELTA_P_COUPLING_INPUT_2575"
CHECKPOINT_ID = "2575"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QR_RAW = ROOT / "source-intake" / "qr-hat" / "raw"
QR_ACCEPTED = ROOT / "source-intake" / "qr-hat" / "accepted"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

RAW_QRHAT = QR_RAW / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"
DOC = ROOT / "2575-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-coupling-input-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_QR_ZERO_2575_SOURCE_REGISTER.csv",
    "parent_zero": OUT / "P8_Y5_QR_ZERO_2575_PARENT_ZERO_SIGNATURE_AUDIT.csv",
    "live_input": OUT / "P8_Y5_QR_ZERO_2575_LIVE_DELTA_P_QRHAT_COUPLING_INPUT_ROW.csv",
    "input_validation": OUT / "P8_Y5_QR_ZERO_2575_DELTA_P_COUPLING_INPUT_VALIDATION.csv",
    "ppn_vector": OUT / "P8_Y5_QR_ZERO_2575_PPN_VECTOR_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_QR_ZERO_2575_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_QR_ZERO_2575_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_QR_ZERO_2575_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_QR_ZERO_2575_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2575_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_zero": LOCAL_BOUNDS / "QR_parent_zero_signature_audit_2575_NONCLAIM.csv",
    "live_input": LOCAL_BOUNDS / "Live_delta_p_qRhat_coupling_input_row_2575_NONCLAIM.csv",
    "input_validation": LOCAL_BOUNDS / "Delta_p_coupling_input_validation_2575_NONCLAIM.csv",
    "ppn_vector": LOCAL_BOUNDS / "PPN_vector_binding_status_2575_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2575_PARENT_HCORE_QR_SOURCE_EQUATION_COUPLING_OWNER.csv",
}

SOURCES = [
    {
        "source_id": "SRC2575_00_2574_handoff",
        "source_path": ROOT / "2574-Y5-R2FR-delta-p-beta-disformal-coupling-PPN-vector-or-parent-grammar-proof.md",
        "needles": ["NEXT2574_0_selected", "LIVE2574_0_parent_zero", "VAL2574_OVERALL"],
        "role": "active handoff selecting Q_R parent-zero or live delta_p/coupling input row",
    },
    {
        "source_id": "SRC2575_01_2501_precedent",
        "source_path": ROOT / "2501-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-input-row.md",
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "QR_PARENT_ZERO_NOT_DERIVED_CURRENT_CORPUS", "VAL2501_OVERALL"],
        "role": "earlier Q_R parent-zero audit and live q_R_hat ceiling import",
    },
    {
        "source_id": "SRC2575_02_1884_contract",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "DPQR1884_2_delta_p", "VAL1884_OVERALL"],
        "role": "delta_p/q_R_hat bridge and strict finite input contract",
    },
    {
        "source_id": "SRC2575_03_1240_zero_attempt",
        "source_path": OUT / "P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
        "needles": ["ZQR1240_5_verdict", "ZERO_CHARGE_THEOREM_NOT_DERIVED"],
        "role": "Q_R zero-charge theorem failure map",
    },
    {
        "source_id": "SRC2575_04_1255_doc",
        "source_path": ROOT / "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md",
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "not an MTS prediction", "VAL1255_13_overall"],
        "role": "first live q_R_hat raw row as nonclaim Cassini ceiling",
    },
    {
        "source_id": "SRC2575_05_qrhat_raw",
        "source_path": RAW_QRHAT,
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "phenomenological_upper_bound_not_theory_prediction"],
        "role": "raw live nonclaim q_R_hat ceiling row",
    },
    {
        "source_id": "SRC2575_06_1249_candidate_results",
        "source_path": OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
        "needles": ["ACCEPTED_NONCLAIM_FINITE_QRHAT", "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM"],
        "role": "finite q_R_hat validator acceptance snapshot",
    },
    {
        "source_id": "SRC2575_07_1244_gm",
        "source_path": OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
        "needles": ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)"],
        "role": "GM/source normalization convention for raw Q_R conversion",
    },
    {
        "source_id": "SRC2575_08_1253_Hcore",
        "source_path": OUT / "P8_Y5_R10_1253_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv",
        "needles": ["HCE1253_0_reciprocal_euler_source", "SOURCE_EQUATION_NOT_DERIVED", "HCE1253_1_boundary_flux_definition"],
        "role": "parent H_core reciprocal source-equation and boundary owner blocker",
    },
    {
        "source_id": "SRC2575_09_2572_coupling",
        "source_path": ROOT / "2572-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": ["CS2572_0_kappa_MTS", "CS2572_1_ell_J", "VAL2572_OVERALL"],
        "role": "coupling shadow audit requiring kappa/ell_J ownership",
    },
    {
        "source_id": "SRC2575_10_2574_validation",
        "source_path": OUT / "P8_Y5_BRR545_2574_VALIDATION.csv",
        "needles": ["VAL2574_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def as_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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
            "signature_id": "QRZ2575_0_parent_generator",
            "needed_clause": "parent reciprocal generator G_R exists before readout",
            "current_evidence": "cell-current branch gives W partial_r C_R=Q_R, but generator ownership is not parent-signed",
            "coupling_owner_clause": "G_R must be defined with kappa_MTS and ell_J fixed before source normalization",
            "status": "GENERATOR_OWNER_UNSIGNED",
            "would_close": "defines what Q_R is and what symmetry/constraint could set it to zero",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_1_boundary_charge_zero",
            "needed_clause": "reciprocal boundary charge vanishes or is pure gauge for allowed local source class",
            "current_evidence": "1240/1884 show conservation and asymptotic flatness do not kill Q_R hair",
            "coupling_owner_clause": "boundary charge must not shift under hidden kappa/ell_J/source-current rescaling",
            "status": "BOUNDARY_CHARGE_ZERO_NOT_DERIVED",
            "would_close": "Q_R=0 in local exterior",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_2_source_descent",
            "needed_clause": "ordinary matter carries no reciprocal R_AB charge",
            "current_evidence": "topological/source zero-charge is named as a possible route but not derived",
            "coupling_owner_clause": "ordinary source current must descend with parent-owned ell_J and no source-only prefactor",
            "status": "SOURCE_DESCENT_UNSIGNED",
            "would_close": "J_R integrates to zero and source bodies cannot generate Q_R",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_3_matter_readout_descent",
            "needed_clause": "matter/readout descends through Q_vis without Weyl, disformal, source-prefactor, endpoint or coupling re-entry",
            "current_evidence": "2572-2574 keep b_R,d_R,w_R,endpoint,kappa,ell_J as live nonclaim rows",
            "coupling_owner_clause": "kappa_MTS and ell_J must be parent coefficients, not post-readout normalization choices",
            "status": "MATTER_READOUT_DESCENT_UNSIGNED",
            "would_close": "delta_p/gamma channel cannot be reopened through local rods, clocks, photons or source normalization",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_4_projection_silence",
            "needed_clause": "boundary, endpoint, tau, PPN gauge and source projection silence is parent-owned",
            "current_evidence": "2574 stages endpoint/readout/source-coupling kernels as missing templates",
            "coupling_owner_clause": "projection cannot absorb Dln_kappa_MTS or Dln_ell_J into fitted GM/H0",
            "status": "PROJECTION_SILENCE_UNSIGNED",
            "would_close": "finite Q_R or zero theorem becomes usable in full PPN vector",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_5_Hcore_source_equation",
            "needed_clause": "parent H_core supplies E_R=delta H_core/delta C_R with explicit bulk source and boundary term",
            "current_evidence": "1253 records formal shape only; explicit H_core and boundary charge class are missing",
            "coupling_owner_clause": "H_core must also own EH/coupling normalization, not import G_ref or fitted GM",
            "status": "HCORE_SOURCE_EQUATION_NOT_DERIVED",
            "would_close": "decides whether Q_R is zero, finite, or a no-go residual from parent dynamics",
            "valid_for_claim": False,
        },
        {
            "signature_id": "QRZ2575_6_verdict",
            "needed_clause": "current MTS parent signs Q_R=0 with coupling/source ownership",
            "current_evidence": "no single parent package signs generator, boundary, source, matter/readout, projection and coupling clauses together",
            "coupling_owner_clause": "missing coupling owner is now a hard blocker, not metadata",
            "status": "QR_PARENT_ZERO_WITH_COUPLING_NOT_DERIVED_CURRENT_CORPUS",
            "would_close": "Q_R=0 -> C_R=0 -> delta_p=0 with no fitted-GM loophole",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def live_input_rows() -> list[dict[str, Any]]:
    raw = read_csv_first_row(RAW_QRHAT)
    q_hat = as_float(raw.get("q_R_hat", "0"))
    delta_p_bound = abs(q_hat) / 2.0
    rows = [
        {
            "input_id": "LIVE2575_0_QRHAT1255_Cassini_ceiling",
            "source_file": str(RAW_QRHAT),
            "source_exists": RAW_QRHAT.exists(),
            "candidate_id": raw.get("candidate_id", "MISSING_CANDIDATE_ID"),
            "route_type": raw.get("route_type", "finite_qR_hat"),
            "q_R_hat_value_or_bound": f"{q_hat:.12g}",
            "q_R_hat_status": "FINITE_NUMERIC" if q_hat > 0 else "MISSING_OR_NONNUMERIC",
            "delta_p_relation": "delta_p=-q_R_hat/2 for signed finite prediction; here only abs(delta_p)<=abs(q_R_hat)/2 is used",
            "delta_p_abs_bound": f"{delta_p_bound:.12e}",
            "coupling_owner_status": "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION",
            "coupling_baseline_status": "COMPARATOR_BASELINE_ONLY_NOT_MTS_FIXED_BEFORE_READOUT",
            "input_kind": raw.get("input_kind", "phenomenological_upper_bound_not_theory_prediction"),
            "prediction_status": "PHENOMENOLOGICAL_CEILING_NOT_MTS_PREDICTION",
            "full_vector_role": "guardrail_ceiling_only_not_score_ready",
            "valid_pipeline_row": bool(raw) and q_hat > 0,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "LIVE2575_1_parent_zero_template",
            "source_file": "MISSING_PARENT_QR_ZERO_COUPLING_SIGNATURE",
            "source_exists": False,
            "candidate_id": "QR_PARENT_ZERO_REQUIRED",
            "route_type": "parent_zero_theorem",
            "q_R_hat_value_or_bound": "0",
            "q_R_hat_status": "ZERO_ONLY_IF_PARENT_SIGNED",
            "delta_p_relation": "Q_R=0 -> C_R=0 -> delta_p=0",
            "delta_p_abs_bound": "0",
            "coupling_owner_status": "MISSING_COUPLING_OWNER_SIGNATURE",
            "coupling_baseline_status": "not_required_if_theorem_zero_but_required_if_scored",
            "input_kind": "theorem_zero",
            "prediction_status": "NOT_ACCEPTED_UNTIL_PARENT_SIGNED",
            "full_vector_role": "would_close_delta_p_component",
            "valid_pipeline_row": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "LIVE2575_2_no_live_mts_prediction",
            "source_file": str(QR_ACCEPTED),
            "source_exists": QR_ACCEPTED.exists(),
            "candidate_id": "NO_ACCEPTED_MTS_PREDICTION_ROW",
            "route_type": "finite_qR_hat_prediction",
            "q_R_hat_value_or_bound": "MISSING_PARENT_PREDICTED_QRHAT",
            "q_R_hat_status": "MISSING_MTS_PREDICTION",
            "delta_p_relation": "delta_p=-q_R_hat/2 would apply after a sourced finite prediction",
            "delta_p_abs_bound": "MISSING_PREDICTED_DELTA_P",
            "coupling_owner_status": "MISSING_PARENT_KAPPA_ELLJ_OWNER",
            "coupling_baseline_status": "MISSING_FIXED_BEFORE_READOUT_BASELINE",
            "input_kind": "prediction_required",
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
    live_rows = data["live_input"]
    ceiling = next(row for row in live_rows if row["input_id"] == "LIVE2575_0_QRHAT1255_Cassini_ceiling")
    rows = [
        {
            "validation_id": "DVAL2575_0_raw_row_exists",
            "test": "raw QRHAT1255 row exists and parses",
            "status": "PASS" if ceiling["valid_pipeline_row"] else "FAIL",
            "notes": "usable as nonclaim pipeline ceiling only",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2575_1_not_prediction",
            "test": "live row is not promoted as MTS prediction",
            "status": "PASS" if ceiling["valid_prediction_row"] is False else "FAIL",
            "notes": "Cassini-derived ceiling cannot prove local GR",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2575_2_delta_p_bound",
            "test": "delta_p ceiling is computed only as abs(delta_p)<=abs(q_R_hat)/2",
            "status": "PASS" if ceiling["delta_p_abs_bound"] == "2.300000000000e-05" else "FAIL",
            "notes": "sign is not assigned; it is a ceiling not a prediction",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2575_3_coupling_not_signed",
            "test": "coupling owner missing blocks prediction use",
            "status": "PASS" if ceiling["coupling_owner_status"] == "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION" else "FAIL",
            "notes": "q_R_hat ceiling is not allowed to fix kappa_MTS or ell_J",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2575_4_parent_zero_rejected",
            "test": "parent zero template remains blocked",
            "status": "PASS",
            "notes": "Q_R=0 still needs parent generator/boundary/source/readout/projection/coupling signature",
            "valid_for_claim": False,
        },
        {
            "validation_id": "DVAL2575_5_full_score_refused",
            "test": "no row is score-ready or claim-ready",
            "status": "PASS" if all(row["score_ready"] is False and row["claim_allowed"] is False for row in live_rows) else "FAIL",
            "notes": "full PPN vector still lacks beta, b_R, d_R, w_R, endpoint/readout and coupling closure",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "PVBS2575_0_delta_p",
            "input_status": "NONCLAIM_CEILING_EXISTS_NOT_PREDICTION",
            "current_input": "QRHAT1255 gives abs(q_R_hat)<=4.6e-5, hence abs(delta_p)<=2.3e-5 as a pipeline ceiling",
            "still_missing": "parent Q_R=0 theorem or parent-predicted finite q_R_hat with coupling owner",
            "coupling_status": "kappa/ellJ owner missing for prediction use",
            "claim_effect": "blocks local-GR/PPN score",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_1_kappa",
            "input_status": "MISSING_PARENT_OWNER",
            "current_input": "none",
            "still_missing": "Dln_kappa_MTS=0 theorem or finite source-normalized response row",
            "coupling_status": "cannot be inferred from G_ref, Cassini ceiling or fitted GM",
            "claim_effect": "blocks beta/source-normalization vector",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_2_ellJ",
            "input_status": "MISSING_PARENT_OWNER",
            "current_input": "none",
            "still_missing": "Dln_ell_J=0 theorem or finite source-current response row",
            "coupling_status": "must be parent-owned before local/cosmology fits",
            "claim_effect": "blocks beta, alpha3 and source-current vector",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_3_beta",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "beta=1 theorem or finite delta_beta_total/source-coupling row",
            "coupling_status": "kappa/ellJ source legs feed beta unless theorem-zero or bounded",
            "claim_effect": "gamma/delta_p ceiling cannot imply beta",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_4_bR",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "b_R theorem-zero or finite coefficient in C_R normalization",
            "coupling_status": "must use same source/readout convention as coupling legs",
            "claim_effect": "no-shadow common Weyl channel remains open",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_5_dR_preferred",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "d_R preferred-frame response kernel and alpha_i bounds",
            "coupling_status": "preferred-frame source-current normalization may couple to kappa*ellJ",
            "claim_effect": "alpha1/alpha2/preferred-frame gates remain blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_6_wR_source",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "source-prefactor zero theorem or finite source-normalization kernel",
            "coupling_status": "must be separated from kappa/ellJ owner rows",
            "claim_effect": "source/GM/beta transfer remains blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_7_endpoint_readout",
            "input_status": "MISSING",
            "current_input": "none",
            "still_missing": "endpoint projection, tau, measured-GM and PPN-gauge tail kernels",
            "coupling_status": "endpoint support must use fixed-before-readout source convention",
            "claim_effect": "gamma/beta extraction and orbital/light-time gates remain blocked",
            "valid_for_claim": False,
        },
        {
            "component_id": "PVBS2575_8_total_abs",
            "input_status": "VECTOR_NOT_SCORE_READY",
            "current_input": "one nonclaim ceiling only",
            "still_missing": "all active components zero/bounded componentwise with no cancellation shortcut",
            "coupling_status": "coupling rows missing from score-ready vector",
            "claim_effect": "all PPN/local-GR claims blocked",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2575_0_internal",
            "claim": "2575 may import QRHAT1255 as private nonclaim pipeline ceiling.",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "source-backed ceiling exists and parses, but prediction and claim flags remain false",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_1_parent_zero",
            "claim": "MTS parent derives Q_R=0 with coupling/source ownership.",
            "gate_status": "BLOCKED",
            "reason": "generator, boundary charge, source descent, matter/readout descent, projection silence and coupling owner are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_2_live_prediction",
            "claim": "live q_R_hat/delta_p row is an MTS prediction.",
            "gate_status": "BLOCKED",
            "reason": "QRHAT1255 is a Cassini-derived phenomenological ceiling, not a parent coefficient/boundary-flux prediction",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_3_coupling_prediction",
            "claim": "kappa_MTS and ell_J are fixed/silent for this local PPN input.",
            "gate_status": "BLOCKED",
            "reason": "coupling owner remains missing and cannot be supplied by the Cassini q_R_hat ceiling",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_4_ppn_vector",
            "claim": "full PPN vector can be scored.",
            "gate_status": "BLOCKED",
            "reason": "delta_p has only a ceiling; beta, b_R, d_R, w_R, kappa, ell_J and endpoint/readout rows remain missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_5_local_GR_Newton",
            "claim": "local GR/Newton is derived.",
            "gate_status": "BLOCKED",
            "reason": "Q_R parent-zero/live prediction, beta, no-shadow, coupling and source/readout gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2575_6_no_shortcuts",
            "claim": "closure zero, comparator-only, gamma-only, fitted-GM or cancellation-only row can pass.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "2575 keeps the live row as ceiling-only and blocks score/claim use",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2575_0_parent_zero",
            "decision": "QR_PARENT_ZERO_WITH_COUPLING_STILL_UNSIGNED",
            "reason": "zero-flux lemma is exact but no parent package signs Q_R=0 plus coupling/source ownership",
            "effect": "keep Q_R=0 as the highest-leverage derivation target",
        },
        {
            "decision_id": "DEC2575_1_live_input",
            "decision": "LIVE_NONCLAIM_QRHAT_CEILING_IMPORTED_WITH_COUPLING_GUARD",
            "reason": "QRHAT1255 exists, has no missing markers, and remains useful as a pipeline ceiling",
            "effect": "PPN pipeline has a guardrail scale: abs(q_R_hat)<=4.6e-5 and abs(delta_p)<=2.3e-5, but no prediction",
        },
        {
            "decision_id": "DEC2575_2_no_prediction",
            "decision": "NO_MTS_QRHAT_OR_COUPLING_PREDICTION_ROW_EXISTS",
            "reason": "the imported row is derived from the Cassini comparator rather than parent MTS coefficients or boundary flux",
            "effect": "do not treat the ceiling as evidence that MTS passes local GR",
        },
        {
            "decision_id": "DEC2575_3_next",
            "decision": "PARENT_HCORE_QR_SOURCE_EQUATION_WITH_COUPLING_OWNER_SELECTED_NEXT",
            "reason": "the next real leap is an equation for Q_R/boundary/source owner and kappa/ell_J normalization, not another comparator translation",
            "effect": "2576 should attempt parent H_core reciprocal source equation/boundary charge owner with coupling slots included",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2575_0_selected",
            "selection_status": "selected",
            "target_file": "2576-Y5-R2FR-parent-Hcore-QR-source-equation-coupling-owner-or-boundary-charge-owner.md",
            "target_script": "scripts/Y5_R2FR_parent_Hcore_QR_source_equation_coupling_owner_or_boundary_charge_owner_2576.py",
            "task": "derive or reject the parent reciprocal H_core source equation and boundary-charge owner that would produce Q_R=0, a parent-predicted finite Q_R, or a strict no-go, while also owning kappa_MTS and ell_J before readout; keep QRHAT1255 as nonclaim ceiling only",
            "acceptance_target": "parent-owned E_R=delta H_core/delta C_R equation with boundary/source/coupling terms, or explicit blocker naming the missing action block; no local-GR claim",
            "guardrails": "do not treat Cassini ceiling as prediction; no closure zero; no GR Schwarzschild import; no gamma-only pass; no fitted GM/H0 shortcut; no GitHub",
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
                    "copy_id": f"COPY2575_{key}",
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
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2575_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2575_01_parent_zero_blocked",
        any(row["signature_id"] == "QRZ2575_6_verdict" and row["status"] == "QR_PARENT_ZERO_WITH_COUPLING_NOT_DERIVED_CURRENT_CORPUS" for row in data["parent_zero"]),
        "Q_R parent-zero signature with coupling remains blocked",
    )
    add(
        "VAL2575_02_live_ceiling_imported",
        any(row["input_id"] == "LIVE2575_0_QRHAT1255_Cassini_ceiling" and row["valid_pipeline_row"] is True for row in data["live_input"]),
        "live QRHAT1255 ceiling row imported as nonclaim pipeline input",
    )
    add(
        "VAL2575_03_ceiling_not_prediction",
        all(row["valid_prediction_row"] is False for row in data["live_input"]),
        "Cassini ceiling is not promoted as an MTS prediction",
    )
    add(
        "VAL2575_04_delta_p_bound_computed",
        any(row["input_id"] == "LIVE2575_0_QRHAT1255_Cassini_ceiling" and row["delta_p_abs_bound"] == "2.300000000000e-05" for row in data["live_input"]),
        "delta_p ceiling computed from q_R_hat ceiling without assigning sign",
    )
    add(
        "VAL2575_05_coupling_guard_active",
        any(row["input_id"] == "LIVE2575_0_QRHAT1255_Cassini_ceiling" and row["coupling_owner_status"] == "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION" for row in data["live_input"]),
        "coupling owner guard blocks prediction use",
    )
    add(
        "VAL2575_06_input_validation",
        all(row["status"] == "PASS" for row in data["input_validation"]),
        "input validation refuses prediction/score use",
    )
    add(
        "VAL2575_07_vector_not_score_ready",
        any(row["component_id"] == "PVBS2575_8_total_abs" and row["input_status"] == "VECTOR_NOT_SCORE_READY" for row in data["ppn_vector"]),
        "full PPN vector remains not score-ready",
    )
    add("VAL2575_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]), "no gate allows Q_R zero, q_R_hat prediction, coupling prediction, PPN, local-GR or Newton claim")
    add(
        "VAL2575_09_next_target_written",
        any(row["route_id"] == "NEXT2575_0_selected" for row in data["next"]),
        "2576 parent Hcore QR source equation with coupling owner target selected",
    )
    add("VAL2575_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2575*", "*P8_Y5_QR_ZERO_2575*", "*JR2575*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2575_11_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2575 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2575_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2575_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2575_OVERALL",
        overall,
        "2575 blocks Q_R parent-zero with coupling, imports QRHAT1255 as live nonclaim ceiling, refuses prediction use, and selects parent Hcore QR source-equation with coupling owner next",
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
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2575 Y5 R2FR QR Parent-Zero Signature Or Live Delta_p Coupling Input Row",
        "",
        "**Status:** private nonclaim checkpoint. `Q_R=0` is still not parent-derived. The existing QRHAT1255 Cassini-derived row remains useful only as a live nonclaim ceiling, now with an explicit coupling-owner guard.",
        "",
        "**Main result:** we retain a live finite ceiling `abs(q_R_hat)<=4.6e-5`, hence `abs(delta_p)<=2.3e-5` under the bridge `delta_p=-q_R_hat/2`. But this is still a comparator-derived ceiling, not an MTS prediction. The upgraded rule is stricter: a prediction row must also sign `kappa_MTS` and `ell_J` ownership or a fixed-before-readout source convention. The next real derivation move is the parent `H_core` reciprocal source equation/boundary-charge owner with coupling slots included.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## QR Parent-Zero Signature Audit",
        markdown_table(data["parent_zero"], ["signature_id", "needed_clause", "current_evidence", "coupling_owner_clause", "status", "would_close", "valid_for_claim"]),
        "",
        "## Live Delta_p / q_R_hat / Coupling Input Row",
        markdown_table(data["live_input"], ["input_id", "source_file", "source_exists", "candidate_id", "route_type", "q_R_hat_value_or_bound", "q_R_hat_status", "delta_p_relation", "delta_p_abs_bound", "coupling_owner_status", "coupling_baseline_status", "input_kind", "prediction_status", "full_vector_role", "valid_pipeline_row", "valid_prediction_row", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Input Validation",
        markdown_table(data["input_validation"], ["validation_id", "test", "status", "notes", "valid_for_claim"]),
        "",
        "## PPN Vector Binding Status",
        markdown_table(data["ppn_vector"], ["component_id", "input_status", "current_input", "still_missing", "coupling_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
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
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QR_ACCEPTED.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "parent_zero": parent_zero_rows(),
        "live_input": live_input_rows(),
        "ppn_vector": ppn_vector_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    data["input_validation"] = input_validation_rows(data)

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["parent_zero"], data["parent_zero"])
    write_csv(OUTPUTS["live_input"], data["live_input"])
    write_csv(OUTPUTS["input_validation"], data["input_validation"])
    write_csv(OUTPUTS["ppn_vector"], data["ppn_vector"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2575_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
