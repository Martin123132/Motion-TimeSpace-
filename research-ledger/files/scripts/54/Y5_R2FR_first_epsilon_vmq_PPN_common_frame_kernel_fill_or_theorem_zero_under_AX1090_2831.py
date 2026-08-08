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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2831-Y5-R2FR-first-epsilon-vmq-PPN-common-frame-kernel-fill-or-theorem-zero-under-AX1090.md"

SRC_2830_NEXT = RESIDUALS / "P8_Y5_R2FR_2830_NEXT_TARGET.csv"
SRC_2830_INTERFACE = RESIDUALS / "P8_Y5_R2FR_2830_EPSILON_VMQ_RESPONSE_KERNEL_INTERFACE.csv"
SRC_2830_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2830_EPSILON_VMQ_SOURCE_ACQUISITION_CONTRACT.csv"
SRC_2829_ACQ = RESIDUALS / "P8_Y5_R2FR_2829_EPSILON_VMQ_SOURCE_READY_ACQUISITION_ROWS.csv"
SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2489_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2489_RETRY = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PARENT_NO_SHADOW_RETRY.csv"
SRC_2489_GATES = RESIDUALS / "P8_Y5_NO_SHADOW_2489_CLAIM_GATES.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"
SRC_2631_QUEUE = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_RESIDUAL_KERNEL_FILL_QUEUE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2831_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2831_PPN_COMMON_FRAME_THEOREM_ZERO_ATTEMPT.csv",
    "kernel_fill": RESIDUALS / "P8_Y5_R2FR_2831_PPN_COMPONENT_KERNEL_FILL_ROWS_NONCLAIM.csv",
    "guard": RESIDUALS / "P8_Y5_R2FR_2831_NO_CANCELLATION_AND_FULL_VECTOR_GUARD.csv",
    "readiness": RESIDUALS / "P8_Y5_R2FR_2831_SCORE_READINESS_MATRIX.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2831_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2831_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2831_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2831_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2831_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": SOURCE_WEIGHT / "epsilon_vmq_PPN_common_frame_kernel_fill_2831_NONCLAIM.csv",
    "guard_copy": LOCAL_BOUNDS / "epsilon_vmq_PPN_no_cancellation_guard_2831_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2831_EPSILON_VMQ_FIRST_SOURCE_VALUE_OR_BOUND_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2831_0_2830_next", SRC_2830_NEXT, "NEXT2830_0_2831", "2830 selected the first epsilon_vmq PPN/common-frame kernel fill"),
        ("SRC2831_1_2830_interface", SRC_2830_INTERFACE, "KI2830_1_PPN_total;KI2830_2_PPN_gamma;KI2830_3_PPN_preferred", "2830 response-kernel interfaces for PPN total/gamma/preferred-frame"),
        ("SRC2831_2_2830_contract", SRC_2830_CONTRACT, "SC2830_1_source_weight;SC2830_3_common_weyl;SC2830_4_disformal;SC2830_5_endpoint", "2830 component acquisition contracts"),
        ("SRC2831_3_2829_acq", SRC_2829_ACQ, "ACQ2829_3_common_weyl;ACQ2829_4_disformal;ACQ2829_5_endpoint", "epsilon_vmq finite component rows inherited from 2829"),
        ("SRC2831_4_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "conditional no-shadow theorem and current failure verdict"),
        ("SRC2831_5_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_1_common_disformal;CM2488_2_source_prefactor;CM2488_3_endpoint_boundary;CM2488_4_qshape_forgetting", "countermodels that block slogan-level zero claims"),
        ("SRC2831_6_2489_kernel", SRC_2489_KERNEL, "PPNK2489_0_conformal_gamma_kernel;PPNK2489_1_CR_delta_p_combo_kernel;PPNK2489_3_disformal_preferred_frame_placeholder;PPNK2489_4_endpoint_readout_tail_placeholder", "existing symbolic PPN/common-frame response scaffold"),
        ("SRC2831_7_2489_retry", SRC_2489_RETRY, "PNC2489_0_terminal_public_action_domain;PNC2489_3_verdict", "parent no-shadow retry clauses remain unsigned"),
        ("SRC2831_8_2489_gates", SRC_2489_GATES, "GATE2489_2_ppn_gamma_score;GATE2489_3_full_ppn_score;GATE2489_5_no_shortcuts", "PPN score gates and no-shortcut guard"),
        ("SRC2831_9_2631_vector", SRC_2631_VECTOR, "PPNV2631_1_bR;PPNV2631_3_dR;PPNV2631_4_wR;PPNV2631_5_endpoint;PPNV2631_8_total_abs", "full PPN no-cancellation vector"),
        ("SRC2831_10_2631_queue", SRC_2631_QUEUE, "KQ2631_2_source_prefactor;KQ2631_3_disformal_preferred_frame;KQ2631_4_endpoint_readout", "residual-kernel fill queue"),
    ]
    return [source_row(*spec) for spec in specs]


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TZ2831_0_parent_terminality",
            "terminal public coframe/action domain",
            "If S_matter and ordinary readout factor only through e_pub=E(Q_vis), then hidden/residual representative directions cannot move rods, clocks, photons or sources.",
            "ZTH2488_0_exact_conditional;PNC2489_0_terminal_public_action_domain",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "2488 gives an exact conditional theorem, but 2489 records that the parent normal form has not signed the action/readout domain.",
            "would set b_R=d_R=w_R=epsilon_endpoint_R=0 before PPN projection",
        ),
        (
            "TZ2831_1_common_weyl_bR",
            "b_R_to_vmq theorem-zero",
            "b_R_to_vmq=0 follows only if ordinary matter/readout has no Weyl slot exp(b_R C_R) and no C_R-dependent measured-GM/gauge tail.",
            "CM2488_0_common_weyl;PPNK2489_0_conformal_gamma_kernel;PPNV2631_1_bR",
            "NOT_PROVED_COUNTERMODEL_SURVIVES",
            "The common Weyl countermodel is covariant and universal, so same-frame/WEP language does not kill it.",
            "keep b_R_to_vmq as a finite nonclaim PPN gamma/light-time component",
        ),
        (
            "TZ2831_2_disformal_dR",
            "d_R_to_vmq theorem-zero",
            "d_R_to_vmq=0 follows only if the observed coframe/action domain excludes any disformal/current/domain vector slot.",
            "CM2488_1_common_disformal;PPNK2489_3_disformal_preferred_frame_placeholder;PPNV2631_3_dR",
            "NOT_PROVED_COUNTERMODEL_SURVIVES",
            "A universal preferred-frame/disformal dependence can remain covariant once a current field is in the domain.",
            "keep d_R_to_vmq as a finite nonclaim alpha_i/preferred-frame component",
        ),
        (
            "TZ2831_3_source_weight",
            "epsilon_vmq_source_weight/w_R theorem-zero",
            "source-weight leak vanishes only if the parent action forbids source-only prefactors and proves the projected mass owner is not double counted.",
            "CM2488_2_source_prefactor;PPNV2631_4_wR;KQ2631_2_source_prefactor",
            "NOT_PROVED_COUNTERMODEL_SURVIVES",
            "Ward conservation can hold while the Hilbert source normalization still shifts, so conservation alone is not a zero proof.",
            "keep epsilon_vmq_source_weight as a finite nonclaim source/WEP/Newton-GM component",
        ),
        (
            "TZ2831_4_endpoint_readout",
            "epsilon_endpoint_to_vmq/readout theorem-zero",
            "endpoint/readout leak vanishes only if boundary endpoints, measured-GM extraction and PPN gauge maps are basic after variation.",
            "CM2488_3_endpoint_boundary;CM2488_4_qshape_forgetting;PPNK2489_4_endpoint_readout_tail_placeholder;PPNV2631_5_endpoint",
            "NOT_PROVED_COUNTERMODEL_SURVIVES",
            "Forgetting a q-label does not prove the observable functor forgets endpoint/readout data.",
            "keep endpoint and readout tails as finite nonclaim orbital/light-time/PPN components",
        ),
        (
            "TZ2831_5_total_ppn_zero",
            "Delta_PPN_abs theorem-zero",
            "Full PPN zero needs every active component zero in the same convention, plus no hidden cancellation identity.",
            "PPNV2631_8_total_abs;GATE2489_3_full_ppn_score",
            "NOT_PROVED_VECTOR_INCOMPLETE",
            "b_R, d_R, w_R/source, endpoint/readout, beta, q_loc and delta_p/q_R_hat channels are not all theorem-zero or finite sourced.",
            "use componentwise absolute vector; no gamma-only score",
        ),
        (
            "TZ2831_6_verdict",
            "2831 theorem-zero verdict",
            "The PPN/common-frame theorem-zero path is exact if the future parent action signs terminal public matter/readout; it is not signed in the current corpus.",
            "ZTH2488_2_current_verdict;PNC2489_3_verdict;GATE2489_1_parent_no_shadow",
            "THEOREM_ZERO_NOT_CLAIMED",
            "Current evidence supports a clean contract, not a proof.",
            "route to first finite b_R/delta_p or parent no-Weyl certificate in 2832",
        ),
    ]
    return [
        nonclaim(
            {
                "theorem_attempt_id": row_id,
                "target": target,
                "required_statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_failure": failure,
                "effect_or_fallback": fallback,
                "theorem_zero_proved": False,
                "control_only": True,
            }
        )
        for row_id, target, statement, anchors, status, failure, fallback in specs
    ]


