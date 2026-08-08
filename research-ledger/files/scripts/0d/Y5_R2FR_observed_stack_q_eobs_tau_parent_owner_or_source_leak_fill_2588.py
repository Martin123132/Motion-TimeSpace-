from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_OBSERVED_STACK_Q_EOBS_TAU_2588"
CHECKPOINT_ID = "2588"

DOC = ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_OBS_STACK_2588_SOURCE_REGISTER.csv",
    "descent_audit": OUT / "P8_Y5_OBS_STACK_2588_Q_OBSE_TAU_DESCENT_AUDIT.csv",
    "owner_certificate": OUT / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
    "leak_rows": OUT / "P8_Y5_OBS_STACK_2588_SOURCE_LEAK_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_OBS_STACK_2588_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_OBS_STACK_2588_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_OBS_STACK_2588_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_OBS_STACK_2588_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_OBS_STACK_2588_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2588_VALIDATION.csv",
}

COPY_TARGETS = {
    "descent_audit": QUEUE / "JR2588_OBSERVED_STACK_DESCENT_AUDIT_NONCLAIM.csv",
    "owner_certificate": QUEUE / "JR2588_OBSERVED_STACK_OWNER_CERTIFICATE_NONCLAIM.csv",
    "leak_rows": LOCAL_BOUNDS / "Observed_stack_q_eobs_tau_leak_rows_2588_NONCLAIM.csv",
    "next_target": QUEUE / "JR2588_VERTICAL_KERNEL_NULLNESS_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2588_00_2587_handoff",
            "source_path": ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            "needles": ["NEXT2587_0_selected", "AD2587_2_eobs_tau", "VAL2587_OVERALL"],
            "role": "active handoff selecting observed-stack q/e_obs/tau owner",
        },
        {
            "source_id": "SRC2588_01_2390_same_frame",
            "source_path": ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "needles": ["SFL2390_0_pullback_definition", "SFC2390_7_MHref", "VAL2390_OVERALL"],
            "role": "prior same-frame coframe/tau lock and leak rows",
        },
        {
            "source_id": "SRC2588_02_2391_q_obse",
            "source_path": ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md",
            "needles": ["QOF2391_1_basic_coframe", "QOC2391_2_presymplectic_null", "VAL2391_OVERALL"],
            "role": "q/Obs_e quotient-basic descent contract and tautology guard",
        },
        {
            "source_id": "SRC2588_03_2528_q_chart",
            "source_path": ROOT / "2528-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
            "needles": ["FCE2528_3_computable_q", "NPS2528_5_selector_verdict", "VAL2528_OVERALL"],
            "role": "q field-chart/equivalence route and no-pole selector warning",
        },
        {
            "source_id": "SRC2588_04_2389_cert",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv",
            "needles": ["OCC2389_0_q_map", "OCC2389_1_eobs_pullback", "OCC2389_3_tau_owner"],
            "role": "current-owner certificate rows for q/e_obs/tau gaps",
        },
        {
            "source_id": "SRC2588_05_tau_contract",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "needles": ["TGC685_0_define_tau_obs", "TGC685_6_verdict"],
            "role": "tau generator source/charge/clock/orbit/boundary contract",
        },
        {
            "source_id": "SRC2588_06_2587_contract",
            "source_path": QUEUE / "JR2587_MIN_PARENT_MATTER_ACTION_CONTRACT_NONCLAIM.csv",
            "needles": ["MCA2587_1_observed_stack", "MCA2587_6_descent_output"],
            "role": "minimal parent matter action contract requiring observed stack ownership",
        },
        {
            "source_id": "SRC2588_07_2587_domain",
            "source_path": LOCAL_BOUNDS / "Minimal_parent_matter_domain_rows_2587_NONCLAIM.csv",
            "needles": ["DM2587_1_q_stack", "DM2587_2_tau_ellJ"],
            "role": "q/frame/tau/ellJ leak rows inherited from 2587",
        },
        {
            "source_id": "SRC2588_08_2587_validation",
            "source_path": OUT / "P8_Y5_BRR545_2587_VALIDATION.csv",
            "needles": ["VAL2587_OVERALL", "PASS"],
            "role": "previous checkpoint validation",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                }
            )
        )
    return rows


