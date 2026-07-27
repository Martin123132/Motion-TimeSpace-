from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from readout_projector_commutator_or_kprojective_gate import (  # noqa: E402
    evaluate_kernel_rows,
    evaluate_projector_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4417"
CLAIM_ID = "L-258"
MARKER = "PPC4161_TRANSITION_READOUT_PROJECTOR_COMMUTATOR_ZERO_OR_KPROJECTIVE_VALUES_4417"
PACKET_MARKER = "PPC4161_PACKET_READOUT_PROJECTOR_COMMUTATOR_ZERO_OR_KPROJECTIVE_VALUES_4417"
DECISION = "PROJECTOR_GAMMA_COMMUTATOR_CLOSED_INSIDE_QEOBS_TAU_BRANCH_PROTOCOL_LEAKAGE_AND_GM_OPEN_NONCLAIM"
NEXT_TARGET = "4418-Y5-R2FR-transition-mass-flux-GM-common-mode-closure-or-source-profile-bound.md"

FORMAL_PATH = FORMAL / "433-PPC4161-transition-readout-projector-commutator-zero-or-Kprojective-values.md"
DOC_PATH = POST / "4417-Y5-R2FR-transition-readout-projector-commutator-zero-or-Kprojective-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4417_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4417_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4417_DERIVATION_ROWS.csv"
PROJECTOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4417_PROJECTOR_COMMUTATOR_INPUT.csv"
PROJECTOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4417_PROJECTOR_COMMUTATOR_OUTPUT.csv"
KPROJECTIVE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4417_KPROJECTIVE_VALUE_INPUT.csv"
KPROJECTIVE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4417_KPROJECTIVE_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4417_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4417_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4417_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4417_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "readout_projector_commutator_or_kprojective_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4417_transition_readout_projector_commutator_zero_or_Kprojective_values.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4416 = SOURCE_DIR / "P8_Y5_R2FR_4416_NEXT_TARGET.csv"
FORMAL_432 = FORMAL / "432-PPC4161-transition-source-readout-SRNG-naturality-or-projective-kernel-values.md"
POST_3572 = POST / "3572-Y5-R2FR-projector-naturality-deltaGammaPi-zero-or-operator-norm.md"
POST_3498 = POST / "3498-Y5-R2FR-projector-naturality-stress-test-or-Kprojector-bound.md"
POST_2124 = POST / "2124-Y5-R2FR-source-feedback-kernel-normal-form-or-first-bounded-row.md"
POST_2123 = POST / "2123-Y5-R2FR-readout-projection-commutator-zero-or-finite-kernel-bound.md"
POST_2122 = POST / "2122-Y5-R2FR-CMSM-live-drop-validator-or-source-readout-owner-lemma.md"
POST_2118 = POST / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
POST_2099 = POST / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"
CSV_3572_STATUS = SOURCE_DIR / "P8_Y5_projector_deltaGamma_naturality_status.csv"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4417_00_4416_next": (
        NEXT_4416,
        "4417-Y5-R2FR-transition-readout-projector-commutator-zero-or-Kprojective-values.md",
        "4416 handoff to projector commutator zero or Kprojective values.",
    ),
    "SRC4417_01_432_formal": (
        FORMAL_432,
        "The public theorem is not closed because",
        "current-chain statement of the projector commutator obstruction.",
    ),
    "SRC4417_02_3572_projector_gamma": (
        POST_3572,
        "delta_Gamma_ind Pi_M=0",
        "projector Gamma naturality closure inside q/e_obs/tau branch.",
    ),
    "SRC4417_03_3572_status": (
        CSV_3572_STATUS,
        "CLOSED_INSIDE_Q_EOBS_TAU_BRANCH_NONCLAIM",
        "canonical projector deltaGamma naturality status.",
    ),
    "SRC4417_04_3498_projector_functor": (
        POST_3498,
        "q/e_obs/tau functor projector",
        "projector naturality stress test and countermodels.",
    ),
    "SRC4417_05_2124_protocol_normal_form": (
        POST_2124,
        "protocol leakage",
        "source-feedback protocol-variable normal form.",
    ),
    "SRC4417_06_2123_commutator_split": (
        POST_2123,
        "pure postprocessing commutators harmless by type",
        "older commutator split: reports closed, source-feedback retained.",
    ),
    "SRC4417_07_2122_commutator_identity": (
        POST_2122,
        "delta(Pi J)=Pi delta J",
        "source/readout owner lemma with exact product rule obstruction.",
    ),
    "SRC4417_08_2118_projective_kernel": (
        POST_2118,
        "KSR2118_6_projective_trace_kernel",
        "projective trace source/readout kernel fallback.",
    ),
    "SRC4417_09_2099_projective_map": (
        POST_2099,
        "DGM2099_6_projective",
        "projective current map into WEP/source/clock/orbital residuals.",
    ),
    "SRC4417_10_gate": (
        GATE_PATH,
        "def evaluate_projector_row",
        "new projector commutator/Kprojective gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    body = text(path)
    if not body or needle not in body:
        return False, -1
    return True, body[: body.index(needle)].count("\n") + 1


def bool_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "PROJ4417_0_import_3572",
            "claim": "The independent-Gamma projector commutator closes inside the q/e_obs/tau-natural LC branch.",
            "derivation": "If Pi=Pi_bar(q(Phi),e_obs(q),tau(q),H_ref,topology) and v is the independent-affine/q-kernel variation with D_v q=D_v e_obs=D_v tau=0, then D_v Pi=0 by the chain rule. With the same-branch source-current zero, D_v(Pi J)=Pi D_v J+(D_v Pi)J=0.",
            "consequence": "The 4416 commutator obstruction is no longer generic for the selected branch; the Gamma/projector piece is branch-closed.",
            "status": "PROJECTOR_GAMMA_COMMUTATOR_ZERO_INSIDE_BRANCH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PROJ4417_1_scope_guard",
            "claim": "Projector Gamma naturality is not metric-stress, mass-flux, or GM calibration closure.",
            "derivation": "A Hodge/e_obs projector can have metric/coframe stress even when it has no independent Gamma slot. Likewise d(Pi J)=0 and measured-GM/common-mode source calibration are separate equations.",
            "consequence": "This protects the result from overclaiming local GR/Newton while still banking the real commutator win.",
            "status": "SCOPE_GUARD_EXPLICIT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PROJ4417_2_protocol_normal_form",
            "claim": "All remaining source-feedback projector leakage is isolated in protocol variables sigma_A.",
            "derivation": "For K_A=Pi_A(y,sigma_A)J_A(y,sigma_A), y=(q,e_obs,A_owned,theta), a vertical variation kills D_v y and leaves D_v K_A=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A]D_v sigma_A.",
            "consequence": "If sigma_A descends through y or is a fixed external protocol, the commutator is zero; otherwise the kernel is L_A epsilon_sigma_A.",
            "status": "PROTOCOL_LEAKAGE_NORMAL_FORM_IMPORTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PROJ4417_3_projective_fallback",
            "claim": "Kprojective remains only for non-natural/projective/source-feedback branches.",
            "derivation": "A projective trace or Gamma-transport projector cannot be erased by the q/e_obs/tau theorem. It requires K_projective, J_norm, support, units, comparator bounds and no-cancellation scoring.",
            "consequence": "The fallback is narrower: it is no longer the default for the selected LC branch, but it remains live for counterbranches and empirical source-feedback protocols.",
            "status": "KPROJECTIVE_FALLBACK_NARROWED_NOT_FILLED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PROJ4417_4_next_physics_gate",
            "claim": "The next non-circling target is mass-flux/GM common-mode closure.",
            "derivation": "Once D_Gamma(Pi J)=0 is branch-closed, the remaining Newton/local-GR source problem is d(Pi_M J_H)=0 plus a measured-GM rule that absorbs only universal common-mode source normalization.",
            "consequence": "The next checkpoint should try to derive flux conservation/common-mode source descent or fill a source-profile bound row.",
            "status": "NEXT_GATE_SELECTED",
            "valid_for_claim": False,
        },
    ]