def kernel_fill_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "KF2831_0_bR_gamma",
            "b_R_to_vmq",
            "common Weyl/coframe shadow",
            "gamma_minus_1;light_time",
            "gamma_obs-1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p)",
            "MISSING_b_R_VALUE_OR_ZERO;MISSING_delta_p_VALUE_OR_ZERO;MISSING_NO_OTHER_PPN_CHANNELS",
            "PPNK2489_1_CR_delta_p_combo_kernel;PPNV2631_1_bR",
            "source b_R and delta_p/q_R_hat in the same source-normalized convention or prove no-Weyl/no-boundary-charge",
        ),
        (
            "KF2831_1_dR_preferred",
            "d_R_to_vmq",
            "disformal/preferred-frame shadow",
            "alpha1;alpha2;alpha3;xi;gamma",
            "Delta_alpha_i_abs += |K_alpha_i_dR*d_R_to_vmq| for each active preferred-frame channel",
            "MISSING_DISFORMAL_METRIC_ANSATZ;MISSING_VECTOR_NORMALIZATION;MISSING_ALPHA_I_RESPONSE_MATRIX",
            "PPNK2489_3_disformal_preferred_frame_placeholder;PPNV2631_3_dR",
            "prove no-disformal/current slot or build the alpha_i response matrix before scoring",
        ),
        (
            "KF2831_2_source_weight",
            "epsilon_vmq_source_weight",
            "source-only/action-weight residual",
            "beta_minus_1;WEP;Newton_GM;R10_source_leg;alpha3",
            "Delta_source_abs += |K_source_w*epsilon_vmq_source_weight| with material/source convention fixed",
            "MISSING_NO_SOURCE_PREFACTOR_THEOREM;MISSING_COMPONENT_BASIS;MISSING_TAU_K_QBAR_PROJECTIONS",
            "PPNV2631_4_wR;KQ2631_2_source_prefactor",
            "prove no source-prefactor/no double counting or source first material/source projection row",
        ),
        (
            "KF2831_3_endpoint_readout",
            "epsilon_endpoint_to_vmq;epsilon_vmq_readout",
            "endpoint/readout/gauge tail",
            "xi;alpha3;orbital_light_time;gamma_readout;beta_readout",
            "Delta_endpoint_abs += |K_endpoint*epsilon_endpoint_to_vmq| + |K_readout*epsilon_vmq_readout|",
            "MISSING_ENDPOINT_SILENCE;MISSING_GM_CALIBRATION_MAP;MISSING_PPN_GAUGE_TRANSFORM",
            "PPNK2489_4_endpoint_readout_tail_placeholder;PPNV2631_5_endpoint;PPNV2631_6_readout_gauge",
            "prove endpoint/readout basicity after variation or source finite endpoint/readout rows",
        ),
        (
            "KF2831_4_total_abs",
            "epsilon_vmq-derived PPN total",
            "componentwise no-cancellation envelope",
            "all_PPN;local_GR_Newton",
            "Delta_PPN_abs=sum abs(active theorem-zero failures and finite residual components)",
            "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS;MISSING_COMMON_CONVENTION;MISSING_NO_CANCELLATION_IDENTITY",
            "PPNV2631_8_total_abs;GATE2489_3_full_ppn_score",
            "score only after every PPN component is theorem-zero or finite/source-backed in one convention",
        ),
    ]
    return [
        nonclaim(
            {
                "kernel_fill_id": row_id,
                "epsilon_component": symbol,
                "ppn_component": component,
                "observable_targets": targets,
                "symbolic_kernel_or_envelope": kernel,
                "missing_for_claim": missing,
                "source_anchors": anchors,
                "next_action": next_action,
                "kernel_filled_symbolically": True,
                "numeric_value_present": False,
                "source_backed_value": False,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, symbol, component, targets, kernel, missing, anchors, next_action in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2831_0_no_gamma_only", "single gamma/Cassini branch cannot stand in for local GR", "PPNV2631_8_total_abs and GATE2489_3_full_ppn_score require the full PPN vector", "score blocked until beta, preferred-frame, source, endpoint/readout, q_loc and delta_p channels are closed"),
        ("GUARD2831_1_no_cancellation_shortcut", "cancellations cannot be assumed between components", "PPNV2631_8_total_abs demands sum abs(active components) unless a parent identity proves exact cancellation", "all component rows stay in an absolute envelope"),
        ("GUARD2831_2_no_value_placeholders", "symbolic rows are not numeric predictions", "2830 and 2831 rows contain missing inputs rather than invented coefficients", "valid_prediction_row remains false"),
        ("GUARD2831_3_no_Cqm_promotion", "PPN component work does not promote C_qm or local lock", "KI2830_0_Cqm still lacks E_q norm/v_m normalization/epsilon_vmq value", "local-GR/Newton claim remains blocked"),
        ("GUARD2831_4_common_convention", "finite rows must share one source-normalized convention", "b_R, delta_p/q_R_hat, d_R, w_R, endpoint and readout tails otherwise cannot be added", "2832 must pick one component and fix its convention before any score"),
    ]
    return [
        nonclaim(
            {
                "guard_id": guard_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for guard_id, guard, because, effect in specs
    ]


def readiness_rows() -> list[dict[str, Any]]:
    specs = [
        ("SR2831_0_theorem_zero", "PPN/common-frame theorem-zero", "NOT_READY", "terminal public coframe/action-domain clause is conditional, not parent-signed", False),
        ("SR2831_1_symbolic_kernel_fill", "symbolic PPN component interface", "READY_NONCLAIM", "b_R, d_R, source-weight and endpoint/readout rows now have explicit PPN component targets", False),
        ("SR2831_2_gamma_score", "gamma/Cassini score", "NOT_READY", "b_R and delta_p/q_R_hat are value-missing and full-vector guards are open", False),
        ("SR2831_3_full_ppn_score", "full PPN score", "NOT_READY", "component values/theorem-zeros and common convention are missing", False),
        ("SR2831_4_local_gr", "local GR/Newton reduction", "NOT_READY", "PPN vector is one gate only; C_qm, beta/source, q_loc and local operator gates remain open", False),
        ("SR2831_5_next_work", "first finite component or parent-zero certificate", "READY_NONCLAIM", "common Weyl b_R/gamma branch is the tightest next surgical target", False),
    ]
    return [
        nonclaim(
            {
                "readiness_id": row_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "score_or_claim_allowed": allowed,
                "control_only": True,
            }
        )
        for row_id, obj, status, reason, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    theorem_blocked = not any(row["theorem_zero_proved"] for row in rows["theorem"])
    kernel_nonclaim = all(row["kernel_filled_symbolically"] and not row["numeric_value_present"] and not row["source_backed_value"] for row in rows["kernel_fill"])
    guards_active = all(row["guard_active"] for row in rows["guard"])
    scores_blocked = not any(row["score_or_claim_allowed"] for row in rows["readiness"])
    specs = [
        ("GATE2831_0_sources", "all 2831 cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2831_1_theorem_zero", "PPN/common-frame theorem-zero is proved", False, "BLOCKED", "parent action-domain and readout terminality remain unsigned"),
        ("GATE2831_2_kernel_fill", "symbolic PPN component rows are filled without numeric claims", kernel_nonclaim, "PASS_INTERNAL_NONCLAIM" if kernel_nonclaim else "BLOCKED", "rows identify kernels and missing inputs but keep all scores false"),
        ("GATE2831_3_guardrails", "no gamma-only/cancellation/value-placeholder shortcut is active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "full vector and no-cancellation guard stays active"),
        ("GATE2831_4_gamma_score", "MTS passes gamma/Cassini", False, "BLOCKED", "b_R/delta_p values and no-other-channel proof missing"),
        ("GATE2831_5_full_ppn", "MTS passes full PPN vector", False, "BLOCKED", "every PPN component is not zero/finite/source-backed in one convention"),
        ("GATE2831_6_local_gr", "local GR/Newton reduction is derived", False, "BLOCKED", "PPN/common-frame branch is not enough and C_qm/local operator gates remain open"),
        ("GATE2831_7_scores_blocked", "all scores remain blocked", scores_blocked and theorem_blocked, "PASS_NONCLAIM" if scores_blocked and theorem_blocked else "BLOCKED", "2831 is a kernel-fill checkpoint only"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2831_0_zero_attempt", "The theorem-zero route was attempted first.", "NOT_CLOSED", "2488 supplies an exact conditional theorem, but the parent action/readout grammar has not signed the premises.", "do not demote it to nonsense; keep it as a future parent-action contract"),
        ("DEC2831_1_kernel_fill", "The PPN common-frame component map is now explicit.", "SYMBOLIC_KERNEL_FILL_BUILT", "b_R, d_R, source-weight and endpoint/readout leaks each have a PPN target and missing-input list.", "use these rows to choose the first finite component or zero certificate"),
        ("DEC2831_2_no_score", "No gamma, PPN or local-GR score is allowed.", "BLOCKED_BY_VALUES_AND_FULL_VECTOR", "a single gamma kernel cannot represent full PPN/local GR and there are no source-backed component values.", "keep all prediction and claim flags false"),
        ("DEC2831_3_next", "The best next target is the common-Weyl b_R/gamma branch.", "NEXT_2832_SELECTED", "it has the cleanest symbolic kernel already present and gives a sharp choice: prove no Weyl slot or source b_R plus delta_p/q_R_hat.", "attempt first finite PPN component value or parent-zero certificate"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2831_0_2832",
                "status": "selected_primary",
                "target_doc": "2832-Y5-R2FR-epsilon-vmq-first-finite-PPN-component-value-or-parent-zero-certificate-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_epsilon_vmq_first_finite_PPN_component_value_or_parent_zero_certificate_under_AX1090_2832.py",
                "mission": "take the b_R/common-Weyl gamma branch first: either prove a parent no-Weyl slot/no-boundary-charge certificate or source finite b_R and delta_p/q_R_hat rows in one convention",
                "acceptance": "must cite 2831 kernel rows, 2489 gamma combo kernel and 2631 full-vector guard; no Cassini score unless values are sourced and full-vector caveat is explicit; no local-GR claim",
                "forbidden": "do not score from symbolic rows; do not treat b_R alone as gamma; do not cancel delta_p or other PPN components by assumption",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2831_0_kernel_copy", OUTPUTS["kernel_fill"], BRANCH_OUTPUTS["kernel_copy"], "source-weight copy of first epsilon_vmq PPN/common-frame component kernel fill"),
        ("BR2831_1_guard_copy", OUTPUTS["guard"], BRANCH_OUTPUTS["guard_copy"], "local-bounds copy of no-cancellation and full-vector guard"),
        ("BR2831_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for first finite PPN component value or parent-zero certificate"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_prediction_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "alpha_bound", "predicted_value", "coefficient_value", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2831_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2831_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2831_2_theorem_zero_not_claimed", not any(row["theorem_zero_proved"] for row in rows_by_name["theorem"]), "theorem-zero attempt remains unclaimed"),
        ("VAL2831_3_kernel_symbolic_nonclaim", all(row["kernel_filled_symbolically"] and not row["numeric_value_present"] and not row["source_backed_value"] and not row["theorem_zero"] for row in rows_by_name["kernel_fill"]), "component kernels are symbolic/source-ready only"),
        ("VAL2831_4_guards_active", all(row["guard_active"] for row in rows_by_name["guard"]), "no-cancellation/full-vector/no-placeholder guards are active"),
        ("VAL2831_5_scores_blocked", not any(row["score_or_claim_allowed"] for row in rows_by_name["readiness"]), "readiness matrix blocks every score/claim"),
        ("VAL2831_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows gamma, full PPN or local GR"),
        ("VAL2831_7_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2831_8_next_target_2832", any(row["next_id"] == "NEXT2831_0_2832" and row["selected"] for row in rows_by_name["next"]), "first finite PPN component/parent-zero certificate selected next"),
        ("VAL2831_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2831_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2831_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2831_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2831_13_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2831_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2831_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2831_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2831_OVERALL",
            "passed": overall,
            "detail": "2831 attempts the PPN/common-frame theorem-zero route, keeps it unclaimed because parent action/readout terminality is unsigned, fills symbolic epsilon_vmq PPN component rows, blocks gamma/full-PPN/local-GR scoring, and selects the b_R/common-Weyl branch for 2832.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2831 - Y5 R2FR First epsilon_vmq PPN Common-Frame Kernel Fill Or Theorem-Zero Under AX1090

Status: `Y5_R2FR_2831_ppn_common_frame_zero_not_proved_symbolic_kernel_fill_nonclaim`

## Private Verdict

2831 tried the clean route first: prove the whole `epsilon_vmq` PPN/common-frame branch zero by parent matter/readout terminality.

That route still does **not** close. The exact conditional theorem exists, but the future parent action has not yet signed the needed clauses: no Weyl slot, no disformal/current slot, no source-prefactor slot, and no endpoint/readout regeneration after variation.

The constructive gain is that the PPN branch is now decomposed into source-ready, nonclaim component rows. The first best next surgical attack is `b_R_to_vmq` in the common-Weyl/gamma channel: either prove the no-Weyl/no-boundary-charge certificate, or source finite `b_R` and `delta_p/q_R_hat` in one convention.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Theorem-Zero Attempt

{markdown_table(rows["theorem"], ["theorem_attempt_id", "target", "status", "proof_or_failure", "effect_or_fallback", "theorem_zero_proved", "valid_for_claim"])}

## PPN Component Kernel Fill Rows

{markdown_table(rows["kernel_fill"], ["kernel_fill_id", "epsilon_component", "ppn_component", "observable_targets", "symbolic_kernel_or_envelope", "missing_for_claim", "numeric_value_present", "valid_for_claim"])}

## No-Cancellation And Full-Vector Guard

{markdown_table(rows["guard"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

## Score Readiness Matrix

{markdown_table(rows["readiness"], ["readiness_id", "object", "status", "reason", "score_or_claim_allowed", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["theorem"] = theorem_rows()
    rows["kernel_fill"] = kernel_fill_rows()
    rows["guard"] = guard_rows()
    rows["readiness"] = readiness_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "theorem", "kernel_fill", "guard", "readiness", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2831_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2831_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