def descent_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "OSA2588_0_observed_stack_target",
            "claim_piece": "single observed stack",
            "formal_statement": "q(Phi) -> e_obs(q), D_obs(q), A_obs(q), tau(q), ell_J(q) is selected before matter variation and before readout",
            "current_status": "TARGET_CONTRACT_EXPLICIT",
            "blocking_gap": "q, Obs_e, tau and ell_J are not parent-constructed for current MTS",
            "effect": "MCA2587 remains a disciplined ansatz rather than source-current proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_1_quotient_existence",
            "claim_piece": "parent quotient q",
            "formal_statement": "a parent vertical distribution V is regular, involutive, free/proper enough locally, and q:Phi_parent->Q_vis is the quotient submersion",
            "current_status": "NOT_PARENT_SIGNED",
            "blocking_gap": "V, rank, bracket/integrability and quotient target are not supplied by the parent action",
            "effect": "q cannot be used as a proof object yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_2_basic_coframe",
            "claim_piece": "observed coframe descends through q",
            "formal_statement": "Lie_v e_parent=0 for every v in V, hence e_parent=Obs_e o q and DObs_e[Dq(v)]=0",
            "current_status": "EXACT_CONDITIONAL_DESCENT_THEOREM",
            "blocking_gap": "basic coframe proof or DObs_e source-weighted bound is missing",
            "effect": "frame-source silence is conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_3_tautology_guard",
            "claim_piece": "no projection-by-declaration",
            "formal_statement": "q_candidate may not include e_obs as a tautological component unless ker(Dq_candidate) is independently null and matter-invisible",
            "current_status": "ANTI_TAUTOLOGY_GUARD_ACTIVE",
            "blocking_gap": "presymplectic-null and matter-invisible kernel certificates are missing",
            "effect": "prevents importing GR-looking coframe success as q ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_4_same_frame_readout",
            "claim_piece": "matter, clocks, rods, photons, orbit and source charge use the same e_obs",
            "formal_statement": "e_source=e_clock=e_photon=e_ruler=e_orbit=e_obs(q)",
            "current_status": "CONDITIONAL_SAME_FRAME_CONTRACT",
            "blocking_gap": "all-sector readout functor and no-shadow-frame theorem are unsigned",
            "effect": "Delta_frame_source_over_MH remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_5_tau_identity",
            "claim_piece": "single tau",
            "formal_statement": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs[e_obs]",
            "current_status": "MISSING_PARENT_TAU_IDENTITY",
            "blocking_gap": "Killing/clock/Hamiltonian/boundary normalization not signed as one generator",
            "effect": "epsilon_tau_selector remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_6_ellJ_identity",
            "claim_piece": "source-current scale functor",
            "formal_statement": "ell_J=ell_J(q) is fixed by parent normalization and not fitted from GM, PPN or local bounds",
            "current_status": "MISSING_PARENT_ELLJ_SCALE",
            "blocking_gap": "no action-normalized source for ell_J exists",
            "effect": "epsilon_tau_ellJ/source-normalization scale leak remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OSA2588_7_verdict",
            "claim_piece": "observed-stack parent owner theorem",
            "formal_statement": "q/e_obs/tau/ell_J are parent-owned and all matter/readout/source maps factor through them before readout",
            "current_status": "OBSERVED_STACK_OWNER_NOT_DERIVED_CURRENT_CORPUS",
            "blocking_gap": "OSA2588_1 through OSA2588_6 remain unsigned",
            "effect": "MCA2587 and J_H=q^*Jbar_H cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def owner_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "certificate_id": "OSC2588_0_q_map",
            "required_certificate": "parent q map",
            "required_test": "q(Phi) components, target Q_vis, Dq matrix and vertical basis are written with constant rank on an open branch",
            "current_status": "MISSING_PARENT_Q_MAP",
            "residual_if_missing": "epsilon_q_owner",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_1_vertical_kernel",
            "required_certificate": "kernel is parent-null and matter-invisible",
            "required_test": "ker(Dq) directions carry zero Hamiltonian/symplectic/source charge and are invisible to matter before readout",
            "current_status": "MISSING_PRESYMPLECTIC_NULL_KERNEL",
            "residual_if_missing": "epsilon_kernel_charge;epsilon_projection_declaration",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_2_Obs_e",
            "required_certificate": "observed coframe functor",
            "required_test": "e_parent is basic over q, or Lie_v e_parent/DObs_e has a sourced finite bound",
            "current_status": "MISSING_PARENT_OBS_E_FUNCTOR",
            "residual_if_missing": "epsilon_DObs_e",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_3_same_readout",
            "required_certificate": "all-sector same-frame readout",
            "required_test": "matter, source, clocks, rods, photons, orbit, PPN projectors and support maps all use e_obs(q)",
            "current_status": "MISSING_ALL_SECTOR_SAME_FRAME_SIGNATURE",
            "residual_if_missing": "Delta_frame_source_over_MH;alpha_readout_or_Delta_W_support",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_4_tau",
            "required_certificate": "parent tau identity",
            "required_test": "one tau_obs is used for source, Hamiltonian charge, clocks, boundary reference and orbit",
            "current_status": "MISSING_PARENT_TAU_IDENTITY",
            "residual_if_missing": "epsilon_tau_selector",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_5_ellJ",
            "required_certificate": "parent ell_J scale",
            "required_test": "ell_J is action-normalized, constant/universal on the branch, or has a parent exchange identity",
            "current_status": "MISSING_PARENT_ELLJ_SCALE",
            "residual_if_missing": "epsilon_ellJ_scale",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_6_no_shadow",
            "required_certificate": "no shadow frame or source prefactor",
            "required_test": "no Weyl/disformal/species/source-prefactor/non-Hilbert-current/readout-tail variable survives outside q/e_obs",
            "current_status": "MISSING_NO_SHADOW_FRAME_THEOREM",
            "residual_if_missing": "epsilon_shadow_frame",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "OSC2588_7_MHref",
            "required_certificate": "positive same-frame M_H_ref",
            "required_test": "H_tau-H_ref is derived in the same q/e_obs/tau branch with no orbital-GM import",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "rows remain non-score-ready",
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "OSL2588_0_q_owner",
            "symbol": "epsilon_q_owner",
            "definition": "abs(int_S(J_H[q_candidate]-J_H[q_parent]))/M_H_ref",
            "needed_for_claim": "parent q map, J_H density and positive same-frame M_H_ref",
            "current_status": "MISSING_PARENT_Q_MAP",
            "units": "dimensionless",
            "observable_link": "source_normalization;PPN;R11;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_1_DObs_e",
            "symbol": "epsilon_DObs_e",
            "definition": "||Lie_v e_parent||_source_weighted / ||e_parent||",
            "needed_for_claim": "basic coframe proof or vertical basis, source weight and operator norm",
            "current_status": "MISSING_BASIC_COFRAME_PROOF_OR_BOUND",
            "units": "dimensionless_frame_response",
            "observable_link": "frame_source;clock;PPN;R10",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_2_frame_source",
            "symbol": "Delta_frame_source_over_MH",
            "definition": "abs(int_S(T_a[e_source]-T_a[e_obs]) tau^a)/M_H_ref",
            "needed_for_claim": "same-frame readout theorem and M_H_ref denominator",
            "current_status": "MISSING_SAME_FRAME_LOCK_OR_BOUND",
            "units": "dimensionless",
            "observable_link": "WEP;source_normalization;PPN;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_3_tau_selector",
            "symbol": "epsilon_tau_selector",
            "definition": "abs(int_S T_a(tau_role^a-tau_obs^a))/M_H_ref",
            "needed_for_claim": "single parent tau identity and same-frame source density",
            "current_status": "MISSING_PARENT_TAU_IDENTITY",
            "units": "dimensionless",
            "observable_link": "clock;Hamiltonian_charge;orbit;source_mass",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_4_ellJ_scale",
            "symbol": "epsilon_ellJ_scale",
            "definition": "source-current scale drift or mismatch from non-parent ell_J",
            "needed_for_claim": "parent ell_J theorem or finite scale-drift bound",
            "current_status": "MISSING_PARENT_ELLJ_SCALE",
            "units": "dimensionless_or_scale_drift",
            "observable_link": "Gdot;source_normalization;orbital;PPN",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_5_shadow_frame",
            "symbol": "epsilon_shadow_frame",
            "definition": "abs(b_g)+abs(b_dis)+abs(b_A)+abs(q_nonH)+abs(source_prefactor_leak)",
            "needed_for_claim": "no-shadow-frame/source-prefactor theorem or finite source-backed coefficients",
            "current_status": "MISSING_NO_SHADOW_FRAME_THEOREM_OR_VALUES",
            "units": "dimensionless",
            "observable_link": "WEP;R10;R11;clock;PPN",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_6_readout_support",
            "symbol": "alpha_readout_or_Delta_W_support",
            "definition": "projector/readout tail plus source-worldtube support retune under observed-stack choice",
            "needed_for_claim": "projector/support descent and no-retune theorem",
            "current_status": "MISSING_PROJECTOR_SUPPORT_DESCENT_OR_BOUND",
            "units": "dimensionless",
            "observable_link": "R10;orbital;PPN;source_normalization",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "OSL2588_TOTAL",
            "symbol": "Delta_observed_stack_total_over_MH",
            "definition": "absolute no-cancellation observed-stack/source-frame obstruction",
            "needed_for_claim": "all q/e_obs/tau/ellJ/no-shadow/readout terms theorem-zero or source-backed finite with M_H_ref",
            "current_status": "TOTAL_OBSERVED_STACK_RETAINED_NONCLAIM",
            "units": "dimensionless_after_MHref",
            "observable_link": "MCA2587;J_H;J_domain;PiM_chainmap;Newton;PPN;R10;R11;local_GR",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def runner_refusal_rows(rows_in: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in rows_in:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"OSR2588_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;MISSING_SOURCE_PATH;VALID_FOR_CLAIM_FALSE",
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2588_0_descent_shape",
            "claim": "observed-stack descent theorem shape is written",
            "gate_status": "PASS_NONCLAIM",
            "reason": "regular quotient plus basic coframe would give e_obs=Obs_e(q) and DObs_e[Dq(v)]=0",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2588_1_parent_q",
            "claim": "parent q map and vertical quotient are constructed",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "V, q components, rank, integrability and target Q_vis are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2588_2_basic_coframe",
            "claim": "e_parent is basic over q",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Lie_v e_parent=0 or DObs_e bound is missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2588_3_tau_ellJ",
            "claim": "tau and ell_J are parent-owned observed-stack functors",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "single tau generator and parent ell_J scale are not derived",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2588_4_source_leak_score",
            "claim": "q/frame/tau/ellJ leak rows are score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "rows lack numeric values, source paths, M_H_ref and arena kernels",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2588_5_Newton_local_GR",
            "claim": "Newton/local-GR source bridge is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "observed-stack descent is necessary but current owner certificates are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2588_0_accept_descent_shape",
            "decision": "QUOTIENT_BASIC_COFRAME_ROUTE_ACCEPTED_CONDITIONAL",
            "reason": "regular parent quotient plus basic coframe gives the exact observed-stack chain-rule theorem",
            "effect": "same-frame/source-current silence becomes derivable only after parent q/kernel/basic-coframe certificates",
        },
        {
            "decision_id": "DEC2588_1_reject_tautology",
            "decision": "REJECT_Q_BY_DECLARATION",
            "reason": "including e_obs in q is not a proof unless the kernel is independently null and matter-invisible",
            "effect": "projection-declaration becomes an explicit blocker instead of a hidden assumption",
        },
        {
            "decision_id": "DEC2588_2_no_promotion",
            "decision": "OBSERVED_STACK_OWNER_NOT_PROVED",
            "reason": "parent q, Obs_e, tau, ell_J, no-shadow, all-sector readout and M_H_ref are unsigned",
            "effect": "MCA2587, J_H ownership, Newton and local-GR claims remain blocked",
        },
        {
            "decision_id": "DEC2588_3_next",
            "decision": "VERTICAL_KERNEL_NULLNESS_SELECTED_NEXT",
            "reason": "without a parent-null/matter-invisible kernel, no q/Obs_e quotient construction is claim-grade",
            "effect": "2589 should prove V=ker(Dq) is presymplectic-null and matter-invisible, or fill kernel-charge/source rows",
        },
    ]
    return [with_stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2588_0_selected",
            "selection_status": "selected",
            "target_file": "2589-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
            "target_script": "scripts/Y5_R2FR_vertical_kernel_presymplectic_null_and_matter_invisible_or_kernel_charge_row_2589.py",
            "task": "prove V=ker(Dq) is parent presymplectic-null, matter-invisible and zero compact-flux so q/Obs_e is not projection-by-declaration, or fill epsilon_kernel_charge, epsilon_q_rank_or_integrability and epsilon_projection_declaration rows",
            "acceptance_target": "kernel nullness and matter invisibility make q/Obs_e ownership claim-grade, or kernel-charge/source leak rows become source-ready nonclaim residuals",
            "guardrails": "no q=(e_obs,...) tautology; no standard-GR frame import; no fitted GM or M_H_ref; no post-readout tau/frame; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2588_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2588_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2588_01_descent_shape_written",
        any(row["audit_id"] == "OSA2588_2_basic_coframe" and row["current_status"] == "EXACT_CONDITIONAL_DESCENT_THEOREM" for row in data["descent_audit"]),
        "quotient/basic-coframe descent route is recorded",
    )
    add(
        "VAL2588_02_tautology_guard",
        any(row["audit_id"] == "OSA2588_3_tautology_guard" for row in data["descent_audit"]),
        "projection-by-declaration guard is active",
    )
    add(
        "VAL2588_03_owner_not_promoted",
        any(row["audit_id"] == "OSA2588_7_verdict" and row["valid_for_claim"] is False for row in data["descent_audit"]),
        "observed-stack owner theorem remains blocked",
    )
    add(
        "VAL2588_04_owner_certificates_blocked",
        all(row["valid_for_claim"] is False for row in data["owner_certificate"]),
        "all observed-stack owner certificates remain nonclaim",
    )
    add(
        "VAL2588_05_leak_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["leak_rows"]),
        "q/frame/tau/ellJ leak rows remain nonclaim",
    )
    add(
        "VAL2588_06_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses unfilled observed-stack rows",
    )
    add(
        "VAL2588_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no observed-stack, source-current, Newton or local-GR claim is allowed",
    )
    add(
        "VAL2588_08_next_target_written",
        any(row["route_id"] == "NEXT2588_0_selected" for row in data["next"]),
        "2589 vertical-kernel nullness target selected",
    )
    add(
        "VAL2588_09_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2588-Y5-R2FR-observed-stack*",
            "*Y5_R2FR_observed_stack_q_eobs_tau*",
            "*P8_Y5_OBS_STACK_2588*",
            "*JR2588*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2588_10_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2588 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2588_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2588_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2588_OVERALL",
        overall,
        "2588 records the observed-stack quotient/basic-coframe route, refuses tautological q promotion, keeps leak rows nonclaim, and selects vertical-kernel nullness next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2588 Y5 R2FR observed-stack q eobs tau parent owner or source leak fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The observed-stack route is exact as a conditional descent theorem, but current MTS does not yet parent-own `q`, `Obs_e`, `tau`, or `ell_J`.",
        "",
        "**Main result:** if a parent vertical distribution `V` forms a regular quotient `q:Phi_parent -> Q_vis`, and the parent coframe is basic over that quotient, then `e_obs=Obs_e(q(Phi))` and `DObs_e[Dq(v)]=0` for `v in ker(Dq)`. That would make the same-frame matter/source route genuinely derivable. Current MTS has not proved the kernel is parent-null/matter-invisible or that the coframe/tau/ell_J stack is basic; so `epsilon_q_owner`, `epsilon_DObs_e`, `Delta_frame_source_over_MH`, and `epsilon_tau_selector` remain nonclaim.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Descent Audit",
        markdown_table(data["descent_audit"], ["audit_id", "claim_piece", "formal_statement", "current_status", "blocking_gap", "effect", "valid_for_claim", "claim_allowed"]),
        "",
        "## Owner Certificate",
        markdown_table(data["owner_certificate"], ["certificate_id", "required_certificate", "required_test", "current_status", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Source Leak Rows",
        markdown_table(data["leak_rows"], ["row_id", "symbol", "definition", "needed_for_claim", "current_status", "units", "observable_link", "numeric_value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed"]),
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
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    leak_rows_data = leak_rows()
    data = {
        "sources": source_register_rows(),
        "descent_audit": descent_audit_rows(),
        "owner_certificate": owner_certificate_rows(),
        "leak_rows": leak_rows_data,
        "runner_refusal": runner_refusal_rows(leak_rows_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["descent_audit"], data["descent_audit"])
    write_csv(OUTPUTS["owner_certificate"], data["owner_certificate"])
    write_csv(OUTPUTS["leak_rows"], data["leak_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2588_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
