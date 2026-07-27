from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lambda_curvature_source_gate import evaluate_bound_rows as evaluate_lambda_bound_rows  # noqa: E402
from local_cosmological_residual_gate import (  # noqa: E402
    evaluate_classifier_rows,
    evaluate_payload_rows,
    read_csv,
    write_csv,
)
from ricci_uu_source_bound_runner import evaluate_bound_rows as evaluate_ricci_bound_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4403"
CLAIM_ID = "L-244"
MARKER = "PPC4161_TRANSITION_LAMBDA_EFF_RESIDUAL_ZERO_OR_LOCAL_COSMOLOGICAL_PAYLOAD_BOUND_4403"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_LAMBDA_EFF_RESIDUAL_ZERO_OR_LOCAL_COSMOLOGICAL_PAYLOAD_BOUND_4403"
DECISION = "LOCAL_RESIDUAL_VECTOR_FACTORED_PRIVATE_ZEROS_AND_SURVIVOR_PAYLOAD_RUNNER_READY"
NEXT_TARGET = "4404-Y5-R2FR-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"

FORMAL_PATH = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
DOC_PATH = POST / "4403-Y5-R2FR-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4403_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

LOCAL_GATE_PATH = SCRIPT_DIR / "local_cosmological_residual_gate.py"
RICCI_RUNNER_PATH = SCRIPT_DIR / "ricci_uu_source_bound_runner.py"
LAMBDA_GATE_PATH = SCRIPT_DIR / "lambda_curvature_source_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4403_transition_Lambda_eff_residual_zero_or_local_cosmological_payload_bound.py"