def projector_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "projector_id": "RPC4417_0_qeobs_tau_LC_branch",
            "projector_class": "q_eobs_tau_natural_mass_source_projector",
            "variation_axis": "independent_Gamma_or_q_kernel_vertical",
            "pi_descends_through_q_eobs_tau": True,
            "support_weights_descend": True,
            "boundary_transport_lc_eobs_or_topology": True,
            "source_current_silent": True,
            "no_gamma_ind_transport": True,
            "no_prevariation_feedback": True,
            "no_calibration_feedback": True,
            "metric_stress_separate": True,
            "flux_closure_separate": True,
            "parent_policy_signed": False,
            "source_path": str(POST_3572),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This imports the 3572 win: D_Gamma Pi and D_Gamma(Pi J) vanish inside the selected q/e_obs/tau LC branch, but it is private/nonclaim.",
        },
        {
            "projector_id": "RPC4417_1_pure_postprocessing_reports",
            "projector_class": "post_variation_report_projector",
            "variation_axis": "after_solve_data_map",
            "pi_descends_through_q_eobs_tau": True,
            "support_weights_descend": True,
            "boundary_transport_lc_eobs_or_topology": True,
            "source_current_silent": True,
            "no_gamma_ind_transport": True,
            "no_prevariation_feedback": True,
            "no_calibration_feedback": True,
            "metric_stress_separate": True,
            "flux_closure_separate": True,
            "parent_policy_signed": False,
            "source_path": str(POST_2123),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Pure reports remain closed by type but do not prove physics source-feedback silence.",
        },
        {
            "projector_id": "RPC4417_2_source_feedback_protocol_leak",
            "projector_class": "source_feedback_or_calibration_protocol",
            "variation_axis": "prevariation_source_feedback",
            "pi_descends_through_q_eobs_tau": True,
            "support_weights_descend": False,
            "boundary_transport_lc_eobs_or_topology": False,
            "source_current_silent": False,
            "no_gamma_ind_transport": True,
            "no_prevariation_feedback": False,
            "no_calibration_feedback": False,
            "metric_stress_separate": True,
            "flux_closure_separate": True,
            "parent_policy_signed": False,
            "source_path": str(POST_2124),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Remaining physical leakage is sigma_A protocol/source-feedback data, not the pure Gamma projector commutator.",
        },
        {
            "projector_id": "RPC4417_3_future_public_projector_contract",
            "projector_class": "future_parent_signed_projector_policy",
            "variation_axis": "all_allowed_local_projector_variations",
            "pi_descends_through_q_eobs_tau": True,
            "support_weights_descend": True,
            "boundary_transport_lc_eobs_or_topology": True,
            "source_current_silent": True,
            "no_gamma_ind_transport": True,
            "no_prevariation_feedback": True,
            "no_calibration_feedback": True,
            "metric_stress_separate": True,
            "flux_closure_separate": True,
            "parent_policy_signed": True,
            "source_path": str(POST_3498),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Complete policy contract; still nonclaim here because it is not parent-signed as the whole public action/readout interface.",
        },
    ]


def kernel_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "kernel_id": "KPV4417_0_source_feedback_sigma",
            "arena": "SOURCE_GM_R10_PPN_ORBIT",
            "residual_symbol": "epsilon_sigma_source_GM",
            "normal_form": "||D_v K_A|| <= (||D_sigma Pi_A||||J_A|| + ||Pi_A||||D_sigma J_A||) ||D_v sigma_A||",
            "lipschitz_factor": "SCHEMA_L_SOURCE_GM_REQUIRED",
            "protocol_leak": "SCHEMA_EPSILON_SIGMA_SOURCE_GM_REQUIRED",
            "K_projective": "SCHEMA_K_SOURCE_GM_REQUIRED",
            "J_norm": "SCHEMA_J_SOURCE_GM_REQUIRED",
            "comparator_bound": "SCHEMA_R10_PPN_ORBIT_BOUND_REQUIRED",
            "source_path": str(POST_2124),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Normal form exists; source profile, GM common-mode calibration and relative source-weight basis still need derivation or sourced values.",
        },
        {
            "kernel_id": "KPV4417_1_projective_trace_counterbranch",
            "arena": "WEP_CLOCK_SOURCE_ORBITAL_COMMON",
            "residual_symbol": "K_projective_trace",
            "normal_form": "Delta_projective^arena = P_projective^arena K_trace J_trace",
            "lipschitz_factor": "SCHEMA_P_PROJECTIVE_REQUIRED",
            "protocol_leak": "SCHEMA_TRACE_SOURCE_SUPPORT_REQUIRED",
            "K_projective": "SCHEMA_K_TRACE_REQUIRED",
            "J_norm": "SCHEMA_J_TRACE_REQUIRED",
            "comparator_bound": "SCHEMA_WEP_CLOCK_SOURCE_ORBITAL_BOUND_REQUIRED",
            "source_path": str(POST_2118),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Retained only for projective/non-natural counterbranches; not needed to close the selected q/eobs/tau Gamma projector gate.",
        },
        {
            "kernel_id": "KPV4417_2_metric_projector_stress",
            "arena": "LOCAL_GR_PPN_R11",
            "residual_symbol": "epsilon_projector_metric_stress",
            "normal_form": "epsilon_metric <= C_stress(partial_readout_P_norm + partial_weight_P_norm + connection_mismatch_norm)",
            "lipschitz_factor": "SCHEMA_C_STRESS_REQUIRED",
            "protocol_leak": "SCHEMA_DOMAIN_STRESS_REQUIRED",
            "K_projective": "SCHEMA_K_METRIC_STRESS_REQUIRED",
            "J_norm": "SCHEMA_J_H_REQUIRED",
            "comparator_bound": "SCHEMA_PPN_R11_BOUND_REQUIRED",
            "source_path": str(POST_3572),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Metric/coframe projector stress is separate from D_Gamma Pi zero and must be derived or bounded before local-GR promotion.",
        },
    ]