CLASSIFIER_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_CLASSIFIER_INPUT.csv"
CLASSIFIER_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_CLASSIFIER_OUTPUT.csv"
PAYLOAD_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_COSMOLOGICAL_PAYLOAD_INPUT.csv"
PAYLOAD_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_COSMOLOGICAL_PAYLOAD_OUTPUT.csv"
RICCI_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_RICCI_FROM_RESIDUAL_INPUT.csv"
RICCI_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_RICCI_FROM_RESIDUAL_OUTPUT.csv"
LAMBDA_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LAMBDA_FROM_RESIDUAL_INPUT.csv"
LAMBDA_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4403_LAMBDA_FROM_RESIDUAL_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4402 = SOURCE_DIR / "P8_Y5_R2FR_4402_NEXT_TARGET.csv"
DERIVATIONS_4402 = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_DERIVATIONS.csv"
RICCI_OUTPUT_4402 = SOURCE_DIR / "P8_Y5_R2FR_4402_RICCI_UU_SOURCE_BOUND_OUTPUT.csv"
CLASSIFIER_4279 = SOURCE_DIR / "P8_Y5_R2FR_4279_RESIDUAL_CLASSIFIER.csv"
ZERO_4279 = SOURCE_DIR / "P8_Y5_R2FR_4279_DERIVED_ZERO_SUBSET.csv"
SURVIVOR_4279 = SOURCE_DIR / "P8_Y5_R2FR_4279_SURVIVOR_BOUND_PACK.csv"
CGAMMA_4279 = SOURCE_DIR / "P8_Y5_R2FR_4279_CGAMMA_FULL_BUDGET_TARGETS.csv"
FORMAL_294 = FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4403_0_4402_next": (
        NEXT_4402,
        "4403-Y5-R2FR-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md",
        "4402 handoff to local Lambda/residual payload.",
    ),
    "SRC4403_1_4402_derivation": (
        DERIVATIONS_4402,
        "RUU4402_1_exact_local_vacuum_zero_requires_Lambda_and_residual_silence",
        "4402 proof that matter vacuum still needs Lambda/residual silence.",
    ),
    "SRC4403_2_4402_ricci_runner": (
        RICCI_OUTPUT_4402,
        "RUB4402_2_small_residual_schema_nonclaim",
        "4402 Ricci source-bound output.",
    ),
    "SRC4403_3_4279_classifier": (
        CLASSIFIER_4279,
        "RC4279_6_Lambda",
        "4279 residual classifier with Lambda and survivor status.",
    ),
    "SRC4403_4_4279_zero_subset": (
        ZERO_4279,
        "ZERO4279_4_c_bdy_compact",
        "4279 private-zero subset.",
    ),
    "SRC4403_5_4279_survivors": (
        SURVIVOR_4279,
        "SURV4279_5_Lambda",
        "4279 survivor-bound pack.",
    ),
    "SRC4403_6_4279_cgamma_targets": (
        CGAMMA_4279,
        "CGT4279_0_Gdot",
        "4279 cGamma local budget targets.",
    ),
    "SRC4403_7_294_left_hand": (
        FORMAL_294,
        "E_res_mu_nu",
        "4278/294 left-hand residual tensor statement.",
    ),
    "SRC4403_8_local_gate": (
        LOCAL_GATE_PATH,
        "def evaluate_payload_rows",
        "New local cosmological/residual payload gate.",
    ),
    "SRC4403_9_ricci_runner": (
        RICCI_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Ricci_uu runner used after residual vector assembly.",
    ),
    "SRC4403_10_lambda_gate": (
        LAMBDA_GATE_PATH,
        "def evaluate_bound_rows",
        "Lambda/lambda elliptic runner used after Ricci score.",
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + block)


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
        write_text(path, text)
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(text and needle in text)),
                "valid_for_claim": "False",
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "LCR4403_0_residual_tensor_factorization",
            "statement": "The local residual tensor entering R_uu decomposes into private-zero channels plus retained survivor channels.",
            "derivation": "Use the 4279 classifier: c_D and delta_kappa are private selector zeros; static Kperp/c_T and compact c_bdy are privately routed; extra Poynting is Hilbert EM and not a second source. The retained local residual payload is c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion, and any open boundary/projector leakage.",
            "new_information": "E_res is no longer a blob: the current private branch has a named survivor vector.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCR4403_1_local_Ruu_residual_payload_law",
            "statement": "In matter vacuum the no-cancellation payload is |R_uu| <= |E_surv,uu| + 1/2 |E_surv| + |Lambda_eff| + |B_projector|.",
            "derivation": "Insert the 4403 factorization into the 4402 trace-reversed law and use absolute sums. Private-zero channels are not allowed to cancel survivor channels; retained channels are added as positive payloads.",
            "new_information": "The Ricci/lambda obstruction now has a scored local residual vector rather than a free-form residual tensor.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCR4403_2_Lambda_eff_scale_law",
            "statement": "A local Lambda_eff contribution can be negligible only by a declared local scale law |Lambda_eff| L_local^2 below the arena metric budget, or by a parent subtraction/zero theorem.",
            "derivation": "The weak-field de Sitter potential contribution scales as Lambda_eff r^2, while the Ricci source contribution scales directly as Lambda_eff in R_uu. Thus a local claim needs either parent-zero/subtraction on W_H or a source-backed L_local and Lambda_eff bound.",
            "new_information": "Cosmological smallness is usable as a bound route, but it is not the same as parent zero.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "LCR4403_3_survivor_priority",
            "statement": "After private zeros, c_Gamma remains the leading local survivor because it couples to Gdot, preferred-location, stress nonconservation, clocks, WEP and R10 budgets.",
            "derivation": "4279 already gives product budgets for c_Gamma but no source-backed profile coefficients. c_R2, Lambda_eff and spin/torsion also remain, but their local payload can be bounded once scales/support are supplied; c_Gamma is the broadest multi-arena bottleneck.",
            "new_information": "The next non-circling target is a first live c_Gamma profile row or a parent memory no-hair proof.",
            "valid_for_claim": "False",
        },
    ]


def classifier_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "coefficient_id": "LRC4403_0_cD",
            "coefficient": "c_D",
            "residual_role": "second_metric_disformal",
            "current_status": "PRIVATE_STANDARD_BRANCH_ZERO",
            "private_zero_basis": "True",
            "parent_zero_signed": "False",
            "same_support": "True",
            "public_scope_allowed": "False",
            "retained_bound_route": "False",
            "source_path": str(ZERO_4279),
            "input_valid_for_claim": "False",
            "notes": "Private selector zero only; no public parent claim.",
        },
        {
            "coefficient_id": "LRC4403_1_delta_kappa",
            "coefficient": "delta_kappa",
            "residual_role": "source_coupling_drift",
            "current_status": "PRIVATE_STANDARD_BRANCH_ZERO",
            "private_zero_basis": "True",
            "parent_zero_signed": "False",
            "same_support": "True",
            "public_scope_allowed": "False",
            "retained_bound_route": "False",
            "source_path": str(ZERO_4279),
            "input_valid_for_claim": "False",
            "notes": "Private kappa lock; numerical G still calibrated, not predicted.",
        },
        {
            "coefficient_id": "LRC4403_2_Kperp_static",
            "coefficient": "Kperp/c_T_static",
            "residual_role": "extra_static_tensor_force",
            "current_status": "PRIVATE_COMPACT_SELECTOR_ZERO",
            "private_zero_basis": "True",
            "parent_zero_signed": "False",
            "same_support": "True",
            "public_scope_allowed": "False",
            "retained_bound_route": "False",
            "source_path": str(ZERO_4279),
            "input_valid_for_claim": "False",
            "notes": "Private static Kperp routed; public no-independent-TT theorem unsigned.",
        },
        {
            "coefficient_id": "LRC4403_3_cPoynt_extra",
            "coefficient": "c_Poynt_extra",
            "residual_role": "extra_EM_Poynting_source",
            "current_status": "PRIVATE_VISIBLE_EM_ZERO",
            "private_zero_basis": "True",
            "parent_zero_signed": "False",
            "same_support": "True",
            "public_scope_allowed": "False",
            "retained_bound_route": "False",
            "source_path": str(ZERO_4279),
            "input_valid_for_claim": "False",
            "notes": "Poynting is Hilbert EM flux in the visible branch, not a second source.",
        },
        {
            "coefficient_id": "LRC4403_4_c_bdy_compact",
            "coefficient": "c_bdy_compact",
            "residual_role": "compact_boundary_edge_charge",
            "current_status": "PRIVATE_COMPACT_COLLAR_ROUTED",
            "private_zero_basis": "True",
            "parent_zero_signed": "False",
            "same_support": "True",
            "public_scope_allowed": "False",
            "retained_bound_route": "False",
            "source_path": str(ZERO_4279),
            "input_valid_for_claim": "False",
            "notes": "Compact no-flux collar only; open/radiative boundary remains separate.",
        },
        {
            "coefficient_id": "LRC4403_5_cGamma",
            "coefficient": "c_Gamma",
            "residual_role": "local_memory_Gamma_Khat",
            "current_status": "SOLE_PRIVATE_LOCAL_SURVIVOR",
            "private_zero_basis": "False",
            "parent_zero_signed": "False",
            "same_support": "False",
            "public_scope_allowed": "False",
            "retained_bound_route": "True",
            "source_path": str(CLASSIFIER_4279),
            "input_valid_for_claim": "False",
            "notes": "Leading survivor; needs memory no-hair or live profile coefficients.",
        },
        {
            "coefficient_id": "LRC4403_6_cR2",
            "coefficient": "c_R2_or_M_R",
            "residual_role": "curvature_squared_finite_range",
            "current_status": "RETAINED_FINITE_RANGE_BOUND_ROUTE",
            "private_zero_basis": "False",
            "parent_zero_signed": "False",
            "same_support": "False",
            "public_scope_allowed": "False",
            "retained_bound_route": "True",
            "source_path": str(SURVIVOR_4279),
            "input_valid_for_claim": "False",
            "notes": "Needs mass/scale law or finite-range bound rows.",
        },
        {
            "coefficient_id": "LRC4403_7_Lambda_eff",
            "coefficient": "Lambda_eff_local",
            "residual_role": "local_vacuum_tidal",
            "current_status": "RETAINED_LOCAL_TIDAL_BOUND_ROUTE",
            "private_zero_basis": "False",
            "parent_zero_signed": "False",
            "same_support": "False",
            "public_scope_allowed": "False",
            "retained_bound_route": "True",
            "source_path": str(SURVIVOR_4279),
            "input_valid_for_claim": "False",
            "notes": "Needs local scale separation or background-subtraction theorem.",
        },
        {
            "coefficient_id": "LRC4403_8_spin_torsion",
            "coefficient": "c_T_spin",
            "residual_role": "spin_torsion_contact_or_nonstatic",
            "current_status": "RETAINED_SPIN_TORSION_BOUND_ROUTE",
            "private_zero_basis": "False",
            "parent_zero_signed": "False",
            "same_support": "False",
            "public_scope_allowed": "False",
            "retained_bound_route": "True",
            "source_path": str(CLASSIFIER_4279),
            "input_valid_for_claim": "False",
            "notes": "Spinless algebraic elimination or torsion bound row required.",
        },
    ]