def claim_gate_rows(
    projector_output: List[Mapping[str, str]],
    kernel_output: List[Mapping[str, str]],
) -> List[Dict[str, object]]:
    projectors = {row["projector_id"]: row for row in projector_output}
    kernels = {row["kernel_id"]: row for row in kernel_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in projector_output + kernel_output)
    return [
        {
            "gate_id": "CG4417_0_projector_gamma_branch_zero",
            "claim": "D_Gamma Pi and D_Gamma(Pi J) are zero inside q/eobs/tau LC branch",
            "passed": projectors["RPC4417_0_qeobs_tau_LC_branch"].get("current_status")
            == "PROJECTOR_COMMUTATOR_BRANCH_ZERO_NONCLAIM",
            "valid_for_claim": False,
            "detail": "3572/3498 result imported into current chain.",
        },
        {
            "gate_id": "CG4417_1_source_feedback_still_open",
            "claim": "all physical source-feedback projectors are silent",
            "passed": False,
            "valid_for_claim": False,
            "detail": "sigma_A protocol leakage, source profile and GM calibration remain open.",
        },
        {
            "gate_id": "CG4417_2_protocol_normal_form",
            "claim": "remaining source-feedback leakage has finite normal form",
            "passed": kernels["KPV4417_0_source_feedback_sigma"].get("current_status")
            == "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "detail": "L_A epsilon_sigma_A schema exists but values are missing.",
        },
        {
            "gate_id": "CG4417_3_projective_counterbranch_retained",
            "claim": "projective trace fallback is retained only for counterbranch/non-natural rows",
            "passed": kernels["KPV4417_1_projective_trace_counterbranch"].get("current_status")
            == "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "detail": "fallback narrowed but not filled.",
        },
        {
            "gate_id": "CG4417_4_local_GR_Newton_claim",
            "claim": "local GR/Newton/PPN follows",
            "passed": False,
            "valid_for_claim": False,
            "detail": "metric stress, d(Pi_M J_H), H_ref/M_H and GM calibration remain open.",
        },
        {
            "gate_id": "CG4417_5_no_claim_outputs",
            "claim": "no generated row is claim-ready",
            "passed": no_claims,
            "valid_for_claim": False,
            "detail": "branch win is internal/private until remaining selector factors close.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4417_0",
            "decision": DECISION,
            "summary": "4417 lifts the 3498/3572 projector naturality result into the current PPC4161 chain. Inside the q/e_obs/tau-natural LC branch, D_Gamma Pi=0 and D_Gamma(Pi J)=0, so the 4416 projector commutator is closed for the independent-Gamma/source-current gate. This does not close metric projector stress, d(Pi_M J_H), H_ref/M_H, boundary flux or measured-GM/common-mode calibration. The source-feedback normal form from 2124 is retained as L_A epsilon_sigma_A, and Kprojective rows remain schema-only for counterbranches.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "best_result": "D_Gamma_Pi_and_D_Gamma_PiJ_zero_inside_q_eobs_tau_LC_branch",
            "still_missing": "metric_projector_stress; d_PiM_JH_flux_closure; H_ref_M_H_lock; boundary_no_flux; measured_GM_common_mode_source_descent; source_profile_bound_values",
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4417_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive d(Pi_M J_H)=0 plus measured-GM/common-mode source descent from Ward/topological/Euler mass-current closure; if not, fill a source-profile/GM finite bound row.",
            "derive_first": "show the same Hamiltonian source current that is Gamma-silent has conserved projected mass flux and only universal common-mode source normalization enters G_ref M_H.",
            "fallback": "fill epsilon_sigma_source_GM, L_source_GM, source profile/composition, GM calibration equation, H_ref/M_H and comparator bounds.",
            "avoid": "using measured orbital GM as proof; hiding relative source weights in fitted G; treating D_Gamma Pi=0 as metric stress or flux closure.",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: Iterable[Mapping[str, object]]) -> str:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return ""
    headers: List[str] = []
    for row in materialized:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in materialized:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source_register: List[Dict[str, object]],
    projector_output: List[Dict[str, str]],
    kernel_output: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 433 PPC4161 transition: readout projector commutator zero or Kprojective values

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4417 is a real bridge move, not another missing-ledger lap:

- The selected q/e_obs/tau LC branch closes the independent-Gamma projector commutator: `D_Gamma Pi=0` and `D_Gamma(Pi J)=0`.
- This imports and current-chain-signs the 3498/3572 result as a private/nonclaim branch gate.
- Pure postprocessing remains closed by type, but source-feedback protocol leakage remains physical.
- Metric/coframe projector stress, mass-flux closure `d(Pi_M J_H)=0`, H_ref/M_H and measured-GM common-mode calibration are still separate gates.
- Kprojective/projector fallback rows are narrowed to counterbranches and source-feedback protocol leakage; they are not score-ready.

## Source Register

{markdown_table(source_register)}

## Derivation Rows

{markdown_table(rows_from(DERIVATION_ROWS))}

## Projector Commutator Gate

{markdown_table(projector_output)}

## Kprojective / Protocol Leakage Fallback

{markdown_table(kernel_output)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4417 - Y5/R2FR transition readout projector commutator zero or Kprojective values

Private checkpoint for the local-GR/Newton route.

Main result: the projector commutator is now branch-closed where it matters for independent Gamma/source-current leakage. If the projector is a q/e_obs/tau functor and the source current is the same branch current, then `D_Gamma Pi=0` and `D_Gamma(Pi J)=0`. The live obstruction has moved to mass-flux/GM/source-profile closure, not the pure projector Gamma commutator.

No local-GR/Newton/PPN/R10/clock/orbital claim fires. Metric projector stress, `d(Pi_M J_H)`, H_ref/M_H, boundary flux, and measured-GM common-mode source descent remain open.

- Formal mirror: `{FORMAL_PATH}`
- Gate: `{GATE_PATH}`
- Generator: `{GENERATOR_PATH}`
- Validation: `{VALIDATION_PATH}`
- Next: `{NEXT_TARGET}`
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    body = text(path)
    block = f"\n{start}\n{section.rstrip()}\n{end}\n"
    if start in body and end in body:
        prefix = body[: body.index(start)]
        suffix = body[body.index(end) + len(end) :]
        write_text(path, prefix.rstrip() + block + suffix.lstrip("\n"))
    else:
        write_text(path, body.rstrip() + "\n" + block)


def update_claims_register() -> None:
    fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
    rows: List[Dict[str, str]] = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                fieldnames = reader.fieldnames
            rows = [row for row in reader if row.get("claim_id") != CLAIM_ID]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "sector": "local_gr",
        "claim": "4417 closes the independent-Gamma projector commutator inside the q/e_obs/tau-natural LC branch: D_Gamma Pi=0 and D_Gamma(Pi J)=0. This imports the 3498/3572 projector naturality result into the current PPC4161 chain. It remains nonclaim because metric/coframe projector stress, d(Pi_M J_H), H_ref/M_H, boundary flux and measured-GM/common-mode source calibration remain open. Kprojective/source-feedback fallback rows are narrowed to counterbranches and protocol leakage but lack values.",
        "current_evidence": "4417 source register, derivation rows, projector commutator output, Kprojective/protocol leakage output, claim gates, decision, status, next target and validation CSV.",
        "evidence": "4417 source register, derivation rows, projector commutator output, Kprojective/protocol leakage output, claim gates, decision, status, next target and validation CSV.",
        "status": "projector_Gamma_commutator_closed_inside_branch_flux_GM_metric_stress_open_nonclaim",
        "next_test": "Derive d(Pi_M J_H)=0 plus measured-GM/common-mode source descent, or fill a source-profile/GM finite bound row.",
        "next_action": "Derive d(Pi_M J_H)=0 plus measured-GM/common-mode source descent, or fill a source-profile/GM finite bound row.",
        "key_risk": "Treating D_Gamma Pi=0 as full metric projector stress silence, flux closure, or measured-GM calibration; hiding relative source weights in fitted G.",
        "risk": "Treating D_Gamma Pi=0 as full metric projector stress silence, flux closure, or measured-GM calibration; hiding relative source weights in fitted G.",
    }
    for key in claim_row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4417 local spine update: projector Gamma commutator branch-closed

4417 imports the 3498/3572 projector naturality theorem into the current local-GR chain. In the q/e_obs/tau-natural LC branch, `D_Gamma Pi=0`, and with the same branch source-current zero, `D_Gamma(Pi J)=0`. That means the 4416 projector commutator is no longer the live independent-Gamma obstruction inside the selected branch. The live source route has moved forward to metric projector stress, mass-flux closure `d(Pi_M J_H)=0`, H_ref/M_H, boundary flux and measured-GM/common-mode source descent."""
    packet_section = """## 4417 packet update: the projector commutator is not the monster anymore

Inside the selected LC branch, q/e_obs/tau naturality kills the Gamma-projector product-rule term. Keep the scope tight: this does not prove Newton or local GR. The next physics gate is source mass flux and calibrated GM: prove the projected Hamiltonian source charge is conserved/common-mode, or fill the source-profile/GM bound row."""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    source_register = rows_from(SOURCE_REGISTER)
    projector_output = rows_from(PROJECTOR_OUTPUT)
    kernel_output = rows_from(KPROJECTIVE_OUTPUT)
    claim_gates = rows_from(CLAIM_GATES)
    projectors = {row["projector_id"]: row["current_status"] for row in projector_output}
    kernels = {row["kernel_id"]: row["current_status"] for row in kernel_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in projector_output + kernel_output + claim_gates)
    checks = [
        ("VAL4417_0_sources_exist", all(row["path_exists"] == "True" for row in source_register), "every cited source path exists"),
        ("VAL4417_1_source_needles_found", all(row["needle_found"] == "True" for row in source_register), "every cited source needle was found"),
        (
            "VAL4417_2_qeobs_projector_branch_zero",
            projectors.get("RPC4417_0_qeobs_tau_LC_branch") == "PROJECTOR_COMMUTATOR_BRANCH_ZERO_NONCLAIM",
            "q/eobs/tau LC projector commutator is branch-zero nonclaim",
        ),
        (
            "VAL4417_3_postprocessing_closed",
            projectors.get("RPC4417_1_pure_postprocessing_reports") == "PROJECTOR_COMMUTATOR_BRANCH_ZERO_NONCLAIM",
            "pure postprocessing report projectors remain closed by type",
        ),
        (
            "VAL4417_4_source_feedback_blocked",
            projectors.get("RPC4417_2_source_feedback_protocol_leak")
            == "PROJECTOR_COMMUTATOR_BLOCKED_FEEDBACK_OR_SUPPORT",
            "source-feedback protocol leakage remains open",
        ),
        (
            "VAL4417_5_source_feedback_schema",
            kernels.get("KPV4417_0_source_feedback_sigma") == "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "source-feedback L epsilon schema is ready but values missing",
        ),
        (
            "VAL4417_6_projective_counterbranch_schema",
            kernels.get("KPV4417_1_projective_trace_counterbranch") == "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "projective counterbranch schema retained",
        ),
        (
            "VAL4417_7_metric_stress_schema",
            kernels.get("KPV4417_2_metric_projector_stress") == "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "metric projector stress schema retained separately",
        ),
        ("VAL4417_8_no_claim_outputs", no_claims, "no generated gate row is valid for claim"),
        ("VAL4417_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-258"),
        ("VAL4417_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4417_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4417_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4417_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4417_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4417_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(PROJECTOR_INPUT, projector_input_rows())
    write_csv(KPROJECTIVE_INPUT, kernel_input_rows())
    write_csv(PROJECTOR_OUTPUT, evaluate_projector_rows(PROJECTOR_INPUT))
    write_csv(KPROJECTIVE_OUTPUT, evaluate_kernel_rows(KPROJECTIVE_INPUT))
    projector_output = rows_from(PROJECTOR_OUTPUT)
    kernel_output = rows_from(KPROJECTIVE_OUTPUT)
    claim_gates = claim_gate_rows(projector_output, kernel_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_register = rows_from(SOURCE_REGISTER)
    write_text(FORMAL_PATH, build_doc(source_register, projector_output, kernel_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(
        VALIDATION_PATH,
        validation_rows(
            {
                "formal": FORMAL_PATH,
                "post": DOC_PATH,
                "next": NEXT_CSV,
            }
        ),
    )


if __name__ == "__main__":
    main()