def payload_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "LCP4403_0_missing_live_local_residual_payload",
            "arena": "local_GR_Newton_PPN",
            "cGamma_uu_abs": "MISSING_CGAMMA_UU",
            "cGamma_trace_abs": "MISSING_CGAMMA_TRACE",
            "cR2_uu_abs": "MISSING_CR2_UU",
            "cR2_trace_abs": "MISSING_CR2_TRACE",
            "spin_torsion_uu_abs": "MISSING_SPIN_UU",
            "spin_torsion_trace_abs": "MISSING_SPIN_TRACE",
            "boundary_open_uu_abs": "MISSING_BOUNDARY_UU",
            "boundary_open_trace_abs": "MISSING_BOUNDARY_TRACE",
            "Lambda_eff_abs": "MISSING_LAMBDA_EFF",
            "projector_boundary_abs": "MISSING_PROJECTOR_BOUNDARY",
            "K_E_c2_abs": "MISSING_K_E_C2",
            "F_E_threshold": "MISSING_THRESHOLD",
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": "False",
            "notes": "Live payload still needs real survivor coefficients and local support constants.",
        },
        {
            "payload_id": "LCP4403_1_private_zero_schema_nonclaim",
            "arena": "private_zero_schema",
            "cGamma_uu_abs": "0",
            "cGamma_trace_abs": "0",
            "cR2_uu_abs": "0",
            "cR2_trace_abs": "0",
            "spin_torsion_uu_abs": "0",
            "spin_torsion_trace_abs": "0",
            "boundary_open_uu_abs": "0",
            "boundary_open_trace_abs": "0",
            "Lambda_eff_abs": "0",
            "projector_boundary_abs": "0",
            "K_E_c2_abs": "1",
            "F_E_threshold": "0.000001",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim arithmetic check: if every survivor is zero, the payload vanishes.",
        },
        {
            "payload_id": "LCP4403_2_small_survivor_payload_smoke_nonclaim",
            "arena": "small_survivor_payload_schema",
            "cGamma_uu_abs": "0.001",
            "cGamma_trace_abs": "0.001",
            "cR2_uu_abs": "0.0006",
            "cR2_trace_abs": "0.0006",
            "spin_torsion_uu_abs": "0.0003",
            "spin_torsion_trace_abs": "0.0003",
            "boundary_open_uu_abs": "0.0001",
            "boundary_open_trace_abs": "0.0001",
            "Lambda_eff_abs": "0.0005",
            "projector_boundary_abs": "0.0002",
            "K_E_c2_abs": "1",
            "F_E_threshold": "0.01",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row for a bounded survivor residual vector.",
        },
        {
            "payload_id": "LCP4403_3_large_survivor_payload_fail_nonclaim",
            "arena": "large_survivor_payload_fail",
            "cGamma_uu_abs": "0.02",
            "cGamma_trace_abs": "0.02",
            "cR2_uu_abs": "0.01",
            "cR2_trace_abs": "0.01",
            "spin_torsion_uu_abs": "0.01",
            "spin_torsion_trace_abs": "0.01",
            "boundary_open_uu_abs": "0.01",
            "boundary_open_trace_abs": "0.01",
            "Lambda_eff_abs": "0.01",
            "projector_boundary_abs": "0.005",
            "K_E_c2_abs": "1",
            "F_E_threshold": "0.01",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim row proving a large survivor vector fails.",
        },
    ]


def ricci_input_rows(payload_output: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for payload_id in ["LCP4403_1_private_zero_schema_nonclaim", "LCP4403_2_small_survivor_payload_smoke_nonclaim"]:
        payload = next(row for row in payload_output if row["payload_id"] == payload_id)
        rows.append(
            {
                "bound_id": f"RUB4403_from_{payload_id}",
                "arena": payload["arena"],
                "kappa_eff_abs": "0",
                "T_uu_norm": "0",
                "T_trace_norm": "0",
                "E_res_uu_norm": payload["E_res_uu_norm"],
                "E_res_trace_norm": payload["E_res_trace_norm"],
                "Lambda_eff_abs": payload["Lambda_eff_abs"],
                "projector_boundary_abs": payload["projector_boundary_abs"],
                "K_E_c2_abs": "1",
                "F_E_threshold": payload["F_E_threshold"],
                "source_path": str(PAYLOAD_OUTPUT_PATH),
                "support_certificate_path": str(PAYLOAD_OUTPUT_PATH),
                "input_valid_for_claim": "False",
                "notes": f"Ricci runner intake generated from {payload_id}.",
            }
        )
    return rows


def lambda_input_rows(ricci_output: List[Dict[str, str]]) -> List[Dict[str, str]]:
    row = next(row for row in ricci_output if row["bound_id"] == "RUB4403_from_LCP4403_2_small_survivor_payload_smoke_nonclaim")
    return [
        {
            "bound_id": "LCB4403_lambda_from_local_survivor_payload_nonclaim",
            "arena": "lambda_from_local_survivor_payload_schema",
            "F_E_norm": row["F_E_norm"],
            "C_poincare": "1.0",
            "C_elliptic_H2": "2.0",
            "K_lambda_stress": "1.0",
            "K_projection": "1.0",
            "arena_threshold": "0.02",
            "boundary_condition": "zero_mean_Neumann",
            "zero_mode_fixed": "True",
            "boundary_flux_silent": "True",
            "source_path": str(RICCI_OUTPUT_PATH),
            "support_certificate_path": str(RICCI_OUTPUT_PATH),
            "input_valid_for_claim": "False",
            "notes": "Lambda elliptic runner intake generated from the 4403 small survivor residual payload.",
        }
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = {
        "private_zero_subset": "private zeros are usable inside the selector only, not public parent-zero claims",
        "survivor_vector": "c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion and open boundary/projector payloads remain retained",
        "local_Ruu_payload": "payload runner exists, but live survivor coefficients/source paths are missing",
        "lambda_payload": "lambda runner consumes the survivor vector score, but current rows are smoke/nonclaim",
        "local_GR_Newton_PPN": "local claims remain blocked until survivor vector is parent-zeroed or source-bounded",
    }
    return [
        {
            "gate_id": f"CG4403_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(gates.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4403_0",
            "decision": DECISION,
            "summary": "4403 factors the local residual tensor into private-zero channels and retained survivor channels. The private branch can remove c_D, delta_kappa, static Kperp, extra Poynting and compact boundary terms only inside its selector scope. The remaining local Ricci/lambda payload is c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion and open boundary/projector leakage. A new local cosmological/residual gate computes E_res_uu, E_res_trace, R_uu and F_E, then feeds the existing Ricci_uu and lambda payload runners. The next best non-circling target is c_Gamma, because it is the broadest multi-arena survivor.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "summary": "local residual vector factored; survivor payload runner feeds Ricci_uu and lambda runners; cGamma selected next.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4403_0",
            "target": NEXT_TARGET,
            "question": "Can c_Gamma be parent-zeroed by a memory no-hair/stationarity theorem, or can the first live c_Gamma profile row be sourced?",
            "preferred_route": "try the parent memory no-hair proof first: D_t Xi_0=0 and grad_perp Xi_0=0 on the same compact support.",
            "fallback_route": "fill the first source-backed c_Gamma profile row for A_src/A_lap/A_drift, T_res/tau_L, Pi_B and arena projection coefficients.",
            "avoid": "letting c_Gamma hide inside E_res after 4403 has made it the leading survivor.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    classifier_output: List[Dict[str, str]],
    payload_output: List[Dict[str, str]],
    ricci_output: List[Dict[str, str]],
    lambda_output: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 419 PPC4161 transition: Lambda_eff residual zero or local cosmological payload bound

Marker: `{MARKER}`

## Result

4403 turns the `Lambda_eff + E_res` obstruction into a scored survivor vector.

Private selector zeros:

- `c_D`
- `delta_kappa`
- static `Kperp/c_T`
- extra Poynting source
- compact no-flux boundary term

Retained local survivor vector:

- `c_Gamma`
- `c_R2/M_R`
- `Lambda_eff`
- spin/torsion contact or non-static torsion
- open boundary/projector leakage

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"

    text += "\n## Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"

    text += """## Payload Law

In matter vacuum:

`|R_uu| <= |E_surv,uu| + 1/2 |E_surv| + |Lambda_eff| + |B_projector|`.

The corresponding lambda source is:

`|F_E| <= |K_E c^2| |R_uu|`.

No cross-channel cancellation is credited.

## Residual Classifier

"""
    for row in classifier_output:
        text += f"- `{row['coefficient']}`: private_zero_usable=`{row['private_zero_usable']}`, bound_required=`{row['bound_required']}`, contributes_to_private_residual=`{row['contributes_to_private_residual']}`, status=`{row['current_status']}`.\n"

    text += "\n## Local Payload Runner\n\n"
    for row in payload_output:
        text += f"- `{row['payload_id']}`: schema_ready=`{row['schema_ready']}`, E_res_uu=`{row['E_res_uu_norm']}`, E_res_trace=`{row['E_res_trace_norm']}`, Ruu_bound=`{row['Ruu_abs_bound']}`, F_E=`{row['F_E_norm']}`, status=`{row['current_status']}`.\n"

    text += "\n## Ricci Runner Feed\n\n"
    for row in ricci_output:
        text += f"- `{row['bound_id']}`: Ruu_abs_bound=`{row['Ruu_abs_bound']}`, F_E_norm=`{row['F_E_norm']}`, status=`{row['current_status']}`.\n"

    text += "\n## Lambda Runner Feed\n\n"
    for row in lambda_output:
        text += f"- `{row['bound_id']}`: payload_score=`{row['lambda_curvature_payload_score']}`, threshold=`{row['arena_threshold']}`, status=`{row['current_status']}`.\n"

    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"

    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    write_text(
        DOC_PATH,
        f"""# 4403 Y5 R2FR: Lambda_eff residual zero or local cosmological payload bound

Marker: `{MARKER}`

## Private checkpoint

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
""",
    )


def write_spine_update() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4403 local spine update: residual vector factored into private zeros and survivor payload

Marker: `{MARKER}`

Spine update: the local `E_res + Lambda_eff` obstruction is now factored. Private selector zeros cover `c_D`, `delta_kappa`, static `Kperp/c_T`, extra Poynting and compact boundary terms. The retained local survivor vector is `c_Gamma`, `c_R2/M_R`, `Lambda_eff`, spin/torsion and open boundary/projector leakage. The survivor vector now feeds the Ricci_uu and lambda runners directly. The leading next target is `c_Gamma`.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4403 packet update: local residual payload vector

Marker: `{PACKET_MARKER}`

Packet update: 4403 creates an executable no-cancellation local residual payload vector and routes it through the existing Ricci_uu and lambda payload runners.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4403 factors the local residual tensor into private-zero channels and retained survivor channels. Inside the private selector, c_D, delta_kappa, static Kperp/c_T, extra Poynting and compact boundary terms are removed only as private zeros. The retained local survivor vector is c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion and open boundary/projector leakage. A local residual payload runner now computes E_res_uu, E_res_trace, R_uu and F_E, then feeds the existing Ricci_uu and lambda payload runners. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4403 source register, local residual derivations, residual classifier input/output, local cosmological payload input/output, Ricci-from-residual rows, lambda-from-residual rows, claim gates, decision, status, next target and validation CSV.",
            "local_residual_vector_factored_survivor_payload_runner_ready_nonclaim",
            "Derive c_Gamma memory no-hair or source the first live c_Gamma profile row.",
            "Promoting private zeros to public claims, hiding c_Gamma in E_res, or allowing residual channels to cancel numerically.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4403_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_DERIVATIONS.csv")
    classifier_output = read_csv(CLASSIFIER_OUTPUT_PATH)
    payload_output = read_csv(PAYLOAD_OUTPUT_PATH)
    ricci_output = read_csv(RICCI_OUTPUT_PATH)
    lambda_output = read_csv(LAMBDA_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4403_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4403_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4403_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4403_2_factorization_written", any(row["derivation_id"] == "LCR4403_0_residual_tensor_factorization" for row in derivations), "residual tensor factorization written")
    add("VAL4403_3_payload_law_written", any(row["derivation_id"] == "LCR4403_1_local_Ruu_residual_payload_law" for row in derivations), "local Ruu payload law written")
    add("VAL4403_4_Lambda_scale_written", any(row["derivation_id"] == "LCR4403_2_Lambda_eff_scale_law" for row in derivations), "Lambda_eff scale law written")
    add("VAL4403_5_cGamma_priority_written", any(row["derivation_id"] == "LCR4403_3_survivor_priority" for row in derivations), "cGamma priority written")
    add("VAL4403_6_private_zero_rows_private_only", any(row["coefficient"] == "c_D" and row["current_status"] == "PRIVATE_ZERO_USABLE_FOR_SELECTOR_ONLY" for row in classifier_output), "private zero rows are private-only")
    add("VAL4403_7_cGamma_retained", any(row["coefficient"] == "c_Gamma" and row["bound_required"] == "True" for row in classifier_output), "cGamma retained as bound route")
    add("VAL4403_8_Lambda_retained", any(row["coefficient"] == "Lambda_eff_local" and row["bound_required"] == "True" for row in classifier_output), "Lambda_eff retained as bound route")
    add("VAL4403_9_zero_payload_computes", any(row["payload_id"] == "LCP4403_1_private_zero_schema_nonclaim" and row["F_E_norm"] == "0" for row in payload_output), "zero payload computes")
    add("VAL4403_10_small_payload_computes", any(row["payload_id"] == "LCP4403_2_small_survivor_payload_smoke_nonclaim" and row["within_threshold"] == "True" for row in payload_output), "small survivor payload computes")
    add("VAL4403_11_large_payload_fails", any(row["payload_id"] == "LCP4403_3_large_survivor_payload_fail_nonclaim" and row["current_status"] == "LOCAL_COSMOLOGICAL_RESIDUAL_PAYLOAD_FAILS_THRESHOLD" for row in payload_output), "large survivor payload fails")
    add("VAL4403_12_ricci_feed_computes", any(row["bound_id"] == "RUB4403_from_LCP4403_2_small_survivor_payload_smoke_nonclaim" and row["schema_ready"] == "True" for row in ricci_output), "Ricci runner consumes survivor score")
    add("VAL4403_13_lambda_feed_computes", any(row["bound_id"] == "LCB4403_lambda_from_local_survivor_payload_nonclaim" and row["schema_ready"] == "True" for row in lambda_output), "lambda runner consumes survivor score")
    add("VAL4403_14_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4403_15_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4403_16_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4403_17_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4403_18_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4403_19_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4403_20_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4403_21_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4403_22_gate_script_exists", LOCAL_GATE_PATH.exists() and "def evaluate_payload_rows" in read_text(LOCAL_GATE_PATH), "local residual gate exists")
    add("VAL4403_23_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = derivation_rows()
    classifier_inputs = classifier_input_rows()
    payload_inputs = payload_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_paths: List[Path] = [CLASSIFIER_INPUT_PATH, PAYLOAD_INPUT_PATH]

    write_csv(CLASSIFIER_INPUT_PATH, classifier_inputs)
    classifier_output = evaluate_classifier_rows(CLASSIFIER_INPUT_PATH)
    write_csv(CLASSIFIER_OUTPUT_PATH, classifier_output)
    csv_paths.append(CLASSIFIER_OUTPUT_PATH)

    write_csv(PAYLOAD_INPUT_PATH, payload_inputs)
    payload_output = evaluate_payload_rows(PAYLOAD_INPUT_PATH)
    write_csv(PAYLOAD_OUTPUT_PATH, payload_output)
    csv_paths.append(PAYLOAD_OUTPUT_PATH)

    ricci_inputs = ricci_input_rows(payload_output)
    write_csv(RICCI_INPUT_PATH, ricci_inputs)
    ricci_output = evaluate_ricci_bound_rows(RICCI_INPUT_PATH)
    write_csv(RICCI_OUTPUT_PATH, ricci_output)
    csv_paths.extend([RICCI_INPUT_PATH, RICCI_OUTPUT_PATH])

    lambda_inputs = lambda_input_rows(ricci_output)
    write_csv(LAMBDA_INPUT_PATH, lambda_inputs)
    lambda_output = evaluate_lambda_bound_rows(LAMBDA_INPUT_PATH)
    write_csv(LAMBDA_OUTPUT_PATH, lambda_output)
    csv_paths.extend([LAMBDA_INPUT_PATH, LAMBDA_OUTPUT_PATH])

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4403_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4403_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4403_DECISION.csv": decisions,
        "P8_Y5_R2FR_4403_STATUS.csv": statuses,
        "P8_Y5_R2FR_4403_NEXT_TARGET.csv": next_targets,
    }

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(
        sources,
        derivations,
        classifier_output,
        payload_output,
        ricci_output,
        lambda_output,
        gates,
        decisions,
        next_targets,
    )
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
